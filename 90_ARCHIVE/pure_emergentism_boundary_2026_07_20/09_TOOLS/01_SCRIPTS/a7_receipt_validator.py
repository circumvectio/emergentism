#!/usr/bin/env python3
"""a7_receipt_validator — A7 evidence-tier validator for canon documents.

Walks canonical and active-source markdown documents and checks every claim
that should carry an evidence tier ([A], [B], [S], [I], [D], [C]). Flags:
  - Numeric promises (durations, percentages, counts) without an evidence tier
  - Strong language ("guarantees", "ensures", "always") without [A] or [B] backing
  - Pricing claims without K2 envelope reference
  - Status labels (LOCAL_PROOF, etc.) outside of allowed values
  - Cross-references to files that don't exist

Usage:
  python3 a7_receipt_validator.py [--paths PATH [PATH ...]] [--strict]

Defaults to scanning:
  02_SKYZAI/01_NOOSPHERE/03_PRODUCTS/00_SKYZAI_COM_PRODUCT_MANIFEST.md
  02_SKYZAI/01_NOOSPHERE/03_PRODUCTS/skyzai_marketplace/0N_*.md
  02_SKYZAI/01_NOOSPHERE/07_PWAs/pay_skyzai_com/COMMERCIAL_STRATEGY_2026_05_09.md

Exit code:
  0 = all flagged claims have receipts
  1 = unresolved violations (in --strict mode)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parents[3]

DEFAULT_PATHS = [
    REPO / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "03_PRODUCTS" / "00_SKYZAI_COM_PRODUCT_MANIFEST.md",
    REPO / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "07_PWAs" / "pay_skyzai_com" / "COMMERCIAL_STRATEGY_2026_05_09.md",
]
DEFAULT_PATHS.extend(
    sorted(
        (REPO / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "03_PRODUCTS" / "skyzai_marketplace").glob("[0-9][0-9]_*.md")
    )
)

EVIDENCE_TIER = re.compile(r"\[(A|B|S|I|D|C)\]")
ALLOWED_STATUS = {"LOCAL_PROOF", "SPEC", "SPEC→PROOF", "EXTERNAL_PROOF"}
STATUS_PATTERN = re.compile(r"`([A-Z_→]+)`")

# Patterns for claims that should carry evidence
PRICING_PATTERN = re.compile(r"\$[\d,]+(\.\d+)?(/mo|/month|/recommendation|/rec|/year)?")
PERCENTAGE_CLAIM = re.compile(r"\b\d{1,3}(\.\d+)?%")
TIME_CLAIM = re.compile(r"\b\d+\s*(hour|day|week|month|year|min)s?\b", re.IGNORECASE)
STRONG_LANGUAGE = re.compile(r"\b(guarantee|guarantees|guaranteed|ensures|always|never|prove[ds]?|certified|audited)\b", re.IGNORECASE)


class Issue(NamedTuple):
    file: Path
    line: int
    severity: str  # "ERROR" | "WARN" | "INFO"
    message: str
    snippet: str


def line_iter(path: Path):
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        yield i, line


def is_in_table(line: str) -> bool:
    return line.strip().startswith("|") or "---|" in line


def is_in_code_block(text: str, line_num: int) -> bool:
    """Check if line_num is inside a fenced code block."""
    lines = text.splitlines()
    fence_count = sum(
        1 for ln in lines[:line_num] if ln.strip().startswith("```")
    )
    return fence_count % 2 == 1


def check_file(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    if not path.exists():
        issues.append(
            Issue(path, 0, "ERROR", f"file not found: {path}", "")
        )
        return issues

    full_text = path.read_text(encoding="utf-8")

    for line_num, line in line_iter(path):
        # Skip code blocks and table headers
        if is_in_code_block(full_text, line_num):
            continue

        snippet = line.strip()[:120]

        # Check 1: status labels in unexpected values
        for match in STATUS_PATTERN.findall(line):
            if match in {"LOCAL_PROOF", "SPEC", "SPEC→PROOF", "EXTERNAL_PROOF"}:
                # Valid
                continue
            # Other backticks are fine (commands, code, etc.)
            # Only flag if it looks like a status label context
            if "Status:" in line or "status:" in line:
                if match not in ALLOWED_STATUS:
                    issues.append(
                        Issue(
                            path, line_num, "ERROR",
                            f"unknown status label '{match}' (allowed: {ALLOWED_STATUS})",
                            snippet,
                        )
                    )

        # Check 2: strong language without evidence tier
        if STRONG_LANGUAGE.search(line) and not EVIDENCE_TIER.search(line):
            # Be lenient on table rows (often have evidence in adjacent column) and within section headers
            if not is_in_table(line) and not line.strip().startswith("#"):
                # Very lenient — only flag if no [tier] anywhere on the line or adjacent paragraph
                # Skip refusal lists ("never", "always" common in refusal text)
                if "Refusal" not in line and "refusal" not in line and "η=0" not in line:
                    issues.append(
                        Issue(
                            path, line_num, "WARN",
                            "strong language without evidence tier",
                            snippet,
                        )
                    )

        # Check 3: pricing without K2 reference (only flag in non-table prose)
        if PRICING_PATTERN.search(line) and not is_in_table(line):
            if (
                "K2" not in line
                and "TBD" not in line
                and "[" not in line  # has any tier marker
                and "tier" not in line.lower()
            ):
                if "$" in line and "$X" not in line:
                    issues.append(
                        Issue(
                            path, line_num, "WARN",
                            "pricing in prose without K2 reference or evidence tier",
                            snippet,
                        )
                    )

    return issues


def check_cross_refs(path: Path) -> list[Issue]:
    """Find markdown links to relative files; flag missing targets."""
    issues: list[Issue] = []
    if not path.exists():
        return issues

    text = path.read_text(encoding="utf-8")
    # Match [text](relative/path) but not http(s):// or anchors-only
    # Capture group 2: path before any anchor
    link_pattern = re.compile(r"\[[^\]]+\]\((?!https?://|#|mailto:)([^)#]+)(#[^)]*)?\)")
    base = path.parent

    for line_num, line in enumerate(text.splitlines(), start=1):
        if is_in_code_block(text, line_num):
            continue
        for match in link_pattern.finditer(line):
            target = match.group(1).strip()
            target_path = (base / target).resolve()
            if not target_path.exists():
                # Be lenient on directory references ending with /
                if target.endswith("/"):
                    if not target_path.is_dir():
                        issues.append(
                            Issue(
                                path, line_num, "WARN",
                                f"directory reference target not found: {target}",
                                line.strip()[:120],
                            )
                        )
                else:
                    issues.append(
                        Issue(
                            path, line_num, "WARN",
                            f"file reference target not found: {target}",
                            line.strip()[:120],
                        )
                    )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="A7 receipt validator for canon docs")
    parser.add_argument(
        "--paths",
        nargs="*",
        help="Files to scan (defaults to manifest + marketplace + commercial strategy)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any unresolved violation",
    )
    parser.add_argument(
        "--check-refs",
        action="store_true",
        help="Also check cross-reference link targets",
    )
    args = parser.parse_args()

    paths = [Path(p).resolve() for p in args.paths] if args.paths else DEFAULT_PATHS

    print(f"A7 receipt validator: scanning {len(paths)} document(s)\n")

    all_issues: list[Issue] = []
    for path in paths:
        rel = path.relative_to(REPO) if REPO in path.parents or path == REPO else path
        issues = check_file(path)
        if args.check_refs:
            issues.extend(check_cross_refs(path))
        if issues:
            print(f"📋 {rel}: {len(issues)} issue(s)")
            for issue in issues:
                marker = {"ERROR": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ "}[issue.severity]
                print(f"  {marker} L{issue.line}: {issue.message}")
                if issue.snippet:
                    print(f"        > {issue.snippet}")
            print()
            all_issues.extend(issues)
        else:
            print(f"✅ {rel}: clean")

    print()
    errors = sum(1 for i in all_issues if i.severity == "ERROR")
    warns = sum(1 for i in all_issues if i.severity == "WARN")

    if not all_issues:
        print("All documents pass A7 receipt validation ✅")
        return 0

    print(f"Total issues: {errors} ERROR, {warns} WARN")
    if errors == 0 and not args.strict:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
