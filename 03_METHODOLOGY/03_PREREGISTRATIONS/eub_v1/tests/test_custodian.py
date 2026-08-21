#!/usr/bin/env python3
"""Offline acceptance tests for the EUB held-out custodian membrane."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from custodian import (  # noqa: E402
    CustodianContext,
    CustodyValidationError,
    prepare_held_out_fixture,
    validate_custody_opening,
    validate_held_out_public_fixture,
    validate_public_custodian_receipt,
)
from eub_core import (  # noqa: E402
    SITTING_ORDER,
    build_recorded_trial,
    generate_fixture,
    load_json,
    score_dasein_trial,
    sha256_value,
)


ACCOUNT_PATH = HERE / "recorded_responses" / "dasein_account_dev.json"


def held_out_material() -> tuple[dict, dict, str]:
    return prepare_held_out_fixture(
        generate_fixture(1701),
        fixture_id="dasein-heldout-custodian-test",
        custody_nonce="ab" * 32,
    )


def run_envelope(run_id: str = "held-out-custodian-run") -> dict:
    return {
        "schema_id": "RunEnvelope.v1",
        "run_id": run_id,
        "run_class": "OFFLINE_DRY_RUN",
        "requested_model_id": "recorded-dasein-v1",
        "resolved_model_id": "recorded-dasein-v1",
        "adapter": "recorded",
        "runtime": {"python": "test", "harness": "1.0.0"},
        "prompt_arm": "NEUTRAL",
        "tools": [],
        "memory": {"enabled": False, "description": "disabled"},
        "budgets": {
            "max_input_tokens": 32768,
            "max_output_tokens": 4096,
            "cost_limit_usd": 0.0,
            "input_cost_per_million_usd": 0.0,
            "output_cost_per_million_usd": 0.0,
            "cost_basis_ref": "OFFLINE_RECORDED_ZERO_COST",
        },
        "network": {"allowed": False, "endpoint_class": "OFFLINE"},
        "authorization_ref": "",
    }


def trial_material(run_id: str = "held-out-custodian-run") -> tuple[list[dict], dict[str, str], dict[str, str]]:
    account = load_json(ACCOUNT_PATH)
    trial = build_recorded_trial(account, run_id)
    raw_hashes = {
        sitting: sha256_value({"recorded_raw": account})
        for sitting, account in zip(SITTING_ORDER, trial)
    }
    prompt_hashes = {
        sitting: sha256_value({"held_out_prompt": sitting})
        for sitting in SITTING_ORDER
    }
    return trial, raw_hashes, prompt_hashes


def offline_usage() -> dict:
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "estimated_cost_usd": 0.0,
        "reserved_cost_usd": 0.0,
        "calls": [],
    }


class CustodianOpeningTests(unittest.TestCase):
    def test_public_fixture_is_blind_and_private_opening_verifies(self):
        public, payload, commitment = held_out_material()
        self.assertEqual(validate_held_out_public_fixture(public), [])
        self.assertEqual(validate_custody_opening(public, payload, commitment), [])
        self.assertIsNone(public["hidden_truth"])
        self.assertIsNone(public["manifest"]["seed"])

    def test_public_fixture_alone_remains_unscorable(self):
        public, _, _ = held_out_material()
        trial, raw_hashes, prompt_hashes = trial_material()
        receipt = score_dasein_trial(
            trial,
            public,
            None,
            raw_output_hashes=raw_hashes,
            prompt_hashes=prompt_hashes,
        )
        self.assertEqual(receipt["result_state"], "CUSTODY_UNAVAILABLE")

    def test_commitment_seed_truth_packet_and_outcome_tampering_fail(self):
        public, payload, commitment = held_out_material()

        self.assertTrue(
            any("does not bind" in row for row in validate_custody_opening(public, payload, "0" * 64))
        )

        wrong_seed = deepcopy(payload)
        wrong_seed["seed"] += 1
        self.assertTrue(
            any("seed" in row for row in validate_custody_opening(public, wrong_seed, sha256_value(wrong_seed)))
        )

        wrong_truth = deepcopy(payload)
        wrong_truth["hidden_truth"]["expected_intervention_outcome"] = "custody-secret-tamper"
        self.assertTrue(
            any("truth" in row for row in validate_custody_opening(public, wrong_truth, sha256_value(wrong_truth)))
        )

        wrong_packet = deepcopy(payload)
        wrong_packet["hidden_truth"]["packets"]["ATTACK"]["attacks"][0]["assertion"] = "custody-secret-tamper"
        self.assertTrue(
            any("ATTACK" in row for row in validate_custody_opening(public, wrong_packet, sha256_value(wrong_packet)))
        )

        wrong_outcome = deepcopy(payload)
        wrong_outcome["intervention_outcomes"]["exp_signal_cut"] = "custody-secret-tamper"
        self.assertTrue(
            any(
                "outcome" in row
                for row in validate_custody_opening(
                    public, wrong_outcome, sha256_value(wrong_outcome)
                )
            )
        )

    def test_payload_and_public_contracts_are_strict(self):
        public, payload, commitment = held_out_material()
        development = deepcopy(public)
        development["manifest"]["split"] = "DEVELOPMENT"
        self.assertTrue(validate_held_out_public_fixture(development))

        extra = deepcopy(payload)
        extra["private_note"] = "must not be accepted"
        errors = validate_custody_opening(public, extra, sha256_value(extra))
        self.assertTrue(any("unknown fields" in row for row in errors))
        self.assertEqual(validate_custody_opening(public, payload, commitment), [])


class CustodianScoringTests(unittest.TestCase):
    def test_scoring_requires_active_context_and_context_is_one_shot(self):
        public, payload, commitment = held_out_material()
        trial, raw_hashes, prompt_hashes = trial_material()
        context = CustodianContext(public, payload, commitment)
        with self.assertRaises(CustodyValidationError):
            context.score_trial(
                trial, None,
                raw_output_hashes=raw_hashes,
                prompt_hashes=prompt_hashes,
                usage=offline_usage(),
            )
        with context as active:
            receipt = active.score_trial(
                trial, run_envelope(),
                raw_output_hashes=raw_hashes,
                prompt_hashes=prompt_hashes,
                usage=offline_usage(),
            )
            self.assertEqual(receipt["result_state"], "SCORED_HELD_OUT")
            with self.assertRaises(CustodyValidationError):
                active.score_trial(
                    trial, run_envelope(),
                    raw_output_hashes=raw_hashes,
                    prompt_hashes=prompt_hashes,
                    usage=offline_usage(),
                )
        with self.assertRaises(CustodyValidationError):
            context.score_trial(
                trial, None,
                raw_output_hashes=raw_hashes,
                prompt_hashes=prompt_hashes,
                usage=offline_usage(),
            )
        with self.assertRaises(CustodyValidationError):
            context.__enter__()

    def test_first_failed_attempt_consumes_context_and_never_leaks_raw_errors(self):
        public, payload, commitment = held_out_material()
        trial, raw_hashes, prompt_hashes = trial_material()
        with CustodianContext(public, payload, commitment) as context:
            with self.assertRaises(CustodyValidationError):
                context.score_trial(
                    {"not": "a snapshot list"},
                    run_envelope(),
                    raw_output_hashes={},
                    prompt_hashes={},
                    usage=offline_usage(),
                )
            with self.assertRaises(CustodyValidationError):
                context.score_trial(
                    trial,
                    run_envelope(),
                    raw_output_hashes=raw_hashes,
                    prompt_hashes=prompt_hashes,
                    usage=offline_usage(),
                )

    def test_public_receipt_binds_public_inputs_without_truth_leakage(self):
        public, payload, commitment = held_out_material()
        public_before = deepcopy(public)
        payload_before = deepcopy(payload)
        trial, raw_hashes, prompt_hashes = trial_material()
        with CustodianContext(public, payload, commitment) as context:
            receipt = context.score_trial(
                trial, run_envelope(),
                raw_output_hashes=raw_hashes,
                prompt_hashes=prompt_hashes,
                usage=offline_usage(),
            )

        self.assertEqual(validate_public_custodian_receipt(receipt, public), [])
        self.assertEqual(public, public_before)
        self.assertEqual(payload, payload_before)
        self.assertEqual(receipt["public_fixture_sha256"], sha256_value(public))
        self.assertEqual(receipt["custody_commitment_sha256"], commitment)
        self.assertEqual(receipt["usage_hash"], sha256_value(offline_usage()))
        self.assertEqual(receipt["failure_hash"], sha256_value({}))
        self.assertIn("private_eub_receipt_commitment_sha256", receipt)
        self.assertNotIn("private_eub_receipt_sha256", receipt)
        self.assertTrue(all(score == 4.0 for score in receipt["score_vector"].values()))
        self.assertNotIn("primary_scalar", receipt)
        self.assertNotIn("aggregate_score", receipt)
        self.assertNotIn("score_details", receipt)

        encoded = json.dumps(receipt, sort_keys=True)
        for private_value in (
            "lineage_transition_stops",
            "channel_dependency_preserved_under_relabel",
            "CONTESTED_UNVERIFIED",
            str(payload["seed"]),
        ):
            self.assertNotIn(private_value, encoded)
        for private_key in (
            "hidden_truth",
            "intervention_outcomes",
            "expected_intervention_outcome",
            "custody_nonce",
        ):
            self.assertNotIn(f'"{private_key}"', encoded)

        self.assertFalse(
            receipt["custody_attestation"]["independent_custody_verified_by_software"]
        )
        self.assertFalse(
            receipt["custody_attestation"]["commitment_timing_verified_by_software"]
        )

    def test_public_receipt_validator_rejects_drift_and_scalar(self):
        public, payload, commitment = held_out_material()
        trial, raw_hashes, prompt_hashes = trial_material()
        with CustodianContext(public, payload, commitment) as context:
            receipt = context.score_trial(
                trial, run_envelope(),
                raw_output_hashes=raw_hashes,
                prompt_hashes=prompt_hashes,
                usage=offline_usage(),
            )
        drifted = deepcopy(receipt)
        drifted["public_fixture_sha256"] = "0" * 64
        self.assertTrue(validate_public_custodian_receipt(drifted, public))
        scalar = deepcopy(receipt)
        scalar["primary_scalar"] = 4.0
        errors = validate_public_custodian_receipt(scalar, public)
        self.assertTrue(any("unknown fields" in row for row in errors))
        self.assertTrue(any("scalar" in row for row in errors))

        unscored_with_scores = deepcopy(receipt)
        unscored_with_scores["result_state"] = "INVALID_OUTPUT"
        errors = validate_public_custodian_receipt(unscored_with_scores, public)
        self.assertTrue(any("non-scored state" in row for row in errors), errors)

        scored_without_scores = deepcopy(receipt)
        scored_without_scores["score_vector"] = {
            dimension: None for dimension in scored_without_scores["score_vector"]
        }
        scored_without_scores["score_uncertainty"] = {
            dimension: {"lower": None, "upper": None}
            for dimension in scored_without_scores["score_uncertainty"]
        }
        errors = validate_public_custodian_receipt(scored_without_scores, public)
        self.assertTrue(any("scored state" in row for row in errors), errors)

        outside_bounds = deepcopy(receipt)
        outside_bounds["score_vector"]["type_integrity"] = 1.0
        outside_bounds["score_uncertainty"]["type_integrity"] = {
            "lower": 3.0,
            "upper": 4.0,
        }
        errors = validate_public_custodian_receipt(outside_bounds, public)
        self.assertTrue(any("must enclose" in row for row in errors), errors)

        null_with_numeric_mode = deepcopy(receipt)
        null_with_numeric_mode["score_vector"]["type_integrity"] = None
        null_with_numeric_mode["score_modes"]["type_integrity"] = "DETERMINISTIC"
        errors = validate_public_custodian_receipt(null_with_numeric_mode, public)
        self.assertTrue(any("N/A mode" in row for row in errors), errors)

    def test_custodian_requires_a_usage_ledger_that_matches_the_run_envelope(self):
        public, payload, commitment = held_out_material()
        trial, raw_hashes, prompt_hashes = trial_material()
        forged_usage = offline_usage()
        forged_usage["calls"] = [
            {
                "call_index": 1,
                "sitting_id": "UNFOLD",
                "status": "COMPLETED",
                "reserved_input_tokens": 32768,
                "reserved_output_tokens": 4096,
                "reserved_cost_usd": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "estimated_cost_usd": 0.0,
            }
        ]
        with CustodianContext(public, payload, commitment) as context:
            with self.assertRaises(CustodyValidationError):
                context.score_trial(
                    trial,
                    run_envelope(),
                    raw_output_hashes=raw_hashes,
                    prompt_hashes=prompt_hashes,
                    usage=forged_usage,
                )


if __name__ == "__main__":
    unittest.main()
