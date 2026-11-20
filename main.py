import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from calculator import calculate_session_summary, session_is_settled
from database import db_cursor, init_db

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="SmashPay - Chia Tiền Cầu Lông", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# ---------- Pydantic Models ----------


class MemberIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    bank_id: str = Field(default="", max_length=30)
    account_no: str = Field(default="", max_length=30)
    account_name: str = Field(default="", max_length=80)
    is_regular: bool = True
    default_payer_id: Optional[int] = None


class SessionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    played_at: str = Field(..., min_length=4, max_length=30)
    parking_fee: int = Field(default=5000, ge=0)
    notes: str = Field(default="", max_length=500)
    participant_ids: List[int] = Field(default_factory=list)
    participant_payers: Dict[int, Optional[int]] = Field(default_factory=dict)
    template_session_id: Optional[int] = None


class TemplateFlag(BaseModel):
    is_template: bool


class SessionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    played_at: Optional[str] = Field(default=None, min_length=4, max_length=30)
    parking_fee: Optional[int] = Field(default=None, ge=0)
    notes: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, pattern="^(open|settled)$")
    participant_ids: Optional[List[int]] = None
    participant_payers: Optional[Dict[int, Optional[int]]] = None


class ParticipantPayerUpdate(BaseModel):
    payer_member_id: Optional[int] = None


class ExpenseItemIn(BaseModel):
    item_name: str = Field(default="", max_length=120)
    amount: int = Field(default=0, ge=0)
    pricing_mode: str = Field(default="per_person", pattern="^(per_person|split_total)$")
    participant_ids: List[int] = Field(default_factory=list)


class ExpenseIn(BaseModel):
    category: str = Field(..., pattern="^(court|shuttle|parking|snack|drink|other)$")
    title: str = Field(..., min_length=1, max_length=120)
    split_type: str = Field(..., pattern="^(equal_split|parking|itemized)$")
    payer_id: Optional[int] = None
    total_amount: int = Field(default=0, ge=0)
    parking_mode: Optional[str] = Field(default=None, pattern="^(separate_payer|included_in_court)$")
    unit_fee: int = Field(default=5000, ge=0)
    participant_ids: List[int] = Field(default_factory=list)
    items: List[ExpenseItemIn] = Field(default_factory=list)


class SettlementToggle(BaseModel):
    is_paid: bool
    paid_at: Optional[str] = None


# ---------- Internal Helpers ----------


