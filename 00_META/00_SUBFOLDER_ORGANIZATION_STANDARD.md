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

Every active documentary sub-subfolder with files should have a `README.md` or
`00_INDEX.md` that states:

1. what the folder is,
2. what it owns,
3. what it must not own,
4. where to read first,
5. whether it is active, archived, generated, or compatibility-only.

Short is better than ornate. A folder front door is a routing instrument, not an essay.

Code packages, generated dependency/build trees, and raw data leaves follow
their native package or dataset conventions. Deep cold-archive descendants may
inherit the nearest archive README when they are one custody batch and have no
independent active meaning. This exception must never be used to hide an active
owner or an unmarked compatibility route.

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

## 9A. Canonical Root Shape

The active root has four classes and no fifth:

```text
01_EMERGENTISM/
├── reader doors                 README, Weltanschauung, Kernel Index, Rosetta
├── control surfaces             00_CONTROL, 00_HANDOFF, 00_META
├── semantic and support lanes   01_TELEOLOGY … 12_PUBLIC_SITE
└── custody surfaces             90_ARCHIVE, 91_COMPATIBILITY
```

Root forwarding stubs are permitted only when they resolve an older citation to
an existing active or historical target. A forwarding stub cannot contain new
doctrine. The repository map in `README.md` is the human front door; this
standard is the architectural owner; `09_TOOLS/01_SCRIPTS/check_tree_contract.py`
is the executable guard. Generated registers describe the tree but do not own it.

### 9A.1 · The root live-set is CLOSED at eight `[D]` — staged 2026-07-22

The root holds exactly **eight live documents**. This is not a description; it
is a closed set, and it is already enforced — `check_tree_contract.py`
`ROOT_BODY_ALLOWLIST` contains these eight names and no others:

| file | job |
|---|---|
| `README.md` | what this is, for a human |
| `AGENTS.md` · `AGENT_README.md` · `CLAUDE.md` | routing, for machines |
| `ROSETTA.md` | shim to the Rosetta Stone lane |
| `00_THE_KERNEL_INDEX.md` | the map — seven owner surfaces |
| `00_THE_WELTANSCHAUUNG.md` | the technical door — the priced creed |
| `00_THE_WELTANSCHAUUNG_ONE_SITTING.md` | the reader's door — one sitting |

**A ninth live root file is a contract amendment, not a file drop.** Adding one
means editing this section and the allowlist together, with a receipt. The
guard already refuses the file; this sentence says why.

### 9A.2 · The stub law `[D]`

Everything else at root — **11 files, verified 2026-07-22** — is a forwarding
stub carrying real demand. A stub only works at the path it forwards *from*, so
a stub **with live citers** may not be moved, renamed, or deleted.

> **Correction, same day.** An earlier draft of this section said *30 stubs,
> 2–33 citations each, append-only, none may be moved.* That count was wrong:
> it never asked **who** was citing. Five tidy passes had generated their own
> audit trail, and those audits name every stub they created — so the machinery
> was citing its own output and the count read it as demand. Re-measured
> against live doctrine only: **11 stubs carry all 58 live citations; 19 had
> zero.** The 19 were relocated to `91_COMPATIBILITY/02_ROOT_STUBS_2026_07_22/`
> with a dated stone and a lookup index. Root: 38 → 19 files.

**The demand test is now the rule:** before claiming a stub is load-bearing,
count only citers that are live doctrine — excluding archives, dated handoff
packets, other stubs, and any audit or tidy-plan document. A stub cited only by
the pass that created it is not load-bearing; it is an echo.

Four binding rules. `09_TOOLS/01_SCRIPTS/check_forwarding_stubs.py` **detects**
violations of them; it does not enforce them, and **it is currently red**:

> **Gate status, dated 2026-07-22.** The checker exits `1` — *75 violations
> across 97 stubs* corpus-wide (70 are in-lane stubs declaring no target at
> all). The **root** surface is clean; the lanes are not. An earlier draft of
> this section said the rules were *"enforced by"* the checker, which read as a
> passing gate over a failing one — **the same false-green pattern this
> standard exists to name, committed inside the standard.** Corrected here. The
> rules below are the contract; the checker is the detector; the backlog is
> real and open.



1. A stub declares at least one target, and it resolves.
2. **`canonical_target` means a LIVE owner.** It may never name a path under
   `90_ARCHIVE/`, and never another stub. If nothing live absorbs the document,
   omit the field.
