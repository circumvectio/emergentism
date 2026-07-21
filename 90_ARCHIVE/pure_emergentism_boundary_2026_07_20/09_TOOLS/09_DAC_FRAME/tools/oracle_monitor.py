#!/usr/bin/env python3
"""Oracle Monitor - Monitors external data sources and validates oracle integrity."""

import json
import os
import datetime

# --- CONFIGURATION ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORACLES_DIR = os.path.join(PROJECT_ROOT, "04_REALITY", "ORACLES")
ALPHA = 0.2  # Learning rate (Impact of new evidence)
THRESHOLD_PROBATION = 0.7  # Score below this triggers probation

def load_oracle(filepath):
    """Loads an oracle definition file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_oracle(filepath, data):
    """Saves the updated oracle definition."""
    data['last_updated'] = datetime.datetime.now().isoformat()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def log_outcome(oracle_id, outcome, context="Routine Check"):
    """
    Updates the confidence score based on a new interaction.
    outcome: 1.0 (Success), 0.5 (Partial/Ambiguous), 0.0 (Failure/Hallucination)
    """
    filename = f"{oracle_id}.json"
    filepath = os.path.join(ORACLES_DIR, filename)
    
    # Create directory if needed
    os.makedirs(ORACLES_DIR, exist_ok=True)
    
    data = load_oracle(filepath)
    
    # If new oracle, initialize
    if not data:
        data = {
            "oracle_id": oracle_id,
            "name": context if context != "Routine Check" else oracle_id,
            "static_grade": "C", # Default conservative start
            "current_confidence": 0.5, # Neutral start
            "status": "ACTIVE",
            "history": []
        }
        print(f"[*] Initialized new tracking for {oracle_id}")

    # --- THE EPISTEMIC EQUATION ---
    # V_new = V_old * (1 - alpha) + Outcome * alpha
    old_confidence = data.get('current_confidence', 0.5)
    new_confidence = (old_confidence * (1 - ALPHA)) + (outcome * ALPHA)
    
    # Round for cleanliness
    new_confidence = round(new_confidence, 4)
    data['current_confidence'] = new_confidence
    
    # Add to history
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "outcome": outcome,
        "context": context
    }
    data['history'].append(entry)
    # Keep history manageable (last 50)
    data['history'] = data['history'][-50:]

    # --- STATUS CHECK ---
    if new_confidence < THRESHOLD_PROBATION:
        if data['status'] != "PROBATION":
            print(f"[!] ALERT: {oracle_id} degraded to PROBATION (Score: {new_confidence})")
        data['status'] = "PROBATION"
    else:
        if data['status'] == "PROBATION":
            print(f"[+] RECOVERY: {oracle_id} restored to ACTIVE (Score: {new_confidence})")
        data['status'] = "ACTIVE"

    save_oracle(filepath, data)
    print(f"[*] Updated {oracle_id}: {old_confidence} -> {new_confidence}")

if __name__ == "__main__":
    # Test Run: Simulate a Google Search failure and a successful GPT-4 call
    print("--- Simulating Interaction ---")
    log_outcome("ORACLE-GOOGLE", 0.0, "Search returned 404 links")
    log_outcome("ORACLE-GPT4", 1.0, "Code compilation successful")
