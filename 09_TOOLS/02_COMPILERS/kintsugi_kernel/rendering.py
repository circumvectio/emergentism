from __future__ import annotations

import copy
import json
import os
import stat
import tempfile
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from .codec import canonical_json_bytes, raw_hash, safe_repo_path
from .diagnostics import KintsugiError
from .gitstate import (
    AttemptPlan,
    GitState,
    _check_head_core_cas,
    _fsync_directory,
    _list_worktrees,
    _plan_next_attempt,
    _read_regular_no_symlinks,
    _reserve_attempt_id,
    _resolve_commit,
    _transition_lock,
    _validate_predecessor_fence,
    inspect_git_state,
    resolve_git_common_dir,
)
from .manifest import _freeze_manifest_value_with_plan, _semantic_diff_paths
from .markdown import (
    extract_fenced_json,
    synchronize_ledger_markdown,
    synchronize_receipt_markdown,
)
from .schema import validate_named_definition
from .semantics import validate_core_records


_SCHEMA_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
_LEDGER_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
_PUBLIC_QUEUE_PATH = (
    "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_public_propagation_queue.json"
)
_CLOSURE_ROOTS = (
    "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts",
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS",
)
_OPERATIONS = frozenset({
    "freeze-manifest",
    "review-target",
    "bundle",
    "transition-core",
})
_TRANSITION_STAGES = frozenset({
    "ATTESTED",
    "FAILED",
    "ABANDONED",
    "COMPLETE",
    "VERIFIED",
})
_REVIEW_INPUT_STAGES = frozenset({
    "ATTESTED",
    "FAILED",
    "ABANDONED",
    "COMPLETE",
})


@dataclass(frozen=True)
class RenderTransactionRequest:
    operation: str
    phase: str
    stage: str | None
    core_path: str
    output_path: str
    canonical_root: Path | None
    base_ref: str | None
    expected_head: str
    expected_core_sha256: str
    logic_review_input: Path | None = None
    btj_review_input: Path | None = None
    finding_dispositions_input: Path | None = None
    abandon_reason: str | None = None


@dataclass(frozen=True)
class _ReadSnapshot:
    path: Path
    label: str
    kind: str
    digest: str | None
    payload: bytes | None
    mode: int | None
    parent_identities: tuple[tuple[str, int, int], ...]


@dataclass(frozen=True)
class _GitFingerprint:
    isolated_signature: tuple[object, ...]
    canonical_signature: tuple[object, ...] | None
    worktrees: tuple[tuple[str, str, str | None], ...]
    base_ref_commit: str | None
    isolated_state: GitState = dataclass_field(compare=False)


@dataclass(frozen=True)
class _NamespaceFingerprint:
    isolated: tuple[tuple[str, str, str | None], ...]
    canonical: tuple[tuple[str, str, str | None], ...] | None


@dataclass(frozen=True)
class _Output:
    relative: str
    payload: bytes


@dataclass
class _StagedOutput:
    output: _Output
    destination: Path
    temporary: Path
    backup: Path | None
    existed: bool
    installed: bool = False


def _raise(code: str, path: str, message: str) -> None:
    raise KintsugiError(code, path, message)


