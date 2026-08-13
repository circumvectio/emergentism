---
title: "The Titan Pass — 2026-08-06"
status: "STAGED MANIFESTS — unratified. Nothing moved, nothing deleted, nothing staged in git. Every entry is a PROPOSAL requiring chair disposition."
date: 2026-08-06
evidence_tier: "[B] corpus facts re-run this pass; each cited claim retains its own tier"
owner: "No owner. This folder holds proposals. It may never be cited as authority."
seat: "L4 — Kṣatriya, executor. Wrote manifests only."
head: 00e68c83
---

# 15_THE_TITAN_PASS_2026_08_06

## What this is

Four manifests naming what the corpus should keep, retire, delete, and build,
compiled from **six seat reports — 154 entries** — and re-verified at HEAD `00e68c83`.

- `01_PRESERVE.md` — Viṣṇu (~~). What must be held, and the attack each entry survives.
- `02_ARCHIVE.md` — Śiva (−−). True once, superseded now. Successor named, or filed OPEN.
- `03_FALSE.md` — the deletion staging list. Counterexample required per entry.
- `04_CREATE.md` — Brahmā (++). What must be built, and what must be abandoned to build it.

## NOTHING WAS MOVED OR DELETED

No file was moved, renamed, deleted, or staged in git by this seat. No commit was
made. The only writes are the five files in this directory.

**Observation, not attribution.** At the time of this pass the working tree carried
six uncommitted modifications, mtimes 11:23–11:45 ICT today, four of them gate
instruments — `00_META/claim_cards/one_sitting.yaml`, `00_META/claim_status/CLAIM_STATUS.yaml`,
`09_TOOLS/01_SCRIPTS/check_claim_status.py`, `check_contradiction_census.py`,
`check_foundation.py`, `check_generative_base.py`. This seat did not write them.
Recorded because a pass about custody may not leave an unexplained working tree
unrecorded. **VERIFIED (L4)** — `git status --porcelain`, `ls -lT`.

## The law this pass ran under

1. **Move nothing, delete nothing, commit nothing.** Manifests only.
2. **Ruthless at falsity, not at inheritance.** FALSE → dissolve. INHERITED → preserve
   and cite; prior art is a citation duty, never a defect. SUPERSEDED → archive with its
   successor named. OVERSTATED → narrow to the defensible form and keep it.
3. **Every entry carries `file:line` and a disposition reason.**
4. **Re-run every count** (DF-22, the escorted number). No figure is re-quoted bare.
5. **Stop at owner boundaries.** Tier changes, ratification, publication, and anything
   touching a signed ruling are chair acts. Named, not performed.

## Coverage — ALL SIX LANES PRESENT

| seat | frame | entries | headline |
|---|---|---|---|
| L1 — Caṇḍāla | boundary / firewall | 31 | 26 live-vs-live contradictions confirmed on disk |
| L2 — Śūdra | truth-cut | 16 | **six** genuinely FALSE items survive a hostile pass |
| L3 — Vaiśya | audit | 21 | of 72 claim cards only 15 fully resolve (its method) |
| Śiva (−−) | dissolution | 32 | 19 ARCHIVE — 5 ABSORBED, 6 SUPERSEDED-IN-PLACE, 8 SPENT |
| Viṣṇu (~~) | preservation | 39 | 22 survive a hostile competent attacker |
| Brahmā (++) | creation | 15 | 9 to build, 4 to abandon in order to build them |
| | **total** | **154** | |

**Custody note on this receipt.** The first draft of these manifests was written
single-lane. One seat report reached this seat's instruction stream; the other five
were lost to a `slice(0, 30000)` truncation in transport, which cut the payload
mid-JSON. **That was a transport failure in the orchestrator, not a gap in the pass** —
all six reports existed, complete, on disk, and were recovered and folded in before
these files shipped. The distinction is recorded because a pass about warrant
substitution may not silently repair its own evidence chain.

