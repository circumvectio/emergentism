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
  vmosk_a_ref: "01_EMERGENTISM/VMOSK_A.md — Perennial Doctrine Root (see also 00_SEVENFOLD_FOUNDATION_ROOT.md)"
---

# The Canonical Formula Block

**Status:** Active
**Evidence tier:** `[A]` for the stated chart identities; `[I]` for their
Emergentist interpretation; `[C]` for universal fit to real systems
**Depends on:** `01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md`, `../01_TELEOLOGY/02_THE_DERIVATION/00_A_SQUARE_CANNOT_BE_NEGATIVE.md`
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

- The first three lines define the open colatitude/radial coordinate of a
  stereographic chart and its reciprocal. They do not include the azimuth and
  therefore are not, by themselves, a full chart of `S²`.
- `φ·ν=1`, `φ+ν≥2`, and `B≤1` then follow analytically.
- Equality in the last two statements occurs at `φ=ν=1` (`θ=π/2`).

These are **chart facts only**. They do not establish an empirical conservation
law, an ontology, an ethic, a teleology, a universal objective, or the finite
node model below. Any such identification is an explicit `[I]` bridge or `[C]`
hypothesis and must carry independent evidence.

**Reading direction.** The block admits two readings in parallel:

- **Conditional predictive reading** (from a chosen model to consequences):
  systems represented by this chart satisfy these identities by construction.
- **Generative reading** (from invariants to worlds): these lines are
  selected construction rules for a world, agent, institution, or DAV
  model that adopts the seed. Read the block as **world-building grammar**,
  not passive description. See
  [The Generative Lagrangian](../01_TELEOLOGY/00_THE_GENERATIVE_LAGRANGIAN.md) for
  the canonical statement of the generative register.

Both readings use the same lines. Neither licenses the inference that reality
itself is spherical, reciprocal, ethical, or sevenfold.

## Non-Canonical Auxiliary Reading

A later exploratory derivation note proposes a **deeper exponential reading** of Line 1:

```text
⊙ = •^○
```

as an Euler-side compression of the exponential bridge from additive to multiplicative structure. This is **not canonical formula-block content** and must not replace the verbatim block above. Treat it as a derivative interpretive note only; see `02_THE_DERIVATION/12_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md`.

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

## Finite-node conjunctive model

Let normalized node factors satisfy `Φ,V∈[0,1]`. A conjunctive aggregator is a
declared model

```text
C : [0,1]² → [0,1]
```

that is monotone in each argument and satisfies
`C(0,V)=C(Φ,0)=0` and `C(1,1)=1`. These conditions define a normalized
**AND-class**; they do not select
a unique formula. Minimum, normalized harmonic, Cobb–Douglas with
`0<α<1`, and product forms can rank the same candidates differently.

Emergentism selects the normalized product as its transparent working model:

```text
P_node := C×(Φ,V) := ΦV
```

This is structural **by declaration inside the framework** and conjectural as a
universal fit to real systems. It is not derived from `φ·ν=1`. If the node
factors are not normalized, the bound `P_node≤1` does not apply.

## Notation rule for `P`

The letter `P` is overloaded across three meanings in the corpus. Each
has its own regime. When compressing, name the regime explicitly:

| Symbol | Meaning | Regime | Tier |
|---|---|---|---|
| `P∞ = φ · ν = 1` | Reciprocal identity in the chosen open chart | Constant by definition for `θ∈(0,π)`; one coordinate diverges at each excluded pole | `[A]` analytic |
| `B = sin θ` | Selected balance coordinate | Varies from the limiting value 0 at the poles to 1 at the equator | `[A]` analytic; `[I]` as “balance” |
| `P_node = C×(Φ,V) = ΦV` | Selected normalized finite-node conjunctive model | D5 option-field quality (`Φ`) and D4 usable means (`V`) are jointly necessary in the declared model; alternative AND-class aggregators remain possible | `[I]` model; `[C]` universal fit |
| `Δ_TW_i`, `Δ_TW_H` | Individual and whole durable-potential changes | Kept separate under the Justice envelope; never laundered into one compensating aggregate | `[I]` value model |

**Disambiguation convention:** do not use `P` bare in source-truth
documents unless the regime is named in the same sentence. Write the
manifold identity as `P∞` or `φ · ν = 1`; write the operational node
measure as `P_node`. Aggregates such as `ΣΔB` or `ΣΔP_node` may be used
descriptively only; they never compensate ethically for destroying one bearer.
Likewise, do not write the finite-node means factor as lowercase `ν` when the
action register is meant: `ν` is the sphere coordinate, while uppercase `V` is
the node's usable D4 means at the boundary.

## Paired Canonical Documents



**See also — the Trinity canon:** [`01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md`](01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md) is the tier-honest home for the selected `{0,1,∞}` Titan tokens, ordinary arithmetic, `1 = 0 × ∞` as an emblem, and the two coupled faces of number (`log 1 = 0`). The analytic block here remains the formal source; the Trinity canon interprets it without upgrading a naming choice into mathematics.

Quote this block first. Then let the next documents interpret it in order:

1. [The Honest Position](../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md) -- evidence tiers, blast radius, downgrade discipline
2. [The Core State of Being](../06_ONTOLOGY/00_THE_ONTOLOGY_OF_BEING.md) -- seed, Being, Dasein, beings
3. [Naming Reconciliation](../08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_NAMING_RECONCILIATION.md) -- Titans, Gods, Demon, Witnesses
4. [The Master Rosetta](../08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md) -- cross-domain mappings downstream of the core state

**Dependency rule:** later documents may interpret, operationalize, or translate the block, but not reverse its order or claim priority over it.

## ASCII Fallback

Use only where Unicode is impossible:

```text
circle-dot = dot x circle
theta in (0, pi); phi * nu = 1 on the open reciprocal chart
(phi - nu)^2 >= 0
phi + nu >= 2
B = 2/(phi + nu) = sin(theta) <= 1
```

---

**Compression rule:** When in doubt, quote the block, then explain.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Quote first, type second.** When referencing any formula, quote the relevant canonical block and state whether the claim is analytic, interpretive, or conjectural.
2. **Respect domain boundaries.** The chart block applies only to systems represented in that chart. The node block is a separately declared model. Never use one as proof of the other.
3. **Verify notation integrity.** The Overleaf typesetting specification is the canonical notation. Do not invent new symbols or alter existing ones.
4. **Link to derivation.** When using a formula, cite its derivation document. The Formula Block is the source of truth; derivations are the proof path.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md`

**Output:** Quote the relevant block, cite derivation, apply to the specific domain context.