def _is_commit(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_raw_hash(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(character in "0123456789abcdef" for character in value[7:])
    )


def _validate_request(request: RenderTransactionRequest) -> None:
    if not isinstance(request, RenderTransactionRequest):
        _raise("KIN-E-CLI", "request", "request must be a RenderTransactionRequest")
    if request.operation not in _OPERATIONS:
        _raise("KIN-E-CLI", "operation", "renderer operation is not recognized")
    if request.phase not in {"A", "B", "C"}:
        _raise("KIN-E-CLI", "phase", "phase must be A, B, or C")
    if request.operation == "transition-core":
        if request.stage not in _TRANSITION_STAGES:
            _raise("KIN-E-CLI", "stage", "transition stage is not recognized")
    elif request.stage is not None:
        _raise("KIN-E-CLI", "stage", "stage is irrelevant to this operation")
    if not isinstance(request.core_path, str) or not request.core_path:
        _raise("KIN-E-CLI", "core-path", "core path must be non-empty")
    if not isinstance(request.output_path, str) or not request.output_path:
        _raise("KIN-E-CLI", "output", "output path must be non-empty")
    if not _is_commit(request.expected_head):
        _raise("KIN-E-CLI", "expected-head", "expected HEAD must be a full lowercase commit")
    if not _is_raw_hash(request.expected_core_sha256):
        _raise(
            "KIN-E-CLI",
            "expected-core-sha256",
            "expected core hash must be a canonical raw SHA-256",
        )
    if request.canonical_root is not None and not isinstance(request.canonical_root, Path):
        _raise("KIN-E-CLI", "canonical-root", "canonical root must be a Path")
    if request.base_ref is not None and (
        not isinstance(request.base_ref, str) or not request.base_ref
    ):
        _raise("KIN-E-CLI", "base-ref", "base ref must be non-empty when supplied")
    for name in (
        "logic_review_input",
        "btj_review_input",
        "finding_dispositions_input",
    ):
        value = getattr(request, name)
        if value is not None and not isinstance(value, Path):
            _raise("KIN-E-CLI", name.replace("_", "-"), "external input must be a Path")

    has_reviews = (
        request.logic_review_input is not None
        or request.btj_review_input is not None
    )
    if request.operation == "freeze-manifest":
        if request.canonical_root is None or request.base_ref is None:
            _raise(
                "KIN-E-CLI",
                "freeze-manifest",
                "final freeze requires canonical root and base ref",
            )
        if has_reviews or request.abandon_reason is not None:
            _raise("KIN-E-CLI", "freeze-manifest", "review or reason input is irrelevant")
    elif request.operation in {"review-target", "bundle"}:
        if request.base_ref is not None:
            _raise("KIN-E-CLI", "base-ref", "base ref is used only by freeze-manifest")
        if has_reviews or request.finding_dispositions_input is not None or request.abandon_reason is not None:
            _raise("KIN-E-CLI", request.operation, "external intake is irrelevant to this operation")
    else:
        if request.base_ref is not None:
            _raise("KIN-E-CLI", "base-ref", "base ref is used only by freeze-manifest")
        if request.finding_dispositions_input is not None:
            _raise("KIN-E-CLI", "finding-dispositions-input", "dispositions allocate attempts only")
        if request.stage not in _REVIEW_INPUT_STAGES and has_reviews:
            _raise("KIN-E-CLI", "review-input", "review input is irrelevant to this stage")
        if request.stage == "ABANDONED":
            if not isinstance(request.abandon_reason, str) or not request.abandon_reason.strip():
                _raise("KIN-E-CLI", "abandon-reason", "ABANDONED requires a non-empty reason")
        elif request.abandon_reason is not None:
            _raise("KIN-E-CLI", "abandon-reason", "reason is permitted only for ABANDONED")


def _safe_repo_value(root: Path, relative: str) -> Path:
    try:
        safe_repo_path(root, relative)
        resolved_root = root.resolve(strict=True)
    except (OSError, RuntimeError):
        _raise("KIN-E-PATH", relative, "repository path cannot be resolved safely")
    return resolved_root.joinpath(*PurePosixPath(relative).parts)


def _mapping(value: object, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _raise("KIN-E-CANONICAL", path, "expected a canonical JSON object")
    return value


def _list(value: object, path: str) -> list[Any]:
    if not isinstance(value, list):
        _raise("KIN-E-MANIFEST", path, "expected an array")
    return value


def _decode_canonical_bytes(payload: bytes, path: str) -> object:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError):
        _raise("KIN-E-JSON", path, "input is not bounded canonical JSON")
    try:
        rendered = canonical_json_bytes(value)
    except RecursionError:
        _raise("KIN-E-JSON", path, "JSON exceeds the supported nesting depth")
    except UnicodeError:
        _raise("KIN-E-CANONICAL", path, "JSON cannot be encoded as canonical UTF-8")
    if payload != rendered:
        _raise("KIN-E-CANONICAL", path, "JSON bytes are not canonical")
    return value


def _load_core_locked(root: Path, relative: str) -> dict[str, Any]:
    payload = _read_regular_no_symlinks(
        root,
        relative,
        code="KIN-E-CONCURRENT",
        require_single_link=True,
    )
    return _mapping(_decode_canonical_bytes(payload, relative), relative)


def _selected_manifest(core: Mapping[str, object], phase: str) -> dict[str, Any]:
    matches = [
        value
        for value in _list(core.get("manifests"), "core.manifests")
        if isinstance(value, dict) and value.get("phase") == phase
    ]
    if len(matches) != 1:
        _raise("KIN-E-MANIFEST", "core.manifests", "phase must select exactly one manifest")
    return matches[0]


def _selected_receipt(core: Mapping[str, object], phase: str) -> dict[str, Any]:
    matches = [
        value
        for value in _list(core.get("phaseReceipts"), "core.phaseReceipts")
        if isinstance(value, dict) and value.get("phase") == phase
    ]
    if len(matches) != 1:
        _raise("KIN-E-RECEIPT", "core.phaseReceipts", "phase must select exactly one receipt")
    return matches[0]


def _current_attempt(
    core: Mapping[str, object], receipt: Mapping[str, object]
) -> dict[str, Any]:
    attempt_id = receipt.get("reviewAttemptId")
    if not isinstance(attempt_id, str):
        _raise("KIN-E-STATE", "receipt.reviewAttemptId", "operation requires a current attempt")
    matches = [
        value
        for value in _list(core.get("reviewAttempts"), "core.reviewAttempts")
        if isinstance(value, dict) and value.get("id") == attempt_id
    ]
    if len(matches) != 1:
        _raise("KIN-E-STATE", "core.reviewAttempts", "current attempt does not resolve exactly once")
    return matches[0]


def _attempt_artifact(core: Mapping[str, object], attempt_id: str) -> dict[str, Any]:
    matches = [
        value
        for value in _list(
            core.get("reviewAttemptArtifacts"), "core.reviewAttemptArtifacts"
        )
        if isinstance(value, dict) and value.get("attemptId") == attempt_id
    ]
    if len(matches) != 1:
        _raise("KIN-E-STATE", "core.reviewAttemptArtifacts", "attempt artifact does not resolve exactly once")
    return matches[0]


def _path_values(value: object, path: str) -> tuple[str, ...]:
    values = _list(value, path)
    if any(not isinstance(item, str) or not item for item in values):
        _raise("KIN-E-MANIFEST", path, "path list contains a malformed value")
    if values != sorted(set(values)):
        _raise("KIN-E-MANIFEST", path, "path list must be sorted and unique")
    return tuple(values)


def _is_below(relative: str, roots: Iterable[str]) -> bool:
    return any(relative == root or relative.startswith(root + "/") for root in roots)


def _validate_repo_output(
    root: Path,
    relative: str,
    manifest: Mapping[str, object],
    *,
    closure_required: bool | None,
) -> Path:
    target = _safe_repo_value(root, relative)
    protected = _path_values(manifest.get("protectedPaths"), "manifest.protectedPaths")
    if _is_below(relative, protected):
        _raise("KIN-E-PROTECTED", relative, "renderer output is inside a protected boundary")
    allowed = set(_path_values(
        manifest.get("allowedChangePaths"), "manifest.allowedChangePaths"
    ))
    if relative not in allowed:
        _raise("KIN-E-SCOPE", relative, "renderer output is not an allowed change path")
    closure = set(_path_values(
        manifest.get("closureOnlyPaths"), "manifest.closureOnlyPaths"
    ))
    if closure_required is True and relative not in closure:
        _raise("KIN-E-SCOPE", relative, "renderer output is not the derived closure role")
    if closure_required is False and relative in closure:
        _raise("KIN-E-SCOPE", relative, "control output cannot be closure-only")
    return target


def _validate_operation_paths(
    root: Path,
    request: RenderTransactionRequest,
    core: Mapping[str, object],
    manifest: Mapping[str, object],
    receipt: Mapping[str, object],
) -> None:
    _validate_repo_output(root, request.core_path, manifest, closure_required=False)
    if request.operation in {"freeze-manifest", "transition-core"}:
        _validate_repo_output(root, request.output_path, manifest, closure_required=False)
        if request.output_path != request.core_path:
            _raise("KIN-E-SCOPE", request.output_path, "operation output must be the core path")
        return
    attempt = _current_attempt(core, receipt)
    field = (
        "reviewTargetPath"
        if request.operation == "review-target"
        else "validationBundlePath"
    )
    expected = attempt.get(field)
    if request.output_path != expected:
        _raise("KIN-E-SCOPE", request.output_path, "output does not match the current attempt role")
    _validate_repo_output(root, request.output_path, manifest, closure_required=True)


def _validate_core_state(
    core: dict[str, Any], snapshots: Mapping[str, _ReadSnapshot]
) -> None:
    schema_payload = _repo_payload(snapshots, _SCHEMA_PATH, code="KIN-E-SCHEMA")
    schema = _mapping(
        _decode_canonical_bytes(schema_payload, _SCHEMA_PATH),
        _SCHEMA_PATH,
    )
    issues = validate_named_definition(schema, "coreData", core)
    if issues:
        issue = sorted(issues)[0]
        _raise(issue.code, issue.path, issue.message)
    semantic_issues = validate_core_records(core)
    if semantic_issues:
        issue = sorted(semantic_issues)[0]
        _raise(issue.code, issue.path, issue.message)
    review = _review_module()
    history_issues = review.validate_review_history(core)
    if history_issues:
        issue = sorted(history_issues)[0]
        _raise(issue.code, issue.path, issue.message)


def _validate_closure_files(
    core: Mapping[str, object],
    snapshots: Mapping[str, _ReadSnapshot],
    namespace: _NamespaceFingerprint,
    *,
    overlay: Mapping[str, bytes] | None = None,
) -> None:
    review = _review_module()
    attempts = [
        value
        for value in _list(core.get("reviewAttempts"), "core.reviewAttempts")
        if isinstance(value, dict)
    ]
    attempt_ids = [value.get("id") for value in attempts]
    if any(not isinstance(value, str) for value in attempt_ids) or len(
        set(attempt_ids)
    ) != len(attempt_ids):
        _raise("KIN-E-BUNDLE", "core.reviewAttempts", "attempt IDs are malformed or duplicated")
    artifact_values = [
        value
        for value in _list(
            core.get("reviewAttemptArtifacts"), "core.reviewAttemptArtifacts"
        )
        if isinstance(value, dict)
    ]
    artifact_ids = [value.get("attemptId") for value in artifact_values]
    if any(not isinstance(value, str) for value in artifact_ids) or len(
        set(artifact_ids)
    ) != len(artifact_ids):
        _raise(
            "KIN-E-BUNDLE",
            "core.reviewAttemptArtifacts",
            "artifact attempt IDs are malformed or duplicated",
        )
    if set(artifact_ids) != set(attempt_ids):
        _raise("KIN-E-BUNDLE", "core.reviewAttemptArtifacts", "attempt/artifact bijection is broken")
    artifacts = {value["attemptId"]: value for value in artifact_values}
    receipt_values = [
        value
        for value in _list(core.get("phaseReceipts"), "core.phaseReceipts")
        if isinstance(value, dict)
    ]
    receipt_ids = [value.get("id") for value in receipt_values]
    if any(not isinstance(value, str) for value in receipt_ids) or len(
        set(receipt_ids)
    ) != len(receipt_ids):
        _raise("KIN-E-BUNDLE", "core.phaseReceipts", "receipt IDs are malformed or duplicated")
    receipts = {value["id"]: value for value in receipt_values}
    attestation_values = [
        value
        for value in _list(core.get("reviewAttestations"), "core.reviewAttestations")
        if isinstance(value, dict)
    ]
    finding_values = [
        value
        for value in _list(core.get("reviewFindings"), "core.reviewFindings")
        if isinstance(value, dict)
    ]
    expected: dict[str, str] = {}

    def record_expected(relative: str, digest: str) -> None:
        if relative in expected:
            _raise("KIN-E-BUNDLE", relative, "closure path is referenced more than once")
        expected[relative] = digest

    for attempt in attempts:
        attempt_id = attempt.get("id")
        artifact = artifacts.get(attempt_id)
        if not isinstance(attempt_id, str) or not isinstance(artifact, dict):
            _raise("KIN-E-BUNDLE", "core.reviewAttemptArtifacts", "attempt/artifact bijection is broken")
        target_path = attempt.get("reviewTargetPath")
        logic_path = attempt.get("logicReviewPath")
        btj_path = attempt.get("btjReviewPath")
        bundle_path = attempt.get("validationBundlePath")
        if not all(isinstance(value, str) for value in (
            target_path, logic_path, btj_path, bundle_path
        )):
            _raise("KIN-E-BUNDLE", attempt_id, "attempt closure path is malformed")
        target_hash = artifact.get("reviewTargetSha256")
        if target_hash is not None:
            if not _is_raw_hash(target_hash):
                _raise("KIN-E-BUNDLE", target_path, "target artifact hash is malformed")
            record_expected(target_path, target_hash)
        has_review = False
        for id_field, hash_field, relative in (
            ("logicAttestationId", "logicReviewSha256", logic_path),
            ("btjAttestationId", "btjReviewSha256", btj_path),
        ):
            has_id = isinstance(attempt.get(id_field), str)
            review_hash = artifact.get(hash_field)
            has_hash = _is_raw_hash(review_hash)
            if has_id != has_hash:
                _raise("KIN-E-BUNDLE", relative, "review state/path/hash biconditional is broken")
            if has_hash:
                has_review = True
                record_expected(relative, str(review_hash))
        if (has_review or attempt.get("status") in {"FAILED", "ABANDONED", "PASSED"}) and target_hash is None:
            _raise("KIN-E-BUNDLE", target_path, "terminal/reviewed attempt requires a target")
        receipt = receipts.get(attempt.get("receiptId"))
        if (
            isinstance(receipt, dict)
            and receipt.get("status") == "VERIFIED"
            and receipt.get("reviewAttemptId") == attempt_id
        ):
            if receipt.get("validationBundlePath") != bundle_path or not _is_raw_hash(
                receipt.get("validationDigest")
            ):
                _raise("KIN-E-BUNDLE", bundle_path, "VERIFIED bundle receipt projection is malformed")
            record_expected(bundle_path, str(receipt["validationDigest"]))

    actual = {
        relative
        for relative, kind, _ in namespace.isolated
        if kind != "DIRECTORY"
    }
    overlay_values = dict(overlay or {})
    actual.update(
        relative
        for relative in overlay_values
        if _is_below(relative, _CLOSURE_ROOTS)
    )
    extra = sorted(actual - set(expected))
    if extra:
        _raise("KIN-E-BUNDLE", extra[0], "unreferenced closure file is present")
    missing = sorted(set(expected) - actual)
    if missing:
        _raise("KIN-E-BUNDLE", missing[0], "referenced closure file is absent")
    for relative, expected_hash in sorted(expected.items()):
        payload = overlay_values.get(relative)
        if payload is None:
            payload = _repo_payload(snapshots, relative, code="KIN-E-BUNDLE")
        if raw_hash(payload) != expected_hash:
            _raise("KIN-E-BUNDLE", relative, "closure file hash differs from its record")
        attempt = next(
            value
            for value in attempts
            if relative in {
                value.get("reviewTargetPath"),
                value.get("logicReviewPath"),
                value.get("btjReviewPath"),
                value.get("validationBundlePath"),
            }
        )
        artifact = artifacts[str(attempt["id"])]
        if relative == attempt.get("reviewTargetPath"):
            _mapping(_decode_canonical_bytes(payload, relative), relative)
            continue
        if relative == attempt.get("validationBundlePath"):
            _mapping(_decode_canonical_bytes(payload, relative), relative)
            continue
        attestation, findings = review._parse_review_document(payload, relative)
        pointer = (
            attempt.get("logicAttestationId")
            if relative == attempt.get("logicReviewPath")
            else attempt.get("btjAttestationId")
        )
        matches = [value for value in attestation_values if value.get("id") == pointer]
        if len(matches) != 1 or matches[0] != attestation:
            _raise("KIN-E-BUNDLE", relative, "review file does not equal its typed attestation")
        finding_ids = attestation.get("findingIds")
        if not isinstance(finding_ids, list):
            _raise("KIN-E-BUNDLE", relative, "review finding IDs are malformed")
        finding_index = {value.get("id"): value for value in finding_values}
        if len(finding_index) != len(finding_values) or findings != [
            finding_index.get(value) for value in finding_ids
        ]:
            _raise("KIN-E-BUNDLE", relative, "review file findings drifted from typed records")
        if attestation.get("reviewTargetDigest") != artifact.get("reviewTargetSha256"):
            _raise("KIN-E-BUNDLE", relative, "review does not bind the exact target digest")


def _external_path(
    root: Path,
    canonical_root: Path | None,
    value: Path,
    label: str,
) -> Path:
    lexical = Path(os.path.abspath(os.fspath(value)))
    try:
        lexical_metadata = lexical.lstat()
    except (OSError, RuntimeError):
        _raise("KIN-E-IO", label, "external input is unavailable")
    if stat.S_ISLNK(lexical_metadata.st_mode):
        _raise("KIN-E-PATH", label, "external input must not be a symlink")
    if not stat.S_ISREG(lexical_metadata.st_mode) or lexical_metadata.st_nlink != 1:
        _raise("KIN-E-PATH", label, "external input must be an ordinary file, not a symlink")
    for parent in lexical.parents:
        try:
            parent_metadata = parent.lstat()
        except OSError:
            _raise("KIN-E-IO", label, "external input parent is unavailable")
        if stat.S_ISLNK(parent_metadata.st_mode):
            try:
                container_metadata = parent.parent.lstat()
            except OSError:
                _raise("KIN-E-IO", label, "external input parent is unavailable")
            immutable_system_alias = (
                parent_metadata.st_uid == 0
                and container_metadata.st_uid == 0
                and stat.S_IMODE(container_metadata.st_mode) & 0o022 == 0
            )
            if not immutable_system_alias:
                _raise("KIN-E-PATH", label, "external input must not have a symlinked parent")
    try:
        resolved = lexical.resolve(strict=True)
        resolved_metadata = resolved.lstat()
    except (OSError, RuntimeError):
        _raise("KIN-E-IO", label, "external input is unavailable")
    if (
        (lexical_metadata.st_dev, lexical_metadata.st_ino)
        != (resolved_metadata.st_dev, resolved_metadata.st_ino)
    ):
        _raise("KIN-E-PATH", label, "external input resolution changed file identity")
    try:
        boundaries = [root.resolve(strict=True)]
    except (OSError, RuntimeError):
        _raise("KIN-E-CONCURRENT", "root", "repository root is unavailable")
    if canonical_root is not None:
        try:
            boundaries.append(canonical_root.resolve(strict=True))
        except (OSError, RuntimeError):
            _raise("KIN-E-CONCURRENT", "canonical-root", "canonical root is unavailable")
    for boundary in boundaries:
        try:
            resolved.relative_to(boundary)
        except ValueError:
            continue
        _raise("KIN-E-PATH", label, "candidate input must be outside both repository worktrees")
    return resolved


def _external_inputs(
    root: Path, request: RenderTransactionRequest
) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for name in (
        "logic_review_input",
        "btj_review_input",
        "finding_dispositions_input",
    ):
        value = getattr(request, name)
        if value is not None:
            if request.canonical_root is None:
                _raise(
                    "KIN-E-CLI",
                    "canonical-root",
                    "external intake requires the canonical worktree boundary",
                )
            result[name] = _external_path(
                root, request.canonical_root, value, name.replace("_", "-")
            )
    return result


def _snapshot_file(path: Path, label: str) -> _ReadSnapshot:
    identities: list[tuple[str, int, int]] = []
    for parent in path.parents:
        try:
            parent_metadata = parent.lstat()
        except FileNotFoundError:
            continue
        except OSError:
            _raise("KIN-E-CONCURRENT", label, "read-set parent is unreadable")
        if stat.S_ISLNK(parent_metadata.st_mode):
            _raise("KIN-E-PATH", label, "read-set path has a symlinked parent")
        identities.append((str(parent), parent_metadata.st_dev, parent_metadata.st_ino))
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return _ReadSnapshot(
            path,
            label,
            "ABSENT",
            None,
            None,
            None,
            tuple(identities),
        )
    except OSError:
        _raise("KIN-E-CONCURRENT", label, "read-set member is unreadable")
    if stat.S_ISLNK(metadata.st_mode):
        try:
            target = os.readlink(path).encode("utf-8", errors="strict")
        except (OSError, UnicodeError):
            _raise("KIN-E-CONCURRENT", label, "symlink read-set member is unreadable")
        return _ReadSnapshot(
            path,
            label,
            "SYMLINK",
            raw_hash(target),
            target,
            None,
            tuple(identities),
        )
    if not stat.S_ISREG(metadata.st_mode):
        _raise("KIN-E-CONCURRENT", label, "read-set member is not an ordinary file")
    if metadata.st_nlink != 1:
        _raise("KIN-E-CONCURRENT", label, "read-set member must have exactly one link")
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(descriptor)
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except OSError:
        _raise("KIN-E-CONCURRENT", label, "read-set member is unreadable")
    if (
        not stat.S_ISREG(after.st_mode)
        or after.st_nlink != 1
        or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
    ):
        _raise("KIN-E-CONCURRENT", label, "read-set member changed during snapshot")
    try:
        current = path.lstat()
    except OSError:
        _raise("KIN-E-CONCURRENT", label, "read-set member changed during snapshot")
    if (
        not stat.S_ISREG(current.st_mode)
        or current.st_nlink != 1
        or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)
    ):
        _raise("KIN-E-CONCURRENT", label, "read-set member changed during snapshot")
    payload = b"".join(chunks)
    return _ReadSnapshot(
        path,
        label,
        "FILE",
        raw_hash(payload),
        payload,
        stat.S_IMODE(after.st_mode),
        tuple(identities),
    )


