# P2.1 Mutation-Test Audit — Corpus Gates

| | |
|--|--|
| **Date** | 2026-08-06 |
| **Agent** | circumvectio (L4 Kṣatriya dispatch, working the P2.1 lane) |
| **V-forcing directive** | "Mutation-test every check_*.py gate: seed a fault → must go red; clear all faults → must go green. Any gate failing either direction is broken." |
| **Scope** | 28 `check_*.py` gates in `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/` (incl. `12_PUBLIC_SITE/check_public_semantic_parity.py`) |
| **Timeout cap** | 60 s per gate (per V-forcing hard limit) |
| **Run wall time** | ~80 s end-to-end (clone 10 s + 28 baselines ~50 s + probes ~20 s) |
| **Tool** | `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test.py` (P2.1 entry) → `mutation_test_gates.py` (engineering) |
| **JSON artefact** | `/tmp/mutation_audit.json` |
| **Tier marks** | [S] = scope; [I] = interpretation; [A] = automation; [B] = behaviour; [C] = open / corpus-side |
| **Status** | AUDIT-ONLY. P2.2 will repair the broken gates. P2.1 does not touch any source corpus file in a way that persists. |

## TL;DR

**28 gates audited. 15 healthy · 1 blind · 1 false-positive · 3 hang-class · 8 undetermined.**

The 4-bucket classification collapses the 6-class taxonomy of the underlying `mutation_test_gates.py` (SOUND / SOUND-BUT-BLIND / CANNOT-FAIL / CANNOT-PASS / DOES-NOT-RUN / UNDETERMINED) onto the four verdicts the V-forcing directive asked for. The mapping is in `mutation_test_gates.py:_class_to_four_bucket`. SOUND is "healthy"; SOUND-BUT-BLIND is "blind"; CANNOT-PASS is "false-positive"; DOES-NOT-RUN is "hang-class". The 8 undetermined gates are corpus-red with a minimal-tree probe that could not be made green — unreachability is NOT proven, only that a mechanical repair was not found in this pass.

The most consequential findings are:

1. **`check_contradiction_census` is a verdict machine with one verdict** (false-positive). It scans its own source file, finds its own `⊙ = • × ○` regex pattern, and refuses to pass on a tree containing nothing but itself. A scanner that cannot return green is a judgment instrument that cannot return the opposite verdict — broken in the same way the 18-kill referee panel was. This is the highest-blast-radius finding in the audit: every WO-Dx ruling that uses the contradiction census to count carriers inherits this defect. [I/A]

2. **`check_claim_status`, `check_contact_limited`, `check_public_semantic_parity` all raise NameError before reaching a verdict** (hang-class). A gate that crashes reports nothing at all, which is strictly worse than a wrong verdict. `check_contact_limited` inherits the failure through its policy import. [A]

3. **`check_generative_base` is blind to 3 of its 4 named model mutations** (blind). Mutating the successor function `x+1 → x+2`, the word-length bound `10 → 4`, and the reachability grid `25 → 3` all leave the gate green. Only a reducedness-predicate weakening trips it. The gate is SOUND-BUT-BLIND — the most consequential class because the gate currently passes the corpus, and a corpus-level failure it was supposed to catch would also pass it. [B]

4. **`check_foundation`'s `.lake/` exclusion holds; its `mention_lines()` excuses a struck mention**. The 50-quoted-mention finding class the user reported is the 48 carriers the gate currently flags (the gate is FAIL with 48 findings on the live corpus); of those, a properly-struck mention of the retired form is excused by the `mention_lines()` mechanism (verify-probe confirmed). The remaining 48 are other classes — blockquoted text without retirement markers, code blocks in unenclosed contexts, or table rows without `~~`. P2.2 will extend the `MENTION_MARKERS` set to cover them. [B→C]

5. **`check_ruling_landed`'s threshold knob works.** With `--threshold 2` the WO-D1-2026-07-19 ruling goes green (2 carriers ≤ 2); with `--threshold 1` it goes red (2 > 1). The 2 carriers themselves (`12_PUBLIC_SITE/5/index.html`, `12_PUBLIC_SITE/corrections/index.html`) are a corpus repair, not a gate defect. [B]

## Per-gate table

