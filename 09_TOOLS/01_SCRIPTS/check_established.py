#!/usr/bin/env python3
"""Fail closed when the verification-state ledger overstates its checks.

This script performs source lint and bounded computational regression. It does
not compile the standalone Lean candidate file and does not prove universal
claims by finite enumeration. The ledger must say exactly that.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "00_ESTABLISHED" / "README.md"
LEAN = ROOT / "09_TOOLS" / "05_FORMAL_VERIFICATION" / "EmergentismCheck.lean"
BASE_CHECK = ROOT / "09_TOOLS" / "01_SCRIPTS" / "check_generative_base.py"

# Entries the manifest must keep listing as NOT established. Shortening this list
# without a verification landing is the manifest's own kill.
MUST_STAY_UNESTABLISHED = [
    "the μ-contract", "η = 0", "P = Φ × V", "Justice", "Power-Max",
    "Egregoreotype", "the Soul Loop", "the Crown Wager", "sphere primacy",
]

FORBIDDEN_INFLATIONS = [
    "Machine-proved — Lean 4",
    "Exhaustively computed",
    "clean axiom traces",
    "every listed entry stops holding",
]


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.exists():
        print("ESTABLISHED: FAIL\n- 00_ESTABLISHED/README.md is missing")
        return 1
    text = MANIFEST.read_text(encoding="utf-8")

    # --- A · Lean source artifact: lint only, never proof execution --------
    if not LEAN.exists():
        errors.append("the Lean file is missing")
    else:
        lean = LEAN.read_text(encoding="utf-8")
        n = len(re.findall(r"^theorem ", lean, re.M))
        claimed = re.search(r"\*\*(\d+) theorem\s+declarations\*\*", text)
        if not claimed:
            errors.append("the ledger does not state a Lean declaration count")
        elif int(claimed.group(1)) != n:
            errors.append(f"ledger claims {claimed.group(1)} Lean declarations; the file has {n}")
        # a real sorry, not the comment asserting there is none
        for m in re.finditer(r"\bsorry\b|\badmit\b", lean):
            line = lean[: m.start()].count("\n") + 1
            ctx = lean.splitlines()[line - 1]
            if not ctx.lstrip().startswith(("--", "/-", "*")) and "no `sorry`" not in ctx:
                errors.append(f"EmergentismCheck.lean:{line} contains a real sorry/admit")

    if "does not yet compile that file" not in text:
        errors.append("the ledger must disclose that this gate does not compile the Lean candidate")

    # --- B · bounded generative-base regression ----------------------------
    if not BASE_CHECK.exists():
        errors.append("check_generative_base.py is missing")
    else:
        r = subprocess.run([sys.executable, str(BASE_CHECK)], capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            errors.append(f"check_generative_base.py FAILED: {(r.stdout or r.stderr).strip()[:200]}")

    # --- every indexed G-claim must exist in the base document --------------
    base_doc = ROOT / "05_COSMOLOGY" / "03_FORMAL_SYSTEM" / "52_THE_GENERATIVE_BASE.md"
    if base_doc.exists():
        doc = base_doc.read_text(encoding="utf-8")
        for gid in re.findall(r"^\| `(G\d+[ab]?)` \|", text, re.M):
            if f"**{gid} ·" not in doc and f"**{gid}a ·" not in doc:
                errors.append(f"manifest lists {gid} but 52_THE_GENERATIVE_BASE.md does not state it")
    else:
        errors.append("52_THE_GENERATIVE_BASE.md is missing")

    if "G2` | **open general claim" not in text:
        errors.append("G2 must remain explicitly open pending a complete injectivity proof")
    for phrase in FORBIDDEN_INFLATIONS:
        if phrase in text:
            errors.append(f"verification inflation remains in ledger: {phrase!r}")

    # --- the ledger's own kill — exclusions may not shrink -----------------
    for item in MUST_STAY_UNESTABLISHED:
        if item not in text:
            errors.append(
                f"'{item}' was removed from the NOT-established list. "
                "Removing an entry requires a landed verification; otherwise this "
                "manifest has become a promotion path and its own kill has fired."
            )

    # --- the folder must own nothing ---------------------------------------
    if "holds no doctrine" not in text or "owns nothing" not in text.lower():
        errors.append("the manifest must state that it holds no doctrine and owns nothing")

    if errors:
        print("ESTABLISHED: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    n_lean = len(re.findall(r"^theorem ", LEAN.read_text(encoding="utf-8"), re.M))
    n_g = len(set(re.findall(r"^\| `(G\d+[ab]?)` \|", text, re.M)))
    print(
        f"ESTABLISHED LEDGER: PASS ({n_lean} Lean declarations linted, not compiled; "
        f"bounded base regression passed; {n_g} G-rows indexed; "
        f"{len(MUST_STAY_UNESTABLISHED)} guarded exclusions intact)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
