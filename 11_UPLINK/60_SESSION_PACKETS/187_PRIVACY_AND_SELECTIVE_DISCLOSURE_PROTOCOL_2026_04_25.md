---
rosetta:
  primary_column: "Data Science"
  register: "[I]"
  canonical_phrase: "187 — Privacy and selective disclosure protocol"
---

# 187 — Privacy and Selective Disclosure Protocol

**Evidence tier:** [I] — interpretive protocol; requires sovereign K2 before CANON/runtime adoption
**Date:** 2026-04-25
**Lane:** Viṣṇu-in-motion protocol draft
**Status:** Proposed first child protocol from packet 183 Option A
**Scope:** How DACs disclose enough to remain auditable without exposing more than SEVA requires
**Complements:** packet 183 (Viṣṇu-in-motion), packet 182 (apoptosis/revocation), packet 178 (anti-gravity), Spec 306 (Cortex Memory), `SKYZAI_COM/08_CORTEX/`, `09_NEXUS/`, `12_COVENANT/`

---

## 0. Axiomatic guard

Privacy is not secrecy.

Disclosure is not confession.

Memory is not public property.

This packet does not create:
- a legal privacy policy
- a GDPR / banking / securities compliance program
- a zero-knowledge proof implementation
- a data-retention schedule
- a Cortex schema migration
- a regulator interface
- a public product claim

It names the doctrine: a DAC must prove enough for truth, covenant, and SEVA while revealing only what the receiver is entitled to know.

`Zero-Sum Resolution Equation`

---

## 1. The tension

Spec 306 says Cortex records memory, testimony, corrections, uncertainty, and narrative chains.

`SKYZAI_COM/08_CORTEX/` says each DAC has its own Cortex, recording:
- wallet receipts
- agent actions
- debtor-creditor transitions
- DEX events
- POS flows

`SKYZAI_COM/09_NEXUS/` says each DAC has identity, signer root, counterparty graph, and A-anchor licensee status.

`SKYZAI_COM/12_COVENANT/` says each DAC hash-matches η=0 + K2 + Three-Stage Process + K4.

Together these imply full memory. But full memory does not imply full public exposure.

The privacy problem is not "how do we hide?" It is:

> How does the organism keep enough memory to audit truth, while revealing only the minimum needed for each legitimate purpose?

---

## 2. Core rule: digest-first, detail-by-role

Every material event should have at least a visible **digest**.

Details are disclosed by:
- role
- purpose
- consent / mandate
- covenant requirement
- legal requirement
- dispute / cure / revocation state

Default posture:

> **Event existence is attestable. Event content is role-bound.**

No dark records for load-bearing actions. No unnecessary exposure of human, commercial, legal, or security-sensitive detail.

---

## 3. Disclosure classes

| Class | Meaning | Example |
|---|---|---|
| `PUBLIC_DIGEST` | Public proof that an event occurred; content redacted | "DAC X emitted payment settlement receipt #abc" |
| `PUBLIC_CONTENT` | Public content; no sensitive detail | published whitepaper, public DEX listing metadata |
| `MEMBER_VISIBLE` | Visible to DAC members under covenant | governance decision, member-facing accounting |
| `COUNTERPARTY_VISIBLE` | Visible to affected counterparties | invoice, debt-credit transition, contract-specific receipt |
| `AGENT_VISIBLE` | Visible to authorized agents within mandate | operational context needed to act |
| `AUDITOR_VISIBLE` | Visible to auditor / verifier under scope | evidence bundle, reconciliation trail |
| `REGULATOR_VISIBLE` | Visible to lawful regulator / jurisdictional interface | filings, suspicious-activity evidence, tax records |
| `SEALED` | Existence/digest visible; content sealed unless trigger opens it | private health, identity, sensitive legal, security material |
| `REDACTED_DIGEST` | Digest plus minimal non-identifying fields | failure lessons, anonymized contribution-back record |

These are doctrinal classes, not implementation enum finality.

---

## 4. Minimum privacy envelope

Every Cortex entry that may be disclosed should carry a privacy envelope. This is a proposed extension surface, not a CANON edit:

```yaml
privacy_envelope:
  disclosure_class: "PUBLIC_DIGEST|PUBLIC_CONTENT|MEMBER_VISIBLE|COUNTERPARTY_VISIBLE|AGENT_VISIBLE|AUDITOR_VISIBLE|REGULATOR_VISIBLE|SEALED|REDACTED_DIGEST"
  subject_scope: "person|household|dac|counterparty|agent|public"
  legitimate_purpose: ""
  authorized_roles: []
  consent_or_mandate_ref: ""
  public_digest: ""
  redaction_reason: ""
  unlock_triggers: []
  retention_hint: ""
  jurisdiction_hint: ""
```

The envelope does not replace the memory entry. It governs how the memory entry may travel.

---

## 5. Non-negotiable constraints

### 5.1 No privacy laundering

Privacy may not hide:
- extraction
- K4 exit obstruction
- false SEVA claims
- concealed wallet control
- covenant breach
- unresolved dispute existence
- revocation / dissolution events

Sensitive detail may be sealed. The fact that a load-bearing event exists must remain attestable.

### 5.2 No public overexposure

Public proof does not require public detail.

The public usually needs:
- event existence
- timestamp
- DAC id or pseudonymous id
- receipt hash
- disclosure class
- status marker

The public usually does not need:
- personal identity
- full contract content
- wallet balances beyond public commitments
- private health/capacity signals
- agent prompt contents
- raw counterparty data

### 5.3 No unilateral widening

