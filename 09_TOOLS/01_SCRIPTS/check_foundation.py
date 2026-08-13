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

import hashlib
import json
import os
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
ADDITIVE_TITAN_CORRECTION = Path(
    "11_UPLINK/50_AUDITS_AND_EXECUTIONS/"
    "243_PUBLIC_RELEASE_PREFLIGHT_AND_CONTACT_SNAPSHOT_2026_08_09.md"
)
ACTIVE_EXTRA_TYPE_SURFACES = (
    FORMAL_ORACLE,
    Path("12_PUBLIC_SITE/generate_public_library.py"),
    # The active K-7 owner lives inside the otherwise historical receipt lane.
    # Keep it in scope explicitly so the archive exclusion cannot hide live
    # Titan syntax at the record front door.
    RECORD_LEDGER,
    # This additive correction authorizes the historical-body exception. It is
    # therefore a current semantic surface and must itself pass the type scan.
    ADDITIVE_TITAN_CORRECTION,
)

# This signed 2026-07-19 receipt predates the typed Foundation repair and ends
# with the retired Titan product notation. Historical receipts are evidence,
# not mutable owners: preserve its exact bytes and require the later additive
# correction that states the current source-owner disposition. Any byte drift
# loses this exception and is scanned normally.
HISTORICAL_SIGNED_TITAN_RECORD = Path("00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md")
HISTORICAL_SIGNED_TITAN_RECORD_SHA256 = (
    "743f994f7d1743a0d2da9afa5553d66adc7c78fa741c6406c985a53a4dfb7371"
)
ADDITIVE_TITAN_CORRECTION_MARKERS = (
    "## Additive historical correction",
    "`00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md` is a dated, signed historical",
    "preserves its original bytes",
    "current formula or a source-owner reinstatement",
    "56_THE_PRODUCT_FORM_OF_THE_BALANCE.md",
    "57_THE_POTENTIAL_READING.md",
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
    Path("14_THE_DISTILLATION"),
    Path("90_ARCHIVE"),
    Path("91_COMPATIBILITY"),
)

# Vendored dependency trees and machine build caches. These are not corpus
# surfaces in any sense — nobody wrote them and nobody can repair them here;
# `.lake/` alone is downloaded Lean/mathlib build output.
#
# MEASURED 2026-08-06, not asserted: of the 3705 files this walk previously
# returned, 2765 (577 MB of 589 MB) lived under `.lake/`, and they produced
# ZERO findings. Regex-scanning them was the entire cost of the run — a full
# gate took 365.20 s wall, so `timeout 12` in CI returned rc=124 and the gate
# read as a hang rather than as a verdict. A gate that times out reports
# nothing at all, which is strictly worse than a gate that fails.
#
# This is a mechanical exclusion of machine artifacts, NOT the doctrinal
# provenance exclusion above (e29066a0). Directory names only, matched at any
# depth, so a nested `.lake/packages/*/.lake/` is pruned at the first level.
ACTIVE_SCAN_EXCLUDED_DIR_NAMES = frozenset(
    {
        ".git",
        ".lake",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "node_modules",
        "venv",
    }
)


