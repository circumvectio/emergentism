---
type: coordination-protocol
evidence-tier: [T] — Technical specification.
date: 2026-05-04
status: ACTIVE — Phase 0 operational protocol
rosetta:
  primary_level: L5
  primary_column: Agent Coordination
  secondary:
    - level: L4
      column: Agent Execution
      role: "own commit/refuse/escalate handoffs and K2 acceptance cards"
    - level: L3
      column: Agent Audit
      role: "rank conflicts, ties, and evidence packets before execution"
    - level: L6
      column: Agent Compression
      role: "prune overgrown sessions and surface pathology flags"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[T/S]"
  canonical_phrase: "Inter-Agent Coordination Protocol"
title: "Inter-Agent Coordination Protocol"
evidence_tier: "[T] technical coordination protocol; [S] structural Rosetta handoff map."
---


# Inter-Agent Coordination Protocol

> How the seven Rosetta castes work together in multi-agent sessions. This is the practical orchestration layer above individual agent runbooks.

---

## 1. Session Types

| Type | Description | Castes Involved | Frequency |
|---|---|---|---|
| **Three-Stage Process Breath** | Routine execution: perceive → explore → rank → execute | L1 → L2 → L3 → L4 | ~95% of sessions |
| **Architectural Ascent** | Deadlock requires redesign | L4 → L5 → L4* | ~4% of sessions |
| **Compression Cycle** | Continuous pruning (parallel to breath) | L6 (continuous) | Runs constantly |
| **Constitutional Moment** | Framework boundary touched | L4 → L7 → L4* | ~1% of sessions |
| **Full Council** | Complex multi-domain question | L1+L2+L3+L4+L5+L6+L7 | Rare; crisis or major decision |
| **Mirror Pair** | Symmetric caste collaboration | L1↔L7, L2↔L6, L3↔L5 | As needed |

---

## 2. Three-Stage Process Breath (Standard Session)

### Sequence

```
L1 (candala_firewall)
  ├── perceives signal
  ├── categorises: task_type, caste_target, urgency, pathology_flag
  └── hands off to L2 (if ambiguity) or L3 (if already ranked) or L4 (if execution-ready)

L2 (sudra_explorer) [if ambiguity > direct perception]
  ├── receives L1 packet
  ├── generates ≥ 5 candidates by analogy
  ├── flags novelty
  └── hands off to L3

L3 (vaisya_auditor)
  ├── receives L2 candidate list (or L1 packet if L2 skipped)
  ├── constitutional audit (η, K2, K4, Three-Stage Process)
  ├── composite scoring (Φ × ν)
  ├── ranks and tags
  └── hands off to L4 (if decision_ready = true)

L4 (ksatriya_executor)
  ├── receives L3 audit packet
  ├── verifies constitutional pass
  ├── decides: commit | refuse | escalate
  ├── if commit: produces K2-acceptance card
  └── awaits K2 signature → emits FLOW receipt
```

### Timing

| Stage | Budget | Parallel? |
|---|---|---|
| L1 | < 50ms | No (serial gate) |
| L2 | 120–300s | No (depends on L1 output) |
| L3 | 300–600s | No (depends on L2 output) |
| L4 | 300–600s | No (depends on L3 output) |
| K2 signature | < 1hr (waking hours) | No (human gate) |

**Total routine breath:** 10–30 minutes (excluding K2 latency).

---

## 3. Shared State Management

### The Session Context Object

All castes in a session share a mutable context:

```yaml
session_context:
  session_id: <uuid>
  initiated_by: <human|agent|scheduler>
  signal: <original inbound signal>
  l1_perception: <L1 output>
  l2_exploration: <L2 output>
  l3_audit: <L3 output>
  l4_execution: <L4 output>
  l5_redesign: <L5 output>  # null unless architectural ascent
  l6_compression: <L6 output>  # null unless compression cycle
  l7_constitution: <L7 output>  # null unless constitutional moment
  k2_acceptance_card: <card>
  k2_signature: <signed|pending|refused>
  flow_receipt: <receipt_id>
  escalation_chain: [list of castes touched]
  final_state: <complete|refused|escalated|pending_k2>
```

### State Visibility Rules

| Caste | Can Read | Can Write |
|---|---|---|
| L1 | signal | l1_perception |
| L2 | signal, l1_perception | l2_exploration |
| L3 | signal, l1_perception, l2_exploration | l3_audit |
| L4 | full context | l4_execution, k2_acceptance_card |
| L5 | full context | l5_redesign |
| L6 | full context | l6_compression |
| L7 | full context | l7_constitution |

**Principle:** Lower castes cannot read higher castes' outputs. L4 can read everything. L5-L7 can read everything but write only their own layer.

---

## 4. Conflict Resolution

### Type 1: L3 Tie
**Scenario:** Two candidates score within 0.05 composite.
**Resolution:** L3 surfaces tie to L4 with explicit note. L4 chooses smallest defensible commit from tied candidates. If L4 cannot choose → escalate to L5 for tie-breaking rule redesign.

