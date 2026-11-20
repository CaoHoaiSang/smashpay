import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from calculator import calculate_session_summary, session_is_settled
from database import backup_db_daily, db_cursor, init_db, make_code

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
    backup_db_daily()


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


class GroupCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)


class GroupJoin(BaseModel):
    code: str = Field(..., min_length=4, max_length=20)


# ---------- Group access ----------


def require_access(authorization: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Hãy vào nhóm trước.")
    token = authorization.split(" ", 1)[1].strip()
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT t.token, t.role, t.group_id, g.name, g.invite_code, g.owner_code
            FROM access_tokens t
            JOIN groups g ON g.id = t.group_id
            WHERE t.token = ?
            """,
            (token,),
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="Phiên nhóm không còn. Hãy vào lại bằng mã nhóm.")
    return dict(row)


def require_owner(access: Dict[str, Any] = Depends(require_access)) -> Dict[str, Any]:
    if access["role"] != "owner":
        raise HTTPException(status_code=403, detail="Chỉ chủ nhóm làm được việc này.")
    return access


def _public_group(access: Dict[str, Any]) -> Dict[str, Any]:
    group = {
        "id": access["group_id"],
        "name": access["name"],
        "invite_code": access["invite_code"],
        "role": access["role"],
    }
    if access["role"] == "owner":
        group["owner_code"] = access["owner_code"]
    return group


def _issue_token(cur, group_id: int, role: str) -> str:
    token = make_code(24)
    cur.execute(
        "INSERT INTO access_tokens (token, group_id, role) VALUES (?, ?, ?)",
        (token, group_id, role),
    )
    return token


def _assert_members_in_group(cur, member_ids: List[int], group_id: int) -> None:
    ids = list({int(mid) for mid in member_ids})
    if not ids:
        return
    placeholders = ",".join("?" for _ in ids)
    cur.execute(
        f"SELECT id FROM members WHERE group_id = ? AND id IN ({placeholders})",
        (group_id, *ids),
    )
    found = {row["id"] for row in cur.fetchall()}
    if found != set(ids):
        raise HTTPException(status_code=400, detail="Có thành viên không thuộc nhóm này.")


def _normalize_code(code: str) -> str:
    return "".join(ch for ch in code.upper() if ch.isalnum())


def _fresh_code(cur, column: str, length: int) -> str:
    if column not in ("invite_code", "owner_code"):
        raise HTTPException(status_code=500, detail="Không tạo được mã nhóm.")
    for _ in range(8):
        code = make_code(length)
        cur.execute(f"SELECT 1 FROM groups WHERE {column} = ?", (code,))
        if not cur.fetchone():
            return code
    raise HTTPException(status_code=500, detail="Không tạo được mã nhóm. Thử lại.")


def _legacy_unclaimed(cur) -> bool:
    cur.execute("SELECT COUNT(*) AS n FROM groups")
    groups = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(*) AS n FROM access_tokens")
    tokens = cur.fetchone()["n"]
    return groups == 1 and tokens == 0


def _expense_member_ids(payload: ExpenseIn) -> List[int]:
    ids: List[int] = []
    if payload.payer_id:
        ids.append(payload.payer_id)
    ids.extend(payload.participant_ids)
    for item in payload.items:
        ids.extend(item.participant_ids)
    return ids


def _group_login(cur, group_row, role: str) -> Dict[str, Any]:
    token = _issue_token(cur, group_row["id"], role)
    group = {
        "id": group_row["id"],
        "name": group_row["name"],
        "invite_code": group_row["invite_code"],
        "role": role,
    }
    if role == "owner":
        group["owner_code"] = group_row["owner_code"]
    return {"token": token, "group": group}


# ---------- Internal Helpers ----------


def _load_session_full(cur, session_id: int, group_id: int) -> Dict[str, Any]:
    cur.execute("SELECT * FROM sessions WHERE id = ? AND group_id = ?", (session_id, group_id))
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
def list_members(include_inactive: bool = False, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        query = """
            SELECT m.*, mp.name AS default_payer_name
            FROM members m
            LEFT JOIN members mp ON mp.id = m.default_payer_id
            WHERE m.group_id = ?
        """
        params: List[Any] = [access["group_id"]]
        if not include_inactive:
            query += " AND m.is_active = 1"
        query += " ORDER BY m.is_regular DESC, m.name COLLATE NOCASE ASC"
        cur.execute(query, params)
        return [dict(r) for r in cur.fetchall()]


@app.post("/api/members", status_code=201)
def create_member(payload: MemberIn, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        default_payer = payload.default_payer_id
        if default_payer is not None:
            _assert_members_in_group(cur, [default_payer], access["group_id"])
        cur.execute(
            """
            INSERT INTO members (name, bank_id, account_no, account_name, is_regular, default_payer_id, group_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.name.strip(),
                payload.bank_id.strip().upper(),
                payload.account_no.strip(),
                payload.account_name.strip().upper(),
                1 if payload.is_regular else 0,
                default_payer,
                access["group_id"],
            ),
        )
        member_id = cur.lastrowid
        cur.execute("SELECT m.*, mp.name AS default_payer_name FROM members m LEFT JOIN members mp ON mp.id = m.default_payer_id WHERE m.id = ?", (member_id,))
        return dict(cur.fetchone())


