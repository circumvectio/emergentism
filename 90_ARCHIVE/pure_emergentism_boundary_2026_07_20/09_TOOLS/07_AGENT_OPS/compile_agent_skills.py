from pathlib import Path
import glob
import os
import re

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BASE_DIR = PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE"
OUTPUT_DIR = BASE_DIR / "02_ORGANS" / "Agentz" / "intake" / "agent_skills"

# Regex patterns to extract RA data
# Handling bold markers mapping out the header metadata
domain_pattern = re.compile(r"\*\*Domain:\*\*\s*(.*?)\s*\|")
expert_pattern = re.compile(r"\*\*Expert Type:\*\*\s*(.*?)(?:\s*\||\n|$)")

def extract_section(text, header_name):
    """Extracts text under a specific markdown header until the next H2 or horizontal rule."""
    # Look for the header
    pattern = re.compile(rf"## {header_name}\s*(.*?)(?=\n## |\n---|\Z)", re.DOTALL | re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return "Not specified."

def process_ra(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata
    domain_match = domain_pattern.search(content)
    expert_match = expert_pattern.search(content)
    
    domain = domain_match.group(1).strip() if domain_match else "Unknown Domain"
    expert = expert_match.group(1).strip() if expert_match else "AI Agent Specialist"

    # Extract sections
    question = extract_section(content, "The Question")
    background = extract_section(content, "Background Provided")
    sub_questions = extract_section(content, "Specific Sub-Questions")
    deliverables = extract_section(content, "Deliverable Requirements")
    success = extract_section(content, "Success Criteria")
    kill = extract_section(content, "Kill Criterion")

    # Generate Agent Prompt Syntax
    prompt = f"""# SYSTEM PROMPT: {os.path.basename(filepath).replace('.md', '')}

## IDENTITY
You are an autonomous AI expert agent operating within the APU orchestrator.
**Domain:** {domain}
**Persona / Expert Sub-Type:** {expert}

## PRIMARY OBJECTIVE
{question}

## CONTEXT & BACKGROUND
{background}

## REQUIRED SUB-TASKS
{sub_questions}

## OUTPUT DELIVERABLES
You must structure your final output to satisfy these requirements:
{deliverables}

## SUCCESS METRICS
Your output will be graded against the following criteria:
{success}

## CRITICAL FAIL-STATE (KILL CRITERION)
WARNING - Avoid this condition at all costs:
{kill}
"""
    return prompt

def main():
    # Ensure output directory exists only when the compiler is actually run.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find all RA files
    ra_files = glob.glob(str(BASE_DIR / "**" / "RA-*.md"), recursive=True)
    print(f"Found {len(ra_files)} RA files.")

    count = 0
    for filepath in ra_files:
        # Determine the organ/entity name by looking at the path parts
        parts = Path(filepath).parts
        # Organism structure looks like: .../02_ORGANS/05_THECIRCLE/06_INTAKE/01_RESEARCH_ASSIGNMENTS/RA-01.md
        # Entity structure looks like: .../01_ENTITIES/04_VAYAN/...
        organ_name = "UNKNOWN"
        for i, part in enumerate(parts):
            if part in ("01_ENTITIES", "02_ORGANS") and i + 1 < len(parts):
                # Grab the folder name right after (e.g., 05_THECIRCLE)
                # Strip the number prefix
                organ_name = re.sub(r'^\d+_', '', parts[i + 1])
                break
        
        basename = os.path.basename(filepath)
        safe_name = f"SKILL_AGENT_{organ_name}_{basename}"
        
        output_path = OUTPUT_DIR / safe_name
        prompt = process_ra(filepath)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        count += 1

    print(f"Successfully compiled {count} Agent Skill prompts into {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
