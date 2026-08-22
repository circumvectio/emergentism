---
title: "SLWP-01 — Burri Strong-Lift / Weak-Projection Conjecture"
id: "SLWP-01"
type: ontology-candidate
status: "PROPOSAL [C] — registered proof program; not W19, not in CLAIM_STATUS.yaml, not adopted canon"
date: 2026-08-22
proposer: "Yves R. Burri"
evidence_tier: "[B] dated proposer provenance; [A] BIL-01 only in its mathematical scope; [S] selected recovery-map requirement; [I] directional reading; [C] universal and crossing-specific emergence claims"
owner: "Ontology candidate subordinate to the Degrees-of-Freedom Ontology, the μ criterion, and the prior strong/weak lineage"
canonical_phrase: "SLWP-01 conjectures strong lift from a frozen lower description and weak recoverable projection from the higher description; BIL-01 does not prove it"
parents:
  - "02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md"
  - "07_THE_DIMENSIONAL_REGISTER_AXIOMS.md"
  - "../05_COSMOLOGY/03_FORMAL_SYSTEM/48_THE_BOUNDARY_CROSSINGS_AND_THE_MU_CRITERION.md"
  - "../00_THE_WELTANSCHAUUNG.md"
evidence_neighbor:
  - "../05_COSMOLOGY/03_FORMAL_SYSTEM/59_BOUNDARY_INFORMATION_LOSS_LEMMA_BIL_01.md"
  - "../05_COSMOLOGY/03_FORMAL_SYSTEM/58_TITAN_LIMIT_CROSSING_PROCESS_CONJECTURE.md"
  - "../03_METHODOLOGY/02_THE_PAPERS/PAPER_O_STRONG_WEAK_EMERGENCE_D5.md"
---

# SLWP-01 — Burri Strong-Lift / Weak-Projection Conjecture

> **Conjecture.** `[C]` Reality's candidate emergence crossings are asymmetric:
> from a frozen lower description, the lift into a genuinely new freedom is
> strong; from the specified higher description, projection back to the lower
> register is weak/recoverable.
>
> **Proof status.** `OPEN`. BIL-01 proves a boundary-information theorem, not
> this ontology. `PA-SLWP-01` below is therefore a **partial proof attempt with
> an explicit failed bridge**, not a proof of the conjecture.

## 1 · Provenance and the actual new move

Yves R. Burri had already stated the directional insight on 2026-07-10:

> “the ladder reads two ways at once — upward strongly emergent, downward
> weakly emergent.”

That formulation and its two named `[C]` wagers remain preserved in the
current [`Weltanschauung`](../00_THE_WELTANSCHAUUNG.md), which distinguishes
upward genesis from downward recovery or selective action without treating
either direction as proved merely by naming it.

The 2026-08-22 contribution is narrower and sharper:

1. BIL-01 proves that a boundary endpoint description can erase the
   trace information needed to reconstruct a finite invariant.
2. SLWP-01 proposes a typed lift/projection account for testing whether the
   same asymmetry holds at candidate D-level crossings.
3. `U_n` below is a forgetful/recovery map. It is **not silently identical** to
   the prior model's action-producing `χ↓`.

This records dated first-party corpus provenance. It makes no global priority,
historical-first, discovery, or ownership claim.

## 2 · The typed conjecture

For one candidate crossing, declare:

```text
L_n       := the frozen lower description at D_n
H_(n+1)   := the proposed higher description at D_(n+1)
U_n       : H_(n+1) → L_n          forgetful/recovery projection
μ_n       : L_n ⇝ H_(n+1)          candidate lift or lift relation
```

If a single selected lift exists only after an additional selector `σ_n` is
declared, write it as a section

```text
s_(n,σ) : L_n → H_(n+1).
```

The target asymmetry is:

```text
U_n ∘ s_(n,σ) = id_(L_n)                        recovery target
s_(n,σ) ∘ U_n ≠ id_(H_(n+1))  in general       upper detail is lost
```

These equations describe a section and a non-injective projection when they
hold. **They do not by themselves prove strong emergence.** A completely
reducible coarse-graining can have exactly this form.

### SLWP-01A · Strong-Lift claim `[C]`

Viewed from the frozen resources of `L_n`, a genuine `μ_n` opens effective
variation that is not formally reducible to that lower description. The
higher state cannot be uniquely reconstructed from `U_n(h)` without the extra
selector, constraint, history, relation, or law carried at the higher level.

### SLWP-01B · Weak-Projection claim `[C]`

Viewed from a specified `h∈H_(n+1)`, a declared `U_n` recovers the lower
description without creating another freedom. “Weak” here means
**recoverable/forgetful projection**. This is a corpus-specific technical use;
it is not silently equated with every literature definition of weak emergence.

### SLWP-01C · Serial-reality claim `[C]`

The conjecture's strongest form says the paired asymmetry holds independently
at each licensed `D_n⇝D_(n+1)` emergence crossing. Each leg is separately
killable. No successful leg supplies evidence for the others.

## 3 · `PA-SLWP-01` — the present proof attempt

