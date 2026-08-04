# Kintsugi Formal-Logic Repair Program — Design Specification

**Date:** 2026-07-11

**Status:** Design approved; implementation not started

**Scope order:** A — signed kernel and recent changes; B — active corpus; C — public phenotype

**Repository approval base:** `main@736cf22`

**Observed execution head:** `main@454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22` (post-approval concurrency addendum)
**Working branch:** `codex/kintsugi-formal-logic-spec`

## 1. Purpose

Build a repeatable repair discipline for the Emergentist framework in which
formal criticism leaves visible, testable improvements rather than silent
rewrites. The program applies the Kintsugi metaphor literally at the level of
method:

1. expose a precise fracture;
2. preserve the failed form as evidence;
3. identify the surviving kernel;
4. make the smallest truthful repair;
5. attach a visible Golden Seam;
6. add a regression fixture that detects recurrence; and
7. propagate the repair from its owner source into derivative summaries.

The outcome is not a declaration that Emergentism is unbreakable. The outcome
is a corpus that can say exactly what survived, what failed, why it failed, and
what evidence could change the verdict again.

## 2. Starting state

The repository already contains:

- the K2-countersigned Burri Rules and receipts 104–107 as historical
  provenance;
- the 30-item Burri Rules derivation ledger;
- formal-logic audit packet 103, which formalized 48 claims and retained nine
  defects after steelmanning;
- a staged Kintsugi Protocol at
  `00_META/00_THE_KINTSUGI_PROTOCOL.md`; and
- a frozen public phenotype under `12_PUBLIC_SITE/`.

The staged protocol refers to a canonical Phase A Formal Stress Ledger numbered
108 at `108_FORMAL_STRESS_LEDGER_2026_07_11.md`; that exact receipt does not
exist. Post-approval `main` added a differently named staged predecessor,
`108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md`. It is provenance,
not the Phase A receipt, and cannot satisfy a `phaseReceipt` path or status. The
protocol also contains claims that fail its own intended discipline: a visible
repair is treated as an automatic truth warrant; its antifragility score adds
heterogeneous quantities; clean no-change trials are misclassified as failures;
and the breakage bounty does not yet protect consent, privacy, compensation,
custody, reversibility, or exit.

The baseline repository test suite currently reports 19 collected nodes: 14
passing tests and five pre-existing allowed failures. The failures belong to marketplace and cross-entity
tests whose Skyzai/OFN fixtures are absent from the current Documents topology.
They occur identically on `main` and in the isolated worktree. They are recorded
as baseline evidence and are outside this program unless a Kintsugi change
directly alters those tests.

### 2.1 Post-approval concurrency addendum

After this design was approved at `736cf22`, canonical `main` advanced through:

- `6c2106f`, which added the staged predecessor receipt 108 and narrowed the
  product-survival claim in
  `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/36_THE_DIMENSIONAL_TROPHIC_CASCADE.md`;
  and
- `2ab90ac`, which added
  `01_TELEOLOGY/02_THE_DERIVATION/07A_F5_UNBUNDLED_COUPLING_PER_DIMENSION_PENDING_K2.md`;
  and
- the intervening historical change that added the open QM/GR ordering tension
  at `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/PD_22A_QM_GR_DIMENSIONAL_ORDERING_TENSION_PENDING_K2.md`;
  and
- `454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22`, the current canonical head, which added
  `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md`.

These commits do not change the approved semantics. They change the execution
inventory. Phase A must rebase onto `454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22`, re-freeze its manifest and
baseline there, and harvest the three new owner claim surfaces as recent-change
inputs.
The differently named staged receipt 108 is a raw-hashed `RECEIPT/PROVENANCE`
source frozen at raw SHA-256
`9cf25b80e6c252aa8d95b63ea1c7cc1ed361c05dedaea4aef72fa001f691069c`
and remains byte-identical. The canonical Phase A receipt remains the exact A4
path and typed ID declared below.

The proof-layer audit at the exact 109 path above is frozen at raw SHA-256
`3d9f63df9ce8aabfa9a16ac5dd25acabf3084b75b6ad29740a61e078ecebd629`.
It is immutable external/pre-program support and provenance only, registered as
`SRC-PROV-109-PROOF-AUDIT` with `kind=SUPPORT` and
`authorityRole=PROVENANCE`: it is not a Kintsugi phase receipt, claim owner,
claim dependency, or authority. Its historical `PENDING_K2` lifecycle creates
no K2 gate for Kintsugi. The human number 109 is therefore non-addressable by
itself: the future Phase B receipt is only `REC-B-109` at the exact path
`11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md`.
Bare `109` has no authority; receipt references require both the typed ID and
exact filename, and Phase B adds the two-row README route defined in §12.

The external audit attachment at
`/Users/Yves/.codex/attachments/ec649130-9018-4d89-a0f1-99b9e82f34b5/pasted-text.txt`
is potential A0B support only, frozen at raw SHA-256
`2937faf077f58a49e3c5953d33c3413ea3108350f82c8166eaf54818cdb5ad73`.
It is `[B/D]` external support; every finding starts `ALLEGED`, and its claimed
counts are not proof. A0B may hash-pin and deduplicate it before `MAN-A-001`
freezes. It is not in A0 scope.

This design amendment and the paired A0-plan amendment are pre-rebase planning
changes outside the A0 implementation diff. A0 still changes exactly four
declared paths and preserves the 19-collected/five-allowed-failure baseline.
If canonical `main` is no longer `454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22` when execution begins, execution
stops before rebasing, inventories the additional delta, and updates this
addendum and the manifest explicitly.

## 3. Governance decision

This program has **no K2 approval, countersign, checkpoint, or veto gate**.
Existing K2-labelled receipts remain untouched as historical provenance; they
do not determine whether a new logical conclusion is valid.
The A0 -> A0B -> A1 -> A2 sequence proceeds one after the other without an
extra K2 pause; no `PENDING_K2` provenance lifecycle changes that sequencing.

Future acceptance is evidence-governed. A repair becomes verified only when:

- its proposition and types are explicit;
- the inference has been checked independently;
- premise soundness and evidence tier are stated separately from validity;
- the Beauty, Truth, and Justice gates pass;
- the owner source and seam ledger agree;
- a regression fixture detects the original failure; and
- an independent delta review finds no new severe fracture introduced by the
  repair.

This decision is bounded to the Kintsugi repair program. It does not silently
rewrite unrelated private-DAV or public-DAV governance surfaces. A future
repo-wide retirement of K2 terminology would be a separate explicit project.

## 4. Scope and non-goals

### In scope

- active owner canon and its active compression surfaces;
- formal validity, premise soundness, modal force, type correctness,
  countermodels, evidence tiers, and falsifiers;
- visible before/after repair history;
- deterministic seam metadata and validation;
- Beauty/Truth/Justice consequence accounting;
- read-only comparison of the frozen public phenotype against repaired canon;
  and
- exact propagation queues for later public work.

### Out of scope

- modifying `90_ARCHIVE/` or `91_COMPATIBILITY/`;
- modifying `12_PUBLIC_SITE/` during this program;
- modifying the contents of receipts 104–107, modifying the staged predecessor
  `108_THE_FORMAL_STRESS_LEDGER_KEEL_RESOLUTION_PENDING_K2.md`, modifying the
  pre-program proof audit
  `109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md`, or renaming their
  historical `PENDING_K2` filenames;
- treating the external audit attachment as an A0 input or treating any of its
  `[B/D]` allegations or claimed counts as proof;
- silently changing the signed `Egregorotype`/`Egregoreotype` spelling question;
- proving literal quantum collapse, physical retrocausality, F5 as a recognized
  physical interaction, or strong emergence from absence of a reducing law;
- converting every sentence in the corpus into symbolic logic; and
- repairing unrelated Skyzai, OFN, marketplace, or cross-entity fixtures.

## 5. Core model

### 5.1 Unit of trial

A trial operates on one load-bearing claim:

```text
Claim = <identity, owner, proposition, types, premises, inference,
         quantifiers, modality, scope, evidence tier, dependencies>
```

A paragraph may contain several claims and must be split before judgment. A
symbol that changes meaning between registers must be indexed by register or
replaced with distinct typed symbols.

The program distinguishes:

- **validity:** whether the conclusion follows from the declared premises;
- **soundness:** whether those premises are supported at their declared tier;
- **modality:** actual, possible, necessary, normative, definitional, or
  conjectural force;
- **typing:** whether every operator consumes and returns the kind of object its
  signature declares; and
- **scope:** the domain in which the conclusion is licensed.

### 5.2 Logic used

The program uses the weakest adequate formalism:

- propositional logic for dependency and contradiction checks;
- many-sorted first-order logic for typed entities and relations;
- explicit modal annotations for possibility, necessity, actuality, and
  normative force;
- probability-space typing for stochastic claims;
- algebra/calculus verification for mathematical claims; and
- countermodels whenever a uniqueness, necessity, universality, or derivation
  claim is challenged.

Rosetta projection is never an inference rule. A structural resemblance may
transfer a question or vocabulary, but it cannot transfer proof or upgrade an
evidence tier.

### 5.3 Verdict vocabulary

Every trial records separate validity and soundness judgments:

```text
validityVerdict ∈ {VALID, INVALID, NOT_APPLICABLE}

soundnessVerdict ∈ {
  SUPPORTED,
  CONDITIONALLY_SUPPORTED,
  UNSUPPORTED,
  REFUTED,
  NOT_APPLICABLE
}
```

It then ends in exactly one overall verdict:

```text
VALID_SOUND
VALID_CONDITIONAL
VALID_UNSUPPORTED_PREMISE
INVALID
UNDERDETERMINED
DEFINITIONAL
OPEN_CONJECTURE
REFUTED
```

`VALID_SOUND` is relative to the stated domain and evidence. It does not mean
metaphysically final. `DEFINITIONAL` records a lawful scaffold choice without
pretending it was derived. `OPEN_CONJECTURE` is a valid endpoint and must not be
repaired into false certainty.

### 5.4 Defect vocabulary

The initial controlled defect classes are:

```text
EQUIVOCATION
TYPE_ERROR
NON_SEQUITUR
HIDDEN_PREMISE
CIRCULARITY
TAUTOLOGY_LAUNDERING
CATEGORY_ERROR
INVALID_MODAL_STRENGTH
QUANTIFIER_SHIFT
SCOPE_ERROR
FALSE_DILEMMA
SELF_SEALING_FALSIFIER
EVIDENCE_TIER_INFLATION
AUTHORITY_DRIFT
COMPRESSION_DRIFT
DIRECT_CONTRADICTION
```

New classes require a schema-version change rather than free-text invention.

## 6. Golden Seam contract

### 6.1 Visible marker

An owner repair receives one compact marker:

```text
[金 KIN-0012] NARROW after hidden-premise countermodel;
surviving kernel and full before/after reasoning: seam ledger KIN-0012.
```

