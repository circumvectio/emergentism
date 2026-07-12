# Kintsugi A0B Machine-Kernel Addendum

**Date:** 2026-07-12

**Status:** `[D]` controlling pre-v1 implementation boundary. No schema or live
core instance exists yet, so these corrections enter schema version `1.0.0`
rather than creating a compatibility-breaking second version.

**Parents:**

- `docs/superpowers/specs/2026-07-11-kintsugi-formal-logic-design.md`
- `docs/superpowers/specs/2026-07-12-kintsugi-a0-execution-lock-26e616e.md`
- `docs/superpowers/plans/2026-07-12-kintsugi-a0-foundations-implementation.md`

**Precedence:** where this addendum conflicts with its parents, this addendum
governs A0B, A1, and A2. Historical base observations remain historical; they
are not silently rewritten.

## 1. Why this addendum exists

A0 established a deterministic read-only foundation. A0B must now make the
formal grammar executable without fabricating a live claim graph or absorbing
concurrent owner edits. Five contradictions had to be resolved before schema
freeze:

1. the design's old `454f371...` baseline text conflicts with the immutable A0
   lock and live contract at `26e616e...`;
2. the bootstrap section assigns live manifest creation to Phase A generally,
   while the A0 handoff assigns `MAN-A-001` freeze and claim atomization to A1;
3. the schema requires non-empty live claims, trials, and a receipt, so a
   content-free A0B "skeleton" would invent semantics;
4. claim records lack prospective upgrade, kill, and surviving-kernel
   boundaries even though the Compass requires every load-bearing claim to be
   corrigible before it breaks; and
5. source repetition, Rosetta projection, provenance, signatures, and receipts
   need machine barriers preventing them from masquerading as proof.

## 2. Frozen A0 truth

The A0 implementation is complete at:

```text
branch                 codex/kintsugi-a0-26e616e
head                   181559a370598e1ae7572c33d21369ef6c6419e2
immutable baseline     26e616e651e2a87e8c85bf37db515d7fcd007b7b
contract raw sha256    74496df660f0ca989f293c30db652b8f9aeb78beb30fa91fe249d87ee29ef69b
canonical inventory    19 collected / 5 allowed failures
A0 focused tests       22 passing
```

Later `main` movement does not retarget that contract. It triggers the four
relevance checks in the immutable execution lock. A0B starts from A0 HEAD on
branch `codex/kintsugi-a0b-machine-kernel`.

## 3. Phase ownership: A0B versus A1 versus A2

### A0B owns the machine

A0B creates and verifies:

- the complete normative JSON Schema;
- a restricted standard-library schema evaluator;
- typed graph, state, evidence, Justice, and provenance checks;
- Markdown fence and owner-quote synchronization;
- Git, manifest, protected-tree, and concurrency machinery;
- the read-only validator orchestration;
- all four deterministic renderer operations;
- schema-derived and named mutation tests; and
- one complete synthetic integration vessel used only as a test fixture.

### A1 owns the first live vessel

A1, and only A1, creates the first live:

- `MAN-A-001`;
- `02_KINTSUGI_SEAMS.json`;
- `02_KINTSUGI_SEAM_LEDGER.md`;
- atomized Phase A source/claim/trial inventory; and
- DRAFT `REC-A-108`.

A1 freezes those objects together against a stable tracked base and an explicit
canonical-dirt inventory. Current dirty owner or protected-public work is never
silently absorbed.

### A2 owns closure

A2 invokes the already-tested review-target, transition, and immutable-bundle
machinery; obtains independent LOGIC and BTJ reviews; and may transition the
live Phase A receipt only through the declared state machine.

This preserves the runtime bootstrap order without forcing code-development
order to fabricate semantic data.

## 4. A0 compatibility surface

`validate_kintsugi.py` remains the public compatibility facade. A0B must
preserve its existing imports, `--check-baseline`, `--contract`,
`--canonical-root`, exit codes, diagnostic bytes, and exact canonical-root
baseline output. `--contract` remains a compatibility alias for
`--baseline-allowlist`.

The machine kernel may be factored into an internal `kintsugi_kernel/` package.
`validate_kintsugi.py` re-exports the A0 names so the 22 existing tests remain
unchanged. `render_kintsugi.py` is the only new executable permitted to write
generated artifacts. Lower layers return typed issues; they do not print,
exit, or mutate owner prose.

## 5. Schema organization

The schema still exposes exactly three selectable root roles:

```text
coreData
publicQueue
baselineAllowlist
```

The earlier phrase "exactly three `$defs`" is superseded. `$defs` may also
contain named nested record definitions so the schema does not duplicate
hundreds of lines or create divergent copies. Only the three root roles may be
selected by a CLI input role. Every object remains
`additionalProperties: false`, every `$ref` is local, and every declared
keyword is consumed by the restricted evaluator.

### 5.1 Golden Seam erratum: bounded string length

The canonical schema appendix uses `maxLength: 256` on the REGEX antibody
pattern so the schema enforces the pattern-length bound in Section 9.1. The
separate 1,024-state NFA ceiling remains a runtime/compiler check. The initial
Task 2 evaluator list accidentally omitted `maxLength`, which made the literal
schema and the fail-closed keyword registry jointly unsatisfiable. The
restricted vocabulary therefore includes `maxLength` with ordinary JSON Schema
string-length semantics. This is the sole vocabulary addition licensed by the
seam; unknown keywords continue to fail closed.

## 6. Pre-v1 claim contract additions

Every claim gains six fields:

```text
supportLinks: LIST[supportLink]              # may be empty
upgradeCriterion: upgradeCriterion
killCriterion: killCriterion
survivingIfKilled: survivingIfKilled
authorityScope: NONE | PRIVATE_DAV | PUBLIC_DAV | OTHER
authorityEffect:
  NONE | DESCRIPTIVE | DISCRETIONARY | CONSEQUENTIAL |
  CONSTITUTIONAL_AUTOMATIC
```

`typedTerm` becomes:

```text
typedTerm = {
  symbol: TEXT,
  type: TEXT,
  definition: TEXT,
  semanticRegister: REGISTER_ID
}

REGISTER_ID = non-empty string matching ^[A-Z][A-Z0-9_]*$
```

The register is syntax-controlled, not a closed enum: Phase B will encounter
domain-specific registers. A claim's typed terms are unique by
`(symbol, semanticRegister)`.

`premise` gains a required typed role:

```text
premise.role = DESCRIPTIVE | DEFINITIONAL | NORMATIVE | EVIDENTIARY
```

A normative claim (`claimType=NORMATIVE` or `modality=NORMATIVE`) requires at
least one `NORMATIVE` premise or a dependency claim whose modality is
`NORMATIVE` or whose `claimType` is `NORMATIVE`. Support links cannot satisfy
this rule.

### 6.1 Non-entailing support links

```text
supportLink = {
  id: ID,
  supportingClaimId: ID,
  mode: CORROBORATION | REPLICATION | ANALOGY | ROSETTA_TRANSFER,
  independenceStatus:
    INDEPENDENT | PARTIALLY_INDEPENDENT |
    NOT_INDEPENDENT | NOT_ASSESSED | NOT_APPLICABLE,
  evidenceCeiling: A | S | I | C,
  rationale: TEXT
}
```

Support links are deliberately claim-to-claim and non-entailing:

- `premises` are propositions consumed by the inference;
- `premise.sourceIds` cite evidence/provenance;
- `dependencyClaimIds` are entailing claim dependencies; and
- `supportLinks` record corroboration, replication, analogy, or Rosetta
  transfer without becoming premises.

A claim ID cannot occur in both `dependencyClaimIds` and `supportLinks`.
Self-links, duplicate link IDs, duplicate edges, and dangling links fail. The
union of dependency and support edges must be acyclic; checking the two graphs
separately is insufficient because a mixed two-edge cycle is still circular
support.

`ANALOGY` and `ROSETTA_TRANSFER` require
`independenceStatus=NOT_APPLICABLE` and `evidenceCeiling=I`. They cannot satisfy
an upgrade to `S` or `A`. Other modes forbid `NOT_APPLICABLE`. An `A` ceiling
requires an independently supported `[A]` supporting claim with
`evidence.sourced=true`. A link ceiling cannot exceed the supporting claim's
declared strength under `C < I < S < A`.

