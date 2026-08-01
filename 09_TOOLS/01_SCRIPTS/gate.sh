#!/usr/bin/env bash
# gate.sh — THE GATE. Runs every corpus checker and fails loudly.
#
# WHY THIS EXISTS. r177 (`177_WP1_DEFECTIVE_VALIDATOR_HARDENED_2026_07_29.md`)
# recorded HOLE 0: "nothing invokes them, there is no gate."
# The corpus had five validators and NOTHING RAN THEM. On 2026-07-29 the corpus map
# confirmed it mechanically — no CI, and a pre-commit hook that was 61 lines of
# .DS_Store cleanup running no checker. A tier could drift between commits and no
# gate fired. That absence, not any single defect, is what lets an [A] column grow
# unchecked.
#
# USAGE
#   bash 09_TOOLS/01_SCRIPTS/gate.sh          run everything, fail on any failure
#   EMERGENTISM_SKIP_LEAN=1 bash ...gate.sh   acknowledge an absent Lean toolchain
#
# INSTALL AS A PRE-COMMIT HOOK
#   bash 09_TOOLS/01_SCRIPTS/gate.sh --install-hook
#
# THE HONEST LIMIT, STATED HERE BECAUSE IT MATTERS. `git commit --no-verify`
# bypasses any pre-commit hook, and this repository's own maintainers use it
# routinely (the legacy hook sweeps unrelated files via `git add -u`, so bypassing
# is the safe habit with a concurrent committer). A HOOK IS THEREFORE NOT A GATE.
# CI is — see .github/workflows/gate.yml, which cannot be skipped from a laptop.

set -uo pipefail
cd "$(dirname "$0")/../.." || exit 2
ROOT="$(pwd)"

if [[ "${1:-}" == "--install-hook" ]]; then
  HOOK="$ROOT/.git/hooks/pre-commit"
  if [[ -f "$HOOK" ]] && ! grep -q "gate.sh" "$HOOK"; then
    cp "$HOOK" "$HOOK.pre-gate.bak"
    # chain: keep the existing cleanup hook, append the gate
    printf '\n# --- appended 2026-07-29: the gate (r183, `183_THE_MANIFEST_AUDITED_ITSELF_AND_FAILED_2026_07_29.md`) ---\nbash "%s" || exit 1\n' \
      "$ROOT/09_TOOLS/01_SCRIPTS/gate.sh" >> "$HOOK"
    echo "gate chained onto the existing pre-commit hook (backup: $HOOK.pre-gate.bak)"
  else
    echo "hook already chains the gate, or no hook present"
  fi
  exit 0
fi

CHECKS=(
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
  # Wired in 2026-07-31. All four existed on disk and were invoked by NOTHING, so the
  # properties they test were unguarded. check_q4_declarations.py is new and exists because
  # build_pwa.py silently reverted a signed ruling while this gate reported PASS.
  # check_trophic_rosetta_doctrine.py was failing on a real defect the moment it was run:
  # a bare ambiguous eta in the constitution, now written in its action register.
  # check_links.py WAS deliberately unwired because it could not fail: it walked a
  # directory that does not exist in this repo, swallowed every exception, and printed
  # "Link check complete." on the way to exit 0. Rewritten 2026-08-01 to actually resolve
  # every local Markdown link, and wired in now that it has a failure path (verified by
  # breaking a link and watching it fail). DELIBERATELY STILL NOT WIRED:
  # check_no_secrets_staged.py inspects the STAGED diff, which a tree gate cannot see; it
  # belongs in .git/hooks/pre-commit, where it is.
  "09_TOOLS/01_SCRIPTS/check_q4_declarations.py"
  "09_TOOLS/01_SCRIPTS/check_barred_claims.py"
  "09_TOOLS/01_SCRIPTS/check_node_product_ranking.py"
  "09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py"
  "09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py"
  "09_TOOLS/01_SCRIPTS/check_links.py"
  "09_TOOLS/01_SCRIPTS/build_receipt_disambiguation.py"
  "09_TOOLS/01_SCRIPTS/test_build_magnum_opus_register.py"
  "03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/R2_HARNESS/test_run_benchmark_freeze.py"
)

