---
title: "D2 Functions and Geometry — Configuration Owner"
status: "ACTIVE FORMAL OWNER — 2026-07-21"
evidence_tier: "[A] standard function and graph mathematics; [S] typed atlas contract; [I/C] rung and μ reading"
owner: "D2 Configuration — this document is the sole semantic owner; Primitives and Type Signatures is the subordinate shared-schema index"
---

# D2 Functions and Geometry — Configuration Owner

D2 is the selected register of **configuration**: distinctions related in one
simultaneously inspectable structure. A graph of a function is the canonical
public instrument. It is not literally every function at once.

## 1. Carrier-to-relation lift `[A/I/C]`

The primary reduced neighbor begins with a bare declared carrier and adds a
relation:

```text
D1 carrier: X
D2 structure: (X,R),  R⊆X^k,  k≥1
ForgetRelation(X,R)=X
```

The construction is ordinary mathematics `[A]`. Calling the newly typed
relation a D2 freedom is the selected `[I/C]` crosswalk. Numbers can encode
relations, so no impossibility theorem is claimed; the narrower point is that
the D1 carrier contract has not yet declared `R` as a relation with its own
invariants and interventions.

## 2. Function and graph types `[A]`

```text
Function := (domain:X, codomain:Y, rule:f)
Graph(f) := Γ_f = {(x,f(x)) : x∈dom(f)} ⊆ X×Y
```

Because a function already includes a rule relating domain and codomain, the
passage `f→Γ_f` is a visualization/re-expression inside D2, not by itself the
D1→D2 lift. It makes domain, range, zeros, poles, symmetry, and limiting
behavior jointly visible. It adds no new mathematical truth and proves no
ontological dimension.

## 3. Set membership and diagonal boundary `[A/I/C]`

For any already declared set `A`, standard set theory supplies

```text
𝒫(A) := {B | B⊆A}
Mem_A := {(a,B)∈A×𝒫(A) | a∈B}.
```

`Mem_A` is a rigorous D1-to-D2 **neighbor** for this scaffold: named elements
are lifted into a simultaneously inspectable membership configuration in a
product. The power-set and membership constructions are standard mathematics
`[A]`; treating that relational lift as an instance of `μ₁` is `[I/C]`, not a
theorem that set formation creates a physical dimension.

Russell's expression must not be promoted into an object:

```text
R? := {x | x∉x}
R?∈R?  ⇔  R?∉R?
```

The contradiction shows that **unrestricted comprehension cannot form `R?` as
a set**. In ZF-style set theory, separation has the bounded form
`{x∈A | P(x)}` for a prior set `A`; no universal set is supplied. In typed or
universe-stratified systems the same attempted self-application crosses a type
or universe boundary. The Russell construction is therefore a set-formation
boundary, not projective infinity, not the projective point `∞_P`, and not
evidence of a μ-crossing.

Cantor's neighboring theorem can be stated without a universal set. For any
declared function `f:X→℘(X)`, form the bounded diagonal subset

```text
D_f := {x∈X | x∉f(x)} ∈ ℘(X).
```

If `f` were surjective, some `a∈X` would satisfy `f(a)=D_f`; then
`a∈D_f ⇔ a∉f(a)=D_f`, a contradiction. Hence no `f:X→℘(X)` is
surjective. This theorem is `[A]`. Placing its same-level totalization boundary
beside `μ₁` is `[I/C]`; it neither proves a new physical dimension nor turns the
Russell class into a set.

## 4. The finite function atlas `[S]`

```text
FunctionAtlasEntry := {
  id:String,
  domain:String,
  codomain:String,
  formula:String,
  parameters:Map,
  singularSet:[String],
  asymptotes:[String],
  symmetries:[String],
  evidenceTier:EvidenceTier
}
```

An atlas renders a declared finite family—linear, polynomial, reciprocal,
exponential, logarithmic, trigonometric, rational, or other named entries.
"All functions" means only "all entries currently declared in this atlas."
No single two-dimensional chart contains every function or every function
space without a coding convention.

## 5. Compactification and geometry `[A]`

The real projective line is a one-dimensional compactification:

```text
ℝP¹ = ℝ ∪ {∞_P}
dim_ℝ(ℝP¹)=1.
```

Adjoining the boundary point `∞_P` does not create D2. It changes the global
structure of the D1 line while preserving its real dimension. The selected D2
opening requires an explicit relational/configurational lift, such as
`Γ_f⊆X×Y` or `Mem_A⊆A×𝒫(A)`.

The Riemann sphere `ℂP¹≅S²` compactifies the complex plane with one projective
point at infinity. A Möbius transformation maps generalized circles (circles
or lines in the plane) to generalized circles. Thus a line is exactly a circle
through the projective point at infinity in this geometry—not a Euclidean
circle of literally infinite radius.

From a bounded observation window, small curvature can be indistinguishable
from zero within declared tolerance. That licenses a bound on curvature/radius,
not a conclusion that a line closes or that physical space is finite.

The Bloch sphere uses the same underlying `S²` for **pure qubit rays**, but its
distinguished quantum structure is not the reciprocal Burri chart. Mixed
qubit states occupy the Bloch ball. Shared manifolds do not transfer meanings.

## 6. μ₁ as a transparent representational crossing `[I/C]`

```text
μ₁:D1→D2
newFreedom = simultaneous relation/configuration
Recover₁(X,R) = X
constructionStatus = reduced [A/S]
emergenceTier = [I/C]
```

For the carrier-to-relation example, the crossing is constructively weak:
`(X,R)` is explicitly declared from `X` and `R`; forgetting the relation returns
`X`. `Γ_f` is a visualization of an already relational function. `Mem_A` is
defined from `A`, `𝒫(A)`, and membership. Calling these relation-bearing
structures a D2 opening is the selected `[I/C]` crosswalk. The
broader claim that nature contains a strongly emergent D1→D2 crossing remains
`[C]` and currently lacks saturation evidence.

## 7. Boundary to D3

D2 can specify a Hilbert space, operators, matrices, a state-space manifold,
and a measurement family as mathematical configurations. D3 begins only when
a normalized positive quantum state is assigned and thereby supplies
context-indexed outcome probabilities. The carrier geometry belongs here; the
probability-bearing quantum state belongs to D3.

*D2 makes relations visible. It does not make a picture into a cause, a quantum
state, or the territory.*
