import os
import re

directories_to_scan = [
    "04_PWAs"
]

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find markdown links: [text](link)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, link in links:
            if link.startswith('http'):
                continue
            # Handle local links
            if link.startswith('#'):
                continue
                
            # If the link doesn't exist relative to the file's dir or root
            file_dir = os.path.dirname(filepath)
            link_path = os.path.join(file_dir, link)
            
            if not os.path.exists(link_path):
                print(f"BROKEN LINK in {filepath}: {link}")

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

for root_dir in directories_to_scan:
    abs_path = os.path.join(os.getcwd(), root_dir)
    for root, dirs, files in os.walk(abs_path):
        for file in files:
            if file.endswith('.md'):
                check_file(os.path.join(root, file))

print("Link check complete.")
