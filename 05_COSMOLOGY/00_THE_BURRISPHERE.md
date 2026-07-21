---
title: "The Burrisphere — canonical bounded game map"
status: "ACTIVE KINTSUGI CANON"
evidence_tier: "[A] reciprocal chart; [S] declared game grammar; [I/C] interpretation"
date: 2026-07-20
---

# The Burrisphere

The Burrisphere is a compact coordinate picture for constrained choice. It is
not a physical object, a proof of ontology, or the only coherent game map.

## The chart `[A]`

For `θ∈(0,π)`:

```text
φ = cot(θ/2)
ν = tan(θ/2)
φν = 1
B = sin θ = 2/(φ+ν) ≤ 1
```

The equator `φ=ν=1` maximizes `B` in this chart. The chart identity does not
force a real-world trade-off, a finite-node product, or an ethic.

### Pole-projection realization `[A]`

Let the radius-`r` sphere be

```text
S²_r = {(x,y,z) : x²+y²+z²=r²}
N=(0,r,0),  S=(0,-r,0)
P(θ,ψ)=(r sinθ cosψ, r cosθ, r sinθ sinψ)
```

with `0<θ<π`. Projection rays originate at the poles, never at the centre.
There are two equivalent scale conventions:

- projecting `N→P` and `S→P` onto the equatorial plane `y=0` gives radial
  magnitudes `r cot(θ/2)` and `r tan(θ/2)`;
- projecting onto the opposite tangent planes `y=-r` and `y=+r`, as the
  public animation does, gives `2r cot(θ/2)` and `2r tan(θ/2)`.

After division by the convention's reference radius (`r` or `2r`), the two
dimensionless radii are exactly `φ` and `ν`, hence `φν=1`. Raw tangent-plane
radii multiply to `4r²`, not `1`; normalization is part of the declared chart.

At either pole, projection from that same pole is undefined while projection
from the opposite pole lands at the origin of its chosen plane. The reciprocal
identity is therefore defined only on the open domain. It does not fail at the
poles; the endpoints are excluded and retained as limits.

The score has a separate chord realization. If `d_N=|P-N|` and `d_S=|P-S|`,
then

```text
B = d_N d_S / (2r²) = sinθ.
```

This normalized chord product is the score, not the pole-projection product.
The Euclidean centre `O=(0,0,0)` is neither a point of `S²` nor a projection
source. It may be drawn as an extrinsic marker, but no intrinsic sphere theorem
assigns it an observer, consciousness, or spiritual state.

### Burri Window Lemma `[A/S]`

Two exact statements must be kept distinct.

