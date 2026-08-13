from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = Path(__file__).with_name("compile_claim_cards.py")
SPEC = importlib.util.spec_from_file_location("compile_claim_cards", MODULE_PATH)
assert SPEC and SPEC.loader
COMPILER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPILER)


def declared_external_sources() -> dict[str, dict[str, object]]:
    """Return the unique, metadata-pinned Skyzai source inventory."""
    inventory: dict[str, dict[str, object]] = {}

    def remember(
        base: Path,
        raw_path: str,
        sha256: str,
        lifecycle: str,
        work_id: str,
        role: str,
    ) -> None:
        canonical = COMPILER._canonical_external_declaration(base, Path(raw_path))
        if canonical is None:
            return
        existing = inventory.get(canonical)
        contract = (sha256, lifecycle)
        if existing is not None and existing["contract"] != contract:
            raise AssertionError(f"conflicting external metadata for {canonical}")
        inventory.setdefault(
            canonical,
            {"contract": contract, "declarations": []},
        )["declarations"].append((base, Path(raw_path), work_id, role))

    for path in sorted((ROOT / COMPILER.CARD_DIR).glob("*.yaml")):
        document = json.loads(path.read_text(encoding="utf-8"))
        source = document.get("source", {})
        if all(isinstance(source.get(field), str) for field in (
            "path", "reviewed_source_sha256", "lifecycle"
        )):
            remember(
                Path("."),
                source["path"],
                source["reviewed_source_sha256"],
                source["lifecycle"],
                document["work_id"],
                "claim_card",
            )
    manifest = json.loads((ROOT / COMPILER.BOOK_MANIFEST_PATH).read_text(encoding="utf-8"))
    for work in manifest["works"]:
        for source in work["historical_sources"]:
            if isinstance(source, dict):
                remember(
                    COMPILER.BOOK_MANIFEST_PATH.parent,
                    source["path"],
                    source["reviewed_source_sha256"],
                    source["lifecycle"],
                    work["work_id"],
                    "book_manifest",
                )
            elif isinstance(source, str):
                canonical = COMPILER._canonical_external_declaration(
                    COMPILER.BOOK_MANIFEST_PATH.parent, Path(source)
                )
                if canonical is not None:
                    existing = inventory.get(canonical)
                    if existing is None:
                        raise AssertionError(
                            f"untyped external source lacks claim-card pin: {canonical}"
                        )
                    sha256, lifecycle = existing["contract"]
                    remember(
                        COMPILER.BOOK_MANIFEST_PATH.parent,
                        source,
                        sha256,
                        lifecycle,
                        work["work_id"],
                        "book_manifest",
                    )
    return inventory


EXTERNAL_SOURCE_DECLARATIONS = declared_external_sources()


def missing_federated_sources() -> list[str]:
    """Return exact external bytes unavailable in an authorized federation."""
    missing: list[str] = []
    for canonical, record in sorted(EXTERNAL_SOURCE_DECLARATIONS.items()):
        sha256 = record["contract"][0]
        available = False
        for base, declared, _, _ in record["declarations"]:
            candidate = COMPILER._bounded_external_candidate(ROOT, base, declared)
            if candidate is not None and candidate.is_file():
                if hashlib.sha256(candidate.read_bytes()).hexdigest() == sha256:
                    available = True
                    break
            relocated = COMPILER._resolve_hash_bound_relocation(
                ROOT, declared, sha256, base
            )
            if relocated is not None:
                available = True
                break
        if not available:
            missing.append(canonical)
    return missing


FEDERATED_SOURCE_GAPS = missing_federated_sources()
REPOSITORY_CONTRACT_SKIP = (
    "exact private Skyzai byte replay unavailable; metadata contracts still run; missing: "
    + ", ".join(FEDERATED_SOURCE_GAPS)
)


