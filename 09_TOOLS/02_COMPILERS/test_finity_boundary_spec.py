from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM"


class FinityBoundarySpecificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = (FORMAL / "47_FINITY_BOUNDARY_CALCULUS_SPEC.md").read_text(encoding="utf-8")
        cls.ledger = json.loads((FORMAL / "48_FINITY_PARADOX_LEDGER.yaml").read_text(encoding="utf-8"))
        cls.countermodels = (FORMAL / "49_FINITY_RECOVERY_AND_COUNTERMODEL_SUITE.md").read_text(encoding="utf-8")

    def test_titans_have_no_numeric_coercion(self) -> None:
        self.assertIn("TitanFrame ↛ Number", self.spec)
        self.assertIn("TitanFrame ↛ Field[F]", self.spec)
        self.assertIn("CM-04", self.countermodels)

    def test_standard_recovery_and_smallest_extension_are_mandatory(self) -> None:
        for marker in ("conservativity", "Smallest-extension test", "Native recovery", "Independent review"):
            self.assertIn(marker, self.spec)

    def test_paradox_rows_are_scoped_and_typed(self) -> None:
        rows = self.ledger["rows"]
        self.assertGreaterEqual(len(rows), 9)
        allowed = set(self.ledger["classifications"])
        self.assertTrue(all(row["classification"] in allowed for row in rows))
        self.assertEqual(len({row["id"] for row in rows}), len(rows))
        for row in rows:
            for field in ("formal_domain", "native_account", "recovered_result", "residual", "rivals", "kill"):
                self.assertTrue(row[field], f"{row['id']} missing {field}")

    def test_open_physics_is_not_promoted(self) -> None:
        measurement = next(row for row in self.ledger["rows"] if row["id"] == "MEAS-01")
        self.assertEqual(measurement["classification"], "unresolved_question")
        self.assertEqual(measurement["evidence_tier"], "C")


if __name__ == "__main__":
    unittest.main()
