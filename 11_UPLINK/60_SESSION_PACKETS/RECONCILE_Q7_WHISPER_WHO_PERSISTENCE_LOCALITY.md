---
rosetta:
  primary_level: L4
  primary_column: Governance
  secondary:
    - level: L1
      column: Method
      role: "per-recipient local storage of accepted WHISPER assignments"
  operator: "Kṛṣṇa ◇"
  register: "[S]"
  canonical_phrase: "Each WHISPER recipient stores their own accepted assignments. The sender stores a counter-receipt. No central database."
---

# Q7 Reconciliation — WHISPER Five-Ws Who Persistence Locality

**Date:** 2026-04-29 (GMT+7)
**Status:** CLOSED — constitutional closure
**Author:** main under K2 directive
**Lane:** WHISPER × Five-Ws × persistence architecture
**Evidence tier:** `[S]` — structural deduction from packet 215 WHISPER spec and packet 214 Five-Ws schema
**Depends on:** [`214_APU_FIRST_PROACTIVITY_FEATURE_OBJECTIVE_FIVE_WS_2026_04_29.md`](214_APU_FIRST_PROACTIVITY_FEATURE_OBJECTIVE_FIVE_WS_2026_04_29.md) (Five-Ws Who field), [`215_INTENT_AUTHORED_EPHEMERAL_MESSAGING_WHISPER_PRIMITIVE_2026_04_29.md`](215_INTENT_AUTHORED_EPHEMERAL_MESSAGING_WHISPER_PRIMITIVE_2026_04_29.md) (WHISPER flow, K0/K2/K4 discipline)

---

## The Question

When Vaibhav K2-accepts a WHISPER assignment from Yves (e.g., "book the plane ticket and organize travel"), where does the confirmed assignment persist?

Three candidates:
- **Yves's side only** — Yves records the accepted commitment; Vaibhav records nothing
- **Vaibhav's side only** — Vaibhav records the accepted commitment; Yves holds a counter-receipt
- **Both sides independently** — each stores their own copy; neither depends on the other

---

## The Decision: Both Sides Independently

**Confirmed assignments persist on both sides independently.** This is the only option that satisfies K0 (No Receipt No Reality), K2 (both parties have a binding record), and K4 (each party exits with their own receipts).

```
Yves sends WHISPER
  → encrypted to Vaibhav's npub
  → Vaibhav receives, decrypts, acts
  → Vaibhav K2-accepts (signs accept/decline)
  → FLOW writes Vaibhav's acceptance receipt
  → Five-Ws Who field on Vaibhav's side: "proposed" → "confirmed"
  → WHISPER auto-deletes from both devices
  → Yves receives accept signal
  → FLOW writes Yves's counter-receipt ("Vaibhav accepted at T")
  → Five-Ws Who field on Yves's side: "pending Vaibhav" → "confirmed by Vaibhav"
```

---

## The Three Persistence Rules

### Rule 1: Confirmed assignments persist on each recipient's side

Every named person in a Five-Ws Who field has their own copy of the assignment once they K2-accept. This is local-first: the assignment lives in Vaibhav's own workflowy, encrypted only to Vaibhav's keys, accessible only to Vaibhav's BitNet router. No relay, no central database, no sender-view.

### Rule 2: The sender holds a counter-receipt

Yves receives the accept signal (not the full content of Vaibhav's signed acceptance, which Vaibhav keeps private). Yves's FLOW writes: `recipient accepted at Unix-ms, signed by Vaibhav's K2 key`. This is a counter-receipt — it proves the assignment was accepted without exposing Vaibhav's private workflowy content.

### Rule 3: WHISPER content deletes; receipts persist

The ephemeral chat (packet 215) auto-deletes after accept/decline/read-without-reply. The ephemeral deletion is complete and permanent. What persists is not the chat but the receipt:

| On Yves's side | On Vaibhav's side |
|---|---|
| `WHO: Vaibhav` — confirmed | `WHO: Vaibhav` — confirmed (self) |
| `ACCEPTED_AT: T` | `ACCEPTED_AT: T` |
| `RECEIPT: Vaibhav K2 sig` (partial) | `RECEIPT: Vaibhav K2 sig` (full) |
| `OBJECTIVE: [title]` (reference) | `OBJECTIVE: [title]` (full, in Vaibhav's own workflowy) |
| `WHISPER content` — deleted | `WHISPER content` — deleted |

---

## Why Not Sender-Only?

Sender-only persistence fails K2 for the recipient. If only Yves records that Vaibhav accepted, then:
- Vaibhav has no binding record of his own commitment
- Vaibhav's workflowy doesn't update
- Vaibhav's Five-Ws Who field stays at "proposed" forever
- Vaibhav could claim the assignment was never confirmed

This violates the principle that the recipient must K2-sign their own acceptance to be bound.

---

## Why Not Recipient-Only?

Recipient-only persistence fails K0 for the sender. If only Vaibhav records the accepted assignment, then:
- Yves has no binding record if Vaibhav later denies
- Yves's workflowy can't update the Who field without trusting Vaibhav's node

The sender needs a counter-receipt. This is why both sides independently store their own copy.

---

## Constitutional Discipline

| Commitment | K0 | K2 | K4 |
|---|---|---|---|
| Yves sends intent | No receipt yet | Yves signed the translation | — |
| Vaibhav accepts | Receipt created on both sides | Vaibhav K2-signed acceptance | Each exits with their own receipt |
| Vaibhav declines | Short signal only | Vaibhav K2-signed decline | Both delete without receipt |
| Read without reply | Auto-delete only | No K2 action | Both delete without receipt |
| Grace Exit | Both sides retain only their own receipts | Valid | Each exits clean with counter-receipt |

**No central database.** Not even a relay-stored copy. The relays carry only encrypted envelopes (NIP-17 gift-wrap). The decrypted assignment lives only on each device. This is what makes WHISPER K4-safe: there is nothing accumulated on a third party to exit from.

---

## One-Line Compression

**Each WHISPER recipient stores their own confirmed assignment locally. The sender stores a counter-receipt. No central persistence. No relay archive. WHISPER content dissolves; receipts persist independently on each side.**

Zero-Sum Resolution Equation

*The assignment lives on both sides. The chat dissolves from both. Each exits with their own receipt.*
