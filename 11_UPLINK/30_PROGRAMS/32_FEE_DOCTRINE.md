---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "API PAY Fee Doctrine"
---

# API PAY Fee Doctrine

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*


> **Every fee must map to a receipt of value delivered. No fee may exceed the value it demonstrably creates.**

Date: 2026-04-16  
Status: Doctrine (Constitutional Guard for Gate 1)  
Canonical path: `32_FEE_DOCTRINE.md`

---

## 0. Purpose

External revenue is the first test of η = 0 discipline.

The moment Skyzai charges an external party, the organism risks the oldest trap: extracting more than it regenerates. This doctrine exists to make that trap structurally impossible.

---

## 1. The One-Sentence Law

**If a fee cannot be matched to a timestamped, receipted, human-legible proof of value delivered, the fee is illegal under the Constitution.**

---

## 2. The Three Fee Classes

| Class | Definition | Example | Constitutional Test |
|-------|------------|---------|---------------------|
| **Implementation fee** | Payment for setup, integration, or migration work | Onboarding a merchant to Skyzai Pay | Receipt shows hours worked, acceptance criteria met, merchant signature |
| **Usage fee** | Payment proportional to actual transaction volume or API call | 1% per successful payment routed | Receipt shows exact transaction count, amount, success status |
| **Evidence fee** | Payment for structured proof, accounting, or statement generation | Live statement export to auditor | Receipt shows statement generated, data coverage, delivery confirmation |

### What is NOT a fee class

- **Rent** — charging for mere access to a platform or relationship graph
- **Lock-in fee** — charging for export, migration, or Grace Exit
- **Vagueness fee** — "service charges" with no receiptable deliverable

These are η > 0 by definition.

---

## 3. The Fee-to-Receipt Mapping Rule

For every fee charged, the following must exist before the fee is finalized:

```
FEE
 ├── value_delivered: string (what the customer got)
 ├── receipt_id: string (link to OFN or internal receipt)
 ├── timestamp_start: ISO-8601 (when work began)
 ├── timestamp_end: ISO-8601 (when value was delivered)
 ├── customer_ack: boolean (customer confirmed value received)
 └── margin_check: fee_amount ≤ provable_value_estimate
```

No receipt → no fee.

---

## 4. The Margin Ceiling

**Fee amount must not exceed the conservative estimate of value delivered.**

| Scenario | Rule |
|----------|------|
| Implementation | Fee ≤ agreed scope × market rate for equivalent labor |
| Usage | Fee ≤ 50% of the cost savings or revenue gain the customer can receipt |
| Evidence | Fee ≤ cost of producing the evidence + modest margin (≤ 20%) |

If the customer cannot produce a receipt of value received, Skyzai must not charge.

---

## 5. Transparency Requirements

Every fee must be:
- **Disclosed before the transaction** (no post-hoc surprise fees)
- **Itemized** (no bundled mystery pricing)
- **Contestable** (customer can dispute and receive human review within 48 hours)
- **Refundable if value is not receipted** (fee auto-reverses if deliverable fails)

---

## 6. Forbidden Fee Patterns

| Pattern | Why it is forbidden |
|---------|---------------------|
| Charging for NEXUS keypair generation | K2 sovereignty must be free to the user |
| Charging for Grace Exit export | K4 is constitutional; monetizing it is extraction |
| Charging for connectivity graph visibility | Graph capital is a network property, not a SKU |
| Charging for API documentation or open specs | Open protocol literacy must not be paywalled |
| Charging for dispute resolution | The arbiter must not profit from conflict |
| Charging for connectivity graph visibility or `c(DAC)` scores | Graph capital is a network property, not a SKU; see `34_EXTENSION_GATE_CHECKLIST.md` |

---

## 7. The η = 0 Test for Any Proposed Fee

Before a new fee is approved, it must pass:

```
1. Can the customer produce a receipt of value received? [YES / NO]
2. Is the fee proportional to that value? [YES / NO]
3. Would the customer pay this fee again voluntarily? [YES / NO]
4. Does Skyzai profit if the customer fails? [NO]
5. Is the fee free of lock-in or coercion? [YES / NO]
```

Any NO means the fee is rejected.

---

## 8. Canonical Compression

> **Skyzai does not sell access. It sells demonstrated value. Every fee is a receipt-bound claim that must survive customer scrutiny.**

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Gate 1 protection — applies to all external revenue proposals.
2. **Your Next Action:** Review any proposed pricing sheet against the three fee classes and the η = 0 test.
3. **Expected Output:** A cleared pricing proposal with every line item mapped to a receipt type, or a rejection memo citing the violated rule.
4. **Success Criteria:** A founder can read your output and know exactly which fees are lawful and which are not.
5. **Canonical Path:** `32_FEE_DOCTRINE.md` (this file).

---

> *A fee without a receipt is a claim without proof. That is the definition of extraction.*  
> *eta = 0. K2 always.*
