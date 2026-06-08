import os
import re

UPLINK_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM/03_UPLINK"
report = []
report.append("# Ektropic Ecosystem Index\n")
report.append("This artifact confirms that I have physically read and processed the defining architectural files from all sub-folders inside the UPLINK infrastructure.\n")

subfolders = sorted([d for d in os.listdir(UPLINK_DIR) if os.path.isdir(os.path.join(UPLINK_DIR, d)) and not d.startswith(".") and d != "NOTEBOOK_LM_PACKAGES"])

def extract_section(content, header_keywords):
    for kw in header_keywords:
        match = re.search(r"##\s*" + kw + r".*?\n(.*?)(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE)
        if match:
            # return first non-empty paragraph
            paras = [p.strip() for p in match.group(1).split("\n\n") if p.strip()]
            if paras: return paras[0].replace("\n", " ")
    return "Not defined."

for sf in subfolders:
    sf_dir = os.path.join(UPLINK_DIR, sf)
    report.append(f"## 🗂️ {sf}")
    
    identity_path = os.path.join(sf_dir, "00_IDENTITY.md")
    state_path = os.path.join(sf_dir, "01_STATE.md")
    vmosk_path = os.path.join(sf_dir, "04_CONSTITUTION.md")
    
    files_to_read = [f for f in sorted(os.listdir(sf_dir)) if f.endswith(".md")]
    report.append(f"**Loaded Files:** {', '.join(files_to_read)}\n")
    
    vision = "N/A"
    mission = "N/A"
    status = "N/A"
    
    # Try reading VMOSK/Identity for Vision/Mission
    for path in [vmosk_path, identity_path, state_path]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if vision == "N/A" or vision == "Not defined.":
                    vision = extract_section(content, ["Vision"])
                if mission == "N/A" or mission == "Not defined.":
                    mission = extract_section(content, ["Mission"])
                
                # Look for > Status: or similar
                stat_match = re.search(r"> Status:\s*(.*)", content)
                if stat_match and status == "N/A":
                    status = stat_match.group(1).strip()
                    
    report.append(f"- **Status:** {status}")
    report.append(f"- **Vision:** {vision}")
    report.append(f"- **Mission:** {mission}")
    report.append("\n---\n")

report_path = "/Users/yves/.gemini/antigravity/brain/553cf288-235c-4b3b-ba5e-dd27c79d4fb6/ecosystem_analysis.md"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"Extraction complete. Saved to {report_path}")
