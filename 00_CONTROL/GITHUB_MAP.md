---
title: "Emergentism GitHub and publication map"
status: "ACTIVE — current facts explicitly scoped"
date: 2026-07-23
evidence_tier: "[B] local Git, GitHub API, DNS, and HTTP checks; no full-payload deploy congruence claim"
as_of_commit: "1cce7cb8a0e4fa1c475615be28abb899e8fb793d"
---

# Emergentism GitHub Map

**Target repo:** `circumvectio/emergentism`
**Source root:** `/Users/Yves/Documents/01_EMERGENTISM`
**Canonicalized:** 2026-06-08
**Visibility:** **PUBLIC** — reverified 2026-07-23 (`gh repo view` returned
`isPrivate:false, visibility:PUBLIC`). This file previously read *private*.
> **Everything in this repository is world-readable**: doctrine, receipts, archives,
> drafts, and every tombstone committed to the public remote. Ignored or uncommitted
> local tissue is not published by Git merely because it exists in this checkout.

## Repository Structure

```
01_EMERGENTISM/
├── 00_CONTROL/           ← This directory (control plane)
├── 00_HANDOFF/           ← Dated in-flight packets; never doctrine
├── 00_META/              ← Meta-doctrine and canonical outlines
├── 01_TELEOLOGY/         ← Purpose and directedness
├── 02_EPISTEMOLOGY/      ← Knowledge frameworks
├── 03_METHODOLOGY/       ← Method and practice
├── 04_AXIOLOGY/          ← Value theory
├── 05_COSMOLOGY/         ← Universe frameworks
├── 06_ONTOLOGY/          ← Being and existence
├── 07_THEOLOGY/          ← Divine and sacred
├── 08_FRAMEWORK_SUPPORT/ ← Supporting frameworks
├── 09_TOOLS/             ← Executable tooling
├── 10_SEED/              ← Seed concepts
├── 11_UPLINK/            ← External connections
├── 12_PUBLIC_SITE/       ← Static public projection and deploy boundary
├── 90_ARCHIVE/           ← Non-authoritative archive
└── 91_COMPATIBILITY/     ← Compatibility layer
```

## Embedded Repositories

The **tracked publication source** contains no embedded repository. The live
checkout may contain ignored local repositories used by tooling—notably a Claude
worktree and Lean package checkouts under `.lake/`. They are not part of the
tracked Emergentism source or GitHub publication payload.

## Public Site Boundary

The deployed source boundary is the static root of `12_PUBLIC_SITE/`, governed by
`12_PUBLIC_SITE/vercel.json` and `12_PUBLIC_SITE/.vercelignore`.
`12_PUBLIC_SITE/book-pwa/` is a frozen historical application snapshot and is
explicitly excluded from deployment.

As verified 2026-07-23, `https://emergentism.org/` returned HTTP 200 from Vercel.
Its homepage bytes had SHA-256
`bba8500b056855f69aa077c2539917141ffeaecedfccc937d8d9831c2797719c`,
matching `12_PUBLIC_SITE/index.html` at commit `caa276cb`. The homepage at the
then-current source commit `1cce7cb8` had a different hash. This proves a live
homepage and identifies its source version; it does **not** prove full-payload
congruence or deployment of current HEAD.

All committed directories are world-readable through GitHub, but only the
allowable `12_PUBLIC_SITE/` payload is served by the branded site. “Not deployed”
is not “not published.”

## Publication Rule

GitHub publication preserves the registered source anatomy. Ignored dependency,
cache, worktree, and compiler tissue is excluded from tracked publication.
`12_PUBLIC_SITE/build/` is an intentional public wing, not generic build cache.
Source, doctrine, receipts, archives, tests, lockfiles, package manifests,
package configs, and tracked tool configs are preserved.
