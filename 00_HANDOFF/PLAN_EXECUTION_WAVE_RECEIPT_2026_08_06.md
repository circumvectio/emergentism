---
type: wave-receipt
title: "Plan-Execution Wave Receipt — 2026-08-06 — six work orders (P1.1, P1.2, P1.4, P2.1, P2.2, P2.3), integrated"
status: "ACTIVE — integration receipt only. Nothing committed by this receipt. K2 disposes."
date: 2026-08-06
work_orders: [P1.1, P1.2, P1.4, P2.1, P2.2, P2.3]
register: "[A] every figure carries a provenance mark (V-A / V-R / U); [B] the eight commands re-run by this receipt at 11:10–11:12 ICT; [I] the cross-report conflicts named in §5; [D] the owner queue in §4 is staged, not decided"
parents:
  - 00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md
  - 00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md
  - 00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md
  - 00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md
  - 00_HANDOFF/GATE_MUTATION_SURVEY_2026_08_06.md
  - 00_HANDOFF/CHECK_FOUNDATION_QUOTE_FIX_2026_08_06.md
  - 00_HANDOFF/STANDING_GATE_FIGURE_RUN_2026_08_06.md
may_sign: false
may_authorize: false
authority_effect: none
---

# Plan-Execution Wave Receipt — 2026-08-06

## 0 · Provenance of this receipt (read this before the numbers)

Two of the six agent reports (**P2.1**, **P2.2**) reached this receipt in full
as structured reports. The other four (**P1.1, P1.2, P1.4, P2.3**) reached it
**truncated**; their content here is reconstructed from the receipts those
agents wrote to disk, cited by path in §1. That is a weaker channel than a
direct report and is marked as such.

**Provenance marks used on every figure in §2:**

| mark | meaning |
|---|---|
| **V-A** | the agent ran the command in its own task and printed the output in its report/receipt |
| **V-R** | **re-run by this receipt** at 2026-08-06 11:10–11:12 ICT; the value shown is mine |
| **U** | **unverified** — carried from a prompt, a conjecture, or not re-run by anyone in-task |

Eight commands were re-run for this receipt. No figure below is escorted.

---

## 1 · The six work orders

| WO | status | files touched (working tree) | verified how |
|---|---|---|---|
| **P1.1** — census → receipt frontmatter (`carrier_set_at_ruling`) | DONE, **proposal only — no receipt changed** | `00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md` (new) | agent re-ran the census against the worked example (V-A); schema not applied anywhere; §2 row 12 shows the census has since moved again (V-R) |
| **P1.2** — ruling-landed gate | DONE, gate ships, **not enforced** | `09_TOOLS/01_SCRIPTS/check_ruling_landed.py` (new), `00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md` (new) | agent: gate output + independent grep + 8 edge cases (V-A). **Re-run here (V-R): byte-identical verdict, same 2 carrier paths, grep reproduces** |
| **P1.4** — is zero propagation architectural? | DONE, measurement; verdict split from the plan's framing | `00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md` (new) | agent measured at committed HEAD `1a83affc`, not the working tree, after one figure failed to reproduce twice (V-A). Not re-run here — needs the historical-commit walk |
| **P2.1** — mutation-test every gate | DONE | `09_TOOLS/01_SCRIPTS/mutation_test_gates.py` (new), `00_HANDOFF/GATE_MUTATION_SURVEY_2026_08_06.md` (new) | agent: 27 baselines + 15 seeded faults in a clone + 6 green probes; live tree proven untouched (V-A). Not re-run here (clone survey, ~minutes) |
| **P2.2** — `check_foundation.py` quotation-blindness + hang | DONE | `09_TOOLS/01_SCRIPTS/check_foundation.py` (**modified**), `00_HANDOFF/CHECK_FOUNDATION_QUOTE_FIX_2026_08_06.md` (new) | agent: timed before/after, `comm` diff of finding sets, 3-context discrimination probe (V-A). **Re-run here (V-R): 4.87s, rc=1, 48 findings / 31 unique locations / 50 suppressions — matches** |
| **P2.3** — standing gate figure | DONE | `00_HANDOFF/STANDING_GATE_FIGURE_2026_08_06.md`, `00_HANDOFF/STANDING_GATE_FIGURE_RUN_2026_08_06.md`, `00_HANDOFF/_run_standing_gate_figure.py/.sh` (new) — **and `09_TOOLS/01_SCRIPTS/gate_health.py` + 3 siblings, which are COMMITTED, see §6** | agent ran the 27 gates twice under a 60s wall (V-A). Not re-run here |

