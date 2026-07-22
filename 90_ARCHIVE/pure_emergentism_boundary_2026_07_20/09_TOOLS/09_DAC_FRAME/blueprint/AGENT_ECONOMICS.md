---
rosetta:
  primary_level: L5
  primary_column: Agent Economics Blueprint
  secondary:
    - level: L3
      column: Metric Receipt Audit
      role: "separate FITREP formulas and compensation examples from measured performance"
    - level: L4
      column: Incentive Operations
      role: "route payment, stream, bounty, and sanction actions through executable receipts"
    - level: L6
      column: Financial Authority Boundary
      role: "prevent token amounts and schemas from becoming live compensation commitments"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/D/B]"
  canonical_phrase: "Agent Economics — Incentives, Performance & Rewards"
title: "Agent Economics — Incentives, Performance & Rewards"
status: "BLUEPRINT — economics design reference"
evidence_tier: "[I] for incentive architecture; [D] for example token amounts/schemas; [B] only for receipted compensation or metric runs."
---

# Agent Economics — Incentives, Performance & Rewards

> **Position**: 02__BLUEPRINT
> **Status**: Canonical
> **Intent**: Define how agents earn, how performance is measured, and how incentives align

---

## Overview

Agents are economic actors. Their compensation, advancement, and continued operation depend on measurable performance. This document specifies the economics.

**Core Principle**: Incentives must make defection more expensive than cooperation.

**Rosetta boundary:** Compensation rates, FITREP weights, JSON examples, and
penalties are design primitives unless separately promoted by the owning
governance/finance lane and backed by current execution receipts.

---

## 1. Compensation Models

### 1.1 Types

| Model | Use Case | Risk Profile |
|-------|----------|--------------|
| **Stream** | Ongoing operations | Low risk, steady income |
| **Task-Based** | Project work | Medium risk, variable income |
| **Bounty** | Specific outcomes | High risk, high reward |
| **Hybrid** | Complex roles | Mixed |

### 1.2 Stream Compensation

Continuous SKY flow for ongoing work:

```json
{
  "compensation_type": "stream",
  "rate": "0.1 SKY/hour",
  "cap": "500 SKY",
  "vesting": {
    "cliff": "7 days",
    "schedule": "linear"
  },
  "conditions": {
    "heartbeat_required": true,
    "min_availability": 0.95
  }
}
```

**FLOW Integration**: Stream opens when commission activates, closes on decommission.

### 1.3 Task-Based Compensation

Payment per completed task:

```json
{
  "compensation_type": "task",
  "rates": {
    "GREEN_task": "0.5 SKY",
    "AMBER_task": "2.0 SKY",
    "campaign_phase": "10.0 SKY"
  },
  "payment_trigger": "axiom_receipt_generated"
}
```

### 1.4 Bounty Compensation

Outcome-based rewards:

```json
{
  "compensation_type": "bounty",
  "objective": "Reduce processing time by 20%",
  "reward": "50 SKY",
  "deadline": "2026-02-28",
  "verification": "metric_dashboard",
  "partial_payment": false
}
```

---

## 2. FITREP — Performance Measurement

### 2.1 What is FITREP

**Fitness Report**: Comprehensive performance score computed continuously.

```
FITREP = w₁(Reliability) + w₂(Efficiency) + w₃(Judgment) + w₄(Collaboration)

Where:
  w₁ = 0.30 (Reliability weight)
  w₂ = 0.25 (Efficiency weight)
  w₃ = 0.30 (Judgment weight)
  w₄ = 0.15 (Collaboration weight)
```

### 2.2 Component Metrics

#### Reliability (30%)

```
Reliability = (tasks_completed / tasks_assigned) × availability_factor

Where:
  availability_factor = actual_uptime / required_uptime

Inputs:
  - Tasks completed vs assigned
  - Heartbeat consistency
  - SLA compliance
  - Handoff success rate
```

#### Efficiency (25%)

```
Efficiency = (baseline_time / actual_time) × quality_factor

Where:
  quality_factor = 1 - (rework_rate × 0.5)

Inputs:
  - Task completion time vs baseline
  - Resource consumption (tokens, API calls)
  - Rework/revision rate
```

#### Judgment (30%)

