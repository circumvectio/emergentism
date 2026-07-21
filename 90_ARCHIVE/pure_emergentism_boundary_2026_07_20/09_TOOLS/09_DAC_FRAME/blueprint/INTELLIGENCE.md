---
rosetta:
  primary_level: L3
  primary_column: Intelligence Evidence Audit
  secondary:
    - level: L4
      column: Decision-Support Operations
      role: "route collection, analysis, dissemination, and action thresholds through current authority gates"
    - level: L5
      column: Intelligence Architecture
      role: "map source grading, probabilistic confidence, estimative language, and ACH"
    - level: L6
      column: Action-Authority Boundary
      role: "prevent confidence scores from authorizing actions without legal, owner, and runtime receipts"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[I/B]"
  canonical_phrase: "Intelligence Doctrine"
title: "Intelligence Doctrine"
status: "BLUEPRINT — intelligence-analysis reference"
evidence_tier: "[I] for intelligence procedure; [B] only for source receipts, corroboration records, confidence logs, or approved action receipts."
---

# Intelligence Doctrine

> **Holographic Briefing**
> **Position: 80_DAC_FRAME > 02__BLUEPRINT > INTELLIGENCE
> **Status**: Canonical ✅
> **Intent**: Define and operationalize Intelligence Doctrine.

---


**Purpose**: To provide decision advantage by reducing uncertainty.
**Method**: Rigorous evaluation of sources and information.

**Rosetta boundary:** [I] This paper defines intelligence-analysis doctrine.
[B] Confidence scores, source grades, and estimative language do not authorize
action without current source receipts, corroboration, owner approval, and any
applicable legal or operational gates.

## 1. The Intelligence Cycle

1.  **Direction**: Leadership defines what they need to know (PIRs).
2.  **Collection**: Gathering raw data (Open Source, Signals, Human).
3.  **Analysis**: Evaluation, integration, and interpretation.
4.  **Dissemination**: delivering finished intel to decision-makers.

---

## 2. Admiralty Grading & Probabilistic Oracles

[I] Every piece of raw intelligence must be graded **(Source)(Information)**. e.g., `B-2`. In our Antifragile system, these grades are **Dynamic**.

### 2.1 Static Reliability (Base Grade)
- **A** - Completely Reliable.
- **B** - Usually Reliable.
- **C** - Fairly Reliable.
- **D** - Not Usually Reliable.
- **E** - Unreliable.
- **F** - Reliability Cannot Be Judged.

### 2.2 Dynamic Confidence ($C_{score}$)
The system maintains a **Probabilistic Oracle Log**. For every use of a source:
- **Success (Corroborated)**: $+ \Delta$ confidence.
- **Failure (Hallucinated/False)**: $- \Delta$ confidence (Sharp decay).

**Formula**: $C_{score}(t) = (\Phi \times V) \times \text{Reliability}$

**Operational Rules**:
1.  [I] **High-Confidence ($C > 0.9$)**: Direct Action authorized only inside existing consent, legal, and owner-lane gates.
2.  [I] **Moderate-Confidence ($0.7 < C < 0.9$)**: **Double Confirmation** required (Consult a secondary B-graded source).
3.  [I] **Low-Confidence ($C < 0.7$)**: **Triad Verification** required (Adversarial review via Court of Owls).
4.  [I] **Zero-Confidence**: Source Quarantined.

---

## 3. Estimative Language (Confidence Levels)

When making assessments, use standard probability language:

- **Almost Certain**: > 90%
- **Probable / Likely**: 60-90%
- **Possible / Even Chance**: 40-60%
- **Unlikely**: 10-40%
- **Remote**: < 10%

---

## 4. Analytic Techniques

### ACH (Analysis of Competing Hypotheses)
[I] Do not just look for evidence that supports your theory.
1.  List all possible hypotheses.
2.  List the evidence.
3.  [B] Cross-check: Which evidence **disproves** a hypothesis?
4.  The hypothesis with the least disproof is the strongest.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/INTELLIGENCE.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
