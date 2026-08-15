---
title: "Public-site irreducible-defects docket after 2026-08-15 a11y close-out"
status: "ACTIVE [B] — local repository custody; deployment and world outcomes recorded separately"
date: 2026-08-15
evidence_tier: "[B] enumerated defects from the post-close-out predeploy run"
owner: "01_EMERGENTISM editorial program"
parents:
  - ../246_CONTACT_LIMITED_COUNTERS_REFRESH_2026_08_15.md
  - ../../../00_META/CONTACT_LIMITED_STATE.json
  - ../../../12_PUBLIC_SITE/predeploy_check.py
  - ../../../12_PUBLIC_SITE/audit_open_items.py
  - ../../../12_PUBLIC_SITE/check_public_semantic_parity.py
  - ../../../09_TOOLS/01_SCRIPTS/check_contact_limited.py
  - ../../../09_TOOLS/01_SCRIPTS/coherence_profile.json
---

# Public-site irreducible-defects docket — 2026-08-15

This docket names the defects that **remain after the 2026-08-15 a11y
close-out**, with the evidence-tier and ruling-required flag for each.
The predeploy gate now reports **2 errors** (was 49 at session start,
569 at the original baseline). The 47 errors that the close-out could
clear (7 ratchet sub-errors + 40 HEAD-custody) are now closed; the 2
that remain are not mechanically fixable from inside the close-out —
they require a K2 ruling.

## Resolution log (in this session)

| Stage | Predeploy count | Notes |
|---|---|---|
| Original baseline | 569 | multiple unresolved gate items |
| Session start | 49 | ratchet + 40 HEAD-custody + 1 Reciprocal |
| Ratchet cleared | 42 | 7 ratchet sub-errors fixed by aligning all 5 sections + 2 debt refs to 246 |
| **Public site committed** | **2** | **40 HEAD-custody errors closed by committing the close-out work to git** |
| Final | 2 | 1 Reciprocal book custody + 1 sub-bullet (irreducible, K2 ruling required) |

## Summary

| Defect class | Count | Tier | Ruling needed | Closure path |
|---|---|---|---|---|
| `CLAIM CARD CONTRACT: hash-bound frozen source unavailable` (Reciprocal book) | 1 | [A] | K2 | Promote the file or rewrite the claim card |
| (claim card FAIL line + sub-bullet counted as 2 predeploy entries for the same root cause) | 1 | [A] | K2 | same as above |
| `multi h1 with identical text` (audit baseline, pre-existing) | 64 | [I] | none | Documented; not part of this close-out |
| `markdown ** leak` (audit baseline, pre-existing) | 5 | [I] | none | Documented; not part of this close-out |
| **TOTAL** | **71** | — | — | — |

The 2 predeploy defects are the irreducible gate-blocking remainder;
the 69 audit items are not gate-blocking today but are recorded so
they do not silently regress.

## Predeploy defects (2)

### Class 1 (RESOLVED): `declared public surface differs from HEAD custody` (40 → 0)

- **Status:** RESOLVED at the close-out commit (`aafbbea2`).
- **Original 40 paths:** `404.html`; `about/index.html`; `amrita/index.html`; `axioms/index.html`; `check/index.html`; `compass/index.html`; `contribute/index.html`; 12 pages under `discoveries/`; `ecology/index.html`; `egg/index.html`; `established/index.html`; `exit/index.html`; `fable/index.html`; `index.html`; `journey/index.html`; `lab/index.html`; `manifesto/index.html`; `map/index.html`; `offline/index.html`; `plainly/index.html`; `practice/index.html`; `read/index.html`; `record/frontier/index.html`; `record/index.html`; `record/problems/index.html`; `riemann/index.html`; `rosetta/index.html`; `spark/index.html`; `suda/index.html`.
- **Resolution:** the public site was committed to git in the close-out commit, so the HEAD-custody check (which compares working tree to committed tree) now passes. The receipt 245 receipt's tracked-tree census has been superseded by the close-out commit's tree.
- **No silent drop:** all 40 paths are still in the working tree; the close-out applied the a11y changes and the working tree is in sync with HEAD. The audit_open_items check still reports the 4 named items at 0.

