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
import sys
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

CARD_ID = re.compile(r"^[A-Z][A-Z0-9]*\d{2}-\d{2}$")
WORK_ID = re.compile(r"^BK-[A-Z0-9-]+$")
DOCKET_ID = re.compile(r"^A[0-7]$")
COMPOSITION_ID = re.compile(r"^COMP-[A-Z0-9-]+$")

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


def _primary_checkout_root(root: Path) -> Path:
    """Return the primary checkout root when ``root`` is a linked Git worktree.

    Historical provenance may intentionally live in a sibling pillar. Relative
    sibling paths work in the primary checkout but not under ``.codex-worktrees``.
    Git's ``commondir`` provides a deterministic, local fallback without changing
    the stored path or generated contract.
    """
    dotgit = root / ".git"
    if not dotgit.is_file():
        return root
    try:
        payload = dotgit.read_text(encoding="utf-8").strip()
        if not payload.startswith("gitdir:"):
            return root
        gitdir = Path(payload.split(":", 1)[1].strip())
        if not gitdir.is_absolute():
            gitdir = (root / gitdir).resolve()
        commondir_file = gitdir / "commondir"
        if not commondir_file.is_file():
            return root
        common = Path(commondir_file.read_text(encoding="utf-8").strip())
        if not common.is_absolute():
            common = (gitdir / common).resolve()
        return common.parent
    except OSError:
        return root


def _resolve_repo_path(root: Path, rel: Path, base: Path = Path(".")) -> Path:
    root = root.resolve()
    candidate = (root / base / rel).resolve()
    if candidate.is_relative_to(root):
        return candidate
    # External provenance resolves from the primary checkout, never from an
    # accidental sibling of the linked worktree. It may not escape the
    # Documents federation that contains the sovereign pillar repositories.
    primary = _primary_checkout_root(root).resolve()
    federation = primary.parent.resolve()
    external = (primary / base / rel).resolve()
    if not external.is_relative_to(federation):
        raise ContractError(f"external provenance path escapes the Documents federation: {rel}")
    return external


def _canonical_corpus_path(root: Path, resolved: Path) -> str:
    """Return a stable corpus-relative path for internal or sibling provenance."""
    root = root.resolve()
    resolved = resolved.resolve()
    if resolved.is_relative_to(root):
        return resolved.relative_to(root).as_posix()
    primary = _primary_checkout_root(root).resolve()
    return Path(os.path.relpath(resolved, primary)).as_posix()


def _resolve_declared_path(root: Path, base: Path, declared: Path) -> Path:
    """Resolve a corpus path without assuming the checkout is the owner root.

    Most declarations are repository-relative and resolve directly. A small
    number intentionally begin with ``..`` because they point to read-only
    source custody in a sibling pillar. Git worktrees live one directory deeper
    than the owner checkout, so their direct expansion is not portable. For a
    parent-relative declaration, collect every existing expansion of the same
    declared tail across checkout ancestors. Exactly one distinct file must
    resolve: shadow copies fail closed instead of letting checkout depth choose
    an owner. The declared string remains the contract and only the uniquely
    resolved source bytes enter generated output.
    """
    root = root.resolve()
    base = base.resolve()
    direct = (base / declared).resolve()
    parts = list(declared.parts)
    while parts and parts[0] == "..":
        parts.pop(0)
    parent_relative = bool(parts) and len(parts) < len(declared.parts)

    candidates: dict[str, Path] = {}

    def remember(candidate: Path) -> None:
        resolved = candidate.resolve()
        if resolved.is_file():
            candidates[resolved.as_posix()] = resolved

    remember(direct)
    if parent_relative:
        tail = Path(*parts)
        for ancestor in root.parents:
            remember(ancestor / tail)

    if len(candidates) == 1:
        return next(iter(candidates.values()))
    if len(candidates) > 1:
        matches = ", ".join(sorted(candidates))
        raise AmbiguousDeclaredPathError(
            f"ambiguous declared path {declared.as_posix()!r}: "
            f"multiple owner candidates resolve: {matches}"
        )
    raise UnresolvedDeclaredPathError(
        f"unresolved declared path {declared.as_posix()!r} from {base.as_posix()}"
    )


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


