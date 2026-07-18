---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "BALANCE-SCORE EXCLUSION — scalar fixture only"
---

# THE BALANCE-SCORE EXCLUSION

## A Scalar Demonstration That the Defined Transfer Lowers `B` at Its Maximum

**Status:** Active Kintsugi repair — scalar score comparison; Nash claim retired
**Hat:** Mathematician
**Evidence Tier:** [S] Structural — formal convergence argument
**Date:** 2026-03-23
**Version:** v2.1
**Depends on:** reciprocal chart and declared balance function; Demonstration 22 owns the separate scalar Nash result

> **A7 boundary note — 2026-06-12.** This document proves a balance-payoff result at equatorial profiles. "Extraction is irrational" means "extraction lowers the extractor's `B` score in the stated balance game." It does **not** prove that extraction is irrational in every real game, that `η = 0` is an unconditional Nash equilibrium, or that private side-payments cannot dominate without enforcement. The wider doctrine reads this as a constitutional target: restore real coupling, monitoring, penalties, due process, and exit so the social game approximates the balance-only result.

---

## 1. DEFINITIONS AND NOTATION

**Definition 1.1 (The Burri Sphere).** The *Burri Sphere* is S² = CP¹ with colatitude θ ∈ [0, π] and azimuthal longitude ψ ∈ [0, 2π).

**Definition 1.2 (Dual stereographic coordinates).** The dual coordinate functions are:

$$\varphi = \cot(\theta/2), \qquad \nu = \tan(\theta/2)$$

satisfying the fundamental constraint φ · ν = 1 for all θ ∈ (0, π).

**Definition 1.3 (The equator).** The *equator* is the set:

$$E = \{p \in S^2 : \theta(p) = \pi/2\} = \{p \in S^2 : \varphi(p) = \nu(p) = 1\}$$

**Definition 1.4 (Balance function).** The *balance function* B: S² → [0, 1] is:

$$B(\theta) = \sin\theta$$

**Definition 1.5 (Tangent moves).** At a point p ∈ S² with coordinates (θ, ψ), a *move* is a tangent vector v ∈ T_p(S²). In coordinates, v = (dθ, dψ). The move induces changes in the dual coordinates:

$$d\varphi = -\frac{1}{2}\csc^2(\theta/2) \, d\theta, \qquad d\nu = \frac{1}{2}\sec^2(\theta/2) \, d\theta$$

At the equator (θ = π/2):

$$d\varphi = -d\theta, \qquad d\nu = d\theta$$

(using csc²(π/4) = 2, sec²(π/4) = 2, and absorbing the factor 1/2).

**Definition 1.6 (The four cardinal moves).** At the equator, the four cardinal moves are:

| Move | Symbol | Direction | dθ | Effect on φ | Effect on ν |
|------|--------|-----------|----|-------------|-------------|
| Arjuna | ↑φ | North | dθ < 0 | dφ > 0 (gains meaning) | dν < 0 (loses capability) |
| Kṛṣṇa | ↑ν | South | dθ > 0 | dφ < 0 (loses meaning) | dν > 0 (gains capability) |
| Kali | ↓φ | South | dθ > 0 | dφ < 0 (excises false meaning) | dν > 0 (gains capability) |
| Extraction | ↓ν (victim) | — | — | — | victim loses ν, extractor gains ν |

> **Note (v2.1).** The four "operators" reduce to two geometric directions on S² (north and south in θ). Arjuna (↑φ) and Kali (↓φ) both move south-to-north or north-to-south respectively. The additional two are distinguished by multi-agent context (self-move vs. extraction, constructive vs. corrective), not by single-agent geometry.

**Remark 1.7 (Directional semantics of extraction).** Extraction is not a single-agent move on S² but a *transfer* between two agents. In an extraction event:

- The **extractor** gains viability: Δνᵢ > 0. This moves the extractor *south* on S² (toward the Kṛṣṇa pole, dθ > 0, ↑ν). The extractor's ν increases beyond 1.
- The **victim** loses viability: Δνⱼ < 0. This moves the victim *north* on S² (toward the Arjuna pole, dθ < 0, ↓ν). The victim's ν decreases below 1.

The distinction between extraction and legitimate moves (Kṛṣṇa's self-development, Kali's corrective redistribution) lies not in direction but in *source and consent*: extraction takes from another agent without mutual benefit.

