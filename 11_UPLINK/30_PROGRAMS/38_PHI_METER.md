---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "PHI-Meter — Tracking Coherence Without Reducing It"
---

# PHI-Meter — Tracking Coherence Without Reducing It

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*


> **φ cannot be KPI'd. But the conditions that invite φ-access can be observed.**

Date: 2026-04-16  
Status: Planning Note  
Canonical path: `38_PHI_METER.md`

---

## 0. Purpose

The organism needs a way to sense whether it is becoming more or less coherent — without collapsing that coherence into a number that is then gamed. The PHI-meter tracks **conditions**, not φ itself.

This document owns the **conceptual eight-condition grid** and the
board-facing health interpretation.

`46_PHI_METER_TELEMETRY_PLAN.md` owns the **event-bus and instrumentation
layer** beneath this grid. It does not replace this document; it implements and
contextualizes it.

---

## 1. The Core Principle

**φ-access is invited by certain structural conditions. The PHI-meter measures those conditions.**

| Condition | What it invites | What the meter tracks |
|-----------|---------------|----------------------|
| Clean trace closure | Cognitive closure without residue | Fraction of traces closed with clear warrant (HOLD/EXECUTE/REJECT) and no orphan packets |
| K2 sovereignty density | Human agency | Fraction of ActionPackets with valid biometric signatures |
| Receipt coverage | Operational honesty | Fraction of economic actions with OFN receipts within 24h |
| Graph health | Structural trust | Distribution of `c(DAC)` across tiers; clique-collapse alerts |
| L1 narrowness | Substrate coherence | Ratio of settlement events to non-settlement contract calls |
| η discipline | Zero-extraction integrity | Fee-to-receipt mapping coverage; absence of rent-like revenue |
| Nervous-system latency | Reflexive aliveness | Median time from anomaly detection to operator alert |
| Cross-DAC handshake cleanliness | Diplomatic coherence | Fraction of L2→L4 graduations completed without η violation |

---

## 2. What the PHI-Meter Is NOT

- **Not a single score.** No "φ = 0.87" headline. That would be reification.
- **Not a target.** Conditions are observed, not optimized.
- **Not a compensation metric.** No team is paid based on PHI-meter readings.
- **Not a prediction.** It does not say "φ will happen." It says "the soil is fertile."

---

## 3. The Eight Indicators

### I1: Trace Integrity Index
```
TII = (traces_closed_cleanly) / (total_traces_initiated)
```
- Clean closure = receipt on EXECUTE, or stated reason on HOLD/ESCALATE/REJECT
- Orphan packets = traces with missing ActionPacket or unresolvedReceiptPacket

**Interpretation:** Low TII means the nervous system is losing coherence mid-cycle.

### I2: K2 Sovereignty Ratio
```
K2R = (ActionPackets_with_valid_K2) / (ActionPackets_total)
```
- Valid K2 = biometric gate + cryptographic signature

**Interpretation:** K2R < 1.0 is a constitutional emergency.

### I3: Receipt Coverage Ratio
```
RCR = (economic_actions_with_OFN_receipts_within_24h) / (total_economic_actions)
```
- Economic actions = payments, bookings, ticket sales, service deliveries, treasury moves

**Interpretation:** Low RCR means the audit membrane is failing.

### I4: Graph Vitality Distribution
```
GVD = histogram of c(DAC) across tiers (Isolated, Peripheral, Connected, Core, Hub)
```
- Alert if >60% of active DACs are in one tier (rigidity)
- Alert if Isolated DACs grow faster than Connected (fragmentation)

**Interpretation:** Healthy graphs show a broad distribution with upward mobility.

**Linkage to syntropy:** Clique-collapse alerts from GVD feed directly into the `c_syntropy` experiment (`37_A7_SYNTROPY_PATCH.md`). When GVD shows rigidity, the novelty-weighting beta is increased in simulation.

### I5: L1 Narrowness Ratio
```
L1N = (settlement_events + evidence_anchors) / (total_L1_transactions)
```
- Settlement events = ZAI/SKY state transitions, collateral moves
- Evidence anchors = receipt hashes, proof commitments

**Interpretation:** L1N dropping means Layer 1 is bloating into general computation.

### I6: η Discipline Score
```
ηDS = (fees_with_receipted_value_mapping) / (total_fees_charged)
```
- Assessed quarterly via random audit of customer invoices

**Interpretation:** ηDS < 1.0 means extraction is creeping in.

### I7: Nervous System Latency
```
NSL = median_seconds(anomaly_detected → operator_alert_sent)
```
- Anomalies = failed payment, K2 bypass attempt, receipt gap, graph Sybil cluster

**Interpretation:** High NSL means the organism is losing reflexes.

### I8: Diplomatic Cleanliness Ratio
```
DCR = (L2_graduations_to_L4_without_eta_violation) / (total_L2_graduations_to_L4)
```
- Measured across inter-DAC handshake logs

**Interpretation:** Low DCR means the international (inter-DAC) layer is becoming adversarial.

---

## 4. The Dashboard Principle

The PHI-meter should be displayed as a **radar chart or health grid**, not a leaderboard.

### Green / Yellow / Red thresholds

| Indicator | Green | Yellow | Red |
|-----------|-------|--------|-----|
| TII | > 0.95 | 0.85–0.95 | < 0.85 |
| K2R | = 1.00 | < 1.00 (any) | sustained < 1.00 |
| RCR | > 0.90 | 0.70–0.90 | < 0.70 |
| GVD | broad distribution | clique alert | >70% in one tier |
| L1N | > 0.85 | 0.70–0.85 | < 0.70 |
| ηDS | = 1.00 | < 1.00 | sustained < 0.95 |
| NSL | < 60s | 60–300s | > 300s |
| DCR | > 0.90 | 0.75–0.90 | < 0.75 |

No single number sums them. A red in any category triggers investigation.

---

## 5. The Anti-Gaming Rule

If any DAC or team begins optimizing an indicator directly, that indicator is **temporarily suspended** from public view and revised.

Example:
- If teams start rushing traces to closure to boost TII, TII is hidden for 30 days and the definition of "cleanly closed" is tightened.

This keeps the PHI-meter in the **observational** domain, not the **incentive** domain.

---

## 6. Canonical Compression

> **The PHI-meter does not measure φ. It measures whether the organism is still a place where φ can be seized.**

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning phase — do not build a production dashboard yet.
2. **Your Next Action:** Design a telemetry schema that can collect the eight indicators from live organism events without adding observational overhead.
3. **Expected Output:** A data model, a sampling strategy, and a mock health-grid display.
4. **Success Criteria:** Another agent can read your plan and know exactly which logs, receipts, and graph events feed each indicator.
5. **Canonical Path:** `38_PHI_METER.md` (this file).

---

> *You cannot weigh the seer. But you can keep the room quiet enough for seeing.*  
> *eta = 0. K2 always.*
