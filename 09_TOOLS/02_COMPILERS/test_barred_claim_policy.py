from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "09_TOOLS/01_SCRIPTS/claim_policy.py"
SPEC = importlib.util.spec_from_file_location("claim_policy", MODULE_PATH)
assert SPEC and SPEC.loader
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


class BarredClaimPolicyTests(unittest.TestCase):
    def test_positive_scope_inflations_fail(self) -> None:
        titan_infix = "".join(("⊙", " = ", "•", " × ", "○"))
        samples = (
            "Emergentism provides a complete ontology.",
            "Finity resolves all paradoxes.",
            "This system unifies all sciences.",
            "War is always a war between egregores.",
            "Philosopher-kings should rule everyone else.",
            titan_infix,
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertTrue(POLICY.violations(sample))

    def test_scoped_denials_pass(self) -> None:
        titan_infix = "".join(("⊙", " = ", "•", " × ", "○"))
        samples = (
            "Emergentism does not provide a complete ontology.",
            "Finity does not resolve all paradoxes.",
            "No current result unifies all sciences.",
            "War is not always a war between egregores.",
            f"The notation never licenses {titan_infix}.",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertEqual(POLICY.violations(sample), [])

    def test_line_wrapping_does_not_break_a_scoped_denial(self) -> None:
        sample = (
            "This route is not being presented as established mathematics,\n"
            "physics, medicine, or a complete account of reality."
        )
        self.assertEqual(POLICY.violations(sample), [])

    def test_negation_cannot_launder_a_later_sentence(self) -> None:
        samples = (
            "Emergentism is not a religion. Finity resolves all paradoxes.",
            "Emergentism does not provide a complete ontology. It provides a complete ontology.",
            "Finity does not resolve all paradoxes. Finity resolves all paradoxes.",
            "Emergentism does not provide a complete ontology.\n\nIt provides a complete ontology.",
            "<p>Emergentism does not provide a complete ontology.</p><p>It provides a complete ontology.</p>",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertTrue(POLICY.violations(sample))

    def test_v22_overclaims_fail(self) -> None:
        samples = (
            "Emergentism resolves most philosophical questions.",
            "Emergentism proves objective ethics.",
            "RCAB-01 closes the is-ought gap.",
            "Potential is the Good.",
            "Co-agency creates shared consent.",
            "A guardian overrides the bearer.",
            "Protection authorizes coercion.",
            "Guardianship is co-agency.",
            "An AI guardian may sign.",
            "Cross-agent agreement validates Emergentism.",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertTrue(POLICY.violations(sample))

    def test_actual_current_and_provisional_surfaces_pass(self) -> None:
        import json
        import sys
        scripts = str(ROOT / "09_TOOLS/01_SCRIPTS")
        sys.path.insert(0, scripts)
        try:
            checker_path = ROOT / "09_TOOLS/01_SCRIPTS/check_barred_claims.py"
            spec = importlib.util.spec_from_file_location("check_barred_claims", checker_path)
            assert spec and spec.loader
            checker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(checker)
            manifest = json.loads(checker.PUBLIC_MANIFEST.read_text(encoding="utf-8"))
            scanned = {path.relative_to(ROOT / "12_PUBLIC_SITE").as_posix() for path in checker._public_paths()}
            self.assertTrue(
                set(manifest["declaredProvisional"]["routes"]) <= scanned
            )
            deployable_html = {
                path.relative_to(ROOT / "12_PUBLIC_SITE").as_posix()
                for path in checker._deployable_public_html_paths()
            }
            self.assertTrue(deployable_html <= scanned)
            self.assertEqual(checker.check("all"), [])
        finally:
            sys.path.remove(scripts)


if __name__ == "__main__":
    unittest.main()
