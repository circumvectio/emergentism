---
title: "Corpus census 2026-08-13 — handoff"
status: "ACTIVE — HANDOFF. Read before starting corpus cleanup or any restructure. Nothing here is signed."
date: 2026-08-13
evidence_tier: "[B] every count re-runnable by the command given; [I] the readings; [D] the docket"
owner: "Dispatch. No item confers authority to execute it."
parents:
  - THE_EXECUTION_PLAN_2026_08_05.md
  - CENSUS_DOCKET_2026_08_13.json
  - CENSUS_FINDINGS_2026_08_13.json
---

# Corpus census — handoff

Ten read-only lenses over the live lane, 2026-08-13. Full data in
`CENSUS_DOCKET_2026_08_13.json` (dispositions) and
`CENSUS_FINDINGS_2026_08_13.json` (192 findings, 10 lens reports).

## 0 · Read this before you brief anything

**Three of the four premises the swarm was briefed with were false.** They were
produced by counting with a raw `find` instead of the builder's own walk rules.

| briefed | actual |
|---|---|
| ~346 documents unindexed | **4** — index is 1,381 rows against 1,385 in-scope |
| four-vs-six Organs contradiction | refuted |
| `ROSETTA_REPLICATOR` Helios leak | refuted as a leak |

**Count with the instrument's own scope rules before you call something a gap.**

## 1 · The headline

**The content is in better shape than the instruments.**

- Of 1,726 live `.md`, exactly **one** byte-identical duplicate pair — already docketed.
- 0 case collisions · 0 malformed dates · 48 of 57 flagged ordinal collisions are
  the declared-intentional families.
- **The archive bucket collapsed from ~30 to 3.** Most proposed archives name no
  successor, or their own banner says *"retained in place for provenance and link
  stability."* The 31 self-declared-dead documents are **already correctly disposed.**

## 2 · Instruments that publish a property they do not test

| instrument | defect |
|---|---|
| `build_corpus_index.py:50` | drops 55 documents' declared `d_register`, then reports the hole as *"the gap this index exposes"* |
| `check_emergentism_purity.py:245` | omits Helios/Aureus/Menexus/SPECTRE/APU.BOT — the five terms the contamination inventory declared in scope; its `KSC-11` test is case-sensitive, so it **misses the one real violation while flagging the sentence that teaches the rule** |
| `check_generative_base.py` | all three declared bounds unasserted (`WORD_LEN` 10→4 still prints PASS) |
| `check_established.py` | literal-substring allowlist; passes any unlisted paraphrase |
| `test_contact_limited.py` | runs 0 tests while printing `FAILED (errors=1)` |
| — | **no orphan/reachability gate exists at all** |

`gate.sh` is globally red — 8 of 20 wired checkers exit 1 — so it cannot separate
new breakage from the standing backlog.

## 3 · Reachability

**432 of 1,387 live documents (31%) have zero inbound edge.** 24 have zero
reference anywhere.

**Two whole top-level lanes are 100% orphaned** — `16_THE_EMISSION` (11/11) and
`15_THE_TITAN_PASS` (5/5) — because `README.md:153` jumps from `13_BOOKS` straight
to `90_ARCHIVE`. Both lanes were created 2026-08-06..13 and never linked. **This is
a two-line fix and it is the cheapest finding in the census.**

## 4 · The restructure gate — built, armed, not yet used

A folder restructure rewrites frontmatter paths, and **no gate had ever checked
that channel.** `09_TOOLS/01_SCRIPTS/check_all_citations.py` now does:

```bash
python3 09_TOOLS/01_SCRIPTS/check_all_citations.py \
    --baseline 00_META/registers/CITATION_BASELINE.json
```

```
citations across all channels : 7,762
resolve                       : 5,719
broken                        : 2,043   <- 771 in channels no gate ever checked
resolve to a stub             :   102   <- alive, semantically dead
```

Baseline recorded at **2,043**. After any move the count must be **at or below**
that or the move reverts. Mutation-verified: one planted bad frontmatter parent
moves it to 2,044 and exit 1.

`2,043` is an **upper bound** — some frontmatter keys carry prose, not paths
(`00_THE_WELTANSCHAUUNG.md` has `supersedes: nothing — supplements …`). The 1,272
inline figure is the trustworthy one. The gate is unaffected: it is a delta, and
stable false positives cancel on both sides of a move.

## 5 · Order of work

1. **Link the two orphaned lanes** into `README.md` — two lines.
2. **Fix `16_THE_EMISSION`'s 56 anchor failures.** It is the converged spine at
   1/200th scale and it fails its own checker. It is the migration rehearsal and it
   is already telling us where the migration breaks. Do not move 1,727 files while
   the 8-file pilot is red.
3. **Repair the five instruments in §2** before trusting any sweep they green-light.
4. **53 auto-safe** items — non-destructive, reversible (fill harvested index
   fields, repair dead citations, add missing frontmatter).
5. **3 archives** — each names a successor and quotes the evidence.
6. **31 rulings** — owner only. These are the only items that need the chair.
7. **Migration**, behind the §4 gate, last.

## 6 · Standing hazards this session confirmed

- **`grep` is a shell function wrapping `ugrep --ignore-files`** — it honours
  `.gitignore`, so a null result never proves absence. Use `/usr/bin/grep`. The
  gitignored `.vercel` build ships 23 stale `KSC-11` spellings that both `git grep`
  and the shell function report as zero.
- **90+ files are dirty from concurrent sessions at any time.** Never assume the
  working tree equals HEAD; never move a file another session is editing.
- **Two incompatible live definitions of `[S]`** — *"follows necessarily"* versus
  *"a considered choice, not a discovery"* — make every `[S]` adjudication
  ambiguous. This is unresolved and it touches the Rosetta count claim.

**Canonical path:** `01_EMERGENTISM/00_HANDOFF/CENSUS_HANDOFF_2026_08_13.md`