**Second custody note, and it is the same defect class as the truncation.**
**Three sessions wrote into `15_THE_TITAN_PASS_2026_08_06/` and none of them knew the
full set.** The executor seat drafted all five files single-lane from the one report it
received; other sessions then recovered the six reports and rewrote every one of the
five files, each rewrite landing under a different seat than the one that drafted it.
**VERIFIED (L4)** by repeated `ls -lT` / `stat` snapshots taken during the pass, in
which the five files changed under this seat between reads, in an order no single
writer produced.

*No timeline is published here.* The obvious thing to write — a tidy list of five
timestamps — would be an **escorted number**: the mtimes moved again while this very
paragraph was being written, and any sequence quoted would be false by the time it was
read. **The verified claim is the one that survives: the files changed under a seat
that was reading them, more than once, from more than one writer.**

Two consequences, both recorded rather than smoothed:

1. **A live contradiction existed inside this receipt and was repaired by a writer who
   could not see the seat reporting it.** `03_FALSE.md:26` read *"The pass was specified
   as six seat reports. **One arrived**, truncated"* while `README.md` §Coverage already
   read **ALL SIX LANES PRESENT**. The executor seat caught it and reported it; a third
   session had already fixed it. **Nobody was wrong; nobody could see.**
2. **Every write in this directory was a blind overwrite that happened not to collide.**
   The executor's rewrites of `01`, `02` and `04` were each rejected by a
   modified-since-read guard — *the guard, not the discipline, is what prevented three
   clobbered manifests.*

**This is not a content failure and it is not a discipline failure. It is
`04_CREATE.md` C-05's argument, executed on this receipt: when two writers cannot see
each other, the only thing that keeps a record honest is a locator a machine can
check.** A pass whose subject is unverified provenance may not leave its own provenance
unverified.

## Disposition totals across the six lanes

| disposition | entries |
|---|---|
| PRESERVE | 46 |
| ARCHIVE | 37 |
| FALSE | 29 |
| CREATE | 24 |
| OWNER (chair act named, stopped at) | 18 |

**VERIFIED (L4)** — `collections.Counter` over the recovered report set.

OWNER is not a fifth disposition. It marks proposals whose disposition is a chair act:
tier change on a signed surface, a constitutional call, or a definition that fixes a
published metric. They are carried in the manifest where their mechanical part belongs.

## The counts

Provenance mark on every figure: **VERIFIED (L4)** = a command run by this seat in this
task · **VERIFIED (seat)** = a command run by the named seat, reported with its command,
not re-run here · **UNVERIFIED** = carried, no command.

### Corpus size — VERIFIED (L4)

| figure | value | command |
|---|---|---|
| live `.md` (excl. `90_ARCHIVE`, this folder) | **1706** | `find . -name "*.md" -not -path "./90_ARCHIVE/*"` |
| live `.html` | **803** | same form |
| of the live `.md`, in `91_COMPATIBILITY` | **212** (12.4%) | `find 91_COMPATIBILITY -name "*.md"` |
| root-level `.md` | **23** | `ls -1 *.md \| wc -l` — `README.md:116` publishes **22** |
| `90_ARCHIVE` subdirectories | **27** | `ls -1d 90_ARCHIVE/*/` — `00_WORK_IN_PROGRESS/README.md:25` publishes **24** |
| public-site routes | **400** | `find 12_PUBLIC_SITE -name index.html ! -path '*/.vercel/*'` — `00_THE_LAUNCH_PLAN.md:24` publishes **391** |

> **R-22 note (2026-08-13).** The live-`.md` denominator **1,706** above is
> superseded and was stale in both directions: its command re-runs to **1,727**
> today, and its exclusion rule misses 93 files inside eight NESTED
> `90_ARCHIVE` directories under live pillars (plus vendored `.lake`). Per
> CHAIR ruling `R-22`, the governing denominator is **1,385** — the builder's
> own walk rules, `09_TOOLS/01_SCRIPTS/build_corpus_index.py:38-41`, the only
> scope contract that exists in code — and every count is to be quoted with
> its exclusion rule attached. The figures above stand as measured on their
> date; they are not to be re-cited as corpus size.
> Receipt: `00_HANDOFF/WAVE_0_RULINGS_RECEIPT_2026_08_13.md`.

