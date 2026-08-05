---
title: "Release Plan — Emergentism: correction first, then one manual"
status: "PLAN — staged, not authorised"
date: 2026-08-05
scope: "12_PUBLIC_SITE deployment, gate repair sequence, and the single release payload"
authority: "None. This document proposes; it decides nothing. Every OWNER-ONLY act below is unperformed."
supersedes: "Nothing. It collects the four audits of 2026-08-05 into one ordered sequence."
evidence_tier: "[D] draft"
kill: "Any phase that ships before its gate has a receipt recording command, exit code, date and commit sha invalidates this plan and the release should be withdrawn."
---


> ## ⚠ VERIFIED ON DISK BEFORE THIS PLAN WAS FILED — the finding that governs it
>
> The live public site does not merely carry a retired notation as decoration. It
> **publishes the retired algebra as display equations, two of them tier-marked
> `[A]`.** `12_PUBLIC_SITE/titans.html`:
>
> ```
> ⊙ = • × ○
>   descent 1 · 0 = 1 / ∞  — computable                              [A]
>   descent 2 · ∞ = 1 / 0  — computable as a limit, never a value    [A]
>   ascent   · 1 = 0 × ∞   — the indeterminate. The emblem.          [I]
> ```
>
> `41_THE_GLYPH_TRANSFORMATIONS.md` §2 states, verbatim: *"neither `0=1/∞` nor
> `∞=1/0` may be cited as a bare field identity or obtained by rearranging the
> emblem."* The site does exactly that, and marks it `[A]` — the corpus's highest
> tier — on **346 pages**, inside `<div class="phi">` display blocks.
>
> `⊙ = • × ○` was retired 2026-08-01 as ill-typed and shown **false in content**
> on 2026-08-05 (the stabiliser of `{0,∞}` in `PGL₂(ℂ)` acts transitively on `ℂ*`,
> so fixing both boundary points fixes no third point).
>
> **This is the strongest possible vindication of "correction before claims," and
> it is the reason Phase 0 is a paper repair and the first deploy carries no new
> claim.** A release issued from this surface would be refuted by the publisher's
> own canon, in one click, by anyone.


# Release Plan — correction first, then one manual

## 0 · How to read this

This plan has one governing constraint, taken verbatim from the release brief and
treated here as binding:

> The corpus's credibility rests on "we went looking and found Euclid."
> Nothing ships from a site that is mid-error. Public correctness precedes public claims.

That constraint decides the whole ordering. It is why the first act is a paper
repair, why the first deploy carries no new claim, and why the release payload —
which is technically independent of the site — is scheduled **after** the site
correction and not before it. The manual could physically ship tomorrow. It must
not, because a reader who reads it will visit the site, and the site currently
publishes a refuted equation at tier `[A]`.

Three reading rules:

1. **A gate is not passed until a receipt says so.** Every gate row in §7 carries
   its measured state as of 2026-08-05 and nothing else. A row may be promoted to
   PASS only by a receipt in `11_UPLINK/50_AUDITS_AND_EXECUTIONS/` recording the
   exact command, its exit code, the date, and the commit sha it ran against.
   Receipts are cited by **path**, never by number.
2. **OWNER-ONLY means no agent may do it, and no agent may schedule it.** Those
   items appear in §2 and are repeated inline where they block a phase. An agent
   encountering one stops and reports.
3. **Every phase is one commit or one commit pair**, so `git revert` is the revert
   procedure. Deploys revert by promoting the prior Vercel deployment, not by
   re-uploading.

Receipt numbers are **not reserved in advance**. The highest existing receipt is
`11_UPLINK/50_AUDITS_AND_EXECUTIONS/242_G2_PROVED_AND_FOUND_TO_BE_PRIOR_ART_2026_08_05.md`.
Each phase mints the next free number **at the time of the act**.

---

## 1 · The five answers, stated before the plan

**What is deployed first, and why that first.**
Nothing is deployed first. The first act is a paper repair to internal registers
(Phase 0), because the public repair to `/established/` cites a register that
currently contradicts it. When a deploy does happen it is **one whole-tree
propagation of corrections already committed**, carrying no new claim. There is no
smaller unit available: `12_PUBLIC_SITE/vercel.json` sets `buildCommand: null`,
`outputDirectory: "."`, and `vercel --prod` uploads the working directory minus
`.vercelignore`. **"Deploy only /amrita/" is not a thing this pipeline can do.**
The "one route, not a sweep" advice from the payload audit is correct about *edit
scope* and inapplicable to *deploy scope*. Consequence: the entire tree must be
correct before the first deploy, and the first deploy propagates all 310 changed
`.html` files at once.

**Which gates must run before anything is published, and which are merely desirable.**
See §7. Nine must-pass gates; eleven desirable. The must-pass set is not
negotiable-by-effort: `12_PUBLIC_SITE/deploy_vercel.sh` runs `predeploy_check.py`
and `check_site_build_artifacts.py` under `set -euo pipefail`, so a red gate is a
hard stop, and forcing past it converts a fail-closed wrapper into a habit.

**What exactly is the release payload, at what tier, with what prohibition list.**
One document: `02_EPISTEMOLOGY/01_EVIDENCE_TIERS/THE_BOUNDARY_RULES_STANDALONE.md`,
published under its own name as *"Boundary Rules — an operating manual for writing
at the edge of a domain. Version 1, draft."* Tier `[D] DRAFT 1`, unpromoted. Three
edits before it ships (Phase 6). Prohibition list at §8, which becomes a file and a
checker in Phase 0.

**What is the smallest honest release, and what is the fuller one.**
Smallest: the manual, alone, with a one-page provenance note, at a stable URL, and
nothing else published in the same act. Fuller: the corrected site as the reference
surface behind it, plus the prohibition list published as the corpus's own
pre-flight instrument, plus F1 closed with a date by the owner. The distillation,
the trade book, the honesty protocol and the four-status taxonomy are **out of
scope for both** — reasons in §9.

**The sequence from today to publication.**
Phase 0 (½ day) → Phase 1 (2–3 days) → Phase 2 (owner, ~1 day of owner time,
calendar-elastic) → Phase 3 (5–12 working days, the long pole) → Phase 4 (½ day
+ owner authorisation) → Phase 5 (½ day) → Phase 6 (½ day + owner publication).
Honest earliest date for the manual in public: **three to four calendar weeks**,
i.e. late August to early September 2026, assuming owner rulings land inside a
week. It is not an afternoon and it is not next Tuesday.

---

## 2 · OWNER-ONLY register

No agent may perform, simulate, pre-stage as "ready to click", or schedule these.
An agent that reaches one stops and reports.

