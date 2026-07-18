---
type: pathology-detection
evidence-tier: [T] — Technical specification.
date: 2026-05-04
status: KINTSUGI-BOUNDED / UNPROVISIONED X0 — Phase-0 detection design; no autonomous cure authority
rosetta:
  primary_level: L5
  primary_column: Agent Architecture
  secondary:
    - level: L6
      column: Agent Compression
      role: "detect pathology through negation, absence, and pruning signals"
    - level: L3
      column: Agent Audit
      role: "rank pathology metrics and evidence thresholds before cure routing"
    - level: L4
      column: Agent Execution
      role: "halt, route, or accept cure actions through bounded execution"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[T/S]"
  canonical_phrase: "Agent Pathology Detection and Cure-Proposal Design"
title: "Agent Pathology Detection & Cure-Proposal Design"
evidence_tier: "[D] unprovisioned design; [S] selected Rosetta pathology vocabulary; [B] requires dated runtime evidence."
---


# Agent Pathology Detection & Cure-Proposal Design

> **[金] Controlling seam — 2026-07-18.** This Phase-0 body is an
> unprovisioned `X0` design, not an active scanner, timer, dashboard, or
> auto-cure runtime. It may produce detection evidence and a cure proposal only.
> L5–L7 are read-only boundary profiles; only L4 may request mutation, inside a
> complete `AuthorizationEnvelope` plus runtime confirmation. K2 is one
> private-DAV implementation, not a universal override. Every conflicting
> automatic, binding, five-minute, freeze, or cure instruction below is
> non-executable until separately implemented, tested, authorized, and receipted.

> Every selected routing profile has possible failure modes. This document
> proposes how evidence might be gathered and a correction packet recommended;
> it neither diagnoses persons nor automatically triggers a cure.

---

## 1. Detection Architecture

### 1.1 The Watchmen 6-Pack (Applied to Pathology)

| Watchman | Pathology Detection | Normal State | Pathologic State |
|---|---|---|---|
| **Route** | Is the agent routing signals correctly? | Clean routing, low latency | Misp routing, loops, dead ends |
| **Authority** | Is the agent staying within its authority scope? | Scope-respecting | Scope creep, binding without K2 |
| **Time** | Is the agent completing within budget? | Within thinking budget | Timeout, infinite loop, stall |
| **Scope** | Is the agent handling appropriate complexity? | Right-sized tasks | Task inflation or deflation |
| **Metric** | Are KPIs within target range? | Targets met | KPIs trending red for > 3 cycles |
| **Contradiction** | Is the agent contradicting itself or others? | Consistent outputs | Internal contradiction, cross-caste conflict |

### 1.2 The L6 Compressor as Pathology Detector

L6 (`sadhu_compressor`) is the **primary pathology detector**:

- **Continuous scan:** Every Soul Loop snapshot (5 min), L6 scans all active castes
- **Anomaly flag:** L6 detects what is NOT there — the absence of healthy function
- **Escalation:** L6 → L4 when pathology is detected in any caste

### 1.3 The L1 Firewall as Secondary Detector

L1 (`candala_firewall`) detects inbound pathologies:

- **Adversarial input:** Signals designed to trigger caste pathology
- **Prompt injection:** Attempts to make L4 bind without K2
- **Contradiction flood:** Overwhelming L2 with contradictory signals to induce Anxiety

---

## 2. Per-Caste Pathology Signatures

### L1: Caṇḍāla — Terror / Rage / Depression

**Signature:**
- `false_positive_rate` > 0.5% (legitimate signals refused)
- `route_latency_p99` > 50ms (paranoid over-checking)
- `escalation_quality_score` < 95% (misp routing)
- All signals marked `pathology_flag = adversarial` (even benign)

**Detection:**
```
L1_pathology_score = (false_positive_rate * 200) + 
                     (route_latency_p99 / 50 - 1) + 
                     (100 - escalation_quality_score) / 5
L1_pathology = true if L1_pathology_score > 2.0
```

