---
rosetta:
  primary_column: "Neuroscience"
  register: "[S/I]"
  canonical_phrase: "Root Structure Optimal Outline -- Agentz pass"
---

# Root Structure Optimal Outline -- Agentz Pass

**Date:** 2026-05-07
**Status:** migration-prep packet; no folder moves authorized by this file
**Scope:** repository root and depth-1/depth-2/depth-3 folder logic
**Source frame:** root `AGENTS.md`, root `README.md`, `manifest.yaml`, Uplink `00_CORE/00_INDEX.md`, Uplink `06_AGENTS.md`, and the current disk tree

## Verdict

The current top-level architecture should stay as seven visible canonical roots:

```text
01_EMERGENTISM/   source core state, Rosetta, Uplink, tools, seed
02_SKYZAI/01_NOOSPHERE/        living organism runtime
02_SKYZAI/04_PUBLIC_SCAFFOLD/        public DAC-machine / product-composition surface
03_VENTURES/          organism-native legal and entity membranes
03_VENTURES/_PORTFOLIO/    independent portfolio lanes
02_SKYZAI/06_SPECTRE/           distributed physical mesh substrate
90_ARCHIVE_AND_COMPATIBILITY/         cold history, tombstones, exports, processed intake
```

The problem is not that the root needs more peer folders. The problem is that
some support folders and depth-1 lanes need sharper labels, and a few route
surfaces still tell older stories. The right next move is route standardization,
not a broad move.

## Agentz Reading

| Level | Function | Structural reading |
|---|---|---|
| L1 inventory | perceive what is on disk | Root contains seven canonical roots, hidden tool config, `backbone/` symlink, `docs/` adjunct, `extract/` scratch, and generated output folders. |
| L2 exploration | enumerate possible shapes | More peer roots would increase confusion. Collapsing portfolio/entity/SPECTRE lanes into Skyzai would violate boundaries; Agentz is the exception now rehomed as Skyzai agent organ. |
| L3 audit | rank by canon and risk | The six-plus-archive root frame is still the strongest shape. The stale areas are support-surface wording, Agentz/Agentz Cloud phrasing, and unlisted depth-1 lanes. |
| L4 decision | act only where reversible | Update route docs and prepare a migration checklist. Do not move or delete root folders in this pass. |
| L5 architecture | define the invariant | Every active root needs the same navigation contract: `README.md`, `AGENTS.md`, owner index, archive lane, and clear authority boundary. |
| L6 prune | remove false options | No new `7_*` root, no top-level Agentz root, no `DATA_ROOM/` root, no hidden legal merger by folder name. |
| L7 guard | preserve constitution | K2 is required before deletes, legal/entity membrane changes, child-DAC reclassification, or mass path rewrites. |

## Root Contract

The root should expose only:

```text
Magnum Opus/
├── AGENTS.md
├── README.md
├── manifest.yaml
├── Makefile
├── LICENSE
├── 00_*.md                      short orientation, handover, and tidy receipts
├── 01_EMERGENTISM/
├── 02_SKYZAI/01_NOOSPHERE/
├── 02_SKYZAI/04_PUBLIC_SCAFFOLD/
├── 03_VENTURES/
├── 03_VENTURES/_PORTFOLIO/
├── 02_SKYZAI/06_SPECTRE/
├── 90_ARCHIVE/
├── backbone -> 04_NETWORK_ENTITIES/SKYZAI/01_NOOSPHERE/00_BACKBONE/
├── docs/                        working design/spec adjunct
├── extract/                     scratch extraction surface
├── cache/ out/ output/ tmp/      generated or local runtime output
└── .*/                          local or automation metadata
```

Root support folders are not architecture roots. If a support artifact becomes
important, it must be promoted into the owner root that can maintain it.

## Depth-1 Navigation Contract

Every active root should converge to this local contract:

| Surface | Role |
|---|---|
| `README.md` | human-readable orientation and lane purpose |
| `AGENTS.md` | local agent law, authority chain, and read-first order |
| `00_*` index/canon file | route map or current truth surface |
| numbered content lanes | stable semantic ownership, not transient sprint names |
| `90_ARCHIVE/` or `99_ARCHIVE/` | local history that still belongs near its owner |

