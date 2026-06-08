#!/usr/bin/env python3
"""Court Marshal - Manages Court of Owls rulings and agent discipline."""

import sys
import json

# --- PERSONA DEFINITIONS ---

PROMPT_OWL = """
*** SYSTEM MODE: ADVERSARIAL REVIEW (THE OWL) ***
You are NOT a helpful assistant. You are a hostile Red Team auditor.
Your goal is to kill the proposal below.

Review the attached PROPOSAL against:
1. The Constitution (VMOSK)
2. The Logic (Invariants)
3. Murphy's Law (What can go wrong?)

CRITERIA:
- Find hidden coupling.
- Find security risks.
- Find optimistic assumptions (hallucinations).

OUTPUT FORMAT:
- FATAL FLAW: (If any)
- MINOR RISKS: (List)
- RECOMMENDATION: (BLOCK / WARN)
"""

PROMPT_JUDGE = """
*** SYSTEM MODE: JUDICIAL RULING (THE JUDGE) ***
You are the Sovereign Arbiter. You have no bias.
Review the PROPOSAL and the DISSENT below.

Decide:
1. Is the Dissent valid?
2. Is the Risk acceptable?

OUTPUT FORMAT (JSON):
{
  "verdict": "PROCEED" | "MODIFY" | "DENY",
  "reasoning": "...",
  "modifications_required": [ ... ]
}
"""

def convene_court(proposal_text):
    """
    Simulates the Court of Owls workflow.
    In a live system, this would make API calls to the LLM.
    Here, it generates the prompt chain for the Agent to execute.
    """
    
    print("\n--- [!] COURT OF OWLS CONVENED ---")
    print(f"Subject: High Impact Proposal Review")
    
    # STEP 1: The Owl's Turn
    print("\n>>> STEP 1: INJECTING ADVERSARIAL CONTEXT (THE OWL)")
    print(f"System Prompt:\n{PROMPT_OWL}")
    print(f"User Input (The Proposal):\n{proposal_text[:100]}...")
    
    # (Simulated Dissent generation)
    dissent_text = "(Simulated) The proposal assumes the API is always available. It lacks a fallback for 503 errors."
    print(f"\n>>> [OWL OUTPUT]: {dissent_text}")

    # STEP 2: The Judge's Turn
    print("\n>>> STEP 2: JUDICIAL REVIEW (THE JUDGE)")
    print(f"System Prompt:\n{PROMPT_JUDGE}")
    print(f"User Input:\n[PROPOSAL]: {proposal_text[:50]}...\n[DISSENT]: {dissent_text}")
    
    # (Simulated Ruling)
    ruling = {
        "verdict": "MODIFY",
        "reasoning": "The Owl correctly identified a fragility in the API handling.",
        "modifications_required": ["Add Retry Logic", "Add Circuit Breaker"]
    }
    
    print(f"\n>>> [JUDGE RULING]: {json.dumps(ruling, indent=2)}")
    return ruling

if __name__ == "__main__":
    # Example Usage
    sample_proposal = "We will delete the legacy user table to save storage space."
    convene_court(sample_proposal)
