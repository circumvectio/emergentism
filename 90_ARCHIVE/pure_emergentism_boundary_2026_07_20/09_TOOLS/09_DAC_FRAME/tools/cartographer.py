#!/usr/bin/env python3
"""Cartographer - Generates ATLAS.json from directory structure."""

import os
import json
import re
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ATLAS_PATH = os.path.join(PROJECT_ROOT, "00_FRAME", "ATLAS.json")
SCHEMA_VERSION = "2.0.0"

def parse_intent(path):
    # Order: INTENT.md -> README.md (Purpose section)
    intent_file = os.path.join(path, "INTENT.md")
    if os.path.exists(intent_file):
        with open(intent_file, "r") as f:
            content = f.read().strip()
            lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")]
            return lines[0] if lines else None
    
    readme_file = os.path.join(path, "README.md")
    if os.path.exists(readme_file):
        with open(readme_file, "r") as f:
            content = f.read()
            # Look for Purpose under Teleology or # Purpose
            match = re.search(r"\*\*Purpose\*\*:\s*(.*)", content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            # Fallback to first line after header 1
            lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")]
            if lines:
                return lines[0]
                
    return None

def parse_contract(path):
    contract_file = os.path.join(path, "CONTRACT.md")
    invariants = []
    if os.path.exists(contract_file):
        with open(contract_file, "r") as f:
            content = f.read()
            invariants = re.findall(r"I-\d+", content)
    return list(set(invariants))

def get_node_id(rel_path):
    mapping = {
        "00_FRAME": "DR-0",
        "01_CONSTITUTION": "DR-1",
        "02_BLUEPRINT": "DR-2",
        "03_CODE": "DR-3",
        "04_REALITY": "DR-4",
        "05_WORLD": "DR-5",
        "06_ORACLES": "DR-6",
        "07_WORK": "DR-7",
        "08_INTAKE": "DR-8",
        "TEMPLATES": "DR-9"
    }
    base = rel_path.split(os.sep)[0]
    return mapping.get(base, "DR-X")

def run_cartographer():
    atlas = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": SCHEMA_VERSION,
            "node_count": 0
        },
        "nodes": {}
    }

    core_folders = ["00_FRAME", "01_CONSTITUTION", "02_BLUEPRINT", "03_CODE", "04_REALITY", "05_WORLD", "06_ORACLES", "07_WORK", "TEMPLATES"]

    for folder in core_folders:
        path = os.path.join(PROJECT_ROOT, folder)
        if os.path.exists(path):
            rel_path = folder
            intent = parse_intent(path) or "Core DAC Component."
            node_id = get_node_id(rel_path)
            
            atlas["nodes"][node_id] = {
                "node_id": node_id,
                "path": rel_path,
                "intent": intent,
                "type": "KERNEL" if node_id.startswith("DR-0") else "SHARD",
                "status": "ACTIVE",
                "invariants": parse_contract(path)
            }
            atlas["metadata"]["node_count"] += 1

    # Also scan for sub-folders with README/INTENT
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if ".git" in root or "99_ARCHIVE" in root:
            continue
        
        rel_path = os.path.relpath(root, PROJECT_ROOT)
        if rel_path == "." or rel_path.split(os.sep)[0] in core_folders:
            # We already handled the root of core folders. Now look deeper.
            if rel_path.count(os.sep) == 0: continue
            
        intent = parse_intent(root)
        if intent:
            node_id = get_node_id(rel_path)
            # Append depth
            depth_suffix = ".".join([str(len(d)) for d in rel_path.split(os.sep)[1:]])
            full_node_id = f"{node_id}.{depth_suffix}" if depth_suffix else node_id

            if full_node_id not in atlas["nodes"]:
                atlas["nodes"][full_node_id] = {
                    "node_id": full_node_id,
                    "path": rel_path,
                    "intent": intent,
                    "type": "DOC",
                    "status": "ACTIVE",
                    "invariants": parse_contract(root)
                }
                atlas["metadata"]["node_count"] += 1

    with open(ATLAS_PATH, "w") as f:
        json.dump(atlas, f, indent=2)
    
    print(f"Success: {ATLAS_PATH} generated with {atlas['metadata']['node_count']} nodes.")

if __name__ == "__main__":
    run_cartographer()
