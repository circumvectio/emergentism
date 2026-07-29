---
title: "Receipt 172 — Claim Status Register and grave adjudication"
date: 2026-07-29
status: "COMMITMENT RECEIPT — editorial construction; no claim promoted, no outcome claimed"
evidence_tier: "[B] files created and validators run; [S] the status ladder and one-way rule; [I] the per-grave adjudication"
owner: 01_EMERGENTISM
parents:
  - 00_THE_RECORD_LEDGER.md
  - ../../00_META/00_SETTLED_CANON_REGISTRY.md
  - ../../06_ONTOLOGY/04_THE_CONJECTURES.md
---

# Receipt 172 — Claim Status Register and grave adjudication

## Request

Owner instruction, 2026-07-29: resurrect the dead forms as conjectures and
work-in-progress, and produce a list separating formally validated conjectures
from unvalidated and rejected ones.

## Finding that shaped the execution `[I]`

The twenty-two dead forms in K-7 §2 are **not one epistemic kind**. The single
word *dead* was carrying at least six distinct states: refuted by an explicit
counterexample inside the claim's own system; refuted by observation within a
declared scope; a type error no evidence can repair; a claim never well-posed
enough to live or die; a strong form narrowed to a live weaker one; and one row
(`DF-22`) that was never a claim at all but a failure of the record machinery.

A flat resurrection would have placed a refuted lemma and an untested wager on
the same shelf. That is the precise move `DF-22` records, `E9` forbids, and
Refusal 5 exists to block. The execution therefore adds a **second axis** rather
than moving anything along the existing one.

## What was built `[B]`

| Path | Role |
|---|---|
| `00_META/00_THE_CLAIM_STATUS_REGISTER.md` | human routing surface: two-axis model, twelve-status ladder, one-way rule, reopening protocol, four tables |
| `00_META/claim_status/CLAIM_STATUS.yaml` | the same rows in the corpus JSON-subset form |
| `09_TOOLS/01_SCRIPTS/check_claim_status.py` | fail-closed validator |

Nothing existing was edited. No tier changed. No owner was displaced. The
register declares itself a routing surface subordinate to K-1…K-7.

## The adjudication `[I]`

All 22 graves are now typed, each with the counterexample that killed it and the
address of its live successor:

- **10** `FORMALLY-REFUTED` — counterexample inside the claim's own system:
  `DF-01, 04, 08, 09, 10, 11, 12, 16, 19, 21`
- **4** `EMPIRICALLY-REFUTED` within declared scope: `DF-03, 06, 07, 13`
- **4** `CATEGORY-ERROR` — repairable only by retyping, never by evidence: `DF-02, 05, 15, 20`
- **2** `NOT-WELL-POSED` — must be re-posed before they can live or die: `DF-17, 18`
- **1** `NARROWED` with the weaker form already live: `DF-14`
- **1** `PROCESS-DEFECT` — routed to `E9` enforcement, not to a wager: `DF-22`

**Twelve of the twenty-two already had a live successor** under an existing
owner (`W3`, `W6`, `W7a`, `W10`, `W11`, `W12`, `E8`, `E9`, `GP-11`, `KSC-04`,
`HC-11`).
The resurrection the instruction asks for had largely already happened,
distributed across the wager and axiom ledgers; what did not exist was a single
surface showing grave → successor → status → next test.

**Two are closed with no successor:** `DF-05` (`φν=1` as conserved discovery) and
`DF-21` (CC-CORE-1). Both are the seam-is-not-the-score error stated twice.

## Newly opened `[C]`

Nine questions satisfy the reopening protocol — new id, explicit weakening or
retyping, the parent's counterexample carried, a discriminator, a kill, a
survivor:

`RQ-01` equator-transfer instrument · `RQ-02` a real `η_move≈0` witness ·
`RQ-03` any hypotheses forcing `N=3` · `RQ-04` substrate plurality ·
`RQ-05` lineage independence for convergence · `RQ-06` a civilizational
discriminator · `RQ-07` a declared dynamics for `(φ−ν)²→0` · `RQ-08` a
predictive numeric overlay · `RQ-09` non-circular `REACHABLE`.

`RQ-01` deserves note: Revelation 3 records that the GFS instrument could not
test a zero-factor knockout at all. The balance hump therefore died **partly of
instrument**, not only of fact — a legitimate reopening the flat grave list hid.

`RQ-09` is not a resurrection. It is the corpus's own named `∅` debt on `E4`,
placed on the same board because it is the largest unpaid item in the framework.

## Verification `[B]`

```
python3 09_TOOLS/01_SCRIPTS/check_claim_status.py   → PASS (18 validated, 17 open, 22 graves, 9 reopened)
python3 09_TOOLS/01_SCRIPTS/check_emergentism_purity.py → PASS (818 active files scanned)
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check → PASS (71 cards, 384 edges)
```

Negative test executed: flipping `DF-11` from `FORMALLY-REFUTED` to
`OPEN-FORMAL` was rejected by the validator with
`cites a counterexample but carries live status OPEN-FORMAL`. The one-way rule
is mechanically enforced, not merely written down. The mutation was reverted and
the register re-verified.

## What this receipt does **not** claim

- No claim was validated, promoted, or strengthened. Status is not evidence.
- The nine `RQ` rows are `[C]` questions with kills attached, not results.
- No test was run against the world. This is a commitment receipt; the outcome
  receipts belong to whoever prosecutes `RQ-01…RQ-09`.
- The register is not an eighth kernel surface and owns nothing.

## Open, carried forward

The stale kill criterion at `08_FRAMEWORK_SUPPORT/00_META/01_THE_THREE_POSTURES.md`
§5 still reads *"if a fourth posture is exhibited that is not a composition of
these three"* while §2 of the same document was amended to four postures by
receipt 129. As written the falsifier can no longer fire. Flagged, not repaired —
it needs its own owner decision.

•   ⊙   ○ — *the graves keep their counterexamples; the doors open outward, onto different questions.*
