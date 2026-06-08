---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "170 — Track A · Week 4 · Mid-Sprint Review Template"
---

# 170 — Track A · Week 4 · Mid-Sprint Review Template

**Evidence tier:** [I] template / structural scaffold; [S] where citing packet 154 §2.3 + §2.6 charter
**Date:** 2026-04-24
**Lane:** Charioteer template — engineering populates at W4; sovereign reviews + decides
**Status:** Draft template (empty of content until W3 receipt lands)
**Complements:** packet 154 (sprint charter); packets 160 / 162 / 168 (Track A W1-W3 gates); packet 163 / 169 (Track B W1-W2 gates); packet 164 (shared harness)

---

## 0. Axiomatic guard

Week 4 is a **review week**, not a spec week. Packet 154 §2.3 says so explicitly. This packet does NOT pre-decide what the review finds — it cannot. W4 content depends on W1-W3 outcomes that don't exist yet.

What this packet provides: a **form** for the review. A checklist of what to examine, a list of decisions to surface, and the escalation paths. When week 4 arrives, engineering fills this template with real facts; sovereign reviews it and signs next-week kickoff (or pivots).

If the review becomes bureaucracy, burn the form and have a conversation. The form is scaffolding; the review is the work.

`Zero-Sum Resolution Equation`

---

## 1. Purpose

Packet 154 §2.3 assigns week 4 this focus: *"Super-checkpoint protocol draft; proof-of-reconstruction algorithm formal"* — which is W3 work. The mid-sprint review sits at the W3/W4 boundary and asks:

> Given what weeks 1–3 produced, is the sprint on track to deliver week 8's full spec? If not, what pivots (scope, timeline, framework, team) need sovereign decision *now* rather than week 8 when pivot is too late?

Week 4's output is not new engineering spec — it is a **go / pivot / stop** decision surface.

---

## 2. What the W4 review packet contains

When engineering fills this template, the resulting packet (`01_EMERGENTISM/11_UPLINK/170a_TRACK_A_W4_REVIEW_<DATE>.md`) has the following sections:

### 2.1 Sprint progress summary (factual)

- Weeks 1-3 gates: ✅ / ❌ per-gate table (from receipts 160a, 162a, 168a + Track B 163a, 169a)
- Formal-methods framework: chosen (from packet 160 D1) — any pivot triggered since? Y/N
- Simulation harness: running / blocked / extended by Track B as planned
- Properties stated: safety N / liveness M (from packet 162 D1/D2)
- Proofs attempted: X proved · Y blocked-with-named-missing-piece · Z unattempted
- Scenarios lived: happy-path + Byzantine + (any new W3+)
- Cross-track friction incidents: N, with resolution timing

### 2.2 Weekly burn-down vs. plan

Per packet 154 §2.3 week-by-week plan, a table showing planned-vs-actual:

| Week | Planned deliverable | Actual outcome | On-track? |
|---|---|---|---|
| 1 | Framework + terminology | (fill from 160a receipt) | ✅/⚠/❌ |
| 2 | Properties + first proof + harness | (fill from 162a receipt) | ✅/⚠/❌ |
| 3 | Super-checkpoint protocol draft | (fill from 168a receipt) | ✅/⚠/❌ |

Charioteer note: any row showing ⚠ or ❌ triggers §4 pivot questions.

### 2.3 Track B progress (parallel)

- Track B W1 gate: ✅/❌ (from 163a)
- Track B W2 gate: ✅/❌ (from 169a)
- Shared-contract stability: packet 164 §7.1 intact? Y/N
- Glossary conflicts surfaced: N, resolution

### 2.4 Invariant I–VII status

Any risk items flagged by minimalism auditor during weeks 1-3? Enumerate. Per-item: resolved / accepted-risk / escalated-to-sovereign.

### 2.5 Risk register delta (vs. packet 149)

Packet 149 risk matrix is baseline. Week 4 review names:
- Risks that have been closed by W1-W3 evidence
- Risks that have been upgraded in severity
- New risks that surfaced during execution (with severity + likelihood + mitigation path)

---

## 3. Decisions the review surfaces for sovereign

Week 4 is where pivots happen, not week 8. The review packet explicitly names any of the below that apply.

### 3.1 Framework pivot (K3 kill criterion from packet 160)

*Does the chosen framework support the W5-W8 deliverables (archiver economics, full adversarial simulation, full spec)?*

If no → sovereign K2 decision:
- **Pivot** — switch framework; weeks 5-8 rescope; sprint extension likely
- **Scope-reduce** — keep framework; drop deliverables that don't fit; receive a narrower W8 spec
- **Push through** — accept increased proof burden; document why

### 3.2 Scope pivot

