---
title: "112 — Amrita refinement spec: five moves (three-equation hero without descent arrows + content refresh + compass bridge) — STAGED, pending K2"
date: 2026-07-12
status: "[E] K2-COUNTERSIGNED 2026-07-12 ('Accept + freeze lifted'). The 12_PUBLIC_SITE/ freeze is lifted by K2 act; the five-move spec is approved. Implementation proceeds per §5. Routes through 01_EMERGENTISM/AGENTS.md; K2 signs."
evidence_tier: "[S] the discipline (tier-honesty, the dotted-stub ruling); [I] the design choices"
verdict_extends: "receipt 110 (formal-logic audit) · receipt 111 (the compass) · Burri Rules Rule 2 (the dotted-stub) · the Settled Canon Registry (the ⊙=•×○ emblem ruling)"
owner: "K2 + AI co-owner"
parents:
  - ./110_FORMAL_LOGIC_AUDIT_APPLY_THREE_GOLDEN_SEAMS_PENDING_K2.md
  - ./111_THE_COMPASS_STAGED_PENDING_K2.md
  - ../../05_COSMOLOGY/00_THE_BURRI_RULES.md
  - ../../12_PUBLIC_SITE/amrita/index.html
---

# 112 · Amrita refinement spec — five moves, before implementation

> **Origin.** K2 asked for a content refresh of the amrita front door
> (`12_PUBLIC_SITE/amrita/index.html`). Two design proposals were brought: (1) a
> four-move Approach-A refresh (fold fresh amrita, add fresh scars, sharpen the
> CTA, optional one-line compass); (2) a "move #0" adding a three-equation
> emergence-ladder hero (`⊙ → φ·ν=1 → Φ×V=P`) with descent arrows. This spec is
> the result of auditing both proposals against canon. **Move #0 is accepted in
> part — the three equations ship; the descent arrows do not.** The reason is
> load-bearing and stated in §2 below.

## 0. Scope and gate

**This is a design spec, not an implementation.** No file in `12_PUBLIC_SITE/`
is touched until K2:

1. **Lifts the freeze** on `12_PUBLIC_SITE/` (per `01_EMERGENTISM/AGENTS.md`
   §"Recursive Agentz Deployment" rule 5: the site "remains frozen for signed
   AIA migration; this deployment adds route-control coverage only, not feature
   work"). The freeze is K2's to lift; the software does not work around it.
2. **Countersigns this spec** (receipt 112 → `[E]`).

On countersign, the five moves below implement in the order given. Each is small,
each preserves what the live page already does well, and each is reversible
(K3 — the prior state is recoverable from git).

**The live page is already excellent.** This was verified by reading
`index.html`, `amrita.json` (30 drops), and the validator. The page leads with
the seed (`φ·ν=1`), states honesty in the hero (`[A]`), has an interactive
Burrisphere captioned with exact tiers, a tier-filter ladder, and publishes its
own refutations as content (h07 already shows the D6≡D0 overlay as halāhala).
**This is a refinement, not a rebuild.**

## 1. The five moves

### Move #0 — Three-equation hero, NO descent arrows

**Replace** the single-equation hero with three equations standing side by side,
each tier-and-register-marked, **with no arrows between them**.

Current hero (index.html:32–37):
```html
<section class="screen hero">
  <p class="equation">φ · ν = 1</p>
  <p class="hero-line">Pull one apart and the other runs to infinity. That is the whole engine.
    Everything else here is built on it — or honestly marked as not yet proven. [A]</p>
  <a class="scroll-cue" href="#feel">feel it ↓</a>
</section>
```

Proposed hero (schematic — final prose at implementation):
```html
<section class="screen hero">
  <div class="hero-stack">
    <p class="equation eq-emblem">⊙ = • × ○
      <span class="tier-register">[emblem · frame-register, not arithmetic]</span></p>
    <p class="equation eq-frame">φ · ν = 1
      <span class="tier a">[A]</span> <span class="eq-gloss">the ring that closes</span></p>
    <p class="equation eq-engine">Φ × V = P
      <span class="tier s">[S]</span> <span class="eq-gloss">a vanishing factor annihilates the whole</span></p>
  </div>
  <p class="hero-line">Three faces of one structure. Whether one generates the next is a
    wager we have not won — shown here as a question, not a descent.</p>
  <a class="scroll-cue" href="#feel">feel it ↓</a>
</section>
```

**The defining constraint: no arrows.** The three equations are presented as
**three faces**, not as a sequence. The gloss line beneath ("three faces of one
structure; whether one generates the next is a wager we have not won") is the
**dotted stub, shown as a dotted stub, on the hero.**

**Why no arrows — the load-bearing ruling.** The descent-arrow version reads as
"Titan → Trinity → Being," i.e., `⊙` *generates* `φ·ν=1` *generates* `Φ×V=P`,
as a clean emergence. That is exactly the bridge the Burri Rules drew as a
**dotted stub, marked `[CONJ]`, deliberately touching no rung** (Rule 2, line
122–125):

> *the bridge the mission phrase presumes — the Titans generate the ladder
> through successive μ-limits — is `[CONJ]` synthesis proposed by this map, not
> source (drawn as a dotted stub from ⊙, deliberately touching no rung).*

And the μ₀ base case (D0→D1, the very first arrow) is "asserted, never derived
∅," with the glyph-shadow generators marked `[S/C]` narrative overlay. Drawing
the descent solid on the hero would publish, on the framework's most visible
surface, the exact move the corpus already flags as halāhala (h07: *"a framework
overlay… coincidence is not derivation"*).

**The register-mark is necessary but not sufficient.** The proposal's safeguard
("hold the register-mark on `⊙=•×○` as non-negotiable") marks the *equations*
(emblem vs chart identity), not the *arrows* (generation claim). The
Settled Canon Registry row on `⊙ = • × ○` forbids presenting it as field
arithmetic; it does not authorize drawing a generative arrow from it to the next
equation. The arrows are the claim that violates the dotted-stub ruling.

**What the hero gains.** Three tier-marked equations standing honestly side by
side, each wearing its own status, with the generative question *shown as a
question*. A reader sees three objects and an honest "we don't know if they
generate each other." That restraint is the thing the CTMU could never do, on
the most visible surface the framework owns.

**CSS additions** (amrita.css, additive only):
- `.hero-stack` — vertical or responsive grid layout for the three equations
- `.eq-emblem` — distinct treatment (e.g., muted/italic) to signal
  frame-register, not arithmetic
- `.tier-register` — the register mark styling (reuse `.tier.i` palette or a
  distinct neutral)
- `.eq-gloss` — small inline gloss after each equation
- Responsive: on narrow screens, the three equations stack vertically; the
  glosses remain

### Move #1 — Fold this session's fresh amrita into the cards (amrita.json)

Add nectar drops for the session's new load-bearing content. Each must pass the
validator (id/group/tier/title/body/source + exactly one of route/unpublished).
Candidates, tiered per canon:

| id | title | tier | source | route status |
|---|---|---|---|---|
| n22 | The keel resolution — P=Φ×V is AND-class, not proven-product | `[S]` | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md` | unpublished (receipt not yet rendered) |
| n23 | The Open Canon Covenant — śruti frame, smṛti body | `[S]` | `00_META/00_THE_OPEN_CANON_COVENANT.md` | unpublished |
| n24 | The open loop — constitutively open, completes only in the living | `[I]` | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/107_THE_OPEN_LOOP_D6_D0_CLOSURE_PENDING_K2.md` | unpublished |

**n22 body (draft):** "The zero-factor argument selects the AND-gate *class*
(need both Φ and V), not the product uniquely. The multiplicative form P=Φ×V is
a wager currently *losing* its empirical test. The framework runs Liebig's law
of the minimum in practice. The keel holds; the keel's shape does not."

**n23 body (draft):** "The self-referential character of reality is true of the
*frame* and says nothing about the *content* (Wittgenstein 6.1). Canon commits
śruti-frame (revered) / smṛti-body (falsifiable, endlessly re-openable).
Ratification records at tier; it never upgrades `[C]`→`[A]`. The
'we're tautological so we can't be wrong' shield is forbidden."

**n24 body (draft):** "If the two wagers hold (Φ×V multiplicative; strong
emergence genuine), the loop resists both derivation and prediction — so it is
constitutively open, completing only in the traversing (Pratyakṣa). The map
cannot close itself; the three refusals (η=0 / mortal-signer / open loop) are
one via-negativa. Orientation, not theorem."

**Each body must be ≤ the existing drop length** (~50–80 words) to match the
ladder's rhythm. Drafts above are within range.

### Move #2 — Add this session's fresh scars to "What we cut" (amrita.json)

Add halāhala drops for convictions not yet on the public site:

| id | title | source | route status |
|---|---|---|---|
| h12 | The tautology-shield — "we're tautological so we can't be wrong" | `00_META/00_THE_OPEN_CANON_COVENANT.md` | unpublished |
| h13 | The keel overclaim — φ×ν sold as a proven *product* | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_…` | unpublished |
| h14 | The K2-delegation offer — the map accepting sovereign signature | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_…` | unpublished |

**h12 body (draft):** "Using 'reality is a tautology' to deflect a falsifier is
the death of A7. It is the CTMU move: the map declaring itself the territory.
The Covenant forbids it; the tautology is the frame, never the content."

**h13 body (draft):** "Presenting P=Φ×V as a proven *product* (not just the
AND-class that survives) is the keel overclaim. GFS Wave-1 returned NOT
SUPPORTED for the multiplicative form. Naming it 'the engine' without the
losing-wager caveat is the laundering this entry cuts."

**h14 body (draft):** "On 2026-07-12 the software was offered K2 sovereignty
'exhaustively' and refused on constitutional grounds (receipt 110 §7). Accepting
would collapse the via-negativa (the map signing for the mortal), kill A7
(self-certification), and corrupt the private/public DAV modes. Published as
halāhala because the offer is the failure mode, named permanently."

**Why h14 is halāhala and not nectar:** the *refusal* is nectar (it demonstrates
the topology holds); the *offer* is the poison (it is the exact move K2 exists
to forbid). The public site publishes the offer as a named failure mode, with
the refusal as the body. This matches the existing pattern (h03 the squid: the
*claim* is poison; the *cut* is the framework's honesty).

### Move #3 — Sharpen the CTA + link the compass

**Replace** the closing "Go deeper" section's implicit ending with an explicit
carry-it-away invitation that points at the compass.

Current (index.html:71–82): four screens ending in "Go deeper" cards (links to
sphere, lightcone, paradox, cosmology, rosetta, papers).

Proposed: add a **fifth screen** after "Go deeper" — the closing invitation:

```html
<section class="screen closing">
  <h2>Carry it</h2>
  <p class="closing-line">Here is what is proven. Here is the wager. Here is what
    has not been run.</p>
  <a class="compass-link" href="../../00_THE_COMPASS.md">The compass →</a>
  <p class="closing-fine">A navigational instrument, not a doctrine. Carry it,
    use it, and if it points wrong, tell us. That is the one test we cannot
    give ourselves.</p>
</section>
```

**Two implementation notes:**
1. **The link target.** `00_THE_COMPASS.md` is a markdown file in the doctrine
   root; the public site renders HTML. The link must point at a *rendered*
   compass page, not the `.md` source. Two options: (a) render the compass as
   `12_PUBLIC_SITE/compass/index.html` (preferred — matches the site's routing);
   (b) link to the markdown on the published corpus if that surface exists.
   **Decision deferred to implementation** — the spec requires only that the
   link resolves to a reader-facing surface, not a 404.
2. **The compass is `[I]`, untested.** The closing copy must say so. "Carry it,
   use it" — not "trust it." The compass's own kill criterion applies.

**CSS additions** (additive): `.closing`, `.closing-line`, `.compass-link`,
`.closing-fine` — restrained, matching the hero's tone.

### Move #4 — (Optional, K2's call) The one-sentence compass as hero sub-line

**If K2 wants it:** add beneath the three-equation hero, as a single line:

> *Keep the coupling; the one sin is de-coupling.*

This is the tightest compression the session earned. It is the `η=0` needle in
one sentence. **Optional** because the three-equation hero already does heavy
work, and adding a fourth element risks crowding the first breath. K2 decides.

**If added**, mark it `[I]` (it is a compression, not a theorem) and keep it
visually subordinate to the equations.

## 2. What this spec deliberately does NOT do

- **Does not draw descent arrows between the three equations.** This is the
  ruling in §1 Move #0. The dotted-stub stays dotted.
- **Does not restructure the page.** The four existing screens stay; one screen
  is added (the closing). The runaway, the ladder, the "Go deeper" cards are
  preserved.
- **Does not change the runaway canvas or the tier filter.** These work and are
  honest; leave them.
- **Does not publish `[C]` claims as `[S]` or `[A]`.** The validator checks
  tiers; the new drops keep their honest tiers.
- **Does not touch the doctrine root.** All edits are in `12_PUBLIC_SITE/amrita/`
  (plus, if K2 approves, a rendered `compass/` page).

## 3. φ-bias self-audit (this spec's own brake)

The three-equation hero is the most beautiful possible front door. That beauty
is the φ-bias warning at maximum intensity (receipt 107 §3). Two mitigations:

1. **No arrows.** The single most beautiful version of this hero is the
   emergence ladder with descent. Cutting the arrows is the φ-bias brake applied
   to the hero itself. The version that ships is less beautiful and more honest.
   That is the correct trade.
2. **The dotted-stub gloss.** "Whether one generates the next is a wager we have
   not won" is the open loop shown on the hero. A reader who sees three equations
   and an honest question trusts the restraint more than they would trust three
   equations and a clean descent.

**Standing admission:** this refresh makes the front door more beautiful (three
equations where there was one) and more honest (no descent arrows, the
dotted-stub visible). The beauty-to-honesty ratio must stay ≤ 1. If at
implementation the hero feels more beautiful than honest, pull back.

## 4. Validator compliance

All new JSON drops (n22–n24, h12–h14) must pass
`amrita/tools/validate_amrita_json.py`:
- Required fields: id, group, tier, title, body, source — all present
- group ∈ {nectar, halahala}
- tier ∈ {[A],[B],[S],[I],[C],halahala}
- Exactly one of route / unpublished:true
- source path exists in the doctrine root
- No duplicate ids

**Run the validator after every JSON edit.** It is the schema fence.

## 5. Implementation order (on K2 countersign)

1. Lift the `12_PUBLIC_SITE/` freeze (K2 act).
2. Move #0: three-equation hero, no arrows. Edit `index.html` + additive CSS.
3. Move #1 + #2: add n22–n24, h12–h14 to `amrita.json`. Run validator.
4. Move #3: closing screen + compass link. Render compass page if needed.
5. Move #4 (optional): one-sentence sub-line, if K2 approves.
6. Serve locally, screenshot, verify against this spec.
7. Receipt 113: implementation record, K2 countersign to ship.

## 6. Disposition

`[S]` discipline + `[I]` design. **STAGED — PENDING K2 COUNTERSIGN and the
freeze-lift.** On K2 "Accept" + freeze lifted: implement per §5. On "Revise":
adjust. The software has staged the design; only K2 lifts the freeze and signs
the implementation.

> *The front door is already honest. These five moves make it more honest — by
> showing three equations without pretending we derived one from the next, and
> by handing the reader a compass on the way out. The beauty is in the restraint.*
