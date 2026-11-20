import unittest

from calculator import calculate_session_summary, session_is_settled


def person(pid, name, payer=None):
    return {"id": pid, "name": name, "payer_member_id": payer}


def by_name(result):
    return {row["name"]: row for row in result["member_summaries"]}


def nets_clear_after_transfers(result):
    balances = {row["member_id"]: row["net"] for row in result["member_summaries"]}
    for transfer in result["transfers"]:
        balances[transfer["from_member_id"]] += transfer["amount"]
        balances[transfer["to_member_id"]] -= transfer["amount"]
    return balances


class CalculatorTests(unittest.TestCase):
    def test_equal_split_and_odd_dong(self):
        people = [person(1, "An"), person(2, "Binh"), person(3, "Chi")]
        result = calculate_session_summary(
            people,
            [{"id": 1, "category": "shuttle", "split_type": "equal_split", "payer_id": 2, "total_amount": 100000, "participant_ids": [1, 2, 3]}],
        )
        rows = by_name(result)
        self.assertEqual([rows["An"]["consumed"], rows["Binh"]["consumed"], rows["Chi"]["consumed"]], [33334, 33333, 33333])
        self.assertEqual(result["total_paid"], result["total_spent"])
        self.assertEqual(set(nets_clear_after_transfers(result).values()), {0})

    def test_included_parking_one_invoice(self):
        people = [person(i, name) for i, name in enumerate(["An", "Binh", "Chi", "Dung"], start=1)]
        result = calculate_session_summary(
            people,
            [
                {"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 1, "total_amount": 260000, "participant_ids": [1, 2, 3, 4]},
                {"id": 2, "category": "parking", "split_type": "parking", "parking_mode": "included_in_court", "unit_fee": 5000, "participant_ids": [1, 2, 3, 4]},
            ],
        )
        self.assertEqual(result["total_spent"], 260000)
        self.assertEqual(result["total_paid"], 260000)
        self.assertEqual(result["expense_computed_totals"][1], 240000)
        self.assertEqual(result["expense_meta"][1]["invoice_total"], 260000)
        self.assertEqual(result["expense_meta"][1]["parking_deducted"], 20000)
        self.assertEqual(result["expense_computed_totals"][2], 20000)
        self.assertEqual(by_name(result)["An"]["breakdown"]["court"], 60000)
        self.assertEqual(by_name(result)["An"]["breakdown"]["parking"], 5000)
        self.assertEqual(set(nets_clear_after_transfers(result).values()), {0})

    def test_removed_parker_does_not_leave_a_gap(self):
        people = [person(1, "An"), person(2, "Binh"), person(3, "Chi")]
        result = calculate_session_summary(
            people,
            [
                {"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 1, "total_amount": 200000, "participant_ids": [1, 2, 3, 4]},
                {"id": 2, "category": "parking", "split_type": "parking", "parking_mode": "included_in_court", "unit_fee": 5000, "participant_ids": [1, 2, 3, 4]},
            ],
        )
        self.assertEqual(result["total_paid"], 200000)
        self.assertEqual(result["total_spent"], 200000)
        self.assertEqual(result["warnings"], [])
        self.assertEqual(set(nets_clear_after_transfers(result).values()), {0})

    def test_parking_peels_across_later_court_invoices(self):
        people = [person(i, name) for i, name in enumerate(["An", "Binh", "Chi", "Dung"], start=1)]
        result = calculate_session_summary(
            people,
            [
                {"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 1, "total_amount": 10000, "participant_ids": [1, 2, 3, 4]},
                {"id": 2, "category": "court", "split_type": "equal_split", "payer_id": 2, "total_amount": 200000, "participant_ids": [1, 2, 3, 4]},
                {"id": 3, "category": "parking", "split_type": "parking", "parking_mode": "included_in_court", "unit_fee": 5000, "participant_ids": [1, 2, 3, 4]},
            ],
        )
        self.assertEqual(result["warnings"], [])
        self.assertEqual(result["expense_meta"][1]["parking_deducted"], 10000)
        self.assertEqual(result["expense_meta"][2]["parking_deducted"], 10000)
        self.assertEqual(result["expense_computed_totals"][2], 190000)
        self.assertEqual(result["total_paid"], result["total_spent"])
        self.assertEqual(set(nets_clear_after_transfers(result).values()), {0})

    def test_parking_above_every_court_invoice_is_capped(self):
        people = [person(i, name) for i, name in enumerate(["An", "Binh", "Chi", "Dung"], start=1)]
        result = calculate_session_summary(
            people,
            [
                {"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 1, "total_amount": 10000, "participant_ids": [1, 2, 3, 4]},
                {"id": 2, "category": "parking", "split_type": "parking", "parking_mode": "included_in_court", "unit_fee": 5000, "participant_ids": [1, 2, 3, 4]},
            ],
        )
        self.assertEqual(result["total_paid"], 10000)
        self.assertEqual(result["total_spent"], 10000)
        self.assertEqual(result["expense_computed_totals"][2], 10000)
        self.assertEqual(result["expense_meta"][2]["parking_unfunded"], 10000)
        self.assertTrue(result["warnings"])
        self.assertEqual(set(nets_clear_after_transfers(result).values()), {0})

    def test_included_parking_without_court_stays_visible_debt(self):
        people = [person(i, name) for i, name in enumerate(["An", "Binh", "Chi", "Dung"], start=1)]
        result = calculate_session_summary(
            people,
            [{"id": 3, "category": "parking", "split_type": "parking", "parking_mode": "included_in_court", "unit_fee": 5000, "participant_ids": [1, 2, 3, 4]}],
        )
        self.assertEqual(result["transfers"], [])
        self.assertEqual(sorted(row["net"] for row in result["member_summaries"]), [-5000, -5000, -5000, -5000])
        self.assertEqual(result["expense_meta"][3]["parking_unmatched"], 1)
        self.assertTrue(result["warnings"])

    def test_zero_parking_fee_stays_zero(self):
        people = [person(1, "An"), person(2, "Binh")]
        result = calculate_session_summary(
            people,
            [{"id": 1, "category": "parking", "split_type": "parking", "payer_id": 1, "parking_mode": "separate_payer", "unit_fee": 0, "participant_ids": [1, 2]}],
        )
        self.assertEqual(result["total_spent"], 0)
        self.assertEqual(result["total_paid"], 0)
        self.assertEqual(by_name(result)["An"]["breakdown"]["parking"], 0)

    def test_chain_rolls_to_final_payer_regardless_of_name_order(self):
        expense = [{"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 4, "total_amount": 120000, "participant_ids": [1, 2, 3]}]
        early_root = calculate_session_summary(
            [person(1, "An", payer=2), person(2, "Binh", payer=3), person(3, "Chi"), person(4, "Dung")],
            expense,
        )
        late_root = calculate_session_summary(
            [person(1, "An"), person(2, "Binh", payer=1), person(3, "Chi", payer=2), person(4, "Dung")],
            expense,
        )
        self.assertEqual(by_name(early_root)["Chi"]["net"], -120000)
        self.assertEqual(by_name(early_root)["An"]["net"], 0)
        self.assertEqual(by_name(early_root)["An"]["paid_by_name"], "Chi")
        self.assertEqual(by_name(late_root)["An"]["net"], -120000)
        self.assertEqual(by_name(late_root)["Binh"]["net"], 0)
        self.assertEqual(by_name(late_root)["Chi"]["paid_by_name"], "An")
        self.assertCountEqual(by_name(late_root)["An"]["paid_for_names"], ["Binh", "Chi"])
        self.assertEqual(early_root["transfers"], [{"from_member_id": 3, "to_member_id": 4, "amount": 120000}])
        self.assertEqual(late_root["transfers"], [{"from_member_id": 1, "to_member_id": 4, "amount": 120000}])

    def test_cycle_keeps_each_balance(self):
        result = calculate_session_summary(
            [person(1, "An", payer=2), person(2, "Binh", payer=1)],
            [{"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 1, "total_amount": 100000, "participant_ids": [1, 2]}],
        )
        rows = by_name(result)
        self.assertTrue(rows["An"]["couple_cycle"])
        self.assertTrue(rows["Binh"]["couple_cycle"])
        self.assertEqual(rows["An"]["net"], 50000)
        self.assertEqual(rows["Binh"]["net"], -50000)
        self.assertEqual(result["transfers"], [{"from_member_id": 2, "to_member_id": 1, "amount": 50000}])
        self.assertTrue(any("vòng" in warning for warning in result["warnings"]))

    def test_one_payer_for_several_people_still_closes(self):
        result = calculate_session_summary(
            [person(1, "An"), person(2, "Binh", payer=1), person(3, "Chi", payer=1)],
            [{"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 3, "total_amount": 90000, "participant_ids": [1, 2, 3]}],
        )
        rows = by_name(result)
        self.assertEqual(rows["An"]["net"], 0)
        self.assertEqual(rows["Binh"]["net"], 0)
        self.assertEqual(rows["Chi"]["net"], 0)
        self.assertEqual(rows["Chi"]["raw_net"], 60000)
        self.assertEqual(result["transfers"], [])

    def test_removing_someone_keeps_invoice_rules(self):
        people = [person(1, "An"), person(2, "Binh"), person(3, "Chi")]
        court = calculate_session_summary(
            people,
            [{"id": 1, "category": "court", "split_type": "equal_split", "payer_id": 1, "total_amount": 200000, "participant_ids": [1, 2, 3, 4]}],
        )
        snack = calculate_session_summary(
            people,
            [{"id": 1, "category": "snack", "split_type": "itemized", "payer_id": 1, "items": [{"amount": 20000, "pricing_mode": "per_person", "participant_ids": [1, 2, 3, 4]}]}],
        )
        parking = calculate_session_summary(
            people,
            [{"id": 1, "category": "parking", "split_type": "parking", "payer_id": 3, "parking_mode": "separate_payer", "unit_fee": 5000, "participant_ids": [1, 2, 3, 4]}],
        )
        self.assertEqual(court["total_spent"], 200000)
        self.assertEqual(snack["total_spent"], 60000)
        self.assertEqual(parking["total_spent"], 15000)
        self.assertEqual(parking["total_paid"], 15000)

    def test_session_settled_requires_paid_transfers_and_no_leftover(self):
        balanced = [{"net": -180000}, {"net": 180000}]
        owed = [{"net": -5000}, {"net": -5000}]
        paid = [{"is_paid": 1}]
        unpaid = [{"is_paid": 0}]
        self.assertFalse(session_is_settled(balanced, []))
        self.assertFalse(session_is_settled(owed, []))
        self.assertFalse(session_is_settled(balanced, unpaid))
        self.assertFalse(session_is_settled(owed, paid))
        self.assertTrue(session_is_settled(balanced, paid))


if __name__ == "__main__":
    unittest.main()
