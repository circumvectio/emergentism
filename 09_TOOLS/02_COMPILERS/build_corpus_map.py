#!/usr/bin/env python3
"""
build_corpus_map.py — Generate holographic synecdoche navigation

Edit _corpus_source.yaml, run this script, all folders update.
Each folder gets 00_CORPUS.md: the whole corpus seen from that folder's perspective.

The whole is present at every point on S².
The perspective differs by position.

•   ⊙   ○
"""
import yaml
import os
import sys

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CORPUS_ROOT = os.path.dirname(SCRIPT_PATH)
SOURCE = os.path.join(CORPUS_ROOT, "_corpus_source.yaml")
OUTPUT_NAME = "00_CORPUS.md"
GENERATED_MARKER = "<!-- GENERATED FILE — DO NOT EDIT DIRECTLY. Edit _corpus_source.yaml and run build_corpus_map.py -->"


def load_source():
    with open(SOURCE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def relative_path(from_folder, to_path):
    """Compute relative markdown link path from one folder to another."""
    return os.path.relpath(
        os.path.join(CORPUS_ROOT, to_path), os.path.join(CORPUS_ROOT, from_folder)
    )


def render_cycle(data, current_folder_id):
    """Render the cosmological cycle with YOU ARE HERE marker."""
    lines = []

    for stage in data["cycle"]:
        lines.append(f"### {stage['dimension']}")
        lines.append(f"*{stage['symbol']}* — {stage['description']}")
        lines.append("")

        for folder in stage["folders"]:
            is_here = folder["id"] == current_folder_id
            marker = "  **⟵ YOU ARE HERE**" if is_here else ""

            if is_here:
                lines.append(
                    f"- **`{folder['id']}/`** — {folder['role']}{marker}"
                )
            else:
                lines.append(f"- `{folder['id']}/` — {folder['role']}")

            # Key docs as sub-bullets with relative links
            for doc in folder.get("key_docs", []):
                full_path = f"{folder['id']}/{doc}"
                rel = relative_path(current_folder_id, full_path)
                lines.append(f"  - [{doc}]({rel})")

        lines.append("")

    return "\n".join(lines)


def render_nav_table(data, current_folder_id):
    """Render the navigation table with relative links to canonical docs."""
    canon = [
        ("README.md", "**This folder's own guide**", "README.md"),
        ("00_GOVERNANCE/00_DATA_ROOM.md", "Master navigation by cosmological tier", None),
        ("00_GOVERNANCE/00_SYSTEM_MAP.md", "Complete architecture (960+ files)", None),
        ("00_EMERGENTISM.md", "The complete Weltanschauung", None),
        ("00_THE_HONEST_POSITION.md", "Canonical epistemic status of every claim", None),
        ("00_GLOSSARY.md", "Every term defined", None),
        ("00_FOREWORD.md", "Entry point: three numbers, one equation", None),
    ]

    lines = [
        "| Document | Purpose |",
        "|----------|---------|",
    ]

    for name, purpose, override_path in canon:
        if override_path:
            rel = override_path
        else:
            rel = relative_path(current_folder_id, name)
        display_name = name.split("/")[-1]
        lines.append(f"| [{display_name}]({rel}) | {purpose} |")

    return "\n".join(lines)


def generate_for_folder(data, folder_id):
    """Generate the full 00_CORPUS.md for one folder."""
    meta = data["meta"]

    sections = [
        GENERATED_MARKER,
        "",
        f"# THE WHOLE — seen from `{folder_id}/`",
        "",
        f"> {meta['equation']}",
        f"> {meta['balance']}",
        "",
        "---",
        "",
        "## The Corpus",
        "",
        data["abstract"].strip(),
        "",
        "---",
        "",
        "## The Cosmological Cycle",
        "",
        "```",
        meta["cycle_flow"].strip(),
        "```",
        "",
        render_cycle(data, folder_id),
        "---",
        "",
        "## Canonical Navigation",
        "",
        render_nav_table(data, folder_id),
        "",
        "---",
        "",
        f"*{meta['equation']}*",
        "",
        f"*Generated from `_corpus_source.yaml` — {meta['date']}*",
        "",
    ]

    return "\n".join(sections)


def main():
    if not os.path.isfile(SOURCE):
        print(f"ERROR: {SOURCE} not found")
        sys.exit(1)

    data = load_source()

    # Collect all folder IDs
    all_folders = []
    for stage in data["cycle"]:
        for folder in stage["folders"]:
            all_folders.append(folder["id"])

    generated = 0
    for folder_id in all_folders:
        target_dir = os.path.join(CORPUS_ROOT, folder_id)
        if not os.path.isdir(target_dir):
            print(f"  WARNING: {folder_id}/ does not exist, skipping")
            continue

        output_path = os.path.join(target_dir, OUTPUT_NAME)
        content = generate_for_folder(data, folder_id)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  ⊙  {folder_id}/{OUTPUT_NAME}")
        generated += 1

    print(f"\n{generated} holographic views generated from _corpus_source.yaml")
    print("•   ⊙   ○")


if __name__ == "__main__":
    main()
