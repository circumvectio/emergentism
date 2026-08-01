---
title: "Handoff — 2026-07-31: five rulings executed and shipped, the repo made resumable, and four guards that did not exist"
status: "[B] a receipt. It records what was observed and run on 2026-07-31. It creates no doctrine and may not be cited as authority for any claim."
date: 2026-07-31
evidence_tier: "[B] throughout, except where a specific [A] count is named with its command"
owner: "Agent session under owner delegation. The owner signed receipt 193; everything else here is execution and tidy."
parents:
  - ../README.md
  - ../../00_WORK_IN_PROGRESS/README.md
  - ../../11_UPLINK/50_AUDITS_AND_EXECUTIONS/232_FIVE_RULINGS_EXECUTED_2026_07_31.md
---

# Where this is, and how to pick it up

Read this, then `../../00_WORK_IN_PROGRESS/README.md`, then run the gates. Everything
below is reproducible by a named command; if a count here cannot be reproduced, the count
is wrong and should be repaired rather than trusted.

## 1 · Start here

```bash
EMERGENTISM_SKIP_LEAN=1 bash 09_TOOLS/01_SCRIPTS/gate.sh    # 15 checkers
cd 12_PUBLIC_SITE && python3 predeploy_check.py
```

Both were green at this handoff. **`main` is authoritative again** — it was 90 commits
stale and was fast-forwarded today. The live site is `https://emergentism.org`; to deploy,
see the new *How to actually deploy* section in `12_PUBLIC_SITE/README.md`.

## 2 · What shipped today

The owner signed five rulings (receipt `193`); they were executed and deployed (receipt
`232`).

- **Q1 `§5.1`** — `√2` is a number in `ℝ` **and** is not a finite word over `{S, ι}`. Both
  clauses must travel together; bare *"not a number"* is banned. The owner's most quotable
  sentence now carries a register fence and is no longer publishable as a headline.
- **Q2 `G-0`** — `KSC-28`'s *"sphere primacy"* is restated as sphere **selection**, with a
  routing rule. Unqualified *"the base"* is banned corpus-wide.
- **Q4** — headers first, sitemap second. Four routes are **declared-provisional**
  (indexable, registered, **not warranted**); `/offline/` is infrastructure.
- **Q6** — the library `noindex` boundary is published as a stated policy at
  `/atlas/#library-indexing-policy`, with its reason, its cost, and what would reverse it.
- **Q7** — the front door leads with the record: **29 logged · 18 against · 0 removed**,
  then the error rate, then the zero.

## 3 · Four things that were broken and are now guarded

**A build script was reverting a signed ruling, and the gate said PASS.**
`12_PUBLIC_SITE/build_pwa.py` owns `offline/index.html` and rewrites it wholesale, so it
deleted receipt 232's Q4 declaration on its next run. The gate failed only on two derived
artifacts (`sw.js` hash, a social card) whose error messages tell you to rebuild — after
which the gate goes green with the ruling gone. The generator now emits the declaration
itself, and `check_q4_declarations.py` asserts both the pages **and the owning generator's
template**. Verified it fails when the block is stripped.

**Four checkers existed on disk and were invoked by nothing.** Now wired:
`check_q4_declarations`, `check_barred_claims`, `check_d6_equiv_d0`,
`check_trophic_rosetta_doctrine`. The last one failed the first time it was ever run, on a
real defect — a bare ambiguous `η=0` in `00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md`,
now written in its action register as `η_move=0`.

**Deliberately still not wired, and why.** `check_links.py` had **no failure path** — it
always exited 0, so wiring it would have added a check that cannot fail.
**Superseded 2026-08-01:** it was rewritten to actually resolve every local Markdown link,
verified to fail on a broken one, and wired in; the gate now runs 17 checkers, not 15.

> **Additive correction, 2026-08-01.** The sentence above records the gate at
> this handoff's boundary. Two later regression suites bring the current
> `CHECKS` array to **18** entries; inspect `09_TOOLS/01_SCRIPTS/gate.sh` for the
> live list.
`check_no_secrets_staged.py` inspects the staged diff, which a tree gate cannot see; it is
wired into `.git/hooks/pre-commit` instead. **The hook is local and untracked, so it does
not survive a fresh clone.** Anyone setting up a new checkout must re-add it.