def _repo_read_paths(
    core: Mapping[str, object],
    manifest: Mapping[str, object],
    receipt: Mapping[str, object],
    request: RenderTransactionRequest,
) -> set[str]:
    result = {
        request.core_path,
        request.output_path,
        _SCHEMA_PATH,
        _LEDGER_PATH,
    }
    for value in _list(core.get("phaseReceipts"), "core.phaseReceipts"):
        if isinstance(value, dict) and isinstance(value.get("path"), str):
            result.add(value["path"])
    if request.phase == "C":
        result.add(_PUBLIC_QUEUE_PATH)
    for value in _list(core.get("sources"), "core.sources"):
        if isinstance(value, dict) and isinstance(value.get("path"), str):
            result.add(value["path"])
    for field in ("candidateFiles", "includedFiles", "finalFiles"):
        for value in _list(manifest.get(field), f"manifest.{field}"):
            if isinstance(value, dict) and isinstance(value.get("path"), str):
                result.add(value["path"])
    for relative in _path_values(
        manifest.get("inventoryReviewPaths"), "manifest.inventoryReviewPaths"
    ):
        result.add(relative)
    snapshots = manifest.get("protectedTreeSnapshots")
    if isinstance(snapshots, dict):
        for worktree in ("isolated", "canonical"):
            for value in _list(
                snapshots.get(worktree),
                f"manifest.protectedTreeSnapshots.{worktree}",
            ):
                if isinstance(value, dict) and isinstance(value.get("path"), str):
                    result.add(value["path"])
    for value in _list(
        manifest.get("protectedProvenance"), "manifest.protectedProvenance"
    ):
        if isinstance(value, dict) and isinstance(value.get("path"), str):
            result.add(value["path"])
    allowances = manifest.get("allowedPreexistingUntracked")
    if isinstance(allowances, dict):
        for worktree in ("isolated", "canonical"):
            for value in _list(
                allowances.get(worktree),
                f"manifest.allowedPreexistingUntracked.{worktree}",
            ):
                if isinstance(value, dict) and isinstance(value.get("path"), str):
                    result.add(value["path"])
    for value in _list(core.get("reviewAttempts"), "core.reviewAttempts"):
        if not isinstance(value, dict):
            continue
        for field in (
            "reviewTargetPath",
            "logicReviewPath",
            "btjReviewPath",
            "validationBundlePath",
        ):
            relative = value.get(field)
            if isinstance(relative, str):
                result.add(relative)
    return result


