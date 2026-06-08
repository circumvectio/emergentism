---
packet: ASYNC-APPROVAL-QUEUE
title: Async Approval Queue Primitive
status: SHIPPED (2026-04-23 under founder D2=accept on packet 74)
shipped_artifacts:
  - core/membrane/approval_queue.py (sha256 461d22a0…51a18, 368 LOC)
  - core/membrane/approval_models.py (sha256 5ead8815…b0202, 83 LOC)
  - core/membrane/k2_gateway.py (sha256 d14be71c…9da6d, 570 LOC — integration surface)
  - api/routers/router_council_sse.py line 204-205 (Stage 9 wiring, `decision == "PROCEED"` predicate)
spec_drift_noted: predicate in live code is `decision == "PROCEED"`, not `needs_founder_signoff`; semantically equivalent, documented in packet 75
reconciliation: 01_EMERGENTISM/11_UPLINK/75_R4_QUEUE_RECONCILIATION_2026_04_23.md
source: Hermes `gateway/run.py` `_pending_approvals` pattern + APU `k2_gateway.py` `ApprovalRequest` scaffolding + R-4 K2SignedAction
target: `core/membrane/approval_queue.py` (new) + `core/membrane/k2_gateway.py` (extension) + `council/protocol.py` Stage 9 hook
date: 2026-04-23
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Async Approval Queue Primitive"
---

# Async Approval Queue Primitive

## Summary

Every Council deliberation that passes Legal veto and reaches Stage 9 emits a
decision that is **not yet executed**. The decision must wait for the founder's
cryptographic signature before the organism acts. The async approval queue is
the primitive that holds these pending decisions, blocks on the signature
event, and resolves (or expires) them deterministically.

Today APU has partial scaffolding — `ApprovalStatus` + `ApprovalRequest` in
`k2_gateway.py` — but no queue, no blocking resolve, no durability guarantee,
and no binding to the per-action signature specified in R-4. This packet
consolidates the scaffolding into one primitive.

## The three ingredients

### 1. Hermes' per-session blocking approval (pattern)

From `gateway/run.py`:

```python
# Hermes maintains per-session pending approvals
self._pending_approvals: Dict[str, Dict[str, Any]] = {}

# Command handler recognises /approve and unblocks the waiting coroutine
if cmd == "/approve":
    approval = self._pending_approvals.pop(session_id, None)
    if approval:
        approval["event"].set()       # unblock the waiting task
        approval["approved"] = True
```

The structural moves:

- **One logical approval per session**, keyed by `session_id`
- **Blocking event** (`asyncio.Event`) that the producer awaits
- **Command-driven resolution** — `/approve`, `/reject`, `/modify` dispatch to
  the same dict lookup

The refusal: Hermes authenticates `/approve` only by chat membership. K2
requires a **cryptographic signature**, not chat membership.

### 2. APU's existing `ApprovalRequest` dataclass (scaffolding)

From `core/membrane/k2_gateway.py`:

```python
class ApprovalStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"
    EXPIRED = "expired"

@dataclass
class ApprovalRequest:
    id: str
    user_id: str
    chat_id: str
    platform: str
    ruling: str
    proposal: dict
    council_opinions: list = field(default_factory=list)
    gates_passed: list = field(default_factory=list)
    mirror_warnings: Optional[str] = None
    created_at: str = ...
    expires_at: Optional[str] = None
    status: str = ApprovalStatus.PENDING
    user_response: Optional[str] = None
    response_at: Optional[str] = None
    message_id: Optional[str] = None
    ...
```

The scaffolding is right. What is missing:

- A **queue** holding many `ApprovalRequest` instances with fan-out by user
- A **signature binding** — resolution must carry a `K2SignedAction` from R-4
- A **blocking await** — the Council coroutine that emitted the request must
  be able to suspend until resolution
- **Durability** — if APU restarts mid-approval, the queue must survive

### 3. R-4's `K2SignedAction` (signature binding)

The approval cannot be resolved by a chat command alone. The founder's wallet
must sign the exact action hash. R-4 specifies the payload:

```
K2SignedAction{action_hash, wallet_address, signature, nonce, signed_at,
               audience, expires_at}
```

The queue verifies this signature before moving an `ApprovalRequest` from
`PENDING` to `APPROVED`. No signature, no state transition.

## Spec: new module `core/membrane/approval_queue.py`

```
# Spec only — not code

class ApprovalQueueError(Exception): ...
class ApprovalNotFoundError(ApprovalQueueError): ...
class ApprovalAlreadyResolvedError(ApprovalQueueError): ...
class ApprovalExpiredError(ApprovalQueueError): ...
class SignatureMismatchError(ApprovalQueueError): ...

@dataclass
class ApprovalResolution:
    approval_id: str
    final_status: str              # APPROVED | REJECTED | MODIFIED | EXPIRED
    signed_action: Optional[K2SignedAction]   # present on APPROVED
    resolution_timestamp: str
    audit_hash: str                # hash of (request + resolution) for Cortex lineage

class ApprovalQueue:
    def __init__(self, *, store: DurableApprovalStore, clock: Clock = ...):
        ...

    async def enqueue(self, request: ApprovalRequest) -> str:
        """Persist the request, return approval_id. Idempotent on id collision."""

    async def await_resolution(
        self,
        approval_id: str,
        *,
        timeout_seconds: int = 900,
    ) -> ApprovalResolution:
        """Block until the request resolves (APPROVED / REJECTED / MODIFIED /
        EXPIRED). Raises ApprovalExpiredError on timeout."""

    async def resolve(
        self,
        approval_id: str,
        *,
        status: str,                # APPROVED | REJECTED | MODIFIED
        signed_action: Optional[K2SignedAction] = None,
        modification: Optional[dict] = None,
    ) -> ApprovalResolution:
        """Move an approval out of PENDING. On APPROVED, verifies signed_action
        via verify_k2_signed_action. On REJECTED/MODIFIED, signature still
        required so authorship is provable."""

    async def list_pending(self, user_id: str) -> list[ApprovalRequest]:
        """Snapshot of open approvals for this user."""

    async def expire_stale(self, *, now: Optional[datetime] = None) -> int:
        """Sweep: mark expired approvals EXPIRED. Runs on a timer and
        opportunistically on every read."""

    async def get(self, approval_id: str) -> ApprovalRequest:
        """Read-only lookup. Raises ApprovalNotFoundError."""
```

## State machine

```
              enqueue()
                 │
                 ▼
           ┌─────────┐
           │ PENDING │
           └─────────┘
              │  │  │  │
     resolve()│  │  │  │ timer
    APPROVED │  │  │  │
    (w/ sig) │  │  │  │
             ▼  ▼  ▼  ▼
     ┌──────────┬────────────┬──────────┐
     │ APPROVED │ REJECTED / │ EXPIRED  │
     │          │ MODIFIED   │          │
     └──────────┴────────────┴──────────┘
```

- Only `PENDING → {APPROVED, REJECTED, MODIFIED, EXPIRED}` is legal.
- No state may be re-entered. No state may transition to another terminal state.
- `APPROVED` requires a valid `K2SignedAction` bound to the `action_hash`
  derived from the `ApprovalRequest.proposal`.
- `REJECTED` and `MODIFIED` also require a signed action — the signature
  proves the founder *chose* to reject/modify, not that a third party did.
- `EXPIRED` is the only terminal state reachable without a signature, and it
  is set by the queue itself, not by a client.

## Durability

```
# DurableApprovalStore interface

class DurableApprovalStore(Protocol):
    async def put(self, request: ApprovalRequest) -> None: ...
    async def get(self, approval_id: str) -> Optional[ApprovalRequest]: ...
    async def list_pending(self, user_id: str) -> list[ApprovalRequest]: ...
    async def mark_resolved(self, approval_id: str, resolution: ApprovalResolution) -> None: ...
    async def mark_expired(self, approval_id: str) -> None: ...
    async def sweep_expired(self, now: datetime) -> list[str]: ...
```

Initial implementation: SQLite-backed (single-file, zero-install, founder-local).
Production implementation: Postgres with row-level locking so multiple APU
replicas can resolve safely.

