#!/usr/bin/env python3
"""Deterministic lifecycle metadata for the frozen library and current reader."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


SITE_ROOT = Path(__file__).resolve().parent
CORPUS_ROOT = SITE_ROOT.parent


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_reader_contract() -> dict[str, Any]:
    books = _load(CORPUS_ROOT / "13_BOOKS/book-manifest.json")
    register = _load(CORPUS_ROOT / "00_META/registers/CLAIM_CARD_REGISTER.json")
    build = _load(SITE_ROOT / "book/build-manifest.json")
    parity = _load(SITE_ROOT / "public_semantic_parity.json")

    work = next((row for row in books.get("works", []) if row.get("work_id") == "BK-ONE-SITTING"), None)
    if not isinstance(work, dict):
        raise ValueError("book manifest has no BK-ONE-SITTING work")

    source = (CORPUS_ROOT / "13_BOOKS" / work["historical_sources"][0]).resolve()
    source_rel = source.relative_to(CORPUS_ROOT).as_posix()
    source_revision = f"sha256:{_sha256(source)}"
    parity_contract = parity.get("claimCardContract", {})
    if parity_contract.get("sourceRevision") != source_revision:
        raise ValueError("public semantic parity source revision is stale")

    register_ids = sorted(
        row["card_id"] for row in register.get("cards", []) if row.get("work_id") == work["work_id"]
    )
    declared_ids = sorted(work.get("claim_card_ids", []))
    if register_ids != declared_ids:
        raise ValueError("current-reader claim cards disagree with the derived register")

    graph_path = CORPUS_ROOT / build["claim_card_contract"]["graph_path"]
    if build["claim_card_contract"].get("graph_sha256") != _sha256(graph_path):
        raise ValueError("public book build manifest has stale claim-graph provenance")

    # 2026-07-31. BK-ONE-SITTING is still the claim-carded work whose provenance is pinned
    # below, and that chain is unchanged. But it is no longer the WHOLE of what book/
    # publishes: the route now carries the ported 25-chapter Reciprocal with the One-Sitting
    # edition as an appendix. Leaving the old fields alone would have left this manifest
    # describing the route as a single short work while the gate went green — a check
    # passing a false description, which is the failure this corpus least tolerates.
    # route_contains is derived from the build manifest, so it cannot drift from what
    # actually shipped.
    ordered = build.get("ordered_source_paths") or []
    ported = [p for p in ordered if p.startswith("13_BOOKS/the_reciprocal/")]

    return {
        "work_id": work["work_id"],
        "title": work["title"],
        "href": "book/",
        "edition": work["edition"],
        "route_contains": {
            "note": (
                "book/ publishes more than the claim-carded work named above. The claim-card "
                "provenance in this block covers that work only; the ported chapters are "
                "tiered [D] and are not claim-carded."
            ),
            "ported_book": "The Reciprocal, ported from the 2026-07-22 Public Edition",
            "ported_chapter_files": len(ported),
            "ported_source_dir": "13_BOOKS/the_reciprocal/",
            "appendices": [p for p in ordered if not p.startswith("13_BOOKS/the_reciprocal/")],
            "total_ordered_sources": len(ordered),
        },
        "source": source_rel,
        "source_revision": source_revision,
        "lifecycle": parity_contract["lifecycle"],
        "public_disposition": parity_contract["publicDisposition"],
        "claim_card_ids": declared_ids,
        "claim_card_register": "00_META/registers/CLAIM_CARD_REGISTER.json",
        "claim_card_register_sha256": _sha256(CORPUS_ROOT / "00_META/registers/CLAIM_CARD_REGISTER.json"),
        "claim_graph": build["claim_card_contract"]["graph_path"],
        "claim_graph_sha256": build["claim_card_contract"]["graph_sha256"],
        "build_manifest": "book/build-manifest.json",
        "output_sha256": build["output"]["sha256"],
        "authority": "Current-reader route metadata; source owners retain semantics and publication provides no evidence.",
    }


def apply_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    result = dict(manifest)
    result["lifecycle"] = "frozen_generated_library"
    result["current_reader"] = current_reader_contract()
    return result


def canonical_bytes(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
