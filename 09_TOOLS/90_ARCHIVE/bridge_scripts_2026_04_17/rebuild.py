#!/usr/bin/env python3
"""
Rebuild the 03_UPLINK AI context packages from their canonical sources.

v4: Intelligent Semantic Blockchain Parsing
    - Fixes the regex \s table-destruction bug.
    - Operates on entire markdown logic blocks (paragraphs/tables) rather than blindly slicing single lines.
    - Retains semantic integrity for closed tags and table layouts.
"""

import os
import re
from datetime import datetime

COMPILER_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(COMPILER_DIR)
UPLINK_DIR = os.path.join(ROOT_DIR, "02_THE_MAP_LEFT_BRAIN", "03_UPLINK")
ORGANISM_DIR = os.path.join(ROOT_DIR, "02_ORGANISM")
TERRITORY_DIR = os.path.join(ROOT_DIR, "01_THE_TERRITORY_RIGHT_BRAIN")

MAX_BYTES = 3 * 1024  # ~3KB per source section
MAX_TOTAL = 8 * 1024  # ~8KB per uplink file total

HEADER_REGEX = re.compile(
    r"(?:>|<!--)\s*UPLINK:\s*Auto-generated\. Sources:\s*\[(.*?)\](?:.*?Generated:.*?)?(?:-->)?"
)

PATH_MAP = {
    "02_ORGANS/04_APUBOT/Agent.md": "02_ORGANS/04_APUBOT/00_ONE_PAGER.md",
    "02_ORGANS/07_EMERGENTISM/Agent.md": "02_ORGANS/07_EMERGENTISM/00_BRIEF.md",
    "01_ENTITIES/01_OFN/Agent.md": "01_ENTITIES/01_OFN/00_VMOSK.md",
    "01_ENTITIES/02_SKYZAI/Agent.md": "01_ENTITIES/02_SKYZAI/00_BRIEF.md",
    "01_ENTITIES/03_FOUNDATION/Agent.md": "01_ENTITIES/03_FOUNDATION/00_BRIEF.md",
    "01_ENTITIES/04_VAYAN/Agent.md": "01_ENTITIES/04_VAYAN/00_BRIEF.md",
    "01_ENTITIES/05_MENEXUS_GMBH/Agent.md": "01_ENTITIES/05_MENEXUS_GMBH/00_BRIEF.md",
    "02_ORGANS/02_HELIOS/Agent.md": "02_ORGANS/02_HELIOS/00_GARDENER_NEXUS.md",
    "02_ORGANS/05_THECIRCLE/Agent.md": "02_ORGANS/05_THECIRCLE/00_BRIEF.md",
    "02_ORGANS/08_THE_CORTEX/Agent.md": "02_ORGANS/08_THE_CORTEX/00_GARDENER_NEXUS.md",
    "02_ORGANS/03_NEXUS/Agent.md": "02_ORGANS/03_NEXUS/00_GARDENER_NEXUS.md",
    "02_ORGANS/06_REALITYFUTURES/Agent.md": "02_ORGANS/06_REALITYFUTURES/00_BRIEF.md",
    "02_ORGANS/01_AUREUS/Agent.md": "02_ORGANS/01_AUREUS/00_BRIEF.md",
    "02_ORGANS/04_APUBOT/SOUL.md": "02_ORGANS/04_APUBOT/runtime/SOUL.md",
    "02_ORGANS/04_APUBOT/00_BRIEF.md": "02_ORGANS/04_APUBOT/00_ONE_PAGER.md",
    "02_ORGANS/04_APUBOT/00_CONTEXT.md": "02_ORGANS/04_APUBOT/00_PRODUCT_NARRATIVE.md",
    "02_ORGANS/04_APUBOT/00_VMOSK.md": "08_THE_DEPLOYMENT/04_APUBOT/00_VMOSK_APU.md",
    "02_ORGANS/04_APUBOT/02_GATE_G1_SPEC.md": "02_ORGANS/04_APUBOT/99_ARCHIVE/02_GATE_G1_SPEC.md",
    "05_INFRASTRUCTURE/01_AIA/00_CHAIRMAN_BRIEF/00_BRIEF.md": "04_PROJECT_MANAGEMENT/00_CHAIRMAN_BRIEF/00_BRIEF.md",
    "05_INFRASTRUCTURE/01_AIA/00_CHAIRMAN_BRIEF/01_BRIEF_015.md": "04_PROJECT_MANAGEMENT/00_CHAIRMAN_BRIEF/01_BRIEF_016.md",
}


def heal_path(src_str):
    s = src_str.strip()
    if s in PATH_MAP:
        return PATH_MAP[s]
    if s.endswith("Agent.md"):
        dirname = os.path.dirname(s)
        for candidate in [
            "00_BRIEF.md",
            "00_IDENTITY.md",
            "00_GARDENER_NEXUS.md",
            "README.md",
        ]:
            path = os.path.join(dirname, candidate) if dirname else candidate
            if os.path.exists(os.path.join(ORGANISM_DIR, path)):
                return path
    return s


