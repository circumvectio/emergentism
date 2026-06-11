# Public Site Boundary

**Path:** `12_PUBLIC_SITE/` (the static site)
**Type:** Pre-generated static HTML/CSS/JS — no build step at deploy time
**Status:** CURRENT as of 2026-06-11 — staged for emergentism.org via
`github.com/Menexus-GmbH/emergentism_org` (PR #1, `migrate/real-project`);
production merge + DNS are owner-gated.

> **Correction note (2026-06-11, K3):** the prior version of this document
> declared `book-pwa/` the public-facing site. That was true for the earlier
> PWA plan and is **retired**: the public surface is now the static site at
> `12_PUBLIC_SITE/` (front door, /0–/6 dimension models, /axioms, /synthesis,
> /soul-loop, /game, the static long-scroll /book with client-side RAG, the
> generated library, /atlas). `book-pwa/` is **frozen source** pending the
> K2-signed AIA migration (`12_PUBLIC_SITE/00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md`)
> and is **excluded from the deployed output** by `.vercelignore`. The prior
> text is superseded, not erased — it remains in git history.

## What is Public

The static site in `12_PUBLIC_SITE/` — every route served after the
`.vercelignore` exclusions. The deploy boundary is enforced twice:

- `.vercelignore` keeps `book-pwa/`, `docs/`, all `*.py` / `*.sh` / `*.md`
  source-and-tooling files, and runtime state out of the served output.
- `predeploy_check.py` (the supply-chain gate) must PASS before any deploy:
  no external resource references, evidence-tier markers on doctrine pages,
  publication boundary respected.

All other directories in this repository (00–11, 90–91) are private doctrinal
material. The public repo mirror (`Menexus-GmbH/emergentism_org`, private)
carries the `12_PUBLIC_SITE/` lane only; secrets are excluded
(`book-pwa/.env` never ships; `.env.example` documents names only).

## Regeneration

The site is pre-generated; Vercel serves it as-is (`vercel.json`:
`framework: null`, `outputDirectory: "."`). Regeneration tooling, run from
`12_PUBLIC_SITE/`:

```bash
python3 -B build_book.py          # THE_LONG_SCROLL.md -> book/index.html
python3 -B build_atlas_index.py   # site tree -> atlas/site_index.json
python3 -B build_rag_index.py     # book + library + doctrine pages -> book/rag_index.json
python3 -B predeploy_check.py     # the gate — must PASS before deploy
```

The 308-page generated library is FROZEN (generator bundle absent — see the
header note in `generate_public_library.py`); fixes to those pages are
hand-patches until the bundle is restored.

## Boundary Rule (unchanged)

Do not commingle private doctrine (00–11, 90–91) with public site code.
The public site may reference doctrine but must not expose raw doctrinal files.
GitHub publication is not a doctrine upgrade, product launch, or public claim
expansion.