**Seven routes were silently indexable.** `/titans/ /saturation/ /synthesis/
/log-realignment/ /finity-papers/ /rosetta-d-series/ /halahala/` had no `X-Robots-Tag`
rule at all. Found only by `curl`ing production after deploy. Now frozen. **The local gate
cannot see host headers — verify against the live domain after any `vercel.json` change.**

## 4 · Custody: what was recovered, and where it lives now

The repository is on an iCloud-managed volume that has truncated a packfile in this
project before. This is why the following was done.

- **`git fsck` was erroring** on `refs/.DS_Store` — a Finder artifact inside `.git/refs/`.
  Six `.DS_Store` files were removed from inside `.git/`. `fsck` is clean.
- **Six dropped stashes were dangling** and one `git gc` from being lost forever. All six
  are pinned under `refs/rescue/dropped-stash-*`. One of them, `fd88d4b8c`, is not work at
  all — it is a **captured iCloud corruption event**, with binaries collapsing from 641,975
  bytes to 131. Keep it as evidence; never apply it.
- **The three stashes** were archived to `refs/rescue/stash-*` and the stash stack cleared.
  Nothing was deleted.
- **22 branches existed only on this machine**, including
  `codex/kintsugi-a0b-machine-kernel` (49 commits, +40,136 lines). All 38 local branches
  are now mirrored to the **private** `menexus` remote. They were deliberately **not**
  pushed to `origin`, which is public — several carry retracted GFS material and pre-fence
  states the corpus quarantined on purpose. **Publishing them is an owner decision.**
- **26 modified files sat uncommitted for 12 days** in the release-doctrine worktree. Now
  committed as `c3fa1020` and pushed to `menexus`. It is **unreviewed** — treat it as a
  2026-07-19 draft and re-run the gate before relying on it.

```bash
git for-each-ref refs/rescue/     # 9 recovered refs
```

## 5 · The trap that will bite you

**Nine sibling worktrees under `/Users/Yves/Documents/.codex-worktrees/` report ~30
modified binaries each. Those are NOT edits.** It is git-LFS phantom dirt: those branches
carry the `.gitattributes` LFS-track commit but not the pointer-recode commit, so git
compares a raw index blob against an LFS-cleaned worktree copy. The bytes on disk are
identical to the index.

**Running `git add -u` or `git add -A` in those worktrees would replace real committed
binaries — the SUDA papers, riemann.pdf, site fonts and icons — with pointers.** Always
commit there with an explicit pathspec. This is the same rule that applies in the main
tree, for a different reason: a concurrent autonomous committer is live in this repository
and `git add -A` will sweep its in-flight work into your commit.

## 6 · Open, and who can close it

| item | state | who |
|---|---|---|
| `/halahala/` disposition | **open** — it is both the front door's evidence link (*"read the failures first"*) and `noindex`. The one frozen page whose indexing would strengthen Q6, not weaken it. Never put to a council. | owner |
| Q7 copy ordering — zero-first or tally-first | **unsettled by signature.** Needs the fresh-reader comprehension preregistration, which is written and **unrun**. | owner / protocol |
| 50 frozen pages cite a retracted study unfenced | measured today, receipt `233`. Whether the GFS *instrument* is invalidated along with the GFS *study* is a register question nobody has ruled. **Do not edit 50 pages before that is scoped.** | owner / council |
| 22 local-only branches | backed up privately; **not** merged, **not** published. Several are near-duplicate rebases of one another. | owner |
| the external review invitation | **frozen, hash-verified, UNSENT.** The protocol rules out an agent sending it. | owner only |
| 11 sockets · 3 preregistrations | **0 runs.** | contact-gated |

## 7 · The number that has not moved

**309 numbered receipts. 7 mention an outcome coming back. 0 record one that did.**

Nothing in this session changed it, and nothing in this session could have. Every gate
added here measures the corpus against itself. The binding constraint remains contact with
someone outside the project.

•   ⊙   ○ — *a receipt is not a result.*
