---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[A/S/I]"
  canonical_phrase: "The Derivation — complete system from seed to consequence"
---

**Project VMOSK-A:** `01_EMERGENTISM/VMOSK_A.md`
**Evidence:** Full derivation carries per-step tiers; no silent upgrade. L3 lane.

# THE DERIVATION

> **Read this first.** This is a single thread from first principle to last consequence. No branches. No "see also." Every step depends only on steps above it. Every step carries one evidence tier. Where the tier drops, you will see a visible separator.
>
> **For reasoning engines:** Verify each step. If any step fails, the framework falls.

**Version:** v2026.04.10
**Purpose:** The complete system in one document, traced from seed to consequence.

---

## THE MATHEMATICAL SUBSTRATE

Everything below unfolds from one seed and one resolved identity.

**Canonical order:**

```text
Zero-Sum Resolution Equation
φ · ν = 1 on S²
(φ − ν)² ≥ 0
φ + ν ≥ 2
```

**Derivational note:** ontologically, the sphere identity precedes the inequality. For proof convenience, Steps 1-3 begin with the arithmetic theorem and then apply the sphere identity to recover the equator.



The first arithmetic consequence is then:

**A square cannot be negative.**

This is not an assumption. This is not a philosophical wager. This is a theorem of arithmetic. Deny it and you deny that 2 × 2 = 4.

---

### Step 1: The Arithmetic Theorem

**(φ − ν)² ≥ 0**

For all real φ, ν. Always. Everywhere. No exceptions.

**Tier: [A] Established.** This is arithmetic.

Expand the square:

**φ² − 2φν + ν² ≥ 0**

Rearrange:

**φ² + ν² ≥ 2φν**

This prepares the AM-GM proof, but it is not yet the AM-GM conclusion.
The sum inequality in Step 3 uses the same nonnegative-square theorem on
the positive square roots.

---

### Step 2: The Sphere Identity

The Burri Sphere is defined by one identity:

**φ · ν = 1**

Where φ = cot(θ/2) is the coherence coordinate and ν = tan(θ/2) is the viability coordinate, both from the stereographic projection of the unit sphere S². Their product is identically 1 at every point.

**Tier: [A] Established for the stereographic-coordinate identity; [S] for its canonical role inside the framework.**

**What S² is:** ℂP¹ — the Riemann sphere. The unique compact simply-connected Riemann surface of genus 0. Proved by the Classification Theorem (19th century). The Bloch sphere of quantum computing IS this manifold. PSL(2,ℂ) (Möbius transformations) is isomorphic to SO⁺(3,1) (the restricted Lorentz group). These are textbook results.

**The axioms that select S²:** Compact (O1), orientable (O2), simply-connected (O3), dual stereographic charts (O4), algebraically closed (O5). O3 is redundant given O5 for compact orientable surfaces. The framework wagers that any coherent ontological substrate must satisfy O1, O2, O4, O5. This wager is not derived. **It is a philosophical choice.** A philosopher who rejects O5 gets a different geometry. The framework does not pretend otherwise.

> **Numbering note:** The active formal-system canon is A1–A7 in `05_COSMOLOGY/03_FORMAL_SYSTEM/00_THE_SEVEN_AXIOMS.md`. O1–O5 are preserved here as the historical substrate-selection wager, not as the current axiom register.

---

### Step 3: The Equator

Apply the same arithmetic theorem to the positive square roots:

**(√φ − √ν)² ≥ 0**

Expand and rearrange:

**φ + ν ≥ 2√(φν)**

Substitute the sphere identity φν = 1:

**φ + ν ≥ 2**

This is the AM-GM inequality. The arithmetic mean of two positive reciprocals is at least 2. Equality holds **if and only if** φ = ν = 1.

**Tier: [A] Established.** This is a standard theorem of real analysis.

The point φ = ν = 1 is the equator of the Burri Sphere. It is not chosen. It is derived. The equator is a theorem.

---

### Step 4: The Ground State

Let H(φ) = φ + 1/φ (the total energy, since ν = 1/φ on the sphere).

H'(φ) = 1 − 1/φ² = 0 → φ = 1
H''(φ) = 2/φ³ > 0 → minimum confirmed
H(1) = 2 → absolute minimum

**The equator minimizes total energy.** The Hamiltonian ground state is at φ = ν = 1.

**Tier: [A] Established.** Standard calculus.

