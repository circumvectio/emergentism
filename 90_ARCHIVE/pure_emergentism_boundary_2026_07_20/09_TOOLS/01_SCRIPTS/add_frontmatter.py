#!/usr/bin/env python3
"""
Add YAML frontmatter to markdown files that lack it.
Maps file paths to layer/organ/entity tags automatically.

Usage: python3 add_frontmatter.py [--dry-run]
"""

import os
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent.parent
DRY_RUN = "--dry-run" in sys.argv

# Layer mapping from folder prefix
LAYER_MAP = {
    "00_INTAKE": "L1",
    "01_FRAMEWORK": "L2",
    "02_ORGANISM": "L3",
    "03_UPLINK": "L4",
    "04_PWAs": "L5",
    "05_TOOLS": "L6",
    "06_SEED": "L7",
}

# Organ mapping
ORGAN_MAP = {
    "TheCircle": "circle",
    "RealityFutures": "refu",
    "ApuBot": "apu",
    "Skyzai": "skyzai",
}

# Entity mapping
ENTITY_MAP = {
    "FOUNDATION": "foundation",
    "MENEXUS": "menexus",
    "QNTM": "qntm",
}

def get_layer(rel_path: str) -> str:
    parts = rel_path.split("/")
    if parts:
        return LAYER_MAP.get(parts[0], "")
    return ""

def get_organ(rel_path: str) -> str:
    for key, val in ORGAN_MAP.items():
        if key in rel_path:
            return val
    return ""

def get_entity(rel_path: str) -> str:
    for key, val in ENTITY_MAP.items():
        if key in rel_path:
            return val
    return ""

def get_type_tag(filename: str) -> str:
    name = filename.lower()
    if "brief" in name: return "brief"
    if "spec" in name or "blueprint" in name: return "spec"
    if "audit" in name: return "audit"
    if "roadmap" in name: return "roadmap"
    if "pr_faq" in name: return "pr_faq"
    if "gap_analysis" in name: return "gap_analysis"
    if "readme" in name: return "index"
    if "claude" in name: return "agent_config"
    if "summary" in name: return "summary"
    return "doc"

def title_from_filename(filename: str) -> str:
    name = Path(filename).stem
    # Remove number prefixes like "00-" or "01_"
    name = re.sub(r"^\d+[-_]", "", name)
    # Convert underscores/hyphens to spaces and title case
    return name.replace("_", " ").replace("-", " ").title()

def has_frontmatter(content: str) -> bool:
    return content.startswith("---\n")

def build_frontmatter(rel_path: str, filename: str) -> str:
    title = title_from_filename(filename)
    layer = get_layer(rel_path)
    organ = get_organ(rel_path)
    entity = get_entity(rel_path)
    type_tag = get_type_tag(filename)

    tags = []
    if layer: tags.append(f"layer/{layer}")
    if organ: tags.append(f"organ/{organ}")
    if entity: tags.append(f"entity/{entity}")
    tags.append(f"type/{type_tag}")

    lines = ["---"]
    lines.append(f"title: \"{title}\"")
    if tags:
        lines.append(f"tags: [{', '.join(tags)}]")
    if layer:
        lines.append(f"layer: {layer}")
    if organ:
        lines.append(f"organ: {organ}")
    if entity:
        lines.append(f"entity: {entity}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)

def process_file(filepath: Path) -> bool:
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False

    if has_frontmatter(content):
        return False

    rel_path = str(filepath.relative_to(ROOT))
    fm = build_frontmatter(rel_path, filepath.name)

    if DRY_RUN:
        print(f"WOULD ADD frontmatter to: {rel_path}")
        return True

    filepath.write_text(fm + content, encoding="utf-8")
    return True

def main():
    # Target directories: Uplink + Organism root + organ briefs + entity briefs + wikis
    targets = [
        ROOT / "03_UPLINK",
        ROOT / "02_ORGANISM",
    ]

    # Also target all wiki directories
    for wiki_dir in ROOT.glob("SKYZAI_ORG/**/wiki"):
        targets.append(wiki_dir)
    for wiki_dir in ROOT.glob("SKYZAI_ORG/09_PWAs/skyzai_org/wiki"):
        targets.append(wiki_dir)

    count = 0
    for target in targets:
        if not target.exists():
            continue
        # Only process direct children (not recursive for root dirs)
        if target == ROOT / "02_ORGANISM":
            files = list(target.glob("*.md"))
        else:
            files = list(target.rglob("*.md"))

        for f in files:
            if process_file(f):
                count += 1

    action = "Would add" if DRY_RUN else "Added"
    print(f"\n{action} frontmatter to {count} files.")

if __name__ == "__main__":
    main()
