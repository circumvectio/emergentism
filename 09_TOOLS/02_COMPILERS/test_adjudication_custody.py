#!/usr/bin/env python3
"""Mutation controls for the immutable 229-finding custody replay."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_adjudication_custody.py"
SPEC = importlib.util.spec_from_file_location("check_adjudication_custody", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

FIXTURE_PATHS = (
    CHECKER.FIRST_LEDGER_REL,
    CHECKER.REMAINING_LEDGER_REL,
    CHECKER.SUPPLEMENT_REL,
    CHECKER.RECEIPT_REL,
)


class AdjudicationCustodyTests(unittest.TestCase):
    def fixture_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for relative in FIXTURE_PATHS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        return root

    def errors(self, root: Path) -> list[str]:
        return CHECKER.adjudication_custody_errors(root)

    def assert_contains(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(any(fragment in error for error in errors), errors)

    def jsonl_records(self, root: Path, relative: Path) -> list[dict]:
        return [json.loads(line) for line in (root / relative).read_text(encoding="utf-8").splitlines()]

    def write_jsonl_records(self, root: Path, relative: Path, records: list[dict]) -> None:
        payload = "\n".join(json.dumps(record, separators=(",", ":")) for record in records) + "\n"
        (root / relative).write_text(payload, encoding="utf-8")

    @staticmethod
    def finding(records: list[dict], global_id: int) -> dict:
        return next(record for record in records[1:] if record.get("global_actionable_id") == global_id)

    def test_baseline_replays_only_four_custody_artifacts(self) -> None:
        root = self.fixture_root()
        self.assertFalse((root / "02_EPISTEMOLOGY").exists())
        self.assertEqual(self.errors(root), [])

    def test_each_frozen_artifact_and_receipt_is_byte_locked(self) -> None:
        expected = {
            CHECKER.FIRST_LEDGER_REL: "first-60 adjudication ledger digest drifted",
            CHECKER.REMAINING_LEDGER_REL: "remaining-169 adjudication ledger digest drifted",
            CHECKER.SUPPLEMENT_REL: "remaining-169 review supplement digest drifted",
            CHECKER.RECEIPT_REL: "Receipt 234 digest drifted",
        }
        for relative, fragment in expected.items():
            with self.subTest(relative=relative):
                root = self.fixture_root()
                path = root / relative
                payload = path.read_bytes()
                if relative == CHECKER.RECEIPT_REL:
                    mutated = payload.replace(b"229", b"228", 1)
                else:
                    mutated = payload.replace(b"record_type", b"record_typE", 1)
                self.assertNotEqual(mutated, payload)
                path.write_bytes(mutated)
                self.assert_contains(self.errors(root), fragment)

    def test_jsonl_requires_unambiguous_regular_records(self) -> None:
        mutations = {
            "duplicate JSON key": lambda payload: payload.replace(
                b'"count":60,', b'"count":60,"count":60,', 1
            ),
            "blank record": lambda payload: payload.replace(b"\n", b"\n\n", 1),
            "byte-order mark": lambda payload: b"\xef\xbb\xbf" + payload,
            "carriage return": lambda payload: payload.replace(b"\n", b"\r\n", 1),
            "missing final newline": lambda payload: payload.rstrip(b"\n"),
            "malformed JSON": lambda payload: b"{not-json}\n" + payload.split(b"\n", 1)[1],
            "non-object row": lambda payload: b"[]\n" + payload.split(b"\n", 1)[1],
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                root = self.fixture_root()
                path = root / CHECKER.FIRST_LEDGER_REL
                path.write_bytes(mutate(path.read_bytes()))
                errors = self.errors(root)
                self.assert_contains(errors, "first-60 adjudication ledger")

        root = self.fixture_root()
        path = root / CHECKER.FIRST_LEDGER_REL
        original = path.read_bytes()
        external = root / "external-first-ledger.jsonl"
        external.write_bytes(original)
        path.unlink()
        path.symlink_to(external)
        self.assert_contains(self.errors(root), "must not traverse a symlink")

    def test_first_slice_requires_every_result_ordinal(self) -> None:
        root = self.fixture_root()
        records = self.jsonl_records(root, CHECKER.FIRST_LEDGER_REL)
        records[1]["journal_result_ordinal"] = 2
        self.write_jsonl_records(root, CHECKER.FIRST_LEDGER_REL, records)
        self.assert_contains(self.errors(root), "result ordinals must be exactly 1 through 60")

    def test_remaining_slice_requires_global_id_relation_and_partition_identity(self) -> None:
        root = self.fixture_root()
        records = self.jsonl_records(root, CHECKER.REMAINING_LEDGER_REL)
        self.finding(records, 229)["global_actionable_id"] = 228
        self.write_jsonl_records(root, CHECKER.REMAINING_LEDGER_REL, records)
        errors = self.errors(root)
        self.assert_contains(errors, "global_actionable_id = 60 + ordinal")
        self.assert_contains(errors, "global actionable ids must be exactly 61 through 229")

        root = self.fixture_root()
        records = self.jsonl_records(root, CHECKER.REMAINING_LEDGER_REL)
        left = self.finding(records, 61)
        right = self.finding(records, 62)
        left["original_verdict"], right["original_verdict"] = (
            right["original_verdict"],
            left["original_verdict"],
        )
        left["final_disposition"], right["final_disposition"] = (
            right["final_disposition"],
            left["final_disposition"],
        )
        self.write_jsonl_records(root, CHECKER.REMAINING_LEDGER_REL, records)
        self.assert_contains(self.errors(root), "remaining-169 adjudication ledger digest drifted")

    def test_remaining_duplicate_targets_are_exact_and_nonrecursive(self) -> None:
        cases = {
            "changed parent": lambda records: self.finding(records, 156).update(
                duplicate_of_global_actionable_id=198
            ),
            "duplicate cycle": lambda records: (
                self.finding(records, 156).update(duplicate_of_global_actionable_id=217),
                self.finding(records, 217).update(duplicate_of_global_actionable_id=156),
            ),
            "missing target": lambda records: self.finding(records, 156).update(
                duplicate_of_global_actionable_id=60
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(label=label):
                root = self.fixture_root()
                records = self.jsonl_records(root, CHECKER.REMAINING_LEDGER_REL)
                mutate(records)
                self.write_jsonl_records(root, CHECKER.REMAINING_LEDGER_REL, records)
                errors = self.errors(root)
                self.assert_contains(errors, "duplicate mappings drifted")
                if label == "duplicate cycle":
                    self.assert_contains(errors, "may not target another duplicate")
                if label == "missing target":
                    self.assert_contains(errors, "names a missing target 60")

    def test_review_supplement_keeps_its_source_and_exact_controls(self) -> None:
        source_mutations = {
            "source path": ("source_ledger", "other-ledger.jsonl"),
            "source hash": ("source_ledger_sha256", "0" * 64),
        }
        for label, (field, value) in source_mutations.items():
            with self.subTest(label=label):
                root = self.fixture_root()
                records = self.jsonl_records(root, CHECKER.SUPPLEMENT_REL)
                records[0][field] = value
                self.write_jsonl_records(root, CHECKER.SUPPLEMENT_REL, records)
                self.assert_contains(self.errors(root), "review supplement metadata drifted")

        corrections = {
            "correction id": ("global_actionable_id", 67, "controlling disposition corrections"),
            "source disposition": ("source_disposition", "DISMISSED_FALSE", "no longer names its source disposition"),
            "reviewed disposition": (
                "reviewed_disposition",
                "FIXED_IN_THIS_ADJUDICATION",
                "controlling disposition corrections",
            ),
        }
        for label, (field, value, expected) in corrections.items():
            with self.subTest(label=label):
                root = self.fixture_root()
                records = self.jsonl_records(root, CHECKER.SUPPLEMENT_REL)
                next(record for record in records if record.get("global_actionable_id") == 66)[field] = value
                self.write_jsonl_records(root, CHECKER.SUPPLEMENT_REL, records)
                self.assert_contains(self.errors(root), expected)

        for unsafe_path in (
            "/outside-the-corpus.md",
            "..\\outside\\proof.md",
            "C:\\outside\\proof.md",
            "\\\\server\\share\\proof.md",
        ):
            with self.subTest(unsafe_path=unsafe_path):
                root = self.fixture_root()
                records = self.jsonl_records(root, CHECKER.SUPPLEMENT_REL)
                next(record for record in records if record.get("global_actionable_id") == 66)[
                    "evidence"
                ] = [unsafe_path]
                self.write_jsonl_records(root, CHECKER.SUPPLEMENT_REL, records)
                self.assert_contains(self.errors(root), "invalid retained evidence metadata")

    def test_review_closures_gate_docket_and_effective_partition_fail_closed(self) -> None:
        cases = {
            "closure": lambda records: next(
                record for record in records if record.get("global_actionable_id") == 70
            ).update(global_actionable_id=71),
            "gate": lambda records: next(
                record for record in records if record.get("record_type") == "gate_preservation"
            ).update(global_actionable_id=211),
            "docket evidence": lambda records: next(
                record for record in records if record.get("record_type") == "open_docket"
            ).update(evidence=copy.deepcopy(CHECKER.REVIEW_DOCKET["evidence"][:-1])),
        }
        expected = {
            "closure": "seven closure confirmations",
            "gate": "topology owner-gate preservation",
            "docket evidence": "KSC-02 downstream-drift docket",
        }
        for label, mutate in cases.items():
            with self.subTest(label=label):
                root = self.fixture_root()
                records = self.jsonl_records(root, CHECKER.SUPPLEMENT_REL)
                mutate(records)
                self.write_jsonl_records(root, CHECKER.SUPPLEMENT_REL, records)
                self.assert_contains(self.errors(root), expected[label])

        root = self.fixture_root()
        records = self.jsonl_records(root, CHECKER.SUPPLEMENT_REL)
        next(record for record in records if record.get("global_actionable_id") == 183)[
            "reviewed_disposition"
        ] = "FIXED_IN_THIS_ADJUDICATION"
        self.write_jsonl_records(root, CHECKER.SUPPLEMENT_REL, records)
        self.assert_contains(self.errors(root), "reviewed effective partition must remain 151 / 8 / 4 / 6")

    def test_receipt_keeps_each_parent_and_declared_hash(self) -> None:
        root = self.fixture_root()
        receipt = root / CHECKER.RECEIPT_REL
        text = receipt.read_text(encoding="utf-8")
        text = text.replace(
            "- ../../" + CHECKER.FIRST_LEDGER_REL.as_posix(),
            "- ../../09_TOOLS/08_AUDIT_ARTIFACTS/other-ledger.jsonl",
            1,
        ).replace(
            CHECKER.REMAINING_META["raw_findings_sha256"],
            "0" * 64,
            1,
        )
        receipt.write_text(text, encoding="utf-8")
        errors = self.errors(root)
        self.assert_contains(errors, "no longer names 2026_08_01_FIRST_60_ADJUDICATION.jsonl")
        self.assert_contains(errors, "no longer declares the frozen SHA-256 for Reconstructed raw findings")


if __name__ == "__main__":
    unittest.main(verbosity=2)