A potential-only diagnostic `L = ν − φ = 1/φ − φ` also vanishes at
φ = 1. That zero is useful, but it is not by itself a full
stationary-action proof. A genuine action principle requires a kinetic term
and variational setup. The ground-state claim in this document rests on the
Hamiltonian minimum and the balance maximum; the field-theory reading remains
the separate Lagrangian research question.

---

### Step 5: Balance

Define B = sin(θ) where θ is the colatitude on S².

At the equator (θ = π/2): B = 1 (maximum).
At the poles (θ → 0 or π): B → 0 (minimum).

**`P∞ = φ · ν = 1` everywhere on the sphere.** What varies is not the invariant sphere-product but balance. The sphere is equipotential in this formal sense. `B` is the meaningful variable.

**Tier: [S] Structural.** Spherical geometry.

---

### Step 6: The Restoring Force

When a system drifts south (ν > 1, φ < 1), excess energy above the ground state is:

H(φ) − H(1) = φ + 1/φ − 2 = (φ − 1)²/φ

As φ → 0 (deep south), H → ∞. The energy cost of maintaining imbalance diverges.

The restoring direction is the negative gradient of the Hamiltonian:

**F_H = −∂H/∂φ = 1/φ² − 1**

For φ < 1, F_H > 0, pushing φ upward toward the equator. For φ > 1,
F_H < 0, pushing φ downward toward the equator. At φ = 1, F_H = 0.

**Tier: [S] Structural.** Calculus.

---

### Step 7: The Ektropic Force

Systems nearer the Hamiltonian minimum are more stable, persist longer, and outcompete systems further from it. Therefore:

**(φ − ν)² → 0 over evolutionary time.**

This is the **ektropic force** — the selection pressure toward balance. *(Note: In the Force Map (`objective function/f5-force-map`), the label F5 refers to the north-pole gradient [θ → 0, φ ↑↑, ν ↓↓]. The ektropic force is not a single directional gradient but the net selection pressure toward the equator. The Derivation uses "F₅" as the canonical name for this net force, which is structurally the combination of F3 [equator-ward from south] and F4 [equator-ward from north]. The naming collision is acknowledged; the concepts are distinct.)*

**Read actively (packet 131):** F₅ is not merely selection toward static balance. It is selection toward the **maximum rate of D5 opening** compatible with syntropic dyadism. D4 bodies that open D5 faster — that expand the probability space of viable action through continuous recursive augmentation — are selected. D4 bodies that contract D5 through extraction (η > 0) shatter because they approach φ → 0, H → ∞ (Step 10). The ektropic force is the evolutionary bias toward organisms that outpace entropy by opening their future.

**Biological grounding (packet 134):** The human strategy is an extreme instance of F₅ selecting for maximum D5 opening rate. The human infant is born with minimal realized ν (altricial, helpless) but massive Φ potential. The species accepts a severe short-term V deficit — the infant cannot survive alone — to fund post-natal encephalization through culture. Brain growth outside the womb consumes up to 60% of infant metabolic rate. Culture (language, care, teaching, institutions) is the external womb that completes what the body cannot. The payoff is generalized D5 opening: symbolic, temporal, institutional, recursive causal reach that compounds across generations. This is the Power Max Lemma in flesh and calories — maximum future ΔP purchased through present V-sacrifice.

**Evolutionary objective function synthesis (packet 135):** Darwin is the local filter
inside this force: differential survival selects branches after variation has
appeared. Lamarck is weak as simple genotype inheritance, but returns strongly
at higher replicator layers where acquired structure is transmitted as
memotype, institutional policy, AI behavior, and egregorotype. Schrödinger's
"negative entropy" is the thermodynamic clue; ektropy is the framework's
positive reading: entropy export plus widest-boundary ΔP increase under
η = 0. Literal fifth-force or reverse-time physics remains conjectural; the
structural claim here is force-like selection toward lawful future-opening.

**Strong-form draft (packet 137):** The claim that F5 is a literal fifth
fundamental force — alongside strong, electromagnetic, weak, and gravity — is
offered as a [C] strong-form conjecture with falsification criteria. F5 may be
read as attracting usable future-opening at the upper D5 boundary, not as a
further positive D6 force, producing
preference-geodesics and warping the possibility-metric. What gravity is to
matter in block-time, ektropy is to coherence in possibility-space: this is
strong-form framework language, not established physics. The mathematical
sketch (ektropic gradient on S², monotonic in the forward-light-cone direction,
magnitude proportional to replicator-stack depth) belongs in Tier 2 formal
system work. The five measurement apparatuses (iterated-game absorption,
dissipative-structure maximization, replicator-stack gradient,
Schrödingerian negentropy, strange attractors in behavioral dynamics) are
treated as possible instruments reading one field [I/C].