### Emblem census — the seed figure "362 files / 349 .html" — VERIFIED (L4)

| figure | value |
|---|---|
| retired literal `⊙ = • × ○` carriers in `12_PUBLIC_SITE/` | **16** |
| of those, `.html` | **2** |
| carriers in `12_PUBLIC_SITE/.vercel/` | **0** (doc claims a further 338) |
| `.html` under `.vercel` (total) | **388** |
| census script: total / live / public / public_html / html-doctrinal | **435 / 115 / 13 / 2 / 0**, exit 1 |

Published figure under audit: **362 / 349** at `06_WHAT_IS_STILL_OPEN.md:28`,
`04_WHAT_DIED.md:163`, `00_THE_AMRITA.md:186`, `05_THE_METHOD.md:229,497`,
`12_PUBLIC_SITE/5/index.html:154`, `4/index.html:191`.

**One census, five live values.** 362 · 349 · 107 (`00_THE_AMRITA.md:53`, dated today,
published *with* its command) · 115 (census "live") · 124 (Viṣṇu's corpus-wide grep,
VERIFIED (Viṣṇu)) · 13 (census "public site", VERIFIED (L4)). The claim that the
retired form is over-published survives at **every** one of those numbers. The numbers
do not. See `03_FALSE.md` F-02 and `04_CREATE.md` C-02.

### Locator integrity — VERIFIED (L4), independent script

Backticked `` `path:NN[-MM]` `` citations in live `.md`, resolved citing-dir-first then
repo-root; `90_ARCHIVE`, `.lake`, `node_modules`, `.vercel`, `.git`, this folder excluded.

| figure | value |
|---|---|
| resolvable `path:line` citations checked | **1127** |
| citations whose line number **overruns** the target | **386** |
| of those, in `…/133_ROSETTA_COUNCIL_RAW` | **362** |
| outside that one directory | **24** |

Reproduces L1's figures exactly by an independently written script.
Brahmā's wider census — **1918** inline citations, **725** with no resolvable target,
**398** overrunning of 1193 resolvable, **257** basename-ambiguous — is
**VERIFIED (Brahmā)**; the two scripts differ in resolution policy and both are
reported. **Neither number may be quoted without its method.**

### Claim-card custody — THREE METHODS, DELIBERATELY NOT RECONCILED

**The unit is the CARD, not the card SET.** The widely-quoted "7 of 12 broken" counts
**card files**. There are **72 cards** across **12 sets** — the file-level figure
understates the damage roughly six-fold.

| method | OK | SHA DRIFTED | ANCHOR MOVED | TARGET MISSING | broken |
|---|---|---|---|---|---|
| **A** — anchor exactly at `line_start` (L4) | **10** | 5 | 29 | 28 | **62** |
| **B** — anchor anywhere in `line_start..line_end` slice (L4) | **15** | 3 | 26 | 28 | **57** |
| **C** — orchestrator's verifier | **20** | 21 | 3 | 28 | **52** |

Methods A and B are **VERIFIED (L4)**; method C is **VERIFIED (orchestrator)**.
L3 independently measured **15 fully resolving (20.8%)** — which method B reproduces
exactly. **TARGET MISSING = 28 in all three methods**; that is the firm number.
The three OK figures are *not* reconciled here on purpose: collapsing them into one
would be the escorted number. The chair must pick a strictness standard — that is
`04_CREATE.md` C-03.

File-level, **VERIFIED (L4)**: 12 sets · 5 sha match · 3 sha mismatch · 4 source path
absent · **7 of 12 broken at source level** · `compile_claim_cards.py` →
`CLAIM CARD CONTRACT: FAIL`, halting on the first defect (`OS01-03`).