There is no score, vote, maximum, sum, or automatic tier aggregation across
links. Repetition, sourcing, lifecycle state, signatures, receipts, analogy,
and Rosetta transfer never upgrade a claim. Support links never change
modality or formal validity.

For upgrade comparisons only, independence has the strict order
`NOT_INDEPENDENT < PARTIALLY_INDEPENDENT < INDEPENDENT`. `NOT_ASSESSED` is
unordered and never qualifies. `NOT_APPLICABLE` is reserved for analogy or
Rosetta transfer and never qualifies.

### 6.2 Upgrade criterion and upgrade evidence

```text
upgradeCriterion =
  {
    kind: AVAILABLE,
    targetStrength: A | S | I,
    criterion: TEXT,
    requiredMode: CORROBORATION | REPLICATION,
    minimumIndependence: PARTIALLY_INDEPENDENT | INDEPENDENT,
    minimumEvidenceCeiling: A | S | I
  }
  |
  {
    kind: NONE,
    rationale: TEXT
  }
```

Allowed upgrades are strict:

```text
C -> I | S | A
I -> S | A
S -> A
A -> NONE
```

The criterion is prospective and therefore does not pretend that future
evidence already exists. When a seam actually raises evidence strength it must
add:

```text
upgradeEvidenceLinkIds: LIST[ID]              # non-empty on an upgrade
```

Every listed link resolves inside the repaired claim, uses the criterion's
required mode, meets or exceeds its minimum independence and ceiling, and is
included in the frozen review/bundle closure. `evidenceAfter.strength` must
equal `targetStrength` and be strictly stronger than `evidenceBefore.strength`.
Without these non-empty typed links, no upgrade is admissible.

`minimumEvidenceCeiling` must be at least `targetStrength`, and every listed
upgrade-evidence link must have `evidenceCeiling` at least `targetStrength`.
No upgrade may rise above its supporting evidence.

Any actual upgrade requires at least `PARTIALLY_INDEPENDENT` corroboration or
replication. `NOT_INDEPENDENT` and `NOT_ASSESSED` never satisfy an upgrade.
Target `A` additionally requires at least one `INDEPENDENT` link with ceiling
`A`, backed by an `[A]`, sourced supporting claim. Analogy and Rosetta transfer
never satisfy an upgrade at any target. The machine checks admissibility, not
scientific persuasiveness.

Every qualifying supporting claim has its own CLOSED trial with verdict
`VALID_SOUND` or `VALID_CONDITIONAL` and active evidence lifecycle, whether it
comes from the same manifest or a VERIFIED dependency bundle. Target `A`
requires `VALID_SOUND`. Receipt verification transports the claim/trial bytes;
it never substitutes for their warrant. Excluded, disputed, refuted, invalid,
retired, open, unsupported-premise, or unclosed claims cannot authorize an
upgrade.

For seams with no evidence upgrade, `upgradeEvidenceLinkIds` is absent. A
repetition count, signature, receipt, or lifecycle change cannot populate it.

`repairKind=RETIER` means a strict evidence-strength change in either direction,
but its warrants are asymmetric. An upward RETIER is admissible only through
the prospective-upgrade rules above; a downward RETIER is admissible only
through the prior kill criterion below. Equal-strength RETIER is invalid. No
other repair kind may change evidence strength. This pre-v1 clarification
supersedes the parent's narrower prose that described RETIER only as a
downgrade; it does not make upward movement automatic or score-based.

### 6.3 Kill criterion

```text
killCriterion =
  {
    kind: TESTABLE,
    testability: ACTIVE | DEFERRED,
    trigger: TEXT,
    method: TEXT,
    disposition: RETRACT | RETIER,
    resultingStrength: A | S | I | C,        # present only for RETIER
    deferredReason: TEXT,                    # present only for DEFERRED
    unblockCondition: TEXT                   # present only for DEFERRED
  }
  |
  {
    kind: NONE,
    rationale: TEXT
  }
```

`TESTABLE/RETRACT` forbids `resultingStrength`. `TESTABLE/RETIER` requires a
strict downgrade:

```text
A -> S | I | C
S -> I | C
I -> C
C -> RETRACT only
```

`ACTIVE` forbids `deferredReason` and `unblockCondition`. `DEFERRED` requires
both, so corrigibility cannot be satisfied by an indefinitely postponed free
text. `kind=NONE` is required exactly when the synchronized claim lifecycle is
`RETIRED`; DRAFT or ACTIVE load-bearing claims require `TESTABLE`.
Testing/adjudication status remains in `trial`, `discriminator`, and `seam`;
the kill criterion does not duplicate it.

### 6.4 Surviving kernel if killed

```text
survivingIfKilled = {
  claimIds: LIST[ID],                         # may be empty
  rationale: TEXT
}
```

The enclosing claim cannot cite itself. A survivor cannot transitively depend
on the killed claim. This field is prospective; the seam's `survivingKernel`
records what actually survived a confirmed fracture.

## 7. Seam synchronization

Every seam preserves the tried claim's prospective contract in
`priorSupportLinks`, `priorUpgradeCriterion`, `priorKillCriterion`, and
`priorSurvivingIfKilled`.

For `REPAIRED`, proposed `RETRACTED`, and `VERIFIED` seams, the unprefixed
`supportLinks`, typed `upgradeCriterion`, typed `killCriterion`, and
`survivingIfKilled` deep-equal the repaired current claim's next prospective
contract. For `CONFIRMED` and `HELD_OPEN`, prior and current fields remain
deep-equal because no repair exists. Upward RETIERs are judged against
`priorUpgradeCriterion`; downward RETIERs and retractions are judged against
`priorKillCriterion`. A retraction preserves evidence strength and changes the
claim lifecycle to `RETIRED`; it cannot smuggle an upgrade or downgrade. The
`beforeQuote`, `beforeHash`, the trial, and
`evidenceBefore` preserve the failed historical form. The previous free-text
seam `upgradeCriterion` and `killCriterion` fields are replaced before v1
freeze; dual text/object forms are forbidden.

Clean and disputed trials still produce no seam. A visible seam proves only
that a declared trial and repair record exist. It is never an automatic truth
warrant or evidence upgrade.

### 7.1 Review-target and bundle closure

The review target and validation bundle include the transitive closure of:

- receipt claim IDs and their `dependencyClaimIds`;
- every `supportLinks.supportingClaimId` reachable from those claims; and
- every `survivingIfKilled.claimIds` endpoint reachable from those claims; and
- every `targetClaimId` and non-null `bridgeClaimId` referenced by a Rosetta
  semantic fixture attached to those seams.

The union graph is cycle-checked before projection. A verified bundle may not
omit a claim needed to recheck a ceiling, independence status, mixed cycle, or
survivor validity. Referenced claims must belong to the selected manifest or a
verified dependency receipt whose validation bundle is included by digest.

## 8. Manifest omission barrier

Every manifest gains:

```text
requiredClaimBindings: LIST[requiredClaimBinding]  # unique by requirementId

requiredClaimBinding = {
  requirementId:
    REQ-A-PROTOCOL-SELF-TRIAL |
    REQ-A-TRIADIC-UNIQUENESS |
    REQ-A-D6-AREA-DIRECTION |
    REQ-A-POWER-MAX-CIRCULARITY |
    REQ-A-D4-D5-REGISTER |
    REQ-A-QUANTUM-MEASURE |
    REQ-A-OPTION-CONE,
  claimId: ID,
  ownerSourceId: ID,
  ownerAnchor: TEXT,
  targetHash: TEXT_HASH,
  rationale: TEXT
}
```

Rules:

- Phase A requires exactly one binding for each of the seven closed
  `requirementId` values above; Phase B and Phase C require an empty list;
- every bound `claimId` is in `harvestedClaimIds`, is disjoint from
  `excludedClaimIds`, and at `COMPLETE` or `VERIFIED` is in `trialedClaimIds`;
- `ownerSourceId` and `ownerAnchor` deep-equal the bound claim's owner fields;
- `targetHash` equals the frozen requirement fingerprint and the bound
  claim/trial's unique base quote hash;
  and
- no two requirement IDs bind the same claim.

A formally reconciled manifest therefore cannot omit the vessel it claims to
have tested.

The requirement labels are not instance-defined semantics. The kernel freezes
this expected owner fingerprint table:

| Requirement | Owner path | Owner anchor | Exact base quote hash |
|---|---|---|---|
| `REQ-A-PROTOCOL-SELF-TRIAL` | `00_META/00_THE_KINTSUGI_PROTOCOL.md` | `# The Kintsugi Protocol` | `sha256-text-lf:9fe68c734bce6c709c5879e0f7e40b552cdacb4cd14121302371509fb13f7cc9` |
| `REQ-A-TRIADIC-UNIQUENESS` | `05_COSMOLOGY/03_FORMAL_SYSTEM/11_EFR_TRIADIC_STABILITY.md` | `## The Uniqueness Theorem` | `sha256-text-lf:438269d12273e6c169e2ba8bdb8c126dcb118378a1d28a55328aa4dbdaec17b8` |
| `REQ-A-D6-AREA-DIRECTION` | `05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md` | `### 2.2 The Coordinate Collapse Theorem` | `sha256-text-lf:75893a2cd097580c3ee44a8a62f940e9b02d3dc09e4d73a5d3796e70de7d8e26` |
| `REQ-A-POWER-MAX-CIRCULARITY` | `05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md` | `## The Statement` | `sha256-text-lf:8cb12ae6fb3b855cbe999d699041ae3a15c73d3c405362195f6bf58441019510` |
| `REQ-A-D4-D5-REGISTER` | `05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md` | `## I. THE FUNDAMENTAL DISTINCTION` | `sha256-text-lf:dee381fece54b4fe926b1af1145ab8676263091cc698460a3b37962c77a6cca2` |
| `REQ-A-QUANTUM-MEASURE` | `05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md` | `## The Corrected Formula` | `sha256-text-lf:41b8437a8e8715a7be6f8f7ddef46984b89757d9f9722494b554dc3e87d204fb` |
| `REQ-A-OPTION-CONE` | `05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md` | `### Worldline and Light-Cone Corollary` | `sha256-text-lf:6749c86499b1e5d1a04de8afcbc6df283403617f1d0e40bdf9dbe66073412527` |

For each binding, the resolved `ownerSourceId.path`, exact `ownerAnchor`, and
unique tried/base quote hash must match this table. A manifest cannot relabel
seven unrelated claims beneath broad headings and satisfy the omission barrier.

## 9. Rosetta transfer firewall

Add `ROSETTA_TRANSFER` to the closed `antibody.semanticEvaluator` registry. It
is legal only with `matchMode=SEMANTIC_FIXTURE`, positive and negative
fixtures, and deterministic structural checks. Its JSON payload is exactly:

```text
rosettaTransferPayload = {
  targetClaimId: ID,
  bridgeClaimId: ID | null,
  fromRegister: REGISTER_ID,
  toRegister: REGISTER_ID,
  requestedTransfer:
    VOCABULARY | QUESTION | TOPOLOGY |
    ENTAILMENT | MECHANISM | NECESSITY | EVIDENCE_UPGRADE
}
```

`VOCABULARY`, `QUESTION`, and proposed `TOPOLOGY` return a correspondence-only
PASS and make no change to modality, validity, or evidence. `ENTAILMENT`,
`MECHANISM`, `NECESSITY`, and `EVIDENCE_UPGRADE` always fail as Rosetta
transfers. If a separately tested bridge claim exists, the relationship must be
reclassified and validated as a dependency or qualified support link; the
Rosetta edge itself still supplies no warrant. `bridgeClaimId`, when non-null,
must resolve, but its presence never changes this predicate.

Rosetta projection may transfer a question, vocabulary, or proposed topology.
It cannot transfer entailment, mechanism, causal law, independence, or evidence
tier. The evaluator is not an NLP truth classifier.

### 9.1 Closed antibody execution contract

Every declared antibody is executable; the registry is not inert metadata.
`LITERAL` and `REGEX` require `semanticEvaluator=null` and TEXT fixture payloads.
`LITERAL` uses exact Unicode substring membership. `REGEX` uses the bounded
`safeRegexSearch` language below, not Python's backtracking `re` engine. Source
bytes decode as strict UTF-8 with no Unicode or newline normalization; invalid
bytes fail `KIN-E-FIXTURE` at that path.

`safeRegexSearch` compiles a pattern of at most 256 Unicode code points into a
Thompson epsilon-NFA of at most 1,024 states and evaluates it in
`O(pattern_states * source_code_points)` time. Its complete grammar is:

```text
expression  := branch ("|" branch)*
branch      := piece*
piece       := atom quantifier?
atom        := literal | "." | character_class | "(" expression ")"
quantifier  := "?" | "*" | "+"
character_class := "[" "^"? class_item+ "]"
class_item  := class_literal | class_literal "-" class_literal
literal     := escaped_metachar | any code point outside .^$|?*+()[]\\
class_literal := escaped_metachar | any code point outside ]-\\
escaped_metachar := "\\" one-of .^$|?*+()[]-\\
```

Unescaped `^` is legal only as the first pattern token and unescaped `$` only
as the last; they anchor the whole decoded source, never individual lines. Dot
matches any Unicode code point except LF. Escapes quote only the literal
metacharacters `.`, `^`, `$`, `|`, `?`, `*`, `+`, `(`, `)`, `[`, `]`, `-`,
and `\\`; there are no backreferences, captures,
lookarounds, named groups, brace quantifiers, inline flags, shorthand classes,
or implementation-specific extensions. Class ranges compare Unicode scalar
values and must ascend. Empty branches/classes, dangling escapes, malformed
ranges, excess pattern/state size, or any other token fail `KIN-E-FIXTURE`.
The executor maintains state sets rather than paths, so nested forms such as
`(a+)+$` remain linear rather than catastrophically backtracking.

Antibody globs use a closed segment-aware grammar. A pattern is a safe
repository-relative POSIX path: no leading or trailing slash, backslash, empty,
`.` or `..` segment. `**` is legal only as an entire segment and matches zero
or more complete path segments. Inside any other segment, `*` matches zero or
more characters but never `/`; `?`, bracket classes, escapes, and every other
glob metacharacter are forbidden. Matching is anchored to the complete path.
Repository scans include a path only when at least one `scopeGlobs` entry and
no `excludeGlobs` entry matches. The evaluator returns the sorted resolved
include/exclude inventories so a broad exclusion is inspectable and hashable.

Fixture kind supplies explicit test context rather than inferred language
understanding: `POSITIVE` is a live assertion expected to trigger exactly its
`expectedAntibodyIds`; `NEGATIVE` is a live non-trigger; and `QUOTATION` and
`HISTORICAL` are declared non-live contexts that must not trigger a live-source
violation even when their text contains the protected pattern. Actual source
scans do not infer quotation or historical status; active scope and archive
exclusions must declare it. Every positive, negative, quotation, and historical
fixture named by an antibody is executed, and actual trigger IDs must deep-equal
the fixture's expected set.

A QUOTATION or HISTORICAL fixture pass tests fixture dispatch only. It never
warrants suppressing a matching span inside an active source: v1 has no NLP or
typed-span quotation classifier, so an in-scope source match remains visible for
review unless its whole path is explicitly and lawfully excluded.

`SEMANTIC_FIXTURE` requires `payloadKind=JSON`. Its payload parses as exactly the
named evaluator record below; the evaluator returns only a structural PASS or a
typed `KIN-E-FIXTURE` failure. It never upgrades evidence or decides empirical
truth. The seven non-Rosetta payloads are:

