#!/usr/bin/env python3
"""Inbound Agent - Processes incoming files and data for ingestion."""

import os
import shutil
import json
import logging
from datetime import datetime

# PATHS (Sorted V1.0)
ROOT_DIR = "/Users/Yves/Desktop/Skyzai_Frontier_Frame v.1.1 "
# Source
STAGING = os.path.join(ROOT_DIR, "06 📂 INTAKE", "04 📁 Staging_Area")
MANIFESTS_SRC = os.path.join(STAGING, "📁 Ready_Manifests")
# Destiny
INBOUND_LOGISTICS = os.path.join(ROOT_DIR, "07 🏭 WORK", "01 📦 INBOUND_LOGISTICS")
RECEIVING_DOCK = os.path.join(INBOUND_LOGISTICS, "01 📁 Receiving_Dock")
INVENTORY_LEDGER = os.path.join(INBOUND_LOGISTICS, "02 📁 Inventory_Ledger")

# Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("INBOUND")

def run_inbound_logistics():
    logger.info("Starting Inbound Logistics Cycle...")
    
    # Ensure Destiny Exists
    if not os.path.exists(RECEIVING_DOCK):
        os.makedirs(RECEIVING_DOCK, exist_ok=True)
    if not os.path.exists(INVENTORY_LEDGER):
        os.makedirs(INVENTORY_LEDGER, exist_ok=True)

    # Scan Staging for Folders
    if not os.path.exists(STAGING):
        logger.error("Staging Area missing.")
        return

    processed_count = 0
    
    for item_name in os.listdir(STAGING):
        item_path = os.path.join(STAGING, item_name)
        
        # We only ingest Directories that look like Batches
        if not os.path.isdir(item_path): continue
        if not item_name.startswith("INGEST_"): continue
        if item_name == "📁 Ready_Manifests": continue

        logger.info(f"[DETECTED] Batch: {item_name}")
        
        # 1. Verify Manifest
        manifest_name = f"{item_name}.json"
        manifest_src_path = os.path.join(MANIFESTS_SRC, manifest_name)
        
        if not os.path.exists(manifest_src_path):
            logger.warning(f"  MISSING MANIFEST for {item_name}. Skipping.")
            continue
            
        # 2. Ingest Content (Physical Move)
        dest_path = os.path.join(RECEIVING_DOCK, item_name)
        if os.path.exists(dest_path):
            logger.warning(f"  COLLISION in Receiving Dock. Skipping {item_name}.")
            continue
            
        shutil.move(item_path, dest_path)
        logger.info(f"  MOVED -> Receiving Dock")
        
        # 3. Update & Move Manifest (Ledgering)
        with open(manifest_src_path, 'r') as f:
            data = json.load(f)
            
        data['status'] = 'INGESTED'
        data['ingest_time_body'] = datetime.now().strftime("%Y%m%d%H%M")
        data['location'] = "07/INBOUND/Receiving"
        
        manifest_dest_path = os.path.join(INVENTORY_LEDGER, manifest_name)
        with open(manifest_dest_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        # Remove old manifest
        os.remove(manifest_src_path)
        logger.info(f"  LEDGERED -> Inventory")
        
        processed_count += 1

    logger.info(f"Cycle Complete. Ingested {processed_count} batches.")

if __name__ == "__main__":
    run_inbound_logistics()