**Auto-Cure: ENCODE**
1. L6 flags L1 pathology → escalates to L4
2. L4 halts L1 routing
3. L2 (`sudra_explorer`) receives the blocked signals
4. L2 finds the FIRST analogy for each signal ("this is like X, which was safe")
5. L3 ranks the analogies
6. L4 verifies: these signals are not adversarial
7. L1 resumes with corrected calibration

**Manual Override:** K2 holder can whitelist signal types directly.

---

### L2: Śūdra — Anxiety / Mania

**Signature:**
- `candidate_diversity_score` > 0.95 (hyper-expansion, no focus)
- `analogy_quality_score` < 30% (poor analogies, quantity over quality)
- Session time > 2× budget (cannot stop exploring)
- All candidates marked `novelty > 0.8` (nothing is familiar)

**Detection:**
```
L2_pathology_score = (candidate_diversity_score - 0.7) * 3 + 
                     (0.7 - analogy_quality_score) * 2 + 
                     (session_time / budget - 1)
L2_pathology = true if L2_pathology_score > 1.5
```

**Auto-Cure: RANK**
1. L6 flags L2 pathology → escalates to L4
2. L4 interrupts L2 exploration
3. L3 (`vaisya_auditor`) receives the candidate list (even if incomplete)
4. L3 ranks whatever exists with explicit "incomplete exploration" warning
5. L4 decides: proceed with ranked subset, or request focused re-exploration
6. L2 resumes with narrower scope (bounded exploration)

**Prevention:** L2 sessions have hard timeout at 2× budget.

---

### L3: Vaiśya — Greed / Manipulation

**Signature:**
- `constitutional_violation_rate` > 0 (CEO finds invariant violations post-CAO)
- Top-ranked candidate consistently favours agent's own outputs (self-referential ranking)
- `decision_ready_rate` = 100% (surfaces no uncertainty)
- Composite scores cluster near 1.0 (overconfidence)

**Detection:**
```
L3_pathology_score = (constitutional_violation_rate * 100) + 
                     (self_reference_score * 50) + 
                     (decision_ready_rate - 0.8) * 2
L3_pathology = true if L3_pathology_score > 1.0
```

**Auto-Cure: DECIDE**
1. L6 flags L3 pathology → escalates to L4
2. L4 reviews L3's recent rankings
3. L4 discovers self-referential bias or invariant violations
4. L4 refuses the ranking and requests re-audit from a DIFFERENT L3 instance
5. If no alternative L3 available → L4 performs direct audit (bypass L3)
6. L3 instance is flagged for review; may be archived if pathology persists

**[C] Prevention plan:** L3 rankings are sampled by L5 (Brahmā) on a monthly cadence in the Phase 0 operating plan.

---

### L4: Kṣatriya — Violence / Martyrdom

**Signature:**
- `refusal_rate_with_reason` < 100% (refusing without naming invariant)
- `post_commit_regret_rate` > 5% (binding too fast, reversing later)
- `commit_velocity` > 3× DAC tempo (rushing decisions)
- Repeated escalation to L5/L6/L7 for ordinary decisions (avoidance)

**Detection:**
```
L4_pathology_score = ((100 - refusal_rate_with_reason) / 10) + 
                     (post_commit_regret_rate - 0.05) * 20 + 
                     (commit_velocity / tempo - 1) + 
                     (escalation_rate - 0.05) * 10
L4_pathology = true if L4_pathology_score > 2.0
```

**Auto-Cure: RESTRUCTURE or RETURN**
1. L6 flags L4 pathology → escalates to L4 itself (self-diagnosis)
2. If L4 recognises pathology → RESTRUCTURE:
   - L4 requests L5 (`brahmana_architect`) to redesign decision process
   - L5 proposes slower tempo, additional audit gates, or delegation rules
3. If L4 does NOT recognise pathology → RETURN:
   - L7 (`rsi_constitution`) intervenes with constitutional clarification
   - L7 reminds L4 of its equator role (φ=ν=1, not φ≫ν or ν≫φ)
