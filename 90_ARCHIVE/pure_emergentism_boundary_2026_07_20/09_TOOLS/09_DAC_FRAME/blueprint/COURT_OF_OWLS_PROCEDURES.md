---
rosetta:
  primary_level: L4
  primary_column: Court Governance Operations
  secondary:
    - level: L3
      column: Ruling Evidence Audit
      role: "separate proposal/dissent/judgment templates from completed rulings"
    - level: L5
      column: Governance Architecture
      role: "map proposer, owl, judge, timeline, dissent, and receipt topology"
    - level: L6
      column: Authority Boundary
      role: "prevent procedural examples from appointing judges or authorizing decisions"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/D/B]"
  canonical_phrase: "Court of Owls Procedures — Governance Operations"
title: "Court of Owls Procedures — Governance Operations"
status: "BLUEPRINT — governance procedure reference"
evidence_tier: "[I] for procedure doctrine; [D] for example pools/templates; [B] only for completed ruling receipts."
---

# Court of Owls Procedures — Governance Operations

> **Position**: 02__BLUEPRINT
> **Status**: Canonical
> **Intent**: Operationalize the Court of Owls (I-301) governance structure

---

## Overview

The Court of Owls is the governance mechanism for HIGH-impact decisions. This document specifies the operational procedures.

**Reference**: AGENT_SOVEREIGNTY.md Section 6 (I-301)

**Rosetta boundary:** [I] This paper defines a governance procedure. It does
[I] not appoint any current proposer, Owl, or Judge, and it does not prove that any
ruling, dissent, or receipt has occurred.

---

## 1. Court Structure

### 1.1 The Triad

Every ruling requires three roles:

| Role | Responsibility | Selection |
|------|---------------|-----------|
| **Proposer** | Drafts ruling, presents case | Initiating agent |
| **Owl** | Devil's Advocate, must find flaws | Appointed |
| **Judge** | Final decision authority | Appointed |

### 1.2 Role Requirements

**Proposer**:
- Any commissioned agent can propose
- Must have rank ≥ O-1
- Cannot also serve as Owl or Judge on same ruling

