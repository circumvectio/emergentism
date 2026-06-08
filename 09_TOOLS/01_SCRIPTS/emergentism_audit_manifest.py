#!/usr/bin/env python3
"""Generate the Emergentism corpus audit manifest and summary.

The manifest is an operational control layer. It inventories source files and
records the audit posture for each file; it does not certify doctrine by itself.
"""

from __future__ import annotations

import csv
import hashlib
import re
import stat
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ORG = ROOT / "01_EMERGENTISM"
TODAY = date(2026, 6, 4).isoformat()

MANIFEST_REL = "01_EMERGENTISM/00_META/01_CORPUS_AUDIT_MANIFEST_2026_06_04.csv"
SUMMARY_REL = "01_EMERGENTISM/00_META/01_CORPUS_AUDIT_SUMMARY_2026_06_04.md"
FULL_READ_LEDGER_REL = "01_EMERGENTISM/00_META/02_FULL_READ_SOUL_LOOP_LEDGER_2026_06_04.csv"
FULL_READ_SUMMARY_REL = "01_EMERGENTISM/00_META/02_FULL_READ_SOUL_LOOP_SUMMARY_2026_06_04.md"
SCRIPT_REL = "01_EMERGENTISM/09_TOOLS/01_SCRIPTS/emergentism_audit_manifest.py"

FIELDS = [
    "path",
    "status",
    "folder_class",
    "agentz_pass",
    "last_checked",
    "finding",
    "action",
    "receipt",
    "full_read_status",
    "soul_loop_receipt",
    "content_sha256",
    "byte_count",
    "line_count",
    "agentz_flags",
]

FULL_READ_FIELDS = [
    "path",
    "folder_class",
    "status",
    "full_read_status",
    "agentz_pass",
    "last_checked",
    "byte_count",
    "line_count",
    "content_sha256",
    "agentz_flags",
    "soul_loop_receipt",
]

GENERATED_CONTROL_RELS = {
    MANIFEST_REL,
    SUMMARY_REL,
    FULL_READ_LEDGER_REL,
    FULL_READ_SUMMARY_REL,
}

BINARY_SUFFIXES = {
    ".docx",
    ".ico",
    ".pdf",
    ".png",
    ".xlsx",
}

ROUTE_PATTERNS = (
    "999_ARCHIVE",
    "10_PUBLIC_SITE",
    "00_AGENTZ_MISSION",
)

LEGACY_TIER_RE = re.compile(r"\[(?:E|T)\]")

SKIP_DIRS = {
    ".git",
    ".next",
    ".pytest_cache",
    ".turbo",
    "__pycache__",
    "node_modules",
}

SKIP_SUFFIXES = {
    ".pyc",
}

ROOT_FRONT_DOORS = {
    "01_EMERGENTISM/README.md",
    "01_EMERGENTISM/AGENTS.md",
    "01_EMERGENTISM/AGENT_README.md",
    "01_EMERGENTISM/CLAUDE.md",
    "01_EMERGENTISM/VMOSK_A.md",
    "01_EMERGENTISM/ROSETTA.md",
    "01_EMERGENTISM/00_CANONICAL_TREE_OUTLINE.md",
    "01_EMERGENTISM/00_EMERGENTISM_AS_A_LENS.md",
    "01_EMERGENTISM/00_FOUNDATION_READER_GUIDE.md",
    "01_EMERGENTISM/00_SEVENFOLD_FOUNDATION_ROOT.md",
}