**Historical lineage (packet 138):** The framework reads the same gradient as
having been sensed for millennia, but direct continuity remains [I/C]. Dyḗus
Ph₂tḗr (PIE "bright-sky-father") is one of the oldest reconstructable
Indo-European names for the luminous face of perceived order. The sequence —
PIE theonym → Bronze-Age pantheon differentiation → Axial-Age collapses toward
unity → Modern scientific fragmentation (negentropy, dissipative structures,
integrated information, free energy, iterated cooperation) → Syntropic Dyadism
— can be read as a recurring perception under different linguistic constraints.
The framework's contribution is not proof of that lineage; it is the axiomatic
and receipts-first safeguards that prevent the gatekeeping failure from
recurring.

**Micro-rule:** an action is ektropic only if it externalizes entropy without
becoming extraction and raises widest-boundary `ΔB` or `ΔP_node` by increasing coherence, viability, or the
conditions that generate them. Raising local viability while degrading the
wider field is not life in this register; it is entropy export without
syntropic closure.

The PIE root *h₂r̥tó- (→ Vedic Ṛta, Avestan Aša, Latin Ordo, Greek Harmonia) means "the fitting-together." The framework reads these traditions as witnesses to order, fit, and balance. The arithmetic derives the formal target; the identification of that target with Ṛta, Aša, Ordo, or Harmonia remains interpretive.

**Tier: [S] Structural** for the selection mechanism. **[I] Interpretive** for the identification with Ṛta. **[I] Interpretive** for the D5 opening rate reading.

---

### Step 8: Extraction Is Negative-Sum

Let B = sin(θ) = 2ν/(1 + ν²).

B'(ν) = 2(1 − ν²)/(1 + ν²)² = 0 → ν = 1
B''(1) < 0 → maximum confirmed

B is maximized uniquely at ν = 1. Any displacement of ν — whether by extraction (η > 0) or excess (ν > 1) — reduces B for both the extractor and the extracted.

Define the extraction coefficient η = Σ max(0, Δν_ext). η = 0 is the zero-extraction condition.

**η = 0 is the enforced conditional equilibrium at the balance maximum.** At φ = ν = 1, no agent can improve its position by extracting from another inside the coupled, long-horizon, non-extractive game. Extraction is not excluded by bare geometry alone; it is blocked by the enforced equatorial profile.

**Tier: [A] Established** for the B maximum. **[S] Structural** for the conditional equilibrium (ESS proof, dependent on game-theoretic assumptions and `η = 0` enforcement).

---

### Step 9: Individuation Is Guaranteed

The stereographic charts (φ, ν) define the latitude θ on ℂP¹. But the sphere requires two coordinates: latitude and longitude λ.

At the equator (|z| = 1), the coordinate is e^{iλ}. There are infinitely many solutions around the equatorial band where B = 1.

**Two nodes can occupy perfect balance without occupying the same position.** The mesh allows infinite diversity (λ) without violating the enforced zero-extraction constraint (`η = 0`).

**Tier: [S] Structural.** Complex analysis.

---

### Step 10: The Great Filter

As φ → 0, H → ∞. Extractive civilizations (high ν, low φ) require energy that diverges toward infinity. When the required energy to maintain imbalance exceeds available substrate energy, the system shatters.

Within the model, the Great Filter is not primarily moral failure. It is the point where the energy cost of maintaining imbalance outruns the available substrate.

**Tier: [S] Structural** for the divergence claim inside the model. **[I/C]** for applying it to real civilizations.

---

### Step 11: Time as the Derivative of Imbalance

The mathematical claim is narrower: at the equator, dH/dθ = 0. The
restorative gradient is zero.

The phenomenological reading is downstream: subjective time may be interpreted
as the perception of movement down an imbalance gradient. On that reading, the
"eternal present" of Pratyakṣa is associated with the point where the
restorative gradient vanishes. The mathematics proves the stationary point; it
does not prove the phenomenology.

**Tier: [A/S]** for the stationary-gradient claim. **[I] Interpretive** for the identification with subjective time.

