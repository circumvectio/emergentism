---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Philosophy
      role: "audit surface for formula tracking across corpus"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A/I/C]"
  canonical_phrase: "Canonical Formula Block"
---

# The Canonical Formula Block

**Status:** Active
**Evidence tier:** `[A]` for the stated chart identities; `[I]` for their
Emergentist interpretation; `[C]` for universal fit to real systems
**Depends on:** `01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md`, `03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md`
**Purpose:** The shortest verbatim block that states the framework's load-bearing sequence without hierarchy drift

---

## Verbatim Analytic Block

```text
Zero-Sum Resolution Equation
θ ∈ (0, π)
φ := cot(θ/2),  ν := tan(θ/2)
φ · ν = 1
(φ − ν)² ≥ 0
φ + ν ≥ 2
B := 2/(φ + ν) = sin θ ≤ 1
```

## Meaning

- The first three lines define one open positive-radial meridian of a
  stereographic chart and its reciprocal. They do not include the azimuth and
  therefore are not, by themselves, a full chart of `S²`.
- `φ·ν=1`, `φ+ν≥2`, and `B≤1` then follow analytically.
- Equality in the last two statements occurs at `φ=ν=1` (`θ=π/2`).

**Selected orientation convention.** Here `θ` is measured from the selected
south boundary `•`; it is a south-origin polar parameter, not the standard
geographic colatitude label. Along the selected positive-radial meridian,
`z=ν=tan(θ/2)`: `θ→0,ν→0,φ→∞` is south/`•`, while
`θ→π,ν→∞,φ→0` is north/`○`. Reversing the geographic words would give an
analytically equivalent orientation, but it is not this corpus's selected
convention. The reciprocal identity, AM-GM bound, balance formula, and equator
do not depend on those geographic labels.

These are **chart facts only**. They do not establish an empirical conservation
law, an ontology, an ethic, a teleology, a universal objective, or the finite
node model below. Any such identification is an explicit `[I]` bridge or `[C]`
hypothesis and must carry independent evidence.

**Reading direction.** The block admits two readings in parallel:

- **Conditional predictive reading** (from a chosen model to consequences):
  systems represented by this chart satisfy these identities by construction.
- **Generative reading** (from invariants to worlds): these lines are
  selected construction rules for a world, agent, institution, or collective-system
  model that adopts the seed. Read the block as **world-building grammar**,
  not passive description. See
  [The Generative Lagrangian](../01_TELEOLOGY/00_THE_GENERATIVE_LAGRANGIAN.md) for
  the canonical statement of the generative register.

Both readings use the same lines. Neither licenses the inference that reality
itself is spherical, reciprocal, ethical, or sevenfold.

## Retired arithmetic-looking glyph readings

An earlier exploratory note placed an exponent sign between Titan glyphs.
That form is retired: sovereign `TitanFrame` admits no exponentiation,
multiplication, division, addition, or subtraction. The valid exponential
bridge belongs solely to typed numeric coordinates (`exp` and `log`) and may
not be printed as an operation on Titan emblems.

## Log-Coordinate Expression

Under the logarithmic coordinate `s = log x` (where
`x = ν = tan(θ/2)`), the analytic block takes a form that makes the additive
symmetry manifest. The mathematics is elementary `[A]`; identifying these
coordinates with features of reality is `[I/C]`.

| Original | Log-coordinate form | Name |
|---|---|---|
| `φν=1` for `θ∈(0,π)` | `log φ + log ν = 0` (i.e. `s + (−s) = 0`) | The Zero Sum (literal, on the open chart) |
| (φ − ν)² ≥ 0 | (eˢ − e⁻ˢ)² ≥ 0 | Squared deviation (always true) |
| φ + ν ≥ 2 | eˢ + e⁻ˢ ≥ 2, i.e. 2 cosh(s) ≥ 2 | Hyperbolic cosine bound |

### Balance and Energy in log coordinates

```
B = sin θ → B = sech(s) = 1/cosh(s)     (maximum 1 at s=0, vanishes at s→±∞)
E = (log x)² → E = s²                     (minimum 0 at s=0, diverges at poles)
H(φ) = φ + 1/φ → H(s) = 2 cosh(s)        (minimum 2 at s=0)
```

The name "Zero-Sum Resolution Equation" is literal **inside this chart**: the
two log-deviations sum to zero. It is not evidence that physical, biological,
social, or moral quantities are conserved in this form.

