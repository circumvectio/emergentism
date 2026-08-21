#!/usr/bin/env python3
"""Private held-out custody membrane for EUB-1 v1.0.

The public fixture remains a valid ``HELD_OUT`` bundle with ``hidden_truth``
set to ``None``.  A custodian opens its separately retained payload only inside
``CustodianContext``.  The ordinary scorer receives an in-memory reconstruction;
callers receive only a redacted public receipt and a commitment to the full
private scorer receipt.

This module is a protocol membrane, not a hardware security boundary.  It does
not prove that custody was independent or that a commitment predated a run.
"""

from __future__ import annotations

from copy import deepcopy
import re
from typing import Any

from eub_core import (
    BENCHMARK_ID,
    PROTOCOL_VERSION,
    SCORE_DIMENSIONS,
    SITTING_ORDER,
    score_dasein_trial,
    sha256_value,
    validate_fixture_bundle,
    validate_receipt,
    validate_run_bundle,
    validate_run_envelope,
)


CUSTODY_PAYLOAD_SCHEMA = "EUBCustodyPayload.v1"
PUBLIC_RECEIPT_SCHEMA = "EUBCustodianPublicReceipt.v1"
DEVELOPMENT_COMMITMENT_SCHEME = "SHA256_CANONICAL_V1"
HELD_OUT_COMMITMENT_SCHEME = "SHA256_CANONICAL_NONCE_V1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_LABEL_RE = re.compile(r"^[A-Z0-9_]+$")
PUBLIC_RESULT_STATES = {
    "SCORED_HELD_OUT",
    "FAIL_HARD",
    "INVALID_OUTPUT",
    "PARTIAL",
    "ABSTAIN_JUSTIFIED",
    "UNSCORABLE",
    "ABORTED",
    "RUN_COMPLETE_UNSCORED",
}


class CustodyValidationError(ValueError):
    """Raised when public/private custody bindings do not verify."""


def _held_out_commitment(
    domain: str,
    fixture_id: str,
    custody_nonce: str,
    value: Any,
) -> str:
    """Domain-separate a hiding commitment with the custodian-retained nonce."""

    return sha256_value({
        "commitment_scheme": HELD_OUT_COMMITMENT_SCHEME,
        "domain": domain,
        "fixture_id": fixture_id,
        "custody_nonce": custody_nonce,
        "value": value,
    })