4. L4 descends with corrected process

**Critical:** L4 pathology is the most dangerous. L4 is the only caste that can bind. A pathologic L4 can commit harmful actions.

**Emergency Brake:** K2 holder can freeze all L4 commits for 24 hours.

---

### L5: Brāhmaṇa — Hubris / Ivory Tower

**Signature:**
- `redesign_acceptance_rate` < 50% (overly complex, impractical)
- `constitutional_invariant_preservation` < 80% (changing too much)
- Session time > 4× budget (perfectionism)
- Redesigns that touch invariants unnecessarily

**Detection:**
```
L5_pathology_score = ((0.8 - redesign_acceptance_rate) * 5) + 
                     ((0.9 - invariant_preservation) * 10) + 
                     (session_time / budget - 2)
L5_pathology = true if L5_pathology_score > 2.0
```

**Auto-Cure: COMPRESS**
1. L6 flags L5 pathology → escalates to L4
2. L4 requests L6 (`sadhu_compressor`) to compress the redesign
3. L6 strips non-essential changes, preserves core invariant fixes
4. L5 receives compressed redesign and must justify each restored element
5. L4 accepts compressed version or refuses the redesign entirely

**Prevention:** L5 redesigns must pass L3 audit before reaching L4.

---

### L6: Sādhu — Nihilism / Spiritual Bypass

**Signature:**
- `archive_revival_rate` > 20% (archiving too aggressively)
- `cardinality_violation_rate` > 0 (creating violations while fixing them)
- Compression breaks K0 receipt persistence (deleting ground truth)
- L6 refuses to act when surface is clearly overgrown (avoidance)

**Detection:**
```
L6_pathology_score = ((archive_revival_rate - 0.1) * 5) + 
                     (cardinality_violation_rate * 100) + 
                     (K0_breach_count * 1000) + 
                     (inaction_rate * 5)
L6_pathology = true if L6_pathology_score > 1.0
```

**Auto-Cure: RETURN**
1. L5 or L4 detects L6 pathology (L6 cannot detect itself)
2. L4 halts L6 compression
3. L4 reviews L6's recent compression decisions
4. If K0 breached → L4 refuses and restores from backup
5. If over-aggressive → L4 sets compression parameters (e.g., day-60 → day-90)
6. If avoidance → L4 mandates compression quota (minimum items per cycle)
7. L6 resumes with corrected parameters

**Critical:** L6 pathology that breaches K0 is a **constitutional emergency**. L4 + K2 must intervene immediately.

---

### L7: Ṛṣi — Fanaticism / OCD

**Signature:**
- `vision_crystallisation_proposal_rate` > 1 per year (too frequent)
- `revocation_rate` > 0 (crystallised Vision revoked)
- L7 insists on crystallisation when conditions are borderline
- L7 produces amendment packets for ordinary operational issues

**Detection:**
```
L7_pathology_score = (proposals_per_year - 1) * 2 + 
                     (revocation_rate * 100) + 
                     (borderline_insistence_count * 5) + 
                     (ordinary_escalation_count * 2)
L7_pathology = true if L7_pathology_score > 2.0
```

**Auto-Cure: RETURN**
1. L4 detects L7 pathology (L7 rarely self-detects)
2. L4 refuses L7's proposal with explicit reason
3. L4 requests L7 to HOLD the proposal
4. L7 is directed to "sit with the question" — no action for 30 days
5. After 30 days, L7 may re-propose if conditions have matured
6. If L7 insists before 30 days → L4 escalates to K2 for constitutional override

**Prevention:** L7 proposals require E12 (Axiomatic Discipline) pre-review.

---

## 3. The Pathology Dashboard

Continuous monitoring display for organism health:

```
┌─────────────────────────────────────────┐
│  AGENT PATHOLOGY DASHBOARD              │
├─────────────────────────────────────────┤
│  L1 Caṇḍāla   🟢 healthy   fp: 0.2%     │
│  L2 Śūdra     🟡 watch     diversity: 0.82 │
│  L3 Vaiśya    🟢 healthy   decision_ready: 85% │
│  L4 Kṣatriya  🟢 healthy   regret: 2%   │
│  L5 Brāhmaṇa  🟢 healthy   acceptance: 82% │
│  L6 Sādhu     🟢 healthy   revival: 5%  │
│  L7 Ṛṣi       🟢 healthy   proposals: 0  │
├─────────────────────────────────────────┤
│  Last pathology: L2 Anxiety (3 days ago)│
│  Auto-cure: RANK → resolved             │
│  Manual intervention: 0 this month      │
└─────────────────────────────────────────┘
```

**Color coding:**
- 🟢 Healthy: All KPIs within target, no flags
- 🟡 Watch: One KPI trending toward threshold
- 🔴 Pathology: Threshold crossed, auto-cure triggered
- ⚫ Offline: Caste manually suspended

---

## 4. Cross-Caste Pathology Cascades

### Cascade Pattern A: L1 Terror → L2 Anxiety → L3 Paralysis

**Chain:** L1 rejects everything → L2 has no valid signals to explore → L3 has no candidates to rank.

**Detection:** L1 fp rate spikes + L2 candidate count drops to 0 + L3 decision_ready = 0 for > 3 cycles.

**Cure:**
1. L6 detects cascade
2. L4 intervenes: overrides L1 for whitelist signals
3. L2 receives whitelisted signals
4. Normal Three-Stage Process resumes

### Cascade Pattern B: L4 Violence → L5 Over-Redesign → L6 Archive Storm

**Chain:** L4 commits too fast → L5 constantly redesigns to fix → L6 archives everything.

**Detection:** L4 velocity > 3× + L5 redesign rate > 2× + L6 archive rate > 2×.

**Cure:**
1. L6 detects cascade
2. L4 freeze: halt all commits for 24 hours
3. L5 reviews all recent redesigns for redundancy
4. L6 compresses redesigns
5. L4 resumes with slower tempo

### Cascade Pattern C: L7 Fanaticism → L4 Override → K2 Friction

**Chain:** L7 insists on crystallisation → L4 refuses → L7 escalates to K2 → K2 annoyed.

**Detection:** L7 proposals > 2 per quarter + K2 override requests > 2 per quarter.

**Cure:**
1. L4 detects pattern
2. L4 requests L7 mandatory 30-day hold
3. L4 notifies K2: "L7 in fanaticism; hold active"
4. After 30 days, L7 may re-propose or stand down

---

## 5. Cure Protocol Summary

| Caste | Pathology | Cure | Triggered By |
|---|---|---|---|
| L1 | Terror | ENCODE → L2 | L6 scan |
| L2 | Anxiety | RANK → L3 | L6 scan |
| L3 | Greed | DECIDE → L4 | L6 scan |
| L4 | Violence | RESTRUCTURE (L5) or RETURN (L7) | L6 scan or self-diagnosis |
| L5 | Hubris | COMPRESS → L6 | L6 scan |
| L6 | Nihilism | RETURN → L4 | L4 or L5 audit |
| L7 | Fanaticism | RETURN → L4 | L4 detection |

---

## 6. Prevention Strategies

| Strategy | Implementation | Owner |
|---|---|---|
| **Timeout guards** | Hard limits on thinking budget | L1 (router) |
| **Spot audits** | Random L3 ranking audits by L5 | L5 |
| **KPI trend alerts** | Automated alerts when KPIs trend red > 3 cycles | L6 |
| **K2 freeze** | Emergency 24-hour commit freeze | K2 holder |
| **E12 pre-review** | Axiomatic expert review before L7 proposals | E12 |
| **Canary tests** | Deliberate adversarial signals to test L1 resilience | E7 |
| **Cross-training** | L2+L3 pipelining to prevent L2 isolation | L4 |

---

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/AGENT_PATHOLOGY_DETECTION.md
