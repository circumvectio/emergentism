---
rosetta:
  primary_level: L5
  primary_column: "Meta"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "Subfolder Organization Standard"
---

# Subfolder Organization Standard

**Status:** active routing standard for `01_EMERGENTISM/`.
**Purpose:** make sub-subfolders effective, efficient, coherent, consistent, and logically sound without moving source-owner files blindly.

This standard governs how the doctrine root should be organized after the sevenfold Foundation reorg.

## 1. Core Rule

Every folder answers one question:

> What does this folder own that its parent does not?

If the answer is unclear, do not move files first. Add a local `README.md`, name the owner, and only then consider physical moves.

## 2. Folder Types

Use these types consistently.

| Type | Naming pattern | Owns | Must contain |
|---|---|---|---|
| Root | `01_TELEOLOGY/`, `11_UPLINK/` | major Rosetta or support lane | `README.md` |
| Source-owner subfolder | `01_FORMAL_SYSTEM/`, `03_THE_PAPERS/` | active canonical body for a topic | `README.md` or `00_INDEX.md` |
| Support subfolder | `05_BUILD_SCRIPTS/`, `data_pipelines/` | tools or supporting artifacts | `README.md` |
| Archive subfolder | `90_ARCHIVE/`, `06_ARCHIVE/` | non-live memory | `README.md` stating non-authority |
| Compatibility subfolder | `91_COMPATIBILITY/` | old links only | `README.md` or moved stub |
| Generated/output subfolder | `COMPLETE_VERSIONS/`, `DELIVERABLES/` | compiled or exported surface | `README.md` naming source owner |

## 3. Local README Contract

Every sub-subfolder with files should have a `README.md` or `00_INDEX.md` that states:

1. what the folder is,
2. what it owns,
3. what it must not own,
4. where to read first,
5. whether it is active, archived, generated, or compatibility-only.

Short is better than ornate. A folder front door is a routing instrument, not an essay.

## 4. Source Ownership

Do not move a file because it "feels nearby." Move it only when its authority owner changes.

Examples:

- formula, Dimensional Framework, Rosetta, and formal system claims belong under Foundation/System Architecture or the relevant support lane;
- public packaging belongs under the current owner lane or AIA book-production/archive surface, not source doctrine;
- synthesis manuscripts may speak beautifully, but claim status routes back to Foundation source;
- Uplink packets route and compress; they do not become source owners;
- compatibility stubs preserve links and should not receive new doctrine.

Translation-control files may live in `00_META/` even when they discuss doctrine,
provided their job is routing, distinction, or repair protocol rather than source
claim ownership. This is why Dimensional Framework/Leadership Pipeline bridge material may remain here
when it is being used to prevent category errors across roots.

## 5. Preferred Subfolder Shape

Use this pattern unless a folder already has a stronger local convention:

```text
FOLDER/
├── README.md
├── 00_INDEX.md              optional when many files need ordered navigation
├── 00_*.md                  local overview / canon / status surfaces
├── 01_*/                    first active sublane
├── 02_*/                    second active sublane
├── 90_ARCHIVE/              local archive only when needed
└── COMPLETE_VERSIONS/       generated/public mirrors only when needed
```

Avoid mixing source manuscripts, compiled outputs, scripts, and archived drafts in the same unmarked folder.

## 6. Path Discipline

The physical root is `01_EMERGENTISM/`.

Older docs may mention retired aliases for former foundations, evidence,
translation, dissemination, organization, entity, portfolio, and archive lanes.
Treat them as historical unless a current front door explicitly preserves a compatibility
path; do not recreate numeric-prefix root aliases.

The archive name in that retired-alias list means the former top-level alias.
Do not recreate retired aliases to repair old links; repoint active references to
`90_ARCHIVE/` or to the current source-owner lane.

When repairing links:

- do not recreate old top-level roots;
- do not rewrite historical compatibility stubs unless their purpose becomes misleading;
- update current front doors before chasing every legacy reference.

## 7. Archive Discipline

Archive folders are cold memory. They may explain, compare, or preserve. They do not govern active doctrine.

An archive README should say:

- why the material is archived,
- what active surface supersedes it,
- how to resurrect something if needed.

## 8. Organization Pass Order

For each folder, apply this order:

1. identify owner and status,
2. add or repair local README/index,
3. fix obvious stale path references in active front doors,
4. move only clear source-owner files,
5. leave compatibility stubs,
6. validate links/manifests,
7. record unresolved gated moves.

This keeps the corpus walkable while protecting source truth.

## 9. Translation-Machine Repair

When a pass is explicitly about tightening the translation machine, apply the
additional protocol in `00_TRANSLATION_MACHINE_PROTOCOL.md`.

The short version:

- preserve the reciprocal kernel before improving prose,
- classify cross-domain claims before amplifying them,
- distinguish `B` from `P_node`,
- repair path drift in active front doors first,
- keep anti-capture as structure, not ornament.

`Zero-Sum Resolution Equation`

---

## 10. Per-pillar Surface Ownership (L5 clarification, 2026-07-22)

This section makes the per-pillar rules explicit so future agents don't conflate lane-caste with doc-caste:

1. **Per-pillar `90_ARCHIVE/` is allowed and recommended** for K3 tombstones that are pillar-specific (e.g., `02_EPISTEMOLOGY/90_ARCHIVE/`). The pillar-local archive is preferred over the root `90_ARCHIVE/` for tombstones whose absorber is the pillar itself.
2. **Per-pillar `00_META/` is forbidden.** Governance lives at the root `01_EMERGENTISM/00_META/` only — never inside a pillar. This is the explicit design per Blueprint §1.2 ("00_META/ = governance spine").
3. **Per-pillar `91_COMPATIBILITY/` is allowed** for -ology-specific legacy path resolution (e.g., `01_EMERGENTISM/02_EPISTEMOLOGY/91_COMPATIBILITY/`). The compatibility function is root-allowed, not root-required.
4. **The `AGENTS.md` / `CLAUDE.md` / `README.md` triplet never carries doctrine.** These are L1 routing surfaces. A README is a front door; it is not a [S] source. A [S] source lives in a `00_THE_*.md` named Door or in a source-owner subfolder, never in the lane's routing triplet.
5. **Per-pillar `Door` (the `00_THE_*.md` file) is the L5 architect's single load-bearing entry.** Each pillar's Door must carry an explicit `"active"` or `"candidate"` status in its frontmatter so the next agent can route to it without re-deriving the seating. Per receipt 145, the Doors are *candidate* until the founder signs; the signing act flips them to *active* with a `receipt:` parent.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md`
