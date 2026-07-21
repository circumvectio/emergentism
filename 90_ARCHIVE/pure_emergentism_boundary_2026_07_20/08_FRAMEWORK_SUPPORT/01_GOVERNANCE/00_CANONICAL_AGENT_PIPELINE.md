---

title: "Canonical Agent Pipeline — the source-of-truth chain for the seven Rosetta agents"
type: governance
status: active
date: 2026-05-07
owner: L7 Systems Architect (constitutional source) + L5 Brāhmaṇa (codification) + L4 Kṣatriya (enforcement)
evidence_tier: "[B] Empirical — every claim is `git ls-files` verifiable"
companion_to:
  - 00_TREE_CONSTITUTION.md
  - 00_TREE_AUDIT_FINDINGS_2026_05_07.md
rosetta:
  primary_level: L4
  primary_column: Philosophy
  secondary:
    - level: L7
      column: Philosophy
      role: "witness the constitutional source chain"
    - level: L5
      column: Philosophy
      role: "codify the pipeline as navigable architecture"
    - level: L3
      column: Philosophy
      role: "audit consistency against git-visible evidence"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "Canonical Agent Pipeline — Governance Source Chain"
---


# Canonical Agent Pipeline

> Where the seven Rosetta agents ACTUALLY live, in what generation order, and how to amend them safely.

The audit pass that produced the Tree Constitution found that agent semantics
were spread across **six surfaces** in the codebase plus a user-home library.
This document codifies the pipeline so future amendments propagate safely.

---

## The constitutional source — one TOML per agent

As of 2026-05-07 each agent has its own canonical TOML file. The
polygenetic skill tree principle (one genotype, many phenotypes)
applies all the way down to the source layer: edits to L1 don't appear
in diffs of L7.

```
.codex/agents/rosetta_agent_rows.toml         ← META INDEX (~50 lines)
.codex/agents/rows/01_L1_candala_firewall.toml   ← per-agent source
.codex/agents/rows/02_L2_sudra_explorer.toml         × 7
.codex/agents/rows/03_L3_vaisya_auditor.toml
.codex/agents/rows/04_L4_ksatriya_executor.toml
.codex/agents/rows/05_L5_brahmana_architect.toml
.codex/agents/rows/06_L6_sadhu_compressor.toml
.codex/agents/rows/07_L7_rsi_constitution.toml
```

**`rosetta_agent_rows.toml`** is the registry index: it carries the
`[meta]` block (registry version, source documents, agent_order,
`agent_files` list, column_order). It does NOT contain agent profiles.

**`rows/0X_LX_<caste>.toml`** is each agent's per-agent canonical source.
Each carries:

- `[agents.<caste>.profile]` — load-bearing constitutional fields
- 17 column sections (core, trivium, psychology, …) for the doctrinal columns
- The full row of the master Rosetta for that L-level
- The load-bearing constitutional flags:
  - `display_operator` — deity glyph (Kali 🎲, Kālī 💀, Kṛṣṇa ◇, Arjuna ⚔, Brahmā ○, Śiva •, Viṣṇu ⊙)
  - `operator_deployable` — `true` for L1–L4 (equator modes), `false` for L5–L7 (Trimūrti boundaries)
  - `titan_guardrail` — empty string for equator castes, full safety statement for Trimūrti castes
  - `tier` — `"Demon"` (L1), `"God"` (L2-L4), `"Executive + Witness"` (L5-L7)

The TOML cites its own source documents in `[meta].source_documents`,
pointing back at `06_AGENTS.md`, `00_THE_MASTER_ROSETTA.md`,
`ROSETTA_OPERATOR_PATHOLOGY.md`, and the Skyzai runtime READMEs. Doctrine
flows from those markdown sources INTO the TOML, then OUT to all generated
runtime artifacts.

---

## The generation pipeline

