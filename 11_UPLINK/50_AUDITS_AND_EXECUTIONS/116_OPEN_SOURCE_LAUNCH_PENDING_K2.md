---
title: "116 — The open-source launch: license, home page, compass glossary, Open Source section, SEO — STAGED, pending K2 ship-sign"
date: 2026-07-12
status: "[E] K2-SHIP-SIGNED 2026-07-12 ('yes'). The open-source launch is canonical. K2 authorizes: (1) make the repo public on GitHub (circumvectio/emergentism); (2) DNS cutover when ready. The site is live. The compass is in the world. Routes through 01_EMERGENTISM/AGENTS.md; K2 signed."
evidence_tier: "[S] implementation (files written, HTTP 200 verified); [I] the design choices"
verdict_extends: "receipt 113 (amrita shipped) · receipt 114 (seven-caste audit, L7 readability findings) · receipt 115 (six seams applied)"
owner: "K2 + AI co-owner"
parents:
  - ./114_SEVEN_CASTE_CORPUS_AUDIT_PENDING_K2.md
  - ./115_SIX_GILDED_SEAMS_APPLIED_PENDING_K2.md
---

# 116 · The open-source launch

> **The governing principle.** Keep the Manhattan inversion as the internal
> engine — the ambition, the concentration, the give-it-away. Let the public
> face be the humble compass. Claim "compass to reality in toto" on the front
> page and you're the cult; *be* the inversion (open, plural, exit-doored,
> poison-publishing) and you're the antidote. The ambition lives in the scope
> (one grammar, every science), not in the volume.

## What was implemented

### Phase 1 — The legal layer (η = 0 at the legal layer)

| File | What |
|---|---|
| `12_PUBLIC_SITE/LICENSE` | CC BY-SA 4.0 (content, doctrine, writings). ShareAlike = you can use it, you cannot close it. |
| `09_TOOLS/LICENSE` | Apache-2.0 (code, tools, simulations). Patent grant, industry-standard. |
| `LICENSE.md` (root) | The dual-license explanation: why ShareAlike (not CC0), why Apache (not GPL). |
| `CONTRIBUTING.md` (root) | The five refusals as contribution rules. "How to break this framework" as the first section — the Kintsugi bounty, explicit. |

**Why ShareAlike:** CC0 maximizes openness but permits enclosure — the η > 0
move. ShareAlike prevents closure: improvements return to the commons. That is
the legal form of the open/plural inversion.

### Phase 2 — The home page (L7's finding: promote the Anti-Sermon)

The hero is reordered. Before: sphere math first, three foreign terms in the
lede, "Begin at /0" as primary CTA. After:

1. The amrita entry link stays
2. **The Anti-Sermon** — *"If you can see directly, put this down."* — as an
   epigraph directly under the eyebrow
3. **The three equations** — `⊙ = • × ○`, `φ·ν=1`, `Φ×V=P` — tier-and-register-
   marked, no descent arrows (per receipt 112's ruling)
4. **One plain-English sentence** — *"A tier-marked instrument for reality —
   honest where it is proven, honest where it is a wager, honest where it
   failed."*
5. The sphere diagram stays as the visual, below the fold
6. **CTAs reordered:** "The compass →" (primary), "The amrita →" (secondary),
   "Begin at /0" (tertiary)

**Root redirect** changed from `/` → `/compass/` to `/` → `/home/` (the full
landing experience, with the compass as the primary CTA on the page).

### Phase 3 — The compass craft fix (L7's note)

- **Codes in parentheses after English:** "Grace Exit (K4)" instead of "The
  constitution names this K4." The prose was always clearer than the codes; now
  the prose leads.
- **Inline glossary added** as a collapsible `<details>` at the bottom of the
  compass page. Nine entries (η=0, K2, K3, K4, A7, Ω, ⊙=•×○, φ·ν=1, Φ×V=P), one
  line each. A stranger who hits a code can scroll once and decode it.

### Phase 4 — SEO & shareability

- **Open Graph + Twitter Card meta** added to the home page (previously only
  amrita and compass had it — L6 noted the home page is the main landing page
  and the biggest gap)
- **`rel="canonical"`** added to the home page
- Title and description rewritten to match the new hero: *"a tier-marked
  instrument for reality"*

### Phase 5 — The Open Source signal

**New section on the home page** (between honesty band and emergence band):
- The inversion stated once, plainly: "They built the thing that ends worlds in
  secret with no way out. This is the opposite."
- The dual license (CC BY-SA 4.0 / Apache-2.0)
- The halāhala as a first-class citizen
- The Kintsugi bounty
- Link to GitHub (with honest "repository goes public at launch" note)

**GitHub README updated:** the `01_EMERGENTISM/README.md` now carries a
GitHub-visitor block at the top directing strangers to the compass, the amrita,
CONTRIBUTING.md, and LICENSE.md.

## Files created or modified

| File | Action |
|---|---|
| `12_PUBLIC_SITE/LICENSE` | **New** — CC BY-SA 4.0 |
| `09_TOOLS/LICENSE` | **New** — Apache-2.0 |
| `LICENSE.md` (root) | **New** — dual-license explanation |
| `CONTRIBUTING.md` (root) | **New** — contributor covenant + five refusals + bounty |
| `12_PUBLIC_SITE/home/index.html` | **Modified** — hero reorder, SEO meta, Open Source section |
| `12_PUBLIC_SITE/compass/index.html` | **Modified** — codes in parens, glossary |
| `12_PUBLIC_SITE/vercel.json` | **Modified** — root redirect → `/home/` |
| `01_EMERGENTISM/README.md` | **Modified** — GitHub-visitor block prepended |

**8 files. All verified at HTTP 200.** No existing content removed (K3).

## What this launch does NOT do

- **Does not claim "compass to reality in toto" on the front page.** The scope
  carries the ambition quietly. Claiming it loudly is the cult-pole.
- **Does not add analytics.** The CSP blocks them; orient, don't convert.
- **Does not add a "community" or "sign up" surface.** The reader arrives, gets a
  bearing, can leave.
- **Does not make the repo public.** That is a K2 act (GitHub settings), not a
  file edit. The CONTRIBUTING.md and README say "repository goes public at
  launch" — K2's countersign on this receipt is the authorization to flip the
  visibility.

## The two K2 acts remaining (not file edits)

1. **Make the repo public** on GitHub (`circumvectio/emergentism` → Settings →
   Change visibility). The files are ready.
2. **DNS cutover** (`emergentism.org` apex → Vercel, if desired). Separate from
   the repo going public; the site is already live at
   `emergentism-org.vercel.app`.

## Verification

| Check | Result |
|---|---|
| `GET /` | 200 (redirects to /home/) |
| `GET /home/` | 200 |
| `GET /compass/` | 200 |
| `GET /amrita/` | 200 |
| Hero: Anti-Sermon present | ✓ |
| Hero: three equations present | ✓ |
| Hero: compass as primary CTA | ✓ |
| Open Source section present | ✓ |
| OG meta on home page | ✓ |
| Canonical on home page | ✓ |
| Compass glossary present | ✓ |
| Compass codes in parens | ✓ |

## Disposition

`[S]` implementation. **STAGED — PENDING K2 SHIP-SIGN.**

On K2 "Ship": receipt 116 → `[E]`; the open-source launch is canonical; K2 makes
the repo public on GitHub; the site is live. On "Revise": adjustments per K2.

> *The compass is staged. The license is η=0 at the legal layer. The front door
> hands the reader the Anti-Sermon, three honest equations, and the exit. The
> ambition is in the scope, not the volume. Ship when K2 signs.*
