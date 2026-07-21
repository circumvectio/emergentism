---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "PHI-Meter Telemetry Plan"
---

# PHI-Meter Telemetry Plan

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*


> **You cannot optimize φ. But you can measure the conditions that invite it.**

Date: 2026-04-16  
Status: Planning Specification  
Canonical path: `46_PHI_METER_TELEMETRY_PLAN.md`

---

## 0. Purpose

Document 38 (`38_PHI_METER.md`) defined eight indicators that track whether the organism is creating conditions favorable to φ-access. This document specifies the telemetry layer: which events, logs, and graph updates feed each indicator, how the data flows, and how the system avoids gaming.

## 0b. Layer Split — 38 vs 46

`38_PHI_METER.md` remains the canonical **conceptual PHI-meter**:
the eight-condition health grid read by founders, operators, and governance.

This document owns the **telemetry implementation layer**:
event sources, event bus, lower-level observables, storage, and computation.

The two documents are compatible, but they do different jobs:

- **38** says what conditions matter
- **46** says how the organism listens for those conditions

## 0c. Mapping Table — 38 Conditions to 46 Telemetry

| 38 condition / dashboard surface | 46 telemetry ownership | How to read the relation |
|---|---|---|
| Clean trace closure / Trace Integrity Index | `τ_error`, `f_loop`, trace and proof events | Telemetry measures error half-life and loop completion; the 38 dashboard compresses that into whether traces are closing cleanly |
| K2 sovereignty density / K2R | `σ_sovereign`, `K2AttestationVerifiedEvent`, override events | 46 proves whether K2 paths remain intact; 38 summarizes that as sovereignty density |
| Receipt coverage / RCR | settlement and receipt events on `PhiEventBus`, plus `f_loop` context | 46 owns the event stream; 38 owns the board-facing receipt-coverage ratio |
| Graph health / GVD | `κ`, topology snapshots, connection events | 46 tracks graph-formation and value/complexity dynamics; 38 renders vitality and clique alerts |
| L1 narrowness / L1N | transaction-type mix in `PhiEventLog` | 46 records event classes; 38 expresses whether Layer 1 remains narrow |
| η discipline / ηDS | fee-mapping audits plus future fee events | 46 contextualizes; 38 remains the constitutional dashboard for zero-extraction integrity |
| Nervous-system latency / NSL | `λ_immune`, alert and anomaly events | 46 measures response timing; 38 reads whether reflexes remain alive |
| Diplomatic cleanliness / DCR | `v_empty`, cross-DAC adoption and resolution events | 46 tracks institutional interactions; 38 compresses them into handshake cleanliness |

The rule:

- when speaking conceptually or board-level, use **38**
- when implementing telemetry or debugging instrumentation, use **46**
- do not let the phrase `PHI-meter` silently mean both at once without naming which layer you are in

---

## 1. The Eight Indicators and Their Telemetry Sources

### 1.1 Cumulative Error Half-Life (`τ_error`)

**Definition:** Median time from error detection to verified fix.

**Telemetry sources:**
- `ErrorDetectedEvent` — timestamp, severity, component, detector_id
- `ErrorFixedEvent` — timestamp, fix_commit_hash, verifier_id
- `ErrorAcknowledgedEvent` — timestamp (if fix is delayed but acknowledged)

**Computation:**
```python
for each error:
    if fixed:
        t_fix = ErrorFixedEvent.timestamp - ErrorDetectedEvent.timestamp
    else:
        t_fix = now - ErrorDetectedEvent.timestamp  # open errors penalize
τ_error = median(t_fix for all errors in window)
```

**Collection frequency:** Real-time events, computed daily.

**Anti-gaming:** Fixes must be verified by a second node (not the original author). Rollbacks within 7 days invalidate the fix.

---

### 1.2 Graph Compression Rate (`κ`)

**Definition:** New value created per unit of graph complexity added.

**Telemetry sources:**
- `ProofSubmittedEvent` — proof_id, value_unlocked, complexity_delta
- `ConnectionFormedEvent` — connection_id, estimated_value, complexity_delta
- `SettlementClosedEvent` — settlement_id, value_transferred

**Computation:**
```python
value_created = sum(value_unlocked) + sum(value_transferred)
complexity_added = sum(complexity_delta)
κ = value_created / (complexity_added + 1)
```

**Collection frequency:** Per event, computed weekly.

