from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from .codec import canonical_json_bytes, raw_hash
from .diagnostics import Issue, KintsugiError
from .gitstate import _read_regular_no_symlinks
from .manifest import (
    _review_subject_projection,
    _selected_manifest_receipt,
    _semantic_record_closure,
)
from .markdown import (
    extract_fenced_json,
    project_review_seam,
    synchronize_ledger_markdown,
    synchronize_receipt_markdown,
    synchronize_review_markdown,
)
from .schema import validate_named_definition
from .semantics import validate_core_records


_SCHEMA_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
_LEDGER_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
_REVIEW_FIELDS = frozenset({
    "id",
    "kind",
    "path",
    "receiptId",
    "reviewerId",
    "reviewerRole",
    "independenceStatement",
    "reviewTargetDigest",
    "verdict",
    "findingIds",
    "openSevereFindingIds",
    "approvedUpgradeSeamIds",
    "approvedGateSeamIds",
    "attemptId",
})
_FINDING_FIELDS = frozenset({
    "id",
    "attemptId",
    "reviewKind",
    "category",
    "severity",
    "statement",
    "claimIds",
    "seamIds",
    "ledgerSectionIds",
    "receiptIds",
    "subjectPaths",
})
_REVIEW_TARGET_FIELDS = frozenset({
    "schemaVersion",
    "phase",
    "manifest",
    "sources",
    "claims",
    "trials",
    "seams",
    "propagations",
    "antibodies",
    "discriminators",
    "fixtures",
    "schemaSha256",
    "ledgerSemanticSections",
    "semanticDiffPaths",
    "priorReviewAttempts",
    "priorReviewAttemptArtifacts",
    "currentAttemptId",
    "receiptId",
    "reviewSubjectDigest",
    "priorReviewAttestations",
    "priorReviewFindings",
    "priorReviewFindingDispositions",
    "receiptNarrativeRawSha256",
    "ledgerPreambleRawSha256",
})
_VALIDATION_BUNDLE_FIELDS = frozenset({
    "schemaVersion",
    "phase",
    "receiptDescriptor",
    "reviewTargetDigest",
    "manifest",
    "sources",
    "claims",
    "trials",
    "seams",
    "propagations",
    "antibodies",
    "discriminators",
    "fixtures",
    "schemaSha256",
    "ledgerSections",
    "logicReviewSha256",
    "btjReviewSha256",
    "publicQueueSha256",
    "dependencyReceipts",
    "reviewAttempts",
    "reviewAttemptArtifacts",
    "reviewAttestations",
    "reviewFindings",
    "reviewFindingDispositions",
    "receiptNarrativeRawSha256",
    "ledgerPreambleRawSha256",
})
_ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]*$")
_PATH_RE = re.compile(
    r"^(?!/)(?!.*(?:^|/)\.{1,2}(?:/|$))(?!.*//)(?!.*\\)[^/]+(?:/[^/]+)*$"
)
_RAW_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_STRENGTH_ORDER = {"C": 0, "I": 1, "S": 2, "A": 3}


def _issue(path: str, code: str, message: str) -> Issue:
    return Issue(path, code, message)


def _raise(path: str, code: str, message: str) -> None:
    raise KintsugiError(code, path, message)


def _mapping(value: object, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _raise(path, "KIN-E-STATE", "expected an object")
    return value


def _valid_id(value: object) -> bool:
    return isinstance(value, str) and bool(_ID_RE.fullmatch(value))


def _valid_path(value: object) -> bool:
    return isinstance(value, str) and bool(_PATH_RE.fullmatch(value))


def _valid_raw_hash(value: object) -> bool:
    return isinstance(value, str) and bool(_RAW_HASH_RE.fullmatch(value))


def _valid_unique_strings(
    value: object, *, predicate: object = _valid_id
) -> bool:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return False
    checker = predicate if callable(predicate) else _valid_id
    return len(value) == len(set(value)) and all(checker(item) for item in value)


def _review_shape_issues(value: object, path: str) -> list[Issue]:
    if not isinstance(value, dict) or set(value) != _REVIEW_FIELDS:
        return [_issue(path, "KIN-E-STATE", "review attestation shape is not exact")]
    issues: list[Issue] = []
    scalar_checks = (
        ("id", _valid_id),
        ("kind", lambda item: item in {"LOGIC", "BTJ"}),
        ("path", _valid_path),
        ("receiptId", _valid_id),
        ("reviewerId", lambda item: isinstance(item, str) and bool(item)),
        ("reviewerRole", lambda item: isinstance(item, str) and bool(item)),
        ("independenceStatement", lambda item: isinstance(item, str) and bool(item)),
        ("reviewTargetDigest", _valid_raw_hash),
        ("verdict", lambda item: item in {"PASS", "FAIL"}),
        ("attemptId", _valid_id),
    )
    for field, checker in scalar_checks:
        if not checker(value.get(field)):
            issues.append(_issue(f"{path}.{field}", "KIN-E-STATE", "review field has invalid type or value"))
    for field in (
        "findingIds",
        "openSevereFindingIds",
        "approvedUpgradeSeamIds",
        "approvedGateSeamIds",
    ):
        if not _valid_unique_strings(value.get(field)):
            issues.append(_issue(f"{path}.{field}", "KIN-E-STATE", "review ID list is malformed or duplicated"))
    return issues


def _finding_shape_issues(value: object, path: str) -> list[Issue]:
    if not isinstance(value, dict) or set(value) != _FINDING_FIELDS:
        return [_issue(path, "KIN-E-STATE", "review finding shape is not exact")]
    issues: list[Issue] = []
    scalar_checks = (
        ("id", _valid_id),
        ("attemptId", _valid_id),
        ("reviewKind", lambda item: item in {"LOGIC", "BTJ"}),
        (
            "category",
            lambda item: item
            in {"LOGIC", "EVIDENCE", "BEAUTY", "JUSTICE", "PROVENANCE", "SCOPE", "PROCESS"},
        ),
        ("severity", lambda item: item in {"CRITICAL", "MAJOR", "MINOR"}),
        ("statement", lambda item: isinstance(item, str) and bool(item)),
    )
    for field, checker in scalar_checks:
        if not checker(value.get(field)):
            issues.append(_issue(f"{path}.{field}", "KIN-E-STATE", "finding field has invalid type or value"))
    for field in ("claimIds", "seamIds", "ledgerSectionIds", "receiptIds"):
        if not _valid_unique_strings(value.get(field)):
            issues.append(_issue(f"{path}.{field}", "KIN-E-STATE", "finding ID list is malformed or duplicated"))
    if not _valid_unique_strings(value.get("subjectPaths"), predicate=_valid_path):
        issues.append(_issue(f"{path}.subjectPaths", "KIN-E-STATE", "finding path list is malformed or duplicated"))
    return issues


def _records(core: Mapping[str, object], field: str) -> list[dict[str, Any]]:
    value = core.get(field)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        _raise(f"core.{field}", "KIN-E-STATE", "expected an object array")
    return value


def _one_by(
    values: Sequence[dict[str, Any]], field: str, expected: object, path: str
) -> dict[str, Any]:
    matches = [value for value in values if value.get(field) == expected]
    if len(matches) != 1:
        _raise(path, "KIN-E-REF", "reference must resolve exactly once")
    return matches[0]


def _decode_canonical(payload: bytes, path: str) -> object:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError):
        _raise(path, "KIN-E-JSON", "input is not bounded canonical JSON")
    if payload != canonical_json_bytes(value):
        _raise(path, "KIN-E-CANONICAL", "JSON bytes are not canonical")
    return value


def _schema_or_raise(
    schema: dict[str, object], definition: str, value: object, code: str
) -> None:
    issues = validate_named_definition(schema, definition, value)
    if issues:
        first = sorted(issues)[0]
        _raise(first.path, code, first.message)


