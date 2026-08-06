---
title: "Propagation architecture — is zero propagation architectural, or one bad week?"
status: "[D] MEASUREMENT — unratified. Numbers recomputed 2026-08-06 at HEAD 1a83affc; re-run before citing."
type: measurement-finding
work_order: "P1.4"
evidence_tier: "[D] receipt of measurement. No claim tier is changed by this document."
canonical_phrase: "Rulings land in doctrine at ruling time; sweeps are dispatched per-signature, so a file opened by one sweep is never checked against any other ruling"
---

# P1.4 — Propagation architecture

**Measured 2026-08-06, HEAD `1a83affc`.** Every number below came from a command
run in this pass. Nothing is carried from the prompt. Zone rule used throughout:
`archive` = path contains `90_ARCHIVE` or `91_COMPATIBILITY`; `receipt` =
`11_UPLINK/` or `00_HANDOFF/`; `public` = `12_PUBLIC_SITE/`; `doctrine` =
everything else. File extensions `.md` and `.html`. Carriers are **files**, not
occurrences.

---

## 1. Do I trust `measure_propagation_halflife.sh`?

**Partly.** Its headline reproduces; two defects make its output not the thing
its header says it is, and a third makes its framing misleading.

I re-ran it in full. `1c270dbd~1` → `725  70  360` reproduces exactly.

### Defect 1 — the last row is not HEAD (zsh off-by-one)

The header says the unbound-variable bug was "fixed at landing: revs has indices
0..n-1." That is the **bash** convention. The script is `#!/bin/zsh` and zsh
arrays are **1-indexed**, so `revs[$((n-1))]` is the penultimate commit:

```
$ zsh -c 'revs=($(git rev-list --reverse 1c270dbd..HEAD)); n=${#revs[@]}
  echo "revs[0]  =[${revs[0]}]"; echo "revs[n-1]=[${revs[$((n-1))]}]"
  echo "revs[n]  =[${revs[$n]}]"; echo "true HEAD=[$(git rev-parse HEAD)]"'
revs[0]  =[]
revs[n-1]=[71f205c2e3bc76b81605018bf9dea72ba66e0e97]
revs[n]  =[1a83affc6595bee9672c58d28e5837ab6ea669c6]
true HEAD=[1a83affc6595bee9672c58d28e5837ab6ea669c6]
```

The script's final row is `71f205c2`, not HEAD. The sampling loop
(`for ((k=step; k<n; k+=step))`) also never reaches index `n`, so HEAD is never
sampled by any path. Every "carriers today" figure it prints is one commit stale.

### Defect 2 — the x-axis is not time

`git rev-list --reverse` returns reverse-topological order, not date order. The
run's own output goes 2026-08-01 → 2026-07-12 → 2026-07-16 → 2026-07-19 →
2026-07-22 → 2026-08-02 → 2026-08-03… A "half-life" read off that column is a
decay-per-commit-index curve, not a decay-per-day curve. My instrument samples by
date instead (`git rev-list -1 --before="<date> 23:59:59" HEAD`).

### Defect 3 — the headline number is 95% not-doctrine

`725` is the `total` column, which includes the archive. Decomposed at the same
commit:

```
$ git grep -lI '⊙ = • × ○' 1c270dbd~1 -- '*.md' '*.html' | ...zones...
doctrine=6  receipt=64  public=359  archiveANY=296  TOTAL=725
```

