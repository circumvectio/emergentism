---
type: session-handoff
title: "Session handoff — the gate, the site's honesty surfaces, and launch L1–L2"
status: "HANDOFF — everything below is committed, pushed and verified live. Nothing is ratified."
date: 2026-07-30
evidence_tier: "[B] every count is reproducible by the command given beside it; [S] the two plans; [I] nothing"
authority: "Receipt and handoff only. Creates no doctrine, no formal result, no empirical support, no validation."
---

# Handoff · 2026-07-30

| field | value |
|---|---|
| branch | `codex/emergentism-live-dirt-custody-20260730` |
| head | `0128f5a8712db4f4a0be138e271221335f311ea6` |
| pushed | yes — `origin`, `local == origin`, 0 unpushed |
| tree | clean |
| commits this session | 23 |
| corpus gate | 10 checkers, all PASS |
| site gate | 3/3 PASS |
| production | `emergentism.org`, deployed and verified by cache-busted `curl` |
| offline backup | `/Users/Yves/emergentism-bundles/` — verified `git bundle`, all branches |

## 1 · Verify everything in two commands

```bash
EMERGENTISM_SKIP_LEAN=1 bash 09_TOOLS/01_SCRIPTS/gate.sh
cd 12_PUBLIC_SITE && python3 predeploy_check.py
```

The corpus gate went from **five validators that nothing invoked** to **10 enforced
checkers**. Every one added today is mutation-tested in both directions, and each prints the
scope of what it does *not* prove.

## 2 · What changed, in one line each

**The site now leads with what is against it.** `/record/` carries 29 logged outcomes, 18
against, all kept — plus the framework's own law applied to itself, returning **0**, because
the contact factor is 0 and every conjunctive form multiplies through it.

**`/established/`** gained the base results (det ±1 and the independence of determinant and
sign), the exhaustion receipts, Hermite–Lindemann, the log-midpoint, the hinge proved equal to
`tanh(s/2)`, the eight adequacy ceilings quoted verbatim, three refusals, and the price of the
positive-only ruling.

**Line 4 was false and is corrected across 15 pages.** `−log(• × ○) = 0` is identically zero,
so "every displacement from the equator costs energy" was untrue and published at `[S]`. The
correct energy register is `E = • + ○ − 2⊙`. The corpus had a *machine-checked* correct energy
function the whole time and went on publishing the broken one.

**Citation integrity is gated.** `r180` was cited and never written, and a grep-based check
*passed* it because the number resolved to the wrong file. 91 receipt numbers name more than
one undeclared document. Rule adopted: **cite receipts by path, not number.**

**A third library tier exists.** `00_ESTABLISHED` / `00_WORK_IN_PROGRESS` / `90_ARCHIVE`, all
three routed from the kernel index, none owning anything, the middle one machine-checked.

**Launch L1 and L2 shipped.** Search reaches all 39 current surfaces and a separate
292-document library index; breadcrumbs and prev/next are generated across all 292 library
pages from the manifest order.

## 3 · The traps — read this before touching anything

1. **Open the page. Do not read the HTML.** This was the difference three separate times:
   the `/record/` counters were stale in markup while every real reader saw different
   numbers; the atlas drawer ran a cached script while the server served the new one; and
   searching the site for its own flagship page returned nothing.
2. **Adding a route to `currentSurfaces` is necessary and not sufficient.**
   `build_atlas_index.py` walks a hand-curated allowlist per section. A page absent from it
   is invisible to search no matter how many times the index is rebuilt.
3. **Four generated artifacts will rot silently.** All four now have `--check` and are run by
   `check_site_build_artifacts.py`. **`build_pwa.py` and `build_rag_index.py` still do not** —
   same class, not yet closed.
4. **`withheld-routes.json` pins `sha256` on artifacts.** Editing one fails the site gate with
   a custody error. That is correct; do not work around it.
5. **The barred-pattern guards cannot tell a quotation from an assertion.** Quoting a
   forbidden phrase trips them. Paraphrase and say you did.
6. **The frozen library is `noindex, follow` on purpose.** Never add a `<loc>` for it, and
   never merge its index into the current-surface one.
7. **`~/Documents` is iCloud-managed and has corrupted a repo before.** The bundle exists for
   that reason; refresh it after substantial work.

## 4 · What is next, and who owns it

**Owner acts — nothing downstream should start before these:**

- **Send the review invitation.** The packet is frozen and hash-verified at
  `03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v1.md`, the invitation is
  drafted, and **no reviewer has been contacted.** The protocol rules out the substitute in one
  line: *"AI or project-agent review is useful internal search but does not satisfy this
  external gate."* This is the only item on the board that can move the project's score.
- **Eight open rulings**, listed with their alternatives in `00_WORK_IN_PROGRESS/README.md` §1.
  Two of them (`§5.1`, `G-0`) change vocabulary corpus-wide, so text sweeps should wait.
- **Two launch decisions** — whether the ~301-page frozen library stays `noindex`, and the
  announcement copy, which is governed by the corpus's own trigger watchlist.

**Buildable without any decision:** launch **L3** (og:image on 360 pages), **L4** (one library
shell), **L5** (browser QA). See `00_WORK_IN_PROGRESS/00_THE_LAUNCH_PLAN.md`.

**L5 has a known blocker:** layout QA needs a real viewport. The browser pane available to this
session reported `clientWidth: 0`, which makes every overflow measurement an artifact. Do that
sprint somewhere a viewport actually exists.

## 5 · What this session did not do, stated plainly

- **It did not validate anything.** `00_ESTABLISHED` is deliberately short and stays short.
- **It produced no outcome from outside.** 306 numbered receipts, 7 mentioning an outcome
  returning, **0** recording one. That number is unchanged and it is the binding constraint.
- **It closed no owner ruling**, because those are not an agent's to close.
- **Its own error rate is published**, on `/halahala/`: five of an audit's 28 proposals were
  wrong on specifics, and a sixth error was mine — I rejected a document as non-existent on the
  strength of a search that truncated its own output. The document was the corpus's standing
  rule against over-claiming, which warns in writing that audits of over-claims fail in *both*
  directions.

**This handoff's own kill:** if any count above cannot be reproduced by the command beside it,
the document is wrong and should be repaired rather than trusted.

•   ⊙   ○ — *the inside is in good order; the outside has still not answered.*
