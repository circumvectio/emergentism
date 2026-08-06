#!/usr/bin/env bash
# _run_standing_gate_figure.sh — runs every check_*.py in 09_TOOLS/01_SCRIPTS/
# with a 60s wall-clock timeout, captures pass/fail/hang/error and wall-clock time.
# Output: NDJSON on stdout (one record per line).
# Usage: bash 00_HANDOFF/_run_standing_gate_figure.sh > /tmp/gates.ndjson 2>/dev/null
set -u

CORPUS_ROOT="/Users/Yves/Documents/01_EMERGENTISM"
SCRIPTS_DIR="$CORPUS_ROOT/09_TOOLS/01_SCRIPTS"
TIMEOUT_SECS=60

cd "$CORPUS_ROOT" || exit 2

# Stable ordering — same as gate.sh invocation order where possible
GATES=(
  "09_TOOLS/01_SCRIPTS/check_foundation.py"
  "09_TOOLS/01_SCRIPTS/check_claim_status.py"
  "09_TOOLS/01_SCRIPTS/check_coherence_profile.py"
  "09_TOOLS/01_SCRIPTS/check_contact_limited.py"
  "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
  "09_TOOLS/01_SCRIPTS/check_generative_base.py"
  "09_TOOLS/01_SCRIPTS/check_established.py"
  "09_TOOLS/01_SCRIPTS/check_receipt_citations.py"
  "09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py"
  "09_TOOLS/01_SCRIPTS/check_work_in_progress.py"
  "09_TOOLS/01_SCRIPTS/check_adjudication_custody.py"
  "09_TOOLS/01_SCRIPTS/check_record_counters.py"
  "09_TOOLS/01_SCRIPTS/check_review_bundle.py"
  "09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py"
  "09_TOOLS/01_SCRIPTS/check_q4_declarations.py"
  "09_TOOLS/01_SCRIPTS/check_barred_claims.py"
  "09_TOOLS/01_SCRIPTS/check_node_product_ranking.py"
  "09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py"
  "09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py"
  "09_TOOLS/01_SCRIPTS/check_links.py"
  "09_TOOLS/01_SCRIPTS/check_contradiction_census.py"
  "09_TOOLS/01_SCRIPTS/check_dead_citations.py"
  "09_TOOLS/01_SCRIPTS/check_forwarding_stubs.py"
  "09_TOOLS/01_SCRIPTS/check_g2_normal_form.py"
  "09_TOOLS/01_SCRIPTS/check_tree_contract.py"
  "09_TOOLS/01_SCRIPTS/check_no_secrets_staged.py"
)

for gate in "${GATES[@]}"; do
  start=$(python3 -c 'import time; print(f"{time.time():.3f}")')
  # Use python timeout — macOS has no gtimeout, and subprocess.run is portable
  out=$(python3 -c "
import subprocess, sys, time
try:
    r = subprocess.run(['python3', '$gate'],
                       capture_output=True, text=True,
                       timeout=$TIMEOUT_SECS, cwd='$CORPUS_ROOT')
    print(r.returncode)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
except subprocess.TimeoutExpired as e:
    print('TIMEOUT')
    sys.stdout.write(e.stdout.decode() if e.stdout else '')
    sys.stderr.write(e.stderr.decode() if e.stderr else '')
" 2>&1)
  end=$(python3 -c 'import time; print(f"{time.time():.3f}")')
  rc=$(echo "$out" | head -1)
  first_line=$(echo "$out" | sed -n '2p' | head -c 200)
  # Compute wall-clock
  wall=$(python3 -c "print(f'{$end - $start:.3f}")")
  # Emit NDJSON
  python3 -c "
import json
rec = {
  'gate': '$gate',
  'rc_marker': '''$rc''',
  'wall_secs': float('$wall'),
  'first_line': '''$first_line'''[:200].replace(chr(10), ' '),
}
print(json.dumps(rec))
"
done
