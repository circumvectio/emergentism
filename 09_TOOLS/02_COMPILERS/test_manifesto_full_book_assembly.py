#!/usr/bin/env python3
"""Completion tests for the staged, private full Emergentist Manifesto.

The test verifies a projection and its evidence boundaries.  It does not treat
the length, a green test suite, or an assembled book as evidence that any
worldview claim is true or ready for public release.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MANIFESTO = ROOT / "13_BOOKS/manifesto"
CONTRACT_PATH = MANIFESTO / "FULL_BOOK_1_CONTRACT.json"
BOOK_PATH = MANIFESTO / "MANIFESTO_BOOK_1.md"
BUILD_PATH = MANIFESTO / "MANIFESTO_BOOK_1_BUILD.json"
LEDGER_PATH = MANIFESTO / "MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json"
ASSEMBLER = ROOT / "09_TOOLS/02_COMPILERS/assemble_manifesto_book.py"
CARD_DIR = ROOT / "00_META/claim_cards"
PREAMBLE_CONTRACT_PATH = MANIFESTO / "manifesto-contract.json"
BOOK_MANIFEST_PATH = ROOT / "13_BOOKS/book-manifest.json"
COMPLETION_GATE_PATH = MANIFESTO / "FULL_BOOK_1_COMPLETION_GATE.md"

SPEC = importlib.util.spec_from_file_location("assemble_manifesto_book", ASSEMBLER)
assert SPEC and SPEC.loader
COMPILER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPILER)

MARKER = re.compile(r"<!-- FULLBOOK-P: ([a-z0-9_-]+) -->")
CARD_ID = re.compile(r"\b[A-Z]+\d{2}-\d{2}\b")
CHAPTER = re.compile(r"(?m)^## ([0-9]+)\. (.+)$")


def load_cards() -> dict[str, dict]:
    cards: dict[str, dict] = {}
    for path in sorted(CARD_DIR.glob("*.yaml")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for card in payload["cards"]:
            cards[card["card_id"]] = {**card, "_work_id": payload["work_id"], "_source": payload["source"]}
    return cards


def marker_units(text: str) -> dict[str, str]:
    matches = list(MARKER.finditer(text))
    units: dict[str, str] = {}
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        units[match.group(1)] = text[match.end() : stop]
    return units


class ManifestoFullBookAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.book = BOOK_PATH.read_text(encoding="utf-8")
        cls.build = json.loads(BUILD_PATH.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.cards = load_cards()
        cls.preamble_records = {
            row["id"]: row
            for row in json.loads(PREAMBLE_CONTRACT_PATH.read_text(encoding="utf-8"))["paragraphs"]
        }
        cls.book_manifest = json.loads(BOOK_MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.units = marker_units(cls.book)
        cls.chapter_by_id = {chapter["id"]: chapter for chapter in cls.contract["chapters"]}

    def manual_custody_fixture(self, staged_path: str) -> tuple[Path, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "corpus"
        books = root / "13_BOOKS"
        books.mkdir(parents=True)
        manifest_path = books / "book-manifest.json"
        manifest_path.write_text(
            json.dumps({
                "works": [{
                    "work_id": "BK-RECIPROCAL-INFINITE-PLAY",
                    "historical_sources": [{
                        "path": "legacy/reciprocal.md",
                        "lifecycle": "frozen",
                        "reviewed_source_sha256": "a" * 64,
                    }],
                    "build_provenance": {
                        "type": "manual",
                        "description": "manual custody fixture",
                        "verification": "focused mutation test",
                    },
                    "staged_critical_edition": staged_path,
                }],
                "editorial_architecture": {
                    "nonbook_claim_routes": [{
                        "work_id": "BK-RECIPROCAL-INFINITE-PLAY",
                        "route_id": "CUSTODY-ONLY-RECIPROCAL-ARCHIVE",
                        "primary_home": "13_BOOKS/reciprocal_infinite_play",
                    }],
                },
            }),
            encoding="utf-8",
        )
        return root, books, manifest_path

    def render_manual_custody(self, root: Path, books: Path, manifest_path: Path) -> str:
        with mock.patch.multiple(
            COMPILER,
            ROOT=root,
            BOOKS=books,
            BOOK_MANIFEST=manifest_path,
        ):
            return COMPILER.custody_note()

    def test_assembler_is_deterministic_and_receipts_are_current(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ASSEMBLER), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("FULL BOOK BUILD: PASS", result.stdout)

    def test_single_inline_reader_has_preamble_and_all_contract_chapters_in_order(self) -> None:
        self.assertIn("## Preamble and Quickstart", self.book)
        observed = [(int(number), title) for number, title in CHAPTER.findall(self.book)]
        expected = [(index, chapter["title"]) for index, chapter in enumerate(self.contract["chapters"][1:], start=1)]
        self.assertEqual(observed, expected)
        self.assertNotIn("mapped_not_drafted", self.book)
        self.assertNotIn("[PLACEHOLDER]", self.book)

    def test_declared_private_full_book_word_range_and_status(self) -> None:
        output = self.build["output"]
        target = self.contract["target_word_range"]
        self.assertGreaterEqual(output["word_count"], target["minimum"])
        self.assertLessEqual(output["word_count"], target["maximum"])
        self.assertEqual(output["path"], "13_BOOKS/manifesto/MANIFESTO_BOOK_1.md")
        self.assertEqual(self.contract["status"], "staged_full_book_build_not_public")
        self.assertEqual(self.contract["manuscript_state"], "private_full_book_completed_not_public")
        self.assertEqual(self.build["public_disposition"], "not_a_public_route")
        self.assertIn("a public release", self.book.split("# Part I", maxsplit=1)[0].lower())

    def test_completion_gate_reports_the_current_private_build_counts(self) -> None:
        gate = COMPLETION_GATE_PATH.read_text(encoding="utf-8")
        self.assertIn(f"{self.build['output']['word_count']:,} words", gate)
        self.assertIn(f"{self.build['paragraph_ledger']['count']} unique source-mapped units", gate)

    def test_every_marked_unit_has_one_receipt_and_one_ledger_entry(self) -> None:
        markers = list(self.units)
        self.assertEqual(len(markers), len(set(markers)))
        ledger_entries = {entry["id"]: entry for entry in self.ledger["paragraphs"]}
        self.assertEqual(set(markers), set(ledger_entries))
        self.assertEqual(self.build["paragraph_ledger"]["count"], len(markers))
        for marker_id, unit in self.units.items():
            with self.subTest(marker=marker_id):
                source_lines = re.findall(r"(?m)^Source cards: .+$", unit)
                self.assertEqual(len(source_lines), 1)
                rendered_cards = CARD_ID.findall(source_lines[0])
                entry = ledger_entries[marker_id]
                self.assertEqual(rendered_cards, entry["claim_card_ids"])
                self.assertGreaterEqual(entry["line_range"][0], 1)
                self.assertGreaterEqual(entry["line_range"][1], entry["line_range"][0])
                for card_id in rendered_cards:
                    self.assertIn(card_id, self.cards)
                expected_revisions = {
                    (
                        self.cards[card_id]["_work_id"],
                        self.cards[card_id]["_source"]["path"],
                        self.cards[card_id]["_source"]["reviewed_source_sha256"],
                    )
                    for card_id in rendered_cards
                }
                actual_revisions = {
                    (
                        row["work_id"],
                        row["source_path"],
                        row["reviewed_source_sha256"],
                    )
                    for row in entry["source_revisions"]
                }
                self.assertEqual(expected_revisions, actual_revisions)
                for row in entry["source_revisions"]:
                    self.assertTrue(row["claim_card_ids"])

    def test_preamble_receipts_exactly_match_the_retained_source_contract(self) -> None:
        for entry in self.ledger["paragraphs"]:
            if not entry["id"].startswith("preamble_"):
                continue
            record_id = entry["id"].removeprefix("preamble_")
            with self.subTest(marker=entry["id"]):
                self.assertIn(record_id, self.preamble_records)
                self.assertEqual(
                    entry["claim_card_ids"],
                    self.preamble_records[record_id]["claim_card_ids"],
                )

    def test_build_receipt_covers_every_card_set_not_only_each_work_id(self) -> None:
        expected = []
        for path in sorted(CARD_DIR.glob("*.yaml")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            expected.append({
                "work_id": payload["work_id"],
                "path": path.relative_to(ROOT).as_posix(),
                "source": payload["source"]["path"],
                "reviewed_source_sha256": payload["source"]["reviewed_source_sha256"],
            })
        actual = self.build["claim_card_sets"]
        self.assertEqual(
            sorted(actual, key=lambda row: (row["work_id"], row["path"])),
            sorted(expected, key=lambda row: (row["work_id"], row["path"])),
        )

    def test_current_body_is_bounded_and_chapter_cards_cover_its_units(self) -> None:
        for entry in self.ledger["paragraphs"]:
            with self.subTest(marker=entry["id"]):
                if entry["lifecycle_class"] == "current_body":
                    self.assertTrue(entry["claim_card_ids"])
                    for card_id in entry["claim_card_ids"]:
                        self.assertEqual(self.cards[card_id]["public"]["state"], "bounded_current")
                chapter = self.chapter_by_id.get(entry["chapter_id"])
                if chapter is not None:
                    self.assertTrue(set(entry["claim_card_ids"]).issubset(set(chapter["claim_card_ids"])))

    def test_research_chapters_and_their_card_atlas_keep_rivals_and_kill_routes_visible(self) -> None:
        for chapter_id in (
            "ch12_titans_research",
            "ch13_world_contact",
            "ch14_action_and_institution_research",
            "ch15_lenses_and_immune_protocol",
        ):
            chapter = self.chapter_by_id[chapter_id]
            chapter_entries = [
                entry
                for entry in self.ledger["paragraphs"]
                if entry["chapter_id"] == chapter_id
            ]
            for entry in chapter_entries:
                unit = self.units[entry["id"]]
                with self.subTest(chapter=chapter_id, research_unit=entry["id"]):
                    self.assertIn("Research status:", unit)
                    self.assertIn("Strongest rival:", unit)
                    self.assertIn("Discriminator:", unit)
                    self.assertIn("Narrow or kill condition:", unit)
                    self.assertIn("Public disposition:", unit)
                    self.assertIn("research_record", entry)
                    record = entry["research_record"]
                    self.assertEqual(record["primary_card_id"], entry["claim_card_ids"][0])
                    self.assertEqual(record["record_basis"], "derived_from_primary_card")
                    self.assertEqual(record["public_disposition"].split(";", 1)[0], "`private_research_record_only`")
                    for key in (
                        "research_status",
                        "strongest_rival",
                        "discriminator",
                        "narrow_or_kill_condition",
                    ):
                        self.assertTrue(record[key])
                    for card_id in entry["claim_card_ids"][1:]:
                        atlas = self.units["atlas_" + card_id.lower().replace("-", "_")]
                        self.assertIn("**Strongest rival:**", atlas)
                        self.assertIn("**Kill or narrowing route:**", atlas)
            research_cards = [
                card_id for card_id in chapter["claim_card_ids"]
                if self.cards[card_id]["public"]["state"] != "bounded_current"
            ]
            for card_id in research_cards:
                atlas_id = "atlas_" + card_id.lower().replace("-", "_")
                with self.subTest(chapter=chapter_id, card=card_id):
                    self.assertIn(atlas_id, self.units)
                    atlas = self.units[atlas_id]
                    self.assertIn("**Strongest rival:**", atlas)
                    self.assertIn("**Discriminator:**", atlas)
                    self.assertIn("**Kill or narrowing route:**", atlas)
                    self.assertIn("**Lifecycle and public ceiling:**", atlas)

    def test_historical_and_frozen_material_stays_in_its_lane(self) -> None:
        historical = [entry for entry in self.ledger["paragraphs"] if entry["chapter_id"] == "ch16_corrections_kept"]
        self.assertTrue(historical)
        self.assertTrue(all(entry["lifecycle_class"] == "historical_provenance" for entry in historical))
        self.assertTrue(all(all(card_id.startswith("SV01-") for card_id in entry["claim_card_ids"]) for entry in historical))
        sarpasya = next(row for row in self.book_manifest["works"] if row["work_id"] == "BK-SARPASYA")
        genealogy_header = self.units["p5-16-001"]
        source = sarpasya["historical_sources"][0]
        source_path = source if isinstance(source, str) else source["path"]
        self.assertIn(source_path, genealogy_header)
        sarpasya_card_source = self.cards["SV01-02"]["_source"]
        self.assertIn(sarpasya_card_source["reviewed_source_sha256"], genealogy_header)
        self.assertIn(sarpasya["build_provenance"]["path"], genealogy_header)
        self.assertIn(sarpasya["build_provenance"]["sha256"], genealogy_header)
        self.assertIn("13_BOOKS/sarpasya_vijayam/DEBRIEF.md", genealogy_header)
        before_atlas = self.book.split("# Appendix B — Claim-Card Atlas", maxsplit=1)[0]
        self.assertNotRegex(before_atlas, r"RIP01-\d{2}")
        frozen = [entry for entry in self.ledger["paragraphs"] if entry["id"].startswith("atlas_rip")]
        self.assertEqual(len(frozen), 7)
        for entry in frozen:
            unit = self.units[entry["id"]]
            self.assertIn("frozen custody record", unit)
            self.assertIn("does not regenerate its claim", unit)
            self.assertEqual(entry["card_public_states"], ["frozen"])
            self.assertEqual(entry["lifecycle_class"], "custody_only")
            self.assertEqual(entry["public_disposition"], "no_regenerated_prose")
        reciprocal = next(row for row in self.book_manifest["works"] if row["work_id"] == "BK-RECIPROCAL-INFINITE-PLAY")
        custody = self.units["appendix_reciprocal_custody"]
        self.assertIn(reciprocal["work_id"], custody)
        self.assertIn("CUSTODY-ONLY-RECIPROCAL-ARCHIVE", custody)
        for source in reciprocal["historical_sources"]:
            self.assertIn(source["path"], custody)
            self.assertIn(source["reviewed_source_sha256"], custody)
        provenance = reciprocal["build_provenance"]
        self.assertEqual(provenance["type"], "projection_artifact")
        staged_path = reciprocal["staged_critical_edition"]
        staged_sha = hashlib.sha256((ROOT / "13_BOOKS" / staged_path).read_bytes()).hexdigest()
        self.assertEqual(provenance["path"], staged_path)
        self.assertEqual(provenance["sha256"], staged_sha)
        self.assertIn(staged_path, custody)
        self.assertIn(staged_sha, custody)

    def test_manual_custody_rejects_absolute_staged_path(self) -> None:
        root, books, manifest_path = self.manual_custody_fixture("/etc/hosts")
        with self.assertRaisesRegex(
            COMPILER.ContractError,
            "must be relative to 13_BOOKS",
        ):
            self.render_manual_custody(root, books, manifest_path)

    def test_manual_custody_rejects_parent_traversal(self) -> None:
        root, books, manifest_path = self.manual_custody_fixture("../escape.md")
        (root / "escape.md").write_text("outside custody", encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "parent traversal"):
            self.render_manual_custody(root, books, manifest_path)

    def test_manual_custody_rejects_file_symlink(self) -> None:
        root, books, manifest_path = self.manual_custody_fixture("linked.md")
        outside = root / "outside.md"
        outside.write_text("outside custody", encoding="utf-8")
        try:
            (books / "linked.md").symlink_to(outside)
        except (NotImplementedError, OSError) as exc:
            self.skipTest(f"file symlinks unavailable: {exc}")
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            self.render_manual_custody(root, books, manifest_path)

    def test_manual_custody_rejects_parent_directory_symlink(self) -> None:
        root, books, manifest_path = self.manual_custody_fixture("linked/staged.md")
        outside = root / "outside"
        outside.mkdir()
        (outside / "staged.md").write_text("outside custody", encoding="utf-8")
        try:
            (books / "linked").symlink_to(outside, target_is_directory=True)
        except (NotImplementedError, OSError) as exc:
            self.skipTest(f"directory symlinks unavailable: {exc}")
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            self.render_manual_custody(root, books, manifest_path)

    def test_manual_custody_requires_a_regular_file(self) -> None:
        root, books, manifest_path = self.manual_custody_fixture("staged-directory")
        (books / "staged-directory").mkdir()
        with self.assertRaisesRegex(COMPILER.ContractError, "regular file"):
            self.render_manual_custody(root, books, manifest_path)

    def test_only_declared_atlas_and_docket_markers_cover_an_immediately_following_heading(self) -> None:
        for marker_id, unit in self.units.items():
            if re.match(r"^(atlas_|docket_)", marker_id):
                with self.subTest(marker=marker_id):
                    self.assertRegex(unit, r"^\s*#{2,3} ")

    def test_full_book_stays_private_and_refusal_bounded(self) -> None:
        front = self.book.split("# Part I", maxsplit=1)[0]
        for phrase in (
            "is not a completed ontology, a public release, a membership test, a political programme",
        ):
            self.assertIn(phrase, front)
        for phrase in (
            "A theorem is not an ontology.",
            "A model is not the territory.",
            "A symbol is not a causal agent.",
            "Any holder may put it down.",
        ):
            self.assertIn(phrase, self.book)


if __name__ == "__main__":
    unittest.main()
