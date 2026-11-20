"""Pure calculation engine for badminton session expense splitting and debt simplification."""

from typing import Any, Dict, List, Tuple


def _split_integer_evenly(total: int, count: int) -> List[int]:
    """Split an integer VND amount across `count` people so the sum equals `total` exactly."""
    if count <= 0:
        return []
    base = total // count
    remainder = total % count
    return [base + (1 if idx < remainder else 0) for idx in range(count)]


def _format_vnd(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + "đ"


def _unit_fee(exp: Dict[str, Any]) -> int:
    """5.000đ only when the fee is missing. An explicit 0 stays 0."""
    raw = exp.get("unit_fee")
    if raw is None or raw == "":
        return 5000
    return max(0, int(raw))


def _session_ids(raw_ids: Any, member_map: Dict[int, Dict[str, Any]]) -> List[int]:
    """People still in the session, in the stored order, without duplicates."""
    seen = set()
    picked: List[int] = []
    for pid in raw_ids or []:
        pid = int(pid)
        if pid in member_map and pid not in seen:
            seen.add(pid)
            picked.append(pid)
    return picked


def _allocate_by_weights(total: int, weights: List[int]) -> List[int]:
    """Split `total` in proportion to `weights` so the parts sum to `total` exactly."""
    count = len(weights)
    if count == 0:
        return []
    if total <= 0:
        return [0] * count
    weight_sum = sum(max(0, int(w)) for w in weights)
    if weight_sum <= 0:
        return _split_integer_evenly(total, count)
    safe_weights = [max(0, int(w)) for w in weights]
    if total >= weight_sum:
        return safe_weights
    base = [(total * w) // weight_sum for w in safe_weights]
    leftover = total - sum(base)
    order = sorted(
        range(count),
        key=lambda idx: (-(total * safe_weights[idx] % weight_sum), idx),
    )
    for idx in order[:leftover]:
        base[idx] += 1
    return base


def _find_cycles(links: Dict[int, int]) -> set:
    cyclic = set()
    for start in links:
        seen: List[int] = []
        index: Dict[int, int] = {}
        cur = start
        while cur in links and cur not in cyclic and cur not in index:
            index[cur] = len(seen)
            seen.append(cur)
            cur = links[cur]
        if cur in index:
            cyclic.update(seen[index[cur] :])
    return cyclic


def _resolve_joint_payments(member_map: Dict[int, Dict[str, Any]]) -> List[str]:
    """Roll balances along payer chains. A cycle keeps each person's own balance."""
    links: Dict[int, int] = {}
    for mid, info in member_map.items():
        payer_id = info.get("payer_member_id")
        if payer_id is None:
            continue
        payer_id = int(payer_id)
        if payer_id in member_map and payer_id != mid:
            links[mid] = payer_id

    cyclic = _find_cycles(links)
    warnings: List[str] = []
    if cyclic:
        names = [member_map[mid]["name"] for mid in sorted(cyclic)]
        warnings.append(
            "Ghép trả chung bị vòng giữa "
            + ", ".join(names)
            + ". Những người trong vòng tự giữ số dư của mình."
        )

    active: Dict[int, int] = {}
    for mid, payer_id in links.items():
        if mid in cyclic or payer_id in cyclic:
            member_map[mid]["couple_cycle"] = True
            continue
        active[mid] = payer_id

    def root_of(mid: int) -> int:
        seen = set()
        cur = mid
        while cur in active and cur not in seen:
            seen.add(cur)
            cur = active[cur]
        return cur

    original_net = {mid: int(info["net"]) for mid, info in member_map.items()}
    grouped: Dict[int, List[int]] = {}
    for mid in active:
        root = root_of(mid)
        if root == mid:
            continue
        grouped.setdefault(root, []).append(mid)

    for root, deps in grouped.items():
        root_info = member_map[root]
        ordered = sorted(deps, key=lambda mid: (member_map[mid]["name"].casefold(), mid))
        for mid in ordered:
            info = member_map[mid]
            info["paid_by_name"] = root_info["name"]
            info["net"] = 0
            root_info["paid_for_names"].append(info["name"])
            root_info["net"] += original_net[mid]
    return warnings


def session_is_settled(member_summaries: List[Dict[str, Any]], settlements: List[Dict[str, Any]]) -> bool:
    """Settled when every transfer is paid and the transfers cover every balance.

    `net` is the balance before transfers. A normal debtor still has a negative
    net while their transfer is what clears it. A session is not finished when
    some balance has no matching transfer, so the nets must sum to zero.
    """
    if not settlements:
        return False
    if any(not int(item.get("is_paid") or 0) for item in settlements):
        return False
    return sum(int(item["net"]) for item in member_summaries) == 0


def calculate_session_summary(
    participants: List[Dict[str, Any]],
    expenses: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Calculate per-member breakdown, net balances, and minimum transfers.

    Supported expense structures:
    - split_type == 'equal_split':
        Divides `total_amount` equally among session members in `participant_ids`.
        Parking with `parking_mode == 'included_in_court'` is peeled out of court
        invoices in creation order before the court remainder is split. The court
        payer is still credited with the full invoice. The amount shown for the
        court line is the remainder after that peel.
    - split_type == 'parking':
        Each session member in `participant_ids` consumes `unit_fee` (5.000 when missing, 0 when set to 0).
        `separate_payer` credits `payer_id` with the sum of those fees.
        `included_in_court` does not credit a separate payer. Only the portion that
        fits in the court invoices is charged, except when the session has no court
        invoice at all: then the full fee stays as unmatched debt.
    - split_type == 'itemized':
        Contains `items`: each item has `amount`, `pricing_mode` ('per_person' | 'split_total'),
        and `participant_ids`.
        - 'per_person': each selected member pays `amount`; subtotal = `amount * len(participant_ids)`.
        - 'split_total': `amount` is split evenly among selected members; subtotal = `amount`.
        `payer_id` is credited with the sum of all item subtotals.

    People no longer in the session are ignored. A fixed invoice (equal split or
    split-total) is re-split among whoever remains. A per-person price or a
    separate parking fee drops the removed person's share.
    Couple links roll the whole balance to the final payer. A cycle is not rolled.
    """
    member_map: Dict[int, Dict[str, Any]] = {}
    for m in participants:
        mid = int(m["id"])
        member_map[mid] = {
            "member_id": mid,
            "name": m["name"],
            "bank_id": m.get("bank_id", ""),
            "account_no": m.get("account_no", ""),
            "account_name": m.get("account_name", ""),
            "payer_member_id": m.get("payer_member_id"),
            "couple_cycle": False,
            "paid": 0,
            "consumed": 0,
            "net": 0,
            "breakdown": {
                "court": 0,
                "shuttle": 0,
                "parking": 0,
                "snack": 0,
                "drink": 0,
                "other": 0,
            },
        }

    # Ensure any payer who might not be in participants is still tracked safely
    def ensure_member(mid: int, fallback_name: str = "") -> None:
        if mid not in member_map:
            member_map[mid] = {
                "member_id": mid,
                "name": fallback_name or f"TV #{mid}",
                "bank_id": "",
                "account_no": "",
                "account_name": "",
                "payer_member_id": None,
                "couple_cycle": False,
                "paid": 0,
                "consumed": 0,
                "net": 0,
                "breakdown": {
                    "court": 0,
                    "shuttle": 0,
                    "parking": 0,
                    "snack": 0,
                    "drink": 0,
                    "other": 0,
                },
            }

    category_totals = {
        "court": 0,
        "shuttle": 0,
        "parking": 0,
        "snack": 0,
        "drink": 0,
        "other": 0,
    }
    warnings: List[str] = []
    expense_computed_totals: Dict[int, int] = {}
    expense_meta: Dict[int, Dict[str, int]] = {}

    def blank_meta(invoice_total: int = 0) -> Dict[str, int]:
        return {
            "invoice_total": invoice_total,
            "parking_deducted": 0,
            "parking_unfunded": 0,
            "parking_unmatched": 0,
        }

    # 1. Parking included in court invoices, counted only for people still in the session.
    included_slots: List[Tuple[int, int, int]] = []
    court_sum = 0
    court_count = 0
    for exp in expenses:
        split_type = exp.get("split_type", "equal_split")
        cat = exp.get("category", "other")
        if cat not in category_totals:
            cat = "other"
        if split_type == "equal_split" and cat == "court":
            court_count += 1
            court_sum += max(0, int(exp.get("total_amount") or 0))
        elif split_type == "parking" and (exp.get("parking_mode") or "") == "included_in_court":
            fee = _unit_fee(exp)
            exp_id = int(exp.get("id", 0))
            for pid in _session_ids(exp.get("participant_ids"), member_map):
                included_slots.append((exp_id, pid, fee))

    requested_parking = sum(fee for _, _, fee in included_slots)
    parking_unmatched = False
    if requested_parking > 0 and court_count == 0:
        parking_unmatched = True
        funded_parking = requested_parking
        peel_budget = 0
        warnings.append(
            "Đã chọn gửi xe gộp vào hóa đơn sân nhưng buổi chưa có khoản Tiền sân. "
            "Tiền xe vẫn được ghi nợ cho từng người và chưa có người nhận."
        )
    elif requested_parking > court_sum:
        funded_parking = court_sum
        peel_budget = court_sum
        warnings.append(
            f"Tổng tiền gửi xe ({_format_vnd(requested_parking)}) lớn hơn tổng hóa đơn sân "
            f"({_format_vnd(court_sum)}). Chỉ tách {_format_vnd(court_sum)}, phần vượt không ghi nợ."
        )
    else:
        funded_parking = requested_parking
        peel_budget = requested_parking

    slot_amounts = (
        [fee for _, _, fee in included_slots]
        if parking_unmatched
        else _allocate_by_weights(funded_parking, [fee for _, _, fee in included_slots])
    )
    included_charges: Dict[int, Dict[int, int]] = {}
    for (exp_id, pid, _), amount in zip(included_slots, slot_amounts):
        bucket = included_charges.setdefault(exp_id, {})
        bucket[pid] = bucket.get(pid, 0) + amount

    # 2. Process every expense
    for exp in expenses:
        exp_id = int(exp.get("id", 0))
        cat = exp.get("category", "other")
        if cat not in category_totals:
            cat = "other"
        split_type = exp.get("split_type", "equal_split")
        payer_id = exp.get("payer_id")

        if split_type == "equal_split":
            raw_total = max(0, int(exp.get("total_amount") or 0))
            p_ids = _session_ids(exp.get("participant_ids"), member_map)

            if payer_id is not None:
                payer_id = int(payer_id)
                ensure_member(payer_id, exp.get("payer_name", ""))
                member_map[payer_id]["paid"] += raw_total

            deducted = 0
            if cat == "court" and peel_budget > 0:
                deducted = min(raw_total, peel_budget)
                peel_budget -= deducted
            splittable_amount = raw_total - deducted

            shares = _split_integer_evenly(splittable_amount, len(p_ids))
            for pid, share in zip(p_ids, shares):
                member_map[pid]["consumed"] += share
                member_map[pid]["breakdown"][cat] += share

            category_totals[cat] += splittable_amount
            expense_computed_totals[exp_id] = splittable_amount
            meta = blank_meta(raw_total)
            meta["parking_deducted"] = deducted
            expense_meta[exp_id] = meta

        elif split_type == "parking":
            unit_fee = _unit_fee(exp)
            p_ids = _session_ids(exp.get("participant_ids"), member_map)
            parking_mode = exp.get("parking_mode") or "separate_payer"

            if parking_mode == "included_in_court":
                charge_map = included_charges.get(exp_id, {})
                charged_total = sum(charge_map.get(pid, 0) for pid in p_ids)
                requested_total = unit_fee * len(p_ids)
                for pid in p_ids:
                    amount = charge_map.get(pid, 0)
                    member_map[pid]["consumed"] += amount
                    member_map[pid]["breakdown"]["parking"] += amount
                category_totals["parking"] += charged_total
                expense_computed_totals[exp_id] = charged_total
                meta = blank_meta(requested_total)
                meta["parking_unfunded"] = 0 if parking_unmatched else max(0, requested_total - charged_total)
                meta["parking_unmatched"] = 1 if parking_unmatched else 0
                expense_meta[exp_id] = meta
            else:
                parking_total = unit_fee * len(p_ids)
                if payer_id is not None:
                    payer_id = int(payer_id)
                    ensure_member(payer_id, exp.get("payer_name", ""))
                    member_map[payer_id]["paid"] += parking_total
                for pid in p_ids:
                    member_map[pid]["consumed"] += unit_fee
                    member_map[pid]["breakdown"]["parking"] += unit_fee
                category_totals["parking"] += parking_total
                expense_computed_totals[exp_id] = parking_total
                expense_meta[exp_id] = blank_meta(parking_total)

        elif split_type == "itemized":
            items = exp.get("items", [])
            invoice_total = 0

            for item in items:
                amount = max(0, int(item.get("amount") or 0))
                pricing_mode = item.get("pricing_mode") or "per_person"
                item_pids = _session_ids(item.get("participant_ids"), member_map)

                if not item_pids or amount == 0:
                    continue

                if pricing_mode == "per_person":
                    subtotal = amount * len(item_pids)
                    for pid in item_pids:
                        member_map[pid]["consumed"] += amount
                        member_map[pid]["breakdown"][cat] += amount
                    invoice_total += subtotal
                else:
                    shares = _split_integer_evenly(amount, len(item_pids))
                    for pid, share in zip(item_pids, shares):
                        member_map[pid]["consumed"] += share
                        member_map[pid]["breakdown"][cat] += share
                    invoice_total += amount

            if payer_id is not None:
                payer_id = int(payer_id)
                ensure_member(payer_id, exp.get("payer_name", ""))
                member_map[payer_id]["paid"] += invoice_total

            category_totals[cat] += invoice_total
            expense_computed_totals[exp_id] = invoice_total
            expense_meta[exp_id] = blank_meta(invoice_total)

    # 3. Net balances, then roll couple chains onto the final payer
    for info in member_map.values():
        info["raw_net"] = info["paid"] - info["consumed"]
        info["net"] = info["raw_net"]
        info["paid_by_name"] = ""
        info["paid_for_names"] = []

    warnings.extend(_resolve_joint_payments(member_map))

    member_summaries: List[Dict[str, Any]] = list(member_map.values())

    # 4. Simplify debts (greedy matching: largest debtor -> largest creditor)
    transfers = simplify_debts(member_summaries)

    total_spent = sum(category_totals.values())
    total_paid = sum(m["paid"] for m in member_summaries)

    return {
        "total_spent": total_spent,
        "total_paid": total_paid,
        "category_totals": category_totals,
        "member_summaries": member_summaries,
        "transfers": transfers,
        "warnings": warnings,
        "expense_computed_totals": expense_computed_totals,
        "expense_meta": expense_meta,
    }


def simplify_debts(member_summaries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Greedy debt simplification minimizing the number of transfers.
    Returns list of dicts: {from_member_id, to_member_id, amount}.
    """
    creditors: List[Tuple[int, int]] = []  # (amount_to_receive, member_id)
    debtors: List[Tuple[int, int]] = []    # (amount_to_pay, member_id)

    for m in member_summaries:
        net = int(m["net"])
        mid = int(m["member_id"])
        if net > 0:
            creditors.append([net, mid])
        elif net < 0:
            debtors.append([-net, mid])

    # Sort descending by amount so largest pairs clear first
    creditors.sort(key=lambda x: (-x[0], x[1]))
    debtors.sort(key=lambda x: (-x[0], x[1]))

    transfers: List[Dict[str, Any]] = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debt_amt, debtor_id = debtors[i]
        cred_amt, creditor_id = creditors[j]
        transfer_amt = min(debt_amt, cred_amt)

        if transfer_amt > 0:
            transfers.append(
                {
                    "from_member_id": debtor_id,
                    "to_member_id": creditor_id,
                    "amount": transfer_amt,
                }
            )

        debtors[i][0] -= transfer_amt
        creditors[j][0] -= transfer_amt

        if debtors[i][0] == 0:
            i += 1
        if creditors[j][0] == 0:
            j += 1

    return transfers
