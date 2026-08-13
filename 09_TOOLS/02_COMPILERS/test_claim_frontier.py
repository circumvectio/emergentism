"""Frontier ledger is a CLAIM_STATUS projection, not a completeness claim."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "12_PUBLIC_SITE/record/frontier.json"
RENDER = ROOT / "09_TOOLS/02_COMPILERS/render_claim_frontier.py"


class FrontierLedgerTests(unittest.TestCase):
    def test_check_mode_is_green(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(RENDER), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fences(self) -> None:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertFalse(data["completeness_claim"])
        self.assertFalse(data["attention_capture"])
        self.assertEqual(data["world_contact_accepted"], 0)
        self.assertEqual(data["k_star"], 0)
        self.assertIn("a reach or spread metric", data["not"])
        self.assertTrue(data["score"].startswith("tier movement"))
        for row in data["claims"]:
            if row["last_move"] is None:
                self.assertIn("Unrecorded", row["last_move_note"])

    def test_row_count_matches_source_buckets(self) -> None:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(data["counts"]["total"], len(data["claims"]))
        self.assertEqual(data["counts"]["total"], 72)


if __name__ == "__main__":
    unittest.main()
