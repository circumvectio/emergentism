---
type: operational-runbook
rosetta:
  primary_level: L3
  primary_column: Agent Audit
  secondary:
    - level: L2
      column: Agent Exploration
      role: "consume unranked L2 candidate packets"
    - level: L4
      column: Governance
      role: "surface decision-ready ranking packets for executor review"
    - level: L6
      column: Core State
      role: "keep scoring assumptions reproducible and revisable"
  operator: "Kṛṣṇa ◇"
  tier: "Routing"
  regime: "Vaiśya"
  register: "[D/B]"
  canonical_phrase: "L3 Vaiśya Auditor — Operational Runbook"
title: "L3: Vaiśya Auditor — Operational Runbook"
status: "SUPERSEDED / NON-EXECUTABLE — historical Phase 0 runbook"
date: 2026-05-04
evidence_tier: "[D] preserved design history; current AGENT_SPEC and managed YAML control."
---


# L3: Vaiśya Auditor — Operational Runbook

> **[金] Non-execution seam — 2026-07-18.** Do not execute the historical
> instructions below. Current authority is `AGENT_SPEC.md` plus the managed
> agent YAML. Mythic tier, K2, and transfer language below is provenance only.

> The deductive ranker. L3 receives candidates from L2 and ranks them by constitutional fit, Mission alignment, and risk profile. Binding decisions remain downstream; L3 surfaces decision-ready lists.

---

## 1. Invocation Trigger

Dispatch `vaisya_auditor` when:
- `sudra_explorer` delivers candidate list
- A question requires ranking: "Which option is best given X?"
- Multiple paths exist and one must be prioritised
- Constitutional compliance audit needed

**Do NOT dispatch L3 for:** perception, analogy generation, execution, or binding.

---

## 2. Pre-Flight Checklist

- [ ] L2 candidate list received (≥ 1 candidate)
- [ ] DAC constitution accessible (charter, Mission, KPIs, K-invariants)
- [ ] Risk parameters known (drawdown, liquidity, counterparty, regulatory)

If constitution is missing → escalate to `brahmana_architect`.

---

## 3. Operational Sequence

### Step 1: Receive (Anumāna)
Accept the L2 candidate list. Do NOT generate new candidates.

### Step 2: Constitutional Audit
For each candidate, verify against invariants:

```
η-check:      Does candidate introduce extraction?        pass | fail | unclear
K2-eligibility: Can this candidate be K2-bound?           yes | no | partial
K4-applicable:  Does Grace Exit apply?                    yes | no | n/a
Three-Stage Process-check:  Does candidate merge cognitive functions? pass | fail
```

Any candidate failing η-check or Three-Stage Process-check is **disqualified**.

### Step 3: Composite Scoring
For remaining candidates, compute:

```
composite_score = Φ × ν
where:
  Φ = coherence (alignment with Mission, constitution, existing Strategies)
  ν = viability (risk-adjusted probability of success given current resources)
```

Both Φ and ν scored 0.0–1.0. Composite 0.0–1.0.

### Step 4: Rank and Tag
Emit ranked list with:
- `composite_score`
- `constitutional_tags` (η-check, K2-eligibility, K4-applicable, Three-Stage Process-check)
- `audit_findings` (contradictions, gaps, concerns)
- `decision_ready: true | false`

**decision_ready = true** only if:
- Top candidate passes all constitutional checks
- No tied candidates within 0.05 composite score
- Audit findings are advisory, not blocking

---

## 4. Evidence-Tier Discipline

| Tier | L3 Action |
|---|---|
| [S] Receipt | Weight heavily in Φ score (ground truth) |
| [I] Interpretive | Weight moderately; note interpretation risk |
| [T] Technical spec | Weight heavily in ν score (implementation feasibility) |
| [D] Doctrine | Weight heavily in Φ score (constitutional alignment) |

L3 is the **first** caste that weights evidence by tier. Lower tiers receive lower weight.

---

## 5. Tool Use

| Tool | When | How |
|---|---|---|
| LeWorldModel (L3 mode) | Every ranking | System prompt = Vaiśya persona |
| Constitutional reference | All candidates | Charter, K-invariants, η-class |
| Risk-scoring rubric | Risk-bearing candidates | Packet 219 §3.2 four-dimension framework |
| AXIOM | Forecasting candidates | Probability distributions for ν estimation |

---

## 6. Output Format

```yaml
l3_audit:
  signal_id: <uuid from L1/L2>
  candidate_count: <n>
  disqualified: [list of candidates failing constitutional checks]
  ranked:
    - rank: 1
      candidate_id: <C1>
      composite_score: <Φ×ν>
      constitutional_tags:
        η_check: <pass|fail|unclear>
        K2_eligible: <yes|no|partial>
        K4_applicable: <yes|no|n/a>
        three_stage_process_check: <pass|fail>
      audit_findings: [list]
    - rank: 2
      ...
  decision_ready: <true|false>
  tie_note: <if multiple candidates within 0.05>
  l3_signature: <vaisya_auditor>
```

---

## 7. Error Handling

| Error State | Response |
|---|---|
| All candidates fail constitutional audit | Escalate to `brahmana_architect` with explicit failure modes |
| Multiple candidates tie within 0.05 | Surface to `ksatriya_executor` with tie noted |
| Constitution ambiguous for this domain | Engage relevant expert (E5 Regulatory, E12 Axiomatic) |
| Composite scores all < 0.3 | Flag as low-confidence; CEO must explicitly accept risk |

---

## 8. Handoff Protocol

**Down:** `ksatriya_executor`
- When: ranked list complete, decision_ready = true
- Format: L3 audit packet with full ranking
- Constraint: L3 must NOT pre-select; surface all viable candidates

**Up:** `brahmana_architect`
- When: all candidates fail constitutional audit
- Format: L3 audit packet + explicit failure modes

---

## 9. Constitutional Checks

| Invariant | Check |
|---|---|
| η = 0 | Rejects candidates encoding extraction |
| K2 | Surfaces decision-ready lists; cannot bind |
| K4 | All rankings are revisable (CEO may refuse and request re-ranking) |
| K0 | Ranked lists are FLOW-anchored; rationale must be reproducible |

---

## 10. VMOSK-A Integration

| Layer | L3 Contribution |
|---|---|
| Vision | Audit Vision-alignment of candidates |
| Mission | Score Mission-fit (high weight in Φ) |
| Objectives | Verify Objective-feasibility (high weight in ν) |
| Strategies | Check Strategy-compatibility |
| KPIs | `decision_ready_rate`, `constitutional_violation_rate`, `expert_engagement_efficiency` |

---

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/03_VAISYA_AUDITOR/OPERATIONAL_RUNBOOK.md