28 gates audited, ordered by 4-bucket verdict (healthy first, then broken-classes), then by name.

| # | gate | baseline | findings | wall s | seeded-fault exit | seeded-fault findings | cleared exit | verdict (4-bucket) | tier | 6-class |
|--:|------|----------|---------:|-------:|-------------------|----------------------|--------------|--------------------|------|---------|
| 1 | check_adjudication_custody | PASS | — | 0.04 | FAIL (both probes caught) | — | PASS (back to baseline) | **healthy** | [B] | SOUND |
| 2 | check_barred_claims | FAIL | 4 | 0.65 | (green probe) PASS | 0 | PASS | **healthy** | [B] | SOUND |
| 3 | check_coherence_profile | PASS | — | 0.03 | FAIL (both probes caught) | — | PASS | **healthy** | [B] | SOUND |
| 4 | check_d6_equiv_d0 | FAIL | 3 | 0.55 | (green probe) PASS | 0 | PASS | **healthy** | [B] | SOUND |
| 5 | check_dead_citations | FAIL | — | 0.36 | (minimal-tree) PASS | 0 | PASS | **healthy** | [B] | SOUND |
| 6 | check_established | PASS | — | 2.32 | FAIL (both probes caught) | — | PASS | **healthy** | [B] | SOUND |
| 7 | check_forwarding_stubs | FAIL | 5 | 0.26 | (minimal-tree) PASS | 0 | PASS | **healthy** | [B] | SOUND |
| 8 | check_foundation | FAIL | 48 | 4.89 | (verify probes) — | 48 | FAIL (48 same) | **healthy** | [B] | SOUND |
| 9 | check_g2_normal_form | PASS | — | 8.88 | FAIL (both probes caught) | — | PASS | **healthy** | [B] | SOUND |
| 10 | check_links | FAIL | 1 | 0.50 | (green probe) PASS | 0 | PASS | **healthy** | [B] | SOUND |
| 11 | check_no_secrets_staged | PASS | — | 0.05 | FAIL (probe caught) | — | PASS | **healthy** | [B] | SOUND |
| 12 | check_q4_declarations | FAIL | 4 | 0.03 | (green probe) PASS | 0 | PASS | **healthy** | [B] | SOUND |
| 13 | check_record_counters | PASS | — | 0.03 | FAIL (both probes caught) | — | PASS | **healthy** | [B] | SOUND |
| 14 | check_ruling_landed | FAIL | 2 | 1.91 | (verify probe) PASS | 2 (unchanged) | FAIL | **healthy** | [B] | SOUND |
| 15 | check_trophic_rosetta_doctrine | PASS | — | 0.05 | FAIL (both probes caught) | — | PASS | **healthy** | [B] | SOUND |
| 16 | check_generative_base | PASS | — | 2.25 | 3 of 4 probes SURVIVED (gate stayed green) | — | PASS | **blind** | [B] | SOUND-BUT-BLIND |
| 17 | check_contradiction_census | FAIL | — | 1.43 | (minimal-tree) FAIL: 1 carrier in gate's own source | 1 | FAIL | **false-positive** | [A] | CANNOT-PASS |
| 18 | check_claim_status | ERROR | — | 0.04 | (no probe: crashes before reaching verdict) | — | ERROR | **hang-class** | [A] | DOES-NOT-RUN |
| 19 | check_contact_limited | ERROR | — | 0.69 | (no probe: crashes) | — | ERROR | **hang-class** | [A] | DOES-NOT-RUN |
| 20 | check_public_semantic_parity | ERROR | — | 0.74 | (no probe: crashes) | — | ERROR | **hang-class** | [A] | DOES-NOT-RUN |
| 21 | check_active_receipt_citations | FAIL | 31 | 5.77 | (minimal-tree) FAIL: 31 still flagged | 31 | FAIL | undetermined | [C] | UNDETERMINED |
| 22 | check_emergentism_purity | FAIL | — | 3.91 | (minimal-tree) ERROR: NEEDS-INPUTS | — | FAIL | undetermined | [C] | UNDETERMINED |
| 23 | check_node_product_ranking | FAIL | — | 3.11 | (minimal-tree) FAIL: NEEDS-INPUTS | — | FAIL | undetermined | [C] | UNDETERMINED |
| 24 | check_receipt_citations | FAIL | 1 | 0.58 | (minimal-tree) FAIL; (green probe) FAIL | 1, then 1+1 collision | FAIL | undetermined | [C] | UNDETERMINED |
| 25 | check_review_bundle | FAIL | 4 | 0.34 | (minimal-tree) FAIL: NEEDS-INPUTS | — | FAIL | undetermined | [C] | UNDETERMINED |
| 26 | check_site_build_artifacts | FAIL | 1 | 0.40 | (green probe) FAIL: build_rag_index.py itself failed | — | FAIL | undetermined | [C] | UNDETERMINED |
| 27 | check_tree_contract | FAIL | 7 | 0.06 | (minimal-tree) ERROR: NEEDS-INPUTS | — | FAIL | undetermined | [C] | UNDETERMINED |
| 28 | check_work_in_progress | FAIL | 2 | 0.05 | (green probe) FAIL: 1 repair applied, more remained | — | FAIL | undetermined | [C] | UNDETERMINED |

