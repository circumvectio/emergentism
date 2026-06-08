---
rosetta:
  primary_level: L5
  primary_column: System Architecture
  secondary:
    - level: L1
      column: Objective Function
      role: "detect contradiction, ghost routes, and stale authority"
    - level: L4
      column: Value Alignment
      role: "execute the smallest defensible write after audit"
    - level: L6
      column: Core State
      role: "prune overgrowth and route dead material to archive"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/I]"
  canonical_phrase: "Rosetta corpus sweep protocol"
title: "Rosetta Corpus Sweep Protocol"
status: "ACTIVE — agent-lane operating protocol, 2026-05-30"
evidence_tier: "[S] where applying existing Rosetta agent grammar; [I] where defining workflow for this repository; [B] only for dated command output, commits, or receipts."
---

# Rosetta Corpus Sweep Protocol

## Folder, Subfolder, Paper: One Pass At A Time

**Purpose:** Give agents a repeatable procedure for applying the Rosetta
castes across the corpus without turning a sweep into a bulk rewrite.

**Scope:** Any folder, subfolder, or paper inside Magnum Opus when the task is
to improve source truth, routing, evidence tiers, or agent usability.

**Non-scope:** This protocol does not authorize silent deletion, public claims,
deployment claims, history rewrites, or edits outside the selected lane.

**Primary rule:** A sweep unit is small enough that an agent can verify it
fresh, explain the delta, and commit only the touched paths.

---

## 0. Select The Sweep Unit

A sweep unit is one of:

| Unit | Use when | Expected output |
|---|---|---|
| Folder | route card, README, manifest, or VMOSK-A is missing or stale | lane-level stabilization |
| Subfolder | local authority exists but a child surface drifts | child-lane repair |
| Paper | one document carries a claim, mapping, or contradiction | document-level repair |

Prefer the smallest unit that changes the final state.

Before editing, record:

```text
target_path:
owner_route:
local_authority_files:
dirty_paths_to_avoid:
validation_commands:
```

If the checkout is shared or dirty, path-scope every command and stage only the
selected unit.

---

## 1. Apply The Seven Castes

Each pass runs the same L1-L7 sequence. The sequence is functional, not a
human-worth hierarchy.

| Level | Agent move | Corpus question | Output |
|---|---|---|---|
| L1 Caṇḍāla | perceive | What is broken, stale, duplicated, unsafe, or falsely routed? | contradiction list |
| L2 Śūdra | explore | What candidate repairs could make the unit more truthful? | option set |
| L3 Vaiśya | audit | Which option follows the local authority and evidence tier? | ranked repair |
| L4 Kṣatriya | execute | What is the smallest defensible edit? | patch / commit |
| L5 Brāhmaṇa | stabilize | What structure, index, or route keeps the edit usable? | README / manifest / map update |
| L6 Sādhu | destroy | What should be pruned, archived, demoted, or explicitly bounded? | deletion, archive route, or kill criterion |
| L7 Ṛṣi | witness | What does this reveal about the whole corpus without taking over execution? | compression note |

L4 is the normal write point. L5/L7 propose and frame. L6 may prune under the
archive-first / K3 discipline, then returns a lean surface to L4.

---

## 2. Create, Stabilize, Destroy

Every sweep should name all three motions, even when one is a no-op.

### Create

Create only what is missing and load-bearing:

- a route card, README row, VMOSK-A shim, evidence tier note, or canonical
  cross-link;
- a narrow reconciliation note when a repeated contradiction needs one place
  to land;
- a small glossary or protocol entry when agents need the term to act safely.

Creation is valid only if it reduces future ambiguity.

### Stabilize

Stabilization makes the unit easier to re-enter:

- update the local README or manifest entry;
- attach evidence tiers and dependency links;
- name the owning source folder;
- separate source truth from summary, archive, mirror, public copy, or draft.

Stabilization is the default motion for active source surfaces.

### Destroy

Destroy means remove false authority, not erase history:

- demote overclaimed language;
- mark drafts as drafts;
- route dead material to archive space;
- remove duplicate indexes when a better canonical route exists;
- add kill criteria for dangerous interpretations.

Deletion without provenance is outside this protocol. Use K3 archive discipline
where historical value remains.

---

## 3. Evidence And Authority Gates

Before a sweep can land, the edited unit should answer:

```text
What tier is each material claim?
What file is source authority?
What file is only summary or translation?
What has no authority to execute?
What would falsify or retire this note?
```

Use the current evidence ladder:

```text
[A] arithmetic / formal proof under stated assumptions
[B] external receipt, command output, or dated verification artifact
[S] structural rule inside accepted canon
[I] interpretive synthesis or proposed mapping
[D] design / deployment draft
[C] conjecture or forward-looking claim
```

Claims about live runtime, law, finance, public deployment, or external uptake
need dated receipts or explicit downgrade labels.

---

## 4. Commit Discipline

For each sweep unit:

1. Check the branch and dirty worktree before editing.
2. Read the local `AGENTS.md`, `CLAUDE.md`, README, and VMOSK-A where present.
3. Patch only the selected unit and required indexes.
4. Run path-scoped whitespace and A7 checks.
5. Run the repo manifest check when topology, links, or routing changed.
6. Stage only the selected paths.
7. Commit with a message that names the lane and motion.
8. Verify the committed range, not only the working tree.

Recommended command shape:

```bash
git diff --check -- <paths>
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/a7_receipt_validator.py --strict --check-refs --paths <paths>
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/manifest_check.py
git diff --cached --check
git diff --check HEAD^ HEAD
```

If another agent commits the same work first, verify the content in `HEAD`,
release the claim, and continue. Convergence is not a conflict.

---

## 5. Sweep Ledger Row

Use this row when reporting or creating a local tracking note:

| Field | Value |
|---|---|
| Target | `<path>` |
| Unit type | folder / subfolder / paper |
| Create | `<created artifact or no-op>` |
| Stabilize | `<index, route, tier, or dependency update>` |
| Destroy | `<pruned, demoted, archived, bounded, or no-op>` |
| Validators | `<commands and result>` |
| Commit | `<hash or pending>` |
| Residual risk | `<known dirty paths, follow-up, or none>` |

This row is evidence only when backed by command output, file diff, or commit
hash.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. Treat this as a procedure for one sweep unit, not permission for bulk
   corpus rewrites.
2. Preserve local owner-lane authority. Repair source owners before patching
   summaries.
3. Translate caste language as functional agent posture. It has no authority to
   rank humans.
4. Keep create/stabilize/destroy explicit in your report.
5. Verify the committed range before claiming a sweep unit landed.

**Canonical Path:** `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/00_CORPUS_SWEEP_PROTOCOL.md`