def _freeze_read_set(
    root: Path,
    core: Mapping[str, object],
    manifest: Mapping[str, object],
    receipt: Mapping[str, object],
    request: RenderTransactionRequest,
    external: Mapping[str, Path],
) -> dict[str, _ReadSnapshot]:
    snapshots: dict[str, _ReadSnapshot] = {}
    canonical: Path | None = None
    if request.canonical_root is not None:
        try:
            canonical = request.canonical_root.resolve(strict=True)
        except (OSError, RuntimeError):
            _raise("KIN-E-CONCURRENT", "canonical-root", "canonical root is unavailable")
    for relative in sorted(_repo_read_paths(core, manifest, receipt, request)):
        path = _safe_repo_value(root, relative)
        snapshots[f"repo:{relative}"] = _snapshot_file(path, relative)
        if canonical is not None:
            canonical_path = _safe_repo_value(canonical, relative)
            snapshots[f"canonical:{relative}"] = _snapshot_file(
                canonical_path, f"canonical:{relative}"
            )
    for name, path in sorted(external.items()):
        snapshots[f"external:{name}"] = _snapshot_file(path, name)
    return snapshots


def _add_read_snapshot(
    snapshots: dict[str, _ReadSnapshot], key: str, path: Path, label: str
) -> None:
    if key in snapshots:
        _raise("KIN-E-CONCURRENT", label, "read-set key was duplicated")
    snapshots[key] = _snapshot_file(path, label)


def _add_repo_snapshot(
    root: Path,
    canonical_root: Path | None,
    snapshots: dict[str, _ReadSnapshot],
    relative: str,
) -> None:
    key = f"repo:{relative}"
    if key not in snapshots:
        snapshots[key] = _snapshot_file(_safe_repo_value(root, relative), relative)
    if canonical_root is None:
        return
    try:
        canonical = canonical_root.resolve(strict=True)
    except (OSError, RuntimeError):
        _raise("KIN-E-CONCURRENT", "canonical-root", "canonical root is unavailable")
    canonical_key = f"canonical:{relative}"
    if canonical_key not in snapshots:
        snapshots[canonical_key] = _snapshot_file(
            _safe_repo_value(canonical, relative),
            f"canonical:{relative}",
        )


def _snapshot_payload(
    snapshots: Mapping[str, _ReadSnapshot],
    key: str,
    *,
    code: str,
    label: str,
) -> bytes:
    snapshot = snapshots.get(key)
    if snapshot is None or snapshot.kind != "FILE" or snapshot.payload is None:
        _raise(code, label, "required frozen input is not an ordinary file")
    return snapshot.payload


def _repo_payload(
    snapshots: Mapping[str, _ReadSnapshot], relative: str, *, code: str
) -> bytes:
    return _snapshot_payload(
        snapshots,
        f"repo:{relative}",
        code=code,
        label=relative,
    )


def _git_state_signature(
    state: GitState, ignored_untracked: frozenset[str]
) -> tuple[object, ...]:
    untracked = tuple(
        (record.path, record.kind, record.sha256)
        for record in state.untracked_records
        if record.path not in ignored_untracked
    )
    return (
        str(state.root),
        state.head,
        state.branch,
        str(state.common_dir),
        state.base_commit,
        state.committed_paths,
        state.staged_paths,
        state.unstaged_paths,
        state.unrepresentable_mode_paths,
        state.noncanonical_index_paths,
        untracked,
    )


def _capture_git_fingerprint(
    root: Path,
    request: RenderTransactionRequest,
    manifest: Mapping[str, object],
    *,
    ignored_untracked: frozenset[str] = frozenset(),
) -> _GitFingerprint:
    base_commit = manifest.get("baseCommit")
    if not isinstance(base_commit, str):
        _raise("KIN-E-MANIFEST", "manifest.baseCommit", "base commit is malformed")
    isolated_state = inspect_git_state(root, base_commit)
    if not isinstance(isolated_state, GitState):
        _raise("KIN-E-CONCURRENT", "git", "Git state has an invalid runtime type")
    canonical_state: GitState | None = None
    if request.canonical_root is not None:
        try:
            canonical_root = request.canonical_root.resolve(strict=True)
        except (OSError, RuntimeError):
            _raise("KIN-E-CONCURRENT", "canonical-root", "canonical root is unavailable")
        value = inspect_git_state(canonical_root, base_commit)
        if not isinstance(value, GitState):
            _raise("KIN-E-CONCURRENT", "git", "canonical Git state has an invalid runtime type")
        canonical_state = value
    worktrees = tuple(
        (str(record.root), record.head, record.branch)
        for record in _list_worktrees(root)
    )
    base_ref_commit = (
        _resolve_commit(
            root,
            base_commit if request.base_ref == "MANIFEST" else request.base_ref,
        )
        if request.base_ref is not None
        else None
    )
    return _GitFingerprint(
        isolated_signature=_git_state_signature(isolated_state, ignored_untracked),
        canonical_signature=(
            _git_state_signature(canonical_state, frozenset())
            if canonical_state is not None
            else None
        ),
        worktrees=worktrees,
        base_ref_commit=base_ref_commit,
        isolated_state=isolated_state,
    )


def _namespace_entries(
    root: Path,
    *,
    ignored: frozenset[Path] = frozenset(),
) -> tuple[tuple[str, str, str | None], ...]:
    values: list[tuple[str, str, str | None]] = []
    resolved_root = root.resolve(strict=True)
    for relative_root in _CLOSURE_ROOTS:
        directory = _safe_repo_value(resolved_root, relative_root)
        try:
            metadata = directory.lstat()
        except FileNotFoundError:
            continue
        except OSError:
            _raise("KIN-E-CONCURRENT", relative_root, "closure namespace is unreadable")
        if stat.S_ISLNK(metadata.st_mode):
            target = os.readlink(directory).encode("utf-8", errors="strict")
            values.append((relative_root, "SYMLINK", raw_hash(target)))
            continue
        if not stat.S_ISDIR(metadata.st_mode):
            _raise("KIN-E-BUNDLE", relative_root, "closure namespace is not a directory")
        if directory not in ignored:
            values.append((relative_root, "DIRECTORY", None))
        for parent, directory_names, file_names in os.walk(
            directory, topdown=True, followlinks=False
        ):
            parent_path = Path(parent)
            for name in sorted(list(directory_names)):
                candidate = parent_path / name
                relative = candidate.relative_to(resolved_root).as_posix()
                candidate_metadata = candidate.lstat()
                if stat.S_ISLNK(candidate_metadata.st_mode):
                    target = os.readlink(candidate).encode("utf-8", errors="strict")
                    values.append((relative, "SYMLINK", raw_hash(target)))
                    directory_names.remove(name)
                elif stat.S_ISDIR(candidate_metadata.st_mode):
                    if candidate not in ignored:
                        values.append((relative, "DIRECTORY", None))
                else:
                    _raise("KIN-E-BUNDLE", relative, "closure namespace entry is malformed")
            for name in sorted(file_names):
                candidate = parent_path / name
                if candidate in ignored:
                    continue
                relative = candidate.relative_to(resolved_root).as_posix()
                snapshot = _snapshot_file(candidate, relative)
                if snapshot.kind not in {"FILE", "SYMLINK"}:
                    _raise("KIN-E-BUNDLE", relative, "closure namespace entry is malformed")
                values.append((relative, snapshot.kind, snapshot.digest))
    return tuple(sorted(values))