def compile_contract(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    root = root.resolve()
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
        source_path = _resolve_declared_path(root, root, source_rel)
        if not source_path.is_file():
            raise ContractError(f"{path}: missing source {source_rel}")
        reviewed_source_sha256 = _require_string(
            source.get("reviewed_source_sha256"), f"{path}:source.reviewed_source_sha256"
        )
        if not re.fullmatch(r"[0-9a-f]{64}", reviewed_source_sha256):
            raise ContractError(f"{path}: reviewed_source_sha256 must be a lowercase SHA-256")
        actual_source_sha256 = _sha256(source_path)
        if reviewed_source_sha256 != actual_source_sha256:
            raise ContractError(
                f"{path}: source revision changed for {source_rel}; review and update reviewed_source_sha256"
            )
        lifecycle = _require_string(source.get("lifecycle"), f"{path}:source.lifecycle")
        if lifecycle not in lifecycle_enum:
            raise ContractError(f"{path}: invalid source lifecycle {lifecycle}")
        source_key = source_rel.as_posix()
        if source_key in sources and sources[source_key]["work_id"] != work_id:
            raise ContractError(f"{source_rel}: declared by multiple work IDs")
        source_lines = source_path.read_text(encoding="utf-8").splitlines()
        sources[source_key] = {
            "work_id": work_id,
            "path": source_key,
            "lifecycle": lifecycle,
            "role": _require_string(source.get("role"), f"{path}:source.role"),
            "sha256": actual_source_sha256,
            "line_count": len(source_lines),
            "resolved_path": source_path.resolve().as_posix(),
            "external_readonly": not source_path.is_relative_to(root),
        }
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
            if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start or end > len(source_lines):
                raise ContractError(f"{card_id}: invalid source line range {start}-{end} for {source_rel}")
            _require_string(locator.get("section"), f"{card_id}.locator.section")
            anchor = _require_string(locator.get("anchor"), f"{card_id}.locator.anchor")
            located_text = _located_text(source_lines, start, end)
            if anchor not in located_text:
                raise ContractError(f"{card_id}: locator anchor is absent from the declared source slice")
            fingerprint = _require_string(
                locator.get("fingerprint_sha256"), f"{card_id}.locator.fingerprint_sha256"
            )
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
                receipt_path = (root / receipt_rel).resolve()
                if not receipt_path.is_file():
                    raise ContractError(f"{card_id}: missing review receipt {receipt_rel.as_posix()}")
                resolved_receipts.append(receipt_path)
            if review_state in AUDIT_RECEIPT_REQUIRED_STATES and not resolved_receipts:
                raise ContractError(f"{card_id}: {review_state} requires a review receipt")
            if (
                review_state in AUDIT_RECEIPT_REQUIRED_STATES
                and len(resolved_receipts) == 1
                and resolved_receipts[0] == source_path.resolve()
            ):
                raise ContractError(
                    f"{card_id}: source cannot be the sole receipt for {review_state}"
                )
            if public_state == "bounded_current" and (review_state in {"typed", "l1_flagged"} or not receipts):
                raise ContractError(f"{card_id}: bounded current wording requires L2-or-later review and a receipt")
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
        lifecycle = _inferred_manifest_lifecycle(work)
        for source_rel_value in _require_list(work.get("historical_sources"), f"{work_id}.historical_sources"):
            source_rel = Path(_require_string(source_rel_value, f"{work_id}.historical_source"))
            source_path = _resolve_declared_path(
                root,
                root / BOOK_MANIFEST_PATH.parent,
                source_rel,
            )
            if not source_path.is_file():
                raise ContractError(f"{work_id}: missing historical source {source_rel_value}")
            reviewed_sha256 = _require_string(
                source_record.get("reviewed_source_sha256"),
                f"{work_id}.historical_source.reviewed_source_sha256",
            )
            if not re.fullmatch(r"[0-9a-f]{64}", reviewed_sha256):
                raise ContractError(f"{work_id}: historical source pin must be a lowercase SHA-256")
            actual_sha256 = _sha256(source_path)
            if reviewed_sha256 != actual_sha256:
                raise ContractError(f"{work_id}: historical source revision changed: {source_rel_value}")
            lifecycle = _require_string(
                source_record.get("lifecycle"), f"{work_id}.historical_source.lifecycle"
            )
            if lifecycle not in lifecycle_enum:
                raise ContractError(f"{work_id}: invalid historical source lifecycle {lifecycle}")
            manifest_sources.append({
                "work_id": work_id,
                "path": source_rel_value,
                "lifecycle": lifecycle,
                "sha256": actual_sha256,
                "external_readonly": not source_path.is_relative_to(root),
                "role": "historical_source",
                "resolved_path": source_path.resolve().as_posix(),
            })
        public_route = work.get("public_route")
        if public_route is not None:
            public_path = (root / BOOK_MANIFEST_PATH.parent / Path(_require_string(public_route, f"{work_id}.public_route"))).resolve()
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
        confirmation_path = (root / confirmation_rel).resolve()
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
            successor_path = root / _require_string(row.get("successor_path"), "edition_disposition.successor_path")
            gate_receipt = root / _require_string(row.get("gate_receipt"), "edition_disposition.gate_receipt")
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
        resolved_key = _require_string(row.get("resolved_path"), "lifecycle_source.resolved_path")
        canonical_path = _canonical_corpus_path(root, Path(resolved_key))
        normalized = {
            "work_id": row["work_id"],
            "path": canonical_path,
            "lifecycle": row["lifecycle"],
            "sha256": row["sha256"],
            "external_readonly": row["external_readonly"],
            "roles": [row["role"]],
        }
        if "line_count" in row:
            normalized["line_count"] = row["line_count"]
        existing = lifecycle_by_resolved_path.get(resolved_key)
        if existing is None:
            lifecycle_by_resolved_path[resolved_key] = normalized
            continue
        for field in ("work_id", "path", "lifecycle", "sha256", "external_readonly"):
            if existing[field] != normalized[field]:
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
