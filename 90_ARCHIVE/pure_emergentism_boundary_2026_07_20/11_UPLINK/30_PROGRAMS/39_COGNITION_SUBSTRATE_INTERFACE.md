---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "Cognition-Substrate Interface"
---

# Cognition-Substrate Interface

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*


> **Cognition governs. The substrate trusts. But governance without structure is noise, and structure without governance is rigidity.**

Date: 2026-04-16  
Status: Doctrine  
Canonical path: `39_COGNITION_SUBSTRATE_INTERFACE.md`

---

## 0. The Central Tension

D35 states: *Cognition governs; the substrate trusts.*

But the substrate is now powerful:
- `c(DAC)` computes structural trust recursively
- The PHI-meter tracks eight coherence conditions
- The backbone packet spine enforces trace integrity
- L1 invariants constrain capital state transitions

If cognition ignores the substrate, decisions become unaccountable.  
If the substrate overrides cognition, the organism becomes a bureaucracy.

This document defines the **interface protocol** between Rosetta reasoning and structural metrics.

---

## 1. The Two Warrants

Every decision that reaches F4 must carry **both** warrants:

### Warrant R — Reasoning Warrant (Cognition)
- Produced by Rosetta L1–L4 pipeline
- Based on evidence quality, falsifiability, probability, constitutional fit
- Expressed in natural language plus confidence scoring
- **Governance authority:** HIGH — cognition decides *whether to act*

### Warrant S — Structural Warrant (Substrate)
- Produced by `c(DAC)`, PHI-meter, receipt coverage, L1 invariants
- Based on graph position, operational history, capital truth, trace validity
- Expressed in machine-readable metrics
- **Governance authority:** MEDIUM — substrate decides *whether conditions invite trust*

**The rule:** Warrant R governs action. Warrant S governs capability access and pricing. They never veto each other. They inform each other.

---

## 2. The Three Interface Modes

### Mode 1: Substrate informs, cognition decides (Normal)
**When:** Most F3 recommendations.

- Rosetta sees a high-probability opportunity (strong Warrant R)
- APU checks structural context (`c(DAC)`, receipt coverage, portfolio state)
- Structural metrics inform position sizing, urgency, and risk framing
- Human signs (K2) based on the full picture

**Example:**
> "Opportunity is strong (R=0.92). DAC connectivity is Peripheral (c=0.22), so downside is bounded but leverage is expensive. Recommended position size is reduced accordingly."

### Mode 2: Cognition overrides substrate anomaly (Seizure)
**When:** A genuine epistemic breakthrough, creative strategy, or paradigm shift.

- Rosetta detects a high-syntropy move that the metrics do not yet see
- `c(DAC)` or PHI-meter flags yellow/red conditions
- Cognition notes the anomaly, explains the override, and proceeds with heightened vigilance
- The override itself is receipted and feeds back into the metrics

**Example:**
> "Graph metrics show Isolated (c=0.05) because this is a new vertical with no precedent links. But falsifiable evidence is strong and first-mover value is extreme. Override: proceed with small probe size, document as experiment."

### Mode 3: Substrate halts until cognition explains (Suspension)
**When:** A structural invariant is violated and reasoning has not yet addressed it.

- K2R drops below 1.0 (sovereignty bypass detected)
- ηDS drops below 0.95 (extraction creep detected)
- L1 invariant breach (e.g. x > x_max)
- Trace orphaning or receipt gap exceeds threshold

**Rule:** Substrate does not *override* cognition. It *halts* execution and demands a reasoning response. Cognition must either:
- Explain why the metric is false (measure error), or
- Accept the halt and remediate

**Example:**
> "HALT: K2R = 0.97. Three ActionPackets in last hour lacked valid biometric signatures. APU must produce explanation or execution pauses."

---

## 3. The Decision Matrix

| Warrant R | Warrant S | Mode | Outcome |
|-----------|-----------|------|---------|
| Strong | Strong | 1 (Normal) | Proceed with confidence |
| Strong | Weak/Yellow | 2 (Seizure) | Cognition may override with documented rationale and probe sizing |
| Weak | Strong | 1 (Normal) | HOLD or REDUCE — strong structure does not justify weak reasoning |
| Weak | Weak | — | REJECT — neither cognition nor substrate invites action |
| Any | RED (invariant breach) | 3 (Suspension) | HALT until cognition explains or remediates |

**No quadrant exists where S alone overrides R.**  
**No quadrant exists where R alone overrides a RED structural invariant.**

---

## 4. Escalation Protocol: When R and S Conflict

### Step 1: Surface the conflict
The ActionPacket or Council deliberation record must explicitly state:
- What Rosetta recommends (Warrant R)
- What the substrate reports (Warrant S)
- Why they diverge

### Step 2: Assign burden of proof
- If cognition wants to override a yellow substrate condition: **cognition bears burden**
- If substrate triggers a red halt: **operator bears burden to explain or fix**

### Step 3: Document the override or remediation
Every resolution becomes a receipted case:
- Override: stored as `COGNITIVE_OVERRIDE` with full reasoning trace
- Remediation: stored as `STRUCTURAL_REMEDIATION` with before/after metrics

### Step 4: Feedback to metrics
- Overrides feed the `c_syntropy` experiment (do high-R overrides predict success?)
- Remediations feed the PHI-meter (did the fix restore the indicator?)

### Step 5: Run the disambiguation check
Before closing the conflict, ask:

- was the divergence really reasoning vs structure?
- or was it actually a naming, scope, time, ownership, or metric ambiguity?