def _selected_attempt(
    core: Mapping[str, object], phase: str, attempt_id: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest, receipt = _selected_manifest_receipt(dict(core), phase)
    attempt = _one_by(
        _records(core, "reviewAttempts"), "id", attempt_id, "core.reviewAttempts"
    )
    if (
        attempt.get("phase") != phase
        or attempt.get("receiptId") != receipt.get("id")
        or receipt.get("reviewAttemptId") != attempt_id
    ):
        _raise("reviewAttempt", "KIN-E-REF", "attempt is not the current phase receipt leaf")
    artifact = _one_by(
        _records(core, "reviewAttemptArtifacts"),
        "attemptId",
        attempt_id,
        "core.reviewAttemptArtifacts",
    )
    return manifest, receipt, attempt, artifact


def project_terminal_review_history(
    core: dict[str, object], phase: str, attempt_id: str
) -> dict[str, list[dict[str, Any]]]:
    _, receipt, current, _ = _selected_attempt(core, phase, attempt_id)
    attempts = [
        value
        for value in _records(core, "reviewAttempts")
        if value.get("phase") == phase and value.get("receiptId") == receipt.get("id")
    ]
    by_id = {value.get("id"): value for value in attempts}
    if len(by_id) != len(attempts):
        _raise("core.reviewAttempts", "KIN-E-REF", "review attempt IDs are duplicated")
    lineage: list[dict[str, Any]] = []
    seen: set[str] = set()
    cursor = current
    while cursor.get("supersedesAttemptId") is not None:
        parent_id = cursor.get("supersedesAttemptId")
        if not isinstance(parent_id, str) or parent_id in seen or parent_id not in by_id:
            _raise("core.reviewAttempts", "KIN-E-CYCLE", "review history is disconnected or cyclic")
        seen.add(parent_id)
        parent = by_id[parent_id]
        if parent.get("status") not in {"FAILED", "ABANDONED"}:
            _raise("core.reviewAttempts", "KIN-E-STATE", "prior review attempt is not terminal")
        lineage.append(parent)
        cursor = parent
    lineage.reverse()
    expected = lineage + [current]
    if attempts != expected:
        _raise("core.reviewAttempts", "KIN-E-REF", "review history is not complete root-to-leaf")
    prior_ids = {value["id"] for value in lineage}
    artifacts = [
        value
        for value in _records(core, "reviewAttemptArtifacts")
        if value.get("attemptId") in prior_ids
    ]
    if [value.get("attemptId") for value in artifacts] != [value.get("id") for value in lineage]:
        _raise("core.reviewAttemptArtifacts", "KIN-E-REF", "prior artifact history is incomplete or reordered")
    chain = lineage + [current]
    ranks = {value["id"]: position for position, value in enumerate(chain)}

    def ordered(
        field: str, key: str, *, include_current: bool = False
    ) -> list[dict[str, Any]]:
        values = [
            value
            for value in _records(core, field)
            if value.get(key) in ranks
        ]
        observed = [ranks[value[key]] for value in values]
        if observed != sorted(observed):
            _raise(f"core.{field}", "KIN-E-REF", "review history is not grouped root-to-leaf")
        permitted = prior_ids | ({attempt_id} if include_current else set())
        return [value for value in values if value.get(key) in permitted]

    prior_attestations = ordered("reviewAttestations", "attemptId")
    prior_findings = ordered("reviewFindings", "attemptId")
    prior_dispositions = ordered(
        "reviewFindingDispositions", "successorAttemptId", include_current=True
    )
    return {
        "attempts": copy.deepcopy(lineage),
        "artifacts": copy.deepcopy(artifacts),
        "attestations": copy.deepcopy(prior_attestations),
        "findings": copy.deepcopy(prior_findings),
        "dispositions": copy.deepcopy(prior_dispositions),
    }


def compute_review_subject_digest(target: dict[str, object]) -> str:
    return raw_hash(canonical_json_bytes(_review_subject_projection(target)))


def build_review_target_from_control_bytes(
    schema: dict[str, object],
    core: dict[str, object],
    *,
    phase: str,
    attempt_id: str,
    ledger_sections: list[dict[str, object]],
    semantic_diff_paths: list[str],
    schema_bytes: bytes,
    ledger_bytes: bytes,
    receipt_bytes: bytes,
    enforce_subject_digest: bool = True,
) -> dict[str, object]:
    if schema_bytes != canonical_json_bytes(schema):
        _raise(_SCHEMA_PATH, "KIN-E-BUNDLE", "schema bytes do not match the supplied schema")
    history_issues = validate_review_history(core)
    if history_issues:
        first = history_issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    manifest, receipt, attempt, _ = _selected_attempt(core, phase, attempt_id)
    history = project_terminal_review_history(core, phase, attempt_id)
    closure = _semantic_record_closure(core, manifest, receipt)

    receipt_sync = synchronize_receipt_markdown(
        receipt_bytes,
        receipt,
        path=str(receipt.get("path")),
        target_frozen=True,
    )
    if receipt_sync.issues:
        first = receipt_sync.issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    all_seams = _records(core, "seams")
    ledger_sync = synchronize_ledger_markdown(
        ledger_bytes, all_seams, path=_LEDGER_PATH
    )
    if ledger_sync.issues:
        first = ledger_sync.issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    computed_sections = [
        {
            "id": section.id,
            "narrativeRawSha256": section.narrative_raw_sha256,
            "seamProjection": copy.deepcopy(section.seam_projection),
        }
        for section in ledger_sync.sections
    ]
    if ledger_sections != computed_sections:
        _raise("ledgerSemanticSections", "KIN-E-BUNDLE", "declared ledger sections drifted")
    seam_ids = set(closure["seamIds"])
    target_manifest = copy.deepcopy(manifest)
    closure_paths = target_manifest.get("closureOnlyPaths")
    if isinstance(closure_paths, list):
        target_manifest["closureOnlyPaths"] = sorted(closure_paths)
    target: dict[str, object] = {
        "schemaVersion": core.get("schemaVersion"),
        "phase": phase,
        "currentAttemptId": attempt_id,
        "receiptId": receipt.get("id"),
        "receiptNarrativeRawSha256": receipt_sync.narrative_raw_sha256,
        "reviewSubjectDigest": None,
        "manifest": target_manifest,
        "sources": copy.deepcopy(closure["sources"]),
        "claims": copy.deepcopy(closure["claims"]),
        "trials": copy.deepcopy(closure["trials"]),
        "seams": [project_review_seam(value) for value in closure["seams"]],
        "propagations": copy.deepcopy(closure["propagations"]),
        "antibodies": copy.deepcopy(closure["antibodies"]),
        "discriminators": copy.deepcopy(closure["discriminators"]),
        "fixtures": copy.deepcopy(closure["fixtures"]),
        "schemaSha256": raw_hash(schema_bytes),
        "ledgerPreambleRawSha256": ledger_sync.preamble.raw_sha256,
        "ledgerSemanticSections": [
            copy.deepcopy(value) for value in computed_sections if value["id"] in seam_ids
        ],
        "semanticDiffPaths": copy.deepcopy(semantic_diff_paths),
        "priorReviewAttempts": history["attempts"],
        "priorReviewAttemptArtifacts": history["artifacts"],
        "priorReviewAttestations": history["attestations"],
        "priorReviewFindings": history["findings"],
        "priorReviewFindingDispositions": history["dispositions"],
    }
    digest = compute_review_subject_digest(target)
    target["reviewSubjectDigest"] = digest
    if enforce_subject_digest and attempt.get("reviewSubjectDigest") != digest:
        _raise("reviewSubjectDigest", "KIN-E-BUNDLE", "attempt subject digest drifted")
    _schema_or_raise(schema, "reviewTarget", target, "KIN-E-BUNDLE")
    return target


def build_review_target_value(
    root: Path,
    schema: dict[str, object],
    core: dict[str, object],
    *,
    phase: str,
    attempt_id: str,
    ledger_sections: list[dict[str, object]],
    semantic_diff_paths: list[str],
) -> dict[str, object]:
    _, receipt, _, _ = _selected_attempt(core, phase, attempt_id)
    schema_bytes = _read_regular_no_symlinks(
        root, _SCHEMA_PATH, code="KIN-E-BUNDLE", require_single_link=True
    )
    ledger_bytes = _read_regular_no_symlinks(
        root, _LEDGER_PATH, code="KIN-E-BUNDLE", require_single_link=True
    )
    receipt_path = str(receipt.get("path"))
    receipt_bytes = _read_regular_no_symlinks(
        root, receipt_path, code="KIN-E-BUNDLE", require_single_link=True
    )
    return build_review_target_from_control_bytes(
        schema,
        core,
        phase=phase,
        attempt_id=attempt_id,
        ledger_sections=ledger_sections,
        semantic_diff_paths=semantic_diff_paths,
        schema_bytes=schema_bytes,
        ledger_bytes=ledger_bytes,
        receipt_bytes=receipt_bytes,
    )


def validate_review_history(core: dict[str, object]) -> list[Issue]:
    issues = list(validate_core_records(core))
    for position, value in enumerate(core.get("reviewAttestations", [])):
        issues.extend(_review_shape_issues(value, f"core.reviewAttestations[{position}]"))
    for position, value in enumerate(core.get("reviewFindings", [])):
        issues.extend(_finding_shape_issues(value, f"core.reviewFindings[{position}]"))
    try:
        for receipt in _records(core, "phaseReceipts"):
            attempt_id = receipt.get("reviewAttemptId")
            phase = receipt.get("phase")
            if isinstance(attempt_id, str) and isinstance(phase, str):
                project_terminal_review_history(core, phase, attempt_id)
        for attempt in _records(core, "reviewAttempts"):
            attempt_id = attempt.get("id")
            if not isinstance(attempt_id, str):
                continue
            reviews, findings = _current_reviews(core, attempt_id)
            issues.extend(validate_review_attestations(core, reviews, findings))
    except KintsugiError as exc:
        issues.append(_issue(exc.path, exc.code, exc.message))
    return sorted(set(issues))


def validate_review_attestations(
    core: dict[str, object],
    reviews: list[dict[str, object]],
    findings: list[dict[str, object]],
) -> list[Issue]:
    issues: list[Issue] = []
    attempts = {value.get("id"): value for value in _records(core, "reviewAttempts")}
    artifacts = {
        value.get("attemptId"): value
        for value in _records(core, "reviewAttemptArtifacts")
    }
    claims = {value.get("id") for value in _records(core, "claims")}
    seams_by_id = {
        value.get("id"): value for value in _records(core, "seams")
    }
    receipts_by_id = {
        value.get("id"): value for value in _records(core, "phaseReceipts")
    }
    subject_paths = {_SCHEMA_PATH, _LEDGER_PATH}
    for source in _records(core, "sources"):
        if isinstance(source.get("path"), str):
            subject_paths.add(source["path"])
    for manifest in _records(core, "manifests"):
        for field in ("candidateFiles", "includedFiles", "finalFiles"):
            values = manifest.get(field)
            if isinstance(values, list):
                subject_paths.update(
                    value["path"]
                    for value in values
                    if isinstance(value, dict) and isinstance(value.get("path"), str)
                )
    subject_paths.update(
        value["path"]
        for value in receipts_by_id.values()
        if isinstance(value.get("path"), str)
    )
    finding_index: dict[object, dict[str, object]] = {}
    for position, value in enumerate(findings):
        path = f"reviewFindings[{position}]"
        shape_issues = _finding_shape_issues(value, path)
        issues.extend(shape_issues)
        if shape_issues or not isinstance(value, dict):
            continue
        finding_id = value.get("id")
        if finding_id in finding_index:
            issues.append(_issue(path, "KIN-E-REF", "review finding ID is duplicated"))
        finding_index[finding_id] = value
        endpoint_checks = (
            ("claimIds", claims),
            ("seamIds", set(seams_by_id)),
            ("ledgerSectionIds", set(seams_by_id) | {"LEDGER-PREAMBLE"}),
            ("receiptIds", set(receipts_by_id)),
            ("subjectPaths", subject_paths),
        )
        for field, allowed in endpoint_checks:
            if any(item not in allowed for item in value[field]):
                issues.append(_issue(f"{path}.{field}", "KIN-E-REF", "finding endpoint does not resolve"))

    kinds: dict[object, dict[str, object]] = {}
    reviewer_ids: list[object] = []
    target_digests: list[object] = []
    finding_counts: dict[object, int] = {}
    for position, review in enumerate(reviews):
        path = f"reviewAttestations[{position}]"
        shape_issues = _review_shape_issues(review, path)
        issues.extend(shape_issues)
        if shape_issues or not isinstance(review, dict):
            continue
        kind = review.get("kind")
        if kind not in {"LOGIC", "BTJ"} or kind in kinds:
            issues.append(_issue(path, "KIN-E-STATE", "review kind must be unique LOGIC or BTJ"))
            continue
        kinds[kind] = review
        reviewer_ids.append(review.get("reviewerId"))
        target_digests.append(review.get("reviewTargetDigest"))
        attempt = attempts.get(review.get("attemptId"))
        if attempt is None:
            issues.append(_issue(path, "KIN-E-REF", "review attempt does not resolve"))
            continue
        artifact = artifacts.get(attempt.get("id"), {})
        ordinal = str(attempt.get("id", "")).rsplit("-", 1)[-1]
        expected_id = f"ATT-{kind}-{attempt.get('phase')}-{ordinal}"
        expected_path = attempt.get(
            "logicReviewPath" if kind == "LOGIC" else "btjReviewPath"
        )
        if (
            review.get("id") != expected_id
            or review.get("path") != expected_path
            or review.get("receiptId") != attempt.get("receiptId")
            or review.get("reviewTargetDigest") != artifact.get("reviewTargetSha256")
        ):
            issues.append(_issue(path, "KIN-E-REF", "review identity/path/target binding drifted"))
        if kind == "LOGIC" and review.get("approvedGateSeamIds"):
            issues.append(_issue(path, "KIN-E-STATE", "LOGIC cannot own Beauty/Justice gate approval"))
        if kind == "BTJ" and review.get("approvedUpgradeSeamIds"):
            issues.append(_issue(path, "KIN-E-STATE", "BTJ cannot own Truth/evidence upgrades"))

        receipt = receipts_by_id.get(attempt.get("receiptId"))
        receipt_seam_ids = (
            sorted(receipt.get("seamIds", []))
            if isinstance(receipt, dict) and isinstance(receipt.get("seamIds"), list)
            else []
        )
        upgrade_ids = sorted(
            seam_id
            for seam_id in receipt_seam_ids
            if isinstance((seam := seams_by_id.get(seam_id)), dict)
            and isinstance(seam.get("evidenceBefore"), dict)
            and isinstance(seam.get("evidenceAfter"), dict)
            and _STRENGTH_ORDER.get(seam["evidenceAfter"].get("strength"), -1)
            > _STRENGTH_ORDER.get(seam["evidenceBefore"].get("strength"), -1)
        )

        named: list[dict[str, object]] = []
        ids = review.get("findingIds")
        if (
            not isinstance(ids, list)
            or len(ids) != len(set(ids))
            or ids != sorted(ids)
        ):
            issues.append(_issue(path, "KIN-E-REF", "review finding IDs are malformed or duplicated"))
            ids = []
        for finding_id in ids:
            finding_counts[finding_id] = finding_counts.get(finding_id, 0) + 1
            finding = finding_index.get(finding_id)
            if (
                finding is None
                or finding.get("attemptId") != attempt.get("id")
                or finding.get("reviewKind") != kind
            ):
                issues.append(_issue(path, "KIN-E-REF", "review finding does not resolve in its attempt/kind"))
            else:
                named.append(finding)
                category = finding.get("category")
                allowed = (
                    {"LOGIC", "EVIDENCE", "PROVENANCE", "SCOPE", "PROCESS"}
                    if kind == "LOGIC"
                    else {"BEAUTY", "JUSTICE", "PROVENANCE", "SCOPE", "PROCESS"}
                )
                if category not in allowed:
                    issues.append(_issue(path, "KIN-E-STATE", "review finding crosses reviewer ownership"))
        ordered_finding_ids = [
            value.get("id")
            for value in findings
            if value.get("attemptId") == attempt.get("id")
            and value.get("reviewKind") == kind
        ]
        if ids != ordered_finding_ids:
            issues.append(_issue(path, "KIN-E-REF", "review findings are omitted or reordered"))
        severe = sorted(
            value.get("id")
            for value in named
            if value.get("severity") in {"CRITICAL", "MAJOR"}
        )
        open_severe = review.get("openSevereFindingIds")
        verdict = review.get("verdict")
        if verdict == "FAIL":
            if not named or not severe or open_severe != severe:
                issues.append(_issue(path, "KIN-E-STATE", "FAIL must expose its exact non-empty severe set"))
        elif verdict == "PASS":
            if open_severe != [] or any(value.get("severity") != "MINOR" for value in named):
                issues.append(_issue(path, "KIN-E-STATE", "PASS permits only MINOR findings and no open severe set"))
            if kind == "LOGIC" and review.get("approvedUpgradeSeamIds") != upgrade_ids:
                issues.append(_issue(path, "KIN-E-STATE", "LOGIC approval must equal the exact upgraded seam set"))
            if kind == "BTJ" and review.get("approvedGateSeamIds") != receipt_seam_ids:
                issues.append(_issue(path, "KIN-E-STATE", "BTJ approval must equal the exact terminal-gate seam set"))
        else:
            issues.append(_issue(path, "KIN-E-STATE", "review verdict is invalid"))
        if verdict == "FAIL" and (
            review.get("approvedUpgradeSeamIds") != []
            or review.get("approvedGateSeamIds") != []
        ):
            issues.append(_issue(path, "KIN-E-STATE", "FAIL cannot approve a gate or evidence upgrade"))

    if len(reviewer_ids) == 2 and len(set(reviewer_ids)) != 2:
        issues.append(_issue("reviewAttestations", "KIN-E-STATE", "LOGIC and BTJ reviewers must be independent identities"))
    if len(target_digests) > 1 and len(set(target_digests)) != 1:
        issues.append(_issue("reviewAttestations", "KIN-E-REF", "reviews do not bind one immutable target"))
    for finding_id in finding_index:
        if finding_counts.get(finding_id) != 1:
            issues.append(_issue("reviewFindings", "KIN-E-REF", "each finding must be named exactly once"))
    return sorted(issues)


def _parse_review_document(payload: bytes, path: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    attestations = extract_fenced_json(payload, "kintsugi-review")
    findings_values = extract_fenced_json(payload, "kintsugi-review-findings")
    if (
        len(attestations) != 1
        or len(findings_values) != 1
        or not isinstance(attestations[0], dict)
        or not isinstance(findings_values[0], list)
        or any(not isinstance(value, dict) for value in findings_values[0])
    ):
        _raise(path, "KIN-E-REVIEW", "review Markdown must contain exactly two typed fences")
    attestation = attestations[0]
    findings = findings_values[0]
    structural_issues = _review_shape_issues(attestation, path)
    structural_issues.extend(
        issue
        for position, value in enumerate(findings)
        for issue in _finding_shape_issues(value, f"{path}.findings[{position}]")
    )
    if structural_issues:
        first = sorted(structural_issues)[0]
        raise KintsugiError(first.code, first.path, first.message)
    finding_ids = [value["id"] for value in findings]
    if finding_ids != sorted(finding_ids) or attestation["findingIds"] != finding_ids:
        _raise(path, "KIN-E-REVIEW", "review findings must be sorted and deep-equal the attestation IDs")
    if any(
        value["attemptId"] != attestation["attemptId"]
        or value["reviewKind"] != attestation["kind"]
        for value in findings
    ):
        _raise(path, "KIN-E-REVIEW", "review finding attempt/kind binding drifted")
    synchronization = synchronize_review_markdown(
        payload, attestation, findings, path=path
    )
    if synchronization.issues:
        first = synchronization.issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    return copy.deepcopy(attestation), copy.deepcopy(findings)


def _apply_review_documents(
    core: dict[str, object],
    attempt: dict[str, Any],
    artifact: dict[str, Any],
    review_documents: list[bytes],
) -> None:
    for ordinal, payload in enumerate(review_documents):
        if not isinstance(payload, bytes):
            _raise(f"reviewDocuments[{ordinal}]", "KIN-E-REVIEW", "review input must be raw bytes")
        attestation, findings = _parse_review_document(
            payload, f"reviewDocuments[{ordinal}]"
        )
        kind = attestation.get("kind")
        if kind not in {"LOGIC", "BTJ"}:
            _raise(f"reviewDocuments[{ordinal}]", "KIN-E-REVIEW", "review kind is invalid")
        pointer = "logicAttestationId" if kind == "LOGIC" else "btjAttestationId"
        hash_field = "logicReviewSha256" if kind == "LOGIC" else "btjReviewSha256"
        if attempt.get(pointer) is not None or artifact.get(hash_field) is not None:
            _raise(f"reviewDocuments[{ordinal}]", "KIN-E-REVIEW", "review kind is already recorded")
        if attestation.get("attemptId") != attempt.get("id"):
            _raise(f"reviewDocuments[{ordinal}]", "KIN-E-REF", "review names another attempt")
        attempt[pointer] = attestation.get("id")
        artifact[hash_field] = raw_hash(payload)
        _records(core, "reviewAttestations").append(attestation)
        _records(core, "reviewFindings").extend(findings)


def _current_reviews(
    core: dict[str, object], attempt_id: object
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    reviews = [
        value for value in _records(core, "reviewAttestations")
        if value.get("attemptId") == attempt_id
    ]
    findings = [
        value for value in _records(core, "reviewFindings")
        if value.get("attemptId") == attempt_id
    ]
    return reviews, findings


def _close_receipt_gates(
    core: dict[str, object],
    receipt: dict[str, Any],
    reviews: list[dict[str, object]],
) -> None:
    by_kind = {value.get("kind"): value for value in reviews}
    if set(by_kind) != {"LOGIC", "BTJ"}:
        _raise("reviewAttestations", "KIN-E-STATE", "gate closure requires LOGIC and BTJ PASS reviews")
    trial_ids = set(receipt.get("trialIds", []))
    owned_trials = [
        trial for trial in _records(core, "trials") if trial.get("id") in trial_ids
    ]
    if len(owned_trials) != len(trial_ids) or any(
        trial.get("receiptId") != receipt.get("id") or trial.get("status") != "CLOSED"
        for trial in owned_trials
    ):
        _raise("receipt.trialIds", "KIN-E-STATE", "completion requires every owned trial CLOSED")
    seam_ids = set(receipt.get("seamIds", []))
    owned_seams = [
        seam for seam in _records(core, "seams") if seam.get("id") in seam_ids
    ]
    if len(owned_seams) != len(seam_ids):
        _raise("receipt.seamIds", "KIN-E-REF", "receipt seam does not resolve exactly once")
    for seam in owned_seams:
        if seam.get("receiptId") != receipt.get("id") or seam.get("status") not in {
            "REPAIRED",
            "RETRACTED",
        }:
            _raise("receipt.seamIds", "KIN-E-STATE", "completion requires a reviewed repaired or retracted seam")
        for field, reviewer_path in (
            ("truthGate", receipt.get("logicReviewPath")),
            ("beautyGate", receipt.get("btjReviewPath")),
            ("justiceGate", receipt.get("btjReviewPath")),
        ):
            gate = seam.get(field)
            if not isinstance(gate, dict):
                _raise(f"seam.{field}", "KIN-E-STATE", "gate object is absent")
            if gate.get("status") != "PENDING" or gate.get("reviewerPath") is not None:
                _raise(f"seam.{field}", "KIN-E-STATE", "candidate gate is not pending review")
            gate["status"] = "PASS"
            gate["reviewerPath"] = reviewer_path
        if seam.get("status") == "REPAIRED":
            seam["status"] = "VERIFIED"


def _checked_transition(value: dict[str, object]) -> dict[str, object]:
    issues = validate_review_history(value)
    if issues:
        first = issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    return value


def _validate_transition_target(
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    attempt: dict[str, Any],
    value: dict[str, Any],
) -> None:
    if set(value) != _REVIEW_TARGET_FIELDS:
        _raise("reviewTarget", "KIN-E-BUNDLE", "review target shape is not exact")
    if (
        value.get("schemaVersion") != core.get("schemaVersion")
        or value.get("phase") != attempt.get("phase")
        or value.get("currentAttemptId") != attempt.get("id")
        or value.get("receiptId") != receipt.get("id")
    ):
        _raise("reviewTarget", "KIN-E-BUNDLE", "review target identity binding drifted")
    for field in (
        "schemaSha256",
        "receiptNarrativeRawSha256",
        "ledgerPreambleRawSha256",
        "reviewSubjectDigest",
    ):
        if not _valid_raw_hash(value.get(field)):
            _raise(f"reviewTarget.{field}", "KIN-E-BUNDLE", "review target hash is malformed")
    diff_paths = value.get("semanticDiffPaths")
    if (
        not _valid_unique_strings(diff_paths, predicate=_valid_path)
        or not diff_paths
    ):
        _raise("reviewTarget.semanticDiffPaths", "KIN-E-BUNDLE", "semantic diff paths are malformed or empty")

    target_manifest = copy.deepcopy(manifest)
    closure_paths = target_manifest.get("closureOnlyPaths")
    if isinstance(closure_paths, list):
        target_manifest["closureOnlyPaths"] = sorted(closure_paths)
    closure = _semantic_record_closure(core, manifest, receipt)
    expected = {
        "manifest": target_manifest,
        "sources": closure["sources"],
        "claims": closure["claims"],
        "trials": closure["trials"],
        "seams": [project_review_seam(item) for item in closure["seams"]],
        "propagations": closure["propagations"],
        "antibodies": closure["antibodies"],
        "discriminators": closure["discriminators"],
        "fixtures": closure["fixtures"],
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            _raise(f"reviewTarget.{field}", "KIN-E-BUNDLE", "review target semantic subject drifted")
    history = project_terminal_review_history(core, str(attempt["phase"]), str(attempt["id"]))
    history_fields = {
        "priorReviewAttempts": history["attempts"],
        "priorReviewAttemptArtifacts": history["artifacts"],
        "priorReviewAttestations": history["attestations"],
        "priorReviewFindings": history["findings"],
        "priorReviewFindingDispositions": history["dispositions"],
    }
    for field, expected_value in history_fields.items():
        if value.get(field) != expected_value:
            _raise(f"reviewTarget.{field}", "KIN-E-BUNDLE", "review target history drifted")
    sections = value.get("ledgerSemanticSections")
    seam_ids = set(closure["seamIds"])
    if not isinstance(sections, list) or {
        item.get("id") for item in sections if isinstance(item, dict)
    } != seam_ids:
        _raise("reviewTarget.ledgerSemanticSections", "KIN-E-BUNDLE", "ledger section set drifted")
    for item in sections:
        if (
            not isinstance(item, dict)
            or set(item) != {"id", "narrativeRawSha256", "seamProjection"}
            or not _valid_raw_hash(item.get("narrativeRawSha256"))
            or item.get("seamProjection")
            != next(
                projected
                for projected in expected["seams"]
                if projected.get("id") == item.get("id")
            )
        ):
            _raise("reviewTarget.ledgerSemanticSections", "KIN-E-BUNDLE", "ledger semantic section drifted")
    digest = compute_review_subject_digest(value)
    if value.get("reviewSubjectDigest") != digest or attempt.get("reviewSubjectDigest") != digest:
        _raise("reviewTarget.reviewSubjectDigest", "KIN-E-BUNDLE", "review subject digest drifted")


def _validate_transition_bundle(
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    attempt: dict[str, Any],
    artifact: dict[str, Any],
    value: dict[str, Any],
) -> None:
    if set(value) != _VALIDATION_BUNDLE_FIELDS:
        _raise("validationBundle", "KIN-E-BUNDLE", "validation bundle shape is not exact")
    closure = _semantic_record_closure(core, manifest, receipt)
    collections = _review_chain_collections(core, str(attempt["phase"]), str(attempt["id"]))
    expected_manifest = copy.deepcopy(manifest)
    closure_only_paths = expected_manifest.get("closureOnlyPaths")
    if isinstance(closure_only_paths, list):
        expected_manifest["closureOnlyPaths"] = sorted(closure_only_paths)
    expected: dict[str, object] = {
        "schemaVersion": core.get("schemaVersion"),
        "phase": attempt.get("phase"),
        "receiptDescriptor": _receipt_descriptor(receipt, attempt, artifact),
        "reviewTargetDigest": artifact.get("reviewTargetSha256"),
        "manifest": expected_manifest,
        "sources": closure["sources"],
        "claims": closure["claims"],
        "trials": closure["trials"],
        "seams": closure["seams"],
        "propagations": closure["propagations"],
        "antibodies": closure["antibodies"],
        "discriminators": closure["discriminators"],
        "fixtures": closure["fixtures"],
        "logicReviewSha256": artifact.get("logicReviewSha256"),
        "btjReviewSha256": artifact.get("btjReviewSha256"),
        "dependencyReceipts": closure["dependencyReceipts"],
        **collections,
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            _raise(f"validationBundle.{field}", "KIN-E-BUNDLE", "validation bundle binding drifted")
    for field in (
        "schemaSha256",
        "receiptNarrativeRawSha256",
        "ledgerPreambleRawSha256",
        "logicReviewSha256",
        "btjReviewSha256",
        "reviewTargetDigest",
    ):
        if not _valid_raw_hash(value.get(field)):
            _raise(f"validationBundle.{field}", "KIN-E-BUNDLE", "validation bundle hash is malformed")
    queue_hash = value.get("publicQueueSha256")
    if attempt.get("phase") == "C":
        if not _valid_raw_hash(queue_hash):
            _raise("validationBundle.publicQueueSha256", "KIN-E-BUNDLE", "public queue binding is malformed")
    elif queue_hash is not None:
        _raise("validationBundle.publicQueueSha256", "KIN-E-BUNDLE", "public queue is legal only for Phase C")
    ledger_sections = value.get("ledgerSections")
    seam_ids = set(closure["seamIds"])
    if (
        not isinstance(ledger_sections, list)
        or {item.get("id") for item in ledger_sections if isinstance(item, dict)} != seam_ids
        or any(
            not isinstance(item, dict)
            or set(item) != {"id", "sectionRawSha256"}
            or not _valid_raw_hash(item.get("sectionRawSha256"))
            for item in ledger_sections
        )
    ):
        _raise("validationBundle.ledgerSections", "KIN-E-BUNDLE", "ledger section binding is malformed")


def transition_core_value(
    core: dict[str, object],
    *,
    phase: str,
    stage: str,
    review_documents: list[bytes],
    abandon_reason: str | None = None,
) -> dict[str, object]:
    if stage not in {"TARGET_READY", "ATTESTED", "FAILED", "ABANDONED", "COMPLETE", "VERIFIED"}:
        _raise("stage", "KIN-E-STATE", "review transition stage is invalid")
    if stage == "ABANDONED":
        if not isinstance(abandon_reason, str) or not abandon_reason.strip():
            _raise("abandonReason", "KIN-E-STATE", "ABANDONED requires a non-empty reason")
    elif abandon_reason is not None:
        _raise("abandonReason", "KIN-E-STATE", "reason is legal only for ABANDONED")

    _checked_transition(copy.deepcopy(core))
    prospective = copy.deepcopy(core)
    _, receipt = _selected_manifest_receipt(prospective, phase)
    attempt_id = receipt.get("reviewAttemptId")
    if not isinstance(attempt_id, str):
        _raise("receipt.reviewAttemptId", "KIN-E-STATE", "transition requires a current attempt")
    manifest, _, attempt, artifact = _selected_attempt(prospective, phase, attempt_id)

    if stage == "TARGET_READY":
        if attempt.get("status") != "PENDING" or len(review_documents) != 1:
            _raise("TARGET_READY", "KIN-E-STATE", "TARGET_READY requires one target for a PENDING attempt")
        payload = review_documents[0]
        value = _mapping(_decode_canonical(payload, "reviewTarget"), "reviewTarget")
        _validate_transition_target(prospective, manifest, receipt, attempt, value)
        digest = raw_hash(payload)
        existing = artifact.get("reviewTargetSha256")
        if existing not in {None, digest}:
            _raise("reviewTarget", "KIN-E-BUNDLE", "immutable review target drifted")
        artifact["reviewTargetSha256"] = digest
        transitioned = _checked_transition(prospective)
        transition_issues = validate_state_transition(core, transitioned, stage)
        if transition_issues:
            first = transition_issues[0]
            raise KintsugiError(first.code, first.path, first.message)
        return transitioned

    if stage == "VERIFIED":
        if (
            attempt.get("status") != "PASSED"
            or receipt.get("status") != "COMPLETE"
            or len(review_documents) != 1
        ):
            _raise("VERIFIED", "KIN-E-STATE", "VERIFIED requires one bundle after COMPLETE")
        payload = review_documents[0]
        value = _mapping(_decode_canonical(payload, "validationBundle"), "validationBundle")
        _validate_transition_bundle(
            prospective, manifest, receipt, attempt, artifact, value
        )
        receipt["status"] = "VERIFIED"
        receipt["validationBundlePath"] = attempt.get("validationBundlePath")
        receipt["validationDigest"] = raw_hash(payload)
        transitioned = _checked_transition(prospective)
        transition_issues = validate_state_transition(core, transitioned, stage)
        if transition_issues:
            first = transition_issues[0]
            raise KintsugiError(first.code, first.path, first.message)
        return transitioned

    if attempt.get("status") != "PENDING" or receipt.get("status") != "DRAFT":
        _raise(stage, "KIN-E-STATE", "review intake requires the current DRAFT/PENDING attempt")
    existing_reviews, _ = _current_reviews(prospective, attempt_id)
    if stage == "ATTESTED" and (existing_reviews or len(review_documents) != 1):
        _raise(stage, "KIN-E-STATE", "ATTESTED requires exactly one newly authored PASS review")
    if stage == "COMPLETE" and (
        len(existing_reviews) != 1
        or existing_reviews[0].get("verdict") != "PASS"
        or len(review_documents) != 1
    ):
        _raise(stage, "KIN-E-STATE", "COMPLETE requires one persisted PASS and one new review")
    if stage == "FAILED" and not 1 <= len(review_documents) <= 2 - len(existing_reviews):
        _raise(stage, "KIN-E-STATE", "FAILED requires one or two bounded review inputs")
    if stage == "ABANDONED" and len(review_documents) > 2 - len(existing_reviews):
        _raise(stage, "KIN-E-STATE", "ABANDONED preserves at most two reviews")
    _apply_review_documents(prospective, attempt, artifact, review_documents)
    reviews, findings = _current_reviews(prospective, attempt_id)
    attestation_issues = validate_review_attestations(prospective, reviews, findings)
    if attestation_issues:
        first = attestation_issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    verdicts = [value.get("verdict") for value in reviews]

    if stage == "ATTESTED":
        if len(reviews) != 1 or verdicts != ["PASS"]:
            _raise(stage, "KIN-E-STATE", "ATTESTED requires exactly one PASS review")
    elif stage == "FAILED":
        if not reviews or "FAIL" not in verdicts:
            _raise(stage, "KIN-E-STATE", "FAILED requires at least one FAIL review")
        attempt["status"] = "FAILED"
    elif stage == "ABANDONED":
        if len(reviews) > 2:
            _raise(stage, "KIN-E-STATE", "ABANDONED preserves at most two reviews")
        attempt["status"] = "ABANDONED"
        attempt["abandonReason"] = abandon_reason
    else:
        if len(reviews) != 2 or sorted(verdicts) != ["PASS", "PASS"]:
            _raise(stage, "KIN-E-STATE", "COMPLETE requires independent LOGIC and BTJ PASS reviews")
        attempt["status"] = "PASSED"
        receipt["status"] = "COMPLETE"
        receipt["reviewTargetDigest"] = artifact.get("reviewTargetSha256")
        receipt["logicReviewPath"] = attempt.get("logicReviewPath")
        receipt["btjReviewPath"] = attempt.get("btjReviewPath")
        _close_receipt_gates(prospective, receipt, reviews)
    transitioned = _checked_transition(prospective)
    transition_issues = validate_state_transition(core, transitioned, stage)
    if transition_issues:
        first = transition_issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    return transitioned


def validate_state_transition(
    before: dict[str, object], after: dict[str, object], stage: str
) -> list[Issue]:
    if stage not in {
        "TARGET_READY",
        "ATTESTED",
        "FAILED",
        "ABANDONED",
        "COMPLETE",
        "VERIFIED",
    }:
        return [_issue("stage", "KIN-E-STATE", "transition stage is invalid")]

    def sequence(value: Mapping[str, object], field: str) -> list[object]:
        selected = value.get(field)
        return selected if isinstance(selected, list) else []

    def changed_indices(field: str) -> list[int]:
        left = sequence(before, field)
        right = sequence(after, field)
        return [
            index
            for index in range(max(len(left), len(right)))
            if index >= len(left) or index >= len(right) or left[index] != right[index]
        ]

    attempt_changes = changed_indices("reviewAttempts")
    artifact_changes = changed_indices("reviewAttemptArtifacts")
    receipt_changes = changed_indices("phaseReceipts")
    selector: object = None
    if stage == "TARGET_READY" and len(artifact_changes) == 1:
        artifacts = sequence(after, "reviewAttemptArtifacts")
        if artifact_changes[0] < len(artifacts) and isinstance(
            artifacts[artifact_changes[0]], dict
        ):
            selector = artifacts[artifact_changes[0]].get("attemptId")
    elif stage == "VERIFIED" and len(receipt_changes) == 1:
        receipts = sequence(after, "phaseReceipts")
        if receipt_changes[0] < len(receipts) and isinstance(
            receipts[receipt_changes[0]], dict
        ):
            selector = receipts[receipt_changes[0]].get("reviewAttemptId")
    elif len(attempt_changes) == 1:
        attempts = sequence(after, "reviewAttempts")
        if attempt_changes[0] < len(attempts) and isinstance(
            attempts[attempt_changes[0]], dict
        ):
            selector = attempts[attempt_changes[0]].get("id")
    if not isinstance(selector, str):
        return [_issue("core", "KIN-E-STATE", "transition does not identify exactly one current attempt")]

    attempts_after = sequence(after, "reviewAttempts")
    artifacts_after = sequence(after, "reviewAttemptArtifacts")
    receipts_after = sequence(after, "phaseReceipts")
    attempt_index = next(
        (index for index, value in enumerate(attempts_after) if isinstance(value, dict) and value.get("id") == selector),
        None,
    )
    artifact_index = next(
        (index for index, value in enumerate(artifacts_after) if isinstance(value, dict) and value.get("attemptId") == selector),
        None,
    )
    receipt_index = next(
        (
            index
            for index, value in enumerate(receipts_after)
            if isinstance(value, dict) and value.get("reviewAttemptId") == selector
        ),
        None,
    )
    if attempt_index is None or artifact_index is None or receipt_index is None:
        return [_issue("core", "KIN-E-STATE", "transition attempt/artifact/receipt binding is incomplete")]
    receipt = receipts_after[receipt_index]
    if not isinstance(receipt, dict):
        return [_issue("core.phaseReceipts", "KIN-E-STATE", "transition receipt is malformed")]

    def diff_paths(left: object, right: object, prefix: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
        if isinstance(left, dict) and isinstance(right, dict):
            paths: list[tuple[object, ...]] = []
            for key in sorted(set(left) | set(right)):
                if key not in left or key not in right:
                    paths.append((*prefix, key))
                else:
                    paths.extend(diff_paths(left[key], right[key], (*prefix, key)))
            return paths
        if isinstance(left, list) and isinstance(right, list):
            paths = []
            for index in range(max(len(left), len(right))):
                if index >= len(left) or index >= len(right):
                    paths.append((*prefix, index))
                else:
                    paths.extend(diff_paths(left[index], right[index], (*prefix, index)))
            return paths
        return [] if left == right else [prefix]

    review_attempt_fields = {
        "ATTESTED": {"logicAttestationId", "btjAttestationId"},
        "FAILED": {"logicAttestationId", "btjAttestationId", "status"},
        "ABANDONED": {
            "logicAttestationId",
            "btjAttestationId",
            "status",
            "abandonReason",
        },
        "COMPLETE": {"logicAttestationId", "btjAttestationId", "status"},
    }.get(stage, set())
    artifact_fields = {
        "TARGET_READY": {"reviewTargetSha256"},
        "ATTESTED": {"logicReviewSha256", "btjReviewSha256"},
        "FAILED": {"logicReviewSha256", "btjReviewSha256"},
        "ABANDONED": {"logicReviewSha256", "btjReviewSha256"},
        "COMPLETE": {"logicReviewSha256", "btjReviewSha256"},
    }.get(stage, set())
    receipt_fields = {
        "COMPLETE": {
            "status",
            "reviewTargetDigest",
            "logicReviewPath",
            "btjReviewPath",
        },
        "VERIFIED": {"status", "validationBundlePath", "validationDigest"},
    }.get(stage, set())
    seam_indices = {
        index
        for index, value in enumerate(sequence(after, "seams"))
        if isinstance(value, dict) and value.get("id") in set(receipt.get("seamIds", []))
    }

    def allowed(path: tuple[object, ...]) -> bool:
        if len(path) >= 3 and path[:2] == ("reviewAttempts", attempt_index):
            return path[2] in review_attempt_fields
        if len(path) >= 3 and path[:2] == ("reviewAttemptArtifacts", artifact_index):
            return path[2] in artifact_fields
        if len(path) >= 3 and path[:2] == ("phaseReceipts", receipt_index):
            return path[2] in receipt_fields
        if path and path[0] in {"reviewAttestations", "reviewFindings"}:
            collection = str(path[0])
            prior_length = len(sequence(before, collection))
            return len(path) >= 2 and isinstance(path[1], int) and path[1] >= prior_length
        if (
            stage == "COMPLETE"
            and len(path) >= 3
            and path[0] == "seams"
            and path[1] in seam_indices
        ):
            if path[2] == "status":
                return True
            return (
                len(path) >= 4
                and path[2] in {"truthGate", "beautyGate", "justiceGate"}
                and path[3] in {"status", "reviewerPath"}
            )
        return False

    issues: list[Issue] = []
    for path in diff_paths(before, after):
        if not allowed(path):
            rendered = "core" + "".join(
                f"[{part}]" if isinstance(part, int) else f".{part}" for part in path
            )
            issues.append(_issue(rendered, "KIN-E-STATE", "transition changed an unauthorized field"))
    issues.extend(validate_review_history(after))
    return sorted(set(issues))


def _review_chain_collections(
    core: dict[str, object], phase: str, attempt_id: str
) -> dict[str, list[dict[str, Any]]]:
    history = project_terminal_review_history(core, phase, attempt_id)
    chain_ids = {value["id"] for value in history["attempts"]} | {attempt_id}
    return {
        "reviewAttempts": copy.deepcopy([
            value for value in _records(core, "reviewAttempts")
            if value.get("id") in chain_ids
        ]),
        "reviewAttemptArtifacts": copy.deepcopy([
            value for value in _records(core, "reviewAttemptArtifacts")
            if value.get("attemptId") in chain_ids
        ]),
        "reviewAttestations": copy.deepcopy([
            value for value in _records(core, "reviewAttestations")
            if value.get("attemptId") in chain_ids
        ]),
        "reviewFindings": copy.deepcopy([
            value for value in _records(core, "reviewFindings")
            if value.get("attemptId") in chain_ids
        ]),
        "reviewFindingDispositions": copy.deepcopy([
            value for value in _records(core, "reviewFindingDispositions")
            if value.get("successorAttemptId") in chain_ids
        ]),
    }


def _receipt_descriptor(
    receipt: dict[str, Any], attempt: dict[str, Any], artifact: dict[str, Any]
) -> dict[str, object]:
    fields = (
        "id",
        "phase",
        "path",
        "manifestId",
        "dependsOnReceiptIds",
        "claimIds",
        "trialIds",
        "seamIds",
        "propagationIds",
        "reviewAttemptId",
    )
    descriptor = {field: copy.deepcopy(receipt.get(field)) for field in fields}
    descriptor.update({
        "status": "VERIFIED",
        "reviewTargetDigest": artifact.get("reviewTargetSha256"),
        "validationBundlePath": attempt.get("validationBundlePath"),
        "logicReviewPath": attempt.get("logicReviewPath"),
        "btjReviewPath": attempt.get("btjReviewPath"),
    })
    return descriptor


def build_validation_bundle_from_control_bytes(
    schema: dict[str, object],
    core: dict[str, object],
    *,
    phase: str,
    attempt_id: str,
    review_target: dict[str, object],
    public_queue: dict[str, object] | None,
    schema_bytes: bytes,
    ledger_bytes: bytes,
    receipt_bytes: bytes,
) -> dict[str, object]:
    if schema_bytes != canonical_json_bytes(schema):
        _raise(_SCHEMA_PATH, "KIN-E-BUNDLE", "schema bytes do not match the supplied schema")
    history_issues = validate_review_history(core)
    if history_issues:
        first = history_issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    _schema_or_raise(schema, "reviewTarget", review_target, "KIN-E-BUNDLE")
    manifest, receipt, attempt, artifact = _selected_attempt(core, phase, attempt_id)
    if attempt.get("status") != "PASSED" or receipt.get("status") not in {"COMPLETE", "VERIFIED"}:
        _raise("validationBundle", "KIN-E-STATE", "bundle requires the current PASSED attempt")
    if artifact.get("reviewTargetSha256") != raw_hash(canonical_json_bytes(review_target)):
        _raise("reviewTarget", "KIN-E-BUNDLE", "review target bytes do not match the attempt artifact")
    if review_target.get("reviewSubjectDigest") != attempt.get("reviewSubjectDigest"):
        _raise("reviewTarget", "KIN-E-BUNDLE", "review subject digest drifted")

    receipt_sync = synchronize_receipt_markdown(
        receipt_bytes,
        receipt,
        path=str(receipt.get("path")),
        target_frozen=True,
    )
    if receipt_sync.issues:
        first = receipt_sync.issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    ledger_sync = synchronize_ledger_markdown(
        ledger_bytes, _records(core, "seams"), path=_LEDGER_PATH
    )
    if ledger_sync.issues:
        first = ledger_sync.issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    closure = _semantic_record_closure(core, manifest, receipt)
    seam_ids = set(closure["seamIds"])
    current_manifest = copy.deepcopy(manifest)
    current_closure_paths = current_manifest.get("closureOnlyPaths")
    if isinstance(current_closure_paths, list):
        current_manifest["closureOnlyPaths"] = sorted(current_closure_paths)
    expected_target_values: dict[str, object] = {
        "manifest": current_manifest,
        "sources": closure["sources"],
        "claims": closure["claims"],
        "trials": closure["trials"],
        "seams": [project_review_seam(value) for value in closure["seams"]],
        "propagations": closure["propagations"],
        "antibodies": closure["antibodies"],
        "discriminators": closure["discriminators"],
        "fixtures": closure["fixtures"],
        "schemaSha256": raw_hash(schema_bytes),
        "receiptNarrativeRawSha256": receipt_sync.narrative_raw_sha256,
        "ledgerPreambleRawSha256": ledger_sync.preamble.raw_sha256,
        "ledgerSemanticSections": [
            {
                "id": section.id,
                "narrativeRawSha256": section.narrative_raw_sha256,
                "seamProjection": copy.deepcopy(section.seam_projection),
            }
            for section in ledger_sync.sections
            if section.id in seam_ids
        ],
    }
    for field, expected in expected_target_values.items():
        if review_target.get(field) != expected:
            _raise(field, "KIN-E-BUNDLE", "review target no longer matches prospective control state")
    collections = _review_chain_collections(core, phase, attempt_id)
    bundle: dict[str, object] = {
        "schemaVersion": core.get("schemaVersion"),
        "phase": phase,
        "receiptDescriptor": _receipt_descriptor(receipt, attempt, artifact),
        "reviewTargetDigest": artifact.get("reviewTargetSha256"),
        "manifest": copy.deepcopy(review_target.get("manifest")),
        "sources": copy.deepcopy(closure["sources"]),
        "claims": copy.deepcopy(closure["claims"]),
        "trials": copy.deepcopy(closure["trials"]),
        "seams": copy.deepcopy(closure["seams"]),
        "propagations": copy.deepcopy(closure["propagations"]),
        "antibodies": copy.deepcopy(closure["antibodies"]),
        "discriminators": copy.deepcopy(closure["discriminators"]),
        "fixtures": copy.deepcopy(closure["fixtures"]),
        "schemaSha256": raw_hash(schema_bytes),
        "ledgerSections": [
            {"id": section.id, "sectionRawSha256": section.raw_sha256}
            for section in ledger_sync.sections
            if section.id in seam_ids
        ],
        "logicReviewSha256": artifact.get("logicReviewSha256"),
        "btjReviewSha256": artifact.get("btjReviewSha256"),
        "publicQueueSha256": (
            raw_hash(canonical_json_bytes(public_queue))
            if phase == "C" and public_queue is not None
            else None
        ),
        "dependencyReceipts": copy.deepcopy(closure["dependencyReceipts"]),
        "receiptNarrativeRawSha256": receipt_sync.narrative_raw_sha256,
        "ledgerPreambleRawSha256": ledger_sync.preamble.raw_sha256,
        **collections,
    }
    if phase == "C" and public_queue is None:
        _raise("publicQueue", "KIN-E-BUNDLE", "Phase C bundle requires the public queue")
    if phase != "C" and public_queue is not None:
        _raise("publicQueue", "KIN-E-BUNDLE", "public queue is legal only for Phase C")
    _schema_or_raise(schema, "validationBundle", bundle, "KIN-E-BUNDLE")
    return bundle


def validate_validation_bundle(
    schema: dict[str, object],
    core: dict[str, object],
    bundle: dict[str, object],
    *,
    phase: str,
    attempt_id: str,
    review_target: dict[str, object],
    public_queue: dict[str, object] | None,
    schema_bytes: bytes | None = None,
    ledger_bytes: bytes | None = None,
    receipt_bytes: bytes | None = None,
) -> list[Issue]:
    issues = [
        _issue(value.path, "KIN-E-BUNDLE", value.message)
        for value in validate_named_definition(schema, "validationBundle", bundle)
    ]
    try:
        _, receipt, attempt, artifact = _selected_attempt(core, phase, attempt_id)
        collections = _review_chain_collections(core, phase, attempt_id)
        semantic_fields = (
            "manifest",
            "sources",
            "claims",
            "trials",
            "propagations",
            "antibodies",
            "discriminators",
            "fixtures",
        )
        for field in semantic_fields:
            if bundle.get(field) != review_target.get(field):
                issues.append(_issue(field, "KIN-E-BUNDLE", "bundle semantic subject drifted"))
        bundle_seams = bundle.get("seams")
        projected_seams = (
            [project_review_seam(value) for value in bundle_seams]
            if isinstance(bundle_seams, list)
            and all(isinstance(value, dict) for value in bundle_seams)
            else None
        )
        if projected_seams != review_target.get("seams"):
            issues.append(_issue("seams", "KIN-E-BUNDLE", "bundle seam subject drifted"))
        for field, value in collections.items():
            if bundle.get(field) != value:
                issues.append(_issue(field, "KIN-E-BUNDLE", "bundle review history drifted"))
        closure = _semantic_record_closure(core, *_selected_manifest_receipt(core, phase))
        expected = {
            "schemaVersion": core.get("schemaVersion"),
            "phase": phase,
            "reviewTargetDigest": artifact.get("reviewTargetSha256"),
            "logicReviewSha256": artifact.get("logicReviewSha256"),
            "btjReviewSha256": artifact.get("btjReviewSha256"),
            "receiptDescriptor": _receipt_descriptor(receipt, attempt, artifact),
            "schemaSha256": review_target.get("schemaSha256"),
            "receiptNarrativeRawSha256": review_target.get(
                "receiptNarrativeRawSha256"
            ),
            "ledgerPreambleRawSha256": review_target.get(
                "ledgerPreambleRawSha256"
            ),
            "dependencyReceipts": closure["dependencyReceipts"],
            "publicQueueSha256": (
                raw_hash(canonical_json_bytes(public_queue))
                if phase == "C" and public_queue is not None
                else None
            ),
        }
        for field, value in expected.items():
            if bundle.get(field) != value:
                issues.append(_issue(field, "KIN-E-BUNDLE", "bundle binding drifted"))
        ledger_sections = bundle.get("ledgerSections")
        expected_section_ids = [
            value.get("id")
            for value in review_target.get("ledgerSemanticSections", [])
            if isinstance(value, dict)
        ]
        observed_section_ids = (
            [value.get("id") for value in ledger_sections if isinstance(value, dict)]
            if isinstance(ledger_sections, list)
            else None
        )
        if observed_section_ids != expected_section_ids:
            issues.append(_issue("ledgerSections", "KIN-E-BUNDLE", "bundle ledger section set drifted"))

        supplied = (schema_bytes, ledger_bytes, receipt_bytes)
        if any(value is not None for value in supplied):
            if not all(isinstance(value, bytes) for value in supplied):
                issues.append(_issue("validationBundle", "KIN-E-BUNDLE", "control bytes must be supplied as one complete set"))
            else:
                exact = build_validation_bundle_from_control_bytes(
                    schema,
                    core,
                    phase=phase,
                    attempt_id=attempt_id,
                    review_target=review_target,
                    public_queue=public_queue,
                    schema_bytes=schema_bytes,
                    ledger_bytes=ledger_bytes,
                    receipt_bytes=receipt_bytes,
                )
                if bundle != exact:
                    issues.append(_issue("validationBundle", "KIN-E-BUNDLE", "bundle differs from exact frozen control projection"))
    except KintsugiError as exc:
        issues.append(_issue(exc.path, "KIN-E-BUNDLE", exc.message))
    return sorted(issues)


def build_validation_bundle_value(
    root: Path,
    schema: dict[str, object],
    core: dict[str, object],
    *,
    phase: str,
    attempt_id: str,
    review_target: dict[str, object],
    public_queue: dict[str, object] | None,
) -> dict[str, object]:
    _, receipt, _, _ = _selected_attempt(core, phase, attempt_id)
    schema_bytes = _read_regular_no_symlinks(
        root, _SCHEMA_PATH, code="KIN-E-BUNDLE", require_single_link=True
    )
    ledger_bytes = _read_regular_no_symlinks(
        root, _LEDGER_PATH, code="KIN-E-BUNDLE", require_single_link=True
    )
    receipt_path = str(receipt.get("path"))
    receipt_bytes = _read_regular_no_symlinks(
        root, receipt_path, code="KIN-E-BUNDLE", require_single_link=True
    )
    return build_validation_bundle_from_control_bytes(
        schema,
        core,
        phase=phase,
        attempt_id=attempt_id,
        review_target=review_target,
        public_queue=public_queue,
        schema_bytes=schema_bytes,
        ledger_bytes=ledger_bytes,
        receipt_bytes=receipt_bytes,
    )


__all__ = [
    "build_review_target_value",
    "build_validation_bundle_value",
    "compute_review_subject_digest",
    "transition_core_value",
    "validate_review_attestations",
    "validate_review_history",
]