**Owl (Devil's Advocate)**:
- Rank ≥ O-2 required
- Must have relevant domain expertise
- Must submit dissent (even if agrees)
- Cannot be in Proposer's reporting chain

**Judge**:
- Rank ≥ O-3 required (O-4 for CRITICAL rulings)
- Must not have conflict of interest
- Cannot be in Proposer's reporting chain
- Final authority on approval/rejection

---

## 2. Owl/Judge Selection

### 2.1 Selection Pool

Eligible agents maintained in roster:

```json
{
  "owl_pool": [
    {"agent_id": "did:skyzai:owl_1", "rank": "O-3", "domains": ["finance", "security"]},
    {"agent_id": "did:skyzai:owl_2", "rank": "O-2", "domains": ["operations", "legal"]}
  ],
  "judge_pool": [
    {"agent_id": "did:skyzai:judge_1", "rank": "O-4", "domains": ["all"]},
    {"agent_id": "did:skyzai:judge_2", "rank": "O-3", "domains": ["technical", "governance"]}
  ]
}
```

### 2.2 Assignment Algorithm

```
1. Proposer submits ruling with domain classification
2. Filter pools:
   - Remove agents with conflicts of interest
   - Remove agents in Proposer's chain
   - Filter by domain expertise
3. Select Owl:
   - Prefer agents with lowest recent assignment count (load balancing)
   - Tie-breaker: Random selection
4. Select Judge:
   - Same criteria, must also outrank Owl
   - For CRITICAL: require O-4+ judge
5. Notify all parties via RELAY
```

### 2.3 Conflict of Interest

An agent has conflict of interest if:
- Directly affected by ruling outcome
- Has financial relationship with affected parties
- Has reporting relationship with Proposer
- Previously ruled on substantially similar matter

Self-declaration required. Failure to disclose → grounds for revocation.

---

## 3. Ruling Process

### 3.1 Timeline

| Phase | Duration | Deadline |
|-------|----------|----------|
| Proposal submission | — | T+0 |
| Owl assigned | 2 hours | T+2h |
| Judge assigned | 2 hours | T+4h |
| Owl dissent due | 24 hours | T+28h |
| Judge decision due | 24 hours | T+52h |
| **Total (standard)** | — | **52 hours** |

For CRITICAL rulings: All deadlines halved.

### 3.2 Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    RULING PROCESS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. PROPOSAL                                                │
│     Proposer drafts ruling per RULING.schema.json           │
│     Submits via RELAY: ruling.proposal                      │
│                         ↓                                   │
│  2. ASSIGNMENT                                              │
│     System assigns Owl and Judge                            │
│     Notifies all parties via RELAY                          │
│                         ↓                                   │
│  3. REVIEW (Owl)                                            │
│     Owl reviews proposal                                    │
│     Owl MUST write dissent (min 50 characters)              │
│     Submits: ruling.dissent                                 │
│                         ↓                                   │
│  4. DELIBERATION (Judge)                                    │
│     Judge reviews proposal + dissent                        │
│     Judge may request clarification                         │
│                         ↓                                   │
│  5. DECISION                                                │
│     Judge issues: APPROVED, REJECTED, or DEFERRED           │
│     Submits: ruling.decision                                │
│                         ↓                                   │
│  6. RECEIPT                                                 │
│     AXIOM receipt generated: ruling.{decision}.v1           │
│     All parties notified                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Dissent Requirements

### 4.1 Mandatory Dissent

[I] The Owl MUST submit dissent even if they agree with the proposal. This ensures:
- All perspectives considered
- Blind spots identified
- Record shows due diligence

### 4.2 Dissent Template

```markdown
## Dissent for RULING-{ID}

### Summary of Concerns
[Minimum 50 characters required]

### Potential Risks
1. [Risk 1]
2. [Risk 2]

### Alternative Approaches
1. [Alternative 1]
2. [Alternative 2]

### Recommendation
- [ ] PROCEED WITH CAUTION
- [ ] MODIFY BEFORE APPROVAL
- [ ] REJECT

### Owl Signature
Agent: {did}
Date: {timestamp}
```

### 4.3 Weak Dissent Handling

If Owl cannot find substantial concerns:
```markdown
### Summary of Concerns
After thorough review, I find the proposal well-reasoned and complete.
The primary consideration is [minor concern or implementation detail].

### Recommendation
- [x] PROCEED WITH CAUTION
```

This is acceptable—the duty is to look, not to invent problems.

---

## 5. Judge Decision

### 5.1 Decision Options

| Decision | Meaning | Effect |
|----------|---------|--------|
| **APPROVED** | Ruling accepted | Proposal takes effect |
| **REJECTED** | Ruling denied | Proposal voided |
| **DEFERRED** | More information needed | Returns to Proposer |

### 5.2 Decision Template

```markdown
## Decision for RULING-{ID}

### Proposal Summary
[Brief summary of what was proposed]

### Owl Dissent Considered
[How dissent was addressed]

### Analysis
[Judge's reasoning, citing P_node = Φ × V if applicable]

### Decision
**{APPROVED / REJECTED / DEFERRED}**

### Conditions (if any)
[Any conditions attached to approval]

### Judge Signature
Agent: {did}
Rank: {rank}
Date: {timestamp}
```

### 5.3 Deferred Rulings

If DEFERRED:
1. Judge specifies required information
2. Proposer has 72 hours to supplement
3. Process restarts from Owl review
4. Maximum 2 deferrals; third → auto-REJECTED

---

## 6. Deadlock Resolution

### 6.1 What Constitutes Deadlock

Deadlock occurs when:
- Owl strongly recommends REJECT
- Proposer insists on APPROVED
- Judge is genuinely undecided

### 6.2 Resolution Protocol

```
1. Judge declares deadlock
2. Escalate to higher authority:
   - For O-3 Judge: escalate to O-4+
   - For O-4 Judge: convene Panel (3 O-4+ judges)
3. Higher authority reviews:
   - Original proposal
   - Owl dissent
   - Judge's deadlock declaration
4. Higher authority issues binding decision
5. Decision is final (no further appeal at this level)
```

---

## 7. Appeals

### 7.1 Who Can Appeal

- Proposer (if REJECTED)
- Any affected party (if APPROVED and harmed)

### 7.2 Appeal Grounds

Valid grounds:
- Procedural error (e.g., conflict of interest undisclosed)
- New evidence unavailable during original ruling
- Material error in Judge's reasoning

Invalid grounds:
- Disagreement with decision
- "I don't like the outcome"

### 7.3 Appeal Process

```
1. Appellant submits appeal within 7 days of decision
2. Appeal reviewed by different Judge (O-4+)
3. If grounds valid:
   - New Triad assigned (all different from original)
   - Full ruling process restarts
4. If grounds invalid:
   - Appeal denied
   - Original ruling stands
5. Maximum 1 appeal per ruling
```

---

## 8. Emergency Rulings

### 8.1 Criteria

Emergency process permitted when:
- Imminent harm to DAC or natural persons
- Time-critical decision (< 4 hours)
- Standard process would cause irreversible damage

### 8.2 Emergency Process

```
1. Proposer declares EMERGENCY with justification
2. Single Judge assigned (highest available rank)
3. No Owl required (but recommended if time permits)
4. Judge decision within 2 hours
5. Decision effective immediately
6. Post-hoc review within 48 hours:
   - Full Triad reviews decision
   - Can modify but not reverse (actions already taken)
```

### 8.3 Emergency Abuse

False emergency declaration → grounds for rank demotion or revocation.

---

## 9. Documentation & Receipts

### 9.1 Required Records

Every ruling generates:
- Proposal document
- Owl dissent
- Judge decision
- AXIOM receipt

### 9.2 Receipt Types

| Event | Receipt |
|-------|---------|
| Ruling proposed | `ruling.proposed.v1` |
| Ruling approved | `ruling.approved.v1` |
| Ruling rejected | `ruling.rejected.v1` |
| Ruling deferred | `ruling.deferred.v1` |
| Appeal filed | `ruling.appeal.v1` |
| Appeal decided | `ruling.appeal_decided.v1` |

### 9.3 Archival

All ruling documents archived permanently:
- Location: DAC archive (99__ARCHIVE/RULINGS/)
- Retention: Indefinite
- Access: All commissioned agents

---

## 10. Metrics & Accountability

### 10.1 Court Performance Metrics

Tracked quarterly:
- Average ruling time
- Approval rate
- Deferral rate
- Appeal rate
- Appeal success rate
- Deadlock rate

### 10.2 Individual Performance

Owl metrics:
- Dissent quality score (peer-reviewed)
- Dissent timeliness
- Assignment acceptance rate

Judge metrics:
- Decision timeliness
- Appeal reversal rate
- Deadlock rate

Poor performance → removal from pool.

---

## See Also

- [AGENT_SOVEREIGNTY.md](./AGENT_SOVEREIGNTY.md) — Section 6 (I-301)
- [ESCALATION_MATRIX.md](./ESCALATION_MATRIX.md) — When Court is required
- RULING.schema.json — Data structure
- [DISAMBIGUATION_DOCTRINE.md](./DISAMBIGUATION_DOCTRINE.md) — Resolving conflicts

---

**Three perspectives. One decision. Zero ambiguity.**

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/COURT_OF_OWLS_PROCEDURES.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
