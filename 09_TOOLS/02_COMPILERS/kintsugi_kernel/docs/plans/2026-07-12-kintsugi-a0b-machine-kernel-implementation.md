# Kintsugi A0B Machine-Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan one task at
> a time. For every task, write the named failing test first, observe the stated
> RED result, implement only the named contract, observe GREEN, and make the
> proposed path-limited commit. Only then does the controller package and
> dispatch review of that committed range.

**Goal:** Build the deterministic, standard-library-only machine that can test
Emergentism's Kintsugi claim grammar without creating or repairing any live
claim, owner, manifest, ledger, receipt, public page, archive record, or
compatibility artifact.

**Controlling contract:**
`docs/superpowers/specs/2026-07-12-kintsugi-a0b-machine-kernel-addendum.md`.
It supersedes conflicting pre-v1 details in the parent design. Do not edit the
parent design to restate the addendum and do not revive the stale draft's old
support-link, kill-criterion, authority, manifest-binding, or three-`$defs`
contracts.

**Architecture:** Keep `validate_kintsugi.py` as the thin, import-compatible A0
facade. Put reusable behavior in a `kintsugi_kernel/` package split by concern:
diagnostics and codecs at the bottom; baseline and schema above them; typed
records, semantics, Markdown, Git, and manifest checks in the middle; review,
orchestration, and rendering at the top. Keep `render_kintsugi.py` as the only
executable allowed to write generated output. All A0B tests use complete
synthetic fixtures and temporary Git repositories.

**Runtime:** Python 3.11 standard library, `unittest`, JSON Schema Draft
2020-12 contract, and read-only Git CLI queries. No third-party runtime
dependency, network access, clock value, random identifier, external asset,
or host-specific path may affect output bytes.

## Global Constraints

- A0B may create the schema, package, CLIs, tests, compiler documentation, and
  a machine-only handoff record.
- A0B must not create `MAN-A-001`, `02_KINTSUGI_SEAMS.json`,
  `02_KINTSUGI_SEAM_LEDGER.md`, `REC-A-108`, live sources/claims/trials/seams,
  reviews, validation bundles, owner repairs, or Phase C queue data.
- A0B must not modify any live owner under `00_META/`, `02_EPISTEMOLOGY/`,
  `05_COSMOLOGY/`, or `07_THEOLOGY/`; anything under `12_PUBLIC_SITE/`,
  `90_ARCHIVE/`, or `91_COMPATIBILITY/`; or the A0 baseline contract.
- Synthetic paths may resemble production shapes only inside temporary test
  directories. Tests never copy live semantic bytes into those fixtures.
- The validator is read-only. Pure lower layers return sorted `Issue` values;
  they do not print, exit, or write. Only the renderer performs bounded writes.
- The A0 compatibility surface remains exact: imports, `--check-baseline`,
  `--contract`, `--canonical-root`, diagnostic bytes, exits, and the canonical
  success line `KIN-OK baseline collected=19 failures=5`.
- `--contract` remains an alias for `--baseline-allowlist`; it is not a second
  baseline source.
- The Kintsugi program's authority scope/effect is `NONE`; no K2 gate is added.
- Review retries are append-only evidence. The five review-history arrays,
  predecessor files, terminal records, and matching hashes are never erased or
  rewritten; a PASSED attempt is terminal and cannot be superseded.
- Every mutating stage uses one Git-common-directory lock, durable attempt-ID
  reservation when allocating, and caller-supplied expected `HEAD` plus raw
  core hash checked before and after lock acquisition.
- Newly authored review bytes enter only through external
  `--logic-review-input` or `--btj-review-input` files during the named
  transactional transition stages. An unrecorded review already inside the
  canonical repository is invalid.
- Every malformed input is controlled: no traceback, deterministic diagnostic
  order, semantic failures exit 1, and invocation/unreadable-input failures
  exit 2.

## Sequential SDD review law

For every Task 1–9, the order is invariant:

1. the fresh implementer records the task's BASE commit;
2. the implementer runs the named RED test, implements only the task, obtains
   GREEN, and creates the path-limited implementation commit;
3. the controller records HEAD, builds the review package for the committed
   `BASE..HEAD` range, and dispatches the task reviewer;
4. any accepted finding is implemented as a path-limited follow-up commit; and
5. the controller rebuilds the package through the new HEAD and repeats review
   until the committed range is review-clean.

No reviewer approves an uncommitted working-tree diff. Task 9's final HEAD,
29-path, forbidden-scope, and clean-status assertions run only after its
review-clean final commit. The controller's whole-branch review remains a
separate gate after all nine task ranges are clean.

## Final tracked file map

Create:

- `03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json`
- `docs/superpowers/plans/2026-07-12-kintsugi-a0b-machine-kernel-implementation.md`
- `docs/superpowers/specs/2026-07-12-kintsugi-a0b-machine-kernel-handoff.md`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/__init__.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/diagnostics.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/codec.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/baseline.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/schema.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/records.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/semantics.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/markdown.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/gitstate.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/manifest.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/review.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/orchestration.py`
- `09_TOOLS/02_COMPILERS/kintsugi_kernel/rendering.py`
- `09_TOOLS/02_COMPILERS/render_kintsugi.py`
- `09_TOOLS/02_COMPILERS/kintsugi_test_support.py`
- `09_TOOLS/02_COMPILERS/test_kintsugi_schema.py`
- `09_TOOLS/02_COMPILERS/test_kintsugi_records.py`
- `09_TOOLS/02_COMPILERS/test_kintsugi_semantics.py`
- `09_TOOLS/02_COMPILERS/test_kintsugi_markdown.py`
- `09_TOOLS/02_COMPILERS/test_kintsugi_manifest.py`
- `09_TOOLS/02_COMPILERS/test_kintsugi_review.py`
- `09_TOOLS/02_COMPILERS/test_render_kintsugi.py`
- `09_TOOLS/02_COMPILERS/test_kintsugi_mutations.py`

Modify:

- `09_TOOLS/02_COMPILERS/validate_kintsugi.py`
- `09_TOOLS/02_COMPILERS/README.md`

Preserve byte-for-byte:

- `09_TOOLS/02_COMPILERS/test_validate_kintsugi.py`
- `09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json`

The controlling addendum is already part of this branch. No exact small path
count from the stale draft survives; Task 9 checks the complete declared set.

## Stable package surface

The package exposes these concern-level entry points. Implementations may use
private helpers, but no task may collapse the package back into a monolith.

```python
# diagnostics.py
@dataclass(frozen=True, order=True)
class Issue:
    path: str
    code: str
    message: str

class KintsugiError(Exception): ...

# codec.py
def canonical_json_bytes(value: object) -> bytes: ...
def raw_hash(payload: bytes) -> str: ...
def text_hash(text: str) -> str: ...
def safe_repo_path(root: Path, relative: str) -> Path: ...
def load_canonical_json(path: Path) -> object: ...

# schema.py
def validate_schema_document(schema: object) -> list[Issue]: ...
def validate_schema_instance(
    schema: dict[str, object], root_role: str, instance: object
) -> list[Issue]: ...
def validate_named_definition(
    schema: dict[str, object], def_name: str, instance: object
) -> list[Issue]: ...

# records.py / semantics.py
def validate_core_records(
    core: dict[str, object], *, phase: str | None = None,
    bootstrap: bool = False
) -> list[Issue]: ...
def validate_public_queue(
    queue: dict[str, object], core: dict[str, object]
) -> list[Issue]: ...
def evaluate_semantic_fixture(
    evaluator: str, payload: dict[str, object], core: dict[str, object]
) -> list[Issue]: ...
def evaluate_antibody_fixture(
    core: dict[str, object], fixture_id: str
) -> list[Issue]: ...
def safe_regex_search(pattern: str, source: str) -> tuple[bool, list[Issue]]: ...
def scan_antibodies(
    core: dict[str, object], documents: dict[str, str]
) -> tuple[dict[str, tuple[str, ...]], list[Issue]]: ...

# markdown.py
def extract_fenced_json(markdown: bytes, fence_kind: str) -> list[object]: ...
def validate_markdown_sync(
    root: Path, core: dict[str, object], ledger_path: Path | None
) -> list[Issue]: ...

# gitstate.py / manifest.py
def inspect_git_state(root: Path, base_commit: str) -> object: ...
def resolve_git_common_dir(root: Path) -> Path: ...
def validate_manifest(
    isolated_root: Path, canonical_root: Path, core: dict[str, object],
    phase: str, base_ref: str
) -> list[Issue]: ...
def freeze_manifest_value(
    isolated_root: Path, canonical_root: Path, core: dict[str, object],
    phase: str, base_ref: str, final: bool,
    finding_dispositions: list[dict[str, object]] | None = None
) -> dict[str, object]: ...

# review.py
def validate_review_attestations(
    core: dict[str, object], reviews: list[dict[str, object]],
    findings: list[dict[str, object]]
) -> list[Issue]: ...
def validate_review_history(core: dict[str, object]) -> list[Issue]: ...
def compute_review_subject_digest(target: dict[str, object]) -> str: ...
def build_review_target_value(
    root: Path, schema: dict[str, object], core: dict[str, object], *,
    phase: str, attempt_id: str, ledger_sections: list[dict[str, object]],
    semantic_diff_paths: list[str]
) -> dict[str, object]: ...
def build_validation_bundle_value(
    root: Path, schema: dict[str, object], core: dict[str, object], *,
    phase: str, attempt_id: str, review_target: dict[str, object],
    public_queue: dict[str, object] | None
) -> dict[str, object]: ...
def transition_core_value(
    core: dict[str, object], *, phase: str, stage: str,
    review_documents: list[bytes], abandon_reason: str | None = None
) -> dict[str, object]: ...

# orchestration.py
def validate_inputs(...) -> list[Issue]: ...

# rendering.py
@dataclass(frozen=True)
class RenderTransactionRequest:
    operation: str
    phase: str
    stage: str | None
    core_path: str
    output_path: str
    canonical_root: Path | None
    base_ref: str | None
    expected_head: str
    expected_core_sha256: str
    logic_review_input: Path | None = None
    btj_review_input: Path | None = None
    finding_dispositions_input: Path | None = None
    abandon_reason: str | None = None

def write_rendered_value(
    root: Path, *, request: RenderTransactionRequest
) -> None: ...
```

These declarations freeze names, inputs, and return families; Task 1 preserves
the pre-existing A0 signatures exactly. Exact record shapes, roles, states,
evidence laws, closure, and renderer operations come from the controlling
addendum and literal schema appendix. The Git-common-dir lock, durable
reservation, rollback journal, and atomic replace helpers are private; callers
cannot bypass operation/stage, CAS, allowed-path, protected-path, review-intake,
or overwrite policy with a public generic writer. `write_rendered_value`
reloads `request.core_path` while holding the shared lock and installs the
complete operation-specific multi-file transaction; no alternate positional or
six-argument call is public. Every transaction freezes its full raw-hash read
set and rechecks HEAD, core, and all inputs immediately before the first
repository replacement.

---

### Task 1: Extract A0 Behind an Import-Compatible Facade

**Files:**

- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/__init__.py`.
- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/diagnostics.py`.
- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/codec.py`.
- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/baseline.py`.
- Create `09_TOOLS/02_COMPILERS/test_kintsugi_schema.py` with only the initial
  compatibility-characterization class.
- Modify `09_TOOLS/02_COMPILERS/validate_kintsugi.py` into a thin facade.
- Do not modify `test_validate_kintsugi.py` or the baseline JSON.

- [ ] Add `CompatibilityExtractionTests` before creating the package. Assert
  that the package and facade expose the same A0 `Issue`, `BaselineResult`,
  `KintsugiError`, constants, codec functions, parser helpers,
  `compare_baseline`, `run_baseline`, and `run_process`; assert
  `validate_kintsugi.main()` retains the existing output and exit behavior.
- [ ] Capture the immutable hashes before editing:

  ```bash
  shasum -a 256 09_TOOLS/02_COMPILERS/test_validate_kintsugi.py \
    09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json
  ```

  Save the two observed hashes in the new compatibility test so later tasks
  detect any edit to those files.
- [ ] Run the new test before creating `kintsugi_kernel/`:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  ```

  **Expected RED:** import failure for `kintsugi_kernel`; no repository file is
  written.
- [ ] Move, without semantic edits, the dataclasses/exception into
  `diagnostics.py`, canonical JSON/hash/path/loading primitives into
  `codec.py`, and all A0 pytest-contract/runner behavior into `baseline.py`.
  Re-export the original A0 public names through `kintsugi_kernel.__init__` and
  `validate_kintsugi.py`. Keep the facade's parser, diagnostic emission, and
  `main()` thin; keep the exact A0 flag defaults and output bytes.
- [ ] Run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
    --check-baseline \
    --canonical-root /Users/Yves/Documents/01_EMERGENTISM
  ```

  **Expected GREEN:** the original 22 tests pass unchanged; compatibility
  tests pass; the last command exits 0, prints exactly
  `KIN-OK baseline collected=19 failures=5` plus one LF on stdout, and prints
  nothing to stderr.
- [ ] Confirm the extraction tests are GREEN and create the path-limited
  implementation commit:

  ```text
  refactor(kintsugi): extract the A0 compatibility kernel
  ```

---

### Task 2: Add the Normative Schema and Restricted Evaluator

**Files:**

- Create `03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json` from the
  literal appendix in this plan.
- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/schema.py`.
- Create `09_TOOLS/02_COMPILERS/kintsugi_test_support.py`.
- Extend `09_TOOLS/02_COMPILERS/test_kintsugi_schema.py`.
- Export schema functions through `kintsugi_kernel/__init__.py` and the facade.

- [ ] Before implementation, extract the already-frozen appendix from this
  plan. Assert it is exactly one JSON line plus LF, parses, carries the exact
  schema ID, has no placeholder or marker text, and equals its own canonical
  JSON bytes. Apply those exact appendix bytes to
  `02_KINTSUGI_SCHEMA.json`; then assert the checked-in artifact and appendix
  are byte-identical. Do not regenerate or reinterpret the schema during
  extraction.
- [ ] In `kintsugi_test_support.py`, add fresh builders for one structurally
  complete valid `coreData`, `publicQueue`, and preserved A0
  `baselineAllowlist`. Builders return deep copies, use deterministic IDs and
  hashes, and never read the live core, owners, or public tree.
- [ ] Add tests for: exact schema `$id`; canonical bytes; exactly three
  CLI-selectable roles (`coreData`, `publicQueue`, `baselineAllowlist`) while
  permitting named nested `$defs`; local refs only; declared-keyword closure;
  unresolved refs and unknown schema keywords failing closed; every object
  rejecting extra properties; booleans rejected as integers; `oneOf` requiring
  exactly one branch; no coercion; schema/instance totality over malformed
  shapes; and all three complete synthetic roots validating.
- [ ] Add focused tests that the schema requires the current pre-v1 fields and
  tagged unions: typed-term register, premise role, claim support/upgrade/kill/
  survivor/authority fields, seam prior/current mirrors and conditional
  `upgradeEvidenceLinkIds`, seven Phase-A `requiredClaimBindings`, empty B/C
  bindings, typed `ownerSearchEvidence`, `mutationLevel`, authority mechanism,
  all eight closed semantic payload definitions, and all review/bundle records.
  Assert that `coreData` requires exactly the five persisted review-history
  collections (`reviewAttempts`, `reviewAttemptArtifacts`,
  `reviewAttestations`, `reviewFindings`, and
  `reviewFindingDispositions`); that `validationBundle` repeats all five; and
  that `reviewTarget` carries `currentAttemptId`, `receiptId`,
  `receiptNarrativeRawSha256`, `reviewSubjectDigest`,
  `ledgerPreambleRawSha256`, plus the five complete prior-history lists; and
  that `validationBundle` repeats both narrative hashes. Add
  negative searches for stale
  `requiredClaimIds`, source-based support links, free-text kill criteria, and
  an exact-three-`$defs` assumption.
- [ ] Validate positive and one-field-negative instances of
  `reviewAttempt`, `reviewAttemptArtifact`, `reviewAttestation`,
  `reviewFinding`, `reviewProcessEvidence`, `reviewFindingDisposition`, and
  `reviewFindingDispositionInput` directly through local
  `$ref`s. Cover canonical attempt-ID shape; PENDING zero/one IDs; FAILED one
  or two IDs; PASSED both IDs; ABANDONED zero/one/two IDs plus reason; FAIL
  non-empty finding/open-severe lists; PASS empty open-severe list; and all
  three disposition tagged unions (`ADDRESSED`, `DISPUTED`,
  `PROCESS_INVALID`); the five typed finding/disposition endpoint lists; and
  hash-bound process-evidence files. Structural schema tests do not substitute
  for Task 3's cross-record exactness checks.
- [ ] Add structural cardinality tests for the honest bootstrap boundary. The
  `coreData` schema must permit `coreData.trials=[]`,
  `manifest.trialedClaimIds=[]`, and `phaseReceipt.trialIds=[]` because the
  schema alone cannot see the CLI bootstrap context. The named `reviewTarget`
  and `validationBundle` definitions must still require non-empty `trials`
  arrays; review and bundle artifacts can never represent a pre-trial vessel.
  The schema permits both empty and non-empty `manifest.finalFiles`; Task 3/5
  enforce the pre-review-DRAFT versus review-ready-DRAFT status law. It also
  permits `manifest.closureOnlyPaths=[]` for the honest no-attempt bootstrap;
  Task 3/5 require the exact derived attempt-path union everywhere else. Prove
  all positive/negative shapes directly through their local `$ref`s.
- [ ] Run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  ```

  **Expected RED:** missing `schema.py`, missing schema artifact, or unhandled
  schema assertions; never an uncontrolled traceback.
- [ ] Implement only the keyword registry frozen by the design/addendum:
  `$schema`, `$id`, `$defs`, `$ref`, `type`, `required`, `properties`,
  `additionalProperties`, `enum`, `pattern`, `minimum`, `minLength`,
  `maxLength`, `minItems`, `maxItems`, `items`, `uniqueItems`, `const`, `allOf`,
  `anyOf`, `oneOf`, `if`, `then`, `else`. `maxLength` is the narrow Golden
  Seam repair that makes the appendix's `maxLength: 256` REGEX bound executable;
  it licenses no other vocabulary expansion. Resolve local JSON Pointers,
  validate schema vocabulary before instances, use `type(value) is int`, never
  coerce/default, and sort all issues by `(path, code, message)`.
- [ ] Implement `validate_named_definition` for closed nested payload,
  attestation, review-target, receipt-descriptor, and bundle definitions. Keep
  `validate_schema_instance` hard-gated to exactly `coreData`, `publicQueue`,
  and `baselineAllowlist`; tests must prove a valid nested definition cannot be
  selected as a fourth CLI root role.
- [ ] Run the focused schema test and then the unchanged A0 tests:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
  ```

  **Expected GREEN:** every schema case passes, all three synthetic roots
  validate with no issues, every closed nested definition validates through the
  internal function without becoming a CLI role, every single-field shape
  mutation receives `KIN-E-SCHEMA` or `KIN-E-SCHEMA-KEYWORD`, and all 22 A0
  tests remain green.
- [ ] Commit:

  ```text
  feat(kintsugi): add the normative v1 schema engine
  ```

---

### Task 3: Close Graph, State, Evidence, Justice, and Rosetta Semantics

**Files:**

- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/records.py`.
- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/semantics.py`.
- Create `09_TOOLS/02_COMPILERS/test_kintsugi_records.py`.
- Create `09_TOOLS/02_COMPILERS/test_kintsugi_semantics.py`.
- Extend `09_TOOLS/02_COMPILERS/kintsugi_test_support.py`.
- Update package exports only as needed.

- [ ] Add table-driven record tests for malformed/global duplicate IDs;
  wrong-kind/dangling refs; source-kind/authority-role matrix; provenance used
  as owner, dependency, or warrant; claim dependency cycles, support cycles,
  and mixed dependency/support cycles; duplicate/self support; survivor
  self-reference/transitive dependence; normative claim without a normative
  premise/dependency; verdict matrix; trial/discriminator/seam state laws;
  receipt identity/phase order; fixture cardinalities; ownerless queue law;
  Phase-A binding exactness/fingerprint/unique-claim rules; and B/C empty
  bindings. Include the five review-history collections in global-ID and
  reference indexing: attempt/artifact exact bijection, root-to-leaf ordering,
  canonical `RVA-{phase}-{str(n).zfill(3)}` round-trip spelling, phase/receipt
  agreement, acyclic supersession, one leaf per `(phase, receiptId)` chain,
  PASSED terminality, attestation/finding/disposition exact resolution, and no
  orphaned history record. Resolve finding/disposition `claimIds`, `seamIds`,
  `ledgerSectionIds`, `receiptIds`, and `subjectPaths` by their typed roles;
  reserve `LEDGER-PREAMBLE` only for the preamble projection and reject it as
  an ordinary global record ID.
- [ ] Test and enforce typed-term uniqueness by the semantic pair
  `(symbol, semanticRegister)`. Reusing a symbol in a different register is a
  distinct typed term; duplicating the same pair fails even when its prose
  definition or declared type differs.
- [ ] Add an explicit modal-force table covering all six modalities (`ACTUAL`,
  `POSSIBLE`, `NECESSARY`, `NORMATIVE`, `DEFINITIONAL`, `CONJECTURAL`). For each
  modality, include a positive that preserves its declared force and a negative
  unmarked substitution. No support link, Rosetta edge, authority record,
  receipt, repetition, or lifecycle change may lift or replace modality; a
  cross-modal conclusion requires an explicit typed entailing premise or
  dependency rather than an invented modality ordering.
- [ ] Add evidence tests for strength ordering; link ceiling bounded by the
  supporting claim; analogy/Rosetta fixed at `I`/`NOT_APPLICABLE`; no automatic
  aggregation; qualifying independent active, closed, admissible trials;
  prospective upgrade criterion; actual upgrade requiring non-empty qualifying
  link IDs; `A` requiring sourced `[A]` plus `VALID_SOUND`; receipt transport
  not replacing warrant; kill `ACTIVE`/`DEFERRED` field laws; strict kill-driven
  downgrade targets; RETRACT at `C`; retired/NONE lifecycle rule; and exact
  prior/current seam contract synchronization.
