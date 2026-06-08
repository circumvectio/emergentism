#!/usr/bin/env python3
"""rosetta_propose.py — Charioteer scaffold that proposes Rosetta annotations.

Companion to ``rosetta_annotate.py``:

    propose → review → apply
    -------   ------   -----
    rosetta_propose.py      (this tool; emits proposals)
    warrior human pass      (edit the proposal JSON/JSONL in place)
    rosetta_annotate.py apply-manifest --write  (writes proposals into files)

Three operating modes:

  1. ``heuristic``    — deterministic file-path + title heuristics only.
                        Offline, no LLM. Suitable when L-folder containment
                        + keyword match is sufficient (Tier A / B).
  2. ``prompt``       — emits the per-file LLM prompt per packet 157 §7 to
                        stdout, ready for paste into an external LLM.
  3. ``manifest``     — writes a JSON manifest the existing apply-manifest
                        command can consume directly.

Key discipline
--------------
This tool PROPOSES ONLY. It never writes frontmatter into target files.
That lane belongs to ``rosetta_annotate.py apply-manifest --write``, which
acts on a human-reviewed manifest — matching packet 157 §10:

    "Does NOT execute annotation (charioteer lane restriction; warrior runs
    the passes)"

References
----------
- packet 157: Rosetta Annotation Strategy (spec)
- packet 158: Phase 2c Receipt and Tier A Gate (scope discipline)
- packet 159: Tier A Rosetta Draft Pack (example output format)
- 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_annotate.py: warrior apply + audit companion
- 01_EMERGENTISM/11_UPLINK/06_AGENTS.md: operator / tier / regime per L-level
"""

from __future__ import annotations

import argparse
import glob as _glob
import json
import re
import sys
from pathlib import Path


# ---
# L-folder → level/operator/tier/regime defaults (packet 159 §1 + 06_AGENTS)
# ---
L_FOLDER_DEFAULTS: dict[str, dict[str, str]] = {
    "01_TELEOLOGY":    {"level": "L1", "operator": "Kali 🎲",  "tier": "Demon", "regime": "Caṇḍāla"},
    "02_EPISTEMOLOGY": {"level": "L2", "operator": "Kālī 💀",  "tier": "God",   "regime": "Śūdra"},
    "03_METHODOLOGY":  {"level": "L3", "operator": "Kṛṣṇa ◇",  "tier": "God",   "regime": "Vaiśya"},
    "04_AXIOLOGY":     {"level": "L4", "operator": "Arjuna ⚔", "tier": "God",   "regime": "Kṣatriya"},
    "05_COSMOLOGY":    {"level": "L5", "operator": "Brahmā ○", "tier": "Executive", "regime": "Brāhmaṇa"},
    "06_ONTOLOGY":     {"level": "L6", "operator": "Śiva •",   "tier": "Executive", "regime": "Sādhu"},
    "07_THEOLOGY":     {"level": "L7", "operator": "Viṣṇu ⊙",  "tier": "Executive", "regime": "Ṛṣi"},
}

# ---
# Canonical columns accepted by rosetta_annotate.py
# ---
VALID_COLUMNS = {
    "Trivium (Grammar/Logic/Rhetoric -> Quadrivium)",
    "Psychology",
    "Philosophy",
    "Political regime",
    "Yoga",
    "Chakra",
    "Mythology",
    "Neuroscience",
    "Computation",
    "Game theory",
    "Civilisational stage",
    "Operator pathology season + DSM",
    "Asura return",
    "Liberal art",
    "PIE roots",
    "Meta",
}

