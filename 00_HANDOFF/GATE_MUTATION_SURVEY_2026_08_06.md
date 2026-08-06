# GATE MUTATION SURVEY — 2026-08-06

**Work order:** P2.1 — mutation-test every gate.
**Tier:** `[A]` — a measurement, not a ruling. Nothing here is ratified; every
number below came from a command run during this task and is reproducible with
`09_TOOLS/01_SCRIPTS/mutation_test_gates.py`.
**Harness:** `09_TOOLS/01_SCRIPTS/mutation_test_gates.py` (new, this task).
**No checker was edited. No corpus data was mutated.** Every probe ran against a
copy-on-write clone in `/private/tmp` or a throwaway minimal tree.

---

## 0. THE QUESTION, AND WHY IT IS THE SAME QUESTION

A referee panel instructed "your default is REFUTED" returned 18 kills in 18
hearings; a fair re-hearing overturned 15. The rule extracted from that episode:

> **A judgment instrument that cannot return the opposite verdict is broken.**

That rule had been applied to exactly one instrument — the panel. The corpus's
own `check_*.py` files are judgment instruments too. Each returns a verdict on
the corpus every time the gate runs. None of them had ever been asked whether it
*can* return the other one.

This survey asks it of all 27, mechanically.

---

## 1. BASELINE CENSUS — verified, and the prior figure corrected

The figure carried into this task was **9 pass / 16 fail / 1 hang**. That figure
is **correct for `09_TOOLS/01_SCRIPTS/` alone (26 files), as measured at
10:42 ICT**, and it is incomplete in two ways:

1. It omits `12_PUBLIC_SITE/check_public_semantic_parity.py` (27th checker).
2. It collapses two different failure modes. Three of the "fails" are not
   failures — they are **tracebacks**. A checker that raises did not judge the
   corpus; it died before judging. `DOES-NOT-RUN` is a strictly worse state than
   `FAIL`, and folding them together hides that.

**Measured 10:42 ICT** (27 checkers, 90 s timeout, `census.py`):
`PASS=9  FAIL=14  ERROR=3  HANG=1`

**Measured 11:04 ICT** (same 27, via `mutation_test_gates.py --census`):
`PASS=8  FAIL=16  ERROR=3  HANG=0`

The two runs differ because **other agents were writing to this tree during the
survey**. Two specific drifts, both verified:

- `check_foundation.py` **hung** (>90 s, no output) at 10:42, and **failed in
  5.3 s** at 11:04. Its mtime moved to `2026-08-06 10:53:37` mid-run. It was
  being edited while I measured it. The hang is real and was observed; whether
  it survives in the current version is not something this survey can assert.
- `check_d6_equiv_d0.py` was **green** at 10:42 and **red** at 11:04, because
  another agent wrote `D6≡D0` twice into
  `00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md`. That is not a defect in the
  survey — it is a live, unplanned demonstration that the fence fires on real
  content written by a real agent.

A 28th checker, `09_TOOLS/01_SCRIPTS/check_ruling_landed.py`, appeared during
the session (another agent). It is **not bare-invocable** — it exits with
`--ruling-id is required` — so `gate.sh`-style invocation cannot run it. It is
outside this survey's spec list and is flagged by the harness on every run.

---

## 2. THE VERDICT TABLE

Run: `mutation_test_gates.py --clone … --json survey3.json`, 2026-08-06 11:04 ICT.

