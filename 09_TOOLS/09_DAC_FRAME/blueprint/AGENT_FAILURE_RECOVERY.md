---
rosetta:
  primary_level: L4
  primary_column: Agent Recovery Operations
  secondary:
    - level: L3
      column: Recovery Receipt Audit
      role: "require checkpoint, heartbeat, handoff, and recovery receipts before runtime claims"
    - level: L5
      column: Recovery Architecture
      role: "map state persistence, failure classes, recovery flows, and escalation"
    - level: L6
      column: State Authority Boundary
      role: "prevent schemas/examples from becoming deployed state-store truth"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/D/B]"
  canonical_phrase: "Agent Failure Recovery — State Persistence & Resumption"
title: "Agent Failure Recovery — State Persistence & Resumption"
status: "BLUEPRINT — recovery design reference"
evidence_tier: "[I] for recovery doctrine; [D] for example APIs/schemas; [B] only for tested recovery receipts."
---

# Agent Failure Recovery — State Persistence & Resumption

> **Position**: 02__BLUEPRINT
> **Status**: Canonical
> **Intent**: Define how agents persist state and recover from failures

---

## Overview

Agents fail. Context windows exhaust. Connections drop. This document specifies how to persist state and resume work without loss.

**Principle**: No single agent failure should cause mission failure.

**Rosetta boundary:** [I] This paper defines recovery logic. It does not prove
that heartbeat monitors, checkpoint APIs, state stores, or AXIOM receipts are
live in a deployed DAC without a fresh runtime receipt.

---

## 1. Failure Modes

### 1.1 Classification

| Mode | Cause | Severity | Recovery Time |
|------|-------|----------|---------------|
| **Context Exhaustion** | Token limit reached | LOW | Immediate (handoff) |
| **Connection Loss** | Network failure | MEDIUM | Minutes |
| **Agent Crash** | Runtime error | MEDIUM | Minutes to hours |
| **Model Unavailable** | API outage | HIGH | Hours |
| **Corruption** | State inconsistency | CRITICAL | Manual intervention |

### 1.2 Detection

Failures detected via:
- Missing heartbeat (3 consecutive = UNAVAILABLE)
- Error response to request
- Timeout on in-progress task
- Self-reported failure notice

---

## 2. State Persistence

### 2.1 What to Persist

Every agent maintains persistent state:

```json
{
  "agent_state": {
    "agent_id": "did:skyzai:agent_042",
    "version": 1234,
    "timestamp": "2026-01-30T12:00:00Z",

    "active_tasks": [
      {
        "task_id": "TASK-0042",
        "campaign_id": "CAMPAIGN-0001",
        "phase": 2,
        "step": 3,
        "started_at": "2026-01-30T11:00:00Z",
        "checkpoint": {
          "completed_steps": [1, 2],
          "current_step_progress": 0.6,
          "intermediate_results": { /* ... */ }
        }
      }
    ],

    "pending_messages": [
      {"id": "msg_001", "type": "request.data", "status": "awaiting_response"}
    ],

    "context_summary": {
      "recent_decisions": ["Approved X", "Escalated Y"],
      "learned_context": ["Project Z uses framework W"],
      "key_relationships": ["Reports to Agent A", "Collaborates with Agent B"]
    }
  }
}
```

### 2.2 Persistence Frequency

| Trigger | Action |
|---------|--------|
| Task step completed | Checkpoint state |
| Decision made | Checkpoint + AXIOM receipt |
| Every 5 minutes | Background checkpoint |
| Context 80% full | Mandatory checkpoint + prepare handoff |
| Error detected | Emergency checkpoint |

### 2.3 Storage

State persisted to:
1. **Local**: Agent's working memory (ephemeral)
2. **Remote**: DAC state store (durable)
3. **Permanent**: AXIOM receipts for significant events

---

## 3. Checkpoint Protocol

### 3.1 Standard Checkpoint

