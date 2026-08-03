from __future__ import annotations

import copy
import fnmatch
import json
from pathlib import Path
from typing import Any, Mapping

from .codec import canonical_json_bytes, normalize_lf, raw_hash, text_hash
from .diagnostics import Issue, KintsugiError
from .gitstate import (
    AttemptPlan,
    FileRecord,
    GitState,
    _base_blob_records,
    _attempt_id_from_path,
    _hash_regular_or_symlink,
    _filesystem_attempt_state,
    _index_record,
    _list_worktrees,
    _plan_next_attempt,
    _resolve_commit,
    _snapshot_protected_tree,
    _read_regular_no_symlinks,
    _reservation_records,
    _validate_predecessor_fence,
    _validate_reachable_terminal_chain,
    _unique_chain_leaf,
    _worktree_attempt_paths,
    inspect_git_state,
    resolve_git_common_dir,
)
from .markdown import (
    project_review_seam,
    synchronize_ledger_markdown,
    synchronize_receipt_markdown,
)
from .records import (
    PHASE_A_REQUIREMENTS,
    RECEIPT_IDENTITIES,
    attempt_paths,
    canonical_attempt,
)


_CORE_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
_SCHEMA_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
_LEDGER_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
_REQUIRED_PROTECTED_ROOTS = frozenset({
    "12_PUBLIC_SITE",
    "90_ARCHIVE",
    "91_COMPATIBILITY",
})
_PARSER_SUFFIXES = {
    "MARKDOWN": (".md", ".markdown"),
    "HTML": (".html", ".htm"),
    "JSON": (".json",),
    "SOURCE_INDEX": (".md", ".markdown", ".json", ".yaml", ".yml"),
}
_PRIOR_REVIEW_FIELDS = (
    "priorReviewAttempts",
    "priorReviewAttemptArtifacts",
    "priorReviewAttestations",
    "priorReviewFindings",
    "priorReviewFindingDispositions",
)
_DISPOSITION_INPUT_FIELDS = frozenset({
    "findingId",
    "disposition",
    "rationale",
    "claimIds",
    "seamIds",
    "ledgerSectionIds",
    "receiptIds",
    "subjectPaths",
    "discriminatorIds",
    "evidenceFiles",
})
_FrozenReads = Mapping[str, tuple[str, bytes]]


def _issue(path: str, code: str, message: str) -> Issue:
    return Issue(path, code, message)


def _raise(path: str, code: str, message: str) -> None:
    raise KintsugiError(code, path, message)


def _require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _raise(path, "KIN-E-MANIFEST", "expected an object")
    return value


def _require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _raise(path, "KIN-E-MANIFEST", "expected a list")
    return value


