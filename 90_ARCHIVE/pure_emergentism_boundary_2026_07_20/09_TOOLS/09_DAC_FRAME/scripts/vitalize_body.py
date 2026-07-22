#!/usr/bin/env python3
"""Vitalize Body - Initializes and maintains the directory structure."""

import os
import shutil
import logging

# PATHS
ROOT_DIR = "/Users/Yves/Desktop/Skyzai_Frontier_Frame v.1.1 "
WORK_DIR = os.path.join(ROOT_DIR, "07 🏭 WORK")
ARCHIVE_DIR = os.path.join(ROOT_DIR, "99 🗑️ ARCHIVE", "Legacy_Work_Sort")

# MAPPINGS (Legacy -> Vitalized)
ORGANS = [
    (["01_LOGISTICS_IN"], "01 📦 INBOUND_LOGISTICS"),
    (["02_OPERATIONS"], "02 ⚙️ OPERATIONS"),
    (["03_LOGISTICS_OUT"], "03 🚚 OUTBOUND_LOGISTICS"),
    (["04_GROWTH", "GROWTH"], "04 📈 GROWTH"),
    (["05_SERVICE"], "05 🤝 SERVICE"),
    (["06_TREASURY"], "06 🏦 TREASURY"),
    (["07_PEOPLE", "HR", "SUPPORT_PEOPLE"], "07 👥 PEOPLE"),
    (["08_TECH", "SUPPORT_TECH", "SUPPORT_INFRA"], "08 🔬 TECH"),
    (["09_PROCUREMENT", "SUPPORT_BUY"], "09 🛒 PROCUREMENT")
]

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def vitalize_body():
    logger.info("Vitalizing The Body (07 WORK)...")
    
    if not os.path.exists(WORK_DIR):
        logger.error(f"Work Dir missing: {WORK_DIR}")
        return

    # 1. Create Archive for Clutter
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # 2. Process Organs
    for sources, target_name in ORGANS:
        target_path = os.path.join(WORK_DIR, target_name)
        
        # Ensure Target
        if not os.path.exists(target_path):
            created = False
            # Try Rename first source if exists
            first_src = os.path.join(WORK_DIR, sources[0])
            if os.path.exists(first_src):
                try:
                    os.rename(first_src, target_path)
                    logger.info(f"Renamed {sources[0]} -> {target_name}")
                    created = True
                except Exception as e:
                    logger.error(f"Rename failed: {e}")
            
            if not created:
                os.makedirs(target_path, exist_ok=True)
                logger.info(f"Created {target_name}")
        
        # Merge remaining sources
        for src in sources:
            src_path = os.path.join(WORK_DIR, src)
            if os.path.exists(src_path) and src_path != target_path:
                logger.info(f"Merging {src} -> {target_name}...")
                for item in os.listdir(src_path):
                    if item.startswith("."): continue
                    shutil.move(os.path.join(src_path, item), os.path.join(target_path, item))
                try: shutil.rmtree(src_path)
                except: pass

    # 3. Create Receving Dock specifically
    dock = os.path.join(WORK_DIR, "01 📦 INBOUND_LOGISTICS", "01 📁 Receiving_Dock")
    inventory = os.path.join(WORK_DIR, "01 📦 INBOUND_LOGISTICS", "02 📁 Inventory_Ledger")
    os.makedirs(dock, exist_ok=True)
    os.makedirs(inventory, exist_ok=True)
    logger.info("Created Inbound Logistics Sub-structure.")

    # 4. Sweep Rest to Archive
    VALID = [o[1] for o in ORGANS] + [".DS_Store", "README.md", "BACKLOG.md", "ROADMAP.md", "DIFF_LOG.md", "LEARNINGS.md"]
    
    for item in os.listdir(WORK_DIR):
        if item in VALID: continue
        
        logger.info(f"Archiving Clutter: {item}")
        try:
            shutil.move(os.path.join(WORK_DIR, item), os.path.join(ARCHIVE_DIR, item))
        except: pass

    logger.info("Body Vitalization Complete.")

if __name__ == "__main__":
    vitalize_body()
