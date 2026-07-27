---
title: "Public Site Boundary"
status: "ACTIVE — release identity, audit, and promotion boundary"
date: 2026-07-27
evidence_tier: "[B] repository, deployment, DNS, and HTTP facts; [I] projection boundary"
---

# Public Site Boundary

**Deploy root:** `12_PUBLIC_SITE/`

The public site is an operable projection of Emergentism, never a source of
doctrine or evidence. Source owners remain upstream. A repository state, a
local pass, an immutable Vercel deployment, production promotion, branded-domain
resolution, and empirical support are distinct facts.

## Current boundary

- `12_PUBLIC_SITE/` is linked to the Vercel project `emergentism-org`.
- `emergentism.org`, `www.emergentism.org`, and
  `emergentism-org.vercel.app` already serve a prior Vercel production release.
- The Finity founder-site tree is only a release candidate until its committed
  bytes are uploaded without moving aliases, audited at the immutable URL, and
  explicitly promoted.
- The release identity is the committed Git tree under `12_PUBLIC_SITE/`,
  filtered by `.vercelignore` and configured by `vercel.json`.
- `reading-manifest.json` enumerates the generated corpus routes;
  `public_semantic_parity.json` binds current public claims to source owners;
  `living-map.json` binds the open-work routes. None can promote doctrine.
- `book-pwa/`, source documents, local tools, plans, archives, credentials, and
  runtime state are excluded by `.vercelignore`.

## Required release sequence

1. Audit public claims against their current source owners.
2. Commit the exact candidate tree and verify the deploy boundary excludes
   source, control, credential, and runtime files.
3. Run each deterministic generator twice and compare SHA-256 manifests.
4. Validate internal links, reachability, assets, HTML, evidence tiers,
   accessibility-sensitive structure, semantic parity, source custody, and the
   deployment boundary.
5. Create a production-target Vercel artifact with aliases held back; audit the
   immutable URL against every reading-manifest route, every core route, current
   homepage markers, security headers, and selected local-versus-served hashes.
6. Promote only that audited artifact. Then verify Vercel aliases, branded-domain
   HTTP, DNS, and served hashes separately.

`git push` is repository custody, not a Vercel deployment prerequisite. A green
local gate is not a preview; an immutable deployment is not production; a
production alias is not DNS proof; a receipt is not proof of the worldview.

## Authority boundary

No product or venture governance descends into this lane. Private-person
financial or legal-contract signatures do not govern editorial, testing,
repository, or deployment work. Consequential acts use scoped accountable
authorization; ordinary work follows user scope, permissions, provenance,
reversibility, and proportionate tests.

## Historical frozen boundary — superseded, preserved

The 2026-07-21 purification pass correctly reported that *that pass* made zero
changes under `12_PUBLIC_SITE/` and claimed no release or deployment. Later
publication work changed the site and promoted a Vercel release, so its
`FROZEN` status ceased to describe current reality. The historical body is
preserved here as provenance, not as an active stop:

> The public site is a projection, not an authority. This purification
> deliberately makes zero changes under `12_PUBLIC_SITE/`; the existing source
> tree therefore remains the pre-purification site, may contain legacy
> application-era language, and is not a release candidate for the repaired
> canon. No release manifest, generated payload, preview, deployment,
> production promotion, or domain state is claimed by this branch.
>
> The site's frozen bytes supply no doctrine or evidence. Source truth remains
> in the dimension and kernel owners named by the internal-completion register.
> A later publication pass must translate from those owners, preserve every tier
> and kill criterion, and keep the site removable without changing the
> worldview.

The six-step discipline first written with that freeze remains active above.