| gate | baseline | rc | wall | class | basis |
|---|---|---|---|---|---|
| check_adjudication_custody | PASS | 0 | 0.05 s | **SOUND** | 2/2 seeded faults caught |
| check_coherence_profile | PASS | 0 | 0.04 s | **SOUND** | 2/2 caught |
| check_established | PASS | 0 | 2.39 s | **SOUND** | 2/2 caught |
| check_g2_normal_form | PASS | 0 | 9.48 s | **SOUND** | 2/2 caught, incl. its own bound |
| check_no_secrets_staged | PASS | 0 | 0.06 s | **SOUND** | 1/1 caught |
| check_record_counters | PASS | 0 | 0.03 s | **SOUND** | 2/2 caught |
| check_trophic_rosetta_doctrine | PASS | 0 | 0.06 s | **SOUND** | 2/2 caught |
| **check_generative_base** | PASS | 0 | 2.60 s | **SOUND-BUT-BLIND** | **3 of 4 mutants survived** |
| check_barred_claims | FAIL | 1 | 0.67 s | **SOUND** | green witness produced |
| check_d6_equiv_d0 | FAIL | 1 | 0.59 s | **SOUND** | green witness produced |
| check_dead_citations | FAIL | 1 | 0.35 s | **SOUND** | green on a clean tree |
| check_forwarding_stubs | FAIL | 1 | 0.28 s | **SOUND** | green on a clean tree |
| check_links | FAIL | 1 | 0.60 s | **SOUND** | green witness produced |
| check_q4_declarations | FAIL | 1 | 0.03 s | **SOUND** | green witness produced |
| **check_contradiction_census** | FAIL | 1 | 1.67 s | **CANNOT-PASS** | **red on a tree containing only itself** |
| **check_claim_status** | ERROR | 1 | 0.05 s | **DOES-NOT-RUN** | `NameError: reopened_ids` |
| **check_contact_limited** | ERROR | 1 | 0.73 s | **DOES-NOT-RUN** | inherits the above |
| **check_public_semantic_parity** | ERROR | 1 | 0.94 s | **DOES-NOT-RUN** | `NameError: excluded_routes` |
| check_active_receipt_citations | FAIL | 1 | 6.37 s | UNDETERMINED | repair set ~124; probes inconclusive |
| check_emergentism_purity | FAIL | 1 | 3.76 s | UNDETERMINED | minimal-tree probe raised |
| check_foundation | FAIL | 1 | 5.34 s | UNDETERMINED | file under concurrent edit |
| check_node_product_ranking | FAIL | 1 | 3.07 s | UNDETERMINED | minimal-tree probe needs inputs |
| check_receipt_citations | FAIL | 1 | 0.65 s | UNDETERMINED | see §5 — two-sided fence |
| check_review_bundle | FAIL | 1 | 0.48 s | UNDETERMINED | repair is an owner act |
| check_site_build_artifacts | FAIL | 1 | 0.50 s | UNDETERMINED | a generator itself fails |
| check_tree_contract | FAIL | 1 | 0.07 s | UNDETERMINED | minimal-tree probe raised |
| check_work_in_progress | FAIL | 1 | 0.07 s | UNDETERMINED | see §4 — same root cause |

**Totals:** SOUND **13** · SOUND-BUT-BLIND **1** · CANNOT-FAIL **0** ·
CANNOT-PASS **1** · DOES-NOT-RUN **3** · UNDETERMINED **9** · total **27**.

**UNDETERMINED means the probe was inconclusive, not that the gate is broken.**
Nine gates are unresolved and are stated as unresolved. Calling an inconclusive
probe a verdict is precisely the failure mode this survey exists to catch, and
an earlier draft of this harness made exactly that mistake — see §7.

---

## 3. THE HEADLINE — one instrument cannot fail, and its sibling can

`check_generative_base.py` checks the corpus's declared generative base:
one object `1`, two operations `S(x) = x + 1` and `iota(x) = 1/x`.

Mutate the successor operation to `x + 2` — i.e. change the corpus's **declared
primitive** — and the checker does not merely still pass. It prints a
**byte-identical** report:

```
UNMUTATED
  GENERATIVE BASE BOUNDED REGRESSION: PASS (232 values from all words to length 10;
  143 unreduced collisions, 0 reduced; CW tree 8191 words / 8191 distinct;
  grid 25x25 reachable; 0 unattained)                                        rc=0

MUTANT  x + 1  ->  x + 2
  GENERATIVE BASE BOUNDED REGRESSION: PASS (232 values from all words to length 10;
  143 unreduced collisions, 0 reduced; CW tree 8191 words / 8191 distinct;
  grid 25x25 reachable; 0 unattained)                                        rc=0
```

The reason is structural: the checker computes both the claim and the reference
from the **same** function, so a mutation moves both sides together. It is a
self-consistency check wearing the costume of a regression test.

