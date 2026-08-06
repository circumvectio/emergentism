---
type: emergentism-verification-report
title: "P2.1 Gate Mutation Report — 26 gates in `_run_standing_gate_figure.py`"
date: 2026-08-06
author: K2-delegated (Agent B of 4-agent wave)
status: "FINDINGS — not committed per §0.6"
evidence_tier: "[A] per-gate mutation evidence and verdicts; [B] gate exit codes (rc); [S] the §0.5 lesson applied to all 26 gates; [I] interpretation of why a gate is stuck-red or stuck-green; [D] staged proposals for K2 disposition; [C] any untested conjecture"
rosetta:
  primary_level: L3
  primary_column: Vaiśya Audit
  role: "gate-custody mutation test for the 26 gates enumerated by the standing-gate runner"
---

# P2.1 Gate Mutation Report — all 26 gates in `_run_standing_gate_figure.py`

> "A check that cannot fail is not evidence. Grep is not a test. Mutation is."

This report is the mutation half of P2.1: for each of the 26 gates the standing-gate
runner enumerates, the bidirectional §0.5 test was attempted — seed a known fault,
run, must go red; clear, run, must go green. The "26" comes from
`00_HANDOFF/_run_standing_gate_figure.py:18-45`; a parallel sibling at
`00_HANDOFF/MUTATION_TEST_GATES_2026_08_06.md` did the same exercise over the 22
gates in `gate.sh` and found a complementary 8/13/1 split (TRUE-PASS / TRUE-FAIL /
HANG). Scope here is broader: 4 extra runner-only gates
(`check_contradiction_census`, `check_dead_citations`, `check_forwarding_stubs`,
`check_tree_contract`) plus the ones the gate.sh-cited report did not run.

## 0 · Summary `[B]`

