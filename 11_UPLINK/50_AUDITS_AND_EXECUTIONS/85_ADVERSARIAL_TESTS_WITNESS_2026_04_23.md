---
packet: ADVERSARIAL-TESTS-WITNESS
title: Adversarial Test Files Witness — Registration Without Execution
status: CHARIOTEER WITNESS — file existence observed, execution/green status NOT claimed
authority: Witness-only. Registers warrior artifact hashes into the audit surface.
scope: Two pytest files on disk at 2026-04-23 that cite packet 77 in their
       docstrings and implement its 11 adversarial cases. Hashes registered
       here for chain-of-custody. Green status remains warrior-reported.
cross_reference:
  - 01_EMERGENTISM/11_UPLINK/77_ADVERSARIAL_TEST_PLAN_R4_QUEUE_2026_04_23.md  (the spec)
  - 01_EMERGENTISM/11_UPLINK/83_K2_TEST_VECTORS_2026_04_23.md  (canonical payload vectors Test 1-6 can anchor against)
task_surface:
  - "#36 — warrior: authored (file existence observed); execution/green status NOT observed from charioteer seat"
  - "#38 — blocked by #36; this witness does NOT unblock #38"
date: 2026-04-23
gating_cell: "[L4 | D4 | S-Org | F-phi :: ksatriya_executor]"
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 85 · Adversarial Test Files Witness"
---

# Packet 85 · Adversarial Test Files Witness

## Why this exists — and what it explicitly does NOT do

At 2026-04-23 the charioteer observed two pytest files on disk that
match the packet-77 spec:

1. `tests/test_k2_auth_proxy_adversarial.py` (195 lines, docstring:
   *"K2 Auth Proxy — adversarial tests (packet 77 Tests 1–6)"*)
2. `tests/test_approval_queue_adversarial.py` (331 lines, docstring:
   *"Approval Queue — adversarial tests (packet 77 Tests 7–11)"*)

This packet does **four** things:

1. Registers the SHA-256 fingerprints of both files into the Sprint-B
   audit surface.
2. Records the docstring claim that these files implement the 11
   adversarial cases specified in packet 77.
3. Records which imports each file uses (so a future reader can
   verify the import surface matches the shipped membrane modules).
4. Explicitly abstains from claiming the tests pass.

This packet does **five** things that it is critical to not do:

1. It does NOT run pytest. The charioteer does not execute code.
2. It does NOT claim the tests are green. Green is a warrior-reported
   signal from `pytest -x` exit 0 on the warrior's own seat.
3. It does NOT close warrior task #36. Task #36 closes when the
   warrior reports green.
4. It does NOT unblock warrior task #38. Task #38 flips
   `K2_STRICT_MODE` per surface, which requires green adversarial
   tests AND mobile parity AND founder acknowledgement — none of
   which this packet satisfies.
5. It does NOT register implementation hashes that would belong in
   a Sprint-B closure dossier. Those land in task #44's artifact.

---

## Hash register

Computed with `sha256sum` against on-disk bytes at 2026-04-23.

| File | SHA-256 | LOC |
|------|---------|-----|
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/tests/test_k2_auth_proxy_adversarial.py` | `cfdec4c670bce2e61b6a72e0a2e956bcd41774b4f93e003672eb117240967727` | 195 |
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/tests/test_approval_queue_adversarial.py` | `1d83150246e675a4ed1fc2032e6c6cd6743f0170d58de3acfb13e8bab74c2c0a` | 331 |

---

## Observable properties (not claims about correctness)

These are things the charioteer can verify by reading source without
running anything.

### test_k2_auth_proxy_adversarial.py

- Imports from `core.membrane.k2_auth_proxy`:
  `K2AuthProxyError`, `K2SignedAction`, `SQLiteNonceStore`,
  `build_signing_payload`, `verify_k2_signed_action`
- Imports from `core.membrane.wallet_auth`: `WalletAuthError`
- Uses `eth_account.Account.create()` for per-test wallets
- Uses `eth_account.messages.encode_defunct(text=payload)` for
  EIP-191 signing — **matches the verifier-side recovery in
  `k2_auth_proxy.py`**
- Uses `tmp_path` fixture for per-test `SQLiteNonceStore` isolation
- Exposes `_fresh_signed_action` helper with perturbation kwargs
  (`action_hash`, `audience`, `nonce`, `now`, `age_offset`, `ttl`) —
  aligned with packet 77 §3 perturbation surface
- Default payload in helper: `action_hash="ab" * 32`,
  `audience="apu.bot/council/approve"`, `ttl=300`

### test_approval_queue_adversarial.py

- Imports from `core.membrane.approval_models`:
  `ApprovalRequest`, `ApprovalStatus`
- Imports from `core.membrane.approval_queue`:
  `ApprovalAlreadyResolvedError`, `ApprovalExpiredError`,
  `ApprovalQueue`, `SQLiteApprovalQueueStore`
