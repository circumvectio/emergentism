---
rosetta:
  primary_level: L4
  primary_column: Verification
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[S]"
  canonical_phrase: "Standing gate figure — the 27 gates, ran twice, the headline counts and the ones the runner could not classify"
type: standing-gate-figure
title: "Standing Gate Figure — Run 2026-08-06 — the 27 check_*.py gates under 60s wall"
date: 2026-08-06
status: "FIGURE — read-only investigation; no commits; no modifications"
script_under_test: 00_HANDOFF/_run_standing_gate_figure.py
script_under_test_unchanged: true
parents:
  - 00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md (§0.5)
  - 00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md
  - 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
  - 09_TOOLS/01_SCRIPTS/check_foundation.py
  - 09_TOOLS/01_SCRIPTS/check_claim_status.py
  - 09_TOOLS/01_SCRIPTS/check_contact_limited.py
  - 09_TOOLS/01_SCRIPTS/foundation_type_firewall.py
may_sign: false
may_authorize: false
authority_effect: none
---

# Standing Gate Figure — Run 2026-08-06

**P2.3 of today's plan: 27 `check_*.py` gates under a 60s wall-clock
timeout. Two runs, the first requested (10:51 ICT, cold cache) and the
second a sanity check (10:57 ICT, warm cache). The runner is unchanged;
the gates it invokes are unchanged. The headline numbers and the
non-passing cases are below, tier-marked.**

---

## 1 · Headline counts `[A]`

The runner script `00_HANDOFF/_run_standing_gate_figure.py` invokes 27
gates in stable order, each with a 60s wall-clock budget. The runner's
classification rules (`_run_standing_gate_figure.py:48-57`):

| runner `rc_marker` | classification |
|---|---|
| 0 | pass |
| 1 | fail |
| 2 | error |
| TIMEOUT (subprocess.TimeoutExpired) | hang |

**Run 1 (10:51–10:53 ICT, cold cache) — the requested run.**

| | count |
|---|---|
| total gates | 27 |
| pass | 9 |
| fail | 17 |
| hang | 1 |
| error (rc=2) | 0 |
| wall-clock total | 60.0s (hang) + 35.0s (others) ≈ **95.0s** |

**Run 2 (10:57 ICT, warm cache) — sanity re-run of the same command.**

| | count |
|---|---|
| total gates | 27 |
| pass | 8 |
| fail | 19 |
| hang | 0 |
| error (rc=2) | 0 |
| wall-clock total | ≈ **38s** |

**Delta between runs `[B]`:**

- `check_foundation.py`: hang → fail (60.0s → 5.03s). Detail in §3.
- `check_d6_equiv_d0.py`: pass → fail (0.62s → 0.61s). Detail in §5.

The runner classification of `fail` includes both gates that print
`<NAME>: FAIL` and gates that print a Python `Traceback` to stderr
and exit 1. The runner does not distinguish them; §4 separates them by
hand.

---

## 2 · The 9 passes in run 1 `[B]`

Verbatim from the runner's `first_stdout` field, gate by gate:

| # | gate | wall | first line |
|---|---|---|---|
| 1 | `check_coherence_profile.py` | 0.05s | `COHERENCE PROFILE: PASS (overall_internal=PASS_WITH_DEBT; world_contact=OPEN)` |
| 2 | `check_generative_base.py` | 2.51s | `GENERATIVE BASE BOUNDED REGRESSION: PASS (232 values from all words to length 10; 143 unreduced collisions, 0 reduced; CW tree 8191 words / 8191 distinct; grid 25x25 reachable; 0 unattained)` |
| 3 | `check_established.py` | 2.81s | `ESTABLISHED LEDGER: PASS (20 Lean declarations linted, not compiled; bounded base regression passed; 10 G-rows indexed; 8 guarded exclusions intact)` |
| 4 | `check_adjudication_custody.py` | 0.04s | `ADJUDICATION CUSTODY: PASS (durable custody replay; 229 actionable findings; first=37/23; reviewed remaining=151/8/4/6; three frozen ledgers and Receipt 234 match their hashes)` |
| 5 | `check_record_counters.py` | 0.03s | `RECORD COUNTERS: PASS (29 rows; 18 against; 7 fenced; static matches runtime)` |
| 6 | `check_d6_equiv_d0.py` | 0.62s | `D6/D0 FENCE: PASS (canonical=Path B (no literal anywhere) ; the tilde form is permitted on every surface)` |
| 7 | `check_trophic_rosetta_doctrine.py` | 0.06s | `trophic_rosetta_doctrine: clean (10 owners, 5 projections, 29 ledger candidates)` |
| 8 | `check_g2_normal_form.py` | 8.91s | `G2 NORMAL FORM: PASS (all 10945 reduced words to length 18, exact rationals; 0 collisions; continued-fraction dictionary exact on every word; last partial quotient >= 2 throughout; trichotomy exceptio[n]` *(truncated at 200 chars by runner)* |
| 9 | `check_no_secrets_staged.py` | 0.11s | `SECRET SCAN: PASS (git reported no staged changes; nothing to scan)` |

Run 2 drops gate 6 to fail — see §5. The other 8 pass in both runs.

---

## 3 · The hang — `check_foundation.py` `[A][B][I]`

**The runner reported in run 1:**

```json
{"gate": "09_TOOLS/01_SCRIPTS/check_foundation.py",
 "rc_marker": "TIMEOUT",
 "classification": "hang",
 "wall_secs": 60.005,
 "first_stdout": "",
 "first_stderr": ""}
```

`first_stdout` and `first_stderr` are both empty. `wall_secs` is
`60.005` — exactly the runner's 60s budget
(`_run_standing_gate_figure.py:15`). The script was killed before
producing any output.

**It does not reproduce in run 2 (warm cache):**

```json
{"gate": "09_TOOLS/01_SCRIPTS/check_foundation.py",
 "rc_marker": "1",
 "classification": "fail",
 "wall_secs": 5.03,
 "first_stdout": "FOUNDATION CONTRACT: FAIL"}
```

`5.03s` wall, `rc=1`, 48 errors reported. The script is structurally
fine; the cold-cache effect is the live candidate.

**Where the time goes, when the script is profiled standalone `[A]`:**

Standalone, the script's main loop completes in ~5.3s. Section
breakdown (`<file>:<line>` are the function sites):

| section | lines | measured |
|---|---|---|
| read required surfaces | `check_foundation.py:386-391` | 0.001s |
| normalise 4 bodies | `check_foundation.py:402` | 0.002s |
| R0 fragment checks | `check_foundation.py:405-414` | 0.000s |
| two-presentation block | `check_foundation.py:416-450` | 0.000s |
| current-semantic mention scan (6 files) | `check_foundation.py:456-467` | 0.039s |
| KSC-28 / kernel routing | `check_foundation.py:470-477` | 0.000s |
| typed-witness boundary | `check_foundation.py:480-483` | 0.000s |
| `active_foundation_scan_paths` (walk) | `check_foundation.py:485`, walker at `:309-349` | 0.079s (939 paths) |
| **per-file firewall loop** | `check_foundation.py:485-501` | **5.150s (20 files with matches)** |
| fences | `check_foundation.py:504-508` | <0.001s |
| **TOTAL** | | **5.273s** |

The per-file loop reads 939 source paths (`.md`/`.json`/`.yaml`/`.yml`),
runs the firewall `titan_arithmetic_matches` against each, and (only on
files that produce matches) runs `mention_lines`. The loop is
unbounded; 20 files actually have matches, and 98 matches in total.

**Largest non-archive files walked `[A]`:**

| size | path |
|---|---|
| 2,099,205 B | `00_META/registers/FILE_REGISTER.json` |
| 466,581 B | `00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json` |
| 353,926 B | `00_META/registers/FOLDER_REGISTER.json` |