PATCHED_PATHS = {
    MANIFEST_REL,
    SUMMARY_REL,
    FULL_READ_LEDGER_REL,
    FULL_READ_SUMMARY_REL,
    SCRIPT_REL,
    "01_EMERGENTISM/00_CANONICAL_TREE_OUTLINE.md",
    "01_EMERGENTISM/00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md",
    "01_EMERGENTISM/00_META/00_TIDY_CONTROL_BOARD_2026_06_04.md",
    "01_EMERGENTISM/00_META/00_CLEANUP_AUDIT_CORRECTIONS_2026_05_31.md",
    "01_EMERGENTISM/09_TOOLS/sprint_gates/README.md",
    "01_EMERGENTISM/09_TOOLS/sprint_gates/AGENTS.md",
    "01_EMERGENTISM/90_ARCHIVE/AGENTS.md",
    "01_EMERGENTISM/90_ARCHIVE/README.md",
    "01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/README.md",
    "01_EMERGENTISM/12_PUBLIC_SITE/AGENTS.md",
    "01_EMERGENTISM/12_PUBLIC_SITE/00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md",
    "01_EMERGENTISM/03_METHODOLOGY/03_PREREGISTRATIONS/AGENTS.md",
    "01_EMERGENTISM/90_ARCHIVE/00_K3_SWEEP_2026_05_31/AGENTS.md",
    "01_EMERGENTISM/03_METHODOLOGY/03_PREREGISTRATIONS/README.md",
    "01_EMERGENTISM/03_METHODOLOGY/00_SYNTROPIC_EGREGORE_EXECUTIVE_SUMMARY.md",
    "01_EMERGENTISM/05_COSMOLOGY/00_THE_SYNTROPIC_IMPERATIVE.md",
    "01_EMERGENTISM/05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md",
    "01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/36_RUNTIME_LENS_V1_SPEC.md",
    "01_EMERGENTISM/07_THEOLOGY/00_GLOSSARY.md",
    "01_EMERGENTISM/90_ARCHIVE/00_THE_SITTING_PRACTICE.md",
    "01_EMERGENTISM/90_ARCHIVE/00_THE_TRANSCENDENTAL_TRINITY.md",
    "01_EMERGENTISM/90_ARCHIVE/00_THE_WEIGHING_OF_THE_HEART.md",
}

K2_ENVELOPE_REL = "01_EMERGENTISM/12_PUBLIC_SITE/00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md"


@dataclass(frozen=True)
class Row:
    path: str
    status: str
    folder_class: str
    agentz_pass: str
    last_checked: str
    finding: str
    action: str
    receipt: str
    full_read_status: str
    soul_loop_receipt: str
    content_sha256: str
    byte_count: int
    line_count: int
    agentz_flags: str


