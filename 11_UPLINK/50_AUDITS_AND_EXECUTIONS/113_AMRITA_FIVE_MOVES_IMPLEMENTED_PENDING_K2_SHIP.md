---
title: "113 — Amrita five moves implemented: three-equation hero (no arrows), six new drops, compass bridge — STAGED, pending K2 ship-sign"
date: 2026-07-12
status: "[E] K2-SHIP-SIGNED 2026-07-12 ('i sign'). Receipt 112 ([E] K2-countersigned + freeze lifted) implemented in full. All five moves applied; validator passed; all surfaces serve 200; verified against spec. SHIPPED. Routes through 01_EMERGENTISM/AGENTS.md; K2 signed."
evidence_tier: "[S] implementation (files edited, validator passed, HTTP 200); [I] the design choices (per receipt 112)"
verdict_extends: "receipt 112 (the spec, [E] K2-countersigned)"
owner: "K2 + AI co-owner"
parents:
  - ./112_AMRITA_REFINEMENT_SPEC_FIVE_MOVES_PENDING_K2.md
  - ../../12_PUBLIC_SITE/amrita/index.html
  - ../../12_PUBLIC_SITE/amrita/amrita.json
  - ../../12_PUBLIC_SITE/compass/index.html
---

# 113 · Amrita five moves — implemented, verified, staged for ship

> **Origin.** Receipt 112 was K2-countersigned ("Accept + freeze lifted")
> 2026-07-12. This receipt records the implementation: five moves applied, the
> dotted-stub ruling honored (no descent arrows), the validator passed, all
> surfaces serving 200. Awaiting K2 ship-sign to deploy.

## 1. What was implemented

### Move #0 — Three-equation hero, NO descent arrows ✓

**File:** `12_PUBLIC_SITE/amrita/index.html` (hero section)
**File:** `12_PUBLIC_SITE/amrita/amrita.css` (`.hero-stack`, `.eq-emblem`, `.tier-register`, `.eq-gloss`)

The hero now shows three equations standing side by side:
- `⊙ = • × ○` — `[emblem · frame-register, not arithmetic]` (muted/italic treatment)
- `φ · ν = 1` — `[A]` the ring that closes
- `Φ × V = P` — `[S]` a vanishing factor annihilates the whole

**No arrows between them.** The gloss line beneath reads: *"Three faces of one
structure. Whether one generates the next is a wager we have not won — shown
here as a question, not a descent."* The dotted stub (Burri Rules Rule 2) is
shown as a dotted stub, on the hero. **Verified:** zero descent-arrow entities
in the hero region.

### Move #1 — Fresh amrita (nectar) ✓

**File:** `12_PUBLIC_SITE/amrita/amrita.json`

Three new nectar drops added:
- **n22** `[S]` — The keel resolution (P=Φ×V is AND-class, not proven-product)
- **n23** `[S]` — The Open Canon Covenant (śruti frame, smṛti body)
- **n24** `[I]` — The open loop (constitutively open, completes only in the living)

### Move #2 — Fresh scars (halāhala) ✓

Three new halāhala drops added:
- **h12** — The tautology-shield ("we're tautological so we can't be wrong")
- **h13** — The keel overclaim (φ×ν sold as a proven product)
- **h14** — The K2-delegation offer (the map accepting sovereign signature)

### Move #3 — Closing screen + compass bridge ✓

**File:** `12_PUBLIC_SITE/amrita/index.html` (new `<section class="screen closing">`)
**File:** `12_PUBLIC_SITE/amrita/amrita.css` (`.closing`, `.compass-link`, `.closing-fine`)
**New file:** `12_PUBLIC_SITE/compass/index.html` (the rendered compass page)

A fifth screen after "Go deeper": *"Here is what is proven. Here is the wager.
Here is what has not been run."* → links to `../compass/` (a rendered page, not
the `.md` source). The compass page carries the needle, the four tests, the
declination, the bearings, the one-line form, and the kill criterion — all
matching `00_THE_COMPASS.md`, at `[I]`, untested, with the "one test we cannot
give ourselves" line at the close.

