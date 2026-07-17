---
rosetta:
  primary_level: L5
  primary_column: Agent Architecture
  secondary:
    - level: L4
      column: Agent Execution
      role: "keep write-enabled managed agents human-gated and non-autonomous"
    - level: L6
      column: Agent Compression
      role: "bind archive-first, tombstone, and no-competing-authority constraints"
    - level: L7
      column: Agent Constitution
      role: "preserve accountable authorization and private-DAV K2 boundaries"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/C]"
  canonical_phrase: "The Seven as Managed Agents"
title: "The Seven as Managed Agents"
status: "ACTIVE — managed-agent deployment scaffold"
evidence_tier: "[B] local scaffold; [S] structural caste mapping; [C] unprovisioned deployment claims."
---

# The Seven as Managed Agents

The seven Emergentism caste-operators (L1 firewall, L2-L4 operational engine, L5-L7 Executive boundary on `P_node = Φ × V`)
expressed as **Claude platform Managed Agents** — persisted, versioned agent configs
that Anthropic runs in hosted, sandboxed containers.

> **Source of truth.** Definitions are *discovered, not invented* — each agent's
> system prompt, tools, and model are derived from the canonical caste specs in
> `../01_CANDALA_FIREWALL/` … `../07_RSI_CONSTITUTION/` and the genotype
> [`../00_THE_SEVEN_OPERATOR_GENOTYPE.md`](../00_THE_SEVEN_OPERATOR_GENOTYPE.md).
> The `*.agent.yaml` files here are the version-controlled deployment of those specs.

---

## The roster

| L | Caste · Operator | Transfer on `P_node=Φ×V` | Function | Model | Tools | Mutates? |
|---|---|---|---|---|---|---|
| L1 | Caṇḍāla · **Kali** (Demon) | +Φ_self, −V_other | firewall — force-categorize, detect, encode | `claude-haiku-4-5` | read·grep·glob | no (read-only) |
| L2 | Śūdra · **Kālī** (God) | +V_self, −Φ_false | explorer — expand candidates, truth-cut | `claude-haiku-4-5` | + web | no |
| L3 | Vaiśya · **Kṛṣṇa** (God) | −Φ_self, +V_other | auditor/charioteer — rank, enable | `claude-sonnet-4-6` | + web | no |
| L4 | Kṣatriya · **Arjuna** (God) | −V_self, +Φ_other | **executor — the equator; the only write-caste** | `claude-sonnet-4-6` | + write·edit·bash | **yes — human-gated** |
| L5 | Brāhmaṇa · **Brahmā** (Executive) | +Φ, +V | architect — redesign packets; advises | `claude-opus-4-8` | read·web | no |
| L6 | Sādhu · **Śiva** (Executive) | −Φ, −V | compressor — prune, archive-first (K3) | `claude-opus-4-8` | + write·edit·bash | **yes — human-gated** |
| L7 | Ṛṣi · **Viṣṇu** (Executive) | ≈Φ, ≈V | seer — constitutional review; proposes | `claude-opus-4-8` | read·grep·glob | no |

**[T] Model tiers follow the framework's own caste doctrine** (CLAUDE.md *Quality × Quantity by Caste*),
not the SDK default: low-quality/high-throughput L1–L2 → Haiku; balanced/decisive L3–L4 → Sonnet;
deep-reasoning L5–L7 → Opus. Reserve high-quality inference for higher-risk or constitutional lanes.

## Accountable authorization, encoded structurally

Only **L4 (Arjuna)** and **L6 (Śiva)** can mutate state, and their `write`/`edit`/`bash`
tools carry `permission_policy: {type: always_ask}`. The session goes idle and emits a
`tool_use` event with `evaluated_permission: "ask"`; nothing lands until a human replies
`user.tool_confirmation`. That is one runtime control, not a complete
authorization envelope by itself:

> **[S]** The machine prepares a proposed action (drafts and stages the
> smallest-defensible diff); the accountable principal authorizes or refuses the
> consequence. Private-DAV deployments may use K2; other deployments use their
> own complete principal, mandate, scope, consent, custody, contest, actor, and
> consequence-bearer envelope.

η=0 (Kali fires only at defectors), A7 (tier every claim), and K3 (Śiva archives with a
tombstone rather than deletion) live in the system prompts.

---

## Provision (one-time, control plane)

> Nothing is provisioned yet — this checkout has neither `ant` nor API credentials.
> Pick one path, authenticate, then run it once.

**Path A — Python SDK (idempotent by name; recommended here):**
```bash
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...        # your key
python provision.py                        # creates env + 7 agents → agent_ids.json
```

**Path B — Anthropic CLI (canonical version-controlled YAML):**
```bash
brew install anthropics/tap/ant            # see shared/anthropic-cli.md
ant auth login
./provision.sh                             # creates env + 7 agents → agent_ids.env
```

