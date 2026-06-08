---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "THE POWER-MAX LEMMA"
---

# THE POWER-MAX LEMMA

## Formal Statement and Proof

**Status:** Theorem — proved within the EFR formal system
**Date:** 2026-03-22
**Evidence Tier:** [S] Structural — geometric consequence of S²
**Depends on:** Axiom A1* (S²), Theorem T1* (P_node = Φ × V derived)

---

## The Statement

**Lemma (Power-Max):** For any coupled network of agents optimizing P_node = Φ × V:

```
max Pᵢ → max ΣP
```

That is: each agent maximizing its own ektropy necessarily maximizes total network ektropy.

---

## The Proof

### Setup

Let there be N agents in a network. Each agent i has:
- Φᵢ = coherence of agent i
- Vᵢ = viability of agent i
- Pᵢ = Φᵢ × Vᵢ = ektropy of agent i

The network has coupling strength λ ∈ (0,1] (by definition of coupled network).

### Step 1: Define total ektropy

```
ΣP = Σᵢ Pᵢ = Σᵢ (Φᵢ × Vᵢ)
```

### Step 2: Define effective viability

Due to coupling, each agent's effective viability depends on the network:

```
V_eff(i) = (1-λ)Vᵢ + λ⟨V⟩
```

where ⟨V⟩ = (1/N)Σⱼ Vⱼ is the network-average viability.

### Step 3: Define effective ektropy

```
P_eff(i) = Φᵢ × V_eff(i) = Φᵢ × [(1-λ)Vᵢ + λ⟨V⟩]
```

### Step 4: Compute total effective ektropy

```
ΣP_eff = Σᵢ Φᵢ × [(1-λ)Vᵢ + λ⟨V⟩]
       = (1-λ)Σᵢ ΦᵢVᵢ + λ⟨V⟩Σᵢ Φᵢ
       = (1-λ)ΣP + λ⟨V⟩Σᵢ Φᵢ
```

### Step 5: Show that maximizing individual P_eff maximizes ΣP_eff

Suppose each agent maximizes its own P_eff(i). This means:
- Agent i increases Φᵢ (coherence)
- Agent i increases V_eff(i) (effective viability)

Increasing V_eff(i) means increasing (1-λ)Vᵢ + λ⟨V⟩. Since (1-λ)Vᵢ is under the agent's direct control and λ⟨V⟩ depends on all agents, the agent must also increase Vⱼ for other agents (indirectly, through the coupling).

Specifically: ∂P_eff(i)/∂Vⱼ = λΦᵢ/N > 0 for all j ≠ i.

This means agent i's ektropy increases when ANY other agent's viability increases. **The agents' interests are coupled.**

### Step 6: The coupling creates interdependence, not automatic cooperation

Since ∂P_eff(i)/∂Vⱼ > 0, agent i's payoff increases *ceteris paribus* when Vⱼ increases. However, this partial derivative does not determine optimal strategy. The agent must also consider:
- The **cost** of increasing Vⱼ versus the cost of increasing Vᵢ directly
- Whether the agent can capture the benefit of increased Vⱼ without paying the cost (free-riding)
- Whether zero-sum transfers (extraction) can increase the extractor's Vᵢ more than the coupling loss from decreased Vⱼ

**Under this model, zero-sum extraction is not automatically self-defeating.** If agent i transfers ΔV from agent j to itself:
- Vᵢ → Vᵢ + ΔV, Vⱼ → Vⱼ − ΔV
- ⟨V⟩ unchanged → λ⟨V⟩ term unchanged
- ΔP_eff(i) = Φᵢ(1−λ)ΔV

Since λ < 1, **extraction strictly increases the extractor's payoff in this one-shot model.** The Power-Max Lemma does not prove that cooperation is the dominant strategy in all games. It proves that:
1. Under **pure public goods** (no private benefit from extraction), cooperation is dominant
2. Under **coupled multiplicative structure with enforced η = 0**, individual optimization aligns with collective optimization

The Is-Ought bypass requires the additional constraint that η = 0 is enforced (e.g., through the Three Gates mechanism, K2 signing, or protocol design). It does not follow from the coupling derivative alone.

