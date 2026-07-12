---
title: "118 — Ship receipt: K2 'i sign' executed — Vercel production deploy live and verified; ONE owner action owed: the DNS cutover (www.emergentism.org still serves Google Sites)"
date: 2026-07-12
status: "[E] EXECUTED on K2 ship-sign ('i sign', 2026-07-12, following receipts 112–117 all [E]). Predeploy gate PASS (all checks green, 313 pages, publication boundary honored). Deployed via Vercel CLI (--prod) as burriyves-7912 to project emergentism-org; deployment ● Ready in 8s. VERIFIED LIVE at the public project alias."
evidence_tier: "[A] the verification (HTTP 200; 43 drops served; n01-corrected body, n25, h15 confirmed live; corrected hero glyphs and register-marks present)"
verdict_extends: "receipt 113 (five moves, ship-signed) · receipt 115 (card corrections, [E]) · receipts 114/116/117 ([E])"
owner: "K2 signed; software executed and verified."
parents:
  - ./113_AMRITA_FIVE_MOVES_IMPLEMENTED_PENDING_K2_SHIP.md
  - ./115_AMRITA_CARD_CORRECTIONS_AUDIT_MANIFEST_PENDING_K2.md
---

# 118 · Ship receipt — deployed, verified, one cable left uncut

## 1. What shipped

The corrected amrita front door and full public site (313 pages), through the
project's own gates:

- **Predeploy supply-chain gate: PASS** (no external resources; hrefs resolve;
  no orphans; tier markers present; `.vercelignore` publication boundary).
- **Deploy:** Vercel CLI `--prod`, project `emergentism-org`
  (prj_RyoMG78ylqIWRSnz7URjkeniOKLH), authenticated as the owner
  (burriyves-7912). Deployment `emergentism-jwuwy61p4` ● Ready.
- **Verified live** at https://emergentism-org.vercel.app/amrita/ :
  HTTP 200 · 43 drops served · n01 carries the corrected
  conserves-vs-annihilates body · n25/h15 present · hero serves
  `Φ × V = P` (corrected glyphs) with both `[emblem · frame-register]` marks.

## 2. The one cable left uncut — OWNER ACTION OWED

**www.emergentism.org does not point at Vercel.** DNS today:
`www` → `ghs.googlehosted.com` (Google Sites serves an old page);
apex → mixed (a Squarespace-range A record among them); apex 301s to www.
The domain is NOT attached to the Vercel project (project domains list lacks
emergentism.org).

The cutover is a registrar-level act on owner infrastructure — K2's hands, not
software's:

1. In Vercel: add `emergentism.org` + `www.emergentism.org` to project
   `emergentism-org` (`vercel domains add`, or dashboard → Domains).
2. At the registrar: point `www` CNAME → `cname.vercel-dns.com` and apex A →
   `76.76.21.21` (Vercel's), replacing the Google Sites / Squarespace records.
3. Verify: `curl -I https://www.emergentism.org/amrita/` → 200 from Vercel.

Until then the canonical public URL is the Vercel alias above; the old Google
Sites page continues to answer on the .org domain.

## 3. Disposition

`[E]`. The signed act is complete and verified. The DNS cutover stands as the
single remaining step between the corrected canon-site and its own name.