def _load_session_full(cur, session_id: int) -> Dict[str, Any]:
    cur.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    sess_row = cur.fetchone()
    if not sess_row:
        raise HTTPException(status_code=404, detail="Không tìm thấy buổi đánh cầu.")
    session = dict(sess_row)

    cur.execute(
        """
        SELECT m.*, sp.payer_member_id, mp.name AS payer_member_name
        FROM session_participants sp
        JOIN members m ON m.id = sp.member_id
        LEFT JOIN members mp ON mp.id = sp.payer_member_id
        WHERE sp.session_id = ?
        ORDER BY m.name COLLATE NOCASE ASC
        """,
        (session_id,),
    )
    participants = [dict(r) for r in cur.fetchall()]

    cur.execute(
        """
        SELECT e.*, m.name AS payer_name
        FROM expenses e
        LEFT JOIN members m ON m.id = e.payer_id
        WHERE e.session_id = ?
        ORDER BY e.id ASC
        """,
        (session_id,),
    )
    expense_rows = [dict(r) for r in cur.fetchall()]

    expenses: List[Dict[str, Any]] = []
    for exp in expense_rows:
        exp_id = exp["id"]
        cur.execute(
            "SELECT member_id FROM expense_participants WHERE expense_id = ? ORDER BY member_id ASC",
            (exp_id,),
        )
        exp["participant_ids"] = [r["member_id"] for r in cur.fetchall()]

        cur.execute(
            "SELECT * FROM expense_items WHERE expense_id = ? ORDER BY id ASC",
            (exp_id,),
        )
        item_rows = [dict(r) for r in cur.fetchall()]
        for item in item_rows:
            cur.execute(
                "SELECT member_id FROM expense_item_participants WHERE item_id = ? ORDER BY member_id ASC",
                (item["id"],),
            )
            item["participant_ids"] = [r["member_id"] for r in cur.fetchall()]
        exp["items"] = item_rows
        expenses.append(exp)

    summary = calculate_session_summary(participants, expenses)

    # Sync settlements only when transfer set actually changes, preserving stable IDs and is_paid flags
    cur.execute("SELECT * FROM settlements WHERE session_id = ?", (session_id,))
    existing_rows = cur.fetchall()
    existing_map = {
        (row["from_member_id"], row["to_member_id"], row["amount"]): (row["is_paid"], row["paid_at"])
        for row in existing_rows
    }
    desired_keys = [
        (tr["from_member_id"], tr["to_member_id"], tr["amount"])
        for tr in summary["transfers"]
    ]

    if sorted(existing_map.keys()) != sorted(desired_keys):
        cur.execute("DELETE FROM settlements WHERE session_id = ?", (session_id,))
        for tr in summary["transfers"]:
            key = (tr["from_member_id"], tr["to_member_id"], tr["amount"])
            is_paid, paid_at = existing_map.get(key, (0, None))
            cur.execute(
                """
                INSERT INTO settlements (session_id, from_member_id, to_member_id, amount, is_paid, paid_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (session_id, tr["from_member_id"], tr["to_member_id"], tr["amount"], is_paid, paid_at),
            )

    cur.execute(
        """
        SELECT
            s.*,
            mf.name AS from_name,
            mt.name AS to_name,
            mt.bank_id AS to_bank_id,
            mt.account_no AS to_account_no,
            mt.account_name AS to_account_name
        FROM settlements s
        JOIN members mf ON mf.id = s.from_member_id
        JOIN members mt ON mt.id = s.to_member_id
        WHERE s.session_id = ?
        ORDER BY s.is_paid ASC, s.amount DESC
        """,
        (session_id,),
    )
    settlements = [dict(r) for r in cur.fetchall()]

    # Attach computed total to each expense for UI convenience
    computed_map = summary.get("expense_computed_totals", {})
    meta_map = summary.get("expense_meta", {})
    for exp in expenses:
        meta = meta_map.get(exp["id"], {})
        exp["computed_total"] = computed_map.get(exp["id"], exp["total_amount"])
        exp["invoice_total"] = meta.get("invoice_total", exp["computed_total"])
        exp["parking_deducted"] = meta.get("parking_deducted", 0)
        exp["parking_unfunded"] = meta.get("parking_unfunded", 0)
        exp["parking_unmatched"] = meta.get("parking_unmatched", 0)

    desired_status = "settled" if session_is_settled(summary["member_summaries"], settlements) else "open"
    if session.get("status") != desired_status:
        cur.execute("UPDATE sessions SET status = ? WHERE id = ?", (desired_status, session_id))
        session["status"] = desired_status

    return {
        "session": session,
        "participants": participants,
        "expenses": expenses,
        "summary": {
            "total_spent": summary["total_spent"],
            "total_paid": summary["total_paid"],
            "category_totals": summary["category_totals"],
            "member_summaries": summary["member_summaries"],
            "warnings": summary["warnings"],
        },
        "settlements": settlements,
    }


# ---------- Members API ----------


@app.get("/api/members")
def list_members(include_inactive: bool = False):
    with db_cursor() as cur:
        query = """
            SELECT m.*, mp.name AS default_payer_name
            FROM members m
            LEFT JOIN members mp ON mp.id = m.default_payer_id
            WHERE 1=1
        """
        if not include_inactive:
            query += " AND m.is_active = 1"
        query += " ORDER BY m.is_regular DESC, m.name COLLATE NOCASE ASC"
        cur.execute(query)
        return [dict(r) for r in cur.fetchall()]


@app.post("/api/members", status_code=201)
def create_member(payload: MemberIn):
    with db_cursor() as cur:
        default_payer = payload.default_payer_id
        cur.execute(
            """
            INSERT INTO members (name, bank_id, account_no, account_name, is_regular, default_payer_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload.name.strip(),
                payload.bank_id.strip().upper(),
                payload.account_no.strip(),
                payload.account_name.strip().upper(),
                1 if payload.is_regular else 0,
                default_payer,
            ),
        )
        member_id = cur.lastrowid
        cur.execute("SELECT m.*, mp.name AS default_payer_name FROM members m LEFT JOIN members mp ON mp.id = m.default_payer_id WHERE m.id = ?", (member_id,))
        return dict(cur.fetchone())