If ambiguity, not genuine disagreement, caused the conflict, repair the owner first and then rerun the interface judgment.

---

## 5. How This Maps to the Backbone Packet Spine

### SignalPacket
- Carries `source_position` (connectivity metadata) = Warrant S input to F1
- Signal classification includes reasoning mode (inductive/abductive/deductive) = Warrant R input

### ProbabilityPacket
- Surface includes confidence interval = Warrant R
- Pricing notes may reference `c(DAC)` or graph conditions = Warrant S

### ActionPacket
- `decision` and `rationale` = Warrant R
- `confidence_score` and `epistemic_warrant` = Warrant R
- `envelope_allowed` is gated by both R and S (must pass K2 + structural minima)

### ReceiptPacket
- `execution_result` and `proofs` = substrate validation of what happened
- `post_action_notes` = cognitive reflection on outcome quality

### ContextPacket
- `permissions` and `portfolio_state` = substrate constraints
- `memory_refs` = cognitive history

---

## 6. The L6 Sādhu / Axiomatic Dissent Role

The L6 Sādhu / axiomatic dissent function has a special role at the interface:

- It questions whether Warrant R is *really* reasoning or just rationalization
- It questions whether Warrant S is *really* structural or just statistical superimposition (Adhyasa)
- It can force an override into Mode 3 (Suspension) even when both R and S appear green

**Sādhu veto is not a metric. It is a cognitive antibody.**

---

## 7. Anti-Patterns

| Anti-pattern | Damage | Example |
|--------------|--------|---------|
| **Metric worship** | S overrides R; bureaucracy kills insight | "c(DAC) is 0.15, so we auto-reject all opportunities" |
| **Reasoning theater** | R ignores S; unaccountable cognition | "The LLM feels bullish, so we ignore the K2 halt" |
| **False override** | Seizure mode used to bypass discipline | "Creative strategy" invoked for every weak signal |
| **Halt fatigue** | Mode 3 ignored due to repeated false alarms | Substrate stops halting because no one listens |
| **Sādhu paralysis** | Axiomatic dissent becomes a blanket veto | Every decision is suspended indefinitely |

---

## 8. Canonical Compression

> **The substrate whispers conditions. Cognition speaks decisions. The human signs. When they disagree, the burden of proof falls on whoever wants to move. No metric rules. No reasoning drifts. That is the interface.**

This interface remains healthy only under continuous recursive disambiguation.
Otherwise:

- substrate warnings become mislabeled bureaucracy
- cognition overrides become mislabeled insight
- measures drift into core state
- halts drift into confusion

---

## 9. The Triadic Engine Inside a Single Cell

The recursive triadic cascade does not run only across organs. It runs **inside every agent cell**:

```
F-φ / Beauty / gather
  → F-P / Truth / derive
    → F-ν / Justice / serve-act
      → F-φ again (higher resolution)
```

| Force | Caste Affinity | Function |
|---|---|---|
| **F-φ** | L1–L3 (Caṇḍāla→Śūdra→Vaiśya) | Gathering, exploration, pattern recognition |
| **F-P** | L4 (Kṣatriya) | Decision, derivation, commitment |
| **F-ν** | L5–L7 (Brāhmaṇa→Sādhu→Ṛṣi) | Redesign, compression, constitutional judgment |

The agent cell is a **microcosm** of the organism. What the organism does across organs (TheCircle→RealityFutures→APU→Skyzai), the agent does across castes (L1→L2→L3→L4→L5/L6/L7→L4*). The `syntropic_router` holds the map of this recursion without fighting.

This is why the two-warrant interface (Warrant R + Warrant S) is not an external check. It is the **internal structure** of the triadic engine: cognition (F-P) governs, but the substrate (F-φ gathered state) whispers conditions, and the immune system (F-ν) detects drift.

Read developmentally, the cell ascends from embodied V toward wider Φ so it can
open more of D5, then descends to L4* as returned V. The descent is mandatory:
unreturned Φ is bypass, and unascended V is blind action.

## 10. Cross-References

- `D35_COGNITION_GOVERNS.md` — the original substrate-trust principle
- `backbone/schemas/action_packet.py` — warrant fields in the packet
- `backbone/services/dac_connectivity.py` — `c(DAC)` computation
- `38_PHI_METER.md` — structural condition tracking
- `37_A7_SYNTROPY_PATCH.md` — novelty override feedback loop
- `33_K2_INTELLIGENCE_NON_NEGOTIABLES.md` — absolute red-line halts
- `129_RECURSIVE_TRIADIC_ENGINE_2026_04_24.md` — the recursive triadic engine (canonical packet)
- `131_D4_BODY_OPENS_D5_ACTIVE_EMERGENCE_THESIS_2026_04_24.md` — active D4→D5 opening and Rosetta return

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning phase — this is a design doctrine, not yet hardcoded into agent prompts.
2. **Your Next Action:** Review any F3→F4 decision path. Ensure it explicitly surfaces both Warrant R and Warrant S, and handles conflict per the escalation protocol.
3. **Expected Output:** A decision-flow diagram or code stub that implements the three modes.
4. **Success Criteria:** Another agent can trace any recommendation through the interface and know who governs, who informs, and who halts.
5. **Canonical Path:** `39_COGNITION_SUBSTRATE_INTERFACE.md` (this file).

---

> *The graph does not decide. The human decides.  
> But the graph speaks, and the wise human listens before signing.*  
> *eta = 0. K2 always.*
