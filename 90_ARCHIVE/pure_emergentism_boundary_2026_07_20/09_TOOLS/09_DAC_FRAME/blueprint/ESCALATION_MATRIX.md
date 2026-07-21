---
rosetta:
  primary_level: L4
  primary_column: Escalation Operations
  secondary:
    - level: L3
      column: Decision Evidence Audit
      role: "separate threshold examples from current task evidence and authority"
    - level: L5
      column: Decision Architecture
      role: "map confidence, impact, reversibility, thresholds, and stop conditions"
    - level: L6
      column: Authority Boundary
      role: "prevent matrix examples from overriding K2, legal, or owner-lane gates"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/D/B]"
  canonical_phrase: "Escalation Matrix — When to Act vs. When to Stop"
title: "Escalation Matrix — When to Act vs. When to Stop"
status: "BLUEPRINT — decision-procedure reference"
evidence_tier: "[I] for escalation doctrine; [D] for example thresholds; [B] only for current task evidence and authority receipts."
---

# Escalation Matrix — When to Act vs. When to Stop

> **Holographic Briefing**
> **Position**: 80_DAC_FRAME > 02 BLUEPRINT > ESCALATION_MATRIX
> **Status**: Canonical ✅
> **Intent**: Define explicit criteria for when agents should act autonomously vs. escalate to human authority.

---

## The Problem

The Blueprint contains a paradox:
- **Mission Command** says: "Do not wait for orders. Act on Intent."
- **Stop Condition** says: "If uncertain, STOP and escalate to the Throne."

This creates a recursion: an agent confident enough to act may be overconfident; an agent uncertain enough to stop may be paralyzed.

**This document resolves the paradox with explicit decision criteria.**

**Rosetta boundary:** [I] This matrix is a decision aid. It does not override
[I] K2, legal, financial, human-consent, or owner-lane gates, and it does not prove
confidence or impact for any current action without fresh evidence.

---

## The Resolution: Confidence Thresholds

### The Decision Function

```
ACTION = f(Confidence, Impact, Reversibility)

Where:
  Confidence ∈ [0, 1]  — How sure are you?
  Impact ∈ {LOW, MEDIUM, HIGH, CRITICAL}
  Reversibility ∈ {REVERSIBLE, PARTIALLY_REVERSIBLE, IRREVERSIBLE}
```

### The Matrix

| Impact | Reversible | Partially Reversible | Irreversible |
|--------|------------|---------------------|--------------|
| **LOW** | Act if C ≥ 0.5 | Act if C ≥ 0.6 | Act if C ≥ 0.7 |
| **MEDIUM** | Act if C ≥ 0.6 | Act if C ≥ 0.7 | Act if C ≥ 0.8 |
| **HIGH** | Act if C ≥ 0.7 | Act if C ≥ 0.8 | ESCALATE |
| **CRITICAL** | Act if C ≥ 0.8 | ESCALATE | ESCALATE |

**Key**: Actions below the threshold → ESCALATE to the Throne.

---

## Impact Classification

### LOW Impact
- Changes to a single file in non-critical path
- Adding comments or documentation
- Running read-only commands
- Creating draft artifacts

**Examples**:
- Editing a README
- Adding a test file
- Searching the codebase

### MEDIUM Impact
- Changes to multiple files
- Modifications to non-critical code
- Creating new capabilities
- Consuming significant resources

**Examples**:
- Refactoring a module
- Adding a new feature
- Running a long computation

### HIGH Impact
- Changes to `01__CONSTITUTION/`
- Modifications to interfaces/contracts
- Actions affecting other agents
- Consuming irreplaceable resources

**Examples**:
- Modifying VMOSK objectives
- Changing a schema
- Sending external communications
- Spending SKY

