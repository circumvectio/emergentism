#!/usr/bin/env python3
"""
phylo_sync_check.py — Phylogenetic-sync CI rule (§5.1 of 06b_PHYLOGENETIC_TREE.md).

Rule: if a PR modifies any trigger-file in the phylogenetic toolchain
(the speciation operator, the niche-manifest schema, the ancestry audit
tool, the merge operator, or any manifest JSON), then that PR must also
update the canonical spec document 11_UPLINK/00_CORE/06b_PHYLOGENETIC_TREE.md.

Usage:
    # CI mode: compare current tree against a base ref.
    python3 phylo_sync_check.py --base origin/main

    # Pre-commit mode: check staged changes only.
    python3 phylo_sync_check.py --staged

    # Local workspace mode: check working-tree + staged vs HEAD.
    python3 phylo_sync_check.py

Exit codes:
    0 — OK (no trigger files changed, OR trigger files changed and doc also changed)
    1 — Phylogenetic-sync violation (trigger changed, doc didn't)
    2 — Error (git not available, bad args, etc.)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Trigger patterns — prefixes or exact paths that, if changed, require
# a matching update to the canonical spec. If a changed path matches any
# pattern here AND does not match an EXEMPT_PATTERNS entry, it triggers.
TRIGGER_PATTERNS: list[str] = [
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/apply_dac_scaffold.py",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/dac_ancestry_audit.py",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/dac_scaffold_manifests/",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/phylo_merge_manifests.py",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/phylo_ancestry_query.py",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/phylo_promote.py",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/phylo_sync_check.py",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/phylo_council_gates.py",
    "SKYZAI_ORG/00_REFERENCE/DAC_FACTORY/DAC_SCAFFOLD/",
    "SKYZAI_ORG/00_REFERENCE/DAC_FACTORY/DAC_STANDARD_FOLDER_STRUCTURE.md",
    "SKYZAI_ORG/00_REFERENCE/DAC_FACTORY/DAC_SCAFFOLD_INSTANTIATION_SPEC.md",
]

# Exempt patterns — editorial/meta files inside trigger dirs that do not
# change the phylogenetic artifact set and therefore do not require a
# matching spec update. Keep this list tight; prefer a doc touch when in
# doubt.
EXEMPT_PATTERNS: list[str] = [
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/dac_scaffold_manifests/README.md",
    "EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/dac_scaffold_manifests/CHANGELOG.md",
    "SKYZAI_ORG/00_REFERENCE/DAC_FACTORY/DAC_SCAFFOLD/SCAFFOLD_FILL_GUIDE.md",
]

# The canonical spec document that must update in lockstep.
DOC_PATH = "EMERGENTISM_ORG/11_UPLINK/06b_PHYLOGENETIC_TREE.md"


def _run_git(args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("error: git not found on PATH", file=sys.stderr)
        sys.exit(2)
    except subprocess.CalledProcessError as exc:
        print(f"error: git {' '.join(args)} failed: {exc.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return [line for line in result.stdout.splitlines() if line.strip()]


def changed_files(base: str | None, staged: bool) -> list[str]:
    if base is not None:
        return _run_git(["diff", "--name-only", f"{base}...HEAD"])
    if staged:
        return _run_git(["diff", "--name-only", "--cached"])
    # default: working tree + staged vs HEAD
    tracked = _run_git(["diff", "--name-only", "HEAD"])
    staged_files = _run_git(["diff", "--name-only", "--cached"])
    return sorted(set(tracked) | set(staged_files))


def _matches(path: str, patterns: list[str]) -> bool:
    return any(path == p or path.startswith(p) for p in patterns)


def is_trigger(path: str) -> bool:
    if _matches(path, EXEMPT_PATTERNS):
        return False
    return _matches(path, TRIGGER_PATTERNS)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Enforce phylogenetic-sync: trigger changes require doc update."
    )
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--base", help="Compare HEAD against this ref (CI mode).")
    mode.add_argument(
        "--staged",
        action="store_true",
        help="Check staged changes only (pre-commit mode).",
    )
    ap.add_argument(
        "--verbose",
        action="store_true",
        help="Print the full list of changed files.",
    )
    args = ap.parse_args(argv)

    files = changed_files(args.base, args.staged)
    triggers = [f for f in files if is_trigger(f)]
    doc_changed = DOC_PATH in files

    if args.verbose:
        print(f"changed files ({len(files)}):")
        for f in files:
            mark = " (trigger)" if is_trigger(f) else ""
            doc_mark = " (spec doc)" if f == DOC_PATH else ""
            print(f"  {f}{mark}{doc_mark}")
        print()

    if not triggers:
        print("✅ phylo-sync OK: no trigger files changed.")
        return 0

    if doc_changed:
        print(
            f"✅ phylo-sync OK: {len(triggers)} trigger file(s) changed, "
            f"{DOC_PATH} updated in same change."
        )
        return 0

    print(
        f"❌ phylo-sync VIOLATION: {len(triggers)} trigger file(s) changed, "
        f"but {DOC_PATH} was not updated.",
        file=sys.stderr,
    )
    print("\nTriggered files:", file=sys.stderr)
    for t in triggers:
        print(f"  - {t}", file=sys.stderr)
    print(
        "\nUpdate the canonical spec (§4 Artifacts or §2 Definitions) "
        "or add a --skip-phylo-sync bypass with explicit justification.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