Two further mutants confirm the gate is also insensitive to its own advertised
scope:

```
MUTANT  WORD_LEN = 10 -> 4    PASS ("12 values from all words to length 4")   rc=0
MUTANT  GRID = 25 -> 3        PASS ("grid 3x3 reachable")                     rc=0
MUTANT  reduced() -> True     FAIL ("G2: 143 values have >1 reduced word")    rc=1
```

So it *can* go red — it is not CANNOT-FAIL — but the exhaustive bound can be cut
from 10 to 4 and the reachability grid from 25×25 to 3×3, and it reports PASS
with the shrunken numbers printed in its own success line. **A reader who trusts
the word PASS learns nothing about how much was checked.**

Now the same two mutations against its sibling, `check_g2_normal_form.py`:

```
MUTANT  x + 1 -> x + 2   FAIL  "check (2) the continued-fraction dictionary:
                                dictionary mismatch on 'S': cf=[2] gives 2, val gives 3"
MUTANT  WORD_LEN 18 -> 3 FAIL  "G2 NORMAL FORM: FAIL (mutation harness is blind)
                                - mutant 'dictionary without the reversal' did NOT
                                  trip its declared check(s) [2]"
```

It catches the model mutation because it checks `val` against an **independent**
reference (the continued-fraction expansion), not against itself. And it catches
the bound mutation because **it carries its own mutation harness and fails when
that harness stops discriminating**.

**The corpus already contains the answer.** `check_g2_normal_form.py` is the
worked example of a sound gate — independent reference + self-monitoring
sensitivity — and it sits in the same directory as a gate that cannot see its
own primitive change. The lesson does not need to be invented; it needs to be
propagated.

---

## 4. ONE INCOMPLETE RENAME TAKES OUT THREE GATES

`00_META/claim_status/CLAIM_STATUS.yaml` has buckets:
`validated · open · graves · investigations · typed_survivors`.
There is **no `reopened` bucket** — it was renamed to `investigations`.

The rename did not finish:

- **`check_claim_status.py:705`** iterates `investigations` but still writes to
  `reopened_ids`, which nothing defines, and still labels its errors
  `"reopened.id"` / `"reopened"`:
  ```
  NameError: name 'reopened_ids' is not defined. Did you mean: 'restored_ids'?
  ```
  The branch is only reached when `investigations` is non-empty. It has 9 rows,
  so it is reached every run. **DOES-NOT-RUN.**
- **`check_contact_limited.py:1597`** calls `_CLAIM_STATUS_POLICY.check(root)`
  and inherits the same traceback. **DOES-NOT-RUN.**
- **`check_work_in_progress.py`** still looks for a `reopened` bucket and
  reports `bucket 'reopened' is missing or is not a list (got NoneType)`. **FAIL.**

One unfinished rename, three gates down, and two of them are not failing loudly
— they are not judging at all.

Independently, `12_PUBLIC_SITE/check_public_semantic_parity.py:541` dies on
`NameError: name 'excluded_routes' is not defined`.

This is a **recurring defect class in this corpus, not a coincidence**.
`check_established.py`'s own header records the third instance verbatim:

> "The loop at the bottom of main() iterated FORBIDDEN_INFLATIONS while nothing
> defined it, so every run of this checker died on NameError. A checker that
> raises cannot pass and cannot fail — it aborts, blocks the gate, and reports
> nothing about the property it exists to guard."

That diagnosis was written on 2026-08-05, one day before this survey found two
more live instances of exactly the same bug. **The lesson was recorded and not
propagated.** A ten-second `python3 -m py_compile`-plus-smoke-run over every
checker would have caught all four.

---

## 5. THE MIRROR OF THE RIGGED PANEL — a gate that cannot say yes

`check_contradiction_census.py` forbids the retired Titan infix `⊙ = • × ○` and
sets its live-file target to **0**. Its scan covers `.md .html .py .json .yaml
.yml` across the whole tree, excluding only `90_ARCHIVE` and `91_COMPATIBILITY`.

Its own docstring, line 4, contains the pattern in literal form.
`09_TOOLS/01_SCRIPTS/` is not excluded. Therefore `live ≥ 1` **always**.