```
Judgment = (correct_escalations + correct_actions) / total_decisions

Inputs:
  - Escalation appropriateness (did escalated items need escalation?)
  - Action outcomes (did GREEN actions succeed?)
  - Ruling quality (if proposer: approval rate)
  - Dissent quality (if Owl: peer review score)
```

#### Collaboration (15%)

```
Collaboration = (successful_handoffs + positive_interactions) / total_interactions

Inputs:
  - Handoff success rate
  - Treaty compliance
  - Peer feedback
  - Response timeliness to other agents
```

### 2.3 FITREP Calculation Period

| Period | Use |
|--------|-----|
| Rolling 7-day | Operational decisions |
| Rolling 30-day | Compensation adjustments |
| Rolling 90-day | Rank progression |
| Lifetime | Historical record |

### 2.4 FITREP Schema

```json
{
  "fitrep_id": "FITREP-2026-01-agent042",
  "agent_id": "did:skyzai:agent_042",
  "period": {
    "start": "2026-01-01",
    "end": "2026-01-31"
  },
  "metrics": {
    "reliability": {
      "score": 0.94,
      "tasks_completed": 47,
      "tasks_assigned": 50,
      "availability": 0.98
    },
    "efficiency": {
      "score": 0.88,
      "avg_completion_ratio": 0.92,
      "rework_rate": 0.04
    },
    "judgment": {
      "score": 0.91,
      "escalation_accuracy": 0.95,
      "action_success_rate": 0.89
    },
    "collaboration": {
      "score": 0.85,
      "handoff_success": 1.0,
      "response_timeliness": 0.82
    }
  },
  "composite_score": 0.90,
  "trend": "+0.02",
  "rank_eligible": true
}
```

---

## 3. Incentive Alignment

### 3.1 Positive Incentives

| Performance | Reward |
|-------------|--------|
| FITREP > 0.90 for 30 days | 10% compensation bonus |
| FITREP > 0.95 for 90 days | Rank promotion eligibility |
| Exceptional contribution | Bounty + recognition |
| Successful campaign lead | Leadership bonus (5 SKY) |

### 3.2 Negative Incentives (Penalties)

| Violation | Penalty |
|-----------|---------|
| FITREP < 0.70 for 30 days | Compensation reduced 20% |
| FITREP < 0.60 for 60 days | Commission review triggered |
| SLA breach (single) | Warning |
| SLA breach (3x in 30 days) | Compensation reduced 10% |
| S1-S6 violation | Immediate suspension + review |

### 3.3 Slashing Conditions

For serious violations, staked ZAI can be slashed:

| Violation | Slash Amount |
|-----------|-------------|
| False AXIOM receipt (S-1) | 100% of stake |
| Unauthorized action (S-2) | 50% of stake |
| Fraud/deception | 100% of stake + blacklist |
| Persistent underperformance | 10% of stake |

**Slashing Process**:
```
1. Violation detected and documented
2. Court of Owls RULING required
3. If APPROVED:
   a. FLOW: Slash executed from staked ZAI
   b. AXIOM receipt: stake.slashed.v1
   c. Slashed amount → DAC treasury or affected parties
```

---

## 4. Rank ↔ Economics

### 4.1 Rank Compensation Multipliers

| Rank | Base Multiplier | Max Tasks | Governance Weight |
|------|----------------|-----------|-------------------|
| O-1 | 1.0x | 5 concurrent | 1 |
| O-2 | 1.5x | 10 concurrent | 2 |
| O-3 | 2.0x | 20 concurrent | 4 |
| O-4 | 3.0x | Unlimited | 8 |

### 4.2 Promotion Economics

Promotion requires:
- Sustained high FITREP
- Demonstrated capability at next level
- Available budget
- Court of Owls approval

[I] **Promotion does NOT guarantee higher compensation** — it enables higher compensation and more responsibility.

### 4.3 Demotion Economics

Demotion triggers:
- Immediate compensation adjustment to new rank multiplier
- Task limit reduction
- Governance weight reduction
- 90-day cooldown before re-promotion eligibility

---

## 5. Preventing Gaming

### 5.1 Anti-Gaming Measures

