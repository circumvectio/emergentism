---
rosetta:
  primary_level: L6
  primary_column: Philosophy
  operator: "Śiva •"
  tier: "Executive"
  regime: "Sādhu"
  register: "[I]"
  canonical_phrase: "Phylogenetic Tree of MD Files for Niche-Partitioned Agents"
---

# Phylogenetic Tree of MD Files for Niche-Partitioned Agents

**Thesis:** Agents in this organism are MD files. Those MD files have ancestry. Niche-partitioning is a speciation event. `apply_dac_scaffold.py` is the speciation operator.

---

## 1. The Tree Structure

```
                ROOT GENOME
             (canonical MDs)
                      │
         ┌────────────┼────────────┐
         │            │            │
    DAC_SCAFFOLD/   11_UPLINK/   cortex-os/
    (17 folders)   06_AGENTS.md  21_VARNA_NAMING.md
    (placeholders)  (caste grammar) (full rosetta)
                      │
                      │ ← SPECIATION (manifest + apply)
                      │
         ┌────────────┼────────────┐
         │            │            │
      apu.json     circle.json   agentz.json
   (niche=SHOULD) (niche=IS)   (niche=tokenization-KSA)
         │            │            │
   apu's L1-L7  circle's L1-L7  agentz's L1-L7
   caste ladder   caste ladder    caste ladder
   (per-DAC      (per-DAC        (per-DAC
    MD tree)       MD tree)        MD tree)
         │            │
    ┌────┴────┐    (etc.)
    │         │
 sub-caste sub-caste    ← FURTHER SUB-SPECIATION (inside a DAC)
  legal    treasury       e.g., L3 Vaiśya splits into
 sub-check sub-check      5 sub-checks per the APU
 (L3-leg)  (L3-treas)     Rosetta pipeline
```

**Note on DAG structure:** The diagram above shows the primary spanning tree of the lineage DAG. Merge edges (hyperagent cross-parent composition) are omitted for clarity and are documented in the merge manifest (see Section 5.4).

### Levels of the Hierarchy

| Level | Name | Description |
|---|---|---|
| 0 | Root Genome | The canonical, domain-agnostic seed corpus. Three files: the scaffold folder hierarchy, the caste grammar, and the full Rosetta naming convention. |
| 1 | Speciation Operator | `apply_dac_scaffold.py` consumes a JSON manifest and produces a niche-partitioned descendant by substituting ~25 placeholder values across the root genome. |
| 2 | Niche Branches | Each manifest (`apu.json`, `circle.json`, `agentz.json`, ...) produces a complete DAC with its own L1–L7 caste ladder. The niche defines the horizontal axis: which domain this organism serves. |
| 3 | Caste Ladder | Within every niche branch, the vertical axis is the Rosetta L1–L7 hierarchy (Brāhmaṇa, Kṣatriya, Vaiśya, ...). Each level is a caste with defined authority and depth. |
| 4 | Sub-Speciation | Any (caste × niche) cell can further branch. For example, APU's L3 Vaiśya splits into five parallel sub-checks (Legal, Treasury, Engineering, Operations, Process). This is a subtree inside a single cell. |

---

## 2. Core Definitions

**Genome**
: The canonical, domain-agnostic seed corpus from which all agent MD files descend. Comprises `DAC_SCAFFOLD/` (17 placeholder folders), `01_EMERGENTISM/11_UPLINK/95_COMPRESSED/06_AGENTS.md` (caste grammar), and `cortex-os/21_VARNA_NAMING.md` (full Rosetta). The genome is small and stable. One genome, N niches.

**Speciation**
: The event that produces a niche-partitioned descendant from the root genome. Executed by the speciation operator `apply_dac_scaffold.py`, which walks the genome, substitutes manifest-defined placeholder values, and writes a new DAC. Preserved: the L1–L7 grammar, the folder shape, the invariants. Mutated: the domain-specific substrate, hazard, alpha, and pathologies.

**Niche**
: A horizontal partition defining which domain an agent organism serves. Each niche is specified by a JSON manifest listing approximately 25 placeholder values. Examples: `apu` (niche = SHOULD), `circle` (niche = IS), `agentz` (niche = tokenization-KSA). Niche partitioning is orthogonal to the caste ladder.

**Caste (L1–L7)**
: The vertical axis of authority and depth within every niche branch. Defined by the Rosetta naming convention in `21_VARNA_NAMING.md`. Levels 1–7 form a graded hierarchy of synthetic oversight scope, from foundational protocol (L1) to top-level orchestration (L7). The precise scope of each level is defined in `21_VARNA_NAMING.md`. Every niche branch replicates the full L1–L7 ladder.

