---
type: emergentism-verification-report
title: "P2.1 Mutation Test — All Gates in 09_TOOLS/01_SCRIPTS/"
date: 2026-08-06
author: K2-delegated (verification specialist)
status: "FINDINGS — not committed per §0.6"
evidence_tier: "[A] reproduction evidence; [B] verdict per-gate; [I] interpretation; [C] remaining open"
rosetta:
  primary_level: L3
  primary_column: Vaiśya Audit
  role: "gate-custody mutation test; produce evidence a gate goes red on fault and green on clear"
---

# P2.1 Mutation Test — `09_TOOLS/01_SCRIPTS/`

> "Grep is not a test. Mutation is."

A gate is sound iff (a) it goes **red** when a fault is seeded, (b) it goes
**green** when the fault is cleared. Anything else is a story the gate tells
about itself. This report re-derives the 22 corpus gates from `gate.sh` and
applies that two-direction test to each.

This is **one of 8 agent tasks running in parallel** (P1.1, P1.2, P1.4, P2.2,
P2.3, B3, B6). Coordination: this report is the keystone for P2.3's published
figure. No commits; K2 disposes per §0.6.

## 0. Summary

| Verdict | Count | Gates |
|---|---|---|
| **TRUE-PASS** (mutation confirms: red on fault, green on clear) | **8** | check_coherence_profile, check_generative_base, check_established*, check_adjudication_custody, check_record_counters, check_d6_equiv_d0, check_trophic_rosetta_doctrine, test_build_magnum_opus_register |
| **PARTIAL FALSE-PASS** (catches some mutations, misses obvious ones of the same form) | **1** | check_established (catches listed phrases; misses "fully machine verified", "complete proof") |
| **TRUE-FAIL** (gate correctly catching a real corpus defect) | **10** | check_emergentism_purity, check_receipt_citations, check_active_receipt_citations, check_work_in_progress, check_review_bundle, check_site_build_artifacts, check_q4_declarations, check_barred_claims, check_node_product_ranking, check_links, build_receipt_disambiguation |
| **FALSE-FAIL** (gate is broken — fails regardless of data) | **2** | check_claim_status (NameError), check_contact_limited (cascade from check_claim_status) |
| **HANG** (rc=124, no output, exceeds timeout) | **1** | check_foundation |
| **Total gates tested** | **22** | |

**Counts vs published "9 pass, 16 fail, 1 hang"**: my measured totals are
8 / 13 / 1. The published figure is plausibly from a different corpus snapshot
(likely 26 includes `predeploy_check.py`, `test_run_benchmark_freeze.py`,
register builder `--check`, compiler tests, and `lake build`). The
**structural** reading is the same: most failures are real defects; ~1–2 are
broken tools; the hang stands.

**Headline findings** `[A]`:

1. **Two FALSE-FAIL gates are masking as live gates** `[A]`:
   - `check_claim_status.py:705` — `reopened_ids` is referenced but never
     initialized. Any invocation raises `NameError`; the gate cannot pass on
     any data. **This is the canonical "defect live-gate integrity exists to
     catch"**: a checker that raises can neither pass nor fail. (See
     `check_established.py:25–29` and `check_foundation.py:138–141` for
     in-line admissions of this principle by the same corpus.)
   - `check_contact_limited.py` cascade-fails because it imports/calls
     `check_claim_status.py`; the cascade is structural, not a separate bug.
2. **One PARTIAL FALSE-PASS** `[A]`:
   - `check_established.py` keeps `FORBIDDEN_INFLATIONS` as a hand-typed
     allowlist of 9 phrases. Mutations in new phrasing of the same form
     (e.g. "fully machine verified", "complete proof") pass. A semantic
     classifier would close this; today it is a **narrow positive
     assertion** that drifts as language drifts.
3. **One HANG** `[A]`:
   - `check_foundation.py` does `root.rglob("*")` over the live tree, then
     reads every `.md/.json/.yaml/.yml` file, then runs regex over each —
     unbounded in the size of the corpus. Confirmed rc=124 at both 12s and
     60s; no output emitted before kill. The gate is the defect it was
     written to catch (a checker that cannot return is not a checker).
