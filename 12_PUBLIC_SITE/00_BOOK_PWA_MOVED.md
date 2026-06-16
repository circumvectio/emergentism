---
rosetta:
  primary_level: L6
  primary_column: K3 Tombstone
  operator: "Śiva •"
  tier: "Executive"
  regime: "Sādhu"
  register: "[S]"
  canonical_phrase: "12_PUBLIC_SITE/book-pwa/ has moved to 02_SKYZAI/03_AIA/app/"
---

# book-pwa has moved to its canonical home

**As of 2026-06-12** (per K2 signoff [`02_SKYZAI/03_AIA/AUDITS/K2_AIA_APP_MIGRATION_SIGNOFF.md`](../../02_SKYZAI/03_AIA/AUDITS/K2_AIA_APP_MIGRATION_SIGNOFF.md), 2026-06-11), the canonical AIA app lives at:

```text
02_SKYZAI/03_AIA/app/
```

This tree (`01_EMERGENTISM/12_PUBLIC_SITE/book-pwa/`) is **preserved, frozen** — per the K2 envelope's "do not archive before deploy-readiness is verified" rule. All new AIA engine work goes to `02_SKYZAI/03_AIA/` (per `02_SKYZAI/03_AIA/CLAUDE.md` + `13_APP_BOOKS_SEPARATION_2026_05_31.md`).

## Why this exists

This is the **ENVELOPE-2 K3 tombstone** per [`00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md`](00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md) §"Execution plan" step 2: "Leave `12_PUBLIC_SITE/00_BOOK_PWA_MOVED.md` redirecting to `03_AIA/app/` (archive-first; never silent-delete)."

K3 discipline: **no silent erasure.** The source tree is preserved at this path until deploy-readiness is verified at the destination. Archival/cleanup of the old `book-pwa/` is a follow-up act after deploy verification.

## Acceptance gates (already passed 2026-06-12)

| Gate | Result |
|---|---|
| `npm test -- --run` | **PASS — 193/193 tests** |
| `npm run lint` | **PASS — no errors** |
| `npm run build` | **PASS — 50 `/book/*` paths SSG-prerendered from the database** |
| `npx prisma migrate status` | **PASS — Database schema is up to date** |
| Route/render smoke (HTTP 200) | **PASS** on `http://localhost:3027/book/the-point-ylnsk` |

Full execution receipt: [`02_SKYZAI/03_AIA/AUDITS/AIA_APP_MIGRATION_RECEIPT_2026_06_12.md`](../../02_SKYZAI/03_AIA/AUDITS/AIA_APP_MIGRATION_RECEIPT_2026_06_12.md).

## Not verified in the migration (honest boundary)

- **Clerk login flow and Stripe webhook round-trip** — keys load (build + 200 OK prove env wiring) but no live login/payment receipt exists. Auth/payment remain `[C]` until a runtime receipt.
- **Deployment** — no deploy was made; the live-site cutover question (old vs new serving path) is untouched and remains owner-gated.
- **`workflowy-clone/` reconciliation** — intentionally NOT done (it was under active concurrent edit at migration time; the packet requires verified-equivalence first).

## Follow-ups (deferred to future passes)

1. Archive/tombstone the old `book-pwa/` tree in `01_EMERGENTISM/12_PUBLIC_SITE/` after **deploy-readiness verification** at the destination (K3 archive-first; this tombstone's purpose is to gate that step).
2. Re-point any deploy tooling that still assumes the old path (Stripe webhook, Vercel project root).
3. Human re-places live `.env` secrets at the destination (already done per the receipt; verify on each deploy).
4. Reconcile `workflowy-clone` behaviors into `02_SKYZAI/03_AIA/app/` once that lane cools.

## References

- [`00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md`](00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md) — the K2 envelope (SIGNED 2026-05-31)
- [`02_SKYZAI/03_AIA/AUDITS/K2_AIA_APP_MIGRATION_SIGNOFF.md`](../../02_SKYZAI/03_AIA/AUDITS/K2_AIA_APP_MIGRATION_SIGNOFF.md) — the K2 signoff (Approved 2026-06-11)
- [`02_SKYZAI/03_AIA/AUDITS/AIA_APP_MIGRATION_RECEIPT_2026_06_12.md`](../../02_SKYZAI/03_AIA/AUDITS/AIA_APP_MIGRATION_RECEIPT_2026_06_12.md) — execution receipt
- [`02_SKYZAI/03_AIA/13_APP_BOOKS_SEPARATION_2026_05_31.md`](../../02_SKYZAI/03_AIA/13_APP_BOOKS_SEPARATION_2026_05_31.md) — the engine/content separation spec
- [`book-pwa/MOVED_TO_CANONICAL.md`](book-pwa/MOVED_TO_CANONICAL.md) — the existing in-book-pwa/ redirect (K3 archive-first; both files preserved per discipline)

---

*⊙ = • × ○*