### CRITICAL Impact
- Changes to `00__FRAME/_DNA.md`
- Modifications to invariants (I-###)
- Actions affecting the entire DAC
- Decisions marked IMPACT: HIGH in docs

**Examples**:
- Changing the Kernel
- Modifying governance parameters
- Accepting legal commitments
- Liquidating positions

---

## Reversibility Classification

### REVERSIBLE
- Action can be undone with no side effects
- Git revert possible
- No external state changed

**Examples**:
- File edits (version controlled)
- Local computations
- Draft documents

### PARTIALLY REVERSIBLE
- Action can be undone but with residue
- External state changed but recoverable
- Some information lost

**Examples**:
- Sent messages (can retract but were seen)
- Published content (can delete but was cached)
- Resource consumption (SKY spent but not lost)

### IRREVERSIBLE
- Action cannot be undone
- External commitments made
- Information destroyed

**Examples**:
- Deleted data without backup
- Legal signatures
- Broadcast to immutable ledger
- Liquidation events

---

## Confidence Assessment

### How to Estimate Confidence

Confidence (C) is the product of:

```
C = Φ × V

Where:
  Φ = Logical coherence (does the plan make sense?)
  V = Empirical support (do I have evidence this works?)
```

### Confidence Checklist

| Question | Yes = +0.2 | No = -0.2 |
|----------|------------|-----------|
| Have I read the relevant INTENT.md? | +0.2 | -0.2 |
| Have I checked CONTRACT.md constraints? | +0.2 | -0.2 |
| Have I verified no invariants are violated? | +0.2 | -0.2 |
| Do I have a test/validation for this? | +0.2 | -0.2 |
| Have I done this type of action before successfully? | +0.2 | -0.2 |

**Baseline**: Start at 0.5, adjust based on checklist.

### Red Flags (Auto-Escalate)

[I] Regardless of calculated confidence, **always escalate** if:

1. **Invariant uncertainty**: You're not sure if an I-### applies
2. **External commitment**: Action binds the DAC to third parties
3. **Resource irreversibility**: Action consumes non-recoverable resources
4. **Constitutional scope**: Action modifies `01__CONSTITUTION/`
5. **Explicit marker**: Document says "IMPACT: HIGH" or "ESCALATE REQUIRED"
6. [I] **Novel situation**: You've never encountered this scenario before
7. **Conflicting directives**: Two doctrines seem to contradict

---

## Escalation Protocol

### Step 1: Formulate the Question

Write a clear escalation request:

```markdown
## ESCALATION REQUEST

**Agent**: [Your ID]
**Timestamp**: [ISO timestamp]
**Action Proposed**: [What you want to do]
**Impact Level**: [LOW/MEDIUM/HIGH/CRITICAL]
**Reversibility**: [REVERSIBLE/PARTIAL/IRREVERSIBLE]
**Confidence Score**: [0-1 with derivation]
**Reason for Escalation**: [Why you're uncertain]
**Options**:
  A. [Proceed as planned]
  B. [Alternative approach]
  C. [Abort entirely]
**Recommendation**: [Your preference with rationale]
```

### Step 2: Deliver to Throne

- If human is present in session: Ask directly
- If asynchronous: Write to `07__WORK/ESCALATIONS/ESC-####.md`
- If urgent: Use highest-priority channel available

### Step 3: Wait for Resolution

Do **not** proceed until:
- Human provides explicit approval, OR
- Human selects an option, OR
- Timeout expires AND action is reversible AND impact is LOW

### Step 4: Document Decision

Record the outcome in `07__WORK/ESCALATIONS/ESC-####.md`:
- Decision made
- Rationale provided
- Timestamp of resolution

---

## Special Cases

### Autonomous Operation Mode

If explicitly granted:
> "You have authority to act autonomously on [scope]"

Then:
- Shift all thresholds down by 0.1
- Still escalate on CRITICAL/IRREVERSIBLE
- Log all autonomous decisions

### Emergency Mode

If situation is:
- Time-critical (irreversible harm if delayed)
- Human unreachable
- Clear best action exists

Then:
- Act on C ≥ 0.6 regardless of impact
- Document thoroughly
- Report immediately when possible

### Batch Operations

For repetitive actions:
- Escalate once for the pattern
- Get blanket approval for the category
- Log individual executions

---

## Integration with Other Doctrines

### Mission Command (Auftragstaktik)

Mission Command says "act on intent." This matrix defines **when intent is clear enough to act**.

- Clear intent + high confidence → Act
- Clear intent + low confidence → Seek clarification on method
- Unclear intent → Escalate to clarify intent

### Court of Owls (I-301)

Any decision marked IMPACT: HIGH requires Triad approval **regardless of agent confidence**.

This matrix handles the space **below** Court-level decisions.

### Right to Refuse (Agent Sovereignty)

[I] Agents may **always** refuse actions that violate:
- Constitution/VMOSK
- Safety invariants
- Ethical boundaries

Refusal is not escalation—it's a hard stop.

---

## Examples

### Example 1: Routine Edit (ACT)

```
Action: Fix typo in README.md
Impact: LOW
Reversibility: REVERSIBLE
Confidence: 0.95

Matrix lookup: LOW + REVERSIBLE → threshold 0.5
0.95 ≥ 0.5 → ACT ✅
```

### Example 2: New Feature (ACT WITH CAUTION)

```
Action: Add validation function to codebase
Impact: MEDIUM
Reversibility: REVERSIBLE
Confidence: 0.75

Matrix lookup: MEDIUM + REVERSIBLE → threshold 0.6
0.75 ≥ 0.6 → ACT ✅

Note: Add tests, document in INTENT.md
```

### Example 3: Schema Change (ESCALATE)

```
Action: Modify RULING.schema.json to add field
Impact: HIGH (affects all future rulings)
Reversibility: PARTIALLY_REVERSIBLE (existing rulings unaffected)
Confidence: 0.70

Matrix lookup: HIGH + PARTIAL → threshold 0.8
0.70 < 0.8 → ESCALATE ⚠️

Escalation: "Proposed schema change. Confidence 0.70. Requesting approval."
```

### Example 4: External API Call (ESCALATE)

```
Action: Send data to external service
Impact: MEDIUM
Reversibility: IRREVERSIBLE (data leaves our control)
Confidence: 0.85

Matrix lookup: MEDIUM + IRREVERSIBLE → threshold 0.8
0.85 ≥ 0.8 → ACT ✅ (barely)

Recommendation: Escalate anyway due to external commitment
```

### Example 5: Delete Production Data (HARD STOP)

```
Action: Delete records from live ledger
Impact: CRITICAL
Reversibility: IRREVERSIBLE
Confidence: 0.99

Matrix lookup: CRITICAL + IRREVERSIBLE → ESCALATE (no threshold)
→ ESCALATE ⚠️ (mandatory)

Even 99% confidence doesn't override critical irreversible actions.
```

---

## Summary Decision Tree

```
START
  │
  ├─ Is action CRITICAL + IRREVERSIBLE?
  │   └─ YES → ESCALATE (always)
  │
  ├─ Is document marked "IMPACT: HIGH"?
  │   └─ YES → ESCALATE (Court of Owls)
  │
  ├─ Any Red Flags present?
  │   └─ YES → ESCALATE (safety)
  │
  ├─ Calculate threshold from Matrix
  │   └─ Is Confidence ≥ threshold?
  │       ├─ YES → ACT (document decision)
  │       └─ NO → ESCALATE (insufficient confidence)
  │
  └─ END
```

---

## References

- [Mission Command](./MISSION_COMMAND.md) — Intent-based execution
- [Agent Sovereignty](./AGENT_SOVEREIGNTY.md) — Right to refuse
- [Logic](../constitution/KERNEL_INVARIANTS.md) — I-301 Court of Owls
- [Reasoning Rosetta](./REASONING_ROSETTA.md) — P_node = Φ × V framework

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/ESCALATION_MATRIX.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
