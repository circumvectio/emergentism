---
title: "O9 release-state ledger — emergentism.org"
date: 2026-08-19
status: "ACTIVE LEDGER — six states kept separate; none is world evidence"
evidence_tier: "[S] commands dated 2026-08-19; [B] local gates; no independent review"
contract: _PLANS/2026_07_28_VMOSK_A_WORLDVIEW_FRONT_DOOR.md · O9
may_sign: false
may_authorize: false
---

# O9 — verified release states

A local green is not a deploy. A deploy is not contact.

| State | Value 2026-08-19 | How measured |
|---|---|---|
| **committed** | `bd9d80f9` (cascade) + P2 nits in flight | `git -C 01_EMERGENTISM log -1` |
| **pushed** | **no** — this sitting not pushed | no `git push` this wave |
| **immutable artifact** | local tree at that commit | not a Vercel deployment id |
| **promoted** | **unknown / not this sitting** | live `last-modified: Thu, 13 Aug 2026 19:19:23 GMT` |
| **DNS** | **yes** — Vercel | apex A `216.198.79.1`/`64.29.17.1`; `www` CNAME `a4dd0143bb653011.vercel-dns-017.com.`; `server: Vercel` |
| **served hash** | see sample below | `curl -sL` then SHA-256 |

## Served-hash sample (live, 2026-08-19)

| URL | sha256 |
|---|---|
| `https://www.emergentism.org/` | `f2631ad60d9832e5ed9d92947ec0885fddce4db8874578e19cf17b2160d7ccda` | <!-- pragma: allow-secret -- served digest -->
| `https://www.emergentism.org/practice/` | `5f0194e21accfc5085b8422e5c5cf56b225c134a49e503e64092d9224a2ad733` | <!-- pragma: allow-secret -- served digest -->
| `https://www.emergentism.org/exit/` | `a76bcdc55661483a754ab44f529d84e11053a53c4f71f6456a6350da17f413b8` | <!-- pragma: allow-secret -- served digest -->

Local `practice/` and `exit/` match live. Local `index.html` (`b18e5d08…`) **does not** match live home — six-door nav is committed, not promoted.

## Local gate (same day)

Command:

```text
EMERGENTISM_PRIMARY_CHECKOUT_ROOT=/Users/Yves/Documents/01_EMERGENTISM \
  python3 predeploy_check.py
```

| Section | Result |
|---|---|
| [1]–[12], [14], [15] | PASS |
| [13] Reciprocal | **bytes match** pin `86b59d4f…` when the env is set |
| [13] Sarpasya | **FAIL** — sibling file hash ≠ reviewed pin. Do not update the pin from the OC-13 dirty tree |
| [16] | **FAIL** — `.vercel/output` (388 HTML) vs tracked baseline 415/208/207 (245) |

Barred claims: PASS. Action visibility: primary `Practice` control is in the mobile topbar (first viewport). Human FPE KPIs: not run.

## Still not O9-complete

Push, promotion of `66c5b7d0`, Sarpasya pin review, FPE-READ freeze/run, outside outcome.

---

*Six columns. None collapsed.*