**Anti-gaming:** `complexity_delta` is measured by VMOSK layer analysis, not self-reported. Artificially simple proofs are up-ranked in complexity by the linter.

---

### 1.3 Mean Cognitive Seizure Interval (`μ_seizure`)

**Definition:** Average time between non-trivial insight events in the reasoning layer.

**Telemetry sources:**
- `SeizureEvent` — timestamp, agent_id, insight_type, warrant_delta
- `WarrantRUpdatedEvent` — timestamp, old_warrant, new_warrant

**Computation:**
```python
seizure_times = [event.timestamp for event in SeizureEvent if warrant_delta > threshold]
if len(seizure_times) > 1:
    intervals = [t[i] - t[i-1] for i in range(1, len(seizure_times))]
    μ_seizure = mean(intervals)
else:
    μ_seizure = infinity  # no seizures
```

**Collection frequency:** Per event, computed daily.

**Anti-gaming:** Seizures are detected by Warrant R changes that contradict previous Warrant S predictions. Trivial oscillations (back-and-forth within 1 hour) are filtered.

---

### 1.4 Immune Response Latency (`λ_immune`)

**Definition:** Time from bad graph event to immune flag + corrective action.

**Telemetry sources:**
- `GraphAnomalyDetectedEvent` — timestamp, anomaly_type, detector_id
- `ImmuneFlagRaisedEvent` — timestamp, flag_id, triggered_by, severity
- `CorrectiveActionEvent` — timestamp, action_type, target_ba_id

**Computation:**
```python
for each anomaly:
    if immune_flag and corrective_action:
        t_response = max(ImmuneFlagRaisedEvent.timestamp, CorrectiveActionEvent.timestamp) - GraphAnomalyDetectedEvent.timestamp
    else:
        t_response = now - GraphAnomalyDetectedEvent.timestamp
λ_immune = median(t_response for all anomalies in window)
```

**Collection frequency:** Real-time, computed daily.

**Anti-gaming:** Corrective actions must be verified by graph state change, not just event emission. False anomaly reports by detectors are penalized.

---

### 1.5 Empty-Throne Decision Velocity (`v_empty`)

**Definition:** Rate of legitimate governance decisions made without central approval.

**Telemetry sources:**
- `ProtocolVoteEvent` — timestamp, proposal_id, outcome, voter_count
- `DACStandardAdoptedEvent` — timestamp, standard_id, adopter_count
- `AXIOMArbitrationResolvedEvent` — timestamp, case_id, resolution_type
- `CentralOverrideEvent` — timestamp, override_type, approver_id (negative signal)

**Computation:**
```python
decisions = count(ProtocolVoteEvent + DACStandardAdoptedEvent + AXIOMResolvedEvent)
overrides = count(CentralOverrideEvent)
v_empty = decisions / (overrides + 1)  # per day, normalized
```

**Collection frequency:** Per event, computed weekly.

**Anti-gaming:** Only votes with >2 distinct voters count. Standards must be referenced in subsequent proofs to count as adopted. AXIOM resolutions must be executed to count.

---

### 1.6 Synergy Loop Frequency (`f_loop`)

**Definition:** How often the reinforcing loops from `30_SYNERGY.md` complete a full cycle.

**Telemetry sources:**
- Loop-specific events:
  - `ProofSubmittedEvent` → `ValueUnlockedEvent` → `ConnectionFormedEvent`
  - `ImmunePenaltyBurnedEvent` → `NewProofSubmittedEvent`
  - `A7SyntropyBonusAwardedEvent` → `NovelConnectionFormedEvent`

**Computation:**
Each loop defines its own cycle detection heuristic. Example for the "Proof → Value → Connection" loop:
```python
cycles = 0
for proof in proofs:
    if ValueUnlockedEvent within 7 days after proof:
        if ConnectionFormedEvent within 30 days after value_unlocked:
            if new_connection involves a different DAC:
                cycles += 1
f_loop = cycles / window_days
```

**Collection frequency:** Daily, with 30-day lookback.

**Anti-gaming:** Cycles must span at least 2 distinct DACs. Self-looping (same BA creating proof, value, and connection) is excluded.

---

### 1.7 DAC Sovereignty Integrity (`σ_sovereign`)

**Definition:** Fraction of Business Accounts that retain full K2/K4 sovereignty without backend override.