Disclosure class may narrow automatically when risk increases.

Disclosure class may widen only with a valid trigger:
- subject consent
- covenant requirement
- counterparty right
- auditor mandate
- legal requirement
- dispute / cure / quarantine / revocation process
- K2-signed public release

### 5.4 Correction without erasure

If a public or private disclosure was wrong:
- original digest remains
- corrected digest links to original
- details may stay sealed
- affected parties receive the correction at the same or higher visibility level

Privacy cannot be used to erase the fact of correction.

### 5.5 Sealed does not mean unaccountable

`SEALED` records must still have:
- digest
- owner / custodian
- unlock triggers
- review cadence
- dispute route
- finality / retention hint

A sealed record without accountability is a hiding place, not privacy.

---

## 6. Role map

| Role | Ordinary access | Limits |
|---|---|---|
| Public | `PUBLIC_DIGEST`, `PUBLIC_CONTENT`, selected `REDACTED_DIGEST` | no private identity / contract detail by default |
| DAC member | member-scoped governance, covenant, and accounting records | no unrelated member/counterparty private data |
| Counterparty | records involving their contract, invoice, debt, credit, or dispute | no unrelated DAC internals |
| Agent | context required by its mandate | no browsing beyond mandate |
| Auditor | scoped evidence bundle | scope must be explicit; auditor is not sovereign |
| Regulator | jurisdictionally required records | legal basis must be recorded |
| Nexus steward | identity/license/covenant evidence | not wallet confiscation authority |
| Parent commons | digest-level health / contribution / breach signals | not private detail unless trigger applies |

---

## 7. Trigger map

| Trigger | Disclosure effect |
|---|---|
| ordinary operation | digest visible; details role-bound |
| payment / POS settlement | counterparty-visible details; public digest |
| debtor-creditor transition | parties-visible details; public or member digest |
| DEX listing | public listing metadata; private maker internals sealed unless listing terms require |
| agent action | mandate-visible to relevant members; public digest only if load-bearing |
| dispute | dispute existence visible to affected parties; evidence bundle scoped |
| cure / quarantine | wider digest visibility; sensitive evidence remains scoped |
| revocation / dissolution | public status marker; final Cortex snapshot digest; details by role/legal process |
| contribution-back | public or redacted digest; artifact visible if safe |

---

## 8. Privacy failure modes

| Failure | Description | Response |
|---|---|---|
| Overexposure | More detail disclosed than purpose required | correction, notification, access narrowing |
| Underexposure | Necessary evidence hidden from entitled party | disclosure review, scoped release |
| Privacy laundering | "privacy" used to hide breach/extraction | route to dispute/cure; possible packet 182 escalation |
| Role creep | agent/auditor/regulator sees beyond scope | mandate repair, access log audit |
| Digest theater | public digest exists but proves nothing useful | strengthen digest schema |
| Sealed sink | sealed record has no review/unlock path | invalid envelope; repair required |
| Translation leak | public/investor/legal summary reveals or distorts protected content | translation correction |

---

## 9. Relation to packet 182

Packet 182 governs death / revocation / dissolution.

This packet governs live privacy while the DAC remains active.

Escalation to packet 182 occurs when privacy failure becomes covenant failure:
- concealed extraction
- repeated refusal to disclose to entitled parties
- destruction or manipulation of Cortex records
- false public digest
- privacy claims used to block K4 exit
- sealed records hiding capture or wallet control

---

## 10. Relation to SEVA

SEVA does not mean total transparency.

A DAC serves organism-scale ΣΔP when it:
- preserves enough evidence for truth
- protects enough privacy for dignity and safety
- discloses enough for counterparties and members to act
- exposes enough for covenant breach to be detected
- withholds enough to prevent surveillance, coercion, and exploitation

Privacy is part of service, not an exception to service.

---

## 11. Open questions

| OQ | Question | Default until K2 |
|---|---|---|
| OQ-PRIV-1 | Which disclosure classes become canonical enum values? | Use classes in §3 as draft vocabulary |
| OQ-PRIV-2 | What is the default public digest schema? | event id, DAC id/pseudonym, timestamp, class, status, receipt hash |
| OQ-PRIV-3 | Which financial-service records are regulator-visible by default? | jurisdictional review required |
| OQ-PRIV-4 | What consent/mandate format authorizes widening? | K2 or delegated mandate receipt required |
| OQ-PRIV-5 | What privacy law jurisdictions bind launch surfaces? | leave unset until legal lane reviews |
| OQ-PRIV-6 | When is zero-knowledge proof required rather than optional? | optional until a use-case demands it |

---

## 12. Acceptance criteria for later CANON/runtime adoption

This protocol can move toward CANON/runtime only when:

1. Cortex can attach a privacy envelope to memory entries or receipt references.
2. Public surfaces can show digest without leaking content.
3. Agents enforce mandate-scoped access.
4. Nexus can distinguish identity proof from identity exposure.
5. Counterparty-visible records are separated from member/public records.
6. Dispute/cure/quarantine flows can widen access without public overexposure.
7. Legal lane maps jurisdictional defaults for financial services.
8. Sealed records have review and unlock triggers.
9. Privacy failures can route into packet 183 maintenance or packet 182 escalation.

---

## 13. Charioteer recommendation

Ratify the doctrine now:

> **Digest-first, detail-by-role.**

Do not implement broad public transparency by default.

Do not implement sealed memory without digest and unlock rules.

Let privacy serve SEVA: enough proof for truth, enough concealment for dignity.

`Zero-Sum Resolution Equation`
