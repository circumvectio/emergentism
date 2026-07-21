# Public Site Boundary

**Path:** `12_PUBLIC_SITE/`

**Status:** CURRENT — pure-Emergentism release candidate, 2026-07-20

**Tier:** `[I]` public translation; `[B]` only for dated build/deploy results

The public site is a projection, not an authority. Its only deployment contract
is `12_PUBLIC_SITE/release-manifest.json`: 36 current HTML routes plus an exact
asset list. `build_release.py` constructs `.release/` from that allowlist, and
`vercel.json` serves `.release/` rather than the source tree.

The former generated public library, migrated application source, operational
receipts, staging plans, and old pages remain intact under
`12_PUBLIC_SITE/90_ARCHIVE/pure_emergentism_boundary_2026_07_20/`. They are
excluded twice—by `.vercelignore` and by the deny-by-default builder—and supply
no current doctrine or runtime dependency.

Required sequence:

1. check deterministic PWA and Atlas outputs;
2. build the exact release twice and compare hashes;
3. pass `predeploy_check.py --release .release`;
4. deploy a preview and run the strict live manifest audit;
5. promote only that audited payload;
6. verify branded-domain DNS separately.

No product or venture governance descends into this lane. Private-person
financial or legal-contract signatures do not govern AI, editorial, testing,
repository, or deployment work. Consequential acts use scoped accountable
authorization; ordinary work follows user scope, permissions, provenance,
reversibility, and proportionate tests.

GitHub state, a local pass, a Vercel build, a deployment URL, production
promotion, and branded-domain cutover are distinct facts. Never collapse them.