| # | Act | Blocks | Where it appears |
|---|---|---|---|
| O-1 | **Disposition of canon amendment `a4a3a493`** — the middle emblem mark denotes the realm (`Finity_F`), not the unit point; `emblem_T(1_T)` withdrawn | OS01-01 re-fingerprinting; any site sweep of the mark; §12 of the manual | Phase 2 |
| O-2 | **OS01-01, OS01-13, OS01-26 custody** — three claim cards whose attested text no longer exists; re-stamping is an assertion "I read the new passage and the card still attests" | `compile_claim_cards.py --check`; predeploy §13/§15 | Phase 2 |
| O-3 | **OS01-08 semantic-owner seat** — migration introduces `K-7`, absent from the legacy `owner_ids` `{K-1, K-3}` | same | Phase 2 |
| O-4 | **Register-vs-checker canon ruling ×4** — grave `repair_path`; grave `status_before_reopening`; `investigation_state` on 9 RQ rows; DF-13 terminal status; plus the deleted `owner_reopening` block | `check_claim_status.py`; predeploy §16 | Phase 2 |
| O-5 | **`excluded_routes` boundary ruling** — what "withheld from the reading surface" means, in one sentence | `check_public_semantic_parity.py`; predeploy §12 | Phase 2 |
| O-6 | **Notation ruling on the retired infix emblem form** — leave / sweep to operator-free / sweep-and-regenerate, across ≥352 live `.html` | generator re-runs; §12 fixtures; deploy | Phase 2 |
| O-7 | **Sign or withdraw receipt 187 / KSC-04** (mortal-signer act) | trade-book precondition 3; any citation of KSC-04 | Phase 2, deferred |
| O-8 | **Close F1 with a date** — or record it as open with a date | any contribution claim, in any copy | Phase 2, deferred |
| O-9 | **Vercel dashboard: confirm whether a Git integration is connected** (Project → Settings → Git) | decides whether the wrapper is a gate or a habit; cannot be answered from disk | Phase 1, blocking |
| O-10 | **Push to a public GitHub remote** (`origin` = circumvectio/emergentism, `menexus` = Menexus-GmbH/emergentism) — publication of public content | the "Check it yourself" clone block; the deploy | Phase 4 |
| O-11 | **The deploy itself** — `./deploy_vercel.sh` | everything downstream | Phase 4 |
| O-12 | **DNS cutover** `www.emergentism.org` → Vercel, per `11_UPLINK/50_AUDITS_AND_EXECUTIONS/118_SHIP_RECEIPT_VERCEL_PROD_DNS_CUTOVER_OWED.md` §2 | the canonical URL the manual points at | Phase 5 |
| O-13 | **Publication of the manual** | the release | Phase 6 |
| O-14 | **The `og:description` "twenty machine-checked theorems"** — deliberately-left open item #6 in `14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md` | the snippet that travels into search | Phase 3, blocking |

---

## 3 · Phase 0 — Repair the paper the site cites (AGENT, ½ day)

**Why first.** The staged `/established/` repair attributes G2 to Hardy & Wright and
retires the reader challenge. `00_ESTABLISHED/README.md` — the register that page
sends readers to, one `git clone` away — still offers the same theorem as an open
challenge. Deploying the page before repairing the register publishes a
self-contradiction on the single most checkable claim either makes. This is the
cheapest blocker on the entire list and it gates both the site and the manual.

**What is done**

| Act | File / line | Note |
|---|---|---|
| 0.1 | `00_ESTABLISHED/README.md` §B table (line ~100) and the paragraph at line ~114 | Replace the `G2` row's "open general claim" and kill column, and the sentence "`G2` remains open until a complete proof or formalization lands", with a **dated seam** citing `05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md` and `11_UPLINK/50_AUDITS_AND_EXECUTIONS/242_G2_PROVED_AND_FOUND_TO_BE_PRIOR_ART_2026_08_05.md`. Do **not** delete the old text — tombstone it in place. New kill for the row: *exhibit a published account predating Hardy & Wright that already partitions non-termination into two directions and identifies them with 0 and ∞.* |
| 0.2 | `05_COSMOLOGY/03_FORMAL_SYSTEM/49_FINITY_RECOVERY_AND_COUNTERMODEL_SUITE.md` frontmatter line 3, §-head line ~24, reasoning at line ~39 | Add the `F0 NOT PASSED` disposition pointer to `42_THE_CASE_FOR_FINITY.md:194` and its receipt. Closes the third of three files; 42 and 47 are already correct. |
| 0.3 | `00_HANDOFF/SESSION_AUDIT_2026_08_05.md:221` | Strike **"Count verified exact."** Recompute with a normalising matcher (NFKC + HTML-entity decode + circle-codepoint class `U+25CB`/`U+25EF`/`U+26AA`), publish the corrected figure with a dated seam. Verified false today: `12_PUBLIC_SITE/amrita/index.html:64,129` encode the form as `&#8857; = &bull; &times; &#9711;` and are invisible to the glyph grep that produced 349. |
| 0.4 | Propagate 0.3's corrected figure | `14_THE_DISTILLATION/00_THE_AMRITA.md` §03 item 5; `14_THE_DISTILLATION/05_THE_METHOD.md` §6; `14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md` item 4; `14_THE_DISTILLATION/02_WHAT_IS_CHOSEN.md` §3. Record the corpus-wide `.md` figure (79 live files outside `12_PUBLIC_SITE` and `90_ARCHIVE`) beside the site figure everywhere the site figure appears. |
| 0.5 | Reopen F4 | Annotate `00_META/claim_cards/one_sitting.yaml` review history: commit `3ef16aa8` closed a **file-level hash check**, not a claim-custody check; 25 of 26 per-card locators were defective at the moment of closure; F4 stays open until `compile_claim_cards.py --check` exits 0. |
| 0.6 | Stale-citation sweep | One grep. Any receipt, ledger row or doc dated **after 2026-08-04 02:34** (merge `80759036`) that cites a `check_claim_status.py` or `compile_claim_cards.py` PASS gets an annotation, not a deletion. `11_UPLINK/.../174_*.md:151` and `.../176_*.md:133` are **honest for their 2026-07-29 date** and must not be impeached. |
| 0.7 | Create the prohibition list as a file | `00_META/RELEASE_PROHIBITION_LIST.md` — §8 of this plan, verbatim, with each line carrying its dated receipt path. Then `09_TOOLS/01_SCRIPTS/check_release_copy.py`, which greps any nominated release surface against it and exits non-zero on a hit. **Mutation-test it before wiring**: it must FAIL on `12_PUBLIC_SITE/amrita/index.html` before it is trusted. Wire into `09_TOOLS/01_SCRIPTS/gate.sh` `CHECKS`. |
| 0.8 | Wire the four orphan checkers or delete them | `check_g2_normal_form.py`, `check_dead_citations.py`, `check_forwarding_stubs.py`, `check_tree_contract.py` exist in `09_TOOLS/01_SCRIPTS/` and are invoked by nothing. Wire or delete — do not leave them on disk where their existence reads as coverage (r177 HOLE 0). |
| 0.9 | Make the silent SKIP explicit | `00_META/claim_cards/{reciprocal_infinite_play,sarpasya_vijayam,self_eating_serpent,six_lenses}.yaml` declare `../02_SKYZAI/03_AIA/...` paths that resolve nowhere, so `missing_federated_sources()` silently skips the two whole-corpus tests. Convert to an explicit, receipted exclusion listing the 28 uncovered cards. Re-pointing them at the live `02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/...` paths is a Phase 2 owner confirmation, not this act. |

**Unblocks.** The `/established/` deploy (0.1); trade-book precondition 4 (0.2); an
honest scope figure for any notation decision (0.3–0.4); the F4 ledger (0.5); the
release-copy gate (0.7).

**GATE 0** — all four must be recorded in the phase receipt with exit codes:

```
python3 09_TOOLS/01_SCRIPTS/check_established.py
python3 09_TOOLS/01_SCRIPTS/check_generative_base.py
python3 09_TOOLS/01_SCRIPTS/check_g2_normal_form.py
python3 09_TOOLS/01_SCRIPTS/check_release_copy.py --surface 12_PUBLIC_SITE/amrita/index.html   # MUST exit non-zero
```

