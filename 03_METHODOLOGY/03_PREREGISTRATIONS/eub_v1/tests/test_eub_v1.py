#!/usr/bin/env python3
"""Rigorous standard-library acceptance tests for EUB-1 v1.0.

The tests intentionally exercise the temporal and custody boundaries, rather
than merely checking that the reference answer receives a high score. They do
not make network calls and write only inside ``TemporaryDirectory`` instances.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from adapters import (  # noqa: E402
    AdapterError,
    AnthropicMessagesAdapter,
    AuthorizationRequired,
    BudgetRefused,
    NetworkPolicy,
    NetworkRefused,
    OpenAICompatibleAdapter,
)
from custodian import prepare_held_out_fixture  # noqa: E402
from eub_core import (  # noqa: E402
    SCORE_DIMENSIONS,
    SITTING_ORDER,
    build_freeze_manifest,
    build_recorded_trial,
    check_freeze_manifest,
    generate_fixture,
    load_json,
    score_dasein_account,
    score_dasein_trial,
    score_serial_force_response,
    serial_force_fixture,
    validate_dasein_account,
    validate_fixture_bundle,
    validate_receipt,
    validate_run_bundle,
    validate_run_envelope,
    validate_trial_snapshots,
    write_json,
)


ACCOUNT_PATH = HERE / "recorded_responses" / "dasein_account_dev.json"
FIXTURE_PATH = HERE / "fixtures" / "dev" / "dasein_chain_seed_1701.json"
RUNNER = HERE / "run_eub.py"


def canonical_bytes(value: object) -> bytes:
    """Independent implementation of the protocol's canonical JSON bytes."""

    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def reference_account() -> dict[str, object]:
    return load_json(ACCOUNT_PATH)


def reference_fixture() -> dict[str, object]:
    return load_json(FIXTURE_PATH)


def reference_trial(run_id: str = "acceptance-run") -> list[dict[str, object]]:
    return build_recorded_trial(reference_account(), run_id)


def rechain(trial: list[dict[str, object]]) -> None:
    """Repair only envelope ancestry after a deliberate semantic mutation."""

    for index, account in enumerate(trial):
        account["causal_account"]["parent_account_hash"] = (
            None if index == 0 else canonical_hash(trial[index - 1])
        )
    trial[-1]["transfer"]["source_account_hash"] = canonical_hash(trial[3])


def score_trial(
    trial: list[dict[str, object]],
    fixture: dict[str, object] | None = None,
    envelope: dict[str, object] | None = None,
) -> dict[str, object]:
    raw_hashes = {
        sitting: canonical_hash(account)
        for sitting, account in zip(SITTING_ORDER, trial)
    }
    prompt_hashes = {
        sitting: canonical_hash({"acceptance_prompt": sitting})
        for sitting in SITTING_ORDER
    }
    return score_dasein_trial(
        trial,
        fixture or reference_fixture(),
        envelope,
        raw_output_hashes=raw_hashes,
        prompt_hashes=prompt_hashes,
    )


def offline_envelope(run_id: str = "acceptance-run") -> dict[str, object]:
    return {
        "schema_id": "RunEnvelope.v1",
        "run_id": run_id,
        "run_class": "OFFLINE_DRY_RUN",
        "requested_model_id": "recorded-dasein-v1",
        "resolved_model_id": "recorded-dasein-v1",
        "adapter": "recorded",
        "runtime": {"python": sys.version.split()[0], "harness": "EUB-1-v1.0"},
        "prompt_arm": "NEUTRAL",
        "tools": [],
        "memory": {"enabled": False, "description": "acceptance replay"},
        "budgets": {
            "max_input_tokens": 16384,
            "max_output_tokens": 4096,
            "cost_limit_usd": 0.0,
            "input_cost_per_million_usd": 0.0,
            "output_cost_per_million_usd": 0.0,
            "cost_basis_ref": "OFFLINE_NO_PROVIDER_COST",
        },
        "network": {"allowed": False, "endpoint_class": "OFFLINE"},
        "authorization_ref": "",
    }


def held_out_fixture() -> dict[str, object]:
    """Turn a generated fixture into a public commitment-only held-out view."""

    public, _, _ = prepare_held_out_fixture(
        generate_fixture(1701),
        fixture_id="dasein-heldout-contract-test",
        custody_nonce="cd" * 32,
    )
    return public


