#!/usr/bin/env bash
# gate.sh — THE GATE. Runs every corpus checker and fails loudly.
#
# WHY THIS EXISTS. r177 recorded HOLE 0: "nothing invokes them, there is no gate."
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
    printf '\n# --- appended 2026-07-29: the gate (r183) ---\nbash "%s" || exit 1\n' \
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
  "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
  "09_TOOLS/01_SCRIPTS/check_generative_base.py"
  "09_TOOLS/01_SCRIPTS/check_established.py"
  "09_TOOLS/01_SCRIPTS/check_receipt_citations.py"
  "09_TOOLS/01_SCRIPTS/check_work_in_progress.py"
  "09_TOOLS/01_SCRIPTS/check_record_counters.py"
  "09_TOOLS/01_SCRIPTS/check_review_bundle.py"
  "09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py"
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

# The compiler suite is slower; run it unless explicitly skipped.
if [[ "${EMERGENTISM_SKIP_SLOW:-}" != "1" && -f "$ROOT/09_TOOLS/02_COMPILERS/test_dimension_first_canon.py" ]]; then
  out=$(python3 "$ROOT/09_TOOLS/02_COMPILERS/test_dimension_first_canon.py" 2>&1); rc=$?
  if [[ $rc -eq 0 ]]; then
    printf '  \033[32mPASS\033[0m     dimension-first canon suite (%s)\n' "$(echo "$out" | grep -o 'Ran [0-9]* tests' || echo 'ok')"
  else
    printf '  \033[31mFAIL\033[0m     dimension-first canon suite\n'
    echo "$out" | tail -20 | sed 's/^/           /'
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