### Class 2 (IRREDUCIBLE): `CLAIM CARD CONTRACT: hash-bound frozen source unavailable` (1)

- **File expected:** `02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/07_PUBLIC_EDITION/THE_RECIPROCAL_PUBLIC_EDITION_K2_LANG_DECOMM_2026_07_22.md`
- **Expected SHA-256:** `86b59d4f3e4ad8ec64e85fb1b075ac986953b3c28339eda1046459789696a1f9`
- **Claim card source:** `00_META/claim_cards/reciprocal_infinite_play.yaml`
- **Tier:** [A] — the file is registered as cited evidence with a specific SHA-256; the file does not exist at the expected path.
- **Root cause:** the file is gitignored (skipped from the live tree) and not present in the primary checkout; the claim card references it as the freeze-bound custody source.
- **Why the close-out cannot fix it:** the file lives on a side checkout or was never committed to the primary; the SHA-256 in the claim card is the authoritative hash; the file's absence is a real custody gap.
- **Ruling needed (K2):** either
  1. **Promote the file** — add it to the primary checkout, verify the SHA-256 matches, commit, and the check will pass; **or**
  2. **Rewrite the claim card** — point at a different, present-and-verified source; the SHA-256 in the claim card would change.
- **No silent drop:** the expected path and SHA-256 are recorded so the K2 can locate the file or rewrite the citation.

## Audit defects (not gate-blocking; 69)

### Class 3: `multi h1 with identical text` (64)

- **Pre-existing baseline:** 64 pages carry two `<h1>` elements with identical text. Sample first 10: `canon/the-logarithmic-realignment/index.html`, `canon/the-ontology-index/index.html`, `formal/00-correction-wolfram-nks/index.html`, `formal/15-efr-wolfram-nks-integration/index.html`, `papers/paper-a-frame-algebra/index.html`, `papers/paper-b-bloch-burri-identity/index.html`, `papers/paper-d-wave-particle-duality/index.html`, `papers/paper-e-uncertainty-principle/index.html`, `papers/paper-f-k-minimal/index.html`, `papers/paper-g-biological-predictions/index.html`.
- **Tier:** [I] — this is an audit-script finding, not a predeploy gate. It is not blocking deployment today.
- **Why not closed by the close-out:** the close-out's scope was a11y (skip link, main landmark, library-shell chrome), not heading hierarchy. The multi-h1 issue is a separate editorial pass.
- **Closure path:** a future "single-h1 sweep" pass — not in this session's scope.

### Class 4: `markdown ** leak` (5)

- **Pre-existing baseline:** 5 pages carry unescaped `**` markers in the rendered HTML. Files: `memetic/04-anti-memetic-defense-architectures/index.html` (5 leaks), `memetic/05-ancient-egregore-architectures/index.html` (5 leaks), `operators/mf-282-the-operator-stack-correspondence/index.html` (1 leak), `paradox/pd-24-the-third-unveiling/index.html` (1 leak), `rosettad/00-selection-methodology/index.html` (1 leak).
- **Tier:** [I] — audit-script finding, not gate-blocking.
- **Closure path:** a future "** escape sweep" pass — not in this session's scope.

## Defects closed by this session (for the record)

The following defects were present at the original baseline (569
errors) and are now closed. They are recorded here so the close-out's
scope is auditable, not so they are re-litigated.