3. `historical_target` means preserved bytes and *may* be archival.
4. **No chains.** A stub points at its terminus, not at another stub.

*Why rules 2 and 4 exist:* on 2026-07-22 fourteen root stubs declared a
`canonical_target` that resolved to a grave or to another tombstone. Every one
existed, so an existence-only check reported zero broken — while readers
following a link labelled "canonical home" landed on a headstone. **Existence
is not status.**

### 9A.3 · The placement rule `[D]` — one line, no judgement call

> **A new document goes to the one owner that would have to be corrected if the
> document turned out to be false.**
>
> If nothing would have to be corrected, it is not doctrine. Route it to
> `00_CONTROL` (receipt for a completed act), `00_HANDOFF` (dated in-flight
> packet), `90_ARCHIVE` (superseded body), or `91_COMPATIBILITY` (path only) —
> **and never to the root.**

### 9A.4 · Lane names are glossed, never renamed `[D]`

There are **seventeen lanes**. The `-ology` names are hard-coded in
`check_tree_contract.py` (three separate lists), the `README.md` repository
map, seventeen route-card triplets, and the Kernel Index. **Renaming buys
cosmetics and costs a mass-breakage event.** The Plain-Language Naming Law is
satisfied by a function gloss, not a directory rename:

| lane | in plain words |
|---|---|
| `00_CONTROL` | receipts and boundaries for completed acts |
| `00_HANDOFF` | dated in-flight working packets |
| `00_META` | the governance spine — routing and claim custody |
| `01_TELEOLOGY` | what is it for |
| `02_EPISTEMOLOGY` | how do we know |
| `03_METHODOLOGY` | how do we work |
| `04_AXIOLOGY` | what is worth |
| `05_COSMOLOGY` | what is the world |
| `06_ONTOLOGY` | what is there |
| `07_THEOLOGY` | what is ultimate |
| `08_FRAMEWORK_SUPPORT` | evidence, compilers, analysis |
| `09_TOOLS` | validators and renderers |
| `10_SEED` | the minimal teachable core |
| `11_UPLINK` | the record — audits and receipts |
| `12_PUBLIC_SITE` | projection; never an owner |
| `90_ARCHIVE` | cold provenance |
| `91_COMPATIBILITY` | paths only, never doctrine |

*Count correction:* an earlier pass in this session twice said "16 lanes."
`ls -1d */` returns **17**. Recorded so the miscount is not inherited.

Within `08_FRAMEWORK_SUPPORT/`, compilers and historical analysis live under
`04_COMPILERS_AND_ANALYSIS/`. No semantic or support lane may create its own
`00_META/`; old references are explained through a `91_COMPATIBILITY/` map.

---

## 10. Per-pillar Surface Ownership (L5 clarification, 2026-07-22)

This section makes the per-pillar rules explicit so future agents don't conflate lane-caste with doc-caste:

1. **Per-pillar `90_ARCHIVE/` is allowed and recommended** for K3 tombstones that are pillar-specific (e.g., `02_EPISTEMOLOGY/90_ARCHIVE/`). The pillar-local archive is preferred over the root `90_ARCHIVE/` for tombstones whose absorber is the pillar itself.
2. **Per-pillar `00_META/` is forbidden.** Governance lives at the root `01_EMERGENTISM/00_META/` only — never inside a pillar. This is the explicit design per Blueprint §1.2 ("00_META/ = governance spine").
3. **Per-pillar `91_COMPATIBILITY/` is allowed** for -ology-specific legacy path resolution (e.g., `01_EMERGENTISM/02_EPISTEMOLOGY/91_COMPATIBILITY/`). The compatibility function is root-allowed, not root-required.
4. **The `AGENTS.md` / `CLAUDE.md` / `README.md` triplet never carries doctrine.** These are routing surfaces. A README is a front door; it is not a source theorem. Structural claims live in a named owner document and retain their own tier.
5. **Per-pillar `Door` (the `00_THE_*.md` file) is the architect's single load-bearing entry.** Each Door must carry an explicit `"active"` or `"candidate"` status so the next reader can route without re-deriving the seating. Any transition is recorded by a dated receipt and the controlling source owner; no private financial-signature convention governs editorial, repository, or AI work.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md`