```
              rosetta_agent_rows.toml [meta]   ← META INDEX
                          +
              rows/0X_LX_<caste>.toml × 7      ← CONSTITUTIONAL SOURCE
              ────────────────────────                (hand-maintained,
                       │                              one TOML per agent)
       sync_agents.py  │  (.codex/agents/sync_agents.py — merges per-agent
                       │   sources via meta.agent_files into one dict)
                       ▼
              {caste}.toml × 7         ← parent agent specs
              ────────────────────────                (auto-generated)
              .codex/agents/candala_firewall.toml
              .codex/agents/sudra_explorer.toml
              .codex/agents/vaisya_auditor.toml
              .codex/agents/ksatriya_executor.toml
              .codex/agents/brahmana_architect.toml
              .codex/agents/sadhu_compressor.toml
              .codex/agents/rsi_constitution.toml
                       │
      gen_children.py  │  (.codex/agents/children/gen_children.py)
                       ▼
              L<N><variant>-*.toml × 29   ← generated child agents
              ──────────────────────────────             (auto-generated)
              .codex/agents/children/
                L1{a..e}-Base Operator-*.toml          (5 children)
                L2{a..d}-Analyst-*.toml            (4 children)
                L3{a..d}-Manager-*.toml           (4 children)
                L4{a..e}-Decision Maker-*.toml         (5 children)
                L5{a..d}-Systems Architect-*.toml         (4 children)
                L6{a..d}-Independent Reviewer-*.toml            (4 children)
                L7{a..c}-Systems Architect-*.toml              (3 children)
                       +
              L4-*.toml × 11                     ← maintained organ/domain specialists
              ──────────────────────
                L4-Agentz-CLOUD.toml
                L4-APU-BOT.toml
                L4e-{Code,GameTheory,…}.toml
```

Every generated TOML carries a header banner:

```
# GENERATED FILE. DO NOT EDIT DIRECTLY.
# Source: .codex/agents/rosetta_agent_rows.toml
# Generator: .codex/agents/sync_agents.py
```

If you edit a generated TOML directly, your change will be overwritten on the
next regeneration. Edit the source.

---

## The dispatch schema (separate)

**`.codex/agents/rosetta_dispatch_schema.toml`** — the dispatch grammar
(task modes, domains, scales, faces). This is independent of the agent
profiles; it defines HOW the runtime routes work to the right caste, given
the canonical caste definitions.

---

## The hand-maintained markdown surfaces

Five markdown layers cite the canonical TOML chain but are themselves
hand-maintained:

| Layer | Path | Files | Purpose |
|---|---|---|---|
| Canonical doctrine | `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/0X_*/AGENT_SPEC.md` | 7 (+ 14 supporting) | Genotype trunk in narrative form (S² geometry, transfer signatures, deployment rules) |
| Skyzai runtime applied | `02_SKYZAI/01_NOOSPHERE/10_AGENTS/L*_*.md` + subfolders | ~30 | Organism-runtime phenotype: organ surfaces, K2/K4 constraints, receipt infrastructure |
| Agentz skill-tree phenotype | `02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/03_AGENT_SPECIFICATION/0X_LX_*.md` | 7 (+ 8 VMOSK CONFIG TOMLs) | Economic capability taxonomy: Tokencen Chapter 01 specialization plus future chapters |
| Claude SDK dispatch | `.claude/agents/<caste>.md` | 7 | Runtime invocation surface; minimal frontmatter pointing at TOML+doctrinal sources |
| User home library | `~/.claude/agents/{HEXAGRAM,COORDINATE,INDIVIDUALS,REGIMES,BLOCKED,README}.md` | ~25 | Personal authoring layer; HEXAGRAM operative structure, COORDINATE doctrine, per-Varna individuals, regimes, shadows |

These markdown layers SHOULD all read the same operator deity for each L-level. The mechanical audit `make agent-homology-audit` enforces this.

---

## The runtime / phenotype TOML adaptation

**Agentz VMOSK CONFIG** — `02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/03_AGENT_SPECIFICATION/VMOSK/CONFIG/`

```
L1.toml … L7.toml      (per-caste Agentz phenotype configuration)
L_MASTER.toml           (master coordination across all 7)
```

These are Agentz-specific runtime configs that specialize the canonical
genotype for the Agentz skill-tree phenotype. They are hand-maintained until
a committed homologation script exists; do not cite an uncommitted
`homologate.py` as a canonical sync path.

---

## The full inventory