# --- use vs mention -------------------------------------------------------
#
# The firewall matches CARRIER TEXT. It cannot tell a document that *writes*
# the retired `⊙ = • × ○` from a document that quotes it to strike it. Both look
# identical to a regex. Measured 2026-08-06: the pre-fix gate flagged
# 48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md at :121, :416 and :417 — the
# exact lines that RETIRE the form. Flagging the retraction is not enforcement;
# it makes the gate unusable and trains readers to ignore it.
#
# This is the same false-positive class check_contradiction_census.py already
# names (`is_meta_reference`, META_BODY_MARKERS): a retirement marker near the
# match means the text is *about* the form, not *asserting* it. Two instruments,
# one pattern. The census resolves it at FILE granularity; a firewall must be
# finer than that or a single strike note would deafen a whole document, so this
# resolves it at BLOCK granularity — a fenced block, a blockquote, a table row,
# or a paragraph. A genuine use elsewhere in the same file still fails.
MENTION_MARKERS = re.compile(
    r"retired|struck|strike|strikethrough|withdraw|retract|revoke|rescind|"
    r"ill-typed|ill typed|ill-formed|not well-formed|inadmissible|"
    r"type error|type violation|notation error|category error|"
    r"refuted|repaired|deprecated|killed|banned|dead|"
    # `forbid` is deliberately NOT bare. Measured 2026-08-06: bare `forbid`
    # excused 52_THE_GENERATIVE_BASE.md:26 (`⊙ = e`) on the strength of a
    # neighbouring sentence reading "`DF-15` forbids citing either as support
    # for the other" — a rule about CITATION PRACTICE, not about the form. That
    # is a genuine cross-type identification of the realm mark with the algebra
    # witness identity, and excusing it would be the gate laundering a real
    # finding. A denial only counts when it is attached to the WRITING of the
    # form or to the type-failure being explained.
    r"forbidden|forbids (?:it|this|the|writing)|"
    r"(?:may|must|can)(?:not| not) be written|not a member of the domain|"
    r"wrong kind of thing|not an operand|"
    r"must never|never (?:be )?(?:written|writes|used|asserted)|"
    r"do(?:es)? not (?:write|use|assert|license|admit)|cannot (?:write|assert)|"
    r"no longer|superseded|supersedes|corrected|correction|"
    r"previously (?:read|carried|said|stated)|(?:this|the) (?:line|paragraph|"
    r"clause|document|edition|version)s? (?:first|previously|once) "
    r"(?:read|carried|said)|read backwards|prior edition|earlier reading|"
    r"is false|are false|is wrong|written wrongly|not a theorem|"
    r"reinstate|violate|"
    # P2.2 (2026-08-06): corpus uses these in the same role as `not an operand`
    # — the row or paragraph explains why a Titan token does not perform a role.
    # `not load-bearing` extends `not a theorem` to a deliverable-level claim;
    # `level error` extends `category error` to a level-mismatch explanation;
    # `no item` and `member of nothing` extend `not a member of the domain` to
    # a row that explains the absence; `labels the lower boundary` and
    # `in the field register` extend `not a member` to a register/exemplar
    # boundary; `no salvage` extends `inadmissible` to a repair verdict; the
    # `D•`/`D∞` "distance from" usage is excluded by `distance from` (the
    # corpus's own convention for "this is a label, not a Titan operand").
    r"is not load-bearing|not load-bearing|"
    r"\bno item\b|member of nothing|level error|"
    r"labels the lower boundary|labels the\b|in the field register|"
    r"no salvage|"
    r"distance from|claimed as nothing",
    re.I,
)

_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
_QUOTE_RE = re.compile(r"^\s*>")
_TABLE_RE = re.compile(r"^\s*\|")
_STRIKETHROUGH_RE = re.compile(r"~~.+?~~")

# How far the prose framing a fenced block may sit from its fences. The 48
# fence at :120-:124 is introduced at :118 and annotated from :126; four lines
# covers both without letting an unrelated section leak in. P2.2 (2026-08-06):
# 56_THE_PRODUCT_FORM_OF_THE_BALANCE.md:105 has the [STRUCK] annotation five
# lines below the closing fence — the calibrated 4 leaves that mention invisible.
# Six covers the 48 case (no unrelated section leaks in: 48's surrounding
# region is also a retirement narrative) and catches the 56 case.
FENCE_CONTEXT_LINES = 6

# P2.2 (2026-08-06): paragraph blocks also gain a small context window so a
# neighbouring block (typically the rung header in a <pre> or the caption
# above a table) can carry the retirement marker. The 12_PUBLIC_SITE/0 rung
# splits on blank lines inside <pre class="rung">; the marker at L57 ("never
# an operand — the Titan frame has no arithmetic") must reach the
# `absorption at ○ · ⊙ → 0` line at L62 — five lines apart. Five is the same
# window the fence case uses and stays small enough that an unrelated
# paragraph cannot rescue a real use.
PARAGRAPH_CONTEXT_LINES = 5


