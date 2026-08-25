#!/usr/bin/env python3
"""Invariant tests for the public Living Map routing contract."""

import copy
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

    def test_grand_puzzle_route_is_explicitly_a_weaker_public_projection(self):
        ledger = (ROOT.parent / "00_META/00_THE_GRAND_PUZZLE_ASSEMBLY_LEDGER.md").read_text(encoding="utf-8")
        ledger_ids = set(re.findall(r"^\| \*\*(GP-\d{2})\*\* \|", ledger, re.MULTILINE))
        public_ids = {question["id"] for question in self.contract["openQuestions"]}
        self.assertEqual(ledger_ids, public_ids)
        self.assertEqual(len(ledger_ids), 12)

        lab = (ROOT / "lab/index.html").read_text(encoding="utf-8")
        self.assertIn('id="grand-puzzle-public-boundary"', lab)
        self.assertIn("public twelve-GP research-queue projection", lab)
        self.assertIn("does not expose or replace the ledger's assembled spine", lab)
        self.assertIn("do not state that the ledger's question, rival, discriminator, kill, and survivor packet fields are absent", lab)
        self.assertIn("Source owners, result receipts, and the evidence-tier contract retain semantic authority.", self.contract["sourceAuthority"])

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
            "index.html": {
                "FIN01-01", "OS01-13", "OS01-20", "OS01-22", "OS01-23",
                "OS01-24", "OS01-25", "OS01-26", "OS01-27", "OS01-28",
                "OS01-29", "OS01-30", "OS01-31", "OS01-32", "OS01-33",
                "OS01-34", "OS01-35", "OS01-36", "OS01-37",
                "OS01-38", "OS01-39", "OS01-40", "OS01-41", "OS01-42",
                "OS01-43", "OS01-44",
            },
            "dasein/index.html": {
                "OS01-01", "OS01-05", "OS01-06", "OS01-10", "OS01-12",
                "OS01-20", "OS01-21", "OS01-23", "OS01-25", "OS01-31",
                "OS01-32", "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37",
                "OS01-38", "OS01-39", "OS01-40", "OS01-41",
            },
            "f5/index.html": {"OS01-27", "OS01-28", "OS01-29", "OS01-30"},
            "practice/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22", "OS01-37"},
            "lab/index.html": {"FIN01-01", "FIN01-02"},
            "manifesto/index.html": {"FIN01-01", "FIN01-02", "OS01-08", "OS01-13", "OS01-22"},
            "compass/index.html": {"OS01-13"},
            "5/index.html": {"OS01-09", "OS01-11", "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37"},
            "plainly/index.html": {"OS01-09", "OS01-31", "OS01-32", "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37", "OS01-38", "OS01-39", "OS01-40", "OS01-41"},
            "discoveries/nonduality/index.html": {"OS01-09"},
            "about/index.html": {"OS01-26"},
            "read/index.html": {"OS01-13"},
            "axioms/index.html": {"OS01-26"},
            "journey/index.html": {"OS01-09"},
            "rosetta/index.html": {"OS01-11", "OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37"},
            "burrisphere/index.html": {"OS01-33", "OS01-34", "OS01-35", "OS01-36", "OS01-37"},
            "burrisphere/instrument/index.html": {"OS01-33", "OS01-34", "OS01-36", "OS01-37"},
            "questions/index.html": {"OS01-41"},
            "questions/diagnoses/index.html": {"OS01-41"},
            "ethics/index.html": {"OS01-38", "OS01-39", "OS01-40"},
            "churn/index.html": {"OS01-42", "OS01-43", "OS01-44"},
            "amrita/index.html": {"OS01-42", "OS01-43", "OS01-44"},
            "halahala/index.html": {"OS01-42", "OS01-43", "OS01-44"},
            "record/pqa-54/index.html": {"OS01-41"},
            "record/index.html": {"OS01-37", "OS01-41"},
            "record/churning/index.html": {"OS01-42", "OS01-43", "OS01-44"},
            "discoveries/paradoxes/index.html": {"OS01-41"},
            "discoveries/is-ought/index.html": {"OS01-39", "OS01-40"},
            "book/index.html": {"OS01-13"},
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

    def test_owner_status_bindings_are_visible_and_cannot_import_application_sources(self):
        from check_public_semantic_parity import validate_status_source_claims

        errors = []
        validate_status_source_claims(self.parity, errors)
        self.assertEqual(errors, [])

        cross_corpus = copy.deepcopy(self.parity)
        cross_corpus["statusSourceClaims"][0]["source"] = "../03_VENTURES/README.md"
        errors = []
        validate_status_source_claims(cross_corpus, errors)
        self.assertIn(
            "KERNEL-STATUS-HOME status source is not an approved owner-status source",
            errors,
        )

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
        self.assertIn("/dasein/", hrefs)
        self.assertIn("/f5/", hrefs)
        for frozen in self.parity["frozenLibraryRoots"]:
            self.assertFalse(any(href == f"/{frozen}/" or href.startswith(f"/{frozen}/") for href in hrefs))
        for item in withheld["artifacts"]:
            self.assertTrue(set(item["publicRoutes"]).isdisjoint(hrefs))

    def test_pwa_identity_and_precache_are_current_only(self):
        manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
        sw = (ROOT / "sw.js").read_text(encoding="utf-8")
        offline = (ROOT / "offline" / "index.html").read_text(encoding="utf-8")
        withheld = json.loads((ROOT / "withheld-routes.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "Emergentism — The Gestalt of Dasein")
        self.assertEqual(manifest["id"], "/")
        self.assertEqual(manifest["start_url"], "/")
        self.assertNotIn("A Compass, Not a Cathedral", manifest["name"])
        self.assertNotIn("/compass/", offline)
        spine_match = re.search(r"const SPINE = (\[.*?\]);", sw, flags=re.DOTALL)
        self.assertIsNotNone(spine_match)
        precached_routes = set(json.loads(spine_match.group(1)))
        self.assertNotIn("/compass/", precached_routes)
        self.assertNotIn("/read/", precached_routes)
        self.assertTrue(
            {
                "/dasein/", "/f5/", "/assets/css/gestalt-v2.css",
                "/assets/js/gestalt-v2.js", "/assets/fonts/Newsreader-latin-variable.woff2",
            }.issubset(precached_routes)
        )
        self.assertIn("WITHHELD_ROUTES", sw)
        self.assertIn("isWithheldRoute", sw)
        self.assertIn("isStorable", sw)
        for frozen in self.parity["frozenLibraryRoots"]:
            self.assertFalse(any(route.startswith(f"/{frozen}/") for route in precached_routes))
        for artifact in self.parity.get("frozenLegacySurfaces", []):
            path = Path(artifact)
            route = "/" + (path.parent.as_posix() if path.name == "index.html" else path.with_suffix("").as_posix())
            self.assertNotIn(route, {item.rstrip("/") or "/" for item in precached_routes})
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