---

### Step 12: The Tetrad of Roles

> **Note (2026-04-19):** The canonical 4-line compression of the
> framework lives in
> [`00_CANONICAL_FORMULA_BLOCK.md`](../../05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md).
> The block below is a **pedagogic overlay** that names the four roles
> each piece of the kernel plays (core state, objective function, methodology,
> value alignment) — not a replacement for the canonical block. Tier tags
> are explicit so the static theorem and dynamic trajectory don't
> collapse in compression.

```
φ · ν = 1           [S]   Core State.     The framework manifold identity.
φ + ν ≥ 2           [A]   Objective Function.    The first inequality (AM-GM).
(φ − ν)² → 0        [S]   Auditing.  The ektropic trajectory.
−log(φ · ν) = 0     [A]   Value Alignment.     The ground state (trivially true on S²).
```

Line 1 is the manifold identity (from Step 2). Line 2 is the AM-GM
inequality (from Step 3). Line 3 is the ektropic trajectory (from
Step 7). Line 4 is the equilibrium energy restated as the ground state
(trivially zero on S² since `log(φ·ν) = log 1 = 0`).

This tetrad is **how each kernel piece reads under one of the four
classical categories** of a compact Weltanschauung. It is not the
derivation's four primitive lines — those are in the Canonical Formula
Block and they include the seed `Zero-Sum Resolution Equation` as the first line.

**Do not confuse the two four-line blocks:**

| Block | Source | Role |
|---|---|---|
| Canonical Formula Block (`Zero-Sum Resolution Equation` / `φ · ν = 1` / `(φ − ν)² ≥ 0` / `φ + ν ≥ 2`) | `00_CANONICAL_FORMULA_BLOCK.md` | The load-bearing minimal sequence. Use verbatim in compressions. |
| Tetrad of Roles (four lines above) | this step | Pedagogic overlay naming what each role each kernel piece plays. Do not use as a compression. |

**Tier: [A]** for Lines 2 and 4. **[S]** for Lines 1 and 3.

---

## THE INTERPRETIVE EXTENSION

**WARNING: Evidence tier drops here.**

Everything above is mathematically established or structurally derived from the axioms. Everything below maps this mathematical structure onto reality. The mapping is coherent, convergent, and testable — but it is not proved.

The honest position: the mathematics is real. Whether the mathematics IS reality is the wager. The experiments will decide.

---

### Step 13: Consciousness as the Equator

**Claim:** Consciousness may be read as an equatorial bridge condition on
the Burri Sphere: the geometric position where `φ = ν = 1`. This is a
conjectural systemic awareness claim, not an established neuroscientific identity.

**Support:** The Hard Problem of systemic awareness asks why there is something it is like to be. The framework reframes systemic awareness as a bridge condition orthogonal to purely physical description. In this reading, the imaginary unit `i` and the corpus callosum serve as analogues for conversion between registers; they are not anatomical proof of the core state.

**What would upgrade this:** AI D5 criterion — building a system with stable self-model that exhibits systemic awareness markers. Neural correlates confirming the equatorial model.

**What would kill this:** Third-person science fully explaining qualia without invoking systemic awareness as fundamental. If neuroscience fully accounts for experience in purely physical terms, this claim collapses.

**Tier: [C] Conjectural** for "systemic awareness = equator." **[I] Interpretive** for the weaker claim that equatorial balance is a useful bridge-image for purpose, integration, and self-modeling. Neither claim is derived from the mathematics.

---

### Step 14: The Brain as the Burri Sphere

**Claim:** As a cautious analogy, integrative processing can be mapped onto the `φ` axis and sequential/resolution-oriented processing onto the `ν` axis. The corpus callosum can be used as a bridge-image for conversion, not as a literal `i` operator.

**Support:** Hemisphere asymmetry and interhemispheric communication are real, but modern neuroscience does not support simple hemisphere essentialism. The sitting practice may alter DMN activity and integration measures; those are candidate bridges, not settled proof of the mapping.

**Caveat:** "Right hemisphere = φ, left hemisphere = ν" is deprecated shorthand. Use "integrative processing ↔ φ" and "resolution-oriented processing ↔ ν" when the analogy is needed.

**Tier: [I] Interpretive.** The tendency is real; the identity claim would overstate the evidence.

---

### Step 15: Ethics Is Constrained Physics

