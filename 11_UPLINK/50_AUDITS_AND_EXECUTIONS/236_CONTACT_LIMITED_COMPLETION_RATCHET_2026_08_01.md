---
title: "Contact-limited completion ratchet — exact internal remainder becomes state-bound"
status: "PASS-WITH-DEBT — state-bound baseline and exact staged verification pass; owner-held and world-contact gates remain open"
date: 2026-08-01
evidence_tier: "[B] measured repository counters and executed local checks; [S] counter and transition contracts; no world-contact claim"
owner: "01_EMERGENTISM"
parents:
  - 235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md
  - ../../00_META/00_CONTACT_LIMITED_COMPLETION_ROADMAP_2026_08_01.md
  - ../../00_META/CONTACT_LIMITED_STATE.json
  - ../../09_TOOLS/01_SCRIPTS/check_contact_limited.py
  - ../../09_TOOLS/02_COMPILERS/test_contact_limited.py
---

# Contact-limited completion ratchet

## Outcome

This sprint turns the finite internal remainder from a prose roadmap into a
recomputed, fail-closed state contract. It does not claim that Emergentism is
finished, true, externally reviewed, replicated, published, or deployed.

The canonical machine baseline is
`00_META/CONTACT_LIMITED_STATE.json`. Its canonical JSON digest binds every
counter, ID set, lifecycle exception, owner-held row, and world-contact fence in
this receipt:

```text
contact_limited_state_canonical_sha256: 143e6d3d8a8c94adb68889498893b197a79102752675b0829eb6fb0649b7dc56
```

The digest is SHA-256 over UTF-8 bytes from JSON serialization with sorted keys,
no insignificant whitespace, and non-ASCII characters retained. A counter or
classification change therefore requires a new dated receipt and a new digest;
editing the state while retaining this receipt must fail.

## 1 · Receipt namespace

Two distinct universes are now named rather than compared as though they were
the same measurement:

| Measurement | Baseline |
|---|---:|
| citable live-lane receipt targets, excluding the `00_*` convention | 306 |
| prefixed Markdown filenames including the six `00_*` convention files | 312 |
| unique citable numeric prefixes | 184 |
| physically reused prefixes | 97 |
| legacy broad-status-word heuristic | 91 |
| reused prefixes unsafe as bare numeric citations | 97 |
| dangling numeric citations | 0 |

The 91 count is retained only as the output of a legacy heuristic. It does not
resolve a target, establish supersession direction, prove reciprocity, or make
six reused prefixes safe. All 97 physically reused prefixes remain unsafe as
bare citations until the citation-custody sprint replaces active ambiguity with
full filenames or an explicit machine binding. Canonical JSON path-set digests bind
the exact 306-target and 312-convention universes, while a canonical JSON digest
binds every reused-prefix group to its exact candidate paths; equal totals cannot
hide a remove-one/add-one substitution.

## 2 · Public lifecycle

The delivery checkout contains 404 HTML artifacts before ignore rules.
Gitignore-style matching excludes 16, leaving 388 deployable artifacts; the ten
withheld custody artifacts are then added back for a 398-artifact lifecycle
universe.

| Lifecycle | Count |
|---|---:|
| current | 40 |
| provisional | 4 |
| frozen | 328 |
| withheld | 11 |
| infrastructure | 1 |
| unclassified | 14 |

The ratchet also binds the non-scalar remainder:

- exactly one clean-route artifact collision remains: `/titans/`, owned by
  `titans.html` and `titans/index.html`, both under the same frozen/noindex
  lifecycle;
- exactly eight declared raw lifecycle overlaps remain: seven
  withheld-plus-frozen artifacts and `offline/index.html` as
  infrastructure-plus-frozen;
- ten withheld artifacts own ten canonical aliases and thirty raw alias forms,
  all redirected to `/historical-boundary/` with noindex/nofollow custody; and
- the existing public predeploy matcher still mishandles nested `_archive/`
  semantics. The ratchet uses the correct directory-component rule, exposes one
  matcher drift, and does not silently inherit that defect.

The fourteen unclassified artifacts remain named in the machine state. This is
a measured Sprint 5 input, not permission to classify them by guesswork. The
state also binds the exact universe and all six category memberships by
canonical JSON path-set digest, so swapping two artifacts between classes at constant
counts is a ratchet failure.