fail=0
missing=0
echo "── THE GATE ──────────────────────────────────────────────────────────"
for c in "${CHECKS[@]}"; do
  if [[ ! -f "$ROOT/$c" ]]; then
    printf '  \033[31mMISSING\033[0m  %s\n' "$c"
    missing=$((missing + 1)); fail=1; continue
  fi
  out=$(python3 "$ROOT/$c" 2>&1); rc=$?
  if [[ $rc -eq 0 ]]; then
    printf '  \033[32mPASS\033[0m     %s\n' "$(echo "$out" | head -1)"
  else
    printf '  \033[31mFAIL\033[0m     %s\n' "$c"
    echo "$out" | sed 's/^/           /'
    fail=1
  fi
done

# Registers are derived custody surfaces. A stale register, or a builder that
# cannot run, fails closed rather than letting the inventory silently drift.
REGISTER_BUILDER="09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py"
if [[ ! -f "$ROOT/$REGISTER_BUILDER" ]]; then
  printf '  \033[31mMISSING\033[0m  %s\n' "$REGISTER_BUILDER"
  missing=$((missing + 1)); fail=1
else
  out=$(python3 "$ROOT/$REGISTER_BUILDER" --check 2>&1); rc=$?
  if [[ $rc -eq 0 ]]; then
    printf '  \033[32mPASS\033[0m     %s\n' "$(echo "$out" | head -1)"
  else
    printf '  \033[31mFAIL\033[0m     %s --check\n' "$REGISTER_BUILDER"
    echo "$out" | sed 's/^/           /'
    fail=1
  fi
fi

# The compiler suite is slower; run every registered test unless explicitly
# skipped. Running one green file is not evidence that the other files passed.
if [[ "${EMERGENTISM_SKIP_SLOW:-}" != "1" ]]; then
  for t in "$ROOT"/09_TOOLS/02_COMPILERS/test_*.py; do
    [[ -f "$t" ]] || continue
    out=$(python3 -B "$t" 2>&1); rc=$?
    if [[ $rc -eq 0 ]]; then
      printf '  \033[32mPASS\033[0m     %s (%s)\n' \
        "$(basename "$t")" "$(echo "$out" | grep -o 'Ran [0-9]* tests' || echo 'ok')"
    else
      printf '  \033[31mFAIL\033[0m     %s\n' "$(basename "$t")"
      echo "$out" | tail -20 | sed 's/^/           /'
      fail=1
    fi
  done
fi

# Lean is a distinct evidence gate, not part of EMERGENTISM_SKIP_SLOW. It may be
# skipped only by an explicit, visible acknowledgement.
LEAN_DIR="$ROOT/09_TOOLS/05_FORMAL_VERIFICATION"
if [[ "${EMERGENTISM_SKIP_LEAN:-}" == "1" ]]; then
  printf '  \033[33mSKIP\033[0m     Lean formal verification (EMERGENTISM_SKIP_LEAN=1)\n'
elif [[ ! -d "$LEAN_DIR" ]]; then
  printf '  \033[31mMISSING\033[0m  09_TOOLS/05_FORMAL_VERIFICATION\n'
  missing=$((missing + 1)); fail=1
elif ! command -v lake >/dev/null 2>&1; then
  printf '  \033[31mMISSING\033[0m  lake (set EMERGENTISM_SKIP_LEAN=1 only for an explicit skip)\n'
  missing=$((missing + 1)); fail=1
else
  out=$(cd "$LEAN_DIR" && lake build 2>&1); rc=$?
  if [[ $rc -eq 0 ]]; then
    printf '  \033[32mPASS\033[0m     Lean formal verification (lake build)\n'
  else
    printf '  \033[31mFAIL\033[0m     Lean formal verification (lake build)\n'
    echo "$out" | tail -40 | sed 's/^/           /'
    fail=1
  fi
fi

echo "──────────────────────────────────────────────────────────────────────"
if [[ $fail -ne 0 ]]; then
  echo "GATE: FAIL — the commit is blocked. Repair, or state why the check is wrong."
  [[ $missing -gt 0 ]] && echo "      $missing checker(s) MISSING — a gate that cannot run is not a gate."
  exit 1
fi
echo "GATE: PASS"
exit 0
