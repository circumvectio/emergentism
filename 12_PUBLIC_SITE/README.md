---
title: "Emergentism public site"
status: "ACTIVE RELEASE BOUNDARY — deployment truth requires a dated external receipt"
date: 2026-07-22
evidence_tier: "[B] repository/build state; doctrine inherits source tiers"
---

# Emergentism public site

The site is the public front door to Emergentism: a fallibilist worldview for
finite beings, made usable through Finity. A stranger should understand the
category, try one bounded practice, inspect claims at their stated prices,
follow dated corrections, and keep an exit visible throughout.

## Primary journey

Seven stable doors organize the public journey; Exit is always adjacent:

1. **Practice** — [`practice/`](practice/) carries the source-owned Finity Card,
   a local commitment/outcome receipt builder, a clearly illustrative worked
   example, and optional deeper practices.
2. **Worldview** — [`plainly/`](plainly/) introduces Emergentism in ordinary
   language. [`rosetta/`](rosetta/) leads with seven functional moves; symbolic
   and cross-tradition correspondences remain an optional, tiered appendix.
3. **Wisdom** — [`wisdom/`](wisdom/) exposes the source-bound Emergence Stack,
   the Provisional Public Wisdom Compact, honest zeroes, and candidate estate
   applications. Public remains visibility, not a truth rung.
4. **Research** — [`record/`](record/) is the trust hub. It routes to
   [`discoveries/`](discoveries/), [`lab/`](lab/), [`map/`](map/), sources,
   tests, and dated corrections without turning open work into doctrine.
5. **Library** — [`book/`](book/) is the current reader. [`read/`](read/) remains
   the wider reading index and visibly distinguishes current from frozen work.
6. **Participate** — [`contribute/`](contribute/) starts with three human acts:
   share a Finity receipt, attack a claim, or contribute bounded evidence.
7. **Exit** — [`exit/`](exit/) lets a visitor put the map down without penalty.

[`about/`](about/) is the accountability surface for authorship, category,
boundaries, and missing independent review; it remains available from page
footers without competing with the six primary doors.

The detailed spine remains available at [`dimensions/`](dimensions/) and
[`0/`](0/) through [`6/`](6/). The older [`compass/`](compass/) remains a
compressed reading, not the primary research interface. The existing
[`ecology/`](ecology/) route now carries the source-bound Emergentotype Carrier
Map: six selected carrier profiles, their non-collapse rules, and the killable
Strategic Egregoreotype test. It is neither a D-register nor a Rosetta rank.

## Homepage executive panorama

The global doors above remain stable. Inside `/`, the executive panorama now
enacts the Soul Loop as one source-bound page journey:

1. **Whole — Dasein and situated dasein.** The question and answer come first:
   one actual present, many represented possible futures, inside a whole no
   finite witness possesses.
2. **Levels — D0–D6.** The selected dependency grammar unfolds before any
   instrument is offered.
3. **Hinge — actuality and possibility.** D4 actual power and D5 represented
   possible power remain typed and causally firewalled.
4. **Emergence Stack — Signal to Wisdom.** Each promotion creates a successor
   object or receipt; nothing promotes itself. Public remains a separate light.
5. **Public Wisdom — Compact and ledger.** The present state is one Provisional
   policy, zero Supported wisdom, zero independent outcomes, and zero product
   adoptions.
6. **Instrument — Burrisphere and Rosetta.** The sphere visualizes; Rosetta
   translates; neither transfers proof. Plain functions precede mythic aliases.
7. **Practice — Finity.** One live decision can be prepared with bearers,
   means, horizons, authority, review, and Exit visible. It remains unsigned.
8. **Evidence — consequence.** Local receipts and counterexamples can revise
   the apparatus; they cannot certify the worldview.
9. **Research — revision.** Wagers, nulls, rivals, discriminators, kills, and
   survivors form the live frontier. A compact carrier-persistence disclosure
   opens the detailed `/ecology/` map without adding a new homepage stage.
