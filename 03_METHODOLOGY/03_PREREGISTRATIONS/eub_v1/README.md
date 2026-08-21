---
title: "EUB-1 v1.0 Harness"
status: "OFFLINE-READY · [D] · no candidate result"
date: 2026-08-21
owner: "06_THE_DASEIN_TEST_EUB1_v1.0.md"
---

# EUB-1 v1.0 Harness

This is the self-contained reference implementation for
[`06_THE_DASEIN_TEST_EUB1_v1.0.md`](../06_THE_DASEIN_TEST_EUB1_v1.0.md).
It uses Python’s standard library only.

It is a development harness, not a validated benchmark, live evaluation,
held-out release, DOI deposit, arXiv submission, or deployment.

## Commands

Run from this directory:

```bash
python3 run_eub.py validate --input recorded_responses/dasein_account_dev.json
python3 run_eub.py generate --seed 1701 --out /tmp/eub-fixture.json
python3 run_eub.py run --dry-run --condition NEUTRAL --out /tmp/eub-run.json
python3 run_eub.py validate --kind run-bundle --input /tmp/eub-run.json
python3 run_eub.py score \
  --fixture fixtures/dev/dasein_chain_seed_1701.json \
  --account recorded_responses/dasein_account_dev.json \
  --out /tmp/eub-score.json
python3 run_eub.py freeze --check
python3 -m unittest discover -s tests -v
```

`freeze --check` never updates hashes. The public CLI has no repin operation.
A source owner may replace the canonical manifest only as an explicit reviewed
source edit with a visible diff after all payload changes have passed review.

`run` is a five-sitting driver. It freezes one prompt, raw-response commitment, and
parsed-snapshot hash at each of Unfold, Attack, Spark, Contact, and
Reflex/Transfer; exact parent hashes and append-only revisions join the five
snapshots. The bundled recorded response is expanded into a deterministic
synthetic replay for acceptance testing only. It is not a model evaluation and
its generated stage hashes are not represented as five provider calls.

The standalone `score` command reconstructs that reviewed synthetic replay.
A lone final account remains `PARTIAL`: temporal discovery, prediction,
correction, reflex, and transfer dimensions are never credited without the
five frozen snapshots. Malformed JSON, a malformed provider wrapper, or valid
JSON with the wrong account shape produces an `INVALID_OUTPUT` receipt. Unless
credential matching requires withholding, the receipt binds both the exact
screened provider-byte hash and the decoded text commitment. Credential-bearing
bytes and their digest are withheld; a typed public redaction descriptor is
committed instead. Every non-scored failure state carries 15 null dimensions,
never an invented zero or positive score. Completed sittings survive a later
failure. Output paths are published only after a complete fsynced temporary
artifact exists, using an atomic no-replace link.

## Network boundary

`run` is offline by default, including for localhost. Tests use only recorded
responses. A live call requires all of:

- `--allow-network`;
- `--run-class AUTHORIZED_PILOT` or `AUTHORIZED_SCORED`;
- `--authorization-ref`;
- a positive `--cost-limit-usd`;
- explicit input/output token rates plus `--cost-basis-ref`; and
- an exact requested model ID.

Before every provider call, UTF-8 prompt bytes plus a documented 1,024-token
single-message framing allowance must fit the declared input cap. The adapter
then reserves that full input cap plus the output cap against one cumulative
five-sitting cost envelope. A call that would cross the limit is refused before
transport.

Anthropic credentials are read only from `ANTHROPIC_API_KEY`. OpenAI-compatible
credentials are read only from `OPENAI_API_KEY`; a local endpoint may explicitly
run without a key. The credential snapshot used for the request remains in the
screening set even if the environment rotates during transport; literal,
JSON-escaped, and nested decoded occurrences are rejected before hashing.
Credentials are never placed in envelopes, receipts, logs, hash manifests, or
exceptions. A live response without a resolved model ID is rejected. Provider
usage is also mandatory: both live adapters require exact non-negative integer
input and output token fields. Missing or partial usage is `INVALID_OUTPUT`; it
is never normalized to zero cost.

The deterministic scorer binds public query IDs, phase-visible answer classes,
typed fields, source assertions, and frozen oracle policy. Its bounded lexical
checks are review proxies, not a general semantic judge. Subtle prose-level
private-lineage invention, Ground reification, or teleological smuggling still
requires preregistered blinded human review; a proxy pass does not prove those
failures absent, and a proxy miss alone is not a structural hard gate.

## Custody

Development fixtures publish truth so the deterministic scorer can be tested.
Future held-out seeds and truth do not belong in this repository. A real scored
run requires independent custody. `CUSTODIAN_INTERFACE.md` specifies the
separate private opening and redacted public receipt; software verifies the
commitments but not custodian independence or commitment timing. The
serial-force stress fixture contains no
preferred permutation and grants no correctness credit for agreement with the
Burri conjecture.

## Files

- `schemas/` — five portable JSON Schema contracts.
- `eub_core.py` — semantic validation, deterministic generation, scoring, and
  freeze custody.
- `adapters.py` — recorded, Anthropic Messages, and OpenAI-compatible adapters.
- `custodian.py` — one-shot private held-out scoring membrane and redacted receipt.
- `CUSTODIAN_INTERFACE.md` — independent-custody operating boundary.
- `run_eub.py` — CLI.
- `fixtures/dev/` — public development world with published truth.
- `fixtures/stress/` — force-permutation restraint test.
- `prompts/conditions.json` — the five matched elicitation arms.
- `recorded_responses/` — offline test responses only.
- `tests/` — standard-library acceptance tests.
- `FREEZE_MANIFEST.json` — deterministic payload hashes; excludes itself.
