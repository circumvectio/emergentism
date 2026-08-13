---
rosetta:
  primary_level: L5
  primary_column: Compiler Front Door
  secondary:
    - level: L3
      column: Reproducibility Audit
      role: "state which compiler outputs are source-backed and which are dormant"
    - level: L4
      column: Compiler Execution
      role: "keep compiler commands explicit and diff-reviewed before generated output is accepted"
    - level: L6
      column: Source Boundary
      role: "make compiler output downstream from source-owned doctrine and route cards"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/I]"
  canonical_phrase: "02_COMPILERS"
title: "02_COMPILERS"
status: "ACTIVE — compiler front door"
evidence_tier: "[B] for local compiler inventory and source-input status; [S] for downstream-output rule; [I] for folder-boundary guidance."
---

# 02_COMPILERS

Focused compiler utilities for building derived maps and compressed working
surfaces from source-owned material.

## What Belongs Here

- narrow compilers that emit indexes, maps, or other derived views
- helper builders that support source-first navigation

## What Does Not

- source doctrine
- hand-authored authority files that should live in the owning row
- deployment scripts

## Authority Rule

Compiler output is downstream. If a compiled artifact disagrees with the owning
source lane, repair the source and recompile.

## Current Compiler Inventory

| Compiler | Output | Status |
|---|---|---|
| `compile_claim_cards.py` | `00_META/registers/CLAIM_CARD_REGISTER.json`, `CLAIM_GRAPH.json`, `CLAIM_LIFECYCLE_INVENTORY.json` | [B/S] Active deterministic claim/owner/dependency compiler. |
| `build_corpus_map.py` | compatibility front door for `compile_claim_cards.py` | [B] Active; the absent-source holographic compiler was replaced in W0. |
| `render_burri_rules.py` | deterministic Burri plate renders from `05_COSMOLOGY/00_THE_BURRI_RULES.md` | [B/S] Active; covered by `test_render_burri_rules.py`. |

## Claim-card commands

```sh
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --write
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check
python3 09_TOOLS/02_COMPILERS/test_corpus_claim_graph.py
```

The `*.yaml` inputs use the JSON subset of YAML 1.2 so compilation remains
stdlib-only and deterministic. Generated graphs are routing views, not owners
or evidence.

Parent-relative source resolution is restricted to the declared `02_SKYZAI`
sibling inside an explicitly configured or linked-worktree federation. The
compiler never scans checkout ancestors, rejects symlink components and path
escapes, and requires exact reviewed SHA-256 bytes whenever that authorized
federation is available. Secret-free CI sets
`EMERGENTISM_ALLOW_UNAVAILABLE_EXTERNAL_SOURCES=1`; that narrowly defers byte
replay for the exact six checked-in path/hash/lifecycle/work contracts while
all local metadata, graph, projection, and generated-output checks still run.
The 28 claim cards backed by four of those sources additionally share an exact
semantic-inventory pin over card ID, source/work binding, line range, section,
anchor, and locator fingerprint; metadata-only mode cannot widen or rewrite a
locator without an explicit reviewed compiler update.
`test_corpus_claim_graph.py` keeps exact byte replay as the only conditional
skip and covers containment, mismatch, unavailable-mode, and repository-wide
contracts.

`test_coherence_profile.py` covers the adjacent script validator's four-axis
contract, including all internal overall states and the rule that an internal
gate is inadmissible as world-contact evidence. Any declared world-contact
record must also resolve to repository-relative custody; a label without a
file cannot move that axis.

`test_claim_status.py` supplies 23 mutation controls for the 48-row claim
lifecycle: exact schema and policy identity, duplicate-key rejection, typed
contact and merged-contact contracts, internal resolutions, grave-parent
dispositions, exact external-owner and restored-result inventories, path
custody, dependency acyclicity, row cardinality, the canonical lifecycle
digest, and the full claim-status contract digest.