def _mention_blocks(lines: list[str]) -> list[tuple[int, int, str]]:
    """Segment raw lines into (start, stop, context_text) mention units.

    Indices are 0-based and half-open. The context is what gets tested for a
    retirement marker; for a fenced block it also includes the prose that
    frames the fence, because that is where a corpus marks a quoted form dead.
    P2.2 (2026-08-06): paragraph blocks now also carry a small context window
    so a neighbour (typically the rung header inside a <pre> that splits on
    blank lines) can carry the marker.
    """

    blocks: list[tuple[int, int, str]] = []
    index = 0
    total = len(lines)
    while index < total:
        line = lines[index]
        if _FENCE_RE.match(line):
            stop = index + 1
            while stop < total and not _FENCE_RE.match(lines[stop]):
                stop += 1
            stop = min(stop + 1, total)  # include the closing fence
            before = max(0, index - FENCE_CONTEXT_LINES)
            after = min(total, stop + FENCE_CONTEXT_LINES)
            blocks.append((index, stop, "\n".join(lines[before:after])))
            index = stop
            continue
        if _QUOTE_RE.match(line):
            stop = index
            while stop < total and _QUOTE_RE.match(lines[stop]):
                stop += 1
            blocks.append((index, stop, "\n".join(lines[index:stop])))
            index = stop
            continue
        if _TABLE_RE.match(line):
            # A table row is its own unit: one struck row must not excuse the
            # rows above and below it.
            blocks.append((index, index + 1, line))
            index += 1
            continue
        if not line.strip():
            index += 1
            continue
        stop = index
        while (
            stop < total
            and lines[stop].strip()
            and not _FENCE_RE.match(lines[stop])
            and not _QUOTE_RE.match(lines[stop])
            and not _TABLE_RE.match(lines[stop])
        ):
            stop += 1
        # P2.2: paragraph blocks now carry PARAGRAPH_CONTEXT_LINES of context
        # on each side so a retirement marker in a neighbouring paragraph
        # (typical: the rung header inside a <pre> that splits on blank lines,
        # or the caption above a table) reaches the carrier line. The table-row
        # branch above is intentionally narrow — a struck row must not rescue
        # the rows around it.
        before = max(0, index - PARAGRAPH_CONTEXT_LINES)
        after = min(total, stop + PARAGRAPH_CONTEXT_LINES)
        blocks.append((index, stop, "\n".join(lines[before:after])))
        index = stop
    return blocks


def mention_lines(text: str) -> set[int]:
    """Return the 1-indexed lines whose carrier text is a MENTION, not a use.

    A line is a mention when the block it belongs to — fenced code, blockquote,
    table row, or paragraph — is annotated as retired/struck/withdrawn/refuted,
    or when the line is markdown strikethrough.
    """

    lines = text.splitlines()
    mentions: set[int] = set()
    for start, stop, context in _mention_blocks(lines):
        if MENTION_MARKERS.search(context):
            mentions.update(range(start + 1, stop + 1))
    for offset, line in enumerate(lines, 1):
        if _STRIKETHROUGH_RE.search(line):
            mentions.add(offset)
    return mentions


def norm(text: str) -> str:
    """Collapse whitespace and markdown emphasis so wording is compared, not layout.

    Underscores are NOT stripped: they carry filenames like 00_THE_FOUNDATION.md.
    """
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text).lower()


def lexical_regular_file_error(root: Path, rel: Path, label: str) -> str | None:
    """Return a custody error for missing, escaped, or symlinked exact paths."""

    lexical_root = Path(os.path.abspath(os.fspath(root)))
    lexical_path = Path(os.path.abspath(os.fspath(root / rel)))
    try:
        parts = lexical_path.relative_to(lexical_root).parts
    except ValueError:
        return f"{label} escapes Foundation root: {rel.as_posix()}"
    current = lexical_root
    if current.is_symlink():
        return f"{label} uses symlink Foundation root: {lexical_root}"
    for part in parts:
        current = current / part
        if current.is_symlink():
            return f"{label} uses symlink component: {current}"
    try:
        resolved_root = lexical_root.resolve(strict=True)
        resolved = lexical_path.resolve(strict=True)
        resolved.relative_to(resolved_root)
    except (FileNotFoundError, RuntimeError, ValueError):
        return f"{label} is missing or escapes Foundation root: {rel.as_posix()}"
    if not resolved.is_file():
        return f"{label} is not a regular file: {rel.as_posix()}"
    return None


def active_foundation_scan_paths(root: Path) -> list[Path]:
    """Discover source-owner and declared-current public type surfaces."""

    paths: set[Path] = set()
    # os.walk rather than rglob so vendored/build trees can be PRUNED instead of
    # walked and then discarded: `.lake/` alone held 2765 of the 3705 files this
    # used to return. Pruning is what turns the run from minutes into seconds.
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name for name in dirnames if name not in ACTIVE_SCAN_EXCLUDED_DIR_NAMES
        ]
        here = Path(dirpath)
        for name in filenames:
            path = here / name
            if path.suffix.lower() not in ACTIVE_SCAN_SUFFIXES:
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


