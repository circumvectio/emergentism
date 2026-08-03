from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class AdequacyProgramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.adequacy = json.loads((ROOT / "00_META/ADEQUACY_DOCKETS.yaml").read_text(encoding="utf-8"))
        cls.science = json.loads((ROOT / "03_METHODOLOGY/00_W7_SCIENCE_INTEGRATION_EXECUTION_REGISTER.yaml").read_text(encoding="utf-8"))
        cls.matrix = (ROOT / "00_META/00_W8_ADEQUACY_DECISION_MATRIX.md").read_text(encoding="utf-8")

    def test_eight_adequacy_rungs_and_closed_maturity_ladder(self) -> None:
        self.assertEqual([row["docket_id"] for row in self.adequacy["dockets"]], [f"A{i}" for i in range(8)])
        self.assertEqual(self.adequacy["status_ladder"], self.science["maturity_states"])

    def test_cheapest_honest_science_order_is_exact(self) -> None:
        expected = ["GP-03", "GP-04", "GP-07", "GP-01", "GP-06", "GP-12", "GP-02", "GP-09", "GP-05", "GP-10", "GP-08", "GP-11"]
        self.assertEqual(self.science["execution_order"], expected)
        self.assertEqual([row["id"] for row in self.science["rows"]], expected)

    def test_every_science_row_has_native_recovery_and_world_gate(self) -> None:
        required = set(self.science["row_contract"])
        allowed = set(self.science["maturity_states"])
        for row in self.science["rows"]:
            self.assertTrue(required <= set(row), f"{row['id']} incomplete")
            self.assertIn(row["maturity_state"], allowed)
            for field in required:
                self.assertTrue(row[field], f"{row['id']} missing {field}")
        self.assertEqual(self.science["rows"][-1]["execution_state"], "runs-last")

    def test_decision_matrix_refuses_compensating_total(self) -> None:
        self.assertIn("No single score is permitted", self.matrix)
        self.assertIn("no compensating total score", self.matrix)
        self.assertNotIn("Overall score", self.matrix)
        self.assertNotIn("weighted total", self.matrix.lower())


if __name__ == "__main__":
    unittest.main()
