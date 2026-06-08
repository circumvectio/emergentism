#!/usr/bin/env python3
"""
apply_dac_scaffold.py — Apply the canonical DAC_SCAFFOLD to a target repo.

Source:  02_ORGANISM/00_REFERENCE/DAC_FACTORY/DAC_SCAFFOLD/
Target:  any directory (e.g. Github/<repo>/)
Manifest: JSON file with {{PLACEHOLDER}} values.

Behaviour:
- Walks scaffold; for each file, writes target_dir / <relative_path> after
  substituting {{KEY}} tokens from the manifest.
- Skips destination files that already exist unless --overwrite is passed.
- Always skips scaffold's root CLAUDE.md / README.md / SCAFFOLD_FILL_GUIDE.md
  (they are template-authority docs, not per-DAC content). Pass
  --include-root-docs to override.
- Writes _DAC_SCAFFOLD_APPLIED.md at target root with the manifest snapshot,
  the scaffold tree hash, files written, files skipped, and unresolved
  placeholders.

Usage:
    python apply_dac_scaffold.py \\
        --manifest 05_TOOLS/scripts/dac_scaffold_manifests/agentz.json \\
        --target   /absolute/path/to/Github/agentz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_0-9]+)\}\}")
SKIP_ROOT_FILES = {"CLAUDE.md", "README.md", "SCAFFOLD_FILL_GUIDE.md"}
DEFAULT_SCAFFOLD = (
    Path(__file__).resolve().parents[3]
    / "SKYZAI_ORG"
    / "00_REFERENCE"
    / "DAC_FACTORY"
    / "DAC_SCAFFOLD"
)


def load_manifest(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for k, v in data.items():
        if v is None:
            continue
        out[str(k).upper()] = str(v)
    return out


def substitute(text: str, manifest: dict[str, str]) -> tuple[str, set[str]]:
    unresolved: set[str] = set()

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in manifest:
            return manifest[key]
        unresolved.add(key)
        return match.group(0)

    return PLACEHOLDER_RE.sub(repl, text), unresolved


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix().encode()
            h.update(b"\x00" + rel + b"\x00")
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def apply(
    scaffold: Path,
    target: Path,
    manifest: dict[str, str],
    overwrite: bool,
    include_root_docs: bool,
) -> dict[str, list]:
    written: list[str] = []
    skipped_existing: list[str] = []
    skipped_root: list[str] = []
    unresolved: dict[str, list[str]] = {}

    for src in sorted(scaffold.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(scaffold)
        if (
            len(rel.parts) == 1
            and rel.name in SKIP_ROOT_FILES
            and not include_root_docs
        ):
            skipped_root.append(str(rel))
            continue
        dst = target / rel
        if dst.exists() and not overwrite:
            skipped_existing.append(str(rel))
            continue
        text = src.read_text(encoding="utf-8")
        new_text, missing = substitute(text, manifest)
        if missing:
            unresolved[str(rel)] = sorted(missing)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(new_text, encoding="utf-8")
        written.append(str(rel))

    return {
        "written": written,
        "skipped_existing": skipped_existing,
        "skipped_root": skipped_root,
        "unresolved": unresolved,
    }


def write_applied_record(
    target: Path,
    manifest_path: Path,
    scaffold: Path,
    report: dict,
) -> Path:
    record = target / "_DAC_SCAFFOLD_APPLIED.md"
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    scaffold_hash = tree_hash(scaffold)
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    lines = [
        "# DAC Scaffold — Application Record",
        "",
        f"- Applied at: {ts}",
        f"- Scaffold source: `{scaffold}`",
        f"- Scaffold tree hash: `{scaffold_hash}`",
        f"- Manifest: `{manifest_path.name}`",
        "",
        "## Manifest snapshot",
        "",
        "```json",
        json.dumps(manifest_data, indent=2, ensure_ascii=False),
        "```",
        "",
        f"## Files written ({len(report['written'])})",
        "",
    ]
    lines += [f"- `{p}`" for p in report["written"]] or ["- (none)"]
    lines += [
        "",
        f"## Skipped (destination already existed) ({len(report['skipped_existing'])})",
        "",
    ]
    lines += [f"- `{p}`" for p in report["skipped_existing"]] or ["- (none)"]
    lines += [
        "",
        f"## Skipped (scaffold root docs) ({len(report['skipped_root'])})",
        "",
    ]
    lines += [f"- `{p}`" for p in report["skipped_root"]] or ["- (none)"]
    if report["unresolved"]:
        lines += ["", "## Unresolved placeholders", ""]
        for path, keys in sorted(report["unresolved"].items()):
            lines.append(f"- `{path}`: {', '.join(keys)}")
    else:
        lines += ["", "## Unresolved placeholders", "", "- (none)"]
    record.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return record


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Apply DAC_SCAFFOLD to a target repo.")
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--target", required=True, type=Path)
    ap.add_argument("--scaffold", type=Path, default=DEFAULT_SCAFFOLD)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--include-root-docs", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if not args.scaffold.is_dir():
        print(f"error: scaffold not found: {args.scaffold}", file=sys.stderr)
        return 2
    if not args.manifest.is_file():
        print(f"error: manifest not found: {args.manifest}", file=sys.stderr)
        return 2

    manifest = load_manifest(args.manifest)
    args.target.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print(f"[dry-run] would apply {args.scaffold} -> {args.target}")
        print(f"[dry-run] manifest keys: {sorted(manifest)}")
        return 0

    report = apply(
        scaffold=args.scaffold,
        target=args.target,
        manifest=manifest,
        overwrite=args.overwrite,
        include_root_docs=args.include_root_docs,
    )
    record = write_applied_record(
        target=args.target,
        manifest_path=args.manifest,
        scaffold=args.scaffold,
        report=report,
    )

    print(f"written:           {len(report['written'])}")
    print(f"skipped (existing): {len(report['skipped_existing'])}")
    print(f"skipped (root docs): {len(report['skipped_root'])}")
    print(f"unresolved files:   {len(report['unresolved'])}")
    print(f"record:            {record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
