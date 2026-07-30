---
title: "The Generative Base — one object, two operations, and the two limits no word attains"
status: "ACTIVE — candidate base. Stands beside 00_THE_FOUNDATION.md §2; supersedes nothing until the owner rules G-0."
date: 2026-07-29
evidence_tier: "[A] G1–G8, computationally verified and mutation-tested and reproducible; [S] the naming of the three categories; [I] the Titan reading"
owner: "Candidate. Does not amend KSC-28, doc 45, or 00_THE_FOUNDATION.md. Owner ruling G-0 pending."
parents:
  - ../../00_THE_FOUNDATION.md
  - 42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md
  - ../01_THE_TRANSCENDENTAL_TRINITY/45_THE_TITAN_INVERSION_STRUCTURE.md
---

# The Generative Base

> **One object. Two operations. Everything else is a word.**

Owner, 2026-07-29:

> *"In our system 0 and ∞ are not numbers and 1 is the only number, while all
> other real numbers are operations that result in something related to these
> Titans."*

This document is that sentence, made precise and checked. It needs no sphere to
state, which is why it exists: the base in `00_THE_FOUNDATION.md` §2 cannot be
read without `Ĉ` already present (the collision, `G-0`; recorded in
`11_UPLINK/50_AUDITS_AND_EXECUTIONS/181_FALSE_ATTESTATION_AND_TWO_PREEXISTING_FAILURES_2026_07_29.md`
and `185_SECTION_5_2_RULED_AND_F_EQUALS_MA_2026_07_30.md`). **This one can.**

> **Citation repair, 2026-07-30.** This line previously read *"the collision,
> r180 / G-0"*. **There is no receipt `r180`.** The number was announced in a
> session summary and never written; the only `180_` file in the corpus is
> `11_UPLINK/60_SESSION_PACKETS/180_DEEP_SADHU_CUT_L7_AND_INVARIANT_RESOLUTION_2026_04_25.md`,
> an unrelated April document. A dangling-citation check *passed* the bad
> reference, because the number resolved — to the wrong file. That is the live
> hazard: 40 receipt files in `50_AUDITS_AND_EXECUTIONS` share a number with
> another document and declare no supersession, so a numeric citation can
> resolve and still be false. Cite receipts by **path**, not by number.

---

## 1 · The base `[S]`

```text
PRIMITIVE      1
OPERATIONS     S(x) = x + 1          the successor
               ι(x) = 1 / x          the inversion
```

That is the whole posit. Two operations and one object. `ι` is **not** imported
here as a symmetry discovered later — it is **constitutive**, one of the two
things the base grants.

**And the primitive's UNIQUENESS is not a free choice `[A]`.** `ι(x) = x` has
exactly one solution on `ℚ⁺`, and it is `1`. There is no second candidate.
*(Machine-checked as `unique_positive_fixed_point`,
`09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean`.)*

> **CORRECTED 2026-07-30, and it is the `F2` error a second time.** This passage
> read: *"You do not choose `1` — you choose `ι`, and `1` arrives as the only thing
> it holds still."* **That is circular.** `ι(x) = 1/x` cannot be written without
> naming `1`; and `x⁻¹` means *the `y` with `xy = e`*, which names the identity
> directly. **`ι` presupposes the unit it was said to force.**
>
> What survives is exactly the split that killed `F2`:
>
> ```text
> EXISTENCE of the unit    presupposed. It is in P1 and in ι's own definition.
> UNIQUENESS of the unit   THEOREM. ι could have had two positive fixed points
>                          and does not.
> ```
>
> `00_THE_FOUNDATION.md:47-49` already states only the surviving half — *"its
> **uniqueness** is the one thing here that nobody chose."* The projection was
> right and this document overclaimed. Under §11's self-kill (*a selection
> presented as forced*), the weaker phrasing is the one the base can carry.

A **word** is a finite string over `{S, ι}`. Its **value** is the result of
applying its letters left to right to `1`. Write `val(w)`.

```text
val(ε)        = 1
val(S)        = 2
val(Sι)       = 1/2
val(SSSSSSιSSS) = 22/7
```

---