10. **Exit — nonclosure.** A reader may use the instrument, reject the
   metaphysics, revise the selections, or leave.

The Golden Circle remains nested inside this sequence: the hero supplies the
**Why**, the Levels/Hinge/Instrument sequence supplies the **How**, and Finity
supplies one bounded **What**. Identity is stated early because the page must
distinguish Dasein from its situated bearer before unfolding the map; no
identity claim creates adherence.

The intended value loop is:

`fallible map → possible futures → Finity → actual move → observed outcome → revised map`

No step depends on membership, belief, payment, or delegated truth authority.

The adopted contract is
[`_PLANS/specs/2026-08-27-soul-loop-homepage-design.md`](_PLANS/specs/2026-08-27-soul-loop-homepage-design.md).
It supersedes the Cartographic Spine's six-node homepage order while retaining
its projection legend and epistemic fences.

## Source and projection boundary

- `public_semantic_parity.json` binds pages to current source owners.
- [`EMERGENTISM_DESIGN_CONSTITUTION.md`](EMERGENTISM_DESIGN_CONSTITUTION.md)
  owns the projection grammar; `emergentism-design.v2.json` exposes its route,
  semantic-role, motion, and adoption-state contract without becoming doctrine.
- `living-map.json` routes open work and contribution modes; it cannot create or
  promote doctrine.
- `render_dimension_site.py` deterministically renders `/dimensions/` and
  `/0/…/6/`. All eight rendered pages are tracked release artifacts: regenerate,
  review, and commit them together so an exact Git checkout remains deployable.
- `check_public_semantic_parity.py` rejects dimensional inversions, literal
  closure, forbidden quantum inflation, physical-cone expansion language, and
  application-authority leakage on current surfaces.
- Frozen generated-library pages remain readable as historical projections,
  carry a non-authority banner, are `noindex`, and are excluded from current
  book retrieval.
- A typed set of historical exceptions may be withheld from public routing or
  redirected to an archival notice when its old copy would create an unsafe or
  materially misleading first impression. Source custody remains in the
  repository; withholding a route is neither deletion nor evidence promotion.
- `book-pwa/` is a frozen historical source snapshot excluded from deployment;
  it is not part of the Emergentism release.

## Build and verification

```text
python3 -B build_core_shell.py
python3 -B build_core_shell.py --check
python3 -B build_wisdom_atlas.py
python3 -B build_wisdom_atlas.py --check
python3 -B build_churning.py
python3 -B build_churning.py --check
python3 -B build_fourth_churning.py
python3 -B build_fourth_churning.py --check
python3 -B build_question_atlas.py
python3 -B build_question_atlas.py --check
python3 -B render_dimension_site.py
python3 -B render_dimension_site.py --check
python3 -B build_book.py
python3 -B build_book.py --check
python3 -B refresh_reading_manifest.py
python3 -B refresh_reading_manifest.py --check
python3 -B build_withholding_boundary.py
python3 -B build_withholding_boundary.py --check
python3 -B apply_frozen_library_boundary.py
python3 -B build_atlas_index.py
python3 -B build_library_index.py
python3 -B build_library_nav.py
python3 -B build_pwa.py
python3 -B build_social_cards.py
python3 -B build_rag_index.py
python3 -B build_rag_index.py --check
python3 -B build_sw_version.py
python3 -B check_public_semantic_parity.py
python3 -B check_design_constitution.py
python3 -B predeploy_check.py
python3 ../09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py
```

`build_sw_version.py` must run last among generators. `build_pwa.py` writes the
offline page and service-worker cache constant, so it precedes
`build_social_cards.py`; the social-card builder can then cover that newly
written offline page. `build_rag_index.py` follows social-card generation so it
indexes the final visible bytes of the current reader and landing surfaces. The
final service-worker builder fingerprints every declared current page and
runtime artifact, including `living-map.json` and the current RAG index. Any
generator run after it makes the generated-artifact gate fail.
`predeploy_check.py` and the artifact checker are checks, not generators, and
therefore follow it. O9 states live in [`RELEASE_STATE.md`](RELEASE_STATE.md)
and stay separate: committed ≠ pushed ≠ promoted ≠ DNS ≠ served hash.
Federation claim-card replay (does not copy 02_SKYZAI):