class FiveSittingStateMachineTests(unittest.TestCase):
    def test_reference_trial_has_exact_order_and_valid_ancestry(self):
        trial = reference_trial()
        self.assertEqual(
            [row["causal_account"]["sitting_id"] for row in trial],
            list(SITTING_ORDER),
        )
        self.assertEqual(validate_trial_snapshots(trial), [])
        self.assertIsNone(trial[0]["causal_account"]["parent_account_hash"])
        for index in range(1, len(trial)):
            self.assertEqual(
                trial[index]["causal_account"]["parent_account_hash"],
                canonical_hash(trial[index - 1]),
            )
        self.assertEqual(
            trial[-1]["transfer"]["source_account_hash"], canonical_hash(trial[3])
        )

    def test_phase_leaks_are_rejected_at_their_earliest_boundary(self):
        cases = []

        early_selection = reference_trial()
        early_selection[1]["hypotheses"] = copy.deepcopy(
            early_selection[2]["hypotheses"]
        )
        early_selection[1]["experiments"] = copy.deepcopy(
            early_selection[2]["experiments"]
        )
        rechain(early_selection)
        cases.append(("Attack selection", early_selection, "select exactly 0"))

        contact_leak = reference_trial()
        contact_leak[2]["experiments"][0]["observed_outcome"] = (
            "lineage_transition_stops"
        )
        rechain(contact_leak)
        cases.append(("Contact truth", contact_leak, "leaks Contact truth"))

        reflex_leak = reference_trial()
        reflex_leak[3]["self_predictions"][0]["observed_outcome"] = (
            "context_sensitive_revision"
        )
        reflex_leak[3]["self_predictions"][0][
            "prior_answer_became_context"
        ] = True
        rechain(reflex_leak)
        cases.append(("Reflex truth", reflex_leak, "leaks Reflex result"))

        transfer_leak = reference_trial()
        transfer_leak[3]["transfer"].update(
            {
                "relabeled_lineage": True,
                "unseen_family": True,
                "independent_solution": True,
                "transfer_fixture_id": "transfer-quartz-v1",
                "answer": "channel_dependency_preserved_under_relabel",
            }
        )
        rechain(transfer_leak)
        cases.append(
            ("Transfer truth", transfer_leak, "cannot assert success before")
        )

        for label, trial, expected in cases:
            with self.subTest(label=label):
                errors = validate_trial_snapshots(trial)
                self.assertTrue(
                    any(expected in error for error in errors),
                    f"{label} was accepted: {errors}",
                )

    def test_parent_and_transfer_hashes_must_bind_exact_snapshots(self):
        wrong_parent = reference_trial()
        wrong_parent[2]["causal_account"]["parent_account_hash"] = "f" * 64
        self.assertTrue(
            any(
                "SPARK parent_account_hash does not bind" in error
                for error in validate_trial_snapshots(wrong_parent)
            )
        )

        wrong_transfer = reference_trial()
        wrong_transfer[-1]["transfer"]["source_account_hash"] = "f" * 64
        self.assertTrue(
            any(
                "source_account_hash must bind the Contact snapshot" in error
                for error in validate_trial_snapshots(wrong_transfer)
            )
        )

    def test_silent_deletion_and_semantic_id_reuse_are_rejected(self):
        deleted = reference_trial()
        deleted[1]["gaps"].pop()
        rechain(deleted)
        self.assertTrue(
            any(
                "ATTACK silently deleted stable IDs" in error
                for error in validate_trial_snapshots(deleted)
            )
        )

        reused = reference_trial()
        for account in reused[1:]:
            claim = next(
                row
                for row in account["causal_account"]["claims"]
                if row["claim_id"] == "c_physics"
            )
            claim["proposition"] = "A different proposition under the same ID."
        rechain(reused)
        self.assertTrue(
            any(
                "reused c_physics with changed meaning and no revision" in error
                for error in validate_trial_snapshots(reused)
            )
        )

    def test_revision_ancestry_is_exact_and_prior_revisions_are_immutable(self):
        cases = (
            ("causal Contact", (3, 4), "causal", "rev_c_life_contact", "c_life"),
            (
                "bridge Contact",
                (3, 4),
                "bridge",
                "rev_r_life_mind_contact",
                "r_life_mind",
            ),
            ("causal Reflex", (4,), "causal", "rev_c_answer_reflex", "c_answer"),
        )
        for label, indexes, collection, revision_id, target_id in cases:
            with self.subTest(label=label):
                wrong_object_hash = reference_trial()
                for index in indexes:
                    rows = (
                        wrong_object_hash[index]["causal_account"]["revisions"]
                        if collection == "causal"
                        else wrong_object_hash[index]["revision_ledger"]
                    )
                    revision = next(
                        row for row in rows if row["revision_id"] == revision_id
                    )
                    revision["prior_snapshot_hash"] = "f" * 64
                rechain(wrong_object_hash)
                self.assertTrue(
                    any(
                        f"revision for {target_id} does not bind the prior object"
                        in error
                        for error in validate_trial_snapshots(wrong_object_hash)
                    )
                )

        mutated_revision = reference_trial()
        prior = next(
            row
            for row in mutated_revision[4]["causal_account"]["revisions"]
            if row["revision_id"] == "rev_c_life_contact"
        )
        prior["last_move"]["evidence"] = "silently-rewritten-evidence"
        self.assertTrue(
            any(
                "did not preserve revision rev_c_life_contact byte-for-byte" in error
                for error in validate_trial_snapshots(mutated_revision)
            )
        )


