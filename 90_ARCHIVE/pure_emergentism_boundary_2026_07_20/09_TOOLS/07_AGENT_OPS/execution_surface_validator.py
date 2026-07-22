#!/usr/bin/env python3
"""
Execution Surface Validator — Scans the entire Emergentism organism for agent-readiness gaps.

Produces a machine-readable AGENT_GAPS.json that agents consume as a task queue.
Extends check_links.py with coverage analysis, evidence-tier validation, and
kill-criteria verification.

Usage:
    python execution_surface_validator.py              # Full scan + report
    python execution_surface_validator.py --json       # Output AGENT_GAPS.json only
    python execution_surface_validator.py --links      # Link check only
    python execution_surface_validator.py --foundation # Foundation-only scan

Exit codes:
    0 = all checks pass (no gaps above threshold)
    1 = gaps found or errors encountered
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime


# --- Configuration ---

ROOT = Path(__file__).parent.parent.parent.parent  # ☀️ Project root

ZONES = {
    "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/00_META": {"threshold": 0.90, "required": True},
    "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE": {"threshold": 0.50, "required": False},
    "01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE": {"threshold": 0.50, "required": False},
    "02_SKYZAI/01_NOOSPHERE": {"threshold": 0.30, "required": True},
    "01_EMERGENTISM/11_UPLINK": {"threshold": 0.30, "required": False},
    "02_SKYZAI/01_NOOSPHERE/07_PWAs": {"threshold": 0.20, "required": True},
    "01_EMERGENTISM/09_TOOLS": {"threshold": 0.30, "required": False},
}

# Files that are exempt from execution surface requirements
EXEMPT_PATTERNS = [
    r".*README\.md$",           # Directory navigation files (optional)
    r".*_AUDIT_REPORT_.*\.md$", # Audit reports are human-facing
    r".*CLAUDE\.md$",           # Per-directory Claude instructions
    r".*AGENTS\.md$",           # Agent routing files
    r".*/90_ARCHIVE/.*",         # Historical archives
    r".*/\.[^/]+/.*",           # Hidden directories (.claude, .codex, etc.)
    r".*/node_modules/.*",       # NPM dependencies
    r".*/__pycache__/.*",        # Python cache
    r".*/\.venv/.*",             # Virtual environments
    r".*/venv/.*",               # Virtual environments
    r".*/target/.*",             # Rust build output
    r".*/dist/.*",               # Build output
    r".*/build/.*",              # Build output
    r".*/\.pytest_cache/.*",     # Test cache
    r".*/\.ruff_cache/.*",       # Linter cache
    r".*/memory/raw/.*",          # Raw memory ingest artifacts
]

# Evidence tier patterns
# Matches single-letter tiers [E], [S], [I], [C] and combo tiers [I/S], [E/S/C], etc.
# Also recognizes VIVEKA/FOUNDATION custom tiers: [T], [Ref], [I/T], [Testable]
TIER_PATTERN = re.compile(r"\[([ESICTRefTesablProp]+(?:/[ESICTRefTesablProp]+)*)\]")
# Also detect text-based evidence tier declarations
TIER_TEXT_PATTERN = re.compile(
    r"^\s*\*\*Evidence\s+[Tt]ier:\*\*\s*(?:\[?[ESICTRefTesablProp]\]?)?",
    re.MULTILINE
)
# Detect tier annotations in tables: | [I] | or | [C] |
TIER_TABLE_PATTERN = re.compile(r"\|\s*\[([ESICTRefTesablProp])\]\s*\|")

KILL_CRITERIA_PATTERNS = [
    re.compile(r"kill\s+(?:criterion|criteri(?:a|on))", re.IGNORECASE),
    re.compile(r"falsif(?:y|ication|ied|iable|iability)", re.IGNORECASE),
    re.compile(r"if.*(?:shown|demonstrated|proven|found)", re.IGNORECASE),
    re.compile(r"this\s+claim\s+(?:falls|is\s+void)", re.IGNORECASE),
    re.compile(r"##\s*Kill\s+Criteria", re.IGNORECASE),
]

# Pattern to detect non-standard evidence tier text (for mismatch reporting)
# Matches actual tier declarations, not mere mentions. Looks for:
# - **Evidence tier:** ...  or **Evidence Tier:** ...
# - Evidence tier: [X] ...
# But NOT: # Evidence Tier (headings), "evidence tiers" (plural mentions),
#          sentences like "Every signal must carry an evidence tier:"
TIER_ANY_TEXT_PATTERN = re.compile(
    r"^(?:\s*[-*]?\s*)?\*?\*?Evidence\s+[Tt]ier\s*[:\-]\s*(?!\s*$)",
    re.IGNORECASE | re.MULTILINE
)

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
EXECUTION_SURFACE_PATTERNS = [
    re.compile(r"##?\s*(?:Agent\s+)?Execution\s+Surface", re.IGNORECASE),
    re.compile(r"Agent\s+Directive", re.IGNORECASE),
]
CANONICAL_PATH_PATTERN = re.compile(r"\*\*Canonical\s+Path:\*\*", re.IGNORECASE)


# --- Data Structures ---

@dataclass
class FileReport:
    path: str
    zone: str
    word_count: int = 0
    has_execution_surface: bool = False
    has_canonical_path: bool = False
    has_evidence_tier: bool = False
    evidence_tiers_found: List[str] = field(default_factory=list)
    has_kill_criteria: bool = False
    has_nonstandard_tier: bool = False
    broken_links: List[str] = field(default_factory=list)
    exempt: bool = False

    def to_dict(self):
        return asdict(self)


@dataclass
class ZoneReport:
    zone: str
    threshold: float
    files: List[FileReport] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def non_exempt_files(self) -> int:
        return sum(1 for f in self.files if not f.exempt)

    @property
    def with_execution_surface(self) -> int:
        return sum(1 for f in self.files if f.has_execution_surface)

    @property
    def with_canonical_path(self) -> int:
        return sum(1 for f in self.files if f.has_canonical_path)

    @property
    def with_kill_criteria(self) -> int:
        return sum(1 for f in self.files if f.has_kill_criteria)

    @property
    def coverage(self) -> float:
        ne = self.non_exempt_files
        if ne == 0:
            return 1.0
        return self.with_execution_surface / ne

    @property
    def meets_threshold(self) -> bool:
        return self.coverage >= self.threshold

    def to_dict(self):
        return {
            "zone": self.zone,
            "threshold": self.threshold,
            "total_files": self.total_files,
            "non_exempt_files": self.non_exempt_files,
            "with_execution_surface": self.with_execution_surface,
            "with_canonical_path": self.with_canonical_path,
            "with_kill_criteria": self.with_kill_criteria,
            "coverage": round(self.coverage, 3),
            "meets_threshold": self.meets_threshold,
            "gaps": [f.to_dict() for f in self.files if not f.exempt and not f.has_execution_surface],
        }


# --- Core Functions ---

def is_exempt(path: str) -> bool:
    """Check if a file is exempt from execution surface requirements."""
    for pattern in EXEMPT_PATTERNS:
        if re.match(pattern, path):
            return True
    return False


def count_words(content: str) -> int:
    """Approximate word count."""
    return len(content.split())


def check_file(filepath: Path, zone: str) -> FileReport:
    """Analyze a single markdown file for agent-readiness."""
    rel_path = str(filepath.relative_to(ROOT))
    report = FileReport(path=rel_path, zone=zone)

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ⚠️  Error reading {rel_path}: {e}")
        return report
    if content is None:
        return report

    report.word_count = count_words(content)
    report.exempt = is_exempt(rel_path)

    # Check execution surface
    for pattern in EXECUTION_SURFACE_PATTERNS:
        if pattern.search(content):
            report.has_execution_surface = True
            break

    # Check canonical path
    if CANONICAL_PATH_PATTERN.search(content):
        report.has_canonical_path = True

    # Check evidence tiers (single, combo, text-based, table-based)
    tiers = TIER_PATTERN.findall(content)
    if TIER_TEXT_PATTERN.search(content):
        tiers.append("TEXT")
    table_tiers = TIER_TABLE_PATTERN.findall(content)
    tiers.extend(table_tiers)
    report.evidence_tiers_found = list(set(tiers))
    report.has_evidence_tier = len(tiers) > 0

    # Track non-standard tier formats for mismatch reporting
    report.has_nonstandard_tier = (
        TIER_ANY_TEXT_PATTERN.search(content) is not None
        and not TIER_PATTERN.search(content)
        and not TIER_TEXT_PATTERN.search(content)
        and not TIER_TABLE_PATTERN.search(content)
    )

    # Check kill criteria (only if file makes actual [C] claims and not exempt)
    # We look for [C] followed by substantive claim text, not just glossary entries
    has_c_claims = has_substantive_c_claims(content)
    if not report.exempt and has_c_claims:
        for pattern in KILL_CRITERIA_PATTERNS:
            if pattern.search(content):
                report.has_kill_criteria = True
                break

    # Check broken links
    file_dir = filepath.parent
    for text, link in LINK_PATTERN.findall(content):
        if link.startswith(("http", "https", "mailto", "#", "file://")):
            continue
        # Strip anchor
        link_clean = link.split("#")[0]
        if not link_clean:
            continue
        link_path = file_dir / link_clean
        if not link_path.exists():
            report.broken_links.append(link)

    return report


def has_substantive_c_claims(content: str) -> bool:
    """Check if the file makes substantive [C] claims, not just mentions [C] in passing."""
    # Look for [C] followed by claim-like text (not just definitions or tier keys)
    # Pattern: [C] followed by text that isn't just "Conjecture" or similar
    claim_pattern = re.compile(
        r"\[C\]\s+(?!Conjecture|conjecture|—|–|-|\(|\[)"
        r"([A-Z][^\.\n]{10,}|"
        r"[Tt]he\s+[A-Z][^\.\n]{8,}|"
        r"[Aa]ll\s+[^\.\n]{8,}|"
        r"[Ii]f\s+[^\.\n]{8,})",
        re.MULTILINE
    )
    return bool(claim_pattern.search(content))


def scan_zone(zone_path: Path, zone_name: str, threshold: float) -> ZoneReport:
    """Scan all markdown files in a zone."""
    report = ZoneReport(zone=zone_name, threshold=threshold)

    if not zone_path.exists():
        print(f"  ⚠️  Zone not found: {zone_path}")
        return report

    SKIP_DIRS = {"node_modules", "__pycache__", ".venv", "venv", "target", "dist", "build", ".pytest_cache", ".ruff_cache"}
    for filepath in zone_path.rglob("*.md"):
        rel_parts = filepath.relative_to(zone_path).parts
        # Skip hidden directories and dependency/build directories
        if any(part.startswith(".") for part in rel_parts):
            continue
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        report.files.append(check_file(filepath, zone_name))

    return report


def print_report(zone_reports: List[ZoneReport], broken_links: List[tuple]):
    """Print human-readable report."""
    print("\n" + "=" * 70)
    print("  EXECUTION SURFACE VALIDATOR REPORT")
    print(f"  Generated: {datetime.now().isoformat()}")
    print(f"  Root: {ROOT}")
    print("=" * 70)

    total_files = 0
    total_with_surface = 0
    total_non_exempt = 0

    print("\n📊 COVERAGE BY ZONE\n")
    print(f"  {'Zone':<40} {'Files':>6} {'Exec':>6} {'Cov':>6} {'Thresh':>6} {'Status':>8}")
    print(f"  {'-'*40} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*8}")

    for zr in zone_reports:
        total_files += zr.total_files
        total_with_surface += zr.with_execution_surface
        total_non_exempt += zr.non_exempt_files

        status = "✅ PASS" if zr.meets_threshold else "❌ FAIL"
        if zr.non_exempt_files == 0:
            status = "⏭️  SKIP"

        print(f"  {zr.zone:<40} {zr.non_exempt_files:>6} {zr.with_execution_surface:>6} "
              f"{zr.coverage*100:>5.1f}% {zr.threshold*100:>5.1f}% {status:>8}")

    overall = total_with_surface / total_non_exempt if total_non_exempt > 0 else 1.0
    print(f"\n  {'OVERALL':<40} {total_non_exempt:>6} {total_with_surface:>6} "
          f"{overall*100:>5.1f}%")

    # Files missing execution surfaces
    print("\n📁 FILES MISSING EXECUTION SURFACES (top 30)\n")
    missing = []
    for zr in zone_reports:
        for f in zr.files:
            if not f.exempt and not f.has_execution_surface:
                missing.append((zr.zone, f.path, f.word_count))

    missing.sort(key=lambda x: x[2], reverse=True)
    for zone, path, wc in missing[:30]:
        print(f"  [{zone:<25}] {path:<50} ({wc:>5} words)")

    if len(missing) > 30:
        print(f"  ... and {len(missing) - 30} more")

    # [C] claims without kill criteria (only files with substantive [C] claims)
    print("\n⚠️  [C] CLAIMS WITHOUT KILL CRITERIA\n")
    c_without_kill = []
    for zr in zone_reports:
        for f in zr.files:
            if not f.exempt and "C" in f.evidence_tiers_found and not f.has_kill_criteria and has_substantive_c_claims(
                (ROOT / f.path).read_text(encoding="utf-8") if (ROOT / f.path).exists() else ""
            ):
                c_without_kill.append((zr.zone, f.path))

    if c_without_kill:
        for zone, path in c_without_kill:
            print(f"  [{zone:<25}] {path}")
    else:
        print("  ✅ All [C] claims have kill criteria")

    # Format mismatch report
    print("\n📋 EVIDENCE TIER FORMAT MISMATCHES (non-standard tier text detected)\n")
    mismatches = []
    for zr in zone_reports:
        for f in zr.files:
            if f.has_nonstandard_tier:
                mismatches.append((zr.zone, f.path))

    if mismatches:
        for zone, path in mismatches[:20]:
            print(f"  [{zone:<25}] {path}")
        if len(mismatches) > 20:
            print(f"  ... and {len(mismatches) - 20} more")
    else:
        print("  ✅ No format mismatches found")

    # Broken links
    print(f"\n🔗 BROKEN LINKS ({len(broken_links)} total)\n")
    if broken_links:
        for source, link in broken_links[:20]:
            print(f"  {source:<60} -> {link}")
        if len(broken_links) > 20:
            print(f"  ... and {len(broken_links) - 20} more")
    else:
        print("  ✅ No broken internal links found")

    print("\n" + "=" * 70)
    print("  END OF REPORT")
    print("=" * 70 + "\n")


def build_gaps_json(zone_reports: List[ZoneReport]) -> dict:
    """Build the machine-readable AGENT_GAPS.json structure."""
    gaps = []
    for zr in zone_reports:
        for f in zr.files:
            if f.exempt:
                continue
            gap = {
                "path": f.path,
                "zone": f.zone,
                "word_count": f.word_count,
                "missing_execution_surface": not f.has_execution_surface,
                "missing_canonical_path": not f.has_canonical_path,
                "missing_evidence_tier": not f.has_evidence_tier,
                "has_nonstandard_tier": f.has_nonstandard_tier,
                "c_without_kill": (
                    "C" in f.evidence_tiers_found
                    and not f.has_kill_criteria
                    and has_substantive_c_claims(
                        (ROOT / f.path).read_text(encoding="utf-8") if (ROOT / f.path).exists() else ""
                    )
                ),
                "broken_links": f.broken_links,
            }
            # Only include files with actual gaps
            if any([
                gap["missing_execution_surface"],
                gap["missing_canonical_path"],
                gap["missing_evidence_tier"],
                gap["c_without_kill"],
                len(gap["broken_links"]) > 0,
            ]):
                gaps.append(gap)

    return {
        "generated": datetime.now().isoformat(),
        "root": str(ROOT),
        "validator_version": "1.1.0",
        "zones": [zr.to_dict() for zr in zone_reports],
        "gaps": gaps,
        "summary": {
            "total_files": sum(zr.total_files for zr in zone_reports),
            "non_exempt_files": sum(zr.non_exempt_files for zr in zone_reports),
            "with_execution_surface": sum(zr.with_execution_surface for zr in zone_reports),
            "overall_coverage": round(
                sum(zr.with_execution_surface for zr in zone_reports) /
                max(1, sum(zr.non_exempt_files for zr in zone_reports)), 3
            ),
            "total_gaps": len(gaps),
            "zones_failing": [zr.zone for zr in zone_reports if not zr.meets_threshold],
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Execution Surface Validator")
    parser.add_argument("--json", action="store_true", help="Output AGENT_GAPS.json only")
    parser.add_argument("--links", action="store_true", help="Link check only")
    parser.add_argument("--foundation", action="store_true", help="Foundation-only scan")
    parser.add_argument("--output", type=str, default="01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/AGENT_GAPS.json", help="Output path for JSON")
    args = parser.parse_args()

    zones_to_scan = ZONES.copy()
    if args.foundation:
        zones_to_scan = {k: v for k, v in zones_to_scan.items() if "FOUNDATIONS" in k}

    zone_reports = []
    all_broken_links = []

    for zone_name, config in zones_to_scan.items():
        zone_path = ROOT / zone_name
        print(f"🔍 Scanning {zone_name} ...")
        zr = scan_zone(zone_path, zone_name, config["threshold"])
        zone_reports.append(zr)
        for f in zr.files:
            for link in f.broken_links:
                all_broken_links.append((f.path, link))
        print(f"   Found {zr.total_files} files, {zr.with_execution_surface} with execution surfaces")

    # Build JSON output
    gaps_data = build_gaps_json(zone_reports)

    output_path = ROOT / args.output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(gaps_data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Written {output_path}")

    if not args.json:
        print_report(zone_reports, all_broken_links)

    # Exit code
    failing_zones = [zr.zone for zr in zone_reports if not zr.meets_threshold]
    if failing_zones:
        print(f"\n❌ Failing zones: {', '.join(failing_zones)}")
        sys.exit(1)
    else:
        print("\n✅ All zones meet coverage thresholds")
        sys.exit(0)


if __name__ == "__main__":
    main()
