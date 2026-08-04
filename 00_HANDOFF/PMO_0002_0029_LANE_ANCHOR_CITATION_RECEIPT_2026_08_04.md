---
type: lane-receipt
title: "01_EMERGENTISM lane receipt — YAML alignment_fence anchor reconciliation + tidy-receipt citation repair"
date: 2026-08-04
dispatch: "00_HANDOFF/pmo/DISPATCH_L_01EMERGENTISM_2026_08_04.md (root lane)"
work_items: "PMO-0002 (lane part) + PMO-0029 (in-lane half)"
caste: "L4 Kṣatriya (01_EMERGENTISM lane session, opencode runtime)"
evidence_tier: "[S] scope discipline (mechanical ref repairs only, no doctrine change); [A] kill files and YAML anchors read from disk and compared; [S] stale/new paths grepped and ls-verified on disk 2026-08-04"
may_sign: false
may_authorize: false
---

# Lane receipt — anchors + tidy-receipt citation (2026-08-04)

## §1 · Act 1 — PMO-0002 (lane part): alignment_fence anchor reconciliation

Source of truth: root `00_HANDOFF/empirical_kills/` (READ ONLY — not edited from
this lane) — README "7/7 corpus-anchored as of 2026-08-03" + the four kill files.
All 7 YAMLs (`08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/agents/0{1..7}_*.agent.yaml`)
checked; 4 changed, 3 verified clean. YAML parse re-verified post-edit (7/7 OK). [A]

### Anchors changed (old → new, tail of `alignment_fence` after "empirical anchor")

| File | Old | New |
|---|---|---|
| `02_sudra_explorer.agent.yaml` (L2 Āmiṣa) | `Pūtanā-form (L2 stone brief :18)` | `2026-08-01 proposing-discipline hold (L2_AMISA_2026_08_03.md, root 00_HANDOFF/empirical_kills/; Pūtanā-form is the failure mode per L2 stone brief :18)` |
| `05_brahmana_architect.agent.yaml` (L5 Sākṣī) | `meta-fact 'the ring has never turned once' is itself a Sākṣī artefact` | `2026-08-03 holobiont framing lapse + recovery (L5_SAKSI_2026_08_03.md, root 00_HANDOFF/empirical_kills/); carried: meta-fact 'the ring has never turned once' is itself a Sākṣī artefact` |
| `06_sadhu_compressor.agent.yaml` (L6 Saṃskāra) | `silent-delete slip family (memory §18, the mv && rmdir chain trap)` | `HELIOS Step 6 silent-delete slip chain (memory §18, the mv && rmdir chain trap; L6_SAMSKARA_2026_08_03.md case 1, root 00_HANDOFF/empirical_kills/; positive holds 2026-08-01 L4 closeout + 2026-08-03 7-fence staging)` |
| `07_rsi_constitution.agent.yaml` (L7 Māyā) | `witness-as-tyrant pathology (speculative per syntropic-dyadism.md §6)` | `2026-08-03 holobiont re-tiering as Māyā-prevention (L7_MAYA_2026_08_03.md, root 00_HANDOFF/empirical_kills/; witness-as-tyrant is the failure mode per L7 stone brief)` |

Rationale per kill file: [A]
- **L2** — kill file ratifies the 2026-08-01 proposing-discipline hold as the case; Pūtanā-form is the named failure mode, not the anchor. Kill-file primary; failure mode carried.
- **L5** — per dispatch: kill-file case (holobiont lapse + recovery) made primary; the meta-fact anchor carried as secondary (the kill file itself cites the meta-fact closing as a Sākṣī statement, References :86).
- **L6** — no substantive drift: memory §18 / mv && rmdir chain IS kill-file case 1 (HELIOS Step 6, "strongest empirical anchor"). Edit is naming alignment + kill-file ref + the two positive holds.
- **L7** — kill file ratifies the 2026-08-03 holobiont re-tiering as direct evidence; witness-as-tyrant carried as the failure mode (L7 stone brief). "Speculative per §6" tag superseded by the ratified [B]-tier fence.

### Anchors verified clean (no change) [A]

| File | Anchor | Matches kills README |
|---|---|---|
| `01_candala_firewall.agent.yaml` (L1 Āma) | ROOT_POLLUTION 2026-06-17 | yes |
| `03_vaisya_auditor.agent.yaml` (L3 Pratirūpa) | lazy-tier trap | yes |
| `04_ksatriya_executor.agent.yaml` (L4 Sva-karma) | 2026-07-28 Mavis-as-principal amendment | yes |

## §2 · Act 2 — PMO-0029 (in-lane half): tidy-receipt citation repair

Stale citation: `00_HANDOFF/EMERGENTISM_TIDY_RECEIPT_2026_08_04.md` →
actual path `../00_HANDOFF/tidy/EMERGENTISM_TIDY_RECEIPT_2026_08_04.md`
(Documents-root lane; ls-verified 2026-08-04). [S]

### Citations repaired (3)

| File | Line | Repair |
|---|---|---|
| `README.md` | :59 | path repointed to `00_HANDOFF/tidy/…` |
| `00_HANDOFF/STALE_SKYZAI_REF_REANCHOR_DOCKET_2026_08_04.md` | :6 (frontmatter `source:`) | path repointed to `00_HANDOFF/tidy/…` |
| `12_PUBLIC_SITE/90_ARCHIVE/tool_noise/2026_07_14_compass_restructure_staging/TOMBSTONE.md` | :8 (frontmatter `source:`) | path repointed to `00_HANDOFF/tidy/…` |

Post-repair grep for `00_HANDOFF/EMERGENTISM_TIDY_RECEIPT` in-lane: **0 hits**. [S]

Note on the TOMBSTONE instance: it sits under `90_ARCHIVE/` (historical custody),
but the tombstone was created 2026-08-04 by the same tidy sprint it cites; the
repair is path-only (all other content preserved) so its source pointer resolves.
Flagged here for lane-owner awareness. [S]

### Observations — not repaired (out of dispatch scope)

- Docket :76 `delivery per EMERGENTISM_TIDY_RECEIPT §3` — bare name, no path; left as-is.
- `00_HANDOFF/0_REF_ORPHAN_VERIFICATION_2026_08_04.md` :6, `00_HANDOFF/PENDING_K2_QUEUE_REFRESH_2026_08_04.md` :6/:13/:14, `00_META/claim_cards/one_sitting.yaml` :16 — these cite the **sibling** receipt `01_EMERGENTISM_TIDY_RECEIPT_2026_08_04.md` (01_-prefixed; also in root `00_HANDOFF/tidy/`), mostly by bare filename or already-correct `tidy/` path. Not the dispatch target; no repair.
- Root-side citations (root README, root docket copies) land with the root PMO session per dispatch §Act 2.

## §3 · Mismatches escalated

None unresolved. All four drifted anchors reconciled mechanically against the
kill files; kill files untouched (root lane). [S]

## §4 · Verification record

- Tree clean before work (`git status --porcelain` empty; branch `main`). [S]
- 7/7 YAMLs parse post-edit (`python3 yaml.safe_load`). [A]
- `git diff --check` clean. [A]
- Commits: path-limited, explicit pathspec; Act 1 commit (4 YAMLs) + Act 2 commit (3 citation files + this receipt).

*η = 0. The anchors point at the kills; the receipts point at the tidy.*
