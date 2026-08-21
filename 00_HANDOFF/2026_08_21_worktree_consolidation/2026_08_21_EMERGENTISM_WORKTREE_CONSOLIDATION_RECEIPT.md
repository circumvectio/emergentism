---
type: execution-receipt
title: "Emergentism worktree consolidation — local receipt"
date: 2026-08-21
status: "[B] LOCAL EXECUTION RECEIPT — unsigned"
owner_direction: "Yves R. Burri: churn down the worktrees and commit the reviewed work"
may_sign: false
may_authorize: false
authority_effect: none
push: false
deployment: false
publication: false
remote_custody: false
---

# Emergentism worktree consolidation — 2026-08-21

## 1. Outcome

`[B]` The local Emergentism estate was reduced from five worktrees and nine
local branches to one worktree and two local branches. Reviewed content was
committed in source-shaped groups before integration. Three broad alternatives
were not merged; their exact tips remain under annotated non-adoption tags.

This receipt records local repository work only. It does not ratify an inner
claim, promote an evidence tier, change `main`, push a ref, deploy a site,
publish a benchmark, or establish independent custody.

## 2. Preserved and integrated work

The dirty refinement worktree was committed in six explicit groups:

| commit | local purpose |
|---|---|
| `592fe220` | archive adverse and legacy inputs with custody tombstones |
| `a1bba06c` | bind F5 language to native mechanisms |
| `5bf8eac9` | tighten evidence and contributor boundaries |
| `f8b551be` | add the VMOSK tracked-corpus census correction |
| `3f1214b0` | record the corrected full-corpus Rosetta audit |
| `79df68bb` | regenerate refinement-tree registers |

The Spark rewrite was preserved separately at `af4a8273`. Its source merge
kept the intentional fallibilist reader, the newer other-stacks boundary, and
the shared accessibility stylesheet; RAG and service-worker artifacts were
regenerated from the resolved tree.

The active keeper branch received:

| commit | integration |
|---|---|
| `f59a4423` | Great Mystery synthesis |
| `ca5610c6` | reviewed refinement and Dasein benchmark |
| `2a442a0a` | Spark reader rewrite |
| `8807ac71` | consolidated-tree register regeneration |

`[B]` Before this receipt was added, the consolidated tree contained 1,489
live indexed documents, 3,889 registered files, and 859 registered folders.
With this receipt staged, the final register census is 1,490 documents, 3,890
files, and 860 folders.

## 3. Retired worktrees and branch successors

All five worktrees were clean immediately before administrative mutation. The
four auxiliary worktrees were removed without `--force`:

- `.codex-worktrees/emergentism-corpus-refinement-20260820`
- `.codex-worktrees/emergentism-corpus-refinement-20260821`
- `.codex-worktrees/emergentism-great-mystery-20260820`
- `.codex-worktrees/emergentism-spark-reader-20260820`

The four merged branches were deleted with `git branch -d`. The three reviewed
non-adoption branches were deleted with `git branch -D` only after exact
annotated-tag equality was rechecked.

| retired branch | peeled recovery commit | disposition |
|---|---|---|
| `codex/emergentism-corpus-refinement-20260820` | `ae062bf68e67751ba21bfcc777acbfd504746e76` | merged; tag `archive/2026-08-21/corpus-refinement-20260820` |
| `codex/emergentism-corpus-refinement-20260821` | `79df68bb86265df4eeed0c083ed98220ca6d7ff3` | merged; tag `archive/2026-08-21/corpus-refinement-20260821` |
| `dosc/emergentism-great-mystery-2026-08-20` | `8e408ce720a7b0f8d2e0bbccb3bfd5b67ef759db` | merged; tag `archive/2026-08-21/great-mystery` |
| `codex/emergentism-spark-reader-20260820` | `af4a82736cd37ce372eaa4f1414d2e5b6d5c0301` | merged; tag `archive/2026-08-21/spark-reader` |
| `chore/glyph-migration-2026-08-14` | `ec7bc5b46c1d094bbe6b723231e949f17580f7c7` | not merged; tag `archive/2026-08-21/glyph-migration` |
| `codex/emergentism-ontology-seed` | `7ff958d6abe9de6aebedb8fbad0f0436be5eb39a` | not merged; tag `archive/2026-08-21/ontology-seed` |
| `dosc/rosetta-cascade-2026-08-20` | `b7854852dbdc156f34e767ac0fcca54468b58244` | not merged; tag `archive/2026-08-21/rosetta-cascade` |

