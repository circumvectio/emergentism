---
packet: AUTOMATIC-RECEIPT-TO-OUTCOME-INGESTION
title: Automatic Receipt-to-Outcome Ingestion
status: WARRIOR RUNTIME PASS — closes the manual-memory gap at F6 by seeding receipt-linked pending outcomes automatically at settlement time. Does not claim realized ΣΔP automation.
authority: packet 98 coordination doctrine + packet 99 sovereign reading + post-99 state in 00_INDEX
depends_on:
  - 01_EMERGENTISM/11_UPLINK/98_THE_COORDINATION_PROBLEM_IN_FOUNDATION_TERMS_2026_04_23.md
  - 01_EMERGENTISM/11_UPLINK/99_SOVEREIGN_READING_OF_FOUNDATION_AND_ROSETTA_2026_04_23.md
  - 02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/spec/APU_COORDINATION_DOCTRINE_2026_04_23.md
date: 2026-04-23
gating_cell: "[L4 | D4 | S-Org | F-phi :: ksatriya_executor]"
rosetta:
  primary_column: "Neuroscience"
  register: "[S/I]"
  canonical_phrase: "Packet 101 · Automatic Receipt-to-Outcome Ingestion"
---

# Packet 101 · Automatic Receipt-to-Outcome Ingestion

## Why this exists

The sovereign/runtime doctrine named a real gap:

> Cortex lineage can witness what decided, and F6 receipts can witness
> that the organism acted, but ΣΔP still depends on manual operator
> memory if outcomes are only recorded later by hand.

That gap is now narrowed materially.

This packet registers the runtime pass that makes the organism
automatically seed a linked outcome row when settlement succeeds.

The point is not to over-claim realized performance.
The point is to stop losing the decision -> transcript -> receipt chain
just because no human remembered to write it down later.

---

## What shipped

### 1. Settlement now auto-seeds a canonical pending outcome

`SettlementRouter.route_approved_proposal(...)` now calls the learning
layer after receipt persistence.

Source surface:

- `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/core/circulation/settlement_router.py`

Behavior:

- after a proposal crosses F6 and yields a `SettlementReceipt`, the
  router seeds a linked `ExecutionOutcome`
- seeded row carries:
  - `proposal_id`
  - `decision`
  - `decision_id`
  - `transcript_id`
  - `receipt_id`
  - `rule_applied`
  - `circle_signal_id`
  - `directive`
  - `decision_class` when available
  - `provider_mix` when available
  - `conflict_score` when available
  - `legal_veto`
- seeded row is marked:
  - `actual_result = "pending"`
  - `resolution_status = "pending"`

This is the correct constitutional stance:

- settlement proves the organism acted
- settlement does **not** prove realized success

So the bridge is automatic, but the PnL claim remains honest.

### 2. Learning now converges on one canonical outcome row per proposal

Source surface:

- `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/core/circulation/learning.py`

New behavior:

- `find_outcome_by_proposal(...)`
- `upsert_outcome(...)`
- `ingest_settlement_receipt(proposal, receipt)`

This matters because one proposal should not sprawl into multiple
independent memory rows.

The new runtime shape is:

1. settlement seeds a pending linked row
2. later realization can replace that row via upsert
3. the proposal keeps one canonical learn-surface record

So the organism now has a real memory spine instead of append-only
forgetfulness.

### 3. Performance metrics now separate pending from realized

Still in `learning.py`.

`get_strategy_performance()` now distinguishes:

- `total_outcomes`
- `realized_outcomes`
- `pending_outcomes`

PnL and win-rate calculations only use realized outcomes.

This prevents a new lie:

> "we automated receipt ingestion, therefore performance improved"

No. The organism simply stopped forgetting linkage.
Realized quality still has to be earned.

### 4. Manual outcome recording now upgrades instead of duplicating

Source surface:

- `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/api/routers/router_learn.py`

The `/outcomes/record` path now uses `upsert_outcome(...)` rather than
blind append.

So a future realized outcome can replace the pending settlement seed
instead of creating a second proposal row.

---

## What this proves

The organism now automatically preserves the minimal chain needed for
empirical coordination learning:

`decision -> transcript -> settlement receipt -> pending outcome`

That is enough to say:

- the receipt/outcome linkage no longer depends on manual operator memory
- the learning layer can be updated later without reconstructing history
- coordination metrics can measure linkage coverage honestly

This is a real sovereign/runtime advance.

---

## What this does NOT prove

This packet does **not** claim full ΣΔP automation.

Three reasons:

1. `pending` is not `profit`

Settlement proves route completion, not realized gain/loss.

2. downstream realization is still a separate event

The organism still needs automatic ingestion of later F4/F5/F6 facts
that establish whether the position resolved profitably, neutrally, or
at a loss.

3. some deliberation metadata is only preserved when it survives onto
the proposal/decision object

`provider_mix`, `conflict_score`, and `decision_class` are seeded when
available, but proposal persistence is not yet a guaranteed complete
carrier of all deliberation-time metadata.

So this packet closes the **memory gap**, not the entire **measurement
gap**.

---

## Verification

Focused proof surface passed:

- `python3 -m py_compile`
  - `core/circulation/learning.py`
  - `core/circulation/settlement_router.py`
  - `api/services.py`
  - `api/routers/router_learn.py`
- `pytest`
  - `tests/test_learning.py`
  - `tests/test_settlement_router.py`

Green result at ship time:

- `16 passed`

New proof obligations covered:

- settlement routing auto-seeds a pending linked outcome
- repeat routing is idempotent
- pending outcomes do not contaminate realized performance metrics

---

## Net effect on the doctrine gap

The post-99 gap:

> receipt-outcome-delta join for ΣΔP measurement

is now best read as two layers, not one:

### Closed layer

- automatic settlement -> pending outcome linkage

### Still open layer

- automatic realized-outcome ingestion and outcome-quality measurement

That is a better decomposition, and a truer one.

---

## Next sovereign move

The clean next runtime frontier is:

1. auto-ingest downstream realized execution facts
2. update the canonical outcome row from `pending` to realized
3. compute ΣΔP proxies from receipts + realized outcomes together

That is the point where the organism stops merely remembering action
and starts measuring consequence.
