---
rosetta:
  primary_level: L7
  operator: "Viṣṇu ⊙"
  tier: "Executive"
  register: "[S]"
  canonical_phrase: "Emergentism — GitHub publication receipt"
title: "GitHub Publication Receipt"
date: 2026-06-08
status: "PUBLISHED — see GitHub URL below"
evidence_tier: "[B] post-cleanup filesystem audit + [S] commit-log receipt + [B] remote HEAD confirmed equal to local HEAD"
---

# Emergentism — GitHub Publication Receipt

**Date:** 2026-06-08
**Local root:** `/Users/yves/Documents/01_EMERGENTISM`
**Target repo:** `circumvectio/emergentism`
**Visibility:** private
**Default branch:** `main`

## Publication Action

| Field | Value |
|---|---|
| GitHub URL | https://github.com/circumvectio/emergentism |
| Local HEAD (pre-receipt) | `1218026f15de14f264222f8383a53483152a56d6` |
| Final local HEAD commit (post-receipt) | `3cf2f4b8705be67ce2cf38b27eb2c770c1f298c7` |
| Remote HEAD confirmed | `3cf2f4b8705be67ce2cf38b27eb2c770c1f298c7` (matches local) |
| Branch pushed | `main` |
| Push operator | Yves (operator-triggered, prior session) |
| Push automation | none — this receipt records human-triggered publication only |

## Cleanup Counts

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Root size (excluding `.git`) | 950M | 60M | **−890M** |
| Tracked files | — | 2,405 | — |
| `node_modules/` directories | 1 | 0 | −1 |
| `__pycache__/` directories | 1 | 0 | −1 |
| `.next/` directories | 0 | 0 | 0 |
| `.pytest_cache/` directories | 0 | 0 | 0 |
| `dist/` `build/` `.turbo/` `coverage/` | 0 | 0 | 0 |
| Embedded `.git/` directories | 0 | 0 | 0 |
| Lockfiles/manifests preserved | 18 | 18 | 0 |
| Local-tissue `.DS_Store` count | many | 0 | swept via `.gitignore` |

## Commit Sequence (chronological)

| # | Commit | Message | Files |
|---|---|---|---:|
| 1 | `aebd74d` | `chore: add canonical control plane` | 5 |
| 2 | `a1166c6` | `chore: remove regenerable build tissue` | 3 |
| 3 | `1218026` | `chore: canonicalize source tree` | 2,400 |
| 4 | `10816dc` | `chore: prepare github publication` | 2 |
| 5 | `3cf2f4b` | `chore: add github publication receipt` | 1 |

The 5-step spec sequence is preserved in the commit graph (control plane → tissue removal → lineage preservation → structure canonicalization → publication prep). The lineage + canonicalization steps for this root are recorded in the `00_CONTROL/` control-plane docs (no source-touching reorg was required) and source bodies are committed under the `canonicalize source tree` step.

## Control Plane

`00_CONTROL/` contains the canonical control plane:

- `GITHUB_MAP.md` — repository shape and lane roles
- `SOURCE_MANIFEST.md` — source category table and lockfile inventory
- `GENERATED_TISSUE_RECEIPT.md` — deleted-tissue receipt with regeneration commands
- `PUBLIC_SITE_BOUNDARY.md` — public surface boundary (`12_PUBLIC_SITE/book-pwa/`)

## Preserved Inputs Verified

| Path | Status |
|---|---|
| `09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml` | OK |
| `12_PUBLIC_SITE/book-pwa/package.json` | OK |
| `12_PUBLIC_SITE/book-pwa/package-lock.json` | OK |
| `12_PUBLIC_SITE/book-pwa/prisma/` | OK |
| `12_PUBLIC_SITE/book-pwa/src/` | OK |
| `12_PUBLIC_SITE/book-pwa/public/` | OK |
| All `00_META/`, `01-07_*ology/`, `08_FRAMEWORK_SUPPORT/`, `09_TOOLS/`, `10_SEED/`, `11_UPLINK/`, `90_ARCHIVE/`, `91_COMPATIBILITY/` source | OK |

## Verification Performed

- [x] No `node_modules`, `.next`, `__pycache__`, `dist`, `build`, `.turbo`, `.pytest_cache`, or `coverage` directory remains under the root
- [x] No nested `.git` directory remains under the root
- [x] All package manifests and lockfiles verified intact
- [x] `00-12` doctrinal anatomy preserved (no reorg)
- [x] `90_ARCHIVE/` and `91_COMPATIBILITY/` clearly non-authoritative (existing `TOMBSTONE.md` and `00_CLEANUP_AUDIT_CORRECTIONS_2026_05_31.md` markers retained)
- [x] `12_PUBLIC_SITE/book-pwa/` preserved as public surface; no commingling with private doctrine in repo
- [x] Claim-boundary grep — zero capital-authority or live-protocol claims added by publication
- [x] `git status` clean

## Remaining Verification Gaps

- [x] **GitHub URL set** — https://github.com/circumvectio/emergentism · remote HEAD verified equal to local HEAD `3cf2f4b`
- [ ] **Aureus doctrine ambient coupling** — this repo contains the Emergentism canon; live Aureus / OFN proof artifacts live in the Aureus entity lane and are not duplicated here. Cross-repo invariants (Five+One constitution, η=0 fence) are referenced via relative path from `00_CONTROL/` and `AGENTS.md`; reviewer should confirm those pointer paths resolve post-push.
- [x] **`book-pwa` post-install build** — follow-through verification on 2026-06-08 passed `npm ci`, `npm test` (`193 passed`), `npm run lint`, and `npm run build`; temporary `node_modules`, `.next`, `__pycache__`, and `.tsbuildinfo` tissue was deleted afterward.
- [ ] **No CI workflows committed** — `book-pwa` does not yet have GitHub Actions. Add as a follow-up.
- [ ] **AGENTS.md / README.md internal relative links** — review post-push and update any absolute URLs (none expected — current docs are path-relative).

## Post-Baseline Verification Follow-Through

**Date:** 2026-06-08

- [x] Public PWA install/test/lint/build passed from
  `12_PUBLIC_SITE/book-pwa`.
- [x] Generated-tissue cleanup rechecked after build: no `node_modules`,
  `.next`, `.pytest_cache`, `__pycache__`, `dist`, `build`, `.turbo`,
  `coverage`, `.tsbuildinfo`, `.pyc`, `.pyo`, or `.DS_Store` residue remains.
- [x] Manifest preservation rechecked:
  `12_PUBLIC_SITE/book-pwa/package.json`,
  `12_PUBLIC_SITE/book-pwa/package-lock.json`, and
  `09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml` exist.

**Advisory:** `npm ci` for `12_PUBLIC_SITE/book-pwa` reported deprecated
transitive packages and 8 dependency audit findings (6 moderate, 1 high, 1
critical). No dependency upgrade was performed in this canonicalization pass.

## Publication Rule (carried forward)

GitHub publication is **source organization**, not a launch, deployment, doctrine upgrade, capital authority claim, or production-readiness claim. The parked/advisory language in `AGENTS.md`, `CLAUDE.md`, and `VMOSK_A.md` is preserved verbatim.

⊙ = • × ○