def extract_key_sections(text, max_bytes):
    """Extract semantically intact blocks (headers, tables, lists, contextual paragraphs) without shearing logic."""
    if len(text.encode("utf-8")) <= max_bytes:
        return text

    # Split safely by paragraphs / logical structures, NOT arbitrary lines.
    blocks = re.split(r'\n\s*\n', text)
    output = []
    total = 0
    paras_after_header = 0

    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        block_bytes = len(block.encode("utf-8")) + 2 # +2 for newline joining overhead
        
        if total + block_bytes > max_bytes:
            if total > 0:
                output.append("... [truncated — see canonical path] ...")
            break

        # Always include Headers
        if block.startswith("#"):
            output.append(block)
            total += block_bytes
            paras_after_header = 0
            continue

        # Always include Tables (identified by pipe characters and newlines)
        if "|" in block and block.startswith("|") or ("|" in block and "\n|" in block):
            output.append(block)
            total += block_bytes
            continue

        # Always include Bullet points / Lists
        if block.startswith("-") or block.startswith("*") or bool(re.match(r"^\d+\.", block)):
            output.append(block)
            total += block_bytes
            continue

        # Always include Constitutional bounds
        if any(kw in block.lower() for kw in ["η = 0", "η=0", "k*=0", "constitutional", "kill criterion", "execution surface", "p-score", "vmosk", "blocker"]):
            output.append(block)
            total += block_bytes
            continue

        # Include up to 2 contextual paragraphs following any header
        if paras_after_header < 2:
            output.append(block)
            total += block_bytes
            paras_after_header += 1
            continue

    return "\n\n".join(output)


def minify_markdown(text):
    # Strip HTML comments unless they are metadata tags (UPLINK, From, Warning)
    text = re.sub(r"<!--(?!\s*(UPLINK|From|Warning)).*?-->", "", text, flags=re.DOTALL)
    
    # Use spatial [ \t] trimming instead of \s so we DON'T destroy Markdown \n boundaries for tables.
    text = re.sub(r"[ \t]+\|", "|", text)
    text = re.sub(r"\|[ \t]+", "|", text)
    
    # Compress massive spacing
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()


def rebuild_all():
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    broken_count = 0
    capped_count = 0

    for root, dirs, files in os.walk(UPLINK_DIR):
        for file in sorted(files):
            if not file.endswith(".md"):
                continue

            filepath = os.path.join(root, file)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            match = HEADER_REGEX.search(content)
            if not match:
                continue

            sources_str = match.group(1)
            raw_sources = [
                s.strip()
                for s in sources_str.split(",")
                if s.strip() and s.strip() != "..."
            ]

            valid_sources = []
            source_contents = []

            for raw_src in raw_sources:
                healed_src = heal_path(raw_src)

                fallback_paths = [
                    os.path.normpath(os.path.join(ORGANISM_DIR, healed_src)) if healed_src.startswith("../") else os.path.join(ORGANISM_DIR, healed_src),
                    os.path.join(TERRITORY_DIR, healed_src.replace("02_ORGANS/08_THE_CORTEX", "08_THE_CORTEX")),
                    os.path.join(TERRITORY_DIR, healed_src.replace("../01_Emergentism_FRAMEWORK", "01_Emergentism_FRAMEWORK")),
                    os.path.join(ROOT_DIR, "02_THE_MAP_LEFT_BRAIN", healed_src)
                ]

                src_path = None
                for p in fallback_paths:
                    if os.path.exists(p):
                        src_path = p
                        break

                if src_path:
                    if healed_src not in valid_sources:
                        valid_sources.append(healed_src)
                        with open(src_path, "r", encoding="utf-8") as f:
                            src_content = f.read().strip()
                        src_content = minify_markdown(src_content)
                        src_content = extract_key_sections(src_content, MAX_BYTES)
                        source_contents.append((healed_src, src_content))
                else:
                    print(f"  BROKEN: [{raw_src}] -> [{healed_src}]")
                    broken_count += 1

            if not valid_sources:
                print(f"  EMPTY: {filepath} — removing")
                os.remove(filepath)
                continue

            total_bytes = 0
            new_content = []
            metadata_block = [
                f"> UPLINK: Auto-generated. Sources: [{', '.join(valid_sources)}] Generated: {today}\n"
            ]

            for healed_src, src_content in source_contents:
                remaining = max(MAX_TOTAL - total_bytes, 512)
                body = src_content
                if len(body.encode("utf-8")) > remaining:
                    body = extract_key_sections(body, remaining)
                    capped_count += 1
                metadata_block.append(f"> From: {healed_src}\n")
                new_content.append(body)
                total_bytes += len(body.encode("utf-8"))
                new_content.append("\n---\n")
                if total_bytes >= MAX_TOTAL:
                    break

            # Append the metadata at the bottom so Google parser doesn't crash on pseudo-frontmatter.
            new_content.extend(metadata_block)

            final_output = "\n".join(new_content)
            if final_output.endswith("\n---\n\n"):
                final_output = final_output[:-5]
            elif final_output.endswith("\n---\n"):
                final_output = final_output[:-5]

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(final_output + "\n")

            count += 1

    print(f"\n{'=' * 50}")
    print(f"UPLINK REBUILD v4 COMPLETE (Semantic Extraction Base)")
    print(f"  Rebuilt:     {count} files")
    print(f"  Broken:      {broken_count} refs (skipped)")
    print(f"  Size-capped: {capped_count} logic blocks gracefully compressed")
    print(f"  Cap:         {MAX_BYTES}B/source, {MAX_TOTAL}B/file")
    print(f"  Date:        {today}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    rebuild_all()
