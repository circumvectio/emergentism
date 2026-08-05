#!/usr/bin/env python3
"""Enforce Foundation consistency across typed owners and current surfaces.

The contract spans nine core routing/type surfaces, seven formal documents,
and three dated ruling receipts. K-5 owns R0, the Settled Canon Registry routes
it (KSC-28), and 00_THE_FOUNDATION.md is a projection that states it whole.
Active source text and manifest-declared current public surfaces are additionally
scanned through the Titan/algebra type firewall. Dated receipts, staged books,
frozen public projections, and archives retain historical syntax outside this
claim. Projections drift; this validator makes current drift visible.

This checks the invariants that must agree across the named owners and the
negative type contract across the scoped source/current-public corpus.

    python3 09_TOOLS/01_SCRIPTS/check_foundation.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from foundation_type_firewall import line_number_for_offset, titan_arithmetic_matches

ROOT = Path(__file__).resolve().parents[2]

PROJECTION = Path("00_THE_FOUNDATION.md")
K5 = Path("00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md")
REGISTRY = Path("00_META/00_SETTLED_CANON_REGISTRY.md")
KERNEL = Path("00_THE_KERNEL_INDEX.md")
FORMULA_BLOCK = Path("05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md")
PRIMITIVES = Path("05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md")
D1_BOUNDARY = Path("05_COSMOLOGY/03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md")
TITAN_CANON = Path(
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/"
    "00_THE_TRANSCENDENTAL_TRINITY_CANON.md"
)
FORMAL_ORACLE = Path("09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean")
PUBLIC_PARITY_MANIFEST = Path("12_PUBLIC_SITE/public_semantic_parity.json")
RECORD_LEDGER = Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md")
ACTIVE_EXTRA_TYPE_SURFACES = (
    FORMAL_ORACLE,
    Path("12_PUBLIC_SITE/generate_public_library.py"),
    # The active K-7 owner lives inside the otherwise historical receipt lane.
    # Keep it in scope explicitly so the archive exclusion cannot hide live
    # Titan syntax at the record front door.
    RECORD_LEDGER,
)

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

REQUIRED_SURFACES = [
    PROJECTION,
    K5,
    REGISTRY,
    KERNEL,
    FORMULA_BLOCK,
    PRIMITIVES,
    D1_BOUNDARY,
    TITAN_CANON,
    FORMAL_ORACLE,
    *FORMAL_DOCS,
    *RULING_RECEIPTS,
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

TYPED_WITNESS_REQUIRED = [
    "algebrawitness := (g, ·, e, a, b)",
    "carrier(algebrawitness) := g",
    "nocoercion(titanframe, carrier(algebrawitness))",
    "arithmeticsignature(titanframe)=∅",
]

# The retired Titan infix (⊙ = • × ○) must never return to a current owner.
# Restored from reconstruction commit 1797138a, where this definition existed;
# it was lost in a subsequent merge (same class as the seven definitions
# restored at 172d5ca6 and presentations_block above). Restored verbatim so the
# gate can fail instead of dying on NameError — a gate that can neither pass nor
# fail is the defect live-gate integrity exists to catch.
RETIRED_TITAN_INFIX = re.compile(r"⊙\s*=\s*•\s*(?:×|\*)\s*○")

ACTIVE_SCAN_SUFFIXES = {".md", ".json", ".yaml", ".yml"}
ACTIVE_SCAN_EXCLUDED_PREFIXES = (
    Path("00_HANDOFF"),
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS"),
    Path("11_UPLINK/60_SESSION_PACKETS"),
    Path("12_PUBLIC_SITE"),
    Path("13_BOOKS"),
    Path("91_COMPATIBILITY"),
)


def norm(text: str) -> str:
    """Collapse whitespace and markdown emphasis so wording is compared, not layout.

    Underscores are NOT stripped: they carry filenames like 00_THE_FOUNDATION.md.
    """
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text).lower()


def active_foundation_scan_paths(root: Path) -> list[Path]:
    """Discover source-owner and declared-current public type surfaces."""

    paths: set[Path] = set()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in ACTIVE_SCAN_SUFFIXES:
            continue
        rel = path.relative_to(root)
        if "90_ARCHIVE" in rel.parts:
            continue
        if any(rel.is_relative_to(prefix) for prefix in ACTIVE_SCAN_EXCLUDED_PREFIXES):
            continue
        paths.add(rel)

    for rel in ACTIVE_EXTRA_TYPE_SURFACES:
        if (root / rel).is_file():
            paths.add(rel)

    manifest = root / PUBLIC_PARITY_MANIFEST
    if manifest.is_file():
        try:
            public_contract = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            public_contract = {}
        for declared in public_contract.get("currentSurfaces", []):
            if not isinstance(declared, str):
                continue
            rel = Path("12_PUBLIC_SITE") / declared
            if (root / rel).is_file():
                paths.add(rel)

    return sorted(paths, key=lambda item: item.as_posix())


def strata_block(body: str) -> str:
    """Return the BASE/INHERITED/EMERGENT block.

    Anchored on the occurrence of 'base' that actually introduces B1.
    """
    for match in re.finditer(r"base — posited", body):
        block = body[match.start(): match.start() + 1600]
        if "b1" in block and "emergent" in block:
            return block
    return ""


def presentations_block(body: str) -> str:
    """Return the two-presentation block from a normalized current owner.

    RESTORED 2026-08-06 from reconstruction commit 1797138a, where this
    definition existed; it was lost in a subsequent merge (same class as the
    seven definitions restored at 172d5ca6). Restored verbatim so the gate
    can fail instead of dying on NameError — a gate that can neither pass nor
    fail is the defect live-gate integrity exists to catch.
    """
    marker = "selected relational presentation"
    start = body.find(marker)
    if start == -1:
        return ""
    return body[start:start + 2200]


def main() -> int:
    errors: list[str] = []

    # --- every home exists -------------------------------------------------
    required = REQUIRED_SURFACES
    bodies: dict[Path, str] = {}
    for rel in required:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing foundation home: {rel.as_posix()}")
            continue
        bodies[rel] = path.read_text(encoding="utf-8")
    for rel in ACTIVE_EXTRA_TYPE_SURFACES:
        if not (ROOT / rel).is_file():
            errors.append(
                f"missing required active Foundation type surface: {rel.as_posix()}"
            )
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

    # --- TitanFrame and the algebra witness remain disjoint ---------------
    for label, body in ((PROJECTION.as_posix(), proj), (K5.as_posix(), k5)):
        for fragment in TYPED_WITNESS_REQUIRED:
            if fragment not in body:
                errors.append(f"{label}: typed witness boundary is missing {fragment!r}")

    active_scan_paths = active_foundation_scan_paths(ROOT)
    for rel in active_scan_paths:
        source_text = (ROOT / rel).read_text(encoding="utf-8")
        for pattern, offset in titan_arithmetic_matches(source_text):
            line_number = line_number_for_offset(source_text, offset)
            errors.append(
                f"{rel.as_posix()}:{line_number}: forbidden Titan arithmetic or "
                f"cross-type identification ({pattern})"
            )

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
        f"({len(required)} surfaces, {len(FENCES)} fences, "
        f"{len(PRESUPPOSED)+len(BASE)} strata symbols, "
        f"{len(active_scan_paths)} source/current-public surfaces type-scanned)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