The full seam appears once in the central ledger. Derivative documents cite the
owner and seam ID; they do not repeat the full block. This preserves visibility
without turning the prose into repair metadata.

### 6.2 What a seam warrants

A seam warrants only this statement:

> This claim was tested by the named trial, failed or survived in the recorded
> way, and now carries a regression fixture for that failure mode.

A seam does not make a claim truer than all untested alternatives. Trust tracks
evidence, trial quality, scope, and repeatability—not the presence of gold
alone.

### 6.3 Repair kinds

The first schema permits only:

```text
NARROW
SPLIT
RETIER
RETRACT
RENAME
RELINK
```

These operations may remove, distinguish, downgrade, or correctly reconnect
existing claims. New supporting theory is not disguised as repair: it enters as
a separate `[D/C]` claim with its own trial.

### 6.4 Repair states

```text
trial: TRIED -> DISPUTED | ADJUDICATED -> CLOSED

confirmed-break seam:
CONFIRMED -> REPAIRED -> VERIFIED
          |
          -> HELD_OPEN
          -> RETRACTED
```

- A disputed trial has no seam until its break is adjudicated as confirmed.
- `HELD_OPEN` is correct when no warranted repair exists. It records
  `containment`, `residualRisk`, and a discriminator, but has no `repairKind` or
  `afterQuote`. A `CRITICAL` or `MAJOR` held-open crack blocks phase completion;
  only a `MINOR` held-open item or an excluded non-authoritative source may pass
  a phase boundary.
- `RETRACTED` preserves the original text in seam history while removing its
  authority; it uses `repairKind=RETRACT` and records the exact replacement
  tombstone or retraction notice as `afterQuote`.
- `REPAIRED` requires `repairKind` and `afterQuote`.
- `VERIFIED` requires independent logic review and passing regression tests.
- A `VERIFIED` seam is immutable. Later derivative propagation is an append-only
  `propagation` event tied to a later receipt; it never mutates the seam frozen
  in an earlier validation bundle.

Allowed seam transitions are exactly:

```text
CONFIRMED -> REPAIRED | HELD_OPEN | RETRACTED
REPAIRED  -> VERIFIED
HELD_OPEN -> REPAIRED | RETRACTED
```

`RETRACTED` is terminal unless a new claim ID is created; reintroducing the old
claim under the same ID is forbidden. A later counterexample to a repaired or
verified claim creates a new trial and successor seam with `priorSeamIds`; the
older seam remains immutable evidence.

A clean trial that finds no break creates a trial record and phase receipt, not
a seam. It may increase tested-claim coverage without inventing gold.

## 7. Machine-readable seam interface

`03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json` is a metadata mirror,
not a semantic authority. Its top-level interface is:

```text
schemaVersion
program
manifests
sources
claims
trials
seams
antibodies
discriminators
fixtures
propagations
phaseReceipts
```

`schemaVersion` is exactly `"1.0.0"` for the first implementation. Controlled
claim types and modalities are:

```text
claimType ∈ {
  MATHEMATICAL, STRUCTURAL, INTERPRETIVE,
  EMPIRICAL, NORMATIVE, METAPHORICAL
}

modality ∈ {
  ACTUAL, POSSIBLE, NECESSARY,
  NORMATIVE, DEFINITIONAL, CONJECTURAL
}

severity ∈ {CRITICAL, MAJOR, MINOR}
```

`CRITICAL` and `MAJOR` are severe. `CRITICAL` means a contradiction or type
failure in a load-bearing claim that invalidates downstream conclusions.
`MAJOR` means the surviving kernel remains usable but its scope, tier, or
inference is materially wrong. `MINOR` means the proposition survives and the
repair is presentational or local provenance correction.

The non-seam record interfaces are:

```text
program = {
  id: ID,
  title: TEXT,
  phaseOrder: [A, B, C],
  protectedPaths: LIST[PATH],
  semanticAuthority: PATH,
  noK2Gate: true
}

manifest = {
  id: ID,
  phase: A | B | C,
  baseCommit: COMMIT_HASH,
  canonicalBranch: main,
  canonicalCommit: COMMIT_HASH,
  discoveryRules: LIST[discoveryRule],
  candidateFiles: LIST[fileHashRecord],
  candidateFileCount: COUNT,
  includedFiles: LIST[fileHashRecord],
  finalFiles: LIST[fileHashRecord],
  finalFileCount: COUNT,
  excludedPaths: LIST[pathExclusion],
  eligibleFileCount: COUNT,
  scannedFileCount: COUNT,
  harvestedClaimIds: LIST[ID],
  excludedClaimIds: LIST[claimExclusion],
  eligibleClaimCount: COUNT,
  trialedClaimIds: LIST[ID],
  trialedClaimCount: COUNT,
  inventoryReviewPaths: LIST[PATH],
  protectedProvenance: LIST[protectedProvenanceRecord],
  protectedPaths: LIST[PATH],
  protectedTreeSnapshots: {
    isolated: LIST[fileHashRecord],
    canonical: LIST[fileHashRecord]
  },
  allowedChangePaths: LIST[PATH],
  closureOnlyPaths: LIST[PATH],
  allowedPreexistingUntracked: {
    isolated: LIST[fileHashRecord],
    canonical: LIST[fileHashRecord]
  }
}

source = {
  id: ID,
  path: PATH,
  kind: OWNER | SUPPORT | COMPRESSION | PUBLIC | RECEIPT,
  phases: LIST[A | B | C],
  sha256: RAW_HASH,
  authorityRole: SEMANTIC_OWNER | EVIDENCE | DERIVATIVE | PROVENANCE
}

claim = {
  id: ID,
  ownerSourceId: ID,
  ownerAnchor: TEXT,
  proposition: TEXT,
  claimType: CLAIM_TYPE,
  typedTerms: LIST[typedTerm],
  premises: LIST[premise],
  conclusion: TEXT,
  inference: inference,
  quantifiers: LIST[quantifier],
  modality: MODALITY,
  scope: scope,
  justiceScope: JUSTICE_SCOPE,
  justiceContext: justiceContext when triggered,
  evidence: evidence,
  dependencyClaimIds: LIST[ID]
}

trial = {
  id: ID,
  claimId: ID,
  manifestId: ID,
  triedQuote: TEXT,
  triedHash: TEXT_HASH,
  steelman: TEXT,
  countermodel: countermodel,
  breakState: NONE | ALLEGED | CONFIRMED,
  defectClass: DEFECT_CLASS | null,
  severity: SEVERITY | null,
  validityVerdict: VALIDITY_VERDICT,
  soundnessVerdict: SOUNDNESS_VERDICT,
  verdict: OVERALL_VERDICT,
  discriminatorIds: LIST[ID],
  seamId: ID | null,
  receiptId: ID,
  status: TRIED | DISPUTED | ADJUDICATED | CLOSED
}

antibody = {
  id: ID,
  seamId: ID,
  pattern: TEXT,
  matchMode: LITERAL | REGEX | SEMANTIC_FIXTURE,
  semanticEvaluator: SEMANTIC_EVALUATOR | null,
  scopeGlobs: LIST[TEXT],
  excludeGlobs: LIST[TEXT],
  positiveFixtureIds: LIST[ID],
  negativeFixtureIds: LIST[ID],
  quotationFixtureIds: LIST[ID],
  historicalFixtureIds: LIST[ID]
}

discriminator = {
  id: ID,
  claimId: ID,
  question: TEXT,
  method: TEXT,
  cheapestTest: TEXT,
  expectedObservations: LIST[TEXT],
  decisionRule: TEXT,
  status: QUEUED | RUNNING | DECISIVE | INCONCLUSIVE | RETIRED
}

fixture = {
  id: ID,
  kind: POSITIVE | NEGATIVE | QUOTATION | HISTORICAL | MUTATION,
  payloadKind: TEXT | JSON,
  payload: TEXT,
  expectedExitCode: 0 | 1,
  expectedErrorCodes: LIST[TEXT],
  expectedAntibodyIds: LIST[ID],
  antibodyIds: LIST[ID],
  seamIds: LIST[ID]
}

propagation = {
  id: ID,
  seamId: ID,
  receiptId: ID,
  derivativeSourceId: ID,
  derivativeAnchor: TEXT,
  derivativeQuote: TEXT,
  derivativeHash: TEXT_HASH,
  status: VERIFIED
}

phaseReceipt = {
  id: ID,
  phase: A | B | C,
  path: PATH,
  status: DRAFT | COMPLETE | VERIFIED,
  manifestId: ID,
  dependsOnReceiptIds: LIST[ID],
  claimIds: LIST[ID],
  trialIds: LIST[ID],
  seamIds: LIST[ID],
  propagationIds: LIST[ID],
  reviewTargetDigest: RAW_HASH | null,
  validationBundlePath: PATH | null,
  validationDigest: RAW_HASH | null,
  logicReviewPath: PATH | null,
  btjReviewPath: PATH | null
}
```

Controlled values are:

```text
source.kind ∈ {OWNER, SUPPORT, COMPRESSION, PUBLIC, RECEIPT}
source.authorityRole ∈ {SEMANTIC_OWNER, EVIDENCE, DERIVATIVE, PROVENANCE}
antibody.matchMode ∈ {LITERAL, REGEX, SEMANTIC_FIXTURE}
antibody.semanticEvaluator ∈ {
  VERDICT_MATRIX, JUSTICE_CONTEXT, RECEIPT_ROLE,
  REGISTER_INDEX, QUANTUM_MEASURE, OPTION_CONE,
  TROPHIC_AGGREGATOR
}
discriminator.status ∈ {QUEUED, RUNNING, DECISIVE, INCONCLUSIVE, RETIRED}
fixture.kind ∈ {POSITIVE, NEGATIVE, QUOTATION, HISTORICAL, MUTATION}
gate.status ∈ {PENDING, PASS, FAIL}
trial.status ∈ {TRIED, DISPUTED, ADJUDICATED, CLOSED}
trial.breakState ∈ {NONE, ALLEGED, CONFIRMED}
seam.status ∈ {CONFIRMED, REPAIRED, HELD_OPEN, RETRACTED, VERIFIED}
propagation.status = VERIFIED
phaseReceipt.status ∈ {DRAFT, COMPLETE, VERIFIED}
claim.justiceScope ∈ {
  NONE, INDIVIDUAL, COLLECTIVE, NORMATIVE, COLLECTIVE_NORMATIVE
}
manifest.protectedProvenance.mode ∈ {FULL_FILE, EXACT_SPAN}
```

Cross-field logic is mandatory:

- `claimType=NORMATIVE` or `modality=NORMATIVE` requires `justiceScope` to be
  `NORMATIVE` or `COLLECTIVE_NORMATIVE`; `NONE`, `INDIVIDUAL`, and `COLLECTIVE`
  are invalid for that claim.
- The overall verdict must match the validity/soundness matrix:

