#!/usr/bin/env python3
"""Fail-closed validator for the Rosetta vNext seed ledger.

``PackManifest`` freezes native vocabulary, native expressions, and exact
source custody only.
``ProjectionManifest`` separately owns directional normalization, invariant,
loss, dependencies, rival, discriminator, kill criterion, round trip, and its
cells. A cell keeps source fact, mapping, authorization, use, and outcome
states orthogonal.

This validates reproducibility and claim discipline, not projection truth.
Run normally for the live ledger and with ``--self-test`` for negative controls.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
DEFAULT_LEDGER = HERE / "rosetta_cells.json"

PACK_REF_RE = re.compile(r"^[A-Z][A-Z0-9_.-]*@[1-9][0-9]*$")
PROJECTION_REF_RE = re.compile(r"^[A-Z][A-Z0-9_.-]*@[1-9][0-9]*$")
TERM_REF_RE = re.compile(
    r"^(?P<pack>[A-Z][A-Z0-9_.-]*@[1-9][0-9]*):"
    r"(?P<term>[A-Za-z0-9][A-Za-z0-9_.∞-]*)$"
)
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

PACK_REQUIRED = {
    "schema_version",
    "pack_id",
    "version",
    "pack_ref",
    "owner_ref",
    "source_path",
    "native_domain",
    "native_terms",
    "native_term_definitions",
    "native_cardinality",
    "source_version",
    "digest_algorithm",
    "source_exact_digest",
    "native_expression_digest_algorithm",
    "native_expression_digest_canonicalization",
    "native_expression_digest",
    "semantic_digest_status",
    "semantic_canonicalization_id",
    "semantic_canonicalization_version",
    "digest_normalization_operations",
    "lifecycle_status",
}
PACK_NONEMPTY = PACK_REQUIRED - {
    "semantic_canonicalization_id",
    "semantic_canonicalization_version",
    "digest_normalization_operations",
}
PACK_FORBIDDEN_PROJECTION_FIELDS = {
    "target_domain",
    "target_pack_refs",
    "normalization_operations",
    "proposed_invariant",
    "discarded_information",
    "dependency_refs",
    "independence_status",
    "strongest_rival",
    "rival_maps",
    "discriminator",
    "kill_criterion",
    "round_trip_test",
    "cells",
    "supersedes_ref",
    "parent_revision",
}

PROJECTION_REQUIRED = {
    "schema_version",
    "projection_id",
    "projection_revision",
    "projection_ref",
    "parent_revision",
    "supersedes_ref",
    "source_pack_ref",
    "source_pack_binding",
    "target_pack_refs",
    "target_pack_bindings",
    "normalization_operations",
    "proposed_invariant",
    "discarded_information",
    "dependency_refs",
    "independence_status",
    "strongest_rival",
    "rival_maps",
    "discriminator",
    "kill_criterion",
    "round_trip_test",
    "claim_digest_algorithm",
    "claim_digest_canonicalization",
    "claim_semantic_digest",
    "resolution_status",
    "resolution_dispositions",
    "predecessor_comparisons",
    "rejected_claim_digests",
    "lifecycle_status",
    "cells",
}
PROJECTION_NONEMPTY = PROJECTION_REQUIRED - {
    "parent_revision",
    "supersedes_ref",
    "normalization_operations",
    "dependency_refs",
    "resolution_dispositions",
    "predecessor_comparisons",
    "rejected_claim_digests",
}

CELL_REQUIRED = {
    "cell_id",
    "projection_ref",
    "source_ref",
    "target_refs",
    "relation_type",
    "column_class",
    "domain_expression",
    "fit_status",
    "fact_tier",
    "mapping_tier",
    "authorization_status",
    "use_status",
    "outcome_status",
    "source_basis",
    "independence_status",
    "fit_reason",
    "discarded_information",
    "dependency_status",
    "dependency_refs",
    "scale",
    "time_horizon",
    "strongest_rival",
    "discriminator",
    "known_biases",
    "kill_criterion",
    "downgrade_path",
    "authorization_envelope_ref",
    "commitment_receipt_refs",
    "commitment_provenance_records",
    "outcome_receipt_refs",
    "outcome_provenance_records",
    "audit_status",
    "verified_by",
    "verified_at",
    "status_transitions",
}
CELL_NONEMPTY = CELL_REQUIRED - {
    "authorization_envelope_ref",
    "commitment_receipt_refs",
    "commitment_provenance_records",
    "outcome_receipt_refs",
    "outcome_provenance_records",
    "status_transitions",
    "dependency_refs",
}

VALID_INDEPENDENCE = {
    "INDEPENDENT",
    "PARTIALLY_DEPENDENT",
    "FRAMEWORK_DERIVED",
    "UNKNOWN",
}
VALID_RELATIONS = {
    "ONE_TO_ONE",
    "ONE_TO_MANY",
    "MANY_TO_ONE",
    "ANALOGY",
    "INVERSION",
    "BOUNDARY",
    "UNMAPPED_SOURCE",
    "UNFILLED_TARGET",
    "EXTRA",
}
VALID_FIT = {
    "FIT",
    "PARTIAL",
    "MULTIROW",
    "UNMAPPED_SOURCE",
    "UNFILLED_TARGET",
    "EXTRA",
    "DISPUTED",
    "KILLED",
    "ARCHIVED",
}
VALID_AUTHORIZATION = {
    "NOT_REQUESTED",
    "PENDING",
    "AUTHORIZED",
    "REFUSED",
    "EXPIRED",
    "REVOKED",
    "INVALID",
    "ABSENT",
    "NOT_REQUIRED",
}
VALID_USE = {"UNUSED", "PROPOSED", "ATTEMPTED", "ABORTED"}
VALID_OUTCOME = {
    "NOT_OBSERVED",
    "OBSERVED",
    "CONTRADICTED",
    "REPLICATED",
    "NON_INFORMATIVE",
}
VALID_DEPENDENCY = {"DIRECT", "INHERITED", "CIRCULAR", "UNRESOLVED", "NONE"}
VALID_LIFECYCLE = {"DRAFT", "ACTIVE", "DISPUTED", "SUPERSEDED", "KILLED", "ARCHIVED"}
VALID_AUDIT = {"DRAFT", "CHECKED", "DISPUTED", "SUPERSEDED", "KILLED", "ARCHIVED"}
VALID_DEPENDENCY_KINDS = {
    "PACK",
    "PROJECTION",
    "CELL",
    "SOURCE",
    "CONTRACT",
    "INTERPRETER",
}
VALID_DEPENDENCY_BINDING_STATUS = {"BOUND", "DEFERRED"}
VALID_TRANSITION_AXES = {
    "fact_tier",
    "mapping_tier",
    "fit_status",
    "authorization_status",
    "use_status",
    "outcome_status",
}
VALID_EVIDENCE_TIER_VOCABULARY = {"A", "B", "S", "I", "C", "D"}
TERMINAL_FIT = {"KILLED", "ARCHIVED"}
VALID_RESOLUTION = {
    "RESOLVED",
    "UNDERDETERMINED",
    "DEFERRED",
    "KILLED",
    "CYCLE_BLOCKED",
    "BUDGET_EXHAUSTED",
    "AUTHORITY_REQUIRED",
    "SOURCE_UNVERIFIABLE",
}
VALID_RESOLUTION_SCOPES = {
    "SCHEMA_CONFORMANCE",
    "SOURCE_AND_CUSTODY",
    "MAPPING_DISAMBIGUATION",
    "APPLICATION_EVIDENCE",
    "REGIME_CONTROL_ANALYSIS",
}

REGIME_REQUIRED = {
    "schema_ref",
    "surface_ref",
    "observation_window",
    "controller_refs",
    "controller_plurality",
    "concentration_measure",
    "alias_coalitions",
    "contestability",
    "revocability",
    "dependency_refs",
    "receipt_independence",
    "observed_consequences",
    "longitudinal_capture_signatures",
    "political_label",
}


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _canonical_digest(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _native_expression_payload(pack: dict[str, Any]) -> list[dict[str, Any]]:
    return pack.get("native_term_definitions", [])


def _pack_manifest_payload(pack: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "schema_version",
        "pack_id",
        "version",
        "owner_ref",
        "native_domain",
        "native_terms",
        "native_term_definitions",
        "native_cardinality",
        "source_version",
        "digest_algorithm",
        "source_exact_digest",
        "native_expression_digest_algorithm",
        "native_expression_digest_canonicalization",
        "native_expression_digest",
        "semantic_digest_status",
        "semantic_canonicalization_id",
        "semantic_canonicalization_version",
        "digest_normalization_operations",
    )
    return {field: pack.get(field) for field in fields}


def _pack_binding_for(pack: dict[str, Any]) -> dict[str, Any]:
    return {
        "binding_schema": "rs.pack_snapshot_binding.v1",
        "pack_ref": pack.get("pack_ref"),
        "owner_ref": pack.get("owner_ref"),
        "source_version": pack.get("source_version"),
        "source_exact_digest": pack.get("source_exact_digest"),
        "pack_manifest_digest_algorithm": "sha256",
        "pack_manifest_digest_canonicalization": "rs.pack_manifest_digest.v1",
        "pack_manifest_digest": _canonical_digest(_pack_manifest_payload(pack)),
    }


def _claim_dependency_refs(value: Any, owning_projection_ref: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    fields = (
        "binding_schema",
        "kind",
        "ref",
        "binding_status",
        "owner_ref",
        "version",
        "digest_algorithm",
        "digest_canonicalization",
        "digest",
        "deferred_reason",
    )
    return [
        {field: entry.get(field) for field in fields}
        for entry in value
        if isinstance(entry, dict)
        and not (
            entry.get("kind") == "PROJECTION"
            and entry.get("ref") == owning_projection_ref
        )
    ]


def _projection_claim_payload(projection: dict[str, Any]) -> dict[str, Any]:
    cell_fields = (
        "source_ref",
        "target_refs",
        "relation_type",
        "column_class",
        "domain_expression",
        "fit_reason",
        "discarded_information",
        "dependency_status",
        "scale",
        "time_horizon",
        "strongest_rival",
        "discriminator",
        "known_biases",
        "kill_criterion",
        "downgrade_path",
    )
    return {
        "schema_version": projection.get("schema_version"),
        "source_pack_binding": projection.get("source_pack_binding"),
        "target_pack_bindings": projection.get("target_pack_bindings"),
        "normalization_operations": projection.get("normalization_operations"),
        "proposed_invariant": projection.get("proposed_invariant"),
        "discarded_information": projection.get("discarded_information"),
        "dependency_refs": _claim_dependency_refs(
            projection.get("dependency_refs"), projection.get("projection_ref")
        ),
        "independence_status": projection.get("independence_status"),
        "strongest_rival": projection.get("strongest_rival"),
        "rival_maps": projection.get("rival_maps"),
        "discriminator": projection.get("discriminator"),
        "kill_criterion": projection.get("kill_criterion"),
        "round_trip_test": projection.get("round_trip_test"),
        "cells": [
            {
                **{field: cell.get(field) for field in cell_fields},
                "dependency_refs": _claim_dependency_refs(
                    cell.get("dependency_refs"), projection.get("projection_ref")
                ),
            }
            for cell in projection.get("cells", [])
            if isinstance(cell, dict)
        ],
    }


def _check_pack_binding(
    owner: str,
    binding: Any,
    pack: dict[str, Any] | None,
    problems: list[str],
) -> None:
    if not isinstance(binding, dict):
        problems.append(f"{owner}: pack binding must be an object, not an availability string")
        return
    required = {
        "binding_schema",
        "pack_ref",
        "owner_ref",
        "source_version",
        "source_exact_digest",
        "pack_manifest_digest_algorithm",
        "pack_manifest_digest_canonicalization",
        "pack_manifest_digest",
    }
    for field in sorted(required - binding.keys()):
        problems.append(f"{owner}: pack binding missing `{field}`")
    if pack is None:
        problems.append(f"{owner}: bound pack {binding.get('pack_ref')!r} is not declared")
        return
    expected = _pack_binding_for(pack)
    for field, expected_value in expected.items():
        if binding.get(field) != expected_value:
            problems.append(
                f"{owner}: pack binding `{field}` does not match bound PackManifest "
                f"({binding.get(field)!r} != {expected_value!r})"
            )


def _check_external_attestation(
    owner: str,
    value: Any,
    problems: list[str],
    *,
    expected_subject_ref: str | None = None,
    expected_status_axis: str | None = None,
    expected_from_status: str | None = None,
    expected_to_status: str | None = None,
    expected_digest_canonicalization: str | None = None,
    expected_subject_digest: str | None = None,
) -> None:
    required = {
        "schema_version",
        "attestation_ref",
        "verifier_ref",
        "verifier_authority_ref",
        "independence_basis",
        "subject_ref",
        "status_axis",
        "from_status",
        "to_status",
        "subject_digest_algorithm",
        "subject_digest_canonicalization",
        "subject_digest",
        "verification_method_ref",
        "issued_at",
        "custody_ref",
        "signature_or_attestation_ref",
    }
    if not isinstance(value, dict):
        problems.append(f"{owner}: typed external verifier attestation is required")
        return
    for field in sorted(required):
        if not _present(value.get(field)):
            problems.append(f"{owner}: external verifier attestation missing `{field}`")
    if value.get("schema_version") != "rs.external_verifier_attestation.v1":
        problems.append(f"{owner}: external verifier attestation schema is invalid")
    if value.get("subject_digest_algorithm") != "sha256":
        problems.append(f"{owner}: verifier subject_digest_algorithm must be sha256")
    if not isinstance(value.get("subject_digest"), str) or not HEX64_RE.fullmatch(
        value.get("subject_digest", "")
    ):
        problems.append(f"{owner}: verifier subject_digest must be 64 lowercase hex characters")
    expected_fields = {
        "subject_ref": expected_subject_ref,
        "status_axis": expected_status_axis,
        "from_status": expected_from_status,
        "to_status": expected_to_status,
        "subject_digest_canonicalization": expected_digest_canonicalization,
        "subject_digest": expected_subject_digest,
    }
    for field, expected in expected_fields.items():
        if expected is not None and value.get(field) != expected:
            problems.append(
                f"{owner}: verifier `{field}` does not bind the attested transition "
                f"({value.get(field)!r} != {expected!r})"
            )


def _status_transition_subject_payload(
    cell: dict[str, Any], transition: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": "rs.status_transition_subject.v1",
        "subject_ref": cell.get("cell_id"),
        "axis": transition.get("axis"),
        "from": transition.get("from"),
        "to": transition.get("to"),
        "recorded_at": transition.get("recorded_at"),
        "reason": transition.get("reason"),
        "receipt_refs": transition.get("receipt_refs"),
    }


def _predecessor_comparison_subject_payload(
    projection: dict[str, Any], comparison: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": "rs.predecessor_comparison_subject.v1",
        "subject_ref": (
            f"{projection.get('projection_ref')}::{comparison.get('predecessor_ref')}"
        ),
        "predecessor_claim_digest": comparison.get("predecessor_claim_digest"),
        "comparison_status": comparison.get("comparison_status"),
        "comparison_reason": comparison.get("comparison_reason"),
    }


def _resolution_disposition_subject_payload(
    disposition: dict[str, Any],
) -> dict[str, Any]:
    """Canonical subject independently attested when a claim is disposed RESOLVED."""
    return {
        field: value
        for field, value in disposition.items()
        if field != "external_verifier_attestation"
    }


def _projection_resolution_audit_state_payload(
    projection: dict[str, Any], prior_dispositions: list[dict[str, Any]]
) -> dict[str, Any]:
    """Bind the full retained audit state without self-hashing status/disposition."""
    manifest = copy.deepcopy(projection)
    manifest.pop("resolution_status", None)
    manifest.pop("resolution_dispositions", None)
    return {
        "schema_version": "rs.projection_resolution_audit_state.v1",
        "projection_ref": projection.get("projection_ref"),
        "claim_semantic_digest": projection.get("claim_semantic_digest"),
        "projection_manifest_without_resolution_declaration": manifest,
        "prior_resolution_dispositions": prior_dispositions,
    }


def _check_resolution_disposition(
    owner: str,
    projection: dict[str, Any],
    ancestors: list[str],
    comparison_by_ref: dict[str, dict[str, Any]],
    projections: dict[str, dict[str, Any]],
    problems: list[str],
) -> None:
    """Require a scoped, non-circular disposition separate from status declaration."""
    history = projection.get("resolution_dispositions")
    if not isinstance(history, list):
        problems.append(f"{owner}: resolution_dispositions must be an append-only list")
        return
    disposition_refs: list[str] = []
    for index, item in enumerate(history):
        if not isinstance(item, dict):
            problems.append(f"{owner}: resolution_dispositions[{index}] must be an object")
            continue
        disposition_ref = item.get("disposition_ref")
        if not isinstance(disposition_ref, str) or not disposition_ref.strip():
            problems.append(
                f"{owner}: resolution_dispositions[{index}] disposition_ref is empty"
            )
            continue
        if disposition_ref in disposition_refs:
            problems.append(f"{owner}: resolution disposition refs must be unique")
        expected_predecessor = disposition_refs[-1] if disposition_refs else None
        if item.get("predecessor_disposition_ref") != expected_predecessor:
            problems.append(
                f"{owner}: resolution disposition history predecessor chain is broken"
            )
        disposition_refs.append(disposition_ref)

    disposition = history[-1] if history and isinstance(history[-1], dict) else None
    current_matches = bool(
        disposition is not None
        and disposition.get("projection_ref") == projection.get("projection_ref")
    )
    if projection.get("resolution_status") != "RESOLVED":
        if current_matches:
            problems.append(
                f"{owner}: a current resolution disposition cannot be hidden behind a non-RESOLVED status"
            )
        return
    if not current_matches or not isinstance(disposition, dict):
        problems.append(f"{owner}: RESOLVED requires a complete resolution disposition")
        return

    required = {
        "schema_version",
        "disposition_ref",
        "predecessor_disposition_ref",
        "projection_ref",
        "claim_semantic_digest",
        "audit_state_digest_algorithm",
        "audit_state_digest_canonicalization",
        "audit_state_digest",
        "from_status",
        "to_status",
        "lineage_projection_refs",
        "lineage_comparison_attestation_refs",
        "resolution_scopes",
        "scope_limitations",
        "world_efficacy_claim",
        "disposition_authority_ref",
        "decision_ref",
        "decision_custody_ref",
        "trust_boundary_ref",
        "decided_at",
        "reason",
        "discriminator_result_refs",
        "evidence_result_refs",
        "external_verifier_attestation",
    }
    for field in sorted(required - disposition.keys()):
        problems.append(f"{owner}: resolution disposition missing `{field}`")
    for field in (
        "disposition_ref",
        "disposition_authority_ref",
        "decision_ref",
        "decision_custody_ref",
        "trust_boundary_ref",
        "decided_at",
        "reason",
    ):
        if not _present(disposition.get(field)):
            problems.append(f"{owner}: resolution disposition `{field}` is empty")
    for field in (
        "lineage_projection_refs",
        "resolution_scopes",
        "scope_limitations",
        "discriminator_result_refs",
        "evidence_result_refs",
    ):
        value = disposition.get(field)
        if not isinstance(value, list) or not value:
            problems.append(
                f"{owner}: resolution disposition `{field}` must be a non-empty list"
            )
        elif any(not isinstance(item, str) or not item.strip() for item in value):
            problems.append(f"{owner}: resolution disposition `{field}` contains an empty item")
        elif len(value) != len(set(value)):
            problems.append(f"{owner}: resolution disposition `{field}` contains duplicates")
    comparison_refs = disposition.get("lineage_comparison_attestation_refs")
    if not isinstance(comparison_refs, list):
        problems.append(
            f"{owner}: resolution disposition `lineage_comparison_attestation_refs` must be a list"
        )
        comparison_refs = []
    elif any(not isinstance(item, str) or not item.strip() for item in comparison_refs):
        problems.append(
            f"{owner}: resolution disposition lineage comparison refs contain an empty item"
        )

    if disposition.get("schema_version") != "rs.resolution_disposition.v1":
        problems.append(f"{owner}: resolution disposition schema is invalid")
    if disposition.get("projection_ref") != projection.get("projection_ref"):
        problems.append(f"{owner}: resolution disposition projection_ref does not match")
    if disposition.get("claim_semantic_digest") != projection.get("claim_semantic_digest"):
        problems.append(f"{owner}: resolution disposition claim digest does not match")
    if disposition.get("audit_state_digest_algorithm") != "sha256":
        problems.append(f"{owner}: resolution audit-state digest algorithm must be sha256")
    if disposition.get("audit_state_digest_canonicalization") != (
        "rs.projection_resolution_audit_state.v1"
    ):
        problems.append(f"{owner}: resolution audit-state canonicalization is invalid")
    expected_audit_state_digest = _canonical_digest(
        _projection_resolution_audit_state_payload(projection, history[:-1])
    )
    if disposition.get("audit_state_digest") != expected_audit_state_digest:
        problems.append(
            f"{owner}: resolution disposition audit-state digest does not bind the full audit state"
        )
    if disposition.get("from_status") not in VALID_RESOLUTION - {"RESOLVED"}:
        problems.append(f"{owner}: resolution disposition from_status is invalid")
    if disposition.get("to_status") != "RESOLVED":
        problems.append(f"{owner}: resolution disposition to_status must be RESOLVED")
    scopes = disposition.get("resolution_scopes")
    if isinstance(scopes, list) and any(scope not in VALID_RESOLUTION_SCOPES for scope in scopes):
        problems.append(f"{owner}: resolution disposition contains an invalid resolution scope")
    if disposition.get("world_efficacy_claim") is not False:
        problems.append(f"{owner}: theoretical resolution must set world_efficacy_claim false")
    if disposition.get("decision_ref") == disposition.get("disposition_ref"):
        problems.append(f"{owner}: decision_ref must be external to the disposition record")

    expected_lineage = list(reversed(ancestors)) + [projection.get("projection_ref")]
    if disposition.get("lineage_projection_refs") != expected_lineage:
        problems.append(
            f"{owner}: resolution lineage must exactly bind the complete root-to-current path"
        )
    expected_comparison_refs: list[Any] = []
    for ancestor in reversed(ancestors):
        comparison = comparison_by_ref.get(ancestor, {})
        attestation = comparison.get("external_verifier_attestation")
        expected_comparison_refs.append(
            attestation.get("attestation_ref") if isinstance(attestation, dict) else None
        )
    if comparison_refs != expected_comparison_refs:
        problems.append(
            f"{owner}: resolution lineage must bind every predecessor comparison attestation"
        )

    subject_digest = _canonical_digest(
        _resolution_disposition_subject_payload(disposition)
    )
    attestation = disposition.get("external_verifier_attestation")
    _check_external_attestation(
        f"{owner}: resolution disposition",
        attestation,
        problems,
        expected_subject_ref=(
            f"{projection.get('projection_ref')}#resolution-disposition/"
            f"{disposition.get('disposition_ref')}"
        ),
        expected_status_axis="resolution_disposition",
        expected_from_status=(
            disposition.get("from_status")
            if isinstance(disposition.get("from_status"), str)
            else None
        ),
        expected_to_status="RESOLVED",
        expected_digest_canonicalization="rs.resolution_disposition_subject.v1",
        expected_subject_digest=subject_digest,
    )
    if isinstance(attestation, dict):
        protected_refs = {
            disposition.get("disposition_authority_ref"),
            disposition.get("decision_custody_ref"),
            projection.get("source_pack_binding", {}).get("owner_ref")
            if isinstance(projection.get("source_pack_binding"), dict)
            else None,
        } | {
            binding.get("owner_ref")
            for binding in projection.get("target_pack_bindings", [])
            if isinstance(binding, dict)
        }
        for verifier_field in ("verifier_ref", "verifier_authority_ref", "custody_ref"):
            if attestation.get(verifier_field) in protected_refs:
                problems.append(
                    f"{owner}: resolution verifier trust boundary overlaps protected decision/source custody"
                )
        if attestation.get("attestation_ref") == disposition.get("decision_ref"):
            problems.append(
                f"{owner}: decision and verifier attestation must be separately referenced"
            )


def _check_authorization_envelope(owner: str, value: Any, problems: list[str]) -> None:
    required = {
        "schema_version",
        "envelope_ref",
        "envelope_digest_algorithm",
        "envelope_digest",
        "principal_ref",
        "mandate_ref",
        "scope",
        "consent_ref",
        "custody_ref",
        "valid_from",
        "expires_at",
        "revocation_ref",
        "revocation_checked_at",
        "contest_path_ref",
        "actor_ref",
        "consequence_bearer_refs",
    }
    if not isinstance(value, dict):
        problems.append(f"{owner}: complete AuthorizationEnvelope reference is required")
        return
    for field in sorted(required - value.keys()):
        problems.append(f"{owner}: AuthorizationEnvelope missing `{field}`")
    for field in (
        "envelope_ref",
        "principal_ref",
        "mandate_ref",
        "scope",
        "consent_ref",
        "custody_ref",
        "valid_from",
        "revocation_checked_at",
        "contest_path_ref",
        "actor_ref",
        "consequence_bearer_refs",
    ):
        if field in value and not _present(value.get(field)):
            problems.append(f"{owner}: AuthorizationEnvelope `{field}` is empty")
    if value.get("schema_version") != "rs.authorization_envelope_ref.v1":
        problems.append(f"{owner}: AuthorizationEnvelope schema is invalid")
    if value.get("envelope_digest_algorithm") != "sha256":
        problems.append(f"{owner}: AuthorizationEnvelope digest algorithm must be sha256")
    if not isinstance(value.get("envelope_digest"), str) or not HEX64_RE.fullmatch(
        value.get("envelope_digest", "")
    ):
        problems.append(f"{owner}: AuthorizationEnvelope digest must be 64 lowercase hex characters")
    if value.get("expires_at") is None and value.get("revocation_ref") is None:
        problems.append(f"{owner}: AuthorizationEnvelope needs expiry or revocation control")


def _check_provenance_records(
    owner: str,
    records: Any,
    kind: str,
    problems: list[str],
) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        problems.append(f"{owner}: {kind}_provenance_records must be a list")
        return []
    schema = f"rs.{kind}_provenance.v1"
    common = {
        "schema_version",
        "receipt_ref",
        "issuer_ref",
        "evidence_authority_ref",
        "custody_ref",
        "signature_or_attestation_ref",
    }
    extra = {"record_digest"} if kind == "commitment" else {
        "observation_ref",
        "observation_digest",
        "method_ref",
        "independence_basis",
    }
    valid: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        prefix = f"{owner}: {kind}_provenance_records[{index}]"
        if not isinstance(record, dict):
            problems.append(f"{prefix} must be an object")
            continue
        for field in sorted(common | extra):
            if not isinstance(record.get(field), str) or not record.get(field, "").strip():
                problems.append(f"{prefix} missing non-empty string `{field}`")
        if record.get("schema_version") != schema:
            problems.append(f"{prefix} schema_version must be {schema}")
        digest_field = "record_digest" if kind == "commitment" else "observation_digest"
        if not isinstance(record.get(digest_field), str) or not HEX64_RE.fullmatch(
            record.get(digest_field, "")
        ):
            problems.append(f"{prefix} `{digest_field}` must be 64 lowercase hex characters")
        valid.append(record)
    return valid


def _safe_source_path(base_dir: Path, raw_path: Any) -> tuple[Path | None, str | None]:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None, "source_path is not a non-empty string"
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return None, "source_path must be relative to the ledger directory"
    ledger_dir = base_dir.resolve()
    corpus_root = ledger_dir.parents[2]
    resolved = (ledger_dir / candidate).resolve()
    try:
        resolved.relative_to(corpus_root)
    except ValueError:
        return None, "source_path escapes the Emergentism corpus root"
    return resolved, None


def _check_receipt_list(owner: str, field: str, value: Any, problems: list[str]) -> list[str]:
    if not isinstance(value, list):
        problems.append(f"{owner}: `{field}` must be a list")
        return []
    if any(not isinstance(ref, str) or not ref.strip() for ref in value):
        problems.append(f"{owner}: `{field}` contains an empty receipt reference")
    return [ref for ref in value if isinstance(ref, str) and ref.strip()]


def _dependency_entries(
    owner: str,
    value: Any,
    problems: list[str],
    *,
    base_dir: Path,
    check_source_files: bool,
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        problems.append(f"{owner}: dependency_refs must be a declared list")
        return []
    entries: list[dict[str, Any]] = []
    for index, entry in enumerate(value):
        prefix = f"{owner}: dependency_refs[{index}]"
        if not isinstance(entry, dict):
            problems.append(f"{prefix} must be an object")
            continue
        kind = entry.get("kind")
        ref = entry.get("ref")
        required = {
            "binding_schema",
            "kind",
            "ref",
            "binding_status",
            "owner_ref",
            "version",
            "digest_algorithm",
            "digest_canonicalization",
            "digest",
            "deferred_reason",
        }
        for field in sorted(required - entry.keys()):
            problems.append(f"{prefix} missing `{field}`")
        if entry.get("binding_schema") != "rs.dependency_binding.v1":
            problems.append(f"{prefix}.binding_schema must be rs.dependency_binding.v1")
        if kind not in VALID_DEPENDENCY_KINDS:
            problems.append(f"{prefix}.kind {kind!r} is invalid")
            continue
        if not isinstance(ref, str) or not ref.strip():
            problems.append(f"{prefix}.ref is empty")
            continue
        if kind == "PROJECTION" and not PROJECTION_REF_RE.fullmatch(ref):
            problems.append(f"{prefix} {ref!r} is malformed; use projection_id@revision")
        if kind == "PACK" and not PACK_REF_RE.fullmatch(ref):
            problems.append(f"{prefix} {ref!r} is malformed; use pack_id@version")
        if kind == "CONTRACT" and not PACK_REF_RE.fullmatch(ref):
            problems.append(f"{prefix} {ref!r} is malformed; use contract_id@version")
        binding_status = entry.get("binding_status")
        if binding_status not in VALID_DEPENDENCY_BINDING_STATUS:
            problems.append(f"{prefix}.binding_status {binding_status!r} is invalid")
        if binding_status == "BOUND":
            for field in (
                "owner_ref",
                "version",
                "digest_algorithm",
                "digest_canonicalization",
                "digest",
            ):
                if not _present(entry.get(field)):
                    problems.append(f"{prefix}: BOUND dependency missing `{field}`")
            if entry.get("digest_algorithm") != "sha256":
                problems.append(f"{prefix}: BOUND dependency digest_algorithm must be sha256")
            if not isinstance(entry.get("digest"), str) or not HEX64_RE.fullmatch(
                entry.get("digest", "")
            ):
                problems.append(f"{prefix}: BOUND dependency digest must be 64 lowercase hex")
            if entry.get("deferred_reason") is not None:
                problems.append(f"{prefix}: BOUND dependency deferred_reason must be null")
            if entry.get("digest_canonicalization") == "exact-bytes":
                source_path, source_error = _safe_source_path(base_dir, entry.get("owner_ref"))
                if source_error:
                    problems.append(f"{prefix}: {source_error}")
                elif check_source_files and source_path is not None:
                    if not source_path.is_file():
                        problems.append(f"{prefix}: bound dependency source does not exist: {source_path}")
                    elif isinstance(entry.get("digest"), str):
                        actual = hashlib.sha256(source_path.read_bytes()).hexdigest()
                        if actual != entry.get("digest"):
                            problems.append(
                                f"{prefix}: bound dependency drift — expected "
                                f"{entry.get('digest')}, got {actual}"
                            )
        elif binding_status == "DEFERRED":
            if not _present(entry.get("deferred_reason")):
                problems.append(f"{prefix}: DEFERRED dependency requires deferred_reason")
            for field in (
                "owner_ref",
                "version",
                "digest_algorithm",
                "digest_canonicalization",
                "digest",
            ):
                if entry.get(field) is not None:
                    problems.append(f"{prefix}: DEFERRED dependency `{field}` must be null")
        entries.append({field: entry.get(field) for field in required})
    return entries


def _find_cycles(graph: dict[str, list[str]], label: str, problems: list[str]) -> None:
    state: dict[str, int] = {}
    stack: list[str] = []
    reported: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in graph:
                continue
            if state.get(neighbor, 0) == 0:
                visit(neighbor)
            elif state.get(neighbor) == 1:
                start = stack.index(neighbor)
                cycle = tuple(stack[start:] + [neighbor])
                if cycle not in reported:
                    reported.add(cycle)
                    problems.append(f"{label} cycle: {' -> '.join(cycle)}")
        stack.pop()
        state[node] = 2

    for node in graph:
        if state.get(node, 0) == 0:
            visit(node)


def _check_round_trip(owner: str, value: Any, problems: list[str]) -> None:
    if not isinstance(value, dict):
        problems.append(f"{owner}: round_trip_test must be an object")
        return
    for field in ("route", "must_preserve", "must_report_as_loss"):
        if not _present(value.get(field)):
            problems.append(f"{owner}: round_trip_test `{field}` is empty")


def _validate_transitions(
    owner: str,
    cell: dict[str, Any],
    evidence_tiers: set[str],
    problems: list[str],
) -> None:
    transitions = cell.get("status_transitions")
    if not isinstance(transitions, list):
        problems.append(f"{owner}: status_transitions must be an append-only list")
        return
    last_to: dict[str, Any] = {}
    for index, transition in enumerate(transitions):
        prefix = f"{owner}: status_transitions[{index}]"
        if not isinstance(transition, dict):
            problems.append(f"{prefix} must be an object")
            continue
        for field in (
            "axis",
            "from",
            "to",
            "recorded_at",
            "reason",
            "receipt_refs",
            "external_verifier_attestation",
        ):
            if field not in transition:
                problems.append(f"{prefix} missing `{field}`")
        for field in ("axis", "from", "to", "recorded_at", "reason"):
            if field in transition and not _present(transition.get(field)):
                problems.append(f"{prefix} has empty `{field}`")
        axis = transition.get("axis")
        old = transition.get("from")
        new = transition.get("to")
        receipts = _check_receipt_list(prefix, "receipt_refs", transition.get("receipt_refs"), problems)
        subject_payload = _status_transition_subject_payload(cell, transition)
        _check_external_attestation(
            prefix,
            transition.get("external_verifier_attestation"),
            problems,
            expected_subject_ref=str(cell.get("cell_id")),
            expected_status_axis=axis if isinstance(axis, str) else None,
            expected_from_status=old if isinstance(old, str) else None,
            expected_to_status=new if isinstance(new, str) else None,
            expected_digest_canonicalization="rs.status_transition_subject.v1",
            expected_subject_digest=_canonical_digest(subject_payload),
        )
        if axis not in VALID_TRANSITION_AXES:
            problems.append(f"{prefix}: axis {axis!r} is invalid")
            continue
        valid_values = {
            "fact_tier": evidence_tiers,
            "mapping_tier": evidence_tiers,
            "fit_status": VALID_FIT,
            "authorization_status": VALID_AUTHORIZATION,
            "use_status": VALID_USE,
            "outcome_status": VALID_OUTCOME,
        }[axis]
        if old not in valid_values or new not in valid_values:
            problems.append(f"{prefix}: {old!r} -> {new!r} uses an invalid value")
            continue
        if axis in last_to and old != last_to[axis]:
            problems.append(f"{prefix}: append-only transition chain is broken")
        last_to[axis] = new
        receipt_required = False
        if axis in {"fact_tier", "mapping_tier"}:
            # Evidence tiers are warrant kinds, not a total strength order. Any
            # change of kind therefore needs an inspectable basis; there is no
            # rank direction that can safely waive the receipt requirement.
            receipt_required = new != old
        elif axis == "fit_status":
            if old in TERMINAL_FIT and new != old:
                problems.append(f"{prefix}: terminal projection revision must be superseded, not rewritten")
            receipt_required = new in {"FIT", "PARTIAL", "MULTIROW"} and new != old
        elif axis == "authorization_status":
            receipt_required = new in {"PENDING", "AUTHORIZED", "NOT_REQUIRED"} and new != old
        elif axis == "use_status":
            receipt_required = new != "UNUSED" and new != old
        elif axis == "outcome_status":
            receipt_required = new != "NOT_OBSERVED" and new != old
        if receipt_required and not receipts:
            if axis in {"fact_tier", "mapping_tier"}:
                problems.append(
                    f"{prefix}: evidence-kind change {old} -> {new} requires a receipt"
                )
            else:
                problems.append(f"{prefix}: status change {old} -> {new} requires a receipt")
    for axis, new in last_to.items():
        if cell.get(axis) != new:
            problems.append(f"{owner}: current {axis} does not match its last transition")


def validate(
    data: Any,
    *,
    base_dir: Path = HERE,
    check_source_files: bool = True,
) -> list[str]:
    problems: list[str] = []
    if not isinstance(data, dict):
        return ["ledger root must be a JSON object"]
    if data.get("schema_ref") != "RS.CORE@1:pack-projection-cell-ledger-v3":
        problems.append("ledger: schema_ref must be RS.CORE@1:pack-projection-cell-ledger-v3")
    if data.get("ledger_revision") != 3:
        problems.append("ledger: ledger_revision must be integer 3")
    if "cells" in data:
        problems.append("ledger: top-level cells are forbidden; ProjectionManifest owns its cells")

    if "tier_order" in data:
        problems.append(
            "ledger: tier_order is forbidden; evidence tiers are warrant kinds, not a total order"
        )
    vocabulary = data.get("evidence_tier_vocabulary")
    if (
        not isinstance(vocabulary, list)
        or not vocabulary
        or any(not isinstance(tier, str) or not tier for tier in vocabulary)
        or len(vocabulary) != len(set(vocabulary))
    ):
        problems.append(
            "ledger: evidence_tier_vocabulary must be a non-empty unique string list"
        )
        evidence_tiers: set[str] = set()
    else:
        evidence_tiers = set(vocabulary)
        if evidence_tiers != VALID_EVIDENCE_TIER_VOCABULARY:
            problems.append(
                "ledger: evidence_tier_vocabulary must contain exactly A, B, S, I, C, and D; "
                "list position has no strength meaning"
            )
    packs_raw = data.get("packs")
    projections_raw = data.get("projections")
    regimes_raw = data.get("regime_records")
    if not isinstance(packs_raw, list):
        problems.append("ledger: packs must be a list")
        packs_raw = []
    if not isinstance(projections_raw, list):
        problems.append("ledger: projections must be a list")
        projections_raw = []
    if not isinstance(regimes_raw, list):
        problems.append("ledger: regime_records must be a list")
        regimes_raw = []

    for index, regime in enumerate(regimes_raw):
        owner = f"regime_records[{index}]"
        if not isinstance(regime, dict):
            problems.append(f"{owner}: must be an object")
            continue
        for field in sorted(REGIME_REQUIRED - regime.keys()):
            problems.append(f"{owner}: missing required field `{field}`")
        if regime.get("schema_ref") != "RS.REGIME@1":
            problems.append(f"{owner}: schema_ref must be RS.REGIME@1")
        for field in (
            "surface_ref",
            "observation_window",
            "controller_refs",
            "controller_plurality",
            "concentration_measure",
            "contestability",
            "revocability",
            "receipt_independence",
        ):
            if field in regime and not _present(regime.get(field)):
                problems.append(f"{owner}: `{field}` must be non-empty")
        for field in (
            "controller_refs",
            "alias_coalitions",
            "observed_consequences",
            "longitudinal_capture_signatures",
        ):
            value = regime.get(field)
            if not isinstance(value, list):
                problems.append(f"{owner}: `{field}` must be a list")
        controller_refs = regime.get("controller_refs")
        if isinstance(controller_refs, list):
            if any(not isinstance(ref, str) or not ref.strip() for ref in controller_refs):
                problems.append(f"{owner}: controller_refs contains an empty reference")
            if len(controller_refs) != len(set(ref for ref in controller_refs if isinstance(ref, str))):
                problems.append(f"{owner}: controller_refs contains duplicates")
        if regime.get("political_label") is not None:
            problems.append(
                f"{owner}: political_label must be null; control observations do not "
                "deterministically emit a political regime"
            )
        _dependency_entries(
            owner,
            regime.get("dependency_refs"),
            problems,
            base_dir=base_dir,
            check_source_files=check_source_files,
        )

    packs: dict[str, dict[str, Any]] = {}
    for index, pack in enumerate(packs_raw):
        owner = f"pack[{index}]"
        if not isinstance(pack, dict):
            problems.append(f"{owner}: must be an object")
            continue
        pref = pack.get("pack_ref")
        owner = f"pack {pref or '<unnamed>'}"
        for field in sorted(PACK_REQUIRED - pack.keys()):
            problems.append(f"{owner}: missing required field `{field}`")
        for field in sorted(PACK_NONEMPTY & pack.keys()):
            if not _present(pack[field]):
                problems.append(f"{owner}: required field `{field}` is empty")
        for field in sorted(PACK_FORBIDDEN_PROJECTION_FIELDS & pack.keys()):
            problems.append(
                f"{owner}: projection-only field `{field}` is forbidden in a native PackManifest"
            )
        if pack.get("schema_version") != "rs.pack_manifest.v2":
            problems.append(
                f"{owner}: active seed schema_version must be rs.pack_manifest.v2; "
                "v1 is historical/read-only"
            )
        pid = pack.get("pack_id")
        version = pack.get("version")
        if not isinstance(pid, str) or not re.fullmatch(r"[A-Z][A-Z0-9_.-]*", pid):
            problems.append(f"{owner}: pack_id {pid!r} is malformed")
        if isinstance(version, bool) or not isinstance(version, int) or version < 1:
            problems.append(f"{owner}: version must be a positive integer")
        expected_ref = f"{pid}@{version}"
        if pref != expected_ref or not isinstance(pref, str) or not PACK_REF_RE.fullmatch(pref):
            problems.append(f"{owner}: pack_ref must be {expected_ref!r}")
        elif pref in packs:
            problems.append(f"{owner}: duplicate pack_ref")
        else:
            packs[pref] = pack

        terms = pack.get("native_terms")
        cardinality = pack.get("native_cardinality")
        if not isinstance(terms, list) or any(not isinstance(term, str) or not term for term in terms):
            problems.append(f"{owner}: native_terms must be a list of non-empty strings")
            terms = []
        elif len(terms) != len(set(terms)):
            problems.append(f"{owner}: native_terms contains duplicates")
        definitions = pack.get("native_term_definitions")
        definition_keys: list[str] = []
        if not isinstance(definitions, list):
            problems.append(f"{owner}: native_term_definitions must be an ordered list")
            definitions = []
        for def_index, definition in enumerate(definitions):
            prefix = f"{owner}: native_term_definitions[{def_index}]"
            if not isinstance(definition, dict):
                problems.append(f"{prefix} must be an object")
                continue
            for field in ("term_key", "label", "description"):
                if not _present(definition.get(field)):
                    problems.append(f"{prefix} missing non-empty `{field}`")
            if isinstance(definition.get("term_key"), str):
                definition_keys.append(definition["term_key"])
        if definition_keys != terms:
            problems.append(
                f"{owner}: native_term_definitions keys/order must exactly equal native_terms"
            )
        if isinstance(cardinality, bool) or not isinstance(cardinality, int) or cardinality < 1:
            problems.append(f"{owner}: native_cardinality must be a positive integer")
        elif len(terms) != cardinality:
            problems.append(
                f"{owner}: hidden cardinality — native_cardinality is {cardinality} "
                f"but native_terms contains {len(terms)} terms"
            )
        if pack.get("digest_algorithm") != "sha256":
            problems.append(f"{owner}: only digest_algorithm 'sha256' is supported")
        exact_digest = pack.get("source_exact_digest")
        if not isinstance(exact_digest, str) or not HEX64_RE.fullmatch(exact_digest):
            problems.append(f"{owner}: source_exact_digest must be 64 lowercase hex characters")
        if pack.get("native_expression_digest_algorithm") != "sha256":
            problems.append(f"{owner}: native_expression_digest_algorithm must be sha256")
        if pack.get("native_expression_digest_canonicalization") != "rs.native_term_definitions.v1":
            problems.append(
                f"{owner}: native_expression_digest_canonicalization must be "
                "rs.native_term_definitions.v1"
            )
        expression_digest = pack.get("native_expression_digest")
        if not isinstance(expression_digest, str) or not HEX64_RE.fullmatch(expression_digest):
            problems.append(f"{owner}: native_expression_digest must be 64 lowercase hex characters")
        elif expression_digest != _canonical_digest(_native_expression_payload(pack)):
            problems.append(f"{owner}: native expression digest does not match key-label-description model")
        if pack.get("semantic_digest_status") != "PROVISIONAL":
            problems.append(f"{owner}: active seed supports semantic_digest_status PROVISIONAL only")
        if pack.get("semantic_canonicalization_id") is not None:
            problems.append(f"{owner}: provisional semantic_canonicalization_id must be null")
        if pack.get("semantic_canonicalization_version") is not None:
            problems.append(f"{owner}: provisional semantic_canonicalization_version must be null")
        if pack.get("digest_normalization_operations") != []:
            problems.append(
                f"{owner}: provisional digest_normalization_operations must be empty; "
                "mapping normalization belongs to ProjectionManifest"
            )
        if "source_semantic_digest" in pack:
            problems.append(f"{owner}: provisional pack may not claim a source_semantic_digest")
        source_path, source_error = _safe_source_path(base_dir, pack.get("source_path"))
        if source_error:
            problems.append(f"{owner}: {source_error}")
        elif check_source_files and source_path is not None:
            if not source_path.is_file():
                problems.append(f"{owner}: source file does not exist: {source_path}")
            elif isinstance(exact_digest, str):
                actual = hashlib.sha256(source_path.read_bytes()).hexdigest()
                if actual != exact_digest:
                    problems.append(
                        f"{owner}: exact source drift — expected {exact_digest}, got {actual}"
                    )
        if pack.get("lifecycle_status") not in VALID_LIFECYCLE:
            problems.append(f"{owner}: lifecycle_status is invalid")

    projections: dict[str, dict[str, Any]] = {}
    projection_dependencies: dict[str, list[str]] = {}
    projection_dependency_entries: dict[str, list[dict[str, Any]]] = {}
    projection_supersession: dict[str, list[str]] = {}
    cells: dict[str, dict[str, Any]] = {}
    cell_dependencies: dict[str, list[str]] = {}
    cell_dependency_entries: dict[str, list[dict[str, Any]]] = {}

    for index, projection in enumerate(projections_raw):
        owner = f"projection[{index}]"
        if not isinstance(projection, dict):
            problems.append(f"{owner}: must be an object")
            continue
        pref = projection.get("projection_ref")
        owner = f"projection {pref or '<unnamed>'}"
        for field in sorted(PROJECTION_REQUIRED - projection.keys()):
            problems.append(f"{owner}: missing required field `{field}`")
        for field in sorted(PROJECTION_NONEMPTY & projection.keys()):
            if not _present(projection[field]):
                problems.append(f"{owner}: required field `{field}` is empty")
        if projection.get("schema_version") != "rs.projection_manifest.v2":
            problems.append(
                f"{owner}: active seed schema_version must be rs.projection_manifest.v2; "
                "v1 is historical/read-only"
            )
        pid = projection.get("projection_id")
        revision = projection.get("projection_revision")
        if not isinstance(pid, str) or not re.fullmatch(r"[A-Z][A-Z0-9_.-]*", pid):
            problems.append(f"{owner}: projection_id {pid!r} is malformed")
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
            problems.append(f"{owner}: projection_revision must be a positive integer")
        expected_ref = f"{pid}@{revision}"
        if pref != expected_ref or not isinstance(pref, str) or not PROJECTION_REF_RE.fullmatch(pref):
            problems.append(f"{owner}: projection_ref must be {expected_ref!r}")
        elif pref in projections:
            problems.append(f"{owner}: duplicate projection_ref")
        else:
            projections[pref] = projection

        source_pack = projection.get("source_pack_ref")
        targets = projection.get("target_pack_refs")
        if source_pack not in packs:
            problems.append(f"{owner}: source_pack_ref {source_pack!r} is not declared")
        if not isinstance(targets, list) or not targets:
            problems.append(f"{owner}: target_pack_refs must be a non-empty list")
            targets = []
        elif len(targets) != len(set(targets)):
            problems.append(f"{owner}: target_pack_refs contains duplicates")
        for target in targets:
            if target not in packs:
                problems.append(f"{owner}: target pack {target!r} is not declared")

        _check_pack_binding(
            f"{owner} source_pack_binding",
            projection.get("source_pack_binding"),
            packs.get(source_pack),
            problems,
        )
        target_bindings = projection.get("target_pack_bindings")
        if not isinstance(target_bindings, list):
            problems.append(f"{owner}: target_pack_bindings must be an ordered list")
            target_bindings = []
        if len(target_bindings) != len(targets):
            problems.append(
                f"{owner}: target_pack_bindings must have one binding per target_pack_ref"
            )
        bound_target_refs = [
            binding.get("pack_ref") if isinstance(binding, dict) else None
            for binding in target_bindings
        ]
        if bound_target_refs != targets:
            problems.append(
                f"{owner}: target_pack_bindings order/refs must exactly equal target_pack_refs"
            )
        for target_index, target in enumerate(targets):
            binding = target_bindings[target_index] if target_index < len(target_bindings) else None
            _check_pack_binding(
                f"{owner} target_pack_bindings[{target_index}]",
                binding,
                packs.get(target),
                problems,
            )

        if projection.get("claim_digest_algorithm") != "sha256":
            problems.append(f"{owner}: claim_digest_algorithm must be sha256")
        if projection.get("claim_digest_canonicalization") != "rs.projection_claim_digest.v1":
            problems.append(
                f"{owner}: claim_digest_canonicalization must be rs.projection_claim_digest.v1"
            )
        claim_digest = projection.get("claim_semantic_digest")
        if not isinstance(claim_digest, str) or not HEX64_RE.fullmatch(claim_digest):
            problems.append(f"{owner}: claim_semantic_digest must be 64 lowercase hex characters")
        if projection.get("resolution_status") not in VALID_RESOLUTION:
            problems.append(f"{owner}: resolution_status is invalid")
        if not isinstance(projection.get("predecessor_comparisons"), list):
            problems.append(f"{owner}: predecessor_comparisons must be an append-only list")
        if not isinstance(projection.get("rejected_claim_digests"), list):
            problems.append(f"{owner}: rejected_claim_digests must be a monotonic list")

        operations = projection.get("normalization_operations")
        if not isinstance(operations, list):
            problems.append(f"{owner}: normalization_operations must be an ordered list")
            operations = []
        for op_index, operation in enumerate(operations):
            if not isinstance(operation, dict):
                problems.append(f"{owner}: normalization_operations[{op_index}] must be an object")
                continue
            for field in ("operation", "detail", "destroyed_information"):
                if not _present(operation.get(field)):
                    problems.append(f"{owner}: normalization_operations[{op_index}] missing `{field}`")
        if not isinstance(projection.get("discarded_information"), list) or not projection.get(
            "discarded_information"
        ):
            problems.append(f"{owner}: discarded_information must be a non-empty loss list")
        if not isinstance(projection.get("rival_maps"), list) or not projection.get("rival_maps"):
            problems.append(f"{owner}: rival_maps must name at least one rival")
        if projection.get("independence_status") not in VALID_INDEPENDENCE:
            problems.append(f"{owner}: independence_status is invalid")
        if projection.get("lifecycle_status") not in VALID_LIFECYCLE:
            problems.append(f"{owner}: lifecycle_status is invalid")
        _check_round_trip(owner, projection.get("round_trip_test"), problems)
        deps = _dependency_entries(
            owner,
            projection.get("dependency_refs"),
            problems,
            base_dir=base_dir,
            check_source_files=check_source_files,
        )
        projection_dependency_entries[pref] = deps
        projection_dependencies[pref] = [
            entry["ref"]
            for entry in deps
            if entry["kind"] == "PROJECTION" and entry.get("binding_status") == "BOUND"
        ]
        predecessor = projection.get("supersedes_ref")
        projection_supersession[pref] = [predecessor] if isinstance(predecessor, str) else []
        parent_revision = projection.get("parent_revision")
        if revision == 1 and (parent_revision is not None or predecessor is not None):
            problems.append(f"{owner}: revision 1 must have null parent_revision and supersedes_ref")
        if isinstance(revision, int) and revision > 1:
            if not isinstance(parent_revision, int) or parent_revision < 1:
                problems.append(f"{owner}: later revision requires a positive parent_revision")
            if not isinstance(predecessor, str):
                problems.append(f"{owner}: later revision requires supersedes_ref")

        projection_cells = projection.get("cells")
        if not isinstance(projection_cells, list) or not projection_cells:
            problems.append(f"{owner}: cells must be a non-empty list owned by the projection")
            projection_cells = []
        for cell_index, cell in enumerate(projection_cells):
            cell_owner = f"{owner} cell[{cell_index}]"
            if not isinstance(cell, dict):
                problems.append(f"{cell_owner}: must be an object")
                continue
            cid = cell.get("cell_id")
            cell_owner = f"cell {cid or '<unnamed>'}"
            for field in sorted(CELL_REQUIRED - cell.keys()):
                problems.append(f"{cell_owner}: missing required field `{field}`")
            for field in sorted(CELL_NONEMPTY & cell.keys()):
                if not _present(cell[field]):
                    problems.append(f"{cell_owner}: required field `{field}` is empty")
            for deprecated in ("row", "cell_tier", "projection_id", "revision", "supersedes"):
                if deprecated in cell:
                    problems.append(f"{cell_owner}: deprecated `{deprecated}` collapses v2 types")
            if not isinstance(cid, str) or not cid:
                continue
            if cid in cells:
                problems.append(f"{cell_owner}: duplicate cell_id")
            else:
                cells[cid] = cell
            if cell.get("projection_ref") != pref:
                problems.append(f"{cell_owner}: projection_ref must be owning projection {pref}")

            source_ref = cell.get("source_ref")
            cell_targets = cell.get("target_refs")
            source_match = TERM_REF_RE.fullmatch(source_ref) if isinstance(source_ref, str) else None
            source_term = None
            if not source_match:
                problems.append(
                    f"{cell_owner}: source_ref {source_ref!r} is bare or malformed; "
                    "use pack_id@version:term_key"
                )
            else:
                source_term = source_match.group("term")
                source_ref_pack = source_match.group("pack")
                if source_ref_pack != source_pack:
                    problems.append(f"{cell_owner}: source_ref is outside projection source_pack_ref")
                elif source_ref_pack in packs and source_term not in packs[source_ref_pack].get(
                    "native_terms", []
                ):
                    problems.append(f"{cell_owner}: source term is absent from native_terms")
            if not isinstance(cell_targets, list) or not cell_targets:
                problems.append(f"{cell_owner}: target_refs must be a non-empty list")
                cell_targets = []
            elif len(cell_targets) != len(set(cell_targets)):
                problems.append(f"{cell_owner}: target_refs contains duplicates")
            target_terms: list[str] = []
            for target in cell_targets:
                match = TERM_REF_RE.fullmatch(target) if isinstance(target, str) else None
                if not match:
                    problems.append(
                        f"{cell_owner}: target_ref {target!r} is bare or malformed; "
                        "use pack_id@version:term_key"
                    )
                    continue
                target_pack = match.group("pack")
                target_term = match.group("term")
                target_terms.append(target_term)
                if target_pack not in targets:
                    problems.append(f"{cell_owner}: target_ref is outside projection target_pack_refs")
                elif target_pack in packs and target_term not in packs[target_pack].get("native_terms", []):
                    problems.append(f"{cell_owner}: target term is absent from native_terms")
            expected_id = (
                f"{pref}:{source_term}_to_{'_and_'.join(target_terms)}"
                if source_term and target_terms
                else None
            )
            if expected_id is not None and cid != expected_id:
                problems.append(f"{cell_owner}: cell_id must be {expected_id!r}")

            relation = cell.get("relation_type")
            if relation not in VALID_RELATIONS:
                problems.append(f"{cell_owner}: relation_type {relation!r} is invalid")
            if relation == "ONE_TO_MANY" and len(cell_targets) < 2:
                problems.append(f"{cell_owner}: ONE_TO_MANY requires at least two targets")
            if relation in {"ONE_TO_ONE", "ANALOGY", "INVERSION", "BOUNDARY"} and len(
                cell_targets
            ) != 1:
                problems.append(f"{cell_owner}: {relation} requires exactly one target")

            fact = cell.get("fact_tier")
            mapping = cell.get("mapping_tier")
            if fact not in evidence_tiers:
                problems.append(
                    f"{cell_owner}: fact_tier {fact!r} is not in evidence_tier_vocabulary"
                )
            if mapping not in evidence_tiers:
                problems.append(
                    f"{cell_owner}: mapping_tier {mapping!r} is not in evidence_tier_vocabulary"
                )
            if cell.get("fit_status") not in VALID_FIT:
                problems.append(f"{cell_owner}: fit_status is invalid")
            if cell.get("authorization_status") not in VALID_AUTHORIZATION:
                problems.append(f"{cell_owner}: authorization_status is invalid")
            if cell.get("use_status") not in VALID_USE:
                problems.append(f"{cell_owner}: use_status is invalid")
            if cell.get("outcome_status") not in VALID_OUTCOME:
                problems.append(f"{cell_owner}: outcome_status is invalid")
            if cell.get("independence_status") not in VALID_INDEPENDENCE:
                problems.append(f"{cell_owner}: independence_status is invalid")
            if cell.get("dependency_status") not in VALID_DEPENDENCY:
                problems.append(f"{cell_owner}: dependency_status is invalid")
            if cell.get("audit_status") not in VALID_AUDIT:
                problems.append(f"{cell_owner}: audit_status is invalid")

            authorization_ref = cell.get("authorization_envelope_ref")
            if authorization_ref is not None:
                _check_authorization_envelope(cell_owner, authorization_ref, problems)
            if cell.get("authorization_status") in {"AUTHORIZED", "EXPIRED", "REVOKED"}:
                if authorization_ref is None:
                    problems.append(
                        f"{cell_owner}: authorization_status {cell.get('authorization_status')} "
                        "requires a complete AuthorizationEnvelope reference"
                    )
            commitment_receipts = _check_receipt_list(
                cell_owner,
                "commitment_receipt_refs",
                cell.get("commitment_receipt_refs"),
                problems,
            )
            outcome_receipts = _check_receipt_list(
                cell_owner, "outcome_receipt_refs", cell.get("outcome_receipt_refs"), problems
            )
            commitment_records = _check_provenance_records(
                cell_owner,
                cell.get("commitment_provenance_records"),
                "commitment",
                problems,
            )
            outcome_records = _check_provenance_records(
                cell_owner,
                cell.get("outcome_provenance_records"),
                "outcome",
                problems,
            )
            commitment_record_refs = [
                record.get("receipt_ref")
                for record in commitment_records
                if isinstance(record.get("receipt_ref"), str)
            ]
            outcome_record_refs = [
                record.get("receipt_ref")
                for record in outcome_records
                if isinstance(record.get("receipt_ref"), str)
            ]
            if len(commitment_receipts) != len(set(commitment_receipts)):
                problems.append(f"{cell_owner}: commitment_receipt_refs contains duplicates")
            if len(outcome_receipts) != len(set(outcome_receipts)):
                problems.append(f"{cell_owner}: outcome_receipt_refs contains duplicates")
            if set(commitment_receipts) != set(commitment_record_refs):
                problems.append(
                    f"{cell_owner}: commitment receipt refs must exactly match typed "
                    "commitment provenance records"
                )
            if set(outcome_receipts) != set(outcome_record_refs):
                problems.append(
                    f"{cell_owner}: outcome receipt refs must exactly match typed outcome "
                    "provenance records"
                )
            if cell.get("use_status") != "UNUSED" and not commitment_records:
                problems.append(
                    f"{cell_owner}: use_status {cell.get('use_status')} requires typed "
                    "commitment provenance"
                )
            if cell.get("outcome_status") != "NOT_OBSERVED" and not outcome_records:
                problems.append(
                    f"{cell_owner}: outcome_status {cell.get('outcome_status')} "
                    "requires typed independent outcome provenance"
                )

            commitment_issuers = {
                record.get("issuer_ref")
                for record in commitment_records
                if isinstance(record.get("issuer_ref"), str) and record.get("issuer_ref")
            }
            outcome_issuers = {
                record.get("issuer_ref")
                for record in outcome_records
                if isinstance(record.get("issuer_ref"), str) and record.get("issuer_ref")
            }
            commitment_authorities = {
                record.get("evidence_authority_ref")
                for record in commitment_records
                if isinstance(record.get("evidence_authority_ref"), str)
                and record.get("evidence_authority_ref")
            }
            outcome_authorities = {
                record.get("evidence_authority_ref")
                for record in outcome_records
                if isinstance(record.get("evidence_authority_ref"), str)
                and record.get("evidence_authority_ref")
            }
            if commitment_issuers & outcome_issuers:
                problems.append(
                    f"{cell_owner}: commitment and outcome issuer sets must be disjoint"
                )
            if commitment_authorities & outcome_authorities:
                problems.append(
                    f"{cell_owner}: commitment and outcome evidence-authority sets "
                    "must be disjoint"
                )
            if cell.get("outcome_status") == "REPLICATED":
                dimensions = {
                    "outcome issuers": [record.get("issuer_ref") for record in outcome_records],
                    "outcome evidence authorities": [
                        record.get("evidence_authority_ref") for record in outcome_records
                    ],
                    "outcome observations": [
                        record.get("observation_ref") for record in outcome_records
                    ],
                    "outcome custody chains": [
                        record.get("custody_ref") for record in outcome_records
                    ],
                }
                if len(outcome_records) < 2:
                    problems.append(
                        f"{cell_owner}: REPLICATED requires at least two independent "
                        "outcome provenance records, not two references"
                    )
                for label, values in dimensions.items():
                    string_values = [value for value in values if isinstance(value, str)]
                    if len(string_values) != len(values) or len(values) != len(set(string_values)):
                        problems.append(f"{cell_owner}: REPLICATED requires distinct {label}")

            transitions = cell.get("status_transitions")
            transition_axes = {
                transition.get("axis")
                for transition in transitions
                if isinstance(transition, dict)
            } if isinstance(transitions, list) else set()
            if cell.get("authorization_status") != "NOT_REQUESTED" and (
                "authorization_status" not in transition_axes
            ):
                problems.append(
                    f"{cell_owner}: non-default authorization_status requires an externally "
                    "attested status transition"
                )
            if cell.get("use_status") != "UNUSED" and "use_status" not in transition_axes:
                problems.append(
                    f"{cell_owner}: non-default use_status requires an externally attested "
                    "status transition"
                )
            if cell.get("outcome_status") != "NOT_OBSERVED" and (
                "outcome_status" not in transition_axes
            ):
                problems.append(
                    f"{cell_owner}: non-default outcome_status requires an externally attested "
                    "status transition"
                )

            deps = _dependency_entries(
                cell_owner,
                cell.get("dependency_refs"),
                problems,
                base_dir=base_dir,
                check_source_files=check_source_files,
            )
            cell_dependency_entries[cid] = deps
            cell_dependencies[cid] = [
                entry["ref"]
                for entry in deps
                if entry["kind"] == "CELL" and entry.get("binding_status") == "BOUND"
            ]
            _validate_transitions(cell_owner, cell, evidence_tiers, problems)

        claim_digest = projection.get("claim_semantic_digest")
        expected_claim_digest = _canonical_digest(_projection_claim_payload(projection))
        if isinstance(claim_digest, str) and HEX64_RE.fullmatch(claim_digest):
            if claim_digest != expected_claim_digest:
                problems.append(
                    f"{owner}: claim_semantic_digest does not match bound mapping semantics "
                    f"({claim_digest} != {expected_claim_digest})"
                )

    all_rejected_claim_digests: set[str] = set()
    for pref, projection in projections.items():
        owner = f"projection {pref}"
        rejected = projection.get("rejected_claim_digests")
        if not isinstance(rejected, list):
            continue
        if len(rejected) != len(set(value for value in rejected if isinstance(value, str))):
            problems.append(f"{owner}: rejected_claim_digests contains duplicates")
        for digest in rejected:
            if not isinstance(digest, str) or not HEX64_RE.fullmatch(digest):
                problems.append(
                    f"{owner}: rejected_claim_digests entries must be 64 lowercase hex"
                )
            else:
                all_rejected_claim_digests.add(digest)

    for pref, projection in projections.items():
        owner = f"projection {pref}"
        for entry in projection_dependency_entries.get(pref, []):
            if entry.get("binding_status") == "DEFERRED":
                if projection.get("resolution_status") == "RESOLVED":
                    problems.append(f"{owner}: RESOLVED may not retain a DEFERRED dependency")
                continue
            if entry.get("kind") == "PACK":
                dep = entry.get("ref")
                if dep not in packs:
                    problems.append(f"{owner}: PACK dependency {dep!r} is not retained")
                    continue
                bound_pack = packs[dep]
                if entry.get("owner_ref") != bound_pack.get("owner_ref"):
                    problems.append(f"{owner}: PACK dependency {dep!r} owner_ref does not match")
                if entry.get("version") != bound_pack.get("source_version"):
                    problems.append(
                        f"{owner}: PACK dependency {dep!r} version must equal source_version"
                    )
                if entry.get("digest_canonicalization") != "rs.pack_manifest_digest.v1":
                    problems.append(
                        f"{owner}: PACK dependency {dep!r} must bind "
                        "rs.pack_manifest_digest.v1"
                    )
                if entry.get("digest") != _canonical_digest(
                    _pack_manifest_payload(bound_pack)
                ):
                    problems.append(
                        f"{owner}: PACK dependency {dep!r} digest does not match "
                        "the retained PackManifest"
                    )
                continue
            if entry.get("kind") != "PROJECTION":
                continue
            dep = entry.get("ref")
            if dep not in projections:
                problems.append(f"{owner}: PROJECTION dependency {dep!r} is not retained")
                continue
            bound_projection = projections[dep]
            if entry.get("owner_ref") != bound_projection.get("projection_id"):
                problems.append(
                    f"{owner}: PROJECTION dependency {dep!r} owner_ref does not match"
                )
            if entry.get("version") != dep:
                problems.append(f"{owner}: PROJECTION dependency {dep!r} version must equal ref")
            if entry.get("digest_canonicalization") != "rs.projection_claim_digest.v1":
                problems.append(
                    f"{owner}: PROJECTION dependency {dep!r} must bind "
                    "rs.projection_claim_digest.v1"
                )
            if entry.get("digest") != bound_projection.get("claim_semantic_digest"):
                problems.append(
                    f"{owner}: PROJECTION dependency {dep!r} digest does not match "
                    "the retained claim"
                )

        predecessor = projection.get("supersedes_ref")
        ancestors: list[str] = []
        comparison_by_ref: dict[str, dict[str, Any]] = {}
        if predecessor is None:
            if projection.get("projection_revision") == 1 and projection.get(
                "predecessor_comparisons"
            ) not in ([], None):
                problems.append(f"{owner}: revision 1 predecessor_comparisons must be empty")
        elif predecessor not in projections:
            problems.append(
                f"{owner}: supersedes_ref {predecessor!r} is not retained; "
                "failed revisions are append-only"
            )
        else:
            old = projections[predecessor]
            if projection.get("projection_id") != old.get("projection_id"):
                problems.append(f"{owner}: may supersede only the same projection_id")
            if projection.get("parent_revision") != old.get("projection_revision"):
                problems.append(f"{owner}: parent_revision must match superseded revision")
            if projection.get("projection_revision") != old.get("projection_revision", 0) + 1:
                problems.append(f"{owner}: projection revisions must advance exactly one")

            cursor: str | None = predecessor
            seen: set[str] = set()
            while isinstance(cursor, str) and cursor in projections and cursor not in seen:
                ancestors.append(cursor)
                seen.add(cursor)
                next_cursor = projections[cursor].get("supersedes_ref")
                cursor = next_cursor if isinstance(next_cursor, str) else None
            ancestor_set = set(ancestors)
            comparisons = projection.get("predecessor_comparisons")
            if not isinstance(comparisons, list):
                comparisons = []
            for comparison_index, comparison in enumerate(comparisons):
                prefix = f"{owner}: predecessor_comparisons[{comparison_index}]"
                if not isinstance(comparison, dict):
                    problems.append(f"{prefix} must be an object")
                    continue
                required = {
                    "comparison_schema",
                    "predecessor_ref",
                    "predecessor_claim_digest",
                    "comparison_status",
                    "comparison_reason",
                    "external_verifier_attestation",
                }
                for field in sorted(required - comparison.keys()):
                    problems.append(f"{prefix} missing `{field}`")
                if comparison.get("comparison_schema") != "rs.predecessor_comparison.v1":
                    problems.append(
                        f"{prefix}.comparison_schema must be rs.predecessor_comparison.v1"
                    )
                comparison_ref = comparison.get("predecessor_ref")
                if not isinstance(comparison_ref, str) or comparison_ref not in ancestor_set:
                    problems.append(f"{prefix}: predecessor_ref is not in the ancestral path")
                    continue
                if comparison_ref in comparison_by_ref:
                    problems.append(f"{prefix}: predecessor_ref is duplicated")
                comparison_by_ref[comparison_ref] = comparison
                predecessor_claim = projections[comparison_ref].get("claim_semantic_digest")
                if comparison.get("predecessor_claim_digest") != predecessor_claim:
                    problems.append(f"{prefix}: predecessor_claim_digest does not match")
                comparison_status = comparison.get("comparison_status")
                if comparison_status not in {"ACCEPTED", "REJECTED"}:
                    problems.append(f"{prefix}: comparison_status is invalid")
                if not _present(comparison.get("comparison_reason")):
                    problems.append(f"{prefix}: comparison_reason is empty")
                subject_payload = _predecessor_comparison_subject_payload(
                    projection, comparison
                )
                subject_ref = f"{pref}::{comparison_ref}"
                _check_external_attestation(
                    prefix,
                    comparison.get("external_verifier_attestation"),
                    problems,
                    expected_subject_ref=subject_ref,
                    expected_status_axis="predecessor_comparison",
                    expected_from_status="UNREVIEWED",
                    expected_to_status=(
                        comparison_status if isinstance(comparison_status, str) else None
                    ),
                    expected_digest_canonicalization=(
                        "rs.predecessor_comparison_subject.v1"
                    ),
                    expected_subject_digest=_canonical_digest(subject_payload),
                )
                rejected = projection.get("rejected_claim_digests")
                if comparison_status == "REJECTED" and (
                    not isinstance(rejected, list) or predecessor_claim not in rejected
                ):
                    problems.append(
                        f"{prefix}: REJECTED comparison digest must be retained in "
                        "rejected_claim_digests"
                    )

            missing_comparisons = ancestor_set - comparison_by_ref.keys()
            if missing_comparisons:
                problems.append(
                    f"{owner}: every ancestral predecessor requires a comparison; missing "
                    f"{sorted(missing_comparisons)}"
                )
            inherited_rejections = old.get("rejected_claim_digests")
            current_rejections = projection.get("rejected_claim_digests")
            if isinstance(inherited_rejections, list) and isinstance(current_rejections, list):
                if not set(inherited_rejections).issubset(set(current_rejections)):
                    problems.append(
                        f"{owner}: rejected_claim_digests must be a monotonic superset "
                        "of the predecessor set"
                    )
            if projection.get("resolution_status") == "RESOLVED":
                rejected_comparisons = [
                    ref
                    for ref in ancestors
                    if comparison_by_ref.get(ref, {}).get("comparison_status") != "ACCEPTED"
                ]
                if rejected_comparisons:
                    problems.append(
                        f"{owner}: RESOLVED requires every ancestral predecessor "
                        f"comparison ACCEPTED; not accepted {rejected_comparisons}"
                    )

        _check_resolution_disposition(
            owner,
            projection,
            ancestors,
            comparison_by_ref,
            projections,
            problems,
        )

        claim_digest = projection.get("claim_semantic_digest")
        if (
            projection.get("resolution_status") == "RESOLVED"
            and isinstance(claim_digest, str)
            and claim_digest in all_rejected_claim_digests
        ):
            problems.append(
                f"{owner}: rejected claim digest cannot become RESOLVED by alias, "
                "removal, or re-addition"
            )
    _find_cycles(projection_dependencies, "projection dependency", problems)
    _find_cycles(projection_supersession, "projection supersession", problems)

    for cid, deps in cell_dependencies.items():
        for dep in deps:
            if dep not in cells:
                problems.append(f"cell {cid}: CELL dependency {dep!r} is not retained")
    _find_cycles(cell_dependencies, "cell dependency", problems)
    return problems


def _load_ledger(path: Path) -> tuple[Any | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [f"ledger not found: {path}"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"cannot read ledger {path}: {exc}"]


def _run_negative_controls(
    data: dict[str, Any], base_dir: Path
) -> tuple[list[str], int]:
    failures: list[str] = []
    control_count = 0

    def first_cell(candidate: dict[str, Any]) -> dict[str, Any]:
        return candidate["projections"][0]["cells"][0]

    def expect(name: str, mutate: Callable[[dict[str, Any]], None], marker: str) -> None:
        nonlocal control_count
        control_count += 1
        candidate = copy.deepcopy(data)
        mutate(candidate)
        found = validate(candidate, base_dir=base_dir, check_source_files=True)
        if not any(marker in problem for problem in found):
            failures.append(
                f"negative control {name!r} did not trigger {marker!r}; problems were {found}"
            )

    def external_attestation(
        *,
        subject_ref: str,
        axis: str,
        old: str,
        new: str,
        canonicalization: str,
        subject_digest: str,
    ) -> dict[str, Any]:
        return {
            "schema_version": "rs.external_verifier_attestation.v1",
            "attestation_ref": "negative-control:attestation",
            "verifier_ref": "negative-control:verifier",
            "verifier_authority_ref": "negative-control:external-authority",
            "independence_basis": "separate fixture authority",
            "subject_ref": subject_ref,
            "status_axis": axis,
            "from_status": old,
            "to_status": new,
            "subject_digest_algorithm": "sha256",
            "subject_digest_canonicalization": canonicalization,
            "subject_digest": subject_digest,
            "verification_method_ref": "negative-control:method@1",
            "issued_at": "2026-07-31T00:00:00Z",
            "custody_ref": "negative-control:external-custody",
            "signature_or_attestation_ref": "negative-control:signature",
        }

    expect(
        "pack/projection conflation",
        lambda candidate: candidate["packs"][0].update({"target_pack_refs": ["GEN7@1"]}),
        "projection-only field",
    )
    expect(
        "bare cross-pack row",
        lambda candidate: first_cell(candidate).update({"source_ref": "L1"}),
        "bare or malformed",
    )
    expect(
        "hidden native cardinality",
        lambda candidate: candidate["packs"][0].update({"native_cardinality": 6}),
        "hidden cardinality",
    )
    expect(
        "native definition drift",
        lambda candidate: candidate["packs"][0]["native_term_definitions"][0].update(
            {"description": "mutated without a new pack version"}
        ),
        "native expression digest does not match",
    )
    expect(
        "source pack model substitution",
        lambda candidate: candidate["projections"][0]["source_pack_binding"].update(
            {"pack_manifest_digest": "0" * 64}
        ),
        "source_pack_binding: pack binding `pack_manifest_digest` does not match",
    )
    expect(
        "target pack model substitution",
        lambda candidate: candidate["projections"][0]["target_pack_bindings"][0].update(
            {"pack_manifest_digest": "0" * 64}
        ),
        "target_pack_bindings[0]: pack binding `pack_manifest_digest` does not match",
    )
    expect(
        "availability-string dependency",
        lambda candidate: candidate["projections"][0].update(
            {"dependency_refs": ["AVAILABLE"]}
        ),
        "dependency_refs[0] must be an object",
    )
    expect(
        "legacy total tier order",
        lambda candidate: candidate.update(
            {"tier_order": list(candidate["evidence_tier_vocabulary"])}
        ),
        "tier_order is forbidden",
    )
    expect(
        "authorization without envelope",
        lambda candidate: first_cell(candidate).update(
            {"authorization_status": "AUTHORIZED", "authorization_envelope_ref": None}
        ),
        "requires a complete AuthorizationEnvelope reference",
    )

    def transition_without_attestation(candidate: dict[str, Any]) -> None:
        cell = first_cell(candidate)
        cell["mapping_tier"] = "S"
        cell["status_transitions"] = [
            {
                "axis": "mapping_tier",
                "from": "I",
                "to": "S",
                "recorded_at": "2026-07-31T00:00:00Z",
                "reason": "negative control",
                "receipt_refs": ["negative-control:receipt"],
                "external_verifier_attestation": None,
            }
        ]

    expect(
        "status transition without external attestation",
        transition_without_attestation,
        "typed external verifier attestation is required",
    )

    def formerly_downward_tier_change_without_receipt(candidate: dict[str, Any]) -> None:
        """A kind change cannot escape receipts by pointing down an invented rank."""
        cell = first_cell(candidate)
        cell["mapping_tier"] = "C"
        transition = {
            "axis": "mapping_tier",
            "from": "I",
            "to": "C",
            "recorded_at": "2026-07-31T00:00:00Z",
            "reason": "negative control for non-ordered evidence kinds",
            "receipt_refs": [],
        }
        transition["external_verifier_attestation"] = external_attestation(
            subject_ref=cell["cell_id"],
            axis="mapping_tier",
            old="I",
            new="C",
            canonicalization="rs.status_transition_subject.v1",
            subject_digest=_canonical_digest(
                _status_transition_subject_payload(cell, transition)
            ),
        )
        cell["status_transitions"] = [transition]

    expect(
        "formerly downward tier change without receipt",
        formerly_downward_tier_change_without_receipt,
        "evidence-kind change I -> C requires a receipt",
    )

    def replayed_attestation(candidate: dict[str, Any]) -> None:
        cell = first_cell(candidate)
        cell["mapping_tier"] = "S"
        transition = {
            "axis": "mapping_tier",
            "from": "I",
            "to": "S",
            "recorded_at": "2026-07-31T00:00:00Z",
            "reason": "negative control",
            "receipt_refs": ["negative-control:receipt"],
        }
        transition["external_verifier_attestation"] = external_attestation(
            subject_ref=cell["cell_id"],
            axis="mapping_tier",
            old="I",
            new="S",
            canonicalization="rs.status_transition_subject.v1",
            subject_digest="0" * 64,
        )
        cell["status_transitions"] = [transition]

    expect(
        "detached verifier attestation",
        replayed_attestation,
        "verifier `subject_digest` does not bind",
    )
    expect(
        "outcome refs without provenance",
        lambda candidate: first_cell(candidate).update(
            {"outcome_status": "OBSERVED", "outcome_receipt_refs": ["outcome:1"]}
        ),
        "requires typed independent outcome provenance",
    )

    def aliased_replication(candidate: dict[str, Any]) -> None:
        cell = first_cell(candidate)
        cell["outcome_status"] = "REPLICATED"
        cell["outcome_receipt_refs"] = ["outcome:1", "outcome:2"]
        cell["outcome_provenance_records"] = [
            {
                "schema_version": "rs.outcome_provenance.v1",
                "receipt_ref": f"outcome:{index}",
                "issuer_ref": "same:issuer",
                "evidence_authority_ref": "same:authority",
                "custody_ref": "same:custody",
                "observation_ref": f"observation:{index}",
                "observation_digest": str(index) * 64,
                "method_ref": "method@1",
                "independence_basis": "claimed only",
                "signature_or_attestation_ref": f"signature:{index}",
            }
            for index in (1, 2)
        ]

    expect(
        "replication by aliased references",
        aliased_replication,
        "REPLICATED requires distinct outcome issuers",
    )

    def overlap_receipt_authority(candidate: dict[str, Any]) -> None:
        cell = first_cell(candidate)
        cell["use_status"] = "PROPOSED"
        cell["outcome_status"] = "OBSERVED"
        cell["commitment_receipt_refs"] = ["commitment:1"]
        cell["outcome_receipt_refs"] = ["outcome:1"]
        cell["commitment_provenance_records"] = [
            {
                "schema_version": "rs.commitment_provenance.v1",
                "receipt_ref": "commitment:1",
                "issuer_ref": "same:issuer",
                "evidence_authority_ref": "same:authority",
                "custody_ref": "commitment:custody",
                "record_digest": "1" * 64,
                "signature_or_attestation_ref": "commitment:signature",
            }
        ]
        cell["outcome_provenance_records"] = [
            {
                "schema_version": "rs.outcome_provenance.v1",
                "receipt_ref": "outcome:1",
                "issuer_ref": "same:issuer",
                "evidence_authority_ref": "same:authority",
                "custody_ref": "outcome:custody",
                "observation_ref": "observation:1",
                "observation_digest": "2" * 64,
                "method_ref": "method@1",
                "independence_basis": "not independent",
                "signature_or_attestation_ref": "outcome:signature",
            }
        ]

    expect(
        "commitment/outcome authority overlap",
        overlap_receipt_authority,
        "commitment and outcome issuer sets must be disjoint",
    )

    def projection_dependency(dep: dict[str, Any]) -> dict[str, Any]:
        return {
            "binding_schema": "rs.dependency_binding.v1",
            "kind": "PROJECTION",
            "ref": dep["projection_ref"],
            "binding_status": "BOUND",
            "owner_ref": dep["projection_id"],
            "version": dep["projection_ref"],
            "digest_algorithm": "sha256",
            "digest_canonicalization": "rs.projection_claim_digest.v1",
            "digest": dep["claim_semantic_digest"],
            "deferred_reason": None,
        }

    def make_projection_cycle(candidate: dict[str, Any]) -> None:
        left, right = candidate["projections"][:2]
        left["dependency_refs"].append(projection_dependency(right))
        right["dependency_refs"].append(projection_dependency(left))

    expect("projection dependency cycle", make_projection_cycle, "projection dependency cycle")
    expect(
        "exact source drift",
        lambda candidate: candidate["packs"][0].update({"source_exact_digest": "0" * 64}),
        "exact source drift",
    )

    def erase_projection_predecessor(candidate: dict[str, Any]) -> None:
        projection = candidate["projections"][0]
        old_ref = projection["projection_ref"]
        projection["projection_revision"] = 2
        projection["projection_ref"] = "PHIL7_TO_GEN7@2"
        projection["parent_revision"] = 1
        projection["supersedes_ref"] = old_ref
        for cell in projection["cells"]:
            cell["projection_ref"] = projection["projection_ref"]
            cell["cell_id"] = cell["cell_id"].replace(
                old_ref + ":", projection["projection_ref"] + ":"
            )

    expect(
        "dangling projection supersession",
        erase_projection_predecessor,
        "failed revisions are append-only",
    )

    def deterministic_regime_label(candidate: dict[str, Any]) -> None:
        candidate["regime_records"] = [
            {
                "schema_ref": "RS.REGIME@1",
                "surface_ref": "negative-control:surface",
                "observation_window": {"start": "t0", "end": "t1"},
                "controller_refs": ["controller:1"],
                "controller_plurality": {"count": 1, "inclusion_rule": "effective control"},
                "concentration_measure": {
                    "metric": "share",
                    "denominator": "surface",
                    "value": 1,
                    "uncertainty": "fixture",
                },
                "alias_coalitions": [],
                "contestability": {"path": "none"},
                "revocability": {"path": "none"},
                "dependency_refs": [],
                "receipt_independence": {"status": "unknown"},
                "observed_consequences": [],
                "longitudinal_capture_signatures": [],
                "political_label": "tyranny",
            }
        ]

    expect(
        "deterministic political regime label",
        deterministic_regime_label,
        "political_label must be null",
    )

    expect(
        "caller-declared RESOLVED without disposition",
        lambda candidate: candidate["projections"][0].update(
            {"resolution_status": "RESOLVED"}
        ),
        "RESOLVED requires a complete resolution disposition",
    )

    def deferred_dependency_resolved(candidate: dict[str, Any]) -> None:
        projection = candidate["projections"][0]
        projection["resolution_status"] = "RESOLVED"
        projection["dependency_refs"].append(
            {
                "binding_schema": "rs.dependency_binding.v1",
                "kind": "INTERPRETER",
                "ref": "interpreter:unavailable",
                "binding_status": "DEFERRED",
                "owner_ref": None,
                "version": None,
                "digest_algorithm": None,
                "digest_canonicalization": None,
                "digest": None,
                "deferred_reason": "custody unavailable",
            }
        )

    expect(
        "resolved projection with deferred dependency",
        deferred_dependency_resolved,
        "RESOLVED may not retain a DEFERRED dependency",
    )

    def rejected_remove_readd(candidate: dict[str, Any]) -> None:
        old = candidate["projections"][0]
        child = copy.deepcopy(old)
        old_ref = old["projection_ref"]
        child_ref = "PHIL7_TO_GEN7@2"
        child["projection_revision"] = 2
        child["projection_ref"] = child_ref
        child["parent_revision"] = 1
        child["supersedes_ref"] = old_ref
        child["resolution_status"] = "RESOLVED"
        child["rejected_claim_digests"] = [old["claim_semantic_digest"]]
        for cell in child["cells"]:
            cell["projection_ref"] = child_ref
            cell["cell_id"] = cell["cell_id"].replace(old_ref + ":", child_ref + ":")
        comparison = {
            "comparison_schema": "rs.predecessor_comparison.v1",
            "predecessor_ref": old_ref,
            "predecessor_claim_digest": old["claim_semantic_digest"],
            "comparison_status": "ACCEPTED",
            "comparison_reason": "negative-control re-add",
        }
        subject_payload = _predecessor_comparison_subject_payload(child, comparison)
        comparison["external_verifier_attestation"] = external_attestation(
            subject_ref=f"{child_ref}::{old_ref}",
            axis="predecessor_comparison",
            old="UNREVIEWED",
            new="ACCEPTED",
            canonicalization="rs.predecessor_comparison_subject.v1",
            subject_digest=_canonical_digest(subject_payload),
        )
        child["predecessor_comparisons"] = [comparison]
        candidate["projections"].append(child)

    expect(
        "rejected claim remove/re-add",
        rejected_remove_readd,
        "rejected claim digest cannot become RESOLVED",
    )
    return failures, control_count


def _print_problems(title: str, problems: list[str]) -> None:
    print(f"\n{title}: FAIL — {len(problems)} problem(s)\n")
    for problem in problems:
        print(f"  - {problem}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--self-test", action="store_true", help="run fail-closed negative controls")
    args = parser.parse_args()
    ledger_path = args.ledger.resolve()
    data, load_problems = _load_ledger(ledger_path)
    if load_problems:
        _print_problems("rosetta cell ledger", load_problems)
        return 1
    assert data is not None
    problems = validate(data, base_dir=ledger_path.parent, check_source_files=True)
    if problems:
        _print_problems("rosetta cell ledger", problems)
        return 1
    cell_count = sum(len(projection["cells"]) for projection in data["projections"])
    print(
        "rosetta cell ledger: PASS "
        f"({len(data['packs'])} native packs, {len(data['projections'])} directional projections, "
        f"{cell_count} cells, exact source digests current)"
    )
    if args.self_test:
        failures, control_count = _run_negative_controls(data, ledger_path.parent)
        if failures:
            _print_problems("rosetta cell ledger self-test", failures)
            return 1
        print(
            "rosetta cell ledger self-test: PASS "
            f"({control_count} fail-closed negative controls)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