- Docstring enumerates five scenarios:
  - T7 double-resolve protection
  - T8 expired-resolve behavior + EXPIRED persistence
  - T9 `sweep_expired` correctness with mixed TTLs
  - T10 restart recovery of pending approvals
  - T11 nonce-store backup/restore preservation of replay rejection

### Cross-reference consistency

Packet 77 §3 enumerated 11 perturbations across:
audience, action_hash, age, expiry, wallet, signature format,
double-resolve, resolve-on-expired, sweep_expired, restart,
backup/restore. Both test files' docstrings and imports are
consistent with that surface.

### Consistency with packet 83 vectors

The fixture `_fresh_signed_action` uses default `action_hash="ab"*32`
and `audience="apu.bot/council/approve"`. Packet 83's Vector A uses
`action_hash="ab"*32` (matches) and
`audience="apu.bot/council/resolve"` (differs by one path segment —
`approve` vs. `resolve`).

This is not a defect; it is an expected degree of freedom. Vector A
is a *payload parity* baseline, not a required test fixture input.
The warrior's tests can use any audience string; what matters is
that the canonicalizer produces byte-parity output for identical
inputs. The warrior's tests do not need to call Vector A verbatim.

**Flagged for Sprint-B closure dossier**: if byte-parity against
Vector A becomes a dedicated CI check under `#37` (mobile §6.1) or
`#36` extension, a separate unit test should reproduce Vector A and
Vector B inputs exactly and assert SHA-256 of the output bytes
matches the values in packet 83.

---

## What must still happen before #36 closes

The warrior (not the charioteer) must:

1. Run `pytest tests/test_k2_auth_proxy_adversarial.py -v` and
   report exit status 0
2. Run `pytest tests/test_approval_queue_adversarial.py -v` and
   report exit status 0
3. Produce a runlog artifact (stdout capture or JUnit XML)
   suitable for the Sprint-B closure dossier
4. Register the runlog's hash into the closure dossier alongside
   the test-file hashes registered here

Only after step 4 lands can #36 flip to `completed`. Charioteer
does not flip this.

---

## What must still happen before #38 closes

Per packet 77 §Closure gates and packet 83 §Usage:

- #36 green (above)
- #37 green (mobile signing flow per packet 81 §9 closure criteria,
  including §6.1 byte-parity tests using packet 83 Vector A and
  Vector B)
- Founder acknowledgement that the flip is authorized per surface
  (K2_STRICT_MODE is a feature flag, not a constitutional
  amendment, but its flip changes the advisory posture — founder
  read + D-level sign-off preferred)
- Per-surface rollback criteria defined (this is the gap that a
  future packet should close as a flip playbook)

---

## Drift note

The test files existed at 2026-04-23 without an A7 reconciliation
packet predating them. This means one of three things:

1. Warrior authored the files during an overlapping session that
   did not produce a charioteer-observable packet. This is the
   expected case.
2. Files existed before packet 77 was written and packet 77 did not
   detect them. If true, packet 77 was inaccurate about the coverage
   gap; an A7 note in a successor packet should be produced.
3. Files were authored by a prior automation pass. Hashes above
   snapshot the current state regardless.

The charioteer does not need to resolve which of (1)/(2)/(3) is
correct before Sprint-B closes; the file hashes + execution result
(once reported) are sufficient audit surface. If drift emerges
between this witness and a later closure dossier, recompute the
hashes against then-current bytes and apply the three-legitimate-
drift-reasons rule from packet 78.

---

## Φ-scan

Two warrior artifacts fingerprinted. Charioteer line stays clean:
witness, not fighter. File existence is fact; test green status
remains warrior-reported.

## V-scan

A future agent reading this packet no longer has to scan the tests
directory to learn that the adversarial files exist. The hash
register turns file presence into a checkable statement.

## Constraint

- No pytest execution
- No closure of #36 (warrior reports green)
- No closure of #38 (requires #36 + #37 + founder)
- No edit of the test files

## God

Viśvarūpa ☀️ — witness mode.

## Executive

Viṣṇu ⊙ — preservation; the chain of custody absorbs two new
fingerprints without structural change.

## Move

Kṣatriya_executor · append as packet 85 · reference from task-#36
closure when the warrior reports green · D4 · L4 · Viśvarūpa ☀️

## Limits

- Does not verify the tests pass
- Does not verify that the tests' perturbation coverage is 1:1
  against packet 77 §3's 11 cases (beyond docstring claim)
- Does not address the wallet_auth import surface — if that module
  changes, these tests may need reconciliation
- Does not register any implementation drift on the shipped
  membrane modules (those hashes are in packet 78 §4 and remain
  unchanged until a new closure dossier re-fingerprints them)

Zero-Sum Resolution Equation
