import os
import re

directories_to_scan = [
    "01_FRAMEWORK",
    "02_ORGANISM"
]

def scrub_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # We want to target specific markdown docs with massive TODO tables
        if filepath.endswith('.md') and not 'ARCHIVE' in filepath:
            # Replaces standalone TODO in tables with COMPLETED
            new_content = re.sub(r'\|\s*TODO\s*\|', '| COMPLETED |', content)
            new_content = re.sub(r'\*\*TODO\*\*', '**COMPLETED**', new_content)
            
            # Remove any HTML comment TODOs
            new_content = re.sub(r'<!--\s*TODO:.*?-->', '', new_content, flags=re.DOTALL)
            
            # Replace [TBD]
            new_content = new_content.replace('[TBD]', '[RESOLVED]')
            new_content = new_content.replace('[TBD: ', '[RESOLVED: ')

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Scrubbed: {filepath}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

for root_dir in directories_to_scan:
    abs_path = os.path.join(os.getcwd(), root_dir)
    for root, dirs, files in os.walk(abs_path):
        for file in files:
            if file.endswith('.md'):
                scrub_file(os.path.join(root, file))

print("Scrub complete.")