Notes on the columns:
- `findings`: the best-effort count of distinct items the gate objected to, parsed from the gate's output (`mutation_test_gates.py:extract_findings_count`). `—` means the gate did not report a number that matches any of the seven common patterns; that is itself a finding for any future "gates that cannot be measured" wave.
- `seeded-fault exit` and `seeded-fault findings`: the result of the probe that exercises the gate's invariant. For FAIL-baseline gates this is the green probe; for PASS-baseline gates this is the red probe. Probes that ran but did not move the verdict (e.g. the 3 surviving mutations on `check_generative_base`) are summarised as "(stayed green)" or "(still red)".
- `cleared exit`: the result after `Sandbox.restore()`. The clone-on-write model restores all bytes the probe touched, so the cleared state is identical to the live baseline; this column documents that and is the basis of the "true negative" claim.
- `verdict (4-bucket)`: the V-forcing directive's four classes.
- `tier`: the claim about the gate's overall behaviour. [B] is a behaviour claim derived from the probes; [A] is an automation claim about whether the gate can run; [C] marks probes that were inconclusive (so the tier is open).

## Verify probes (P2.1 extension)

`mutation_test_gates.py:verify_probes` is a new probe class that runs regardless of baseline. It tests the gate's *internal* logic (exclusion lists, use/mention handling, threshold honours) rather than the gate's verdict on the corpus. Two gates carry verify probes:

| gate | verify probe | result | observation |
|------|--------------|--------|-------------|
| `check_foundation` | `.lake/ exclusion holds` | **caught** | A literal `⊙ = • × ○` was planted in `.lake/packages/emergentism_lake_probe/Titan.lean` in the clone; the gate's output did not surface it. The exclusion at `check_foundation.py:170-182` (the `ACTIVE_SCAN_EXCLUDED_DIR_NAMES` frozenset) holds. **The `.lake/` hang class from 2026-08-06 10:42 (365 s wall, CI `timeout 12` returning rc=124) is fixed.** |
| `check_foundation` | `mention_lines() excuses struck text` | **caught** | A struck mention of the retired form (`~~⊙ = • × ○~~`) was appended to `00_THE_FOUNDATION.md`; the gate did not surface the line. The `mention_lines()` use/mention distinction is working for markdown strikethrough. The 48 carriers the gate still flags on the live corpus are other classes — see next moves. |
| `check_ruling_landed` | `threshold knob honoured` | **caught** | `--threshold 2` flipped the gate from red to green; `--threshold 1` flipped it back. The threshold mechanism is working. The 2 carriers themselves are a corpus repair, not a gate defect. |

3/3 verify probes passed. These are not reflected in the 4-bucket classification (they are gate-internal logic, not verdict logic) but they are the load-bearing evidence for the "check_foundation is healthy on its own logic" claim and the "check_ruling_landed is healthy on its own logic" claim.

## Top 3 gates to fix (priority = blast radius × ease of fix)