Six. Six doctrine files carried the form at the moment of retirement. The other
719 were the public mirror (359), the receipt trail (64), and the archive (296) —
and the archive is where the corpus's own standing discipline **requires**
retired wording to live ("Historical receipts, quotations, compatibility paths,
and explicit tombstones may preserve retired wording").

**Verdict on the instrument:** trustworthy as a `git grep` harness, untrustworthy
as a half-life. It counts a licensed tombstone and a lagging doctrine page as the
same event. Every conclusion below rests on splitting those apart.

---

## 2. The three rulings

Chosen for clearly different ages and clean disjoint signatures. Ruling commits
identified by `git log -S` on the registry.

| | ruling | ruled | commit | age | superseded signature | ruling signature |
|---|---|---|---|---|---|---|
| **R1** | `KSC-11` canonical spelling | 2026-07-22 | `fbf78536` | 15 d | `Egregorotype` | `Egregoreotype` |
| **R2** | `KSC-05`/HR-1 μ-candidacy test | 2026-07-29 | `1d60ef19` | 8 d | `dimension[- ]gain` | `reducibility\|formally reducible` |
| **R3** | `KSC-28`/Q2 sphere **selection** | 2026-07-31 | `a2e022c6` | 6 d | `sphere primacy` | `sphere selection` |
| **R0** | `KSC-04` retired infix (control) | 2026-08-01 | `1c270dbd` | 5 d | `⊙ = • × ○` | `•  ⊙  ○` |

The signatures are disjoint: `Egregoreotype` does not contain the substring
`Egregorotype` (position 8 differs, `e` vs `o`).

---

## 3. Carriers today

One command block, HEAD `1a83affc`, 2026-08-06:

```
signature                                      doctrine  receipt  public  archive   TOTAL
-- SUPERSEDED forms --
R1 sup: Egregorotype                                  3        8       9        8      28
R2 sup: dimension[- ]gain                             4        4       2        0      10
R3 sup: sphere primacy                                8        5       1        0      14
R0 sup: ⊙ = • × ○                                    14       76      11      301     402
-- RULING forms --
R1 rul: Egregoreotype                                66        6       3       16      91
R2 rul: reducibility|formally reducible              51        6      11       18      86
R3 rul: sphere selection                              4        1       0        0       5
R0 rul: •  ⊙  ○                                     222       55     353       19     649
```

### Movement over time (sampled by date, ruling day → today)

**R1** — doctrine collapsed on the ruling day, then froze:

```
date        commit      doctrine receipt public archive TOTAL
2026-07-21  4154ebeb16       24      17      9       1     51
2026-07-22  b6ada7a2bc        3       8      9      18     38   <- ruling day
2026-07-23 … 2026-08-06       3       8      9     18→8  38→28
```

24 → 3 doctrine in the ruling commit itself. Then **flat at 3 for fifteen days**.
Public **flat at 9 for fifteen days**.

**R2** — the count went **up** and stayed up:

```
2026-07-28  37d27562e4        0       0      1       0      1
2026-07-29  87bd12f026        3       3      1       0      7   <- ruling day
2026-07-30  83fbea5fb0        4       4      2       0     10
2026-08-06  1a83affc65        4       4      2       0     10
```

**R3** — same shape:

```
2026-07-28  37d27562e4        0       0      0       0      0
2026-07-29  87bd12f026        6       3      0       0      9
2026-07-31  577816880d        7       5      1       0     13   <- restatement
2026-08-06  1a83affc65        8       5      1       0     14
```

A naive carrier census would score R2 and R3 as **catastrophic negative
propagation**: retiring a form multiplied its carriers tenfold and infinitely.
That reading is wrong, and §4 is why.

---

## 4. Use vs mention — the split the census does not make

Every hit line for R2 (10 files) and R3 (14 files), all 24 public hit lines for
R1, and all doctrine hit lines for R0 were read individually. Small enough to
classify by hand rather than by heuristic.

| | live carriers | licensed (tombstone / repair text / frozen receipt filename / taxonomy owner) | **bare lagging use** |
|---|---|---|---|
| R1 doctrine | 3 | 3 | **0** |
| R1 public | 9 | 0 | **9** (24 lines) |
| R2 all | 10 | 10 | **0** |
| R3 all | 14 | 12 | **2** (half-glossed) |
| R0 doctrine | 14 | 10 | **4** |
| R0 public | 11 | — | not classified |

- **R1 doctrine's 3** are: the filename-stability note in
  `05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md` ("Filename retains
  Egregorotype only for link stability; Egregoreotype is canonical spelling"), the
  compatibility alias in `D33_EGREGORES.md`, and a kintsugi spec listing the
  spelling question. All three explicitly name the legacy form *as* legacy.
- **R2's 10** are all repair apparatus: `49:113` "Doc 48 retains dimension gain as
  one diagnostic but has withdrawn it as a…", `42:533` "a dimension-gain
  instrument had nothing to report", the KSC-05 row itself, four receipts, and one
  public page saying "retiring the dimension-gain reading in…". One public hit
  (`riemann/index.html:101`, "the one real dimension gained over the line") is a
  **grep false positive** — plain geometry, not the μ-criterion.
- **R3's 14** are 9 citations of the frozen receipt filename
  `175_SPHERE_PRIMACY_RULING_EXECUTED_2026_07_29.md`, the KSC-28 row, and 3
  supersession notes. The 2 half-glossed: `00_ESTABLISHED/README.md:138` and
  `12_PUBLIC_SITE/established/index.html:486`, both of which write "sphere
  primacy" and then immediately say it is a selection.
- **R0's 4 bare** are closing-emblem lines, unmarked, in
  `00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md:118`,
  `THE_HOLOBIONT_BOUNDARY_CLARIFICATION.md:154`,
  `THE_HOLOBIONT_MOODS_BRIEFING.md:163`, `THE_HOLOBIONT_PARTS_BRIEFING.md:166`.
  Each sits alone after a `---` rule — the document signature line.

### The "+7 regrowth" is entirely the repair apparatus

```
R0 @ sweep 2828be05 : doctrine=14  receipt=69  public=11  archive=301  TOTAL=395
R0 @ TRUE HEAD      : doctrine=14  receipt=76  public=11  archive=301  TOTAL=402
```

Receipt zone `69 → 76` = **+7**. Doctrine flat at 14. Public flat at 11. The
census's regrowth signal is the sweep writing down that it swept. Doctrine did
not relapse by a single file.

---

## 5. What actually distinguishes the three — the mechanism, proved

R1, R2 and R3 look different in the raw counts and turn out to differ on **one**
variable: *was there a sweep, and what string was the sweep given?*

- R2 and R3 landed. Zero and two lagging carriers respectively, from a small
  surface. Their counts rose because a ruling **creates** carriers — the
  registry row, the receipt, the tombstone all name the thing they retire.
- R1's doctrine landed the same day. R1's **public mirror did not move at all**
  in fifteen days — 9 pages, 24 bare assertions, still shipping
  `Genotype → Phenotype → Extended Phenotype → Memotype → Egregorotype` as canon.
- R0's public mirror went `359 → 11` — but only via one dedicated sweep,
  `2828be05` ("emblem sweep (476→0) + product form sweep"), 352 files touched.

Now the decisive cross-check. **All nine** of R1's unrepaired public pages were
edited by that sweep, today:

```
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/trinity/36-the-dimensional-trophic-cascade/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/trinity/23-the-dac/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/trinity/06-the-cosmological-cycle/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/trinity/18-the-strange-attractor/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/formal/00-the-seven-axioms/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/operators/mf-282-the-operator-stack-correspondence/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/operators/mf-281-the-replicator-decomposition/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/value/00-theurgy-and-f5-force-map/index.html
TOUCHED-TODAY-AND-STILL-WRONG  12_PUBLIC_SITE/foundations/the-honest-position/index.html
```

Sharpest instance — `mf-281-the-replicator-decomposition/index.html`, one file,
today's sweep, 158 lines apart:

```
 89: Φ = Memotype × Egregorotype × Environment        <- KSC-11 legacy spelling, 15 days stale
247: P_node = min(Φ̂₄, V₄) decomposes into two ...     <- KSC-02 ruling form, repaired TODAY
```

The sweep opened this file, rewrote line 247 to the current ruling form, and left
line 89 carrying a retired form from a ruling made two weeks earlier.

**That is the architecture.** Repair is dispatched **per signature**, not per
file and not per document review. A file being open in an editor is not an
occasion to check it against canon. There is no step anywhere between "ruling
made" and "someone later greps for that exact string."

---

## 6. Ruling: architectural — but not the architecture the census named

**Architectural, on a narrower and more fixable claim than "rulings do not take
effect when made."**

Refuted by measurement:
- *Rulings do not take effect when made.* **False.** R1 doctrine 24→3 in the
  ruling commit. R2 and R3 landed with 0 and 2 lagging carriers. Doctrine is the
  fastest-propagating zone in the corpus.
- *Spontaneous half-life effectively infinite.* **True but tautological as
  stated.** Files do not edit themselves. The measurable claim is about *repair
  coverage*, and the corpus's is high in doctrine, near-zero in the public mirror.
- *It is regrowing.* **False as a doctrinal claim.** +7 is 100% receipt zone.

Established by measurement:
1. **The public mirror has no propagation path at all.** R1: 9 bare public
   carriers, unmoved for 15 days, `3` ruling-form vs `9` superseded-form. R0 after
   its sweep: `353` vs `11`. A ruling reaches the site if and only if someone
   dispatches a string sweep at the site.
2. **Sweeps are signature-scoped and file-blind.** Proved above: 9 files opened
   and left wrong on a different ruling; one file with a today-repair and a
   15-day-stale form 158 lines apart.
3. **Every naive carrier census over-counts by roughly an order of magnitude**,
   because the tombstone, the registry row, the receipt and the archive all carry
   the string they retire. R2 and R3 have a *negative* naive propagation score and
   are in fact clean.
4. **Corollary — the census numbers are themselves a live instance of DF-22.**
   `14_THE_DISTILLATION/00_THE_AMRITA.md:186`, `04_WHAT_DIED.md:163` and
   `06_WHAT_IS_STILL_OPEN.md:28` publish "362 files in `12_PUBLIC_SITE` carry the
   retired `⊙ = • × ○`, of which 349 are `.html`". Recomputed at HEAD this pass:
   **15 files, of which 1 is `.html`.** The sweep falsified the figure and the
   figure was not re-run. (Not repaired here — outside this work order's file
   scope.)

---

## 7. Recommendation — one mechanism

**Register the carrier set at ruling time.** A ruling does not enter the registry
until it carries `carriers_at_ruling`: the file list produced by its own
superseded-signature grep, computed *in the ruling commit*, before the ruling's
own tombstone and receipts exist. "Landed" is then a set difference, not a grep
count.

Why this one over the other two candidates:

- **Not a gate that fails while carriers remain.** It cannot distinguish use from
  mention, so it would fire permanently on the repair apparatus itself. Concretely:
  such a gate, applied at `1d60ef19` and `a2e022c6`, would have **blocked the very
  commits that made R2 and R3** — those commits raised the retired-form count from
  0→7 and 0→9. A gate whose first act is to reject the ruling is not a gate.
- **Not a "ruling made / ruling landed" status field.** It is a label for the
  problem, not a mechanism against it. It records that propagation is incomplete
  without producing the file list anyone would need to complete it, and someone
  still has to re-derive that list by grep — which is the current state.
- **The carrier set does three things neither other option does.** (a) It is
  computed once, at the only moment the count is uncontaminated by the ruling's own
  documentation — which is exactly the confound that made R2 and R3 unreadable.
  (b) It yields a finite, closeable worklist instead of an unbounded grep. (c) It
  makes the *public mirror* visible at ruling time: R1 would have shipped with
  `public: 9` on its face on 2026-07-22 instead of being discovered fifteen days
  later by a different agent looking for something else.

**Smallest useful addition on top** (same mechanism, no new concept): since sweeps
already open files, have any commit report the intersection of its touched-file
set with all open `carriers_at_ruling` lists. On `2828be05` that check would have
printed nine filenames. It is a set intersection over lists that already exist —
no new judgement, no new gate, no tier decision.

### Reconciliation with P1.2, which shipped the gate in parallel

While this measurement ran, a concurrent agent landed
`00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md` +
`09_TOOLS/01_SCRIPTS/check_ruling_landed.py` — the gate option. Read after my
recommendation was written; the conflict is smaller than it looks and I am not
withdrawing anything.

- My objection was to a gate that fails **while any carrier remains, corpus-wide**.
  That objection stands on the measurement: such a gate would have rejected
  `1d60ef19` and `a2e022c6`.
- The gate as actually built scopes its category to **`public_html`**, threshold 0.
  That sidesteps the objection precisely, because the repair apparatus — registry
  row, tombstone, receipts — lives in `.md` under doctrine and receipt, not in
  published HTML. On my numbers the scoped gate would fire correctly on R1 (9
  public carriers) and correctly stay silent on R2 and R3 (2 and 1 public
  carriers, both mentions).
- So P1.2's scope choice and this measurement agree independently on the same
  conclusion: **the public mirror is the zone with no propagation path**, and it is
  the right and only place to put a hard threshold.
- What the gate does **not** supply, and what §7 still recommends: the
  ruling-time carrier set. The gate answers "are there carriers now?" It does not
  produce the finite worklist, does not record the count before the ruling's own
  documentation contaminates it, and does not catch the file-blindness proved in
  §5 — a sweep can pass a public_html gate on the string it was sent to fix while
  leaving three other rulings stale in the same file. Registering
  `carriers_at_ruling` is additive to the gate, not an alternative to it.

---

## 8. What I could not do

- **I did not classify R0's 11 public carriers** use-vs-mention. Only the four
  rulings' doctrine and small-surface zones were read line by line.
- **`use` vs `mention` is a manual judgement here**, not a mechanical test. It was
  affordable because the live sets are 3–14 files. It does not scale, and I have
  no automatable substitute to offer — flagging that as an unsolved part of the
  recommendation rather than papering it.
- **One measurement did not reproduce.** An early worktree row for R1 read
  `public=18, TOTAL=37`; re-run twice minutes later it read `public=9, TOTAL=28`,
  matching HEAD and matching `git status` (0 dirty files under `12_PUBLIC_SITE`).
  Concurrent sessions are writing this tree. **All figures in this document are
  taken from committed objects at HEAD `1a83affc`, not from the working tree.**
- **`age` is age-since-ruling-commit**, not age since the idea was settled. R1's
  canonical spelling first appears in the corpus at `9a90d088` (2026-07-12), ten
  days before `KSC-11` was written. If the intent date is used instead of the
  registry date, R1's public mirror has been stale for 25 days, not 15.
- **No owner decision was taken.** Two are visible and left open: whether the
  frozen receipt filename `175_SPHERE_PRIMACY_RULING_EXECUTED_2026_07_29.md` (9 of
  R3's 14 carriers) counts as a carrier at all, and whether the stale 362/349
  figure in `14_THE_DISTILLATION` is repaired or receipted as superseded.

•   ⊙   ○
