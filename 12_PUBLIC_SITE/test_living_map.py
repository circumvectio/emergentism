#!/usr/bin/env python3
"""Invariant tests for the public Living Map routing contract."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VALID_REGISTERS = {
    "D0", "mu0", "D1", "mu1", "D2", "mu2", "D3", "mu3",
    "D4", "mu4", "D5", "b6", "D6", "r6",
}
VALID_STATUSES = {
    "ready-to-freeze", "component-contact", "formal-only", "deferred",
}


class LivingMapContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((ROOT / "living-map.json").read_text(encoding="utf-8"))
        cls.parity = json.loads((ROOT / "public_semantic_parity.json").read_text(encoding="utf-8"))

    def test_pipeline_is_monotone_and_world_contact_precedes_replication(self):
        self.assertEqual(
            self.contract["pipeline"],
            [
                "open", "proposed", "typed", "adversarially-tested",
                "testable", "world-contacted", "independently-replicated",
            ],
        )

    def test_questions_are_unique_complete_and_ordered(self):
        questions = self.contract["openQuestions"]
        self.assertEqual(len(questions), 11)
        self.assertEqual({q["id"] for q in questions}, {f"GP-{n:02d}" for n in range(1, 12)})
        self.assertEqual({q["priority"] for q in questions}, set(range(1, 12)))
        required = {
            "title", "shortTitle", "registers", "lane", "status", "tier",
            "question", "nextMilestone", "moves", "kill", "priority",
        }
        for question in questions:
            self.assertTrue(required.issubset(question), question["id"])
            self.assertTrue(set(question["registers"]).issubset(VALID_REGISTERS), question["id"])
            self.assertIn(question["status"], VALID_STATUSES)
            self.assertTrue(question["kill"].strip())

    def test_contract_cannot_become_secret_or_payment_intake(self):
        forbidden_keys = {
            "apiKey", "api_key", "secret", "token", "paymentMethod",
            "cardNumber", "privateData", "modelVerdict",
        }

        def walk(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden_keys.intersection(value))
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(self.contract)

    def test_dimension_contract_has_exact_typed_spine(self):
        self.assertEqual(
            self.parity["sequence"],
            [
                "D0", "mu0", "D1", "mu1", "D2", "mu2", "D3", "mu3",
                "D4", "mu4", "D5", "b6", "D6", "r6", "D0",
            ],
        )
        self.assertNotIn("mu5", self.parity["sequence"])
        self.assertNotIn("mu6", self.parity["sequence"])

    def test_public_routes_and_assets_exist(self):
        for relative in (
            "map/index.html", "lab/index.html", "contribute/index.html",
            "assets/css/living-map.css", "assets/js/living-map.js",
            "living-map.json", "public_semantic_parity.json",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)
        surfaces = set(self.parity["currentSurfaces"])
        self.assertTrue({"map/index.html", "lab/index.html", "contribute/index.html"}.issubset(surfaces))

    def test_contribution_copy_states_the_static_boundary(self):
        copy = (ROOT / "contribute" / "index.html").read_text(encoding="utf-8")
        for phrase in (
            "Never paste or send a personal API key.",
            "does not yet accept payments, credentials, private data, or live model jobs",
            "No payment, credential or live inference endpoint exists",
        ):
            self.assertIn(phrase, copy)


if __name__ == "__main__":
    unittest.main()
