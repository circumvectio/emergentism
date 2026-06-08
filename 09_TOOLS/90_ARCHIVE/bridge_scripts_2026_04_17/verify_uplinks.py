import os
import re

UPLINK_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM/03_UPLINK"
corrupted = []
total = 0

for root, _, files in os.walk(UPLINK_DIR):
    for f in files:
        if f.endswith(".md"):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as fp:
                content = fp.read()
            total += 1
            if len(content.strip()) < 10:
                corrupted.append(f"{f} (Empty or too short)")
            elif "<!-- UPLINK: Auto-generated" in content and "<!-- From: " not in content and "Canonical Path:" not in content and "UPLINK:" not in content:
                corrupted.append(f"{f} (Missing body content)")

print(f"Scanned {total} UPLINK files.")
if corrupted:
    print("Found corrupted files:")
    for c in corrupted:
        print("  - " + c)
else:
    print("No corrupted files found. All payloads are structurally sound.")