The pre-consolidation keeper is additionally preserved at
`archive/2026-08-21/theory-pre-consolidation`, peeled commit
`88537fcd3e6806a0a3ef22d711166f5f9b3961d5`.

Retained local branches:

- `main` at `2967fd9059c2ae4f81e552eb9043efefacec7889`
- `theory/parasite-load-2026-08-17`

`main` was not moved or merged.

## 4. Recovery custody

A complete-history bundle was created before worktree or branch retirement:

- path:
  `/Users/Yves/emergentism_rescue_2026_08_21/emergentism_pre_retirement_20260821.bundle`
- size: 32,355,319 bytes
- SHA-256:
  `da259e56a2b20aa14889c66b1cbb952bb79a373edbc570c9c16f3a87ff2ee6cb` <!-- # pragma: allow-secret — content hash, not a credential -->
- contents: the two keeper branches and all eight annotated recovery tags
- result: `git bundle verify` passed and reported a complete history

The bundle and the earlier dirty-byte rescue are on the same disk as the
repository. They improve operator-error recovery but do not protect against
device loss and are not remote custody.

The invalid Git-ref namespace file `.git/refs/.DS_Store` was moved, not
deleted, to:

`/Users/Yves/emergentism_rescue_2026_08_21/git_admin_noise/refs_DS_Store_2026_08_21`

Its exact size is 6,148 bytes and its SHA-256 is
`7301542d4ac61e85f712de7ca1cf03ee69e2eb2fcec578c53ebbf3718a489489`. <!-- # pragma: allow-secret — content hash, not a credential -->
After the move, `git fsck --no-reflogs` exited zero with no errors and 294
dangling-object notices. No garbage collection or object pruning ran.

## 5. Verification at consolidated HEAD `8807ac71`

| check | result |
|---|---|
| `git diff --check` and clean status | PASS |
| file/folder register `--check` | PASS — 3,889 files / 859 folders |
| target JSON and JSONL parsing | PASS |
| managed-agent source/hash checker | PASS |
| EUB v1 unit tests | PASS — 79/79 |
| EUB freeze | PASS |
| EUB recorded-account and fixture validation | PASS |
| Dasein paper release check | PASS — local package only |
| public semantic parity | PASS |
| deterministic site artifacts | PASS |
| RAG / service-worker checks | PASS — 120 passages / 68 assets |
| local Markdown links | PASS — 2,845 resolved / 0 broken |

Two broad gates remain honestly red:

- `predeploy_check.py`: four errors from unconfigured external claim-card
  custody, inherited Skyzai source-hash drift, and ignored
  `12_PUBLIC_SITE/.vercel/output/` counter residue. The tracked deployable HTML
  universe remains 208.
- `check_emergentism_purity.py`: inherited VMOSK, Rosetta, external-mapping,
  and projection-contract drift. The dedicated managed-agent hash checker
  passes; the broader purity contract still needs an owner-led repair.

No EUB-owned regression was found. A local PASS proves neither deployment nor
external validation.

## 6. Recorded execution incidents

`[B]` During the read-only boundary audit, a worker invoked
`build_corpus_index.py --help`. That script has no help-only mode and rewrote
an already-dirty Corpus Index. Execution stopped and the incident was
reported. Independent comparison showed that restoring the rescued older
index would reintroduce known Dasein drift; L4 later regenerated all three
registers deliberately after the source commits and again after integration.

`[B]` The first branch-retirement preflight stopped without mutation because
several full OIDs had been copied incorrectly beyond their verified short
prefixes. The corrected preflight compared each live branch directly to its
annotated tag and retained fixed checks for HEAD, tree, file hash, size, and
rescue-path noncollision.

## 7. Remaining boundary

- The active theory branch was 20 commits ahead of its stored `origin` state
  before this receipt. No network refresh or push was performed in this wave.
- All archive tags and the bundle are local-only.
- The Skyzai fleet register requires a separate owning-repository correction.
- Publication, deployment, DNS, `main` promotion, and off-device archival
  custody remain separate human-authorized acts.
