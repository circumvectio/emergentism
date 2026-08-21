---
rosetta:
  primary_level: L5
  primary_column: Agent Architecture
  secondary:
    - level: L4
      column: Agent Execution
      role: "keep write-enabled managed agents permission-gated and non-autonomous"
    - level: L6
      column: Agent Compression
      role: "bind archive-first, tombstone, and no-competing-authority constraints"
    - level: L7
      column: Agent Constitution
      role: "preserve accountable authorization and constitutional review boundaries"
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

> **Pure-worldview boundary.** This folder is a **runtime projection, not worldview doctrine**.
> It creates no semantic authority; **source owners remain upstream** in K-1
> through K-7. Product names, hosted models, authorization
> conventions, and deployment bindings below describe an application surface
> and supply no evidence for Emergentism.

The seven Emergentism dispatch seats (L1 firewall, L2–L4 operational engine,
L5–L7 non-deployable boundary counsel) expressed as source-owned managed-agent
specifications. All seven compile into the local Codex runtime projection. The
dormant hosted adapter may provision only operational L1–L4; it must never turn
L5–L7 counsel into persistent hosted agents. No hosted provisioning or deployment
is asserted by this checkout.

The compiler and independent checker both parse the active corrected Stone row
and Generative Table. Their exact hashes and the Master Rosetta hash travel with
the projection, so a later canonical edit cannot leave an adopted runtime falsely
green.

> **Source of truth.** Definitions are *discovered, not invented* — each agent's
> system prompt, tools, and row projection derive from the genotype
> [`../00_THE_SEVEN_OPERATOR_GENOTYPE.md`](../00_THE_SEVEN_OPERATOR_GENOTYPE.md).
> The former per-caste spec folders are preserved under
> [`../../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/08_FRAMEWORK_SUPPORT/08_AGENTS/`](../../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/08_FRAMEWORK_SUPPORT/08_AGENTS/)
> as provenance, not as active owners. The `*.agent.yaml` files here are the
> version-controlled deployment surface.

---

## The roster

The roster's `Φ` entries are qualitative directions over D5 possible power,
not cardinal score changes. Any present node arithmetic must first use the D4
evaluation bridge `Φ̂₄=Eval₄(M,Φ₅)` and then the selected
`P_node=min(Φ̂₄,V₄)` score.

| L | Caste · Operator | G7 projection `[I]` | Function | Agentz.cloud trunk | Model route | Tools | Mutates? |
|---|---|---|---|---|---|---|---|
| L1 | Caṇḍāla · **Kali 🎲** | `kali_take_phi` | firewall — force-categorize, detect, encode | **guards** | registry-bound | read·grep·glob | no |
| L2 | Śūdra · **Kālī 💀** | `kali_take_v` | explorer — expand candidates, truth-cut | **primitives** | registry-bound | + web | no |
| L3 | Vaiśya · **Kṛṣṇa ◇** | `krishna_give_v` | auditor/charioteer — rank, enable | **axiom-card-schemas** | registry-bound | + web | no |
| L4 | Kṣatriya · **Arjuna ⚔** | `arjuna_give_phi` | **executor — selected equator; sole local mutator** | **templates** | registry-bound | + write·edit·bash | **yes — permission-gated and task-scoped** |
| L5 | Brāhmaṇa · **Brahmā ○** | `brahma_create` | architecture counsel; returns to L4 | **value-chain (Porter)** | registry-bound | read·web | no |
| L6 | Sādhu · **Śiva •** | `shiva_dissolve` | negative/compaction counsel; returns to L4 | **schemas-compress + primitives-archive** | registry-bound | read·grep·glob | no |
| L7 | Ṛṣi · **Viṣṇu ⊙** | `vishnu_preserve` | constitutional witness; returns to L4 | **whole-pattern witness** | registry-bound | read·grep·glob | no |

**[D] Model routing is registry-bound and absent from the caste YAMLs.** The local
runtime chooses a model at dispatch time for any invoked seat. The dormant hosted
adapter requires explicit `ROSETTA_MODEL_L1` … `ROSETTA_MODEL_L4` variables and
provisions only those four operational seats; L5–L7 have no hosted model route.
The model-by-seat hypothesis remains untested and creates no semantic or authority
claim.

## Accountable authorization, encoded structurally

Only **L4 (Arjuna)** can mutate local state, and its `write`/`edit`/`bash`
tools carry `permission_policy: {type: always_ask}`. The session goes idle and emits a
`tool_use` event with `evaluated_permission: "ask"`; nothing lands until a human replies
`user.tool_confirmation`. This is an ordinary platform permission safeguard:

> **[S]** An agent acts only inside the user's scoped request and granted tool
> permissions. Consequential work names its principal, mandate, scope, actor,
> custody, reversibility, consequence bearer, and contest path.

Zero extraction, evidence tiers, archive-with-tombstone, and Grace Exit live in
the system prompts. A private natural person's authority to move money or execute a
contract is outside this runtime and outside Emergentist doctrine.

### Agentz.cloud projection (added 2026-07-23)