def _repo_path(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value or value.startswith("/") or "\\" in value:
        _raise(path, "KIN-E-MANIFEST", "expected a repository-relative POSIX path")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        _raise(path, "KIN-E-MANIFEST", "path contains a forbidden segment")
    return value


def _file_record(value: Any, path: str) -> FileRecord:
    record = _require_mapping(value, path)
    relative = _repo_path(record.get("path"), f"{path}.path")
    kind = record.get("kind")
    digest = record.get("sha256")
    if kind not in {"FILE", "SYMLINK"}:
        _raise(f"{path}.kind", "KIN-E-MANIFEST", "file kind is invalid")
    if not isinstance(digest, str) or not digest.startswith("sha256:") or len(digest) != 71:
        _raise(f"{path}.sha256", "KIN-E-MANIFEST", "raw hash is invalid")
    if any(character not in "0123456789abcdef" for character in digest[7:]):
        _raise(f"{path}.sha256", "KIN-E-MANIFEST", "raw hash is invalid")
    return FileRecord(relative, kind, digest)


def _file_records(value: Any, path: str) -> tuple[FileRecord, ...]:
    records = tuple(_file_record(item, f"{path}[{index}]") for index, item in enumerate(
        _require_list(value, path)
    ))
    if len({record.path for record in records}) != len(records):
        _raise(path, "KIN-E-MANIFEST", "file paths must be unique")
    if records != tuple(sorted(records, key=lambda record: record.path)):
        _raise(path, "KIN-E-MANIFEST", "file records must be sorted by path")
    return records


def _path_list(value: Any, path: str) -> tuple[str, ...]:
    result = tuple(_repo_path(item, f"{path}[{index}]") for index, item in enumerate(
        _require_list(value, path)
    ))
    if len(set(result)) != len(result) or result != tuple(sorted(result)):
        _raise(path, "KIN-E-MANIFEST", "paths must be unique and sorted")
    return result


def _selected_manifest_receipt(
    core: dict[str, object], phase: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    if phase not in RECEIPT_IDENTITIES:
        _raise("phase", "KIN-E-MANIFEST", "selected phase is invalid")
    manifests = [
        item for item in _require_list(core.get("manifests"), "core.manifests")
        if isinstance(item, dict) and item.get("phase") == phase
    ]
    receipts = [
        item for item in _require_list(core.get("phaseReceipts"), "core.phaseReceipts")
        if isinstance(item, dict) and item.get("phase") == phase
    ]
    if len(manifests) != 1 or len(receipts) != 1:
        _raise("manifest", "KIN-E-MANIFEST", "phase requires exactly one manifest and receipt")
    manifest, receipt = manifests[0], receipts[0]
    expected_id, expected_path, expected_dependencies = RECEIPT_IDENTITIES[phase]
    if (
        receipt.get("id") != expected_id
        or receipt.get("path") != expected_path
        or tuple(receipt.get("dependsOnReceiptIds", ())) != expected_dependencies
        or receipt.get("manifestId") != manifest.get("id")
    ):
        _raise("receipt", "KIN-E-MANIFEST", "phase receipt identity is non-canonical")
    return manifest, receipt


def _resolve_roots(
    isolated_root: Path,
    canonical_root: Path,
    manifest: dict[str, Any],
    base_ref: str,
) -> tuple[GitState, GitState, str]:
    base_commit = manifest.get("baseCommit")
    canonical_commit = manifest.get("canonicalCommit")
    if not isinstance(base_commit, str) or len(base_commit) != 40:
        _raise("manifest.baseCommit", "KIN-E-CONCURRENT", "base commit is invalid")
    if not isinstance(canonical_commit, str) or len(canonical_commit) != 40:
        _raise("manifest.canonicalCommit", "KIN-E-CONCURRENT", "canonical commit is invalid")
    if manifest.get("canonicalBranch") != "main":
        _raise("manifest.canonicalBranch", "KIN-E-CONCURRENT", "canonical branch must be main")
    selected_ref = base_commit if base_ref == "MANIFEST" else base_ref
    if base_ref != "MANIFEST" and (
        not isinstance(base_ref, str)
        or not 7 <= len(base_ref) <= 40
        or any(character not in "0123456789abcdef" for character in base_ref)
    ):
        _raise("baseRef", "KIN-E-CONCURRENT", "base ref must be MANIFEST or hexadecimal")
    resolved_base = _resolve_commit(isolated_root, selected_ref)
    if resolved_base != base_commit or _resolve_commit(canonical_root, selected_ref) != base_commit:
        _raise("baseRef", "KIN-E-CONCURRENT", "base ref does not equal the manifest base")
    isolated = inspect_git_state(isolated_root, base_commit)
    canonical = inspect_git_state(canonical_root, base_commit)
    assert isinstance(isolated, GitState) and isinstance(canonical, GitState)
    if isolated.root == canonical.root or isolated.common_dir != canonical.common_dir:
        _raise("canonicalRoot", "KIN-E-CONCURRENT", "roots are not distinct linked worktrees")
    worktrees = _list_worktrees(isolated.root)
    by_root = {record.root: record for record in worktrees}
    if isolated.root not in by_root or canonical.root not in by_root:
        _raise("canonicalRoot", "KIN-E-CONCURRENT", "root is not a registered worktree")
    main_roots = [record for record in worktrees if record.branch == "main"]
    if len(main_roots) != 1 or main_roots[0].root != canonical.root:
        _raise("canonicalRoot", "KIN-E-CONCURRENT", "canonical root is not the unique main worktree")
    if canonical.branch != "main" or canonical.head != canonical_commit:
        _raise("canonicalRoot", "KIN-E-CONCURRENT", "canonical HEAD moved after manifest freeze")
    return isolated, canonical, base_commit


def _glob_match(relative: str, pattern: str) -> bool:
    if not isinstance(pattern, str) or not pattern or pattern.startswith("/") or "\\" in pattern:
        _raise("manifest.discoveryRules", "KIN-E-MANIFEST", "discovery glob is invalid")
    path_parts = relative.split("/")
    pattern_parts = pattern.split("/")
    memo: dict[tuple[int, int], bool] = {}

    def visit(path_index: int, pattern_index: int) -> bool:
        key = (path_index, pattern_index)
        if key in memo:
            return memo[key]
        if pattern_index == len(pattern_parts):
            answer = path_index == len(path_parts)
        elif pattern_parts[pattern_index] == "**":
            answer = visit(path_index, pattern_index + 1) or (
                path_index < len(path_parts) and visit(path_index + 1, pattern_index)
            )
        else:
            answer = (
                path_index < len(path_parts)
                and fnmatch.fnmatchcase(path_parts[path_index], pattern_parts[pattern_index])
                and visit(path_index + 1, pattern_index + 1)
            )
        memo[key] = answer
        return answer

    return visit(0, 0)


def _reserved_control_paths(
    core: dict[str, object], receipt: dict[str, Any], phase: str
) -> tuple[set[str], set[str]]:
    fixed = {_CORE_PATH, _LEDGER_PATH, _repo_path(receipt.get("path"), "receipt.path")}
    attempts: set[str] = set()
    selected_chain: list[dict[str, Any]] = []
    for index, attempt in enumerate(_require_list(core.get("reviewAttempts"), "core.reviewAttempts")):
        record = _require_mapping(attempt, f"core.reviewAttempts[{index}]")
        attempt_phase = record.get("phase")
        attempt_id = record.get("id")
        if not canonical_attempt(attempt_id, attempt_phase):
            _raise(
                f"core.reviewAttempts[{index}].id",
                "KIN-E-MANIFEST",
                "attempt ID is invalid",
            )
        identity = RECEIPT_IDENTITIES.get(str(attempt_phase))
        if identity is None or record.get("receiptId") != identity[0]:
            _raise(
                f"core.reviewAttempts[{index}].receiptId",
                "KIN-E-MANIFEST",
                "attempt receipt ownership is non-canonical",
            )
        expected = attempt_paths(attempt_id)
        actual = tuple(record.get(field) for field in (
            "reviewTargetPath",
            "logicReviewPath",
            "btjReviewPath",
            "validationBundlePath",
        ))
        if actual != expected:
            _raise(
                f"core.reviewAttempts[{index}]",
                "KIN-E-MANIFEST",
                "attempt roles are not the exact four derived paths",
            )
        # Every declared attempt is a typed control artifact and must be
        # filtered from source discovery, even when it belongs to another
        # phase.  Only the selected phase contributes closure-only paths.
        attempts.update(expected)
        if attempt_phase == phase:
            selected_chain.append(record)
    try:
        leaf = _unique_chain_leaf(selected_chain, context="manifest attempt chain")
    except KintsugiError as exc:
        _raise("core.reviewAttempts", "KIN-E-MANIFEST", exc.message)
    pointer = receipt.get("reviewAttemptId")
    if (leaf is None and pointer is not None) or (
        leaf is not None and pointer != leaf.get("id")
    ):
        _raise(
            "receipt.reviewAttemptId",
            "KIN-E-MANIFEST",
            "receipt pointer must name the unique selected attempt-chain leaf",
        )
    return fixed, attempts


def _discover_candidates(
    manifest: dict[str, Any], base_records: tuple[FileRecord, ...], reserved: set[str]
) -> tuple[tuple[FileRecord, ...], tuple[FileRecord, ...], tuple[str, ...]]:
    by_path = {record.path: record for record in base_records}
    candidate_paths: set[str] = set()
    excluded_paths: set[str] = set()
    rules = _require_list(manifest.get("discoveryRules"), "manifest.discoveryRules")
    if not rules:
        _raise("manifest.discoveryRules", "KIN-E-MANIFEST", "at least one discovery rule is required")
    for index, raw_rule in enumerate(rules):
        rule = _require_mapping(raw_rule, f"manifest.discoveryRules[{index}]")
        parser = rule.get("parser")
        if parser not in _PARSER_SUFFIXES:
            _raise(f"manifest.discoveryRules[{index}].parser", "KIN-E-MANIFEST", "parser is invalid")
        include_globs = _require_list(rule.get("includeGlobs"), f"manifest.discoveryRules[{index}].includeGlobs")
        exclude_globs = _require_list(rule.get("excludeGlobs"), f"manifest.discoveryRules[{index}].excludeGlobs")
        if not include_globs or not exclude_globs:
            _raise(f"manifest.discoveryRules[{index}]", "KIN-E-MANIFEST", "include and exclude globs are required")
        for include in include_globs:
            matched = sorted(path for path in by_path if _glob_match(path, include))
            if not matched:
                _raise(f"manifest.discoveryRules[{index}].includeGlobs", "KIN-E-MANIFEST", "include glob matches no base path")
            for relative in matched:
                if relative in reserved:
                    continue
                if not relative.lower().endswith(_PARSER_SUFFIXES[parser]):
                    _raise(f"manifest.discoveryRules[{index}].parser", "KIN-E-MANIFEST", "parser does not match selected path")
                candidate_paths.add(relative)
                if any(_glob_match(relative, exclude) for exclude in exclude_globs):
                    excluded_paths.add(relative)
    included_paths = candidate_paths - excluded_paths
    candidates = tuple(by_path[path] for path in sorted(candidate_paths))
    included = tuple(by_path[path] for path in sorted(included_paths))
    return candidates, included, tuple(sorted(excluded_paths))


def _validate_inventory(
    root: Path,
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    phase: str,
    base_commit: str,
) -> tuple[set[str], set[str]]:
    fixed_controls, attempt_controls = _reserved_control_paths(core, receipt, phase)
    reserved = fixed_controls | attempt_controls
    for relative in sorted(fixed_controls):
        try:
            _read_regular_no_symlinks(
                root,
                relative,
                code="KIN-E-MANIFEST",
                require_single_link=True,
            )
        except KintsugiError:
            _raise(relative, "KIN-E-MANIFEST", "reserved control file is missing or not regular")
    base_records = _base_blob_records(root, base_commit)
    expected_candidates, expected_included, expected_excluded = _discover_candidates(
        manifest, base_records, reserved
    )
    candidates = _file_records(manifest.get("candidateFiles"), "manifest.candidateFiles")
    included = _file_records(manifest.get("includedFiles"), "manifest.includedFiles")
    final = _file_records(manifest.get("finalFiles"), "manifest.finalFiles")
    excluded_values = _require_list(manifest.get("excludedPaths"), "manifest.excludedPaths")
    excluded: list[str] = []
    for index, value in enumerate(excluded_values):
        record = _require_mapping(value, f"manifest.excludedPaths[{index}]")
        relative = _repo_path(record.get("path"), f"manifest.excludedPaths[{index}].path")
        if not isinstance(record.get("reason"), str) or not record["reason"]:
            _raise(f"manifest.excludedPaths[{index}].reason", "KIN-E-MANIFEST", "exclusion reason is required")
        excluded.append(relative)
    if tuple(excluded) != tuple(sorted(set(excluded))):
        _raise("manifest.excludedPaths", "KIN-E-MANIFEST", "excluded paths must be unique and sorted")
    if reserved & ({record.path for record in candidates} | {record.path for record in included} | {record.path for record in final} | set(excluded)):
        _raise("manifest", "KIN-E-MANIFEST", "reserved control path entered a source inventory")
    if candidates != expected_candidates or included != expected_included or tuple(excluded) != expected_excluded:
        _raise("manifest", "KIN-E-MANIFEST", "candidate/included/excluded partition differs from discovery")
    if manifest.get("candidateFileCount") != len(candidates):
        _raise("manifest.candidateFileCount", "KIN-E-MANIFEST", "candidate count is stale")
    if manifest.get("eligibleFileCount") != len(included) or manifest.get("scannedFileCount") != len(included):
        _raise("manifest.eligibleFileCount", "KIN-E-MANIFEST", "eligible/scanned count is stale")
    current_attempt = receipt.get("reviewAttemptId")
    if current_attempt is None:
        if receipt.get("status") != "DRAFT":
            _raise(
                "receipt.reviewAttemptId",
                "KIN-E-MANIFEST",
                "only a pre-review DRAFT may have no current review attempt",
            )
        if final or manifest.get("finalFileCount") != 0:
            _raise("manifest.finalFiles", "KIN-E-MANIFEST", "pre-review DRAFT must have no final snapshot")
    else:
        expected_final = tuple(sorted(
            (_hash_regular_or_symlink(root, record.path) for record in included),
            key=lambda record: record.path,
        ))
        if final != expected_final or manifest.get("finalFileCount") != len(expected_final):
            _raise("manifest.finalFiles", "KIN-E-MANIFEST", "review-ready final snapshot is stale")
    expected_closure = tuple(sorted({
        path
        for attempt in _require_list(core.get("reviewAttempts"), "core.reviewAttempts")
        if isinstance(attempt, dict) and attempt.get("phase") == phase
        for path in attempt_paths(str(attempt.get("id")))
    }))
    closure = _path_list(manifest.get("closureOnlyPaths"), "manifest.closureOnlyPaths")
    allowed = _path_list(manifest.get("allowedChangePaths"), "manifest.allowedChangePaths")
    if closure != expected_closure or not set(closure).issubset(set(allowed)):
        _raise("manifest.closureOnlyPaths", "KIN-E-MANIFEST", "closure-only paths are not the exact attempt union")
    if set(closure) & fixed_controls:
        _raise("manifest.closureOnlyPaths", "KIN-E-MANIFEST", "fixed control paths cannot be closure-only")
    allowed_attempt_paths: set[str] = set()
    for relative in allowed:
        try:
            derived_attempt = _attempt_id_from_path(relative)
        except KintsugiError as exc:
            _raise(relative, "KIN-E-MANIFEST", exc.message)
        if derived_attempt is not None:
            allowed_attempt_paths.add(relative)
    if allowed_attempt_paths != set(closure):
        _raise(
            "manifest.allowedChangePaths",
            "KIN-E-MANIFEST",
            "attempt-shaped allowances must equal the declared closure union",
        )
    return {record.path for record in included}, reserved


def _validate_claim_partition(
    root: Path,
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    phase: str,
    included_paths: set[str],
    reserved_paths: set[str],
) -> None:
    harvested = _require_list(manifest.get("harvestedClaimIds"), "manifest.harvestedClaimIds")
    trialed = _require_list(manifest.get("trialedClaimIds"), "manifest.trialedClaimIds")
    exclusions = _require_list(manifest.get("excludedClaimIds"), "manifest.excludedClaimIds")
    if any(not isinstance(value, str) for value in harvested + trialed):
        _raise("manifest.harvestedClaimIds", "KIN-E-MANIFEST", "claim IDs must be strings")
    excluded: list[str] = []
    for index, value in enumerate(exclusions):
        record = _require_mapping(value, f"manifest.excludedClaimIds[{index}]")
        claim_id = record.get("claimId")
        if not isinstance(claim_id, str) or not isinstance(record.get("reason"), str) or not record["reason"]:
            _raise(f"manifest.excludedClaimIds[{index}]", "KIN-E-MANIFEST", "claim exclusion is invalid")
        excluded.append(claim_id)
    if len(set(harvested)) != len(harvested) or len(set(trialed)) != len(trialed) or len(set(excluded)) != len(excluded):
        _raise("manifest.harvestedClaimIds", "KIN-E-MANIFEST", "claim partitions must be unique")
    h, t, x = set(harvested), set(trialed), set(excluded)
    all_trials = _require_list(core.get("trials"), "core.trials")
    exact_bootstrap = (
        phase == "A"
        and receipt.get("status") == "DRAFT"
        and receipt.get("reviewAttemptId") is None
        and all_trials == []
        and receipt.get("trialIds") == []
        and t == set()
        and x == set()
        and manifest.get("finalFiles") == []
        and manifest.get("closureOnlyPaths") == []
        and bool(h)
    )
    receipt_claims = _require_list(receipt.get("claimIds"), "receipt.claimIds")
    expected_receipt_claims = h if exact_bootstrap else t
    if (
        any(not isinstance(value, str) or not value for value in receipt_claims)
        or len(set(receipt_claims)) != len(receipt_claims)
        or set(receipt_claims) != expected_receipt_claims
    ):
        _raise(
            "receipt.claimIds",
            "KIN-E-MANIFEST",
            "receipt claim roots are not the exact reviewed claim set",
        )
    if t & x or (not exact_bootstrap and h != t | x):
        _raise("manifest.harvestedClaimIds", "KIN-E-MANIFEST", "harvested claims are not the trial/exclusion partition")
    if manifest.get("eligibleClaimCount") != len(h) or manifest.get("trialedClaimCount") != len(t):
        _raise("manifest.eligibleClaimCount", "KIN-E-MANIFEST", "claim counts are stale")
    claims = {
        item.get("id"): item
        for item in _require_list(core.get("claims"), "core.claims")
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    sources = {
        item.get("id"): item
        for item in _require_list(core.get("sources"), "core.sources")
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if not h or not h.issubset(claims):
        _raise("manifest.harvestedClaimIds", "KIN-E-MANIFEST", "harvested claim does not resolve")
    reserved_casefold = {relative.casefold() for relative in reserved_paths}
    for source in sources.values():
        source_path = source.get("path")
        if (
            isinstance(source_path, str)
            and source_path.casefold() in reserved_casefold
        ):
            _raise(
                "core.sources",
                "KIN-E-MANIFEST",
                "reserved control path cannot be reintroduced as a raw-hashed source",
            )
    for claim_id in h:
        source = sources.get(claims[claim_id].get("ownerSourceId"))
        if source is None or source.get("path") not in included_paths:
            _raise("core.sources", "KIN-E-MANIFEST", "claim owner source is outside the included inventory")
    for source in sources.values():
        if phase in source.get("phases", ()) and source.get("kind") != "RECEIPT":
            if source.get("path") not in included_paths:
                _raise("core.sources", "KIN-E-MANIFEST", "phase source is outside the included inventory")
            relative = str(source.get("path"))
            try:
                current_source = _hash_regular_or_symlink(root, relative)
            except KintsugiError as exc:
                _raise(relative, "KIN-E-MANIFEST", exc.message)
            if source.get("sha256") != current_source.sha256:
                _raise(
                    relative,
                    "KIN-E-MANIFEST",
                    "source raw hash does not match the current reviewed bytes",
                )
    trials = [
        item for item in all_trials
        if isinstance(item, dict) and item.get("manifestId") == manifest.get("id")
    ]
    if not exact_bootstrap:
        if {trial.get("claimId") for trial in trials} != t:
            _raise("core.trials", "KIN-E-MANIFEST", "trials do not exactly cover trialed claims")
        if set(receipt.get("trialIds", ())) != {trial.get("id") for trial in trials}:
            _raise("receipt.trialIds", "KIN-E-MANIFEST", "receipt trial IDs are stale")
    elif phase != "A" or not h:
        _raise("core.trials", "KIN-E-MANIFEST", "empty trials are legal only in exact Phase-A bootstrap")
    _validate_phase_a_bindings(
        root,
        core,
        manifest,
        receipt,
        phase,
        h,
        t,
        x,
        claims,
        sources,
        trials,
        exact_bootstrap,
    )


def _validate_phase_a_bindings(
    root: Path,
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    phase: str,
    harvested: set[str],
    trialed: set[str],
    excluded: set[str],
    claims: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    trials: list[dict[str, Any]],
    bootstrap: bool,
) -> None:
    bindings = _require_list(manifest.get("requiredClaimBindings"), "manifest.requiredClaimBindings")
    if phase != "A":
        if bindings:
            _raise("manifest.requiredClaimBindings", "KIN-E-MANIFEST", "Phase B/C bindings must be empty")
        return
    by_requirement: dict[str, dict[str, Any]] = {}
    bound_claims: set[str] = set()
    for index, value in enumerate(bindings):
        binding = _require_mapping(value, f"manifest.requiredClaimBindings[{index}]")
        requirement = binding.get("requirementId")
        if requirement in by_requirement or requirement not in PHASE_A_REQUIREMENTS:
            _raise(f"manifest.requiredClaimBindings[{index}]", "KIN-E-MANIFEST", "requirement binding is missing or duplicated")
        claim_id = binding.get("claimId")
        if not isinstance(claim_id, str) or claim_id in bound_claims:
            _raise(f"manifest.requiredClaimBindings[{index}].claimId", "KIN-E-MANIFEST", "bound claims must be distinct")
        by_requirement[requirement] = binding
        bound_claims.add(claim_id)
    if set(by_requirement) != set(PHASE_A_REQUIREMENTS):
        _raise("manifest.requiredClaimBindings", "KIN-E-MANIFEST", "Phase A requires all seven frozen bindings")
    declared_trial_ids = set(receipt.get("trialIds", ()))
    canonical_receipt_id = RECEIPT_IDENTITIES["A"][0]
    owner_text_by_path: dict[str, str] = {}
    for requirement, expected in PHASE_A_REQUIREMENTS.items():
        owner_path, anchor, target_hash = expected
        binding = by_requirement[requirement]
        claim_id = binding.get("claimId")
        claim = claims.get(claim_id)
        source = sources.get(binding.get("ownerSourceId"))
        if (
            claim is None
            or claim_id not in harvested
            or claim_id in excluded
            or binding.get("ownerSourceId") != claim.get("ownerSourceId")
            or binding.get("ownerAnchor") != claim.get("ownerAnchor")
            or binding.get("ownerAnchor") != anchor
            or binding.get("targetHash") != target_hash
            or source is None
            or source.get("path") != owner_path
        ):
            _raise("manifest.requiredClaimBindings", "KIN-E-MANIFEST", "frozen Phase-A binding does not match its owner and claim")
        owner_text = owner_text_by_path.get(owner_path)
        if owner_text is None:
            try:
                owner_payload = _read_regular_no_symlinks(
                    root,
                    owner_path,
                    code="KIN-E-MANIFEST",
                    require_single_link=True,
                )
                owner_text = normalize_lf(owner_payload.decode("utf-8"))
            except KintsugiError as exc:
                _raise(owner_path, "KIN-E-MANIFEST", exc.message)
            except UnicodeDecodeError:
                _raise(owner_path, "KIN-E-MANIFEST", "owner source is not valid UTF-8")
            owner_text_by_path[owner_path] = owner_text
        if normalize_lf(anchor) not in owner_text:
            _raise(
                owner_path,
                "KIN-E-MANIFEST",
                "frozen Phase-A owner anchor is absent from the reviewed bytes",
            )
        if not bootstrap:
            owned_trials = [
                trial for trial in trials if trial.get("claimId") == claim_id
            ]
            matching_trials = [
                trial
                for trial in owned_trials
                if trial.get("id") in declared_trial_ids
                and trial.get("manifestId") == manifest.get("id")
                and trial.get("receiptId") == canonical_receipt_id
                and trial.get("triedHash") == target_hash
                and isinstance(trial.get("triedQuote"), str)
                and text_hash(trial["triedQuote"]) == target_hash
            ]
            if (
                claim_id not in trialed
                or len(owned_trials) != 1
                or len(matching_trials) != 1
            ):
                _raise("manifest.requiredClaimBindings", "KIN-E-MANIFEST", "binding lacks its unique matching trial")
            tried_quote = normalize_lf(str(matching_trials[0]["triedQuote"]))
            if owner_text.count(tried_quote) != 1:
                _raise(
                    owner_path,
                    "KIN-E-MANIFEST",
                    "frozen Phase-A tried quote must occur exactly once in its owner bytes",
                )


def _validate_protected(
    isolated: GitState,
    canonical: GitState,
    manifest: dict[str, Any],
) -> None:
    protected_paths = _path_list(manifest.get("protectedPaths"), "manifest.protectedPaths")
    if not _REQUIRED_PROTECTED_ROOTS.issubset(protected_paths):
        _raise("manifest.protectedPaths", "KIN-E-PROTECTED", "required protected roots are absent")
    snapshots = _require_mapping(manifest.get("protectedTreeSnapshots"), "manifest.protectedTreeSnapshots")
    # These are independent phase-start baselines.  Task 7 binds their temporal
    # origin through raw-core CAS; this pure validator proves each root against
    # its already-frozen value and must not collapse the two roots together.
    expected_isolated = _file_records(snapshots.get("isolated"), "manifest.protectedTreeSnapshots.isolated")
    expected_canonical = _file_records(snapshots.get("canonical"), "manifest.protectedTreeSnapshots.canonical")
    current_isolated = _snapshot_protected_tree(isolated.root, protected_paths)
    current_canonical = _snapshot_protected_tree(canonical.root, protected_paths)
    if current_isolated != expected_isolated or current_canonical != expected_canonical:
        _raise("manifest.protectedTreeSnapshots", "KIN-E-PROTECTED", "protected tree drifted from its frozen snapshot")
    provenance = _require_list(manifest.get("protectedProvenance"), "manifest.protectedProvenance")
    seen: set[str] = set()
    for index, value in enumerate(provenance):
        record = _require_mapping(value, f"manifest.protectedProvenance[{index}]")
        relative = _repo_path(record.get("path"), f"manifest.protectedProvenance[{index}].path")
        if not any(
            relative == root or relative.startswith(root + "/")
            for root in protected_paths
        ):
            _raise(
                relative,
                "KIN-E-PROTECTED",
                "protected provenance path is outside the protected boundary",
            )
        if relative in seen:
            _raise("manifest.protectedProvenance", "KIN-E-PROTECTED", "provenance paths are duplicated")
        seen.add(relative)
        try:
            payloads = [
                _read_regular_no_symlinks(
                    state.root, relative, code="KIN-E-PROTECTED"
                )
                for state in (isolated, canonical)
            ]
        except KintsugiError:
            raise
        if record.get("mode") == "FULL_FILE":
            if any(raw_hash(payload) != record.get("sha256") for payload in payloads):
                _raise(relative, "KIN-E-PROTECTED", "FULL_FILE provenance hash drifted")
        elif record.get("mode") == "EXACT_SPAN":
            span = record.get("exactSpan")
            if not isinstance(span, str) or not span:
                _raise(relative, "KIN-E-PROTECTED", "EXACT_SPAN text is missing")
            encoded = span.encode("utf-8")
            if raw_hash(encoded) != record.get("sha256") or any(encoded not in payload for payload in payloads):
                _raise(relative, "KIN-E-PROTECTED", "EXACT_SPAN provenance drifted")
        else:
            _raise(relative, "KIN-E-PROTECTED", "protected provenance mode is invalid")


def _validate_scope(
    isolated: GitState,
    canonical: GitState,
    manifest: dict[str, Any],
    included_paths: set[str],
    typed_control_paths: set[str],
) -> None:
    allowed = set(_path_list(manifest.get("allowedChangePaths"), "manifest.allowedChangePaths"))
    protected = set(_path_list(manifest.get("protectedPaths"), "manifest.protectedPaths"))
    closure = set(_path_list(manifest.get("closureOnlyPaths"), "manifest.closureOnlyPaths"))
    review_bound_paths = included_paths | typed_control_paths | closure
    allowances = _require_mapping(manifest.get("allowedPreexistingUntracked"), "manifest.allowedPreexistingUntracked")
    for label, state in (("isolated", isolated), ("canonical", canonical)):
        # Root-specific allowances are part of the CAS-bound phase-start core;
        # byte equality here prevents later drift without inventing symmetry.
        expected = _file_records(
            allowances.get(label),
            f"manifest.allowedPreexistingUntracked.{label}",
        )
        current_untracked = {record.path: record for record in state.untracked_records}
        expected_map = {record.path: record for record in expected}
        if any(path not in current_untracked or current_untracked[path] != record for path, record in expected_map.items()):
            _raise(f"manifest.allowedPreexistingUntracked.{label}", "KIN-E-SCOPE", "pre-existing untracked allowance drifted")
        changed = set(state.committed_paths) | set(state.staged_paths) | set(state.unstaged_paths) | set(current_untracked)
        changed -= set(expected_map)
        if state.noncanonical_index_paths:
            _raise(
                state.noncanonical_index_paths[0],
                "KIN-E-SCOPE",
                "non-default index visibility hides the reviewed worktree state",
            )
        unbound_modes = set(state.unrepresentable_mode_paths)
        if unbound_modes:
            _raise(
                sorted(unbound_modes)[0],
                "KIN-E-SCOPE",
                "Git mode change is not representable in the frozen file record",
            )
        for relative in state.staged_paths:
            indexed = _index_record(state.root, relative)
            try:
                worktree: FileRecord | None = _hash_regular_or_symlink(
                    state.root, relative
                )
            except KintsugiError:
                path = state.root.joinpath(*relative.split("/"))
                if path.exists() or path.is_symlink():
                    raise
                worktree = None
            if indexed != worktree:
                _raise(
                    relative,
                    "KIN-E-SCOPE",
                    "staged index bytes differ from the reviewed worktree bytes",
                )
        if label == "canonical" and changed & included_paths:
            _raise(
                sorted(changed & included_paths)[0],
                "KIN-E-SCOPE",
                "canonical source dirt cannot be absorbed by the isolated review allowance",
            )
        for relative in sorted(changed):
            if any(relative == root or relative.startswith(root + "/") for root in protected):
                _raise(relative, "KIN-E-PROTECTED", "protected path changed")
            if relative not in allowed:
                _raise(relative, "KIN-E-SCOPE", "path changed outside the allowed scope")
            if relative not in review_bound_paths:
                _raise(
                    relative,
                    "KIN-E-SCOPE",
                    "changed semantic path lacks a hash-bearing or typed review projection",
                )


def _validate_manifest_or_raise(
    isolated_root: Path,
    canonical_root: Path,
    core: dict[str, object],
    phase: str,
    base_ref: str,
) -> None:
    _require_mapping(core, "core")
    manifest, receipt = _selected_manifest_receipt(core, phase)
    isolated, canonical, base_commit = _resolve_roots(
        isolated_root, canonical_root, manifest, base_ref
    )
    _validate_reachable_terminal_chain(
        isolated.root,
        core,
        phase,
        str(receipt.get("id")),
        _CORE_PATH,
    )
    fixed_controls, declared_attempt_paths = _reserved_control_paths(core, receipt, phase)
    inventory_review_paths = _path_list(
        manifest.get("inventoryReviewPaths"),
        "manifest.inventoryReviewPaths",
    )
    if not inventory_review_paths:
        _raise(
            "manifest.inventoryReviewPaths",
            "KIN-E-MANIFEST",
            "at least one inventory review path is required",
        )
    allowed_change_paths = set(_path_list(
        manifest.get("allowedChangePaths"),
        "manifest.allowedChangePaths",
    ))
    if not set(inventory_review_paths).issubset(allowed_change_paths):
        _raise(
            "manifest.inventoryReviewPaths",
            "KIN-E-MANIFEST",
            "inventory review paths must be declared allowed semantic changes",
        )
    if set(inventory_review_paths) & (fixed_controls | declared_attempt_paths):
        _raise(
            "manifest.inventoryReviewPaths",
            "KIN-E-MANIFEST",
            "reserved control artifacts cannot masquerade as inventory reviews",
        )
    declared_attempt_ids = {
        str(value.get("id"))
        for value in _require_list(core.get("reviewAttempts"), "core.reviewAttempts")
        if isinstance(value, dict)
    }
    for label, state in (("isolated", isolated), ("canonical", canonical)):
        for relative in inventory_review_paths:
            try:
                _read_regular_no_symlinks(
                    state.root,
                    relative,
                    code="KIN-E-MANIFEST",
                    require_single_link=True,
                )
            except KintsugiError:
                _raise(
                    relative,
                    "KIN-E-MANIFEST",
                    f"inventory review is missing or non-regular in the {label} root",
                )
        for relative in sorted(fixed_controls):
            try:
                _read_regular_no_symlinks(
                    state.root,
                    relative,
                    code="KIN-E-MANIFEST",
                    require_single_link=True,
                )
            except KintsugiError:
                _raise(
                    relative,
                    "KIN-E-MANIFEST",
                    f"reserved control file is missing from the {label} root",
                )
        filesystem_ids, obstructions = _filesystem_attempt_state(state.root)
        if obstructions:
            _raise(
                obstructions[0],
                "KIN-E-CONCURRENT",
                f"attempt artifact role is obstructed in the {label} root",
            )
        undeclared_ids = set(filesystem_ids) - declared_attempt_ids
        if undeclared_ids:
            _raise(
                sorted(undeclared_ids)[0],
                "KIN-E-MANIFEST",
                f"undeclared attempt directory exists in the {label} root",
            )
        undeclared = set(_worktree_attempt_paths(state.root)) - declared_attempt_paths
        if undeclared:
            _raise(
                sorted(undeclared)[0],
                "KIN-E-MANIFEST",
                f"undeclared attempt artifact exists in the {label} root",
            )
    included, reserved = _validate_inventory(
        isolated.root, core, manifest, receipt, phase, base_commit
    )
    _validate_claim_partition(
        isolated.root,
        core,
        manifest,
        receipt,
        phase,
        included,
        reserved,
    )
    _validate_protected(isolated, canonical, manifest)
    _validate_scope(
        isolated,
        canonical,
        manifest,
        included,
        fixed_controls | {_SCHEMA_PATH},
    )


def validate_manifest(
    isolated_root: Path,
    canonical_root: Path,
    core: dict[str, object],
    phase: str,
    base_ref: str,
) -> list[Issue]:
    try:
        _validate_manifest_or_raise(isolated_root, canonical_root, core, phase, base_ref)
    except KintsugiError as exc:
        return [_issue(exc.path, exc.code, exc.message)]
    except (OSError, TypeError, ValueError, UnicodeError) as exc:
        return [_issue("manifest", "KIN-E-MANIFEST", f"manifest validation failed safely: {exc.__class__.__name__}")]
    return []


def _frozen_file_record(
    root: Path,
    relative: str,
    read_overrides: _FrozenReads | None,
) -> FileRecord:
    if read_overrides is None:
        return _hash_regular_or_symlink(root, relative)
    frozen = read_overrides.get(relative)
    if frozen is None:
        _raise(relative, "KIN-E-CONCURRENT", "frozen read set does not cover required bytes")
    kind, payload = frozen
    if kind not in {"FILE", "SYMLINK"} or not isinstance(payload, bytes):
        _raise(relative, "KIN-E-CONCURRENT", "frozen read-set member is malformed")
    return FileRecord(relative, kind, raw_hash(payload))


def _frozen_regular_bytes(
    root: Path,
    relative: str,
    read_overrides: _FrozenReads | None,
) -> bytes:
    if read_overrides is None:
        return _read_regular_no_symlinks(
            root,
            relative,
            code="KIN-E-MANIFEST",
            require_single_link=True,
        )
    frozen = read_overrides.get(relative)
    if frozen is None:
        _raise(relative, "KIN-E-CONCURRENT", "frozen read set does not cover required bytes")
    kind, payload = frozen
    if kind != "FILE" or not isinstance(payload, bytes):
        _raise(relative, "KIN-E-CONCURRENT", "required frozen input is not an ordinary file")
    return payload


def _read_control_bytes(
    root: Path,
    relative: str,
    read_overrides: _FrozenReads | None = None,
) -> bytes:
    try:
        return _frozen_regular_bytes(root, relative, read_overrides)
    except KintsugiError as exc:
        _raise(
            relative,
            "KIN-E-MANIFEST",
            exc.message,
        )


def _semantic_diff_paths(
    state: GitState, manifest: dict[str, Any], closure: set[str]
) -> list[str]:
    changed = (
        set(state.committed_paths)
        | set(state.staged_paths)
        | set(state.unstaged_paths)
        | {record.path for record in state.untracked_records}
    )
    allowances = _require_mapping(
        manifest.get("allowedPreexistingUntracked"),
        "manifest.allowedPreexistingUntracked",
    )
    changed -= {
        record.path
        for record in _file_records(
            allowances.get("isolated"),
            "manifest.allowedPreexistingUntracked.isolated",
        )
    }
    semantic: list[str] = []
    for relative in sorted(changed):
        try:
            derived_attempt = _attempt_id_from_path(relative)
        except KintsugiError as exc:
            _raise(relative, "KIN-E-MANIFEST", exc.message)
        if derived_attempt is not None:
            if relative not in closure:
                _raise(
                    relative,
                    "KIN-E-MANIFEST",
                    "undeclared attempt artifact entered the changed-path set",
                )
            continue
        semantic.append(relative)
    return semantic


def _review_subject_projection(target: dict[str, object]) -> dict[str, object]:
    """Return the one canonical preimage for a review-subject digest.

    Task 7 may enrich or validate the target, but it must delegate digest
    normalization here.  Attempt number, retry history, and closure artifact
    paths are transport mechanics; all other reviewed values remain bound.
    """
    projected = copy.deepcopy(_require_mapping(target, "reviewTarget"))
    phase = projected.get("phase")
    current_attempt = projected.get("currentAttemptId")
    if not canonical_attempt(current_attempt, phase):
        _raise(
            "reviewTarget.currentAttemptId",
            "KIN-E-MANIFEST",
            "current review attempt ID is non-canonical",
        )
    prior_attempts = _require_list(
        projected.get("priorReviewAttempts"),
        "reviewTarget.priorReviewAttempts",
    )
    attempt_ids = [current_attempt]
    for index, value in enumerate(prior_attempts):
        attempt = _require_mapping(value, f"reviewTarget.priorReviewAttempts[{index}]")
        attempt_id = attempt.get("id")
        if not canonical_attempt(attempt_id, phase):
            _raise(
                f"reviewTarget.priorReviewAttempts[{index}].id",
                "KIN-E-MANIFEST",
                "prior review attempt ID is non-canonical",
            )
        attempt_ids.append(attempt_id)
    if len(set(attempt_ids)) != len(attempt_ids):
        _raise(
            "reviewTarget.priorReviewAttempts",
            "KIN-E-MANIFEST",
            "review attempt identities are duplicated",
        )
    projected.pop("currentAttemptId", None)
    projected.pop("reviewSubjectDigest", None)
    for field in _PRIOR_REVIEW_FIELDS:
        projected.pop(field, None)
    manifest = _require_mapping(projected.get("manifest"), "reviewTarget.manifest")
    closure = _path_list(
        manifest.get("closureOnlyPaths"),
        "reviewTarget.manifest.closureOnlyPaths",
    )
    expected_closure = tuple(sorted({
        relative
        for attempt_id in attempt_ids
        for relative in attempt_paths(attempt_id)
    }))
    if closure != expected_closure:
        _raise(
            "reviewTarget.manifest.closureOnlyPaths",
            "KIN-E-MANIFEST",
            "review target closure is not the exact attempt-path union",
        )
    semantic_diff = _path_list(
        projected.get("semanticDiffPaths"),
        "reviewTarget.semanticDiffPaths",
    )
    inventory_paths = {
        record.path
        for field in ("candidateFiles", "includedFiles", "finalFiles")
        for record in _file_records(
            manifest.get(field), f"reviewTarget.manifest.{field}"
        )
    }
    for relative in sorted(inventory_paths | set(semantic_diff)):
        try:
            derived_attempt = _attempt_id_from_path(relative)
        except KintsugiError as exc:
            _raise(relative, "KIN-E-MANIFEST", exc.message)
        if derived_attempt is not None:
            _raise(
                relative,
                "KIN-E-MANIFEST",
                "attempt artifact entered the semantic subject",
            )
    manifest["closureOnlyPaths"] = []
    allowed = _path_list(
        manifest.get("allowedChangePaths"),
        "reviewTarget.manifest.allowedChangePaths",
    )
    allowed_attempt_paths: set[str] = set()
    normalized_allowed: list[str] = []
    for relative in allowed:
        try:
            derived_attempt = _attempt_id_from_path(relative)
        except KintsugiError as exc:
            _raise(relative, "KIN-E-MANIFEST", exc.message)
        if derived_attempt is not None:
            allowed_attempt_paths.add(relative)
            continue
        normalized_allowed.append(relative)
    if allowed_attempt_paths != set(expected_closure):
        _raise(
            "reviewTarget.manifest.allowedChangePaths",
            "KIN-E-MANIFEST",
            "attempt-shaped allowances are not the exact declared closure",
        )
    manifest["allowedChangePaths"] = normalized_allowed
    return projected


def _record_collection(
    core: dict[str, object], name: str
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    index: dict[str, dict[str, Any]] = {}
    for position, value in enumerate(_require_list(core.get(name), f"core.{name}")):
        record = _require_mapping(value, f"core.{name}[{position}]")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id or record_id in index:
            _raise(
                f"core.{name}[{position}].id",
                "KIN-E-MANIFEST",
                f"{name} identity is missing or duplicated",
            )
        records.append(record)
        index[record_id] = record
    return records, index


def _decode_rosetta_fixture(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, str) or not value:
        _raise(path, "KIN-E-MANIFEST", "Rosetta fixture payload is not JSON text")

    def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, child in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = child
        return result

    try:
        decoded = json.loads(
            value,
            object_pairs_hook=closed_object,
            parse_constant=lambda constant: (_ for _ in ()).throw(
                ValueError(f"invalid constant: {constant}")
            ),
        )
    except (TypeError, ValueError, json.JSONDecodeError):
        _raise(path, "KIN-E-MANIFEST", "Rosetta fixture payload is invalid JSON")
    if not isinstance(decoded, dict):
        _raise(path, "KIN-E-MANIFEST", "Rosetta fixture payload must be an object")
    return decoded


def _semantic_record_closure(
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
) -> dict[str, list[dict[str, Any]] | set[str]]:
    sources, source_index = _record_collection(core, "sources")
    claims, claim_index = _record_collection(core, "claims")
    trials, trial_index = _record_collection(core, "trials")
    seams, seam_index = _record_collection(core, "seams")
    propagations, propagation_index = _record_collection(core, "propagations")
    antibodies, antibody_index = _record_collection(core, "antibodies")
    discriminators, discriminator_index = _record_collection(core, "discriminators")
    fixtures, _ = _record_collection(core, "fixtures")
    receipts, receipt_index = _record_collection(core, "phaseReceipts")

    selected_receipt_id = receipt.get("id")
    if not isinstance(selected_receipt_id, str) or selected_receipt_id not in receipt_index:
        _raise("receipt.id", "KIN-E-MANIFEST", "selected receipt is absent from the core")
    selected_manifest_claims = set(
        _require_list(manifest.get("harvestedClaimIds"), "manifest.harvestedClaimIds")
    )
    root_claim_ids = _require_list(receipt.get("claimIds"), "receipt.claimIds")
    if not root_claim_ids or any(not isinstance(value, str) for value in root_claim_ids):
        _raise("receipt.claimIds", "KIN-E-MANIFEST", "receipt claim roots are invalid")

    def dependency_fields(dependency: dict[str, Any], dependency_id: str) -> list[str]:
        if dependency.get("status") != "VERIFIED":
            _raise(
                dependency_id,
                "KIN-E-MANIFEST",
                "dependency receipt is not VERIFIED",
            )
        digest = dependency.get("validationDigest")
        if (
            not isinstance(digest, str)
            or not digest.startswith("sha256:")
            or len(digest) != 71
            or any(character not in "0123456789abcdef" for character in digest[7:])
        ):
            _raise(
                dependency_id,
                "KIN-E-MANIFEST",
                "dependency receipt validation digest is invalid",
            )
        _repo_path(
            dependency.get("validationBundlePath"),
            f"receipt.{dependency_id}.validationBundlePath",
        )
        values = _require_list(
            dependency.get("dependsOnReceiptIds"),
            f"receipt.{dependency_id}.dependsOnReceiptIds",
        )
        if (
            any(not isinstance(value, str) or not value for value in values)
            or len(set(values)) != len(values)
        ):
            _raise(
                f"receipt.{dependency_id}.dependsOnReceiptIds",
                "KIN-E-MANIFEST",
                "dependency receipt links are invalid",
            )
        return values

    dependency_receipt_ids: set[str] = set()
    visiting_receipts: list[str] = [selected_receipt_id]
    visiting_receipt_positions: dict[str, int] = {selected_receipt_id: 0}

    def visit_dependency(dependency_id: str) -> None:
        if dependency_id in visiting_receipt_positions:
            cycle = (
                visiting_receipts[visiting_receipt_positions[dependency_id]:]
                + [dependency_id]
            )
            _raise(
                "receipt.dependsOnReceiptIds",
                "KIN-E-MANIFEST",
                "dependency receipt cycle: " + " -> ".join(cycle),
            )
        if dependency_id in dependency_receipt_ids:
            return
        dependency = receipt_index.get(dependency_id)
        if dependency is None:
            _raise(
                dependency_id,
                "KIN-E-MANIFEST",
                "dependency receipt is absent",
            )
        visiting_receipt_positions[dependency_id] = len(visiting_receipts)
        visiting_receipts.append(dependency_id)
        for child_id in dependency_fields(dependency, dependency_id):
            visit_dependency(child_id)
        visiting_receipts.pop()
        visiting_receipt_positions.pop(dependency_id, None)
        dependency_receipt_ids.add(dependency_id)

    direct_dependencies = _require_list(
        receipt.get("dependsOnReceiptIds"), "receipt.dependsOnReceiptIds"
    )
    if (
        any(not isinstance(value, str) or not value for value in direct_dependencies)
        or len(set(direct_dependencies)) != len(direct_dependencies)
    ):
        _raise(
            "receipt.dependsOnReceiptIds",
            "KIN-E-MANIFEST",
            "selected receipt dependency links are invalid",
        )
    for dependency_id in direct_dependencies:
        visit_dependency(dependency_id)

    selected_receipts = [
        receipt if receipt_id == selected_receipt_id else receipt_index[receipt_id]
        for receipt_id in [selected_receipt_id]
        + [
            value["id"]
            for value in receipts
            if value["id"] in dependency_receipt_ids
        ]
    ]

    def declared_record_ids(
        field: str,
        index: dict[str, dict[str, Any]],
        label: str,
    ) -> set[str]:
        owners: dict[str, str] = {}
        for owner in selected_receipts:
            owner_id = str(owner["id"])
            values = _require_list(owner.get(field), f"receipt.{owner_id}.{field}")
            if (
                any(not isinstance(value, str) or not value for value in values)
                or len(set(values)) != len(values)
            ):
                _raise(
                    f"receipt.{owner_id}.{field}",
                    "KIN-E-MANIFEST",
                    f"declared {label} identities are invalid",
                )
            for record_id in values:
                if record_id in owners:
                    _raise(
                        record_id,
                        "KIN-E-MANIFEST",
                        f"{label} is declared by multiple receipts",
                    )
                record = index.get(record_id)
                if record is None or record.get("receiptId") != owner_id:
                    _raise(
                        record_id,
                        "KIN-E-MANIFEST",
                        f"declared {label} is absent or owned by another receipt",
                    )
                owners[record_id] = owner_id
        return set(owners)

    declared_trial_ids = declared_record_ids("trialIds", trial_index, "trial")
    declared_seam_ids = declared_record_ids("seamIds", seam_index, "seam")
    declared_propagation_ids = declared_record_ids(
        "propagationIds", propagation_index, "propagation"
    )
    for trial_id in declared_trial_ids:
        seam_id = trial_index[trial_id].get("seamId")
        if seam_id is not None and seam_id not in declared_seam_ids:
            _raise(
                trial_id,
                "KIN-E-MANIFEST",
                "declared trial seam is absent from the receipt seam set",
            )
    candidate_seam_ids = set(declared_seam_ids)

    graph: dict[str, set[str]] = {claim_id: set() for claim_id in claim_index}
    for claim_id, claim in claim_index.items():
        graph[claim_id].update(
            value for value in claim.get("dependencyClaimIds", ())
            if isinstance(value, str)
        )
        graph[claim_id].update(
            link.get("supportingClaimId")
            for link in claim.get("supportLinks", ())
            if isinstance(link, dict) and isinstance(link.get("supportingClaimId"), str)
        )
        surviving = claim.get("survivingIfKilled")
        if isinstance(surviving, dict):
            graph[claim_id].update(
                value for value in surviving.get("claimIds", ())
                if isinstance(value, str)
            )

    for fixture_position, fixture in enumerate(fixtures):
        attached_seams = {
            str(antibody.get("seamId"))
            for antibody_id in fixture.get("antibodyIds", ())
            for antibody in [antibody_index.get(antibody_id, {})]
            if antibody.get("semanticEvaluator") == "ROSETTA_TRANSFER"
            and antibody.get("seamId") in candidate_seam_ids
        }
        if not attached_seams or fixture.get("payloadKind") != "JSON":
            continue
        payload = _decode_rosetta_fixture(
            fixture.get("payload"), f"core.fixtures[{fixture_position}].payload"
        )
        endpoints = [payload.get("targetClaimId")]
        if payload.get("bridgeClaimId") is not None:
            endpoints.append(payload.get("bridgeClaimId"))
        if any(not isinstance(value, str) for value in endpoints):
            _raise(
                f"core.fixtures[{fixture_position}].payload",
                "KIN-E-MANIFEST",
                "Rosetta fixture endpoints are invalid",
            )
        for seam_id in attached_seams:
            seam = seam_index.get(seam_id)
            if seam is None or not isinstance(seam.get("claimId"), str):
                _raise(seam_id, "KIN-E-MANIFEST", "Rosetta fixture seam is unresolved")
            graph.setdefault(str(seam["claimId"]), set()).update(endpoints)

    visiting: list[str] = []
    visiting_positions: dict[str, int] = {}
    visited: set[str] = set()

    def visit(claim_id: str) -> None:
        if claim_id in visited:
            return
        if claim_id in visiting_positions:
            cycle = visiting[visiting_positions[claim_id]:] + [claim_id]
            _raise(
                "reviewTarget.claims",
                "KIN-E-MANIFEST",
                "semantic review closure contains a cycle: " + " -> ".join(cycle),
            )
        claim = claim_index.get(claim_id)
        if claim is None:
            _raise(claim_id, "KIN-E-MANIFEST", "semantic review closure claim is absent")
        visiting_positions[claim_id] = len(visiting)
        visiting.append(claim_id)
        for endpoint in sorted(graph.get(claim_id, ())):
            visit(endpoint)
        visiting.pop()
        visiting_positions.pop(claim_id, None)
        visited.add(claim_id)

    for claim_id in root_claim_ids:
        visit(claim_id)

    for claim_id in visited:
        if claim_id in selected_manifest_claims:
            continue
        owners = [
            dependency
            for dependency in receipts
            if claim_id in dependency.get("claimIds", ())
        ]
        if len(owners) != 1:
            _raise(
                claim_id,
                "KIN-E-MANIFEST",
                "external closure claim has no unique dependency receipt",
            )
        owner = owners[0]
        if owner.get("id") not in dependency_receipt_ids:
            _raise(
                claim_id,
                "KIN-E-MANIFEST",
                "external closure claim lacks a verified dependency bundle",
            )

    selected_trials = {
        trial["id"]
        for trial in trials
        if trial["id"] in declared_trial_ids and trial.get("claimId") in visited
    }

    selected_seams = {
        seam_id
        for seam_id in declared_seam_ids
        if seam_index[seam_id].get("claimId") in visited
    }
    selected_seams.update(
        trial_index[trial_id].get("seamId")
        for trial_id in selected_trials
        if trial_index[trial_id].get("seamId") is not None
    )
    selected_seams = {
        seam_id for seam_id in selected_seams
        if isinstance(seam_id, str)
        and seam_id in seam_index
        and seam_index[seam_id].get("claimId") in visited
    }

    selected_propagations = {
        propagation["id"]
        for propagation in propagations
        if propagation["id"] in declared_propagation_ids
        and propagation.get("seamId") in selected_seams
    }

    selected_antibodies = {
        antibody["id"] for antibody in antibodies
        if antibody.get("seamId") in selected_seams
    }
    selected_fixtures = {
        fixture["id"] for fixture in fixtures
        if set(fixture.get("seamIds", ())) & selected_seams
        or set(fixture.get("antibodyIds", ())) & selected_antibodies
    }
    selected_discriminators: set[str] = set()
    for trial_id in selected_trials:
        selected_discriminators.update(
            value for value in trial_index[trial_id].get("discriminatorIds", ())
            if isinstance(value, str)
        )
    for seam_id in selected_seams:
        selected_discriminators.update(
            value for value in seam_index[seam_id].get("discriminatorIds", ())
            if isinstance(value, str)
        )
    if not selected_discriminators.issubset(discriminator_index):
        _raise(
            "reviewTarget.discriminators",
            "KIN-E-MANIFEST",
            "closure discriminator is absent",
        )

    selected_source_ids: set[str] = set()
    for claim_id in visited:
        claim = claim_index[claim_id]
        owner_id = claim.get("ownerSourceId")
        if isinstance(owner_id, str):
            selected_source_ids.add(owner_id)
        for premise in claim.get("premises", ()):
            if isinstance(premise, dict):
                selected_source_ids.update(
                    value for value in premise.get("sourceIds", ())
                    if isinstance(value, str)
                )
    for seam_id in selected_seams:
        seam = seam_index[seam_id]
        owner_id = seam.get("ownerSource")
        if isinstance(owner_id, str):
            selected_source_ids.add(owner_id)
        selected_source_ids.update(
            value for value in seam.get("sourceIds", ())
            if isinstance(value, str)
        )
    for propagation_id in selected_propagations:
        source_id = propagation_index[propagation_id].get("derivativeSourceId")
        if isinstance(source_id, str):
            selected_source_ids.add(source_id)
    if not selected_source_ids.issubset(source_index):
        _raise("reviewTarget.sources", "KIN-E-MANIFEST", "closure source is absent")

    return {
        "sources": [value for value in sources if value["id"] in selected_source_ids],
        "claims": [value for value in claims if value["id"] in visited],
        "trials": [value for value in trials if value["id"] in selected_trials],
        "seams": [value for value in seams if value["id"] in selected_seams],
        "propagations": [
            value for value in propagations if value["id"] in selected_propagations
        ],
        "antibodies": [
            value for value in antibodies if value["id"] in selected_antibodies
        ],
        "discriminators": [
            value for value in discriminators if value["id"] in selected_discriminators
        ],
        "fixtures": [value for value in fixtures if value["id"] in selected_fixtures],
        "seamIds": selected_seams,
        "dependencyReceipts": [
            {
                "id": value["id"],
                "validationDigest": value["validationDigest"],
            }
            for value in receipts
            if value["id"] in dependency_receipt_ids
        ],
    }


def _subject_target_value(
    root: Path,
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    phase: str,
    attempt_id: str,
    state: GitState,
    read_overrides: _FrozenReads | None = None,
) -> dict[str, object]:
    receipt_bytes = _read_control_bytes(
        root,
        _repo_path(receipt.get("path"), "receipt.path"),
        read_overrides,
    )
    receipt_sync = synchronize_receipt_markdown(
        receipt_bytes,
        receipt,
        path=str(receipt.get("path")),
        target_frozen=True,
    )
    if receipt_sync.issues:
        issue = receipt_sync.issues[0]
        raise KintsugiError(issue.code, issue.path, issue.message)

    closure = _semantic_record_closure(core, manifest, receipt)
    seams = closure["seams"]
    assert isinstance(seams, list)
    ledger_bytes = _read_control_bytes(root, _LEDGER_PATH, read_overrides)
    all_seams, _ = _record_collection(core, "seams")
    ledger_sync = synchronize_ledger_markdown(
        ledger_bytes,
        all_seams,
        path=_LEDGER_PATH,
    )
    if ledger_sync.issues:
        issue = ledger_sync.issues[0]
        raise KintsugiError(issue.code, issue.path, issue.message)

    schema_sha256 = raw_hash(
        _read_control_bytes(root, _SCHEMA_PATH, read_overrides)
    )
    attempts = _require_list(core.get("reviewAttempts"), "core.reviewAttempts")
    artifacts = _require_list(
        core.get("reviewAttemptArtifacts"), "core.reviewAttemptArtifacts"
    )
    prior_ids = {
        value.get("id")
        for value in attempts
        if (
            isinstance(value, dict)
            and value.get("id") != attempt_id
            and value.get("phase") == phase
            and value.get("receiptId") == receipt.get("id")
        )
    }
    target: dict[str, object] = {
        "schemaVersion": core.get("schemaVersion"),
        "phase": phase,
        "currentAttemptId": attempt_id,
        "receiptId": receipt.get("id"),
        "receiptNarrativeRawSha256": receipt_sync.narrative_raw_sha256,
        # This field is deliberately removed by _review_subject_projection.
        "reviewSubjectDigest": None,
        "manifest": copy.deepcopy(manifest),
        "sources": copy.deepcopy(closure["sources"]),
        "claims": copy.deepcopy(closure["claims"]),
        "trials": copy.deepcopy(closure["trials"]),
        "seams": [project_review_seam(value) for value in seams],
        "propagations": copy.deepcopy(closure["propagations"]),
        "antibodies": copy.deepcopy(closure["antibodies"]),
        "discriminators": copy.deepcopy(closure["discriminators"]),
        "fixtures": copy.deepcopy(closure["fixtures"]),
        "schemaSha256": schema_sha256,
        "ledgerPreambleRawSha256": ledger_sync.preamble.raw_sha256,
        "ledgerSemanticSections": [
            {
                "id": section.id,
                "narrativeRawSha256": section.narrative_raw_sha256,
                "seamProjection": copy.deepcopy(section.seam_projection),
            }
            for section in ledger_sync.sections
            if section.id in closure["seamIds"]
        ],
        "semanticDiffPaths": _semantic_diff_paths(
            state,
            manifest,
            set(_path_list(manifest.get("closureOnlyPaths"), "manifest.closureOnlyPaths")),
        ),
        "priorReviewAttempts": copy.deepcopy([
            value for value in attempts
            if isinstance(value, dict) and value.get("id") in prior_ids
        ]),
        "priorReviewAttemptArtifacts": copy.deepcopy([
            value for value in artifacts
            if isinstance(value, dict) and value.get("attemptId") in prior_ids
        ]),
        "priorReviewAttestations": copy.deepcopy([
            value for value in _require_list(
                core.get("reviewAttestations"), "core.reviewAttestations"
            )
            if isinstance(value, dict) and value.get("attemptId") in prior_ids
        ]),
        "priorReviewFindings": copy.deepcopy([
            value for value in _require_list(
                core.get("reviewFindings"), "core.reviewFindings"
            )
            if isinstance(value, dict) and value.get("attemptId") in prior_ids
        ]),
        "priorReviewFindingDispositions": copy.deepcopy([
            value for value in _require_list(
                core.get("reviewFindingDispositions"),
                "core.reviewFindingDispositions",
            )
            if isinstance(value, dict)
            and value.get("successorAttemptId") in (prior_ids | {attempt_id})
        ]),
    }
    return target


def _validate_disposition_input_shape(value: Any, path: str) -> dict[str, Any]:
    record = _require_mapping(value, path)
    if set(record) != _DISPOSITION_INPUT_FIELDS:
        _raise(path, "KIN-E-MANIFEST", "finding disposition input shape is not exact")
    for field in (
        "claimIds",
        "seamIds",
        "ledgerSectionIds",
        "receiptIds",
        "subjectPaths",
        "discriminatorIds",
        "evidenceFiles",
    ):
        values = _require_list(record.get(field), f"{path}.{field}")
        if field != "evidenceFiles":
            if any(not isinstance(item, str) or not item for item in values):
                _raise(
                    f"{path}.{field}",
                    "KIN-E-MANIFEST",
                    "disposition endpoints must be non-empty strings",
                )
            if len(set(values)) != len(values):
                _raise(
                    f"{path}.{field}",
                    "KIN-E-MANIFEST",
                    "disposition endpoints must be unique",
                )
    evidence_values = _require_list(record.get("evidenceFiles"), f"{path}.evidenceFiles")
    evidence_keys: list[tuple[Any, Any]] = []
    for index, value in enumerate(evidence_values):
        evidence = _require_mapping(value, f"{path}.evidenceFiles[{index}]")
        if set(evidence) != {"path", "sha256"}:
            _raise(
                f"{path}.evidenceFiles[{index}]",
                "KIN-E-MANIFEST",
                "process evidence shape is not exact",
            )
        relative = _repo_path(evidence.get("path"), f"{path}.evidenceFiles[{index}].path")
        digest = evidence.get("sha256")
        if (
            not isinstance(digest, str)
            or not digest.startswith("sha256:")
            or len(digest) != 71
            or any(character not in "0123456789abcdef" for character in digest[7:])
        ):
            _raise(
                f"{path}.evidenceFiles[{index}].sha256",
                "KIN-E-MANIFEST",
                "process evidence hash is invalid",
            )
        evidence_keys.append((relative, digest))
    if len(set(evidence_keys)) != len(evidence_keys):
        _raise(
            f"{path}.evidenceFiles",
            "KIN-E-MANIFEST",
            "process evidence records must be unique",
        )
    if not isinstance(record.get("findingId"), str):
        _raise(f"{path}.findingId", "KIN-E-MANIFEST", "finding ID is invalid")
    if not isinstance(record.get("rationale"), str) or not record["rationale"]:
        _raise(f"{path}.rationale", "KIN-E-MANIFEST", "disposition rationale is required")
    if record.get("disposition") not in {"ADDRESSED", "DISPUTED", "PROCESS_INVALID"}:
        _raise(f"{path}.disposition", "KIN-E-MANIFEST", "disposition kind is invalid")
    return record


def _decode_canonical_object(payload: bytes, path: str) -> dict[str, Any]:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=lambda constant: (_ for _ in ()).throw(
                ValueError(f"invalid constant: {constant}")
            ),
        )
        rendered = canonical_json_bytes(value)
    except (
        UnicodeDecodeError,
        UnicodeError,
        ValueError,
        json.JSONDecodeError,
        RecursionError,
    ):
        _raise(path, "KIN-E-MANIFEST", "review target is not bounded canonical JSON")
    if payload != rendered or not isinstance(value, dict):
        _raise(path, "KIN-E-MANIFEST", "review target is not a canonical JSON object")
    return value


def _id_index(target: dict[str, Any], field: str) -> dict[str, dict[str, Any]]:
    records = _require_list(target.get(field), f"reviewTarget.{field}")
    index: dict[str, dict[str, Any]] = {}
    for position, value in enumerate(records):
        record = _require_mapping(value, f"reviewTarget.{field}[{position}]")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id or record_id in index:
            _raise(
                f"reviewTarget.{field}[{position}].id",
                "KIN-E-MANIFEST",
                "review-target endpoint ID is missing or duplicated",
            )
        index[record_id] = record
    return index


def _predecessor_review_target(
    root: Path,
    core: dict[str, object],
    predecessor: dict[str, Any],
    read_overrides: _FrozenReads | None,
) -> dict[str, Any]:
    predecessor_id = predecessor.get("id")
    target_path = _repo_path(
        predecessor.get("reviewTargetPath"),
        "predecessor.reviewTargetPath",
    )
    artifacts = [
        value
        for value in _require_list(
            core.get("reviewAttemptArtifacts"), "core.reviewAttemptArtifacts"
        )
        if isinstance(value, dict) and value.get("attemptId") == predecessor_id
    ]
    if len(artifacts) != 1:
        _raise(target_path, "KIN-E-MANIFEST", "predecessor target artifact is absent")
    payload = _frozen_regular_bytes(root, target_path, read_overrides)
    expected_raw_hash = artifacts[0].get("reviewTargetSha256")
    if expected_raw_hash is None or raw_hash(payload) != expected_raw_hash:
        _raise(target_path, "KIN-E-MANIFEST", "predecessor target bytes are not hash-bound")
    target = _decode_canonical_object(payload, target_path)
    if (
        target.get("currentAttemptId") != predecessor_id
        or target.get("phase") != predecessor.get("phase")
        or target.get("receiptId") != predecessor.get("receiptId")
    ):
        _raise(target_path, "KIN-E-MANIFEST", "predecessor target identity is inconsistent")
    subject_digest = raw_hash(canonical_json_bytes(_review_subject_projection(target)))
    if subject_digest != predecessor.get("reviewSubjectDigest"):
        _raise(target_path, "KIN-E-MANIFEST", "predecessor subject digest is inconsistent")
    return target


def _validate_disposition_endpoint_laws(
    root: Path,
    core: dict[str, object],
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    predecessor: dict[str, Any] | None,
    successor: dict[str, Any],
    dispositions: list[dict[str, object]],
    successor_target: dict[str, object],
    read_overrides: _FrozenReads | None,
) -> None:
    if predecessor is None:
        if dispositions:
            _raise(
                "findingDispositions",
                "KIN-E-MANIFEST",
                "a first review attempt cannot carry predecessor dispositions",
            )
        return

    semantic_dispositions = [
        value for value in dispositions if value.get("disposition") != "PROCESS_INVALID"
    ]
    predecessor_digest = predecessor.get("reviewSubjectDigest")
    successor_digest = successor.get("reviewSubjectDigest")
    if semantic_dispositions and successor_digest == predecessor_digest:
        _raise(
            "findingDispositions",
            "KIN-E-MANIFEST",
            "ADDRESSED or DISPUTED disposition requires a changed review subject",
        )
    if successor_digest == predecessor_digest and any(
        value.get("disposition") != "PROCESS_INVALID" for value in dispositions
    ):
        _raise(
            "findingDispositions",
            "KIN-E-MANIFEST",
            "same-subject retry permits only PROCESS_INVALID dispositions",
        )
    if not semantic_dispositions:
        return

    successor_target_value = _require_mapping(successor_target, "successorReviewTarget")
    claims = _id_index(successor_target_value, "claims")
    seams = _id_index(successor_target_value, "seams")
    ledger_sections = _id_index(successor_target_value, "ledgerSemanticSections")
    discriminators = _id_index(successor_target_value, "discriminators")
    target_manifest = _require_mapping(
        successor_target_value.get("manifest"), "successorReviewTarget.manifest"
    )
    final_records = {
        record.path: record
        for record in _file_records(
            target_manifest.get("finalFiles"),
            "successorReviewTarget.manifest.finalFiles",
        )
    }
    fixed_controls, attempt_controls = _reserved_control_paths(core, receipt, str(receipt.get("phase")))
    reserved_controls = fixed_controls | attempt_controls | {_SCHEMA_PATH}
    closure = set(
        _path_list(
            manifest.get("closureOnlyPaths"),
            "successorReviewTarget.manifest.closureOnlyPaths",
        )
    )
    receipt_id = successor_target_value.get("receiptId")

    predecessor_target: dict[str, Any] | None = None
    predecessor_claims: dict[str, dict[str, Any]] = {}
    predecessor_seams: dict[str, dict[str, Any]] = {}
    predecessor_ledger_sections: dict[str, dict[str, Any]] = {}
    predecessor_final_records: dict[str, FileRecord] = {}

    def load_predecessor_endpoint_indexes() -> None:
        nonlocal predecessor_target
        nonlocal predecessor_claims
        nonlocal predecessor_seams
        nonlocal predecessor_ledger_sections
        nonlocal predecessor_final_records
        if predecessor_target is not None:
            return
        predecessor_target = _predecessor_review_target(
            root, core, predecessor, read_overrides
        )
        predecessor_claims = _id_index(predecessor_target, "claims")
        predecessor_seams = _id_index(predecessor_target, "seams")
        predecessor_ledger_sections = _id_index(
            predecessor_target, "ledgerSemanticSections"
        )
        predecessor_manifest = _require_mapping(
            predecessor_target.get("manifest"), "predecessorReviewTarget.manifest"
        )
        predecessor_final_records = {
            record.path: record
            for record in _file_records(
                predecessor_manifest.get("finalFiles"),
                "predecessorReviewTarget.manifest.finalFiles",
            )
        }

    for ordinal, record in enumerate(dispositions):
        kind = record.get("disposition")
        if kind == "PROCESS_INVALID":
            continue
        base = f"findingDispositions[{ordinal}]"
        changed_endpoint = False

        for claim_id in record.get("claimIds", []):
            if claim_id not in claims:
                _raise(
                    f"{base}.claimIds",
                    "KIN-E-MANIFEST",
                    f"claim endpoint is outside the successor subject: {claim_id}",
                )
            if kind == "ADDRESSED":
                load_predecessor_endpoint_indexes()
                changed_endpoint |= predecessor_claims.get(str(claim_id)) != claims[claim_id]

        for seam_id in record.get("seamIds", []):
            if seam_id not in seams:
                _raise(
                    f"{base}.seamIds",
                    "KIN-E-MANIFEST",
                    f"seam endpoint is outside the successor subject: {seam_id}",
                )
            if kind == "ADDRESSED":
                load_predecessor_endpoint_indexes()
                changed_endpoint |= predecessor_seams.get(str(seam_id)) != seams[seam_id]

        for section_id in record.get("ledgerSectionIds", []):
            if section_id == "LEDGER-PREAMBLE":
                if kind == "ADDRESSED":
                    load_predecessor_endpoint_indexes()
                    assert predecessor_target is not None
                    changed_endpoint |= (
                        predecessor_target.get("ledgerPreambleRawSha256")
                        != successor_target_value.get("ledgerPreambleRawSha256")
                    )
                continue
            if section_id not in ledger_sections:
                _raise(
                    f"{base}.ledgerSectionIds",
                    "KIN-E-MANIFEST",
                    f"ledger endpoint is outside the successor subject: {section_id}",
                )
            if kind == "ADDRESSED":
                load_predecessor_endpoint_indexes()
                changed_endpoint |= (
                    predecessor_ledger_sections.get(str(section_id))
                    != ledger_sections[section_id]
                )

        for disposition_receipt_id in record.get("receiptIds", []):
            if disposition_receipt_id != receipt_id:
                _raise(
                    f"{base}.receiptIds",
                    "KIN-E-MANIFEST",
                    "receipt endpoint is outside the successor chain",
                )
            if kind == "ADDRESSED":
                load_predecessor_endpoint_indexes()
                assert predecessor_target is not None
                changed_endpoint |= (
                    predecessor_target.get("receiptNarrativeRawSha256")
                    != successor_target_value.get("receiptNarrativeRawSha256")
                )

        for subject_path in record.get("subjectPaths", []):
            if (
                subject_path in reserved_controls
                or subject_path in closure
                or subject_path not in final_records
            ):
                _raise(
                    f"{base}.subjectPaths",
                    "KIN-E-MANIFEST",
                    f"subject path is not a non-control final source: {subject_path}",
                )
            if kind == "ADDRESSED":
                load_predecessor_endpoint_indexes()
                changed_endpoint |= (
                    predecessor_final_records.get(str(subject_path))
                    != final_records[subject_path]
                )

        if kind == "DISPUTED":
            for discriminator_id in record.get("discriminatorIds", []):
                if discriminator_id not in discriminators:
                    _raise(
                        f"{base}.discriminatorIds",
                        "KIN-E-MANIFEST",
                        f"discriminator is outside the successor subject: {discriminator_id}",
                    )
        elif kind == "ADDRESSED" and not changed_endpoint:
            _raise(
                base,
                "KIN-E-MANIFEST",
                "ADDRESSED names no endpoint whose canonical projection changed",
            )


def _expand_finding_dispositions(
    root: Path,
    core: dict[str, object],
    manifest: dict[str, Any],
    predecessor_id: str | None,
    successor_id: str,
    inputs: list[dict[str, object]] | None,
    read_overrides: _FrozenReads | None = None,
) -> list[dict[str, object]]:
    raw_inputs = [] if inputs is None else inputs
    if not isinstance(raw_inputs, list):
        _raise("findingDispositions", "KIN-E-MANIFEST", "finding dispositions must be a list")
    if predecessor_id is None:
        if raw_inputs:
            _raise(
                "findingDispositions",
                "KIN-E-MANIFEST",
                "a first review attempt cannot carry predecessor dispositions",
            )
        return []
    findings = [
        value
        for value in _require_list(core.get("reviewFindings"), "core.reviewFindings")
        if isinstance(value, dict) and value.get("attemptId") == predecessor_id
    ]
    expected_ids = sorted(str(value.get("id")) for value in findings)
    parsed = [
        _validate_disposition_input_shape(value, f"findingDispositions[{index}]")
        for index, value in enumerate(raw_inputs)
    ]
    if [value.get("findingId") for value in parsed] != expected_ids:
        _raise(
            "findingDispositions",
            "KIN-E-MANIFEST",
            "dispositions must exactly cover predecessor findings in finding-ID order",
        )

    artifact_by_attempt = {
        value.get("attemptId"): value
        for value in _require_list(
            core.get("reviewAttemptArtifacts"), "core.reviewAttemptArtifacts"
        )
        if isinstance(value, dict)
    }
    attempt_by_id = {
        value.get("id"): value
        for value in _require_list(core.get("reviewAttempts"), "core.reviewAttempts")
        if isinstance(value, dict)
    }
    predecessor = attempt_by_id.get(predecessor_id)
    artifact = artifact_by_attempt.get(predecessor_id)
    if predecessor is None or artifact is None:
        _raise("findingDispositions", "KIN-E-MANIFEST", "predecessor evidence is absent")
    predecessor_evidence = {
        predecessor.get("reviewTargetPath"): artifact.get("reviewTargetSha256"),
        predecessor.get("logicReviewPath"): artifact.get("logicReviewSha256"),
        predecessor.get("btjReviewPath"): artifact.get("btjReviewSha256"),
    }
    final_records = {
        value.path: value
        for value in _file_records(manifest.get("finalFiles"), "manifest.finalFiles")
    }
    expanded: list[dict[str, object]] = []
    for ordinal, record in enumerate(parsed, start=1):
        disposition = record["disposition"]
        semantic_lists = (
            record["claimIds"],
            record["seamIds"],
            record["ledgerSectionIds"],
            record["receiptIds"],
            record["subjectPaths"],
        )
        if disposition == "PROCESS_INVALID":
            if any(semantic_lists) or record["discriminatorIds"] or not record["evidenceFiles"]:
                _raise(
                    f"findingDispositions[{ordinal - 1}]",
                    "KIN-E-MANIFEST",
                    "PROCESS_INVALID requires only bound process evidence",
                )
            for evidence_index, raw_evidence in enumerate(record["evidenceFiles"]):
                evidence = _require_mapping(
                    raw_evidence,
                    f"findingDispositions[{ordinal - 1}].evidenceFiles[{evidence_index}]",
                )
                if set(evidence) != {"path", "sha256"}:
                    _raise(
                        f"findingDispositions[{ordinal - 1}].evidenceFiles[{evidence_index}]",
                        "KIN-E-MANIFEST",
                        "process evidence shape is not exact",
                    )
                relative = _repo_path(evidence.get("path"), "processEvidence.path")
                digest = evidence.get("sha256")
                if predecessor_evidence.get(relative) == digest and digest is not None:
                    continue
                final_record = final_records.get(relative)
                if (
                    final_record is None
                    or final_record.kind != "FILE"
                    or final_record.sha256 != digest
                ):
                    _raise(relative, "KIN-E-MANIFEST", "process evidence is not hash-bound")
                if _frozen_file_record(root, relative, read_overrides) != final_record:
                    _raise(relative, "KIN-E-MANIFEST", "process evidence bytes drifted")
        elif disposition == "ADDRESSED":
            if (
                not any(semantic_lists)
                or record["discriminatorIds"]
                or record["evidenceFiles"]
            ):
                _raise(
                    f"findingDispositions[{ordinal - 1}]",
                    "KIN-E-MANIFEST",
                    "ADDRESSED requires a semantic endpoint and no discriminator/process evidence",
                )
        elif not record["discriminatorIds"] or record["evidenceFiles"]:
            _raise(
                f"findingDispositions[{ordinal - 1}]",
                "KIN-E-MANIFEST",
                "DISPUTED requires a resolving discriminator and no process evidence",
            )
        expanded.append({
            "id": f"RFD-{successor_id}-{ordinal:03d}",
            "fromAttemptId": predecessor_id,
            "successorAttemptId": successor_id,
            **copy.deepcopy(record),
        })
    return expanded


def freeze_manifest_value(
    isolated_root: Path,
    canonical_root: Path,
    core: dict[str, object],
    phase: str,
    base_ref: str,
    final: bool,
    finding_dispositions: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    issues = validate_manifest(isolated_root, canonical_root, core, phase, base_ref)
    if issues:
        issue = issues[0]
        raise KintsugiError(issue.code, issue.path, issue.message)
    if not final:
        return copy.deepcopy(core)

    _, receipt = _selected_manifest_receipt(core, phase)
    if receipt.get("status") != "DRAFT":
        _raise("receipt.status", "KIN-E-MANIFEST", "final freeze requires a DRAFT receipt")
    prior_attempt_id = receipt.get("reviewAttemptId")
    if prior_attempt_id is not None:
        if not isinstance(prior_attempt_id, str):
            _raise("receipt.reviewAttemptId", "KIN-E-MANIFEST", "attempt pointer is invalid")
        _validate_predecessor_fence(
            isolated_root,
            core,
            phase,
            str(receipt.get("id")),
            _CORE_PATH,
        )
    plan = _plan_next_attempt(
        isolated_root,
        core,
        phase,
        str(receipt.get("id")),
    )
    return _construct_frozen_manifest_value_with_plan(
        isolated_root,
        canonical_root,
        core,
        phase,
        base_ref,
        final,
        finding_dispositions,
        attempt_plan=plan,
    )


def _freeze_manifest_value_with_plan(
    isolated_root: Path,
    canonical_root: Path,
    core: dict[str, object],
    phase: str,
    base_ref: str,
    final: bool,
    finding_dispositions: list[dict[str, object]] | None = None,
    *,
    attempt_plan: AttemptPlan,
    expected_head: str,
    expected_core_sha256: str,
    read_overrides: _FrozenReads | None = None,
    frozen_git_state: GitState | None = None,
) -> dict[str, object]:
    """Freeze with the exact attempt durably reserved under the transition lock."""
    _, receipt = _selected_manifest_receipt(core, phase)
    common_dir = resolve_git_common_dir(isolated_root)
    matching = [
        record
        for record in _reservation_records(common_dir)
        if record.get("id") == attempt_plan.id
    ]
    expected_reservation = {
        "id": attempt_plan.id,
        "phase": attempt_plan.phase,
        "receiptId": attempt_plan.receipt_id,
        "expectedHead": expected_head,
        "expectedCoreSha256": expected_core_sha256,
    }
    if len(matching) != 1 or matching[0] != expected_reservation:
        _raise(
            "reviewAttempts",
            "KIN-E-CONCURRENT",
            "attempt plan is not bound to the exact durable reservation",
        )
    expected_plan = _plan_next_attempt(
        isolated_root,
        core,
        phase,
        str(receipt.get("id")),
        ignore_reservation_id=attempt_plan.id,
    )
    if expected_plan != attempt_plan:
        _raise(
            "reviewAttempts",
            "KIN-E-CONCURRENT",
            "reserved attempt is not the canonical next allocation",
        )
    return _construct_frozen_manifest_value_with_plan(
        isolated_root,
        canonical_root,
        core,
        phase,
        base_ref,
        final,
        finding_dispositions,
        attempt_plan=attempt_plan,
        read_overrides=read_overrides,
        frozen_git_state=frozen_git_state,
    )


def _construct_frozen_manifest_value_with_plan(
    isolated_root: Path,
    canonical_root: Path,
    core: dict[str, object],
    phase: str,
    base_ref: str,
    final: bool,
    finding_dispositions: list[dict[str, object]] | None = None,
    *,
    attempt_plan: AttemptPlan,
    read_overrides: _FrozenReads | None = None,
    frozen_git_state: GitState | None = None,
) -> dict[str, object]:
    """Construct prospective bytes for one already-validated attempt plan.

    This lower pure helper exists so the public read-only preview can preserve
    its frozen signature.  The transactional renderer must use the
    reservation-verifying wrapper above.
    """
    issues = validate_manifest(isolated_root, canonical_root, core, phase, base_ref)
    if issues:
        issue = issues[0]
        raise KintsugiError(issue.code, issue.path, issue.message)
    if not final:
        return copy.deepcopy(core)

    _, current_receipt = _selected_manifest_receipt(core, phase)
    prospective = copy.deepcopy(core)
    manifest, receipt = _selected_manifest_receipt(prospective, phase)
    if receipt.get("status") != "DRAFT":
        _raise("receipt.status", "KIN-E-MANIFEST", "final freeze requires a DRAFT receipt")
    prior_attempt_id = receipt.get("reviewAttemptId")
    if prior_attempt_id is not None:
        if not isinstance(prior_attempt_id, str):
            _raise("receipt.reviewAttemptId", "KIN-E-MANIFEST", "attempt pointer is invalid")
        _validate_predecessor_fence(
            isolated_root,
            core,
            phase,
            str(receipt.get("id")),
            _CORE_PATH,
        )
    plan = attempt_plan
    phase_attempts = [
        attempt
        for attempt in _require_list(core.get("reviewAttempts"), "core.reviewAttempts")
        if isinstance(attempt, dict)
        and attempt.get("phase") == phase
        and attempt.get("receiptId") == receipt.get("id")
    ]
    predecessor = _unique_chain_leaf(phase_attempts, context="attempt")
    predecessor_id = str(predecessor["id"]) if predecessor is not None else None
    if (
        plan.phase != phase
        or plan.receipt_id != receipt.get("id")
        or plan.predecessor_id != predecessor_id
        or plan.paths != attempt_paths(plan.id)
        or any(attempt.get("id") == plan.id for attempt in phase_attempts)
    ):
        _raise(
            "reviewAttempts",
            "KIN-E-CONCURRENT",
            "reserved attempt plan does not match the current review chain",
        )
    if predecessor is not None and predecessor.get("status") not in {"FAILED", "ABANDONED"}:
        _raise(
            "reviewAttempts",
            "KIN-E-CONCURRENT",
            "reserved successor requires a FAILED or ABANDONED predecessor",
        )

    included = _file_records(manifest.get("includedFiles"), "manifest.includedFiles")
    final_records = tuple(sorted(
        (
            _frozen_file_record(isolated_root, record.path, read_overrides)
            for record in included
        ),
        key=lambda record: record.path,
    ))
    manifest["finalFiles"] = [
        {"path": record.path, "kind": record.kind, "sha256": record.sha256}
        for record in final_records
    ]
    manifest["finalFileCount"] = len(final_records)
    prior_closure = set(
        _path_list(manifest.get("closureOnlyPaths"), "manifest.closureOnlyPaths")
    )
    closure = sorted(prior_closure | set(plan.paths))
    manifest["closureOnlyPaths"] = closure
    manifest["allowedChangePaths"] = sorted(
        set(_path_list(manifest.get("allowedChangePaths"), "manifest.allowedChangePaths"))
        | set(plan.paths)
    )

    dispositions = _expand_finding_dispositions(
        isolated_root,
        prospective,
        manifest,
        plan.predecessor_id,
        plan.id,
        finding_dispositions,
        read_overrides,
    )
    _require_list(
        prospective.get("reviewFindingDispositions"),
        "core.reviewFindingDispositions",
    ).extend(dispositions)

    attempt = {
        "id": plan.id,
        "phase": phase,
        "receiptId": receipt.get("id"),
        "supersedesAttemptId": plan.predecessor_id,
        "reviewSubjectDigest": None,
        "reviewTargetPath": plan.paths[0],
        "logicReviewPath": plan.paths[1],
        "btjReviewPath": plan.paths[2],
        "validationBundlePath": plan.paths[3],
        "logicAttestationId": None,
        "btjAttestationId": None,
        "status": "PENDING",
        "abandonReason": None,
    }
    _require_list(prospective.get("reviewAttempts"), "core.reviewAttempts").append(attempt)
    _require_list(
        prospective.get("reviewAttemptArtifacts"), "core.reviewAttemptArtifacts"
    ).append({
        "attemptId": plan.id,
        "reviewTargetSha256": None,
        "logicReviewSha256": None,
        "btjReviewSha256": None,
    })
    receipt["reviewAttemptId"] = plan.id

    state = frozen_git_state or inspect_git_state(
        isolated_root, str(manifest.get("baseCommit"))
    )
    assert isinstance(state, GitState)
    target = _subject_target_value(
        isolated_root,
        prospective,
        manifest,
        current_receipt,
        phase,
        plan.id,
        state,
        read_overrides,
    )
    attempt["reviewSubjectDigest"] = raw_hash(
        canonical_json_bytes(_review_subject_projection(target))
    )
    _validate_disposition_endpoint_laws(
        isolated_root,
        prospective,
        manifest,
        receipt,
        predecessor,
        attempt,
        dispositions,
        target,
        read_overrides,
    )

    prospective_issues = validate_manifest(
        isolated_root,
        canonical_root,
        prospective,
        phase,
        base_ref,
    )
    if prospective_issues:
        issue = prospective_issues[0]
        raise KintsugiError(issue.code, issue.path, issue.message)
    final_state = frozen_git_state or inspect_git_state(
        isolated_root, str(manifest.get("baseCommit"))
    )
    assert isinstance(final_state, GitState)
    final_target = _subject_target_value(
        isolated_root,
        prospective,
        manifest,
        current_receipt,
        phase,
        plan.id,
        final_state,
        read_overrides,
    )
    final_digest = raw_hash(
        canonical_json_bytes(_review_subject_projection(final_target))
    )
    if final_digest != attempt["reviewSubjectDigest"]:
        _raise(
            "reviewTarget",
            "KIN-E-CONCURRENT",
            "review subject changed during the prospective freeze",
        )
    settled_state = frozen_git_state or inspect_git_state(
        isolated_root, str(manifest.get("baseCommit"))
    )
    assert isinstance(settled_state, GitState)
    settled_target = _subject_target_value(
        isolated_root,
        prospective,
        manifest,
        current_receipt,
        phase,
        plan.id,
        settled_state,
        read_overrides,
    )
    settled_digest = raw_hash(
        canonical_json_bytes(_review_subject_projection(settled_target))
    )
    if settled_digest != final_digest:
        _raise(
            "reviewTarget",
            "KIN-E-CONCURRENT",
            "review subject did not remain stable after prospective validation",
        )
    settled_issues = validate_manifest(
        isolated_root,
        canonical_root,
        prospective,
        phase,
        base_ref,
    )
    if settled_issues:
        issue = settled_issues[0]
        _raise(
            issue.path,
            "KIN-E-CONCURRENT",
            f"reviewed state changed after prospective validation: {issue.code}: {issue.message}",
        )
    return prospective


__all__ = ["freeze_manifest_value", "validate_manifest"]
