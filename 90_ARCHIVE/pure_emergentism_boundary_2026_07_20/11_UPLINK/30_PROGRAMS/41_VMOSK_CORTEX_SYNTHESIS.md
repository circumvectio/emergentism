---
rosetta:
  primary_column: "Neuroscience"
  register: "[I]"
  canonical_phrase: "VMOSK × Cortex Synthesis"
---

# VMOSK × Cortex Synthesis

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*


> **VMOSK is the replicator stack. Cortex is the memory/witness nervous layer that keeps it alive. Without Cortex, VMOSK is a filing cabinet. Without VMOSK, Cortex is raw memory without purpose.**

> **Boundary note (2026-04-24):** this document describes VMOSK-A and Cortex
> in synthesis. It does not make Cortex sovereign, self-correcting by itself, or
> the whole immune system. Cortex stores, searches, witnesses, recalls, lints,
> and raises review obligations. Human / council authority resolves. For the
> current boundary repair, see
> `130_BOUNDARY_AUDIT_ORGANISM_MODEL_2026_04_24.md`.

Date: 2026-04-16  
Status: Planning Doctrine  
Canonical path: `41_VMOSK_CORTEX_SYNTHESIS.md`

---

## 0. The Core Synergy

VMOSK-A defines *what the organism is at every timescale*:
- **V**ision (decades)
- **M**ission (years)
- **O**bjectives (quarters)
- **S**trategies (continuous)
- **K**PIs (monthly)
- **A**gents (per-cycle)

Cortex is the *memory, search, compilation, and witness layer* (L∞) that:
- stores every VMOSK artifact
- detects when layers drift or contradict
- triggers review cadences
- compiles organism-wide coherence
- makes VMOSK queryable across all fractal scales

**The synthesis:** VMOSK provides the schema. Cortex provides the memory and
witness runtime that keeps the schema queryable, reviewable, and contradiction
aware. Cortex surfaces drift; it does not decide the repair outcome.

---

## 1. The Six Mappings

### Mapping 1: Storage

Every VMOSK layer lives in Cortex as a typed document:

| VMOSK Layer | Cortex Document Type | Storage Path Convention |
|-------------|----------------------|-------------------------|
| V | Constitutional amendment / Canon | `canon/vision/<epoch>/` |
| M | Mission activation record | `missions/<organ_or_dac>/<year>/` |
| O | Quarterly objective pack | `objectives/<organ_or_dac>/<year>-Q<n>/` |
| S | Strategy note / tactical decision log | `strategies/<organ_or_dac>/active/` |
| K | KPI report / P-score statement | `metrics/<organ_or_dac>/<yyyy-mm>/` |
| A | Agent assignment / execution trace | `agents/<organ_or_dac>/<cycle_id>/` |

Cortex enforces:
- **Lineage linking:** Every M must link to its parent V. Every O must link to its parent M.
- **Signature validation:** Each layer is signed by the key appropriate to its stratum (V=Foundation key, M=Organ key, O=Project key, etc.)
- **Version immutability:** Once a V or M is signed and stored, it is not overwritten. Amendments create new epochs.

### Mapping 2: Query

Cortex turns VMOSK into a live query surface:

| Query | Cortex Function |
|-------|-----------------|
| "What is the active Mission for APU?" | Search `missions/apu/` for latest signed M record |
| "Which Objectives depend on Vision 2026-Q1?" | Backlink search from V through M to O |
| "Has any Strategy violated its parent Objective?" | Contradiction detection across linked layers |
| "What is the P-score trend for TheCircle?" | Aggregate `metrics/thecircle/` over time |
| "Which Agents were assigned to Objective O-14?" | Forward link from O to A records |

### Mapping 3: Review Triggering

Cortex watches time and state to trigger VMOSK governance cadences:

| Cadence | Cortex Trigger | Action |
|---------|----------------|--------|
| V review (90-day amendment window) | Calendar alert + Foundation key notification | Publish proposed amendment, collect node-level responses |
| M activation / deactivation | Annual calendar trigger + P-score threshold | Organ keys sign new M, archive old M |
| O quarterly planning | Calendar trigger + mission-drift detector | Project keys draft O pack, link to active M |
| S continuous update | Real-time event stream (new partnership, market shift, anomaly) | Strategy notes append automatically, flagged for human review if they contradict active O |
| K monthly report | Calendar trigger + receipt aggregation | Reporting keys sign KPI publication |
| A per-cycle assignment | Execution cycle completion + objective gap analysis | Agent keys sign next-cycle assignments |

**Critical rule:** Cortex does not *decide* the review outcome. It *surfaces the need for review* and *compiles the evidence*.

### Mapping 4: Contradiction Detection

Cortex runs a continuous linter across VMOSK layers:

| Contradiction Type | Detection Logic | Escalation |
|--------------------|-----------------|------------|
| O contradicts M | Keyword/topic mismatch; objective targets a mission that is inactive or archived | Yellow alert to project keys |
| K contradicts O | KPI shows progress in a direction opposite to stated objective | Orange alert to reporting + project keys |
| S contradicts O | Strategy document pursues a market/partnership not mentioned in active objectives | Yellow alert to strategy keys |
| A contradicts S | Agent assignment executes a tactic not covered by active strategy | Yellow alert to agent operator |
| V amendment without M update | New V epoch exists, but no M has been re-linked to it | Red alert to organ keys |

These are **surface-and-escalate**, not auto-correct. The human (or DAC council) resolves contradictions. Cortex ensures they are not invisible.

**Interpretation:** this is continuous recursive disambiguation at the governance-memory layer.
Cortex does not merely find contradictions.
It forces the organism to ask:

- what exactly is in conflict?
- which layer owns the correction?
- whether the conflict is lexical, authority, temporal, runtime, or metric drift
- what downstream surfaces must be refreshed once the owner is repaired

### Mapping 5: Fractal Scaling

VMOSK operates at organism, organ, DAC, and agent levels. Cortex supports this by namespacing:

```
cortex://vmosk/organism/V/2026/
cortex://vmosk/organism/M/2026/
cortex://vmosk/thecircle/V/2026/
cortex://vmosk/thecircle/M/2026/
cortex://vmosk/dac-alpha/V/2026/
cortex://vmosk/dac-alpha/M/2026/
cortex://vmosk/agent-117/V/...   # agent-level micro-vision
```

This means:
- A query for "current Mission" can be scoped to organism, organ, or DAC
- A contradiction linter can run at any fractal level
- A rollup view can show how all organ Missions align (or diverge) from organism Mission

### Mapping 6: Witness and P-Score

Cortex is the witness layer for VMOSK health. It computes:

- **Φ (coherence):** How well aligned are the VMOSK layers? Contradictions reduce Φ.
- **V (viability):** Are the layers actually being reviewed and updated on cadence? Stale layers reduce V.
- **P_node = Φ × V:** The organism's or organ's live position.

Cortex publishes these as signed `metrics/` documents, making P-score a first-class K-layer artifact.

---

## 2. The Runtime Sequence

```
1. EVENT occurs in the organism
   (payment, partnership, anomaly, completion, failure)

2. CORTEX ingests the event as a receipt / trace / signal

3. CORTEX updates relevant VMOSK layers:
   - S (strategy note if market shift)
   - K (KPI if metric affected)
   - A (agent trace if execution event)

4. CORTEX runs contradiction linter:
   - Does the new S contradict active O?
   - Does the updated K contradict M?
   - What kind of ambiguity has appeared?
   - Which owning layer must be corrected first?

5. IF contradiction detected:
   - Alert the relevant keyholders
   - Compile evidence packet
   - Pause dependent agent assignments (Mode 3 suspension)

6. IF review cadence triggered:
   - Surface the review need
   - Pull parent-layer links
   - Draft delta report (what changed since last review)

7. HUMAN / DAC COUNCIL resolves:
   - Amends layer
   - Overrides alert with documented reasoning
   - Or lets the suspension stand until remediation

8. CORTEX receipts the resolution:
   - New signed layer stored
   - P-score recomputed
   - Graph capital updated if DAC-level

This means the VMOSK × Cortex runtime is not only memory plus contradiction detection.
It is the replicator stack's concrete engine of continuous recursive disambiguation.
```

