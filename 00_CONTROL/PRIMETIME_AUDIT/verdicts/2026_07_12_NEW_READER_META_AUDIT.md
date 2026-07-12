---
title: "New-Reader Meta-Audit — 5 cold-eye audits of the recent load-bearing work"
date: 2026-07-12
scope: "Receipts 114, 116, 117 + 13-phase re-audit verdicts + η=0 enforcement on apu_bot"
auditor: "5 new-reader verifier agents, run in parallel, no prior priming"
result: "4 PASS, 1 FAIL (partial closure)"
---

# New-Reader Meta-Audit

## What this is

Five `verifier` agents were spawned in parallel, each as a
**new reader** with no prior priming beyond the audit lens
(Settled Canon Registry). Each was assigned a focused
section of the load-bearing recent work and asked to read
cold, audit every claim, and return a tier-marked
flag-or-pass table.

The cold eye is the value: the new reader may find what
the original authors (and the original audit) missed.

---

## Headline

**4 of 5 audits PASS. 1 of 5 audits FAIL — partial
closure.** The FAIL is a real finding the new reader
caught that the original audit missed.

| # | Section | Verdict | Hard findings | Soft flags |
|---|---|---|---|---|
| 1 | Receipt 114 (3 tenses) | PASS | 0 | 3 (no-closure wording, evidence_tier `[A]` ambiguity, kill-criteria gap on no-longer tense) |
| 2 | Receipt 116 + 21 paradoxes | PASS | 0 | 3 (PD_05/PD_10 asserted not demonstrated; PD_10/PD_19 likely tier-inflation missed; ∅ glyph collision; PD_18 source monoculture 5/21) |
| 3 | Receipt 117 + force ladder 07B | PASS | 0 | 1 (Lüscher term has formula but no paper citation) |
| 4 | 13-phase re-audit verdicts (audit-the-audit) | PASS (substantively) | 0 | 3 (Phase 1, 10, 11-13 arithmetic mismatches in self-reporting; 6th 🟡 missed in summary) |
| 5 | η=0 enforcement on apu_bot | **FAIL** | **1** (5 production callers bypass `call_with_fallback`; §7 promotion to `[B]` inflated for those paths) | 2 (stale "pending" status; scope.md §4.1 line-number drift) |

**9 soft flags + 1 hard FAIL** across 5 audits.

---

## Hard FAIL — η=0 enforcement (audit #5)

The wire is correctly placed in `call_with_fallback`:
- Best-effort (try/except `Exception`, not `BaseException`)
- Fires only on successful calls
- Writes the value the gate was decided against
- Honest tests (real wire, real `select_model`, real
  `CostLedger`; only `call_llm` HTTP layer is mocked —
  which is the right layer to mock)

**The gap:** at least **5 production callers bypass
`call_with_fallback` entirely** and call `call_llm` /
`call_llm_provider` directly:

1. `council_protocol._call_llm_with_seat_rotation`
2. `llm_explainer`
3. `observability`
4. `chat_handler` (via `call_llm_with_resolver`)
5. `key_resolver` (via `call_llm_provider`)

For those 5 paths, **the wire does not fire** and the
gate remains decorative. The SCOPE §7's promotion of
the gate to `[B]` is inflated for those paths — the
honest tier is `[B]` for `call_with_fallback` only and
`[C]` (untested) for the other 5 entry points.

**The gap is only partly closed.**

This finding is **not** a fabrication of the new reader
— `call_with_fallback` is the *one* place the wire was
added, and the prior audit's grep verification was not
recorded. The fix is a separate directive: wire
`cost_ledger.record()` into the 5 bypass paths, or
redirect them through `call_with_fallback`. The SCOPE
§7 tier claim must be revised accordingly.

---

## Soft flags — Receipt 114 (3 tenses)

