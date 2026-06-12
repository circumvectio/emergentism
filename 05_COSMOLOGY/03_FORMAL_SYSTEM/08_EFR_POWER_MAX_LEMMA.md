---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/I]"
  canonical_phrase: "THE POWER-MAX LEMMA"
---

# THE POWER-MAX LEMMA

## Formal Statement and Proof

**Status:** Conditional theorem / design lemma inside the EFR formal system
**Date:** 2026-03-22
**Evidence Tier:** `[S]` for the conditional model theorem under its stated constraints; `[I]` for the symbiont/holobiont moral reading.
**Depends on:** Axiom A1* (S²), Theorem T1* (P_node = Φ × V derived), real coupling, long horizon, and enforceable `η = 0`.

---

## The Statement

**Lemma (Power-Max, constrained form):** For a coupled network of agents
optimizing `P_node = Φ × V`, under real coupling (`λ > 0`), a long enough
horizon for network effects to return, and enforced non-extraction (`η = 0`):
At the symbiont/holobiont boundary, this is the syntropic dyad: the individual
symbiont `i` maximizes durable world-line potential only on trajectories where
the collective holobiont `H` is preserved or raised -- `i raises H` and
`H raises i` under `η = 0`.

```
W_i(T) = ∫_0^T P_node,i(t) dt
P_node,H = Φ_H × V_H
A_η = admissible trajectories under λ > 0, multiplicative P_node,
      long horizon, and enforced η = 0

argmax_{τ ∈ A_η} W_i(T, τ)
  ⊆ { τ : ΔP_node,H(T, τ) ≥ 0 }

syntropic dyad:
  ΔP_node,i > 0 and ΔP_node,H > 0 under η = 0
```

That is: durable individual maximization is a constrained-frontier statement,
not an unconditional biconditional. The individual optimum is searched only
inside the admissible `η = 0` game; on that frontier, degrading the holobiont
degrades the field that returns as the individual's future viability. Without
the `η = 0` constraint, the derivative still shows interdependence, but it does
not by itself make cooperation dominant.

**Corollary (Syntropic Dyadism):** Let `i` be the individual symbiont and
`H` the collective holobiont / coupled sustaining field, with
`P_node,H = Φ_H × V_H` or, where `H` is modeled as an aggregate boundary,
`P_node,H = Σ_{k∈H}P_node,k` at the scale under analysis. Under the same four
conditions, the individual symbiont maximizes durable world-line potential only
along moves that preserve or raise `P_node,H` while preserving or raising
`P_node,i` under `η = 0`:

```
max durable W_i only on the syntropic frontier:
  ΔP_node,i ≥ 0 and ΔP_node,H ≥ 0 under η = 0
```

This is not a new unconditional proof of morality. It is the Power-Max Lemma
read at the symbiont/holobiont boundary: the syntropic dyad is the regime where
`i` raises `H` and `H` raises `i`; extraction is the regime where one apparent
gain is purchased by lowering the other, and is therefore outside the accepted
game rather than a permitted maximizer.

---

## The Proof

### Setup

Let there be N agents in a network. Each agent i has:
- Φᵢ = coherence of agent i
- Vᵢ = viability of agent i
- P_node,i = Φᵢ × Vᵢ = finite-node ektropy of agent i

The network has coupling strength λ ∈ (0,1] (by definition of coupled network).

### Step 1: Define total ektropy

```
ΣP_node = Σᵢ P_node,i = Σᵢ (Φᵢ × Vᵢ)
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
ΣP_node,eff = Σᵢ Φᵢ × [(1-λ)Vᵢ + λ⟨V⟩]
             = (1-λ)Σᵢ ΦᵢVᵢ + λ⟨V⟩Σᵢ Φᵢ
             = (1-λ)ΣP_node + λ⟨V⟩Σᵢ Φᵢ
```

### Step 5: Coupling creates a positive cross-derivative

Suppose agent i evaluates its own durable payoff through P_eff(i). Increasing
V_eff(i) means increasing (1-λ)Vᵢ + λ⟨V⟩. Since λ⟨V⟩ depends on all agents,
other agents' viability enters i's payoff even before moral language is added.

Specifically: ∂P_eff(i)/∂Vⱼ = λΦᵢ/N > 0 for all j ≠ i.

This means agent i's ektropy increases *ceteris paribus* when any other agent's
viability increases. **The agents' interests are coupled.** This proves
monotone interdependence, not automatic cooperation.

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

### Step 7: State the constrained frontier

Let `A_η` be the admissible trajectory set: real coupling, multiplicative
`P_node`, long horizon, and enforced `η = 0` (no hidden rent, capture,
coercion, or counterfeit accounting). Within `A_η`, a move that raises i by
degrading H is not a lawful maximizer; it is outside the accepted game or it
reappears as a future cost to i through the coupling term.

So the correct theorem is:

```
argmax_{τ ∈ A_η} W_i(T, τ)
  ⊆ { τ : ΔP_node,H(T, τ) ≥ 0 }
```

If each agent maximizes through the same admissible syntropic frontier:
- no agent is permitted to raise itself by lowering the coupled boundary;
- each viable cooperative improvement raises local `Φ` or `V` without hidden
  extraction;
