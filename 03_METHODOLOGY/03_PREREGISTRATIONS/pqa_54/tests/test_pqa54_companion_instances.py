"""Companion/projection instances stay unrun and do not increment PQA-54 counts."""
from __future__ import annotations

import json
import unittest
from pathlib import Path


PQA54 = Path(__file__).resolve().parents[1]
CONTRACTS = PQA54 / "contracts"
LAUNCH = {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0}


def _load(name: str) -> dict:
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


class CompanionAndProjectionInstances(unittest.TestCase):
    def test_schema_stubs_remain_unrun(self) -> None:
        eub = _load("PQAEUBCompanion.v1.json")
        pub = _load("PQAPublicProjection.v1.json")
        self.assertEqual(eub["status"], "frozen_schema_unrun")
        self.assertEqual(pub["status"], "frozen_schema_unrun")
        self.assertIn("eub1_frozen_hashes", eub["required_fields"])
        self.assertNotIn("eub1_frozen_hashes", eub)
        self.assertNotIn("counts", pub)

    def test_companion_instance_has_readonly_hashes_and_forbids_transfer(self) -> None:
        inst = _load("PQAEUBCompanion.v1.instance.json")
        self.assertTrue(inst["forbid_score_or_truth_transfer"])
        self.assertFalse(inst["writes_eub_scores"])
        self.assertFalse(inst["transfers_truth"])
        files = inst["eub1_frozen_hashes"]["files"]
        self.assertGreaterEqual(len(files), 1)
        for digest in files.values():
            self.assertTrue(digest.startswith("sha256:"))
            hexpart = digest.split(":", 1)[1]
            self.assertEqual(len(hexpart), 64)
            int(hexpart, 16)

    def test_public_projection_counts_stay_54_0_0_0(self) -> None:
        inst = _load("PQAPublicProjection.v1.instance.json")
        self.assertEqual(inst["counts"], LAUNCH)
        wording = inst["bounded_public_wording"].lower()
        self.assertIn("does not end philosophy", wording)
        self.assertIn("0 resolved", wording)
        self.assertNotIn("resolved most", wording)


if __name__ == "__main__":
    unittest.main()
