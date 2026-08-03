#!/usr/bin/env python3
"""Mutation checks for the dimension-first public release projection."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "12_PUBLIC_SITE"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parity = load("public_semantic_parity", SITE / "check_public_semantic_parity.py")
frozen = load("frozen_library_boundary", SITE / "apply_frozen_library_boundary.py")
renderer = load("dimension_renderer", SITE / "render_dimension_site.py")
rag_builder = load("book_rag_builder", SITE / "build_rag_index.py")
atlas_builder = load("atlas_builder", SITE / "build_atlas_index.py")
predeploy = load("public_predeploy", SITE / "predeploy_check.py")


class PublicReleaseSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((SITE / "public_semantic_parity.json").read_text(encoding="utf-8"))

    def test_exact_typed_sequence(self) -> None:
        self.assertEqual(self.data["sequence"], parity.EXPECTED_SEQUENCE)
        self.assertEqual([x["id"] for x in self.data["levels"]], [f"D{i}" for i in range(7)])
        transitions = [x["transition"]["id"] for x in self.data["levels"] if "transition" in x]
        self.assertEqual(transitions, ["mu0", "mu1", "mu2", "mu3", "mu4", "b6"])
        self.assertEqual(self.data["levels"][4]["modality"], "actual")
        self.assertEqual(self.data["levels"][5]["modality"], "possible")

    def test_claim_card_projection_contract_is_current(self) -> None:
        self.assertEqual(self.data["schemaVersion"], 2)
        contract = self.data["claimCardContract"]
        source = ROOT / contract["source"]
        self.assertEqual(
            contract["sourceRevision"],
            "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest(),
        )
        register = json.loads((ROOT / contract["register"]).read_text(encoding="utf-8"))
        known = {card["card_id"] for card in register["cards"]}
        for level in self.data["levels"]:
            self.assertTrue(level["claimCardIds"])
            self.assertTrue(set(level["claimCardIds"]) <= known)
            self.assertEqual(level["sourceRevision"], contract["sourceRevision"])
            self.assertEqual(level["lifecycle"], "reader_synthesis")
            self.assertEqual(level["publicDisposition"], "bounded_current")

    def test_forbidden_claim_mutations_are_caught(self) -> None:
        mutations = {
            "literal D6 identity": "D6 ≡ D0",
            "extra mu crossing": "μ5 opens",
            "invalid scalar sampling": "Sample[∫|ψ|²]",
            "physical cone inflation": "the physical light cone widens",
            "quantum dimensional stacking": "Everett is a five-dimensional realm",
            "quantum-gravity solution inflation": "we solved quantum gravity",
            "zero-momentum D3 inflation": "D3 has no momentum",
            "application authority leakage": "Sky" + "zai governs this claim",
        }
        for name, text in mutations.items():
            with self.subTest(name=name):
                self.assertRegex(text, parity.FORBIDDEN[name])

    def test_provisional_surfaces_are_inside_parity_prohibition_scope(self) -> None:
        audited = set(parity.parity_audit_surfaces(self.data))
        provisional = set(self.data["declaredProvisional"]["routes"])
        self.assertTrue(provisional)
        self.assertTrue(provisional <= audited)
        self.assertTrue(set(self.data["currentSurfaces"]) <= audited)
        self.assertTrue(
            set(self.data["infrastructureRoutes"]["routes"]).isdisjoint(audited)
        )

    def test_d3_preserves_momentum_and_open_physics(self) -> None:
        d3 = self.data["levels"][3]
        joined = " ".join(str(value) for value in d3.values())
        self.assertIn("momentum distributions", joined)
        self.assertIn("noncommuting observables", joined)
        self.assertIn("does not solve measurement, quantum gravity", joined)

    def test_renderer_is_deterministic_and_instrument_is_wired(self) -> None:
        first = renderer.render()
        second = renderer.render()
        self.assertEqual(first, second)
        for path, body in first.items():
            if path.parent.name == "dimensions":
                continue
            self.assertIn('class="diagram visual-panel"', body)
            self.assertIn('type="importmap"', body)
            self.assertIn('type="module" src="../dimensions/dimensions.js"', body)

    def test_frozen_boundary_is_idempotent(self) -> None:
        sample = "<html><body><main>old claim</main></body></html>"
        once = frozen.desired(sample)
        self.assertIn(frozen.MARKER, once)
        self.assertEqual(frozen.desired(once), once)

    def test_rag_excludes_frozen_library(self) -> None:
        rag = json.loads((SITE / "book/rag_index.json").read_text(encoding="utf-8"))
        prefixes = tuple(f"{root}:" for root in self.data["frozenLibraryRoots"])
        self.assertTrue(rag["passages"])
        self.assertFalse(any(str(item.get("id", "")).startswith(prefixes) for item in rag["passages"]))

    def test_release_checker_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SITE / "check_public_semantic_parity.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_atlas_generator_check_binds_full_provenance_payload(self) -> None:
        payload = atlas_builder.build_payload()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "site_index.json"
            original_output = atlas_builder.OUT
            try:
                atlas_builder.OUT = output
                output.write_text(atlas_builder.canonical_payload(payload), encoding="utf-8")
                self.assertEqual(atlas_builder.main(["--check"]), 0)
                for field, value in (
                    ("schemaVersion", 999),
                    ("generated", "unbound-generator.py"),
                    ("source", "unbound-source.json"),
                    ("exclusions", {}),
                ):
                    with self.subTest(field=field):
                        corrupted = dict(payload)
                        corrupted[field] = value
                        output.write_text(
                            atlas_builder.canonical_payload(corrupted), encoding="utf-8"
                        )
                        self.assertEqual(atlas_builder.main(["--check"]), 1)
            finally:
                atlas_builder.OUT = original_output

    def test_corpus_gate_runs_public_predeploy(self) -> None:
        gate = (ROOT / "09_TOOLS/01_SCRIPTS/gate.sh").read_text(encoding="utf-8")
        self.assertIn('"12_PUBLIC_SITE/predeploy_check.py"', gate)

    def test_css_parser_dependency_is_pinned_for_the_public_gate(self) -> None:
        requirements = (ROOT / "09_TOOLS/01_SCRIPTS/requirements.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"tinycss2=={predeploy.TINYCSS2_REQUIRED_VERSION}", requirements)

    def test_predeploy_parses_single_quoted_unquoted_and_protocol_relative_resources(self) -> None:
        body = (
            "<a href='missing.html'>missing</a>"
            "<link rel='stylesheet' href=//cdn.example/style.css>"
            "<script src='https://cdn.example/app.js'></script>"
            "<img src=//cdn.example/card.png>"
            "<script src='https://evil.example/first.js' src='/assets/js/safe.js'></script>"
            "<link rel='preload' as='script' href=https://cdn.example/preload.js>"
            "<link rel='dns-prefetch' href=//dns.example>"
            "<img srcset='https://cdn.example/first.png 1x, /assets/second.png 2x'>"
            "<input type='image' src='https://cdn.example/button.png'>"
            "<svg><image href='https://cdn.example/vector.png'></image>"
            "<feImage xlink:href='//cdn.example/filter.png'></feImage></svg>"
            "<svg><script href='https://cdn.example/svg-script.js'></script>"
            "<script xlink:href='//cdn.example/svg-xlink.js'></script></svg>"
            "<svg><audio href='https://cdn.example/svg-audio.mp3'></audio>"
            "<video xlink:href='//cdn.example/svg-video.mp4'></video>"
            "<iframe href='https://cdn.example/svg-frame.html'></iframe>"
            "<foreignObject xlink:href='//cdn.example/svg-foreign.html'></foreignObject>"
            "<font-face-uri xlink:href='https://cdn.example/svg-font.svg'></font-face-uri></svg>"
            "<svg><rect cursor='url(https://cdn.example/cursor.png), auto'"
            " filter='url(//cdn.example/filter.svg#f)' fill='url(https://cdn.example/paint.svg#g)'"
            " stroke='url(//cdn.example/stroke.svg#s)' clip-path='url(https://cdn.example/clip.svg#c)'"
            " mask='url(//cdn.example/mask.svg#m)' marker-start='url(https://cdn.example/start.svg#a)'"
            " marker-mid='url(//cdn.example/mid.svg#a)' marker-end='url(https://cdn.example/end.svg#a)'></rect></svg>"
            "<iframe srcdoc=\"&lt;script src='https://cdn.example/srcdoc.js'&gt;&lt;/script&gt;\"></iframe>"
            "<style>@import \"https://cdn.example/theme.css\"; .x { background: url(//cdn.example/bg.png); }</style>"
            "<style>.image { background-image: image-set(\"https://cdn.example/one.png\" 1x, url(//cdn.example/two.png) 2x); }</style>"
            "<style>.webkit { background-image: -webkit-image-set(\"https://cdn.example/webkit.png\" 1x); }</style>"
            "<div style='background-image: url(https://cdn.example/inline.png)'></div>"
        )
        escaped_css = r'.escape { background-image: url("https\3a //escaped.example/p.png"); }'
        body += f"<style>{escaped_css}</style>"
        body += (
            "<iframe src='data:text/html,%3Cscript%20src%3D%22https%3A%2F%2Fcdn.example%2Fdata.js%22%3E%3C%2Fscript%3E'></iframe>"
            "<img src='data:image/svg+xml,%3Csvg%3E%3Cscript%20href%3D%22https%3A%2F%2Fcdn.example%2Fdata-svg.js%22%3E%3C%2Fscript%3E%3C%2Fsvg%3E'>"
            "<img src='data:text/xml,%3Csvg%2F%3E'>"
            "<img src='data:image/svg+xml,%3C%3Fxml-stylesheet%20href%3D%22https%3A%2F%2Fcdn.example%2Fdata.css%22%3F%3E%3Csvg%2F%3E'>"
        )
        self.assertIn("missing.html", predeploy.extract_hrefs(body))
        root_target, target_type = predeploy.resolve_link("home/index.html", "../", "../")
        self.assertEqual(target_type, "relative")
        self.assertEqual(Path(root_target), SITE)
        self.assertTrue(predeploy.is_inside_public_root(root_target))
        self.assertTrue(
            {
                ("link", "//cdn.example/style.css"),
                ("script", "https://cdn.example/app.js"),
                ("img", "//cdn.example/card.png"),
                ("script", "https://evil.example/first.js"),
                ("link", "https://cdn.example/preload.js"),
                ("link", "//dns.example"),
                ("img srcset", "https://cdn.example/first.png"),
                ("input", "https://cdn.example/button.png"),
                ("image", "https://cdn.example/vector.png"),
                ("feimage", "//cdn.example/filter.png"),
                ("script", "https://cdn.example/svg-script.js"),
                ("script", "//cdn.example/svg-xlink.js"),
                ("audio", "https://cdn.example/svg-audio.mp3"),
                ("video", "//cdn.example/svg-video.mp4"),
                ("iframe", "https://cdn.example/svg-frame.html"),
                ("foreignobject", "//cdn.example/svg-foreign.html"),
                ("font-face-uri", "https://cdn.example/svg-font.svg"),
                ("rect cursor", "https://cdn.example/cursor.png"),
                ("rect filter", "//cdn.example/filter.svg#f"),
                ("rect fill", "https://cdn.example/paint.svg#g"),
                ("rect stroke", "//cdn.example/stroke.svg#s"),
                ("rect clip-path", "https://cdn.example/clip.svg#c"),
                ("rect mask", "//cdn.example/mask.svg#m"),
                ("rect marker-start", "https://cdn.example/start.svg#a"),
                ("rect marker-mid", "//cdn.example/mid.svg#a"),
                ("rect marker-end", "https://cdn.example/end.svg#a"),
                ("iframe srcdoc script", "https://cdn.example/srcdoc.js"),
                ("style", "https://cdn.example/theme.css"),
                ("style", "//cdn.example/bg.png"),
                ("style", "https://cdn.example/one.png"),
                ("style", "//cdn.example/two.png"),
                ("style", "https://cdn.example/webkit.png"),
                ("style", "https://escaped.example/p.png"),
                ("div inline style", "https://cdn.example/inline.png"),
                ("prohibited iframe text/html data document", "text/html"),
                ("img SVG data script", "https://cdn.example/data-svg.js"),
                ("prohibited img text/xml data document", "text/xml"),
                ("img SVG data prohibited SVG XML stylesheet", "xml-stylesheet"),
            }.issubset(set(predeploy.external_resource_references(body)))
        )
        with self.assertRaisesRegex(ValueError, "CSS parse error"):
            predeploy.external_resource_references(
                "<style>@import \"https://cdn.example/unclosed.css\";<body>still style"
            )

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "index.html").write_text(body, encoding="utf-8")
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    self.assertTrue(any("//cdn.example/style.css" in item for item in predeploy.ERRORS))
                    self.assertTrue(any("https://cdn.example/app.js" in item for item in predeploy.ERRORS))
                finally:
                    predeploy.ERRORS.clear()

    def test_predeploy_rejects_external_base_and_keeps_local_base_route_semantics(self) -> None:
        external_base = (
            "<base href='https://evil.example/'>"
            "<script src='assets/app.js'></script><a href='safe.html'>safe</a>"
        )
        self.assertIn(("base", "https://evil.example/"), predeploy.external_resource_references(external_base))
        self.assertEqual(predeploy.extract_hrefs(external_base), ["safe.html"])
        self.assertEqual(
            predeploy.base_href_issues("index.html", "<base href='//evil.example/'>"),
            [("base", "//evil.example/")],
        )
        self.assertEqual(
            predeploy.base_href_issues("index.html", r"<base href='https:\evil.example/'>"),
            [("base", r"https:\evil.example/")],
        )
        self.assertEqual(
            predeploy.base_href_issues("index.html", "<base href='///evil.example/'>"),
            [("base", "///evil.example/")],
        )
        self.assertTrue(predeploy.is_external_resource("////evil.example/asset.js"))
        self.assertTrue(predeploy.is_external_resource("file:///private/asset.js"))

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "index.html").write_text(external_base, encoding="utf-8")
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    self.assertTrue(any("external base" in item for item in predeploy.ERRORS))
                    predeploy.ERRORS.clear()
                    self.assertFalse(predeploy.check_internal_links())
                    self.assertTrue(any("unsafe base" in item for item in predeploy.ERRORS))
                finally:
                    predeploy.ERRORS.clear()

    def test_predeploy_follows_declarative_svg_manifest_and_extensionless_surfaces(self) -> None:
        body = (
            "<link rel='preload' as='image' "
            "imagesrcset='https://evil.example/preload.png 1x, /safe.png 2x'>"
            "<link rel='manifest' href='site-manifest?revision=1'>"
            "<link rel='stylesheet' href='assets/stylesheet'>"
            "<iframe src='embedded-document'></iframe>"
            "<meta http-equiv='refresh' content='0; url=https://evil.example/refresh'>"
            "<script type='speculationrules'>"
            '{"prefetch":[{"urls":["https://evil.example/next"]}]}'
            "</script>"
            "<img src='/local.png' attributionsrc='https://evil.example/attribution'>"
            "<model src='https://evil.example/model.usdz' "
            "environmentmap='https://evil.example/night.hdr'></model>"
            "<svg xml:base='https://evil.example/'><image href='local.svg'></image></svg>"
        )
        refs = set(predeploy.external_resource_references(body))
        self.assertTrue(
            {
                ("link imagesrcset", "https://evil.example/preload.png"),
                ("meta refresh", "https://evil.example/refresh"),
                ("speculationrules prefetch", "https://evil.example/next"),
                ("img attributionsrc", "https://evil.example/attribution"),
                ("model", "https://evil.example/model.usdz"),
                ("model", "https://evil.example/night.hdr"),
                ("xml:base", "https://evil.example/"),
            }.issubset(refs)
        )
        with self.assertRaisesRegex(ValueError, "document-selected speculationrules"):
            predeploy.external_resource_references(
                "<script type='speculationrules'>"
                '{"prefetch":[{"source":"document","where":{"href_matches":"https://evil.example/*"}}]}'
                "</script>"
            )
        self.assertIn(
            ("link", "https://evil.example/prefixed.css"),
            predeploy.svg_external_resource_references(
                "<svg xmlns='http://www.w3.org/2000/svg' "
                "xmlns:h='http://www.w3.org/1999/xhtml'>"
                "<h:link rel='stylesheet' href='https://evil.example/prefixed.css'/></svg>",
                "prefixed.svg",
            ),
        )
        self.assertIn(
            ("image", "https://evil.example/prefixed.svg"),
            predeploy.svg_external_resource_references(
                "<svg:svg xmlns:svg='http://www.w3.org/2000/svg' "
                "xmlns:x='http://www.w3.org/1999/xlink'>"
                "<svg:image x:href='https://evil.example/prefixed.svg'/></svg:svg>",
                "prefixed.svg",
            ),
        )
        self.assertIn(
            ("manifest localized icon", "https://evil.example/fr.png"),
            predeploy.webmanifest_resource_candidates(
                '{"icons_localized":{"fr":[{"src":"https://evil.example/fr.png"}]}}',
                "manifest.webmanifest",
            ),
        )

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "index.html").write_text(
                "<link rel='manifest' href='site-manifest?revision=1'>"
                "<link rel='stylesheet' href='assets/stylesheet'>"
                "<iframe src='embedded-document'></iframe>",
                encoding="utf-8",
            )
            (site / "assets").mkdir()
            (site / "assets" / "stylesheet").write_text(
                "@import url('https://evil.example/extensionless.css');", encoding="utf-8"
            )
            (site / "embedded-document").write_text(
                "<script src='https://evil.example/extensionless-document.js'></script>",
                encoding="utf-8",
            )
            (site / "asset.XML").write_text(
                "<svg:svg xmlns:svg='http://www.w3.org/2000/svg'>"
                "<svg:image href='https://evil.example/xml-asset.svg'/></svg:svg>",
                encoding="utf-8",
            )
            (site / "site-manifest").write_text(
                '{"icons":[{"src":"https://evil.example/manifest-icon.png"}]}',
                encoding="utf-8",
            )
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    joined = "\n".join(predeploy.ERRORS)
                    self.assertIn("extensionless.css", joined)
                    self.assertIn("extensionless-document.js", joined)
                    self.assertIn("xml-asset.svg", joined)
                    self.assertIn("manifest-icon.png", joined)
                finally:
                    predeploy.ERRORS.clear()

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site.parent / "outside.html").write_text("[A] outside", encoding="utf-8")
            (site / "public_semantic_parity.json").write_text(
                '{"currentSurfaces":["../outside.html"],"declaredProvisional":{"routes":[]}}',
                encoding="utf-8",
            )
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                with self.assertRaisesRegex(ValueError, "escapes 12_PUBLIC_SITE"):
                    predeploy.declared_semantic_html_files()

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site.parent / "outside.js").write_text("outside", encoding="utf-8")
            (site.parent / "outside.css").write_text("outside", encoding="utf-8")
            (site / "index.html").write_text(
                "<script src='../outside.js'></script>"
                "<style>@import url('../outside.css');</style>",
                encoding="utf-8",
            )
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    self.assertTrue(
                        any("script -> ../outside.js (escapes public-site root)" in item for item in predeploy.ERRORS)
                    )
                    self.assertTrue(
                        any("style -> ../outside.css (escapes public-site root)" in item for item in predeploy.ERRORS)
                    )
                finally:
                    predeploy.ERRORS.clear()

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "index.html").write_text("<p>local page</p>", encoding="utf-8")
            (site / "assets").mkdir()
            (site / "assets" / "site.css").write_text(
                "@import url(//cdn.example/theme.css);", encoding="utf-8"
            )
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    self.assertTrue(any("assets/site.css" in item for item in predeploy.ERRORS))
                finally:
                    predeploy.ERRORS.clear()

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "index.html").write_text(
                "<style>@import \"https://cdn.example/unclosed.css\";<body>still style",
                encoding="utf-8",
            )
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    self.assertTrue(
                        any("cannot verify static resource references" in item for item in predeploy.ERRORS)
                    )
                finally:
                    predeploy.ERRORS.clear()

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "index.html").write_text("<p>local page</p>", encoding="utf-8")
            (site / "assets").mkdir()
            (site / "assets" / "site.css").write_text(
                '@import url("data:text/css,%40import%20url(https%3A%2F%2Fevil.example%2Fa.css)%3B");',
                encoding="utf-8",
            )
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    self.assertTrue(
                        any("prohibited css text/css data document" in item for item in predeploy.ERRORS)
                    )
                finally:
                    predeploy.ERRORS.clear()

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "docs" / "assets").mkdir(parents=True)
            (site / "docs" / "index.html").write_text(
                "<base href='assets/'><a href='safe.html'>safe</a>", encoding="utf-8"
            )
            (site / "docs" / "assets" / "safe.html").write_text("safe", encoding="utf-8")
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertTrue(predeploy.check_internal_links())
                finally:
                    predeploy.ERRORS.clear()

    def test_predeploy_closes_xhtml_automatic_manifest_and_svg_routes(self) -> None:
        """Regression fence for declarative surfaces outside ordinary .html pages."""

        self.assertIn(
            ("unverifiable img", "%FF"),
            predeploy.html_resource_root_escapes("<img src='%FF'>", "index.html"),
        )

        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site / "index.html").write_text(
                "<meta http-equiv='refresh' content='0;url=refresh-route'>"
                "<link rel='prefetch' href='prefetch-route'>"
                "<link rel='prerender' href='prerender-route'>"
                "<iframe src='xhtml-route'></iframe>"
                "<script type='speculationrules'>"
                '{"prefetch":[{"urls":["speculation-route"]}]}'
                "</script>"
                "<link rel='manifest' href='manifest.webmanifest'>",
                encoding="utf-8",
            )
            for route, source in {
                "refresh-route": "refresh.js",
                "prefetch-route": "prefetch.js",
                "prerender-route": "prerender.js",
                "speculation-route": "speculation.js",
                "manifest-route": "manifest.js",
            }.items():
                (site / route).write_text(
                    f"<script src='https://evil.example/{source}'></script>", encoding="utf-8"
                )
            (site / "manifest.webmanifest").write_text(
                json.dumps(
                    {
                        "start_url": "manifest-route",
                        "scope_extensions": [{"origin": "https://evil.example/scope"}],
                        "url_handlers": [{"origin": "https://evil.example/handler"}],
                        "serviceworker": {"src": "https://evil.example/worker.js"},
                    }
                ),
                encoding="utf-8",
            )
            (site / "prefixed.xhtml").write_text(
                "<?xml version='1.0'?>"
                "<h:html xmlns:h='http://www.w3.org/1999/xhtml'><h:head>"
                "<h:style><![CDATA[body{background:url(https://evil.example/xhtml.png)}]]>"
                "</h:style></h:head><h:body/></h:html>",
                encoding="utf-8",
            )
            (site / "xhtml-route").write_text(
                "<h:html xmlns:h='http://www.w3.org/1999/xhtml'><h:head>"
                "<h:style><![CDATA[body{background:url(https://evil.example/extensionless-xhtml.png)}]]>"
                "</h:style></h:head><h:body/></h:html>",
                encoding="utf-8",
            )
            (site / "legacy.htm").write_text(
                "<script src='https://evil.example/legacy.js'></script>", encoding="utf-8"
            )
            (site / "feed.rss").write_text(
                "<?xml-stylesheet href='https://evil.example/feed.css'?><rss/>", encoding="utf-8"
            )
            (site / "animated.svg").write_text(
                "<svg xmlns='http://www.w3.org/2000/svg'><image id='i' href='/local'/>"
                "<animate href='#i' attributeName='href' to='https://evil.example/smil.png'/>"
                "</svg>",
                encoding="utf-8",
            )
            (site / "legacy-background.html").write_text(
                "<table><tr background='https://evil.example/row.png'></tr></table>",
                encoding="utf-8",
            )
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_external_refs())
                    joined = "\n".join(predeploy.ERRORS)
                    for expected in (
                        "refresh.js",
                        "prefetch.js",
                        "prerender.js",
                        "speculation.js",
                        "manifest.js",
                        "manifest scope extension",
                        "manifest URL handler",
                        "manifest serviceworker source",
                        "xhtml.png",
                        "extensionless-xhtml.png",
                        "legacy.js",
                        "prohibited XML stylesheet",
                        "prohibited SVG SMIL URL animation",
                        "row.png",
                    ):
                        self.assertIn(expected, joined)
                finally:
                    predeploy.ERRORS.clear()

    def test_predeploy_rejects_single_quoted_missing_link_and_tierless_current_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "withheld-routes.json").write_text('{"artifacts": []}', encoding="utf-8")
            (site.parent / "outside.html").write_text("outside", encoding="utf-8")
            (site / "index.html").write_text(
                "<a href='missing.html'>missing</a><a href='../outside.html'>outside</a>",
                encoding="utf-8",
            )
            (site / "public_semantic_parity.json").write_text(
                '{"currentSurfaces": ["current/index.html"], "declaredProvisional": {"routes": []}}',
                encoding="utf-8",
            )
            (site / "current").mkdir()
            (site / "current/index.html").write_text("<p>no tier</p>", encoding="utf-8")
            with patch.object(predeploy, "BASE_DIR", str(site)), patch.object(
                predeploy, "WITHHELD_REGISTRY_PATH", str(site / "withheld-routes.json")
            ):
                predeploy.ERRORS.clear()
                try:
                    self.assertFalse(predeploy.check_internal_links())
                    self.assertTrue(any("missing.html" in item for item in predeploy.ERRORS))
                    self.assertTrue(any("escapes public-site root" in item for item in predeploy.ERRORS))
                    predeploy.ERRORS.clear()
                    self.assertFalse(predeploy.check_tier_markers())
                    self.assertTrue(any("current/index.html" in item for item in predeploy.ERRORS))
                finally:
                    predeploy.ERRORS.clear()

    def test_public_book_manifest_is_current(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SITE / "build_book.py"), "--check"],
            cwd=SITE,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        manifest = json.loads((SITE / "book/build-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], "emergentism/public-book-build/v2")
        self.assertEqual(manifest["work_id"], "BK-ONE-SITTING")

        # v2 is deliberately narrower than the retired 29-source projection:
        # one current reader source, with exact byte custody, and no inherited
        # Reciprocal chapters silently entering either output or retrieval.
        self.assertEqual(len(manifest["sources"]), 1)
        source = manifest["sources"][0]
        self.assertEqual(source["path"], "00_THE_WELTANSCHAUUNG_ONE_SITTING.md")
        self.assertEqual(source["lifecycle"], "reader_synthesis")
        self.assertIs(source["public_eligible"], True)
        self.assertEqual(manifest["ordered_source_paths"], [source["path"]])
        self.assertEqual(
            source["sha256"],
            hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest(),
        )

        catalog = manifest["catalog_contract"]
        self.assertEqual(catalog["schema"], "emergentism/book-manifest/v1")
        self.assertEqual(catalog["path"], "13_BOOKS/book-manifest.json")
        self.assertEqual(catalog["release_state"], "source_active_current_public_reader")
        self.assertEqual(catalog["public_route"], "../12_PUBLIC_SITE/book/index.html")
        self.assertEqual(
            catalog["sha256"],
            hashlib.sha256((ROOT / catalog["path"]).read_bytes()).hexdigest(),
        )

        output = manifest["output"]
        self.assertEqual(output["path"], "book/index.html")
        self.assertEqual(
            output["sha256"],
            hashlib.sha256((SITE / output["path"]).read_bytes()).hexdigest(),
        )
        coverage = manifest["claim_card_contract"]["coverage"]
        self.assertEqual(coverage["claim_card_count"], 26)
        self.assertEqual(len(coverage["rendered_source_chapter_order"]), 12)
        self.assertEqual(coverage["public_states"], ["bounded_current", "candidate"])
        self.assertEqual(coverage["review_states"], ["implemented", "l3_audited"])

        withheld = manifest["withheld_provenance"]
        self.assertEqual(withheld["path"], "13_BOOKS/the_reciprocal/")
        self.assertEqual(withheld["lifecycle"], "withheld_staged_provenance")
        self.assertIs(withheld["included_in_output"], False)
        self.assertIs(withheld["included_in_rag"], False)

    def test_public_book_routes_grand_puzzle_to_its_explicit_boundary(self) -> None:
        book = (SITE / "book/index.html").read_text(encoding="utf-8")
        self.assertEqual(book.count('href="../lab/#questions"'), 2)
        self.assertIn(
            '<a href="../lab/#questions"><code>Grand Puzzle Assembly Ledger</code></a>',
            book,
        )
        self.assertIn(
            '<a href="../lab/#questions"><code>Grand Puzzle Assembly</code></a>',
            book,
        )
        self.assertIn('<a href="../sources/"><code>The Lived Compass</code></a>', book)

    def test_rag_source_integrity_negative_controls(self) -> None:
        # The generator's permanent controls must reject both loss of the
        # declared source and byte drift against its v2 SHA-256 receipt.
        rag_builder.source_negative_controls()


if __name__ == "__main__":
    unittest.main()