```text
VALID_SOUND               = VALID / SUPPORTED
VALID_CONDITIONAL         = VALID / CONDITIONALLY_SUPPORTED
VALID_UNSUPPORTED_PREMISE = VALID / UNSUPPORTED
INVALID                   = INVALID / NOT_APPLICABLE
UNDERDETERMINED           = INVALID / NOT_APPLICABLE
DEFINITIONAL              = NOT_APPLICABLE / NOT_APPLICABLE
OPEN_CONJECTURE           = NOT_APPLICABLE /
                            UNSUPPORTED | CONDITIONALLY_SUPPORTED
REFUTED                   = VALID | NOT_APPLICABLE / REFUTED
```

The schema encodes these combinations with `allOf` and `if/then`; the validator
does not infer or repair a mismatched verdict.

The normative machine contract is
`03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json`, expressed as JSON
Schema Draft 2020-12. It defines the core data file, the Phase C queue, and the
baseline-failure allowlist, with `additionalProperties: false` at every object.
The standard-library validator
implements only the schema keywords used by that file: `type`, `required`,
`properties`, `additionalProperties`, `enum`, `pattern`, `minimum`, `minLength`,
`minItems`, `maxItems`, `items`, `uniqueItems`, `const`, `$ref`, `allOf`, `anyOf`,
`oneOf`, `if/then/else`, plus the structural meta-keywords `$schema`, `$id`, and
`$defs`. The schema defines exactly `$defs.coreData`, `$defs.publicQueue`, and
`$defs.baselineAllowlist`; each CLI input role selects its named root definition
before validation. `$schema`, `$id`, and `$defs` organize the schema but do not
act as instance assertions. An unknown key, unknown schema keyword, unresolved
reference, or unconsumed field fails validation.

The types, enums, conditionals, cardinalities, and references in this section
are normative now; the schema artifact is their mechanical transcription and
may not choose alternative types or defaults. The implementation plan must
show the complete schema content rather than delegating any field decision to
the implementer.

The schema uses these primitive conventions:

```text
ID        = non-empty string matching ^[A-Z][A-Z0-9_-]*$
PATH      = repository-relative POSIX path; no leading slash or '..'
COMMIT_HASH = string matching ^[0-9a-f]{40}$
RAW_HASH  = string matching ^sha256:[0-9a-f]{64}$
TEXT_HASH = string matching ^sha256-text-lf:[0-9a-f]{64}$
TEXT      = non-empty UTF-8 string
COUNT     = integer >= 0; booleans are rejected as integers
BOOLEAN   = JSON true or false
LIST[T]   = JSON array of T; unique where the schema says uniqueItems=true

CLAIM_TYPE = the six claimType values in §7
MODALITY = the six modality values in §7
SEVERITY = CRITICAL | MAJOR | MINOR
DEFECT_CLASS = the controlled vocabulary in §5.4
VALIDITY_VERDICT = the validity vocabulary in §5.3
SOUNDNESS_VERDICT = the soundness vocabulary in §5.3
OVERALL_VERDICT = the eight overall verdicts in §5.3
REPAIR_KIND = NARROW | SPLIT | RETIER | RETRACT | RENAME | RELINK
JUSTICE_SCOPE = NONE | INDIVIDUAL | COLLECTIVE |
                NORMATIVE | COLLECTIVE_NORMATIVE
```

Named nested values have these exact shapes:

```text
fileHashRecord = {path: PATH, kind: FILE | SYMLINK, sha256: RAW_HASH}
pathExclusion = {path: PATH, reason: TEXT}
claimExclusion = {claimId: ID, reason: TEXT}
typedTerm = {symbol: TEXT, type: TEXT, definition: TEXT}
premise = {
  id: ID, proposition: TEXT, evidence: evidence,
  sourceIds: LIST[ID]
}
inference = {rule: TEXT, formalization: TEXT}
quantifier = {
  variable: TEXT,
  kind: FOR_ALL | EXISTS | EXACTLY_ONE | NONE,
  domain: TEXT
}
scope = {
  domain: TEXT,
  population: TEXT,
  timeHorizon: TEXT,
  conditions: LIST[TEXT]
}
evidence = {
  strength: A | S | I | C,
  sourced: BOOLEAN,
  lifecycle: DRAFT | ACTIVE | RETIRED
}
justiceContext = {
  individual: TEXT,
  whole: TEXT,
  eta: TEXT,
  beneficiary: LIST[TEXT],
  costBearer: LIST[TEXT],
  consent: {
    status: OBTAINED | NOT_REQUIRED | MISSING,
    basis: TEXT
  },
  custody: TEXT,
  reversibility: REVERSIBLE | PARTIAL | IRREVERSIBLE,
  exit: TEXT,
  optionConeEffect: {
    direction: WIDENS | NEUTRAL | CONTRACTS | MIXED,
    rationale: TEXT
  }
}
countermodel = {
  description: TEXT,
  construction: TEXT,
  defeatedConclusion: TEXT
}
gate = {
  status: PENDING | PASS | FAIL,
  rationale: TEXT,
  reviewerPath: PATH | null
}
credit = {displayName: TEXT, role: TEXT}
containment = {
  antibodyIds: LIST[ID],
  blockedDependencyClaimIds: LIST[ID],
  rationale: TEXT
}
residualRisk = {severity: CRITICAL | MAJOR | MINOR, description: TEXT}
discoveryRule = {
  id: ID,
  includeGlobs: LIST[TEXT],
  excludeGlobs: LIST[TEXT],
  parser: MARKDOWN | HTML | JSON | SOURCE_INDEX,
  rationale: TEXT
}
protectedProvenanceRecord =
  FULL_FILE {path: PATH, mode: FULL_FILE, sha256: RAW_HASH}
  | EXACT_SPAN {
      path: PATH, mode: EXACT_SPAN, exactSpan: TEXT, sha256: RAW_HASH
    }
```

Fields named `typedTerms`, `premises`, `quantifiers`, and `discoveryRules` are
non-empty arrays of their corresponding nested type. `beautyGate`, `truthGate`,
and `justiceGate` are `gate` objects. `countermodel` is always present; when no
countermodel is found, its description and construction state the bounded
search performed and `defeatedConclusion` states `NONE_FOUND`.

Only these list fields may be empty:

- `manifest.excludedPaths`, `excludedClaimIds`, and either root-specific
  `allowedPreexistingUntracked` list when no such item exists;
- `claim.dependencyClaimIds` and `scope.conditions` when the claim declares no
  dependency or condition;
- `trial.discriminatorIds` when `breakState=NONE`;
- `seam.priorSeamIds` for the first seam on a claim;
- `antibody.excludeGlobs` when the antibody has no excluded scope;
- fixture error/match/reference lists when their declared fixture kind and
  `expectedExitCode` make that relationship inapplicable;
- Phase A's `phaseReceipt.dependsOnReceiptIds` and a phase receipt's `seamIds`
  when that phase confirmed no break; and
- a phase receipt's `propagationIds` when that phase performs no derivative
  propagation; and
- `reviewAttestation.findingIds`, `openSevereFindingIds`,
  `approvedUpgradeSeamIds`, and `approvedGateSeamIds`; PASS requires
  `openSevereFindingIds=[]`, while the other three remain empty when no finding,
  upgrade, or terminal gate applies; and
- Phase C `candidateOwners` and owned `seamIds` under the tagged-union rules in
  §13.

Every other list has `minItems: 1`; all ID lists use `uniqueItems: true`.

`program` is exactly one object. Every plural top-level key is an array.
`manifests`, `sources`, `claims`, `trials`, and `phaseReceipts` have at least one
record. `seams`, `antibodies`, `discriminators`, and `fixtures` may be empty only
during the Phase A bootstrap state; `propagations` may be empty in any phase
that performs no derivative propagation. A verified receipt may not reference
an empty required collection.

Cross-references are closed and typed:

```text
manifest.harvestedClaimIds / excludedClaimIds.claimId -> claims.id
claim.ownerSourceId / seam.ownerSource               -> sources.id
claim.dependencyClaimIds / seam.dependencyClaimIds    -> claims.id
trial.claimId / seam.claimId                          -> claims.id
trial.manifestId / phaseReceipt.manifestId            -> manifests.id
trial.discriminatorIds / seam.discriminatorIds         -> discriminators.id
trial.seamId                                           -> seams.id or null
trial.receiptId / seam.receiptId                       -> phaseReceipts.id
seam.priorSeamIds                                      -> seams.id
seam.sourceIds                                         -> sources.id
seam.regressionFixtureIds                              -> fixtures.id
antibody.seamId                                        -> seams.id
antibody.positiveFixtureIds                            -> fixtures.id
antibody.negativeFixtureIds                            -> fixtures.id
antibody.quotationFixtureIds                           -> fixtures.id
antibody.historicalFixtureIds                          -> fixtures.id
fixture.antibodyIds                                    -> antibodies.id
fixture.seamIds                                        -> seams.id
propagation.seamId                                     -> seams.id
propagation.receiptId                                  -> phaseReceipts.id
propagation.derivativeSourceId                         -> sources.id
phaseReceipt.claimIds                                  -> claims.id
phaseReceipt.trialIds                                  -> trials.id
phaseReceipt.seamIds                                   -> seams.id
phaseReceipt.propagationIds                            -> propagations.id
phaseReceipt.dependsOnReceiptIds                       -> phaseReceipts.id
```

Every reference target must exist, reference arrays contain no duplicates, and
no undeclared entailment cycle is allowed among `claim.dependencyClaimIds`.
A source with `authorityRole=PROVENANCE` may be cited only as historical input:
it cannot be a `claim.ownerSourceId`, cannot share its path with any
`phaseReceipt.path`, cannot satisfy `dependsOnReceiptIds`, and cannot by itself
upgrade evidence strength. It also cannot appear in
`claim.dependencyClaimIds`; `SRC-PROV-109-PROOF-AUDIT` is constrained by every
one of these rules. Phase A contains exactly one `phaseReceipt` record,
`REC-A-108`, even though the audit lane contains two filenames beginning with
the number 108. Phase B contains exactly one `phaseReceipt` record,
`REC-B-109`, at
`11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md`,
even though the audit lane contains the frozen pre-program 109 filename too.
Bare human numbers 108 and 109 are not identifiers and carry no authority;
phase-receipt references require the typed ID and exact path.

`COMPLETE` means the producing pass claims all declared artifacts exist and both
review attestations pass against one frozen semantic package. `VERIFIED`
additionally requires matching hashes, complete manifest coverage, passing
validation, and the immutable validation bundle.

Before review, the renderer canonicalizes a `reviewTarget` containing a semantic
projection of the phase manifest; the phase's source/claim/trial/propagation/
antibody/discriminator/fixture records; a semantic projection of each seam; the
raw schema hash; `ledgerSemanticSections`; and `semanticDiffPaths` from
`baseCommit` to the candidate tree. `manifest.closureOnlyPaths` explicitly names
the review-target output, validation bundle, and both independent review files.
It is a subset of `allowedChangePaths`. The manifest projection retains the
complete scope law but removes hash records for those closure-only paths from
`candidateFiles`, `includedFiles`, and `finalFiles`. `semanticDiffPaths` is the
changed-path set minus `closureOnlyPaths`; the review-target output path is passed
to the renderer and must itself be one of those declared closure-only paths.
This makes render-then-recompute, post-review, and post-bundle targets byte-stable
without hiding an owner or semantic artifact.

