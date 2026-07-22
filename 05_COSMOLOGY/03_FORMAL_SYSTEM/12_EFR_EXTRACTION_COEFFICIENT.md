---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "THE EXTRACTION COEFFICIENT (η)"
---

> 🟡 **CORRECTED (v3.0) — 2026-04-05**
> **Evidence Tier:** [S] Structural for Lotka-Volterra formalization; [C] Conjecture for Good/Bad/Evil mapping
> **History:** v1.0 FAILED peer review (predator's η w.r.t. prey is ∞ not <1; logical error in proof). v2.0 removed circular predator proof, replaced with substrate-maintenance criterion, added "Two Scopes of η" section. v3.0 adds Population-Dynamics Proof formalizing the categorical break via Lotka-Volterra vs. uncoupled exponential dynamics.
> **Status:** Categorical break now formalized. [S] tier for dynamical-systems claim. [C] tier for moral-ontological mapping. Awaiting independent verification by ecological modeler.
> **See:** `../../08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/00_INTERNAL_REVIEW_FINDINGS.md` for original findings.

---


> **Register bridge (2026-07-22, per `46_THE_ETA_CONVERSION_MAP.md`).** The η
> defined in this paper is the **ratio register** (`η_ratio`): break-even is
> **1**, not 0. It is *not* the action fence `η_move = 0` (the R1
> non-extraction rule), whose zero names non-extraction, and not a study's `η_domain`. The
> three registers convert only as licensed in the map — in particular the two
> zeros do not translate ("do not compare the two thresholds as if they were
> the same number," `40_THE_LOGARITHMIC_REALIGNMENT.md` §3). This banner closes
> the register gap recorded by Receipt 158: this file previously presented the ratio as *the*
> definition with no register marker.

# THE EXTRACTION COEFFICIENT (η)

## Formal Definition of Good, Bad, and Evil (v3.0)

**Status:** Corrected after peer review; categorical break now formalized
**Date:** 2026-04-05
**Evidence Tier:** [S] Structural (Lotka-Volterra dynamics); [C] Conjecture (moral-ontological mapping)
**Purpose:** Provide the moral-ontological foundation for the Magnum Opus
**Version:** v3.0 — population-dynamics proof added; categorical break formalized via coupled vs. uncoupled dynamics

> **v2.0 correction:** The original predator/cancer proof contained a logical error: it claimed the predator has η < 1 because it "would starve without prey," but η is defined as extraction/contribution, and a predator contributes nothing to its prey's substrate. The predator's η w.r.t. prey is formally ∞, not <1. The predator-prey cycle is maintained by population dynamics and co-evolution, not by the predator's η being bounded. The categorical break between Bad and Evil is now justified by the substrate-maintenance criterion (whether the system's operation preserves the regenerative capacity of its environment) rather than by the predator's individual η. Tier corrected from [S] to [C] — Good/Bad/Evil are normative categories mapped onto structural features, not structural derivations.

---

## The Problem

The framework has three axes: D (dimensions), L (levels), E (scales). But it lacks a fourth axis: the moral-ontological distinction that determines whether an operation is regenerative, cyclical, or terminal.

Without this axis, the reader has no vocabulary for distinguishing natural destruction from ground negation. The "continuum error" — treating Good and Evil as degrees of the same thing — is the most common misunderstanding of the framework.

---

## The M-Axis: Moral Core State

### Definition: η (Extraction Coefficient)

Let η represent the ratio of what a system takes from its substrate to what it contributes:

```
η = (extraction) / (contribution)
```

- **η < 1:** The system contributes more than it takes (symbiotic)
- **η = 1:** The system takes and gives equally (trophic balance)
- **η > 1:** The system takes more than it gives (parasitic)
- **η → ∞:** The system eliminates the substrate's capacity to generate (ground negation)

### The Three Levels

| Level | Name | η | Operation | Ground Status |
|-------|------|---|-----------|---------------|
| **Good** | Ektropy | η < 1 | Cooperative, positive-sum integration | Φ present, expanding |
| **Bad** | Clearing | η ≈ 1 | Natural destruction within cycle | Φ intact, cycle turns |
| **Evil** | Ground Negation | η → ∞ | Engineered elimination of regeneration | Φ declared absent |

### The Critical Distinction

**Bad and Evil are categorically different, not degrees of the same thing.**

- The predator (Bad) kills the prey but does not eliminate the capacity for future prey. The cycle continues. The ground holds.
- The cancer (Evil) eliminates the host's capacity to regenerate. The cycle stops. The ground is salted.

**The distinction:** [C] A predator's extraction is bounded by population dynamics — co-evolution enforces equilibrium because prey collapse eliminates the predator's substrate. The predator's η is not literally < 1 (a predator extracts everything from each individual prey), but the *system-level* extraction rate is bounded by the prey's regeneration rate.

A cancer extracts without regenerative constraint — η → ∞ at the system level until the host is gone. The cancer eliminates the substrate it depends on.

**The categorical break:** η → ∞ is not "η = 1 taken to extremes." It is a qualitative discontinuity. Below η → ∞, the system maintains the substrate. At η → ∞, the system eliminates the substrate. These are different operations, not different degrees.

---

## Two Scopes of η

η operates at two distinct scales:

| Scope | What It Captures | Interpretation |
|-------|-----------------|----------------|
| **Single system** | Extraction ratio (what system takes vs gives) | Instantaneous measure — can fluctuate |
| **Network / structural** | Extraction coefficient (standing wave vs substrate) | Persistent diagnostic — defines the system's category |

**The instantaneous η is a measure. The structural η is a diagnostic.**

A system can have η > 1 temporarily (bad quarter, crisis response) without being parasitic. Structural η > 1 means the system is architecturally parasitic — it will continue extracting regardless of circumstances.

**The test:** η > 1 temporarily is Bad. Structural η → ∞ permanently is Evil.

---

## The Population-Dynamics Proof (v3.0)

The v2.0 correction identified the problem: a predator's individual η w.r.t. prey is ∞, yet predators are Bad (cyclical), not Evil (ground-negating). The substrate-maintenance criterion was asserted but not formalized. This section provides the formalization.

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

**Result:** [S] At the Lotka-Volterra equilibrium, η_sys = 1 exactly. The system self-regulates to trophic balance.

**The negative feedback mechanism:** If predators over-extract (η_sys > 1), prey declines, which starves predators, which reduces y, which reduces η_sys back toward 1. If predators under-extract (η_sys < 1), prey grows, predators thrive, y increases, η_sys rises back toward 1. The coupling between predator and prey populations creates a basin of attraction around η_sys = 1.

**Key insight:** The individual predator's η w.r.t. a single prey is ∞ (total extraction, zero contribution). But the SYSTEM-level η_sys is bounded at 1 because the predator population is dynamically coupled to the prey population. The predator cannot escape this coupling — over-extraction destroys the predator, not just the prey.

### 2. Cancer: The Uncoupled Case

[S] Cancer cell growth within a host:

```
dC/dt = rC      (exponential growth, rate r > 0)
```

This is NOT a Lotka-Volterra system. The critical structural difference: cancer growth rate r is not coupled to host health. There is no term of the form (-γC) that increases as the host weakens. The cancer does not "starve" as the host declines — it continues growing until physical resource exhaustion.

**System-level extraction rate:**

```
η_sys = (host resources consumed by cancer) / (host regenerative capacity)
```

As cancer grows exponentially and host capacity H declines:

```
dH/dt = -rC + σ      (host loses resources to cancer, regenerates at rate σ)
```

Once rC > σ (cancer consumption exceeds host regeneration), H declines monotonically. As H → 0, η_sys → ∞. There is no negative feedback loop: the cancer does not reduce its growth rate as the host weakens. The system has no finite attractor.

### 3. The Formal Criterion

**Definition (Trophically Bounded).** A system S operating on substrate G is *trophically bounded* if its system-level extraction rate η_sys possesses a finite attractor under the system's own dynamics — i.e., the dynamics of S include a negative feedback coupling between S's extraction rate and G's capacity, such that η_sys converges to a finite equilibrium.

**Definition (Ground-Negating).** A system S operating on substrate G is *ground-negating* if η_sys has no finite attractor under the system's own dynamics — i.e., S's extraction rate is not coupled to G's declining capacity, and η_sys diverges as G is depleted.

**Theorem (sketch).**

> In any coupled predator-prey system with Lotka-Volterra dynamics (or any system with analogous negative feedback between extraction and substrate), η_sys converges to a finite equilibrium.
>
> In any uncoupled exponential growth system (or any system lacking negative feedback between extraction and substrate), η_sys diverges.
>
> The categorical break between trophically bounded and ground-negating systems is a structural property of the coupling topology, not a matter of degree.

**Proof sketch.** For Lotka-Volterra: the equilibrium (x*, y*) is a center in the phase plane; trajectories orbit it. η_sys = βy/α oscillates around 1. The system cannot reach η_sys → ∞ without y → ∞, which requires x → ∞ (since dy/dt > 0 only when δx > γ), creating an unbounded positive feedback loop that contradicts the bounded orbits of the Lotka-Volterra system. For uncoupled exponential growth: dC/dt = rC has solution C(t) = C₀e^(rt). Since H is bounded and C grows without bound, η_sys = rC/σ → ∞ as t → ∞. No structural mechanism arrests this divergence. QED (sketch).

### 4. The Mapping to Good / Bad / Evil

[C] Conjecture — the mapping from dynamical-systems categories to moral-ontological categories:

| Dynamical Category | η_sys Behavior | Moral Category | Example |
|--------------------|---------------|----------------|---------|
| Mutualistic coupling | η_sys < 1 (finite attractor below 1) | **Good** | Mycorrhizal networks, open-source ecosystems |
| Predatory coupling | η_sys ≈ 1 (finite attractor at 1) | **Bad** | Predator-prey cycles, creative destruction, market competition |
| Uncoupled extraction | η_sys → ∞ (no finite attractor) | **Evil** | Cancer, Ponzi schemes, totalitarian resource extraction |

**The categorical break is between coupled and uncoupled dynamics.** A system with any finite attractor for η_sys — whether at 0.5 or at 1 or at 1.5 — is categorically different from a system with no finite attractor. The former preserves the substrate (even if roughly). The latter eliminates it. This is a topological property of the phase space, not a quantitative threshold.

### 5. Evidence Tier and Kill Criterion

**Evidence tiers:**
- [S] Structural: The Lotka-Volterra equilibrium result and the divergence of uncoupled exponential growth are established mathematical ecology. The definitions of trophically bounded and ground-negating are structural.
- [C] Conjecture: The mapping of these dynamical categories onto Good/Bad/Evil is a normative interpretation, not a mathematical derivation. The claim that moral categories track coupling topology is a philosophical thesis.

**Kill criterion:** If a system with η_sys → ∞ (ground-negating dynamics) can achieve stable coexistence with its substrate WITHOUT structural modification to introduce negative feedback coupling, the categorical break fails and the three-level model collapses to a continuum.

---

## The Connection to the Framework

The M-Axis connects to every other axis:

| Axis | Relationship to η |
|------|-------------------|
| D (Dimensions) | Evil operates at D4 (physical extraction) and D5 (informational extraction) |
| L (Levels) | Evil is L1-L2 operating at scale (survival-level extraction applied systemically) |
| E (Scales) | Evil is E5-E6 (civilizational extraction through institutional capture) |
| P_node (finite-node ektropy) | Evil reduces usable `P_node` by destroying Φ while inflating or maintaining V; `P∞ = φ·ν = 1` remains the background manifold invariant, so the collapse is a finite-node/contact-register loss rather than a change to the sphere identity. |

---

## What Would Falsify This

1. **No categorical break found:** If η → ∞ is reachable through gradual increase of η > 1, the three-level model is wrong
2. **Evil operates regeneratively:** If ground negation somehow preserves the substrate, the model is wrong
3. **Good and Evil are interchangeable:** If systems can switch between η < 1 and η → ∞ without structural change, the model is wrong

---

## Summary

```
η < 1: Good (symbiotic)
η ≈ 1: Bad (trophic balance)
η → ∞: Evil (ground negation)

The categorical break is at η → ∞.
Not a continuum. A discontinuity.
Good and Evil are different operations, not different degrees.
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

> **Status:** CORRECTED (v3.0) — population-dynamics proof added; categorical break formalized via Lotka-Volterra vs. uncoupled dynamics. Tier: [S] for dynamical claim, [C] for moral mapping. Awaiting independent verification by ecological modeler. See `../../08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/00_INTERNAL_REVIEW_FINDINGS.md`.