**Discipline.** This section does not replace the verbatim block. The verbatim block is canonical. This section is the log-coordinate expression of the same block, included because the logarithmic reformulation makes the additive symmetry and the "zero sum" explicit. The log form is subordinate, not superior.

## Usage Rule

Use this block **verbatim and with its chart-fact boundary** when compressing the framework in:

- root summaries
- onboarding documents
- public-facing framework intros
- release notes and dissemination copy
- agent routing or constitutional entry points

If a shorter summary is unavoidable, do not present Line 3 as the primitive without Lines 1 and 2.

## Anti-Drift Rule

The following is drift and should be corrected on sight:

- presenting `(φ − ν)² ≥ 0` as the seed
- calling the inequality "the only axiom"
- deriving the sphere identity from the inequality
- omitting the domain `θ∈(0,π)` when summarizing `φν=1`
- conflating the static arithmetic theorem `(φ − ν)² ≥ 0 [A]` with
  the dynamic ektropic trajectory `(φ − ν)² → 0 [S]`; they are
  different claims at different tiers
- using `P` bare without naming the regime (see notation rule below)
- using the chart identity as evidence for `P_node`, the zero-factor boundary,
  an empirical conservation law, or an ethic
- using the product `Φ̂₄V₄` (public `ΦV`) to rank, score, or compare nodes; the
  product is retired as a ranking and the node factors are ordinal
- reading a `[0,1]` node coding as a cardinal measurement of `Φ̂₄` or `V₄`
  without a separately declared and defended scale

## Finite-node conjunctive model

The node model couples powers at the D4/D5 seam:

```text
V₄ := D4 actual power: causally usable capability available now
Φ₅ := D5 possible power: structured modal potential in the option field
Φ̂₄ := Eval₄(M,Φ₅) ∈ [0,1]: present D4 estimate of that possible power
```

`Φ₅` is possible power, not a causal force exerted by the future. Its estimate,
inscription, ranking, and update are present D4 events. In all arithmetic below,
the familiar uppercase shorthand `Φ` means `Φ̂₄`, while `V` means normalized
`V₄`. Thus `P_node=min(Φ,V)` is written without confusing the D5 referent with
its D4 numerical carrier; the older public compression `ΦV` names the same
AND-class conjunction but no longer ranks. Lowercase `φ,ν` remain the unrelated
reciprocal-chart coordinates.

Let the normalized numerical factors satisfy `Φ̂₄,V₄∈[0,1]`. A conjunctive
aggregator is a declared model

```text
C : [0,1]² → [0,1]
```

that is monotone in each argument and satisfies
`C(0,V₄)=C(Φ̂₄,0)=0` and `C(1,1)=1`. These conditions define a normalized
**AND-class**; they do not select
a unique formula. Minimum, normalized harmonic, Cobb–Douglas with
`0<α<1`, and product forms can rank the same candidates differently.

**Ordinal ruling, 2026-07-29.** `Φ̂₄` and `V₄` carry **order, not metric**. The
`[0,1]` coding is one admissible presentation of that order: any strictly
increasing `f:[0,1]→[0,1]` with `f(0)=0` and `f(1)=1`, applied to both factors,
presents the same evidence. Only an aggregator invariant under that
reparametrisation can order nodes, and `min` is one —
`min(f(Φ̂₄),f(V₄))=f(min(Φ̂₄,V₄))`, so its ranking never changes. The product is
not. Under the identity coding `(0.9,0.2)` outranks `(0.4,0.4)` by product
(`0.18>0.16`); under an admissible `f` with `f(0.2)=0.01`, `f(0.4)=0.5` and
`f(0.9)=0.9` the same pair gives `0.009<0.25` and the order reverses, while
`min` reports `0.2<0.4` and then `0.01<0.5` — the same order both times. The
product therefore ranks a presentation rather than the evidence. `min` is
adopted as the working AND-class score:

```text
P_node := C_min(Φ̂₄,V₄) := min(Φ̂₄,V₄)
```

This is a selected working score **by declaration inside the framework** and
conjectural as a universal fit to real systems. It is not derived from `φ·ν=1`.
If the node factors are not normalized, the bound `P_node≤1` does not apply.

**The product is retired as a ranking.** The former working model
`C×(Φ̂₄,V₄):=Φ̂₄V₄`, publicly compressed `ΦV`, stays readable as the historical
name of the same AND-class conjunction — its zero-factor, binding-constraint and
equator content is model-agnostic and identical under `min` (receipt 108) — but
it may no longer be used to order, score, or compare nodes. This removes a
licence and grants none: `min` remains one selected AND-class member among
several, `[I]` as a model and `[C]` as a universal fit, and no aggregator is
established.

