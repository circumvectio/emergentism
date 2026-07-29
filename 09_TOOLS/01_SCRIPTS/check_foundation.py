#!/usr/bin/env python3
"""Enforce foundation consistency across its four homes.

The foundation is stated in four places by design: K-5 owns R0, the Settled Canon
Registry routes it (KSC-28), docs 45-47 own the formal results, and
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

# Stratum assignments. Drift here is the failure this validator exists to catch:
# a selected item quietly presented as forced is the session's own named failure mode.
# Amended 2026-07-29: the bottom stratum is the declared BASE, not FORCED.
# G-0b exit Z: F1 is folded into PRESUPPOSED as a property of the P1 apparatus.
# It is NOT a selection — exit Z does not ratify sentence-implies-selection.
# A base may still be selected. Nothing is forced.
PRESUPPOSED = ["P1"]
BASE = ["B1", "B2", "B3"]
EMERGENT = ["emergent"]

# Fences that must never fall out of the foundation, with the homes that must carry them.
FENCES = [
    ("T1 is analytic and world-empty",
     [r"empty of world"],
     [PROJECTION, FORMAL_DOCS[0], RULING_RECEIPTS[2]]),
    ("admissibility is not existence / not plenitude",
     [r"never plenitude|admissibility, never existence|not plenitude"],
     [PROJECTION, RULING_RECEIPTS[2]]),
    ("uniqueness is declared policy, not theorem",
     [r"declared policy.{0,40}not (a )?theorem|policy, not theorem|remains \[s\] declared, not \[a\]|declared, not \[a\]"],
     [PROJECTION, FORMAL_DOCS[2], RULING_RECEIPTS[1]]),
    ("R0 is a refusal, never an axiom",
     [r"refusal, never an axiom|not an axiom"],
     [PROJECTION, K5, REGISTRY]),
    ("the line is the iota-invariant meridian, not a rejected rival",
     [r"meridian"],
     [PROJECTION, RULING_RECEIPTS[1]]),
    ("arithmetic is chart-local",
     [r"chart-local"],
     [PROJECTION, REGISTRY, RULING_RECEIPTS[1]]),
]


def norm(text: str) -> str:
    """Collapse whitespace and markdown emphasis so wording is compared, not layout.

    Underscores are NOT stripped: they carry filenames like 00_THE_FOUNDATION.md.
    """
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text).lower()


def strata_block(body: str) -> str:
    """Return the BASE/INHERITED/EMERGENT block.

    Anchored on the occurrence of 'base' that actually introduces B1.
    """
    for match in re.finditer(r"base — posited", body):
        block = body[match.start(): match.start() + 1600]
        if "b1" in block and "emergent" in block:
            return block
    return ""


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

    # --- the three strata agree between K-5 and the projection -------------
    for label, body in (("K-5", k5), ("00_THE_FOUNDATION.md", proj)):
        block = strata_block(body)
        if not block:
            errors.append(f"{label}: the BASE/INHERITED/EMERGENT strata block is missing")
            continue
        emg_at = block.find("emergent")
        if emg_at == -1:
            errors.append(f"{label}: strata block must run BASE then EMERGENT")
            continue
        base_seg, emg_seg = block[:emg_at], block[emg_at:]

        for sym in BASE:
            if sym.lower() not in base_seg:
                errors.append(f"{label}: {sym} is not listed under BASE")
        for sym in PRESUPPOSED:
            if sym.lower() not in body:
                errors.append(f"{label}: {sym} (the presupposed stratum) is not listed")
        # the sphere must now be EMERGENT, never BASE
        if "sphere" in base_seg or "ℂp¹" in base_seg:
            errors.append(f"{label}: the sphere appears in BASE — it is emergent (step 6)")
        if "ℤ" not in emg_seg and "z " not in emg_seg:
            errors.append(f"{label}: the emergent chain must begin at ℤ")

        # The failure this validator now exists for: the word FORCED returning to
        # the bottom stratum, or the false "exactly one identity" coming back.
        if "forced" in base_seg and not any(s in base_seg for s in ("nothing here is forced", "none is forced", "nothing forced")):
            errors.append(f"{label}: the BASE stratum must not be described as forced")
        if "exactly one identity" in block:
            errors.append(f"{label}: the false 'exactly one identity' claim has returned")

    # --- the refuted F2 must not survive in ANY home ------------------------
    # r180: the strata guard above scans only K-5 and the projection, so the
    # false "exactly one identity" sat unflagged in the registry while this
    # validator reported PASS. A PROXIMITY window does not work here — the
    # withdrawal note sits next to the very place a re-assertion would land,
    # and shields it. So the rule is exact: the phrase may appear in the
    # registry exactly once, and only inside the canonical quoted withdrawal.
    QUOTED = 'it read "a multiplicative structure has exactly one identity"'
    hits = registry.count("exactly one identity")
    if QUOTED not in registry:
        errors.append(
            "00_SETTLED_CANON_REGISTRY.md: the F2 withdrawal record is missing or altered. "
            "F2 is permanently refuted; its supersession must stay recorded verbatim"
        )
    if hits > 1:
        errors.append(
            f"00_SETTLED_CANON_REGISTRY.md: 'exactly one identity' appears {hits} times; "
            "exactly one (the withdrawal quote) is permitted — a live re-assertion has returned"
        )

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
        f"{len(PRESUPPOSED)+len(BASE)} strata symbols)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
