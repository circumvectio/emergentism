---
rosetta:
  primary_level: L4
  primary_column: OPSEC Operations
  secondary:
    - level: L3
      column: Threat Evidence Audit
      role: "separate critical-information, threat, vulnerability, and risk claims from current evidence"
    - level: L5
      column: Security Architecture
      role: "map OPSEC steps, critical information lists, indicators, countermeasures, and agent responsibilities"
    - level: L6
      column: Lawful Security Boundary
      role: "prevent OPSEC or countermeasure language from authorizing deception, illegal conduct, or unapproved security action"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/B]"
  canonical_phrase: "Operations Security (OPSEC) Doctrine"
title: "Operations Security (OPSEC) Doctrine"
status: "BLUEPRINT — security-operations reference"
evidence_tier: "[I] for OPSEC doctrine; [B] only for current CIL, threat model, risk register, approval, or security-control receipts."
---

# Operations Security (OPSEC) Doctrine

> **Holographic Briefing**
> **Position: 80_DAC_FRAME > 02__BLUEPRINT > OPSEC
> **Status**: Canonical ✅
> **Intent**: Define and operationalize Operations Security (OPSEC) Doctrine.

---


**Purpose**: To deny the adversary the information they need to harm us.
**Method**: Identify what matters, hide the indicators, and disrupt collection.

**Rosetta boundary:** [I] This paper defines OPSEC doctrine, not proof of live
security controls or permission for deception, unlawful conduct, or unapproved
countermeasures. [B] Security claims require current CIL, threat-model,
risk-register, approval, and control receipts.

## The 5 Steps of OPSEC

### 1. Identify Critical Information (CI)
[I] What are the "Crown Jewels"? What specific facts, if known by the adversary, would lead to mission failure?
- *Examples*: Product launch dates, pricing strategies, unpatched vulnerabilities, private keys, customer lists.

### 2. Analyze Threats
Who is the adversary?
- **Intent**: Do they want to harm us?
- **Capability**: Can they harm us?
- *Examples*: Competitors, Hackers, Insider Threats, Leakers.

### 3. Analyze Vulnerabilities
How can the adversary get the CI? What are the **Indicators**?
- *Indicators*: Observable actions that point to the CI. (e.g., ordering pizza late at night indicates a crunch/launch).
- *Vulnerabilities*: Unencrypted comms, public code repos, talkative employees.

### 4. Assess Risk
**Risk = Impact x Probability**.
- If Impact is High (Failure) and Probability is High (Easy to find) -> **CRITICAL**.

### 5. Apply Countermeasures
Action taken to reduce risk.
- **Hide the Indicator**: Encrypt the data, use code names.
- [I] **Deception boundary**: Do not plant false flags or misrepresent identity without explicit lawful authorization and owner approval.
- **Disrupt**: Block the collection method.

---

## Agent Responsibilities
1.  **Read the CIL**: Know what is secret.
2.  [I] **Redact**: Never output CI into logs or public channels.
3.  [I] **Need to Know**: Do not ask for CI unless required for the task.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/OPSEC.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
