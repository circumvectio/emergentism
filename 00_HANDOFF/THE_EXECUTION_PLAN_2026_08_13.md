---
title: "The Execution Plan — 2026-08-13, from the ten-lens census"
status: "ACTIVE — DISPATCH SURFACE. [S] throughout: this plan SELECTS an ordering. It creates no canon, settles no claim, and confers no authority to execute any item — the owner-class field does that. Supersedes the ordering of THE_EXECUTION_PLAN_2026_08_05.md; see §0."
date: 2026-08-13
evidence_tier: "[B] every count re-runnable by the command given and measured 2026-08-13; [S] the ordering and the wave structure; [I] the dependency reasoning in §1"
owner: "Dispatch. No work order here confers authority to perform it."
parents:
  - CENSUS_HANDOFF_2026_08_13.md
  - CENSUS_DOCKET_2026_08_13.json
  - THE_EXECUTION_PLAN_2026_08_05.md
---

# The Execution Plan — 2026-08-13

> **START HERE IF YOU ARE A NEW SESSION:**
> [`SESSION_CLOSE_2026_08_13.md`](SESSION_CLOSE_2026_08_13.md) records what was
> executed against this plan on 2026-08-13, the three current gate numbers, the
> next five actions with owners, and two live threads (the Spark deploy refusal
> and the podcast venture rename) that exist nowhere else in the corpus. Read it
> before this file — it is shorter and it says what has already moved.

**For an agent with none of the originating context.** Read §0, §1 and §6 before
touching anything. The census that produced this plan is at
[`CENSUS_HANDOFF_2026_08_13.md`](CENSUS_HANDOFF_2026_08_13.md); the item-level
data is in `CENSUS_DOCKET_2026_08_13.json`.

---

## 0 · What changed since the 2026-08-05 plan

That plan is **not superseded in its protocol** — its §0 anti-rederivation rules
still govern and are restated in §6 here. Its **work orders are partly spent**:

| 2026-08-05 work order | state on 2026-08-13 |
|---|---|
| `WO-A3` — *"not one document declares its register in frontmatter"* | **premise spent.** 55 now do — and its own verification step could not detect that, because `build_corpus_index.py:50` drops the declared value |
| `WO-A1` | **self-inconsistent.** Its heading says 177, its body says 134, and today's measurement says 20 |
| §0 protocol | **stands unchanged.** Re-read it |

**The 2026-08-05 plan was written from an assumption the census refuted:** that
the corpus's problem is unfindable *content*. It is not.

> **The content is in better shape than the instruments.** One byte-identical
> duplicate pair in 1,726 live documents. Zero case collisions. Zero malformed
> dates. The archive bucket collapsed from ~30 to 3 once the candidates were
> opened. **Five instruments publish a property they do not test.**

Plan accordingly: **repair the instruments before trusting any sweep they green-light.**

---

## 1 · The dependency that sets the order

Two of the 31 rulings are **upstream of almost everything else**. Neither takes
more than a few minutes, and until they land, work downstream of them is not
quotable.

```
        R-08  what does [S] mean?              R-22  which denominator governs?
     two incompatible live definitions      ten lenses used ten different numbers
                  │                                        │
                  ▼                                        ▼
        every tier adjudication                  every count in every report
                  │                                        │
                  └──────────────┬─────────────────────────┘
                                 ▼
                    WAVE 1 · repair the instruments
                                 ▼
                    WAVE 2 · 53 auto-safe repairs
                                 ▼
                    WAVE 3 · 3 archives
                                 ▼
                    WAVE 4 · the emission pilot  ← the migration rehearsal
                                 ▼
                    WAVE 5 · the migration, behind the citation gate
```

**`R-08` is the keystone.** The census states it plainly: *"This ruling is
upstream of every other tier adjudication and no agent can make it."* One live
definition says `[S]` means *"follows necessarily"*; the other says *"a considered
choice, not a discovery."* Those are opposites. Every `[S]` in the corpus — including
the Rosetta's *"the count is `[S]`, selected"* — is ambiguous until you rule.