## 2 · Five theorems `[A]`

**G1 · Reachability is exactly `ℚ⁺`.**
For every `q ∈ ℚ⁺` there is a finite word `w` with `val(w) = q`; and every word's
value lies in `ℚ⁺`.

*Proof.* (⊇) Induct on `num(q) + den(q)`. If `q = 1`, take `ε`. If `q > 1` then
`q − 1 ∈ ℚ⁺` with strictly smaller sum, and `q = S(q−1)`. If `q < 1` then
`1/q > 1` with the same sum, and one `ι` step reduces to the previous case. The
measure strictly decreases, so the recursion terminates — this **is** the
Euclidean algorithm. (⊆) `S` and `ι` both map `ℚ⁺` into `ℚ⁺`. ∎

**G2 · Reduced words are unique normal forms.**
Call `w` **reduced** if it contains no `ιι` and does not begin with `ι`. Then the
map `w ↦ val(w)` is a **bijection** from reduced words onto `ℚ⁺`.

The two exclusions are not conventions. They are precisely the two facts that
define `ι`:

```text
ιι = id        ι is an involution
ι(1) = 1       1 is ι's fixed point   (hence a leading ι is the empty word)
```

So `G2` says: **the word monoid modulo `ι`'s own identity has unique normal
forms, and they are the positive rationals.**

*Verified by exhaustion* over all `2^11 − 1` words of length ≤ 10: 143 of 232
values carry multiple *unreduced* words; **0 of them carry multiple reduced
words.** Equivalently, in the Calkin–Wilf presentation `{S, L}` with
`L = ιSι : x ↦ x/(x+1)`, all `8191` words of length ≤ 12 have `8191` **distinct**
values — a perfect binary tree.

**G3 · No word attains `•`.**
There is no word `w` with `val(w) = 0`.

*Proof.* `S` maps `ℚ⁺ → ℚ⁺` and `ι` maps `ℚ⁺ → ℚ⁺`; `1 ∈ ℚ⁺`; so by induction
every reachable value is strictly positive. Separately and more sharply:
`ι(x) = 0` has **no solution at all** — there is no `x` whose reciprocal is zero.
Zero is not merely un-visited. **There is no step that lands on it.** ∎

**G4 · No word attains `○`.**
Every word is finite, so `val(w)` is a finite rational. To reach an unbounded
value one would have to *complete* infinitely many operations, and a completed
infinity of operations is not a word. ∎

**G5 · Both limits are approached.**
`val(S^n) = n+1 → ∞` and `val(S^n ι) = 1/(n+1) → 0`. Every neighbourhood of
either limit contains reachable values.

> **G3–G5 together are the corpus's oldest sentence, now a theorem rather than a
> description:** *the limit is approached and never reached.* The reason is
> **finiteness of words**, not slowness and not stipulation. You approach because
> one more operation is always available. You never arrive because there is no
> last one.

---

## 2A · What each operation contributes — the asymmetry `[A]`

The two operations are not two of a kind. Verified by exhaustive closure.

**G6 · `ι` alone is sterile; `S` alone is one-directional.**

```text
from 1, closing under  ι  alone   ->  {1}           NOTHING.  ι(1)=1, and ιι=id.
from 1, closing under  S  alone   ->  ℕ⁺            one direction only, no fractions
from 1, closing under  S and ι    ->  ℚ⁺            all of finity
```

Inversion generates **nothing at all** by itself. Succession generates a ray.
Only together do they give finity.

**G7 · `•` is a direction only because `ι` reflects `○`.**
Closing under `S` alone, **no value ever falls below `1`** (verified: the minimum
of the `S`-closure is `1`). The descent toward zero exists only as
`S^n ι = 1/(n+1)` — the mirror image of the ascent.

```text
S^n      ->  2, 3, 4, …   ->  ○      succession reaches toward totality
S^n ι    ->  ½, ⅓, ¼, …   ->  •      inversion turns that reach around
```

> **Absence is not a second posit standing beside totality. It is totality seen
> through the inversion.** The base never declares two horizons; it declares one
> reach and one reflection, and the second horizon is what the reflection makes.

