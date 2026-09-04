---
type: refinement-proposal
pass: "cron refinement pass, Soul Loop + VMOSK-A"
date: 2026-09-05
target: "00_ESTABLISHED.md line 45 (Section B, our measurements)"
defect_check_fired: "escorted-number (kernel defect 1: does a figure travel with the command that produces it?)"
tier: "[D] staged proposal; the row it proposes to fix is [B] once escorted"
may_sign: false
may_authorize: false
---

# PROP — escort the outcome-change count in the founding ledger

## The finding (V)

00_ESTABLISHED.md §B row 45 states: **"Receipted outcome-changes in the grammar's
lifetime: one"** — tiered `[B]` — but no command, path, or query travels with the
figure. The kernel's own first defect check (escorted-number, DF-22's
instrument) asks exactly this, and the ledger's Section A preamble demands each
row carry owner + hypotheses. The founding ledger currently fails its own
kernel's first check on its own soil.

## The refinement (M→O/S/K)

Append to the row's third column the command that produces the count, so the
figure is re-runnable (this also discharges the stale-measurement check for
future passes). Candidate command, to be verified or corrected by the ledger
owner before promotion:

```sh
git -C 01_EMERGENTISM log --oneline --grep="outcome" -i -- 11_UPLINK/50_AUDITS_AND_EXECUTIONS/
```

If no command reproduces "one", the row loses its `[B]` and is re-tiered
`[I] recollection` until escorted — per the tier grammar's own rule (a tier may
be lowered with evidence; never raised by fluency).

## dies_if

This proposal dies if: the count is escorted by an existing command this
proposal failed to find (then the row is already compliant and this file is
redundant — delete it).

## Kernel-check self-audit

escorted-number: fixes it · restates-existing: no (adds missing provenance) ·
tier-promotion: no · stale-measurement: improves · axis-mix: no ·
convergence/coincidence/unfalsifiable/self-certifying/warrant-substitution: not
triggered (no new claim; a provenance demand on an existing claim).