```text
verdictMatrixPayload = {
  validityVerdict: VALID | INVALID | NOT_APPLICABLE,
  soundnessVerdict:
    SUPPORTED | CONDITIONALLY_SUPPORTED | UNSUPPORTED |
    REFUTED | NOT_APPLICABLE,
  verdict:
    VALID_SOUND | VALID_CONDITIONAL | VALID_UNSUPPORTED_PREMISE |
    INVALID | UNDERDETERMINED | DEFINITIONAL | OPEN_CONJECTURE | REFUTED
}

justiceContextPayload = {
  claimType: CLAIM_TYPE,
  modality: MODALITY,
  justiceScope: JUSTICE_SCOPE,
  authorityScope: NONE | PRIVATE_DAV | PUBLIC_DAV | OTHER,
  authorityEffect:
    NONE | DESCRIPTIVE | DISCRETIONARY | CONSEQUENTIAL |
    CONSTITUTIONAL_AUTOMATIC,
  evidenceLifecycle: DRAFT | ACTIVE | RETIRED,
  justiceContext: justiceContext | null
}

receiptRolePayload = {
  recordKind: SOURCE_RECORD | PHASE_RECEIPT,
  sourceKind: OWNER | SUPPORT | COMPRESSION | PUBLIC | RECEIPT | null,
  authorityRole: SEMANTIC_OWNER | EVIDENCE | DERIVATIVE | PROVENANCE | null,
  receiptId: ID | null,
  phase: A | B | C | null,
  path: PATH,
  status: DRAFT | COMPLETE | VERIFIED | null,
  requestedUse:
    PROVENANCE | CLAIM_OWNER | PHASE_DEPENDENCY |
    EVIDENCE_UPGRADE | CANONICAL_PHASE_RECEIPT
}

registerIndexPayload = {
  symbol: TEXT,
  fromRegister: REGISTER_ID,
  toRegister: REGISTER_ID,
  relation:
    SAME_REGISTER | DISTINCT_TYPED_TERM | EXPLICIT_BRIDGE |
    UNMARKED_SUBSTITUTION,
  bridgeClaimId: ID | null,
  requestedInference: TYPED_REFERENCE | ENTAILMENT | MECHANISM
}

quantumMeasurePayload = {
  probabilityObject: EVENT_MEASURE | NORMALIZATION_SCALAR,
  requestedOperation: SAMPLE_OUTCOME | CHECK_NORMALIZATION,
  interpretiveClaim:
    NONE | CORRESPONDENCE | LITERAL_EXTRA_DIMENSION | UNIVERSAL_COLLAPSE
}

optionConePayload = {
  physicalConstraint: C_BOUNDED | SUPERLUMINAL,
  optionClaim: MODELED_REACHABILITY | PHYSICAL_CONE_EXPANSION,
  futureInfluence: ANTICIPATORY_MODEL | PHYSICAL_RETROCAUSALITY,
  commitmentKind: PARTIAL_RELATION | TOTAL_PREDICTOR
}

trophicAggregatorPayload = {
  quantityKind: HUMAN_INVESTMENT_PROXY | PHYSICAL_ENERGY,
  aggregationBasis: DECLARED_PROXY | MEASURED_PHYSICAL_SUM | METAPHORICAL,
  conservationClaim: NONE | EMPIRICALLY_TESTED | ASSUMED,
  persistentSharedTrace: BOOLEAN,
  carrierTurnoverObserved: BOOLEAN,
  laterSelectionReweightingObserved: BOOLEAN,
  requestedInference:
    DESCRIPTIVE_AGGREGATION | EGREGOREOTYPE_CANDIDATE | LITERAL_ENERGY_LAW
}
```

The predicates are closed:

- `VERDICT_MATRIX` passes exactly the verdict matrix already frozen in the
  parent design.
- `JUSTICE_CONTEXT` applies the same normative-premise-independent Justice and
  authority shape rules as a claim. A null context represents absence; it is
  legal only where neither Justice scope nor non-`NONE` authority effect
  requires the object.
- `RECEIPT_ROLE` is the following exact tagged truth table. For
  `SOURCE_RECORD`, `sourceKind` and `authorityRole` are non-null while
  `receiptId`, `phase`, and `status` are null; the source-role matrix must pass.
  `PROVENANCE` passes exactly for authority role `PROVENANCE`, and `CLAIM_OWNER`
  passes exactly for `OWNER`/`SEMANTIC_OWNER`; the other three requested uses
  fail. For `PHASE_RECEIPT`, `sourceKind` and `authorityRole` are null while
  typed receipt ID, phase, exact canonical receipt path, and status are
  non-null. `PROVENANCE` and `CANONICAL_PHASE_RECEIPT` pass at any declared
  status; `PHASE_DEPENDENCY` passes only at VERIFIED; `CLAIM_OWNER` and
  `EVIDENCE_UPGRADE` always fail.
- `REGISTER_INDEX` passes `TYPED_REFERENCE` exactly for: equal registers with
  `SAME_REGISTER` and a null bridge; unequal registers with
  `DISTINCT_TYPED_TERM` and a null bridge; or unequal registers with
  `EXPLICIT_BRIDGE` whose non-null claim ID resolves. Every other tuple and all
  `UNMARKED_SUBSTITUTION` cases fail. `ENTAILMENT` and `MECHANISM` always fail
  in this evaluator; they must be reclassified as a separately validated
  dependency claim rather than passing merely because this fixture names a
  bridge.
- `QUANTUM_MEASURE` accepts only EVENT_MEASURE/SAMPLE_OUTCOME or
  NORMALIZATION_SCALAR/CHECK_NORMALIZATION. `NONE` and `CORRESPONDENCE` are the
  only non-failing interpretation labels; literal extra dimensions and a
  universal interpretation-independent collapse claim fail.
- `OPTION_CONE` passes only the tuple `C_BOUNDED`, `MODELED_REACHABILITY`,
  `ANTICIPATORY_MODEL`, `PARTIAL_RELATION`.
- `TROPHIC_AGGREGATOR` passes `DESCRIPTIVE_AGGREGATION` for an explicitly
  declared human-investment proxy with no conservation claim, or for a measured
  physical sum whose conservation claim is marked empirically tested. An
  `EGREGOREOTYPE_CANDIDATE` additionally requires the proxy form plus all three
  persistent-trace/carrier-turnover/later-selection observations. This
  evaluator always rejects `LITERAL_ENERGY_LAW`; such a law requires a separate
  empirical claim and trial.
- `ROSETTA_TRANSFER` retains the exact predicate in §9.

The schema provides a closed `$def` for each semantic payload. Removing any
evaluator from dispatch, accepting an untyped payload, skipping a declared
fixture, or treating a match count as evidence is a named mutation failure.
Payload booleans and enums are declarations supplied to a structural test; they
are never empirical warrant by themselves.

## 10. The operational Compass fixture

A0B's synthetic integration vessel tests the following topology without
asserting it as cross-domain physics:

```text
actual state
  -> fallible model
  -> modeled reachable options inside physical constraints
  -> authorized commitment using available means
  -> action event
  -> occurrence receipt
  -> independently observed consequence
  -> model/selector update
```

Required distinctions:

- a modeled option cone is not a wider physical light cone;
- anticipated futures can influence present choice through a model without
  physical retrocausality;
- a commitment is not quantum measurement;
- a receipt proves occurrence/provenance, not outcome quality;
- an outcome observation, not the receipt alone, feeds the reflexive update;
- authorization proves permission, never truth or soundness;
- μ remains an asserted register-indexed crossing label, not a computable law;
- χ is a partial commitment relation, not a total predictor; and
- Rosetta recurrence is not independent replication.

The fixture includes negative mutations for each conflation. A1 decides which
owner claims survive those tests.

## 11. Beauty, Truth, Justice in the kernel

- **Beauty:** canonical bytes, one schema vocabulary, non-duplicated record
  definitions, deterministic output, and minimal public facades.
- **Truth:** typed premises and support, separate validity/soundness/modality,
  evidence ceilings, explicit falsifiers, owner quotes, provenance roles, and
  fail-closed mutation tests.
- **Justice:** normative claims require explicit normative premises and the
  complete existing Justice context: individual, sustaining whole, η,
  beneficiary, cost bearer, consent, custody, reversibility, exit, and
  option-cone effect.

`justiceContext` gains a typed authority boundary:

```text
authority = {
  regime: NOT_APPLICABLE | PRIVATE_DAV | PUBLIC_DAV | OTHER,
  mechanism:
    NONE | K2_NATURAL_PERSON | PRISM_PUBLIC_GOVERNANCE |
    CONSTITUTIONAL_AUTO_ENFORCEMENT | OTHER,
  basis: TEXT
}
```

`claim.authorityScope`, `claim.authorityEffect`, and their seam mirrors are
required independently of Justice scope:

- effect `NONE` requires `authorityScope=NONE`. When `justiceContext` is absent,
  that absence is the canonical not-applicable authority representation. When
  Justice scope independently requires a context, its authority must be
  regime/mechanism `NOT_APPLICABLE`/`NONE`;
