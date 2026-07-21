---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "Reconciliation Action Matrix — 2026-04-14"
---

# RECONCILIATION ACTION MATRIX — 2026-04-14

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

## From Honest Diagnosis to Governed Repair

> This document operationalizes `11_CANON_RECONCILIATION.md`.
> It converts contradictions into explicit repair tracks with owners, affected files, required decisions, and freeze status.

---

## Purpose

The organism now has enough cognitive and architectural reality that unresolved contradictions are more dangerous than missing features.

This matrix exists to:
1. identify each launch-blocking contradiction,
2. name the canonical decision required,
3. point to the affected files/contracts/docs,
4. define freeze or launch status,
5. make reconciliation governable.

---

## Status Legend

- **FROZEN** — must not be launched or strongly claimed until reconciled
- **PARTIAL** — real in some form but overstated or incomplete
- **ACTIVE** — safe to iterate publicly with caution
- **CANONICAL DECISION REQUIRED** — multiple realities exist; one must be chosen
- **RESOLVED** — retained as governance memory; not a live blocker unless linked
  surfaces drift again

---

## Self-Application Note

This matrix is both:

- a live freeze-and-repair surface
- a governance memory surface

That means not every row is the same kind of work. In particular:

- `FROZEN`, `PARTIAL`, and `CANONICAL DECISION REQUIRED` rows remain live
  governance work
- `RESOLVED` rows remain only as trace unless new contradiction appears

Read this matrix through continuous recursive disambiguation. Do not treat
governance memory as a flat implementation queue.

---

## Executive Rule

> **No financial, sovereign, or architectural claim may remain in active launch language if code, contracts, and canon do not agree on what it is.**

---

## Action Matrix

| ID | Domain | Claim / Contradiction | Current Reality | Affected Files / Surfaces | Required Canonical Decision | Status | Owner Track |
|---|---|---|---|---|---|---|---|
| C1 | Economic | **ZAI demurrage** described as continuous idle-balance redistribution | Current token/contract implementation does not support live rebasing/redistribution mechanics | 04_ECONOMICS.md, ZAI contracts, wallet and credit docs | Either implement actual demurrage mechanism or remove/downgrade claim from canon | **FROZEN** | Financial reconciliation |
| C2 | Economic | **SKY interest flow** claimed as live and routed to AMM | No implemented interest accrual path matching described economics | 04_ECONOMICS.md, Vault / FlowWallet / AMM-related contracts | Either implement cost-of-capital mechanics or remove all active interest-routing claims | **FROZEN** | Financial reconciliation |
| C3 | Economic | **Lombard Bridge** historically meant three different products across canon/spec/code | Canon, spec, and code described mutually incompatible instruments; later canon retired the term and kept `Vault.sol` as the surviving primitive | Uplink economics, credit specs, vault contracts, `14_LOMBARD_BRIDGE_DECISION.md` | Propagate the retirement/freeze language everywhere old launch phrasing survives | **RESOLVED** | Financial propagation / historical trace |
| C4 | Economic | **LP-100 fixed supply forever** vs mint path | Supply invariant and code behavior disagree | LP100 and PRISM contracts, Uplink economics, token docs | Either remove mint path or remove fixed-supply claim | **FROZEN** | Contract reconciliation |
| C5 | Economic | **Grace Exit** promises full NAV redemption | Exit promise appears underfunded or unsafe relative to current mechanics | Grace Exit docs, PPOFactory / vault / liquidity logic, economics docs | Redefine NAV truthfully, fund reserve, or suspend claim | **FROZEN** | Financial reconciliation |
| C6 | Architecture | **F1 never predicts** vs Circle forecasting code | `estimate_market_probability()` and POST `/api/forecast/market` removed from TheCircle (2026-04-16). Remaining TimesFM pipeline outputs narrative durability scores (F1/IS observation). | Circle forecasting code, architecture docs, organ contracts | Completed — prediction logic removed; module reframed as F1 durability scoring. | **RESOLVED** | Organ-boundary reconciliation |
| C7 | Architecture | **Strict F-flow schemas** claimed, ad-hoc implementations exist | Live flows still drift in places from documented strict contracts | 05_ARCHITECTURE.md, bridge code, integration docs | Either implement real schema enforcement everywhere or downgrade docs from strictness claim | **PARTIAL** | Backbone and integration reconciliation |
| C8 | Sovereignty | **K2 human-signs-every-action** guarantee overstated | Stubs/bypasses exist or have existed; guarantee not fully cryptographic everywhere | K2 gateway, heartbeat paths, constitutional docs | Remove strong sovereignty claim until end-to-end cryptographic enforcement is real | **FROZEN** | Sovereignty reconciliation |
| M1 | Mathematical | **L(x)** treated as derived and sometimes effectively load-bearing | Derivation status disputed or absent in canonical formalism | Uplink economics, framework math docs, FAQs | Downgrade tier or provide rigorous derivation | **CANONICAL DECISION REQUIRED** | Mathematical reconciliation |
| M2 | Mathematical | **phi·nu = 1** manifold identity collapsed into node-level operational P in compressed docs | Seed/compression docs blur domain distinctions | 01_SEED.md, 06_SEED, framework math docs | Restore explicit manifold vs node-level distinction everywhere | **PARTIAL** | Mathematical reconciliation |
| M3 | Mathematical | **phi·nu = 1 everywhere on S2** domain slippage | Pole exclusions exist in canon, but not propagated consistently | math derivation docs, compressed summaries | Correct every “everywhere” claim to domain-restricted form | **CANONICAL DECISION REQUIRED** | Mathematical reconciliation |
| M4 | Epistemic | **Evidence-tier discipline** fractured by extra/non-canonical tiers | Four-tier system is not uniformly respected | framework canon, theorem and axiom docs | Restore one tier system and reclassify violators | **CANONICAL DECISION REQUIRED** | Epistemic reconciliation |
| X1 | Canon | **4-organ restructure** canonical, but not fully propagated | The 4-organ model is canonical; multiple legacy docs still describe 6/7-organ reality | old architecture docs, summaries, indexes, explanatory files | Continue propagation of the canonical 4-organ model and archive or demote legacy-only surfaces | **PARTIAL** | Corpus reconciliation / propagation residue |
| X2 | Canon | **P-SCORES** contains competing organism-P values and formulas | Score truth is not singular | SKYZAI_ORG/P-SCORES.md, state docs, summaries | Choose one formula and annotate confidence/uncertainty honestly | **CANONICAL DECISION REQUIRED** | State reconciliation |
| X3 | Governance | **False-Phi incident** governance loop open | Responsible agent / closure action unresolved | P-SCORES.md, governance notes, audit trails | Close the governance loop or remove stale action language | **PARTIAL** | Governance reconciliation |
| A1 | Architecture | **SPECTRE body/brain separation plus fallback** overstated | Implementation scaffolding incomplete relative to claim strength | SPECTRE docs/specs, architecture docs | Downgrade to roadmap/research until actually implemented | **FROZEN** | SPECTRE reconciliation |
| A2 | Architecture | **Unsupported ROI figures** | No current derivation or evidence attached | architecture/spec docs, pitch surfaces | Remove or attach derivation and evidence | **FROZEN** | Architecture reconciliation |
| A3 | Tooling | **Destructive post-tool hook/linter** damages backbone/tests/init files | Autoimmune tooling risk persists | tool configs, hooks, workflow docs | Disable, scope, or replace destructive hook before further expansion | **ACTIVE / HIGH PRIORITY** | Tooling reconciliation |
| A4 | Repository | **Repository continuity and recoverability discipline** | A real git history exists, but continuity still depends on branch discipline, archive hygiene, and not letting local mirrors outrun source truth | repo root, workflow, archive discipline | Preserve commit continuity, avoid mirror-first drift, and keep archive/source boundaries explicit | **ACTIVE / HIGH PRIORITY** | Repository continuity |

