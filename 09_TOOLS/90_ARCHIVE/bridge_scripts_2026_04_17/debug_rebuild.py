import re, os
MAX_BYTES = 6 * 1024

def extract_key_sections(text, max_bytes):
    if len(text.encode("utf-8")) <= max_bytes:
        return text

    lines = text.split("\n")
    output = []
    total = 0
    section_lines = 0

    for line in lines:
        line_bytes = len(line.encode("utf-8")) + 1
        if line.startswith("#"):
            output.append(line)
            total += line_bytes
            section_lines = 0
            continue
        if "|" in line and line.strip().startswith("|"):
            output.append(line)
            total += line_bytes
            continue
        if line.strip().startswith("- **") or line.strip().startswith("* **"):
            output.append(line)
            total += line_bytes
            continue
        if any(kw in line.lower() for kw in ["η = 0", "η=0", "k*=0", "constitutional"]):
            output.append(line)
            total += line_bytes
            continue
        if section_lines < 8:
            output.append(line)
            total += line_bytes
            section_lines += 1
            continue
        if total >= max_bytes * 0.95:
            output.append("")
            output.append(f"... [truncated — full source at canonical path] ...")
            break

    return "\n".join(output)

fpath = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM/08_THE_DEPLOYMENT/04_APUBOT/00_VMOSK_APU.md"
with open(fpath, "r", encoding="utf-8") as f:
    orig = f.read().strip()
    
result = extract_key_sections(orig, MAX_BYTES * 3)
print("EXTRACT KEY SECTIONS SIZE:", len(result))
print("First 200 chars:")
print(result[:200])
