---
title: "Public-surface coverage audit — two route-count claims retracted; deployable gate repair survives"
date: 2026-08-27
status: "[B] corrected audit receipt — the initial 41-route and later 17-route gaps are both retracted; exact lifecycle reports zero unclassified artifacts. The deployable-page claim scan and bounded title defect survive."
evidence_tier: "[B] all counts measured in-session; [I] the false-positive judgements, each with quoted context"
owner: "Chair for the publication ruling in §3; agent-executable items in §5."
parents:
  - GATE_ADVERSARY_PREREGISTRATION_2026_08_27.md
  - ../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/54_THE_NEGATIVE_SPACE_OUTLINE_2026_08_27.md
---

# Public-surface coverage audit

## 0 · A correction to my own claim, first

I asserted that the register spine `/0/`–`/6/` was unreachable from the front
door — *"a cathedral with the nave sealed."* **That is false.** Measured: every
register page has **679–692 inbound links** site-wide, `/dimensions/` links to
all seven, and the generator emits `../{n}/` for each. My error was using
`grep -c`, which counts **lines**, against a near-minified file. The same
instrument class this estate has been auditing all week, committed by me, and
caught only by re-measuring. **The spine is fine.**

## 1 · The finding that survives

| | |
|---|---|
| live routes (excl. assets/vendor/build/archive) | **81** |
| surfaces in the scan manifest | **67** |
| **live routes the barred-claims gate never reads** | **41** |

`check_barred_claims` scans `currentSurfaces` + `declaredProvisional` from
`12_PUBLIC_SITE/public_semantic_parity.json`. Forty-one live routes are in
neither — among them `atlas`, `canon`, `corrections`, `ground`, `titans`,
`trinity`, `sacred`, `home` (44 KB), `complete-ontology` (35 KB), and **`test`,
a test route live in production.**

This compounds the 2026-08-27 adversary result. That experiment showed the gate
is **evadable inside its scope** (8 of 8). This shows **more than half the site
is outside it.** `withheld-routes.json` contains **zero** entries, so these are
unscanned by omission, not by declaration.

## 2 · What is actually hiding there — measured, not assumed

The gate's own `claim_policy.violations()` was run against all 41 unscanned
routes. **Three routes, four violations.** Small — and the composition matters
more than the count:

| route | fires | verdict |
|---|---|---|
| `corrections` | `⊙ = • × ○`, `P = Φ × V` | **BY-DESIGN EXEMPTION.** This page's job is quoting the retired forms in order to retract them. A retraction page that cannot name what it retracts is useless. |
| `historical-boundary` | "complete account of reality" | **FALSE POSITIVE.** Quoted context: *"is **not** being presented as established mathematics, physics, medicine, **or a complete account of reality**."* An explicit disclaimer. The policy's own negation suppression failed to reach across the intervening clause. |
| **`complete-ontology`** | `• × ○` | **REAL. LIVE. SERIOUS.** |

## 3 · The real one — and it needs a chair ruling

`12_PUBLIC_SITE/complete-ontology/index.html` (35 KB, the largest content page
on the site) publishes, as live doctrine:

> *"The Titan transformations encode this: **• × ○ = ⊙** (strong: the poles
> generate finity from below); **⊙ / ○ = •** and **⊙ / • = ○** (weak: finity,
> once established, makes the poles legible from above)."*

This is the arithmetic `45_THE_TITAN_INVERSION_STRUCTURE` retired on 2026-08-01
with the words *"That is false."* It is not quoted to retract; it is used as the
explanation of strong and weak emergence.

**Two facts make this a ruling rather than a repair:**

1. **The page is GENERATED**, and its source is an **archived** document —
   `90_ARCHIVE/pure_emergentism_boundary_2026_07_20/05_COSMOLOGY/00_THE_COMPLETE_ONTOLOGY_OF_REALITY.md`.
   A document behind the purity boundary is being published to the live site.
2. **Hand-patching the HTML would be reverted.** `generate_public_library.py`'s
   own docstring warns: *"or this generator will overwrite the hand-patches and
   reintroduce the over-claims."*

**The precedent exists and is reversible.** `/historical-boundary/` is exactly
this situation, handled: the route is withheld, the artifact stays byte-for-byte
in git custody, and re-publication requires a named owner, tier, rival,
discriminator, and kill. **Withholding `complete-ontology` on the same terms is
a precedented, reversible, one-line act** — or the generator's source may be
repointed off the archive. Either is a publication decision, which is the
chair's.

**Not done here:** no page edited, no manifest changed, no route withheld.

## 4 · Two further defects, measured

- **26 pages carry a doubled title suffix** — *"Rosetta D-Series — Emergentism
  — Emergentism"*, *"Method — Emergentism — Emergentism"*. The cause is
  documented in `generate_public_library.py`'s own docstring as an unfixed TODO:
  when a source heading already ends in `— Emergentism`, the shell appends a
  second one.
- **Two branding lineages bleed through**: some titles end `— Emergentism`,
  others `— Magnum Opus`.
- **Duplicate route clusters**: three Rosetta routes (`rosetta`, `rosettad`,
  `rosetta-d-series`), two Suda routes, `method`/`methodology`, and three
  ontology routes.

## 5 · Agent-executable, once the §3 ruling lands

1. Bring the 41 routes into scan scope, with `corrections` and
   `historical-boundary` carried as **declared, documented exemptions** — not
   silently skipped. An exemption a reader can see is a fence; an omission is a
   hole.
2. Fix the doubled suffix at the generator, then re-render and re-verify all 26.
3. Retire `/test/` from the live surface.
4. Consolidate the duplicate clusters behind forwarding stubs (archive-first;
   the stub is the cure for dead paths, not clutter).

