#!/usr/bin/env python3
"""Invariant tests for the public Living Map routing contract."""

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VALID_REGISTERS = {
    "D0", "mu0", "D1", "mu1", "D2", "mu2", "D3", "mu3",
    "D4", "mu4", "D5", "b6", "D6", "r6",
}
VALID_MATURITY_STATES = {
    "typed", "packet-complete", "evidence-open", "component-supported",
    "independently-replicated", "narrowed", "killed", "deferred", "frozen",
}
VALID_EXECUTION_STATES = {
    "ready-to-freeze", "new-preregistration-required",
    "real-domain-freeze-required", "composite-test-required",
    "fair-D4-baselines-required", "independent-metric-missing",
    "row-by-row-only", "native-row-maps-missing",
    "discriminator-or-nonidentifiability-required", "runs-last",
}
VALID_PROGRAM_STATES = {"active", "queued", "deferred"}
EXPECTED_STATES = {
    "GP-03": ("packet-complete", "discriminator-or-nonidentifiability-required", "deferred"),
    "GP-04": ("packet-complete", "ready-to-freeze", "queued"),
    "GP-07": ("component-supported", "new-preregistration-required", "queued"),
    "GP-01": ("packet-complete", "real-domain-freeze-required", "queued"),
    "GP-06": ("component-supported", "composite-test-required", "queued"),
    "GP-12": ("packet-complete", "ready-to-freeze", "queued"),
    "GP-02": ("component-supported", "fair-D4-baselines-required", "queued"),
    "GP-09": ("deferred", "independent-metric-missing", "deferred"),
    "GP-05": ("packet-complete", "row-by-row-only", "queued"),
    "GP-10": ("deferred", "native-row-maps-missing", "deferred"),
    "GP-08": ("deferred", "discriminator-or-nonidentifiability-required", "deferred"),
    "GP-11": ("deferred", "runs-last", "deferred"),
}


class LivingMapContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((ROOT / "living-map.json").read_text(encoding="utf-8"))
        cls.parity = json.loads((ROOT / "public_semantic_parity.json").read_text(encoding="utf-8"))

    def test_maturity_execution_and_program_states_are_separate(self):
        self.assertEqual(self.contract["schemaVersion"], 2)
        self.assertEqual(
            self.contract["maturityStates"],
            [
                "typed", "packet-complete", "evidence-open",
                "component-supported", "independently-replicated", "narrowed",
                "killed", "deferred", "frozen",
            ],
        )
        self.assertEqual(set(self.contract["executionStates"]), VALID_EXECUTION_STATES)
        self.assertEqual(set(self.contract["programStates"]), VALID_PROGRAM_STATES)
        self.assertNotIn("status", self.contract)

    def test_questions_are_unique_complete_and_ordered(self):
        questions = self.contract["openQuestions"]
        self.assertEqual(len(questions), 12)
        self.assertEqual({q["id"] for q in questions}, {f"GP-{n:02d}" for n in range(1, 13)})
        self.assertEqual({q["priority"] for q in questions}, set(range(1, 13)))
        required = {
            "title", "shortTitle", "registers", "lane", "maturityState",
            "executionState", "programState", "tier", "question",
            "nextMilestone", "moves", "kill", "priority",
        }
        for question in questions:
            self.assertTrue(required.issubset(question), question["id"])
            self.assertTrue(set(question["registers"]).issubset(VALID_REGISTERS), question["id"])
            self.assertIn(question["maturityState"], VALID_MATURITY_STATES)
            self.assertIn(question["executionState"], VALID_EXECUTION_STATES)
            self.assertIn(question["programState"], VALID_PROGRAM_STATES)
            self.assertNotIn("status", question)
            self.assertTrue(question["kill"].strip())
            self.assertEqual(
                (question["maturityState"], question["executionState"], question["programState"]),
                EXPECTED_STATES[question["id"]],
            )

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

    def test_surface_claims_bind_current_cards_sources_and_markers(self):
        expected = {
            "index.html": {"FIN01-01", "OS01-13", "OS01-20", "OS01-22", "OS01-26"},
            "practice/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22"},
            "lab/index.html": {"FIN01-01", "FIN01-02"},
            "manifesto/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22"},
        }
        bindings = {item["surface"]: item for item in self.parity["surfaceClaims"]}
        self.assertEqual(set(bindings), set(expected))
        for surface, card_ids in expected.items():
            binding = bindings[surface]
            self.assertEqual(set(binding["claimCardIds"]), card_ids)
            self.assertEqual(len(binding["claimCardIds"]), len(card_ids))
            source_bound_cards = set()
            for source_binding in binding["claimSources"]:
                source = ROOT.parent / source_binding["source"]
                revision = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
                self.assertEqual(source_binding["sourceRevision"], revision)
                self.assertIn(source_binding["lifecycle"], {"active", "reader_synthesis"})
                source_bound_cards.update(source_binding["claimCardIds"])
            self.assertEqual(source_bound_cards, card_ids)
            self.assertEqual(binding["publicDisposition"], "bounded_current")
            page = (ROOT / surface).read_text(encoding="utf-8")
            for marker in binding["requiredMarkers"]:
                self.assertIn(marker, page)

    def test_current_atlas_excludes_frozen_and_withheld_routes(self):
        atlas = json.loads((ROOT / "atlas" / "site_index.json").read_text(encoding="utf-8"))
        withheld = json.loads((ROOT / "withheld-routes.json").read_text(encoding="utf-8"))
        hrefs = {
            page["href"]
            for section in atlas["tree"]
            for page in section["pages"]
        }
        self.assertEqual(atlas["schemaVersion"], 2)
        self.assertEqual(atlas["status"], "current-cleared-surfaces-only")
        self.assertIn("/read/", hrefs)
        for frozen in self.parity["frozenLibraryRoots"]:
            self.assertFalse(any(href == f"/{frozen}/" or href.startswith(f"/{frozen}/") for href in hrefs))
        for item in withheld["artifacts"]:
            self.assertTrue(set(item["publicRoutes"]).isdisjoint(hrefs))

    def test_pwa_identity_and_precache_are_current_only(self):
        manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
        sw = (ROOT / "sw.js").read_text(encoding="utf-8")
        offline = (ROOT / "offline" / "index.html").read_text(encoding="utf-8")
        withheld = json.loads((ROOT / "withheld-routes.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "Emergentism — A Worldview for Finite Beings")
        self.assertEqual(manifest["id"], "/")
        self.assertEqual(manifest["start_url"], "/")
        self.assertNotIn("A Compass, Not a Cathedral", manifest["name"])
        self.assertNotIn("/compass/", sw)
        self.assertNotIn("/compass/", offline)
        spine_match = re.search(r"const SPINE = (\[.*?\]);", sw, flags=re.DOTALL)
        self.assertIsNotNone(spine_match)
        precached_routes = set(json.loads(spine_match.group(1)))
        self.assertNotIn("/read/", precached_routes)
        self.assertIn("WITHHELD_ROUTES", sw)
        self.assertIn("isWithheldRoute", sw)
        self.assertIn("isStorable", sw)
        for frozen in self.parity["frozenLibraryRoots"]:
            self.assertFalse(any(route.startswith(f"/{frozen}/") for route in precached_routes))
        for item in withheld["artifacts"]:
            self.assertTrue(set(item["publicRoutes"]).isdisjoint(precached_routes))

    def test_contribution_copy_states_the_static_boundary(self):
        copy = (ROOT / "contribute" / "index.html").read_text(encoding="utf-8")
        for phrase in (
            "Never paste or send a personal API key.",
            "does not accept payments, credentials, private data, or live model jobs",
            "No payment, credential or live inference endpoint exists",
        ):
            self.assertIn(phrase, copy)


if __name__ == "__main__":
    unittest.main()
