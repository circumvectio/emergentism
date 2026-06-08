import os
import re

UPLINK_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM/03_UPLINK"
OUTPUT_DIR = os.path.join(UPLINK_DIR, "NOTEBOOK_LM_PACKAGES")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Get all directories in UPLINK_DIR
subdirs = [d for d in os.listdir(UPLINK_DIR) 
           if os.path.isdir(os.path.join(UPLINK_DIR, d)) 
           and not d.startswith(".")]

def minify_for_context(text):
    text = re.sub(r'<!--(?!\s*(UPLINK|From|Warning)).*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'\n{4,}', '\n\n', text)
    return text.strip()

for folder in subdirs:
    if folder == "NOTEBOOK_LM_PACKAGES":
        continue
    
    target_path = os.path.join(UPLINK_DIR, folder)
    output_path = os.path.join(OUTPUT_DIR, f"{folder}_MASTER.md")
    
    combined_content = []
    combined_content.append(f"# UPLINK DATAROOM FOR: {folder}\n")
    combined_content.append(f"This is the compressed, unified architectural context for {folder}, ready for Notebook LM ingestion.\n\n")
    
    file_count = 0
    # Process files in deterministic order to ensure readability
    for root, _, files in os.walk(target_path):
        for f in sorted(files):
            if f.endswith(".md"):
                file_path = os.path.join(root, f)
                with open(file_path, 'r', encoding='utf-8') as file_in:
                    content = file_in.read()
                
                rel_path = os.path.relpath(file_path, target_path)
                combined_content.append(f"--- START OF DOCUMENT: {rel_path} ---")
                combined_content.append(minify_for_context(content))
                combined_content.append(f"--- END OF DOCUMENT: {rel_path} ---\n\n")
                file_count += 1
                
    if file_count > 0:
        with open(output_path, 'w', encoding='utf-8') as file_out:
            file_out.write("\n".join(combined_content))
        print(f"Generated {folder}_MASTER.md ({os.path.getsize(output_path) / 1024:.2f} KB) from {file_count} files.")