**G8a · `ι` is an involution with a unique fixed point `[A]` — and this half lives
on the base.** `ι(ι(x)) = x` for every reachable `x`, and `1` is the only reachable
value with `ι(x) = x`. Verified over the reachable set **using rationals only — no
real number enters the check.**

**G8b · Under `s = log x`, `ι` is the reflection `s ↦ −s` — `[A] given ℝ`.**
True, and it is what makes "1 is the centre" geometric rather than merely
fixed-point. But it is **not a statement about the base's objects**, and the
reason is sharp:

> **`log q` is TRANSCENDENTAL for every `q ∈ ℚ⁺` with `q ≠ 1`.**
> *Proof.* Suppose `log q = a` were algebraic. `a ≠ 0`, since `q ≠ 1`. By
> Hermite–Lindemann `e^a` is then transcendental, so `q = e^a` is transcendental —
> but `q ∈ ℚ` is algebraic. Contradiction. ∎

So `log(reachable) = {0} ∪ transcendentals`. **The log coordinate sees exactly one
point of finity — the centre — and sends every other reachable value clean outside
`ℚ`.** `G8b` therefore carries **completion to `ℝ` as a premise**, and belongs in
the premise ledger, not in the base.

> **CORRECTION, 2026-07-29, self-caught.** `G8` was first published here as one
> claim at `[A]`, stating the log form as though it held of the base's own objects.
> It does not. The split above is the repair. The load-bearing half — finity is
> symmetric about its centre, and **the symmetry is the operation that generates
> it** — is `G8a` and survives untouched.


**G9 · The determinant invariant — what the base can and cannot generate `[A]`.**
As Möbius maps the generators are matrices in `PGL(2,ℚ)`:

```text
S = [[1,1],[0,1]]   det +1        ι = [[0,1],[1,0]]   det −1
```

so **every word has determinant `±1`.** A scalar `λ` scales a determinant by `λ²`,
so a primitive matrix `M` with `det M = d` is a word only if `dλ² = ±1` has a
rational solution.

**Consequence — Suda's hinge is not a word.** `u = (x−1)/(x+1)` is
`[[1,−1],[1,1]]`, primitive, with `det u = 2`; and `2λ² = ±1` has no rational
solution. *Verified by exhaustion:* of the `6763` distinct projective words of
length ≤ 16, `u` is in **none**.

> **`ρ`, `E` and `u` all fail to live on the base, but for two different reasons.**
> `ρ` and `E` escape through **transcendence** (G8b). `u` escapes through an
> **algebraic invariant** — it is the wrong determinant. The hinge is *imported*,
> not generated, and `42:395` currently tiers it `[A]` without recording that.

**What the base does own in its place:** `L(x) = x/(x+1) = [[1,0],[1,1]]` has
determinant `1` and **is** a word. It is the Calkin–Wilf second generator, already
used in `G2`'s cross-check. So the base has a native companion coordinate — it is
simply not Suda's.

**G10 · The determinant is not the only obstruction — sign is independent `[A]`.**
`G9` is necessary, not sufficient, and the two invariants come apart in all four
combinations. Verified:

```text
map              det   passes G9   stays in ℚ⁺   a word?
S    x+1          +1      yes          yes         YES
ι    1/x          −1      yes          yes         YES
n    −x           −1      yes          NO          no  <- G9 does NOT catch it
n∘ι  −1/x         +1      yes          NO          no  <- G9 does NOT catch it
D    2x           +2      NO           yes         no  <- caught by det alone
u    (x−1)/(x+1)  +2      NO           NO          no  <- over-determined
```

`n∘ι : x ↦ −1/x` (`42:374`) is the decisive witness: **determinant `+1`, passes
`G9`, and is still not a word** — because `G1` commits every word's value to `ℚ⁺`
and `n∘ι(1) = −1 ∉ ℚ⁺`. Both halves of that refutation are already committed text.

> **THEREFORE `G9` DOES NOT CLOSE THE `§5.2` FORK.** The sign obstruction is
> independent of the determinant obstruction, and the `−1` question is untouched
> by anything proved here. **It remains an open owner ruling.**

