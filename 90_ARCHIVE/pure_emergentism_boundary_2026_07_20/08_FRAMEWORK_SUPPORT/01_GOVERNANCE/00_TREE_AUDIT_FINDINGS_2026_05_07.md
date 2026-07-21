---

title: "Tree Audit Findings — corrections after the Agentz five-caste pass"
type: audit-record
status: active
date: 2026-05-07
owner: L3 Vaiśya (verification) + L6 Sādhu (compression review)
evidence_tier: "[B] Empirical — git ls-files counts are authoritative"
companion_to: 00_TREE_CONSTITUTION.md
rosetta:
  primary_level: L3
  primary_column: Philosophy
  secondary:
    - level: L4
      column: Philosophy
      role: "route corrections into governance enforcement"
    - level: L6
      column: Philosophy
      role: "compress audit findings without inflating authority"
    - level: L5
      column: Philosophy
      role: "stabilize tree topology as corpus architecture"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[B/I]"
  canonical_phrase: "Tree Audit Findings — Corrections Record"
---


# Tree Audit Findings (Corrections)

[I] When the L1/L2/L3/L5/L6 caste agents audited the folder tree on 2026-05-07,
two of L6 Sādhu's compression-queue items rested on disk-file counts that
included gitignored content. This file records the corrections so future
audits don't repeat the misread.

The Tree Constitution (`00_TREE_CONSTITUTION.md`) and audit ladder remain
correct; only specific finding numbers were wrong.

---

## Correction 1 — TOKENIZATION_CENTRES/00_GENERAL is not overgrown

**L6 finding (uncorrected):** "34,420 files; mix of docs + WEBSITE (PWA) + intake. Escalate to L5 for redesign."

**Truth ([B] verified by `git ls-files`):**
- Total tracked files: **1,791**
- Largest subfolder: `21_WEBSITE/` with 392 tracked files (a Next.js PWA project)
- Disk count showed 32,985 because `21_WEBSITE/15_TOKENCEN_KSA_PWA/node_modules/` contains 32,377 untracked files

**Verdict:** The tracked structure is a coherent 24-subfolder operating canon
(00_INVESTOR_PACKET, 01_ENTITY_CANON, 02_TOKEN_MODEL, 03_OFFER_STACK,
04_COUNTERPARTY_MAP, 05_ASSET_PROGRAMS, …, 21_WEBSITE, 22_STAKEHOLDERS).
PWA code at `21_WEBSITE/` legitimately lives inside the portfolio sidecar
because Tokencen IS a portfolio sidecar (per Routing Law). No split required.

The disk imbalance is real but is a `node_modules/` issue, not a tracked-tree
issue. Fix already in place: `.gitignore` covers it.

---

## Correction 2 — QNTM (the institutional MPC/ZK-Identity rail)/intelligence is not overgrown

**L6 finding (uncorrected):** "24,444 files. Same pattern — WEBSITE app inside intelligence/. Flag."

**Truth ([B] verified by `git ls-files`):**
- Total tracked files in `03_VENTURES/_PORTFOLIO/QNTM (the institutional MPC/ZK-Identity rail)/intelligence/`: **137**
- The 24k disk count came from gitignored Next.js / build artifacts inside
  the intelligence subtree

**Verdict:** No overgrowth. No split required.

---

## Correction 3 — sevenfold mirror is phenotype scaffold, not duplicate doctrine

**L6 finding (uncorrected):** "23 files; compact to README pointers only."

**Truth ([S] verified by READMEs):** The mirror at `02_SKYZAI/01_NOOSPHERE/02_ORGANS/_DOCTRINE/01_TELEOLOGY..07_THEOLOGY/`
is the organism's L1–L7 phenotype scaffold (powerplants, datacentres, soresfi,
tokens, coupling_patterns, state_sensors). The 01_TELEOLOGY README states it:
"At Foundation scale, Objective Function names the gradient. At organism scale,
Objective Function must become metabolism." Not redundant content; intentionally
sparse scaffolding.

**Verdict:** Compaction would erase legitimate scaffolding. Resolution
already applied in commit `63606d599`: SSoT discipline footer added to
each mirror README.

---

## Correction 4 — 91_COMPATIBILITY layers are doing their job

**L6 finding (uncorrected):** "Self-described non-authoritative; only 2 active refs; archive once refs are repointed."

**Truth ([B] verified by `git grep`):** 7 internal path references
(governance reports, master indexes, BREAKTHROUGH packets, a SKYZAI_COM
wallet spec) deliberately cite the 91_COMPATIBILITY paths as "historical
route clue" — they are using the compatibility layer for its intended
purpose. The "2 active refs" count was based on filename match, not
deep-path match.

**Verdict:** Don't archive. Resolution already applied in commit `1accd5550`:
TOMBSTONE.md added to both 91_COMPATIBILITY layers documenting their role
and the conditions under which archival becomes correct.

---

## Pattern: distinguish tracked vs disk

**The lesson:** [B/I] when counting "how big is this folder," use `git ls-files`,
not `find . -type f`. Build artifacts, virtualenvs, and node_modules dominate
disk-file counts but contribute zero to repository semantics. The L6
compression queue's disk-based scan was correct in spirit (something is
wrong with how big this looks) but pointed at the wrong remedy (split the
folder vs. confirm gitignore).

**Convention added:** any future tree audit lists tracked-only counts unless
explicitly measuring storage pressure.

---

## What This Doesn't Change

The four laws (Boundary, Ownership, Routing, Failure-Mode), the 7-root
manifest, the seven mechanical tests, and the audit ladder (L1 detect →
L2 explore → L3 rank → L4 act → L5 redesign → L6 compress → L7 transcend)
are all unaffected. L3 Vaiśya's headline finding — **C0 strictly dominates;
no redesign warranted** — held under both the original and corrected counts.

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_TREE_AUDIT_FINDINGS_2026_05_07.md