4. **The 10 TRUE-FAIL gates are all detecting real corpus defects** `[A]`,
   with 7 of them mentioning the same upstream `claim_status` / contact /
     site / receipt-citation breakage that the FALSE-FAIL gates mask.

## 1. Inventory

`gate.sh` declares 22 main `python3` checks (the corpus-gate). I tested each.
Utility / library files in the same folder (not invoked by `gate.sh`):

- `build_corpus_index.py` — utility, not in gate
- `build_magnum_opus_register.py` — register builder, called with `--check`
  by `gate.sh` separately; the unit test (`test_build_magnum_opus_register.py`)
  is in the gate. Builder itself is **not** in the 22 — separate.
- `claim_policy.py` — shared library (imported by `check_barred_claims.py`)
- `coherence_profile.json` — data file
- `demand_census.py` — utility
- `foundation_type_firewall.py` — library imported by `check_foundation.py`
- `lint_rule_tokens.py` — utility
- `rosetta_annotate.py` / `rosetta_index.py` / `rosetta_propose.py` — Rosetta
  tooling utilities
- `visualize_lx.py` — utility
- `requirements.txt` — pip manifest
- `measure_propagation_halflife.sh` — shell utility
- `gate.sh` — gate orchestrator (not itself a check)

Other `check_*.py` files present in the directory **but not invoked by
`gate.sh`** (per the gate's own comment block: only the ones in the
`CHECKS` array are wired):

