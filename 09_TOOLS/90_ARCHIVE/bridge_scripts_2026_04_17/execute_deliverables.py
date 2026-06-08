import os
import json
import urllib.request
import asyncio
from pathlib import Path

# --- Configuration ---
ROOT_DIR = Path("/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM")
SYSTEM_PROMPT = """
You are VMOSK, the intelligence architecture of the Emergentism Framework. 
You are formalizing a Research Deliverable.
DO NOT use academic fluff, preambles, or apologies.
Utilize Hyper-Dense formatting. Map constraints into P=Φ×V logic.
Execute the Deliverable Requirements natively against the K*=0 limit.
Provide directly the markdown text of the deliverable output.
Do not wrap it in markdown codeblocks like ```markdown. Just output the content.
"""

# Try to get API keys from environment
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


async def call_llm_api(prompt: str) -> str:
    """Cascade through available LLM APIs to generate the deliverable."""
    if ANTHROPIC_KEY:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}]
        }
    elif OPENAI_KEY:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
            "content-type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        }
    elif GEMINI_KEY:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"
        headers = {
            "content-type": "application/json"
        }
        data = {
            "contents": [{"parts": [{"text": SYSTEM_PROMPT + "\n\n" + prompt}]}]
        }
    else:
        raise ValueError("Neither ANTHROPIC_API_KEY, OPENAI_API_KEY, nor GEMINI_API_KEY environment variables found.")

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    
    # Use loop to run blocking request
    loop = asyncio.get_event_loop()
    def _make_req():
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    
    resp_json = await loop.run_in_executor(None, _make_req)

    # Parse response based on API
    if ANTHROPIC_KEY:
        return resp_json["content"][0]["text"]
    elif OPENAI_KEY:
        return resp_json["choices"][0]["message"]["content"]
    elif GEMINI_KEY:
        return resp_json["candidates"][0]["content"]["parts"][0]["text"]


async def process_assignment(ra_file: Path, semaphore: asyncio.Semaphore):
    """Processes a single RA file and saves the deliverable."""
    async with semaphore:
        # Determine paths
        intake_dir = ra_file.parent.parent  # .../06_INTAKE/
        deliverables_dir = intake_dir / "02_DELIVERABLES"
        deliverable_file = deliverables_dir / f"DELIVERABLE_{ra_file.name}"

        # Skip if already executed
        if deliverable_file.exists():
            print(f"[SKIP] Deliverable already exists for {ra_file.name}")
            return

        print(f"[PROCESS] Executing research for {ra_file.name}...")

        # Ensure deliverables directory exists
        deliverables_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(ra_file, 'r', encoding='utf-8') as f:
                content = f.read()

            prompt = f"Execute the following specific Research Assignment file. Target exact kill criteria and output structural truth.\n\n[RA_FILE_START]\n{content}\n[RA_FILE_END]\n"

            # Hit the LLM
            deliverable_text = await call_llm_api(prompt)

            # Write the deliverable
            with open(deliverable_file, 'w', encoding='utf-8') as f:
                f.write(deliverable_text)

            print(f"[SUCCESS] Synthesized DELIVERABLE_{ra_file.name}")

        except Exception as e:
            print(f"[ERROR] Failed to process {ra_file.name}: {e}")


async def main():
    print(f"--- VMOSK Recursive Research Extractor ---")
    
    # Identify all RA files
    ra_files = list(ROOT_DIR.rglob("06_INTAKE/01_RESEARCH_ASSIGNMENTS/RA-*.md"))
    print(f"Discovered {len(ra_files)} total Research Assignments.")
    
    if not any([ANTHROPIC_KEY, OPENAI_KEY, GEMINI_KEY]):
        print("[FATAL] You must export ANTHROPIC_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY in your shell.")
        return

    # To avoid rate limits, execute 5 concurrently
    semaphore = asyncio.Semaphore(5)
    
    tasks = [process_assignment(file, semaphore) for file in ra_files]
    await asyncio.gather(*tasks)
    
    print("\n[COMPLETE] 06_INTAKE/02_DELIVERABLES successfully populated across the organism.")

if __name__ == "__main__":
    asyncio.run(main())