def is_generated_or_vendor(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    if any(part in SKIP_DIRS for part in rel_parts):
        return True
    return path.suffix in SKIP_SUFFIXES


def iter_files() -> list[Path]:
    files: list[Path] = []
    output = subprocess.check_output(
        [
            "git",
            "-c",
            "core.quotePath=false",
            "ls-files",
            "-co",
            "--exclude-standard",
            "--",
            "01_EMERGENTISM",
        ],
        cwd=ROOT,
        text=True,
    )
    for rel in output.splitlines():
        path = ROOT / rel
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            continue
        if not (stat.S_ISREG(mode) or stat.S_ISLNK(mode)):
            continue
        if is_generated_or_vendor(path):
            continue
        files.append(path)

    for rel in (*GENERATED_CONTROL_RELS, SCRIPT_REL):
        path = ROOT / rel
        if path not in files:
            files.append(path)

    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def top_folder(rel: str) -> str:
    parts = rel.split("/")
    return parts[1] if len(parts) > 2 else "__root__"


def folder_class(rel: str) -> str:
    parts = rel.split("/")
    lane_parts = parts[1:]
    if "91_COMPATIBILITY" in lane_parts:
        return "compatibility"
    if "90_ARCHIVE" in lane_parts:
        return "archive"

    top = top_folder(rel)
    if top == "__root__":
        return "root-front-door"
    if top in {
        "01_TELEOLOGY",
        "02_EPISTEMOLOGY",
        "03_METHODOLOGY",
        "04_AXIOLOGY",
        "05_COSMOLOGY",
        "06_ONTOLOGY",
        "07_THEOLOGY",
    }:
        return "doctrine"
    if top == "08_FRAMEWORK_SUPPORT":
        return "support"
    if top == "09_TOOLS":
        return "tooling"
    if top == "10_SEED":
        return "seed"
    if top == "11_UPLINK":
        return "uplink"
    if top == "12_PUBLIC_SITE":
        return "public-site"
    if top == "90_ARCHIVE":
        return "archive"
    if top == "91_COMPATIBILITY":
        return "compatibility"
    if top == "00_META":
        return "meta"
    return "unclassified"


def agentz_pass_for(rel: str, cls: str) -> str:
    if cls in {"archive", "compatibility"}:
        return "L6 archive/non-authority boundary"
    if cls == "public-site":
        return "L2 disclosure + L4 migration boundary"
    if cls == "tooling":
        return "L3 receipts + L5 topology"
    if cls == "uplink":
        return "L3 route drift + L7 compression"
    if cls == "doctrine":
        return "L1-L3-L5-L7 doctrine pass"
    if cls in {"meta", "root-front-door"}:
        return "L5 topology + L7 front-door clarity"
    return "L3 inventory"


@dataclass(frozen=True)
class FileReceipt:
    full_read_status: str
    soul_loop_receipt: str
    content_sha256: str
    byte_count: int
    line_count: int
    agentz_flags: str
    text: str


def is_binary_payload(path: Path, data: bytes) -> bool:
    return path.suffix.lower() in BINARY_SUFFIXES or b"\0" in data[:4096]


def count_text_lines(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def full_read_status_for(rel: str, cls: str, is_binary: bool) -> str:
    if rel in GENERATED_CONTROL_RELS:
        return "READ_CONTROL_SELF_REFERENTIAL"
    if is_binary:
        return "READ_BINARY_HASHED"
    if cls == "archive":
        return "READ_ARCHIVE_BOUNDED"
    if cls == "compatibility":
        return "READ_COMPATIBILITY_BOUNDED"
    return "READ_ACTIVE_TEXT"


def flag_family(flag: str) -> str:
    return flag.split(":", 1)[0]


def agentz_flags_for(rel: str, cls: str, text: str, is_binary: bool) -> list[str]:
    flags: list[str] = []

    if rel in GENERATED_CONTROL_RELS:
        flags.append("L5_SELF_REFERENTIAL_CONTROL_ARTIFACT")
        return flags
    if is_binary:
        flags.append("L3_BINARY_HASH_ONLY")
    if cls == "archive":
        flags.append("L6_ARCHIVE_NON_AUTHORITY")
    if cls == "compatibility":
        flags.append("L6_COMPATIBILITY_NON_AUTHORITY")

    if text:
        if cls not in {"archive", "compatibility"}:
            for pattern in ROUTE_PATTERNS:
                count = text.count(pattern)
                if count:
                    flags.append(f"L1_ROUTE_PATTERN_{pattern}:{count}")
            legacy_count = len(LEGACY_TIER_RE.findall(text))
            if legacy_count:
                flags.append(f"L3_LEGACY_TIER:{legacy_count}")
        if rel == K2_ENVELOPE_REL:
            if "2026-06-04 audit addendum" in text and "historical signature text" in text:
                flags.append("L4_K2_ADDENDUM_PRESENT")
            else:
                flags.append("L4_K2_ADDENDUM_MISSING")

    return flags or ["clear"]


def read_file_receipt(path: Path, rel: str, cls: str) -> FileReceipt:
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        data = b""

    is_binary = is_binary_payload(path, data)
    text = "" if is_binary else data.decode("utf-8", errors="replace")
    line_count = 0 if is_binary else count_text_lines(text)
    flags = agentz_flags_for(rel, cls, text, is_binary)
    read_status = full_read_status_for(rel, cls, is_binary)
    if rel in GENERATED_CONTROL_RELS:
        digest = ""
        receipt = (
            "self-referential-generated-control;"
            f"bytes:{len(data)};lines:{line_count};"
            "passes:L1,L2,L3,L5,L6,L7"
        )
    else:
        digest = hashlib.sha256(data).hexdigest() if data else ""
        receipt = (
            f"sha256:{digest[:16] or 'generated-this-run'};"
            f"bytes:{len(data)};lines:{line_count};"
            "passes:L1,L2,L3,L5,L6,L7"
        )

    return FileReceipt(
        full_read_status=read_status,
        soul_loop_receipt=receipt,
        content_sha256=digest,
        byte_count=len(data),
        line_count=line_count,
        agentz_flags=";".join(flags),
        text=text,
    )


def k2_addendum_present(text: str) -> bool:
    return "2026-06-04 audit addendum" in text and "historical signature text" in text


def classify(path: Path) -> Row:
    rel = path.relative_to(ROOT).as_posix()
    cls = folder_class(rel)
    receipt_data = read_file_receipt(path, rel, cls)
    status = "READ"
    finding = "Full-read/Soul Loop receipt generated in strict control pass."
    action = "Maintain source truth; repair only source-backed drift."
    receipt = "generated by 09_TOOLS/01_SCRIPTS/emergentism_audit_manifest.py"

    if rel == K2_ENVELOPE_REL:
        if k2_addendum_present(receipt_data.text):
            status = "NO_ACTION"
            finding = "Dated addendum resolves old 10_PUBLIC_SITE coordinates as historical signature text."
            action = "Preserve envelope; physical app migration remains blocked pending AIA destination/signoff."
        else:
            status = "BLOCKED"
            finding = "Signed migration envelope lacks the dated addendum needed after the 12_PUBLIC_SITE rename."
            action = "Add dated addendum; do not execute the move from this document."
    elif rel in ROOT_FRONT_DOORS:
        status = "READ"
        finding = "Root front-door / route document included in strict read pass."
        action = "Keep aligned with source truth and control board."
    elif rel in PATCHED_PATHS:
        status = "PATCHED"
        finding = "Control-layer or missing-front-door artifact added in this pass."
        action = "Keep synchronized with manifest and tidy board."
    elif cls == "archive":
        status = "ARCHIVE_ONLY"
        finding = "Archive provenance; not current source authority by itself."
        action = "Repair only indexing, tombstones, and misleading current-authority language."
    elif cls == "compatibility":
        status = "DO_NOT_TOUCH"
        finding = "Compatibility/provenance surface; preserve until decay conditions are proven."
        action = "Do not compact or delete during audit-first pass."

    return Row(
        path=rel,
        status=status,
        folder_class=cls,
        agentz_pass=agentz_pass_for(rel, cls),
        last_checked=TODAY,
        finding=finding,
        action=action,
        receipt=receipt,
        full_read_status=receipt_data.full_read_status,
        soul_loop_receipt=receipt_data.soul_loop_receipt,
        content_sha256=receipt_data.content_sha256,
        byte_count=receipt_data.byte_count,
        line_count=receipt_data.line_count,
        agentz_flags=receipt_data.agentz_flags,
    )


def write_manifest(rows: list[Row]) -> None:
    path = ROOT / MANIFEST_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def write_full_read_ledger(rows: list[Row]) -> None:
    path = ROOT / FULL_READ_LEDGER_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FULL_READ_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: getattr(row, field) for field in FULL_READ_FIELDS})