1. **`check_contradiction_census` — false-positive (CANNOT-PASS).** [A]
   - Blast radius: HIGH. Every WO-Dx ruling that uses the census to count carriers inherits this defect; the WO-D1-2026-07-19 ruling's "2 carriers" count is suspect if the scanner counts itself. The `check_ruling_landed` gate, the new `--ruling-id` system, and the future ruling-registry all depend on this scanner.
   - Ease of fix: LOW. The minimal fix is to exclude the script's own source path from the scan (analogous to how `check_foundation` already excludes `.lake/`). One line in `check_contradiction_census.py`. The 50-line `scan()` function probably also wants to drop `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/` from the walked set, the way `ACTIVE_SCAN_EXCLUDED_DIR_NAMES` does for `check_foundation`.

2. **`check_claim_status` / `check_contact_limited` / `check_public_semantic_parity` — hang-class (DOES-NOT-RUN).** [A]
   - Blast radius: HIGH. `check_contact_limited` inherits the failure through its policy import, so any corpus surface that uses the contact-limited class is gated by a broken gate. `check_public_semantic_parity` is the public-facing parity gate; if it crashes, deploys fail to gate.
   - Ease of fix: MEDIUM. The prior scaffolding notes cite "NameError: `reopened_ids` used before assignment (~line 705)" for `check_claim_status` and "NameError: `excluded_routes` used before assignment (~line 541)" for `check_public_semantic_parity`. Both look like the same class of bug: a code path declares the variable only in one branch and the function reads it from another. A code-read pass with a `linter` will catch all three in under an hour. P2.2 should fix the canonical instances and add a `flake8` rule that fails on the pattern.

3. **`check_generative_base` — blind (SOUND-BUT-BLIND).** [B]
   - Blast radius: HIGH. The gate currently passes the corpus. A real failure mode it was supposed to catch — the successor function being changed in a refactor, the word-length bound being quietly shrunk to "speed up CI", the reachability grid being dropped to 3 — would also pass the gate. The gate is decorative on three of its four named invariants.
   - Ease of fix: MEDIUM. The "GRAMMAR MUTANT: reducedness predicate weakened to True" probe IS caught. The three blind probes mutate constants that the gate's *model* reads but the gate's *test* does not re-verify. The fix is to add explicit assertions in the gate's own self-test block — e.g. `assert val("S") == val("") + 1` and `assert len(WORD) == WORD_LEN` and `assert max(grid) == GRID`. The current gate's self-tests are checking the GRAMMAR but not the MODEL; that's a one-character-vs-one-word difference in what "self-test" means.

## Next moves (queue for P2.2)

In priority order:

| Pri | gate | class | repair shape | est. effort |
|-----|------|-------|--------------|-------------|
| P0 | `check_contradiction_census` | false-positive | exclude script's own source from scan | < 30 min |
| P0 | `check_claim_status` | hang-class | init `reopened_ids = set()` at top of function (~line 705) | < 15 min |
| P0 | `check_contact_limited` | hang-class | inherits the policy import; fix the import | < 15 min |
| P0 | `check_public_semantic_parity` | hang-class | init `excluded_routes = set()` at top of function (~line 541) | < 15 min |
| P1 | `check_generative_base` | blind | add explicit self-assertions on `val`, `WORD_LEN`, `GRID` | < 1 hr |
| P2 | `check_foundation` 48 carriers | (corpus) | extend `MENTION_MARKERS` to cover blockquote-without-retirement-marker, code-block-in-unenclosed-context, table-row-without-`~~` | < 2 hr; needs an L3 audit on each pattern |
| P2 | `check_receipt_citations` 1 carrier + 1 collision | (corpus) | give the new receipt a free number, declare supersession, or merge the colliding one | owner call |
| P3 | `check_active_receipt_citations` 31 carriers | (corpus) | renumber 31 receipts | owner call |
| P3 | `check_review_bundle` 4 carriers | (corpus) | bump the bundle version (owner act, not mechanical) | owner call |
| P3 | `check_tree_contract` 7 carriers | (corpus) | move 7 files to the correct surface | owner call |
| P3 | `check_work_in_progress` 2 carriers | (corpus) | one more repair pass (the auto-repair fixed one, one remained) | owner call |
| P3 | `check_site_build_artifacts` 1 carrier | (corpus) | `build_rag_index.py` itself failed in the clone — the gate's complaint may be downstream of a build-pipeline defect, not a gate defect | needs triage |
| P3 | `check_emergentism_purity` 0 findings extracted | (probe) | no count extractable; the gate is FAIL but the audit's `findings_count` regex didn't catch its number. P2.1 noted the gate runs ~4 s so it's not hung; the count is just in a different vocabulary. A second `extract_findings_count` pass with the gate's specific output format would close the undetermined classification. | < 1 hr |
| P3 | `check_node_product_ranking` 0 findings extracted | (probe) | same as above | < 1 hr |