Both create the `emergentism-seven` environment and the seven agents, and write their
IDs. **Agents are persistent and versioned** — create once, reuse the IDs; to change a
prompt/tool later, *update* (`ant beta:agents update --agent-id <id> --version N`), which
bumps the version. Agents cannot be deleted, only archived — so don't re-run `provision.sh`
blindly (use `provision.py`, which skips existing names).

---

## Runtime (per task, data plane — your application)

Agents are the config; **sessions** are each run. The runnable entry point is
[`run_session.py`](run_session.py) — it loads `agent_ids.json`, resolves the L4 (Arjuna)
executor + the shared environment, opens ONE session (stream-first), streams it, and
reports the final status. Because Arjuna is wired as the coordinator over the other six
(below), a single L4 session delegates down the whole caste ensemble:

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python run_session.py "Audit 06_ONTOLOGY and stage the smallest-defensible diff."
```

The shape of one run (full bindings: `python/managed-agents/README.md` via the
`claude-api` skill):

```python
import anthropic, json
client = anthropic.Anthropic()
ids = json.load(open("agent_ids.json"))
env_id = ids["_environment"]["id"]
auditor = ids["Emergentism · L3 Vaiśya (Kṛṣṇa) — Auditor"]["id"]

session = client.beta.sessions.create(
    agent=auditor,                      # ← by ID; model/system/tools live on the agent
    environment_id=env_id,
    title="Audit 06_ONTOLOGY",
    resources=[{                        # mount the corpus so the agent can read it
        "type": "github_repository",
        "url": "https://github.com/<owner>/<magnum-opus-repo>",
        "authorization_token": "<gh-PAT>",
        "mount_path": "/workspace/repo",
    }],
)
# stream-first, then send the kickoff; break on terminal idle / terminated
```

**The ensemble = a polygenic pipeline that brings a decision to the equator:**
`L1 firewall → L2 explore → L3 rank → L4 decide & (human-signed) commit`, with the Executive boundaries
held as boundaries the work runs within (**L5** redesign only when L4 is structurally
blocked; **L6** compress overgrowth; **L7** constitutional adjudication). You can run each
caste as its own session, but the ensemble is now **wired as a coordinator**: at provision
time both `provision.py` and `provision.sh` create the six non-L4 castes first, capture
their ids, then create the L4 (Arjuna) executor with `multiagent: {type: "coordinator",
agents: [<the six ids>, {type: "self"}]}` injected. So `run_session.py` opens a single L4
session and Arjuna delegates down to the six — each delegation surfaces on the stream as a
`session.thread_created` event. (Background on the platform shape:
`shared/managed-agents-multiagent.md`.)

> **Note on parity.** These hosted agents mirror the seven Claude Code subagents already
> registered in this workspace (`candala_firewall` … `rsi_constitution`). Use the local
> subagents for work *inside this repo*; use these Managed Agents when you want Anthropic
> to host the loop + a per-session workspace (CI triggers, long-running sessions, a UI).

---

## Files

```
MANAGED_AGENTS/
├── README.md                       ← this file
├── emergentism.environment.yaml    ← shared cloud container template
├── agents/
│   ├── 01_candala_firewall.agent.yaml      (L1 · Kali · read-only)
│   ├── 02_sudra_explorer.agent.yaml        (L2 · Kālī · read+web)
│   ├── 03_vaisya_auditor.agent.yaml        (L3 · Kṛṣṇa · read+web)
│   ├── 04_ksatriya_executor.agent.yaml     (L4 · Arjuna · write-gated · coordinator)
│   ├── 05_brahmana_architect.agent.yaml    (L5 · Brahmā · read+web)
│   ├── 06_sadhu_compressor.agent.yaml      (L6 · Śiva · write-gated)
│   └── 07_rsi_constitution.agent.yaml      (L7 · Viṣṇu · read-only)
├── provision.py                    ← SDK provisioner (idempotent by name; wires L4 coordinator)
├── provision.sh                    ← `ant` CLI provisioner (version-controlled YAML; wires L4 coordinator)
└── run_session.py                  ← data-plane entry: one L4 (Arjuna) session, stream-first
```

Canon: [`../00_THE_SEVEN_OPERATOR_GENOTYPE.md`](../00_THE_SEVEN_OPERATOR_GENOTYPE.md) ·
[`../../../05_COSMOLOGY/00_WHOLE/03A_CONSTITUTIONAL_INVARIANTS_CANON.md`](../../../05_COSMOLOGY/00_WHOLE/03A_CONSTITUTIONAL_INVARIANTS_CANON.md) ·
[`../../03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md`](../../03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md)