---

## 2 · The number ledger

Every figure any agent reported, with its provenance mark. Nothing is
re-quoted without a mark.

### P2.1 — mutation survey

| # | figure | mark |
|---|---|---|
| 1 | prior standing figure "9 pass / 16 fail / 1 hang" | **U** — carried into the agent's prompt; agent found it correct for the 26 `09_TOOLS` checkers alone, omitting the 27th and collapsing 3 tracebacks into "fail" |
| 2 | own census 10:42 ICT, 27 checkers, 90s timeout: PASS=9 FAIL=14 ERROR=3 HANG=1 | **V-A** |
| 3 | final survey 11:04 ICT baseline: ERROR=3 FAIL=16 PASS=8 | **V-A** |
| 4 | verdicts: CANNOT-PASS=1 · DOES-NOT-RUN=3 · SOUND=13 · SOUND-BUT-BLIND=1 · UNDETERMINED=9 · total 27 | **V-A** |
| 5 | **CANNOT-FAIL = 0** — no gate stayed green under every seeded fault | **V-A** |
| 6 | red probes: 8 green gates, 15 seeded faults, 12 caught (3 survivors all on `check_generative_base`) | **V-A** |
| 7 | green probes: 6 red gates driven to green | **V-A** |
| 8 | `check_generative_base` baseline: 232 values to length 10, 143 unreduced collisions, 0 reduced, CW tree 8191 words / 8191 distinct, grid 25×25 | **V-A** |
| 9 | same gate under mutation: `x+1→x+2` byte-identical PASS; `WORD_LEN 10→4` → PASS "12 values"; `GRID 25→3` → PASS "grid 3×3" | **V-A** |
| 10 | `check_receipt_citations` `AMBIGUOUS_BASELINE = 91`; corpus reports 93; clean tree reports 0 and also fails | **V-A** |
| 11 | `check_active_receipt_citations` ≈124 violations | **V-A** (magnitude, agent-stated as approximate) |
| 12 | agent's **first** harness returned 8 CANNOT-PASS; corrected to 1 | **V-A** — self-caught measurement error, §5.6 |
| 13 | `check_foundation` HANG 90.01s at 10:42, FAIL 5.3s at 11:04; its mtime moved to 10:53:37 mid-survey | **V-A** (mtime **V-R**: `11:00:05` now — the file moved again after the survey) |

### P2.2 — check_foundation

| # | figure | mark |
|---|---|---|
| 14 | "roughly eight minutes" / "hangs" | **U** — prompt figure, **refuted** by row 15 |
| 15 | pre-fix: real **365.20s**, user 255.51, sys 6.53, rc=1 (terminates, not an infinite hang); `timeout 12` → rc **124** | **V-A** |
| 16 | profile: walk 0.97s → **3705** paths; regex match **364.18s**; `line_number` 0.06s | **V-A** |
| 17 | scan set: **2765** `.lake` files / **577,045,791** bytes vs **940** non-`.lake` / **11,722,724** bytes = 98% of bytes, **0** findings | **V-A**. Independent corroboration of the mechanism (**V-R**): **46,595** files of all types under `09_TOOLS/03_SIMULATIONS/formal_reap/.lake/` |
| 18 | post-fix: 4.91 / 5.45 / 5.24 / 5.15s, rc=1; walk **939** surfaces; `timeout 12` → rc 1 | **V-A**. **V-R: 4.87s, rc=1** |
| 19 | findings 98 → 48 raw; 60 → 31 unique locations; 29 suppressed; **0 newly appearing** (`comm -13` empty) | **V-A**. **V-R: 48 finding lines, 31 unique locations** |
| 20 | run prints "(50 quoted-and-struck mention(s) not flagged)" | **V-A**. **V-R: 50** |
| 21 | suppression audit: 30 checked, 28 on strike vocabulary, **2** on a bare "forbid"; after tightening, `52:26` flags again and `48:389` stays excused | **V-A** |
| 22 | diff size: 200 insertions, 13 deletions, unstaged | **V-A**. **V-R: `1 file changed, 200 insertions(+), 13 deletions(-)`** |
| 23 | the residual quadratic in `foundation_type_firewall.py` costs 0.06s corpus-wide today | **V-A** — real, currently harmless, deliberately not fixed (out of scope) |

