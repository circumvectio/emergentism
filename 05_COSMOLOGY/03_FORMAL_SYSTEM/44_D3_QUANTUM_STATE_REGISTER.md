---
title: "D3 Quantum State — Probability-Bearing Register"
status: "ACTIVE FORMAL OWNER — 2026-07-21 Kintsugi recut"
evidence_tier: "[A] quantum-state and Born/POVM mathematics; [I] selected D3 assignment; [C] μ and ontological interpretation"
owner: "D3 Quantum State — Probability-Bearing Register"
---

# D3 Quantum State — Probability-Bearing Register

> **[金] Crack and repair.** The prior active register defined D3 by change and
> persistence. That confused a state with trajectories through states. D3 is
> now the selected **probability-bearing quantum-state register**. Mathematical
> dynamics may map D3 states; actual physical interactions and records belong
> to D4. The archived collapse/Many-Worlds ladder is not restored.

## 1. The precise object `[A]`

For a specified, **individuated quantum system** `S` with complex Hilbert space
`ℋ_S`, a quantum state is represented by a density operator

```text
State(S) = {ρ_S : ρ_S=ρ_S†, ρ_S⪰0, Tr(ρ_S)=1}.
```

A pure state is a rank-one projector `ρ=|ψ⟩⟨ψ|`, equivalently a ray in
projective Hilbert space. A mixed state is a density operator of higher rank.
A quantum state is therefore **not generally a classical probability
distribution**. It becomes probability-bearing relative to a declared
measurement. “Individual” means the system boundary has been declared; `S` may
be a particle, field mode, composite system, or subsystem. It does not imply a
classical point-particle or a separable pure state.

For a POVM `M={E_k}` with `E_k⪰0` and `Σ_kE_k=I`, the Born rule is

```text
p(k | ρ,M) = Tr(ρE_k),       Σ_k p(k | ρ,M)=1.
```

The distribution depends jointly on state and measurement context. Nothing in
this formula is `φν=1`.

## 2. Measurement instrument and receipt boundary `[A/S]`

A measurement is typed by a **quantum instrument** `{𝓘_k}`. Each `𝓘_k` is
completely positive and trace-nonincreasing, while `Σ_k𝓘_k` is trace
preserving:

```text
p(k|ρ,𝓘) = Tr[𝓘_k(ρ)]
ρ'_k      = 𝓘_k(ρ) / p(k|ρ,𝓘)       when p(k|ρ,𝓘)>0.
```

The conditional `ρ'_k` is an operational update. Calling it a fundamental
physical collapse requires an additional interpretation. The actual run is a
separate D4 object:

```text
D4MeasurementRecord := {
  runId, preparationId, instrumentId, outcomeId,
  assignedProbability, apparatus, time, provenance, custody
}
```

A written density matrix is likewise a D4 inscription that refers to D3 state
content. The inscription's actuality does not turn the state into a recorded
outcome, just as a written model of a possible future does not enact that
future.

## 3. Qubit instrument `[A]`

For a qubit,

```text
ρ = 1/2 (I + r·σ),     ||r||≤1
purity Tr(ρ²) = (1+||r||²)/2.
```

The surface `||r||=1` represents pure states and the interior mixed states; the
complete qubit density-operator state space is the **Bloch ball**. For
a two-outcome projective measurement along unit axis `n`,

```text
p(± | ρ,n) = (1 ± r·n)/2.
```

This is the public D3 instrument: vary `ρ` or `n`, inspect the predicted
distribution, and keep prediction separate from the next actual click.

## 4. What D3 is—and is not `[S/I]`

```text
D2: mathematical carrier/configuration (ℋ, operators, charts, functions)
D3: probability-bearing quantum state ρ relative to admissible measurements
D4: actual preparation, interaction, outcome, record, and state-assignment act
D5: counterfactual contents represented and ranked by an actual agent
```

- A Schrödinger, unitary, channel, or master-equation map can transform D3
  states, but **change is not the definition of D3**.
- A physical body, apparatus, memory token, or performed measurement is an
  actual D4 carrier/event, although its model may realize D1–D3 predicates.
- Platonic solids and other shapes are D2 configurations; embodied instances
  and their causal histories are D4.