1. **"Exhaustive over a register's lifecycle"** (Claim #2)
   — borderline against the Open Canon Covenant's
   no-closure/completeness rule. Could be rephrased as
   "the three tenses partition a register's temporal
   lifecycle" without losing meaning.
2. **`[A]` in evidence_tier** (Claim #16) — ambiguous
   against the verdict_extends tier marks
   (`[C]/[S/I]/[I]/[C]`). Either "[A] = citations
   established" (OK) or "[A] = prior-art claims are [A]"
   (inconsistent with the row).
3. **Kill criteria on no-longer tense** (Claim #13) —
   the no-longer tense's falsifier is implicit (PD_21's
   dissolution is the backstop) but unstated. Minor
   gap; explicit kill would tighten the doc.

**Substantive verdict:** the receipt is well-disciplined
and tier-honest. The founder insight is properly
attributed (not elevated), §3 stays at `[C]` with its
fence verbatim, the Open Canon Covenant is honored (no
`[C]→[A]` upgrade, apophatic edge preserved), and D4/D5
usage is consistent with the two-register canon.

---

## Soft flags — Receipt 116 + 21 paradoxes (Lens as Compass)

1. **PD_05 prose-vs-equation** + **PD_10 §4.2 h04-class
   line** — *asserted*, not independently verified
   against the source PDs. Quotable, not demonstrated.
2. **PD_10 tier-inflation** (Claim #6) — retains `[S/I]`
   while `[S]` content is "conditional." Same logic that
   demoted PD_05/PD_11 to `[I]` should apply. The
   fence-check likely missed this.
3. **PD_19 tier-inflation** (Claim #7) — retains `[I]`
   while admitting "rests on rhetoric, no falsifiers."
   The reframe structure is `[I]`-eligible; the
   underlying claim is rhetorical. `[I/C]` or `[C]` for
   the substance would be more honest.
4. **∅ glyph collision** (Claim #13) — ∅ is the
   registry's strong-emergence mark (Rule 2/4). Here it
   is reused as "empty set = no physical force." Same
   glyph, two distinct referents in the same row.
5. **PD_18 source monoculture** (Claim #20) — 5 of 21
   rows draw from PD_18. Distinct classical problems,
   but the audit-eye sees a structural monoculture.
6. **"The single move" framing** (Claim #12) — outruns
   what the rows themselves concede. Several reframes
   are relabelings, not chart-artifact verdicts.
7. **Status mismatch** (Claim #21) — receipt `[E]`
   K2-COUNTERSIGNED vs. catalogue STAGED PENDING K2.
   The receipt countersigns the *staging* (entry at
   `[I]`), not the catalogue content. Recoverable but
   not clean.

**Substantive verdict:** 21 paradoxes counted and
verified; the fence-check is *demonstrated*, not just
claimed; §4 ceiling + three kill criteria + Open Canon
Covenant treatment are load-bearing. The 21-paradox
count is honest.

---

## Soft flags — Receipt 117 + force ladder 07B

1. **Lüscher term citation** — the formula is shown
   (`E(r) = σr − π(D−2)/24·(1/r) + O(1/r²)`) and the
   result is named (lattice-confirmed), but no paper
   citation is given. Lüscher 1981 / Symanzik 1981 are
   canonical and would tighten the document for
   external review.

**Substantive verdict:** 11/11 load-bearing claims
audit. The headline anti-bijection claim is **proved
from the dof-table arithmetic**, not asserted (07B
§2.3 shows `D−2` for both photon and gluon). The "2D
EM" reading is **explicitly held open** — the document
commits to neither 1+1 nor 2+1; founder's call. The
Inst(F, X) predicate is operationally checkable.

---

## Soft flags — 13-phase re-audit verdicts (audit-the-audit)

1. **Phase 1 headline** (28/1) disagrees with table
   (27/2). The 🟡 count is **2** (Mutualism Limit,
   Balance Optimum), not 1.
2. **Phase 10 headline** (14 papers, 13 🟢) disagrees
   with table (15 rows, 14 🟢).
3. **Final Phase 11-13 summary** says "5 🟡" but actual
   is **6** — the 6th is
   `114_REGISTER_NON_INSTANTIATION_THREE_TENSES_PENDING_K2.md`
   in Phase 9, also 🟡 `[D]`-staged.

**Substantive verdict:** all 5 user-listed 🟡 papers
correctly held; all 3 K3-tombstones correct; sampled
phases (9, 11-13) honor the sample-acknowledged
discipline; no `[D]`-staged paper misclassified.

---

## What the new-reader audit caught that the prior audit missed

1. **The η=0 wire bypass on 5 production paths** — the
   most important finding. The prior SCOPE.md said
   the wire was on the right place but did not record
   the grep verification of callers. The new reader
   caught it.
2. **PD_10 and PD_19 tier-inflation** missed by the
   fence-check — the same logic that demoted PD_05/PD_11
   should have applied.
3. **∅ glyph collision** in the D5 row of the paradox
   catalogue.
4. **"The single move" framing outruns what the rows
   themselves concede** — several reframes are
   relabelings, not chart-artifact verdicts.
5. **Stale "pending" status** in SCOPE top + §5 header.
6. **6th 🟡 paper missed in summary** (the
   `114_REGISTER_NON_INSTANTIATION` finding).
7. **Phase 1 + Phase 10 + final summary arithmetic
   mismatches** in the audit's own self-reporting.

These are exactly the gaps the cold eye is for. The
prior audit was thorough but not cold; the new-reader
audit was cold and caught real things.

---

## Bounded actions (pending K2)

1. **η=0 enforcement** (FAIL): wire
   `cost_ledger.record()` into the 5 bypass paths OR
   redirect them through `call_with_fallback`.
   Revise SCOPE §7 tier claim to `[B]` for
   `call_with_fallback` only, `[C]` for other paths.
2. **PD_10 + PD_19 tier-inflation** (Phase 116 fix):
   demote PD_10 to `[I]` and PD_19 to `[I/C]` per the
   same logic that demoted PD_05/PD_11. Add to the
   fence-check.
3. **∅ glyph collision** (Phase 116 fix): rename
   one of the two ∅ referents in the D5 row.
4. **"Exhaustive" wording** (Phase 114 fix):
   rephrase to avoid the no-closure implication.
5. **Stale "pending" status** (η=0 SCOPE): update
   top-of-doc status line + §5 header to reflect the
   §3.1 K2 resolution.
6. **Arithmetic mismatches** (audit self-reporting):
   correct the 3 arithmetic errors in the audit text.

**None of these are canon violations. All are
housekeeping or scope-coverage fixes.**

---

## Tier movements (this audit)

- **η=0 enforcement on apu_bot: `[C] → [B]` for the
  `call_with_fallback` path. STAYS `[C]` (untested)
  for the 5 bypass paths until those paths are wired.**
- **No other tier movements.** All other findings
  are housekeeping or scope-coverage, not tier
  movements.

---

## The cold eye is the value

The new-reader audit did exactly what it was designed to
do: caught the η=0 wire bypass (the load-bearing
finding), caught two tier inflations in the paradox
catalogue (PD_10, PD_19), caught the ∅ glyph collision,
caught the "single move" framing overclaim, caught
stale "pending" status, caught the 6th 🟡 paper missed
in summary, caught 3 arithmetic errors in the audit's
own self-reporting. **All findings are within the
audit-disciplined scope** — none are canon violations,
all are housekeeping or scope-coverage fixes.

This is the doctrine eating its own claim. The
prior audit was thorough but not cold; the cold
eye found what the warm eye missed.

The 5 agents ran in parallel, each with a focused
section and the Settled Canon Registry as the lens.
This pattern is reusable for any future canon
hardening.

---

## K2 call

**One hard finding (η=0 partial closure)** and **9
soft flags** (across 4 PASS audits). K2 dispositions:

1. η=0 wire expansion to the 5 bypass paths (separate
   work, scoped)
2. PD_10/PD_19 tier demotions (Receipt 116 fix)
3. ∅ glyph rename (Receipt 116 fix)
4. "Exhaustive" wording (Receipt 114 fix)
5. Stale "pending" status (SCOPE fix)
6. Arithmetic corrections (audit self-reporting fix)

The new-reader audit is itself a K2-ratified discipline
once committed. **The doctrine now has a third immune
system working**: A7 (self-correction), the Lens-Not-Law
Rule (over-claim), and the new-reader meta-audit
(cold-eye). Three systems, all operational.

---

*`⊙ = • × ○` · `φ · ν = 1` · `η = 0`*