class ClaimGraphContractTests(unittest.TestCase):
    def make_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "corpus"
        copies = [
            "00_THE_KERNEL_INDEX.md",
            "00_THE_WELTANSCHAUUNG_ONE_SITTING.md",
            "00_META/schemas/claim-card.schema.yaml",
            "00_META/ADEQUACY_DOCKETS.yaml",
            "00_META/00_ONE_SITTING_CLAIM_CARD_SET_01.md",
            "00_META/claim_cards/one_sitting.yaml",
        ]
        schema = json.loads((ROOT / "00_META/schemas/claim-card.schema.yaml").read_text(encoding="utf-8"))
        copies.extend(schema["owner_registry"].values())
        for rel in copies:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, target)
        # The production OS01-12 card correctly depends on RIP01-03, but this
        # deliberately minimal fixture includes only the One-Sitting card set.
        # Remove that external dependency here so fixture failures continue to
        # isolate the contract mutation under test.
        fixture_cards_path = root / "00_META/claim_cards/one_sitting.yaml"
        fixture_cards = json.loads(fixture_cards_path.read_text(encoding="utf-8"))
        os12 = next(
            card for card in fixture_cards["cards"] if card["card_id"] == "OS01-12"
        )
        os12["dependencies"] = [
            dependency
            for dependency in os12["dependencies"]
            if dependency != "RIP01-03"
        ]
        fixture_cards_path.write_text(json.dumps(fixture_cards), encoding="utf-8")
        (root / "13_BOOKS").mkdir(parents=True)
        (root / "12_PUBLIC_SITE/book").mkdir(parents=True)
        (root / "12_PUBLIC_SITE/book/index.html").write_text("book", encoding="utf-8")
        (root / "legacy.md").write_text("legacy", encoding="utf-8")
        manifest = json.loads((ROOT / "13_BOOKS/book-manifest.json").read_text(encoding="utf-8"))
        active = copy.deepcopy(manifest["works"][0])
        active["owner_ids"] = sorted(
            {card["semantic_owner_id"] for card in fixture_cards["cards"]}
        )
        active["build_provenance"] = {
            "type": "manual",
            "description": "Fixture projection.",
            "verification": "Fixture checks.",
        }
        legacy = {
            "work_id": "BK-LEGACY-FIXTURE", "title": "Legacy fixture", "edition": "historical",
            "historical_sources": [{
                "path": "../legacy.md",
                "lifecycle": "legacy",
                "reviewed_source_sha256": hashlib.sha256(b"legacy").hexdigest(),
            }], "chapter_order": [], "owner_ids": [],
            "claim_card_ids": [], "release_state": "historical_readonly_debrief_open",
            "public_route": None,
            "build_provenance": {
                "type": "manual",
                "description": "Fixture is not built.",
                "verification": "Fixture checks.",
            },
        }
        architecture = {
            "schema": "emergentism/book-composition/v2",
            "status": "staged_proposal",
            "confirmation": {
                "state": "unconfirmed", "receipt": None, "receipt_sha256": None,
            },
            "authority": "projection_only_no_semantic_authority",
            "decision": "Fixture proposal only.",
            "compositions": [
                {
                    "composition_id": "COMP-ACTIVE-01-WELTANSCHAUUNG",
                    "catalog_class": "active_book", "title": "Fixture reader",
                    "anchor_work_id": "BK-ONE-SITTING",
                    "output": {"state": "current_reader_rebuild_pending"},
                    "components": [{
                        "work_id": "BK-ONE-SITTING", "claim_selection": "all",
                        "projection_mode": "primary",
                    }],
                },
                {
                    "composition_id": "COMP-ACTIVE-02-TITANS",
                    "catalog_class": "active_research_book", "title": "Fixture research book",
                    "output": {"state": "planned_not_built"}, "components": [],
                },
                {
                    "composition_id": "COMP-ACTIVE-03-LIVED-COMPASS",
                    "catalog_class": "active_practice_book", "title": "Fixture practice book",
                    "output": {"state": "planned_not_built"}, "components": [],
                },
                {
                    "composition_id": "COMP-HISTORICAL-01-SERPENT-CYCLE",
                    "catalog_class": "historical_critical_reader", "title": "Fixture history",
                    "output": {"state": "planned_not_built"}, "components": [],
                },
            ],
            "edition_dispositions": [
                {
                    "work_id": "BK-ONE-SITTING",
                    "existing_edition_disposition": "retained_and_rebuilt_in_place",
                },
                {
                    "work_id": "BK-LEGACY-FIXTURE",
                    "existing_edition_disposition": "preserved_module_projection",
                },
            ],
            "nonbook_claim_routes": [],
            "integrity": {
                "existing_claim_card_count": 26,
                "primary_cards_by_composition": {
                    "COMP-ACTIVE-01-WELTANSCHAUUNG": 26,
                    "COMP-ACTIVE-02-TITANS": 0,
                    "COMP-ACTIVE-03-LIVED-COMPASS": 0,
                    "COMP-HISTORICAL-01-SERPENT-CYCLE": 0,
                },
                "primary_cards_by_nonbook_home": {},
                "total_primary_or_custody_routes": 26,
            },
        }
        (root / "13_BOOKS/book-manifest.json").write_text(
            json.dumps({
                "schema": "emergentism/book-manifest/v2", "works": [active, legacy],
                "editorial_architecture": architecture,
            }),
            encoding="utf-8",
        )
        return temp, root

    def mutate_cards(self, root: Path, fn) -> None:
        path = root / "00_META/claim_cards/one_sitting.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        fn(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def mutate_book_manifest(self, root: Path, fn) -> None:
        path = root / "13_BOOKS/book-manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        fn(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def confirm_architecture_with_receipt(
        self, root: Path, receipt: str, receipt_sha256: str
    ) -> None:
        def mutate(manifest):
            manifest["editorial_architecture"]["status"] = "confirmed"
            manifest["editorial_architecture"]["confirmation"] = {
                "state": "confirmed",
                "receipt": receipt,
                "receipt_sha256": receipt_sha256,
            }

        self.mutate_book_manifest(root, mutate)

    def supersede_first_edition(
        self, root: Path, successor_path: str, gate_receipt: str
    ) -> None:
        def mutate(manifest):
            disposition = manifest["editorial_architecture"]["edition_dispositions"][0]
            disposition["existing_edition_disposition"] = "superseded_by_successor"
            disposition["successor_path"] = successor_path
            disposition["gate_receipt"] = gate_receipt

        self.mutate_book_manifest(root, mutate)

    def write_supersession_fixture_files(self, root: Path) -> tuple[str, str]:
        successor = root / "successor.md"
        receipt = root / "gate-receipt.md"
        successor.write_text("successor", encoding="utf-8")
        receipt.write_text("gate receipt", encoding="utf-8")
        return successor.name, receipt.name

    def assert_external_locator_inventory_mutation_fails(self, mutate) -> None:
        target = (ROOT / "00_META/claim_cards/reciprocal_infinite_play.yaml").resolve()
        original_read = COMPILER._read_json_yaml

        def mutated_read(path: Path) -> dict:
            document = original_read(path)
            if path.resolve() == target:
                document = copy.deepcopy(document)
                mutate(document["cards"][0]["locator"])
            return document

        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(
                COMPILER, "_read_json_yaml", side_effect=mutated_read
            ):
                with self.assertRaisesRegex(
                    COMPILER.ContractError,
                    "external card locator semantic inventory changed",
                ):
                    COMPILER.compile_contract(
                        ROOT, allow_unavailable_external=True
                    )

    def test_external_metadata_inventory_is_exactly_six_hash_pins(self) -> None:
        expected = {
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/00_THE_INFINITE_BOOK_OF_EMERGENCE.md": "081fb55303f07409713c086bbb73bd3d2025eebf14713c54a6629483b91aa3a9",
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/08_PRIOR_BOOKS/01_BOOK_I_SARPASYA_VIJAYAM/DISSEMINATION/SARPASYA_VIJAYAM_EDITION_1.md": "aa59ccbda3ca3f615f71aaf11141e45b9b10588f8454295e6445742d18199436",
            "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/02_BOOK_II_THE_SIX_LENSES/DISSEMINATION/THE_SIX_LENSES_EDITION_1.md": "17ad1a31461f27738b0128a2e53fbed78e5aadeee04ee2de8aadf4cb74fe0ab2",
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/08_PRIOR_BOOKS/03_BOOK_III_THE_SELF_EATING_SERPENT/DISSEMINATION/THE_SELF_EATING_SERPENT_EDITION_1.md": "397ee521026dd999431250bbc55e86181ffc03b6b14a820adf98d70ab81f3ac4",
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/07_PUBLIC_EDITION/THE_RECIPROCAL_PUBLIC_EDITION_K2_LANG_DECOMM_2026_07_22.md": "86b59d4f3e4ad8ec64e85fb1b075ac986953b3c28339eda1046459789696a1f9",
            "../02_SKYZAI/08_EVOLUTIONARY_NETWORK/README.md": "df8887940ce76d68e1073ee18b197b3a64059fef73ad094128d6143a4a6105d6",
        }
        observed = {
            path: record["contract"][0]
            for path, record in EXTERNAL_SOURCE_DECLARATIONS.items()
        }
        self.assertEqual(observed, expected)
        expected_bindings = {
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/00_THE_INFINITE_BOOK_OF_EMERGENCE.md": (
                "frozen", frozenset({"BK-RECIPROCAL-INFINITE-PLAY"}),
                frozenset({"book_manifest"}), frozenset({"13_BOOKS"}),
            ),
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/08_PRIOR_BOOKS/01_BOOK_I_SARPASYA_VIJAYAM/DISSEMINATION/SARPASYA_VIJAYAM_EDITION_1.md": (
                "legacy", frozenset({"BK-SARPASYA"}),
                frozenset({"claim_card", "book_manifest"}),
                frozenset({".", "13_BOOKS"}),
            ),
            "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/02_BOOK_II_THE_SIX_LENSES/DISSEMINATION/THE_SIX_LENSES_EDITION_1.md": (
                "legacy", frozenset({"BK-SIX-LENSES"}),
                frozenset({"claim_card", "book_manifest"}),
                frozenset({".", "13_BOOKS"}),
            ),
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/08_PRIOR_BOOKS/03_BOOK_III_THE_SELF_EATING_SERPENT/DISSEMINATION/THE_SELF_EATING_SERPENT_EDITION_1.md": (
                "legacy", frozenset({"BK-SELF-EATING"}),
                frozenset({"claim_card", "book_manifest"}),
                frozenset({".", "13_BOOKS"}),
            ),
            "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/07_PUBLIC_EDITION/THE_RECIPROCAL_PUBLIC_EDITION_K2_LANG_DECOMM_2026_07_22.md": (
                "frozen", frozenset({"BK-RECIPROCAL-INFINITE-PLAY"}),
                frozenset({"claim_card", "book_manifest"}),
                frozenset({".", "13_BOOKS"}),
            ),
            "../02_SKYZAI/08_EVOLUTIONARY_NETWORK/README.md": (
                "proposal", frozenset({"BK-EVOLUTIONARY-NETWORK"}),
                frozenset({"book_manifest"}), frozenset({"13_BOOKS"}),
            ),
        }
        observed_bindings = {
            path: (
                record["contract"][1],
                frozenset(row[2] for row in record["declarations"]),
                frozenset(row[3] for row in record["declarations"]),
                frozenset(row[0].as_posix() for row in record["declarations"]),
            )
            for path, record in EXTERNAL_SOURCE_DECLARATIONS.items()
        }
        self.assertEqual(observed_bindings, expected_bindings)
        self.assertEqual(COMPILER.EXTERNAL_SOURCE_CONTRACTS, {
            path: (expected[path], binding[0], next(iter(binding[1])), binding[2])
            for path, binding in expected_bindings.items()
        })
        for record in EXTERNAL_SOURCE_DECLARATIONS.values():
            self.assertRegex(record["contract"][0], r"^[0-9a-f]{64}$")

    @unittest.skipIf(FEDERATED_SOURCE_GAPS, REPOSITORY_CONTRACT_SKIP)
    def test_authorized_external_source_bytes_replay_exactly(self) -> None:
        for canonical, record in EXTERNAL_SOURCE_DECLARATIONS.items():
            expected_sha256 = record["contract"][0]
            matches: list[Path] = []
            for base, declared, _, _ in record["declarations"]:
                candidate = COMPILER._bounded_external_candidate(ROOT, base, declared)
                if candidate is not None and candidate.is_file():
                    matches.append(candidate)
                relocated = COMPILER._resolve_hash_bound_relocation(
                    ROOT, declared, expected_sha256, base
                )
                if relocated is not None:
                    matches.append(relocated[0])
            self.assertTrue(matches, canonical)
            self.assertTrue(
                any(
                    hashlib.sha256(path.read_bytes()).hexdigest() == expected_sha256
                    for path in matches
                ),
                canonical,
            )

    def test_repository_contract_compiles(self) -> None:
        register, graph, lifecycle = COMPILER.compile_contract(
            ROOT, allow_unavailable_external=True
        )
        self.assertEqual(register["schema"], "emergentism/claim-card-register/v2")
        self.assertEqual(graph["schema"], "emergentism/claim-owner-dependency-graph/v2")
        self.assertEqual(lifecycle["schema"], "emergentism/claim-lifecycle-inventory/v3")
        self.assertEqual(register["metrics"]["cards"], 72)
        self.assertEqual(register["metrics"]["works_with_cards"], 9)
        expected_owners = (
            {f"K-{i}" for i in range(1, 8)}
            | {f"KER-{i}" for i in range(1, 8)}
        )
        self.assertEqual(
            {row["owner_id"] for row in register["owners"]}, expected_owners
        )
        self.assertGreater(graph["metrics"]["edges"], 300)
        self.assertEqual(lifecycle["baseline"]["tracked_files"], 3205)

    def test_deterministic_generation(self) -> None:
        first = COMPILER.compile_contract(ROOT, allow_unavailable_external=True)
        second = COMPILER.compile_contract(ROOT, allow_unavailable_external=True)
        self.assertEqual([COMPILER._canonical_bytes(x) for x in first], [COMPILER._canonical_bytes(x) for x in second])

    def test_check_detects_deliberate_drift(self) -> None:
        temp, root = self.make_fixture()
        self.addCleanup(temp.cleanup)
        outputs = COMPILER.compile_contract(root)
        COMPILER.write_outputs(root, outputs)
        self.assertEqual(COMPILER.check_outputs(root, outputs), [])
        (root / COMPILER.REGISTER_PATH).write_text("{}\n", encoding="utf-8")
        self.assertTrue(COMPILER.check_outputs(root, outputs))

    def test_titans_formal_current_custody_is_exact(self) -> None:
        card_path = ROOT / "00_META/claim_cards/titans_formal.yaml"
        document = json.loads(card_path.read_text(encoding="utf-8"))
        source = ROOT / document["source"]["path"]
        self.assertEqual(
            document["source"]["reviewed_source_sha256"],
            hashlib.sha256(source.read_bytes()).hexdigest(),
        )
        lines = source.read_text(encoding="utf-8").splitlines()
        for card in document["cards"]:
            locator = card["locator"]
            located = COMPILER._located_text(
                lines, locator["line_start"], locator["line_end"]
            )
            self.assertIn(locator["anchor"], located, card["card_id"])
            self.assertEqual(
                locator["fingerprint_sha256"],
                COMPILER._text_sha256(located),
                card["card_id"],
            )

    def test_titans_inversion_restatement_tracks_no_coercion_owner(self) -> None:
        card_path = ROOT / "00_META/claim_cards/titans_inversion.yaml"
        document = json.loads(card_path.read_text(encoding="utf-8"))
        source = ROOT / document["source"]["path"]
        self.assertEqual(
            document["source"]["reviewed_source_sha256"],
            hashlib.sha256(source.read_bytes()).hexdigest(),
        )
        self.assertEqual(len(document["cards"]), 1)
        card = document["cards"][0]
        self.assertEqual(card["card_id"], "TIT01-06")
        self.assertEqual([row["tier"] for row in card["evidence"]], ["I"])
        self.assertEqual(card["public"]["state"], "source_only")
        self.assertEqual(
            card["strongest_rival"],
            "Use the projective orbit facts without Titan imagery.",
        )
        self.assertEqual(
            card["kill_criterion"],
            "Retire the representation if readers or generated text apply inversion or arithmetic directly to Titan seats.",
        )
        serialized = json.dumps(card, ensure_ascii=False)
        for retired_mapping in ("r_T", "Feature(Ĉ)", "ι_*"):
            self.assertNotIn(retired_mapping, serialized)
        locator = card["locator"]
        lines = source.read_text(encoding="utf-8").splitlines()
        located = COMPILER._located_text(
            lines, locator["line_start"], locator["line_end"]
        )
        self.assertIn(locator["anchor"], located)
        self.assertIn("no-coercion", located)
        self.assertEqual(
            locator["fingerprint_sha256"], COMPILER._text_sha256(located)
        )

    def test_titans_narrative_current_custody_is_exact(self) -> None:
        card_path = ROOT / "00_META/claim_cards/titans_narrative.yaml"
        document = json.loads(card_path.read_text(encoding="utf-8"))
        source = ROOT / document["source"]["path"]
        self.assertEqual(
            document["source"]["reviewed_source_sha256"],
            hashlib.sha256(source.read_bytes()).hexdigest(),
        )
        lines = source.read_text(encoding="utf-8").splitlines()
        for card in document["cards"]:
            locator = card["locator"]
            located = COMPILER._located_text(
                lines, locator["line_start"], locator["line_end"]
            )
            self.assertIn(locator["anchor"], located, card["card_id"])
            self.assertEqual(
                locator["fingerprint_sha256"],
                COMPILER._text_sha256(located),
                card["card_id"],
            )

    def test_duplicate_card_id_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data["cards"].append(copy.deepcopy(data["cards"][0])))
        with self.assertRaisesRegex(COMPILER.ContractError, "duplicate claim-card"):
            COMPILER.compile_contract(root)

    def test_dangling_dependency_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data["cards"][0].update(dependencies=["OS99-99"]))
        with self.assertRaisesRegex(COMPILER.ContractError, "dangling"):
            COMPILER.compile_contract(root)

    def test_dependency_cycle_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        def mutate(data):
            data["cards"][0]["dependencies"] = [data["cards"][1]["card_id"]]
            data["cards"][1]["dependencies"] = [data["cards"][0]["card_id"]]
        self.mutate_cards(root, mutate)
        with self.assertRaisesRegex(COMPILER.ContractError, "dependency cycle"):
            COMPILER.compile_contract(root)

    def test_missing_owner_path_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        (root / "06_ONTOLOGY/04_THE_CONJECTURES.md").unlink()
        with self.assertRaisesRegex(COMPILER.ContractError, "missing owner path"):
            COMPILER.compile_contract(root)

    def test_invalid_source_locator_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data["cards"][0]["locator"].update(line_end=999999))
        with self.assertRaisesRegex(COMPILER.ContractError, "invalid source line range"):
            COMPILER.compile_contract(root)

    def test_locator_anchor_and_fingerprint_are_verified(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data["cards"][0]["locator"].update(anchor="not in source"))
        with self.assertRaisesRegex(COMPILER.ContractError, "locator anchor"):
            COMPILER.compile_contract(root)

    def test_locator_fingerprint_mismatch_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data["cards"][0]["locator"].update(fingerprint_sha256="0" * 64))
        with self.assertRaisesRegex(COMPILER.ContractError, "locator fingerprint"):
            COMPILER.compile_contract(root)

    def test_reviewed_source_revision_is_pinned(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        source = root / "00_THE_WELTANSCHAUUNG_ONE_SITTING.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "source revision changed"):
            COMPILER.compile_contract(root)

    def test_claim_requires_one_semantic_owner(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data["cards"][0].pop("semantic_owner_id"))
        with self.assertRaisesRegex(COMPILER.ContractError, "semantic_owner_id"):
            COMPILER.compile_contract(root)

    def test_supporting_owner_cannot_duplicate_semantic_owner(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        def mutate(data):
            data["cards"][0]["supporting_owner_ids"].append(data["cards"][0]["semantic_owner_id"])
        self.mutate_cards(root, mutate)
        with self.assertRaisesRegex(COMPILER.ContractError, "supporting owners"):
            COMPILER.compile_contract(root)

    def test_supporting_owner_ids_must_be_unique(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        def mutate(data):
            data["cards"][4]["supporting_owner_ids"] *= 2
        self.mutate_cards(root, mutate)
        with self.assertRaisesRegex(COMPILER.ContractError, "supporting owners"):
            COMPILER.compile_contract(root)

    def test_legacy_owner_ids_is_forbidden(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data["cards"][0].update(owner_ids=["K-1"]))
        with self.assertRaisesRegex(COMPILER.ContractError, "legacy owner_ids"):
            COMPILER.compile_contract(root)

    def test_v1_card_set_schema_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(root, lambda data: data.update(schema="emergentism/claim-card-set/v1"))
        with self.assertRaisesRegex(COMPILER.ContractError, "claim-card-set/v2"):
            COMPILER.compile_contract(root)

    def test_current_public_card_requires_review_receipt(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        def mutate(data):
            data["cards"][0]["review"] = {"state": "typed", "receipts": []}
        self.mutate_cards(root, mutate)
        with self.assertRaisesRegex(COMPILER.ContractError, "requires L2-or-later"):
            COMPILER.compile_contract(root)

    def test_declared_review_receipt_must_exist(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(
            root,
            lambda data: data["cards"][0]["review"].update(receipts=["00_META/missing-review.md"]),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "missing review receipt"):
            COMPILER.compile_contract(root)

    def test_review_receipt_direct_file_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-review.md"
        outside.write_text("outside review", encoding="utf-8")
        (root / "review-link.md").symlink_to(outside)
        self.mutate_cards(
            root,
            lambda data: data["cards"][0]["review"].update(
                receipts=["review-link.md"]
            ),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_review_receipt_parent_directory_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-review"
        outside.mkdir()
        (outside / "receipt.md").write_text("outside review", encoding="utf-8")
        (root / "review-custody").symlink_to(outside, target_is_directory=True)
        self.mutate_cards(
            root,
            lambda data: data["cards"][0]["review"].update(
                receipts=["review-custody/receipt.md"]
            ),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_source_cannot_self_attest_as_sole_l3_receipt(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        def mutate(data):
            data["cards"][0]["review"] = {
                "state": "l3_audited",
                "receipts": [data["source"]["path"]],
            }
        self.mutate_cards(root, mutate)
        with self.assertRaisesRegex(COMPILER.ContractError, "source cannot be the sole receipt"):
            COMPILER.compile_contract(root)

    def test_every_entering_chapter_requires_card_coverage(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][0]["chapter_order"].append("uncarded-chapter")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "chapters lack claim-card coverage"):
            COMPILER.compile_contract(root)

    def test_manifest_card_set_must_be_exact(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][0]["claim_card_ids"].remove("OS01-07")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "manifest claim-card set differs"):
            COMPILER.compile_contract(root)

    def test_manifest_card_ids_cannot_repeat(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][0]["claim_card_ids"].append("OS01-01")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "duplicate claim-card id in manifest"):
            COMPILER.compile_contract(root)

    def test_manifest_owners_are_derived_from_semantic_owners(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][0]["owner_ids"].append("K-6")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "semantic-owner projection"):
            COMPILER.compile_contract(root)

    def test_v1_book_manifest_schema_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["schema"] = "emergentism/book-manifest/v1"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "book-manifest/v2"):
            COMPILER.compile_contract(root)

    def test_historical_source_revision_is_pinned(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][1]["historical_sources"][0]["reviewed_source_sha256"] = "0" * 64
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "historical source revision changed"):
            COMPILER.compile_contract(root)

    def test_historical_source_requires_explicit_lifecycle(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][1]["historical_sources"][0].pop("lifecycle")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "historical_source.lifecycle"):
            COMPILER.compile_contract(root)

    def test_legacy_string_historical_source_requires_existing_claim_pin(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][1]["historical_sources"] = ["../legacy.md"]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(
            COMPILER.ContractError,
            "legacy string historical source lacks hash-bound claim-card custody",
        ):
            COMPILER.compile_contract(root)

    def test_manifest_lifecycle_inference_is_ordered_and_bounded(self) -> None:
        cases = {
            "legacy_and_frozen_projection": "frozen",
            "historical_readonly_projection": "legacy",
            "external_runtime_projection": "proposal",
            "proposal_projection": "proposal",
            "source_active_public_projection": "projection",
            "source_active_current_public_reader": "active",
        }
        for release_state, expected in cases.items():
            with self.subTest(release_state=release_state):
                self.assertEqual(
                    COMPILER._inferred_manifest_lifecycle(
                        {"release_state": release_state}
                    ),
                    expected,
                )

    def test_build_provenance_must_be_typed(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][0]["build_provenance"] = "ambiguous/path/or/prose"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "typed object"):
            COMPILER.compile_contract(root)

    def test_path_build_provenance_is_hash_pinned(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        artifact = root / "13_BOOKS/fixture.md"
        artifact.write_text("fixture\n", encoding="utf-8")
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][0]["build_provenance"] = {
            "type": "projection_artifact",
            "path": "fixture.md",
            "sha256": "0" * 64,
        }
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "build provenance revision changed"):
            COMPILER.compile_contract(root)

    def test_linked_worktree_fallback_is_external_only(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        primary = base / "Documents/01_EMERGENTISM"
        root = base / "worktrees/repair"
        gitdir = primary / ".git/worktrees/repair"
        gitdir.mkdir(parents=True)
        root.mkdir(parents=True)
        (root / ".git").write_text(f"gitdir: {gitdir}\n", encoding="utf-8")
        (gitdir / "commondir").write_text("../..\n", encoding="utf-8")
        external = base / "Documents/02_SKYZAI/provenance.md"
        external.parent.mkdir(parents=True)
        external.write_text("history", encoding="utf-8")
        (primary / "internal.md").parent.mkdir(parents=True, exist_ok=True)
        (primary / "internal.md").write_text("stale", encoding="utf-8")
        # CI intentionally exports a primary checkout for production custody.
        # This fixture supplies its own linked-worktree primary and must test
        # that contract independently of the caller's environment.
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                COMPILER._resolve_repo_path(root, Path("../02_SKYZAI/provenance.md")),
                external.resolve(),
            )
            self.assertEqual(
                COMPILER._resolve_repo_path(root, Path("internal.md")),
                (root / "internal.md").resolve(),
            )

    def test_external_path_cannot_escape_documents_federation(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        with self.assertRaisesRegex(
            COMPILER.ContractError,
            "external provenance must escape exactly once",
        ):
            COMPILER._resolve_repo_path(root, Path("../../../outside.md"))

    def test_graph_has_exactly_one_ownership_edge_per_claim(self) -> None:
        register, graph, _ = COMPILER.compile_contract(
            ROOT, allow_unavailable_external=True
        )
        owned = [edge for edge in graph["edges"] if edge["kind"] == "owned_by"]
        self.assertEqual(len(owned), register["metrics"]["cards"])
        self.assertEqual(len({edge["from"] for edge in owned}), register["metrics"]["cards"])

    def test_generated_contracts_contain_no_absolute_paths(self) -> None:
        outputs = COMPILER.compile_contract(ROOT, allow_unavailable_external=True)
        def walk(value):
            if isinstance(value, dict):
                for item in value.values(): yield from walk(item)
            elif isinstance(value, list):
                for item in value: yield from walk(item)
            elif isinstance(value, str):
                yield value
        self.assertFalse([value for output in outputs for value in walk(output) if value.startswith("/")])

    def test_zero_card_work_cannot_declare_chapters(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][1]["chapter_order"] = ["uncarded"]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "zero-card work"):
            COMPILER.compile_contract(root)

    def test_public_route_absolute_path_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "absolute-public.html"
        outside.write_text("outside public", encoding="utf-8")
        self.mutate_book_manifest(
            root,
            lambda manifest: manifest["works"][0].update(
                public_route=outside.as_posix()
            ),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "public route must be relative"):
            COMPILER.compile_contract(root)

    def test_public_route_must_exist_with_clear_failure(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_book_manifest(
            root,
            lambda manifest: manifest["works"][0].update(
                public_route="../12_PUBLIC_SITE/missing.html"
            ),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "missing public route"):
            COMPILER.compile_contract(root)

    def test_public_route_cannot_target_internal_nonpublic_file(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        (root / "internal.html").write_text("not public", encoding="utf-8")
        self.mutate_book_manifest(
            root,
            lambda manifest: manifest["works"][0].update(
                public_route="../internal.html"
            ),
        )
        with self.assertRaisesRegex(
            COMPILER.ContractError, "public route must remain inside 12_PUBLIC_SITE"
        ):
            COMPILER.compile_contract(root)

    def test_public_route_parent_traversal_escape_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-public.html"
        outside.write_text("outside public", encoding="utf-8")
        self.mutate_book_manifest(
            root,
            lambda manifest: manifest["works"][0].update(
                public_route="../../outside-public.html"
            ),
        )
        with self.assertRaisesRegex(
            COMPILER.ContractError, "public route traverses outside the corpus root"
        ):
            COMPILER.compile_contract(root)

    def test_public_route_direct_file_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-public.html"
        outside.write_text("outside public", encoding="utf-8")
        (root / "public-link.html").symlink_to(outside)
        self.mutate_book_manifest(
            root,
            lambda manifest: manifest["works"][0].update(
                public_route="../public-link.html"
            ),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_public_route_parent_directory_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-public"
        outside.mkdir()
        (outside / "index.html").write_text("outside public", encoding="utf-8")
        (root / "public-custody").symlink_to(outside, target_is_directory=True)
        self.mutate_book_manifest(
            root,
            lambda manifest: manifest["works"][0].update(
                public_route="../public-custody/index.html"
            ),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_composition_cannot_duplicate_primary_routes(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        component = copy.deepcopy(manifest["editorial_architecture"]["compositions"][0]["components"][0])
        manifest["editorial_architecture"]["compositions"][0]["components"].append(component)
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "exactly one primary"):
            COMPILER.compile_contract(root)

    def test_reference_only_route_does_not_count_as_primary_home(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["compositions"][0]["components"][0]["projection_mode"] = "reference_only"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "exactly one primary"):
            COMPILER.compile_contract(root)

    def test_composition_integrity_totals_are_derived(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["integrity"]["existing_claim_card_count"] = 27
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "integrity totals drifted"):
            COMPILER.compile_contract(root)

    def test_staged_architecture_is_data_driven_not_hardcoded_to_three_plus_one(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        removed = manifest["editorial_architecture"]["compositions"].pop()
        manifest["editorial_architecture"]["integrity"]["primary_cards_by_composition"].pop(
            removed["composition_id"]
        )
        path.write_text(json.dumps(manifest), encoding="utf-8")
        COMPILER.compile_contract(root)

    def test_composition_catalog_class_is_restricted(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["compositions"][1]["catalog_class"] = "extra_book"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "invalid catalog class"):
            COMPILER.compile_contract(root)

    def test_staged_architecture_cannot_claim_confirmation(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["confirmation"] = {
            "state": "confirmed",
            "receipt": "00_META/00_ONE_SITTING_CLAIM_CARD_SET_01.md",
            "receipt_sha256": "0" * 64,
        }
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "explicitly unconfirmed"):
            COMPILER.compile_contract(root)

    def test_confirmed_architecture_receipt_must_exist(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.confirm_architecture_with_receipt(
            root, "missing-confirmation.md", "0" * 64
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "missing confirmation receipt"):
            COMPILER.compile_contract(root)

    def test_architecture_confirmation_direct_file_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-confirmation.md"
        outside.write_text("outside confirmation", encoding="utf-8")
        (root / "confirmation-link.md").symlink_to(outside)
        self.confirm_architecture_with_receipt(
            root,
            "confirmation-link.md",
            hashlib.sha256(outside.read_bytes()).hexdigest(),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_architecture_confirmation_parent_directory_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-confirmation"
        outside.mkdir()
        receipt = outside / "receipt.md"
        receipt.write_text("outside confirmation", encoding="utf-8")
        (root / "confirmation-custody").symlink_to(
            outside, target_is_directory=True
        )
        self.confirm_architecture_with_receipt(
            root,
            "confirmation-custody/receipt.md",
            hashlib.sha256(receipt.read_bytes()).hexdigest(),
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_editorial_front_doors_keep_proposal_unconfirmed(self) -> None:
        manifest = json.loads(
            (ROOT / "13_BOOKS/book-manifest.json").read_text(encoding="utf-8")
        )
        architecture = manifest["editorial_architecture"]
        self.assertEqual(architecture["status"], "staged_proposal")
        self.assertEqual(architecture["confirmation"]["state"], "unconfirmed")
        for relative in (
            "13_BOOKS/README.md",
            "13_BOOKS/00_CATALOG.md",
            "13_BOOKS/01_THREE_BOOK_ARCHITECTURE.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8").lower()
            self.assertIn("proposal", text, relative)
            self.assertIn("unconfirmed", text, relative)

    def test_historical_reader_components_are_reference_only(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["compositions"][3]["components"].append({
            "work_id": "BK-ONE-SITTING", "claim_selection": "all", "projection_mode": "primary",
        })
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "historical-reader components must be reference_only"):
            COMPILER.compile_contract(root)

    def test_nonbook_primary_home_is_restricted(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["nonbook_claim_routes"].append({
            "route_id": "BAD-ROUTE", "work_id": "BK-ONE-SITTING",
            "claim_selection": "all", "primary_home": "arbitrary_home",
        })
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "invalid primary_home"):
            COMPILER.compile_contract(root)

    def test_nonbook_route_ids_are_unique(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        route = {
            "route_id": "DUPLICATE", "work_id": "BK-LEGACY-FIXTURE",
            "claim_card_ids": [], "primary_home": "historical_custody_only",
        }
        manifest["editorial_architecture"]["nonbook_claim_routes"] = [route, copy.deepcopy(route)]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "duplicate nonbook route id"):
            COMPILER.compile_contract(root)

    def test_edition_disposition_is_restricted(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["edition_dispositions"][0][
            "existing_edition_disposition"
        ] = "silently_deleted"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "invalid edition disposition"):
            COMPILER.compile_contract(root)

    def test_supersession_requires_successor_and_gate_receipt(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["edition_dispositions"][0][
            "existing_edition_disposition"
        ] = "superseded_by_successor"
        manifest["editorial_architecture"]["edition_dispositions"][0].update(
            successor_path="missing-successor.md", gate_receipt="missing-gate.md"
        )
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "requires an existing successor"):
            COMPILER.compile_contract(root)

    def test_supersession_successor_absolute_path_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-successor.md"
        outside.write_text("outside successor", encoding="utf-8")
        _, receipt = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(root, outside.as_posix(), receipt)
        with self.assertRaisesRegex(
            COMPILER.ContractError, "successor_path must be relative"
        ):
            COMPILER.compile_contract(root)

    def test_supersession_successor_parent_traversal_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-successor.md"
        outside.write_text("outside successor", encoding="utf-8")
        _, receipt = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(root, "../outside-successor.md", receipt)
        with self.assertRaisesRegex(
            COMPILER.ContractError, "successor_path must be root-relative without parent traversal"
        ):
            COMPILER.compile_contract(root)

    def test_supersession_successor_direct_file_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-successor.md"
        outside.write_text("outside successor", encoding="utf-8")
        successor = root / "successor-link.md"
        successor.symlink_to(outside)
        _, receipt = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(root, successor.name, receipt)
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_supersession_successor_parent_directory_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-successor"
        outside.mkdir()
        (outside / "successor.md").write_text("outside successor", encoding="utf-8")
        (root / "successor-custody").symlink_to(
            outside, target_is_directory=True
        )
        _, receipt = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(
            root, "successor-custody/successor.md", receipt
        )
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_supersession_gate_receipt_absolute_path_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-gate.md"
        outside.write_text("outside gate", encoding="utf-8")
        successor, _ = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(root, successor, outside.as_posix())
        with self.assertRaisesRegex(
            COMPILER.ContractError, "gate_receipt must be relative"
        ):
            COMPILER.compile_contract(root)

    def test_supersession_gate_receipt_parent_traversal_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-gate.md"
        outside.write_text("outside gate", encoding="utf-8")
        successor, _ = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(root, successor, "../outside-gate.md")
        with self.assertRaisesRegex(
            COMPILER.ContractError, "gate_receipt must be root-relative without parent traversal"
        ):
            COMPILER.compile_contract(root)

    def test_supersession_gate_receipt_direct_file_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-gate.md"
        outside.write_text("outside gate", encoding="utf-8")
        gate = root / "gate-link.md"
        gate.symlink_to(outside)
        successor, _ = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(root, successor, gate.name)
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_supersession_gate_receipt_parent_directory_symlink_fails(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        outside = Path(temp.name) / "outside-gate"
        outside.mkdir()
        (outside / "receipt.md").write_text("outside gate", encoding="utf-8")
        (root / "gate-custody").symlink_to(outside, target_is_directory=True)
        successor, _ = self.write_supersession_fixture_files(root)
        self.supersede_first_edition(root, successor, "gate-custody/receipt.md")
        with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
            COMPILER.compile_contract(root)

    def test_reference_module_requires_reference_only_mode(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["editorial_architecture"]["compositions"][1]["reference_modules"] = [{
            "path": "../00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "projection_mode": "primary",
        }]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "reference modules must declare"):
            COMPILER.compile_contract(root)

    def test_uncarded_source_module_blocks_built_output(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        composition = manifest["editorial_architecture"]["compositions"][1]
        composition["output"]["state"] = "built_private"
        composition["source_modules"] = [{
            "path": "../legacy.md",
            "coverage_state": "uncarded", "claim_card_ids": [],
        }]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "cannot promote output with uncarded"):
            COMPILER.compile_contract(root)

    def test_source_module_reverse_coverage_detects_hidden_cards(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        composition = manifest["editorial_architecture"]["compositions"][0]
        composition["source_modules"] = [{
            "path": "../00_THE_WELTANSCHAUUNG_ONE_SITTING.md",
            "coverage_state": "uncarded",
            "claim_card_ids": [],
        }]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "module coverage differs"):
            COMPILER.compile_contract(root)

    def test_generated_register_exposes_exactly_one_projection_home(self) -> None:
        register, graph, _ = COMPILER.compile_contract(
            ROOT, allow_unavailable_external=True
        )
        self.assertEqual(len(register["cards"]), 72)
        self.assertTrue(all(row.get("primary_projection_home") for row in register["cards"]))
        self.assertTrue(all(row.get("projection_kind") for row in register["cards"]))
        self.assertEqual(len(graph["composition_summaries"]), 4)
        projected = [edge for edge in graph["edges"] if edge["kind"] == "projected_to"]
        self.assertEqual(len(projected), 72)

    def test_zero_card_legacy_source_is_in_inventory(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        _, _, lifecycle = COMPILER.compile_contract(root)
        legacy = [row for row in lifecycle["sources"] if row["work_id"] == "BK-LEGACY-FIXTURE"]
        self.assertEqual(len(legacy), 1)
        self.assertEqual(legacy[0]["lifecycle"], "legacy")

    def test_lifecycle_inventory_contains_no_absolute_paths(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        _, _, lifecycle = COMPILER.compile_contract(root)
        self.assertTrue(lifecycle["sources"])
        for source in lifecycle["sources"]:
            self.assertNotIn("resolved_path", source)
            self.assertFalse(Path(source["path"]).is_absolute())

    def test_standalone_does_not_discover_arbitrary_sibling(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        federation = Path(temp.name) / "Documents"
        worktree = federation / ".codex-worktrees/emergentism"
        source = federation / "02_SKYZAI/source.md"
        worktree.mkdir(parents=True)
        source.parent.mkdir(parents=True)
        source.write_text("federated source", encoding="utf-8")

        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                COMPILER.UnresolvedDeclaredPathError,
                "unresolved declared path",
            ):
                COMPILER._resolve_declared_path(
                    worktree,
                    worktree,
                    Path("../02_SKYZAI/source.md"),
                )

    def test_standalone_clone_resolves_explicit_primary_checkout(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        standalone = base / "standalone/emergentism"
        primary = base / "Documents/01_EMERGENTISM"
        source = base / "Documents/02_SKYZAI/source.md"
        standalone.mkdir(parents=True)
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        source.parent.mkdir(parents=True)
        source.write_text("hash-bound sibling source", encoding="utf-8")

        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            resolved = COMPILER._resolve_declared_path(
                standalone,
                standalone,
                Path("../02_SKYZAI/source.md"),
            )
        self.assertEqual(resolved, source.resolve())

    def test_hash_bound_relocation_prefers_unique_longest_suffix(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        standalone = base / "standalone/emergentism"
        primary = base / "Documents/01_EMERGENTISM"
        preferred = base / "Documents/02_SKYZAI/new/old/tree/frozen.md"
        export = base / "Documents/02_SKYZAI/export/frozen.md"
        standalone.mkdir(parents=True)
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        preferred.parent.mkdir(parents=True)
        export.parent.mkdir(parents=True)
        preferred.write_text("same frozen bytes", encoding="utf-8")
        export.write_text("same frozen bytes", encoding="utf-8")
        expected = hashlib.sha256(b"same frozen bytes").hexdigest()

        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            resolved = COMPILER._resolve_hash_bound_relocation(
                standalone,
                Path("../02_SKYZAI/old/tree/frozen.md"),
                expected,
            )
        self.assertEqual(resolved, (preferred.resolve(), 2))

    def test_explicit_current_checkout_enables_hash_bound_relocation(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        federation = Path(temp.name) / "Documents"
        primary = federation / "01_EMERGENTISM"
        relocated = federation / "02_SKYZAI/new/tree/frozen.md"
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        relocated.parent.mkdir(parents=True)
        relocated.write_text("pinned CI bytes", encoding="utf-8")
        expected = hashlib.sha256(b"pinned CI bytes").hexdigest()

        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            resolved = COMPILER._resolve_hash_bound_relocation(
                primary,
                Path("../02_SKYZAI/old/tree/frozen.md"),
                expected,
            )
        self.assertEqual(resolved, (relocated.resolve(), 1))

    def test_hash_bound_relocation_rejects_equally_specific_custody(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        standalone = base / "standalone/emergentism"
        primary = base / "Documents/01_EMERGENTISM"
        first = base / "Documents/02_SKYZAI/a/old/tree/frozen.md"
        second = base / "Documents/02_SKYZAI/b/old/tree/frozen.md"
        standalone.mkdir(parents=True)
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        first.parent.mkdir(parents=True)
        second.parent.mkdir(parents=True)
        first.write_text("same frozen bytes", encoding="utf-8")
        second.write_text("same frozen bytes", encoding="utf-8")
        expected = hashlib.sha256(b"same frozen bytes").hexdigest()

        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            with self.assertRaisesRegex(
                COMPILER.AmbiguousDeclaredPathError,
                "multiple equally specific custody paths",
            ):
                COMPILER._resolve_hash_bound_relocation(
                    standalone,
                    Path("../02_SKYZAI/old/tree/frozen.md"),
                    expected,
                )

    def test_configured_federation_does_not_bypass_source_hash(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        primary = base / "Documents/01_EMERGENTISM"
        source = base / (
            "Documents/02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/"
            "01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/"
            "09_BOOK_PRODUCTION_ARCHIVE/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/"
            "07_PUBLIC_EDITION/"
            "THE_RECIPROCAL_PUBLIC_EDITION_K2_LANG_DECOMM_2026_07_22.md"
        )
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        source.parent.mkdir(parents=True)
        source.write_text("wrong bytes", encoding="utf-8")

        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            with self.assertRaisesRegex(COMPILER.ContractError, "source revision changed"):
                COMPILER.compile_contract(ROOT, allow_unavailable_external=True)

    def test_missing_frozen_custody_has_explicit_non_skip_diagnostic(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                COMPILER.FrozenSourceUnavailableError,
                "hash-bound frozen source unavailable.*validation was not skipped",
            ):
                COMPILER.compile_contract(ROOT, allow_unavailable_external=False)

    def test_metadata_only_mode_rejects_unregistered_external_source(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.mutate_cards(
            root,
            lambda data: data["source"].update(
                path="../02_SKYZAI/unreviewed.md",
                lifecycle="frozen",
                reviewed_source_sha256="0" * 64,
            ),
        )
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                COMPILER.ContractError,
                "not in the reviewed metadata-only inventory",
            ):
                COMPILER.compile_contract(root, allow_unavailable_external=True)

    def test_metadata_only_mode_rejects_external_huge_locator_range(self) -> None:
        self.assert_external_locator_inventory_mutation_fails(
            lambda locator: locator.update(line_end=locator["line_end"] + 1_000_000)
        )

    def test_metadata_only_mode_rejects_external_locator_anchor_drift(self) -> None:
        self.assert_external_locator_inventory_mutation_fails(
            lambda locator: locator.update(anchor="arbitrary unavailable-source anchor")
        )

    def test_metadata_only_mode_rejects_external_locator_fingerprint_drift(self) -> None:
        self.assert_external_locator_inventory_mutation_fails(
            lambda locator: locator.update(fingerprint_sha256="0" * 64)
        )

    def test_metadata_only_mode_joins_legacy_external_strings(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            _, _, lifecycle = COMPILER.compile_contract(
                ROOT, allow_unavailable_external=True
            )
        external = {
            row["path"]: row
            for row in lifecycle["sources"]
            if row["external_readonly"]
        }
        self.assertEqual(set(external), set(COMPILER.EXTERNAL_SOURCE_CONTRACTS))
        for path, contract in COMPILER.EXTERNAL_SOURCE_CONTRACTS.items():
            self.assertEqual(external[path]["sha256"], contract[0])
            self.assertEqual(external[path]["lifecycle"], contract[1])
            self.assertEqual(
                external[path]["byte_validation"],
                "exact_sha256_when_authorized_federation_available; "
                "explicit_unavailable_mode_validates_metadata_only",
            )

    def test_unavailable_external_environment_requires_exact_boolean(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        with mock.patch.dict(
            os.environ,
            {COMPILER.ALLOW_UNAVAILABLE_EXTERNAL_ENV: "yes"},
            clear=True,
        ):
            with self.assertRaisesRegex(COMPILER.ContractError, "exactly 0 or 1"):
                COMPILER.compile_contract(root)

    def test_direct_repository_source_resolves_uniquely(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "corpus"
        source = root / "owned/source.md"
        source.parent.mkdir(parents=True)
        source.write_text("owned source", encoding="utf-8")

        resolved = COMPILER._resolve_declared_path(
            root,
            root,
            Path("owned/source.md"),
        )
        self.assertEqual(resolved, source.resolve())

    def test_internal_source_file_symlink_escape_fails(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        root = base / "corpus"
        outside = base / "outside.md"
        root.mkdir()
        outside.write_text("outside", encoding="utf-8")
        (root / "source.md").symlink_to(outside)
        for resolver in (
            lambda: COMPILER._resolve_repo_path(root, Path("source.md")),
            lambda: COMPILER._resolve_declared_path(root, root, Path("source.md")),
        ):
            with self.subTest(resolver=resolver):
                with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
                    resolver()

    def test_internal_source_directory_symlink_escape_fails(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        root = base / "corpus"
        outside = base / "outside"
        root.mkdir()
        outside.mkdir()
        (outside / "source.md").write_text("outside", encoding="utf-8")
        (root / "linked").symlink_to(outside, target_is_directory=True)
        for resolver in (
            lambda: COMPILER._resolve_repo_path(root, Path("linked/source.md")),
            lambda: COMPILER._resolve_declared_path(
                root, root, Path("linked/source.md")
            ),
        ):
            with self.subTest(resolver=resolver):
                with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
                    resolver()

    def test_external_declared_source_symlink_escape_fails(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        federation = Path(temp.name) / "Documents"
        primary = federation / "01_EMERGENTISM"
        outside = Path(temp.name) / "outside.md"
        source = federation / "02_SKYZAI/path/source.md"
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        outside.write_text("outside", encoding="utf-8")
        source.parent.mkdir(parents=True)
        source.symlink_to(outside)
        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
                COMPILER._resolve_declared_path(
                    primary, primary, Path("../02_SKYZAI/path/source.md")
                )

    def test_external_source_directory_symlink_escape_fails(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        federation = Path(temp.name) / "Documents"
        primary = federation / "01_EMERGENTISM"
        outside = Path(temp.name) / "outside"
        pillar = federation / "02_SKYZAI"
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        outside.mkdir()
        (outside / "source.md").write_text("outside", encoding="utf-8")
        pillar.mkdir()
        (pillar / "linked").symlink_to(outside, target_is_directory=True)
        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            with self.assertRaisesRegex(COMPILER.ContractError, "symlink component"):
                COMPILER._resolve_declared_path(
                    primary, primary, Path("../02_SKYZAI/linked/source.md")
                )

    def test_configured_primary_checkout_symlink_fails(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        primary = base / "real/01_EMERGENTISM"
        linked = base / "linked-emergentism"
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        linked.symlink_to(primary, target_is_directory=True)
        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: linked.as_posix()},
            clear=True,
        ):
            with self.assertRaisesRegex(COMPILER.ContractError, "may not be a symlink"):
                COMPILER._configured_primary_checkout_root()

    def test_hash_bound_relocation_rejects_symlink_candidate(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        federation = Path(temp.name) / "Documents"
        primary = federation / "01_EMERGENTISM"
        outside = Path(temp.name) / "frozen.md"
        source = federation / "02_SKYZAI/relocated/frozen.md"
        primary.mkdir(parents=True)
        (primary / "AGENTS.md").write_text("route", encoding="utf-8")
        (primary / "00_THE_KERNEL_INDEX.md").write_text("kernel", encoding="utf-8")
        outside.write_text("same bytes", encoding="utf-8")
        source.parent.mkdir(parents=True)
        source.symlink_to(outside)
        expected = hashlib.sha256(b"same bytes").hexdigest()
        with mock.patch.dict(
            os.environ,
            {COMPILER.PRIMARY_CHECKOUT_ENV: primary.as_posix()},
            clear=True,
        ):
            with self.assertRaisesRegex(COMPILER.ContractError, "rejects symlink source"):
                COMPILER._resolve_hash_bound_relocation(
                    primary,
                    Path("../02_SKYZAI/old/frozen.md"),
                    expected,
                )

    def test_parent_relative_source_never_scans_ancestors(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        temp_root = Path(temp.name)
        federation = temp_root / "Documents"
        worktree = federation / ".codex-worktrees/emergentism"
        nearest = federation / "02_SKYZAI/source.md"
        farther = temp_root / "02_SKYZAI/source.md"
        worktree.mkdir(parents=True)
        nearest.parent.mkdir(parents=True)
        farther.parent.mkdir(parents=True)
        nearest.write_text("nearest candidate", encoding="utf-8")
        farther.write_text("farther candidate", encoding="utf-8")

        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                COMPILER.UnresolvedDeclaredPathError,
                "unresolved declared path",
            ):
                COMPILER._resolve_declared_path(
                    worktree,
                    worktree,
                    Path("../02_SKYZAI/source.md"),
                )

    def test_unresolved_declared_path_fails_explicitly(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "corpus"
        root.mkdir()

        with self.assertRaisesRegex(
            COMPILER.UnresolvedDeclaredPathError,
            "unresolved declared path",
        ):
            COMPILER._resolve_declared_path(
                root,
                root,
                Path("missing/source.md"),
            )


if __name__ == "__main__":
    unittest.main()