Probe — a temp tree whose only file is the checker itself:

```
Total files in 01_EMERGENTISM (pattern hits): 1
Live files (exclude 90_ARCHIVE, 91_COMPATIBILITY): 1
Targets: 0 live / 0 public site / 0 HTML-as-doctrinal-use
Status: FAIL  (live=1, public=0, html-doctrinal=0)
Top files (top 10 by path):
  09_TOOLS/01_SCRIPTS/check_contradiction_census.py
CENSUS: FAIL  (exit 1)
```

**CANNOT-PASS, proven.** Delete every other file in the corpus and it still
returns FAIL, naming itself. The only input on which it goes green is one in
which it does not exist. It has one verdict, exactly like the panel.

The fix is one line and is *not* mine to make: obfuscate the pattern in the
docstring, or add the checker's own path to the exclusion set. Both are edits to
a checker, and this task is read-only on checkers.

### 5b. A second, softer version of the same shape

`check_receipt_citations.py` holds `AMBIGUOUS_BASELINE = 91`. On the corpus it
reports 93 and fails — correct, a real collision was introduced. But run it on a
**clean** tree and it fails there too:

```
RECEIPT CITATIONS: FAIL
- ambiguous receipt numbers FELL to 0 (baseline 91) — good, but lower
  AMBIGUOUS_BASELINE in this file to lock the gain in.
```

It is red when the property gets worse **and** red when the property becomes
perfect. Green is the single point 91. This is defensible as a ratchet — it
forces the baseline down — but it means the gate can never report success from a
repair alone, and a reader cannot tell "worse" from "fixed" by the exit code.
Classified UNDETERMINED, flagged here because it is the same shape as §5 with
one green point instead of none.

---

## 6. WHAT THE SOUND GATES ACTUALLY CAUGHT

Every SOUND verdict rests on a probe that ran, not on an assertion:

| gate | seeded fault | result |
|---|---|---|
| check_adjudication_custody | one newline appended to a frozen JSONL | FAIL "must contain no blank JSONL records" |
| check_adjudication_custody | a `FALSE` verdict flipped to `REAL_OPEN` in place | FAIL |
| check_coherence_profile | overall state claimed better than its worst axis | FAIL "declared PASS, computed PASS_WITH_DEBT" |
| check_coherence_profile | world contact `OPEN`→`ESTABLISHED`, evidence list empty | FAIL |
| check_established | manifest inflated to "compiles cleanly" | FAIL "verification inflation remains in ledger" |
| check_established | `η = 0` quietly dropped from the NOT-ESTABLISHED list | FAIL |
| check_d6_equiv_d0 | literal `D6 ≡ D0` on a live surface | FAIL, named file and line |
| check_no_secrets_staged | Anthropic-shaped key staged in the clone's index | FAIL "SECRET LEAK DETECTED" |
| check_record_counters | static no-JS counter understated by 3 | FAIL "a no-JS reader would see the wrong number" |
| check_record_counters | one `cut` row relabelled `held` | FAIL |
| check_trophic_rosetta_doctrine | hereditary-extraction licence added to a live owner | FAIL, rule `higher-caste-extraction` |
| check_trophic_rosetta_doctrine | required phrase `η_move = 0` removed | FAIL |
| check_g2_normal_form | successor `x+1 → x+2` | FAIL, dictionary mismatch |
| check_g2_normal_form | exhaustive bound 18 → 3 | FAIL "mutation harness is blind" |

And six red gates were driven to green, proving the red is a finding about the
corpus rather than a property of the instrument:

| gate | repair applied in the clone | result |
|---|---|---|
| check_barred_claims | rewrote 4 barred strings on public routes 2/4/5 | PASS |
| check_d6_equiv_d0 | rewrote 5 literal forms to the tilde form in 1 file | PASS |
| check_links | de-linked the one target that is not on disk | PASS |
| check_q4_declarations | restored `index, follow` on 4 governed routes | PASS |
| check_dead_citations | clean tree | PASS "0 live documents" |
| check_forwarding_stubs | clean tree | PASS "0 stubs, none points at a grave" |