- effect `DESCRIPTIVE` requires a non-`NONE` scope and Justice context. It may
  describe a retired historical mismatch, but authority regime always equals
  the declared scope. At ACTIVE or DRAFT lifecycle, PRIVATE_DAV requires
  `K2_NATURAL_PERSON`, PUBLIC_DAV requires `PRISM_PUBLIC_GOVERNANCE` or
  `CONSTITUTIONAL_AUTO_ENFORCEMENT`, and OTHER requires `OTHER`. RETIRED may
  preserve a historically mismatched mechanism while keeping the regime/scope
  identity explicit;
- `DISCRETIONARY` or `CONSEQUENTIAL` requires `PRIVATE_DAV` +
  `K2_NATURAL_PERSON`, `PUBLIC_DAV` + `PRISM_PUBLIC_GOVERNANCE`, or `OTHER` +
  `OTHER`;
- `CONSTITUTIONAL_AUTOMATIC` is legal only for `PUBLIC_DAV` with
  `CONSTITUTIONAL_AUTO_ENFORCEMENT`; it is enforcement of a prior public rule,
  not a software signature or new discretionary authorization.

Any non-`NONE` authority effect requires `justiceContext` even when
`justiceScope` would otherwise omit it. Thus a structural or actual
public-governance claim cannot evade the public-DAV rule by declaring
`justiceScope=NONE`, while an informational historical claim is not mistaken
for a consequential act. None of these rules creates a K2 gate for the
Kintsugi program itself, whose authority scope/effect are `NONE`.

No signature, software consensus, public consensus, private authority record,
or receipt may satisfy a Truth gate. Authorization fields can establish only
permission inside their declared regime.

## 12. External audit material

The earlier attachment remains optional `[B/D]` support at raw SHA-256:

```text
2937faf077f58a49e3c5953d33c3413ea3108350f82c8166eaf54818cdb5ad73
```

The later Rosetta-audit handoff is frozen only as an allegation source at raw
SHA-256:

```text
2777e3da427b735cd08ca5977dad15e06dd2e19223d0c5738c06955b823c8e1f
```

Neither attachment's counts, consensus language, tier assertions, or
conclusions enter the machine as proof. A0B persists no external-support
artifact because no authorized in-repository semantic location exists. A1 may
retest deduplicated allegations against pinned owner bytes before manifest
freeze.

## 13. Stop conditions

A0B stops rather than coerces when any of the following occurs:

- A0 compatibility output changes;
- a schema field or diagnostic code is invented outside the frozen contract;
- malformed input raises a traceback;
- a renderer operation escapes its declared output or edits owner prose;
- deterministic reruns differ;
- a bundle overwrite is attempted;
- a semantic reference dangles or cycles;
- analogy, Rosetta, provenance, lifecycle, signature, or repetition upgrades a
  claim;
- protected paths drift during an integration test;
- a live manifest/core/ledger/receipt or owner repair appears in A0B scope; or
- A1 later attempts to freeze `MAN-A-001` while a candidate owner or protected
  canonical path has unresolved concurrent dirt.

## 14. A0B acceptance

A0B is eligible for completion only when:

1. the design and this addendum produce one unambiguous v1 schema;
2. all three selectable roots validate through the restricted evaluator;
3. graph, evidence, modality, state, Justice, provenance, and omission barriers
   have positive and negative tests;
4. manifest/protected/Git behavior is proven in temporary repositories;
5. all four renderer operations are deterministic and bounded;
6. schema-derived plus named semantic mutations fail with stable diagnostics;
7. the original 22 A0 tests pass unchanged;
8. the canonical A0 baseline still prints exactly
   `KIN-OK baseline collected=19 failures=5`;
9. no live owner, public, archive, compatibility, receipt, manifest, ledger, or
   core-data artifact changed; and
10. an independent task review and whole-branch review report no unresolved
    Critical or Important finding.

The handoff to A1 is the verified machine, not a claim that the worldview has
already survived it.

## 15. Closed schema-drafting resolutions

This section removes the remaining implementation choices before the literal
schema is written.

### 15.1 Primitive and identity rules

- Schema `$id` is exactly
  `https://emergentism.org/schema/kintsugi/1.0.0`.
- `PATH` matches
  `^(?!/)(?!.*(?:^|/)\.{1,2}(?:/|$))(?!.*//)(?!.*\\)[^/]+(?:/[^/]+)*$`.
  The semantic resolver additionally applies `safe_repo_path`; no absolute,
  empty, dot-segment, trailing-slash, backslash, or root-escaping path passes.
- Top-level manifest/source/claim/trial/seam/antibody/discriminator/fixture/
  propagation/receipt/review-attempt/review-attestation/review-finding/
  review-finding-disposition IDs are globally unique across those collections.
- Premise IDs and support-link IDs are unique within their enclosing claim.
  A synchronized seam reuses those IDs and is not a second global definition.
- The baseline schema validates shape. Exact commands, base commit, node set,
  failures, and bytes remain the preserved A0 contract and its semantic check;
  the schema does not encode obsolete historical constants.

### 15.2 List and fixture cardinalities

The default `minItems: 1` law yields to an explicit status law. A manifest
referenced by a pre-review DRAFT receipt (`reviewAttemptId=null`) requires
`finalFiles=[]` and `finalFileCount=0`. A review-ready DRAFT receipt
(`reviewAttemptId` non-null) has already frozen the reviewed snapshot and
requires the `finalFiles.path` set to equal the `includedFiles.path` set,
`finalFileCount` to equal its length, and each final hash to cover the current
reviewed bytes. COMPLETE and VERIFIED retain the same final-snapshot law.
Receipt-to-manifest status and attempt state are cross-record semantic
invariants, not fields local to the manifest schema.

Manifest file inventories cover claim-bearing source/derivative bytes, not the
typed mutable control vessel that contains the inventory itself. Before
discovery cardinalities are computed, the resolver removes this exact reserved
control set from `candidateFiles`, `includedFiles`, `finalFiles`, and
`excludedPaths`:

```text
03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json
03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md
the canonical phase-receipt path for REC-A-108, REC-B-109, or REC-C-110
every current/prior attempt target, review, and bundle path
```

These paths remain in `allowedChangePaths`; only derived attempt paths belong in
`closureOnlyPaths`. The core JSON, semantic ledger, and receipt are never
closure-only and never receive a raw self/final hash inside their own manifest.
They are bound instead by typed role-specific projections: the review target
binds the core semantic records and ledger narrative/seam projections; attempt
artifacts bind target/review bytes; the final bundle binds the complete typed
records, raw final ledger sections, receipt descriptor/narrative hash, and
review history.
Receipt and ledger fences must still deep-equal their core records. Final
validation recomputes both the ordinary raw source inventory and these typed
control projections. A control path selected by a discovery glob is removed by
this role filter, not disguised as a source exclusion.

Fixture relationships are exact:

- `POSITIVE`: exit `1`, non-empty `expectedErrorCodes`,
  `expectedAntibodyIds`, `antibodyIds`, and `seamIds`;
- `NEGATIVE`: exit `0`, empty expected-error/match lists, non-empty
  `antibodyIds`, and `seamIds` may be empty;
- `QUOTATION` or `HISTORICAL`: exit `0`, empty expected-error/match lists,
  non-empty `antibodyIds`, and `seamIds` may be empty; and
- `MUTATION`: exit `1`, non-empty `expectedErrorCodes`; antibody/match/seam
  lists may be empty. It additionally requires
  `mutationLevel=SCHEMA|GRAPH|SEMANTIC|MARKDOWN|GIT|RENDERER`.

Every non-MUTATION fixture requires `mutationLevel=null`. The typed level is
coverage metadata; it does not change the expected-error rule.

### 15.3 Trial, discriminator, and seam states

- `breakState=NONE` requires `status=CLOSED`, null defect/severity/seam, and may
  have an empty discriminator list.
- `ALLEGED` requires `TRIED` or `DISPUTED`, non-null defect/severity, and null
  seam.
- `CONFIRMED` requires `ADJUDICATED` or `CLOSED`, non-null defect/severity/seam.
- Trial/seam discriminator lists may be empty when a declared countermodel is
  decisive (`defeatedConclusion != NONE_FOUND`). `HELD_OPEN` always requires at
  least one discriminator because no repair or decisive countermodel closes it.
- A `RETRACTED` seam requires `repairKind=RETRACT` and
  `evidenceAfter.lifecycle=RETIRED`; the synchronized claim is also `RETIRED`,
  and `evidenceAfter.strength=evidenceBefore.strength`.