### Move #4 — (Declined at implementation) ✓

The optional one-sentence compass sub-line under the hero was **not added**.
The three-equation hero already carries the register-marks and the dotted-stub
gloss; a fourth element would crowd the first breath. Per receipt 112 §1
Move #4: "K2 decides." The default (omit) was taken; K2 can request it on review.

## 2. Verification — all gates passed

| Check | Result |
|---|---|
| `validate_amrita_json.py` | **OK: 38 drops (24 nectar, 14 halāhala), all sources exist** |
| All four source paths for new drops | **Exist** (verified pre-edit) |
| JSON valid (parse) | **Yes** (38 drops load) |
| Six new ids present (n22–n24, h12–h14) | **All True** |
| `GET /amrita/` | **200** |
| `GET /amrita/amrita.json` | **200** |
| `GET /amrita/amrita.css` | **200** |
| `GET /compass/` | **200** |
| Hero has three equations | **Yes** (eq-emblem, eq-frame, eq-engine) |
| Hero has NO descent arrows | **Yes** (0 arrow entities between equations; 3 total are scroll-cue + compass link + tier filter) |
| Closing screen links `../compass/` | **Yes** |
| Compass page carries kill criterion | **Yes** |
| New drops keep honest tiers (no `[C]`→`[A]`) | **Yes** (n22 `[S]`, n23 `[S]`, n24 `[I]`, h12–h14 halāhala) |
| Route/unpublished contract (validator rule) | **Passed** (all six new drops are `unpublished:true`, no decoy routes) |

## 3. Files changed

| File | Change |
|---|---|
| `12_PUBLIC_SITE/amrita/index.html` | Hero replaced (3 equations, no arrows); closing screen added |
| `12_PUBLIC_SITE/amrita/amrita.css` | Additive: `.hero-stack`, `.eq-emblem`, `.eq-gloss`, `.tier-register`, `.closing`, `.compass-link`, `.closing-fine` |
| `12_PUBLIC_SITE/amrita/amrita.json` | +6 drops (n22–n24, h12–h14); 38 total |
| `12_PUBLIC_SITE/compass/index.html` | **New file** — rendered compass page |

**No existing drop was modified.** No route was broken. The prior state is
recoverable from git (K3).

## 4. The dotted-stub ruling, honored

The defining constraint of receipt 112 was: **no descent arrows between the
three equations.** The implementation honors it. The three equations stand side
by side, each tier-and-register-marked, with the generative question shown as a
question. A reader sees three honest objects and the line *"whether one
generates the next is a wager we have not won"* — the open loop, visible at
first glance.

This is the move that separates the hero from the CTMU. Langan would have drawn
the arrows. The framework refused to, because its own canon (Burri Rules Rule 2)
says the bridge is `[CONJ]`, dotted, touching no rung.

## 5. φ-bias self-audit (this implementation's brake)

Receipt 112 §3: "if at implementation the hero feels more beautiful than honest,
pull back." Applied:

- **The hero with three equations is more beautiful than the one-equation
  version.** Acknowledged.
- **The hero with no arrows is less beautiful than the descent-ladder version.**
  Also acknowledged.
- **Net: the beauty-to-honesty ratio stays ≤ 1.** The three equations earn
  their place by each carrying an honest tier; the absence of arrows earns its
  place by honoring the dotted stub. The reader sees restraint, not closure.
  **No pull-back needed.** The spec's brake held.

## 6. Disposition

`[S]` implementation (verified, validator-passed, HTTP 200). **STAGED — PENDING
K2 SHIP-SIGN.**

On K2 "Ship": the five moves are live; receipt 113 → `[E]`; the front door now
hands the reader three honest equations and a compass on the way out. On
"Revise": adjustments per K2's call. The software implemented and verified; only
K2 signs to deploy.

> *The front door now shows three faces without pretending we derived one from
> the next, and hands the reader a compass at the exit. The beauty is in the
> restraint. Ship when K2 signs.*
