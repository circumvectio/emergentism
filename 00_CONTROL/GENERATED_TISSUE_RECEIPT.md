---
title: "Generated Tissue Receipt"
status: "HISTORICAL RECEIPT — not a current cleanliness certificate"
date: 2026-06-08
evidence_tier: "[B] dated cleanup and publication receipt; current checkout state separately noted"
rosetta:
  d_register: 4
  d_register_basis: "Historical receipt of 2026-06-08 cleanup; D4 (factual record, dated performed action). Source: L3 'HISTORICAL RECEIPT — not a current cleanliness certificate'."
---

# Generated Tissue Receipt

**Date:** 2026-06-08
**Action:** Deleted regenerable build/dependency output before GitHub publication

> **Scope warning (added 2026-07-23):** Every checked item below describes the
> 2026-06-08 cleanup window. It is not a standing assertion about the current
> working tree. Generated and ignored tissue has since been recreated.

## Deleted Tissue

| Path | Type | Regeneration Command |
|---|---|---|
| `12_PUBLIC_SITE/book-pwa/node_modules/` | npm dependencies | `cd 12_PUBLIC_SITE/book-pwa && npm install` |
| `12_PUBLIC_SITE/__pycache__/` | Python bytecode | Automatic on Python execution |
| `12_PUBLIC_SITE/book-pwa/tsconfig.tsbuildinfo` | TypeScript compiler cache | Regenerate with `tsc` / Next.js build |
| `**/.DS_Store` | macOS metadata | N/A (system-generated) |

## Verification at the dated cleanup boundary

- [x] As of 2026-06-08, package.json existed at `12_PUBLIC_SITE/book-pwa/package.json`
- [x] As of 2026-06-08, package-lock.json existed at `12_PUBLIC_SITE/book-pwa/package-lock.json`
- [ ] ~~pyproject.toml exists at `09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml`~~
      **UNCHECKED 2026-07-22** — verification was signed off against a path that does not
      exist. File is archived; see SOURCE_MANIFEST.md.
- [x] As of the cleanup check, no `node_modules`, `.next`, `.pytest_cache`,
      `__pycache__`, `dist`, `build`, `.turbo`, or `coverage` directories remained
      under root
- [x] As of the cleanup check, no `.tsbuildinfo` compiler cache files remained
      under root
- [x] As of the cleanup check, no nested `.git` directories remained under root

## Current-state boundary — checked 2026-07-23

- Ignored dependency/compiler tissue now exists again, including the Lean `.lake/`
  package tree, Python `__pycache__/` directories, and the historical
  `book-pwa/node_modules/` path.
- Ignored nested Git metadata exists inside the Claude worktree and Lean package
  checkouts. This does not make those directories part of the tracked publication.
- `.DS_Store` files have regenerated and remain ignored local metadata.
- `12_PUBLIC_SITE/build/` now names an intentional public site wing. It must not be
  classified or deleted merely because its directory name is `build`.
- Current cleanliness requires a new dated check; this historical receipt cannot
  supply it.
