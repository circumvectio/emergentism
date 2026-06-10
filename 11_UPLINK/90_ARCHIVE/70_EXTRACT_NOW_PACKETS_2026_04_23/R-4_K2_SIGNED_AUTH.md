---
packet: R-4
title: K2-Native Signed Auth
status: SHIPPED (2026-04-23 under founder D2=accept on packet 74)
shipped_artifacts:
  - core/membrane/k2_auth_proxy.py (sha256 62445d34…828e28, 183 LOC)
  - core/membrane/approval_queue.py (sha256 461d22a0…51a18, 368 LOC)
  - core/membrane/approval_models.py (sha256 5ead8815…b0202, 83 LOC)
  - core/membrane/k2_gateway.py (sha256 d14be71c…9da6d, 570 LOC)
reconciliation: 01_EMERGENTISM/11_UPLINK/75_R4_QUEUE_RECONCILIATION_2026_04_23.md
source: Goose `oidc-proxy/` + `GOVERNANCE.md` + consensus rubric
target: `core/membrane/wallet_auth.py` (extension) + new `core/membrane/k2_auth_proxy.py`
date: 2026-04-23
rosetta:
  primary_level: L4
  primary_column: K2 Signed-Auth Reconciliation
  secondary:
    - level: L3
      column: Cryptographic Receipt Audit
      role: "separate shipped artifact hashes and specs from current implementation truth"
    - level: L6
      column: Signature-Locus Boundary
      role: "preserve founder-wallet signing authority against CI or service-account delegation"
    - level: L5
      column: Wallet Auth Architecture
      role: "map OIDC-inspired audience/age/budget binding into K2-native signatures"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I/D]"
  canonical_phrase: "R-4 · K2-Native Signed Auth"
---

# R-4 · K2-Native Signed Auth

**Rosetta boundary:** [I] This packet documents K2 signed-auth reconciliation/spec history. It does not [B] prove current auth safety, artifact hashes, replay protection, or shipped code behavior without fresh receipts.

## Summary

APU's current `wallet_auth.py` verifies a wallet signature over a fixed
session message (`ENCRYPTION_MESSAGE`). [B/I] That supports a wallet-control inference in this packet's reconcile model but does
not bind the signature to a specific **action** — so any valid session
signature could theoretically authorize any action within the session.

This packet specifies a K2-native extension: signatures bind to a per-action
hash (BIP-340 Schnorr or EIP-191 message, depending on chain), with rate
limits and audience checks inspired by Goose's OIDC-proxy pattern — but
with the signing authority remaining with the founder's wallet, not
delegated to a CI identity.

## Current state (live)

`core/membrane/wallet_auth.py`:

```python
F2_SESSION_MESSAGE = ENCRYPTION_MESSAGE

def verify_wallet_signature(*, wallet_address, wallet_signature, message=F2_SESSION_MESSAGE):
    recovered = Account.recover_message(encode_defunct(text=message), signature=wallet_signature)
    if normalize_wallet_address(recovered) != normalize_wallet_address(wallet_address):
        raise WalletAuthError("Wallet signature does not match wallet address")
    return derive_user_id(normalize_wallet_address(wallet_address))
```

Strengths:

- Cryptographic (EIP-191 personal_sign)
- Deterministic user-ID derivation
- Minimal surface

Weaknesses (for K2 purposes):

- Session signature is reusable across actions — one sign grants many operations
- No replay protection (nonce / timestamp / audience)
- No binding to `action_hash` (what the founder is signing **for**)

## Source pattern (Goose OIDC proxy)

From `oidc-proxy/README.md`:

```
GitHub Actions (OIDC token) → Worker (validate JWT, inject API key) → Upstream API
```

Worker validates:

- Issuer (`OIDC_ISSUER`)
- Audience (`OIDC_AUDIENCE`)
- Token age (`MAX_TOKEN_AGE_SECONDS`, default 20 min)
- Per-token request budget (`MAX_REQUESTS_PER_TOKEN`)
- Per-token rate limit (`RATE_LIMIT_PER_SECOND`)
- Optional allow-list of repos/refs

The relevant structural moves (not the identity choice):

- **Audience binding** — token is valid only for a named upstream
- **Age binding** — token expires quickly
- **Budget binding** — per-token call ceiling
- **Rate limiting** — per-token ceiling

## What to take

- Per-action audience binding (signature binds to `action_hash` + domain tag)
- Age binding (signature includes a `signed_at` timestamp; verifier enforces
  max age)
- Nonce to prevent replay
- Budget tracking per signature (default: 1 use, matches Goose's
  single-action model better than their batched 200)

## What to refuse

