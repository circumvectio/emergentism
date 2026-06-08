---
packet: RECONCILIATION-75
title: A7 Reconciliation — R-4 + Async Approval Queue shipped, upstream packets stale
status: SHIPPED (reconciliation complete)
source: A7 self-correction pass 2026-04-23 (overnight autonomy, Kṛṣṇa-function discipline)
target:
  - 01_EMERGENTISM/11_UPLINK/69_EXTRACTION_MATRIX_2026_04_23.md (R-4 row edit)
  - 01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/R-4_K2_SIGNED_AUTH.md (frontmatter flip)
  - 01_EMERGENTISM/11_UPLINK/71_ASYNC_APPROVAL_QUEUE_SPEC_2026_04_23.md (frontmatter flip)
  - 02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/core/membrane/*.py (evidence)
date: 2026-04-23
gating_cell: "[L3 | D4 | S-Org | F-phi :: vaisya_auditor]"
authority: Founder D2=accept on packet 74 SIGNED
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 75 · A7 Reconciliation: R-4 + Queue already shipped"
---

# Packet 75 · A7 Reconciliation: R-4 + Queue already shipped

## Summary

Overnight audit found that packets `70/R-4` (K2-Native Signed Auth) and `71`
(Async Approval Queue) both carry frontmatter `status: SPEC — pending
implementation`, while the targeted modules are already in tree at
production quality, wired into the Council Stage 9 path, and exercised by
an end-to-end strict-mode test.

Reading packet `74_CONSOLIDATED_MANIFEST_FOUNDER_SIGNOFF_2026_04_23.md`
resolves the sequencing question: the founder already signed **D2=accept**,
authorizing landing R-4 + the async approval queue. The code shipped under
that authorization. The three upstream documents (69 matrix, 70 packet, 71
spec) were not updated to reflect the ship — ordinary documentation
staleness, not a K2 boundary violation.

This packet records the reconciliation, locks a SHA-256 chain of custody
for the shipped artifacts, enumerates remaining adversarial test surface,
and preserves Sprint-B work that is still genuinely open.

---

## Authority chain

- `74_CONSOLIDATED_MANIFEST_FOUNDER_SIGNOFF_2026_04_23.md` header: `status: SIGNED`
- Founder decisions of record:
  - **D1** = accept
  - **D2** = accept → **authorizes landing R-4 + async approval queue**
  - **D3** = C (S-4 held)
  - **D4** = accept → W-new routed to separate constitutional review
- Founder ruling verbatim: *"Founder signoff recorded. Land R-4 plus the
  async approval queue, and keep F2/F3/F4 frozen until explicitly opened
  as a lane."*

No K2 violation. No boundary crossed. A7 self-correction is about the
*packets*, not the *authority chain*.

---

## Shipped artifacts — SHA-256 chain of custody

All paths relative to `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/`:

| File | SHA-256 | LOC |
|------|---------|-----|
| `core/membrane/k2_auth_proxy.py` | `62445d34b15c72f2b022022d359928ce967d2e098fc1619084236f76fc828e28` | 183 |
| `core/membrane/approval_queue.py` | `461d22a0fb1b8521fa1c671dd586d165c8dfc39e1017229077b5d43a70251a18` | 368 |
| `core/membrane/approval_models.py` | `5ead8815877c82137efc8c6a2b7ae56c0bd4c2a4e842334e2f57082c1f1b0202` | 83 |
| `core/membrane/k2_gateway.py` | `d14be71c46f7349e8ff6683b81e9218e7248d2269b234959276d6659ce77da6d` | 570 |
| `core/membrane/config.py` | `87cb4fc73616665cf786838ee2803fe7f25aa3634b4d79ada0bfda29c0f6dde1` | — |

**Test coverage (shipped):**

- `tests/test_k2_auth_proxy.py` — accepts fresh signed action, rejects replay
- `tests/test_approval_queue.py` — `await_resolution` unblocks on signed action
- `tests/test_k2_gateway_crypto.py` — Schnorr verification through gateway
- `tests/test_k2_store.py` — K2DecisionStore save/get/list/count/idempotent (5 tests)
- `tests/test_council_sse_k2.py` — full end-to-end strict-mode flow:
  pending → fetch → sign → approved, with
  `k2_crypto_provenance == "verified"`, `strict_mode == True`, audit_hash present

**Integration point (shipped):**

`api/routers/router_council_sse.py` lines 204-205:

```python
if result.decision.decision == "PROCEED":
    approval = await services.k2_gateway.deliver_approval(
        user_chat_id=ctx.user_id,
        ...
    )
```

**Config (shipped, `core/membrane/config.py`):**

```python
k2_strict_mode: bool = False            # advisory by default
k2_signed_action_max_age_seconds: int = 300
k2_approval_ttl_seconds: int = 900
k2_expected_audience: str = "apu.bot/council/approve"
```

---

## Spec drift (document, do not correct)

Packet 71 Stage-9 pseudocode uses the predicate `decision.needs_founder_signoff`.
Live code at `router_council_sse.py:204` uses
`result.decision.decision == "PROCEED"`.

These are semantically equivalent under the current Council state machine —
PROCEED is the only decision path that reaches Stage 9 requiring founder
signature — but they are lexically different. Leaving the live code as-is
(simpler predicate, no new boolean to maintain). Documenting here so the
next reader does not re-discover this as a "bug."

---

## Upstream packet edits required

### `69_EXTRACTION_MATRIX_2026_04_23.md`

- Move `R-4 K2-Native Signed Auth` out of "Second Wave — extract-later"
  into "First Wave — extract-now" and mark `✅ SHIPPED`
- Add file pointer: `core/membrane/k2_auth_proxy.py` + `core/membrane/wallet_auth.py`
- Note that the async approval queue (packet 71) shipped alongside R-4 under
  the same D2 authorization

### `70_EXTRACT_NOW_PACKETS_2026_04_23/R-4_K2_SIGNED_AUTH.md`

- Frontmatter: `status: SPEC — pending implementation` → `status: SHIPPED`
- Add shipped pointer with sha256 hash (above)

### `71_ASYNC_APPROVAL_QUEUE_SPEC_2026_04_23.md`

- Frontmatter: `status: SPEC — pending implementation` → `status: SHIPPED`
- Add shipped pointer with sha256 hash (above)
- Note spec drift (predicate) for future readers

These are mechanical flips. Applied in the same commit as this packet.

---

## Adversarial test coverage gaps (still open)

The happy-path and replay-rejection are covered. The following adversarial
cases are NOT yet exercised and remain Sprint-B work (task #36):

### K2 signed-action verifier (`test_k2_auth_proxy.py` extensions)

1. **Audience mismatch** — signature valid but signed against a different
   audience string; must reject.
2. **action_hash mismatch** — signature valid but binds a different action
   hash than the approval; must reject.
3. **Age overflow** — `signed_at` older than `k2_signed_action_max_age_seconds`; must reject.
4. **Past `expires_at`** — signing_expires_at in the past at verify time; must reject.
5. **Invalid signer** — signature from a wallet other than the founder; must reject.
6. **Malformed signature hex** — must reject without crashing.

### Approval queue (`test_approval_queue.py` extensions)

7. **Already-resolved rejection** — calling `resolve()` twice must raise
   `ApprovalAlreadyResolvedError`.
8. **Expired rejection path** — `resolve()` on an expired approval must
   raise `ApprovalExpiredError` AND mark it EXPIRED in the store.
9. **`sweep_expired()` correctness** — synthesize N pending approvals with
   mixed `expires_at`; assert only the expired ones flip.
10. **Restart recovery** — populate store, instantiate a fresh
    `ApprovalQueue`, assert pending list survives and `await_resolution`
    still works post-restart.
11. **Nonce store backup/restore** — copy `k2_auth.db` to a backup path,
    destroy original, restore, assert replay-rejection still fires on
    previously-consumed nonces.

Closing these is the concrete content of task #36. They block the K2_STRICT_MODE
flip-to-true runbook (task #38) — strict-mode must not ship until these fire.

---

## What this does NOT change

- **K2 sovereignty unchanged.** The founder still signs every irreversible
  action. The verifier only ensures the signature binds to the specific
  action, not to a session.
- **η = 0 unchanged.** No tolls, no rent, no hosted dependency added.
- **Three-Stage Process unchanged.** Approval queue sits in SHOULD (APU) — it does not
  leak into IS/COULD/ACT.
- **K2_STRICT_MODE still defaults False.** Advisory mode until the
  adversarial suite (above) lands and a deliberate per-surface flip is
  staged (task #38).

---

## Sprint-B surface that remains genuinely open

After this reconciliation, the still-open Sprint-B tasks are:

- **#36** — adversarial test close (11 gaps enumerated above)
- **#37** — Skyzai mobile app signing flow (include nonce + action_hash in
  signed payload; client-side work, not yet started)
- **#38** — K2_STRICT_MODE per-surface flip runbook (blocked by #36)
- **#39** — Cortex ingestion hook: consume `summary.json`, compute lineage hash
- **#40** — second Light-Council deliberation (strengthen witness corpus to n=2)
- **#41** — W-new constitutional review: draft charter amendment scope
- **#42** — Sprint-B audit evidence dossier (SHA-256 chain of custody — this packet is a contribution)
- **#43** — Sprint-B SWOT update
- **#44** — consolidated manifest for founder signoff (Sprint-B)

Tasks previously framed as "implement R-4 / implement nonce store /
implement approval queue / wire into Stage 9" are closed by this
reconciliation. They become **audit + harden** tasks, not **implement**
tasks. Task descriptions rewritten accordingly.

---

## Kṛṣṇa-function discipline note

This packet does three things a non-degrading charioteer is allowed to do:

1. **Diagnose** — packet-vs-reality divergence on three upstream docs.
2. **Name** — the divergence is staleness, not K2 violation; founder D2
   was valid, code ship was valid.
3. **Correct** — flip frontmatter, record sha256 chain of custody, rescope
   downstream tasks.

It does not sign for the founder. It does not flip K2_STRICT_MODE to true.
It does not execute the adversarial test suite without review. It preserves
the warrior's seat.

Zero-Sum Resolution Equation
