---
rosetta:
  primary_level: L4
  primary_column: Method
  secondary:
    - level: L3
      column: Method
      role: "fifth communication primitive — ephemeral 1:1 intent-mediated"
  operator: "Kṛṣṇa ◇"
  register: "[I/S]"
  canonical_phrase: "Intent-authored, AI-mediated, ephemeral peer-to-peer messaging over Nostr. The user expresses intent via @-mention; the AI drafts and transmits a DM peer-to-peer; the message auto-deletes after read; the recipient's AI mediates accept/decline; acceptance creates a K2-signed binding receipt. WHISPER is the fifth communication primitive."
---

# PACKET 215 — WHISPER: INTENT-AUTHORED EPHEMERAL PEER-TO-PEER MESSAGING

**Date:** 2026-04-29 (GMT+7)
**Status:** ACTIVE — operational doctrine + new communication primitive
**Author:** main (wonderful-lalande-b1cb18) under K2 directive
**Lane:** NEXUS substrate (sovereign identity + Nostr graph) × 03_ORGANISM §17 (communication primitives) × packet 214 (APU proactivity)
**Evidence tier:** [I] for the WHISPER primitive design and ephemerality discipline | [S] for the integration with existing four primitives + K2 acceptance pattern | [C] avoided
**Depends on:** [`214_APU_FIRST_PROACTIVITY_FEATURE_OBJECTIVE_FIVE_WS_2026_04_29.md`](214_APU_FIRST_PROACTIVITY_FEATURE_OBJECTIVE_FIVE_WS_2026_04_29.md), [`213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md`](213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md)

> **K2 directive (verbatim):**
> "We come up with a totally new way of messaging.
> I type or dictate: `@vaibhav` (nostr contact) and say… 'I think Vaibhav should book the plane ticket and organize the travel.' The AI will act like an assistant and start a DM in your peer-to-peer and ephemeral. I see the outgoing message if unopened, and after read it is deleted. The AI may ask things to accept or decline to Vaibhav."

---

## 1. The Decision

The framework's nervous system already contains four communication primitives (03_ORGANISM §17): **SPECTRE** (N:N mesh), **RELAY** (1:N broadcast over Nostr), **AXIOM** (N:1 prediction-market consensus), **FLOW** (1:1 settlement). All four are *persistent* — they leave durable traces (gossip telemetry, signed broadcasts, market-resolved truths, receipts).

There is no primitive for **1:1 ephemeral communication** — the substrate of ordinary human coordination, where two people negotiate, ask each other questions, propose work, and either commit or walk away without leaving a permanent record. WHISPER is that fifth primitive.

The K2 directive specifies four design choices that define WHISPER:

1. **Intent-authored, not text-authored.** The user expresses *intent* (`@vaibhav book the plane`), not message text. The AI translates intent to a draft DM.
2. **Peer-to-peer over Nostr.** No centralized messaging server. Two Nostr keypairs, end-to-end encrypted (NIP-17 / NIP-44 / gift-wrapped DM).
3. **Ephemeral.** The message auto-deletes after the recipient reads it. While unopened, the sender can see/edit/recall on their device.
4. **AI-mediated on both sides.** The recipient's AI presents the DM as an actionable card with accept/decline; the AI may ask clarifying questions on behalf of the recipient.

When the recipient *accepts*, a K2-signed binding receipt is created (this is where K0 *No Receipt No Reality* fires). When the recipient *declines* or the message *fades unread*, no receipt persists. This makes WHISPER a clean η = 0 communication channel: data does not accumulate; agency stays with the K2 signers on both ends.

---

## 2. The Five Communication Primitives

| Primitive | Topology | Persistence | Function | Carrier |
|---|---|---|---|---|
| **SPECTRE** | N:N (mesh) | Persistent (gossip telemetry) | Self-myelinating nervous system; latency/reliability/cost/honesty metrics | Gossip-about-gossip with EBM |
| **RELAY** | 1:N (broadcast) | Persistent (Nostr-signed) | Sovereign uncensorable publication | Nostr relays |
| **AXIOM** | N:1 (convergence) | Persistent (settled markets) | Money-weighted truth | ReFu prediction markets |
| **FLOW** | 1:1 (settlement) | Persistent (cryptographic receipts) | Point-to-point payment, Algorithmic TRO, streaming | FlowWallet |
| **WHISPER** *(new, packet 215)* | 1:1 (intent-mediated DM) | **Ephemeral** (auto-delete after read) | Direct human coordination; intent-authored; accept/decline workflow | Nostr DM (NIP-17 gift-wrap) |