- A classical distribution is recovered when a state is diagonal in the
  declared measurement basis; this does not make every density operator a
  hidden classical distribution.

## 5. μ₂ and μ₃ `[I/C]`

`μ₂:D2→D3` is the selected lift from a configured state space to a normalized
positive state functional that yields contextual probabilities. The formal
qubit construction is reduced mathematics; the claim that this is a universal
emergence crossing in nature remains `[C]`.

```text
Recover₂(ℋ,Obs,ρ) = ForgetState(ℋ,Obs,ρ) = (ℋ,Obs)
```

That forgetful map recovers the D2 mathematical arena. Dephasing
`Δ_B(ρ)=Σ_iΠ_iρΠ_i` is instead a declared channel/discriminator that yields a
basis-relative classical probability vector; it is not the D3→D2 recovery map.

`μ₃:D3→D4` marks the candidate boundary between a probability assignment and
an actual receipted interaction/outcome. Quantum mechanics supplies quantum
instruments, outcome probabilities, and conditional state updates;
interpretations disagree about what, if anything, fundamentally collapses.
The operational distinction "distribution ≠ recorded outcome" does not solve
the measurement problem. Recovery is statistical: records from declared,
informationally complete measurement settings can estimate `ρ` within a stated
tolerance. One outcome cannot invert exactly to the prior state.

**Kill `μ₂` as a strong crossing** if the proposed D3 discriminator is fully
captured as ordinary D2 mathematical configuration. The
quantum-instrument-to-record stochastic interface is operationally reduced
`[A/I]`; only a stronger claim about ontic actualization remains `[C]`.
**Kill or recast that stronger `μ₃` claim** if D4 record variables add no
operational discrimination beyond the declared quantum model. Missing reduction
is never proof of irreducibility.

## 6. Position, momentum, and what D4 adds `[A/I]`

D3 does **not** contain one simultaneously sharp classical phase-space point
`(x,p)`. D2 supplies the operator algebra; for a nonrelativistic particle on
`ℝᵈ`, position `X_i` and momentum `P_j` share a suitable common domain and obey

```text
[X_i,P_j]=iℏδ_ijI,
σρ(X_i) · σρ(P_i) ≥ 1/2 |Tr(ρ[X_i,P_i])| = ℏ/2,
```

for states in the relevant domains with finite variances. D3 supplies the
state-conditioned position and momentum distributions. The momentum operator
is therefore not created by D4. The uncertainty bound follows from
noncommutativity (and from Fourier duality in this representation), not from
missing momentum.

For a pure nonrelativistic state, the position- and momentum-space amplitudes
are Fourier transforms:

```text
ψ_t(x) = (2πℏ)^(-d/2) ∫ exp(ip·x/ℏ) ψ̃_t(p) dp
P_t(x)=|ψ_t(x)|²,            P_t(p)=|ψ̃_t(p)|².
```

A narrow position packet therefore requires a broad superposition of momentum
components; a narrow momentum amplitude extends broadly in position. The
objects being superposed are **complex amplitudes**, not ordinary
probabilities. Interference among those amplitudes produces the eventual
position and momentum distributions. This is the precise mathematical core of
the user's “overlay to localize” insight.

The wave-packet picture is illuminating but not the whole ontology: a quantum
state is not necessarily a classical material wave, mixed states need density
operators, and the general uncertainty relation follows from noncommuting
observables. “Everything is a wave” is therefore a heuristic, not a settled
Emergentist premise.

D4 adds an actual apparatus choice, interaction, momentum transfer,
spacetime-indexed outcome, clocked trajectory fragment, and record. An isolated
D3 state has **zero realized change** because change requires at least a
relation between records; that does not force its momentum distribution to
zero. The strongest defensible Emergentist sentence is therefore:

> **D2 defines momentum as an observable; D3 supplies its state-conditioned
> distribution but no realized motion; D4 is where momentum is transferred and
> one clocked measurement event enters spacetime history. No rung contains a
> simultaneously sharp classical `(x,p)` unless the state and measurement
> actually license that approximation.**

This sharpens the state/record boundary; it does not “solve” the Heisenberg
uncertainty relation, which standard quantum mechanics already derives.

