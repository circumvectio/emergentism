#!/usr/bin/env python3
"""Three probes for the last_move triple, or it is not a gate."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_claim_last_move.py"
SPEC = importlib.util.spec_from_file_location("check_claim_last_move", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

EVIDENCE = "11_UPLINK/50_AUDITS_AND_EXECUTIONS/239_OPEN_CLAIM_DISPOSITION_2026_08_01.md"


class LastMoveContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = CHECKER.load_document(ROOT / CHECKER.STATUS_PATH)

    def row(self, document, bucket: str, row_id: str):
        return next(row for _b, row in CHECKER.claim_rows(document) if row["id"] == row_id)

    def test_live_register_passes_without_backfill(self) -> None:
        self.assertEqual(CHECKER.check(self.document, ROOT), [])

    def test_status_change_without_last_move_is_red(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "open", "W4")["status"] = "NARROWED"
        errors = CHECKER.check(document, ROOT)
        self.assertTrue(any("W4: status changed without last_move" in e for e in errors), errors)

    def test_status_change_with_well_formed_last_move_is_green(self) -> None:
        document = copy.deepcopy(self.document)
        row = self.row(document, "open", "W4")
        row["status"] = "NARROWED"
        row["last_move"] = {
            "mover": "239_OPEN_CLAIM_DISPOSITION",
            "date": "2026-08-01",
            "evidence": EVIDENCE,
        }
        self.assertEqual(CHECKER.check(document, ROOT), [])

    def test_dangling_evidence_is_red(self) -> None:
        document = copy.deepcopy(self.document)
        row = self.row(document, "open", "W4")
        row["last_move"] = {
            "mover": "239_OPEN_CLAIM_DISPOSITION",
            "date": "2026-08-01",
            "evidence": "missing_receipt.md",
        }
        errors = CHECKER.check(document, ROOT)
        self.assertTrue(any("does not exist" in e for e in errors), errors)

    def test_presence_without_shape_is_red(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "open", "W4")["last_move"] = "yves"
        errors = CHECKER.check(document, ROOT)
        self.assertTrue(any("must be an object" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