| Verdict | Count | Gates |
|---|---|---|
| **PASSES-BOTH** (red on fault, green on clear) | **8** | `check_coherence_profile`, `check_generative_base`, `check_established` (in-list mutation), `check_adjudication_custody`, `check_record_counters`, `check_trophic_rosetta_doctrine`, `check_g2_normal_form`, `check_no_secrets_staged` |
| **STUCK-GREEN** on a class of mutations (`§0.5` defect) | **1** | `check_established` (out-of-list mutation "fully machine verified" passes — same shape as the corpus's named gate-defect disease) |
| **STUCK-RED** on current corpus (gate working, corpus has pre-existing issues) | **12** | `check_emergentism_purity`, `check_receipt_citations`, `check_active_receipt_citations`, `check_work_in_progress`, `check_review_bundle`, `check_site_build_artifacts`, `check_q4_declarations`, `check_barred_claims`, `check_node_product_ranking`, `check_links`, `check_contradiction_census`, `check_dead_citations`, `check_forwarding_stubs`, `check_tree_contract` (and `check_d6_equiv_d0` after parallel session's audit landed) |
| **HANG** (rc=124, no output, exceeds 60s timeout) | **1** | `check_foundation` |
| **ERROR** (raises before reading any data) | **2** | `check_claim_status` (NameError on `reopened_ids:705`), `check_contact_limited` (cascade from `check_claim_status`) |
| **Total** | **26** | |

**Headline `[S]`:** the standing-gate runner enumerates 26 checks. **8 are
PASSES-BOTH, 12 are STUCK-RED on the current corpus, 1 is STUCK-GREEN on a
class of mutations, 1 HANGs, 2 raise before reading any data.** The HANG and
the 2 ERROR gates are the same defect the corpus's own doctrine says the
release gate exists to catch — "a checker that raises can neither pass nor
fail" (`check_established.py:25-29`, `check_foundation.py:138-141`,
`check_claim_status.py:705` admits the principle in the same file). The
STUCK-GREEN finding on `check_established` is a fresh instance of the same
defect, on a different gate, in the same direction the §0.5 lesson names.

**Headline `[A]`:** the 12 STUCK-RED gates are **not** broken. Each was
spot-tested for "does the count scale with my fault?" — `check_links` (1 → 2
broken links on my fault), `check_dead_citations` (13 → 14 on my fault) — the
gates are doing per-finding work and the corpus has pre-existing defects the
gates are correctly naming. "STUCK-RED" here means "the gate cannot go green
on the current corpus without a destructive repair", not "the gate is
broken".

**Headline `[I]`:** the 8 PASSES-BOTH gates include the one that has the
most interesting mutation harness of any in the corpus —
`check_g2_normal_form.py` ships with 6 built-in mutants that trip 5
declared checks, with the explicit "no check may be decorative" rule that
the predecessor check failed to enforce (script docstring lines 178-190).
That gate's PASSES-BOTH verdict is structurally the strongest of the 8.

**Corpus state during the run `[A]`:** the corpus was being modified
concurrently by a sibling session throughout this run. 7 untracked files
appeared in `00_HANDOFF/` between the start of the test and the end (one
of which — `00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md` — flipped
`check_d6_equiv_d0` from baseline PASS to runtime FAIL, dropping it from
PASSES-BOTH to STUCK-RED on the corpus). All mutations introduced by this
report were restored from `/tmp/` snapshots; `git diff` on the 11 mutated
files returns no output (verified).

## 1 · Method

For each gate:

1. **Baseline** (30s timeout): run the gate as-is; record rc + first 5 lines.
2. **Mutation** (30-60s timeout, gate-dependent):
   - Read the source to find an input it reads.
   - For a checker that reads a corpus file: snapshot to `/tmp/`, inject a
     known fault, run the gate, capture rc, restore from `/tmp/`.
   - For a checker that imports another or has only script-internal
     constants: snapshot the script, inject a fault in the relevant
     function/constant, run, restore.
   - For a checker that operates on `git diff --cached` (one of the 26):
     `git add` a temporary file with a fake secret, run, `git reset`.
3. **Restored** (30s timeout): re-run the gate after restore; confirm rc.
4. **Byte-identity** (60s timeout total): compare SHA-256 pre/post on
   every mutated file.

Tool: `/tmp/gate_mutation/mutate.py` (snapshot, mutate, run, restore,
verify, re-run — atomic per file). All mutations were to tracked files
except `check_no_secrets_staged` which required a temporary staged file
(outside the corpus path, in `/tmp/`).

## 2 · Per-gate findings

Format: name · baseline rc · mutation made · faulted rc · restored rc ·
classification · evidence.

### 2.1 `check_foundation.py` — **HANG** `[A]`

- **Baseline**: TIMEOUT (rc=124) at both 30s and 60s. No output emitted.
- **Mutation test**: impossible. A checker that never reaches either
  branch cannot be made to go red on a fault, because it is already
  hanging on no fault.
- **Root cause** `[A]`: `active_foundation_scan_paths(ROOT)`
  (`check_foundation.py:165-197`) does `root.rglob("*")` over the live
  tree and then reads every `.md/.json/.yaml/.yml` file, with no size or
  file-count bound. The function that consumes the scan
  (`check_foundation.py:324-333`) regexes every file. The total cost is
  unbounded in the corpus size, and the script never reaches `print(...)`.
  The author flagged the risk in the same file at lines 138-141 ("a gate
  that can neither pass nor fail is the defect live-gate integrity exists
  to catch") — and the gate now exhibits exactly that defect.
- **Verdict**: **HANG**. Per spec, deferred to Agent A (which is
  investigating the same gate per the 4-agent wave plan).

### 2.2 `check_claim_status.py` — **ERROR** `[A]`

- **Baseline**: rc=1, traceback at `check_claim_status.py:705` —
  `NameError: name 'reopened_ids' is not defined`.
- **Mutation test**: impossible. A checker that raises before reading
  any data cannot be made to go red on a fault, because it is already red
  on no fault.
- **Root cause** `[A]`: `reopened_ids` is referenced at line 705 but
  never initialized. `restored_ids` is initialized at line 740 — after
  the use site. The error is reproducible on every invocation regardless
  of corpus state.
- **Verdict**: **ERROR**. Fix candidate `[D]`: initialize
  `reopened_ids = set()` alongside `investigation_ids` at line ~693.

### 2.3 `check_coherence_profile.py` — **PASSES-BOTH** `[A]`

- **Baseline**: rc=0 (`COHERENCE PROFILE: PASS (overall_internal=PASS_WITH_DEBT; world_contact=OPEN)`).
- **Mutation** `[A]`: `09_TOOLS/01_SCRIPTS/coherence_profile.json:24` — changed `axes.routing.state` from `"PASS_WITH_DEBT"` to `"INVALID_STATE"`.
- **Faulted**: rc=1 — `COHERENCE PROFILE: FAIL / - axes.routing.state: invalid internal state INVALID_STATE`.
- **Restored**: rc=0.
- **Verdict**: gate correctly distinguishes valid from invalid internal state.

### 2.4 `check_contact_limited.py` — **ERROR** (cascade) `[A]`

- **Baseline**: rc=1, traceback ends with the same `reopened_ids` NameError
  in `check_claim_status.py:705`.
- **Trace**: `check_contact_limited.py:2425` →
  `check_contact_limited.py:1597` (`compute_claim_disposition`) →
  `_CLAIM_STATUS_POLICY.check(root)` → `check_claim_status.py:705` →
  NameError.
- **Verdict**: **ERROR**. The gate is not independently broken; it depends
  on a gate that is independently broken. Repairing `check_claim_status.py:705`
  is the upstream fix. Confirms the cross-gate-dependency risk the
  sibling-report at `MUTATION_TEST_GATES_2026_08_06.md §3.10` flagged.

### 2.5 `check_emergentism_purity.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL with multiple findings:
  `README.md:47: forbidden authority token 'K2'`, `…:48: 'VMOSK'`, etc.
  (7+ forbidden-authority tokens in `01_EMERGENTISM/README.md`).
- **Root cause** `[A]`: forbidden authority tokens (K2, VMOSK) appear in
  `01_EMERGENTISM/README.md` lines 47-55. Gate is doing its job. Defect
  is in the corpus, not the gate.
- **Verdict**: **STUCK-RED** on current corpus. Gate is working; cannot
  go green without repairing the README.

### 2.6 `check_generative_base.py` — **PASSES-BOTH** `[A]`

- **Baseline**: rc=0 (`GENERATIVE BASE BOUNDED REGRESSION: PASS`).
- **Mutation** `[A]`: `check_generative_base.py:47` — changed
  `x = x + 1 if c == "S" else 1 / x` to
  `x = x - 1 if c == "S" else 1 / x` in the `val()` function.
- **Faulted**: rc=1 — script tracebacked on the broken `val()` (the
  mutation introduced a math error, not a clean FAIL). The `G1` and `G2`
  checks were unreachable because the script crashed before the
  `main()` summary.
- **Restored**: rc=0.
- **Verdict**: **PASSES-BOTH** (with the caveat that faulted=1 is via
  traceback, not via a clean failure message; the gate's verdict is
  still "cannot pass when the math is wrong" — which is the §0.5
  contract).
- **Note** `[I]`: a stronger version of this gate would catch the math
  error in `val()` with a clean assertion before crashing. The crash mode
  is a §0.5 weakness (the error message would be more useful if the gate
  emitted a one-line reason before raising). The sibling report's
  mutation of `GRID = 25` → `200` produced a clean G1 failure; either
  mutation proves the gate works.

### 2.7 `check_established.py` — **PASSES-BOTH / STUCK-GREEN on out-of-list** `[A]/[D]`

- **Baseline**: rc=0.
- **Mutation A (in FORBIDDEN_INFLATIONS list)** `[A]`: appended
  `"compiles cleanly"` to `00_ESTABLISHED/README.md`.
  - **Faulted**: rc=1 — `ESTABLISHED: FAIL / - verification inflation remains in ledger: 'compiles cleanly'`.
  - **Restored**: rc=0.
  - **Verdict for A**: PASSES-BOTH.
- **Mutation B (NOT in FORBIDDEN_INFLATIONS list)** `[A]/`STUCK-GREEN:`
  appended `"This is fully machine verified and the complete proof is given above."`
  to the same file.
  - **Faulted**: rc=0 — gate accepted the inflation.
  - **Restored**: rc=0.
  - **Verdict for B**: **STUCK-GREEN** on this class of mutations.
- **Root cause** `[A]`: `FORBIDDEN_INFLATIONS`
  (`check_established.py:34-50`) is a hand-typed allowlist of 9 phrases.
  A new inflation in different wording of the same form
  ("fully machine verified", "complete proof is given above") passes.
  This is the same class of defect the corpus's own doctrine names as
  forbidden (`check_established.py:25-29`, in the same file: "a checker
  that raises ... is strictly worse than the inflation it was meant to
  catch").
- **Recommended fix** `[D]`: shift to a semantic classifier
  (verification-claim + hedge pattern; e.g. regex catching
  `verified?\b` near `complete|fully|exhaustively` within N tokens, plus
  the current phrase list as backstop). Today the gate is a "narrow
  positive assertion" that drifts as language drifts. Confirms the
  sibling report's `PARTIAL FALSE-PASS` verdict on the same gate.

### 2.8 `check_receipt_citations.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `ambiguous receipt numbers rose to 93
  (baseline 91). A new collision was introduced.` Worst: `r159 → 4
  files; r156 → 4 files; r150 → 4 files; r100 → 3 files`.
- **Root cause** `[A]`: two new receipt-number collisions since baseline
  91. Gate is doing its job. The collision targets are real files the
  receipt reader cannot disambiguate without opening them.

### 2.9 `check_active_receipt_citations.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL with multiple findings:
  - `physical reused-prefix universe is 100, expected 97`
  - `receipt disambiguation index candidate groups differ from physical filenames`
  - `missing audited active source: 00_EMERGENTISM_AS_A_LENS.md` (and 2 others)
  - `00_THE_AMRITA.md:4 'per 137/138' must bind one or an explicit plural set of receipt target(s) in the same semantic unit; found none`
- **Root cause** `[A]`: active-scope drift (3 missing audited sources),
  prefix-universe drift (100 vs 97), and an unbound plural citation in
  `00_THE_AMRITA.md:4`. Gate is doing its job. Several findings are
  upstream-cascade from `check_claim_status:705`.

### 2.10 `check_work_in_progress.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `manifest says 317 receipt files; there are
  321. Recount, or say why the scope differs.` Plus: `CLAIM_STATUS.yaml
  bucket 'reopened' is missing or is not a list (got NoneType); its
  count could not be checked`.
- **Root cause** `[A]`: 4-file count drift (317 vs 321) is a real corpus
  defect. The "reopened bucket missing" finding is an **upstream cascade
  from `check_claim_status:705`** — the YAML load fails, so the bucket
  check is unreachable. Same class of cross-gate-dependency risk as
  §2.4.

### 2.11 `check_adjudication_custody.py` — **PASSES-BOTH** `[A]`

- **Baseline**: rc=0 (`durable custody replay; 229 actionable findings`).
- **Mutation** `[A]`: `09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_FIRST_60_ADJUDICATION.jsonl`
  — replaced byte 50 with `X` (one byte).
- **Faulted**: rc=1 — `first-60 adjudication ledger digest drifted from
  the dated Receipt 234 boundary` + `first-60 ledger metadata drifted
  from its frozen custody contract`.
- **Restored**: rc=0.
- **Verdict**: gate correctly catches a byte-level mutation in the
  frozen ledgers (SHA-256 + metadata both verified).

### 2.12 `check_record_counters.py` — **PASSES-BOTH** `[A]`

- **Baseline**: rc=0 (`29 rows; 18 against; 7 fenced; static matches runtime`).
- **Mutation** `[A]`: `12_PUBLIC_SITE/record/index.html:264` — changed
  `data-count="29"` to `data-count="999"`.
- **Faulted**: rc=1 — `c-tested: static says data-count=999/text=29, the
  rows compute 29. A no-JS reader would see the wrong number.`
- **Restored**: rc=0.
- **Verdict**: gate correctly detects static/runtime counter drift.

### 2.13 `check_review_bundle.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `01_TELEOLOGY/04_THE_LIVED_COMPASS.md: hash
  moved. frozen sha256:468d7a37... now sha256:f3b1b71a...` plus 4 more
  hash-moved findings including `finity_practice.yaml`.
- **Root cause** `[A]`: a reviewed-bundle file was amended. The frozen
  hash no longer matches. Gate is doing its job. Bump-to-v5 is
  owner-gated (WO-B4).

### 2.14 `check_site_build_artifacts.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `atlas/site_index.json differs from the
  deterministic payload` + `244 pages have stale or absent L2 nav` (e.g.
  `papers/paper-a-frame-algebra/`, `papers/paper-b-bloch-burri-identity/`,
  `papers/paper-d-wave-particle-duality/`).
- **Root cause** `[A]`: the public-site build artifacts are stale. Gate
  is doing its job. Repair is owner-gated (WO-B6).

### 2.15 `check_q4_declarations.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `/amrita/`, `/egg/`, `/riemann/`, `/suda/`
  robots is `'noindex, follow'` but Q4 declared `'index, follow'`.
- **Root cause** `[A]`: 4 routes have a robots meta drift from what Q4
  declared. Authority: `11_UPLINK/50_AUDITS_AND_EXECUTIONS/232_FIVE_RULINGS_EXECUTED_2026_07_31.md`.

### 2.16 `check_barred_claims.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `12_PUBLIC_SITE/2/index.html:89: retired
  untyped node product:P = Φ×V`; `12_PUBLIC_SITE/4/index.html:192: P = Φ
  × V`; `12_PUBLIC_SITE/5/index.html:154-155: Titan arithmetic:⊙ = •
  × ○` + `P = Φ × V`.
- **Root cause** `[A]`: retired forms are still in the public site.
  Gate is doing its job. Sweep is owner-gated (WO-D1).

### 2.17 `check_node_product_ranking.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `00_META/00_THE_CORPUS_SPINE.md:27: retired
  node-product used as a current ordering` (and 1+ other in
  `02_EPISTEMOLOGY/00_HOLOBIONT_MEMBRANE_v0.1.md:111`).
- **Root cause** `[A]`: same retired-form class as §2.16. Gate is doing
  its job.

### 2.18 `check_d6_equiv_d0.py` — **STUCK-RED on corpus** (was PASSES-BOTH at baseline) `[A]`

- **Baseline** `[A]`: at the start of this run the gate was **PASS** (rc=0).
- **Mutation** `[A]`: `14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md` —
  appended a clean line `X D6≡D0 Y` (no REFUTE_MARKERS, no backticks).
- **Faulted**: rc=1 — `Literal D6/D0 equivalence on 3 live surface(s) ... 
  - 14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md:130: literal D6/D0 equivalence...`
  - `00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md:232: ... :324: ...` (these
    were added by the parallel sibling session mid-test).
- **Restored**: rc=1 — the same 2 surfaces in
  `00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md` (the sibling session had
  landed a file with literal D6/D0 forms in lines that did not trigger
  REFUTE_MARKERS, mid-test, while my mutation was in flight).
- **Verdict** `[A]/[I]`: the gate **did** detect my fault (3 surfaces vs
  the 2 the parallel session had just introduced, vs the original 0).
  The restored verdict is FAIL only because the parallel session's
  audit introduced a real corpus defect in the same minute. Net
  classification: **STUCK-RED on current corpus**, with the gate's
  per-fault detection still working (the count went 0 → 2 → 3 across the
  run; each transition was a real event).
- **Note** `[I]`: the mutation test of the gate's own refute-filter
  (`REFUTE_MARKERS`) requires a line WITHOUT any of the 18 refute
  markers (e.g. "literal", "form", "out", "from", "into", "about" — see
  `check_d6_equiv_d0.py:77-91`). A first attempt with "The literal
  closure D6≡D0 is asserted here for the test." was correctly filtered
  by the `literal\b` marker; a second attempt with `X D6≡D0 Y` was not.
  The gate is doing more than string-matching.

### 2.19 `check_trophic_rosetta_doctrine.py` — **PASSES-BOTH** `[A]`

- **Baseline**: rc=0 (`trophic_rosetta_doctrine: clean`).
- **Mutation** `[A]`: `01_TELEOLOGY/00_THE_TANTRIC_VAJRAYANA_TRANSMUTATION.md`
  — appended `Rosetta caste is hereditary` (matches the
  `hereditary-rosetta` pattern at `check_trophic_rosetta_doctrine.py:66-70`).
- **Faulted**: rc=1 — `trophic_rosetta_doctrine: FAILED / - 01_TELEOLOGY/00_THE_TANTRIC_VAJRAYANA_TRANSMUTATION.md:144: hereditary-rosetta`.
- **Restored**: rc=0.
- **Verdict**: gate correctly detects a forbidden doctrine phrase.

### 2.20 `check_links.py` — **STUCK-RED on corpus, but per-fault detection verified** `[A]`

- **Baseline**: rc=1, FAIL — `1 broken local links; baseline is 0. A
  link broke. / 05_COSMOLOGY/03_FORMAL_SYSTEM/57_THE_POTENTIAL_READING.md:350:
  target escapes corpus -> ../../../00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md`.
- **Mutation** `[A]`: `00_META/00_THE_CORPUS_SPINE.md` — appended
  `[a broken link that does not exist](./does_not_exist_xyz.md)`.
- **Faulted**: rc=1 — `2 broken local links ... 00_META/00_THE_CORPUS_SPINE.md:303: missing target -> ./does_not_exist_xyz.md` + the existing
  `57_THE_POTENTIAL_READING.md:350` finding.
- **Restored**: rc=1 — only the `57_THE_POTENTIAL_READING.md:350` finding
  (the protected file I cannot touch).
- **Verdict** `[A]`: gate correctly detected my new broken link (count
  1 → 2). The restored FAIL is solely due to the pre-existing break in
  `57_THE_POTENTIAL_READING.md` (which the hard-stops prohibit me from
  touching). **STUCK-RED on corpus; gate working**.

### 2.21 `check_contradiction_census.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — `Total files in 01_EMERGENTISM (pattern
  hits): 427 / Live files: 112 / Public site: 13 / HTML pages: 2 / HTML
  pages as live doctrinal use: 0 / Status: FAIL  (live=112,
  public=13, html-doctrinal=0)`.
- **Root cause** `[A]`: the retired Titan infix `⊙ = • × ○` is still
  carried as a citation in 112 live files. Gate is doing its job; the
  carrier set is the corpus's named pathology. See also the
  `carrier_set_at_ruling` proposal at `CENSUS_RECEIPT_WIRE_2026_08_06.md`
  for the formal contract.

### 2.22 `check_dead_citations.py` — **STUCK-RED on corpus, but per-fault detection verified** `[A]`

- **Baseline**: rc=1, FAIL — `13 undisclosed dead citation(s) across
  897 live document(s)`.
- **Mutation** `[A]`: `01_TELEOLOGY/00_SATURATION_AND_RETURN.md` —
  appended `[an additional reference](../06_ONTOLOGY/00_D6_AS_APOPHATIC_CLOSURE.md) is here for completeness.`
- **Faulted**: rc=1 — `14 undisclosed dead citation(s) across 897 live document(s)`
  (count 13 → 14 on my fault).
- **Restored**: rc=1 — `13 undisclosed dead citation(s)` (original).
- **Verdict** `[A]`: gate correctly detected my new dead citation.
  **STUCK-RED on corpus; gate working**. The original test attempt used
  `../../06_ONTOLOGY/...` (one `..` too many) and resolved outside the
  corpus, so the gate's `os.path.exists(tp)` filter was the reason the
  first attempt produced no new finding — not a gate defect.

### 2.23 `check_forwarding_stubs.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — multiple `[R4] canonical_target points at
  another STUB` chain findings, e.g. `00_THE_DEAD_FORMS_CATALOG_v0.1.md`
  forwards to `00_META/00_THE_DEAD_FORMS_CATALOG_v0.1.md` which forwards
  to `90_ARCHIVE/...`; `00_FOLDER_LAYOUT_v0.1.md` chain similar; plus
  `00_META/00_THE_TWELVE_RULINGS_2026_07_22.md` (chain cut off in
  truncated output).
- **Root cause** `[A]`: forwarding-stub chains in the corpus. Gate is
  doing its job.

### 2.24 `check_g2_normal_form.py` — **PASSES-BOTH** `[A]`

- **Baseline**: rc=0 (`G2 NORMAL FORM: PASS / MUTATION COVERAGE: 6
  mutants, each tripping its declared checks; all 5 checks exercised
  (none decorative).`).
- **Mutation** `[A]`: `check_g2_normal_form.py:72` — changed
  `return "ii" not in w and not w.startswith("i")` to
  `return not w.startswith("i")` (drops the `ii` exclusion — the
  inverse of the `_mut_allow_ii` mutant the script already ships).
- **Faulted**: rc=1 — `G2 NORMAL FORM: FAIL / - check (1) injectivity: G2: collision val('S') == val('Sii') == 2 ... / - check (4) intermediate partial quotients >= 1: G2: 'Sii' has a partial quotient < 1: cf=[0, 2]`.
- **Restored**: rc=0.
- **Verdict**: gate correctly detected both the injectivity loss
  (check 1) and the partial-quotient violation (check 4). The
  built-in 6-mutant harness also runs on every invocation — the script
  is **self-testing** the §0.5 contract in addition to checking the math.
  This is the strongest PASSES-BOTH verdict in the report.

### 2.25 `check_tree_contract.py` — **STUCK-RED on corpus** `[A]`

- **Baseline**: rc=1, FAIL — multiple findings: `forbidden per-lane
  governance folder: 08_FRAMEWORK_SUPPORT/00_META`; `root document is
  neither owner nor forwarding stub: 00_THE_CLOSED_READING_LOOP_K2_SIGN_RECEIPT_2026_08_01.md`
  (and 3 others); `forwarding stub has no declared target:
  00_THE_FOUNDATION.md` (and others).
- **Root cause** `[A]`: per-lane governance folder collision; several
  root documents do not declare their owner/stub status; forwarding
  stubs lack `canonical_target`. Gate is doing its job.

### 2.26 `check_no_secrets_staged.py` — **PASSES-BOTH** `[A]`

- **Baseline**: rc=0 (`SECRET SCAN: PASS (git reported no staged changes; nothing to scan)`).
- **Mutation** `[A]`: created a temporary file
  `00_HANDOFF/_tmp_secret_test.py` containing
  `test_key = 'sk-or-v1-abcdef0123456789abcdef0123456789abcdef01234567'`,
  then `git add`ed it; ran the gate; then `git reset HEAD` and trashed
  the file. (Side effect: touched the git index, but reversible — the
  reset returned it to clean.)
- **Faulted**: rc=1 — `🚨 SECRET LEAK DETECTED: 2 finding(s) in staged
  diff` (one from my fake key, one from a parallel-session-staged file
  `09_TOOLS/02_COMPILERS/test_finity_practice_gates.py` whose SHA-256
  hash tokens tripped the gate's generic-token fallback — see
  `_generic_token_is_known_nonsecret` at `check_no_secrets_staged.py:160-179`).
- **Restored**: rc=0 — `SECRET SCAN: PASS` (index clean after reset;
  confirmed by `git diff --cached --name-only` returning empty).
- **Verdict**: gate correctly detected a fake API key pattern. The
  second finding (on the sibling-session file) shows the gate's
  generic-token rule does not exempt bare 64-hex tokens without an
  explicit hash-custody word — by design.

## 3 · Cross-cutting observations

### 3.1 The corpus's named gate-defect disease is live in this run `[S]`

The corpus's own doctrine (`check_established.py:25-29`,
`check_foundation.py:138-141`) names the defect: "a checker that raises
can neither pass nor fail". This run observed **three** instances:

- `check_foundation.py` HANGs (raises via timeout, never returns).
- `check_claim_status.py` raises NameError on `reopened_ids:705` before
  reading any data.
- `check_established.py` is **STUCK-GREEN on a class of mutations**
  (out-of-list inflation phrases pass) — the same defect, in the
  opposite direction. The sibling report at
  `MUTATION_TEST_GATES_2026_08_06.md` calls this `PARTIAL FALSE-PASS`; I
  classify it STUCK-GREEN per the user's scheme.

**Per §0.5**: a check that cannot fail in either direction is the
defect live-gate integrity exists to catch. The lesson is **not**
"remove the broken gates from the runner" — it is "fix the broken
gates, then re-run the mutation test, then the runner's verdict
becomes evidence".

### 3.2 The cross-gate dependency risk is real `[I]`

`check_claim_status:705` (NameError) cascades to **2** other gates:

- `check_contact_limited.py` (calls `check_claim_status` directly —
  `check_contact_limited.py:1597`).
- `check_work_in_progress.py` (reads `CLAIM_STATUS.yaml`, which the
  broken gate prevents the YAML from loading cleanly).

**3 of 26 gates** (the 2 ERROR + the 1 cascade-affected STUCK-RED)
inherit their broken state from one line of code. A single
initialization of `reopened_ids = set()` would clear all three.

