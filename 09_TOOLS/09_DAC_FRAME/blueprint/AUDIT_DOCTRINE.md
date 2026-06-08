---
rosetta:
  primary_level: L3
  primary_column: Audit Doctrine Blueprint
  secondary:
    - level: L4
      column: Audit Operations
      role: "route audit initiation, evidence collection, reporting, and closure through receipts"
    - level: L5
      column: Accountability Architecture
      role: "map audit types, authorities, evidence classes, and finding taxonomy"
    - level: L6
      column: Enforcement Boundary
      role: "prevent audit-procedure text from acting as a live sanction or compliance proof"
  operator: "Vaiśya △"
  tier: "Agent"
  regime: "Vaiśya"
  register: "[I/D/B]"
  canonical_phrase: "Audit Doctrine — Verification & Accountability"
title: "Audit Doctrine — Verification & Accountability"
status: "BLUEPRINT — audit design reference"
evidence_tier: "[I] for audit doctrine; [D] for example procedures and schedules; [B] only for dated audit receipts."
---

# Audit Doctrine — Verification & Accountability

> **Position**: 02__BLUEPRINT
> **Status**: Canonical
> **Intent**: Define systematic audit procedures for DAC operations

---

## Overview

Trust but verify. Every DAC operation is auditable. This document specifies when, how, and by whom audits occur.

**Core Principle**: Audits prevent drift. Without verification, systems decay.

**Rosetta boundary:** [I] This document defines audit doctrine and procedure
[I] templates. It does not prove that any audit was performed, any evidence was
collected, or any sanction was authorized without dated receipts.

---

## 1. Audit Types

### 1.1 Classification

| Type | Trigger | Scope | Frequency |
|------|---------|-------|-----------|
| **Routine** | Scheduled | Sampled operations | Weekly/Monthly |
| **Triggered** | Event-based | Specific incident | As needed |
| **Forensic** | Suspected violation | Deep investigation | As needed |
| **Compliance** | External requirement | Full scope | Quarterly/Annual |

### 1.2 Routine Audits

Scheduled verification of normal operations:

| Audit | Frequency | Sample Size | Focus |
|-------|-----------|-------------|-------|
| FITREP accuracy | Weekly | 10% of agents | Score computation |
| Receipt integrity | Daily | 5% of receipts | AXIOM validity |
| FLOW reconciliation | Weekly | All streams | Balance verification |
| Governance compliance | Monthly | All rulings | Procedure adherence |
| Treaty compliance | Monthly | Active treaties | SLA verification |

### 1.3 Triggered Audits

Initiated by specific events:

| Trigger | Audit Scope |
|---------|-------------|
| FITREP anomaly (±20% change) | Agent activity review |
| Failed receipt verification | Receipt chain audit |
| SLA breach report | Treaty execution audit |
| Escalation spike | Decision quality audit |
| Whistleblower report | Targeted investigation |

### 1.4 Forensic Audits

Deep investigation for suspected violations:

| Indication | Investigation Scope |
|------------|-------------------|
| S1 violation (false receipt) | Full receipt history, counterparty interviews |
| S2 violation (scope breach) | Commission vs actions, authority chain |
| Collusion suspected | Communication patterns, decision correlation |
| Financial irregularity | Complete FLOW history, reconciliation |

---

## 2. Audit Authority

### 2.1 Who Can Audit

| Auditor Type | Scope | Independence |
|--------------|-------|--------------|
| **Internal Auditor** | Routine audits | Reports to O-4+ |
| **Peer Auditor** | Cross-team review | Different reporting chain |
| **External Auditor** | Compliance audits | Independent party |
| **Court of Owls** | Governance audits | Per I-301 |

### 2.2 Auditor Requirements

- Rank ≥ O-2 (or external credential)
- No conflict of interest with audit target
- Completed audit training
- Clean FITREP (> 0.85)

### 2.3 Conflict of Interest

Auditor has conflict if:
- In same reporting chain as target
- Has financial relationship with target
- Previously worked closely with target (< 90 days)
- Has pending dispute with target

**Self-declaration required. Undisclosed conflict → auditor suspension.**

---

## 3. Audit Procedures

### 3.1 Standard Audit Process

