#!/usr/bin/env python3
"""Fail closed when application-era authority leaks into active Emergentism.

The scan is intentionally scoped to source owners, front doors, route cards,
and active tooling. Archives, compatibility stubs, public projection, session
packets, handoffs, and dated receipts are provenance rather than authority.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ROUTE_EXCLUDED_PARTS = {
    "90_ARCHIVE",
    "12_PUBLIC_SITE",
    "00_HANDOFF",
    "50_AUDITS_AND_EXECUTIONS",
}

CORPUS_EXCLUDED_PARTS = ROUTE_EXCLUDED_PARTS | {
    "91_COMPATIBILITY",
    "60_SESSION_PACKETS",
}

ACTIVE_TOP_LEVELS = {
    "00_CONTROL",
    "00_META",
    "01_TELEOLOGY",
    "02_EPISTEMOLOGY",
    "03_METHODOLOGY",
    "04_AXIOLOGY",
    "05_COSMOLOGY",
    "06_ONTOLOGY",
    "07_THEOLOGY",
    "08_FRAMEWORK_SUPPORT",
    "09_TOOLS",
    "10_SEED",
    "11_UPLINK",
}

TEXT_SUFFIXES = {".md", ".py", ".r", ".json", ".yaml", ".yml", ".toml"}

# Exact historical/forwarding surfaces permitted by the purity contract. They
# remain readable for provenance but cannot own current semantics.
PROVENANCE_EXCEPTIONS = {
    Path("08_FRAMEWORK_SUPPORT/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK_MOVED.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/COMPARATIVE/2026_06_05_FILENAME_REPAIR_RECEIPT.md"),
    Path("09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"),
    Path("09_TOOLS/02_COMPILERS/test_dimension_first_canon.py"),
}

LEGACY_ALIAS_EXCEPTIONS = {
    Path("05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_DOMAINS/D33_EGREGORES.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/AXIOM_PAPERS/AX5_THE_EGREGORE.md"),
}

# ASCII-alphanumeric boundaries are deliberate: Python's ``\b`` treats ``_``
# as a word character, which previously let tokens such as ``02_SKYZAI`` and
# ``PENDING_K2`` escape. Plural DAV/DAC forms are forbidden too.
FORBIDDEN = re.compile(
    r"(?i)(?<![A-Za-z0-9])(?:Skyzai|VMOSK(?:-A|_A)?|DAVs?|DACs?|PRISM|Agentz(?:-runtime)?|K2)(?![A-Za-z0-9])"
)

FRONT_DOORS = [
    "README.md",
    "AGENT_README.md",
    "00_THE_WELTANSCHAUUNG.md",
    "00_THE_KERNEL_INDEX.md",
    "00_META/README.md",
    "01_TELEOLOGY/README.md",
    "02_EPISTEMOLOGY/README.md",
    "03_METHODOLOGY/README.md",
    "04_AXIOLOGY/README.md",
    "05_COSMOLOGY/README.md",
    "06_ONTOLOGY/README.md",
    "07_THEOLOGY/README.md",
    "08_FRAMEWORK_SUPPORT/README.md",
    "09_TOOLS/README.md",
    "10_SEED/README.md",
    "11_UPLINK/README.md",
]

OWNERS = [
    "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md",
    "00_META/00_SETTLED_CANON_REGISTRY.md",
    "00_META/00_THE_COMPASS.md",
    "00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md",
    "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md",
    "05_COSMOLOGY/00_THE_BURRI_RULES.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/43_D2_FUNCTION_ATLAS_AND_CONFIGURATION.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/44_D3_QUANTUM_STATE_REGISTER.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/10_THE_SOUL_LOOP.md",
    "05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md",
    "05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md",
    "04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md",
    "06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md",
    "06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md",
    "06_ONTOLOGY/04_THE_CONJECTURES.md",
    "06_ONTOLOGY/06_THE_REVELATIONS.md",
    "06_ONTOLOGY/07_THE_DIMENSIONAL_REGISTER_AXIOMS.md",
]


def is_active_route(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        path.name in {"AGENTS.md", "CLAUDE.md"}
        and not any(part.startswith(".") for part in rel.parts)
        and not any(
        part in ROUTE_EXCLUDED_PARTS for part in rel.parts
        )
    )


def is_active_corpus_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if not rel.parts or rel.parts[0] not in ACTIVE_TOP_LEVELS:
        return False
    if any(part.startswith(".") for part in rel.parts):
        return False
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    if any(part in CORPUS_EXCLUDED_PARTS for part in rel.parts):
        return False
    if rel.parts[:2] == ("00_META", "registers"):
        return False
    if rel in PROVENANCE_EXCEPTIONS:
        return False
    return True


def scan_file(path: Path, *, allow_legacy_alias: bool = False) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing scoped file: {path.relative_to(ROOT)}"]
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = FORBIDDEN.search(line)
        if match:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_no}: forbidden authority token {match.group(0)!r}"
            )
        if "Egregorotype" in line and not allow_legacy_alias:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_no}: unmarked legacy spelling 'Egregorotype'"
            )
    return errors


def main() -> int:
    errors: list[str] = []
    scoped = [ROOT / p for p in FRONT_DOORS + OWNERS]
    scoped.extend(p for p in ROOT.rglob("*") if p.is_file() and is_active_route(p))
    scoped.extend(p for p in ROOT.rglob("*") if p.is_file() and is_active_corpus_file(p))

    seen: set[Path] = set()
    for path in scoped:
        path = path.resolve()
        if path in seen:
            continue
        seen.add(path)
        allow_alias = path.relative_to(ROOT) in LEGACY_ALIAS_EXCEPTIONS
        errors.extend(scan_file(path, allow_legacy_alias=allow_alias))

    # The historical Record is exempt from vocabulary scanning, but it must
    # state the current non-authority boundary prominently.
    record = ROOT / "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md"
    record_text = record.read_text(encoding="utf-8")
    required = (
        "Historical labels remain",
        "create no present work authority",
        "money and legal contracts",
    )
    for phrase in required:
        if phrase not in record_text:
            errors.append(f"record boundary missing phrase: {phrase!r}")

    if errors:
        print("EMERGENTISM PURITY: FAIL")
        for error in errors:
            print(error)
        return 1

    print(f"EMERGENTISM PURITY: PASS ({len(seen)} active files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
