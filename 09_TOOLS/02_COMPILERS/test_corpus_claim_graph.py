from __future__ import annotations

import copy
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


def missing_federated_sources() -> list[str]:
    """Return declared claim-card sources unavailable beside this checkout.

    The repository contract includes frozen lineage in sibling pillar repos.
    Unit fixtures remain self-contained; only the two full-repository
    integration checks require the complete Documents federation.
    """
    missing: list[str] = []
    for path in sorted((ROOT / COMPILER.CARD_DIR).glob("*.yaml")):
        document = json.loads(path.read_text(encoding="utf-8"))
        source = document.get("source", {})
        source_rel = source.get("path")
        if isinstance(source_rel, str):
            try:
                COMPILER._resolve_declared_path(ROOT, ROOT, Path(source_rel))
            except COMPILER.UnresolvedDeclaredPathError:
                missing.append(source_rel)
    return missing


FEDERATED_SOURCE_GAPS = missing_federated_sources()
REPOSITORY_CONTRACT_SKIP = (
    "complete Documents federation not present; missing declared source(s): "
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
        (root / "13_BOOKS").mkdir(parents=True)
        (root / "12_PUBLIC_SITE/book").mkdir(parents=True)
        (root / "12_PUBLIC_SITE/book/index.html").write_text("book", encoding="utf-8")
        (root / "legacy.md").write_text("legacy", encoding="utf-8")
        manifest = json.loads((ROOT / "13_BOOKS/book-manifest.json").read_text(encoding="utf-8"))
        active = copy.deepcopy(manifest["works"][0])
        legacy = {
            "work_id": "BK-LEGACY-FIXTURE", "title": "Legacy fixture", "edition": "historical",
            "historical_sources": ["../legacy.md"], "chapter_order": [], "owner_ids": [],
            "claim_card_ids": [], "release_state": "historical_readonly_debrief_open",
            "public_route": None, "build_provenance": "not_built"
        }
        (root / "13_BOOKS/book-manifest.json").write_text(
            json.dumps({"schema": "emergentism/book-manifest/v1", "works": [active, legacy]}),
            encoding="utf-8",
        )
        return temp, root

    def mutate_cards(self, root: Path, fn) -> None:
        path = root / "00_META/claim_cards/one_sitting.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        fn(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    @unittest.skipIf(FEDERATED_SOURCE_GAPS, REPOSITORY_CONTRACT_SKIP)
    def test_repository_contract_compiles(self) -> None:
        register, graph, lifecycle = COMPILER.compile_contract(ROOT)
        self.assertEqual(register["metrics"]["cards"], 71)
        self.assertEqual(register["metrics"]["works_with_cards"], 9)
        self.assertEqual({row["owner_id"] for row in register["owners"]}, {f"K-{i}" for i in range(1, 8)})
        self.assertGreater(graph["metrics"]["edges"], 100)
        self.assertEqual(lifecycle["baseline"]["tracked_files"], 3205)

    @unittest.skipIf(FEDERATED_SOURCE_GAPS, REPOSITORY_CONTRACT_SKIP)
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

    def test_every_entering_chapter_requires_card_coverage(self) -> None:
        temp, root = self.make_fixture(); self.addCleanup(temp.cleanup)
        path = root / "13_BOOKS/book-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["works"][0]["claim_card_ids"] = ["OS01-01"]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(COMPILER.ContractError, "chapters lack claim-card coverage"):
            COMPILER.compile_contract(root)

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

    def test_parent_relative_source_resolves_unique_nearest_ancestor(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        federation = Path(temp.name) / "Documents"
        worktree = federation / ".codex-worktrees/emergentism"
        source = federation / "02_SIBLING/source.md"
        worktree.mkdir(parents=True)
        source.parent.mkdir(parents=True)
        source.write_text("federated source", encoding="utf-8")

        resolved = COMPILER._resolve_declared_path(
            worktree,
            worktree,
            Path("../02_SIBLING/source.md"),
        )
        self.assertEqual(resolved, source.resolve())

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

    def test_parent_relative_source_rejects_ambiguous_ancestors(self) -> None:
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        temp_root = Path(temp.name)
        federation = temp_root / "Documents"
        worktree = federation / ".codex-worktrees/emergentism"
        nearest = federation / "02_SIBLING/source.md"
        farther = temp_root / "02_SIBLING/source.md"
        worktree.mkdir(parents=True)
        nearest.parent.mkdir(parents=True)
        farther.parent.mkdir(parents=True)
        nearest.write_text("nearest candidate", encoding="utf-8")
        farther.write_text("farther candidate", encoding="utf-8")

        with self.assertRaisesRegex(
            COMPILER.AmbiguousDeclaredPathError,
            "multiple owner candidates resolve",
        ) as raised:
            COMPILER._resolve_declared_path(
                worktree,
                worktree,
                Path("../02_SIBLING/source.md"),
            )
        message = str(raised.exception)
        self.assertIn(nearest.resolve().as_posix(), message)
        self.assertIn(farther.resolve().as_posix(), message)

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
