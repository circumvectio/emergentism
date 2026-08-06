#!/usr/bin/env python3
"""
_run_standing_gate_figure.py — runs every check_*.py in 09_TOOLS/01_SCRIPTS/
with a 60s wall-clock timeout, captures pass/fail/hang/error and wall-clock time.
Output: NDJSON on stdout (one record per line).
"""
import json
import subprocess
import sys
import time
from pathlib import Path

CORPUS_ROOT = Path("/Users/Yves/Documents/01_EMERGENTISM")
SCRIPTS_DIR = CORPUS_ROOT / "09_TOOLS" / "01_SCRIPTS"
TIMEOUT_SECS = 60

# Stable order — same as gate.sh invocation order where possible
GATES = [
    "09_TOOLS/01_SCRIPTS/check_foundation.py",
    "09_TOOLS/01_SCRIPTS/check_claim_status.py",
    "09_TOOLS/01_SCRIPTS/check_coherence_profile.py",
    "09_TOOLS/01_SCRIPTS/check_contact_limited.py",
    "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py",
    "09_TOOLS/01_SCRIPTS/check_generative_base.py",
    "09_TOOLS/01_SCRIPTS/check_established.py",
    "09_TOOLS/01_SCRIPTS/check_receipt_citations.py",
    "09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py",
    "09_TOOLS/01_SCRIPTS/check_work_in_progress.py",
    "09_TOOLS/01_SCRIPTS/check_adjudication_custody.py",
    "09_TOOLS/01_SCRIPTS/check_record_counters.py",
    "09_TOOLS/01_SCRIPTS/check_review_bundle.py",
    "09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py",
    "09_TOOLS/01_SCRIPTS/check_q4_declarations.py",
    "09_TOOLS/01_SCRIPTS/check_barred_claims.py",
    "09_TOOLS/01_SCRIPTS/check_node_product_ranking.py",
    "09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py",
    "09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py",
    "09_TOOLS/01_SCRIPTS/check_links.py",
    "09_TOOLS/01_SCRIPTS/check_contradiction_census.py",
    "09_TOOLS/01_SCRIPTS/check_dead_citations.py",
    "09_TOOLS/01_SCRIPTS/check_forwarding_stubs.py",
    "09_TOOLS/01_SCRIPTS/check_g2_normal_form.py",
    "09_TOOLS/01_SCRIPTS/check_tree_contract.py",
    "09_TOOLS/01_SCRIPTS/check_no_secrets_staged.py",
]


def classify(rc_marker: str, had_timeout: bool) -> str:
    if had_timeout:
        return "hang"
    if rc_marker == "0":
        return "pass"
    if rc_marker == "1":
        return "fail"
    if rc_marker == "2":
        return "error"
    return f"other_{rc_marker}"


def first_line(s: str) -> str:
    for line in s.splitlines():
        line = line.strip()
        if line:
            return line[:200]
    return ""


def main() -> int:
    out = sys.stdout
    for gate in GATES:
        start = time.time()
        had_timeout = False
        rc_marker = "-1"
        stdout_text = ""
        stderr_text = ""
        try:
            r = subprocess.run(
                ["python3", gate],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECS,
                cwd=str(CORPUS_ROOT),
            )
            rc_marker = str(r.returncode)
            stdout_text = r.stdout or ""
            stderr_text = r.stderr or ""
        except subprocess.TimeoutExpired as e:
            had_timeout = True
            rc_marker = "TIMEOUT"
            stdout_text = (e.stdout.decode() if e.stdout else "") or ""
            stderr_text = (e.stderr.decode() if e.stderr else "") or ""
        end = time.time()
        wall = end - start
        classification = classify(rc_marker, had_timeout)
        rec = {
            "gate": gate,
            "rc_marker": rc_marker,
            "classification": classification,
            "wall_secs": round(wall, 3),
            "first_stdout": first_line(stdout_text),
            "first_stderr": first_line(stderr_text),
        }
        out.write(json.dumps(rec) + "\n")
        out.flush()
        # Human-readable on stderr for live progress
        print(
            f"  [{classification:5s}] rc={rc_marker:>3s} {wall:6.2f}s  {gate}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
