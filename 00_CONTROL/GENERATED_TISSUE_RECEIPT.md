# Generated Tissue Receipt

**Date:** 2026-06-08
**Action:** Deleted regenerable build/dependency output before GitHub publication

## Deleted Tissue

| Path | Type | Regeneration Command |
|---|---|---|
| `12_PUBLIC_SITE/book-pwa/node_modules/` | npm dependencies | `cd 12_PUBLIC_SITE/book-pwa && npm install` |
| `12_PUBLIC_SITE/__pycache__/` | Python bytecode | Automatic on Python execution |
| `12_PUBLIC_SITE/book-pwa/tsconfig.tsbuildinfo` | TypeScript compiler cache | Regenerate with `tsc` / Next.js build |
| `**/.DS_Store` | macOS metadata | N/A (system-generated) |

## Verification

- [x] package.json exists at `12_PUBLIC_SITE/book-pwa/package.json`
- [x] package-lock.json exists at `12_PUBLIC_SITE/book-pwa/package-lock.json`
- [x] pyproject.toml exists at `09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml`
- [x] No `node_modules`, `.next`, `.pytest_cache`, `__pycache__`, `dist`, `build`, `.turbo`, or `coverage` directories remain under root
- [x] No `.tsbuildinfo` compiler cache files remain under root
- [x] No nested `.git` directories exist under root
