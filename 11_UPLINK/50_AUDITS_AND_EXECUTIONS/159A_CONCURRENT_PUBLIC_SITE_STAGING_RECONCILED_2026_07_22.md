---
title: "Receipt 159A — Concurrent public-site staging reconciled"
date: 2026-07-22
status: "EXECUTED [B] — staging collision disclosed, site slice audited, and release gate repaired"
evidence_tier: "[B] Git parent diff, staged-path observation, public checks, and deterministic gates; no doctrine"
owner: 01_EMERGENTISM
type: concurrent-staging-reconciliation
receipt: 159A
parents:
  - 159_UNTRACKED_ARRIVALS_RECONCILIATION_2026_07_22.md
  - 158_PUBLICATION_AND_WORLD_CONTACT_LAUNCH_2026_07_22.md
---

# Receipt 159A — Concurrent public-site staging reconciled

## The seam

Before commit `9f6b7413`, the cleanup path check showed only the Receipt-159
archive slice staged. During the commit window, a concurrent website task
staged thirteen already-present tracked changes under `12_PUBLIC_SITE/`. Git
therefore wrote both slices into one commit whose subject names only the
untracked-arrivals reconciliation.

The collision is preserved rather than hidden or history-rewritten. The
website changes did not originate in the untracked cleanup, and Receipt 159's
claim that its intended stage excluded them describes the pre-commit check,
not the final commit object.

## Website slice audited after admission

The co-committed public slice:

- makes `/` the actual front door and permanently redirects `/home/` to it;
- normalizes apex-domain sitemap and robots references;
- routes old home links back to `/`;
- excludes future Finder-style ` 2` conflicts from Vercel inputs;
- rewrites the mass-shell discovery from an inflated identity claim to the
  bounded massive-timelike factorization, with the person-level mapping kept
  interpretive and unvalidated; and
- updates the sitemap and orphan crawl to the current discovery-led funnel.

The first post-commit predeploy run found three intentional but undeclared
orphans: the retained `/home/` body behind its redirect, plus frozen no-index
`/ontology/` and `/theology/` compatibility projections. The gate now lists
those three explicit exceptions with reasons. It does not weaken general
orphan detection.

## Verification boundary

The public semantic suite, purity scan, and link check passed on the combined
tree. The full predeploy gate is rerun after this receipt and the explicit
orphan exception. Register generation occurs only after the combined tree is
stable, so it cannot describe one slice while hashing another.

This receipt does not assign authorship, claim a deployment, or convert a
concurrency race into a preferred workflow. Its purpose is to make the actual
commit boundary legible and require the accidentally co-committed surface to
earn its own checks.

## Kill criterion

This reconciliation fails if the parent diff is misdescribed, the mass-shell
page restores the inflated Einstein-equation claim, the three orphan
exceptions are not redirect/no-index compatibility surfaces, any other orphan
is ignored, the complete public gate fails, or commit history is presented as
though the two staging acts were one authored task.