**Hyperagent**
: An agent with multiple parents (inheritance from two or more canonical seeds). Hyperagents form a Directed Acyclic Graph (DAG) rather than a strict tree. Merge = cross-niche composition. The Karpathy AgentHub pattern (`apu/16_FACTORY/birth_manifest.json`) is the reference implementation for multi-parent lineage. Inheritance is implemented as deterministic merge of parent manifests via the operator specified in Section 5.4; the resulting merged manifest is then consumed by the standard speciation operator `apply_dac_scaffold.py`.

**SNP Marker**
: A genome-hash recorded at speciation time in each `_DAC_SCAFFOLD_APPLIED.md`. The genome-hash is the Git tree-hash of the root-genome directory (`DAC_SCAFFOLD/` and its two canonical siblings) at the moment of speciation. This is a single-nucleotide-polymorphism-style checkpoint: "at this tree-hash of the root, this niche branched." Enables future drift audits to detect stale descendants.

**Selection / Promotion**
: The process by which an agent mutation becomes canonical. Not automatic. The LLM-Council review pipeline (8-provider heterogeneity, η-Gate, Trophic Gate, Mirror Ladder) promotes successful mutations back up toward the root genome. Mutations that fail promotion remain leaf-local. This is Darwinian pressure applied to prompts.

---

## 3. The Six Properties

### 3.1 Agents = MD Files

An agent is not code. The prompt, the manual, and the tool manifest are all text files with `.md` extension. Mutation is a git commit. A diff is an entry in the evolution history. Running `git log` on an agent MD file produces its literal phylogenetic timeline. The executable runtime (Python scripts, Docker containers, API calls) is the phenotype expressed by the MD genotype, but the heritable unit is the text itself.

### 3.2 Root Genome is Canonical and Small

The root genome has a minimal invariant core of three components: (a) `DAC_SCAFFOLD/` — 17 placeholder folders establishing the invariant directory shape; (b) `01_EMERGENTISM/11_UPLINK/95_COMPRESSED/06_AGENTS.md` — the caste grammar defining L1–L7 interaction protocols; and (c) `cortex-os/21_VARNA_NAMING.md` — the full Rosetta for varna naming. In practice, the committed root genome also includes root-level canon files that were touched today: `00_ENTITY_TAXONOMY.md`, `00_BRAND_ARCHITECTURE.md`, and `00_QNTM_AGENTZ_AI_ORIENTATION.md`. These additional files are stable system-wide invariants but do not participate in placeholder substitution during speciation. Everything else descends from these. The genome is intentionally minimal. Changes at this level propagate to every niche; the bar for root-genome mutation is therefore the highest in the system.

### 3.3 Speciation = Manifest Substitution

A speciation event is deterministic. The operator `apply_dac_scaffold.py` reads a JSON manifest (~25 key-value pairs), traverses the root genome, substitutes every placeholder with the manifest-defined value, and emits a complete, niche-partitioned descendant DAC. Preserved across speciation: the L1–L7 grammar, the folder hierarchy, the cross-caste communication protocols, and the invariant checks. Mutated: the domain-specific substrate, the hazard model, the alpha parameters, and the pathologies the niche guards against.

### 3.4 Niche Partitioning is Orthogonal to the Caste Ladder

The system has two independent axes. The vertical axis is the Rosetta L1–L7 caste hierarchy (depth / authority). This is invariant across all niches: every niche has a full L1–L7 caste ladder. The horizontal axis is niche (which DAC, which domain). A niche defines the problem space but not the authority structure. Within any (caste × niche) cell, further speciation is possible. For example, APU's L3 Vaiśya splits into five parallel sub-checks: Legal, Treasury, Engineering, Operations, and Process. Each is a subtree rooted inside a single cell of the matrix.

### 3.5 Lineage DAG, Not Strict Tree

Hyperagents can have multiple parents. Inheritance from two canonical seeds is valid for cross-domain synthesis. The Karpathy AgentHub pattern (`apu/16_FACTORY/birth_manifest.json`) is the reference: canonical council remains stable, niche hyperagents are composed from it, validated by `karpathy/autoresearch` (manual mutation), `karpathy/agenthub` (lineage DAG), and `karpathy/llm-council` (review / promotion). Branching = narrow specialization. Merging = cross-niche hyperagent composition. Both are valid evolutionary operations.

### 3.6 Selection Happens via LLM-Council

