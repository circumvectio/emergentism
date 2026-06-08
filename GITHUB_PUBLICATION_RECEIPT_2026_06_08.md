# GitHub Publication Receipt

**Date:** 2026-06-08
**Repository:** `circumvectio/emergentism`
**URL:** https://github.com/circumvectio/emergentism
**Visibility:** private
**Local root:** `/Users/yves/Documents/01_EMERGENTISM`
**Canonical source commit before receipt:** `1218026f15de14f264222f8383a53483152a56d6`
**Prior remote backup branch:** `pre-canonicalization-2026-06-08`
**Prior remote main backed up from:** `b8f2f6b28480101e57e7e163963963c379acabab`

## Cleanup Counts

- Planned generated tissue removed or verified absent: 2 directories
  - `12_PUBLIC_SITE/book-pwa/node_modules/`
  - `12_PUBLIC_SITE/__pycache__/`
- Nested embedded git repositories removed: 0
- Source/manifest artifacts preserved: 3 package/runtime manifests
- Oversized files over 95 MB: 0
- `.DS_Store` files remaining: 0

## Verification

- [x] No `node_modules`, `.next`, `.pytest_cache`, `__pycache__`, `dist`, `build`, `.turbo`, `coverage`, `.venv`, `venv`, `out`, `cache`, `.cache`, `deps`, `graphify-out`, or `nats_store` directories remain under the root.
- [x] No nested `.git` directories remain under the root.
- [x] `12_PUBLIC_SITE/book-pwa/package.json` and `package-lock.json` are preserved.
- [x] `09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml` is preserved.
- [x] Public site scripts were inspected with `npm --prefix 12_PUBLIC_SITE/book-pwa pkg get scripts`.

## Verification Gaps

- The public-site build was not run because `node_modules/` was intentionally removed and an in-place reinstall would recreate generated tissue before publication. Rebuild command: `cd 12_PUBLIC_SITE/book-pwa && npm install && npm run build`.

