#!/usr/bin/env python3
"""
Probe the live Emergentism domain against the generated public reading manifest.

This is a post-deploy/cutover audit, not the local predeploy gate. By default it
prints an evidence summary and exits 0 so it can be used while the domain is
still known to be pointed at an older host. Use --strict after cutover to fail
when expected corpus routes, core front doors, or repository root markers are
missing.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


SITE_ROOT = Path(__file__).resolve().parent
DEFAULT_BASE_URL = "https://www.emergentism.org/"
WITHHELD_REGISTRY_PATH = SITE_ROOT / "withheld-routes.json"
PARITY_MANIFEST_PATH = SITE_ROOT / "public_semantic_parity.json"


def load_withheld_registry() -> dict[str, Any]:
    with WITHHELD_REGISTRY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_public_parity() -> dict[str, Any]:
    with PARITY_MANIFEST_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


WITHHELD_REGISTRY = load_withheld_registry()
PUBLIC_PARITY = load_public_parity()
HISTORICAL_BOUNDARY_MARKER = WITHHELD_REGISTRY["boundary"]["marker"]
HISTORICAL_BOUNDARY_PATH = WITHHELD_REGISTRY["boundary"]["publicRoute"]
RISKY_WITHHELD_BODY_MARKERS = (
    "The Complete Ontology of Reality",
    "MF-283: THE ORTHOGONALITY THEOREM",
    "MF-285: DREAMS ARE UNANCHORED D5",
    "MF-296: GRAVITY IS TIME",
    "MF-298: DARK MATTER AS MUTUAL INFORMATION",
    "/5+1 — The 5+1 Constitution",
    "The Burrisphere — Magnum Opus",
    "The Argument: Emergence as Lens on Dasein",
)
FROZEN_ROOTS = set(PUBLIC_PARITY["frozenLibraryRoots"])


def current_route_paths() -> list[str]:
    routes: list[str] = []
    for artifact in PUBLIC_PARITY["currentSurfaces"]:
        if not artifact.endswith("index.html"):
            continue
        if artifact.split("/", 1)[0] in FROZEN_ROOTS:
            continue
        routes.append("" if artifact == "index.html" else artifact[:-10])
    routes.extend(
        [
            "robots.txt", "sitemap.xml", "reading-manifest.json",
            "public_semantic_parity.json", "living-map.json",
            "atlas/site_index.json", "manifest.webmanifest",
        ]
    )
    return list(dict.fromkeys(routes))


CORE_PATHS = current_route_paths()
HASH_SAMPLE_ARTIFACTS = {
    "": "index.html",
    "practice/": "practice/index.html",
    "questions/": "questions/index.html",
    "churn/": "churn/index.html",
    "amrita/": "amrita/index.html",
    "halahala/": "halahala/index.html",
    "record/churning/": "record/churning/index.html",
    "churn/corpus.json": "churn/corpus.json",
    "churn/corpus.jsonl": "churn/corpus.jsonl",
    "public_semantic_parity.json": "public_semantic_parity.json",
    "living-map.json": "living-map.json",
    "atlas/site_index.json": "atlas/site_index.json",
    "manifest.webmanifest": "manifest.webmanifest",
    "sw.js": "sw.js",
}
DEFAULT_BODY_READ_LIMIT = 220_000


@dataclass(frozen=True)
class ProbeResult:
    path: str
    status: int | str
    final_url: str
    title: str
    bytes_read: int
    body_sha256: str
    repo_worldview_identity: bool
    repo_finity_action: bool
    repo_finity_card: bool
    repo_local_receipt: bool
    repo_generated_manifest: bool
    repo_historical_boundary: bool
    risky_withheld_body: bool
    old_vmgsta_markers: bool
    google_sites_markers: bool
    x_robots_tag: str
    cache_control: str
    cdn_cache_control: str
    error: str = ""


def load_manifest() -> dict[str, Any]:
    manifest_path = SITE_ROOT / "reading-manifest.json"
    with manifest_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def title_from_html(text: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()[:120]


def probe(base_url: str, path: str, timeout: float) -> ProbeResult:
    url = urljoin(base_url, path)
    request = Request(
        url,
        headers={"User-Agent": "Codex Emergentism live corpus audit"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            artifact = HASH_SAMPLE_ARTIFACTS.get(path)
            local_artifact = SITE_ROOT / artifact if artifact is not None else None
            # Exact release witnesses must hash the complete expected object.
            # Read one byte beyond its committed local size so an unexpectedly
            # longer response also fails closed, while keeping every response
            # bounded even if the remote host is compromised or misrouted.
            read_limit = DEFAULT_BODY_READ_LIMIT
            if local_artifact is not None and local_artifact.is_file():
                read_limit = local_artifact.stat().st_size + 1
            body = response.read(read_limit)
            return build_result(
                path,
                response.status,
                response.geturl(),
                body,
                response.headers,
            )
    except HTTPError as exc:
        try:
            body = exc.read(60_000)
            return build_result(path, exc.code, exc.geturl(), body, exc.headers)
        except Exception as read_exc:  # pragma: no cover - network dependent
            return ProbeResult(
                path=path,
                status=exc.code,
                final_url=exc.geturl(),
                title="",
                bytes_read=0,
                body_sha256="",
                repo_worldview_identity=False,
                repo_finity_action=False,
                repo_finity_card=False,
                repo_local_receipt=False,
                repo_generated_manifest=False,
                repo_historical_boundary=False,
                risky_withheld_body=False,
                old_vmgsta_markers=False,
                google_sites_markers=False,
                x_robots_tag="",
                cache_control="",
                cdn_cache_control="",
                error=f"HTTPError body read failed: {type(read_exc).__name__}: {read_exc}",
            )
    except Exception as exc:  # pragma: no cover - network dependent
        return ProbeResult(
            path=path,
            status="ERR",
            final_url=url,
            title="",
            bytes_read=0,
            body_sha256="",
            repo_worldview_identity=False,
            repo_finity_action=False,
            repo_finity_card=False,
            repo_local_receipt=False,
            repo_generated_manifest=False,
            repo_historical_boundary=False,
            risky_withheld_body=False,
            old_vmgsta_markers=False,
            google_sites_markers=False,
            x_robots_tag="",
            cache_control="",
            cdn_cache_control="",
            error=f"{type(exc).__name__}: {exc}",
        )


def build_result(
    path: str,
    status: int,
    final_url: str,
    body: bytes,
    headers: Any,
) -> ProbeResult:
    text = body.decode(
        headers.get_content_charset() or "utf-8",
        errors="replace",
    )
    return ProbeResult(
        path=path,
        status=status,
        final_url=final_url,
        title=title_from_html(text),
        bytes_read=len(body),
        body_sha256=hashlib.sha256(body).hexdigest(),
        repo_worldview_identity="A worldview for finite beings" in text,
        repo_finity_action="Frame one decision" in text,
        repo_finity_card="Finity Card" in text,
        repo_local_receipt="private two-face receipt" in text,
        repo_generated_manifest=(
            "Generated by 12_PUBLIC_SITE" in text or "reading-manifest.json" in text
        ),
        repo_historical_boundary=HISTORICAL_BOUNDARY_MARKER in text,
        risky_withheld_body=any(marker in text for marker in RISKY_WITHHELD_BODY_MARKERS),
        old_vmgsta_markers=all(
            marker in text for marker in ["Vision", "Mission", "Strategy", "Tactics", "Action"]
        ),
        google_sites_markers=("Google Sites" in text or "sites.google.com" in text),
        x_robots_tag=headers.get("X-Robots-Tag", ""),
        cache_control=headers.get("Cache-Control", ""),
        cdn_cache_control=headers.get("CDN-Cache-Control", ""),
    )


def unique_paths(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for path in paths:
        if path not in seen:
            result.append(path)
            seen.add(path)
    return result


def run_audit(base_url: str, timeout: float, workers: int) -> dict[str, Any]:
    manifest = load_manifest()
    manifest_paths = [doc["href"].lstrip("/") for doc in manifest["documents"]]
    withheld_paths = unique_paths(
        [WITHHELD_REGISTRY["boundary"]["publicRoute"].lstrip("/")]
        + [
            route.lstrip("/")
            for item in WITHHELD_REGISTRY["artifacts"]
            for route in item["publicRoutes"]
        ]
    )
    # Hash witnesses are a separate release invariant: a sampled artifact may
    # be intentionally absent from both the reading manifest and the current
    # HTML route set (for example corpus JSON/JSONL or the service worker).
    # Every witness therefore has to enter the probe plan explicitly; otherwise
    # the strict audit reports a false ``NOT_PROBED`` mismatch.
    paths = unique_paths(
        CORE_PATHS
        + manifest_paths
        + withheld_paths
        + list(HASH_SAMPLE_ARTIFACTS)
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(lambda path: probe(base_url, path, timeout), paths))

    manifest_set = set(manifest_paths)
    core_set = set(CORE_PATHS)
    withheld_set = set(withheld_paths)
    manifest_results = [result for result in results if result.path in manifest_set]
    core_results = [result for result in results if result.path in core_set]
    withheld_results = [result for result in results if result.path in withheld_set]
    result_by_path = {result.path: result for result in results}
    sampled_hashes = []
    for path, artifact in HASH_SAMPLE_ARTIFACTS.items():
        local_path = SITE_ROOT / artifact
        result = result_by_path.get(path)
        expected = hashlib.sha256(local_path.read_bytes()).hexdigest() if local_path.is_file() else ""
        served = result.body_sha256 if result is not None else ""
        sampled_hashes.append(
            {
                "path": path,
                "artifact": artifact,
                "status": result.status if result is not None else "NOT_PROBED",
                "expected_sha256": expected,
                "served_sha256": served,
                "matches": bool(expected and served and expected == served),
            }
        )
    withheld_manifest_hrefs = {
        item["manifestDocument"]["href"]
        for item in WITHHELD_REGISTRY["artifacts"]
        if item.get("manifestDocument") is not None
    }

    return {
        "base_url": base_url,
        "generated_by": manifest.get("generated_by"),
        "source_snapshot": manifest.get("source_snapshot"),
        "manifest_documents": len(manifest_paths),
        "total_probes": len(results),
        "status_counts": dict(Counter(str(result.status) for result in results)),
        "manifest_status_counts": dict(
            Counter(str(result.status) for result in manifest_results)
        ),
        "core_results": [asdict(result) for result in core_results],
        "withheld_results": [asdict(result) for result in withheld_results],
        "sampled_hashes": sampled_hashes,
        "withheld_manifest_leaks": sorted(withheld_manifest_hrefs & set(manifest_paths)),
        "sample_manifest_failures": [
            asdict(result) for result in manifest_results if result.status != 200
        ][:20],
    }


def print_summary(report: dict[str, Any]) -> None:
    print("Emergentism live-domain corpus audit")
    print(f"base_url: {report['base_url']}")
    print(f"manifest_documents: {report['manifest_documents']}")
    print(f"total_probes: {report['total_probes']}")
    print(f"status_counts: {report['status_counts']}")
    print(f"manifest_status_counts: {report['manifest_status_counts']}")
    print()
    print("Core routes:")
    for result in report["core_results"]:
        path = result["path"] or "/"
        marker_bits = []
        if result["repo_worldview_identity"]:
            marker_bits.append("repo:Worldview")
        if result["repo_finity_action"]:
            marker_bits.append("repo:Action")
        if result["repo_finity_card"]:
            marker_bits.append("repo:Card")
        if result["old_vmgsta_markers"]:
            marker_bits.append("old:VMGSTA")
        if result["google_sites_markers"]:
            marker_bits.append("google-sites")
        markers = ",".join(marker_bits) or "-"
        print(f"- {path}: {result['status']} final={result['final_url']} markers={markers}")
    print()
    print("Sampled served hashes:")
    for sample in report["sampled_hashes"]:
        path = sample["path"] or "/"
        verdict = "MATCH" if sample["matches"] else "MISMATCH"
        print(f"- {path}: {verdict} ({sample['status']})")
    print()
    print("Withheld routes:")
    for result in report["withheld_results"]:
        marker = "boundary" if result["repo_historical_boundary"] else "MISSING-BOUNDARY"
        risky = " RISKY-BODY" if result["risky_withheld_body"] else ""
        print(
            f"- {result['path']}: {result['status']} final={result['final_url']} "
            f"marker={marker}{risky} robots={result['x_robots_tag']!r} "
            f"cache={result['cache_control']!r}"
        )


def strict_failures(report: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    manifest_status = report["manifest_status_counts"]
    all_manifest_live = manifest_status == {"200": report["manifest_documents"]}
    if not all_manifest_live:
        failures.append(
            "generated manifest documents are not all 200 "
            f"(manifest_status_counts={manifest_status})"
        )

    if report["withheld_manifest_leaks"]:
        failures.append(
            "withheld routes leaked into reading-manifest.json "
            f"({report['withheld_manifest_leaks']})"
        )

    bad_withheld = []
    for result in report["withheld_results"]:
        robots = {
            token.strip().lower()
            for token in result["x_robots_tag"].split(",")
            if token.strip()
        }
        required_robots = {"noindex", "noarchive", "nosnippet"}
        if (
            result["status"] != 200
            or not result["repo_historical_boundary"]
            or urlparse(result["final_url"]).path != HISTORICAL_BOUNDARY_PATH
            or result["risky_withheld_body"]
            or not required_robots.issubset(robots)
            or "no-store" not in result["cache_control"].lower()
            or "no-store" not in result["cdn_cache_control"].lower()
        ):
            bad_withheld.append(result)
    if bad_withheld:
        sample = ", ".join(
            f"{result['path']}={result['status']}"
            for result in bad_withheld[:12]
        )
        suffix = "" if len(bad_withheld) <= 12 else f", +{len(bad_withheld) - 12} more"
        failures.append(
            "withheld routes do not all serve the no-store/noindex historical "
            f"boundary ({sample}{suffix})"
        )

    bad_core = [
        result for result in report["core_results"] if result["status"] != 200
    ]
    if bad_core:
        sample = ", ".join(
            f"{result['path'] or '/'}={result['status']}" for result in bad_core[:12]
        )
        suffix = "" if len(bad_core) <= 12 else f", +{len(bad_core) - 12} more"
        failures.append(f"core/front-door routes are not all 200 ({sample}{suffix})")

    bad_hashes = [sample for sample in report["sampled_hashes"] if not sample["matches"]]
    if bad_hashes:
        sample = ", ".join((item["path"] or "/") for item in bad_hashes)
        failures.append(f"sampled served hashes differ from the local release ({sample})")

    root = next(
        (result for result in report["core_results"] if result["path"] == ""),
        None,
    )
    if root is None:
        failures.append("root route was not probed")
        return failures

    if not root["repo_worldview_identity"]:
        failures.append("root route is missing worldview marker: A worldview for finite beings")
    if not root["repo_finity_action"]:
        failures.append("root route is missing Finity action marker: Frame one decision")
    if root["old_vmgsta_markers"]:
        failures.append("root route still contains old VMGSTA link-hub markers")
    if root["google_sites_markers"]:
        failures.append("root route still contains Google Sites markers")

    practice = next(
        (result for result in report["core_results"] if result["path"] == "practice/"),
        None,
    )
    if practice is None or not practice["repo_finity_card"]:
        failures.append("practice route is missing source-practice marker: Finity Card")
    if practice is None or not practice["repo_local_receipt"]:
        failures.append("practice route is missing local commitment/outcome receipt marker")

    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--json", action="store_true", help="print full JSON report")
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "exit non-zero unless generated documents, core routes, and root "
            "repository markers prove cutover"
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    report = run_audit(args.base_url, args.timeout, args.workers)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_summary(report)

    if args.strict:
        failures = strict_failures(report)
        if failures:
            print("\nStrict audit failures:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
