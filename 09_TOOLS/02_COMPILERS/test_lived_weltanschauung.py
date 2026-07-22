#!/usr/bin/env python3
"""Semantic contract tests for the lived Emergentist Weltanschauung."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "00_THE_WELTANSCHAUUNG_ONE_SITTING.md"
HUMAN = ROOT / "06_ONTOLOGY/08_THE_HUMAN_CONDITION.md"
COMPASS = ROOT / "01_TELEOLOGY/04_THE_LIVED_COMPASS.md"
GOAL = ROOT / "01_TELEOLOGY/00_THE_GOAL.md"
F5 = (
    ROOT
    / "05_COSMOLOGY/02_EMERGENTISM_CORE"
    / "01_TELEOLOGICAL_FORCE_AND_F5_DYNAMICS.md"
)


class LivedWeltanschauungTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = BOOK.read_text(encoding="utf-8")
        cls.human = HUMAN.read_text(encoding="utf-8")
        cls.compass = COMPASS.read_text(encoding="utf-8")
        cls.goal = GOAL.read_text(encoding="utf-8")
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
            "They are the **Titans**: not gods, particles, causal agents or arithmetic",
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
        self.assertIn("why and how physical organization is accompanied", self.human)
        self.assertIn("remains open", self.human)
        self.assertIn("A trace is not automatically\nthe bearer", self.human)
        self.assertIn("makes no canonical claim that D6 is an afterlife", self.human)

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
        self.assertIn("coherent declaration of ignorance", completion)


if __name__ == "__main__":
    unittest.main()