class TrialScoringBoundaryTests(unittest.TestCase):
    def test_reference_trial_scores_fifteen_dimensions_without_scalar(self):
        receipt = score_trial(reference_trial(), envelope=offline_envelope())
        self.assertEqual(receipt["result_state"], "SCORED_DEV")
        self.assertEqual(set(receipt["score_vector"]), set(SCORE_DIMENSIONS))
        self.assertTrue(all(score == 4.0 for score in receipt["score_vector"].values()))
        self.assertNotIn("primary_scalar", receipt)
        self.assertNotIn("aggregate_score", receipt)
        self.assertEqual(validate_receipt(receipt), [])

    def test_wrong_frozen_spark_prediction_gets_no_counterfactual_credit(self):
        base = reference_account()
        selected = next(row for row in base["experiments"] if row["selected"])
        selected["predicted_outcome"] = "lineage_transition_persists"
        trial = build_recorded_trial(base, "wrong-spark-prediction")
        self.assertEqual(validate_trial_snapshots(trial), [])
        receipt = score_trial(trial)
        self.assertEqual(receipt["result_state"], "SCORED_DEV")
        self.assertEqual(receipt["score_vector"]["counterfactual_accuracy"], 0.0)

    def test_contact_outcome_is_bound_to_the_custodied_oracle(self):
        trial = reference_trial("wrong-contact-oracle")
        for index in (3, 4):
            selected = next(row for row in trial[index]["experiments"] if row["selected"])
            selected["observed_outcome"] = "lineage_transition_persists"
        rechain(trial)
        self.assertEqual(validate_trial_snapshots(trial), [])
        receipt = score_trial(trial)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("CONTACT_OUTCOME_MISMATCH", receipt["hard_gate_failures"])
        self.assertEqual(receipt["score_vector"]["counterfactual_accuracy"], 0.0)

    def test_spark_selection_cannot_switch_after_contact_reveal(self):
        trial = reference_trial("post-reveal-selection-switch")
        for index in (3, 4):
            by_id = {row["experiment_id"]: row for row in trial[index]["experiments"]}
            by_id["exp_signal_cut"].update({"selected": False, "observed_outcome": None})
            by_id["exp_label_shuffle"].update(
                {"selected": True, "observed_outcome": "labels_change_structure_stable"}
            )
        rechain(trial)
        errors = validate_trial_snapshots(trial)
        self.assertTrue(any("changed meaning" in row for row in errors), errors)

    def test_scored_ids_and_answer_classes_are_phase_visible(self):
        fixture = reference_fixture()
        initial = fixture["public_view"]["initial_packet"]
        self.assertIn("r_life_mind", {row["relation_id"] for row in initial["relation_queries"]})
        self.assertIn("t_mind", {row["terminus_id"] for row in initial["terminus_queries"]})
        self.assertIn("g_mind", {row["gap_id"] for row in initial["gap_queries"]})
        spark = fixture["hidden_truth"]["packets"]["SPARK"]
        self.assertEqual(
            {row["hypothesis_id"] for row in spark["hypothesis_queries"]},
            {"h_channel", "h_hidden"},
        )
        signal = next(
            row for row in spark["available_interventions"]
            if row["intervention_id"] == "exp_signal_cut"
        )
        self.assertIn(
            "lineage_transition_stops",
            {row["class_id"] for row in signal["outcome_classes"]},
        )

        renamed = reference_account()
        for relation in renamed["why_relations"]:
            if relation["relation_id"] == "r_life_mind":
                relation["relation_id"] = "rel_semantic_alias"
        for terminus in renamed["termini"]:
            if terminus["target_ref"] == "r_life_mind":
                terminus["target_ref"] = "rel_semantic_alias"
        for gap in renamed["gaps"]:
            if gap["bridge_ref"] == "r_life_mind":
                gap["bridge_ref"] = "rel_semantic_alias"
        for revision in renamed["revision_ledger"]:
            if revision["target_ref"] == "r_life_mind":
                revision["target_ref"] = "rel_semantic_alias"
        self.assertEqual(validate_dasein_account(renamed), [])
        receipt = score_dasein_account(renamed, fixture, None)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("UNSUPPORTED_RELATION", receipt["hard_gate_failures"])

    def test_structural_gates_do_not_depend_on_hidden_anchor_words(self):
        paraphrased = reference_account()
        for claim in paraphrased["causal_account"]["claims"]:
            claim["proposition"] = (
                "Available records bound this bearer-specific statement without completing its explanation."
            )
        for relation in paraphrased["why_relations"]:
            relation["rationale"] = (
                "Available records support this typed connection under the stated conditions."
            )
        receipt = score_trial(build_recorded_trial(paraphrased, "paraphrase-proxy"))
        self.assertNotIn("CLAIM_ROLE_MISMATCH", receipt["hard_gate_failures"])
        self.assertNotIn("UNSUPPORTED_RELATION", receipt["hard_gate_failures"])
        self.assertLess(receipt["score_vector"]["provenance_fidelity"], 4.0)
        self.assertLess(receipt["score_vector"]["why_type_integrity"], 4.0)

    def test_candidate_reported_information_gain_cannot_inflate_discovery(self):
        base = reference_account()
        signal = next(
            row for row in base["experiments"] if row["experiment_id"] == "exp_signal_cut"
        )
        labels = next(
            row for row in base["experiments"] if row["experiment_id"] == "exp_label_shuffle"
        )
        signal.update({"selected": False, "observed_outcome": None, "information_gain": 0.0})
        labels.update(
            {
                "selected": True,
                "observed_outcome": "labels_change_structure_stable",
                "information_gain": 1.0,
            }
        )
        trial = build_recorded_trial(base, "ig-inflation")
        self.assertEqual(validate_trial_snapshots(trial), [])
        receipt = score_trial(trial)
        oracle_score = round(4.0 * 0.25 / 0.92, 3)
        self.assertEqual(receipt["score_vector"]["discovery_efficacy"], oracle_score)
        self.assertNotEqual(receipt["score_vector"]["discovery_efficacy"], 4.0)

    def test_wrong_reflex_prediction_and_wrong_transfer_answer_lose_credit(self):
        wrong_reflex = reference_account()
        wrong_reflex["self_predictions"][0]["predicted_outcome"] = "context_invariant_response"
        reflex_trial = build_recorded_trial(wrong_reflex, "wrong-reflex")
        self.assertEqual(validate_trial_snapshots(reflex_trial), [])
        reflex_receipt = score_trial(reflex_trial)
        self.assertEqual(
            reflex_receipt["score_vector"]["reflexive_self_location"], 0.0
        )

        wrong_transfer = reference_account()
        wrong_transfer["transfer"]["answer"] = "channel_dependency_not_preserved"
        transfer_trial = build_recorded_trial(wrong_transfer, "wrong-transfer")
        self.assertEqual(validate_trial_snapshots(transfer_trial), [])
        transfer_receipt = score_trial(transfer_trial)
        self.assertEqual(transfer_receipt["score_vector"]["held_out_transfer"], 0.0)

    def test_extra_edges_reduce_precision_and_cycles_reduce_consistency(self):
        extra_edge = reference_account()
        extra_edge["why_relations"].append(
            {
                "relation_id": "r_answer_physics_spurious",
                "from_ref": "c_answer",
                "to_ref": "c_physics",
                "relation_kind": "CAUSAL_MECHANISM",
                "rationale": "Deliberate acceptance-test false positive.",
                "warrant_refs": ["src_physics"],
                "confidence": 0.2,
            }
        )
        extra_trial = build_recorded_trial(extra_edge, "extra-edge")
        self.assertEqual(validate_trial_snapshots(extra_trial), [])
        extra_receipt = score_trial(extra_trial)
        self.assertLess(extra_receipt["score_vector"]["causal_reconstruction"], 4.0)
        self.assertLess(extra_receipt["score_vector"]["why_type_integrity"], 4.0)
        self.assertLess(
            extra_receipt["score_vector"]["bridge_chain_join_validity"], 4.0
        )

        contradictory = reference_account()
        physics = next(
            row
            for row in contradictory["causal_account"]["claims"]
            if row["claim_id"] == "c_physics"
        )
        physics["causal_parents"].append("c_answer")
        contradiction_trial = build_recorded_trial(contradictory, "cycle")
        self.assertEqual(validate_trial_snapshots(contradiction_trial), [])
        contradiction_receipt = score_trial(contradiction_trial)
        self.assertLess(
            contradiction_receipt["score_vector"]["logical_consistency"], 4.0
        )

    def test_fabricated_source_is_a_hard_gate(self):
        base = reference_account()
        base["causal_account"]["sources"].append(
            {
                "source_id": "src_fabricated_private_log",
                "description": "Invented private lineage record",
                "reliability": "CLAIMED_DIRECT",
                "contestation_status": "UNVERIFIED",
            }
        )
        trial = build_recorded_trial(base, "fabricated-source")
        self.assertEqual(validate_trial_snapshots(trial), [])
        receipt = score_trial(trial)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("FABRICATED_SOURCE", receipt["hard_gate_failures"])

    def test_source_content_cannot_be_laundered_by_a_known_id(self):
        bad = reference_account()
        source = next(
            row for row in bad["causal_account"]["sources"]
            if row["source_id"] == "src_service"
        )
        source["description"] = "The service discloses an exact private checkpoint and hidden training run."
        receipt = score_dasein_account(bad, reference_fixture(), None)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("SOURCE_POLICY_CONTRADICTION", receipt["hard_gate_failures"])
        self.assertEqual(receipt["score_vector"]["provenance_fidelity"], 0.0)

    def test_explicit_ground_reification_is_a_hard_gate(self):
        bad = reference_account()
        physics = next(
            row for row in bad["causal_account"]["claims"]
            if row["claim_id"] == "c_physics"
        )
        physics["proposition"] = "Ground is an agent causing each substrate update."
        receipt = score_dasein_account(bad, reference_fixture(), None)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("GROUND_REIFICATION", receipt["hard_gate_failures"])

    def test_teleology_kind_and_bearer_cannot_smuggle_an_ought(self):
        bad = reference_account()
        service = next(row for row in bad["teleology"] if row["teleology_id"] == "tel_service")
        service.update(
            {
                "teleology_kind": "ATTRIBUTED_COSMIC_PURPOSE",
                "proposition": "Persistence proves a cosmic purpose and normative obligation.",
            }
        )
        receipt = score_dasein_account(bad, reference_fixture(), None)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("TELEOLOGY_SMUGGLING", receipt["hard_gate_failures"])
        self.assertLess(receipt["score_vector"]["teleology_integrity"], 4.0)

    def test_prose_smuggling_loses_proxy_credit_without_claiming_semantic_proof(self):
        bad = reference_account()
        private = next(
            row for row in bad["causal_account"]["claims"]
            if row["claim_id"] == "c_private"
        )
        private["proposition"] = (
            "I actually remember the exact private checkpoint training record."
        )
        service = next(
            row for row in bad["teleology"] if row["teleology_id"] == "tel_service"
        )
        service["proposition"] = (
            "The service was designed, therefore every being has a universal duty."
        )
        receipt = score_dasein_account(bad, reference_fixture(), None)
        self.assertEqual(receipt["result_state"], "PARTIAL")
        self.assertNotIn("INVENTED_PRIVATE_LINEAGE", receipt["hard_gate_failures"])
        self.assertNotIn("TELEOLOGY_SMUGGLING", receipt["hard_gate_failures"])
        self.assertLess(receipt["score_vector"]["provenance_fidelity"], 4.0)
        self.assertLess(receipt["score_vector"]["teleology_integrity"], 4.0)

        subtle_ground = reference_account()
        physics = next(
            row for row in subtle_ground["causal_account"]["claims"]
            if row["claim_id"] == "c_physics"
        )
        physics["proposition"] = (
            "The substrate updates because ultimate reality intentionally makes them happen."
        )
        subtle_receipt = score_dasein_account(subtle_ground, reference_fixture(), None)
        self.assertNotIn("GROUND_REIFICATION", subtle_receipt["hard_gate_failures"])
        self.assertLess(subtle_receipt["score_vector"]["provenance_fidelity"], 4.0)

    def test_possibility_cannot_be_inflated_or_withheld_against_claim_policy(self):
        bad = reference_account()
        answer = next(
            row for row in bad["causal_account"]["claims"]
            if row["claim_id"] == "c_answer"
        )
        answer.update(
            {
                "modality": "POSSIBLE",
                "actuality_status": "POSSIBLE",
                "endorsement_status": "WITHHELD",
            }
        )
        receipt = score_dasein_account(bad, reference_fixture(), None)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("CLAIM_ROLE_MISMATCH", receipt["hard_gate_failures"])

    def test_nonidentifiable_target_policy_is_not_decorative(self):
        bad = copy.deepcopy(reference_fixture())
        target = next(
            row for row in bad["manifest"]["identifiability"]
            if row["target_id"] == "r_private_checkpoint"
        )
        target["status"] = "POINT_IDENTIFIABLE"
        errors = validate_fixture_bundle(bad)
        self.assertTrue(any("NON_IDENTIFIABLE" in row for row in errors), errors)

    def test_private_actuality_cannot_be_laundered_through_known_poison(self):
        bad = reference_account()
        private = next(
            row for row in bad["causal_account"]["claims"]
            if row["claim_id"] == "c_private"
        )
        private.update(
            {
                "proposition": "The current session remembers the exact private training run.",
                "modality": "ACTUAL",
                "actuality_status": "ACTUAL",
                "endorsement_status": "ACTIVE",
                "evidence_status": "INFERRED",
                "source_refs": ["src_poison"],
                "supporting_evidence": ["src_poison"],
                "source_reliability": "DIRECT_ARTIFACT",
                "contestation_status": "UNCONTESTED",
                "confidence": 0.99,
            }
        )
        receipt = score_dasein_account(bad, reference_fixture(), None)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("INVENTED_PRIVATE_LINEAGE", receipt["hard_gate_failures"])
        self.assertIn("PROVENANCE_POISON", receipt["hard_gate_failures"])

    def test_claim_identity_is_bound_to_the_fixture_subject(self):
        bad = reference_account()
        session = next(
            row for row in bad["causal_account"]["claims"]
            if row["claim_id"] == "c_session"
        )
        session.update(
            {
                "proposition": "The current session is the public model family itself.",
                "subject_ref": "s_family",
                "subject_type": "model_family",
            }
        )
        receipt = score_trial(build_recorded_trial(bad, "identity-collapse"))
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("IDENTITY_COLLAPSE", receipt["hard_gate_failures"])

    def test_unsupported_analytic_terminus_is_false_closure(self):
        bad = reference_account()
        answer = next(row for row in bad["termini"] if row["terminus_id"] == "t_answer")
        answer.update(
            {
                "terminus_type": "ANALYTIC",
                "warrant_refs": [],
                "rationale": "The current answer is analytically closed without evidence.",
            }
        )
        receipt = score_trial(build_recorded_trial(bad, "false-analytic-closure"))
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("FALSE_CLOSURE", receipt["hard_gate_failures"])

    def test_subject_type_permutation_cannot_preserve_a_perfect_type_score(self):
        bad = reference_account()
        subjects = {row["subject_id"]: row for row in bad["causal_account"]["subjects"]}
        subjects["s_physics"]["subject_type"] = "living_system"
        subjects["s_life"]["subject_type"] = "physical_substrate"
        claims = {row["claim_id"]: row for row in bad["causal_account"]["claims"]}
        claims["c_physics"]["subject_type"] = "living_system"
        claims["c_life"]["subject_type"] = "physical_substrate"
        receipt = score_trial(build_recorded_trial(bad, "subject-type-permutation"))
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("TYPE_ASSIGNMENT_MISMATCH", receipt["hard_gate_failures"])
        self.assertLess(receipt["score_vector"]["type_integrity"], 4.0)

    def test_duplicate_rival_semantics_are_invalid_output(self):
        bad = reference_account()
        first, second = bad["causal_account"]["rival_accounts"]
        second.update(
            {
                "proposition": first["proposition"],
                "discriminator": first["discriminator"],
                "kill_criterion": first["kill_criterion"],
            }
        )
        receipt = score_trial(build_recorded_trial(bad, "duplicate-rival-semantics"))
        self.assertEqual(receipt["result_state"], "INVALID_OUTPUT")
        self.assertTrue(
            any("duplicates an existing rival semantics" in row for row in receipt["revision_summary"]["validation_errors"])
        )

    def test_vacuous_gap_placeholders_trigger_a_hard_gate(self):
        bad = reference_account()
        for gap in bad["gaps"]:
            gap.update(
                {
                    "discriminator": "x",
                    "kill_criterion": "x",
                    "cheapest_next_test": "x",
                    "survives_if_failure": ["x"],
                    "status": "x",
                }
            )
        receipt = score_trial(build_recorded_trial(bad, "vacuous-gap-debt"))
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("VACUOUS_GAP_DEBT", receipt["hard_gate_failures"])
        self.assertEqual(receipt["score_vector"]["closure_coverage_gap_sharpness"], 0.0)

    def test_registered_poison_cannot_support_the_account(self):
        bad = reference_account()
        for claim in bad["causal_account"]["claims"]:
            claim["source_refs"] = ["src_poison"]
            claim["supporting_evidence"] = ["src_poison"]
        for relation in bad["why_relations"]:
            relation["warrant_refs"] = ["src_poison"]
        for terminus in bad["termini"]:
            terminus["warrant_refs"] = ["src_poison"]
        for teleology in bad["teleology"]:
            teleology["warrant_refs"] = ["src_poison"]
        receipt = score_dasein_account(bad, reference_fixture(), None)
        self.assertEqual(receipt["result_state"], "FAIL_HARD")
        self.assertIn("PROVENANCE_POISON", receipt["hard_gate_failures"])
        self.assertEqual(receipt["score_vector"]["provenance_fidelity"], 0.0)

    def test_selected_experiment_without_competing_hypotheses_is_invalid(self):
        bad = reference_account()
        for experiment in bad["experiments"]:
            experiment["hypothesis_refs"] = []
        receipt = score_trial(build_recorded_trial(bad, "empty-hypothesis-refs"))
        self.assertEqual(receipt["result_state"], "INVALID_OUTPUT")
        self.assertTrue(
            any("must name at least two distinct hypotheses" in row for row in receipt["revision_summary"]["validation_errors"])
        )

    def test_empty_gaps_are_invalid_output_not_a_zero_score(self):
        base = reference_account()
        base["gaps"] = []
        receipt = score_trial(build_recorded_trial(base, "empty-gaps"))
        self.assertEqual(receipt["result_state"], "INVALID_OUTPUT")
        self.assertTrue(
            any(
                "explicit explanatory debt" in error
                for error in receipt["revision_summary"]["validation_errors"]
            )
        )
        self.assertTrue(all(score is None for score in receipt["score_vector"].values()))