# ---
# Keyword heuristics for primary_column inference (first match wins)
# ---
COLUMN_KEYWORDS: list[tuple[re.Pattern[str], str]] = [
    # Meta first — filename-level signals ("known unknowns", "audit report",
    # "remaining questions", "reconciliation scope") are strong cross-cutting
    # flags and should beat incidental "logic"/"rhetoric" hits.
    (re.compile(r"(?i)\b(known\s*unknowns|audit[_\s]report|remaining[_\s]questions|reconciliation[_\s]scope|what[_\s]is[_\s]actually[_\s]novel|d[_\s]level[_\s]studies|d[_\s]scaffold|corpus[_\s]map|meta)\b"), "Meta"),
    # Yoga next — "sitting practice", "pratyakṣa", "bindu", "aum" must beat
    # Neuroscience hits when a yoga file happens to mention the brain.
    (re.compile(r"(?i)\b(sitting\s*practice|pratyak|yoga|chakra|samādhi|samadhi|bhakti|karma\s*yoga|jñāna|jnana|rāja|raja\s*yoga|sannyāsa|sannyasa|tantra|bindu|aum|meditation)\b"), "Yoga"),
    # Mythology before Neuroscience — the Egyptian/Greek/etc. source files
    # often discuss brain-as-symbol too.
    (re.compile(r"(?i)\b(egypt|greek|norse|sumer|tarot|jung|ring\s*that|ouroboros|tolkien|weighing\s*of\s*the\s*heart)\b"), "Mythology"),
    (re.compile(r"(?i)\b(neuro|cortex|hemisphere|corpus\s*callosum|DMN|TPN|brain\s+is\s+the)\b"), "Neuroscience"),
    (re.compile(r"(?i)\b(MDL|minimal\s*description\s*length|ternary|bitnet|computational\s*sphere|optimizer\s+algorithm)\b"), "Computation"),
    (re.compile(r"(?i)\b(game\s*theory|behavioral\s*economics|nash\s*equilibrium|payoff\s*matrix|tit[_\s]for[_\s]tat)\b"), "Game theory"),
    (re.compile(r"(?i)\b(piaget|kohlberg|maslow|virtue|shadow|metamorphoses?|pedagogy[_\s]of)\b"), "Psychology"),
    (re.compile(r"(?i)\b(plato|tyranny|democracy|oligarch|timocracy|aristocracy|theocracy|anarchy|political\s*regime)\b"), "Political regime"),
    (re.compile(r"(?i)\b(PIE\s*root|etymology|anmut|demut|brahman\s*as\s*ground|ṛta|asha)\b"), "PIE roots"),
    (re.compile(r"(?i)\b(trivium|quadrivium|liberal\s*art)\b"), "Liberal art"),
]

ROOT = Path(__file__).resolve().parents[3]
FOUNDATION = ROOT / "01_EMERGENTISM"
if not FOUNDATION.exists():
    FOUNDATION = ROOT / "EMERGENTISM_ORG"
FOUNDATION_REL = FOUNDATION.relative_to(ROOT).as_posix()

COMPAT_ROOT_PATTERNS = (
    re.compile(rf"^{re.escape(FOUNDATION_REL)}/00_.*\.md$"),
    re.compile(rf"^{re.escape(FOUNDATION_REL)}/_AUDIT_REPORT_2026_04_21\.md$"),
)

COMPAT_DIR_PREFIXES = (
    f"{FOUNDATION_REL}/01_FORMAL_SYSTEM/",
    f"{FOUNDATION_REL}/02_THE_DERIVATION/",
    f"{FOUNDATION_REL}/03_THE_PAPERS/",
    f"{FOUNDATION_REL}/00_THE_TRANSCENDENTAL_TRINITY/",
)


class ProposeError(Exception):
    """User-facing tool error."""


# ---
# File helpers
# ---
def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    try:
        path.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise ProposeError(f"path escapes repo: {value}") from exc
    return path


def is_compat_surface(path: Path) -> bool:
    rel_path = rel(path)
    if rel_path == f"{FOUNDATION_REL}/00_SEVENFOLD_FOUNDATION_ROOT.md":
        return False
    if any(pattern.match(rel_path) for pattern in COMPAT_ROOT_PATTERNS):
        return True
    return rel_path.startswith(COMPAT_DIR_PREFIXES)


def tier_a_targets() -> list[Path]:
    files: list[Path] = []
    for folder in L_FOLDER_DEFAULTS:
        root = FOUNDATION / folder
        if not root.exists():
            continue
        files.extend(
            sorted(
                p
                for p in root.glob("*.md")
                if p.name != "README.md" and not is_compat_surface(p)
            )
        )
    return files


def read_head(path: Path, n: int = 2000) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(n)
    except (IOError, OSError) as exc:
        raise ProposeError(f"read failed {path}: {exc}") from exc


def detect_l_folder(path: Path) -> str | None:
    """Return L-folder name if path lives under one of the 7 canonical homes."""
    try:
        rel = path.resolve().relative_to(FOUNDATION)
    except ValueError:
        return None
    parts = rel.parts
    if not parts:
        return None
    return parts[0] if parts[0] in L_FOLDER_DEFAULTS else None


def detect_meta(path: Path) -> bool:
    try:
        rel = path.resolve().relative_to(FOUNDATION)
    except ValueError:
        return False
    return bool(rel.parts) and rel.parts[0] == "00_META"


def extract_title(head: str, fallback: str) -> str:
    for line in head.splitlines()[:40]:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("# ").strip()
    return fallback