- [ ] Add an exhaustive bidirectional `repairKind=RETIER` table over the strict
  evidence order `C < I < S < A`: all six upward pairs (`C->I`, `C->S`,
  `C->A`, `I->S`, `I->A`, `S->A`) pass only when the prior upgrade criterion
  and non-empty qualifying upgrade-evidence links are satisfied; all six
  downward pairs (`A->S`, `A->I`, `A->C`, `S->I`, `S->C`, `I->C`) pass only
  when authorized by the prior kill criterion. Every equal-tier RETIER fails,
  and every non-RETIER repair kind fails if it changes strength. A
  `RETRACTED` seam instead preserves strength, sets lifecycle to `RETIRED`, and
  synchronizes a retired claim; it never masquerades as a RETIER.
- [ ] Add bootstrap semantic tests around the schema's deliberately permissive
  empty arrays. The only accepted empty-trial vessel is explicit
  `phase=A`, `bootstrap=True`, with DRAFT `REC-A-108`, non-empty claims and
  harvested requirement bindings, `coreData.trials=[]`,
  `MAN-A-001.trialedClaimIds=[]`, `trialedClaimCount=0`,
  `REC-A-108.trialIds=[]`, `MAN-A-001.finalFiles=[]`, and
  `finalFileCount=0`, with `MAN-A-001.closureOnlyPaths=[]`. Reject the same
  vessel for bare/non-bootstrap validation,
  Phase B, Phase C, or any COMPLETE/VERIFIED receipt. For every receipt, enforce
  the attempt-sensitive biconditional: `reviewAttemptId=null` exactly for a
  pre-review DRAFT, with empty `finalFiles`/zero count; allocation makes it
  non-null forever, and a non-null current PENDING attempt requires
  the final-file path set to equal the included-file path set, the count to
  equal its length, and every final hash to cover the current reviewed bytes.
  COMPLETE and VERIFIED retain that same frozen final-snapshot law.
  Independently require `closureOnlyPaths` to equal the empty union when the
  selected phase has no attempt and otherwise the exact four-derived-path union
  for every declared attempt in that phase; no non-bootstrap attempt chain may
  use the bootstrap emptiness exception.
- [ ] Add cross-record gate tests. Before review, every gate is PENDING with a
  null reviewer path. Every seam cited by a DRAFT receipt must retain PENDING
  core gates; neither PASS nor FAIL is legal in the DRAFT core. COMPLETE and
  VERIFIED receipts require every terminal cited gate to be PASS; Truth's
  reviewer path equals the LOGIC receipt review path, while Beauty and Justice
  paths equal the BTJ receipt review path. Apply the same core-state rule to
  VERIFIED seams and to proposed-versus-terminal RETRACTED seams through their
  referencing receipt state. Immutable PASS/FAIL attestation behavior belongs
  to Task 7, after the review interface exists.
- [ ] Add Justice/authority tests for all five authority effects and four
  scopes/regimes: `NONE`; descriptive historical retirement; active/DRAFT
  public K2 refusal; private consequential K2; public discretionary/
  consequential PRISM; public constitutional auto-enforcement; OTHER/OTHER;
  required Justice context on every non-NONE effect; and the rule that
  authorization never changes validity, soundness, modality, or evidence.
- [ ] For `authorityEffect=NONE`, test the canonical absent-context
  representation with `authorityScope=NONE`. When collective/normative Justice
  scope independently requires a context, require its authority to be exactly
  `NOT_APPLICABLE`/`NONE`; reject a fabricated operative regime or mechanism in
  either representation.
- [ ] Test `validate_public_queue(queue, core)` as a pure cross-record
  validator: manifest/source/receipt resolution, complete owner search, OWNED
  and OWNERLESS tagged unions, disposition restrictions, candidate membership,
  and exact fence-independent queue semantics. It returns issues and never
  reads Markdown, Git, or the live public tree.
- [ ] Add exact execution/dispatch tests for `evaluate_antibody_fixture` and
  `scan_antibodies`: `LITERAL` exact Unicode substring membership; `REGEX`
  through `safeRegexSearch`, never Python's backtracking `re` engine; strict
  UTF-8 with no Unicode normalization; and invalid regex. Test the complete
  grammar, anchors, Unicode scalar ranges, escapes, size/state ceilings, and
  deterministic Thompson epsilon-NFA state-set evaluation. Include a long
  near-match for `(a+)+$` that completes within the linear work bound and a
  malformed/oversize corpus that fails `KIN-E-FIXTURE`. Implement the
  addendum's anchored,
  segment-aware safe glob grammar rather than `fnmatch`: absolute paths,
  backslashes, empty/dot/dot-dot segments, `?`, character classes, and escapes
  are invalid; `**` is legal only as a whole segment and spans zero or more
  segments; `*` stays within one segment and never matches `/`. Scope and
  exclude inventories are independently sorted before subtraction. Test exact
  expected trigger-ID sets and POSITIVE, NEGATIVE, QUOTATION, and HISTORICAL
  fixture dispatch. Live source scans do not infer quotation spans: a text
  match remains visible unless its entire path is lawfully excluded. Every
  fixture declared by an antibody executes exactly once.
- [ ] Exercise positive and negative rows for all eight semantic evaluators and
  their exact schema payload definitions: `VERDICT_MATRIX`, `JUSTICE_CONTEXT`,
  `RECEIPT_ROLE`, `REGISTER_INDEX`, `QUANTUM_MEASURE`, `OPTION_CONE`,
  `TROPHIC_AGGREGATOR`, and `ROSETTA_TRANSFER`. For Rosetta, require
  `VOCABULARY`, `QUESTION`, and `TOPOLOGY` to pass as correspondence only and
  require `ENTAILMENT`, `MECHANISM`, `NECESSITY`, and `EVIDENCE_UPGRADE` to fail
  even when a bridge ID resolves. Cover the addendum's exact
  `verdictMatrixPayload`, `justiceContextPayload`, `receiptRolePayload`,
  `registerIndexPayload`, `quantumMeasurePayload`, `optionConePayload`,
  `trophicAggregatorPayload`, and `rosettaTransferPayload` predicates. In
  particular, sampling a normalization scalar fails, physical-light-cone
  widening fails, literal trophic-energy law fails, and an Egregoreotype is
  only a candidate when proxy/trace/turnover/reweighting predicates all hold.
  Payload booleans and enums are declarations to test, never empirical warrant.
- [ ] Run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_records.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_semantics.py' -v
  ```

  **Expected RED:** the schema-valid negative vessels return no semantic issue,
  or the new modules are absent.
- [ ] Implement typed collection indexes and validate duplicates before edges.
  Check all reference kinds explicitly. Detect cycles over the union graph with
  deterministic three-color DFS and a canonical lexicographic cycle display.
  Keep evidence, provenance, lifecycle, authorization, modality, and formal
  verdict axes independent. Implement `validate_public_queue`,
  `evaluate_antibody_fixture`, and `scan_antibodies` as pure functions. Use
  closed dispatcher tables for state, verdict, authority, every match mode,
  every fixture context, all eight semantic evaluators, and every review
  history record kind. Compile only the frozen safe glob grammar and bounded
  `safeRegexSearch` grammar; execute regexes as Thompson NFA state sets. Do not infer
  scientific persuasiveness, quotation boundaries in live documents, or moral
  truth.
- [ ] Run both focused modules and the schema module:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_records.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_semantics.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  ```

  **Expected GREEN:** the complete synthetic vessel has zero issues; each
  one-law negative produces its declared stable primary code (`KIN-E-ID`,
  `KIN-E-REF`, `KIN-E-CYCLE`, `KIN-E-VERDICT`, `KIN-E-STATE`,
  `KIN-E-JUSTICE`, `KIN-E-RECEIPT`, `KIN-E-FIXTURE`, or `KIN-E-QUEUE`) in stable
  order; no test relies on source repetition or authority as proof.
- [ ] Commit:

  ```text
  feat(kintsugi): close graph and semantic invariants
  ```

---

### Task 4: Synchronize Markdown, Quotes, and Machine Records

**Files:**

- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/markdown.py`.
- Create `09_TOOLS/02_COMPILERS/test_kintsugi_markdown.py`.
- Extend `09_TOOLS/02_COMPILERS/kintsugi_test_support.py` with temporary
  Markdown/owner builders.
- Update package exports only as needed.

- [ ] Add byte-oriented tests for exactly one `json kintsugi-seam` fence per
  `## KIN-...` ledger section; exactly one `json kintsugi-receipt` in each
  synthetic receipt; exactly one `json kintsugi-review` in each review; and
  exactly one `json kintsugi-public-queue` in the synthetic Phase C queue
  Markdown. Test malformed JSON, unterminated fences, wrong labels, duplicates,
  missing records, extra records, deep-equality drift, duplicate headings,
  UTF-8 failure, CRLF, and deterministic issue order.
- [ ] Add exact-byte section tests: a seam section starts at its `## KIN-...`
  heading and ends immediately before the next such heading or EOF;
  `narrativeRawSha256` changes for any narrative-byte change but is insensitive
  to any unrelated section. For every two-sided seam/receipt narrative, hash
  exactly `UTF8("KINTSUGI-NARRATIVE-V1") || 0x00 ||
  uint64be(len(prefix)) || prefix || uint64be(len(suffix)) || suffix`, with raw
  byte lengths and overflow refusal. Exclude the fence opener, JSON bytes,
  closer, and fence-boundary newlines. Move identical prose from one fence side
  to the other and require a different digest, proving the framing prevents
  concatenation ambiguity. Fence records compare parsed deep equality, while
  narrative hashes remain raw-byte hashes.
- [ ] Add ledger-preamble and receipt-narrative tests.
  `ledgerPreambleRawSha256` hashes the exact bytes from offset zero through the
  byte before the first seam heading, using the empty-byte SHA-256 when absent.
  `receiptNarrativeRawSha256` hashes the exact UTF-8 bytes before and after the
  unique receipt fence through the same framed prefix/suffix function. Change
  every byte class around each fence/heading and prove the expected hash
  changes; relocate bytes across a fence and prove the digest changes even when
  raw concatenation would be identical; change only
  mechanical JSON fence fields and prove the narrative hashes do not. Reject
  dynamic status prose outside a receipt fence after target freeze.
- [ ] Change only mechanical gate/status/reviewer-path bytes in a synchronized
  core record and its seam fence. Prove the extracted narrative bytes and
  `narrativeRawSha256` remain identical. Preserve the resulting semantic-section
  input as a characterization used by Task 7 to prove review-target stability.
- [ ] Add owner synchronization tests: declared owner path is safe and exists;
  `beforeHash`/`triedHash` use LF-normalized text hashes; `afterQuote` appears
  exactly once; owner source raw hash matches; owner anchor is present; and no
  Markdown parser ever rewrites a file.
- [ ] Run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_markdown.py' -v
  ```

  **Expected RED:** missing parser/synchronizer or missing diagnostics for at
  least one malformed fence/quote case.
- [ ] Implement line-start fence recognition on raw bytes, strict UTF-8 and
  standard-library JSON parsing, preserved byte offsets, exact section bounds,
  role-specific record lookup, deep equality, and owner quote/hash checks.
  Report malformed fenced JSON as `KIN-E-JSON`, record/fence drift as
  `KIN-E-LEDGER`, and owner mismatch as `KIN-E-QUOTE`. Never normalize bytes
  for raw section/source hashes. Fence bytes are synchronization evidence, not
  part of the narrative hash domain. Return the ledger preamble projection and
  typed receipt narrative projection alongside seam sections so Task 7 can bind
  them without reparsing or normalizing bytes.
- [ ] Run the focused test plus prior record tests:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_markdown.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_records.py' -v
  ```

  **Expected GREEN:** all valid synthetic Markdown/owner records synchronize,
  every single drift is detected with deterministic offsets/codes, and file
  hashes before and after validation are identical.
- [ ] Commit:

  ```text
  feat(kintsugi): synchronize Markdown and owner records
  ```

---

### Task 5: Enforce Git, Manifest, Concurrency, and Protected-Tree Closure

**Files:**

- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/gitstate.py`.
- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/manifest.py`.
- Create `09_TOOLS/02_COMPILERS/test_kintsugi_manifest.py`.
- Extend `09_TOOLS/02_COMPILERS/kintsugi_test_support.py` with a temporary Git
  repository/worktree factory.
- Update package exports only as needed.

- [ ] Build every test repository from synthetic bytes: a `main` checkout, one
  isolated worktree, two owner/support files, representative protected public/
  archive/compat files, a symlink, pre-existing untracked bytes, and a base
  commit. Never initialize a Git repository inside the real worktree.
- [ ] Add partition/count tests for candidate/included/excluded and
  harvested/trialed/excluded sets, pre-review-DRAFT empty `finalFiles`,
  review-ready-DRAFT/COMPLETE/VERIFIED final coverage, trial coverage,
  candidate-membership subset, discovery/parser rules, base-blob hashes, exact
  current final hashes, `FULL_FILE` and `EXACT_SPAN` provenance, recursive
  protected snapshots, allowed change/closure paths, and byte-proven
  subtraction of pre-existing untracked files. For a non-null current attempt,
  `freeze-manifest --final` must set `finalFiles.path == includedFiles.path`,
  exact count equality, and hashes over the bytes actually subjected to
  review; a stale current hash fails before a target can be rendered.
- [ ] Add reserved typed-control-artifact tests. Before discovery counts, remove
  the exact core JSON, semantic ledger, canonical selected phase-receipt path,
  and every current/prior attempt target/review/bundle path from manifest
  `candidateFiles`, `includedFiles`, `finalFiles`, and `excludedPaths`, even
  when an include glob selects them. They remain allowed changes; only derived
  attempt paths are closure-only. Prove the core/ledger/receipt never receive a
  raw self/final hash and are instead completely bound by target core semantics,
  ledger preamble/section/seam projections, receipt narrative/descriptor,
  attempt artifact hashes, and final bundle history. Reject a missing reserved
  path, a control path disguised as an exclusion/source, or any raw self-hash
  reintroduction.
- [ ] Test `closureOnlyPaths` as the exact union of four paths derived from
  every declared review attempt in the selected phase, with no caller-selected
  additions or omissions. For each canonical attempt ID `{id}`, derive only:

  ```text
  09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{id}/review_target.json
  11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{id}_LOGIC.md
  11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS/{id}_BTJ.md
  09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/{id}/validation_bundle.json
  ```

  Require the union to be a subset of `allowedChangePaths`. Add one-field
  negatives for phase/role swaps, omissions, additions, fixed legacy paths,
  and attempts to hide an owner, protocol, schema, test, core, semantic ledger,
  receipt, public queue, or any other semantic path as closure-only; fail
  before semantic diff paths are computed.
- [ ] Add frozen-requirement tests for all seven Phase-A binding IDs, exact
  owner path/anchor/base quote fingerprints from the addendum, unique bound
  claims, bound source/claim/trial agreement, and empty B/C bindings.
- [ ] Add Git-state negatives for committed, staged, unstaged, renamed, deleted,
  and untracked scope escape; NUL-delimited Git output containing valid
  newline-bearing and tab-bearing filenames; canonical HEAD movement; wrong
  branch/common directory/worktree; explicit ref not resolving to manifest
  base; `MANIFEST` mismatch; candidate owner dirt; protected tracked/untracked
  drift in either root; symlink-target drift; and special-file refusal.
- [ ] Add attempt-allocation and concurrency tests with two linked synthetic
  worktrees sharing one `git rev-parse --git-common-dir`. Require canonical ID
  round-trip and the smallest unused positive `n` after scanning core records,
  derived worktree paths, the current tree, reachable history, and durable
  reservations. Under an exclusive-create `.kintsugi-transition.lock`, create
  exactly one canonical
  `kintsugi-attempt-reservations/{id}.json` containing ID, phase, receipt,
  expected HEAD, and expected raw core hash. Check caller-supplied HEAD/core
  expectations both before and inside the lock. Test concurrent allocators,
  burned reservations after failure, collisions, malformed/stale reservation,
  stale HEAD, stale core hash, crash-residue lock refusal, and `finally` lock
  cleanup. Never steal or time-expire a lock and never reuse a reserved ID.
- [ ] Add predecessor immutability tests. A successor may allocate only from
  the unique FAILED/ABANDONED leaf in its `(phase, receiptId)` chain after that
  predecessor's terminal core/receipt fence, target if present, every extant
  review, and recorded artifact hashes are committed exactly at current HEAD.
  Reject an uncommitted predecessor, rewritten terminal bytes, missing hash,
  PASSED predecessor, second chain leaf, or reachable-history collision.
- [ ] Run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_manifest.py' -v
  ```

  **Expected RED:** missing Git/manifest modules or at least one scope/protected
  mutation passes.
- [ ] Implement Git subprocess calls with explicit argv, `-z` output, and NUL
  parsing; never parse human-formatted status. Resolve the selected base to one
  full commit and require agreement with the manifest. Enumerate protected
  trees with `os.scandir`, hash regular file bytes and symlink target bytes,
  reject special files, and compare both isolated and canonical inventories.
  Resolve the Git common directory explicitly, implement lock/reservation and
  HEAD/core compare-and-swap as fail-closed helpers, and enumerate current plus
  reachable Git paths without parsing human-formatted output.
  `freeze_manifest_value` returns a candidate value only; it performs no write.
  Task 7 is the sole caller that installs a frozen value transactionally.
- [ ] Run the focused manifest test twice to expose hidden nondeterminism, then
  the prior schema/record tests:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_manifest.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_manifest.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_records.py' -v
  ```

  **Expected GREEN:** valid synthetic repositories pass twice with identical
  values; every one-path/state mutation emits `KIN-E-MANIFEST`, `KIN-E-SCOPE`,
  `KIN-E-PROTECTED`, or `KIN-E-CONCURRENT`; neither checkout changes.
- [ ] Commit:

  ```text
  feat(kintsugi): enforce manifest and Git scope closure
  ```

---

### Task 6: Orchestrate the Read-Only Validator and A0B CLI

**Files:**

- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/orchestration.py`.
- Modify `09_TOOLS/02_COMPILERS/validate_kintsugi.py` without changing its A0
  re-exports or A0 execution path.
- Extend `09_TOOLS/02_COMPILERS/test_kintsugi_schema.py` and
  `09_TOOLS/02_COMPILERS/test_kintsugi_records.py` with orchestration/CLI tests.
- Update package exports only as needed.

- [ ] Add CLI tests for mutually exclusive `--check`/`--check-baseline`; the
  A0 alias pair; `--phase {A,B,C}`; `--bootstrap`; `--base-ref`; `--data`;
  `--schema`; `--ledger`; `--public-queue`; `--baseline-allowlist`; and
  `--canonical-root`. Require phase to have a base ref and an absolute
  canonical root, bootstrap to be Phase A only, and baseline mode to reject
  phase/bootstrap/check inputs.
- [ ] Add orchestration tests proving the order is schema load/validation,
  canonical instance validation, record semantics, Markdown sync, manifest/
  Git checks when a phase is selected, public queue only for Phase C or an
  explicit input, and phase/receipt-state checks that do not require review or
  bundle machinery. One malformed stage must prevent downstream evaluation
  without masking its primary issue. Task 7 extends orchestration with verified
  review-attestation and validation-bundle checks after those interfaces exist.
- [ ] Add totality and I/O tests: missing default live core is a controlled exit
  2 `KIN-E-IO` (A1 has not created it); synthetic semantic failure is exit 1
  with empty stdout; success is exit 0 with exactly one deterministic `KIN-OK`
  line; argument failure is exit 2 with path slot `CLI`; no traceback; running
  from another CWD resolves defaults from the compiler root; no input or Git
  file changes.
- [ ] Run the affected tests before implementation:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_records.py' -v
  ```

  **Expected RED:** `--check` is rejected by the A0-only parser and/or the
  orchestration module is absent.
- [ ] Implement `validate_inputs` as a read-only coordinator over lower layers.
  It returns sorted issues and never catches/rewrites semantic meaning. Extend
  the facade parser and output adapter while keeping `run_baseline` untouched.
  Resolve only repository-relative `--data`, `--schema`, `--ledger`,
  `--public-queue`, `--baseline-allowlist`, and `--contract` values through
  `safe_repo_path`; do not create missing defaults. Validate the absolute
  `--canonical-root` separately through strict path resolution and Git
  worktree/common-directory checks. `--contract` and
  `--baseline-allowlist` must resolve to one value or fail on conflict.
- [ ] Run the two focused modules, unchanged A0 tests, and the real baseline:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_records.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
  python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
    --check-baseline \
    --canonical-root /Users/Yves/Documents/01_EMERGENTISM
  ```

  **Expected GREEN:** synthetic full checks behave exactly as declared; the
  absent live core fails honestly without a write; all A0 tests pass; and the
  real baseline output remains byte-exact.
- [ ] Commit:

  ```text
  feat(kintsugi): expose read-only A0B validation
  ```

---

### Task 7: Render Retry-Safe Review Attempts and Atomic Closure

**Files:**

- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/review.py`.
- Create `09_TOOLS/02_COMPILERS/kintsugi_kernel/rendering.py`.
- Create `09_TOOLS/02_COMPILERS/render_kintsugi.py`.
- Create `09_TOOLS/02_COMPILERS/test_kintsugi_review.py`.
- Create `09_TOOLS/02_COMPILERS/test_render_kintsugi.py`.
- Extend `09_TOOLS/02_COMPILERS/kintsugi_test_support.py` with review and
  renderer fixtures.
- Update package exports only as needed.

- [ ] Add pure review-target tests for the exact schema shape: typed
  `currentAttemptId`, `receiptId`, `receiptNarrativeRawSha256`,
  `reviewSubjectDigest`, semantic manifest projection, receipt-fence omission,
  `ledgerPreambleRawSha256`, declared sorting only, exact ledger semantic
  sections, semantic diff paths, schema hash, and transitive closure
  across receipt claims, dependencies, support targets, survivor targets, and
  Rosetta target/bridge endpoints. The five `priorReview*` lists contain the
  complete terminal ancestor chain, matching artifacts, every extant
  attestation/finding, and every disposition in root-to-leaf order; they are
  empty on the first attempt and exclude the current PENDING attempt. Include
  valid dependency-receipt closure and negatives for omitted, reordered,
  orphaned, dangling, or cyclic closure.