---

## Priority Order

### Priority 0 — Immediate Continuity Protection
1. Preserve real git continuity and archive/source discipline
2. Contain destructive hook/linter behavior
3. Keep backbone tests alive

### Priority 1 — Freeze Unsafe Financial/Sovereignty Claims
4. Freeze demurrage, interest, Lombard, LP-100 fixed-supply, Grace Exit, and strong K2 guarantees in active launch language

### Priority 2 — Canonical Decisions
5. Continue propagation of the Lombard Bridge retirement / `Vault.sol` canonical decision
6. Choose one P-score formula and annotate uncertainty honestly
7. Choose one evidence-tier regime
8. Complete 4-organ propagation
9. Resolve L(x) status

### Priority 3 — Code / Contract Alignment
10. Implement what survives canon
11. Remove what does not
12. Stop describing aspirational architecture as implemented reality

---

## Freeze / Unfreeze Rule

A frozen claim may only move to **PARTIAL** or **ACTIVE** if all three are true:

1. **Code / contract reality exists**
2. **Canon describes that reality accurately**
3. **State/architecture/docs no longer describe competing versions**

No exceptions.

---

## What Can Still Launch Honestly

| Layer | Launchable? | Reason |
|---|---|---|
| Cognitive organism (Rosetta / Three-Stage Process / refusal) | **YES** | Real, breathing, packetized, reason-governed |
| Backbone / packet spine | **YES** | Real, tested, canonical |
| Public framework / explanatory sites | **YES** | Public explanatory surfaces can launch; they do not prove financial, sovereign, or credit-runtime claims by themselves |
| Local/demo organism loop | **YES** | Traceable and refusal-capable |
| Financial organism / tokenomics / credit layer | **NO** | Contradictions unresolved |
| Sovereign K2 guarantees | **NO** | Must not be overstated |
| Grace Exit / credit redemption claims | **NO** | Unsafe until reconciled |
| Full SPECTRE nervous system claims | **NO** | Roadmap/research, not implemented reality |

---

## Governing Law

> **The cognition discriminates; the substrate trusts.**

This law still stands.
But it now applies equally to the corpus itself:
- the cognition must discriminate what is real, partial, contradicted, and fictional,
- and the substrate of canon must trust only what has earned that status.

---

## Closing Rule

> **No false coherence.**

The organism is allowed to be partial.
It is not allowed to pretend contradiction is integration.

---
**Companion file:** [11_CANON_RECONCILIATION.md](11_CANON_RECONCILIATION.md)
**Constitutional law:** The cognition discriminates; the substrate trusts.
**Symbol:** Zero-Sum Resolution Equation


## Freeze Pass note

The active launch/documentation surfaces have been partially downgraded on
2026-04-14 to prevent unsafe financial and sovereignty claims from being
presented as implemented reality. Continue this source-first pass wherever
stale launch language remains, and archive superseded traces rather than
leaving them to impersonate live blockers.


See also: [13_FINANCIAL_RECONCILIATION.md](13_FINANCIAL_RECONCILIATION.md) for the single-source-of-truth memo that narrows the financial organism to what can be claimed honestly now.


See also: [14_LOMBARD_BRIDGE_DECISION.md](14_LOMBARD_BRIDGE_DECISION.md) for the canonical decision freezing Lombard Bridge until one surviving credit product is chosen.


Foundation surfaces: [FOUNDATION_GOVERNANCE_QUEUE.md](../../../03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/FOUNDATION_GOVERNANCE_QUEUE.md) and [FOUNDATION_DECISIONS_REGISTER.md](../../../03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/FOUNDATION_DECISIONS_REGISTER.md).