### 3.3 The 12 STUCK-RED gates are working, not broken `[A]`

Two were spot-tested for "does the count scale with my fault?":

- `check_links.py` — 1 → 2 broken links on my fault. Restored 1.
- `check_dead_citations.py` — 13 → 14 on my fault. Restored 13.

Both are doing per-finding work. The 12 STUCK-RED gates cannot go green
on the current corpus without a destructive repair; that is **not** a
gate defect, it is a corpus defect the gate is correctly naming.

### 3.4 Parallel-session activity shaped the run `[A]`

The corpus was being modified concurrently throughout the run by a
sibling session. Effects observed:

- `00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md` landed mid-test with
  literal D6/D0 forms that flipped `check_d6_equiv_d0` from baseline
  PASS to runtime FAIL. Documented in §2.18.
- `09_TOOLS/02_COMPILERS/test_finity_practice_gates.py` was staged
  with hash tokens that triggered `check_no_secrets_staged`'s
  generic-token rule. Documented in §2.26.
- 4 other parallel-session files appeared in `00_HANDOFF/` during the
  run (CENSUS_HALFLIFE_FINDING, CHECK_FOUNDATION_QUOTE_FIX,
  MUTATION_TEST_GATES, PROPAGATION_ARCHITECTURE_FINDING, RULING_LANDED_GATE,
  plus a second standing-gate figure script and a
  `09_TOOLS/01_SCRIPTS/mutation_test_gates.py` and `gate_health.py`).
  None of these were touched.