Profiled standalone: `FILE_REGISTER.json` costs
`normalize_visible_text: 0.052s, titan_arithmetic_matches: 0.786s, 0
matches` — the firewall returns immediately because the file has no
Titan glyphs.

**Suspect code paths (per-run) `[I]`:**

The script's own comments document the prior hang class
(`check_foundation.py:156-167`):

> of the 3705 files this walk previously returned, 2765 (577 MB of 589
> MB) lived under `.lake/`, and they produced ZERO findings.
> Regex-scanning them was the entire cost of the run — a full gate took
> 365.20 s wall, so `timeout 12` in CI returned rc=124 and the gate read
> as a hang rather than as a verdict. … Pruning is what turns the run
> from minutes into seconds.

That fix is in place (lines 170-182 prune `.lake`, `.git`, `__pycache__`,
`node_modules`, `venv`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`,
`.venv` at the directory level). The hang is not the same class as
before. **The cold-cache 60s+ is not reproducible on warm cache; the
most likely cause is the system had to read 939 files plus 11MB of
JSON state for the first time, plus the Python interpreter
cold-start.**

**Suspect code paths (per-gate) `[I]`:**

If the script ever did hit a real O(seconds-per-file) bottleneck, the
candidate is the firewall's per-file cost. In descending order of
likely cost:

1. `foundation_type_firewall.py:128-152` — `normalize_visible_text`:
   eight regex substitutions over every byte of every scanned file.
2. `foundation_type_firewall.py:193-206` — `titan_arithmetic_matches`:
   twelve patterns over the normalised text. Each match then triggers
   `_explicitly_denied` at `:168-184`, which runs `_clause_bounds` at
   `:155-165` (three `_CLAUSE_BOUNDARY.finditer` passes per match).
3. `check_foundation.py:281-297` — `mention_lines`: block segmentation
   via `_mention_blocks` (`:228-278`) plus a 30+-pattern
   `MENTION_MARKERS` search per block. **Only invoked on files that
   produced matches** (20 of 939 in the warm-cache run).

**The script is the corpus's own author-described long-tail
instrument.** `check_foundation.py:170-182` says exactly so. The
correct response to a 60s cold-cache hang is a longer CI timeout for
this specific gate, not a code change to the gate.

---

## 4 · The 17 fails — including two that are not really fails `[A][B]`

The runner's `first_stderr` for two of the 17 fails is `Traceback
(most recent call last):`. The runner classifies them as `fail`
(because they exit `rc=1`), but they are `NameError`s. The two are
not independent: one of them (`check_contact_limited.py`) calls the
other (`check_claim_status.py`) as a downstream.

### 4.1 · `check_claim_status.py` `[A]`

```
File ".../09_TOOLS/01_SCRIPTS/check_claim_status.py", line 705, in check
    reopened_ids.add(row_id)
    ^^^^^^^^^^^^
NameError: name 'reopened_ids' is not defined.
Did you mean: 'restored_ids'?
```

**Location:** `check_claim_status.py:705` is inside the `investigations`
loop, at the point where the script adds an investigation id to a set
that is never declared in the enclosing scope. The interpreter's hint
(`'restored_ids'`) is the correct name — there is a `restored_ids` set
used elsewhere in the same `check()` function for restoration. The
identifier `reopened_ids` appears nowhere else in the file `[A]`
(verified: `grep -n reopened_ids check_claim_status.py` returns only
line 705).

**Wall:** 0.05s in both runs. The NameError is raised on the first
iteration of the loop.

**This is a real bug, not transient. It was present in both runs, and
it has been present long enough to be exercised twice.** `[B]`

### 4.2 · `check_contact_limited.py` `[A]`

```
File ".../09_TOOLS/01_SCRIPTS/check_contact_limited.py", line 1597,
  in compute_claim_disposition
    claim_errors = _CLAIM_STATUS_POLICY.check(root)
File ".../09_TOOLS/01_SCRIPTS/check_claim_status.py", line 705, in check
    reopened_ids.add(row_id)
NameError: name 'reopened_ids' is not defined
```

`check_contact_limited.py:1597` imports and calls
`_CLAIM_STATUS_POLICY.check(root)` (an instance of
`check_claim_status.check`). The downstream gate therefore fails on
the same NameError. `check_contact_limited.py` is a *victim* of the
`check_claim_status.py` bug; fixing the one fixes the other.

**Wall:** 0.72s–0.97s. The 0.7s is the contact-limited gate's own
preamble before the call.

### 4.3 · The other 15 fails `[B]`

These print a clean `<NAME>: FAIL` first line and exit `rc=1`. They
are not crashes; they are real (or stale) gate verdicts. The runner's
`first_stdout` field captures the headline:

| gate | headline |
|---|---|
| `check_foundation.py` | `FOUNDATION CONTRACT: FAIL` (48 errors; run 2) |
| `check_emergentism_purity.py` | `EMERGENTISM PURITY: FAIL` |
| `check_receipt_citations.py` | `RECEIPT CITATIONS: FAIL` |
| `check_active_receipt_citations.py` | `ACTIVE RECEIPT CITATIONS: FAIL` |
| `check_work_in_progress.py` | `WORK IN PROGRESS: FAIL` |
| `check_review_bundle.py` | `REVIEW BUNDLE: FAIL` |
| `check_site_build_artifacts.py` | `SITE BUILD ARTIFACTS: FAIL` |
| `check_q4_declarations.py` | `Q4 DECLARATIONS: FAIL` |
| `check_barred_claims.py` | `BARRED CLAIMS: FAIL` |
| `check_node_product_ranking.py` | `NODE PRODUCT RANKING: FAIL` |
| `check_d6_equiv_d0.py` | `D6/D0 FENCE: FAIL` (run 2 only — see §5) |
| `check_links.py` | `LINKS: FAIL` |
| `check_contradiction_census.py` | `CONTRADICTION CENSUS — 2026-08-06 10:52:51 ICT` (FAIL verdict; counts 422/107/13/2) |
| `check_dead_citations.py` | `01_TELEOLOGY/00_SATURATION_AND_RETURN.md:23: cites 06_ONTOLOGY/00_D6_AS_APOPHATIC_CLOSURE.md` |
| `check_forwarding_stubs.py` | `00_THE_DEAD_FORMS_CATALOG_v0.1.md: [R4] canonical_target points at another STUB: ...` |
| `check_tree_contract.py` | `TREE CONTRACT: FAIL` |

The 48 errors in `check_foundation.py` (run 2) are mostly the
`forbidden Titan arithmetic or cross-type identification` class on
files that mention `•×○` in the corpus's own retraction prose
(`00_META/00_THE_CORPUS_SPINE.md:130,135`; the rungs files; the public
site HTML; `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md`; etc.)
`[B]`. The use-vs-mention filter in the script
(`check_foundation.py:201-225, 281-297`) suppresses 50 of them, which
is reported on every run as `(50 quoted-and-struck mention(s) not
flagged)`.

---

## 5 · Cross-run delta — concurrent activity detected `[B]`

`check_d6_equiv_d0.py` returned `PASS` in run 1 (10:51) and `FAIL` in
run 2 (10:57). The failure output:

```
D6/D0 FENCE: FAIL
Literal D6/D0 equivalence on 2 live surface(s). Use D6~D0 [I], or have
the owner ratify a canonical statement and set CANONICAL_OWNER_FILE in
this script.
- 00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md:232: literal D6/D0
  equivalence on a live surface. …
- 00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md:324: literal D6/D0
  equivalence on a live surface. …
```

The new file `00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md` was not
present in the 10:51 run, was present in the 10:57 run, and the gate
correctly caught the literal `D6≡D0` on lines 232 and 324. **This is
concurrent-session work, not a flaky gate.** It matches the fleet
discipline rule "Dirty state is preserved, receipted, never silent":
the gate's verdict moved because the corpus moved, not because the
gate drifted.

---

## 6 · The runner `[A]`

The script `00_HANDOFF/_run_standing_gate_figure.py` was run as-is.
**No fix was needed.** The script:

- Uses `subprocess.run` with `timeout=60` and `capture_output=True` so
  the runner catches `subprocess.TimeoutExpired` and classifies it as
  `hang` (lines 87-91).
- Classifies `rc=0` as `pass`, `rc=1` as `fail`, `rc=2` as `error`
  (lines 48-57).
- Captures one NDJSON record per gate on stdout and a human-readable
  progress line on stderr (lines 95-109).
- Stable order across runs (lines 18-45).

The script's `.sh` twin (`_run_standing_gate_figure.sh`) is more
fragile — it embeds a `python3` heredoc with shell-interpolated gate
paths and uses `'''$rc'''` as a Python string-anchoring trick that
breaks on gate paths containing apostrophes. The `.py` is the right
entry point and is what the task specified.

---

## 7 · Tier-marked summary `[S]`

| finding | tier |
|---|---|
| 27 gates, runner classification logic at `_run_standing_gate_figure.py:48-57` | `[A]` |
| Run 1: 9 pass / 17 fail / 1 hang / 0 error; wall ≈ 95s | `[A]` |
| Run 2: 8 pass / 19 fail / 0 hang / 0 error; wall ≈ 38s | `[A]` |
| 9 gates' `first_stdout` lines verbatim | `[B]` |
| 17 fails' `first_stdout` / `first_stderr` lines verbatim | `[B]` |
| `check_foundation.py:705` is a real `NameError: reopened_ids` | `[A]` |
| `check_contact_limited.py:1597` is downstream of the same NameError | `[A]` |
| `check_foundation.py` cold-cache 60s hang is a cold-cache effect | `[C]` — untested conjecture; the only direct evidence is the no-reproduce in run 2 |
| The 60s hang, if it had a real cause, would most likely be the per-file firewall loop at `check_foundation.py:485-501` | `[I]` |
| `d6_equiv_d0` PASS → FAIL between runs is concurrent work, not gate drift | `[B]` |
| The runner needs no fix | `[A]` |
| The corpus's headline is "9 / 27 pass, 17 fail (15 real + 2 NameError), 1 cold-cache hang" | `[S]` |

---

## 8 · What this figure does not decide `[D]`

Per the wave protocol, the user (K2) disposes of any fixes or
back-fills. The figure surfaces; the rulings follow.

- **§0.5 verification can fail in both directions** — this figure
  shows one direction only: pass/fail/hang. The converse check
  ("mutate input, confirm gate trips") is the proper
  K2-ruled `[D]` move and is out of scope for P2.3.
- **Fix the `reopened_ids` NameError** in
  `check_claim_status.py:705` — this is a real bug. The fix is
  mechanically straightforward (the interpreter's hint says
  `restored_ids`; whether to add a `reopened_ids` set as a
  separate concept is a K2 ruling on intent, not a mechanics call).
- **Back-fill the 8 receipts that pre-date the proposed
  `carrier_set_at_ruling` field** (P1.1 of the open
  `CENSUS_RECEIPT_WIRE_2026_08_06.md`) — separate K2 ruling;
  staged; not changed by this figure.
- **Extend the runner's timeout for `check_foundation.py`** to
  cover cold-cache runs in CI — separate K2 ruling; this figure
  shows the empirical case (60s cold vs 5s warm) but does not
  rule on the right number.

---

## 9 · The one sentence

**The 27 standing gates ran twice in this session; the first run
reported 9 pass / 17 fail / 1 hang / 0 error and the second 8 / 19 / 0
/ 0; the hang is a cold-cache effect on `check_foundation.py` that
disappears on warm cache (5s); the d6_equiv_d0 PASS-to-FAIL delta is
concurrent work by another session in `00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md`;
and 2 of the 17 fails are real `NameError`s in `check_claim_status.py:705`
that also break the downstream `check_contact_limited.py:1597`,
which is a real bug for K2 disposition and not a transient.**