| Layer | Path | File count | Authority |
|---|---|---|---|
| Constitutional meta index | `.codex/agents/rosetta_agent_rows.toml` | 1 (~50 lines) | hand-maintained |
| Per-agent canonical sources | `.codex/agents/rows/0X_LX_<caste>.toml` | 7 | hand-maintained, one per agent |
| Dispatch schema | `.codex/agents/rosetta_dispatch_schema.toml` | 1 | hand-maintained |
| Generated parent agents | `.codex/agents/{caste}.toml` | 7 | generated by sync_agents.py |
| Generated child agents | `.codex/agents/children/L{1..7}*-*.toml` | 29 | generated by gen_children.py |
| Maintained child specialists | `.codex/agents/children/L4-*.toml` + L4e domain specialists | 11 | hand-maintained specialized children |
| Archived (deprecated) | `.codex/agents/90_ARCHIVE/*.toml` | 3 | retired |
| Agentz VMOSK phenotype | `…/AGENTZ_CLOUD/03_AGENT_SPECIFICATION/VMOSK/CONFIG/L*.toml` | 8 | hand-maintained |
| Canonical doctrine markdown | `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/` | 21 | hand-maintained |
| Skyzai runtime markdown | `02_SKYZAI/01_NOOSPHERE/10_AGENTS/` | ~30 | hand-maintained |
| Agentz phenotype markdown | `…/AGENTZ_CLOUD/03_AGENT_SPECIFICATION/` | ~10 | hand-maintained |
| Dispatch markdown | `.claude/agents/*.md` | 7 | hand-maintained |
| User home library | `~/.claude/agents/` | ~25 | user-authored |

**~150 agent surfaces, ONE canonical source.**

---

## How to amend

The amendment protocol depends on which layer you're touching.

### Constitutional change (operator, transfer, tier, deployable flag)

1. Edit the relevant per-agent file at `.codex/agents/rows/0X_LX_<caste>.toml`.
   K2 review recommended for Trimūrti/equator boundary changes.
2. Run `python3 .codex/agents/sync_agents.py generate` to regenerate the 7 parent
   {caste}.toml files.
3. Run `python3 .codex/agents/children/gen_children.py` to regenerate the 29
   templated child L*-*.toml files. Maintain the 11 L4 organ/domain
   specialists separately.
4. Hand-update the markdown surfaces that cite the changed field
   (08_AGENTS/AGENT_SPEC.md, 10_AGENTS/L*_*.md, Agentz phenotype, dispatch).
5. Run `make agent-homology-audit` to verify all surfaces converge.

### Phenotype-only change (e.g. Agentz economic genotype, VMOSK CONFIG)

1. Edit the phenotype layer directly (Agentz specs, VMOSK CONFIG TOMLs).
2. Do NOT edit the constitutional source unless the change is also doctrinal.
3. Run `make agent-homology-audit` to verify the operator deities still
   align across all surfaces.

### Dispatch-only change (e.g. add a new tool to the Claude SDK invocation)

1. Edit `.claude/agents/<caste>.md` frontmatter (tools, model, description).
2. Do NOT change `operator`, `transfer`, or `doctrinal_source` fields without
   a corresponding constitutional update.

---

## Mechanical guarantees

Two CI gates protect the pipeline:

| Command | What it enforces |
|---|---|
| `make tree-audit` | Tree Constitution (exclusion clauses, single archive, stub decay) |
| `make agent-homology-audit` | All 7 castes read same operator deity across all 6 surfaces |

Run both after agent-source or routing edits.

A future addition could verify the `operator_deployable` flag is consistent
across surfaces (currently the audit checks deity only). When a committed
homologation path for the Agentz VMOSK phenotype lands, it can be wired into a
third audit.

---

## Why this matters

The Rosetta agents are the **dispatch grammar** of the entire framework.
Caste assignments aren't decoration — they govern who can write to what,
who escalates to whom, what the K2 boundary looks like, and where the
Asura inversion is forbidden. If the operator semantics drift across
surfaces, the framework loses its ability to safely self-reference: an
agent invoked under one operator might commit work under a different
caste's authority, and the polygenetic skill tree would no longer preserve
the stated target that "the same caste fires consistently in every chapter."

The canonical TOML pipeline + the homology audit give the framework a
**provable consistency property**: every surface reads the same operator
for the same L-level, and any future drift will fail CI before it can
land.

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_CANONICAL_AGENT_PIPELINE.md