**`R-22`**: adopt **1,385**, the builder's own walk rules. It is the only figure
derived from an instrument rather than from a hand-rolled `find`. Recording it
kills the class of error that produced three false premises in one day.

---

## 2 · WAVE 0 — the two rulings · **owner-class: CHAIR**

| id | question | recommendation on file |
|---|---|---|
| `R-08` | What does `[S]` mean — *follows necessarily*, or *a considered choice*? | rule first, then re-run the tier findings |
| `R-22` | Which live-`.md` denominator governs? | adopt **1,385** (builder walk rules) |

**RULED 2026-08-13 (in-session, CHAIR):** `R-08` → `[S]` means **selected** —
a considered choice, not a discovery; re-run the tier findings under it.
`R-22` → adopt **1,385**, quoted always with its exclusion rule.
Receipt: [`WAVE_0_RULINGS_RECEIPT_2026_08_13.md`](WAVE_0_RULINGS_RECEIPT_2026_08_13.md).

**Nothing downstream should be reported as a number until `R-22` lands.**

---

## 3 · WAVE 1 — repair the instruments · **owner-class: AGENT**

An instrument that reports a property it does not test is worse than no
instrument: it converts an unchecked corpus into a green dashboard. All five
were found by mutation probe, and each repair must ship with a **planted negative**
that proves the repaired checker can go red.

| id | instrument | defect | repair |
|---|---|---|---|
| `W1-01` | `build_corpus_index.py:50` | drops 55 documents' declared `d_register`, then reports the hole as *"the gap this index exposes"* | stop dropping it; re-run; the 3.0% population figure is an artifact of this bug |
| `W1-02` | `check_emergentism_purity.py:245` | omits Helios / Aureus / Menexus / SPECTRE / APU.BOT — the exact five the contamination inventory declared in scope. Its `KSC-11` test is **case-sensitive**, so it misses the one real violation while flagging the sentence that teaches the rule | add the five; make the `KSC-11` test case-insensitive; exempt the teaching sentence by anchor, not by case |
| `W1-03` | `check_generative_base.py` | all three declared bounds unasserted — `WORD_LEN` 10→4 still prints PASS | assert `WORD_LEN`, `GRID`, `CW_DEPTH`. A half-landed repair is already on file at `MUTATION_TEST_RECEIPT_2026_08_06.md:112` |
| `W1-04` | `check_established.py` | literal-substring allowlist; its own header admits it *"drifted the day it was written"* | `R-19`: ship the staged semantic classifier, **or** rule the allowlist adequate and stop calling it verification |
| `W1-05` | `test_contact_limited.py` | runs **0 tests** while printing `FAILED (errors=1)` | read the drift before re-syncing the byte-count registry |
| `W1-06` | *(absent)* | **no orphan/reachability gate exists.** 432 of 1,387 live docs have zero inbound edge | build one. Hard-code the two exclusions the census proved necessary |
| `W1-07` | `check_links.py` | inline links only. **771 broken references live in frontmatter channels no gate has ever checked** | superseded in part: `check_all_citations.py` now covers every channel. `R-25`: fold it into `gate.sh` report-only first, with its own ratchet |

**`gate.sh` is globally red** — 8 of 20 wired checkers exit 1 — so it cannot
separate new breakage from the standing backlog. `R-16` asks you to rule, per
checker, *real defect or drifted ratchet baseline*. **Until that lands, `gate.sh`
green means nothing and must not be cited as verification.**

---

## 4 · WAVES 2–3 — the safe repairs and the three archives · **owner-class: AGENT**

**Wave 2 — 53 auto-safe items**, all non-destructive and reversible:
12 frontmatter · 8 `canonical_phrase` · 6 index · 4 link · 4 status · 3 register ·
3 README · 2 citation · 11 other. Enumerated in `CENSUS_DOCKET_2026_08_13.json`.

Two constraints on this wave:

- **Harvest, never infer.** `canonical_phrase` is null on 544 of 1,381 rows —
  including `00_THE_KERNEL_INDEX.md`, the front door. Fill only what a document
  declares. `null` beats a plausible value.