def _capture_namespace_fingerprint(
    root: Path,
    request: RenderTransactionRequest,
    *,
    ignored: frozenset[Path] = frozenset(),
) -> _NamespaceFingerprint:
    canonical: tuple[tuple[str, str, str | None], ...] | None = None
    if request.canonical_root is not None:
        try:
            canonical_root = request.canonical_root.resolve(strict=True)
        except (OSError, RuntimeError):
            _raise("KIN-E-CONCURRENT", "canonical-root", "canonical root is unavailable")
        canonical = _namespace_entries(canonical_root)
    return _NamespaceFingerprint(
        isolated=_namespace_entries(root, ignored=ignored),
        canonical=canonical,
    )


def _recheck_read_set(
    root: Path,
    request: RenderTransactionRequest,
    snapshots: Mapping[str, _ReadSnapshot],
    git_fingerprint: _GitFingerprint,
    namespace_fingerprint: _NamespaceFingerprint,
    *,
    ignored_untracked: frozenset[str] = frozenset(),
    ignored_namespace: frozenset[Path] = frozenset(),
) -> None:
    _check_head_core_cas(
        root,
        request.core_path,
        request.expected_head,
        request.expected_core_sha256,
    )
    for key in sorted(snapshots):
        expected = snapshots[key]
        current = _snapshot_file(expected.path, expected.label)
        parent_map = {
            path: (device, inode)
            for path, device, inode in current.parent_identities
        }
        parents_changed = any(
            parent_map.get(path) != (device, inode)
            for path, device, inode in expected.parent_identities
        )
        if (
            current.kind != expected.kind
            or current.digest != expected.digest
            or current.mode != expected.mode
            or parents_changed
        ):
            _raise(
                "KIN-E-CONCURRENT",
                expected.label,
                "read-set member changed before repository replacement",
            )
    current_git = _capture_git_fingerprint(
        root,
        request,
        _selected_manifest(_load_core_locked(root, request.core_path), request.phase),
        ignored_untracked=ignored_untracked,
    )
    if current_git != git_fingerprint:
        _raise(
            "KIN-E-CONCURRENT",
            "git",
            "Git state, worktree registry, or base reference changed before replacement",
        )
    current_namespace = _capture_namespace_fingerprint(
        root,
        request,
        ignored=ignored_namespace,
    )
    if current_namespace != namespace_fingerprint:
        _raise(
            "KIN-E-CONCURRENT",
            "closure-namespace",
            "closure namespace changed before repository replacement",
        )


def _receipt_bytes(
    current_payload: bytes,
    current_receipt: Mapping[str, object],
    prospective_receipt: Mapping[str, object],
    relative: str,
) -> bytes:
    synchronized = synchronize_receipt_markdown(
        current_payload,
        current_receipt,
        path=relative,
    )
    if synchronized.issues:
        issue = synchronized.issues[0]
        _raise(issue.code, issue.path, issue.message)
    records = [
        record
        for record in synchronized.records
        if record.role == "kintsugi-receipt"
    ]
    if len(records) != 1:
        _raise("KIN-E-LEDGER", relative, "receipt must contain exactly one machine fence")
    record = records[0]
    rendered = (
        current_payload[:record.json_start]
        + canonical_json_bytes(dict(prospective_receipt))
        + current_payload[record.json_end:]
    )
    verified = synchronize_receipt_markdown(
        rendered,
        prospective_receipt,
        path=relative,
    )
    if verified.issues:
        issue = verified.issues[0]
        _raise(issue.code, issue.path, issue.message)
    if verified.narrative_raw_sha256 != synchronized.narrative_raw_sha256:
        _raise("KIN-E-RECEIPT", relative, "renderer changed receipt narrative bytes")
    return rendered


def _disposition_input(
    payload: bytes | None, label: str
) -> list[dict[str, object]] | None:
    if payload is None:
        return None
    value = _decode_canonical_bytes(payload, label)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        _raise("KIN-E-CANONICAL", label, "finding dispositions must be a canonical object array")
    return copy.deepcopy(value)


def _freeze_outputs(
    root: Path,
    request: RenderTransactionRequest,
    core: dict[str, Any],
    receipt: dict[str, Any],
    common_dir: Path,
    snapshots: dict[str, _ReadSnapshot],
    git_fingerprint: _GitFingerprint,
) -> tuple[list[_Output], Path]:
    canonical_root = request.canonical_root
    base_ref = request.base_ref
    assert canonical_root is not None and base_ref is not None
    disposition_snapshot = snapshots.get("external:finding_dispositions_input")
    dispositions = _disposition_input(
        (
            disposition_snapshot.payload
            if disposition_snapshot is not None
            and disposition_snapshot.kind == "FILE"
            else None
        ),
        "finding-dispositions-input",
    )
    for disposition in dispositions or []:
        evidence_files = disposition.get("evidenceFiles")
        if not isinstance(evidence_files, list):
            continue
        for evidence in evidence_files:
            if not isinstance(evidence, dict) or not isinstance(evidence.get("path"), str):
                continue
            _add_repo_snapshot(
                root,
                canonical_root,
                snapshots,
                evidence["path"],
            )

    plan: AttemptPlan = _plan_next_attempt(
        root,
        core,
        request.phase,
        str(receipt.get("id")),
    )
    if plan.predecessor_id is not None:
        _validate_predecessor_fence(
            root,
            core,
            request.phase,
            str(receipt.get("id")),
            request.core_path,
        )
    for relative in plan.paths:
        snapshot = _snapshot_file(_safe_repo_value(root, relative), relative)
        if snapshot.kind != "ABSENT":
            _raise(
                "KIN-E-CONCURRENT",
                relative,
                "new attempt closure path already exists",
            )
        key = f"repo:{relative}"
        existing = snapshots.get(key)
        if existing is not None and existing != snapshot:
            _raise("KIN-E-CONCURRENT", relative, "closure path snapshot disagrees")
        snapshots[key] = snapshot
        canonical_path = _safe_repo_value(canonical_root, relative)
        canonical_snapshot = _snapshot_file(
            canonical_path, f"canonical:{relative}"
        )
        if canonical_snapshot.kind != "ABSENT":
            _raise(
                "KIN-E-CONCURRENT",
                relative,
                "new attempt closure path already exists in the canonical worktree",
            )
        snapshots[f"canonical:{relative}"] = canonical_snapshot
    reservation = _reserve_attempt_id(
        common_dir,
        plan,
        request.expected_head,
        request.expected_core_sha256,
    )
    prospective = _freeze_manifest_value_with_plan(
        root,
        canonical_root,
        core,
        request.phase,
        base_ref,
        True,
        dispositions,
        attempt_plan=plan,
        expected_head=request.expected_head,
        expected_core_sha256=request.expected_core_sha256,
        read_overrides={
            key.removeprefix("repo:"): (snapshot.kind, snapshot.payload)
            for key, snapshot in snapshots.items()
            if key.startswith("repo:")
            and snapshot.kind in {"FILE", "SYMLINK"}
            and snapshot.payload is not None
        },
        frozen_git_state=git_fingerprint.isolated_state,
    )
    prospective_receipt = _selected_receipt(prospective, request.phase)
    prospective_attempt = _current_attempt(prospective, prospective_receipt)
    if prospective_attempt.get("id") != plan.id:
        _raise("KIN-E-CONCURRENT", "attempt", "freeze plan changed after reservation")

    receipt_relative = receipt.get("path")
    if not isinstance(receipt_relative, str):
        _raise("KIN-E-RECEIPT", "receipt.path", "receipt path is malformed")
    current_receipt_bytes = _repo_payload(
        snapshots,
        receipt_relative,
        code="KIN-E-RECEIPT",
    )
    return [
        _Output(request.core_path, canonical_json_bytes(prospective)),
        _Output(
            receipt_relative,
            _receipt_bytes(
                current_receipt_bytes,
                receipt,
                prospective_receipt,
                receipt_relative,
            ),
        ),
    ], reservation


def _review_module() -> Any:
    try:
        from . import review
    except ImportError:
        _raise("KIN-E-CLI", "review", "review kernel is unavailable")
    return review


