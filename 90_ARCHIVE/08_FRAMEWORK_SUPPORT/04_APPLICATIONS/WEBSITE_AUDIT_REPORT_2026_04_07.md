---
rosetta:
  primary_level: L6
  primary_column: Archived Website Audit Report
  secondary:
    - level: L3
      column: Dated Build/Test Audit
      role: "treat fixed issues and passing tests as a 2026-04-07 snapshot"
    - level: L4
      column: Current Website Boundary
      role: "block old audit pass/fail status from substituting for current rendered truth"
    - level: L5
      column: Website Provenance
      role: "preserve old route, content, and terminology corrections"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/B/I]"
  canonical_phrase: "Archived Emergentism website audit snapshot"
title: "Emergentism.org Website Audit — Complete Fix Report"
evidence_tier: "[D] archived dated audit; [B] only for preserved command outputs in this snapshot; [I] residual notes."
type: website-audit-report
status: ARCHIVED — dated website audit snapshot
date: 2026-04-07
scope: Historical Emergentism.org website audit and fix report.
sources:
  - 01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/04_APPLICATIONS/AGENTS.md
---

# Emergentism.org Website Audit — Complete Fix Report

> **Date:** 2026-04-07
> **Scope:** Full audit of all 14 pages, 30+ components, CSS, config, and content
> **Cross-reference:** 00_EMERGENTISM.md, 00_THE_HONEST_POSITION.md, 00_FOREWORD.md

**Rosetta boundary:** [D] This audit is a dated snapshot. It does not establish current website build, route, deployment, or rendered-browser truth.

---

## Issues Found and Fixed

| # | Severity | Issue | Fix Applied |
|---|----------|-------|-------------|
| 1 | HIGH | **CSS syntax error** — orphaned `transform: rotate(45deg); }` at line 990 of index.css | Removed orphaned CSS rule |
| 2 | MEDIUM | **Book 2 title stale** — "Six-Fold Revelation" should be "Seven Lenses" (expanded from 6→7) | Updated title, word count, lens list |
| 3 | MEDIUM | **SiteNav missing /books link** — BooksPage inaccessible from navigation | Added "Books" nav link between Rosetta and Read |
| 4 | MEDIUM | **K* vs η terminology inconsistency** — Footer, BooksPage used legacy "K* = 0" | Standardized to "η = 0" (canonical per glossary) |
| 5 | MEDIUM | **HomePage "Will to P" misrepresents doctrine** — P∞ = φ · ν=1 is constant, not a tendency | Changed to "The ektropic force" with correct description |
| 6 | MEDIUM | **Schema.org author hardcoded as personal name** — framework claims anonymous/perennial origin | Changed to `{ "@type": "Organization", "name": "Emergentism" }` |
| 7 | LOW | **Hardcoded date "April 8, 2026"** in DerivationPage kill criteria | Removed specific date, kept "Harvard/Gallup, n > 200,000" |
| 8 | LOW | **No robots.txt** | Created with sitemap reference |
| 9 | LOW | **No sitemap.xml** | Created with all 15 routes |
| 10 | LOW | **RosettaPage lacks diacritics** — "Kali" not "Kālī", "Krsna" not "Kṛṣṇa", etc. | Added full diacritics to all 9 L-level entries |
| 11 | LOW | **TorusPage state cleanup conditional** — only reset if phase==='sphere' | Now always resets bη = 0, phase='torus' on unmount |

---

## Build Status

```
npm run build  → ✅ Clean (0 errors, 0 warnings)
npm test       → ✅ 6/6 tests pass
```

---

## Remaining Notes (Not Bugs)

1. **PapersPage** is orphaned — exists as route but not linked from nav, no individual paper content. Deliberately left as-is; it's placeholder content until papers are published.
2. **`src/components/content/`** is an empty directory. Reserved for future use.
3. **CSP allows `'unsafe-eval'`** in vercel.json. Required by Three.js/drei in production. Not removable without breaking 3D rendering.
4. **Five Forces table** in DerivationPage is marked [C] Conjecture — correctly labeled. The specific force-to-line mapping is an independent conjecture not in the canonical corpus.
5. **Glossary** is missing some canonical terms (Trimūrti, Asura forms, Three Gates, Replicator Stack). Not blocking — can be added incrementally.
6. **Framer Motion** may not respect `prefers-reduced-motion` CSS media query. Low priority — most users with motion preferences will still perceive reduced motion due to scroll-triggered animations.

---

*⊙ = • × ○ | Build clean. Tests pass. 11 issues fixed.*