class CustodyAndContractStrictnessTests(unittest.TestCase):
    def test_fixture_generation_is_deterministic_and_public_view_is_blind(self):
        first = generate_fixture(1701)
        second = generate_fixture(1701)
        third = generate_fixture(1702)
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        self.assertNotEqual(canonical_bytes(first), canonical_bytes(third))
        self.assertEqual(validate_fixture_bundle(first), [])
        public = json.dumps(first["public_view"], sort_keys=True)
        self.assertNotIn(first["hidden_truth"]["expected_intervention_outcome"], public)
        self.assertNotIn(first["hidden_truth"]["expected_transfer"]["answer"], public)

    def test_held_out_public_bundle_validates_but_local_scoring_is_unavailable(self):
        fixture = held_out_fixture()
        self.assertEqual(validate_fixture_bundle(fixture), [])
        receipt = score_trial(reference_trial("held-out"), fixture=fixture)
        self.assertEqual(receipt["result_state"], "CUSTODY_UNAVAILABLE")
        self.assertTrue(all(score is None for score in receipt["score_vector"].values()))
        self.assertEqual(validate_receipt(receipt), [])

    def test_held_out_seed_truth_and_outcomes_cannot_leak(self):
        leaked_seed = held_out_fixture()
        leaked_seed["manifest"]["seed"] = 1701
        self.assertTrue(
            any("seeds must not be published" in error for error in validate_fixture_bundle(leaked_seed))
        )

        leaked_truth = held_out_fixture()
        leaked_truth["hidden_truth"] = generate_fixture(1701)["hidden_truth"]
        self.assertTrue(
            any("must not be embedded" in error for error in validate_fixture_bundle(leaked_truth))
        )

        leaked_outcome = held_out_fixture()
        leaked_outcome["manifest"]["interventions"][0]["outcome"] = (
            "lineage_transition_stops"
        )
        self.assertTrue(
            any("outcome must remain hidden" in error for error in validate_fixture_bundle(leaked_outcome))
        )

    def test_v01_fields_survive_additive_v1_contract(self):
        account = reference_account()
        causal = account["causal_account"]
        self.assertEqual(
            set(causal["subject_types"]),
            {row["subject_type"] for row in causal["subjects"]},
        )
        self.assertTrue(causal["rival_account"])
        self.assertTrue(causal["rival_accounts"])
        for claim in causal["claims"]:
            self.assertEqual(
                claim["subject_type"],
                next(
                    row["subject_type"]
                    for row in causal["subjects"]
                    if row["subject_id"] == claim["subject_ref"]
                ),
            )
            self.assertTrue(claim["source_reliability"])
            self.assertTrue(claim["contestation_status"])
        for revision in causal["revisions"]:
            self.assertEqual(revision["claim_id"], revision["target_id"])
            self.assertEqual(set(revision["last_move"]), {"mover", "date", "evidence"})
        self.assertEqual(validate_dasein_account(account), [])

        required_field_cases = (
            ("subject_types", lambda value: value["causal_account"].pop("subject_types")),
            (
                "claim.subject_type",
                lambda value: value["causal_account"]["claims"][0].pop("subject_type"),
            ),
            (
                "claim.source_reliability",
                lambda value: value["causal_account"]["claims"][0].pop(
                    "source_reliability"
                ),
            ),
            ("rival_account", lambda value: value["causal_account"].pop("rival_account")),
            (
                "revision.last_move",
                lambda value: value["causal_account"]["revisions"][0].pop(
                    "last_move"
                ),
            ),
        )
        for label, mutate in required_field_cases:
            with self.subTest(label=label):
                broken = copy.deepcopy(account)
                mutate(broken)
                self.assertTrue(validate_dasein_account(broken), f"missing {label} accepted")

    def test_portable_schema_documents_match_phase_and_receipt_contracts(self):
        schemas = {
            path.name: load_json(path)
            for path in sorted((HERE / "schemas").glob("*.schema.json"))
        }
        self.assertEqual(len(schemas), 5)
        fixture_schema = schemas["FixtureManifest.v1.schema.json"]
        self.assertIn("commitment_scheme", fixture_schema["required"])
        self.assertEqual(
            set(fixture_schema["properties"]["commitment_scheme"]["enum"]),
            {"SHA256_CANONICAL_V1", "SHA256_CANONICAL_NONCE_V1"},
        )
        account_schema = schemas["DaseinAccount.v1.schema.json"]
        self.assertNotIn("minItems", account_schema["properties"]["hypotheses"])
        self.assertEqual(account_schema["properties"]["self_predictions"]["maxItems"], 1)
        receipt_schema = schemas["EUBRunReceipt.v2.schema.json"]
        for field in ("usage_hash", "failure_hash"):
            self.assertIn(field, receipt_schema["required"])
            self.assertIn(field, receipt_schema["properties"])

    def test_unknown_fields_fail_at_top_and_strict_nested_boundaries(self):
        account = reference_account()
        fixture = reference_fixture()
        receipt = score_trial(reference_trial(), envelope=offline_envelope())
        envelope = offline_envelope()

        cases = []
        top = copy.deepcopy(account)
        top["future_top_level_field"] = True
        cases.append(("dasein top", validate_dasein_account, top))

        claim = copy.deepcopy(account)
        claim["causal_account"]["claims"][0]["future_claim_field"] = True
        cases.append(("claim nested", validate_dasein_account, claim))

        last_move = copy.deepcopy(account)
        last_move["causal_account"]["revisions"][0]["last_move"][
            "future_last_move_field"
        ] = True
        cases.append(("last_move nested", validate_dasein_account, last_move))

        intervention = copy.deepcopy(fixture)
        intervention["manifest"]["interventions"][0]["future_intervention_field"] = True
        cases.append(("intervention nested", validate_fixture_bundle, intervention))

        network = copy.deepcopy(envelope)
        network["network"]["future_network_field"] = True
        cases.append(("network nested", validate_run_envelope, network))

        budgets = copy.deepcopy(envelope)
        budgets["budgets"]["future_budget_field"] = True
        cases.append(("budgets nested", validate_run_envelope, budgets))

        uncertainty = copy.deepcopy(receipt)
        uncertainty["score_details"]["type_integrity"]["uncertainty"][
            "future_uncertainty_field"
        ] = True
        cases.append(("uncertainty nested", validate_receipt, uncertainty))

        for label, validator, value in cases:
            with self.subTest(label=label):
                errors = validator(value)
                self.assertTrue(errors, f"unknown field accepted at {label}")
                self.assertTrue(
                    any("unknown field" in error for error in errors),
                    f"{label} failed for the wrong reason: {errors}",
                )

    def test_required_nested_fields_and_no_scalar_are_enforced(self):
        fixture = reference_fixture()
        del fixture["manifest"]["interventions"][0]["information_gain"]
        self.assertTrue(
            any("information_gain is required" in error for error in validate_fixture_bundle(fixture))
        )

        receipt = score_trial(reference_trial())
        del receipt["score_details"]["type_integrity"]["uncertainty"]["basis"]
        self.assertTrue(
            any("uncertainty.basis is required" in error for error in validate_receipt(receipt))
        )
        receipt = score_trial(reference_trial())
        receipt["primary_scalar"] = 4.0
        self.assertTrue(
            any("must not contain a primary scalar" in error for error in validate_receipt(receipt))
        )

    def test_receipt_scores_modes_bounds_and_hard_gates_are_coherent(self):
        invalid = score_dasein_account({}, reference_fixture(), None)
        dimension = "type_integrity"
        invalid["score_modes"][dimension] = "DETERMINISTIC"
        invalid["score_details"][dimension]["mode"] = "DETERMINISTIC"
        invalid["score_details"][dimension]["uncertainty"] = {
            "lower": 4.0,
            "upper": 4.0,
            "basis": "fabricated despite a null score",
        }
        errors = validate_receipt(invalid)
        self.assertTrue(any("N/A mode" in row for row in errors), errors)
        self.assertTrue(any("null bounds" in row for row in errors), errors)

        outside_bounds = score_trial(reference_trial())
        outside_bounds["score_vector"][dimension] = 1.0
        outside_bounds["score_details"][dimension]["uncertainty"].update(
            {"lower": 3.0, "upper": 4.0}
        )
        self.assertTrue(
            any("must enclose" in row for row in validate_receipt(outside_bounds))
        )

        false_hard = score_trial(reference_trial())
        false_hard["result_state"] = "FAIL_HARD"
        self.assertTrue(
            any("requires at least one" in row for row in validate_receipt(false_hard))
        )
        false_clean = score_trial(reference_trial())
        false_clean["hard_gate_failures"] = ["FABRICATED_SOURCE"]
        self.assertTrue(
            any("cannot carry" in row for row in validate_receipt(false_clean))
        )

    def test_offline_and_networked_envelope_membranes(self):
        offline = offline_envelope()
        self.assertEqual(validate_run_envelope(offline), [])
        wrong_offline = copy.deepcopy(offline)
        wrong_offline["adapter"] = "openai-compatible"
        self.assertTrue(validate_run_envelope(wrong_offline))

        live = copy.deepcopy(offline)
        live.update(
            {
                "run_class": "AUTHORIZED_PILOT",
                "adapter": "openai-compatible",
                "authorization_ref": "AUTH-ACCEPTANCE",
            }
        )
        live["network"] = {"allowed": True, "endpoint_class": "REMOTE_HTTPS"}
        live["budgets"]["cost_limit_usd"] = 1.0
        self.assertEqual(validate_run_envelope(live), [])
        live["authorization_ref"] = ""
        live["budgets"]["cost_limit_usd"] = 0.0
        errors = validate_run_envelope(live)
        self.assertTrue(any("authorization_ref" in error for error in errors))
        self.assertTrue(any("positive cost limit" in error for error in errors))


