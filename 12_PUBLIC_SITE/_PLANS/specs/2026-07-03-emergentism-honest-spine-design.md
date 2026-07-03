---
rosetta:
  primary_level: L5
  primary_column: Public-Site Narrative Architecture
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/I]"
  canonical_phrase: "The Honest Spine — Amrita front door for the Emergentism public site"
title: "Design — The Honest Spine (Amrita front door)"
status: "DESIGN — approved 2026-07-03. Awaiting spec review, then writing-plans."
evidence_tier: "[S] site-architecture decisions; [I] narrative/UX intent; [B] only for future dated deploy receipts."
---

# Design — The Honest Spine (Amrita front door)

## 1 · Goal & purpose

Build a bespoke front-door **journey** for the Emergentism public site whose *pitch is its honesty*: lead with the single `[A]`-proven result (conjugacy), make it *felt* through one interactive scene, then present the amrita's tier-honest nectar/halāhala split — the thing no rival "theory of everything" site does. It converts the skeptic by showing exactly where the framework is proven, scoped, and **wrong**.

Audience (settled): **the skeptic** as the spine, with **one awe-moment** as the hook. Not primarily seeker-experience, not recruiter.

## 2 · Scope

**In scope**
- A single new **self-contained route** `/amrita/` (hand-authored), reusing the existing dark design system.
- One interactive WebGL scene (the Burrisphere runaway) as an ES module using the already-vendored `vendor/three-0.160.0/`.
- A published content projection `amrita/amrita.json` derived from `01_EMERGENTISM/00_THE_AMRITA.md`.
- Wiring the route into the topbar nav, `sitemap.xml`, and the predeploy gate.

**Out of scope (explicit)**
- `book-pwa/` — frozen/migrated to `02_SKYZAI/03_AIA/app/`; **do not touch**.
- The corpus generator (`generate_public_library.py`) and the ~350 generated routes — **unchanged**. The spine only *links into* them.
- Full site re-sequence (Approach ②) and the standalone-instrument build (Approach ③) — deferred.
- `emergentism.org` DNS cutover and the Vercel production push — **owner-gated** (K2); this work stops at preview-ready + verified.

## 3 · Architecture

- **Static HTML + existing `assets/css/xai.css`** — same black shell, `0–6 R S A` topbar, `⊙ = • × ○` footer. Native look from day one; no new CSS framework.
- **No build step** for the page itself: hand-authored `12_PUBLIC_SITE/amrita/index.html`, one scene module `12_PUBLIC_SITE/amrita/runaway.mjs`, one data file `12_PUBLIC_SITE/amrita/amrita.json`.
- **Layering:** the generated library is the untouched reference beneath; the spine is an additive route. Promoting it to the landing later is a one-line nav change, out of scope now.
- **Files added (all under `12_PUBLIC_SITE/`):**
  - `amrita/index.html` — the four-screen scrolling journey.
  - `amrita/runaway.mjs` — the Three.js scene (imports from `../vendor/three-0.160.0/`).
  - `amrita/amrita.json` — drops: `{ id, group: nectar|halahala, tier, title, body, source }`.
  - nav/sitemap/predeploy registration (edits to existing nav include + `sitemap.xml` + `predeploy_check.py` allowlist if required).

## 4 · The journey — four screens (one scrolling page)

1. **The One True Thing** — black screen, `φ · ν = 1`, then: *"Pull one apart and the other runs to infinity. That's the whole engine. Everything else here is built on it — or honestly marked as not yet proven."*
2. **Feel It** — the interactive runaway (§5).
3. **The Honest Ladder** — the amrita rendered from `amrita.json`: **nectar** (tier-badged, color-coded) and **halāhala** (visibly *cut*). A tier filter: `[A]` / `[S]` / `what we cut`. Kill-criteria surfaced on the load-bearing drops.
4. **Go Deeper** — a card grid into live wings (Paradox, Cosmology, Rosetta, Papers), each card carrying its tier badge.

## 5 · The runaway scene (interactive heart)

- Three.js `S²`. A **draggable point** sets colatitude `θ`; live readouts of `φ = cot(θ/2)`, `ν = tan(θ/2)`, `B = sin θ`, `γ = (φ+ν)/2`.
- Toward the equator → `φ,ν→1`, `B→1` (glow). Toward a pole → one factor → **∞**, its conjugate → **0**, `B→0`, `γ` diverges; a small bar viz makes the runaway visceral.
- **Persistent honest caption:** *"The one `[A]`-proven result — pure AM-GM on the reciprocal. It does not by itself prove the equator is anyone's optimum; that is `[S]` and conditional."* Awe and honesty in the same frame.
- **Fallback:** if WebGL is unavailable, a static SVG sphere + the same live number readout (accessible; predeploy-clean).

## 6 · Content & tier visual language

- Reuse existing tier vocabulary `[A]/[B]/[S]/[I]/[C]` as color-coded badges — `[A]` brightest, dimming to `[C]`; **halāhala** gets a distinct poison treatment (struck text + muted danger accent), never styled like nectar.
- Every drop links to its corpus source (site rule: no claim above `[I]` without pointing home). `amrita.json` carries the `source` path per drop.

## 7 · Verification & deploy

- Must pass **`predeploy_check.py`** (links, tier coverage, publication boundary, chrome drift).
- **Local browser verification** (preview tools): serve the static site, drive the runaway (drag to pole → confirm `ν→∞`, `B→0` readouts), screenshot proof of interaction before "done".
- **Deploy is owner-gated:** build + preview-ready only; the Vercel production push and DNS cutover are the owner's K2 act.

## 8 · Success criteria

1. `/amrita/` renders natively in the existing dark shell, topbar + footer intact.
2. Screen 1 leads with `φ·ν=1` and the anti-grandiosity line; no claim above `[I]` is unsourced.
3. The runaway scene is interactive and correct (`ν→∞`, `φ→0`, `B→0` at a pole; all →1 at equator), with a WebGL-less fallback.
4. The ladder shows nectar tier-badged and halāhala visibly cut, filterable by tier.
5. `predeploy_check.py` passes; a local screenshot proves the interaction.

## 9 · Open questions

- Route name `/amrita/` vs `/begin/` vs `/the-one-true-thing/` — default `/amrita/` (matches the corpus doc); trivially changeable.
- Whether to also expose the ladder as a generated wing later — deferred; not needed for this build.

⊙ = • × ○
