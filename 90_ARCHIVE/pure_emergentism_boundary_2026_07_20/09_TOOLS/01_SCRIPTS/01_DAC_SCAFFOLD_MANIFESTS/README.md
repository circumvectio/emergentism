---
rosetta:
  primary_level: L5
  primary_column: Scaffold Manifest Architecture
  secondary:
    - level: L4
      column: Scaffold Application
      role: "document the live apply command and no-clobber execution boundary"
    - level: L6
      column: Path Provenance
      role: "destroy stale 02_ORGANISM and 05_TOOLS references as active authority"
    - level: L7
      column: DAC Genesis Boundary
      role: "keep factory-tier status distinct from born-DAC constitutional completion"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/I]"
  canonical_phrase: "DAC Scaffold Manifests"
title: "DAC Scaffold Manifests"
status: "ACTIVE — scaffold manifest front door"
evidence_tier: "[B] for live script/scaffold paths and manifest inventory; [S] for DAC-birth rule; [I] for retained-but-not-applied classification."
---

# DAC Scaffold Manifests

Per-repo manifests consumed by [`../apply_dac_scaffold.py`](../apply_dac_scaffold.py) to instantiate the canonical 17-folder DAC scaffold ([`../../../../02_SKYZAI/01_NOOSPHERE/09_REFERENCE/DAV_FACTORY/NODE_DAV/`](../../../../02_SKYZAI/01_NOOSPHERE/09_REFERENCE/DAV_FACTORY/NODE_DAV/)) into a target GitHub repo.

## Tier mapping (2026-04-23)

Two tiers of "apply the DAC template" exist in the organism:

| Tier | What it means | Applies to |
|---|---|---|
| **Factory (17 folders)** | Full canonical DAC scaffold — `00_IDENTITY` through `16_FACTORY`, plus README + CLAUDE. The repo is treated as a born (or soon-to-be-born) DAC. | Real DACs + organs |
| **Entry-spine only** | Lightweight repo-root spine: `README.md` + `00_BRIEF.md` + `CLAUDE.md` + `LANES.md` (+ optional `VMOSK_A.md`, activation plan). For repo legibility; not a DAC. | Entities, brands, products, framework spine |

The lighter entry-spine is **not** a DAC; the factory scaffold is a DAC in potentia that only counts as born after its `16_FACTORY/00_DACGENESIS_CONFIG.md` is filled and the minimum required files carry real substrate / hazard / alpha / membrane / receipts / pathology content.

## Current state (as of 2026-04-23)

| Repo | Tier | Manifest | Applied |
|---|---|---|---|
| `apu` | Factory | [`apu.json`](apu.json) | pending |
| `circle` | Factory | [`circle.json`](circle.json) | pending |
| `realityfutures` | Factory | [`realityfutures.json`](realityfutures.json) | pending |
| `skyzai-org` | Factory (meta-DAC) | [`skyzai-org.json`](skyzai-org.json) | pending |
| `skyzai-com` | Entry-spine | — | n/a (compliant) |
| `emergentism` | Entry-spine (canonical source) | — | n/a (compliant) |
| `agentz` | Entry-spine | [`agentz.json`](agentz.json) — retained for possible DAC graduation | **not applied** |
| `qntm` | Entry-spine | — | n/a (compliant) |
| `menexus` | Entry-spine | — | n/a (compliant) |
| `aureus` | Entry-spine | — | n/a (compliant) |
| `helios` | Entry-spine | — | n/a (compliant) |
| `yieldfront` | Entry-spine | — | n/a (compliant) |
| `DEX` | Factory (revised 2026-04-23 PM — scaffold populated by parallel session including 16_FACTORY/birth_manifest.json; prior classification was entry-spine product-surface) | [`DEX.json`](DEX.json) | 2026-04-24 — retroactive manifest applied (no-clobber); `_DAC_SCAFFOLD_APPLIED.md` now present in `Github/DEX/`; drift audit reports ALIGNED |

## Apply

```bash
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/apply_dac_scaffold.py \
    --manifest 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/01_DAC_SCAFFOLD_MANIFESTS/<repo>.json \
    --target   /absolute/path/to/Github/<repo>
```

[B] By default, the tool skips files that already exist at the destination (use `--overwrite` to force). Scaffold root docs (`CLAUDE.md`, `README.md`, `SCAFFOLD_FILL_GUIDE.md`) are skipped by default to avoid clobbering per-repo entry-spine content.

## Retained-but-not-applied

- `agentz.json` — agentz ended up at entry-spine tier per 2026-04-23 classification. [I] The manifest is retained so that if Agentz later graduates to full-DAC status (post-SHA-close, post-SSB-seating, post-first-SSB-certified-issuance), the scaffold can be applied without re-drafting ~25 substantive placeholders.
