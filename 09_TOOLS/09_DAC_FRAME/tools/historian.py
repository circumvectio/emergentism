#!/usr/bin/env python3
"""Historian - Tracks and analyzes historical changes and decisions."""

import re
import os
import collections
from datetime import datetime

# --- CONFIGURATION ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEARNINGS_FILE = os.path.join(PROJECT_ROOT, "07_WORK", "LEARNINGS.md")
PROPOSALS_DIR = os.path.join(PROJECT_ROOT, "07_WORK", "PROPOSALS")
THRESHOLD = 3  # The Rule of Three

def parse_learnings():
    """Reads LEARNINGS.md and extracts bullet points."""
    if not os.path.exists(LEARNINGS_FILE):
        print(f"[!] {LEARNINGS_FILE} not found. Creating dummy for demo.")
        create_dummy_data()
        
    with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract bullet points (-, *, +)
    bullets = re.findall(r"^[\-\*\+]\s+(.*)", content, re.MULTILINE)
    return bullets

def analyze_patterns(items):
    """
    Simple keyword clustering to find repeated failure modes.
    In a full LLM context, this would be a semantic embedding search.
    """
    # Stopwords to ignore
    stopwords = {'the', 'and', 'to', 'of', 'a', 'in', 'is', 'that', 'for', 'it', 'was', 'failure', 'error', 'this', 'with', 'from', 'have', 'were'}
    
    word_counts = collections.Counter()
    
    for item in items:
        # Normalize
        words = re.findall(r'\w+', item.lower())
        relevant_words = [w for w in words if w not in stopwords and len(w) > 3]
        word_counts.update(relevant_words)

    hotspots = [w for w, c in word_counts.items() if c >= THRESHOLD]
    
    final_clusters = {}
    for hotspot in hotspots:
        related_items = [item for item in items if hotspot in item.lower()]
        if len(related_items) >= THRESHOLD:
            final_clusters[hotspot] = related_items
            
    return final_clusters

def draft_amendment(keyword, evidence):
    """Generates a Constitutional Amendment Proposal."""
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"PROPOSAL_I-{timestamp}-{keyword.upper()}.md"
    filepath = os.path.join(PROPOSALS_DIR, filename)
    
    os.makedirs(PROPOSALS_DIR, exist_ok=True)
    
    content = f"""# CONSTITUTIONAL AMENDMENT PROPOSAL
**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Trigger:** Pattern Detected in '{keyword}' (Frequency: {len(evidence)})
**Status:** DRAFT

## 1. The Evidence (Pain)
The Historian detected the following repeated issues in `LEARNINGS.md`:
"""
    for item in evidence:
        content += f"- {item}\n"
        
    content += f"""
## 2. Proposed Invariant (The Cure)
**Draft Rule:** "I-NEW: The system MUST enforce strict handling of {keyword} to prevent recurrence."

*(Agent: Refine this rule to be specific, binary, and testable.)*

## 3. Ratification
- [ ] **MERGE** into `01_CONSTITUTION/LOGIC.md`
- [ ] **REJECT** (False Positive)
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def create_dummy_data():
    """Generates sample data to demonstrate the logic."""
    os.makedirs(os.path.dirname(LEARNINGS_FILE), exist_ok=True)
    with open(LEARNINGS_FILE, 'w', encoding='utf-8') as f:
        f.write("# Project Learnings\n\n")
        f.write("- 2024-01-01: API timeout caused data loss during sync.\n")
        f.write("- 2024-01-05: The timeout setting was too low for large files.\n")
        f.write("- 2024-01-10: Another timeout error occurred on the legacy server.\n")
        f.write("- 2024-01-12: UI glitch in the dashboard.\n")

def run_historian():
    print("[*] Historian waking up...")
    items = parse_learnings()
    print(f"[*] Scanned {len(items)} memory items.")
    
    clusters = analyze_patterns(items)
    
    if not clusters:
        print("[*] No patterns meeting the threshold detected.")
        return

    print(f"[!] Detected {len(clusters)} recurring failure patterns.")
    
    for keyword, evidence in clusters.items():
        print(f"    - Pattern: '{keyword}' (Count: {len(evidence)})")
        path = draft_amendment(keyword, evidence)
        print(f"    - Drafted Proposal: {path}")

if __name__ == "__main__":
    run_historian()
