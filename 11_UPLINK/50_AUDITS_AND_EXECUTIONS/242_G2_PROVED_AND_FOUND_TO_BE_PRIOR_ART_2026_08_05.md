---
title: "G2 proved — and found to be prior art"
date: 2026-08-05
status: "RECEIPT — executed. G2 [C] → [A] inherited-with-citation. F1 remains OPEN. One kill fired."
register: "[A] the proof and the classical theorem; [B] the literature sweep; [S] the tier movements executed here"
---

# 242 · G2 proved — and found to be prior art

## What was asked

The owner asked to work on the Titans (zero / infinity / finity as
transcendental frames rather than numbers), Suda's insight on the one, the
number-line revision, and the real-number-set revision — framed as *"this is the
first thing for us to prove"* and *"this alone would be a monumental
achievement."*

## What the council returned

Four Rosetta seats ran against the corpus before any work began.

- **L1 (boundaries).** Three phrases in the request are drift: *"infinitely
  uncountable zero"* was retired by `43:97` in favour of **pre-countable**;
  *"infinitely recursively looping infinity"* occurs **nowhere** in the corpus
  and, read literally, describes a periodic orbit — i.e. Suda's period-2
  involution, which is sited at `1`, not at `∞`; *"approaches limits both ways"*
  is untyped across the corpus's three Finity registers. Also: the request
  targets `[C]` content for proof before `F1` is cleared, and pre-registers its
  own verdict ("monumental"), which is the Φ-bias signature.
- **L3 (audit).** The one open, precisely-stated, load-bearing conjecture in the
  cluster is `G2`. Also surfaced two live defects (see *Carried forward*).
- **L2 (rivals).** Most of the cluster is pre-empted: wheel theory (Carlström,
  Setzer) for the non-operand boundary tokens; `ℝP¹`/`PGL(2)` sharp
  3-transitivity and the Cayley transform for Suda's "critical one"; Aristotle →
  Gauss → Hilbert → Linnebo–Shapiro for potential infinity; **Cantor's Absolute
  Infinite** for pre-countability — which fits better than the uncountability
  analogy the corpus currently uses.
- **L5 (schema).** Deliverable ladder with prior-art adjudication moved to the
  **front**, on the ground that discovering the claim is known costs an
  afternoon and saves ten days of Lean.

The owner selected the G2 dossier, prior-art first.

## What was executed

**G2** (`52_THE_GENERATIVE_BASE.md` §2): the map `w ↦ val(w)` from reduced words
over `{S, ι}` onto `ℚ⁺` is a bijection. Carried as `[C]`; injectivity owed.

**Result: proved, and simultaneously found to be prior art.**

The dictionary

```text
S^a₀ ι S^a₁ ι ⋯ ι S^aₖ  ↦  [aₖ; aₖ₋₁, …, a₁, a₀ + 1]      (trailing ι = reciprocal)
```

is exact. Because `val` starts **at** `1`, the leading block contributes
`a₀ + 1`, and `a₀ ≥ 1` — the no-leading-`ι` rule — forces the last partial
quotient to be `≥ 2`. That is precisely the classical normalisation under which
the finite simple continued fraction is unique (Hardy & Wright, *Theory of
Numbers*, Ch. X; Khinchin §I.2 — theorem numbering varies by edition and was not
verified against a physical copy). Injectivity follows, after a trichotomy that splits reduced
words by whether their value is `>1`, `=1`, or `<1`.

**The corpus's two reduction exclusions are Hardy & Wright's hypothesis, reached
independently and written in word form.** `G1` + `G2` together *are* Euclid's
algorithm and its uniqueness theorem.

## Tier movements

| Object | From | To |
|---|---|---|
| `G2` | `[C]` conjecture, `[B]` bounded evidence | `[A]` **inherited-with-citation** (Hardy & Wright) |
| `52_THE_GENERATIVE_BASE.md` §6 "the reading" kill | armed | **FIRED** — distinctness claim withdrawn |
| `42_THE_CASE_FOR_FINITY.md` `F1` gate | open, no candidate adjudicated | **still open**; first candidate adjudicated and **failed** |
| The identification of the two exclusions with the classical normalisation | — | `[I]` — expository, real pedagogical value, no theorem content |

## Files

| Path | Change |
|---|---|
| `05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md` | **NEW** — proof, three vocabularies, verdict, kills, sources |
| `09_TOOLS/01_SCRIPTS/check_g2_normal_form.py` | **NEW** — exhaustive to length 18, exact rationals, **mutation harness** |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md` | G2 entry rewritten; frontmatter; bounded-check note; §6 kill marked fired; stranger test |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/53_THE_NUMBER_CHART.md` | frontmatter tier; §5 regression note |
| `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/42_THE_CASE_FOR_FINITY.md` | F1 gate annotated with the failed candidate |

