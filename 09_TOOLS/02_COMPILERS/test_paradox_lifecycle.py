from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PARADOX = ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS"
LEDGER = ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/48_FINITY_PARADOX_LEDGER.yaml"


class ParadoxLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pd18 = (PARADOX / "PD_18_THE_EXTRACTION_PARADOX.md").read_text(encoding="utf-8")
        cls.synthesis = (PARADOX / "00_THE_EXTRACTION_PATTERN.md").read_text(encoding="utf-8")
        cls.index = (PARADOX / "PD_00_INDEX.md").read_text(encoding="utf-8")
        cls.readme = (PARADOX / "README.md").read_text(encoding="utf-8")
        cls.audit = (PARADOX / "00_PARADOX_SUITE_AUDIT.md").read_text(encoding="utf-8")
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_pd18_is_frozen_and_routes_the_killed_universal_form(self) -> None:
        for marker in (
            'status: "FROZEN — superseded; no current semantic authority"',
            "lifecycle: frozen",
            "DF-18 — terminal NOT-WELL-POSED universal-dissolution form",
            "not a current paradox solution",
        ):
            self.assertIn(marker, self.pd18)
        for barred in (
            "All Paradoxes Are One Paradox",
            "Most old paradoxes share a hidden structure",
            "**The resolution:**",
            "It dissolves them in its own register",
            "All roads lead to the same place",
        ):
            self.assertNotIn(barred, self.pd18)

    def test_surviving_synthesis_is_explicitly_bounded(self) -> None:
        for marker in (
            'status: "EVIDENCE-OPEN — row mapping incomplete"',
            "cannot promote one row by analogy with another",
            "supplies no common causal mechanism",
            "does not by itself adjudicate",
        ):
            self.assertIn(marker, self.synthesis)
        for barred in (
            "Most old paradoxes share a hidden structure",
            "**The resolution the framework offers:**",
            "It dissolves them in its own register",
            "The practice response in these cases is the same",
            "The paradoxes are evidence for the pattern",
        ):
            self.assertNotIn(barred, self.synthesis)

    def test_route_documents_agree_on_pd18_and_pd23_lifecycle(self) -> None:
        for surface in (self.index, self.readme, self.audit):
            self.assertIn("PD_18", surface)
            self.assertIn("frozen", surface.lower())
            self.assertIn("PD_23", surface)
            self.assertIn("superseded", surface.lower())
        self.assertIn("Legacy numbered routes", self.readme)
        self.assertIn("owns numbering, not substance", self.audit.lower())

    def test_scoped_resolution_requires_native_review(self) -> None:
        self.assertIn("scoped_resolution", self.ledger["classifications"])
        self.assertNotIn("resolution", self.ledger["classifications"])
        contract = self.ledger["scoped_resolution_requirements"]
        required = set(contract["required_fields"])
        self.assertTrue(
            {"scope", "formal_domain", "native_account", "recovered_result", "residual", "rivals", "kill", "native_review"}
            <= required
        )
        self.assertEqual(contract["required_native_review_status"], "complete")
        allowed_review_states = set(self.ledger["native_review_states"])
        for row in self.ledger["rows"]:
            review = row["native_review"]
            self.assertIn(review["status"], allowed_review_states)
            if row["classification"] == "scoped_resolution":
                for field in required:
                    self.assertTrue(row.get(field), f"{row['id']} missing {field}")
                self.assertEqual(review["status"], "complete")
                self.assertTrue(review["receipt"])

    def test_existing_standard_rows_are_not_promoted_without_review(self) -> None:
        by_id = {row["id"]: row for row in self.ledger["rows"]}
        for row_id in ("ZENO-01", "REAL-01"):
            self.assertEqual(by_id[row_id]["classification"], "formal_correction")
            self.assertEqual(by_id[row_id]["native_review"]["status"], "pending")


if __name__ == "__main__":
    unittest.main()
