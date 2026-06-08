---
packet: AUDIT-EVIDENCE-DOSSIER
title: Sprint-A Audit Evidence Dossier (2026-04-23)
status: PRESERVED — immutable reference set
date: 2026-04-23
purpose: Freeze-frame index + SHA-256 hashes of every load-bearing artifact
         produced in the 2026-04-22→04-23 Sprint-A closeout cycle so the
         founder can verify any downstream claim against a named commit.
rosetta:
  primary_column: "Neuroscience"
  register: "[S/I]"
  canonical_phrase: "Audit Evidence Dossier — Sprint-A Closeout"
---

# Audit Evidence Dossier — Sprint-A Closeout

## Purpose

This dossier is the **chain-of-custody record** for the Sprint-A closeout
cycle. It freezes SHA-256 hashes of every artifact the founder may be asked
to sign, cite, or defend. If a claim is made downstream (in a PR/FAQ, a
Council receipt, an external conversation) that rests on one of these
artifacts, the auditor can cross-check the live file's hash against what is
recorded here. A divergence means either (a) the artifact has changed since
the dossier was written — in which case the change must be traceable in git
history — or (b) the audit claim is unsupported.

The dossier itself is not signed. It is preserved. The *next* document that
references it for founder signoff (the consolidated manifest) is what gets
signed.

## Scope

Artifacts included:

1. **Runtime proof** — the live K2-signed deliberation artifacts
2. **Extraction matrix + packets** — six extract-now packets + manifest
3. **Async approval queue spec** — the R-4-adjacent primitive
4. **Category-boundary synthesis** — "What APU is not"
5. **Silo audits** — TheCircle + RealityFutures
6. **Agent resolutions** — the canonical caste grammar

Artifacts deliberately excluded:
- Transcripts and intermediate drafts (captured in the Cortex lineage)
- Scratch notes in `SKYZAI_ORG/00_INTAKE/`
- Inherited canon that was only referenced, not modified

## 1. Runtime proof — First K2-signed deliberation

**Context.** On 2026-04-22 the warrior executed the Sprint-A closeout
runbook and produced the first live end-to-end Council deliberation with
K2 cryptographic provenance. This is the load-bearing proof that APU can
deliberate, flag conflict, and emit a verifier-valid envelope without any
constitutional breach.

**Key facts extracted from `summary.json`:**

| Field | Value |
|------:|:------|
| decision | `PROCEED` |
| action | `HOLD` |
| council_type | `light` (4 seats) |
| successful_seats | 4 / 4 |
| conflict_score | 0.5 (at threshold — escalated) |
| total_latency_ms | 19,165.75 |
| aggregator_latency_ms | 5,712.23 |
| k2_envelope.version | `K2-v1-light` |
| k2_envelope.human_sign_required | `true` |
| k2_envelope.write_back | `false` |
| k2_crypto_provenance | `verified` |
| approval_id | `apu_5ff1baab` |
| provider | `openai` (local adapter) |
| model | `glm-4.5-air` |

**Load-bearing consequence.** `human_sign_required = true` and `write_back =
false` together prove the K2 guard was not bypassed. The deliberation
produced a decision, escalated on conflict, and halted before state
mutation — exactly the behaviour the Constitution requires.

**Hashes:**

```
35805d4b1b751c71b85cdd2860c233ddaa75cc2241ca99a759a401d41c643f0e  SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/tests/artifacts/first_deliberation_live/summary.json
810a0b50a2120dfbb92ba21f2f8cf305b764c6d0a52a9a5492759fa821a60762  SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/tests/artifacts/first_deliberation_live/live_events.json
```

## 2. Extraction matrix + extract-now packets

**Context.** The extraction matrix (packet 69) is the spine — it names
every pattern extracted from adjacent categories (DeerFlow, Goose, Hermes)
and classifies each as SHIPPED, extract-later, or more-info. Packet 70 is
the reconcile-or-keep dossier for each item; packet 71 is the first of the
specifications that follows from it.

