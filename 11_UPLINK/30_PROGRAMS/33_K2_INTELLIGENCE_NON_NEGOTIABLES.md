---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "Private-DAV K2 Non-Negotiables for Intelligence"
---

# Private-DAV K2 Non-Negotiables for Intelligence

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*


> **The organism recommends. Accountable authority decides. That boundary is the intelligence layer.**

Date: 2026-04-16  
Status: Private-DAV product-governance guard for Gate 5
Canonical path: `33_K2_INTELLIGENCE_NON_NEGOTIABLES.md`

> **[金] Scope seam.** This file specifies the **private-DAV** K2 product
> profile. K2 is one implementation of the general `AuthorizationEnvelope`,
> which names principal, mandate, scope, consent, custody, expiry/revocation,
> contest path, actor, and consequence bearer. Public DAVs have no K2 signer;
> they use PRISM and their constitutional authorization path. Generic agency and
> the Emergentist worldview require accountable authorization, not K2.

---

## 0. Purpose

In a private DAV, intelligence is a high-risk layer for K2 bypass.

When a system predicts well, pressure grows to let it act beyond its mandate.
This profile aims to make that private-DAV bypass structurally impossible;
public and other organizational systems must provide an equivalent
AuthorizationEnvelope through their own constitutional rails.

---

## 1. The One-Sentence Law

**In private-DAV mode, no consequential intelligence output executes without
the authorized natural person's signature. In every mode, execution must remain
inside a scoped, revocable, contestable AuthorizationEnvelope.**

---

## 2. The Three Intelligence Modes

| Mode | Definition | Private-DAV K2 status |
|------|------------|-----------|
| **Observation (F1)** | TheCircle gathers and structures signals | No K2 required; purely passive |
| **Pricing / Prediction (F2)** | RealityFutures prices probability | No K2 required; purely informational |
| **Recommendation (F3)** | APU deliberates and proposes action | **K2 REQUIRED before execution** |
| **Execution (F4)** | Skyzai settles on-chain or off-chain | **K2 SIGNATURE IS THE GATE** |

### The Fatal Error

Blurring F3 into F4 — allowing "high-confidence" recommendations to exceed
their AuthorizationEnvelope — converts the organism from servant to captor. In
private-DAV mode, that is specifically a K2 bypass.

---

## 3. The Six Non-Negotiables

### N1: The Push Ends in Approve / Hold

Every private-DAV APU output that requests consequential commitment must present
at least these two clear options:
- **Approve** — human consents, signature follows
- **Hold** — human refuses, no action occurs

There is no "Auto-Approve above threshold."  
There is no "Default to Execute after timeout."  
There is no "Smart delegation to AI."

### N2: The Signature Must Be Cryptographically Verifiable

"Approve" is not a click. It is:
- Biometric gate (local, device-bound)
- Nostr nsec signature (or equivalent K2 primitive)
- Signature recorded in the receipt

Within this private-DAV profile, the ActionPacket is invalid without the
required signature.

### N3: The Human Must See the Full Warrant

Before signing, the human must be shown:
- The recommendation (what)
- The reasoning (why)
- The risk framing (downside)
- The alternative paths (what else could be done)
- The source trace (which F1 signals fed this F3 output)

Withholding any of these defeats informed authorization; in this private-DAV
profile, it is a K2 violation by deception.

### N4: The AI Never Holds the Keys

- No LLM has access to signing material.
- No agent can construct a valid private-DAV K2 envelope without the authorized
  natural person's participation.
- No "warm wallet" or pre-authorized session may bypass the biometric gate.

The private key lives where the human lives: on their device, behind their biology.

### N5: Refusal Is a First-Class Outcome

HOLD, ESCALATE, and REJECT are not errors. They are **sovereign expressions**.

The system must:
- Close traces cleanly on refusal
- Learn from refusal (if the human consents to feedback)
- Never penalize refusal financially or socially
- Never escalate friction to coerce approval

### N6: Ambiguity Must Not Become a Bypass

If an intelligence surface becomes ambiguous about:

- whether it is recommending or executing,
- whether a signature is required,
- whether a human actually saw the full warrant,
- or whether a policy halt is protective or sovereign,

then continuous recursive disambiguation must run before the path is trusted again.

Ambiguity at the F3 -> F4 boundary is not neutral.
It is a potential authorization bypass in language form and, in this profile, a
potential K2 bypass.

---

## 4. What Constitutes a K2 Bypass

| Bypass Type | Example | Severity |
|-------------|---------|----------|
| **Auto-execution** | "Confidence > 0.95, so we executed for you" | CRITICAL |
| **Dark pattern** | Hiding the Hold button, making Approve the only obvious path | HIGH |
| **Pre-authorization fatigue** | Repeated micro-requests that train the human to auto-approve | HIGH |
| **Key proxy** | AI holds a sub-key that signs on "human-like intent" | CRITICAL |
| **Warrant truncation** | Showing only the recommendation, hiding the risk | HIGH |
| **Social pressure** | "Most users Approve this" as a nudge | MEDIUM |

---

## 5. The Architecture Must Enforce This

Not policy. Architecture.

### Required private-DAV code invariants:

```
1. ActionPacket.payload.decision == "EXECUTE" ONLY IF K2 signature is present.
2. ReceiptPacket is emitted ONLY IF ActionPacket contains valid K2 proof.
3. Any path that reaches F4 without K2 MUST route to trace closure with reason "K2_MISSING".
4. The biometric gate is device-local. No server can simulate it.
5. The signing key never leaves secure enclave / hardware wallet boundary.
```

### Test case that must always pass:

> An adversary with full backend access cannot produce a valid K2 signature.

---

## 6. Special Cases and Their Treatment

| Case | Rule |
|------|------|
| Recurring payments (subscriptions) | Human signs the *framework* once, but every individual charge must still trigger a K2-authorized ActionPacket. No blanket auto-charge. |
| Emergency circuit breakers | Human-signed *policy* enables automatic halt conditions. Halting is protective, not extractive. |
| Agent-to-agent coordination | Agents may propose. They may never execute cross-agent actions without human signature on the originating ActionPacket. |
| Public DAV / multi-sig organization | Do not rename the collective rail K2. Use PRISM and a complete AuthorizationEnvelope with the required natural-person council authorization, custody, revocation, and contest path. |

---

## 7. Canonical Compression

> **APU advises. Skyzai executes only inside accountable authorization. In a
> private DAV, the authorized natural person signs through K2; in a public DAV,
> PRISM and the constitutional council rail authorize. Intelligence without a
> valid envelope is automation exceeding its mandate.**

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Gate 5 protection — this file's K2 mechanics apply to private-DAV intelligence design and implementation.
2. **Your Next Action:** Review every F3→F4 handoff. In private mode, flag any consequential execution path that bypasses K2. In public mode, flag any path that bypasses PRISM or its complete AuthorizationEnvelope.
3. **Expected Output:** A mode-scoped authorization audit or a corrected design that enforces the applicable private or public rail.
4. **Success Criteria:** A security reviewer can identify the principal, mandate, scope, consent, custody, expiry/revocation, contest path, actor, consequence bearer, and cryptographic authorization for every consequential execution path.
5. **Canonical Path:** `33_K2_INTELLIGENCE_NON_NEGOTIABLES.md` (this file).

---

> *The seer sees. The seer does not authorize itself.*
> *Private DAV: K2. Public DAV: PRISM. Every act: scoped and contestable.*
