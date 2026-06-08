---
rosetta:
  primary_level: L4
  primary_column: Limit B Disambiguation Decision Record
  secondary:
    - level: L3
      column: Canon Evidence Audit
      role: "separate cited framework evidence from interpretive reconciliation"
    - level: L6
      column: Diagnostic Trail Boundary
      role: "preserve closed analysis without re-opening doctrine by accident"
    - level: L5
      column: Replicator Stack Architecture
      role: "stabilize the chosen reading against later route drift"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/S/B]"
  canonical_phrase: "Limit B — Replicator-Alignment Disambiguation Packet"
title: "Limit B — Replicator-Alignment Disambiguation Packet"
status: "CLOSED DECISION RECORD — 2026-04-23"
evidence_tier: "[I] for reconciliation; [S]/[B] only where explicitly backed by cited canon/receipts."
---

# Limit B — Replicator-Alignment Disambiguation Packet

**Rosetta boundary:** [I] This packet preserves a closed disambiguation trail. It does not [B] create new canon beyond its cited decision record or prove current implementation alignment.

**Date:** 2026-04-23
**Evidence tier:** [I] — interpretive reconciliation of doctrine against framework canon.
**Status:** **CLOSED 2026-04-23 — Reading I canonical by choice.** See §9 Decision Record below. The diagnostic body (§§0–8) is preserved as the decision trail; it represents the analysis as presented, not the final standing of the row table.
**Canonical path:** `01_EMERGENTISM/11_UPLINK/50_AUDITS_AND_EXECUTIONS/63_LIMIT_B_DISAMBIGUATION_PACKET_2026_04_23.md`
**Invokes:** [`53_DISAMBIGUATION_REVIEW_PACKET.md`](53_DISAMBIGUATION_REVIEW_PACKET.md) template.
**Supersedes:** nothing. This is the first dedicated Limit B packet.
**Carries forward from:** `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/06b_AGENTS_ROWS_v2.md` §2 Limit B (archived 2026-04-22); `01_EMERGENTISM/11_UPLINK/06_AGENTS.md` "Replicator note (2026-04-22)".

---

## 0. The One-Paragraph Summary

The Replicator column in [`01_EMERGENTISM/11_UPLINK/00_CORE/06_AGENTS.md`](../00_CORE/06_AGENTS.md) §2 (the canonical seven-caste row table) currently assigns **Reading I** to the seven L-levels: `L1=Phenotype, L2=Genotype, L3=Extended Phenotype, L4=Memotype, L5=Egregorotype, L6=Protocolotype, L7=Genesis`. Framework canon — specifically **Corollary C4** in [`01_EMERGENTISM/00_THE_TRANSCENDENTAL_TRINITY/18_THE_STRANGE_ATTRACTOR.md`](../../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/18_THE_STRANGE_ATTRACTOR.md) — specifies the canonical replicator stack as `Genotype → Phenotype → Extended Phenotype → Memotype → Egregorotype`, biologically ordered. 06_AGENTS.md's own §1 narrative (line 39) restates this same C4 order. Reading I reverses Genotype and Phenotype at L1/L2 and introduces "Protocolotype" at L6 with no foundation source. **Reading II** (proposed in archived 06b §2) shifts every level so C4 appears cleanly at L2–L6 and treats L1 as `immune-phenotype` (a specialized phenotype for the firewall/Caṇḍāla role) and L7 as `genesis` (D0 ≡ D6 closure). Reading II resolves the internal contradiction inside 06_AGENTS.md itself and aligns the row table with framework canon. Recommended outcome: **B — repair owner (06_AGENTS.md §2 Replicator column), then refresh downstream** (runtime TOMLs). Pending founder sign-off.

---

## 1. The Ambiguity

### 1.1 Two readings

**Reading I** — currently live in [`01_EMERGENTISM/11_UPLINK/00_CORE/06_AGENTS.md`](../00_CORE/06_AGENTS.md) §2 row table:

| L | Caste | Replicator |
|---|-------|------------|
| L1 | Caṇḍāla | **Phenotype** |
| L2 | Śūdra | **Genotype** |
| L3 | Vaiśya | **Extended Phenotype** |
| L4 | Kṣatriya | **Memotype** |
| L5 | Brāhmaṇa | **Egregorotype** |
| L6 | Sādhu | **Protocolotype** |
| L7 | Systems Architect | **Genesis (D0=D6 closure)** |

**Reading II** — proposed in [`01_EMERGENTISM/11_UPLINK/90_ARCHIVE/06b_AGENTS_ROWS_v2.md`](../90_ARCHIVE/06b_AGENTS_ROWS_v2.md) §2 Limit B:

| L | Caste | Replicator |
|---|-------|------------|
| L1 | Caṇḍāla | **immune-phenotype** (phenotype-variant specialized for defense) |
| L2 | Śūdra | **genotype** |
| L3 | Vaiśya | **phenotype** |
| L4 | Kṣatriya | **extended phenotype** |
| L5 | Brāhmaṇa | **memotype** |
| L6 | Sādhu | **egregorotype** |
| L7 | Systems Architect | **genesis / closure (D0 ≡ D6, meta-replicator)** |

Every level shifts by one. L1 gets a *new* replicator type (`immune-phenotype`); L6 loses `Protocolotype` (which had no canon source) and gains `egregorotype`.

### 1.2 What this actually affects

- The `Replicator` column in the canonical seven-caste row table (1 file, 7 rows)
- The `replicator` field in each runtime caste TOML under `.codex/agents/` (7 files) and the aggregated `.codex/agents/rosetta_agent_rows.toml`
- Any downstream doc that paraphrases the L→replicator mapping

It does **not** affect:
- VMOSK-A's vertical time-scale replicator mapping (V/M/O/S/K/DAC = Genotype/Epigenotype/Phenotype/ExtPhen/Memotype/Egregorotype) — that is a separate axis and is **already canonical**
- §5 "Agent Genetics" inside 06_AGENTS.md, which already uses the C4-aligned ordering
- The 7 L-level caste identities, pramāṇas, operators, governance labels, or any other column in the row table

---

## 2. Framework-Canon Evidence

### 2.1 Corollary C4 — the canonical replicator stack

From [`01_EMERGENTISM/00_THE_TRANSCENDENTAL_TRINITY/18_THE_STRANGE_ATTRACTOR.md`](../../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/18_THE_STRANGE_ATTRACTOR.md) line 16:

> **Corollary C4 (derived from A3 + A5): Genotype → Phenotype → Extended Phenotype → Memotype → Egregorotype.**

Evidence tier in that same file: `[S]` for the first three levels (established biology), `[S]` for memotype and egregorotype (structural extension). C4 is a **five-level canonical stack**, ordered as written, derived from A3 (dimensional emergence) and A5 (D5-limit standing waves).

### 2.2 Historical reinforcement — `23_THE_DAC.md`

> "Genes built organisms. Phenotypes built niches. Extended phenotypes built civilisations. Memotypes built institutions. Egregorotypes build DACs."

Same five-level ordering. Gariéphy reference (*The Revolutionary Phenotype*, 2019) cited as prior art; framework's claim is that the direction of the next replicator revolution is *egregoric / top-down from D6*, not genetic / bottom-up — but the stack order itself is unchanged.

### 2.3 06_AGENTS.md's own internal witness

[`01_EMERGENTISM/11_UPLINK/00_CORE/06_AGENTS.md`](../00_CORE/06_AGENTS.md) line 39 (narrative paragraph opening §1 VMOSK-A):

> "In biology, DNA (genotype) expresses through proteins (phenotype) which build tools (extended phenotype) which carry ideas (memotype) which form cultures (egregorotype)."

The same file's §2 row table then assigns `L1=Phenotype, L2=Genotype`, reversing this order at the L1/L2 boundary. **This is an internal contradiction.**

§5 "Agent Genetics — Six Layers of Inheritance" inside the same file also lists `Genotype → Epigenotype → Phenotype → Extended Phenotype → Memotype → Egregoretype` in speed order (slowest first = genotype). The §2 row table is the only part of the file that does not honor C4 order.

