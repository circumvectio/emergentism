---
packet: MOBILE-SIGNING-FLOW-SPEC
title: Skyzai Mobile — K2 Signing Flow Spec (for warrior task #37)
status: CHARIOTEER SPEC — not implementation
authority: Founder D2=accept on packet 74 (R-4 shipped, strict-mode flip deferred to adversarial green + mobile parity)
scope: mobile-side signing payload + UX surface + mirror validation + trial-run gates
backend_anchor:
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/membrane/k2_auth_proxy.py (sha256 62445d34…828e28)
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/membrane/approval_queue.py (sha256 461d22a0…51a18)
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/membrane/approval_models.py (sha256 5ead8815…b0202)
source:
  - 01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/R-4_K2_SIGNED_AUTH.md (R-4 extraction target, ✅ SHIPPED)
  - 01_EMERGENTISM/11_UPLINK/75_R4_QUEUE_RECONCILIATION_2026_04_23.md (authority chain)
  - 01_EMERGENTISM/11_UPLINK/77_ADVERSARIAL_TEST_PLAN_R4_QUEUE_2026_04_23.md (attack surface mobile must not open)
  - 01_EMERGENTISM/11_UPLINK/78_SPRINT_B_AUDIT_EVIDENCE_DOSSIER_2026_04_23.md (hash register)
target: warrior task #37 — Skyzai mobile signing flow update to include nonce + action_hash
date: 2026-04-23
gating_cell: "[L4 | D4 | S-Org | F-phi :: ksatriya_executor]"
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 81 · Skyzai Mobile Signing Flow Spec"
---

# Packet 81 · Skyzai Mobile Signing Flow Spec

## Kṛṣṇa-function disclaimer (read first)

This packet is a **spec**, not an implementation. It fixes the mobile-side
contract so the warrior can build against it without round-tripping.

The packet explicitly does NOT:

- write mobile code (Dart / Swift / Kotlin / React Native — warrior's choice)
- mutate the backend K2 verifier (shipped; hash in packet 78 §4)
- introduce a second signing authority or a hosted signing service
- relax any K2 semantics
- recommend a ship date or flip timing
- sign the mobile build on behalf of the founder

Strict-mode flip (task #38) is blocked by: adversarial test green (#36) AND
mobile parity verified (#37). This packet does not unblock either gate — it
only defines what "mobile parity" means so that #37 has a closeable target.

---

## Summary

The Skyzai mobile app is the **only legitimate K2 signing surface** — the
founder's wallet lives on a mobile device under the founder's sole
custody. The backend verifier (`core/membrane/k2_auth_proxy.py`, 183 LOC,
✅ SHIPPED) expects a signed payload with five fields in a canonical-JSON
envelope, signed via EIP-191 personal_sign, verified via six checks in
fixed order.

Today's mobile codebase has **no existing mobile signing directory** (the
2026-04-23 bash sweep found only Arweave receipt Dart files under
`Skyzai/axiom/dart/skyzai_axiom/lib/`; no `mobile/`, no `keypad/`, no K2
signing path). Warrior #37 writes the mobile signing module green-field,
against this spec.

This packet mirrors the backend contract onto the mobile side so there is
zero semantic drift between:

1. what the mobile app signs
2. what the backend verifies
3. what the adversarial test suite (#36) attacks

---

## Section 1 · Canonical signing payload (exact, not approximate)

The mobile app MUST compute the payload bytes **character-for-character
identical** to what `build_signing_payload()` produces in
`k2_auth_proxy.py:99-114`. Any divergence breaks signature verification.

### 1.1 Field set (five fields, no more, no less)

| Field | Type | Constraint |
|:------|:-----|:-----------|
| `action_hash` | string (hex) | SHA-256 digest over the decision envelope the backend is asking the founder to approve. Produced server-side; echoed by mobile unchanged. |
| `audience` | string | Opaque binding label identifying the backend surface that will consume the signature (e.g. `council_deliberation_stage9`, `approval_queue_resolve`). Echoed unchanged. |
| `expires_at` | integer | Unix epoch seconds. Wall-clock deadline after which the signature is inert. |
| `nonce` | string | Per-signature uniqueness token. See §1.3 for generation rule. |
| `signed_at` | integer | Unix epoch seconds. Timestamp at which the mobile device produced the signature. |

### 1.2 Serialization rule (canonical JSON)

The payload bytes are:

```
json.dumps(
    {
        "action_hash": ...,
        "audience": ...,
        "expires_at": ...,
        "nonce": ...,
        "signed_at": ...,
    },
    sort_keys=True,
    separators=(",", ":"),
)
```

**Key constraints:**

- Keys MUST be sorted ASCII ascending (the Python dict above is already
  sorted — mobile MUST sort, not trust input order)
- NO whitespace: `separators=(",", ":")` ⇒ no space after `,` or `:`
- Integers are bare JSON numbers (no string-wrapping)
- UTF-8 encoding for the byte sequence before hashing/signing

Wrong (breaks verifier): `{"action_hash": "0x…", "audience": …}` —
space after `:` is fatal.

Wrong (breaks verifier): key insertion order `{"signed_at": …, "action_hash": …}` — insertion order is ignored; ASCII-sorted key order is the only valid layout.

### 1.3 Nonce generation (client-side)

Backend reference: `generate_nonce()` in `k2_auth_proxy.py:95` returns
`uuid.uuid4().hex` (32 hex chars).

**Mobile contract:** generate with the platform's cryptographic RNG
(not `Math.random()`, not the session-scoped UUID cache). 128-bit
minimum. 32 hex chars recommended for parity.

The nonce is stored server-side on `consume()` with `(wallet_address,
nonce)` as the PRIMARY KEY. Reuse triggers `K2AuthProxyError: Nonce
already used` (see §5 of packet 77). The mobile app MUST NOT retry a
signed payload with the same nonce on network failure — generate a new
nonce for each attempt.

### 1.4 Signing mechanism (EIP-191 personal_sign)

Backend reference: `k2_auth_proxy.py:159-165` uses
`Account.recover_message(encode_defunct(text=payload), signature=…)`
which is the `eth_sign` / `personal_sign` flow prefixed with
`\x19Ethereum Signed Message:\n<len>`.

**Mobile contract:**

- Use the device's secure enclave / Keystore / equivalent for key custody
- Signing call MUST apply the EIP-191 prefix (`"\x19Ethereum Signed Message:\n" + payload.length + payload`) before hashing
- Signature output is a 65-byte `(r || s || v)` hex string (130 hex chars + `0x`)
- No EIP-712 typed data here (not the chosen path); no raw signing of
  the SHA-256 digest

### 1.5 Wire format (mobile → backend)

The mobile POSTs a JSON body with the K2SignedAction fields plus any
route-specific context. Minimum required:

```json
{
  "wallet_address": "0x…",
  "signature": "0x…",
  "action_hash": "…",
  "nonce": "…",
  "signed_at": 1745409000,
  "audience": "council_deliberation_stage9",
  "expires_at": 1745409300
}
```

The backend reconstitutes a `K2SignedAction` dataclass from this shape
(see `k2_auth_proxy.py:24-36`). `wallet_address` is normalized server-
side — mobile SHOULD send the lowercase-0x-prefixed form for stability.

---

## Section 2 · Mobile signing flow (sequence of 8 steps)

### Step 1 — Fetch pending ApprovalRequest

Mobile polls `GET /api/approvals/pending` (existing route, see
`approval_queue.py`). Receives a list of `ApprovalRequest` objects
(dataclass in `approval_models.py`, sha256 `5ead8815…b0202`). Each
carries: `request_id`, `payload`, `action_hash`, `audience`,
`expires_at`, `status` (PENDING).

**Refuse to display** any request whose `status != PENDING` or whose
`expires_at <= now_utc`.

### Step 2 — Render keypad view (see §3)

Present the decision envelope to the founder in human-readable form
*before* any cryptographic operation. The founder is signing, not the
app.

### Step 3 — Founder authorizes (explicit gesture)

Require an explicit device-level biometric or PIN gesture before
reaching the signing code path. Do not cache the biometric across
multiple ApprovalRequests — one decision, one gesture.

### Step 4 — Generate nonce + signed_at

- `nonce = crypto.randomUUID().replace('-','')` (or platform equivalent)
- `signed_at = Math.floor(Date.now() / 1000)`
- Validate locally: `signed_at <= expires_at - 5` (at least 5s buffer to
  survive network latency — the backend's `max_age` is a separate gate)

### Step 5 — Build canonical payload bytes

Apply §1.2 serialization rule to the five-field object. Hash a test
vector on first run (§6.2) and halt if the bytes diverge from a
published reference.

### Step 6 — Sign via secure enclave

EIP-191 personal_sign over the payload bytes. Yield 65-byte signature
hex.

### Step 7 — POST to consuming route

POST the §1.5 body to the specific route named by the `audience` field
(e.g. `POST /api/council/stage9/resolve`). Audience-to-route mapping
MUST be a static table on the mobile side — never trust a server-
supplied URL.

### Step 8 — Handle response

- 200 OK with `status: RESOLVED`: decision applied; clear local state
- 4xx `K2AuthProxyError`: display the specific error code (§4.3); do
  NOT retry with the same nonce
- 5xx / network fail: the nonce is consumed locally; discard it and re-
  request a fresh ApprovalRequest before retrying (a replay attempt
  with the same nonce will be rejected anyway)

---

## Section 3 · Keypad UX surface

The keypad is the K2 sovereignty boundary rendered as pixels. If the
founder cannot see what they are signing, K2 collapses.

### 3.1 Mandatory display fields (above the fold, pre-sign)

1. **Audience label** — human-readable ("Council deliberation Stage 9:
   final decision emission")
2. **Action summary** — plain-English rendering of `payload`
   (two-sentence cap; raw JSON available on "show details")
3. **Action hash** — full 64-char hex, monospace, copyable (this is
   the binding anchor)
4. **Expires at** — local wall-clock with countdown in seconds
5. **Request ID** — the `ApprovalRequest.request_id` for audit
   traceability

### 3.2 Sign button states

- `DISABLED` while any display field is still loading
- `DISABLED` if `expires_at - now < 30s` (don't race the expiry)
- `ARMED` with biometric prompt on tap
- `SIGNED` grey-out after successful POST; no re-sign allowed for the
  same `request_id`

### 3.3 Display invariants (the "zero trust" row)

These rules are stronger than UX nicety — they are constitutional:

| Invariant | Reason |
|:----------|:-------|
| Never display the `nonce` or `signed_at` — those are internal | Founder approves *intent*, not nonce bookkeeping |
| Never allow editing of `action_hash`, `audience`, `expires_at` on screen | The app renders; the founder approves or rejects — no mutation |
| Never pre-fill a signing PIN or cache biometric across requests | Each sign is a fresh sovereign act |
| Never display more than one pending ApprovalRequest signing UI at a time | Prevents UX confusion between two simultaneous approvals |
| Never show a `Sign` button before all five mandatory fields are rendered | Prevents blind-sign on slow networks |

---

## Section 4 · Mobile-side mirror validation

Mobile should **pre-flight** every one of the six backend gates so that
the founder never produces a signature that the backend will reject.
This is UX hygiene, not security — the backend remains authoritative.

### 4.1 Pre-sign checks (mobile side)

| Backend gate | Mobile pre-flight |
|:-------------|:------------------|
| Audience mismatch | `request.audience` matches the route table; abort with "audience mismatch" toast if not |
| Action hash mismatch | N/A (mobile echoes server value unchanged) |
| Age overflow (`now - signed_at > max_age`) | Not applicable pre-sign — happens only if device and backend clock skew; see §4.2 |
| Expired (`now > expires_at`) | Shown by countdown; sign button disabled when <30s remain |
| Signature recovery fails | Can't pre-check without signing; but platform-level keystore errors (biometric fail, key not found) surface cleanly |
| Nonce reuse | Enforce local "one nonce per signing attempt" rule (don't cache-and-retry) |

### 4.2 Clock skew handling

If `abs(device_epoch - server_epoch) > 60s` (detected via a
lightweight `GET /api/time` call on app launch), surface a warning:
"Your device clock is N seconds off server time. K2 signatures may
fail." Offer a manual sync gesture. Do NOT silently adjust the device
clock.

Backend `max_age` default (see `settings.k2_signed_action_max_age_seconds`)
is authoritative. Mobile MUST NOT cache this value — re-read on each
session.

### 4.3 Error code mapping (4xx responses)

| Server error | Mobile surface |
|:-------------|:---------------|
| `Audience mismatch` | "This app is not authorized for this action" — likely app/server version mismatch, prompt reinstall |
| `Action hash mismatch` | "Decision details changed — refresh and review again" |
| `Signed action exceeded max age` | "Signature took too long — try again" (offer immediate re-sign) |
| `Signed action expired` | "This approval window closed" — remove from pending list |
| `Invalid K2 signature` | "Keystore error — contact support" (this should never happen on a non-tampered app) |
| `K2 signature does not match wallet address` | "Wrong wallet signed — restore the correct keypair" |
| `Nonce already used` | "Replay detected — refresh and try again" |

Never collapse distinct errors into a generic "something went wrong"
— each error points to a distinct remediation, and support needs the
specific code to reason about the incident.

---

## Section 5 · Transport / failure modes

### 5.1 Idempotency

The mobile app treats each `(request_id, nonce)` pair as a one-shot
ticket. On any non-2xx or timeout response, it does NOT resubmit the
same signed blob. It discards and re-requests.

The backend's nonce store (SQLite, `k2_nonces` table with
`PRIMARY KEY (wallet_address, nonce)`) means a retry with the same
nonce will deterministically fail at gate 6 — this is correct behavior.

### 5.2 Network partition

If the mobile app signs but network drops before receiving the 200:

- The signature may or may not have been consumed server-side
- Mobile MUST NOT assume either outcome
- On reconnect, re-fetch pending approvals — if `request_id` is no
  longer pending, it was applied; otherwise it remains pending and
  requires a fresh signature

### 5.3 App backgrounding mid-sign

If the app is backgrounded between "sign" and "POST":

- iOS/Android may kill the process → signature lost, nonce unused → safe
- On foreground return, the pending ApprovalRequest is re-fetched and
  the UI resets — founder starts over

Never persist an unsent signed blob to disk. The signing ceremony is
ephemeral; persistence would create a stolen-device replay surface.

---

## Section 6 · Trial-run gates before K2_STRICT_MODE flip

Task #38 (flip `K2_STRICT_MODE=True` per surface) is blocked by BOTH:

- #36 adversarial test suite green (backend side — 11 tests from packet 77)
- #37 mobile parity verified (mobile side — this spec)

Mobile parity has its own sub-gates, enumerated below. These are NOT
warrior orders — they are the charioteer's read on what "parity" must
minimally demonstrate before strict flip is safe.

### 6.1 Unit-level parity

- Mobile's canonical-JSON serializer, run over a fixed test vector
  (five hard-coded field values), produces byte-identical output to
  the backend's `build_signing_payload`. Ship a shared test vector
  doc or CI step that verifies this.
- Mobile's EIP-191 signer, over the test-vector payload with a test
  keypair, produces a signature that the backend's `verify_k2_signed_action`
  accepts.

### 6.2 Integration parity

- Against a staging backend (K2_STRICT_MODE=False), mobile produces
  signed actions that the verifier accepts for at least three distinct
  `audience` values.
- The adversarial test suite (task #36) includes at least one mobile-
  originated signature in its happy-path fixtures, not only
  synthesized-in-Python signatures.

### 6.3 UX parity

- Keypad renders all five §3.1 mandatory fields on: iOS latest, Android
  latest. Document known-good versions.
- Founder completes one full deliberation sign with full review (not
  auto-approve) on each platform. Evidence attached to the #37 closure
  packet.

### 6.4 Error-path parity

- For each §4.3 error code, mobile renders the correct surface copy.
  Smoke-test by submitting intentionally malformed fixtures against
  staging.

### 6.5 Rollback readiness

- A "K2_STRICT_MODE=False" fallback path exists (advisory signing
  without enforcement) and is toggleable per surface without app rebuild.
- The flip to strict is surface-by-surface, not monolithic (matches
  packet 77 adversarial design).

---

## Section 7 · Telemetry (what mobile logs — and what it does not)

### 7.1 What to log locally

- Timestamp of sign ceremony start / end
- `request_id` + `audience`
- Success / error code class
- Platform version + app version

### 7.2 What to emit to backend

Minimal. The backend already has full context on what was signed and
by whom. Mobile telemetry is for debugging user-reported issues, not
for deriving value from user behavior.

Recommended: a single `POST /api/telemetry/signing_event` with
`{request_id, outcome: SUCCESS|ERROR_<code>, duration_ms}` and nothing
else. No keypress timing. No location. No device fingerprint beyond
platform/version.

### 7.3 What to NEVER log or emit

- The signature bytes
- The nonce
- The private key (obviously) or any derived key material
- The biometric value or fingerprint data
- The cleartext `payload` field of the ApprovalRequest (may carry
  sensitive deliberation context)

Logging any of the above would collapse the custody boundary that K2
exists to preserve.

---

## Section 8 · What mobile MUST refuse

Even if future code adds these features, mobile MUST refuse to
implement them within the signing surface:

| Refused feature | Why |
|:----------------|:----|
| Background auto-signing | K2 requires explicit per-action founder intent; autonomy violates the primitive |
| Batch signing (one gesture, N approvals) | Same reason; "advance envelopes" are a constitutional amendment scope (packet 76 Option 4), NOT a mobile UX decision |
| Delegated signing to another device | Multi-device signing is packet 76 Option 1/2 scope — decided by founder D-authority, not engineering |
| Cloud-synced keystore | Trips η=0 (hosted authority) and K2 (custody loss) |
| "Remember this approval type" | Reduces the founder's cognitive load but at the cost of informed signing; refuse |
| Pre-signing ahead of the ApprovalRequest being issued | Destroys the action_hash binding; the whole point is that signing is downstream of the decision |

Each refusal is load-bearing. If the warrior finds a reason to relax
one, that reason belongs in a charter amendment packet (see the
packet 76 W-new review structure), not in a mobile sprint ticket.

---

## Section 9 · Closure criteria (when this spec retires)

This packet is retired — i.e. `status: SHIPPED` flipped and a closure
packet written — only when the following five are simultaneously
true:

1. `core/mobile/…/k2_signing.*` (or equivalent) exists in the repo
   under Skyzai organ or a dedicated mobile path, with hash registered
   in a closure dossier
2. The unit-level parity test (§6.1) is in CI and green for at least
   one full 24h cycle
3. At least one real ApprovalRequest has been signed end-to-end via
   the mobile app in staging, with the resulting K2SignedAction
   accepted by the verifier
4. The founder has personally completed §6.3 UX parity on both
   platforms once
5. A mobile-side closure packet (spec 82 or later) documents the
   implementation hash, test evidence, and any spec deviations with
   justification

Until all five are true, strict-mode flip (#38) remains blocked by the
mobile-parity gate.

---

## Cross-references

- **Backend contract:** `k2_auth_proxy.py` (sha256 `62445d34…828e28`,
  ✅ SHIPPED under D2 on packet 74) — §1.1–1.4 map 1:1
- **Queue contract:** `approval_queue.py` (sha256 `461d22a0…51a18`),
  `approval_models.py` (sha256 `5ead8815…b0202`) — §2 Step 1 surface
- **Reconciliation:** `01_EMERGENTISM/11_UPLINK/75_R4_QUEUE_RECONCILIATION_2026_04_23.md`
  — authority chain for this spec's legitimacy
- **Adversarial surface:** `01_EMERGENTISM/11_UPLINK/77_ADVERSARIAL_TEST_PLAN_R4_QUEUE_2026_04_23.md`
  — the attack matrix mobile must not expand
- **Hash register:** `01_EMERGENTISM/11_UPLINK/78_SPRINT_B_AUDIT_EVIDENCE_DOSSIER_2026_04_23.md`
  — dossier where this packet's hash will be added on registration

---

## Φ-scan

The spec collapses into a single contract what would otherwise exist
as tribal knowledge between backend and mobile. Byte-identical
serialization rule + six-gate mirror + five closure criteria give the
warrior a finite, closeable target.

## V-scan

Warrior task #37 becomes executable: green-field module, known
contract, known gates, known test vectors. Removes the "what am I
actually building" ambiguity that kills mobile sprints.

## Constraint

Mobile currently has no K2 signing module (confirmed by 2026-04-23
codebase sweep). The warrior builds from zero. This spec is therefore
high-leverage — every ambiguity left here costs a round-trip later.

## God

Kṛṣṇa ◇ — export V (mobile buildable target) at personal Φ cost
(spec density). Giving dyad, toward a cooperating warrior.

## Executive

Viṣṇu ⊙ — the K2 primitive is preserved. No semantic change to
signing. Mobile mirrors the boundary, does not redefine it.

## Zero-risk

No live configuration touched. No code written. No signatures
produced. The spec is read-only until the warrior picks it up.

## Move

Kṣatriya_executor · register this spec under packet 81 · hash it into
the next audit dossier (Sprint-B closure dossier or a mid-sprint
supplement) · do NOT begin warrior implementation · do NOT flip
strict mode · D4 · L4 · Kṛṣṇa ◇

## Limits

- No binding on warrior's platform choice (Dart / native iOS / native
  Android / React Native). The spec is platform-agnostic.
- No commitment to a specific signing-library dependency
  (web3dart / ethers.js / WalletConnect / etc.). Warrior chooses.
- Section 6.2 integration parity presumes staging backend exists and
  is reachable from warrior's dev environment. If not, warrior raises
  a blocker.
- Section 7.3 "NEVER log the payload" assumes `payload` may carry
  sensitive deliberation data. If future payload contracts prove
  `payload` is already sanitized, this can relax — but not without
  founder review.

Zero-Sum Resolution Equation