Plus: `grep -rn 'G2 remains open' 00_ESTABLISHED/ 12_PUBLIC_SITE/` returns nothing.

**REVERT.** `git revert <phase-0 sha>`. No published surface changes in this phase,
so revert is total.

**RECEIPT.** Next free number, `11_UPLINK/50_AUDITS_AND_EXECUTIONS/`, titled for the
register repair. Must state that no deploy occurred.

**EFFORT.** 4 hours agent. 0 owner.

---

## 4 · Phase 1 — Make the gates honest *before* making them green (AGENT + O-9)

**The rule that orders this phase.** Repairing `check_public_semantic_parity.py`'s
`NameError` alone converts a loud traceback into a green
`PUBLIC SEMANTIC PARITY: PASS` over a site with ~352 violations, because the module
audits **48 of 799** `.html` files. That is the corpus's documented failure mode —
evidence of checking published as the warrant — reproduced inside its own gate.
**Scope first, names second, and never the reverse.**

| Act | Who | Detail |
|---|---|---|
| 1.1 | AGENT | **Scope `check_public_semantic_parity.py` before touching the names.** Make the page scan walk every deployable HTML file — the set `predeploy_check.py` §1/§5 already walks via `get_public_html_files()` — and keep the manifest-binding checks on the 48 declared surfaces. **Proof obligation: run it BEFORE the NameError fix and confirm it reports ~352 emblem hits.** A repair that does not first make the gate loud has not been verified. |
| 1.2 | AGENT | Replace `TITAN_INFIX_REJECT_FIXTURES` (`:124`, three literal-glyph strings) with a **normalising matcher** over the emblem's codepoints: NFKC, HTML-entity decode, and a circle class covering `U+25CB`, `U+25EF`, `U+26AA`. Mutation-test against `12_PUBLIC_SITE/amrita/index.html:64,129` — the guard must fail on that file before it is trusted. |
| 1.3 | AGENT | `import fnmatch`, and **decide explicitly** about `_vercelignore_patterns` (:200) and `_ignored` (:207): either delete both (honest; stops the file looking better-covered than it is) or restore the `1797138a` classification loop that called them at :315/:320 and errored on any file that was neither current, infrastructure, frozen, withheld nor deploy-ignored. Restoring is the higher-value option — it is the only mechanism that would notice a **new** unclassified public file. |
| 1.4 | AGENT | **Triage the 23 unclassified pages** carrying the retired form that are in neither a `frozenLibraryRoots` prefix nor `withheld-routes.json`: `atlas/`, `cosmology/`, `epistemology/`, `methodology/`, `ontology/`, `theology/`, `titans/`, `titans.html`, `sphere.html`, `cascade.html`, `passage.html`, `sources/`, `rosetta-d-series/`, `log-realignment/`, `suda-notes/`, `r/0`–`r/6`. Each is current (fix notation per O-6), frozen (add to a root), or withheld (add with sha256 and a reason). This does **not** wait on any ruling except O-6 for the "current" branch. |
| 1.5 | AGENT | **Gate 3 rename, the correct direction.** In `09_TOOLS/01_SCRIPTS/check_claim_status.py`: `reopened_ids` → `investigation_ids` at :705, :730, :732 (**not** the reverse — initialising `reopened_ids` leaves `investigation_ids` permanently empty and silently kills the successor-resolution check at :771–778). Then map sections `reopened` → `investigations` and `restored` → `typed_survivors` at :179, :380, :386, :741, :794, and add `investigations`, `typed_survivors`, `investigation_authorization` to `KNOWN_SECTIONS`. The mapping is forced by the register's actual keys and by the checker's own leftover error strings. **Output: a 57-error disposition sheet for O-4. Do not conform the checker to the register — HOLE 5 at :100–107 forbids it.** |
| 1.6 | AGENT | **Claim-card mechanical batch, 22 of 25.** Relocate 17 stale fingerprints whose attested bytes are present verbatim at HEAD (drift +84 to +119; OS01-01 drifted +1) and recover 5 stripped cards (OS01-04, -05, -08, -09, -23) from `1797138a`, whose recovered anchors relocate to unique single hits at 198–203, 206–224, 247–268, 271–288, 544–564. **Receipt = byte-equality proof: the OLD fingerprint must hash the slice at the NEW coordinates.** Migrate 4 of the 5 owner sets mechanically (identical sets); **hold OS01-08 for O-3**. Hold OS01-01, -13, -26 for O-2. |
| 1.7 | AGENT | **Harden the compiler so this cannot recur.** `09_TOOLS/02_COMPILERS/compile_claim_cards.py`: refuse a re-stamp when newly hashed bytes differ from previously attested bytes unless the card declares `relocated_from` (pure move) or `re_reviewed` (content changed, with a reviewer). This single schema change converts "the file moved" vs "the claim was re-reviewed" from a convention into a gate — and it is the direct repair for the `3ef16aa8` failure. |
| 1.8 | AGENT | `_inferred_manifest_lifecycle` (called at `compile_claim_cards.py:564`, defined nowhere, **absent from `1797138a` too — must be written**, which requires deciding what lifecycle a manifest work infers) and `source_record` (read at :575/:584 inside a `historical_sources` loop that treats items as strings via `_require_string`; a half-finished list-of-objects → list-of-strings change). **Fix both in the same pass** or `source_record` presents as a fresh regression the moment the lifecycle lands. |
| 1.9 | AGENT | Reconcile `12_PUBLIC_SITE/build_withholding_boundary.py:233`: `frozenLegacySurfaces` → `frozenLibraryRoots` (the key was deleted from under it when `public_semantic_parity.json` went to schemaVersion 2), or restore the key deliberately if the two sets differ. Regenerate `vercel.json`'s redirect + header block: **170 of 201 withheld public routes have no redirect; 156 lack noindex/noarchive/nosnippet; 151 lack no-store.** Re-record the 56 of 67 drifted artifact sha256/bytes. *This is a routing and record failure, not an exposure — Layer A holds: all 67 artifacts are literally in `.vercelignore`, zero withheld routes in `sitemap.xml`.* |
| 1.10 | AGENT | Delete `12_PUBLIC_SITE/.vercel/output/` — a 2026-07-28 `target: preview` snapshot, 91 directories, 338 HTML files carrying the retired form, publishable verbatim by `vercel deploy --prod --prebuilt`, bypassing every generator and every check. Then extend `predeploy_check.py` §11 to assert no `.vercel/output` tree exists. |
| 1.11 | **OWNER (O-9)** | Vercel dashboard → Project `emergentism-org` → Settings → Git: confirm whether a repository is connected. `.vercel/.env.production.local` carries `VERCEL_GIT_PROVIDER`, `VERCEL_GIT_REPO_OWNER`, `VERCEL_GIT_REPO_SLUG`, `VERCEL_GIT_COMMIT_REF`, `VERCEL_GIT_COMMIT_SHA` (key names only — the file was not opened, per `README.md:173`). **If a repo is connected, every push to the production branch auto-deploys with no gate, the whole fail-closed wrapper is decorative, and today's commits may already be live.** Remedy: disconnect, or add an Ignored Build Step that runs the gate. |

**Unblocks.** O-4's disposition sheet (1.5); O-2/O-3 framed as three quoted diffs
and one seat question rather than a 25-card slog (1.6); predeploy §10 (1.9) and §12
(1.1–1.3); and the answer to whether any of this machinery matters (1.11).