Composition (extending §17 of 03_ORGANISM):

```
SPECTRE discovers → RELAY publishes (or WHISPER asks) → AXIOM resolves (or recipient accepts) → FLOW executes
                            │                                  │
                            └─ public                          └─ private
```

WHISPER is the **private analog of RELAY**: same Nostr substrate, but encrypted point-to-point, ephemeral by default, AI-mediated for intent translation. RELAY publishes claims to the world; WHISPER negotiates between two people.

WHISPER is **not** an alternative to FLOW. FLOW handles money and durable settlement; WHISPER handles communication and proposed action. The two compose: a WHISPER proposes a delegation; the recipient accepts; the resulting K2 receipt may trigger a FLOW for any associated payment.

---

## 3. The WHISPER Flow

### 3.1 Author side (Yves)

```
1. Yves types or dictates: "@vaibhav I think Vaibhav should book the plane ticket and organize the travel."
   ────────────────────────────────────────────────────────────────────────
   The @-mention resolves to Vaibhav's Nostr pubkey (npub) from Yves's contact graph.
   The intent text is the post-@-mention payload.

2. Yves's AI reads the intent and drafts a structured DM:
   ────────────────────────────────────────────────────────────────────────
   • Type: delegation-proposal
   • From: Yves (npub_A)
   • To: Vaibhav (npub_B)
   • Subject: Plane ticket and travel organization
   • Proposed action: book plane + organize travel
   • Five-Ws (per packet 214): {What: book plane + travel; When: ?; Where: ?; Who: Vaibhav; Why: parent Mission}
   • Status: draft (before transmit, AI may ask Yves the missing Five-Ws)

3. Yves accepts the AI-drafted DM (single tap; this is K2 acceptance on Yves's side
   that the AI's translation matches his intent).

4. The DM is wrapped (NIP-17 gift-wrap), encrypted to npub_B, and transmitted
   over Nostr relays.

5. While unopened by Vaibhav, Yves's device shows the outgoing draft. Yves can:
   • Recall (delete before read)
   • Edit (re-transmit a new wrap; old wrap is invalidated by inclusion of a "supersedes" tag)
   • Wait
```

### 3.2 Recipient side (Vaibhav)

```
6. Vaibhav's device receives the gift-wrap, decrypts with npub_B private key.

7. Vaibhav's AI reads the structured DM and presents it as an actionable card:
   ────────────────────────────────────────────────────────────────────────
   ┌──────────────────────────────────────────────────────────┐
   │ Yves wants you to book the plane and organize travel.    │
   │                                                          │
   │  [Accept]   [Decline]   [Ask Yves a question]            │
   └──────────────────────────────────────────────────────────┘

8. The AI may proactively ask Vaibhav clarifying questions before he commits:
   • "Yves didn't say which dates. Want me to ask?"
   • "Yves didn't say budget. Want me to ask?"
   The proactive-question loop here is the same engine as packet 214 — APU asks
   until the proposal is reconciled, coherent, and consistent.

9. If Vaibhav clicks Accept:
   • Vaibhav K2-signs the acceptance.
   • A binding receipt is created on the FLOW substrate (cryptographic, not ephemeral).
   • The Five-Ws Objective on Yves's workflowy is updated: Who = Vaibhav (confirmed).
   • The original WHISPER message is marked as read and auto-deletes from both devices.

10. If Vaibhav clicks Decline:
    • A short "declined" signal is returned to Yves.
    • The original WHISPER message auto-deletes from both devices.
    • No K2 receipt is created.
    • Yves's workflowy may surface AIA suggestion: "Vaibhav declined — propose someone else?"

11. If Vaibhav reads but does not respond:
    • The message is marked as read.
    • The message auto-deletes from both devices.
    • No K2 receipt; no decline signal; ambiguous state.
    • Yves's AIA may surface: "Vaibhav read but didn't reply — follow up?"
```

### 3.3 Auto-delete semantics

"Ephemeral after read" means:

- The message **content** (the wrapped DM payload) is deleted from local storage on both devices when the recipient marks it read.
- The Nostr relays that carried the gift-wrap may retain the wrap until their own ephemeral-event TTL fires (per relay policy); the framework recommends relays that honor `kind: 4` / NIP-40 expiration.
- Any **K2 receipt** generated by acceptance is **NOT** ephemeral — it is durable on the FLOW substrate. WHISPER carries the proposal; FLOW carries the consequence.