The seam projection contains every seam field except mechanical closure: a
`VERIFIED` status is normalized back to `REPAIRED`, and each Beauty/Truth/Justice
gate is projected to its `rationale` only, omitting `status` and `reviewerPath`.
`RETRACTED` remains `RETRACTED` because retraction is a semantic disposition.
For every seam named by the receipt, the renderer parses exactly one fenced
`json kintsugi-seam` record from its raw ledger section and emits:

```text
ledgerSemanticSection = {
  id: ID,
  narrativeRawSha256: RAW_HASH,
  seamProjection: review_seam_projection(parsed fenced seam)
}
```

`narrativeRawSha256` hashes the exact raw bytes before and after that one fence,
concatenated in source order; changing prose, headings, spacing, or line endings
therefore changes the target. The parsed fence must deep-equal the corresponding
core seam before projection. Changing only seam status/gate closure fields in
both representations leaves the target stable; changing `afterQuote`, any other
semantic seam field, or ledger narrative changes it. Raw whole-section hashes
are deliberately absent from the review target and remain in the final
validation bundle only.

The target excludes receipt status/digest fields and closure-only file bytes.
`reviewTargetDigest` is the raw SHA-256 of the canonical target bytes. Both
reviewers receive those bytes and cite that digest. After review begins, only
review files; `REPAIRED -> VERIFIED`; gate `PENDING -> PASS|FAIL` plus
`reviewerPath`; the phase receipt's mechanical closure fields; its synchronized
receipt fence; final hashes for closure-only files; and the new validation bundle
may change. These permitted closure mutations must reproduce the same
review-target bytes. Any other owner, claim, seam, manifest-final, or ledger
change invalidates the target and requires both reviews to restart.

At the `COMPLETE -> VERIFIED` transition, the runner emits one immutable
canonical JSON file at `phaseReceipt.validationBundlePath` and sets
`validationDigest` to the raw-byte SHA-256 of that exact file. The receipt file
itself and its digest field are excluded from the bundle to avoid recursion.
The renderer constructs a prospective final `receiptDescriptor`: it copies the
COMPLETE receipt, sets `status=VERIFIED` and `validationBundlePath` to the exact
requested output, and removes `validationDigest`. After the bundle is written,
the only permitted receipt mutation is to match that descriptor and add the
computed digest. Final validation deep-compares the live receipt with the
descriptor after removing `validationDigest`.
The exact bundle is:

```text
validationBundle = {
  schemaVersion: "1.0.0",
  phase: phaseReceipt.phase,
  receiptDescriptor: phaseReceipt with validationDigest removed,
  reviewTargetDigest: phaseReceipt.reviewTargetDigest,
  manifest: the exact referenced manifest object,
  sources: all source records transitively referenced by the phase,
  claims: records named by phaseReceipt.claimIds plus their dependencies,
  trials: records named by phaseReceipt.trialIds,
  seams: records named by phaseReceipt.seamIds plus prior seams,
  propagations: records named by phaseReceipt.propagationIds,
  antibodies: records attached to those seams,
  discriminators: records referenced by those trials/seams,
  fixtures: records referenced by those seams/antibodies,
  schemaSha256: raw hash of 02_KINTSUGI_SCHEMA.json,
  ledgerSections: [
    {id, sectionRawSha256} for each phaseReceipt.seamIds entry
  ],
  logicReviewSha256: raw hash of logicReviewPath,
  btjReviewSha256: raw hash of btjReviewPath,
  publicQueueSha256: raw Phase C queue hash, null for A/B,
  dependencyReceipts: [
    {id, validationDigest} for each dependsOnReceiptIds entry
  ]
}
```

Each `ledgerSections` hash covers the raw UTF-8 bytes from that seam's
`## KIN-...` heading through the byte before the next seam heading (or EOF), so
later phases may append new sections without altering a verified earlier
bundle. Every record array and ledger-section list is sorted lexicographically
by `id`; dependency receipts are sorted by `id`; file/path arrays inside the
manifest are sorted by `path`; all other arrays preserve their schema-declared
semantic order or, when declared sets, are sorted lexicographically. The bundle
is serialized by the canonical JSON algorithm in §14 and written once. Later
phases reference its digest and may not regenerate or modify it.

Manifest coverage is intentionally bounded rather than metaphysically
exhaustive. At phase start, the discovery rules and human-reviewed claim
inventory are frozen. Completion requires:

```text
C = set(candidateFiles.path)
I = set(includedFiles.path)
F = set(finalFiles.path)
E = set(excludedPaths.path)
C = I disjoint-union E
candidateFileCount = len(C)
eligibleFileCount = scannedFileCount = len(I)
if receipt.status = DRAFT: F = empty and finalFileCount = 0
if receipt.status in {COMPLETE, VERIFIED}: F = I and finalFileCount = len(F)

H = set(harvestedClaimIds)
T = set(trialedClaimIds)
X = set(excludedClaimIds.claimId)
H = T disjoint-union X
eligibleClaimCount = len(H)
trialedClaimCount = len(T)
T = set(trial.claimId where trial.manifestId = this manifest.id)
set(closureOnlyPaths) subset-of set(allowedChangePaths)
```

Candidate, included, excluded, harvested, trialed, and excluded-claim paths/IDs
are individually unique. Every exclusion has a reason. Candidate and included
hashes are immutable input hashes and must match the corresponding blobs at
`baseCommit`; they are not expected to match a repaired worktree. At completion,
every `finalFiles` hash must match the current verified worktree, and every
modified included owner must have a closed trial plus a seam or an explicitly
recorded no-change disposition. `inventoryReviewPaths` names the read-only
reviews of the frozen inventory. The receipt therefore proves complete coverage
of its declared manifest and before/after states, not the impossible claim that
no unrecognized proposition exists anywhere in prose.

`protectedProvenance` freezes receipts 104–107, the staged predecessor receipt
108, and the pre-program proof audit 109 as `FULL_FILE` records. The exact 108
and 109 records use the raw hashes in §2.1. The proof audit remains
`SRC-PROV-109-PROOF-AUDIT`; it cannot become a phase receipt, claim owner,
dependency, or authority. `protectedProvenance` also
freezes the exact countersign-history spans retained inside any editable owner
as `EXACT_SPAN`; the span text is included and its raw UTF-8 byte SHA-256 must
still match. This preserves historical provenance without granting it logical
authority. `protectedPaths` always includes `12_PUBLIC_SITE`, every
`90_ARCHIVE` subtree, and `91_COMPATIBILITY`.

Protected-tree validation does not depend on Git ignore rules. At phase start,
the runner recursively enumerates every regular file and symbolic link below
each protected path using `os.scandir`, including tracked, untracked, and
ignored entries. Regular files are raw-byte hashed; symlinks hash the UTF-8
bytes of `os.readlink(path)`. Special files fail the snapshot. Empty directories
are not semantic content. The sorted records form two independent baselines:
`protectedTreeSnapshots.isolated` and `protectedTreeSnapshots.canonical`.
Completion compares each checkout only with its own baseline and requires exact
path, kind, and raw-hash equality.

The Git checks are additional scope guards:

```text
git diff --name-only <baseCommit> -- <protected paths>          -> empty
C_root = set(git diff --name-only <baseCommit>..HEAD -- all paths)
S_root = set(git status --porcelain=v1 -z --untracked-files=all paths)
P_root = set(manifest.allowedPreexistingUntracked[root].path)
((C_root union S_root) - P_root)
  subset-of set(manifest.allowedChangePaths)
```

`C_root` closes the committed-scope hole: committing an off-scope path cannot
make it disappear from validation. `S_root` covers staged, unstaged, and
untracked state. Both are parsed without line splitting; NUL-delimited status
records are mandatory.

The pre-existing `12_PUBLIC_SITE/docs/superpowers/` item in the canonical
checkout is expanded into one
`allowedPreexistingUntracked.canonical` record per file and must remain
byte-identical. The isolated list is frozen independently and is empty at the
design baseline. A path may be subtracted through `P_root` only when its current
kind and raw hash exactly match its frozen record; a missing or changed baseline
entry fails rather than becoming an allowed phase change. No new untracked
protected-path item is allowed in either root. Final verification checks each
checkout against its root-specific snapshot and allowance.

Every seam record contains:

```text
id: ID
claimId: ID
ownerSource: ID
ownerAnchor: TEXT
beforeQuote: TEXT
beforeHash: TEXT_HASH
priorSeamIds: LIST[ID]
claimType: CLAIM_TYPE
typedTerms: LIST[typedTerm]
premises: LIST[premise]
conclusion: TEXT
inference: inference
quantifiers: LIST[quantifier]
modality: MODALITY
scope: scope
justiceScope: JUSTICE_SCOPE
justiceContext: justiceContext when triggered
evidenceBefore: evidence
sourceIds: LIST[ID]
dependencyClaimIds: LIST[ID]
countermodel: countermodel
defectClass: DEFECT_CLASS
severity: SEVERITY
validityVerdict: VALIDITY_VERDICT
soundnessVerdict: SOUNDNESS_VERDICT
verdict: OVERALL_VERDICT
repairKind: REPAIR_KIND when repaired/retracted/verified
afterQuote: TEXT when repaired/retracted/verified
survivingKernel: TEXT
evidenceAfter: evidence when repaired/retracted/verified
upgradeCriterion: TEXT
killCriterion: TEXT
beautyGate: gate
truthGate: gate
justiceGate: gate
credit: credit
creditConsent: NAMED | ALIAS | ANONYMOUS
receiptId: ID
regressionFixtureIds: LIST[ID]
discriminatorIds: LIST[ID]
containment: containment only when held open
residualRisk: residualRisk only when held open
status: CONFIRMED | REPAIRED | HELD_OPEN | RETRACTED | VERIFIED
```

For `REPAIRED`, `RETRACTED`, and `VERIFIED`, `repairKind`, `afterQuote`, and
`evidenceAfter` are required. For `CONFIRMED`, those fields
and the containment fields are absent. For `HELD_OPEN`, repair fields are
absent and `containment`, `residualRisk`, and at least one `discriminatorId` are
required. `priorSeamIds` is always present and may be empty only for the first
trial of a claim. No clean no-change trial appears in `seams`.

`claim.evidence`, `evidenceBefore`, and `evidenceAfter` are objects rather than
single labels:

```text
strength ∈ {A, S, I, C}
sourced ∈ {true, false}          # the orthogonal [B] provenance axis
lifecycle ∈ {DRAFT, ACTIVE, RETIRED}  # the orthogonal [D] status axis
```