**GATE 1**

```
python3 12_PUBLIC_SITE/check_public_semantic_parity.py        # must RUN; expected FAIL, ~352 emblem hits + binding errors
python3 09_TOOLS/01_SCRIPTS/check_claim_status.py             # must RUN; expected FAIL with 57 enumerated errors
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check  # must reach OS01-01/-13/-26 and stop there, not at OS01-01 alone
python3 -m pytest 09_TOOLS/.../test_corpus_claim_graph.py -q  # expected: failures drop from 38 toward ~26; record the exact number
```

Gate 1 passes when **every one of the three dead gates executes to completion and
reports real errors**. It does *not* require any of them to be green. A green
result at this stage would be the defect.

Plus the hard stop: **O-9 answered.** If a Git integration exists and is not
disabled, this plan is suspended until it is.

**REVERT.** Each act is its own commit; `git revert` per act. 1.10 deletes a
build artifact — regenerable by `vercel build`, and its deletion is the point.

**RECEIPT.** One receipt for the lineage, naming merge `80759036`
(2026-08-04 02:34:02 +0700, "conflicts resolved main-side: newer canon stands") as
the single origin of every defect repaired in this phase. That is cheaper and truer
than five unrelated bug reports: **no gate rotted; one merge cut them.**

**EFFORT.** 2–3 working days agent. ~15 minutes owner (O-9), on the critical path.

---

## 5 · Phase 2 — The owner rulings (OWNER-ONLY, ~1 day of owner time)

Nothing in this phase is agent work. It is presented as a single sitting because
the six rulings are cheap individually and expensive as six separate context
switches.

| Ruling | What is asked | Cost to decide |
|---|---|---|
| **O-1** canon amendment `a4a3a493` | Ratify, amend, or reject: the middle emblem mark denotes the realm (all of finity), never an operand; the unit's mark is its numeral. Note two independent reasons this is genuinely open: `49_THE_THREE_MODES_OF_COUNTING.md` §3 carries both "Left open deliberately" (~:101) and "RESOLVED 2026-08-05" (:105–106), the latter warranted by a generic directive that `00_HANDOFF/SESSION_AUDIT_2026_08_05.md:155` names as the day's clearest instance of the corpus's own failure mode; and docs 48/49 are both STAGED PROPOSAL, unratified. | Read two passages |
| **O-2** OS01-01, -13, -26 | Three quoted diffs, three yes/no. OS01-01's single changed word is `finite unit` → `finite realm` — **the emblem amendment itself**, which means re-stamping it without O-1 would ratify an unratified canon change by hash. Bind OS01-01 explicitly to O-1's disposition. OS01-13 and -26 both move from "no default aggregator" to "a selected `min` default" on P = Φ×V; re-fingerprinting certifies the selected-`min` reading, which is doctrine, not a coordinate. | Read three short passages |
| **O-3** OS01-08 | Ratify the `K-7` semantic seat (absent from the legacy `{K-1, K-3}`), or fall back to a K-1/K-3 designation until ratified. Claim: "Commitment and outcome require separate, contestable receipts." | One decision |
| **O-4** register vs checker | Four rulings covering 57 errors: (a) do graves retain `repair_path`, or does it move to the successor inquiry (22 instances)? (b) same for `status_before_reopening` (21)? (c) what `investigation_state` do the 9 RQ rows carry? (d) DF-13 — is the terminal status `EMPIRICALLY-REFUTED` or `NOT-WELL-POSED`? Plus: the `owner_reopening` block is required by the checker at :346–368 against receipts 174/239 and has been deleted from the register — restore or release the requirement. | Four decisions, then scripted application |
| **O-5** `excluded_routes` | One sentence defining "withheld from the reading surface". The `1797138a` expression **cannot be restored verbatim** — it read `frozenLegacySurfaces`, a key schemaVersion 2 does not have, so a faithful restore compiles and silently excludes nothing: the exact defect it repairs. Candidate: `withheld-routes.json` `publicRoutes` (67 artifacts) ∪ the 15 `frozenLibraryRoots`; open sub-questions are whether `.html` variants and route prefixes count. | One sentence |
| **O-6** notation | Leave / sweep to the operator-free arrangement / sweep and regenerate, across ≥352 live `.html` and 79 live `.md` outside the site. Note: a decorative sign-off inside a dated receipt is arguably part of that receipt's provenance and should be **tombstoned, not rewritten**. A one-route repair is legible as a correction; a 352-page sweep is legible as a rebrand. | One decision, large consequences |
| **O-7, O-8** | Deferred out of the release path. KSC-04 / receipt 187 blocks only the trade book, which is parked. F1 blocks only a contribution claim, which the release does not make. Both may be closed at leisure; neither is scheduled here. | — |

**GATE 2.** A single signed disposition sheet exists at
`11_UPLINK/50_AUDITS_AND_EXECUTIONS/<next>_RELEASE_DISPOSITION_SHEET_2026-08-XX.md`
recording six rulings with reasons and dates. No agent act in Phase 3 begins before
its governing ruling is on that sheet.

**REVERT.** Rulings are recorded, not applied, in this phase. Reverting is
amending the sheet with a dated superseding entry.

**EFFORT.** ~1 day of owner attention, elastic across the calendar. This is the
single largest scheduling risk in the plan.

---

## 6 · Phase 3 — Apply the rulings and turn the gates green (AGENT, 5–12 working days)

This is the long pole. It is priced honestly: most of it is custody re-stamping and
authoring, and very little of it is scriptable.

