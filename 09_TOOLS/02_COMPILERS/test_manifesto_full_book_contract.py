#!/usr/bin/env python3
"""Lifecycle and ownership contracts for the staged full Manifesto book."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "13_BOOKS/manifesto/FULL_BOOK_1_CONTRACT.json"
MANIFEST_PATH = ROOT / "13_BOOKS/book-manifest.json"
CARD_DIR = ROOT / "00_META/claim_cards"


def load_cards() -> tuple[dict[str, dict], dict[str, str]]:
    cards: dict[str, dict] = {}
    work_ids: dict[str, str] = {}
    for path in sorted(CARD_DIR.glob("*.yaml")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for card in payload["cards"]:
            cards[card["card_id"]] = card
            work_ids[card["card_id"]] = payload["work_id"]
    return cards, work_ids


class ManifestoFullBookContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.cards, cls.work_ids = load_cards()

    def test_is_book_one_not_a_fourth_book_or_semantic_owner(self) -> None:
        self.assertEqual(self.contract["schema"], "emergentism/full-book-projection/v1")
        self.assertEqual(self.contract["projection_id"], "MANIFESTO-BOOK-1")
        self.assertEqual(self.contract["composition_id"], "COMP-ACTIVE-01-WELTANSCHAUUNG")
        self.assertEqual(self.contract["status"], "staged_full_book_build_not_public")
        self.assertEqual(self.contract["authority"], "projection_only_no_semantic_authority")
        self.assertIn("K-1 through K-7", self.contract["semantic_owner_rule"])
        compositions = self.manifest["editorial_architecture"]["compositions"]
        composition = next(row for row in compositions if row["composition_id"] == self.contract["composition_id"])
        self.assertEqual(composition["title"], self.contract["title"])
        self.assertEqual(
            composition["output"]["state"],
            "private_full_book_completed_not_public",
        )
        self.assertEqual(composition["output"]["planned_path"], self.contract["manuscript_path"])
        self.assertIsNone(composition["output"]["public_route"])

    def test_current_body_chapters_are_bounded_current_only(self) -> None:
        for chapter in self.contract["chapters"]:
            if chapter["lifecycle_class"] != "current_body":
                continue
            with self.subTest(chapter=chapter["id"]):
                self.assertTrue(chapter["claim_card_ids"])
                for card_id in chapter["claim_card_ids"]:
                    self.assertIn(card_id, self.cards)
                    self.assertEqual(self.cards[card_id]["public"]["state"], "bounded_current")
                self.assertEqual(
                    sorted({self.work_ids[card_id] for card_id in chapter["claim_card_ids"]}),
                    sorted(chapter["source_work_ids"]),
                )
                self.assertEqual(
                    chapter["public_disposition"],
                    "bounded_current_only_after_full_chapter_and_public_gates",
                )

    def test_non_current_chapters_never_present_as_current_body(self) -> None:
        for chapter in self.contract["chapters"]:
            if chapter["lifecycle_class"] not in {"research_record", "historical_provenance"}:
                continue
            with self.subTest(chapter=chapter["id"]):
                self.assertNotIn("bounded_current", chapter["public_disposition"])
                self.assertTrue(chapter["claim_card_ids"])
                self.assertEqual(
                    sorted({self.work_ids[card_id] for card_id in chapter["claim_card_ids"]}),
                    sorted(chapter["source_work_ids"]),
                )

    def test_frozen_reciprocal_is_custody_not_regenerated_book_prose(self) -> None:
        claimed = {
            card_id
            for chapter in self.contract["chapters"]
            for card_id in chapter["claim_card_ids"]
        }
        self.assertFalse(any(card_id.startswith("RIP01-") for card_id in claimed))
        custody = next(
            item for item in self.contract["appendices"]
            if item["id"] == "appendix_reciprocal_custody"
        )
        self.assertEqual(custody["lifecycle_class"], "custody_only")
        self.assertEqual(custody["custody_work_id"], "BK-RECIPROCAL-INFINITE-PLAY")
        self.assertEqual(custody["public_disposition"], "no_regenerated_prose")

    def test_part_order_is_complete_and_unique(self) -> None:
        chapter_ids = [chapter["id"] for chapter in self.contract["chapters"]]
        self.assertEqual(len(chapter_ids), len(set(chapter_ids)))
        routed = [chapter_id for part in self.contract["parts"] for chapter_id in part["chapter_ids"]]
        self.assertEqual(routed, chapter_ids)
        self.assertEqual(self.contract["parts"][0]["id"], "preamble")
        self.assertEqual(self.contract["parts"][-1]["id"], "part_v")

    def test_every_chapter_is_assembled_with_a_private_source_module_after_local_completion(self) -> None:
        self.assertEqual(
            self.contract["manuscript_state"],
            "private_full_book_completed_not_public",
        )
        self.assertEqual(
            {chapter["build_state"] for chapter in self.contract["chapters"]},
            {"private_full_book_completed_not_public"},
        )
        for chapter in self.contract["chapters"]:
            with self.subTest(chapter=chapter["id"]):
                path = ROOT / "13_BOOKS" / chapter["draft_path"]
                self.assertTrue(path.is_file(), path)
        self.assertEqual(
            self.contract["assembler_path"],
            "09_TOOLS/02_COMPILERS/assemble_manifesto_book.py",
        )
        self.assertEqual(
            self.contract["paragraph_ledger_path"],
            "manifesto/MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json",
        )
if __name__ == "__main__":
    unittest.main()
