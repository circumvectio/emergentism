---
title: "Rosetta ledger — two parallel implementations collided"
date: 2026-07-31
status: "[S] observation. Nothing reconciled; nothing of either party's work altered."
d_register: 4
d_register_basis: "convention collision observation (line 4: \"[S] observation\"); audit of factual divergence at D4"
rosetta:
  canonical_phrase: "Two parallel sessions built the Rosetta ledger with different conventions in the same file; the checker reporting 38 problems is the checker working"
canonical_phrase: "Receipt (2026-07-31) of the 38-checker-failure collision between two parallel rosetta-cells.json implementations; four mechanical mismatches catalogued (enum casing, normalization_steps, projection_id, PHIL5/PHIL7 placeholder), merge proposed, neither party's work altered."
---

# Why `check_rosetta_cells.py` reports 38 problems

**It is working.** Two efforts built the machine-readable ledger in parallel on the
same day, in the same file, with different conventions. The checker is reporting
that divergence, which is what it is for.

## What happened

| Commit | Author-side | Content |
|---|---|---|
| `902795ea` | concurrent session | vNext refinement proposal `[D]` |
| `7140a813` | this session | `rosetta_cells.json` + `check_rosetta_cells.py` — 4 cells, 2 packs |
| `67309777` | this session | PHIL5 counter-rival — 9 cells, 3 packs, GEN7 rival-debt |
| *(uncommitted)* | concurrent session | 643-line rewrite of `rosetta_cells.json`, plus `31_ROSETTA_CORE_v0.md`, `32_PACK_SOUL4_v0.md`, `33_LIVE_DRIFT_RECONCILIATION_v0.md` |

Both committed versions are in history. The working-tree rewrite is the concurrent
session's and has been left untouched.

## The four mismatches, all mechanical

1. **Enum casing.** Their cells use `FRAMEWORK_DERIVED` / `PARTIALLY_DEPENDENT`; the checker expects the schema's own lowercase-hyphenated forms (`framework-derived`, `partially dependent`). Pick one and normalise — the schema document is the tiebreaker.
2. **`normalization_steps` absent** on their packs. Required by rule 5, which is the rule that stops a five-part tradition being silently reshaped to seven. Worth keeping.
3. **Relation-cells carry no `projection_id`, `row`, or `cell_tier`.** Their ledger introduces a genuinely new object — a *relation between two cells* (`PHIL7@1:purpose__to__GEN7@1:L7__r1`) — which my schema did not anticipate. **This is their design being better than mine on this point**: a cross-pack relation is exactly what the teleology collision needs to be expressible as data rather than prose. The checker should gain a separate `relations` section with its own required fields rather than forcing relations through the cell shape.
4. **PHIL7 rivals reverted to placeholders** (`PHIL5_rival_pending`), and PHIL5 is absent from their pack list. Their version predates the counter-rival being built.

## Recommendation

Do not resolve this by picking a winner. Their relation objects and their
`ROSETTA_CORE`/`SOUL4` packs are additive to what is committed; the checker's rules
are additive to what they wrote. The merge is: their data model, extended with
`normalization_steps` and the built PHIL5 rival, validated by an extended checker
that knows about relations.

**Until then the checker fails, and that is the correct state.** A green checker
over two incompatible ledgers would be worse than a red one.

## The general hazard

This is the fourth same-day collision between parallel sessions in this estate:
two entity-graph designs, two sprint plans to G6, two records of one owner
signature, and now two cell ledgers. Run `git log --oneline -15` and `git status`
before starting work in any active lane.