**Definition 1.8 (Multi-agent system).** A *multi-agent system* consists of N agents, each occupying a position on S². Agent i has coordinates (θᵢ, ψᵢ) and dual coordinates (φᵢ, νᵢ) with φᵢ · νᵢ = 1.

**Definition 1.9 (Self-move vs. extraction).** A *self-move* by agent i changes (θᵢ, ψᵢ) without affecting any other agent's coordinates. An *extraction* by agent i from agent j is an operation in which:

1. Agent i's viability increases: Δνᵢ > 0 (extractor moves south, ↑ν)
2. Agent j's viability decreases: Δνⱼ < 0 (victim moves north, ↓ν)
3. The total viability is conserved: Δνᵢ + Δνⱼ = 0

The extraction transfers viability from j to i while holding the total constant.

**Definition 1.10 (Extraction coefficient).** The *extraction coefficient* η for the system is:

$$\eta = \sum_{i=1}^{N} \max(0, \Delta\nu_i^{\text{ext}})$$

where Δνᵢᵉˣᵗ denotes the change in νᵢ due to extraction (not self-adjustment). η = 0 means no extraction occurs.

> **Note (v2.1).** η is formally defined as the extraction coefficient in Packet F2. Here it measures total extraction volume in the game.

**Definition 1.11 (Constraint propagation).** After extraction, each agent must still satisfy the fundamental constraint. If agent i has νᵢ → νᵢ + Δν after extraction, then:

$$\varphi_i \to \frac{1}{\nu_i + \Delta\nu}$$

This is not an independent assumption; it follows from φ · ν = 1.

---

## 2. THE BALANCE MAXIMUM THEOREM

**Lemma 2.1 (Balance as a function of ν).** For an agent with viability ν > 0, the balance is:

$$B(\nu) = \sin(2\arctan(\nu)) = \frac{2\nu}{1 + \nu^2}$$

*Proof.* From ν = tan(θ/2), we get θ = 2 arctan(ν). Applying the double-angle identity:

$$\sin\theta = \sin(2\arctan(\nu)) = 2\sin(\arctan(\nu))\cos(\arctan(\nu))$$

Using $\sin(\arctan(x)) = x/\sqrt{1+x^2}$ and $\cos(\arctan(x)) = 1/\sqrt{1+x^2}$:

$$B(\nu) = 2 \cdot \frac{\nu}{\sqrt{1+\nu^2}} \cdot \frac{1}{\sqrt{1+\nu^2}} = \frac{2\nu}{1 + \nu^2}$$

**Verification:** At ν = 1 (equator): B(1) = 2/(1+1) = 1. ✓
At ν = 0 (north pole): B(0) = 0. ✓
As ν → ∞ (south pole): B → 0. ✓ ∎

**Theorem 2.2 (The equator is the unique global maximum of B).** The function $B(\nu) = 2\nu/(1 + \nu^2)$ for ν ∈ (0, ∞) achieves its unique global maximum at ν = 1, with B(1) = 1.

*Proof.*

**Step 1.** Compute the first derivative:

$$B'(\nu) = \frac{d}{d\nu}\left(\frac{2\nu}{1 + \nu^2}\right) = \frac{2(1 + \nu^2) - 2\nu \cdot 2\nu}{(1 + \nu^2)^2} = \frac{2(1 - \nu^2)}{(1 + \nu^2)^2}$$

**Step 2.** Find critical points. Setting B'(ν) = 0:

$$2(1 - \nu^2) = 0 \implies \nu^2 = 1 \implies \nu = 1$$

(since ν > 0, we discard ν = −1).

**Step 3.** Compute the second derivative:

$$B''(\nu) = \frac{d}{d\nu}\left(\frac{2(1 - \nu^2)}{(1 + \nu^2)^2}\right)$$

Using the quotient rule with numerator f(ν) = 2(1 − ν²) and denominator g(ν) = (1 + ν²)²:

$$f'(\nu) = -4\nu, \qquad g'(\nu) = 4\nu(1 + \nu^2)$$

$$B''(\nu) = \frac{-4\nu(1+\nu^2)^2 - 2(1-\nu^2) \cdot 4\nu(1+\nu^2)}{(1+\nu^2)^4}$$

At ν = 1:

$$B''(1) = \frac{-4(1)(4) - 2(0)(4)(2)}{16} = \frac{-16}{16} = -1$$

**Step 4.** Since B'(1) = 0 and B''(1) = −1 < 0, the point ν = 1 is a strict local maximum by the second derivative test.