@app.put("/api/members/{member_id}")
def update_member(member_id: int, payload: MemberIn, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        _assert_members_in_group(cur, [member_id], access["group_id"])
        default_payer = payload.default_payer_id
        if default_payer == member_id:
            default_payer = None
        if default_payer is not None:
            _assert_members_in_group(cur, [default_payer], access["group_id"])
        cur.execute(
            """
            UPDATE members
            SET name = ?, bank_id = ?, account_no = ?, account_name = ?, is_regular = ?, default_payer_id = ?
            WHERE id = ? AND group_id = ?
            """,
            (
                payload.name.strip(),
                payload.bank_id.strip().upper(),
                payload.account_no.strip(),
                payload.account_name.strip().upper(),
                1 if payload.is_regular else 0,
                default_payer,
                member_id,
                access["group_id"],
            ),
        )
        cur.execute("SELECT m.*, mp.name AS default_payer_name FROM members m LEFT JOIN members mp ON mp.id = m.default_payer_id WHERE m.id = ?", (member_id,))
        return dict(cur.fetchone())


@app.delete("/api/members/{member_id}")
def delete_member(member_id: int, access: Dict[str, Any] = Depends(require_owner)):
    with db_cursor() as cur:
        _assert_members_in_group(cur, [member_id], access["group_id"])
        cur.execute("UPDATE members SET is_active = 0 WHERE id = ? AND group_id = ?", (member_id, access["group_id"]))
        return {"ok": True}


@app.post("/api/members/{member_id}/restore")
def restore_member(member_id: int, access: Dict[str, Any] = Depends(require_owner)):
    with db_cursor() as cur:
        _assert_members_in_group(cur, [member_id], access["group_id"])
        cur.execute("UPDATE members SET is_active = 1 WHERE id = ? AND group_id = ?", (member_id, access["group_id"]))
        cur.execute(
            "SELECT m.*, mp.name AS default_payer_name FROM members m LEFT JOIN members mp ON mp.id = m.default_payer_id WHERE m.id = ?",
            (member_id,),
        )
        return dict(cur.fetchone())


# ---------- Sessions API ----------


@app.get("/api/sessions")
def list_sessions(access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT
                s.*,
                (SELECT COUNT(*) FROM session_participants sp WHERE sp.session_id = s.id) AS participant_count,
                (SELECT COUNT(*) FROM settlements st WHERE st.session_id = s.id) AS total_transfers,
                (SELECT COUNT(*) FROM settlements st WHERE st.session_id = s.id AND st.is_paid = 1) AS paid_transfers
            FROM sessions s
            WHERE s.group_id = ?
            ORDER BY s.played_at DESC, s.id DESC
            """,
            (access["group_id"],),
        )
        rows = [dict(r) for r in cur.fetchall()]
        for row in rows:
            full = _load_session_full(cur, row["id"], access["group_id"])
            row["status"] = full["session"]["status"]
            row["total_spent"] = full["summary"]["total_spent"]
            row["total_transfers"] = len(full["settlements"])
            row["paid_transfers"] = sum(1 for st in full["settlements"] if st["is_paid"])
        return rows


@app.post("/api/sessions", status_code=201)
def create_session(payload: SessionCreate, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        pids = set(payload.participant_ids)
        _assert_members_in_group(cur, list(pids), access["group_id"])
        cur.execute(
            """
            INSERT INTO sessions (title, played_at, parking_fee, notes, group_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (payload.title.strip(), payload.played_at.strip(), payload.parking_fee, payload.notes.strip(), access["group_id"]),
        )
        session_id = cur.lastrowid
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
            cur.execute(
                "SELECT id FROM sessions WHERE id = ? AND group_id = ?",
                (payload.template_session_id, access["group_id"]),
            )
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Không tìm thấy buổi dùng làm mẫu.")
            _copy_session_expenses(cur, payload.template_session_id, session_id, pids)
        return _load_session_full(cur, session_id, access["group_id"])


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
def set_session_template(session_id: int, payload: TemplateFlag, access: Dict[str, Any] = Depends(require_owner)):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM sessions WHERE id = ? AND group_id = ?", (session_id, access["group_id"]))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy buổi đánh cầu.")
        if payload.is_template:
            cur.execute("UPDATE sessions SET is_template = 0 WHERE group_id = ?", (access["group_id"],))
            cur.execute(
                "UPDATE sessions SET is_template = 1 WHERE id = ? AND group_id = ?",
                (session_id, access["group_id"]),
            )
        else:
            cur.execute(
                "UPDATE sessions SET is_template = 0 WHERE id = ? AND group_id = ?",
                (session_id, access["group_id"]),
            )
        return _load_session_full(cur, session_id, access["group_id"])


@app.get("/api/sessions/{session_id}")
def get_session(session_id: int, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        return _load_session_full(cur, session_id, access["group_id"])


@app.put("/api/sessions/{session_id}")
def update_session(session_id: int, payload: SessionUpdate, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM sessions WHERE id = ? AND group_id = ?", (session_id, access["group_id"]))
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
            WHERE id = ? AND group_id = ?
            """,
            (title, played_at, parking_fee, notes, status, session_id, access["group_id"]),
        )

        if payload.participant_ids is not None:
            pids = set(payload.participant_ids)
            _assert_members_in_group(cur, list(pids), access["group_id"])
            if payload.participant_payers:
                _assert_members_in_group(
                    cur,
                    [pid for pid in payload.participant_payers.values() if pid],
                    access["group_id"],
                )
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

        return _load_session_full(cur, session_id, access["group_id"])


@app.put("/api/sessions/{session_id}/participants/{member_id}/payer")
def set_participant_payer(session_id: int, member_id: int, payload: ParticipantPayerUpdate, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT 1 FROM session_participants sp
            JOIN sessions s ON s.id = sp.session_id
            WHERE sp.session_id = ? AND sp.member_id = ? AND s.group_id = ?
            """,
            (session_id, member_id, access["group_id"]),
        )
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
        return _load_session_full(cur, session_id, access["group_id"])


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: int, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute("DELETE FROM sessions WHERE id = ? AND group_id = ?", (session_id, access["group_id"]))
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
def create_expense(session_id: int, payload: ExpenseIn, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM sessions WHERE id = ? AND group_id = ?", (session_id, access["group_id"]))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy buổi đánh cầu.")
        _assert_members_in_group(cur, _expense_member_ids(payload), access["group_id"])

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
        return _load_session_full(cur, session_id, access["group_id"])


@app.put("/api/expenses/{expense_id}")
def update_expense(expense_id: int, payload: ExpenseIn, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT e.session_id
            FROM expenses e
            JOIN sessions s ON s.id = e.session_id
            WHERE e.id = ? AND s.group_id = ?
            """,
            (expense_id, access["group_id"]),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy khoản chi.")
        session_id = row["session_id"]
        _assert_members_in_group(cur, _expense_member_ids(payload), access["group_id"])

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
        return _load_session_full(cur, session_id, access["group_id"])


@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT e.session_id
            FROM expenses e
            JOIN sessions s ON s.id = e.session_id
            WHERE e.id = ? AND s.group_id = ?
            """,
            (expense_id, access["group_id"]),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy khoản chi.")
        session_id = row["session_id"]
        cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        cur.execute(
            "UPDATE sessions SET updated_at = datetime('now', 'localtime') WHERE id = ?",
            (session_id,),
        )
        return _load_session_full(cur, session_id, access["group_id"])


# ---------- Settlements API ----------


@app.patch("/api/settlements/{settlement_id}")
def toggle_settlement(settlement_id: int, payload: SettlementToggle, access: Dict[str, Any] = Depends(require_access)):
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT st.session_id
            FROM settlements st
            JOIN sessions s ON s.id = st.session_id
            WHERE st.id = ? AND s.group_id = ?
            """,
            (settlement_id, access["group_id"]),
        )
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

        return _load_session_full(cur, session_id, access["group_id"])


# ---------- Groups ----------


@app.get("/api/groups/status")
def groups_status():
    with db_cursor() as cur:
        return {"legacy_unclaimed": _legacy_unclaimed(cur)}


@app.post("/api/groups", status_code=201)
def create_group(payload: GroupCreate):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Hãy nhập tên nhóm.")
    with db_cursor() as cur:
        if _legacy_unclaimed(cur):
            raise HTTPException(status_code=409, detail="Hãy nhận sổ cũ trước khi tạo nhóm mới.")
        cur.execute(
            "INSERT INTO groups (name, invite_code, owner_code) VALUES (?, ?, ?)",
            (name, _fresh_code(cur, "invite_code", 6), _fresh_code(cur, "owner_code", 10)),
        )
        cur.execute("SELECT * FROM groups WHERE id = ?", (cur.lastrowid,))
        return _group_login(cur, cur.fetchone(), "owner")


@app.post("/api/groups/join")
def join_group(payload: GroupJoin):
    code = _normalize_code(payload.code)
    if len(code) < 4:
        raise HTTPException(status_code=400, detail="Mã nhóm chưa đúng.")
    with db_cursor() as cur:
        cur.execute(
            "SELECT * FROM groups WHERE invite_code = ? OR owner_code = ?",
            (code, code),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy nhóm với mã này.")
        role = "owner" if row["owner_code"] == code else "member"
        return _group_login(cur, row, role)


@app.post("/api/groups/claim-legacy")
def claim_legacy():
    with db_cursor() as cur:
        if not _legacy_unclaimed(cur):
            raise HTTPException(status_code=409, detail="Sổ cũ đã có người nhận.")
        cur.execute("SELECT * FROM groups ORDER BY id ASC LIMIT 1")
        return _group_login(cur, cur.fetchone(), "owner")


@app.get("/api/group")
def get_current_group(access: Dict[str, Any] = Depends(require_access)):
    return _public_group(access)


# ---------- Health & Static Frontend ----------


def _recognize_vi_pcm(pcm: bytes) -> str:
    if len(pcm) < 3200:
        raise HTTPException(status_code=400, detail="Đoạn nói quá ngắn.")
    url = (
        "https://www.google.com/speech-api/v2/recognize"
        "?client=chromium&lang=vi-VN&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
    )
    req = urllib.request.Request(
        url,
        data=pcm,
        headers={"Content-Type": "audio/l16; rate=16000"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            body = res.read().decode("utf-8", "ignore")
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Không chuyển được giọng nói thành chữ. Hãy nói lại.") from exc

    text = ""
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        for item in data.get("result") or []:
            alternatives = item.get("alternative") or []
            if alternatives and alternatives[0].get("transcript"):
                text = alternatives[0]["transcript"]
    if not text:
        raise HTTPException(status_code=422, detail="Chưa nghe rõ điểm. Nói lại tỷ số.")
    return text


@app.post("/api/voice/transcribe")
async def transcribe_voice(request: Request, access: Dict[str, Any] = Depends(require_access)):
    """Used when the installed home-screen app cannot run the browser speech engine."""
    del access
    pcm = await request.body()
    return {"text": _recognize_vi_pcm(pcm)}


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