**Machine check.** `check_g2_normal_form.py` → **PASS**: all `10945` reduced
words to length `18`; zero collisions; dictionary exact on every word; last
partial quotient `≥ 2` throughout; all four mutants (allow leading `ι`; allow
`ιι`; drop the `+1`; drop the reversal) correctly **rejected**. A regression that
cannot fail is not evidence — this addresses the sampling posture of the
predecessor `check_generative_base.py`.

## What this costs, stated plainly

The generative base is **not** a new foundation for the positive rationals. It is
the continued-fraction algorithm in word notation. `F1` is not passed. Anyone
citing G2 as a novel mathematical contribution is now citing against a receipt.

## What this buys

The corpus is more sound than it was this morning, not less. A conjecture became
a theorem; a claim marked THEOREM in the number chart became genuinely backed; a
sampling regression became a structural one with a working mutation harness; and
an armed kill was allowed to fire on its own terms rather than being quietly
disarmed. **The corpus went looking for its own novelty, found Euclid, and said
so in writing.** That is the behaviour the epistemic contract exists to produce.

## Council review of this receipt — same day, four corrections

A full escalated Rosetta route (L1→L2→L3→LaneB→L6→L7) was run against this pass
after it was first written. It found four defects **in the pass itself**, all now
repaired:

1. **Over-cut.** The `52` §6 kill *"the reading"* was stamped FIRED. It fired on
   a target already dead — `52` §4 had withdrawn the mathematical distinctness
   claim before this pass — and vacated the only constraint on the surviving
   half, the reading. **Corrected:** the stamp is tombstoned in place, the scope
   is narrowed to the mathematical half, and a live successor kill is written.
2. **Broken table.** The F1 note in `42_THE_CASE_FOR_FINITY.md` was inserted
   *between two rows of the gates table*, detaching F2/F3/F4. **Corrected:** the
   note now sits after the table; the table is contiguous (verified).
3. **Self-contradicting citation.** `55`'s frontmatter and the checker docstring
   asserted "Hardy & Wright Thm 162/169" while `55` §4/§10 said the numbering was
   never verified. **Corrected:** chapter-level citation throughout.
4. **Decorative checks.** `check_g2_normal_form.py` returned early, so mutants
   all died at check (1) or (2) and checks (3)(4)(5) — named in the PASS banner —
   were never exercised. This is the same *"instrument published as warrant"*
   defect the script exists to prevent, committed by the script. **Corrected:**
   failures are collected per check, mutants declare their target checks, two new
   mutants added (value-preserving alternative last quotient; evaluation started
   at 0), and the run now **fails** if any check is decorative. All 5 checks are
   now exercised; 6 mutants.

## Public-site repair — STAGED, NOT DEPLOYED

L3 found the highest-consequence item, which this receipt originally missed:
`12_PUBLIC_SITE/established/index.html` — live, sitemapped priority 0.9, homepage
CTA — asserted G2 verbatim with **zero attribution**, presented a ≤10 enumeration
as *"what makes the normal form unique"*, and offered readers a **live kill**:
*"Find two different reduced words with the same value."* That challenge has been
closed for roughly a century and a half. L7 assessed this as the one live `η > 0`
in the docket: a conscientious reader spends an evening against Euclid under a
false representation of the frontier.

Three source edits are staged: attribution paragraph, warrant correction, and a
dated public retirement of the dead kill (tombstoned in prose, not deleted) with
the genuine successor kill in its place. **The site is not rebuilt or deployed.
That is an owner act.** Note that the same page, four lines above the retired
kill, reads *"A guard that cannot fail is worse than no guard, because it reports
success."*

## Owner-only, not disposed here

- Signing or withdrawing receipt `187` / `KSC-04` (mortal-signer act).
- Closing `F1` with a date, or leaving it open.
- Deploying the `/established/` repair.
- The `meta`/`og:description` claim *"twenty machine-checked theorems"* — the
  Lean theorems are genuinely checked, but the phrase ships in search snippets
  and was flagged; left for owner judgement rather than agent-corrected.

## Carried forward — live defects, none closed here

