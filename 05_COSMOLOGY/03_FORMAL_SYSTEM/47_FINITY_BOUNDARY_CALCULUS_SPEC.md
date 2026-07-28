---
title: "Finity Boundary Calculus — Formal Research Specification"
status: "ACTIVE SPECIFICATION — F0 syntax packet complete; novelty and world claims evidence-open"
date: 2026-07-28
evidence_tier: "[A] inherited mathematics; [S] declared type system; [I] Finity reading; [C] any new-calculus claim"
owner_route: "K-1 with K-3/K-4 recovery and kill review"
adequacy_docket: A1
---

# Finity Boundary Calculus

Finity is specified here as a **conservative boundary-and-extension protocol**.
Its first job is not to add a magical value between zero and infinity. Its job
is to make every boundary claim declare a domain, type, obstruction,
extension, recovery map, rival, novelty burden and failure condition.

The packet is F0: its syntax and acceptance obligations are defined. It has not
yet earned F1 mathematical novelty. If every useful result translates into
known partial algebra, projective geometry, topology, analysis or type theory,
the survivor is a useful specification layer—not a new foundational algebra.

## 1. Sorts

```text
TitanFrame       ::= zero_T | one_T | unbounded_T
NarrativeMode    ::= TheInfinite_R | Finity_R | Infinity_R
Glyph
EvalStatus       ::= value | undefined | indeterminate_form
                   | diverges | extended_value

NatPos | Int | Rat | Real | Complex | Field[F]
ProjectivePoint[P1(F)] | ExtendedReal
MetricSpace[X] | TopologicalSpace[X] | Point[X]
Sequence[X] | Net[X] | Filter[X] | LimitContext[X]

PartialOperation[A,B]
Extension[Base,Extended]
Embedding[Base,Extended]
RecoveryMap[Extended,Base]
BoundaryWitness
BoundaryDiagnosis
MuCrossing
```

`TitanFrame` receives equality and rendering only:

```text
render_T : TitanFrame → Glyph
TitanFrame ↛ Number
TitanFrame ↛ Field[F]
TitanFrame ↛ ProjectivePoint[P1(F)]
```

Similar display glyphs never create an implicit coercion. `zero_T`, the
integer `0_N`, the additive identity `0_F`, and a projective coordinate are
different terms until an explicit map is declared.

## 2. Judgments and syntax

```text
Γ ⊢ e : S                 e has sort S
Γ ⊢ e ⇓ v : S             e evaluates ordinarily
Γ ⊢ e ⇑ status            e receives a boundary diagnosis
Γ ⊢ Base ↪ Extended       an extension and embedding are declared
Γ ⊢ Extended ↠ Base       a recovery map is declared
Γ ⊢ μ : MuCrossing        μ is an evidence record, not a value
```

Formal mode uses typed boundary glyphs where ambiguity matters:

```text
zero_T   0_N   0_F   infinity_P   infinity_ER
```

For a field `F`, division is partial:

```text
div_F : F × NonZero[F] → F
```

An input `a/0_F` enters the diagnostic grammar because it is outside the
operation's domain. It does not acquire a field value by renaming the error.

## 3. Evaluation distinctions

The calculus must keep five cases separate:

1. **ill-typed** — terms from incompatible sorts were combined;
2. **undefined** — a well-typed input lies outside a partial operation's domain;
3. **indeterminate form** — a limit expression does not determine its limit
   without further information;
4. **divergent** — the declared limiting process does not converge in the named
   target space; and
5. **extended value** — a value exists only after a named change of carrier and
   operations.

Consequently `[A]`:

- field division by zero remains undefined;
- `0/0` is not a field value and may be an indeterminate form only inside a
  declared limit context;
- projective reciprocal is a map on `P¹(F)`, not retroactive field division;
- convergence requires a named topology or metric, trajectory and target; and
- cardinal, ordinal, projective and extended-real infinities are not silently
  interchangeable.

## 4. Finity protocol `[S/I]`

```text
FinityProtocol(boundary) :=
    declared type
  + base domain
  + named obstruction
  + smallest explicit extension
  + conservative recovery
  + serious rival
  + novelty test
  + kill criterion
```

The selected philosophical reading `[I]` is that finity concerns a bounded,
inspectable approach to a declared limit. That reading supplies no new theorem
until a formal result exceeds its translation into established mathematics.

## 5. Standard-mathematics translation `[A/S]`

| W3 construct | Conservative translation |
|---|---|
| `TitanFrame` | inductive datatype with no numeric instances |
| field fragment | ordinary many-sorted algebra or a theorem-prover field library |
| partial division | a nonzero-denominator subtype or explicit error result |
| `P¹(F)` | standard projective line |
| `ExtendedReal` | explicit extended-real construction |
| convergence | metric epsilon definition or topological filter/net definition |
| `EvalStatus` | diagnostic algebraic datatype |
| `MuCrossing` | typed evidence and provenance record |

The first formal obligation is conservativity:

```text
For every base-language term e in its native domain:
  Eval_Finity(e) = Eval_standard(e).

For every base theorem T:
  the Finity layer obtains no contrary theorem unless an explicitly named
  extension changes the carrier, operation or axioms.
```

## 6. Smallest-extension test `[S]`

For a boundary witness `b` in base theory `B`, a candidate extension `E` is
admissible only if:

1. `i : B ↪ E` is explicit;
2. base theorems are preserved under `i`;
3. `E` interprets the named witness rather than a rhetorical neighborhood;
4. every new sort, axiom and operation is enumerated;
5. a declared smaller rival extension cannot perform the same task; and
6. recovery or ablation identifies what disappears on return to `B`.

“Smallest” is relative to a declared ordering—such as fewer new sorts,
operations, axioms or altered domains. It is not metaphysical minimality.

## 7. Recovery obligations

Every extension must pass:

- **R0 Type integrity:** Titan arithmetic and silent coercions fail to parse.
- **R1 Native recovery:** accepted arithmetic, analysis, geometry and type
  theory keep their native results.
- **R2 Extension transparency:** base, carrier, embedding, changed operations
  and costs are listed.
- **R3 Boundary specificity:** the exact obstruction is named.
- **R4 Limit specificity:** space, topology or metric, path, target and failure
  condition are declared.
- **R5 μ recovery:** every crossing record names lower-register recovery, rival,
  prediction, discriminator and kill.
- **R6 Novelty separation:** known re-expression and candidate new theorem or
  tool are different statuses.
- **R7 Independent review:** a reviewer outside the authoring process can run
  the same translation and countermodel suite.

## 8. μ boundary

`MuCrossing` is a record with fields:

```text
system_boundary, saturation_measure, threshold, candidate_new_freedom,
lower_register_recovery, rival_models, preregistered_prediction,
discriminator, kill_criterion, custody
```

It is never a number or causal operator. No joint score, force analogy or
successful neighboring row promotes another crossing.

## 9. Stop conditions

The program fails or narrows when:

- the parser permits Titan arithmetic or silent extension;
- the standard fragment changes ordinary results;
- “resolution” lacks a scoped row in the paradox ledger;
- the alleged extension is larger than a named sufficient rival;
- every output is known theory and no theorem, invariant, classification,
  no-go result or tool exceeds cited prior art;
- a μ packet lacks recovery, rival, discriminator or kill; or
- independent formal review cannot reproduce the result.

No failure destroys the useful type boundary. It changes the scope and name of
what survived.