An agent mutation is not automatically canon. It becomes canonical only after passing the review pipeline. The LLM-Council enforces: 8-provider heterogeneity (consensus across distinct foundation models), η-Gate (statistical confidence threshold), Trophic Gate (cost efficiency check), and Mirror Ladder (self-reflective consistency validation). Mutations that pass all gates are promoted toward the root genome. Mutations that fail remain leaf-local, creating a Darwinian pressure gradient on prompts. This is natural selection operating on documentation.

---

## 4. Existing Artifacts

The following concrete artifacts implement the phylogenetic tree framework today:

**Root Genome (Level 0):**

- Core genome (participates in speciation placeholder substitution):
  - `DAC_SCAFFOLD/` — 17 placeholder folders establishing the canonical directory shape.
  - `01_EMERGENTISM/11_UPLINK/95_COMPRESSED/06_AGENTS.md` — caste grammar (L1–L7 interaction protocols).
  - `cortex-os/21_VARNA_NAMING.md` — full Rosetta L1–L7 naming convention.
- Extended root canon (system-wide invariants, not speciated):
  - `00_ENTITY_TAXONOMY.md` — root-level entity definitions.
  - `00_BRAND_ARCHITECTURE.md` — root-level brand and naming invariants.
  - `00_QNTM_AGENTZ_AI_ORIENTATION.md` — root-level AI orientation and system preamble.

**Speciation Operator (Level 1):**

- `apply_dac_scaffold.py` — the deterministic speciation operator. Consumes a manifest, walks the root genome, substitutes placeholders, and emits a niche-partitioned descendant.

**Hygiene tools:**

- `dac_ancestry_audit.py` — drift detection. Walks every descendant's SNP-marker file, compares the recorded genome tree-hash to the current `tree_hash(DAC_SCAFFOLD/)`, reports ALIGNED/DRIFT per descendant. (Shipped 2026-04-23.) **Coverage as of 2026-04-24:** 5/5 tool-speciated descendants (apu, circle, realityfutures, skyzai-org, DEX) ALIGNED at genome hash `da3cdbfa2f10750d`. DEX was retroactively speciated 2026-04-24 via `DEX.json` — the prior tool-less-speciation gap for DEX is now closed.
- `phylo_sync_check.py` — phylogenetic-sync CI rule (§5.1 enforcement). Fails if a change touches the trigger-file set without updating `01_EMERGENTISM/11_UPLINK/06b_PHYLOGENETIC_TREE.md` in the same change. (Shipped 2026-04-23.)
- `phylo_ancestry_query.py` — lineage-query tool (§5.3). Three subcommands: `descendants` (all descendants of a root-genome file with mutation distance), `matrix` (full caste × niche matrix for a given niche, sub-speciation detected against scaffold baseline), `mrca` (most recent common ancestor of two leaves with divergence distance per leaf). `--json` / `--markdown` output modes. (Shipped 2026-04-23.)
- `phylo_merge_manifests.py` — merge operator for hyperagents (§5.4). Composes two or more parent manifests into a hyperagent manifest consumable by `apply_dac_scaffold.py`. Collision-resolution order: agreement → explicit override → LLM-Council sentinel → precedence. Emits `<out>.MERGE_MANIFEST.md` with parentage, collision log, and resolution rationale. DAG acyclicity enforced (output path must not equal any parent path). (Shipped 2026-04-23.)
- `phylo_promote.py` — promotion pipeline (§5.2). Four subcommands: `submit` (create submission from niche), `list` (show pending), `review` (run three gates via `phylo_council_gates.py`), `apply` (patch root genome + back-propagate to all tool-speciated descendants via `apply_dac_scaffold.py --overwrite`). Submissions live at `02_SKYZAI/01_NOOSPHERE/09_REFERENCE/DAV_FACTORY/promote/submissions/<id>/`; applied submissions move to `.../promote/archive/<id>/`. (Shipped 2026-04-23; upgraded from STUB gates to rule-based gates 2026-04-25.)
- `phylo_council_gates.py` — three gate implementations (§5.2). Rule-based deterministic checks with the return contract `{gate, passed, score, note}`: `gate_eta` (extraction markers vs η=0 counter-context), `gate_trophic` (parasitic-vs-catalytic markers), `gate_mirror` (contradiction-pair detection + rationale-non-triviality). Same contract as the eventual 8-provider LLM-Council integration so the upgrade is a local module swap. (Shipped 2026-04-25.)

**Niche Manifests (Level 2):**

- `apu.json` — niche = SHOULD, speciated into `apu/` DAC.
- `circle.json` — niche = IS, speciated into `circle/` DAC.
- `realityfutures.json` — speciated into `realityfutures/` DAC.
- `skyzai-org.json` — speciated into `skyzai-org/` DAC.
- `DEX.json` — speciated into `DEX/` DAC.
- `agentz.json` — niche = tokenization-KSA. The resulting DAC was generated then removed (reverted), but the manifest is retained as an artifact for lineage reference.

