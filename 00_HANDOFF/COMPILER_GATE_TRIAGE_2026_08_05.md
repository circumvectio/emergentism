---
title: "Compiler-gate triage — the 61 failures are four defects, not sixty-one"
status: "TRIAGE — diagnosis only. Nothing repaired here. Three of the four require a decision this pass had no standing to make."
date: 2026-08-05
evidence_tier: "[S] every count and every root cause reproduced on disk this session; [I] the attribution of masking"
owner: "Handoff. The claim-card custody owner and the author of the unfinished reopened/restored feature are the two people this document is addressed to."
parents:
  - ../11_UPLINK/50_AUDITS_AND_EXECUTIONS/242_G2_PROVED_AND_FOUND_TO_BE_PRIOR_ART_2026_08_05.md
---

# Compiler-gate triage

## The correction this document exists to make

Two figures were reported earlier today and **both were wrong**. They are
corrected here because the corpus's characteristic failure is an unverified
number quoted as a result.

| Reported | Actual |
|---|---|
| "restoring the merge-lost symbols kills 64 of 65" | **it killed 4** (65 failed → 61 failed) |
| "the remaining failures are 30 genuine contract violations" | **they are ~4 distinct defects**, one of which masks about thirty tests |

The second correction is the substantive one. There are not thirty things wrong
with the corpus's claim graph. There is **one stale claim-card locator**, and it
throws before the tests can reach the conditions they were written to probe.

---

## Defect 1 — `OS01-01` locator fingerprint (masks ~30 tests)

**Symptom.** `compile_claim_cards.py:412` raises
`ContractError: OS01-01: locator fingerprint does not match the declared source
slice`. Roughly thirty tests in `test_corpus_claim_graph.py` are written as
"assert this specific error is raised" — *"exactly one primary"*, *"dangling"*,
*"dependency cycle"*, *"duplicate claim-card"*, and so on. Each one now fails
with *"…does not match `OS01-01: locator fingerprint…`"*, because the compiler
dies on `OS01-01` before reaching the condition under test.

**Those thirty tests are not reporting thirty violations. They are reporting the
same one, thirty times.** Their actual subjects are untested and their status is
unknown until this clears.

**Diagnosis (reproduced on disk).** The card lives in
`00_META/claim_cards/one_sitting.yaml` and points into
`00_THE_WELTANSCHAUUNG_ONE_SITTING.md`, declaring `line_start: 39`,
`line_end: 52`, and a fingerprint.

- The anchor text is now at **line 40**, not 39. The declared slice therefore
  begins on a blank line.
- The slice at HEAD lines **40–53** is **byte-identical** to the slice at lines
  39–52 in the parent of merge `80759036`. The content did not change; it moved
  down by exactly one line.
- **But the declared fingerprint matches neither version.** Parent slice 39–52
  hashes to `c0dcb98f…`; the card declares `91d39149…`.

**Therefore the card was already stale before merge `80759036`**, and a +1 line
shift is *not* a sufficient repair. Re-fingerprinting would assert that the
current slice is what `OS01-01` is supposed to attest, which is a judgement about
the card's meaning, not a mechanical correction.

**Not repaired here, deliberately.** Needs the claim-card custody owner.
**Cost when it clears:** roughly thirty tests become informative for the first
time in an unknown period, and may then reveal real violations. Expect a second
wave; that is the gate working.

---

## Defect 2 — `reopened_ids` is used and never initialised (21 failures)

**Symptom.** `check_claim_status.py:705` — `NameError: name 'reopened_ids' is not
defined` (16 failures), plus `KeyError: 'reopened'` at
`test_claim_status.py:40` (5 failures).

**Diagnosis.** The name is read at `:705`, `:730` and `:732` and assigned
nowhere. It is **also absent from `1797138a`**, so this is not merge loss like
`PINNED_GRAVE_STATUS` was — it is newer, half-written work. The expected data
sections `reopened` and `restored` are likewise absent from the JSON the checker
reads.

