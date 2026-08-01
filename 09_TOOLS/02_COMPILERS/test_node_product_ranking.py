#!/usr/bin/env python3
"""Negative controls for the KSC-02 node-product regression gate."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "09_TOOLS/01_SCRIPTS"
CHECKER = SCRIPTS / "check_node_product_ranking.py"

sys.path.insert(0, str(SCRIPTS))
try:
    spec = importlib.util.spec_from_file_location("check_node_product_ranking", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
finally:
    sys.path.pop(0)


class NodeProductRankingTests(unittest.TestCase):
    def assert_barred(self, text: str) -> None:
        self.assertTrue(module.violations_in_text(text), text)

    def assert_allowed(self, text: str) -> None:
        self.assertEqual(module.violations_in_text(text), [], text)

    def test_current_product_rankings_fail(self) -> None:
        barred = (
            "Emergentism selects P_node = Φ × V as its working score.",
            "The current node score is Φ̂₄V₄.",
            "Rank nodes by ΦV.",
            "Maximize φ × ν across candidates.",
            "P = Phi * V is the default objective.",
            "P_node=ΦV is selected but not uniquely derived.",
            "Compare the selected node product with other aggregators.",
        )
        for text in barred:
            with self.subTest(text=text):
                self.assert_barred(text)

    def test_adjacent_unrelated_qualifier_does_not_shield_assertion(self) -> None:
        bypasses = (
            "The historical product is retired.\nP_node = Φ × V is the current score.",
            "A separately cardinal candidate was tested.\nRank nodes by ΦV.",
            "The old formula does not rank nodes.\nP = Phi * V is the default objective.",
        )
        for text in bypasses:
            with self.subTest(text=text):
                self.assert_barred(text)

    def test_explicit_history_candidates_and_denials_pass(self) -> None:
        allowed = (
            "The historical product Φ×V is retired as a node ranking.",
            "Compare C×=Φ̂₄V₄ only as a separately cardinal candidate.",
            "No physical force follows from Φ×V.",
            "The current score is min(Φ̂₄,V₄); the old product ΦV is retired.",
            "The analytic identity φν=1 ranks nothing and is not a node score.",
            "The preregistered experimental product candidate is P = Phi * V.",
            "The historical selected node product is retired as a ranking.",
        )
        for text in allowed:
            with self.subTest(text=text):
                self.assert_allowed(text)

    def test_scope_matches_active_corpus_contract(self) -> None:
        active = ROOT / "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md"
        excluded = (
            ROOT / "05_COSMOLOGY/90_ARCHIVE/example.md",
            ROOT / "91_COMPATIBILITY/example.md",
            ROOT / "12_PUBLIC_SITE/example.md",
            ROOT / "00_HANDOFF/example.md",
            ROOT / "11_UPLINK/50_AUDITS_AND_EXECUTIONS/example.md",
            ROOT / "11_UPLINK/60_SESSION_PACKETS/example.md",
            ROOT / "00_META/registers/example.json",
        )
        managed_projection = (
            ROOT / "08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/README.md"
        )
        self.assertTrue(module.is_node_ranking_scoped(active))
        self.assertTrue(module.is_node_ranking_scoped(managed_projection))
        for path in excluded:
            with self.subTest(path=path):
                self.assertFalse(module.is_node_ranking_scoped(path))

    def test_fixture_is_the_only_file_exclusion(self) -> None:
        self.assertEqual(
            module.FIXTURE_EXCLUSION,
            Path("09_TOOLS/02_COMPILERS/test_node_product_ranking.py"),
        )
        self.assertNotIn(ROOT / module.FIXTURE_EXCLUSION, module.active_paths())

    def test_live_active_corpus_has_no_violation(self) -> None:
        errors, count = module.check_active_corpus()
        self.assertGreater(count, 0)
        self.assertEqual(errors, [], "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
