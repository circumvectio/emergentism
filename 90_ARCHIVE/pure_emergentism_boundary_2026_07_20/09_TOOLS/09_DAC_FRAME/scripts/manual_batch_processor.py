#!/usr/bin/env python3
"""Manual Batch Processor - Processes batches of files manually."""

import os
import shutil
import json
import logging
from datetime import datetime

# CONFIG PATHS (Sorted V1.0)
ROOT_DIR = "/Users/Yves/Desktop/Skyzai_Frontier_Frame v.1.1 "
INTAKE_DIR = os.path.join(ROOT_DIR, "06 📂 INTAKE")
DROP_ZONE = os.path.join(INTAKE_DIR, "01 📁 Raw_Drop_Zone")
WASHING = os.path.join(INTAKE_DIR, "03 📁 Washing_Station")
STAGING = os.path.join(INTAKE_DIR, "04 📁 Staging_Area")
STAGING_MANIFESTS = os.path.join(STAGING, "📁 Ready_Manifests")

# Setup
if not os.path.exists(STAGING_MANIFESTS):
    os.makedirs(STAGING_MANIFESTS, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def process_batches():
    logger.info(f"Scanning {DROP_ZONE} for Batches...")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    
    for item in os.listdir(DROP_ZONE):
        if item.startswith("."): continue
        if item == "README.md": continue
        if item == "📁 Manual_Uploads": continue # Skip the upload folder itself if empty
        
        src_path = os.path.join(DROP_ZONE, item)
        
        # We process BOTH files and folders here manually
        item_type = "BATCH" if os.path.isdir(src_path) else "FILE"
        
        # 1. SENTRY: Move to Wash
        logger.info(f"[SENTRY] Accepted {item} ({item_type}) -> Washing Station")
        wash_path = os.path.join(WASHING, item)
        if os.path.exists(wash_path):
            logger.warning(f"  Collision in Wash: {item}. Skipping.")
            continue
            
        shutil.move(src_path, wash_path)
        
        # 2. SCRUBBER: Rename & Stage
        clean_name = item.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace("%20", "_")
        ingest_name = f"INGEST_{item_type}_{timestamp}_{clean_name}"
        
        stage_path = os.path.join(STAGING, ingest_name)
        logger.info(f"[SCRUBBER] Normalizing {item} -> {ingest_name}")
        shutil.move(wash_path, stage_path)
        
        # 3. MANIFEST
        manifest = {
            "original_name": item,
            "staged_name": ingest_name,
            "type": item_type,
            "ingest_time": timestamp,
            "status": "CLEAN",
            "source": "06_INTAKE/MANUAL_BATCH"
        }
        
        man_path = os.path.join(STAGING_MANIFESTS, f"{ingest_name}.json")
        with open(man_path, "w") as f:
            json.dump(manifest, f, indent=2)
            
        logger.info(f"[PLATED] Manifest created at {man_path}")

    logger.info("Batch Processing Complete.")

if __name__ == "__main__":
    process_batches()
