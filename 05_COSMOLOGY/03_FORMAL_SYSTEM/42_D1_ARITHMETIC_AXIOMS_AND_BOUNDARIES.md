---
title: "D1 Arithmetic — Typed Axioms and Boundary Semantics"
status: "ACTIVE FORMAL OWNER — 2026-07-21 Kintsugi repair"
evidence_tier: "[A] standard mathematics in named structures; [S] typed interface; [I/C] Emergentist rung and μ reading"
owner: "D1 Arithmetic — this document is the sole semantic owner; Primitives and Type Signatures is the subordinate shared-schema index"
---

# D1 Arithmetic — Typed Axioms and Boundary Semantics

D1 is the selected register of **distinction**. Arithmetic is its first public
instrument, not a claim that numbers caused reality. Every expression below is
evaluated in a named type; changing the type is an explicit operation.

## 1. The sovereign frame and signed number spine `[A/S/I]`

The object-level D0 carrier has one opaque role and no positive freedom. The
Titan names belong to the metalanguage used to describe its boundary:

```text
Carrier(D0) := {ground_0}
PositiveFreedom(Carrier(D0))=∅
TitanFrame : Type_Meta
0_T : TitanFrame                 # ground-facing metaframe term
0_N : Number
ground_0 ≠ 0_T
0_T ≠ 0_N
NoCoercion(TitanFrame,Carrier(D0))
TitanFrame ↛ Number
```

`ground_0` is the sole D0 object-level role. `0_T` is the metalinguistic
Ground_T seat rendered by the point glyph `•`; it is not a token inside D0 and
neither belongs to nor seeds a number set. The selected D1 presentation opens
instead with an oriented unit-magnitude pair:

```text
SignedUnit_N := {+1_N, -1_N}
ℕ⁺ := {1_N,2_N,3_N,…}
-ℕ⁺ := {-n_N | n_N∈ℕ⁺}
SignedMagnitude := {+,-}×ℕ⁺
embed(+ ,n)=n; embed(- ,n)=-n
ℤ_• := image(embed) = ℕ⁺ ⊎ (-ℕ⁺) = ℤ \ {0_N}
```

Here `⊎` is the ordinary union of two disjoint subsets of standard `ℤ`; the
product `{+,-}×ℕ⁺` is the tagged construction that does not presuppose the
integer carrier. The equality with `ℤ\{0_N}` is the image of the displayed
embedding, not an independent construction of all integer operations.

The mathematical facts about these sets are `[A]`; reading the co-opening of
the two orientations as the first D1 distinction is a selected Emergentist
interpretation `[I]`. It is not a derivation of the integers from a Titan.

`ℤ_•` is the **nonzero signed-integer set**, not an additive group or ring:

```text
(+1_N)+(-1_N)=0_N ∉ ℤ_•
```

It is closed under multiplication but lacks multiplicative inverses for most
members. Standard integer arithmetic therefore uses the explicit completion

```text
ℤ := ℤ_• ⊔ {0_N}.
```

The subsequent ambient fields and their nonzero multiplicative sectors must
also remain distinct:

```text
ℤ ↪ ℚ ↪ ℝ ↪ ℂ
ℚ^× := ℚ \ {0_N}
ℝ^× := ℝ \ {0_N}
```

`ℚ` and `ℝ` are fields and contain numeric zero; `ℚ^×` and `ℝ^×` are their
multiplicative groups and exclude it. Neither nonzero sector is closed under
addition. Each extension solves a named closure or completion problem; none
makes every syntactic expression meaningful.

“Whole numbers” is skipped as a primitive rung. Where the pedagogical term
means `{0,1,2,…}`, it is only the subset `{0_N}∪ℕ⁺` and adds no structure.

The field division operation is partial:

```text
div_F : F × (F \\ {0}) → F
```

Therefore `a/0` is undefined in every field. This is a domain fact, not a
numerical value and not proof of an emergence event.

## 2. Unit-multiplicity construction `[A/S/I]`

The Emergentist D1 presentation begins with a nonempty unit, not with numeric
zero:

```text
UnitSeed U := {★}
1_N := |U|
n_N := |U₁ ⊔ U₂ ⊔ … ⊔ U_n|,  n≥1
ℕ⁺ := {n_N | n≥1}
```

Thus every positive natural is a finite **multiplicity of one**: equivalently,
`n_N=1_N+⋯+1_N` with `n` summands. It is not a product of ones, because every
finite product `1_N·…·1_N` still equals `1_N`. Addition corresponds to disjoint
union of finite representatives; multiplication of finite cardinals
corresponds to Cartesian product.

`U` is a chosen singleton representative and `1_N` is the first positive
cardinality in this presentation. It is not literally “the first set” of
standard set theory: `∅` is also a set, and many distinct singleton sets have
the same cardinality. The canonical claim is about positive cardinality, not a
unique ontological set.

Numeric zero enters the signed integer system only through explicit completion:

```text
0_N := |∅|
adjoin₀(ℤ_•) := ℤ = {0_N} ∪ ℤ_•
```

So `0_N∉ℕ⁺` and `0_N∉ℤ_•`; it is not a positive successor or a multiplicity of
the nonempty unit. It is present in the standard integers and every subsequent
ambient field because their additive structure requires it. This is a
categorization choice, not deletion of zero from standard mathematics.

The types remain separate across the origin aperture:

```text
1_T : TitanFrame
1_N : Number
1_T ≠ 1_N
μ₀ does not coerce 1_T into 1_N
```

The Titan term frames the unit role; the singleton construction supplies an
ordinary arithmetic representative after D1 opens. No Titan arithmetic occurs.

## 3. Five statuses that must not be conflated `[A/S]`

