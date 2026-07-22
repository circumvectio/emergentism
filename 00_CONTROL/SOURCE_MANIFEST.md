# Source Manifest

**Root:** 01_EMERGENTISM
**Status:** Canonical source body
**Local path:** `/Users/yves/Documents/01_EMERGENTISM`

## Pre-Cleanup Snapshot

| Measure | Value |
|---|---:|
| Root size before generated-tissue deletion | 950M |
| Combined source checksum list hash | `175e461731f57fe1c3052c6d27b2476fbb28e80ca469a144bf2c324c43373f6c` |
| Non-generated files over 50MB | 0 |

## Source Categories

| Category | Directories | Count |
|---|---|---|
| Doctrine | 00_META, 01-07 | 8 |
| Support | 08_FRAMEWORK_SUPPORT, 09_TOOLS | 2 |
| Seed | 10_SEED, 11_UPLINK | 2 |
| Public | 12_PUBLIC_SITE | 1 |
| Archive | 90_ARCHIVE, 91_COMPATIBILITY | 2 |

## Regenerable Tissue Removed

- `12_PUBLIC_SITE/book-pwa/node_modules/` — npm reinstallable from package.json
- `12_PUBLIC_SITE/__pycache__/` — Python bytecode regenerable
- `.DS_Store` files — macOS metadata

## Lockfiles/Manifests Preserved

- `12_PUBLIC_SITE/book-pwa/package.json`
- `12_PUBLIC_SITE/book-pwa/package-lock.json`
- ~~`09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml`~~ — **corrected 2026-07-22:**
  not present at this path. The only non-vendored copy is
  `90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml`.
  `06_PACKAGES/` now holds route cards only.

## Authority Rule

`00_META/` and the seven doctrinal lanes remain authoritative unless a later
dated control-plane receipt moves a specific artifact.
