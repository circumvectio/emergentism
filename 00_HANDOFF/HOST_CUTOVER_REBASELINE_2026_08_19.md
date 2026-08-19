---
title: "Host-cutover rebaseline + first-contact nav alignment"
status: "ACTIVE [B] — local repository custody; world contact unchanged"
date: 2026-08-19
evidence_tier: "[S] live-host and gate commands dated 2026-08-19; [B] local predeploy; no independent world result"
owner: "01_EMERGENTISM/12_PUBLIC_SITE"
parents:
  - LEFTOVER_DISPOSITION_2026_08_13.md
  - ../11_UPLINK/50_AUDITS_AND_EXECUTIONS/245_CONTACT_LIMITED_TRACKED_TREE_REBASELINE_2026_08_14.md
  - ../12_PUBLIC_SITE/_PLANS/2026_07_28_VMOSK_A_WORLDVIEW_FRONT_DOOR.md
  - ../06_ONTOLOGY/ruminations/00_RUMINATION_ON_EMERGENTISM_ORG_2026_08_19.md
---

# Host-cutover rebaseline — 2026-08-19

Unnumbered on purpose: a `246_` prefix would trip the contact-limited
receipt-namespace ratchet. `245` remains the last numbered baseline.

## Live host `[S]`

Measured 2026-08-19 with `curl -sI -L` and `dig +short`:

| Check | Result |
|---|---|
| `https://emergentism.org/` | 200 → `www` |
| `https://www.emergentism.org/` | 200, `server: Vercel` |
| `/spark/` `/spark.md` `/practice/` `/exit/` `/llms.txt` | 200 |
| DNS | apex A `216.198.79.1` / `64.29.17.1`; `www` CNAME `a4dd0143bb653011.vercel-dns-017.com.` |
| `last-modified` | Thu, 13 Aug 2026 19:19:23 GMT |

The 2026-08-13 leftover line “No host cutover” and VIS-00 “DNS unpaid / live
host still 404s `/spark.md`” are stale. They stay on disk with dated banners.
Cutover is not contact. `world_contact_accepted` remains **0**.

## Local predeploy `[B]`

`python3 predeploy_check.py` (Homebrew 3.11.7, tinycss2 1.5.1, markdown 3.10.2):

| Section | Result |
|---|---|
| [1]–[11], [14], [15] | PASS after this sitting's edits (HEAD-custody reds clear on commit) |
| [12] KERNEL-STATUS sourceRevision | **fixed** — `refresh_source_revisions.py` now covers `statusSourceClaims`; pin `sha256:6f464ef15a0903e481fdc1033a886fa7a899c013d39d86f1d1b7e2f660a47539` |
| [13] claim-card Reciprocal | **held** — frozen source lives in `02_SKYZAI`; checker refuses the escape without `EMERGENTISM_PRIMARY_CHECKOUT_ROOT`. Named, not harvested. |
| [16] deploy-ignore counters | **held** — stored 415/208/207 (tracked, per 245); actual 803/596/207 includes local `.vercel/output` (388 HTML). Same class 245 already named. Do not write 803 back into the tracked baseline. |

`python3.11` from `~/.local` lacks tinycss2; that is an interpreter miss, not a
site defect. Run the gate with Homebrew `python3`.

## Public hygiene this sitting

Front-door packet O3: primary nav is `Practice · Worldview · Research · Library · Participate · Exit`.

Home and `/plainly/` had Spark / Manifesto in the primary nav; other primary
pages did not. Spark and Manifesto remain in the homepage footer and
choose-your-depth body. Primary nav now matches the six-door grammar.

## What this receipt does not do

- No deploy, push, DNS change, or reviewer contact.
- No `BLUEPRINT_*.md`. The site remains a projection.
- No CONTACT_LIMITED counter rewrite.
- No claim-card path rewrite into 02_SKYZAI.

---

*The readable column is live. The world has not answered.*
