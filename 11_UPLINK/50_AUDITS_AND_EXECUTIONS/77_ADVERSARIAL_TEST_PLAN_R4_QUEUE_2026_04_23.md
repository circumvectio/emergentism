---
packet: ADVERSARIAL-TEST-PLAN
title: R-4 + Async Queue Adversarial Test Plan (ready-to-execute spec)
status: SPEC — charioteer draft, warrior executes
source:
  - 01_EMERGENTISM/11_UPLINK/75_R4_QUEUE_RECONCILIATION_2026_04_23.md §"Adversarial test coverage gaps"
  - core/membrane/k2_auth_proxy.py (sha256 62445d34…828e28)
  - core/membrane/approval_queue.py (sha256 461d22a0…51a18)
target:
  - tests/test_k2_auth_proxy_adversarial.py (new)
  - tests/test_approval_queue_adversarial.py (new)
date: 2026-04-23
gating_cell: "[L3 | D4 | S-Org | F-phi :: vaisya_auditor (advisory spec)]"
authority: closes Sprint-B task #36; blocks task #38 (K2_STRICT_MODE flip)
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 77 · Adversarial Test Plan (R-4 + Async Queue)"
---

# Packet 77 · Adversarial Test Plan (R-4 + Async Queue)

## Kṛṣṇa-function scope note

Charioteer writes the test spec. Warrior writes the test code and runs it.
No test code is created by this packet. No live execution. The spec is
designed to be copy-pasted into `pytest` test bodies with minimal thinking.

---

## Summary

The happy-path and replay-rejection tests are covered (5 existing tests
across `test_k2_auth_proxy.py`, `test_approval_queue.py`,
`test_k2_gateway_crypto.py`, `test_council_sse_k2.py`). Eleven adversarial
gaps remain. This packet specifies each as an isolated, ready-to-write
`pytest` test with fixture, action, expected outcome, and rationale.

