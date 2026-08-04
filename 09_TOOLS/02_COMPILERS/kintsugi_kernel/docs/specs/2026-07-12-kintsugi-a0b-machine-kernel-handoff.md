# Kintsugi A0B Machine-Kernel Handoff

**Record date:** 2026-07-12

**Observed:** 2026-07-17
**Status:** `[B]` reproducible local machine evidence; `[D]` handoff scope.

This record transfers a tested machine grammar, not semantic authority. A0B
validates grammar and transaction machinery. It does not validate Emergentism,
repair canon, or create a live Kintsugi vessel. The compiler remains downstream
from source-owned doctrine.

See the [compiler front door](../../../09_TOOLS/02_COMPILERS/README.md), the
[controlling addendum](2026-07-12-kintsugi-a0b-machine-kernel-addendum.md), and
the [implementation plan](../plans/2026-07-12-kintsugi-a0b-machine-kernel-implementation.md).

## Frozen identities

| Object | Identity |
|---|---|
| Immutable baseline | `26e616e651e2a87e8c85bf37db515d7fcd007b7b` |
| A0 head | `181559a370598e1ae7572c33d21369ef6c6419e2` |
| Schema raw SHA-256 | `f8c4205af97635f8eea9f83cbf3a1e05ff50a0f64bc6ee8dd54ff61f6df78a3f` |
| Baseline contract SHA-256 | `74496df660f0ca989f293c30db652b8f9aeb78beb30fa91fe249d87ee29ef69b` |
| Task 8 head | `e62d9a815b4579397e4fabd1e707d65f5dcab0fd` |

Named Kintsugi endpoints are Task 1 `b5707cb`, Task 2 terminal `eb70b2c`, Task
3 terminal `7a7e8dd`, Task 4 terminal `8bea53e`, Task 5 terminal `08ab206`, Task
6 `7fb7b0c`, Task 7 `5005204`, and Task 8 `e62d9a8`. These are endpoint
identities, not a claim that every intervening ancestry commit is Kintsugi-only;
unrelated GFS and canon commits occur between Tasks 6 and 7.

## Machine surface

The schema exposes exactly `coreData`, `publicQueue`, and `baselineAllowlist` as
selectable root roles. The public renderer operations are `freeze-manifest`,
`review-target`, `transition-core`, and `bundle`. The lifecycle is final
freeze/allocation, `TARGET_READY`, `ATTESTED`, `FAILED` or `ABANDONED`,
`COMPLETE`, then `VERIFIED`.

The renderer enforces a shared Git-common-directory lock, expected-HEAD and
raw-core compare-and-swap before and inside the lock, a frozen final read set,
and rollback after partial replacement. Final `freeze-manifest` additionally
persists its attempt reservation; a failed post-reservation freeze therefore
leaves that attempt ID burned. Standalone `bundle` only preflights canonical
bytes, while `transition-core --stage VERIFIED` materializes the bundle.
Retries reuse an identical extant target, reject target drift, and allow a
same-subject successor only when the predecessor process is invalidated by
exact bound evidence.

The five history arrays are append-only. External logic, Beauty/Truth/Justice,
and finding-disposition candidates remain outside both repositories until
atomic intake. Typed-control filtering and framed ledger/receipt narrative
hashes prevent prose from impersonating state.

## Reproducible evidence

- Frozen baseline, run twice: `KIN-OK baseline collected=19 failures=5`.
- A0 compatibility: 22 tests.
- Schema and documentation: 65 tests.
- Records: 55 tests.
- Semantics: 46 tests.
- Markdown synchronization: 91 tests.
- Manifest/Git: 129 tests.
- Review: 15 tests.
- Compass mutation projection: 6 tests containing 14 ordered fallacy cases.
- Renderer: 38 tests, including rollback and concurrent-state refusal.
- `test_kintsugi_*.py`: 407 tests.
- Validator compatibility, Kintsugi, and renderer groups together: 467 tests.

The renderer and mutation suites were run twice with identical outcomes. The
through-Task-8 net scope is 27 declared paths from A0 head, its forbidden-tree
diff is empty, and Task 8 ended clean.

## Evidence limits

- There is no live manifest, core, semantic ledger, receipt, review, validation
  bundle, or public queue.
- Default `--check` remains a controlled missing-input `KIN-E-IO` state because
  `02_KINTSUGI_SEAMS.json` does not exist.
- Tests are synthetic and externally uncalibrated.
- Arbitrary baseline test bodies are not sandboxed by the validator.
- This evidence establishes no empirical, quantum, unification, deployment, or
  canon-validity conclusion.
- Task 9's final 29-path scope and commit identity remain external controller
  gates; this handoff does not certify its own future commit or independent
  review.

## A1 machine-only handoff

A1 performs exactly this sequence:

1. Freeze a stable tracked boundary and canonical-dirt inventory.
2. Create `MAN-A-001`.
3. Atomize live Phase-A sources, claims, and trials.
4. Jointly create `02_KINTSUGI_SEAMS.json` and
   `02_KINTSUGI_SEAM_LEDGER.md`.
5. Stage DRAFT `REC-A-108`.
6. Run read-only Phase-A bootstrap validation.

A2—not A1—owns external review intake and state transitions. The first live
vessel must therefore remain absent until A1 deliberately creates the complete
tracked boundary.
