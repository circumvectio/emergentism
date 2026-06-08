import os

sources = {
    "00_BRIEF.md": open("../../02_ORGANS/05_THECIRCLE/00_BRIEF.md").read(),
    "00_CONTEXT.md": open("../../02_ORGANS/05_THECIRCLE/00_CONTEXT.md").read(),
    "00_VMOSK.md": open("../../02_ORGANS/05_THECIRCLE/00_VMOSK.md").read(),
}

mappings = {
    "THECIRCLE_00_IDENTITY.md": ["00_CONTEXT.md"],
    "THECIRCLE_01_STATE.md": ["00_BRIEF.md", "00_CONTEXT.md"],
    "THECIRCLE_02_ARCHITECTURE.md": ["00_CONTEXT.md"],
    "THECIRCLE_03_PRODUCT.md": ["00_CONTEXT.md"],
    "THECIRCLE_04_CONSTITUTION.md": ["00_VMOSK.md"],
    "THECIRCLE_05_SPRINT.md": ["00_BRIEF.md", "00_VMOSK.md"],
    "THECIRCLE_06_CONTEXT.md": ["00_CONTEXT.md", "00_VMOSK.md"],
}

for fname, src_names in mappings.items():
    content = f"<!-- UPLINK: Auto-generated. Sources: [{', '.join(['02_ORGANS/05_THECIRCLE/' + s for s in src_names])}] Generated: 2026-04-09 -->\n\n"
    for src in src_names:
        content += f"<!-- From: 02_ORGANS/05_THECIRCLE/{src} -->\n"
        content += sources[src] + "\n\n"
    
    with open(f"05_THECIRCLE/{fname}", "w") as f:
        f.write(content)

print("THECIRCLE fixed manually via script!")
