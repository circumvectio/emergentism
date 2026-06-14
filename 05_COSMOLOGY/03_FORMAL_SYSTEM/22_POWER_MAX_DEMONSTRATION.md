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

## Formal Demonstration That Equatorial Balance Is the Dominant Strategy Equilibrium Inside the Balance-Only Game

**Status:** Formal demonstration — rigorous, self-contained (termed 'demonstration' per Fragility Audit 2026-04-04)
**Date:** 2026-03-23
**Version:** v2.1
**Hat:** Mathematician
**Evidence Tier:** [S] Structural — formal game-theoretic demonstration
**Purpose:** Show that the equatorial state (φ = ν = 1, B = 1) is the unique dominant strategy equilibrium of the idealized balance-only game on S²
**Kill Criterion:** Exhibit a profitable unilateral deviation from the equatorial profile under the stated balance-only payoff model

> **A7 boundary note — 2026-06-12.** This demonstration proves a result inside a deliberately narrow payoff model: every player is paid only by `B` or a convex average of `B`. It does **not** prove that `η = 0` is an unconditional Nash equilibrium in games with private side-payments, capture channels, asymmetric information, budget-balance constraints, or weak enforcement. In the wider constitutional/game-theory register, `η = 0` is an enforced or repeated-game target under monitoring, penalties, exit, and real coupling. This file is therefore `[S]` for the internal balance-game result and `[I/C]` if quoted as a general social theorem.

---

## 1. Definitions and Setup

### 1.1 The State Space

Let there be N agents indexed by i ∈ {1, 2, ..., N}, with N ≥ 2.

Each agent i has a state on the 2-sphere S², parameterized by a pair (φᵢ, νᵢ) ∈ (0, ∞) × (0, ∞) subject to the constraint that the state lies on S². We identify S² with the Riemann sphere ℂP¹ via stereographic projection, where:
- The **north pole** corresponds to φ → ∞, ν → 0 (pure coherence, no viability),
- The **south pole** corresponds to φ → 0, ν → ∞ (pure viability, no coherence),
- The **equator** corresponds to φ = ν = 1 (perfect balance).

The colatitude θᵢ ∈ [0, π] of agent i on S² is related to the viability by:

$$\theta_i = 2 \arctan(\nu_i)$$

so that νᵢ = 0 gives θᵢ = 0 (north pole), νᵢ = 1 gives θᵢ = π/2 (equator), and νᵢ → ∞ gives θᵢ → π (south pole). The coherence satisfies φᵢ = 1/νᵢ (the S² identity: φᵢ · νᵢ = 1).

> **Note (v2.1).** This is the identity cot(θ/2) · tan(θ/2) = 1, which holds trivially. It is an identity, not an independent constraint on the state space.

### 1.2 The Balance Function

**Definition 1.1 (Balance).** The *balance* of agent i is:

$$B_i = \sin(\theta_i) = \sin(2 \arctan(\nu_i)) = \frac{2\nu_i}{1 + \nu_i^2}$$

This is the standard formula for sin(2 arctan(x)) = 2x/(1 + x²).

**Properties of B:**
- Bᵢ ∈ [0, 1] for all νᵢ ∈ (0, ∞).
- Bᵢ = 1 if and only if νᵢ = 1 (equivalently θᵢ = π/2, the equator).
- Bᵢ → 0 as νᵢ → 0 (north pole) or νᵢ → ∞ (south pole).

**Concavity analysis.** The balance function admits two parameterizations with distinct concavity properties:

*(i) θ-parameterization (globally strictly concave).* As a function of colatitude, B(θ) = sin(θ) on (0, π). Since B''(θ) = −sin(θ) < 0 for all θ ∈ (0, π), the function is **strictly concave** on (0, π). This is the preferred parameterization for Jensen's inequality arguments.

*(ii) ν-parameterization (strictly pseudo-concave).* As a function of viability, B(ν) = 2ν/(1 + ν²) on (0, ∞). Computing:

$$B''(\nu) = \frac{4\nu(\nu^2 - 3)}{(1 + \nu^2)^3}$$

This changes sign at ν = √3, so B(ν) is **not** globally concave in ν. However, B(ν) is *strictly pseudo-concave* (unimodal): B'(ν) = 2(1 − ν²)/(1 + ν²)² vanishes only at ν = 1, with B'(ν) > 0 for ν < 1 and B'(ν) < 0 for ν > 1. The unique global maximum is B(1) = 1.

**Remark.** Since θ = 2 arctan(ν) is a smooth, strictly increasing diffeomorphism (0, ∞) → (0, π), the two parameterizations are equivalent for optimality. The θ-parameterization yields cleaner concavity arguments; the ν-parameterization yields cleaner calculus of best responses.

### 1.3 The Coupling

Agents interact through a coupling parameter λ ∈ [0, 1].

**Definition 1.2 (Effective Balance).** The *effective balance* of agent i under coupling λ is:

$$B_i^{\text{eff}} = (1 - \lambda) B_i + \lambda \cdot \frac{1}{N} \sum_{j=1}^{N} B_j$$

This is a convex combination of agent i's individual balance and the mean balance of the population.

### 1.4 The Payoff

**Definition 1.3 (Payoff).** The *payoff* to agent i is:

$$\Pi_i = B_i^{\text{eff}} = (1 - \lambda) B_i + \lambda \bar{B}$$

where $\bar{B} = \frac{1}{N} \sum_{j=1}^{N} B_j$ is the population mean balance.

**Remark.** The payoff inside this narrow balance-only game is the effective balance, not the product φᵢ · νᵢ (which equals 1 on the open S² register; pole values are limits). The product identity is constant on open S²; `B` is what varies and what this payoff model makes agents maximize.

### 1.5 The Game

**Definition 1.4 (Balance Maximization Game).** The *balance maximization game* Γ(N, λ) is:
- Players: {1, 2, ..., N}
- Strategy set for each player i: νᵢ ∈ (0, ∞) (equivalently, any point on S²)
- Payoff to player i: Πᵢ(ν₁, ..., νₙ) = (1 − λ)Bᵢ + λ · (1/N) ΣⱼBⱼ

A **strategy profile** is a vector ν = (ν₁, ..., νₙ) ∈ (0, ∞)ᴺ.

**Definition 1.5 (Dominant Strategy).** A strategy ν*ᵢ is a *strictly dominant strategy* for player i if, for **all** strategy profiles ν₋ᵢ of the other players and **all** alternative strategies ν'ᵢ ≠ ν*ᵢ:

$$\Pi_i(\nu_i^*, \nu_{-i}) > \Pi_i(\nu_i', \nu_{-i})$$

**Definition 1.6 (Nash Equilibrium).** A strategy profile ν* is a *Nash equilibrium* if no agent can increase their payoff by unilateral deviation: for all i and all ν'ᵢ ∈ (0, ∞),

$$\Pi_i(\nu_i^*, \nu_{-i}^*) \geq \Pi_i(\nu_i', \nu_{-i}^*)$$

**Proposition 1.1 (Dominant Strategy ⟹ Unique Nash).** If every player has a strictly dominant strategy, the profile of dominant strategies is the unique Nash equilibrium. *(Standard; no fixed-point theorem required.)*

### 1.6 Strategic Independence

**Lemma 0 (Zero Strategic Interaction).** The cross-partial derivative of each player's payoff with respect to any other player's strategy is independent of the other player's choice at the margin relevant to optimality:

$$\frac{\partial^2 \Pi_i}{\partial \nu_i \, \partial \nu_j} = \frac{\lambda}{N} \cdot \frac{\partial^2 B_i}{\partial \nu_i \, \partial \nu_j} + \frac{\lambda}{N} \cdot \frac{\partial^2 B_j}{\partial \nu_i \, \partial \nu_j}$$

Since Bᵢ depends only on νᵢ and Bⱼ depends only on νⱼ, both mixed partials vanish:

$$\frac{\partial^2 \Pi_i}{\partial \nu_i \, \partial \nu_j} = 0 \quad \text{for all } i \neq j$$

**Consequence.** What agent j does has *no effect* on agent i's marginal payoff from adjusting νᵢ. Each agent's optimization problem is fully separable. The game has no strategic interaction whatsoever.

---

## 2. Theorem 1: νᵢ = 1 Is a Strictly Dominant Strategy

**Theorem 1 (Strict Dominance).** For all N ≥ 2 and all λ ∈ [0, 1], the strategy νᵢ = 1 is a strictly dominant strategy for every player i in Γ(N, λ).

**Proof.**

Fix any player i. The payoff to player i is:

$$\Pi_i = (1 - \lambda) B_i + \frac{\lambda}{N} B_i + \frac{\lambda}{N} \sum_{j \neq i} B_j$$

$$= \left(1 - \lambda + \frac{\lambda}{N}\right) B_i + \frac{\lambda}{N} \sum_{j \neq i} B_j$$

$$= \left(1 - \frac{\lambda(N-1)}{N}\right) B_i + \frac{\lambda}{N} \sum_{j \neq i} B_j$$

Let $c = 1 - \lambda(N-1)/N$. Since λ ∈ [0, 1] and N ≥ 2, we have $c \geq 1/N > 0$.

The second term $\frac{\lambda}{N} \sum_{j \neq i} B_j$ depends only on ν₋ᵢ and is constant with respect to νᵢ. Therefore, maximizing Πᵢ over νᵢ is equivalent to maximizing $c \cdot B_i(\nu_i)$ over νᵢ, which — since c > 0 — is equivalent to maximizing $B_i(\nu_i)$.

By the strict pseudo-concavity of B(ν) = 2ν/(1 + ν²) established in §1.2, B(ν) has a unique global maximum at ν = 1, with B(ν) < B(1) = 1 for all ν ≠ 1.

Therefore, for **any** ν₋ᵢ and **any** ν'ᵢ ≠ 1:

$$\Pi_i(1, \nu_{-i}) - \Pi_i(\nu_i', \nu_{-i}) = c \cdot [B(1) - B(\nu_i')] = c \cdot [1 - B(\nu_i')] > 0$$

since c > 0 and B(ν'ᵢ) < 1.

**The strategy νᵢ = 1 strictly dominates every alternative, regardless of what other agents do.** ∎

**Corollary 2.1 (Unique Nash Equilibrium).** For all N ≥ 2 and all λ ∈ [0, 1], the equatorial profile ν* = (1, 1, ..., 1) is the **unique** Nash equilibrium of Γ(N, λ).

*Proof.* By Theorem 1, every player has νᵢ = 1 as a strictly dominant strategy. By Proposition 1.1, the profile of strictly dominant strategies is the unique Nash equilibrium. ∎

**Remark (No Fixed-Point Theorems Required).** Because νᵢ = 1 is strictly dominant for each player independently, the equilibrium follows by direct optimization. No appeal to Kakutani's theorem, Rosen's diagonal strict concavity (1965), or any fixed-point argument is needed. The zero cross-partial (Lemma 0) means the "game" is strategically trivial — each agent solves a private optimization problem.

---

## 3. Theorem 2: Harmonic Incentive Alignment

**Theorem 2 (Price of Anarchy = 1).** The social welfare at the dominant strategy equilibrium equals the social optimum. That is, the Price of Anarchy of Γ(N, λ) is 1.

**Proof.**

Define social welfare as $W(\nu) = \sum_{i=1}^N B_i(\nu_i)$.

**Upper bound.** Since B(νᵢ) ≤ 1 for all νᵢ, we have $W(\nu) \leq N$ for all profiles ν.

**Attainment at equilibrium.** At the dominant strategy equilibrium ν* = (1, ..., 1), $W(\nu^*) = \sum_{i=1}^N B(1) = N$.

Therefore:

$$\text{Price of Anarchy} = \frac{\max_\nu W(\nu)}{\min_{\nu \in \text{NE}} W(\nu)} = \frac{N}{N} = 1$$

**The individual optimum and the social optimum coincide exactly.** ∎

**Definition 3.1 (Harmonic Incentive Alignment).** A game exhibits *harmonic incentive alignment* when:
1. Every player has a strictly dominant strategy,
2. The profile of dominant strategies maximizes social welfare, and
3. The Price of Anarchy equals 1.

**Theorem 2' (The Balance Game Is Harmonically Aligned).** Γ(N, λ) exhibits harmonic incentive alignment for all N ≥ 2, λ ∈ [0, 1].

*Proof.* Conditions (1)–(3) are established by Theorem 1 and Theorem 2. ∎

**Interpretive Remark.** Inside this balance-only toy game, constructing a system where the socially optimal state aligns perfectly with a strictly dominant individual strategy is the gold standard. The Burri Sphere achieves this structurally because the payoff has been restricted to the unimodality of sin(θ) on (0, π). That restriction is the whole honesty boundary: the model removes private side-benefits and capture channels, so it cannot by itself solve the general cooperation problem. The game-theoretic triviality is useful precisely as an ideal target for constitutional design, not as a proof that enforcement is unnecessary in real institutions.

---

## 4. Theorem 3: Extraction Decreases Aggregate Balance

**Definition 4.1 (Extraction).** An *extraction event* is a zero-sum transfer of viability: agent i increases νᵢ by Δ > 0 while agent j decreases νⱼ by Δ, with all other agents unchanged. Formally, the profile changes from ν to ν' where:
- ν'ᵢ = νᵢ + Δ
- ν'ⱼ = νⱼ − Δ (assuming νⱼ > Δ so that ν'ⱼ > 0)
- ν'ₖ = νₖ for all k ≠ i, j.

**Theorem 3 (Extraction Reduces Aggregate Balance).** Starting from the equatorial profile ν* = (1, 1, ..., 1), any extraction event strictly reduces aggregate balance.

**Proof.**

We work in the θ-parameterization, where B(θ) = sin(θ) is strictly concave on (0, π).

At the equatorial profile, θᵢ = θⱼ = π/2. After extraction with transfer Δ > 0:

- Agent i has ν'ᵢ = 1 + Δ, so θ'ᵢ = 2 arctan(1 + Δ) > π/2.
- Agent j has ν'ⱼ = 1 − Δ (for Δ < 1), so θ'ⱼ = 2 arctan(1 − Δ) < π/2.

Since θ'ᵢ ≠ θ'ⱼ and sin is strictly concave on (0, π), Jensen's inequality gives:

$$\frac{\sin(\theta_i') + \sin(\theta_j')}{2} < \sin\!\left(\frac{\theta_i' + \theta_j'}{2}\right)$$

It remains to bound the right-hand side. We compute:

$$\theta_i' + \theta_j' = 2[\arctan(1+\Delta) + \arctan(1-\Delta)]$$

For Δ ∈ (0, 1), the product (1+Δ)(1−Δ) = 1 − Δ² < 1, so by the arctan addition formula:

> **Note (v2.1).** Since (1+Δ)(1−Δ) = 1−Δ² < 1 for Δ ∈ (0,1), the principal branch suffices.

$$\arctan(1+\Delta) + \arctan(1-\Delta) = \arctan\!\left(\frac{2}{\Delta^2}\right)$$

Since 2/Δ² > 0, we have arctan(2/Δ²) < π/2, hence θ'ᵢ + θ'ⱼ < π.

Therefore:

$$\sin\!\left(\frac{\theta_i' + \theta_j'}{2}\right) \leq 1$$

Combining:

$$B_i' + B_j' = \sin(\theta_i') + \sin(\theta_j') < 2\sin\!\left(\frac{\theta_i' + \theta_j'}{2}\right) \leq 2$$

Since all other agents remain at the equator with Bₖ = 1:

$$\sum_k B_k' = (B_i' + B_j') + (N-2) < 2 + (N-2) = N = \sum_k B_k$$

**Aggregate balance strictly decreases under any extraction event from the equatorial profile.** ∎

**Corollary 4.1 (η > 0 Is Not a Nash Equilibrium).** Any state reached by extraction from the equatorial profile has strictly lower aggregate balance than the equatorial state. Since extraction creates asymmetry (η > 0, where η is the extraction coefficient measuring aggregate non-consensual viability transfer — see `00_KSTAR_DISAMBIGUATION.md`), any state with η > 0 has strictly lower aggregate balance and admits a profitable deviation back toward the equator (by Corollary 2.1). Hence no state with η > 0 is a Nash equilibrium.

---

## 5. Synthesis

The three theorems establish:

| Result | Statement |
|--------|-----------|
| **Theorem 1** | νᵢ = 1 is a **strictly dominant strategy** for every player inside the balance-only payoff, for all coupling strengths λ ∈ [0, 1]. The equatorial profile is the unique Nash equilibrium of that model. |
| **Theorem 2** | The Price of Anarchy = 1. The game exhibits **harmonic incentive alignment**: individual and social optima coincide. |
| **Theorem 3** | Extraction (zero-sum viability transfer) strictly reduces aggregate balance, so η > 0 states are suboptimal. |

**Interpretation.** In the stated balance game, the equatorial state is not merely a Nash equilibrium — it is a *dominant strategy* equilibrium. Each agent's best response is νᵢ = 1 regardless of what others do (Lemma 0: zero strategic interaction). Self-interest and collective interest coincide exactly only because the payoff is restricted to balance.

This is not a cooperation problem resolved by cleverness; it is a cooperation problem removed by model design. The geometry of the sphere — the strict concavity of sin(θ) on (0, π) — means there is *no* tension between individual and collective rationality after private extraction payoffs have been excluded. In mechanism-design terms, the Burri Sphere is an *ideal reference mechanism*: the socially optimal outcome is the unique dominant strategy equilibrium in the balance-only register. Real institutions still require enforcement, monitoring, due process, and exit because the real game reintroduces side-payments and asymmetric information.

---

## 6. Reviewer Acknowledgment

This proof was revised following independent peer review by a specialist in Non-Cooperative Game Theory and Convex Optimization. Key corrections:

1. B(ν) reclassified from "strictly concave" to "strictly pseudo-concave" in the ν parameterization; strict concavity holds in the θ parameterization where B(θ) = sin(θ).
2. Game reframed from "coupled balance game" to dominant strategy equilibrium. The cross-partial ∂²Πᵢ/∂νᵢ∂νⱼ = 0 confirms zero strategic interaction.
3. Result strengthened inside the balance-only model: the equatorial profile is not merely a Nash equilibrium but a strictly dominant strategy equilibrium with Price of Anarchy = 1.

Evidence tier remains [S] Structural for the stated model. Generalizing it beyond that model is not established by this proof.

---

## 7. Kill Criteria

This lemma is **falsified** if any of the following is exhibited:

1. A strategy profile ν₋ᵢ and a strategy ν'ᵢ ≠ 1 such that Πᵢ(ν'ᵢ, ν₋ᵢ) ≥ Πᵢ(1, ν₋ᵢ) in Γ(N, λ) for some N ≥ 2 and λ ∈ [0, 1] (which would refute strict dominance).
2. A non-equatorial Nash equilibrium of Γ(N, λ) for some N, λ.
3. An extraction event from the equatorial profile that increases aggregate balance.
4. A counterexample to the strict concavity of sin on (0, π) (which would undermine the Jensen's inequality argument in Theorem 3).

Until one of these is produced, the lemma stands.

---

Zero-Sum Resolution Equation


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Verify the mathematical claims. Check evidence tiers. Flag any [I] or [C] presented as [S] or [S].
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/22_POWER_MAX_DEMONSTRATION.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