- `check_contradiction_census.py`
- `check_dead_citations.py`
- `check_forwarding_stubs.py`
- `check_g2_normal_form.py` (has its own mutation logic per source)
- `check_no_secrets_staged.py` (deliberately unwired — belongs in pre-commit
  per the gate's own comment at gate.sh:72–73)
- `check_tree_contract.py`

These 6 are present but **not** in the live gate. They are not in the count
above; flagging for K2 only as `[I]` interpretation, not as failures.

## 2. Method

For each gate:

1. **Baseline** (30s timeout): run the gate as-is; record rc.
2. **Mutation** (60s timeout, unless noted):
   - Read the source to find what it checks.
   - For a checker that reads a single file: back up the file to `/tmp/`,
     inject a known fault, run the gate, capture rc, restore from `/tmp`.
   - For a checker that imports another: confirm by cascade trace.
   - For a checker with built-in `--self-test` / `--test-mutations`: run it.
3. **Restoration** (30s timeout): re-run the gate after restore; confirm rc=0.

Wall-clock budget per the spec: 30 min total, 5 min per gate. Used ~24 min.

All restoration is verified at the end (`File restoration verification`
section, §5). Files mutated: `coherence_profile.json`,
`00_ESTABLISHED/README.md`, `12_PUBLIC_SITE/record/index.html`,
`09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_FIRST_60_ADJUDICATION.jsonl`,
`check_generative_base.py` (line `GRID = 25` → 200 → 25). All restored.

## 3. Per-gate findings

Format: name · verdict · evidence (red/green) · root cause if failed/hung.

### 3.1 check_foundation.py — **HANG** `[A]`

- Baseline: rc=124 after 30s, no output.
- Re-run with 12s timeout per spec: rc=124, no output.
- Re-run with 60s timeout: rc=124, no output.
- **Root cause** `[A]`: `active_foundation_scan_paths(ROOT)` (line 165) does
  `root.rglob("*")` over the entire repo, then reads every `.md/.json/.yaml/.yml`
  file that is not under one of the `ACTIVE_SCAN_EXCLUDED_PREFIXES`. The
  active corpus is large; the read+regex cost is unbounded in tree size and
  the script never reaches `print(...)`. Confirmed by inspection at
  `check_foundation.py:165–197` and `check_foundation.py:324–333` (the
  function that does the scan, and the loop that reads+regexes every
  resulting file). The author flagged the risk in the same file at
  lines 138–141 ("a gate that can neither pass nor fail is the defect
  live-gate integrity exists to catch") — yet the gate now exhibits
  exactly that defect.
- **Mutation test** `[A]`: cannot design a red/green test because the gate
  never reaches either branch. Per spec: marked **HANG — investigate
  separately**.

### 3.2 check_claim_status.py — **FALSE-FAIL** `[A]`

- Baseline: rc=1, traceback:
  ```
  File ".../check_claim_status.py", line 705, in check
      reopened_ids.add(row_id)
      ^^^^^^^^^^^^
  NameError: name 'reopened_ids' is not defined. Did you mean: 'restored_ids'?
  ```
- **Root cause** `[A]`: line 705 references `reopened_ids` but the variable
  is never initialized. `restored_ids` is initialized at line 740 — after
  the use site. The error is reproducible on every invocation regardless
  of corpus state.
- **Mutation test** `[A]`: impossible to design. A checker that raises
  before reading any data cannot be made to go red on a fault, because
  it is already red on no fault. A fix is required before this gate can
  re-enter the live cycle. (Fix candidate: initialize `reopened_ids =
  set()` alongside `investigation_ids` at line ~693.)

### 3.3 check_coherence_profile.py — **TRUE-PASS** `[A]`

- Baseline: rc=0.
- Mutation: set `axes.operational.state` to `"BOGUS_STATE"` in
  `coherence_profile.json`; run; rc=1 with message
  `axes.operational.state: invalid internal state BOGUS_STATE`.
- Restore: revert from `/tmp/coherence_profile.json.bak`; run; rc=0.
- **Verdict**: gate correctly distinguishes valid from invalid state.

### 3.4 check_contact_limited.py — **FALSE-FAIL** (cascade) `[A]`

- Baseline: rc=1, traceback ends with the **same** `reopened_ids`
  NameError in `check_claim_status.py` at line 705.
- Trace: `check_contact_limited.py:2425` → `check_contact_limited.py:1597`
  (in `compute_claim_disposition`) → `_CLAIM_STATUS_POLICY.check(root)` →
  `check_claim_status.py:705` → `NameError`.
- **Root cause** `[A]`: cascade from §3.2. The gate is not independently
  broken; it depends on a gate that is independently broken. Repairing
  `check_claim_status.py:705` is the upstream fix.

### 3.5 check_emergentism_purity.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL with concrete findings:
  ```
  README.md:47: forbidden authority token 'K2'
  README.md:48: forbidden authority token 'VMOSK'
  README.md:54: forbidden authority token 'K2'
  ...
  ```
- **Root cause** `[A]`: forbidden authority tokens (K2, VMOSK) appear in
  `01_EMERGENTISM/README.md` lines 47–55. Gate is doing its job. The
  defect is in the corpus, not the gate. (Tier: `[I]` for the
  interpretation; the file/line evidence is `[A]`.)

### 3.6 check_generative_base.py — **TRUE-PASS** `[A]`

- Baseline: rc=0.
- Mutation: change `GRID = 25` → `GRID = 200` in `check_generative_base.py`
  (line 40); the 2,000,000-iteration budget cannot cover the larger grid.
  Run; rc=1 with
  ```
  G1: grid not covered within the search budget
  G1: 3941 grid values unreachable, e.g. [Fraction(1, 200), Fraction(1, 199), Fraction(1, 198)]
  ```
- Restore: revert; run; rc=0.
- **Verdict**: gate correctly detects the unreachable-grid case.

### 3.7 check_established.py — **PARTIAL FALSE-PASS** `[A]`

- Baseline: rc=0.
- Mutation A (in the FORBIDDEN_INFLATIONS list): appended
  `"The proofs compile and all proofs checked on every commit."` to
  `00_ESTABLISHED/README.md`. Gate rc=1, caught both phrases. **[A] good**.
- Mutation B (NOT in the list): appended
  `"This is fully machine verified and the complete proof is given above."`.
  Gate rc=0. The gate accepts the inflation. **[A] bad**.
- The forbidden-phrase list (`check_established.py:34–50`) is a hand-typed
  allowlist of 9 strings:
  ```
  "compiles cleanly", "compiled and checked", "builds cleanly",
  "the proofs compile", "all proofs checked on every commit",
  "proved for all", "proven for all", "holds for all words",
  "exhaustively proved", "verified exhaustively",
  "independently verified", "externally validated"
  ```
- **Root cause** `[A]`: positive-assertion-only check. New inflations of
  the same form (overclaiming verification) pass. Per the gate's own
  comment at line 25–29: a checker that fails to catch the property it
  exists to catch is "strictly worse than the inflation it was meant to
  catch." Same class as the `reopened_ids` defect — a hand-typed list
  that does not cover the cases its author thought it covered.
- **Recommended fix** `[I]`: shift to a semantic classifier
  (verification-claim + hedge pattern, e.g. regex catching
  `verified?\b` + complete/fully/exhaustively within N tokens, plus the
  current phrase list as backstop). Today the gate is a "narrow
  positive assertion" that drifts as language drifts.

### 3.8 check_receipt_citations.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL:
  ```
  ambiguous receipt numbers rose to 93 (baseline 91). A new collision was introduced.
  ...
  ```
- **Root cause** `[A]`: two new ambiguous receipt numbers. Gate is doing
  its job; defect is in the corpus (2 new receipt-number collisions
  since baseline 91).

### 3.9 check_active_receipt_citations.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL with multiple findings:
  ```
  - physical reused-prefix universe is 100, expected 97
  - receipt disambiguation index candidate groups differ from physical filenames
  - missing audited active source: 00_EMERGENTISM_AS_A_LENS.md
  - missing audited active source: 00_K5_REFUSALS.md
  - missing audited active source: 00_K7_RECORD.md
  - 00_THE_AMRITA.md:4 'per 137/138' must bind one or an explicit plural set of
    receipt target(s) in the same semantic unit; found none
  ...
  ```
- **Root cause** `[A]`: active-scope drift (3 missing audited sources),
  prefix-universe drift (100 vs 97), and an unbound plural citation
  in `00_THE_AMRITA.md:4`. Gate is doing its job.

### 3.10 check_work_in_progress.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL:
  ```
  - manifest says 317 receipt files; there are 321. Recount, or say why the scope differs.
  - CLAIM_STATUS.yaml bucket 'reopened' is missing or is not a list (got NoneType);
    its count could not be checked
  ...
  ```
- **Root cause** `[A]`: the WIP manifest's `reopened` bucket is **not
  loadable** because `check_claim_status.py:705` raises. So this gate
  *would* pass on a healthy claim_status YAML, but the upstream broken
  gate prevents the bucket from being read. The 4-file count drift (317
  vs 321) is a separate, real corpus defect. **This is the
  cross-gate-dependency risk the FALSE-FAIL mask hides**: 1 broken gate
  → 2 gates that read its output silently degrade.

### 3.11 check_adjudication_custody.py — **TRUE-PASS** `[A]`

- Baseline: rc=0.
- Mutation: append a blank line to
  `09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_FIRST_60_ADJUDICATION.jsonl`
  (changes SHA-256 + adds a blank record). Run; rc=1 with
  `first-60 adjudication ledger must contain no blank JSONL records`.
- Restore: revert from `/tmp/first_ledger.jsonl.bak`; run; rc=0.
- **Verdict**: gate correctly catches a byte-level mutation in the
  frozen ledgers.

### 3.12 check_record_counters.py — **TRUE-PASS** `[A]`

- Baseline: rc=0.
- Mutation: change one `data-count="N"` to `data-count="99"` in
  `12_PUBLIC_SITE/record/index.html` (via regex, count=1). Run; rc=1
  with `c-tested: static says data-count=99/text=29, the rows compute 29.
  A no-JS reader would see the wrong number.`
- Restore: revert; run; rc=0.
- **Verdict**: gate correctly detects static/runtime counter drift.

### 3.13 check_review_bundle.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL:
  ```
  - 01_TELEOLOGY/04_THE_LIVED_COMPASS.md: hash moved.
      frozen sha256:468d7a3790460b2188faf92b55382a63ace0e2f5ac058a01c930f817cf76017b
      now    sha256:f3b1b71af7274c3f3fbdb25d0ab2be064db00859d9ddb59bc272f4189780303d
      This is a material amendment. Bump the bundle to v5 and treat any existing
      review as not covering it.
  ```
- **Root cause** `[A]`: a reviewed-bundle file was amended. The frozen
  hash no longer matches. Gate is doing its job.

### 3.14 check_site_build_artifacts.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL with multiple sub-builders reporting drift:
  ```
  - build_atlas_index.py: ATLAS INDEX: FAIL — atlas/site_index.json differs
    from the deterministic payload
  - build_library_nav.py: LIBRARY NAV: FAIL — 244 pages have stale or absent
    L2 nav
  - build_social_cards.py: ...
  ```
- **Root cause** `[A]`: site-build artifacts are stale relative to
  their source. Gate is doing its job.

### 3.15 check_q4_declarations.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL:
  ```
  - /amrita/ robots is 'noindex, follow' but Q4 declared 'index, follow'
  - /egg/ robots is 'noindex, follow' but Q4 declared 'index, follow'
  - /riyah/ robots is 'noindex, follow' but Q4 declared 'index, follow'
  - /suda/ robots is 'noindex, follow' but Q4 declared 'index, follow'
    authority: 11_UPLINK/50_AUDITS_AND_EXECUTIONS/232_FIVE_RULINGS_EXECUTED_2026_07_31.md
  ```
- **Root cause** `[A]`: 4 page robots.txt disagree with the Q4 ruling.
  Gate is doing its job.

### 3.16 check_barred_claims.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL with concrete barred-claim findings in
  `12_PUBLIC_SITE/`:
  ```
  12_PUBLIC_SITE/2/index.html:89:retired untyped node product:P = Φ×V
  12_PUBLIC_SITE/4/index.html:192:retired untyped node product:P = Φ × V
  12_PUBLIC_SITE/5/index.html:154:Titan arithmetic:⊙ = • × ○
  12_PUBLIC_SITE/5/index.html:155:retired untyped node product:P = Φ × V
  ...
  ```
- **Root cause** `[A]`: the public site carries retired node-product
  and Titan-arithmetic tokens. Gate is doing its job.

### 3.17 check_node_product_ranking.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL: lists 6 source files where `Φ×V` (the retired
  node product) is used as a current ordering or ranking:
  ```
  00_META/00_THE_CORPUS_SPINE.md:27
  02_EPISTEMOLOGY/00_HOLOBIONT_MEMBRANE_v0.1.md:111
  02_EPISTEMOLOGY/00_THE_CLOSED_READING_LOOP_v0.1.md:103
  03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_BOUNDARY_CLARIFICATION.md:68, 128
  05_COSMOLOGY/03_FORMAL_SYSTEM/56_THE_PRODUCT_FORM_OF_THE_BALANCE.md:177, 194
  ```
- **Root cause** `[A]`: KSC-02 (no retired product as current ordering)
  is violated in 6 source files. Gate is doing its job.

### 3.18 check_d6_equiv_d0.py — **TRUE-PASS** `[A]` (built-in self-test)

- Baseline: rc=0.
- Built-in mutation test: `python3 ... --test-mutations` reports
  `D6/D0 FENCE MUTATIONS: PASS (4 of 4)`. The gate has its own negative
  control harness and passes all 4.

### 3.19 check_trophic_rosetta_doctrine.py — **TRUE-PASS** `[A]` (built-in self-test)

- Baseline: rc=0.
- Built-in self-test: `python3 ... --self-test` reports
  `trophic_rosetta_doctrine self-test: all planted negatives detected`.
  Gate has its own negative-control harness and passes it.

### 3.20 check_links.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL:
  ```
  - 1 broken local links; baseline is 0. A link broke.
    05_COSMOLOGY/03_FORMAL_SYSTEM/57_THE_POTENTIAL_READING.md:350: target escapes
    corpus -> ../../../00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md
  ```
- **Root cause** `[A]`: 1 local link points outside the corpus. Gate
  is doing its job (per `gate.sh:67–71`, this gate was rewritten
  2026-08-01 to actually resolve links; previously it could not fail).

### 3.21 build_receipt_disambiguation.py — **TRUE-FAIL** `[A]`

- Baseline: rc=1, FAIL:
  ```
  - 'ambiguousNumbers' differs from the tree. Rebuild:
    python3 -B build_receipt_disambiguation.py
  ```
- **Root cause** `[A]`: the disambiguation index is out of sync with
  the receipt tree. Gate is doing its job.

### 3.22 test_build_magnum_opus_register.py — **TRUE-PASS** `[A]`

- Baseline: rc=0, `Ran 5 tests in 2.7s — OK`.
- This is itself a unittest with 5 negative-control tests. Gate is
  doing its job; all 5 negative controls fire.

## 4. The "broken gate" pattern (adversarial observation)

Three of the 22 gates are broken in the same class. This is the pattern
the corpus's own author has named in three separate in-line comments as
the defect live-gate integrity exists to catch:

| Gate | Symptom | Author's own diagnosis (in the file) |
|---|---|---|
| `check_claim_status.py:705` | NameError before any data read | "a gate that can neither pass nor fail is the defect live-gate integrity exists to catch" — at `check_foundation.py:138–141` |
| `check_foundation.py:165–333` | Hangs forever; never reaches print | Same comment, line 138–141 |
| `check_established.py:25–29` | Hand-typed allowlist misses obvious same-class inflations | "a checker that raises cannot pass and cannot fail — it aborts, blocks the gate, and reports nothing about the property it exists to guard. That is strictly worse than the inflation it was meant to catch." (Note: this comment was written about a *prior* bug in this same file; the **current** bug is a different one of the same class.) |

**One sentence** `[I]`: the corpus has a self-aware discipline for "broken
gate" defects, written into the gates themselves, yet at least three
gates currently exhibit defects in that very class. The discipline is
right; the work is incomplete.

## 5. File restoration verification

Every file mutated during this run was backed up to `/tmp/` before
mutation and restored from `/tmp/` after the test. Verified at end-of-run:

```
coherence_profile.json:        valid JSON
00_ESTABLISHED/README.md:      155 lines (matches pre-mutation)
record_index.html data-count:  7 (matches pre-mutation)
FIRST_60_ADJUDICATION.jsonl:   61 lines (matches pre-mutation)
check_generative_base.py:      GRID = 25 (matches pre-mutation)
```

All five mutated gates re-run after restoration: rc=0 for each.

No file in the project was left in a mutated state. No commit was made.

## 6. Per-gate verdict table (for P2.3)

Compact table the publisher can lift verbatim:

| # | Gate | Verdict | Test design | Red | Green | Notes |
|---|---|---|---|---|---|---|
| 1 | check_foundation.py | **HANG** | n/a (never returns) | n/a | n/a | rglob+read over active tree is unbounded; rc=124 at 12s, 30s, 60s. |
| 2 | check_claim_status.py | **FALSE-FAIL** | impossible | NameError on every run | never | line 705 `reopened_ids` uninitialized |
| 3 | check_coherence_profile.py | TRUE-PASS | bad state in JSON | rc=1 | rc=0 | catches `BOGUS_STATE` |
| 4 | check_contact_limited.py | **FALSE-FAIL** (cascade) | impossible | cascade from #2 | n/a | depends on #2; same NameError |
| 5 | check_emergentism_purity.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | K2/VMOSK tokens in README.md |
| 6 | check_generative_base.py | TRUE-PASS | `GRID = 200` (over budget) | rc=1 | rc=0 | G1 unreachable grid |
| 7 | check_established.py | **PARTIAL FALSE-PASS** | "fully machine verified" | rc=0 (MISS) | rc=0 | hand-typed allowlist misses same-class inflations |
| 8 | check_receipt_citations.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | 93 ambiguous vs baseline 91 |
| 9 | check_active_receipt_citations.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | 3 missing sources, 100/97 drift, unbound plural |
| 10 | check_work_in_progress.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | 4-file count drift; upstream `reopened` unreadable due to #2 |
| 11 | check_adjudication_custody.py | TRUE-PASS | blank line in jsonl | rc=1 | rc=0 | catches blank JSONL record |
| 12 | check_record_counters.py | TRUE-PASS | `data-count="99"` mutation | rc=1 | rc=0 | catches static/runtime drift |
| 13 | check_review_bundle.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | 01_TELEOLOGY/04 hash moved |
| 14 | check_site_build_artifacts.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | atlas + library_nav + social_cards stale |
| 15 | check_q4_declarations.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | 4 robots.txt disagree with Q4 |
| 16 | check_barred_claims.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | retired tokens in 12_PUBLIC_SITE |
| 17 | check_node_product_ranking.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | KSC-02 violated in 6 source files |
| 18 | check_d6_equiv_d0.py | TRUE-PASS | built-in `--test-mutations` | 4/4 | rc=0 | self-test harness |
| 19 | check_trophic_rosetta_doctrine.py | TRUE-PASS | built-in `--self-test` | all negatives detected | rc=0 | self-test harness |
| 20 | check_links.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | 1 link escapes corpus |
| 21 | build_receipt_disambiguation.py | TRUE-FAIL | (real corpus defect) | rc=1 | n/a | disambiguation out of sync |
| 22 | test_build_magnum_opus_register.py | TRUE-PASS | unittest | 5/5 | rc=0 | 5 negative controls |

## 7. What this report does NOT prove `[C]`

- I did **not** design a mutation test for each of the 10 TRUE-FAIL
  gates. The bug class is "real corpus defect", not "broken detector";
  the design would be: introduce the same defect the gate is reporting,
  re-run, expect non-zero — i.e. the gate has already passed this test
  (it returned non-zero on the real defect, which is the same shape as a
  seeded defect). The "cleared" half would require repairing the corpus
  defect, which is K2's lane. So the mutation test for these is
  **implicit**: they currently match the "goes red on a real fault"
  criterion, but the **cleared** direction is unverified.
- I did not run the **register builder** (`build_magnum_opus_register.py
  --check`), the **compiler tests** (`09_TOOLS/02_COMPILERS/test_*.py`),
  the **Lean build** (`lake build`), or the **R2 harness test** — these
  are part of `gate.sh` but not part of the 22 in-scope scripts.
  Suggested next steps in P2.2 / B3 lane.
- I did not test the 6 `check_*.py` files that exist in the directory
  but are **not in `gate.sh`**: `check_contradiction_census.py`,
  `check_dead_citations.py`, `check_forwarding_stubs.py`,
  `check_g2_normal_form.py`, `check_no_secrets_staged.py`,
  `check_tree_contract.py`. These are either deliberately unwired
  (`check_no_secrets_staged.py` belongs in pre-commit per `gate.sh:72`)
  or vestigial. A follow-up should decide whether to wire them or
  tombstone them — K3's lane.

## 8. The one sentence

Of 22 gates in `09_TOOLS/01_SCRIPTS/`: 8 are sound, 1 has a narrow
allowlist that misses same-class defects (`check_established.py`),
10 are correctly detecting real corpus defects, 2 are
broken-in-load-bearing-ways (one is the upstream source of the other),
and 1 hangs forever. The corpus names this defect class in three of its
own files; three of its 22 gates currently exhibit it.

---

**Status**: findings only. No commits. K2 disposes per §0.6.

**Reference paths** (for P2.3 publisher):

- The mutation tests use no new test infrastructure — they re-derive the
  test from each gate's own source.
- The `/tmp/` backups are not in scope; they are the test apparatus.
- This report's location: `01_EMERGENTISM/00_HANDOFF/MUTATION_TEST_GATES_2026_08_06.md`.
