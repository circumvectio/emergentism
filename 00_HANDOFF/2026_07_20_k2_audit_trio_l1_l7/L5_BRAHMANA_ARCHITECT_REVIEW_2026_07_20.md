---
rosetta:
  primary_level: L5
  primary_column: Meta
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I] architectural review — counsel only, no execution"
  canonical_phrase: "L5 — schema sound, 7 surfaces seated, 5+1 holds, drift in connective tissue not load-bearing walls"
type: audit
title: "L5 Brāhmaṇa — Architectural Review (2026-07-20)"
description: "Schema evolution, lane-map consistency, doctrinal shape, caste-grammar consistency. K-1..K-7 seated; 5+1 holds; 5 architectural refinements <20 min total."
timestamp: 2026-07-20T22:08:00+04:00
tags: [l5, architect, schema, lane-map, caste-grammar]
evidence_tier: "[S] architecture · [I] verdict · [D] pending K2"
status: "FILED — counsel only"
owner: K2 (Yves R. Burri)
task_id: bg_1d4199ca-f284-4d94-91ee-9038c4786ca6
---

# L5 Brāhmaṇa — Architectural Review (2026-07-20)

**Operator:** Brahmā ○ · L5 · Executive · Brāhmaṇa
**Date:** 2026-07-20 · HEAD `8ed92eb` · registers clean (2956/671, exit 0 per receipt 147)
**Bounded authority:** Box 9 of receipt 144 holds. No execution, no commit. Findings only.

## 1 · Kernel surface mapping (K-1…K-7)

