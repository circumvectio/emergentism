#!/usr/bin/env python3
"""Metabolic Cycle - Orchestrates the continuous operational rhythm of the DAC."""

import os
import sys
import time
import subprocess
import logging
from datetime import datetime

# CONFIG PATHS
ROOT_DIR = "/Users/Yves/Desktop/Skyzai_Frontier_Frame v.1.1 "
SCRIPTS_DIR = os.path.join(ROOT_DIR, "03 💻 CODE", "Scripts")

# LOGGING
LOG_DIR = os.path.join(ROOT_DIR, "07 🏭 WORK", "02 ⚙️ OPERATIONS", "03 📁 SLA_Monitoring")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    
CYCLE_LOG = os.path.join(LOG_DIR, "CYCLE_LOG.txt")

logging.basicConfig(
    filename=CYCLE_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
logger = logging.getLogger("HEARTBEAT")

def run_script(script_name, args=[]):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        logger.error(f"Script missing: {script_name}")
        return False
        
    logger.info(f"--- Triggering {script_name} ---")
    try:
        cmd = [sys.executable, script_path] + args
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        # Log output indent
        for line in result.stdout.splitlines():
            logger.info(f"  [{script_name}] {line}")
        if result.stderr:
             for line in result.stderr.splitlines():
                 logger.warning(f"  [{script_name} STDERR] {line}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run {script_name}: {e}")
        logger.error(e.stderr)
        return False

def run_metabolic_cycle():
    start_time = datetime.now()
    logger.info(f"=== METABOLIC CYCLE STARTED: {start_time} ===")
    
    # 1. MEMBRANE (Pulse)
    # Detects New Files -> Moves to Staging
    logger.info("PHASE 1: MEMBRANE (Immune Defense)")
    success = run_script("membrane_agent.py", args=["--pulse"])
    if not success: logger.error("Membrane Phase Failed.")

    # 2. INBOUND (Ingest)
    # Consumes Staging -> Moves to Receiving Dock
    logger.info("PHASE 2: INBOUND (Ingestion)")
    success = run_script("inbound_agent.py")
    if not success: logger.error("Inbound Phase Failed.")

    # 3. OPERATIONS (Digest)
    # Receving Dock -> Outbound Shipping
    logger.info("PHASE 3: OPERATIONS (Digestion)")
    success = run_script("operations_agent.py")
    if not success: logger.error("Operations Phase Failed.")
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"=== CYCLE COMPLETE: {duration} ===")
    print(f"\nCycle Logged to: {CYCLE_LOG}")

if __name__ == "__main__":
    run_metabolic_cycle()
