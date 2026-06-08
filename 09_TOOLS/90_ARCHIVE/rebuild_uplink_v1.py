#!/usr/bin/env python3
"""
UPLINK Rebuild Script
Regenerates all AI project context folders from the dataroom source files.

Usage:
    python3 rebuild.py              # Rebuild all
    python3 rebuild.py OFN          # Rebuild one
    python3 rebuild.py --check      # Check if UPLINKs are stale
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Dynamic Origin Routing 
# Navigate from 03_UPLINK up to the Root cleanly.
# ---------------------------------------------------------------------------
DATAROOM = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Source mappings: which files feed each UPLINK
# Keys are relative to DATAROOM (Root). Each UPLINK gets 7 output files.
# ---------------------------------------------------------------------------

UPLINK_SOURCES = {
    # ------------------------------------------------------------------
    # ORGANISM — The full organism overview (DAC_BLUEPRINT)
    # ------------------------------------------------------------------
    "ORGANISM": {
        "00_IDENTITY.md": ["02_ORGANISM/00_DAC_BLUEPRINT.md", "02_ORGANISM/00_TELEOLOGY.md"],
        "01_STATE.md": ["02_ORGANISM/00_DAC_BLUEPRINT.md"],
        "02_ARCHITECTURE.md": ["02_ORGANISM/00_DAC_BLUEPRINT.md", "02_ORGANISM/00_TELEOLOGY.md"],
        "03_PRODUCT.md": ["02_ORGANISM/00_DAC_BLUEPRINT.md"],
        "04_CONSTITUTION.md": ["02_ORGANISM/00_DAC_BLUEPRINT.md"],
        "05_SPRINT.md": ["02_ORGANISM/00_TELEOLOGY.md"],
        "06_CONTEXT.md": ["02_ORGANISM/00_DAC_BLUEPRINT.md", "02_ORGANISM/00_TELEOLOGY.md"],
    },

    # ------------------------------------------------------------------
    # Skyzai — The platform (Brahma)
    # ------------------------------------------------------------------
    "Skyzai": {
        "00_IDENTITY.md": ["02_ORGANISM/Skyzai/VMOSK_A.md"],
        "01_STATE.md": ["02_ORGANISM/Skyzai/VMOSK_A.md"],
        "02_ARCHITECTURE.md": ["02_ORGANISM/Skyzai/VMOSK_A.md"],
        "03_PRODUCT.md": ["02_ORGANISM/Skyzai/VMOSK_A.md"],
        "04_CONSTITUTION.md": ["02_ORGANISM/Skyzai/VMOSK_A.md"],
        "05_SPRINT.md": ["02_ORGANISM/Skyzai/VMOSK_A.md"],
        "06_CONTEXT.md": ["02_ORGANISM/Skyzai/VMOSK_A.md"],
    },

    # ------------------------------------------------------------------
    # APUBOT — The charioteer (L4)
    # ------------------------------------------------------------------
    "APUBOT": {
        "00_IDENTITY.md": ["02_ORGANISM/ApuBot/VMOSK_A.md"],
        "01_STATE.md": ["02_ORGANISM/ApuBot/VMOSK_A.md"],
        "02_ARCHITECTURE.md": ["02_ORGANISM/ApuBot/VMOSK_A.md"],
        "03_PRODUCT.md": ["02_ORGANISM/ApuBot/VMOSK_A.md"],
        "04_CONSTITUTION.md": ["02_ORGANISM/ApuBot/VMOSK_A.md"],
        "05_SPRINT.md": ["02_ORGANISM/ApuBot/VMOSK_A.md"],
        "06_CONTEXT.md": ["02_ORGANISM/ApuBot/VMOSK_A.md"],
    },

    # ------------------------------------------------------------------
    # THECIRCLE — Observation commons (L5)
    # ------------------------------------------------------------------
    "THECIRCLE": {
        "00_IDENTITY.md": ["02_ORGANISM/TheCircle/VMOSK_A.md"],
        "01_STATE.md": ["02_ORGANISM/TheCircle/VMOSK_A.md"],
        "02_ARCHITECTURE.md": ["02_ORGANISM/TheCircle/VMOSK_A.md"],
        "03_PRODUCT.md": ["02_ORGANISM/TheCircle/VMOSK_A.md"],
        "04_CONSTITUTION.md": ["02_ORGANISM/TheCircle/VMOSK_A.md"],
        "05_SPRINT.md": ["02_ORGANISM/TheCircle/VMOSK_A.md"],
        "06_CONTEXT.md": ["02_ORGANISM/TheCircle/VMOSK_A.md"],
    },

    # ------------------------------------------------------------------
    # REALITYFUTURES — Prediction markets (L6)
    # ------------------------------------------------------------------
    "REALITYFUTURES": {
        "00_IDENTITY.md": ["02_ORGANISM/RealityFutures/VMOSK_A.md"],
        "01_STATE.md": ["02_ORGANISM/RealityFutures/VMOSK_A.md"],
        "02_ARCHITECTURE.md": ["02_ORGANISM/RealityFutures/VMOSK_A.md"],
        "03_PRODUCT.md": ["02_ORGANISM/RealityFutures/VMOSK_A.md"],
        "04_CONSTITUTION.md": ["02_ORGANISM/RealityFutures/VMOSK_A.md"],
        "05_SPRINT.md": ["02_ORGANISM/RealityFutures/VMOSK_A.md"],
        "06_CONTEXT.md": ["02_ORGANISM/RealityFutures/VMOSK_A.md"],
    },

    # ------------------------------------------------------------------
    # AUREUS — Hard assets and property rights (L1)
    # ------------------------------------------------------------------
    "AUREUS": {
        "00_IDENTITY.md": ["04_PWAs/aureus_money/PR_FAQ.md", "02_ORGANISM/Skyzai/execution/aureus/VMOSK_A.md"],
        "01_STATE.md": ["04_PWAs/aureus_money/PR_FAQ.md"],
        "02_ARCHITECTURE.md": ["02_ORGANISM/Skyzai/execution/aureus/VMOSK_A.md"],
        "03_PRODUCT.md": ["04_PWAs/aureus_money/PR_FAQ.md"],
        "04_CONSTITUTION.md": ["02_ORGANISM/Skyzai/execution/aureus/VMOSK_A.md"],
        "05_SPRINT.md": ["04_PWAs/aureus_money/PR_FAQ.md"],
        "06_CONTEXT.md": ["02_ORGANISM/Skyzai/execution/aureus/VMOSK_A.md"],
    },

    # ------------------------------------------------------------------
    # HELIOS — Hardware, sensors, energy (L3)
    # ------------------------------------------------------------------
    "HELIOS": {
        "00_IDENTITY.md": ["04_PWAs/helios_you/PR_FAQ.md", "02_ORGANISM/Skyzai/execution/helios/VMOSK_A.md"],
        "01_STATE.md": ["04_PWAs/helios_you/PR_FAQ.md"],
        "02_ARCHITECTURE.md": ["02_ORGANISM/Skyzai/execution/helios/VMOSK_A.md"],
        "03_PRODUCT.md": ["04_PWAs/helios_you/PR_FAQ.md"],
        "04_CONSTITUTION.md": ["02_ORGANISM/Skyzai/execution/helios/VMOSK_A.md"],
        "05_SPRINT.md": ["04_PWAs/helios_you/PR_FAQ.md"],
        "06_CONTEXT.md": ["02_ORGANISM/Skyzai/execution/helios/VMOSK_A.md"],
    },
}

def get_uplink_dir(name: str) -> Path:
    """Returns the perfectly valid Cortex UPLINK destination directory."""
    return DATAROOM / "02_ORGANISM" / "Skyzai" / "memory" / "cortex" / "UPLINKS" / name

def read_source(path: str) -> str:
    full_path = DATAROOM / path
    if not full_path.exists():
        return f"<!-- SOURCE NOT FOUND: {path} -->"
    return full_path.read_text(encoding="utf-8")

def generate_header(sources: list, uplink_name: str, filename: str) -> str:
    source_list = ", ".join(sources)
    return (
        f"<!-- UPLINK: Auto-generated. "
        f"Sources: [{source_list}] "
        f"Generated: {datetime.now().strftime('%Y-%m-%d')} -->\n"
    )

def rebuild_uplink(name: str, dry_run: bool = False) -> int:
    if name not in UPLINK_SOURCES:
        print(f"  Unknown UPLINK: {name}")
        return 0

    uplink_dir = get_uplink_dir(name)
    if not dry_run:
        uplink_dir.mkdir(parents=True, exist_ok=True)

    files_written = 0
    for filename, sources in UPLINK_SOURCES[name].items():
        header = generate_header(sources, name, filename)
        contents = []
        missing = []
        for source in sources:
            full_path = DATAROOM / source
            if not full_path.exists():
                missing.append(source)
                contents.append(f"<!-- SOURCE NOT FOUND: {source} -->")
            else:
                content = full_path.read_text(encoding="utf-8")
                contents.append(f"<!-- From: {source} -->\n{content}")

        if missing:
            for m in missing:
                print(f"  WARNING: source not found: {m}")

        body = "\n\n---\n\n".join(contents)
        output_text = header + "\n" + body

        output = uplink_dir / filename
        if dry_run:
            print(f"  [dry-run] Would write UPLINKS/{name}/{filename} ({len(sources)} sources)")
        else:
            output.write_text(output_text, encoding="utf-8")
        files_written += 1

    verb = "Would rebuild" if dry_run else "Rebuilt"
    print(f"  {verb} UPLINK/{name}/ ({files_written} files)")
    return files_written

def check_staleness() -> list:
    stale = []
    for name, files in UPLINK_SOURCES.items():
        uplink_dir = get_uplink_dir(name)
        for filename, sources in files.items():
            output = uplink_dir / filename
            if not output.exists():
                stale.append(f"{name}/{filename}: MISSING")
                continue
            output_mtime = output.stat().st_mtime
            for source in sources:
                source_path = DATAROOM / source
                if source_path.exists() and source_path.stat().st_mtime > output_mtime:
                    stale.append(f"{name}/{filename}: stale (source {source} newer)")
                    break
    return stale

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--check":
            stale = check_staleness()
            if stale:
                print("Stale UPLINKs:")
                for s in stale:
                    print(f"  {s}")
                sys.exit(1)
            else:
                print("All UPLINKs are current")
            return
        if arg == "--dry-run":
            print("Dry run -- no files will be written\n")
            total = 0
            for name in sorted(UPLINK_SOURCES):
                total += rebuild_uplink(name, dry_run=True)
            print(f"\n  Would rebuild {len(UPLINK_SOURCES)} UPLINKs ({total} files total)")
            return
        rebuild_uplink(arg)
        return

    print(f"Rebuilding all {len(UPLINK_SOURCES)} UPLINKs...\n")
    total = 0
    for name in sorted(UPLINK_SOURCES):
        total += rebuild_uplink(name)
    print(f"\n  All {len(UPLINK_SOURCES)} UPLINKs rebuilt ({total} files total)")

if __name__ == "__main__":
    main()