**Step 5.** To confirm this is the *global* maximum: B(ν) > 0 for all ν > 0, B(ν) → 0 as ν → 0⁺ and as ν → ∞, and there is exactly one critical point in (0, ∞). By the first derivative test, B is increasing on (0, 1) and decreasing on (1, ∞). Therefore ν = 1 is the unique global maximum. ∎

---

## 3. THE STRATEGIC EXCLUSION THEOREM

**Remark 3.0 (Why "strategic," not "geometric").** The post-extraction state (1+Δν, 1−Δν) *exists* on S² — the geometry does not forbid the move. What makes extraction irrational in this file is the *stated payoff structure*: the balance function B(ν) = 2ν/(1+ν²) peaks at ν = 1 and curves downward in every direction. Extraction is excluded not because the destination is geometrically impossible, but because it is a dominated move when the only payoff is balance. Add private side-payments or weak enforcement and this proof no longer settles the game.

### 3A. Primary Proof: The Purely Selfish Case (λ = 0)

**Theorem 3.1 (Strategic Exclusion — Selfish Case).** Consider an agent i at the equator (φᵢ = νᵢ = 1) in a multi-agent system. Suppose agent i extracts viability Δν > 0 from agent j, so that:

$$\nu_i \to 1 + \Delta\nu, \qquad \nu_j \to 1 - \Delta\nu$$

Then the extractor's balance *strictly decreases*:

$$B_i(1 + \Delta\nu) < B_i(1) = 1 \qquad \text{for all } \Delta\nu > 0$$

This holds even if agent i assigns zero weight to agent j's welfare (λ = 0), because the only modeled payoff is the extractor's own balance. No empathy or social preference is required inside the model; no claim is made here about games where extraction also pays private benefits outside `B`.

*Proof.*

**Step 1.** After extraction, agent i has viability νᵢ = 1 + Δν with Δν > 0. By Lemma 2.1:

$$B_i = \frac{2(1 + \Delta\nu)}{1 + (1 + \Delta\nu)^2}$$

**Step 2.** By Theorem 2.2, B(ν) achieves its unique global maximum at ν = 1. Since 1 + Δν > 1 (as Δν > 0), we have:

$$B_i = B(1 + \Delta\nu) < B(1) = 1$$

**Step 3.** The inequality is strict because ν = 1 is the *unique* maximum (Theorem 2.2, Step 5). No assumption about agent i's concern for others is used. The result is purely self-interested: the extractor harms *itself*. ∎

### 3B. Strengthening: The Coupled Case (λ > 0)

**Theorem 3.1* (Strategic Exclusion — Coupled Case).** If agent i assigns any positive weight λ > 0 to agent j's balance, the penalty for extraction is strictly greater than in the selfish case.

*Proof.* Suppose agent i's effective payoff is:

$$U_i = B_i + \lambda \, B_j, \qquad \lambda > 0$$

After extraction of Δν > 0 from j:

$$U_i = B(1 + \Delta\nu) + \lambda \, B(1 - \Delta\nu)$$