The repo already uses `AGENTS.md` heavily. If a separate `AGENT_README.md` is
later wanted for AI-only navigation, it should be generated from `AGENTS.md` and
`README.md`, not allowed to become a third authority surface.

## Depth-2 / Depth-3 Refinement Rule

Depth is allowed only when it improves ownership, routing, or auditability.
Every depth-2 lane should answer four questions without requiring a full-corpus
read:

| Question | Folder surface |
|---|---|
| What is this lane? | `README.md` or `00_INDEX.md` |
| Who may act here? | `AGENTS.md`, inherited if local file is absent |
| What is source vs runtime? | `01_CANON/`, `01_SOURCE/`, `02_RUNTIME/`, or named equivalents |
| Where do old or generated artifacts go? | `90_ARCHIVE/`, `99_ARCHIVE/`, or root-level generated-output policy |

Prefer this depth-3 vocabulary where the owner lane does not already have a
strong local convention:

```text
00_INDEX/ or 00_META/       route map, active claims, current truth
01_CANON/ or 01_SOURCE/     source documents and constitutional specs
02_RUNTIME/ or 02_APP/      implementation, deployed code, derived runtime
03_DATA/ or 03_EVIDENCE/    structured inputs, receipts, evidence tiers
04_OPERATIONS/              runbooks, checklists, management surfaces
05_AUDITS/                  audit reports and verification receipts
90_ARCHIVE/ or 99_ARCHIVE/  owner-local history, never active canon
```

Agentz adds one special depth rule: every public polygenetic tree branch must
resolve to a deployed L-level agent row, not only to a story page. The binding
is:

```text
agentz.cloud branch
  -> 04_NETWORK_ENTITIES/SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/08_AGENTZ_CLOUD_PWA/
  -> 04_NETWORK_ENTITIES/SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/03_RUNTIME_DISPATCH/
  -> .codex/agents/rows/0X_LX_<agent>.toml
  -> .codex/agents/<agent runtime TOML>
  -> receipt in Agentz audit/runtime surface
```

## Root-Specific Target Shape

### 01_EMERGENTISM

Keep the existing shape. It is already the clearest Rosetta-aligned source root:

```text
00_META/
01_TELEOLOGY/
  ├── 01_F5_FORCE/
  ├── 02_THE_DERIVATION/
  └── 90_ARCHIVE/
02_EPISTEMOLOGY/
  └── 01_EVIDENCE_TIERS/
03_METHODOLOGY/
  ├── 01_THE_DERIVATION/
  ├── 02_THE_PAPERS/
  └── 90_ARCHIVE/
04_AXIOLOGY/
  ├── 01_THEURGY/
  └── 02_VALUE_THEORY/
05_COSMOLOGY/
  ├── 01_THE_TRANSCENDENTAL_TRINITY/
  ├── 02_EMERGENTISM_CORE/
  └── 03_FORMAL_SYSTEM/
06_ONTOLOGY/
07_THEOLOGY/
08_FRAMEWORK_SUPPORT/
  ├── 00_META/
  ├── 01_GOVERNANCE/
  ├── 02_OPERATORS/
  ├── 03_EVIDENCE/
  │   └── ROSETTA_STONE/
  ├── 04_APPLICATIONS/
  ├── 05_SYNTHESIS/
  ├── 06_TRANSLATION/
  ├── 07_DISSEMINATION/
  ├── 08_AGENTS/
  │   ├── 00_C_SUITE/
  │   ├── 01_CANDALA_FIREWALL/
  │   ├── 02_SUDRA_EXPLORER/
  │   ├── 03_VAISYA_AUDITOR/
  │   ├── 04_KSATRIYA_EXECUTOR/
  │   ├── 05_BRAHMANA_ARCHITECT/
  │   ├── 06_SADHU_COMPRESSOR/
  │   └── 07_RSI_CONSTITUTION/
  └── 90_ARCHIVE/
11_UPLINK/
  ├── 00_CORE/
  ├── 10_RECONCILIATION/
  ├── 20_SCOPE/
  ├── 25_EXPERIMENTS/
  ├── 30_PROGRAMS/
  ├── 50_AUDITS_AND_EXECUTIONS/
  ├── 60_SESSION_PACKETS/
  ├── 70_EXTRACT_NOW_PACKETS/
  ├── 90_ARCHIVE/
  └── 95_COMPRESSED/
09_TOOLS/
  ├── 01_SCRIPTS/
  ├── 02_COMPILERS/
  ├── 03_SIMULATIONS/
  ├── 04_DATA_PIPELINES/
  ├── 05_DEPLOY/
  ├── 06_PACKAGES/
  ├── 07_AGENT_OPS/
  ├── 08_AUDIT_ARTIFACTS/
  ├── 09_DAC_FRAME/
  ├── 10_SPRINT_GATES/
  └── 90_ARCHIVE/
10_SEED/
91_COMPATIBILITY/
  └── 01_FOUNDATIONS/
```

