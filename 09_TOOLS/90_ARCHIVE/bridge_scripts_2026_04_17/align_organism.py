import os
import re

TARGET_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM"

# Patterns to replace
REPLACEMENTS = [
    ("02_ORGANISM", "02_ORGANISM"),
    ("05_MENEXUS", "05_MENEXUS"),
    ("../../../01_Emergentism_FRAMEWORK/01_THE_AXIOMS", "../../../01_Emergentism_FRAMEWORK/01_THE_AXIOMS"),
    ("../../01_Emergentism_FRAMEWORK/01_THE_AXIOMS", "../../01_Emergentism_FRAMEWORK/01_THE_AXIOMS")
]

ignore_dirs = {'.git', 'node_modules', '.next', '.claude', '__pycache__', 'websites', '06_ARCHIVE'}

files_updated = 0

for root, dirs, files in os.walk(TARGET_DIR):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for file in files:
        if file.endswith('.md') or file.endswith('.json') or file.endswith('.py') or file.endswith('.toml'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue

            new_content = content
            for old_pat, new_pat in REPLACEMENTS:
                new_content = new_content.replace(old_pat, new_pat)

            if new_content != content:
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_updated += 1
                except Exception:
                    pass

print(f"\nTotal files updated (resume): {files_updated}")
