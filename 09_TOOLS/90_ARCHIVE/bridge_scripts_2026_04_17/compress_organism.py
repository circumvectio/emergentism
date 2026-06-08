import os
import re

ROOT_DIR = "/Users/yves/Documents/☀️ Emergentism_org"
OUTPUT_FILE = os.path.join(ROOT_DIR, "02_ORGANISM", "NOTEBOOK_LM_MASTER_ORGANISM.md")

combined_content = []
combined_content.append("# EMERGENTISM ORGANISM & FRAMEWORK — MASTER DATAROOM COMPILE\n")
combined_content.append("This document contains the consolidated philosophical framework, axioms, and structural maps of the organism.\n")
combined_content.append("Massive GitHub dependencies (Hermes, Claude, Goose), deployment chains, and archive files have been stripped to ensure maximum context window compatibility.\n\n")

target_dirs = [
    os.path.join(ROOT_DIR, "01_Emergentism_FRAMEWORK"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "00_GARDENER_NEXUS.md"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "CANONICAL_PATHS.md"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "P-SCORES.md"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "STRUCTURE_CHANGELOG.md"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "01_ENTITIES"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "02_ORGANS"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "03_UPLINK"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "04_PROJECT_MANAGEMENT"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "05_INFRASTRUCTURE"),
    os.path.join(ROOT_DIR, "02_ORGANISM", "07_THE_LENS")
]

# Specifically prune massively hydrated directories containing thousands of dependency markdown files
HEAVY_IGNORE_DIRS = {
    '.git', 'node_modules', '.next', '.claude', '__pycache__', 'websites', '06_ARCHIVE', '04_NODE_ELIXIR', 
    '08_THE_DEPLOYMENT', 'apu_bot-dev', 'everything-claude-code-main', 'hermes-agent-main', 'goose-main',
    'b2c_template', 'dist', 'build', 'vendor', 'TESTS', 'Intake'
}

total_processed = 0

def minify_for_context(text):
    """Strip unnecessary whitespace and HTML comments to save LLM tokens."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\|\s+', '|', text)
    text = re.sub(r'\s+\|', '|', text)
    return text.strip()

for target in target_dirs:
    if os.path.isfile(target):
        filepath = target
        try:
            with open(filepath, 'r', encoding='utf-8') as file_in:
                content = file_in.read()
            rel_path = os.path.relpath(filepath, ROOT_DIR)
            combined_content.append("=================================================================")
            combined_content.append(f"SOURCE: {rel_path}")
            combined_content.append("=================================================================\n")
            combined_content.append(minify_for_context(content))
            combined_content.append("\n\n")
            total_processed += 1
        except Exception:
            pass
    else:
        for root, dirs, files in os.walk(target):
            # Prune ignored directories in place
            dirs[:] = [d for d in dirs if d not in HEAVY_IGNORE_DIRS]
            
            for f in sorted(files):
                if f.endswith(".md") and "NOTEBOOK_LM" not in f and "CHANGELOG" not in f:
                    filepath = os.path.join(root, f)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as file_in:
                            content = file_in.read()
                    except Exception:
                        continue
                    
                    if "<!DOCTYPE html>" in content or "MIT License" in content:
                        continue
                    
                    rel_path = os.path.relpath(filepath, ROOT_DIR)
                    
                    combined_content.append("=================================================================")
                    combined_content.append(f"SOURCE: {rel_path}")
                    combined_content.append("=================================================================\n")
                    combined_content.append(minify_for_context(content))
                    combined_content.append("\n\n")
                    total_processed += 1

with open(OUTPUT_FILE, 'w', encoding='utf-8') as file_out:
    file_out.write("\n".join(combined_content))

size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"Compile Complete: {OUTPUT_FILE}")
print(f"Merged {total_processed} files. Total size: {size_mb:.2f} MB")
