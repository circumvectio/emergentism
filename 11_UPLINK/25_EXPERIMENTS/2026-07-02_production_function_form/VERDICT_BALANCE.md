---
title: "Verdict — Balance-hump (Burri anthropic sphere): output peaks at Φ=ν?"
date: 2026-07-03
status: "RECORDED HISTORICAL VERDICT — result unchanged"
evidence_tier: "[B] reproducible result on real public data; [I] interpretation"
data: "Munnell US-states panel (Rdatasets/plm/Produc.csv), n=816. Y=gsp, L=emp, K=pc+pcap."
provenance: "Tests the CORRECTED claim (owner, 2026-07-03): P is multiplicative but the payoff is MAXIMIZED at balance Φ=ν (B=sin θ peaks at 1), a HUMP in the factor ratio — not the unbounded Cobb-Douglas of VERDICT.md. run_balance.py, RUN_OUTPUT_BALANCE.txt."
---

# Verdict — The Anthropic Balance Hump

## Result

**The anthropic balance claim (output multiplicative, maximized at Φ=ν) is REJECTED — and the data shows the *anti-pattern*: a balance *trough*, not a balance *peak*.**

Decomposing the two inputs into **scale** `S = (logL+logK)/2` and **ratio** `d = logL−logK`, and fitting a curvature term `d²`:

| Model | 10-fold CV RMSE on Y |
|---|---:|
| M0 scale-only | 6,870 |
| M1 Cobb-Douglas (ratio linear) | 6,658 |
| **M2 balance-curvature (adds d²)** | **6,080** ← best |

The curvature term is **real and strongly significant** — but the **wrong sign**:

> **d² coefficient = +0.274, t = +16.5.** A balance *hump* (max at Φ=ν, declining with imbalance) requires **d² < 0** (concave). The data gives **d² > 0 (convex)** — output is *minimized* near balance and **rises as either factor dominates.** Aggregate production **rewards specialization/imbalance; it does not reward balance.**

## Kill-criteria

| # | Criterion | Result |
|---|---|---|
| ANTHROPIC | a real balance *hump* exists (d²<0, \|t\|>2, beats CD out-of-sample) | **FAIL** (d² is significantly **positive** — a trough) |
| SYMMETRIC | the optimum sits at Φ=ν (d*≈0) | **N/A** — there is no maximum to locate; the extremum is a *minimum* |

## Why this is robust (not a units artifact)

"Balance = Φ=ν" depends on an arbitrary Φ↔ν exchange rate (labor-units vs capital-dollars), so the *location* of the extremum is normalization-dependent. But the **sign of the curvature (convex vs concave) is normalization-invariant** — a trough stays a trough under any rescaling of the axes. So "no hump; imbalance is rewarded" is a real finding about aggregate production, not an artifact of how I normalized.

## The honest caveats (fair to the framework)

1. **Scale.** This is **aggregate** production (whole economies). Comparative advantage means economies *should* reward specialization — so a convex trough is exactly what standard economics predicts, and it is not the regime the axe example is about. The **single-agent task scale** (fell one tree: skill × tool) is **not tested here** and remains the framework's best-surviving ground.
2. **The hump is stronger than the intuition.** Even at agent scale, the axe intuition delivers **conjunction** ("no axe → 0; unlimited chainsaws don't help one person *past a point*") — which is *plateau / min / diminishing returns*, **not** a hump. A master carpenter with "too many tools" does **not** produce *less*; the hump's distinctive feature — output **declining** past balance — is absent from the intuition itself. Conjunction ✓; symmetric balance-peak ✗, even conceptually.

## What survives / what dies

- **Dies:** the symmetric balance hump `B = sin θ` peaking at Φ=ν — the object the L4-apex / "the equator is the optimum" superstructure is built on. Rejected at aggregate scale with the opposite-sign curvature; unsupported by the agent-scale intuition it was meant to formalize.
- **Survives:** **conjunction** (need both; zero-factor collapse) — form-agnostic, plausibly true, still untested at agent scale.

## The one remaining test

Single-agent task data sampling **near-zero** inputs (skill-but-no-tool, tool-but-no-skill): does output (a) collapse to ~0 off either axis — conjunction; (b) **peak at balance and decline past it** — the anthropic hump; or (c) plateau — Leontief. Only (b) vindicates the anthropic sphere. Neither the aggregate data nor the axe intuition has produced (b) yet.

*— Reproducible local result; not canon, deployment evidence, or external replication.*
