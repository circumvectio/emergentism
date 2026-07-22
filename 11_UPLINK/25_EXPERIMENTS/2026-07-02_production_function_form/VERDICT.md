---
title: "Verdict — Production-function form: the agency-register P = Φ × V"
date: 2026-07-02
status: "RECORDED HISTORICAL VERDICT — result unchanged"
evidence_tier: "[B] reproducible result on a real public dataset; [I] interpretation"
data: "Munnell US-states productivity panel (Rdatasets/plm/Produc.csv), n=816 (48 states × 17 yrs, 1970-1986). Y=gsp, L=emp, K=pc+pcap."
provenance: "Executes the agency-register test that supersedes the GFS well-being test (see ../2026-07-02_gfs_pooled_multiplicative_vs_additive/VERDICT.md post-verdict correction). run_prodfn.py, RUN_OUTPUT.txt."
---

# Verdict — The Symmetric Product, on Real Output Data

## Result

**The framework's specific claim — flourishing/output is a *symmetric, balanced* product `Φ × V` (the form the `B = sin θ` / L4-apex superstructure requires) — is DECISIVELY REJECTED. All four pre-registered kill-criteria FAIL.**

This is the *agency* operationalization you asked for (output = labor × capital = means × execution), not the well-being survey. Run properly, the symmetric product fails **harder** here than the mis-operationalized GFS test did.

## Numbers (10-fold CV RMSE on output Y — lower is better; reproducible via `run_prodfn.py`)

| Model | CV RMSE | verdict |
|---|---:|---|
| **E — CES** (best ρ = −0.9) | **6,445** | best; ρ≈−1 is the **near-linear / high-substitution** end, *not* the product |
| A — additive (levels) `c + aL + bK` | 6,721 | the "sum" — essentially ties the winner |
| B — Cobb-Douglas, **free** elasticities | 6,799 | multiplicative, but no better than additive |
| D — Leontief / `min(L,K)` | 9,142 | perfect-complements: worse |
| **C — product-unit `Φ×V` (the framework's literal claim)** | **580,799** | catastrophically misspecified |

Cobb-Douglas elasticities (full sample): **labor a = 0.611, capital b = 0.442** (a+b = 1.05).

## Kill-criteria (all pre-registered in `run_prodfn.py`)

| # | Criterion | Result | Why |
|---|---|---|---|
| K1 | multiplicative beats additive | **FAIL** | additive (6,721) **ties/edges** Cobb-Douglas (6,799) out-of-sample — the product earns no advantage |
| KC2 | symmetric balance-product (a≈b, a+b≈1) | **FAIL** | a=0.61 ≠ b=0.44 — labor and capital enter **asymmetrically**, so there is **no `Φ=ν` equator optimum** |
| KC2b | literal `Φ×V` (unit elasticities) ≈ general CD | **FAIL** | forcing a=b=1 gives a+b=2 (wrong returns-to-scale) → an ~85× worse fit |
| K3 | CES substitution ρ ≈ 0 (Cobb-Douglas family) | **FAIL** | best ρ = −0.9, at the **additive/linear** end, away from the product |

## What this kills

- **The symmetric, unit-elasticity, balanced product `Φ × V`.** Real output is not it: the factors are asymmetric (0.61 vs 0.44), so there is no balance-at-the-equator optimum, and the literal unit product is badly misspecified. The `B = sin θ` / L4-apex machinery, which *needs* the symmetric product, gets no support.
- **Even the weak "it's multiplicative, not additive" leg** — additive fits at least as well here, and CES prefers a near-linear (highly substitutable) form. In this data, labor and capital **substitute**; they do not multiply in the framework's rigid sense.

## What survives — and the caveat that keeps this honest (fair to the framework)

- **The zero-factor catastrophe is NOT tested here, because this data never samples near-zero inputs.** Every US state has substantial labor *and* capital, so the one regime where a product genuinely beats a sum — one factor → 0 → total collapse — is never observed. When both factors are bounded away from zero, additive ≈ multiplicative locally (first-order Taylor), and no dataset without near-zero cases can separate them. This is exactly the GFS "μ-limit / below-threshold additive is sufficient" point, and it is real.
- So the framework's **true surviving claim is the weak one**: *conjunction* — you need both (no axe → 0; no skill → 0). That is almost certainly true, and this test does not touch it. But conjunction is satisfied by `min`, by Cobb-Douglas, and by the product alike — it does **not** single out `Φ×V`, and it does not deliver the balance-optimum the framework is built on.
- **Honest inflation note:** the product-unit's 580,799 is exaggerated by exponential smearing on a badly-misspecified model; treat it as "decisively rejected," not as a precise 85× ratio.

## Net across both registers

The agency reframe (correct as a critique of the GFS verdict) does **not** rescue the multiplicative claim. In **both** registers now tested — survey well-being (GFS) and real production/agency (Munnell) — the framework's specific balanced-product structure fails. What survives is only the untested, form-agnostic conjunction ("need both near zero"). The teleological bridge does not earn `[I] → [B]`; it earns a sharper `[I]`: *"conjunction near the boundary, of unknown functional form, with no demonstrated symmetric-balance optimum."*

## The one test that could still earn it

Isolate the surviving claim: a **task/production dataset that samples near-zero inputs** — subjects with the skill but *no tool*, or the tool but *no skill* — and test whether output collapses to ~0 (product/min) rather than degrading linearly (additive). That is the only place `Φ×V` can beat the sum, and it is the only test that would move the claim from `[I]` toward `[B]`.

*— Reproducible local result; not canon, deployment evidence, or external replication.*