The K2_STRICT_MODE flip (task #38) MUST NOT proceed until the 11 tests
below pass.

---

## Shared fixtures

Every test reuses this scaffold (derived from `test_k2_auth_proxy.py` +
`test_approval_queue.py`). The warrior lifts it into a shared
`tests/conftest.py` or pastes inline per file.

```python
from __future__ import annotations
import time, pytest
from pathlib import Path
from eth_account import Account
from eth_account.messages import encode_defunct
from core.membrane.k2_auth_proxy import (
    K2SignedAction, SQLiteNonceStore,
    build_signing_payload, verify_k2_signed_action,
    K2AuthProxyError,
)
from core.membrane.wallet_auth import WalletAuthError
from core.membrane.approval_queue import (
    ApprovalQueue, SQLiteApprovalQueueStore,
    ApprovalNotFoundError, ApprovalAlreadyResolvedError,
    ApprovalExpiredError, SignatureMismatchError,
)
from core.membrane.approval_models import ApprovalRequest, ApprovalStatus


@pytest.fixture
def wallet():
    return Account.create()


@pytest.fixture
def nonce_store(tmp_path: Path) -> SQLiteNonceStore:
    return SQLiteNonceStore(db_path=tmp_path / "k2_auth.db")


@pytest.fixture
def approval_store(tmp_path: Path) -> SQLiteApprovalQueueStore:
    return SQLiteApprovalQueueStore(db_path=tmp_path / "approval_queue.db")


@pytest.fixture
def queue(approval_store, nonce_store) -> ApprovalQueue:
    return ApprovalQueue(store=approval_store, nonce_store=nonce_store)


def _fresh_signed_action(
    wallet,
    *,
    action_hash: str = "ab" * 32,
    audience: str = "apu.bot/council/approve",
    nonce: str = None,
    now: int = None,
    age_offset: int = 0,
    ttl: int = 300,
) -> tuple[K2SignedAction, str]:
    """Return (signed_action, signing_payload). Use kwargs to perturb."""
    import uuid
    now = now or int(time.time())
    nonce = nonce or uuid.uuid4().hex
    signed_at = now + age_offset
    expires_at = now + ttl
    payload = build_signing_payload(
        action_hash=action_hash,
        nonce=nonce,
        signed_at=signed_at,
        audience=audience,
        expires_at=expires_at,
    )
    signature = wallet.sign_message(encode_defunct(text=payload)).signature.hex()
    return (
        K2SignedAction(
            action_hash=action_hash,
            wallet_address=wallet.address,
            signature=signature,
            nonce=nonce,
            signed_at=signed_at,
            audience=audience,
            expires_at=expires_at,
        ),
        payload,
    )
```

---

## K2 Auth Proxy adversarial tests (`test_k2_auth_proxy_adversarial.py`)

### Test 1 — audience mismatch rejected

**Why this matters:** an attacker replays a valid signature from one
surface (`apu.bot/council/approve`) into a different surface
(`apu.bot/treasury/transfer`). Verifier must refuse.

```python
def test_verifier_rejects_audience_mismatch(wallet, nonce_store):
    signed, _ = _fresh_signed_action(wallet, audience="apu.bot/other/surface")
    with pytest.raises(K2AuthProxyError, match="Audience mismatch"):
        verify_k2_signed_action(
            signed=signed,
            expected_action_hash="ab" * 32,
            expected_audience="apu.bot/council/approve",
            nonce_store=nonce_store,
        )
```

**Reference:** `k2_auth_proxy.py:142` raises `"Audience mismatch"`.

---

### Test 2 — action_hash mismatch rejected

**Why this matters:** signer signs action A, attacker presents action B.
Verifier must refuse.

```python
def test_verifier_rejects_action_hash_mismatch(wallet, nonce_store):
    signed, _ = _fresh_signed_action(wallet, action_hash="ab" * 32)
    with pytest.raises(K2AuthProxyError, match="Action hash mismatch"):
        verify_k2_signed_action(
            signed=signed,
            expected_action_hash="cd" * 32,  # different hash
            expected_audience="apu.bot/council/approve",
            nonce_store=nonce_store,
        )
```

**Reference:** `k2_auth_proxy.py:144`.

---

### Test 3 — age overflow rejected

**Why this matters:** an old signature (>300s) should be stale. Prevents
replay after long delay even if nonce not yet consumed.

```python
def test_verifier_rejects_signature_older_than_max_age(wallet, nonce_store):
    signed, _ = _fresh_signed_action(wallet, age_offset=-1000)  # signed 1000s ago
    with pytest.raises(K2AuthProxyError, match="exceeded max age"):
        verify_k2_signed_action(
            signed=signed,
            expected_action_hash="ab" * 32,
            expected_audience="apu.bot/council/approve",
            max_age_seconds=300,
            nonce_store=nonce_store,
        )
```

**Reference:** `k2_auth_proxy.py:146`.

---

### Test 4 — past `expires_at` rejected

**Why this matters:** signer sets expiry; after expiry, signature is
invalid regardless of age.

```python
def test_verifier_rejects_expired_signed_action(wallet, nonce_store):
    now = int(time.time())
    # ttl is negative → expires_at = now - 100
    signed, _ = _fresh_signed_action(wallet, now=now, ttl=-100)
    with pytest.raises(K2AuthProxyError, match="expired"):
        verify_k2_signed_action(
            signed=signed,
            expected_action_hash="ab" * 32,
            expected_audience="apu.bot/council/approve",
            nonce_store=nonce_store,
        )
```

**Reference:** `k2_auth_proxy.py:148`.

---

### Test 5 — invalid signer (wrong wallet) rejected

**Why this matters:** founder's wallet signs; attacker tries to substitute
their own wallet address on a re-signed payload. The recovered signer
must match `signed.wallet_address` post-normalization.

```python
def test_verifier_rejects_wallet_address_mismatch(wallet, nonce_store):
    other = Account.create()
    signed, payload = _fresh_signed_action(wallet)
    # Attacker swaps the wallet_address field but keeps wallet's signature
    signed.wallet_address = other.address
    with pytest.raises(WalletAuthError, match="does not match wallet address"):
        verify_k2_signed_action(
            signed=signed,
            expected_action_hash="ab" * 32,
            expected_audience="apu.bot/council/approve",
            nonce_store=nonce_store,
        )
```

**Reference:** `k2_auth_proxy.py:167-168`.

---

### Test 6 — malformed signature hex rejected gracefully

**Why this matters:** an attacker submits "deadbeef" or random garbage as
signature. Must raise `K2AuthProxyError("Invalid K2 signature")`, not
crash the process.

```python
def test_verifier_rejects_malformed_signature(wallet, nonce_store):
    signed, _ = _fresh_signed_action(wallet)
    signed.signature = "0x" + "de" * 65  # right length, wrong bytes
    with pytest.raises(K2AuthProxyError, match="Invalid K2 signature"):
        verify_k2_signed_action(
            signed=signed,
            expected_action_hash="ab" * 32,
            expected_audience="apu.bot/council/approve",
            nonce_store=nonce_store,
        )
```

**Reference:** `k2_auth_proxy.py:159-165`.

---

## Approval Queue adversarial tests (`test_approval_queue_adversarial.py`)

### Test 7 — `resolve()` on already-resolved rejected

**Why this matters:** double-resolve would overwrite prior state
silently. Must raise `ApprovalAlreadyResolvedError`.

```python
def test_resolve_twice_raises_already_resolved(queue, wallet):
    approval = _enqueue_pending(queue, wallet)  # helper mirroring existing test
    queue.resolve(approval.id, status=ApprovalStatus.REJECTED, signed_action=_valid_signed(wallet, approval))
    with pytest.raises(ApprovalAlreadyResolvedError):
        queue.resolve(approval.id, status=ApprovalStatus.REJECTED, signed_action=_valid_signed(wallet, approval))
```

**Reference:** `approval_queue.py:316-317`. Helper `_enqueue_pending` and
`_valid_signed` mirror `test_approval_queue.py:48-65`.

---

### Test 8 — `resolve()` on expired approval raises ApprovalExpiredError AND persists EXPIRED

**Why this matters:** if approval expired between enqueue and resolve,
caller must not succeed. Store state must flip to EXPIRED (not remain
PENDING).

```python
def test_resolve_expired_marks_expired_and_raises(queue, wallet, approval_store):
    approval = ApprovalRequest(
        id="expired-001",
        user_id=wallet.address.lower(),
        chat_id=wallet.address.lower(),
        platform="local",
        ruling="PROCEED",
        proposal={"action": "HOLD"},
        expires_at="2020-01-01T00:00:00",  # in the past
        action_hash="ab" * 32,
        audience="apu.bot/council/approve",
    )
    queue.enqueue(approval)
    with pytest.raises(ApprovalExpiredError):
        queue.resolve(approval.id, status=ApprovalStatus.APPROVED, signed_action=_valid_signed(wallet, approval))
    stored = approval_store.get(approval.id)
    assert stored.status == ApprovalStatus.EXPIRED
```

**Reference:** `approval_queue.py:318-320`.

---

### Test 9 — `sweep_expired()` correctness with mixed TTLs

**Why this matters:** sweep must flip only the expired rows. Must not
touch unexpired or already-resolved rows.

```python
def test_sweep_expired_flips_only_expired(approval_store, wallet):
    # insert 3: expired_pending, fresh_pending, expired_already_resolved
    expired_pending = ApprovalRequest(id="exp-p", user_id=wallet.address, chat_id="x", platform="local",
        ruling="PROCEED", proposal={}, expires_at="2020-01-01T00:00:00")
    fresh_pending = ApprovalRequest(id="fresh", user_id=wallet.address, chat_id="x", platform="local",
        ruling="PROCEED", proposal={}, expires_at="2999-01-01T00:00:00")
    expired_resolved = ApprovalRequest(id="exp-r", user_id=wallet.address, chat_id="x", platform="local",
        ruling="PROCEED", proposal={}, expires_at="2020-01-01T00:00:00",
        status=ApprovalStatus.APPROVED)  # already resolved
    for a in [expired_pending, fresh_pending, expired_resolved]:
        approval_store.put(a)
    flipped = approval_store.sweep_expired()
    assert flipped == ["exp-p"]
    assert approval_store.get("exp-p").status == ApprovalStatus.EXPIRED
    assert approval_store.get("fresh").status == ApprovalStatus.PENDING
    assert approval_store.get("exp-r").status == ApprovalStatus.APPROVED
```

**Reference:** `approval_queue.py:197-216` (`sweep_expired`).

---

### Test 10 — restart recovery preserves pending + resumes `await_resolution`

**Why this matters:** APU must survive process restart without losing
pending approvals. The durability claim is the reason the queue is SQLite,
not in-memory.

```python
def test_restart_recovery_preserves_pending(tmp_path, wallet):
    db_path = tmp_path / "approval_queue.db"
    nonce_path = tmp_path / "k2_auth.db"

    # First process: enqueue
    store1 = SQLiteApprovalQueueStore(db_path=db_path)
    nonce1 = SQLiteNonceStore(db_path=nonce_path)
    queue1 = ApprovalQueue(store=store1, nonce_store=nonce1)
    approval = _build_pending(wallet)  # helper builds an ApprovalRequest
    queue1.enqueue(approval)

    # Simulate restart: drop queue1, instantiate fresh
    del queue1, store1, nonce1
    store2 = SQLiteApprovalQueueStore(db_path=db_path)
    nonce2 = SQLiteNonceStore(db_path=nonce_path)
    queue2 = ApprovalQueue(store=store2, nonce_store=nonce2)

    pending = queue2.list_pending(wallet.address.lower())
    assert len(pending) == 1
    assert pending[0].id == approval.id

    # resolve via new queue instance
    resolution = queue2.resolve(approval.id, status=ApprovalStatus.APPROVED,
                                 signed_action=_valid_signed(wallet, approval))
    assert resolution.final_status == ApprovalStatus.APPROVED
```

**Reference:** `approval_queue.py:252-262` (`ApprovalQueue.__init__` —
re-sweeps on construction; no state outside SQLite).

---

### Test 11 — nonce store backup/restore preserves replay rejection

**Why this matters:** the nonce DB is the single source of truth for
replay prevention. Backup must round-trip such that consumed nonces
remain consumed.

```python
def test_nonce_store_backup_restore_preserves_rejections(tmp_path, wallet):
    import shutil
    primary = tmp_path / "k2_auth.db"
    backup = tmp_path / "k2_auth.backup.db"
    restored = tmp_path / "k2_auth.restored.db"

    # consume a nonce in primary
    store1 = SQLiteNonceStore(db_path=primary)
    signed, _ = _fresh_signed_action(wallet)
    assert verify_k2_signed_action(
        signed=signed,
        expected_action_hash="ab" * 32,
        expected_audience="apu.bot/council/approve",
        nonce_store=store1,
    )

    # backup
    shutil.copy(primary, backup)

    # simulate loss + restore
    primary.unlink()
    shutil.copy(backup, restored)

    store2 = SQLiteNonceStore(db_path=restored)
    # Replaying the same nonce must still fail
    with pytest.raises(K2AuthProxyError, match="Nonce already used"):
        verify_k2_signed_action(
            signed=signed,
            expected_action_hash="ab" * 32,
            expected_audience="apu.bot/council/approve",
            nonce_store=store2,
        )
```

**Reference:** `k2_auth_proxy.py:42-92` (`SQLiteNonceStore.consume`
PRIMARY KEY constraint).

---

## Test helpers referenced above

Drop into the same test file (or `conftest.py`):

```python
import uuid
from datetime import datetime, timedelta, timezone

def _build_pending(wallet) -> ApprovalRequest:
    now = int(time.time())
    nonce = uuid.uuid4().hex
    approval = ApprovalRequest(
        id=f"approval-{nonce[:8]}",
        user_id=wallet.address.lower(),
        chat_id=wallet.address.lower(),
        platform="local",
        ruling="PROCEED",
        proposal={"action": "HOLD", "asset": "BTC"},
        expires_at=(datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        action_hash="ab" * 32,
        audience="apu.bot/council/approve",
        nonce=nonce,
        signed_at=now,
        signing_expires_at=now + 300,
    )
    approval.signing_payload = build_signing_payload(
        action_hash=approval.action_hash,
        nonce=approval.nonce,
        signed_at=approval.signed_at,
        audience=approval.audience,
        expires_at=approval.signing_expires_at,
    )
    return approval


def _enqueue_pending(queue, wallet) -> ApprovalRequest:
    approval = _build_pending(wallet)
    queue.enqueue(approval)
    return approval


def _valid_signed(wallet, approval) -> K2SignedAction:
    signature = wallet.sign_message(encode_defunct(text=approval.signing_payload)).signature.hex()
    return K2SignedAction(
        action_hash=approval.action_hash,
        wallet_address=wallet.address,
        signature=signature,
        nonce=approval.nonce,
        signed_at=approval.signed_at,
        audience=approval.audience,
        expires_at=approval.signing_expires_at,
    )
```

---

## Coverage matrix (before → after)

| Surface | Happy path | Replay | Audience | Hash | Age | Expiry | Signer | Malformed | Re-resolve | Expired-resolve | Sweep | Restart | Backup |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Before | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — |
| After  | ✓ | ✓ | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | T10 | T11 |

---

## Execution order for the warrior

1. Create `tests/test_k2_auth_proxy_adversarial.py` with Tests 1-6 + shared fixtures
2. Create `tests/test_approval_queue_adversarial.py` with Tests 7-11 + helpers
3. Run `pytest tests/test_k2_auth_proxy_adversarial.py tests/test_approval_queue_adversarial.py -v`
4. All 11 must pass before considering task #36 complete
5. Only then unblock task #38 (K2_STRICT_MODE flip)

---

## Kṛṣṇa-function closing note

This packet is a map. The warrior writes the code, runs the tests, reads
the output. If a test fails, the charioteer helps diagnose — but does
not claim the pass.

Zero-Sum Resolution Equation