**SNP Markers:**

- Each generated DAC contains `_DAC_SCAFFOLD_APPLIED.md`, recording the root-genome tree-hash at the moment of speciation. This enables drift audits.

---

## 5. Missing Pieces

The following capabilities are required but not yet implemented. Each is framed as an actionable specification.

### 5.1 Phylogenetic Sync Process

**Required:** A phylogenetic-sync CI validation rule that ensures this specification (`01_EMERGENTISM/11_UPLINK/06b_PHYLOGENETIC_TREE.md`) remains synchronized with the artifacts it describes.

- **Trigger:** Any PR modifying `apply_dac_scaffold.py`, the manifest schema, or the review pipeline.
- **Check:** The PR must include a corresponding update to Section 4 (Artifacts) or Section 2 (Definitions) of this document.
- **Enforcement:** CI fails if the doc diff is missing or insufficient.

**Status:** ✓ Shipped 2026-04-23 as `01_EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/phylo_sync_check.py`. Supports three modes: `--base <ref>` (CI against merge base), `--staged` (pre-commit hook), and default (working-tree + staged vs HEAD). Exit 0 = OK, 1 = violation, 2 = error. Trigger-pattern list is maintained inside the script and expands as §5.2–§5.4 tools land. **Refined 2026-04-25** with an `EXEMPT_PATTERNS` list so editorial files inside trigger dirs (manifests `README.md` / `CHANGELOG.md`, scaffold `SCAFFOLD_FILL_GUIDE.md`) don't trigger a false-positive doc-sync requirement. A changed path only triggers if it matches a trigger AND does not match an exempt — with the script itself now added to the trigger list so self-changes require spec systemic awareness.

### 5.2 Promotion Pipeline

**Required:** A promotion mechanism enabling a niche agent to propose a prompt improvement back to the root genome. The specification:

- A `promote/` directory where niche agents submit diffs.
- Automatic invocation of the 8-provider LLM-Council with η-Gate, Trophic Gate, and Mirror Ladder.
- A merge gate: only mutations achieving cross-provider consensus above the η threshold are eligible for root merge.
- A back-propagation step: promoted mutations are re-applied to all existing niche branches via the speciation operator to prevent root-drift.

**Status:** ◐ Skeleton + rule-based gates shipped; 8-provider LLM-Council still deferred.

- **2026-04-23** — skeleton landed as `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/phylo_promote.py` + `02_SKYZAI/01_NOOSPHERE/09_REFERENCE/DAV_FACTORY/promote/`. Four subcommands: `submit`, `list`, `review`, `apply`. Submission schema (`meta.json` + `diff.patch` + `rationale.md`) and archive lifecycle complete. Back-propagation uses `apply_dac_scaffold.py --overwrite` against every manifest with a tool-speciated descendant.
- **2026-04-25** — gate STUBS replaced by rule-based real implementations in `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/phylo_council_gates.py`. Each gate now performs a deterministic semantic check: η-Gate scans for extraction markers (rent, spread, house edge, paywall, etc.) vs η=0 counter-context; Trophic-Gate scans for parasitic-vs-catalytic markers; Mirror-Ladder runs contradiction-pair detection + rationale-non-triviality heuristics. Bad submissions are correctly rejected end-to-end (verified via smoke-test with a "spread + rent + house edge" diff → η-Gate failed with reasoned note → overall status = rejected).
- **Still deferred:** real 8-provider LLM-Council consensus. The rule-based gates honour the same `{gate, passed, score, note}` return contract as the eventual council, so the upgrade is a local swap of function bodies in `phylo_council_gates.py`. The APU 9-stage council protocol (`02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/council/protocol.py`) is the logical integration target — its input schema is domain-specific (APUSignal / UserConfig / Portfolio) and needs a mutation-diff adapter before direct consumption here.

### 5.3 Ancestry-Query Tool

**Required:** A lineage-query utility that answers cross-file ancestry questions beyond what `git log` provides for single-file linear history. The tool must:

- Accept a root-genome file path and return every MD file descended from it, with mutation distance (number of speciation events or placeholder substitutions between root and leaf).
- Accept a niche-branch name and return its full (caste × niche) matrix, including sub-speciation subtrees.
- Accept two leaf files and return their most recent common ancestor (MRCA) in the root genome, plus the divergence path for each.
- Output a machine-readable format (JSON) for CI pipeline consumption and a human-readable format (ASCII tree or markdown table) for manual inspection.