**Telemetry sources:**
- `K2AttestationVerifiedEvent` — timestamp, ba_id, decision
- `K4ExitCompletedEvent` — timestamp, ba_id
- `BackendOverrideEvent` — timestamp, ba_id, override_type, reason
- `KeyCompromiseReportEvent` — timestamp, ba_id

**Computation:**
```python
total_bas = count(all active BAs)
overridden_bas = count(distinct ba_id in BackendOverrideEvent where override_type in ["k2_bypass", "k4_block", "key_recovery_without_consent"])
compromised_bas = count(distinct ba_id in KeyCompromiseReportEvent)
σ_sovereign = (total_bas - overridden_bas - compromised_bas) / total_bas
```

**Collection frequency:** Daily snapshot.

**Anti-gaming:** Overrides must be publicly logged with AXIOM case reference. Hidden overrides discovered by audit are counted retroactively and penalized 10×.

---

### 1.8 Innovation-to-Discipline Ratio (`ρ_id`)

**Definition:** Balance between new structural features and compliance with existing invariants.

**Telemetry sources:**
- `NewFeatureDeployedEvent` — timestamp, feature_id, vmnsk_layer
- `InvariantViolationEvent` — timestamp, invariant_id, feature_id (if linked)
- `VMOSKUpdateProposedEvent` — timestamp, layer, change_type
- `VMOSKUpdateRejectedEvent` — timestamp, layer, rejection_reason

**Computation:**
```python
innovation_score = count(NewFeatureDeployedEvent) + 0.5 * count(VMOSKUpdateProposedEvent)
discipline_penalty = count(InvariantViolationEvent) + 0.3 * count(VMOSKUpdateRejectedEvent)
ρ_id = innovation_score / (discipline_penalty + 1)
```

**Collection frequency:** Weekly.

**Anti-gaming:** Features must be in production >7 days to count. Invariant violations must be verified by automated tests or AXIOM.

---

## 2. Telemetry Architecture

### Event Bus

All PHI-meter telemetry flows through a dedicated **PhiEventBus**.

```python
class PhiEventBus:
    """Append-only event stream for PHI-meter indicators."""
    
    def emit(self, event: PhiEvent) -> None:
        # Write to append-only log
        # Trigger real-time indicator updates where applicable
        pass
    
    def query(self, event_type: str, window: TimeWindow) -> list[PhiEvent]:
        # Return events for batch computation
        pass
```

### Data Stores

| Store | Purpose | Retention |
|-------|---------|-----------|
| **PhiEventLog** | Append-only raw events | 90 days hot, 2 years cold |
| **PhiIndicatorCache** | Pre-computed indicator values | Latest value + 90-day history |
| **PhiSnapshotStore** | Periodic full-system snapshots | Weekly, indefinite |

### Computation Modes

| Indicator | Mode | Trigger |
|-----------|------|---------|
| `τ_error` | Real-time + daily batch | ErrorDetectedEvent, ErrorFixedEvent |
| `κ` | Weekly batch | Cron + manual refresh |
| `μ_seizure` | Daily batch | Cron |
| `λ_immune` | Real-time + daily batch | Anomaly events |
| `v_empty` | Weekly batch | Governance events |
| `f_loop` | Daily batch | Cron |
| `σ_sovereign` | Daily snapshot | Cron |
| `ρ_id` | Weekly batch | VMOSK events |

---

## 3. The Query Interface

### For Dashboards

```python
GET /phi/meter/latest
{
  "τ_error": { "value": 4.2, "unit": "hours", "trend": "improving" },
  "κ": { "value": 1.8, "unit": "value/complexity", "trend": "stable" },
  "μ_seizure": { "value": 72, "unit": "hours", "trend": "declining" },
  ...
}
```

### For Alerts

```python
POST /phi/meter/alert-rules
{
  "indicator": "σ_sovereign",
  "threshold": 0.95,
  "comparator": "<",
  "action": "notify_governance_channel"
}
```

### For Researchers

```python
GET /phi/meter/history?indicator=τ_error&from=2026-01-01&to=2026-04-01
{
  "data": [
    { "date": "2026-01-01", "value": 12.5 },
    ...
  ]
}
```

---

## 4. Anti-Gaming Architecture

Rule from `38_PHI_METER.md`: **Optimize an indicator → hide and revise it.**

### The Hiding Protocol