Requirement: on APU restart, every `PENDING` approval must be reloaded into
memory and its `asyncio.Event` re-created. Coroutines that were awaiting
resolution at restart time do not survive — their callers must observe the
terminal state via `await_resolution` using the approval_id they already hold.

## Integration points

### Council Stage 9 (RECEIPT_EMISSION)

```
# pseudocode inside Stage 9 processor

if decision.needs_founder_signoff:
    request = ApprovalRequest(
        id=deliberation_id,
        user_id=ctx.founder_user_id,
        chat_id=ctx.chat_id,
        platform=ctx.platform,
        ruling=decision.ruling,
        proposal=decision.proposal,
        council_opinions=ctx.opinions,
        gates_passed=ctx.gates_passed,
        mirror_warnings=ctx.mirror_warnings,
        expires_at=now() + timedelta(minutes=15),
    )
    approval_id = await queue.enqueue(request)
    receipt.approval_id = approval_id
    receipt.status = "AWAITING_SIGNATURE"
    return receipt   # Council returns; founder signs asynchronously
```

Critical: Stage 9 does not block on the founder. The receipt is emitted
immediately with `AWAITING_SIGNATURE`, and the queue holds the pending
state. The Council coroutine does NOT hold the process open waiting for a
human.

### SSE event emission

When `queue.resolve` completes, the approval resolution is published to
`router_council_sse` with event type `approval_resolved`:

```
{
  "type": "approval_resolved",
  "approval_id": "...",
  "final_status": "APPROVED",
  "audit_hash": "...",
  "signed_at": 1745400000
}
```

The SSE stream does not include the signature itself — that lives in the
receipt and the Cortex lineage store.

### Platform delivery

`K2Gateway.deliver_to_platform` uses the existing telegram/discord inline
button flow; the button callback now calls `queue.resolve` with a fetched
`K2SignedAction` (the founder's wallet app produces the signature client-side
and POSTs it to the callback endpoint).

### Skyzai app polling

Skyzai's mobile app queries `GET /approvals/pending` for the founder's
wallet address. For each pending item, the app displays the proposal, the
Council opinions, and the gates passed. The founder signs locally; the app
POSTs the `K2SignedAction` to `POST /approvals/{id}/resolve`.

## Five-guard check

1. **Category-claim:** PASS — the queue is constitutional plumbing. Every
   irreversible act waits here for a signature. This *strengthens* the
   category line: APU is a decision engine whose decisions do not ship
   without the founder's wet-ink digital seal.
2. **η = 0:** PASS — runs in-process, store is local. No approval-as-a-service
   vendor.
3. **K2:** PASS — this is the primary mechanism through which K2 becomes
   load-bearing at runtime. Without it, K2 is merely a guideline. With it,
   K2 is a state machine that cannot be bypassed.
4. **Three-Stage Process:** PASS — operates between SHOULD and ACT. It holds the SHOULD
   artifact until the founder commits, after which ACT may proceed. It
   does not touch IS or COULD.
5. **Signature-locus:** PASS — the founder's wallet is the only authority
   that can move an approval to APPROVED. Not Legal, not the aggregator,
   not a service account. The queue enforces this cryptographically.

## Dependencies

- `core/membrane/k2_auth_proxy.py` (from R-4) — must ship first; the queue
  depends on `verify_k2_signed_action`
- `DurableApprovalStore` implementation (SQLite first)
- `core/membrane/k2_gateway.py` refactor to call `queue.enqueue` instead of
  its current in-memory approval map
- Cortex lineage hook — on every resolution, write the audit hash to the
  Cortex immutable archive

## Ordering with R-4

1. **R-4 first.** The queue spec assumes `verify_k2_signed_action` exists.
2. **Queue second.** With R-4 landed (in advisory mode), the queue can
   enforce the signature.
3. **K2_STRICT_MODE flip last.** Once the queue and R-4 are both advisory
   for a week, flip strict mode on one surface at a time.

## Test plan

