#!/usr/bin/env python3
"""Contracts for the staged, projection-only Emergentist manifesto."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "13_BOOKS/manifesto/manifesto-contract.json"
DRAFT = ROOT / "13_BOOKS/manifesto/MANIFESTO_DRAFT_0.md"
BOOK_MANIFEST = ROOT / "13_BOOKS/book-manifest.json"
CARD_DIR = ROOT / "00_META/claim_cards"


def load_card_data() -> tuple[dict[str, dict], dict[str, str], dict[str, dict]]:
    cards: dict[str, dict] = {}
    card_work_ids: dict[str, str] = {}
    card_sets: dict[str, dict] = {}
    for path in sorted(CARD_DIR.glob("*.yaml")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        work_id = payload["work_id"]
        card_sets[work_id] = payload["source"]
        for card in payload["cards"]:
            cards[card["card_id"]] = card
            card_work_ids[card["card_id"]] = work_id
    return cards, card_work_ids, card_sets


class ManifestoProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.draft = DRAFT.read_text(encoding="utf-8")
        # Markdown line wrapping is editorial, not semantic.  Contract phrases
        # must survive a reflow of the staged reader manuscript.
        cls.flat_draft = " ".join(cls.draft.split())
        cls.cards, cls.card_work_ids, cls.card_sets = load_card_data()
        cls.book_manifest = json.loads(BOOK_MANIFEST.read_text(encoding="utf-8"))
        cls.manifest_works = {
            work["work_id"]: work for work in cls.book_manifest["works"]
        }
        cls.works = set(cls.manifest_works)

    def test_manifesto_is_a_staged_projection_not_a_semantic_owner(self) -> None:
        self.assertEqual(self.contract["schema"], "emergentism/manifesto-projection/v1")
        self.assertEqual(self.contract["status"], "staged_editorial_draft_not_public")
        self.assertEqual(self.contract["authority"], "projection_only_no_semantic_authority")
        self.assertEqual(self.contract["public_disposition"], "not_a_public_route")
        self.assertIn("not a new source of doctrine", self.flat_draft)
        self.assertIn("K-1 through K-7 retain semantic ownership", self.draft)

    def test_body_uses_only_currently_bounded_cards(self) -> None:
        body_ids = self.contract["body_claim_card_ids"]
        self.assertEqual(len(body_ids), len(set(body_ids)))
        for card_id in body_ids:
            with self.subTest(card_id=card_id):
                card = self.cards[card_id]
                self.assertEqual(card["public"]["state"], "bounded_current")

    def test_section_cards_are_known_and_are_part_of_the_body_contract(self) -> None:
        body_ids = set(self.contract["body_claim_card_ids"])
        for section in self.contract["sections"]:
            self.assertTrue(section["claim_card_ids"], section["id"])
            for card_id in section["claim_card_ids"]:
                with self.subTest(section=section["id"], card_id=card_id):
                    self.assertIn(card_id, self.cards)
                    self.assertIn(card_id, body_ids)

    def test_body_sources_are_pinned_to_the_current_card_revisions(self) -> None:
        revisions = {entry["work_id"]: entry for entry in self.contract["source_revisions"]}
        body_work_ids = {
            self.card_work_ids[card_id]
            for card_id in self.contract["body_claim_card_ids"]
        }
        self.assertEqual(set(revisions), body_work_ids)
        for work_id in body_work_ids:
            with self.subTest(work_id=work_id):
                self.assertEqual(
                    revisions[work_id]["source_path"],
                    self.card_sets[work_id]["path"],
                )
                self.assertEqual(
                    revisions[work_id]["reviewed_source_sha256"],
                    self.card_sets[work_id]["reviewed_source_sha256"],
                )

    def test_every_marked_paragraph_has_the_declared_boundary_and_source_map(self) -> None:
        markers = re.findall(r"<!-- MANIFESTO-P: ([a-z0-9_]+) -->", self.draft)
        self.assertEqual(len(markers), len(set(markers)))
        paragraphs = {entry["id"]: entry for entry in self.contract["paragraphs"]}
        self.assertEqual(set(markers), set(paragraphs))

        revisions = {entry["work_id"] for entry in self.contract["source_revisions"]}
        body_ids = set(self.contract["body_claim_card_ids"])
        lines = self.draft.splitlines()
        for marker_id, paragraph in paragraphs.items():
            with self.subTest(paragraph=marker_id):
                start, end = paragraph["line_range"]
                self.assertGreaterEqual(start, 1)
                self.assertLessEqual(start, end)
                self.assertLessEqual(end, len(lines))
                rendered_range = " ".join("\n".join(lines[start - 1 : end]).split())
                self.assertIn(" ".join(paragraph["anchor"].split()), rendered_range)
                self.assertTrue(
                    set(paragraph["source_revision_work_ids"]).issubset(self.works)
                )
                for card_id in paragraph["claim_card_ids"]:
                    self.assertIn(card_id, self.cards)
                derived_work_ids = {
                    self.card_work_ids[card_id]
                    for card_id in paragraph["claim_card_ids"]
                }
                self.assertTrue(
                    derived_work_ids.issubset(set(paragraph["source_revision_work_ids"]))
                )

                if paragraph["kind"] == "current_body":
                    self.assertEqual(paragraph["lifecycle"], "current_body")
                    self.assertEqual(paragraph["public_disposition"], "bounded_current")
                    self.assertTrue(paragraph["claim_card_ids"])
                    self.assertTrue(paragraph["source_revision_work_ids"])
                    for card_id in paragraph["claim_card_ids"]:
                        self.assertIn(card_id, body_ids)
                        self.assertEqual(self.cards[card_id]["public"]["state"], "bounded_current")
                    self.assertEqual(set(paragraph["source_revision_work_ids"]), derived_work_ids)
                    self.assertTrue(derived_work_ids.issubset(revisions))
                else:
                    self.assertNotEqual(paragraph["public_disposition"], "bounded_current")

    def test_book_catalog_records_match_the_corpus_manifest(self) -> None:
        records = {record["work_id"]: record for record in self.contract["book_records"]}
        self.assertEqual(set(records), self.works)
        for work_id, record in records.items():
            with self.subTest(work_id=work_id):
                source = self.manifest_works[work_id]
                for field in ("title", "release_state", "public_route"):
                    self.assertEqual(record[field], source[field])
                    if record[field] is not None:
                        self.assertIn(str(record[field]), self.draft)

    def test_every_existing_book_has_one_manifest_role_without_new_ownership(self) -> None:
        roles = self.contract["book_roles"]
        role_ids = [role["work_id"] for role in roles]
        self.assertEqual(len(role_ids), len(set(role_ids)))
        self.assertEqual(set(role_ids), self.works)
        self.assertNotIn("primary_claim_card_owner", self.contract)

    def test_network_state_is_structure_only(self) -> None:
        reference = self.contract["external_structural_reference"]
        self.assertEqual(reference["url"], "https://thenetworkstate.com/")
        self.assertEqual(
            self.contract["compression_ladder"],
            ["one_sentence", "one_image", "short_argument", "one_essay", "research_record"],
        )
        exclusions = set(reference["explicitly_excluded"])
        for required in ("state-building", "sovereignty", "founder entitlement", "growth as validation"):
            self.assertIn(required, exclusions)
        self.assertIn("This draft proposes no political project", self.draft)

    def test_refusals_and_exit_are_load_bearing(self) -> None:
        for phrase in self.contract["non_negotiable_refusals"]:
            self.assertIn(phrase, self.flat_draft)
        for phrase in (
            "None is a membership test",
            "No agreement, popularity, publication, or AI endorsement upgrades a proposition",
        ):
            self.assertIn(phrase, self.flat_draft)

    def test_research_frontier_does_not_promise_completion(self) -> None:
        for forbidden in (
            "completed algebra",
            "total ontology",
            "universal paradox resolution",
            "science unification",
        ):
            self.assertIn(forbidden, self.flat_draft)
        self.assertIn("source-only at this drafting state", self.flat_draft)


if __name__ == "__main__":
    unittest.main()