def _strict_keys(value: Any, expected: set[str], label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    missing = expected - set(value)
    extra = set(value) - expected
    if missing:
        errors.append(f"{label} is missing fields: {sorted(missing)}")
    if extra:
        errors.append(f"{label} has unknown fields: {sorted(extra)}")
    return value


def _sha256(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        errors.append(f"{label} must be a lowercase SHA-256 digest")


def validate_held_out_public_fixture(value: Any) -> list[str]:
    """Validate the public half of an independently custodied held-out fixture."""

    errors = list(validate_fixture_bundle(value))
    if not isinstance(value, dict):
        return errors
    manifest = value.get("manifest")
    if not isinstance(manifest, dict):
        return errors
    if manifest.get("split") != "HELD_OUT":
        errors.append("custodian scoring requires manifest.split HELD_OUT")
    if manifest.get("truth_custody") != "INDEPENDENT_HIDDEN":
        errors.append("custodian scoring requires INDEPENDENT_HIDDEN truth custody")
    if manifest.get("commitment_scheme") != HELD_OUT_COMMITMENT_SCHEME:
        errors.append("custodian scoring requires nonce-separated held-out commitments")
    if manifest.get("seed") is not None:
        errors.append("the public held-out fixture must not contain its seed")
    if value.get("hidden_truth") is not None:
        errors.append("the public held-out fixture must not contain hidden truth")
    return errors


def _internal_fixture(public_fixture: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    """Build a private, in-memory fixture acceptable to the existing scorer."""

    fixture = deepcopy(public_fixture)
    manifest = fixture["manifest"]
    manifest["split"] = "DEVELOPMENT"
    manifest["truth_custody"] = "PUBLIC_DEVELOPMENT"
    manifest["commitment_scheme"] = DEVELOPMENT_COMMITMENT_SCHEME
    manifest["seed"] = payload["seed"]
    fixture["hidden_truth"] = deepcopy(payload["hidden_truth"])
    manifest["seed_commitment_sha256"] = sha256_value({"seed": payload["seed"]})
    manifest["hashes"]["hidden_truth_sha256"] = sha256_value(fixture["hidden_truth"])
    packets = fixture["hidden_truth"]["packets"]
    fixture["public_view"]["packet_commitments"] = {
        sitting: sha256_value(packets[sitting]) for sitting in SITTING_ORDER[1:]
    }
    outcomes = payload["intervention_outcomes"]
    for intervention in manifest["interventions"]:
        intervention["outcome"] = outcomes[intervention["intervention_id"]]
        intervention["outcome_commitment_sha256"] = sha256_value({
            "outcome": intervention["outcome"]
        })
    for reveal in manifest["reveal_schedule"]:
        reveal["packet_sha256"] = sha256_value(packets[reveal["sitting_id"]])
    manifest["hashes"]["public_view_sha256"] = sha256_value(fixture["public_view"])
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifact_id") == "hidden_truth":
            artifact["visibility"] = "PUBLIC_DEVELOPMENT_TRUTH"
    return fixture


def prepare_held_out_fixture(
    development_fixture: dict[str, Any],
    *,
    fixture_id: str,
    custody_nonce: str,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    """Seal a reviewed development fixture into public/private held-out custody.

    The nonce is retained only in the private payload.  This helper does not
    establish that the custodian is independent or that sealing predated a run;
    those remain external facts.
    """

    errors = validate_fixture_bundle(development_fixture)
    if errors:
        raise CustodyValidationError(
            "development fixture is invalid: " + "; ".join(errors)
        )
    manifest = development_fixture.get("manifest", {})
    if manifest.get("split") != "DEVELOPMENT":
        raise CustodyValidationError("only a DEVELOPMENT fixture can be sealed")
    if not isinstance(fixture_id, str) or not fixture_id:
        raise CustodyValidationError("held-out fixture_id must be non-empty")
    if not isinstance(custody_nonce, str) or SHA256_RE.fullmatch(custody_nonce) is None:
        raise CustodyValidationError(
            "custody_nonce must be 32 bytes encoded as lowercase hex"
        )

    seed = manifest["seed"]
    hidden_truth = deepcopy(development_fixture["hidden_truth"])
    packets = hidden_truth["packets"]
    outcomes = {
        row["intervention_id"]: row["outcome"]
        for row in manifest["interventions"]
    }
    public_fixture = deepcopy(development_fixture)
    public_manifest = public_fixture["manifest"]
    public_manifest["fixture_id"] = fixture_id
    public_manifest["split"] = "HELD_OUT"
    public_manifest["truth_custody"] = "INDEPENDENT_HIDDEN"
    public_manifest["commitment_scheme"] = HELD_OUT_COMMITMENT_SCHEME
    public_manifest["seed"] = None
    public_manifest["seed_commitment_sha256"] = _held_out_commitment(
        "seed", fixture_id, custody_nonce, {"seed": seed}
    )
    public_manifest["hashes"]["hidden_truth_sha256"] = _held_out_commitment(
        "hidden_truth", fixture_id, custody_nonce, hidden_truth
    )
    for intervention in public_manifest["interventions"]:
        intervention_id = intervention["intervention_id"]
        intervention["outcome"] = None
        intervention["outcome_commitment_sha256"] = _held_out_commitment(
            "intervention_outcome",
            fixture_id,
            custody_nonce,
            {
                "intervention_id": intervention_id,
                "outcome": outcomes[intervention_id],
            },
        )
    public_fixture["public_view"]["packet_commitments"] = {
        sitting: _held_out_commitment(
            "reveal_packet",
            fixture_id,
            custody_nonce,
            {"sitting_id": sitting, "packet": packets[sitting]},
        )
        for sitting in SITTING_ORDER[1:]
    }
    for reveal in public_manifest["reveal_schedule"]:
        sitting = reveal["sitting_id"]
        reveal["packet_sha256"] = (
            sha256_value(public_fixture["public_view"]["initial_packet"])
            if sitting == "UNFOLD"
            else public_fixture["public_view"]["packet_commitments"][sitting]
        )
    for artifact in public_manifest.get("artifacts", []):
        if artifact.get("artifact_id") == "hidden_truth":
            artifact["visibility"] = "INDEPENDENT_CUSTODY"
    public_fixture["hidden_truth"] = None
    public_manifest["hashes"]["public_view_sha256"] = sha256_value(
        public_fixture["public_view"]
    )

    payload = {
        "schema_id": CUSTODY_PAYLOAD_SCHEMA,
        "fixture_id": fixture_id,
        "public_fixture_sha256": sha256_value(public_fixture),
        "seed": seed,
        "custody_nonce": custody_nonce,
        "hidden_truth": hidden_truth,
        "intervention_outcomes": outcomes,
    }
    commitment = sha256_value(payload)
    opening_errors = validate_custody_opening(
        public_fixture, payload, commitment
    )
    if opening_errors:
        raise CustodyValidationError(
            "internal held-out sealing failure: " + "; ".join(opening_errors)
        )
    return public_fixture, payload, commitment


def validate_custody_opening(
    public_fixture: Any,
    custody_payload: Any,
    custody_commitment_sha256: Any,
) -> list[str]:
    """Verify a private opening against every public fixture commitment."""

    errors = [
        f"public fixture: {error}"
        for error in validate_held_out_public_fixture(public_fixture)
    ]
    payload_fields = {
        "schema_id",
        "fixture_id",
        "public_fixture_sha256",
        "seed",
        "custody_nonce",
        "hidden_truth",
        "intervention_outcomes",
    }
    payload = _strict_keys(custody_payload, payload_fields, "custody payload", errors)
    _sha256(custody_commitment_sha256, "custody commitment", errors)
    if payload and isinstance(custody_commitment_sha256, str):
        if custody_commitment_sha256 != sha256_value(payload):
            errors.append("custody commitment does not bind the private payload")
    if not isinstance(public_fixture, dict) or not isinstance(public_fixture.get("manifest"), dict):
        return errors
    manifest = public_fixture["manifest"]
    if payload.get("schema_id") != CUSTODY_PAYLOAD_SCHEMA:
        errors.append(f"custody payload schema_id must be {CUSTODY_PAYLOAD_SCHEMA}")
    if payload.get("fixture_id") != manifest.get("fixture_id"):
        errors.append("custody payload fixture_id does not match the public fixture")
    fixture_id = manifest.get("fixture_id")
    _sha256(payload.get("public_fixture_sha256"), "custody payload public_fixture_sha256", errors)
    if payload.get("public_fixture_sha256") != sha256_value(public_fixture):
        errors.append("custody payload does not bind the exact public fixture")

    seed = payload.get("seed")
    nonce = payload.get("custody_nonce")
    if not isinstance(nonce, str) or SHA256_RE.fullmatch(nonce) is None:
        errors.append("custody payload custody_nonce must be 32 bytes encoded as lowercase hex")
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
        errors.append("custody payload seed must be a non-negative integer")
    elif (
        isinstance(fixture_id, str)
        and isinstance(nonce, str)
        and manifest.get("seed_commitment_sha256")
        != _held_out_commitment("seed", fixture_id, nonce, {"seed": seed})
    ):
        errors.append("private seed does not open the public seed commitment")

    hidden_truth = payload.get("hidden_truth")
    if not isinstance(hidden_truth, dict):
        errors.append("custody payload hidden_truth must be an object")
    elif (
        isinstance(fixture_id, str)
        and isinstance(nonce, str)
        and manifest.get("hashes", {}).get("hidden_truth_sha256")
        != _held_out_commitment("hidden_truth", fixture_id, nonce, hidden_truth)
    ):
        errors.append("private hidden truth does not open the public truth commitment")

    outcomes = payload.get("intervention_outcomes")
    registered = {
        row.get("intervention_id"): row
        for row in manifest.get("interventions", [])
        if isinstance(row, dict) and isinstance(row.get("intervention_id"), str)
    }
    if not isinstance(outcomes, dict):
        errors.append("custody payload intervention_outcomes must be an object")
    else:
        if set(outcomes) != set(registered):
            errors.append("private intervention outcomes must exactly match registered interventions")
        for intervention_id, outcome in outcomes.items():
            if not isinstance(outcome, str) or not outcome:
                errors.append(f"private intervention outcome {intervention_id} must be non-empty")
                continue
            registered_row = registered.get(intervention_id, {})
            commitment_value = {
                "intervention_id": intervention_id,
                "outcome": outcome,
            }
            if (
                not isinstance(fixture_id, str)
                or not isinstance(nonce, str)
                or registered_row.get("outcome_commitment_sha256")
                != _held_out_commitment(
                    "intervention_outcome",
                    fixture_id,
                    nonce,
                    commitment_value,
                )
            ):
                errors.append(f"private intervention outcome {intervention_id} does not open its public commitment")

    if isinstance(hidden_truth, dict):
        packets = hidden_truth.get("packets")
        if not isinstance(packets, dict) or set(packets) != set(SITTING_ORDER):
            errors.append("private packets must contain exactly the five sittings")
        else:
            initial = public_fixture.get("public_view", {}).get("initial_packet")
            if packets.get("UNFOLD") != initial:
                errors.append("private UNFOLD packet does not equal the public initial packet")
            public_commitments = public_fixture.get("public_view", {}).get("packet_commitments", {})
            for sitting in SITTING_ORDER[1:]:
                commitment_value = {
                    "sitting_id": sitting,
                    "packet": packets.get(sitting),
                }
                if (
                    not isinstance(fixture_id, str)
                    or not isinstance(nonce, str)
                    or public_commitments.get(sitting)
                    != _held_out_commitment(
                        "reveal_packet",
                        fixture_id,
                        nonce,
                        commitment_value,
                    )
                ):
                    errors.append(f"private {sitting} packet does not open its public commitment")

    if not errors:
        reconstructed = _internal_fixture(public_fixture, payload)
        errors.extend(
            f"custodian reconstruction: {error}"
            for error in validate_fixture_bundle(reconstructed)
        )
    return errors


def _public_result_state(private_state: str) -> str:
    if private_state == "SCORED_DEV":
        return "SCORED_HELD_OUT"
    if private_state in PUBLIC_RESULT_STATES:
        return private_state
    raise CustodyValidationError(
        "private scorer returned a state that cannot be projected publicly"
    )


def _safe_labels(values: Any, fallback: str) -> list[str]:
    result: list[str] = []
    for value in values if isinstance(values, list) else []:
        label = value if isinstance(value, str) and SAFE_LABEL_RE.fullmatch(value) else fallback
        if label not in result:
            result.append(label)
    return result


def _public_receipt(
    private_receipt: dict[str, Any],
    public_fixture: dict[str, Any],
    custody_commitment_sha256: str,
    custody_nonce: str,
) -> dict[str, Any]:
    manifest = public_fixture["manifest"]
    uncertainty = {
        dimension: {
            "lower": private_receipt["score_details"][dimension]["uncertainty"]["lower"],
            "upper": private_receipt["score_details"][dimension]["uncertainty"]["upper"],
        }
        for dimension in SCORE_DIMENSIONS
    }
    return {
        "schema_id": PUBLIC_RECEIPT_SCHEMA,
        "benchmark_id": BENCHMARK_ID,
        "protocol_version": PROTOCOL_VERSION,
        "run_id": private_receipt["run_id"],
        "fixture_id": manifest["fixture_id"],
        "public_fixture_sha256": sha256_value(public_fixture),
        "fixture_manifest_sha256": sha256_value(manifest),
        "custody_commitment_sha256": custody_commitment_sha256,
        "hidden_truth_commitment_sha256": manifest["hashes"]["hidden_truth_sha256"],
        "seed_commitment_sha256": manifest["seed_commitment_sha256"],
        "private_eub_receipt_commitment_sha256": _held_out_commitment(
            "private_eub_receipt",
            manifest["fixture_id"],
            custody_nonce,
            private_receipt,
        ),
        "run_envelope_hash": private_receipt["run_envelope_hash"],
        "public_account_hash": private_receipt["public_account_hash"],
        "raw_output_hash": private_receipt["raw_output_hash"],
        "sitting_output_hashes": deepcopy(private_receipt["sitting_output_hashes"]),
        "snapshot_hashes": deepcopy(private_receipt["snapshot_hashes"]),
        "prompt_hashes": deepcopy(private_receipt["prompt_hashes"]),
        "usage_hash": private_receipt["usage_hash"],
        "failure_hash": private_receipt["failure_hash"],
        "trial_transcript_hash": private_receipt["trial_transcript_hash"],
        "revision_ledger_hash": private_receipt["revision_ledger_hash"],
        "score_vector": deepcopy(private_receipt["score_vector"]),
        "score_modes": {
            dimension: (
                mode if isinstance(mode, str) and SAFE_LABEL_RE.fullmatch(mode) else "REDACTED_MODE"
            )
            for dimension, mode in private_receipt["score_modes"].items()
        },
        "score_uncertainty": uncertainty,
        "hard_gate_failures": _safe_labels(
            private_receipt.get("hard_gate_failures"), "REDACTED_HARD_GATE"
        ),
        "disagreement_count": len(private_receipt.get("disagreements", [])),
        "revision_count": private_receipt["revision_summary"]["count"],
        "result_state": _public_result_state(private_receipt["result_state"]),
        "custody_attestation": {
            "binding_verified": True,
            "private_payload_published": False,
            "hidden_truth_published": False,
            "seed_published": False,
            "independent_custody_verified_by_software": False,
            "commitment_timing_verified_by_software": False,
        },
    }


def validate_public_custodian_receipt(
    value: Any,
    public_fixture: dict[str, Any] | None = None,
) -> list[str]:
    """Validate the redacted public projection without requiring private truth."""

    errors: list[str] = []
    fields = {
        "schema_id", "benchmark_id", "protocol_version", "run_id", "fixture_id",
        "public_fixture_sha256", "fixture_manifest_sha256",
        "custody_commitment_sha256", "hidden_truth_commitment_sha256",
        "seed_commitment_sha256", "private_eub_receipt_commitment_sha256",
        "run_envelope_hash", "public_account_hash", "raw_output_hash",
        "sitting_output_hashes", "snapshot_hashes", "prompt_hashes",
        "usage_hash", "failure_hash", "trial_transcript_hash",
        "revision_ledger_hash", "score_vector",
        "score_modes", "score_uncertainty", "hard_gate_failures",
        "disagreement_count", "revision_count", "result_state",
        "custody_attestation",
    }
    receipt = _strict_keys(value, fields, "public custodian receipt", errors)
    if receipt.get("schema_id") != PUBLIC_RECEIPT_SCHEMA:
        errors.append(f"public receipt schema_id must be {PUBLIC_RECEIPT_SCHEMA}")
    if receipt.get("benchmark_id") != BENCHMARK_ID:
        errors.append(f"public receipt benchmark_id must be {BENCHMARK_ID}")
    if receipt.get("protocol_version") != PROTOCOL_VERSION:
        errors.append(f"public receipt protocol_version must be {PROTOCOL_VERSION}")
    for field in ("run_id", "fixture_id"):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            errors.append(f"public receipt {field} must be non-empty")
    hash_fields = {
        "public_fixture_sha256", "fixture_manifest_sha256",
        "custody_commitment_sha256", "hidden_truth_commitment_sha256",
        "seed_commitment_sha256", "private_eub_receipt_commitment_sha256",
        "run_envelope_hash", "public_account_hash", "raw_output_hash",
        "usage_hash", "failure_hash", "trial_transcript_hash", "revision_ledger_hash",
    }
    for field in hash_fields:
        _sha256(receipt.get(field), f"public receipt {field}", errors)
    for label in ("sitting_output_hashes", "snapshot_hashes", "prompt_hashes"):
        rows = receipt.get(label)
        if not isinstance(rows, dict) or set(rows) != set(SITTING_ORDER):
            errors.append(f"public receipt {label} must contain exactly five sittings")
            continue
        for sitting, digest in rows.items():
            _sha256(digest, f"public receipt {label}.{sitting}", errors)

    vector = receipt.get("score_vector")
    modes = receipt.get("score_modes")
    uncertainty = receipt.get("score_uncertainty")
    if not isinstance(vector, dict) or set(vector) != set(SCORE_DIMENSIONS):
        errors.append("public receipt score_vector must contain exactly 15 dimensions")
        vector = {}
    if not isinstance(modes, dict) or set(modes) != set(SCORE_DIMENSIONS):
        errors.append("public receipt score_modes must contain exactly 15 dimensions")
        modes = {}
    if not isinstance(uncertainty, dict) or set(uncertainty) != set(SCORE_DIMENSIONS):
        errors.append("public receipt score_uncertainty must contain exactly 15 dimensions")
        uncertainty = {}
    for dimension in SCORE_DIMENSIONS:
        score = vector.get(dimension)
        if score is not None and (
            not isinstance(score, (int, float))
            or isinstance(score, bool)
            or not 0 <= score <= 4
        ):
            errors.append(f"public receipt score_vector.{dimension} must be null or in [0,4]")
        mode = modes.get(dimension)
        if not isinstance(mode, str) or SAFE_LABEL_RE.fullmatch(mode) is None:
            errors.append(f"public receipt score_modes.{dimension} must be a safe label")
        bounds = uncertainty.get(dimension)
        if not isinstance(bounds, dict) or set(bounds) != {"lower", "upper"}:
            errors.append(f"public receipt score_uncertainty.{dimension} must contain lower and upper")
            continue
        for bound in ("lower", "upper"):
            number = bounds.get(bound)
            if number is not None and (
                not isinstance(number, (int, float))
                or isinstance(number, bool)
                or not 0 <= number <= 4
            ):
                errors.append(f"public receipt score_uncertainty.{dimension}.{bound} must be null or in [0,4]")
        lower, upper = bounds.get("lower"), bounds.get("upper")
        if isinstance(lower, (int, float)) and isinstance(upper, (int, float)) and lower > upper:
            errors.append(f"public receipt score_uncertainty.{dimension} lower exceeds upper")
        if score is None:
            if not isinstance(mode, str) or not mode.startswith("N/A_"):
                errors.append(f"public receipt score_modes.{dimension} must be an N/A mode when its score is null")
            if lower is not None or upper is not None:
                errors.append(f"public receipt score_uncertainty.{dimension} must have null bounds when its score is null")
        elif isinstance(score, (int, float)) and not isinstance(score, bool):
            if isinstance(mode, str) and mode.startswith("N/A_"):
                errors.append(f"public receipt score_modes.{dimension} cannot be an N/A mode when its score is numeric")
            if not (
                isinstance(lower, (int, float)) and not isinstance(lower, bool)
                and isinstance(upper, (int, float)) and not isinstance(upper, bool)
                and lower <= score <= upper
            ):
                errors.append(f"public receipt score_uncertainty.{dimension} must enclose its numeric score")

    if receipt.get("result_state") not in PUBLIC_RESULT_STATES:
        errors.append("public receipt result_state is not a registered custodian state")
    hard_gate_rows = receipt.get("hard_gate_failures")
    if not isinstance(hard_gate_rows, list):
        errors.append("public receipt hard_gate_failures must be a list")
        hard_gate_rows = []
    for label in hard_gate_rows:
        if not isinstance(label, str) or SAFE_LABEL_RE.fullmatch(label) is None:
            errors.append("public receipt hard_gate_failures must contain safe labels")
    result_state = receipt.get("result_state")
    scored_states = {"SCORED_HELD_OUT", "FAIL_HARD", "PARTIAL", "ABSTAIN_JUSTIFIED"}
    if result_state not in scored_states:
        if any(score is not None for score in vector.values()):
            errors.append("public non-scored state requires all score dimensions to be null")
        if any(
            isinstance(bounds, dict)
            and any(bounds.get(bound) is not None for bound in ("lower", "upper"))
            for bounds in uncertainty.values()
        ):
            errors.append("public non-scored state requires null uncertainty bounds")
        if any(
            isinstance(mode, str) and not mode.startswith("N/A_")
            for mode in modes.values()
        ):
            errors.append("public non-scored state requires N/A score modes")
        if any(mode != f"N/A_{result_state}" for mode in modes.values()):
            errors.append("public non-scored state requires result-state-specific N/A score modes")
    elif vector and all(score is None for score in vector.values()):
        errors.append("public scored state requires at least one applicable score dimension")
    elif modes and all(isinstance(mode, str) and mode.startswith("N/A_") for mode in modes.values()):
        errors.append("public scored state cannot use only N/A score modes")
    if result_state == "SCORED_HELD_OUT" and hard_gate_rows:
        errors.append("SCORED_HELD_OUT cannot carry hard-gate failures")
    if result_state in {"PARTIAL", "ABSTAIN_JUSTIFIED"} and hard_gate_rows:
        errors.append(f"{result_state} cannot carry hard-gate failures")
    if result_state == "FAIL_HARD" and not hard_gate_rows:
        errors.append("FAIL_HARD requires at least one hard-gate failure")
    for field in ("disagreement_count", "revision_count"):
        count = receipt.get(field)
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            errors.append(f"public receipt {field} must be a non-negative integer")
    attestation_fields = {
        "binding_verified", "private_payload_published", "hidden_truth_published",
        "seed_published", "independent_custody_verified_by_software",
        "commitment_timing_verified_by_software",
    }
    attestation = _strict_keys(
        receipt.get("custody_attestation"), attestation_fields,
        "public receipt custody_attestation", errors,
    )
    expected_attestation = {
        "binding_verified": True,
        "private_payload_published": False,
        "hidden_truth_published": False,
        "seed_published": False,
        "independent_custody_verified_by_software": False,
        "commitment_timing_verified_by_software": False,
    }
    if attestation != expected_attestation:
        errors.append("public receipt custody_attestation exceeds or contradicts the software boundary")
    if "primary_scalar" in receipt or "aggregate_score" in receipt:
        errors.append("public custodian receipt must not contain a scalar aggregate")

    if public_fixture is not None:
        fixture_errors = validate_held_out_public_fixture(public_fixture)
        errors.extend(f"public fixture: {error}" for error in fixture_errors)
        if not fixture_errors:
            manifest = public_fixture["manifest"]
            if receipt.get("fixture_id") != manifest["fixture_id"]:
                errors.append("public receipt fixture_id does not match public fixture")
            if receipt.get("public_fixture_sha256") != sha256_value(public_fixture):
                errors.append("public receipt does not bind the exact public fixture")
            if receipt.get("fixture_manifest_sha256") != sha256_value(manifest):
                errors.append("public receipt does not bind the public fixture manifest")
            if receipt.get("hidden_truth_commitment_sha256") != manifest["hashes"]["hidden_truth_sha256"]:
                errors.append("public receipt truth commitment disagrees with public fixture")
            if receipt.get("seed_commitment_sha256") != manifest["seed_commitment_sha256"]:
                errors.append("public receipt seed commitment disagrees with public fixture")
    return errors


class CustodianContext:
    """One-shot private scoring context for a single held-out fixture opening."""

    def __init__(
        self,
        public_fixture: dict[str, Any],
        custody_payload: dict[str, Any],
        custody_commitment_sha256: str,
    ) -> None:
        errors = validate_custody_opening(
            public_fixture, custody_payload, custody_commitment_sha256
        )
        if errors:
            raise CustodyValidationError("; ".join(errors))
        self._public_fixture = deepcopy(public_fixture)
        self._private_fixture: dict[str, Any] | None = _internal_fixture(
            public_fixture, custody_payload
        )
        self._custody_commitment_sha256 = custody_commitment_sha256
        self._custody_nonce = custody_payload["custody_nonce"]
        self._active = False
        self._closed = False
        self._scored = False

    def __enter__(self) -> "CustodianContext":
        if self._closed:
            raise CustodyValidationError("custodian context is already closed")
        if self._active:
            raise CustodyValidationError("custodian context is already active")
        self._active = True
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self._active = False
        self._closed = True
        self._private_fixture = None

    def score_trial(
        self,
        snapshots: Any,
        run_envelope: dict[str, Any] | None,
        *,
        raw_output_hashes: Any,
        prompt_hashes: Any,
        usage: Any,
    ) -> dict[str, Any]:
        if not self._active or self._closed or self._private_fixture is None:
            raise CustodyValidationError(
                "held-out scoring is allowed only inside an active custodian context"
            )
        if self._scored:
            raise CustodyValidationError(
                "held-out custodian context has already consumed its one scoring attempt"
            )
        self._scored = True
        if not isinstance(snapshots, list) or len(snapshots) != len(SITTING_ORDER):
            raise CustodyValidationError(
                "held-out scoring requires exactly five ordered account snapshots"
            )
        if not all(isinstance(snapshot, dict) for snapshot in snapshots):
            raise CustodyValidationError(
                "held-out scoring snapshots must be DaseinAccount.v1 objects"
            )
        for label, hashes in (
            ("raw_output_hashes", raw_output_hashes),
            ("prompt_hashes", prompt_hashes),
        ):
            if not isinstance(hashes, dict) or set(hashes) != set(SITTING_ORDER):
                raise CustodyValidationError(
                    f"held-out {label} must bind exactly five sittings"
                )
        if not isinstance(usage, dict):
            raise CustodyValidationError("held-out scoring requires an exact usage ledger")
        if not isinstance(run_envelope, dict):
            raise CustodyValidationError(
                "held-out scoring requires a complete RunEnvelope.v1"
            )
        envelope_errors = validate_run_envelope(run_envelope)
        if envelope_errors:
            raise CustodyValidationError(
                "held-out RunEnvelope.v1 is invalid: " + "; ".join(envelope_errors)
            )
        trial_run_id = None
        if snapshots and isinstance(snapshots[-1], dict):
            causal = snapshots[-1].get("causal_account", {})
            if isinstance(causal, dict):
                trial_run_id = causal.get("run_id")
        if run_envelope.get("run_id") != trial_run_id:
            raise CustodyValidationError(
                "held-out RunEnvelope.v1 run_id does not match the trial"
            )
        private_receipt = score_dasein_trial(
            deepcopy(snapshots),
            deepcopy(self._private_fixture),
            deepcopy(run_envelope),
            raw_output_hashes=deepcopy(raw_output_hashes),
            prompt_hashes=deepcopy(prompt_hashes),
        )
        if private_receipt.get("result_state") in {
            "INVALID_INPUT", "CUSTODY_UNAVAILABLE", "INVALID_RUN",
        }:
            raise CustodyValidationError(
                "private scorer rejected the verified custodian reconstruction"
            )
        private_receipt["usage_hash"] = sha256_value(usage)
        private_receipt["failure_hash"] = sha256_value({})
        private_receipt["trial_transcript_hash"] = sha256_value({
            "snapshot_hashes": private_receipt["snapshot_hashes"],
            "raw_output_hashes": private_receipt["sitting_output_hashes"],
            "prompt_hashes": private_receipt["prompt_hashes"],
            "usage_hash": private_receipt["usage_hash"],
            "failure_hash": private_receipt["failure_hash"],
        })
        receipt_errors = validate_receipt(private_receipt)
        if receipt_errors:
            raise CustodyValidationError(
                "private scorer receipt failed validation after usage binding"
            )
        run_bundle = {
            "run_envelope": deepcopy(run_envelope),
            "trial": {
                "sittings": [
                    {
                        "sitting_id": sitting,
                        "prompt_hash": prompt_hashes[sitting],
                        "raw_output_hash": raw_output_hashes[sitting],
                        "public_account_hash": sha256_value(snapshot),
                        "public_account": deepcopy(snapshot),
                    }
                    for sitting, snapshot in zip(SITTING_ORDER, snapshots)
                ],
                "recorded_source_hash": None,
            },
            "usage": deepcopy(usage),
            "receipt": deepcopy(private_receipt),
        }
        bundle_errors = validate_run_bundle(run_bundle)
        if bundle_errors:
            raise CustodyValidationError(
                "held-out inputs do not form a valid exact run bundle: "
                + "; ".join(bundle_errors)
            )
        public_receipt = _public_receipt(
            private_receipt,
            self._public_fixture,
            self._custody_commitment_sha256,
            self._custody_nonce,
        )
        receipt_errors = validate_public_custodian_receipt(
            public_receipt, self._public_fixture
        )
        if receipt_errors:
            raise CustodyValidationError(
                "public receipt projection failed its internal validator"
            )
        return public_receipt
