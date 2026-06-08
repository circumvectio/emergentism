---
rosetta:
  primary_column: "Yoga"
  register: "[I]"
  canonical_phrase: "157 — Rosetta Annotation Strategy: Apply the Rosetta to Every Doc"
---

# 157 — Rosetta Annotation Strategy: Apply the Rosetta to Every Doc

**Evidence tier:** [I] methodology; [S] Rosetta structure cited from `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/`; [C] batch plan pending sovereign K2
**Date:** 2026-04-24
**Lane:** Charioteer spec; warrior/sovereign executes annotation passes
**Status:** Strategy active; Tier A applied (`32e2c320b` + META close-out); Tier B root/00_CORE applied via packet 161 manifest; Tier C remains gated
**Complements:** packet 156 (Phase 2c filesystem reorg)
**Prerequisite packets:** 143, 144, 145, 146–155 lineage

---

## 0. Axiomatic guard

The Rosetta is a reading lens, not a cage. A doc without Rosetta annotation that still teaches well is fine. A doc with perfect frontmatter that nobody reads is annotation-gatekeeping. This strategy is the discipline that *helps readers find* where a doc sits in the larger field — not a purity audit.

`Zero-Sum Resolution Equation`

---

## 1. What "Rosetta annotation" means

The Rosetta Stone (canonical at `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/`) is a 7-row × N-column matrix:
- **Rows** = L-levels L1…L7 (Caṇḍāla → Systems Architect / Objective Function → Institutional Narrative)
- **Columns** = domains (Three-Stage Process, Psychology, Philosophy, Yoga, Chakra, Mythology, Neuroscience, Game Theory, Civilizational Stage, Liberal Arts, PIE roots, etc.)

Each document in the corpus has — implicitly or explicitly — a **Rosetta position**: its primary L-level (row) + its primary domain (column).

**Rosetta annotation** = making that position explicit in frontmatter so readers can:
1. Navigate by L-level (find all L3 Auditing content)
2. Navigate by domain column (find all "Neuroscience" content across L-levels)
3. Cross-read horizontally (what does L4 look like in Yoga vs. in Game Theory?)
4. Cross-read vertically (how does Data Science move from L1 to L7?)

---

## 2. Frontmatter spec

Every doc gets an optional `rosetta:` block in YAML frontmatter:

```yaml
---
name: Example document title
rosetta:
  primary_level: L4              # one of L1..L7
  primary_column: Value Alignment       # canonical column name
  secondary:                     # 0..n cross-refs
    - level: L3
      column: Auditing
      role: "falsification entry"
    - level: L6
      column: Core State
      role: "axiomatic counterweight"
  operator: "Arjuna ⚔"           # optional — which God/Executive governs
  tier: "God"                    # optional — Executive / God / Witness / Demon
  regime: "Kṣatriya"             # optional — Rosetta caste
  register: "[S]"                # evidence tier: E/S/I/C
  canonical_phrase: "Justice signs"  # optional — L-folder anchor phrase
---
```

**Minimum required fields:** `primary_level`, `primary_column`, `register`.
**Recommended:** `secondary` + `canonical_phrase`.
**Optional:** `operator`, `tier`, `regime`.

---

## 3. Canonical column names

From packet 06_AGENTS + ROSETTA_STONE authority:

| Column | Short | Example content |
|---|---|---|
| Three-Stage Process (Grammar/Logic/Rhetoric → Four-Stage Analytical Model) | C-T | First 3 L-levels trivium; L4+ quadrivium |
| Psychology (Piaget/Kohlberg/Maslow/virtue/shadow) | C-Ψ | Stage + virtue + shadow per caste |
| Philosophy (discipline/question/data science/exemplars) | C-Φ | Objective Function / Data Science / etc. |
| Political regime (Plato's sequence) | C-Π | Tyranny → Democracy → Oligarchy → Timocracy → Aristocracy → Anarchy → Theocracy |
| Yoga (path + gītā chapter) | C-Σ | Tantra / Bhakti / Jñāna / Karma / Rāja / Sannyāsa / Samādhi |
| Chakra (element + alchemy stage) | C-Ch | Mūlādhāra → Sahasrāra |
| Mythology (Greek/Norse/Sumerian/Tarot/Jungian/animal) | C-Μ | Per caste |
| Neuroscience (brain region + hemisphere + brainwave + mode) | C-Ν | Brainstem/limbic/cortex/DMN per caste |
| Computation (algorithm + process) | C-Κ | Immune / RL / Generative / Optimizer / Homeostat / Compression / Universal |
| Game theory (strategy + cooperation + Nash) | C-Γ | Always defect → infinite game |
| Civilisational stage (culture + tech + environment) | C-Χ | Survival → Closure |
| Operator pathology season + DSM | C-Π+ | Immune/Truth/Enable/Defence/Spring/Autumn/Summer |
| Asura return (inversion) | C-Α | Kali enthroned → Asura-Trimūrti |
| Liberal art (Three-Stage Process/Four-Stage Analytical Model + TPN/DMN) | C-Λ | Grammar→Astronomy across L1..L7 |
| PIE roots (h₂r̥tó / dyeu / serpent) | C-PIE | Chaos → Brahman |

**Rule:** Use canonical column names in `primary_column` field. Free-text descriptions go in `role` sub-field.

---

## 4. Batch plan — annotate what, in what order

Realistic scope: ~2,000–3,000 docs across the repo. Not a single-pass project. Three-tier batch plan:

### 4.1 Tier A — Framework / Foundation docs (high leverage, narrow scope)

Target: `01_EMERGENTISM/` — after Phase 2c, ~85 files distributed across L-folders.

Annotation here is highest-leverage because:
- These docs are the most-read by future agents
- They already have L-folder homes (post-Phase-2c)
- Annotation converts implicit L-level into explicit frontmatter

Estimated effort: 2–4 hours warrior-lane (read each doc, add frontmatter).

### 4.2 Tier B — Uplink routing docs (`01_EMERGENTISM/11_UPLINK/`)

Target: `01_EMERGENTISM/11_UPLINK/*.md` — the ~100+ uplink docs that AI agents ingest first.

Annotation here sharpens agent-food quality: routing docs self-declare their L-level + domain.

Estimated effort: 4–8 hours warrior-lane.

### 4.3 Tier C — CANON + organism docs (`02_SKYZAI/01_NOOSPHERE/`)

Target: `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/` — ~1,950 CANON files; plus organ docs.

This is the largest batch. Recommend: annotation via automated draft pass (LLM reads each file, proposes Rosetta frontmatter, warrior reviews).

Estimated effort: 20–40 hours warrior-lane, or ~8 hours with LLM-assisted pre-draft + warrior review.

### 4.4 Tier D — Everything else

Target: `02_SKYZAI/01_NOOSPHERE/09_PWAs/`, `01_EMERGENTISM/09_TOOLS/`, `02_SKYZAI/01_NOOSPHERE/00_INTAKE/`, etc.

Lower priority. Annotate as content touches them; no mass-annotation pass.

---

## 5. Execution pattern — per-doc annotation

For each doc:

**Step 1 — Read.** Understand the doc's core claim / question / scope.

**Step 2 — Identify primary L-level.**
- L1 Objective Function → future-vector / direction / F5 / teleos
- L2 Data Science → pattern / disclosure / induction / beauty
- L3 Auditing → procedure / inference / testability / truth
- L4 Value Alignment → value / choice under uncertainty / sign / justice
- L5 System Architecture → positive model / system / testimony / received structure
- L6 Core State → axiomatic / via negativa / Ground / pruning
- L7 Institutional Narrative → symbol / rite / institution / pratibha

**Step 3 — Identify primary column.**
What lens does the doc use? Philosophy? Neuroscience? Yoga? Game theory? Most often obvious from title + first paragraph.

**Step 4 — Identify secondaries.**
Does the doc span multiple L-levels or columns? Add as `secondary` entries.

**Step 5 — Check register.**
What evidence tier? [S] empirical, [S] structural, [I] interpretive, [C] conjectural. Use existing register if present.

**Step 6 — Write frontmatter.**
Add block per §2 template.

**Step 7 — Preserve existing frontmatter.**
If doc has existing frontmatter (name, description, etc.), *add* `rosetta:` block — do not overwrite.

---

## 6. Worked example

**Input file:** `05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md`

**Analysis:**
- Primary L-level: L5 (positive structural model)
- Primary column: Philosophy (System Architecture discipline)
- Secondary: L3 Auditing (the block is an audit surface for formula tracking)
- Operator: Brahmā ○ (Executive — boundary creation / systematic building)
- Tier: Executive
- Regime: Brāhmaṇa
- Register: [S]
- Canonical phrase: "Emergentism models"

**Output frontmatter:**

```yaml
---
name: Canonical Formula Block
description: Compression of all structural formulas governing the framework
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Auditing
      role: "audit surface for formula tracking"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "Emergentism models"
---
```

---

## 7. Automation option — LLM-assisted draft

For Tier C (CANON, ~1,950 files), recommend automated draft pass:

**Tool:** short Python script or LLM workflow that for each file:
1. Reads first 2,000 characters
2. Emits proposed `rosetta:` block based on §5 heuristic
3. Warrior reviews + corrects before merge

**Prompt template for the LLM pass:**

> Read this document. Based on its content, propose a Rosetta annotation in YAML frontmatter format per packet 157 §2 spec. Output only the `rosetta:` YAML block. Use canonical column names from §3. Identify primary L-level (L1-L7), primary column, optional secondary cross-refs, evidence tier [E/S/I/C], and (if clear) operator + tier + regime + canonical phrase. If uncertain about any field, omit it rather than guess.

**Warrior review:** batch ~50 files at a time; correct mis-classifications; commit.

---

## 8. Acceptance criteria per tier

### Tier A (Framework)

☐ Every file in `01_EMERGENTISM/0X_L-FOLDER/*.md` has `rosetta:` frontmatter
☐ Primary L-level matches the containing L-folder (internal consistency)
☐ All 7 L-folders have at least one file with each column represented (or explicit note of absence)
☐ Spot-check review: 10 random files show correct classification

### Tier B (Uplink)

☐ All `01_EMERGENTISM/11_UPLINK/*.md` have `rosetta:` frontmatter
☐ Spot-check review: routing quality maintained

### Tier C (CANON)

☐ LLM-draft pass completed on ~1,950 files
☐ Warrior review completed on ≥ 500 files before commit
☐ Automated consistency check: no file claims `primary_level: L3` in `05_COSMOLOGY/` branch

### Tier D (Everything else)

☐ No formal gate. Annotate as content touches.

---

## 9. Sovereign K2 decision form

**OQ-Rosetta-1 — Annotation priority order.**
☐ R1a — Tier A only (Framework); defer B–D (charioteer recommended for first pass)
☐ R1b — Tier A + B (Framework + Uplink); defer C–D
☐ R1c — All four tiers (ambitious; multi-week warrior-lane project)

**OQ-Rosetta-2 — Automation scope.**
☐ R2a — Manual annotation throughout (warrior reads + writes each)
☐ R2b — LLM-assisted draft for Tier C only; manual for A/B (charioteer recommended)
☐ R2c — LLM-assisted draft for B + C + D; manual only for A

**OQ-Rosetta-3 — Cross-reference tool.**
☐ R3a — No tool; annotations live in frontmatter only
☐ R3b — Build `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/rosetta_index.py` that scans repo + generates L-level + column indexes (charioteer recommended; post-Tier-A)
☐ R3c — Defer tool until all Tiers complete

---

## 10. What this packet does NOT do

- Does NOT execute annotation (charioteer lane restriction; warrior runs the passes)
- Does NOT change CANON content
- Does NOT alter Rosetta Stone structure itself (that's a Lane B constitutional question if raised)
- Does NOT touch file locations (Phase 2c packet 156 covers that)

---

## 11. Dependencies and sequencing

Phase 2c (packet 156) should complete **before** Tier A Rosetta annotation. Reasons:
- Files are at their L-folder destinations, so filesystem layer and annotation layer agree
- L-folder README claims are stable
- No risk of re-annotating files that subsequently move

Track A engineering sprint (packet 154) is independent of Rosetta annotation and can proceed in parallel.

Mesh / cluster / EBM scaffolds (packets 150b, 151, 152, 153) are independent of Rosetta annotation.

---

## 12. References

**Rosetta authority:**
- `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/README.md`
- `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md`

**Agent grammar:**
- `01_EMERGENTISM/11_UPLINK/06_AGENTS.md` — VMOSK-A + Rosetta castes + operators

**Session context:**
- 146–156 (current reorg + reconciliation sequence)
- 143 Sevenfold Foundation Root
- 144 D-Scaffold / L-Ladder Bridge
- 145 As Above So Below

**External:**
- Project CLAUDE.md — "Rosetta horizontals are canonical in `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/`"

---

*Rosetta annotation strategy. Charioteer writes the method; warrior/sovereign executes the passes across tiers.*

`Zero-Sum Resolution Equation`