- **`VMOSK_A.md`** (`R-15`): its supersession is signed and countersigned, yet
  line 15 still says `ACTIVE CONTROL PROJECTION`, so an agent grepping `^status:`
  gets the wrong answer. **Fix the status line here; do not archive the file** —
  archiving is blocked on propagation, not on the decision.

**Wave 3 — exactly three archives.** Each names a successor and quotes the evidence:

| from | superseded by |
|---|---|
| `B3_TODO.md` | `00_HANDOFF/pmo/B3_WAVE_RECEIPT_2026_08_06.md` |
| `00_WORK_IN_PROGRESS/00_THE_PROGRAM_PLAN.md` | `00_META/00_CONTACT_LIMITED_COMPLETION_ROADMAP_2026_08_01.md` |
| `12_PUBLIC_SITE/_PLANS/2026_07_28_VMOSK_A_FINITY_PUBLIC_RELEASE.md` | `…/2026_07_28_VMOSK_A_WORLDVIEW_FRONT_DOOR.md` |

**The other ~27 candidates are not in this bucket on purpose.** They name no
successor, or their own banner orders them to stay — *"retained in place for
provenance and link stability."* The 31 self-declared-dead documents are
**already correctly disposed** (`R-01`: rule STAY).

Use `git mv`, never `cp`+`rm`, so history follows. **Skip any file dirty in the
working tree and name it** — 90+ files are dirty from concurrent sessions at any
time, and no authorization makes it safe to move a file another session is editing.

---

## 5 · WAVES 4–5 — the pilot, then the migration

### `W4` · Fix `16_THE_EMISSION` first · **owner-class: AGENT → now CHAIR**

> **EXECUTED 2026-08-13, and it stopped on a ruling.** `56 → 21 → 10` anchor
> failures across two passes (`050cc466`, `52dc0858`), while the gate's coverage
> ROSE — anchors verified in prose `180 → 188`. `check_anchors.py` was never
> modified; verified by `git diff --quiet`, not asserted.
>
> **The remaining 10 are one question, not ten.** Relaxing `pair()`'s adjacency
> rule clears **9 of the 10** immediately. That was refused deliberately: buying
> green by loosening the gate is the failure this whole lane exists to prevent.
> **`R-32` (new): is `pair()`'s adjacency rule correct?** Rule it and Wave 4
> closes; until then Wave 5 stays shut, because a migration rehearsal that only
> passes with its checker loosened has rehearsed nothing.
>
> **RULED 2026-08-13 (in-session, CHAIR): the rule stands — fix the
> documents.** The ten failures are content defects: five quotes to correct
> against their targets, four bare paths to anchor or mark `{no-anchor}`, one
> ambiguous basename to disambiguate. `pair()` is not to be touched.
> Receipt: [`R32_RULING_RECEIPT_2026_08_13.md`](R32_RULING_RECEIPT_2026_08_13.md).
>
> Also fixed here, and it is the **fourth** instance of one defect class today:
> `A_THE_LADDER/05_D4_ACTUAL.md` was stale *and committed at HEAD* — a generated
> artifact its own generator would not reproduce. `emit.py --verify` now reports
> byte-identical across all 10 outputs. **Add that check to `gate.sh` when `R-16`
> lands; nothing currently watches for generator drift.**

`16_THE_EMISSION/A_THE_LADDER/` **is** the target spine — `00_GROUND · 01_THE_UNIT ·
02_D1_ARITHMETIC · 03_D2_CONFIGURATION · 04_D3_STATE · 05_D4_ACTUAL ·
06_D5_POSSIBLE · 07_HORIZON`. `check_anchors.py` exits **1** with **56 anchor
failures**, 8 `path:line` violations and 3 double-stationed entries.

**This is the migration at 1/200th scale and it is already failing.** Do not move
1,727 files while the eight-file rehearsal is red. Fixing it is the cheapest
possible information about what the migration will cost.