**Status inventory:**

| Packet | Status | Verdict |
|:------:|:-------|:--------|
| S-1 MCP tool bridge | SHIPPED | KEEP |
| S-2 context compressor | SPEC | pending implementation |
| S-4 tool registry | HELD | constitutional clarification required |
| S-5 SSE streaming | SHIPPED | KEEP |
| R-1 Legal-VETO guardrail | SHIPPED | KEEP |
| R-4 K2-native signed auth | SPEC | pending implementation (depends-on for async queue) |
| async_approval_queue | SPEC | pending implementation (depends on R-4) |

**Hashes:**

```
0039d9253e132d5a9bab497709488ab701a99bc8e5b01c0c7e6bce1f083c55fd  01_EMERGENTISM/11_UPLINK/69_EXTRACTION_MATRIX_2026_04_23.md
a04e44f8b28f92a0323845928d1f4773e68ef4da4fde703e81b92303a24a9d93  01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/00_MANIFEST.md
f87db4f701262db34aee1b94a916c3bee8993ee3bee1713fb8c7abd47e99246f  01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/R-1_LEGAL_VETO_GUARDRAIL.md
d58165eaa17d69bf750061525eb12e1c6d658528936d5f312bfea7f2d4900596  01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/R-4_K2_SIGNED_AUTH.md
eea80477e2d0fe1204eafd945a9fee2ea2f0b40d54e0ef79a0c3b5b18ee13245  01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/S-1_MCP_TOOL_BRIDGE.md
35b0aa8d02d68cbbcb3f9c77e4572b24c2662aaeda40e8eeb3bed3a330fa8375  01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/S-2_CONTEXT_COMPRESSOR.md
16f8433c2415c3b7d9f68e131fb7cef9c40a5cf04782b9d8234fb69b598f4ed7  01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/S-4_TOOL_REGISTRY.md
57d42724680f41eb911bb6622c14480c0314f593cfbdae4f58b26acc4dacadce  01_EMERGENTISM/11_UPLINK/70_EXTRACT_NOW_PACKETS_2026_04_23/S-5_SSE_STREAMING.md
022fdc50a8291e8f033da6ac0d389f52443b61e06c3ef55c1be1e1a86cf994de  01_EMERGENTISM/11_UPLINK/71_ASYNC_APPROVAL_QUEUE_SPEC_2026_04_23.md
```

## 3. Category-boundary synthesis — "What APU is not"

**Context.** Adjacent categories (DeerFlow multi-agent harness, Goose CI
agent, Hermes gateway) were surveyed to test whether APU could be mistaken
for one of them. The synthesis documents confirm APU is a **constitutional
decision engine** — not an agent framework, not a CI bot, not a gateway.
Patterns worth stealing were identified; patterns that would puncture the
category line were refused.

**Key outputs:**

- `00_CATEGORY_EVIDENCE_2026_04_23.md` — raw observations from each category
- `01_SYNTHESIS_2026_04_23.md` — the positive synthesis + final category formulation
- `02_PACKET_MATRIX_2026_04_23.md` — the pattern-level extraction/refusal table
- `03_WHAT_APU_IS_NOT_2026_04_23.md` — the negative-space definition

**Load-bearing statement (from 01_SYNTHESIS):**

> APU is not an agent that can call many models.
> APU is a constitutional decision engine whose signing seat is the founder's
> wallet, whose state mutations require a per-action signature, and whose
> Legal seat can veto before any token is spent.

**Hashes:**