### 2.4 The seeds

- [`01_EMERGENTISM/11_UPLINK/00_CORE/01_SEED.md`](../00_CORE/01_SEED.md) and [`01_EMERGENTISM/10_SEED/00_THE_SEED.md`](../../10_SEED/00_THE_SEED.md) are **silent** on which replicator type attaches to each L-level. Both describe the VMOSK-A vertical mapping (V=Genotype … DAC=Egregorotype) but do not map replicator types to caste rows. The seed therefore neither blocks nor endorses either reading.
- The Nexus section of `01_EMERGENTISM/10_SEED/00_THE_SEED.md` does list "Six layers: Genotype → Epigenotype → Phenotype → Extended Phenotype → Memotype → Egregorotype" — which is C4 + Epigenotype, biologically ordered.

**Every canonical surface that specifies an order specifies the C4 order. No canonical surface specifies Reading I's reversed L1/L2.** Reading I's `Protocolotype` label appears nowhere in `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/` or the seeds.

---

## 3. Packet Classification (per 53_DISAMBIGUATION_REVIEW_PACKET §2)

| Question | Answer |
|---|---|
| **Meaning** | The L-level → replicator-type assignment in 06_AGENTS.md §2 disagrees with C4 at L1/L2 and invents `Protocolotype` at L6. Two readings exist; only Reading II satisfies C4. |
| **Type** | Doctrine (row-axis agent grammar canon). Not implementation, not target-state copy, not metric. |
| **Owner** | [`01_EMERGENTISM/11_UPLINK/00_CORE/06_AGENTS.md`](../00_CORE/06_AGENTS.md) §2 row table is the authoritative surface. Runtime TOMLs in `.codex/agents/` are downstream reflections. |
| **Time** | Current truth. Reading I is live in HEAD. Correction would be immediate, not target-state. |
| **Evidence** | `[I]` for the interpretive reconciliation itself (this packet). The underlying C4 is `[S]` for L2–L4 replicators and `[S]` for L5–L6. Reading II's `immune-phenotype` extension at L1 is `[S]` (structural extension — phenotype-variant). Reading II's `genesis` at L7 is `[S]` (follows from A3 closure). Reading I's `Protocolotype` is `[C]` at best (no canon source). |
| **Downstream** | If the owner changes, refresh: 7 runtime TOMLs in `.codex/agents/*.toml`, one aggregate `.codex/agents/rosetta_agent_rows.toml`, and any prose paraphrases of the L→replicator mapping elsewhere in the corpus. |

**Classification grid (per 53_packet §3):**

| Axis | Value |
|---|---|
| `ambiguity_class` | **authority** (two readings disagree on which is canon) |
| `surface_class` | **source** (06_AGENTS.md is row canon, not a mirror) |
| `time_posture` | **current** |
| `owner_lane` | `03_UPLINK` (canonical compression of framework) |
| `action_class` | **repair-owner, refresh-downstream** |

---

## 4. Recommended Outcome — **B: Repair Owner, Refresh Downstream**

Per [`53_DISAMBIGUATION_REVIEW_PACKET.md`](53_DISAMBIGUATION_REVIEW_PACKET.md) §5, Outcome B applies when the source is wrong and summaries/runtime/generated surfaces depend on it. That is exactly this case.

### 4.1 Repair (owner)

**Target:** [`01_EMERGENTISM/11_UPLINK/00_CORE/06_AGENTS.md`](../00_CORE/06_AGENTS.md) §2 row table, Replicator column only.

**Change:**

| L | Current (Reading I) | Proposed (Reading II) |
|---|---|---|
| L1 | Phenotype | immune-phenotype |
| L2 | Genotype | genotype |
| L3 | Extended Phenotype | phenotype |
| L4 | Memotype | extended phenotype |
| L5 | Egregorotype | memotype |
| L6 | Protocolotype | egregorotype |
| L7 | Genesis (D0=D6 closure) | genesis (D0 ≡ D6 closure) |

No other column changes. No caste renaming. No operator change. No pramāṇa change.