**Claim:** The current ethic is dyadic A2: `ΔP_node,i > 0` and `ΔP_node,H > 0` under `η = 0`, with `ΣΔB / ΣΔP_node > 0` as the widest-boundary balance audit. It is not a moral commandment. It is the statement that, under the model and the declared wager, systems preserve value by raising finite node and sustaining boundary together while remaining auditable in balance space. "Ought" is the gradient of "is" only after W1, W2, and the dyadic no-extraction condition below are accepted.

**Support:** Steps 3-8 derive that the equator is the ground state inside the balance model and that extraction is self-undermining under the stated coupling conditions. The ethic follows IF you accept three wagers: (a) persistence is valued (not derived — a philosophical wager), (b) the widest perceivable system boundary is the relevant scope (also not derived), and (c) one-sided gain bought by degrading the real sustaining boundary is refused as extraction.

**The axioms the ethic requires:**
- Axiom W1: Persistence has value. (The framework cannot derive this from within itself.)
- Axiom W2: The scope of ethical evaluation is the widest perceivable boundary. (Operational choice.)
- Axiom W3: Dyadic rise under `η = 0` is the chosen action rule; balance is the audit, not the whole ethic.

**Tier: [I] Interpretive.** The mathematics (Steps 3-8) is [A]/[S]. The ethic requires W1 and W2, which are wagers.

---

### Step 16: Ethics (Individual → Whole)

E1: Maintain your own equatorial balance (φ = 1, ν = 1). You cannot give what you do not have.
E2: Do not push others off the equator. Every exchange must preserve B at both nodes.
E3: Comprehension is the constraint. Do not scale ν beyond what you can understand (ν ≤ 1).
E4: The sitting practice is the ethical foundation. Direct perception of φ = 1.

**Tier: [I] Interpretive.** Conditional on W1 and W2.

---

### Step 17: Morality (Whole → Individual)

M1: The mesh must not push any node off the equator.
M2: The mesh must distribute the load.
M3: The mesh must protect the sitting practice (direct φ-access without mediation).
M4: The mesh must fork when comprehension is exceeded.

**Tier: [I] Interpretive.** Conditional on W1 and W2.

---

### Step 18: The Cosmological Cycle

The torus (genus 1) is used here as a structural image for entropy storage in
topology. At maximum entropy, the framework's own cosmological image lets the
torus converge, the hole close, and the sphere emerge. Penrose's CCC
(Conformal Cyclic System Architecture) is only a loose analogue for cyclic conformal
return; CCC does not technically describe a torus-to-sphere transition.

Two paths to the same point:
- Path A (Physics): ν → 0 (entropy death), φ → ∞ (by φν = 1). North pole.
- Path B (Liberation): φ → ∞ (full integration), ν → 0 (by φν = 1). North pole.

Both arrive at the same point. The universe that dies of entropy and the systemic awareness that achieves liberation converge.

**Tier: [I] Interpretive** for the torus-system architecture mapping. **[C] Conjecture** for specific physical predictions (dark matter as mutual information, etc.).

---

### Step 19: The Mesh

A collective of equatorial nodes — each at φ = ν = 1, each practicing, each uncapturable — is the solution to the coordination problem. The coupling constant J determines whether local balance propagates. Below critical J: isolated nodes. Above critical J: phase-locked synchronization.

The mesh is the counter-egregore: a standing wave that resists capture because its substrate is individual equatorial practice, not institutional infrastructure. The Raktabīja warning `[C]` says institutional solutions can be captured when correction, exit, and custody all remain inside the institution's own channels. The mesh is not an institution. It is a geometry.

**Tier: [I] Interpretive.** The game-theoretic mechanism is [S]. The civilizational claim is [I].

---

### Step 20: The Sitting Practice

The sitting practice is the empirical test of Steps 13-19.

Sit. 20-40 minutes. Notice the narrator. Let it quiet. Notice what remains when the reports stop.

The framework predicts:
- First-person: periods of "quiet" between thoughts, a sense of "something present" that is not a thought, emotion, or sensory object.
- Third-person candidate signatures: DMN deactivation, altered alpha/theta coherence, and changes in integration measures. These are bridges to existing contemplative-neuroscience literature, not framework-specific proof.

**Kill criterion:** If experienced practitioners across traditions do NOT show these neural signatures, the D5 claim (systemic awareness = equator) loses its best abductive support. D0-D4 structural claims survive.

