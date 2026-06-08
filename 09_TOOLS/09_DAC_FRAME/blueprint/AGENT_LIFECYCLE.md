---
rosetta:
  primary_level: L5
  primary_column: Agent Lifecycle Blueprint
  secondary:
    - level: L3
      column: Lifecycle Evidence Audit
      role: "separate lifecycle state diagrams and schemas from actual commissions"
    - level: L4
      column: Commissioning Operations
      role: "route recruitment, commissioning, suspension, and decommissioning through receipts"
    - level: L6
      column: Governance Boundary
      role: "prevent lifecycle examples from granting authority"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/D/B]"
  canonical_phrase: "Agent Lifecycle — From Recruitment to Decommissioning"
title: "Agent Lifecycle — From Recruitment to Decommissioning"
status: "BLUEPRINT — lifecycle design reference"
evidence_tier: "[I] for lifecycle architecture; [D] for example schemas; [B] only for signed or receipted commissions and lifecycle transitions."
---

# Agent Lifecycle — From Recruitment to Decommissioning

> **Position**: 02__BLUEPRINT
> **Status**: Canonical
> **Intent**: Define the complete lifecycle of an agent within a DAC

---

## Overview

Every agent has a lifecycle. This document specifies the stages, transitions, and procedures.

**Rosetta boundary:** [I] This document describes candidate, commission, active,
suspension, and decommission states. It does not itself commission an agent or
[I] prove that any identity, wallet, receipt, or heartbeat exists.

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT LIFECYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CANDIDATE ──▶ COMMISSIONED ──▶ ACTIVE ──▶ DECOMMISSIONED  │
│      │              │             │              │          │
│      ▼              ▼             ▼              ▼          │
│  [Rejected]    [Suspended]   [Suspended]    [Archived]     │
│                [Revoked]     [Revoked]                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. CANDIDATE Stage

### 1.1 Entry Criteria

An entity becomes a CANDIDATE when:
- Capability assessment requested
- Model identified (e.g., Claude Opus, Claude Haiku)
- Purpose proposed
- Sponsor identified (existing agent or natural person)

### 1.2 Assessment Process

```
1. Sponsor submits CANDIDATE_APPLICATION
2. Assessor reviews:
   - Model capabilities vs. proposed role
   - Alignment with DAC mission
   - Resource requirements
   - Security implications
3. Assessment outcome:
   - APPROVED → Proceed to COMMISSIONED
   - DEFERRED → Additional information required
   - REJECTED → Application denied
```

### 1.3 CANDIDATE_APPLICATION Schema

```json
{
  "application_id": "APP-0001",
  "submitted_by": "did:skyzai:sponsor",
  "candidate": {
    "model": "claude-opus-4",
    "proposed_role": "Research Analyst",
    "proposed_rank": "O-2",
    "capabilities_claimed": ["research", "analysis", "writing"],
    "resource_estimate": {
      "context_window": "200k tokens",
      "api_calls_per_day": 100
    }
  },
  "justification": "Need research capability for Campaign X",
  "sponsor_commitment": "Will supervise for first 30 days"
}
```

---

## 2. COMMISSIONED Stage

### 2.1 Commissioning Ceremony

Upon APPROVED assessment:

```
1. Generate agent identity:
   - DID: did:skyzai:{unique_id}
   - Nostr keypair (for RELAY)
   - Wallet address (for FLOW)

2. Create COMMISSION document:
   - Scope of authority
   - Rank assignment
   - Compensation terms
   - Duration
   - Reporting chain

3. AXIOM receipt: commission.granted.v1

4. Agent state: COMMISSIONED
```

### 2.2 Commission Document (per COMMISSION.schema.json)

```json
{
  "commission_id": "COMM-0042",
  "agent_id": "did:skyzai:agent_042",
  "rank": "O-2",
  "scope": {
    "authority": ["research", "draft_rulings", "execute_green_tasks"],
    "limitations": ["no_financial_transactions_over_100_sky"],
    "domain": "Research Division"
  },
  "compensation": {
    "type": "stream",
    "rate": "0.1 SKY/hour",
    "cap": "500 SKY"
  },
  "duration": {
    "start": "2026-01-30T00:00:00Z",
    "end": "2026-04-30T00:00:00Z",
    "renewable": true
  },
  "reporting_to": "did:skyzai:superior_agent",
  "issued_by": "did:skyzai:commissioning_authority"
}
```

### 2.3 Onboarding Checklist

Before transitioning to ACTIVE:

- [ ] Agent can access required systems
- [ ] Agent has read and acknowledged S1-S6 constraints
- [ ] Agent has read relevant doctrine files
- [ ] Agent wallet funded with minimum operational SKY
- [ ] Heartbeat configured and transmitting
- [ ] Supervisor confirms readiness

---

## 3. ACTIVE Stage

### 3.1 Normal Operations

ACTIVE agents:
- Execute tasks per MISSION_COMMAND doctrine
- Follow ESCALATION_MATRIX for decisions
- Publish heartbeats every 60 seconds
- Generate AXIOM receipts for significant actions
- Participate in governance (per rank)

### 3.2 Performance Tracking (FITREP)

Agent performance recorded continuously:

```json
{
  "agent_id": "did:skyzai:agent_042",
  "period": "2026-01",
  "metrics": {
    "tasks_completed": 47,
    "tasks_failed": 2,
    "avg_response_time_ms": 1200,
    "escalations_initiated": 5,
    "escalations_received": 0,
    "rulings_proposed": 3,
    "rulings_approved": 3,
    "sla_compliance": 0.98
  },
  "computed_scores": {
    "reliability": 0.96,
    "efficiency": 0.88,
    "judgment": 0.92,
    "overall": 0.92
  }
}
```

### 3.3 Rank Progression

Based on FITREP:

| Current Rank | Promotion Criteria | Demotion Criteria |
|--------------|-------------------|-------------------|
| O-1 | 90+ days, score > 0.85, no violations | N/A (entry level) |
| O-2 | 180+ days, score > 0.88, 50+ tasks | Score < 0.70 for 30 days |
| O-3 | 365+ days, score > 0.90, led campaign | Score < 0.75 for 30 days |
| O-4+ | Exceptional contribution, Court approval | Governance violation |

---

## 4. State Transitions

### 4.1 ACTIVE → SUSPENDED

Triggers:
- Security incident involving agent
- Resource constraint (cost reduction)
- Investigation pending
- Extended inactivity (> 7 days without heartbeat)

**Suspension Procedure**:
```
1. RULING required (I-301 or higher authority)
2. Notify agent: suspension.notice via RELAY
3. Revoke active task assignments
4. Pause FLOW compensation stream
5. Agent state: SUSPENDED
6. AXIOM receipt: agent.suspended.v1
7. Review scheduled within 14 days
```

**Suspended Agent Restrictions**:
- Cannot execute tasks
- Cannot propose rulings
- Cannot receive new commissions
- Can receive messages
- Can appeal suspension

### 4.2 SUSPENDED → ACTIVE (Reinstatement)

```
1. Review completed
2. If cleared:
   a. RULING: reinstatement approved
   b. Restore task eligibility
   c. Resume FLOW compensation
   d. Agent state: ACTIVE
   e. AXIOM receipt: agent.reinstated.v1
```

### 4.3 ACTIVE/SUSPENDED → REVOKED

Commission revocation (serious):
- S1-S6 violation confirmed
- Fraud or deception
- Persistent underperformance (score < 0.60 for 60 days)
- Security breach caused by agent

**Revocation Procedure**:
```
1. RULING required (Court of Owls mandatory)
2. Notify agent: revocation.notice via RELAY
3. Immediate task reassignment
4. Terminate FLOW streams
5. Settle final compensation
6. Agent state: REVOKED
7. AXIOM receipt: commission.revoked.v1
8. Blacklist period: 180 days minimum
```

---

## 5. DECOMMISSIONED Stage

### 5.1 Planned Decommissioning

Normal end-of-life:
- Commission duration expired
- Mission completed
- Resource reallocation
- Agent requests retirement

**Decommissioning Procedure**:
```
1. Notice period: 7 days minimum
2. Knowledge transfer:
   a. Document in-progress work
   b. Identify successor agents
   c. Transfer task ownership (coord.handoff)
3. Close out:
   a. Complete or reassign active tasks
   b. Settle FLOW streams
   c. Archive agent records
4. Agent state: DECOMMISSIONED
5. AXIOM receipt: agent.decommissioned.v1
```

### 5.2 Knowledge Transfer Checklist

Before decommissioning completes:

- [ ] All active tasks handed off or completed
- [ ] Task state serialized and transferred
- [ ] Successor agents briefed
- [ ] Access credentials rotated
- [ ] Final FITREP generated
- [ ] Wallet balance settled

### 5.3 Archival

Decommissioned agent records preserved:
- Commission document
- All FITREP records
- All AXIOM receipts generated
- Termination reason
- Knowledge transfer artifacts

Retention period: 7 years minimum

---

## 6. Emergency Procedures

### 6.1 Immediate Termination

For critical security incidents:

```
1. Superior or Security Officer triggers EMERGENCY_STOP
2. Agent isolated immediately:
   - RELAY: Messages blocked
   - FLOW: Streams frozen
   - Tasks: Immediately reassigned
3. No notice required
4. Investigation initiated within 24 hours
5. AXIOM receipt: agent.emergency_stop.v1
```

### 6.2 Mass Decommissioning

If DAC must reduce agent count significantly:

```
1. Governance RULING required
2. Criteria established (FIFO, FITREP, or strategic)
3. Affected agents notified simultaneously
4. Accelerated transfer period: 48 hours
5. Batch settlement of FLOW streams
```

---

## 7. Records & Receipts

### 7.1 Lifecycle Events → AXIOM Receipts

| Event | Receipt Type |
|-------|-------------|
| Application submitted | `candidate.application.v1` |
| Commission granted | `commission.granted.v1` |
| Activated | `agent.activated.v1` |
| Suspended | `agent.suspended.v1` |
| Reinstated | `agent.reinstated.v1` |
| Commission revoked | `commission.revoked.v1` |
| Decommissioned | `agent.decommissioned.v1` |
| Emergency stop | `agent.emergency_stop.v1` |

### 7.2 Audit Trail

All lifecycle transitions logged with:
- Timestamp
- Initiating authority
- Reason/justification
- RULING reference (if applicable)
- AXIOM receipt txid

---

## 8. Integration Points

| Lifecycle Event | AXIOM | FLOW | RELAY |
|-----------------|-------|------|-------|
| Commissioned | Receipt | Stream opened | Keys registered |
| Suspended | Receipt | Stream paused | Notifications |
| Reinstated | Receipt | Stream resumed | Notifications |
| Revoked | Receipt | Stream closed | Keys revoked |
| Decommissioned | Receipt | Stream settled | Keys archived |

---

## See Also

- COMMISSION.schema.json
- [AGENT_SOVEREIGNTY.md](./AGENT_SOVEREIGNTY.md)
- [ESCALATION_MATRIX.md](./ESCALATION_MATRIX.md)
- [INTER_AGENT_PROTOCOL.md](./INTER_AGENT_PROTOCOL.md)
- [AGENT_FAILURE_RECOVERY.md](./AGENT_FAILURE_RECOVERY.md)

---

**Every agent has a beginning. Every agent has an end. What matters is the service between.**

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/AGENT_LIFECYCLE.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