`test_contact_limited.py` supplies 70 mutation controls for the exact bounded
completion inventory. It removes artifacts and lifecycle rows, swaps contact
contracts and grave-parent dispositions, preserves counts while substituting
debt IDs, fabricates internal world evidence, changes the nested archive-ignore
rule, and mutates alias/overlap lifecycles; each move must fail rather than
silently rewrite the baseline. Temporary Git histories also prove that a new
receipt may land once, an unchanged receipt survives a later commit, a
same-path rewrite fails, and shallow parent history fails closed.

`test_active_receipt_citations.py` supplies 24 mutation controls for typed and
exact target substitution, same-line binding, packet/receipt lane separation,
new-owner discovery, filename-extension spoofs, duplicate/malformed JSON,
context-hashed diagnostics, immutable digest custody, and the delivered public
dependency closure through CSS, modules, manifests, workers, service workers,
precache lists, and imported worker scripts.

`test_node_product_ranking.py` supplies positive and negative controls for the
KSC-02 regression gate, including adjacent-denial bypasses, exact scope
exclusions, the Managed Agents projection, and the live active-corpus scan.

`test_review_bundle.py` supplies mutation and entrypoint controls for the
external-review status projection: the live registry/document pair, a blocked
packet falsely labeled ready to send, missing no-contact/no-review boundary
phrases, and a discovered paired v5 packet that must fail rather than inherit
the v4 technical contract.

`test_work_in_progress.py` supplies mutation controls for the three
source-bound WIP owner/contact rows: exact held debt, profile, review, docket,
and rendered-Markdown contracts must survive without turning this manifest
into owner selection or contact authority.

`test_adjudication_custody.py` supplies mutation controls for the four
byte-locked 2026-08-01 custody artifacts: strict JSONL structure, cardinality,
ordinal and duplicate joins, supplement corrections/closures/gate/docket, the
derived 151/8/4/6 reviewed partition, and Receipt 234's parents and declared
hashes. Its baseline temporary corpus contains only those four artifacts; it
does not replay external journals, inspect current source evidence, or infer
semantic repairs.

**Corrected 2026-07-22.** This table previously held only the dormant
`build_corpus_map.py` row, so it read as though the lane had no working
compiler — while omitting the deterministic Burri plate renderer that the parent
lane README names as this folder's headline active surface. Counted by listing
`*.py` here: 7 files, of which 5 are `test_*.py`, leaving 2 compilers; both are
now in the table. The dormancy claim for `build_corpus_map.py` was rechecked and
holds (line 19 sets `SOURCE` to `_corpus_source.yaml` under `09_TOOLS/`, which is
absent). Runnability receipt for the renderer, 2026-07-22:
`python3 09_TOOLS/02_COMPILERS/render_burri_rules.py --check` exited 0 with
`BURRI-OK topology valid; generated SVG bytes are current`.

## Route Upstream

- main tool inventory: `../README.md` and `../CLAUDE.md`
- current corpus gate: `../01_SCRIPTS/gate.sh`
- Uplink route map: `../../11_UPLINK/README.md`

## Kintsugi audit foundation

The A0 baseline validator freezes the known repository test state without treating existing failures as new truth:

```bash
set -euo pipefail
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check-baseline \
  --canonical-root /Users/Yves/Documents/01_EMERGENTISM
```

`kintsugi_baseline_failures.json` records 19 baseline node IDs and five exact failure signatures at `main@26e616e651e2a87e8c85bf37db515d7fcd007b7b`. A previously failing node may turn green; a removed node, new failure, exception drift, or signature drift fails. The validator itself introduces no direct writes and disables pytest cache and Python bytecode writes; arbitrary repository test bodies are not sandboxed. The baseline gate has no external approval gate.

## Kintsugi A0B machine kernel

> **Boundary:** A0B validates grammar and transaction machinery; it does not validate Emergentism, repair canon, or create a live Kintsugi vessel.

**Purity classification:** A0B sources and fixtures are non-semantic tooling records.
Their historical governance vocabulary is test or provenance data,
not a premise, owner, or authority claim for Emergentism. The purity checker
exempts only its enumerated artifacts; new siblings remain scanned by default.