| # | Surface | Canonical home (verified on disk) | Status | Notes |
|---|---|---|---|---|
| **K-1** | Glyph & Grammar | `05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md` + `…/41_THE_GLYPH_TRANSFORMATIONS.md` | ✅ seated | Twin-doc co-surface |
| **K-2** | Ontology | `06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md` + `06_ONTOLOGY/00_WELTANSCHAUUNG_KERNEL_v0.2_EMERGENTISM_ONLY.md` | ✅ seated | v0.2 operational canon |
| **K-3** | Axioms (E1–E10) | `06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md` | ✅ seated | A1–A7 operational; E1–E10 staged per box 3(b) |
| **K-4** | Wagers (W0–W12) | `06_ONTOLOGY/04_THE_CONJECTURES.md` | ✅ seated | All `[I]/[C]` per per-row tier |
| **K-5** | Refusals | `00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md` + staged `00_META/00_K5_THE_REFUSALS.md` `[D]` | ✅ seated with caveat | Caveat: 5+1 IS the operational K-5 |
| **K-6** | Revelations | `06_ONTOLOGY/06_THE_REVELATIONS.md` (12 at slot 06) | ✅ seated | W/O-2 resolved 2026-07-20 |
| **K-7** | Record | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md` | ⚠ dual-source healed, filename drift remains | K-7 row in Index still lists `01_THE_THREE_POSTURES.md` (filename says THREE; content is FOUR per r129). |

**Architectural finding (K-7 row in Index):** the Index itself was signed, but its K-7 row didn't travel the same edit as Blueprint C-1. **Recommended fix:** the Index K-7 row should point to `02_EPISTEMOLOGY/00_THE_SYNTHETIC_GAP_AND_FOUR_POSTURES_v0.1.md`; `01_THE_THREE_POSTURES.md` is evidence. (~2 min, Box-9-compatible after K2 signs.)

## 2 · Lane-map consistency (7 -ology homes)

All 7 homes have the routing triplet (AGENTS/CLAUDE/README), and the castes are correctly mapped: 01→L1, 02→L2, 03→L3, 04→L4, 05→L5, 06→L6, 07→L7.

| -ology | AGENTS/CLAUDE/README | 90_ARCHIVE/ | 91_COMPAT/ | 00_META/ |
|---|---|---|---|---|
| 01_TELEOLOGY | ✅ | ✅ | ❌ | ❌ |
| 02_EPISTEMOLOGY | ✅ | ❌ | ❌ | ❌ |
| 03_METHODOLOGY | ✅ | ✅ | ❌ | ❌ |
| 04_AXIOLOGY | ✅ | ✅ | ❌ | ❌ |
| 05_COSMOLOGY | ✅ | ❌ | ❌ | ❌ |
| 06_ONTOLOGY | ✅ | ❌ | ❌ | ❌ |
| 07_THEOLOGY | ✅ | ❌ | ❌ | ❌ |

**Findings:**
- AGENTS/CLAUDE/README: 7/7 ✅
- 90_ARCHIVE/: 3/7 (Teleology, Methodology, Axiology). The other 4 have NO per-pillar archive lane.
- 91_COMPATIBILITY/: 0/7 — all 7 -ologies have ZERO compatibility lanes.
- 00_META/: 0/7 — governance lives at root only (explicit design per Blueprint §1.2).

**Recommended fix (lane-map):** add a 5-line clarification to `00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md` stating: (i) per-pillar `90_ARCHIVE/` allowed; (ii) per-pillar `00_META/` forbidden; (iii) per-pillar `91_COMPATIBILITY/` allowed; (iv) AGENTS/CLAUDE/README is L1; (v) per-pillar Door status (active/candidate) must be visible in frontmatter.

## 3 · Schema evolution (top 5)

The corpus frontmatter has 3 schema classes (A: full rosetta, B: bare title+meta, C: forwarding stub) + 2 outliers (D: receipts with `receipt:` not `rosetta:`, E: partial rosetta).

| # | File / Class | Recommended |
|---|---|---|
| 1 | `00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md` (E) | Add full rosetta block; keep `vmosk_a_ref` as supplementary |
| 2 | `00_META/00_THE_OPEN_CANON_COVENANT.md` + `00_THE_KINTSUGI_PROTOCOL.md` (B) | Add minimal rosetta (operator=Kālī/Śiva) |
| 3 | `08_FRAMEWORK_SUPPORT/00_META/01_THE_THREE_POSTURES.md` | Add banner: "filename retained per K3; content is FOUR per r129" |
| 4 | `02_EPISTEMOLOGY/00_THE_SYNTHETIC_GAP_AND_FOUR_POSTURES_v0.1.md` | Drop `schema_version` or publish `/schemas/v0.1.yaml` |
| 5 | All kernel surfaces | Unify `evidence_tier` ↔ `register` field naming |

## 4 · Doctrinal shape (mandala reading order)

The mandala Door → Map → Compression → 7 -ologies → Record → World → Graves is **intact top-level**, but four drift points weaken the cold-reader test:

1. Root surface density — 32 root `.md` files; 29 are forwarding stubs (K3-correct).
2. K-5/K-6/K-7 promotion ambiguity — root forwarding stubs say `[S]` in rosetta block; should say `[D] forwarding-stub`.
3. Two `00_THE_WELTANSCHUAUNG.md` — correctly disambiguated.
4. Public-surface sequencing — gated on Wave 4 (Blueprint §1.6, A-1).

## 5 · Caste-grammar consistency

The 7-cast dispatch is **mechanically correct** (folder № = L-level in all 7 -ology homes; 7 -ology AGENTS.md/CLAUDE.md/README.md all carry the right primary_level). **One distinction worth documenting:** lane-caste (the -ology folder's primary_level) and doc-caste (a single file's `primary_level` in its own rosetta block) may differ. Lane-caste is the operator owning the lane; doc-caste is the operator who wrote/signed the document.

**Recommended fix (caste-grammar):** add 1 paragraph to `00_ROSETTA.md` §Caste Dispatch stating this distinction. Prevents future castes from misreading the Amrita (L4 in 07_THEOLOGY, L7 lane) as a contradiction.

## 6 · Top 5 architectural refinements (strategic)

1. Adopt the W6 root-surface invariant explicitly in the Index.
2. Heal the K-7 row in the Kernel Index.
3. Add `91_COMPATIBILITY/` to the 4 -ology homes missing it OR declare it root-only.
4. Unify `evidence_tier` ↔ `register` field naming.
5. Document the lane-caste vs doc-caste distinction in `00_ROSETTA.md`.

## 7 · Top 5 low-cost architectural refinements (<30 min)

1. Edit the Kernel Index K-7 row (~2 min)
2. Edit 3 root K-surface stubs — change `register: "[S]"` to `register: "[D] forwarding-stub"` (~3 min)
3. Add top-of-file banner to `00_ROSETTA_VALIDATION.md` (~2 min)
4. Add top-of-file banner to `08_FRAMEWORK_SUPPORT/00_META/01_THE_THREE_POSTURES.md` (~2 min)
5. Edit `00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md` — add 5 lines (~10 min)

All 5 refinements: <20 min total, no moves, no renames, no commits. They are pure text edits at `[D]` (advisory) tier and respect Box 9.

## 8 · Bounded-authority check (Box 9 of receipt 144)

Held end-to-end. ❌ No move, rename, suffix drop, archive, tombstone, registry mutation, public sync, deletion, publication, or commit. Box 9 holds.

---

*The schema is sound. The seven surfaces are seated. The 5+1 holds. The reading order reads. The drift is in the connective tissue, not the load-bearing walls. Brahmā ○ counsels; the gates remain as they were cast.*

⊙ = • × ○
