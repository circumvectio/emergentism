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


def _inferred_manifest_lifecycle(work: dict[str, Any]) -> str:
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


def compile_contract(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    schema = _read_json_yaml(root / SCHEMA_PATH)
    dockets_doc = _read_json_yaml(root / DOCKET_PATH)
    book_manifest = _read_json_yaml(root / BOOK_MANIFEST_PATH)

    enums = schema.get("enums", {})
    owner_registry = schema.get("owner_registry", {})
    required_fields = set(schema.get("required_card_fields", []))
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
        work_id = _require_string(document.get("work_id"), f"{path}:work_id")
        if not WORK_ID.fullmatch(work_id):
            raise ContractError(f"{path}: invalid work_id {work_id}")
        source = document.get("source")
        if not isinstance(source, dict):
            raise ContractError(f"{path}: source must be an object")
        source_rel = Path(_require_string(source.get("path"), f"{path}:source.path"))
        source_path = _resolve_declared_path(root, root, source_rel)
        if not source_path.is_file():
            raise ContractError(f"{path}: missing source {source_rel}")
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
            "sha256": _sha256(source_path),
            "line_count": len(source_lines),
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
            start = locator.get("line_start")
            end = locator.get("line_end")
            if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start or end > len(source_lines):
                raise ContractError(f"{card_id}: invalid source line range {start}-{end} for {source_rel}")
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
            owners = _require_list(card.get("owner_ids"), f"{card_id}.owner_ids")
            if not owners or any(owner not in owner_registry for owner in owners):
                raise ContractError(f"{card_id}: one or more owner IDs are invalid")
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
            for receipt_value in receipts:
                receipt_rel = Path(_require_string(receipt_value, f"{card_id}.review.receipt"))
                if receipt_rel.is_absolute() or ".." in receipt_rel.parts:
                    raise ContractError(f"{card_id}: review receipt must be a root-relative corpus path")
                if not (root / receipt_rel).is_file():
                    raise ContractError(f"{card_id}: missing review receipt {receipt_rel.as_posix()}")
            if public_state == "bounded_current" and (review_state in {"typed", "l1_flagged"} or not receipts):
                raise ContractError(f"{card_id}: bounded current wording requires L2-or-later review and a receipt")
            cards[card_id] = {
                **card,
                "source": {"path": source_key, "work_id": work_id, "lifecycle": lifecycle},
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
        declared_cards = _require_list(work.get("claim_card_ids"), f"{work_id}.claim_card_ids")
        for card_id in declared_cards:
            if card_id not in cards:
                raise ContractError(f"{work_id}: unknown claim-card id {card_id}")
            if cards[card_id]["source"]["work_id"] != work_id:
                raise ContractError(f"{work_id}: claim-card {card_id} belongs to another work")
        chapter_order = _require_list(work.get("chapter_order"), f"{work_id}.chapter_order")
        if declared_cards:
            covered = {chapter for card_id in declared_cards for chapter in cards[card_id]["chapters"]}
            missing_chapters = [chapter for chapter in chapter_order if chapter not in covered]
            if missing_chapters:
                raise ContractError(f"{work_id}: chapters lack claim-card coverage: {', '.join(missing_chapters)}")
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
            manifest_sources.append({
                "work_id": work_id,
                "path": source_rel_value,
                "lifecycle": lifecycle,
                "sha256": _sha256(source_path),
                "external_readonly": not source_path.is_relative_to(root),
            })
        public_route = work.get("public_route")
        if public_route is not None:
            public_path = (root / BOOK_MANIFEST_PATH.parent / Path(_require_string(public_route, f"{work_id}.public_route"))).resolve()
            if not public_path.is_file():
                raise ContractError(f"{work_id}: missing public route {public_route}")

    if set(work_cards) - manifest_ids:
        raise ContractError(f"claim-card works absent from book manifest: {sorted(set(work_cards) - manifest_ids)}")

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
            "owner_ids": sorted(card["owner_ids"]),
            "dependency_ids": sorted(card["dependencies"]),
            "docket_ids": sorted(card["docket_ids"]),
            "disposition": card["disposition"],
            "review_state": card["review"]["state"],
            "public_state": card["public"]["state"],
        })
    register = {
        "schema": "emergentism/claim-card-register/v1",
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
        for owner in sorted(card["owner_ids"]):
            graph_edges.append({"from": card_id, "kind": "owned_by", "to": owner})
        for dependency in sorted(card["dependencies"]):
            graph_edges.append({"from": card_id, "kind": "depends_on", "to": dependency})
        for docket_id in sorted(card["docket_ids"]):
            graph_edges.append({"from": card_id, "kind": "tested_by", "to": docket_id})
        graph_edges.append({"from": card_id, "kind": "projected_from", "to": card["source"]["work_id"]})
    for owner, owner_path in sorted(owner_registry.items()):
        graph_nodes.append({"id": owner, "kind": "semantic_owner", "path": owner_path})
    for docket_id in sorted(docket_map):
        graph_nodes.append({"id": docket_id, "kind": "adequacy_docket", "status": docket_map[docket_id]["status"]})
    for work_id in sorted(manifest_ids):
        graph_nodes.append({"id": work_id, "kind": "book_projection"})
    graph = {
        "schema": "emergentism/claim-owner-dependency-graph/v1",
        "authority": "derived graph; publication and graph membership provide no evidence",
        "nodes": sorted(graph_nodes, key=lambda row: (row["kind"], row["id"])),
        "edges": sorted(graph_edges, key=lambda row: (row["from"], row["kind"], row["to"])),
        "metrics": {"nodes": len(graph_nodes), "edges": len(graph_edges)},
    }

    lifecycle_sources = list(sources.values()) + manifest_sources
    lifecycle_counts = Counter(row["lifecycle"] for row in lifecycle_sources)
    lifecycle = {
        "schema": "emergentism/claim-lifecycle-inventory/v1",
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
