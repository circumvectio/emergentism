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
        cls.design = json.loads(
            (SITE / "emergentism-design.v1.json").read_text(encoding="utf-8")
        )
        cls.css = (SITE / "assets/css/gestalt-v2.css").read_text(encoding="utf-8")
        cls.js = (SITE / "assets/js/gestalt-v2.js").read_text(encoding="utf-8")

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
        self.assertEqual(len(rendered), len(shell.CORE_PAGES))
        self.assertTrue(
            {
                "questions/index.html",
                "ethics/index.html",
                "record/pqa-54/index.html",
            }
            <= set(shell.CORE_PAGES)
        )
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
                relative = path.relative_to(SITE).as_posix()
                self.assertIn('data-emergentism-design="v1"', body)
                self.assertIn(
                    f'data-emergentism-surface="{shell.SURFACE_FAMILIES[relative]}"',
                    body,
                )
                self.assertEqual(body.count('data-g2-semantic-key="v1"'), 1)

    def test_design_constitution_is_public_source_bound_and_checkable(self) -> None:
        self.assertEqual(self.design["schema"], "emergentism/PublicDesignContract.v1")
        self.assertEqual(self.design["version"], "1.0.0")
        self.assertEqual(
            set(self.design["semanticRoles"]),
            {"boundary", "actual", "possible", "conjecture", "evidence", "poison"},
        )
        self.assertEqual(len(self.design["routes"]), 32)
        self.assertTrue(self.design["boundary"]["projection_only"])
        self.assertFalse(self.design["boundary"]["creates_evidence"])
        self.assertFalse(self.design["boundary"]["creates_authority"])
        self.assertFalse(self.design["boundary"]["proves_comprehension"])
        self.assertEqual(self.design["adoptionState"]["reader_comprehension"], "untested")
        self.assertEqual(
            self.design["adoptionState"]["independent_accessibility_review"],
            "not_run",
        )
        for row in self.design["routes"]:
            with self.subTest(route=row["path"]):
                body = (SITE / row["path"]).read_text(encoding="utf-8")
                self.assertIn('data-emergentism-design="v1"', body)
                self.assertIn(
                    f'data-emergentism-surface="{row["family"]}"',
                    body,
                )
                self.assertEqual(body.count('data-g2-semantic-key="v1"'), 1)

        result = subprocess.run(
            [sys.executable, str(SITE / "check_design_constitution.py")],
            cwd=SITE,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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
        self.assertNotIn('aria-current="location"', nav)
        self.assertIn('data-current-section="true"', nav)
        exact_nav = shell.render_nav("worldview", "/plainly/")
        self.assertIn('href="/plainly/" aria-current="page"', exact_nav)
        self.assertNotIn('href="/" aria-current="page"', exact_nav)
        malformed = {
            "orphan nav marker": base.replace("<main>", "<!-- gestalt-core-nav:start --><main>"),
            "duplicate nav markers": base.replace("<main>", nav + nav + "<main>"),
            "wrong Gestalt version": base.replace("<html", '<html data-gestalt="v1"'),
            "wrong design version": base.replace(
                "<html", '<html data-emergentism-design="v0"'
            ),
            "wrong surface family": base.replace(
                "<body", '<body data-emergentism-surface="product"'
            ),
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
        self.assertIn('aria-labelledby="world-title"', overview)
        self.assertIn('aria-describedby="world-desc"', overview)
        self.assertNotRegex(overview, r'<figure[^>]+aria-labelledby=')
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

    def test_double_atlas_projection_rays_are_collinear_with_the_point(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        atlas = home.split('<figure class="g2-atlas g2-double-atlas"', 1)[1].split(
            "</figure>", 1
        )[0]
        point_match = re.search(
            r'<circle class="g2-svg-fill--actual" cx="([^"]+)" cy="([^"]+)"',
            atlas,
        )
        self.assertIsNotNone(point_match)
        point = tuple(float(value) for value in point_match.groups())

        for ray_class, plane_y in (
            ("possible-line", 92.0),
            ("evidence-line", 448.0),
        ):
            match = re.search(
                rf'<line class="{ray_class} g2-double-atlas__ray" '
                r'x1="([^"]+)" y1="([^"]+)" x2="([^"]+)" y2="([^"]+)"',
                atlas,
            )
            self.assertIsNotNone(match)
            x1, y1, x2, y2 = (float(value) for value in match.groups())
            px, py = point
            cross_product = (px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)
            self.assertAlmostEqual(cross_product, 0.0, delta=0.15)
            self.assertEqual(y2, plane_y)

    def test_actuality_firewall_is_typed_binary_and_reflows_without_clipping(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        firewall = home.split('id="actuality"', 1)[1]
        firewall = firewall.split("</section>", 1)[0]
        equation = firewall.split('<div class="g2-power-equation', 1)[1]
        equation = equation.split('<div class="g2-firewall-copy">', 1)[0]

        self.assertIn("g2-power-equation--binary", equation)
        self.assertIn('role="group"', equation)
        self.assertIn("g2-power-term--actual", equation)
        self.assertIn("V₄ · actual power", equation)
        self.assertIn("g2-power-term--possible", equation)
        self.assertIn("Φ₅ · possible power", equation)
        self.assertIn('<span class="g2-sr-only">is not equal to</span>', equation)
        self.assertNotIn("Scrollable", equation)
        self.assertNotIn('tabindex="0"', equation)
        self.assertIn("g2-loop g2-loop--compact", firewall)
        self.assertIn(".g2-loop--compact span:last-child { grid-column: span 2; }", self.css)

        self.assertRegex(
            self.css,
            r"\.g2-power-equation--binary\s*\{[^}]*grid-template-columns:\s*"
            r"minmax\(0, 1fr\)\s+44px\s+minmax\(0, 1fr\);",
        )
        self.assertRegex(
            self.css,
            r"\.g2-power-equation--binary\s+\.g2-power-term--actual\s+strong\s*"
            r"\{\s*color:\s*var\(--g2-actual\);",
        )
        self.assertRegex(
            self.css,
            r"\.g2-power-equation--binary\s+\.g2-power-term--possible\s+strong\s*"
            r"\{\s*color:\s*var\(--g2-possible\);",
        )
        self.assertIn("@media (max-width: 640px)", self.css)
        self.assertIn("@media (max-width: 760px)", self.css)
        self.assertNotIn(".g2-section h2 { font-size: clamp(2.65rem, 13vw, 4.4rem); }", self.css)

        dasein = (SITE / "dasein/index.html").read_text(encoding="utf-8")
        rosetta = (SITE / "rosetta/index.html").read_text(encoding="utf-8")
        self.assertIn("D5 possible power is not equal to its D4 estimate", dasein)
        self.assertIn("D5 possible power informs a present D4 evaluation", rosetta)
        self.assertIn('class="g2-power-equation" role="group"', dasein)
        self.assertIn('class="g2-power-equation" role="group"', rosetta)
        self.assertNotIn('class="g2-power-equation" role="region"', dasein)
        self.assertNotIn('class="g2-power-equation" role="region"', rosetta)
        self.assertNotIn('aria-label="Scrollable typed power relations"', dasein)
        self.assertNotIn('aria-label="Scrollable D5 to D4 action pathway"', rosetta)

    def test_static_accessibility_and_local_resource_contract(self) -> None:
        self.assertIn("min-height: 48px", self.css)
        self.assertIn("min-width: 48px", self.css)
        self.assertIn("prefers-reduced-motion: reduce", self.css)
        self.assertIn("forced-colors: active", self.css)
        self.assertRegex(
            self.css,
            r"\.g2-signature-grid\s*>\s*\*\s*\{\s*min-width:\s*0;",
        )
        self.assertRegex(
            self.css,
            r"\.g2-firewall-grid\s*>\s*\*,\s*\.g2-signature-grid\s*>\s*\*\s*"
            r"\{\s*min-width:\s*0;",
        )
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

    def test_finite_emergence_motion_is_opt_in_static_safe_and_bounded(self) -> None:
        self.assertIn('matchMedia?.("(prefers-reduced-motion: reduce)")', self.js)
        self.assertIn('"IntersectionObserver" in window', self.js)
        self.assertIn("observer.unobserve(entry.target)", self.js)
        self.assertIn('document.querySelectorAll(".g2-menu")', self.js)
        self.assertIn('root.dataset.gestaltMotion = "reduced"', self.js)
        self.assertIn('root.dataset.gestaltMotion = "static"', self.js)
        self.assertNotIn("requestAnimationFrame", self.js)
        self.assertNotIn("setInterval", self.js)
        self.assertNotRegex(self.js, r"\.hidden\s*=|setAttribute\([\"']aria-hidden|\binert\b")
        self.assertLess(len(self.js.encode("utf-8")), 8_000)

        self.assertIn("@keyframes g2-boundary-settle", self.css)
        self.assertIn("@keyframes g2-path-emerge", self.css)
        self.assertIn('html[data-gestalt-motion="active"]', self.css)
        self.assertIn(":focus-within", self.css)
        self.assertIn("stroke-dashoffset: 0 !important", self.css)

        opted_in = {
            relative
            for relative in shell.CORE_PAGES
            if "data-g2-reveal" in (SITE / relative).read_text(encoding="utf-8")
            or "data-g2-draw" in (SITE / relative).read_text(encoding="utf-8")
        }
        self.assertEqual(opted_in, {"index.html", "plainly/index.html", "dasein/index.html"})
        self.assertEqual(opted_in, set(self.design["motion"]["optInRoutes"]))

        home = (SITE / "index.html").read_text(encoding="utf-8")
        hero_copy = home.split(
            '<div class="g2-hero__copy g2-hero__opening">', 1
        )[1].split('<figure class="g2-atlas g2-world-figure"', 1)[0]
        self.assertNotIn("data-g2-reveal", hero_copy)
        self.assertNotIn("data-g2-draw", hero_copy)
        self.assertIn("guide-line", home)
        self.assertNotIn('data-g2-reveal="coins"', home)
        self.assertIn('data-cartographic-node="gestalt"', home)

    def test_reader_heading_and_interaction_controls_keep_release_semantics(self) -> None:
        book = (SITE / "book/index.html").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"<h1\b", book, re.I)), 1)
        self.assertEqual(
            len(re.findall(r'<header class="ch-head">.*?<h2\b', book, re.I)),
            12,
        )

        book_builder = (SITE / "build_book.py").read_text(encoding="utf-8")
        self.assertIn('heading_tag = "h1" if first else "h2"', book_builder)
        self.assertIn("min-height:48px", book_builder)

        atlas = (SITE / "assets/js/atlas-drawer.js").read_text(encoding="utf-8")
        book_ai = (SITE / "assets/js/book-ai.js").read_text(encoding="utf-8")
        outline = (SITE / "assets/js/workflowy-outline.js").read_text(encoding="utf-8")
        for source, panel_id in (
            (atlas, "atlas-panel"),
            (book_ai, "ask-panel"),
            (outline, "wf-rail"),
        ):
            with self.subTest(panel=panel_id):
                self.assertIn('setAttribute("aria-controls", "' + panel_id + '")', source)
                self.assertIn('setAttribute("aria-expanded", "false")', source)
                self.assertIn('setAttribute("aria-hidden", "true")', source)
                self.assertIn("min-height:48px", source)

        discoveries = (SITE / "discoveries/index.html").read_text(encoding="utf-8")
        self.assertIn('<h2 class="reveal">The trial board.</h2>', discoveries)

        practice = (SITE / "practice/index.html").read_text(encoding="utf-8")
        living_map = (SITE / "assets/css/living-map.css").read_text(encoding="utf-8")
        instrument = (SITE / "assets/css/burrisphere-instrument.css").read_text(encoding="utf-8")
        self.assertIn("min-height:48px;display:inline-flex", practice)
        self.assertIn(".filterbar button{min-height:48px", living_map)
        self.assertIn(".copy-button{min-width:48px;min-height:48px", living_map)
        self.assertIn(".bi-actions button span:last-child { display: block; }", instrument)
        self.assertIn("bottom: 402px; width: 255px", instrument)
        self.assertIn("min-height: 232px", instrument)
        self.assertIn("font-size: .58rem", instrument)
        self.assertNotIn(".bi-thesis { display: none; }", instrument)
        self.assertIn(".bi-boundary { display: block;", instrument)
        self.assertIn(".g2-page .g2-button--primary", self.css)
        self.assertIn("color:#989ca7", living_map)
        self.assertIn("opacity: .76", instrument)

        dimensions_builder = (SITE / "render_dimension_site.py").read_text(encoding="utf-8")
        self.assertIn(".crossing b{{color:var(--text-muted)}}", dimensions_builder)
        self.assertNotIn(".crossing b{{color:var(--text-dim)}}", dimensions_builder)

        record = (SITE / "record/index.html").read_text(encoding="utf-8")
        self.assertEqual(record.count('class="case'), 30)
        self.assertEqual(record.count('<h3 class="claimline" id="case-'), 29)
        self.assertEqual(record.count('aria-labelledby="case-'), 29)

    def test_definition_lists_use_native_list_markup(self) -> None:
        for relative in (
            "plainly/index.html",
            "dasein/index.html",
            "rosetta/index.html",
            "ethics/index.html",
            "record/pqa-54/index.html",
        ):
            page = (SITE / relative).read_text(encoding="utf-8")
            with self.subTest(page=relative):
                self.assertNotIn('<div class="g2-definition-list"', page)
                self.assertIn('<dl class="g2-definition-list"', page)

    def test_wide_burrisphere_atlas_is_named_and_keyboard_scrollable(self) -> None:
        for relative, cue_id in (
            ("burrisphere/index.html", "burrisphere-scroll-cue"),
        ):
            page = (SITE / relative).read_text(encoding="utf-8")
            with self.subTest(scroll_region=relative):
                self.assertIn('role="region"', page)
                self.assertIn('tabindex="0"', page)
                self.assertIn(f'aria-describedby="{cue_id}"', page)
                self.assertIn("Swipe or scroll sideways", page)

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
                "/dasein/", "/f5/", "/questions/", "/ethics/",
                "/churn/", "/amrita/", "/halahala/", "/record/churning/",
                "/churn/corpus.json", "/churn/corpus.jsonl", "/churn/corpus.md",
                "/record/pqa-54/", "/assets/css/gestalt-v2.css",
                "/assets/js/gestalt-v2.js", "/emergentism-design.v1.json",
                "/assets/fonts/Newsreader-latin-variable.woff2",
                "/burrisphere/", "/burrisphere/instrument/",
                "/assets/css/burrisphere-instrument.css", "/assets/js/burrisphere-instrument.js",
                "/vendor/three-0.160.0/three.module.js", "/vendor/three-0.160.0/controls/OrbitControls.js",
                "/favicon.svg",
            }.issubset(set(pwa.safe_spine()))
        )

    def test_homepage_is_ordered_showroom_with_reachable_workshop(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        nodes = re.findall(r'data-cartographic-node="([^"]+)"', home)
        self.assertEqual(
            nodes,
            [
                "gestalt", "ladder", "hinge", "instrument",
                "practice", "evidence", "research", "exit",
            ],
        )
        ladder = home.split('data-cartographic-node="ladder"', 1)[1].split(
            'data-cartographic-node="hinge"', 1
        )[0]
        for number in range(7):
            self.assertIn(f'href="/{number}/"', ladder)
        for tier in ("[A]", "[B]", "[S]", "[I]", "[C]", "[D]"):
            self.assertIn(tier, home)
        evidence = home.split('data-cartographic-node="evidence"', 1)[1].split(
            'data-cartographic-node="research"', 1
        )[0]
        self.assertIn("research lead, never truth evidence", evidence)
        self.assertIn("Convergence selects research questions", evidence)
        exit_field = home.split('data-cartographic-node="exit"', 1)[1].split("</section>", 1)[0]
        self.assertIn("The map remains optional.", exit_field)
        self.assertIn('href="/record/"', exit_field)
        self.assertIn('href="/churn/"', exit_field)
        self.assertIn('href="/exit/"', exit_field)
        self.assertNotIn("22 survivor candidates · 29 poison warnings", home)
        self.assertIn(
            "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved",
            home,
        )
        self.assertIn("--g2-poison: #d97557", self.css)
        self.assertIn(".g2-churn-seam__track", self.css)

    def test_homepage_instrument_practice_evidence_and_research_contracts(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        instrument = home.split('data-cartographic-node="instrument"', 1)[1].split(
            'data-cartographic-node="practice"', 1
        )[0]
        self.assertIn("g2-double-atlas", instrument)
        self.assertIn("Burrisphere visualizes. Rosetta translates. Neither transfers proof.", instrument)
        self.assertIn("bottom action/projection plane", instrument)
        self.assertIn("sphere path carries no transfer", instrument)
        self.assertIn("G7@1 ≠ GEN7@1", instrument)
        self.assertIn("OVERLAY NOT RUN", instrument)

        practice = home.split('data-cartographic-node="practice"', 1)[1].split(
            'data-cartographic-node="evidence"', 1
        )[0]
        self.assertIn("The Finity Card", practice)
        self.assertIn("No equation derives this ought.", practice)
        self.assertIn("Prepared decision transaction · unsigned", practice)
        self.assertIn("The action exit is the signature boundary", practice)
        self.assertIn("The separate worldview Exit", practice)

        evidence = home.split('data-cartographic-node="evidence"', 1)[1].split(
            'data-cartographic-node="research"', 1
        )[0]
        self.assertIn("no theorem is claimed as ours", evidence)
        self.assertIn("Selections that do work", evidence)
        self.assertIn("Counterexamples with teeth", evidence)
        self.assertIn("eight frozen gates admitted eight constructed evasions", evidence)
        self.assertIn("the prediction failed", evidence)
        self.assertNotIn("R2 says nothing about M4/F3", evidence)

        research = home.split('data-cartographic-node="research"', 1)[1].split(
            'data-cartographic-node="exit"', 1
        )[0]
        for heading in (
            "One of 24 assignments",
            "One present, three explanations",
            "Can an AI unfold—and revise—the account?",
            "Perennial questions remain earned results",
        ):
            self.assertIn(heading, research)
        for branch in ("F5-W", "F5-N", "F5-R"):
            self.assertIn(branch, research)
        self.assertIn("OFFLINE-READY", research)
        self.assertIn("no candidate has been evaluated", research)

    def test_homepage_post_audit_refinement_contract(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        legend = home.split('class="g2-tier-legend g2-tier-legend--early"', 1)[1].split(
            "</div>", 1
        )[0]
        ladder_offset = home.index('data-cartographic-node="ladder"')
        legend_offset = home.index('class="g2-tier-legend g2-tier-legend--early"')
        self.assertLess(legend_offset, ladder_offset)
        self.assertIn("the letters price claims, not people", home)
        for tier, meaning in (
            ("[A]", "proved within stated definitions or hypotheses"),
            ("[B]", "sourced, receipted, or observed"),
            ("[S]", "structural consequence inside a declared framework"),
            ("[I]", "interpretation, not derivation"),
            ("[C]", "a conjecture that can lose, with its kill stated"),
            ("[D]", "unresolved, staged, or awaiting a test"),
        ):
            self.assertIn(tier, legend)
            self.assertIn(meaning, legend)

        self.assertIn("One-minute field prompt", home)
        self.assertIn("The instrument does not decide.", home)
        self.assertIn("authority and any later act remain external", home)
        self.assertIn("This is a prompt—not a promised result.", home)
        self.assertGreater(
            home.index('class="g2-field-kit g2-field-kit--practice"'),
            home.index('data-cartographic-node="practice"'),
        )

        self.assertEqual(home.count('class="g2-atlas__viewport"'), 2)
        self.assertEqual(home.count('role="region" tabindex="0"'), 4)
        self.assertRegex(
            home,
            r'<svg[^>]+role="img"[^>]+aria-labelledby="world-title"[^>]+'
            r'aria-describedby="world-desc"',
        )
        self.assertRegex(
            home,
            r'<svg[^>]+role="img"[^>]+aria-labelledby="atlas-title"[^>]+'
            r'aria-describedby="atlas-desc"',
        )
        self.assertNotRegex(home, r'<figure[^>]+aria-labelledby=')
        self.assertGreaterEqual(home.count('<g aria-hidden="true">'), 2)
        self.assertEqual(home.count("Swipe to inspect"), 1)

        action_groups = re.findall(r'<div class="g2-actions">(.*?)</div>', home, re.S)
        self.assertEqual(len(action_groups), 6)
        for group in action_groups:
            self.assertEqual(group.count("g2-button--primary"), 1)
            self.assertNotIn('class="g2-button"', group)
        self.assertEqual(home.count("g2-action-link"), 6)

        self.assertIn('data-g2-rail data-active-section="Whole"', home)
        self.assertEqual(home.count("data-g2-rail-link"), 8)
        self.assertEqual(home.count('aria-current="location"'), 1)
        self.assertIn('.g2-atlas-rail a[aria-current="location"]', self.css)
        self.assertIn('content: "Journey"', self.css)
        self.assertIn("width: 760px", self.css)
        self.assertIn(".g2-action-link", self.css)
        self.assertIn('grid-template-columns: 1fr;', self.css)
        self.assertIn('document.querySelector("[data-g2-rail]")', self.js)
        self.assertIn('setAttribute("aria-current", "location")', self.js)
        self.assertNotIn("scrollIntoView", self.js)

        self.assertIn(
            "transaction means a structured decision packet—not money, signing, or execution",
            home,
        )
        self.assertIn("The prepared record is not outcome evidence", home)
        self.assertIn("solid and instantiated", home)
        self.assertNotIn("solid and settled", home)
        self.assertIn("Actual · solid and instantiated", self.design["requiredVisibleKey"])

    def test_homepage_h1_is_the_atlas_index_title(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", home, re.I | re.S)
        self.assertIsNotNone(h1)
        expected = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
        explicit = re.search(r'data-atlas-title="([^"]+)"', home)
        self.assertIsNotNone(explicit)
        self.assertEqual(explicit.group(1), expected)
        atlas = json.loads((SITE / "atlas/site_index.json").read_text(encoding="utf-8"))
        indexed = {
            page["href"]: page["title"]
            for section in atlas["tree"]
            for page in section["pages"]
        }
        self.assertEqual(indexed["/"], expected)
        self.assertEqual(indexed["/0/"], "/0 — Boundary frames")
        self.assertEqual(indexed["/practice/"], "The Practice — what a person actually does")
        self.assertEqual(indexed["/record/"], "The Trial Record")


if __name__ == "__main__":
    unittest.main()
