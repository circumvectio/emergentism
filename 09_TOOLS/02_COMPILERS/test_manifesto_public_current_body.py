#!/usr/bin/env python3
"""Lock the staged Manifesto public current-body extract.

A green test is not a public edition and not an Amrita receipt.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXTRACTOR = ROOT / "09_TOOLS/02_COMPILERS/extract_manifesto_public_current_body.py"
OUTPUT = ROOT / "13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_STAGED.md"
RECEIPT = ROOT / "13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_STAGED.json"

FORBIDDEN = (
    "## 12.",
    "## 13.",
    "## 14.",
    "## 15.",
    "## 16.",
    "RIP01-",
    "# Part IV — The Frontier Stated Honestly",
)


class ManifestoPublicCurrentBodyTests(unittest.TestCase):
    def test_extractor_check_is_clean(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(EXTRACTOR), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_extract_excludes_research_genealogy_and_reciprocal(self) -> None:
        text = OUTPUT.read_text(encoding="utf-8")
        for needle in FORBIDDEN:
            self.assertNotIn(needle, text, needle)

    def test_receipt_is_not_a_public_route(self) -> None:
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(receipt["public_route"], None)
        self.assertEqual(receipt["g10"], "unpaid")
        self.assertFalse(receipt["retargets_book_builder"])
        self.assertIn("ch17_right_to_leave", receipt["included"])
        self.assertIn("ch12_titans_research", receipt["excluded"])

    def test_seams_do_not_point_at_missing_chapters(self) -> None:
        text = OUTPUT.read_text(encoding="utf-8")
        self.assertNotIn("that precede it", text)
        self.assertIn("not part of this current-body extract", text)
        self.assertIn("contains no research, historical, or custody chapters", text)


if __name__ == "__main__":
    unittest.main()