def _control_values(
    snapshots: Mapping[str, _ReadSnapshot],
    core: Mapping[str, object],
    receipt: Mapping[str, object],
    *,
    receipt_bytes: bytes | None = None,
    ledger_bytes: bytes | None = None,
) -> tuple[dict[str, object], bytes, bytes, bytes, list[dict[str, object]]]:
    schema_bytes = _repo_payload(
        snapshots,
        _SCHEMA_PATH,
        code="KIN-E-BUNDLE",
    )
    schema = _mapping(
        _decode_canonical_bytes(schema_bytes, _SCHEMA_PATH),
        _SCHEMA_PATH,
    )
    if ledger_bytes is None:
        ledger_bytes = _repo_payload(
            snapshots,
            _LEDGER_PATH,
            code="KIN-E-BUNDLE",
        )
    seams = [
        value
        for value in _list(core.get("seams"), "core.seams")
        if isinstance(value, dict)
    ]
    ledger_sync = synchronize_ledger_markdown(
        ledger_bytes,
        seams,
        path=_LEDGER_PATH,
    )
    if ledger_sync.issues:
        issue = ledger_sync.issues[0]
        _raise(issue.code, issue.path, issue.message)
    sections = [
        {
            "id": section.id,
            "narrativeRawSha256": section.narrative_raw_sha256,
            "seamProjection": copy.deepcopy(section.seam_projection),
        }
        for section in ledger_sync.sections
    ]
    receipt_relative = receipt.get("path")
    if not isinstance(receipt_relative, str):
        _raise("KIN-E-RECEIPT", "receipt.path", "receipt path is malformed")
    if receipt_bytes is None:
        receipt_bytes = _repo_payload(
            snapshots,
            receipt_relative,
            code="KIN-E-BUNDLE",
        )
    return schema, schema_bytes, ledger_bytes, receipt_bytes, sections


def _semantic_paths(
    state: GitState,
    manifest: dict[str, Any],
) -> list[str]:
    closure = set(_path_values(
        manifest.get("closureOnlyPaths"), "manifest.closureOnlyPaths"
    ))
    return _semantic_diff_paths(state, manifest, closure)


def _review_target_value(
    snapshots: Mapping[str, _ReadSnapshot],
    git_state: GitState,
    core: dict[str, Any],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    attempt: dict[str, Any],
) -> dict[str, object]:
    review = _review_module()
    schema, schema_bytes, ledger_bytes, receipt_bytes, sections = _control_values(
        snapshots, core, receipt
    )
    return review.build_review_target_from_control_bytes(
        schema,
        core,
        phase=str(attempt.get("phase")),
        attempt_id=str(attempt.get("id")),
        ledger_sections=sections,
        semantic_diff_paths=_semantic_paths(git_state, manifest),
        schema_bytes=schema_bytes,
        ledger_bytes=ledger_bytes,
        receipt_bytes=receipt_bytes,
    )


def _read_target(
    snapshots: Mapping[str, _ReadSnapshot],
    core: Mapping[str, object],
    attempt: Mapping[str, object],
) -> tuple[dict[str, object], bytes]:
    relative = attempt.get("reviewTargetPath")
    if not isinstance(relative, str):
        _raise("KIN-E-BUNDLE", "attempt.reviewTargetPath", "target path is malformed")
    payload = _repo_payload(
        snapshots,
        relative,
        code="KIN-E-BUNDLE",
    )
    target = _mapping(_decode_canonical_bytes(payload, relative), relative)
    artifact = _attempt_artifact(core, str(attempt.get("id")))
    if artifact.get("reviewTargetSha256") != raw_hash(payload):
        _raise("KIN-E-BUNDLE", relative, "target bytes do not match the attempt artifact")
    return target, payload


def _public_queue(
    snapshots: Mapping[str, _ReadSnapshot], phase: str
) -> dict[str, object] | None:
    if phase != "C":
        return None
    payload = _repo_payload(
        snapshots,
        _PUBLIC_QUEUE_PATH,
        code="KIN-E-QUEUE",
    )
    return _mapping(
        _decode_canonical_bytes(payload, _PUBLIC_QUEUE_PATH),
        _PUBLIC_QUEUE_PATH,
    )


def _bundle_value(
    snapshots: Mapping[str, _ReadSnapshot],
    core: dict[str, Any],
    receipt: dict[str, Any],
    attempt: dict[str, Any],
    target: dict[str, object],
    *,
    receipt_bytes: bytes | None = None,
    ledger_bytes: bytes | None = None,
) -> dict[str, object]:
    review = _review_module()
    schema, schema_bytes, ledger_bytes, selected_receipt_bytes, _ = _control_values(
        snapshots,
        core,
        receipt,
        receipt_bytes=receipt_bytes,
        ledger_bytes=ledger_bytes,
    )
    bundle = review.build_validation_bundle_from_control_bytes(
        schema,
        core,
        phase=str(attempt.get("phase")),
        attempt_id=str(attempt.get("id")),
        review_target=target,
        public_queue=_public_queue(snapshots, str(attempt.get("phase"))),
        schema_bytes=schema_bytes,
        ledger_bytes=ledger_bytes,
        receipt_bytes=selected_receipt_bytes,
    )
    issues = review.validate_validation_bundle(
        schema,
        core,
        bundle,
        phase=str(attempt.get("phase")),
        attempt_id=str(attempt.get("id")),
        review_target=target,
        public_queue=_public_queue(snapshots, str(attempt.get("phase"))),
    )
    if issues:
        issue = issues[0]
        _raise(issue.code, issue.path, issue.message)
    return bundle


def _review_target_outputs(
    request: RenderTransactionRequest,
    core: dict[str, Any],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    snapshots: Mapping[str, _ReadSnapshot],
    git_state: GitState,
) -> list[_Output]:
    review = _review_module()
    attempt = _current_attempt(core, receipt)
    if attempt.get("status") != "PENDING":
        _raise("KIN-E-STATE", "attempt.status", "TARGET_READY requires a PENDING attempt")
    target = _review_target_value(
        snapshots,
        git_state,
        core,
        manifest,
        receipt,
        attempt,
    )
    target_bytes = canonical_json_bytes(target)
    target_relative = str(attempt.get("reviewTargetPath"))
    target_snapshot = snapshots.get(f"repo:{target_relative}")
    if target_snapshot is None:
        _raise("KIN-E-CONCURRENT", target_relative, "target is absent from the frozen read set")
    if target_snapshot.kind == "FILE":
        existing = target_snapshot.payload
        if existing != target_bytes:
            _raise("KIN-E-BUNDLE", target_relative, "immutable review target drifted")
    elif target_snapshot.kind != "ABSENT":
        _raise("KIN-E-BUNDLE", target_relative, "immutable review target is not a regular file")
    artifact = _attempt_artifact(core, str(attempt.get("id")))
    expected_hash = raw_hash(target_bytes)
    recorded_hash = artifact.get("reviewTargetSha256")
    if target_snapshot.kind == "FILE" and recorded_hash is None:
        _raise(
            "KIN-E-BUNDLE",
            target_relative,
            "unrecorded canonical target cannot be adopted as a retry",
        )
    if recorded_hash == expected_hash:
        prospective = copy.deepcopy(core)
    else:
        prospective = review.transition_core_value(
            core,
            phase=request.phase,
            stage="TARGET_READY",
            review_documents=[target_bytes],
        )
    outputs: list[_Output] = []
    if prospective != core:
        outputs.append(_Output(request.core_path, canonical_json_bytes(prospective)))
    if target_snapshot.kind == "ABSENT":
        outputs.append(_Output(target_relative, target_bytes))
    return outputs


def _review_documents(
    snapshots: Mapping[str, _ReadSnapshot],
) -> tuple[list[bytes], list[tuple[str, bytes]]]:
    documents: list[bytes] = []
    typed: list[tuple[str, bytes]] = []
    for name in ("logic_review_input", "btj_review_input"):
        snapshot = snapshots.get(f"external:{name}")
        if snapshot is None:
            continue
        if snapshot.kind != "FILE" or snapshot.payload is None:
            _raise("KIN-E-IO", name, "review candidate is not a frozen regular file")
        payload = snapshot.payload
        values = extract_fenced_json(payload, "kintsugi-review")
        findings = extract_fenced_json(payload, "kintsugi-review-findings")
        if len(values) != 1 or len(findings) != 1 or not isinstance(values[0], dict):
            _raise("KIN-E-REVIEW", name, "review candidate has an invalid fence set")
        kind = values[0].get("kind")
        expected = "LOGIC" if name == "logic_review_input" else "BTJ"
        if kind != expected:
            _raise("KIN-E-REVIEW", name, "review candidate kind disagrees with its input slot")
        documents.append(payload)
        typed.append((expected, payload))
    return documents, typed


def _prospective_receipt_output(
    snapshots: Mapping[str, _ReadSnapshot],
    current_receipt: dict[str, Any],
    prospective_receipt: dict[str, Any],
) -> _Output | None:
    if current_receipt == prospective_receipt:
        return None
    relative = current_receipt.get("path")
    if not isinstance(relative, str) or prospective_receipt.get("path") != relative:
        _raise("KIN-E-RECEIPT", "receipt.path", "transition changed receipt identity")
    current_bytes = _repo_payload(
        snapshots,
        relative,
        code="KIN-E-RECEIPT",
    )
    return _Output(
        relative,
        _receipt_bytes(current_bytes, current_receipt, prospective_receipt, relative),
    )


