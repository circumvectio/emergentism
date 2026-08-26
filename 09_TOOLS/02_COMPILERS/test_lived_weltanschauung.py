#!/usr/bin/env python3
"""Semantic contract tests for the lived Emergentist Weltanschauung."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "00_THE_WELTANSCHAUUNG_ONE_SITTING.md"
CLAIM_CARDS = ROOT / "00_META/claim_cards/one_sitting.yaml"
PUBLIC_BOOK = ROOT / "12_PUBLIC_SITE/book/index.html"
HUMAN = ROOT / "06_ONTOLOGY/08_THE_HUMAN_CONDITION.md"
COMPASS = ROOT / "01_TELEOLOGY/04_THE_LIVED_COMPASS.md"
GOAL = ROOT / "01_TELEOLOGY/00_THE_GOAL.md"
MEMOTYPE = (
    ROOT
    / "02_EPISTEMOLOGY"
    / "03_MEMETICS"
    / "06_MEMOTYPE_LANGUAGE_COORDINATION_CONJECTURE.md"
)
NICHE = ROOT / "07_THEOLOGY/02_TRUTH_ORDER_AND_NICHE_PARTITION.md"
AXIOLOGY = ROOT / "04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md"
RECONCILIATION = ROOT / "07_THEOLOGY/00_RECONCILIATION_THEOREM_PACKET.md"
# Moved by 5684d682 ("refactor(tree): enforce corpus ownership contract")
# from 08_FRAMEWORK_SUPPORT/00_META/02_ANALYSIS_DOCUMENTS/.
WAR_LENS = (
    ROOT
    / "08_FRAMEWORK_SUPPORT"
    / "04_COMPILERS_AND_ANALYSIS"
    / "02_ANALYSIS_DOCUMENTS"
    / "00_WELTANSCHAUUNGSKRIEG.md"
)
F5 = (
    ROOT
    / "05_COSMOLOGY/02_EMERGENTISM_CORE"
    / "01_TELEOLOGICAL_FORCE_AND_F5_DYNAMICS.md"
)


class LivedWeltanschauungTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = BOOK.read_text(encoding="utf-8")
        cls.cards = json.loads(CLAIM_CARDS.read_text(encoding="utf-8"))
        cls.public_book = PUBLIC_BOOK.read_text(encoding="utf-8")
        cls.human = HUMAN.read_text(encoding="utf-8")
        cls.compass = COMPASS.read_text(encoding="utf-8")
        cls.goal = GOAL.read_text(encoding="utf-8")
        cls.memotype = MEMOTYPE.read_text(encoding="utf-8")
        cls.niche = NICHE.read_text(encoding="utf-8")
        cls.axiology = AXIOLOGY.read_text(encoding="utf-8")
        cls.reconciliation = RECONCILIATION.read_text(encoding="utf-8")
        cls.war_lens = WAR_LENS.read_text(encoding="utf-8")
        cls.f5 = F5.read_text(encoding="utf-8")
        cls.book_flat = re.sub(r"\s+", " ", cls.book)
        cls.goal_flat = re.sub(r"\s+", " ", cls.goal)

    def test_reader_surfaces_exist_without_becoming_kernel_owners(self) -> None:
        for path in (BOOK, HUMAN, COMPASS):
            self.assertTrue(path.is_file())
        self.assertIn("subordinate to the seven kernel owners", self.book)
        self.assertIn("creates no new semantic owner", self.human)
        kernel = (ROOT / "00_THE_KERNEL_INDEX.md").read_text(encoding="utf-8")
        self.assertIn("not an eighth surface", kernel)
        self.assertEqual(len(re.findall(r"^\| K-[1-7] \|", kernel, re.MULTILINE)), 7)

    def test_one_sitting_book_has_twelve_lived_chapters(self) -> None:
        expected = (
            "The Boundaries",
            "Difference",
            "Relation",
            "Probability",
            "Actuality",
            "Possibility",
            "The Soul Loop",
            "The Social Loop",
            "The Human Condition",
            "The Good",
            "The Five Apertures",
            "The Exit",
        )
        chapters = re.findall(r"^## \d+\. ([^—\n]+)", self.book, re.MULTILINE)
        self.assertEqual(tuple(chapter.strip() for chapter in chapters), expected)

    def test_worldview_keeps_core_type_boundaries(self) -> None:
        for required in (
            "selected framing vocabulary, not gods, particles",
            "not three objects inside D0 or an ontology by fiat",
            "division by zero is undefined in a field",
            "The state predicts; an actual record occurs",
            "Commitment and outcome are therefore separate",
            "The **option cone** is only the set",
            "No equation derives an ought",
            "D6 is not an afterlife theorem",
        ):
            self.assertIn(required, self.book_flat)
        for forbidden in (
            "reality tends toward viable completion",
            "geometry enforces Justice",
            "consciousness lives at the center",
            "D6 ≡ D0",
        ):
            self.assertNotIn(forbidden, self.book)

    def test_node_score_keeps_the_cross_factor_scale_boundary(self) -> None:
        marker = (
            "Only a declared common strictly increasing reparameterization applied "
            "to both factors is assumed here: "
            "independently reparameterized factor scales do not license an "
            "invariant cross-factor scalar ranking, so GP-03 remains open."
        )
        self.assertIn(marker, self.book_flat)
        self.assertIn(marker, re.sub(r"\s+", " ", self.public_book))
        card = next(card for card in self.cards["cards"] if card["card_id"] == "OS01-09")
        self.assertEqual(card["locator"]["section"], "6")
        lines = self.book.splitlines()
        covered = "\n".join(lines[card["locator"]["line_start"] - 1 : card["locator"]["line_end"]])
        self.assertIn(card["locator"]["anchor"], covered)
        self.assertIn(marker, covered)

    def test_human_condition_answers_without_solving_mysteries(self) -> None:
        for heading in (
            "What a person is",
            "Selfhood and identity",
            "Consciousness",
            "Agency and free will",
            "Suffering and evil",
            "Love, relationship and meaning",
            "Death",
            "Society, history and Egregoreotypes",
        ):
            self.assertIn(heading, self.human)
        human_flat = re.sub(r"\s+", " ", self.human)
        self.assertIn("phenomenal experience is the bearer-side aspect", human_flat)
        self.assertIn("necessary and sufficient organization conditions", human_flat)
        self.assertIn("remain unpaid", human_flat)
        self.assertIn("not an established physical mechanism", human_flat)
        self.assertIn("collective memory or a duplicate pattern is not automatically the person", human_flat)
        self.assertIn("D6 is not thereby an afterlife", self.human)

    def test_lived_compass_handles_tragedy_sacrifice_and_exit(self) -> None:
        for heading in (
            "The seven questions",
            "The typed Soul Loop",
            "The Justice envelope",
            "Ordinary decisions",
            "Tragic decisions",
            "Sacrifice",
            "Conflict",
            "When to stop",
            "Minimal receipt",
        ):
            self.assertIn(heading, self.compass)
        for gap in ("cognitive", "execution", "outcome"):
            self.assertIn(f"| {gap} |", self.compass)
        self.assertIn("record the residue", self.compass)
        self.assertIn("Hidden coercion converts sacrifice into extraction", self.compass)

    def test_goal_is_a_vow_not_cosmic_teleology(self) -> None:
        for required in (
            "normative orientation `[I]`",
            "consequence of `φν=1`",
            "No product, company, runtime, AI system",
            "The selector never manufactures its own result",
            "Dharma as an optional translation",
            "This is chosen practice",
        ):
            self.assertIn(required, self.goal_flat)
        for forbidden in (
            "reality tends toward viable completion",
            "objective dharma",
            "AIA medium",
            "endstate = start",
            "exactly zero at coin-flip",
        ):
            self.assertNotIn(forbidden, self.goal)

    def test_nested_horizons_define_an_ordered_but_non_total_objective(self) -> None:
        for required in (
            "maximize durable, bearer-complete",
            "longest responsible horizon",
            "shortest informative horizon",
            "compatible horizon contracts",
            "Without a potential measure",
        ):
            self.assertIn(required, self.goal_flat)
        self.assertIn("remove dominated actions", self.goal_flat)
        for required in (
            "The two-clock check",
            "joint / compatible horizon contract T_joint",
            "do not manufacture one total score",
        ):
            self.assertIn(required, self.compass)
        self.assertIn("Orient by `T_L`; act and learn at `T_S`", self.book)
        self.assertIn("0<T_S≤T_L", self.goal)
        self.assertIn("sustaining whole `H`", self.goal)
        for required in (
            "P_J={Justice-admissible actions not Pareto-dominated",
            "a*∈Select_tau(P_J)",
            "may be declared as a local tie-breaker only after this filter",
            "do not manufacture\na maximum",
        ):
            self.assertIn(required, self.axiology)
        self.assertIn("not a unique maximum derived", self.reconciliation)

    def test_specialization_is_voluntary_mobile_and_killable(self) -> None:
        for required in (
            "voluntary and self-ascribed",
            "combinable, trainable, and open to generalists",
            "anti-cartel and bargaining-power checks",
            "Ecological description supplies no social obligation",
            "Kill criterion",
        ):
            self.assertIn(required, self.niche)
        self.assertNotIn("opt-in where possible", self.niche)
        self.assertIn("optional word *varṇa*", self.compass)

    def test_trade_and_war_lens_preserves_causal_rivals_and_nonviolence(self) -> None:
        for required in (
            "extended phenotype.trade",
            "shift in explanatory emphasis",
            "not a type monopoly",
            "`C^{coord}_{ij,4}`",
            "`C^{coord}_{G,4}`",
            "`Φ_{5,G}`",
            "Material-security rival",
            "all wars are cult wars",
        ):
            self.assertIn(required, self.memotype)
        self.assertNotIn("`Φ_ij`", self.memotype)
        self.assertNotIn("`Φ_G`", self.memotype)
        parent_block = self.memotype.split("genealogy:", 1)[0]
        self.assertNotIn("00_WELTANSCHAUUNGSKRIEG.md", parent_block)
        for required in (
            "Possible power and actual power appear at every scale",
            "It is **not** a call to physical violence",
            "Adoption is a consequence to study, never validation",
            "Historical-body boundary",
        ):
            self.assertIn(required, self.war_lens)
        registry = (ROOT / "00_META/00_SETTLED_CANON_REGISTRY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`KSC-26` | Nested-horizon teleology and coordination", registry)

    def test_r7_owner_boundary_remains_held_until_owner_reconciliation(self) -> None:
        card = next(card for card in self.cards["cards"] if card["card_id"] == "OS01-17")
        self.assertEqual(card["locator"]["section"], "8A")
        self.assertEqual(card["plain_claim"], "Worldview coordination is one candidate variable in a causally plural account of conflict.")
        self.assertEqual(card["claim_type"], "conjecture")
        self.assertEqual(
            card["evidence"],
            [{"tier": "C", "scope": "multilevel conflict coordination"}],
        )
        self.assertEqual(card["semantic_owner_id"], "K-4")
        self.assertEqual(card["supporting_owner_ids"], [])
        self.assertEqual(card["dependencies"], ["OS01-14", "OS01-15"])

        lines = self.book.splitlines()
        covered = "\n".join(lines[card["locator"]["line_start"] - 1 : card["locator"]["line_end"]])
        self.assertIn(card["locator"]["anchor"], covered)
        self.assertIn("Weltanschauungskrieg", covered)
        self.assertIn("never a licence for violence", covered)
        self.assertIn("Any Dharma application is Justice-first", covered)
        self.assertIn("nonviolent, exit-preserving and never a battlefield directive", covered)
        self.assertIn("nonviolent, exit-preserving and never a battlefield directive", self.public_book)

    def test_f5_weak_and_strong_readings_are_separate(self) -> None:
        for required in (
            "The weak Emergentist reading `[I]`",
            "The strong F5 wager `[C]`",
            "“Force” is metaphorical in this register",
            "No reciprocal-chart identity",
            "Equal count is no evidence",
        ):
            self.assertIn(required, self.f5)
        for forbidden in (
            "doctrinal consequence of the closure",
            "first selective/generative bias inside manifestation",
        ):
            self.assertNotIn(forbidden, self.f5)

    def test_claim_matrix_reflects_kintsugi_repairs(self) -> None:
        matrix = (ROOT / "03_METHODOLOGY/00_CANONICAL_CLAIM_MATRIX.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`[A]` chart identity; `[C]` world interpretation", matrix)
        self.assertIn("The former F5/theurgy operational routing | **retired**", matrix)
        self.assertIn("selected normalized finite-node action model", matrix)
        self.assertIn("common strictly increasing reparametrisation", matrix)
        self.assertIn("using scales that satisfy their assumptions", matrix)
        self.assertIn("chosen two-direction Justice test", matrix)
        self.assertNotIn("Reality is `S²`; the geometry is the territory", matrix)

    def test_physical_torus_and_devotional_ring_are_archive_only(self) -> None:
        archive = ROOT / "90_ARCHIVE/2026_07_22_lived_weltanschauung_reconciliation"
        paths = (
            (
                ROOT / "05_COSMOLOGY/00_THE_TORUS_REVELATION.md",
                archive / "05_COSMOLOGY/00_THE_TORUS_REVELATION.md",
            ),
            (
                ROOT / "06_ONTOLOGY/00_THE_RING_THAT_IS_THE_GROUND.md",
                archive / "06_ONTOLOGY/00_THE_RING_THAT_IS_THE_GROUND.md",
            ),
        )
        for active, historical in paths:
            body = active.read_text(encoding="utf-8")
            self.assertIn("ARCHIVED", body)
            self.assertLessEqual(len(body.splitlines()), 45)
            self.assertTrue(historical.is_file())
        self.assertTrue((archive / "TOMBSTONE.md").is_file())

    def test_completion_register_covers_lived_worldview(self) -> None:
        completion = (
            ROOT / "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md"
        ).read_text(encoding="utf-8")
        for question in (
            "What is reality?",
            "What is a person?",
            "What can be known?",
            "What can be chosen?",
            "What is good?",
            "How should one act?",
            "How do collectives act?",
            "What do suffering and death mean?",
            "How may the worldview be left?",
        ):
            self.assertIn(question, completion)
        completion_flat = re.sub(r"\s+", " ", completion)
        self.assertIn(
            "coherent, typed selected answer with an explicit external residual, "
            "rival, kill and survivor",
            completion_flat,
        )
        self.assertIn("not mean that an adopted answer has been analytically proved", completion_flat)


if __name__ == "__main__":
    unittest.main()