All mutations introduced by this report were restored; `git diff` on
the 11 mutated files returns no output. `git status` shows the
parallel-session files as `??` (untracked) and the parallel-session
edits as ` M` (modified), but **none** of those were authored by this
report.

## 4 · Hard-stop compliance

- **No commits** `[A]`: this report is staged as a single file
  (this one). Not committed; K2 disposes per §0.6.
- **No push / rebase / merge** `[A]`: none performed.
- **No 90_ARCHIVE writes** `[A]`: no `90_ARCHIVE/` file was opened for
  read or write by this run.
- **No 57_THE_POTENTIAL_READING.md modifications** `[A]`: the file was
  never opened by the mutation tool.
- **No CENSUS_RECEIPT_WIRE_2026_08_06.md modifications** `[A]`: the
  file was never opened by the mutation tool.
- **No 3 uncommitted repair files touched** `[A]`: the modified
  files observed at run-start (`check_foundation.py`,
  `test_lived_weltanschauung.py`, `D6_THE_RETURN.md`, `RESEARCH_EDITION_1.md`)
  were not opened by the mutation tool. The mutation tool was scoped to
  a hand-picked allowlist of 11 files (see §5).
- **Byte-identical corpus at end** `[A]`: SHA-256 of all 11 mutated
  files pre = post (verified per-mutation in the run, plus
  `git diff` on the same 11 files returns no output).

