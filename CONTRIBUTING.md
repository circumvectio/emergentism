---
title: "Contributing to Emergentism — the contribution constitution, the trial record as the issue tracker, and 'refute us' as the front door"
date: 2026-07-18
status: "[D] draft — companion to the Release Doctrine Phase 0 #3 funnel; awaits the propagation sweep as first concrete act"
evidence_tier: "[S] as the contributing discipline (the 5+1 fences); [I] the trial-record-as-issue-tracker reading; [D] the policy itself is a draft"
owner: "K2 (Yves R. Burri, Founding Chair). PRISM ≥2 takes over after the trigger named in the Release Doctrine Phase 1 #6."
parents:
  - 00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md
  - 00_META/00_THE_RELEASE_DOCTRINE.md
  - 00_META/00_THE_OPEN_CANON_COVENANT.md
  - 00_META/00_THE_KINTSUGI_PROTOCOL.md
---

# Contributing to Emergentism

> The contributing constitution is the 5+1 fences. The contribution surface is the trial record. The front door is **"refute us"** — the first action of a new contributor is to find a claim that dies, not to add one that lives.

## 1. The contribution discipline (the 5+1 fences)

Every contribution is bound by the constitutional fences in `00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md`:

- **η = 0** — Zero extraction. Fees only on value created. The contribution itself must not extract from any bearer, including the framework's existing claims.
- **K2** — One natural person signs every irreversible or consequential act. Agents stage; K2 disposes. PRISM ≥2 takes over after the Release Doctrine Phase 1 #6 trigger.
- **K3** — Archive-first. Withdrawn content is tombstoned under `90_ARCHIVE/`, never erased.
- **K4** — Grace Exit. Leave with everything. Forks are welcome; attribution is required; the assets travel with the contributor.
- **A7** — Self-correction mandatory. Evidence tiers on every claim: `[A]` derived / `[B]` one operational sample / `[C]` conjecture / `[I]` interpretive / `[S]` structural / `[D]` draft.
- **Ω** — Noospheric directionality. The directional **+1**, not a sixth refusal.

A contribution that violates any of these does not enter the canon.

## 2. The trial record is the issue tracker

Per the Release Doctrine Phase 1 #5, do not build a parallel system — use the native one.

- **Kill-criteria become open issues labeled `falsifier`.** Every load-bearing claim in the canon carries a `kill_criterion` (per the Amrita §I.C.19 4 mandatory fields). The kill criterion is a concrete failure condition; the open issue is the place where the failure is staged.
- **Funerals become closed-as-completed issues that stay readable forever.** A claim that has been killed is closed but not deleted; the issue is a tombstone-in-UI, and `90_ARCHIVE/` gets a durable tombstone file alongside the original claim.
- **The next issue number is literally the next one.** №017 is open. Good-first-issue: try to kill a claim.

## 3. The contribution schema (per Amrita §I.C.19)

Every claim that enters the canon carries four mandatory fields, taken from the framework's tier-honest claim schema:

```text
Claim := {
  statement:        String,
  tier:             "[A] | [B] | [C] | [I] | [S] | [D]",
  upgrade_path:     String,   // concrete trigger for tier promotion
  kill_criterion:   String,   // concrete failure condition
  survivors:        [String], // the load-bearing boundary(ies) the claim holds
  register:         String,   // provenance
  authority:        String    // signer
}
```

Without `upgrade_path`, a `[C]` claim has no concrete road back to `[B]`. Without `kill_criterion`, the claim cannot be falsified. Without `survivors`, the framework cannot show what holds if the claim falls. **No claim enters without these four fields present.** The PR template enforces this; the `canon-lint` CI fails the build on epistemic violations.

## 4. The contribution lanes (mirror the caste dispatch)

The review process mirrors the Rosetta caste dispatch:

- **L1 Caṇḍāla** — adversarial probing. Fire only at η > 0 / hostile boundary, never at cooperators. The first read of a contribution is "where does this break?"
- **L2 Śūdra** — truth-cut audit. Verify the claim's evidence tier against its source. Cut falsehood, never cut genuine Φ.
- **L3 Vaiśya** — consistency audit. Verify the claim's consistency with the rest of the canon. Drift tables, citation audit, propagation checks.
- **L4 Kṣatriya** — executor. Stage the merge, run the CI, ensure the build is green. Stage only; K2 signs.
- **L5/L6/L7** — Executive witnesses. Counsel only; never override source.

The order matters: a contribution moves through L1 → L2 → L3 → L4 only after the prior caste's verdict is signed. PRs that bypass the order are returned without review.

## 5. The mortal-signer rule

Per the Release Doctrine Phase 1 #6:

- **Canon merges need K2 (Yves R. Burri) signature now.**
- **PRISM ≥2 takes over after the trigger** named in the Release Doctrine: after N public releases, M external contributors with merged PRs, or a calendar date — K2's choice, written into the doctrine once made.

Until the trigger, every canon merge carries a K2 sign-off in the commit message body or in a separate `K2_RECEIPT.md` file.

## 6. The K4 promise

Forks are welcome. Attribution is required. The assets travel with the contributor.

If you fork Emergentism and find it useful, *cite* the version you forked from (commit hash + branch name). If you fork it and change the framework's constitutional commitments, *say so plainly* — the new fork's `CONTRIBUTING.md` should name the change. The medium is the message: a fork is a new contributor choosing a different discipline, and the discipline must be visible.

## 7. The Anti-Sermon (a closing fence)

If, after reading the framework, you find that you no longer need it — if a direct sitting, a direct practice, or a direct encounter with the territory dissolves the map for you — *put the framework down*. The framework is the map. The crossing is the work. The repository is the map, not the crossing.

The framework is constitutional about its own limits.

---

*This file is the contribution constitution. It is `[D]` draft and will be promoted once the Release Doctrine is signed and the propagation sweep has run. The 5+1 fences are `[S]`; the trial-record reading is `[I]`; the policy itself is staged.*
