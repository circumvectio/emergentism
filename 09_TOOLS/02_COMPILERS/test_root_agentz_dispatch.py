from __future__ import annotations

import copy
import hashlib
import importlib.util
import re
import shutil
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_root_agentz_dispatch as sync
import validate_agentz_rosetta as contract


class RootAgentzDispatchCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.specs = sync.load_validated_specs()
        cls.by_level = {spec["metadata"]["level"]: spec for spec in cls.specs}
        cls.outputs = sync.render_kernel()
        cls.source_bundle_sha256 = sync.source_bundle_digest()
        cls.output_sha256 = sync.output_digest(cls.outputs)

    def make_target(self, root: Path) -> Path:
        return root / ".codex/agents"

    def write_fresh(
        self,
        target: Path,
        outputs: dict[Path, bytes] | None = None,
        source_root: Path = sync.SOURCE_ROOT,
    ) -> str:
        rendered = outputs or sync.render_kernel(source_root)
        before = sync.preimage_digest(target)
        return sync.write_kernel(
            target,
            rendered,
            before,
            sync.source_bundle_digest(source_root),
            sync.output_digest(rendered),
            source_root,
        )

    def copy_source_bundle(self, destination: Path) -> None:
        for relative_path in sync.SOURCE_BUNDLE_PATHS:
            source = sync.SOURCE_ROOT / relative_path
            target = destination / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    def test_exact_thirteen_file_kernel_and_cx_exclusion(self) -> None:
        self.assertEqual(13, len(self.outputs))
        self.assertEqual(set(sync.KERNEL_PATHS), set(self.outputs))
        self.assertFalse(any("cx_suite" in path.parts for path in self.outputs))

    def test_render_is_byte_deterministic(self) -> None:
        first = sync.render_kernel()
        second = sync.render_kernel()
        self.assertEqual(first, second)
        for path in sync.KERNEL_PATHS:
            self.assertEqual(hashlib.sha256(first[path]).digest(), hashlib.sha256(second[path]).digest())

    def test_complete_source_bundle_is_bound_and_each_member_moves_digest(self) -> None:
        self.assertEqual(13, len(sync.SOURCE_BUNDLE_PATHS))
        with tempfile.TemporaryDirectory() as temporary:
            source_root = Path(temporary)
            self.copy_source_bundle(source_root)
            baseline = sync.source_bundle_digest(source_root)
            for relative_path in sync.SOURCE_BUNDLE_PATHS:
                path = source_root / relative_path
                original = path.read_bytes()
                path.write_bytes(original + b"\nsource-drift-fixture\n")
                self.assertNotEqual(baseline, sync.source_bundle_digest(source_root))
                path.write_bytes(original)

    def test_every_output_file_moves_output_digest(self) -> None:
        for path in sync.KERNEL_PATHS:
            changed = copy.deepcopy(self.outputs)
            changed[path] += b"\noutput-drift-fixture\n"
            self.assertNotEqual(self.output_sha256, sync.output_digest(changed))

    def test_source_snapshot_change_fails_closed(self) -> None:
        real_snapshot = sync._source_bundle_snapshot
        calls = 0

        def drifting_snapshot(source_root: Path) -> tuple[str, dict[str, str]]:
            nonlocal calls
            calls += 1
            digest, hashes = real_snapshot(source_root)
            if calls == 2:
                digest = "0" * 64
            return digest, hashes

        with mock.patch.object(sync, "_source_bundle_snapshot", side_effect=drifting_snapshot):
            with self.assertRaisesRegex(sync.SyncError, "source/control bundle changed"):
                sync.render_kernel()

    def test_schema_uses_route_select_and_typed_four_plus_three(self) -> None:
        schema = tomllib.loads(self.outputs[Path("rosetta_dispatch_schema.toml")].decode("utf-8"))
        self.assertEqual(
            ["PARSE", "ROUTE_SELECT", "DRAFT", "LINT", "GROUND"],
            schema["dispatch"]["sequence"],
        )
        self.assertNotIn("GOD_SELECT", schema["dispatch"]["sequence"])
        self.assertFalse(schema["meta"]["cx_suite_loaded"])
        operational = [row["level"] for row in schema["agents"] if row["operational_move"]]
        boundaries = [row["level"] for row in schema["agents"] if not row["operational_move"]]
        self.assertEqual(["L1", "L2", "L3", "L4"], operational)
        self.assertEqual(["L5", "L6", "L7"], boundaries)
        self.assertEqual("D4 actual carriers do", schema["typing"]["rule"].split("; only ")[-1])

    def test_rows_are_exact_typed_projections(self) -> None:
        for level, path in sync.ROW_PATHS.items():
            row = tomllib.loads(self.outputs[path].decode("utf-8"))
            source_meta = self.by_level[level]["metadata"]
            self.assertTrue(contract.REQUIRED_METADATA.issubset(row["meta"]))
            for key in contract.REQUIRED_METADATA:
                self.assertEqual(str(source_meta[key]), row["meta"][key])
            self.assertEqual(level in {"L1", "L2", "L3", "L4"}, row["dispatch"]["operational_move"])
            if level == "L4":
                self.assertEqual(["write", "edit", "bash"], row["tools"]["mutating"])
                self.assertEqual(
                    "write=always_ask,edit=always_ask,bash=always_ask",
                    row["tools"]["permission_policy"],
                )
                self.assertEqual(list(sync.AUTHORIZATION_FIELDS), row["authorization"]["required_fields"])
                self.assertEqual("required_for_attempted_L4_action", row["receipts"]["commitment_receipt"])
            else:
                self.assertEqual([], row["tools"]["mutating"])
                self.assertEqual("no_mutating_tools", row["tools"]["permission_policy"])
                self.assertEqual([], row["authorization"]["required_fields"])
                self.assertEqual(
                    "not_applicable_no_consequential_action",
                    row["authorization"]["private_dav_rail"],
                )
            self.assertEqual("returned_separately_by_environment", row["receipts"]["outcome_receipt"])
            self.assertFalse(row["receipts"]["selector_may_manufacture_outcome"])

    def test_receipt_based_analogy_is_not_identity_or_authority(self) -> None:
        for path in sync.ROW_PATHS.values():
            row = tomllib.loads(self.outputs[path].decode("utf-8"))
            identity = " ".join(
                [row["meta"]["name"], row["meta"]["description"], row["meta"]["operator"]]
            ).lower()
            self.assertNotIn("god", identity)
            self.assertNotIn("demon", identity)
            analogy = row["consequence_analogy"]
            self.assertEqual("unclassified", analogy["classification_default"])
            self.assertEqual(sync.CLASSIFICATION_GATE, analogy["classification_gate"])
            self.assertIn(
                "distinct hash-pinned trusted world-issuer key",
                analogy["classification_gate"],
            )
            self.assertEqual(sync.DEMON_BEARING_PREDICATE, analogy["demon_bearing"])
            self.assertEqual(sync.GOD_BEARING_PREDICATE, analogy["god_bearing"])
            self.assertEqual(sync.STASIS_PREDICATE, analogy["stasis"])
            self.assertEqual(sync.STRICT_SYNTROPY_PREDICATE, analogy["strict_syntropy"])
            self.assertIn("stronger subset", analogy["strict_syntropy_relation"])
            self.assertEqual("none", analogy["identity_effect"])
            self.assertEqual("none", analogy["authorization_effect"])

        schema = tomllib.loads(
            self.outputs[Path("rosetta_dispatch_schema.toml")].decode("utf-8")
        )["consequence_analogy"]
        self.assertEqual("unclassified", schema["classification_default"])
        self.assertEqual(sync.CLASSIFICATION_GATE, schema["classification_gate"])
        self.assertEqual(sync.DEMON_BEARING_PREDICATE, schema["demon_bearing"])
        self.assertEqual(sync.GOD_BEARING_PREDICATE, schema["god_bearing"])
        self.assertEqual(sync.STASIS_PREDICATE, schema["stasis"])
        self.assertEqual(sync.STRICT_SYNTROPY_PREDICATE, schema["strict_syntropy"])
        self.assertFalse(schema["identity_or_authority_transfer"])

    def test_manifest_hashes_every_non_manifest_output(self) -> None:
        manifest = self.outputs[sync.MANIFEST_PATH].decode("utf-8")
        for path in sync.NON_MANIFEST_PATHS:
            data = self.outputs[path]
            row = rf"\| `{re.escape(path.as_posix())}` \| {len(data)} \| `{hashlib.sha256(data).hexdigest()}` \|"
            self.assertRegex(manifest, row)
        self.assertNotIn("rows/cx_suite", "\n".join(line for line in manifest.splitlines() if line.startswith("| `")))

    def test_guarded_write_preserves_cx_and_check_converges(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            cx_file = target / "rows/cx_suite/KEEP.toml"
            cx_file.parent.mkdir(parents=True)
            cx_file.write_text('status = "separate"\n', encoding="utf-8")
            before = sync.preimage_digest(target)
            after = sync.write_kernel(
                target,
                self.outputs,
                before,
                self.source_bundle_sha256,
                self.output_sha256,
                sync.SOURCE_ROOT,
            )
            self.assertEqual([], sync.kernel_drift(target, self.outputs))
            self.assertEqual(after, sync.preimage_digest(target))
            self.assertEqual('status = "separate"\n', cx_file.read_text(encoding="utf-8"))

    def test_stale_preimage_refuses_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            target.mkdir(parents=True)
            stale = sync.preimage_digest(target)
            readme = target / "README.md"
            readme.write_text("concurrent edit\n", encoding="utf-8")
            with self.assertRaises(sync.PreimageMismatch):
                sync.write_kernel(
                    target,
                    self.outputs,
                    stale,
                    self.source_bundle_sha256,
                    self.output_sha256,
                    sync.SOURCE_ROOT,
                )
            self.assertEqual("concurrent edit\n", readme.read_text(encoding="utf-8"))

    def test_source_drift_before_write_refuses_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "source"
            self.copy_source_bundle(source_root)
            outputs = sync.render_kernel(source_root)
            source_digest = sync.source_bundle_digest(source_root)
            output_digest = sync.output_digest(outputs)
            target = self.make_target(root / "documents")
            before = sync.preimage_digest(target)
            source_file = source_root / sync.CONTROL_DIR_REL / "contract.py"
            source_file.write_bytes(source_file.read_bytes() + b"\nsource-drift-fixture\n")

            with self.assertRaisesRegex(sync.SourceBundleMismatch, "under lock"):
                sync.write_kernel(
                    target,
                    outputs,
                    before,
                    source_digest,
                    output_digest,
                    source_root,
                )
            self.assertTrue(all(value is None for value in sync.snapshot_kernel(target).values()))

    def test_source_drift_during_staging_refuses_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "source"
            self.copy_source_bundle(source_root)
            outputs = sync.render_kernel(source_root)
            source_digest = sync.source_bundle_digest(source_root)
            output_digest = sync.output_digest(outputs)
            target = self.make_target(root / "documents")
            before = sync.preimage_digest(target)
            source_file = source_root / sync.CONTROL_DIR_REL / "contract.py"
            real_stage = sync._stage_file
            calls = 0

            def drift_after_first_stage(destination: Path, data: bytes) -> Path:
                nonlocal calls
                staged = real_stage(destination, data)
                calls += 1
                if calls == 1:
                    source_file.write_bytes(
                        source_file.read_bytes() + b"\nsource-drift-fixture\n"
                    )
                return staged

            with mock.patch.object(sync, "_stage_file", side_effect=drift_after_first_stage):
                with self.assertRaisesRegex(sync.SourceBundleMismatch, "while staging"):
                    sync.write_kernel(
                        target,
                        outputs,
                        before,
                        source_digest,
                        output_digest,
                        source_root,
                    )
            self.assertTrue(all(value is None for value in sync.snapshot_kernel(target).values()))

    def test_output_drift_before_write_refuses_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            changed = copy.deepcopy(self.outputs)
            changed[Path("README.md")] += b"\noutput-drift-fixture\n"
            with self.assertRaisesRegex(sync.OutputDigestMismatch, "before lock"):
                sync.write_kernel(
                    target,
                    changed,
                    sync.preimage_digest(target),
                    self.source_bundle_sha256,
                    self.output_sha256,
                    sync.SOURCE_ROOT,
                )
            self.assertTrue(all(value is None for value in sync.snapshot_kernel(target).values()))

    def test_output_drift_during_staging_refuses_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            before = sync.preimage_digest(target)
            real_output_digest = sync.output_digest
            calls = 0

            def drifting_output_digest(outputs: dict[Path, bytes]) -> str:
                nonlocal calls
                calls += 1
                digest = real_output_digest(outputs)
                return "0" * 64 if calls == 4 else digest

            with mock.patch.object(sync, "output_digest", side_effect=drifting_output_digest):
                with self.assertRaisesRegex(sync.OutputDigestMismatch, "while staging"):
                    sync.write_kernel(
                        target,
                        self.outputs,
                        before,
                        self.source_bundle_sha256,
                        self.output_sha256,
                        sync.SOURCE_ROOT,
                    )
            self.assertTrue(all(value is None for value in sync.snapshot_kernel(target).values()))

    def test_caught_replace_failure_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            self.write_fresh(target)
            before_snapshot = sync.snapshot_kernel(target)
            before_digest = sync.snapshot_digest(before_snapshot)
            calls = 0
            real_replace = sync.os.replace

            def fail_second(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected replace failure")
                real_replace(source, destination)

            with mock.patch.object(sync, "_replace", side_effect=fail_second):
                with self.assertRaises(OSError):
                    sync.write_kernel(
                        target,
                        self.outputs,
                        before_digest,
                        self.source_bundle_sha256,
                        self.output_sha256,
                        sync.SOURCE_ROOT,
                    )
            self.assertEqual(before_snapshot, sync.snapshot_kernel(target))

    def test_mid_write_external_edit_is_preserved_and_prior_replace_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            self.write_fresh(target)
            before_snapshot = sync.snapshot_kernel(target)
            before_digest = sync.snapshot_digest(before_snapshot)
            real_replace = sync.os.replace
            calls = 0

            def inject_external_edit(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                real_replace(source, destination)
                if calls == 1:
                    (target / "DISPATCH.md").write_text("external concurrent edit\n", encoding="utf-8")

            with mock.patch.object(sync, "_replace", side_effect=inject_external_edit):
                with self.assertRaises(sync.PreimageMismatch):
                    sync.write_kernel(
                        target,
                        self.outputs,
                        before_digest,
                        self.source_bundle_sha256,
                        self.output_sha256,
                        sync.SOURCE_ROOT,
                    )
            self.assertEqual(before_snapshot[Path("README.md")], (target / "README.md").read_bytes())
            self.assertEqual("external concurrent edit\n", (target / "DISPATCH.md").read_text(encoding="utf-8"))

    def test_homology_audit_reads_tracked_yaml_and_generated_row(self) -> None:
        script = sync.SOURCE_ROOT / "09_TOOLS/01_SCRIPTS/agent_homology_audit.py"
        module_spec = importlib.util.spec_from_file_location("agent_homology_audit_test", script)
        self.assertIsNotNone(module_spec)
        self.assertIsNotNone(module_spec.loader)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary:
            documents_root = Path(temporary)
            target = self.make_target(documents_root)
            self.write_fresh(target)
            for row in module.CASTES:
                surfaces = module.audit_caste(sync.SOURCE_ROOT, documents_root, row)
                self.assertEqual(
                    module._extract_operator(surfaces["canonical_yaml"]),
                    module._extract_operator(surfaces["root_dispatch"]),
                )

    def test_active_pipeline_names_tracked_authority_not_missing_legacy_index(self) -> None:
        pipeline = (
            sync.SOURCE_ROOT
            / "08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_CANONICAL_AGENT_PIPELINE.md"
        ).read_text(encoding="utf-8")
        self.assertIn(sync.SOURCE_DIR_REL.as_posix(), pipeline)
        self.assertIn(sync.GENERATOR_REL.as_posix(), pipeline)
        self.assertEqual(1, pipeline.count(".codex/agents/rosetta_agent_rows.toml"))
        self.assertIn("pipeline is superseded", pipeline)
        self.assertNotIn(".codex/agents/sync_agents.py", pipeline)


if __name__ == "__main__":
    unittest.main()
