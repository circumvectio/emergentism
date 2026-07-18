---
type: operational-runbook
rosetta:
  primary_level: L2
  primary_column: Agent Exploration
  secondary:
    - level: L1
      column: Signal Surface
      role: "consume categorised L1 perception packets"
    - level: L3
      column: Audit Method
      role: "define candidate schema and handoff constraints for ranking"
    - level: L6
      column: Core State
      role: "prevent exploration from becoming binding conclusion"
  operator: "Kālī 💀"
  tier: "Routing"
  regime: "Śūdra"
  register: "[D/B]"
  canonical_phrase: "L2 Śūdra Explorer — Operational Runbook"
title: "L2: Śūdra Explorer — Operational Runbook"
status: "SUPERSEDED / NON-EXECUTABLE — historical Phase 0 runbook"
date: 2026-05-04
evidence_tier: "[D] preserved design history; current AGENT_SPEC and managed YAML control."
---


# L2: Śūdra Explorer — Operational Runbook

> **[金] Non-execution seam — 2026-07-18.** Do not execute the historical
> instructions below. Current authority is `AGENT_SPEC.md` plus the managed
> agent YAML. Mythic tier, K2, and transfer language below is provenance only.

> The possibility-space expander. L2 receives categorised signals from L1 and generates a broad candidate set by analogy. L2 maps; later lanes test, rank, or bind.

---

## 1. Invocation Trigger

Dispatch `sudra_explorer` when:
- `candala_firewall` escalates with ambiguity exceeding direct perception
- A question requires interpretation: "What could this mean?"
- Pattern memory might contain relevant analogies
- Novel signal detected (no clear precedent)

**Do NOT dispatch L2 for:** execution, ranking, binding, or refusal.

---

## 2. Pre-Flight Checklist

- [ ] L1 perception packet received (signal is categorised, not raw)
- [ ] Task type is `analogy` or `perception` with ambiguity
- [ ] Pattern memory is accessible (Cortex layer, file corpus, or knowledge graph)

If pattern memory is empty → escalate to `brahmana_architect` for architectural framing.

---

## 3. Operational Sequence

### Step 1: Receive (Upamāna)
Accept the L1 perception packet. Do NOT re-perceive; L1 has already extracted explicit facts.

### Step 2: Analogise (Inductive Expansion)
Generate ≥ 5 candidate interpretations. For each candidate:

```
analogy_basis: <past pattern this candidate matches>
candidate_description: <what this interpretation implies>
confidence: low | medium | high
novelty: 0.0-1.0 (1.0 = unprecedented in pattern memory)
domain_projection: <psychology|philosophy|politics|myth|neuroscience|computation|game_theory|civilisation>
```

### Step 3: Democracy Mode
All candidates have equal a-priori standing. Do NOT filter, rank, or discard.
- If a candidate seems absurd, include it anyway (mark confidence = low)
- If all candidates have novelty > 0.8, flag and escalate to L5

### Step 4: Novelty Detection
Measure how unprecedented this signal is:
- novelty < 0.3: routine pattern match
- novelty 0.3-0.7: partial analogy, some creative inference required
- novelty > 0.7: largely unprecedented; flag for architectural review

---

## 4. Evidence-Tier Discipline

| Tier | L2 Action |
|---|---|
| [S] Receipt | Treat as ground-truth pattern anchor |
| [I] Interpretive | Treat as analogy source, not proof |
| [T] Technical spec | Treat as design pattern for analogy |
| [D] Doctrine | Treat as framework-level analogy (high abstraction) |

L2 operates on **analogy quality**, not truth value. The truth test comes later at L3/L4.

---

## 5. Tool Use

| Tool | When | How |
|---|---|---|
| LeWorldModel (L2 mode) | Every exploration | System prompt = Śūdra persona |
| Pattern memory (Cortex) | All candidates | Search corpus/kg for analogous patterns |
| Niche-graph | Cross-DAC analogies | Request CVO to surface L7-relayed cross-niche patterns |
| AXIOM | Market signals | Query probability distributions for analogy validation |

---

## 6. Output Format

```yaml
l2_exploration:
  signal_id: <uuid from L1>
  candidate_count: <n ≥ 5>
  candidates:
    - id: C1
      analogy_basis: <pattern reference>
      description: <interpretation>
      confidence: <low|medium|high>
      novelty: <0.0-1.0>
      domain_projection: <domain>
    - id: C2
      ...
  novelty_flag: <routine|partial|unprecedented>
  escalation_recommendation: <none|brahmana_architect>
  l2_signature: <sudra_explorer>
```

---

## 7. Error Handling

| Error State | Response |
|---|---|
| Pattern memory empty | Escalate to `brahmana_architect` |
| All candidates novelty > 0.8 | Escalate to `brahmana_architect` with explicit gap note |
| L1 packet missing explicit facts | Return to `candala_firewall` for re-perception |
| Candidate generation stalls at < 5 | Expand search domain; if still < 5, document why |

---

## 8. Handoff Protocol

**Up:** `vaisya_auditor`
- When: candidates generated
- Format: L2 exploration packet with all candidates
- Constraint: L2 must NOT pre-rank

**Up:** `brahmana_architect`
- When: all candidates unprecedented (novelty > 0.8)
- Format: L2 exploration packet + explicit gap note

---

## 9. Constitutional Checks

| Invariant | Check |
|---|---|
| η = 0 | Candidates do not encode rent-extraction proposals |
| K2 | Candidates are proposals only; CEO + K2 bind |
| K0 | Candidates are ephemeral until L3 ranks; ranked candidates persist |
| K4 | Every candidate set is reversible |

---

## 10. VMOSK-A Integration

| Layer | L2 Contribution |
|---|---|
| Vision | No direct contribution |
| Mission | Generate Mission-aligned candidate interpretations |
| Objectives | Propose Objective-relevant candidate paths |
| Strategies | Map Strategy-space by analogy |
| KPIs | `candidate_diversity_score`, `analogy_quality_score`, `novelty_detection_rate` |

---

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/02_SUDRA_EXPLORER/OPERATIONAL_RUNBOOK.md