### `W5` · The migration · **owner-class: CHAIR to authorise, AGENT to execute**

The gate exists and is mutation-verified:

```bash
python3 09_TOOLS/01_SCRIPTS/check_all_citations.py \
    --baseline 00_META/registers/CITATION_BASELINE.json
```

Baseline **2,043**. Protocol, in order, and no step may be skipped:

1. `git mv` every path — history follows.
2. Rewrite **every** relative link **and** every frontmatter `parents` / `sources` /
   `depends_on` / `supersedes` entry. The frontmatter channel is where a move does
   its damage and it holds 771 of the broken references today.
3. Re-run the gate. **Post-move must be ≤ 2,043.** Above it, revert the whole move.
4. Re-run `check_anchors.py`, `gate.sh`, and the public-site gates.
5. Only then update the registers.

**Hard bound:** `2,043` is an *upper* bound — some frontmatter keys carry prose,
not paths. That does not weaken the gate, which is a **delta**: stable false
positives cancel on both sides. Do not "fix" the false positives mid-migration;
that moves the baseline under your own feet.

---

## 6 · Hard stops — for any agent, in any wave

1. **Never `git add -A` or `git add .`.** Explicit pathspec, then
   `git diff --cached --name-only` before every commit, then `git show --stat HEAD`.
2. **`grep` is a shell function wrapping `ugrep --ignore-files` and honours
   `.gitignore`.** A null result never proves absence. Use `/usr/bin/grep` for any
   "this does not exist" claim and say which instrument you used.
3. **Verify the premise before you brief anything.** Three of four swarm premises
   were refuted on 2026-08-13, all from counting with a raw `find` instead of the
   artifact's own scope rules.
4. **Archive-first, never delete.** `git mv` into `90_ARCHIVE`, never `rm`.
5. **Commit only when asked.** Other sessions work in this tree concurrently.
6. **A gate that cannot fail is not evidence.** Every repaired checker ships with a
   planted negative that proves it goes red.
7. **Owner-only acts:** ratify canon, promote a tier, sign or close a receipt,
   deploy, declare a DAV, re-fingerprint a claim card, bulk-move outside the three
   named archives.

---

## 7 · The 31 rulings

All 31 are in `CENSUS_DOCKET_2026_08_13.json` with a recommendation on each.
Grouped by what they unblock:

| group | ids | unblocks |
|---|---|---|
| **upstream** | `R-08` `R-22` | every tier adjudication; every quotable count |
| **instruments** | `R-16`…`R-21` `R-25` `R-30` | Wave 1, and `gate.sh` meaning anything |
| **disposition policy** | `R-01`…`R-03` `R-12`…`R-15` `R-26`…`R-29` | Wave 3 and the Titan Pass |
| **doctrine** | `R-05`…`R-09` `R-31` | `P = Φ × V` in two K2-signed documents; `KSC-13` fences; POA-as-authority |
| **published surface** | `R-10` `R-11` | the public site; the 23 stale `KSC-11` spellings no instrument can see |
| **docketed elsewhere** | `R-04` `R-23` `R-24` | `D-OWNER-01`, unset for 11 days |

**`R-06` is the one to read first after the two upstream rulings.** `P = Φ × V` is
asserted as live `[S]` doctrine in **two K2-signed epistemology documents**, against
`KSC-02`. The recommendation is to narrow both to the surviving AND-class form
`P_node = min(Φ̂₄, V₄)`.

---

## 8 · Kills

| claim | what refutes it |
|---|---|
| this plan's counts | re-run the command beside each; any diff is a defect here |
| the ordering | show a wave whose output does not depend on the wave before it |
| `R-08` is upstream | exhibit a tier adjudication that is unambiguous under **both** live definitions of `[S]` |
| the three archives | show a successor named here that does not supersede its source |
| **this plan** | if it is ever cited as authority to execute an item whose owner-class is CHAIR |

**Canonical path:**
`01_EMERGENTISM/00_HANDOFF/THE_EXECUTION_PLAN_2026_08_13.md`

•   ⊙   ○
