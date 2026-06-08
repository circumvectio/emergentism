import os

UPLINK_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM/03_UPLINK"
report = []

total_files = 0
healthy = 0
warnings = 0
errors = 0

for root, _, files in os.walk(UPLINK_DIR):
    for f in sorted(files):
        if f.endswith(".md") and f not in ["NOTEBOOK_LM_MASTER.md", "README.md"]:
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, UPLINK_DIR)
            total_files += 1
            
            with open(filepath, 'r', encoding='utf-8') as fp:
                content = fp.read()
                
            size = len(content)
            
            note_flags = []
            status = "PASS"
            
            if size < 80:
                note_flags.append(f"Empty payload.")
                status = "FAIL"
                errors += 1
                
            unclosed = content.count("<!--") - content.count("-->")
            if unclosed != 0:
                note_flags.append(f"Unclosed HTML ({unclosed}).")
                status = "WARN"
                warnings += 1
                
            if "..." in content and "[truncated" in content:
                note_flags.append("Size-capped safely")
                
            if status == "FAIL" or status == "WARN":
                report.append(f"[{status}] {rel_path} - {', '.join(note_flags)}")

if not report:
    print(f"✅ Deep Validation Passed: '{total_files}' UPLINK Files structurally flawless.")
else:
    print(f"Out of {total_files} files, found {len(report)} files with issues:")
    print("\n".join(report))