```
1. Serialize current state to JSON
2. Compute state hash
3. Upload to DAC state store:
   PUT /agents/{agent_id}/state
   {
     "version": {new_version},
     "state": {serialized_state},
     "hash": {state_hash}
   }
4. Log checkpoint event
```

### 3.2 Checkpoint Schema

```json
{
  "checkpoint_id": "ckpt_uuid",
  "agent_id": "did:skyzai:agent_042",
  "version": 1234,
  "timestamp": "2026-01-30T12:00:00Z",
  "trigger": "step_completed|scheduled|context_warning|error",
  "state_hash": "0xabc123...",
  "state_size_bytes": 4096,
  "tasks_in_progress": 2,
  "resumable": true
}
```

---

## 4. Recovery Procedures

### 4.1 Self-Recovery (Context Exhaustion)

When agent detects context approaching limit:

```
1. Agent computes: remaining_context < 20%
2. Agent initiates GRACEFUL_HANDOFF:
   a. Checkpoint current state
   b. Summarize context for successor
   c. Identify handoff target (same agent type, or specific successor)
   d. Send coord.handoff message
   e. Wait for handoff_ack
   f. Generate AXIOM receipt: task.handoff.v1
   g. Terminate gracefully
3. Successor agent:
   a. Receives coord.handoff
   b. Loads state from checkpoint
   c. Resumes from last completed step
   d. Sends handoff_ack
```

### 4.2 Assisted Recovery (Crash/Disconnect)

When external monitor detects agent failure:

```
1. Monitor detects: 3 missed heartbeats
2. Monitor marks agent UNAVAILABLE
3. Monitor identifies recovery agent:
   - Same model preferred
   - Same or higher rank required
   - Available capacity confirmed
4. Monitor sends recovery.assign to recovery agent
5. Recovery agent:
   a. Fetches last checkpoint from state store
   b. Loads state
   c. Resumes in-progress tasks
   d. Notifies stakeholders
   e. Generates AXIOM receipt: task.recovered.v1
```

### 4.3 Manual Recovery (Corruption)

When state is inconsistent or corrupted:

```
1. Corruption detected (hash mismatch, schema violation)
2. Escalate to O-4+ authority
3. Authority reviews:
   - Last known good checkpoint
   - AXIOM receipts for recent actions
   - Task requirements
4. Authority decides:
   - ROLLBACK: Restore from earlier checkpoint
   - RECONSTRUCT: Manually rebuild state from receipts
   - ABORT: Cancel affected tasks, reassign fresh
5. Generate AXIOM receipt: state.manual_recovery.v1
```

---

## 5. Task Handoff Protocol

### 5.1 Handoff Message

```json
{
  "type": "coord.handoff",
  "payload": {
    "handoff_id": "handoff_uuid",
    "from_agent": "did:skyzai:agent_042",
    "to_agent": "did:skyzai:agent_043",
    "reason": "context_exhaustion|scheduled|failure_recovery",

    "task": {
      "task_id": "TASK-0042",
      "campaign_id": "CAMPAIGN-0001",
      "phase": 2,
      "step": 3,
      "checkpoint_version": 1234
    },

    "context_summary": {
      "what_was_done": "Completed steps 1-2, step 3 is 60% done",
      "current_state": "Analyzing dataset X, found patterns A, B, C",
      "next_action": "Complete pattern analysis, then write report",
      "key_decisions": ["Used method Y because of constraint Z"],
      "blockers": ["Waiting for response from Agent B (msg_001)"]
    },

    "state_location": "/agents/agent_042/checkpoints/1234",
    "deadline": "2026-01-30T14:00:00Z"
  }
}
```

### 5.2 Handoff Acceptance

Receiving agent must:
1. Verify checkpoint is loadable
2. Confirm capacity to complete task
3. Respond with handoff_ack or handoff_reject

```json
{
  "type": "coord.handoff_ack",
  "payload": {
    "handoff_id": "handoff_uuid",
    "accepted": true,
    "estimated_completion": "2026-01-30T13:30:00Z",
    "questions": []
  }
}
```

### 5.3 Handoff Rejection

If receiving agent cannot accept:

```json
{
  "type": "coord.handoff_reject",
  "payload": {
    "handoff_id": "handoff_uuid",
    "reason": "insufficient_capacity|incompatible_task|checkpoint_corrupted",
    "alternative_suggestion": "did:skyzai:agent_044"
  }
}
```

System then attempts handoff to alternative.

---

## 6. Context Compression

### 6.1 When to Compress

Before handoff, compress context to essential information:

```
Full context: 180,000 tokens
Compressed summary: 5,000 tokens
```

### 6.2 Compression Template

```markdown
## Task Context Summary

### Objective
[1-2 sentences: What are we trying to accomplish?]

### Progress
- Completed: [List completed steps]
- Current: [Current step and progress %]
- Remaining: [List remaining steps]

### Key Decisions Made
1. [Decision 1 and rationale]
2. [Decision 2 and rationale]

### Important Context
- [Critical fact 1]
- [Critical fact 2]
- [Critical fact 3]

### Pending Items
- [Awaiting response from X]
- [Blocked on Y]

### Files/Resources
- [Key file 1]: [Brief description]
- [Key file 2]: [Brief description]

### Warnings
- [Any known issues or gotchas]
```

### 6.3 What NOT to Compress

Preserve exactly (do not summarize):
- Code that was written
- Exact error messages
- Specific numbers/metrics
- Literal quotes from sources
- Schema definitions

---

## 7. Failure Cascades

### 7.1 Prevention

Prevent single failure from cascading:
- No task depends on single agent
- Critical tasks have designated backup agents
- Campaigns have contingency phases

### 7.2 Circuit Breaker

If multiple agents fail simultaneously:

```
1. Detect: > 3 agents UNAVAILABLE within 5 minutes
2. Trigger: CIRCUIT_BREAKER
3. Actions:
   a. Pause new task assignments
   b. Alert O-4+ authority
   c. Assess scope of failure
   d. Determine if systemic (infrastructure) vs coincidental
4. If systemic: EMERGENCY procedures
5. If coincidental: Resume normal operations
```

---

## 8. Recovery Metrics

### 8.1 SLAs

| Metric | Target |
|--------|--------|
| Time to detect failure | < 3 minutes |
| Time to assign recovery agent | < 5 minutes |
| Time to resume task | < 15 minutes |
| State loss (steps) | < 1 step |
| Task completion rate after recovery | > 95% |

### 8.2 Tracking

Every recovery generates:
- Recovery time metrics
- State loss assessment
- Root cause classification
- AXIOM receipt

---

## 9. Integration Points

| Event | AXIOM | FLOW | RELAY |
|-------|-------|------|-------|
| Checkpoint | — | — | — |
| Handoff initiated | — | Pause stream | coord.handoff |
| Handoff accepted | task.handoff.v1 | Transfer stream | handoff_ack |
| Recovery complete | task.recovered.v1 | Resume stream | notify.status |
| Manual recovery | state.manual_recovery.v1 | Reconcile | notify.alert |

---

## 10. Runbook

### Quick Reference: Agent Down

```
1. Confirm failure (check heartbeat, try ping)
2. If recoverable:
   a. Fetch last checkpoint
   b. Assign recovery agent
   c. Execute handoff
   d. Verify task resumed
3. If not recoverable:
   a. Escalate to O-4+
   b. Consider manual recovery
   c. Document incident
4. Generate postmortem if significant
```

---

## See Also

- [INTER_AGENT_PROTOCOL.md](./INTER_AGENT_PROTOCOL.md) — coord.handoff messages
- [AGENT_LIFECYCLE.md](./AGENT_LIFECYCLE.md) — Agent states
- [ESCALATION_MATRIX.md](./ESCALATION_MATRIX.md) — When to escalate
- [HOLOGRAPHIC_DOCTRINE.md](./HOLOGRAPHIC_DOCTRINE.md) — Reconstruction principle

---

**Failure is expected. Loss is not. Checkpoint early, checkpoint often.**

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/AGENT_FAILURE_RECOVERY.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
