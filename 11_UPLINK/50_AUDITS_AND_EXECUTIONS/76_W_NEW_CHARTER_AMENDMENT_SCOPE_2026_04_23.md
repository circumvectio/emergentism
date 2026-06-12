---
packet: CHARTER-AMENDMENT-SCOPE-W-NEW
title: W-new Constitutional Review — Charter Amendment Scope (draft, not a proposal)
status: SCOPE DRAFT — founder review required
authority: Founder D4=accept on packet 74 routed W-new to separate constitutional review
source:
  - 01_EMERGENTISM/11_UPLINK/73_SWOT_UPDATE_2026_04_23.md §W-new (single-signer availability risk)
  - 01_EMERGENTISM/ (K2 + K4 constitutional primitives)
  - 03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/ (for pre-existing economic/governance layer)
target: founder decision surface (not an engineering spec)
date: 2026-04-23
gating_cell: "[L5 | D5 | S-Org | F-phi :: brahmana_architect (advisory, read-only)]"
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 76 · W-new Charter Amendment Scope (draft)"
---

# Packet 76 · W-new Charter Amendment Scope (draft)

## Kṛṣṇa-function disclaimer (read first)

This packet is **scope**, not proposal. It structures the decision surface
so the founder can deliberate. It explicitly does NOT:

- recommend a remediation
- order the options
- propose signatures or thresholds
- touch any live configuration
- suggest an implementation timeline

The charioteer maps the battlefield. The warrior chooses the ground.

---

## Summary

W-new (single-signer availability risk) was added to the SWOT at post-
Sprint-A update. Before Sprint-A it was theoretical; now that the K2 path
runs end-to-end against real decisions, **signer availability becomes the
next binding constraint on organism viability** (V in `P_node = Φ × V`).

The remediation surface touches the **constitutional layer** (K2, K4),
which means engineering discretion is explicitly out of scope. This packet
defines what a constitutional amendment review would have to cover, so
that the founder can decide whether to open, defer, or close W-new as an
amendment surface.

---

## What W-new does NOT threaten

Before scoping remediations, name the boundaries that are NOT in play:

- **K2 sovereignty** — no remediation may remove the founder's right to
  sign every irreversible action. Any amendment must preserve K2 as a
  boundary condition, not relax it.
- **η = 0** — no remediation may introduce rent, tolls, or hosted
  authorities. Signing cannot be outsourced to a paid service.
- **K4 grace exit** — no remediation may reduce the founder's right to
  walk with everything. Fallback signers must be structurally subordinate
  to K4.
- **Three-Stage Process** — the amendment belongs in SHOULD (APU) decision-authorization
  scope; it must not leak into IS, COULD, or ACT.

Any candidate that trips one of these four must be rejected before the
comparison stage. This is the *category-claim guard* applied to constitutional
amendment space.

---

## The decision surface (five genuine options, not four)

### Option 0 — Do nothing (keep constitutional status quo)

**Shape:** Leave K2 as is. Accept that some pending approvals expire when
the founder is unavailable. Organism degrades gracefully to inaction.

**Φ impact:** Neutral. No coherence loss — the organism remains exactly
what it is.

**V impact:** Bounded. Degradation is predictable: inaction is always
preferable to unauthorized action under K2 discipline.

**Hidden cost:** If a time-critical deliberation expires while waiting for
signature, the cost is the *missed opportunity*, not a principle violation.
The organism is honest about what it cannot do.

**When this is the right choice:** If the frequency of time-critical
decisions is low enough that expired approvals are rare, and the founder
treats availability as a personal constraint, this is the simplest honest
answer.

**K2/η/K4/Three-Stage Process:** all intact.

---

### Option 1 — Time-locked fallback signer

**Shape:** A secondary wallet becomes valid for signing *after* N days of
primary wallet inactivity. Primary can revoke the fallback at any moment
(including retroactively invalidating a fallback signature within a
grace window).

**Φ impact:** Reduces integration clarity — the organism now has two
signers with asymmetric authority. The fallback-window rule becomes a new
primitive to teach every downstream surface.