---

## 3. The Cortex-VMOSK Query Language (Planned)

A conceptual query syntax for how agents and operators interact with the synthesis:

```yaml
# Query the active mission for an organ
GET vmosk://thecircle/M/active

# Find contradictions between O and M for a DAC
LINT vmosk://dac-alpha/O/* vs vmosk://dac-alpha/M/active

# Roll up all organ strategies aligned to organism objective O-3
ROLLUP vmosk://*/S/active WHERE parent_objective = "O-3"

# Trigger review for stale K records
REVIEW vmosk://*/K WHERE age > 35d

# Compute P-score for an organ
SCORE vmosk://thecircle/*
```

This is not a database query language. It is a **governance query language** — designed for councils, agents, and operators to ask "where are we?" and "what is misaligned?"

---

## 4. Anti-Patterns

| Anti-pattern | Damage | Defense |
|--------------|--------|---------|
| **Cortex auto-corrects VMOSK layers** | Substrate overrides cognition; bureaucracy by algorithm | Cortex surfaces and alerts. Humans amend. |
| **VMOSK layers become write-only documentation** | Cortex stores them but no one queries them | Review cadences are triggered and receipted. Stale layers reduce P-score. |
| **Fractal levels collapse into one global VMOSK** | Organ/DAC agency is erased | Namespacing enforces fractal separation. Organism rollups are explicit, not default. |
| **P-score gaming** | Layers are updated frequently but emptily to boost V | Φ checks for actual content delta and cross-layer alignment. Empty updates reduce Φ. |
| **Contradiction fatigue** | Too many alerts → operators ignore them | Severity tiers (yellow/orange/red) + Sādhu / L6 axiomatic triage. |

---

## 5. Canonical Compression

> **VMOSK is the organism's replicator DNA. Cortex is the ribosome that reads it, the memory/witness layer that detects drift, and the nervous system that signals when repair is needed.**

Or more practically:

> **VMOSK says what should be true at every timescale. Cortex watches what is actually happening, stores the proof, and raises the alarm when the two diverge.**

And in governance terms:

> **VMOSK names the layers. Cortex keeps recursively disambiguating them as reality moves.**

---

## 6. Cross-References

- `A6-vmosk-a.md` — VMOSK-A replicator stack definition
- `00_BRIEF.md` (Cortex) — Cortex capabilities and current state
- `00_ACTIVATION_RUNBOOK.md` — Witness layer and VMOSK protocol activation plan
- `39_COGNITION_SUBSTRATE_INTERFACE.md` — how reasoning and substrate interact
- `40_EMPTY_THRONE_GOVERNANCE.md` — centerless governance model for VMOSK amendments
- `38_PHI_METER.md` — P-score and coherence tracking
- `130_BOUNDARY_AUDIT_ORGANISM_MODEL_2026_04_24.md` — boundary repair for
  VMOSK-A, Cortex, AIA, SPECTRE, P-scores, and runtime truth

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning phase — do not modify Cortex storage schemas or VMOSK document formats yet.
2. **Your Next Action:** Design a prototype query that a DAC council could run to detect misalignment between its current O and M layers.
3. **Expected Output:** A query specification, a sample result format, and a contradiction-linter rule that would trigger it.
4. **Success Criteria:** A council member can read your design and understand exactly what Cortex would surface and what they must decide.
5. **Canonical Path:** `41_VMOSK_CORTEX_SYNTHESIS.md` (this file).

---

> *The DNA does not govern. The cell does not remember. They need each other.*  
> *eta = 0. K2 always.*
