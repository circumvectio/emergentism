---
rosetta:
  primary_level: L4
  primary_column: Active Defense Blueprint
  secondary:
    - level: L3
      column: Security Receipt Audit
      role: "require dated health, invariant, or breach-detection receipts before runtime claims"
    - level: L5
      column: Defense Architecture
      role: "map canaries, invariants, honeytokens, and fail-closed design"
    - level: L6
      column: Runtime Boundary
      role: "prevent design examples from becoming deployed security proof"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/D/B]"
  canonical_phrase: "Active Defense Doctrine (Tripwires)"
title: "Active Defense Doctrine (Tripwires)"
status: "BLUEPRINT — design reference"
evidence_tier: "[I] for doctrine; [D] for example patterns; [B] only for deployed and tested tripwire receipts."
---

# Active Defense Doctrine (Tripwires)

> **Holographic Briefing**
> **Position: 80_DAC_FRAME > 02__BLUEPRINT > ACTIVE_DEFENSE
> **Status**: Canonical ✅
> **Intent**: Define and operationalize Active Defense Doctrine (Tripwires).

---


**Purpose**: To detect failure *during* operation, not just after.
**Method**: Place "Sensors" in the code that trigger on specific dangerous conditions.

**Rosetta boundary:** This paper defines a design pattern. It is not evidence
that any canary, invariant, honeytoken, or fail-closed behavior is deployed.
Runtime security truth requires current logs, tests, or incident receipts.

## 1. The Tripwire Concept
[I] A Tripwire is a piece of code (invariant check) or a data artifact that should **never be touched** under normal operations. If it is touched, it means containment is breached.

## 2. Types of Sensors

### The Canary (Health Check)
- **Function**: Validates that the system is alive.
- **Example**: `GET /healthz` -> 200 OK.
- **Action**: If dead, restart.

### The Invariant (Sanity Check)
- **Function**: Validates that "Reality" matches "Physics".
- **Example**: `assert balance >= 0`.
- **Action**: If violated, CRASH IMMEDIATELY (Fail Fast). Do not corrupt data.

### The Honeytoken (Breach Detection)
- **Function**: Detects unauthorized scanning/access.
- **Example**: A fake AWS Key buried in a config file. Or a user account `admin_test` that no one uses.
- **Action**: If accessed, trigger SEV1 Security Incident. We are compromised.

## 3. Rules of Engagement
- **Do not block valid traffic**: Tripwires must have 0% false positives.
- **Fail Closed**: If the security system fails, the door stays locked.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/ACTIVE_DEFENSE.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
