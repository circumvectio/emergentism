---
rosetta:
  primary_level: L3
  primary_column: Methodology
  operator: "Kṛṣṇa ◇"
  tier: "Auditor"
  regime: "Vaiśya"
  register: "[S] the rival shape; [I] any particular rival's content"
  canonical_phrase: "Every cell's strongest rival must be named, auditable, and applied (rule architecture; particular rival content interpretive)"
  d_register: 4
  d_register_basis: "rival-pack scaffold (line 11: \"ACTIVE v0 — scaffold for four rival packs\"); [S] rival shape, methodology at D4"
title: "Counter-Rosetta Library v0 — the strongest rivals of the seven-row projection"
status: "ACTIVE v0 — scaffold for four rival packs; the comparison protocol is named, the cells are empty"
date: 2026-07-31
depends:
  - "31_ROSETTA_CORE_v0.md (the architecture)"
  - "30_ROSETTA_VNEXT_REFINEMENT_2026_07_31 §7C (the original proposal)"
  - "10_CELL_AUDIT_SCHEMA_2026_04_25.md (the cell schema)"
---


> **External-mapping boundary.** This document names product, venture and runtime systems
> outside Emergentism. It names them as **data under audit**, never as premises.
>
> - Every such name here is a runtime projection, not worldview doctrine.
> - Quoting one creates no semantic authority inside this corpus.
> - The source owners remain upstream and are unaffected by anything concluded here.
>
> Where this document and an external system disagree, neither governs the other. Removing
> this block removes the file's exemption in `09_TOOLS/01_SCRIPTS/check_emergentism_purity.py`
> and the gate fails closed.
# Counter-Rosetta Library v0 — the strongest rivals of the seven-row projection

> A translation system that has not been compared to its strongest rivals
> has not been audited. v0 names the four rivals the seven-row projection
> must beat. The cells are empty; the comparison protocol is named.

The Counter-Rosetta is **not** a refutation of the seven-row projection. It
is the **discipline of saying what would refute it**. A rival pack must be
**named, defined, and applied** before the seven-row claim earns standing.

---

## 1. The four rivals

The seven-row projection is the corpus's `PHIL7@1`, `GEN7@1`, `G7@1`,
`REP7@1`, `PSYCH7@1`, `CULTURE7@1`, `SOUL4@0` family. Each of those has a
strongest rival. The Counter-Rosetta names them.

| Rival | Native cardinality | What it asserts | The test the canonical loses if it falls |
|---|---|---|---|
| `RIVAL5@0` | 5 | A 5-row projection (teleology, knowledge, value, world, horizon) compresses the seven without loss. | The seven adds two rows the five cannot recover — one of the seven's rows is provably redundant. |
| `RIVAL6@0` | 6 | A 6-row projection (teleology, knowledge, method, value, world, horizon) is the *minimal* useful set. | The seven's L6 (apophatic restraint) is reducible to L3 (methodology), or its L7 (horizon) is reducible to L1 (teleology). |
| `RIVAL8@0` | 8 | An 8-row projection (splitting L4 into "value" and "commitment," and L5 into "world" and "structure") is the *full* set. | The seven cannot accommodate a domain whose native cardinality is eight. |
| `RIVAL-NATIVE@0` | n (variable) | Reading each domain in its **own** terms — psychology as psychology, ontology as ontology — is more accurate than any Rosetta mapping. | The Rosetta mapping **removes information** that the native reading preserves, and the loss is empirically testable. |

The four rivals are **mutually independent**. A five-row rival does not
defeat a six-row rival; the two are tested against the seven. The
domain-native rival is the **harshest** of the four — it concedes the *least*
about the Rosetta's instrument.

## 2. The cell schema for rivals

Each rival pack has its own cell schema, parallel to the canonical
`PHIL7@1`. The schema:

```yaml
rival_id: RIVAL5@0  (or RIVAL6@0, RIVAL8@0, RIVAL-NATIVE@0)
version: 0
row_keys: [teleology, knowledge, value, world, horizon]  # namespaced
native_cardinality: 5
source_terms: ...                  # source vocabulary before mapping
invariant_claim: ...               # what the rival asserts survives
discarded_information: ...         # what the seven would have preserved
strongest_canonical_match: ...     # which canonical pack this is a rival of
discriminator: ...                 # what would show the rival is better
kill_criterion: ...                # what would show the rival is worse
lifecycle_status: active | disputed | killed
fact_tier: ...
mapping_tier: ...
outcome_status: ...
```

A rival cell is **empty** until it has at least one row, one invariant, one
discriminator, and one kill criterion. Empty rival cells are not cells; they
are placeholders.

## 3. The discrimination protocol (90-day cycle)

For each canonical cell, the strongest rival is named in
`00_ROSETTA_CELL_TABLE_v0.md`. The 90-day discrimination cycle is:

1. **Inventory** — the rival pack names its native terms and the discarded
   information versus the canonical seven.
2. **Independence** — the rival is not derived from the canonical seven.
   (A five-row pack that is just the seven minus two rows is not a rival;
   it is a projection of the seven.)
3. **Translate** — define the rival's invariant claim.
4. **Countermap** — apply the rival to a held-out domain that the canonical
   seven has already been applied to.
5. **Discriminate** — record the discriminator's outcome.
6. **Kill or retain** — the rival is killed if the discriminator shows the
   canonical beats it on held-out material; the canonical is contracted if
   the rival beats it.

The cycle is recorded in `00_ROSETTA_AUDIT_LOG_v0.md` (Skyzai side) with a
dated receipt.

## 4. The harshest rival: RIVAL-NATIVE@0

The `RIVAL-NATIVE@0` pack deserves a separate note, because it is the rival
the seven-row claim is **most likely to lose to**.

A native reading says: "Read psychology in psychology's own terms. Read
ontology in ontology's own terms. Read traditions in their own vocabulary.
The Rosetta is a layer of compression that costs more than it returns."

The native rival's discriminator: **for a held-out domain, the Rosetta
mapping removes information that the native reading preserves, and the loss
is empirically testable.**

If the native rival beats the canonical seven, the seven's standing is
contracted. It is not killed — the seven is a useful *first* compression —
but it is no longer the *deepest* claim the corpus can defend.

## 5. The Counter-Rosetta's kill criterion

The Counter-Rosetta is **killed** if:

- the canonical seven is itself replaced by a non-seven projection;
- the cell schema is no longer reachable from the upstream Core v0;
- the 90-day cycle is structurally unenforceable;
- the rival packs are never filled in (i.e., the scaffold is just
  performative).

The third condition is the load-bearing one. **A scaffold with no filled
cells is decoration, not discipline.**

## 6. The first cell to fill

