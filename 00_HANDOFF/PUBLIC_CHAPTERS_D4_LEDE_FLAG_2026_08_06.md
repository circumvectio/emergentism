---
title: "FLAG — public chapter 4 lede carries struck content; deploy-gated"
type: flag-receipt
date: 2026-08-06
evidence_tier: "[S] the exposure inventory, verified on disk 2026-08-06 00:30"
status: "RESOLVED 2026-08-06 — the site sweep (commit 2828be05, 352 files, emblem count 476→0, product-form sweep, corrections page at /corrections/) repaired the chapter-4 lede: the receipt line is struck through with the corrected headline substituted ('The act is actual whether or not a receipt carries it. The receipt is for admissibility.'), a Repaired section carries the full strike record, and the killed-items page lists the price-list metaphor [killed] and the reflexive claim [refuted]. Verified on disk: all remaining occurrences of the struck lines sit inside strike/repair/kill-list context, which is the corpus pattern. The deploy gate remains owner-gated; this flag closes."
may_sign: false
may_authorize: false
authority_effect: none
---

# FLAG — `12_PUBLIC_SITE/4/index.html` lede

The D4 adjudication (second pass, 2026-08-06) struck three things that the
chapter-4 public lede still carries, verified on disk at 00:30:

1. **`"A record without a receipt is not actual"` — presented as "the D4
   headline"** (lede and standalone bold line, `:48`, `:52`). Not a corpus
   line: written by the composing session, contradicted by
   `44_D3_QUANTUM_STATE_REGISTER.md:64` and
   `34_D4_D5_CANONICAL_REFERENCE.md:152`. The corpus types the performed
   event as actual, not its record. Surviving form: an admissibility
   convention `[S]` — a record is not admissible in the claim register until
   a receipt carries it; the doctrine of constituted actuality is inherited
   (Searle, Ferraris, Austin, Latour, FRE 901/803(6), Muller–Feith–Fruin).
   Internal repair of `14_THE_DISTILLATION/00_THE_RUNGS_2026_08_05.md` was
   observed in progress by the authoring session at 00:30 (four sites,
   uncommitted at observation) and is left to it; this flag covers only the
   public projection.
2. **Price-metaphor lede text** — "One of the priced records is actual… one
   record has the unit price, the rest have nothing"; "D4 is the rung where
   the price-list is realised." The price-list reading was struck in the D3
   adjudication: owned five times over (de Finetti, Peres, Schrödinger 1935,
   Fuchs–Schack, Hardy) and firing `KSC-16`'s kill on non-contextuality.
   Chapters 2 and 3 already carry their repairs on disk; chapter 4's lede
   does not yet.
3. **"The state collapses, decoheres, or updates" stamped `[A/B]`** — the
   council rejected a D4 phrase precisely because read alone it names
   wavefunction collapse; ontic actualization is `[C]`, unpaid; the
   operational update is `[A]` and the interpretation is not. The tier stamp
   on the lede sentence is the worst placement of the three.

**Scope:** the generated routes `/0`–`/6` are gitignored and untracked;
nothing here is served until a deploy, and deploy is owner-gated with no
partial mode. Containment to the outside therefore holds for now; the flag
exists so the deploy decision is made with this list in hand. Chapters 2 and
3 were verified repaired on disk at the same pass; chapters 0, 1, 5, 6
carried no struck form matching the sweep patterns at check time.

**Do not:** deploy `/4` before the lede is repaired or disposed; edit the
route while the repair wave's mtimes are still moving (last observed
00:22:07 on `/3` and `/4`).

*Filed by the opencode session (qwen3.8-max-preview) during propagation of
the D4 adjudication.*