> **CORRECTION, 2026-07-29.** This session stated that "the hinge's determinant
> *is* the fork — you don't get one without the other." That is false, and the
> error mattered: it would have made `G9` appear to settle `§5.2` for free, which
> is a selection presented as forced — the move `00_THE_FOUNDATION.md` §11 fires
> on. `u` is **over-determined**: wrong determinant, *and* it leaves `ℚ⁺`, *and*
> `u(1) = 0` kills it by `G3` with no matrix theory at all.

*(Not claimed: that non-negative entries plus `det ±1` jointly CHARACTERISE the
words. That is a stronger, unverified conjecture and is not asserted here.)*


> **CORRECTION, 2026-07-29.** Before the experiment returned, this session
> predicted the hinge would score `DERIVED` at zero premises because `u` maps `ℚ⁺`
> into `ℚ ∩ (−1,1)` using no reals. **Staying inside `ℚ` is necessary and not
> sufficient**; the determinant is **an** obstruction — and, per G10 below, **not the
> one that keeps the base positive.** The prediction was refuted.


**Consequence — two of the three Titan relations are enacted, not posited.**
`• = ⊙/○` and `○ = ⊙/•` say the horizons are each other's `ι`-images. Here that
is not an assertion the base makes; it is **what it means for `ι` to be one of the
two generators.** The base does not claim the relation. It performs it.