- OIDC itself. APU identities are wallet-native; GitHub/Google/any-IDP is a
  third party that punctures η = 0 and the signature-locus guard.
- Long-lived tokens. The 20-minute Goose default is reasonable for CI; for
  K2, each action has its own signature with its own narrow window.
- Delegation. Goose's pattern allows a CI identity to stand in for a human;
  K2 requires the **founder's wallet** to sign. No service account.

## Spec: new module `core/membrane/k2_auth_proxy.py`

```
# Spec only — not code

@dataclass
class K2SignedAction:
    action_hash: str           # hash(canonical_serialize(proposal))
    wallet_address: str
    signature: str
    nonce: str                 # random, enforced unique per wallet
    signed_at: int             # unix seconds
    audience: str              # e.g. "apu.bot/council/decide" — domain tag
    expires_at: int            # signed_at + max_age

class K2AuthProxyError(Exception): ...

def build_signing_payload(action_hash: str, nonce: str, signed_at: int, audience: str, expires_at: int) -> str:
    """Canonical string the wallet must sign. Deterministic, auditable."""

def verify_k2_signed_action(
    *,
    signed: K2SignedAction,
    expected_action_hash: str,
    expected_audience: str,
    max_age_seconds: int = 300,   # 5 minutes
    nonce_store: NonceStore,       # durable, founder-scoped
) -> str:
    """Returns wallet-derived user id on success, raises on failure.

    Checks (in order):
      1. expected_audience == signed.audience
      2. expected_action_hash == signed.action_hash
      3. time.time() - signed.signed_at <= max_age_seconds
      4. time.time() <= signed.expires_at
      5. nonce is fresh (not in nonce_store); insert before returning
      6. EIP-191 recover(build_signing_payload(...), signature) == wallet_address
    """
```

## Extension to `wallet_auth.py`

- Keep `verify_wallet_signature` for the fixed-session path (read-only
  surfaces like profile lookup)
- Route all state-mutating or execution-adjacent calls through
  `verify_k2_signed_action` instead
- Add a feature flag `K2_STRICT_MODE` so Sprint-A can begin in advisory mode
  (log what would have failed) before moving to enforcing mode

## Live surfaces that need migration

- `K2Gateway.resolve_with_crypto_signature` (already cryptographic; extend to
  verify per-action binding and nonce)
- Any API router that accepts `X-Wallet-Signature` header and currently
  validates against the session message
- MCP client surfaces that claim to authenticate via wallet

## Five-guard check

1. **Category-claim:** PASS — tightens the constitutional story. K2 gains
   teeth: no reusable session signature stands in for per-action authorization.
2. **η = 0:** PASS — entirely local. Wallet signs client-side; APU verifies
   in-process; no third-party IDP.
3. **K2:** PASS — this is the most direct K2 reinforcement possible. Each
   irreversible action now carries its own cryptographic proof.
4. **Three-Stage Process:** PASS — operates at the membrane layer, orthogonal to the
   IS/COULD/SHOULD/ACT axis.
5. **Signature-locus:** PASS — the founder's wallet remains the sole signer.
   No CI identity, no service account, no IDP.

## Dependencies

- Durable nonce store (SQLite or Postgres) scoped per wallet
- Deterministic canonical serializer for the signing payload
- API router refactor for state-mutating endpoints

## Risk notes

- Rollout order matters: ship the verifier + feature flag first, audit for a
  week in advisory mode, then flip `K2_STRICT_MODE=true` for one surface at
  a time
- The Skyzai app must update its signing flow to include nonce + action hash;
  the mobile keypad UX needs a trial
- A lost nonce store = founder temporarily locked out; the store must have
  backup/restore before `K2_STRICT_MODE` goes live anywhere

## Test plan

- Unit: signing payload is byte-deterministic across platforms
- Unit: nonce-reuse is rejected even if all other checks pass
- Unit: expired signature is rejected
- Integration: old `verify_wallet_signature` still works on read-only surfaces
- Integration: state-mutating endpoint requires `K2SignedAction` under strict mode
- Adversarial: replay attempts, audience confusion, action-hash tampering

## Commit template

```
feat(auth): K2-native per-action signed authorization (audience + nonce + age binding)

- add core/membrane/k2_auth_proxy.py (K2SignedAction + verifier)
- add durable nonce store
- wire state-mutating routers to K2_STRICT_MODE feature flag
- preserve wallet_auth.py session-signature path for read-only surfaces

Reconciles with extraction matrix packet R-4.
Founder signs every irreversible action; no delegation.
```

## Zero-risk

Drafting this spec cannot break anything. First code change is the verifier
module with `K2_STRICT_MODE=false` — no behavior change until the flag flips.
