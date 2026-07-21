#!/usr/bin/env python3
"""OPERATOR BRIEF GENERATOR — tomorrow's brief from current organism state.

Reads canonical organism state surfaces and emits a single-page brief
formatted for the Principal (Yves). The brief is the forcing function:
running it surfaces exactly which checks don't exist, which reversible
actions can't be auto-fixed, and which K2 envelopes are stale.

The brief format:
  1. TOP 3 BLOCKERS        — what stops the organism from breathing
  2. SAFE-NOW QUEUE        — reversible actions that cleared all gates
  3. NEEDS-K2 QUEUE        — irreversible actions awaiting signature
  4. P-SCORES SNAPSHOT     — organism health at a glance
  5. RECENT CHANGES        — what moved since last brief

Usage:
    python3 generate_operator_brief.py > brief_2026-05-08.md
    python3 generate_operator_brief.py --date 2026-05-08 --output-dir ~/briefs/

Exit codes:
    0  brief generated
    1  critical state unreadable (blockers may be underestimated)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ============================================================================
# CONFIG — paths relative to Magnum Opus root
# ============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
STATE_SURFACES = {
    "runtime_truth": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "ORGANISM_RUNTIME_TRUTH.md",
    "p_scores": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "P-SCORES.md",
    "soma_log": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "08_SOMA_LOG" / "2026-05" / "events.md",
    "health_wiring": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "HEALTH_WIRING.md",
}
ORGAN_BRIEFS = {
    "TheCircle": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "TheCircle" / "00_BRIEF.md",
    "RealityFutures": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "RealityFutures" / "00_BRIEF.md",
    "APU": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "ApuBot" / "00_BRIEF.md",
    "Skyzai": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "Skyzai" / "00_BRIEF.md",
    "EvolutionaryNetwork": PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "EvolutionaryNetwork" / "00_BRIEF.md",
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================
@dataclass
class Blocker:
    severity: str  # P0 | P1 | P2
    organ: str
    description: str
    evidence: str
    owner: str = ""

@dataclass
class SafeNowItem:
    action: str
    organ: str
    reversibility: str  # "fully_reversible" | "reversible_with_rollback"
    auto_fix_status: str  # "ready" | "blocked_by_missing_predicate"
    predicate_missing: str = ""

@dataclass
class NeedsK2Item:
    envelope_id: str
    organ: str
    description: str
    staged_at: str
    reversibility: str = "irreversible"

@dataclass
class OrganHealth:
    name: str
    code_p: float = 0.0
    runtime_p: float = 0.0
    phi: float = 0.0
    nu: float = 0.0
    status: str = "unknown"
    blocker_count: int = 0

@dataclass
class Brief:
    date: str
    blockers: list[Blocker] = field(default_factory=list)
    safe_now: list[SafeNowItem] = field(default_factory=list)
    needs_k2: list[NeedsK2Item] = field(default_factory=list)
    organ_health: list[OrganHealth] = field(default_factory=list)
    recent_commits: list[dict] = field(default_factory=list)
    a7_violations: int = 0
    health_status: str = "unknown"


# ============================================================================
# OBSERVE — collect raw state
# ============================================================================
def read_file(path: Path, max_lines: int = 200) -> str:
    """Read file, return empty string if missing."""
    if not path.exists():
        return ""
    try:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) > max_lines:
            return "\n".join(lines[:max_lines]) + f"\n... ({len(lines) - max_lines} more lines)"
        return text
    except Exception as e:
        return f"[READ ERROR: {e}]"


def parse_p_scores(text: str) -> list[OrganHealth]:
    """Extract organ P-scores from P-SCORES.md table."""
    organs: list[OrganHealth] = []
    # Match table rows: | **TheCircle** | IS (F1) | `0.53` (`Phi=0.80`, `V=0.66`) | `0.25` (`Phi=0.65`, `V=0.38`) |
    pattern = r"\|\s*\*\*([^*]+)\*\*\s*\|\s*[^|]+\|\s*`([0-9.]+)`\s*\(\`Phi=([0-9.]+)\`\s*,\s*\`V=([0-9.]+)\`.*?\)\s*\|\s*`([0-9.]+)`\s*\(\`Phi=([0-9.]+)\`\s*,\s*\`V=([0-9.]+)\`"
    for m in re.finditer(pattern, text, re.DOTALL):
        organs.append(OrganHealth(
            name=m.group(1).strip(),
            code_p=float(m.group(2)),
            phi=float(m.group(3)),
            nu=float(m.group(4)),
            runtime_p=float(m.group(5)),
        ))
    return organs


def parse_blockers_from_brief(text: str, organ_name: str) -> list[Blocker]:
    """Extract blockers from an organ BRIEF."""
    blockers: list[Blocker] = []
    # Look for "Blocker" or "P0" or "CRITICAL" sections
    for severity in ["P0", "P1", "P2"]:
        pattern = rf"(?:^|\n)\s*[-*]\s*(?:\[{severity}\]|{severity}).*?(?=\n\s*[-*]|\Z)"
        for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
            line = match.group(0).strip()
            # Clean up markdown
            line = re.sub(r"\[.*?\]", "", line)  # remove links
            line = re.sub(r"\*\*", "", line)  # remove bold
            line = line.strip("- *")
            if len(line) > 20:
                blockers.append(Blocker(
                    severity=severity,
                    organ=organ_name,
                    description=line[:200],
                    evidence="from_organ_brief",
                ))
    return blockers


def get_recent_commits(n: int = 10) -> list[dict]:
    """Get recent commits from git log."""
    try:
        result = subprocess.run(
            ["git", "log", f"--max-count={n}", "--pretty=format:%h|%s|%ci"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        commits: list[dict] = []
        for line in result.stdout.strip().split("\n"):
            if "|" in line:
                parts = line.split("|", 2)
                if len(parts) == 3:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1],
                        "date": parts[2][:10],
                    })
        return commits
    except Exception:
        return []


def run_health_check() -> str:
    """Try to run health.py, return status string."""
    health_path = PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "Agentz" / "health.py"
    if not health_path.exists():
        return "health.py not found"
    try:
        result = subprocess.run(
            [sys.executable, str(health_path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return "healthy"
        return f"unhealthy (rc={result.returncode})"
    except Exception as e:
        return f"check_failed: {e}"


def count_a7_violations() -> int:
    """Run a7_validator and count violations."""
    validator_path = PROJECT_ROOT / ".codex" / "agents" / "a7_validator.py"
    if not validator_path.exists():
        return -1
    try:
        result = subprocess.run(
            [sys.executable, str(validator_path), "--json"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        data = json.loads(result.stdout)
        return data.get("violations", -1)
    except Exception:
        return -1


# ============================================================================
# SELECT — filter state into actionable categories
# ============================================================================
def select_blockers(brief: Brief) -> list[Blocker]:
    """Select top blockers, deduplicate, rank by severity."""
    # Sort: P0 first, then P1, then P2
    severity_order = {"P0": 0, "P1": 1, "P2": 2}
    sorted_blockers = sorted(
        brief.blockers,
        key=lambda b: (severity_order.get(b.severity, 3), b.organ),
    )
    # Deduplicate by description similarity (simple: exact match on first 80 chars)
    seen: set[str] = set()
    deduped: list[Blocker] = []
    for b in sorted_blockers:
        key = b.description[:80].lower()
        if key not in seen:
            seen.add(key)
            deduped.append(b)
    return deduped[:10]  # cap at 10


def infer_safe_now_items(organ_health: list[OrganHealth], blockers: list[Blocker]) -> list[SafeNowItem]:
    """Infer what could be auto-executed based on health and blockers."""
    items: list[SafeNowItem] = []
    # Organs with runtime P > 0.5 and no P0 blockers are candidates for auto-actions
    blocker_organs = {b.organ for b in blockers if b.severity == "P0"}
    for oh in organ_health:
        if oh.name not in blocker_organs and oh.runtime_p > 0.5:
            items.append(SafeNowItem(
                action=f"{oh.name} routine cadence (health check, P-SCORE refresh)",
                organ=oh.name,
                reversibility="fully_reversible",
                auto_fix_status="ready",
            ))
        elif oh.name not in blocker_organs and oh.runtime_p <= 0.5:
            items.append(SafeNowItem(
                action=f"{oh.name} runtime P below threshold — needs attention before auto-action",
                organ=oh.name,
                reversibility="fully_reversible",
                auto_fix_status="blocked_by_missing_predicate",
                predicate_missing="runtime_p > 0.5 threshold not met",
            ))
    return items


def infer_needs_k2(organ_health: list[OrganHealth], blockers: list[Blocker]) -> list[NeedsK2Item]:
    """Infer what needs K2 signature."""
    items: list[NeedsK2Item] = []
    # P0 blockers that affect execution surfaces need K2 review
    for b in blockers:
        if b.severity == "P0" and b.organ in ("Skyzai", "APU"):
            items.append(NeedsK2Item(
                envelope_id=f"k2-review-{b.organ.lower()}-{b.severity}",
                organ=b.organ,
                description=f"P0 blocker: {b.description[:100]}",
                staged_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            ))
    # Organs with large code/runtime gaps also need K2 review for deployment decisions
    for oh in organ_health:
        gap = oh.code_p - oh.runtime_p
        if gap > 0.3:
            items.append(NeedsK2Item(
                envelope_id=f"k2-deploy-review-{oh.name.lower()}",
                organ=oh.name,
                description=f"Code/runtime gap = {gap:.2f}. Deploy to runtime?",
                staged_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            ))
    return items


# ============================================================================
# FORMAT — emit brief as markdown
# ============================================================================
def format_brief(brief: Brief) -> str:
    """Format brief as human-readable markdown."""
    lines: list[str] = []
    date_str = brief.date
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines.append("---")
    lines.append(f"title: \"Operator Brief — {date_str}\"")
    lines.append("type: operator-brief")
    lines.append(f"generated_at: \"{now}\"")
    lines.append(f"evidence_tier: \"[S] structural checks; [B] git log receipt; [I] inferred actions\"")
    lines.append("---")
    lines.append("")
    lines.append(f"# Operator Brief — {date_str}")
    lines.append("")
    lines.append(f"> Generated: {now} | Evidence: [S] structural + [B] git + [I] inferred")
    lines.append("")

    # --- TOP 3 BLOCKERS ---
    lines.append("## 🔴 Top Blockers")
    lines.append("")
    top_blockers = brief.blockers[:3]
    if top_blockers:
        for i, b in enumerate(top_blockers, 1):
            lines.append(f"{i}. **[{b.severity}] {b.organ}** — {b.description}")
            if b.evidence:
                lines.append(f"   *Evidence: {b.evidence}*")
    else:
        lines.append("No P0 blockers detected. Monitor P1/P2 below.")
    lines.append("")

    # All blockers table
    if brief.blockers:
        lines.append("### All Blockers")
        lines.append("")
        lines.append("| Severity | Organ | Description |")
        lines.append("|----------|-------|-------------|")
        for b in brief.blockers:
            desc = b.description[:80].replace("|", "\\|")
            lines.append(f"| {b.severity} | {b.organ} | {desc} |")
        lines.append("")

    # --- SAFE-NOW QUEUE ---
    lines.append("## 🟢 Safe-Now Queue (reversible)")
    lines.append("")
    ready = [x for x in brief.safe_now if x.auto_fix_status == "ready"]
    blocked = [x for x in brief.safe_now if x.auto_fix_status == "blocked_by_missing_predicate"]
    if ready:
        lines.append(f"**Ready ({len(ready)} items):**")
        for item in ready:
            lines.append(f"- [{item.organ}] {item.action}")
    else:
        lines.append("No reversible actions ready for auto-execution.")
    if blocked:
        lines.append("")
        lines.append(f"**Blocked ({len(blocked)} items):**")
        for item in blocked:
            lines.append(f"- [{item.organ}] {item.action}")
            lines.append(f"  *Missing: {item.predicate_missing}*")
    lines.append("")

    # --- NEEDS-K2 QUEUE ---
    lines.append("## 🟡 Needs-K2 Queue (irreversible)")
    lines.append("")
    if brief.needs_k2:
        lines.append(f"**{len(brief.needs_k2)} envelopes awaiting signature:**")
        lines.append("")
        lines.append("| ID | Organ | Description | Staged |")
        lines.append("|------|-------|-------------|--------|")
        for item in brief.needs_k2:
            desc = item.description[:60].replace("|", "\\|")
            lines.append(f"| `{item.envelope_id}` | {item.organ} | {desc} | {item.staged_at} |")
    else:
        lines.append("No irreversible actions awaiting K2 signature.")
    lines.append("")

    # --- P-SCORES SNAPSHOT ---
    lines.append("## 📊 P-SCORES Snapshot")
    lines.append("")
    if brief.organ_health:
        lines.append("| Organ | Code P | Runtime P | Φ | ν | Gap |")
        lines.append("|-------|--------|-----------|---|---|-----|")
        for oh in brief.organ_health:
            gap = oh.code_p - oh.runtime_p
            gap_str = f"{gap:+.2f}"
            lines.append(f"| {oh.name} | {oh.code_p:.2f} | {oh.runtime_p:.2f} | {oh.phi:.2f} | {oh.nu:.2f} | {gap_str} |")
    else:
        lines.append("P-SCORES not parseable.")
    lines.append("")
    lines.append(f"**Health check:** {brief.health_status}")
    lines.append(f"**A7 violations:** {brief.a7_violations if brief.a7_violations >= 0 else 'unavailable'}")
    lines.append("")

    # --- RECENT CHANGES ---
    lines.append("## 📝 Recent Changes")
    lines.append("")
    if brief.recent_commits:
        for c in brief.recent_commits[:5]:
            lines.append(f"- `{c['hash']}` ({c['date']}) — {c['message']}")
    else:
        lines.append("Git history unavailable.")
    lines.append("")

    # --- WHAT THIS BRIEF DOES NOT KNOW ---
    lines.append("## ⚠️  What This Brief Does Not Know")
    lines.append("")
    lines.append("The following checks were attempted but failed — these gaps mean")
    lines.append("the brief may be under-reporting blockers or over-reporting safety:")
    lines.append("")
    missing: list[str] = []
    if not STATE_SURFACES["runtime_truth"].exists():
        missing.append("ORGANISM_RUNTIME_TRUTH.md — runtime truth boundary unknown")
    if not STATE_SURFACES["p_scores"].exists():
        missing.append("P-SCORES.md — health metrics unavailable")
    if brief.a7_violations < 0:
        missing.append("a7_validator.py — evidence-tier discipline unchecked")
    if brief.health_status.startswith("check_failed") or brief.health_status == "health.py not found":
        missing.append("health.py — organism health check failed")
    if not missing:
        missing.append("All canonical checks passed. Brief is as complete as current instrumentation allows.")
    for m in missing:
        lines.append(f"- {m}")
    lines.append("")

    lines.append("---")
    lines.append("*This brief is a forcing function. If it looks thin, the instrumentation is thin.*")
    lines.append("*⊙ = • × ○*")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================
def generate_brief(date_str: str) -> Brief:
    """Observe → Select → Brief."""
    brief = Brief(date=date_str)

    # OBSERVE: P-SCORES
    p_scores_text = read_file(STATE_SURFACES["p_scores"])
    brief.organ_health = parse_p_scores(p_scores_text)

    # OBSERVE: Organ BRIEFs for blockers
    for organ_name, brief_path in ORGAN_BRIEFS.items():
        text = read_file(brief_path, max_lines=100)
        if text:
            blockers = parse_blockers_from_brief(text, organ_name)
            brief.blockers.extend(blockers)

    # OBSERVE: Runtime truth and P-SCORES gaps
    for source_name, source_path in [
        ("runtime_truth", STATE_SURFACES["runtime_truth"]),
        ("p_scores", STATE_SURFACES["p_scores"]),
    ]:
        text = read_file(source_path)
        in_gaps_section = False
        for line in text.splitlines():
            if any(marker in line for marker in ["Current Gaps", "Current Blocks", "Blocker", "P0 Blocker"]):
                in_gaps_section = True
                continue
            if in_gaps_section:
                if line.startswith("## ") or line.startswith("---") or line.startswith("| "):
                    in_gaps_section = False
                    continue
                if line.strip().startswith("-") or line.strip().startswith("*"):
                    desc = line.strip("- *").strip()
                    if len(desc) > 10 and not desc.startswith("|"):
                        brief.blockers.append(Blocker(
                            severity="P0",
                            organ="Organism",
                            description=desc[:200],
                            evidence=source_name,
                        ))

    # OBSERVE: Git history
    brief.recent_commits = get_recent_commits(10)

    # OBSERVE: Health check
    brief.health_status = run_health_check()

    # OBSERVE: A7 violations
    brief.a7_violations = count_a7_violations()

    # SELECT: Rank and deduplicate blockers
    brief.blockers = select_blockers(brief)

    # SELECT: Infer safe-now items
    brief.safe_now = infer_safe_now_items(brief.organ_health, brief.blockers)

    # SELECT: Infer needs-K2 items
    brief.needs_k2 = infer_needs_k2(brief.organ_health, brief.blockers)

    return brief


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate operator brief from organism state")
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                        help="Brief date (YYYY-MM-DD)")
    parser.add_argument("--output-dir", default="",
                        help="Directory to write brief_YYYY-MM-DD.md (default: stdout)")
    args = parser.parse_args()

    brief = generate_brief(args.date)
    markdown = format_brief(brief)

    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"brief_{args.date}.md"
        out_path.write_text(markdown, encoding="utf-8")
        print(f"Wrote: {out_path}")
    else:
        print(markdown)

    # Exit code: 1 if critical state unreadable
    if brief.health_status.startswith("check_failed") or brief.a7_violations < 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