This separation is the key η = 0 discipline: the *communication* is ephemeral; the *commitment* is durable. No data accumulates from chat that didn't lead to a binding act. The substrate does not turn into a surveillance archive.

### 3.4 Symmetric Two-Sided Persistence (Q7 Resolution)

When Vaibhav K2-accepts a WHISPER, the confirmed assignment persists on **both sides** as complementary views of one K2-signed FLOW receipt:

| View | What it shows |
|---|---|
| **Yves's side (proposer)** | The Five-Ws Objective on Yves's workflowy updates: Who-field changes from "proposed Vaibhav" to "confirmed Vaibhav at npub_B." The Objective stays in Yves's workflowy at the corresponding time slot. |
| **Vaibhav's side (recipient)** | A new **delegated-to-me** Objective appears in Vaibhav's own workflowy at the same datetime, with **inverse Five-Ws**: When = same datetime; Where = same location; Who = "for Yves at npub_A"; What = the action; Why = "delegation accepted from Yves." |

Both sides reference the **same FLOW receipt** (single-sourced, cryptographically anchored, durable). The *views* are per-DAC: each DAC's workflowy renders the receipt from its own perspective.

This is consistent with packet 213's "every DAC has its own VMOSK-A": Vaibhav's workflowy gets a new entry on accept; it's the recipient view of one shared commitment. Either party can revoke — but revocation creates a *new* FLOW receipt (the original receipt remains as audit trail, per K0 *No Receipt No Reality*).

