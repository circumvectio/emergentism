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
10. Deployment publication boundary excludes source/control/runtime files
11. Current public semantics match the dimension-first source contract

Exit 0 if all checks pass, 1 if any fail.
"""

import json
import fnmatch
import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORS = []
WARNINGS = []

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
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [
            d for d in dirs if d not in {"node_modules", "vendor", ".git", ".vercel", ".next",
                                          "90_ARCHIVE", "_archive", "_STAGING_COMPASS_RESTRUCTURE"}
        ]
        for f in filenames:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
                if not rel.startswith("partials/"):
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
        # 2026-07-20 (receipt 146): legacy homepage snapshot, intentionally unlinked (K3)
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
                         "sources/index.html", "atlas/index.html"}:
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
    # 2026-07-20 amendment (receipt 146; completion-plan step 5): the landing architecture is
    # now discovery-led and /read/-mediated. The gate verifies the declared funnel + doorways.
    # The 16-dir generated library grid is deliberately delinked from the landing per the
    # compressed-map doctrine (sitemap policy: published, crawlable, never first-contact);
    # its chrome is covered by check [9].
    for href in [
        "read/",
        "discoveries/",
        "fable/",
        "plainly/",
        "record/",
        "axioms/",
        "book/",
        "practice/",
        "build/",
        "map/",
    ]:
        if f'href="{href}"' in index_body:
            ok(f"landing links {href}")
        else:
            error(f"landing missing link to {href}")
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
    if pattern.endswith("/"):
        prefix = pattern.rstrip("/")
        return rel_path == prefix or rel_path.startswith(prefix + "/")
    if "/" not in pattern:
        return fnmatch.fnmatch(os.path.basename(rel_path), pattern) or fnmatch.fnmatch(rel_path, pattern)
    return fnmatch.fnmatch(rel_path, pattern.lstrip("/"))

def is_vercel_ignored(rel_path, patterns):
    ignored = False
    for pattern in patterns:
        negated = pattern.startswith("!")
        raw = pattern[1:] if negated else pattern
        if vercelignore_matches(rel_path, raw):
            ignored = not negated
    return ignored

def check_publication_boundary():
    print("\n[10] Deployment publication boundary")
    patterns = load_vercelignore_patterns()
    if patterns is None:
        error(".vercelignore missing")
        return False

    required_patterns = {
        "book-pwa/",
        "90_ARCHIVE/",
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
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md",
        "generate_public_library.py",
        "predeploy_check.py",
        "predeploy_check.sh",
        "audit_live_domain_against_manifest.py",
        "deploy.sh",
        "__pycache__/predeploy_check.cpython-311.pyc",
    ]
    leaked = [rel for rel in risky_paths if not is_vercel_ignored(rel, patterns)]
    if leaked:
        for rel in leaked:
            error(f"publication boundary would not ignore: {rel}")
        return False

    ok(".vercelignore excludes source/control/runtime files")
    return True

def check_semantic_parity():
    print("\n[11] Dimension-first semantic parity")
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
        check_publication_boundary(),
        check_semantic_parity(),
    ]

    print("\n" + "=" * 60)
    if ERRORS:
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
