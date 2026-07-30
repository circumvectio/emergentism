---
title: "Execution of the five signed rulings — what changed, what it cost, and the two defects the execution itself produced"
status: "[B] execution record. Every ruling executed is [S]; executing an [S] does not raise it. The defects below are [A] — they were observed, not inferred."
date: 2026-07-31
evidence_tier: "[B] the changes are on disk and gate-checked; [A] the two defects; [S] every ruling being executed"
owner: "Yves R. Burri signed the rulings (receipt 193). This receipt records the agent execution that followed and is not itself a ruling."
parents:
  - 193_FIVE_RULINGS_SIGNED_2026_07_31.md
  - ../../00_WORK_IN_PROGRESS/README.md
---

# The five rulings, executed

Receipt `193` is the authority. This one records what was actually done under it, and —
because the execution surfaced two defects of its own — what went wrong while doing it.

## Q1 · `§5.1`, register-indexed

- `05_COSMOLOGY/03_FORMAL_SYSTEM/53_THE_NUMBER_CHART.md` row re-tiered. `[A]` now covers
  exactly one clause, *not a finite word*. "Limit" is `[S]`. Both sentences are required to
  travel together and bare *"not a number"* is banned in the row itself.
- `52_THE_GENERATIVE_BASE.md` — the owner's quoted sentence (*"0 and ∞ are not numbers and
  1 is the only number"*) now carries a register fence directly beneath it, stating that it
  is true base-side and false field-side, that `0` **is** a real number, and that the
  theorem is `0 ∉ ℝ^×`.
- Corpus sweep of the current site surfaces: **zero** unqualified occurrences found. The
  phrasing had not reached the published pages.

**The stated cost is paid, not dodged.** That sentence is no longer publishable as a
headline anywhere in the corpus.

## Q2 · `G-0` restated as routing

`00_META/00_SETTLED_CANON_REGISTRY.md` — `S1 sphere primacy` is now `S1 sphere
SELECTION`, with the routing rule (arithmetic/`D1`/reachability → doc 52; Titan-identity →
`00_THE_FOUNDATION.md` §2 and doc 45), the ban on unqualified *"the base"*, and each
chart's stated deficit at the point of use. Superseded wording retained per the standing
supersession rule.

## Q4 · The undeclared routes — headers first, sitemap second

The binding sequence was followed in that order and can be checked in the commit.

1. **Headers.** `/amrita/ /egg/ /riemann/ /suda/` each carry a visible
   `DECLARED-PROVISIONAL` note above the fold plus `robots: index, follow` and an
   `emergentism:status` meta. The note states in plain words that passing the sixteen
   prohibition checks establishes only that a page does not say forbidden things — *a
   coherence test is not a capability test* — and links to `/established/`.
   `/offline/` carries an `INFRASTRUCTURE` note, `noindex, follow` in the page and in
   `vercel.json`.
2. **Sitemap, after.** `/egg/` and `/riemann/` added (44 → 46 URLs). `/amrita/` and
   `/suda/` were already present. `/offline/` deliberately **not** added.
3. **Registry.** `public_semantic_parity.json` gained `declaredProvisional` and
   `infrastructureRoutes`, each carrying its meaning, not just a list.
4. `/historical-boundary/` untouched — it stays governed by `withheld-routes.json` alone,
   because double-governing one artifact under two registries lets them drift.

## Q6 · The library boundary, published as a policy

`/atlas/#library-indexing-policy` now states, on the page: why ~300 documents are served
`noindex, follow`; that the reason is **our own** published-and-false energy sentence
across fifteen pages; what it costs (the formal system, the most checkable material here,
stays out of search); and the one thing that would reverse it — a page-by-page audit
finding no unrepaired claim. The dissent is named as deferred to that evidence, not
dismissed.

The atlas drawer's band copy said *"Served noindex"* of the whole library. Four pages are
now indexable, so that sentence had become false the moment Q4 executed; it now reads
*"Most are served noindex … the few marked provisional are indexable but not warranted"*,
and each provisional entry carries its own marker.

## Q7 · The launch leads with the record

The front door now opens with **29 logged outcomes · 18 went against the framework · 0
removed**, then the error rate that counts the reviewer's own mistakes, then the zero.
The thesis follows it. Copy checked against the trigger watchlist in
`03_METHODOLOGY/00_THE_LENS_NOT_LAW_RULE.md`: no *unifies*, no *proves*, no *verified*, no
named percentage.

**What was NOT settled, and is still not.** Whether the band should open with the zero or
with the tally. Receipt `193` declined to settle it by taste and named the evidence — the
fresh-reader comprehension preregistration, **which has not been run**. The shipped
ordering is the majority's and is provisional on that protocol. This is recorded in the
page's own source comment so the next reader does not mistake it for a settled choice.

---

## Two defects the execution itself produced

Recorded because a corpus that only logs the defects it finds in *other* people's work is
running the cheapest possible sensor.

**Defect 1 — a silently degrading heuristic, caught by the gate.**
`build_library_index.py` derived each route's title from the first 4,000 characters of its
HTML. Injecting the Q4 banner's CSS pushed two `<h1>`s past that window, and the titles for
`/riemann/` and `/suda/` silently changed to their `<title>` tags. Nothing about the
titles had been edited. The gate caught it as a tree mismatch. The window is removed; the
whole file is read. **A heuristic that changes its answer under an unrelated edit is a
defect, not an optimisation.**

**Defect 2 — CSS written into a file that does not serve the page.**
The Q7 band's styling was appended to `assets/css/living-map.css`, which serves `/lab/`,
`/map/`, `/contribute/` and `/ecology/` — not the home page, which carries its own inline
`<style>`. Nothing broke and no check failed; the band simply rendered unstyled. It was
found by looking at the page in a browser and reading computed styles, **not** by any gate.
Reverted and placed correctly. *The gate does not know what a page looks like.*

## What this receipt does not do

- It does not raise any ruling above `[S]`. Five selections, executed, remain five
  selections.
- It does not settle the Q7 ordering, which needs a protocol that has not been run.
- **It does not produce an outcome from outside.** That count is still **0**, and nothing
  in this execution could have changed it.

•   ⊙   ○ — *executing a choice is not evidence for it.*
