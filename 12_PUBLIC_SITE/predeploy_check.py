#!/usr/bin/env python3
"""
Pre-deploy supply-chain gate for 12_PUBLIC_SITE.

Checks:
1. No external http(s) resource references (security gate)
2. All internal hrefs resolve to existing files
3. No orphan pages (every public page has at least one inbound link)
4. Required assets present where referenced
5. Basic HTML well-formedness (DOCTYPE, html/head/body tags)
6. Tier-marker presence on doctrine pages
7. Operators route uses current evidence tier markers
8. Public reading bundle is wired
9. Generated library pages preserve the generator chrome contract
10. Historical-withholding bytes, redirects, and search boundary agree
11. Deployment publication boundary excludes source/control/runtime files
12. Current/provisional public semantics match their source contract
13. Claim cards, lifecycles, and barred-claim policy match source contracts
14. The public book and its build manifest match deterministic source hashes
15. The frozen-library manifest names the current reader deterministically
16. The contact-limited public lifecycle has zero unclassified artifacts

Exit 0 if all checks pass, 1 if any fail.
"""

import json
import hashlib
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
WITHHELD_REGISTRY_PATH = os.path.join(BASE_DIR, "withheld-routes.json")
ERRORS = []
WARNINGS = []


def load_withheld_registry():
    with open(WITHHELD_REGISTRY_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def withheld_artifact_paths():
    return {item["artifact"] for item in load_withheld_registry()["artifacts"]}

def error(msg):
    ERRORS.append(msg)
    print(f"  ✗ {msg}")

def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠ {msg}")

def ok(msg):
    print(f"  ✓ {msg}")

def get_public_html_files():
    files = []
    withheld = withheld_artifact_paths()
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [
            d for d in dirs if d not in {"node_modules", "vendor", ".git", ".vercel", ".next",
                                          "90_ARCHIVE", "_archive", "_STAGING_COMPASS_RESTRUCTURE"}
        ]
        for f in filenames:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
                if not rel.startswith("partials/") and rel.replace(os.sep, "/") not in withheld:
                    files.append(rel)
    return sorted(files)

def read_file(rel_path):
    path = os.path.join(BASE_DIR, rel_path)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()

def extract_hrefs(body):
    static_body = re.sub(r"<script\b[^>]*>.*?</script>", "", body, flags=re.IGNORECASE | re.DOTALL)
    return re.findall(r'href="([^"]+)"', static_body)

def extract_base_href(body):
    match = re.search(r'<base\b[^>]*href="([^"]+)"', body, flags=re.IGNORECASE)
    return match.group(1) if match else None

def resolve_link(from_file, href, base_href=None):
    if href.startswith(("http://", "https://", "//", "mailto:", "javascript:", "data:", "#")):
        return None, "external"
    # Strip fragment before path resolution (page/#anchor targets the page)
    href = href.split("#", 1)[0]
    if not href:
        return None, "external"
    if href.startswith("/"):
        target = os.path.normpath(os.path.join(BASE_DIR, href.lstrip("/")))
        return target, "absolute"
    from_dir = os.path.dirname(from_file)
    base_dir = os.path.normpath(os.path.join(BASE_DIR, from_dir, base_href or ""))
    target = os.path.normpath(os.path.join(base_dir, href))
    return target, "relative"

def check_external_refs():
    print("\n[1] External resource references (security gate)")
    found = False
    for html_file in get_public_html_files():
        body = read_file(html_file)
        # Flag external stylesheets (security concern)
        matches = re.finditer(r'<link[^>]*rel="stylesheet"[^>]*href="(https?://[^"]+)"', body)
        for m in matches:
            found = True
            error(f"{html_file}: external stylesheet -> {m.group(1)}")
        # Flag external scripts/modules (security concern)
        matches = re.finditer(r'<script[^>]*src="(https?://[^"]+)"', body)
        for m in matches:
            found = True
            error(f"{html_file}: external script -> {m.group(1)}")
        # Flag external img/media src
        for tag in ["img", "video", "audio", "source", "iframe"]:
            pattern = rf'<{tag}[^>]*src="(https?://[^"]+)"'
            matches = re.finditer(pattern, body, re.IGNORECASE)
            for m in matches:
                found = True
                error(f"{html_file}: external {tag} -> {m.group(1)}")
    if not found:
        ok("No external script/stylesheet/media references")
    return not found

def check_internal_links():
    print("\n[2] Internal link resolution")
    dead = []
    for html_file in get_public_html_files():
        body = read_file(html_file)
        base_href = extract_base_href(body)
        for href in extract_hrefs(body):
            target, ltype = resolve_link(html_file, href, base_href)
            if target is None:
                continue
            if os.path.exists(target):
                continue
            if os.path.isdir(target) and os.path.exists(os.path.join(target, "index.html")):
                continue
            if not href.endswith("/") and not os.path.splitext(target)[1]:
                index_file = os.path.join(target, "index.html")
                if os.path.exists(index_file):
                    continue
            dead.append((html_file, href, os.path.relpath(target, BASE_DIR)))
    if dead:
        for src, href, missing in dead:
            error(f"{src} -> {href} (missing: {missing})")
    else:
        ok("All internal links resolve")
    return len(dead) == 0

def check_orphans():
    print("\n[3] Orphan page check")
    html_files = get_public_html_files()
    html_set = {os.path.normpath(os.path.join(BASE_DIR, f)) for f in html_files}
    # Crawl root = the site's actual front door.
    entry = os.path.normpath(os.path.join(BASE_DIR, "index.html"))
    reachable = set()
    queue = [entry] if os.path.exists(entry) else []
    while queue:
        full = os.path.normpath(queue.pop(0))
        if full in reachable or full not in html_set:
            continue
        reachable.add(full)
        html_file = os.path.relpath(full, BASE_DIR)
        body = read_file(html_file)
        base_href = extract_base_href(body)
        for href in extract_hrefs(body):
            target, _ = resolve_link(html_file, href, base_href)
            if not target:
                continue
            target = os.path.normpath(target)
            if os.path.isdir(target):
                target = os.path.normpath(os.path.join(target, "index.html"))
            elif not os.path.splitext(target)[1]:
                target = os.path.normpath(os.path.join(target, "index.html"))
            if target in html_set and target not in reachable:
                queue.append(target)
    ignored = {
        # PWA offline fallback: served by the service worker, unlinked by design
        os.path.normpath(os.path.join(BASE_DIR, "offline", "index.html")),
        # Custom 404: served by Vercel on miss, unlinked by design
        os.path.normpath(os.path.join(BASE_DIR, "404.html")),
        # 2026-07-20 (receipt 146, `146_FOUNDER_RULING_EXECUTE_2026_07_20.md`):
        # legacy homepage snapshot,
        # intentionally unlinked (K3)
        os.path.normpath(os.path.join(BASE_DIR, "index_legacy_2026_07_19.html")),
        # /home/ is a retained legacy body behind the permanent /home/ -> / redirect.
        os.path.normpath(os.path.join(BASE_DIR, "home", "index.html")),
        # Frozen discipline projections remain directly addressable and noindex,
        # but no longer participate in the current reader funnel.
        os.path.normpath(os.path.join(BASE_DIR, "ontology", "index.html")),
        os.path.normpath(os.path.join(BASE_DIR, "theology", "index.html")),
    }
    orphans = [
        os.path.relpath(full, BASE_DIR)
        for full in sorted(html_set - reachable - ignored)
    ]
    if orphans:
        for o in orphans:
            error(f"Not reachable from /: {o}")
    else:
        ok("All public pages reachable from /")
    return len(orphans) == 0

def check_required_assets():
    print("\n[4] Required asset presence")
    all_ok = True
    # Check xai.css exists
    xai = os.path.join(BASE_DIR, "assets", "css", "xai.css")
    if os.path.exists(xai):
        ok("assets/css/xai.css present")
    else:
        error("assets/css/xai.css missing")
        all_ok = False
    # Check theme.js exists
    theme = os.path.join(BASE_DIR, "assets", "js", "theme.js")
    if os.path.exists(theme):
        ok("assets/js/theme.js present")
    else:
        error("assets/js/theme.js missing")
        all_ok = False
    # Check source-note.css exists
    sn = os.path.join(BASE_DIR, "assets", "css", "source-note.css")
    if os.path.exists(sn):
        ok("assets/css/source-note.css present")
    else:
        error("assets/css/source-note.css missing")
        all_ok = False
    # Check dimensions.js exists
    dim = os.path.join(BASE_DIR, "dimensions", "dimensions.js")
    if os.path.exists(dim):
        ok("dimensions/dimensions.js present")
    else:
        error("dimensions/dimensions.js missing")
        all_ok = False

    # Deployed binary/visual assets must be real worktree objects, never Git
    # LFS pointer stubs. Keep this scan cheap and scoped to deployable assets.
    asset_extensions = {
        ".woff", ".woff2", ".ttf", ".otf",
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico",
    }
    lfs_prefix = b"version https://git-lfs.github.com/spec/v1"
    patterns = load_vercelignore_patterns() or []
    checked_assets = 0
    asset_failures = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [
            d for d in dirs
            if d not in {".git", ".vercel", ".next", "node_modules", "90_ARCHIVE", "_archive"}
        ]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in asset_extensions:
                continue
            path = os.path.join(root, filename)
            rel = os.path.relpath(path, BASE_DIR).replace(os.sep, "/")
            if is_vercel_ignored(rel, patterns):
                continue
            checked_assets += 1
            try:
                with open(path, "rb") as fh:
                    sample = fh.read(256)
            except OSError as exc:
                asset_failures.append(f"{rel}: unreadable ({exc})")
                continue
            if not sample:
                asset_failures.append(f"{rel}: empty deployed asset")
            elif sample.startswith(lfs_prefix):
                asset_failures.append(f"{rel}: Git LFS pointer, not asset bytes")

    if not checked_assets:
        error("no deployable font/icon/image assets found")
        all_ok = False
    elif asset_failures:
        for finding in asset_failures:
            error(finding)
        all_ok = False
    else:
        ok(f"{checked_assets} deployable font/icon/image assets are real worktree objects")
    return all_ok

def check_html_wellformedness():
    print("\n[5] HTML well-formedness")
    issues = []
    for html_file in get_public_html_files():
        body = read_file(html_file)
        if not body.strip().upper().startswith("<!DOCTYPE"):
            issues.append((html_file, "missing DOCTYPE"))
        if "<html" not in body.lower():
            issues.append((html_file, "missing <html> tag"))
        if "</html>" not in body.lower():
            issues.append((html_file, "missing </html> tag"))
        if "<head>" not in body.lower():
            issues.append((html_file, "missing <head> tag"))
        if "</head>" not in body.lower():
            issues.append((html_file, "missing </head> tag"))
        if "<body>" not in body.lower() and '<body ' not in body.lower():
            issues.append((html_file, "missing <body> tag"))
        if "</body>" not in body.lower():
            issues.append((html_file, "missing </body> tag"))
    if issues:
        for f, issue in issues:
            error(f"{f}: {issue}")
    else:
        ok("All pages have DOCTYPE, html, head, body tags")
    return len(issues) == 0

def check_tier_markers():
    print("\n[6] Evidence tier markers on doctrine pages")
    missing = []
    for html_file in get_public_html_files():
        # Skip utility pages that don't need tier markers
        if html_file in {"index.html", "app.html", "cascade.html", "sphere.html",
                         "lightcone.html", "infinite.html", "about/index.html",
                         "sources/index.html", "atlas/index.html",
                         "historical-boundary/index.html"}:
            continue
        body = read_file(html_file)
        # Check for at least one tier marker
        if not re.search(r'\[A\]|\[S\]|\[I\]|\[C\]|\[B\]|\[D\]', body):
            missing.append(html_file)
    if missing:
        for f in missing:
            warn(f"No evidence tier markers: {f}")
    else:
        ok("All doctrine pages have evidence tier markers")
    return True  # Warnings only

def check_operator_tier_hygiene():
    print("\n[7] Operators tier hygiene")
    legacy_marker = re.compile(
        r"\[(?:[ABCSID]*/)*(?:E|T)(?:/[ABCSIDET]*)?\]"
        r"|\[(?:E|T)\s+for"
        r"|[;,]\s+(?:E|T)\s+for"
    )
    offenders = []
    for html_file in get_public_html_files():
        if not html_file.startswith("operators/"):
            continue
        body = read_file(html_file)
        if legacy_marker.search(body):
            offenders.append(html_file)
    if offenders:
        for f in offenders:
            error(f"{f}: legacy operator tier marker escaped public normalization")
    else:
        ok("Operators route uses current [A/B/S/I/D/C] tier markers")
    return len(offenders) == 0

def check_public_reading_bundle():
    print("\n[8] Public reading bundle wiring")
    required_surfaces = [
        "read/index.html",
        "papers/index.html",
        "canon/index.html",
        "foundations/index.html",
        "operators/index.html",
        "will/index.html",
        "value/index.html",
        "ground/index.html",
        "sacred/index.html",
        "method/index.html",
        "meta/index.html",
        "reading-manifest.json",
    ]
    all_ok = True
    for rel in required_surfaces:
        if os.path.exists(os.path.join(BASE_DIR, rel)):
            ok(f"{rel} present")
        else:
            error(f"{rel} missing")
            all_ok = False

    manifest_path = os.path.join(BASE_DIR, "reading-manifest.json")
    if not os.path.exists(manifest_path):
        return False

    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except Exception as exc:
        error(f"reading-manifest.json is not valid JSON: {exc}")
        return False

    documents = manifest.get("documents", [])
    counts = {}
    for doc in documents:
        counts[doc.get("section")] = counts.get(doc.get("section"), 0) + 1
        href = doc.get("href", "")
        if not href:
            error(f"manifest document missing href: {doc}")
            all_ok = False
            continue
        target = os.path.join(BASE_DIR, href)
        if href.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            error(f"manifest target missing: {href}")
            all_ok = False

    expected = {
        "papers": 26,
        "canon": 8,
        "foundations": 12,
        "trinity": 42,
        "formal": 37,
        "paradox": 26,
        "memetic": 6,
        "rosettad": 38,
        "operators": 29,
        "will": 30,
        "value": 10,
        "ground": 9,
        "sacred": 6,
        "method": 12,
        "meta": 6,
    }
    registry = load_withheld_registry()
    withheld_manifest_hrefs = set()
    for item in registry["artifacts"]:
        manifest_doc = item.get("manifestDocument")
        if manifest_doc is None:
            continue
        expected[manifest_doc["section"]] -= 1
        withheld_manifest_hrefs.add(manifest_doc["href"])

    published_hrefs = {doc.get("href") for doc in documents}
    leaked_hrefs = sorted(withheld_manifest_hrefs & published_hrefs)
    if leaked_hrefs:
        for href in leaked_hrefs:
            error(f"withheld artifact remains in reading-manifest.json: {href}")
        all_ok = False
    else:
        ok("withheld artifacts are absent from reading-manifest.json")
    for section, expected_count in expected.items():
        actual = counts.get(section, 0)
        if actual == expected_count:
            ok(f"{section}: {actual} rendered docs")
        else:
            error(f"{section}: expected {expected_count} rendered docs, found {actual}")
            all_ok = False

    total_expected = sum(expected.values())
    if len(documents) == total_expected:
        ok(f"public corpus documents wired: {len(documents)}")
    else:
        error(f"expected {total_expected} public corpus documents, found {len(documents)}")
        all_ok = False

    index_body = read_file("index.html")
    # 2026-07-28: the public front is worldview-first with an immediate practice.
    # These are the declared current reader, evidence, participation, and exit
    # hubs; the frozen historical library is not a first-contact requirement.
    for href in [
        "practice/",
        "plainly/",
        "discoveries/",
        "record/",
        "lab/",
        "book/",
        "about/",
        "contribute/",
        "exit/",
    ]:
        if f'href="{href}"' in index_body:
            ok(f"landing links {href}")
        else:
            error(f"landing missing link to {href}")
            all_ok = False

    practice_body = read_file("practice/index.html")
    for marker in [
        'id="receipt-builder"',
        "Face 1 · commitment",
        "Face 2 · observed outcome",
        "no transmission",
        "comparative benefit over simpler decision practices remains open",
    ]:
        if marker not in practice_body:
            error(f"practice missing local-receipt boundary marker: {marker}")
            all_ok = False

    return all_ok

def check_generated_library_chrome():
    print("\n[9] Generated library chrome contract")
    manifest_path = os.path.join(BASE_DIR, "reading-manifest.json")
    if not os.path.exists(manifest_path):
        error("reading-manifest.json missing; cannot verify generated chrome")
        return False

    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except Exception as exc:
        error(f"reading-manifest.json is not valid JSON: {exc}")
        return False

    generated_pages = set()
    for href in manifest.get("routes", {}).values():
        if href.endswith("/"):
            generated_pages.add(os.path.normpath(os.path.join(href, "index.html")))
    for doc in manifest.get("documents", []):
        href = doc.get("href", "")
        if href.endswith("/"):
            generated_pages.add(os.path.normpath(os.path.join(href, "index.html")))

    required_markers = [
        '<main class="library-shell">',
        '<section class="library-hero">',
        '<div class="library-route-row">',
        '<article class="library-article">',
        '<aside class="library-meta">',
        "Generated by 12_PUBLIC_SITE/generate_public_library.py",
    ]
    drifted = []
    for rel in sorted(generated_pages):
        path = os.path.join(BASE_DIR, rel)
        if not os.path.exists(path):
            drifted.append((rel, "missing generated page"))
            continue
        body = read_file(rel)
        missing = [marker for marker in required_markers if marker not in body]
        if missing:
            drifted.append((rel, "missing " + ", ".join(missing)))

    if drifted:
        for rel, finding in drifted:
            error(f"{rel}: generated-library chrome drift ({finding})")
        return False

    ok(f"Generated library chrome present on {len(generated_pages)} pages")
    return True

def load_vercelignore_patterns():
    path = os.path.join(BASE_DIR, ".vercelignore")
    if not os.path.exists(path):
        return None
    patterns = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                patterns.append(stripped)
    return patterns

def vercelignore_matches(rel_path, pattern):
    rel_path = rel_path.replace(os.sep, "/")
    pattern = pattern.replace(os.sep, "/")
    if pattern.startswith("!"):
        return False
    anchored = pattern.startswith("/")
    if "[" in pattern or "]" in pattern:
        raise ValueError(
            f"unsupported character-class pattern in .vercelignore: {pattern!r}"
        )
    directory_only = pattern.endswith("/")
    if anchored:
        pattern = pattern[1:]
    if directory_only:
        pattern = pattern[:-1]
    if not pattern:
        raise ValueError("empty .vercelignore pattern is unsupported")

    regex = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "*":
            if index + 1 < len(pattern) and pattern[index + 1] == "*":
                while index + 1 < len(pattern) and pattern[index + 1] == "*":
                    index += 1
                if index + 1 < len(pattern) and pattern[index + 1] == "/":
                    regex.append(r"(?:[^/]+/)*")
                    index += 1
                else:
                    regex.append(r".*")
            else:
                regex.append(r"[^/]*")
        elif char == "?":
            regex.append(r"[^/]")
        else:
            regex.append(re.escape(char))
        index += 1
    expression = "".join(regex)
    candidate = rel_path.strip("/")
    parts = candidate.split("/") if candidate else []
    directory_parts = parts if rel_path.endswith("/") else parts[:-1]
    if directory_only:
        if not anchored and "/" not in pattern:
            return any(
                re.fullmatch(expression, part, flags=re.IGNORECASE) is not None
                for part in directory_parts
            )
        directory_prefixes = (
            "/".join(directory_parts[:index])
            for index in range(1, len(directory_parts) + 1)
        )
        return any(
            re.fullmatch(expression, prefix, flags=re.IGNORECASE) is not None
            for prefix in directory_prefixes
        )
    if "/" not in pattern and not anchored:
        return re.fullmatch(
            expression, parts[-1] if parts else "", flags=re.IGNORECASE
        ) is not None
    return re.fullmatch(expression, candidate, flags=re.IGNORECASE) is not None

def is_vercel_ignored(rel_path, patterns):
    rel_path = rel_path.replace(os.sep, "/").strip("/")
    cache = {}

    def is_kept(candidate, *, directory=False):
        cache_key = (candidate, directory)
        if cache_key in cache:
            return cache[cache_key]
        parts = candidate.split("/") if candidate else []
        if len(parts) > 1:
            parent = "/".join(parts[:-1])
            if not is_kept(parent, directory=True):
                cache[cache_key] = False
                return False
        ignored = False
        match_path = candidate + "/" if directory else candidate
        for pattern in patterns:
            negated = pattern.startswith("!")
            raw = pattern[1:] if negated else pattern
            if vercelignore_matches(match_path, raw):
                ignored = not negated
        cache[cache_key] = not ignored
        return not ignored

    return not is_kept(rel_path)


def header_source_covers(source, route):
    if source == route:
        return True
    if source.endswith("(.*)"):
        return route.startswith(source[:-4])
    return False


def normalize_index_route(value):
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if raw.startswith(("https://", "http://")):
        raw = urlparse(raw).path
    elif raw.startswith("/"):
        pass
    elif re.fullmatch(r"[A-Za-z0-9._~%+@/-]+", raw) and "/" in raw:
        raw = "/" + raw
    else:
        return None
    raw = raw.split("#", 1)[0].split("?", 1)[0]
    return raw or "/"


def routes_named_by_index_surface(rel_path):
    path = os.path.join(BASE_DIR, rel_path)
    body = read_file(rel_path)
    routes = set()
    if rel_path.endswith(".json"):
        data = json.loads(body)

        def visit(value):
            if isinstance(value, dict):
                for nested in value.values():
                    visit(nested)
            elif isinstance(value, list):
                for nested in value:
                    visit(nested)
            else:
                route = normalize_index_route(value)
                if route:
                    routes.add(route)

        visit(data)
        return routes

    if rel_path.endswith(".xml"):
        for location in re.findall(r"<loc>(.*?)</loc>", body, flags=re.IGNORECASE | re.DOTALL):
            route = normalize_index_route(location)
            if route:
                routes.add(route)
        return routes

    base_href = extract_base_href(body)
    for href in extract_hrefs(body):
        if href.startswith(("https://", "http://")):
            route = normalize_index_route(href)
            if route:
                routes.add(route)
            continue
        target, _ = resolve_link(rel_path, href, base_href)
        if target is None:
            continue
        try:
            rel = os.path.relpath(target, BASE_DIR).replace(os.sep, "/")
        except ValueError:
            continue
        if rel == "index.html":
            routes.add("/")
        elif rel.endswith("/index.html"):
            routes.add("/" + rel)
            routes.add("/" + rel[:-10])
        elif os.path.isdir(target) or href.split("#", 1)[0].endswith("/"):
            routes.add("/" + rel.rstrip("/") + "/")
        else:
            routes.add("/" + rel)
    return routes


def check_historical_public_boundary():
    print("\n[10] Historical public-withholding boundary")
    all_ok = True
    try:
        registry = load_withheld_registry()
    except Exception as exc:
        error(f"withheld-routes.json is not valid JSON: {exc}")
        return False

    exact_artifacts = {
        "app.html",
        "complete-ontology/index.html",
        "five-plus-one/index.html",
        "burrisphere/index.html",
        "dasein/index.html",
        "canon/the-complete-ontology-of-reality/index.html",
        "operators/mf-283-the-orthogonality-theorem-v2/index.html",
        "operators/mf-285-dreams-are-unanchored-d5/index.html",
        "operators/mf-296-gravity-is-time/index.html",
        "operators/mf-298-dark-matter-is-mutual-information/index.html",
    }
    entries = registry.get("artifacts", [])
    registered_artifacts = {item.get("artifact") for item in entries}
    if registered_artifacts != exact_artifacts:
        error(
            "withheld-routes.json artifact set drift: "
            f"expected {sorted(exact_artifacts)}, found {sorted(registered_artifacts)}"
        )
        all_ok = False
    else:
        ok("withholding registry names the exact ten historical artifacts")

    boundary = registry.get("boundary", {})
    boundary_artifact = boundary.get("artifactRoute", "")
    boundary_public_route = boundary.get("publicRoute", "")
    marker = boundary.get("marker", "")
    boundary_path = os.path.join(BASE_DIR, boundary_artifact)
    if not os.path.exists(boundary_path):
        error(f"historical boundary page missing: {boundary_artifact}")
        all_ok = False
    else:
        boundary_body = read_file(boundary_artifact)
        required_boundary_markers = [
            marker,
            'name="robots" content="noindex, noarchive, nosnippet, nofollow"',
            'http-equiv="Cache-Control" content="no-store, max-age=0"',
            "preserved, not published",
        ]
        missing_markers = [value for value in required_boundary_markers if not value or value not in boundary_body]
        if missing_markers:
            error(f"historical boundary page missing marker(s): {missing_markers}")
            all_ok = False
        else:
            ok("historical boundary page is explicit, noindex, and no-store")

    patterns = load_vercelignore_patterns() or []
    for item in entries:
        artifact = item.get("artifact", "")
        if not artifact or artifact.startswith("/") or ".." in artifact.split("/"):
            error(f"unsafe artifact path in withholding registry: {artifact!r}")
            all_ok = False
            continue
        path = os.path.join(BASE_DIR, artifact)
        if not os.path.isfile(path):
            error(f"withheld artifact missing from git worktree: {artifact}")
            all_ok = False
            continue
        with open(path, "rb") as fh:
            current_bytes = fh.read()
        actual_hash = hashlib.sha256(current_bytes).hexdigest()
        actual_size = len(current_bytes)
        if actual_hash != item.get("sha256") or actual_size != item.get("bytes"):
            error(
                f"withheld artifact custody drift: {artifact} "
                f"sha256={actual_hash} bytes={actual_size}"
            )
            all_ok = False

        git_path = f"12_PUBLIC_SITE/{artifact}"
        process = subprocess.run(
            ["git", "-C", REPO_DIR, "show", f"HEAD:{git_path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode:
            error(f"withheld artifact is not present at HEAD: {git_path}")
            all_ok = False
        else:
            head_hash = hashlib.sha256(process.stdout).hexdigest()
            if head_hash != actual_hash or len(process.stdout) != actual_size:
                error(f"withheld artifact differs from HEAD custody: {artifact}")
                all_ok = False

        if artifact not in patterns or not is_vercel_ignored(artifact, patterns):
            error(f".vercelignore lacks exact withheld artifact exclusion: {artifact}")
            all_ok = False

    if all_ok:
        ok("all ten artifact bytes match registered SHA-256, HEAD, and exact deploy exclusions")

    try:
        with open(os.path.join(BASE_DIR, "vercel.json"), "r", encoding="utf-8") as fh:
            vercel = json.load(fh)
    except Exception as exc:
        error(f"vercel.json is not valid JSON: {exc}")
        return False

    redirect_map = {
        rule.get("source"): rule
        for rule in vercel.get("redirects", [])
    }
    header_rules = vercel.get("headers", [])
    required_robots = {"noindex", "noarchive", "nosnippet"}
    all_public_routes = [boundary_public_route]
    for item in entries:
        all_public_routes.extend(item.get("publicRoutes", []))
        for route in item.get("publicRoutes", []):
            redirect = redirect_map.get(route, {})
            if redirect.get("destination") != boundary_public_route or redirect.get("permanent") is not False:
                error(f"withheld route lacks exact reversible boundary redirect: {route}")
                all_ok = False

    for route in all_public_routes:
        route_headers = {}
        for rule in header_rules:
            if header_source_covers(rule.get("source", ""), route):
                for header in rule.get("headers", []):
                    route_headers[header.get("key", "").lower()] = header.get("value", "")
        robots = {token.strip().lower() for token in route_headers.get("x-robots-tag", "").split(",")}
        cache_control = route_headers.get("cache-control", "").lower()
        cdn_cache_control = route_headers.get("cdn-cache-control", "").lower()
        if not required_robots.issubset(robots):
            error(f"withheld route lacks noindex/noarchive/nosnippet headers: {route}")
            all_ok = False
        if "no-store" not in cache_control or "no-store" not in cdn_cache_control:
            error(f"withheld route lacks browser/CDN no-store headers: {route}")
            all_ok = False

    index_surfaces = [
        "reading-manifest.json",
        "atlas/index.html",
        "atlas/site_index.json",
        "atlas/source-ledger.json",
        "sitemap.xml",
        "book/rag_index.json",
        "read/index.html",
        "canon/index.html",
        "operators/index.html",
    ]
    withheld_public_routes = {
        route
        for item in entries
        for route in item.get("publicRoutes", [])
    }
    for surface in index_surfaces:
        try:
            named_routes = routes_named_by_index_surface(surface)
        except Exception as exc:
            error(f"cannot inspect index/search surface {surface}: {exc}")
            all_ok = False
            continue
        leaked_routes = sorted(withheld_public_routes & named_routes)
        for route in leaked_routes:
            error(f"withheld route remains in current index/search surface: {surface} -> {route}")
            all_ok = False

    sitemap_body = read_file("sitemap.xml")
    if boundary_public_route in sitemap_body:
        error("noindex historical boundary must not be advertised in sitemap.xml")
        all_ok = False

    service_worker = read_file("sw.js")
    if "WITHHELD_ROUTES" not in service_worker or "isWithheldRoute" not in service_worker:
        error("service worker lacks the explicit withheld-route cache bypass")
        all_ok = False
    for route in sorted(set(all_public_routes)):
        if route not in service_worker:
            error(f"service worker withheld-route registry missing: {route}")
            all_ok = False

    if all_ok:
        ok("reversible redirects, headers, indexes, search, sitemap, and service-worker boundary agree")
    return all_ok

def check_publication_boundary():
    print("\n[11] Deployment publication boundary")
    patterns = load_vercelignore_patterns()
    if patterns is None:
        error(".vercelignore missing")
        return False

    required_patterns = {
        "book-pwa/",
        "90_ARCHIVE/",
        "_archive/",
        "_STAGING_COMPASS_RESTRUCTURE/",
        "docs/",
        "__pycache__/",
        "*.py",
        "*.sh",
        "*.md",
        ".env",
        ".env.*",
        "*.db",
        "*.tsbuildinfo",
    }
    missing = sorted(required_patterns - set(patterns))
    if missing:
        for pattern in missing:
            error(f".vercelignore missing required pattern: {pattern}")
        return False

    risky_paths = [
        "book-pwa/.env",
        "book-pwa/dev.db",
        "book-pwa/README.md",
        "docs/superpowers/README.md",
        "_STAGING_COMPASS_RESTRUCTURE/00_COMPASS_RESTRUCTURE_RECEIPT.md",
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md",
        "generate_public_library.py",
        "predeploy_check.py",
        "predeploy_check.sh",
        "audit_live_domain_against_manifest.py",
        "withheld-routes.json",
        "deploy.sh",
        "deploy_vercel.sh",
        "deploy_target_contract.py",
        "__pycache__/predeploy_check.cpython-311.pyc",
        "compass/_archive/index_2026_07_12_pre_restructure.html",
        "a/b/_archive/c.html",
    ]
    leaked = [rel for rel in risky_paths if not is_vercel_ignored(rel, patterns)]
    if leaked:
        for rel in leaked:
            error(f"publication boundary would not ignore: {rel}")
        return False

    safe_paths = [
        "_archiveish/index.html",
        "compass/_archiveish/index.html",
        "compass/archive/index.html",
        "_archive.html",
    ]
    overmatched = [rel for rel in safe_paths if is_vercel_ignored(rel, patterns)]
    if overmatched:
        for rel in overmatched:
            error(f"publication boundary overmatches safe path: {rel}")
        return False

    vercel_entry = read_file("deploy_vercel.sh")
    for marker in (
        ".vercel/project.json",
        "deploy_target_contract.py",
        "--vercel-link",
        "predeploy_check.py",
        "check_site_build_artifacts.py",
        "exec vercel --prod --yes",
    ):
        if marker not in vercel_entry:
            error(f"Vercel entrypoint lacks fail-closed marker: {marker}")
            return False
    target_contract = read_file("deploy_target_contract.py")
    for marker in (
        "EMERGENTISM_VERCEL_PROJECT_ID_PIN",
        "EMERGENTISM_VERCEL_ORG_ID_PIN",
        "hmac.compare_digest",
        "--self-test",
    ):
        if marker not in target_contract:
            error(f"Vercel target contract lacks explicit-pin marker: {marker}")
            return False

    fallback = read_file("deploy.sh")
    if "--delete-excluded" in fallback:
        error("fallback deploy still uses global excluded-file deletion")
        return False
    for marker in (
        ".emergentism-static-target-v1",
        "emergentism.org-static-target-v1",
        "emergentism-static-v1)/releases/",
        "mkdir '${RELEASE_PATH}'",
        'rsync "${RSYNC_ARGS[@]}" --',
        "--self-test",
        "No live symlink, domain, or DNS target was changed",
    ):
        if marker not in fallback:
            error(f"fallback deploy lacks versioned-target guard: {marker}")
            return False

    book_ai = read_file("assets/js/book-ai.js")
    for marker in (
        "key-free book",
        'fetch("/book/rag_index.json")',
        "textContent",
        "no external endpoint",
    ):
        if marker not in book_ai:
            error(f"current book retrieval lacks key-free marker: {marker}")
            return False
    for forbidden in (
        "localStorage",
        "x-api-key",
        "anthropic-dangerous-direct-browser-access",
        "headers.authorization",
        "fetch(c.url",
        'type: "password"',
        "Endpoint URL",
        '"Bearer "',
    ):
        if forbidden in book_ai:
            error(f"current book public asset still exposes browser credential flow: {forbidden}")
            return False

    for command, label in (
        (["bash", os.path.join(BASE_DIR, "deploy.sh"), "--self-test"], "fallback target contract"),
        (["bash", os.path.join(BASE_DIR, "deploy_vercel.sh"), "--self-test"], "Vercel target contract"),
    ):
        process = subprocess.run(
            command,
            cwd=BASE_DIR,
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if process.returncode:
            error((process.stdout + process.stderr).strip() or f"{label} self-test failed")
            return False

    ok(".vercelignore, key-free retrieval, and fail-closed deployment entrypoints agree")
    return True

def check_semantic_parity():
    print("\n[12] Dimension-first semantic parity")
    process = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "check_public_semantic_parity.py")],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    ok(process.stdout.strip())
    return True

def check_claim_card_contract():
    print("\n[13] Claim-card and lifecycle contract")
    commands = (
        [sys.executable, os.path.join(REPO_DIR, "09_TOOLS/02_COMPILERS/compile_claim_cards.py"), "--check"],
        [sys.executable, os.path.join(REPO_DIR, "09_TOOLS/01_SCRIPTS/check_barred_claims.py"), "--scope", "all"],
    )
    all_ok = True
    for command in commands:
        process = subprocess.run(command, cwd=REPO_DIR, text=True, capture_output=True, check=False)
        if process.returncode:
            all_ok = False
            for line in (process.stdout + process.stderr).strip().splitlines():
                error(line)
        else:
            ok(process.stdout.strip())
    return all_ok

def check_public_book_build():
    print("\n[14] Deterministic public-book build")
    process = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "build_book.py"), "--check"],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    ok(process.stdout.strip())
    return True

