---
title: "Public-surface coverage audit — the barred-claims gate sees less than half the live site"
date: 2026-08-27
status: "[B] audit receipt — every count recomputed on disk 2026-08-27 and re-runnable by the commands given. Changes nothing; one item requires a chair ruling."
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
