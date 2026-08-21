---
type: runtime-projection-contract
title: "Rosetta managed-agent projection contract"
status: "ACTIVE — source-to-local-runtime contract"
evidence_tier: "[S] source ownership and field mapping; [A] deterministic hash mechanics; [I] cross-domain Rosetta cells."
date: 2026-08-21
---

# Rosetta managed-agent projection contract

This contract maps the seven source-owned `agents/*.agent.yaml` files into the
local `.codex/agents/` runtime projection. It creates no doctrine, identity,
authority, model assignment, or deployment claim.

## Source precedence

1. The canonical Rosetta Stone owns row semantics.
2. The seven manifest-listed YAML files own managed-agent prompts and tool policy.
3. The root runtime files are deterministic derived views.

The three-line fence travels into every generated surface:

1. Geometry is `[A]`, given the selected chart.
2. Seven seats are `[S]`, selected rather than derived; 3, 5, or 9 satisfy the
   same symmetry.
3. Every cross-domain cell is `[I]` and inherits no source-domain warrant.

`GEN7` seats are not `G7` move keys. The G7 cell on each row is an `[I]`
directional projection only.

## Source-to-output mapping

| Output field | YAML source or deterministic derivation |
|---|---|
| name, description | top-level YAML fields |
| level, caste, operator/id, G7 projection, pramāṇa, reasoning, -ology, regime, equation, axis, deployability, involution mirror, virtue/vice, dispatch line, and Stone refs | the identically named `metadata.*` fields |
| role class, route, G7 cell, REP6, VMOSK-A, balance, mathematical note, tiers, exact stop condition, mission-closability gate, and move-or-split misroute action | `metadata.runtime_projection.*` |
| authority booleans and disposer class | `metadata.authority.*` |
| Agentz trunk, Agentz disposition, and A3 close-out pointer | `metadata.agentz_trunk`, `metadata.agentz_disp`, and `metadata.a3_closeout_ref` |
| enabled tools | top-level `tools[].configs[]`, filtered where `enabled=true` |
| permissions | derived from the enabled-tool set |
| source path and source SHA-256 | manifest-listed YAML path and current bytes |
| source bundle SHA-256 | sorted `path + NUL + file_sha256 + LF` records |
| canonical Stone paths, SHA-256 values, and bundle SHA-256 | live `00_THE_MASTER_ROSETTA.md`, `38_THE_FULL_ROSETTA_CORRECTED.md`, and `D_SERIES_ROWS/00_GENERATIVE_TABLE.md` bytes |
| row filename | fixed compatibility mapping from L1–L7 to the seven existing row names |

All other YAML content remains source-only unless this table names it. Omission
does not silently create a derived field, and adding a projected field requires
an explicit contract/compiler/checker change in the same review wave.

Model choice is intentionally absent. It is registry-bound at dispatch time and
must never be pinned in a caste YAML or generated row.

The following legacy runtime fields are dropped because no current source owner
defines them: `input_type`, `output_type`, `evaluation_contract`,
`budget_source`, `budget_required_fields`,
`full_closure_positions`, `role_class` outside the typed projection,
`operator_tier`, `balance_coordinate`, `equation_domain`, and
`d4_d5_contract`. Reintroduction requires an owner field and this contract to be
amended first.

The level-owned stop conditions are a closed seven-row contract:

| Level | Exact stop condition |
|---|---|
| L1 | `ambiguity_exceeds_direct_evidence` |
| L2 | `candidates_ready_for_ranking` |
| L3 | `ranked_options_with_uncertainty_and_risks` |
| L4 | `action_committed_or_refused_or_escalated` |
| L5 | `alternatives_risks_owners_and_kill_criteria_complete` |
| L6 | `paths_successors_risks_and_reversibility_complete` |
| L7 | `invariant_reason_scope_risks_downgrade_and_return_complete` |

## Fail-closed invariants

- The manifest lists exactly seven YAMLs and all hashes match before compilation.
- Both compiler and independent checker parse the two active Stone-owned row
  tables, compare their row semantics to every YAML, and carry those tables plus
  the Master Rosetta's exact live hashes into every row, schema, and deployment
  manifest.
- A Stone-row mismatch or canonical-source byte change fails the adopted runtime
  check until a new side proposal is independently reviewed and adopted.
- YAML duplicate keys fail parsing.
- Each YAML, generated row, and schema entry carries the exact level-owned stop
  condition. A mission must be closable by that condition. If it is not, the
  mission is split or moved to the station whose pramāṇa and stop condition can
  close it; retrying the unchanged mission is forbidden.
- L1 direct perception is bounded to one named source or artifact and may report
  only what is visible within it. Cross-source inference and consistency work
  route to L3. A timeout caused by violating this boundary is a briefing error,
  not evidence of station failure.
- L4 ends a completed owned change in a local commit without asking the owner to
  choose cadence. For a non-trivial or mixed surface, L1 maps direct dirty paths,
  L2 proposes revertible groups, L3 ranks ownership and reversibility risk, and L4
  stages by explicit pathspec after inspecting write activity. `git add -A` is
  forbidden; active or unresolved foreign work is excluded. Commit remains a local
  receipt, never authority, deployment, publication, settlement, or permission to
  push.
- L1–L4 are operational; L5–L7 are non-deployable boundary counsel.
- Only L4 may expose enabled `write`, `edit`, or `bash`, and each such tool must
  carry `permission_policy.type=always_ask`.
- Every row has `stage_only=true` and `may_sign`, `may_authorize`, `may_publish`,
  `may_transmit`, and `may_settle` set to false.
- PRISM verifies only. Public DAV consequence requires at least two natural
  persons under the applicable external authority.
- Compiler output is UTF-8, LF-only, key-ordered, and timestamp-free.

## Generation and adoption

The compiler emits twelve payload files plus a thirteenth
`DEPLOYMENT_MANIFEST.md` that hashes those twelve and excludes itself. The
manifest is an active generated surface, not an optional residual. The compiler
may emit only to an explicit side directory. `--check` is
write-free. Adoption into `.codex/agents/` is a separate, diff-reviewed L4 act;
the compiler refuses that directory as an emission target. Independent semantic
certification uses `check_root_agentz_projection.py`, not the generator's own
success claim. The checker reparses the YAML independently, compares every
contract-mapped field, recomputes the bundle digest, and validates every
deployment-manifest entry.

No compiler run, hash match, local adoption, commit, or receipt proves hosted
provisioning, deployment, signing, authorization, publication, settlement, or a
world outcome.
