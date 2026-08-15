# Contributing to Emergentism

> *They built the thing that ends worlds — in secret, with no way out.*
> *This is the opposite — built in the open, publishing its own poison,*
> *with the exit marked. The clearest compass we can make, and it's yours.*

## How to break this framework (the Kintsugi bounty)

**The fastest way to contribute is to find a break.**

The Emergentism framework invites adversarial review. If you find a claim that
overstates its evidence tier, a proof that doesn't hold, a paradox "dissolution"
that's actually a frame-trick, or a contradiction the corpus cannot metabolize —
**report it.** The [Kintsugi Protocol](01_EMERGENTISM/00_META/00_THE_KINTSUGI_PROTOCOL.md)
governs how breaks are handled:

- A confirmed break (adversarially verified) earns a **golden seam** `[金]` in
  the canon — a permanent, credited repair with your name as the breaker.
- The seam is stronger than the original. A repaired claim outranks an untested one.
- Enemies become unpaid quality engineers; skeptics become co-authors of the fences.

**There is no version of a successful attack that damages the corpus.** If you
break a load-bearing claim and the framework cannot repair it, that is the
framework's own kill criterion firing — and that is the most valuable
contribution you can make.

## The five refusals — as contribution rules

The framework's constitution (`5 + 1`) applies to contributors as much as to the
organism. Every PR, issue, and discussion inherits these:

| Refusal | What it means for contributors |
|---|---|
| **η = 0** (no extraction) | Don't extract value from other contributors. Credit is permanent and non-negotiable. If your work builds on someone else's, their name stays on it. |
| **K2** (mortal signer) | Only Yves R. Burri signs irreversible acts (canon changes, tier upgrades). Contributors stage; K2 disposes. No AI can sign. |
| **K3** (archive-first) | Never delete. Superseded content is tombstoned (marked and moved to `90_ARCHIVE/`), not erased. Every change is traceable. |
| **K4** (grace exit) | Contributors can leave at any time with everything. No lock-in, no obligation, no social debt. |
| **A7** (self-correction) | Every claim carries an evidence tier: `[A]` established, `[S]` structural, `[I]` interpretive, `[C]` conjecture. Never present a `[C]` as an `[A]`. |

## How to contribute

### Finding and reporting a break

1. Read the [Settled Canon Registry](01_EMERGENTISM/00_META/00_SETTLED_CANON_REGISTRY.md)
   first — many questions are already settled, and re-litigating them is the
   defect, not the ruling.
2. Open an issue with: the claim, where it lives, why it breaks, and the tier
   it *should* be at. Be specific. "This is wrong" is noise; "Paper A line 73
   writes 0·∞=1 as field arithmetic when the registry says it's an emblem" is a
   crack.
3. If the break survives review, it gets gilded. Your name enters the canon.

### Contributing code or tools

1. Code goes in `01_EMERGENTISM/09_TOOLS/` under Apache-2.0.
2. Match the existing patterns: stdlib-only Python where possible, no heavy
   dependencies, self-contained scripts that reproduce their results.
3. Every computation must report its tier honestly. A simulation result is `[B]`
   (built by us), not `[A]` (established independently).

### Contributing doctrine or writing

1. Doctrine goes in `01_EMERGENTISM/` under CC BY-SA 4.0.
2. Every claim-bearing change must state its tier. Use the frontmatter
   `register:` field and the inline `[A]/[S]/[I]/[C]` marks.
3. No tier upgrades without K2 countersign. A `[C]` committed to canon is a
   canonically-recorded conjecture, not a settled truth.

## What this project is NOT

- **Not a cult.** The Anti-Sermon — *"if you can see directly, put this down"* —
  is the first thing on the compass and cannot be revoked by any authority. If
  this framework demands your belief, it has broken.
- **Not a product.** No analytics, no conversion funnel, no "sign up to learn
  the truth." The reader arrives, gets a bearing, can test it, and can leave.
- **Not closed.** ShareAlike. You can fork it. You can build on it. You cannot
  close it.

## Recognition

Contributors are credited in the seam they produce (`[金]` credit field), in
receipts, and in the Settled Canon Registry. There is no leaderboard, no
reputation score, no gamification. Credit is permanent, specific, and honest.

---

*η = 0. Orient, don't convert. Break it if you can.*