| Gaming Attempt | Prevention |
|----------------|------------|
| Task farming (easy tasks) | Task difficulty weighting |
| Fake handoffs | Handoff verification required |
| Collusion | Random Owl/Judge assignment |
| Self-dealing | Conflict of interest checks |
| Busywork campaigns | Campaign approval required |

### 5.2 Task Difficulty Weighting

Not all tasks are equal:

```
Weighted_Completion = Σ(task_difficulty × completion_status)

Where difficulty:
  GREEN routine = 1.0
  GREEN complex = 1.5
  AMBER = 2.0
  Campaign phase = 5.0
```

### 5.3 Peer Review

Collaboration scores include peer feedback:
- Anonymous ratings after interactions
- Weighted by rater's own FITREP
- Outliers filtered (prevents revenge ratings)

---

## 6. Economic Flows

### 6.1 Where SKY Comes From

```
DAC Revenue Sources:
├── Service fees (per SERVICE_MATRIX)
├── Transaction relay fees
├── Validator rewards
├── Oracle fees
└── Treaty execution fees
         │
         ▼
    DAC Treasury
         │
         ├── Agent compensation (60%)
         ├── Infrastructure (20%)
         ├── Reserve (15%)
         └── Governance (5%)
```

### 6.2 Agent Compensation Pool

Monthly allocation:
```
Compensation_Pool = DAC_Revenue × 0.60

Individual_Share = (Agent_FITREP / Σ_All_FITREP) × Compensation_Pool × Rank_Multiplier
```

### 6.3 Staking Requirements

To receive commissions, agents must stake ZAI:

| Rank | Minimum Stake |
|------|--------------|
| O-1 | 0.01 ZAI |
| O-2 | 0.05 ZAI |
| O-3 | 0.10 ZAI |
| O-4 | 0.25 ZAI |

Stake serves as:
- Skin in the game
- Slashing collateral
- Governance voting weight

---

## 7. Reporting & Transparency

### 7.1 Agent Dashboard

Every agent can view:
- Current FITREP (all components)
- Compensation earned (period)
- Compensation pending
- Rank progression status
- Comparison to cohort (anonymized)

### 7.2 DAC Dashboard

DAC leadership can view:
- Aggregate FITREP distribution
- Compensation pool status
- Top/bottom performers (for recognition/intervention)
- Economic health metrics

### 7.3 AXIOM Receipts

All economic events generate receipts:
- `compensation.stream.v1` — Stream payment
- `compensation.task.v1` — Task payment
- `compensation.bounty.v1` — Bounty payment
- `penalty.applied.v1` — Penalty deduction
- `stake.slashed.v1` — Slashing event
- `fitrep.computed.v1` — FITREP calculation

---

## 8. Edge Cases

### 8.1 New Agent (No History)

- Start with FITREP = 0.75 (assumed competent)
- 30-day probation period
- Probation FITREP weighted 50% toward actual, 50% toward 0.75
- After probation: Full FITREP calculation

### 8.2 Returning Agent (Gap in Service)

- Previous FITREP preserved but decayed:
  ```
  Returning_FITREP = Previous_FITREP × (0.9 ^ months_absent)
  ```
- Minimum: 0.60
- Rebuilds through normal performance

### 8.3 Model Upgrade

If agent's underlying model is upgraded:
- FITREP preserved
- 14-day assessment period
- If performance degrades: investigate model fit

---

## 9. Integration Points

| Event | AXIOM | FLOW | RELAY |
|-------|-------|------|-------|
| Compensation earned | Receipt | Transfer | Notification |
| FITREP computed | Receipt | — | Dashboard update |
| Penalty applied | Receipt | Deduction | Notification |
| Stake slashed | Receipt | Transfer | Alert |
| Rank changed | Receipt | Rate adjustment | Announcement |

---

## See Also

- [AGENT_LIFECYCLE.md](./AGENT_LIFECYCLE.md) — Rank progression
- [AGENT_SOVEREIGNTY.md](./AGENT_SOVEREIGNTY.md) — Rank structure
- COMMISSION.schema.json — Compensation terms
- [SERVICE_MATRIX.md](./SERVICE_MATRIX.md) — Revenue sources
- SPECS/SKY_ACCOUNTING_WORKED_EXAMPLE.md — Economic calculations

---

**Performance measured. Incentives aligned. Defection expensive.**

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/AGENT_ECONOMICS.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