- [ ] Prove the target and bundle close the reserved control-artifact gap. The
  target binds typed core semantics, the ledger preamble plus every section's
  narrative/seam projection, and receipt narrative bytes outside its fence;
  attempt artifacts bind target/review bytes; the bundle binds complete typed
  records, raw final ledger sections, receipt descriptor/narrative, and full
  history. Recompute live preamble/receipt hashes at closure and reject any
  unbound or changed control byte even though control paths are absent from the
  manifest's candidate/included/final/excluded inventories.
- [ ] Add review-subject digest tests. Hash canonical target semantics after
  removing `currentAttemptId`, `reviewSubjectDigest`, and all five
  `priorReview*` fields; retain `receiptId`; normalize attempt mechanics by
  setting manifest `closureOnlyPaths=[]`, filtering all derived attempt paths
  from `allowedChangePaths`, and retaining no closure-file hash records. A new
  attempt number/history/path alone preserves the digest; an owner, claim,
  seam, trial, propagation, ledger semantic section, schema, or other reviewed
  semantic change alters it. The full review-target raw hash remains the digest
  signed by attestations and stored at completion.
- [ ] Add review-Markdown and transactional-ingestion tests. Each review has
  exactly one `json kintsugi-review` fence and one
  `json kintsugi-review-findings` fence; sorted finding IDs deep-equal the
  attestation, and every finding's attempt/kind matches its enclosing review.
  The raw artifact hash covers both fences and intervening bytes. Newly
  authored bytes are accepted only from optional `--logic-review-input` and
  `--btj-review-input` paths outside the canonical repository, only for a kind
  not yet recorded, and only when the parsed attempt/path/kind equal the
  derived current attempt. Validate the complete prospective state before
  staging the canonical review plus core/artifact/finding/receipt updates, and
  test all-or-nothing install/rollback. An unrecorded canonical review file or
  any direct overwrite fails closed.
- [ ] Add `validate_review_attestations` tests for distinct LOGIC/BTJ reviewer
  identities, one immutable target digest, exact derived paths/IDs, and both
  PASS/FAIL outcomes. FAIL requires non-empty `findingIds` and
  `openSevereFindingIds`, with the latter exactly the referenced
  CRITICAL/MAJOR set. PASS has no open severe finding and may name only MINOR
  findings. LOGIC alone owns Truth/evidence upgrades; BTJ alone owns Beauty/
  Justice; authorization never upgrades evidence. A FAIL remains immutable,
  keeps the DRAFT candidate gates PENDING/null, and blocks completion.
- [ ] Add anti-reviewer-shopping and successor-transaction tests.
  `freeze-manifest --final --finding-dispositions-input <external-json>` accepts
  an absent/empty sorted array only for the first attempt; otherwise it requires
  exactly one `reviewFindingDispositionInput` per direct-predecessor finding.
  Under the shared lock, reserve the successor ID, expand deterministic
  `RFD-{successorId}-{ordinal}` records, and prospectively validate successor,
  dispositions, final manifest, receipt pointer, subject digest, and core graph
  together before writing. Failure burns the reservation but leaves no dangling
  record. `ADDRESSED` requires at least one changed claim, seam,
  ledger-section/`LEDGER-PREAMBLE`, receipt, or non-control final-source path
  endpoint and empty discriminator/evidence-file lists. `DISPUTED` requires a
  resolving discriminator and empty evidence files. `PROCESS_INVALID` requires
  one or more `reviewProcessEvidence {path,sha256}` records, empty semantic
  endpoint/discriminator lists, and exact immutable predecessor artifact or
  successor regular-final-file bytes. ADDRESSED/DISPUTED changes the subject
  digest; same-subject retry requires every disposition PROCESS_INVALID.
  Preserve every ancestor finding/disposition/evidence hash in later targets
  and the final bundle.
- [ ] Add exact state-machine tests for `TARGET_READY`, `ATTESTED`, `FAILED`,
  `ABANDONED`, `COMPLETE`, and `VERIFIED`. PENDING has zero or one PASS
  attestation and null reason; FAILED has one/two reviews with at least one
  FAIL/open-severe set; ABANDONED has zero/one/two preserved reviews and a
  reason; PASSED has two independent PASS reviews and can arise only atomically
  with DRAFT -> COMPLETE. COMPLETE changes only reviewed `REPAIRED ->
  VERIFIED`, owned terminal gates/reviewer paths, current attempt/artifact/
  attestation/finding state, and typed receipt closure fields. VERIFIED changes
  only receipt status/bundle path/bundle digest plus the atomic bundle install.
  Mutate owner, quote, evidence, narrative, collection, unowned gate, seam, or
  any extra receipt/attempt field one at a time and require `KIN-E-STATE`.
- [ ] Starting from Task 4's characterization, change only the synchronized
  core/fence mechanical status, gate, and reviewer-path bytes. Prove fence bytes
  remain excluded from `narrativeRawSha256` and the complete review target is
  byte-identical until an allowed semantic field changes.
- [ ] Test the state/path/hash biconditionals and reject every unreferenced
  closure file:

  ```text
  PENDING                    target optional; 0/1 PASS review; bundle absent
  FAILED                     target + all recorded reviews present; bundle absent
  PASSED + receipt COMPLETE target + both reviews present; bundle absent
  PASSED + receipt VERIFIED target + both reviews + bundle present
  ABANDONED                  target/reviews exactly as recorded; bundle absent
  ```

  Target existence exactly follows `reviewTargetSha256`; each review exists
  exactly when both its attestation ID and artifact hash are non-null; all
  extant files hash exactly to records and every review names the exact target
  digest. Reject hidden partial review bytes, a bundle for PENDING/FAILED/
  ABANDONED/COMPLETE, stale prior bundles, or any extra closure file.
- [ ] Add renderer tests for all four operations (`freeze-manifest`,
  `review-target`, `bundle`, `transition-core`): CWD-independent discovery,
  repository-relative explicit safe output, allowed-change membership,
  protected/escape refusal, same-directory temporary file, `os.replace`, temp
  cleanup, canonical bytes, deterministic rerun, input preservation on failure,
  review-target identical reuse/drift refusal, bundle no-overwrite, final-owner
  closed-trial/seam gate, and no owner prose edit. Every mutating invocation
  requires `--expected-head` and `--expected-core-sha256`, obtains the shared
  Git-common-directory lock, and repeats both compare-and-swap checks while
  locked. Only `freeze-manifest --final` creates a durable attempt reservation.
- [ ] Add final pre-replacement read-set tests for every mutating request. While
  locked, freeze a sorted raw-hash set covering core, schema, manifest sources,
  ledger, receipt, existing target/reviews, external candidate review/
  disposition inputs, every current output byte or typed `ABSENT`, and the
  reservation record. After all temporaries are written and fsynced but
  immediately before the first repository `os.replace`, re-read HEAD, raw core,
  and every read-set member. Inject one drift at that boundary for changed,
  removed, newly appeared, unreadable, and retargeted-symlink inputs and require
  abort before any replacement, complete temp cleanup, and only an already-made
  reservation remaining burned. Prove earlier validation under the custom lock
  cannot substitute for this final CAS.
- [ ] Exercise exactly one public operation-aware writer surface:
  `write_rendered_value(root: Path, *, request: RenderTransactionRequest) ->
  None`. Construct the frozen request dataclass with every field declared in
  the stable package surface; reject missing, extra, incompatible, or
  operation-irrelevant inputs. For every operation, test exact allowed-change
  membership, protected-path rejection, closure-only role/path agreement, and
  overwrite rule. Prove the function reloads `request.core_path` while holding
  the shared lock and installs the complete operation-specific multi-file
  transaction. Assert no six-argument call, generic public
  `atomic_write_canonical`, or other raw-writer bypass exists; the
  same-directory atomic helper remains private.
- [ ] Test the exact renderer sequence. `freeze-manifest --final` freezes the
  filtered final source snapshot, reserves/records a new PENDING attempt with
  null artifact hashes, expands required external disposition inputs in that
  same transaction, and refuses a live non-terminal leaf until it is ABANDONED.
  `review-target` performs TARGET_READY. `transition-core --stage ATTESTED`
  ingests the first PASS and stays DRAFT/PENDING. FAILED and ABANDONED preserve
  all zero-to-two extant reviews/findings and stay DRAFT. COMPLETE ingests the
  second independent PASS, first constructs and validates the entire
  prospective VERIFIED bundle in memory, then atomically sets PASSED, closes
  owned gates, and makes the receipt COMPLETE without writing a bundle.
  VERIFIED revalidates and atomically installs bundle/core/receipt. The
  standalone `bundle` operation is deterministic construction/preflight only;
  it may not leave a canonical bundle without the matching VERIFIED state.
- [ ] Invoke `freeze_manifest_value` only with its frozen optional
  `finding_dispositions` list and invoke `transition_core_value` only with its
  frozen optional `abandon_reason`. Test a successor allocation with a complete
  disposition input, first-attempt allocation with `None`/empty dispositions,
  and ABANDONED transitions with zero reviews plus a required non-empty reason,
  one review, and two reviews. Reject dispositions on an operation that does
  not allocate, a reason outside ABANDONED, and ABANDONED without a reason.
- [ ] Test receipt projection: `reviewAttemptId=null` exactly for every
  pre-review DRAFT, becomes non-null exactly on first allocation, then equals
  the unique current leaf and never returns to null. DRAFT keeps target/review/
  bundle receipt fields null even when its attempt records artifacts.
  COMPLETE/VERIFIED require
  the current PASSED attempt and exact target/review agreement; COMPLETE keeps
  bundle fields null, while VERIFIED sets the derived bundle path and exact
  digest. Validate the prospective receipt descriptor,
  `receiptNarrativeRawSha256`, `ledgerPreambleRawSha256`, review/schema/ledger/
  queue/dependency hashes, all five persisted history arrays, attempt/artifact
  bijection, and current final LOGIC/BTJ hashes. Receipt signatures or
  lifecycle never replace warrant.
- [ ] Run before implementation:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_review.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_render_kintsugi.py' -v
  ```

  **Expected RED:** missing review/rendering modules and CLI.
- [ ] Implement review projections as pure functions. Deep-diff prospective
  transition values and allow only the stage-specific frozen JSON-pointer sets.
  Implement subject projection/digest, history closure/disposition checks,
  typed endpoint/process-evidence resolution, attestation/finding ownership,
  state/path/hash biconditionals, reserved-control filtering, and full
  prospective-bundle validation as pure functions. Extend orchestration
  here—not in Task 6—so completion consumes immutable attestations/history and
  VERIFIED consumes the exact bundle. In `rendering.py`, the operation-aware
  writer enforces operation/stage, shared lock, HEAD/core CAS, manifest
  allowances, protected/closure roles, external review-intake rules, and
  overwrite policy. Freeze the complete sorted raw-hash read set, stage every
  output to same-directory temporary files, flush/fsync, perform the final
  HEAD/core/all-input CAS immediately before the first `os.replace`, install
  the complete set, and roll back the full transaction on any failure; remove
  temps in `finally`. Permit overwrite
  only where the stage explicitly allows it, with target identical-byte reuse,
  immutable review/terminal history, and bundle immutability. Keep every raw
  atomic helper private. `render_kintsugi.py` only parses, loads, calls,
  reports, and exits.
- [ ] Run both focused suites twice and all prior focused tests once:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_review.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_render_kintsugi.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_review.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_render_kintsugi.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_*.py' -v
  ```

  **Expected GREEN:** all four operations and six stages generate byte-identical
  values on unchanged synthetic inputs; retries expose complete prior history;
  every unsafe, stale, shopping, laundering, drifting, partial, or extra
  transition fails closed; bundle overwrite is refused; the real worktree is
  untouched.
- [ ] Commit:

  ```text
  feat(kintsugi): render bounded review and closure artifacts
  ```

---

### Task 8: Lock the Mutation Matrix and Operational Compass Fixture

**Files:**

- Create `09_TOOLS/02_COMPILERS/test_kintsugi_mutations.py`.
- Extend `09_TOOLS/02_COMPILERS/kintsugi_kernel/semantics.py` only where a
  named operational predicate is still missing.
- Extend `09_TOOLS/02_COMPILERS/kintsugi_test_support.py` with the Compass
  vessel and deterministic mutation enumerator.

- [ ] Build one complete synthetic operational Compass vessel whose typed
  chain is: actual state -> fallible model -> modeled reachable options inside
  physical constraints -> authorized commitment using available means ->
  action event -> occurrence receipt -> independently observed consequence ->
  model/selector update. Mark it explicitly synthetic and correspondence-level;
  it is not evidence that the worldview is true across domains.
- [ ] Add one negative mutation for every required distinction: option cone as
  physical cone expansion; modeled future as physical retrocausality;
  commitment as quantum measurement; receipt as outcome proof; receipt without
  independent consequence observation driving update; authorization as truth;
  mu crossing as a computable law; chi as a total predictor; and Rosetta
  recurrence as independent replication. Each mutation changes one field/edge
  and declares one stable code.
- [ ] Add the named design mutations:
  `DELETE_REQUIRED_FIELD`, `ADD_UNKNOWN_FIELD`, `SCALAR_TO_ARRAY`,
  `SCALAR_TO_OBJECT`, `SCALAR_TO_NULL`, `INTEGER_TO_BOOLEAN`, `INVALID_ENUM`,
  `INVALID_ID`, `INVALID_PATH`, `INVALID_HASH`, `DANGLING_REFERENCE`,
  `DUPLICATE_ID`, `DEPENDENCY_CYCLE`, `STALE_OWNER_QUOTE`,
  `PHASE_ORDER_BYPASS`, `PROTECTED_PATH_CHANGE`, `COMMITTED_SCOPE_ESCAPE`,
  `PROVENANCE_AS_AUTHORITY`, `RECEIPT_FENCE_DRIFT`, `REVIEW_TARGET_DRIFT`, and
  `BUNDLE_OVERWRITE`. Add named pre-v1 mutations for mixed cycles, analogy/
  Rosetta upgrades, unsupported upgrade links, kill/deferred/downgrade laws,
  surviving-kernel dependence, missing/misbound requirements, public K2,
  constitutional signature conflation, owner-search incompleteness, and
  closure omission. Add `CLOSURE_ONLY_SEMANTIC_HIDING`,
  `OMITTED_EVALUATOR_DISPATCH`, `SKIPPED_DECLARED_FIXTURE`, and
  `MATCH_COUNT_AS_EVIDENCE`. Add retry/closure mutations
  `ATTEMPT_ID_ALIAS`, `ATTEMPT_RESERVATION_REUSE`, `STALE_HEAD_CORE_CAS`,
  `UNCOMMITTED_PREDECESSOR`, `PASSED_SUPERSESSION`, `SECOND_CHAIN_LEAF`,
  `PARTIAL_REVIEW_HIDDEN`, `UNRECORDED_CANONICAL_REVIEW`,
  `REVIEW_HISTORY_OMISSION`, `FINDING_DISPOSITION_OMISSION`,
  `REVIEWER_SHOPPING`, `SAME_SUBJECT_LAUNDERING`,
  `EARLY_VALIDATION_BUNDLE`, and `PARTIAL_RENDER_TRANSACTION`; each must fail
  with its declared stable code.
  Add `RESERVED_CONTROL_INVENTORY_LEAK`, `UNBOUND_CONTROL_ARTIFACT`,
  `LEDGER_PREAMBLE_DRIFT`, `RECEIPT_NARRATIVE_DRIFT`,
  `INVALID_FINDING_ENDPOINT`, `PARTIAL_DISPOSITION_INPUT`,
  `UNBOUND_PROCESS_EVIDENCE`, `PRE_REVIEW_ATTEMPT_POINTER`,
  `SAFE_REGEX_UNSUPPORTED_TOKEN`, `SAFE_REGEX_STATE_LIMIT`, and
  `SAFE_REGEX_REDOS_REGRESSION` with the same one-fact/stable-code discipline.
- [ ] Repeat Task 3's antibody contract end to end through production
  orchestration: positive and negative rows for all eight semantic evaluators;
  LITERAL, REGEX, and SEMANTIC_FIXTURE dispatch; POSITIVE, NEGATIVE, QUOTATION,
  and HISTORICAL contexts; the closed segment-aware safe-glob scope/exclude
  grammar; the complete bounded Thompson-NFA `safeRegexSearch` grammar and
  `(a+)+$` near-match regression; invalid/oversize glob/regex; exact expected
  include/exclude and trigger sets; and source-negative document scans. Require every
  declared fixture to execute and prove that zero, one, or many text matches
  never alter evidence, modality, validity, or authority.
- [ ] For each Phase A/B/C synthetic attempt chain, mutate the derived
  four-path union by omitting an ancestor path, adding an unreferenced path,
  swapping an ID/phase/role, or substituting one owner, protocol, schema, test,
  core, semantic-ledger, receipt, or public-queue path. Require rejection before
  review-target semantic diff computation, so closure mechanics cannot hide a
  semantic change.
- [ ] Mutate the reserved control-path filter in each manifest inventory
  (`candidateFiles`, `includedFiles`, `finalFiles`, `excludedPaths`) and then
  mutate each typed replacement binding in target/bundle. Require the former to
  reject raw self-hash/deadlock reintroduction and the latter to reject an
  unbound core, ledger preamble/section, receipt narrative, target, review, or
  history byte.
- [ ] Mutate every review-attempt state/path/hash matrix cell and each legal
  transition edge. Cover a PENDING hidden review, ABANDONED erased partial
  review, FAIL without exact severe findings, PASS with severe finding,
  COMPLETE without prospective VERIFIED-bundle preflight, DRAFT with mismatched
  final-file path/hash, receipt/current-leaf drift, and VERIFIED with omitted or
  altered ancestor history. Each mutation changes one semantic fact and is
  rejected before any canonical byte changes.
- [ ] Derive structural mutations deterministically from the normative
  schema's required fields, scalar properties, enums, patterns, and tagged
  unions. Every fixture has `kind=MUTATION`, `expectedExitCode=1`, non-empty
  `expectedErrorCodes`, and a typed `mutationLevel`; non-mutations have
  `mutationLevel=null`. Assert no mutation changes the source vessel and no two
  named cases are byte-identical.
- [ ] Run before completing the matrix:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_mutations.py' -v
  ```

  **Expected RED:** at least one named conflation or schema-derived mutation is
  accepted, omitted, or emits a different stable code.
- [ ] Complete only the missing closed predicates/enumeration. The mutation
  runner deep-copies its input, invokes the same production validators, and
  treats any exception/traceback, stdout on failure, missing expected code, or
  non-1 semantic exit as a test failure. Do not add a score, probabilistic
  judgment, NLP classifier, or cross-domain proof claim.
- [ ] Run the mutation module twice, then all A0B and A0 tests:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_mutations.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_mutations.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_*.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
  ```

  **Expected GREEN:** both mutation runs enumerate the same ordered case IDs
  and diagnostics; every required conflation is killed; the valid Compass
  vessel passes; all focused and original tests remain green.
- [ ] Commit:

  ```text
  test(kintsugi): lock the Compass mutation matrix
  ```

---

### Task 9: Document the A1 Handoff and Prove A0B Scope

**Files:**

- Modify `09_TOOLS/02_COMPILERS/README.md`.
- Create
  `docs/superpowers/specs/2026-07-12-kintsugi-a0b-machine-kernel-handoff.md`.
- Do not change machine behavior except for documentation-link tests if needed.

- [ ] Update the compiler README with the package boundaries, the three root
  roles, read-only validator commands, four renderer operations, stable
  diagnostic/exit contract, six explicit renderer stages, canonical retry-ID/
  history law, external review-intake flags, Git-common-dir lock/reservation,
  `--finding-dispositions-input`, reserved typed-control filtering and narrative
  hashes, bounded `safeRegexSearch`, HEAD/core CAS requirements, synthetic-only A0B boundary, and the honest fact
  that default live `--check` returns missing-input until A1 creates/finalizes
  its jointly frozen vessel. Do not include a command that writes to the live
  core path during A0B.
- [ ] Write the machine-only handoff with: A0 and observed implementation
  commits through Task 8 only; schema raw hash; focused test commands/counts;
  repeated deterministic renderer/concurrency/retry/mutation evidence; exact
  preserved baseline line; protected/no-live scope checks; open limits; and the explicit A1
  sequence (freeze stable tracked boundary, create `MAN-A-001`, atomize live
  Phase-A sources/claims/trials, create the ledger, and stage DRAFT
  `REC-A-108`). State that A0B validates machinery, not the worldview or any
  live claim. The handoff never predicts or self-hashes its own final Task 9
  documentation commit.
- [ ] Add or extend a documentation test that resolves every new Markdown link
  and rejects live renderer examples. Run it before the documentation edit.

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_schema.py' -v
  ```

  **Expected RED:** the handoff/README contract or link is absent.
- [ ] Apply the README and handoff edits, rerun the focused documentation test
  to GREEN, and create the path-limited Task 9 implementation commit:

  ```text
  docs(kintsugi): hand off the verified A0B machine
  ```

  Do not run final `...HEAD`, 29-path, forbidden-scope, or clean-status
  assertions yet.
- [ ] The controller records Task 9 BASE and HEAD, builds the committed-range
  review package, and dispatches the task reviewer. Apply accepted findings as
  path-limited follow-up commits, rebuild the `BASE..HEAD` package, and repeat
  review until the committed range is clean. No review is performed against an
  uncommitted diff.
- [ ] Only after the review-clean final Task 9 commit, run the complete
  verification set from the A0B worktree root:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_validate_kintsugi.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_kintsugi_*.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
    -s 09_TOOLS/02_COMPILERS -p 'test_render_kintsugi.py' -v
  python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
    --check-baseline \
    --canonical-root /Users/Yves/Documents/01_EMERGENTISM
  git diff --check 181559a370598e1ae7572c33d21369ef6c6419e2
  ```

  **Expected GREEN:** all tests pass, no traceback or generated cache enters
  the tree, the baseline command exits 0 with the exact 19/5 line, and diff
  check is empty.
