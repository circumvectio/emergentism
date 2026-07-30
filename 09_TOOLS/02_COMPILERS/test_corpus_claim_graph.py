from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = Path(__file__).with_name("compile_claim_cards.py")
SPEC = importlib.util.spec_from_file_location("compile_claim_cards", MODULE_PATH)
assert SPEC and SPEC.loader
COMPILER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPILER)


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

    def test_repository_contract_compiles(self) -> None:
        register, graph, lifecycle = COMPILER.compile_contract(ROOT)
        self.assertEqual(register["schema"], "emergentism/claim-card-register/v2")
        self.assertEqual(graph["schema"], "emergentism/claim-owner-dependency-graph/v2")
        self.assertEqual(lifecycle["schema"], "emergentism/claim-lifecycle-inventory/v3")
        self.assertEqual(register["metrics"]["cards"], 72)
        self.assertEqual(register["metrics"]["works_with_cards"], 9)
        self.assertEqual({row["owner_id"] for row in register["owners"]}, {f"K-{i}" for i in range(1, 8)})
        self.assertGreater(graph["metrics"]["edges"], 300)
        self.assertEqual(lifecycle["baseline"]["tracked_files"], 3205)

    def test_deterministic_generation(self) -> None:
        first = COMPILER.compile_contract(ROOT)
        second = COMPILER.compile_contract(ROOT)
        self.assertEqual([COMPILER._canonical_bytes(x) for x in first], [COMPILER._canonical_bytes(x) for x in second])

    def test_check_detects_deliberate_drift(self) -> None:
        temp, root = self.make_fixture()
        self.addCleanup(temp.cleanup)
        outputs = COMPILER.compile_contract(root)
        COMPILER.write_outputs(root, outputs)
        self.assertEqual(COMPILER.check_outputs(root, outputs), [])
        (root / COMPILER.REGISTER_PATH).write_text("{}\n", encoding="utf-8")
        self.assertTrue(COMPILER.check_outputs(root, outputs))

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
        external = base / "Documents/02_EXTERNAL/provenance.md"
        external.parent.mkdir(parents=True)
        external.write_text("history", encoding="utf-8")
        (primary / "internal.md").parent.mkdir(parents=True, exist_ok=True)
        (primary / "internal.md").write_text("stale", encoding="utf-8")
        self.assertEqual(
            COMPILER._resolve_repo_path(root, Path("../02_EXTERNAL/provenance.md")),
            external.resolve(),
        )
        self.assertEqual(
            COMPILER._resolve_repo_path(root, Path("internal.md")),
            (root / "internal.md").resolve(),
        )

    def test_external_path_cannot_escape_documents_federation(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        with self.assertRaisesRegex(COMPILER.ContractError, "escapes the Documents federation"):
            COMPILER._resolve_repo_path(root, Path("../../../outside.md"))

    def test_graph_has_exactly_one_ownership_edge_per_claim(self) -> None:
        register, graph, _ = COMPILER.compile_contract(ROOT)
        owned = [edge for edge in graph["edges"] if edge["kind"] == "owned_by"]
        self.assertEqual(len(owned), register["metrics"]["cards"])
        self.assertEqual(len({edge["from"] for edge in owned}), register["metrics"]["cards"])

    def test_generated_contracts_contain_no_absolute_paths(self) -> None:
        outputs = COMPILER.compile_contract(ROOT)
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
        register, graph, _ = COMPILER.compile_contract(ROOT)
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

    def test_lifecycle_inventory_deduplicates_physical_sources(self) -> None:
        _, _, lifecycle = COMPILER.compile_contract(ROOT)
        paths = [row["path"] for row in lifecycle["sources"]]
        self.assertEqual(len(paths), len(set(paths)))
        lived_compass = [
            row for row in lifecycle["sources"]
            if row["path"] == "01_TELEOLOGY/04_THE_LIVED_COMPASS.md"
        ]
        self.assertEqual(len(lived_compass), 1)
        self.assertEqual(lived_compass[0]["lifecycle"], "active")
        self.assertEqual(
            lived_compass[0]["roles"], ["historical_source", "practical_source_owner"]
        )

    def test_translation_conjecture_depends_on_separate_native_primacy_vow(self) -> None:
        register, _, _ = COMPILER.compile_contract(ROOT)
        rows = {row["card_id"]: row for row in register["cards"]}
        self.assertEqual(rows["RIP01-03"]["semantic_owner_id"], "K-1")
        self.assertEqual(rows["OS01-12"]["semantic_owner_id"], "K-4")
        self.assertIn("RIP01-03", rows["OS01-12"]["dependency_ids"])
        cards = json.loads(
            (ROOT / "00_META/claim_cards/one_sitting.yaml").read_text(encoding="utf-8")
        )["cards"]
        os12 = next(card for card in cards if card["card_id"] == "OS01-12")
        self.assertNotIn("native objects, mechanisms, equations and evidence remain primary", os12["plain_claim"])


if __name__ == "__main__":
    unittest.main()