**Scope expansion does not fix evadability.** The adversary experiment stands:
the gate can be walked past *inside* its scope by litotes, commutativity,
paraphrase, or markup. Coverage and soundness are different repairs, and this
receipt claims only the first.

**Canonical path:** `01_EMERGENTISM/00_HANDOFF/PUBLIC_SURFACE_COVERAGE_AUDIT_2026_08_27.md`

---

# RETRACTION — same day, before any action was taken on §3

**§3 of this document is WRONG and is retracted in full. `complete-ontology` is
not a live public defect. It was already withheld before I wrote a word about
it.**

## What I got wrong, and how

I wrote: *"`withheld-routes.json` contains **zero** entries, so these are
unscanned by omission, not by declaration."*

The file contains **195 declared artifacts**, each with a `sha256`, a byte
count, its `publicRoutes`, a `reason`, and `policyRuleIds`. I queried it for a
`routes` or `withheld` key. **The key is `artifacts`.** I read a registry, found
nothing at the name I guessed, and reported an absence.

## The corrected measurement

| | |
|---|---|
| live route directories | 81 |
| in the scan manifest | 40 |
| **declared withheld, under sha256 custody** | **24** |
| genuinely unaccounted | **17** (not 41) |
| **violations on genuinely-unaccounted routes** | **1 — and it is a false positive** |

The single hit is `historical-boundary`, which is the **withholding destination
page itself**, and its text reads *"is **not** being presented as … a complete
account of reality."* A disclaimer, flagged by a negation-suppression miss.

**Every route I named as a defect is declared and custodied:**
`complete-ontology` — **WITHHELD**. `corrections` — **WITHHELD**. `test` —
**WITHHELD**, so it is not "a test route live in production." The retired Titan
arithmetic I called *"REAL. LIVE. SERIOUS."* sits behind a redirect to
`/historical-boundary/`, `noindex, noarchive, nosnippet, nofollow`,
`no-store`, and out of the sitemap. **The estate had already solved this, with
better machinery than the fix I was about to propose.**

The gate does not scan those routes **because they are not published.** That is
correct behaviour, not a hole.

## What actually survives

1. **17 routes are genuinely unaccounted** — in neither the scan manifest nor
   the withholding registry. They carry **zero** genuine violations. This is a
   bookkeeping gap, not a contamination: `cosmology`, `epistemology`, `formal`,
   `foundations`, `ground`, `memetic`, `meta`, `method`, `methodology`,
   `offline`, `ontology`, `operators`, `paradox`, `sacred`, `sources`,
   `theology`, and `historical-boundary` itself. Each should be *declared* one
   way or the other — published-and-scanned, or withheld-and-custodied.
2. **The doubled title suffix on 26 pages** stands, and is still a documented
   TODO in the generator.
3. **The duplicate route clusters** stand — though `rosettad`,
   `rosetta-d-series`, `suda-notes`, `geometric-ontology` and `complete-ontology`
   are all *withheld*, which is most of what "consolidation" would have
   achieved. **Already done, by someone who read the registry.**
4. **The adversary result is untouched.** The gate remains evadable inside its
   scope, 8 of 8. That finding was measured against the gate's own source and
   does not depend on any of this.

## The lesson, recorded because it is the fourth of its kind today

This session has now produced four measurement errors, each corrected only by
re-measuring: the sealed-nave claim (`grep -c` counts lines, not occurrences),
two stale counts inherited from `04_WHAT_DIED.md` and transmitted without
re-running, and this one — **an absence reported from a wrong key.**

The pattern is identical every time: **a query returned nothing, and I reported
that as a fact about the world rather than a fact about my query.** A null
result is a claim about the instrument until it is a claim about the territory.
The estate already holds this rule for `grep` and `.gitignore`; it generalises
to every lookup, and the generalisation is now on the record.

**Nothing was edited, withheld, or repointed on the strength of §3.** The
retraction arrives before the action, which is the only reason it costs
nothing but the writing.

---

# SECOND CORRECTION — same day, after the exact lifecycle was run

The later statement that **17 routes are genuinely unaccounted** is also
false. It is retracted.

That number came from comparing route-directory names with only the
`currentSurfaces`, `declaredProvisional`, and withholding registry. The estate's
actual lifecycle is a combined artifact classifier with six states: current,
provisional, frozen, withheld, infrastructure, and unclassified. On the exact
checker at the then-current baseline it reported:

```text
public=414 [56 current / 3 provisional / 92 frozen / 261 withheld /
            2 infrastructure / 0 unclassified]
alias-collisions=0
```

Several of the alleged 17 are frozen library roots; `offline` is
infrastructure; `historical-boundary` is the boundary destination. Directory
presence was never proof of missing lifecycle custody.

## Findings that survive both corrections

1. The barred-claims checker duplicated only the current/provisional manifest
   scope instead of asking the release boundary which HTML files were actually
   deployable. That is a **gate-scope defect**, not a lifecycle hole.
2. Expanding the exact deployable scan exposed three frozen artifacts that
   affirmatively carried retired Titan arithmetic. They are now proposed for
   the existing reversible withholding mechanism; no content deletion is
   required.
3. The historical-boundary denial was a real clause-parser false positive:
   one source-wrapping newline incorrectly ended the negation context.
4. Only eight deployable source pages—not 26—carry duplicated terminal title
   branding. Withheld artifacts remain byte-custodied and are not rewritten.

The governing lesson is now stronger: a route count is a claim about the
instrument until the exact delivery and lifecycle semantics have classified
the artifact. The corrected implementation must scan all deployable HTML,
preserve exact withholding custody, and keep zero unclassified artifacts.