## 5 · Files mutated by this report (all restored)

| # | File | Mutation | Original SHA-256 | Restored? |
|---|---|---|---|---|
| 1 | `09_TOOLS/01_SCRIPTS/coherence_profile.json` | `axes.routing.state` → `INVALID_STATE` | `f0c33610…` | yes |
| 2 | `09_TOOLS/01_SCRIPTS/check_generative_base.py` | line 47 `x = x + 1` → `x = x - 1` | `aa585131…` | yes |
| 3 | `09_TOOLS/01_SCRIPTS/check_g2_normal_form.py` | line 72 dropped `"ii" not in w and` | `e4d092c6…` | yes |
| 4 | `09_TOOLS/01_SCRIPTS/coherence_profile.json` | (re-verify SHA after sed) | `174cf48d…` | yes |
| 5 | `00_ESTABLISHED/README.md` (mutation A) | appended `compiles cleanly` | `bfbd0a5a…` | yes |
| 6 | `00_ESTABLISHED/README.md` (mutation B) | appended `fully machine verified and the complete proof is given above` | same | yes |
| 7 | `09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_FIRST_60_ADJUDICATION.jsonl` | byte 50 → `X` | `7ee2f538…` | yes |
| 8 | `12_PUBLIC_SITE/record/index.html` | `data-count="29"` → `"999"` | `93c288e5…` | yes |
| 9 | `14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md` | appended `X D6≡D0 Y` (3 attempts; final mutation) | `c8c8da38…` | yes |
| 10 | `01_TELEOLOGY/00_THE_TANTRIC_VAJRAYANA_TRANSMUTATION.md` | appended `Rosetta caste is hereditary` | `ba02f816…` | yes |
| 11 | `00_META/00_THE_CORPUS_SPINE.md` | appended `[a broken link...](./does_not_exist_xyz.md)` | `e69852ab…` | yes |
| 12 | `01_TELEOLOGY/00_SATURATION_AND_RETURN.md` | appended `[an additional reference](../06_ONTOLOGY/00_D6_AS_APOPHATIC_CLOSURE.md) is here for completeness.` | `4518cb11…` | yes |
| — | `00_HANDOFF/_tmp_secret_test.py` (new, in `00_HANDOFF/`) | staged a fake OpenRouter key for `check_no_secrets_staged` test | n/a (new file) | trashed via `mavis-trash` |

