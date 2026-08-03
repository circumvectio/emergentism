---
title: "Emergentism Source Manifest"
status: "ACTIVE ROUTE — legacy snapshot limitations disclosed"
date: 2026-07-23
evidence_tier: "[B] filesystem and Git routing facts; legacy digest is custody-only"
---

# Source Manifest

**Root:** 01_EMERGENTISM
**Status:** Canonical source body
**Local path:** `/Users/Yves/Documents/01_EMERGENTISM`

## Historical pre-cleanup snapshot — 2026-06-08

| Measure | Value |
|---|---:|
| Root size before generated-tissue deletion | 950M |
| Legacy combined source-checksum-list hash | `175e461731f57fe1c3052c6d27b2476fbb28e80ca469a144bf2c324c43373f6c` |
| Non-generated files over 50MB | 0 |

The root-size claim is corroborated by the
[archived 2026-06-08 publication receipt](../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/00_CONTROL/GITHUB_PUBLICATION_RECEIPT_2026_06_08.md).
The checksum-list digest is preserved for custody, but the checksum list itself
was not located in the current checkout or active Git history. It is therefore
**not independently reproducible** and must not be presented as a current
integrity proof. Future source or release integrity claims must name a Git commit
and preserve the exact manifest being hashed.

## Source Categories

| Category | Directories | Count |
|---|---|---|
| Control and handoff | 00_CONTROL, 00_HANDOFF | 2 |
| Doctrine | 00_META, 01-07 | 8 |
| Support | 08_FRAMEWORK_SUPPORT, 09_TOOLS | 2 |
| Seed | 10_SEED | 1 |
| Record | 11_UPLINK | 1 |
| Public | 12_PUBLIC_SITE | 1 |
| Books | 13_BOOKS | 1 |
| Archive | 90_ARCHIVE, 91_COMPATIBILITY | 2 |

Total registered source lanes: **17**. Hidden `.claude/` content is local agent
tooling, not a registered Emergentism source lane or publication surface.

## Regenerable tissue removed at the historical cleanup boundary

- `12_PUBLIC_SITE/book-pwa/node_modules/` — npm reinstallable from package.json
- `12_PUBLIC_SITE/__pycache__/` — Python bytecode regenerable
- `.DS_Store` files — macOS metadata

These are dated cleanup facts, not current-tree invariants. Ignored local tissue
has since regenerated. `12_PUBLIC_SITE/build/` is now an intentional public wing
and is not covered by the old generic build-directory deletion rule.

## Lockfiles/Manifests Preserved

- `12_PUBLIC_SITE/book-pwa/package.json`
- `12_PUBLIC_SITE/book-pwa/package-lock.json`
- ~~`09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml`~~ — **corrected 2026-07-22:**
  not present at this path. The only non-vendored copy is
  `90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml`.
  `06_PACKAGES/` now holds route cards only.

## Authority Rule

`00_META/` and the seven doctrinal lanes remain authoritative unless a later
dated control-plane receipt moves a specific artifact. `13_BOOKS/` is a
projection-only workshop and creates no eighth owner.