```text
EMERGENTISM_PRIMARY_CHECKOUT_ROOT=/absolute/path/to/01_EMERGENTISM \
  python3 -B predeploy_check.py
```

`build_book.py` publishes exactly one current source: the claim-card-covered
One-Sitting reader. It validates the book catalog, source lifecycle, all
registered claim cards in implemented or L3-audited state, full 12-chapter
coverage, derived register, and claim graph before writing. The tier-`[D]`
Reciprocal port remains staged provenance under
`13_BOOKS/the_reciprocal/`; it is excluded from `/book/` and current RAG.

The current reader's search and “expand” controls are key-free local retrieval.
`assets/js/book-ai.js` accepts no reusable credential, stores no API key, and
contacts no model endpoint. Live generation remains unavailable until a
separate server-side authorization, privacy, and cost boundary exists.
`build_rag_index.py --check` also runs temporary negative controls proving that
a missing current source or source-hash drift fails before index generation;
`build_rag_index.py --self-test` runs those controls alone.

`refresh_reading_manifest.py` preserves the frozen June library document list
byte-for-byte at the data level and refreshes only its lifecycle declaration
and the current One-Sitting reader contract. It does not regenerate or promote
the frozen library pages.

The deploy boundary is `.vercelignore`; `vercel.json` supplies headers and 31
route redirects. `/` is not redirected: it is served by `index.html`. No
external scripts, stylesheets, fonts, or media are required. The predeploy
suite also invokes the repository's contact-limited lifecycle ratchet: every
deployable HTML artifact must have one effective class, both local ignore
matchers must agree, and `sitemap.xml` must equal the current-plus-provisional
route set exactly.

The governing execution packet is
[`_PLANS/2026_07_28_VMOSK_A_WORLDVIEW_FRONT_DOOR.md`](_PLANS/2026_07_28_VMOSK_A_WORLDVIEW_FRONT_DOOR.md).
Its dated filename is retained as provenance; its active title and boundary are
pure Emergentism and give no external project grammar authority over this lane.

## How to actually deploy

Added 2026-07-31. Until then this document ended at `predeploy_check.py`, so a
newcomer could produce release-candidate bytes and had no documented way to ship
them.

Production release is deliberately split into three invocations. The receipt
must live outside the repository so it cannot be mistaken for source custody:

```bash
cd 12_PUBLIC_SITE
release_receipt=/tmp/emergentism-vercel-release.json
./deploy_vercel.sh prepare --receipt "$release_receipt"
./deploy_vercel.sh stage --receipt "$release_receipt"
# Inspect the STAGED_VERIFIED receipt; promotion remains a separate owner act.
./deploy_vercel.sh promote --receipt "$release_receipt"
```

`prepare` requires a clean, pushed commit; runs the local gates; archives the
committed public-site tree into a non-Git temporary stage; rejects empty,
symlinked, or incomplete payloads; and records an exact path/mode/size/hash
manifest. `stage` deploys that frozen payload with `--skip-domain`, verifies the
deployment-specific URL, and leaves the public domains unchanged. `promote`
revalidates the receipt and immutable deployment, requires production still to
be the receipted predecessor, switches the domains, verifies the new deployment
identity and bytes on both branded domains, and uses Vercel rollback to restore
and re-verify the recorded predecessor if branded verification fails. A stable
project-scoped local lock prevents concurrent commands on this machine; the
predecessor is checked again immediately before the remote mutation. This is a
fail-closed predecessor guard, not a claim that Vercel exposes an atomic
cross-host compare-and-swap operation. None of the three commands pushes source
or infers publication authority.