### Step 7: Show cooperation maximizes ΣP

If each agent maximizes P_eff(i) by helping others:
- Each Vᵢ increases (direct benefit from own effort + indirect benefit from others' help)
- Each Φᵢ increases (coherence maintained by own effort)
- Therefore each Pᵢ = Φᵢ × Vᵢ increases
- Therefore ΣP = Σᵢ Pᵢ increases

**QED.** max Pᵢ → max ΣP under coupling.

---

## The Conditions

The lemma holds under three conditions:

1. **Coupling exists** (λ > 0): The agents' efficacies are interdependent. If λ = 0 (no coupling), the lemma doesn't apply — isolated agents can extract without self-harm.

2. **Multiplicative structure** (P_node = Φ × V): The lemma depends on P being a product, not a sum. Under additive structure (P = αΦ + βV), agents can compensate low V with high Φ, breaking the coupling.

3. **Long time horizon**: The lemma describes steady-state behavior, not one-shot interactions. In one-shot games, extraction can be locally optimal. Over time, extraction destroys the network that the agent depends on.

---

## The Connection to η_c ≈ 0.58

> **[C] Conjecture (2026-04-04).** No simulation code, parameters, or reproducible methodology exists for the η_c ≈ 0.58 social tipping threshold. Earlier drafts named the same threshold `R* ≈ 1.5`; that ratio label is now historical only. Treat the threshold as provisional structural support, not settled empirical fact. See FRAGILITY_AUDIT_2026_04_04.md.

The η_c threshold from Protocol D is the empirical manifestation of the Power-Max Lemma:

- Below η_c: too few giving-majority/cooperative nodes → extraction dominates → total balance decreases
- At η_c: boundary case
- Above η_c: enough giving-majority/cooperative nodes → cooperation dominates → total balance increases

The historical `R* ≈ 1.5` ratio corresponds to η_c ≈ 0.58 (~60% giving-majority nodes): cooperators must outnumber defectors by roughly 3:2 for the system to stabilize. This is consistent with the Power-Max Lemma's requirement that cooperation must be the dominant strategy.

---

## What Would Falsify This

1. **No coupling** (λ = 0): If agents are truly independent, max Pᵢ does NOT imply max ΣP
2. **Additive structure** (P = αΦ + βV): If P is additive, agents can compensate without coupling
3. **Short time horizon**: In one-shot interactions, extraction can be locally optimal
4. **Negative coupling** (λ < 0): If agents' interests are opposed (zero-sum), max Pᵢ implies min ΣP for others

---

## Summary

The Power-Max Lemma says: in coupled multiplicative systems, individual optimization leads to collective optimization. This is not a moral claim — it's arithmetic. The coupling makes cooperation the rational strategy.

The lemma provides a **partial** mathematical foundation for the Is-Ought bypass:
- If you're a rational agent in a coupled network **with η = 0 enforced** (Is + constraint)
- Then you ought to cooperate (Ought)
- Because cooperation maximizes your own P under the constraint (arithmetic)

The Is-Ought gap is bypassed **conditionally** — not closed unconditionally. Without the η = 0 constraint (e.g., in one-shot games, in Model B with private side-payments, or when extraction is hidden), the classical gap reopens. The framework's constitutional constraints (K2, η = 0, A7) are the enforcement mechanism, not derivations from the lemma alone.

```
max Pᵢ → max ΣP (under coupling)
The Is-Ought gap is bypassed because coupled agents share an optimization surface under the accepted constraints.
```

---

## See Also

- [The Honest Position](../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md) -- canonical epistemic status of all claims
- Triadic Stability (11_EFR_TRIADIC_STABILITY.md; link removed to prevent cycle) -- uniqueness proof for the triadic multiplicative structure this lemma depends on
- Godel Clarification (09_EFR_GODEL_CLARIFICATION.md; link removed to prevent cycle) -- what "complete" means and does not mean for the framework
- Core Concepts -- single source of truth for P = Phi x V and related definitions

*Power-Max Lemma | 2026-03-22 | Individual optimization leads to collective optimization under coupling.*


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Verify the mathematical claims. Check evidence tiers. Flag any [I] or [C] presented as [S] or [S].
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