@app.put("/api/members/{member_id}")
def update_member(member_id: int, payload: MemberIn):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM members WHERE id = ?", (member_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy thành viên.")
        default_payer = payload.default_payer_id
        if default_payer == member_id:
            default_payer = None
        cur.execute(
            """
            UPDATE members
            SET name = ?, bank_id = ?, account_no = ?, account_name = ?, is_regular = ?, default_payer_id = ?
            WHERE id = ?
            """,
            (
                payload.name.strip(),
                payload.bank_id.strip().upper(),
                payload.account_no.strip(),
                payload.account_name.strip().upper(),
                1 if payload.is_regular else 0,
                default_payer,
                member_id,
            ),
        )
        cur.execute("SELECT m.*, mp.name AS default_payer_name FROM members m LEFT JOIN members mp ON mp.id = m.default_payer_id WHERE m.id = ?", (member_id,))
        return dict(cur.fetchone())


@app.delete("/api/members/{member_id}")
def delete_member(member_id: int):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM members WHERE id = ?", (member_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy thành viên.")
        # Soft delete so historical sessions remain intact
        cur.execute("UPDATE members SET is_active = 0 WHERE id = ?", (member_id,))
        return {"ok": True}


@app.post("/api/members/{member_id}/restore")
def restore_member(member_id: int):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM members WHERE id = ?", (member_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy thành viên.")
        cur.execute("UPDATE members SET is_active = 1 WHERE id = ?", (member_id,))
        cur.execute(
            "SELECT m.*, mp.name AS default_payer_name FROM members m LEFT JOIN members mp ON mp.id = m.default_payer_id WHERE m.id = ?",
            (member_id,),
        )
        return dict(cur.fetchone())


# ---------- Sessions API ----------


