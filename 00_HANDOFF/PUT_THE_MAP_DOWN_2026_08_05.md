---
rosetta:
  primary_level: L7
  primary_column: "Philosophy — session close"
  operator: "Viṣṇu ⊙"
  register: "[I] session receipt; [B] all counts reproduced; [S] protocol design"
  canonical_phrase: "Put the map down — the cold-reader trial protocol, the Lean path, the operational layer state, and the honest close"
title: "Put the Map Down — the session receipt"
status: "ACTIVE — the four deliverables the ascent's close requires"
date: 2026-08-05
---

# Put the Map Down

> *The map is good exactly where it is checkable. The map cannot certify
> itself. When the map has done its work, put it down.*

This is the session receipt. Four things, each honest about what it is and
isn't.

---

## I. The cold-reader trial — protocol design

**What this is:** a test protocol for whether the Seed Ladder actually
orients a stranger. Not a trial I can take — I already know the ladder. The
test requires someone who doesn't.

**What the ladder claims to be:**

> *Candidate minimum-sufficient orientation for a declared finite reader —
> tested by cold readers, never certified by the text itself.*

That claim has been cited across the corpus for weeks. **It has never been
tested.** This protocol is how it gets tested.

### The protocol

**Materials.** Seven pages: `00_THE_SEED.md` + `D0` through `D6`. Nothing
else. No ascent readings, no handoff receipts, no audit trail, no AGENTS.md,
no Rosetta dispatch. The naked ladder.

**Reader.** A person with:
- no prior contact with this corpus
- enough mathematics to check `sin θ = 2 sin(θ/2) cos(θ/2)` with pencil and paper
- no faith asked

**Procedure.**
1. Hand the reader the seven pages. Say: *"Read these in order. Take as
   long as you want. When you are done, I will ask you six questions."*
2. Do not answer questions during the read. The ladder is either
   self-sufficient or it isn't; help during the read contaminates the test.
3. After the read, ask:

| # | Question | What it tests |
|---|---|---|
| 1 | *Draw the sphere. Mark where you are strongest. Mark where B = 0. Why?* | D2 comprehension — the product of margins |
| 2 | *A system runs at a/b = 100. What fraction of its capacity does it operate at?* | D2/D5 transfer — the balance discount |
| 3 | *Can you derive the unit from the two boundaries? Why or why not?* | D1 comprehension — existence presupposed |
| 4 | *What is the difference between the seam, the score, and the node?* | The iron separation — the fence |
| 5 | *Is the ethic derived from the geometry? Quote the page that says.* | D5 comprehension — vow not theorem |
| 6 | *What is the one thing you could not check? What tier does it carry?* | Tier discipline — the reader left with an open question, not a false certainty |

**Scoring.**
- Questions 1–4 have checkable answers. The reader either has them or
  doesn't. **A reader who gets 3 of 4 has been oriented.** A reader who
  gets fewer has not, and the ladder is not yet minimum-sufficient.
- Question 5 is the fence test. The correct answer is "no, it is a vow"
  with a citation. A reader who answers "yes" has been **mis-oriented** —
  and that is the most important failure mode to catch.
- Question 6 is the honesty test. A reader who answers "nothing — it's all
  proven" has been **over-claimed at**. A reader who names a `[C]` or
  open question has been oriented honestly.

**Kill criteria for the ladder:**
- Any reader who answers Q5 "yes" (the ethic is derived) → the ladder
  failed its most important fence.
- Fewer than 3 of 4 on Q1–Q4 across two independent readers → the ladder
  is not minimum-sufficient.
- Any reader who cannot name a single unchecked claim → the ladder
  over-claims.

**What I cannot do:** take the test. I am not cold. The test requires a
stranger.

---

## II. The Lean path — what is proven and what remains

**Already machine-checked** (`EmergentismCheck.lean`, 212 lines, 8661 jobs,
no sorry, no added axioms, 2026-07-29):

| Claim | Theorem | Status |
|---|---|---|
| No quotient by zero in a field | `no_quotient_by_zero` | ✅ proven |
| Inversion fixes exactly ±1 | `inversion_fixed_iff` | ✅ proven |
| Unique positive fixed point is 1 | `unique_positive_fixed_point` | ✅ proven |
| Orbit product x·ι(x) = 1 | `orbit_product` | ✅ proven |
| Keel = complementary angles | `keel_is_complementary_angles` | ✅ proven |
| Energy E=(log x)² minimal at 1 | `energy_min_at_one` | ✅ proven |
| At most one two-sided identity | `at_most_one_identity` | ✅ proven |
| Existence NOT forced (F2 counterexample) | `existence_not_forced` | ✅ proven |
| Ĉ is not a ring (structural reason) | `no_absorber_in_nontrivial_ring` | ✅ proven |

