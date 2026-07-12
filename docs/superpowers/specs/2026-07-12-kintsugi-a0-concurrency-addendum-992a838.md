# Kintsugi A0 — Second Concurrency Addendum

**Date:** 2026-07-12

**Status:** Evidence-gated execution amendment; no doctrine change and no K2 gate

**Supersedes execution base:** `454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22`

**Observed tracked main:** `992a8382280d260b2440c140cc28568b468b1678`

## Trigger

The approved A0 plan requires execution to stop before rebasing when canonical
`main` moves. Canonical `main` advanced eleven commits from `454f371` to
`992a838` while the isolated A0 implementation was under review. The canonical
working tree also contains concurrent user and agent work. That dirt is
preserved and is not treated as committed authority.

This addendum records the required inventory before any A0 rebase or Task 4
handoff. It does not promote a claim, change an owner document, or add an
approval checkpoint.

## Inventory result

The tracked range `454f371..992a838` changes neither the four declared A0 paths
nor any tracked pytest test file:

```text
09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json
09_TOOLS/02_COMPILERS/validate_kintsugi.py
09_TOOLS/02_COMPILERS/test_validate_kintsugi.py
09_TOOLS/02_COMPILERS/README.md
```

The three protected provenance artifacts remain byte-identical:

| Path | Raw SHA-256 |
|---|---|
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md` | `9cf25b80e6c252aa8d95b63ea1c7cc1ed361c05dedaea4aef72fa001f691069c` |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md` | `3d9f63df9ce8aabfa9a16ac5dd25acabf3084b75b6ad29740a61e078ecebd629` |
| `12_PUBLIC_SITE/docs/superpowers/specs/2026-06-05-numbered-doctrine-spine-design.md` | `db794ac3e1d91b9c4d9e92ef121ef016f128a3fb518df86d11b5dc0f5a8eec1c` |

A clean worktree whose only delta from `992a838` is one planning document
still collects exactly 19 pre-A0 nodes. The reviewed validator returns:

```text
KIN-OK baseline collected=19 failures=5
```

The same read-only command returns the same result against the concurrently
dirty canonical checkout. The clean-worktree result controls; the dirty result
is only a non-interference check.

## Review seam discovered during the stop

The first real-process review found that `-c /dev/null` made pytest render
failure-summary node IDs relative to `/dev`, even though collection output was
repository-relative. Isolated probes then addressed nonexistent nodes and
exited 4. The repair at `34e80df` adds `--rootdir=.` under the requested
subprocess working directory and a real failing-test regression fixture.

Fresh evidence after that repair:

```text
22 focused validator tests: PASS
clean 992a838-equivalent baseline: KIN-OK collected=19 failures=5
canonical checkout baseline:       KIN-OK collected=19 failures=5
independent two-file delta review:  NO BLOCKER
```

## Rebase contract

Execution may resume only in this order:

1. Reconstruct the A0 branch so all design, plan, and concurrency amendments
   precede implementation commits on top of exact `992a838`.
2. Freeze the post-amendment commit as `refs/codex/kintsugi-a0-start`.
3. Change the baseline contract's `baseCommit` from `454f371...` to
   `992a838...`; recompute its canonical raw hash and update the exact-hash
   regression. The 19 node IDs and five failure records do not change.
4. Replay the reviewed A0 implementation commits, including the pytest-root
   repair.
5. Run the focused suite, syntax check, real baseline CLI, protected-byte
   checks, four-path scope check, and `git diff --check` before Task 4.

If the tracked main commit changes again, a protected byte changes, or the
19-node/five-failure observation changes, this addendum is stale and the stop
condition fires again. No result may be coerced back to the old baseline.