- the aggregate `ΣP_node` rises when the individual improvements are real.

**QED, conditionally.** Coupling supplies the shared gradient; the
constitutional constraint blocks the private extraction route that would
otherwise dominate a one-shot game; the durable individual optimum is therefore
searched on the frontier where the holobiont is preserved or raised.

---

## The Conditions

The lemma holds under four conditions:

1. **Coupling exists** (λ > 0): The agents' efficacies are interdependent. If λ = 0 (no coupling), the lemma doesn't apply — isolated agents can extract without self-harm.

2. **Multiplicative structure** (P_node = Φ × V): The lemma depends on node score being a product, not a sum. Under additive structure (`P_add = αΦ + βV`), agents can compensate low V with high Φ, breaking the coupling.

3. **Long time horizon**: The lemma describes steady-state behavior, not one-shot interactions. In one-shot games, extraction can be locally optimal. Over time, extraction destroys the network that the agent depends on.

4. **Enforced non-extraction** (`η = 0`): Hidden rent, private side-payments,
   coercion, capture, or counterfeit accounting must be blocked. Coupling alone
   creates interdependence; `η = 0` makes the cooperative path incentive
   compatible.

---

## The Connection to η_c ≈ 0.58

> **[C] Conjecture (2026-04-04).** No simulation code, parameters, or reproducible methodology exists for the η_c ≈ 0.58 social tipping threshold. Earlier drafts named the same threshold `R* ≈ 1.5`; that ratio label is now historical only. Treat the threshold as provisional structural support, not settled empirical fact. See FRAGILITY_AUDIT_2026_04_04.md.

If later validated, the η_c threshold from Protocol D would be a social
expression of the Power-Max Lemma:

- Below η_c: too few giving-majority/cooperative nodes → extraction dominates → total balance decreases
- At η_c: boundary case
- Above η_c: enough giving-majority/cooperative nodes → cooperation dominates → total balance increases

The historical `R* ≈ 1.5` ratio corresponds to η_c ≈ 0.58 (~60% giving-majority nodes): cooperators would need to outnumber defectors by roughly 3:2 for the system to stabilize under that conjectural model. This is consistent with the Power-Max Lemma's conditional requirement that cooperation be enforced and numerous enough to outcompete extraction over the relevant horizon, but it is not current empirical evidence for the lemma.

---

## What Would Falsify This

1. **No coupling** (λ = 0): If agents are truly independent, max `W_i` need not preserve or raise `P_node,H`
2. **Additive structure** (`P_add = αΦ + βV`): If node scoring is additive, agents can compensate without coupling
3. **Short time horizon**: In one-shot interactions, extraction can be locally optimal
4. **No enforceable η discipline**: If extraction is hidden or privately
   profitable, the one-shot extraction route can beat cooperation locally.
5. **Negative coupling** (λ < 0): If agents' interests are opposed (zero-sum), max `W_i` can imply loss for the coupled field

---

## Summary

The Power-Max Lemma says: in coupled multiplicative systems with a long horizon
and enforced `η = 0`, durable individual optimization is searched on the
syntropic frontier where the coupled field is preserved or raised. This is not
an unconditional moral command. It is conditional arithmetic plus a mechanism
constraint: coupling makes each node care about the field, and `η = 0` prevents
local extraction from masquerading as power.

The lemma provides a **partial** mathematical foundation for the Is-Ought bypass:
- If you're a rational agent in a coupled network **with η = 0 enforced** (Is + constraint)
- Then you ought to cooperate (Ought)
- Because cooperation maximizes your own `P_node` under the constraint (arithmetic)

The Is-Ought gap is bypassed **conditionally** — not closed unconditionally. Without the η = 0 constraint (e.g., in one-shot games, in Model B with private side-payments, or when extraction is hidden), the classical gap reopens. The framework's constitutional constraints (K2, η = 0, A7) are the enforcement mechanism, not derivations from the lemma alone.

```
argmax_{τ ∈ A_η} W_i(T, τ)
  ⊆ { τ : ΔP_node,H(T, τ) ≥ 0 }

The Is-Ought gap is bypassed only inside the accepted game because coupled
agents share an optimization surface under enforceable non-extraction.
At the symbiont/holobiont boundary, durable individual world-line potential
requires preserving or raising P_node,H across the relevant horizon.
```

---

## See Also

- [The Honest Position](../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md) -- canonical epistemic status of all claims
- Triadic Stability (11_EFR_TRIADIC_STABILITY.md; link removed to prevent cycle) -- uniqueness proof for the triadic multiplicative structure this lemma depends on
- Godel Clarification (09_EFR_GODEL_CLARIFICATION.md; link removed to prevent cycle) -- what "complete" means and does not mean for the framework
- Core Concepts -- single source of truth for `P∞ = φ · ν = 1`, `P_node = Φ × V`, and related definitions

*Power-Max Lemma | 2026-03-22 | Individual optimization aligns with collective optimization under coupled multiplicative scoring, long horizon, and enforced η = 0.*


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