@app.get("/api/sessions")
def list_sessions():
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT
                s.*,
                (SELECT COUNT(*) FROM session_participants sp WHERE sp.session_id = s.id) AS participant_count,
                (SELECT COUNT(*) FROM settlements st WHERE st.session_id = s.id) AS total_transfers,
                (SELECT COUNT(*) FROM settlements st WHERE st.session_id = s.id AND st.is_paid = 1) AS paid_transfers
            FROM sessions s
            ORDER BY s.played_at DESC, s.id DESC
            """
        )
        rows = [dict(r) for r in cur.fetchall()]
        # Compute total_spent accurately for each session
        for row in rows:
            full = _load_session_full(cur, row["id"])
            row["status"] = full["session"]["status"]
            row["total_spent"] = full["summary"]["total_spent"]
            row["total_transfers"] = len(full["settlements"])
            row["paid_transfers"] = sum(1 for st in full["settlements"] if st["is_paid"])
        return rows


@app.post("/api/sessions", status_code=201)
def create_session(payload: SessionCreate):
    with db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO sessions (title, played_at, parking_fee, notes)
            VALUES (?, ?, ?, ?)
            """,
            (payload.title.strip(), payload.played_at.strip(), payload.parking_fee, payload.notes.strip()),
        )
        session_id = cur.lastrowid
        pids = set(payload.participant_ids)
        for mid in pids:
            payer = payload.participant_payers.get(mid)
            if payer is None:
                cur.execute("SELECT default_payer_id FROM members WHERE id = ?", (mid,))
                d_row = cur.fetchone()
                if d_row and d_row["default_payer_id"] and d_row["default_payer_id"] in pids:
                    payer = d_row["default_payer_id"]
            if payer == mid or (payer and payer not in pids):
                payer = None
            cur.execute(
                "INSERT OR IGNORE INTO session_participants (session_id, member_id, payer_member_id) VALUES (?, ?, ?)",
                (session_id, mid, payer),
            )
        if payload.template_session_id:
            cur.execute("SELECT id FROM sessions WHERE id = ?", (payload.template_session_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Không tìm thấy buổi dùng làm mẫu.")
            _copy_session_expenses(cur, payload.template_session_id, session_id, pids)
        return _load_session_full(cur, session_id)


def _copy_session_expenses(cur, source_id: int, dest_id: int, participant_ids: set) -> None:
    """Copy the expense form, including amounts, onto a new session.

    People who are not coming this time are dropped from each split. A fixed
    invoice stays the same amount and is split among whoever remains.
    """
    allowed = set(participant_ids)
    cur.execute("SELECT * FROM expenses WHERE session_id = ? ORDER BY id ASC", (source_id,))
    expenses = [dict(row) for row in cur.fetchall()]
    for exp in expenses:
        cur.execute(
            "SELECT member_id FROM expense_participants WHERE expense_id = ? ORDER BY member_id ASC",
            (exp["id"],),
        )
        kept_ids = [row["member_id"] for row in cur.fetchall() if row["member_id"] in allowed]

        cur.execute("SELECT * FROM expense_items WHERE expense_id = ? ORDER BY id ASC", (exp["id"],))
        copied_items = []
        for item in cur.fetchall():
            item = dict(item)
            cur.execute(
                "SELECT member_id FROM expense_item_participants WHERE item_id = ? ORDER BY member_id ASC",
                (item["id"],),
            )
            item_ids = [row["member_id"] for row in cur.fetchall() if row["member_id"] in allowed]
            if item_ids:
                copied_items.append((item, item_ids))

        if exp["split_type"] in ("equal_split", "parking") and not kept_ids:
            continue
        if exp["split_type"] == "itemized" and not copied_items:
            continue

        if exp["split_type"] == "parking":
            stored_total = int(exp["unit_fee"] or 0) * len(kept_ids)
        elif exp["split_type"] == "itemized":
            stored_total = 0
            for item, item_ids in copied_items:
                if item["pricing_mode"] == "per_person":
                    stored_total += int(item["amount"] or 0) * len(item_ids)
                else:
                    stored_total += int(item["amount"] or 0)
        else:
            stored_total = int(exp["total_amount"] or 0)

        cur.execute(
            """
            INSERT INTO expenses (session_id, category, title, split_type, payer_id, total_amount, parking_mode, unit_fee)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dest_id,
                exp["category"],
                exp["title"],
                exp["split_type"],
                exp["payer_id"],
                stored_total,
                exp["parking_mode"],
                exp["unit_fee"],
            ),
        )
        new_expense_id = cur.lastrowid
        if exp["split_type"] in ("equal_split", "parking"):
            for mid in kept_ids:
                cur.execute(
                    "INSERT OR IGNORE INTO expense_participants (expense_id, member_id) VALUES (?, ?)",
                    (new_expense_id, mid),
                )
        else:
            for item, item_ids in copied_items:
                cur.execute(
                    """
                    INSERT INTO expense_items (expense_id, item_name, amount, pricing_mode)
                    VALUES (?, ?, ?, ?)
                    """,
                    (new_expense_id, item["item_name"], item["amount"], item["pricing_mode"]),
                )
                new_item_id = cur.lastrowid
                for mid in item_ids:
                    cur.execute(
                        "INSERT OR IGNORE INTO expense_item_participants (item_id, member_id) VALUES (?, ?)",
                        (new_item_id, mid),
                    )


@app.put("/api/sessions/{session_id}/template")
def set_session_template(session_id: int, payload: TemplateFlag):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy buổi đánh cầu.")
        if payload.is_template:
            cur.execute("UPDATE sessions SET is_template = 0")
            cur.execute("UPDATE sessions SET is_template = 1 WHERE id = ?", (session_id,))
        else:
            cur.execute("UPDATE sessions SET is_template = 0 WHERE id = ?", (session_id,))
        return _load_session_full(cur, session_id)


@app.get("/api/sessions/{session_id}")
def get_session(session_id: int):
    with db_cursor() as cur:
        return _load_session_full(cur, session_id)


@app.put("/api/sessions/{session_id}")
def update_session(session_id: int, payload: SessionUpdate):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy buổi đánh cầu.")

        title = payload.title.strip() if payload.title is not None else row["title"]
        played_at = payload.played_at.strip() if payload.played_at is not None else row["played_at"]
        parking_fee = payload.parking_fee if payload.parking_fee is not None else row["parking_fee"]
        notes = payload.notes.strip() if payload.notes is not None else row["notes"]
        status = payload.status if payload.status is not None else row["status"]

        cur.execute(
            """
            UPDATE sessions
            SET title = ?, played_at = ?, parking_fee = ?, notes = ?, status = ?,
                updated_at = datetime('now', 'localtime')
            WHERE id = ?
            """,
            (title, played_at, parking_fee, notes, status, session_id),
        )

        if payload.participant_ids is not None:
            pids = set(payload.participant_ids)
            cur.execute("SELECT member_id, payer_member_id FROM session_participants WHERE session_id = ?", (session_id,))
            existing_payers = {r["member_id"]: r["payer_member_id"] for r in cur.fetchall()}

            cur.execute("DELETE FROM session_participants WHERE session_id = ?", (session_id,))
            for mid in pids:
                if payload.participant_payers is not None and mid in payload.participant_payers:
                    payer = payload.participant_payers[mid]
                else:
                    payer = existing_payers.get(mid)
                    if payer is None:
                        cur.execute("SELECT default_payer_id FROM members WHERE id = ?", (mid,))
                        d_row = cur.fetchone()
                        if d_row and d_row["default_payer_id"] and d_row["default_payer_id"] in pids:
                            payer = d_row["default_payer_id"]
                if payer == mid or (payer and payer not in pids):
                    payer = None
                cur.execute(
                    "INSERT OR IGNORE INTO session_participants (session_id, member_id, payer_member_id) VALUES (?, ?, ?)",
                    (session_id, mid, payer),
                )

        return _load_session_full(cur, session_id)


@app.put("/api/sessions/{session_id}/participants/{member_id}/payer")
def set_participant_payer(session_id: int, member_id: int, payload: ParticipantPayerUpdate):
    with db_cursor() as cur:
        cur.execute("SELECT 1 FROM session_participants WHERE session_id = ? AND member_id = ?", (session_id, member_id))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Thành viên không nằm trong buổi đánh.")

        payer = payload.payer_member_id
        if payer == member_id:
            payer = None
        if payer is not None:
            cur.execute("SELECT 1 FROM session_participants WHERE session_id = ? AND member_id = ?", (session_id, payer))
            if not cur.fetchone():
                raise HTTPException(status_code=400, detail="Người trả thay phải cùng tham gia buổi đánh này.")

        cur.execute(
            "UPDATE session_participants SET payer_member_id = ? WHERE session_id = ? AND member_id = ?",
            (payer, session_id, member_id),
        )
        return _load_session_full(cur, session_id)


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: int):
    with db_cursor() as cur:
        cur.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy buổi đánh cầu.")
        return {"ok": True}


# ---------- Expenses API ----------


def _write_expense_children(cur, expense_id: int, payload: ExpenseIn) -> None:
    cur.execute("DELETE FROM expense_participants WHERE expense_id = ?", (expense_id,))
    cur.execute("DELETE FROM expense_items WHERE expense_id = ?", (expense_id,))

    if payload.split_type in ("equal_split", "parking"):
        for mid in set(payload.participant_ids):
            cur.execute(
                "INSERT OR IGNORE INTO expense_participants (expense_id, member_id) VALUES (?, ?)",
                (expense_id, mid),
            )
    elif payload.split_type == "itemized":
        for item in payload.items:
            cur.execute(
                """
                INSERT INTO expense_items (expense_id, item_name, amount, pricing_mode)
                VALUES (?, ?, ?, ?)
                """,
                (expense_id, item.item_name.strip(), item.amount, item.pricing_mode),
            )
            item_id = cur.lastrowid
            for mid in set(item.participant_ids):
                cur.execute(
                    "INSERT OR IGNORE INTO expense_item_participants (item_id, member_id) VALUES (?, ?)",
                    (item_id, mid),
                )


def _compute_stored_total(payload: ExpenseIn) -> int:
    if payload.split_type == "equal_split":
        return payload.total_amount
    if payload.split_type == "parking":
        return payload.unit_fee * len(set(payload.participant_ids))
    if payload.split_type == "itemized":
        total = 0
        for item in payload.items:
            cnt = len(set(item.participant_ids))
            if cnt == 0:
                continue
            if item.pricing_mode == "per_person":
                total += item.amount * cnt
            else:
                total += item.amount
        return total
    return payload.total_amount


@app.post("/api/sessions/{session_id}/expenses", status_code=201)
def create_expense(session_id: int, payload: ExpenseIn):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy buổi đánh cầu.")

        stored_total = _compute_stored_total(payload)
        cur.execute(
            """
            INSERT INTO expenses (session_id, category, title, split_type, payer_id, total_amount, parking_mode, unit_fee)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                payload.category,
                payload.title.strip(),
                payload.split_type,
                payload.payer_id,
                stored_total,
                payload.parking_mode,
                payload.unit_fee,
            ),
        )
        expense_id = cur.lastrowid
        _write_expense_children(cur, expense_id, payload)
        cur.execute(
            "UPDATE sessions SET updated_at = datetime('now', 'localtime') WHERE id = ?",
            (session_id,),
        )
        return _load_session_full(cur, session_id)


@app.put("/api/expenses/{expense_id}")
def update_expense(expense_id: int, payload: ExpenseIn):
    with db_cursor() as cur:
        cur.execute("SELECT session_id FROM expenses WHERE id = ?", (expense_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy khoản chi.")
        session_id = row["session_id"]

        stored_total = _compute_stored_total(payload)
        cur.execute(
            """
            UPDATE expenses
            SET category = ?, title = ?, split_type = ?, payer_id = ?,
                total_amount = ?, parking_mode = ?, unit_fee = ?
            WHERE id = ?
            """,
            (
                payload.category,
                payload.title.strip(),
                payload.split_type,
                payload.payer_id,
                stored_total,
                payload.parking_mode,
                payload.unit_fee,
                expense_id,
            ),
        )
        _write_expense_children(cur, expense_id, payload)
        cur.execute(
            "UPDATE sessions SET updated_at = datetime('now', 'localtime') WHERE id = ?",
            (session_id,),
        )
        return _load_session_full(cur, session_id)


@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int):
    with db_cursor() as cur:
        cur.execute("SELECT session_id FROM expenses WHERE id = ?", (expense_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy khoản chi.")
        session_id = row["session_id"]
        cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        cur.execute(
            "UPDATE sessions SET updated_at = datetime('now', 'localtime') WHERE id = ?",
            (session_id,),
        )
        return _load_session_full(cur, session_id)


# ---------- Settlements API ----------


@app.patch("/api/settlements/{settlement_id}")
def toggle_settlement(settlement_id: int, payload: SettlementToggle):
    with db_cursor() as cur:
        cur.execute("SELECT session_id FROM settlements WHERE id = ?", (settlement_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch.")
        session_id = row["session_id"]
        if payload.is_paid:
            paid_at = payload.paid_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            paid_at = None
        cur.execute(
            "UPDATE settlements SET is_paid = ?, paid_at = ? WHERE id = ?",
            (1 if payload.is_paid else 0, paid_at, settlement_id),
        )

        return _load_session_full(cur, session_id)


# ---------- Health & Static Frontend ----------


@app.get("/api/health")
def health():
    return {"status": "ok"}


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Frontend not found"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