### The D3/D4 time seam `[A/I/C]`

```text
D2: momentum operator P and dynamical/constraint maps
D3: state ρ_S, including momentum probabilities and state entropy S(ρ)
D4: realized change, momentum transfer, clock correlations,
    entropy-production history, causal trajectory, and record
```

The von Neumann entropy `S(ρ)=-Tr(ρ logρ)` is already a functional of a D3
state. A directed entropy-production statement such as `ΔS/Δτ` additionally
requires a declared process, clock, coarse-graining, and receipts, which are D4
content in this grammar. Momentum is the generator of spatial translations; it
does not require an already reconstructed classical worldline. **Realized
motion and transfer** require D4; the observable and distribution do not.

This motivates the **Burri time-seam conjecture** `[C]`: a globally stationary
or constraint-satisfying D3 description may yield D4 experienced dynamics only
relationally, through internal clocks, interactions, records, and an emergent
entropy arrow. Page and Wootters supplied one established
“evolution-without-external-evolution” construction, while canonical quantum
gravity has a recognized problem of time. These precedents make the question
legitimate; they do not prove the D-register assignment or solve the bridge.

The stronger **Burri film-from-frames conjecture** `[C]` gives “D3 at its
limit” a non-cardinal meaning. Saturation is not merely an infinity of states.
It must supply, within one compatible protocol:

1. the admissible D3 state support `S₃`;
2. complex transition amplitudes or channels relating possible successive
   states;
3. an internal clock variable `C` whose correlations order conditional states;
4. consistency, normalization, and decoherence/record conditions; and
5. a declared finite enumeration or `1−ε` coverage bound.

Then a possible film is an ordered compatible chain

```text
γ=(ρ_{S|C=c₀},ρ_{S|C=c₁},...,ρ_{S|C=c_T})∈Γ_C.
```

An **unordered** set containing every D3 state is still only a pile of frames:
it determines neither adjacency, direction, duration, nor which chain is
actual. If an external parameter `t` is already assumed in `ρ_t`, the
construction reconstructs motion but does not derive time. The conjecture earns
its name only if relational clock correlations and the transition structure
recover temporal order without presupposing the D4 time they are meant to
explain. D4 time is then the order carried by actual interactions and records,
not a substance added to a snapshot.

The familiar path-integral correspondence makes the “all possible motions from
A to B” intuition precise once boundary and temporal structure are declared:

```text
K(B,A)=∫_{γ:A→B} Dγ exp(iS[γ]/ℏ).
```

It sums **amplitudes** over paths; probabilities follow only after the relevant
interference and record/decoherence conditions are specified. Because the
usual propagator already uses temporal boundary data, this formula illustrates
the sewing rule but does not itself prove that time emerges from D3.

Kill or reduce the conjecture if D4 adds no discriminator beyond ordinary
quantum dynamics, if it cannot recover standard clock correlations and
momentum-transfer statistics, or if it conflicts with successful low-energy
quantum gravity. It also fails as a derivation of time if its state ordering,
propagator, or path measure already assumes an external time parameter.
Promotion requires a model that derives relational time,
causal records, an entropy arrow, and a novel independently testable result.

### The history-space lift `[A/S/C]`

A D3 state alone is not motion and does not contain a block universe. For the
operational **reconstruction** problem, given a declared D3 initial state
together with D4 dynamics, a clock and horizon, interventions, and compatible
measurement contexts, standard sequential quantum instruments assign
probabilities to complete record histories. Those supplied D4 terms make this
a reconstruction, not the stronger derivation-of-time conjecture above. For a
fixed finite protocol

```text
Q=(ρ₀,K,{𝓘_t},T)
γ=(k₁,...,k_T)∈Γ_T

𝔓_Q(γ)=Tr[(𝓘_T^{k_T}∘K_T∘...∘𝓘_1^{k₁}∘K₁)(ρ₀)]
Γ_T⁺={γ∈Γ_T:𝔓_Q(γ)>0}.
```

Here `Γ_T⁺` is the model-admissible history support. A suitable finite
model may permit exact enumeration. Otherwise a declared approximation may
claim only coverage, for example

