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
    if work.get("release_state") != "source_active_current_public_reader":
        raise ValueError("BK-ONE-SITTING is not declared as the current public reader")
    if work.get("public_route") != "../12_PUBLIC_SITE/book/index.html":
        raise ValueError("BK-ONE-SITTING public route drift")

    publication_sources = work.get("publication_sources")
    if not isinstance(publication_sources, list) or len(publication_sources) != 1:
        raise ValueError("current reader must declare exactly one publication source")
    publication_source = publication_sources[0]
    if publication_source.get("public_eligible") is not True:
        raise ValueError("current reader source is not explicitly public-eligible")
    if publication_source.get("lifecycle") not in {"active", "reader_synthesis"}:
        raise ValueError("current reader source has a barred lifecycle")
    source_rel = publication_source["path"]
    source = (CORPUS_ROOT / source_rel).resolve()
    if not source.is_file() or source.relative_to(CORPUS_ROOT).as_posix() != source_rel:
        raise ValueError("current reader source is missing or escapes the corpus")
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

    if build.get("schema") != "emergentism/public-book-build/v2":
        raise ValueError("public book build manifest schema drift")
    if build.get("work_id") != work["work_id"]:
        raise ValueError("public book build work mismatch")
    catalog_contract = build.get("catalog_contract", {})
    if (
        catalog_contract.get("schema") != books.get("schema")
        or catalog_contract.get("path") != "13_BOOKS/book-manifest.json"
        or catalog_contract.get("sha256") != _sha256(CORPUS_ROOT / "13_BOOKS/book-manifest.json")
        or catalog_contract.get("release_state") != work["release_state"]
        or catalog_contract.get("public_route") != work["public_route"]
    ):
        raise ValueError("public book catalog contract drift")
    if build.get("ordered_source_paths") != [source_rel]:
        raise ValueError("public book includes an undeclared or non-current source")
    build_sources = build.get("sources")
    if not isinstance(build_sources, list) or len(build_sources) != 1:
        raise ValueError("public book build must contain exactly one source contract")
    built_source = build_sources[0]
    if (
        built_source.get("path") != source_rel
        or built_source.get("lifecycle") != publication_source["lifecycle"]
        or built_source.get("public_eligible") is not True
        or built_source.get("claim_card_set") != publication_source["claim_card_set"]
    ):
        raise ValueError("public book source lifecycle/coverage contract drift")
    if built_source.get("sha256") != _sha256(source):
        raise ValueError("public book source revision drift")
    coverage = build.get("claim_card_contract", {}).get("coverage", {})
    if sorted(coverage.get("claim_card_ids", [])) != declared_ids:
        raise ValueError("public book claim-card coverage drift")
    if set(coverage.get("covered_chapters", [])) != set(work.get("chapter_order", [])):
        raise ValueError("public book chapter coverage drift")
    if set(coverage.get("public_states", [])) - {"bounded_current", "candidate"}:
        raise ValueError("public book contains a non-current claim-card state")
    if set(coverage.get("review_states", [])) - {"implemented", "l3_audited"}:
        raise ValueError("public book contains an unreviewed claim-card state")

    graph_path = CORPUS_ROOT / build["claim_card_contract"]["graph_path"]
    if build["claim_card_contract"].get("graph_sha256") != _sha256(graph_path):
        raise ValueError("public book build manifest has stale claim-graph provenance")

    return {
        "work_id": work["work_id"],
        "title": work["title"],
        "href": "book/",
        "edition": work["edition"],
        "publication_scope": {
            "ordered_sources": [source_rel],
            "source_count": 1,
            "claim_card_count": len(declared_ids),
            "covered_chapters": coverage["covered_chapters"],
            "withheld_provenance": {
                "path": "13_BOOKS/the_reciprocal/",
                "included_in_book": False,
                "included_in_rag": False,
            },
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
    withheld = _load(SITE_ROOT / "withheld-routes.json")
    withheld_hrefs = {
        row["manifestDocument"]["href"]
        for row in withheld.get("artifacts", [])
        if isinstance(row.get("manifestDocument"), dict)
        and row["manifestDocument"].get("href")
    }
    # A withheld frozen-library landing page withdraws that whole catalogue from
    # the *current* reader.  Its individual noindex projections stay in source
    # custody, but a current reading manifest must not make their descendants
    # look like an endorsed public path merely because their old root happened
    # to contain no direct manifestDocument row.
    withheld_library_roots = {
        artifact.removesuffix("index.html")
        for row in withheld.get("artifacts", [])
        if isinstance((artifact := row.get("artifact")), str)
        and artifact.endswith("/index.html")
        and artifact.count("/") == 1
    }

    def is_withheld_current_href(href: object) -> bool:
        return isinstance(href, str) and (
            href in withheld_hrefs
            or any(href.startswith(root) for root in withheld_library_roots)
        )

    result["documents"] = [
        row for row in result.get("documents", [])
        if not is_withheld_current_href(row.get("href"))
    ]
    result["routes"] = {
        name: href
        for name, href in result.get("routes", {}).items()
        if not is_withheld_current_href(href)
    }
    result["lifecycle"] = "frozen_generated_library"
    result["current_reader"] = current_reader_contract()
    return result


def canonical_bytes(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