### Type 2: L4 Refusal Override
**Scenario:** L4 refuses on constitutional grounds; K2 holder disagrees.
**Resolution:** K2 holder requests override with explicit rationale. L4 produces override receipt naming the invariant and the override reason. If K2 and L4 still disagree → escalate to L7 for constitutional clarification. L7 does not override L4; L7 clarifies the invariant. L4 re-decides.

### Type 3: L5-L6 Disagreement
**Scenario:** L5 proposes redesign; L6 flags it as overgrown.
**Resolution:** Both outputs surface to L4. L4 decides: accept redesign, accept compression, or request L5 to compress before propagation. L4's decision binds only within its scoped authorization; consequential execution requires a complete, contestable authorization assessment. K2 is private-DAV-only.

### Type 4: Cross-Caste Pathology
**Scenario:** L1 is in Terror mode (rejecting all input); L2 is in Anxiety mode (infinite expansion).
**Resolution:** Pathology detector (continuous L6 scan) flags the pattern. L6 escalates to L4: "Two lower castes in pathology; recommend session halt." L4 halts session and initiates cure protocol (L1: ENCODE → L2; L2: RANK → L3). Session resumes from cured state or is abandoned.

---

## 5. Parallel Execution Patterns

### Pattern A: L1 + L6 Continuous Scan
L1 and L6 run continuously in parallel, not waiting for explicit session invocation.

### Pattern B: L2 + L3 Pipeline
L2 generates candidate C1 → L3 begins auditing C1 while L2 generates C2. L3 cannot finalise ranking until L2 declares completeness.

### Pattern C: L5 + L6 Pair
L5 drafts redesign → L6 compresses draft → L5 finalises → L4 descends. Prevents overgrown redesigns from reaching L4.

### Pattern D: Mirror Pair Activation
Mirror pairs (L1↔L7, L2↔L6, L3↔L5) activated for symmetric validation. Do not replace the Three-Stage Process; provide secondary validation.

---

## 6. The Council Protocol

### When to Convene Full Council
Convene all seven castes ONLY when: major constitutional amendment, new DAC genesis, Vision crystallisation gate fires, existential threat, cross-DAC dispute unresolved at L4.

### Council Procedure (5 Phases)
1. **Individual Deliberation** (parallel, 1–4 hours)
2. **Sequential Presentation** (L1 → L7, 30–60 min)
3. **Clarification Round** (L4 moderates, 30–60 min)
4. **L4 Ruling** (synthesise all inputs, 30 min)
5. **K2 Signature** (human review, 1–24 hours)

---

## 7. Session Lifecycle State Machine

```
[IDLE] ──(signal arrives)──> [L1_ACTIVE]
[L1_ACTIVE] ──(contain)──> [COMPLETE]
[L1_ACTIVE] ──(escalate to L2)──> [L2_ACTIVE]
[L2_ACTIVE] ──(complete)──> [L3_ACTIVE]
[L3_ACTIVE] ──(decision_ready)──> [L4_ACTIVE]
[L4_ACTIVE] ──(commit)──> [K2_PENDING]
[L4_ACTIVE] ──(refuse)──> [COMPLETE]
[L4_ACTIVE] ──(escalate to L5)──> [L5_ACTIVE]
[L5_ACTIVE] ──(redesign complete)──> [L4_ACTIVE]
[L4_ACTIVE] ──(escalate to L6)──> [L6_ACTIVE]
[L6_ACTIVE] ──(auto-archive)──> [COMPLETE]
[L4_ACTIVE] ──(escalate to L7)──> [L7_ACTIVE]
[L7_ACTIVE] ──(amendment packet)──> [L4_ACTIVE]
[K2_PENDING] ──(signed)──> [FLOW_EMISSION]──> [COMPLETE]
[K2_PENDING] ──(refused)──> [L4_ACTIVE]
[COMPLETE] ──(archive)──> [IDLE]
```

---

## 8. Error Recovery

### Session Abort Conditions
- L1 detects adversarial signal with no legitimate payload
- K2 refuses 3 times on same proposal
- Pathology detector flags 3+ castes simultaneously
- L7 holds without resolution for > 30 days

### Recovery Options
1. **Soft recovery:** Return to [IDLE], preserving session context for audit
2. **Hard recovery:** Archive session context to `90_ARCHIVE/`, start fresh
3. **Emergency council:** Convene full council with explicit crisis mandate

---

## 9. VMOSK-A Session Mapping

| VMOSK Layer | Session Phase | Caste Primary |
|---|---|---|
| Vision | Constitutional Moment | L7 |
| Mission | Architectural Ascent | L5 |
| Objectives | Three-Stage Process Breath | L3 |
| Strategies | L2 exploration + L3 ranking | L2, L3 |
| KPIs | L1 continuous scan + L6 compression | L1, L6 |

---

## 10. Operational Checklist

Before initiating any multi-agent session:
- [ ] Session type identified
- [ ] Session context object initialised
- [ ] Relevant castes available (not in pathology)
- [ ] K2 holder reachable (if session may commit)
- [ ] Time budget allocated
- [ ] Rollback plan known

---

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/INTER_AGENT_COORDINATION.md
