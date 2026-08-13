"""Frontier ledger is a CLAIM_STATUS projection, not a completeness claim."""

from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "12_PUBLIC_SITE/record/frontier.json"
RENDER = ROOT / "09_TOOLS/02_COMPILERS/render_claim_frontier.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("claim_frontier_renderer", RENDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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

    def test_html_projection_escapes_source_owned_text(self) -> None:
        renderer = load_renderer()
        payload = {
            "counts": {"total": 1},
            "claims": [{
                "id": "X<script>", "bucket": "open", "status": "OPEN",
                "tier": "C", "statement": "<img src=x onerror=alert(1)>",
                "raise": "a & b", "kill": "</p><script>bad()</script>",
                "owner": "owner<unsafe>", "last_move": {"date": "2026-08-13"},
            }],
        }
        page = renderer.render_html(payload)
        self.assertNotIn("<script>", page)
        self.assertNotIn("<img src=x", page)
        self.assertIn("X&lt;script&gt;", page)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", page)
        self.assertIn("a &amp; b", page)
        self.assertIn('property="og:image"', page)
        self.assertNotIn("<!--OG:AUTO-->", page)


if __name__ == "__main__":
    unittest.main()