**Not repaired here, deliberately.** Initialising the variable or fabricating the
data sections would mean inventing the semantics of somebody's unfinished
feature. Needs its author.

---

## Defect 3 — `finity_practice.yaml` schema version (3 failures)

**Symptom.** `compile_claim_cards.py:340` —
`00_META/claim_cards/finity_practice.yaml: expected claim-card-set/v2`.

**Diagnosis.** The card set declares a schema older than the compiler now
requires. Either the file needs migrating to `v2` or the compiler needs to accept
the older version. Which one is correct depends on whether `v2` added a required
field that this set genuinely lacks.

**Not repaired here.** Small, but it is a schema decision.

---

## Defect 4 — one `sha256` pin drift (1 failure)

**Symptom.** `test_finity_practice_gates.py` — declared pin
`468d7a37…` against actual `f3b1b71a…`, sourced from
`CLAIM_LIFECYCLE_INVENTORY.json`, on `01_TELEOLOGY/04_THE_LIVED_COMPASS.md`.

**Diagnosis.** Same class as Defect 1: a custody pin that no longer matches its
source. Same question — was the source change intended?

**Not repaired here.** Same reason.

---

## What WAS repaired this session

Six definitions lost in merge `80759036`, recovered verbatim from `1797138a`
with provenance comments in place:

- `check_claim_status.py` — `INVESTIGATION_STATES`, `PINNED_GRAVE_STATUS`
- `compile_claim_cards.py` — `_text_sha256`, `_located_text`,
  `_primary_checkout_root`, `_resolve_repo_path`, `_canonical_corpus_path`

Both files raised `NameError` on every run before this. Measured effect:
**65 failed / 63 passed → 61 failed / 67 passed.**

---

## Also found, not repaired — the file register is internally inconsistent

`00_META/registers/FILE_REGISTER.json` fails its own generator's `--check`:

```
entry_count=3445 but entries has 3519 rows
duplicate entry paths: 8, including
  09_TOOLS/01_SCRIPTS/check_generative_base.py, VMOSK_A.md,
  00_META/00_THE_CLAIM_STATUS_REGISTER.md
FOLDER_REGISTER.json: entry_count=795 but entries has 806 rows
```

So the register is not merely stale — its declared count disagrees with its own
contents, and it carries duplicates.

Regenerating with `--write` was attempted and **reverted**. It produced
**+132 / −49 entries across sixteen lanes**, which is corpus-wide maintenance
belonging to no single wave; the 49 removals are files other sessions moved or
archived. Committing that under this session's message would have been an
unattributed sweep. The regeneration is deterministic and reproducible in about
three minutes by anyone who owns it:

```bash
python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --write
```

Consequence in the meantime: the three artifacts created today
(`55_G2_PRIOR_ART_ADJUDICATION.md`, receipt `242_*`,
`check_g2_normal_form.py`) are **absent from the file register**. They are
recorded in `00_THE_RECORD_LEDGER.md`, which was updated.

---

## Recommended order

1. **Defect 1 first.** It is a single card and it is masking about thirty tests.
   Nothing downstream can be assessed until it clears, and clearing it will
   probably surface a second wave of real findings.
2. **Defect 3**, then **Defect 4** — both small, both decisions rather than
   typing.
3. **Defect 2** — needs its author; until then the claim-status contract runs
   only partially.
4. **The register** — a standalone maintenance commit, by whoever owns
   registration, not folded into feature work.

**None of these were caused by this session's work.** Verified: the six-file
subset returns identical counts with this session's changes present and reverted
to `HEAD` (65/63 both ways, before the symbol restoration improved it to 61/67).

**Canonical path:** `01_EMERGENTISM/00_HANDOFF/COMPILER_GATE_TRIAGE_2026_08_05.md`

•   ⊙   ○