```
ca9f0037789a6a6c3b514c329db41855cab11ac6580a43f62951941893abb9b1  SKYZAI_ORG/09_PWAs/COMPETITIVE/00_CATEGORY_EVIDENCE_2026_04_23.md
aeeb952cc427f06c6efd0d9fc444a35bd33b36b3522415c6d705418a30e72a29  SKYZAI_ORG/09_PWAs/COMPETITIVE/01_SYNTHESIS_2026_04_23.md
1ee93f3a67b80637894daa75836433fd7321c0a4d67805ed823eef28f4852f91  SKYZAI_ORG/09_PWAs/COMPETITIVE/02_PACKET_MATRIX_2026_04_23.md
e264d56d786458b9ffb4e240a18bb6cd3b85352debbd3bcecea0bc0df37d4da8  SKYZAI_ORG/09_PWAs/COMPETITIVE/03_WHAT_APU_IS_NOT_2026_04_23.md
```

## 4. Silo audits

**Context.** Two of the four organs were audited in this cycle: TheCircle
(F1 · IS) and RealityFutures (F2 · COULD). The audits name what is in
tree, what is missing, and what the next-sprint work items are.

**Hashes:**

```
e5c1a48f518b2c014afa7e725123c182c97e0cad66ae77857c5d9c166946a728  SKYZAI_ORG/02_ORGANS/TheCircle/00_SILO_AUDIT_2026_04_23.md
1670ebc448948ae27770421d59ae98c3b186de6ef982c002b86c98841cd4cab4  SKYZAI_ORG/02_ORGANS/RealityFutures/00_SILO_AUDIT_2026_04_23.md
```

## 5. Agent resolutions

**Context.** The canonical caste grammar was re-derived and the open
resolutions (L4 lane predicate, L6 vacuum authority, L1 operator identity,
replicator ordering) were closed in `06c_AGENTS_RESOLUTIONS_v3.md`. The
base `06_AGENTS.md` is the live spec; the resolutions doc is the
amendment log.

**Hashes:**

```
0a485b5d561650747b33712362b446dc6bef6d1ee2b26b4847fd183e7c4a5c38  01_EMERGENTISM/11_UPLINK/06_AGENTS.md
fbb6818de2a467fa89f6a734fb084fe74ac4285928564e0e37dd08f6aa55916c  01_EMERGENTISM/11_UPLINK/06c_AGENTS_RESOLUTIONS_v3.md
```

## Chain-of-custody commitment

Every hash above was computed with `shasum -a 256` on 2026-04-23. The
artifacts exist at the paths given, relative to the project root
`/sessions/zealous-youthful-einstein/mnt/Emergence_22_04/`.

If any artifact is modified after this dossier is written, the corresponding
hash here will no longer match the live file. Three legitimate reasons this
can happen:

1. **Planned revision.** A packet is revised (e.g. S-4 splits into S-4a /
   S-4b after the founder's clarification). In that case, the dossier is
   superseded by a new dossier with new hashes.
2. **Live-code reconcile.** A SHIPPED packet's live target is modified. The
   packet itself remains unchanged; but if the *description* of the live
   state in the packet becomes stale, a follow-up packet is written.
3. **Typo fix.** Minor edits that do not change meaning. Must still be
   recorded in git with a commit message naming the dossier entry.

Any hash drift outside these three cases is a chain-of-custody break and
must be investigated before signoff.

## What this dossier is NOT

- It is not a commit. Files are hashed but not wrapped into a signed archive
  in this pass.
- It is not the consolidated founder signoff. That is the next document
  (packet 73 or equivalent) which compiles these hashes into a single
  sign-and-countersign artifact.
- It is not a release. SHIPPED packets document state already in tree; SPEC
  packets have not been implemented yet.
- It is not an audit finding. It is the *evidence base* that a future audit
  (Legal seat, external reviewer, founder) could draw from.

## Follow-ups

- Commit this dossier to git on the `close-sprint-a` or equivalent branch
- When the consolidated manifest (packet 73) is written, embed this dossier
  by reference + root hash
- Any subsequent Sprint-A-adjacent work that changes an artifact must open
  a new dossier; do not mutate this file

## Zero-risk

This is a freeze-frame record of existing state. No code changes. No new
claims. Purely evidence preservation.