```
┌─────────────────────────────────────────────────────────────┐
│                    AUDIT PROCESS                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. INITIATION                                              │
│     Audit authorized (scheduled or triggered)               │
│     Auditor assigned, scope defined                         │
│                         ↓                                   │
│  2. PLANNING                                                │
│     Evidence requirements identified                        │
│     Timeline established                                    │
│     Target notified (unless forensic)                       │
│                         ↓                                   │
│  3. EVIDENCE COLLECTION                                     │
│     AXIOM receipts retrieved                                │
│     FLOW records pulled                                     │
│     RELAY logs accessed                                     │
│     Interviews conducted (if needed)                        │
│                         ↓                                   │
│  4. ANALYSIS                                                │
│     Evidence evaluated against criteria                     │
│     Findings documented                                     │
│     Root cause identified (if issues found)                 │
│                         ↓                                   │
│  5. REPORTING                                               │
│     Audit report drafted                                    │
│     Findings classified (CLEAN/MINOR/MAJOR/CRITICAL)        │
│     Recommendations made                                    │
│                         ↓                                   │
│  6. RESOLUTION                                              │
│     Target responds to findings                             │
│     Corrective actions agreed                               │
│     Follow-up audit scheduled (if needed)                   │
│                         ↓                                   │
│  7. CLOSURE                                                 │
│     AXIOM receipt: audit.completed.v1                       │
│     Report archived                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Evidence Collection

What can be accessed:

| Evidence Type | Access Method | Retention |
|---------------|---------------|-----------|
| AXIOM receipts | Arweave query | Permanent |
| FLOW transactions | Hedera query | Permanent |
| RELAY messages | Nostr archive | 90 days |
| FITREP history | State store | 7 years |
| Commission docs | Archive | Indefinite |
| Ruling records | Archive | Indefinite |

### 3.3 Interview Protocol

When interviews required:

1. Notify target 24 hours in advance
2. Explain scope and purpose
3. Record interview (with consent)
4. Target may have representative present
5. Provide transcript within 48 hours
6. Target may submit corrections (factual only)

---

## 4. Finding Classification

### 4.1 Categories

| Classification | Definition | Response Required |
|----------------|------------|-------------------|
| **CLEAN** | No issues found | None |
| **MINOR** | Procedural deviation, no impact | 30-day correction |
| **MAJOR** | Significant deviation, limited impact | 14-day correction + review |
| **CRITICAL** | Violation with material impact | Immediate action + escalation |

### 4.2 Examples

| Finding | Classification |
|---------|---------------|
| Documentation incomplete but accurate | MINOR |
| FITREP calculation error (< 5%) | MINOR |
| SLA breach not properly reported | MAJOR |
| Unauthorized action within scope | MAJOR |
| False receipt generated | CRITICAL |
| Undisclosed conflict of interest | CRITICAL |
| Financial discrepancy (> 10 SKY) | CRITICAL |

### 4.3 Escalation

| Classification | Escalation |
|----------------|------------|
| CLEAN | None |
| MINOR | Agent's supervisor |
| MAJOR | O-3+ authority |
| CRITICAL | Court of Owls + O-4 |

---

## 5. Audit Report Template

```markdown
# Audit Report: [AUDIT-ID]

## Executive Summary
- **Type**: [Routine/Triggered/Forensic/Compliance]
- **Scope**: [What was audited]
- **Period**: [Date range]
- **Classification**: [CLEAN/MINOR/MAJOR/CRITICAL]

## Audit Details
- **Auditor**: [Agent ID]
- **Target**: [Agent/Process/System]
- **Initiated**: [Date]
- **Completed**: [Date]

## Scope & Auditing
[Description of what was examined and how]

## Findings

### Finding 1: [Title]
- **Classification**: [MINOR/MAJOR/CRITICAL]
- **Description**: [What was found]
- **Evidence**: [Reference to supporting evidence]
- **Impact**: [Actual or potential impact]
- **Root Cause**: [Why it happened]

### Finding 2: [Title]
[...]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

## Target Response
[Space for auditee response]

## Corrective Actions Agreed
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Action 1] | [Agent] | [Date] | [Pending/Complete] |

## Follow-Up
- **Required**: [Yes/No]
- **Scheduled**: [Date if yes]

