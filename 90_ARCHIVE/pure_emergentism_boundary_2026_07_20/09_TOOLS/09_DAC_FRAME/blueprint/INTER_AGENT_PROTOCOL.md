---
rosetta:
  primary_level: L5
  primary_column: Inter-Agent Protocol Architecture
  secondary:
    - level: L3
      column: Protocol Evidence Audit
      role: "separate schema examples, relay primitives, and SLA claims from deployed protocol receipts"
    - level: L4
      column: Coordination Operations
      role: "route requests, responses, handoffs, treaty execution, sync, heartbeat, and errors into receipted flows"
    - level: L6
      column: Runtime/Authority Boundary
      role: "prevent protocol examples from proving live messaging, signatures, relays, SLAs, or agent authority"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/D/B]"
  canonical_phrase: "Inter-Agent Protocol — Communication & Coordination"
title: "Inter-Agent Protocol — Communication & Coordination"
status: "BLUEPRINT — protocol-architecture reference"
evidence_tier: "[I] for protocol design; [D] for example payloads/SLA values; [B] only for deployed relay, signature, encryption, receipt, heartbeat, or treaty logs."
---

# Inter-Agent Protocol — Communication & Coordination

> **Position**: 02__BLUEPRINT
> **Status**: Canonical
> **Intent**: Define how agents communicate, coordinate, and execute treaties

---

## Overview

[I] Agents are autonomous but must coordinate. This protocol defines the message formats, routing rules, and coordination patterns for agent-to-agent communication.

**Rosetta boundary:** [I] This paper is protocol architecture. [D] JSON
payloads, SLA values, DID examples, relay references, and treaty examples are
not proof of live infrastructure. [B] Runtime claims require deployed relay,
signature, encryption, receipt, heartbeat, treaty, or log evidence.

**Transport**: RELAY primitive (Nostr)
**Encryption**: SPECTRE primitive (libsodium sealed boxes)
**Receipts**: AXIOM primitive (Arweave)

---

## 1. Message Types

### 1.1 Request-Response

| Type | Direction | Purpose |
|------|-----------|---------|
| `request.data` | A → B | Request information |
| `response.data` | B → A | Provide information |
| `request.action` | A → B | Request B perform action |
| `response.action` | B → A | Confirm action taken |
| `request.ruling` | A → Court | Request governance decision |
| `response.ruling` | Court → A | Deliver decision |

### 1.2 Notifications

| Type | Direction | Purpose |
|------|-----------|---------|
| `notify.status` | A → Subscribers | Status update |
| `notify.alert` | A → Relevant | Urgent notification |
| `notify.completion` | A → Stakeholders | Task completed |

### 1.3 Coordination

| Type | Direction | Purpose |
|------|-----------|---------|
| `coord.handoff` | A → B | Transfer responsibility |
| `coord.sync` | A ↔ B | Synchronize state |
| `coord.heartbeat` | A → Network | Prove liveness |

---

## 2. Message Format

[I] All messages follow this structure:

```json
{
  "protocol": "skyzai.inter_agent.v1",
  "id": "msg_uuid_here",
  "type": "request.data",
  "from": {
    "agent_id": "did:skyzai:alice",
    "npub": "npub1...",
    "rank": "O-2"
  },
  "to": {
    "agent_id": "did:skyzai:bob",
    "npub": "npub1..."
  },
  "payload": {
    // Type-specific content
  },
  "metadata": {
    "timestamp": "2026-01-30T12:00:00Z",
    "expires": "2026-01-30T12:05:00Z",
    "priority": "NORMAL",
    "encryption": "none|sealed_box",
    "reply_to": "msg_uuid_of_original"
  },
  "signature": "sig_hex_here"
}
```

---

## 3. Request-Response Protocol

### 3.1 Standard Request