This prevents provenance or lifecycle state from masquerading as epistemic
strength. `creditConsent` is `NAMED`, `ALIAS`, or `ANONYMOUS`; a real name is
valid only with `NAMED` consent.

Every field shown in a record interface is required unless this specification
declares it conditional. Arrays may be empty only where the relationship is
genuinely absent. The declared nullable fields are:

- `trial.breakState=NONE` requires `defectClass`, `severity`, and `seamId` to be
  `null`; `ALLEGED` requires defect and severity but keeps `seamId=null` and
  status `TRIED` or `DISPUTED`; `CONFIRMED` requires all three non-null and
  status `ADJUDICATED` or `CLOSED`;
- `antibody.matchMode=SEMANTIC_FIXTURE` requires a non-null closed-registry
  `semanticEvaluator`; `LITERAL` and `REGEX` require it to be `null`;
- `phaseReceipt.reviewTargetDigest`, `validationBundlePath`, `validationDigest`,
  `logicReviewPath`, and `btjReviewPath` are `null` while the receipt is
  `DRAFT`; review target and review paths are non-empty at `COMPLETE`, while
  bundle path and digest remain `null`; all five are non-empty at `VERIFIED`
  after the immutable bundle is emitted once;
- `seam.repairKind`, `afterQuote`, and `evidenceAfter` are absent only for
  `CONFIRMED` and `HELD_OPEN`; and
- `seam.containment` and `residualRisk` are present only for `HELD_OPEN`; and
- `justiceContext` is present only for the three Justice-triggering
  `justiceScope` values declared below.

No other field accepts `null`. Status-dependent absence is validated before
rendering or owner-source comparison.

All three seam gates are `PENDING` with `reviewerPath=null` before independent
review while a seam is `CONFIRMED`, `REPAIRED`, `HELD_OPEN`, or a proposed
`RETRACTED` disposition. After review, phase completion requires `RETRACTED` and
`VERIFIED` seams to carry three `PASS` gates with non-null reviewer paths. A
`FAIL` gate blocks completion; it never silently becomes `PENDING`.

For claims and seams whose `justiceScope` is `COLLECTIVE`, `NORMATIVE`, or
`COLLECTIVE_NORMATIVE`, the typed `justiceContext` object defined above is
required.

For `justiceScope=NONE` or `INDIVIDUAL`, `justiceContext` is absent. The schema
uses this trigger for deterministic conditional validation.

All IDs are unique and stable. Files and receipts must exist. `beforeHash`
preserves the tried text even after its owner changes. `afterQuote` must match
the verified owner source exactly once. Free-form fields may explain a verdict
but cannot replace required typed fields.

The Markdown ledger is the human semantic authority for repairs. Each seam
section has this exact grammar:

````text
## KIN-0001 — concise title

Human explanation of the crack, surviving kernel, and repair.

```json kintsugi-seam
{ complete seam record }
```
````

The validator extracts every `json kintsugi-seam` fence with the standard
library JSON parser. The embedded record must deep-equal the record with the
same ID in `02_KINTSUGI_SEAMS.json`. Owner files remain authoritative for the
claim text; `beforeQuote`/`beforeHash` freeze the tried version and
`afterQuote` must match the repaired owner. Other JSON collections are control
metadata and may not introduce a proposition absent from an owner source or
seam-ledger trial.

Each phase receipt Markdown file contains exactly one fenced record that
deep-equals its machine record:

````text
```json kintsugi-receipt
{ complete phaseReceipt record }
```
````

Each independent review Markdown file contains exactly one attestation:

```text
reviewAttestation = {
  id: ID,
  kind: LOGIC | BTJ,
  path: PATH,
  receiptId: ID,
  reviewerId: TEXT,
  reviewerRole: TEXT,
  independenceStatement: TEXT,
  reviewTargetDigest: RAW_HASH,
  verdict: PASS | FAIL,
  findingIds: LIST[ID],
  openSevereFindingIds: LIST[ID],
  approvedUpgradeSeamIds: LIST[ID],
  approvedGateSeamIds: LIST[ID]
}
```

The attestation is fenced as `json kintsugi-review`. The two review paths,
review IDs, and reviewer IDs must be distinct; both target the same
`reviewTargetDigest`. `PASS` requires an empty `openSevereFindingIds` list. The
LOGIC review alone may list `approvedUpgradeSeamIds`; the BTJ review alone may
list `approvedGateSeamIds`. Receipt and review fences are parsed and compared
before bundle validation.

Independent review means two read-only reviewers receive the same immutable
diff and seam package: one reviews formal validity, types, modality, and tier;
the other reviews Beauty, Justice, consequence boundaries, and propagation.
Neither reviewer may author or edit the repair being reviewed.

The machine verifies the structure of these attestations, distinct identities,
target digest, declared verdicts, and absence of open severe findings. It does
not claim to infer intellectual independence, substantive truth, Beauty, or
Justice. Those remain accountable human/reviewer judgments. Likewise, an
evidence upgrade is structurally admissible only when the seam's ID appears in
the LOGIC attestation and cited evidence records exist; the validator does not
pretend to decide whether the evidence is scientifically persuasive.

## 8. Beauty, Truth, and Justice gates

### Beauty — coherent form

A repair passes Beauty when:

- one owner carries the full semantic statement;
- terminology and register indices are consistent;
- the seam is visible but proportionate;
- derivative prose can cite the owner without restating the whole trial;
- the proof/dependency graph has no decorative edge; and
- subtraction is preferred when added structure is unnecessary.

Beauty fails when a repair merely makes a contradiction harder to see.

### Truth — warranted inference

A repair passes Truth when:

- the exact proposition is atomized;
- every term and operator is typed;
- premises, quantifiers, scope, and modality are explicit;
- validity and premise soundness receive separate verdicts;
- at least one serious countermodel or discriminator is recorded;
- evidence tiers cannot increase through analogy, repetition, authority, or
  compression; and
- the surviving kernel, upgrade criterion, and kill criterion are stated.

Truth permits `HELD_OPEN` and `RETRACTED`. It forbids forced coherence.

### Justice — consequence and agency

A repair passes Justice when:

- it identifies who benefits and who bears the cost;
- attribution uses a real name only with consent, otherwise an approved alias;
- custody of data and receipts is explicit;
- correction is reversible unless the irreversibility is named and justified;
- affected people retain meaningful exit;
- individual and whole are both represented;
- `eta`, extraction risk, and option-cone contraction are visible; and
- no critic is declared an “unpaid quality engineer” without consent and an
  honest account of compensation.

Justice fails if prestige, elegance, or corpus survival is purchased through
hidden labor or reduced agency.

## 9. Antifragility without a gameable score

The staged protocol's scalar sum is replaced by two vectors:

```text
risk = (
  open severe cracks,
  unmarked active derivative drifts,
  unreceipted repairs
)

gain = (
  adversarially tested claims,
  regression fixtures,
  runnable discriminators
)
```

A confirmed-break cycle passes the antifragility test when `risk` decreases
lexicographically by severity and `gain` does not decrease. `HELD_OPEN` is an
honest trial disposition but not an antifragility pass for a severe crack. A
clean stress test creates a trial record and may produce a valid no-change
phase receipt without creating a seam. The protocol must never manufacture a
crack, antibody, or experiment merely to increase a metric.

For every confirmed break:

1. the crack is repaired or retracted; if it is held open, its risk remains in
   the phase vector and a severe item blocks completion;
2. the same failure becomes mechanically detectable;
3. the receipt states what survived; and
4. no evidence, consent, custody, reversibility, exit, or authority boundary is
   weakened.

## 10. Repair cycle

The program reuses the Soul Loop rather than inventing another operator:

```text
Beauty intake
    -> Truth trial
    -> Justice repair
    -> Golden receipt
    -> regression return
    -> next model and selector
```

Operational order:

1. freeze the tried quote and owner revision;
2. check the Settled Canon Registry and prior receipts;
3. atomize and type the claim;
4. formalize premises, inference, conclusion, modality, and scope;
5. steelman it independently;
6. construct a countermodel or cheapest discriminator;
7. issue the verdict;
8. select the smallest lawful repair kind;
9. run BTJ gates;
10. edit the owner first;
11. add the seam, receipt, antibody, and regression fixture;
12. update active derivatives; and
13. rerun a delta trial to detect repair-induced fractures.

## 11. Phase A — kernel and recent changes

Phase A proves the protocol on itself before using it on the corpus.

### A0. Bootstrap order

The protocol cannot truthfully cite a completed receipt before the receipt
exists. Phase A therefore boots in this fixed order:

1. freeze manifest `MAN-A-001` at the phase base commit, including full-file
   hashes for receipts 104–107, the staged predecessor receipt 108, and the
   pre-program proof audit 109, exact countersign-history spans, protected
   trees, and separate isolated/canonical protected-tree and pre-existing
   untracked snapshots;
2. create the ledger/JSON skeleton and validator schema;
3. create `REC-A-108` with `status=DRAFT` and no completion claim;
4. run `--phase A --bootstrap`, which accepts only this explicitly incomplete
   state and checks paths, schemas, hashes, and status honesty;
5. self-trial and repair the Kintsugi Protocol, citing `REC-A-108` as `DRAFT`;
6. trial and repair the Phase A kernel;
7. complete both independent reviews and the full Phase A validation; and
8. change `REC-A-108` to `VERIFIED` only after its declared digest, manifest,
   trials, seams, and reviews all match.

`--bootstrap` is legal only for Phase A and can never satisfy a phase completion
gate.

### A1. Self-trial of Kintsugi

Repair `00_META/00_THE_KINTSUGI_PROTOCOL.md` so that it:

- cites the real `REC-A-108`;
- separates seam visibility from truth warrant;
- allows subtraction and clean retraction as gold;
- uses the risk/gain vectors above;
- permits a clean no-change receipt;
- defines credit consent and privacy;
- removes coercive “unpaid quality engineer” language;
- anchors every invoked audit method; and
- replaces pending-K2 lifecycle language with this program's evidence-governed
  acceptance states.

The protocol's own defects become its founding seam rather than disappearing.

### A2. Core trial set

The first bounded vessel is the countersigned 30-item Burri Rules ledger plus
claims changed since audit 103. Existing audit conclusions are inputs and
regression fixtures, not automatically rerun from scratch.

The initial high-confidence stress targets, each of which must be retried before
receiving a `CONFIRMED` state, are:

1. **Triadic uniqueness:** inversion closure does not uniquely derive
   `{0,1,infinity}` without selecting the positive-real component; a fourth
   point's cross-ratio is additional data rather than proof of redundancy.
2. **D6 area direction:** `Area({nu >= nu_0})` tends to `4pi`, not zero, as
   `nu_0 -> 0`; point coordinate and threshold were conflated.
3. **Power-Max circularity:** optimizing over a set already defined to exclude
   extraction proves admissibility by definition, not independent dominance or
   moral obligation.
4. **D4/D5 type ambiguity:** the mu and chi readings can coexist only when
   register membership is part of the type.