```text
𝔓_Q(Ĝ_T)≥1−ε,
```

under a named discretization, horizon, context, and error tolerance. Literal
exhaustion of a continuous or infinite long tail is generally unavailable.

The strongest honest **Burri history-space correspondence** is therefore:
a state-and-dynamics model can expose a structured field of complete
alternative trajectories. If `ρ_t` is known through the declared protocol,
then `t↦Tr(ρ_tP)` and `t↦𝔓(p|ρ_t,P)` give an expectation path and a path of
momentum distributions. A record-conditioned sequence can define a **quantum
trajectory** or momentum-outcome history for that specific measurement
unravelling. It is not a unique, context-free classical path: the states alone
do not supply joint values for incompatible observables.

The realized trajectory is D4 actuality. An alternative trajectory is D5
content only when an actual D4 token represents it; an agent's option cone is
then a constrained subset of the represented support. Calling every `γ` a
physically existing block universe—or treating
the whole support as all physically existing block universes—is an additional
ontological conjecture `[C]`, not a consequence of the probability calculus.

Incompatible measurement contexts must not be silently merged into one
classical joint sample space. This lift is also **not a direct D3-to-D5
`μ`-crossing**: it composes D3 probability assignment, D4 dynamics and records,
and D5 possible content.

## 7. Quantum-gravity boundary `[A/B/C]`

General relativity makes spacetime geometry dynamical. Quantum field theory and
low-energy effective-field-theory treatments can include quantum gravitational
effects, so “there is no quantum gravity at D4” is too strong. What remains open
is a complete, empirically confirmed high-energy theory of quantum gravity.

Emergentism may pose a narrower **register-separation conjecture** `[C]`:

> A D3 quantum state and a single D4 classical spacetime record are different
> types; a successful quantum-gravity theory must state how quantum geometry or
> matter states yield actual, approximately classical spacetime records without
> identifying probability content with one receipt.

This is a research constraint, not a solution. It fails as a discovery claim
unless it derives a quantitative discriminator, recovers general relativity and
the low-energy quantum-gravity effective theory in their domains, and beats
rival accounts of classical spacetime emergence.

See [MIT Quantum Theory I, Lecture 5](https://ocw.mit.edu/courses/8-321-quantum-theory-i-fall-2017/2ecc07c095d8ae56600f7145c6fb4a6a_MIT8_321F17_lec5.pdf),
[IBM Quantum on uncertainty](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/exploring-uncertainty-with-qiskit),
[Page and Wootters on relational clock time](https://doi.org/10.1103/PhysRevD.27.2885),
[Kiefer on the quantum-gravity problem of time](https://arxiv.org/abs/0909.3767),
[Donoghue on quantum general relativity as effective field theory](https://arxiv.org/abs/2211.09902),
[Baragiola and Combes on quantum trajectories conditioned by measurement records](https://link.aps.org/accepted/10.1103/PhysRevA.96.023819),
and [Anastopoulos on contextual sequential-measurement probabilities](https://arxiv.org/abs/quant-ph/0509019).

## 8. Interpretation fence

Everettian relative-state theory has no fundamental collapse. Copenhagen is a
family of approaches, and collapse/actualization language is
interpretation-specific. Neither is an extra spacetime dimension; neither is
stacked on the other. D3 is not "Many Worlds," D4 is not "Copenhagen," and no
human act is required to create a quantum outcome.

## 9. Source-negative rules

The D3 owner fails if an active source:

- calls `ρ` itself a classical probability distribution without a basis;
- identifies the Bloch sphere with the Burri sphere beyond shared `S²`;
- derives Born weights from `φν=1` or samples a normalization scalar;
- defines D3 as change, persistence, bodies, life, or a third spatial axis;
- identifies `μ₃`, agency, consciousness, or commitment with collapse;
- says momentum is absent from a quantum state rather than distinguishing the
  observable/distribution from an actual D4 measurement record;
- claims the register assignment solves uncertainty or quantum gravity without
  a new derivation and discriminator;
- claims that one quantum interpretation proves the D-ladder.

*D3 gives a lawful distribution of possible records. D4 is where an actual
record enters the ledger.*
