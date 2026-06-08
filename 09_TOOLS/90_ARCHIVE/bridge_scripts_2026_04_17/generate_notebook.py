import os
import re

UPLINK_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM/03_UPLINK"
OUTPUT_FILE = os.path.join(UPLINK_DIR, "NOTEBOOK_LM_MASTER.md")

combined_content = []
combined_content.append("# EMERGENTISM ORGANISM — COMPLETE AI CONTEXT UPLINK\n")
combined_content.append("This document is a highly compressed, token-optimized compilation of the entire Emergentism 14-entity organism architecture.\n")
combined_content.append("It is compiled explicitly for insertion into NotebookLM or other high-context agentic reasoning environments.\n\n")

print("Validating all UPLINK .md files for corruption before Master Compile...")
corrupted_files = []
total_processed = 0

for root, _, files in os.walk(UPLINK_DIR):
    for f in sorted(files):
        if f.endswith(".md") and f != "NOTEBOOK_LM_MASTER.md":
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file_in:
                content = file_in.read()
            
            # Simple corruption heuristic checks:
            if "<!DOCTYPE html>" in content or "\x00" in content:
                corrupted_files.append(filepath)
                continue
            
            rel_path = os.path.relpath(filepath, UPLINK_DIR)
            
            combined_content.append("=================================================================")
            combined_content.append(f"DOCUMENT SOURCE: {rel_path}")
            combined_content.append("=================================================================\n")
            combined_content.append(content)
            combined_content.append("\n\n")
            total_processed += 1

if corrupted_files:
    print(f"Warning: Found {len(corrupted_files)} corrupted files and excluded them:")
    for c in corrupted_files:
        print(f"  - {c}")
else:
    print("Success: Zero corruption detected.")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as file_out:
    file_out.write("\n".join(combined_content))

size_kb = os.path.getsize(OUTPUT_FILE) / 1024
print(f"\nCompile Complete: {OUTPUT_FILE}")
print(f"Merged {total_processed} valid UPLINK files. Total payload size: {size_kb:.2f} KB")