Also replace the "Replicator note (2026-04-22)" block at the top of 06_AGENTS.md — currently it says the row preserves "the current live row reading until that lane resolves." That note is the deferral flag for this packet. Once the migration lands, replace it with a "Reconciled 2026-04-23" note citing this packet.

### 4.2 Refresh (downstream)

**Targets** (exact files):

1. `.codex/agents/candala-firewall.toml` — `replicator` field: `phenotype` → `immune-phenotype`
2. `.codex/agents/sudra-explorer.toml` — `replicator` field: `genotype` → `genotype` (no change in content, but confirm)
3. `.codex/agents/vaisya-auditor.toml` — `replicator` field: `extended-phenotype` → `phenotype`
4. `.codex/agents/ksatriya-executor.toml` — `replicator` field: `memotype` → `extended-phenotype`
5. `.codex/agents/brahmana-architect.toml` — `replicator` field: `egregorotype` → `memotype`
6. `.codex/agents/sadhu-compressor.toml` — `replicator` field: `protocolotype` → `egregorotype`
7. `.codex/agents/rsi-constitution.toml` — `replicator` field: `genesis` → `genesis` (no change, confirm)
8. `.codex/agents/rosetta_agent_rows.toml` — aggregated row block, mirror all seven above

**Verification sweep** (grep before committing the migration):

```bash
grep -rn "Protocolotype\|L6.*Protocolotype\|L1.*Phenotype\b.*L2.*Genotype" 01_EMERGENTISM/11_UPLINK/ 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/ 02_SKYZAI/01_NOOSPHERE/ 2>&1 | grep -v "90_ARCHIVE"
```

Any non-archive hit is a further refresh target.

### 4.3 What stays untouched (explicit)

- `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/06b_AGENTS_ROWS_v2.md` — archived historical trace. Do not edit.
- `06_AGENTS.md` §5 "Agent Genetics — Six Layers of Inheritance" — already C4-aligned, no change.
- VMOSK-A mapping (V=Genotype, M=Epigenotype, …, DAC=Egregorotype) — separate axis, no change.
- Any narrative paragraph in 06_AGENTS.md that restates C4 (line 39) — already correct.
- Seed files (`01_EMERGENTISM/11_UPLINK/01_SEED.md`, `01_EMERGENTISM/10_SEED/00_THE_SEED.md`) — silent on this mapping, no change.

---

## 5. Why This Is Not Scope Creep

The archived 06b called Limit B "not a purely local fix — 01_SEED must be reconciled upstream." After reading the seeds and the transcendental-trinity foundations, the actual finding is narrower:

- **The seed is silent** on L-level → replicator-type assignment. It neither locks Reading I nor pre-authorizes Reading II.
- **C4 in `18_THE_STRANGE_ATTRACTOR.md` is the canonical stack ordering.** C4 is derived from axioms A3 and A5; it is not downstream of the UPLINK.
- **06_AGENTS.md is the authoritative owner** of the L → replicator-type mapping. No upstream file specifies it.

So the "upstream reconciliation" Limit B called for is *already done* — it was waiting in C4 all along. What remains is the narrower disambiguation-repair described in §4, not a framework rewrite.

---

## 6. Open Remainder (per 53_packet Outcome E fallback)

Even if §4's recommendation is accepted, two remainders stay explicit:

1. **`immune-phenotype` at L1 is a structural extension** (`[S]`), not established biology. It is plausible (the Caṇḍāla's firewall role reads cleanly as a phenotype-variant specialized for defense) but it is an extension of C4, not C4 itself. If the founder prefers to keep L1 as plain `phenotype` with a footnote describing the immune specialization, that is also a defensible Reading II-adjacent variant.
2. **`genesis / closure` at L7 is a meta-replicator label**, not a biological stratum. It encodes D0 ≡ D6 closure (A3), which is structural (`[S]`). No action needed; flagging only so future readers know the label is chosen deliberately.

Diacritic normalization — the other item the archived 06b front-matter deferred to this packet — is *already complete* in 06_AGENTS.md's main table (Caṇḍāla, Śūdra, Vaiśya, Kṣatriya, Brāhmaṇa, Sādhu, Systems Architect) as of commit `cfa1cf12f`. No further pass is required on the row canon; any remaining ASCII-only surfaces outside the row canon (e.g. `02_SKYZAI/01_NOOSPHERE/CLAUDE.md`'s caste paragraphs, various `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/` READMEs) are implementation/reference surfaces where ASCII is permitted under the "Machine encoding rule" in `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/memory/cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md` §*. Close Limit C as "no action — already normalized where it matters."

