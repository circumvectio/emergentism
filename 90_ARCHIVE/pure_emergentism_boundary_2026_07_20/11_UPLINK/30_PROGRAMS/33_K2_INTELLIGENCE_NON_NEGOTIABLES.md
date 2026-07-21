---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "K2 Non-Negotiables for Intelligence"
---

# K2 Non-Negotiables for Intelligence

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*


> **The organism recommends. The human decides. That boundary is the intelligence layer.**

Date: 2026-04-16  
Status: Doctrine (Constitutional Guard for Gate 5)  
Canonical path: `33_K2_INTELLIGENCE_NON_NEGOTIABLES.md`

---

## 0. Purpose

Intelligence is the most dangerous layer for K2 bypass.

When a system becomes smart enough to predict well, the temptation grows to let it act on its own. This doctrine makes that temptation structurally impossible.

---

## 1. The One-Sentence Law

**No intelligence output may execute without a human signature. Intelligence that auto-executes ceases to be intelligence and becomes compulsion.**

---

## 2. The Three Intelligence Modes

| Mode | Definition | K2 Status |
|------|------------|-----------|
| **Observation (F1)** | TheCircle gathers and structures signals | No K2 required; purely passive |
| **Pricing / Prediction (F2)** | RealityFutures prices probability | No K2 required; purely informational |
| **Recommendation (F3)** | APU deliberates and proposes action | **K2 REQUIRED before execution** |
| **Execution (F4)** | Skyzai settles on-chain or off-chain | **K2 SIGNATURE IS THE GATE** |

### The Fatal Error

Blurring F3 into F4 — allowing "high-confidence" recommendations to auto-execute — destroys K2 and converts the organism from servant to captor.

---

## 3. The Five Non-Negotiables

### N1: The Push Ends in Approve / Hold

Every APU output that reaches a human must present exactly two sovereign options:
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

Without the signature, the ActionPacket is invalid.

### N3: The Human Must See the Full Warrant

Before signing, the human must be shown:
- The recommendation (what)
- The reasoning (why)
- The risk framing (downside)
- The alternative paths (what else could be done)
- The source trace (which F1 signals fed this F3 output)

Withholding any of these is a K2 violation by deception.

### N4: The AI Never Holds the Keys

- No LLM has access to signing material.
- No agent can construct a valid K2 envelope without human participation.
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
It is a potential K2 bypass in language form.

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

### Required code invariants:

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
| DAO / multi-sig DACs | K2 becomes multi-sig. Each signer is a human with their own biometric gate. No AI seat in the multi-sig. |

---

## 7. Canonical Compression

> **APU is a council of advisors. Skyzai is the executor. The human is the only sovereign. Intelligence without K2 is not intelligence. It is automation wearing a reasoning mask.**

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Gate 5 protection — applies to all intelligence-layer design and implementation.
2. **Your Next Action:** Review any F3→F4 handoff path. If a single line of code can execute without K2, flag it as a constitutional violation.
3. **Expected Output:** A K2 audit report for any proposed intelligence feature, or a corrected design that hardcodes N1–N5.
4. **Success Criteria:** A security reviewer can read your output and verify that no execution path bypasses the human signature.
5. **Canonical Path:** `33_K2_INTELLIGENCE_NON_NEGOTIABLES.md` (this file).

---

> *The seer sees. The seer does not decide.  
> The human decides. The human signs.  
> That gap is where sovereignty lives.*  
> *eta = 0. K2 always.*