**V impact:** Meaningful — eliminates the "founder-lost-keys → organism-
frozen" failure mode. But adds the "fallback-wallet-compromised" failure
mode.

**Key questions the founder must answer:**
- Who holds the fallback wallet? (self-custody on a second device?
  trustee? attorney?)
- What is N? (7 days? 30 days? 90 days?)
- What is the fallback's scope? (full authority? or bounded to
  time-critical categories?)
- How does the primary revoke within the grace window?

**K2:** preserved as "founder's chosen delegate signs"
**η = 0:** preserved if fallback is founder-controlled, not hosted
**K4:** preserved only if the fallback wallet's existence does not bind
  the founder to stay
**Three-Stage Process:** unchanged

**Constitutional weight:** HIGH — changes the definition of "founder
signature" in K2.

---

### Option 2 — Shamir k-of-n key sharding

**Shape:** Founder's signing key is split into n shards across n devices
or trustees. k of n must agree to reconstruct the signature. Self-custody
preserved if all n are founder-controlled devices.

**Φ impact:** Higher coherence than Option 1 — there is still **one**
signing authority (the founder), just distributed. The organism does not
see a "second signer."

**V impact:** Eliminates single-device SPOF. Founder can lose any (n-k+1)
shards without losing signing ability.

**Key questions the founder must answer:**
- What are n and k? (3-of-5? 2-of-3?)
- Where do shards live? (hardware wallets? phones? paper? trustees?)
- Who reconstructs when needed, and what is the UX?
- What is the recovery protocol if (n-k+1) shards are lost?