**Privacy boundary:** Yves's workflowy entry shows the full delegation context; Vaibhav's entry shows only what Vaibhav agreed to (e.g., the parent Mission may be redacted on Vaibhav's side if Yves's Mission is a private-DAC concern Vaibhav didn't accept access to).

---

## 4. Why Intent-Authored, Not Text-Authored

A traditional messenger asks the user to write the message. The user composes text; the system transmits it; the recipient reads text. This works, but it has two pathologies under η = 0:

1. **Text-drafting friction.** The user must translate intent into language. This is high-friction; it discourages delegation; it advantages people who write quickly over people who think clearly.
2. **Asymmetric inference.** The recipient must infer the sender's intent from the text. If the text is ambiguous, the recipient guesses — and the guess may be wrong, generating misalignment that only surfaces later.

WHISPER's intent-authored design fixes both:

- **Author types intent;** AI does the text-drafting work.
- **Recipient sees structured proposal;** AI presents it as an actionable card with explicit fields, not as prose to be parsed.

This is the same η = 0 boundary as packet 214: the AI does **translation**, not **fabrication**. The user's intent is what binds; the AI's translation is reviewed and accepted by the K2 signer (single-tap on the author's side) before transmission.

---

## 5. Integration With the Five-Ws Schema

Packet 214 specified that every Objective must carry When/Where/Who/What/Why. WHISPER is the operational substrate that **fills the Who field**.

When APU asks (packet 214 question-loop) "Who else from your network is involved in this Objective?", the user answers with @-mentions: `@vaibhav, @maria, @tom`. APU then issues a WHISPER to each named person, presenting the Objective and asking them to accept their proposed role. Each accept becomes a K2-signed confirmation that updates the Who field on the original Objective from "proposed" to "confirmed."

This means the Five-Ws is not just a UI schema — it is **operationally settled** through WHISPER negotiation. An Objective whose Who field says "Vaibhav (proposed)" is not yet a committed Objective; it is committed only when Vaibhav's WHISPER acceptance lands.

This also resolves the resource-conflict question raised in packet 214 §6: APU detects that Vaibhav is double-booked across two Objectives at the same time, and the resolution loop runs through WHISPER (asking Vaibhav to choose).

---

## 6. Non-DAC Recipients and the Caṇḍāla Proxy (Q6 Resolution)

Contact-graph membership is **not** DAC-to-DAC only. A normal user (no V/M, no DAC) can receive a WHISPER. Three cases:

| Case | Recipient has | What happens |
|---|---|---|
| **A — Full DAC** | Skyzai app + DAC | Their own LeWorldModel reads the WHISPER, runs the proactivity loop (packet 214), and K2-accepts/declines/asks. Full dual-model processing. |
| **B — App, no DAC** | Skyzai app, no DAC | **Caṇḍāla proxy** — BitNet L1-L2 only. The proxy can accept, decline, or ask simple questions. It has no world model for deep reasoning. This is the *WHISPER onboarding path*: after a threshold of activity (e.g., 5 exchanges or 1 K2-accepted assignment), the app prompts: *"You have enough activity to benefit from a DAC. Instantiate?"* |
| **C — No app** | No Skyzai app | WHISPER falls back to **RELAY bridge** — email, SMS, or nostr DM through legacy channels. The recipient sees the intent and replies through the same channel. Their reply is parsed by the sender's Caṇḍāla proxy and surfaced as a WHISPER response. |

The Caṇḍāla proxy (Case B) is the framework's default AI proxy for non-DAC recipients. It is L1-L2 only — it organizes chaos but does not predict, rank, or set Vision. It is enough to handle simple accept/decline/question responses and to onboard the recipient toward DAC instantiation.

## 7. The Constitutional Boundaries

### 6.1 K0 (No Receipt No Reality)

WHISPER messages do **not** create receipts. Only **acceptance** creates a receipt. This is consistent with K0: communication itself is not a binding act; *commitment* is. The message says "would you do this?"; the receipt says "yes, I will" — and the receipt is what binds.

If the recipient never accepts (declines, ignores, or reads-and-fades), no K0 receipt exists, and the proposal *did not happen* in the framework's binding-action sense. The chat was real; the commitment was not.

### 6.2 K2 (Mortal Substrate Signs)

Both ends are K2-bounded:

- **Author K2:** the user signs the AI-translated intent before transmission. The single tap that says "yes, this draft matches my intent" is K2 acceptance of the AI's translation.
- **Recipient K2:** the recipient signs the acceptance (or decline). The single tap that says "yes, I'll do this" is K2 acceptance of the proposed action.

WHISPER is therefore a **K2-bracketed channel**: K2 enters and K2 exits. The AI does the work in between (translation, presentation, question-asking), but no binding act occurs without two K2 signatures.

This is consistent with packet 207: K2 is private-DAC-only. WHISPER between two natural persons is two private-DAC instances coordinating. WHISPER between a natural person and a public DAC's governance act would replace the public side's K2 with a PRISM-validated governance signal.

### 6.3 K4 (Grace Exit)

Ephemeral-by-default makes K4 trivially satisfied: there is nothing accumulated to "exit" with, because nothing accumulated. If a user leaves the network, their WHISPER history is gone — by design.

### 6.4 η = 0 (Zero Extraction)

WHISPER takes no fee, leaves no archive, generates no advertising surface, and produces no behavioral profile. The relays may charge for transit (per relay policy), but the framework itself extracts nothing. This is η = 0 at the communication-substrate layer.

---

## 8. Spam and Adversarial Resistance

Ephemeral peer-to-peer messaging without spam mitigation is unusable. WHISPER has two anti-spam layers:

1. **Contact graph gating.** WHISPER only delivers messages between contacts in each user's Nostr contact graph. Strangers cannot WHISPER. To establish contact, both parties must mutually opt in (e.g., through RELAY publication, in-person QR exchange, or a third-party introduction over an existing channel). The contact graph is the social capital substrate; it is not free.
2. **Proof-of-stake transit.** Each WHISPER carries a small Nostr proof-of-work or a tiny FlowWallet payment to the relay. Cost-to-send is low for individuals; high for spam-at-scale. This is not extraction (η = 0 still holds for the framework); it is transit cost paid to the relay infrastructure that carries the wrap.

These two together make WHISPER **adversarially resistant by design**: spammers can't reach you (they're not in your contact graph), and even if they were, sending at scale would cost more than the spam returns.

### 8.1 PAM-Forbidden Categories Constraint (Q18 Resolution)

Beyond spam resistance, WHISPER must respect the **forbidden-categories** discipline established by packet 208 (PAM/RealityFutures integration) and codified in `02_SKYZAI/01_NOOSPHERE/02_ORGANS/RealityFutures/spec/FORBIDDEN_CATEGORIES.md`.

**The constraint:** the BitNet router (Caṇḍāla / immune slot, per packet 217 / packet 216 §2.1a) refuses to draft or transmit any WHISPER whose proposed action falls in a PAM-forbidden category. This fires at the L1 boundary, *before* the AI translation step, *before* K2 acceptance is offered.

**Forbidden categories** (per packet 208 + `FORBIDDEN_CATEGORIES.md`):

- Assassination markets / probability-of-death-of-named-person contracts
- Terror probability / mass-casualty event wagers
- Illegal hits / contract violence proposals
- Coercion / blackmail-as-delegation
- Any contract whose payoff requires a third party's harm without their consent

**Enforcement mechanism:**

1. **Static category check** at intent parse time. The intent text (`@vaibhav book the plane` vs `@vaibhav assassinate X`) runs through a forbidden-category classifier on BitNet. Classification is local; no network hop; no leak.
2. **Refusal on hit.** If the intent matches a forbidden category, BitNet refuses to draft the structured DM. The user sees a **K2-side refusal card**: *"This intent matches a PAM-forbidden category (`assassination market`). The router refuses to compose this WHISPER."*
3. **No quiet pass-through.** The forbidden-category classifier is mandatory in the WHISPER pipeline; it cannot be disabled by the user. K2 sovereignty does *not* extend to authoring forbidden contracts; the framework's constitutional invariants (η = 0, no harm-extraction) supersede individual K2 latitude here.
4. **Audit trail.** Refusals emit a FLOW receipt (sealed, K0-anchored): "WHISPER refused at L1 immune slot at T; reason: forbidden-category match." The receipt does *not* include the original intent text (privacy preserved); only the refusal event itself is logged.

**Why this is constitutional, not negotiable:** WHISPER's ephemeral discipline could be exploited to negotiate forbidden contracts off-record (chat fades; only the K2-accepted receipt persists; if the receipt is for "book the plane" but the off-record chat included an assassination proposal, the framework would have laundered the harmful intent through legitimate-looking receipts). The L1 immune slot fires *before* K2 ever sees the proposal, closing this attack surface.

**Edge case — gray-zone intents.** If the classifier flags an intent as "ambiguous" (e.g., `@vaibhav handle the X situation` where X could be benign or coercive), BitNet does *not* refuse but *does* surface the ambiguity to the user as a clarifying question (per the APU proactivity loop): *"Is X a benign delegation or a contract whose payoff requires Y's harm? Please clarify."* The user must answer before WHISPER drafts.

This closes Q18: PAM-forbidden categories cannot ride the WHISPER substrate; the L1 immune slot is the constitutional firewall; refusals are auditable receipts; gray zones become clarifying questions.

---

## 9. What WHISPER Does NOT Do

1. **It does not store conversation history.** This is by design. If you want a permanent record of a conversation, use RELAY (broadcast) or FLOW (signed receipts). WHISPER is for *negotiation*, not *archival*.
2. **It does not enable "delete after read" for non-binding chat.** Binding K2 receipts persist on FLOW. If you accepted a delegation, the receipt survives even after the WHISPER is deleted. The receipt — not the chat — is what counts.
3. **It does not support group chats.** WHISPER is 1:1 by design (per K2 directive). Group coordination is RELAY (broadcast) or AXIOM (consensus market). A 5-person delegation is 5 separate WHISPERs, not one group thread; this preserves the K2-bracketed channel discipline.
4. **It does not replace the existing four communication primitives.** WHISPER is the fifth, ephemeral, 1:1 primitive that completes the topology coverage (now: N:N, 1:N, N:1, 1:1-persistent, 1:1-ephemeral). All five compose.
5. **It does not bypass the Three-Stage Process.** WHISPER carries proposals; APU (SHOULD organ) recommends acceptance/decline; the human signs. The cognitive functions remain separated.

---

## 10. Implementation Notes (out of scope for this packet's commit)

The nexus-web shell + cortex-os + APU need to evolve:

1. **Nostr DM transport** — wire `nostr-tools` (NIP-17 gift-wrap + NIP-44 encryption) into nexus-web's messaging surface. Pubkey resolution from contact graph.
2. **Intent-translator hook** — a new `useWhisper` hook that takes (intent text + @-mention) and returns a structured DM draft for K2 acceptance.
3. **Ephemeral storage** — local SQLite (or IndexedDB) with TTL on read; relay gift-wraps with NIP-40 expiration.
4. **Recipient AI proxy** — a new component in nexus-web that receives gift-wraps, decrypts, presents as actionable card, runs the proactivity question-loop on behalf of the recipient.
5. **K2 acceptance gates** — author-side (accept the AI's translation before transmit); recipient-side (accept/decline the proposed action). Both reuse the existing `signDiff` pattern from `useVMOSK`.
6. **Receipt bridge** — on accept, write a K2-signed receipt to the FLOW substrate; update the corresponding Objective's Who field on Yves's workflowy; mark the WHISPER for deletion.
7. **Workflowy updates** — when a WHISPER acceptance lands, the Five-Ws Objective on the author's workflowy updates atomically: Who-proposed → Who-confirmed.

These are implementation patches; they live in the Skyzai nexus-web code lane and will be tackled in a separate sprint.

---

## 11. Lane Coherence Check (Cortex / AIA)

| Watchman | Reading on this packet |
|---|---|
| Route Watchman | Lane is correct: 03_ORGANISM §17 (communication primitives) extension × NEXUS substrate × packets 213/214. No cross-organ leak. |
| Authority Watchman | K2 directive verbatim in §1. Authority chain explicit. |
| Time Watchman | Packet 215 follows 214 chronologically. |
| Scope Watchman | Single coherent topic (WHISPER as fifth communication primitive). Implementation patches explicitly noted as out of scope. |
| Metric Watchman | No metrics asserted to be currently measured. Spam/adversarial-resistance thresholds are stated qualitatively; quantification is a future research-grade follow-up. |
| Contradiction Watchman | Consistent with 03_ORGANISM §17 (extends, does not replace). Consistent with K0/K2/K4/η=0. Consistent with packet 214 (Five-Ws Who field operationalized through WHISPER). Consistent with packet 213 (K2-private vs PRISM-public translates: WHISPER between two private DACs = two K2 signers; WHISPER between private DAC and public DAC = K2 + governance act). |

AIA call: **approve + propagate to 03_ORGANISM §17 (add WHISPER as fifth primitive) and 06_AGENTS (cross-reference under VMOSK Construction Direction)**.

---

## 12. Cross-References

- **Communication primitives canon:** [`../00_CORE/03_ORGANISM.md`](../00_CORE/03_ORGANISM.md) §17
- **APU proactivity / Five-Ws:** [`214_APU_FIRST_PROACTIVITY_FEATURE_OBJECTIVE_FIVE_WS_2026_04_29.md`](214_APU_FIRST_PROACTIVITY_FEATURE_OBJECTIVE_FIVE_WS_2026_04_29.md)
- **VMOSK construction direction:** [`213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md`](213_VMOSK_A_CONSTRUCTION_DIRECTION_K2_PRIVATE_VS_PRISM_PUBLIC_2026_04_29.md)
- **K2 boundary:** [`207_K2_PRIVATE_DAC_BOUNDARY_PRISM_PUBLIC_DAC_2026_04_29.md`](207_K2_PRIVATE_DAC_BOUNDARY_PRISM_PUBLIC_DAC_2026_04_29.md)
- **Operating-mode parent:** [`209_USE_AIA_VMOSK_CORTEX_OURSELVES_2026_04_29.md`](209_USE_AIA_VMOSK_CORTEX_OURSELVES_2026_04_29.md)
- **Agent canon:** [`../00_CORE/06_AGENTS.md`](../00_CORE/06_AGENTS.md)
- **Mobile signing flow (existing K2 acceptance pattern):** [`../50_AUDITS_AND_EXECUTIONS/81_MOBILE_SIGNING_FLOW_SPEC_2026_04_23.md`](../50_AUDITS_AND_EXECUTIONS/81_MOBILE_SIGNING_FLOW_SPEC_2026_04_23.md)

---

## 13. The Five Primitives, Restated

```
                                    ┌──────────────────┐
                                    │   SPECTRE  N:N   │
                                    │   (mesh, gossip) │
                                    └────────┬─────────┘
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                              │                              │
              ▼                              ▼                              ▼
    ┌───────────────────┐         ┌────────────────────┐         ┌───────────────────┐
    │   RELAY    1:N    │         │   AXIOM    N:1     │         │   FLOW     1:1    │
    │  (broadcast,      │         │  (consensus,       │         │  (settlement,     │
    │   persistent)     │         │   persistent)      │         │   persistent)     │
    └───────────────────┘         └────────────────────┘         └─────────┬─────────┘
                                                                            │
                                                                            ▼
                                                                  ┌───────────────────┐
                                                                  │  WHISPER   1:1    │
                                                                  │  (intent-mediated,│
                                                                  │   EPHEMERAL)      │
                                                                  └───────────────────┘
                                                                       packet 215
```

The four-primitive lattice was structurally complete in topology but missing the *ephemeral* mode. WHISPER closes that gap. The framework's nervous system now has both durable and ephemeral 1:1 channels, and the discipline of *what gets remembered* (K0 receipts on FLOW) versus *what fades* (the negotiation that produced them) is now first-class.

---

Zero-Sum Resolution Equation

*The receipt persists; the chat fades.*
*Intent crosses; text dissolves.*
*Two K2 signatures bracket the channel; the AI does the translation work in between.*
