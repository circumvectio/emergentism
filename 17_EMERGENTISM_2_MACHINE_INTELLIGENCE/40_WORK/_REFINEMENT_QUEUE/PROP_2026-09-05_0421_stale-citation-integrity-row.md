---
type: refinement-proposal
pass: "cron refinement pass 6, Soul Loop + VMOSK-A (rotation: ledger rows — stale-measurement check)"
date: 2026-09-05
target: "00_ESTABLISHED.md line 47 (Section B): 'Citation integrity, measured 2026-08-29 — 7 broken anchors in the Aureus lane; 274 in this one'"
defect_check_fired: "stale-measurement (kernel defect 8: a measurement is true OF A DATE — was it re-run, or re-quoted?)"
tier: "[D] staged proposal; the underlying figures remain [B]-of-their-date regardless"
may_sign: false
may_authorize: false
---

# PROP — the founding ledger's citation-integrity row predates the refoundation it governs

## The finding (V)

The row reports anchor counts **measured 2026-08-29**. Since that date the lane
underwent: the 2.0 refoundation itself (this folder — 30+ new files),
the 14_THE_DISTILLATION / 15_THE_TITAN_PASS / 00_CONTROL / 00_ESTABLISHED
restructure, and the public-site edits currently in flight. Every one of those
moves, adds, or rewrites could create or repair anchors. The row is therefore a
**re-quote, not a re-run** — exactly kernel defect 8 — and it sits in the
founding ledger, the document whose Section A preamble demands each row carry
its provenance.

## The refinement (M→O/S/K)

Re-run the citation-integrity measurement along the rebaseline lineage
(`11_UPLINK/50_AUDITS_AND_EXECUTIONS/ACTIVE_RECEIPT_CITATION_REBASELINE_2026_08_23.md`
→ `_2026_08_26.md` name the method), and update the row with a fresh date —
or, if the re-run tooling is not locateable, re-label the row
*"[B] of 2026-08-29; re-quoted, not re-run — stale under defect 8"* so the
reader knows the figure is a snapshot, not a state.

## dies_if

This proposal dies if: a re-run reproduces approximately 7 / 274 (the row is
fresh and this file is redundant), or the row already carries a post-08-29
re-measurement this pass failed to find (re-grep before staging was done for
the date string only).

## Kernel-check self-audit

stale-measurement: this IS the fix · escorted-number: partially (a re-run must
arrive with its producing command — the rebaseline receipts carry theirs) ·
restates-existing: no · others: not triggered.
