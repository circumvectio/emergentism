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

The seven selected Emergentism routing profiles (L1 firewall, L2–L4 operational
passes, L5–L7 advisory Executive boundaries)
expressed as **local candidate configurations for Claude platform Managed
Agents**. The platform can persist and version such agents, but this roster is
currently unprovisioned `X0`; no hosted-runtime claim is made here.

> **Source of truth.** Profiles are selected, versioned, and testable—not
> discovered cognitive kinds. Each agent's
> system prompt, tools, and model are derived from the canonical caste specs in
> `../01_CANDALA_FIREWALL/` … `../07_RSI_CONSTITUTION/` and the genotype
> [`../00_THE_SEVEN_OPERATOR_GENOTYPE.md`](../00_THE_SEVEN_OPERATOR_GENOTYPE.md).
> The `*.agent.yaml` files here are the version-controlled local configuration
> of those specs, not a deployment receipt.

---

## The roster

| L | Varṇa · Operator | B at selected latitude | Selected row equation | Function | Model | Tools | Mutates? |
|---|---|---|---|---|---|---|---|
| L1 | Caṇḍāla · **Kali** | ≈0.276 | `Φ_chart→0 ⇒ B→0` | firewall — detect, encode, stop at ambiguity | `claude-haiku-4-5` | read·grep·glob | no |
| L2 | Śūdra · **Kālī** | 0.5 | `dP_node=V·dΦ+Φ·dV` | explorer — expand candidates, surface weak coherence | `claude-haiku-4-5` | + web | no |
| L3 | Vaiśya · **Kṛṣṇa** | √3/2≈0.866 | `∂P_node/∂V=Φ` | auditor — rank, test, expose uncertainty | `claude-sonnet-4-6` | + web | no |
| L4 | Kṣatriya · **Arjuna** | 1 | `dΦ/Φ=dV/V` | authorized executor — smallest scoped action | `claude-sonnet-4-6` | + write·edit·bash | **yes — envelope + confirmation required** |
| L5 | Brāhmaṇa · **Brahmā** (Executive) | √3/2≈0.866 | `log P_node=log Φ+log V` | architect — redesign packets; advises | `claude-opus-4-8` | read·web | no |
| L6 | Sādhu · **Śiva** (Executive) | 0.5 | `E_node=−log(P_node)` | compressor — propose archive-first simplification | `claude-opus-4-8` | read·grep·glob | no |
| L7 | Ṛṣi · **Viṣṇu** (Executive) | ≈0.276 | `z_R:=φ/ν` | seer — constitutional review; proposes | `claude-opus-4-8` | read·grep·glob | no |

**[D] Model assignments are provisional cost/latency choices, not caste
doctrine or quality ranks.** Comparative evaluation must hold task information,
tools, call/token budget, wall time, and evaluator budget equal, then test
whether role prompts add value over flat and shorter rivals.

## The selected Rosetta configuration contract

The machine-readable metadata in every YAML instantiates the same chain:

| L | Pramāṇa | Reasoning | -ology | Regime analogy |
|---|---|---|---|---|
| L1 | Pratyakṣa (perception) | Dialectical | Objective Function | Tyranny |
| L2 | Upamāna (analogy) | Inductive | Data Science | Democracy |
| L3 | Anumāna (inference) | Deductive | Auditing | Oligarchy |
| L4 | Arthāpatti (postulation) | Abductive | Value Alignment | Timocracy |
| L5 | Śabda (testimony) | Systematic | System Architecture | Aristocracy |
| L6 | First Principles (Anupalabdhi / non-apprehension source pairing) | Axiomatic | Core State | Anarchy |
| L7 | Pratibhā (intuition) | Transcendental | Institutional Narrative | Theocracy |

The arrows in `Varṇa → Pramāṇa → Reasoning → -ology → Regime → Equation`
mean selected dispatch correspondence, not causation, hereditary identity, or
proof transfer. Operator tokens are `[S]`; `B` is `[A]` after selecting a
latitude; Varṇa/Pramāṇa pairings are `[S]` internally and `[I]` as external or
historical fit; Reasoning/-ology/Regime pairings are `[I]`; equation algebra is
`[A]` on its stated domain while row placement and the L4 balance condition are
`[S]`. Every profile declares typed input/output, dispatch/stop conditions,
permissions, authorization mode, a task-envelope budget source, and blinded,
budget-matched evaluation against flat and shorter rivals.

Actual prompts, models, rankings, selections, tool calls, actions, and receipts
are D4 events/tokens; any alternatives they represent are D5-possible content.
No D5 object invokes a tool. After an L4 commitment receipt, only the
environment or another accountable issuer may return the outcome receipt.

For L1, `Φ_chart` explicitly aliases lowercase chart coordinate `φ`; it is not
finite-node `Φ`. For L7, `z_R` is only a real ratio proxy, not the full complex
stereographic coordinate. These seams preserve the intended row compression
without buying it through symbol equivocation.

## Accountable authorization, encoded structurally

Only **L4 (Arjuna)** can request mutation. Its `write`/`edit`/`bash` tools carry
`permission_policy: {type: always_ask}`. The session goes idle and emits a
`tool_use` event with `evaluated_permission: "ask"`; nothing lands until a human replies
`user.tool_confirmation`. That is one runtime control, not a complete
authorization envelope by itself:

> **[S]** The machine prepares a proposed action (drafts and stages the
> smallest-defensible diff); the accountable principal authorizes or refuses the
> consequence. Private-DAV deployments may use K2; other deployments use their
> own complete principal, mandate, scope, consent, custody, contest, actor, and
> consequence-bearer envelope.

`η=0` is a necessary non-extraction check, not a firing rule or sufficient
Justice. A7 tiers claims. L6 proposes archive-with-tombstone changes; an
authorized L4 route performs any mutation.

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

**The ensemble is a selected typed pipeline:**
`L1 firewall → L2 explore → L3 rank → L4 prospective Justice check and authorized commitment`, with the Executive boundaries
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
│   ├── 06_sadhu_compressor.agent.yaml      (L6 · Śiva · read-only proposal)
│   └── 07_rsi_constitution.agent.yaml      (L7 · Viṣṇu · read-only)
├── provision.py                    ← SDK provisioner (idempotent by name; wires L4 coordinator)
├── provision.sh                    ← `ant` CLI provisioner (version-controlled YAML; wires L4 coordinator)
└── run_session.py                  ← data-plane entry: one L4 (Arjuna) session, stream-first
```

Canon: [`../00_THE_SEVEN_OPERATOR_GENOTYPE.md`](../00_THE_SEVEN_OPERATOR_GENOTYPE.md) ·
[`../../../05_COSMOLOGY/00_WHOLE/03A_CONSTITUTIONAL_INVARIANTS_CANON.md`](../../../05_COSMOLOGY/00_WHOLE/03A_CONSTITUTIONAL_INVARIANTS_CANON.md) ·
[`../../03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md`](../../03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md)