```text
EvaluationStatus :=
  value | undefined | indeterminate_form | diverges | extended_value
```

| Expression | Declared setting | Status |
|---|---|---|
| `a/b`, `b≠0` | field `F` | `value` |
| `a/0` | field `F` | `undefined` |
| `0/0` | field `F` | `undefined` |
| `0/0` inside a limit | limit syntax | `indeterminate_form` |
| `lim_(x→0+) 1/x` | extended real line | `extended_value: +∞` |
| `lim_(x→0−) 1/x` | extended real line | `extended_value: −∞` |
| `lim_(x→0) 1/x` | ordinary two-sided real limit | `diverges` / does not exist |

`∞` is not thereby an ordinary field element. In the real projective line one
may adjoin one unsigned projective point; in the extended real line one may
adjoin the ordered endpoints `−∞,+∞`. Those are different constructions.

## 4. The sovereign Titan/projective boundary `[A/I]`

The opaque type `TitanFrame={0_T,1_T,∞_T}` carries the roles
`{Ground_T,Unit_T,Horizon_T}`, is rendered by `{•,⊙,○}`, and is visually
associated with `{0,1,∞}`. Rendering is not coercion:

```text
TitanFrame ↛ Number
ArithmeticSignature(TitanFrame)=∅
add_T, sub_T, mul_T, div_T, pow_T, log_T : undefined
```

Titan frames therefore remain outside arithmetic. Ordinary numeric `0` and `1`
remain numbers and lawful operands. The projective point `∞` is admitted only
after an explicitly named extension. The live three-seat display is deliberately
operator-free:

```text
•     ⊙     ○
0_T   1_T   ∞_T
```

The former infix glyph rendering is historical typography, not a live formula:
`mul_T` is undefined, and projective infinity is not a field element, so numeric
`0×∞` is not a well-formed field product. The notation `0·∞` may name an
indeterminate **limit form**, or it may acquire a separately declared rule in a
named extended arithmetic. No operator may be inserted between the Titan seats
and used as a proof.

The prohibition is total within the Titan type: apparent expressions such as
`1_T/1_T`, `0_T/1_T`, `∞_T/1_T`, and `0_T×∞_T` are not operations with unusual
values; they are inadmissible terms. This does not revoke ordinary arithmetic
on the distinct number type.

A deliberately typed projective reciprocal map may instead be defined, for
`N∈ℂ\{0}`, as

```text
f_N : ℂP¹ → ℂP¹
f_N(z)=N/z for z∈ℂ\\{0};  f_N(0)=∞;  f_N(∞)=0.
```

That total map is a construction on `ℂP¹`, not a repaired field quotient.

## 5. Reciprocal-chart facts `[A]`

For `x>0`, let `s=log x`, inversion `ι(x)=1/x`, and
`E_s(x)=(log x)²`. Then

```text
s(1/x)=-s(x)
E_s(1/x)=E_s(x)
sign(log 1)=0
```

`E_s` is a convex quadratic in the coordinate `s`; it is not globally convex
as a function of `x`. Projective equality of rays does not erase sign:
`[-1:1]≠[1:1]` on `ℝP¹`.

## 6. Suda source reconciliation `[A/B/I/C]`

Minoru Suda's 2025 Parts I–III package several useful reciprocal constructions:
division by a **nonzero** divisor as multiplication by its reciprocal, the
projective swap `0↔∞`, the positive-ray reflection `log x↦−log x`, the invariant
`E_s=(log x)²`, the hinge coordinate `u=(x−1)/(x+1)` with `u(1/x)=−u(x)`, and
the phase bit `sign(log x)`. These formulas are standard or directly checkable
mathematics `[A]`; Suda's contribution here is their packaging and proposed
interpretation `[B/I]`.

The reconciliation also corrects four boundaries:

- `E_s` is strictly convex in `s=log x`, not globally in `x`;
- `sign(log 1)=0`, and inversion on the full projective line fixes `±1`, not
  only the selected positive fixed point;
- the ordinary two-sided limit `lim_(x→0)1/x` does not exist, so Suda's
  `0*:=lim_(x→0)1/x=±∞` cannot redefine `0/0` as standard arithmetic;
- names such as "energy," "critical singularity," "fold," and "infinite egg"
  are interpretive proposals `[I/C]`, not consequences of the formulas.

The remaining Suda papers may inform later philosophical comparisons, but they
provide no additional D1 arithmetic axiom. See the
[source crosswalk](../../03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/SUDA_DIMENSIONAL_CROSS_REFERENCE.md).

## 7. μ₀ and the division boundary `[I/C]`

`μ₀:D0↝D1` is the selected **origin aperture**: the move from the sole
object-level role `ground_0` to at least one operational distinction. It has no
saturated lower positive register. The three Titan seats describe this
boundary from the metalanguage; none is the source object of `μ₀`. Division by
zero is a useful reverse boundary witness because it shows where a field
operation stops; it neither defines nor proves `μ₀`.

**Recovery:** quotient all D1 distinctions into one class to recover
`Carrier(D0)={ground_0}`. **Kill:** remove the aperture reading if it adds no
discriminator beyond ordinary typed mathematics.

## 8. Paradox policy

Arithmetic is not advertised as "all paradoxes solved." A claimed dissolution
must identify the type error or changed domain, preserve the original problem
when no such error exists, and state what remains open. In particular:

- Zeno requires a convergence model, not `∞` as a last integer;
- Russell is a set-formation problem, not division by zero;
- Gödel incompleteness is not repaired by projective compactification;
- `0.999…=1` is equality of real limits, not a Titan identity.

*The boundary is crossed by changing the structure explicitly, never by making
an undefined field expression secretly denote a new number.*
