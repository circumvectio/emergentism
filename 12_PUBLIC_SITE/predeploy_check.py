#!/usr/bin/env python3
"""Fail-closed gate for the deny-by-default Emergentism public release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "release-manifest.json"
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".mjs", ".txt", ".webmanifest", ".xml"}
FORBIDDEN_NAMES = (
    "Skyzai", "VMOSK", "VMOSK-A", "K2", "PRISM", "DAV", "DAC", "Agentz",
    "Menexus", "Aureus", "OFN", "APU.BOT", "Circle.news",
)
FORBIDDEN_NAME_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9])(?:" + "|".join(re.escape(x) for x in FORBIDDEN_NAMES) + r")(?![A-Za-z0-9])"
)
FORBIDDEN_CLAIM_RE = {
    "physical light-cone inflation": re.compile(r"(?i)physical\s+light\s*cone.{0,24}(?:widen|expand)"),
    "invalid scalar sampling": re.compile(r"Sample\s*\[\s*∫"),
    "Born/chart conflation": re.compile(r"(?i)Born\s+rule\s*(?:=|is)\s*(?:φ\s*[·×*]\s*ν|phi\s*[·×*]\s*nu)"),
    "quantum dimensional stacking": re.compile(r"(?i)(?:Everett|Copenhagen).{0,80}(?:five|four|5|4)[- ]dimensional"),
    "retired GFS positive validation": re.compile(
        r"(?is)(?:Global\s+Flourishing\s+Study|\bGFS\b).{0,100}"
        r"(?:validat(?:e[sd]?|ion)|confirm(?:s|ed|ation)?|prov(?:e[sd]?|ing)|"
        r"corroborat(?:e[sd]?|ion)|support(?:s|ed|ing)?|"
        r"evidence\s+for\s+(?:the\s+)?(?:framework|Emergentism))"
        r"|(?:validat(?:e[sd]?|ion)|confirm(?:s|ed|ation)?|prov(?:e[sd]?|ing)|"
        r"corroborat(?:e[sd]?|ion)|support(?:s|ed|ing)?).{0,100}"
        r"(?:Global\s+Flourishing\s+Study|\bGFS\b)"
    ),
    "noncanonical public host": re.compile(r"https://emergentism\.org(?:/|\b)"),
}
NOINDEX_ROUTES = {"/map/", "/journey/", "/test/", "/build/", "/atlas/", "/five-plus-one/"}
PUBLIC_ORIGIN = "https://www.emergentism.org"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str, str]] = []
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs if value is not None}
        if "id" in values:
            self.ids.append(values["id"])
        for attr in ("href", "src"):
            if attr in values:
                self.refs.append((tag.lower(), attr, values[attr]))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def manifest() -> dict:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 1 or data.get("status") != "pure-emergentism-release":
        raise ValueError("unsupported release manifest")
    return data


def expected_files(data: dict) -> set[str]:
    files = {row["file"] for row in data["routes"]}
    files.update(data["rootFiles"])
    files.update(data["assetFiles"])
    files.add("RELEASE_SHA256")
    return files


def output_files(out: Path) -> set[str]:
    return {path.relative_to(out).as_posix() for path in out.rglob("*") if path.is_file()}


def calculated_hash(out: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in out.rglob("*") if p.is_file() and p.name != "RELEASE_SHA256"):
        rel = path.relative_to(out).as_posix()
        digest.update(rel.encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def local_target(out: Path, current: Path, raw: str) -> tuple[Path | None, str]:
    parts = urlsplit(raw)
    if parts.scheme or raw.startswith("//"):
        return None, parts.fragment
    if not parts.path:
        return current, parts.fragment
    target = out / parts.path.lstrip("/") if parts.path.startswith("/") else current.parent / parts.path
    target = target.resolve()
    try:
        target.relative_to(out.resolve())
    except ValueError:
        return target, parts.fragment
    if target.is_dir() or parts.path.endswith("/"):
        target = target / "index.html"
    elif not target.exists() and not target.suffix:
        target = target / "index.html"
    return target, parts.fragment


def check_exact_tree(out: Path, data: dict, errors: list[str]) -> None:
    expected = expected_files(data)
    actual = output_files(out)
    for rel in sorted(expected - actual):
        fail(errors, f"missing release file: {rel}")
    for rel in sorted(actual - expected):
        fail(errors, f"undeclared release file: {rel}")
    for archive in data["archiveRoots"]:
        if any(rel == archive or rel.startswith(archive + "/") for rel in actual):
            fail(errors, f"archive escaped into release: {archive}")
    recorded = (out / "RELEASE_SHA256").read_text(encoding="ascii").strip() if (out / "RELEASE_SHA256").exists() else ""
    actual_hash = calculated_hash(out)
    if recorded != actual_hash:
        fail(errors, f"release hash mismatch: recorded={recorded or 'missing'} actual={actual_hash}")


def check_purity(out: Path, errors: list[str]) -> None:
    for path in sorted(p for p in out.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES):
        body = path.read_text(encoding="utf-8", errors="replace")
        if FORBIDDEN_NAME_RE.search(body):
            fail(errors, f"external-system leakage: {path.relative_to(out)}")
        for label, pattern in FORBIDDEN_CLAIM_RE.items():
            if pattern.search(body):
                fail(errors, f"{label}: {path.relative_to(out)}")
        for match in re.finditer(r"D6\s*(?:≡|=)\s*D0", body):
            context = body[max(0, match.start() - 180):match.end() + 180].lower()
            if not any(marker in context for marker in ("legacy", "literal", "died", "failed", "must not", "supersed", "<s>")):
                fail(errors, f"live literal closure identity: {path.relative_to(out)}")
        if "/book/rag_index.json" in body or "book-ai.js" in body:
            fail(errors, f"retired retrieval dependency: {path.relative_to(out)}")


def check_html_and_links(out: Path, data: dict, errors: list[str]) -> None:
    route_by_file = {row["file"]: row["path"] for row in data["routes"]}
    file_by_resolved = {(out / rel).resolve(): route for rel, route in route_by_file.items()}
    graph: dict[str, set[str]] = defaultdict(set)
    ids_by_path: dict[Path, set[str]] = {}
    parsers: dict[Path, PageParser] = {}

    for rel, route in route_by_file.items():
        path = out / rel
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        lowered = body.lower()
        for required in ("<!doctype html", "<html", "<head", "<body"):
            if required not in lowered:
                fail(errors, f"HTML structure missing {required}: {rel}")
        parser = PageParser()
        parser.feed(body)
        parsers[path.resolve()] = parser
        ids_by_path[path.resolve()] = set(parser.ids)
        if len(parser.ids) != len(set(parser.ids)):
            fail(errors, f"duplicate HTML id: {rel}")
        if route not in {"/", "/404/", "/offline/", "/atlas/"} and not re.search(r"\[(?:A|B|S|I|D|C)\]", body):
            fail(errors, f"page lacks an evidence-tier marker: {rel}")

    for current, parser in parsers.items():
        current_route = file_by_resolved[current]
        for tag, attr, raw in parser.refs:
            parts = urlsplit(raw)
            if parts.scheme in {"http", "https"}:
                resource = attr == "src" or (tag == "link" and re.search(r"stylesheet|icon|manifest", raw, re.I))
                if resource:
                    fail(errors, f"external resource reference: {current.relative_to(out)} -> {raw}")
                continue
            if parts.scheme in {"mailto", "data", "javascript"} or raw.startswith(("//", "#")):
                continue
            target, fragment = local_target(out, current, raw)
            if target is None:
                continue
            try:
                rel_target = target.resolve().relative_to(out.resolve())
            except ValueError:
                fail(errors, f"link escapes release: {current.relative_to(out)} -> {raw}")
                continue
            if not target.is_file():
                fail(errors, f"broken local reference: {current.relative_to(out)} -> {raw}")
                continue
            resolved = target.resolve()
            if resolved in file_by_resolved and tag == "a":
                graph[current_route].add(file_by_resolved[resolved])
            if fragment and resolved in ids_by_path and fragment not in ids_by_path[resolved]:
                fail(errors, f"missing fragment #{fragment}: {current.relative_to(out)} -> {rel_target}")

    atlas = json.loads((out / "atlas/site_index.json").read_text(encoding="utf-8"))
    atlas_routes = {page["href"] for section in atlas.get("tree", []) for page in section.get("pages", [])}
    expected_atlas = {row["path"] for row in data["routes"]} - {"/404/", "/offline/", "/atlas/"}
    if atlas_routes != expected_atlas:
        fail(errors, f"atlas route drift: missing={sorted(expected_atlas-atlas_routes)} extra={sorted(atlas_routes-expected_atlas)}")
    graph["/atlas/"].update(atlas_routes)
    for route in list(graph):
        if route != "/atlas/":
            graph[route].add("/atlas/")

    reached = {"/"}
    queue = deque(["/"])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in reached:
                reached.add(nxt)
                queue.append(nxt)
    expected_reachable = {row["path"] for row in data["routes"]} - {"/404/", "/offline/"}
    for route in sorted(expected_reachable - reached):
        fail(errors, f"release route is unreachable: {route}")


def check_css_and_js_closure(out: Path, errors: list[str]) -> None:
    patterns = [
        re.compile(r"url\(\s*['\"]?([^)'\"]+)"),
        re.compile(r"\bfrom\s+['\"]([^'\"]+)['\"]"),
        re.compile(r"\b(?:import|fetch)\(\s*['\"]([^'\"]+)['\"]"),
    ]
    for path in sorted(p for p in out.rglob("*") if p.suffix.lower() in {".css", ".js", ".mjs"}):
        body = path.read_text(encoding="utf-8", errors="replace")
        for pattern in patterns:
            for raw in pattern.findall(body):
                if raw.startswith(("data:", "#")) or urlsplit(raw).scheme or (not raw.startswith(("/", "."))):
                    continue
                target, _ = local_target(out, path.resolve(), raw)
                if target is not None and not target.is_file():
                    fail(errors, f"broken code dependency: {path.relative_to(out)} -> {raw}")


def check_metadata(out: Path, data: dict, errors: list[str]) -> None:
    pwa = json.loads((out / "manifest.webmanifest").read_text(encoding="utf-8"))
    if pwa.get("start_url") != "/" or pwa.get("id") != "/compass/":
        fail(errors, "PWA identity or start URL drifted")
    sw = (out / "sw.js").read_text(encoding="utf-8")
    precache_match = re.search(r"const PRECACHE = (\[.*?\]);", sw, flags=re.DOTALL)
    if not precache_match:
        fail(errors, "service-worker precache list missing")
    else:
        precache = json.loads(precache_match.group(1))
        for raw in precache:
            target, _ = local_target(out, (out / "sw.js").resolve(), raw)
            if target is None or not target.is_file():
                fail(errors, f"service-worker precache target missing: {raw}")
    sitemap = ElementTree.parse(out / "sitemap.xml")
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    listed = {urlsplit(node.text or "").path for node in sitemap.findall(".//s:loc", namespace)}
    expected = {row["path"] for row in data["routes"]} - {"/404/", "/offline/"} - NOINDEX_ROUTES
    if listed != expected:
        fail(errors, f"sitemap route drift: missing={sorted(expected-listed)} extra={sorted(listed-expected)}")

    for row in data["routes"]:
        route = row["path"]
        body = (out / row["file"]).read_text(encoding="utf-8", errors="replace")
        expected_url = PUBLIC_ORIGIN + route
        canonical = re.findall(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', body, re.I)
        og_urls = re.findall(r'<meta\s+[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']+)', body, re.I)
        if canonical != [expected_url]:
            fail(errors, f"canonical URL drift: {row['file']} expected={expected_url} actual={canonical}")
        if og_urls != [expected_url]:
            fail(errors, f"og:url drift: {row['file']} expected={expected_url} actual={og_urls}")
        robots = re.findall(r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']+)', body, re.I)
        if route in NOINDEX_ROUTES | {"/offline/"} and not any("noindex" in value.lower() for value in robots):
            fail(errors, f"secondary route lacks noindex: {row['file']}")


def check_build_boundary(errors: list[str]) -> None:
    vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    if vercel.get("outputDirectory") != ".release" or "build_release.py" not in (vercel.get("buildCommand") or ""):
        fail(errors, "Vercel is not bound to the manifest-built release")
    ignored = (ROOT / ".vercelignore").read_text(encoding="utf-8")
    for required in ("90_ARCHIVE/", ".release/", "output/", "*.md"):
        if required not in ignored:
            fail(errors, f".vercelignore lacks {required}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", default=".release")
    args = parser.parse_args()
    out = (ROOT / args.release).resolve()
    if not out.is_dir():
        print(f"FAIL: release directory missing: {out}")
        return 1
    try:
        data = manifest()
    except Exception as exc:
        print(f"FAIL: release manifest invalid: {exc}")
        return 1

    errors: list[str] = []
    check_exact_tree(out, data, errors)
    check_purity(out, errors)
    check_html_and_links(out, data, errors)
    check_css_and_js_closure(out, errors)
    check_metadata(out, data, errors)
    check_build_boundary(errors)

    if errors:
        print(f"FAIL: {len(errors)} release finding(s)")
        for message in errors:
            print(f" - {message}")
        return 1
    print(f"PASS: pure release routes={len(data['routes'])} files={len(output_files(out))} sha256={calculated_hash(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
