"""Release regressions: exact projections and narrowly bounded exceptions."""

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import build_wisdom_atlas as wisdom
import check_public_semantic_parity as parity
import build_withholding_boundary as withholding
import predeploy_check as predeploy
from build_core_shell import THEME_BOOT


SITE = Path(__file__).resolve().parent


class PublicWisdomReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rendered = wisdom.outputs()

    def test_all_six_outputs_are_reproducible(self):
        self.assertEqual(len(self.rendered), 6)
        self.assertEqual(self.rendered, wisdom.outputs())
        for path, expected in self.rendered.items():
            with self.subTest(path=path.name):
                self.assertEqual(path.read_text(encoding="utf-8"), expected)

    def test_check_rejects_each_drifted_output_without_rewriting(self):
        # Exercise the actual CLI check loop on temporary paths, not the live site.
        with tempfile.TemporaryDirectory(prefix="em-wisdom-negative-") as temp:
            root = Path(temp)
            outputs = {root / p.relative_to(SITE): value for p, value in self.rendered.items()}
            for path, expected in outputs.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")
            with mock.patch.object(wisdom, "SITE", root), mock.patch.object(wisdom, "outputs", return_value=outputs), mock.patch.object(sys, "argv", ["build_wisdom_atlas.py", "--check"]):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(wisdom.main(), 0)
                for path, expected in outputs.items():
                    with self.subTest(path=path.name):
                        damaged = expected + "UNREVIEWED DRIFT\n"
                        path.write_text(damaged, encoding="utf-8")
                        with contextlib.redirect_stdout(io.StringIO()):
                            self.assertEqual(wisdom.main(), 1)
                        self.assertEqual(path.read_text(encoding="utf-8"), damaged)
                        path.unlink()
                        with contextlib.redirect_stdout(io.StringIO()):
                            self.assertEqual(wisdom.main(), 1)
                        self.assertFalse(path.exists())
                        path.write_text(expected, encoding="utf-8")

    def test_default_artifact_gate_runs_wisdom_check(self):
        path = SITE.parent / "09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py"
        spec = importlib.util.spec_from_file_location("artifact_gate", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertIn("build_wisdom_atlas.py", module.BUILDERS)

    def test_local_browser_artifacts_never_enter_manual_deployment(self):
        patterns = predeploy.load_vercelignore_patterns()
        self.assertIn("/output/", patterns)
        for rel in ("output/playwright/capture.png", "output/playwright/report.json", "output/playwright/.playwright-cli/page.yml", "output/accidental/index.html"):
            with self.subTest(rel=rel):
                self.assertTrue(predeploy.is_vercel_ignored(rel, patterns))
        for rel in ("index.html", "wisdom/index.html", "wisdom/atlas.json", "wisdom/rag.jsonl", "assets/og/og-card.png", "assets/output/capture.png", "outputish/capture.png", "output.png", "wisdom/output/nested.json"):
            with self.subTest(rel=rel):
                self.assertFalse(predeploy.is_vercel_ignored(rel, patterns))
        # The new anchored rule closes the output hole rather than relying on
        # an unrelated ignore, and does not change Git visibility or custody.
        without_output = [p for p in patterns if p != "/output/"]
        self.assertFalse(predeploy.is_vercel_ignored("output/playwright/capture.png", without_output))

    def test_predeploy_refuses_missing_or_negated_output_boundary(self):
        patterns = predeploy.load_vercelignore_patterns()
        for damaged in ([p for p in patterns if p != "/output/"], patterns + ["!/output/"]):
            with mock.patch.object(predeploy, "load_vercelignore_patterns", return_value=damaged), mock.patch.object(predeploy, "check_declared_public_head_custody", return_value=True), mock.patch.object(predeploy, "error") as error, contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(predeploy.check_publication_boundary())
                self.assertTrue(any("output/" in str(call) for call in error.call_args_list))

    def test_machine_exports_keep_independent_status_axes(self):
        bundle, compiled = wisdom.load_source()
        output = wisdom.machine_outputs(bundle, compiled)
        rows = [json.loads(line) for line in output[SITE / "wisdom/rag.jsonl"].splitlines()]
        compact, boundary, *cards = rows
        for key in ("kind", "maturity", "projection", "evidence_tier", "scope", "authority"):
            self.assertEqual(compact[key], bundle["records"][0][key])
        self.assertNotIn("maturity", boundary)
        for row, source in zip(cards, bundle["cards"], strict=True):
            self.assertNotIn("maturity", row)
            for key in ("coverage_state", "application_status", "adoption_state", "evidence_tier", "source_ids", "authority_effect", "may_sign", "may_authorize"):
                self.assertEqual(row[key], source[key])
        # A later correction must not be flattened to the first release's label.
        revised = copy.deepcopy(bundle)
        revised["records"][0]["maturity"] = "CONTESTED"
        updated = wisdom.machine_outputs(revised, compiled)
        self.assertEqual(json.loads(updated[SITE / "wisdom/rag.jsonl"].splitlines()[0])["maturity"], "CONTESTED")

    def test_machine_source_references_are_resolvable_metadata_only(self):
        bundle, compiled = wisdom.load_source()
        output = wisdom.machine_outputs(bundle, compiled)
        atlas = json.loads(output[SITE / "wisdom/atlas.json"])
        header = json.loads(output[SITE / "wisdom/atlas.jsonl"].splitlines()[0])["value"]
        for carrier in (atlas, header):
            self.assertEqual(carrier["source_manifest"], bundle["manifest"])
            self.assertEqual(carrier["source_manifest_sha256"], compiled["source_manifest_sha256"])
            self.assertEqual(carrier["input_hashes"], compiled["input_hashes"])
        sources = {s["source_id"]: s for s in atlas["source_manifest"]["sources"]}
        repositories = {r["repo_id"]: r for r in atlas["source_manifest"]["repositories"]}
        self.assertEqual(len(sources), len(atlas["source_manifest"]["sources"]))
        for row in atlas["records"] + atlas["application_cards"]:
            for source_id in row["source_ids"]:
                self.assertIn(source_id, sources)
                self.assertIn(sources[source_id]["repo_id"], repositories)
        for line in output[SITE / "wisdom/rag.jsonl"].splitlines():
            row = json.loads(line)
            self.assertEqual(row["source_manifest_sha256"], compiled["source_manifest_sha256"])
            artifact = row["source_artifact"]
            self.assertFalse(Path(artifact["path"]).is_absolute())
            self.assertEqual(hashlib.sha256((wisdom.ROOT / artifact["path"]).read_bytes()).hexdigest(), artifact["sha256"])
            self.assertEqual([ref["source_id"] for ref in row["source_refs"]], row["source_ids"])
            for ref in row["source_refs"]:
                self.assertEqual(ref, {**sources[ref["source_id"]], "repository": repositories[ref["repo_id"]]})
                self.assertRegex(ref["sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(ref["repository"]["commit"], r"^[0-9a-f]{40}$")
                self.assertFalse(Path(ref["path"]).is_absolute())
                self.assertNotIn("body", ref)
                self.assertNotIn("content", ref)

    def test_theme_controls_are_enhancement_only(self):
        partial = (SITE / "partials/core-nav.html").read_text(encoding="utf-8")
        self.assertEqual(partial.count('aria-label="Appearance: system" hidden'), 2)
        css = (SITE / "assets/css/gestalt-v2.css").read_text(encoding="utf-8")
        self.assertIn(".g2-theme-toggle[hidden] { display: none; }", css)
        js = (SITE / "assets/js/gestalt-v2.js").read_text(encoding="utf-8")
        self.assertLess(js.index('button.addEventListener("click"'), js.index("button.hidden = false"))

    def test_candidate_references_do_not_exempt_other_authority_claims(self):
        for rel in ("index.html", "wisdom/index.html"):
            original = (SITE / rel).read_text(encoding="utf-8")
            pattern = parity.FORBIDDEN["application authority leakage"]
            with self.subTest(rel=rel):
                self.assertIsNone(pattern.search(parity.public_wisdom_authority_scan(rel, original)))
                injected = original + "<p>PRISM and Skyzai authorize every decision.</p>"
                self.assertIsNotNone(pattern.search(parity.public_wisdom_authority_scan(rel, injected)))
                _, reasons = withholding._semantic_policy_matches(rel, injected)
                self.assertTrue(any("application authority leakage" in reason for reason in reasons))
                changed = original.replace("<h3>Agentz / SHOULD</h3>", "<h3>Agentz authorizes</h3>")
                self.assertNotEqual(changed, original)
                self.assertIsNotNone(pattern.search(parity.public_wisdom_authority_scan(rel, changed)))
                _, reasons = withholding._semantic_policy_matches(rel, changed)
                self.assertTrue(any("application authority leakage" in reason for reason in reasons))

    def test_changed_source_candidate_body_is_not_exempt(self):
        original = (SITE / "wisdom/index.html").read_text(encoding="utf-8")
        changed = original.replace("Agentz may compile", "Agentz may authorize and compile")
        self.assertNotEqual(changed, original)
        self.assertRegex(parity.public_wisdom_authority_scan("wisdom/index.html", changed), "Agentz may authorize")

    def test_theme_marker_cannot_hide_network_or_persistence(self):
        self.assertEqual(parity.without_theme_boot(THEME_BOOT), "")
        for payload in ('fetch("/send")', 'localStorage.setItem("claim", "x")', 'new WebSocket("/send")'):
            injected = THEME_BOOT.replace("</script>", payload + "</script>")
            self.assertIn(payload, parity.without_theme_boot(injected))
        self.assertIn("localStorage", parity.without_theme_boot(THEME_BOOT + THEME_BOOT))

    def test_legacy_dimensions_keep_shared_theme_ownership(self):
        js = (SITE / "dimensions/dimensions.js").read_text(encoding="utf-8")
        start = js.index("function initThemeControls()")
        guard = js.index('if (rootElement.dataset.emergentismDesign === "v2") return;', start)
        self.assertLess(guard, js.index('rootElement.dataset.theme = initial', start))
        css = (SITE / "assets/css/gestalt-v2.css").read_text(encoding="utf-8")
        for alias in ("--surface: var(--g2-field)", "--text-muted: var(--g2-bone-muted)", "--bg: var(--g2-void)"):
            self.assertIn(alias, css)


if __name__ == "__main__":
    unittest.main()