1. **Indicator masking:** If an agent or user starts gaming an indicator (detected by anomaly detection on the indicator's own time series), that indicator is **masked from public dashboards** for 30 days.
2. **Revision process:** During the masking period, the indicator definition is reviewed. Either:
   - The computation is hardened to remove the exploit.
   - The indicator is deprecated and replaced.
3. **Re-release:** After revision, the indicator returns with a new version number.

### Gaming detection heuristics

| Indicator | Gaming Signal |
|-----------|---------------|
| `τ_error` | Sudden drop in error detection without corresponding drop in actual bugs |
| `κ` | Spike in low-complexity proofs with negligible value |
| `μ_seizure` | Burst of trivial Warrant R oscillations |
| `λ_immune` | Self-reported anomalies with no actual graph changes |
| `v_empty` | Fake votes by sock-puppet DACs |
| `f_loop` | Artificially closed loops between colluding BAs |
| `σ_sovereign` | Hidden backend overrides not logged |
| `ρ_id` | Deployed features with no real usage |

### Governance of indicators

- **Proposal:** Any DAC can propose a new indicator or a revision.
- **Adoption:** Indicators become canonical when referenced in ≥3 independent DAC proof loops.
- **Deprecation:** An indicator is deprecated if `σ_sovereign` drops below 0.90 for 30 days (the organism is too compromised to measure itself honestly).

---

## 5. Privacy and Sovereignty

- **No biometric data** in PHI-meter telemetry.
- **No private messages** in PHI-meter telemetry.
- **BA identities** are pseudonymized in published indicator datasets.
- **Raw event logs** are access-controlled to the organism's audit nodes.
- **Counterparties** may query aggregate indicators but not per-BA breakdowns.

---

## 6. Integration with VMOSK×Cortex

- **VMOSK layer A** (Assets): Telemetry events include asset IDs.
- **VMOSK layer S** (Structures): Indicator definitions are versioned structures.
- **Cortex nervous system:** The `PhiEventBus` is a first-class packet producer. Cortex queries can join PHI-meter data with proof graphs, immune flags, and AXIOM outcomes.

Example Cortex query:
```sql
SELECT 
  f_loop.value AS loop_frequency,
  immune_flags.count AS immune_flags_7d,
  κ.value AS compression_rate
FROM phi_meter f_loop, immune_events, phi_meter κ
WHERE f_loop.date = immune_events.date
  AND κ.date = f_loop.date
  AND f_loop.value > 0.5
  AND immune_flags.count = 0
ORDER BY κ.value DESC;
```

This query finds high-synergy, low-conflict periods — the φ-inviting conditions.

---

## 7. Canonical Compression

> **The PHI-meter is a stethoscope, not a scoreboard. It listens to the organism's breath. If someone starts holding their breath to game the reading, the stethoscope moves to a different spot. The goal is not to maximize any number. The goal is to keep listening honestly.**

---

## 8. Cross-References

- `38_PHI_METER.md` — the eight indicators and their conceptual foundation
- `30_SYNERGY.md` — the loops that `f_loop` measures
- `35_IMMUNE_SYSTEM_ECONOMICS.md` — the immune system that `λ_immune` tracks
- `40_EMPTY_THRONE_GOVERNANCE.md` — the governance velocity that `v_empty` tracks
- `41_VMOSK_CORTEX_SYNTHESIS.md` — the query and nervous system layer
- `33_K2_INTELLIGENCE_NON_NEGOTIABLES.md` — the sovereignty that `σ_sovereign` guards

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning specification complete. Ready for event bus schema and indicator computation implementation.
2. **Your Next Action:** Produce or review a telemetry implementation handoff packet that names the event bus schema, the eight indicator computations, cadence expectations, and anti-gaming heuristics. Do not jump directly from UPLINK into code unless the active runtime state explicitly authorizes build work.
3. **Expected Output:** A handoff-ready telemetry plan, an indicator checklist, and a synthetic-test outline that a deeper implementation surface can execute without reopening the planning logic.
4. **Success Criteria:** Another engineer or agent can implement the PHI-meter event bus and indicator layer from the handoff packet alone, with gaming detection and masking rules preserved.
5. **Canonical Path:** `46_PHI_METER_TELEMETRY_PLAN.md` (this file).

---

> *Measure the garden, not the flower. If the flower is gamed, move the measuring stick.*  
> *eta = 0. K2 always.*