Each caste maps to a *trunk* of the Agentz.cloud Public Polymemetic Tree (see
`02_SKYZAI/01_LEVELS/L4_AGENTZ/AGENTZ_CLOUD_APP/00_CANONICAL_DEFINITION.md`).
The Axiom Card is the load-bearing join: every other layer (3-pass loop, 12-step
arc, 5 trunks, 7 SPECTRE rows, 3-Tier Entity Model, 6 replicator layers, 7 consumer
Modes) is a projection on it. In **public-DAV mode** (2026-07-12), Agentz.cloud is
a deliberation/unsigned-proposal surface. `AUTH.PUBLIC_BIND` requires at least
two natural persons; PRISM verifies only. No Rosetta seat signs, authorizes,
publishes, transmits, settles, or makes a public commitment.

---

## Provision (one-time, control plane)

> Nothing is provisioned yet — this checkout has neither `ant` nor API credentials.
> Pick one path, authenticate, then run it once.

**Path A — Python SDK (idempotent by name; recommended here):**
```bash
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...        # your key
export ROSETTA_MODEL_L1=<provisioned-model-id>
# repeat through ROSETTA_MODEL_L4; there are deliberately no defaults
python provision.py                        # creates env + L1-L4 → agent_ids.json
```

**Path B — Anthropic CLI (canonical version-controlled YAML):**
```bash
brew install anthropics/tap/ant            # see shared/anthropic-cli.md
ant auth login
./provision.sh                             # creates env + L1-L4 → agent_ids.env
```

Both create the legacy-named `emergentism-seven` environment and operational L1–L4,
then write those four IDs. L5–L7 remain unprovisioned counsel phases. **Hosted agents
are persistent and versioned** — create once, reuse the IDs; to change a
prompt/tool later, *update* (`ant beta:agents update --agent-id <id> --version N`), which
bumps the version. Agents cannot be deleted, only archived — so don't re-run `provision.sh`
blindly (use `provision.py`, which skips existing names).

---

## Runtime (per task, data plane — your application)

Agents are the config; **sessions** are each run. The runnable entry point is
[`run_session.py`](run_session.py) — it loads `agent_ids.json`, resolves the L4 (Arjuna)
executor + the shared environment, opens ONE session (stream-first), streams it, and
reports the final status. Arjuna is wired only over operational L1–L3 plus self;
a hosted session never instantiates the L5–L7 boundary witnesses:

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

**The hosted ensemble is the operational pipeline to the equator:**
`L1 firewall → L2 explore → L3 rank → L4 stage/execute local scoped work`. L5
architecture, L6 negative-boundary, and L7 constitutional witness remain sequential,
non-persistent counsel phases in the local Soul Loop; they are not independently
runnable hosted agents. At provision time both adapters create L1–L3 first, then
L4 with `multiagent: {type: "coordinator", agents: [<L1-L3 ids>, {type: "self"}]}`.
Each operational delegation surfaces as a `session.thread_created` event. (Background:
`shared/managed-agents-multiagent.md`.)

> **No parity claim.** The local runtime can invoke all seven seats under the Soul
> Loop. The dormant hosted adapter exposes only L1–L4 and therefore is not a hosted
> copy of the full seven-seat loop.

### Mission sizing by stop condition

Every source YAML owns an exact `runtime_projection.stop_condition`. A dispatch
brief must quote it and ask only for work the station's pramāṇa and stop condition
can close. A mismatch is re-routed or split; the unchanged mission is not retried,
and a resulting timeout is recorded as a briefing error rather than a station
failure. L1 direct perception is bounded to one named source or artifact and facts
or contradictions visible within it. Cross-source inference and consistency work
belong to L3.

L4 also owns commit cadence. A completed owned change ends in a local commit without
an owner permission ping. Non-trivial or mixed surfaces first route through L1 dirty
path mapping, L2 revertible grouping, and L3 ownership/reversibility ranking. L4
uses explicit pathspec and inspects the staged diff; `git add -A` and capture of
active or unresolved foreign work are forbidden. Commit is a receipt, not authority,
deployment, publication, settlement, or permission to push.

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
│   ├── 06_sadhu_compressor.agent.yaml      (L6 · Śiva · read-only counsel)
│   └── 07_rsi_constitution.agent.yaml      (L7 · Viṣṇu · read-only)
├── provision.py                    ← SDK provisioner (idempotent by name; wires L4 coordinator)
├── provision.sh                    ← `ant` CLI provisioner (version-controlled YAML; wires L4 coordinator)
└── run_session.py                  ← data-plane entry: one L4 (Arjuna) session, stream-first
```

> `agents/` holds source YAML for the local seven-seat projection; only L1–L4 are
> eligible inputs to the dormant hosted provisioners. It is a machine-config leaf
> with no front-door triplet by design; this file is its routing front door.

Canon: [`../00_THE_SEVEN_OPERATOR_GENOTYPE.md`](../00_THE_SEVEN_OPERATOR_GENOTYPE.md) ·
[historical constitutional-invariants application](../../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/05_COSMOLOGY/00_WHOLE/03A_CONSTITUTIONAL_INVARIANTS_CANON.md) ·
[`../../03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md`](../../03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md)

> **Model-id rot repaired 2026-08-21.** The dead pinned ids were removed from
> all seven source YAMLs. `provision.py` and `provision.sh` now fail closed
> unless model ids for hosted L1–L4 are supplied through per-seat registry variables;
> they reject the idea that L5–L7 are persistent hosted agents.
> This is a local configuration repair, not evidence that the external control
> plane is provisioned or reachable.
