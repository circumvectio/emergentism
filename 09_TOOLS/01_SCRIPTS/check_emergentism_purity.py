#!/usr/bin/env python3
"""Fail closed when application-era authority leaks into active Emergentism.

The scan is intentionally scoped to source owners, front doors, route cards,
and active tooling. Archives, compatibility stubs, public projection, session
packets, handoffs, and dated receipts are provenance rather than authority.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ROUTE_EXCLUDED_PARTS = {
    "90_ARCHIVE",
    "91_COMPATIBILITY",
    "12_PUBLIC_SITE",
    "00_HANDOFF",
    "50_AUDITS_AND_EXECUTIONS",
}

CORPUS_EXCLUDED_PARTS = ROUTE_EXCLUDED_PARTS | {
    "91_COMPATIBILITY",
    "60_SESSION_PACKETS",
}

ACTIVE_TOP_LEVELS = {
    # 2026-08-01: 00_ESTABLISHED, 00_WORK_IN_PROGRESS and 13_BOOKS were ACTIVE lanes sitting
    # outside this checker's scope. 00_ESTABLISHED is the corpus's short list of what
    # survives an outside check — arguably the document that most needs the gate — and it
    # was carrying both a literal product form and a bare eta, invisible to every checker.
    # 00_HANDOFF stays excluded: it is dated provenance, like the receipt lanes.
    "00_CONTROL",
    "00_ESTABLISHED",
    "00_WORK_IN_PROGRESS",
    "13_BOOKS",
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

RECEIPT_CITATION_LANES = (
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS"),
    Path("11_UPLINK/60_SESSION_PACKETS"),
)

# Derived custody surfaces repeat source semantic units and exact historical
# filenames by design. Their dedicated checker and digest receipt own that
# copied content; scanning the copy as fresh doctrine would both double count
# and misread identity strings as authority assertions.
DERIVED_CUSTODY_SURFACES = {
    Path("00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json"),
}

# Exact historical/forwarding surfaces permitted by the purity contract. They
# remain readable for provenance but cannot own current semantics.
PROVENANCE_EXCEPTIONS = {
    Path("08_FRAMEWORK_SUPPORT/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK_MOVED.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/COMPARATIVE/2026_06_05_FILENAME_REPAIR_RECEIPT.md"),
    Path("09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"),
    Path("09_TOOLS/01_SCRIPTS/lint_rule_tokens.py"),
    Path("09_TOOLS/02_COMPILERS/test_dimension_first_canon.py"),
}

# These files are live deployment projections of the Rosetta work grammar, not
# worldview premises or semantic owners. Keep the exception narrow and require
# an explicit boundary contract below; do not turn this into a token allowlist.
PROJECTION_EXCEPTION_PREFIXES = {
    Path("08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS"),
}

# Four canonical cards must name their immutable external source paths. The
# exception applies only to a structured source record that simultaneously
# declares legacy/frozen lifecycle and historical-lineage role; it does not permit
# the external name in claims, instructions, owners, or reader language.
HISTORICAL_LINEAGE_CARD_PATHS = {
    Path("00_META/claim_cards/self_eating_serpent.yaml"),
    Path("00_META/claim_cards/reciprocal_infinite_play.yaml"),
    Path("00_META/claim_cards/sarpasya_vijayam.yaml"),
    Path("00_META/claim_cards/six_lenses.yaml"),
}

# EXTERNAL-MAPPING AUDITS. Added 2026-08-01.
#
# Some corpus documents exist precisely to AUDIT a claimed correspondence between this
# framework and an external product or venture system. To do that they must quote the
# external system's own words — and quoting a claim in order to refute it is the opposite
# of importing it as authority. 31_CELL_SOUL4_TO_GEN7 is the clear case: it quotes an
# external mapping and concludes "They are not independent", killing a convergence claim.
# Genericising those names would destroy the audit, because you cannot show that two
# mappings are a definitional readback of each other without naming both.
#
# THE EXEMPTION IS EARNED, NOT GRANTED. A listed file must itself carry the same boundary
# declaration this checker already demands of projection directories. If the declaration is
# missing the file FAILS — louder than before, because a silent exemption is worse than a
# violation. This is deliberately per-file rather than per-directory: a directory-wide pass
# would let a genuinely authority-importing document hide beside a legitimate audit.
EXTERNAL_MAPPING_AUDIT_PATHS = {
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/30_ROSETTA_VNEXT_REFINEMENT_2026_07_31.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/31_CELL_SOUL4_TO_GEN7_2026_07_31.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/32_PACK_SOUL4_v0.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/32_PACK_ECO7_CANDIDATE_2026_07_31.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/33_LIVE_DRIFT_RECONCILIATION_v0.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/34_COUNTER_ROSETTA_LIBRARY_v0.md"),
}

# The exact phrases a listed file must carry to keep its exemption. Same three the
# projection-directory boundary already requires, so there is one rule, not two.
EXTERNAL_MAPPING_BOUNDARY_PHRASES = (
    "runtime projection, not worldview doctrine",
    "creates no semantic authority",
    "source owners remain upstream",
)

# Structured records whose source-path values necessarily name an external tree.
EXTERNAL_SOURCE_PATH_FILES = {
    Path("13_BOOKS/book-manifest.json"),
    Path("13_BOOKS/self_eating_serpent/CRITICAL_EDITION_1.md"),
    Path("13_BOOKS/self_eating_serpent/DEBRIEF.md"),
}

LEGACY_ALIAS_EXCEPTIONS = {
    Path("05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_DOMAINS/D33_EGREGORES.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/AXIOM_PAPERS/AX5_THE_EGREGORE.md"),
}

# The root work-programme projection must be nameable without re-importing the
# retired application authority that originally used the same framework label.
# The exception is deliberately exact: only the projection file itself and
# non-semantic references to that exact filename may carry the label. All other
# forbidden tokens, including external governance names, remain scanned.
CONTROL_PROJECTION_PATHS = (
    Path("VMOSK_A.md"),
    Path("VMOSK_A_v2_2026_07_31.md"),
)
CONTROL_PROJECTION_REFERENCE_PATHS = {Path("README.md"), Path("AGENTS.md")}

# ASCII-alphanumeric boundaries are deliberate: Python's ``\b`` treats ``_``
# as a word character, which previously let tokens such as ``02_SKYZAI`` and
# ``PENDING_K2`` escape. Plural DAV/DAC forms are forbidden too.
FORBIDDEN = re.compile(
    r"(?i)(?<![A-Za-z0-9])(?:Skyzai|VMOSK(?:-A|_A)?|DAVs?|DACs?|PRISM|Agentz(?:-runtime)?|K2)(?![A-Za-z0-9])"
)

# These are not forbidden words in all contexts; they are exact inflationary
# claims from the retired agent-activation island. Their historical bodies are
# allowed only in archive. Active forwarding tombstones may name the subject
# but must not restore these assertions.
FORBIDDEN_APPLICATION_CLAIMS = re.compile(
    r"(?i)(?:The Great Work is complete|AI charioteer has veto|"
    r"contains everything needed for an ASI to|All proofs checked on every commit|"
    r"Burri Sphere\s*\|\s*80%|Seven Axioms stand as mathematical necessities)"
)

APPLICATION_TOMBSTONES = {
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/00_CANONICAL_CORPUS.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/03_PRACTICE_TRANSLATION_MATRIX.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/04_DISSOLUTION_FORMAL_VERIFICATION.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/05_SEPARATION_OPERATOR_PROTOCOLS.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/06_COAGULATION_ACTIVATION_PACKAGE.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_07_DISCOVERY_OF_FINITY.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_09_THE_SOUL_LOOP.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_15_THE_TRINITY.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_INDEX.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/OP_384_FUNCTION_TESTING.md"),
}

REQUIRED_READER_SURFACES = {
    Path("00_THE_WELTANSCHAUUNG_ONE_SITTING.md"),
    Path("01_TELEOLOGY/04_THE_LIVED_COMPASS.md"),
    Path("06_ONTOLOGY/08_THE_HUMAN_CONDITION.md"),
}

LIVED_TOMBSTONES = {
    Path("05_COSMOLOGY/00_THE_TORUS_REVELATION.md"),
    Path("06_ONTOLOGY/00_THE_RING_THAT_IS_THE_GROUND.md"),
}

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
    "00_META/00_THE_GRAND_PUZZLE_ASSEMBLY_LEDGER.md",
    "00_META/00_KNOWN_UNKNOWNS_PROGRAM.md",
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
    "05_COSMOLOGY/03_FORMAL_SYSTEM/45_SATURATION_CONTRAST_AND_APERTURE_BOUNDARY.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/10_THE_SOUL_LOOP.md",
    "05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md",
    "05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md",
    "04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md",
    "06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md",
    "06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md",
    "06_ONTOLOGY/04_THE_CONJECTURES.md",
    "06_ONTOLOGY/06_THE_REVELATIONS.md",
    "06_ONTOLOGY/07_THE_DIMENSIONAL_REGISTER_AXIOMS.md",
    "03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md",
    "03_METHODOLOGY/00_EXTERNAL_COMPONENT_CALIBRATION_2026_07_20.md",
]


def is_active_route(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        path.name in {"AGENTS.md", "CLAUDE.md"}
        and not any(part.startswith(".") for part in rel.parts)
        and not any(rel.is_relative_to(prefix) for prefix in PROJECTION_EXCEPTION_PREFIXES)
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
    if rel in DERIVED_CUSTODY_SURFACES:
        return False
    if rel in PROVENANCE_EXCEPTIONS:
        return False
    if any(rel.is_relative_to(prefix) for prefix in PROJECTION_EXCEPTION_PREFIXES):
        return False
    return True


def physical_receipt_target_names(root: Path) -> tuple[str, ...]:
    names: set[str] = set()
    for lane in RECEIPT_CITATION_LANES:
        base = root / lane
        if not base.is_dir():
            continue
        for target in base.rglob("*.md"):
            match = re.match(r"^(\d{2,3})[_A-Za-z]", target.name)
            if match and match.group(1) != "00":
                names.add(target.name)
    return tuple(sorted(names, key=lambda value: (-len(value), value)))


def _complete_filename_token(text: str, start: int, end: int) -> bool:
    before = text[start - 1] if start else ""
    after = text[end] if end < len(text) else ""
    before_continues = before.isalnum() or before in "_.-"
    after_continues = after.isalnum() or after in "_-/"
    if after == ".":
        following = text[end + 1] if end + 1 < len(text) else ""
        after_continues = following.isalnum() or following in "_.-"
    return not before_continues and not after_continues


def forbidden_match_is_exact_receipt_target(
    line: str,
    match: re.Match[str],
    target_names: tuple[str, ...],
) -> bool:
    for name in target_names:
        start = 0
        while True:
            position = line.find(name, start)
            if position < 0:
                break
            end = position + len(name)
            start = end
            if (
                position <= match.start() < match.end() <= end
                and _complete_filename_token(line, position, end)
            ):
                return True
    return False


def scan_file(
    path: Path,
    *,
    allow_legacy_alias: bool = False,
    receipt_target_names: tuple[str, ...] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing scoped file: {path.relative_to(ROOT)}"]
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    if receipt_target_names is None:
        receipt_target_names = physical_receipt_target_names(ROOT)

    # An external-mapping audit keeps its exemption only while it carries the boundary.
    # Checked ONCE per file, before any line is scanned, so a file that has quietly lost
    # its declaration fails immediately rather than scanning clean on an exemption it no
    # longer earns.
    # A relative PATH to an immutable external source is not an authority claim. The
    # checker already grants this to four claim cards; the book records need the same, and
    # for the same reason: you cannot cite a historical edition without naming where it is.
    # Deliberately narrow — the token is permitted only on a line that is a source-path
    # declaration, never in prose, instructions, owners or reader language.
    def _is_external_source_path(line: str) -> bool:
        stripped = line.strip().strip(",")
        keyed = any(
            stripped.startswith(k)
            for k in ('"', "historical_source:", "source:", "historical_sources:", "-")
        )
        return keyed and "../" in stripped and stripped.count(" ") <= 2

    external_mapping_audit = False
    if rel in EXTERNAL_MAPPING_AUDIT_PATHS:
        missing = [p for p in EXTERNAL_MAPPING_BOUNDARY_PHRASES if p not in text]
        if missing:
            errors.append(
                f"{rel}: listed as an external-mapping audit but its boundary declaration is "
                f"incomplete — missing {missing!r}. Either restore the declaration verbatim or "
                f"remove the file from EXTERNAL_MAPPING_AUDIT_PATHS and strip the external names."
            )
        else:
            external_mapping_audit = True

    for line_no, line in enumerate(text.splitlines(), 1):
        historical_source_record = (
            rel in HISTORICAL_LINEAGE_CARD_PATHS
            and '"source"' in line
            and '"path"' in line
            and '"lifecycle"' in line
            and any(f'"{lifecycle}"' in line for lifecycle in ("legacy", "frozen"))
            and '"role"' in line
            and '"historical_lineage"' in line
        )
        for match in FORBIDDEN.finditer(line):
            control_projection_name = (
                rel in CONTROL_PROJECTION_PATHS
                and match.group(0).lower().startswith("vmosk")
            )
            control_projection_reference = (
                rel in CONTROL_PROJECTION_REFERENCE_PATHS
                and match.group(0).lower().startswith("vmosk")
                and "VMOSK_A.md" in line
                and "non-semantic" in line.lower()
            )
            if not (
                historical_source_record
                or control_projection_name
                or control_projection_reference
                or external_mapping_audit
                or forbidden_match_is_exact_receipt_target(
                    line, match, receipt_target_names
                )
                or (
                    rel in EXTERNAL_SOURCE_PATH_FILES
                    and _is_external_source_path(line)
                )
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_no}: forbidden authority token {match.group(0)!r}"
                )
        application_match = FORBIDDEN_APPLICATION_CLAIMS.search(line)
        if application_match:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_no}: retired application claim "
                f"{application_match.group(0)!r}"
            )
        if "Egregorotype" in line and not allow_legacy_alias:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_no}: unmarked legacy spelling 'Egregorotype'"
            )
    return errors


def main() -> int:
    errors: list[str] = []
    scoped = [ROOT / p for p in FRONT_DOORS + OWNERS]
    scoped.extend(ROOT / p for p in CONTROL_PROJECTION_PATHS)
    scoped.extend(p for p in ROOT.rglob("*") if p.is_file() and is_active_route(p))
    scoped.extend(p for p in ROOT.rglob("*") if p.is_file() and is_active_corpus_file(p))

    seen: set[Path] = set()
    receipt_target_names = physical_receipt_target_names(ROOT)
    for path in scoped:
        path = path.resolve()
        if path in seen:
            continue
        seen.add(path)
        allow_alias = path.relative_to(ROOT) in LEGACY_ALIAS_EXCEPTIONS
        errors.extend(
            scan_file(
                path,
                allow_legacy_alias=allow_alias,
                receipt_target_names=receipt_target_names,
            )
        )

    for prefix in PROJECTION_EXCEPTION_PREFIXES:
        boundary = ROOT / prefix / "README.md"
        if not boundary.is_file():
            errors.append(f"missing projection boundary: {prefix}/README.md")
            continue
        boundary_text = boundary.read_text(encoding="utf-8")
        for phrase in (
            "runtime projection, not worldview doctrine",
            "creates no semantic authority",
            "source owners remain upstream",
        ):
            if phrase not in boundary_text:
                errors.append(
                    f"projection boundary {prefix}/README.md missing phrase: {phrase!r}"
                )

    for rel in CONTROL_PROJECTION_PATHS:
        control_projection = ROOT / rel
        if not control_projection.is_file():
            errors.append(f"missing control projection: {rel}")
            continue
        control_text = control_projection.read_text(encoding="utf-8")
        for phrase in (
            'semantic_authority: "none"',
            "creates no theorem, ontology, axiology",
            "or eighth kernel owner",
            "biological correspondences are optional `[I]` Rosetta annotations",
        ):
            if phrase not in control_text:
                errors.append(
                    f"control projection {rel} missing phrase: {phrase!r}"
                )

    for rel in APPLICATION_TOMBSTONES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing application forwarding tombstone: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if "ARCHIVED" not in text and "SUPERSEDED" not in text:
            errors.append(f"application path is not marked archived/superseded: {rel}")
        if len(text.splitlines()) > 90:
            errors.append(f"application forwarding tombstone regrew into an active body: {rel}")

    for rel in REQUIRED_READER_SURFACES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing lived Weltanschauung reader surface: {rel}")

    for rel in LIVED_TOMBSTONES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing lived-synthesis forwarding tombstone: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if "ARCHIVED" not in text:
            errors.append(f"lived-synthesis path is not marked archived: {rel}")
        if len(text.splitlines()) > 45:
            errors.append(f"lived-synthesis tombstone regrew into an active body: {rel}")

    lived_archive = ROOT / "90_ARCHIVE/2026_07_22_lived_weltanschauung_reconciliation"
    for rel in (
        Path("TOMBSTONE.md"),
        Path("05_COSMOLOGY/00_THE_TORUS_REVELATION.md"),
        Path("06_ONTOLOGY/00_THE_RING_THAT_IS_THE_GROUND.md"),
    ):
        if not (lived_archive / rel).is_file():
            errors.append(f"missing lived-synthesis archive artifact: {rel}")

    application_archive = (
        ROOT / "90_ARCHIVE/2026_07_22_asi_operator_application_boundary/TOMBSTONE.md"
    )
    if not application_archive.is_file():
        errors.append("missing ASI operator application archive tombstone")

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
