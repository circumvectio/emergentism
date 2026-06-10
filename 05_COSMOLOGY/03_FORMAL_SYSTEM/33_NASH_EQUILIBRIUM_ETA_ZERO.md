---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "Geometric Constraint Enforcement in Multi-Agent Systems: η = 0 as Nash Equilibrium on S^2"
---

# Geometric Constraint Enforcement in Multi-Agent Systems: η = 0 as Nash Equilibrium on S^2

**Authors:** Research note prepared for the Emergentism.org corpus
**Date:** 2026-04-04
**Evidence Tier:** [S] Structural — the game-theoretic arguments are standard; the mapping to S^2 geometry is structural
**Status:** Working paper — open questions flagged
**Kill Criteria:** If private extraction benefit can be shown to exceed collective B-reduction even under repeated play with monitoring, the dominant-strategy result fails and the mechanism requires enforcement.

> **[A7 audit note — 2026-06-10, headline-discipline pass]** The title "η = 0 as Nash Equilibrium" is **conditional** and must be read with the abstract, not as an unconditional claim. η=0 is a strict dominant strategy **only in the degenerate pure-public-goods model** (no private benefit); with private side-payments it is **not** a Nash equilibrium (this paper's own Model-B / tragedy-of-the-commons result). The honest statement: η=0 is sustainable only (a) as a **repeated-game folk-theorem** equilibrium under sufficient patience — *flagged here as an open question, not proven* — or (b) as a **VCG/mechanism-design** outcome under monitoring + penalties + exit, i.e. **enforced low-extraction, not self-enforcing**. **Missing adversarial citation to add:** *Green & Laffont (1977)* — strategyproof + efficient ⇒ **not budget-balanced**; exact zero-extraction-with-balance is provably impossible in the general quasi-linear setting, so the Three-Gates penalty is the unavoidable surplus-burn the impossibility theorem predicts. The S² geometry is **presentational** (a re-parameterization of the public-goods first-order condition), not an independent source of equilibrium. Full grounding: `../../../03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/00_COSMOLOGY_AND_CONSTITUTION_AUDIT.md` Part II.

---

## Abstract

We formalize the multi-agent deliberation system of 9 active council roles in Agentz (7 seat-level Royal Directorates plus Chief of Staff synthesis and Vision Keeper witness) as an extraction game on the Riemann sphere S^2 and investigate whether the constitutional constraint η = 0 (zero extraction from cooperators) constitutes a Nash equilibrium. Under the pure public-goods formulation where all payoffs are mediated through the collective balance function B = sin(theta), η_i = 0 for all i is a strict dominant strategy inside this model. We then show this result breaks down when agents can capture private side-payments, recovering the classical tragedy-of-the-commons structure. The Three Gates mechanism (Receipt-Bound, Truth-Gated, Exit-Safe) is analyzed as a mechanism design solution that restores the dominant-strategy property by eliminating the private-benefit channel. We compare with Ostrom's design principles, Myerson's incentive compatibility, and cooperative game theory core stability. The key contribution is showing that S^2 geometry provides a natural formalization: the maximum of sin(theta) at the equator creates a geometric basin of attraction that standard Euclidean public goods games lack.

> **Notation note:** formula blocks retain ASCII `eta_i`, `theta`, and `phi` where that keeps the local derivation readable. Prose should read them as `η_i`, `θ`, and `φ`.

---

## 1. Formal Game Definition

### 1.1 Players

Let N = {1, 2, ..., 9} be the set of active council roles:

| i | Directorate | God-Operator | Domain |
|---|-------------|-------------|--------|
| 1 | Intelligence | Arjuna | Signal detection |
| 2 | Strategy | Kṛṣṇa | Scenario planning |
| 3 | Legal | Kālī (destroyer) | Compliance, eta audit |
| 4 | Engineering | Arjuna | Build, execute |
| 5 | Treasury | Kṛṣṇa | Resource allocation |
| 6 | Procurement | Kali (taker) | Acquire, negotiate |
| 7 | Sādhu | Śiva | Remainder analysis, axiomatic dissent |
| 8 | Chief of Staff synthesis | Viṣṇu | Compile, recommend |
| 9 | Vision Keeper | Viśvarūpa | Meta-witness, escalation |

### 1.2 Strategy Space

Each player i chooses an extraction level eta_i in [0, infinity).

- eta_i = 0: Full cooperation. Player contributes without extraction.
- eta_i > 0: Player extracts value from the system (information hoarding, resource capture, scope creep, etc.).

### 1.3 State Variable: Colatitude theta

The system state is described by colatitude theta on S^2, where:
- theta = 90 degrees (equator, L4): phi = nu = 1, maximum balance
- theta -> 0 degrees (north pole): phi -> infinity, nu -> 0 (coherence without viability)
- theta -> 180 degrees (south pole): phi -> 0, nu -> infinity (viability without coherence)

The constraint phi * nu = 1 holds on S^2 \\{N, S\\} (everywhere except the poles, where the cot/tan parameterization is undefined). The balance function is:

```
B(theta) = sin(theta)
```

### 1.4 Extraction-to-State Map

Define theta as a function of aggregate extraction:

```
theta(eta_1, ..., eta_9) = pi/2 - f(sum_{i=1}^{9} eta_i)
```

where f: [0, infinity) -> [0, pi/2] is continuously differentiable, strictly monotonically increasing, with f(0) = 0 and lim_{x->infinity} f(x) = pi/2.

A natural choice is f(x) = (pi/2) * (1 - e^{-alpha*x}) for some sensitivity parameter alpha > 0.

**Interpretation:** When total extraction is zero, the system sits at the equator (theta = 90 degrees). As aggregate extraction increases, the system moves toward a pole, and B decreases.

### 1.5 Payoff Functions

#### Model A: Pure Public Goods (No Private Benefit)

```
u_i(eta_1, ..., eta_9) = B(theta(eta_1, ..., eta_9)) = sin(pi/2 - f(sum_j eta_j)) = cos(f(sum_j eta_j))
```

Every player receives the same payoff — the collective balance. There is no private benefit to extraction.

#### Model B: Public Goods with Private Side-Payment

```
u_i(eta_1, ..., eta_9) = (1 - delta) * cos(f(sum_j eta_j)) + delta * g(eta_i)
```

where delta in (0,1) weights public vs. private benefit and g: [0, infinity) -> [0, infinity) is a concave, increasing function representing the private gain from extraction (e.g., g(eta) = eta^beta for 0 < beta < 1).

---

## 2. Nash Equilibrium Analysis

### 2.1 Theorem 1 (Dominant Strategy under Model A)

**Theorem.** Under Model A (pure public goods), eta_i = 0 is a strictly dominant strategy for every player i. Therefore eta* = (0, 0, ..., 0) is the unique Nash equilibrium (and in fact the unique dominant-strategy equilibrium).

**Proof.**

Fix any player i and any strategy profile eta_{-i} of the other players. Player i's payoff is:

```
u_i(eta_i, eta_{-i}) = cos(f(eta_i + sum_{j != i} eta_j))
```

Since f is strictly increasing, increasing eta_i strictly increases the argument of cos. Since f(0) = 0 and f maps into [0, pi/2], the argument cos(f(.)) lives in [0, pi/2], where cosine is strictly decreasing.

Therefore, for any eta_i' > eta_i >= 0:

```
f(eta_i' + sum_{j != i} eta_j) > f(eta_i + sum_{j != i} eta_j)
```

implies

```
cos(f(eta_i' + sum_{j != i} eta_j)) < cos(f(eta_i + sum_{j != i} eta_j))
```

So u_i is strictly decreasing in eta_i for any fixed eta_{-i}. The unique maximizer is eta_i = 0. Since this holds for all eta_{-i}, eta_i = 0 is a strictly dominant strategy.

**QED**

**Remark.** This result is "too clean" — it holds because there is no private return to extraction. The system is a pure public good with no rivalry. This is analogous to the trivial case of a public goods game where contributing costs nothing. The interesting question is Model B.

### 2.2 Theorem 2 (Tragedy under Model B: Existence of eta* > 0 Equilibria)

**Theorem.** Under Model B with delta > 0, g differentiable, g'(0) > 0, and f'(0) > 0, the strategy profile eta* = (0, ..., 0) is NOT a Nash equilibrium. There exists a symmetric Nash equilibrium at some eta* > 0.

**Proof.**

Consider player i's first-order condition at a candidate interior equilibrium:

```
du_i/d(eta_i) = -(1 - delta) * sin(f(sum_j eta_j)) * f'(sum_j eta_j) + delta * g'(eta_i) = 0
```

At the candidate eta = (0, ..., 0):

```
du_i/d(eta_i)|_{eta=0} = -(1 - delta) * sin(f(0)) * f'(0) + delta * g'(0)
                        = -(1 - delta) * sin(0) * f'(0) + delta * g'(0)
                        = 0 + delta * g'(0)
                        = delta * g'(0) > 0
```

Since the derivative is strictly positive at eta_i = 0, player i can increase payoff by choosing eta_i > 0. So eta = 0 is NOT a best response. The zero-extraction profile is not a Nash equilibrium.

For the symmetric interior equilibrium, set eta_i = eta* for all i. The FOC becomes:

```
(1 - delta) * sin(f(9 * eta*)) * f'(9 * eta*) = delta * g'(eta*)
```

Since the LHS is zero at eta* = 0 and grows as eta* increases (for small eta*), while the RHS = delta * g'(eta*) starts positive at eta* = 0 and decreases (g concave), a crossing exists by the intermediate value theorem.

**QED**

### 2.3 The AM-GM Connection

The constraint phi * nu = 1 on S^2 combined with the AM-GM inequality yields:

```
(phi + nu) / 2 >= sqrt(phi * nu) = 1
```

with equality iff phi = nu (the equator). This means the arithmetic mean of coherence and viability is minimized at the equator for fixed geometric mean. This is the *dual* of the standard interpretation: for fixed product, the most *balanced* allocation (equal shares) minimizes the sum. In the S^2 context, the equator is simultaneously the point of:

- Maximum balance: B = sin(theta) = 1
- Minimum total "spread": phi + nu minimized at 2
- Zero gradient: dB/d(theta) = cos(theta) = 0

The AM-GM structure means that any deviation from phi = nu = 1 increases the arithmetic mean while keeping the geometric mean fixed. Translated to the game: extraction creates asymmetry between phi and nu, moving the system off-equator, which reduces B for everyone. The AM-GM inequality thus provides the *geometric reason* why the equator is a basin of attraction — it is the unique minimizer of a convex functional on S^2 subject to the multiplicative constraint.

### 2.4 The Geometric Advantage over Euclidean Models

Standard public goods games on R^n have linear or quasi-linear payoffs, which produce corner solutions. The S^2 geometry provides:

1. **Compactness:** The strategy space maps to a compact manifold. No boundary issues.
2. **Curvature-induced concavity:** B = sin(theta) is strictly concave near theta = 90 degrees. This produces interior optima rather than boundary optima.
3. **Pole identification:** The poles (0 and infinity) are regular points, not singularities. The "tragedy" scenarios (pure coherence, pure viability) are geometric points, not asymptotic limits.
4. **Natural gradient flow:** dB/d(theta) = cos(theta) provides a gradient that points toward the equator from both hemispheres. This is a geometric restoring force absent in Euclidean models.

---

## 3. The Three Gates as Mechanism Design

### 3.1 The Problem

Model B shows that when private extraction benefits exist, eta = 0 is unstable. The Three Gates are a mechanism to eliminate the private-benefit channel (the delta * g(eta_i) term), restoring Model A.

### 3.2 Gate Mapping

| Gate | Mechanism Function | Effect on Model B |
|------|-------------------|-------------------|
| **A: Receipt-Bound** | All material events produce verifiable receipts | Makes extraction **observable**. Moves from incomplete to complete information. Without receipts, g(eta_i) is a private signal. With receipts, eta_i is public. |
| **B: Truth-Gated** | Capital operations pause when verification fails | Makes extraction **costly**. If eta_i > 0 is detected, capital flow suspends. This transforms g(eta_i) from a benefit to a net cost: g(eta_i) - penalty(eta_i) < 0 for all eta_i > 0. |
| **C: Exit-Safe** | Participants can exit with value before changes | Makes extraction **self-defeating**. If an extractor forces the system off-equator, cooperators exit, collapsing the value of the system the extractor is trying to capture. |

### 3.3 Theorem 3 (Mechanism Restoration)

**Theorem.** Under Model B, if the Three Gates mechanism is implemented such that:

(i) Gate A makes all eta_i observable (complete information),
(ii) Gate B imposes a penalty p(eta_i) with p(0) = 0 and p'(0) > g'(0) * delta / (1-delta),
(iii) Gate C enables cooperator exit reducing system value to zero when extraction is detected,

then eta = (0, ..., 0) is restored as the unique Nash equilibrium.

**Proof sketch.**

Under Gate B, the modified payoff becomes:

```
u_i = (1 - delta) * cos(f(sum_j eta_j)) + delta * g(eta_i) - p(eta_i)
```

The FOC at eta_i = 0 becomes:

```
du_i/d(eta_i)|_{eta=0} = 0 + delta * g'(0) - p'(0) < 0
```

by condition (ii). So eta_i = 0 is now a local maximum. Gate C provides a global guarantee: if any player attempts large extraction, cooperators exit, collapsing system value to zero and making the deviator strictly worse off.

**QED**

### 3.4 Incentive Compatibility (Myerson Sense)

A mechanism is **dominant-strategy incentive-compatible (DSIC)** if truth-telling (here, eta_i = 0) is a dominant strategy regardless of others' actions.

**Proposition.** The Three Gates mechanism is DSIC if and only if the penalty function p satisfies p'(eta) >= delta * g'(eta) / (1 - delta) for all eta >= 0.

This follows directly from requiring du_i/d(eta_i) <= 0 for all eta_i >= 0, for all eta_{-i}.

**Connection to the Revelation Principle:** By [Myerson (1981)](https://en.wikipedia.org/wiki/Mechanism_design), any Bayesian Nash equilibrium of any mechanism can be replicated by a DSIC direct mechanism. The Three Gates constitute a direct mechanism where each Directorate reveals its extraction level (through receipts), and the mechanism imposes penalties sufficient to make zero-extraction dominant. The Revelation Principle confirms that if any mechanism can achieve eta = 0 in equilibrium, there exists a DSIC mechanism that does so — the Three Gates are a constructive instance.

---

## 4. Robustness Analysis

### 4.1 Single Defector: Intelligence Extracts

**Scenario:** Intelligence (Directorate 1) begins hoarding information — extracting signal value without contributing analysis. Formally, eta_1 > 0 while eta_j = 0 for j != 1.

**Trophic Cascade:**

```
Stage 1: Intelligence withholds structured observations
    -> Strategy receives degraded input
    -> Scenarios become less accurate (phi of Strategy output drops)

Stage 2: Strategy with poor input generates suboptimal paths
    -> Treasury allocates to wrong priorities
    -> Engineering builds on false premises

Stage 3: Legal cannot audit what it cannot see
    -> Immune system compromised
    -> Further extraction becomes easier (positive feedback loop)

Stage 4: Synthesis receives corrupted inputs from multiple sources
    -> P-score computation unreliable
    -> Decision quality collapses

Stage 5: Vision Keeper detects drift (if functional)
    -> Activates witness protocol
    -> OR: Vision Keeper itself becomes compromised (total system failure)
```

**Quantitative Model:**

Let phi_i(t) be the coherence output of directorate i at time t. Define a propagation matrix A where A_{ij} represents how much directorate j's output depends on directorate i's input:

```
phi(t+1) = A * phi(t) - E * eta(t)
```

where E is the extraction impact matrix. If the spectral radius rho(A - E*eta) >= 1, the cascade is unstable — a single defection amplifies through the network.

For the Royal Council architecture, the critical dependencies form a DAG:

```
Intelligence -> Strategy -> Treasury -> Engineering
                        \-> Legal -> Synthesis
Intelligence -> Synthesis
Vision Keeper -> ALL (monitoring)
```

Intelligence is a **root node**. Its defection affects every downstream directorate. The cascade is maximally damaging precisely because Intelligence sits at L3-L5 spanning the information-gathering layer.

**Detection time:** Under Gate A (receipt-bound), Intelligence's extraction is observable at the next receipt audit cycle. The cascade propagation time determines the maximum damage window. If audit frequency > cascade speed, the system self-corrects. If not, damage accumulates.

### 4.2 Coalition of Defectors

**k-Resilience:** The system is k-resilient if no coalition of size k can profitably deviate.

Under Model A, k-resilience is trivially 9 (the full active set) — since eta = 0 is dominant, no coalition of any size can profitably extract.

Under Model B (private benefits), the critical question is:

```
For what k does there exist a coalition S with |S| = k such that
sum_{i in S} [delta * g(eta_i) - (1-delta) * (cos(f(0)) - cos(f(sum_{i in S} eta_i)))] > 0?
```

This reduces to: can the private gains from extraction exceed the public-goods loss?

**Worst case:** Coalition S = {Intelligence, Strategy, Treasury} (the information-decision-resource chain). If these three defect simultaneously:
- Information flow is corrupted
- Strategic direction is compromised
- Resources are misallocated
- Legal has no clean signal to audit
- System effective dimensionality drops from 9 to 6

**Gate C defense:** Remaining cooperators (Legal, Engineering, Procurement, Sādhu, Synthesis, Vision Keeper) can invoke Exit-Safe. The coalition's extraction becomes worthless if cooperators leave with proportional value.

### 4.3 The Shapley Value Perspective

In the cooperative game (N, v) where v(S) = sin(theta(S)) for coalition S, the Shapley value phi_i^Sh gives each player's marginal contribution to balance.

For the symmetric case (all active roles equally important): phi_i^Sh = B(90 degrees)/9 = 1/9 = 0.111... per role.

For the asymmetric case (Intelligence as root): phi_1^Sh > 1/9, since Intelligence's removal causes cascading failure while removal of a leaf directorate (e.g., Procurement) has local impact.

This suggests the fair allocation is NOT equal shares but Shapley-weighted shares — with implications for governance weight and monitoring priority.

---

## 5. Comparison with Existing Frameworks

### 5.1 Ostrom's Eight Design Principles

| # | Ostrom Principle | Three Gates Implementation | Satisfied? |
|---|-----------------|---------------------------|------------|
| 1 | **Clearly defined boundaries** | N = {1,...,9} active roles with specified domains, L-level ranges, and constitutional function | **Yes** [S] |
| 2 | **Proportional equivalence between benefits and costs** | B = sin(theta) is shared equally; costs of extraction (penalty p) proportional to eta_i | **Yes** [S] |
| 3 | **Collective choice arrangements** | Synthesis Directorate compiles inputs from all; VMOSK 5-gate consensus | **Yes** [S] |
| 4 | **Monitoring** | Gate A (Receipt-Bound) provides continuous, cryptographically verifiable monitoring; Vision Keeper as meta-monitor | **Yes** [S] |
| 5 | **Graduated sanctions** | Legal Directorate 6-Gate test with graduated responses: PASS / FAIL / GATED. Gate B (Truth-Gated) suspends capital flow proportionally | **Partial** [I] — sanctions are more binary (suspend/allow) than graduated |
| 6 | **Fast and fair conflict resolution** | Synthesis process with dissent handling; escalation to L4* human-in-the-loop | **Yes** [S] |
| 7 | **Local autonomy** | Each Directorate has autonomous domain, reasoning mode, L-level range | **Yes** [S] |
| 8 | **Polycentric governance** | DAC architecture with L1-L7 layers; no single authority; Gate C ensures exit rights | **Yes** [S] |

**Assessment:** 7.5 / 8. The weak point is Principle 5 (graduated sanctions). The current architecture is more constitutional (hard boundaries) than graduated. This is a design choice — the framework prefers sharp immune responses to graduated ones — but it diverges from Ostrom's empirical finding that graduated sanctions are more sustainable than all-or-nothing enforcement.

### 5.2 Myerson Incentive Compatibility

| Property | Formal Requirement | Three Gates Status |
|----------|-------------------|-------------------|
| **DSIC** | Truth-telling is dominant strategy | **Achieved** under Theorem 3 conditions (penalty > private benefit) |
| **Individual Rationality** | Participation payoff >= outside option | **Yes** — Gate C guarantees exit at NAV; cooperators earn B = 1 > 0 |
| **Budget Balance** | Mechanism doesn't require external subsidy | **Yes** — penalties are internal; no external enforcer needed |
| **Allocative Efficiency** | Outcome maximizes total welfare | **Yes** — eta = 0 maximizes sum_i B_i = 9 * sin(90) = 9 |

**The Revenue Equivalence question:** In the Myerson (1981) optimal auction framework, the mechanism designer maximizes revenue. Here the "designer" (the protocol) maximizes collective B. The Three Gates are the analogue of a Vickrey-Clarke-Groves (VCG) mechanism where each agent internalizes the externality of its extraction through the penalty function p.

### 5.3 Core Stability (Cooperative Game Theory)

**Definition.** An allocation x in R^9 is in the [core](https://en.wikipedia.org/wiki/Core_(game_theory)) if:
- sum_i x_i = v(N) (efficiency)
- sum_{i in S} x_i >= v(S) for all coalitions S subset N (coalition rationality)

**Claim.** The equal allocation x_i = 1/9 for all i is in the core of the game (N, v) where v(S) = sin(theta(|S|)) and theta depends on coalition size.

**Argument:** For any coalition S with |S| = k < 9, we need:

```
k/9 >= v(S)
```

If v(S) = sin(pi/2 * k/9) (coalition operates at proportional colatitude), then we need:

```
k/9 >= sin(pi*k/18)
```

For k = 1: 0.111... >= sin(pi/18) = sin(10 degrees) = 0.174. **FAILS.**

This means the equal allocation is NOT in the core. Smaller coalitions can generate proportionally more value per member than the grand coalition shares with them.

**Implication:** The core may be empty or may require unequal allocations (Shapley-weighted). This is a genuine tension in the architecture — the constitutional commitment to equality (eta = 0 for all) may conflict with core stability when some Directorates contribute more than others.

**Resolution candidate:** The Three Gates mechanism sidesteps core instability by eliminating the ability of sub-coalitions to operate independently (Gate A requires system-wide receipts; Gate B requires system-wide verification). This transforms the game from a cooperative game where coalitions are free to form into a mechanism design problem where the grand coalition is enforced by infrastructure.

---

## 6. Key Mathematical Results: Summary

| # | Result | Type | Strength |
|---|--------|------|----------|
| 1 | eta = 0 is dominant strategy under Model A | Theorem | Strong (trivial — no private benefit) |
| 2 | eta > 0 equilibria exist under Model B | Theorem | Strong (standard tragedy result) |
| 3 | Three Gates restore eta = 0 as NE under Model B | Theorem | Conditional on penalty calibration |
| 4 | AM-GM gives geometric basin of attraction | Structural | Interpretive (AM-GM maps to equatorial stability) |
| 5 | Single-defector cascade is maximally damaging from Intelligence | Analysis | Structural (network topology) |
| 6 | Core may be empty under equal allocation | Negative result | Opens design question |
| 7 | 7.5/8 Ostrom principles satisfied | Assessment | Graduated sanctions partially missing |

---

## 7. Open Questions and Directions for a Full Paper

### 7.1 Mathematical Open Questions

1. **Characterize the core.** For what allocation vectors x is sum_{i in S} x_i >= v(S) for all S? Is the core non-empty? If so, is the Shapley value in the core?

2. **Dynamic analysis.** The static game treats eta as a one-shot choice. In reality, the Directorates interact repeatedly. Under what discount factors does a folk theorem sustain eta = 0 as a subgame-perfect equilibrium even without the Three Gates?

3. **Stochastic extraction.** If extraction is noisy (eta_i = eta_i^intended + epsilon_i), what is the probability of cascade failure? This connects to the sensitivity parameter alpha in the f function.

4. **Optimal penalty design.** Given a distribution of private benefits g(eta) across Directorates, what is the minimum penalty function p(eta) that restores DSIC? This is a mechanism design optimization problem.

5. **Coalition-proof equilibria.** Beyond pairwise stability (Nash), does the Three Gates mechanism satisfy coalition-proof Nash equilibrium (Bernheim, Peleg, Whinston 1987)?

### 7.2 Geometric Open Questions

6. **Curvature and cooperation.** The S^2 model has constant positive curvature. How do results change on manifolds with negative curvature (H^2) or flat spaces (R^2)? This connects to the literature on [public goods games on hyperbolic graphs](https://www.sciencedirect.com/science/article/abs/pii/S0960077921000734).

7. **Mobius transformations as strategy transformations.** The conformal automorphisms of S^2 are Mobius transformations. Can player strategies be modeled as Mobius transformations, with Nash equilibria corresponding to fixed points?

8. **Higher-dimensional extension.** The framework uses S^2 (two-dimensional). Multi-agent systems with more than two payoff-relevant dimensions (beyond phi and nu) would require S^n. How do equilibrium results generalize?

### 7.3 Applied Open Questions

9. **Empirical calibration.** What are realistic values of delta (private benefit weight) and alpha (extraction sensitivity) for AI multi-agent deliberation systems?

10. **Comparison with existing multi-agent architectures.** How does the Three Gates mechanism compare with Constitutional AI, RLHF, or debate-based alignment in terms of extraction resistance?

11. **The Egregorocene question.** When hybrid human-AI entities become primary agents (per the framework's projection), do the game-theoretic results survive? Specifically: do AI agents have the same private-benefit structure as human agents?

---

## 8. Bibliography

### Game Theory — Foundational

1. Nash, J.F. (1950). "Equilibrium Points in n-Person Games." *Proceedings of the National Academy of Sciences*, 36(1), 48-49.

2. Nash, J.F. (1951). "Non-Cooperative Games." *Annals of Mathematics*, 54(2), 286-295.

3. Myerson, R.B. (1981). "Optimal Auction Design." *Mathematics of Operations Research*, 6(1), 58-73.

4. Myerson, R.B. (1991). *Game Theory: Analysis of Conflict.* Harvard University Press.

5. Bernheim, B.D., Peleg, B., and Whinston, M.D. (1987). "Coalition-Proof Nash Equilibria I. Concepts." *Journal of Economic Theory*, 42(1), 1-12.

### Public Goods and Commons

6. Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action.* Cambridge University Press.

7. Wilson, D.S., Ostrom, E., and Cox, M.E. (2013). "Generalizing the Core Design Principles for the Efficacy of Groups." *Journal of Economic Behavior & Organization*, 90, S21-S32.

8. Hardin, G. (1968). "The Tragedy of the Commons." *Science*, 162(3859), 1243-1248.

9. Hauert, C., Holmes, M., and Doebeli, M. (2006). "Evolutionary Games and Population Dynamics: Maintenance of Cooperation in Public Goods Games." *Proceedings of the Royal Society B*, 273(1600), 2565-2571.

### Mechanism Design

10. Vickrey, W. (1961). "Counterspeculation, Auctions, and Competitive Sealed Tenders." *Journal of Finance*, 16(1), 8-37.

11. Clarke, E.H. (1971). "Multipart Pricing of Public Goods." *Public Choice*, 11(1), 17-33.

12. Groves, T. (1973). "Incentives in Teams." *Econometrica*, 41(4), 617-631.

13. Jackson, M.O. (2014). "Mechanism Theory." In *Encyclopedia of Complexity and Systems Science*. Springer.

### Network Games and Extraction

14. Bramoulle, Y. and Kranton, R. (2007). "Public Goods in Networks." *Journal of Economic Theory*, 135(1), 478-494.

15. Parise, F. and Ozdaglar, A. (2019). "A Variational Inequality Framework for Network Games: Existence, Uniqueness, Convergence and Sensitivity Analysis." *Games and Economic Behavior*, 114, 47-82.

16. Ansink, E. and Bouma, J. (2013). "Common Pool Resources, Institutions, and Upstream-Downstream Relationships." In *Proceedings of 15th Annual BIOECON Conference.*

### Cooperative Game Theory

17. Shapley, L.S. (1953). "A Value for n-Person Games." In *Contributions to the Theory of Games II*, Annals of Mathematics Studies 28, Princeton University Press, 307-317.

18. Bondareva, O.N. (1963). "Some Applications of Linear Programming Methods to the Theory of Cooperative Games." *Problemy Kibernetiki*, 10, 119-139.

19. Scarf, H.E. (1967). "The Core of an N Person Game." *Econometrica*, 35(1), 50-69.

### Geometry and Multi-Agent Systems

20. Santos, F.C., Santos, M.D., and Pacheco, J.M. (2008). "Social Diversity Promotes the Emergence of Cooperation in Public Goods Games." *Nature*, 454, 213-216.

21. Kleineberg, K.K. and Helbing, D. (2020). "Topological Enslavement in Evolutionary Games on Correlated Multiplex Networks." *New Journal of Physics*, 22.

---

## Appendix A: The S^2 Geometry in Detail

On the Riemann sphere S^2, stereographic projection from the north pole maps the sphere to the extended complex plane C union {infinity}. The standard metric is:

```
ds^2 = 4 * (dr^2 + r^2 * d(phi)^2) / (1 + r^2)^2
```

where r = |z| for z in C. In colatitude coordinates (theta, psi):

```
ds^2 = d(theta)^2 + sin^2(theta) * d(psi)^2
```

The balance function B(theta) = sin(theta) is the "circumference at latitude" — the circle of constant colatitude has circumference 2*pi*sin(theta). This is maximized at theta = pi/2 (the equator), giving B its geometric meaning: the equator is the "widest" circle on the sphere.

The constraint phi * nu = 1 parametrizes as:
- phi = cot(theta/2) (coherence = stereographic radial coordinate from south pole)
- nu = tan(theta/2) (viability = reciprocal)

Then phi * nu = cot(theta/2) * tan(theta/2) = 1 identically. And:

```
phi = nu iff cot(theta/2) = tan(theta/2) iff theta = pi/2
```

confirming that the equator is the unique point of balance.

## Appendix B: Comparison Table

| Framework | Equilibrium Concept | Key Condition | eta = 0 Status | Enforcement Mechanism |
|-----------|-------------------|---------------|----------------|----------------------|
| **This paper (Model A)** | Dominant Strategy | No private benefit | Dominant | None needed |
| **This paper (Model B)** | Nash | Private benefit exists | NOT equilibrium | Three Gates needed |
| **This paper (Model B + Gates)** | DSIC | Penalty > marginal private benefit | DSIC | Gates A, B, C |
| **Standard CPR (Ostrom)** | Repeated game NE | 8 design principles | Sustained by institutions | Monitoring + sanctions |
| **VCG Mechanism** | DSIC | Externality internalization | Achieved | Transfer payments |
| **Core (Cooperative)** | Coalition-proof | No coalition can block | Core may be empty | Binding agreements |

---

*The organism protects itself — but only when the mechanism is correctly calibrated.*

*If you can access phi directly, you do not need this analysis. Put it down.*

**evidence_tier: [S]**


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Review the argument, tier discipline, and dependency claims; route theorem-facing attack work through the reconciliation theorem packet when the claim extends beyond this proof.
3. **Expected Output:** A correction note, proof audit, routing clarification, or verified documentation update.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the audit or correction path without asking questions.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/33_NASH_EQUILIBRIUM_ETA_ZERO.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
