#!/usr/bin/env python3
"""Enforce the corrected typed foundation across current semantic owners.

K-5 owns R0, the Settled Canon Registry routes it (KSC-28), current formal docs
own their scoped results, and
00_THE_FOUNDATION.md is a projection that states it whole. Projections drift.
The claim register has a validator; the foundation did not.

This checks the invariants that must hold across all four, so that repair work
cannot silently desynchronise them.

    python3 09_TOOLS/01_SCRIPTS/check_foundation.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PROJECTION = Path("00_THE_FOUNDATION.md")
K5 = Path("00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md")
REGISTRY = Path("00_META/00_SETTLED_CANON_REGISTRY.md")
KERNEL = Path("00_THE_KERNEL_INDEX.md")

FORMAL_DOCS = [
    Path("05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/45_THE_TITAN_INVERSION_STRUCTURE.md"),
    Path("05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/46_THE_ADMISSIBILITY_OF_NOTHING.md"),
    Path("05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/47_THE_EMERGENCE_OF_FINITY.md"),
    Path("05_COSMOLOGY/03_FORMAL_SYSTEM/48_THE_BOUNDARY_CROSSINGS_AND_THE_MU_CRITERION.md"),
    Path("05_COSMOLOGY/03_FORMAL_SYSTEM/49_THE_LORENTZ_MOEBIUS_CORRESPONDENCE.md"),
    Path("05_COSMOLOGY/03_FORMAL_SYSTEM/50_BLOCK_UNIVERSE_PLURALITY_AND_THE_SURVIVAL_OF_CHOICE.md"),
    Path("05_COSMOLOGY/03_FORMAL_SYSTEM/51_CCC_AND_THE_PRE_ARTICULATE_BOUNDARY.md"),
    Path("05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md"),
    Path("05_COSMOLOGY/03_FORMAL_SYSTEM/47_FINITY_BOUNDARY_CALCULUS_SPEC.md"),
]

RULING_RECEIPTS = [
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS/174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md"),
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS/175_SPHERE_PRIMACY_RULING_EXECUTED_2026_07_29.md"),
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS/176_THE_FOUNDATION_SEATED_R0_ADOPTED_2026_07_29.md"),
]

# The R0 refusal must say the same thing wherever it is stated. Normalised
# fragments, so reflow and emphasis do not trip the check but meaning does.
R0_CORE = [
    "no necessary being",
    "refuses to treat existence as self-warranting",
    "grants existence no logical entitlement",
]

# The current contract compares two selected, non-substitutable presentations.
PRESUPPOSED = ["P1"]
RELATIONAL = ["R1", "R2", "R3"]
REACHABILITY = ["G0", "ℚ⁺", "S(x)=x+1", "ι(x)=1/x"]

# Fences that must never fall out of the foundation, with the homes that must carry them.
FENCES = [
    ("typed formal facts are world-empty",
     [r"empty of world"],
     [PROJECTION, FORMAL_DOCS[0]]),
    ("admissibility is not existence / not plenitude",
     [r"never plenitude|admissibility, never existence|not plenitude"],
     [PROJECTION, FORMAL_DOCS[1]]),
    ("uniqueness is declared policy, not theorem",
     [r"declared policy.{0,40}not (a )?theorem|policy, not theorem|remains \[s\] declared, not \[a\]|declared, not \[a\]"],
     [PROJECTION, FORMAL_DOCS[2]]),
    ("R0 is a refusal, never an axiom",
     [r"refusal, never an axiom|not an axiom"],
     [PROJECTION, K5, REGISTRY]),
    ("the line is the iota-invariant meridian, not a rejected rival",
     [r"meridian"],
     [PROJECTION, FORMAL_DOCS[0]]),
    ("arithmetic is chart-local",
     [r"chart-local"],
     [PROJECTION, REGISTRY, FORMAL_DOCS[0]]),
]

RETIRED_TITAN_INFIX = re.compile(r"⊙\s*=\s*•\s*(?:×|\*)\s*○")


def norm(text: str) -> str:
    """Collapse whitespace and markdown emphasis so wording is compared, not layout.

    Underscores are NOT stripped: they carry filenames like 00_THE_FOUNDATION.md.
    """
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text).lower()


def presentations_block(body: str) -> str:
    """Return the two-presentation block from a normalized current owner."""
    marker = "selected relational presentation"
    start = body.find(marker)
    if start == -1:
        return ""
    return body[start:start + 2200]


def main() -> int:
    errors: list[str] = []

    # --- every home exists -------------------------------------------------
    required = [PROJECTION, K5, REGISTRY, KERNEL] + FORMAL_DOCS + RULING_RECEIPTS
    bodies: dict[Path, str] = {}
    for rel in required:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing foundation home: {rel.as_posix()}")
            continue
        bodies[rel] = path.read_text(encoding="utf-8")
    if errors:
        print("FOUNDATION CONTRACT: FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1

    proj, k5, registry, kernel = (norm(bodies[p]) for p in (PROJECTION, K5, REGISTRY, KERNEL))

    # --- R0 says the same thing in K-5 and the projection ------------------
    for fragment in R0_CORE:
        for label, body in (("K-5", k5), ("00_THE_FOUNDATION.md", proj)):
            if fragment not in body:
                errors.append(f"R0 drift: {label} is missing the core clause {fragment!r}")

    # --- R0 is seated as prior, not as a sixth refusal ---------------------
    if "not a sixth refusal" not in k5:
        errors.append("K-5 must state that R0 is not a sixth refusal (the 5+1 name is unchanged)")
    if "prior to the five" not in k5:
        errors.append("K-5 must state that R0 is prior to the five refusals")

    # --- the two selected presentations agree between K-5 and projection ---
    for label, body in (("K-5", k5), ("00_THE_FOUNDATION.md", proj)):
        block = presentations_block(body)
        if not block:
            errors.append(f"{label}: the two-presentation block is missing")
            continue
        for sym in RELATIONAL:
            if norm(sym) not in block:
                errors.append(f"{label}: {sym} is not listed under the relational presentation")
        for sym in REACHABILITY:
            if norm(sym) not in block:
                errors.append(f"{label}: {sym} is not listed under the reachability presentation")
        for sym in PRESUPPOSED:
            if sym.lower() not in body:
                errors.append(f"{label}: {sym} (the presupposed stratum) is not listed")
        if "not a derivation" not in block and "not equivalent" not in block:
            errors.append(f"{label}: the two presentations must be explicitly non-substitutable")
        if "exactly one identity" in block:
            errors.append(f"{label}: the false 'exactly one identity' claim has returned")

    # --- conditional identity theorem and non-operand frame stay explicit ---
    if "if present, is unique" not in registry and "if present, is unique" not in proj:
        errors.append("the corrected conditional identity-uniqueness theorem is missing")
    current_semantic = [PROJECTION, K5, REGISTRY, FORMAL_DOCS[0], FORMAL_DOCS[2], FORMAL_DOCS[-1]]
    for rel in current_semantic:
        for lineno, line in enumerate(bodies[rel].splitlines(), 1):
            if RETIRED_TITAN_INFIX.search(line):
                errors.append(f"{rel.as_posix()}:{lineno}: retired Titan infix returned to a current owner")

    # --- KSC-28 routes the foundation --------------------------------------
    if "ksc-28" not in registry:
        errors.append("Settled Canon Registry is missing the KSC-28 foundation row")

    # --- the projection is discoverable and declares itself non-owning -----
    if PROJECTION.name.lower() not in kernel:
        errors.append("Kernel Index does not route to 00_THE_FOUNDATION.md")
    if "eighth" not in proj:
        errors.append("00_THE_FOUNDATION.md must disclaim being an eighth kernel surface")

    # --- fences present in every home that must carry them ------------------
    for name, patterns, homes in FENCES:
        for home in homes:
            body = norm(bodies[home])
            if not any(re.search(p, body) for p in patterns):
                errors.append(f"fence lost — {name!r} absent from {home.as_posix()}")

    if errors:
        print("FOUNDATION CONTRACT: FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1

    print(
        f"FOUNDATION CONTRACT: PASS "
        f"({len(required)} homes, {len(FENCES)} fences, "
        f"{len(PRESUPPOSED)+len(RELATIONAL)+len(REACHABILITY)} typed symbols)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