The dual `08_` folders are intentional: one is source support, one is compressed
agent food. Do not renumber them just for visual neatness.

### 02_SKYZAI/01_NOOSPHERE

Keep Skyzai as the organism body. The target outline is:

```text
00_BACKBONE/
  ├── adapters/
  ├── api/
  ├── local_runtime/
  ├── schemas/
  ├── services/
  └── tests/
01_INTAKE/
  ├── QUEUE/
  ├── CASTES/
  ├── PROCESSED/
  └── 99_QUARANTINE/
02_ORGANS/
  ├── 01_TELEOLOGY/
  ├── 02_EPISTEMOLOGY/
  ├── 03_METHODOLOGY/
  ├── 04_AXIOLOGY/
  ├── 05_COSMOLOGY/
  ├── 06_ONTOLOGY/
  ├── 07_THEOLOGY/
  ├── Agentz/
  ├── ApuBot/
  ├── EvolutionaryNetwork/
  ├── RealityFutures/
  ├── Skyzai/
  └── TheCircle/
03_PRODUCTS/
04_CHILD_DAVS/
  ├── yieldfront/
  └── AGENTZ_CLOUD/      technical/PWA scar only; not child-DAC canon
05_PROJECT_MANAGEMENT/
  ├── 00_CANON/
  ├── 01_SPRINTS/
  ├── 02_AUDITS/
  ├── 03_MEMOS/
  ├── 04_HISTORY/
  ├── 05_INTELLIGENCE/
  ├── 06_EXECUTIVE_PROGRAMS/
  └── 07_OPERATIONS/
06_SPANNING_COMMONS/
  ├── Habitat/
  ├── Nexus/
  └── branding/
07_PWAs/
  ├── emergentism_org/
  ├── skyzai_org/
  ├── skyzai_com/
  ├── apu_bot/
  ├── realityfutures_com/
  ├── circle_news/
  ├── qntm/
  └── other public app surfaces/
08_SOMA_LOG/
  └── YYYY-MM/
09_REFERENCE/
  └── DAC_FACTORY/
10_AGENTS/
  ├── 01_CANDALA_FIREWALL/
  ├── 02_SUDRA_EXPLORER/
  ├── 03_VAISYA_AUDITOR/
  ├── 04_KSATRIYA_EXECUTOR/
  ├── 05_BRAHMANA_ARCHITECT/
  ├── 06_SADHU_COMPRESSOR/
  ├── 07_RSI_CONSTITUTION/
  ├── 20_OPERATIONALIZED/
  └── AIA_PRODUCT/
99_ARCHIVE/
```

Two follow-ups are needed before any move:

1. `03_PRODUCTS/` exists and has a valid README, but root README and
   `manifest.yaml` still understate it. Decide whether it is an active product
   lane, compatibility lane, or should be folded into `07_PWAs/` and
   `02_SKYZAI/04_PUBLIC_SCAFFOLD/`.
2. `04_CHILD_DAVS/AGENTZ_CLOUD/` stays as technical implementation lane only;
Agentz itself remains the applied-core state front door at
   `02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/`.

### 02_SKYZAI/02_PUBLIC_SCAFFOLD

Keep the public DAC-machine scaffold. Its current sequence is logical:

```text
00_META/
00_REFERENCE/
  ├── implementation_scaffold/
  └── public_surfaces/
01_FACTORY/
02_WALLET/
03_EQUITY/
04_CREDIT/
05_DEX/
06_POS/
  └── brand/
07_AGENTS/
08_CORTEX/
09_NEXUS/
10_AIA/
11_TRIVIUM/
12_COVENANT/
13_LAUNCH/
14_FRONTEND/
15_SDK/
16_API/
17_OPERATIONAL/
91_COMPATIBILITY/
```

