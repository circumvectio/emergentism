#!/usr/bin/env python3
"""Fail closed when the verification-state ledger overstates its checks.

This script performs source lint and bounded computational regression. It does
not compile the standalone Lean candidate file and does not prove universal
claims by finite enumeration. The ledger must say exactly that.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "00_ESTABLISHED" / "README.md"
LEAN = ROOT / "09_TOOLS" / "05_FORMAL_VERIFICATION" / "EmergentismCheck.lean"
BASE_CHECK = ROOT / "09_TOOLS" / "01_SCRIPTS" / "check_generative_base.py"

# Phrases the manifest may NOT contain, because each would claim more than this
# script actually performs.
#
# RESTORED 2026-08-05 (this comment previously mis-dated it 2026-08-01). The loop at the bottom of main() iterated FORBIDDEN_INFLATIONS
# while nothing defined it, so every run of this checker died on NameError. A checker
# that raises cannot pass and cannot fail — it aborts, blocks the gate, and reports
# nothing about the property it exists to guard. That is strictly worse than the
# inflation it was meant to catch.
#
# The two limits below are this file's own docstring, turned into tests. The docstring
# says the script "does not compile the standalone Lean candidate file and does not
# prove universal claims by finite enumeration. The ledger must say exactly that."
FORBIDDEN_INFLATIONS = [
    # (1) the Lean candidate is LINTED, never built — there is no toolchain here
    "compiles cleanly",
    "compiled and checked",
    "builds cleanly",
    "the proofs compile",
    "all proofs checked on every commit",
    # (2) bounded enumeration is evidence for a bound, never a universal proof
    "proved for all",
    "proven for all",
    "holds for all words",
    "exhaustively proved",
    "verified exhaustively",
    # (3) the tier vocabulary itself — publication is not verification
    "independently verified",
    "externally validated",
    # (4) P2.2 mutation-test 2026-08-06: the allowlist drifted the day it
    # was written; an inflation in different wording of the same form
    # ("fully machine verified", "complete proof is given above") was
    # accepted as PASS. Adding the missed phrases is the minimum fix; a
    # semantic classifier (verification-claim + hedge pattern) is the
    # proper fix and is staged [D] for K2.
    "fully machine verified",
    "complete proof is given above",
]

# Entries the manifest must keep listing as NOT established. Shortening this list
# without a verification landing is the manifest's own kill.
MUST_STAY_UNESTABLISHED = [
    "the μ-contract", "η = 0", "P_node := min(Φ̂₄,V₄)", "Justice", "Power-Max",
    "the Soul Loop", "the Crown Wager", "sphere primacy",
]


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.exists():
        print("ESTABLISHED: FAIL\n- 00_ESTABLISHED/README.md is missing")
        return 1
    text = MANIFEST.read_text(encoding="utf-8")

    # --- A · the Lean file -------------------------------------------------
    # r183 (`183_THE_MANIFEST_AUDITED_ITSELF_AND_FAILED_2026_07_29.md`): THIS
    # BLOCK USED TO COUNT "^theorem " AND GREP FOR sorry, AND NOTHING
    # ELSE. A Lean file whose every theorem statement was replaced with a FALSE
    # one would have passed, provided the count stayed at 20. And the corpus's
    # copy had no lakefile or toolchain, so it could not be built at all.
    #
    # The rule now: THE CHECKER MAY NOT REPORT PASS WHEN IT CANNOT VERIFY.
    # If the toolchain is absent it says UNVERIFIED and exits non-zero.
    lakefile = LEAN.parent / "lakefile.toml"
    toolchain = LEAN.parent / "lean-toolchain"
    if not lakefile.exists() or not toolchain.exists():
        errors.append(
            "the Lean project is not buildable — lakefile.toml or lean-toolchain is "
            "missing, so no oracle can be run and no claim here is verified"
        )
    if shutil.which("lake") is None:
        errors.append(
            "UNVERIFIED: `lake` is not on PATH, so the Lean theorems could not be "
            "re-checked. This checker does not pass what it cannot verify — install "
            "the toolchain or run with EMERGENTISM_SKIP_LEAN=1 to acknowledge the gap"
        )

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

    import os
    if os.environ.get("EMERGENTISM_SKIP_LEAN") == "1":
        errors = [e for e in errors if not e.startswith("UNVERIFIED:")]
        print("ESTABLISHED: NOTE — Lean re-check SKIPPED by EMERGENTISM_SKIP_LEAN=1")

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
    # r183 (`183_THE_MANIFEST_AUDITED_ITSELF_AND_FAILED_2026_07_29.md`) · THE
    # SCOPE OF THIS PASS, PRINTED SO IT CANNOT BE OVER-READ.
    # The Lean half is verified STRUCTURALLY here: project files present, toolchain
    # available, theorem count matches, no sorry. THE PROOFS ARE NOT RE-RUN — a full
    # `lake build` requires fetching mathlib (GB-scale) and cannot live in a validator.
    # The proofs WERE run, once, and the receipt records the output.
    print(
        "  scope: Lean half verified STRUCTURALLY (files, toolchain, count, no sorry). "
        "Proofs NOT re-run here — see receipt 182 (`182_C_HAT_IS_NOT_A_RING_MACHINE_CHECKED_2026_07_29.md`) "
        "for the build. "
        "The base half IS re-run."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
