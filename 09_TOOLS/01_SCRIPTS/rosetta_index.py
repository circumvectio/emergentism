#!/usr/bin/env python3
"""Build a navigational index from Rosetta frontmatter.

Read-only by default. The script scans markdown files, extracts the ``rosetta:``
frontmatter block, and emits either Markdown or JSON. Use ``--output`` when you
want to write the generated index to disk.

Examples:
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_index.py --tier-a
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_index.py --paths 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_FOUNDATIONS --format json
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_index.py --tier-a --include-missing --output /tmp/rosetta_index.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
FOUNDATION = ROOT / "01_EMERGENTISM"
if not FOUNDATION.exists():
    FOUNDATION = ROOT / "EMERGENTISM_ORG"
FOUNDATION_REL = FOUNDATION.relative_to(ROOT).as_posix()

LEVEL_ORDER = [f"L{i}" for i in range(1, 8)]
LEVEL_NAMES = {
    "L1": "Teleology",
    "L2": "Epistemology",
    "L3": "Methodology",
    "L4": "Axiology",
    "L5": "Cosmology",
    "L6": "Ontology",
    "L7": "Theology",
}

LEVEL_FOLDERS = {
    "01_TELEOLOGY": "L1",
    "02_EPISTEMOLOGY": "L2",
    "03_METHODOLOGY": "L3",
    "04_AXIOLOGY": "L4",
    "05_COSMOLOGY": "L5",
    "06_ONTOLOGY": "L6",
    "07_THEOLOGY": "L7",
}

SKIP_DIRS = {
    ".git",
    ".next",
    ".venv",
    ".venv_proof",
    "__pycache__",
    "node_modules",
    "dist",
}

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


@dataclass
class RosettaEntry:
    path: str
    title: str
    primary_level: str | None
    primary_column: str | None
    register: str | None
    operator: str | None
    tier: str | None
    regime: str | None
    canonical_phrase: str | None
    secondary_count: int


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    try:
        path.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"path escapes repo: {value}") from exc
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
    for folder in LEVEL_FOLDERS:
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


def iter_markdown(paths: Iterable[Path], *, include_compat: bool = False) -> Iterable[Path]:
    for start in paths:
        if not start.exists():
            continue
        if start.is_file():
            if start.suffix == ".md" and (include_compat or not is_compat_surface(start)):
                yield start
            continue

        for path in start.rglob("*.md"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if not include_compat and is_compat_surface(path):
                continue
            yield path


def split_frontmatter(content: str) -> tuple[str | None, str]:
    if not content.startswith("---\n"):
        return None, content
    end = content.find("\n---\n", 4)
    if end == -1:
        return None, content
    return content[4:end], content[end + 5 :]


def extract_title(content: str, path: Path) -> str:
    _, body = split_frontmatter(content)
    for line in body.splitlines()[:60]:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("# ").strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def extract_rosetta_block(frontmatter: str | None) -> str | None:
    if frontmatter is None:
        return None
    match = re.search(r"(?ms)^rosetta:\n(?P<body>(?:  .*\n?)+)", frontmatter)
    if not match:
        return None
    body = match.group("body")
    # Stop at the next unindented key if the regex captured too much.
    stop = re.search(r"(?m)^[A-Za-z0-9_-]+:", body)
    if stop:
        body = body[: stop.start()]
    return "rosetta:\n" + body.rstrip()


def scalar(block: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s+{re.escape(key)}:\s*(.+?)\s*$", block)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] in {"'", '"'} and value[-1] == value[0]:
        value = value[1:-1]
    return value


def secondary_count(block: str) -> int:
    return len(re.findall(r"(?m)^\s+-\s+level:\s+L[1-7]\s*$", block))


def parse_entry(path: Path) -> RosettaEntry | None:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    frontmatter, _ = split_frontmatter(content)
    block = extract_rosetta_block(frontmatter)
    if block is None:
        return None
    return RosettaEntry(
        path=rel(path),
        title=extract_title(content, path),
        primary_level=scalar(block, "primary_level"),
        primary_column=scalar(block, "primary_column"),
        register=scalar(block, "register"),
        operator=scalar(block, "operator"),
        tier=scalar(block, "tier"),
        regime=scalar(block, "regime"),
        canonical_phrase=scalar(block, "canonical_phrase"),
        secondary_count=secondary_count(block),
    )


def collect_missing(paths: Iterable[Path], *, include_compat: bool = False) -> list[str]:
    missing: list[str] = []
    for path in iter_markdown(paths, include_compat=include_compat):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        frontmatter, _ = split_frontmatter(content)
        if extract_rosetta_block(frontmatter) is None:
            missing.append(rel(path))
    return sorted(set(missing))


def render_markdown(entries: list[RosettaEntry], missing: list[str]) -> str:
    by_level: dict[str, list[RosettaEntry]] = defaultdict(list)
    by_column: dict[str, list[RosettaEntry]] = defaultdict(list)
    for entry in entries:
        by_level[entry.primary_level or "UNSET"].append(entry)
        by_column[entry.primary_column or "UNSET"].append(entry)

    lines = [
        "# Rosetta Index",
        "",
        "Generated from `rosetta:` frontmatter. This is a navigation surface, not a doctrine authority.",
        "",
        f"Annotated files: {len(entries)}",
        f"Missing annotations: {len(missing)}",
        "",
        "## By L-Level",
        "",
    ]

    for level in LEVEL_ORDER + sorted(k for k in by_level if k not in LEVEL_ORDER):
        rows = sorted(by_level.get(level, []), key=lambda e: e.path)
        if not rows:
            continue
        label = LEVEL_NAMES.get(level, "Unspecified")
        lines.extend([f"### {level} — {label}", ""])
        for entry in rows:
            column = entry.primary_column or "UNSET"
            register = f" {entry.register}" if entry.register else ""
            lines.append(f"- [{entry.title}]({entry.path}) — {column}{register}")
        lines.append("")

    lines.extend(["## By Column", ""])
    for column in sorted(by_column):
        rows = sorted(by_column[column], key=lambda e: (e.primary_level or "", e.path))
        lines.extend([f"### {column}", ""])
        for entry in rows:
            level = entry.primary_level or "UNSET"
            lines.append(f"- `{level}` [{entry.title}]({entry.path})")
        lines.append("")

    if missing:
        lines.extend(["## Missing Rosetta Frontmatter", ""])
        for path in missing:
            lines.append(f"- `{path}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_json(entries: list[RosettaEntry], missing: list[str]) -> str:
    payload = {
        "entry_count": len(entries),
        "missing_count": len(missing),
        "entries": [asdict(entry) for entry in sorted(entries, key=lambda e: e.path)],
        "missing": missing,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier-a", action="store_true", help="scan packet-159 Tier A targets")
    parser.add_argument(
        "--paths",
        nargs="*",
        default=[],
        help="repo-relative files or directories to scan",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="output format",
    )
    parser.add_argument("--output", help="optional repo-relative or absolute output path")
    parser.add_argument("--include-missing", action="store_true", help="include missing files")
    parser.add_argument("--include-compat", action="store_true", help="include compatibility stubs")
    parser.add_argument("--fail-missing", action="store_true", help="exit nonzero if missing files exist")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.tier_a and not args.paths:
        print("error: provide --tier-a or --paths", file=sys.stderr)
        return 2

    if args.tier_a:
        scan_paths = tier_a_targets()
    else:
        scan_paths = [resolve_repo_path(path) for path in args.paths]

    entries: list[RosettaEntry] = []
    for path in iter_markdown(scan_paths, include_compat=args.include_compat):
        entry = parse_entry(path)
        if entry is not None:
            entries.append(entry)

    missing = collect_missing(scan_paths, include_compat=args.include_compat) if args.include_missing else []
    output = render_json(entries, missing) if args.format == "json" else render_markdown(entries, missing)

    if args.output:
        output_path = resolve_repo_path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    if args.fail_missing and missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
