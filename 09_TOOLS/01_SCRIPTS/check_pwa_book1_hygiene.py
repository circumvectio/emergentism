#!/usr/bin/env python3
"""One-command hygiene for the PWA / Book I current-body loop.

Green here is stacked firewood. It is not a public edition, not deploy,
and not the Amrita.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKS = (
    [sys.executable, "-m", "unittest", "09_TOOLS.02_COMPILERS.test_manifesto_public_current_body"],
    [sys.executable, "-B", "09_TOOLS/02_COMPILERS/extract_manifesto_public_current_body.py", "--check"],
    [sys.executable, "-B", "09_TOOLS/01_SCRIPTS/scan_halahala_current.py"],
    [sys.executable, "-B", "09_TOOLS/01_SCRIPTS/check_q4_declarations.py"],
    [sys.executable, "-B", "12_PUBLIC_SITE/check_public_semantic_parity.py"],
)


def main() -> int:
    failed = 0
    for cmd in CHECKS:
        print("$", " ".join(cmd))
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            failed += 1
            print(f"FAIL {cmd[-1]} ({result.returncode})")
    if failed:
        print(f"HYGIENE: FAIL ({failed} check(s))")
        return 1
    print("HYGIENE: PASS — firewood stacked; Amrita not emerged; G10 unpaid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
