#!/usr/bin/env python3
"""Validate claim-card contracts and build deterministic derived registers.

The ``*.yaml`` inputs intentionally use the JSON subset of YAML 1.2. That
keeps the human contract YAML-compatible while making the compiler stdlib-only.
Generated outputs contain no clock, branch, user, or environment fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
CARD_DIR = Path("00_META/claim_cards")
DOCKET_PATH = Path("00_META/ADEQUACY_DOCKETS.yaml")
SCHEMA_PATH = Path("00_META/schemas/claim-card.schema.yaml")
BOOK_MANIFEST_PATH = Path("13_BOOKS/book-manifest.json")
REGISTER_PATH = Path("00_META/registers/CLAIM_CARD_REGISTER.json")
GRAPH_PATH = Path("00_META/registers/CLAIM_GRAPH.json")
LIFECYCLE_PATH = Path("00_META/registers/CLAIM_LIFECYCLE_INVENTORY.json")
PRIMARY_CHECKOUT_ENV = "EMERGENTISM_PRIMARY_CHECKOUT_ROOT"
ALLOW_UNAVAILABLE_EXTERNAL_ENV = "EMERGENTISM_ALLOW_UNAVAILABLE_EXTERNAL_SOURCES"
EXTERNAL_SOURCE_PILLAR = "02_SKYZAI"

CARD_ID = re.compile(r"^[A-Z][A-Z0-9]*\d{2}-\d{2}$")
WORK_ID = re.compile(r"^BK-[A-Z0-9-]+$")
DOCKET_ID = re.compile(r"^A[0-7]$")
COMPOSITION_ID = re.compile(r"^COMP-[A-Z0-9-]+$")

# Disclosure-safe metadata allowlist for private sibling sources. These paths
# and pins already exist in the checked-in claim cards/book manifest; no source
# bytes are embedded here. Metadata-only CI may defer byte replay only for these
# exact contracts and declaring roles. Any new external dependency requires an
# explicit reviewed compiler change.
EXTERNAL_SOURCE_CONTRACTS: dict[str, tuple[str, str, str, frozenset[str]]] = {
    "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/00_THE_INFINITE_BOOK_OF_EMERGENCE.md": (
        "081fb55303f07409713c086bbb73bd3d2025eebf14713c54a6629483b91aa3a9",
        "frozen",
        "BK-RECIPROCAL-INFINITE-PLAY",
        frozenset({"book_manifest"}),
    ),
    "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/01_BOOK_I_SARPASYA_VIJAYAM/DISSEMINATION/SARPASYA_VIJAYAM_EDITION_1.md": (
        "aa59ccbda3ca3f615f71aaf11141e45b9b10588f8454295e6445742d18199436",
        "legacy",
        "BK-SARPASYA",
        frozenset({"claim_card", "book_manifest"}),
    ),
    "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/02_BOOK_II_THE_SIX_LENSES/DISSEMINATION/THE_SIX_LENSES_EDITION_1.md": (
        "17ad1a31461f27738b0128a2e53fbed78e5aadeee04ee2de8aadf4cb74fe0ab2",
        "legacy",
        "BK-SIX-LENSES",
        frozenset({"claim_card", "book_manifest"}),
    ),
    "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/03_BOOK_III_THE_SELF_EATING_SERPENT/DISSEMINATION/THE_SELF_EATING_SERPENT_EDITION_1.md": (
        "397ee521026dd999431250bbc55e86181ffc03b6b14a820adf98d70ab81f3ac4",
        "legacy",
        "BK-SELF-EATING",
        frozenset({"claim_card", "book_manifest"}),
    ),
    "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/07_PUBLIC_EDITION/THE_RECIPROCAL_PUBLIC_EDITION_K2_LANG_DECOMM_2026_07_22.md": (
        "86b59d4f3e4ad8ec64e85fb1b075ac986953b3c28339eda1046459789696a1f9",
        "frozen",
        "BK-RECIPROCAL-INFINITE-PLAY",
        frozenset({"claim_card", "book_manifest"}),
    ),
    "../02_SKYZAI/08_EVOLUTIONARY_NETWORK/README.md": (
        "df8887940ce76d68e1073ee18b197b3a64059fef73ad094128d6143a4a6105d6",
        "proposal",
        "BK-EVOLUTIONARY-NETWORK",
        frozenset({"book_manifest"}),
    ),
}
EXTERNAL_CARD_LOCATOR_INVENTORY_COUNT = 28
EXTERNAL_CARD_LOCATOR_INVENTORY_SHA256 = (
    "010e35009ab30cdb089f8fb23451e37a259da0e16e5cde3555b8d09839088258"
)

ALLOWED_COMPOSITION_CLASSES = {
    "active_book",
    "active_research_book",
    "active_practice_book",
    "historical_critical_reader",
}
ALLOWED_COMPOSITION_OUTPUT_STATES = {
    "active_book": {
        "planned_not_built",
        "current_reader_rebuild_pending",
        "built_private",
        "private_full_book_completed_not_public",
        "active_public",
    },
    "active_research_book": {"planned_not_built", "built_private", "active_public"},
    "active_practice_book": {"planned_not_built", "built_private", "active_public"},
    "historical_critical_reader": {"planned_not_built", "built_private", "released_historical"},
}
ALLOWED_ARCHITECTURE_STATUSES = {"staged_proposal", "confirmed"}
ALLOWED_BUILD_PROVENANCE_TYPES = {"generator", "projection_artifact", "manual"}
ALLOWED_NONBOOK_HOMES = {"research_dossier", "historical_custody_only"}
ALLOWED_EDITION_DISPOSITIONS = {
    "retained_and_rebuilt_in_place",
    "retained_source_and_public_practice_projection",
    "preserve_until_research_edition_2_passes",
    "preserved_module_projection",
    "preserved_dossier_projection",
    "preserve_until_historical_reader_exists",
}
AUDIT_RECEIPT_REQUIRED_STATES = {
    "l3_audited",
    "owner_approved",
    "implemented",
    "projection_audited",
    "closed",
}


class ContractError(ValueError):
    """Raised when a source contract fails closed."""


class UnresolvedDeclaredPathError(ContractError):
    """Raised when no file satisfies a declared source path."""


class FrozenSourceUnavailableError(UnresolvedDeclaredPathError):
    """Raised when hash-bound frozen custody is unavailable for validation."""


class AmbiguousDeclaredPathError(ContractError):
    """Raised when a portable source declaration has multiple owners."""


def _read_json_yaml(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"{path}: invalid JSON-subset YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{path}: root must be an object")
    return value


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# RESTORED 2026-08-05. _located_text, _resolve_repo_path and _canonical_corpus_path
# are USED in this file and were DEFINED NOWHERE — dropped by merge 80759036
# ("conflicts resolved main-side"), which left the claim-card compiler raising
# NameError on every run and took the claim-graph contract tests down with it.
# _primary_checkout_root is restored because the other two depend on it. Recovered
# verbatim from 1797138a. Receipt:
# 11_UPLINK/50_AUDITS_AND_EXECUTIONS/242_G2_PROVED_AND_FOUND_TO_BE_PRIOR_ART_2026_08_05.md


def _text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _located_text(lines: list[str], start: int, end: int) -> str:
    """Return the exact, newline-normalized inclusive source slice."""
    return "\n".join(lines[start - 1:end])


def _configured_primary_checkout_root() -> Path | None:
    """Return an explicit full-federation Emergentism checkout, when configured.

    Standalone clones cannot validate source bytes held by a sibling pillar. An
    authorized local replay may therefore point at a complete, read-only
    federation. The value is deliberately an Emergentism checkout root (not an
    arbitrary search directory), and marker files make a wrong or stale
    configuration fail closed.
    """
    raw = os.environ.get(PRIMARY_CHECKOUT_ENV)
    if raw is None:
        return None
    configured_lexical = Path(raw)
    if not configured_lexical.is_absolute():
        raise ContractError(f"{PRIMARY_CHECKOUT_ENV} must be an absolute path")
    configured_lexical = _lexical_absolute(configured_lexical)
    if configured_lexical.is_symlink():
        raise ContractError(f"{PRIMARY_CHECKOUT_ENV} may not be a symlink")
    configured = configured_lexical.resolve()
    if not configured.is_dir():
        raise ContractError(f"{PRIMARY_CHECKOUT_ENV} is not a directory: {configured}")
    markers = (configured / "AGENTS.md", configured / "00_THE_KERNEL_INDEX.md")
    if any(not marker.is_file() or marker.is_symlink() for marker in markers):
        raise ContractError(
            f"{PRIMARY_CHECKOUT_ENV} is not an Emergentism checkout: {configured}"
        )
    return configured


def _primary_checkout_root(root: Path) -> Path:
    """Return the primary checkout root when ``root`` is a linked Git worktree.

    Historical provenance may intentionally live in a sibling pillar. Relative
    sibling paths work in the primary checkout but not under ``.codex-worktrees``.
    Git's ``commondir`` provides a deterministic, local fallback without changing
    the stored path or generated contract.
    """
    root = root.resolve()
    configured = _configured_primary_checkout_root()
    dotgit = root / ".git"
    if not dotgit.is_file():
        return configured or root
    try:
        payload = dotgit.read_text(encoding="utf-8").strip()
        if not payload.startswith("gitdir:"):
            return configured or root
        gitdir = Path(payload.split(":", 1)[1].strip())
        if not gitdir.is_absolute():
            gitdir = (root / gitdir).resolve()
        commondir_file = gitdir / "commondir"
        if not commondir_file.is_file():
            return configured or root
        common = Path(commondir_file.read_text(encoding="utf-8").strip())
        if not common.is_absolute():
            common = (gitdir / common).resolve()
        primary = common.parent.resolve()
        if configured is not None and configured != primary:
            raise ContractError(
                f"{PRIMARY_CHECKOUT_ENV} conflicts with linked-worktree primary: "
                f"{configured} != {primary}"
            )
        return primary
    except OSError:
        return configured or root


def _lexical_absolute(path: Path) -> Path:
    """Return an absolute normalized path without following symlinks."""
    return Path(os.path.abspath(os.fspath(path)))


def _reject_symlink_components(path: Path, boundary: Path, label: str) -> None:
    """Reject symlinks at or below a lexical trust boundary.

    Resolving first would erase the evidence that a path escaped through a
    symlink. Walk the normalized lexical spelling instead, then callers may
    resolve and perform a second containment check.
    """
    path = _lexical_absolute(path)
    boundary = _lexical_absolute(boundary)
    try:
        relative = path.relative_to(boundary)
    except ValueError as exc:
        raise ContractError(f"{label} escapes allowed root {boundary}: {path}") from exc
    current = boundary
    if current.is_symlink():
        raise ContractError(f"{label} uses symlink trust root: {current}")
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ContractError(f"{label} uses symlink component: {current}")


def _canonical_external_declaration(base: Path, declared: Path) -> str | None:
    """Normalize one declared path and admit only the Skyzai sibling pillar."""
    if base.is_absolute() or declared.is_absolute():
        raise ContractError("external source normalization requires relative paths")
    normalized = Path(os.path.normpath((base / declared).as_posix()))
    parts = normalized.parts
    if not parts or parts[0] != "..":
        return None
    if (
        len(parts) < 3
        or parts[1] != EXTERNAL_SOURCE_PILLAR
        or any(part in {"", ".", ".."} for part in parts[2:])
    ):
        raise ContractError(
            "external provenance must escape exactly once into declared sibling "
            f"{EXTERNAL_SOURCE_PILLAR}: {declared.as_posix()}"
        )
    return normalized.as_posix()


def _require_registered_external_source(
    canonical: str,
    reviewed_sha256: str,
    lifecycle: str,
    work_id: str,
    declaring_role: str,
) -> None:
    expected = EXTERNAL_SOURCE_CONTRACTS.get(canonical)
    observed = (reviewed_sha256, lifecycle, work_id)
    if expected is None or observed != expected[:3] or declaring_role not in expected[3]:
        raise ContractError(
            "external source is not in the reviewed metadata-only inventory: "
            f"path={canonical}, work_id={work_id}, lifecycle={lifecycle}, "
            f"role={declaring_role}, sha256={reviewed_sha256}"
        )


def _external_card_locator_inventory_sha256(rows: list[dict[str, Any]]) -> str:
    ordered = sorted(rows, key=lambda row: (row["source_path"], row["card_id"]))
    return hashlib.sha256(_canonical_bytes(ordered)).hexdigest()


def _authorized_external_roots(root: Path) -> tuple[Path, Path] | None:
    """Return the explicitly bounded federation and Skyzai roots, if allowed."""
    root = root.resolve()
    configured = _configured_primary_checkout_root()
    primary = _primary_checkout_root(root).resolve()
    # A standalone clone does not gain authority over an arbitrary neighbour.
    if configured is None and primary == root:
        return None
    federation = primary.parent.resolve()
    pillar_lexical = federation / EXTERNAL_SOURCE_PILLAR
    _reject_symlink_components(pillar_lexical, federation, "external pillar")
    pillar = pillar_lexical.resolve()
    if not pillar.is_relative_to(federation):
        raise ContractError(f"external pillar escapes configured federation: {pillar}")
    return federation, pillar


def _bounded_external_candidate(
    root: Path,
    base: Path,
    declared: Path,
) -> Path | None:
    """Resolve an exact external declaration inside the one allowed pillar."""
    canonical = _canonical_external_declaration(base, declared)
    if canonical is None:
        return None
    roots = _authorized_external_roots(root)
    if roots is None:
        return None
    federation, pillar = roots
    candidate = _lexical_absolute(federation / Path(canonical).relative_to(".."))
    _reject_symlink_components(candidate, pillar, "external source")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(pillar):
        raise ContractError(f"external source escapes {pillar}: {declared.as_posix()}")
    return resolved


def _resolve_repo_path(root: Path, rel: Path, base: Path = Path(".")) -> Path:
    root = root.resolve()
    candidate_lexical = _lexical_absolute(root / base / rel)
    if candidate_lexical.is_relative_to(root):
        _reject_symlink_components(candidate_lexical, root, "repository source")
        resolved = candidate_lexical.resolve()
        if not resolved.is_relative_to(root):
            raise ContractError(f"repository source escapes checkout: {rel.as_posix()}")
        return resolved
    external = _bounded_external_candidate(root, base, rel)
    if external is None:
        raise UnresolvedDeclaredPathError(
            f"external provenance unavailable for {rel.as_posix()}; configure "
            f"{PRIMARY_CHECKOUT_ENV} for exact replay, or explicitly acknowledge "
            f"metadata-only validation with {ALLOW_UNAVAILABLE_EXTERNAL_ENV}=1"
        )
    return external


def _resolve_internal_corpus_path(
    root: Path,
    rel: Path,
    label: str,
    base: Path = Path("."),
    *,
    allow_normalized_parent_components: bool = False,
) -> Path:
    """Resolve a declared path only inside the corpus trust root.

    Root-relative declarations may not contain parent components.  A small
    number of manifest-relative fields legitimately begin with ``..`` because
    their base is ``13_BOOKS``; those declarations are admitted only when the
    lexically normalized candidate still lies inside the corpus.  Resolution
    then flows through ``_resolve_repo_path`` so direct and ancestor symlinks
    are rejected before any bytes are read.
    """
    root = root.resolve()
    if rel.is_absolute():
        raise ContractError(f"{label} must be relative")
    if not allow_normalized_parent_components and ".." in rel.parts:
        raise ContractError(f"{label} must be root-relative without parent traversal")
    candidate_lexical = _lexical_absolute(root / base / rel)
    if not candidate_lexical.is_relative_to(root):
        raise ContractError(f"{label} traverses outside the corpus root")
    resolved = _resolve_repo_path(root, rel, base)
    if not resolved.is_relative_to(root):
        raise ContractError(f"{label} resolves outside the corpus root")
    return resolved


def _canonical_corpus_path(root: Path, resolved: Path) -> str:
    """Return a stable corpus-relative path for internal or sibling provenance."""
    root = root.resolve()
    resolved = resolved.resolve()
    if resolved.is_relative_to(root):
        return resolved.relative_to(root).as_posix()
    primary = _primary_checkout_root(root).resolve()
    return Path(os.path.relpath(resolved, primary)).as_posix()


def _resolve_declared_path(root: Path, base: Path, declared: Path) -> Path:
    """Resolve owned files directly and external files inside one federation.

    External declarations are accepted only when their normalized path enters
    ``02_SKYZAI`` exactly once and an explicit or linked-worktree federation is
    available. No ancestor scan or arbitrary sibling discovery is permitted.
    """
    root = root.resolve()
    base = base.resolve()
    try:
        base_rel = base.relative_to(root)
    except ValueError as exc:
        raise ContractError(f"declared-path base escapes checkout: {base}") from exc
    direct_lexical = _lexical_absolute(base / declared)
    if direct_lexical.is_relative_to(root):
        _reject_symlink_components(direct_lexical, root, "declared source")
        direct = direct_lexical.resolve()
        if not direct.is_relative_to(root):
            raise ContractError(f"declared source escapes checkout: {declared.as_posix()}")
        if direct.is_file():
            return direct
        parent_relative = False
    else:
        parent_relative = True
        external = _bounded_external_candidate(root, base_rel, declared)
        if external is not None and external.is_file():
            return external
    federation_hint = (
        f"; set {PRIMARY_CHECKOUT_ENV} to an Emergentism checkout inside the "
        f"federation containing {EXTERNAL_SOURCE_PILLAR} for exact byte replay"
        if parent_relative
        else ""
    )
    raise UnresolvedDeclaredPathError(
        f"unresolved declared path {declared.as_posix()!r} from {base.as_posix()}"
        f"{federation_hint}; source validation was not skipped"
    )


def _resolve_hash_bound_relocation(
    root: Path,
    declared: Path,
    expected_sha256: str,
    base: Path = Path("."),
) -> tuple[Path, int] | None:
    """Resolve moved sibling custody only by exact content identity.

    Topology changes may move a frozen or legacy file while its claim card keeps
    the reviewed path as provenance. When a full federation checkout is
    available, search only the declared sibling pillar, require the reviewed
    SHA-256, and select the unique candidate with the longest common path suffix.
    A tied best match is an ownership ambiguity and fails closed. The returned
    count records how many byte-identical custody copies were observed.
    """
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ContractError("hash-bound relocation requires a lowercase SHA-256")
    canonical = _canonical_external_declaration(base, declared)
    if canonical is None:
        return None
    parts = list(Path(canonical).relative_to("..").parts)
    roots = _authorized_external_roots(root)
    if roots is None:
        return None
    _, pillar = roots
    if not pillar.is_dir():
        return None

    matching: list[Path] = []
    for directory, dirnames, filenames in os.walk(pillar, followlinks=False):
        directory_path = Path(directory)
        # Never traverse symlinked directories. A matching-name symlink is an
        # explicit contract failure rather than an invisible non-match.
        dirnames[:] = [
            name for name in dirnames if not (directory_path / name).is_symlink()
        ]
        if parts[-1] not in filenames:
            continue
        candidate = directory_path / parts[-1]
        if candidate.is_symlink():
            raise ContractError(
                f"hash-bound relocation rejects symlink source: {candidate}"
            )
        _reject_symlink_components(candidate, pillar, "hash-bound relocation")
        resolved = candidate.resolve()
        if not resolved.is_relative_to(pillar):
            raise ContractError(f"hash-bound relocation escapes {pillar}: {candidate}")
        if resolved.is_file() and _sha256(resolved) == expected_sha256:
            matching.append(resolved)
    matching.sort(key=lambda candidate: candidate.as_posix())
    if not matching:
        return None

    def suffix_score(candidate: Path) -> int:
        score = 0
        for expected, actual in zip(reversed(parts), reversed(candidate.parts)):
            if expected != actual:
                break
            score += 1
        return score

    scores = {candidate: suffix_score(candidate) for candidate in matching}
    best_score = max(scores.values())
    best = [candidate for candidate, score in scores.items() if score == best_score]
    if len(best) != 1:
        matches = ", ".join(candidate.as_posix() for candidate in best)
        raise AmbiguousDeclaredPathError(
            f"hash-bound relocation for {declared.as_posix()!r} has multiple "
            f"equally specific custody paths at SHA-256 {expected_sha256}: {matches}"
        )
    return best[0], len(matching)


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{label}: expected non-empty string")
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{label}: expected list")
    return value


def _assert_acyclic(nodes: Iterable[str], edges: dict[str, list[str]], label: str) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, trail: list[str]) -> None:
        if node in visiting:
            cycle = " -> ".join(trail + [node])
            raise ContractError(f"{label}: dependency cycle: {cycle}")
        if node in visited:
            return
        visiting.add(node)
        for dependency in edges.get(node, []):
            visit(dependency, trail + [node])
        visiting.remove(node)
        visited.add(node)

    for node in sorted(nodes):
        visit(node, [])


def _inferred_manifest_lifecycle(work: dict[str, Any]) -> str:
    """Infer the legacy string-source lifecycle from a work release state.

    New historical-source records carry an explicit lifecycle and hash. This
    inference remains only for older string entries that can be joined to an
    already hash-pinned claim-card source for the same work; it never supplies a
    missing content pin.
    """
    state = str(work.get("release_state", ""))
    if "frozen" in state:
        return "frozen"
    if "historical_readonly" in state:
        return "legacy"
    if "external_runtime" in state or "proposal" in state:
        return "proposal"
    if "projection" in state:
        return "projection"
    return "active"


def compile_contract(
    root: Path = ROOT,
    allow_unavailable_external: bool | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    if allow_unavailable_external is None:
        raw_allow = os.environ.get(ALLOW_UNAVAILABLE_EXTERNAL_ENV)
        if raw_allow not in {None, "0", "1"}:
            raise ContractError(
                f"{ALLOW_UNAVAILABLE_EXTERNAL_ENV} must be exactly 0 or 1"
            )
        allow_unavailable_external = raw_allow == "1"
    elif not isinstance(allow_unavailable_external, bool):
        raise ContractError("allow_unavailable_external must be boolean")
    schema = _read_json_yaml(root / SCHEMA_PATH)
    dockets_doc = _read_json_yaml(root / DOCKET_PATH)
    book_manifest = _read_json_yaml(root / BOOK_MANIFEST_PATH)

    if schema.get("schema") != "emergentism/claim-card-schema/v2":
        raise ContractError(f"{SCHEMA_PATH}: expected claim-card-schema/v2")
    if book_manifest.get("schema") != "emergentism/book-manifest/v2":
        raise ContractError(f"{BOOK_MANIFEST_PATH}: expected book-manifest/v2")
    enums = schema.get("enums", {})
    owner_registry = schema.get("owner_registry", {})
    required_fields = set(schema.get("required_card_fields", []))
    required_source_fields = set(schema.get("required_source_fields", []))
    required_locator_fields = set(schema.get("required_locator_fields", []))
    if not required_fields:
        raise ContractError(f"{SCHEMA_PATH}: required_card_fields is empty")
    expected_owners = {f"K-{i}" for i in range(1, 8)} | {f"KER-{i}" for i in range(1, 8)}
    if set(owner_registry) != expected_owners:
        raise ContractError(
            f"{SCHEMA_PATH}: owner registry must contain exactly K-1 through K-7 "
            f"and KER-1 through KER-7 (Phase 2 of the naming-reconciliation docket; "
            f"see 00_THE_KERNEL_INDEX.md for the dual-write convention)"
        )
    kernel_index = (root / "00_THE_KERNEL_INDEX.md").read_text(encoding="utf-8")
    for owner_id, rel in sorted(owner_registry.items()):
        owner_path = root / rel
        if not owner_path.is_file():
            raise ContractError(f"{owner_id}: missing owner path {rel}")
        if rel not in kernel_index:
            raise ContractError(f"{owner_id}: owner path is not named in 00_THE_KERNEL_INDEX.md: {rel}")

    ladder = dockets_doc.get("status_ladder")
    expected_ladder = [
        "typed", "packet-complete", "evidence-open", "component-supported",
        "independently-replicated", "narrowed", "killed", "deferred", "frozen",
    ]
    if ladder != expected_ladder:
        raise ContractError(f"{DOCKET_PATH}: status ladder must match the canonical maturity sequence")
    dockets = _require_list(dockets_doc.get("dockets"), f"{DOCKET_PATH}:dockets")
    docket_map: dict[str, dict[str, Any]] = {}
    docket_edges: dict[str, list[str]] = {}
    for docket in dockets:
        if not isinstance(docket, dict):
            raise ContractError(f"{DOCKET_PATH}: every docket must be an object")
        docket_id = _require_string(docket.get("docket_id"), "docket_id")
        if not DOCKET_ID.fullmatch(docket_id) or docket_id in docket_map:
            raise ContractError(f"invalid or duplicate docket id: {docket_id}")
        status = _require_string(docket.get("status"), f"{docket_id}.status")
        if status not in ladder:
            raise ContractError(f"{docket_id}: invalid maturity status {status}")
        owners = _require_list(docket.get("owner_ids"), f"{docket_id}.owner_ids")
        if not owners or any(owner not in owner_registry for owner in owners):
            raise ContractError(f"{docket_id}: invalid owner_ids")
        _require_string(docket.get("gate"), f"{docket_id}.gate")
        _require_string(docket.get("kill_or_narrow"), f"{docket_id}.kill_or_narrow")
        dependencies = _require_list(docket.get("depends_on"), f"{docket_id}.depends_on")
        docket_map[docket_id] = docket
        docket_edges[docket_id] = dependencies
    if set(docket_map) != {f"A{i}" for i in range(8)}:
        raise ContractError(f"{DOCKET_PATH}: dockets must be exactly A0 through A7")
    for docket_id, dependencies in docket_edges.items():
        for dependency in dependencies:
            if dependency not in docket_map:
                raise ContractError(f"{docket_id}: unknown docket dependency {dependency}")
    _assert_acyclic(docket_map, docket_edges, "adequacy dockets")

    card_files = sorted((root / CARD_DIR).glob("*.yaml"))
    if not card_files:
        raise ContractError(f"{CARD_DIR}: no claim-card sets found")
    cards: dict[str, dict[str, Any]] = {}
    sources: dict[str, dict[str, Any]] = {}
    card_edges: dict[str, list[str]] = {}
    work_cards: dict[str, list[str]] = defaultdict(list)
    external_card_locator_inventory: list[dict[str, Any]] = []
    lifecycle_enum = set(enums.get("source_lifecycle", []))
    type_enum = set(enums.get("claim_type", []))
    tier_enum = set(enums.get("evidence_tier", []))
    disposition_enum = set(enums.get("disposition", []))
    public_enum = set(enums.get("public_state", []))
    review_enum = set(enums.get("review_state", []))

    for path in card_files:
        document = _read_json_yaml(path)
        if document.get("schema") != "emergentism/claim-card-set/v2":
            raise ContractError(f"{path}: expected claim-card-set/v2")
        work_id = _require_string(document.get("work_id"), f"{path}:work_id")
        if not WORK_ID.fullmatch(work_id):
            raise ContractError(f"{path}: invalid work_id {work_id}")
        source = document.get("source")
        if not isinstance(source, dict):
            raise ContractError(f"{path}: source must be an object")
        missing_source = sorted(required_source_fields - set(source))
        if missing_source:
            raise ContractError(f"{path}: source missing fields: {', '.join(missing_source)}")
        source_rel = Path(_require_string(source.get("path"), f"{path}:source.path"))
        reviewed_source_sha256 = _require_string(
            source.get("reviewed_source_sha256"), f"{path}:source.reviewed_source_sha256"
        )
        if not re.fullmatch(r"[0-9a-f]{64}", reviewed_source_sha256):
            raise ContractError(f"{path}: reviewed_source_sha256 must be a lowercase SHA-256")
        lifecycle = _require_string(source.get("lifecycle"), f"{path}:source.lifecycle")
        if lifecycle not in lifecycle_enum:
            raise ContractError(f"{path}: invalid source lifecycle {lifecycle}")
        external_canonical = _canonical_external_declaration(Path("."), source_rel)
        if external_canonical is not None:
            _require_registered_external_source(
                external_canonical,
                reviewed_source_sha256,
                lifecycle,
                work_id,
                "claim_card",
            )
        custody_resolution = "declared_path"
        relocation_match_count = 0
        source_path: Path | None = None
        unavailable_external = False
        try:
            source_path = _resolve_declared_path(root, root, source_rel)
        except UnresolvedDeclaredPathError as exc:
            relocated = _resolve_hash_bound_relocation(
                root, source_rel, reviewed_source_sha256
            )
            authorized_external = (
                _authorized_external_roots(root)
                if external_canonical is not None
                else None
            )
            if relocated is not None:
                source_path, relocation_match_count = relocated
                custody_resolution = "hash_bound_relocation"
            elif (
                external_canonical is not None
                and allow_unavailable_external
                and authorized_external is None
            ):
                unavailable_external = True
                custody_resolution = "external_unavailable"
            elif external_canonical is not None and authorized_external is not None:
                raise ContractError(
                    f"{path}: configured {EXTERNAL_SOURCE_PILLAR} custody does not contain "
                    f"the exact reviewed bytes for {source_rel}; expected SHA-256 "
                    f"{reviewed_source_sha256}"
                ) from exc
            elif lifecycle == "frozen":
                raise FrozenSourceUnavailableError(
                    f"{path}: hash-bound frozen source unavailable: {source_rel}; "
                    f"expected SHA-256 {reviewed_source_sha256}; provide the declared "
                    f"custody via {PRIMARY_CHECKOUT_ENV}; validation was not skipped"
                ) from exc
            else:
                raise
        if source_path is not None and not source_path.is_file():
            raise ContractError(f"{path}: missing source {source_rel}")
        actual_source_sha256 = (
            reviewed_source_sha256 if unavailable_external else _sha256(source_path)
        )
        if not unavailable_external and reviewed_source_sha256 != actual_source_sha256:
            raise ContractError(
                f"{path}: source revision changed for {source_rel}; review and update reviewed_source_sha256"
            )
        source_key = source_rel.as_posix()
        if source_key in sources and sources[source_key]["work_id"] != work_id:
            raise ContractError(f"{source_rel}: declared by multiple work IDs")
        source_lines = (
            None
            if unavailable_external
            else source_path.read_text(encoding="utf-8").splitlines()
        )
        source_row = {
            "work_id": work_id,
            "path": source_key,
            "lifecycle": lifecycle,
            "role": _require_string(source.get("role"), f"{path}:source.role"),
            "sha256": actual_source_sha256,
            "resolved_path": (
                (external_canonical or source_key)
                if unavailable_external
                else source_path.resolve().as_posix()
            ),
            "lifecycle_key": (
                external_canonical
                if external_canonical is not None
                else source_path.resolve().as_posix()
            ),
            "canonical_path": source_key,
            "external_readonly": external_canonical is not None,
            "content_available": not unavailable_external,
            "custody_resolution": custody_resolution,
            "relocation_match_count": relocation_match_count,
        }
        if external_canonical is None:
            source_row["line_count"] = len(source_lines)
        sources[source_key] = source_row
        for card in _require_list(document.get("cards"), f"{path}:cards"):
            if not isinstance(card, dict):
                raise ContractError(f"{path}: every card must be an object")
            missing = sorted(required_fields - set(card))
            if missing:
                raise ContractError(f"{path}: card missing fields: {', '.join(missing)}")
            card_id = _require_string(card.get("card_id"), f"{path}:card_id")
            if not CARD_ID.fullmatch(card_id) or card_id in cards:
                raise ContractError(f"invalid or duplicate claim-card id: {card_id}")
            chapters = _require_list(card.get("chapters"), f"{card_id}.chapters")
            if not chapters or any(not isinstance(chapter, str) or not chapter for chapter in chapters):
                raise ContractError(f"{card_id}: chapters must contain non-empty slugs")
            locator = card.get("locator")
            if not isinstance(locator, dict):
                raise ContractError(f"{card_id}: locator must be an object")
            missing_locator = sorted(required_locator_fields - set(locator))
            if missing_locator:
                raise ContractError(f"{card_id}: locator missing fields: {', '.join(missing_locator)}")
            start = locator.get("line_start")
            end = locator.get("line_end")
            if (
                not isinstance(start, int)
                or not isinstance(end, int)
                or start < 1
                or end < start
                or (source_lines is not None and end > len(source_lines))
            ):
                raise ContractError(f"{card_id}: invalid source line range {start}-{end} for {source_rel}")
            section = _require_string(locator.get("section"), f"{card_id}.locator.section")
            anchor = _require_string(locator.get("anchor"), f"{card_id}.locator.anchor")
            fingerprint = _require_string(
                locator.get("fingerprint_sha256"), f"{card_id}.locator.fingerprint_sha256"
            )
            if not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
                raise ContractError(f"{card_id}: locator fingerprint must be a lowercase SHA-256")
            if source_lines is not None:
                located_text = _located_text(source_lines, start, end)
                if anchor not in located_text:
                    raise ContractError(f"{card_id}: locator anchor is absent from the declared source slice")
                if fingerprint != _text_sha256(located_text):
                    raise ContractError(f"{card_id}: locator fingerprint does not match the declared source slice")
            claim_type = _require_string(card.get("claim_type"), f"{card_id}.claim_type")
            if claim_type not in type_enum:
                raise ContractError(f"{card_id}: invalid claim type {claim_type}")
            evidence = _require_list(card.get("evidence"), f"{card_id}.evidence")
            if not evidence:
                raise ContractError(f"{card_id}: evidence cannot be empty")
            tiers: list[str] = []
            for record in evidence:
                if not isinstance(record, dict):
                    raise ContractError(f"{card_id}: evidence records must be objects")
                tier = _require_string(record.get("tier"), f"{card_id}.evidence.tier")
                if tier not in tier_enum:
                    raise ContractError(f"{card_id}: invalid evidence tier {tier}")
                _require_string(record.get("scope"), f"{card_id}.evidence.scope")
                tiers.append(tier)
            semantic_owner = _require_string(card.get("semantic_owner_id"), f"{card_id}.semantic_owner_id")
            if "owner_ids" in card:
                raise ContractError(f"{card_id}: legacy owner_ids is forbidden by the singular-owner contract")
            if semantic_owner not in owner_registry:
                raise ContractError(f"{card_id}: invalid semantic owner {semantic_owner}")
            supporting_owners = _require_list(card.get("supporting_owner_ids"), f"{card_id}.supporting_owner_ids")
            if any(owner not in owner_registry for owner in supporting_owners):
                raise ContractError(f"{card_id}: one or more supporting owner IDs are invalid")
            if semantic_owner in supporting_owners or len(set(supporting_owners)) != len(supporting_owners):
                raise ContractError(f"{card_id}: supporting owners must be unique and exclude the semantic owner")
            dependencies = _require_list(card.get("dependencies"), f"{card_id}.dependencies")
            docket_ids = _require_list(card.get("docket_ids"), f"{card_id}.docket_ids")
            if any(docket_id not in docket_map for docket_id in docket_ids):
                raise ContractError(f"{card_id}: unknown adequacy docket")
            if "C" in tiers and not docket_ids:
                raise ContractError(f"{card_id}: conjectures require a research docket")
            _require_string(card.get("plain_claim"), f"{card_id}.plain_claim")
            _require_list(card.get("type_boundaries"), f"{card_id}.type_boundaries")
            for field in ("strongest_rival", "discriminator", "kill_criterion", "survivor_if_killed"):
                _require_string(card.get(field), f"{card_id}.{field}")
            consequence = card.get("consequence")
            if not isinstance(consequence, dict) or not isinstance(consequence.get("applicable"), bool):
                raise ContractError(f"{card_id}: consequence must declare applicability")
            for field in ("bearers", "consent", "reversibility", "exit"):
                if field not in consequence:
                    raise ContractError(f"{card_id}: consequence missing {field}")
            if consequence["applicable"] and not _require_list(consequence["bearers"], f"{card_id}.consequence.bearers"):
                raise ContractError(f"{card_id}: consequential claim must name bearers")
            disposition = _require_string(card.get("disposition"), f"{card_id}.disposition")
            if disposition not in disposition_enum:
                raise ContractError(f"{card_id}: invalid disposition {disposition}")
            public = card.get("public")
            if not isinstance(public, dict):
                raise ContractError(f"{card_id}: public must be an object")
            public_state = _require_string(public.get("state"), f"{card_id}.public.state")
            if public_state not in public_enum:
                raise ContractError(f"{card_id}: invalid public state {public_state}")
            _require_string(public.get("wording"), f"{card_id}.public.wording")
            review = card.get("review")
            if not isinstance(review, dict):
                raise ContractError(f"{card_id}: review must be an object")
            review_state = _require_string(review.get("state"), f"{card_id}.review.state")
            if review_state not in review_enum:
                raise ContractError(f"{card_id}: invalid review state {review_state}")
            receipts = _require_list(review.get("receipts"), f"{card_id}.review.receipts")
            resolved_receipts: list[Path] = []
            for receipt_value in receipts:
                receipt_rel = Path(_require_string(receipt_value, f"{card_id}.review.receipt"))
                if receipt_rel.is_absolute() or ".." in receipt_rel.parts:
                    raise ContractError(f"{card_id}: review receipt must be a root-relative corpus path")
                receipt_path = _resolve_internal_corpus_path(
                    root,
                    receipt_rel,
                    f"{card_id}: review receipt",
                )
                if not receipt_path.is_file():
                    raise ContractError(f"{card_id}: missing review receipt {receipt_rel.as_posix()}")
                resolved_receipts.append(receipt_path)
            if review_state in AUDIT_RECEIPT_REQUIRED_STATES and not resolved_receipts:
                raise ContractError(f"{card_id}: {review_state} requires a review receipt")
            if (
                review_state in AUDIT_RECEIPT_REQUIRED_STATES
                and len(resolved_receipts) == 1
                and source_path is not None
                and resolved_receipts[0] == source_path.resolve()
            ):
                raise ContractError(
                    f"{card_id}: source cannot be the sole receipt for {review_state}"
                )
            if public_state == "bounded_current" and (review_state in {"typed", "l1_flagged"} or not receipts):
                raise ContractError(f"{card_id}: bounded current wording requires L2-or-later review and a receipt")
            if external_canonical is not None:
                external_card_locator_inventory.append({
                    "anchor": anchor,
                    "card_id": card_id,
                    "fingerprint_sha256": fingerprint,
                    "line_end": end,
                    "line_start": start,
                    "section": section,
                    "source_path": external_canonical,
                    "work_id": work_id,
                })
            cards[card_id] = {
                **card,
                "source": {
                    "path": source_key,
                    "work_id": work_id,
                    "lifecycle": lifecycle,
                    "reviewed_source_sha256": actual_source_sha256,
                },
                "evidence_tiers": sorted(set(tiers)),
            }
            card_edges[card_id] = dependencies
            work_cards[work_id].append(card_id)

    expected_external_card_works = {
        contract[2]
        for contract in EXTERNAL_SOURCE_CONTRACTS.values()
        if "claim_card" in contract[3]
    }
    raw_manifest_works = book_manifest.get("works")
    declared_manifest_work_ids = (
        {
            work.get("work_id")
            for work in raw_manifest_works
            if isinstance(work, dict) and isinstance(work.get("work_id"), str)
        }
        if isinstance(raw_manifest_works, list)
        else set()
    )
    if external_card_locator_inventory or (
        expected_external_card_works & declared_manifest_work_ids
    ):
        if not expected_external_card_works.issubset(declared_manifest_work_ids):
            raise ContractError(
                "external card locator inventory has a partial work binding"
            )
        inventory_sha256 = _external_card_locator_inventory_sha256(
            external_card_locator_inventory
        )
        if (
            len(external_card_locator_inventory)
            != EXTERNAL_CARD_LOCATOR_INVENTORY_COUNT
            or inventory_sha256 != EXTERNAL_CARD_LOCATOR_INVENTORY_SHA256
        ):
            raise ContractError(
                "external card locator semantic inventory changed: "
                f"count={len(external_card_locator_inventory)}, "
                f"sha256={inventory_sha256}; expected "
                f"count={EXTERNAL_CARD_LOCATOR_INVENTORY_COUNT}, "
                f"sha256={EXTERNAL_CARD_LOCATOR_INVENTORY_SHA256}"
            )

    for card_id, dependencies in card_edges.items():
        for dependency in dependencies:
            if dependency not in cards:
                raise ContractError(f"{card_id}: dangling claim dependency {dependency}")
    _assert_acyclic(cards, card_edges, "claim graph")

    works = _require_list(book_manifest.get("works"), f"{BOOK_MANIFEST_PATH}:works")
    manifest_ids: set[str] = set()
    manifest_work_map: dict[str, dict[str, Any]] = {}
    manifest_sources: list[dict[str, Any]] = []
    for work in works:
        if not isinstance(work, dict):
            raise ContractError(f"{BOOK_MANIFEST_PATH}: every work must be an object")
        required_work = {
            "work_id", "edition", "historical_sources", "chapter_order", "owner_ids",
            "claim_card_ids", "release_state", "public_route", "build_provenance",
        }
        missing = sorted(required_work - set(work))
        if missing:
            raise ContractError(f"book manifest work missing: {', '.join(missing)}")
        work_id = _require_string(work.get("work_id"), "book work_id")
        if not WORK_ID.fullmatch(work_id) or work_id in manifest_ids:
            raise ContractError(f"invalid or duplicate book work id: {work_id}")
        manifest_ids.add(work_id)
        manifest_work_map[work_id] = work
        declared_cards = _require_list(work.get("claim_card_ids"), f"{work_id}.claim_card_ids")
        if len(declared_cards) != len(set(declared_cards)):
            raise ContractError(f"{work_id}: duplicate claim-card id in manifest")
        for card_id in declared_cards:
            if card_id not in cards:
                raise ContractError(f"{work_id}: unknown claim-card id {card_id}")
            if cards[card_id]["source"]["work_id"] != work_id:
                raise ContractError(f"{work_id}: claim-card {card_id} belongs to another work")
        expected_cards = set(work_cards.get(work_id, []))
        if set(declared_cards) != expected_cards:
            missing_cards = sorted(expected_cards - set(declared_cards))
            extra_cards = sorted(set(declared_cards) - expected_cards)
            raise ContractError(
                f"{work_id}: manifest claim-card set differs from source cards; "
                f"missing={missing_cards}, extra={extra_cards}"
            )
        chapter_order = _require_list(work.get("chapter_order"), f"{work_id}.chapter_order")
        if len(chapter_order) != len(set(chapter_order)):
            raise ContractError(f"{work_id}: duplicate chapter slug in manifest")
        if declared_cards:
            covered = {chapter for card_id in declared_cards for chapter in cards[card_id]["chapters"]}
            missing_chapters = [chapter for chapter in chapter_order if chapter not in covered]
            if missing_chapters:
                raise ContractError(f"{work_id}: chapters lack claim-card coverage: {', '.join(missing_chapters)}")
            extra_chapters = sorted(covered - set(chapter_order))
            if extra_chapters:
                raise ContractError(f"{work_id}: claim cards name undeclared chapters: {', '.join(extra_chapters)}")
        elif chapter_order:
            raise ContractError(f"{work_id}: zero-card work cannot declare entering chapters")
        owners = _require_list(work.get("owner_ids"), f"{work_id}.owner_ids")
        if any(owner not in owner_registry for owner in owners):
            raise ContractError(f"{work_id}: invalid owner id")
        if len(owners) != len(set(owners)):
            raise ContractError(f"{work_id}: duplicate owner id")
        expected_owners = {cards[card_id]["semantic_owner_id"] for card_id in declared_cards}
        if set(owners) != expected_owners:
            raise ContractError(
                f"{work_id}: owner_ids must equal semantic-owner projection; "
                f"expected={sorted(expected_owners)}, found={sorted(set(owners))}"
            )
        inferred_lifecycle = _inferred_manifest_lifecycle(work)
        pinned_sources = {
            Path(source["resolved_path"]).resolve().as_posix(): source
            for source in sources.values()
            if source["work_id"] == work_id
        }
        for raw_source in _require_list(
            work.get("historical_sources"), f"{work_id}.historical_sources"
        ):
            source_record: dict[str, Any] | None
            if isinstance(raw_source, dict):
                source_record = raw_source
                source_rel_value = _require_string(
                    source_record.get("path"), f"{work_id}.historical_source.path"
                )
            else:
                source_record = None
                source_rel_value = _require_string(raw_source, f"{work_id}.historical_source")
            source_rel = Path(source_rel_value)
            if source_rel.is_absolute():
                raise ContractError(f"{work_id}: historical source paths must be manifest-relative")
            external_canonical = _canonical_external_declaration(
                BOOK_MANIFEST_PATH.parent, source_rel
            )
            custody_resolution = "declared_path"
            relocation_match_count = 0
            unavailable_external = False
            pinned: dict[str, Any] | None = None
            if source_record is not None:
                reviewed_sha256 = _require_string(
                    source_record.get("reviewed_source_sha256"),
                    f"{work_id}.historical_source.reviewed_source_sha256",
                )
                if not re.fullmatch(r"[0-9a-f]{64}", reviewed_sha256):
                    raise ContractError(
                        f"{work_id}: historical source pin must be a lowercase SHA-256"
                    )
                lifecycle = _require_string(
                    source_record.get("lifecycle"), f"{work_id}.historical_source.lifecycle"
                )
                if lifecycle not in lifecycle_enum:
                    raise ContractError(
                        f"{work_id}: invalid historical source lifecycle {lifecycle}"
                    )
            else:
                reviewed_sha256 = ""
                lifecycle = inferred_lifecycle

            source_path: Path | None = None
            try:
                source_path = _resolve_repo_path(
                    root, source_rel, BOOK_MANIFEST_PATH.parent
                )
            except UnresolvedDeclaredPathError:
                source_path = None
            if source_path is not None and source_path.is_file():
                pinned = pinned_sources.get(source_path.resolve().as_posix())
            elif source_record is not None:
                relocated = _resolve_hash_bound_relocation(
                    root,
                    source_rel,
                    reviewed_sha256,
                    BOOK_MANIFEST_PATH.parent,
                )
                authorized_external = (
                    _authorized_external_roots(root)
                    if external_canonical is not None
                    else None
                )
                if relocated is not None:
                    source_path, relocation_match_count = relocated
                    custody_resolution = "hash_bound_relocation"
                elif (
                    external_canonical is not None
                    and allow_unavailable_external
                    and authorized_external is None
                ):
                    unavailable_external = True
                    custody_resolution = "external_unavailable"
                elif external_canonical is not None and authorized_external is not None:
                    raise ContractError(
                        f"{work_id}: configured {EXTERNAL_SOURCE_PILLAR} custody does not "
                        f"contain the exact reviewed bytes for {source_rel_value}; expected "
                        f"SHA-256 {reviewed_sha256}"
                    )
                else:
                    raise ContractError(
                        f"{work_id}: hash-bound historical source unavailable: "
                        f"{source_rel_value}; expected SHA-256 {reviewed_sha256}; "
                        "validation was not skipped"
                    )
            elif source_record is None:
                pinned_by_name = [
                    source
                    for source in pinned_sources.values()
                    if Path(source["canonical_path"]).name == source_rel.name
                ]
                if len(pinned_by_name) == 1:
                    pinned = pinned_by_name[0]
                    unavailable_external = not bool(
                        pinned.get("content_available", True)
                    )
                    source_path = (
                        None
                        if unavailable_external
                        else Path(pinned["resolved_path"])
                    )
                    custody_resolution = _require_string(
                        pinned.get("custody_resolution"),
                        f"{work_id}.historical_source.custody_resolution",
                    )
                    relocation_match_count = int(
                        pinned.get("relocation_match_count", 0)
                    )

            if source_record is None:
                if pinned is None:
                    raise ContractError(
                        f"{work_id}: legacy string historical source lacks hash-bound "
                        f"claim-card custody: {source_rel_value}; inferred lifecycle "
                        f"{inferred_lifecycle!r} is diagnostic only; migrate this entry "
                        "to a pinned object"
                    )
                reviewed_sha256 = _require_string(
                    pinned.get("sha256"), f"{work_id}.historical_source.derived_sha256"
                )
                lifecycle = _require_string(
                    pinned.get("lifecycle"), f"{work_id}.historical_source.derived_lifecycle"
                )
            if external_canonical is not None:
                _require_registered_external_source(
                    external_canonical,
                    reviewed_sha256,
                    lifecycle,
                    work_id,
                    "book_manifest",
                )
            if not unavailable_external and (source_path is None or not source_path.is_file()):
                raise ContractError(f"{work_id}: missing historical source {source_rel_value}")
            actual_sha256 = reviewed_sha256 if unavailable_external else _sha256(source_path)
            if not unavailable_external and reviewed_sha256 != actual_sha256:
                raise ContractError(f"{work_id}: historical source revision changed: {source_rel_value}")
            canonical_path = Path(
                os.path.normpath((BOOK_MANIFEST_PATH.parent / source_rel).as_posix())
            ).as_posix()
            manifest_source = {
                "work_id": work_id,
                "path": source_rel_value,
                "canonical_path": canonical_path,
                "lifecycle": lifecycle,
                "sha256": actual_sha256,
                "external_readonly": external_canonical is not None,
                "role": "historical_source",
                "resolved_path": (
                    canonical_path
                    if unavailable_external
                    else source_path.resolve().as_posix()
                ),
                "lifecycle_key": (
                    external_canonical
                    if external_canonical is not None
                    else source_path.resolve().as_posix()
                ),
            }
            if custody_resolution == "hash_bound_relocation":
                manifest_source["custody_resolution"] = custody_resolution
                manifest_source["relocation_match_count"] = relocation_match_count
            manifest_sources.append(manifest_source)
        public_route = work.get("public_route")
        if public_route is not None:
            public_rel = Path(_require_string(public_route, f"{work_id}.public_route"))
            public_path = _resolve_internal_corpus_path(
                root,
                public_rel,
                f"{work_id}: public route",
                BOOK_MANIFEST_PATH.parent,
                allow_normalized_parent_components=True,
            )
            public_root = (root / "12_PUBLIC_SITE").resolve()
            if not public_path.is_relative_to(public_root):
                raise ContractError(
                    f"{work_id}: public route must remain inside 12_PUBLIC_SITE"
                )
            if not public_path.is_file():
                raise ContractError(f"{work_id}: missing public route {public_route}")
        provenance = work.get("build_provenance")
        if not isinstance(provenance, dict):
            raise ContractError(f"{work_id}: build_provenance must be a typed object")
        provenance_type = _require_string(provenance.get("type"), f"{work_id}.build_provenance.type")
        if provenance_type not in ALLOWED_BUILD_PROVENANCE_TYPES:
            raise ContractError(f"{work_id}: invalid build provenance type {provenance_type}")
        if provenance_type == "manual":
            if set(provenance) != {"type", "description", "verification"}:
                raise ContractError(f"{work_id}: manual build provenance has invalid fields")
            _require_string(provenance.get("description"), f"{work_id}.build_provenance.description")
            _require_string(provenance.get("verification"), f"{work_id}.build_provenance.verification")
        else:
            if set(provenance) != {"type", "path", "sha256"}:
                raise ContractError(f"{work_id}: path build provenance has invalid fields")
            provenance_rel_value = _require_string(
                provenance.get("path"), f"{work_id}.build_provenance.path"
            )
            provenance_rel = Path(provenance_rel_value)
            if provenance_rel.is_absolute():
                raise ContractError(f"{work_id}: build provenance path must be manifest-relative")
            provenance_path = _resolve_repo_path(root, provenance_rel, BOOK_MANIFEST_PATH.parent)
            if not provenance_path.is_file() or not provenance_path.is_relative_to(root):
                raise ContractError(f"{work_id}: missing or external build provenance {provenance_rel_value}")
            provenance_sha = _require_string(
                provenance.get("sha256"), f"{work_id}.build_provenance.sha256"
            )
            if not re.fullmatch(r"[0-9a-f]{64}", provenance_sha):
                raise ContractError(f"{work_id}: build provenance hash must be a lowercase SHA-256")
            if provenance_sha != _sha256(provenance_path):
                raise ContractError(f"{work_id}: build provenance revision changed: {provenance_rel_value}")

    if set(work_cards) - manifest_ids:
        raise ContractError(f"claim-card works absent from book manifest: {sorted(set(work_cards) - manifest_ids)}")

    # Editorial compositions remove reader overlap without moving semantic
    # ownership or duplicating claim cards between source work records.
    architecture = book_manifest.get("editorial_architecture")
    if not isinstance(architecture, dict):
        raise ContractError(f"{BOOK_MANIFEST_PATH}: editorial_architecture is required")
    if architecture.get("schema") != "emergentism/book-composition/v2":
        raise ContractError(f"{BOOK_MANIFEST_PATH}: expected book-composition/v2")
    architecture_status = _require_string(
        architecture.get("status"), "editorial_architecture.status"
    )
    if architecture_status not in ALLOWED_ARCHITECTURE_STATUSES:
        raise ContractError(f"editorial_architecture: invalid status {architecture_status}")
    confirmation = architecture.get("confirmation")
    if not isinstance(confirmation, dict) or set(confirmation) != {
        "state", "receipt", "receipt_sha256"
    }:
        raise ContractError("editorial_architecture: invalid confirmation contract")
    confirmation_state = _require_string(
        confirmation.get("state"), "editorial_architecture.confirmation.state"
    )
    if architecture_status == "staged_proposal":
        if confirmation_state != "unconfirmed" or any(
            confirmation.get(key) is not None for key in ("receipt", "receipt_sha256")
        ):
            raise ContractError(
                "editorial_architecture: staged proposal must remain explicitly unconfirmed"
            )
    else:
        if confirmation_state != "confirmed":
            raise ContractError("editorial_architecture: confirmed status requires confirmed state")
        confirmation_rel = Path(_require_string(
            confirmation.get("receipt"), "editorial_architecture.confirmation.receipt"
        ))
        if confirmation_rel.is_absolute() or ".." in confirmation_rel.parts:
            raise ContractError("editorial_architecture: confirmation receipt must be corpus-relative")
        confirmation_path = _resolve_internal_corpus_path(
            root,
            confirmation_rel,
            "editorial_architecture: confirmation receipt",
        )
        if not confirmation_path.is_file():
            raise ContractError("editorial_architecture: missing confirmation receipt")
        confirmation_sha = _require_string(
            confirmation.get("receipt_sha256"),
            "editorial_architecture.confirmation.receipt_sha256",
        )
        if not re.fullmatch(r"[0-9a-f]{64}", confirmation_sha) or confirmation_sha != _sha256(confirmation_path):
            raise ContractError("editorial_architecture: invalid confirmation receipt hash")
    if architecture.get("authority") != "projection_only_no_semantic_authority":
        raise ContractError("editorial_architecture: projection-only authority boundary drifted")
    _require_string(architecture.get("decision"), "editorial_architecture.decision")
    compositions = _require_list(architecture.get("compositions"), "editorial_architecture.compositions")
    if not compositions:
        raise ContractError("editorial_architecture: at least one composition is required")
    composition_ids: set[str] = set()
    primary_routes: dict[str, list[str]] = defaultdict(list)
    primary_route_info: dict[str, dict[str, str]] = {}
    primary_counts: dict[str, int] = {}
    composition_summaries: list[dict[str, Any]] = []

    def selected_cards(record: dict[str, Any], label: str) -> set[str]:
        work_id = _require_string(record.get("work_id"), f"{label}.work_id")
        if work_id not in manifest_work_map:
            raise ContractError(f"{label}: unknown work_id {work_id}")
        has_all = record.get("claim_selection") == "all"
        has_ids = "claim_card_ids" in record
        if has_all == has_ids:
            raise ContractError(f"{label}: choose exactly one of claim_selection=all or claim_card_ids")
        chosen = set(work_cards.get(work_id, [])) if has_all else set(
            _require_list(record.get("claim_card_ids"), f"{label}.claim_card_ids")
        )
        if has_ids and len(chosen) != len(record["claim_card_ids"]):
            raise ContractError(f"{label}: duplicate selected claim-card id")
        invalid = sorted(
            card_id for card_id in chosen
            if card_id not in cards or cards[card_id]["source"]["work_id"] != work_id
        )
        if invalid:
            raise ContractError(f"{label}: cards do not belong to {work_id}: {invalid}")
        return chosen

    for composition in compositions:
        if not isinstance(composition, dict):
            raise ContractError("editorial_architecture: every composition must be an object")
        composition_id = _require_string(composition.get("composition_id"), "composition_id")
        if not COMPOSITION_ID.fullmatch(composition_id) or composition_id in composition_ids:
            raise ContractError(f"invalid or duplicate composition id: {composition_id}")
        composition_ids.add(composition_id)
        catalog_class = _require_string(composition.get("catalog_class"), f"{composition_id}.catalog_class")
        if catalog_class not in ALLOWED_COMPOSITION_CLASSES:
            raise ContractError(f"{composition_id}: invalid catalog class {catalog_class}")
        title = _require_string(composition.get("title"), f"{composition_id}.title")
        output = composition.get("output")
        if not isinstance(output, dict):
            raise ContractError(f"{composition_id}.output must be an object")
        output_state = _require_string(output.get("state"), f"{composition_id}.output.state")
        if output_state not in ALLOWED_COMPOSITION_OUTPUT_STATES[catalog_class]:
            raise ContractError(f"{composition_id}: invalid output state {output_state}")
        anchor_work = composition.get("anchor_work_id")
        if anchor_work is not None and anchor_work not in manifest_ids:
            raise ContractError(f"{composition_id}: unknown anchor_work_id {anchor_work}")
        count = 0
        for index, component in enumerate(_require_list(composition.get("components"), f"{composition_id}.components")):
            if not isinstance(component, dict):
                raise ContractError(f"{composition_id}.components[{index}]: expected object")
            label = f"{composition_id}.components[{index}]"
            chosen = selected_cards(component, label)
            mode = _require_string(component.get("projection_mode"), f"{label}.projection_mode")
            if mode not in {"primary", "reference_only"}:
                raise ContractError(f"{label}: invalid projection_mode {mode}")
            if catalog_class == "historical_critical_reader" and mode != "reference_only":
                raise ContractError(f"{label}: historical-reader components must be reference_only")
            if mode == "primary":
                count += len(chosen)
                for card_id in chosen:
                    primary_routes[card_id].append(composition_id)
                    primary_route_info[card_id] = {
                        "primary_projection_home": composition_id,
                        "projection_kind": catalog_class,
                    }
        primary_counts[composition_id] = count
        uncarded_modules: list[str] = []
        for module in composition.get("source_modules", []):
            if not isinstance(module, dict):
                raise ContractError(f"{composition_id}.source_modules: every module must be a coverage object")
            module_path_value = _require_string(module.get("path"), f"{composition_id}.source_modules.path")
            module_path = Path(module_path_value)
            resolved = _resolve_repo_path(root, module_path, BOOK_MANIFEST_PATH.parent)
            if not resolved.is_file() or not resolved.is_relative_to(root):
                raise ContractError(f"{composition_id}: missing or external source module {module_path_value}")
            coverage_state = _require_string(
                module.get("coverage_state"), f"{composition_id}.source_modules.coverage_state"
            )
            if coverage_state not in {"uncarded", "carded"}:
                raise ContractError(f"{composition_id}: invalid module coverage_state {coverage_state}")
            module_cards = _require_list(
                module.get("claim_card_ids"), f"{composition_id}.source_modules.claim_card_ids"
            )
            if len(module_cards) != len(set(module_cards)):
                raise ContractError(f"{composition_id}: duplicate module claim-card id")
            module_rel = resolved.relative_to(root).as_posix()
            exact_source_cards = {
                card_id for card_id, card in cards.items()
                if card["source"]["path"] == module_rel
            }
            if set(module_cards) != exact_source_cards:
                raise ContractError(
                    f"{composition_id}: module coverage differs from exact source cards for "
                    f"{module_path_value}; expected={sorted(exact_source_cards)}, "
                    f"found={sorted(set(module_cards))}"
                )
            expected_coverage = "carded" if exact_source_cards else "uncarded"
            if coverage_state != expected_coverage:
                raise ContractError(
                    f"{composition_id}: module coverage_state must be {expected_coverage} "
                    f"for {module_path_value}"
                )
            for card_id in module_cards:
                if card_id not in cards:
                    raise ContractError(f"{composition_id}: unknown module claim-card id {card_id}")
                card_source = cards[card_id]["source"]
                if card_source["path"] != module_rel or card_source["reviewed_source_sha256"] != _sha256(resolved):
                    raise ContractError(
                        f"{composition_id}: module card {card_id} does not resolve to the exact source revision"
                    )
            if coverage_state == "uncarded":
                uncarded_modules.append(module_path_value)
        if output_state != "planned_not_built" and uncarded_modules:
            raise ContractError(
                f"{composition_id}: cannot promote output with uncarded source modules: {uncarded_modules}"
            )
        for module in composition.get("reference_modules", []):
            if not isinstance(module, dict):
                raise ContractError(f"{composition_id}.reference_modules: every module must be an object")
            module_path_value = _require_string(module.get("path"), f"{composition_id}.reference_modules.path")
            if module.get("projection_mode") != "reference_only":
                raise ContractError(f"{composition_id}: reference modules must declare projection_mode=reference_only")
            module_path = Path(module_path_value)
            resolved = _resolve_repo_path(root, module_path, BOOK_MANIFEST_PATH.parent)
            if not resolved.is_file() or not resolved.is_relative_to(root):
                raise ContractError(f"{composition_id}: missing or external reference module {module_path_value}")
        composition_summaries.append({
            "composition_id": composition_id,
            "catalog_class": catalog_class,
            "title": title,
            "output_state": output_state,
            "primary_card_count": count,
        })

    dispositions = _require_list(architecture.get("edition_dispositions"), "editorial_architecture.edition_dispositions")
    disposition_ids = [_require_string(row.get("work_id") if isinstance(row, dict) else None, "edition_disposition.work_id") for row in dispositions]
    if len(disposition_ids) != len(set(disposition_ids)) or set(disposition_ids) != manifest_ids:
        raise ContractError("editorial_architecture: edition dispositions must name every work exactly once")
    for row in dispositions:
        if not isinstance(row, dict):
            raise ContractError("edition_disposition must be an object")
        disposition = _require_string(
            row.get("existing_edition_disposition"), "edition_disposition.existing_edition_disposition"
        )
        if disposition.startswith("superseded_"):
            successor_rel = Path(_require_string(
                row.get("successor_path"), "edition_disposition.successor_path"
            ))
            gate_receipt_rel = Path(_require_string(
                row.get("gate_receipt"), "edition_disposition.gate_receipt"
            ))
            successor_path = _resolve_internal_corpus_path(
                root,
                successor_rel,
                "edition_disposition.successor_path",
            )
            gate_receipt = _resolve_internal_corpus_path(
                root,
                gate_receipt_rel,
                "edition_disposition.gate_receipt",
            )
            if not successor_path.is_file() or not gate_receipt.is_file():
                raise ContractError("superseded edition requires an existing successor and gate receipt")
        elif disposition not in ALLOWED_EDITION_DISPOSITIONS:
            raise ContractError(f"invalid edition disposition: {disposition}")

    nonbook_counts: dict[str, int] = defaultdict(int)
    nonbook_route_ids: set[str] = set()
    nonbook_summaries: list[dict[str, Any]] = []
    for index, route in enumerate(_require_list(architecture.get("nonbook_claim_routes"), "editorial_architecture.nonbook_claim_routes")):
        if not isinstance(route, dict):
            raise ContractError("editorial_architecture: every nonbook route must be an object")
        route_id = _require_string(route.get("route_id"), f"nonbook_claim_routes[{index}].route_id")
        if route_id in nonbook_route_ids:
            raise ContractError(f"duplicate nonbook route id: {route_id}")
        nonbook_route_ids.add(route_id)
        chosen = selected_cards(route, f"nonbook_claim_routes[{index}]")
        home = _require_string(route.get("primary_home"), f"{route_id}.primary_home")
        if home not in ALLOWED_NONBOOK_HOMES:
            raise ContractError(f"{route_id}: invalid primary_home {home}")
        nonbook_counts[home] += len(chosen)
        for card_id in chosen:
            primary_routes[card_id].append(route_id)
            primary_route_info[card_id] = {
                "primary_projection_home": route_id,
                "projection_kind": home,
            }
        nonbook_summaries.append({
            "route_id": route_id,
            "projection_kind": home,
            "primary_card_count": len(chosen),
        })

    route_errors = {card_id: routes for card_id, routes in sorted(primary_routes.items()) if len(routes) != 1}
    missing_routes = sorted(set(cards) - set(primary_routes))
    if route_errors or missing_routes:
        raise ContractError(
            "editorial_architecture: every card needs exactly one primary, dossier, or custody route; "
            f"duplicates={route_errors}, missing={missing_routes}"
        )
    integrity = architecture.get("integrity")
    if not isinstance(integrity, dict):
        raise ContractError("editorial_architecture.integrity must be an object")
    expected_integrity = {
        "existing_claim_card_count": len(cards),
        "primary_cards_by_composition": dict(sorted(primary_counts.items())),
        "primary_cards_by_nonbook_home": dict(sorted(nonbook_counts.items())),
        "total_primary_or_custody_routes": len(primary_routes),
    }
    if integrity != expected_integrity:
        raise ContractError(
            f"editorial_architecture: integrity totals drifted; expected={expected_integrity}, found={integrity}"
        )

    card_rows = []
    for card_id in sorted(cards):
        card = cards[card_id]
        card_rows.append({
            "card_id": card_id,
            "work_id": card["source"]["work_id"],
            "source_path": card["source"]["path"],
            "source_lifecycle": card["source"]["lifecycle"],
            "locator": card["locator"],
            "chapters": sorted(card["chapters"]),
            "claim_type": card["claim_type"],
            "evidence_tiers": card["evidence_tiers"],
            "semantic_owner_id": card["semantic_owner_id"],
            "supporting_owner_ids": sorted(card["supporting_owner_ids"]),
            "dependency_ids": sorted(card["dependencies"]),
            "docket_ids": sorted(card["docket_ids"]),
            "disposition": card["disposition"],
            "review_state": card["review"]["state"],
            "public_state": card["public"]["state"],
            **primary_route_info[card_id],
        })
    register = {
        "schema": "emergentism/claim-card-register/v2",
        "authority": "derived routing register; K-1 through K-7 remain semantic owners",
        "inputs": [path.relative_to(root).as_posix() for path in card_files],
        "owners": [{"owner_id": owner, "path": path} for owner, path in sorted(owner_registry.items())],
        "cards": card_rows,
        "metrics": {
            "cards": len(card_rows),
            "works_with_cards": len(work_cards),
            "public_bounded_current": sum(row["public_state"] == "bounded_current" for row in card_rows),
            "conjecture_cards": sum("C" in row["evidence_tiers"] for row in card_rows),
        },
    }

    graph_nodes = []
    graph_edges = []
    for card_id in sorted(cards):
        card = cards[card_id]
        graph_nodes.append({"id": card_id, "kind": "claim", "lifecycle": card["source"]["lifecycle"]})
        graph_edges.append({"from": card_id, "kind": "owned_by", "to": card["semantic_owner_id"]})
        for owner in sorted(card["supporting_owner_ids"]):
            graph_edges.append({"from": card_id, "kind": "supported_by", "to": owner})
        for dependency in sorted(card["dependencies"]):
            graph_edges.append({"from": card_id, "kind": "depends_on", "to": dependency})
        for docket_id in sorted(card["docket_ids"]):
            graph_edges.append({"from": card_id, "kind": "tested_by", "to": docket_id})
        graph_edges.append({"from": card_id, "kind": "projected_from", "to": card["source"]["work_id"]})
        graph_edges.append({
            "from": card_id,
            "kind": "projected_to",
            "to": primary_route_info[card_id]["primary_projection_home"],
        })
    for owner, owner_path in sorted(owner_registry.items()):
        graph_nodes.append({"id": owner, "kind": "semantic_owner", "path": owner_path})
    for docket_id in sorted(docket_map):
        graph_nodes.append({"id": docket_id, "kind": "adequacy_docket", "status": docket_map[docket_id]["status"]})
    for work_id in sorted(manifest_ids):
        graph_nodes.append({"id": work_id, "kind": "book_projection"})
    for summary in composition_summaries:
        graph_nodes.append({"id": summary["composition_id"], "kind": "book_composition", **summary})
    for summary in nonbook_summaries:
        graph_nodes.append({"id": summary["route_id"], "kind": "nonbook_claim_route", **summary})
    graph = {
        "schema": "emergentism/claim-owner-dependency-graph/v2",
        "authority": "derived graph; publication and graph membership provide no evidence",
        "nodes": sorted(graph_nodes, key=lambda row: (row["kind"], row["id"])),
        "edges": sorted(graph_edges, key=lambda row: (row["from"], row["kind"], row["to"])),
        "composition_summaries": sorted(composition_summaries, key=lambda row: row["composition_id"]),
        "metrics": {"nodes": len(graph_nodes), "edges": len(graph_edges)},
    }

    lifecycle_by_resolved_path: dict[str, dict[str, Any]] = {}
    for row in list(sources.values()) + manifest_sources:
        resolved_key = _require_string(
            row.get("lifecycle_key") or row.get("resolved_path"),
            "lifecycle_source.lifecycle_key",
        )
        canonical_path = row.get("canonical_path") or _canonical_corpus_path(
            root, Path(resolved_key)
        )
        normalized = {
            "work_id": row["work_id"],
            "path": canonical_path,
            "lifecycle": row["lifecycle"],
            "sha256": row["sha256"],
            "external_readonly": row["external_readonly"],
            "roles": [row["role"]],
        }
        if row["external_readonly"]:
            normalized["byte_validation"] = (
                "exact_sha256_when_authorized_federation_available; "
                "explicit_unavailable_mode_validates_metadata_only"
            )
        if "line_count" in row:
            normalized["line_count"] = row["line_count"]
        existing = lifecycle_by_resolved_path.get(resolved_key)
        if existing is None:
            lifecycle_by_resolved_path[resolved_key] = normalized
            continue
        for field in (
            "work_id",
            "path",
            "lifecycle",
            "sha256",
            "external_readonly",
            "byte_validation",
        ):
            if field not in existing and field not in normalized:
                continue
            if existing.get(field) != normalized.get(field):
                raise ContractError(
                    f"lifecycle source conflict for {canonical_path}: {field} "
                    f"{existing[field]!r} != {normalized[field]!r}"
                )
        existing["roles"] = sorted(set(existing["roles"] + normalized["roles"]))
        if "line_count" in normalized:
            existing["line_count"] = normalized["line_count"]
    lifecycle_sources = list(lifecycle_by_resolved_path.values())
    lifecycle_counts = Counter(row["lifecycle"] for row in lifecycle_sources)
    lifecycle = {
        "schema": "emergentism/claim-lifecycle-inventory/v3",
        "baseline": {
            "date": "2026-07-28",
            "tracked_files": 3205,
            "tracked_markdown": 2239,
            "public_html": 402,
            "note": "Recorded W0 entry inventory; later generated additions do not rewrite this baseline."
        },
        "counts": dict(sorted(lifecycle_counts.items())),
        "sources": sorted(lifecycle_sources, key=lambda row: (row["work_id"], row["path"])),
    }
    return register, graph, lifecycle


def write_outputs(root: Path, outputs: tuple[dict[str, Any], dict[str, Any], dict[str, Any]]) -> None:
    for rel, value in zip((REGISTER_PATH, GRAPH_PATH, LIFECYCLE_PATH), outputs):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_canonical_bytes(value))


def check_outputs(root: Path, outputs: tuple[dict[str, Any], dict[str, Any], dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for rel, value in zip((REGISTER_PATH, GRAPH_PATH, LIFECYCLE_PATH), outputs):
        path = root / rel
        expected = _canonical_bytes(value)
        if not path.is_file():
            errors.append(f"missing generated output: {rel}")
        elif path.read_bytes() != expected:
            errors.append(f"generated output drift: {rel}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write deterministic derived registers")
    mode.add_argument("--check", action="store_true", help="validate inputs and require generated registers to match")
    args = parser.parse_args(argv)
    try:
        outputs = compile_contract(ROOT)
    except ContractError as exc:
        print(f"CLAIM CARD CONTRACT: FAIL\n- {exc}")
        return 1
    if args.write:
        write_outputs(ROOT, outputs)
        print(f"CLAIM CARD CONTRACT: WROTE {len(outputs[0]['cards'])} cards, {outputs[1]['metrics']['edges']} edges")
        return 0
    errors = check_outputs(ROOT, outputs)
    if errors:
        print("CLAIM CARD CONTRACT: FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"CLAIM CARD CONTRACT: PASS ({len(outputs[0]['cards'])} cards, {outputs[1]['metrics']['edges']} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