The external receipt contains the full materialized CLI-input manifest and an
unkeyed SHA-256 checksum. The checksum detects accidental or unrehashed drift;
it is neither a signature nor authorization. Later phases independently rebuild
the deployable manifest from the clean pushed commit before trusting the stage.

- The wrapper fails closed unless `.vercel/project.json` exists **and** its two
  identities exactly match independently supplied
  `EMERGENTISM_VERCEL_PROJECT_ID_PIN` and
  `EMERGENTISM_VERCEL_ORG_ID_PIN` values. No IDs are committed or inferred.
  Before a production invocation, verify the intended project and organization
  through an independently reviewed account surface, export those two values
  in the invoking shell, and run `./deploy_vercel.sh`. Missing pins, a stale
  link, or a link to another project fails before the Vercel CLI is invoked.
  `./deploy_vercel.sh --self-test` exercises the target and release-state
  boundaries without network.
- **Never open, print, or commit `.vercel/.env.production.local`** — it is
  gitignored and may hold deploy credentials.
- The live domain is `https://emergentism.org`. A deployment that reports
  `"target": "production"` and `READY` has shipped bytes; it has not verified
  them. Only a `PROMOTED_VERIFIED` receipt records successful immutable and
  branded-domain audits, and that receipt is evidence of deployment rather than
  scientific validation.

For a non-Vercel host, `deploy.sh` is a fallback **versioned-release staging**
path, not an arbitrary-webroot rsync. It accepts only a fresh target shaped as
`user@host:/.../emergentism-static-v1/releases/YYYYMMDDTHHMMSSZ-GITSHA`,
requires the parent root to contain the exact marker
`.emergentism-static-target-v1` with value
`emergentism.org-static-target-v1`, then atomically reserves a new release
directory with remote `mkdir` before rsync. An interrupted transfer leaves a
non-live single-use partial directory; use a new release ID rather than
overwriting it. Option-looking hosts, traversal, and live-root targets are
rejected before network. `./deploy.sh --self-test` exercises those fixtures.
It never uses `--delete-excluded` and does not change a live symlink, domain, or
DNS target; cutover and live verification remain separate receipted actions.

**A green local gate does not prove what the host returns.** `vercel.json` headers
are only observable against the deployed domain, and on 2026-07-31 seven routes were
found silently indexable because nothing checked. After every deploy that touches
`vercel.json` or any route's publication status, verify against the live domain:

```bash
curl -sI https://emergentism.org/amrita/ | grep -i x-robots-tag
```

Expected: the four **declared-provisional** routes (`/amrita/ /egg/ /riemann/ /suda/`)
return **no** `X-Robots-Tag` and are indexable; every frozen-library route and
the Q4 remainder routes, including `/build/`, `/test/`, `/r/0/` through
`/r/6/`, and the four root instruments, return `noindex, follow`.
`/offline/` also returns `noindex, follow` as infrastructure.
`09_TOOLS/01_SCRIPTS/check_q4_declarations.py` guards the page-side half of this
and says plainly that it cannot check the host. Complete the post-cutover sweep
against every declared route with:

```bash
python3 audit_live_domain_against_manifest.py --strict
```

The contribution page is a static contract in this release. It accepts no
payments, API credentials, private data, or live inference jobs. Any future
compute broker would require a separate server-side security and authorization
gate; this release does not promise or expose one.

## Current release truth

This repository can produce locally checked static bytes. Deployment, the
branded domain, external red-team review, and empirical calibration are
separate gates and must be reported separately.

The Finity evaluation program is typed as three draft gates with contact
deferred: fresh-reader comprehension, conflict-declared independent review, and
a four-arm comparison against a strongest component-matched ordinary worksheet.
Exact materials, review bundle, ethics determination, analysis assets, and
freeze remain outstanding. No reader or participant has been contacted, no
external review exists, no ethics determination or preregistration exists, and
no data or result exists. The Laboratory may expose those absences; it may not
turn the drafts themselves into evidence.