### P1.1 — census wire-up

| # | figure | mark |
|---|---|---|
| 24 | `SURGICAL_DEFECT` receipt's own prose figures: 422 / 107 / 16 / 2 | **V-A** (read from the receipt) |
| 25 | agent's re-run at ~10:48: 422 / 107 / **13** / 2 — public count moved by 3 since the ruling | **V-A** |
| 26 | **V-R at 11:11:00 ICT: total 433 / live 118 / public 13 / HTML 2 / HTML-as-doctrinal-use 0** — total +11 and live +11 against row 25 within the same hour | **V-R** |
| 27 | 8 wave-receipts on disk pre-date the proposed field | **V-A** |

### P1.2 — ruling-landed gate

| # | figure | mark |
|---|---|---|
| 28 | `WO-D1-2026-07-19`: carriers **2**, threshold 0, `NOT_LANDED`, exit 1; carriers = `12_PUBLIC_SITE/5/index.html`, `12_PUBLIC_SITE/corrections/index.html` | **V-A**. **V-R at 11:10 ICT: identical, and the independent grep returns the same two files** |
| 29 | 8 edge cases verified; 1 ruling registered; 3 further retired forms named as unregistered | **V-A** |

### P1.4 — propagation architecture

All P1.4 figures are from **committed HEAD `1a83affc`**, not the working tree —
the agent switched after one figure failed to reproduce (row 35).