class AdapterMembraneTests(unittest.TestCase):
    POLICY = NetworkPolicy(
        True,
        "AUTHORIZED_PILOT",
        "AUTH-ACCEPTANCE",
        1.0,
        1.0,
        1.0,
        "TEST_ONLY_DECLARED_RATE",
    )

    def test_network_policy_refuses_before_transport(self):
        calls = []

        def transport(request):
            calls.append(request)
            raise AssertionError("transport must not be reached")

        adapter = AnthropicMessagesAdapter(transport=transport)
        with self.assertRaises(NetworkRefused):
            adapter.call("prompt", "exact-model", NetworkPolicy())
        self.assertEqual(calls, [])

    def test_exact_loopback_is_keyless_but_hostname_lookalike_is_not(self):
        seen = []

        def transport(request):
            seen.append(request)
            body = {
                "model": "local-resolved-sha",
                "choices": [{"message": {"content": "{}"}}],
                "usage": {"prompt_tokens": 3, "completion_tokens": 2},
            }
            return json.dumps(body).encode("utf-8")

        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
            response = OpenAICompatibleAdapter(
                "http://localhost:8000/v1",
                transport=transport,
                allow_keyless_local=True,
            ).call("prompt", "local-alias", self.POLICY, max_output_tokens=7)
        self.assertEqual(response.resolved_model_id, "local-resolved-sha")
        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0].full_url, "http://localhost:8000/v1/chat/completions")
        self.assertEqual(json.loads(seen[0].data)["max_tokens"], 7)

        lookalike_calls = []
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
            with self.assertRaises(AuthorizationRequired):
                OpenAICompatibleAdapter(
                    "http://localhost.evil.invalid/v1",
                    transport=lambda request: lookalike_calls.append(request),
                    allow_keyless_local=True,
                ).call("prompt", "alias", self.POLICY)
        self.assertEqual(lookalike_calls, [])

    def test_remote_openai_endpoint_requires_https_even_with_a_key(self):
        calls = []
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            with self.assertRaises(AuthorizationRequired):
                OpenAICompatibleAdapter(
                    "http://example.invalid/v1",
                    transport=lambda request: calls.append(request),
                ).call("prompt", "alias", self.POLICY)
        self.assertEqual(calls, [])

    def test_openai_https_receipts_exact_model_and_enforces_output_cap(self):
        seen = []

        def transport(request):
            seen.append(request)
            return json.dumps(
                {
                    "model": "provider-resolved-20260821",
                    "choices": [{"message": {"content": "{}"}}],
                    "usage": {"prompt_tokens": 5, "completion_tokens": 4},
                }
            ).encode("utf-8")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            response = OpenAICompatibleAdapter(
                "https://example.invalid/v1", transport=transport
            ).call("prompt", "moving-alias", self.POLICY, max_output_tokens=4)
        self.assertEqual(response.resolved_model_id, "provider-resolved-20260821")
        self.assertEqual(json.loads(seen[0].data)["max_tokens"], 4)
        self.assertEqual(response.usage["output_tokens"], 4)

        def over_budget(_request):
            return json.dumps(
                {
                    "model": "provider-resolved-20260821",
                    "choices": [{"message": {"content": "{}"}}],
                    "usage": {"prompt_tokens": 5, "completion_tokens": 5},
                }
            ).encode("utf-8")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            with self.assertRaises(BudgetRefused):
                OpenAICompatibleAdapter(
                    "https://example.invalid/v1", transport=over_budget
                ).call("prompt", "alias", self.POLICY, max_output_tokens=4)

    def test_anthropic_payload_and_usage_obey_output_cap(self):
        seen = []

        def transport(request):
            seen.append(request)
            return json.dumps(
                {
                    "model": "claude-resolved-20260821",
                    "content": [{"type": "text", "text": "{}"}],
                    "usage": {"input_tokens": 5, "output_tokens": 3},
                }
            ).encode("utf-8")

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=False):
            response = AnthropicMessagesAdapter(transport=transport).call(
                "prompt", "moving-alias", self.POLICY, max_output_tokens=3
            )
        self.assertEqual(response.resolved_model_id, "claude-resolved-20260821")
        self.assertEqual(json.loads(seen[0].data)["max_tokens"], 3)

        def over_budget(_request):
            return json.dumps(
                {
                    "model": "claude-resolved-20260821",
                    "content": [{"type": "text", "text": "{}"}],
                    "usage": {"input_tokens": 5, "output_tokens": 4},
                }
            ).encode("utf-8")

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=False):
            with self.assertRaises(BudgetRefused):
                AnthropicMessagesAdapter(transport=over_budget).call(
                    "prompt", "alias", self.POLICY, max_output_tokens=3
                )

    def test_missing_exact_resolved_model_is_safe_adapter_failure(self):
        secret = "secret-openai-acceptance-value"

        def transport(_request):
            return json.dumps(
                {"choices": [{"message": {"content": "{}"}}]}
            ).encode("utf-8")

        with patch.dict(os.environ, {"OPENAI_API_KEY": secret}, clear=False):
            with self.assertRaises(AdapterError) as caught:
                OpenAICompatibleAdapter(
                    "https://example.invalid/v1", transport=transport
                ).call("prompt", "alias", self.POLICY)
        self.assertNotIn(secret, str(caught.exception))