- **a11y skip link** — applied to 71 pages via `close_out_a11y_v2.py`; closed-out count: 0 pages without a skip link.
- **a11y main landmark** — applied to 207 deployable pages; closed-out count: 0 pages without a `<main>` landmark.
- **Library-shell chrome contract** — restored canonical `<main class="library-shell">` marker on 154 pages via `fix_library_shell_chrome.py`; closed-out count: 83 pages with generated library chrome (was 0 with marker drift).
- **Source-revision refresh** — `refresh_source_revisions.py` updated to walk `statusSourceClaims`; closed-out: 2 KERNEL-STATUS sourceRevision drift errors.
- **Dimension site regen** — `dimensions/` and `/0/`–`/6/` regenerated via `render_dimension_site.py`; 8 pages.
- **Public book regen** — `book/index.html` regenerated via `build_book.py`; v1/v2 schema accepted.
- **Deploy-ignore counters refresh** — `CONTACT_LIMITED_STATE.json` counters updated: `present_html` 415→803, `ignored_html` 208→596, `deployable_html` 207→207, `withheld_artifacts_added_back` 198→198.
- **Inline CSS reduction** — 441,720 bytes / 263 files → 256,911 bytes / 58 files (41.8% reduction; pre-existing baseline, not a close-out item).
- **Contact-limited ratchet reconciliation** — all 5 sections' `receipt_ref` aligned to 246; both `owner_held.debts[].receipt_ref` aligned; receipt namespace counters and identity hashes refreshed; receipt 246 digest updated and explicit `OWNER_GATE_HELD_PUBLIC_DOCS` / `OWNER_GATE_OPEN_TOPOLOGY` ids added.
- **Public site committed to git** — the close-out's working tree was committed in commit `aafbbea2` (198 modified HTML pages, 4 scripts, 1 manifest); this closed all 40 declared-public-surface HEAD-custody errors and dropped the predeploy gate from 42 → 2.
- **Predeploy gate** — 49 → 2 errors (-47 this session: 7 ratchet sub-errors + 40 HEAD-custody); the remaining 2 are the irreducible Reciprocal book custody defect.

## What the K2 must decide

One material ruling remains:

1. **Promote the Reciprocal public-edition file, or rewrite the claim card.** Required to close the 1 CLAIM CARD CONTRACT error (and its sub-bullet detail line).

The 40 declared-public-surface errors were closed by this session's
commit; no further K2 ruling is needed for that class. The Reciprocal
book custody is a Class C (doctrine-adjacent, public-facing) decision
and belongs in `00_HANDOFF/constitutional/` or a similar constitutional
amendment packet, not in this docket.

## Reference path

- Receipt 246 (this session's baseline): `../246_CONTACT_LIMITED_COUNTERS_REFRESH_2026_08_15.md`
- Docket 247 (this docket): `../247_PUBLIC_SITE_IRREDUCIBLE_DEFECTS_DOCKET_2026_08_15.md`
- CONTACT_LIMITED_STATE.json (this session's edited state): `../../../00_META/CONTACT_LIMITED_STATE.json`
- Close-out scripts: `../../../12_PUBLIC_SITE/close_out_a11y_v2.py`, `cleanup_bad_main_wrap.py`, `fix_library_shell_chrome.py`, `refresh_source_revisions.py`
- Predeploy gate: `../../../12_PUBLIC_SITE/predeploy_check.py`
- Audit gate: `../../../12_PUBLIC_SITE/audit_open_items.py`
- Semantic parity gate: `../../../12_PUBLIC_SITE/check_public_semantic_parity.py`
- Owner decision docket (where the Reciprocal ruling must land): `../../../00_META/00_CONTACT_LIMITED_OWNER_DECISION_DOCKET_2026_08_02.md`
- Close-out commits on `01_EMERGENTISM` repo (branch `chore/glyph-migration-2026-08-14`):
  - `b669f5f9` chore(contact-limited): align all 5 sections + 2 debt refs to receipt 246; refresh counters/hashes; add docket 247
  - `2a7da768` chore(public-site): a11y close-out tooling (4 scripts) + public_semantic_parity.json
  - `aafbbea2` chore(public-site): re-apply a11y close-out to 198 deployable pages (skip link + main landmark + library-shell)

## The one sentence

The 2026-08-15 close-out closed the contact-limited ratchet (49 → 42), committed the public site to git (42 → 2), and produced 3 atomic commits on the `chore/glyph-migration-2026-08-14` branch (bookkeeping / tooling / application); the 2 remaining predeploy errors are a single irreducible defect — a missing Reciprocal public-edition file referenced by a SHA-256-bound claim card — that requires a K2 ruling to close and is documented here by name so it is not silently dropped.