def check_reading_manifest_contract():
    print("\n[15] Reading-manifest lifecycle contract")
    process = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "refresh_reading_manifest.py"), "--check"],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    ok(process.stdout.strip())
    return True


def check_contact_limited_lifecycle():
    print("\n[16] Contact-limited public lifecycle closure")
    checker = os.path.join(
        REPO_DIR, "09_TOOLS", "01_SCRIPTS", "check_contact_limited.py"
    )
    process = subprocess.run(
        [sys.executable, "-B", checker],
        cwd=REPO_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    summary = process.stdout.strip().splitlines()
    ok(summary[0] if summary else "contact-limited lifecycle ratchet passed")
    return True

def main():
    print("=" * 60)
    print("Pre-deploy supply-chain gate — 12_PUBLIC_SITE")
    print("=" * 60)

    results = [
        check_external_refs(),
        check_internal_links(),
        check_orphans(),
        check_required_assets(),
        check_html_wellformedness(),
        check_tier_markers(),
        check_operator_tier_hygiene(),
        check_public_reading_bundle(),
        check_generated_library_chrome(),
        check_historical_public_boundary(),
        check_publication_boundary(),
        check_semantic_parity(),
        check_claim_card_contract(),
        check_public_book_build(),
        check_reading_manifest_contract(),
        check_contact_limited_lifecycle(),
    ]

    # `results` was built and never read: the exit decision used only the global ERRORS
    # list, so any check that returned False WITHOUT appending to ERRORS was silently
    # ignored and the deploy went green. Fold the returned verdicts into the same
    # condition. Only an explicit False counts, so a check that returns None (no explicit
    # return) is not treated as a failure it never claimed.
    failed = [i for i, r in enumerate(results) if r is False]

    print("\n" + "=" * 60)
    if ERRORS or failed:
        if failed and not ERRORS:
            print(
                f"FAIL: {len(failed)} check(s) returned False without recording an error "
                f"(indices {failed}). A check that fails silently is a deploy hole."
            )
        print(f"FAIL: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        sys.exit(1)
    elif WARNINGS:
        print(f"PASS with warnings: {len(WARNINGS)} warning(s)")
        sys.exit(0)
    else:
        print("PASS: all checks green")
        sys.exit(0)

if __name__ == "__main__":
    main()