### Input theorem `[A]`

[BIL-01](../05_COSMOLOGY/03_FORMAL_SYSTEM/59_BOUNDARY_INFORMATION_LOSS_LEMMA_BIL_01.md)
shows that the endpoint map

```text
E(trace) = (0,+∞)
```

cannot recover the limiting product: paths with the same endpoint signature
produce `0`, any finite `N`, `+∞`, or no limit.

### Proposed bridge `[I]`

Treat the endpoint pair as a lossy lower description and the full correlated
trace as the information needed for the higher reconstruction. This is a clean
model of an asymmetric question:

```text
full trace  ──forget──▶  endpoint pair
endpoint pair  ──?──▶  no unique full trace.
```

### Result

```text
PA-SLWP-01 = PARTIAL / BRIDGE NOT ESTABLISHED.
```

The attempt establishes that directional information loss is mathematically
possible and that endpoint projection can destroy reconstruction data. It does
not establish that:

- D0 is numeric zero;
- a boundary trace is a D-level lift;
- lost information is a new effective freedom;
- noninvertibility entails irreducibility;
- any physical, biological, mental, or social transition is strongly emergent;
- every higher description admits the required recovery map; or
- the same mechanism operates at all D levels.

All of the mathematics already lives in D1. PA-SLWP-01 does not establish `μ₀`.

Noninvertibility is not strong emergence. A many-to-one projection can be an
ordinary, fully reducible coarse-graining.

## 4 · The test each crossing owes

| Field | Required content |
|---|---|
| lower freeze | exact lower vocabulary, laws, state, grain, and resource bound |
| higher candidate | exact claimed new variation and its bearer |
| projection | explicit `U_n` and what it forgets |
| recovery | test of whether `U_n(h)` reproduces the declared lower behavior |
| lower rival | best formal generator/reduction using only frozen lower resources |
| novelty discriminator | observation or intervention separating higher novelty from redescription |
| prediction | one held-out difference beyond the lower rival |
| kill | event that reclassifies the leg as weak/reduced, ill-posed, or false |
| survivor | what remains useful if the strong reading dies |

The existing μ contract remains controlling: missing reduction is necessary at
most for candidacy, never sufficient for strong emergence.

## 5 · Modular claims and kills

| Claim | Tier | Kill / downgrade |
|---|---:|---|
| BIL-01 endpoint underdetermination | `[A]` | one continuous endpoint-only extension compatible with every finite path |
| BIL-01 is a useful image of projection loss | `[I]` | the analogy adds no distinction to the emergence test |
| one specified `U_n` recovers its lower description | `[S/A/B]` only after demonstration | failed recovery or an under-typed map |
| one specified lift is strongly emergent | `[C]` | formal reduction from the frozen lower description |
| all candidate D crossings obey SLWP | `[C]` | one licensed counterexample kills the universal form |
| downward projection is weak/recoverable | `[C]` per leg | no valid projection or recovery for that leg |

A many-to-one map that remains fully generated by lower laws is an explicit
rival and kills noninvertibility as evidence of strong emergence.

## 6 · Survivor if the universal conjecture dies

Even if every ontological leg fails, three things survive:

1. BIL-01 remains an ordinary-analysis theorem.
2. The distinction between lift, projection, selector, and recovery remains a
   useful research grammar.
3. The prior strong-up/weak-down model remains preserved at its own stated tier
   and with its own two wagers; this document neither thaws nor erases it.

## 7 · Adoption boundary

`SLWP-01` is a registered proposal and proof program. It is not `W19`, it is
not in `CLAIM_STATUS.yaml`, and its presence in the conjecture/proof-attempt
manifest supplies no evidence. Wager adoption belongs to
[`04_THE_CONJECTURES.md`](04_THE_CONJECTURES.md); validation routing belongs to
the claim-status owner.

The strongest honest sentence today is:

> `[A]` Boundary projection can erase the rate and correlation that determine
> a finite result. `[I]` That is a precise image of why reconstruction upward
> may require information absent from a lower description. `[C]` Whether this
> asymmetry constitutes strong emergence upward and weak projection downward
> at every D-level remains an open, modular conjecture.

## Cross-reference — the arithmetic instance and the grading (2026-08-22)

`../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/52_TITAN_SEMANTICS_V3_THE_RULE_AND_THE_WEDGE_2026_08_22.md`
§5b supplies, same day and independently: the concrete arithmetic instance
(every finite `N` runs a distinct lawful path to the SAME boundary pair
`(0, ∞)`; the pair forgets the path — the κ is the erased memory), the
emergence-grading table (resultant / weak / strong ↔ settled / serviced /
unbacked, with Bedau's simulation-derivability equal to the serviced tier),
the Batterman/Berry prior-art fence, and the hyperreal stress test (`*ℝ`
internalizes paths as members; the Titans stay outside every extension).
**Ownership of the directional conjecture stays HERE (SLWP-01).** §5b lends an
instance and a grading, never a second owner; BIL-01 remains the lemma both
lean on.