5. **Quantum type error:** a normalized scalar cannot be sampled, and
   normalization does not derive the quadratic Born measure.
6. **Physical/option-cone category error:** human symbolic reach may widen a
   modeled/reachable option cone inside `J+`; it does not widen the physical
   light cone beyond spacetime and `c`.

### A3. Required owner repairs

`MAN-A-001.allowedChangePaths` is the exhaustive union of the owner/support
paths in this section and the artifact/index paths in A4. Phase A rejects every
other tracked or untracked diff path. The owner/support paths are exactly:

- `00_META/00_THE_KINTSUGI_PROTOCOL.md`;
- `01_TELEOLOGY/02_THE_DERIVATION/07A_F5_UNBUNDLED_COUPLING_PER_DIMENSION_PENDING_K2.md`;
- `05_COSMOLOGY/00_THE_BURRI_RULES.md`;
- `05_COSMOLOGY/00_THE_BURRI_RULES_LEDGER.md`;
- `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/36_THE_DIMENSIONAL_TROPHIC_CASCADE.md`;
- `05_COSMOLOGY/03_FORMAL_SYSTEM/00_THE_SEVEN_AXIOMS.md`;
- `05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md`;
- `05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md`;
- `05_COSMOLOGY/03_FORMAL_SYSTEM/11_EFR_TRIADIC_STABILITY.md`;
- `05_COSMOLOGY/03_FORMAL_SYSTEM/21_TRIADIC_STABILITY_CORRESPONDENCE.md`;
- `05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md`;
- `05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md`; and
- `08_FRAMEWORK_SUPPORT/00_META/02_ANALYSIS_DOCUMENTS/00_KINTSUGI.md` through a
  reconciliation banner rather than historical erasure;
- `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/PD_22A_QM_GR_DIMENSIONAL_ORDERING_TENSION_PENDING_K2.md`.

Receipts 105–107, the staged predecessor receipt 108, and the pre-program proof
audit 109 are immutable historical inputs, never trial authorities, claim
owners, dependencies, or eligibility gates. The proof audit's `PENDING_K2`
lifecycle adds no K2 gate. Synchronizing the receipts'
provenance into the Burri ledger is the first ledger repair target; no receipt
can determine the validity of a new conclusion. Existing countersign history
remains visible, but corrected claims do not inherit truth from the signature.

### A4. Phase A artifacts

- Modify: `docs/superpowers/specs/2026-07-11-kintsugi-formal-logic-design.md`
  only for the approved concurrency/implementability addendum; freeze it before
  `MAN-A-001`.
- Create: `docs/superpowers/plans/2026-07-12-kintsugi-a0-foundations-implementation.md`;
  execute it first. Reserve
  `docs/superpowers/plans/2026-07-12-kintsugi-a0b-machine-kernel-implementation.md`,
  `docs/superpowers/plans/2026-07-12-kintsugi-a1-owner-repairs-implementation.md`,
  and
  `docs/superpowers/plans/2026-07-12-kintsugi-a2-review-closure-implementation.md`.
  Their contents are written one after the other from the preceding verified
  artifacts; `MAN-A-001` may allow these exact paths but may not invent their
  contents or hashes before they exist.

- Modify: `00_META/00_THE_KINTSUGI_PROTOCOL.md`
- Create: `03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md`
- Create: `03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json`
- Create: `03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json`
- Create: `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md`
- Create: `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108A_FORMAL_LOGIC_REVIEW_2026_07_11.md`
- Create: `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108B_BTJ_REVIEW_2026_07_11.md`
- Create: `09_TOOLS/02_COMPILERS/validate_kintsugi.py`
- Create: `09_TOOLS/02_COMPILERS/test_validate_kintsugi.py`
- Create: `09_TOOLS/02_COMPILERS/render_kintsugi.py`
- Create: `09_TOOLS/02_COMPILERS/test_render_kintsugi.py`
- Create: `09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json`
- Create: `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_A_review_target.json`
- Create: `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_A_validation_bundle.json`
- Modify: `03_METHODOLOGY/01_THE_DERIVATION/README.md`
- Modify: `09_TOOLS/02_COMPILERS/README.md`
- Modify: `11_UPLINK/50_AUDITS_AND_EXECUTIONS/README.md` with a two-row routing
  note distinguishing the frozen staged predecessor 108 from canonical
  `REC-A-108`.

The plan/spec amendments above are committed before rebasing and before
freezing `refs/codex/kintsugi-a0-start`; they are planning provenance, not part
of the A0 implementation diff. The A0 diff measured from that post-rebase ref
remains exactly the four compiler paths declared by the A0 plan.

`MAN-A-001.closureOnlyPaths` is exactly the two review paths plus
`09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_A_review_target.json` and
`09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_A_validation_bundle.json`. It is a
subset of `allowedChangePaths`. No owner, semantic ledger, schema, test,
protocol, or core-data path may be classified closure-only.

Phase A becomes eligible for evidence-governed verification when every severe
kernel crack is repaired or retracted; the validator and mutation suite pass;
independent logic and BTJ attestations both declare PASS against the same target;
a final delta trial introduces no new severe fracture; and `REC-A-108` is
`VERIFIED`. The machine checks the declarations and hashes, not their
substantive truth. A severe `HELD_OPEN` seam blocks this transition.

## 12. Phase B — active corpus

Phase B applies the verified Phase A vocabulary and antibodies to the active
corpus.

### Included surfaces

- `00_META/` active sources;
- `01_TELEOLOGY/` through `07_THEOLOGY/`;
- active owner material under `08_FRAMEWORK_SUPPORT/`;
- `09_TOOLS/` claim and audit machinery;
- `10_SEED/`; and
- active routing/compression under `11_UPLINK/00_CORE/`, reconciliation, and
  current programs/audits.

### Excluded surfaces

- `12_PUBLIC_SITE/`;
- every `90_ARCHIVE/` subtree;
- `91_COMPATIBILITY/`;
- historical session packets except as provenance; and
- unrelated product, runtime, venture, or entity repositories.

### Method

1. Require `REC-A-108` at its exact canonical Phase A receipt path to be
   `VERIFIED`; otherwise `--phase B` fails before
   corpus traversal.
2. Freeze manifest `MAN-B-001` with every included file hash, exclusion reason,
   discovery rule, harvested claim ID, and an `allowedChangePaths` set equal to
   the included active-file paths plus exactly these new review/receipt paths:
   `109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md`,
   `109A_FORMAL_LOGIC_REVIEW_2026_07_11.md`, and
   `109B_BTJ_REVIEW_2026_07_11.md`, all under
   `11_UPLINK/50_AUDITS_AND_EXECUTIONS/`, plus
   `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_B_review_target.json` and
   `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_B_validation_bundle.json`.
3. Reuse packet 103, audits 100–101, the Canonical Claim Matrix, Honest
   Position, Falsifiers Index, Theorem Upgrade Protocol, Settled Canon Registry,
   and Burri ledger.
4. Audit the delta since packet 103 first.
5. Harvest remaining active load-bearing claims by owner, not by keyword count.
6. Trial necessity, uniqueness, universality, normative, and cross-domain claims
   before descriptive local claims.
7. Repair owner sources before compression surfaces.
8. Add exact drift signatures as antibodies with positive, negative,
   quotation, and historical fixtures.
9. Run a complete active-corpus delta after propagation.
10. Create
    `11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md`
    with typed ID `REC-B-109`, and mark it `VERIFIED` only after manifest
    coverage and both reviews pass.
11. Update `11_UPLINK/50_AUDITS_AND_EXECUTIONS/README.md` with exactly two 109
    routing rows:

    | Exact filename | Typed ID | Route |
    |---|---|---|
    | `109_THE_PROOF_LAYER_AUDIT_FOUR_FALSE_LEMMAS_PENDING_K2.md` | `SRC-PROV-109-PROOF-AUDIT` | immutable pre-program `SUPPORT/PROVENANCE`; never a phase receipt, owner, dependency, authority, or K2 gate |
    | `109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md` | `REC-B-109` | canonical Phase B receipt |

    The route resolves only by exact filename plus typed ID. Bare `109` is
    ambiguous human numbering and has no authority.

No settled item is reopened merely because a legacy document uses reconciled
shorthand. It is reopened only when a new counterexample attacks the ruling's
actual premises or an active source triggers the registry's “Still flag if”
condition.

Phase B completes when every manifest-eligible file is scanned or has an
explicit exclusion reason, every harvested claim has a closed trial or a
non-severe held-open disposition, no severe crack remains held open, no
compression surface upgrades a lower-tier owner claim, the full active-corpus
validator passes twice without a new repair between runs, and `REC-B-109` at
the exact active-corpus receipt path is `VERIFIED`.

## 13. Phase C — frozen public phenotype

Phase C is read-only with respect to `12_PUBLIC_SITE/`.

Phase C requires `REC-A-108` and `REC-B-109` to be `VERIFIED`; otherwise `--phase C`
fails before reading the public tree. It freezes manifest `MAN-C-001`, including
every public HTML/Markdown/JSON claim-bearing file, its hash, the deterministic
claim-discovery rule, and every explicit exclusion. Its `allowedChangePaths`
contains exactly:

- `03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json`;
- `11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md`;
- `11_UPLINK/50_AUDITS_AND_EXECUTIONS/110A_FORMAL_LOGIC_REVIEW_2026_07_11.md`;
- `11_UPLINK/50_AUDITS_AND_EXECUTIONS/110B_BTJ_REVIEW_2026_07_11.md`; and
- `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_public_propagation_queue.json`; and
- `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_C_review_target.json`; and
- `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_C_validation_bundle.json`.

It compares every manifest-discovered public claim against the repaired owner
source and produces:

- `11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md`;
- `09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_public_propagation_queue.json`.

Each queue item records:

```text
route
publicFile
publicQuote
ownership
driftClass
currentEvidence
maximumPublicStrength
requiredAction
severity
verificationCommand
```

The queue item is a tagged union:

```text
ownership = OWNED:
  require ownerSourceId, claimId, seamIds
  forbid ownerSearchEvidence, candidateOwners

ownership = OWNERLESS:
  require ownerSearchEvidence, candidateOwners, disposition
  forbid ownerSourceId, claimId, seamIds
```

`candidateOwners` may be an empty array only when
`ownerSearchEvidence` records a complete manifest-bounded search.
For an owned `KEEP` or `CITE` item, `seamIds` may be empty; every other owned
action requires at least one seam ID explaining the divergence.
An owned `KEEP` item is the only clean queue disposition: it requires
`driftClass=null` and `severity=null`. Every non-`KEEP` action requires both
fields to be non-null. This prevents coverage from manufacturing a defect.

The Phase C JSON root and item types are:

```text
publicQueue = {
  schemaVersion: "1.0.0",
  manifestId: ID,
  receiptId: ID,
  items: LIST[publicQueueItem]
}

publicQueueItem common fields = {
  route: TEXT,
  publicFile: PATH,
  publicQuote: TEXT,
  ownership: OWNED | OWNERLESS,
  driftClass: DEFECT_CLASS | null,
  currentEvidence: evidence,
  maximumPublicStrength: A | S | I | C,
  requiredAction: KEEP | CITE | NARROW | RETIER | RETRACT | REGENERATE,
  severity: SEVERITY | null,
  verificationCommand: TEXT
}

OWNED adds {
  ownerSourceId: ID,
  claimId: ID,
  seamIds: LIST[ID]
}

OWNERLESS adds {
  ownerSearchEvidence: LIST[TEXT],
  candidateOwners: LIST[PATH],
  disposition: TEXT
}
```

The schema uses `oneOf` plus `additionalProperties:false` so fields from the
opposite ownership variant are rejected rather than ignored.

Queue references are closed against the core data:

- `publicQueue.manifestId` resolves to the unique Phase C manifest;
- `publicQueue.receiptId` resolves to the Phase C receipt whose path is the 110
  Markdown queue;
- every `publicFile` occurs in that manifest's `includedFiles`;
- an owned `ownerSourceId` resolves to a source with
  `authorityRole=SEMANTIC_OWNER`;
- its `claimId` resolves to a claim whose `ownerSourceId` is the same source;
  and
- every non-empty `seamIds` entry resolves to a seam for that same claim and
  owner source.

Ownerless items contain no invented core IDs; their search evidence and
candidate paths are bounded by the Phase C manifest.

The Markdown queue is a deterministic rendering of the canonical JSON queue
and embeds exactly one `json kintsugi-public-queue` fence that deep-equals it.
Hand-authored Markdown may add explanatory prose around the fence but cannot
alter, omit, or add queue items.

`requiredAction` is one of `KEEP`, `CITE`, `NARROW`, `RETIER`, `RETRACT`, or
`REGENERATE`. Phase C does not perform the action. Public propagation remains a
later, separately scoped migration/repair project.

Phase C completes when every manifest-discovered public load-bearing claim is
mapped to an owner or flagged as ownerless, eligible/scanned/excluded coverage
counts reconcile exactly, the queue validates deterministically, receipt 110 is
`VERIFIED`, and no file under `12_PUBLIC_SITE/` has changed.

## 14. Validator behavior

`validate_kintsugi.py` uses only the Python standard library. It never edits
files.

`render_kintsugi.py` is the separate deterministic producer. It also uses only
the standard library and exposes four explicit operations:

```text
freeze-manifest  # populate input candidate/included hashes at phase start, or finalFiles at closure
review-target    # emit the immutable semantic package reviewed by LOGIC and BTJ
bundle           # emit the validation bundle after both reviews pass
transition-core  # apply only the declared COMPLETE or VERIFIED mechanical fields
```

The renderer accepts one repository-relative `--output` path that must be in the
selected manifest's `allowedChangePaths`, refuses protected paths and root
escapes, writes canonical JSON through a same-directory temporary file plus
`os.replace`, and never edits owner prose. `bundle` refuses to overwrite any
existing output. `review-target` accepts an existing output only when the bytes
are identical and otherwise fails, so review closure can prove the target did
not move. `freeze-manifest --final` refuses an owner whose current input
hash differs from the frozen trial hash unless that owner has a closed trial and
recorded seam. Re-running any operation on unchanged inputs must produce the
same bytes; a byte difference is a test failure.

`transition-core --stage COMPLETE` reads the two deep-equal PASS review
attestations, checks their shared target digest, changes only reviewed
`REPAIRED -> VERIFIED` statuses, terminal gate status/reviewer paths, and the
receipt's target/review/status fields, then atomically replaces the canonical
core JSON at the explicit output. `transition-core --stage VERIFIED` requires
the immutable bundle, verifies its prospective receipt descriptor, and changes
only receipt status, bundle path, and bundle digest. It never edits owner prose,
ledger narrative, or Markdown fences; those human-readable surfaces are patched
separately and must deep-equal before the transition validates. Any other JSON
delta fails `KIN-E-STATE`.

### Commands

Run from the repository root:

```text
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check --phase A --bootstrap --base-ref 454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22 --canonical-root /Users/Yves/Documents/01_EMERGENTISM
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check --phase A --base-ref MANIFEST --canonical-root /Users/Yves/Documents/01_EMERGENTISM
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check --phase B --base-ref MANIFEST --canonical-root /Users/Yves/Documents/01_EMERGENTISM
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check --phase C --base-ref MANIFEST --canonical-root /Users/Yves/Documents/01_EMERGENTISM
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check-baseline --canonical-root /Users/Yves/Documents/01_EMERGENTISM
python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py'
python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_render_kintsugi.py'
python3 -B 09_TOOLS/02_COMPILERS/render_kintsugi.py freeze-manifest --phase A --base-ref 454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22 --canonical-root /Users/Yves/Documents/01_EMERGENTISM --output 03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json
python3 -B 09_TOOLS/02_COMPILERS/render_kintsugi.py review-target --phase A --output 09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_A_review_target.json
python3 -B 09_TOOLS/02_COMPILERS/render_kintsugi.py bundle --phase A --output 09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_A_validation_bundle.json
python3 -B 09_TOOLS/02_COMPILERS/render_kintsugi.py transition-core --phase A --stage COMPLETE --output 03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json
python3 -B 09_TOOLS/02_COMPILERS/render_kintsugi.py transition-core --phase A --stage VERIFIED --bundle 09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_phase_A_validation_bundle.json --output 03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json
```

The implementation discovers the repository root as
`Path(__file__).resolve().parents[2]`; the current working directory does not
change path resolution. Defaults are:

```text
--data         03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json
--schema       03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json
--ledger       03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md
--public-queue 09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_public_propagation_queue.json
--baseline-allowlist 09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json
```

Each default has an explicit same-named override flag accepting one
repository-relative path. Bare `--check` validates schema, hashes,
cross-references, Markdown synchronization, and every receipt already marked
`VERIFIED`, but does not claim any incomplete phase is complete. `--phase`
adds that phase's coverage and completion gates. `--base-ref` is mandatory with
`--phase` and supplies the Git comparison point for protected-path checks.
The literal value `MANIFEST` resolves to the selected phase manifest's exact
40-character `baseCommit`; an explicit 7–40 character hexadecimal Git object
name is also accepted and must resolve to the same commit or validation fails.
`--public-queue` is read only for Phase C or when explicitly supplied.
`--check-baseline` runs the exact repository test command and applies the
versioned failure rule below; it cannot be combined with `--phase` or
`--bootstrap`.

The renderer shares the validator's root discovery, safe-path resolver,
canonical JSON function, schema checks, and deterministic diagnostic format;
it does not duplicate or weaken those contracts.

`--canonical-root` is also mandatory with `--phase` and accepts one absolute
directory. The validator requires that directory to be the `main` worktree in
`git worktree list --porcelain`, share the same Git common directory as the
isolated root, and match the manifest's `canonicalBranch` and
`canonicalCommit`. It is the only root used for canonical-checkout untracked
and protected-provenance checks. Bare `--check` performs no external-worktree
check because it makes no phase-completion claim.

The full command enforces phase order: B requires verified `REC-A-108`; C
requires verified `REC-A-108` and `REC-B-109` at their exact canonical paths. A manifest whose input hashes no longer
match `baseCommit`, or whose final hashes no longer match the reviewed
worktree, is stale and fails until the affected claims are retried against a
newly frozen manifest.

At phase start, canonical `HEAD` must equal the manifest's `canonicalCommit`.
Any later canonical-HEAD movement is `KIN-E-CONCURRENT` before a rebase or owner
edit. Any candidate owner whose base blob, tried quote, or review-target final
hash changes outside the declared repair sequence stops that claim and requires
a new manifest/retrial. Concurrency is evidence to re-freeze, never permission
to auto-merge doctrine.

### Exit codes

Schema version `1.0.0` freezes this diagnostic-code registry:

```text
KIN-E-CLI          invocation/argument error
KIN-E-IO           missing or unreadable input
KIN-E-JSON         malformed JSON or fenced JSON
KIN-E-SCHEMA-KEYWORD unknown schema keyword or unresolved $ref
KIN-E-SCHEMA       instance/schema mismatch
KIN-E-PATH         unsafe, absolute, escaping, or unexpected path
KIN-E-CANONICAL    non-canonical JSON bytes or hash-domain mismatch
KIN-E-ID           duplicate or malformed stable ID
KIN-E-REF          missing, wrong-kind, or forbidden reference
KIN-E-CYCLE        undeclared claim dependency cycle
KIN-E-VERDICT      invalid validity/soundness/overall combination
KIN-E-STATE        invalid trial/seam/receipt/gate transition or fields
KIN-E-JUSTICE      missing or inconsistent Justice context
KIN-E-LEDGER       missing, duplicate, or non-equal Markdown fence
KIN-E-QUOTE        owner quote/hash mismatch
KIN-E-MANIFEST     partition, count, input-hash, or final-hash mismatch
KIN-E-SCOPE        committed/staged/unstaged/untracked path outside allowance
KIN-E-PROTECTED    protected-tree, provenance, or frozen-baseline drift
KIN-E-REVIEW       review identity, target, verdict, or gate mismatch
KIN-E-RECEIPT      receipt role, phase order, or status mismatch
KIN-E-BUNDLE       review-target/bundle digest or immutability failure
KIN-E-FIXTURE      antibody/evaluator/fixture mismatch
KIN-E-QUEUE        public queue union, ownership, or rendering mismatch
KIN-E-BASELINE     removed test, new failure, or signature drift
KIN-E-CONCURRENT   canonical HEAD or owner changed after manifest freeze
```

Adding or renaming a code requires a schema-version change. Each diagnostic has
one primary code; explanatory detail belongs in the message, not an invented
sub-code.

```text
0  validation passed
1  semantic/schema/path/fixture failure
2  invocation or unreadable-input failure
```

Diagnostics identify seam ID, JSON path, owner file, and the failed invariant.
Malformed input must produce a controlled diagnostic rather than an exception
trace. Output ordering is deterministic.

Canonical JSON bytes are UTF-8 encoding of:

```python
json.dumps(
    value,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
    allow_nan=False,
) + "\n"
```

The program keeps two deliberately different hash domains:

- **Raw-byte hashes** use SHA-256 over the file's exact bytes with no decoding or
  normalization and use the `sha256:` prefix. They apply to manifest file
  hashes, `source.sha256`, `FULL_FILE` provenance, the UTF-8 bytes of a stored
  `EXACT_SPAN`, protected tracked/untracked files, and canonical JSON bytes. A
  line-ending-only change therefore breaks protected provenance.
- **Semantic-text hashes** convert `CRLF` and bare `CR` to `LF`, perform no other
  whitespace or Unicode normalization, hash the resulting UTF-8 bytes, and use
  the `sha256-text-lf:` prefix. Only `beforeHash`, `triedHash`, and quote-matching
  fixtures use this domain.

