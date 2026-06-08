#!/usr/bin/env bash
# Provision the seven Emergentism caste agents via the Anthropic CLI (`ant`).
# Canonical version-controlled flow: the *.agent.yaml files are the source of truth.
#
# Prerequisites:
#   brew install anthropics/tap/ant        # or see shared/anthropic-cli.md
#   ant auth login                         # or: export ANTHROPIC_API_KEY=sk-ant-...
#
# One-time setup (control plane). Re-running CREATES DUPLICATES — `ant` has no
# create-or-reuse; for re-apply use `ant beta:agents update --agent-id <id> --version N`.
# Prefer provision.py (idempotent by name) if you may run more than once.
#
# Order matters (multiagent coordinator wiring):
#   1. Create the shared environment.
#   2. Create the SIX non-L4 caste agents FIRST, capturing each id.
#   3. Assemble the L4 Kṣatriya (Arjuna) executor body from its *.agent.yaml and
#      INJECT a multiagent block built from the six captured ids:
#        multiagent: {type: coordinator, agents: [<six ids>, {type: self}]}
#      so a single L4 session delegates down the caste ensemble. `ant beta:agents
#      create` reads the assembled YAML from stdin.
set -euo pipefail
cd "$(dirname "$0")"

OUT="agent_ids.env"
: > "$OUT"

# The L4 executor is identified by the 04_ spec file; everything else is "the six".
L4_FILE="agents/04_ksatriya_executor.agent.yaml"

echo "Creating shared environment…"
ENV_ID=$(ant beta:environments create < emergentism.environment.yaml --transform id -r)
echo "ENV_ID=$ENV_ID" | tee -a "$OUT"

# 1. The six non-L4 castes first — capture their ids for the L4 coordinator roster.
SIX_IDS=()
for f in agents/0*.agent.yaml; do
  [ "$f" = "$L4_FILE" ] && continue        # defer L4 until the six exist
  name=$(awk -F'"' '/^name:/{print $2; exit}' "$f")
  id=$(ant beta:agents create < "$f" --transform id -r)
  key=$(basename "$f" .agent.yaml | tr '[:lower:]-' '[:upper:]_')
  echo "${key}_ID=$id" | tee -a "$OUT"
  echo "  + $name -> $id"
  SIX_IDS+=("$id")
done

# 2. The L4 Kṣatriya (Arjuna) executor, wired as coordinator over the six.
#    Assemble its YAML body and append an injected multiagent block. We use python3
#    (already a soft dep of this bundle via provision.py) to splice the roster in
#    cleanly without disturbing the L4 spec's existing tool/permission_policy config.
echo "Wiring L4 (Arjuna) as multiagent coordinator over ${#SIX_IDS[@]} castes + self…"
l4_name=$(awk -F'"' '/^name:/{print $2; exit}' "$L4_FILE")
L4_ID=$(
  SIX_IDS_CSV="$(IFS=,; echo "${SIX_IDS[*]}")" \
  L4_FILE="$L4_FILE" \
  python3 - <<'PY' | ant beta:agents create --transform id -r
import os, sys
six = [i for i in os.environ["SIX_IDS_CSV"].split(",") if i]
roster = "".join(f"  - {i}\n" for i in six) + "  - {type: self}\n"
body = open(os.environ["L4_FILE"]).read()
if not body.endswith("\n"):
    body += "\n"
# Inject the coordinator roster: the six captured agent ids + self-delegation.
body += "multiagent:\n  type: coordinator\n  agents:\n" + roster
sys.stdout.write(body)
PY
)
key=$(basename "$L4_FILE" .agent.yaml | tr '[:lower:]-' '[:upper:]_')
echo "${key}_ID=$L4_ID" | tee -a "$OUT"
echo "  + $l4_name -> $L4_ID  [+coordinator over ${#SIX_IDS[@]} + self]"

echo ""
echo "Wrote $OUT. L4 (Arjuna) coordinates ${#SIX_IDS[@]} castes + self."
echo "Start a session with:  ant beta:sessions create --agent $L4_ID --environment-id $ENV_ID"
