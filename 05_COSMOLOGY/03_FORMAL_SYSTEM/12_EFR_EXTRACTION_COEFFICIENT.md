---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "THE EXTRACTION COEFFICIENT (η_ratio)"
---

> 🟡 **CORRECTED (v3.1) — 2026-07-23**
> **Evidence Tier:** [S] for the stated classical Lotka–Volterra equilibrium and closed-orbit result; [C] for the selected bounded/ground-negating distinction and Good/Bad/Evil mapping
> **History:** v1.0 FAILED peer review (predator's `η_ratio` w.r.t. prey is ∞ not <1; logical error in proof). v2.0 removed the circular predator proof. v3.0 added a population-dynamics contrast but incorrectly described the classical coexistence equilibrium as attracting. v3.1 restores the correct center/closed-orbit result and confines the broader categorical claim to `[C]`.
> **Status:** Model contrast repaired. The classical equilibrium is a center, not an attractor. Generalisation to real ecosystems, cancer, or moral categories still requires independent evidence.
> **See:** `../../08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/00_INTERNAL_REVIEW_FINDINGS.md` for original findings.

---


> **Register bridge (2026-07-22, per `46_THE_ETA_CONVERSION_MAP.md`).** The `η_ratio`
> defined in this paper is the **ratio register** (`η_ratio`): break-even is
> **1**, not 0. It is *not* the action fence `η_move = 0` (the R1
> non-extraction rule), whose zero names non-extraction, and not a study's `η_domain`. The
> three registers convert only as licensed in the map — in particular the two
> zeros do not translate ("do not compare the two thresholds as if they were
> the same number," `40_THE_LOGARITHMIC_REALIGNMENT.md` §3). This banner closes
> the register gap recorded by Receipt 158: this file previously presented the ratio as *the*
> definition with no register marker.

# THE EXTRACTION COEFFICIENT (`η_ratio`)

## Formal Definition of Good, Bad, and Evil (v3.1)

**Status:** Corrected after peer review; model contrast stated without an attractor claim
**Date:** 2026-07-23
**Evidence Tier:** [S] for the declared classical Lotka–Volterra result; [C] for generalised ecology and moral-ontological mapping
**Purpose:** Provide the moral-ontological foundation for the Magnum Opus
**Version:** v3.1 — classical center/closed-orbit correction; categorical extension retiered

> **v2.0 correction:** The original predator/cancer proof contained a logical error: it claimed the predator has `η_ratio < 1` because it "would starve without prey," but the ratio is extraction/contribution, and a predator contributes nothing to its prey's substrate. The predator's prey-relative `η_ratio` is formally ∞, not <1. Predator–prey cycling is maintained by the declared population dynamics, not by the predator's individual ratio being bounded. The Good/Bad/Evil categories remain normative mappings, not structural derivations.

---

## The Problem

The framework has three axes: D (dimensions), L (levels), E (scales). But it lacks a fourth axis: the moral-ontological distinction that determines whether an operation is regenerative, cyclical, or terminal.

Without this axis, the reader has no vocabulary for distinguishing natural destruction from ground negation. The "continuum error" — treating Good and Evil as degrees of the same thing — is the most common misunderstanding of the framework.

---

## The M-Axis: Moral Core State

### Definition: `η_ratio` (Extraction Coefficient)

Let `η_ratio` represent the ratio of what a system takes from its substrate to what it contributes:

```
η_ratio = (extraction) / (contribution)
```

- **`η_ratio < 1`:** The system contributes more than it takes (symbiotic)
- **`η_ratio = 1`:** The system takes and gives equally (trophic balance)
- **`η_ratio > 1`:** The system takes more than it gives (parasitic)
- **`η_ratio → ∞`:** The chosen denominator approaches zero while extraction persists (candidate ground-negation signal)

### The Three Levels

| Level | Name | `η_ratio` | Operation | Ground Status |
|-------|------|---|-----------|---------------|
| **Good** | Ektropy | `η_ratio < 1` | Cooperative, positive-sum integration | Φ present, expanding |
| **Bad** | Clearing | `η_ratio ≈ 1` | Natural destruction within cycle | Φ intact, cycle turns |
| **Evil** | Ground Negation | `η_ratio → ∞` | Elimination of declared regeneration | Φ declared absent |

### The Critical Distinction

**Bad and Evil are categorically different, not degrees of the same thing.**

- A modeled predator–prey system may cycle while preserving positive populations
  under its declared equations. This does not prove every real trophic system
  persists.
- A stipulated depletion model can cross an irreversible regenerative floor.
  Calling a real cancer or institution ground-negating requires separate
  evidence, boundary, and horizon.

**The distinction:** `[C]` A predator's individual `η_ratio` with respect to
one prey can be infinite, while a declared system-level ratio can remain finite
and periodic. Classical Lotka–Volterra does not enforce convergence; it supplies
a center with closed orbits under its idealized assumptions.

A separately stipulated uncoupled depletion model can make `η_ratio`
diverge. Actual cancer biology is not established by that contrast.

**The selected categorical proposal `[C]`:** preserve regenerative capacity
over the declared horizon versus erase it. A divergent `η_ratio` can diagnose
the latter in some models, but the moral category is not derived from the
number alone.

---

## Two scopes of `η_ratio`

`η_ratio` operates at two distinct scales:

| Scope | What It Captures | Interpretation |
|-------|-----------------|----------------|
| **Single system** | Extraction ratio (what system takes vs gives) | Instantaneous measure — can fluctuate |
| **Network / structural** | Extraction coefficient (standing wave vs substrate) | Persistent diagnostic — defines the system's category |

**The instantaneous ratio is a measure. The structural ratio is a diagnostic.**

A system can have `η_ratio > 1` temporarily without being architecturally
parasitic. A persistent ratio above one is evidence only relative to the
declared baseline, horizon, and regenerative model.

**The test:** name the domain and regenerative floor; do not infer moral status
from one instantaneous ratio.

---

## The population-dynamics contrast (v3.1)

The v2.0 correction identified the problem: a predator's individual ratio with
respect to prey can be infinite while the system-level model remains bounded.
This section states the classical result and one contrast model; it does not
formalize a universal moral break.

### 1. Lotka-Volterra: The Predator Case

[S] The classical Lotka-Volterra predator-prey equations:

```
dx/dt = αx - βxy      (prey: grows at rate α, consumed at rate β per predator encounter)
dy/dt = δxy - γy       (predator: grows at rate δ per prey consumed, dies at rate γ)
```

where x = prey population, y = predator population, and α, β, δ, γ > 0.

**System-level extraction rate.** Define:

```
η_sys = (prey consumed per unit time) / (prey regenerated per unit time)
       = βxy / αx
       = βy / α
```

At equilibrium (dx/dt = 0, dy/dt = 0):

```
x* = γ/δ,   y* = α/β
```

Substituting y* into η_sys:

```
η_sys* = β(α/β) / α = 1
```

**Result:** [S] At the Lotka-Volterra coexistence equilibrium, `η_sys = 1`
exactly. The classical coexistence equilibrium is a center. Outside that
equilibrium, positive trajectories form closed periodic orbits around it. It does **not**
converge to the equilibrium or supply a basin of attraction.

**The cycling mechanism:** If predators over-extract (`η_sys > 1`), prey
declines; after a phase lag, predators decline and `η_sys` falls. If predators
under-extract, prey can grow; after a phase lag, predators grow and `η_sys`
rises. In the classical equations this produces neutral oscillation around the
coexistence equilibrium, not damping toward it. Density dependence, functional
responses, spatial structure, stochasticity, or other mechanisms are needed
for claims about attraction in real ecosystems.

**Key insight:** The individual predator's `η_ratio` with respect to a single
prey can be infinite (total extraction, zero contribution), while the modeled
system ratio remains finite and cycles around `1` on a closed classical orbit.
The equilibrium value is `1`; the orbit is not identically `1`. The broader
claim that real trophic systems are bounded requires a separately stated model
and evidence.

### 2. A stipulated uncoupled contrast

`[A]` Consider the following deliberately simplified exponential-growth model.
It is a mathematical contrast, not a sufficient model of cancer biology:

```
dC/dt = rC      (exponential growth, rate r > 0)
```

This is not a Lotka–Volterra system. In the stipulated equations, growth rate
`r` is not coupled to host health. No claim follows that actual cancers lack
feedback, resource limits, immune interaction, spatial structure, or treatment
response.

**System-level extraction rate:**

```
η_sys = (host resources consumed by cancer) / (host regenerative capacity)
```

As cancer grows exponentially and host capacity H declines:

```
dH/dt = -rC + σ      (host loses resources to cancer, regenerates at rate σ)
```

Once `rC > σ` in this model, `H` declines monotonically. As `H → 0`, the
chosen ratio diverges. The result belongs to the stipulated equations only.

### 3. The Formal Criterion

**Definition (Trophically Bounded).** A system `S` operating on substrate `G`
is *trophically bounded over a declared horizon* if its system-level extraction
rate `η_sys` remains inside a finite invariant or absorbing set under the
declared dynamics. Convergence to a finite equilibrium is one possible case;
bounded periodic orbit is another.

**Definition (Ground-Negating).** A system `S` operating on substrate `G` is
*ground-negating over a declared horizon* if the chosen system ratio diverges
or regenerative capacity crosses a declared irreversible floor under the
stated dynamics. This is a framework definition `[I/C]`, not a theorem that
every uncoupled system behaves this way.

**Theorem (sketch).**

> In the classical two-species Lotka-Volterra predator-prey model with positive
> initial populations, `η_sys` remains finite and oscillates on a closed orbit
> around the coexistence value `1`; it does not converge to that value.
>
> A specifically declared uncoupled exponential model can make `η_sys`
> diverge while regenerative capacity is treated as bounded. This is a
> model-specific contrast, not a theorem about every system lacking one named
> feedback term.
>
> The proposed categorical break between trophically bounded and
> ground-negating systems is `[C]` when extended beyond those declared models.

**Proof sketch.** For classical Lotka-Volterra, the coexistence equilibrium is a
center and positive non-equilibrium trajectories follow conserved closed level
sets; `η_sys = βy/α` therefore oscillates rather than converges. For the
stipulated exponential contrast, `C(t)=C₀e^(rt)` and a separately bounded
regeneration denominator makes the chosen ratio diverge. This establishes the
contrast between these two models only. It does not prove that every ecological
predator-prey system is bounded or that every cancer follows uncoupled
exponential growth.

### 4. The Mapping to Good / Bad / Evil

[C] Conjecture — the mapping from dynamical-systems categories to moral-ontological categories:

| Dynamical Category | η_sys Behavior | Moral Category | Example |
|--------------------|---------------|----------------|---------|
| Regenerative coupling | `η_sys < 1` over the declared horizon | **Good** `[C]` | candidate mutualistic cases |
| Trophic coupling | equilibrium `η_sys = 1`; bounded motion may cycle | **Bad** `[C]` | classical predator–prey model as formal analogy |
| Ground-negating dynamics | ratio diverges or regenerative floor is crossed | **Evil** `[C]` | stipulated depletion models; institutional analogies require evidence |

**Selected categorical proposal `[C]`.** The proposed break is between dynamics
that preserve regenerative capacity over the declared horizon and dynamics
that erase it. A finite equilibrium is not required: a bounded cycle may also
preserve the modeled ground. Coupling alone is insufficient, and the proposal
is not established as a universal topological law.

### 5. Evidence Tier and Kill Criterion

**Evidence tiers:**
- [S] Structural: In the declared classical Lotka–Volterra model the coexistence
  equilibrium has `η_sys = 1` and positive non-equilibrium trajectories are
  closed periodic orbits around a center. Divergence follows analytically for
  the separately stipulated exponential contrast.
- [C] Conjecture: The mapping of these dynamical categories onto Good/Bad/Evil is a normative interpretation, not a mathematical derivation. The claim that moral categories track coupling topology is a philosophical thesis.

**Kill criterion:** If a system with η_sys → ∞ (ground-negating dynamics) can achieve stable coexistence with its substrate WITHOUT structural modification to introduce negative feedback coupling, the categorical break fails and the three-level model collapses to a continuum.

---

## The Connection to the Framework

The M-Axis connects to every other axis:

| Axis | Relationship to `η_ratio` |
|------|-------------------|
| D (Dimensions) | Evil operates at D4 (physical extraction) and D5 (informational extraction) |
| L (Levels) | Evil is L1-L2 operating at scale (survival-level extraction applied systemically) |
| E (Scales) | Evil is E5-E6 (civilizational extraction through institutional capture) |
| P_node (finite-node ektropy) | Evil reduces usable `P_node` by destroying Φ while inflating or maintaining V; `P∞ = φ·ν = 1` remains the background manifold invariant, so the collapse is a finite-node/contact-register loss rather than a change to the sphere identity. |

---

## What Would Falsify This

1. **No categorical break found:** If `η_ratio → ∞` is reached without the proposed regenerative discontinuity, the three-level model is wrong
2. **Evil operates regeneratively:** If ground negation somehow preserves the substrate, the model is wrong
3. **Good and Evil are interchangeable:** If systems can switch between `η_ratio < 1` and `η_ratio → ∞` without structural change, the model is wrong

---

## Summary

```
η_ratio < 1: candidate regenerative relation
η_ratio ≈ 1: declared trophic balance
η_ratio → ∞: candidate ground-negation signal

The selected categorical proposal concerns regenerative capacity, not a bare
number. Its moral mapping remains [C].
```

*Extraction Coefficient | 2026-03-22 | Good, Bad, and Evil are categorically different.*


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Verify the mathematical claims. Check evidence tiers. Flag any [I] or [C] presented as [S] or [S].
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/12_EFR_EXTRACTION_COEFFICIENT.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*

---

> **Status:** CORRECTED (v3.1) — the classical coexistence equilibrium is a
> center with closed periodic orbits, not an attractor. Tier: [S] for that
> declared model result; [C] for ecological generalisation and moral mapping.
> See `../../08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/00_INTERNAL_REVIEW_FINDINGS.md`.
