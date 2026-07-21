#!/usr/bin/env python3
"""Membrane Agent - Manages boundaries and access control between zones."""

import os
import time
import shutil
import json
import logging
import sys
from datetime import datetime

# --- CONFIGURATION (ADAPTED FOR V1.1 SORTED STRUCTURE) ---
# Dynamic Root detection
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Physical Paths (Emoji System)
INTAKE_DIR = os.path.join(ROOT_DIR, "06 📂 INTAKE")
REALITY_DIR = os.path.join(ROOT_DIR, "04 🌍 REALITY")

# Anatomy Definitions
DROP_ZONE = os.path.join(INTAKE_DIR, "01 📁 Raw_Drop_Zone")
QUARANTINE = os.path.join(INTAKE_DIR, "02 📁 Quarantine_Lab")
WASHING = os.path.join(INTAKE_DIR, "03 📁 Washing_Station")
STAGING = os.path.join(INTAKE_DIR, "04 📁 Staging_Area")

# Input Vectors (Physical with Emojis, Logical aliases)
VECTOR_MANUAL = os.path.join(DROP_ZONE, "📁 Manual_Uploads") 
VECTOR_CHAT = os.path.join(DROP_ZONE, "📁 Chat_Stream")       
VECTOR_INDUSTRY = os.path.join(DROP_ZONE, "📁 Industry_Signals") 

# Sub-chambers
INCINERATOR = os.path.join(QUARANTINE, "📁 Incinerator")
ISOLATION = os.path.join(QUARANTINE, "📁 Isolation_Chamber")
STAGING_MANIFESTS = os.path.join(STAGING, "📁 Ready_Manifests")
AUDIT_LOG_DIR = os.path.join(REALITY_DIR, "📁 Audit_Logs")
AUDIT_LOG = os.path.join(AUDIT_LOG_DIR, "INTAKE_MEMBRANE.log")

# Forbidden Patterns
FORBIDDEN_EXTENSIONS = ['.exe', '.bat', '.sh', '.bin']
MALICIOUS_KEYWORDS = ['virus', 'malware', 'trojan', 'hack']