Do not split this into multiple product roots. This is a composition surface,
not a live organism and not a legal entity.

### 04_ENTITIES

Keep entity membranes explicit:

```text
00_SHARED/
  ├── DAC_TEMPLATE/
  └── REPLICATION_PACKET/
FOUNDATION/
  ├── CANON/
  ├── brand/
  ├── emergentism_org/
  ├── reference/
  ├── stakeholders/
  ├── wiki/
  └── _archive/
MENEXUS/
  ├── brand/
  ├── finance/
  ├── legal_templates/
  ├── operations/
  ├── partners/
  ├── product_specs/
  ├── source_notes/
  ├── stakeholders/
  └── wiki/
AUREUS/
  ├── brand/
  ├── stakeholders/
  └── wiki/
HELIOS/
  ├── agents/
  ├── brand/
  └── website/
```

Each entity can have its own `brand/`, `stakeholders/`, `wiki/`, and
operation-specific folders. Do not mix QNTM (the institutional MPC/ZK-Identity rail), Tokencen, or Agentz into this root
unless a legal/entity decision changes.

### 03_VENTURES/_PORTFOLIO

Target shape:

```text
00_SHARED/                 proposed only if shared portfolio conventions grow
QNTM (the institutional MPC/ZK-Identity rail)/                      UK-FCA banking path
  ├── 00_CONTROL/
  ├── 00_INVESTOR_PACKET/
  ├── 01_ENTITY_CANON/
  ├── 03_BRAND_ASSETS/
  ├── QNTM_DATA_ROOM/
  ├── SKYZAI_BRIDGE/
  ├── intelligence/
  ├── stakeholders/
  ├── wiki/
  └── 90_PROVENANCE/
TOKENIZATION_CENTRES/      Tokencen country-centre lane
  ├── 00_GENERAL/
  ├── 01_KINGDOM_OF_SAUDI_ARABIA/
  └── 02_UNITED_ARAB_EMIRATES/
SHARED_RESEARCH/           reference inputs only
SKYZAI_BRIDGE/             commons-interface map
```

Agentz is no longer the special non-venture occupant of this root. It moved to
`02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/`. Keep Tokencen and QNTM (the institutional MPC/ZK-Identity rail) as portfolio lanes.

Agentz front-door expansion now lives under Skyzai organs:

```text
02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/
├── AGENT_README.md                  agent-only one-page entry generated from README + AGENTS
├── README.md                        human identity and boundary
├── 00_ROUTE_MAP/                    source-owner map; no duplicated doctrine
│   ├── deployed-agent-binding table
│   ├── source-vs-runtime matrix
│   └── migration compatibility map
├── 01_IDENTITY_AND_BOUNDARIES/      what Agentz is and is not
│   ├── non-entity boundary
│   ├── non-child-DAC boundary
│   └── regulated-claims boundary
├── 02_SOURCE_CANON/                 pointers to Rosetta agent genotype
│   ├── 01_EMERGENTISM/.../08_AGENTS pointers
│   ├── Uplink 06_AGENTS pointer
│   └── Rosetta row pointer
├── 03_RUNTIME_DISPATCH/             pointers to .codex/agents and sync rules
│   ├── .codex/agents/rows binding
│   ├── project agent TOML binding
│   ├── spawn-plan / managed-agent adapters
│   └── receipt requirement
├── 04_AGENT_SPECIFICATIONS/         phenotype-spec index
│   ├── L1_CANDALA_FIREWALL -> candala_firewall
│   ├── L2_SUDRA_EXPLORER -> sudra_explorer
│   ├── L3_VAISYA_AUDITOR -> vaisya_auditor
│   ├── L4_KSATRIYA_EXECUTOR -> ksatriya_executor
│   ├── L5_BRAHMANA_ARCHITECT -> brahmana_architect
│   ├── L6_SADHU_COMPRESSOR -> sadhu_compressor
│   └── L7_RSI_CONSTITUTION -> rsi_constitution
├── 05_GOOSE_AND_ROUTERS/            Goose/TOM/router integration maps
│   ├── derived-runtime doctrine
│   ├── router disambiguation
│   └── continuous-run discipline
├── 06_ARCHITECTURE_L5/              L5 design and critical assessments
│   ├── polygenetic tree architecture
│   ├── quantity/quality subagent orchestration
│   └── critical assessments
├── 07_CONSTITUTION_L7/              K2 directives and invariant boundaries
│   ├── K2 envelope requirements
│   ├── no-autonomy boundary
│   └── witness review
├── 08_AGENTZ_CLOUD_PWA/             public PWA map
│   ├── public tree branches
│   ├── Academy routes
│   ├── runtime interface routes
│   └── claim-language guardrails
├── 09_ACADEMY/                      education/product map
│   ├── L1-L7 disclosure ladder
│   ├── exercises
│   └── certificates or receipts, if ever ratified
├── 10_CHAPTERS/                     chapter adapters only
│   ├── Tokencen adapters
│   ├── QNTM (the institutional MPC/ZK-Identity rail) adapters
│   └── no hidden legal merger
├── 11_BRAND_LANGUAGE_CLAIMS/        public wording and banned phrases
│   ├── approved Agentz language
│   ├── banned Swiss / Series A / child-DAC claims
│   └── agentz.cloud wording
├── 12_AUDITS_RECEIPTS/              homology/tree/runtime receipts
│   ├── homology receipts
│   ├── Goose/router receipts
│   ├── deployment receipts
│   └── stale-reference sweeps
├── 13_MIGRATION_PREP/               link inventory and dry-run packets
│   ├── 03_VENTURES/_PORTFOLIO/Agentz absorption packet
│   ├── AGENTZ_CLOUD technical-lane decision packet
│   └── compatibility stub plan
└── 99_ARCHIVE_INDEX/                index only; cold history remains in owner archives
```

