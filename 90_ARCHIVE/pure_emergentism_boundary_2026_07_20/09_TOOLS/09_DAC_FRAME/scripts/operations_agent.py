#!/usr/bin/env python3
"""Operations Agent - Handles day-to-day operational tasks and workflows."""

import os
import shutil
import logging
from datetime import datetime

# PATHS
ROOT_DIR = "/Users/Yves/Desktop/Skyzai_Frontier_Frame v.1.1 "
WORK_DIR = os.path.join(ROOT_DIR, "07 🏭 WORK")

# Inputs
RECEIVING_DOCK = os.path.join(WORK_DIR, "01 📦 INBOUND_LOGISTICS", "01 📁 Receiving_Dock")

# Processing
OPERATIONS = os.path.join(WORK_DIR, "02 ⚙️ OPERATIONS")
ACTIVE_STREAMS = os.path.join(OPERATIONS, "01 📁 Active_Streams")

# Outputs
OUTBOUND = os.path.join(WORK_DIR, "03 🚚 OUTBOUND_LOGISTICS")
SHIPPING_LANE = os.path.join(OUTBOUND, "01 📁 Shipping_Lane")

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("OPS")

def get_tree_structure(path):
    """Generates a simple text tree of the directory."""
    tree_str = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f == ".DS_Store": continue
            tree_str += f"{subindent}{f}\n"
    return tree_str

def run_operations():
    logger.info("Starting Operations Cycle (Digestion)...")
    
    # Ensure Anatomy
    if not os.path.exists(ACTIVE_STREAMS):
        os.makedirs(ACTIVE_STREAMS, exist_ok=True)
    if not os.path.exists(SHIPPING_LANE):
        os.makedirs(SHIPPING_LANE, exist_ok=True)
        
    if not os.path.exists(RECEIVING_DOCK):
        logger.warning("Receiving Dock missing.")
        return

    # Process Batches
    for item in os.listdir(RECEIVING_DOCK):
        if item.startswith("."): continue
        
        batch_path = os.path.join(RECEIVING_DOCK, item)
        if not os.path.isdir(batch_path): continue
        
        logger.info(f"[DIGESTING] {item}...")
        
        # 1. Analyze (Generate Tree)
        tree = get_tree_structure(batch_path)
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        
        report_content = f"""# DIGESTION REPORT: {item}
**Date**: {timestamp}
**Source**: Inbound Receiving Dock
**Status**: PROCESSED

## Content Analysis
The following structure was extracted from the batch:

```text
{tree}
```

## Action
- Transferred to Outbound Logistics.
"""
        # 2. Write Report
        report_name = f"DIGESTION_{timestamp}_{item}.md"
        report_path = os.path.join(ACTIVE_STREAMS, report_name)
        with open(report_path, "w") as f:
            f.write(report_content)
        logger.info(f"  Report generated: {report_name}")
        
        # 3. Excrete (Move to Shipping)
        dest_path = os.path.join(SHIPPING_LANE, item)
        if os.path.exists(dest_path):
            logger.warning(f"  Collision in Shipping Lane for {item}. Skipping move.")
            continue
            
        shutil.move(batch_path, dest_path)
        logger.info(f"  MOVED -> Shipping Lane")

    logger.info("Operations Cycle Complete.")

if __name__ == "__main__":
    run_operations()