*Does the W1-W3 pace suggest W4-W8 can deliver the full packet 153d spec?*

If no → sovereign K2 decision:
- **Sprint extension** — add weeks 9-10 to close the spec
- **Scope reduction** — trim packet 153 §4 open questions; explicit list of what closes vs. defers
- **Full-spec deferral** — sprint delivers partial; production-ready spec comes in a second sprint

### 3.3 Team pivot

*Is the role-map filled and productive?*

If any role is unfilled or underperforming → sovereign K2 decision:
- **Role rebalance** — reshuffle assignments (packet 165 allows rotation for minimalism auditor; others require sovereign K2)
- **Role collapse** — per packet 165 §6 if fewer bodies available than roles
- **Hire / contractor** — if specific skill gap (formal-methods specialist missing is the most common)

### 3.4 Cross-track coordination pivot

*Is Track A ↔ Track B coordination working, or is the weekly sync a bottleneck?*

If no → sovereign K2 decision on:
- Sync cadence change (more or less frequent)
- Explicit escalation budget (48h rule firmer)
- Track B descope / pause (if substrate work is the critical path)

### 3.5 Invariant-risk pivot

*Any weeks-1-3 design decisions that put Invariants I–VII at risk?*

If yes → immediate sovereign K2 call; invariant-flex is sovereign-only and extremely rare. Charioteer does not recommend any Invariant flex; review packet surfaces the tension, sovereign decides.

---

## 4. Pivot decision form (sovereign K2 slots)

The W4 review packet concludes with a decision form sovereign signs:

```
PIVOTS TRIGGERED (check all that apply):

☐ 3.1 Framework pivot → chosen:     ☐ Pivot    ☐ Scope-reduce   ☐ Push-through
☐ 3.2 Scope pivot     → chosen:     ☐ Extend   ☐ Reduce         ☐ Defer
☐ 3.3 Team pivot      → chosen:     ☐ Rebal    ☐ Collapse       ☐ Hire
☐ 3.4 Cross-track     → chosen:     ☐ Cadence  ☐ Escalation-tight ☐ Track B pause
☐ 3.5 Invariant risk  → chosen:     ☐ Hold     ☐ Flex (VERY RARE)

☐ NO PIVOTS — continue W5 per charter

SOVEREIGN SIGNATURE: ______________________  DATE: ______________
```

---

## 5. Escalation paths during W4

Any finding during W4 review that doesn't fit the §3 pivot categories escalates via:

| Category | Path |
|---|---|
| Engineering-internal (scope, timeline, assignment) | CTO decides; sovereign informed |
| Layer-discipline (minimalism audit) | Sovereign decides; bypasses CTO |
| Invariant-risk | Sovereign K2 only; immediate |
| CANON drift (property or protocol contradicts CANON) | Sovereign K2; may trigger packet-level revision |
| External (funding, legal, team availability) | Sovereign handles outside sprint lane |

---

## 6. What W4 does NOT attempt

- No new engineering spec (weeks 5-8 gates come from charioteer-post-W4, if needed)
- No proof work (continues but is not review artifact)
- No scope expansion mid-review (only contraction or framework pivot)
- No Invariant flex without explicit sovereign K2 with justification
- No bypassing weekly receipts — 160a, 162a, 168a are required inputs

---

## 7. Acceptance criteria for the W4 review packet

The filled template at `01_EMERGENTISM/11_UPLINK/170a_TRACK_A_W4_REVIEW_<DATE>.md` passes iff:

☐ §2.1–§2.5 filled with factual content from receipts (no empty sections)
☐ §3.1–§3.5 explicitly marked *triggered* or *not triggered* (no nulls)
☐ §4 signature form has a sovereign mark (at least "NO PIVOTS — continue" counts as signed)
☐ Minimalism auditor sign-off on the review itself
☐ Packet committed before W5 begins

If any ☐ is open, W5 does not begin.

---

## 8. References

- packet 154 §2.3: Mid-sprint review scheduled week 4 (charter source)
- packet 154 §2.6: Week-by-week gates (burn-down baseline for §2.2)
- packet 154 §2.9: Minimalism auditor role (§6 reference)
- packets 160, 162, 168: Track A W1-W3 gates (receipt inputs)
- packets 163, 169: Track B W1-W2 gates (parallel track inputs)
- packet 149: Risk matrix (baseline for §2.5 delta)
- packet 165: Role-map (§3.3 reference)
- packet 167: K2 consolidation form (precedent for §4 signature form)
- packet 99 §4.2: Sovereign Non-Delegation Law (all pivots are sovereign-only)

---

*Charioteer mid-sprint review template. Engineering populates at W4; sovereign signs §4 decision form; W5 kicks off based on result.*

`Zero-Sum Resolution Equation`
