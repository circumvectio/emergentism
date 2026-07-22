---
title: "Receipt 158 — Publication and world-contact launch"
date: 2026-07-22
status: "EXECUTED [B] — main pushed and production artifact public; custom-domain DNS, review result, and empirical result remain open"
evidence_tier: "[B] Git, Vercel, DNS, HTTP, and GitHub issue state; no empirical or doctrinal promotion"
owner: 01_EMERGENTISM
type: publication-and-world-contact-receipt
receipt: 158
parents:
  - 157_DIMENSION_FIRST_RELEASE_CANDIDATE_2026_07_22.md
  - ../../03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md
---

# Receipt 158 — Publication and world-contact launch

## Disposition

The dimension-first Emergentism release crossed four operational boundaries:

1. the release lineage was reconciled into local `main`;
2. `main` was pushed to both registered Git remotes;
3. a production Vercel artifact was built and made publicly reachable; and
4. independent review and the first-priority empirical preregistration were
   opened as public, externally answerable requests.

This is publication and test **launch**, not external review, empirical
calibration, independent replication, or integrated-worldview validation.

## Git custody

The reconciled release body was pushed through commit `0d9510c7`:

- `https://github.com/circumvectio/emergentism.git`, branch `main`;
- `https://github.com/Menexus-GmbH/emergentism.git`, branch `main`; and
- the bounded release branch
  `codex/emergentism-release-integration-2026-07-22` on both remotes.

The dirty primary checkout's unrelated untracked duplicate arrivals were not
deleted, staged, overwritten, or included in the release.

## Production artifact

Vercel project `emergentism-org` first produced deployment
`dpl_GX9JjUMAWJpn7kkmgqqHfwBMzhFK`:

`https://emergentism-q0tuz3kc5-yves-projects-c163dce1.vercel.app`

Deployment authentication was disabled for this public project. Direct HTTP
checks returned `200` for `/`, `/dimensions/`, `/3/`, and `/formal/`. The D3
page retained density-operator, momentum-distribution, POVM, Born, and
uncertainty wording. `/formal/` retained `x-robots-tag: noindex, follow`.

After the public Record gained the outside-review and GP-03 links, production
was synchronized from commit `0d9510c7` as deployment
`dpl_EMXVa5Vg1menRK6UEdPxQ5J7zQbq`:

`https://emergentism-ejhj767bk-yves-projects-c163dce1.vercel.app`

Fresh checks returned `200` for `/`, `/dimensions/`, `/3/`, `/record/`, and
`/formal/`; the Record contained both world-contact links, and the formal route
retained its no-index header. This receipt-only correction follows that source
snapshot and changes no deployed public semantics.

## Custom-domain boundary

The Vercel project owns aliases for `emergentism.org` and
`www.emergentism.org`, but the authoritative third-party DNS has not been cut
over:

```text
emergentism.org A     198.185.159.144
www.emergentism.org   CNAME ghs.googlehosted.com.
```

The apex still reaches Squarespace and redirects to the former Google Sites
surface. Vercel reports the required records for the two attached hosts as:

```text
A emergentism.org     76.76.21.21
A www.emergentism.org 76.76.21.21
```

The current nameservers are `ns-cloud-d1` through `ns-cloud-d4.googledomains.com`.
Changing records at that provider requires the external account's DNS
credentials; repository, GitHub, and Vercel authorization cannot perform that
third-party mutation. Therefore **deployment is complete; custom-domain
cutover is not**.

## Independent review gate opened

Public issue [`circumvectio/emergentism#2`](https://github.com/circumvectio/emergentism/issues/2)
requests an identifiable outside review at the released commit. It requires
conflict disclosure, file-and-line findings, reproducible defects, serious
counterexamples, repair wording, and a verdict that separates internal
coherence, calibration, and worldview adequacy.

Opening the issue is a review request. The gate closes only when a genuinely
independent reviewer publishes a method and result. Repository agents,
contributors to this release, and the founder cannot self-satisfy that gate.

## Empirical calibration gate opened

Public issue [`circumvectio/emergentism#3`](https://github.com/circumvectio/emergentism/issues/3)
launches the Empirical Program Board's first-priority socket, GP-03. It asks for
a timestamped preregistration comparing the selected product model against
minimum, harmonic, additive, and fitted CES or Cobb-Douglas rivals using
independent `Phi` and `V` measures and held-out external outcomes.

No data were collected and no preregistration was accepted by this act. A
future result may move only the tested product/aggregator claim in the tested
domain. It cannot promote the ontology, ethics, five-crossing census, or whole
Weltanschauung by association.

## Remaining world gates

- mutate third-party DNS and verify both custom hosts from independent
  resolvers;
- receive and adjudicate a genuinely independent review;
- freeze an acceptable GP-03 preregistration before inspecting held-out data;
- run the study, publish nulls and adverse results, and obtain independent
  replication before any broad calibration claim; and
- keep later socket work claim-local rather than converting component wins
  into total-system confirmation.

## Kill criteria

This receipt fails if the named Git commit is absent from either remote main,
the deployment is inaccessible, the HTTP/page-boundary checks do not reproduce,
the GitHub issues are missing or materially weaker than described, the custom
domain is represented as cut over before DNS proves it, or a review request or
preregistration request is reported as an external result.

The project has reached the road. The road has not yet returned a verdict.
