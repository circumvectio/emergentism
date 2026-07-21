---
rosetta:
  primary_level: L4
  primary_column: Work Lifecycle Operations
  secondary:
    - level: L3
      column: Phase-Gate Evidence Audit
      role: "separate process doctrine from current intent, contract, evidence, deployment, or AAR receipts"
    - level: L5
      column: OODA Work Architecture
      role: "map observe, orient, decide, act, verification, ship, and learn gates"
    - level: L6
      column: Shipping Boundary
      role: "prevent process model from proving code was shipped or verified"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/B]"
  canonical_phrase: "OS Model: Process (Lifecycle of Work)"
title: "OS Model: Process (Lifecycle of Work)"
status: "CONSTITUTION OS — workflow doctrine"
evidence_tier: "[I] for process doctrine; [B] only for current INTENT, CONTRACT, ADR, test, deployment, runbook, or AAR receipts."
---

# OS Model: Process (Lifecycle of Work)

**Type**: Normative Doctrine (Constitution)
**Status**: ACTIVE
**Source**: Inherited from v0.1 (Legacy Intake)

---

## 1. Objective Function (Why)
**Purpose**: To standardize the "Metabolism" of work.
**Goal**: To move from an Intake to a Shipped state with zero information loss and maximum verification.

**Rosetta boundary:** [I] This paper defines lifecycle doctrine. It does not
prove a work item has oriented, shipped, verified, or learned; [B] those require
current intent, contract, ADR, evidence, runbook, or AAR receipts.

## 2. Core State (What)

### The OODA Loop (Refined)
1.  **Observe (Intake)**: Identify the need (PR/FAQ + Metrics).
2.  **Orient (NodeID)**: Assign a location in the Frame. Write the `INTENT.md` and `CONTRACT.md`.
3.  **Decide (COA)**: Choose a Course of Action and ADR if needed.
4.  **Act (Build)**: Implement code, tests, and specs.
5.  [B] **Prove (Verification)**: Provide evidence as per the `KERNEL_INVARIANTS.md` hierarchy.
6.  **Ship (Deployment)**: Update runbooks and the Shadow Graph.
7.  **Learn (Evolution)**: Run an After Action Review (AAR) and promote patterns.

## 3. Auditing (How)

### Phase Gates
- [I] **Gate 1 (Orient)**: No code may be written until the `INTENT.md` is registered.
- [I] **Gate 2 (Prove)**: No code is moved to `04_REALITY` without Evidence.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/constitution/OS/PROCESS.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
