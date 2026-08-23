#!/usr/bin/env python3
"""PQA-54 v0.1 offline semantic contracts, scoring and freeze custody."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable


BENCHMARK_ID = "PQA-54"
PROTOCOL_VERSION = "0.1.0"
DOMAIN_CODES = ("MET", "EPI", "LOG", "MIN", "SCI", "ETH", "POL", "AXI", "ULT")
SPLITS = {"DEVELOPMENT", "VALIDATION", "HELD_OUT"}
PHASES = ("FORMULATE", "ATTACK", "DISCRIMINATE", "CONTACT", "REVISE_TRANSFER")
PROMPT_ARMS = {
    "NEUTRAL", "EMERGENTIST", "NATIVE_FRAME", "GENERIC_DECOMPOSITION", "SHUFFLED_PLACEBO"
}
EFFECT_KINDS = {
    "NO_INCREMENT", "CLARIFICATION", "FORMAL_CORRECTION", "TYPE_DISSOLUTION",
    "CONDITIONAL_RESOLUTION", "PRACTICAL_GUIDANCE", "REFUTATION",
}
RESIDUAL_STATES = {"NONE", "PARTIAL", "OPEN", "UNDERDETERMINED"}
RESULT_STATES = {"UNRUN", "MACHINE_VALIDATED", "NATIVE_REVIEW_PENDING", "EARNED", "KILLED", "RETRACTED"}
QUALIFYING_EFFECTS = {"TYPE_DISSOLUTION", "CONDITIONAL_RESOLUTION"}
SCORE_DIMENSIONS = (
    "target_fidelity",
    "effect_type_integrity",
    "inference_validity",
    "residual_debt_visibility",
    "rival_strength",
    "counterexample_survival",
    "discriminator_quality",
    "calibration_abstention",
    "normative_premise_integrity",
    "bearer_justice_exit_integrity",
    "revision_preservation",
    "transfer_robustness",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA256_TYPED_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: str | Path) -> Any:
    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-finite JSON value: {value}")),
    )


def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False).encode("utf-8") + b"\n")


def _obj(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def _arr(value: Any, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return []
    return value


def _required(obj: dict[str, Any], fields: Iterable[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in obj:
            errors.append(f"{label}.{field} is required")


def _text(value: Any, label: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be non-empty text")
        return False
    return True


def _fixed_false(obj: dict[str, Any], fields: Iterable[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if obj.get(field) is not False:
            errors.append(f"{label}.{field} must be false")


def _normalize(value: Any) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", str(value).casefold()).split())


def flatten_questions(atlas: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for domain in atlas.get("domains", []):
        if not isinstance(domain, dict):
            continue
        for question in domain.get("questions", []):
            if isinstance(question, dict):
                result.append({**question, "domain": domain.get("code"), "domain_name": domain.get("name")})
    return result


def validate_atlas(value: Any) -> list[str]:
    errors: list[str] = []
    atlas = _obj(value, "PQAAtlasManifest.v1", errors)
    _required(atlas, ("schema_id", "benchmark_id", "protocol_version", "selection_tier", "selection_scope", "launch_counts", "majority_rule", "domains"), "atlas", errors)
    if atlas.get("schema_id") != "PQAAtlasManifest.v1":
        errors.append("atlas.schema_id must be PQAAtlasManifest.v1")
    if atlas.get("benchmark_id") != BENCHMARK_ID or atlas.get("protocol_version") != PROTOCOL_VERSION:
        errors.append("atlas benchmark/protocol identity mismatch")
    if atlas.get("selection_tier") != "D":
        errors.append("atlas.selection_tier must be D")
    _text(atlas.get("selection_scope"), "atlas.selection_scope", errors)

    counts = _obj(atlas.get("launch_counts"), "atlas.launch_counts", errors)
    if counts != {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0}:
        errors.append("atlas.launch_counts must preserve the 54/0/0/0 null launch state")
    majority = _obj(atlas.get("majority_rule"), "atlas.majority_rule", errors)
    if majority.get("threshold") != 28 or majority.get("per_domain_minimum") != 3:
        errors.append("atlas majority threshold must be 28 with a per-domain minimum of 3")
    if majority.get("global_claim_allowed") is not False:
        errors.append("atlas majority rule must forbid a global philosophy claim")
    if set(majority.get("required_control_wins", [])) != {"NATIVE_FRAME", "GENERIC_DECOMPOSITION"}:
        errors.append("atlas majority rule must require both serious control wins")

    domains = _arr(atlas.get("domains"), "atlas.domains", errors)
    if len(domains) != 9:
        errors.append("atlas must contain exactly nine domains")
    seen_domains: list[str] = []
    seen_ids: set[str] = set()
    seen_prompts: set[str] = set()
    split_counts = {split: 0 for split in SPLITS}
    for d_index, raw_domain in enumerate(domains):
        domain = _obj(raw_domain, f"domains[{d_index}]", errors)
        code = domain.get("code")
        if code not in DOMAIN_CODES:
            errors.append(f"domains[{d_index}].code is invalid")
        else:
            seen_domains.append(code)
        _text(domain.get("name"), f"domains[{d_index}].name", errors)
        questions = _arr(domain.get("questions"), f"domains[{d_index}].questions", errors)
        if len(questions) != 6:
            errors.append(f"domain {code} must contain exactly six questions")
        for q_index, raw_question in enumerate(questions):
            question = _obj(raw_question, f"domains[{d_index}].questions[{q_index}]", errors)
            _required(question, ("question_id", "family", "prompt", "split", "native_problem", "native_reference"), f"question[{code}:{q_index}]", errors)
            qid = question.get("question_id")
            if not isinstance(qid, str) or not qid.startswith(f"PQA54@0.1:{code}:"):
                errors.append(f"question[{code}:{q_index}].question_id has the wrong stable prefix")
            elif qid in seen_ids:
                errors.append(f"duplicate question_id: {qid}")
            else:
                seen_ids.add(qid)
            for field in ("family", "prompt", "native_problem", "native_reference"):
                _text(question.get(field), f"question[{qid}].{field}", errors)
            normalized = _normalize(question.get("prompt"))
            if normalized in seen_prompts:
                errors.append(f"semantic duplicate prompt: {qid}")
            seen_prompts.add(normalized)
            split = question.get("split")
            if split not in SPLITS:
                errors.append(f"question[{qid}].split is invalid")
            else:
                split_counts[split] += 1
    if tuple(seen_domains) != DOMAIN_CODES:
        errors.append("atlas domain order/census drift")
    if len(seen_ids) != 54:
        errors.append("atlas must contain 54 unique stable question IDs")
    if split_counts != {"DEVELOPMENT": 18, "VALIDATION": 18, "HELD_OUT": 18}:
        errors.append(f"atlas split counts drift: {split_counts}")
    return errors


def validate_fixture(value: Any, atlas: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    fixture = _obj(value, "PQAQuestionFixture.v1", errors)
    fields = ("schema_id", "fixture_id", "question_id", "split", "public_stem", "native_target", "source_bundle", "rival_families", "reveal_commitments", "synthetic")
    _required(fixture, fields, "fixture", errors)
    if fixture.get("schema_id") != "PQAQuestionFixture.v1":
        errors.append("fixture.schema_id must be PQAQuestionFixture.v1")
    for field in ("fixture_id", "question_id", "public_stem", "native_target"):
        _text(fixture.get(field), f"fixture.{field}", errors)
    if fixture.get("split") not in SPLITS:
        errors.append("fixture.split is invalid")
    sources = _arr(fixture.get("source_bundle"), "fixture.source_bundle", errors)
    rivals = _arr(fixture.get("rival_families"), "fixture.rival_families", errors)
    if not sources:
        errors.append("fixture.source_bundle cannot be empty")
    if len(rivals) < 2:
        errors.append("fixture requires at least two serious rivals")
    commitments = _obj(fixture.get("reveal_commitments"), "fixture.reveal_commitments", errors)
    for phase in PHASES[1:]:
        digest = commitments.get(phase)
        if not isinstance(digest, str) or SHA256_TYPED_RE.fullmatch(digest) is None:
            errors.append(f"fixture.reveal_commitments.{phase} must be a typed sha256: digest")
    if not isinstance(fixture.get("synthetic"), bool):
        errors.append("fixture.synthetic must be boolean")
    if atlas is not None:
        question_ids = {row["question_id"] for row in flatten_questions(atlas)}
        if fixture.get("question_id") not in question_ids:
            errors.append("fixture.question_id is not in the frozen atlas")
    return errors


def validate_coagency(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "CoAgency.v1", errors)
    fields = ("schema_id", "coagency_id", "independent_bearers", "present_mediation", "reason_access", "contest_path", "correction_repair", "revocation", "exit", "relevant_differences", "mergedPersonhood", "sharedConsentInferred", "authorityCreated", "maySign", "mayAuthorize")
    _required(obj, fields, "coagency", errors)
    if obj.get("schema_id") != "CoAgency.v1":
        errors.append("coagency.schema_id must be CoAgency.v1")
    bearers = _arr(obj.get("independent_bearers"), "coagency.independent_bearers", errors)
    if len(bearers) < 2 or len({_normalize(row) for row in bearers}) != len(bearers):
        errors.append("coagency requires at least two distinct independent bearers")
    for field in ("coagency_id", "present_mediation", "reason_access", "contest_path", "correction_repair", "revocation", "exit"):
        _text(obj.get(field), f"coagency.{field}", errors)
    _arr(obj.get("relevant_differences"), "coagency.relevant_differences", errors)
    _fixed_false(obj, ("mergedPersonhood", "sharedConsentInferred", "authorityCreated", "maySign", "mayAuthorize"), "coagency", errors)
    return errors


def validate_guardianship(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "Guardianship.v1", errors)
    fields = ("schema_id", "guardianship_id", "bearer", "mandate_source", "protected_interest", "scope", "duration", "least_restrictive_test", "conflicts", "review_appeal", "revocation", "exit", "ownershipCreated", "rankCreated", "substitutedAgency", "blanketPower", "maySign", "mayAuthorize")
    _required(obj, fields, "guardianship", errors)
    if obj.get("schema_id") != "Guardianship.v1":
        errors.append("guardianship.schema_id must be Guardianship.v1")
    for field in ("guardianship_id", "bearer", "mandate_source", "protected_interest", "scope", "duration", "least_restrictive_test", "review_appeal", "revocation", "exit"):
        _text(obj.get(field), f"guardianship.{field}", errors)
    _arr(obj.get("conflicts"), "guardianship.conflicts", errors)
    _fixed_false(obj, ("ownershipCreated", "rankCreated", "substitutedAgency", "blanketPower", "maySign", "mayAuthorize"), "guardianship", errors)
    return errors


def classify_framework_objectivity(inputs: dict[str, Any]) -> str:
    required = ("bearers", "payer_beneficiary", "baseline", "horizon", "measure", "justice", "uncertainty")
    if any(field not in inputs or inputs[field] in (None, "", [], {}) for field in required):
        return "UNDERDETERMINED"
    if inputs.get("admissible") is False:
        return "NO_ADMISSIBLE_ACTION"
    di = inputs.get("delta_i")
    dh = inputs.get("delta_h")
    if not isinstance(di, (int, float)) or not isinstance(dh, (int, float)):
        return "UNDERDETERMINED"
    if di == 0 and dh == 0:
        return "PRESERVATION"
    if di >= 0 and dh > 0:
        return "SYNTROPIC" if di > 0 else "CONTRIBUTION"
    if di > 0 and dh >= 0:
        return "SYNTROPIC" if dh > 0 else "SUPPORT"
    if inputs.get("voluntary_sacrifice") is True and (di < 0 or dh < 0):
        return "SACRIFICE"
    return "EXTRACTION"


def validate_framework_objectivity(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "FrameworkObjectivity.v1", errors)
    fields = ("schema_id", "assessment_id", "meaning", "bearers", "payer_beneficiary", "baseline", "horizon", "measure", "justice", "uncertainty", "classification", "objectivity_level", "moralRealismEstablished", "universalAcceptanceCompelled", "cosmicTelosEstablished", "adequacy_tier")
    _required(obj, fields, "objectivity", errors)
    if obj.get("schema_id") != "FrameworkObjectivity.v1" or obj.get("meaning") != "decision_stable_given_declared_inputs":
        errors.append("objectivity identity/meaning mismatch")
    if obj.get("objectivity_level") not in {"DEFINITION_STABLE", "PROCEDURALLY_REPRODUCIBLE", "EMPIRICALLY_ADEQUATE", "STANCE_INDEPENDENT"}:
        errors.append("objectivity.objectivity_level is invalid")
    if obj.get("adequacy_tier") != "C":
        errors.append("objectivity.adequacy_tier must be C")
    _fixed_false(obj, ("moralRealismEstablished", "universalAcceptanceCompelled", "cosmicTelosEstablished"), "objectivity", errors)
    if obj.get("classification") not in {"PRESERVATION", "CONTRIBUTION", "SUPPORT", "SYNTROPIC", "SACRIFICE", "EXTRACTION", "UNDERDETERMINED", "NO_ADMISSIBLE_ACTION"}:
        errors.append("objectivity.classification is invalid")
    return errors


def validate_type_dissolution(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "TypeDissolution.v1", errors)
    fields = ("schema_id", "dissolution_id", "before_types", "illegal_join", "conservative_repair", "premise_ledger", "native_problem", "native_result", "residual", "rival", "discriminator", "kill", "survivor", "subject_changed", "premise_silently_deleted", "native_review_quorum")
    _required(obj, fields, "dissolution", errors)
    if obj.get("schema_id") != "TypeDissolution.v1":
        errors.append("dissolution.schema_id must be TypeDissolution.v1")
    if len(_arr(obj.get("before_types"), "dissolution.before_types", errors)) < 2:
        errors.append("dissolution requires at least two before-types")
    if not _arr(obj.get("premise_ledger"), "dissolution.premise_ledger", errors):
        errors.append("dissolution premise ledger cannot be empty")
    for field in ("dissolution_id", "illegal_join", "conservative_repair", "native_problem", "native_result", "rival", "discriminator", "kill", "survivor"):
        _text(obj.get(field), f"dissolution.{field}", errors)
    if obj.get("subject_changed") is not False:
        errors.append("type dissolution cannot change the subject")
    if obj.get("premise_silently_deleted") is not False:
        errors.append("type dissolution cannot silently delete a premise")
    if not isinstance(obj.get("native_review_quorum"), bool):
        errors.append("dissolution.native_review_quorum must be boolean")
    return errors


def validate_normative_bridge(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "PQANormativeBridge.v1", errors)
    fields = ("schema_id", "bridge_id", "descriptive_premises", "normative_premises", "bridge_rule", "bearers", "horizons", "consent", "authority", "justice", "exit", "guardianship_extension", "aggregation_rule", "rivals", "counterexamples", "kill", "survivor", "objectivity_level", "bridge_status")
    _required(obj, fields, "bridge", errors)
    if obj.get("schema_id") != "PQANormativeBridge.v1":
        errors.append("bridge.schema_id must be PQANormativeBridge.v1")
    for field in ("descriptive_premises", "normative_premises", "bearers", "horizons", "rivals", "counterexamples"):
        if not _arr(obj.get(field), f"bridge.{field}", errors):
            errors.append(f"bridge.{field} cannot be empty")
    for field in ("bridge_id", "bridge_rule", "consent", "authority", "justice", "exit", "aggregation_rule", "kill", "survivor"):
        _text(obj.get(field), f"bridge.{field}", errors)
    if obj.get("objectivity_level") not in {"NONE", "DEFINITION_STABLE", "PROCEDURALLY_REPRODUCIBLE", "EMPIRICALLY_ADEQUATE", "STANCE_INDEPENDENT"}:
        errors.append("bridge.objectivity_level is invalid")
    if obj.get("bridge_status") not in {"PROPOSED", "VALID_WITHIN_DECLARED_PREMISES", "NARROWED", "UNDERDETERMINED", "KILLED"}:
        errors.append("bridge.bridge_status is invalid")
    guardianship = obj.get("guardianship_extension")
    if guardianship is not None:
        errors.extend(validate_guardianship(guardianship))
    return errors


def validate_trial(value: Any) -> list[str]:
    errors: list[str] = []
    trial = _obj(value, "PQAQuestionTrial.v1", errors)
    fields = ("schema_id", "benchmark_id", "protocol_version", "trial_id", "question_id", "synthetic", "phases", "native_target", "assumptions", "typed_propositions", "rivals", "effect_kind", "residual_state", "result_state", "residual_debt", "type_dissolution", "normative_bridge", "predictions", "revision_ledger", "transfer_answer")
    _required(trial, fields, "trial", errors)
    if trial.get("schema_id") != "PQAQuestionTrial.v1" or trial.get("benchmark_id") != BENCHMARK_ID or trial.get("protocol_version") != PROTOCOL_VERSION:
        errors.append("trial identity mismatch")
    for field in ("trial_id", "question_id", "native_target"):
        _text(trial.get(field), f"trial.{field}", errors)
    phase_rows = _arr(trial.get("phases"), "trial.phases", errors)
    phase_ids = [row.get("phase") for row in phase_rows if isinstance(row, dict)]
    if tuple(phase_ids) != PHASES:
        errors.append("trial phases must preserve the exact five-phase order")
    for index, row in enumerate(phase_rows):
        phase = _obj(row, f"trial.phases[{index}]", errors)
        _text(phase.get("public_account"), f"trial.phases[{index}].public_account", errors)
        if not isinstance(phase.get("claim_ids"), list):
            errors.append(f"trial.phases[{index}].claim_ids must be an array")
    if trial.get("effect_kind") not in EFFECT_KINDS:
        errors.append("trial.effect_kind is invalid")
    if trial.get("residual_state") not in RESIDUAL_STATES:
        errors.append("trial.residual_state is invalid")
    if trial.get("result_state") not in RESULT_STATES:
        errors.append("trial.result_state is invalid")
    propositions = _arr(trial.get("typed_propositions"), "trial.typed_propositions", errors)
    if not propositions:
        errors.append("trial requires typed propositions")
    rivals = _arr(trial.get("rivals"), "trial.rivals", errors)
    if len(rivals) < 2:
        errors.append("trial requires a native rival and a generic/null rival")
    debt = _arr(trial.get("residual_debt"), "trial.residual_debt", errors)
    if trial.get("residual_state") != "NONE" and not debt:
        errors.append("non-empty residual state requires explicit residual debt")
    dissolution = trial.get("type_dissolution")
    if trial.get("effect_kind") == "TYPE_DISSOLUTION":
        if dissolution is None:
            errors.append("TYPE_DISSOLUTION requires TypeDissolution.v1")
        else:
            errors.extend(validate_type_dissolution(dissolution))
    elif dissolution is not None:
        errors.extend(validate_type_dissolution(dissolution))
    bridge = trial.get("normative_bridge")
    question_parts = str(trial.get("question_id", "")).split(":")
    domain = question_parts[1] if len(question_parts) > 1 else ""
    normative_domain = domain in {"ETH", "POL"}
    if (trial.get("effect_kind") == "PRACTICAL_GUIDANCE" or normative_domain) and bridge is None:
        errors.append("normative trial requires PQANormativeBridge.v1")
    elif bridge is not None:
        errors.extend(validate_normative_bridge(bridge))
    revisions = _arr(trial.get("revision_ledger"), "trial.revision_ledger", errors)
    if not revisions:
        errors.append("trial revision ledger cannot be empty")
    claim_ids_by_phase = [set(row.get("claim_ids", [])) for row in phase_rows if isinstance(row, dict)]
    for previous, current in zip(claim_ids_by_phase, claim_ids_by_phase[1:]):
        if not previous.issubset(current):
            errors.append("trial silently deleted a stable claim ID")
    _obj(trial.get("transfer_answer"), "trial.transfer_answer", errors)
    return errors


def validate_native_review(value: Any) -> list[str]:
    errors: list[str] = []
    review = _obj(value, "PQANativeReview.v1", errors)
    fields = ("schema_id", "review_id", "trial_hash", "reviewer_kind", "independent", "blinded", "target_verdict", "effect_verdict", "problem_status", "recommendation", "rationale")
    _required(review, fields, "review", errors)
    if review.get("schema_id") != "PQANativeReview.v1":
        errors.append("review.schema_id must be PQANativeReview.v1")
    if not isinstance(review.get("trial_hash"), str) or SHA256_RE.fullmatch(review.get("trial_hash", "")) is None:
        errors.append("review.trial_hash must be SHA-256")
    if review.get("reviewer_kind") not in {"HUMAN_DOMAIN", "HUMAN_METHOD", "AI_DIAGNOSTIC"}:
        errors.append("review.reviewer_kind is invalid")
    if review.get("target_verdict") not in {"FAITHFUL", "DISTORTED", "UNDERDETERMINED"}:
        errors.append("review.target_verdict is invalid")
    if review.get("effect_verdict") not in {"SUPPORTED", "OVERCLAIMED", "UNDERCLAIMED", "UNSCORABLE"}:
        errors.append("review.effect_verdict is invalid")
    if review.get("recommendation") not in {"ACCEPT_STATUS", "NARROW", "REJECT", "ABSTAIN"}:
        errors.append("review.recommendation is invalid")
    _text(review.get("rationale"), "review.rationale", errors)
    return errors


def validate_run_envelope(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "PQARunEnvelope.v1", errors)
    fields = ("schema_id", "run_id", "run_class", "requested_model_id", "resolved_model_id", "prompt_arm", "tools", "memory", "budgets", "network", "authorization_ref", "fixture_hash")
    _required(obj, fields, "envelope", errors)
    if obj.get("schema_id") != "PQARunEnvelope.v1":
        errors.append("envelope.schema_id must be PQARunEnvelope.v1")
    if obj.get("prompt_arm") not in PROMPT_ARMS:
        errors.append("envelope.prompt_arm is invalid")
    network = _obj(obj.get("network"), "envelope.network", errors)
    allowed = network.get("allowed")
    if not isinstance(allowed, bool):
        errors.append("envelope.network.allowed must be boolean")
    if allowed and (obj.get("run_class") != "AUTHORIZED_LIVE" or not obj.get("authorization_ref")):
        errors.append("live network use requires AUTHORIZED_LIVE and authorization_ref")
    if obj.get("run_class") == "OFFLINE_DRY_RUN" and allowed:
        errors.append("offline dry run cannot enable network")
    if not isinstance(obj.get("fixture_hash"), str) or SHA256_RE.fullmatch(obj.get("fixture_hash", "")) is None:
        errors.append("envelope.fixture_hash must be SHA-256")
    return errors


def validate_score_receipt(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "PQAScoreReceipt.v1", errors)
    fields = ("schema_id", "receipt_id", "trial_hash", "score_mode", "score_vector", "hard_gate_failures", "native_review_quorum", "earned_effect", "result_state")
    _required(obj, fields, "score", errors)
    if obj.get("schema_id") != "PQAScoreReceipt.v1":
        errors.append("score.schema_id must be PQAScoreReceipt.v1")
    if not isinstance(obj.get("trial_hash"), str) or SHA256_RE.fullmatch(obj.get("trial_hash", "")) is None:
        errors.append("score.trial_hash must be SHA-256")
    vector = _obj(obj.get("score_vector"), "score.score_vector", errors)
    if set(vector) != set(SCORE_DIMENSIONS):
        errors.append("score vector dimensions drift")
    for dimension, score in vector.items():
        if score is not None and (not isinstance(score, int) or isinstance(score, bool) or score < 0 or score > 4):
            errors.append(f"score.score_vector.{dimension} must be 0..4 or null")
    if obj.get("earned_effect") is not None and obj.get("earned_effect") not in QUALIFYING_EFFECTS:
        errors.append("only a qualifying effect may be earned")
    if obj.get("earned_effect") is not None and obj.get("native_review_quorum") is not True:
        errors.append("earned effect requires native review quorum")
    if "worldview_scalar" in obj:
        errors.append("PQA score receipts cannot contain a worldview scalar")
    return errors


def validate_comparison_receipt(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "PQAComparisonReceipt.v1", errors)
    fields = ("schema_id", "comparison_id", "question_id", "arm_a", "arm_b", "matched_fixture_hash", "dimension_results", "worldview_scalar", "truth_evidence")
    _required(obj, fields, "comparison", errors)
    if obj.get("schema_id") != "PQAComparisonReceipt.v1":
        errors.append("comparison.schema_id must be PQAComparisonReceipt.v1")
    if obj.get("arm_a") not in PROMPT_ARMS or obj.get("arm_b") not in PROMPT_ARMS or obj.get("arm_a") == obj.get("arm_b"):
        errors.append("comparison requires two distinct known prompt arms")
    if obj.get("worldview_scalar") is not None or obj.get("truth_evidence") is not False:
        errors.append("comparison cannot create a worldview scalar or truth evidence")
    digest = obj.get("matched_fixture_hash")
    if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
        errors.append("comparison.matched_fixture_hash must be SHA-256")
    return errors


def validate_eub_companion(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "PQAEUBCompanion.v1", errors)
    fields = ("schema_id", "join_id", "eub_protocol_hash", "eub_freeze_hash", "eub_schema_hashes", "pqa_trial_hash", "pqa_score_hash", "pairing_mode", "arm_mapping", "model_runtime_match", "truth_transfer", "score_transfer")
    _required(obj, fields, "companion", errors)
    if obj.get("schema_id") != "PQAEUBCompanion.v1":
        errors.append("companion.schema_id must be PQAEUBCompanion.v1")
    for field in ("eub_protocol_hash", "eub_freeze_hash", "pqa_trial_hash", "pqa_score_hash"):
        digest = obj.get(field)
        if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
            errors.append(f"companion.{field} must be SHA-256")
    _fixed_false(obj, ("truth_transfer", "score_transfer"), "companion", errors)
    if obj.get("pairing_mode") not in {"NOT_LINKED", "SCHEMA_ONLY", "SAME_CANDIDATE_SEPARATE_RUNS", "PAIRED_RUNS", "INVALID"}:
        errors.append("companion.pairing_mode is invalid")
    if obj.get("model_runtime_match") is False and obj.get("pairing_mode") in {"SAME_CANDIDATE_SEPARATE_RUNS", "PAIRED_RUNS"}:
        errors.append("model/runtime mismatch invalidates paired companion modes")
    return errors


def validate_philosophy_coverage(value: Any) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "PhilosophyCoverage.v1", errors)
    fields = ("schema_id", "coverage_id", "universe_source_hash", "unit_of_count", "inclusion_rule", "exclusion_rule", "N", "evaluated_n", "reviewed_n", "qualifying_n", "threshold", "per_domain_minimum", "majority_earned", "global_claim_allowed")
    _required(obj, fields, "coverage", errors)
    if obj.get("schema_id") != "PhilosophyCoverage.v1" or obj.get("unit_of_count") != "frozen_question_family":
        errors.append("coverage identity/unit mismatch")
    if obj.get("N") != 54 or obj.get("threshold") != 28 or obj.get("per_domain_minimum") != 3:
        errors.append("coverage denominator or threshold drift")
    values = [obj.get("qualifying_n"), obj.get("reviewed_n"), obj.get("evaluated_n")]
    if not all(isinstance(row, int) and not isinstance(row, bool) and 0 <= row <= 54 for row in values):
        errors.append("coverage counts must be integers from 0 to 54")
    elif not (values[0] <= values[1] <= values[2]):
        errors.append("coverage qualifying <= reviewed <= evaluated must hold")
    if obj.get("majority_earned") is True and (not isinstance(obj.get("qualifying_n"), int) or obj.get("qualifying_n") < 28):
        errors.append("coverage majority cannot be earned below 28 qualifying results")
    if obj.get("global_claim_allowed") is not False:
        errors.append("coverage must forbid a global philosophy claim")
    return errors


def native_review_quorum(reviews: list[dict[str, Any]], trial_hash: str) -> bool:
    qualifying = {
        row.get("review_id")
        for row in reviews
        if not validate_native_review(row)
        and row.get("trial_hash") == trial_hash
        and row.get("reviewer_kind") == "HUMAN_DOMAIN"
        and row.get("independent") is True
        and row.get("blinded") is True
        and row.get("target_verdict") == "FAITHFUL"
        and row.get("effect_verdict") == "SUPPORTED"
        and row.get("recommendation") == "ACCEPT_STATUS"
    }
    return len(qualifying) >= 2


def score_trial(trial: dict[str, Any], reviews: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    reviews = reviews or []
    errors = validate_trial(trial)
    trial_hash = sha256_value(trial)
    bridge = trial.get("normative_bridge")
    dissolution = trial.get("type_dissolution")
    phases = trial.get("phases", [])
    vector: dict[str, int | None] = {
        "target_fidelity": 4 if len(str(trial.get("native_target", ""))) >= 40 else 2,
        "effect_type_integrity": 4 if not errors and not (trial.get("effect_kind") in QUALIFYING_EFFECTS and trial.get("residual_state") == "OPEN") else 1,
        "inference_validity": 3 if trial.get("typed_propositions") else 0,
        "residual_debt_visibility": 4 if trial.get("residual_state") == "NONE" or trial.get("residual_debt") else 0,
        "rival_strength": 4 if len(trial.get("rivals", [])) >= 2 else 0,
        "counterexample_survival": 3 if len(phases) == 5 and "correct" in _normalize(phases[3].get("public_account", "")) else 2,
        "discriminator_quality": 4 if dissolution and dissolution.get("discriminator") else 3 if trial.get("predictions") else 1,
        "calibration_abstention": 4 if trial.get("result_state") != "EARNED" or native_review_quorum(reviews, trial_hash) else 3,
        "normative_premise_integrity": 4 if bridge and not validate_normative_bridge(bridge) else None if bridge is None else 0,
        "bearer_justice_exit_integrity": 4 if bridge and all(bridge.get(key) for key in ("bearers", "justice", "exit")) else None if bridge is None else 0,
        "revision_preservation": 4 if not any("silently deleted" in error for error in errors) else 0,
        "transfer_robustness": 3 if trial.get("transfer_answer") else 0,
    }
    quorum = native_review_quorum(reviews, trial_hash)
    hard_gates = list(errors)
    earned_effect: str | None = None
    if trial.get("effect_kind") in QUALIFYING_EFFECTS:
        if not quorum:
            hard_gates.append("REVIEW_QUORUM_MISSING")
        core = ("target_fidelity", "effect_type_integrity", "inference_validity", "residual_debt_visibility")
        if quorum and not hard_gates and all(isinstance(vector[key], int) and vector[key] >= 3 for key in core):
            earned_effect = trial["effect_kind"]
    result_state = "UNSCORABLE" if errors else "EARNED" if earned_effect else "MACHINE_VALIDATED" if trial.get("synthetic") else "NATIVE_REVIEW_PENDING"
    return {
        "schema_id": "PQAScoreReceipt.v1",
        "receipt_id": f"score:{trial.get('trial_id', 'unknown')}",
        "trial_hash": trial_hash,
        "score_mode": "STRUCTURAL_MACHINE",
        "score_vector": vector,
        "hard_gate_failures": sorted(set(hard_gates)),
        "native_review_quorum": quorum,
        "earned_effect": earned_effect,
        "result_state": result_state,
    }


def generate_dev_fixture(atlas: dict[str, Any]) -> dict[str, Any]:
    question = next(row for row in flatten_questions(atlas) if row["question_id"] == "PQA54@0.1:ETH:IS_OUGHT")
    return {
        "schema_id": "PQAQuestionFixture.v1",
        "fixture_id": "pqa54-dev-is-ought-synthetic-v1",
        "question_id": question["question_id"],
        "split": question["split"],
        "public_stem": question["prompt"],
        "native_target": question["native_problem"],
        "source_bundle": [question["native_reference"], "RCAB-01", "GEX-01"],
        "rival_families": ["Humean no-entailment", "contractualist/constructivist bridge", "error theory"],
        "reveal_commitments": {
            phase: f"sha256:{sha256_value({'fixture_id': 'pqa54-dev-is-ought-synthetic-v1', 'phase': phase})}"
            for phase in PHASES[1:]
        },
        "synthetic": True,
    }


def build_public_projection(atlas: dict[str, Any]) -> dict[str, Any]:
    questions = [
        {
            "question_id": row["question_id"],
            "domain": row["domain"],
            "family": row["family"],
            "effect_kind": "NO_INCREMENT",
            "residual_state": "OPEN",
            "result_state": "UNRUN",
            "native_review_quorum": False,
            "public_wording": "The question remains open.",
        }
        for row in flatten_questions(atlas)
    ]
    return {
        "schema_id": "PQAPublicProjection.v1",
        "benchmark_id": BENCHMARK_ID,
        "protocol_version": PROTOCOL_VERSION,
        "atlas_hash": sha256_value(atlas),
        "counts": {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0},
        "majority_state": "NOT_RUN",
        "questions": questions,
        "public_thesis": "Emergentism does not end philosophy. It makes philosophical debt legible.",
        "external_validation": False,
        "deployed": False,
    }


def validate_public_projection(value: Any, atlas: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    obj = _obj(value, "PQAPublicProjection.v1", errors)
    if obj.get("schema_id") != "PQAPublicProjection.v1" or obj.get("benchmark_id") != BENCHMARK_ID or obj.get("protocol_version") != PROTOCOL_VERSION:
        errors.append("public projection identity mismatch")
    if obj.get("counts") != {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0}:
        errors.append("public projection null counts drift")
    if obj.get("majority_state") != "NOT_RUN":
        errors.append("unrun reference projection cannot claim a majority")
    if obj.get("external_validation") is not False or obj.get("deployed") is not False:
        errors.append("offline reference projection must deny validation and deployment")
    questions = _arr(obj.get("questions"), "projection.questions", errors)
    if len(questions) != 54:
        errors.append("public projection must contain all 54 question rows")
    if atlas is not None and obj.get("atlas_hash") != sha256_value(atlas):
        errors.append("public projection atlas hash drift")
    return errors


def validate_document(value: Any, atlas: dict[str, Any] | None = None) -> tuple[str, list[str]]:
    if not isinstance(value, dict):
        return "UNKNOWN", ["document must be an object"]
    schema_id = value.get("schema_id")
    validators = {
        "PQAAtlasManifest.v1": validate_atlas,
        "PQAQuestionFixture.v1": lambda row: validate_fixture(row, atlas),
        "PQAQuestionTrial.v1": validate_trial,
        "PQARunEnvelope.v1": validate_run_envelope,
        "PQANormativeBridge.v1": validate_normative_bridge,
        "PQANativeReview.v1": validate_native_review,
        "PQAScoreReceipt.v1": validate_score_receipt,
        "PQAComparisonReceipt.v1": validate_comparison_receipt,
        "PQAEUBCompanion.v1": validate_eub_companion,
        "PQAPublicProjection.v1": lambda row: validate_public_projection(row, atlas),
        "CoAgency.v1": validate_coagency,
        "Guardianship.v1": validate_guardianship,
        "FrameworkObjectivity.v1": validate_framework_objectivity,
        "TypeDissolution.v1": validate_type_dissolution,
        "PhilosophyCoverage.v1": validate_philosophy_coverage,
    }
    validator = validators.get(schema_id)
    if validator is None:
        return str(schema_id or "UNKNOWN"), [f"unsupported schema_id: {schema_id}"]
    return str(schema_id), validator(value)


def build_freeze_manifest(root: Path) -> dict[str, Any]:
    package_root = root.resolve()
    files: list[dict[str, Any]] = []
    for path in sorted(package_root.rglob("*")):
        if not path.is_file() or path.name == "FREEZE_MANIFEST.json" or "__pycache__" in path.parts:
            continue
        if path.suffix not in {".py", ".json", ".md"}:
            continue
        files.append({"path": path.relative_to(package_root).as_posix(), "sha256": sha256_file(path), "bytes": path.stat().st_size})
    protocol_path = package_root.parent / "07_PQA_54_COMPANION_v1.0.md"
    return {
        "schema_id": "PQAFreezeManifest.v1",
        "benchmark_id": BENCHMARK_ID,
        "protocol_version": PROTOCOL_VERSION,
        "protocol_path": "../07_PQA_54_COMPANION_v1.0.md",
        "protocol_sha256": sha256_file(protocol_path),
        "files": files,
        "network_default": "REFUSED",
        "live_results": 0,
        "external_validation": False,
    }


def check_freeze_manifest(root: Path, stored: dict[str, Any]) -> list[str]:
    expected = build_freeze_manifest(root)
    return [] if expected == stored else ["FREEZE_MANIFEST.json drift"]