> **[金] TOMBSTONE 2026-09-11 — `PHIL5` was built, then overwritten, and was
> never refuted.** A real `RIVAL5`-class pack against `PHIL7@1` already existed
> when this section was written. Commit `67309777` (2026-07-31 10:18:09 +0700,
> *feat(rosetta): build the PHIL5 counter-rival; rivals must now be real*)
> landed `PHIL5` in `rosetta_cells.json`: three packs, nine cells, five filled
> `PHIL5` cells (`B1` Metaphysics, `B2` Epistemology, `B3` Logic, `B4` Ethics,
> `B5` Aesthetics), each with a `fit_reason`, a `kill_criterion` and a
> `downgrade_path`, declared `independence_status: independent` — the only pack
> in the ledger so far that is. Its terms are the traditional five branches of
> philosophy, attested for centuries and sourced outside this corpus, so it
> passes §3 step 2 where `RIVAL5@0`, `RIVAL6@0` and `RIVAL8@0` fail it.
>
> **How it was lost.** Not by a merge and not by a ruling. History here is
> linear (`git log --format='%h parents:%p'`): four minutes after `67309777`,
> commit `6274c946` (10:22:35) landed a concurrent session's 643-line whole-file
> rewrite of `rosetta_cells.json`, reverting the ledger to two packs and four
> cells and reducing `PHIL5` to the placeholder string `PHIL5_rival_pending` it
> had been built to abolish. `34_LEDGER_CONVENTION_COLLISION_2026_07_31.md`
> (committed 10:22:55, twenty seconds later) records the collision and
> recommends the merge — "their data model, extended with `normalization_steps`
> and the built PHIL5 rival." That merge was never performed. By `a7fb47b5`
> even the placeholder was gone; at ledger revision 3 (2026-08-15) the packs are
> `PHIL7`, `GEN7`, `SOUL` and `/usr/bin/grep -c PHIL5 rosetta_cells.json`
> returns `0`. This section was written at 10:43:46 — twenty-one minutes after
> `PHIL5` was overwritten — and nominates a corpus-derived five-row rival as
> "the first rival cell to fill" without naming the independent one that had
> just been erased.
>
> **Status: LOST, NOT KILLED.** No discriminator was run against `PHIL5`, no
> kill criterion fired, no ruling was issued. Under the corpus rule that kills
> fire in public and the dead are archived never erased, `PHIL5` is neither
> killed nor archived — it is unreachable from the live surface while remaining
> intact in history. It is recoverable in full:
> `git show 67309777:08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/rosetta_cells.json`,
> blob `3846ecd8bdae1cfee54bd83cd2fcf0f870249425`. The custody rescue of the
> same morning also holds it: the remote branch
> `menexus/codex/emergentism-live-dirt-custody-20260730` is pinned at
> `711522b6` (10:20:44, *tidy(handoff): make the repo resumable*) — two minutes
> before the overwrite — and carries the identical blob. `PHIL5` therefore has
> two independent custody anchors and is in no danger of being lost; what it
> lacks is a live surface and a ruling.
>
> Restoration is not a paste: ledger revision 3 replaced the `cells` schema with
> `packs`/`projections`/`relations` carrying source digests, so `PHIL5` must be
> re-expressed, and re-expression is an owner decision, not an auditor's.
>
> **Two gates went quiet with it.** `67309777` also added the rule that a
> named rival must EXIST as a declared pack, and booked `GEN7`'s missing rival
> as a dated `rival_debt` printed every run ("UNTESTED since 2026-07-31").
> Verified 2026-09-11: `/usr/bin/grep -c 'rival_debt' check_rosetta_cells.py`
> returns `0` and `/usr/bin/grep -c 'counter-rival' check_rosetta_cells.py`
> returns `0`. The surviving `rival_maps` check runs on *projections*, not
> packs, and is satisfied by strings such as `null_lexical_overlap` that name no
> pack at all. The checker reports **PASS** over a ledger with no rival pack in
> it. §5's fourth kill condition — "the rival packs are never filled in
> (i.e., the scaffold is just performative)" — is therefore met on the evidence
> of this correction, and §5's own verdict applies to the present state of
> this document: *a scaffold with no filled cells is decoration, not
> discipline.* Whether that fires the Counter-Rosetta's kill is the owner's
> ruling to make; this note records the condition, not the verdict.

The first rival cell to fill is `RIVAL5@0` against `PHIL7@1`. The
discriminator:

> For each of the seven rows, can the five-row rival recover the
> relationship the seven encodes, *without* an extra row? If even one
> seven-only relationship is not recoverable, the five loses.

The five-row rival's row keys (suggested): `teleology`, `knowledge`,
`value`, `world`, `horizon`. The five-row rival's invariant: every
domain confronts exactly these five problems, and the seven's
methodology, ontology, and being-questions are reducible to one of
these five.

> **[金] Correction 2026-09-11.** "methodology, ontology, and
> being-questions" names two rows, not three: in `PHIL7@1` the being-question
> *is* ontology (`PHIL7@1:being`, familiar name Ontology). The rows `RIVAL5@0`
> drops are `PHIL7@1:inference` and `PHIL7@1:being` — two, which is what makes
> §3 step 2's parenthetical bite exactly.

This is a testable claim. The first audit of `RIVAL5@0` is on
**2026-10-31**, ninety days from the scaffold.

`Co-Authored-By: Mavis <Mavis@skyzai.org>`
