#!/usr/bin/env python3
"""
Uplink Compiler — Auto-generates EMERGENTISM_ORG/11_UPLINK/ from source documents.

Reads the living codebase and compiles the 11 Uplink files automatically.
Run after every major change to keep the Uplink current.

Usage:
    python compile_uplink.py                    # Compile all 11 files
    python compile_uplink.py --file 09_STATE    # Compile one file
    python compile_uplink.py --check            # Check if Uplink is stale

The Cortex compiler pattern applied to the Uplink.
"""

import os
import sys
import json
import time
import re
import subprocess
from pathlib import Path
from datetime import datetime


# --- Configuration ---

ROOT = Path(__file__).resolve().parents[2]  # 01_EMERGENTISM/
REPO_ROOT = ROOT.parent
UPLINK_DIR = ROOT / "11_UPLINK"
CORE_UPLINK_DIR = UPLINK_DIR / "00_CORE"
RECONCILIATION_UPLINK_DIR = UPLINK_DIR / "10_RECONCILIATION"
ORGANISM_DIR = REPO_ROOT / "2_SKYZAI_ORG"
FRAMEWORK_DIR = ROOT / "08_FRAMEWORK_SUPPORT"
MANAGEMENT_DIR = ORGANISM_DIR / "05_PROJECT_MANAGEMENT"

# Source files for each Uplink document
SOURCES = {
    "01_SEED.md": [
        # The seed is hand-written — it's the 30-line compressed essence
        # Don't auto-generate. Just verify it's not stale.
    ],
    "02_FRAMEWORK.md": [
        ROOT / "02_EPISTEMOLOGY" / "01_EVIDENCE_TIERS" / "00_THE_HONEST_POSITION.md",
        FRAMEWORK_DIR / "00_START_HERE.md",
    ],
    "03_ORGANISM.md": [
        ORGANISM_DIR / "09_REFERENCE" / "00_DAC_BLUEPRINT.md",
        ORGANISM_DIR / "VISION.md",
        ROOT / "05_COSMOLOGY" / "01_THE_TRANSCENDENTAL_TRINITY" / "22_THE_TELEOLOGY.md",
    ],
    "04_ECONOMICS.md": [
        ORGANISM_DIR / "09_REFERENCE" / "00_DAC_BLUEPRINT.md",
        # SoResFi spec in TheCircle
    ],
    "05_ARCHITECTURE.md": [
        ORGANISM_DIR / "09_REFERENCE" / "00_DAC_BLUEPRINT.md",
        ORGANISM_DIR / "P-SCORES.md",
    ],
    "06_AGENTS.md": [
        ORGANISM_DIR / "02_ORGANS" / "Skyzai" / "VMOSK_A.md",
    ],
    "07_NEXUS.md": [
        ORGANISM_DIR / "02_ORGANS" / "Skyzai" / "membrane" / "00_NEXUS_SPEC.md",
    ],
    "08_PRODUCTS.md": [
        REPO_ROOT / "4_ENTITIES" / "HELIOS" / "00_BRIEF.md",
        REPO_ROOT / "4_ENTITIES" / "AUREUS" / "00_BRIEF.md",
    ],
    "09_STATE.md": [
        ORGANISM_DIR / "P-SCORES.md",
        ORGANISM_DIR / "CLAUDE.md",
        ORGANISM_DIR / "ORGANISM_RUNTIME_TRUTH.md",
        MANAGEMENT_DIR / "CANON_INDEX.md",
    ],
    "10_GLOSSARY.md": [
        # Glossary is compiled from all sources
    ],
}

UPLINK_TARGETS = {
    "01_SEED.md": CORE_UPLINK_DIR / "01_SEED.md",
    "02_FRAMEWORK.md": CORE_UPLINK_DIR / "02_FRAMEWORK.md",
    "03_ORGANISM.md": CORE_UPLINK_DIR / "03_ORGANISM.md",
    "04_ECONOMICS.md": CORE_UPLINK_DIR / "04_ECONOMICS.md",
    "05_ARCHITECTURE.md": CORE_UPLINK_DIR / "05_ARCHITECTURE.md",
    "06_AGENTS.md": CORE_UPLINK_DIR / "06_AGENTS.md",
    "07_NEXUS.md": CORE_UPLINK_DIR / "07_NEXUS.md",
    "08_PRODUCTS.md": CORE_UPLINK_DIR / "08_PRODUCTS.md",
    "09_STATE.md": CORE_UPLINK_DIR / "09_STATE.md",
    "10_GLOSSARY.md": RECONCILIATION_UPLINK_DIR / "10_GLOSSARY.md",
}


def get_file_mtime(path: Path) -> float:
    """Get file modification time, or 0 if not found."""
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return 0