## 3 · Claim disposition

The earlier phrase “17 open claims” described only the W section of the machine
owner. The complete investigation owner has 26 rows:

- 17 W rows: 16 live-status rows and one terminal `NOT-WELL-POSED` row;
- 13 W rows routed to contact and four routed to internal disposition; and
- nine reopened research questions, `RQ-01` through `RQ-09`, still explicitly
  unadjudicated.

The ratchet binds the exact W ID-to-status map, not only its histogram. It also
preserves the W3 conflict: the machine owner still says `OPEN-EMPIRICAL`, while
`184_THE_PRODUCT_CONJECTURE_RULED_2026_07_30.md` and the empirical program say
the conjecture cannot be prosecuted as written without a defended cardinal
scale and invariant discriminator. This sprint exposes that source
reconciliation; it does not settle it silently.

## 4 · Owner-held residue

Exactly two routing debts remain, and both exact IDs are bound here:

1. `OWNER_GATE_HELD_PUBLIC_DOCS` — name the current numbered-doctrine-spine
   specification and route or explicitly retain its byte-identical duplicate.
2. `OWNER_GATE_OPEN_TOPOLOGY` — reconcile the root rule against per-pillar
   `00_META` lanes with the active `08_FRAMEWORK_SUPPORT/00_META/` exception.

A raw count of two is insufficient. Deletion, substitution, missing evidence,
or changing either owner question without a new dated receipt must fail.

## 5 · World-contact boundary

World contact remains `OPEN`, with zero accepted evidence records and two open
requirements: a discriminating independent observation, and independent
replication or external review filed as outcome custody.

No external-evidence validator exists yet, so any transition away from `OPEN`
fails closed. Commits, gates, model review, invitations, preregistrations,
internal receipts, bare URLs, and staged protocols are explicitly inadmissible
as world evidence. A future transition requires independent-party identity,
independence basis, discriminating protocol, outcome, verbatim custody, and
provenance.

## 6 · Negative controls and verification

Fifty-seven focused mutation controls cover stale counters, unsafe-prefix
relabeling, ignore semantics, lifecycle overlaps, artifact and withheld-alias
collisions, W/RQ disappearance, count-preserving status swaps, debt
substitution, internal-world-evidence spoofing, receipt-history rewrites,
membership substitutions, duplicate JSON keys, and ambiguous path-set
serialization. Nineteen Foundation mutation controls separately exercise the
typed firewall, including the active Record Ledger and a synthetic Titan
arithmetic violation.

The exact staged-tree replay passed with no skip:

- all 21 top-level scripted checks passed, followed by the independent derived-
  register reproducibility check;
- all 16 compiler suites passed, including 57 contact-limited tests, 19
  Foundation tests, and six staged-secret-scanner negative controls;
- the staged secret scan reported no secret patterns;
- Lean formal verification passed with `lake build`;
- purity scanned 919 active files, the Foundation firewall type-scanned 1,059
  source/current-public surfaces, and 2,485 local Markdown links resolved with
  zero broken links;
- the reproducible corpus registers contain 3,418 files and 794 folders; and
- the public predeploy suite passed 15/15 after generating 71 claim cards with
  384 edges; the site-artifact check also passed.

The first preliminary gate correctly fired because the work-in-progress mirror
had replaced the machine bucket label `open` with explanatory prose and did not
spell out its 312-file receipt convention count. Those two summaries were made
explicit; the isolated manifest checker and the full no-skip gate then passed.
This is evidence that the gate rejected drift, not evidence that its first run
was green.

## Remaining route

Sprint 4 owns active citation ambiguity; Sprint 5 owns fourteen public lifecycle
rows and the matcher drift; Sprint 6 owns the 26-row claim-disposition universe.
External review and world tests still require actual independent contact and
cannot be simulated by repository work.

No push, merge, deployment, publication, DNS change, email, reviewer contact,
participant recruitment, contract, money movement, or legal signature is
performed by this receipt.

## Kill criterion

This receipt fails if its canonical state digest does not match, any finite
remainder is omitted from the state or its scalar summary is omitted from the
CLI, a reused prefix is called safe without an exact target, a public alias gains
two owners, an RQ row disappears, debt labels are substituted at constant count,
or an internal artifact moves world contact.

---

*A counter is custody only when changing it leaves a dated seam.*
