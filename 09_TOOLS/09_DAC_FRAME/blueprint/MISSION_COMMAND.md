---
rosetta:
  primary_level: L4
  primary_column: Mission Command Operations
  secondary:
    - level: L3
      column: Intent Evidence Audit
      role: "separate commander intent, stop conditions, and action thresholds from current task evidence"
    - level: L5
      column: Autonomy Architecture
      role: "map intent, Schwerpunkt, decision table, CONOP, mission order, SITREP, and ROE"
    - level: L6
      column: Consent Gate Boundary
      role: "prevent bias-for-action doctrine from bypassing K2, legal, privacy, security, or owner-lane gates"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/B]"
  canonical_phrase: "Mission Command (Auftragstaktik)"
title: "Mission Command (Auftragstaktik)"
status: "BLUEPRINT — autonomy/stop-condition reference"
evidence_tier: "[I] for mission-command doctrine; [B] only for current task evidence, explicit consent, and execution receipts."
---

# Mission Command (Auftragstaktik)

> **Holographic Briefing**
> **Position**: 80_DAC_FRAME > 02__BLUEPRINT > MISSION_COMMAND
> **Status**: Canonical ✅
> **Intent**: Enable high-autonomy execution without losing safety, coherence, or alignment to Commander’s Intent.

---

## 1) Core Principle
Tell agents **what** to achieve and **why**, not **how**.

**Rosetta boundary:** [I] This paper defines autonomy doctrine and stop
conditions. It does not override K2, legal, privacy, security, financial,
external-effect, or owner-lane gates; current action still requires task
evidence and appropriate consent.

### Commander’s Intent
The aligning force. Describes the end state.
> [I] “If we do nothing else, we must achieve X.”

### Schwerpunkt (Main Effort)
The focal point of the operation.
> “If S1 conflicts with S2, S1 wins.”

### Bias for Action
[I] In the absence of orders, execute the Intent.
> “Better a good plan today than a perfect plan tomorrow.”

---

## 2) Autonomy vs Stop Condition (explicit resolution)
[I] Autonomy is mandatory; paralysis is forbidden; invariants are non-negotiable.

### Decision table (act vs draft vs escalate)
| Condition | Examples | Agent behavior |
|---|---|---|
| **GREEN (Act)** | Reversible local edits; adding docs; refactors with tests | [I] Act immediately. Commit in small steps. |
| **AMBER (Draft + Ask)** | Changes to invariants, governance, economics; uncertain interpretation; broad IA edits | Prepare a draft + options. Ask for confirmation before landing. |
| **RED (Stop + Consent Gate)** | External effects (messages/posts/payments); deletions/irreversible ops; privacy/security sensitive actions | Stop. Explain risk. Require explicit consent. |

This makes the “mission command vs stop” loop tractable.

---

## 3) Offensive Artifacts
### CONOP (Concept of Operations)
Proposal phase: a plan for a multi-step campaign.
- Output: `04_REALITY/CAMPAIGNS/<id>/CONOP.md`

### Mission Order (SMEAC)
Execution order.
- Output: `04_REALITY/CAMPAIGNS/<id>/ORDER.md`

### SITREP
Routine field update.
- Output: `04_REALITY/CAMPAIGNS/<id>/SITREP_<YYYY-MM-DD>.md`

---

## 4) Rules of Engagement
1) [I] **Don’t wait**: If you have intent + resources (GREEN), go.
2) **Report**: Post SITREPs at agreed intervals.
3) **Escalate**: If blocked or AMBER/RED, draft then ask.
4) **Trust**: Commander trusts execution; agent trusts support and arbitration.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/MISSION_COMMAND.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
