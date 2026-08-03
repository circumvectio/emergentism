#!/usr/bin/env python3
"""Fail closed on ambiguous receipt citations in active source owners.

Receipt prefixes are physically reused across the two live receipt lanes.  A
numeric token therefore becomes trustworthy only when the same line names one
exact candidate filename (or an explicit plural target set).  The registry also
freezes every exact receipt/packet filename or path in the adjudicated active
owner set.  That second inventory prevents a repaired exact target from being
silently swapped for a different same-prefix file.  Content hashes and ordinals
are identity; line numbers are hints for people.

The older ``check_receipt_citations.py`` still owns the corpus-wide dangling
and 91-prefix legacy heuristic baseline.  This checker does not weaken or
replace it.  In particular, all 97 physically reused prefixes remain unsafe as
bare citations even when a legacy status token makes only 91 look dangerous.

Default mode is read-only.  ``--write`` is an explicit maintainer operation and
will refuse to write while an active occurrence is unresolved or unadjudicated.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = Path("00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json")
RECEIPT_INDEX = Path(
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_RECEIPT_DISAMBIGUATION_INDEX.json"
)
RECEIPT_REF = Path(
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/"
    "241_K3_LEGACY_NOOP_ARCHIVE_LINK_NEUTRALIZER_2026_08_02.md"
)
PUBLIC_MANIFEST = Path("12_PUBLIC_SITE/public_semantic_parity.json")
REGISTRY_DIGEST = re.compile(
    r"^active_receipt_citation_registry_canonical_sha256: ([0-9a-f]{64})$",
    re.M,
)
RECEIPT_LANES = (
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS"),
    Path("11_UPLINK/60_SESSION_PACKETS"),
)
RECEIPT_NAME = re.compile(r"^(\d{2,3})[_A-Za-z]")

# A bare ``r`` plus three digits remains distinct from two-digit Rosetta rows.
# rows.  Explicit receipt/receipts phrases may use two or three digits.
BARE_R = re.compile(r"\br(\d{3})\b", re.I)
_RECEIPT_NUMBER = r"(?<!\d)\d{2,3}(?![A-Za-z0-9])"
_LIST_SEP = r"(?:\s*(?:/|[-\u2013\u2014]|&)\s*|\s*,\s*(?:(?:and|or)\s+)?|\s+(?:and|or)\s+)"
RECEIPT_PHRASE = re.compile(
    rf"\breceipts?\b(?:[ \t]*[:-][ \t]*|[ \t]+)({_RECEIPT_NUMBER}(?:{_LIST_SEP}{_RECEIPT_NUMBER})*)",
    re.I,
)
PACKET_PHRASE = re.compile(
    rf"\bpackets?\b(?:[ \t]*[:-][ \t]*|[ \t]+)({_RECEIPT_NUMBER}(?:{_LIST_SEP}{_RECEIPT_NUMBER})*)",
    re.I,
)
PER_SHORTHAND = re.compile(
    r"\bper\s*(?:C\d+\s*)?/?\s*(\d{3})(?:\s*/\s*(\d{3}))?(?=\s|\u00a7|[,.;:)]|$)",
    re.I,
)
NUMBER = re.compile(r"(?<!\d)\d{2,3}(?!\d)")
RANGE_MARK = re.compile(r"[-\u2013\u2014]")

SCHEMA = "emergentism/active-receipt-citation-registry/v1"
EXPECTED_REUSED_PREFIXES = 97
EXPECTED_ACTIVE_OCCURRENCES_BEFORE_PLURAL_AUDIT = 186
EXPECTED_REPAIR_BASELINE = 182
EXPECTED_ACTIVE_SOURCE_SET_SHA256 = (
    "d8c4137b22281083872aaa6c17081c55140b0c218d360dc03f2a9716046aebde"  # pragma: allow-secret
)
PROGRAM_PLAN_DIAGNOSTIC_SHA256 = (
    "ad043098565d406743474397d23cc7276ef9ae7ce341d76c977788636dda5953"  # pragma: allow-secret
)

# The audited active owners combine the independently reconstructed actionable
# scope with every other active/current source found to contain an exact target.
# Dated handoffs and receipt bodies, archives, books, compatibility shims, and
# frozen/withheld public output remain report-only historical custody.
AUDITED_ACTIVE_SOURCES = (
    ".github/workflows/gate.yml",
    "00_CANONICAL_TREE_OUTLINE.md",
    "00_EMERGENTISM_AS_A_LENS.md",
    "00_ESTABLISHED/README.md",
    "00_FOLDER_LAYOUT_v0.1.md",
    "00_K5_REFUSALS.md",
    "00_K6_REVELATIONS.md",
    "00_K7_RECORD.md",
    "00_META/00_CONTACT_LIMITED_COMPLETION_ROADMAP_2026_08_01.md",
    "00_META/00_FOLDER_LAYOUT_v0.1.md",
    "00_META/00_FOUNDATION_READER_GUIDE.md",
    "00_META/00_SETTLED_CANON_REGISTRY.md",
    "00_META/00_THE_CLAIM_STATUS_REGISTER.md",
    "00_META/00_THE_DISTILLED_DOCTRINE.md",
    "00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md",
    "00_META/00_THE_KINTSUGI_PROTOCOL.md",
    "00_META/00_THE_OPEN_CANON_COVENANT.md",
    "00_META/claim_status/CLAIM_STATUS.yaml",
    "00_META/CONTACT_LIMITED_STATE.json",
    "00_SEVENFOLD_FOUNDATION_ROOT.md",
    "00_THE_AMRITA.md",
    "00_THE_COMPASS.md",
    "00_THE_FOUNDATION.md",
    "00_THE_GOAL.md",
    "00_THE_WELTANSCHAUUNG.md",
    "00_WORK_IN_PROGRESS/00_THE_PROGRAM_PLAN.md",
    "00_WORK_IN_PROGRESS/README.md",
    "01_TELEOLOGY/01_F5_FORCE/02_THE_SERPENT_IS_F5.md",
    "03_METHODOLOGY/00_THE_DOCTRINAL_LADDER.md",
    "03_METHODOLOGY/01_THE_DERIVATION/01_BURRI_RULES_DERIVATION_LEDGER.md",
    "03_METHODOLOGY/02_THE_PAPERS/PAPER_V_STEELMAN.md",
    "03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/00_PROGRAM.md",
    "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md",
    "05_COSMOLOGY/00_WHOLE/README.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/09_THE_TRIADIC_CASCADE.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/37_SEXUAL_SELECTION_AS_VISIBLE_F5.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/39_NEOTENY_AS_F5_DELAY_AND_CULTURAL_WOMB.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/41_THE_GLYPH_TRANSFORMATIONS.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/46_THE_ADMISSIBILITY_OF_NOTHING.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/47_THE_EMERGENCE_OF_FINITY.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/SIMULATION_SPEC.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/00_THE_SEVEN_AXIOMS.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/09_EFR_GODEL_CLARIFICATION.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/12_EFR_EXTRACTION_COEFFICIENT.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/41_UNIFIED_DIMENSIONAL_DERIVATION.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/46_THE_ETA_CONVERSION_MAP.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/48_THE_BOUNDARY_CROSSINGS_AND_THE_MU_CRITERION.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/49_THE_LORENTZ_MOEBIUS_CORRESPONDENCE.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/51_CCC_AND_THE_PRE_ARTICULATE_BOUNDARY.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/53_THE_NUMBER_CHART.md",
    "06_ONTOLOGY/00_BOUNDED_GENERATIVE_EMERGENTISM_2026_07_19.md",
    "06_ONTOLOGY/00_WELTANSCHAUUNG_KERNEL_v0.2_EMERGENTISM_ONLY.md",
    "06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md",
    "06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md",
    "06_ONTOLOGY/04_THE_CONJECTURES.md",
    "06_ONTOLOGY/05_THE_CREED_AND_SPIRAL.md",
    "06_ONTOLOGY/06_THE_REVELATIONS.md",
    "06_ONTOLOGY/ruminations/00_E1_E10_RUMINATION_L7_RSI_2026_07_19.md",
    "06_ONTOLOGY/ruminations/00_RUMINATION_ON_DOF_2026_07_19.md",
    "06_ONTOLOGY/ruminations/00_RUMINATION_ON_THE_TEN_REVELATIONS_2026_07_19.md",
    "07_THEOLOGY/00_THE_AMRITA.md",
    "08_FRAMEWORK_SUPPORT/00_MASTER_INDEX.md",
    "08_FRAMEWORK_SUPPORT/00_META/01_THE_THREE_POSTURES.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/PD_07_FERMI_PARADOX.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/PD_19_THE_HARD_PROBLEM_OF_CONSCIOUSNESS.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_ROSETTA_PROTOCOL.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/05_NON_WEIRD_SWEEP_2026_04_25.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_CIVILISATIONAL.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_INDIGENOUS_AMERICAN.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_MYTHOLOGY.md",
    "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_REPLICATOR.md",
    "09_TOOLS/01_SCRIPTS/build_receipt_disambiguation.py",
    "09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py",
    "09_TOOLS/01_SCRIPTS/check_adjudication_custody.py",
    "09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py",
    "09_TOOLS/01_SCRIPTS/check_claim_status.py",
    "09_TOOLS/01_SCRIPTS/check_contact_limited.py",
    "09_TOOLS/01_SCRIPTS/check_established.py",
    "09_TOOLS/01_SCRIPTS/check_generative_base.py",
    "09_TOOLS/01_SCRIPTS/check_foundation.py",
    "09_TOOLS/01_SCRIPTS/check_q4_declarations.py",
    "09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py",
    "09_TOOLS/01_SCRIPTS/check_work_in_progress.py",
    "09_TOOLS/01_SCRIPTS/coherence_profile.json",
    "09_TOOLS/01_SCRIPTS/gate.sh",
    "09_TOOLS/01_SCRIPTS/rosetta_annotate.py",
    "09_TOOLS/01_SCRIPTS/rosetta_index.py",
    "09_TOOLS/01_SCRIPTS/rosetta_propose.py",
    "09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean",
    "09_TOOLS/05_FORMAL_VERIFICATION/README.md",
    "09_TOOLS/05_FORMAL_VERIFICATION/lakefile.toml",
    "10_SEED/01_THE_SEED_LADDER/D2_GEOMETRY.md",
    "10_SEED/01_THE_SEED_LADDER/D5_THE_GAME.md",
    "10_SEED/01_THE_SEED_LADDER/README.md",
    "11_UPLINK/00_CORE/README.md",
    "11_UPLINK/00_THE_UPLINK.md",
    "11_UPLINK/10_RECONCILIATION/README.md",
    "11_UPLINK/53_DISAMBIGUATION_REVIEW_PACKET.md",
    "11_UPLINK/56_CORPUS_DISAMBIGUATION_EXECUTION_2026_04_16.md",
    "11_UPLINK/57_CORPUS_DISAMBIGUATION_EXECUTION_2026_04_16_ROUND2.md",
    "11_UPLINK/58_BREAKTHROUGH_HARDENING_INDEX.md",
    "11_UPLINK/59_BREAKTHROUGH_HARDENING_DEBRIEF.md",
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md",
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/README.md",
    "11_UPLINK/60_SESSION_PACKETS/README.md",
    "12_PUBLIC_SITE/amrita/amrita.css",
    "12_PUBLIC_SITE/amrita/amrita.json",
    "12_PUBLIC_SITE/amrita/index.html",
    "12_PUBLIC_SITE/assets/js/pwa.js",
    "12_PUBLIC_SITE/build_pwa.py",
    "12_PUBLIC_SITE/discoveries/mass-shell/index.html",
    "12_PUBLIC_SITE/discoveries/the-crossing/index.html",
    "12_PUBLIC_SITE/ecology/index.html",
    "12_PUBLIC_SITE/exit/README.md",
    "12_PUBLIC_SITE/journey/index.html",
    "12_PUBLIC_SITE/predeploy_check.py",
    "12_PUBLIC_SITE/public_semantic_parity.json",
    "12_PUBLIC_SITE/record/index.html",
    "12_PUBLIC_SITE/sw.js",
)
KNOWN_REPORT_ONLY_RESOLVED = {
    "05_COSMOLOGY/00_THE_TORUS_REVELATION.md",
}

SPECIAL_RECEIPT_TARGETS = {
    "134": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/134_ROSETTA_FULL_SET_PURIFICATION_AUDIT_2026_07_19/",
}

TEXT_SUFFIXES = {
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".js",
    ".py",
    ".sh",
    ".lean",
    ".toml",
    ".html",
    ".css",
    ".mjs",
    ".webmanifest",
}
DISCOVERY_SKIP_PARTS = {
    ".git",
    ".lake",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
}
SELF_TEST_FIXTURE_PATHS = {
    "09_TOOLS/02_COMPILERS/test_active_receipt_citations.py",
    "09_TOOLS/02_COMPILERS/test_contact_limited.py",
}
NON_CITATION_INVENTORIES = {
    # Generated topology inventories enumerate filenames by design. Their own
    # register compiler/gate owns byte parity; treating those rows as prose
    # citations would create a registry <-> file-register digest cycle.
    "00_META/registers/FILE_REGISTER.json",
    "00_META/registers/FOLDER_REGISTER.json",
}
NON_CITATION_PREFIXES = (
    # Vendored libraries use row-like identifiers which are not corpus receipt
    # language. They remain in the delivered dependency census, while
    # their integrity/licence custody belongs to the public-site gates.
    Path("12_PUBLIC_SITE/vendor"),
)
ACTIVE_ROUTE_NAMES = {"README.md", "AGENTS.md", "CLAUDE.md"}

DIAGNOSTIC_UNITS = (
    (
        "00_WORK_IN_PROGRESS/00_THE_PROGRAM_PLAN.md",
        2,
        PROGRAM_PLAN_DIAGNOSTIC_SHA256,
        frozenset({"117", "139"}),
    ),
    (
        "00_WORK_IN_PROGRESS/README.md",
        7,
        "049a1fa373ba943ea5004f09e92fa3887bcbb11c6f9fa04086ba8a174e63686e",  # pragma: allow-secret
        frozenset({"149", "150", "151"}),
    ),
    (
        "09_TOOLS/01_SCRIPTS/build_receipt_disambiguation.py",
        2,
        "0cabf6f6bd43771f5d5b16e9592b5f9ef4bd056c98dd633de240694d363f0239",  # pragma: allow-secret
        frozenset({"150"}),
    ),
    (
        "09_TOOLS/01_SCRIPTS/check_receipt_citations.py",
        3,
        "e5d4eec7d5b000c3512abaee9fe880e78b26696405bb8945dad7620ebd7019d6",  # pragma: allow-secret
        frozenset({"139"}),
    ),
    (
        "09_TOOLS/01_SCRIPTS/check_receipt_citations.py",
        5,
        "52c098a11205206f93fdad1ceba9c6ead083d4e12e97b4115cf9479fa1fb8f42",  # pragma: allow-secret
        frozenset({"156"}),
    ),
    (
        "09_TOOLS/01_SCRIPTS/check_receipt_citations.py",
        7,
        "60090d08d67593858f510032154f185f6c1b7315f6ac18cb52e9dcd9394d864f",  # pragma: allow-secret
        frozenset({"139"}),
    ),
)


class ContractError(Exception):
    """One or more citation-custody invariants failed."""

    def __init__(self, errors: str | Iterable[str]):
        self.errors = [errors] if isinstance(errors, str) else list(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class Citation:
    number: str
    start: int
    end: int
    token: str
    phrase_start: int
    phrase_end: int
    namespace: str = "receipt"
    expanded: bool = False


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys
        )
    except FileNotFoundError as exc:
        raise ContractError(f"missing machine owner: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON at {path}: {exc}") from exc


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def path_set_sha256(paths: Iterable[str]) -> str:
    return canonical_sha256(sorted(set(paths)))


def semantic_unit_sha256(unit: str) -> str:
    return hashlib.sha256(unit.encode("utf-8")).hexdigest()


def receipt_files(root: Path) -> dict[str, list[Path]]:
    by_number: dict[str, list[Path]] = defaultdict(list)
    for lane in RECEIPT_LANES:
        base = root / lane
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            match = RECEIPT_NAME.match(path.name)
            if match and match.group(1) != "00":
                by_number[match.group(1)].append(path.relative_to(root))
    return dict(by_number)


def reused_groups(root: Path) -> dict[str, list[str]]:
    return {
        number: sorted(str(path) for path in paths)
        for number, paths in receipt_files(root).items()
        if len(paths) > 1
    }


def packet_files(root: Path) -> dict[str, list[str]]:
    by_number: dict[str, list[str]] = defaultdict(list)
    base = root / RECEIPT_LANES[1]
    if not base.is_dir():
        return {}
    for path in sorted(base.rglob("*.md")):
        match = RECEIPT_NAME.match(path.name)
        if match and match.group(1) != "00":
            by_number[match.group(1)].append(str(path.relative_to(root)))
    return dict(by_number)


def indexed_reused_groups(root: Path) -> dict[str, list[str]]:
    index = load_json(root / RECEIPT_INDEX)
    if not isinstance(index, dict) or not isinstance(index.get("rows"), list):
        raise ContractError(f"malformed receipt disambiguation index: {RECEIPT_INDEX}")
    groups: dict[str, list[str]] = {}
    for row in index["rows"]:
        if not isinstance(row, dict) or not isinstance(row.get("entries"), list):
            raise ContractError(f"malformed receipt disambiguation row: {row!r}")
        number = str(row.get("number", ""))
        paths: list[str] = []
        for entry in row["entries"]:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                raise ContractError(f"malformed receipt disambiguation entry: {entry!r}")
            paths.append(entry["path"])
        if number in groups:
            raise ContractError(f"duplicate receipt disambiguation row r{number}")
        if len(paths) != len(set(paths)):
            raise ContractError(f"duplicate candidate path in receipt index row r{number}")
        groups[number] = sorted(paths)
    if index.get("ambiguousNumbers") != len(groups):
        raise ContractError("receipt index ambiguousNumbers does not match its rows")
    return groups


def _expand_number_phrase(match: re.Match[str], namespace: str) -> list[Citation]:
    body = match.group(1)
    base = match.start(1)
    numbers = list(NUMBER.finditer(body))
    result: list[Citation] = []
    for item in numbers:
        result.append(
            Citation(
                item.group(0),
                base + item.start(),
                base + item.end(),
                match.group(0),
                match.start(),
                match.end(),
                namespace=namespace,
            )
        )
    for left, right in zip(numbers, numbers[1:]):
        separator = body[left.end() : right.start()]
        if not RANGE_MARK.search(separator):
            continue
        lo, hi = int(left.group(0)), int(right.group(0))
        if hi <= lo or hi - lo > 200:
            raise ContractError(
                f"malformed or over-broad {namespace} range {match.group(0)!r}"
            )
        present = {int(item.number) for item in result}
        for number in range(lo + 1, hi):
            if number in present:
                continue
            result.append(
                Citation(
                    str(number),
                    match.start(),
                    match.end(),
                    f"{match.group(0)} [expanded r{number}]",
                    match.start(),
                    match.end(),
                    namespace=namespace,
                    expanded=True,
                )
            )
    return result


def citation_mentions(text: str) -> list[Citation]:
    receipt_phrases = list(RECEIPT_PHRASE.finditer(text))
    packet_phrases = list(PACKET_PHRASE.finditer(text))
    phrases = receipt_phrases + packet_phrases
    shorthands = list(PER_SHORTHAND.finditer(text))
    mentions: list[Citation] = []
    for phrase in receipt_phrases:
        mentions.extend(_expand_number_phrase(phrase, "receipt"))
    for phrase in packet_phrases:
        mentions.extend(_expand_number_phrase(phrase, "packet"))
    for match in BARE_R.finditer(text):
        if any(p.start() <= match.start() < p.end() for p in phrases + shorthands):
            continue
        mentions.append(
            Citation(
                match.group(1),
                match.start(),
                match.end(),
                match.group(0),
                match.start(),
                match.end(),
                namespace="receipt",
            )
        )
    for match in shorthands:
        for group in (1, 2):
            if match.group(group) is None:
                continue
            mentions.append(
                Citation(
                    match.group(group),
                    match.start(group),
                    match.end(group),
                    match.group(0),
                    match.start(),
                    match.end(),
                    namespace="receipt",
                )
            )
    return sorted(
        mentions,
        key=lambda item: (
            item.phrase_start,
            item.phrase_end,
            item.namespace,
            int(item.number),
            item.expanded,
        ),
    )


def _literal_token_present(text: str, literal: str) -> bool:
    """Return true only for a complete filename/path token.

    Slashes delimit a basename and are intentionally allowed at either edge;
    alphanumerics plus filename punctuation continue the token. Thus a relative
    path can bind a basename, while ``x126_TARGET.md`` and
    ``126_TARGET.md.bak`` cannot impersonate it.
    """
    start = 0
    while True:
        position = text.find(literal, start)
        if position < 0:
            return False
        end = position + len(literal)
        start = end
        if not _filename_token_is_complete(text, position, end):
            continue
        return True


def _filename_token_is_complete(text: str, position: int, end: int) -> bool:
    before = text[position - 1] if position else ""
    after = text[end] if end < len(text) else ""
    before_continues = before.isalnum() or before in "_.-"
    after_continues = after.isalnum() or after in "_-"
    if after == ".":
        following = text[end + 1] if end + 1 < len(text) else ""
        after_continues = following.isalnum() or following in "_.-"
    return not before_continues and not after_continues


def _literal_candidate_hits(unit: str, candidates: list[str]) -> set[str]:
    return {
        path
        for path in candidates
        if _literal_token_present(unit, Path(path).name)
        or _literal_token_present(unit, path)
    }


def semantic_unit(text: str, mention: Citation) -> str:
    """Return the one physical line that must bind a typed citation.

    Paragraph-wide binding is intentionally forbidden: a filename in a later
    sentence, appendix line, or ledger row must not shield a bare locator above.
    Owners with wrapped prose keep the exact target on the citation line.
    """
    line_start = text.rfind("\n", 0, mention.phrase_start) + 1
    line_end = text.find("\n", mention.phrase_end)
    if line_end < 0:
        line_end = len(text)
    return text[line_start:line_end]


def exact_target_mentions(
    text: str,
    targets: dict[str, list[str]],
) -> tuple[list[tuple[Citation, str]], list[str]]:
    """Locate exact physical target names/paths in one audited source.

    A basename that exists at more than one physical path is insufficient by
    itself; its line must contain exactly one full repo-relative path.  This is
    the exact-token half of the ratchet and is deliberately independent of the
    ``receipt N``/``packet N`` phrase parser.
    """
    by_basename: dict[str, list[str]] = defaultdict(list)
    for paths in targets.values():
        for target in paths:
            by_basename[Path(target).name].append(target)

    found: list[tuple[Citation, str]] = []
    errors: list[str] = []
    for basename, candidate_paths in sorted(by_basename.items()):
        start = 0
        while True:
            position = text.find(basename, start)
            if position < 0:
                break
            end = position + len(basename)
            start = end
            if not _filename_token_is_complete(text, position, end):
                continue

            line_start = text.rfind("\n", 0, position) + 1
            line_end = text.find("\n", end)
            if line_end < 0:
                line_end = len(text)
            line = text[line_start:line_end]
            full_path_hits = {path for path in candidate_paths if path in line}
            if len(candidate_paths) == 1:
                target = candidate_paths[0]
            elif len(full_path_hits) == 1:
                target = next(iter(full_path_hits))
            else:
                detail = ", ".join(sorted(candidate_paths))
                errors.append(
                    f"exact basename {basename!r} maps to multiple physical paths; "
                    f"cite one repo-relative path on the same line: {detail}"
                )
                continue

            match = RECEIPT_NAME.match(basename)
            if match is None:
                errors.append(f"exact target basename lost its numeric prefix: {basename}")
                continue
            namespace = (
                "exact_packet"
                if target.startswith(f"{RECEIPT_LANES[1]}/")
                else "exact_receipt"
            )
            found.append(
                (
                    Citation(
                        match.group(1),
                        position,
                        end,
                        basename,
                        position,
                        end,
                        namespace=namespace,
                    ),
                    target,
                )
            )

    for number, target in sorted(SPECIAL_RECEIPT_TARGETS.items(), key=lambda item: int(item[0])):
        start = 0
        while True:
            position = text.find(target, start)
            if position < 0:
                break
            end = position + len(target)
            start = end
            found.append(
                (
                    Citation(
                        number,
                        position,
                        end,
                        target,
                        position,
                        end,
                        namespace="exact_receipt_bundle",
                    ),
                    target,
                )
            )

    return (
        sorted(found, key=lambda item: (item[0].start, item[0].namespace, item[1])),
        errors,
    )


def occurrence_row(
    source: str,
    text: str,
    mention: Citation,
    source_ordinal: int,
    resolution: str,
    target: str | list[str],
) -> dict[str, Any]:
    line_start = text.rfind("\n", 0, mention.phrase_start) + 1
    line_end = text.find("\n", mention.phrase_end)
    if line_end < 0:
        line_end = len(text)
    unit = text[line_start:line_end]
    prior_units = text[:line_start].splitlines()
    unit_occurrence = sum(1 for prior in prior_units if prior == unit)
    unit_mentions = citation_mentions(unit)
    relative_start = mention.start - line_start
    citation_ordinal = next(
        (
            index
            for index, item in enumerate(unit_mentions)
            if item.number == mention.number
            and item.namespace == mention.namespace
            and item.start == relative_start
            and item.expanded == mention.expanded
        ),
        0,
    )
    return {
        "source": source,
        "semantic_unit_sha256": semantic_unit_sha256(unit),
        "semantic_unit_occurrence": unit_occurrence,
        "citation_ordinal": citation_ordinal,
        "source_occurrence_ordinal": source_ordinal,
        "token": mention.token,
        "namespace": mention.namespace,
        "number": mention.number,
        "expanded_from_range": mention.expanded,
        "target": target,
        "resolution": resolution,
    }


def build_occurrences(
    root: Path,
    groups: dict[str, list[str]],
    packets: dict[str, list[str]],
    all_targets: dict[str, list[str]],
) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for source in AUDITED_ACTIVE_SOURCES:
        path = root / source
        if not path.is_file():
            errors.append(f"missing audited active source: {source}")
            continue
        text = path.read_text(encoding="utf-8", errors="strict")
        source_ordinal = 0
        for mention in citation_mentions(text):
            if _diagnostic_occurrence_allowed(source, text, mention):
                continue
            candidates: list[str]
            if mention.namespace == "packet":
                candidates = packets.get(mention.number, [])
                if not candidates:
                    errors.append(
                        f"{source} names packet {mention.number}, but lane 60 has no such packet"
                    )
                    source_ordinal += 1
                    continue
            elif mention.number in SPECIAL_RECEIPT_TARGETS:
                target = SPECIAL_RECEIPT_TARGETS[mention.number]
                if not (root / target).is_dir():
                    errors.append(f"special receipt target disappeared: {target}")
                    source_ordinal += 1
                    continue
                if target not in semantic_unit(text, mention):
                    unit_line = text.count("\n", 0, mention.phrase_start) + 1
                    errors.append(
                        f"{source}:{unit_line} {mention.token!r} is not bound to special target {target}"
                    )
                    source_ordinal += 1
                    continue
                rows.append(
                    occurrence_row(
                        source,
                        text,
                        mention,
                        source_ordinal,
                        "inline_exact_special_target",
                        target,
                    )
                )
                source_ordinal += 1
                continue
            elif mention.number in groups:
                candidates = groups[mention.number]
            else:
                continue

            hits = _literal_candidate_hits(semantic_unit(text, mention), candidates)
            plural_set = mention.token.lower().startswith("receipts")
            if not hits or (len(hits) > 1 and not plural_set):
                unit_line = text.count("\n", 0, mention.phrase_start) + 1
                detail = "none" if not hits else ", ".join(sorted(hits))
                errors.append(
                    f"{source}:{unit_line} {mention.token!r} must bind "
                    f"{'one or an explicit plural set of' if mention.namespace == 'receipt' else 'exactly one'} "
                    f"{mention.namespace} target(s) in the same semantic unit; found {detail}"
                )
                source_ordinal += 1
                continue
            target = next(iter(hits)) if len(hits) == 1 else sorted(hits)
            rows.append(
                occurrence_row(
                    source,
                    text,
                    mention,
                    source_ordinal,
                    "inline_exact_target_set" if isinstance(target, list) else "inline_exact_target",
                    target,
                )
            )
            source_ordinal += 1

        exact_mentions, exact_errors = exact_target_mentions(text, all_targets)
        errors.extend(f"{source}: {error}" for error in exact_errors)
        for mention, target in exact_mentions:
            if mention.namespace == "exact_receipt_bundle" and not (root / target).is_dir():
                errors.append(f"{source}: exact receipt bundle disappeared: {target}")
                continue
            if mention.namespace != "exact_receipt_bundle" and not (root / target).is_file():
                errors.append(f"{source}: exact receipt target disappeared: {target}")
                continue
            rows.append(
                occurrence_row(
                    source,
                    text,
                    mention,
                    source_ordinal,
                    "exact_target_token",
                    target,
                )
            )
            source_ordinal += 1
    return rows, errors


def public_active_artifacts(root: Path) -> set[str]:
    public = root / "12_PUBLIC_SITE"
    if not public.is_dir():
        return set()
    manifest = load_json(root / PUBLIC_MANIFEST)
    if not isinstance(manifest, dict):
        raise ContractError(f"malformed public lifecycle manifest: {PUBLIC_MANIFEST}")
    current = manifest.get("currentSurfaces")
    provisional = manifest.get("declaredProvisional")
    if not isinstance(current, list) or not all(isinstance(item, str) for item in current):
        raise ContractError("public currentSurfaces must be a list of paths")
    if not isinstance(provisional, dict) or not isinstance(provisional.get("routes"), list):
        raise ContractError("public declaredProvisional.routes must be a list")
    routes = list(current) + list(provisional["routes"])
    if not all(isinstance(item, str) for item in routes):
        raise ContractError("public active lifecycle contains a non-path value")
    active = {f"12_PUBLIC_SITE/{item}" for item in routes}

    # Current/provisional HTML owns its delivered local dependencies too.  Scan
    # executable/style/data dependencies, not ordinary navigation links, so an
    # active page cannot hide a bare locator in a fetched JSON or companion CSS.
    dependency_patterns = (
        re.compile(r"\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I),
        re.compile(r"<link\b[^>]*\bhref\s*=\s*[\"']([^\"']+)[\"']", re.I),
        re.compile(r"\bfetch\(\s*[\"']([^\"']+)[\"']", re.I),
        re.compile(r"\burl\(\s*[\"']?([^\"')]+)", re.I),
        re.compile(r"@import\s+[\"']([^\"']+)[\"']", re.I),
        re.compile(
            r"\b(?:import|export)\s+(?:[^\"']*?\s+from\s+)?[\"']([^\"']+)[\"']",
            re.I,
        ),
        re.compile(r"\bimport\(\s*[\"']([^\"']+)[\"']", re.I),
        re.compile(r"\bserviceWorker\.register\(\s*[\"']([^\"']+)[\"']", re.I),
        re.compile(r"\bnew\s+(?:Shared)?Worker\(\s*[\"']([^\"']+)[\"']", re.I),
        re.compile(
            r"\b(?:paintWorklet|audioWorklet)\.addModule\(\s*[\"']([^\"']+)[\"']",
            re.I,
        ),
    )
    queue = list(sorted(active))
    public_resolved = public.resolve()
    while queue:
        source = queue.pop(0)
        path = root / source
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError):
            continue
        dependencies = [
            match.group(1)
            for pattern in dependency_patterns
            for match in pattern.finditer(text)
        ]
        for import_scripts in re.finditer(
            r"\bimportScripts\((.*?)\)", text, re.S
        ):
            dependencies.extend(
                match.group(1)
                for match in re.finditer(
                    r"[\"']([^\"']+)[\"']", import_scripts.group(1)
                )
            )
        if source == "12_PUBLIC_SITE/sw.js":
            spine = re.search(r"\bconst\s+SPINE\s*=\s*\[(.*?)\]\s*;", text, re.S)
            if spine:
                dependencies.extend(
                    match.group(1)
                    for match in re.finditer(r"[\"']([^\"']+)[\"']", spine.group(1))
                )
        for dependency in dependencies:
            raw = dependency.split("#", 1)[0].split("?", 1)[0].strip()
            if not raw or raw.startswith(("http:", "https:", "//", "data:", "mailto:")):
                continue
            candidate = public / raw.lstrip("/") if raw.startswith("/") else path.parent / raw
            candidate = candidate.resolve()
            if not candidate.is_relative_to(public_resolved):
                continue
            if candidate.is_dir():
                candidate = candidate / "index.html"
            if not candidate.is_file() or candidate.suffix.lower() not in TEXT_SUFFIXES:
                continue
            relative = str(candidate.relative_to(root.resolve()))
            if relative not in active:
                active.add(relative)
                queue.append(relative)
    return active


def _is_report_only(path: Path, public_active: set[str]) -> bool:
    parts = path.parts
    if "90_ARCHIVE" in parts:
        return True
    if parts and parts[0] == "00_HANDOFF":
        return not (len(parts) == 2 and path.name in ACTIVE_ROUTE_NAMES)
    if parts and parts[0] in {"13_BOOKS", "91_COMPATIBILITY"}:
        return True
    value = str(path)
    if any(value == str(lane) or value.startswith(f"{lane}/") for lane in RECEIPT_LANES):
        if value == "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md":
            return False
        return not (path.parent in RECEIPT_LANES and path.name in ACTIVE_ROUTE_NAMES)
    if parts and parts[0] == "12_PUBLIC_SITE":
        return value not in set(AUDITED_ACTIVE_SOURCES) and value not in public_active
    return value in KNOWN_REPORT_ONLY_RESOLVED


def _diagnostic_occurrence_allowed(source: str, text: str, mention: Citation) -> bool:
    lines = text.splitlines()
    line_offsets: list[int] = []
    offset = 0
    for line in lines:
        line_offsets.append(offset)
        offset += len(line) + 1
    for expected_source, width, digest, numbers in DIAGNOSTIC_UNITS:
        if source != expected_source or mention.number not in numbers:
            continue
        for index in range(0, len(lines) - width + 1):
            unit = "\n".join(lines[index : index + width])
            if semantic_unit_sha256(unit) != digest:
                continue
            unit_start = line_offsets[index]
            unit_end = unit_start + len(unit)
            if unit_start <= mention.phrase_start <= unit_end:
                return True
    return False


def discover_unregistered_ambiguity_errors(
    root: Path,
    groups: dict[str, list[str]],
    packets: dict[str, list[str]],
    all_targets: dict[str, list[str]],
) -> tuple[list[str], int]:
    """Catch new typed or exact citations outside the active-owner registry."""
    errors: list[str] = []
    report_only = 0
    active = set(AUDITED_ACTIVE_SOURCES)
    public_active = public_active_artifacts(root)
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root)
        if any(part in DISCOVERY_SKIP_PARTS for part in rel.parts):
            continue
        source = str(rel)
        if (
            source in SELF_TEST_FIXTURE_PATHS
            or source in NON_CITATION_INVENTORIES
            or any(rel == prefix or rel.is_relative_to(prefix) for prefix in NON_CITATION_PREFIXES)
        ):
            continue
        report = _is_report_only(rel, public_active)
        if source in active or rel == REGISTRY_PATH or report:
            if report:
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                report_only += sum(
                    1
                    for item in citation_mentions(text)
                    if (
                        item.namespace == "packet" and item.number in packets
                    )
                    or (
                        item.namespace == "receipt"
                        and (
                            item.number in groups
                            or item.number in SPECIAL_RECEIPT_TARGETS
                        )
                    )
                )
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError):
            continue
        for mention in citation_mentions(text):
            tracked = (
                mention.namespace == "packet" and mention.number in packets
            ) or (
                mention.namespace == "receipt"
                and (
                    mention.number in groups
                    or mention.number in SPECIAL_RECEIPT_TARGETS
                )
            )
            if not tracked:
                continue
            if _diagnostic_occurrence_allowed(source, text, mention):
                continue
            line = text.count("\n", 0, mention.phrase_start) + 1
            errors.append(
                f"new unregistered active ambiguity at {source}:{line}: {mention.token!r}"
            )

        exact_mentions, exact_errors = exact_target_mentions(text, all_targets)
        errors.extend(
            f"new unregistered active exact-target ambiguity at {source}: {error}"
            for error in exact_errors
        )
        for mention, target in exact_mentions:
            line = text.count("\n", 0, mention.phrase_start) + 1
            errors.append(
                "new unregistered active exact target at "
                f"{source}:{line}: {mention.token!r} -> {target}"
            )
    return errors, report_only


def _candidate_rows(groups: dict[str, list[str]]) -> list[dict[str, Any]]:
    return [
        {
            "number": number,
            "unsafe_bare": True,
            "candidate_paths": paths,
        }
        for number, paths in sorted(groups.items(), key=lambda item: int(item[0]))
    ]


def build_registry(root: Path) -> dict[str, Any]:
    physical = receipt_files(root)
    all_targets = {
        number: sorted(str(path) for path in paths)
        for number, paths in physical.items()
    }
    groups = {
        number: paths for number, paths in all_targets.items() if len(paths) > 1
    }
    packets = packet_files(root)
    public_active = public_active_artifacts(root)
    errors: list[str] = []
    if len(groups) != EXPECTED_REUSED_PREFIXES:
        errors.append(
            f"physical reused-prefix universe is {len(groups)}, expected {EXPECTED_REUSED_PREFIXES}"
        )
    if path_set_sha256(AUDITED_ACTIVE_SOURCES) != EXPECTED_ACTIVE_SOURCE_SET_SHA256:
        errors.append("hard-coded audited active-source set hash drifted")
    try:
        indexed = indexed_reused_groups(root)
        if indexed != groups:
            errors.append(
                "receipt disambiguation index candidate groups differ from physical filenames"
            )
    except ContractError as exc:
        errors.extend(exc.errors)
    rows, occurrence_errors = build_occurrences(root, groups, packets, all_targets)
    errors.extend(occurrence_errors)
    broad_errors, report_only = discover_unregistered_ambiguity_errors(
        root, groups, packets, all_targets
    )
    errors.extend(broad_errors)
    if errors:
        raise ContractError(errors)
    return {
        "schema": SCHEMA,
        "status": "ACTIVE_INTERNAL_CITATION_CUSTODY",
        "boundary": (
            "A registered exact filename/path token disambiguates a receipt citation; it does not "
            "ratify the receipt, promote evidence, or rewrite historical custody."
        ),
        "custody": {
            "receipt_ref": str(RECEIPT_REF),
            "digest_marker": "active_receipt_citation_registry_canonical_sha256",
            "rebaseline_rule": "A changed registry requires a new dated receipt path.",
        },
        "scope": {
            "active_source_count": len(AUDITED_ACTIVE_SOURCES),
            "active_source_set_sha256": path_set_sha256(AUDITED_ACTIVE_SOURCES),
            "active_sources": list(AUDITED_ACTIVE_SOURCES),
            "public_current_provisional_text_dependency_count": len(public_active),
            "public_current_provisional_text_dependencies_sha256": path_set_sha256(public_active),
            "scope_cut": {
                "text_suffixes": sorted(TEXT_SUFFIXES),
                "non_citation_inventories": sorted(NON_CITATION_INVENTORIES),
                "non_citation_prefixes": sorted(str(path) for path in NON_CITATION_PREFIXES),
                "self_test_fixture_paths": sorted(SELF_TEST_FIXTURE_PATHS),
                "known_report_only_resolved": sorted(KNOWN_REPORT_ONLY_RESOLVED),
                "active_route_names": sorted(ACTIVE_ROUTE_NAMES),
                "binary_public_dependencies": (
                    "delivered but omitted from citation-text scanning"
                ),
            },
            "historical_policy": (
                "Dated handoffs and receipt bodies, archives, books, compatibility "
                "shims, and generated/frozen/withheld public outputs outside the active "
                "delivery dependency closure are report-only."
            ),
            "report_only_typed_locator_occurrences_observed": report_only,
            "diagnostic_exemptions": [
                {
                    "source": source,
                    "semantic_unit_lines": width,
                    "semantic_unit_sha256": digest,
                    "numbers": sorted(numbers, key=int),
                    "reason": "context-hashed diagnostic, not a target-selecting citation",
                }
                for source, width, digest, numbers in DIAGNOSTIC_UNITS
            ],
        },
        "receipt_universe": {
            "source_index": str(RECEIPT_INDEX),
            "citable_targets": sum(len(paths) for paths in all_targets.values()),
            "all_candidate_paths_sha256": canonical_sha256(all_targets),
            "reused_prefixes": len(groups),
            "all_reused_prefixes_unsafe_bare": True,
            "candidate_groups_sha256": canonical_sha256(groups),
            "groups": _candidate_rows(groups),
        },
        "packet_namespace": {
            "lane": str(RECEIPT_LANES[1]),
            "typed_rule": (
                "packet N selects lane 60 and must name exactly one physical packet "
                "path in the same semantic unit"
            ),
            "numbered_prefixes": len(packets),
            "candidate_groups_sha256": canonical_sha256(packets),
        },
        "occurrences": {
            "legacy_actionable_baseline": EXPECTED_REPAIR_BASELINE,
            "singular_pre_plural_audit_occurrences": EXPECTED_ACTIVE_OCCURRENCES_BEFORE_PLURAL_AUDIT,
            "count": len(rows),
            "typed_locator_count": sum(
                1 for row in rows if not row["namespace"].startswith("exact_")
            ),
            "exact_target_token_count": sum(
                1 for row in rows if row["namespace"].startswith("exact_")
            ),
            "source_count": len({row["source"] for row in rows}),
            "rows_sha256": canonical_sha256(rows),
            "rows": rows,
        },
    }


def _git_path_bytes(root: Path, revision: str, path: Path) -> bytes | None:
    """Read one path from a required commit, distinguishing absence from failure."""
    verify = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if verify.returncode != 0:
        raise ContractError([f"required git revision unavailable: {revision}"])
    tree = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-z", revision, "--", path.as_posix()],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if tree.returncode != 0:
        raise ContractError(
            [f"cannot inspect {path} at required git revision {revision}"]
        )
    if not tree.stdout:
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path.as_posix()}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise ContractError([f"cannot read {path} at required git revision {revision}"])
    return result.stdout


def _first_parent_revision(root: Path) -> str | None:
    """Return HEAD's first parent; fail when shallow history hides it."""
    shallow = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--is-shallow-repository"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if shallow.returncode != 0:
        raise ContractError(["cannot determine whether git history is shallow"])
    row = subprocess.run(
        ["git", "-C", str(root), "rev-list", "--parents", "-n", "1", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if row.returncode != 0 or not row.stdout.strip():
        raise ContractError(["cannot inspect HEAD first-parent history"])
    parts = row.stdout.split()
    if len(parts) == 1:
        if shallow.stdout.strip().lower() == "true":
            raise ContractError(["first-parent history unavailable in shallow repository"])
        return None
    return parts[1]


def custody_errors(root: Path, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    receipt = root / RECEIPT_REF
    if not receipt.is_file():
        return [f"missing registry custody receipt: {RECEIPT_REF}"]
    receipt_bytes = receipt.read_bytes()
    text = receipt_bytes.decode("utf-8", errors="ignore")
    markers = REGISTRY_DIGEST.findall(text)
    digest = canonical_sha256(registry)
    if markers != [digest]:
        errors.append(
            f"{RECEIPT_REF} must contain exactly one registry digest marker {digest}"
        )
    try:
        head = _git_path_bytes(root, "HEAD", RECEIPT_REF)
    except ContractError as exc:
        errors.extend(exc.errors)
        return errors
    if head is not None and head != receipt_bytes:
        errors.append(f"{RECEIPT_REF} differs from committed HEAD bytes")
    if head is not None:
        try:
            parent_revision = _first_parent_revision(root)
            parent = (
                _git_path_bytes(root, parent_revision, RECEIPT_REF)
                if parent_revision is not None
                else None
            )
        except ContractError as exc:
            errors.extend(exc.errors)
        else:
            if parent is not None and head != parent:
                errors.append(f"{RECEIPT_REF} differs from immutable first-parent bytes")
    return errors


def validate_registry(
    root: Path, registry: dict[str, Any], *, require_custody: bool = True
) -> tuple[int, int]:
    expected = build_registry(root)
    errors: list[str] = []
    if registry != expected:
        errors.append(
            "registry differs from physical candidates or active semantic-unit locators; "
            "run --write only after adjudicating the drift"
        )
    if require_custody:
        errors.extend(custody_errors(root, registry))
    if errors:
        raise ContractError(errors)
    return (
        expected["occurrences"]["count"],
        expected["scope"]["report_only_typed_locator_occurrences_observed"],
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    try:
        expected = build_registry(ROOT)
        if args.write:
            target = ROOT / REGISTRY_PATH
            target.write_text(
                json.dumps(expected, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(
                f"active citation registry: wrote {expected['occurrences']['count']} "
                f"occurrences across {expected['occurrences']['source_count']} sources"
            )
            print(
                f"  custody pending until {RECEIPT_REF.name} contains: "
                f"active_receipt_citation_registry_canonical_sha256: {canonical_sha256(expected)}"
            )
            return 0
        registry = load_json(ROOT / REGISTRY_PATH)
        count, report_only = validate_registry(ROOT, registry)
    except ContractError as exc:
        print("ACTIVE RECEIPT CITATIONS: FAIL")
        for error in exc.errors[:30]:
            print(f"- {error}")
        if len(exc.errors) > 30:
            print(f"- ...and {len(exc.errors) - 30} more")
        return 1
    print(
        f"ACTIVE RECEIPT CITATIONS: PASS ({count} active custody rows; "
        f"{registry['occurrences']['typed_locator_count']} typed locators; "
        f"{registry['occurrences']['exact_target_token_count']} exact target tokens; "
        f"{EXPECTED_REUSED_PREFIXES} reused prefixes all unsafe bare; "
        f"{report_only} report-only historical typed locators observed)"
    )
    print(
        "  scope: proves exact active target custody, not receipt truth, evidence tier, "
        "publication, deployment, or historical renumbering."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