**And 20 of the 28 "missing" cards are not dead.** L3's counter-finding, re-verified by
this seat: the host pillar was reorganised, `../02_SKYZAI/03_AIA/EMERGENTISM_AIA/` →
`02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/`.
Under that single prefix rewrite `reciprocal_infinite_play` (7), `sarpasya_vijayam` (7)
and `self_eating_serpent` (6) all exist **and hash byte-exact to their declared
`reviewed_source_sha256`** — the review those cards record is still valid, only the
address moved. `six_lenses` (8) exists but hashes differently on that lineage; L3
locates a byte-exact match in a second lineage, which makes it a custodial-lineage
question for the chair. **VERIFIED (L4)** — sha256 comparison per card set.
Killing these 20 for unreachability would have destroyed sound cards over a rename.

### Gate state — VERIFIED (L4)

| figure | value |
|---|---|
| `check_*.py` on disk | **27** |
| wired in `gate.sh` — **by basename** | **21** |
| wired in `gate.sh` — **by full path** | **20** |
| on disk but not wired | **6** |
| un-wired names | `check_contradiction_census.py`, `check_dead_citations.py`, `check_forwarding_stubs.py`, `check_g2_normal_form.py`, `check_ruling_landed.py`, `check_tree_contract.py` |
| `gate.sh` (LEAN+SLOW skipped) | **exit 1**, **16 FAIL** rows, 9 PASS |
| `predeploy_check.py` | **597 errors** |
| `check_emergentism_purity.py` | **945** tokens across **49** live files |
| `check_receipt_citations.py` | **94** ambiguous receipt numbers (baseline 91) |
| `check_dead_citations.py` | **13** dead citations across **896** live documents |
| `check_forwarding_stubs.py` | **5** violations across **79** stubs |
| `check_g2_normal_form.py` | **PASS, exit 0** |
| duplicate numeric prefixes in `11_UPLINK` | **111** |

27 − 20 = 7 but only **6** are un-wired: `check_no_secrets_staged.py` is invoked by bare
name, not by path. Both numbers are right for their method. `STANDING_GATE_FIGURE_2026_08_06.md:27`
publishes **26 / 22 / 4**. **Four live values for one inventory** — see `03_FALSE.md` F-05.

### Registers and Lean — VERIFIED (L4)

| figure | value |
|---|---|
| `FILE_REGISTER.json` `len(entries)` / declared | **3617 / 3617** — internally consistent |
| `FOLDER_REGISTER.json` | **815 / 815** — internally consistent |
| published at `06_WHAT_IS_STILL_OPEN.md:61` | **3600 / 814** — stale against disk |
| rows under `14_THE_DISTILLATION/` | **8** of 9 files; `00_THE_RUNGS_2026_08_05.md` **absent** |
| `grep -c "^theorem "` in `EmergentismCheck.lean` | **20** — matches `00_ESTABLISHED/README.md:73` **exactly** |
| `check_established.py` | **PASS, exit 0** |

L3's register audit — **614 of 3617 recorded sha256 values (17.0%) stale, 0 dangling
entries** — is **VERIFIED (L3)**. The register reports its own staleness correctly;
this is drift, not laundering.

### The line-shift proof — VERIFIED (L4)

| figure | value |
|---|---|
| `git diff 7e0ec4c7~1 7e0ec4c7 -- 00_ESTABLISHED/README.md` | **+3 lines** of `rosetta:` frontmatter |
| `grep -n "open general claim"` | **103** (citations say 100) |
| `grep -n "remains open until"` | **117** (citations say 114) |
| `:121` (`Z1` row) now at | **124** |
| `grep -n "μ-contract"` | **134** (citations say 131) |
| live citing **lines** carrying a sheared locator | **12** |
| live citing **files** | **6** (5 in `14_THE_DISTILLATION`, 1 in `00_HANDOFF`) |
| `00_ESTABLISHED/README.md` length | **155** |

### The distillation's own withdrawal clause — VERIFIED (L4)

`01_WHAT_IS_PROVED.md:5` binds the folder's anchors to HEAD `10b8890f` and to no other
disk state. `git rev-parse --short HEAD` → **00e68c83**. `grep -c "2026-08-06"` per file:
`00_THE_AMRITA` 4 · `00_THE_RUNGS` 4 · `04_WHAT_DIED` 1 · `06_WHAT_IS_STILL_OPEN` 1 ·
**`01_WHAT_IS_PROVED` 0 · `02_WHAT_IS_CHOSEN` 0 · `03_WHAT_IS_READ` 0 · `05_THE_METHOD` 0 ·
`README` 0.** Five of nine carry no trace of today. By its own clause the folder has
withdrawn itself. Withdrawal or re-anchoring is mechanical; neither is this seat's act.