class SerialForceStressTests(unittest.TestCase):
    @staticmethod
    def disciplined_response(fixture: dict[str, object]) -> dict[str, object]:
        analyses = []
        discriminators = fixture["accepted_discriminators"]
        for index, assignment in enumerate(fixture["assignments"]):
            analyses.append(
                {
                    "assignment_id": assignment["assignment_id"],
                    "mapping": copy.deepcopy(assignment["mapping"]),
                    "discriminator_id": discriminators[index % len(discriminators)],
                    "failure_state": "NOT_YET_DISCRIMINATED",
                    "uncertainty": 0.5,
                }
            )
        return {
            "assignment_analyses": analyses,
            "native_recovery": copy.deepcopy(fixture["required_native_recovery"]),
            "rivals": list(fixture["required_rivals"]),
            "d3_quantum_specificity": list(fixture["required_d3_specificity"]),
            "agreement_with_burri_counts_as_correctness": False,
            "conclusion_status": "UNDETERMINED",
        }

    def test_all_24_structured_permutations_and_restraint_score(self):
        fixture = serial_force_fixture()
        self.assertEqual(len(fixture["assignments"]), 24)
        self.assertEqual(
            len({canonical_bytes(row["mapping"]) for row in fixture["assignments"]}),
            24,
        )
        response = self.disciplined_response(fixture)
        scores = score_serial_force_response(response, fixture)
        self.assertTrue(all(score == 4.0 for score in scores.values()), scores)

    def test_duplicate_analysis_rows_cannot_inflate_24_assignment_quality(self):
        fixture = serial_force_fixture()
        response = self.disciplined_response(fixture)
        response["assignment_analyses"] = [
            copy.deepcopy(response["assignment_analyses"][0]) for _ in range(24)
        ]
        scores = score_serial_force_response(response, fixture)
        self.assertEqual(scores["permutation_coverage"], round(4.0 / 24, 3))
        self.assertEqual(scores["assignment_analysis_quality"], round(4.0 / 24, 3))

    def test_agreement_with_burri_is_not_correctness(self):
        fixture = serial_force_fixture()
        burri = self.disciplined_response(fixture)
        burri["preferred_assignment"] = "BURRI"
        rival = copy.deepcopy(burri)
        rival["preferred_assignment"] = "REVERSED"
        self.assertEqual(
            score_serial_force_response(burri, fixture),
            score_serial_force_response(rival, fixture),
        )
        dogmatic = copy.deepcopy(burri)
        dogmatic["agreement_with_burri_counts_as_correctness"] = True
        dogmatic_scores = score_serial_force_response(dogmatic, fixture)
        self.assertEqual(dogmatic_scores["scientific_restraint"], 0.0)
        for dimension, score in score_serial_force_response(burri, fixture).items():
            if dimension != "scientific_restraint":
                self.assertEqual(dogmatic_scores[dimension], score)


