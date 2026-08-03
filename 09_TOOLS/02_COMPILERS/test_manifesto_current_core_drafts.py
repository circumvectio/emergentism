#!/usr/bin/env python3
"""Keep preserved workbench core drafts inside the current-claim ceiling."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOOKS_DIR = ROOT / "13_BOOKS"
CONTRACT = ROOT / "13_BOOKS/manifesto/FULL_BOOK_1_CONTRACT.json"
CARD_DIR = ROOT / "00_META/claim_cards"
MARKER = re.compile(r"<!-- FULLBOOK-P: ([a-z0-9_-]+) -->")
CARD_ID = re.compile(r"\b([A-Z][A-Z0-9]*\d{2}-\d{2})\b")


def load_cards() -> dict[str, dict]:
    cards: dict[str, dict] = {}
    for path in sorted(CARD_DIR.glob("*.yaml")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for card in payload["cards"]:
            cards[card["card_id"]] = card
    return cards


class ManifestoCurrentCoreDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.cards = load_cards()

    def test_workbench_drafts_remain_private_and_preserved_after_assembly(self) -> None:
        modules = self.contract["unintegrated_draft_modules"]
        self.assertEqual(len(modules), 2)
        for module in modules:
            with self.subTest(path=module["path"]):
                self.assertEqual(module["status"], "superseded_workbench_draft_preserved_not_assembled")
                self.assertEqual(module["public_disposition"], "not_a_public_route")
                self.assertTrue((BOOKS_DIR / module["path"]).is_file())

    def test_every_draft_marker_has_exactly_one_current_card_line(self) -> None:
        for module in self.contract["unintegrated_draft_modules"]:
            path = BOOKS_DIR / module["path"]
            text = path.read_text(encoding="utf-8")
            markers = list(MARKER.finditer(text))
            self.assertEqual(len(markers), len({match.group(1) for match in markers}))
            self.assertGreater(len(markers), 0)
            for index, marker in enumerate(markers):
                end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
                section = text[marker.end():end]
                source_lines = re.findall(r"^Source cards: (.+)$", section, flags=re.MULTILINE)
                with self.subTest(path=module["path"], marker=marker.group(1)):
                    self.assertEqual(len(source_lines), 1)
                    card_ids = CARD_ID.findall(source_lines[0])
                    self.assertTrue(card_ids)
                    for card_id in card_ids:
                        self.assertIn(card_id, self.cards)
                        self.assertEqual(self.cards[card_id]["public"]["state"], "bounded_current")

    def test_no_research_or_frozen_card_id_enters_current_core_drafts(self) -> None:
        prohibited_prefixes = ("TIT01-", "DHY01-", "EN01-", "SES01-", "SL01-", "SV01-", "RIP01-")
        for module in self.contract["unintegrated_draft_modules"]:
            text = (BOOKS_DIR / module["path"]).read_text(encoding="utf-8")
            with self.subTest(path=module["path"]):
                self.assertFalse(any(prefix in text for prefix in prohibited_prefixes))


if __name__ == "__main__":
    unittest.main()