| Act | Detail | Effort |
|---|---|---|
| 3.1 | Apply O-4 to `00_META/claim_status/CLAIM_STATUS.yaml`; re-run `check_claim_status.py` to green. | 1 day |
| 3.2 | Apply O-1/O-2/O-3 to `00_META/claim_cards/one_sitting.yaml` — 3 judgement cards + the K-7 seat — each with the diff quoted in the receipt. | ½ day |
| 3.3 | `00_META/claim_cards/finity_practice.yaml` v1 → v2: its 2 cards need anchors, fingerprints and owners **authored** (judgement, not transcription), and `reviewed_source_sha256` reconciled against `01_TELEOLOGY/04_THE_LIVED_COMPASS.md`. | ½ day |
| 3.4 | Apply O-5; run `check_public_semantic_parity.py` and work the **30 binding errors**: 13 `sourceRevision` drifts on the D0–D6 / μ0–μ4 canonical sources under `05_COSMOLOGY/`, 4 on index/practice/lab/manifesto claim sources, 1 on the claim-card contract, and **10 missing surface claim bindings** (compass, 5, plainly, discoveries/nonduality, about, read, axioms, journey, rosetta, book). **Every binding is a custody act, not a patch.** Add a fixture asserting the derived exclusion set is non-empty and contains a known withheld route — the failure being repaired is an exclusion set that quietly evaluates to nothing. | 3–7 days |
| 3.5 | Apply O-6. If the ruling is *sweep*: the operator-free rendering, denial on the same line where a denial is needed, dated, and **regenerate the library wings afterwards so source and artifact agree**. If the ruling is *leave*: record the figure beside every public discussion of it. Either way, `check_public_semantic_parity.py` must **enforce** the ruling, not assert it. | ½–2 days |
| 3.6 | Predeploy §15 `claimCardContract.sourceRevision` re-stamp against `00_THE_WELTANSCHAUUNG_ONE_SITTING.md` (must follow 3.2, never precede it) and §14 book-manifest schema drift. | 2 hours |
| 3.7 | Regenerate the three stale artifact generators and commit: `build_library_nav.py` (244 pages stale), `build_rag_index.py` (stale book-catalog contract), `build_sw_version.py` (cache name `emergentism-4060da5f0a1b` vs asset hash `emergentism-7938590c6a2e` — a mismatch means returning visitors get stale assets on first load after deploy). **Run after 3.5, not before.** | 2 hours |
| 3.8 | **New predeploy rule class: public claim hygiene.** Today nothing tests attribution, prior art, or whether an offered falsifier is still open — §6/§7 test only for the *presence* of a tier marker, and `check_barred_claims.py --scope public` PASSES. Two rules: (a) every stated theorem on a public page carries an attribution string or an explicit "ours" marker; (b) every offered falsifier resolves to an OPEN row in the claim register. This is the rule class that would have caught today's three `/established/` defects, none of which was reachable by any of the 16 predeploy sections or the 25 `gate.sh` checks. | ½ day |
| 3.9 | Remove the four `<loc>` blocks for `/suda/`, `/amrita/`, `/egg/`, `/riemann/` from `12_PUBLIC_SITE/sitemap.xml`, and add to `predeploy_check.py` a cross-reference of every `<loc>` against its target's robots meta, failing the build on a match. Fix the residual authoring defect: `suda/index.html:4,39`, `egg/index.html:4,47`, `amrita/index.html:4,26`, `riemann/index.html:4,39` each carry **two conflicting robots metas** (`noindex,follow` then `index,follow`) — delete the second in each. | 2 hours |
| 3.10 | **Content repairs that survive in both live and disk.** `12_PUBLIC_SITE/established/index.html`: line 50 ("claims that a machine or an exhaustive computation verifies") and line 62 ("re-computed by exhaustion on every run") are the thesis statement of the exact error the staged repair corrects 100 lines below — rewrite to "proved, or machine-checked, or bounded by a computation whose bounds are stated" and "proved — with a bounded regression re-run on every checker run, which is coverage, not warrant". Lines 537–539: retire the three remaining closed challenges with the same dated treatment as G2, or better, reframe the list head as *falsification conditions of `[A]` claims, all closed by the proofs above, published so a reader can check the proofs, not so a reader can win.* Line 228: replace "Nothing else in any ring does that" (ruled false as worded — −1 additively generates ℤ) with the kill-accurate ℤ-is-initial-in-Ring form. | ½ day |
| 3.11 | `12_PUBLIC_SITE/papers/index.html`: stop reproducing the retired form inside its own denial. Rewrite in words, per the treatment commit `2005ed5b` already applied to doc 48 §4.2. | 1 hour |
| 3.12 | **`12_PUBLIC_SITE/amrita/index.html` — the single highest-value edit on the site.** Line 64's display block and line 129's footer twin carry three retired items above the fold, captioned "Three faces of one structure": the retired infix emblem (dead twice — ill-typed 2026-08-01 per doc 45; false in content 2026-08-05 by the PGL₂(ℂ) stabiliser argument, doc 48 §4.1, whose own words are "There is no salvage sentence"); `φ · ν = 1` labelled "`[A]` the ring that closes" (DF-05 types it CATEGORY-ERROR with no successor owner); and `Φ × V = P` at `[S]`. A "not arithmetic" caption is **not** a denial marker — `THE_BOUNDARY_RULES_STANDALONE.md` §12:325 rules exactly this: the denial goes on the same line, never in a caption, never as decoration. Also strike "the one `[A]`-proven result — pure AM–GM on the reciprocal". Retire, denial on the same line, dated. | 2 hours |
| 3.13 | **OWNER (O-14):** `established/index.html` lines 7 and 19 ship "twenty machine-checked theorems" into `og:description` and the meta description. The count is right (20 `^theorem` in `09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean`); the status is not — "machine-checked" holds at one remove, the recorded build is `11_UPLINK/.../182_C_HAT_IS_NOT_A_RING_MACHINE_CHECKED_2026_07_29.md`, and the Lean file's last commit `31fa4533` (2026-08-01) postdates that build and has never been compiled. The body is honest; the snippet is what travels. Either rewrite both to "twenty theorems machine-checked at one remove (build receipt, 2026-07-29)", or drop the count from the snippet and leave it in the body where its scope clause travels with it. **Do not deploy the count unchanged while calling this a launch.** | Owner |
| 3.14 | Also fix, because a hostile reader screenshots it before reading a word: the live typo on `/discoveries/index.html` — "One method, one method, twenty-one famous knots". | 5 minutes |

**GATE 3** — all must be run and recorded, all must exit 0:

```
python3 12_PUBLIC_SITE/predeploy_check.py                       # 16/16 sections
python3 09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check
python3 09_TOOLS/01_SCRIPTS/check_claim_status.py
python3 12_PUBLIC_SITE/check_public_semantic_parity.py
python3 09_TOOLS/01_SCRIPTS/check_release_copy.py --scope public
bash    09_TOOLS/01_SCRIPTS/gate.sh
python3 -m pytest <test_corpus_claim_graph, test_claim_status, test_contact_limited, \
                   test_dimension_first_canon, test_emergentist_compass_semantics> -q
```

And one non-mechanical gate, stated because it is the point of the whole phase:
**the mutation test.** `check_public_semantic_parity.py` must be demonstrated to
FAIL on a deliberately reverted `/amrita/` before its PASS on the repaired tree is
accepted. A guard that cannot fail is worse than no guard, because it reports
success.

**REVERT.** Per-act commits. 3.5 and 3.7 touch hundreds of generated files —
those two get their own commits so a revert does not entangle the content repairs.

**EFFORT.** 5–12 working days. The spread is real and it is almost entirely 3.4:
17 `sourceRevision` re-stamps and 10 authored surface claim bindings, every one a
custody act. Do not present this as an afternoon.

---

## 7 · Phase 4 — The correction deploy (OWNER-ONLY act, agent-prepared, ½ day)

**What ships.** One whole-tree upload of corrections already committed. **No new
claim.** 310 changed `.html` files relative to the live build. The live build is
commit `b7e0d00d` (2026-08-01), identified by the live `sw.js` cache token
`22eef5cf55bd`, which appears at that commit and nowhere later. Five routes differ
materially and every one differs in a direction where the live text states
something the corpus has since refuted or retired: `/established/`, `/plainly/`,
`/axioms/`, `/record/`, `/5/`. Six more differ only by the undeployed `noindex`
line — which is signed ruling Q6
(`11_UPLINK/.../193_FIVE_RULINGS_SIGNED_2026_07_31.md`, 3–1) and is currently
unenforced: `/titans/`, `/titans.html`, `/papers/`, `/formal/`, `/foundations/`,
`/trinity/` serve with **no robots meta at all**, and `/suda/`, `/amrita/`,
`/egg/`, `/riemann/` serve with `index, follow` and **no `[D]` frozen-library
banner**, so they present as current pages.

**Pre-flight, in order, no step skippable**