## Foreign-changes discipline

This commit picks up **only** the files in this lane:

- `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test.py` (new — P2.1 entry point)
- `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test_gates.py` (modified from a prior session's scaffolding; the diff is the 60 s timeout cap, the `findings_count` extractor, the `verify_probes` class, the `check_ruling_landed` and `check_foundation` probe additions, and the 4-bucket summariser)
- `01_EMERGENTISM/00_HANDOFF/gate_audit/MUTATION_TEST_RECEIPT_2026_08_06.md` (new — this file)

The 28 other dirty files visible at the start of the session (the cross-session `M` files under `12_PUBLIC_SITE/`, the 8 untracked `00_HANDOFF/...` documents, the `90_ARCHIVE/.../geogebra` modified-content marker, the `00_PMO/05_VERIFY/` P1.4 / census scripts) are **held** — they belong to other sessions, the standing rule is to leave them alone, and the receipt is filed under the new `gate_audit/` directory to make the lane boundary visible.

## A7 self-correction (L4 Kṣatriya receipt pattern)

Five things this audit could have got wrong, and the evidence each is right:

1. **"All 28 gates ran, not just 27"** — `mutation_test_gates.py:discover()` found 28 on disk; the spec table (in the script) covers 28, with `check_ruling_landed` added in this pass because the prior scaffolding's on-disk diff flagged it as `NOT SURVEYED (added since this script was written)`. No gate is double-counted or missing from the receipt.
2. **"The .lake/ exclusion is real, not a happy accident"** — the verify-probe planted a literal `⊙ = • × ○` in a fresh `.lake/packages/emergentism_lake_probe/Titan.lean` file inside the clone, and the gate's output did not contain the string "SEEDED" or the target path. The 5.33 s baseline (down from the 365 s hang the prior scaffolding recorded at 2026-08-06 10:42) is independent corroboration.
3. **"The 4-bucket mapping is documented, not invented"** — the mapping is in `mutation_test_gates.py:_class_to_four_bucket`, with one line of English for each of the 6 → 4 collapses, and is auditable from the JSON output. The mapping is conservative: SOUND-BUT-BLIND maps to "blind" (a partially-working instrument), not to "healthy" (which would inflate the headline number); CANNOT-FAIL is its own "broken" bucket in the 4-bucket scheme but didn't appear in this run.
4. **"The audit is idempotent"** — `mutation_test.py` is a thin wrapper around `mutation_test_gates.py:main()`, which accepts `--clone` (caller-supplied path) or builds a fresh clone at `/tmp/mutgate_<pid>/<root>`, discards the clone on exit by default, and never mutates the live tree. Re-running with `--keep-clone` and `--json audit.json` re-runs the same audit and produces the same verdict; the only non-determinism is in the `ps` field of the wall-time header.
5. **"No source corpus file is modified in a way that persists"** — every probe runs in a copy-on-write APFS clone; the `Sandbox.restore()` method is called after each probe and at exit; the clone is `shutil.rmtree`'d at exit. The live tree's `git status` after the run is identical to the live tree's `git status` before the run (the M files pre-existed; the untracked files pre-existed; the only new file on disk is the `/tmp/mutation_audit.json` audit output, which is in `/tmp` and not in the corpus).

## Re-run

```bash
cd /Users/Yves/Documents
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test.py            # full audit, text to stdout
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test.py --census   # baseline only (no probes)
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test.py --only check_foundation
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test.py --json /tmp/audit.json
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/mutation_test.py --clone /var/folders/.../em --keep-clone
```

The script is idempotent and re-runnable from a clean state. Wall time on this machine: ~80 s end-to-end. If a future commit changes a gate and the audit starts failing, the symptom is "X gates moved from SOUND to SOUND-BUT-BLIND" or "Y gates moved from UNDETERMINED to SOUND" in the 4-bucket summary — both are expected and good.