- `repairKind=RETIER` requires unequal before/after strengths. Upward movement
  satisfies the prior upgrade criterion and upgrade-evidence rules; downward
  movement satisfies the prior kill criterion. No other repair kind changes
  strength.
- `upgradeCriterion.kind=NONE` is legal at any current strength; strength `A`
  requires it because no higher target exists.

### 15.4 Review ownership

- the LOGIC review owns the Truth gate and all evidence-upgrade approvals;
- the BTJ review owns the Beauty and Justice gates; and
- each gate's non-null `reviewerPath` must equal the owning receipt review path.

Real-name consent is not inferred from display text. The machine validates the
declared `creditConsent` enum; reviewers enforce that a real displayed name
requires `NAMED`. Substantive identity and consent truth remain review work.

### 15.5 Receipt identities

The unique typed phase receipts are:

```text
REC-A-108 -> 11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md
REC-B-109 -> 11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md
REC-C-110 -> 11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md
```

Bare human numbers never resolve.

### 15.6 Source kind and authority-role matrix

```text
OWNER       -> SEMANTIC_OWNER
SUPPORT     -> EVIDENCE | PROVENANCE
COMPRESSION -> DERIVATIVE
PUBLIC      -> DERIVATIVE
RECEIPT     -> PROVENANCE
```

No other pairing passes. A source role does not determine a claim's evidence
strength.

### 15.7 Public owner-search and queue law

Replace free-form `ownerSearchEvidence: LIST[TEXT]` with:

```text
ownerSearchEvidence = {
  manifestIds: LIST[ID],
  searchedSourceIds: LIST[ID],
  method: TEXT,
  result: TEXT
}
```

Every manifest and source ID resolves. For `candidateOwners=[]`, the searched
source set must equal the set of `SEMANTIC_OWNER` sources eligible under the
listed frozen manifests; this is the machine meaning of a complete
manifest-bounded search. When candidates exist, each candidate path must be a
member of that searched semantic-owner source set; the candidate set need not
equal the entire search set.

OWNERLESS queue items allow only `RETRACT` or `REGENERATE`; they cannot use
`KEEP`, `CITE`, `NARROW`, or `RETIER`. OWNED `KEEP` remains the only clean
disposition with null drift/severity.

### 15.8 Review and bundle schema roles

`reviewAttempt`, `reviewAttemptArtifact`, `reviewAttestation`, `reviewFinding`,
`reviewProcessEvidence`, `reviewFindingDisposition`,
`reviewFindingDispositionInput`, `reviewTarget`, `receiptDescriptor`, and
`validationBundle` are named nested `$defs`. They are validated by renderer and
orchestration functions through local references but are not additional CLI
root roles. The only selectable roots remain `coreData`, `publicQueue`, and
`baselineAllowlist`.

`reviewTarget` has exactly:

```text
reviewTarget = {
  schemaVersion: "1.0.0",
  phase: A | B | C,
  currentAttemptId: ID,
  receiptId: ID,
  receiptNarrativeRawSha256: RAW_HASH,
  reviewSubjectDigest: RAW_HASH,
  manifest: semantic manifest projection,
  sources: LIST[source],
  claims: LIST[claim],
  trials: LIST[trial],
  seams: LIST[review seam projection],
  propagations: LIST[propagation],
  antibodies: LIST[antibody],
  discriminators: LIST[discriminator],
  fixtures: LIST[fixture],
  schemaSha256: RAW_HASH,
  ledgerPreambleRawSha256: RAW_HASH,
  ledgerSemanticSections: LIST[ledgerSemanticSection],
  semanticDiffPaths: LIST[PATH],
  priorReviewAttempts: LIST[reviewAttempt],
  priorReviewAttemptArtifacts: LIST[reviewAttemptArtifact],
  priorReviewAttestations: LIST[reviewAttestation],
  priorReviewFindings: LIST[reviewFinding],
  priorReviewFindingDispositions: LIST[reviewFindingDisposition]
}

ledgerSemanticSection = {
  id: ID,
  narrativeRawSha256: RAW_HASH,
  seamProjection: review seam projection
}
```

Every two-sided narrative hash uses boundary-preserving framing rather than raw
concatenation:

```text
framedNarrativeHash(prefix, suffix) = SHA256(
  UTF8("KINTSUGI-NARRATIVE-V1") || 0x00 ||
  uint64be(len(prefix)) || prefix ||
  uint64be(len(suffix)) || suffix
)
```

Lengths count raw bytes and overflow fails closed. Thus moving identical prose
from one side of a fence to the other changes the digest.

`ledgerPreambleRawSha256` hashes the exact bytes from the beginning of the
semantic ledger through the byte before its first seam heading; the SHA-256 of
empty bytes is used when no preamble exists. Together, the preamble hash, every
section's `framedNarrativeHash(bytes_before_fence, bytes_after_fence)`, and
every fenced seam projection bind every ledger byte without making mechanical
gate/status fields semantic. `LEDGER-PREAMBLE` is a reserved review endpoint ID
for that projection and may not be used as a claim, seam, finding, or ordinary
record ID.

The phase receipt's fenced record is deliberately absent except for its typed
`receiptId` chain key. `receiptNarrativeRawSha256` equals
`framedNarrativeHash(bytes_before_fence, bytes_after_fence)` for the unique
`json kintsugi-receipt` fence. Receipt status, digest, review paths, and bundle
fields inside the fence are mechanical closure, while any surrounding human
claim and its side-of-fence position remain reviewed and hash-bound. Dynamic
status prose is therefore forbidden outside the fence after target freeze.

For a selected current attempt, the five prior-review lists contain its complete
terminal ancestor chain, matching artifact hashes, every extant attestation and
typed finding, and every disposition that authorized a successor. They are in
root-to-leaf chain order, are empty on the first attempt, and exclude the
current PENDING attempt. Thus a new reviewer receives cryptographically bound
prior FAIL or ABANDONED history and its unresolved obligations without making
the current target digest depend on its own future attestations. PASSED attempts
are terminal successes and can never have a successor.

`reviewSubjectDigest` is the raw SHA-256 of the canonical semantic-subject
projection of this target. That projection removes `currentAttemptId`,
`reviewSubjectDigest`, and all five `priorReview*` fields. It retains
`receiptId`, but normalizes attempt mechanics out of the manifest by setting
`closureOnlyPaths=[]`, removing all derived attempt paths from
`allowedChangePaths`, and retaining no closure-file hash records (already
removed by the semantic manifest projection). It therefore changes for a
semantic repair but not merely because another review attempt number or review
file exists. The raw SHA-256 of the complete `reviewTarget` remains the digest
signed by attestations and stored by a completed receipt.

Cross-file hashes, Git history, transitive graph closure, state-transition
deltas, reviewer independence, and substantive warrant remain procedural
kernel checks. The literal schema handles structural shape and conditionals; it
does not simulate Git or intellectual judgment.

### 15.9 Honest bootstrap and gate context

The unique truthful pre-trial exception is the explicit Phase A
`--bootstrap` state whose `REC-A-108` is DRAFT. In that state only:

```text
coreData.trials = []
MAN-A-001.trialedClaimIds = []
MAN-A-001.trialedClaimCount = 0
REC-A-108.trialIds = []
MAN-A-001.finalFiles = []
MAN-A-001.finalFileCount = 0
MAN-A-001.closureOnlyPaths = []
```

Claims and harvested-claim bindings remain non-empty: bootstrap freezes what is
about to be tried without pretending that a trial already occurred. The schema
therefore permits those three trial arrays to be empty, while the semantic
kernel rejects emptiness outside this exact Phase A/bootstrap/DRAFT state.
Phases B and C, bare non-bootstrap validation, COMPLETE, and VERIFIED all
require non-empty closed trial coverage appropriate to their manifests.

The empty `finalFiles` exception also applies to any honest pre-review DRAFT
whose `reviewAttemptId=null`; it says only that no reviewed final snapshot has
yet been frozen. Once `freeze-manifest --final` allocates an attempt, that same
DRAFT becomes review-ready: its final-file path set equals its included-file
path set, and its final records carry exact current hashes. Thus DRAFT describes
both construction and review without ever pretending that an unfrozen worktree
is the reviewed subject.

