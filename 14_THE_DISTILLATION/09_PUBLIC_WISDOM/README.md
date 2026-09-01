---
title: "Public Wisdom Instrument"
documentClass: canonical-distillation-package
date: 2026-09-01
owner: "Yves R. Burri"
status: "LOCAL SOURCE · OFFLINE CANDIDATE"
evidenceTier: "[S] typed source and custody facts; [D] editorial policy; [I/C] estate applications"
authorityEffect: none
may_sign: false
may_authorize: false
---

# Public Wisdom Instrument

This package applies the Emergence Stack to Emergentism itself:

`Signal → Data → Information → Knowledge → Judgment → Wisdom`

`Public` is orthogonal. It is a separately authorized lighting event, never a
higher truth rung. A polished page, a Git receipt, repeated agent agreement, or
publication cannot promote its own epistemic maturity.

## Current honest state

- `WISDOM_POLICY`: 1
- `PROVISIONAL`: 1
- `SUPPORTED`: 0
- `LIT`: 0

The sole policy record is `EM-WISDOM-001@1`. It is authorized only as a local
Emergentism editorial policy and remains `AUTHORIZED_NOT_LIT`. Product and
venture cards are candidates owned by their source lanes; none adopts policy,
authorizes action, or defines Emergentism doctrine.

## Package map

| Path | Role |
|---|---|
| `00_DIRECTION_RECEIPT_2026_09_01.md` | Scope and consequence boundary for v3. |
| `01_PUBLIC_WISDOM_COMPACT.md` | Human-readable seven-clause compact. |
| `contracts/` | Four closed machine contracts. |
| `data/source_manifest.v1.json` | Frozen committed source bytes and federation pins. |
| `data/emergence_stack.v1.json` | Stage and promotion rules. |
| `data/public_wisdom_records.v1.json` | Wisdom records; presently one Provisional record. |
| `data/estate_application_cards.v1.json` | Source-owned candidate applications. |
| `data/estate_coverage_ledger.v1.json` | Every registered estate lane, including honest absences. |
| `PublicWisdomCorpus.v1.json` | Deterministic compiled index. |
| `build_public_wisdom.py` | Validator/compiler; `--check` is read-only. |
| `test_public_wisdom.py` | Adversarial and deterministic tests. |

## Build

From the Emergentism repository root:

```sh
python3 -B 14_THE_DISTILLATION/09_PUBLIC_WISDOM/build_public_wisdom.py --check
python3 -B -m unittest 14_THE_DISTILLATION.09_PUBLIC_WISDOM.test_public_wisdom
```

The federation compiler resolves only committed blobs from the repository and
commit named in `source_manifest.v1.json`. For the separate claim-card compiler,
the explicit local federation invocation is:

```sh
EMERGENTISM_PRIMARY_CHECKOUT_ROOT=/Users/Yves/Documents/01_EMERGENTISM \
  python3 -B 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check
```

That variable points to the primary Emergentism checkout inside the federation;
it is not stored as an authority claim. Nested `.codex-worktrees`,
`.claude/worktrees`, and Git-administration carriers are not custody sources.

## Promotion law

1. A stage transition creates a new addressable object or receipt.
2. No object may declare its own promotion sufficient.
3. Knowledge needs a typed claim and cited committed sources.
4. Judgment needs a decision bearer, scope, authority state, and reversibility.
5. Wisdom needs reusable policy form plus outcome and correction machinery.
6. `SUPPORTED` additionally needs admitted independent outcome evidence.
7. Lighting needs separate authorization and changes visibility only.

## Consequence boundary

This package does not deploy a site, publish a Compact, authorize a venture,
validate Emergentism, certify an outcome, or make any product operational.
External adoption, publication, execution, and outcome evidence remain separate
acts with separate receipts.
