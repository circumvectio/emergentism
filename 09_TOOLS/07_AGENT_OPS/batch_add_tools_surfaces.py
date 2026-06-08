#!/usr/bin/env python3
"""Batch-add execution surfaces to 05_TOOLS dac_frame and simulation files."""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

with open(ROOT / "05_TOOLS" / "agent_ops" / "AGENT_GAPS.json", "r", encoding="utf-8") as f:
    gaps_data = json.load(f)

tools_files = [
    g for g in gaps_data["gaps"]
    if g["zone"] == "05_TOOLS" and g["missing_execution_surface"]
]

SURFACE_TEMPLATE = """
---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `{path}`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.
"""

modified = 0
errors = 0

for gap in tools_files:
    filepath = ROOT / gap["path"]
    try:
        content = filepath.read_text(encoding="utf-8")
        if "Agent Execution Surface" in content:
            continue
        surface = SURFACE_TEMPLATE.format(path=gap["path"])
        filepath.write_text(content + surface, encoding="utf-8")
        modified += 1
    except Exception as e:
        errors += 1
        print(f"  ⚠️  Error modifying {gap['path']}: {e}")

print(f"\n✅ Modified {modified} Tools files")
if errors:
    print(f"❌ Errors: {errors}")
