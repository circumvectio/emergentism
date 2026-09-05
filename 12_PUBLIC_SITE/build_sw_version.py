#!/usr/bin/env python3
"""Derive the service-worker cache name from the content it caches.

THE BUG THIS FIXES, FOUND BY TESTING RATHER THAN READING. sw.js carried

    const CACHE = 'emergentism-714ce56d26e0';

as a hand-written literal, and the runtime strategy is stale-while-revalidate. So:

  · the cache key never changed across deploys unless a human remembered to edit it;
  · `activate` only prunes old caches when sw.js itself changes, which it didn't;
  · SWR then serves the CACHED asset on a returning visitor's first post-deploy load.

Observed live: a freshly deployed atlas-drawer.js was served correctly by the server
(200, new content) while the page executed the previous version from cache. For a launch
that means every prior visitor's first impression is the old site.

THE FIX. Compute the cache name from a sha256 over the precached asset list and the
bytes of every local asset sw.js references. Any asset change ⇒ new cache name ⇒
`activate` prunes and the new bytes win on first load.

Usage:
  python3 -B build_sw_version.py           rewrite the constant if it is stale
  python3 -B build_sw_version.py --check   fail if it is stale (for the gate)
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SW = ROOT / "sw.js"
CONST = re.compile(r"const CACHE = '([^']+)';")

# Assets whose bytes must influence the cache name. Anything served to a browser and
# cached by the worker belongs here; misses only cost staleness, never correctness.
GLOBS = ("assets/js/*.js", "assets/css/*.css", "atlas/*.json", "*.webmanifest")
EXTRA = (
    "reading-manifest.json",
    "public_semantic_parity.json",
    "emergentism-design.v2.json",
    "living-map.json",
    "wisdom/atlas.json",
    "wisdom/atlas.jsonl",
    "wisdom/rag.jsonl",
    "frontier/v1/catalog.json",
    "book/rag_index.json",
)
REQUIRED_RUNTIME_JSON = {
    "living-map.json",
    "book/rag_index.json",
    "emergentism-design.v2.json",
    "wisdom/atlas.json",
    "wisdom/atlas.jsonl",
    "wisdom/rag.jsonl",
    "frontier/v1/catalog.json",
}

# HTML COUNTS TOO, and leaving it out was a real hole in the first version of this script.
# The worker runs stale-while-revalidate on navigations, so a page whose PROSE changed —
# the most common kind of change here — would have been served from cache to every
# returning visitor with no version bump. Only the declared current surfaces are
# fingerprinted: the frozen library is noindex and its churn should not invalidate the
# whole cache.
def current_surface_files(root: Path = ROOT) -> list[Path]:
    parity = root / "public_semantic_parity.json"
    if not parity.is_file():
        raise FileNotFoundError("public_semantic_parity.json is missing")
    try:
        cs = json.loads(parity.read_text(encoding="utf-8")).get("currentSurfaces", [])
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"public_semantic_parity.json is invalid: {exc}") from exc
    if not isinstance(cs, list) or not cs:
        raise ValueError("public_semantic_parity.json has no currentSurfaces list")
    files = [root / c for c in cs if isinstance(c, str) and c.endswith(".html")]
    missing = [p.relative_to(root).as_posix() for p in files if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"current surface is missing: {missing[0]}")
    return files


def fingerprint_files(root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    for glob in GLOBS:
        files.extend(sorted(root.glob(glob)))
    for rel in EXTRA:
        path = root / rel
        if not path.is_file():
            raise FileNotFoundError(f"fingerprinted runtime artifact is missing: {rel}")
        files.append(path)
    files.extend(current_surface_files(root))
    rels = {path.relative_to(root).as_posix() for path in files}
    missing_runtime = sorted(REQUIRED_RUNTIME_JSON - rels)
    if missing_runtime:
        raise ValueError(f"runtime JSON omitted from service-worker fingerprint: {missing_runtime[0]}")
    return sorted(set(files))


def fingerprint(root: Path = ROOT, sw_path: Path | None = None) -> tuple[str, int]:
    h = hashlib.sha256()
    files = fingerprint_files(root)
    # the precache list inside sw.js counts too — changing what is cached is a change
    active_sw = sw_path or (root / "sw.js")
    if not active_sw.is_file():
        raise FileNotFoundError("sw.js is missing")
    sw = active_sw.read_text(encoding="utf-8")
    h.update(CONST.sub("const CACHE = '';", sw).encode("utf-8"))
    for p in files:
        h.update(str(p.relative_to(root)).encode("utf-8"))
        h.update(p.read_bytes())
    return h.hexdigest()[:12], len(files)


def negative_controls() -> None:
    """Prove both runtime JSON artifacts actually move the cache fingerprint."""
    source_files = [SW, *fingerprint_files(ROOT)]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for source in source_files:
            target = root / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        baseline, _ = fingerprint(root)
        for rel in sorted(REQUIRED_RUNTIME_JSON):
            target = root / rel
            target.write_bytes(target.read_bytes() + b" ")
            changed, _ = fingerprint(root)
            if changed == baseline:
                raise ValueError(f"negative control escaped service-worker fingerprint: {rel}")
            target.write_bytes(target.read_bytes()[:-1])
            restored, _ = fingerprint(root)
            if restored != baseline:
                raise ValueError(f"negative control did not restore fingerprint: {rel}")


def main(argv: list[str]) -> int:
    if not SW.exists():
        print("SW VERSION: FAIL\n- sw.js is missing")
        return 1
    sw = SW.read_text(encoding="utf-8")
    m = CONST.search(sw)
    if not m:
        print("SW VERSION: FAIL\n- no `const CACHE = '...'` found in sw.js")
        return 1

    try:
        negative_controls()
        want, n = fingerprint()
    except (OSError, ValueError) as exc:
        print(f"SW VERSION: FAIL\n- {exc}")
        return 1
    have = m.group(1)
    expected = f"emergentism-{want}"

    if "--check" in argv:
        if have != expected:
            print("SW VERSION: FAIL")
            print(f"- cache name is '{have}' but the cached assets hash to '{expected}'.")
            print("  Returning visitors would get stale assets on their first load after")
            print("  deploy. Run: python3 -B build_sw_version.py")
            return 1
        print(f"SW VERSION: PASS ({have}, derived from {n} assets)")
        print("  scope: proves the cache key tracks asset content, so `activate` prunes on "
              "change. It does NOT prove the worker's strategy is right for every route.")
        return 0

    if have == expected:
        print(f"sw version: already current ({have}, {n} assets)")
        return 0
    SW.write_text(CONST.sub(f"const CACHE = '{expected}';", sw, count=1), encoding="utf-8")
    print(f"sw version: {have} -> {expected}  ({n} assets fingerprinted)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
