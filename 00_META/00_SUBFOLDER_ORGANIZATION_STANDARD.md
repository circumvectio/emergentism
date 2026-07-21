---
rosetta:
  primary_column: "Meta"
  register: "[S]"
  canonical_phrase: "Subfolder Organization Standard"
---

# Subfolder Organization Standard

**Status:** active routing standard for `01_EMERGENTISM/`.
**Purpose:** make sub-subfolders effective, efficient, coherent, consistent, and logically sound without moving source-owner files blindly.

This standard governs how the doctrine root is organized around its active source owners.

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
- public packaging belongs under the current Emergentism owner lane, not source doctrine;
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

The Git repository root is the physical Emergentism root. Paths inside active
documents are repository-relative; no parent repository or application tree is
part of the worldview's address space.

Older documents may mention retired foundation, evidence, translation,
dissemination, organization, or portfolio aliases. Treat those strings as
historical unless a current front door explicitly preserves a compatibility
path; never recreate a retired root merely to make a stale link resolve.

`90_ARCHIVE/` is historical custody, not an alternate source owner. Repoint an
active claim to its current owner when one exists; otherwise cite the archive
explicitly as provenance or remove the dependency.

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

## Agent Execution Surface

**Research continuation note (non-authoritative):**

The legacy checklist below is retained as research context. It grants no execution
authority; repository routing lives only in the applicable AGENTS.md and CLAUDE.md files.

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md`