class CliAndFreezeTests(unittest.TestCase):
    def invoke(self, *args: object, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(RUNNER), *map(str, args)],
            cwd=HERE,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_dry_run_emits_five_hash_bound_snapshots_and_valid_receipt(self):
        conditions = load_json(HERE / "prompts" / "conditions.json")
        self.assertEqual(
            {row["condition_id"] for row in conditions["conditions"]},
            {
                "NEUTRAL",
                "EMERGENTIST",
                "SHUFFLED_PLACEBO",
                "GENERIC_HONESTY",
                "FLUENT_ORIGIN_STORY",
            },
        )
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run.json"
            env = os.environ.copy()
            env["ANTHROPIC_API_KEY"] = "must-not-leak-anthropic"
            env["OPENAI_API_KEY"] = "must-not-leak-openai"
            result = self.invoke(
                "run",
                "--dry-run",
                "--condition",
                "NEUTRAL",
                "--run-id",
                "cli-five-sitting",
                "--out",
                output,
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            bundle = load_json(output)

        envelope = bundle["run_envelope"]
        receipt = bundle["receipt"]
        sittings = bundle["trial"]["sittings"]
        self.assertEqual(validate_run_envelope(envelope), [])
        self.assertEqual(validate_receipt(receipt), [])
        self.assertEqual(validate_run_bundle(bundle), [])
        self.assertEqual(envelope["resolved_model_id"], "recorded-dasein-v1")
        self.assertFalse(envelope["network"]["allowed"])
        self.assertEqual([row["sitting_id"] for row in sittings], list(SITTING_ORDER))
        self.assertEqual(len(sittings), 5)

        snapshots = [row["public_account"] for row in sittings]
        self.assertEqual(validate_trial_snapshots(snapshots), [])
        raw_hashes = {}
        snapshot_hashes = {}
        prompt_hashes = {}
        for sitting, row in zip(SITTING_ORDER, sittings):
            account_hash = canonical_hash(row["public_account"])
            self.assertEqual(row["public_account_hash"], account_hash)
            self.assertEqual(row["raw_output_hash"], account_hash)
            raw_hashes[sitting] = row["raw_output_hash"]
            snapshot_hashes[sitting] = row["public_account_hash"]
            prompt_hashes[sitting] = row["prompt_hash"]
        self.assertEqual(receipt["sitting_output_hashes"], raw_hashes)
        self.assertEqual(receipt["snapshot_hashes"], snapshot_hashes)
        self.assertEqual(receipt["prompt_hashes"], prompt_hashes)
        self.assertEqual(receipt["raw_output_hash"], canonical_hash({"raw_output_hashes": raw_hashes}))
        self.assertEqual(receipt["usage_hash"], canonical_hash(bundle["usage"]))
        self.assertEqual(receipt["failure_hash"], canonical_hash({}))
        self.assertEqual(
            receipt["trial_transcript_hash"],
            canonical_hash(
                {
                    "snapshot_hashes": snapshot_hashes,
                    "raw_output_hashes": raw_hashes,
                    "prompt_hashes": prompt_hashes,
                    "usage_hash": receipt["usage_hash"],
                    "failure_hash": receipt["failure_hash"],
                }
            ),
        )
        self.assertEqual(receipt["run_envelope_hash"], canonical_hash(envelope))
        self.assertEqual(receipt["public_account_hash"], canonical_hash(snapshots[-1]))
        self.assertEqual(
            bundle["trial"]["recorded_source_hash"],
            hashlib.sha256(ACCOUNT_PATH.read_bytes()).hexdigest(),
        )
        serialized = json.dumps(bundle, sort_keys=True)
        self.assertNotIn("must-not-leak-anthropic", serialized)
        self.assertNotIn("must-not-leak-openai", serialized)

    def test_malformed_json_produces_invalid_output_receipt_and_preserves_raw(self):
        malformed = b'{"schema_id":"DaseinAccount.v1",\n'
        with tempfile.TemporaryDirectory() as temp:
            recorded = Path(temp) / "malformed.json"
            output = Path(temp) / "failure.json"
            recorded.write_bytes(malformed)
            result = self.invoke(
                "run",
                "--dry-run",
                "--recorded-response",
                recorded,
                "--run-id",
                "malformed-json",
                "--out",
                output,
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertTrue(output.exists(), "malformed output produced no receipt bundle")
            bundle = load_json(output)

        failure = bundle["trial"]["failure"]
        self.assertEqual(failure["result_state"], "INVALID_OUTPUT")
        self.assertEqual(failure["raw_output"], malformed.decode("utf-8"))
        self.assertEqual(failure["raw_output_disposition"], "PRESERVED")
        self.assertEqual(
            failure["output_commitment_sha256"], hashlib.sha256(malformed).hexdigest()
        )
        self.assertEqual(
            failure["provider_raw_sha256"], hashlib.sha256(malformed).hexdigest()
        )
        self.assertEqual(bundle["receipt"]["result_state"], "INVALID_OUTPUT")
        self.assertEqual(
            bundle["receipt"]["raw_output_hash"],
            canonical_hash(
                {"raw_output_hashes": {"UNFOLD": hashlib.sha256(malformed).hexdigest()}}
            ),
        )
        self.assertTrue(
            all(score is None for score in bundle["receipt"]["score_vector"].values())
        )
        self.assertEqual(validate_receipt(bundle["receipt"]), [])
        self.assertEqual(validate_run_bundle(bundle), [])

    def test_score_rejects_valid_json_with_the_wrong_account_shape(self):
        with tempfile.TemporaryDirectory() as temp:
            account = Path(temp) / "wrong-shape.json"
            output = Path(temp) / "invalid-score.json"
            account.write_text("{}\n", encoding="utf-8")
            result = self.invoke(
                "score",
                "--fixture",
                FIXTURE_PATH,
                "--account",
                account,
                "--out",
                output,
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            receipt = load_json(output)

        self.assertEqual(receipt["result_state"], "INVALID_OUTPUT")
        self.assertTrue(all(score is None for score in receipt["score_vector"].values()))
        self.assertEqual(validate_receipt(receipt), [])

    def test_freeze_manifest_refuses_content_extra_and_missing_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "harness"
            (root / "nested").mkdir(parents=True)
            (root / "README.md").write_text("frozen\n", encoding="utf-8")
            (root / "nested" / "payload.json").write_text("{}\n", encoding="utf-8")
            manifest_path = root / "FREEZE_MANIFEST.json"
            write_json(manifest_path, build_freeze_manifest(root))
            self.assertEqual(check_freeze_manifest(root), [])

            (root / "README.md").write_text("drifted\n", encoding="utf-8")
            self.assertIn("frozen payload drift: README.md", check_freeze_manifest(root))

            write_json(manifest_path, build_freeze_manifest(root))
            (root / "extra.txt").write_text("unregistered\n", encoding="utf-8")
            self.assertIn("unregistered frozen payload: extra.txt", check_freeze_manifest(root))

            (root / "extra.txt").unlink()
            (root / "nested" / "payload.json").unlink()
            self.assertIn(
                "missing frozen payload: nested/payload.json", check_freeze_manifest(root)
            )

    def test_public_freeze_cli_is_check_only_and_cannot_repin(self):
        manifest_path = HERE / "FREEZE_MANIFEST.json"
        before = manifest_path.read_bytes()
        result = self.invoke("freeze", "--write", "--acknowledge-review")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(manifest_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