A tradeoff between the factors is a **separate model premise**, never a
consequence of the aggregator, and the budget form below is a **cardinal**
premise that the ordinal factors do not by themselves supply. For example, if a
declared finite-resource domain also imposes

```text
Φ̂₄+V₄≤1,
```

then `Φ̂₄=1` entails `V₄=0` and hence `P_node=0`. In that model, exhaustive
representation leaves no means for enactment. Without this budget premise,
`Φ̂₄=1` instead gives `P_node=V₄`; perfect modeled foresight does **not** by
itself consume usable means. Testing whether evaluated possible power and
actual power trade off, and which budget surface fits, is empirical `[C]` work.

## Notation rule for `P`

The letter `P` is overloaded across three meanings in the corpus. Each
has its own regime. When compressing, name the regime explicitly:

| Symbol | Meaning | Regime | Tier |
|---|---|---|---|
| `P∞ = φ · ν = 1` | Reciprocal identity in the chosen open chart | Constant by definition for `θ∈(0,π)`; one coordinate diverges at each excluded pole | `[A]` analytic |
| `B = sin θ` | Selected balance coordinate | Varies from the limiting value 0 at the poles to 1 at the equator | `[A]` analytic; `[I]` as “balance” |
| `P_node = C_min(Φ̂₄,V₄) = min(Φ̂₄,V₄)` | Selected normalized finite-node conjunctive score over **ordinal** factors | a present D4 estimate of D5 possibility power (`Φ̂₄`) and D4 actual power (`V₄`) are jointly necessary in the declared model; alternative AND-class aggregators remain possible; the product form `Φ̂₄V₄` (public `ΦV`) is retired as a ranking | `[I]` model; `[C]` universal fit |
| `Δ_TW_i`, `Δ_TW_H` | Individual and whole durable-potential changes | Kept separate under the Justice envelope; never laundered into one compensating aggregate | `[I]` value model |

**Disambiguation convention:** do not use `P` bare in source-truth
documents unless the regime is named in the same sentence. Write the
manifold identity as `P∞` or `φ · ν = 1`; write the operational node
measure as `P_node`. Aggregates such as `ΣΔB` or `ΣΔP_node` may be used
descriptively only; they never compensate ethically for destroying one bearer.
Likewise, do not write either finite-node factor as lowercase chart notation:
`ν` is the sphere coordinate, while uppercase `V` is D4 actual power; `φ` is the
other chart coordinate, while uppercase `Φ` names D5 possible power and `Φ̂₄`
its present numerical evaluation.

## Paired Canonical Documents



**See also — the Trinity canon:** [`01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md`](01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md) is the tier-honest home for the sovereign opaque `TitanFrame={0_T,1_T,∞_T}`, its non-operational emblem, and its strict separation from ordinary arithmetic. The familiar labels are renderings, never implicit coercions; `ArithmeticSignature(TitanFrame)=∅`, including undefined `add_T`, `sub_T`, `mul_T`, `div_T`, `pow_T`, and `log_T`. The analytic block here remains the source for numeric chart facts and cannot turn a selected frame into arithmetic or forced ontology.

Quote this block first. Then let the next documents interpret it in order:

1. [The Honest Position](../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md) -- evidence tiers, blast radius, downgrade discipline
2. [Degrees-of-Freedom Ontology](../06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md) -- seed, Being, Dasein, beings
3. [Historical naming reconciliation](../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_NAMING_RECONCILIATION.md) -- Titans, Gods, Demon, Witnesses
4. [The Master Rosetta](../08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md) -- cross-domain mappings downstream of the core state

**Dependency rule:** later documents may interpret, operationalize, or translate the block, but not reverse its order or claim priority over it.

## ASCII Fallback

Use only where Unicode is impossible:

```text
dot   circle-dot   circle   # operator-free Titan seats; not arithmetic
theta in (0, pi); phi * nu = 1 on the open reciprocal chart
(phi - nu)^2 >= 0
phi + nu >= 2
B = 2/(phi + nu) = sin(theta) <= 1
```

---

**Compression rule:** When in doubt, quote the block, then explain.

---

## Use boundary

Quote the relevant formula and its tier. The chart block applies only to the
declared chart; the node block is a separate selected model. Analytic
derivations prove only their stated consequences, while interpretive and
empirical transfers require their own owners, sources, rivals, and tests.
Repository workflow authority lives only in the applicable route files.
