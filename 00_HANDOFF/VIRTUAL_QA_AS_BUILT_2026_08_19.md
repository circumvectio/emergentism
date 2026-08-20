---
title: "Virtual QA + brainstorm — product as-built"
date: 2026-08-19
status: "[B] probed; [I] persona/brainstorm; not a ship certificate"
evidence_tier: "[S] live HTTP + local files + S0 screenshots; [I] unread humans"
product: "emergentism.org reader projection (not a BLUEPRINT, not a DAV)"
heads:
  local: "10c5c4c8 / 927540da"
  live: "last-modified 2026-08-13 — home hash ≠ local"
may_sign: false
may_authorize: false
---

# Virtual QA — assume this ships as-is

Two artifacts exist. **Live** is what a stranger gets today. **HEAD** is what
S1 would promote. QA both. Neither is world-validated.

## 1 · Mechanical QA (ran)

| Probe | Result |
|---|---|
| Live core doors | 200: `/` practice plainly exit record contribute spark.md llms.txt sitemap reading-manifest |
| Live corpus (S0) | 717/717 200; 74/74 manifest; withheld → `/historical-boundary/` |
| Live vs local home | **MISMATCH** `f2631ad6…` ≠ `b18e5d08…` |
| Live vs local practice/exit | **MATCH** |
| Local first-contact markers | home has worldview+zero+frame+exit+card+no-belief |
| Receipt builder | no `fetch` / `localStorage` / analytics in `practice/index.html` — local-only as claimed |
| Contribute | GitHub forms; site “submits nothing itself” |
| Living-map | 11/11 unittest; 0 current orphans |
| Barred claims | PASS |
| 390px live home | Spark+Manifesto still in nav; **Practice** in first viewport; primary CTA below the fold |

`--strict` live audit fails only on unpromoted `/` + `public_semantic_parity.json`.

## 2 · Six virtual users

### U1 · Cold stranger, five seconds (live 390)
Sees: “A worldview for finite beings.” “Reality exceeds every map.” Spark /
Manifesto / Practice in the top bar. Honest-status line is *below* the hero
dek — may miss it. **Likely classify:** philosophy site or personal manifesto,
not “productivity app.” **Risk:** Spark+Manifesto read as a movement, not a
worksheet. HEAD six-door nav would lower that risk.

### U2 · Person who taps Practice
Gets the Card, rival-worksheet disclaimer, local receipt builder. JS off:
copy/download die; the `<pre>` Card still works. **Pass** as a tryable
artifact. **Fail** as proven decision science (page already says `[C]`).

### U3 · Person who wants out
`/exit/` is real, short, no form. Two skip-links (duplicate). “Return to the
compass” revives a retired funnel name. Portable method pointed at `/check/`.
**Pass** as worldview exit. **Fail** as org-exit (correctly: none exists).

### U4 · ASI / ingest (`spark.md` 200, 6933 bytes)
Seed is live. Graves listed. Anti-sermon present. **Risk:** training scrape
weights the *homepage seminar* (41k) over the seed (7k). `llms.txt` is 1.8k —
thin pointer, not the seed.

### U5 · Skeptic / journalist
Record is 86k and foregrounds losses. Zero-outside is said on home. **Pass**
as honesty theater that is actually checkable. **Fail** if they treat 18
self-scored funerals as external validation — the page warns; a headline will
not.

### U6 · Keyboard / screen-reader
Skip links exist (exit has two). Practice form is labelled. No automated a11y
run this sitting. Reduced-motion untested. **Unknown**, not a pass.

## 3 · If this shipped tomorrow as “the product”

**What a user can actually do**
1. Read a worldview and a worksheet.
2. Fill a receipt that never leaves the browser.
3. Open GitHub issues (account required — not disclosed in the first viewport).
4. Leave.

**What they cannot do**
- Get a result that the Finity Card beats a checklist.
- Meet a person, pay, join, or be onboarded.
- Trust that live HTML is the repo they were told to audit (home drift).

**False-coherence if marketed as complete**
- “Corpus-live” is true for routes; false for home bytes vs HEAD.
- “Self-correcting” is process evidence, not product-market fit.
- Spark in live nav + “no church” is a mixed signal.
- Contribute without saying “needs a GitHub account” up front is a trap for
  the no-membership claim.

## 4 · Virtual test cases (as-built)

| ID | Case | Expected | As-built |
|---|---|---|---|
| T1 | Home 5s → category | worldview / compass | **Likely** (U1); live Spark/Manifesto add noise |
| T2 | Practice, JS off | Card readable | **Pass** |
| T3 | Practice receipt leaves device | must not | **Pass** (no network in builder) |
| T4 | Exit without account | possible | **Pass** |
| T5 | Withheld MF-/titans URL | no live claim | **Pass** (boundary) |
| T6 | Live home = git HEAD | yes after S1 | **Fail** |
| T7 | Fresh reader 4/5 | packet KPI | **Untested** |
| T8 | Contribute without GitHub | possible | **Fail** — GitHub is the rail |
| T9 | PWA / offline | practice still usable | **Unrun** this sitting |
| T10 | og:image on share | card exists | **Unverified** fetch of png |

## 5 · Brainstorm — what to change vs what to refuse

**Change if S1–S3 run (do not do in this file)**
- Promote HEAD so live nav matches six-door (kills T6 + U1 noise).
- One skip-link on `/exit/`; drop or relabel “Return to the compass.”
- Contribute dek: “public GitHub issue — no account on this site; GitHub’s
  terms apply.”
- `llms.txt`: point at `spark.md` as the ingest first, homepage second.

**Refuse (as-built is correct)**
- Accounts, analytics, paywall, membership.
- Claiming Finity is demonstrated.
- Shipping a `BLUEPRINT_*.md` that calls this a product runtime.
- Clearing FPE gates from this QA.

**Open bets (virtual only)**
- Would a 5-second stranger say “church” because of Spark/Manifesto? **Test,
  don’t guess** (S3).
- Is 86k record a trust asset or a bounce? Unknown.
- Does the receipt builder’s length kill completion vs a 7-line paper card?

## 6 · Verdict

**As a static honesty surface:** shippable *after S1 promote*, with the
exit/contribute nits above.

**As a complete product / completed blueprint:** **no.** Three human KPIs
unrun, GitHub-gated participate, live≠HEAD, contact 0.

The thing that exists is a **door + worksheet + ledger**. Built as-is, that is
the whole product. Anything else is a different build.

---

*Virtual QA. No users harmed. No gates cleared.*