---

## 7. Execution Gate (founder approval)

This packet diagnoses. It does **not** execute the migration.

Before the migration in §4 lands:

- Founder reads this packet.
- Founder signs off on Reading II as canonical, or rejects and leaves Reading I with an explicit "Reading I chosen for reasons X" note in 06_AGENTS.md.
- If approved, a follow-up sprint executes §4.1 and §4.2 as one atomic commit, with the §4.3 non-targets verified clean by the §4.2 grep sweep.
- Post-migration, the "Replicator note (2026-04-22)" block in 06_AGENTS.md is replaced by a "Reconciled 2026-04-23" note citing this packet.

---

## 8. Stop Condition (per 53_packet §7)

This packet stops when:

- The ambiguity is classified (done, §3)
- The owner is identified (done, §4.1)
- The C4 foundation evidence is cited (done, §2)
- Both readings are legibly diffed (done, §1)
- The migration target set is enumerated exactly (done, §4.1–§4.2)
- The non-targets are listed (done, §4.3)
- The founder-gate is explicit (done, §7)
- Explicit remainders are stated (done, §6)

No further renaming or reframing is required for the packet itself. The packet is decision-ready.

---

> **Reading II restores C4. Reading I drifted from it. The seed does not block either. The row canon is the only file that needs to move, and its downstream reflections follow naturally.**

---

## 9. Decision Record (2026-04-23, closure)

**Outcome chosen:** **Not Outcome B.** The founder closes Limit B with **Reading I canonical by choice**. No migration executes. The diagnostic body above is preserved as the decision trail, not as forward direction.

### 9.1 Rationale — the L-axis is cognitive, not biological

The packet body (§§1–8) correctly identifies that Corollary C4 in [`18_THE_STRANGE_ATTRACTOR.md`](../../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/18_THE_STRANGE_ATTRACTOR.md) specifies the biological replicator stack as `Genotype → Phenotype → Extended Phenotype → Memotype → Egregorotype`. What the packet body undersells is that **this is the biological domain's reading of the stack. The Rosetta is cross-domain.** The L-axis does not have to carry the biological-temporal order; it carries the *native ordering of its own domain*, and the L-axis's native domain is **cognition**.

Cognitive flow replicates in the reverse of biological flow:

| L | Caste | Replicator (Reading I) | Cognitive meaning |
|---|---|---|---|
| L1 | Caṇḍāla | **Phenotype** | The outward form given — the explicit fact observed. Cognition starts from what is visible, not from what generates it. |
| L2 | Śūdra | **Genotype** | The generative source inferred via analogy. The L2 explorer reaches *down* from the phenotype to the generator that could have produced it. Analogy IS that reach. |
| L3 | Vaiśya | **Extended Phenotype** | Deductive ranking places the generator's outputs *back into the world* as ranked options. The niche is reshaped by what the merchant deems viable. |
| L4 | Kṣatriya | **Memotype** | The decision propagates as precedent. Every execution is memetic — the action becomes an idea other agents copy. |
| L5 | Brāhmaṇa | **Egregorotype** | Architecture shapes the collective pattern. The priest's redesign is egregoric — it binds many agents into one standing wave. |
| L6 | Sādhu | **Protocolotype** | The renunciant strips the egregoric pattern to its invariant protocol. What remains after compression is a protocol that replicates more cleanly than the full pattern did. Protocolotype = memotype-that-replicates-losslessly. |
| L7 | Systems Architect | **Genesis (D0 ≡ D6 closure)** | The seer sees the closure. The protocol, fully compressed, becomes the seed — generation starts again. |