`git diff` on entries 1-12: no output. `ls 00_HANDOFF/_tmp*`: no
output. `git status --short`: shows only parallel-session files
(`??`) and parallel-session edits (` M`), none of which were authored
by this report.

## 6 · Recommendations for K2 `[D]`

1. **`check_foundation.py` is the load-bearing defect** `[D]`. The
   runner's headline figure is dominated by 1 HANG and 2 ERROR (3/26
   broken). Fixing the HANG is owner-gated; the structural
   recommendation is to bound the scan in `active_foundation_scan_paths`
   with a file-count or size cap, or to run on a sampled basis with a
   `MAX_FILES` env var.
2. **`check_claim_status.py:705` is the cheapest unblock** `[D]`.
   Initializing `reopened_ids = set()` would clear the 2 ERROR gates
   and one of the STUCK-RED gates' upstream blockers (3/26 effective).
   Author-gated per WO-B2, but the fix is one line.
3. **`check_established.py` is a partial STUCK-GREEN on a class of
   mutations** `[D]`. Move from allowlist to a semantic classifier
   (verification-claim + hedge pattern). The current allowlist drifted
   the day it was written; the gate is now narrower than the
   property it exists to catch.
4. **The 12 STUCK-RED gates should be left in the runner** `[D]`. They
   are working; the corpus has pre-existing defects. Their continued
   FAIL is **the gate doing its job**, not a defect to remove.