def _prospective_ledger_output(
    snapshots: Mapping[str, _ReadSnapshot],
    current_core: Mapping[str, object],
    prospective_core: Mapping[str, object],
) -> _Output | None:
    current_seams = [
        value
        for value in _list(current_core.get("seams"), "core.seams")
        if isinstance(value, dict)
    ]
    prospective_seams = [
        value
        for value in _list(prospective_core.get("seams"), "prospective.seams")
        if isinstance(value, dict)
    ]
    if current_seams == prospective_seams:
        return None
    current_by_id = {value.get("id"): value for value in current_seams}
    prospective_by_id = {value.get("id"): value for value in prospective_seams}
    if set(current_by_id) != set(prospective_by_id):
        _raise("KIN-E-STATE", "core.seams", "transition changed the ledger seam identity set")
    current_bytes = _repo_payload(
        snapshots,
        _LEDGER_PATH,
        code="KIN-E-LEDGER",
    )
    synchronized = synchronize_ledger_markdown(
        current_bytes,
        current_seams,
        path=_LEDGER_PATH,
    )
    if synchronized.issues:
        issue = synchronized.issues[0]
        _raise(issue.code, issue.path, issue.message)
    rendered = bytearray(synchronized.preamble.raw)
    for section in synchronized.sections:
        seam = prospective_by_id.get(section.id)
        if seam is None:
            _raise("KIN-E-LEDGER", section.id, "prospective seam is absent from the ledger")
        rendered.extend(section.prefix)
        rendered.extend(b"```json kintsugi-seam\n")
        rendered.extend(canonical_json_bytes(seam))
        rendered.extend(b"```\n")
        rendered.extend(section.suffix)
    payload = bytes(rendered)
    verified = synchronize_ledger_markdown(
        payload,
        prospective_seams,
        path=_LEDGER_PATH,
    )
    if verified.issues:
        issue = verified.issues[0]
        _raise(issue.code, issue.path, issue.message)
    if verified.preamble.raw != synchronized.preamble.raw:
        _raise("KIN-E-LEDGER", _LEDGER_PATH, "renderer changed ledger preamble bytes")
    before_narratives = {
        section.id: section.narrative_raw_sha256
        for section in synchronized.sections
    }
    after_narratives = {
        section.id: section.narrative_raw_sha256
        for section in verified.sections
    }
    if before_narratives != after_narratives:
        _raise("KIN-E-LEDGER", _LEDGER_PATH, "renderer changed ledger narrative bytes")
    return _Output(_LEDGER_PATH, payload)


def _transition_outputs(
    request: RenderTransactionRequest,
    core: dict[str, Any],
    receipt: dict[str, Any],
    snapshots: Mapping[str, _ReadSnapshot],
) -> list[_Output]:
    review = _review_module()
    attempt = _current_attempt(core, receipt)
    target, _ = _read_target(snapshots, core, attempt)
    documents, typed_documents = _review_documents(snapshots)
    stage = request.stage
    assert stage is not None

    if stage == "VERIFIED":
        if documents:
            _raise("KIN-E-CLI", "review-input", "VERIFIED accepts no review candidates")
        bundle = _bundle_value(snapshots, core, receipt, attempt, target)
        bundle_bytes = canonical_json_bytes(bundle)
        prospective = review.transition_core_value(
            core,
            phase=request.phase,
            stage=stage,
            review_documents=[bundle_bytes],
        )
    else:
        if stage == "COMPLETE":
            persisted_ids = [
                value
                for value in (
                    attempt.get("logicAttestationId"),
                    attempt.get("btjAttestationId"),
                )
                if isinstance(value, str)
            ]
            if len(persisted_ids) != 1 or len(documents) != 1:
                _raise(
                    "KIN-E-STATE",
                    "COMPLETE",
                    "COMPLETE requires one persisted PASS and one new independent PASS",
                )
        prospective = review.transition_core_value(
            core,
            phase=request.phase,
            stage=stage,
            review_documents=documents,
            abandon_reason=request.abandon_reason,
        )
        bundle = None
        bundle_bytes = None

    prospective_receipt = _selected_receipt(prospective, request.phase)
    outputs = [_Output(request.core_path, canonical_json_bytes(prospective))]
    for kind, payload in typed_documents:
        field = "logicReviewPath" if kind == "LOGIC" else "btjReviewPath"
        relative = attempt.get(field)
        if not isinstance(relative, str):
            _raise("KIN-E-REVIEW", field, "derived review path is malformed")
        destination_snapshot = snapshots.get(f"repo:{relative}")
        if destination_snapshot is None or destination_snapshot.kind != "ABSENT":
            _raise("KIN-E-REVIEW", relative, "canonical review cannot be overwritten")
        outputs.append(_Output(relative, payload))

    receipt_output = _prospective_receipt_output(
        snapshots, receipt, prospective_receipt
    )
    if receipt_output is not None:
        outputs.append(receipt_output)
    ledger_output = _prospective_ledger_output(snapshots, core, prospective)
    if ledger_output is not None:
        outputs.append(ledger_output)

    if stage == "COMPLETE":
        # COMPLETE is licensed only when the complete prospective VERIFIED
        # bundle can be built against the staged receipt fence in memory.
        prospective_attempt = _current_attempt(prospective, prospective_receipt)
        staged_receipt = (
            receipt_output.payload
            if receipt_output is not None
            else _repo_payload(
                snapshots,
                str(receipt.get("path")),
                code="KIN-E-RECEIPT",
            )
        )
        _bundle_value(
            snapshots,
            prospective,
            prospective_receipt,
            prospective_attempt,
            target,
            receipt_bytes=staged_receipt,
            ledger_bytes=(ledger_output.payload if ledger_output is not None else None),
        )
    elif stage == "VERIFIED":
        assert bundle is not None and bundle_bytes is not None
        bundle_relative = attempt.get("validationBundlePath")
        if not isinstance(bundle_relative, str):
            _raise("KIN-E-BUNDLE", "attempt.validationBundlePath", "bundle path is malformed")
        destination_snapshot = snapshots.get(f"repo:{bundle_relative}")
        if destination_snapshot is None or destination_snapshot.kind != "ABSENT":
            _raise("KIN-E-BUNDLE", bundle_relative, "validation bundle is immutable")
        outputs.append(_Output(bundle_relative, bundle_bytes))
    return outputs


def _preflight_bundle(
    request: RenderTransactionRequest,
    core: dict[str, Any],
    receipt: dict[str, Any],
    snapshots: Mapping[str, _ReadSnapshot],
) -> None:
    attempt = _current_attempt(core, receipt)
    if receipt.get("status") != "COMPLETE" or attempt.get("status") != "PASSED":
        _raise(
            "KIN-E-STATE",
            "bundle",
            "standalone bundle preflight requires PASSED plus receipt COMPLETE",
        )
    relative = attempt.get("validationBundlePath")
    if not isinstance(relative, str) or request.output_path != relative:
        _raise("KIN-E-SCOPE", request.output_path, "bundle output role is invalid")
    destination_snapshot = snapshots.get(f"repo:{relative}")
    if destination_snapshot is None or destination_snapshot.kind != "ABSENT":
        _raise("KIN-E-BUNDLE", relative, "standalone bundle never overwrites canonical bytes")
    target, _ = _read_target(snapshots, core, attempt)
    _bundle_value(snapshots, core, receipt, attempt, target)


def _ensure_parent_directories(root: Path, relative: str) -> list[Path]:
    pure = PurePosixPath(relative)
    current = root.resolve(strict=True)
    created: list[Path] = []
    for part in pure.parts[:-1]:
        candidate = current / part
        try:
            metadata = candidate.lstat()
        except FileNotFoundError:
            try:
                candidate.mkdir(mode=0o700)
                _fsync_directory(current, relative)
            except OSError:
                _raise("KIN-E-CONCURRENT", relative, "cannot create output directory safely")
            created.append(candidate)
            current = candidate
            continue
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            _raise("KIN-E-PATH", relative, "output path has a non-directory or symlinked parent")
        current = candidate
    return created