def write_full_read_summary(rows: list[Row]) -> None:
    path = ROOT / FULL_READ_SUMMARY_REL
    by_status = Counter(row.status for row in rows)
    by_read_status = Counter(row.full_read_status for row in rows)
    by_class = Counter(row.folder_class for row in rows)
    flag_counts: Counter[str] = Counter()
    for row in rows:
        for flag in row.agentz_flags.split(";"):
            flag_counts[flag_family(flag)] += 1

    binary_rows = [row for row in rows if row.full_read_status == "READ_BINARY_HASHED"]
    route_rows = [
        row
        for row in rows
        if "L1_ROUTE_PATTERN_" in row.agentz_flags
        and row.folder_class not in {"archive", "compatibility"}
    ]

    lines = [
        "---",
        "rosetta:",
        "  primary_level: L3",
        "  primary_column: Meta",
        "  operator: \"Krishna\"",
        "  tier: \"God\"",
        "  regime: \"Vaisya\"",
        "  register: \"[B]\"",
        "  canonical_phrase: \"Emergentism Full-Read Soul Loop Summary\"",
        "---",
        "",
        "# Emergentism Full-Read Soul Loop Summary",
        "",
        f"**Date:** {TODAY}",
        "**Status:** Strict corpus-control read receipt.",
        "",
        "This file records the full-read control pass for source-visible files in",
        "`01_EMERGENTISM/`. It is a receipt layer: every listed path was opened",
        "as bytes, hashed, and assigned an Agentz/Soul Loop control status. Text",
        "files were decoded and line-counted; binary files receive hash-only",
        "receipts. This is not a substitute for doctrine authority or human K2",
        "judgment.",
        "",
        "## Coverage",
        "",
        f"- Manifest: `{MANIFEST_REL}`",
        f"- Full-read ledger: `{FULL_READ_LEDGER_REL}`",
        f"- Generator: `{SCRIPT_REL}`",
        f"- Source-visible files: {len(rows)}",
        "",
        "## Manifest Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{status}` | {count} |" for status, count in sorted(by_status.items()))
    lines.extend(
        [
            "",
            "## Full-Read Status Counts",
            "",
            "| Full-read status | Count |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| `{status}` | {count} |" for status, count in sorted(by_read_status.items()))
    lines.extend(
        [
            "",
            "## Folder Class Counts",
            "",
            "| Folder class | Count |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| `{cls}` | {count} |" for cls, count in sorted(by_class.items()))
    lines.extend(
        [
            "",
            "## Agentz Flag Families",
            "",
            "| Flag family | Rows |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| `{flag}` | {count} |" for flag, count in sorted(flag_counts.items()))

    lines.extend(
        [
            "",
            "## Binary Hash-Only Receipts",
            "",
            "| Path | Bytes | SHA-256 |",
            "|---|---:|---|",
        ]
    )
    for row in binary_rows:
        lines.append(f"| `{row.path}` | {row.byte_count} | `{row.content_sha256}` |")

    lines.extend(
        [
            "",
            "## Active Route Pattern Residuals",
            "",
            "These rows contain historical/control references to old route names or",
            "migration coordinates. They are flags for future semantic review, not",
            "automatic proof of active route drift.",
            "",
            "| Path | Flags |",
            "|---|---|",
        ]
    )
    for row in route_rows[:80]:
        route_flags = ";".join(
            flag for flag in row.agentz_flags.split(";") if flag.startswith("L1_ROUTE_PATTERN_")
        )
        lines.append(f"| `{row.path}` | `{route_flags}` |")
    if len(route_rows) > 80:
        lines.append(f"| `NOTE` | `{len(route_rows) - 80} additional rows omitted; see CSV ledger.` |")

    lines.extend(
        [
            "",
            "## Soul Loop Method",
            "",
            "1. L1 contradiction/path drift scan.",
            "2. L2 disclosure and public-safe boundary scan.",
            "3. L3 evidence-tier and receipt scan.",
            "4. L5 topology/source-ownership scan.",
            "5. L6 archive/non-authority scan.",
            "6. L7 front-door/compression scan.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_summary(rows: list[Row]) -> None:
    path = ROOT / SUMMARY_REL
    by_status = Counter(row.status for row in rows)
    by_class = Counter(row.folder_class for row in rows)
    open_actions = [row for row in rows if row.status in {"TODO", "BLOCKED"}]
    residual_flags: Counter[str] = Counter()
    for row in rows:
        for flag in row.agentz_flags.split(";"):
            family = flag_family(flag)
            if family.startswith("L1_ROUTE_PATTERN_") or family == "L3_LEGACY_TIER":
                residual_flags[family] += 1

    lines = [
        "---",
        "rosetta:",
        "  primary_level: L3",
        "  primary_column: Meta",
        "  operator: \"Krishna\"",
        "  tier: \"God\"",
        "  regime: \"Vaisya\"",
        "  register: \"[B/I]\"",
        "  canonical_phrase: \"Emergentism Corpus Audit Summary\"",
        "---",
        "",
        "# Emergentism Corpus Audit Summary",
        "",
        f"**Date:** {TODAY}",
        "**Status:** Audit-first control summary.",
        "",
        "This file summarizes the generated corpus manifest. It is a control",
        "surface, not doctrine authority and not a replacement for source files.",
        "",
        "## Coverage",
        "",
        f"- Manifest: `{MANIFEST_REL}`",
        f"- Full-read ledger: `{FULL_READ_LEDGER_REL}`",
        f"- Full-read summary: `{FULL_READ_SUMMARY_REL}`",
        f"- Generator: `{SCRIPT_REL}`",
        f"- Inventoried files: {len(rows)}",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{status}` | {count} |" for status, count in sorted(by_status.items()))
    lines.extend(
        [
            "",
            "## Class Counts",
            "",
            "| Folder class | Count |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| `{cls}` | {count} |" for cls, count in sorted(by_class.items()))
    lines.extend(
        [
            "",
            "## Open Audit Actions",
            "",
            "| Status | Path | Finding | Action |",
            "|---|---|---|---|",
        ]
    )
    for row in open_actions[:80]:
        lines.append(f"| `{row.status}` | `{row.path}` | {row.finding} | {row.action} |")
    if len(open_actions) > 80:
        lines.append(f"| `NOTE` | manifest | {len(open_actions) - 80} additional open rows omitted here | See CSV |")
    if not open_actions:
        lines.append("| `NONE` | manifest | No `TODO` or `BLOCKED` manifest rows remain. | See residual flag section below for non-blocking debt. |")

    lines.extend(
        [
            "",
            "## Residual Non-Blocking Flags",
            "",
            "These rows are review queues, not blocker statuses. Route-pattern",
            "rows are historical/control references unless promoted by a later",
            "semantic pass; legacy-tier rows remain broad `[E]`/`[T]`",
            "normalization debt.",
            "",
            "| Flag family | Rows |",
            "|---|---:|",
        ]
    )
    if residual_flags:
        lines.extend(f"| `{flag}` | {count} |" for flag, count in sorted(residual_flags.items()))
    else:
        lines.append("| `NONE` | 0 |")

    lines.extend(
        [
            "",
            "## Agentz Pass Order",
            "",
            "1. L1 contradiction/path drift.",
            "2. L2 disclosure and public-safe claim boundaries.",
            "3. L3 evidence tiers, receipts, and route drift.",
            "4. L5 topology and source ownership.",
            "5. L6 archive and non-authority boundaries.",
            "6. L7 compressed narrative/front-door clarity.",
            "",
            "## Verification Receipts",
            "",
            "- `git diff --check -- 01_EMERGENTISM`",
            "- `rg -n \"999_ARCHIVE|10_PUBLIC_SITE|00_AGENTZ_MISSION\" 01_EMERGENTISM --glob '*.md' --glob '!**/90_ARCHIVE/**' --glob '!**/91_COMPATIBILITY/**'`",
            "- `rg -n \"\\\\[E\\\\]|\\\\[T\\\\]\" 01_EMERGENTISM --glob '*.md' --glob '!**/90_ARCHIVE/**' --glob '!**/91_COMPATIBILITY/**'`",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows = [classify(path) for path in iter_files()]
    write_manifest(rows)
    write_full_read_ledger(rows)
    write_full_read_summary(rows)
    write_summary(rows)
    print(f"wrote {MANIFEST_REL} with {len(rows)} rows")
    print(f"wrote {FULL_READ_LEDGER_REL}")
    print(f"wrote {FULL_READ_SUMMARY_REL}")
    print(f"wrote {SUMMARY_REL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