- [ ] Verify forbidden scope is empty:

  ```bash
  git diff --name-only 181559a370598e1ae7572c33d21369ef6c6419e2...HEAD -- \
    00_META 02_EPISTEMOLOGY 05_COSMOLOGY 07_THEOLOGY \
    03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json \
    03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md \
    11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md \
    12_PUBLIC_SITE 90_ARCHIVE 91_COMPATIBILITY
  ```

  **Expected:** empty output. The schema itself is outside these forbidden
  targets and is the only new file in the derivation directory.
- [ ] Verify the complete tracked A0B delta equals the declared 29-path set:

  ```bash
  python3 -B - <<'PY'
  import subprocess

  expected = {
      "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json",
      "09_TOOLS/02_COMPILERS/README.md",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/__init__.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/baseline.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/codec.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/diagnostics.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/gitstate.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/manifest.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/markdown.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/orchestration.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/records.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/rendering.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/review.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/schema.py",
      "09_TOOLS/02_COMPILERS/kintsugi_kernel/semantics.py",
      "09_TOOLS/02_COMPILERS/kintsugi_test_support.py",
      "09_TOOLS/02_COMPILERS/render_kintsugi.py",
      "09_TOOLS/02_COMPILERS/test_kintsugi_manifest.py",
      "09_TOOLS/02_COMPILERS/test_kintsugi_markdown.py",
      "09_TOOLS/02_COMPILERS/test_kintsugi_mutations.py",
      "09_TOOLS/02_COMPILERS/test_kintsugi_records.py",
      "09_TOOLS/02_COMPILERS/test_kintsugi_review.py",
      "09_TOOLS/02_COMPILERS/test_kintsugi_schema.py",
      "09_TOOLS/02_COMPILERS/test_kintsugi_semantics.py",
      "09_TOOLS/02_COMPILERS/test_render_kintsugi.py",
      "09_TOOLS/02_COMPILERS/validate_kintsugi.py",
      "docs/superpowers/plans/2026-07-12-kintsugi-a0b-machine-kernel-implementation.md",
      "docs/superpowers/specs/2026-07-12-kintsugi-a0b-machine-kernel-addendum.md",
      "docs/superpowers/specs/2026-07-12-kintsugi-a0b-machine-kernel-handoff.md",
  }
  actual = set(subprocess.check_output([
      "git", "diff", "--name-only",
      "181559a370598e1ae7572c33d21369ef6c6419e2...HEAD",
  ], text=True).splitlines())
  missing = sorted(expected - actual)
  extra = sorted(actual - expected)
  if missing or extra:
      raise SystemExit(f"A0B scope mismatch: missing={missing} extra={extra}")
  print("KIN-OK A0B scope paths=29")
  PY
  ```

  **Expected:** `KIN-OK A0B scope paths=29` and no stderr. Also run
  `git status --short`; after the final commit it must be empty.
- [ ] If any post-commit command fails, patch only the declared Task 9 paths,
  rerun the focused tests to GREEN, create a path-limited follow-up commit,
  rebuild the committed `BASE..HEAD` review package, and repeat task review to
  clean before rerunning complete verification, forbidden-scope, 29-path, and
  clean-status checks against the new HEAD. Task 9 ends only on a review-clean,
  fully verified committed tree.

After the review-clean Task 9 final commit and its HEAD-based checks succeed,
the controller—not the Task 9 implementer—runs the independent whole-branch
review and resolves every Critical or Important finding in follow-up commits
before A0B handoff.

## A0B acceptance

- The literal schema appendix and checked-in schema are byte-identical after
  canonicalization, expose only the three CLI-selectable roles, and validate a
  complete synthetic instance of each role.
- Schema, graph, state, evidence, modality, Justice, authority, provenance,
  omission, Rosetta, Markdown, Git, protected-tree, review, bundle, transition,
  and queue barriers have positive and negative tests.
- The five persisted review-history arrays are complete and append-only;
  canonical per-phase attempt allocation is shared-worktree-safe; every
  predecessor finding is visibly disposed; same-subject retries cannot launder
  substantive failure; PASSED is terminal; and all historical bytes remain
  bound into later targets and the final bundle.
- Reserved mutable control artifacts never enter manifest C/I/F/E inventories
  or self-hash. Their complete typed semantics and raw narrative regions are
  instead bound by target/artifacts/bundle, including ledger preamble and
  receipt narrative hashes.
- Finding locations are typed across claims, seams, ledger sections/preamble,
  receipts, and subject files; PROCESS_INVALID evidence is path-and-hash bound;
  successor ID reservation, disposition expansion, and graph update are one
  fail-closed transaction.
- Every schema-derived and named mutation fails with the declared stable code;
  the operational Compass vessel passes only with all nine distinctions intact.
- The renderer's four operations/six stages are deterministic, safe-path-bound,
  lock/CAS guarded, transactional, and tested only in temporary synthetic
  repositories. Raw review inputs enter only through the typed external intake;
  no public raw writer or early canonical bundle exists.
- REGEX antibodies run only through the bounded Thompson-NFA
  `safeRegexSearch`; unsupported syntax, state/pattern overflow, and ReDoS
  probes fail deterministically without invoking Python's backtracking engine.
- The original 22 A0 tests pass without changing their source or the baseline
  contract, and the canonical baseline prints the exact 19/5 line.
- The tracked delta is exactly the declared 29 paths. No live owner, core,
  manifest, ledger, receipt, review, bundle, public, archive, or compatibility
  artifact changed.
- Independent task reviews and the controller's post-Task-9 whole-branch review
  report no unresolved Critical or Important finding.
- The handoff says only that the machine is ready. A1, A2, and later phases
  retain responsibility for live truth claims, repairs, review, and promotion.

## Appendix A: Complete Literal JSON Schema

This appendix is the frozen, independently reviewed complete canonical schema.
Its one-line JSON plus LF is the sole Task 2 source for the checked-in schema
artifact. It parses with schema ID
`https://emergentism.org/schema/kintsugi/1.0.0`, uses only the declared keyword
vocabulary, includes every current addendum record and conditional, and keeps
CLI selection limited to the three root roles. Nested definitions are validated
only through the internal named-definition function; they do not become CLI
roles. No generator, marker, or prose placeholder is part of the schema bytes.

