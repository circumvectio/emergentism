#!/usr/bin/env bash
# commit_2026_04_23.sh — land the 2026-04-23 uplink delta from charioteer session
#
# Scope: ONLY the two uplink files I (charioteer) edited.
#   - EMERGENTISM_ORG/11_UPLINK/05_ARCHITECTURE.md  (header recompiled to 2026-04-23; runbook landing note)
#   - EMERGENTISM_ORG/11_UPLINK/09_STATE.md         (Shipped Packets row for FIRST_DELIBERATION_RUNBOOK; judgment line extended)
#
# NOT in scope — the parallel session owns and will commit these separately:
#   - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/circulation/ai_client.py
#   - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/council/light_council.py
#   - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/scripts/first_deliberation.py (untracked)
#   - SKYZAI_ORG/02_ORGANS/Skyzai/memory/26_TECH_RESEARCH_ORGANISM_F1_F4.md      (untracked)
#   - SKYZAI_ORG/02_ORGANS/Skyzai/memory/27_DEEP_TECH_EVAL_APU_CIRCLE.md         (untracked)
#
# Prerequisites:
#   1. cd to the repo root: /Users/Yves/Documents/Emergence_22_04 (or equivalent)
#   2. Sandbox left a 0-byte .git/index.lock behind. Clear it first:
#        rm -f .git/index.lock
#
# Then run: bash EMERGENTISM_ORG/09_TOOLS/scripts/commit_2026_04_23.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

if [ -f .git/index.lock ]; then
  echo "ERROR: .git/index.lock still present. Remove it first:  rm -f .git/index.lock" >&2
  exit 1
fi

FILES=(
  "EMERGENTISM_ORG/11_UPLINK/05_ARCHITECTURE.md"
  "EMERGENTISM_ORG/11_UPLINK/09_STATE.md"
)

echo "Staging charioteer uplink delta:"
for f in "${FILES[@]}"; do
  echo "  - $f"
done
git add -- "${FILES[@]}"

echo
echo "Staged diff:"
git diff --cached --stat

echo
echo "Committing..."
git commit -m "$(cat <<'EOF'
docs(uplink): 2026-04-23 runbook-landing delta

EMERGENTISM_ORG/11_UPLINK/05_ARCHITECTURE.md:
- Header recompiled to 2026-04-23.
- Adds note that FIRST_DELIBERATION_RUNBOOK.md has landed as the
  1-function adapter wedge for `call_llm_provider`, unblocking both
  Light Council and full 9-stage protocol in the same patch.

EMERGENTISM_ORG/11_UPLINK/09_STATE.md:
- Shipped Packets table gains a row for First Deliberation Runbook.
- Judgment-line trace point to the runbook + 1-function wedge as the
  path that flips `judgment_stubbed` to live.

Source of truth: `02_ORGANS/Agentz/FIRST_DELIBERATION_RUNBOOK.md`
(committed earlier in 5fdc73c14).
EOF
)"

echo
echo "Commit landed. Recent log:"
git log --oneline -3