Note on `check_links`: the dangling target,
`00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md`,
**exists nowhere in the tree** — `00_HANDOFF/constitutional/` does not exist. The
citing document is `05_COSMOLOGY/03_FORMAL_SYSTEM/57_THE_POTENTIAL_READING.md:350`
and it calls the target "the §6 chair brief". A live document cites a chair brief
that was never written. That is a finding for someone else's work order; this
survey only used it as a green witness.

---

## 7. WHAT I GOT WRONG, AND HOW IT WAS CAUGHT

The first version of this harness returned **8 CANNOT-PASS**. Seven were wrong.

It treated "still red on a minimal tree" as proof that green is unreachable. But
most of these gates read manifests, registries and git output; on a minimal tree
they fail *for want of inputs*, which says nothing about reachability. Two of
them did not even fail — they raised, and the harness counted a traceback as a
verdict.

Fixed: a minimal-tree failure now counts as CANNOT-PASS **only if the gate's own
path appears in its own complaint** (`SELF-REFUTING`); everything else is
`NEEDS-INPUTS` and lands in UNDETERMINED. That took CANNOT-PASS from 8 to 1.

I am recording this because a survey that hands out CANNOT-PASS verdicts from an
inconclusive probe would be committing, in the act of measuring it, the exact
defect it was built to measure. The first draft did. It is fixed, and the rule
is now written into the harness docstring so the next run cannot quietly regress.

---

## 8. OPEN — OWNER DECISIONS, NOT MINE

1. **Wire the survey into the gate?** `mutation_test_gates.py` surveys; it does
   not gate. Making a CANNOT-FAIL or DOES-NOT-RUN checker block a commit is a
   constitutional change to what the build enforces. Not taken.
2. **Fix the census self-reference?** Requires editing a checker (out of scope
   here) and choosing between two semantics: exclude the tool directory from the
   scan, or obfuscate the pattern in the docstring. The first weakens the fence
   over tooling; the second is cosmetic. That is a semantics call.
3. **`check_generative_base` — repair or retire?** Its sibling
   `check_g2_normal_form.py` already covers the injectivity property with an
   independent reference. Whether the older bounded regression should be fixed,
   demoted to a smoke test, or removed from `gate.sh` is a scope decision.
4. **`check_receipt_citations` two-sided fence** — is "red when the count
   improves" the intended ratchet, or should an improvement pass and print a
   loud instruction? A semantics call on what an exit code means.
5. **`check_ruling_landed.py`** requires `--ruling-id`, so `gate.sh`'s bare
   invocation cannot run it. Someone must decide its default invocation.

## 9. REPRODUCING THIS

```bash
python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py --census
python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py --json survey.json
python3 09_TOOLS/01_SCRIPTS/mutation_test_gates.py --only check_generative_base
```

The harness clones the corpus copy-on-write before any probe and refuses to run
if the clone fails. It restores every byte it touches after each probe. The live
tree was verified unmodified after every run of this survey: `git status` showed
only `09_TOOLS/01_SCRIPTS/mutation_test_gates.py` and this report as new from
this task.

**Counts drift between runs because other agents are writing to this tree.**
Re-run the census; do not quote the table above without re-running it.

### Concurrent edit to the harness itself

While this report was being written, another agent edited
`mutation_test_gates.py`: `DEFAULT_TIMEOUT` and `SLOW_TIMEOUT` were tightened to
60 s, and a `findings`-magnitude extractor was added to `run_script`. The survey
was re-run against the edited file. **Every verdict is unchanged:**

```
baseline: ERROR=3  FAIL=16  PASS=8
verdict : CANNOT-PASS=1  DOES-NOT-RUN=3  SOUND=13  SOUND-BUT-BLIND=1  UNDETERMINED=9
total   : 27
```

The 60 s cap is safe for the current tree — the slowest gate measured 9.5 s — but
it is tighter than the 90 s at which `check_foundation` was observed to hang at
10:42. Under the 60 s cap that observation would be reported identically
(`HANG`), so nothing is lost; note only that "hang" now means ">60 s", not
">90 s".