```
Agent A                          Agent B
   │                                │
   │──── request.data ─────────────▶│
   │     (id: msg_001)              │
   │                                │
   │                          [Process]
   │                                │
   │◀──── response.data ────────────│
   │      (reply_to: msg_001)       │
   │                                │
```

### 3.2 Timeouts

| Priority | Timeout | Retry Count |
|----------|---------|-------------|
| CRITICAL | 30 seconds | 3 |
| HIGH | 60 seconds | 3 |
| NORMAL | 5 minutes | 2 |
| LOW | 30 minutes | 1 |

### 3.3 Timeout Handling

```
1. Send request with expires timestamp
2. Wait for response until expires
3. If no response:
   a. Retry up to retry_count times
   b. If still no response:
      - Log failure
      - Escalate if CRITICAL/HIGH priority
      - Mark agent B as potentially unavailable
```

---

## 4. Treaty Execution

[I] Treaties (per TREATY.schema.json) define ongoing agreements. This section specifies execution.

### 4.1 Treaty Lifecycle

```
┌──────────────────────────────────────────────────────┐
│                  TREATY LIFECYCLE                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  PROPOSED ──▶ NEGOTIATING ──▶ SIGNED ──▶ ACTIVE     │
│      │            │              │          │        │
│      ▼            ▼              ▼          ▼        │
│  [Rejected]   [Failed]      [Voided]   [Expired]    │
│                                         [Completed] │
│                                         [Breached]  │
└──────────────────────────────────────────────────────┘
```

### 4.2 Treaty Proposal

```json
{
  "type": "treaty.proposal",
  "payload": {
    "treaty_id": "TREATY-0001",
    "parties": ["did:skyzai:alice", "did:skyzai:bob"],
    "terms": {
      "alice_provides": "Data analysis service",
      "bob_provides": "0.5 SKY per analysis",
      "sla": {
        "response_time": "< 60 seconds",
        "availability": ">= 99%"
      },
      "duration": "30 days",
      "termination_notice": "7 days"
    }
  }
}
```

### 4.3 Treaty Signing

[I] Both parties sign:
1. Each party reviews terms
2. Each party signs treaty document
3. AXIOM receipt generated: `treaty.signed.v1`
4. Treaty enters ACTIVE state

### 4.4 SLA Monitoring

During ACTIVE state:
```
1. Each request logged with timestamp
2. Response time measured
3. Availability computed: (successful_responses / total_requests) * 100
4. If SLA breached:
   a. First breach: notify.alert to counterparty
   b. Second breach: notify.alert + request.remediation
   c. Third breach: treaty.breach_notice
```

### 4.5 Breach Handling

```json
{
  "type": "treaty.breach_notice",
  "payload": {
    "treaty_id": "TREATY-0001",
    "breaching_party": "did:skyzai:bob",
    "violations": [
      {"sla": "response_time", "required": "<60s", "actual": "120s", "count": 5}
    ],
    "remedy_requested": "Restore service within 24 hours",
    "escalation_deadline": "2026-01-31T12:00:00Z"
  }
}
```

If not remedied by deadline → Escalate to Court of Owls (RULING required)

---

## 5. Coordination Patterns

### 5.1 Task Handoff

When Agent A must transfer work to Agent B:

```json
{
  "type": "coord.handoff",
  "payload": {
    "task_id": "TASK-0042",
    "context": {
      "campaign_id": "CAMPAIGN-0001",
      "phase": 2,
      "progress": "Step 3 of 5 complete",
      "state": { /* Serialized task state */ }
    },
    "reason": "Context window exhausted",
    "deadline": "2026-01-30T14:00:00Z"
  }
}
```

**Handoff Protocol**:
```
1. Agent A serializes current state
2. Agent A sends coord.handoff to Agent B
3. Agent B acknowledges with coord.handoff_ack
4. Agent B resumes from state
5. Agent A generates AXIOM receipt: task.handoff.v1
6. Agent A terminates task ownership
```

### 5.2 State Synchronization

For agents maintaining shared state:

```json
{
  "type": "coord.sync",
  "payload": {
    "sync_id": "sync_uuid",
    "resource": "shared_ledger_X",
    "my_version": 42,
    "my_hash": "0xabc123...",
    "request": "compare"
  }
}
```

**Sync Protocol**:
```
1. Agent A sends coord.sync with version/hash
2. Agent B compares:
   - If match: respond with "in_sync"
   - If A ahead: respond with "request_update"
   - If B ahead: respond with delta
   - If diverged: respond with "conflict" + escalate
```

### 5.3 Heartbeat

[I] All active agents publish heartbeats:

```json
{
  "type": "coord.heartbeat",
  "payload": {
    "agent_id": "did:skyzai:alice",
    "status": "ACTIVE",
    "load": 0.7,
    "active_tasks": 3,
    "services": ["relay", "query", "validation"]
  }
}
```

**Heartbeat Rules**:
- Frequency: Every 60 seconds
- Missing 3 consecutive heartbeats → Agent marked UNAVAILABLE
- UNAVAILABLE agents excluded from new task assignments

---

## 6. Error Handling

### 6.1 Message Delivery Failure

| Failure | Recovery |
|---------|----------|
| Relay unavailable | Switch to fallback relay |
| Recipient offline | Queue message (max 24h) |
| Signature invalid | Reject, log, alert |
| Payload malformed | Reject with error response |

### 6.2 Error Response Format

```json
{
  "type": "error",
  "payload": {
    "code": "INVALID_SIGNATURE",
    "message": "Signature verification failed",
    "original_message_id": "msg_001",
    "recoverable": false
  }
}
```

### 6.3 Error Codes

| Code | Meaning | Recoverable |
|------|---------|-------------|
| `INVALID_SIGNATURE` | Sig verification failed | No |
| `MALFORMED_PAYLOAD` | JSON parse error | No |
| `UNKNOWN_TYPE` | Message type not recognized | No |
| `TIMEOUT` | Response not received in time | Yes (retry) |
| `UNAUTHORIZED` | Sender lacks permission | No |
| `UNAVAILABLE` | Recipient offline | Yes (queue) |
| `RATE_LIMITED` | Too many requests | Yes (backoff) |

---

## 7. Security

### 7.1 Authentication

[I] All messages must be signed:
1. Serialize payload to canonical JSON
2. Sign with agent's Ed25519 private key
3. Include signature in message
4. Recipient verifies against sender's known public key

### 7.2 Encryption (SPECTRE)

For CONFIDENTIAL or RESTRICTED messages:
```
1. Classify message per SPECTRE privacy levels
2. If encrypted:
   a. Retrieve recipient's Curve25519 public key
   b. Encrypt payload with sealed box
   c. Set metadata.encryption = "sealed_box"
3. Recipient decrypts before processing
```

### 7.3 Replay Prevention

Messages include:
- `id`: Unique UUID
- `timestamp`: Creation time
- `expires`: Validity window

[I] Recipients must:
- Reject messages with duplicate IDs
- Reject messages past expiry
- Reject messages with timestamp > 5 minutes in future

---

## 8. Implementation Notes

**Code Location**: `lib/features/nostr/` in Aureus codebase

**Key Classes**:
- `NostrRemoteDatasource` — Message sending/receiving
- `RelayServiceManager` — Relay connection management
- `NostrEncoderService` — Message encoding

**Integration Points**:
- RELAY: All messages routed through Nostr relays
- SPECTRE: Encryption via `crypto.box.seal`
- AXIOM: Significant interactions generate receipts

---

## See Also

- RELAY Primitive
- SPECTRE Primitive
- TREATY.schema.json
- [ESCALATION_MATRIX.md](./ESCALATION_MATRIX.md)
- PRIMITIVE_INTEGRATION.md

---

**Communication is coordination. Coordination is [I] power.**

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/INTER_AGENT_PROTOCOL.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