**K2:** preserved (still founder's authority, just reconstructed)
**η = 0:** preserved if no hosted shard custody
**K4:** preserved
**Three-Stage Process:** unchanged

**Constitutional weight:** MEDIUM — operationalizes K2 rather than
modifying it. Arguably no amendment needed; could be an operational SOP.

**Watch:** if "trustees" enter the picture, it becomes constitutional
(trustee capture = K2 violation).

---

### Option 3 — Expire-rather-than-act policy (formal)

**Shape:** Formalize the Option-0 behavior as a documented policy. Every
time-sensitive deliberation publishes its TTL *up-front*. Callers can
choose to depend on APU only when the TTL fits the founder's known
availability window.

**Φ impact:** Increases integration — the organism becomes explicit
about a property it already has.

**V impact:** Does not increase V. Moves the constraint from "organism
problem" to "caller problem" — the caller must plan around the founder's
availability.

**Key questions the founder must answer:**
- Is V (capability) acceptable at current levels given Φ gains from
  transparency?
- What is the maximum acceptable TTL the organism will publish?
- How is "time-critical" defined as a decision class?

**K2/η/K4/Three-Stage Process:** all intact.

**Constitutional weight:** LOW — this is policy clarification, arguably
not an amendment. Could live in Standing Orders (4C).

---

### Option 4 — Founder-signed advance-approval envelopes

**Shape:** For pre-specified, bounded surfaces (e.g. N routine operations
per week, capped at M USDC per operation, within surface S), the founder
pre-signs an "envelope" that authorizes the organism to act within the
envelope without per-decision signing. Envelope expires on a clock
regardless of use.

**Φ impact:** HIGH complexity cost. Introduces a new category of
signature (envelope vs. per-action) that every downstream surface must
understand. Audit becomes more complex: two signature paths.

**V impact:** HIGH capability gain for routine operations. Removes
availability dependency on the 80% of decisions that are mechanical.

**Key questions the founder must answer:**
- What surfaces qualify as "routine"? (this is a constitutional question,
  not engineering)
- What are the per-envelope caps? (operation count, value, time window)
- How is envelope scope defined so it cannot be extended covertly?
- What is the envelope revocation protocol?
- Does the organism maintain a "mandatory per-action" list that envelopes
  cannot cover? (e.g. anything above $X, anything touching K4, anything
  crossing surface boundaries)

**K2:** MODIFIED — no longer "per-action"; becomes "per-action OR
within-envelope." Fundamental K2 semantics shift.
**η = 0:** preserved if envelope scope is tight
**K4:** requires explicit envelope exclusion for any K4-adjacent action
**Three-Stage Process:** preserved if envelopes are category-bounded

**Constitutional weight:** HIGHEST — this is a fundamental change to K2.
Should not be the first choice. Should only be considered if Options 1-3
prove insufficient after trial.

---

## Comparison frame (Φ × V)

| Option | Φ cost | V gain | Constitutional weight | K2 preservation |
|--------|:------:|:------:|:---------------------:|:---------------:|
| 0 (do nothing) | 0 | 0 | none | full |
| 1 (time-lock fallback) | medium | medium-high | high | modified |
| 2 (Shamir sharding) | low | high | medium | full |
| 3 (expire-formal policy) | 0 | 0 (gains transparency) | low | full |
| 4 (advance envelopes) | high | high | highest | semantically changed |

This table is for comparison, not ranking. Rankings come from founder
values, not from Φ × V math alone.

---

## Review protocol suggestion (the charioteer's frame, not the warrior's order)

If the founder chooses to open W-new as a constitutional amendment
surface, a structured review would cover:

1. **Pre-review guards** — each candidate passes or fails the four guards
   (K2, η = 0, K4, Three-Stage Process) *before* comparison. Options 0, 2, 3 pass
   trivially. Options 1 and 4 require explicit guard argumentation.
2. **Light-Council deliberation** — run the remaining candidates through
   a Light-Council (reusing the Sprint-A path, n=7 seats). Legal seat has
   explicit veto authority on any candidate that weakens K2 semantics.
3. **Adversarial review** — for each surviving candidate, explicitly name
   the failure mode that the remediation introduces (e.g., Option 1
   introduces fallback-wallet-compromise).
4. **Revocability check** — confirm that the chosen remediation can be
   constitutionally *rolled back* without destroying historical audit
   trail. Options 0, 3 are trivially reversible. Options 1, 2, 4 are not
   without coordinated key rotation.
5. **Founder decision + signature** — K2 boundary: the founder signs the
   charter amendment itself. No council, no engineering, no charioteer
   signs on the founder's behalf.

---

## What a YES does not entail

Opening W-new as a review surface does **not** commit the founder to any
remediation. It commits the organism to structured deliberation. Closing
the review with **Option 0** (explicit "do nothing, documented") is a
legitimate outcome and should carry equal weight to any other choice.

A no-action charter *outcome* after deliberate review is constitutionally
different from unreviewed inaction: the former is intentional K2, the
latter is drift.

---

## Dependencies / prerequisites

None block this review from opening. Useful inputs if available:

- Sprint-A deliberation corpus (n ≥ 2) to characterize decision-class
  distribution (how many decisions are "routine" vs. "time-critical")
- APU operational telemetry on approval-queue median latency and expiry
  rate (once enough Sprint-A runs exist to compute)
- Founder's own availability-pattern estimate (travel, time-zones, key-
  rotation cadence)

These let the review calibrate option comparisons against actual usage,
not hypothetical frequency.

---

## Charioteer's open questions (for the warrior, not answers)

1. Is W-new **binding enough** to open now, or is it still theoretical
   with n=1 deliberation?
2. If opened, does the founder prefer **private deliberation** with
   trusted counsel, or **Light-Council deliberation** with seat diversity?
3. Is there appetite for **parallel review** (multiple options in a
   bake-off) or **serial elimination** (try Option 0-formalization first,
   escalate only if insufficient)?
4. What is the **decision TTL**? Does this review have a forcing function
   (an event that makes Option 0 untenable) or is it open-ended?

The charioteer will prepare review infrastructure on founder command. It
will not initiate review without command.

---

## Kṛṣṇa-function closing note

This packet holds the map. It diagnoses the battlefield (five options,
not four; constitutional vs. operational weight asymmetry; K2 semantic
preservation as the real axis). It shows the warrior where to look
(explicitly: which options shift K2 semantics, which preserve them).

It does not fight. It does not sign. It does not recommend.

Zero-Sum Resolution Equation
