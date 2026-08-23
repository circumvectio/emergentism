#!/usr/bin/env python3
"""Run the site's generated-artifact checks so they cannot drift unnoticed.

Seven artifact classes in 12_PUBLIC_SITE are generated from declared source
surfaces and would otherwise rot silently:

  questions/ and record/pqa-54/
                             the 54-question atlas and its null-state research
                             record, generated from the frozen PQA-54 contract.
  atlas/site_index.json      the current-surface search index. It DID go stale: two
                             declared current surfaces were absent, so searching for
                             the site's own flagship page returned nothing.
  atlas/library_index.json   the 292-document frozen-library search index, built from
                             reading-manifest.json. Stale = search misses documents.
  292 library pages          breadcrumb + prev/next, injected between markers from the
                             manifest order. Stale = a dangling `next`, which looks
                             exactly like a correct one.
  social-card metadata       derived from each served page's declared title and
                             description. Stale = shared previews no longer match pages.
  book/rag_index.json        current-reader and front-of-house retrieval passages, bound
                             to the current book source and output hashes.
  sw.js's CACHE constant     derived from the bytes of every current surface and cached
                             asset. Stale = returning visitors get the previous site.

All seven generators expose --check. gate.sh calls checkers with no arguments, so this wrapper
exists to pass it. Exits 0 only if all seven agree with the tree.
"""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "12_PUBLIC_SITE"
BUILDERS = (
    "build_question_atlas.py",
    "build_atlas_index.py",
    "build_library_index.py",
    "build_library_nav.py",
    "build_social_cards.py",
    "build_rag_index.py",
    "build_sw_version.py",
)


def main() -> int:
    failures, lines = [], []
    for b in BUILDERS:
        p = SITE / b
        if not p.exists():
            failures.append(f"{b} is missing — a generated artifact has no generator")
            continue
        r = subprocess.run([sys.executable, "-B", str(p), "--check"],
                           capture_output=True, text=True, cwd=SITE, timeout=180)
        out = (r.stdout or r.stderr).strip()
        if r.returncode != 0:
            failures.append(f"{b}:\n    " + out.replace("\n", "\n    "))
        else:
            lines.append(out.splitlines()[0] if out else f"{b}: ok")

    if failures:
        print("SITE BUILD ARTIFACTS: FAIL")
        for f in failures:
            print(f"- {f}")
        print("  fix: replay the documented 12_PUBLIC_SITE generator sequence, ending "
              "with build_sw_version.py")
        return 1
    print("SITE BUILD ARTIFACTS: PASS")
    for l in lines:
        print(f"  {l}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