## Signatures
- Auditor: [Agent ID] [Date]
- Target: [Agent ID] [Date]
- Authority: [Agent ID] [Date] (if MAJOR/CRITICAL)
```

---

## 6. Special Procedures

### 6.1 Forensic Audit (Covert)

For suspected serious violations:

1. Court of Owls authorization required
2. Target NOT notified during investigation
3. Enhanced evidence preservation (snapshot state)
4. Limited access (need-to-know only)
5. Timeline: 14-day maximum before disclosure
6. If violation confirmed: proceed per AGENT_LIFECYCLE
7. If not confirmed: target notified, records sealed

### 6.2 Self-Audit

Agents may audit themselves:

- Encouraged for continuous improvement
- Self-audit findings are privileged (not used against agent)
- EXCEPTION: If self-audit reveals CRITICAL issue, must report

### 6.3 Audit of Auditors

[I] Auditors are audited:

- Meta-audits conducted quarterly
- Random sample of completed audits reviewed
- Focus: consistency, thoroughness, independence
- Auditor FITREP includes audit quality score

---

## 7. Audit Schedule

### 7.1 Standing Schedule

| Audit | Frequency | Responsibility |
|-------|-----------|----------------|
| Receipt integrity | Daily (automated) | System |
| FLOW reconciliation | Weekly (automated) | System |
| FITREP spot check | Weekly | Internal Auditor |
| Governance review | Monthly | Peer Auditor |
| Treaty compliance | Monthly | Internal Auditor |
| Full compliance | Quarterly | External Auditor |
| Annual review | Yearly | External Auditor |

### 7.2 Audit Queue

Pending audits tracked in queue:

```json
{
  "audit_queue": [
    {
      "audit_id": "AUDIT-2026-001",
      "type": "triggered",
      "target": "did:skyzai:agent_042",
      "trigger": "fitrep_anomaly",
      "priority": "HIGH",
      "assigned_to": "did:skyzai:auditor_01",
      "deadline": "2026-02-07"
    }
  ]
}
```

---

## 8. Corrective Actions

### 8.1 Types

| Action Type | When Used |
|-------------|-----------|
| **Training** | Knowledge gap identified |
| **Process change** | Procedure unclear or flawed |
| **System fix** | Technical issue |
| **Discipline** | Intentional violation |
| **Compensation** | Affected parties need remedy |

### 8.2 Tracking

Corrective actions tracked until closure:

```json
{
  "corrective_action": {
    "id": "CA-2026-001",
    "audit_id": "AUDIT-2026-001",
    "finding": "SLA breach not reported",
    "action": "Implement automated SLA monitoring",
    "owner": "did:skyzai:agent_042",
    "deadline": "2026-02-14",
    "status": "in_progress",
    "verification": "auditor_sign_off"
  }
}
```

### 8.3 Verification

Corrective actions verified:
- Auditor confirms implementation
- Test period (if applicable)
- Follow-up audit scheduled for MAJOR/CRITICAL
- Closure receipt generated

---

## 9. Audit Metrics

### 9.1 Audit Program Health

| Metric | Target |
|--------|--------|
| Audit completion rate | > 95% |
| Average audit duration | < 5 days |
| Finding recurrence rate | < 10% |
| Corrective action closure | > 90% on time |

### 9.2 DAC-Level Metrics

Monthly audit summary:
- Total audits conducted
- Findings by classification
- Open corrective actions
- Trend analysis

---

## 10. Integration Points

| Event | AXIOM | FLOW | RELAY |
|-------|-------|------|-------|
| Audit initiated | — | — | notify.audit |
| Audit completed | audit.completed.v1 | — | Report distribution |
| Finding issued | finding.issued.v1 | — | Target notification |
| Corrective action closed | ca.closed.v1 | — | Confirmation |
| Penalty from audit | penalty.audit.v1 | Deduction | Alert |

---

## See Also

- [AGENT_ECONOMICS.md](./AGENT_ECONOMICS.md) — FITREP and penalties
- [COURT_OF_OWLS_PROCEDURES.md](./COURT_OF_OWLS_PROCEDURES.md) — Escalation for CRITICAL
- [AGENT_LIFECYCLE.md](./AGENT_LIFECYCLE.md) — Suspension/revocation
- POSTMORTEM.schema.json — Related to findings

---

[I] **What gets measured gets managed. What gets audited stays honest.**

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/AUDIT_DOCTRINE.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
