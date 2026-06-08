#!/usr/bin/env python3
"""Ignition - Bootstrap script for initializing the Frontier Frame."""

import os
import re
import json
import logging
from datetime import datetime

# CONFIG
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
KERNEL_DIR = os.path.join(ROOT_DIR, "080_Kernel_and_Policy")
VECTORS_DIR = os.path.join(ROOT_DIR, "800_Test_Vectors", "vectors")

# FILES
KERNEL_FILE = os.path.join(KERNEL_DIR, "081_Kernel_Invariants.md")
AGENT_KERNEL_FILE = os.path.join(KERNEL_DIR, "087_Agent_Kernel_Invariants.md")
POLICY_FILE = os.path.join(KERNEL_DIR, "085_Policy_Baseline_v1.md")
GOV_VECTOR_FILE = os.path.join(VECTORS_DIR, "governance.json")

# LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("IGNITION")

def banner():
    print("""
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░  S K Y Z A I  IGNITION   ░░
    ░░        Cycle 001         ░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    """)

def ingest_kernel(file_path):
    """
    Parses 081_Kernel_Invariants.md to extract K-IDs.
    Returns a dict of {id: predicate_summary}.
    """
    if not os.path.exists(file_path):
        logger.error(f"Kernel file missing: {file_path}")
        return None

    invariants = {}
    with open(file_path, 'r') as f:
        content = f.read()
        # Find all "### K{id}: {Title}"
        matches = re.findall(r'### (K\d+): (.*)', content)
        for mid, title in matches:
            invariants[mid] = title.strip()
    
    logger.info(f"Loaded {len(invariants)} Kernel Invariants from 081.")
    return invariants

def ingest_policy(file_path):
    """
    Parses 085_Policy_Baseline_v1.md to extract Parameters.
    Scans the Summary Table (approximate).
    """
    if not os.path.exists(file_path):
        logger.error(f"Policy file missing: {file_path}")
        return None

    params = {}
    with open(file_path, 'r') as f:
        # Simple extraction: look for `VARIABLE_NAME` | value pattern in table
        for line in f:
            if "|" in line and "`" in line:
                # pipe table row
                parts = [p.strip() for p in line.split("|")]
                if len(parts) > 3:
                     # Attempt to find `VAR` in second or first column
                     var_match = re.search(r'`([A-Z_]+)`', line)
                     if var_match:
                         var_name = var_match.group(1)
                         # Value usually in next col
                         value_col = parts[2] if len(parts) > 2 else ""
                         params[var_name] = value_col
    
    logger.info(f"Loaded {len(params)} Policy Parameters from 085.")
    return params

def load_vector_suite(file_path):
    if not os.path.exists(file_path):
        logger.warning(f"Vector suite missing: {file_path}")
        return None
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            logger.info(f"Loaded Vector Suite: {os.path.basename(file_path)} ({len(data)} vectors)")
            return data
    except Exception as e:
        logger.error(f"Failed to load vector suite: {e}")
        return None

def validate_system(kernel, policy, vectors):
    """
    The Ignition Test.
    Does the Kernel exist? Is Policy complete? Do vectors load?
    """
    errors = []

    # 1. Kernel Completeness
    required_k = [f"K{i}" for i in range(1, 16)] # K1-K15
    for k in required_k:
        if k not in kernel:
            errors.append(f"Missing Kernel Invariant: {k}")

    # 2. Policy Check
    required_p = ["ZAI_TOTAL_SUPPLY", "CHECKPOINT_INTERVAL_SECONDS"]
    for p in required_p:
        if p not in policy:
            errors.append(f"Missing Policy Param: {p}")

    # 3. Vector Check
    if not vectors:
        errors.append("No Test Vectors loaded")

    return errors

def main():
    banner()
    logger.info("Initializing System Ignition...")

    # PHASE 1: INGESTION
    kernel = ingest_kernel(KERNEL_FILE)
    agent_kernel = ingest_kernel(AGENT_KERNEL_FILE)
    
    if kernel and agent_kernel:
        kernel.update(agent_kernel) # Merge K1-K9 with K10-K15
    
    policy = ingest_policy(POLICY_FILE)
    
    if not kernel or not policy:
        logger.critical("IGNITION ABORTED: SYSTEM DEFINITION MISSING")
        exit(1)

    # PHASE 2: VECTOR LOADING
    gov_vectors = load_vector_suite(GOV_VECTOR_FILE)

    # PHASE 3: VALIDATION
    errors = validate_system(kernel, policy, gov_vectors)

    if errors:
        logger.error("SYSTEM INTEGRITY CHECK FAILED:")
        for e in errors:
            logger.error(f"  [X] {e}")
        exit(1)
    
    logger.info("SYSTEM INTEGRITY VERIFIED [GREEN]")
    logger.info(f"Kernel Hash: {hash(str(kernel))}") # Mock hash
    logger.info(f"Policy Hash: {hash(str(policy))}")
    logger.info("Ready for Runtime.")

if __name__ == "__main__":
    main()