This outline is a routing shell. It should not physically absorb all Agentz
material. The source genotype remains in `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/`,
runtime TOMLs remain in `.codex/agents/`, and the inherited `agentz.cloud`
technical/PWA material remains in `02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/`
until a K2-approved move packet exists.

### 02_SKYZAI/06_SPECTRE

Keep SPECTRE as peer substrate:

```text
00_BACKBONE/
01_SPECTRE_NTON/
  └── N:N routing
02_RELAY_1TON/
  └── 1:N broadcast
03_AXIOM_NTO1/
  └── N:1 convergence
04_FLOW_1TO1/
  └── 1:1 direct settlement
05_ENERGY_MARKET/
06_HOLARCHY/
10_ARCHITECTURE/
20_NETWORK/
30_DEPLOYMENT/
91_COMPATIBILITY/
```

Do not nest SPECTRE under Skyzai. Do not give it internal caste agents unless
K2 reclassifies it; it is substrate, not a Three-Stage Process organ.

### 90_ARCHIVE

Keep archive organized by source-owner and archive function:

```text
00_INDEX/
01_LANE_LEGACY/
  ├── framework/
  ├── intake/
  ├── organism/
  ├── root/
  ├── sprint/
  ├── tools/
  └── uplink/
02_ENTITY_HISTORY/
  ├── Agentz/
  ├── FOUNDATION/
  ├── MENEXUS/
  ├── Skyzai/
  ├── VAYAN/
  ├── aureus/
  └── helios/
03_RAW_INTAKE/
  └── YYYY-MM-DD/
04_PROCESSED_INTAKE/
  └── PROCESSED/
05_DATA_ROOMS_AND_EXPORTS/
06_BINARY_COLDSTORE_CANDIDATES/
99_TOMBSTONES/
```

Archive before delete. Tombstones must preserve enough route information for a
future agent to understand why an old path should not be revived.

## Implementation Receipt -- 2026-05-08

The depth-1 navigation sweep is now structurally complete: dry-run inventory
via `01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 1`
reports zero missing depth-1 `AGENTS.md` files across the seven canonical roots.

The first depth-3/depth-4 implementation pass is scoped to the Agentz organ,
because it is the active polygenetic-tree routing surface. The Agentz subfolder
shell now has local `AGENTS.md` coverage from:

```text
02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/00_ROUTE_MAP/
through
02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/99_ARCHIVE_INDEX/
```

including:

```text
03_RUNTIME_DISPATCH/01_DEPLOYED_AGENT_BINDINGS/
08_AGENTZ_CLOUD_PWA/01_POLYGENETIC_TREE/
```

This makes the `agentz.cloud` branch contract navigable by agents without
turning the public PWA into the source of truth. The branch route remains:

```text
agentz.cloud branch
  -> Agentz organ subfolder
  -> deployed-agent binding
  -> .codex/agents/rows/0X_LX_<agent>.toml
  -> .codex/agents/<agent runtime TOML>
  -> audit/runtime receipt
```

The next root-by-root pass executed the `01_EMERGENTISM/` depth-2 cleanup:
all source-core state depth-2 lanes now have local `AGENTS.md` routing, and the
two missing depth-2 `README.md` anchors were added at:

```text
01_EMERGENTISM/11_UPLINK/00_INDEX/README.md
01_EMERGENTISM/90_ARCHIVE/50_AUDITS/README.md
```

The generator now distinguishes active owner lanes from archive and
compatibility lanes so archive folders are not promoted to current canon by
their generated routing surfaces. Remaining depth-2 cleanup should continue
root by root; generated output, vendor copies, and intake folders still require
owner review before write.

## Migration Sequence

1. **No-move doc repair.** Fix root-facing docs that still contradict the live
   folder law. This packet begins that pass.
2. **Owner inventory.** For each root, inventory depth-1 folders against
   `README.md`, `AGENTS.md`, and `manifest.yaml`.
3. **Route classification.** Mark each odd folder as active owner lane,
   support adjunct, compatibility stub, local generated output, intake, or
   archive candidate.
4. **Navigation standardization.** Ensure every active root has clear
   `README.md` and `AGENTS.md` coverage before content moves.
5. **Move packets only after K2.** For actual folder moves, prepare exact
   source/destination tables, compatibility stubs, and path-reference repair.
6. **Audit gates.** After each move packet: `make tree-audit`,
   `make manifest-check`, and the relevant Agentz/Goose audits if agent routing
   surfaces changed.

## Immediate Work Orders

| Priority | Work order | Boundary |
|---|---|---|
| P0 | Keep root README, manifest, and actual disk tree in sync. | reversible docs only |
| P0 | Resolve whether `02_SKYZAI/01_NOOSPHERE/03_PRODUCTS/` should be manifest-active. | no moves before decision |
| P0 | Repair stale Agentz Swiss / Series A / child-DAC wording in owner surfaces. | archive/supersede before delete |
| P0 | Absorb old `05_PORTFOLIO_ORGS/Agentz/` material into `04_NETWORK_ENTITIES/SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/` after dirty parallel work is reviewed. | K2 move packet required |
| P0 | Decide whether `02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/` stays as a named technical-lane scar or migrates later under the Agentz organ. | K2 move packet required |
| P1 | Add or refresh depth-2 `AGENTS.md` coverage root by root after dry-run review. | navigation only |
| P1 | Classify root `docs/`, `extract/`, `tmp/`, `output/`, `cache/`, and `out/` in README and ignore policy. | no deletes |
| P1 | Audit `02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/03_AGENT_SPECIFICATION/README.md`; it appears to describe AIA_PRODUCT while `INDEX.md` is the actual Agentz spec index. | route repair only |
| P1 | Audit `02_SKYZAI/01_NOOSPHERE/04_CHILD_DAVS/AGENTZ_CLOUD/CHAPTERS/01_TOKENIZATION/README.md` against its `CHARTER.md`; stale Swiss / Series A language appears to remain. | no legal merger |
| P1 | Repair Uplink `00_CORE/00_INDEX.md` manifest pointer and compressed Uplink Agentz/Tokencen naming. | avoid sweeping parallel edits |
| P1 | Clarify SPECTRE agent-name branding vs SPECTRE physical mesh substrate. | naming only |
| P2 | Produce root-by-root migration tables for any remaining `_from_root/` or compatibility lanes. | K2 before moves |

## Hard Stops

- Do not delete live content during outline work.
- Do not create new peer roots for data rooms, websites, brands, Agentz, QNTM (the institutional MPC/ZK-Identity rail),
  Tokencen, or SPECTRE derivatives.
- Do not merge legal/entity lanes by filesystem convenience.
- Do not turn temporary output into canon.
- Do not let `agentz.cloud` language reanimate the dissolved Swiss company or
  Series A frame.

The optimal outline is therefore conservative: keep the seven-root architecture,
standardize local navigation, repair stale route text, then move only with a
packet and receipt.