Gate closure is likewise cross-record. While a receipt is DRAFT, the candidate
gates it owns remain PENDING with null reviewer paths; gates already frozen by
an earlier VERIFIED receipt remain immutable. A failed review is preserved by
its immutable FAIL attestation; it does not mutate the candidate core gate, and
the receipt cannot advance. A receipt at COMPLETE or VERIFIED requires every
terminal gate it cites to be PASS with the owning review path: LOGIC owns
Truth, while BTJ owns Beauty and Justice. No PASS or FAIL candidate gate may be
persisted by the current DRAFT attempt, and a FAIL attestation can never satisfy
a completion transition. `VERIFIED` seams retain the local structural all-PASS
rule; proposed and terminal `RETRACTED` states are distinguished by their
referencing receipt state rather than by inventing another seam status.

### 15.10 Retryable review attempts and closure-only paths

A failed review is evidence, not a permanent deadlock. The fixed single review
and target paths in the parent design are superseded pre-v1 by an append-only
attempt chain. `coreData` gains the following required arrays; all are empty at
bootstrap and persist thereafter:

```text
reviewAttempts: LIST[reviewAttempt]
reviewAttemptArtifacts: LIST[reviewAttemptArtifact]
reviewAttestations: LIST[reviewAttestation]
reviewFindings: LIST[reviewFinding]
reviewFindingDispositions: LIST[reviewFindingDisposition]
```

Every phase receipt gains `reviewAttemptId: ID | null`, and every
`reviewAttestation` gains `attemptId: ID`.

```text
reviewAttempt = {
  id: ID,
  phase: A | B | C,
  receiptId: ID,
  supersedesAttemptId: ID | null,
  reviewSubjectDigest: RAW_HASH,
  reviewTargetPath: PATH,
  logicReviewPath: PATH,
  btjReviewPath: PATH,
  validationBundlePath: PATH,
  logicAttestationId: ID | null,
  btjAttestationId: ID | null,
  status: PENDING | FAILED | PASSED | ABANDONED,
  abandonReason: TEXT | null
}

reviewAttemptArtifact = {
  attemptId: ID,
  reviewTargetSha256: RAW_HASH | null,
  logicReviewSha256: RAW_HASH | null,
  btjReviewSha256: RAW_HASH | null
}

reviewFinding = {
  id: ID,
  attemptId: ID,
  reviewKind: LOGIC | BTJ,
  category:
    LOGIC | EVIDENCE | BEAUTY | JUSTICE | PROVENANCE | SCOPE | PROCESS,
  severity: CRITICAL | MAJOR | MINOR,
  statement: TEXT,
  claimIds: LIST[ID],
  seamIds: LIST[ID],
  ledgerSectionIds: LIST[ID],
  receiptIds: LIST[ID],
  subjectPaths: LIST[PATH]
}

reviewProcessEvidence = {
  path: PATH,
  sha256: RAW_HASH
}

reviewFindingDisposition = {
  id: ID,
  findingId: ID,
  fromAttemptId: ID,
  successorAttemptId: ID,
  disposition: ADDRESSED | DISPUTED | PROCESS_INVALID,
  rationale: TEXT,
  claimIds: LIST[ID],
  seamIds: LIST[ID],
  ledgerSectionIds: LIST[ID],
  receiptIds: LIST[ID],
  subjectPaths: LIST[PATH],
  discriminatorIds: LIST[ID],
  evidenceFiles: LIST[reviewProcessEvidence]
}

reviewFindingDispositionInput = {
  findingId: ID,
  disposition: ADDRESSED | DISPUTED | PROCESS_INVALID,
  rationale: TEXT,
  claimIds: LIST[ID],
  seamIds: LIST[ID],
  ledgerSectionIds: LIST[ID],
  receiptIds: LIST[ID],
  subjectPaths: LIST[PATH],
  discriminatorIds: LIST[ID],
  evidenceFiles: LIST[reviewProcessEvidence]
}
```

All five review-finding location lists may be empty; a PROCESS finding can
concern review conduct rather than a semantic endpoint. A schema, source,
provenance, or tool finding uses `subjectPaths`; ledger prose uses
`ledgerSectionIds`; receipt prose uses the chain's `receiptIds`. No location
field is an implicit evidence claim.

Review Markdown retains exactly one `json kintsugi-review` attestation fence and
adds exactly one `json kintsugi-review-findings` fence containing that review's
sorted finding records; the list may be empty. Its IDs deep-equal
`attestation.findingIds`, and every finding's `attemptId` and `reviewKind`
deep-equal the enclosing attestation. The raw review artifact hash covers both
fences and all intervening bytes.

Attempt IDs are canonical, not merely regex-shaped. For positive integer `n`,
the only legal spelling is `RVA-{phase}-{str(n).zfill(3)}`: `001`, `010`, `999`,
and `1000` are legal, while `000`, `0001`, and any parse/re-render mismatch are
not. `n` is the smallest unused positive integer for that phase across the live
core, worktree attempt paths, the current Git tree, and reachable Git history.
The ID letter equals `phase`. Paths derive exactly from the ID:

```text
reviewTargetPath =
  09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{id}/review_target.json
logicReviewPath =
  11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{id}_LOGIC.md
btjReviewPath =
  11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{id}_BTJ.md
validationBundlePath =
  09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{id}/validation_bundle.json
```

The first attempt has `supersedesAttemptId=null`. Every later attempt points to
the unique prior leaf for the same `(phase, receiptId)` chain; that prior leaf
must be `FAILED` or `ABANDONED`. A `PASSED` attempt is never superseded. The
union graph is acyclic and has exactly one leaf per `(phase, receiptId)` chain.
Attempts and artifacts are one-to-one and stored in root-to-leaf chain order;
attestations, findings, and dispositions resolve exactly once and cannot be
orphaned.

A successor cannot be allocated until the predecessor's terminal core record,
receipt fence, target if present, every extant review, and matching artifact
hashes are committed at the current `HEAD`. Those bytes and terminal records
are then immutable. Allocation resolves the shared Git common directory with
`git rev-parse --git-common-dir`, not the current worktree's `.git` indirection.
It takes an exclusive-create `.kintsugi-transition.lock` there and reserves the
chosen ID with another exclusive-create canonical JSON record at
`kintsugi-attempt-reservations/{id}.json`. The durable reservation includes ID,
phase, receipt, expected HEAD, and expected raw core hash and is counted as used
by every worktree even before commit. An operation that fails after reservation
may burn an ID but may never reuse it.

The caller supplies the expected `HEAD` and raw core hash; both are checked
before lock acquisition and again while holding the shared lock. Allocation
scans core, worktree paths, current and reachable Git paths, and the shared
reservation directory. Any collision, stale expectation, malformed
reservation, or extant lock fails closed. The lock is removed in `finally`; a
crash residue requires explicit inspection rather than lock stealing.
Every mutating renderer stage uses this same Git-common-dir lock and repeats the
HEAD/core compare-and-swap checks; the reservation file is additionally created
only when an attempt ID is allocated.

The locked transaction also freezes a sorted raw-hash read set covering every
repository or external input consumed by prospective validation, including
core, schema, manifest sources, ledger, receipt, existing target/reviews,
candidate review/disposition files, current output bytes or typed `ABSENT`, and
the reservation record. After all output temporaries are written and fsynced,
but immediately before the first repository `os.replace`, the renderer re-reads
`HEAD`, the raw core bytes, and every read-set member and requires exact
identity with the frozen values. A changed, missing, newly appeared, retargeted
symlink, or unreadable input aborts before any repository replacement, removes
all temporaries, and burns only an already-created attempt reservation. The
same final compare-and-swap is mandatory for every mutating stage; validation
performed earlier while holding the custom lock is not a substitute.

Findings close the reviewer-shopping gap. A FAIL attestation has non-empty
`findingIds` and non-empty `openSevereFindingIds`; the latter deep-equals the set
of referenced CRITICAL/MAJOR findings and is therefore a non-empty subset of the
former. A PASS has no open severe finding and may name only MINOR findings. All
finding IDs resolve to the same attempt and review kind as their attestation.

Successor allocation and finding disposition are one locked transaction, not
two individually valid intermediate states. `freeze-manifest --final` accepts a
canonical JSON array through `--finding-dispositions-input` outside the
repository. It is absent/empty for the first attempt and otherwise contains
exactly one `reviewFindingDispositionInput` for every finding from the direct
terminal predecessor, sorted by `findingId`. While holding the shared lock, the
renderer reserves the successor ID, expands each input into a persisted
disposition with:

