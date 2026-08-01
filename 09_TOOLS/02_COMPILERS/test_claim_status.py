#!/usr/bin/env python3
"""Mutation controls for the Claim Status v2 disposition contract."""

from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_claim_status.py"
SPEC = importlib.util.spec_from_file_location("check_claim_status", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ClaimStatusV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = CHECKER.load_document(ROOT / CHECKER.STATUS_PATH)

    def errors_for(self, document):
        with mock.patch.object(CHECKER, "load_document", return_value=document):
            return CHECKER.check(ROOT)

    def assert_invalid(self, document, needle: str) -> None:
        errors = self.errors_for(document)
        self.assertTrue(errors, "mutation unexpectedly passed")
        self.assertTrue(
            any(needle in error for error in errors),
            f"expected {needle!r}; got {errors}",
        )

    def row(self, document, section: str, row_id: str):
        return next(row for row in document[section] if row["id"] == row_id)

    def test_live_contract_passes_and_binds_full_scope(self) -> None:
        self.assertEqual(CHECKER.check(ROOT), [])
        self.assertEqual(len(CHECKER.lifecycle_rows(self.document)), 48)
        self.assertEqual(
            CHECKER.canonical_lifecycle_sha256(self.document),
            "4f01474e67957703b81c6e99ed8a82a0905e2b584be48a4c6d2390f9d8c7eb0e",  # pragma: allow-secret -- public corpus digest fixture
        )
        self.assertEqual(
            CHECKER.canonical_contract_sha256(self.document),
            "017cbc2a76d93c7d30340a57cfa56f12520ea0581917e711ceafb2a31b5d237d",  # pragma: allow-secret -- public corpus digest fixture
        )

    def test_duplicate_json_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"schema":"one","schema":"two"}', encoding="utf-8")
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.load_document(path)

    def test_schema_drift_fails(self) -> None:
        document = copy.deepcopy(self.document)
        document["schema"] = "emergentism/claim-status/v1"
        self.assert_invalid(document, "schema must be")

    def test_missing_disposition_fails(self) -> None:
        document = copy.deepcopy(self.document)
        del self.row(document, "open", "W4")["disposition"]
        self.assert_invalid(document, "missing disposition")

    def test_status_kind_mismatch_fails(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "open", "W4")["status"] = "DECORATIVE"
        self.assert_invalid(document, "CONTACT-GATED requires")

    def test_unknown_contract_field_fails(self) -> None:
        document = copy.deepcopy(self.document)
        contract = self.row(document, "open", "W4")["disposition"]["contracts"][0]
        contract["outcome"] = "fabricated"
        self.assert_invalid(document, "unknown keys: outcome")

    def test_duplicate_contract_id_fails(self) -> None:
        document = copy.deepcopy(self.document)
        w4 = self.row(document, "open", "W4")["disposition"]["contracts"]
        w4[1]["contract_id"] = w4[0]["contract_id"]
        self.assert_invalid(document, "duplicate contact contract id")

    def test_dangling_owner_fails(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "open", "W4")["disposition"]["claim_owner"] = "missing.md"
        self.assert_invalid(document, "file does not exist")

    def test_fake_external_target_and_blocker_fail(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "reopened", "RQ-03")["disposition"]["target_ids"] = ["W99"]
        self.assert_invalid(document, "self or unknown target")

        document = copy.deepcopy(self.document)
        contract = self.row(document, "open", "W4")["disposition"]["contracts"][0]
        contract["blocked_by"] = ["GP-99"]
        self.assert_invalid(document, "not a governed prerequisite")

    def test_external_owner_source_must_declare_exact_marker(self) -> None:
        self.assertTrue(
            CHECKER.external_owner_marker_declared(
                ROOT / CHECKER.EXTERNAL_OWNER_FILES["HC-11"], "HC-11"
            )
        )
        with mock.patch.object(
            CHECKER,
            "external_owner_marker_declared",
            side_effect=lambda _path, owner_id: owner_id != "HC-11",
        ):
            errors = CHECKER.check(ROOT)
        self.assertTrue(
            any("external owner HC-11: source does not declare" in error for error in errors),
            errors,
        )

    def test_integrated_support_promotion_fails(self) -> None:
        document = copy.deepcopy(self.document)
        contract = self.row(document, "open", "W8")["disposition"]["contracts"][0]
        contract["integrated_support"] = "validated"
        self.assert_invalid(document, "integrated_support must remain absent")

    def test_blocker_and_maturity_must_move_together(self) -> None:
        document = copy.deepcopy(self.document)
        contract = self.row(document, "open", "W4")["disposition"]["contracts"][0]
        contract["blocked_by"] = []
        self.assert_invalid(document, "blocked maturity and blocked_by")

    def test_terminal_blocker_and_dependency_cycle_fail(self) -> None:
        document = copy.deepcopy(self.document)
        contract = self.row(document, "open", "W4")["disposition"]["contracts"][0]
        contract["blocked_by"] = ["W0-CROWN"]
        self.assert_invalid(document, "terminal, or not a governed prerequisite")

        document = copy.deepcopy(self.document)
        w4 = self.row(document, "open", "W4")["disposition"]["contracts"][0]
        w7e = self.row(document, "open", "W7e")["disposition"]["contracts"][0]
        w4["blocked_by"] = ["W7e"]
        w7e["maturity"] = "blocked"
        w7e["blocked_by"] = ["W4"]
        self.assert_invalid(document, "contact blocker cycle")

    def test_merge_target_must_directly_own_contract(self) -> None:
        document = copy.deepcopy(self.document)
        disposition = self.row(document, "reopened", "RQ-01")["disposition"]
        disposition["target_ids"] = ["RQ-02"]
        self.assert_invalid(document, "is not a direct CONTACT-GATED row")

    def test_merge_target_cannot_block_on_its_merged_row(self) -> None:
        document = copy.deepcopy(self.document)
        target = self.row(document, "open", "W4")["disposition"]["contracts"][0]
        target["maturity"] = "blocked"
        target["blocked_by"] = ["W3"]
        self.assert_invalid(document, "contact blocker cycle")

    def test_internal_fv_tier_mismatch_fails(self) -> None:
        document = copy.deepcopy(self.document)
        resolution = self.row(document, "reopened", "RQ-03")["disposition"]["resolution"]
        resolution["result_tier"] = "S"
        self.assert_invalid(document, "FV result tier does not match")

    def test_iv_result_identity_is_row_owned(self) -> None:
        document = copy.deepcopy(self.document)
        resolution = self.row(document, "reopened", "RQ-04")["disposition"]["resolution"]
        resolution["result_id"] = "IV-W3-01"
        self.assert_invalid(document, "IV result_id must be owned by its row id")

    def test_governance_metadata_is_required_and_pinned(self) -> None:
        document = copy.deepcopy(self.document)
        del document["human_owner"]
        self.assert_invalid(document, "missing keys: human_owner")

        document = copy.deepcopy(self.document)
        document["routing_role"] = "semantic authority and tier promotion"
        self.assert_invalid(document, "validation-only, no-promotion boundary")

    def test_validated_results_are_inventory_and_digest_bound(self) -> None:
        document = copy.deepcopy(self.document)
        document["validated"] = [
            row for row in document["validated"] if row["id"] != "FV-01"
        ]
        self.assert_invalid(document, "validated inventory drifted")

        document = copy.deepcopy(self.document)
        self.row(document, "validated", "FV-19")["result"] += " mutated"
        self.assertNotEqual(
            CHECKER.canonical_contract_sha256(document),
            CHECKER.canonical_contract_sha256(self.document),
        )

    def test_restored_result_owner_must_resolve(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "restored", "TR-01")["owner"] = "missing-restored-owner.md"
        self.assert_invalid(document, "TR-01.owner: file does not exist")

    def test_count_preserving_status_swap_fails(self) -> None:
        document = copy.deepcopy(self.document)
        w4 = self.row(document, "open", "W4")
        w11 = self.row(document, "open", "W11")
        w4["status"], w11["status"] = w11["status"], w4["status"]
        self.assert_invalid(document, "CONTACT-GATED requires")

    def test_grave_transition_cannot_remain_owner_reopened(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "graves", "DF-04")["status"] = "OWNER-REOPENED"
        self.assert_invalid(document, "remain unadjudicated")

    def test_row_substitution_fails_even_at_constant_count(self) -> None:
        document = copy.deepcopy(self.document)
        self.row(document, "reopened", "RQ-09")["id"] = "RQ-10"
        self.assert_invalid(document, "RQ inventory drifted")


if __name__ == "__main__":
    unittest.main(verbosity=2)
