---
rosetta:
  canonical_phrase: "Kintsugi A0 immutable execution lock (2026-07-12) — freezes the A0 baseline at 26e616e and replaces live-head equality with a four-check relevance audit; a technical concurrency rule, not an approval gate."
---

# Kintsugi A0 — Immutable Execution Lock

**Date:** 2026-07-12

**Status:** Controlling concurrency rule for A0 execution

**Frozen execution base:** `26e616e651e2a87e8c85bf37db515d7fcd007b7b`

## Why this lock exists

Canonical `main` advanced from `992a838` to `26e616e` during the final A0
acceptance run. The new commit adds only receipt 120. It changes no declared A0
path, no tracked pytest test, and no protected provenance byte. A real baseline
run still returns:

```text
KIN-OK baseline collected=19 failures=5
```

Restarting the entire history for every unrelated main commit would turn the
concurrency fence into a moving-target failure. This lock freezes one clean,
audited execution base and replaces live-head equality after the freeze with a
relevance audit.

## Frozen contract

The A0 baseline contract records:

```text
baseCommit = 26e616e651e2a87e8c85bf37db515d7fcd007b7b
raw SHA-256 = 74496df660f0ca989f293c30db652b8f9aeb78beb30fa91fe249d87ee29ef69b
collected nodes = 19
allowed failures = 5
```

The protected hashes remain:

| Path | Raw SHA-256 |
|---|---|
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md` | `9cf25b80e6c252aa8d95b63ea1c7cc1ed361c05dedaea4aef72fa001f691069c` |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md` | `3d9f63df9ce8aabfa9a16ac5dd25acabf3084b75b6ad29740a61e078ecebd629` |
| `12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md` | `db794ac3e1d91b9c4d9e92ef121ef016f128a3fb518df86d11b5dc0f5a8eec1c` |

## Post-freeze drift rule

After `refs/codex/kintsugi-a0-start` is frozen at the planning commit descending
from `26e616e`, a later canonical-main advance does not automatically invalidate
A0. It triggers four checks over `26e616e..main`:

1. no declared A0 implementation path changed;
2. no tracked pytest test path changed;
3. the three protected hashes still match; and
4. the real baseline still reports the frozen 19 nodes and five failures.

If all four hold, A0 remains valid at its immutable base and the newer main
commit is recorded for the later integration/rebase boundary. If any fails,
execution stops and the baseline is re-frozen; no result is coerced back to the
old observation.

This is a technical concurrency rule, not an approval gate. It supersedes the
live-head-equality requirement in the earlier A0 plan and second concurrency
addendum after the execution ref is frozen.