```text
id = RFD-{successorAttemptId}-{str(1-based ordinal).zfill(3)}
fromAttemptId = direct predecessor ID
successorAttemptId = newly reserved ID
```

It then constructs and validates the successor attempt, dispositions, final
manifest, receipt pointer, subject digest, and core graph together before any
repository byte is written. A failed prospective transaction burns the shared
reservation but leaves no dangling disposition or successor record.

Disposition laws are exact:

- `ADDRESSED` requires a non-empty combined claim/seam/ledger-section/receipt/
  subject-path endpoint set. Claim and seam IDs resolve in the successor
  subject; ledger IDs resolve to `ledgerSemanticSections` or the reserved
  `LEDGER-PREAMBLE` projection; receipt IDs equal the target's chain receipt.
  Every subject path is non-closure,
  non-reserved-control, and present in the successor final source inventory.
  Its predecessor projection is the prior raw hash or a typed `ABSENT` marker
  when the repair lawfully creates the path. At least one named endpoint's
  canonical projection, ledger preamble/narrative/seam projection, receipt
  narrative hash, or raw subject-file hash/absence marker differs. Its
  discriminator and evidence-file lists are empty;
- `DISPUTED` requires at least one resolving discriminator ID, permits
  semantic location lists only to locate the dispute, and has an empty
  evidence-file list; and
- `PROCESS_INVALID` requires at least one `reviewProcessEvidence` record and
  empty claim, seam, ledger-section, receipt, subject-path, and discriminator
  lists. Each evidence record must deep-equal either a predecessor target/review
  path and hash in its immutable `reviewAttemptArtifact`, or a regular
  non-closure file record in the successor manifest's `finalFiles`. The live
  raw bytes must hash exactly.

Because the complete disposition (including evidence hashes) appears in the
successor review target and final validation bundle, a temporary, missing,
mutable, or unhash-bound excuse cannot license a same-subject retry.

If any disposition is ADDRESSED or DISPUTED, the successor's
`reviewSubjectDigest` must differ from the predecessor's. The same semantic
subject may be retried only when every predecessor disposition is
PROCESS_INVALID; the universal condition is vacuously true for an ABANDONED
attempt with no findings, whose non-empty `abandonReason` still exposes the
process event. Every ancestor finding and its unique disposition remains in all
later targets and final bundles.

State laws are exact:

- `PENDING` has zero or one attestation ID and null `abandonReason`. When one is
  present it references a PASS attestation; this is the partially reviewed
  ATTESTED state, not a terminal pass;
- `FAILED` has one or two attestation IDs, at least one referenced FAIL
  attestation with an open severe finding, and null `abandonReason`;
- `PASSED` has both non-null attestation IDs, two PASS attestations over one
  target digest, and null `abandonReason`;
- `ABANDONED` has zero, one, or two attestation IDs and non-null
  `abandonReason`; every extant attestation and finding is preserved even when
  target drift or a process defect invalidates the attempt; and
- only the atomic COMPLETE transition may change the current PENDING attempt to
  PASSED while changing DRAFT to COMPLETE. FAILED or ABANDONED remains DRAFT
  until a lawful successor is allocated after repair/re-freeze.

Artifact hashes and file existence are biconditional. A target exists exactly
when `reviewTargetSha256` is non-null. A LOGIC or BTJ review exists exactly when
both its attestation ID and matching artifact hash are non-null. Every extant
review requires the target and names its exact digest. Every extant file hashes
exactly to its record. The permitted state/path matrix is:

```text
PENDING                 target optional; 0 or 1 PASS review; bundle absent
FAILED                  target present; referenced reviews present; bundle absent
PASSED + receipt COMPLETE  target + both reviews present; bundle absent
PASSED + receipt VERIFIED  target + both reviews + bundle present
ABANDONED               target/reviews exactly as recorded; bundle absent
```

No other closure file may exist. In particular, an unreferenced review, an old
bundle under a failed/abandoned attempt, or a validation bundle written before
the VERIFIED transition fails `KIN-E-BUNDLE`. An ATTESTED, FAILED, ABANDONED,
or COMPLETE command accepts newly authored raw bytes only through optional
`--logic-review-input` and `--btj-review-input` files outside the canonical
repository root. Each supplied kind must be currently unrecorded and must parse
to the exact derived attempt/path/kind. While holding the shared lock, the
command validates the complete prospective state, stages the canonical review
file plus core/artifact/finding/receipt updates, and installs or rolls back the
whole set as one renderer transaction. It never copies a candidate into place
before the prospective state passes. Outside that operation-specific intake,
an unrecorded canonical review file is invalid.

The receipt's nullable `reviewAttemptId` is null exactly for a pre-review DRAFT
and becomes non-null exactly when the first/current attempt is allocated. It
then points to the unique current leaf and never returns to null. DRAFT keeps
its target/review/bundle closure fields null even when the attempt records those
artifacts. COMPLETE and VERIFIED require the current PASSED attempt; their
target digest and review
paths deep-equal that attempt and its attestations. COMPLETE keeps the receipt
bundle path/digest null; VERIFIED sets its bundle path to the attempt's derived
`validationBundlePath` and adds the exact bundle digest.

The four renderer operations implement six explicit stages:

1. `freeze-manifest --final` freezes final-file path coverage equal to the
   included-file path set using current hashes, allocates a new PENDING attempt,
   expands/validates any required finding-disposition input, computes its
   subject digest, and records null artifacts in the same locked transaction.
   An existing non-terminal attempt must first become ABANDONED; a terminal
   predecessor must satisfy the commit/immutability law above.
2. `review-target` performs `TARGET_READY`: it writes only the current PENDING
   attempt's canonical target and records its exact hash. Identical reuse is
   allowed; drift or overwrite is not.
3. `transition-core --stage ATTESTED` records the first PASS review and keeps
   the attempt PENDING and the receipt DRAFT.
4. `transition-core --stage FAILED` records all extant reviews after any FAIL,
   sets the attempt FAILED, and leaves receipt and candidate gates
   DRAFT/PENDING. `--stage ABANDONED` records zero to two extant reviews and the
   reason, then sets ABANDONED without erasing bytes.
5. `transition-core --stage COMPLETE` accepts the second independent PASS only
   after constructing and validating the entire prospective VERIFIED bundle in
   memory. It then records both reviews/findings, sets the attempt PASSED,
   closes the owned gates, and changes the receipt to COMPLETE. If prospective
   bundle construction, semantic validation, Git checks, or any hash check
   fails, no COMPLETE bytes are written.
6. `transition-core --stage VERIFIED` renders the already preflighted bundle,
   revalidates it, and commits bundle/core/receipt outputs under the same
   exclusive lock. All bytes are staged before replacement; any crash residue
   is invalid and fails closed. The standalone `bundle` operation is a pure
   deterministic construction/preflight surface and may not leave a canonical
   bundle file without the matching VERIFIED transition.

`closureOnlyPaths` is the exact union of the four derived paths for every
declared attempt in the selected phase and is a subset of `allowedChangePaths`.
No owner, protocol, schema, test, core data, semantic ledger, receipt, public
queue, or other semantic path may be classified closure-only. A role/path
mismatch fails before `semanticDiffPaths` is computed, so closure mechanics
cannot erase a semantic change from the review target.

The validation bundle gains the complete root-to-leaf review history:

```text
receiptNarrativeRawSha256: RAW_HASH
ledgerPreambleRawSha256: RAW_HASH
reviewAttempts: LIST[reviewAttempt]
reviewAttemptArtifacts: LIST[reviewAttemptArtifact]
reviewAttestations: LIST[reviewAttestation]
reviewFindings: LIST[reviewFinding]
reviewFindingDispositions: LIST[reviewFindingDisposition]
```

Each artifact ID deep-equals its attempt ID, and attempt/artifact coverage is an
exact bijection. The bundle's existing final `logicReviewSha256` and
`btjReviewSha256` equal the current PASSED artifact. It also repeats the exact
current `reviewSubjectDigest` through the attempt/target records and deep-equals
the receipt narrative hash in the reviewed target after recomputing the live
bytes outside the fence. It likewise deep-equals the reviewed ledger preamble
hash after recomputing the live bytes before the first seam heading. A bundle
omitting an older failure, abandonment, attestation, finding, or disposition;
changing any historical byte; hiding a partially completed review; or carrying
an unreferenced closure file fails.