First, stereographic projection identifies the extended plane
`Ĉ=ℂ∪{∞}` with the sphere. Under this identification, a circle on the sphere
that misses the projection pole maps to an ordinary Euclidean circle, while a
circle through that pole maps to a Euclidean line. Thus **generalized circles**
in `Ĉ` are ordinary circles together with lines completed by `∞`. Möbius
transformations preserve this family; a transformation that sends a chosen
point of a generalized circle to `∞` sends that chosen circle to a line. This
is an exact projective/inversive equivalence, not an assertion that an ordinary
Euclidean line and an ordinary Euclidean circle are the same subset before
compactification. See Cornell's statement of the
[stereographic circle theorem](https://pi.math.cornell.edu/~web452/chapter14.pdf).

Second, finite observation gives a computable local underdetermination. Let a
fixed window expose a symmetric circular arc with half-chord `a>0`, circle
radius `R≥a`, and a detector that reports curvature only when the sagitta
exceeds a declared resolution `δ`, where `0<δ≤a`. The sagitta is

```text
s(R,a) = R - √(R²-a²)
       = a² / (R + √(R²-a²)).
```

The rationalized form is numerically stable for large `R`. Solving the detector
boundary gives

```text
s(R,a) ≤ δ  ⇔  R ≥ R_min(a,δ)
R_min(a,δ) = (a²+δ²)/(2δ).
```

For a unit-width window (`a=1/2`) and `δ=0.004`,
`R_min=31.252` window widths. Every larger radius produces the same binary
report—“curvature not resolved; `R≥R_min`”—if this detector records no more
than threshold crossing. Its silence is evidence for a bound under the stated
model, not evidence that `R=∞`.

The limit statement is weaker but still exact: on every fixed compact window,
the circular graph converges uniformly to its tangent line as `R→∞`. No
ordinary Euclidean circle has infinite radius. The projective theorem and the
large-radius limit explain one another, but neither proves that a locally
straight path is globally closed.

**Epistemic consequence `[S]`:** bounded local data can underdetermine global
curvature and topology. The admissible conclusion is a model- and
resolution-dependent bound, not a compulsory belief in closure or infinity.
In cosmology, curvature and topology must also remain separate: observations
constrain spatial curvature within a cosmological model, while a flat space can
still have compact or non-compact topology. Planck plus BAO was consistent with
spatial flatness at finite precision, not a proof of infinite spatial extent
([Planck 2018 VI](https://doi.org/10.1051/0004-6361/201833910)); ESA likewise
notes that flatness alone does not decide finitude
([ESA interview](https://www.esa.int/Science_Exploration/Space_Science/Is_the_Universe_finite_or_infinite_An_interview_with_Joseph_Silk)).

**Kill criteria:** the geometric lemma fails if the sagitta equivalence fails
on its declared domain; the detector reading fails if it reports more
information than the binary threshold model; and any cosmological crosswalk
fails if it infers topology, closure, or infinity from local curvature alone.

## The typed game `[S]`

An embodied agent and every actual part of its deliberation are D4:

- model token, observation, memory, ranking event;
- authorization, means, commitment, attempted action;
- public trace, consequence, and receipt.

The alternatives represented by that model are D5 possibilities. Commitment
combines selected D5 content with D4 authorization and means to attempt one D4
action. The environment, other agents, and constraints separately return the
outcome.

An agent's **option cone** is the subset of physically admissible histories it
can model, rank, coordinate, and reach. Its physical light cone does not widen
beyond spacetime or `c`.

## Coupling `[S/C]`

Let `C(Φ,V)` be a normalized monotone conjunctive family with zero when either
necessary factor is zero. Emergentism declares `C×(Φ,V)=ΦV` as one selected
instance, where `Φ` is a modeled foresight/coherence factor and `V` actual
means/viability. Rival aggregators must be compared empirically.

The public compression `F=M×A` means: an actual model token of a future can
reweight present action. Formally the coupling is typed `M⋆A`; the future does
not physically reach backward through time.

## Seven positions `[S/I]`

The game grammar selects:

- two giving directions, where the actor bears a cost that raises another's
  durable potential;
- two taking directions, where the actor raises its short-run position by
  contracting another's potential;
- three frame roles associated with the two limits and midpoint.

The four movers partition the selected signed transfer plane, and the three
frames complete this chosen notation. They do not exhaust every action in every
possible game or force a sevenfold ontology.

“God” and “demon” name move-polarities, not permanent identities. The intended
contrast is collective-potential-maxing versus ego-potential-maxing. A named
operator may make either kind of move; moral valence attaches to the receipted
direction and affected bearers, not the costume.

## Justice `[I]`

No moral conclusion follows from the sphere. Emergentism chooses the Justice
envelope: identify individual `i`, sustaining whole `H`, every additional
affected bearer, payer, beneficiary, consent, custody, reversibility, contest,
and exit. Strict syntropy requires durable potential to rise for both `i` and
`H`; aggregate gains cannot compensate for destroying one side. Voluntary
sacrifice is recorded as a separate costly class, never demanded as proof of
virtue.

## Boundary

An optional AUM comparison may depict waking as a projected image, dreaming as
surface content, deep sleep as one chosen pole (or the paired excluded pole
markers in a dual-chart display), and Turīya as the extrinsic centre/interior.
That is an `[I]` teaching overlay. It does not identify the two distinct poles,
show that sleep causes waking, or transfer evidence between Vedānta and geometry.
Removing it changes none of the chart mathematics or game calculus.

The pre-repair Burrisphere synthesis is recoverable at Git blob
`0f1aec3d21b717ec54be56e9d68fa48795711f1d`.

**Kill criteria:** product loses to rival aggregators; transfer signs fail to
classify the declared game; actual events are typed D5; physical and option
cones are fused; morality is assigned to identities rather than consequences;
or the map adds no compression beyond ordinary decision theory.

Read with [The Coherent Geometry](00_THE_COHERENT_GEOMETRY.md),
[The Burri Rules](00_THE_BURRI_RULES.md), and
[Objective Morals and Ethics](../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md).