# Logging Setup
if not os.path.exists(AUDIT_LOG_DIR):
    os.makedirs(AUDIT_LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=AUDIT_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
logger = logging.getLogger('MEMBRANE_V2')

class SentryAgent:
    """The Nose: Detects threats in all Drop Zone vectors."""
    
    def scan(self):
        # Scan all input vectors
        targets = [DROP_ZONE, VECTOR_MANUAL, VECTOR_CHAT, VECTOR_INDUSTRY]
        
        for target_dir in targets:
            if not os.path.exists(target_dir):
                # Auto-create vectors if missing
                os.makedirs(target_dir, exist_ok=True)
                continue
            
            for filename in os.listdir(target_dir):
                if filename.startswith('.'): continue
                if filename == "README.md": continue
                if os.path.isdir(os.path.join(target_dir, filename)): continue
                
                filepath = os.path.join(target_dir, filename)
                if os.path.isfile(filepath):
                    self.process_file(filepath, filename, target_dir)

    def process_file(self, filepath, filename, source_dir):
        source_name = os.path.basename(source_dir)
        # Clean source name of emojis for logging/logic if needed, but keeping simple
        
        logger.info(f"[SENTRY] Detected object in {source_name}: {filename}")
        
        # 1. Biological Check
        ext = os.path.splitext(filename)[1].lower()
        is_toxic = any(k in filename.lower() for k in MALICIOUS_KEYWORDS)
        is_weapon = ext in FORBIDDEN_EXTENSIONS
        
        if is_toxic or is_weapon:
            self.incinerate(filepath, filename, "Toxic Signature Detected")
            return

        # 2. Vector-Specific Logic
        if source_dir == VECTOR_CHAT and ext != '.json':
             self.isolate(filepath, filename, "Chat Logs must be JSON")
             return
        
        # 3. Pass to Wash
        self.pass_to_wash(filepath, filename, source_name)

    def incinerate(self, filepath, filename, reason):
        dest = os.path.join(INCINERATOR, f"{int(time.time())}_{filename}")
        shutil.move(filepath, dest)
        logger.warning(f"[SENTRY] INCINERATED {filename}: {reason}")

    def isolate(self, filepath, filename, reason):
        dest = os.path.join(ISOLATION, f"{int(time.time())}_{filename}")
        shutil.move(filepath, dest)
        logger.warning(f"[SENTRY] ISOLATED {filename}: {reason}")

    def pass_to_wash(self, filepath, filename, origin):
        # We prepend the origin to the filename so the Scrubber knows context
        # Sanitize origin name (remove emojis for filename safety if desired, but simple append works)
        safe_origin = origin.replace("📁 ", "").replace(" ", "_")
        new_name = f"{safe_origin}___{filename}"
        dest = os.path.join(WASHING, new_name)
        shutil.move(filepath, dest)
        logger.info(f"[SENTRY] PASSED {filename} to Washing Station.")


class ScrubberAgent:
    """The Liver: Sanitizes, Aligns to Niche Ontology, and Plates."""
    
    def scrub(self):
        if not os.path.exists(WASHING): return 

        for filename in os.listdir(WASHING):
            if filename.startswith('.'): continue
            
            filepath = os.path.join(WASHING, filename)
            if os.path.isfile(filepath):
                self.normalize_and_stage(filepath, filename)

    def normalize_and_stage(self, filepath, filename):
        logger.info(f"[SCRUBBER] Scrubbing {filename}...")
        
        # Parse Origin (added by Sentry)
        parts = filename.split("___")
        origin = parts[0] if len(parts) > 1 else "UNKNOWN"
        real_filename = parts[-1]
        
        # 1. Normalize Name
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        clean_name = real_filename.replace(" ", "_").replace("-", "_")
        
        # Prefix depends on vector
        if "Chat_Stream" in origin:
            prefix = "MEMORY"
        elif "Industry_Signals" in origin:
            prefix = "INTEL"
        else:
            prefix = "INGEST"
            
        final_name = f"{prefix}_{timestamp}_{clean_name}"
        
        # 2. Ontology Alignment (Simulated)
        # In a real system, this would call the Niche Shared Intelligence to map terms.
        ontology_tag = "NICHE_STANDARD_V1"
        
        # 3. Generate Manifest
        manifest = {
            "original_name": real_filename,
            "staged_name": final_name,
            "origin_vector": origin,
            "ingest_time": timestamp,
            "status": "KOSHER",
            "ontology_version": ontology_tag,
            "size_bytes": os.path.getsize(filepath)
        }
        
        # 4. Move to Staging
        dest = os.path.join(STAGING, final_name)
        shutil.move(filepath, dest)
        
        # 5. Write Manifest
        manifest_path = os.path.join(STAGING_MANIFESTS, f"{final_name}.json")
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
            
        logger.info(f"[SCRUBBER] PLATED {final_name} in Staging. (Vector: {origin})")

def run_pulse():
    """Runs a single pass of the immune system (For Automation)."""
    logger.info("Membrane Pulse Initiated...")
    
    # Ensure Anatomy Exists
    dirs_to_create = [
        DROP_ZONE, VECTOR_MANUAL, VECTOR_CHAT, VECTOR_INDUSTRY,
        QUARANTINE, INCINERATOR, ISOLATION,
        WASHING, STAGING, STAGING_MANIFESTS,
        AUDIT_LOG_DIR
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)
    
    sentry = SentryAgent()
    scrubber = ScrubberAgent()
    
    sentry.scan()
    scrubber.scrub()
    logger.info("Membrane Pulse Complete.")

def run_membrane_loop():
    logger.info("Initializing Immune System (Chat & Niche Enabled)...")
    logger.info(f"Target Root: {ROOT_DIR}")

    # Ensure Anatomy on Boot
    run_pulse() 
    
    logger.info("Membrane Active. Listening for Files, Chat Logs, and Industry Signals...")
    try:
        while True:
            run_pulse() # Re-using pulse logic for loop to keep DRY
            time.sleep(5)
    except KeyboardInterrupt:
        logger.info("Membrane Shutting Down.")

if __name__ == "__main__":
    if "--pulse" in sys.argv:
        run_pulse()
    else:
        run_membrane_loop()