```
# 1. working tree must equal HEAD — a deploy publishes the tree, not a commit
git status --porcelain          # must be empty; today it shows
                                # 12_PUBLIC_SITE/sw.js and 12_PUBLIC_SITE/atlas/library_index.json modified

# 2. record what is about to be published
git rev-parse HEAD > /tmp/deploy_sha
git diff --name-only b7e0d00d..HEAD -- 12_PUBLIC_SITE | grep -c '\.html$'

# 3. OWNER (O-10): push, so the site's own "Check it yourself" block is not stale
#    The clone block names circumvectio/emergentism @ codex/emergentism-live-dirt-custody-20260730,
#    verified today at fa3b116b (2026-07-30) with all three raw URLs returning 200 — but that
#    branch's check_generative_base.py still says "Verify G1-G5" and still owes "a complete
#    injectivity proof", i.e. it contradicts the page the moment the page deploys.
#    The page has already been caught twice by audits for this block. This would be the third.

# 4. re-verify the three raw.githubusercontent URLs named in the clone block

# 5. the deploy itself — OWNER (O-11)
cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE && ./deploy_vercel.sh
```

`deploy_vercel.sh` self-sequences: `--self-test`-capable target contract → env pin
against `.vercel/project.json` (project `emergentism-org`) → `predeploy_check.py`
→ `check_site_build_artifacts.py` → `vercel --prod --yes`. It refuses arguments,
so the `--prebuilt` bypass is unreachable through the wrapper — which is why 1.10
deleted the snapshot the bare CLI could have published.

**Post-deploy verification, same session, non-optional**

```
python3 12_PUBLIC_SITE/audit_live_domain_against_manifest.py --strict
# then diff the five material routes against HEAD, byte for byte
for r in established plainly axioms record 5; do
  curl -sS "https://<vercel-alias>/$r/" | diff -q - "12_PUBLIC_SITE/$r/index.html" || echo "DRIFT: /$r/"
done
```

Then **add that post-deploy diff as a permanent step in `deploy.sh`**. The corpus
already learned once, at receipt №027, that having a result verified somewhere is
not the same as having it applied anywhere.

**GATE 4.** The strict live audit exits 0 and is filed as a receipt; the five-route
diff is clean; the receipt records **deployment id, the git sha, and the generator
input sha** — because no existing deploy receipt binds a deployment to a commit
(`11_UPLINK/.../118_*.md` records deployment `emergentism-jwuwy61p4` and a page
count, no sha). Until that binding exists, "what is live" is answerable only by
probing the domain.

**REVERT.** Promote the previous deployment in Vercel — do **not** re-upload the
old tree, which would republish the retired notation from a working directory that
no longer matches any commit.

**EFFORT.** ½ day agent preparation. Owner: the push, the deploy, ~30 minutes.

---

## 8 · Phase 5 — Canonical host (OWNER-ONLY, O-12, blocking for the manual)

`robots.txt` advertises `Sitemap: https://emergentism.org/sitemap.xml` and all 44
`<loc>` entries are `https://emergentism.org/…`, while `www.emergentism.org` still
resolves to `ghs.googlehosted.com` and serves an old Google Sites page, the apex is
mixed with a Squarespace A record, and the domain is not attached to the Vercel
project. `audit_live_domain_against_manifest.py` defaults to
`https://www.emergentism.org/` and is deliberately non-strict for exactly this
reason.

**Why this blocks the manual and not the correction deploy.** A correction deploy
improves whatever the Vercel alias serves regardless of DNS. A *published document*
needs a stable URL and a provenance note pointing at a real host. Publishing the
manual while the advertised canonical host serves someone else's page is a
self-inflicted credibility wound of exactly the kind this plan exists to avoid.

**Act.** Registrar change plus `vercel domains add`, per
`11_UPLINK/50_AUDITS_AND_EXECUTIONS/118_SHIP_RECEIPT_VERCEL_PROD_DNS_CUTOVER_OWED.md` §2.
Then re-run the strict live audit against the real canonical host and file it.

**GATE 5.** `audit_live_domain_against_manifest.py --strict` exits 0 against
`https://emergentism.org/` **and** `https://www.emergentism.org/`.

**Alternative, if the cutover is not wanted:** host the manual at a URL that does
not depend on the corpus domain at all, and say so in the provenance note. That is
acceptable and it is a decision, not a fallback.

**EFFORT.** Owner, ~1 hour plus DNS propagation.

---

## 9 · Phase 6 — The release (AGENT edits, OWNER publication, ½ day + O-13)

### The payload

**Name.** *Boundary Rules — an operating manual for writing at the edge of a
domain. Version 1, draft.*

**Source.** `02_EPISTEMOLOGY/01_EVIDENCE_TIERS/THE_BOUNDARY_RULES_STANDALONE.md`,
397 lines, §§0–15.

**Tier.** `[D] DRAFT 1`. **Do not promote the tier to buy respectability.** §0's
line-local strikeability is the honest status and costs nothing.

**Form.** One document. Not a site, not a launch, not a book, not a folder. A PDF
or a single page under its own name, with a stable URL and a date.

### The three edits (AGENT)

