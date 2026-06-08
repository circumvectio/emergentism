#!/usr/bin/env python3
"""
Batch-add lightweight execution surfaces to PWA wiki/content files.

Usage:
    python batch_add_pwa_wiki_surfaces.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

# Load gaps
with open(ROOT / "05_TOOLS" / "agent_ops" / "AGENT_GAPS.json", "r", encoding="utf-8") as f:
    gaps_data = json.load(f)

wiki_files = [
    g for g in gaps_data["gaps"]
    if g["zone"] == "04_PWAs" and g["missing_execution_surface"] and "wiki" in g["path"]
]

other_pwa_files = [
    g for g in gaps_data["gaps"]
    if g["zone"] == "04_PWAs" and g["missing_execution_surface"] and "wiki" not in g["path"]
]

SURFACE_TEMPLATE = """
---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a downstream public content page.** The canonical source lives in `EMERGENTISM_ORG/08_FRAMEWORK_SUPPORT/` or `SKYZAI_ORG/`. Edit source upstream, not here.
2. **Preserve evidence tiers.** Do not upgrade `[I]` or `[C]` claims to `[A]`, `[B]`, or `[S]` when reproducing them here.
3. **Regenerate from source.** If the upstream source changes, regenerate this page rather than editing it independently.
4. **Canonical Path:** `{path}`

**Output:** This is content. Route edits to upstream source. Regenerate when source changes.
"""

modified = 0
errors = 0

for gap in wiki_files + other_pwa_files:
    filepath = ROOT / gap["path"]
    try:
        content = filepath.read_text(encoding="utf-8")
        # Skip if already has execution surface (double-check)
        if "Agent Execution Surface" in content:
            continue
        surface = SURFACE_TEMPLATE.format(path=gap["path"])
        filepath.write_text(content + surface, encoding="utf-8")
        modified += 1
    except Exception as e:
        errors += 1
        print(f"  ⚠️  Error modifying {gap['path']}: {e}")

print(f"\n✅ Modified {modified} PWA files")
if errors:
    print(f"❌ Errors: {errors}")
