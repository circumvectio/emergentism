---
title: "Public Site Boundary"
status: "ACTIVE — current boundary plus preserved historical body"
date: 2026-07-23
evidence_tier: "[B] dated repository, DNS, and HTTP facts; [I] projection boundary"
---

# Public Site Boundary

**Path:** `12_PUBLIC_SITE/`

**Status:** The former frozen boundary is superseded. The current deployment is
live, but exact current-HEAD/full-payload congruence is not established.

> **This document's factual claims are no longer true, and it did not withdraw itself.**
> It stated that "this purification deliberately makes **zero changes** under
> `12_PUBLIC_SITE/`" and that "no release manifest, generated payload, preview,
> deployment, production promotion, or domain state is claimed by this branch."
> At correction commit `dbec3298`, exactly **360 files** had changed under
> `12_PUBLIC_SITE/` since `fbf78536`. At audit commit `1cce7cb8` on 2026-07-23,
> the count was **364**. The site was **promoted to production**, and
> **`emergentism.org` serves a Vercel payload** (verified `HTTP 200`; public DNS
> returned `64.29.17.1` and `216.198.79.1`).
>
> The freeze sentence was *true of the pass that wrote it* — that commit touched
> zero site files. It became false the moment other passes ran, and nothing
> re-scoped it. **A boundary that cannot notice its own breach is not a boundary.**
> Its six-step required sequence is retained below as an unmet standard. No
> immutable release allow-list or double-build full-payload hash comparison was
> located, while production promotion has occurred.

## Current boundary — verified 2026-07-23

- The production homepage is live and returned HTTP 200 from Vercel.
- The live homepage SHA-256 is
  `bba8500b056855f69aa077c2539917141ffeaecedfccc937d8d9831c2797719c`.
- Those bytes match `12_PUBLIC_SITE/index.html` at commit `caa276cb`, not the
  homepage at then-current source commit `1cce7cb8`.
- `12_PUBLIC_SITE/book-pwa/` is frozen historical source and excluded by
  `.vercelignore`; it is not the Emergentism deployment.
- No full served-manifest comparison, immutable release allow-list, or
  double-build payload comparison is claimed.
- Repository state, source HEAD, preview, production, DNS, and empirical evidence
  remain separate gates.

## Historical frozen-boundary body — preserved, not current

The following text records the earlier boundary. It is retained for provenance
and must not be read as a description of current production state.

The public site is a projection, not an authority. This purification deliberately
makes **zero changes** under `12_PUBLIC_SITE/`; the existing source tree therefore
remains the pre-purification site, may contain legacy application-era language,
and is **not** a release candidate for the repaired canon. No release manifest,
generated payload, preview, deployment, production promotion, or domain state is
claimed by this branch.

The site's frozen bytes supply no doctrine or evidence. Source truth remains in
the dimension and kernel owners named by the internal-completion register. A later
publication pass must translate from those owners, preserve every tier and kill
criterion, and keep the site removable without changing the worldview.

## Required sequence and current disposition

1. Audit the source against the repaired owner map — local audit receipts exist;
   their scope does not prove the live payload.
2. Define an explicit immutable release allow-list — **not located**.
3. Build the exact payload twice and compare hashes — **not located**.
4. Validate links, claims, assets, accessibility, and source-tier fidelity —
   local gates exist; they remain distinct from served-payload proof.
5. Deploy a preview and audit the served manifest — **no complete served-manifest
   receipt located**.
6. Promote only that audited payload, then verify domain state separately —
   production and DNS are live; the full-payload custody chain remains open.

No product or venture governance descends into this lane. Private-person
financial or legal-contract signatures do not govern AI, editorial, testing,
repository, or deployment work. Consequential acts use scoped accountable
authorization; ordinary work follows user scope, permissions, provenance,
reversibility, and proportionate tests.

Repository state, a local pass, a build, a preview URL, production promotion,
and branded-domain cutover are distinct facts. Never collapse them.