| # | figure | mark |
|---|---|---|
| 30 | `measure_propagation_halflife.sh` at `1c270dbd~1` → `725 70 360` reproduces exactly | **V-A** |
| 31 | carriers today, superseded forms (doctrine/receipt/public/archive/total): R1 3/8/9/8/**28** · R2 4/4/2/0/**10** · R3 8/5/1/0/**14** · R0 14/76/11/301/**402** | **V-A** |
| 32 | ruling forms: R1 **91** · R2 **86** · R3 **5** · R0 **649** | **V-A** |
| 33 | R1 doctrine **24 → 3** inside the ruling commit, then flat at 3 for **15 days**; public flat at **9** for 15 days | **V-A** |
| 34 | published figure "**362** files in `12_PUBLIC_SITE` carry the retired form, of which **349** are `.html`" (in `00_THE_AMRITA.md:186`, `04_WHAT_DIED.md:163`, `06_WHAT_IS_STILL_OPEN.md:28`) vs recomputed **15 files, 1 `.html`** | published figure **U** (never re-run since the sweep); recomputed **V-A** |
| 35 | one measurement did not reproduce: R1 `public=18, TOTAL=37` → re-run twice → `public=9, TOTAL=28` | **V-A** — concurrent writes |
| 36 | "+7 regrowth" is **100% receipt zone**, 0% doctrine | **V-A** |
| 37 | R3 age 22 d 18 h (brief asked for >1 month; nearest older ruling was never executed); R1 stale 15 d by ruling date, **25 d** by intent date | **V-A**, the 25 d reading marked `[I]` by the agent |

### P2.3 — standing gate figure

| # | figure | mark |
|---|---|---|
| 38 | 27 gates, 60s wall. Run 1 (10:51–10:53, cold): **9 pass / 17 fail / 1 hang / 0 error**, wall ≈95s | **V-A** |
| 39 | Run 2 (10:57, warm): **8 pass / 19 fail / 0 hang / 0 error**, wall ≈38s | **V-A** |
| 40 | `check_foundation` 60.0s hang → 5.03s fail between runs | **V-A**; the *cold-cache* explanation is **U** — the agent marked it `[C]` and §5.1 gives a competing account |
| 41 | `check_d6_equiv_d0` pass → fail (0.62s → 0.61s), caused by another agent's file | **V-A** |
| 42 | `gate_health.py` + 3 siblings: **4 files, 1051 insertions**, committed as `f68287b4` at 11:08:19 | **V-R** (`git show --stat`) |

### Denominators (this receipt's own count)

| # | figure | mark |
|---|---|---|
| 43 | **V-R at 11:09 ICT: 27 `check_*.py` in `09_TOOLS/01_SCRIPTS/` + 1 in `12_PUBLIC_SITE/` = 28.** The wave's "27" is already stale by one: `check_ruling_landed.py` (mtime 10:49:21) is P1.2's own output | **V-R** |
| 44 | `gate.sh` names **21** distinct `check_*.py` (**V-R**); one agent report says 22; another enumerates 26; the runner enumerates 27; the survey covered 27; the tree now holds 28 | **V-R** for 21 and 28; the others **V-A** at their own moments. **There is no single authoritative gate denominator.** |

---

## 3 · What was NOT done

### BLOCKED-ON-OWNER (mechanical part done; the remaining act is a decision)

- **P2.1 — the 4 NameError-class checkers** (`check_claim_status:705` `reopened_ids`, `check_contact_limited` inheriting it, `check_public_semantic_parity:541` `excluded_routes`, `check_work_in_progress` reading a `reopened` bucket renamed to `investigations`). One-line-class repairs; they are edits to checkers, which P2.1's scope forbade. Three gates currently **do not judge at all**.
- **P2.1 — wiring the mutation survey into the gate.** Deliberately not done: making a CANNOT-FAIL / DOES-NOT-RUN verdict block a commit changes what the build enforces.
- **P2.1 — `check_contradiction_census` self-reference.** Proven SELF-REFUTING (fails on a tree containing only itself, because its own docstring carries the forbidden literal). Both candidate fixes are semantics calls.
- **P1.1 — the schema is proposed, applied to nothing.** No receipt carries `carrier_set_at_ruling`. Back-fill vs forward-only is unresolved.
- **P1.2 — the gate is enforceable but not enforced.** No hook, no CI step. And the two residual carriers are public-site HTML: patching them is a publication act.
- **P1.4 — the two open rulings the agent named:** whether the frozen receipt filename `175_SPHERE_PRIMACY_RULING_EXECUTED_2026_07_29.md` (9 of R3's 14 carriers) counts as a carrier at all; and whether the stale 362/349 figure is repaired or receipted as superseded.
- **P2.2 — `52_THE_GENERATIVE_BASE.md:26` (`⊙ = e`, posit B4).** The tightened filter now flags it. Whether that is a genuine firewall violation or a declared posit the firewall must permit changes the gate's verdict; not decided.
- **P2.2 — the vendored-artifact exclusion** (`.git .lake .mypy_cache .pytest_cache .ruff_cache .venv __pycache__ node_modules venv`) narrows the gate's field of view from 3705 surfaces to 939. Treated as mechanical, flagged for owner visibility.

### NOT-ATTEMPTED (and why)

- **P2.1 — 9 gates left UNDETERMINED.** No green witness and no proof of unreachability: repair sets too large to edit mechanically (`check_active_receipt_citations` ≈124 violations, `check_emergentism_purity`, `check_node_product_ranking`), or owner-gated (`check_review_bundle` needs a bundle-version bump), or blocked by a second defect (`check_site_build_artifacts` stays red after replaying all 6 generators because `build_rag_index.py` itself exits 1).
- **P2.2 — the residual quadratic** in `foundation_type_firewall.py` (out of file scope; costs 0.06s today).
- **P2.2 — a second false-positive class left standing:** `00_META/00_THE_CORPUS_SPINE.md:130` and `:135`, where the heading "The • / ○ correspondence is a reading" is flagged because `/` is read as division. Punctuation-vs-operator, not use-vs-mention. **V-R: still the first two findings of the current run.**
- **P1.4 — R0's 11 public carriers were not classified use-vs-mention**, and the agent states it has **no automatable substitute** for that judgement.
- **P2.3 — the converse direction of §0.5** ("mutate the input, confirm the gate trips") was declared out of scope; P2.1 did it independently.
- **This receipt** did not re-run the P2.1 clone survey, the P1.4 historical-commit walk, or the P2.3 27-gate sweep. Their figures stand as **V-A**, not **V-R**.

---

## 4 · Owner-decision queue (deduplicated across the six)

| # | decision | raised by |
|---|---|---|
| 1 | **Repair the 4 NameError-class checkers** — and rule on intent for `reopened` vs `investigations` (add a set, or rename to `restored_ids`?). Three gates are currently silent, not failing. | P2.1, P2.3 |
| 2 | **Does a mutation verdict gate the build?** Wire CANNOT-FAIL / CANNOT-PASS / DOES-NOT-RUN into CI, or keep the survey advisory. | P2.1 |
| 3 | **`check_contradiction_census` self-reference** — exclude `09_TOOLS/` from its scan (weakens the fence over tooling) or obfuscate the literal in its docstring (cosmetic). | P2.1 |
| 4 | **`check_generative_base` — repair, demote, or retire.** Its sibling `check_g2_normal_form` already covers injectivity against an independent reference. | P2.1 |
| 5 | **`check_receipt_citations` two-sided fence** — should an *improvement* pass loudly instead of failing? Green is currently the single point 91. | P2.1 |
| 6 | **`check_ruling_landed.py` has no bare invocation** (`--ruling-id` required), so `gate.sh`-style invocation cannot run it. Decide its default, or that it is not a gate. | P2.1 |
| 7 | **`⊙ = e` at `52_THE_GENERATIVE_BASE.md:26`** — firewall violation or permitted posit B4? | P2.2 |
| 8 | **Ratify or reject the vendored-artifact scan exclusion** in `check_foundation.py`. | P2.2 |
| 9 | **`MENTION_MARKERS` vocabulary as policy** — it includes broad words ("corrected", "correction", "violate", "reinstate") beyond pure strike vocabulary. | P2.2 |
| 10 | **Mechanism for propagation: carrier-set-at-ruling vs a carriers-remain gate — these two conflict.** P1.2 shipped the gate; P1.4 argues the same gate applied at `1d60ef19` / `a2e022c6` **would have blocked the very commits that made rulings R2 and R3**. Both cannot be adopted as specified. | P1.2 vs P1.4 |
| 11 | **`carrier_set_at_ruling`: back-fill the 8 pre-existing receipts, or forward-only?** And settle the ruling-id convention before any back-fill. | P1.1, P2.3 |
| 12 | **Enforcement timing for P1.1's field and P1.2's gate** — both explicitly deferred; enforcement is a ruling on the contract, not on the instrument. | P1.1, P1.2 |
| 13 | **Ruling registry location** — module-level dict today; a sibling registry file is wanted at ~5 rulings. Also: 3 further retired forms are unregistered (antipodality chordal-distance-2; `⊙ = f(•) × g(○)`; "a record without a receipt is not actual"). | P1.1, P1.2 |
| 14 | **Per-ruling threshold default** (today a global 0). | P1.2 |
| 15 | **The stale 362/349 public-carrier figure** in `00_THE_AMRITA.md:186`, `04_WHAT_DIED.md:163`, `06_WHAT_IS_STILL_OPEN.md:28` — repair, or receipt as superseded? Recomputed value is 15 files / 1 HTML. | P1.4 |
| 16 | **Does `175_SPHERE_PRIMACY_RULING_EXECUTED_2026_07_29.md` count as a carrier?** It is 9 of R3's 14. | P1.4 |
| 17 | **Patch the 2 public-site HTML carriers** so `WO-D1` returns LANDED — a publication act on `12_PUBLIC_SITE/5/index.html` and `/corrections/index.html`. | P1.2 |
| 18 | **Gate timeout policy** — the runner's 60s wall vs the observed cold/warm spread. | P2.3 |

---

## 5 · What no plan anticipated

**5.1 — Two agents give incompatible causes for the same hang, and the timeline
favours neither report's headline.** P2.3 recorded `check_foundation` at 60.0s
(hang) in run 1 (10:51) and 5.03s in run 2 (10:57), and marked *cold cache*
`[C]`. P2.2 measured the same gate at **365.20s** and attributed it to 2765
vendored `.lake` files, then **edited the file** — P2.1 independently observed
its mtime move to 10:53:37, i.e. **between P2.3's two runs**. The likeliest
account is that P2.3 measured the pre-fix gate, then the post-fix gate, not a
cache effect. No agent asserted this; it only appears when the three reports are
laid side by side. Neither the 60s nor the 365s figure was produced by an
instrument that knew the file was changing underneath it.

**5.2 — The wave measured a moving corpus, repeatedly, and the instruments
caught it.** `check_d6_equiv_d0` went green→red because another agent wrote
`D6≡D0` twice into `NEW_FINDINGS_AUDIT_2026_08_06.md` (P2.3, P2.1). P1.4 had a
figure fail to reproduce and moved all its measurement to committed HEAD. The
census moved **422/107 → 433/118** between P1.1's run and this receipt's
(§2 rows 25–26, one hour apart). Any figure in this wave without a timestamp is
already wrong.

**5.3 — The plan's four-way taxonomy has no cell for what P2.1 found.**
`check_generative_base` is not CANNOT-FAIL — weakening `reduced()` trips it —
but its exhaustive bound can be cut 10→4 and its grid 25×25→3×3 and it prints
**PASS with the shrunken numbers in its own success line**. P2.1 had to add
SOUND-BUT-BLIND. A reader who trusts "PASS" learns nothing about how much was
checked.

**5.4 — The sound-gate pattern already exists in the corpus and was never
propagated.** `check_g2_normal_form` catches both a model mutation and the
shrinking of its own declared bound, because it checks against an **independent
reference** and carries a self-monitoring harness. Its sibling in the same
directory, on the same subject, catches neither, because it computes claim and
reference from the same function.

**5.5 — A published diagnosis did not become a swept fix.**
`check_established.py`'s own header, dated 2026-08-05, records the
NameError-kills-a-checker lesson verbatim. Two more live instances were sitting
in the tree the next day, plus a third from an unfinished `reopened →
investigations` rename. A ten-second smoke run over every checker finds all four.

**5.6 — One agent committed, in the act of measuring, the defect it was
measuring — and caught itself.** P2.1's first harness returned 8 CANNOT-PASS;
seven were artefacts of treating "still red on a minimal tree" as unreachability,
and two of those were tracebacks being counted as verdicts. Corrected to 1.
Recorded here because the correction, not the number, is the finding.

**5.7 — P1.4's verdict is not the verdict the plan's question presupposed.**
Measured: "rulings do not take effect when made" is **false** (R1 doctrine 24→3
inside the ruling commit); "spontaneous half-life is infinite" is **true but
tautological** (files do not edit themselves); "it is regrowing" is **false as a
doctrinal claim** (+7 is 100% receipt zone). What is architectural is narrower:
the **public mirror has no propagation path at all**, and sweeps are
signature-scoped and file-blind. A naive carrier census over-counts by roughly an
order of magnitude because the tombstone, the registry row, the receipt and the
archive all carry the string they retire.

**5.8 — A live DF-22 instance was found inside the corpus's own published
surface.** `00_THE_AMRITA.md:186`, `04_WHAT_DIED.md:163` and
`06_WHAT_IS_STILL_OPEN.md:28` publish 362 files / 349 HTML; recomputed, 15
files / 1 HTML. The sweep falsified the figure and the figure was not re-run.

**5.9 — Work-order duplication across overlapping waves.** The tree contains
**two** P2.1 instruments (`mutation_test_gates.py` + `GATE_MUTATION_SURVEY`, and
`mutation_test.py` + `GATE_MUTATION_REPORT` + `MUTATION_TEST_GATES.md`) over
three different gate denominators (22 / 26 / 27), **two** P2.3 artefact sets
(`_run_standing_gate_figure.*` and the committed `gate_health.*`), and **three**
P1.4 documents (`PROPAGATION_ARCHITECTURE_FINDING`, `CENSUS_HALFLIFE_FINDING`,
`CENSUS_HALFLIFE_3_RULINGS`) whose own frontmatter attributes them variously to a
"4-agent wave" and an "8-agent wave (P1.1, P1.2, P1.4, P2.2, P2.3, B3, B6)". The
six-agent framing this receipt was given does not match what is on disk. Two
agents also edited each other's files mid-run (P2.1 reports its harness being
edited by another agent; it re-ran and verdicts held).

**5.10 — Small factual defects found in passing, not repaired:**
- `05_COSMOLOGY/03_FORMAL_SYSTEM/57_THE_POTENTIAL_READING.md` cites
  `00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md`
  at lines **51, 264 and 350** (P2.1 reported one; **V-R: three**). Neither the
  file nor the directory `00_HANDOFF/constitutional/` exists.
- `STANDING_GATE_FIGURE_RUN_2026_08_06.md` §7 attributes the `reopened_ids`
  NameError to `check_foundation.py:705`; its own §9 and P2.1 both place it at
  `check_claim_status.py:705`. A transcription slip in a tier-`[A]` row.

---

## 6 · Commit status

**This receipt commits nothing and stages nothing.** It creates exactly one file:
`00_HANDOFF/PLAN_EXECUTION_WAVE_RECEIPT_2026_08_06.md`. No `git add`, no
`git add -A`, no commit was run by this task.

**V-R at 11:09 ICT — `git diff --cached --stat` is empty; nothing is staged.**
The wave's working-tree state at that moment:

```
 M 00_META/registers/CORPUS_INDEX.jsonl
 M 09_TOOLS/01_SCRIPTS/check_foundation.py          <- P2.2
 M 10_SEED/01_THE_SEED_LADDER/D6_THE_RETURN.md
?? 00_HANDOFF/CENSUS_HALFLIFE_3_RULINGS_2026_08_06.md
?? 00_HANDOFF/CENSUS_HALFLIFE_FINDING_2026_08_06.md
?? 00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md     <- P1.1
?? 00_HANDOFF/CHECK_FOUNDATION_QUOTE_FIX_2026_08_06.md   <- P2.2
?? 00_HANDOFF/GATE_MUTATION_REPORT_2026_08_06.md
?? 00_HANDOFF/GATE_MUTATION_SURVEY_2026_08_06.md    <- P2.1
?? 00_HANDOFF/MUTATION_TEST_GATES_2026_08_06.md
?? 00_HANDOFF/NEW_FINDINGS_AUDIT_2026_08_06.md
?? 00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md  <- P1.4
?? 00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md      <- P1.2
?? 00_HANDOFF/STANDING_GATE_FIGURE_2026_08_06.md    <- P2.3
?? 00_HANDOFF/STANDING_GATE_FIGURE_RUN_2026_08_06.md<- P2.3
?? 00_HANDOFF/_run_standing_gate_figure.py/.sh      <- P2.3
?? 09_TOOLS/01_SCRIPTS/check_ruling_landed.py       <- P1.2
?? 09_TOOLS/01_SCRIPTS/mutation_test.py
?? 09_TOOLS/01_SCRIPTS/mutation_test_gates.py       <- P2.1
?? B3_TODO.md
```

**One exception must be recorded, not smoothed over.** HEAD advanced during the
wave. `f68287b4` — *"feat(tools): P2.3 — gate_health.py (standing pass/fail/hang
figure)"*, 11:08:19, 4 files / 1051 insertions
(`gate_health.py`, `gate_health.json`, `gate_health.md`,
`02_COMPILERS/test_gate_health.py`) — is a **P2.3-labelled commit**, alongside
`f3e7c1ab` (P4 B3) and `0f10f3e5` (B3 receipt) at 11:07 and 11:03. This receipt
did not make them and cannot say which lane did. Every other artefact above is
working-tree only, pending K2.

**Nothing in this wave changes a claim tier, ratifies an instrument, or
authorises a publication act.** Six instruments and measurements exist; K2
disposes.

•   ⊙   ○