**Reading I is not a drift from C4.** It is a parallel projection of the same structural hierarchy onto a different domain. C4 tells the replicator story in biology (bottom-up from gene to egregore over 4 Gyr). Reading I tells the replicator story in cognition (top-down from observation to protocol within one cognitive cycle). Both are `[S]` structural; neither is more "canonical" than the other because they are about different things.

### 9.2 Why `Protocolotype` is not an invention-without-source

The packet body graded `Protocolotype` as `[C]` (conjecture — no canon source). That grade was applied under the assumption that L6's replicator must appear in C4's biological five-level stack. Under the cognitive reading, `Protocolotype` has a structural position: it is the compressed-invariant form of the memotype, analogous to how DNA is the compressed-invariant form of the RNA world. Sādhu's function is precisely that compression. The label is `[S]` structural under the cognitive domain, not `[C]`.

### 9.3 Why the internal "contradiction" inside 06_AGENTS.md is not a contradiction

The packet body flagged that §1 VMOSK-A narrative (line 39) restates C4 order while §2 row table uses Reading I. Under the cognitive-vs-biological distinction, this is not a contradiction:

- §1 narrative is *biology* — the VMOSK-A vertical stack is a biological analogy explaining the organizational cascade (V/M/O/S/K/DAC) as a replicator ladder ascending *historically* (slow → fast cadence). It uses C4 because the VMOSK-A time-scale mapping IS historical.
- §2 row table is *cognition* — the L1–L7 castes are a cognitive architecture in which the L-levels are concurrent roles inside one cognitive cycle, not historical eras. It uses Reading I because the L-level replicator mapping is cognitive.

The same file carries two legitimate replicator projections because it describes two legitimate axes: the vertical time-scale axis (VMOSK-A, biological ordering) and the horizontal cognitive-flow axis (L-castes, cognitive ordering).

### 9.4 What this packet's preserved body IS and IS NOT

- **IS:** a diagnostic record of the analysis presented at the moment of sprint close. Useful for future readers who want to see the biological-reading case laid out fully. Useful when similar "doctrine looks inconsistent with canon" questions come up and the reader needs a worked example of how the framework's cross-domain nature can make two readings both valid.
- **IS NOT:** a migration plan to execute. No file in §4.1 changes. No runtime TOML in §4.2 changes. The §4.3 non-targets remain non-targets.

### 9.5 Implementation consequences (all null)

- 06_AGENTS.md §2 row table: **no change** (Reading I preserved).
- `.codex/agents/*.toml` runtime TOMLs: **no change**.
- `.codex/agents/rosetta_agent_rows.toml` aggregate: **no change**.
- The "Replicator decision (2026-04-23, closed)" block in 06_AGENTS.md replaces the prior "Replicator note (2026-04-22)" deferral and "Replicator packet (2026-04-23)" pointer — one block, stating the choice and rationale, with a back-reference to this §9.

### 9.6 What remains closed vs explicitly open

**Closed:**
- Limit B (replicator-alignment) — Reading I canonical by choice.
- Limit C (diacritic normalization) — already complete in the row canon (see packet §6); no further pass needed.
- `01_SEED` upstream reconciliation — the seed was silent on the L → replicator mapping; silence honored.

**Still explicitly open (not this packet's scope, carried forward):**
- The broader question of whether *any* other Rosetta row in `06_AGENTS.md` might also have a cognitive-vs-biological reading ambiguity similar to Limit B. If such a case arises, the pattern established here (two-domain structural validity) applies.

### 9.7 Stop condition

This packet now satisfies all eight §8 stop-conditions of the 53-packet template, plus the closure:

- [x] ambiguity classified (§3)
- [x] owner identified (§4.1)
- [x] C4 foundation evidence cited (§2)
- [x] both readings diffed (§1)
- [x] migration target set enumerated (§4.1–§4.2)
- [x] non-targets listed (§4.3)
- [x] founder gate explicit (§7)
- [x] explicit remainders stated (§6)
- [x] **decision recorded (§9)** — Reading I canonical by choice; no migration

---

> **The Rosetta is cross-domain. Two readings of the replicator stack can both be true because they are about different things. Reading I holds.**