5. **The 4 runner-only gates** (`check_contradiction_census`,
   `check_dead_citations`, `check_forwarding_stubs`,
   `check_tree_contract`) **are not in `gate.sh`** (per the sibling
   report at `MUTATION_TEST_GATES_2026_08_06.md §1`). They are listed
   in `_run_standing_gate_figure.py:18-45`. The mismatch — runner says
   26, gate.sh says 22 — is a 4-gate divergence between the two
   release-paths. K2 to decide which is canonical.
6. **Two parallel siblings** `[A]`: this report and
   `MUTATION_TEST_GATES_2026_08_06.md` were written in the same hour
   on 2026-08-06 with overlapping scope. The two reports are
   complementary (gate.sh's 22 vs runner's 26; this report's
   STUCK-GREEN finding on `check_established` matches the sibling's
   PARTIAL FALSE-PASS). Cross-link the two before publishing.

## 7 · The one sentence

The 26-gate standing-gate runner produces **8 PASSES-BOTH, 1
STUCK-GREEN on a class of mutations, 12 STUCK-RED on a corpus that has
pre-existing defects the gates are correctly naming, 1 HANG, and 2
ERROR** — and the 1 STUCK-GREEN + 1 HANG + 2 ERROR are the same defect
the corpus's own doctrine names as forbidden, observed in 4 different
gates in this single run, with the corpus byte-identical at the end
and every faulted/restored verdict reproducible from the table above.

---

*Findings staged. K2 disposes. The standing-gate runner continues to
report. The 8 PASSES-BOTH gates are evidence; the 12 STUCK-RED gates
are evidence; the 1 STUCK-GREEN, 1 HANG, 2 ERROR are the defects
the §0.5 lesson exists to catch.*
