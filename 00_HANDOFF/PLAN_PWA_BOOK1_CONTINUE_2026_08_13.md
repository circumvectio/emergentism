# PWA + Book I current-body — continue plan

> Superseded for *next* work by `PLAN_NEXT_MOVES_2026_08_13.md`. Keep this file as the 2026-08-13 standing lock.

> In-repo only. Not a public release. Not Amrita emerged. Not Halāhala contained.

**Goal:** Keep the means (public PWA) honest and keep Book I’s *public current-body* staged, checked, and unshipped until G10 is actually paid.

**Architecture:** `/book/` stays One-Sitting. The Manifesto current-body lives only under `13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_STAGED.md`. PWA generators own chrome/spine. A denial-aware scanner watches CURRENT surfaces. No retarget of `CURRENT_WORK_ID`. No Titans/Reciprocal ingress.

**Stack:** static `12_PUBLIC_SITE`, `build_pwa.py`, `build_book.py`, `extract_manifesto_public_current_body.py`, `scan_halahala_current.py`, unittest.

---

## Done (do not redo)

- Next book named: Manifesto public current-body (Preamble + 1–11 + 17).
- Spark on PWA spine + doors; Q4 robots unclashed; `/amrita/` product-as-score fenced.
- Extract exists, seams reseated, hostile read LIVE=0, CURRENT HTML LIVE=0.
- `check_public_semantic_parity.py` PASS; `check_q4_declarations.py` PASS.

## In-repo next (this loop)

### Task 1 — Lock the extract in unittest
Add `09_TOOLS/02_COMPILERS/test_manifesto_public_current_body.py`.
Run: `python3 -m unittest 09_TOOLS.02_COMPILERS.test_manifesto_public_current_body`
Must fail if ch12–16, RIP01, or `public_route` appear; must pass `--check`.

### Task 2 — Keep the four commands green after every edit
```
python3 -B 09_TOOLS/02_COMPILERS/extract_manifesto_public_current_body.py --check
python3 -B 09_TOOLS/01_SCRIPTS/scan_halahala_current.py
python3 -B 09_TOOLS/01_SCRIPTS/check_q4_declarations.py
python3 -B 12_PUBLIC_SITE/check_public_semantic_parity.py
```

### Task 3 — Do not do these
- Do not write the extract into `/book/` or the sitemap.
- Do not retarget `build_book.py` `CURRENT_WORK_ID`.
- Do not ship Titans / Reciprocal / Serpent.
- Do not deploy, commit, or say the Amrita sentence.
- Do not cite `16_THE_EMISSION` or Second Churning for Justice / 5+1 / η / D-ladder.

## Human / world gates (unpaid)

1. Fresh-reader tier comprehension (preregistered).
2. Independent *human* hostile review.
3. Public edition + semantic parity + predeploy + immutable artifact.
4. Operator deploy + live `audit_live_domain_against_manifest.py --strict`.
5. World contact still 0 — a green repo is not a world receipt.

## Found this pass (do not silently heal)

Private full-book assembly (`test_manifesto*.py` except our extract file) is **already stale**:
live One-Sitting / Compass hashes drifted; five `one_sitting.yaml` cards still use
legacy `owner_ids` mid-migration; `manifesto-contract.json` lags `book-manifest.json`.
That is concurrent dirty-tree debt. Do not race claim-card ownership.

Our extract tests remain the hygiene gate for the public current-body slice.

`compile_claim_cards.py --check` remains **blocked** on missing Skyzai historical
Reciprocal/Sarpasya files (`02_SKYZAI/03_AIA/...`). Those hashes are not in
this checkout. Do not invent the archive.

One command:

```
python3 -B 09_TOOLS/01_SCRIPTS/check_pwa_book1_hygiene.py
```

The loop may *continue* forever as hygiene. It may *crown* only when CURRENT stays poison-free **and** G10 is paid **and** a live host serves the bytes **and** world contact is no longer silently treated as internal cleanup. Until then: stack firewood, hold the poison, do not drink.