1. **Delete the boundary marks from §12** (:311–326), from §6's `log ○` / `√•` /
   `card(•)` and `• = 0` / `○ = ∞` rows (rewrite generically as "a boundary
   label"), and from card item 10. Keep rule N restated in words. **Reason, in the
   manual's own sentence:** *"A version of this manual with the marks deleted is
   exactly as strong."* This removes the manual's only dependency on O-1 — and
   §12's "Draft-1 history" paragraph, honest as it is, narrates the middle mark's
   sort changing region→point→region inside one day, which is the single most
   quotable instability in the document.
2. **Neutralise §5's parent reference** (:174): "the corpus this manual comes
   from" → "one framework that uses these rules". Keep the fence verbatim — it is
   the strongest sentence in §5 — and move the provenance to the note, not the
   body.
3. **Ship §13's eight self-reported defects in the body**, not as an appendix,
   including §13.4's concession that the boundary-label/non-member identification
   "is the defect most likely to be present".

### The provenance note (one page, appended)

Who wrote it. That it came out of a philosophical corpus. That the corpus's own
prior-art sweep found six of its seven boundary claims pre-empted and its one open
mathematical conjecture proved and found to be Hardy & Wright's. That the manual is
the part that survived. That §14 credits Brahmagupta, Cauchy, Möbius, Setzer,
Carlström, Bergstra, Kahan, Lan–DeMets and Goldacre rather than claiming them.

**That paragraph is the entire self-check story, told once, as the answer to "why
trust this document" — and never as the pitch that answers "why should I care
about you."**

### The framing ruling, stated so it cannot drift

Neither *"here is our discovery"* nor *"here is what we found when we checked
ourselves."*

The first is refuted by the corpus's own instruments: F1 open with its first and
only candidate adjudicated prior art, F0 NOT PASSED, F2–F4 not started, 155
receipts and zero outcome receipts from outside.

The second is worse, and this is the load-bearing judgement of the plan. The
corpus's named failure mode is *evidence of checking published as the warrant*. A
release headlined "here is what we found when we checked ourselves" takes the
checking record and offers it as the reason to take the corpus seriously. That is
not an instance of the failure mode; it is the definition of it, performed at
maximum scale in the one venue where it cannot be quietly corrected. It is
self-refuting: the moment self-checking becomes the pitch it stops being
self-checking and becomes marketing, and every subsequent kill acquires a motive.
The corpus already ruled this way once — `14_THE_DISTILLATION/05_THE_METHOD.md` §6
deliberately excludes the Kintsugi corollary that a repaired claim outranks an
untested one, "because that converts the record of a repair into a warrant for the
claim."

**The subject of the release is the tool, never the corpus.** Headline: the rules.
Provenance: the record. Never the reverse. **Operational test for every sentence of
release copy: if a proposed sentence has the corpus as its grammatical subject, cut
it.** Second test, from the site's own front page: if a sentence would not sit
comfortably next to *"the number that matters most is zero"*, cut it.

### Pre-flight (AGENT, all must run)

```
python3 09_TOOLS/01_SCRIPTS/check_release_copy.py --surface <manual> --surface <provenance-note>
python3 09_TOOLS/01_SCRIPTS/check_g2_normal_form.py
grep -n 'the corpus this manual comes from' 02_EPISTEMOLOGY/01_EVIDENCE_TIERS/THE_BOUNDARY_RULES_STANDALONE.md   # must return nothing
```

**GATE 6.** Gate 0 through Gate 5 all green with receipts; `check_release_copy.py`
exits 0 on both surfaces; the manual's URL resolves; nothing else is published in
the same act.

**REVERT.** Unpublish the URL and record a dated withdrawal note. A published
document cannot be un-read, which is the reason for every gate above it.

**EFFORT.** ½ day agent. Owner: the publication act.

---

## 10 · Gate ledger — must-pass vs desirable, with today's measured state

**MUST PASS before anything is published.** No exceptions, no forcing.

| # | Gate | Command | State 2026-08-05 |
|---|---|---|---|
| M1 | Deploy boundary | `python3 12_PUBLIC_SITE/predeploy_check.py` | **RUN → FAIL, exit 1, 585 errors** across 6 of 16 sections: §10 withholding (535), §16 contact-limited (20), §15 reading manifest (13), §13 claim cards (8), §12 parity (8), §14 book manifest (1). §§1–9, 11 PASS. |
| M2 | Generated-artifact agreement | `python3 09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py` | **RUN → FAIL**: 244 stale nav pages, stale RAG book-catalog contract, `sw.js` cache-name mismatch |
| M3 | Public semantic parity | `python3 12_PUBLIC_SITE/check_public_semantic_parity.py` | **RUN → NameError `excluded_routes` at :540. Has never executed.** Second latent NameError: `fnmatch` used at :216/:218, never imported. Scope defect: audits 48 of 799 files. |
| M4 | Claim-card custody | `python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check` | **RUN → FAIL at OS01-01.** 25 of 26 locators defective; 38 of 55 tests fail, all with the identical message. |
| M5 | Claim status | `python3 09_TOOLS/01_SCRIPTS/check_claim_status.py` | **RUN → NameError `reopened_ids` at :705.** Fully reconciled in a scratch copy it reports **57 errors**. |
| M6 | Corpus gate | `bash 09_TOOLS/01_SCRIPTS/gate.sh` | **RUN → FAIL**, ~15 checks and 6+ test files |
| M7 | G2 / generative base / established | `check_g2_normal_form.py`, `check_generative_base.py`, `check_established.py` | `check_g2_normal_form.py` **is not in `gate.sh`'s `CHECKS` array** — invoked by nothing. Others wired. |
| M8 | Release-copy prohibition grep | `python3 09_TOOLS/01_SCRIPTS/check_release_copy.py` | **DOES NOT EXIST.** Created in Phase 0.7. |
| M9 | Live-domain truth, post-deploy | `python3 12_PUBLIC_SITE/audit_live_domain_against_manifest.py --strict` | **NOT RUN.** Exits 0 without `--strict` by design, because the domain points elsewhere. This is the only check in the system that tests what a reader actually receives. |

**DESIRABLE, not release-blocking.** Real work; does not gate publication.

- Re-record the 56 of 67 drifted withholding artifact sha256/bytes (record hygiene; **no exposure** — Layer A holds).
- Re-point the four orphan claim-card files at live `02_SKYZAI` paths (28 cards, never contract-checked in this checkout). *Making the SKIP explicit **is** blocking, cheaply — Phase 0.9.*
- Wire or delete `check_dead_citations.py`, `check_forwarding_stubs.py`, `check_tree_contract.py`.
- Recompile `09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean` at `31fa4533` and file a fresh build receipt. *Desirable; the `og:description` fix (O-14) is blocking and independent.*
- Sweep the 79 live `.md` outside the site carrying the retired form. **Record the figure; do not sweep** — a decorative sign-off in a dated receipt is part of that receipt's provenance.
- Restore rather than delete `check_public_semantic_parity.py`'s `.vercelignore` classification loop (higher value: the only mechanism that notices a *new* unclassified public file).
- Verify Kepler *Harmonices Mundi* 1619 and Berstel–de Luca 1996 (Raney tree) against page-level sources — **blocking only if any part of the trade book ever ships**.
- Reconcile `00_KNOWN_UNKNOWNS.md` KU-6 ("Reopened" on SU(3)) and KU-7 (the refuted Lagrangian).
- Doc 48:331 (withdrawn path-independence contrast inside a block headed MAY NEVER BE DROPPED) and 48:380 (slogan its own child rules false-or-empty, no correction marker while §4.1 and §5.2 carry theirs).
- Write the supersession line **into** `07_THEOLOGY/00_THE_AMRITA.md` — required before anything downstream of `14_THE_DISTILLATION` is quoted publicly, including in the manual's provenance note.
- `00_HANDOFF/` release-scope decision record, dated, with a reason beside each excluded payload. *This artifact does not exist, which is why four payloads were in contention at once.*

---

## 11 · The prohibition list (binding annex; becomes `00_META/RELEASE_PROHIBITION_LIST.md`)

Nothing on this list may appear in the manual, the provenance note, the site, a
snippet, a caption, a decorative sign-off, or a denial that reproduces the thing it
denies. Each line carries a dated receipt in the file version.

**A · Mathematical claims**

1. The retired infix emblem product form, and its two rearrangements — **dead twice**: ill-typed 2026-08-01 (`45_THE_TITAN_INVERSION_STRUCTURE.md`); false in content 2026-08-05 by the PGL₂(ℂ) stabiliser argument (doc 48 §4.1, classical Möbius/Klein). No display use, no sign-off, no "not arithmetic" caption. **Denial on the same line, or not at all.**
2. "Any two of the three positions fix the third" — false; the stabiliser of {0, ∞} in PGL₂(ℂ) acts transitively on ℂ*. **"There is no salvage sentence."**
3. G2 as a mathematical contribution — it is Hardy & Wright ch. X (also Khinchin §I.2, Perron), with Euclid underneath. Never state it without the owner on the same line. Doc 55 §7 forbids citing it as passing F1.
4. "Find two different reduced words with the same value" as a live challenge — closed ~150 years.
5. `φ·ν = 1` as a discovery, a conserved quantity, a "keel", or "the ring that closes" — DF-05 types it CATEGORY-ERROR with no successor. It is cot(θ/2)·tan(θ/2) ≡ 1, and it is safe only because ν is *defined* as 1/φ.
6. "Zero is not a number" / "X is not a number" bare — banned phrasing, signed 2026-07-31. Write 0 ∈ ℝ, 0 ∉ ℝˣ.
7. "−log(φ·ν) is the energy" / "every displacement from the equator costs energy" — refuted; identically zero. Repaired form: E = φ + ν − 2.
8. "Nothing else in any ring does that" — false as worded; −1 additively generates ℤ.
9. SU(3) / Standard Model from S² in any direction — all four paths closed, K2-countersigned 2026-08-04. **And** its mirror: "an SU(3) gauge theory cannot be defined over S²" — retracted; the bundle exists.
10. Gödel lifting universally — Presburger 1929, Tarski 1948–51.
11. "The framework is restored by proof on ℂP¹" — stale agent memory, contradicted by disk.

**B · Gate and status claims**

12. F0 may not be cited as cleared — **NOT PASSED**; its negative tests are three `assertIn` substring assertions on prose, and CM-04, which requires an expression to fail type checking, is "verified" by its own id appearing in a document. Nothing type-checks; no executable term language exists.
13. F1 may not be cited as passed — **OPEN**, first and only candidate adjudicated prior art.
14. F2, F3, F4 — **NOT STARTED**. No utility, scientific-contact or independent-transmission claim may be made at all. F4 is reopened by this plan.
15. "Machine-checked" never flat — say **at one remove**, every time.
16. μ₂ and μ₃ may not be presented as open — adjudicated FAILED, and both failures survive the change of instrument. μ₀ owes its discriminator; HR-1 is open.
17. The four-status taxonomy may not be presented as tested — the pre-registered twenty-reader test against a control **has never been run**.
18. **Any release copy asserting a gate state must quote the gate table verbatim, not paraphrase it.** Paraphrase is where promotion happens.

**C · Laws, aggregators, framings**

19. P = Φ×V is an **AND-class law**, not a proved product. KSC-02 adopts `min` as the working score and retires the product as a ranking. No aggregator is established. R6 shows the composition is additive in the empowerment register, where φ·ν = 1 marks the **dead state**, and the sum is 6–10× more conserved than the product in every regime.
20. η = 0 is a conditional gate, not a consequence of any count.
21. The extraction law's squid exemplar is refuted — *Dosidicus gigas* is panmictic, semelparous, weak-targeting: the counterexample.
22. The symmetric balance hump is dead twice — data show a trough (Munnell), and the pre-registered instrument was retracted for construct invalidity.
23. N = 3 is **selected**, not derived — the discharging lemma is false (ℤ₅ has no proper subgroups, by Lagrange).
24. Seven-as-forced is refuted — planetary confound; one lineage counted as many.
25. The Rosetta, L1–L7, the D0–D6 ladder, Justice/Power-Max formulae, the 5+1 Constitution, the paradox dissolutions (DF-18 NOT-WELL-POSED), the Titan ontological reading, the Samudra Manthan, and "the potential reading" — none may enter a release **as a finding**.
26. "Three faces of one structure" — the `/amrita/` caption binding the emblem, φ·ν and Φ×V — may not be published in any form.

**D · Provenance and process claims — the ones a release makes by accident, because they feel like modesty**

27. No claim that the method works — `[C]`, never run as a controlled trial.
28. No claim that the receipt/register system is an executed practice — the instance has fired its own kill. **Copy the rule; do not sell the instance.**
29. No claim of external validation — 155 receipts, zero outcome receipts from outside. `/discoveries/` already says "none has yet been independently validated by an external human reviewer". **That sentence must not be softened.**
30. Suda (PhilArchive 2025) may not be cited as convergent support — rule S3, one claim twice.
31. No claim that the boundary rules are enforced — their own frontmatter says `not_a_gate`; §13.8 says read every enforcement statement in the subjunctive.
32. No claim that corrections have propagated — several have not.
33. **No count may be quoted that was not re-run in the same pass.**

**Standing condition.** Where this list is summarised, adopt the corpus's own
sentence verbatim: *"None of that is thereby false. It is unchecked, or selected,
or interpretive, and those are different things from false."* And its condition:
quietly shortening the list turns the artifact into a promotion path.

**If the "21 proved, 1 owned" figure ever ships**, it ships with the admission
function on the same line: `14_THE_DISTILLATION/01_WHAT_IS_PROVED.md` admits `[A]`
only, so the count measures theorem-ownership and nothing else. Omitting that turns
an honest measurement into unfalsifiable humility — the mirror image of the
overclaim, and equally unhelpful. **If stating the admission function feels like it
weakens the sentence, that is the signal the sentence was being used
rhetorically.**

---

## 12 · Honest calendar

| Phase | Agent | Owner | Elapsed |
|---|---|---|---|
| 0 · Paper repair | 4 h | — | ½ day |
| 1 · Gates honest | 2–3 days | 15 min (O-9, blocking) | 3 days |
| 2 · Rulings | — | ~1 day, elastic | 1–7 days |
| 3 · Apply + green | 5–12 days | ~½ day (O-14, 3.2 review) | 5–12 days |
| 4 · Correction deploy | ½ day | ~30 min (O-10, O-11) | 1 day |
| 5 · Canonical host | — | ~1 h + propagation | 1–2 days |
| 6 · The manual | ½ day | publication act (O-13) | ½ day |

**Total: three to four calendar weeks** to the manual in public, assuming owner
rulings land within a week of being asked. The dominant uncertainty is act 3.4 —
17 `sourceRevision` re-stamps and 10 authored surface claim bindings, each a
custody act — and the second is O-2/O-4 latency. Anyone who prices this as an
afternoon has priced the traceback and not the custody.

---

## 13 · What is explicitly not in this plan

- **The distillation (`14_THE_DISTILLATION/`).** Its own README §10 kill fires on the act of citing it as authority, and public release *is* that act — a reader outside the repo has no source to prefer over it, which voids the §2 rule that source documents retain semantic ownership. Its supersession of `07_THEOLOGY/00_THE_AMRITA.md` is also one-sided, so releasing it publishes two distillations giving two answers. **Use it as designed: the internal instrument that says what may not be said in public. It is the source of §11, not a publication.**
- **The trade book (`13_BOOKS/titans/`).** Ch.9's load-bearing premise — that accountability to a declared bound is unowned — is refuted in three of the corpus's own files; 0 of 4 declared preconditions are met; 4 of 11 chapters exist; the twenty-reader test has never been run; and §11 says outright that shipping before §8's preconditions "has become the thing it was written to avoid and should be withdrawn." Park it. If one piece ever goes out, it is Ch.8, and only after Kepler and Berstel–de Luca are verified at page level.
- **The honesty protocol as a product.** Efficacy `[C]`; its own frontmatter violates its own strip test.
- **The four-status taxonomy standalone.** Ch.4 of an unfinished book whose single pre-registered test has not run — and, by its own closing words, "a piece of ordinary equipment", which is right and is not a release.
- **Any corpus-wide notation sweep as a release act.** `14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md` item 4 correctly routes republication to OWNER-ONLY. It appears here only as ruling O-6 and its enforcement.

---

## 14 · Kill criteria for this plan

- **A gate goes green without a mutation test.** If `check_public_semantic_parity.py` reports PASS and has not been shown to FAIL on a reverted `/amrita/`, the gate is decorative and this plan's Phase 1 has failed on its own terms.
- **The scope repair lands after the name repair.** If `excluded_routes` is defined before the scan walks every deployable file, the first green PASS is a lie and the plan should be restarted at 1.1.
- **A receipt dated after this plan cites a claim-status or claim-card PASS without recording an exit code.** That is the seventh instance recurring, and it means the ledger did not learn.
- **Any owner-only item in §2 appears as completed work in an agent's receipt.** Stop, revert, and re-scope.
- **The release copy acquires a sentence whose grammatical subject is the corpus.** The framing ruling in Phase 6 has failed and the payload should be withheld until it is rewritten.
- **The manual ships in the same act as anything else.** A second artifact turns a manual into a launch, and a launch has a subject.

The right ambition is the corpus's own, from `CH09`: *"to become boring — to end up
in the sort of place where nobody cites it because everybody does it."*