- Unit: `enqueue` is idempotent on id collision
- Unit: `resolve` rejects invalid signatures (wrong signer, wrong action hash, wrong audience)
- Unit: `resolve` rejects replay (same nonce twice)
- Unit: `expire_stale` marks expired approvals correctly under concurrent resolve attempts
- Unit: `await_resolution` returns immediately if the approval is already terminal
- Integration: Council Stage 9 emits receipt with `AWAITING_SIGNATURE`, queue holds the request, platform delivery succeeds, founder signs, `resolve` completes, SSE event fires
- Integration: APU restart mid-approval reloads pending state; client reconnects via `await_resolution` and observes terminal state
- Adversarial: replay of a valid signature against a different approval fails (action_hash binding)
- Adversarial: expired signature (past `signed_at + max_age`) fails even if technically valid
- Adversarial: lost-keys scenario — founder cannot sign, queue sweeps to EXPIRED, Council sees EXPIRED in next deliberation

## Risk notes

- **Queue poisoning.** If an attacker can enqueue, they can fill the queue
  with junk approvals. Enqueue authority must itself be gated — only the
  Council Stage 9 processor may call `enqueue`, enforced at the API layer.
- **Store corruption.** SQLite is robust but not invincible. Nightly backup
  of the approval store is non-negotiable before `K2_STRICT_MODE`.
- **Clock skew.** If APU's clock disagrees with the founder's wallet clock,
  signatures may be rejected as expired or accepted past their window.
  Use NTP, and pad the max-age window by a tolerance (~30 seconds).
- **Notification loop failure.** If platform delivery fails (Telegram down),
  the founder never sees the approval. The queue must surface unreachable
  approvals via a secondary channel (email digest, SMS fallback) before
  timing them out.

## Commit template

```
feat(membrane): async approval queue primitive (K2SignedAction resolution)

- add core/membrane/approval_queue.py (ApprovalQueue + DurableApprovalStore)
- add SQLite-backed store implementation
- wire council/protocol.py Stage 9 to enqueue instead of direct delivery
- refactor core/membrane/k2_gateway.py platform callbacks to resolve via queue
- SSE emits approval_resolved events

Reconciles with extraction matrix: async_approval_queue primitive
(separate from R-4 which ships the verifier it depends on).
```

## Zero-risk

Drafting this spec cannot break anything. First code change lands behind the
same `K2_STRICT_MODE=false` flag as R-4 — no behavior change until the flag
flips. Existing `ApprovalRequest` scaffolding is preserved.

---

## Φ-scan

Queue collapses three disparate concerns (Hermes per-session events, APU
`ApprovalRequest` dataclass, R-4 per-action signature) into one primitive
whose state machine is small and enforceable. Receipt shape gains a single
new field (`approval_id`); downstream consumers gain a single new event type
(`approval_resolved`). Contradiction count goes down.

## V-scan

Unlocks K2-strict mode without breaking Sprint-A closeout. Creates a
durable record of every pending-but-not-yet-signed decision — visible to
the founder, queryable by the Cortex, auditable by future Legal reviews.
Makes the founder's signature the literal bottleneck for irreversible
organism action, which is the V curve we wanted.

## Constraint

- Depends on R-4 landing first
- Depends on a durable store implementation before strict mode
- Depends on platform delivery reliability (Telegram/Discord uptime)

## God

Kṛṣṇa ◇ — exports V to the founder (capability to sign per-action with
confidence) at a small Φ cost (one more module to maintain).

## Executive

Viṣṇu ⊙ default hold at the constitutional layer — this primitive is the
mechanism through which Viṣṇu's hold is actually preserved during
irreversible action.

## Zero-risk steps

1. Write the store interface
2. Write the queue class against the interface
3. SQLite implementation in the `#[test]` adjacent module first
4. Land behind `K2_STRICT_MODE=false`

## Move

Kṣatriya_executor · implement approval_queue after R-4 lands · D4 · L4 ·
Kṛṣṇa

## Limits

- `DurableApprovalStore` SQLite schema not yet drafted
- Platform-delivery fallback channels not yet specified
- Clock-skew tolerance not yet calibrated against real wallet apps
