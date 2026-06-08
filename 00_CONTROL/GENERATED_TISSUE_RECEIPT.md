# Emergentism Generated Tissue Receipt

**Date:** 2026-06-08
**Policy:** Regenerable build and dependency tissue may be deleted.

## Pre-Cleanup Tissue

| Path | Size | Decision |
|---|---:|---|
| `12_PUBLIC_SITE/book-pwa/node_modules` | 890M | delete; regenerate with `npm install` / `npm ci` |
| `12_PUBLIC_SITE/__pycache__` | 80K | delete; Python runtime cache |

## Preserved Inputs

- `12_PUBLIC_SITE/book-pwa/package.json`
- `12_PUBLIC_SITE/book-pwa/package-lock.json`

## Verification Target

After cleanup, no `node_modules`, `.next`, `.pytest_cache`, `__pycache__`,
`dist`, `build`, `.turbo`, or `coverage` directories should remain under this
root.

