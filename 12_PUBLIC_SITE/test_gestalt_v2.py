#!/usr/bin/env python3
"""Focused contracts for the Gestalt of Dasein v2 public projection."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
F5_CONTRACT = ROOT / "05_COSMOLOGY/02_EMERGENTISM_CORE/F5Fork.v1.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


shell = load("gestalt_shell_test", SITE / "build_core_shell.py")
pwa = load("gestalt_pwa_test", SITE / "build_pwa.py")


class GestaltV2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fork = json.loads(F5_CONTRACT.read_text(encoding="utf-8"))
        cls.css = (SITE / "assets/css/gestalt-v2.css").read_text(encoding="utf-8")

    def test_f5_fork_has_three_equal_contact_arms_and_a_real_null(self) -> None:
        self.assertEqual(self.fork["schema"], "emergentism/F5Fork.v1")
        self.assertFalse(self.fork["epistemic_contract"]["truth_bonus_before_contact"])
        self.assertFalse(self.fork["epistemic_contract"]["agreement_is_evidence"])
        branches = {row["id"]: row for row in self.fork["branches"]}
        self.assertEqual(set(branches), {"F5-W", "F5-N", "F5-R"})
        self.assertEqual(
            {key: row["tier"] for key, row in branches.items()},
            {"F5-W": "[I/C]", "F5-N": "[D/C]", "F5-R": "[C]"},
        )
        for row in branches.values():
            self.assertTrue(
                {"mechanism", "strongest_rival", "discriminator", "kill", "survivor"}
                <= set(row)
            )
        law = self.fork["candidate_history_law"]
        self.assertEqual(law["null"], "kappa = 0 is the no-F5 arm.")
        self.assertEqual(law["strong_wager"], "kappa != 0 is the F5-R arm.")
        self.assertEqual(len(self.fork["independently_killable_propositions"]), 5)
        self.assertEqual(self.fork["option_ledger"]["aggregation"], "pareto_frontier")

    def test_shell_is_byte_idempotent_and_exactly_owned(self) -> None:
        rendered = shell.outputs()
        self.assertEqual(len(rendered), 15)
        self.assertEqual(set(rendered), {SITE / rel for rel in shell.CORE_PAGES})
        for path, body in rendered.items():
            with self.subTest(path=path.relative_to(SITE)):
                self.assertEqual(path.read_text(encoding="utf-8"), body)
                self.assertEqual(body.count("<!-- gestalt-core-nav:start -->"), 1)
                self.assertEqual(body.count("<!-- gestalt-core-footer:start -->"), 1)
                self.assertEqual(len(re.findall(r'<main\b[^>]*\bid=["\']main["\']', body, re.I)), 1)
                self.assertRegex(body, r'<main\b[^>]*\btabindex=["\']-1["\']')
                self.assertIn('/assets/css/gestalt-v2.css', body)
                self.assertIn('/assets/js/gestalt-v2.js', body)
                self.assertEqual(body.count('/favicon.svg'), 1)
                self.assertEqual(body.count('rel="icon"'), 1)

    def test_shell_rejects_malformed_ownership_and_preserves_article_footer(self) -> None:
        base = (
            '<html><head><title>x</title></head><body><main>m</main>'
            '<footer class="article-notes">Article note</footer></body></html>'
        )
        rendered = shell.render_page(base, "worldview")
        self.assertIn("Article note", rendered)
        self.assertEqual(rendered.count("<footer"), 2)

        css_only = base.replace(
            "</head>",
            '<link rel="stylesheet" href="/assets/css/gestalt-v2.css" /></head>',
        )
        rendered = shell.render_page(css_only, "worldview")
        self.assertEqual(rendered.count("/assets/css/gestalt-v2.css"), 1)
        self.assertEqual(rendered.count("/assets/js/gestalt-v2.js"), 1)

        uppercase = '<HTML><HEAD><title>x</title></HEAD><BODY><main>m</main></BODY></HTML>'
        self.assertIn('data-gestalt="v2"', shell.render_page(uppercase, "worldview"))

        nav = shell.render_nav("worldview")
        malformed = {
            "orphan nav marker": base.replace("<main>", "<!-- gestalt-core-nav:start --><main>"),
            "duplicate nav markers": base.replace("<main>", nav + nav + "<main>"),
            "wrong Gestalt version": base.replace("<html", '<html data-gestalt="v1"'),
            "missing head close": base.replace("</head>", ""),
        }
        for name, fixture in malformed.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                shell.render_page(fixture, "worldview")

    def test_signature_atlas_is_semantic_without_color_or_motion(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        match = re.search(
            r'<figure class="[^"]*\bg2-atlas\b[^"]*".*?</figure>',
            home,
            re.S,
        )
        self.assertIsNotNone(match)
        overview = match.group(0)
        self.assertIn('role="img"', overview)
        self.assertRegex(overview, r'aria-labelledby="[^"]+ [^"]+"')
        self.assertIn("<title", overview)
        self.assertIn("<desc", overview)
        self.assertIn("possible-line", overview)
        self.assertIn("evidence-line", overview)
        self.assertIn("solid · actual", overview)
        self.assertNotIn("future light cone", overview.casefold())

        f5 = (SITE / "f5/index.html").read_text(encoding="utf-8")
        figure = f5.split('<figure class="g2-atlas"', 1)[1].split("</figure>", 1)[0]
        self.assertIn('role="img"', figure)
        self.assertRegex(figure, r'aria-labelledby="[^"]+ [^"]+"')
        self.assertIn("<title", figure)
        self.assertIn("<desc", figure)
        self.assertIn("actual-line", figure)
        self.assertIn("possible-line", figure)
        self.assertIn("conjecture-line", figure)
        self.assertIn("evidence-line", figure)
        self.assertIn("[C] UNVALIDATED", figure)
        self.assertIn("ΣT", figure)
        self.assertNotIn("future light cone", figure.casefold())
        self.assertIn("solid · actual", figure)
        self.assertIn("dash · conjecture", figure)

    def test_static_accessibility_and_local_resource_contract(self) -> None:
        self.assertIn("min-height: 48px", self.css)
        self.assertIn("min-width: 48px", self.css)
        self.assertIn("prefers-reduced-motion: reduce", self.css)
        self.assertNotRegex(self.css, r"(?:linear|radial|conic)-gradient\s*\(")
        for relative in shell.CORE_PAGES:
            page = (SITE / relative).read_text(encoding="utf-8")
            with self.subTest(page=relative):
                self.assertNotRegex(page, r'<(?:script|img)\b[^>]*\bsrc=["\']https?://')
                self.assertNotRegex(
                    page,
                    r'<link\b(?=[^>]*\brel=["\'](?:stylesheet|preload|icon|manifest)["\'])'
                    r'[^>]*\bhref=["\']https?://',
                )
                self.assertNotRegex(page, r'<(?:main|section|article)\b[^>]*\bhidden\b')
        for number in range(7):
            page = (SITE / str(number) / "index.html").read_text(encoding="utf-8")
            self.assertIn("This illustration carries no evidence beyond the typed text above.", page)
            self.assertIn('html:not([data-gestalt-enhanced="true"]) .fallback{display:flex}', page)

    def test_newsreader_is_local_open_licensed_and_hash_bound(self) -> None:
        font = SITE / "assets/fonts/Newsreader-latin-variable.woff2"
        license_path = SITE / "assets/fonts/Newsreader-OFL.txt"
        source = (SITE / "assets/fonts/Newsreader-SOURCE.md").read_text(encoding="utf-8")
        digest = hashlib.sha256(font.read_bytes()).hexdigest()
        self.assertEqual(digest, "01817351be3edfc1714fe6d60ddea6a22a169a5ebd033b50c7f9495e5d9c386a")
        self.assertIn(digest, source)
        self.assertIn("SIL Open Font License 1.1", source)
        self.assertIn("SIL OPEN FONT LICENSE", license_path.read_text(encoding="utf-8"))
        self.assertIn('url("../fonts/Newsreader-latin-variable.woff2")', self.css)

    def test_local_favicon_is_semantic(self) -> None:
        favicon = (SITE / "favicon.svg").read_text(encoding="utf-8")
        self.assertIn('aria-labelledby="favicon-title favicon-description"', favicon)
        self.assertIn('<title id="favicon-title">', favicon)
        self.assertIn('<desc id="favicon-description">', favicon)
        self.assertNotRegex(favicon, r'(?:href|src)=["\']https?://')

    def test_pwa_check_is_read_only_and_precaches_v2_spine(self) -> None:
        protected = [SITE / "manifest.webmanifest", SITE / "offline/index.html", SITE / "sw.js"]
        before = {path: path.read_bytes() for path in protected}
        result = subprocess.run(
            [sys.executable, str(SITE / "build_pwa.py"), "--check"],
            cwd=SITE,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, {path: path.read_bytes() for path in protected})
        self.assertTrue(
            {
                "/dasein/", "/f5/", "/assets/css/gestalt-v2.css",
                "/assets/js/gestalt-v2.js", "/assets/fonts/Newsreader-latin-variable.woff2",
                "/favicon.svg",
            }.issubset(set(pwa.safe_spine()))
        )


if __name__ == "__main__":
    unittest.main()