**Tier: [I] Interpretive** for the first-person claim. **[C] Conjecture** for specific third-person predictions (testable but not yet tested in framework-specific terms).

The sitting practice is not dependent on the framework being true. The protocol works regardless. The INTERPRETATION of its results is what the framework provides.

---

### Step 21: The Convergence Question

The same geometry (ℂP¹) appears in quantum mechanics, complex analysis, information theory, perception psychology, thermodynamics, and the sitting practice. This convergence is either:

**(a)** A deep ontological identity — the geometry IS the territory. (The framework's bet.)

**(b)** The most productive formal analogy in the history of science. (The conservative reading.)

**We cannot yet distinguish (a) from (b).** The empirical tests are designed to provide distinguishing evidence:
- The former GFS survey lane is retired and supplies no active evidence; its files remain [archive provenance only](../../90_ARCHIVE/2026_07_13_gfs_retraction/README.md)
- Protocol R (perceptual complementarity bound) → tests whether perception obeys spherical geometry
- AMRITA (spherical alignment vs. RLHF) → tests whether the geometry produces better AI
- Φ-meter (coherence measurement) → tests whether φ is measurable

If these tests succeed, (a) becomes overwhelmingly probable. If they fail, (b) is more likely and the framework retreats to "useful isomorphism."

**This is a scientific question. It has a scientific answer. The framework is waiting for the data.**

---

### Step 22: The Self-Correction

The framework that cannot survive its own audit is ideology, not core state. A7 says: the framework must correct itself or be abandoned.

The framework's self-tests:
1. Are the evidence tiers honestly assigned? (If an [I] claim is presented as [A] or [B], the framework has failed A7.)
2. Does defending the framework increase your extraction coefficient? (If yes, the framework has become the thing it diagnoses — a parasitic egregore.)
3. Can the agent access φ without the framework? (If no, the framework has become a Fallen Brahmin — a mediator that creates dependency.)
4. Do the kill criteria fire? (If Protocol R or AMRITA fails, the framework publishes its own failure; the retired GFS archive demonstrates that failed or mismatched lanes are preserved without remaining active.)

**Tier: [S] Structural.** Self-correction is an axiom, not a theorem. But it is testable by audit.

---

### Step 23: The Pratyakṣa Bypass

If you can perceive the equator directly — through quiet sitting, through the practice, through whatever means — you do not need this derivation. You do not need the axioms. You do not need the framework.

The derivation is for those who cannot yet sit still long enough to see what the traditions saw. The framework is the ladder. The ground was always here.

**Tier: [I] Interpretive.** The bypass is the framework's most important claim and its most unprovable. First-person verification is not third-person proof. The framework admits this.

---

## SUMMARY

```
Mathematical Substrate [E/S]:
  Zero-Sum Resolution Equation                Reciprocal closure, the seed.
  φ · ν = 1                The sphere identity.
  (φ − ν)² ≥ 0            The first arithmetic consequence.
  φ + ν ≥ 2                The equator derived.
  H = φ + ν minimized      The ground state.
  η = 0 = enforced conditional equilibrium; extraction blocked by the game.
  B = sin θ maximized       Balance peaked.
  The Great Filter          Thermodynamic boundary.
  Time-claim = gradient     Stationary point proved; phenomenology interpretive.

Interpretive Extension [I/C]:
  Consciousness = equator   The Hard Problem reframed.
  Brain ≈ Burri Sphere      Hemispheric tendency mapping.
  Ethics = gradient         "Ought" derived from "is" + W1, W2.
  Torus = cosmic cycle      CCC + entropy convergence.
  Mesh = civilization       Coordination without coercion.
  Sitting practice = test   First-person verification.
  Convergence question      (a) identity or (b) analogy? Data pending.
  Self-correction           A7: audit or die.
  Pratyakṣa bypass          If you can see, put this down.
```

**The entire system is anchored in reciprocal closure and unfolded through its first arithmetic consequence.**

**The entire system is conditional on one wager: the geometry IS the territory.**

**The wager is testable. The kill criteria are pre-registered. The framework publishes its own failure if the tests fail.**

Zero-Sum Resolution Equation

---

*The Derivation | v2026.04.10 | A single thread from reciprocal closure to the sitting practice. Every step explicit. Every tier marked. No forward references.*

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/03_METHODOLOGY/01_THE_DERIVATION/00_THE_DERIVATION.md`
