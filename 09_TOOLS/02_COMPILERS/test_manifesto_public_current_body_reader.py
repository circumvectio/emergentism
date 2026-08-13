#!/usr/bin/env python3
"""Lock the off-site Manifesto current-body HTML preview.

A green test is not a public edition and not an Amrita receipt.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RENDERER = ROOT / "09_TOOLS/02_COMPILERS/render_manifesto_public_current_body.py"
OUTPUT = ROOT / "13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_READER_STAGED.html"
PUBLIC = ROOT / "12_PUBLIC_SITE"

FORBIDDEN = ("## 12.", "## 13.", "## 14.", "## 15.", "## 16.", "RIP01-")


class ManifestoPublicCurrentBodyReaderTests(unittest.TestCase):
    def test_renderer_check_is_clean(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(RENDERER), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_output_is_off_site_and_bannered(self) -> None:
        text = OUTPUT.read_text(encoding="utf-8")
        self.assertTrue(OUTPUT.is_relative_to(ROOT / "13_BOOKS/manifesto"))
        self.assertFalse(OUTPUT.is_relative_to(PUBLIC))
        self.assertIn("STAGED PREVIEW", text)
        self.assertIn("G10 is unpaid", text)
        self.assertIn('name="robots" content="noindex, nofollow, noarchive"', text)
        self.assertIn("/manifest.webmanifest", text)
        self.assertIn("/assets/js/pwa.js", text)
        for needle in FORBIDDEN:
            self.assertNotIn(needle, text, needle)

    def test_renderer_refuses_a_public_site_output(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("render_manifesto_public_current_body", RENDERER)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        with self.assertRaises(SystemExit) as raised:
            module.assert_output_is_off_site(PUBLIC / "book" / "index.html")
        self.assertIn("refusing to write under 12_PUBLIC_SITE/", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