*(Per §5.3 this is a statement about reachability classes only. It is **not**
doc 45's chart identity `φ·ν = 1`, and `DF-15` forbids either supporting the other.)*

---

## 3 · The three categories `[S]`

The naming is the selected part. The structure above is not.

```text
⊙   FINITY      the reachable                 = ℚ⁺ = val(reduced words)
•   ABSENCE     the ι-limit; no word attains it
○   TOTALITY    the S-limit; no word attains it
```

`1` is **the only primitive**, and it is also the unique `ι`-fixed point. Every
other value is an operation — not *constructible from* `1` but literally **a word
applied to** `1`, with a unique reduced normal form. `3/5` does not *have* a
derivation; `3/5` **is** `SιSιSι`.

**What is new here is the categorisation, not the objects.** `ℚ⁺` is standard;
continued fractions are ancient; the tree is Calkin–Wilf (2000). `KSC-12` applies:
the mathematics transfers no proof to the reading. **The reading is: reachability
is finity, and the Titans are what unreachability looks like from inside.** That
sentence has no counterpart in the literature and is the claim this document makes.

### 3.1 · What to call the seats — **proto-number** `[S]`

§3 names three categories. Two of them are single **seats**: `•` and `○`. The
corpus says repeatedly what those seats are **not** — not numbers (`53` §1), not
operands (`45:83-85`), not terms (`42:237-245`) — and never once what they **are**.
A category defined only by negation gets refilled by the reader with the nearest
positive: *very small* and *very large*. This supplies the noun instead.

> **proto-number** *n.* A seat a number system must **name** in order to state its
> own boundary, and can never take as an **operand**.
> `ArithmeticSignature(proto-number) = ∅` (`KSC-04`; `29:66-69`). Neither a number
> nor nothing — the third thing.

Both halves of the test must hold:

| | Test | Verified by |
|---|---|---|
| **nameable** | the system's own statements refer to it | `G3` — *`ι(x)=0` has no solution* is a sentence about `•`; `G4` — *every word is finite* is a sentence about `○` |
| **non-operand** | no operation accepts it | `KSC-04`: no `add`, `sub`, `mul`, `div`, `pow`, `log` — and no implicit coercion |

**Why not nothing.** `G5`: every neighbourhood of either seat contains reachable
values — `val(S^n ι) → 0`, `val(S^n) → ∞`. Nothing has no neighbourhood crowded
with somethings. The seat is approached from every side; only the arrival is missing.

**Why not a number.** `G3`, `G4`: no word attains either, and the failure is not
scarcity — `ι(x) = 0` has **no solution at all**. Not un-visited: unlandable.

**This is doc 42's third category from the other side.** `42:237-245` classifies the
**expression** — `0_T × ∞_T` is an *inadmissible term*, not "no such element" and
not "indeterminate form", but *not a term*. `proto-number` classifies the **seat**.
One fact, two faces: the seat is a proto-number exactly because every expression
putting it in an operator slot is an inadmissible term. `DF-15` binds — that is one
datum in two notations, not two witnesses.

#### The two fences the prefix requires `[S]`

**F-1 · "proto-" is not priority — not temporal, not constructional, not
generative.** `00_THE_FOUNDATION.md:377-382` rules the other direction: two poles do
not generate a middle, and the construction runs `ℝ₊ ──compactify──▶ adjoin {0,∞}` —
**`⊙` is not the child of `•` and `○`; `•` and `○` are the boundary of `⊙`.**
`KSC-28` lists *"the interior is said to be produced by the poles"* as a kill. On
this base the seats are **posterior**: `G3` and `G4` name them as the base's two
failures to arrive, so the base can name them only once it has a word to fail with.
`G7` denies them even parity with each other — `•` is `○` reflected, not a second
posit.

> `proto-` marks **incompleteness of numberhood**, never precedence. A proto-number
> is not a number-in-waiting: nothing promotes it, and it never becomes one. If the
> prefix is ever read as priority, this section has been turned against `KSC-28` —
> withdraw the term rather than defend it.

**F-2 · The seats are proto-numbers; `⊙` read as *finity* is not.** The glyph carries
three referents and only one of them is a seat:

| `⊙` read as | Object | Operands? | proto-number? |
|---|---|---|---|
| `1_T` / `Unit_T` (`KSC-04`; `29:28`) | a `TitanFrame` term, one chart up from this base; `1_T ≠ 1_N` | none | **yes** |
| FINITY `= ℚ⁺` (§3 above; `53` §1) | the reachable class | **every member is a lawful operand** | no |
| the equator `\|z\| = 1` (`45:53`) | a circle of points of `Ĉ` | operands on the affine chart | no |

`45:201-202` gives the internal resolution: *`⊙`'s dot is the unit `1`, and `⊙`'s
circle is the boundary.* So the **circle** is where the seats sit — the rim
`45:187-190` shows is not in the image of `ℝ₊` — while the **dot** is this base's
primitive `1`, which is a number and the operand every word is applied to. *"`⊙`
finity is a proto-number"* is therefore true of the seat and **false of finity**,
which is nothing but numbers. `DF-15` again: three readings, one datum. **The
definition pins to the type, never to the glyph.**

**Kill.** Exhibit an operation of this base accepting `•`, `○` or `1_T` as an
argument; or state `G3`/`G4` without referring to the seat they deny. Either kills
the category. Separately and independently: if `proto-` is ever used to license the
seats as prior to, productive of, or convertible into numbers, `F-1` has been
dropped.

---

## 4 · What is emergent, and why `Ĉ` is now genuinely reached

The base above names two things it cannot exhibit. Compactification is exactly the
act of **giving those two a name as points**:

```text
                                                              tier   why
1  ℚ⁺              G1 — the reachable. COUNTABLE.             [A]    theorem
   ↓ completion     adds LIMITS of words, not words           [S]    declared move
2  ℝ₊              UNCOUNTABLE
   ↓ compactify     the two horizons become points            [S]    declared move

**Every arrow after the first is a declaration, not a derivation**, and each is
priced in §5. That is the specific improvement over the previous chain: the old
ladder claimed to *derive* the sphere while its bottom rung already presupposed
it. This one claims only to *reach* it, and pays for each step out loud.
3  ℝ₊ ∪ {•, ○}     ι becomes total:  ι(•) = ○,  ι(○) = •
   ↓ complexify     the reflection s ↦ −s becomes a rotation   [S]    declared move
4  Ĉ = ℂP¹         ι is a Möbius map; the poles are its 2-cycle
```

**`Ĉ` is where the unattainable becomes nameable.** That is a reason to build it,
not merely a place to start from — which is what edition 2 wanted and could not
get, because its base could not be read without the sphere it was supposed to
produce.

---

## 5 · Three gaps, stated because they are load-bearing `[S]`

**5.1 · The third mode — the irrationals are the words that never stop inverting.**
`[A]` classification · `[S]` its three declarations · `[I]` the naming. An irrational
is not a limit from outside; it is **a word in the same two operations that never
halts**:

```text
√2 = [1;2,2,2,…]     = S ι SS ι SS ι SS …
φ  = [1;1,1,…]       = S ι S ι S ι …
e  = [2;1,2,1,1,4,…] = SS ι S ι SS ι S ι S ι SSSS …
```

**The base's own `val` cannot read them, and this must be said first.** `52:65-66`
defines a word's value as its letters applied **left to right**. On an infinite word
that is a **dynamical orbit**, and it does not converge. `SιSιSι…` gives:

```text
2, ½, 3/2, ⅔, 5/3, ⅗, 8/5, ⅝, 13/8, 8/13, …
```

two accumulation points, `φ` and `1/φ`, consecutive terms a unit apart forever.
Verified: a period-`k` word gives **exactly `k`** such points, the value and its
`S`-shifts. The orbit *holds* the number and never *picks* it; on a non-periodic word
(`e`) it is unbounded.

The continued fraction builds the **other way** — leftmost letter applied last, each
new letter innermost:

```text
val_L(w) = lₙ(…l₁(1))   an ORBIT.   does not converge
val_R(w) = l₁(…lₙ(1))   a NEST.     converges (Seidel–Stern)
```

On **finite** words the readings are conjugate by reversal —
`val_R(w) = val_L(w̄)`, zero mismatches over all `8191` words of length ≤ 12 — so
**`G1` is direction-blind**; both reach exactly `ℚ⁺`. **`G2` is not**: its normal form
mirrors from *no leading `ι`* to *no trailing `ι`*.

**What must be declared `[S]`.**

```text
D-i    infinite words are admitted           G3/G4 must now say FINITE word
D-ii   they are read as a NEST, not an orbit  a convention, not a theorem
D-iii  a convergent nest DENOTES its limit    <- this is still the completion
```

**`D-iii` does not remove the completion, and nothing here claims it does.** `ℝ` is
still required; what changes is that the added values stop being anonymous — each
irrational arrives with **one canonical Cauchy sequence**, bound
`|x−pₙ/qₙ| < 1/qₙqₙ₊₁`. Cheaper in *explanation*, not *strength*; reading it as
strength-reduction is the move `§11` fires on.

**The classification, exhaustively checked** — infinite words with no `ιι`:

```text
= S^∞                      → ○   unattainable
= ι S^∞                    → •   unattainable
finitely many ι, otherwise → a RATIONAL, already carried by a finite word
infinitely many ι          → a positive IRRATIONAL, bijectively
```

**Exactly two exceptional words, and they are the two Titans:** over every no-`ιι`
prefix to length 14 only `ε` and `ι` survive. Denotation is declared **only for words
with infinitely many `ι`** — there it is a bijection onto the positive irrationals.

> **The sentence the base earns:** finity is what **halts**; the irrationals are the
> words in which the inversion **never stops**; the Titans are the two in which it
> **stops forever**.

**Consequence for `§4`: rung 2 is no longer an unexplained arrow.**

```text
1  HALTING        finite words                  ℚ⁺           [A]
2  NON-HALTING    infinite words, ι recurring   irrationals  [S] D-i…D-iii
3  UNATTAINABLE   S^∞ and ι S^∞                 ○ and •      [A] no limit in ℝ₊
```

`ℝ₊` is `mode 1 ⊔ mode 2` exactly, nothing left over.

**Fences.**
1. **Process, not program.** Only *countably many* infinite words are outputs of a
   finite program. The naming is total because a word is a **process**; read
   "operation" algorithmically and it scopes to the computable reals — the completion
   returns for the rest.
2. **The seed drops out.** For infinite words the limit is seed-independent (checked at
   `1, 2, 7, 1000, 1/1000`): *"`3/5` **is** `SιSιSι` applied to `1`"* has an exact
   analogue for `√2`, minus *applied to `1`*. **The unit is what halting needs.**
3. `KSC-12`. Simple continued fractions are Euler's; `⟨S,ι⟩` generating the modular
   group is textbook. **No theorem below transfers to the reading.** *(Whether the
   halting wall is a `μ` is NOT claimed — doc 48's seam is open.)*

**Kill.** Exhibit an infinite word whose **left-to-right** prefixes converge to an
irrational, for a class rich enough to name them all; that retires `D-ii`. Or a
positive irrational carried by two distinct no-`ιι` words with infinitely many `ι`, or
by none. Or a third no-`ιι` word whose nest limits to `0` or `∞`. Or, against the
reading: show *"the irrationals are the non-halting words"* adds nothing to *"the
irrationals are the infinite simple continued fractions."*

**5.2 · `−1` costs zero.** `S` and `ι` never leave `ℚ⁺`. `KSC-21`'s oriented pair
`{+1, −1}` therefore needs a third operation. If that operation is additive
inverse, then `1 + (−1) = 0` and **zero becomes reachable**, which forfeits `G3`
and with it "0 is not a number." The fork is exact and unavoidable:

```text
positive-only, no zero, no −1        G3 holds, KSC-21 unsupported
signed, with −1                      KSC-21 holds, G3 falls
```

> **RULED 2026-07-30 — POSITIVE-ONLY.** The base stays `⟨S, ι⟩` on `ℚ⁺`. `G1`–`G10`
> stand exactly as written; `G3` holds and *"0 is not a number"* survives; the
> unit's uniqueness stays forced.
>
> **The cost, accepted and recorded here rather than absorbed:** `KSC-21`'s oriented
> pair `{+1, −1}` is **NOT supported by this base**. Nothing in `⟨S, ι⟩` reaches
> `−1`, and no argument in this document should be read as reaching it. **D1 is
> seated one chart up, by a declared move** — the same kind of declared move as
> completion and compactification in §4, and priced the same way.
>
> This is not a claim that `−1` does not exist. It is a claim about what this base
> generates. `ι` considered as a map on `ℝ` fixes exactly `±1`
> (`inversion_fixed_iff`, machine-checked); the base's words reach only one of the
> two. **That asymmetry is now a stated property of the base, not an open question.**
>
> **Kill:** exhibit a finite word over `{S, ι}` whose value is negative — or show
> that D1 can be seated without any declared move beyond the base.

**5.3 · This is a third reading of `{•, ⊙, ○}`.** Doc 45 reads the triple as the
coupled-chart identity on `Ĉ`; doc 46 reads it set-theoretically (`∅`, sets,
proper classes); this document reads it as reachability. **`DF-15` binds: these
are one datum in three notations. None may be cited as support for another, and
their agreement is not evidence.**

---

## 6 · Kills

| Claim | Kill |
|---|---|
| `G1` | exhibit `q ∈ ℚ⁺` reachable by no finite word, or a word whose value is irrational |
| `G2` | exhibit two distinct reduced words with the same value |
| `G3` | exhibit a word with value `0` |
| `G4` | exhibit a word with unbounded value |
| `G5` | exhibit a neighbourhood of `0` or `∞` containing no reachable value |
| the base | show the corpus needs a value that no finite word attains **and** that is not obtained by a declared completion |
| the reading | show "reachability = finity" is a notational variant of an existing account, not a distinct claim |

**This document's own kill.** If `⊙`, `•`, `○` are used here as anything other
than *names for reachability classes* — if they are read back as points, operands,
or a warrant — this base has been fused with doc 45's and should be repaired or
withdrawn rather than defended.

---

## 7 · The stranger test

A stranger needs no metaphysics to check this page. Hand them `22/7` and the two
operations; they will find `SSSSSSιSSS` with a pencil, and they will find it is
the only reduced word that works. `G3` they can check in one line: nothing's
reciprocal is zero.

**Reproduce:** `09_TOOLS/01_SCRIPTS/check_generative_base.py` — exhaustive over all
words to length 10, the Calkin–Wilf tree to depth 12, and reachability of every
`p/q` with `p, q ≤ 25`. It exits non-zero on any failure.

•   ⊙   ○ — *one object, two moves, and two horizons that recede at exactly the speed you walk.*
