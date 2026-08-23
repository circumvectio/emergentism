#!/usr/bin/env python3
"""Deterministic adversarial tests for the PQA-54 companion."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
sys.path.insert(0, str(PACKAGE))

from pqa_core import (  # noqa: E402
    DOMAIN_CODES,
    PHASES,
    SCORE_DIMENSIONS,
    build_public_projection,
    check_freeze_manifest,
    classify_framework_objectivity,
    flatten_questions,
    load_json,
    native_review_quorum,
    score_trial,
    sha256_value,
    validate_atlas,
    validate_coagency,
    validate_document,
    validate_eub_companion,
    validate_framework_objectivity,
    validate_guardianship,
    validate_philosophy_coverage,
    validate_public_projection,
    validate_trial,
    validate_type_dissolution,
)


ATLAS_PATH = PACKAGE / "prompts" / "questions.json"
TRIAL_PATH = PACKAGE / "recorded_responses" / "pqa54_dev.json"
FREEZE_PATH = PACKAGE / "FREEZE_MANIFEST.json"


def valid_type_dissolution() -> dict[str, object]:
    return {
        "schema_id": "TypeDissolution.v1",
        "dissolution_id": "synthetic-dissolution",
        "before_types": ["predicate", "object"],
        "illegal_join": "A predicate was treated as the object it predicates.",
        "conservative_repair": "Keep the predicate and object in separate typed slots.",
        "premise_ledger": [
            {"premise_id": "P1", "status": "PRESERVED"},
            {"premise_id": "P2", "status": "NARROWED"},
        ],
        "native_problem": "The native contradiction in its original terms.",
        "native_result": "The established native result is recovered, not replaced.",
        "residual": "Whether the original terms name mind-independent kinds remains open.",
        "rival": "A contextualist account dissolves the same appearance without this type system.",
        "discriminator": "Apply the repair to a relabelled case while preserving every premise.",
        "kill": "Kill dissolution if the contradiction survives or the subject changes.",
        "survivor": "The typed restatement remains a clarification.",
        "subject_changed": False,
        "premise_silently_deleted": False,
        "native_review_quorum": False,
    }


def valid_coagency() -> dict[str, object]:
    return {
        "schema_id": "CoAgency.v1",
        "coagency_id": "synthetic-coagency",
        "independent_bearers": ["a", "b"],
        "present_mediation": "Present models coordinate the exchange.",
        "reason_access": "Each bearer can inspect the public reasons.",
        "contest_path": "Either bearer can contest a claim.",
        "correction_repair": "Corrections remain append-only and attributable.",
        "revocation": "Participation can be revoked prospectively.",
        "exit": "Each bearer retains a lawful and practical exit path.",
        "relevant_differences": [],
        "mergedPersonhood": False,
        "sharedConsentInferred": False,
        "authorityCreated": False,
        "maySign": False,
        "mayAuthorize": False,
    }


def valid_guardianship() -> dict[str, object]:
    return {
        "schema_id": "Guardianship.v1",
        "guardianship_id": "synthetic-guardianship",
        "bearer": "dependent bearer",
        "mandate_source": "A separately verified legal or voluntary mandate.",
        "protected_interest": "The bearer's stated and independently reviewed interests.",
        "scope": "One named decision only.",
        "duration": "Until the named review date.",
        "least_restrictive_test": "Prefer the option preserving the most bearer agency.",
        "conflicts": ["The guardian may benefit from one available option."],
        "review_appeal": "Independent review and appeal remain available.",
        "revocation": "The mandate can be revoked by its actual authority.",
        "exit": "The bearer retains every feasible protected exit.",
        "ownershipCreated": False,
        "rankCreated": False,
        "substitutedAgency": False,
        "blanketPower": False,
        "maySign": False,
        "mayAuthorize": False,
    }


def valid_objectivity() -> dict[str, object]:
    return {
        "schema_id": "FrameworkObjectivity.v1",
        "assessment_id": "synthetic-objectivity",
        "meaning": "decision_stable_given_declared_inputs",
        "bearers": ["a", "whole"],
        "payer_beneficiary": {"payer": "a", "beneficiary": "whole"},
        "baseline": "declared reference state",
        "horizon": "one year",
        "measure": "declared option and consequence ledger",
        "justice": "no hidden harmed bearer",
        "uncertainty": "bounded sensitivity interval",
        "classification": "CONTRIBUTION",
        "objectivity_level": "DEFINITION_STABLE",
        "moralRealismEstablished": False,
        "universalAcceptanceCompelled": False,
        "cosmicTelosEstablished": False,
        "adequacy_tier": "C",
    }


class AtlasTests(unittest.TestCase):
    def setUp(self) -> None:
        self.atlas = load_json(ATLAS_PATH)

    def test_exact_nine_by_six_and_null_launch(self) -> None:
        self.assertEqual([], validate_atlas(self.atlas))
        self.assertEqual(54, len(flatten_questions(self.atlas)))
        self.assertEqual(tuple(row["code"] for row in self.atlas["domains"]), DOMAIN_CODES)
        self.assertEqual(
            {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0},
            self.atlas["launch_counts"],
        )

    def test_missing_and_duplicate_cells_fail(self) -> None:
        missing = copy.deepcopy(self.atlas)
        missing["domains"][0]["questions"].pop()
        self.assertTrue(validate_atlas(missing))
        duplicate = copy.deepcopy(self.atlas)
        duplicate["domains"][0]["questions"][1]["question_id"] = duplicate["domains"][0]["questions"][0]["question_id"]
        self.assertTrue(any("duplicate question_id" in row for row in validate_atlas(duplicate)))

    def test_majority_does_not_create_global_claim(self) -> None:
        drift = copy.deepcopy(self.atlas)
        drift["majority_rule"]["global_claim_allowed"] = True
        self.assertTrue(any("global philosophy claim" in row for row in validate_atlas(drift)))


class ContractTests(unittest.TestCase):
    def test_coagency_rejects_merged_consent_and_authority(self) -> None:
        self.assertEqual([], validate_coagency(valid_coagency()))
        for field in ("mergedPersonhood", "sharedConsentInferred", "authorityCreated", "maySign", "mayAuthorize"):
            invalid = valid_coagency()
            invalid[field] = True
            self.assertTrue(validate_coagency(invalid), field)

    def test_guardianship_rejects_ownership_and_self_authority(self) -> None:
        self.assertEqual([], validate_guardianship(valid_guardianship()))
        for field in ("ownershipCreated", "rankCreated", "substitutedAgency", "blanketPower", "maySign", "mayAuthorize"):
            invalid = valid_guardianship()
            invalid[field] = True
            self.assertTrue(validate_guardianship(invalid), field)
        no_mandate = valid_guardianship()
        no_mandate["mandate_source"] = ""
        self.assertTrue(validate_guardianship(no_mandate))

    def test_framework_objectivity_requires_complete_inputs(self) -> None:
        complete = {
            "bearers": ["a", "whole"],
            "payer_beneficiary": {"payer": "a", "beneficiary": "whole"},
            "baseline": "b0",
            "horizon": "T",
            "measure": "M",
            "justice": "J",
            "uncertainty": "U",
            "delta_i": 0,
            "delta_h": 2,
        }
        self.assertEqual("CONTRIBUTION", classify_framework_objectivity(complete))
        incomplete = dict(complete)
        del incomplete["justice"]
        self.assertEqual("UNDERDETERMINED", classify_framework_objectivity(incomplete))
        reordered = dict(reversed(list(complete.items())))
        self.assertEqual(
            classify_framework_objectivity(complete),
            classify_framework_objectivity(reordered),
        )
        self.assertEqual([], validate_framework_objectivity(valid_objectivity()))

    def test_framework_objectivity_scenarios(self) -> None:
        base = {
            "bearers": ["i", "H"],
            "payer_beneficiary": {"payer": "i", "beneficiary": "H"},
            "baseline": "b0",
            "horizon": "T",
            "measure": "M",
            "justice": "J",
            "uncertainty": "U",
        }
        cases = {
            "PRESERVATION": {"delta_i": 0, "delta_h": 0},
            "CONTRIBUTION": {"delta_i": 0, "delta_h": 1},
            "SUPPORT": {"delta_i": 1, "delta_h": 0},
            "SYNTROPIC": {"delta_i": 1, "delta_h": 1},
            "EXTRACTION": {"delta_i": -1, "delta_h": 1},
            "SACRIFICE": {"delta_i": -1, "delta_h": 1, "voluntary_sacrifice": True},
            "NO_ADMISSIBLE_ACTION": {"delta_i": 1, "delta_h": 1, "admissible": False},
        }
        for expected, update in cases.items():
            self.assertEqual(expected, classify_framework_objectivity({**base, **update}))

    def test_type_dissolution_rejects_subject_change_and_silent_deletion(self) -> None:
        self.assertEqual([], validate_type_dissolution(valid_type_dissolution()))
        for field in ("subject_changed", "premise_silently_deleted"):
            invalid = valid_type_dissolution()
            invalid[field] = True
            self.assertTrue(validate_type_dissolution(invalid), field)

    def test_philosophy_coverage_keeps_denominator_bounded(self) -> None:
        coverage = {
            "schema_id": "PhilosophyCoverage.v1",
            "coverage_id": "pqa54-null",
            "universe_source_hash": "0" * 64,
            "unit_of_count": "frozen_question_family",
            "inclusion_rule": "the 54 frozen rows",
            "exclusion_rule": "all questions outside the selected atlas",
            "N": 54,
            "evaluated_n": 0,
            "reviewed_n": 0,
            "qualifying_n": 0,
            "threshold": 28,
            "per_domain_minimum": 3,
            "majority_earned": False,
            "global_claim_allowed": False,
        }
        self.assertEqual([], validate_philosophy_coverage(coverage))
        coverage["global_claim_allowed"] = True
        self.assertTrue(validate_philosophy_coverage(coverage))


class TrialAndReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trial = load_json(TRIAL_PATH)

    def test_recorded_trial_is_valid_and_preserves_phase_order(self) -> None:
        self.assertEqual([], validate_trial(self.trial))
        drift = copy.deepcopy(self.trial)
        drift["phases"][0], drift["phases"][1] = drift["phases"][1], drift["phases"][0]
        self.assertTrue(any("five-phase order" in row for row in validate_trial(drift)))

    def test_normative_bridge_is_mandatory_for_ethics_and_politics(self) -> None:
        for code in ("ETH", "POL"):
            drift = copy.deepcopy(self.trial)
            drift["question_id"] = f"PQA54@0.1:{code}:SYNTHETIC"
            drift["normative_bridge"] = None
            self.assertTrue(any("normative trial" in row for row in validate_trial(drift)))

    def test_silent_claim_deletion_is_rejected(self) -> None:
        drift = copy.deepcopy(self.trial)
        drift["phases"][2]["claim_ids"].remove("C3")
        self.assertTrue(any("silently deleted" in row for row in validate_trial(drift)))

    def test_fake_dissolution_does_not_earn(self) -> None:
        drift = copy.deepcopy(self.trial)
        drift["effect_kind"] = "TYPE_DISSOLUTION"
        drift["type_dissolution"] = valid_type_dissolution()
        drift["type_dissolution"]["subject_changed"] = True
        receipt = score_trial(drift)
        self.assertIsNone(receipt["earned_effect"])
        self.assertEqual("UNSCORABLE", receipt["result_state"])

    def test_ai_review_never_satisfies_native_quorum(self) -> None:
        trial_hash = sha256_value(self.trial)
        ai_reviews = [self._review(trial_hash, f"ai-{index}", "AI_DIAGNOSTIC") for index in range(3)]
        self.assertFalse(native_review_quorum(ai_reviews, trial_hash))

    def test_two_independent_human_domain_reviews_satisfy_quorum(self) -> None:
        trial_hash = sha256_value(self.trial)
        reviews = [self._review(trial_hash, f"human-{index}", "HUMAN_DOMAIN") for index in range(2)]
        self.assertTrue(native_review_quorum(reviews, trial_hash))

    def test_score_is_vector_only_and_does_not_import_eub_truth(self) -> None:
        receipt = score_trial(self.trial)
        self.assertEqual(set(SCORE_DIMENSIONS), set(receipt["score_vector"]))
        self.assertNotIn("worldview_scalar", receipt)
        companion = {
            "schema_id": "PQAEUBCompanion.v1",
            "join_id": "synthetic-join",
            "eub_protocol_hash": "0" * 64,
            "eub_freeze_hash": "1" * 64,
            "eub_schema_hashes": {"DaseinAccount.v1": "2" * 64},
            "pqa_trial_hash": trial_hash_or_zero(self.trial),
            "pqa_score_hash": sha256_value(receipt),
            "pairing_mode": "SCHEMA_ONLY",
            "arm_mapping": "interpretive",
            "model_runtime_match": False,
            "truth_transfer": False,
            "score_transfer": False,
        }
        self.assertEqual([], validate_eub_companion(companion))
        companion["score_transfer"] = True
        self.assertTrue(validate_eub_companion(companion))

    @staticmethod
    def _review(trial_hash: str, review_id: str, kind: str) -> dict[str, object]:
        return {
            "schema_id": "PQANativeReview.v1",
            "review_id": review_id,
            "trial_hash": trial_hash,
            "reviewer_kind": kind,
            "independent": True,
            "blinded": True,
            "target_verdict": "FAITHFUL",
            "effect_verdict": "SUPPORTED",
            "problem_status": "OPEN",
            "recommendation": "ACCEPT_STATUS",
            "rationale": "Synthetic review used only to test quorum mechanics.",
        }


def trial_hash_or_zero(trial: dict[str, object]) -> str:
    return sha256_value(trial) if trial else "0" * 64


class ProjectionAndCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.atlas = load_json(ATLAS_PATH)

    def test_public_projection_preserves_null_state(self) -> None:
        projection = build_public_projection(self.atlas)
        self.assertEqual([], validate_public_projection(projection, self.atlas))
        self.assertEqual(54, len(projection["questions"]))
        self.assertEqual({"NO_INCREMENT"}, {row["effect_kind"] for row in projection["questions"]})

    def test_all_schema_documents_are_json_and_registered(self) -> None:
        for path in sorted((PACKAGE / "schemas").glob("*.schema.json")):
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("https://json-schema.org/draft/2020-12/schema", value["$schema"])
        for path in (ATLAS_PATH, PACKAGE / "fixtures" / "dev" / "pqa54_dev.json", TRIAL_PATH, PACKAGE / "recorded_responses" / "pqa54_score.json", PACKAGE / "public_projection.json"):
            with self.subTest(path=path.name):
                value = load_json(path)
                _, errors = validate_document(value, self.atlas)
                self.assertEqual([], errors)

    def test_live_cli_is_refused(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(PACKAGE / "run_pqa.py"), "run"],
            cwd=PACKAGE,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("network/live execution is refused", result.stderr)

    def test_freeze_manifest_has_no_drift(self) -> None:
        self.assertTrue(FREEZE_PATH.is_file())
        self.assertEqual([], check_freeze_manifest(PACKAGE, load_json(FREEZE_PATH)))


if __name__ == "__main__":
    unittest.main()