The dated [A0B machine handoff](kintsugi_kernel/docs/specs/2026-07-12-kintsugi-a0b-machine-kernel-handoff.md)
records the reproducible local evidence and the limits on the first live A1
vessel.

| Package boundary | Responsibility |
|---|---|
| `diagnostics.py` / `codec.py` | Typed issues, canonical JSON, hashes, and safe repository paths |
| `baseline.py` / `schema.py` | Frozen A0 baseline and restricted schema evaluation |
| `records.py` / `semantics.py` | Typed record graph, evidence/Justice rules, antibodies, and the downstream Compass mutation projection |
| `markdown.py` | Machine-fence synchronization and framed narrative hashes |
| `gitstate.py` / `manifest.py` | Git scope, protected-tree, manifest, attempt, and compare-and-swap laws |
| `review.py` | Review target, attestations, history, transitions, and validation bundle |
| `orchestration.py` | Read-only dependency-ordered validation |
| `rendering.py` | One operation-aware atomic transaction writer |
| `validate_kintsugi.py` / `render_kintsugi.py` | Stable validator and renderer command-line facades |

The schema exposes exactly three selectable root roles: `coreData`,
`publicQueue`, and `baselineAllowlist`.

### Read-only checks

Frozen baseline:

```bash
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check-baseline \
  --canonical-root /Users/Yves/Documents/01_EMERGENTISM
```

Default live check:

```bash
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check
```

The default check currently exits `2` with controlled `KIN-E-IO` because
`02_KINTSUGI_SEAMS.json` does not yet exist. That is an honest missing-input
state, not a validation failure.

Explicit phase-check template:

```bash
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check --phase A --bootstrap --base-ref <tracked-base> \
  --canonical-root <canonical-root>
```

Stable output is `KIN-OK validation` for a successful full check and
`KIN-OK baseline collected=19 failures=5` for the frozen baseline. Failures use
`KIN-ERROR <path> <code>: <message>`.

Validator exits are `0` pass, `1` semantic validation failure, and `2` CLI or
I/O failure. Renderer exits are `0` pass, `1` transaction rejection, and `2`
parser or request error.

### Renderer contract, not a live invocation

| Operation | Role |
|---|---|
| `freeze-manifest` | Finalize the manifest, allocate the smallest unused attempt ID, and freeze the subject |
| `review-target` | Materialize the already-bound review target |
| `transition-core` | Apply one legal review-state transition with external review intake |
| `bundle` | Preflight the immutable bundle against a `COMPLETE` receipt without writing it; `transition-core --stage VERIFIED` materializes it |

The six lifecycle stages are: (1) final freeze/allocation, (2) `TARGET_READY`,
(3) `ATTESTED`, (4) `FAILED` or `ABANDONED`, (5) `COMPLETE`, and (6)
`VERIFIED`. A retry uses the canonical smallest-unused attempt ID and preserves
append-only `reviewAttempts`, `reviewAttemptArtifacts`, `reviewAttestations`,
`reviewFindings`, and `reviewFindingDispositions`. `PASSED` is terminal;
`FAILED` or `ABANDONED` requires an exact predecessor disposition before retry.

External candidates enter through `--logic-review-input`,
`--btj-review-input`, and `--finding-dispositions-input`. They remain outside
both repositories until atomic intake. Every transaction holds the shared Git
common-directory lock, checks expected HEAD and core hash before and inside the
lock, freezes the read set, and rolls back on a partial replacement. Final
`freeze-manifest` additionally persists its attempt reservation, so a failed
post-reservation freeze leaves that attempt ID burned.

Typed-control prose is filtered outside machine fences. Ledger and receipt
narratives use framed hashes so fence-side movement changes the digest.
`safeRegexSearch` is bounded to a 256-code-point pattern and a 1,024-state
Thompson NFA; it does not invoke Python's backtracking regular-expression
engine.
