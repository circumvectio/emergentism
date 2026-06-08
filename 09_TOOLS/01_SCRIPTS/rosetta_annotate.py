#!/usr/bin/env python3
"""Rosetta frontmatter helper.

This tool is intentionally narrow:

- list the Tier A Foundation files from packet 159
- audit whether files already carry a ``rosetta:`` frontmatter block
  and, for Foundation L-folder files, whether the primary level matches
  the owning folder
- apply a reviewed JSON/JSONL manifest when ``--write`` is explicitly passed

It does not infer doctrine. Charioteer packets propose annotations; this tool only
helps a warrior apply or verify reviewed blocks without touching compatibility
stubs by accident.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
FOUNDATION = ROOT / "01_EMERGENTISM"
if not FOUNDATION.exists():
    FOUNDATION = ROOT / "EMERGENTISM_ORG"
FOUNDATION_REL = FOUNDATION.relative_to(ROOT).as_posix()

LEVEL_FOLDERS = {
    "01_TELEOLOGY": "L1",
    "02_EPISTEMOLOGY": "L2",
    "03_METHODOLOGY": "L3",
    "04_AXIOLOGY": "L4",
    "05_COSMOLOGY": "L5",
    "06_ONTOLOGY": "L6",
    "07_THEOLOGY": "L7",
}

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


class RosettaError(Exception):
    """User-facing tool error."""


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    try:
        path.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise RosettaError(f"path escapes repo: {value}") from exc
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


def split_frontmatter(content: str) -> tuple[str | None, str]:
    if not content.startswith("---\n"):
        return None, content
    end = content.find("\n---\n", 4)
    if end == -1:
        return None, content
    return content[4:end], content[end + 5 :]


def has_rosetta(content: str) -> bool:
    frontmatter, _ = split_frontmatter(content)
    if frontmatter is None:
        return False
    return re.search(r"(?m)^rosetta:\s*$", frontmatter) is not None


def extract_primary_level(content: str) -> str | None:
    frontmatter, _ = split_frontmatter(content)
    if frontmatter is None:
        return None
    match = re.search(r"(?m)^\s+primary_level:\s*[\"']?(L[1-7])[\"']?\s*$", frontmatter)
    return match.group(1) if match else None


def expected_level(path: Path) -> str | None:
    try:
        rel_parts = path.resolve().relative_to(FOUNDATION).parts
    except ValueError:
        return None
    if not rel_parts:
        return None
    return LEVEL_FOLDERS.get(rel_parts[0])


def yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return json.dumps(str(value), ensure_ascii=False)


def render_yaml_mapping(data: dict[str, Any], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.extend(render_yaml_mapping(value, indent + 2))
        elif isinstance(value, list):
            lines.append(f"{pad}{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{pad}  - {next(iter(item))}: {yaml_scalar(next(iter(item.values())))}")
                    for sub_key, sub_value in list(item.items())[1:]:
                        lines.append(f"{pad}    {sub_key}: {yaml_scalar(sub_value)}")
                else:
                    lines.append(f"{pad}  - {yaml_scalar(item)}")
        else:
            lines.append(f"{pad}{key}: {yaml_scalar(value)}")
    return lines


def normalize_rosetta_block(entry: dict[str, Any]) -> str:
    if "block" in entry:
        block = str(entry["block"]).strip()
        if block.startswith("---"):
            raise RosettaError("manifest block must omit frontmatter delimiters")
        return block

    rosetta = entry.get("rosetta")
    if not isinstance(rosetta, dict):
        raise RosettaError("manifest entry must contain 'rosetta' object or 'block' string")

    level = rosetta.get("primary_level")
    if level is not None and level not in {f"L{i}" for i in range(1, 8)}:
        raise RosettaError(f"invalid primary_level: {level}")

    column = rosetta.get("primary_column")
    if column is not None and column not in VALID_COLUMNS:
        raise RosettaError(f"invalid primary_column: {column}")

    return "\n".join(render_yaml_mapping({"rosetta": rosetta}))


def insert_rosetta(content: str, block: str, *, replace: bool = False) -> str:
    if has_rosetta(content) and not replace:
        return content

    frontmatter, body = split_frontmatter(content)
    if frontmatter is None:
        return f"---\n{block.strip()}\n---\n\n{content}"

    if has_rosetta(content) and replace:
        # Deliberately simple replacement: remove the old top-level rosetta block
        # until the next unindented key. Human review is still required.
        frontmatter = re.sub(
            r"(?ms)^rosetta:\n(?:  .*\n?)+(?=^[A-Za-z0-9_-]+:|\Z)",
            "",
            frontmatter,
        ).rstrip()

    return f"---\n{frontmatter.rstrip()}\n{block.strip()}\n---\n{body}"


def read_manifest(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        entries = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        raw = json.loads(text)
        entries = raw["entries"] if isinstance(raw, dict) and "entries" in raw else raw
    if not isinstance(entries, list):
        raise RosettaError("manifest must be a JSON list, JSONL file, or object with entries")
    for entry in entries:
        if not isinstance(entry, dict) or "path" not in entry:
            raise RosettaError("each manifest entry must be an object with a path")
    return entries


def command_list_tier_a(_: argparse.Namespace) -> int:
    for path in tier_a_targets():
        print(rel(path))
    return 0


def command_audit(args: argparse.Namespace) -> int:
    targets = tier_a_targets() if args.tier_a else [resolve_repo_path(p) for p in args.paths]
    issues = 0

    for path in targets:
        if not path.exists() or path.suffix != ".md":
            print(f"SKIP {rel(path) if path.exists() else path}: not a markdown file")
            continue
        content = path.read_text(encoding="utf-8")
        expected = expected_level(path)
        primary = extract_primary_level(content)
        if not has_rosetta(content):
            print(f"MISSING {rel(path)}")
            issues += 1
            continue
        if expected and primary and primary != expected:
            print(f"LEVEL {rel(path)}: expected {expected}, found {primary}")
            issues += 1

    if issues:
        print(f"{issues} issue(s)")
        return 1
    print("rosetta audit ok")
    return 0


def command_apply_manifest(args: argparse.Namespace) -> int:
    manifest = read_manifest(resolve_repo_path(args.manifest))
    changed = 0

    for entry in manifest:
        path = resolve_repo_path(str(entry["path"]))
        if is_compat_surface(path) and not args.allow_compat:
            raise RosettaError(f"refusing compatibility surface without --allow-compat: {rel(path)}")
        if not path.exists():
            raise RosettaError(f"path does not exist: {rel(path)}")
        if path.suffix != ".md":
            raise RosettaError(f"path is not markdown: {rel(path)}")

        content = path.read_text(encoding="utf-8")
        block = normalize_rosetta_block(entry)
        updated = insert_rosetta(content, block, replace=args.replace)
        if updated == content:
            print(f"UNCHANGED {rel(path)}")
            continue
        changed += 1
        action = "WRITE" if args.write else "WOULD_WRITE"
        print(f"{action} {rel(path)}")
        if args.write:
            path.write_text(updated, encoding="utf-8")

    print(f"{'changed' if args.write else 'would change'} {changed} file(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_cmd = subparsers.add_parser("list-tier-a", help="print Tier A target files")
    list_cmd.set_defaults(func=command_list_tier_a)

    audit_cmd = subparsers.add_parser("audit", help="audit rosetta frontmatter presence")
    audit_cmd.add_argument("paths", nargs="*", help="markdown files to audit")
    audit_cmd.add_argument("--tier-a", action="store_true", help="audit packet-159 Tier A targets")
    audit_cmd.set_defaults(func=command_audit)

    apply_cmd = subparsers.add_parser(
        "apply-manifest",
        help="apply reviewed JSON/JSONL rosetta manifest; dry-run unless --write",
    )
    apply_cmd.add_argument("manifest", help="JSON or JSONL manifest")
    apply_cmd.add_argument("--write", action="store_true", help="write changes to disk")
    apply_cmd.add_argument("--replace", action="store_true", help="replace an existing rosetta block")
    apply_cmd.add_argument(
        "--allow-compat",
        action="store_true",
        help="allow writes to compatibility-stub surfaces",
    )
    apply_cmd.set_defaults(func=command_apply_manifest)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "audit" and not args.tier_a and not args.paths:
        parser.error("audit requires --tier-a or at least one path")
    try:
        return args.func(args)
    except RosettaError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
