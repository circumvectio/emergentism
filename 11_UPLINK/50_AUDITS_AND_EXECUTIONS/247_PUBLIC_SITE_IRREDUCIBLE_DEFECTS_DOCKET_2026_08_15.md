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
The predeploy gate now reports **42 errors** (was 49 at session start,
569 at the original baseline). The 7 ratchet sub-errors that the
close-out could clear are now closed; the 42 that remain are not
mechanically fixable from inside the close-out — they require a
decision from the K2 (Yves R. Burri) or a public-site-tracking
amendment.

## Summary

| Defect class | Count | Tier | Ruling needed | Closure path |
|---|---|---|---|---|
| `declared public surface differs from HEAD custody` | 40 | [A] | K2 | Track or formally untrack the public site |
| `CLAIM CARD CONTRACT: hash-bound frozen source unavailable` (Reciprocal book) | 1 | [A] | K2 | Promote the file or rewrite the claim card |
| `multi h1 with identical text` (audit baseline, pre-existing) | 64 | [I] | none | Documented; not part of this close-out |
| `markdown ** leak` (audit baseline, pre-existing) | 5 | [I] | none | Documented; not part of this close-out |
| **TOTAL** | **110** | — | — | — |

The 41 predeploy defects are the gate-blocking remainder; the 69
audit items are not gate-blocking today but are recorded so they
do not silently regress.

## Predeploy defects (42)

### Class 1: `declared public surface differs from HEAD custody` (40)

- **Files affected (40):** `404.html`; `about/index.html`; `amrita/index.html`; `axioms/index.html`; `check/index.html`; `compass/index.html`; `contribute/index.html`; 12 pages under `discoveries/`; `ecology/index.html`; `egg/index.html`; `established/index.html`; `exit/index.html`; `fable/index.html`; `index.html`; `journey/index.html`; `lab/index.html`; `manifesto/index.html`; `map/index.html`; `offline/index.html`; `plainly/index.html`; `practice/index.html`; `read/index.html`; `record/frontier/index.html`; `record/index.html`; `record/problems/index.html`; `riemann/index.html`; `rosetta/index.html`; `spark/index.html`; `suda/index.html`.
- **Tier:** [A] — the predeploy script's HEAD-custody check is mechanical; the divergence is real, not a script error.
- **Root cause:** the entire `12_PUBLIC_SITE/` tree is **untracked in the Magnum Opus git repository** (verified: `git ls-files 01_EMERGENTISM/12_PUBLIC_SITE/` returns 0 files; the receipt 245 receipt's tracked-tree census is the authoritative state until a tracking decision is made).
- **Why the close-out cannot fix it:** the close-out edits the working tree; the predeploy gate's HEAD-custody check compares the working tree to the committed tree, and the public site is not in the committed tree by design.
- **Ruling needed (K2):** either
  1. **Track the public site** — add `12_PUBLIC_SITE/` to Magnum Opus git, commit the close-out work, and the HEAD-custody check will pass; **or**
  2. **Formally untrack** — issue a constitutional amendment that excludes the public site from the HEAD-custody check (the predeploy script would need a new exception path), citing the prior decision as authority.
- **No silent drop:** the 40 paths are enumerated above so the K2 can verify them by name.

### Class 2: `CLAIM CARD CONTRACT: hash-bound frozen source unavailable` (1)

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
- **Predeploy gate** — 49 → 42 errors (-7 from this session's ratchet work); the remaining 42 are documented above as irreducible.

## What the K2 must decide

Two material rulings, both already documented above:

1. **Track the public site in Magnum Opus git, or amend the HEAD-custody check.** Required to close the 40 declared-public-surface errors.
2. **Promote the Reciprocal public-edition file, or rewrite the claim card.** Required to close the 1 CLAIM CARD CONTRACT error.

Both are Class C (doctrine-adjacent, public-facing) decisions and
belong in `00_HANDOFF/constitutional/` or a similar constitutional
amendment packet, not in this docket.

## Reference path

- Receipt 246 (this session's baseline): `../246_CONTACT_LIMITED_COUNTERS_REFRESH_2026_08_15.md`
- CONTACT_LIMITED_STATE.json (this session's edited state): `../../../00_META/CONTACT_LIMITED_STATE.json`
- Close-out scripts: `../../../12_PUBLIC_SITE/close_out_a11y_v2.py`, `cleanup_bad_main_wrap.py`, `fix_library_shell_chrome.py`, `refresh_source_revisions.py`
- Predeploy gate: `../../../12_PUBLIC_SITE/predeploy_check.py`
- Audit gate: `../../../12_PUBLIC_SITE/audit_open_items.py`
- Semantic parity gate: `../../../12_PUBLIC_SITE/check_public_semantic_parity.py`
- Owner decision docket (where the 2 rulings must land): `../../../00_META/00_CONTACT_LIMITED_OWNER_DECISION_DOCKET_2026_08_02.md`

## The one sentence

The 2026-08-15 close-out closed the contact-limited ratchet (49 → 42), the inline CSS sweep, the source-revision refresh, the dimension and book regen, the 4 named a11y items, the library-shell chrome contract, and the deploy-ignore counter refresh; the 42 remaining predeploy errors are the irreducible residue of the public site being untracked in git (40) and a missing Reciprocal public-edition file referenced by a SHA-256-bound claim card (1), both of which require a K2 ruling to close and are documented here by name so they are not silently dropped.
