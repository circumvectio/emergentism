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

## 6. Pre-v1 claim contract additions

Every claim gains five fields:

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
deep-equal because no repair exists. Actual evidence upgrades are judged
against `priorUpgradeCriterion`; retiers and retractions are judged against
`priorKillCriterion`. `beforeQuote`, `beforeHash`, the trial, and
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

- effect `NONE` requires scope/regime `NONE`/`NOT_APPLICABLE` and mechanism
  `NONE`;
- effect `DESCRIPTIVE` requires a non-`NONE` scope and Justice context. It may
  describe a retired historical mismatch, but an ACTIVE or DRAFT public claim
  still forbids `K2_NATURAL_PERSON`;
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
  propagation/receipt IDs are globally unique across those collections.
- Premise IDs and support-link IDs are unique within their enclosing claim.
  A synchronized seam reuses those IDs and is not a second global definition.
- The baseline schema validates shape. Exact commands, base commit, node set,
  failures, and bytes remain the preserved A0 contract and its semantic check;
  the schema does not encode obsolete historical constants.

### 15.2 List and fixture cardinalities

The default `minItems: 1` law yields to an explicit status law. In particular,
a DRAFT manifest requires `finalFiles=[]` and `finalFileCount=0`.

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
  `evidenceAfter.lifecycle=RETIRED`; the synchronized claim is also `RETIRED`.
- `upgradeCriterion.kind=NONE` is legal at any current strength; strength `A`
  requires it because no higher target exists.

### 15.4 Review ownership

- the LOGIC review owns the Truth gate and all evidence-upgrade approvals;
- the BTJ review owns the Beauty and Justice gates; and
- each gate's non-null `reviewerPath` must equal the owning receipt review path.

Real-name consent is not inferred from display text. The machine validates only
the declared `creditConsent` enum and the existing rule that a real displayed
name requires `NAMED`; substantive identity/consent truth remains review work.

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

`reviewAttestation`, `reviewTarget`, `receiptDescriptor`, and
`validationBundle` are named nested `$defs`. They are validated by renderer and
orchestration functions through local references but are not additional CLI
root roles. The only selectable roots remain `coreData`, `publicQueue`, and
`baselineAllowlist`.

`reviewTarget` has exactly:

```text
reviewTarget = {
  schemaVersion: "1.0.0",
  phase: A | B | C,
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
  ledgerSemanticSections: LIST[ledgerSemanticSection],
  semanticDiffPaths: LIST[PATH]
}

ledgerSemanticSection = {
  id: ID,
  narrativeRawSha256: RAW_HASH,
  seamProjection: review seam projection
}
```

The phase receipt is deliberately absent. Receipt status, digest, review paths,
and bundle fields are mechanical closure, not reviewed semantics.

Cross-file hashes, Git history, transitive graph closure, state-transition
deltas, reviewer independence, and substantive warrant remain procedural
kernel checks. The literal schema handles structural shape and conditionals; it
does not simulate Git or intellectual judgment.
