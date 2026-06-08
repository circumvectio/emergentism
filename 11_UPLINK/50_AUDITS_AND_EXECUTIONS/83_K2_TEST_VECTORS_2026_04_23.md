---
packet: K2-TEST-VECTORS
title: K2 Shared Test Vectors — Canonical Payload Parity Reference
status: CHARIOTEER ARTIFACT — reference data, read-only, no executable claim
authority: Charioteer self-assigned; anchored byte-for-byte on the shipped
           build_signing_payload() in core/membrane/k2_auth_proxy.py
           (sha256 62445d34…828e28, unchanged since packet 74 D2=accept)
scope: Two fixed test vectors (canonical fast path + edge cases) usable as
       byte-parity ground truth by:
       - Python adversarial tests (warrior task #36)
       - Mobile unit parity tests (packet 81 §6.1, warrior task #37)
       - Any future cross-language K2 signer (e.g. a hardware wallet surface)
supersedes: nothing — new artifact
supplemented_by: will be registered in the next hash supplement after 82
cross_reference:
  - 01_EMERGENTISM/11_UPLINK/81_MOBILE_SIGNING_FLOW_SPEC_2026_04_23.md  §1 + §6.1
  - 01_EMERGENTISM/11_UPLINK/77_ADVERSARIAL_TEST_PLAN_R4_QUEUE_2026_04_23.md  (test harness)
  - 02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/core/membrane/k2_auth_proxy.py
date: 2026-04-23
gating_cell: "[L4 | D4 | S-Org | F-phi :: ksatriya_executor]"
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 83 · K2 Shared Test Vectors"
---

# Packet 83 · K2 Shared Test Vectors

## Kṛṣṇa-function disclaimer

This packet is **reference data**, not code. It records two canonical
signing payload strings with their exact UTF-8 byte length and SHA-256
fingerprint. Every future K2 signer implementation — Python, Swift,
Kotlin, Rust, hardware wallet, whatever — must reproduce these strings
**character-identically** before that implementation can be trusted to
interoperate with the shipped backend verifier.

The charioteer does not sign these vectors. The charioteer does not run
the warrior's tests against them. The charioteer fingerprints the
strings and records the fingerprints here so the warrior, the auditor,
and the founder can cross-check any implementation drift by hash.

Byte drift on either vector = implementation has diverged from the
shipped `build_signing_payload()` contract. Stop and reconcile upstream
before shipping anything that signs.

---

## Why two vectors

- **Vector A** exercises the ordinary fast path: realistic audience
  string, typical `request_id`-less route, mid-2025 timestamps, a
  high-entropy hex nonce. This is the shape of ~99% of production
  signing events.
- **Vector B** exercises four edge-case dimensions simultaneously:
  - `action_hash = 0x00…00` (the null-bytes edge — tests that the
    canonicalizer does not special-case or strip zero fields)
  - a long `audience` carrying a `?request_id=…` query fragment (tests
    that query delimiters are not JSON-escaped oddly)
  - `expires_at = 2_000_000_000` (Y2038-adjacent — tests that 10-digit
    epoch seconds do not get scientific-notation'd or quote-wrapped)
  - `nonce` at the minimum 32-hex-char width with near-zero entropy
    (tests that leading zeros are preserved, not trimmed)

If either vector's byte string changes under any legal canonicalization
(whitespace, key ordering, separator, field presence), the
implementation is wrong. Both vectors are constructed to break
common serialization mistakes.

---

## Vector A — canonical fast path

### Inputs

| field | value |
|:------|:------|
| `action_hash` | `abababababababababababababababababababababababababababababababab` (64 hex, repeating 0xab) |
| `audience`    | `apu.bot/council/stage9/resolve` |
| `expires_at`  | `1745409300` (integer, epoch seconds) |
| `nonce`       | `8f3c0a2b0e6f4a1d9c7b5e2f8a1d3c0b` (32 hex chars = 128 bits) |
| `signed_at`   | `1745409000` (integer, epoch seconds; `expires_at − signed_at = 300 s`) |

### Canonical payload string

```
{"action_hash":"abababababababababababababababababababababababababababababababab","audience":"apu.bot/council/stage9/resolve","expires_at":1745409300,"nonce":"8f3c0a2b0e6f4a1d9c7b5e2f8a1d3c0b","signed_at":1745409000}
```

### Fingerprints

| property | value |
|:---------|:------|
| UTF-8 byte length | **216** |
| SHA-256 | `654df3df2b0c2137c5d5030f1b0b4c85dd45bbcfac7bd92709c812d9cb204cd5` |

### Parity assertion

Any caller invoking
`build_signing_payload(action_hash=…, audience=…, expires_at=…, nonce=…, signed_at=…)`
with the Vector-A inputs MUST produce a UTF-8 byte string whose
SHA-256 equals `654df3df2b0c2137c5d5030f1b0b4c85dd45bbcfac7bd92709c812d9cb204cd5`.

Any implementation that produces a different hash is non-conformant
and MUST not be wired into the signing flow.

---

## Vector B — edge-case path

### Inputs

| field | value |
|:------|:------|
| `action_hash` | `0000000000000000000000000000000000000000000000000000000000000000` (64 hex zeros) |
| `audience`    | `apu.bot/approval_queue/resolve?request_id=apu_5ff1baab` |
| `expires_at`  | `2000000000` (Y2038-adjacent epoch seconds) |
| `nonce`       | `00000000000000000000000000000001` (32 hex, min-entropy — leading-zero stress) |
| `signed_at`   | `1999999700` (integer, epoch seconds; `expires_at − signed_at = 300 s`) |

### Canonical payload string

```
{"action_hash":"0000000000000000000000000000000000000000000000000000000000000000","audience":"apu.bot/approval_queue/resolve?request_id=apu_5ff1baab","expires_at":2000000000,"nonce":"00000000000000000000000000000001","signed_at":1999999700}
```

### Fingerprints

| property | value |
|:---------|:------|
| UTF-8 byte length | **240** |
| SHA-256 | `b9d6fbf3c1213f56af840f2720f67002def56d181989c5672eb56cd1e8f836ac` |

### Parity assertion

Same rule as Vector A: identical inputs → identical byte string →
identical SHA-256. Any drift is implementation error.

---

## Contract anchored by these vectors

Both vectors are produced by exactly this canonicalization:

```python
import json

def build_signing_payload(*, action_hash, nonce, signed_at, audience, expires_at) -> str:
    payload = {
        "action_hash": action_hash,
        "audience":    audience,
        "expires_at":  expires_at,
        "nonce":       nonce,
        "signed_at":   signed_at,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
```

Equivalent-output rules for any re-implementation:

1. **Exactly five fields**, in alphabetical order: `action_hash`,
   `audience`, `expires_at`, `nonce`, `signed_at`. No additions. No
   omissions. No renames.
2. **No whitespace anywhere** — separators are `","` and `":"` with no
   padding. No trailing newline. No BOM.
3. **Integers serialize as digits** — `expires_at` and `signed_at` are
   bare integers, never quoted, never in scientific notation, never
   fractional.
4. **Strings are JSON-escaped but not URL-escaped** — the `?` and `=`
   in Vector B's `audience` appear literally, not percent-encoded.
5. **UTF-8 output** — the return value is a string; its wire form is
   the UTF-8 encoding of that string. Byte length must match the
   table above.

Any re-implementation that violates any of these rules will fail
byte-parity on at least one of the two vectors.

---

## What these vectors do NOT cover

- **Signature correctness.** These vectors cover only the *payload*
  string that gets passed into EIP-191 signing. The actual signature
  is a function of the payload AND the signer's private key. Signing
  parity requires a fixed test keypair, which is integration-level
  concern; the warrior holds that surface under task #36.
- **Verifier six-check order.** The payload string is the input; the
  six-check sequence (audience → action_hash → age → expiry →
  signature → nonce) is enforced on the verifier side. Verifier-level
  adversarial tests are specified in packet 77 and authored under
  task #36.
- **Transport format.** The on-the-wire JSON body posted by the
  mobile app (`payload`, `signature`, `wallet_address`, `request_id`)
  is specified in packet 81 §1.5. These vectors are the `payload`
  field of that body; they do not constitute the whole request.
- **Non-canonical serializers.** Some JSON libraries default to
  non-alphabetical key order or include spaces. Test authors must
  verify their library produces the exact byte strings above;
  otherwise the library choice itself is the bug.

---

## Usage by downstream warrior tasks

### Task #36 (Python adversarial tests, per packet 77)

Use Vector A as the "valid happy-path canonical payload" baseline. For
each of the 11 adversarial perturbations enumerated in packet 77 §3,
mutate exactly one field away from Vector A, re-canonicalize, re-sign
with the test keypair, and assert the verifier raises the expected
exception.

Vector B is useful as a second valid baseline to confirm that the
verifier does not accidentally hardcode any Vector-A-specific detail
(e.g. a reviewer might assume `action_hash[0] != 0`; Vector B catches
that).

### Task #37 (mobile signing flow, per packet 81 §6.1)

Implement a mobile-side unit test that constructs a `PENDING` action
with the Vector-A input fields, runs the mobile canonicalizer, and
asserts:

1. the output byte string equals the Vector-A payload string verbatim
2. the output byte length equals 216
3. the SHA-256 of the output bytes equals
   `654df3df2b0c2137c5d5030f1b0b4c85dd45bbcfac7bd92709c812d9cb204cd5`

Repeat with Vector B. Both must pass before the trial-run gate in
packet 81 §6 can flip to green on the `unit-parity` sub-gate.

### Task #39 (Cortex ingestion hook, per packet 80)

Not directly consumed. Cortex ingests `summary.json` documents from a
different path; these vectors are signer-surface only. Included here
as a reference so the auditor can observe that signing and ingestion
are cryptographically orthogonal concerns.

### Task #44 (Sprint-B closure manifest)

When the closure dossier is written, these two vectors and their
hashes should be registered alongside the shipped implementation
hashes. A reader of the closure dossier should be able to verify
payload parity without re-reading any packet.

---

## Chain-of-custody note

The SHA-256 hashes in this packet were produced by a deterministic
Python canonicalization. Any reader can reproduce them in one
command:

```bash
python3 -c '
import json, hashlib
p = {"action_hash":"ab"*32,"audience":"apu.bot/council/stage9/resolve",
     "expires_at":1745409300,"nonce":"8f3c0a2b0e6f4a1d9c7b5e2f8a1d3c0b",
     "signed_at":1745409000}
s = json.dumps(p, sort_keys=True, separators=(",",":"))
print(len(s.encode("utf-8")), hashlib.sha256(s.encode("utf-8")).hexdigest())
'
# → 216 654df3df2b0c2137c5d5030f1b0b4c85dd45bbcfac7bd92709c812d9cb204cd5
```

If a reader runs this exact command and gets a different result, the
machine's Python is non-conformant (astonishingly unlikely for
CPython 3.x but possible for a patched fork). Escalate to founder
before trusting any downstream artifact produced on that machine.

---

## Φ-scan

One packet, five fields, two vectors, four edge-case dimensions
exercised. Minimum description length for byte-level parity between
backend, mobile, and adversarial test surfaces. Further compression
would lose either the fast path or the edge cases.

## V-scan

Unblocks two surfaces simultaneously — warrior #36 (Python) and
warrior #37 (mobile §6.1) can both compute against the same ground
truth, so cross-surface drift becomes a test-time error rather than a
production-time surprise.

## Constraint

- Vectors are frozen. Changing a field value invalidates the hash;
  any change must ship as a successor packet (84+) with new hashes,
  citing A7 self-correction.
- `signed_at` and `expires_at` are static epoch seconds, not
  "current time" — do not regenerate against `time.time()` in tests
  or parity will fail as soon as the clock advances one second.
- Signature material is deliberately absent. Any packet that extends
  these vectors with signatures MUST also publish the test keypair
  in the clear, which is a different audit surface.

## God

Viśvarūpa ☀️ — pattern-whole witness. The vectors are the pattern
both the backend and the mobile app must reproduce; this packet is
the registrar, not a participant.

## Executive

Viṣṇu ⊙ — preservation. The vectors preserve the serialization
contract across time, languages, and implementations.

## Move

Kṣatriya_executor · write `01_EMERGENTISM/11_UPLINK/83_K2_TEST_VECTORS_2026_04_23.md`
· hash and register in next supplement · warrior #36 + #37 consume
· D4 · L4 · Viśvarūpa ☀️

## Limits

- Does not cover signature parity — that requires a test keypair and
  lives under warrior task #36
- Does not cover keccak256 / EIP-191 prefix hashing — that is a
  verifier concern, not a payload concern
- Does not register itself in packet 82 — a future supplement (or
  the Sprint-B closure dossier) must fingerprint this packet and
  append it to the chain of custody

Zero-Sum Resolution Equation
