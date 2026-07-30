#!/usr/bin/env python3
"""Run the site's generated-artifact checks so they cannot drift unnoticed.

Two artifacts in 12_PUBLIC_SITE are generated from manifests and would otherwise rot
silently:

  atlas/library_index.json   the 292-document frozen-library search index, built from
                             reading-manifest.json. Stale = search misses documents.
  sw.js's CACHE constant     derived from the bytes of every current surface and cached
                             asset. Stale = returning visitors get the previous site.

Both generators expose --check. gate.sh calls checkers with no arguments, so this wrapper
exists to pass it. Exits 0 only if both agree with the tree.
"""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "12_PUBLIC_SITE"
BUILDERS = ("build_library_index.py", "build_sw_version.py")


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
        print("  fix: cd 12_PUBLIC_SITE && python3 -B build_library_index.py && "
              "python3 -B build_sw_version.py")
        return 1
    print("SITE BUILD ARTIFACTS: PASS")
    for l in lines:
        print(f"  {l}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
