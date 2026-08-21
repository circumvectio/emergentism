#!/usr/bin/env bash
# Provision only operational L1-L4 via the Anthropic CLI (`ant`).
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
#   2. Create L1-L3 FIRST, capturing each id.
#   3. Assemble the L4 Kṣatriya (Arjuna) executor body from its *.agent.yaml and
#      INJECT a multiagent block built from the L1-L3 ids:
#        multiagent: {type: coordinator, agents: [<L1-L3 ids>, {type: self}]}
#      so a single L4 session delegates across the operational ensemble. L5-L7
#      remain non-deployable counsel and are never persistent hosted agents. `ant beta:agents
#      create` reads the assembled YAML from stdin.
set -euo pipefail
cd "$(dirname "$0")"

OUT="agent_ids.env"
: > "$OUT"

# L4 is deferred until hosted operational workers L1-L3 exist.
L4_FILE="agents/04_ksatriya_executor.agent.yaml"

model_for_file() {
  local spec_file="$1"
  local level
  local model_var
  local model_id
  level=$(awk -F'"' '/^[[:space:]]+level:/{print $2; exit}' "$spec_file")
  model_var="ROSETTA_MODEL_${level}"
  model_id="${!model_var:-}"
  if [ -z "$model_id" ]; then
    echo "Missing $model_var; model routing is registry-bound" >&2
    return 2
  fi
  printf '%s' "$model_id"
}

render_spec() {
  local spec_file="$1"
  local model_id
  model_id=$(model_for_file "$spec_file")
  SPEC_FILE="$spec_file" MODEL_ID="$model_id" python3 - <<'PY'
import os, sys, yaml
with open(os.environ["SPEC_FILE"], encoding="utf-8") as handle:
    spec = yaml.safe_load(handle)
spec["model"] = os.environ["MODEL_ID"]
yaml.safe_dump(spec, sys.stdout, allow_unicode=True, sort_keys=False)
PY
}

echo "Creating shared environment…"
ENV_ID=$(ant beta:environments create < emergentism.environment.yaml --transform id -r)
echo "ENV_ID=$ENV_ID" | tee -a "$OUT"

# 1. L1-L3 only — boundary rows L5-L7 are deliberately not provisioned.
OPERATIONAL_IDS=()
for f in agents/0[1-3]_*.agent.yaml; do
  name=$(awk -F'"' '/^name:/{print $2; exit}' "$f")
  id=$(render_spec "$f" | ant beta:agents create --transform id -r)
  key=$(basename "$f" .agent.yaml | tr '[:lower:]-' '[:upper:]_')
  echo "${key}_ID=$id" | tee -a "$OUT"
  echo "  + $name -> $id"
  OPERATIONAL_IDS+=("$id")
done

# 2. L4, wired as coordinator over L1-L3 plus self.
#    Assemble its YAML body and append an injected multiagent block. We use python3
#    (already a soft dep of this bundle via provision.py) to splice the roster in
#    cleanly without disturbing the L4 spec's existing tool/permission_policy config.
echo "Wiring L4 (Arjuna) as multiagent coordinator over ${#OPERATIONAL_IDS[@]} operational seats + self…"
l4_name=$(awk -F'"' '/^name:/{print $2; exit}' "$L4_FILE")
L4_ID=$(
  OPERATIONAL_IDS_CSV="$(IFS=,; echo "${OPERATIONAL_IDS[*]}")" \
  L4_FILE="$L4_FILE" \
  MODEL_ID="$(model_for_file "$L4_FILE")" \
  python3 - <<'PY' | ant beta:agents create --transform id -r
import os, sys, yaml
workers = [i for i in os.environ["OPERATIONAL_IDS_CSV"].split(",") if i]
with open(os.environ["L4_FILE"], encoding="utf-8") as handle:
    spec = yaml.safe_load(handle)
spec["model"] = os.environ["MODEL_ID"]
spec["multiagent"] = {"type": "coordinator", "agents": [*workers, {"type": "self"}]}
yaml.safe_dump(spec, sys.stdout, allow_unicode=True, sort_keys=False)
PY
)
key=$(basename "$L4_FILE" .agent.yaml | tr '[:lower:]-' '[:upper:]_')
echo "${key}_ID=$L4_ID" | tee -a "$OUT"
echo "  + $l4_name -> $L4_ID  [+coordinator over ${#OPERATIONAL_IDS[@]} + self]"

echo ""
echo "Wrote $OUT. L4 coordinates ${#OPERATIONAL_IDS[@]} operational seats + self; L5-L7 remain non-deployable counsel."
echo "Start a session with:  ant beta:sessions create --agent $L4_ID --environment-id $ENV_ID"
