---
rosetta:
  primary_level: L4
  primary_column: Axiology
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[S]"
  canonical_phrase: "K2 envelope — migrate current 12_PUBLIC_SITE/book-pwa source to 02_SKYZAI/02_AIA/app"
title: "K2 ENVELOPE — App Migration (12_PUBLIC_SITE/book-pwa → 02_SKYZAI/02_AIA/app; historical 10_PUBLIC_SITE signature preserved)"
status: "SIGNED 2026-05-31 (Yves R. Burri) — K2 GATE CLEARED. The mortal performed the binding act of authorization. Physical execution coordinates with the AIA engine lane (spec 13, mid-consolidation); book-pwa lands once 02_SKYZAI/02_AIA/app/ is ready, not into a half-built tree."
evidence_tier: "[S] structural migration plan; [B] for the verified facts (gitignore state, file inventory); [D] for the unexecuted move."
date: 2026-05-31
---

# K2 ENVELOPE — App Migration

> **The machine prepares the collapse; the human performs the binding act.** This is a staging envelope (`L4 → K2`). It describes one irreversible act and stages it for a natural-person signature. **No file has moved.** Do not execute the move from this document; execute only after the signature block below is filled.

> **2026-06-04 audit addendum.** This signed envelope preserves the original
> `10_PUBLIC_SITE/book-pwa` signature coordinates. The current source path is
> `01_EMERGENTISM/12_PUBLIC_SITE/book-pwa/` after the namespace-collision
> rename from `10_PUBLIC_SITE/` to `12_PUBLIC_SITE/`. Treat the old `10_`
> coordinates below as historical signature text, not executable shell
> coordinates. Physical migration to `02_SKYZAI/02_AIA/app/` remains blocked until the
> AIA lane has a ready destination and a final signoff receipt.

## The act (one line)

Current executable interpretation: move the frozen app source **`01_EMERGENTISM_ORG/12_PUBLIC_SITE/book-pwa/`** → **`02_AIA/app/`** only after the AIA destination and final signoff receipt exist. The signed 2026-05-31 text used `10_PUBLIC_SITE/book-pwa`; that string is preserved below as historical signature provenance, not as a shell path.

## Why (the boundary the move honours)

The prime directive of `02_SKYZAI/02_AIA` is *"the weltanschauung is content, not code."* The `book-pwa` is the **worldview-agnostic engine** (the AIA medium) — it is **AIA, not discovery**, and is currently buried inside the discovery root. The canonical target layout is the parallel-AI architecture spec **[`02_SKYZAI/02_AIA/13_APP_BOOKS_SEPARATION_2026_05_31.md`](../../02_SKYZAI/02_AIA/13_APP_BOOKS_SEPARATION_2026_05_31.md)**: engine in `02_SKYZAI/02_AIA/app/`, content in `02_SKYZAI/02_AIA/EMERGENTISM_AIA/`, bridged only by `worldview.manifest.json`. This envelope is the **source-side K2 surface**; the AIA lane owns the engine and **verifies after** (per spec 13: *"whoever reorganizes executes from this; I verify after"*).

## What moves, what doesn't ([B] verified 2026-05-31)

- **Moves (git-tracked source):** `book-pwa/` app source — Next.js + Clerk + Stripe + Prisma + `@anthropic-ai/sdk`. `git mv` preserves history.
- **Does NOT move in git (gitignored, rebuilt at destination):** `node_modules/` (~1.2 GB), `.next/` (~615 MB), `dev.db`, `.env`. **Verified:** `.env` is **not tracked** (no secrets in git); `.env`/`node_modules`/`.next` are all in `.gitignore`. The real `CLERK_SECRET_KEY` / `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` live only in the local `.env` and must be re-placed at the destination by the human — **never commit them.**

## Risks the K2 signer must weigh

1. **Live payment + auth surface.** Clerk and Stripe are wired with live-mode intent. A path change can break build/deploy, env-var resolution, and webhook URLs. Stripe webhook endpoints and any Vercel/host project settings referencing `12_PUBLIC_SITE/book-pwa` must be re-pointed.
2. **Concurrent engine work.** The AIA lane is actively consolidating `app_scaffold/` + `workflowy-clone/` + the buried `INFINITE_BOOK_PRODUCT` into `02_SKYZAI/02_AIA/app/` (spec 13). The move must **land into their target, not collide with it** — coordinate timing; do not move into a half-built `02_SKYZAI/02_AIA/app/`.
3. **Build reproducibility.** `node_modules`/`.next` rebuild at the destination (`npm install && npm run build`) — verify the build is green *before* tombstoning the old location.
4. **η = 0 / K4.** The Stripe integration must keep the server-decided price + payment-validated webhook (already hardened, commit `0e0debc0e`); the app must remain exportable (no lock-in).

## Execution plan (only after signature)

1. **ENVELOPE-1 — the move.** `git mv 01_EMERGENTISM/12_PUBLIC_SITE/book-pwa → 02_SKYZAI/02_AIA/app` (or merge into the AIA-lane's staged `02_SKYZAI/02_AIA/app/` per their direction). Existence-guarded relink of inbound references. `npm install && npm run build` at the destination — **must pass.**
2. **ENVELOPE-2 — K3 tombstone.** Leave `12_PUBLIC_SITE/00_BOOK_PWA_MOVED.md` redirecting to `02_AIA/app/` (archive-first; never silent-delete). Update `CLAUDE.md` and public-site route cards to read "moved → `02_AIA/app/`".
3. **Re-point deploy config** (Stripe webhook, host project root) and **re-place `.env` secrets** at the destination (human, out-of-band).
4. **Preserve the resolved `10_` collision** — `10_SEED` remains the sole live `10`; do not recreate `10_PUBLIC_SITE/`.
5. **AIA lane verifies** against spec 13.

## Verification gate (all must be green before ENVELOPE-2)

- [ ] `git mv` preserved history (renames, not delete+add)
- [ ] inbound links relinked; 0 regressions (existence-guarded)
- [ ] `npm run build` green at `02_SKYZAI/02_AIA/app/`
- [ ] no secret committed (`git ls-files | grep .env` empty)
- [ ] Stripe webhook + host root re-pointed
- [ ] AIA-lane sign-off (spec 13)

## K2 signature

The block below is the historical signed authorization text. Its `10_PUBLIC_SITE`
path is superseded by the 2026-06-04 audit addendum above.

```
ACT: Move 10_PUBLIC_SITE/book-pwa → 02_SKYZAI/02_AIA/app (engine/content separation, spec 13)
STATUS: SIGNED — K2 GATE CLEARED 2026-05-31

K2 (natural person): Yves R. Burri — "I sign"      date: 2026-05-31
Notes / conditions:  Authorized. Physical execution coordinates with the AIA
  lane: 02_SKYZAI/02_AIA/app/ is an empty shell mid-consolidation (app_scaffold +
  workflowy-clone per spec 13); book-pwa's relation to that consolidation is
  the AIA lane's architectural call. Land book-pwa once app/ is ready, not into
  a half-built tree. Human re-places live .env secrets at destination; build
  must verify green before the K3 tombstone.
```

> Until the AIA destination and final signoff receipt exist, the app stays where it is. The agents may route, draft, audit, and warn; they may not perform the mortal collapse.

⊙ = • × ○
