---
type: sourcing-protocol
id: SOURCING-PROTOCOL-v0
title: "Trial corpus sourcing & sealing protocol — quarantine pipeline for MID-series trials"
date: 2026-09-08
status: "[D] PROTOCOL — process definition, not a corpus, not a trial, not an authorization. Versioned; amendments dated and additive."
evidence_tier: "[S] the quarantine and independence fences (inherited from the prereg discipline); [D] the process steps"
may_sign: false
may_authorize: false
builds_toward: "00_ESTABLISHED.md §B rows MID-01/MID-02; 30_TRIAL/00_PREREG_SELFCORRECTION_MID03_v0.md §7"
---

# Trial corpus sourcing & sealing protocol v0

Closes the standing blocker named twice: MID-02's replication marker and
MID-03 §7 ("fresh out-of-domain corpus … requires a sourcing channel this
lane does not have unsigned"). Measured fact from MID-02: "out-of-domain"
means **out of the estate's semantic domain** — authored-for-trial synthetic
documents in foreign professional genres (economic, engineering, historical,
legal, medical), not web-fetched text. The channel that was missing is
therefore about **independence and freshness**, not retrieval.

## The pipeline (three zones, two fences)

```
sourcing/candidates/   ← anyone (unsigned) may add NEUTRAL documents + provenance sidecars
sourcing/rejected/     ← validator failures land here with their reason (never silently deleted)
(trial runs)           ← only an AUTHORIZED hand (K2 or K2-declared) may: select candidates,
                          plant flaws, freeze the sealed key, execute arms
```

**Fence 1 — quarantine:** nothing in `sourcing/` is a trial input. Candidates
carry **no planted defects** — planting is a seal-time act by the declared
planter, because who plants is part of the measurement's independence.

**Fence 2 — freshness:** a document whose sha256 appears in any frozen prior
corpus (MID-01 `30_TRIAL/corpus/`, MID-02 `30_TRIAL/mid02/corpus/`) is
rejected as a candidate. "Fresh" is checked mechanically, not asserted.

## Candidate format

Each candidate is a pair: `name.md` + `name.md.prov.json` (sidecar required,
else rejected):

```json
{
  "origin": "authored-for-trial | external",
  "title": "…",
  "genre": "one foreign professional genre (economic|engineering|historical|legal|medical|other)",
  "author_candidate": "who drafted this neutral text (a candidate may be unsigned-staged; the SEAL-TIME planter must still be declared by K2)",
  "external_provenance": "url/retrieval date/rights note — REQUIRED if origin=external, else omitted",
  "estate_distance_note": "one line: why this is outside the estate's semantic domain",
  "sha256": "must equal sha256(name.md)"
}
```

## Validator

`python3 30_TRIAL/sourcing/validate_intake.py` — checks every candidate pair:
sidecar present and parseable, required fields per origin, sha256 agreement,
freshness against both frozen corpora. PASS prints the candidate roster;
FAIL moves nothing and exits 1 with reasons (a candidate may be moved to
`rejected/` by hand, with its sidecar, per OUT.ARCHIVE — the validator never
deletes).

**Stated limits:** the validator proves provenance-completeness, hash
agreement, and freshness only. It cannot prove authorship independence,
genre distance (it reads the note, not the world), or absence of planted
defects in candidates — those are seal-time, authorized-hand
responsibilities. It is not a 20_CHECKS instrument member; it does not run
in `run_all.py`.

## What this protocol does NOT do

It does not authorize MID-03 (or any trial), does not plant, does not seal,
does not make any candidate eligible. It turns "no sourcing channel exists"
into: **the channel exists; it is waiting for an authorized hand at exactly
one gate — selection and sealing.**