def historical_signed_titan_record_binding(root: Path) -> tuple[list[str], bool]:
    """Validate the one exact historical record and its additive correction."""

    errors: list[str] = []
    record = root / HISTORICAL_SIGNED_TITAN_RECORD
    record_exact = False
    record_custody_error = lexical_regular_file_error(
        root, HISTORICAL_SIGNED_TITAN_RECORD, "historical signed Titan record"
    )
    if record_custody_error is not None:
        errors.append(record_custody_error)
    else:
        actual = hashlib.sha256(record.read_bytes()).hexdigest()
        if actual != HISTORICAL_SIGNED_TITAN_RECORD_SHA256:
            errors.append(
                "historical signed Titan record digest drift: expected "
                f"{HISTORICAL_SIGNED_TITAN_RECORD_SHA256}, got {actual}"
            )
        else:
            record_exact = True

    correction = root / ADDITIVE_TITAN_CORRECTION
    correction_exact = False
    correction_custody_error = lexical_regular_file_error(
        root, ADDITIVE_TITAN_CORRECTION, "additive Titan correction receipt"
    )
    if correction_custody_error is not None:
        errors.append(correction_custody_error)
    else:
        try:
            body = correction.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"additive Titan correction receipt is unreadable: {exc}")
        else:
            missing = [
                marker for marker in ADDITIVE_TITAN_CORRECTION_MARKERS if marker not in body
            ]
            if missing:
                errors.append(
                    "additive Titan correction lost required marker(s): "
                    + ", ".join(repr(marker) for marker in missing)
                )
            else:
                correction_exact = True

    return errors, record_exact and correction_exact


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

    historical_errors, historical_record_bound = historical_signed_titan_record_binding(
        ROOT
    )
    errors.extend(historical_errors)

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
        path = ROOT / rel
        if not path.exists() and not path.is_symlink():
            errors.append(
                f"missing required active Foundation type surface: {rel.as_posix()}"
            )
        else:
            custody_error = lexical_regular_file_error(
                ROOT, rel, "required active Foundation type surface"
            )
            if custody_error is not None:
                errors.append(custody_error)
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

    # --- the two selected presentations are stated in the projection ---
    # CORRECTED 2026-08-06: the reconstruction-era gate required this block in
    # BOTH K-5 and the foundation, but git history (git log -S 'selected
    # relational presentation' -- 00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md)
    # returns nothing — K-5 NEVER carried the block. K-5 is the 5+1
    # constitution of refusals; the two-presentation block belongs to the
    # foundation (the projection), which references it. Requiring it in K-5
    # was a stale expectation, and a gate that fails on content a document
    # never held is the stale-verdict defect live-gate integrity exists to
    # remove. The block is now required where it lives; K-5's reference to
    # "either presentation" (:111) is checked for presence, not the block.
    for label, body in (("00_THE_FOUNDATION.md", proj),):
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

    # K-5 references the presentations without carrying the block; keep the
    # reference present so the two documents stay connected (see corrected
    # loop above — K-5 never carried the block itself).
    if "presentation" not in k5:
        errors.append("K-5: the reference to the two presentations is missing")

    # --- conditional identity theorem and non-operand frame stay explicit ---
    if "if present, is unique" not in registry and "if present, is unique" not in proj:
        errors.append("the corrected conditional identity-uniqueness theorem is missing")
    current_semantic = [PROJECTION, K5, REGISTRY, FORMAL_DOCS[0], FORMAL_DOCS[2], FORMAL_DOCS[-1]]
    mentions_skipped = 0
    for rel in current_semantic:
        mentions = mention_lines(bodies[rel])
        for lineno, line in enumerate(bodies[rel].splitlines(), 1):
            if not RETIRED_TITAN_INFIX.search(line):
                continue
            if lineno in mentions:
                # Quoting the retired infix in order to strike it is the
                # document doing its job, not the infix returning.
                mentions_skipped += 1
                continue
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
        matches = titan_arithmetic_matches(source_text)
        if not matches:
            continue
        if rel == HISTORICAL_SIGNED_TITAN_RECORD and historical_record_bound:
            # Exact immutable history, paired with an additive correction. The
            # SHA binding ensures no extra formula or prose can hide here.
            mentions_skipped += len(matches)
            continue
        # Only pay for the mention pass on files that actually matched.
        mentions = mention_lines(source_text)
        for pattern, offset in matches:
            line_number = line_number_for_offset(source_text, offset)
            if line_number in mentions:
                mentions_skipped += 1
                continue
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

    # The suppression is reported on every run, pass or fail. A use-vs-mention
    # filter is exactly the kind of change that can turn a gate into one that
    # cannot fail, so the number it hides is never allowed to be invisible.
    mention_note = f"{mentions_skipped} quoted-and-struck mention(s) not flagged"

    if errors:
        print("FOUNDATION CONTRACT: FAIL")
        print("\n".join(f"- {e}" for e in errors))
        print(f"({mention_note})")
        return 1

    print(
        f"FOUNDATION CONTRACT: PASS "
        f"({len(required)} surfaces, {len(FENCES)} fences, "
        f"{len(PRESUPPOSED)+len(RELATIONAL)+len(REACHABILITY)} strata symbols, "
        f"{len(active_scan_paths)} source/current-public surfaces type-scanned, "
        f"{mention_note})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
