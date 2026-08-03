---
title: "Public lifecycle closure — every deployable HTML artifact receives one bounded state"
status: "EXECUTION RECEIPT — pre-freeze local gates passed; post-commit replay required; no deployment"
date: 2026-08-01
evidence_tier: "[B] repository inventory, matcher replay, and local checks; [S] Q4 lifecycle selection; no publication or world-contact claim"
owner: "01_EMERGENTISM"
parents:
  - 193_FIVE_RULINGS_SIGNED_2026_07_31.md
  - 237_ACTIVE_CITATION_CUSTODY_RATCHET_2026_08_01.md
  - ../../00_META/CONTACT_LIMITED_STATE.json
  - ../../12_PUBLIC_SITE/public_semantic_parity.json
  - ../../12_PUBLIC_SITE/vercel.json
  - ../../12_PUBLIC_SITE/.vercelignore
  - ../../12_PUBLIC_SITE/predeploy_check.py
  - ../../09_TOOLS/01_SCRIPTS/check_contact_limited.py
  - ../../09_TOOLS/02_COMPILERS/test_contact_limited.py
---

# Public lifecycle closure

## Outcome

The 398-artifact public HTML universe is now exhaustively classified by its
machine owners. `404.html` is infrastructure: it is an unlinked, `noindex`
error fallback that carries no doctrine. The other thirteen formerly
unclassified artifacts remain served but are frozen `noindex, follow` pending
disposition. This executes the already-signed Q4 rule in
`193_FIVE_RULINGS_SIGNED_2026_07_31.md`; it does not promote, rewrite, remove,
publish, or deploy any page.

The two canonical machine digests will be bound before commit:

```text
active_receipt_citation_registry_canonical_sha256: 67537f466ce3fc5276b977e7dd3e69438c26a5d140f2d7fa184362dbdd61b090
contact_limited_state_canonical_sha256: 7a119146863e2fe1c359ce910710b212dbbf4bc7c2e4be971d5924e443af22ba
```

After commit this receipt is immutable. Any later baseline change requires a
new dated receipt path.

## 1 · The fourteen dispositions

- infrastructure: `404.html`;
- frozen public wings/instruments: `build/index.html`, `cascade.html`,
  `lightcone.html`, `passage.html`, `sphere.html`, and `test/index.html`;
- frozen legacy Rosetta sequence: `r/0/index.html` through
  `r/6/index.html`.

The final lifecycle totals are 40 current, four provisional, 341 frozen,
eleven withheld, two infrastructure, and zero unclassified. The universe stays
398. `/build/` and `/test/` were removed from `sitemap.xml` only after their
response-header rules existed, preserving Q4's headers-first sequencing.

No page body or Atlas source ledger was changed. Stale or historically bounded
content is evidence for freezing; it is not silently repaired by classification.

## 2 · Deployment-ignore matcher convergence

The `_archive/` rule in `.vercelignore` was already correct. Its unanchored
directory form applies to a matching directory component at any depth, so it
excludes `compass/_archive/index_2026_07_12_pre_restructure.html`. The public
predeploy helper had implemented only a root-prefix interpretation.

The helper now uses the same supported gitignore-style subset as the
contact-limited checker: ordered negation, unanchored directory components,
root-relative directory prefixes, `*`, `?`, and `**`, with unsupported
character classes rejected rather than approximated. The two independent
implementations are compared across every file present beneath
`12_PUBLIC_SITE/` on every contact-limited run. The production predeploy check
also carries positive and negative `_archive/` probes.

Local inspection of the installed Vercel CLI 53.1.1 showed its bundled
`node-ignore` 4.0.6 receiving `.vercelignore` verbatim. In a
`.vercelignore`-only replay, the bundled matcher and the contact checker both
ignored 173 of 618 present site files; the old predeploy helper ignored 172 and
missed exactly the nested Compass archive. The CLI's built-in ignore list adds
the present `.gitignore`, bringing the full local CLI count to 174. After repair
the two repository implementations have zero set difference on the declared
`.vercelignore` rules. This is a bounded local matcher observation, not a
deployment receipt.

## 3 · Lifecycle checks at the deployment boundary

The public semantic parity and barred-claim scanners now include declared
provisional pages as well as current pages. Infrastructure remains outside
claim-warrant scans. The contact-limited ratchet now refuses any nonzero
unclassified count and requires `sitemap.xml` to equal the exact 44-route set
of current plus provisional HTML artifacts. `predeploy_check.py` runs that
ratchet as its sixteenth class. A deploy wrapper can no longer pass merely
because the full repository gate was not invoked separately.

## 4 · Verification

The candidate tree immediately before this receipt was frozen passed:

- the full repository gate, including all seventeen registered Python compiler
  suites and the Lean `lake build`;
- 24 active-citation custody mutations and 70 contact-limited lifecycle,
  matcher, ancestry, and sitemap mutations;
- all sixteen public predeploy classes, including 292 wired corpus documents,
  308 generated-library pages, 71 claim cards, 384 graph edges, and the
  deterministic twelve-chapter / 3,145-word public book;
- the exact lifecycle recount of 398 public HTML artifacts at
  `40/4/341/11/2/0`, with one declared alias collision, eight raw overlaps,
  and zero matcher drift;
- the generated register check at 3,423 files and 794 folders, 2,486 resolved
  local Markdown links with zero broken, and the 921-active-file purity scan.

The commit-bound handoff still requires `git diff --check`, the staged-secret
scan, and an immediate post-commit replay of the active-citation,
contact-limited, and generated-register custody checks. Those post-freeze
results are reported by the committing handoff; they cannot be written back
into this immutable receipt.

## Boundaries

This receipt records local repository state only. It performs no push, merge,
deployment, publication, DNS change, email, reviewer contact, legal signature,
contract, money movement, or external-system mutation. The two owner-held
debts, `OWNER_GATE_HELD_PUBLIC_DOCS` and `OWNER_GATE_OPEN_TOPOLOGY`, and the
world-contact state remain open and unchanged.

## Kill criterion

This closure fails if any deployable HTML artifact lacks exactly one effective
lifecycle class, a frozen route remains advertised in the sitemap, the two
ignore matchers disagree, a provisional page escapes prohibition scans, a
deploy precheck can skip the lifecycle ratchet, an old digest receipt is
rewritten, or a local pass is described as deployment or world evidence.

---

*Classification closes ambiguity; it does not confer warrant.*
