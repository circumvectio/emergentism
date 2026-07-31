---
title: "The Q6 kill was run: 50 frozen library pages cite a retracted study unfenced — the reader dissent is answered against, by measurement"
status: "[A] the counts are reproducible by one command. [S] unchanged — Q6 remains a selection; it is now a selection with evidence under it."
date: 2026-07-31
evidence_tier: "[A] the page counts and the fenced/unfenced split; [B] the classification of a page as current vs frozen, which is read from public_semantic_parity.json; [S] Q6 itself"
owner: "Found during the handoff tidy of 2026-07-31. No owner ruling is requested or implied — this receipt reports a measurement Q6 itself named."
parents:
  - 193_FIVE_RULINGS_SIGNED_2026_07_31.md
  - 232_FIVE_RULINGS_EXECUTED_2026_07_31.md
  - ../../00_META/00_THE_CLAIM_STATUS_REGISTER.md
---

# The library audit Q6 asked for, partially run

## What Q6 staked itself on

Ruling Q6 kept the ~300-page library at `noindex, follow` and published the reason. The
reader seat dissented — *"my lens is checkability, and this hides the checkable material"*
— and the majority did not dismiss the dissent. It **deferred it to evidence** and named
the evidence:

> A page-by-page audit of the library. If the frozen library carries no unrepaired claim
> contradicted by a later ruling, the safety ground vanishes and the dissent wins on reach
> alone.

That audit had not been run. One slice of it now has.

## The measurement

The Global Flourishing Study was **retracted** by this corpus.
`00_META/00_THE_CLAIM_STATUS_REGISTER.md:212` records `DF-06 | balance hump as empirical
law | EMPIRICALLY-REFUTED | Munnell trough; GFS retracted`. So any page still offering GFS
as a live instrument is carrying an unrepaired claim contradicted by a later ruling —
exactly the class Q6 named.

Counting pages under `12_PUBLIC_SITE/` that mention `GFS` or `Global Flourishing`, and
splitting them by the publication tier recorded in `public_semantic_parity.json`:

| tier | pages mentioning GFS | of which carry NO retraction language |
|---|---|---|
| **current surfaces** (incl. declared-provisional) | **1** | **0** |
| **frozen library** | **68** | **50** |

The single current-surface mention is `/record/`, and it is the retraction record itself —
fenced, and doing its job.

Representative unfenced instance, `12_PUBLIC_SITE/formal/13-efr-two-sacrifices/index.html`
line 238, which offers the retracted instrument as one of three interchangeable valid
choices:

> *"Any operationalization of B (Ryff balance, GFS multiplicative score, organizational
> health metrics) works."*

Reproduce with:

```bash
grep -rl -e GFS -e "Global Flourishing" 12_PUBLIC_SITE --include=index.html
```

## What this settles, and what it does not

**It answers the Q6 dissent, against the dissent.** The reader seat's case was that the
frozen library holds the most checkable material and should be reachable by search. The
counter-case was safety. Safety was, until today, an *argument*. It is now a **number**: 50
frozen pages present a retracted study as a live instrument, with no fence. Indexing them
would make search the distribution channel for exactly that. **The freeze is vindicated on
the evidence Q6 itself nominated.**

**It does not vindicate the corpus.** The same number is an indictment. Fifty pages went on
saying something the corpus had already retracted, and nothing in the repository noticed
until a tidy pass grepped for it. That is the *propagation* failure receipt 232 already
recorded in another register — a corpus that corrects in one place and not the others.

**It does not make Q6 `[A]`.** Q6 is a selection and stays one. Evidence under a selection
is not a proof of it.

**It is one slice, not the audit.** GFS is a single retracted item. The full page-by-page
audit Q6 named would sweep every claim the corpus has since narrowed, refuted or
tombstoned. Until that runs, the correct statement is *"the library is known to carry at
least 50 unrepaired pages,"* never *"the library has been audited."*

## What it costs to fix, stated honestly

Fencing 50 pages is not a tidy task and was not attempted here. It requires a doctrinal
judgment this receipt does not make: whether citing the GFS **instrument** as one possible
operationalization of balance is invalidated by the retraction of the GFS **study's
findings**. Those are different claims and the corpus's own register-discipline says they
must be treated as different. **An owner or a council should scope that before anyone
edits fifty pages.**

## Kill

Show that the 50 pages do not in fact present GFS as live — that the mentions are
historical, quoted, or already fenced by wording my search did not match. Then the count is
wrong and this receipt overstates. The command above is the whole method; it matches
`retract|withdraw|register-wrong` case-insensitively and nothing else, so a page fenced in
different words would be miscounted as unfenced. **That is a real weakness of this
measurement and it cuts against my own conclusion.**

•   ⊙   ○ — *a freeze defended by a number is still a freeze; it is just no longer only an opinion.*
