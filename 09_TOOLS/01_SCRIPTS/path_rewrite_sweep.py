#!/usr/bin/env python3
"""path_rewrite_sweep.py — Post-reorg path-reference sweep.

Rewrites old-root path references to new two-root (EMERGENTISM_ORG / SKYZAI_ORG)
layout. Dry-run by default. Idempotent — running twice produces no further
changes on already-rewritten files.

Mappings (applied in order; longer first to avoid prefix collisions):

    01_FRAMEWORK/01_FOUNDATIONS/  ->  EMERGENTISM_ORG/
    01_FRAMEWORK/                 ->  EMERGENTISM_ORG/08_FRAMEWORK_SUPPORT/
    03_UPLINK/                    ->  EMERGENTISM_ORG/11_UPLINK/
    05_TOOLS/                     ->  EMERGENTISM_ORG/09_TOOLS/
    06_SEED/                      ->  EMERGENTISM_ORG/10_SEED/
    04_PWAs/                      ->  SKYZAI_ORG/09_PWAs/
    04_NETWORK_ENTITIES/                  ->  SKYZAI_ORG/04_NETWORK_ENTITIES/
    02_ORGANISM/                  ->  SKYZAI_ORG/
    00_INTAKE/                    ->  SKYZAI_ORG/00_INTAKE/

Safety:
  - Matches only when the prefix is at line start OR preceded by a non-alphanumeric
    non-underscore non-slash character (so we don't rewrite `SKYZAI_ORG/02_ORGANISM/`
    as `SKYZAI_ORG/SKYZAI_ORG/` etc.)
  - Excludes: .git, 08_ARCHIVE, 90_ARCHIVE, 91_COMPATIBILITY, Github, PROCESSED,
    .claude
  - Excludes root README.md, EMERGENTISM_ORG/README.md, and SKYZAI_ORG/README.md
    (deliberate migration docs)
  - Only touches *.md files (doc refs; code refs are structurally different and out of scope)

Usage:
    python3 path_rewrite_sweep.py                # dry-run (default)
    python3 path_rewrite_sweep.py --write        # actually modify files
    python3 path_rewrite_sweep.py --scope SKYZAI_ORG   # restrict to a subtree
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# Mappings — ordered longest-prefix-first so specific roots win over broad roots.
MAPPINGS = [
    ("01_FRAMEWORK/01_FOUNDATIONS/", "EMERGENTISM_ORG/"),
    ("01_FRAMEWORK/",                "EMERGENTISM_ORG/08_FRAMEWORK_SUPPORT/"),
    ("03_UPLINK/",                   "EMERGENTISM_ORG/11_UPLINK/"),
    ("05_TOOLS/",                    "EMERGENTISM_ORG/09_TOOLS/"),
    ("06_SEED/",                     "EMERGENTISM_ORG/10_SEED/"),
    ("04_PWAs/",                     "SKYZAI_ORG/09_PWAs/"),
    ("03_VENTURES/",                 "SKYZAI_ORG/03_VENTURES/"),
    ("02_ORGANISM/",                 "SKYZAI_ORG/"),
    ("00_INTAKE/",                   "SKYZAI_ORG/00_INTAKE/"),
]

# Boundary: either start-of-line, or a character that is NOT alphanumeric / _ / /
# (so we don't match `EMERGENTISM_ORG/02_ORGANISM/` etc.)
BOUNDARY = r"(?:^|(?<=[^A-Za-z0-9_/]))"

COMPILED = [(re.compile(BOUNDARY + re.escape(old)), new) for old, new in MAPPINGS]

EXCLUDE_DIRS = {
    ".git",
    "08_ARCHIVE",
    "90_ARCHIVE",
    "91_COMPATIBILITY",
    "Github",
    "PROCESSED",
    ".claude",
    ".codex",  # already hand-fixed with historical note
    "node_modules",
    ".venv",
    ".venv_proof",
    "__pycache__",
}

EXCLUDE_FILES = {
    "README.md",                       # root — migration table
    "EMERGENTISM_ORG/README.md",       # two-root README — migration doc
    "SKYZAI_ORG/README.md",            # two-root README — migration doc
}


def should_skip_path(rel: str) -> bool:
    parts = rel.split("/")
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if rel in EXCLUDE_FILES:
        return True
    return False


def rewrite(content: str) -> tuple[str, int]:
    """Apply all mappings. Return (new_content, num_replacements)."""
    total = 0
    out = content
    for pattern, new in COMPILED:
        out, n = pattern.subn(new, out)
        total += n
    return out, total


def iter_markdown(root: Path, scope: Path | None):
    base = scope if scope else root
    for path in base.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        try:
            rel = path.resolve().relative_to(root).as_posix()
        except ValueError:
            continue
        if rel in EXCLUDE_FILES:
            continue
        yield path, rel


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true",
                    help="Actually modify files. Default: dry-run.")
    ap.add_argument("--scope", default=None,
                    help="Restrict to a subtree (repo-relative), e.g. SKYZAI_ORG")
    ap.add_argument("--root", default=None,
                    help="Repo root (auto-detected as parents[3] of this script)")
    ap.add_argument("--show", type=int, default=10,
                    help="Sample N files' diffs on dry-run (default 10)")
    args = ap.parse_args(argv)

    if args.root:
        root = Path(args.root).resolve()
    else:
        root = Path(__file__).resolve().parents[3]

    scope = (root / args.scope).resolve() if args.scope else None

    total_files = 0
    changed_files = 0
    total_replacements = 0
    samples_shown = 0

    for path, rel in iter_markdown(root, scope):
        total_files += 1
        try:
            content = path.read_text(encoding="utf-8")
        except (IOError, UnicodeDecodeError) as exc:
            print(f"SKIP {rel}: {exc}", file=sys.stderr)
            continue

        new_content, n = rewrite(content)
        if n == 0:
            continue
        changed_files += 1
        total_replacements += n

        if args.write:
            path.write_text(new_content, encoding="utf-8")
            print(f"WRITE {rel} ({n} replacements)")
        else:
            prefix = "WOULD_WRITE"
            print(f"{prefix} {rel} ({n} replacements)")
            if samples_shown < args.show:
                # Show first 3 changed lines
                shown = 0
                for old_line, new_line in zip(content.splitlines(), new_content.splitlines()):
                    if old_line != new_line and shown < 3:
                        print(f"    - {old_line[:120]}")
                        print(f"    + {new_line[:120]}")
                        shown += 1
                samples_shown += 1

    action = "Wrote" if args.write else "Would write"
    print(f"\n{action} {changed_files} files with {total_replacements} total replacements "
          f"(scanned {total_files} markdown files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
