---
title: "Pin Custody — Owner Decision Docket"
date: 2026-08-14
status: "UNRATIFIED — selected option UNSET"
evidence_tier: "[B] exact-byte recoveries and mutation-tested custody behavior; [S] only after an owner selects an option"
type: owner-decision-docket
semantic_authority: none
selected_option: UNSET
scope: "legacy or frozen reviewed-source pins used by claim cards and book projections"
---

# Pin Custody — Owner Decision Docket

This docket does not add a settled-canon row. It separates an already enforced
repository safety rule from the still-unselected question of whether that rule
belongs in the doctrine registry.

## Facts already established `[B]`

1. A reviewed SHA-256 identifies exact bytes. It does not make those bytes true,
   current, canonical, public, or independently validated.
2. A missing or changed reviewed source fails closed. A convenient live file is
   not a replacement merely because its title or subject is familiar.
3. When the exact bytes survive at one uniquely matching custody path, the
   compiler may resolve that same-digest relocation while retaining the
   declared path, lifecycle, work, role, and revision in the generated record.
4. A semantic revision requires a new reviewed record. The predecessor remains
   recoverable and the change names its owner, date, evidence, and disposition.
5. The current claim-card compiler and its mutations already enforce these
   repository contracts. This docket must not be used to waive a missing card,
   changed source, ambiguous relocation, or unresolved owner decision.

## Decision

### Option A — ADOPT AS SETTLED DISCIPLINE

Add the rule to the change-and-failure owner and then register a fresh settled
canon identifier after auditing the identifier namespace. The adopted clause
must preserve all five facts above and must say explicitly that hash equality
is custody, not semantic warrant.

### Option B — KEEP OPERATIONAL ONLY

Retain the rule in claim-card and book tooling, tests, and receipts. Do not
represent a repository custody mechanism as doctrine.

### Option C — REJECT AS A GENERAL RULE

Remove any proposed doctrinal generalization while keeping each existing
reviewed-source contract fail-closed until its own source owner re-adjudicates
or retires it.

**Selected option: UNSET.**

## Ratification gate

Selection requires a dated owner disposition naming A, B, or C. If A is
selected, a separate execution receipt must identify the edited source owner,
the newly allocated registry identifier, every propagated checker/test
contract, and the mutation evidence. No model agreement, branch merge, byte
recovery, or green local gate counts as that selection.