def extract_register(head: str) -> str | None:
    """Pull an existing [E/S/I/C] evidence tier if declared in the header.

    Returns just the tier marker (e.g. "[S/I]") — not the surrounding prose.
    """
    patterns = [
        r"evidence[_ ]?tier[:\"\s]*[`\"']?(\[[ESIC/]+\])",
        r"\*\*Evidence Tier:\*\*\s*`?(\[[ESIC/]+\])",
        r"register[:\s]*[\"']?(\[[ESIC/]+\])",
        r"^\s*register[:\s]*(\[[ESIC/]+\])",
    ]
    for pat in patterns:
        m = re.search(pat, head, re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip().strip("'\"`")
    return None


def propose_primary_column(title: str, head: str) -> str:
    haystack = f"{title}\n{head}"
    for pat, col in COLUMN_KEYWORDS:
        if pat.search(haystack):
            return col
    return "Philosophy"


def canonical_phrase(title: str) -> str:
    s = title
    s = re.sub(r"^THE\s+", "", s, flags=re.IGNORECASE)
    return s.title() if s.isupper() else s.strip()


# ---
# Proposal construction
# ---
def propose_block(path: Path) -> dict:
    """Return a {primary_level, primary_column, operator, ...} dict."""
    head = read_head(path)
    title = extract_title(head, path.stem.replace("_", " "))
    register = extract_register(head) or "[S/I]"
    column = propose_primary_column(title, head)
    block: dict = {
        "primary_column": column,
        "register": register,
        "canonical_phrase": canonical_phrase(title),
    }

    if detect_meta(path):
        # META: primary_level intentionally omitted per packet 158 §6
        block["primary_column"] = "Meta" if column == "Meta" else column
        return block

    lf = detect_l_folder(path)
    if lf:
        defaults = L_FOLDER_DEFAULTS[lf]
        block["primary_level"] = defaults["level"]
        block["operator"] = defaults["operator"]
        block["tier"] = defaults["tier"]
        block["regime"] = defaults["regime"]
    return block


def validate_block(block: dict) -> None:
    col = block.get("primary_column")
    if col and col not in VALID_COLUMNS:
        raise ProposeError(f"invalid primary_column: {col}")
    lvl = block.get("primary_level")
    if lvl and lvl not in {f"L{i}" for i in range(1, 8)}:
        raise ProposeError(f"invalid primary_level: {lvl}")


def format_yaml_block(block: dict) -> str:
    order = [
        "primary_level", "primary_column", "operator",
        "tier", "regime", "register", "canonical_phrase",
    ]
    lines = ["rosetta:"]
    for key in order:
        if key in block:
            val = block[key]
            if isinstance(val, str):
                val = json.dumps(val, ensure_ascii=False)
            lines.append(f"  {key}: {val}")
    return "\n".join(lines)


# ---
# LLM prompt template (packet 157 §7)
# ---
LLM_PROMPT_TEMPLATE = """\
Read this document. Based on its content, propose a Rosetta annotation in YAML
frontmatter format per packet 157 §2 spec. Output only the `rosetta:` YAML
block. Use canonical column names from packet 157 §3. Identify primary L-level
(L1-L7), primary column, optional secondary cross-refs, evidence tier
[E/S/I/C], and (if clear) operator + tier + regime + canonical phrase. If
uncertain about any field, omit it rather than guess.

Canonical columns: Philosophy, Neuroscience, Computation, Game theory,
Political regime, Mythology, Psychology, Yoga, PIE roots, Liberal art, Meta.

L-level operator/tier/regime defaults:
  L1 Teleology    → Kali 🎲 / Demon / Caṇḍāla
  L2 Epistemology → Kālī 💀 / God / Śūdra
  L3 Methodology  → Kṛṣṇa ◇ / God / Vaiśya
  L4 Axiology     → Arjuna ⚔ / God / Kṣatriya
  L5 Cosmology    → Brahmā ○ / Executive / Brāhmaṇa
  L6 Ontology     → Śiva • / Executive / Sādhu
  L7 Theology     → Viṣṇu ⊙ / Executive / Ṛṣi

Document path: {path}

Document head (first 2000 chars):
---
{head}
---
"""


def build_prompt(path: Path) -> str:
    return LLM_PROMPT_TEMPLATE.format(path=rel(path), head=read_head(path))


# ---
# Target resolution
# ---
def expand_glob(pattern: str) -> list[Path]:
    raw_pattern = pattern if Path(pattern).is_absolute() else str(ROOT / pattern)
    return [resolve_repo_path(match) for match in sorted(_glob.glob(raw_pattern, recursive=True))]


def resolve_targets(
    target_args: list[str],
    *,
    tier_a: bool = False,
    include_compat: bool = False,
) -> list[Path]:
    out: list[Path] = []
    if tier_a:
        out.extend(tier_a_targets())
    for t in target_args:
        if t.startswith("glob:"):
            out.extend(expand_glob(t[len("glob:"):]))
        else:
            out.append(resolve_repo_path(t))

    resolved: list[Path] = []
    seen: set[str] = set()
    for path in out:
        if not path.is_file() or path.suffix != ".md":
            continue
        if not include_compat and is_compat_surface(path):
            continue
        key = rel(path)
        if key in seen:
            continue
        seen.add(key)
        resolved.append(path)
    return sorted(resolved, key=rel)


# ---
# Command handlers
# ---
def command_heuristic(args: argparse.Namespace) -> int:
    targets = resolve_targets(
        args.targets,
        tier_a=args.tier_a,
        include_compat=args.include_compat,
    )
    if not targets:
        print("No target markdown files resolved.", file=sys.stderr)
        return 1
    for path in targets:
        block = propose_block(path)
        validate_block(block)
        print(f"# {rel(path)}")
        print("```yaml")
        print(format_yaml_block(block))
        print("```")
        print()
    return 0


def command_prompt(args: argparse.Namespace) -> int:
    targets = resolve_targets(
        args.targets,
        tier_a=args.tier_a,
        include_compat=args.include_compat,
    )
    if not targets:
        print("No target markdown files resolved.", file=sys.stderr)
        return 1
    for path in targets:
        print(f"# ===== prompt for {rel(path)} =====")
        print(build_prompt(path))
        print()
    return 0


def command_manifest(args: argparse.Namespace) -> int:
    targets = resolve_targets(
        args.targets,
        tier_a=args.tier_a,
        include_compat=args.include_compat,
    )
    if not targets:
        print("No target markdown files resolved.", file=sys.stderr)
        return 1

    entries: list[dict] = []
    for path in targets:
        block = propose_block(path)
        validate_block(block)
        entries.append({"path": rel(path), "rosetta": block})

    if args.format == "jsonl":
        out_text = "\n".join(json.dumps(e, ensure_ascii=False) for e in entries)
    else:
        out_text = json.dumps({"entries": entries}, ensure_ascii=False, indent=2)

    if args.out:
        out_path = resolve_repo_path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text + ("\n" if not out_text.endswith("\n") else ""), encoding="utf-8")
        print(f"Wrote {len(entries)} proposals to {rel(out_path)}", file=sys.stderr)
    else:
        sys.stdout.write(out_text)
        sys.stdout.write("\n")
    return 0