```json
{"$defs":{"allowedFailure":{"additionalProperties":false,"properties":{"exceptionType":{"$ref":"#/$defs/text"},"nodeId":{"$ref":"#/$defs/text"},"requiredSignature":{"$ref":"#/$defs/text"}},"required":["nodeId","exceptionType","requiredSignature"],"type":"object"},"allowedPreexistingUntracked":{"additionalProperties":false,"properties":{"canonical":{"items":{"$ref":"#/$defs/fileHashRecord"},"minItems":0,"type":"array","uniqueItems":true},"isolated":{"items":{"$ref":"#/$defs/fileHashRecord"},"minItems":0,"type":"array","uniqueItems":true}},"required":["isolated","canonical"],"type":"object"},"antibody":{"additionalProperties":false,"allOf":[{"else":{"properties":{"semanticEvaluator":{"type":"null"}}},"if":{"properties":{"matchMode":{"const":"SEMANTIC_FIXTURE"}},"required":["matchMode"]},"then":{"properties":{"semanticEvaluator":{"enum":["VERDICT_MATRIX","JUSTICE_CONTEXT","RECEIPT_ROLE","REGISTER_INDEX","QUANTUM_MEASURE","OPTION_CONE","TROPHIC_AGGREGATOR","ROSETTA_TRANSFER"],"type":"string"}}}},{"if":{"properties":{"matchMode":{"const":"REGEX"}},"required":["matchMode"]},"then":{"properties":{"pattern":{"maxLength":256}}}}],"properties":{"excludeGlobs":{"items":{"$ref":"#/$defs/text"},"minItems":0,"type":"array"},"historicalFixtureIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"id":{"$ref":"#/$defs/id"},"matchMode":{"enum":["LITERAL","REGEX","SEMANTIC_FIXTURE"],"type":"string"},"negativeFixtureIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"pattern":{"$ref":"#/$defs/text"},"positiveFixtureIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"quotationFixtureIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"scopeGlobs":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"seamId":{"$ref":"#/$defs/id"},"semanticEvaluator":{"anyOf":[{"enum":["VERDICT_MATRIX","JUSTICE_CONTEXT","RECEIPT_ROLE","REGISTER_INDEX","QUANTUM_MEASURE","OPTION_CONE","TROPHIC_AGGREGATOR","ROSETTA_TRANSFER"],"type":"string"},{"type":"null"}]}},"required":["id","seamId","pattern","matchMode","semanticEvaluator","scopeGlobs","excludeGlobs","positiveFixtureIds","negativeFixtureIds","quotationFixtureIds","historicalFixtureIds"],"type":"object"},"authority":{"additionalProperties":false,"properties":{"basis":{"$ref":"#/$defs/text"},"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"],"type":"string"},"regime":{"enum":["NOT_APPLICABLE","PRIVATE_DAV","PUBLIC_DAV","OTHER"],"type":"string"}},"required":["regime","mechanism","basis"],"type":"object"},"authorityEffect":{"enum":["NONE","DESCRIPTIVE","DISCRETIONARY","CONSEQUENTIAL","CONSTITUTIONAL_AUTOMATIC"],"type":"string"},"authorityScope":{"enum":["NONE","PRIVATE_DAV","PUBLIC_DAV","OTHER"],"type":"string"},"baselineAllowlist":{"additionalProperties":false,"properties":{"allowedFailures":{"items":{"$ref":"#/$defs/allowedFailure"},"minItems":1,"type":"array","uniqueItems":true},"baseCommit":{"$ref":"#/$defs/commitHash"},"baselineNodeIds":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array","uniqueItems":true},"collectCommand":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"collectedAtBaseline":{"$ref":"#/$defs/count"},"command":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"schemaVersion":{"const":"1.0.0"}},"required":["schemaVersion","baseCommit","command","collectCommand","collectedAtBaseline","baselineNodeIds","allowedFailures"],"type":"object"},"claim":{"additionalProperties":false,"allOf":[{"else":{"properties":{"justiceContext":{"type":"null"}}},"if":{"anyOf":[{"properties":{"justiceScope":{"enum":["COLLECTIVE","NORMATIVE","COLLECTIVE_NORMATIVE"]}},"required":["justiceScope"]},{"properties":{"authorityEffect":{"enum":["DESCRIPTIVE","DISCRETIONARY","CONSEQUENTIAL","CONSTITUTIONAL_AUTOMATIC"]}},"required":["authorityEffect"]}]},"then":{"required":["justiceContext"]}},{"if":{"properties":{"claimType":{"const":"NORMATIVE"}},"required":["claimType"]},"then":{"properties":{"justiceScope":{"enum":["NORMATIVE","COLLECTIVE_NORMATIVE"]}}}},{"if":{"properties":{"modality":{"const":"NORMATIVE"}},"required":["modality"]},"then":{"properties":{"justiceScope":{"enum":["NORMATIVE","COLLECTIVE_NORMATIVE"]}}}},{"if":{"properties":{"authorityEffect":{"const":"NONE"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"const":"NONE"},"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"NONE"},"regime":{"const":"NOT_APPLICABLE"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"enum":["PRIVATE_DAV","PUBLIC_DAV","OTHER"]}},"required":["justiceContext"]}},{"if":{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"enum":["PRIVATE_DAV","PUBLIC_DAV","OTHER"]}},"required":["justiceContext"]}},{"if":{"properties":{"authorityEffect":{"const":"CONSTITUTIONAL_AUTOMATIC"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"const":"PUBLIC_DAV"},"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"CONSTITUTIONAL_AUTO_ENFORCEMENT"},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"OTHER"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"PRISM_PUBLIC_GOVERNANCE"},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"OTHER"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidence":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidence"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"properties":{"evidence":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidence"]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromC"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromC"}}}},{"if":{"properties":{"evidence":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidence"]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromI"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromI"}}}},{"if":{"properties":{"evidence":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidence"]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromS"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromS"}}}},{"if":{"properties":{"evidence":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidence"]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromA"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromA"}}}},{"if":{"properties":{"evidence":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]}},"required":["evidence"]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killNone"}}}},{"if":{"properties":{"evidence":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidence"]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killTestable"}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidence":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidence"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidence":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidence"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"OTHER"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidence":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidence"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}}],"properties":{"authorityEffect":{"$ref":"#/$defs/authorityEffect"},"authorityScope":{"$ref":"#/$defs/authorityScope"},"claimType":{"$ref":"#/$defs/claimType"},"conclusion":{"$ref":"#/$defs/text"},"dependencyClaimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"evidence":{"$ref":"#/$defs/evidence"},"id":{"$ref":"#/$defs/id"},"inference":{"$ref":"#/$defs/inference"},"justiceContext":{"$ref":"#/$defs/justiceContext"},"justiceScope":{"$ref":"#/$defs/justiceScope"},"killCriterion":{"$ref":"#/$defs/killCriterion"},"modality":{"$ref":"#/$defs/modality"},"ownerAnchor":{"$ref":"#/$defs/text"},"ownerSourceId":{"$ref":"#/$defs/id"},"premises":{"items":{"$ref":"#/$defs/premise"},"minItems":1,"type":"array","uniqueItems":true},"proposition":{"$ref":"#/$defs/text"},"quantifiers":{"items":{"$ref":"#/$defs/quantifier"},"minItems":1,"type":"array","uniqueItems":true},"scope":{"$ref":"#/$defs/scope"},"supportLinks":{"items":{"$ref":"#/$defs/supportLink"},"minItems":0,"type":"array","uniqueItems":true},"survivingIfKilled":{"$ref":"#/$defs/survivingIfKilled"},"typedTerms":{"items":{"$ref":"#/$defs/typedTerm"},"minItems":1,"type":"array","uniqueItems":true},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterion"}},"required":["id","ownerSourceId","ownerAnchor","proposition","claimType","typedTerms","premises","conclusion","inference","quantifiers","modality","scope","justiceScope","authorityScope","authorityEffect","evidence","dependencyClaimIds","supportLinks","upgradeCriterion","killCriterion","survivingIfKilled"],"type":"object"},"claimExclusion":{"additionalProperties":false,"properties":{"claimId":{"$ref":"#/$defs/id"},"reason":{"$ref":"#/$defs/text"}},"required":["claimId","reason"],"type":"object"},"claimType":{"enum":["MATHEMATICAL","STRUCTURAL","INTERPRETIVE","EMPIRICAL","NORMATIVE","METAPHORICAL"],"type":"string"},"commitHash":{"pattern":"^[0-9a-f]{40}$","type":"string"},"consent":{"additionalProperties":false,"properties":{"basis":{"$ref":"#/$defs/text"},"status":{"enum":["OBTAINED","NOT_REQUIRED","MISSING"],"type":"string"}},"required":["status","basis"],"type":"object"},"containment":{"additionalProperties":false,"properties":{"antibodyIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"blockedDependencyClaimIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"rationale":{"$ref":"#/$defs/text"}},"required":["antibodyIds","blockedDependencyClaimIds","rationale"],"type":"object"},"coreData":{"additionalProperties":false,"properties":{"antibodies":{"items":{"$ref":"#/$defs/antibody"},"minItems":0,"type":"array","uniqueItems":true},"claims":{"items":{"$ref":"#/$defs/claim"},"minItems":1,"type":"array","uniqueItems":true},"discriminators":{"items":{"$ref":"#/$defs/discriminator"},"minItems":0,"type":"array","uniqueItems":true},"fixtures":{"items":{"$ref":"#/$defs/fixture"},"minItems":0,"type":"array","uniqueItems":true},"manifests":{"items":{"$ref":"#/$defs/manifest"},"minItems":1,"type":"array","uniqueItems":true},"phaseReceipts":{"items":{"$ref":"#/$defs/phaseReceipt"},"minItems":1,"type":"array","uniqueItems":true},"program":{"$ref":"#/$defs/program"},"propagations":{"items":{"$ref":"#/$defs/propagation"},"minItems":0,"type":"array","uniqueItems":true},"reviewAttemptArtifacts":{"items":{"$ref":"#/$defs/reviewAttemptArtifact"},"minItems":0,"type":"array","uniqueItems":true},"reviewAttempts":{"items":{"$ref":"#/$defs/reviewAttempt"},"minItems":0,"type":"array","uniqueItems":true},"reviewAttestations":{"items":{"$ref":"#/$defs/reviewAttestation"},"minItems":0,"type":"array","uniqueItems":true},"reviewFindingDispositions":{"items":{"$ref":"#/$defs/reviewFindingDisposition"},"minItems":0,"type":"array","uniqueItems":true},"reviewFindings":{"items":{"$ref":"#/$defs/reviewFinding"},"minItems":0,"type":"array","uniqueItems":true},"schemaVersion":{"const":"1.0.0"},"seams":{"items":{"$ref":"#/$defs/seam"},"minItems":0,"type":"array","uniqueItems":true},"sources":{"items":{"$ref":"#/$defs/source"},"minItems":1,"type":"array","uniqueItems":true},"trials":{"items":{"$ref":"#/$defs/trial"},"minItems":0,"type":"array","uniqueItems":true}},"required":["schemaVersion","program","manifests","sources","claims","trials","seams","antibodies","discriminators","fixtures","propagations","phaseReceipts","reviewAttempts","reviewAttemptArtifacts","reviewAttestations","reviewFindings","reviewFindingDispositions"],"type":"object"},"count":{"minimum":0,"type":"integer"},"countermodel":{"additionalProperties":false,"properties":{"construction":{"$ref":"#/$defs/text"},"defeatedConclusion":{"$ref":"#/$defs/text"},"description":{"$ref":"#/$defs/text"}},"required":["description","construction","defeatedConclusion"],"type":"object"},"credit":{"additionalProperties":false,"properties":{"displayName":{"$ref":"#/$defs/text"},"role":{"$ref":"#/$defs/text"}},"required":["displayName","role"],"type":"object"},"defectClass":{"enum":["EQUIVOCATION","TYPE_ERROR","NON_SEQUITUR","HIDDEN_PREMISE","CIRCULARITY","TAUTOLOGY_LAUNDERING","CATEGORY_ERROR","INVALID_MODAL_STRENGTH","QUANTIFIER_SHIFT","SCOPE_ERROR","FALSE_DILEMMA","SELF_SEALING_FALSIFIER","EVIDENCE_TIER_INFLATION","AUTHORITY_DRIFT","COMPRESSION_DRIFT","DIRECT_CONTRADICTION"],"type":"string"},"dependencyReceipt":{"additionalProperties":false,"properties":{"id":{"$ref":"#/$defs/id"},"validationDigest":{"$ref":"#/$defs/rawHash"}},"required":["id","validationDigest"],"type":"object"},"discoveryRule":{"additionalProperties":false,"properties":{"excludeGlobs":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"id":{"$ref":"#/$defs/id"},"includeGlobs":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"parser":{"enum":["MARKDOWN","HTML","JSON","SOURCE_INDEX"],"type":"string"},"rationale":{"$ref":"#/$defs/text"}},"required":["id","includeGlobs","excludeGlobs","parser","rationale"],"type":"object"},"discriminator":{"additionalProperties":false,"properties":{"cheapestTest":{"$ref":"#/$defs/text"},"claimId":{"$ref":"#/$defs/id"},"decisionRule":{"$ref":"#/$defs/text"},"expectedObservations":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"id":{"$ref":"#/$defs/id"},"method":{"$ref":"#/$defs/text"},"question":{"$ref":"#/$defs/text"},"status":{"enum":["QUEUED","RUNNING","DECISIVE","INCONCLUSIVE","RETIRED"],"type":"string"}},"required":["id","claimId","question","method","cheapestTest","expectedObservations","decisionRule","status"],"type":"object"},"evidence":{"additionalProperties":false,"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE","RETIRED"],"type":"string"},"sourced":{"type":"boolean"},"strength":{"$ref":"#/$defs/evidenceStrength"}},"required":["strength","sourced","lifecycle"],"type":"object"},"evidenceStrength":{"enum":["A","S","I","C"],"type":"string"},"fileHashRecord":{"additionalProperties":false,"properties":{"kind":{"enum":["FILE","SYMLINK"],"type":"string"},"path":{"$ref":"#/$defs/path"},"sha256":{"$ref":"#/$defs/rawHash"}},"required":["path","kind","sha256"],"type":"object"},"fixture":{"additionalProperties":false,"allOf":[{"if":{"properties":{"kind":{"const":"POSITIVE"}},"required":["kind"]},"then":{"properties":{"antibodyIds":{"minItems":1},"expectedAntibodyIds":{"minItems":1},"expectedErrorCodes":{"minItems":1},"expectedExitCode":{"const":1},"mutationLevel":{"type":"null"},"seamIds":{"minItems":1}}}},{"if":{"properties":{"kind":{"enum":["NEGATIVE","QUOTATION","HISTORICAL"]}},"required":["kind"]},"then":{"properties":{"antibodyIds":{"minItems":1},"expectedAntibodyIds":{"maxItems":0},"expectedErrorCodes":{"maxItems":0},"expectedExitCode":{"const":0},"mutationLevel":{"type":"null"},"seamIds":{"minItems":0}}}},{"if":{"properties":{"kind":{"const":"MUTATION"}},"required":["kind"]},"then":{"properties":{"antibodyIds":{"minItems":0},"expectedAntibodyIds":{"minItems":0},"expectedErrorCodes":{"minItems":1},"expectedExitCode":{"const":1},"mutationLevel":{"enum":["SCHEMA","GRAPH","SEMANTIC","MARKDOWN","GIT","RENDERER"],"type":"string"},"seamIds":{"minItems":0}}}}],"properties":{"antibodyIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"expectedAntibodyIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"expectedErrorCodes":{"items":{"$ref":"#/$defs/text"},"minItems":0,"type":"array","uniqueItems":true},"expectedExitCode":{"enum":[0,1],"type":"integer"},"id":{"$ref":"#/$defs/id"},"kind":{"enum":["POSITIVE","NEGATIVE","QUOTATION","HISTORICAL","MUTATION"],"type":"string"},"mutationLevel":{"anyOf":[{"enum":["SCHEMA","GRAPH","SEMANTIC","MARKDOWN","GIT","RENDERER"],"type":"string"},{"type":"null"}]},"payload":{"$ref":"#/$defs/text"},"payloadKind":{"enum":["TEXT","JSON"],"type":"string"},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true}},"required":["id","kind","payloadKind","payload","mutationLevel","expectedExitCode","expectedErrorCodes","expectedAntibodyIds","antibodyIds","seamIds"],"type":"object"},"gate":{"oneOf":[{"$ref":"#/$defs/gatePending"},{"$ref":"#/$defs/gateReviewed"}]},"gatePass":{"additionalProperties":false,"properties":{"rationale":{"$ref":"#/$defs/text"},"reviewerPath":{"$ref":"#/$defs/path"},"status":{"const":"PASS"}},"required":["status","rationale","reviewerPath"],"type":"object"},"gatePending":{"additionalProperties":false,"properties":{"rationale":{"$ref":"#/$defs/text"},"reviewerPath":{"type":"null"},"status":{"const":"PENDING"}},"required":["status","rationale","reviewerPath"],"type":"object"},"gateRationale":{"additionalProperties":false,"properties":{"rationale":{"$ref":"#/$defs/text"}},"required":["rationale"],"type":"object"},"gateReviewed":{"additionalProperties":false,"properties":{"rationale":{"$ref":"#/$defs/text"},"reviewerPath":{"$ref":"#/$defs/path"},"status":{"enum":["PASS","FAIL"],"type":"string"}},"required":["status","rationale","reviewerPath"],"type":"object"},"id":{"minLength":1,"pattern":"^[A-Z][A-Z0-9_-]*$","type":"string"},"inference":{"additionalProperties":false,"properties":{"formalization":{"$ref":"#/$defs/text"},"rule":{"$ref":"#/$defs/text"}},"required":["rule","formalization"],"type":"object"},"justiceContext":{"additionalProperties":false,"properties":{"authority":{"$ref":"#/$defs/authority"},"beneficiary":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"consent":{"$ref":"#/$defs/consent"},"costBearer":{"items":{"$ref":"#/$defs/text"},"minItems":1,"type":"array"},"custody":{"$ref":"#/$defs/text"},"eta":{"$ref":"#/$defs/text"},"exit":{"$ref":"#/$defs/text"},"individual":{"$ref":"#/$defs/text"},"optionConeEffect":{"$ref":"#/$defs/optionConeEffect"},"reversibility":{"enum":["REVERSIBLE","PARTIAL","IRREVERSIBLE"],"type":"string"},"whole":{"$ref":"#/$defs/text"}},"required":["individual","whole","eta","beneficiary","costBearer","consent","custody","reversibility","exit","optionConeEffect","authority"],"type":"object"},"justiceContextPayload":{"additionalProperties":false,"properties":{"authorityEffect":{"$ref":"#/$defs/authorityEffect"},"authorityScope":{"$ref":"#/$defs/authorityScope"},"claimType":{"$ref":"#/$defs/claimType"},"evidenceLifecycle":{"enum":["DRAFT","ACTIVE","RETIRED"],"type":"string"},"justiceContext":{"anyOf":[{"$ref":"#/$defs/justiceContext"},{"type":"null"}]},"justiceScope":{"$ref":"#/$defs/justiceScope"},"modality":{"$ref":"#/$defs/modality"}},"required":["claimType","modality","justiceScope","authorityScope","authorityEffect","evidenceLifecycle","justiceContext"],"type":"object"},"justiceScope":{"enum":["NONE","INDIVIDUAL","COLLECTIVE","NORMATIVE","COLLECTIVE_NORMATIVE"],"type":"string"},"killActiveRetier":{"additionalProperties":false,"properties":{"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["A","S","I","C"],"type":"string"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength"],"type":"object"},"killActiveRetract":{"additionalProperties":false,"properties":{"disposition":{"const":"RETRACT"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition"],"type":"object"},"killCriterion":{"oneOf":[{"$ref":"#/$defs/killTestable"},{"$ref":"#/$defs/killNone"}]},"killCriterionFromA":{"oneOf":[{"$ref":"#/$defs/killTestableFromA"},{"$ref":"#/$defs/killNone"}]},"killCriterionFromC":{"oneOf":[{"$ref":"#/$defs/killTestableFromC"},{"$ref":"#/$defs/killNone"}]},"killCriterionFromI":{"oneOf":[{"$ref":"#/$defs/killTestableFromI"},{"$ref":"#/$defs/killNone"}]},"killCriterionFromS":{"oneOf":[{"$ref":"#/$defs/killTestableFromS"},{"$ref":"#/$defs/killNone"}]},"killDeferredRetier":{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["A","S","I","C"],"type":"string"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength","deferredReason","unblockCondition"],"type":"object"},"killDeferredRetract":{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETRACT"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","deferredReason","unblockCondition"],"type":"object"},"killNone":{"additionalProperties":false,"properties":{"kind":{"const":"NONE"},"rationale":{"$ref":"#/$defs/text"}},"required":["kind","rationale"],"type":"object"},"killRetierToC":{"oneOf":[{"additionalProperties":false,"properties":{"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["C"],"type":"string"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength"],"type":"object"},{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["C"],"type":"string"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength","deferredReason","unblockCondition"],"type":"object"}]},"killRetierToI":{"oneOf":[{"additionalProperties":false,"properties":{"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["I"],"type":"string"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength"],"type":"object"},{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["I"],"type":"string"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength","deferredReason","unblockCondition"],"type":"object"}]},"killRetierToS":{"oneOf":[{"additionalProperties":false,"properties":{"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["S"],"type":"string"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength"],"type":"object"},{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["S"],"type":"string"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength","deferredReason","unblockCondition"],"type":"object"}]},"killRetract":{"oneOf":[{"$ref":"#/$defs/killActiveRetract"},{"$ref":"#/$defs/killDeferredRetract"}]},"killTestable":{"oneOf":[{"$ref":"#/$defs/killActiveRetract"},{"$ref":"#/$defs/killDeferredRetract"},{"$ref":"#/$defs/killActiveRetier"},{"$ref":"#/$defs/killDeferredRetier"}]},"killTestableFromA":{"oneOf":[{"$ref":"#/$defs/killRetract"},{"additionalProperties":false,"properties":{"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["S","I","C"],"type":"string"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength"],"type":"object"},{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["S","I","C"],"type":"string"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength","deferredReason","unblockCondition"],"type":"object"}]},"killTestableFromC":{"$ref":"#/$defs/killRetract"},"killTestableFromI":{"oneOf":[{"$ref":"#/$defs/killRetract"},{"additionalProperties":false,"properties":{"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["C"],"type":"string"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength"],"type":"object"},{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["C"],"type":"string"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength","deferredReason","unblockCondition"],"type":"object"}]},"killTestableFromS":{"oneOf":[{"$ref":"#/$defs/killRetract"},{"additionalProperties":false,"properties":{"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["I","C"],"type":"string"},"testability":{"const":"ACTIVE"},"trigger":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength"],"type":"object"},{"additionalProperties":false,"properties":{"deferredReason":{"$ref":"#/$defs/text"},"disposition":{"const":"RETIER"},"kind":{"const":"TESTABLE"},"method":{"$ref":"#/$defs/text"},"resultingStrength":{"enum":["I","C"],"type":"string"},"testability":{"const":"DEFERRED"},"trigger":{"$ref":"#/$defs/text"},"unblockCondition":{"$ref":"#/$defs/text"}},"required":["kind","testability","trigger","method","disposition","resultingStrength","deferredReason","unblockCondition"],"type":"object"}]},"ledgerSection":{"additionalProperties":false,"properties":{"id":{"$ref":"#/$defs/id"},"sectionRawSha256":{"$ref":"#/$defs/rawHash"}},"required":["id","sectionRawSha256"],"type":"object"},"ledgerSemanticSection":{"additionalProperties":false,"properties":{"id":{"$ref":"#/$defs/id"},"narrativeRawSha256":{"$ref":"#/$defs/rawHash"},"seamProjection":{"$ref":"#/$defs/reviewSeamProjection"}},"required":["id","narrativeRawSha256","seamProjection"],"type":"object"},"manifest":{"additionalProperties":false,"allOf":[{"else":{"properties":{"requiredClaimBindings":{"maxItems":0}}},"if":{"properties":{"phase":{"const":"A"}},"required":["phase"]},"then":{"properties":{"requiredClaimBindings":{"maxItems":7,"minItems":7}}}}],"properties":{"allowedChangePaths":{"items":{"$ref":"#/$defs/path"},"minItems":1,"type":"array","uniqueItems":true},"allowedPreexistingUntracked":{"$ref":"#/$defs/allowedPreexistingUntracked"},"baseCommit":{"$ref":"#/$defs/commitHash"},"candidateFileCount":{"$ref":"#/$defs/count"},"candidateFiles":{"items":{"$ref":"#/$defs/fileHashRecord"},"minItems":1,"type":"array","uniqueItems":true},"canonicalBranch":{"const":"main"},"canonicalCommit":{"$ref":"#/$defs/commitHash"},"closureOnlyPaths":{"items":{"$ref":"#/$defs/path"},"minItems":0,"type":"array","uniqueItems":true},"discoveryRules":{"items":{"$ref":"#/$defs/discoveryRule"},"minItems":1,"type":"array","uniqueItems":true},"eligibleClaimCount":{"$ref":"#/$defs/count"},"eligibleFileCount":{"$ref":"#/$defs/count"},"excludedClaimIds":{"items":{"$ref":"#/$defs/claimExclusion"},"minItems":0,"type":"array","uniqueItems":true},"excludedPaths":{"items":{"$ref":"#/$defs/pathExclusion"},"minItems":0,"type":"array","uniqueItems":true},"finalFileCount":{"$ref":"#/$defs/count"},"finalFiles":{"items":{"$ref":"#/$defs/fileHashRecord"},"minItems":0,"type":"array","uniqueItems":true},"harvestedClaimIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"id":{"$ref":"#/$defs/id"},"includedFiles":{"items":{"$ref":"#/$defs/fileHashRecord"},"minItems":1,"type":"array","uniqueItems":true},"inventoryReviewPaths":{"items":{"$ref":"#/$defs/path"},"minItems":1,"type":"array","uniqueItems":true},"phase":{"$ref":"#/$defs/phase"},"protectedPaths":{"items":{"$ref":"#/$defs/path"},"minItems":1,"type":"array","uniqueItems":true},"protectedProvenance":{"items":{"$ref":"#/$defs/protectedProvenanceRecord"},"minItems":1,"type":"array","uniqueItems":true},"protectedTreeSnapshots":{"$ref":"#/$defs/protectedTreeSnapshots"},"requiredClaimBindings":{"items":{"$ref":"#/$defs/requiredClaimBinding"},"maxItems":7,"minItems":0,"type":"array","uniqueItems":true},"scannedFileCount":{"$ref":"#/$defs/count"},"trialedClaimCount":{"$ref":"#/$defs/count"},"trialedClaimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true}},"required":["id","phase","baseCommit","canonicalBranch","canonicalCommit","discoveryRules","candidateFiles","candidateFileCount","includedFiles","finalFiles","finalFileCount","excludedPaths","eligibleFileCount","scannedFileCount","harvestedClaimIds","requiredClaimBindings","excludedClaimIds","eligibleClaimCount","trialedClaimIds","trialedClaimCount","inventoryReviewPaths","protectedProvenance","protectedPaths","protectedTreeSnapshots","allowedChangePaths","closureOnlyPaths","allowedPreexistingUntracked"],"type":"object"},"modality":{"enum":["ACTUAL","POSSIBLE","NECESSARY","NORMATIVE","DEFINITIONAL","CONJECTURAL"],"type":"string"},"optionConeEffect":{"additionalProperties":false,"properties":{"direction":{"enum":["WIDENS","NEUTRAL","CONTRACTS","MIXED"],"type":"string"},"rationale":{"$ref":"#/$defs/text"}},"required":["direction","rationale"],"type":"object"},"optionConePayload":{"additionalProperties":false,"properties":{"commitmentKind":{"enum":["PARTIAL_RELATION","TOTAL_PREDICTOR"],"type":"string"},"futureInfluence":{"enum":["ANTICIPATORY_MODEL","PHYSICAL_RETROCAUSALITY"],"type":"string"},"optionClaim":{"enum":["MODELED_REACHABILITY","PHYSICAL_CONE_EXPANSION"],"type":"string"},"physicalConstraint":{"enum":["C_BOUNDED","SUPERLUMINAL"],"type":"string"}},"required":["physicalConstraint","optionClaim","futureInfluence","commitmentKind"],"type":"object"},"overallVerdict":{"enum":["VALID_SOUND","VALID_CONDITIONAL","VALID_UNSUPPORTED_PREMISE","INVALID","UNDERDETERMINED","DEFINITIONAL","OPEN_CONJECTURE","REFUTED"],"type":"string"},"ownerSearchEvidence":{"additionalProperties":false,"properties":{"manifestIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"method":{"$ref":"#/$defs/text"},"result":{"$ref":"#/$defs/text"},"searchedSourceIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true}},"required":["manifestIds","searchedSourceIds","method","result"],"type":"object"},"path":{"minLength":1,"pattern":"^(?!/)(?!.*(?:^|/)\\.{1,2}(?:/|$))(?!.*//)(?!.*\\\\)[^/]+(?:/[^/]+)*$","type":"string"},"pathExclusion":{"additionalProperties":false,"properties":{"path":{"$ref":"#/$defs/path"},"reason":{"$ref":"#/$defs/text"}},"required":["path","reason"],"type":"object"},"phase":{"enum":["A","B","C"],"type":"string"},"phaseReceipt":{"additionalProperties":false,"allOf":[{"if":{"properties":{"phase":{"const":"A"}},"required":["phase"]},"then":{"properties":{"dependsOnReceiptIds":{"const":[]},"id":{"const":"REC-A-108"},"path":{"const":"11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md"}}}},{"if":{"properties":{"phase":{"const":"B"}},"required":["phase"]},"then":{"properties":{"dependsOnReceiptIds":{"const":["REC-A-108"]},"id":{"const":"REC-B-109"},"path":{"const":"11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md"}}}},{"if":{"properties":{"phase":{"const":"C"}},"required":["phase"]},"then":{"properties":{"dependsOnReceiptIds":{"const":["REC-A-108","REC-B-109"]},"id":{"const":"REC-C-110"},"path":{"const":"11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md"}}}},{"if":{"properties":{"status":{"const":"DRAFT"}},"required":["status"]},"then":{"properties":{"btjReviewPath":{"type":"null"},"logicReviewPath":{"type":"null"},"reviewTargetDigest":{"type":"null"},"validationBundlePath":{"type":"null"},"validationDigest":{"type":"null"}}}},{"if":{"properties":{"status":{"const":"COMPLETE"}},"required":["status"]},"then":{"properties":{"btjReviewPath":{"$ref":"#/$defs/path"},"logicReviewPath":{"$ref":"#/$defs/path"},"reviewAttemptId":{"$ref":"#/$defs/id"},"reviewTargetDigest":{"$ref":"#/$defs/rawHash"},"validationBundlePath":{"type":"null"},"validationDigest":{"type":"null"}}}},{"if":{"properties":{"status":{"const":"VERIFIED"}},"required":["status"]},"then":{"properties":{"btjReviewPath":{"$ref":"#/$defs/path"},"logicReviewPath":{"$ref":"#/$defs/path"},"reviewAttemptId":{"$ref":"#/$defs/id"},"reviewTargetDigest":{"$ref":"#/$defs/rawHash"},"validationBundlePath":{"$ref":"#/$defs/path"},"validationDigest":{"$ref":"#/$defs/rawHash"}}}}],"properties":{"btjReviewPath":{"anyOf":[{"$ref":"#/$defs/path"},{"type":"null"}]},"claimIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"dependsOnReceiptIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"id":{"$ref":"#/$defs/id"},"logicReviewPath":{"anyOf":[{"$ref":"#/$defs/path"},{"type":"null"}]},"manifestId":{"$ref":"#/$defs/id"},"path":{"$ref":"#/$defs/path"},"phase":{"$ref":"#/$defs/phase"},"propagationIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"reviewAttemptId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"reviewTargetDigest":{"anyOf":[{"$ref":"#/$defs/rawHash"},{"type":"null"}]},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"status":{"enum":["DRAFT","COMPLETE","VERIFIED"],"type":"string"},"trialIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"validationBundlePath":{"anyOf":[{"$ref":"#/$defs/path"},{"type":"null"}]},"validationDigest":{"anyOf":[{"$ref":"#/$defs/rawHash"},{"type":"null"}]}},"required":["id","phase","path","status","manifestId","dependsOnReceiptIds","claimIds","trialIds","seamIds","propagationIds","reviewTargetDigest","validationBundlePath","validationDigest","logicReviewPath","btjReviewPath","reviewAttemptId"],"type":"object"},"premise":{"additionalProperties":false,"properties":{"evidence":{"$ref":"#/$defs/evidence"},"id":{"$ref":"#/$defs/id"},"proposition":{"$ref":"#/$defs/text"},"role":{"enum":["DESCRIPTIVE","DEFINITIONAL","NORMATIVE","EVIDENTIARY"],"type":"string"},"sourceIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true}},"required":["id","proposition","evidence","sourceIds","role"],"type":"object"},"program":{"additionalProperties":false,"properties":{"id":{"$ref":"#/$defs/id"},"noK2Gate":{"const":true},"phaseOrder":{"const":["A","B","C"]},"protectedPaths":{"items":{"$ref":"#/$defs/path"},"minItems":1,"type":"array","uniqueItems":true},"semanticAuthority":{"$ref":"#/$defs/path"},"title":{"$ref":"#/$defs/text"}},"required":["id","title","phaseOrder","protectedPaths","semanticAuthority","noK2Gate"],"type":"object"},"propagation":{"additionalProperties":false,"properties":{"derivativeAnchor":{"$ref":"#/$defs/text"},"derivativeHash":{"$ref":"#/$defs/textHash"},"derivativeQuote":{"$ref":"#/$defs/text"},"derivativeSourceId":{"$ref":"#/$defs/id"},"id":{"$ref":"#/$defs/id"},"receiptId":{"$ref":"#/$defs/id"},"seamId":{"$ref":"#/$defs/id"},"status":{"const":"VERIFIED"}},"required":["id","seamId","receiptId","derivativeSourceId","derivativeAnchor","derivativeQuote","derivativeHash","status"],"type":"object"},"protectedProvenanceExactSpan":{"additionalProperties":false,"properties":{"exactSpan":{"$ref":"#/$defs/text"},"mode":{"const":"EXACT_SPAN"},"path":{"$ref":"#/$defs/path"},"sha256":{"$ref":"#/$defs/rawHash"}},"required":["path","mode","exactSpan","sha256"],"type":"object"},"protectedProvenanceFullFile":{"additionalProperties":false,"properties":{"mode":{"const":"FULL_FILE"},"path":{"$ref":"#/$defs/path"},"sha256":{"$ref":"#/$defs/rawHash"}},"required":["path","mode","sha256"],"type":"object"},"protectedProvenanceRecord":{"oneOf":[{"$ref":"#/$defs/protectedProvenanceFullFile"},{"$ref":"#/$defs/protectedProvenanceExactSpan"}]},"protectedTreeSnapshots":{"additionalProperties":false,"properties":{"canonical":{"items":{"$ref":"#/$defs/fileHashRecord"},"minItems":1,"type":"array","uniqueItems":true},"isolated":{"items":{"$ref":"#/$defs/fileHashRecord"},"minItems":1,"type":"array","uniqueItems":true}},"required":["isolated","canonical"],"type":"object"},"publicQueue":{"additionalProperties":false,"properties":{"items":{"items":{"$ref":"#/$defs/publicQueueItem"},"minItems":1,"type":"array","uniqueItems":true},"manifestId":{"$ref":"#/$defs/id"},"receiptId":{"const":"REC-C-110"},"schemaVersion":{"const":"1.0.0"}},"required":["schemaVersion","manifestId","receiptId","items"],"type":"object"},"publicQueueItem":{"oneOf":[{"$ref":"#/$defs/publicQueueOwnedKeep"},{"$ref":"#/$defs/publicQueueOwnedCite"},{"$ref":"#/$defs/publicQueueOwnedRepair"},{"$ref":"#/$defs/publicQueueOwnerless"}]},"publicQueueOwnedCite":{"additionalProperties":false,"properties":{"claimId":{"$ref":"#/$defs/id"},"currentEvidence":{"$ref":"#/$defs/evidence"},"driftClass":{"$ref":"#/$defs/defectClass"},"maximumPublicStrength":{"$ref":"#/$defs/evidenceStrength"},"ownerSourceId":{"$ref":"#/$defs/id"},"ownership":{"const":"OWNED"},"publicFile":{"$ref":"#/$defs/path"},"publicQuote":{"$ref":"#/$defs/text"},"requiredAction":{"const":"CITE"},"route":{"$ref":"#/$defs/text"},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"severity":{"$ref":"#/$defs/severity"},"verificationCommand":{"$ref":"#/$defs/text"}},"required":["route","publicFile","publicQuote","ownership","driftClass","severity","currentEvidence","maximumPublicStrength","requiredAction","verificationCommand","ownerSourceId","claimId","seamIds"],"type":"object"},"publicQueueOwnedKeep":{"additionalProperties":false,"properties":{"claimId":{"$ref":"#/$defs/id"},"currentEvidence":{"$ref":"#/$defs/evidence"},"driftClass":{"type":"null"},"maximumPublicStrength":{"$ref":"#/$defs/evidenceStrength"},"ownerSourceId":{"$ref":"#/$defs/id"},"ownership":{"const":"OWNED"},"publicFile":{"$ref":"#/$defs/path"},"publicQuote":{"$ref":"#/$defs/text"},"requiredAction":{"const":"KEEP"},"route":{"$ref":"#/$defs/text"},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"severity":{"type":"null"},"verificationCommand":{"$ref":"#/$defs/text"}},"required":["route","publicFile","publicQuote","ownership","driftClass","severity","currentEvidence","maximumPublicStrength","requiredAction","verificationCommand","ownerSourceId","claimId","seamIds"],"type":"object"},"publicQueueOwnedRepair":{"additionalProperties":false,"properties":{"claimId":{"$ref":"#/$defs/id"},"currentEvidence":{"$ref":"#/$defs/evidence"},"driftClass":{"$ref":"#/$defs/defectClass"},"maximumPublicStrength":{"$ref":"#/$defs/evidenceStrength"},"ownerSourceId":{"$ref":"#/$defs/id"},"ownership":{"const":"OWNED"},"publicFile":{"$ref":"#/$defs/path"},"publicQuote":{"$ref":"#/$defs/text"},"requiredAction":{"enum":["NARROW","RETIER","RETRACT","REGENERATE"],"type":"string"},"route":{"$ref":"#/$defs/text"},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"severity":{"$ref":"#/$defs/severity"},"verificationCommand":{"$ref":"#/$defs/text"}},"required":["route","publicFile","publicQuote","ownership","driftClass","severity","currentEvidence","maximumPublicStrength","requiredAction","verificationCommand","ownerSourceId","claimId","seamIds"],"type":"object"},"publicQueueOwnerless":{"additionalProperties":false,"properties":{"candidateOwners":{"items":{"$ref":"#/$defs/path"},"minItems":0,"type":"array","uniqueItems":true},"currentEvidence":{"$ref":"#/$defs/evidence"},"disposition":{"$ref":"#/$defs/text"},"driftClass":{"$ref":"#/$defs/defectClass"},"maximumPublicStrength":{"$ref":"#/$defs/evidenceStrength"},"ownerSearchEvidence":{"$ref":"#/$defs/ownerSearchEvidence"},"ownership":{"const":"OWNERLESS"},"publicFile":{"$ref":"#/$defs/path"},"publicQuote":{"$ref":"#/$defs/text"},"requiredAction":{"enum":["RETRACT","REGENERATE"],"type":"string"},"route":{"$ref":"#/$defs/text"},"severity":{"$ref":"#/$defs/severity"},"verificationCommand":{"$ref":"#/$defs/text"}},"required":["route","publicFile","publicQuote","ownership","driftClass","currentEvidence","maximumPublicStrength","requiredAction","severity","verificationCommand","ownerSearchEvidence","candidateOwners","disposition"],"type":"object"},"quantifier":{"additionalProperties":false,"properties":{"domain":{"$ref":"#/$defs/text"},"kind":{"enum":["FOR_ALL","EXISTS","EXACTLY_ONE","NONE"],"type":"string"},"variable":{"$ref":"#/$defs/text"}},"required":["variable","kind","domain"],"type":"object"},"quantumMeasurePayload":{"additionalProperties":false,"properties":{"interpretiveClaim":{"enum":["NONE","CORRESPONDENCE","LITERAL_EXTRA_DIMENSION","UNIVERSAL_COLLAPSE"],"type":"string"},"probabilityObject":{"enum":["EVENT_MEASURE","NORMALIZATION_SCALAR"],"type":"string"},"requestedOperation":{"enum":["SAMPLE_OUTCOME","CHECK_NORMALIZATION"],"type":"string"}},"required":["probabilityObject","requestedOperation","interpretiveClaim"],"type":"object"},"rawHash":{"pattern":"^sha256:[0-9a-f]{64}$","type":"string"},"receiptDescriptor":{"additionalProperties":false,"allOf":[{"if":{"properties":{"phase":{"const":"A"}},"required":["phase"]},"then":{"properties":{"dependsOnReceiptIds":{"const":[]},"id":{"const":"REC-A-108"},"path":{"const":"11_UPLINK/50_AUDITS_AND_EXECUTIONS/108_FORMAL_STRESS_LEDGER_2026_07_11.md"}}}},{"if":{"properties":{"phase":{"const":"B"}},"required":["phase"]},"then":{"properties":{"dependsOnReceiptIds":{"const":["REC-A-108"]},"id":{"const":"REC-B-109"},"path":{"const":"11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md"}}}},{"if":{"properties":{"phase":{"const":"C"}},"required":["phase"]},"then":{"properties":{"dependsOnReceiptIds":{"const":["REC-A-108","REC-B-109"]},"id":{"const":"REC-C-110"},"path":{"const":"11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_KINTSUGI_PUBLIC_PHENOTYPE_PROPAGATION_QUEUE_2026_07_11.md"}}}}],"properties":{"btjReviewPath":{"$ref":"#/$defs/path"},"claimIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"dependsOnReceiptIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"id":{"$ref":"#/$defs/id"},"logicReviewPath":{"$ref":"#/$defs/path"},"manifestId":{"$ref":"#/$defs/id"},"path":{"$ref":"#/$defs/path"},"phase":{"$ref":"#/$defs/phase"},"propagationIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"reviewAttemptId":{"$ref":"#/$defs/id"},"reviewTargetDigest":{"$ref":"#/$defs/rawHash"},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"status":{"const":"VERIFIED"},"trialIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"validationBundlePath":{"$ref":"#/$defs/path"}},"required":["id","phase","path","status","manifestId","dependsOnReceiptIds","claimIds","trialIds","seamIds","propagationIds","reviewTargetDigest","validationBundlePath","logicReviewPath","btjReviewPath","reviewAttemptId"],"type":"object"},"receiptRolePayload":{"additionalProperties":false,"properties":{"authorityRole":{"anyOf":[{"enum":["SEMANTIC_OWNER","EVIDENCE","DERIVATIVE","PROVENANCE"],"type":"string"},{"type":"null"}]},"path":{"$ref":"#/$defs/path"},"phase":{"anyOf":[{"$ref":"#/$defs/phase"},{"type":"null"}]},"receiptId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"recordKind":{"enum":["SOURCE_RECORD","PHASE_RECEIPT"],"type":"string"},"requestedUse":{"enum":["PROVENANCE","CLAIM_OWNER","PHASE_DEPENDENCY","EVIDENCE_UPGRADE","CANONICAL_PHASE_RECEIPT"],"type":"string"},"sourceKind":{"anyOf":[{"enum":["OWNER","SUPPORT","COMPRESSION","PUBLIC","RECEIPT"],"type":"string"},{"type":"null"}]},"status":{"anyOf":[{"enum":["DRAFT","COMPLETE","VERIFIED"],"type":"string"},{"type":"null"}]}},"required":["recordKind","sourceKind","authorityRole","receiptId","phase","path","status","requestedUse"],"type":"object"},"registerId":{"minLength":1,"pattern":"^[A-Z][A-Z0-9_]*$","type":"string"},"registerIndexPayload":{"additionalProperties":false,"properties":{"bridgeClaimId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"fromRegister":{"$ref":"#/$defs/registerId"},"relation":{"enum":["SAME_REGISTER","DISTINCT_TYPED_TERM","EXPLICIT_BRIDGE","UNMARKED_SUBSTITUTION"],"type":"string"},"requestedInference":{"enum":["TYPED_REFERENCE","ENTAILMENT","MECHANISM"],"type":"string"},"symbol":{"$ref":"#/$defs/text"},"toRegister":{"$ref":"#/$defs/registerId"}},"required":["symbol","fromRegister","toRegister","relation","bridgeClaimId","requestedInference"],"type":"object"},"repairKind":{"enum":["NARROW","SPLIT","RETIER","RETRACT","RENAME","RELINK"],"type":"string"},"requiredClaimBinding":{"additionalProperties":false,"allOf":[{"if":{"properties":{"requirementId":{"const":"REQ-A-PROTOCOL-SELF-TRIAL"}},"required":["requirementId"]},"then":{"properties":{"ownerAnchor":{"const":"# The Kintsugi Protocol"},"targetHash":{"const":"sha256-text-lf:9fe68c734bce6c709c5879e0f7e40b552cdacb4cd14121302371509fb13f7cc9"}}}},{"if":{"properties":{"requirementId":{"const":"REQ-A-TRIADIC-UNIQUENESS"}},"required":["requirementId"]},"then":{"properties":{"ownerAnchor":{"const":"## The Uniqueness Theorem"},"targetHash":{"const":"sha256-text-lf:438269d12273e6c169e2ba8bdb8c126dcb118378a1d28a55328aa4dbdaec17b8"}}}},{"if":{"properties":{"requirementId":{"const":"REQ-A-D6-AREA-DIRECTION"}},"required":["requirementId"]},"then":{"properties":{"ownerAnchor":{"const":"### 2.2 The Coordinate Collapse Theorem"},"targetHash":{"const":"sha256-text-lf:75893a2cd097580c3ee44a8a62f940e9b02d3dc09e4d73a5d3796e70de7d8e26"}}}},{"if":{"properties":{"requirementId":{"const":"REQ-A-POWER-MAX-CIRCULARITY"}},"required":["requirementId"]},"then":{"properties":{"ownerAnchor":{"const":"## The Statement"},"targetHash":{"const":"sha256-text-lf:8cb12ae6fb3b855cbe999d699041ae3a15c73d3c405362195f6bf58441019510"}}}},{"if":{"properties":{"requirementId":{"const":"REQ-A-D4-D5-REGISTER"}},"required":["requirementId"]},"then":{"properties":{"ownerAnchor":{"const":"## I. THE FUNDAMENTAL DISTINCTION"},"targetHash":{"const":"sha256-text-lf:dee381fece54b4fe926b1af1145ab8676263091cc698460a3b37962c77a6cca2"}}}},{"if":{"properties":{"requirementId":{"const":"REQ-A-QUANTUM-MEASURE"}},"required":["requirementId"]},"then":{"properties":{"ownerAnchor":{"const":"## The Corrected Formula"},"targetHash":{"const":"sha256-text-lf:41b8437a8e8715a7be6f8f7ddef46984b89757d9f9722494b554dc3e87d204fb"}}}},{"if":{"properties":{"requirementId":{"const":"REQ-A-OPTION-CONE"}},"required":["requirementId"]},"then":{"properties":{"ownerAnchor":{"const":"### Worldline and Light-Cone Corollary"},"targetHash":{"const":"sha256-text-lf:6749c86499b1e5d1a04de8afcbc6df283403617f1d0e40bdf9dbe66073412527"}}}}],"properties":{"claimId":{"$ref":"#/$defs/id"},"ownerAnchor":{"$ref":"#/$defs/text"},"ownerSourceId":{"$ref":"#/$defs/id"},"rationale":{"$ref":"#/$defs/text"},"requirementId":{"enum":["REQ-A-PROTOCOL-SELF-TRIAL","REQ-A-TRIADIC-UNIQUENESS","REQ-A-D6-AREA-DIRECTION","REQ-A-POWER-MAX-CIRCULARITY","REQ-A-D4-D5-REGISTER","REQ-A-QUANTUM-MEASURE","REQ-A-OPTION-CONE"],"type":"string"},"targetHash":{"$ref":"#/$defs/textHash"}},"required":["requirementId","claimId","ownerSourceId","ownerAnchor","targetHash","rationale"],"type":"object"},"residualRisk":{"additionalProperties":false,"properties":{"description":{"$ref":"#/$defs/text"},"severity":{"$ref":"#/$defs/severity"}},"required":["severity","description"],"type":"object"},"reviewAttempt":{"additionalProperties":false,"allOf":[{"if":{"properties":{"status":{"const":"PENDING"}},"required":["status"]},"then":{"oneOf":[{"properties":{"btjAttestationId":{"type":"null"},"logicAttestationId":{"type":"null"}}},{"properties":{"btjAttestationId":{"type":"null"},"logicAttestationId":{"$ref":"#/$defs/id"}}},{"properties":{"btjAttestationId":{"$ref":"#/$defs/id"},"logicAttestationId":{"type":"null"}}}],"properties":{"abandonReason":{"type":"null"}}}},{"if":{"properties":{"status":{"const":"FAILED"}},"required":["status"]},"then":{"anyOf":[{"properties":{"logicAttestationId":{"$ref":"#/$defs/id"}}},{"properties":{"btjAttestationId":{"$ref":"#/$defs/id"}}}],"properties":{"abandonReason":{"type":"null"}}}},{"if":{"properties":{"status":{"const":"PASSED"}},"required":["status"]},"then":{"properties":{"abandonReason":{"type":"null"},"btjAttestationId":{"$ref":"#/$defs/id"},"logicAttestationId":{"$ref":"#/$defs/id"}}}},{"if":{"properties":{"status":{"const":"ABANDONED"}},"required":["status"]},"then":{"properties":{"abandonReason":{"$ref":"#/$defs/text"}}}}],"properties":{"abandonReason":{"anyOf":[{"$ref":"#/$defs/text"},{"type":"null"}]},"btjAttestationId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"btjReviewPath":{"$ref":"#/$defs/path"},"id":{"minLength":1,"pattern":"^RVA-[ABC]-(?:00[1-9]|0[1-9][0-9]|[1-9][0-9]{2,})$","type":"string"},"logicAttestationId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"logicReviewPath":{"$ref":"#/$defs/path"},"phase":{"$ref":"#/$defs/phase"},"receiptId":{"$ref":"#/$defs/id"},"reviewSubjectDigest":{"$ref":"#/$defs/rawHash"},"reviewTargetPath":{"$ref":"#/$defs/path"},"status":{"enum":["PENDING","FAILED","PASSED","ABANDONED"],"type":"string"},"supersedesAttemptId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"validationBundlePath":{"$ref":"#/$defs/path"}},"required":["id","phase","receiptId","supersedesAttemptId","reviewTargetPath","logicReviewPath","btjReviewPath","validationBundlePath","logicAttestationId","btjAttestationId","status","abandonReason","reviewSubjectDigest"],"type":"object"},"reviewAttemptArtifact":{"additionalProperties":false,"properties":{"attemptId":{"$ref":"#/$defs/id"},"btjReviewSha256":{"anyOf":[{"$ref":"#/$defs/rawHash"},{"type":"null"}]},"logicReviewSha256":{"anyOf":[{"$ref":"#/$defs/rawHash"},{"type":"null"}]},"reviewTargetSha256":{"anyOf":[{"$ref":"#/$defs/rawHash"},{"type":"null"}]}},"required":["attemptId","reviewTargetSha256","logicReviewSha256","btjReviewSha256"],"type":"object"},"reviewAttestation":{"additionalProperties":false,"allOf":[{"if":{"properties":{"verdict":{"const":"PASS"}},"required":["verdict"]},"then":{"properties":{"openSevereFindingIds":{"maxItems":0}}}},{"if":{"properties":{"kind":{"const":"LOGIC"}},"required":["kind"]},"then":{"properties":{"approvedGateSeamIds":{"maxItems":0}}}},{"if":{"properties":{"kind":{"const":"BTJ"}},"required":["kind"]},"then":{"properties":{"approvedUpgradeSeamIds":{"maxItems":0}}}},{"if":{"properties":{"verdict":{"const":"FAIL"}},"required":["verdict"]},"then":{"properties":{"findingIds":{"minItems":1},"openSevereFindingIds":{"minItems":1}}}}],"properties":{"approvedGateSeamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"approvedUpgradeSeamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"attemptId":{"$ref":"#/$defs/id"},"findingIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"id":{"$ref":"#/$defs/id"},"independenceStatement":{"$ref":"#/$defs/text"},"kind":{"enum":["LOGIC","BTJ"],"type":"string"},"openSevereFindingIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"path":{"$ref":"#/$defs/path"},"receiptId":{"$ref":"#/$defs/id"},"reviewTargetDigest":{"$ref":"#/$defs/rawHash"},"reviewerId":{"$ref":"#/$defs/text"},"reviewerRole":{"$ref":"#/$defs/text"},"verdict":{"enum":["PASS","FAIL"],"type":"string"}},"required":["id","kind","path","receiptId","reviewerId","reviewerRole","independenceStatement","reviewTargetDigest","verdict","findingIds","openSevereFindingIds","approvedUpgradeSeamIds","approvedGateSeamIds","attemptId"],"type":"object"},"reviewFinding":{"additionalProperties":false,"properties":{"attemptId":{"$ref":"#/$defs/id"},"category":{"enum":["LOGIC","EVIDENCE","BEAUTY","JUSTICE","PROVENANCE","SCOPE","PROCESS"],"type":"string"},"claimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"id":{"$ref":"#/$defs/id"},"ledgerSectionIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"receiptIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"reviewKind":{"enum":["LOGIC","BTJ"],"type":"string"},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"severity":{"$ref":"#/$defs/severity"},"statement":{"$ref":"#/$defs/text"},"subjectPaths":{"items":{"$ref":"#/$defs/path"},"minItems":0,"type":"array","uniqueItems":true}},"required":["id","attemptId","reviewKind","category","severity","statement","claimIds","seamIds","subjectPaths","ledgerSectionIds","receiptIds"],"type":"object"},"reviewFindingDisposition":{"additionalProperties":false,"allOf":[{"if":{"properties":{"disposition":{"const":"ADDRESSED"}},"required":["disposition"]},"then":{"anyOf":[{"properties":{"claimIds":{"minItems":1}}},{"properties":{"seamIds":{"minItems":1}}},{"properties":{"ledgerSectionIds":{"minItems":1}}},{"properties":{"receiptIds":{"minItems":1}}},{"properties":{"subjectPaths":{"minItems":1}}}],"properties":{"discriminatorIds":{"maxItems":0},"evidenceFiles":{"maxItems":0}}}},{"if":{"properties":{"disposition":{"const":"DISPUTED"}},"required":["disposition"]},"then":{"properties":{"discriminatorIds":{"minItems":1},"evidenceFiles":{"maxItems":0}}}},{"if":{"properties":{"disposition":{"const":"PROCESS_INVALID"}},"required":["disposition"]},"then":{"properties":{"claimIds":{"maxItems":0},"discriminatorIds":{"maxItems":0},"evidenceFiles":{"minItems":1},"ledgerSectionIds":{"maxItems":0},"receiptIds":{"maxItems":0},"seamIds":{"maxItems":0},"subjectPaths":{"maxItems":0}}}}],"properties":{"claimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"discriminatorIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"disposition":{"enum":["ADDRESSED","DISPUTED","PROCESS_INVALID"],"type":"string"},"evidenceFiles":{"items":{"$ref":"#/$defs/reviewProcessEvidence"},"minItems":0,"type":"array","uniqueItems":true},"findingId":{"$ref":"#/$defs/id"},"fromAttemptId":{"$ref":"#/$defs/id"},"id":{"$ref":"#/$defs/id"},"ledgerSectionIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"rationale":{"$ref":"#/$defs/text"},"receiptIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"subjectPaths":{"items":{"$ref":"#/$defs/path"},"minItems":0,"type":"array","uniqueItems":true},"successorAttemptId":{"$ref":"#/$defs/id"}},"required":["id","findingId","fromAttemptId","successorAttemptId","disposition","rationale","claimIds","seamIds","discriminatorIds","subjectPaths","evidenceFiles","ledgerSectionIds","receiptIds"],"type":"object"},"reviewFindingDispositionInput":{"additionalProperties":false,"allOf":[{"if":{"properties":{"disposition":{"const":"ADDRESSED"}},"required":["disposition"]},"then":{"anyOf":[{"properties":{"claimIds":{"minItems":1}}},{"properties":{"seamIds":{"minItems":1}}},{"properties":{"ledgerSectionIds":{"minItems":1}}},{"properties":{"receiptIds":{"minItems":1}}},{"properties":{"subjectPaths":{"minItems":1}}}],"properties":{"discriminatorIds":{"maxItems":0},"evidenceFiles":{"maxItems":0}}}},{"if":{"properties":{"disposition":{"const":"DISPUTED"}},"required":["disposition"]},"then":{"properties":{"discriminatorIds":{"minItems":1},"evidenceFiles":{"maxItems":0}}}},{"if":{"properties":{"disposition":{"const":"PROCESS_INVALID"}},"required":["disposition"]},"then":{"properties":{"claimIds":{"maxItems":0},"discriminatorIds":{"maxItems":0},"evidenceFiles":{"minItems":1},"ledgerSectionIds":{"maxItems":0},"receiptIds":{"maxItems":0},"seamIds":{"maxItems":0},"subjectPaths":{"maxItems":0}}}}],"properties":{"claimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"discriminatorIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"disposition":{"enum":["ADDRESSED","DISPUTED","PROCESS_INVALID"],"type":"string"},"evidenceFiles":{"items":{"$ref":"#/$defs/reviewProcessEvidence"},"minItems":0,"type":"array","uniqueItems":true},"findingId":{"$ref":"#/$defs/id"},"ledgerSectionIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"rationale":{"$ref":"#/$defs/text"},"receiptIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"seamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"subjectPaths":{"items":{"$ref":"#/$defs/path"},"minItems":0,"type":"array","uniqueItems":true}},"required":["findingId","disposition","rationale","claimIds","seamIds","subjectPaths","discriminatorIds","evidenceFiles","ledgerSectionIds","receiptIds"],"type":"object"},"reviewProcessEvidence":{"additionalProperties":false,"properties":{"path":{"$ref":"#/$defs/path"},"sha256":{"$ref":"#/$defs/rawHash"}},"required":["path","sha256"],"type":"object"},"reviewSeamProjection":{"additionalProperties":false,"allOf":[{"if":{"properties":{"verdict":{"const":"VALID_SOUND"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"SUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"const":"VALID_CONDITIONAL"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"CONDITIONALLY_SUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"const":"VALID_UNSUPPORTED_PREMISE"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"UNSUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"enum":["INVALID","UNDERDETERMINED"]}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"NOT_APPLICABLE"},"validityVerdict":{"const":"INVALID"}}}},{"if":{"properties":{"verdict":{"const":"DEFINITIONAL"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"NOT_APPLICABLE"},"validityVerdict":{"const":"NOT_APPLICABLE"}}}},{"if":{"properties":{"verdict":{"const":"OPEN_CONJECTURE"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"enum":["UNSUPPORTED","CONDITIONALLY_SUPPORTED"]},"validityVerdict":{"const":"NOT_APPLICABLE"}}}},{"if":{"properties":{"verdict":{"const":"REFUTED"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"REFUTED"},"validityVerdict":{"enum":["VALID","NOT_APPLICABLE"]}}}},{"else":{"properties":{"justiceContext":{"type":"null"}}},"if":{"anyOf":[{"properties":{"justiceScope":{"enum":["COLLECTIVE","NORMATIVE","COLLECTIVE_NORMATIVE"]}},"required":["justiceScope"]},{"properties":{"authorityEffect":{"enum":["DESCRIPTIVE","DISCRETIONARY","CONSEQUENTIAL","CONSTITUTIONAL_AUTOMATIC"]}},"required":["authorityEffect"]}]},"then":{"required":["justiceContext"]}},{"if":{"properties":{"claimType":{"const":"NORMATIVE"}},"required":["claimType"]},"then":{"properties":{"justiceScope":{"enum":["NORMATIVE","COLLECTIVE_NORMATIVE"]}}}},{"if":{"properties":{"modality":{"const":"NORMATIVE"}},"required":["modality"]},"then":{"properties":{"justiceScope":{"enum":["NORMATIVE","COLLECTIVE_NORMATIVE"]}}}},{"if":{"properties":{"authorityEffect":{"const":"NONE"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"const":"NONE"},"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"NONE"},"regime":{"const":"NOT_APPLICABLE"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"enum":["PRIVATE_DAV","PUBLIC_DAV","OTHER"]}},"required":["justiceContext"]}},{"if":{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"enum":["PRIVATE_DAV","PUBLIC_DAV","OTHER"]}},"required":["justiceContext"]}},{"if":{"properties":{"authorityEffect":{"const":"CONSTITUTIONAL_AUTOMATIC"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"const":"PUBLIC_DAV"},"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"CONSTITUTIONAL_AUTO_ENFORCEMENT"},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"OTHER"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"PRISM_PUBLIC_GOVERNANCE"},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"OTHER"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromC"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromC"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromC"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromC"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromC"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromC"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromI"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromI"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromI"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromI"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromS"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromS"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromS"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromS"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromS"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromS"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromA"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromA"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromA"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromA"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromA"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromA"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killNone"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killTestable"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killNone"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killTestable"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killNone"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killTestable"}}}},{"if":{"properties":{"status":{"const":"CONFIRMED"}},"required":["status"]},"then":{"properties":{"afterQuote":{"type":"null"},"containment":{"type":"null"},"evidenceAfter":{"type":"null"},"repairKind":{"type":"null"},"residualRisk":{"type":"null"},"upgradeEvidenceLinkIds":{"type":"null"}}}},{"if":{"properties":{"status":{"const":"HELD_OPEN"}},"required":["status"]},"then":{"properties":{"afterQuote":{"type":"null"},"discriminatorIds":{"minItems":1},"evidenceAfter":{"type":"null"},"repairKind":{"type":"null"},"upgradeEvidenceLinkIds":{"type":"null"}},"required":["containment","residualRisk"]}},{"if":{"properties":{"status":{"const":"REPAIRED"}},"required":["status"]},"then":{"properties":{"containment":{"type":"null"},"repairKind":{"enum":["NARROW","SPLIT","RETIER","RENAME","RELINK"]},"residualRisk":{"type":"null"}},"required":["repairKind","afterQuote","evidenceAfter"]}},{"if":{"properties":{"status":{"const":"RETRACTED"}},"required":["status"]},"then":{"oneOf":[{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]}],"properties":{"containment":{"type":"null"},"evidenceAfter":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]},"killCriterion":{"$ref":"#/$defs/killNone"},"priorKillCriterion":{"$ref":"#/$defs/killRetract"},"repairKind":{"const":"RETRACT"},"residualRisk":{"type":"null"},"upgradeEvidenceLinkIds":{"type":"null"}},"required":["repairKind","afterQuote","evidenceAfter"]}},{"else":{"properties":{"upgradeEvidenceLinkIds":{"type":"null"}}},"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"repairKind":{"const":"RETIER"}},"required":["upgradeEvidenceLinkIds"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"repairKind":{"const":"RETIER"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","REPAIRED","RETRACTED"]}},"required":["status"]},{"properties":{"countermodel":{"properties":{"defeatedConclusion":{"const":"NONE_FOUND"}},"required":["defeatedConclusion"]}},"required":["countermodel"]}]},"then":{"properties":{"discriminatorIds":{"minItems":1}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeAvailableTargetI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeAvailableTargetS"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeAvailableTargetA"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killRetierToC"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killRetierToI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killRetierToS"}}}},{"if":{"properties":{"repairKind":{"const":"RETIER"}},"required":["repairKind"]},"then":{"oneOf":[{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]}]}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"OTHER"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"OTHER"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}}],"properties":{"afterQuote":{"$ref":"#/$defs/text"},"authorityEffect":{"$ref":"#/$defs/authorityEffect"},"authorityScope":{"$ref":"#/$defs/authorityScope"},"beautyGate":{"$ref":"#/$defs/gateRationale"},"beforeHash":{"$ref":"#/$defs/textHash"},"beforeQuote":{"$ref":"#/$defs/text"},"claimId":{"$ref":"#/$defs/id"},"claimType":{"$ref":"#/$defs/claimType"},"conclusion":{"$ref":"#/$defs/text"},"containment":{"$ref":"#/$defs/containment"},"countermodel":{"$ref":"#/$defs/countermodel"},"credit":{"$ref":"#/$defs/credit"},"creditConsent":{"enum":["NAMED","ALIAS","ANONYMOUS"],"type":"string"},"defectClass":{"$ref":"#/$defs/defectClass"},"dependencyClaimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"discriminatorIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"evidenceAfter":{"$ref":"#/$defs/evidence"},"evidenceBefore":{"$ref":"#/$defs/evidence"},"id":{"$ref":"#/$defs/id"},"inference":{"$ref":"#/$defs/inference"},"justiceContext":{"$ref":"#/$defs/justiceContext"},"justiceGate":{"$ref":"#/$defs/gateRationale"},"justiceScope":{"$ref":"#/$defs/justiceScope"},"killCriterion":{"$ref":"#/$defs/killCriterion"},"modality":{"$ref":"#/$defs/modality"},"ownerAnchor":{"$ref":"#/$defs/text"},"ownerSource":{"$ref":"#/$defs/id"},"premises":{"items":{"$ref":"#/$defs/premise"},"minItems":1,"type":"array","uniqueItems":true},"priorKillCriterion":{"$ref":"#/$defs/killCriterion"},"priorSeamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"priorSupportLinks":{"items":{"$ref":"#/$defs/supportLink"},"minItems":0,"type":"array","uniqueItems":true},"priorSurvivingIfKilled":{"$ref":"#/$defs/survivingIfKilled"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterion"},"quantifiers":{"items":{"$ref":"#/$defs/quantifier"},"minItems":1,"type":"array","uniqueItems":true},"receiptId":{"$ref":"#/$defs/id"},"regressionFixtureIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"repairKind":{"$ref":"#/$defs/repairKind"},"residualRisk":{"$ref":"#/$defs/residualRisk"},"scope":{"$ref":"#/$defs/scope"},"severity":{"$ref":"#/$defs/severity"},"soundnessVerdict":{"$ref":"#/$defs/soundnessVerdict"},"sourceIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"status":{"enum":["CONFIRMED","REPAIRED","HELD_OPEN","RETRACTED"],"type":"string"},"supportLinks":{"items":{"$ref":"#/$defs/supportLink"},"minItems":0,"type":"array","uniqueItems":true},"survivingIfKilled":{"$ref":"#/$defs/survivingIfKilled"},"survivingKernel":{"$ref":"#/$defs/text"},"truthGate":{"$ref":"#/$defs/gateRationale"},"typedTerms":{"items":{"$ref":"#/$defs/typedTerm"},"minItems":1,"type":"array","uniqueItems":true},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterion"},"upgradeEvidenceLinkIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"validityVerdict":{"$ref":"#/$defs/validityVerdict"},"verdict":{"$ref":"#/$defs/overallVerdict"}},"required":["id","claimId","ownerSource","ownerAnchor","beforeQuote","beforeHash","priorSeamIds","claimType","typedTerms","premises","conclusion","inference","quantifiers","modality","scope","justiceScope","authorityScope","authorityEffect","evidenceBefore","sourceIds","dependencyClaimIds","countermodel","defectClass","severity","validityVerdict","soundnessVerdict","verdict","survivingKernel","priorSupportLinks","priorUpgradeCriterion","priorKillCriterion","priorSurvivingIfKilled","supportLinks","upgradeCriterion","killCriterion","survivingIfKilled","beautyGate","truthGate","justiceGate","credit","creditConsent","receiptId","regressionFixtureIds","discriminatorIds","status"],"type":"object"},"reviewTarget":{"additionalProperties":false,"properties":{"antibodies":{"items":{"$ref":"#/$defs/antibody"},"minItems":0,"type":"array","uniqueItems":true},"claims":{"items":{"$ref":"#/$defs/claim"},"minItems":1,"type":"array","uniqueItems":true},"currentAttemptId":{"$ref":"#/$defs/id"},"discriminators":{"items":{"$ref":"#/$defs/discriminator"},"minItems":0,"type":"array","uniqueItems":true},"fixtures":{"items":{"$ref":"#/$defs/fixture"},"minItems":0,"type":"array","uniqueItems":true},"ledgerPreambleRawSha256":{"$ref":"#/$defs/rawHash"},"ledgerSemanticSections":{"items":{"$ref":"#/$defs/ledgerSemanticSection"},"minItems":0,"type":"array","uniqueItems":true},"manifest":{"$ref":"#/$defs/manifest"},"phase":{"$ref":"#/$defs/phase"},"priorReviewAttemptArtifacts":{"items":{"$ref":"#/$defs/reviewAttemptArtifact"},"minItems":0,"type":"array","uniqueItems":true},"priorReviewAttempts":{"items":{"$ref":"#/$defs/reviewAttempt"},"minItems":0,"type":"array","uniqueItems":true},"priorReviewAttestations":{"items":{"$ref":"#/$defs/reviewAttestation"},"minItems":0,"type":"array","uniqueItems":true},"priorReviewFindingDispositions":{"items":{"$ref":"#/$defs/reviewFindingDisposition"},"minItems":0,"type":"array","uniqueItems":true},"priorReviewFindings":{"items":{"$ref":"#/$defs/reviewFinding"},"minItems":0,"type":"array","uniqueItems":true},"propagations":{"items":{"$ref":"#/$defs/propagation"},"minItems":0,"type":"array","uniqueItems":true},"receiptId":{"$ref":"#/$defs/id"},"receiptNarrativeRawSha256":{"$ref":"#/$defs/rawHash"},"reviewSubjectDigest":{"$ref":"#/$defs/rawHash"},"schemaSha256":{"$ref":"#/$defs/rawHash"},"schemaVersion":{"const":"1.0.0"},"seams":{"items":{"$ref":"#/$defs/reviewSeamProjection"},"minItems":0,"type":"array","uniqueItems":true},"semanticDiffPaths":{"items":{"$ref":"#/$defs/path"},"minItems":1,"type":"array","uniqueItems":true},"sources":{"items":{"$ref":"#/$defs/source"},"minItems":1,"type":"array","uniqueItems":true},"trials":{"items":{"$ref":"#/$defs/trial"},"minItems":1,"type":"array","uniqueItems":true}},"required":["schemaVersion","phase","manifest","sources","claims","trials","seams","propagations","antibodies","discriminators","fixtures","schemaSha256","ledgerSemanticSections","semanticDiffPaths","priorReviewAttempts","priorReviewAttemptArtifacts","currentAttemptId","receiptId","reviewSubjectDigest","priorReviewAttestations","priorReviewFindings","priorReviewFindingDispositions","receiptNarrativeRawSha256","ledgerPreambleRawSha256"],"type":"object"},"rosettaTransferPayload":{"additionalProperties":false,"properties":{"bridgeClaimId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"fromRegister":{"$ref":"#/$defs/registerId"},"requestedTransfer":{"enum":["VOCABULARY","QUESTION","TOPOLOGY","ENTAILMENT","MECHANISM","NECESSITY","EVIDENCE_UPGRADE"],"type":"string"},"targetClaimId":{"$ref":"#/$defs/id"},"toRegister":{"$ref":"#/$defs/registerId"}},"required":["targetClaimId","bridgeClaimId","fromRegister","toRegister","requestedTransfer"],"type":"object"},"scope":{"additionalProperties":false,"properties":{"conditions":{"items":{"$ref":"#/$defs/text"},"minItems":0,"type":"array"},"domain":{"$ref":"#/$defs/text"},"population":{"$ref":"#/$defs/text"},"timeHorizon":{"$ref":"#/$defs/text"}},"required":["domain","population","timeHorizon","conditions"],"type":"object"},"seam":{"additionalProperties":false,"allOf":[{"if":{"properties":{"verdict":{"const":"VALID_SOUND"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"SUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"const":"VALID_CONDITIONAL"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"CONDITIONALLY_SUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"const":"VALID_UNSUPPORTED_PREMISE"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"UNSUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"enum":["INVALID","UNDERDETERMINED"]}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"NOT_APPLICABLE"},"validityVerdict":{"const":"INVALID"}}}},{"if":{"properties":{"verdict":{"const":"DEFINITIONAL"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"NOT_APPLICABLE"},"validityVerdict":{"const":"NOT_APPLICABLE"}}}},{"if":{"properties":{"verdict":{"const":"OPEN_CONJECTURE"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"enum":["UNSUPPORTED","CONDITIONALLY_SUPPORTED"]},"validityVerdict":{"const":"NOT_APPLICABLE"}}}},{"if":{"properties":{"verdict":{"const":"REFUTED"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"REFUTED"},"validityVerdict":{"enum":["VALID","NOT_APPLICABLE"]}}}},{"else":{"properties":{"justiceContext":{"type":"null"}}},"if":{"anyOf":[{"properties":{"justiceScope":{"enum":["COLLECTIVE","NORMATIVE","COLLECTIVE_NORMATIVE"]}},"required":["justiceScope"]},{"properties":{"authorityEffect":{"enum":["DESCRIPTIVE","DISCRETIONARY","CONSEQUENTIAL","CONSTITUTIONAL_AUTOMATIC"]}},"required":["authorityEffect"]}]},"then":{"required":["justiceContext"]}},{"if":{"properties":{"claimType":{"const":"NORMATIVE"}},"required":["claimType"]},"then":{"properties":{"justiceScope":{"enum":["NORMATIVE","COLLECTIVE_NORMATIVE"]}}}},{"if":{"properties":{"modality":{"const":"NORMATIVE"}},"required":["modality"]},"then":{"properties":{"justiceScope":{"enum":["NORMATIVE","COLLECTIVE_NORMATIVE"]}}}},{"if":{"properties":{"authorityEffect":{"const":"NONE"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"const":"NONE"},"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"NONE"},"regime":{"const":"NOT_APPLICABLE"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"enum":["PRIVATE_DAV","PUBLIC_DAV","OTHER"]}},"required":["justiceContext"]}},{"if":{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"enum":["PRIVATE_DAV","PUBLIC_DAV","OTHER"]}},"required":["justiceContext"]}},{"if":{"properties":{"authorityEffect":{"const":"CONSTITUTIONAL_AUTOMATIC"}},"required":["authorityEffect"]},"then":{"properties":{"authorityScope":{"const":"PUBLIC_DAV"},"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"CONSTITUTIONAL_AUTO_ENFORCEMENT"},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"OTHER"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","K2_NATURAL_PERSON","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"PRISM_PUBLIC_GOVERNANCE"},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"authorityEffect":{"enum":["DISCRETIONARY","CONSEQUENTIAL"]}},"required":["authorityEffect"]},{"properties":{"authorityScope":{"const":"OTHER"}},"required":["authorityScope"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["NONE","PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT","OTHER"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromC"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromC"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromC"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromC"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromC"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromC"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromI"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromI"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromI"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromI"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromS"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromS"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromS"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromS"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromS"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromS"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killCriterionFromA"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromA"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromA"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromA"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killCriterionFromA"},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterionFromA"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killNone"}}}},{"if":{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killTestable"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killNone"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killTestable"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killNone"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"killCriterion":{"$ref":"#/$defs/killTestable"}}}},{"if":{"properties":{"status":{"const":"CONFIRMED"}},"required":["status"]},"then":{"properties":{"afterQuote":{"type":"null"},"containment":{"type":"null"},"evidenceAfter":{"type":"null"},"repairKind":{"type":"null"},"residualRisk":{"type":"null"},"upgradeEvidenceLinkIds":{"type":"null"}}}},{"if":{"properties":{"status":{"const":"HELD_OPEN"}},"required":["status"]},"then":{"properties":{"afterQuote":{"type":"null"},"discriminatorIds":{"minItems":1},"evidenceAfter":{"type":"null"},"repairKind":{"type":"null"},"upgradeEvidenceLinkIds":{"type":"null"}},"required":["containment","residualRisk"]}},{"if":{"properties":{"status":{"const":"REPAIRED"}},"required":["status"]},"then":{"properties":{"containment":{"type":"null"},"repairKind":{"enum":["NARROW","SPLIT","RETIER","RENAME","RELINK"]},"residualRisk":{"type":"null"}},"required":["repairKind","afterQuote","evidenceAfter"]}},{"if":{"properties":{"status":{"const":"RETRACTED"}},"required":["status"]},"then":{"oneOf":[{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]}],"properties":{"containment":{"type":"null"},"evidenceAfter":{"properties":{"lifecycle":{"const":"RETIRED"}},"required":["lifecycle"]},"killCriterion":{"$ref":"#/$defs/killNone"},"priorKillCriterion":{"$ref":"#/$defs/killRetract"},"repairKind":{"const":"RETRACT"},"residualRisk":{"type":"null"},"upgradeEvidenceLinkIds":{"type":"null"}},"required":["repairKind","afterQuote","evidenceAfter"]}},{"else":{"properties":{"upgradeEvidenceLinkIds":{"type":"null"}}},"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"repairKind":{"const":"RETIER"}},"required":["upgradeEvidenceLinkIds"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"repairKind":{"const":"RETIER"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"countermodel":{"properties":{"defeatedConclusion":{"const":"NONE_FOUND"}},"required":["defeatedConclusion"]}},"required":["countermodel"]}]},"then":{"properties":{"discriminatorIds":{"minItems":1}}}},{"if":{"properties":{"status":{"const":"VERIFIED"}},"required":["status"]},"then":{"properties":{"beautyGate":{"$ref":"#/$defs/gatePass"},"containment":{"type":"null"},"justiceGate":{"$ref":"#/$defs/gatePass"},"repairKind":{"enum":["NARROW","SPLIT","RETIER","RENAME","RELINK"]},"residualRisk":{"type":"null"},"truthGate":{"$ref":"#/$defs/gatePass"}},"required":["repairKind","afterQuote","evidenceAfter"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeAvailableTargetI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeAvailableTargetS"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeAvailableTargetA"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killRetierToC"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]},{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killRetierToI"}}}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","VERIFIED"]}},"required":["status"]},{"anyOf":[{"allOf":[{"properties":{"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceAfter"]}]}]}]},"then":{"properties":{"priorKillCriterion":{"$ref":"#/$defs/killRetierToS"}}}},{"if":{"properties":{"repairKind":{"const":"RETIER"}},"required":["repairKind"]},"then":{"oneOf":[{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"A"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"S"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"C"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"I"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"A"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"S"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]},{"properties":{"evidenceAfter":{"properties":{"strength":{"const":"I"}},"required":["strength"]},"evidenceBefore":{"properties":{"strength":{"const":"C"}},"required":["strength"]}},"required":["evidenceBefore","evidenceAfter"]}]}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["CONFIRMED","HELD_OPEN"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"OTHER"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceBefore":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceBefore"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PRIVATE_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"K2_NATURAL_PERSON"},"regime":{"const":"PRIVATE_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"PUBLIC_DAV"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"enum":["PRISM_PUBLIC_GOVERNANCE","CONSTITUTIONAL_AUTO_ENFORCEMENT"]},"regime":{"const":"PUBLIC_DAV"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}},{"if":{"allOf":[{"properties":{"status":{"enum":["REPAIRED","RETRACTED","VERIFIED"]}},"required":["status"]},{"properties":{"authorityEffect":{"const":"DESCRIPTIVE"},"authorityScope":{"const":"OTHER"}},"required":["authorityEffect","authorityScope"]},{"properties":{"evidenceAfter":{"properties":{"lifecycle":{"enum":["DRAFT","ACTIVE"]}},"required":["lifecycle"]}},"required":["evidenceAfter"]}]},"then":{"properties":{"justiceContext":{"properties":{"authority":{"properties":{"mechanism":{"const":"OTHER"},"regime":{"const":"OTHER"}},"required":["regime","mechanism"]}},"required":["authority"]}},"required":["justiceContext"]}}],"properties":{"afterQuote":{"$ref":"#/$defs/text"},"authorityEffect":{"$ref":"#/$defs/authorityEffect"},"authorityScope":{"$ref":"#/$defs/authorityScope"},"beautyGate":{"$ref":"#/$defs/gate"},"beforeHash":{"$ref":"#/$defs/textHash"},"beforeQuote":{"$ref":"#/$defs/text"},"claimId":{"$ref":"#/$defs/id"},"claimType":{"$ref":"#/$defs/claimType"},"conclusion":{"$ref":"#/$defs/text"},"containment":{"$ref":"#/$defs/containment"},"countermodel":{"$ref":"#/$defs/countermodel"},"credit":{"$ref":"#/$defs/credit"},"creditConsent":{"enum":["NAMED","ALIAS","ANONYMOUS"],"type":"string"},"defectClass":{"$ref":"#/$defs/defectClass"},"dependencyClaimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"discriminatorIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"evidenceAfter":{"$ref":"#/$defs/evidence"},"evidenceBefore":{"$ref":"#/$defs/evidence"},"id":{"$ref":"#/$defs/id"},"inference":{"$ref":"#/$defs/inference"},"justiceContext":{"$ref":"#/$defs/justiceContext"},"justiceGate":{"$ref":"#/$defs/gate"},"justiceScope":{"$ref":"#/$defs/justiceScope"},"killCriterion":{"$ref":"#/$defs/killCriterion"},"modality":{"$ref":"#/$defs/modality"},"ownerAnchor":{"$ref":"#/$defs/text"},"ownerSource":{"$ref":"#/$defs/id"},"premises":{"items":{"$ref":"#/$defs/premise"},"minItems":1,"type":"array","uniqueItems":true},"priorKillCriterion":{"$ref":"#/$defs/killCriterion"},"priorSeamIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"priorSupportLinks":{"items":{"$ref":"#/$defs/supportLink"},"minItems":0,"type":"array","uniqueItems":true},"priorSurvivingIfKilled":{"$ref":"#/$defs/survivingIfKilled"},"priorUpgradeCriterion":{"$ref":"#/$defs/upgradeCriterion"},"quantifiers":{"items":{"$ref":"#/$defs/quantifier"},"minItems":1,"type":"array","uniqueItems":true},"receiptId":{"$ref":"#/$defs/id"},"regressionFixtureIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"repairKind":{"$ref":"#/$defs/repairKind"},"residualRisk":{"$ref":"#/$defs/residualRisk"},"scope":{"$ref":"#/$defs/scope"},"severity":{"$ref":"#/$defs/severity"},"soundnessVerdict":{"$ref":"#/$defs/soundnessVerdict"},"sourceIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"status":{"enum":["CONFIRMED","REPAIRED","HELD_OPEN","RETRACTED","VERIFIED"],"type":"string"},"supportLinks":{"items":{"$ref":"#/$defs/supportLink"},"minItems":0,"type":"array","uniqueItems":true},"survivingIfKilled":{"$ref":"#/$defs/survivingIfKilled"},"survivingKernel":{"$ref":"#/$defs/text"},"truthGate":{"$ref":"#/$defs/gate"},"typedTerms":{"items":{"$ref":"#/$defs/typedTerm"},"minItems":1,"type":"array","uniqueItems":true},"upgradeCriterion":{"$ref":"#/$defs/upgradeCriterion"},"upgradeEvidenceLinkIds":{"items":{"$ref":"#/$defs/id"},"minItems":1,"type":"array","uniqueItems":true},"validityVerdict":{"$ref":"#/$defs/validityVerdict"},"verdict":{"$ref":"#/$defs/overallVerdict"}},"required":["id","claimId","ownerSource","ownerAnchor","beforeQuote","beforeHash","priorSeamIds","claimType","typedTerms","premises","conclusion","inference","quantifiers","modality","scope","justiceScope","authorityScope","authorityEffect","evidenceBefore","sourceIds","dependencyClaimIds","countermodel","defectClass","severity","validityVerdict","soundnessVerdict","verdict","survivingKernel","priorSupportLinks","priorUpgradeCriterion","priorKillCriterion","priorSurvivingIfKilled","supportLinks","upgradeCriterion","killCriterion","survivingIfKilled","beautyGate","truthGate","justiceGate","credit","creditConsent","receiptId","regressionFixtureIds","discriminatorIds","status"],"type":"object"},"severity":{"enum":["CRITICAL","MAJOR","MINOR"],"type":"string"},"soundnessVerdict":{"enum":["SUPPORTED","CONDITIONALLY_SUPPORTED","UNSUPPORTED","REFUTED","NOT_APPLICABLE"],"type":"string"},"source":{"additionalProperties":false,"allOf":[{"if":{"properties":{"kind":{"const":"OWNER"}},"required":["kind"]},"then":{"properties":{"authorityRole":{"const":"SEMANTIC_OWNER"}}}},{"if":{"properties":{"kind":{"const":"SUPPORT"}},"required":["kind"]},"then":{"properties":{"authorityRole":{"enum":["EVIDENCE","PROVENANCE"]}}}},{"if":{"properties":{"kind":{"enum":["COMPRESSION","PUBLIC"]}},"required":["kind"]},"then":{"properties":{"authorityRole":{"const":"DERIVATIVE"}}}},{"if":{"properties":{"kind":{"const":"RECEIPT"}},"required":["kind"]},"then":{"properties":{"authorityRole":{"const":"PROVENANCE"}}}}],"properties":{"authorityRole":{"enum":["SEMANTIC_OWNER","EVIDENCE","DERIVATIVE","PROVENANCE"],"type":"string"},"id":{"$ref":"#/$defs/id"},"kind":{"enum":["OWNER","SUPPORT","COMPRESSION","PUBLIC","RECEIPT"],"type":"string"},"path":{"$ref":"#/$defs/path"},"phases":{"items":{"$ref":"#/$defs/phase"},"minItems":1,"type":"array","uniqueItems":true},"sha256":{"$ref":"#/$defs/rawHash"}},"required":["id","path","kind","phases","sha256","authorityRole"],"type":"object"},"supportLink":{"additionalProperties":false,"allOf":[{"else":{"properties":{"independenceStatus":{"enum":["INDEPENDENT","PARTIALLY_INDEPENDENT","NOT_INDEPENDENT","NOT_ASSESSED"]}}},"if":{"properties":{"mode":{"enum":["ANALOGY","ROSETTA_TRANSFER"]}},"required":["mode"]},"then":{"properties":{"evidenceCeiling":{"const":"I"},"independenceStatus":{"const":"NOT_APPLICABLE"}}}}],"properties":{"evidenceCeiling":{"$ref":"#/$defs/evidenceStrength"},"id":{"$ref":"#/$defs/id"},"independenceStatus":{"enum":["INDEPENDENT","PARTIALLY_INDEPENDENT","NOT_INDEPENDENT","NOT_ASSESSED","NOT_APPLICABLE"],"type":"string"},"mode":{"enum":["CORROBORATION","REPLICATION","ANALOGY","ROSETTA_TRANSFER"],"type":"string"},"rationale":{"$ref":"#/$defs/text"},"supportingClaimId":{"$ref":"#/$defs/id"}},"required":["id","supportingClaimId","mode","independenceStatus","evidenceCeiling","rationale"],"type":"object"},"survivingIfKilled":{"additionalProperties":false,"properties":{"claimIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"rationale":{"$ref":"#/$defs/text"}},"required":["claimIds","rationale"],"type":"object"},"text":{"minLength":1,"type":"string"},"textHash":{"pattern":"^sha256-text-lf:[0-9a-f]{64}$","type":"string"},"trial":{"additionalProperties":false,"allOf":[{"if":{"properties":{"verdict":{"const":"VALID_SOUND"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"SUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"const":"VALID_CONDITIONAL"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"CONDITIONALLY_SUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"const":"VALID_UNSUPPORTED_PREMISE"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"UNSUPPORTED"},"validityVerdict":{"const":"VALID"}}}},{"if":{"properties":{"verdict":{"enum":["INVALID","UNDERDETERMINED"]}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"NOT_APPLICABLE"},"validityVerdict":{"const":"INVALID"}}}},{"if":{"properties":{"verdict":{"const":"DEFINITIONAL"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"NOT_APPLICABLE"},"validityVerdict":{"const":"NOT_APPLICABLE"}}}},{"if":{"properties":{"verdict":{"const":"OPEN_CONJECTURE"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"enum":["UNSUPPORTED","CONDITIONALLY_SUPPORTED"]},"validityVerdict":{"const":"NOT_APPLICABLE"}}}},{"if":{"properties":{"verdict":{"const":"REFUTED"}},"required":["verdict"]},"then":{"properties":{"soundnessVerdict":{"const":"REFUTED"},"validityVerdict":{"enum":["VALID","NOT_APPLICABLE"]}}}},{"if":{"properties":{"breakState":{"const":"NONE"}},"required":["breakState"]},"then":{"properties":{"defectClass":{"type":"null"},"discriminatorIds":{"minItems":0},"seamId":{"type":"null"},"severity":{"type":"null"},"status":{"const":"CLOSED"}}}},{"if":{"properties":{"breakState":{"const":"ALLEGED"}},"required":["breakState"]},"then":{"properties":{"defectClass":{"$ref":"#/$defs/defectClass"},"seamId":{"type":"null"},"severity":{"$ref":"#/$defs/severity"},"status":{"enum":["TRIED","DISPUTED"]}}}},{"if":{"properties":{"breakState":{"const":"CONFIRMED"}},"required":["breakState"]},"then":{"properties":{"defectClass":{"$ref":"#/$defs/defectClass"},"seamId":{"$ref":"#/$defs/id"},"severity":{"$ref":"#/$defs/severity"},"status":{"enum":["ADJUDICATED","CLOSED"]}}}},{"if":{"allOf":[{"properties":{"breakState":{"enum":["ALLEGED","CONFIRMED"]}},"required":["breakState"]},{"properties":{"countermodel":{"properties":{"defeatedConclusion":{"const":"NONE_FOUND"}},"required":["defeatedConclusion"]}},"required":["countermodel"]}]},"then":{"properties":{"discriminatorIds":{"minItems":1}}}}],"properties":{"breakState":{"enum":["NONE","ALLEGED","CONFIRMED"],"type":"string"},"claimId":{"$ref":"#/$defs/id"},"countermodel":{"$ref":"#/$defs/countermodel"},"defectClass":{"anyOf":[{"$ref":"#/$defs/defectClass"},{"type":"null"}]},"discriminatorIds":{"items":{"$ref":"#/$defs/id"},"minItems":0,"type":"array","uniqueItems":true},"id":{"$ref":"#/$defs/id"},"manifestId":{"$ref":"#/$defs/id"},"receiptId":{"$ref":"#/$defs/id"},"seamId":{"anyOf":[{"$ref":"#/$defs/id"},{"type":"null"}]},"severity":{"anyOf":[{"$ref":"#/$defs/severity"},{"type":"null"}]},"soundnessVerdict":{"$ref":"#/$defs/soundnessVerdict"},"status":{"enum":["TRIED","DISPUTED","ADJUDICATED","CLOSED"],"type":"string"},"steelman":{"$ref":"#/$defs/text"},"triedHash":{"$ref":"#/$defs/textHash"},"triedQuote":{"$ref":"#/$defs/text"},"validityVerdict":{"$ref":"#/$defs/validityVerdict"},"verdict":{"$ref":"#/$defs/overallVerdict"}},"required":["id","claimId","manifestId","triedQuote","triedHash","steelman","countermodel","breakState","defectClass","severity","validityVerdict","soundnessVerdict","verdict","discriminatorIds","seamId","receiptId","status"],"type":"object"},"trophicAggregatorPayload":{"additionalProperties":false,"properties":{"aggregationBasis":{"enum":["DECLARED_PROXY","MEASURED_PHYSICAL_SUM","METAPHORICAL"],"type":"string"},"carrierTurnoverObserved":{"type":"boolean"},"conservationClaim":{"enum":["NONE","EMPIRICALLY_TESTED","ASSUMED"],"type":"string"},"laterSelectionReweightingObserved":{"type":"boolean"},"persistentSharedTrace":{"type":"boolean"},"quantityKind":{"enum":["HUMAN_INVESTMENT_PROXY","PHYSICAL_ENERGY"],"type":"string"},"requestedInference":{"enum":["DESCRIPTIVE_AGGREGATION","EGREGOREOTYPE_CANDIDATE","LITERAL_ENERGY_LAW"],"type":"string"}},"required":["quantityKind","aggregationBasis","conservationClaim","persistentSharedTrace","carrierTurnoverObserved","laterSelectionReweightingObserved","requestedInference"],"type":"object"},"typedTerm":{"additionalProperties":false,"properties":{"definition":{"$ref":"#/$defs/text"},"semanticRegister":{"$ref":"#/$defs/registerId"},"symbol":{"$ref":"#/$defs/text"},"type":{"$ref":"#/$defs/text"}},"required":["symbol","type","definition","semanticRegister"],"type":"object"},"upgradeAvailable":{"additionalProperties":false,"allOf":[{"if":{"properties":{"targetStrength":{"const":"A"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"const":"A"}}}},{"if":{"properties":{"targetStrength":{"const":"S"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S"]}}}},{"if":{"properties":{"targetStrength":{"const":"I"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S","I"]}}}}],"properties":{"criterion":{"$ref":"#/$defs/text"},"kind":{"const":"AVAILABLE"},"minimumEvidenceCeiling":{"enum":["A","S","I"],"type":"string"},"minimumIndependence":{"enum":["PARTIALLY_INDEPENDENT","INDEPENDENT"],"type":"string"},"requiredMode":{"enum":["CORROBORATION","REPLICATION"],"type":"string"},"targetStrength":{"enum":["A","S","I"],"type":"string"}},"required":["kind","targetStrength","criterion","requiredMode","minimumIndependence","minimumEvidenceCeiling"],"type":"object"},"upgradeAvailableTargetA":{"additionalProperties":false,"allOf":[{"if":{"properties":{"targetStrength":{"const":"A"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"const":"A"}}}},{"if":{"properties":{"targetStrength":{"const":"S"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S"]}}}},{"if":{"properties":{"targetStrength":{"const":"I"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S","I"]}}}}],"properties":{"criterion":{"$ref":"#/$defs/text"},"kind":{"const":"AVAILABLE"},"minimumEvidenceCeiling":{"enum":["A","S","I"],"type":"string"},"minimumIndependence":{"enum":["PARTIALLY_INDEPENDENT","INDEPENDENT"],"type":"string"},"requiredMode":{"enum":["CORROBORATION","REPLICATION"],"type":"string"},"targetStrength":{"enum":["A"],"type":"string"}},"required":["kind","targetStrength","criterion","requiredMode","minimumIndependence","minimumEvidenceCeiling"],"type":"object"},"upgradeAvailableTargetI":{"additionalProperties":false,"allOf":[{"if":{"properties":{"targetStrength":{"const":"A"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"const":"A"}}}},{"if":{"properties":{"targetStrength":{"const":"S"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S"]}}}},{"if":{"properties":{"targetStrength":{"const":"I"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S","I"]}}}}],"properties":{"criterion":{"$ref":"#/$defs/text"},"kind":{"const":"AVAILABLE"},"minimumEvidenceCeiling":{"enum":["A","S","I"],"type":"string"},"minimumIndependence":{"enum":["PARTIALLY_INDEPENDENT","INDEPENDENT"],"type":"string"},"requiredMode":{"enum":["CORROBORATION","REPLICATION"],"type":"string"},"targetStrength":{"enum":["I"],"type":"string"}},"required":["kind","targetStrength","criterion","requiredMode","minimumIndependence","minimumEvidenceCeiling"],"type":"object"},"upgradeAvailableTargetS":{"additionalProperties":false,"allOf":[{"if":{"properties":{"targetStrength":{"const":"A"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"const":"A"}}}},{"if":{"properties":{"targetStrength":{"const":"S"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S"]}}}},{"if":{"properties":{"targetStrength":{"const":"I"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S","I"]}}}}],"properties":{"criterion":{"$ref":"#/$defs/text"},"kind":{"const":"AVAILABLE"},"minimumEvidenceCeiling":{"enum":["A","S","I"],"type":"string"},"minimumIndependence":{"enum":["PARTIALLY_INDEPENDENT","INDEPENDENT"],"type":"string"},"requiredMode":{"enum":["CORROBORATION","REPLICATION"],"type":"string"},"targetStrength":{"enum":["S"],"type":"string"}},"required":["kind","targetStrength","criterion","requiredMode","minimumIndependence","minimumEvidenceCeiling"],"type":"object"},"upgradeCriterion":{"oneOf":[{"$ref":"#/$defs/upgradeAvailable"},{"$ref":"#/$defs/upgradeNone"}]},"upgradeCriterionFromA":{"$ref":"#/$defs/upgradeNone"},"upgradeCriterionFromC":{"oneOf":[{"additionalProperties":false,"allOf":[{"if":{"properties":{"targetStrength":{"const":"A"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"const":"A"}}}},{"if":{"properties":{"targetStrength":{"const":"S"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S"]}}}},{"if":{"properties":{"targetStrength":{"const":"I"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S","I"]}}}}],"properties":{"criterion":{"$ref":"#/$defs/text"},"kind":{"const":"AVAILABLE"},"minimumEvidenceCeiling":{"enum":["A","S","I"],"type":"string"},"minimumIndependence":{"enum":["PARTIALLY_INDEPENDENT","INDEPENDENT"],"type":"string"},"requiredMode":{"enum":["CORROBORATION","REPLICATION"],"type":"string"},"targetStrength":{"enum":["I","S","A"],"type":"string"}},"required":["kind","targetStrength","criterion","requiredMode","minimumIndependence","minimumEvidenceCeiling"],"type":"object"},{"$ref":"#/$defs/upgradeNone"}]},"upgradeCriterionFromI":{"oneOf":[{"additionalProperties":false,"allOf":[{"if":{"properties":{"targetStrength":{"const":"A"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"const":"A"}}}},{"if":{"properties":{"targetStrength":{"const":"S"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S"]}}}},{"if":{"properties":{"targetStrength":{"const":"I"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S","I"]}}}}],"properties":{"criterion":{"$ref":"#/$defs/text"},"kind":{"const":"AVAILABLE"},"minimumEvidenceCeiling":{"enum":["A","S","I"],"type":"string"},"minimumIndependence":{"enum":["PARTIALLY_INDEPENDENT","INDEPENDENT"],"type":"string"},"requiredMode":{"enum":["CORROBORATION","REPLICATION"],"type":"string"},"targetStrength":{"enum":["S","A"],"type":"string"}},"required":["kind","targetStrength","criterion","requiredMode","minimumIndependence","minimumEvidenceCeiling"],"type":"object"},{"$ref":"#/$defs/upgradeNone"}]},"upgradeCriterionFromS":{"oneOf":[{"additionalProperties":false,"allOf":[{"if":{"properties":{"targetStrength":{"const":"A"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"const":"A"}}}},{"if":{"properties":{"targetStrength":{"const":"S"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S"]}}}},{"if":{"properties":{"targetStrength":{"const":"I"}},"required":["targetStrength"]},"then":{"properties":{"minimumEvidenceCeiling":{"enum":["A","S","I"]}}}}],"properties":{"criterion":{"$ref":"#/$defs/text"},"kind":{"const":"AVAILABLE"},"minimumEvidenceCeiling":{"enum":["A","S","I"],"type":"string"},"minimumIndependence":{"enum":["PARTIALLY_INDEPENDENT","INDEPENDENT"],"type":"string"},"requiredMode":{"enum":["CORROBORATION","REPLICATION"],"type":"string"},"targetStrength":{"enum":["A"],"type":"string"}},"required":["kind","targetStrength","criterion","requiredMode","minimumIndependence","minimumEvidenceCeiling"],"type":"object"},{"$ref":"#/$defs/upgradeNone"}]},"upgradeNone":{"additionalProperties":false,"properties":{"kind":{"const":"NONE"},"rationale":{"$ref":"#/$defs/text"}},"required":["kind","rationale"],"type":"object"},"validationBundle":{"additionalProperties":false,"allOf":[{"else":{"properties":{"publicQueueSha256":{"type":"null"}}},"if":{"properties":{"phase":{"const":"C"}},"required":["phase"]},"then":{"properties":{"publicQueueSha256":{"$ref":"#/$defs/rawHash"}}}}],"properties":{"antibodies":{"items":{"$ref":"#/$defs/antibody"},"minItems":0,"type":"array","uniqueItems":true},"btjReviewSha256":{"$ref":"#/$defs/rawHash"},"claims":{"items":{"$ref":"#/$defs/claim"},"minItems":1,"type":"array","uniqueItems":true},"dependencyReceipts":{"items":{"$ref":"#/$defs/dependencyReceipt"},"minItems":0,"type":"array","uniqueItems":true},"discriminators":{"items":{"$ref":"#/$defs/discriminator"},"minItems":0,"type":"array","uniqueItems":true},"fixtures":{"items":{"$ref":"#/$defs/fixture"},"minItems":0,"type":"array","uniqueItems":true},"ledgerPreambleRawSha256":{"$ref":"#/$defs/rawHash"},"ledgerSections":{"items":{"$ref":"#/$defs/ledgerSection"},"minItems":0,"type":"array","uniqueItems":true},"logicReviewSha256":{"$ref":"#/$defs/rawHash"},"manifest":{"$ref":"#/$defs/manifest"},"phase":{"$ref":"#/$defs/phase"},"propagations":{"items":{"$ref":"#/$defs/propagation"},"minItems":0,"type":"array","uniqueItems":true},"publicQueueSha256":{"anyOf":[{"$ref":"#/$defs/rawHash"},{"type":"null"}]},"receiptDescriptor":{"$ref":"#/$defs/receiptDescriptor"},"receiptNarrativeRawSha256":{"$ref":"#/$defs/rawHash"},"reviewAttemptArtifacts":{"items":{"$ref":"#/$defs/reviewAttemptArtifact"},"minItems":1,"type":"array","uniqueItems":true},"reviewAttempts":{"items":{"$ref":"#/$defs/reviewAttempt"},"minItems":1,"type":"array","uniqueItems":true},"reviewAttestations":{"items":{"$ref":"#/$defs/reviewAttestation"},"minItems":1,"type":"array","uniqueItems":true},"reviewFindingDispositions":{"items":{"$ref":"#/$defs/reviewFindingDisposition"},"minItems":0,"type":"array","uniqueItems":true},"reviewFindings":{"items":{"$ref":"#/$defs/reviewFinding"},"minItems":0,"type":"array","uniqueItems":true},"reviewTargetDigest":{"$ref":"#/$defs/rawHash"},"schemaSha256":{"$ref":"#/$defs/rawHash"},"schemaVersion":{"const":"1.0.0"},"seams":{"items":{"$ref":"#/$defs/seam"},"minItems":0,"type":"array","uniqueItems":true},"sources":{"items":{"$ref":"#/$defs/source"},"minItems":1,"type":"array","uniqueItems":true},"trials":{"items":{"$ref":"#/$defs/trial"},"minItems":1,"type":"array","uniqueItems":true}},"required":["schemaVersion","phase","receiptDescriptor","reviewTargetDigest","manifest","sources","claims","trials","seams","propagations","antibodies","discriminators","fixtures","schemaSha256","ledgerSections","logicReviewSha256","btjReviewSha256","publicQueueSha256","dependencyReceipts","reviewAttempts","reviewAttemptArtifacts","reviewAttestations","reviewFindings","reviewFindingDispositions","receiptNarrativeRawSha256","ledgerPreambleRawSha256"],"type":"object"},"validityVerdict":{"enum":["VALID","INVALID","NOT_APPLICABLE"],"type":"string"},"verdictMatrixPayload":{"additionalProperties":false,"properties":{"soundnessVerdict":{"$ref":"#/$defs/soundnessVerdict"},"validityVerdict":{"$ref":"#/$defs/validityVerdict"},"verdict":{"$ref":"#/$defs/overallVerdict"}},"required":["validityVerdict","soundnessVerdict","verdict"],"type":"object"}},"$id":"https://emergentism.org/schema/kintsugi/1.0.0","$schema":"https://json-schema.org/draft/2020-12/schema"}
```