**Explicitly NOT checked (§7, stated so the file cannot be over-read):**
- No ontological, ethical, teleological, or cosmological claim.
- The dimension counts underwriting the μ-criterion (HR-1 ruling owed).
- Suda's hinge `= tanh(log x / 2)` (numerically verified to 1e-12, not proved).
- The Lorentz–Möbius correspondence (inherited physics, not re-derived).

**The path forward:**
1. **Suda's hinge in Lean.** The numerical verification exists; the formal
   proof is the natural next step. This would upgrade the balance-score
   identity from numerically verified to machine-checked.
2. **The AM-GM chain.** `min(a,b) ≤ HM(a,b) ≤ 2·min(a,b)` — elementary,
   provable, and would formalize the "weaker leg governs" result.
3. **The product form.** `D• · D∞ = sin θ` — the double-angle identity in
   Lean. This is the corpus's `[I]` reading attached to a classical `[A]`
   identity; formalizing the identity is trivial, formalizing the *reading*
   is not (and should not be attempted — readings are `[I]`).

**What Lean cannot do:** verify the vow, the fence, the findability, or the
reading. Those are `[I]` or `[C]` and belong to human judgment.

---

## III. The operational layer — current state

**Root repo (Magnum Opus main):**
- Gate GREEN — all 4 checkers PASS, stable across consecutive runs.
- `00_HANDOFF/` decongested — depth-1 reduced from 14 loose files to 3.
- PMO registry at 44 valid WIs (35 archived).
- Chair sign packet landed (47 decisions).

**Emergentism repo:**
- Unfindable count: **0** (was 117 at session start).
- Corpus index: 1324 rows, 62.1% with `canonical_phrase`.
- Claim card compiler: FAIL (finity_practice.yaml schema v1→v2 — OWNER).
- File register: regenerated (3617 entries).
- Ascent readings: D1–○ complete (7 readings, 1410 lines).
- Finity_L: killed (8 domains, 0 survivors).

**Open items requiring the owner (K2):**
- Finity_practice.yaml v2 migration (content decisions: owner IDs, sha256).
- OS01-01 re-fingerprint (masks ~30 tests).
- The ⊙ emblem amendment (staged for owner disposition).
- The 349 published pages with retired `⊙ = • × ○`.
- The E2 "seed" gloss contradiction (canon amendment).
- The XaaS binder citation (file does not exist).
- The deploy gate (Councilor B, DNS, ring turn — all host-gated).

---

## IV. The put-it-down receipt

**What this session did:**

| Stream | What | Commits |
|---|---|---|
| **C (contact)** | Finity_L searched 8 domains, killed cleanly | `1553a87e`, `072a13fb`, `90bf5527` |
| **A (findability)** | Unfindable 117 → 0; ascent D1–○ complete | `429b4bf2`–`879481cf` |
| **B (gates)** | fnmatch fixed, dead-forms repointed, register regenerated | `172d5ca6`, `f3d0c2fb` |
| **Method** | §IV circularity recorded; protocol followed | `78a071dc` |

**What this session did NOT do:**
- Did not take the cold-reader trial (I am not cold).
- Did not write new canon (all readings are `[I]` projections).
- Did not move files (the nothing-moves rule held).
- Did not promote a tier, pass a gate, or declare a DAV.

**The honest ledger:**

```
Φ (coherence):  rose — 1410 lines of reader projection, 117→0 findable
V (contact):    one negative result (Finity_L killed) + Lean already green
BAL (balance):  rose — 51.9% → 62.1% phrase coverage
GM (size):      rose — 1324 indexed documents

⊙ = GM × BAL = larger × more balanced = more capable than yesterday
V = still near zero — one clean refutation, no positive external result
```

**The trap, named one last time:** *"we killed our own claim, therefore
killing claims confirms us"* is unfalsifiable. The Finity_L kill does not
confirm the framework. It removes one untested conjecture and costs one
`[C]`. The framework is not more likely to be true because it killed
something. It is more *credible* because it was willing to.

---

## V. The map, put down

The ascent is complete. The index is built. The gates run. The kill is
clean. The Lean `[A]` set is machine-checked. The cold-reader protocol is
written but cannot be taken from inside.

**What remains is not more map.** What remains is:
1. **A stranger reads seven pages** and answers six questions. (Cold-reader
   trial — external, cannot be done from inside.)
2. **The owner decides** the open items. (K2 acts — not an agent's to make.)
3. **A Lean proof of Suda's hinge** upgrades one numerical verification to
   formal. (Mechanical, bounded, can be done — but it is Φ-adjacent, not V.)
4. **The ring turns** on you.skyzai.com. (Host-gated — one real external
   person with their own key.)

The map is good exactly where it is checkable. It cannot certify itself.
And it has done its work.

*Put it down.*

•   ⊙   ○
