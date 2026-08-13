---
title: "R-32 Ruling Receipt — pair()'s adjacency rule stands; the ten anchor failures are content defects"
status: "RECEIPT — records the CHAIR ruling on R-32 given in-session 2026-08-13. Creates no doctrine; the ruling is the authority. Confers no authority to loosen the checker — it orders the opposite."
date: 2026-08-13
evidence_tier: "[S] the ruling — selected by CHAIR (K2) in-session, owned as a choice; [B] the checker run and the failure list, re-run on disk 2026-08-13."
owner: "CHAIR ruled; agent recorded. Recording confers nothing."
parents:
  - THE_EXECUTION_PLAN_2026_08_13.md
  - SPARK_EMISSION_RECEIPT_2026_08_13.md
---

# R-32 Ruling Receipt — 2026-08-13

**The question** (filed by the Wave 4 session at
`THE_EXECUTION_PLAN_2026_08_13.md` §5): *is `pair()`'s adjacency rule
correct?* Relaxing it reportedly clears 9 of the 10 remaining anchor
failures in `16_THE_EMISSION` immediately.

**Ruled: the rule stands. Fix the documents.**

`check_anchors.py:403` keeps its tight attachment — same line, or the
immediately following block with at most a short lead-in. The ten failures
are **content defects in the emission documents**, and they are repaired as
content:

1. **ANCHOR DOES NOT RESOLVE (5):** correct each quoted string to what the
   target actually says, or correct the target path where the checker asks
   *"wrong file?"*. A quote that runs past its closing mark into document
   prose is a quote-boundary defect in the document, not in the gate.
2. **UNANCHORED CITATION (4):** put the quoted string on the same line as
   its path, or mark the reference `{no-anchor}` where the drop is
   deliberate — the gate already exempts and itemises that mark.
3. **CITED PATH DOES NOT RESOLVE (1):** `check_links.py` at
   `A_THE_LADDER/05_D4_ACTUAL.md:64` is ambiguous — two files share the
   basename. Disambiguate with the full path. No adjacency change could
   ever clear this one; it is named here so no one credits it to the rule.

**What this ruling forbids:** any relaxation, widening, or re-windowing of
`pair()` to buy green. The working session's refusal to loosen the gate was
correct and is ratified: a migration rehearsal that only passes with its
checker loosened has rehearsed nothing.

**What it orders:** the ten repairs above, then a clean `check_anchors.py`
run (exit 0), after which Wave 4 closes and Wave 5's gate condition is met.
The repairs are AGENT-class; the checker is not to be modified.

**Canonical path:**
`01_EMERGENTISM/00_HANDOFF/R32_RULING_RECEIPT_2026_08_13.md`

•   ⊙   ○
