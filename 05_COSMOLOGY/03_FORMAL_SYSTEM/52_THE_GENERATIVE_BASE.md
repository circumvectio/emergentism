---
title: "The Generative Base — one object, two operations, and the two limits no word attains"
status: "ACTIVE — candidate arithmetic/reachability base. The 2026-07-29 B-ii mixed-type ruling is superseded by the 2026-08-01 Foundation type firewall; this file defines no Titan arithmetic."
date: 2026-07-29
evidence_tier: "[A] G1–G10 in the declared rational/real structures; [S] typed boundary names; [I] any analogy to the operator-free Titan emblem"
owner: "Candidate arithmetic/reachability owner. Does not amend KSC-28, the Trinity canon, Primitive Types, doc 45, or 00_THE_FOUNDATION.md. Titan type questions route to the Trinity canon and 29_PRIMITIVES_AND_TYPE_SIGNATURES.md; no Titan identity exists here."
parents:
  - 42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md
  - 29_PRIMITIVES_AND_TYPE_SIGNATURES.md
  - ../01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md
---

# The Generative Base

> **Type correction, 2026-08-01.** The 2026-07-29 exit B-ii inserted a fourth
> mixed-type posit into `00_THE_FOUNDATION.md`. That ruling is superseded: the
> Foundation now separates its group witness from the opaque Titan frame and
> declares no coercion between them. This document owns only the arithmetic and
> reachability results below. It exports no Titan equation or identity.

> **One object. Two operations. Everything else is a word.**

Owner, 2026-07-29:

> *"In our system 0 and ∞ are not numbers and 1 is the only number, while all
> other real numbers are operations that result in something related to these
> Titans."*

> **Legacy quote — not current syntax.** It is retained as provenance for the
> question that produced this owner, not as a mapping from numbers to Titans.

> **§5.1 RULED 2026-07-31 — this sentence may no longer be published bare.** It is
> true *base-side* and false *field-side*, and the ruling requires both registers to
> travel together. `0` **is** a real number; the theorem is `0 ∉ ℝ^×`. `√2` **is** a
> number in `ℝ`, and **is not** a finite word over `{S, ι}` — that second clause is
> the `[A]` one. Base-side phrasing is *a non-halting word whose nest **denotes** a
> limit*. **The cost is accepted and it is the owner's own most quotable line: it
> stops being a headline.** Receipt: `../../11_UPLINK/50_AUDITS_AND_EXECUTIONS/193_FIVE_RULINGS_SIGNED_2026_07_31.md`.

This document is the legacy sentence's arithmetic/reachability question made
precise and checked. The earlier Foundation projection required `Ĉ` in the base
it purported to generate; that historical collision was recorded in
`11_UPLINK/50_AUDITS_AND_EXECUTIONS/181_FALSE_ATTESTATION_AND_TWO_PREEXISTING_FAILURES_2026_07_29.md`.
The current Foundation no longer has that defect: it begins with a separate
typed group witness and presents the sphere only in a selected construction.
This document remains a candidate reachability owner, not a correction the
current Foundation still awaits.

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
> The current Foundation makes the surviving split explicit: `B1` selects a
> group, `B2` selects an element, and `B3` defines its inverse; uniqueness of an
> identity is conditional on the declared group structure. This document's
> primitive `1_N` and reciprocal operation are a separate selected base, not
> something the Titan frame or a sentence forces. Under §11's self-kill (*a
> selection presented as forced*), the weaker phrasing is the one this base can
> carry.

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

**G3 · No finite word attains numeric zero.**
There is no word `w` with `val(w) = 0`.

*Proof.* `S` maps `ℚ⁺ → ℚ⁺` and `ι` maps `ℚ⁺ → ℚ⁺`; `1 ∈ ℚ⁺`; so by induction
every reachable value is strictly positive. Separately and more sharply:
`ι(x) = 0` has **no solution at all** — there is no `x` whose reciprocal is zero.
Zero is not merely un-visited. **There is no step that lands on it.** ∎

**G4 · No finite word attains an unbounded value.**
Every word is finite, so `val(w)` is a finite rational. To reach an unbounded
value one would have to *complete* infinitely many operations, and a completed
infinity of operations is not a word. ∎

**G5 · Both limits are approached.**
`val(S^n) = n+1 → ∞` and `val(S^n ι) = 1/(n+1) → 0`. Every neighbourhood of
either limit contains reachable values.

> **G3–G5 together establish a typed reachability theorem rather than a Titan
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

**G7 · The descent toward zero is the reciprocal of unbounded ascent.**
Closing under `S` alone, **no value ever falls below `1`** (verified: the minimum
of the `S`-closure is `1`). The descent toward zero exists only as
`S^n ι = 1/(n+1)` — the mirror image of the ascent.

```text
S^n      ->  2, 3, 4, …   ->  HORIZON_LIMIT
S^n ι    ->  ½, ⅓, ¼, …   ->  GROUND_LIMIT
```

Here `GROUND_LIMIT` and `HORIZON_LIMIT` are typed extended-real boundary names,
not Titan terms. The theorem says only that reciprocal sequences exchange the
two limiting directions. It does not define one Titan through another.

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


**Consequence — numeric reciprocal behavior is enacted, not a Titan relation.**
The generators produce positive rational values and reciprocal limiting
sequences. TitanFrame has no `iota`, division, limit, or reachability signature,
so none of these results forms or performs an operation on Titan roles.