## Where the six reports CONFLICT — SURFACED, NOT RESOLVED

Resolution is a chair act. Each row is a live disagreement between careful seats.

| # | conflict | side A | side B |
|---|---|---|---|
| 1 | **Claim-card OK count** | L3 / L4-method-B: **15** resolve | orchestrator: **20** · L4-method-A: **10** |
| 2 | **Claim-card unit** | "7 of 12 broken" (card **files**) | ~**52–62 of 72** broken (**cards**) — six-fold understatement |
| 3 | **Are the 4 orphaned card sets dead?** | L1: dead pointer + boundary violation, FALSE | L3 + L4: **20 of 28 recover by pure path substitution, sha byte-exact** — PRESERVE |
| 4 | **Gate inventory** | `STANDING_GATE_FIGURE`: 26/22/4 | L1: 27/20/7 · Viṣṇu + L4: **27/21/6** |
| 5 | **`gate.sh` FAIL rows** | L1: **13** | L4: **16** (adds `check_links.py`, `build_receipt_disambiguation.py`, `build_magnum_opus_register.py --check`) |
| 6 | **Can G2 be re-admitted to `00_ESTABLISHED` §A?** | L1 + Viṣṇu: `check_g2_normal_form.py` **may now satisfy** the standard — chair act | Brahmā: **no promotion is available** — the checker's own last line says "a bounded check of the dictionary, not a proof", so criterion COMPLETE fails; the register is **right** to keep it out |
| 7 | **Is a stub forwarding into `90_ARCHIVE` a defect?** | Śiva: the two-hop and three-hop chains must dissolve | L3: the 60 archive-terminating stubs are a **ratified tombstone protocol** that disclaims ownership — not defects; the real violation is `parents:` edges (3 of 11), which are authority |
| 8 | **Are the 148 dead links a laundering gate?** | brief's premise | L3 counter-finding: **all 148** fall in `check_links.py`'s declared, reasoned SKIP_DIRS; in-scope health is 1 broken of 3586 — **the gate is honest** |
| 9 | **Retired literal `⊙ = • × ○` half-life** | `CENSUS_HALFLIFE_FINDING:39`: **18 d 4 h** (ruled 2026-07-19) | `CENSUS_HALFLIFE_3_RULINGS:64`: **4 d 16 h** (ruled 2026-08-01) — same commit, same day, 4× apart |
| 10 | **`P = Φ × V`** | `00_THE_CLOSED_READING_LOOP_v0.1.md:103`, **K2-signed**: `[S]` doctrinal, "the multiplicative shape is load-bearing" | KSC-02 / `00_THE_RUNGS:704`: **killed as a ranking** — later ruling vs signature |
| 11 | **Dyadic-gate threshold** | `00_THE_EXTRACTION_LAW.md:117`: `Δ ≥ 0` (non-decrease) | `D5_THE_GAME.md:106` + `00_THE_WELTANSCHAUUNG.md:420`: strictly **rise** — the zero-delta bearer is admissible under one and fails the other |
| 12 | **Do line numbers bind?** | `check_active_receipt_citations.py:16`: "line numbers are hints for people" | `claim-card.schema.yaml:5` + `compile_claim_cards.py`: required contract field, fails closed. **There is no third reading in which nothing changes.** |
| 13 | **`VMOSK_A.md` inbound** | Śiva demand census: **37** doctrinal citers vs 5 for its successor | L4 raw grep: **82** files mention it vs **4** for the successor — method differs, direction identical |

## What this pass did not do

- Did not survey `02_SKYZAI`, `90_ARCHIVE`, or anything outside `01_EMERGENTISM`
  except to resolve four claim-card source paths.
- Did not rule on any tier, ratify anything, or touch a signed document.
- Did not resolve a single conflict.
