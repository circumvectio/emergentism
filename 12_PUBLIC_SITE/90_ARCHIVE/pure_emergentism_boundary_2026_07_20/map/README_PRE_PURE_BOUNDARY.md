---
rosetta:
  primary_level: L4
  primary_column: Meta
  operator: "Arjuna ⚔"
  tier: "Executive"
  regime: "Kṣatriya handoff — map wing build complete"
  register: "[S] for structural claims; [B] for file-path evidence; [I] for design interpretation."
canonical_phrase: "The Map — one grammar, all sciences, honest about where it frays"
title: "map_rosetta_wing — Staging Build Receipt"
evidence_tier: "[S] for build artifacts; [B] for path verification."
---

# map_rosetta_wing — Staging Build Receipt

**Agent:** map_rosetta_wing (Rosetta L4 Kṣatriya)  
**Date:** 2026-07-14  
**Staging:** `01_EMERGENTISM/12_PUBLIC_SITE/_STAGING_COMPASS_RESTRUCTURE/map_rosetta_wing/`  
**Status:** Build complete — pending integration review

---

## I. Files Produced

| File | Size | Purpose |
|---|---|---|
| `index.html` | ~20.6 KB | Main page — the 5-column honest Rosetta table, honesty layer, cross-domain cards, kill criterion |
| `map.css` | ~6.9 KB | Wing-specific styles — table, honesty cards, role toggle, scope guard, kill criterion |
| `map.js` | ~3.4 KB | Interactivity — functional/Sanskrit/both toggle, table row hover highlighting, localStorage persistence |
| `README.md` | This file | Build receipt and integration notes |

**Total:** 4 files, ~31 KB (unminified). [B]

---

## II. Design System Compliance

- **CSS:** Links to `../../assets/css/xai.css` (the canonical design system) [B]
- **Colors:** Uses CSS variables `--bg`, `--surface`, `--text`, `--text-muted`, `--gold`, `--border`, `--instrument-*` [S]
- **Typography:** `var(--font-heading)`, `var(--font-body)`, `var(--font-mono)` [S]
- **Spacing:** `var(--space-*)`, `var(--shape-*)`, `var(--target-min)` [S]
- **No external fetches:** Self-hosted Roboto only, per xai.css gate-safe mandate [B]
- **Theme:** Inherits dark/light toggle via `../../assets/js/theme.js` [S]

---

## III. Audit Synthesis Compliance

### The 5-Column Honest Table (Audit §V)

The audit commanded: **"Create /map/ wing — Rosetta Stone as hero; completeness does the boasting"** and **"5-column honest table (not 22-column 'proof by overwhelming')"**.

| Column | Content | Evidence Tier |
|---|---|---|
| Level | L1–L7 | [S] |
| Discipline | Teleology → Theology | [S] |
| Functional Role | Firewall, Truth-Cut, Audit, Executor, Architect, Compressor, Witness | [B] |
| Operator | Kali, Kālī, Kṛṣṇa, Arjuna, Brahmā, Śiva, Viṣṇu | [B] |
| Evidence | [B] / [I] / [C] per column strength | [S] |

**Default display:** Functional roles (secular front door). Sanskrit available via toggle. [S] — addresses H8 (Sanskrit entry barrier) and H10 (caste system as cult signal).

### Honesty Layer (Audit §III — Halāhala)

- **H3 (Convergence-as-proof):** Surfaced honestly: "One mathematician's work (Suda) = 1 datum, not confirmation. The convergence is suggestive, not confirmatory." [I]
- **H4 ("Exactly seven, by necessity"):** Reframed: "seven is the filing grammar that emerged from the constraint surface." [I]
- **H8 (Sanskrit entry barrier):** Default to functional roles; Sanskrit as optional depth layer. [S]
- **H10 (Caste system as cult signal):** Functional roles (Firewall, Truth-Cut, Audit, Executor, Architect, Compressor, Witness) with Sanskrit as optional. [S]
- **H11 ("Manhattan Project" rhetoric):** The Manhattan frame lives in the build, not the copy. The page is a humble compass, not a grandiose claim. [S]

### Kill Criterion (Audit §V — Compass discipline)

Four falsification conditions for the Rosetta itself, with evidence tiers on each claim. [S]

---

## IV. Evidence Tier Discipline

Every claim in the page carries an evidence tier:

- **[S]** — Structural / routing / taxonomy
- **[B]** — Bounded / derived from [A]
- **[I]** — Interpretive / synthesis
- **[C]** — Conjectural / forward target

No [C] claim is presented as fact without caveat. [S]

---

## V. Navigation Integration

The page links to the proposed new architecture:

- `../../compass/` — The Compass (default landing) [S]
- `../../test/` — Falsifiers (proposed) [S]
- `../../halāhala/` — What We Learned (proposed) [S]
- `../../read/` — The Library (existing) [B]

Topbar includes `C` (Compass) in the number-nav, replacing the old `R` (Rosetta) as the default route. [S]

---

## VI. K2 / Governance Notes

- **No K2 act executed:** This is a staging build, not a deployment. [S]
- **No existing files modified:** All output is in `_STAGING_COMPASS_RESTRUCTURE/`. [B]
- **K3 archive-first:** If this wing supersedes `../../rosetta/index.html`, the old file should be tombstoned, not deleted. [S]
- **FCA check:** N/A — this is the Emergentism doctrine pillar, not a regulated venture. [S]

---

## VII. Integration Checklist (for parent orchestrator)

- [ ] Review `index.html` for copy accuracy and tier discipline
- [ ] Verify `map.css` has no conflicts with `xai.css` variable names
- [ ] Test `map.js` toggle functionality across browsers
- [ ] Confirm relative paths (`../../`) will resolve correctly after restructure
- [ ] Decide whether to tombstone old `../../rosetta/` or redirect
- [ ] K2 ratification of Compass as default front door (Stage 7) [K2-GATED]

---

*The Map is not the territory. The territory is not the goal. The goal is to navigate well enough to put all of them down.*

⊙ = • × ○