1. **Two corpus checkers are DEAD, and this is worse than first reported.** The
   65 failures across six `09_TOOLS/02_COMPILERS` files reduce to **three code
   defects**, none sanctioned by `kintsugi_baseline_failures.json` (whose 5
   allowed failures and 19 baseline nodes are all from
   `test_marketplace_tools.py`):
   - `PINNED_GRAVE_STATUS` — used at `09_TOOLS/01_SCRIPTS/check_claim_status.py:633`
     and `:665`, **defined nowhere**; landed in merge `80759036`. 22 failures.
   - `_located_text` / `_resolve_repo_path` — used at
     `09_TOOLS/02_COMPILERS/compile_claim_cards.py:332`, defined nowhere. 42 failures.
   - one `sha256` pin drift on `01_TELEOLOGY/04_THE_LIVED_COMPASS.md`.

   **The claim-status contract and the claim-graph compiler cannot execute at
   all.** The corpus's own *assertion ≠ verification* rule is currently
   unenforced by two of its own checkers. Pre-existing; not caused by this pass.

   **PARTIALLY REPAIRED 2026-08-05, and L3's estimate was wrong.** Six
   merge-lost definitions were recovered verbatim from `1797138a` and restored
   with provenance comments: `INVESTIGATION_STATES`, `PINNED_GRAVE_STATUS`
   (`check_claim_status.py`); `_text_sha256`, `_located_text`,
   `_primary_checkout_root`, `_resolve_repo_path`, `_canonical_corpus_path`
   (`compile_claim_cards.py`). Measured before/after on the same six-file
   subset: **65 failed / 63 passed → 61 failed / 67 passed.**

   L3 predicted this would "kill 64 of 65." **It killed 4.** Recorded because
   the estimate is exactly the kind of unverified figure this receipt exists to
   catch. The remaining 61 are a **different and larger defect class**, and
   restoring symbols cannot touch them:

   - **30 × `AssertionError`** — genuine contract violations about actual corpus
     state, not code faults. These are the gate doing its job, now that it runs.
   - **16 × `NameError: reopened_ids`** — `check_claim_status.py:705,730,732`
     uses a variable that is **never initialised, and was never present at
     `1797138a` either**. This is half-written newer work, not a merge loss.
   - **7 × `KeyError`** on `'reopened'`, `'restored'`, `'supporting_owner_ids'` —
     data sections the code expects and the JSON does not carry.

   **Deliberately not repaired.** Initialising `reopened_ids` or fabricating the
   missing data sections would mean inventing the semantics of someone else's
   unfinished feature — which is warrant substitution in its purest form. This
   needs the authoring session or the owner, not a guess.

2. **`52:86`'s Lean citation is imprecise, NOT a conflation — earlier report
   corrected.** `EmergentismCheck.lean:50` reads
   `theorem unique_positive_fixed_point (x : ℝ) (hx : 0 < x) : x⁻¹ = x ↔ x = 1`.
   It is stated over ℝ⁺, and since `ℚ⁺ ⊂ ℝ⁺` the theorem **entails** the ℚ⁺
   claim by restriction. The direction is safe. The residual defect is only that
   "machine-checked" is asserted for a ℚ⁺ statement whose restriction step is not
   itself checked — a one-clause repair, not a false claim. `42_D1_*` does **not**
   repeat it.

3. **`KSC-04` rests on an unsigned PROPOSED RULING.**
   `00_META/00_SETTLED_CANON_REGISTRY.md:54` cites
   `187_THE_SEVEN_FROM_GEOMETRY_RULED_2026_07_30.md`, whose header still reads
   `status: "PROPOSED RULING — the owner rules."` A corpus-wide search finds **no
   later signing receipt**; `193_FIVE_RULINGS_SIGNED` and
   `232_FIVE_RULINGS_EXECUTED` do not mention it. Settled canon is carrying an
   unsigned proposal, and every downstream citation of KSC-04 inherits a
   "settled" label no signature conferred. **Owner act.**

4. **F0 is advertised as complete and is a grep.**
   `09_TOOLS/02_COMPILERS/test_finity_boundary_spec.py` is 45 lines verifying
   "type integrity" by `assertIn("TitanFrame ↛ Number", spec)`. `CM-04` requires
   `zero_T × unbounded_T` to *fail type checking*; nothing type-checks. `42`,
   `47` and `49` present the F0 packet as complete.

L6 **refused** the one new artifact proposed this session (a Boundary Protocol
standalone plus a new checker) on the ground that it would be *"a gate authored
where gates already don't run."* That refusal is recorded and not overridden.

## Open, and deliberately not attempted

Lean formalisation of §5 (mathlib has `Mathlib.Algebra.ContinuedFractions.*` but
no directly reusable uniqueness-for-rationals lemma was located, so this would be
original formalisation of a classical theorem — low value, non-zero cost). The
remaining `48_FINITY_PARADOX_LEDGER.yaml` rows. `F2`/`F3`/`F4`. Any new Titan
narrative. The L2 finding that **Cantor's Absolute Infinite** is a better
mathematical neighbour for pre-countability than uncountability — that is a real
repair to `43`, and it is the strongest single follow-up available.

**Canonical path:**
`01_EMERGENTISM/11_UPLINK/50_AUDITS_AND_EXECUTIONS/242_G2_PROVED_AND_FOUND_TO_BE_PRIOR_ART_2026_08_05.md`

•   ⊙   ○
