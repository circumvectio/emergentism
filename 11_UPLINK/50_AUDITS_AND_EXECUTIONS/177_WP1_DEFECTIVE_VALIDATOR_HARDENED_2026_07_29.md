---
title: "Receipt 177 — WP-1 found defective; validator hardened; a false attestation corrected"
date: 2026-07-29
status: "CORRECTION RECEIPT — records a false commit attestation, an over-broad ruling, and seven validator holes"
evidence_tier: "[B] the defects, reproduced and dated; [S] the hardening; [I] the reading"
owner: 01_EMERGENTISM
parents:
  - 172_CLAIM_STATUS_REGISTER_AND_GRAVE_ADJUDICATION_2026_07_29.md
  - 174_OWNER_REOPENING_AND_TITAN_RESTORATION_2026_07_29.md
  - ../../00_META/00_THE_CLAIM_STATUS_REGISTER.md
---

# Receipt 177 — WP-1 was defective

An adversarial verification of the WP-1 and WP-2 repairs (2026-07-29, 9 agents,
61 mutations against a sandboxed copy) returned **44 of 61 mutations passing** a
validator this corpus had four times described as "fail-closed."

This receipt exists because `00_META/00_THE_CLAIM_STATUS_REGISTER.md` §7 clause 4
forbids narrowing that criterion without a dated receipt recording that it fired.
It fired. This is the receipt.

## §1 · The verdict that matters first `[B]`

**Neither WP-1 nor WP-2 committed DF-22.** WP-1 preserved its original kill
criterion word-for-word and recorded the firing in the open. WP-2 left the §2
grave table **byte-identical** — verified by diff, grave-date census unchanged.
No tombstone, grave date or counterexample was disturbed, and no tier was
promoted anywhere.

That established, WP-1 was **defective**, and the corpus should hold both facts.

## §2 · The false attestation `[B]`

Commit `f05cbc31` states: *"CLAIM_STATUS.yaml untouched — it was already correct."*

**It was not correct.** `rules[1]` still carried the retired one-move rule
verbatim — *"may only be superseded by a new row with a new id"* — directly
contradicting `rules[5]`, which named `OWNER-REOPENED` as lawful and listed only
**three** of its four preconditions, silently dropping `status_before_reopening`.

The `rules` block is never read by the validator, so it is machine-facing text
that drifts unchecked. **A false statement in a commit message is not DF-22, but
it is the nearest thing to it produced in this programme**, and it is recorded
here rather than amended away. `rules[1]` is now repaired to state all three
lawful moves.

## §3 · Receipt 174 was over-broad by exactly one row `[B]`

r174 moved **all 22** dead forms to `OWNER-REOPENED`. `DF-14` was already
`NARROWED` — a **live** status — so "reopening" it was meaningless, and it
recorded `status_before_reopening: "NARROWED"`, a live-to-live reopening that
means nothing.

**Corrected:** `DF-14` returns to `NARROWED`, its true state, with its weaker
form live under `KSC-04`. The scope now reads **21 reopened, not 22**. r174's
ruling stands; its blanket application was one row too wide.

## §4 · The seven holes, and the hardening `[S]`

**HOLE 0 — the validator is not a gate.** Verified: no `.github/workflows`, no
pre-commit or pre-push reference, no Makefile or runner. Nothing invokes it. Every
corpus claim that "emptying a counterexample **fails the build**" was false —
**there is no build.** Receipts 172, 174, 175 and 176 each call it fail-closed.
That word was earned only in the sense that a human ran it and it failed; it was
never automatic. **Recorded as an open debt, not repaired here** — installing a
gate is a change to how this repository operates and belongs to its owner.

The six content holes are now closed, each re-tested with the audit's own killing
mutation:

| # | Hole | Closed by |
|---|---|---|
| 1 | `restored` and unknown top-level sections unvalidated — a refuted form appendable as `FORMALLY-VALID` | unknown sections refused; `restored` rows typed, `TR-nn` ids only, grave ids rejected |
| 2 | `NARROWED` an unguarded live status — all 22 relabelled, preconditions and ruling deleted, PASS | `NARROWED` guarded identically to `OWNER-REOPENED` |
| 3 | counterexample softening undetectable — every one set to `"none"`, PASS | placeholder pattern + minimum content length |
| 4 | receipt check `is_file()` on an unresolved path — `/etc/passwd` passed | repo-relative, no `..`, pinned to the r174 ruling, non-trivial size |
| 5 | **self-amending constitution** — vocabularies read from the file under validation, so moving a status disabled every check gated on it | vocabularies **pinned in the script**; the document must now *match* them |
| 6 | `status_before_reopening` never type-checked — `"banana"` passed | must be a **terminal** status |

**Hole 5 is the one to remember.** A checker that takes its constitution from the
file it is policing is not a checker. That is the structural lesson, and it
generalises beyond this validator.

Two live defects were caught by the hardened checker on its first run, and both
were real: `DF-14` above, and `DF-08`'s counterexample, which was too thin to
carry the kill it recorded. Both repaired.

## §5 · What remains owed `[B]`

- **A gate.** Until something invokes these checkers automatically, they are
  advisory. Owner decision.
- `00_META/00_THE_CLAIM_STATUS_REGISTER.md` §2 still carries a "when and only
  when, all five are supplied … a new ID" paragraph ten lines below the new
  three-move table; read literally it makes all reopened rows illegitimate.
- §5's "fourteen of the twenty-two" should read **twelve**.
- K-7's receipt-169 scope credits it with `KSC-25`; receipt 169 explicitly
  disclaims that ruling. Restate as provenance, not authorship.
- K-7's "Row 9 stays dead" sits under "every row is now `OWNER-REOPENED`" — the
  intent is right and conservative, the wording is quotable against itself.
- `00_META/registers/FILE_REGISTER.json` sha for the ledger is stale after WP-2;
  regenerate, do not hand-edit.

## §6 · The amended criterion, and why this receipt had to exist

`00_META/00_THE_CLAIM_STATUS_REGISTER.md` §7 clause 4 reads: *this surface has
failed if the criterion is narrowed, weakened or deleted **without a dated
receipt recording that it fired***.

WP-1 amended that criterion in the same act that enacted it, and filed no
receipt. Clause 4 tripped on its author. **This receipt discharges it.**

The corpus should notice what happened here: a rule written on 2026-07-29 caught
its own author within hours, by machine, and the catch was reported rather than
quietly repaired. That is the apparatus working. It is also not evidence the
apparatus is right — only that it is live.

•   ⊙   ○ — *a checker that takes its constitution from its subject is not a checker.*