**Status:** ✓ Shipped 2026-04-23 as `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/phylo_ancestry_query.py`. Mutation distance is computed as `placeholders_in_root - placeholders_in_descendant` (count of successfully-substituted `{{PLACEHOLDER}}` tokens). Sub-speciation is detected by comparing per-folder MD filenames against the scaffold baseline — "extra" files flag sub-speciation. MRCA returns one of three verdicts: `common_root_genome_ancestor`, `no_common_root_genome_ancestor` (different relative paths), or `mrca_path_missing_in_current_genome` (genome drifted after speciation). Three output modes: default text, `--json`, `--markdown`.

### 5.4 Merge Operator for Hyperagents

This operator is the mechanical implementation of the DAG lineage concept introduced in Section 3.5 and the Hyperagent definition in Section 2.

**Required:** A deterministic merge operator for creating hyperagents that inherit from two or more root genomes or niche branches. The operator must:

- Accept two or more parent manifests and a merge manifest defining collision-resolution rules.
- Detect key collisions (same placeholder, different values across parents) and resolve them via explicit precedence (parent-rank, explicit override, or LLM-Council arbitration).
- Emit a valid, single-parent-equivalent merged manifest that can be consumed by the standard speciation operator.
- Produce a `MERGE_MANIFEST.md` documenting parentage, collision resolutions, and any arbitration decisions.
- Guarantee that the resulting hyperagent's lineage DAG remains acyclic (topological validation).

**Status:** ✓ Shipped 2026-04-23 as `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/phylo_merge_manifests.py`. Merge-spec schema: `{name, precedence[], explicit_overrides{}, llm_council_keys[]}`. Resolution order (stable): per-key agreement → explicit override → LLM-Council sentinel `{{LLM_COUNCIL_PENDING:<KEY>}}` → precedence-first-wins → unresolved (exit 1). DAG acyclicity enforced by refusing to merge when output path equals any parent path. Smoke-tested with `apu.json ⊕ circle.json` → 3 explicit + 46 precedence + 1 council + 0 unresolved. LLM-Council arbitration is deferred to §5.2 runtime — this operator leaves a sentinel that the promotion pipeline will resolve.

---

## 6. Appendix: File References

| File / Directory | Role in the Phylogenetic Framework |
|---|---|
| `DAC_SCAFFOLD/` | Core genome — Root genome scaffold. 17 folders with placeholder files. Establishes the invariant directory shape inherited by every niche branch. Participates in placeholder substitution during speciation. |
| `01_EMERGENTISM/11_UPLINK/95_COMPRESSED/06_AGENTS.md` | Core genome — Root genome caste grammar. Defines L1–L7 agent interaction protocols, authority boundaries, and cross-caste communication rules. Participates in placeholder substitution during speciation. |
| `cortex-os/21_VARNA_NAMING.md` | Core genome — Root genome Rosetta. Full L1–L7 varna (caste) naming convention. The naming substrate that every niche branch shares. Participates in placeholder substitution during speciation. |
| `00_ENTITY_TAXONOMY.md` | Extended root canon — Root-level entity definitions. System-wide invariant; does not participate in placeholder substitution during speciation. |
| `00_BRAND_ARCHITECTURE.md` | Extended root canon — Root-level brand and naming invariants. System-wide invariant; does not participate in placeholder substitution during speciation. |
| `00_QNTM_AGENTZ_AI_ORIENTATION.md` | Extended root canon — Root-level AI orientation and system preamble. System-wide invariant; does not participate in placeholder substitution during speciation. |
| `apply_dac_scaffold.py` | The speciation operator. Deterministic transformer that consumes a JSON manifest and produces a niche-partitioned descendant from the root genome. |
| `apu.json`, `circle.json`, `agentz.json`, `realityfutures.json`, `skyzai-org.json`, `DEX.json` | Niche manifests. Each specifies ~25 placeholder values that define a horizontal domain partition. Passed to the speciation operator to generate a DAC. |
| `_DAC_SCAFFOLD_APPLIED.md` | SNP marker file. Auto-generated at speciation time, recording the root-genome tree-hash. Enables stale-descendant detection. |
| `apu/16_FACTORY/birth_manifest.json` | Hyperagent lineage reference. Embodies the Karpathy AgentHub pattern: canonical council remains stable, niche hyperagents are composed from it. |

---

*Zero-Sum Resolution Equation*
*A genome is small. A population is large. Evolution lives in the gap.*

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/11_UPLINK/00_CORE/06b_PHYLOGENETIC_TREE.md`