Canonical JSON files must already equal their canonical bytes; the validator
reports drift but never rewrites them.

For exit code 1, stdout is empty and each sorted stderr line has this form:

```text
KIN-ERROR <json-path-or-file> <stable-code>: <message>
```

For exit code 2, the path slot is `CLI`. No failure output may contain
`Traceback`. A successful check prints one deterministic `KIN-OK` summary line
to stdout and nothing to stderr.

### Mandatory checks

- schema version and exact enums;
- unique manifest, source, claim, trial, seam, antibody, discriminator, fixture,
  propagation, and phase-receipt IDs;
- scalar/container type correctness;
- existing owner, source, receipt, and derivative paths;
- dependency endpoints and no undeclared entailment cycles;
- exact candidate/included/excluded, final-file, and
  harvested/trialed/excluded manifest partitions with counts derived from
  unique sets; input hashes match `baseCommit` and final hashes match the
  verified worktree;
- after byte-verifying and subtracting the selected root's frozen
  `allowedPreexistingUntracked` paths, every path in the union of
  `baseCommit..HEAD` committed changes plus staged/unstaged/untracked status is
  contained in the selected phase's exact `allowedChangePaths`;
- exact `afterQuote` match in the declared owner;
- status-aware required/nullable fields, including complete before/after,
  surviving-kernel, evidence, upgrade, and kill fields where applicable;
- no `strength: C/I -> S/A` promotion unless the declared upgrade criterion is
  satisfied by the cited evidence; Rosetta, repetition, `sourced=true`, and
  lifecycle changes can never supply that upgrade;
- provenance and lifecycle axes validated independently from strength;
- provenance-only receipts cannot own claims, satisfy phase dependencies,
  impersonate the canonical receipt path, or justify tier upgrades;
- collective/normative Justice fields;
- owner-first full seam and derivative compact references;
- no completed receipt cited when the file is absent;
- deep-equal seam, receipt, review, and public-queue Markdown fences;
- distinct review identities, one review-target digest, declared PASS verdicts,
  closed severe findings, and gate/upgrade attestations;
- deterministic canonical JSON bytes and deterministic renderer output;
- byte-level protected-provenance checks for receipts 104–107, the staged
  predecessor receipt 108, the pre-program proof audit 109, and retained
  countersign-history spans; and
- tracked/untracked protected-path checks for public site, archive, and
  compatibility trees in both the isolated and canonical checkouts.

The validator must be total over malformed JSON shapes. The mutation matrix
changes one leaf or relationship at a time from an otherwise valid fixture:

```text
DELETE_REQUIRED_FIELD
ADD_UNKNOWN_FIELD
SCALAR_TO_ARRAY
SCALAR_TO_OBJECT
SCALAR_TO_NULL
INTEGER_TO_BOOLEAN
INVALID_ENUM
INVALID_ID
INVALID_PATH
INVALID_HASH
DANGLING_REFERENCE
DUPLICATE_ID
DEPENDENCY_CYCLE
STALE_OWNER_QUOTE
PHASE_ORDER_BYPASS
PROTECTED_PATH_CHANGE
COMMITTED_SCOPE_ESCAPE
PROVENANCE_AS_AUTHORITY
RECEIPT_FENCE_DRIFT
REVIEW_TARGET_DRIFT
BUNDLE_OVERWRITE
```

Each mutation must return exit code 1, emit at least one matching stable error
code on stderr, emit no stdout, and contain no traceback. CLI/read failures are
tested separately for exit code 2. Test enumeration comes from the normative
schema's `required`, `properties`, enums, patterns, and reference declarations,
so every declared required field and scalar leaf is exercised.

## 15. Regression fixture set

The first release includes positive, negative, quotation, and historical
fixtures for:

- chart identity presented as empirical conservation;
- zero-factor behavior presented as a unique product derivation;
- `is` presented as `ought` without a declared normative premise;
- taxonomy presented as mathematical necessity;
- D4/D5 cross-register substitution without a register index;
- absence of a reducing law presented as proof of strong emergence;
- normalization presented as derivation of the Born rule;
- sampling a scalar normalization constant;
- analogy presented as a physical mechanism;
- a wider option cone presented as a wider physical light cone;
- a staged or missing receipt presented as completed;
- a visible seam presented as automatic evidence upgrade;
- a historical quotation falsely flagged as a live assertion; and
- collective benefit asserted without consent, custody, reversibility, exit,
  or cost-bearer disclosure.

## 16. Verification contract

### Baseline regression allowlist

The exact repository-suite command, run from the repository root, is:

```text
python3 -m pytest -q --tb=short
```

The exact identity-collection command is separate and mandatory:

```text
python3 -m pytest --collect-only -q
```

The execution command proves pass/fail behavior; the collection command proves
that every frozen baseline node still exists. The baseline adapter runs and
parses both.

`kintsugi_baseline_failures.json` is fixed at schema version `1.0.0` and the
post-approval execution base commit
`454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22`. Its canonical raw-byte hash is
`sha256:92bc13d84b0cee317f648af6b1589f507e23a227afb40da2d66fb94282017957`.
Its normative initial content is:

```json
{
  "schemaVersion": "1.0.0",
  "baseCommit": "454f3719b6adf1d6d5a73ae3bb9eab6a34e45c22",
  "command": ["python3", "-m", "pytest", "-q", "--tb=short"],
  "collectCommand": ["python3", "-m", "pytest", "--collect-only", "-q"],
  "collectedAtBaseline": 19,
  "baselineNodeIds": [
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_constrained_kernel_preserves_lower_law_support",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_default_run_has_perturbable_positive_costed_witness",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_freeze_manifest_export_is_deterministic_json",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_freeze_manifest_records_hashes_and_frozen_objects",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_negative_controls_reject_false_macro_constraint_witnesses",
    "03_METHODOLOGY/03_PREREGISTRATIONS/physics_to_biology_harness/test_vesicle_macro_constraint.py::VesicleMacroConstraintTests::test_report_export_is_tier_honest_json",
    "09_TOOLS/01_SCRIPTS/test_cross_entity_receipt_traversal.py::test_traversal",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_passes_on_seeded_catalog",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_strict_passes_on_seeded_catalog",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_default_passes_with_only_warnings",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_strict_flags_unresolved_warnings",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_listings_have_titles",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_manifest_exists_and_links_resolve",
    "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_cross_entity_receipt_traversal_passes",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_parse_index",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_passes",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_fails_on_missing_file",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_fails_on_hash_mismatch",
    "09_TOOLS/01_SCRIPTS/test_mver_validator.py::test_validation_flags_unindexed_file"
  ],
  "allowedFailures": [
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_passes_on_seeded_catalog",
      "exceptionType": "AssertionError",
      "requiredSignature": "discipline check failed:"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_discipline_strict_passes_on_seeded_catalog",
      "exceptionType": "AssertionError",
      "requiredSignature": "assert 1 == 0"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_a7_default_passes_with_only_warnings",
      "exceptionType": "AssertionError",
      "requiredSignature": "assert 1 == 0"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_manifest_exists_and_links_resolve",
      "exceptionType": "AssertionError",
      "requiredSignature": "00_SKYZAI_COM_PRODUCT_MANIFEST.md"
    },
    {
      "nodeId": "09_TOOLS/01_SCRIPTS/test_marketplace_tools.py::test_cross_entity_receipt_traversal_passes",
      "exceptionType": "AssertionError",
      "requiredSignature": "09_K2_ROUTE_READINESS_RECEIPT.jsonld"
    }
  ]
}
```

An actual failing node must be in this allowlist and match both exception type
and required signature. The actual failure-ID set may be a strict subset if an
old failure starts passing, but every `baselineNodeIds` entry must remain in the
current collected-node set. Any removed/renamed baseline node, new failing ID,
or changed exception/signature fails the baseline check. Additional collected
tests are allowed only when they pass. Warnings do not enter the failure
allowlist but remain visible in the captured pytest output.

Every phase runs:

- validator unit and mutation tests;
- phase-specific semantic fixtures;
- source-negative scans for its antibodies;
- local Markdown-link validation;
- deterministic JSON comparison;
- `git diff --check`;
- protected-path diff checks;
- the repository baseline command checked against the versioned allowlist;
- independent formal-logic review;
- independent BTJ review; and
- a final diff review against the phase's starting commit.

The five pre-existing cross-pillar test failures remain documented. All other
baseline tests must not regress. If a Kintsugi change touches the failing test
surface, those failures become in-scope and must be resolved before completion.

## 17. Failure handling

- A disputed fracture remains a `DISPUTED` trial with no seam; it is not
  harmonized. `HELD_OPEN` is reserved for a confirmed break lacking a warranted
  repair.
- A repair that creates a larger unsupported claim is rejected.
- A repair that cannot preserve Justice is retracted or redesigned.
- A missing source or receipt blocks verification.
- An owner/derivative disagreement is repaired at the owner first.
- A validator crash is a validator defect; malformed input never counts as a
  corpus failure until the tool reports it cleanly.
- A clean stress test may close with a no-change receipt.
- Concurrent changes to an owner file stop that seam's edit until the new owner
  revision is retried.

## 18. Acceptance criteria

The complete A -> B -> C program is accepted when:

1. the Kintsugi Protocol has survived its own trial and carries its founding
   seam;
2. `REC-A-108` at `11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md` is `VERIFIED` and matches the seam ledger and Phase A manifest;
3. the six initial kernel fractures have verified dispositions;
4. the Burri ledger and active owner canon agree;
5. every severe fracture in the frozen active-corpus manifest is repaired or
   retracted with a receipt; no severe fracture is `HELD_OPEN`;
6. compression surfaces cannot silently upgrade owner claims;
7. every repair has a regression fixture;
8. BTJ Justice fields are complete for normative and collective claims;
9. `REC-B-109` at its exact canonical path is `VERIFIED` and two consecutive active-corpus validation
   passes produce no new repair;
10. receipt 110 is `VERIFIED` and the public propagation queue covers every
    claim discovered by the frozen public manifest;
11. `12_PUBLIC_SITE/`, archives, and compatibility surfaces remain unchanged;
12. independent logic and BTJ reviews report no unresolved severe finding; and
13. every A/B/C manifest reconciles eligible, scanned, and explicitly excluded
    counts, and all new files, links, JSON, tests, and diffs validate.

Acceptance is a receipt-backed state, not a sovereign declaration. Any later
counterexample may create a successor trial and seam without erasing the prior
repair history.

## 19. Why this is Kintsugi

Beauty is not smoothness. It is a vessel whose history can be read without
destroying its form.

Truth is not victory. It is the exact boundary between what follows, what is
stipulated, what is interpreted, and what remains conjectural.

Justice is not corpus preservation at any price. It is repair without hidden
extraction: the critic, author, reader, affected individual, and collective all
retain attribution, custody, reversibility, and exit.

The gold is therefore not added doctrine. The gold is the new inability to make
the same mistake invisibly.