def count_files(path: Path) -> int:
    """Count files while pruning obvious archive and tool noise."""
    try:
        result = subprocess.run(
            [
                "rg",
                "--files",
                str(path),
                "-g",
                "!**/_legacy/**",
                "-g",
                "!**/_LEGACY/**",
                "-g",
                "!**/.git/**",
                "-g",
                "!**/.venv/**",
                "-g",
                "!**/node_modules/**",
                "-g",
                "!**/__pycache__/**",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return sum(1 for line in result.stdout.splitlines() if line.strip())
    except (subprocess.SubprocessError, FileNotFoundError):
        count = 0
        for root, dirs, files in os.walk(path):
            dirs[:] = [
                d for d in dirs
                if "_legacy" not in d
                and "_LEGACY" not in d
                and d not in {".git", ".venv", "node_modules", "__pycache__"}
            ]
            for name in files:
                if "_legacy" in name or "_LEGACY" in name:
                    continue
                count += 1
        return count


def extract_first_table(content: str, header_pattern: str) -> list[str]:
    """Extract the first markdown table after a matching header."""
    lines = content.splitlines()
    seen_header = False
    table = []

    for line in lines:
        if not seen_header and re.match(header_pattern, line):
            seen_header = True
            continue

        if seen_header and line.startswith("|"):
            table.append(line)
            continue

        if seen_header and table and not line.strip():
            break

    return table


def rewrite_p_scores_links_for_uplink(table: list[str]) -> list[str]:
    """Rewrite P-SCORES.md-relative links for the generated Uplink state file."""
    return [
        line.replace("](02_ORGANS/", "](../../../02_SKYZAI/01_NOOSPHERE/02_ORGANS/")
        for line in table
    ]


def check_staleness() -> dict[str, bool]:
    """Check which Uplink files are older than their sources."""
    results = {}
    for uplink_file, source_files in SOURCES.items():
        uplink_path = UPLINK_TARGETS.get(uplink_file, UPLINK_DIR / uplink_file)
        uplink_mtime = get_file_mtime(uplink_path)

        if uplink_mtime == 0:
            results[uplink_file] = True  # Missing = stale
            continue

        stale = False
        for source in source_files:
            if source.exists() and source.stat().st_mtime > uplink_mtime:
                stale = True
                break
        results[uplink_file] = stale

    return results


def compile_09_state():
    """Compile a legacy 09_STATE.md sketch from current file counts and partial status inputs.

    This is not a complete live-state authority surface. Proof links, current runtime
    truth, and richer P-score synthesis still require manual or higher-level AI review.
    """
    p_scores_path = ORGANISM_DIR / "P-SCORES.md"
    if not p_scores_path.exists():
        return None

    content = p_scores_path.read_text()

    # Count files per organ
    organs = {}
    organs_dir = ORGANISM_DIR / "02_ORGANS"
    runtime_organs = {"TheCircle", "RealityFutures", "ApuBot", "Skyzai"}
    for organ_path in sorted(
        p
        for p in organs_dir.iterdir()
        if p.is_dir() and p.name in runtime_organs
    ):
        organs[organ_path.name] = count_files(organ_path)

    # Count files per entity
    entities = {}
    entities_dir = REPO_ROOT / "4_ENTITIES"
    for entity_path in sorted(p for p in entities_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        entities[entity_path.name] = count_files(entity_path)

    p_score_table = extract_first_table(content, r"^## Organ")
    p_score_table = rewrite_p_scores_links_for_uplink(p_score_table)

    latest_symbiosis = None
    symbiosis_dir = ORGANISM_DIR / "02_ORGANS" / "Skyzai" / "memory" / "symbiosis_traces"
    if symbiosis_dir.exists():
        candidates = sorted(symbiosis_dir.glob("symbiosis_*.json"), reverse=True)
        if candidates:
            try:
                latest_symbiosis = json.loads(candidates[0].read_text())
                latest_symbiosis["_path"] = str(candidates[0].relative_to(REPO_ROOT))
            except Exception:
                latest_symbiosis = None

    # Generate state document
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# THE STATE — Auto-compiled {now}",
        "",
        "> Auto-generated by compile_uplink.py as a partial state sketch.",
        "> Do not edit directly.",
        "> Read `SKYZAI_ORG/ORGANISM_RUNTIME_TRUTH.md`,",
        "> `SKYZAI_ORG/05_PROJECT_MANAGEMENT/CANON_INDEX.md`, and",
        "> `SKYZAI_ORG/P-SCORES.md` before making present-tense claims.",
        "",
        "## P-Scores (from P-SCORES.md)",
        "",
    ]

    if p_score_table:
        lines.extend(p_score_table)
    else:
        lines.append("_P-score table unavailable; read `SKYZAI_ORG/P-SCORES.md` directly._")

    lines.extend([
        "",
        "## File Counts (Current)",
        "",
        "### Organs",
        "",
    ])

    for name, count in organs.items():
        lines.append(f"- **{name}:** {count} files")

    lines.extend(["", "### Entities", ""])
    for name, count in entities.items():
        lines.append(f"- **{name}:** {count} files")

    lines.extend([
        "",
        "## Current Operating Shape",
        "",
        "- `NEXUS` acquires",
        "- `Private Business Account` converts",
        "- `API PAY` activates",
        "- `Events` prove",
        "- `POS` scales",
        "- `Cortex + AIA` compound",
        "",
    ])

    lines.extend([
        "## Current Route Snapshot",
        "",
        "_This block is read from the latest symbiosis trace. Treat it as historical route telemetry, not the canonical status board. `P-SCORES.md`, `ORGANISM_RUNTIME_TRUTH.md`, and dated organ receipts outrank these labels when they disagree._",
        "",
    ])

    route_summary = ((latest_symbiosis or {}).get("confederation") or {}).get("route_summary") or {}
    conf_organs = ((latest_symbiosis or {}).get("confederation") or {}).get("per_organ") or {}
    if route_summary:
        lines.extend([
            f"- route state: `{route_summary.get('route_state')}`",
            f"- sensing: `{route_summary.get('sensing')}`",
            f"- pricing: `{route_summary.get('pricing')}`",
            f"- judgment: `{route_summary.get('judgment')}`",
            f"- execution: `{route_summary.get('execution')}`",
        ])
        blockers = route_summary.get("top_blockers") or []
        resolved_blocker_markers = (
            "F3 status stale in BRIEF",
            "Backbone adapter orphaned",
        )
        blockers = [
            blocker
            for blocker in blockers
            if not any(marker in blocker for marker in resolved_blocker_markers)
        ]
        if blockers:
            lines.append("- trace blockers:")
            for blocker in blockers[:5]:
                lines.append(f"  - {blocker}")
            if any("No live F1 input" in blocker for blocker in blockers):
                lines.append("- note: `No live F1 input` here refers to the live deployed symbiosis route.")
                lines.append("- note: bounded local F1 proof now exists separately, including a fresh-source TheCircle -> APU -> Skyzai loop.")
        if latest_symbiosis and latest_symbiosis.get("_path"):
            lines.append(f"- source trace: `{latest_symbiosis['_path']}`")
    elif conf_organs:
        lines.append("- confederation witnesses exist, but route summary was unavailable at compile time")
    else:
        lines.append("- no symbiosis trace found; read the latest digest and symbiosis trace directly")

    lines.extend([
        "",
        "## Reading Rule",
        "",
        "Do not read this page as permission to relaunch stale launch claims or",
        "the old flat parallel-organ stack.",
        "",
        "Read it as a compressed bridge anchored to the rooted proof sequence:",
        "",
        "`NEXUS -> Private Business Account -> API PAY -> proof loop -> POS later`",
        "",
        "And read any route summary as assistance, not authority:",
        "",
        "`micro organ readings -> macro route picture -> human judgment -> K2`",
        "",
        "---",
        "",
        f"*Compiled: {now}*",
    ])

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Uplink Compiler")
    parser.add_argument("--check", action="store_true", help="Check staleness only")
    parser.add_argument("--file", type=str, help="Compile a single file (e.g., 09_STATE)")
    args = parser.parse_args()

    if args.check:
        print("Uplink Staleness Check")
        print("=" * 50)
        staleness = check_staleness()
        any_stale = False
        for filename, is_stale in staleness.items():
            status = "STALE ⚠️" if is_stale else "OK ✓"
            print(f"  {status}  {filename}")
            if is_stale:
                any_stale = True

        if any_stale:
            print("\nRun `python compile_uplink.py` to recompile stale files.")
            sys.exit(1)
        else:
            print("\nAll Uplink files are current.")
            sys.exit(0)

    if args.file:
        target = args.file if args.file.endswith(".md") else f"{args.file}.md"
        print(f"Compiling: {target}")
        if target == "09_STATE.md":
            content = compile_09_state()
            if content:
                target_path = UPLINK_TARGETS[target]
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(content)
                print(f"  Written: {target_path}")
        else:
            print(f"  Auto-compilation not yet implemented for {target}")
            print("  (09_STATE.md is only a legacy partial auto-compile surface; other files still need manual or AI-driven review.)")
        return

    # Full compilation
    print("Uplink Full Compilation")
    print("=" * 50)

    # Check what's stale
    staleness = check_staleness()
    stale_count = sum(1 for v in staleness.values() if v)
    print(f"  {stale_count} files need recompilation")

    # Compile 09_STATE (the one we can fully auto-generate)
    print("\n  Compiling 09_STATE.md...")
    content = compile_09_state()
    if content:
        target_path = UPLINK_TARGETS["09_STATE.md"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content)
        print("  ✓ 09_STATE.md compiled as a legacy partial state sketch from file counts + manual status text")

    # For other files: report staleness but don't auto-generate
    # (They require LLM-level summarization which this script can't do)
    print("\n  Other files require LLM compilation:")
    for filename, is_stale in staleness.items():
        if filename == "09_STATE.md":
            continue
        if is_stale:
            sources = SOURCES.get(filename, [])
            source_names = [s.name for s in sources if s.exists()]
            print(f"  ⚠️ {filename} is stale (sources: {', '.join(source_names) or 'check manually'})")

    print("\n  To recompile stale files: ask an AI agent to read the sources")
    print("  and regenerate the Uplink file. The Cortex compiler pattern.")
    print()
    print("  Done. ⊙ = • × ○")


if __name__ == "__main__":
    main()
