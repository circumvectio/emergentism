---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Kṛṣṇa ◇"
  tier: "Executive"
  regime: "Vaiśya"
  register: "[S] routing; referenced claims retain their own tiers"
  canonical_phrase: "One non-owning manifest for conjectures, proofs, counterexamples, refutations, and failed proof attempts"
type: meta-pointer-index
title: "Conjectures and Proof Attempts — manifest-bounded index"
status: "ACTIVE 2026-08-24 — routing and completeness accounting only"
owner: "00_META discoverability; semantic and validation ownership remains distributed"
---

# Conjectures and Proof Attempts

This is the requested one-place front door for Emergentism's conjectures and
attempts at proof.

It is deliberately a **pointer manifest**, not a new doctrine owner. Moving or
copying every source here would create competing propositions, broken links,
and tier drift. The actual conjectures, theorems, counterexamples, nulls, and
refutations remain at their source owners.

## The four-way firewall

```text
analytic theorem ≠ emergence analogy ≠ ontological conjecture ≠ adopted canon
```

Container membership never promotes an inner claim.

- [`BIL-01`](../../05_COSMOLOGY/03_FORMAL_SYSTEM/59_BOUNDARY_INFORMATION_LOSS_LEMMA_BIL_01.md)
  is an `[A]` ordinary-analysis theorem about endpoint information loss.
- Reading that theorem as an image of directional emergence is `[I]`.
- [`TEA-01`](../../06_ONTOLOGY/12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md)
  is an `[A]` theorem of relative type-extension asymmetry; mapping any natural
  crossing to its premises remains `[C]` under `SLWP-01`.
- [`EAS-10@1`](../../06_ONTOLOGY/14_THE_TEN_EMERGENTIST_ANSWERS_2026_08_24.md)
  records ten owner-adopted internal answers. Adoption is a lifecycle state,
  not proof, validation, PQA adjudication or publication.
- [`04_THE_CONJECTURES.md`](../../06_ONTOLOGY/04_THE_CONJECTURES.md) remains
  the sole W0–W12 wager ledger.
- [`CLAIM_STATUS.yaml`](../claim_status/CLAIM_STATUS.yaml) remains the
  validation-status router. The manifest does not become another status axis.

## What “all” means here

The index is **manifest-complete as of 2026-08-24 under scope-rules v1**. That
means:

1. every row in the machine claim-status catalog is snapshotted by exact ID;
2. every dedicated source-owner packet selected by the dated conjecture/proof
   census and the 2026-08-24 internal-answer amendment is represented;
3. decisive proof, counterexample, refutation, and provenance surfaces cited by
   those owners are represented; and
4. every excluded class and unresolved discovery debt is stated in
   [`MANIFEST.json`](MANIFEST.json).

It does **not** mean every sentence containing “may,” every third-party
conjecture cited by the corpus, every possible future proof attempt, exhaustive
archive coverage, complete mathematics, or a validated worldview. A new
qualifying source missing from the manifest kills the completeness claim until
it is classified.

## Read order

1. [`MANIFEST.json`](MANIFEST.json) — exact entries, source hashes, relations,
   exclusions, and frozen claim-status IDs.
2. [The Wager Ledger](../../06_ONTOLOGY/04_THE_CONJECTURES.md) — W0–W12 forms,
   entry tiers, kills, and graves.
3. [The Claim Status Register](../00_THE_CLAIM_STATUS_REGISTER.md) — current
   validation-status vocabulary and human-readable rows.
4. [BIL-01](../../05_COSMOLOGY/03_FORMAL_SYSTEM/59_BOUNDARY_INFORMATION_LOSS_LEMMA_BIL_01.md),
   [SLWP-01 / TEA-01](../../06_ONTOLOGY/12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md),
   and [the ten-answer layer](../../06_ONTOLOGY/14_THE_TEN_EMERGENTIST_ANSWERS_2026_08_24.md)
   — theorem, failed transfer, relative proof, selected answers and retained
   natural-world debts.

## How an attempt is represented

Each manifest entry separates:

- a stable manifest locator from any source-owned claim ID;
- record kind from lifecycle;
- evidence tier from validation status;
- source owner from historical evidence;
- target claim from attempt outcome;
- rival, discriminator, kill, and survivor; and
- live material from archive or public projections.

Failed attempts remain addressable. A refutation is not deleted when a weaker
successor survives.

## Drift gate

Run:

```sh
python3 -B 09_TOOLS/01_SCRIPTS/check_conjecture_proof_attempt_manifest.py
```

The checker fails on malformed structure, duplicate entry locators, dangling
or absolute paths, source-hash drift, stale claim-status IDs, archive/public
projections presented as live owners, `SLWP-01` masquerading as `W19` or a
canonical status row, and a missing theorem/conjecture boundary.

## Adding a conjecture or proof attempt

1. Write or repair the proposition at its semantic owner.
2. State its tier, lifecycle, assumptions, rival, discriminator, kill, and
   survivor there.
3. Add a pointer entry and source hash to `MANIFEST.json`.
4. Preserve any failed predecessor and typed relation.
5. Run this folder's checker, the claim-status checks when applicable, the link
   checker, and generated-register checks.

No step above adopts a wager, validates a claim, publishes a paper, or deploys
a public surface.

## Historical predecessor

The archived April peer-review router at
`90_ARCHIVE/08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/01_CONJECTURES_AND_PROOFS/`
is preserved as historical design precedent. It is not revived as a live
authority and is not counted as a current source owner.