*(Per §5.3 this is a statement about reachability classes only. It is **not**
doc 45's chart identity `φ·ν = 1`, and `DF-15` forbids either supporting the other.)*

---

## 3 · The three categories `[S]`

The naming is the selected part. The structure above is not.

```text
FINITE            the reachable = positive rationals = val(reduced words)
GROUND_LIMIT      the reciprocal limit; no finite word attains it
HORIZON_LIMIT     the unbounded limit; no finite word attains it
```

The selected Titan emblem `• ⊙ ○` remains a separate operator-free
interpretive frame. The three mathematical categories above are not its terms.

`1` is **the only primitive**, and it is also the unique `ι`-fixed point. Every
other value is an operation — not *constructible from* `1` but literally **a word
applied to** `1`, with a unique reduced normal form. `3/5` does not *have* a
derivation; `3/5` **is** `SιSιSι`.

**What is new here is the categorisation, not the objects.** `ℚ⁺` is standard;
continued fractions are ancient; the tree is Calkin–Wilf (2000). `KSC-12` applies:
the mathematics transfers no proof to the selected interpretation. **The reading
is: reachability may be called finity, while the two unattained limiting
directions may be compared with the ground and horizon roles.** That is an
analogy `[I]`, not an identity or a map.

### 3.1 · Type firewall — boundary markers are not Titan terms `[S]`

The earlier version called the two mathematical boundary markers
"proto-numbers" and then reused Titan glyphs for them. That move is withdrawn.
It conflated three different objects:

| Type | Terms used here | Operations |
|---|---|---|
| `Number` | positive rational values, with numeric zero mentioned only as an unattained limit | the declared arithmetic operations |
| `ProjectivePoint` | `0_P`, `infinity_P` after a separately declared compactification | the declared projective reciprocal map |
| `TitanFrame` | ground, unit, and horizon roles; displayed as `• ⊙ ○` | none; operator-free emblem only |

G3 and G4 are statements about finite words over positive rationals and their
limits. They do not refer to Titan seats and prove nothing about TitanFrame.
Compactification later creates typed projective points; it does not convert a
limit into a Titan.

The word **proto-number** is therefore retired in this owner. A Titan role is
not an incomplete number, a number-in-waiting, a projective endpoint, or an
operand. Conversely, the numeric unit, the reachable class of positive
rationals, and an equatorial projective locus are not the Titan unit role.

**Kill.** Any equation, map, operation, or proof transfer between TitanFrame and
the numeric/projective structures above kills this type firewall. A selected
analogy may be stated only as analogy and may carry no theorem in either
direction.

---

## 4 · What is emergent, and why `Ĉ` is now genuinely reached

The base above names two things it cannot exhibit. Compactification is exactly the
act of **giving those two a name as points**:

```text
                                                              tier   why
1  ℚ⁺              G1 — the reachable. COUNTABLE.             [A]    theorem
   ↓ completion     adds LIMITS of words, not words           [S]    declared move
2  ℝ₊              UNCOUNTABLE
   ↓ compactify     the two boundary limits become points     [S]    declared move

**Every arrow after the first is a declaration, not a derivation**, and each is
priced in §5. That is the specific improvement over the previous chain: the old
ladder claimed to *derive* the sphere while its bottom rung already presupposed
it. This one claims only to *reach* it, and pays for each step out loud.
3  ℝ₊ ∪ {0_P, infinity_P}
                     iota_P becomes total on the named completion
   ↓ complexify     the reflection s ↦ −s becomes a rotation   [S]    declared move
4  Ĉ = ℂP¹         iota_P is a Möbius map; the projective endpoints are its 2-cycle
```

**`Ĉ` is where the unattained limits receive typed projective representatives.**
Those representatives are not Titan roles. This is a reason to build `Ĉ`,
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
= S^∞                      → HORIZON_LIMIT   unattainable by finite words
= ι S^∞                    → GROUND_LIMIT    unattainable by finite words
finitely many ι, otherwise → a RATIONAL, already carried by a finite word
infinitely many ι          → a positive IRRATIONAL, bijectively
```

**Exactly two exceptional boundary words:** over every no-`ιι`
prefix to length 14 only `ε` and `ι` survive. Denotation is declared **only for words
with infinitely many `ι`** — there it is a bijection onto the positive irrationals.

> **The sentence the base earns:** finity is what **halts**; the irrationals are the
> words in which the inversion **never stops**; the two exceptional words name
> the limiting directions in this mathematical presentation.

**Consequence for `§4`: rung 2 is no longer an unexplained arrow.**

```text
1  HALTING        finite words                  ℚ⁺           [A]
2  NON-HALTING    infinite words, ι recurring   irrationals  [S] D-i…D-iii
3  UNATTAINABLE   S^∞ and ι S^∞                 boundary limits  [A] no value in ℝ₊
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

**5.3 · The former third reading is withdrawn.** Earlier editions reused the
Titan triple for chart, set-theoretic, and reachability structures, then called
them one datum in three notations. They are not one datum: each structure has
its own terms and operations. This document owns only reachability. Doc 45 owns
its typed projective/chart facts, and the Trinity canon owns the operator-free
Titan frame. No agreement, identity, coercion, or proof transfer is asserted.

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

**This document's own kill.** If Titan glyphs are used here as names for
reachability classes, points, operands, limits, or warrants, this base has
crossed its type boundary and must be repaired or withdrawn rather than
defended.

---

## 7 · The stranger test

A stranger needs no metaphysics to check this page. Hand them `22/7` and the two
operations; they will find `SSSSSSιSSS` with a pencil, and they will find it is
the only reduced word that works. `G3` they can check in one line: nothing's
reciprocal is zero.

**Reproduce:** `09_TOOLS/01_SCRIPTS/check_generative_base.py` — exhaustive over all
words to length 10, the Calkin–Wilf tree to depth 12, and reachability of every
`p/q` with `p, q ≤ 25`. It exits non-zero on any failure.

• ⊙ ○ — *selected operator-free emblem. The arithmetic base itself has one
numeric object, two operations, and two limiting directions that no finite word
attains.*