By Theorem 3.1, B(1 + Δν) < 1 (the selfish loss). By Corollary 3.3 below, B(1 − Δν) < 1 (the victim's loss). Therefore:

$$U_i < 1 + \lambda \cdot 1 = 1 + \lambda = U_i^{\text{equator}}$$

The total loss is:

$$\Delta U_i = [B(1+\Delta\nu) - 1] + \lambda[B(1-\Delta\nu) - 1] < 0$$

Coupling adds a secondary penalty term λ[B(1−Δν) − 1] < 0, but the primary result (Theorem 3.1) already establishes irrationality without it. ∎

**Corollary 3.2 (Extraction lowers balance at the equator).** For ANY Δν > 0, no matter how small, the extractor's balance decreases. There is no threshold below which extraction is beneficial in the balance-only payoff. The strategic exclusion is total only within that payoff model.

*Proof.* Theorem 3.1 holds for all Δν > 0 without restriction on magnitude. ∎

**Corollary 3.3 (The victim also loses balance).** The victim j, with νⱼ = 1 − Δν for Δν > 0, also loses balance:

$$B_j = B(1 - \Delta\nu) < B(1) = 1$$

*Proof.* Since 0 < 1 − Δν < 1 (assuming Δν < 1), and B is strictly increasing on (0, 1) by Theorem 2.2 Step 5, and 1 − Δν < 1, we have B(1 − Δν) < B(1) = 1. ∎

**Corollary 3.4 (Extraction is negative-sum for balance).** The total balance loss from extraction is:

$$\Delta B_{\text{total}} = B(1 + \Delta\nu) + B(1 - \Delta\nu) - 2$$

This quantity is strictly negative for all Δν ∈ (0, 1).

*Proof.* Define h(x) = B(1 + x) + B(1 − x) for x ∈ (0, 1):

$$h(x) = \frac{2(1+x)}{1+(1+x)^2} + \frac{2(1-x)}{1+(1-x)^2}$$

We have h(0) = 2. We compute h'(0):

$$h'(x) = B'(1+x) - B'(1-x)$$

At x = 0: h'(0) = B'(1) − B'(1) = 0. Now h''(0):

$$h''(x) = B''(1+x) + B''(1-x)$$

At x = 0: h''(0) = 2B''(1) = 2(−1) = −2 < 0.

Since h(0) = 2, h'(0) = 0, and h''(0) = −2 < 0, by Taylor expansion:

$$h(x) = 2 - x^2 + O(x^4) < 2 \quad \text{for small } x > 0$$

For the global result: since B achieves its unique maximum at ν = 1, and both 1 + x and 1 − x differ from 1 when x ≠ 0, we have B(1 + x) < 1 and B(1 − x) < 1, hence h(x) < 2. ∎

---

## 4. RETIRED NASH CLAIM — THE ACTION GAME WAS UNDER-SPECIFIED

> **[金] Kintsugi seam.** The former action list—`self-move`, `extract from j`,
> or `do nothing`—did not define move magnitudes, simultaneous transfer
> resolution, feasibility, or the outcome when another player extracts from the
> focal player. “Do nothing” therefore could not guarantee that the focal state
> remained at `B_i=1`, and the claimed unique-Nash proof did not follow.

No Nash theorem is live from that action list. The valid nearby result belongs
to [`22_POWER_MAX_DEMONSTRATION.md`](22_POWER_MAX_DEMONSTRATION.md), whose fully
specified scalar game `Γ(N,λ)` pays every player only through its own `B` and
the population mean. In that deliberately balance-only fixture, `ν_i=1` is
strictly dominant, the all-balanced scalar profile is the unique Nash
equilibrium, and the Price of Anarchy is 1. That theorem does not establish
`η=0` as a general equilibrium of real extraction games.

---

## 5. THE STRATEGIC EXCLUSION

**Theorem 5.1 (The Strategic Exclusion — Master Statement).** The exclusion of extraction at the equator is not a prohibition but a strategic fact inside the balance-only payoff, formalized as follows:

**(i) Maximum principle.** The equator is the unique global maximum of the balance function B(ν) = 2ν/(1 + ν²). Any displacement from ν = 1 decreases B.

**(ii) Extraction is a displacement.** Extraction maps νᵢ = 1 to νᵢ = 1 + Δν ≠ 1. It is a displacement from the maximum.

**(iii) Displacements from a strict maximum are strictly suboptimal.** B(1 + Δν) < B(1) for all Δν ≠ 0.

**(iv) Therefore:** For `0<Δν<1`, the defined scalar transfer from `(1,1)` to
`(1+Δν,1−Δν)` lowers both declared `B` scores. The coordinates remain
admissible; the chart does not forbid them. This is a score comparison, not a
dominance or equilibrium result for an under-specified action game.

*Proof.* This is a direct synthesis of Theorem 2.2 (scalar maximum), Theorem
3.1 (the extractor's score decreases), and Corollary 3.3 (the counterparty's
score decreases). The local curvature follows from `B''(1)=−1<0`. No Nash
claim is used. ∎

**Remark 5.2 (Saddle-free maximum).** The equator is not a saddle point. In the (θ, ψ) coordinates, B = sin θ depends only on θ. In the θ-direction, B''(π/2) = −sin(π/2) = −1 < 0. In the ψ-direction, ∂B/∂ψ = 0 and ∂²B/∂ψ² = 0 (B is ψ-independent). The Hessian at the equator is:

$$H = \begin{pmatrix} -1 & 0 \\ 0 & 0 \end{pmatrix}$$

This is negative semi-definite (eigenvalues −1 and 0). Along any direction with dθ ≠ 0, the balance strictly decreases. The ψ-direction is neutral (movement along the equator preserves balance). There is no direction in which balance increases. The equator is saddle-free.

---

## 6. DOMAIN BOUNDARY: EQUATOR VS. OFF-EQUATOR

**Remark 6.0 (Explicit domain of the theorem).** Theorem 3.1 and Corollaries
3.2–3.4 are scalar score comparisons *at the all-balanced profile*—where every
declared `ν_i=1`. Section 4's action-game Nash claim is retired. These results
do not claim that all redistribution is harmful in all states.

**Proposition 6.1 (Off-balance scalar correction raises both `B` scores).**
Consider an asymmetric two-agent scalar state with `ν₁=1+δ` and `ν₂=1−δ`
for `0<δ<1`. A declared transfer `0<Δν≤δ` from the first coordinate to the
second moves both toward `ν=1`. The aggregate score is:

$$\Sigma B = B(1 + \delta - \Delta\nu) + B(1 - \delta + \Delta\nu)$$

is strictly increasing in Δν for Δν ∈ (0, δ), achieving its maximum at Δν = δ (the equatorial state).

*Proof.* Taking the derivative with respect to Δν:

$$\frac{d\Sigma B}{d(\Delta\nu)} = -B'(1 + \delta - \Delta\nu) + B'(1 - \delta + \Delta\nu)$$

For `0<Δν<δ`, the first argument is greater than 1, so its derivative is
negative; the second is less than 1, so its derivative is positive. Therefore
`dΣB/d(Δν)>0`. At `Δν=δ`, both coordinates equal 1 and both individual scores
reach their declared maximum. No false global-concavity premise is needed. ∎

**Remark 6.2 (Operator analogy only `[I]`).** Proposition 6.1 can illustrate a
repair move in the selected operator vocabulary: within this score, shifting
two scalar coordinates toward 1 raises both `B` values. It does not establish
that a real party is bloated, another is starved, a transfer is authorized, or
redistribution is just. Those require measured constructs, consent, custody,
and bearer-complete Justice.

**Summary of domain boundaries:**

| Configuration | Redistribution effect | Governing result |
|---|---|---|
| All `νᵢ=1` | The defined scalar displacement lowers `B` | Theorem 3.1 |
| Pair `1+δ,1−δ` with `0<δ<1` | Moving both scalar coordinates toward 1 raises both `B` scores | Proposition 6.1 |
| Other scalar profiles | Effect requires direct evaluation; no global concavity or moral verdict is assumed | monotonicity of `B` on either side of 1 |

---

## 7. QUANTITATIVE ANALYSIS OF EXTRACTION LOSS

**Proposition 7.1 (Extraction loss formula).** For an agent at the equator who extracts Δν, the balance loss is:

$$\Delta B_i = B(1 + \Delta\nu) - 1 = \frac{2(1 + \Delta\nu)}{1 + (1 + \Delta\nu)^2} - 1 = -\frac{(\Delta\nu)^2}{2 + 2\Delta\nu + (\Delta\nu)^2}$$

*Proof.* Let u = 1 + Δν. Then:

$$B(u) - 1 = \frac{2u}{1 + u^2} - 1 = \frac{2u - 1 - u^2}{1 + u^2} = \frac{-(u-1)^2}{1 + u^2} = \frac{-(\Delta\nu)^2}{1 + (1+\Delta\nu)^2}$$

Expanding the denominator: 1 + (1 + Δν)² = 1 + 1 + 2Δν + (Δν)² = 2 + 2Δν + (Δν)². ∎

**Corollary 7.2 (Quadratic loss).** For small extractions (Δν ≪ 1):

$$\Delta B_i \approx -\frac{(\Delta\nu)^2}{2}$$

The loss is quadratic in the extraction amount. Even infinitesimally small extractions produce a loss, albeit a second-order one.

**Proposition 7.3 (Marginal balance of extraction is zero).** The first derivative of the extractor's balance with respect to Δν, evaluated at Δν = 0, is:

$$\left.\frac{dB_i}{d(\Delta\nu)}\right|_{\Delta\nu = 0} = B'(1) = 0$$

*Proof.* Direct from Theorem 2.2, Step 2. ∎

**Remark 7.4.** The vanishing first derivative might suggest that small extractions are "harmless." This is false. The second derivative B''(1) = −1 < 0 ensures that the loss, while second-order, is strictly negative for any Δν ≠ 0. The equator is a hilltop, not a plateau.

---

## 8. CHART-SCORE BEHAVIOR, NOT AN AUTOMATIC TAX

**Remark 8.1 (What the chart actually proves).** Inside the declared reciprocal
chart, increasing the coordinate `ν` beyond 1 forces `φ=1/ν` downward, and the
declared score `B(ν)=2ν/(1+ν²)` also decreases. This is an analytic property of
the coordinates and score. It does not show that a real agent accumulated a
resource, lost meaning, paid a tax, or became less successful.

A Pigouvian tax is an institutional mechanism with measured external costs,
an assessed base, enforcement, and distributional consequences. The chart
provides none of those things automatically. Any real non-extraction regime
still requires operational variables, authorization, monitoring, due process,
enforcement, and exit.

**Remark 8.2 (Optional resource-curse analogy `[I/C]`).** The economic resource
curse can motivate a comparison, but the chart does not formalize or explain
that empirical phenomenon. It only yields the following values for its own
dimensionless score. At `ν=2`:

$$B(2) = \frac{4}{5} = 0.80$$

while `B(1)=1.00`. At `ν=5`:

$$B(5) = \frac{10}{26} \approx 0.385$$

Thus the selected score is about 38.5% of its maximum. Interpreting `ν` as
wealth, capability, or hoarding—and interpreting lower `B` as a real
punishment—requires an independently tested bridge and domain-native rivals.

---

## 9. KILL CRITERIA

The analytic score result is invalid if a stated derivation fails under its
definitions; changing a definition creates a different model and does not
falsify the original identity. The domain interpretation is killed if its
operationalized score loses to a fair rival. Concretely:

1. An algebraic counterexample under the stated `B` and transfer definitions
   exposes a proof error.

2. A modified balance function is a rival specification; if it predicts or
   intervenes better in the target domain, the application of this `B` is
   retired there.

3. A failure of either score comparison in the explicitly defined
   `(1+Δν,1−Δν)` transfer for `0<Δν<1`

4. A tangent-direction counterexample under the defined `B` exposes a proof
   error in Remark 5.2.

5. Observed agents receiving unmodeled private benefits from extraction show
   that the scalar score is not their payoff; this kills the real-game bridge,
   not the chart identity.

---

## 10. ASSUMPTIONS REGISTER

> **Proof-local axiom convention.** The labels `A*n` below are
> **proof-local** to this document, distinguished by the star (`*`)
> from the operational canon `A1–A7` defined in
> [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md) and the
> substrate-selection wager `O1–O5` reconciled in
> [`../00_GOVERNANCE/00_MASTER_INDEX.md`](../../08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_MASTER_INDEX.md)
> Axiom Namespace section. When this proof references the operational
> canon or the substrate-selection axioms, it does so explicitly.

| # | Assumption | Status | Used in |
|---|-----------|--------|---------|
| A1* | S² = CP¹ with standard coordinates | Standard | Def 1.1 |
| A2* | φ = cot(θ/2), ν = tan(θ/2) | Definition | Def 1.2 |
| A3* | φ · ν = 1 on S² \ {N, S} | Follows from A2* | Def 1.2 |
| A4* | B = sin θ is the balance function | Definition | Def 1.4 |
| A5* | Extraction conserves total ν (zero-sum) | Definition | Def 1.9 |
| A6* | `B_i` is a declared scalar diagnostic, not a complete real utility | Definition | §§2–3 |
| A7* | All agents start at the equator | Premise of Thm 3.1 | Thm 3.1 |
| A8* | Domain: theorem holds at equatorial profiles; off-equator analysis in §6 | Explicit | Prop 6.1 |

---

## Reviewer Acknowledgment

This proof was revised following an internal role-based adversarial review
focused on non-cooperative game theory and mechanism design. No independently
identified external peer-review report is claimed. The historical notes below are retained as
provenance; the former dominance/Nash language and resource-curse promotion are
superseded by the Kintsugi repairs in §§4 and 8:

1. Directional definitions fixed: the extractor moves south (↑ν), the victim moves north (↓ν).
2. Renamed from "Geometric Exclusion" to "Strategic Exclusion"; current repair further narrows this to a scalar score comparison, not a dominance theorem.
3. Proof simplified: extraction lowers the extractor's `B` score even for λ=0 inside the balance-only payoff. Coupling adds secondary penalty but is not required for that internal result.
4. Domain explicitly bounded: the all-balanced transfer theorem is local to the declared scalar fixture; Proposition 6.1 is likewise score-local.
5. The former resource-curse connection is now a removable `[I/C]` analogy, not a formalization.

Evidence tier remains `[S]` for the stated scalar score comparisons. Any game,
economic, institutional, or moral generalization needs a separately specified
model and evidence.

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
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/24_GEOMETRIC_EXCLUSION_CONVERGENCE.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