# ---
# CLI
# ---
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_h = sub.add_parser("heuristic", help="print per-file YAML proposals (offline heuristics)")
    p_h.add_argument("targets", nargs="*", help="files or 'glob:<pattern>'")
    p_h.add_argument("--tier-a", action="store_true", help="use packet-159 Tier A targets")
    p_h.add_argument("--include-compat", action="store_true", help="include compatibility stubs")
    p_h.set_defaults(func=command_heuristic)

    p_p = sub.add_parser("prompt", help="emit per-file LLM prompts (packet 157 §7)")
    p_p.add_argument("targets", nargs="*", help="files or 'glob:<pattern>'")
    p_p.add_argument("--tier-a", action="store_true", help="use packet-159 Tier A targets")
    p_p.add_argument("--include-compat", action="store_true", help="include compatibility stubs")
    p_p.set_defaults(func=command_prompt)

    p_m = sub.add_parser(
        "manifest",
        help="write JSON/JSONL manifest consumable by rosetta_annotate.py apply-manifest",
    )
    p_m.add_argument("targets", nargs="*", help="files or 'glob:<pattern>'")
    p_m.add_argument("--out", help="output file (stdout if omitted)")
    p_m.add_argument("--format", choices=["json", "jsonl"], default="json")
    p_m.add_argument("--tier-a", action="store_true", help="use packet-159 Tier A targets")
    p_m.add_argument("--include-compat", action="store_true", help="include compatibility stubs")
    p_m.set_defaults(func=command_manifest)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "targets") and not args.targets and not getattr(args, "tier_a", False):
        parser.error(f"{args.command} requires --tier-a or at least one target")
    try:
        return args.func(args)
    except ProposeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