def _stage_output(
    root: Path,
    output: _Output,
    snapshot: _ReadSnapshot,
) -> tuple[_StagedOutput, list[Path]]:
    created = _ensure_parent_directories(root, output.relative)
    destination = _safe_repo_value(root, output.relative)
    if snapshot.path != destination:
        _raise("KIN-E-CONCURRENT", output.relative, "output snapshot names another path")
    if snapshot.kind not in {"ABSENT", "FILE"}:
        _raise("KIN-E-SCOPE", output.relative, "output is not an ordinary file")
    existed = snapshot.kind == "FILE"
    mode = snapshot.mode if snapshot.mode is not None else 0o644
    original = snapshot.payload if snapshot.payload is not None else b""

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.kintsugi-",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        written = 0
        while written < len(output.payload):
            count = os.write(descriptor, output.payload[written:])
            if count <= 0:
                raise OSError("zero-byte output write")
            written += count
        os.fsync(descriptor)
    except OSError:
        os.close(descriptor)
        temporary.unlink(missing_ok=True)
        _raise("KIN-E-CONCURRENT", output.relative, "cannot persist staged output")
    os.close(descriptor)

    backup: Path | None = None
    if existed:
        backup_descriptor, backup_name = tempfile.mkstemp(
            prefix=f".{destination.name}.kintsugi-backup-",
            suffix=".tmp",
            dir=destination.parent,
        )
        backup = Path(backup_name)
        try:
            os.fchmod(backup_descriptor, mode)
            written = 0
            while written < len(original):
                count = os.write(backup_descriptor, original[written:])
                if count <= 0:
                    raise OSError("zero-byte backup write")
                written += count
            os.fsync(backup_descriptor)
        except OSError:
            os.close(backup_descriptor)
            backup.unlink(missing_ok=True)
            temporary.unlink(missing_ok=True)
            _raise("KIN-E-CONCURRENT", output.relative, "cannot persist rollback backup")
        os.close(backup_descriptor)
    return _StagedOutput(output, destination, temporary, backup, existed), created


def _cleanup_directories(created: Iterable[Path]) -> None:
    for directory in sorted(set(created), key=lambda item: len(item.parts), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass


def _install_outputs(
    root: Path,
    request: RenderTransactionRequest,
    outputs: list[_Output],
    snapshots: Mapping[str, _ReadSnapshot],
    git_fingerprint: _GitFingerprint,
    namespace_fingerprint: _NamespaceFingerprint,
) -> None:
    staged: list[_StagedOutput] = []
    created_directories: list[Path] = []
    try:
        seen: set[str] = set()
        for output in sorted(outputs, key=lambda item: item.relative):
            if output.relative in seen:
                _raise("KIN-E-CONCURRENT", output.relative, "transaction output is duplicated")
            seen.add(output.relative)
            snapshot = snapshots.get(f"repo:{output.relative}")
            if snapshot is None:
                _raise(
                    "KIN-E-CONCURRENT",
                    output.relative,
                    "transaction output is absent from the frozen read set",
                )
            if snapshot.kind == "FILE" and snapshot.payload == output.payload:
                continue
            staged_output, created = _stage_output(root, output, snapshot)
            staged.append(staged_output)
            created_directories.extend(created)

        ignored_paths = frozenset(
            path
            for item in staged
            for path in (item.temporary, item.backup)
            if path is not None
        )
        ignored_untracked = frozenset(
            path.relative_to(root).as_posix()
            for path in ignored_paths
        )
        for item in staged:
            temporary_snapshot = _snapshot_file(
                item.temporary,
                f"staged:{item.output.relative}",
            )
            if (
                temporary_snapshot.kind != "FILE"
                or temporary_snapshot.payload != item.output.payload
            ):
                _raise(
                    "KIN-E-CONCURRENT",
                    item.output.relative,
                    "staged output changed before repository replacement",
                )
            if item.backup is not None:
                expected = snapshots[f"repo:{item.output.relative}"]
                backup_snapshot = _snapshot_file(
                    item.backup,
                    f"backup:{item.output.relative}",
                )
                if (
                    backup_snapshot.kind != "FILE"
                    or backup_snapshot.payload != expected.payload
                ):
                    _raise(
                        "KIN-E-CONCURRENT",
                        item.output.relative,
                        "rollback backup changed before repository replacement",
                    )
        _recheck_read_set(
            root,
            request,
            snapshots,
            git_fingerprint,
            namespace_fingerprint,
            ignored_untracked=ignored_untracked,
            ignored_namespace=frozenset(set(ignored_paths) | set(created_directories)),
        )

        try:
            for item in staged:
                os.replace(item.temporary, item.destination)
                item.installed = True
            for directory in sorted({item.destination.parent for item in staged}):
                _fsync_directory(directory, "transaction")
        except (OSError, KintsugiError):
            rollback_failed = False
            for item in reversed(staged):
                if not item.installed:
                    continue
                try:
                    if item.existed:
                        if item.backup is None:
                            rollback_failed = True
                            continue
                        os.replace(item.backup, item.destination)
                    else:
                        item.destination.unlink(missing_ok=True)
                except OSError:
                    rollback_failed = True
            for directory in sorted({item.destination.parent for item in staged}):
                try:
                    _fsync_directory(directory, "rollback")
                except KintsugiError:
                    rollback_failed = True
            detail = "repository replacement failed"
            if rollback_failed:
                detail += " and rollback was incomplete"
            _raise("KIN-E-CONCURRENT", "transaction", detail)
    finally:
        for item in staged:
            item.temporary.unlink(missing_ok=True)
            if item.backup is not None:
                item.backup.unlink(missing_ok=True)
        _cleanup_directories(created_directories)


def write_rendered_value(
    root: Path, *, request: RenderTransactionRequest
) -> None:
    """Install one operation-specific renderer transaction, or change nothing."""

    _validate_request(request)
    if not isinstance(root, Path):
        _raise("KIN-E-CLI", "root", "repository root must be a Path")
    try:
        resolved_root = root.resolve(strict=True)
    except (OSError, RuntimeError):
        _raise("KIN-E-PATH", "root", "repository root is unavailable")
    _safe_repo_value(resolved_root, request.core_path)

    # Caller CAS is checked before lock acquisition and repeated inside it.
    _check_head_core_cas(
        resolved_root,
        request.core_path,
        request.expected_head,
        request.expected_core_sha256,
    )
    try:
        common_dir = resolve_git_common_dir(resolved_root)
    except RuntimeError:
        _raise("KIN-E-CONCURRENT", "git", "Git common directory cannot be resolved safely")
    with _transition_lock(common_dir):
        _check_head_core_cas(
            resolved_root,
            request.core_path,
            request.expected_head,
            request.expected_core_sha256,
        )
        core = _load_core_locked(resolved_root, request.core_path)
        manifest = _selected_manifest(core, request.phase)
        receipt = _selected_receipt(core, request.phase)
        _validate_operation_paths(
            resolved_root,
            request,
            core,
            manifest,
            receipt,
        )
        external = _external_inputs(resolved_root, request)
        snapshots = _freeze_read_set(
            resolved_root,
            core,
            manifest,
            receipt,
            request,
            external,
        )
        git_fingerprint = _capture_git_fingerprint(
            resolved_root,
            request,
            manifest,
        )
        namespace_fingerprint = _capture_namespace_fingerprint(
            resolved_root,
            request,
        )
        _validate_core_state(core, snapshots)
        _validate_closure_files(
            core,
            snapshots,
            namespace_fingerprint,
        )

        reservation: Path | None = None
        if request.operation == "freeze-manifest":
            outputs, reservation = _freeze_outputs(
                resolved_root,
                request,
                core,
                receipt,
                common_dir,
                snapshots,
                git_fingerprint,
            )
        elif request.operation == "review-target":
            outputs = _review_target_outputs(
                request,
                core,
                manifest,
                receipt,
                snapshots,
                git_fingerprint.isolated_state,
            )
        elif request.operation == "transition-core":
            outputs = _transition_outputs(
                request,
                core,
                receipt,
                snapshots,
            )
        else:
            _preflight_bundle(request, core, receipt, snapshots)
            _recheck_read_set(
                resolved_root,
                request,
                snapshots,
                git_fingerprint,
                namespace_fingerprint,
            )
            return

        if reservation is not None:
            _add_read_snapshot(
                snapshots,
                f"reservation:{reservation.name}",
                reservation,
                "reservation",
            )
        for output in outputs:
            _validate_repo_output(
                resolved_root,
                output.relative,
                manifest,
                closure_required=(
                    True
                    if output.relative in set(
                        _path_values(
                            manifest.get("closureOnlyPaths"),
                            "manifest.closureOnlyPaths",
                        )
                    )
                    else False
                ),
            )
        prospective_core = core
        core_outputs = [
            output for output in outputs if output.relative == request.core_path
        ]
        if len(core_outputs) > 1:
            _raise("KIN-E-CONCURRENT", request.core_path, "core output is duplicated")
        if core_outputs:
            prospective_core = _mapping(
                _decode_canonical_bytes(
                    core_outputs[0].payload,
                    request.core_path,
                ),
                request.core_path,
            )
        _validate_core_state(prospective_core, snapshots)
        _validate_closure_files(
            prospective_core,
            snapshots,
            namespace_fingerprint,
            overlay={
                output.relative: output.payload
                for output in outputs
                if _is_below(output.relative, _CLOSURE_ROOTS)
            },
        )
        _install_outputs(
            resolved_root,
            request,
            outputs,
            snapshots,
            git_fingerprint,
            namespace_fingerprint,
        )


__all__ = ["RenderTransactionRequest", "write_rendered_value"]
