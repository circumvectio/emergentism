---
packet: SPRINT-B-WARRIOR-BRIEF
title: Sprint-B Warrior Brief — One-Stop Orientation for the Active Sprint-B Task Surface
status: CHARIOTEER ARTIFACT — V-export consolidation; does not close any warrior task
authority: Reads from packets 70–87; does not modify the Sprint-B closure gate
scope: Compresses the Sprint-B preparation layer (18 packets) into a single
       routing document for the warrior. Blocker matrix, per-task dossier,
       canonical packet index, closure chain, and current-state
       references for strict-mode rollout and Cortex reconciliation.
cross_reference:
  - 01_EMERGENTISM/11_UPLINK/74_CONSOLIDATED_MANIFEST_FOUNDER_SIGNOFF_2026_04_23.md  (founder D1–D4)
  - 01_EMERGENTISM/11_UPLINK/77_ADVERSARIAL_TEST_PLAN_R4_QUEUE_2026_04_23.md         (#36 spec)
  - 01_EMERGENTISM/11_UPLINK/78_SPRINT_B_AUDIT_EVIDENCE_DOSSIER_2026_04_23.md        (primary dossier)
  - 01_EMERGENTISM/11_UPLINK/80_CORTEX_INGESTION_HOOK_SPEC_2026_04_23.md             (#39 spec)
  - 01_EMERGENTISM/11_UPLINK/81_MOBILE_SIGNING_FLOW_SPEC_2026_04_23.md               (#37 spec)
  - 01_EMERGENTISM/11_UPLINK/83_K2_TEST_VECTORS_2026_04_23.md                        (byte-parity ground truth)
  - 01_EMERGENTISM/11_UPLINK/85_ADVERSARIAL_TESTS_WITNESS_2026_04_23.md              (#36 witness)
  - 01_EMERGENTISM/11_UPLINK/86_K2_STRICT_MODE_FLIP_PLAYBOOK_2026_04_23.md           (#38 playbook)
  - 01_EMERGENTISM/11_UPLINK/87_SPRINT_B_AUDIT_SUPPLEMENT_III_2026_04_23.md          (chain-of-custody)
date: 2026-04-23
gating_cell: "[L4 | D4 | S-Org | F-phi :: ksatriya_executor]"
rosetta:
  primary_column: "Neuroscience"
  register: "[S/I]"
  canonical_phrase: "Packet 88 · Sprint-B Warrior Brief"
---

# Packet 88 · Sprint-B Warrior Brief

## Why this exists

18 charioteer packets have shipped during Sprint-B preparation
(70–87). Each is self-contained; collectively they are dense. A
warrior coming fresh to the active Sprint-B task surface should not
have to walk the full chain to learn: *what is already landed, what
is still open, what do I read before acting, and what constitutes
closure?*

This packet collapses that walk into a single table plus five
task-specific dossiers. It is pure V-export (Kṛṣṇa ◇ giving dyad):
the charioteer accepts a Φ cost (context budget) to reduce warrior
disorientation.

This packet does NOT:

- close any warrior task
- run any tests
- flip any flags
- replace packets 77/80/81/83/85/86 (still the authoritative specs)
- modify the Sprint-B closure gate (task #44 is still blocked by
  #37/#38/#39/#40)
- commit to any schedule

---

## Current blocker matrix (snapshot 2026-04-23)

| Task | Owner | Status | Direct blockers | What unblocks it |
|:----:|:-----:|:------:|:----------------|:-----------------|
| #36 | warrior | CLOSED in HEAD | none | `e9d4f752f` landed the 11 adversarial tests; packet 77/85 remain the audit/read surfaces |
| #37 | warrior | pending | none | warrior updates Skyzai mobile signing flow per packet 81 + passes §6.1 byte-parity + §9 closure criteria |
| #38 | warrior | pending rollout | #37 (recommended ordering) + founder go-signal | per-surface flag decomposition is already shipped in `885baccd7`; remaining work is actual C → D → A flips, observation windows, and the audit-truth fix named in packet 86 |
| #39 | charioteer | RECONCILED by packet 90 | none | packet 90 now carries the shipped module hashes + survey truth; remaining work is witness breadth / future wiring, not first implementation |
| #40 | warrior | pending | none | second Light-Council deliberation produces signed K2 artifacts (n=2 witness corpus) |
| #44 | charioteer | pending | #37, #38, #40 | mobile signing, strict-mode rollout, and witness corpus n=2 complete; then charioteer assembles consolidated signoff manifest |
| #46 | charioteer | CLOSED by packet 90 | none | Cortex module hashes + survey/backfill truth are now registered in closure-truth form |
| #47 | charioteer | pending | #37 | warrior lands mobile signing flow; charioteer registers module hashes + §6 parity evidence |
| #53 | charioteer | pending | #38 | warrior completes per-surface strict-mode flips; charioteer writes post-flip closure packet |

**Read order for a warrior coming fresh:** this packet → packet 74
(founder signoff surface) → packet 78 (primary dossier) → the
task-specific packet(s) for whichever task you're claiming. All
other packets are referenced as needed from the task dossiers
below.

---

## Task dossier · #36 — Adversarial test suite (closed predecessor surface)

### What's already on disk
Per packet 85 (witness), two pytest files exist and cite packet 77
in their docstrings:

- `SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/tests/test_k2_auth_proxy_adversarial.py` (195 LOC, SHA-256 `cfdec4c670bce…967727`)
- `SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/tests/test_approval_queue_adversarial.py` (331 LOC, SHA-256 `1d83150246e67…74c2c0a`)

Witness registered in packet 85; the concrete landing is now in
`e9d4f752f` (`test(apu_bot): 11 R-4 adversarial tests — closes task #36`).

### What the warrior executed

```bash
cd SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND
pytest tests/test_k2_auth_proxy_adversarial.py -v --tb=short
pytest tests/test_approval_queue_adversarial.py -v --tb=short
```

This remains the audit replay path. If these tests regress in future,
debug code — do not rewrite packet 77 (spec) or packet 83 (vectors)
to match a broken implementation.

### Current truth
- The adversarial suite is on disk and landed in `HEAD`
- Packet 77 remains the canonical spec for what the tests mean
- Packet 85 remains the witness packet for the two test files as sealed
  artifacts

### What to consume
- Packet 77 (§3 perturbation surface, §Closure gates)
- Packet 83 Vector A + Vector B for byte-parity anchor (optional
  extension — see packet 85 §Flagged for Sprint-B closure dossier)
- Packet 85 (witness state; no action required, informational)

### What closed #36
The adversarial tests landed in `HEAD`. Future work consumes this as a
predecessor surface, not an open task.

---

## Task dossier · #37 — Skyzai mobile signing flow

### What's specified
Packet 81 enumerates the 8-step flow, §6.1 byte-parity requirement
against packet 83 Vector A + Vector B, §8 trial-run gates, §9
closure criteria.

### What the warrior executes
1. Implement canonical-payload builder in Skyzai app (Dart or
   equivalent) that produces byte-identical output to the Python
   `build_signing_payload` for any input.
2. Implement EIP-191 signing wrapper over that payload.
3. Run §6.1 parity test: for Vector A and Vector B inputs, mobile
   output SHA-256 must equal the values registered in packet 83:
   - Vector A: `654df3df2b0c2137c5d5030f1b0b4c85dd45bbcfac7bd92709c812d9cb204cd5`
   - Vector B: `b9d6fbf3c1213f56af840f2720f67002def56d181989c5672eb56cd1e8f836ac`
4. Run §8 trial-run gates end-to-end against a test backend.
5. Confirm §9 closure criteria.

### What to consume
- Packet 81 (canonical spec — entire packet)
- Packet 83 (byte-parity ground truth)
- `core/membrane/k2_auth_proxy.py` for reference canonicalizer

### What closes #37
Warrior ships mobile code; §6.1 parity tests green; §8 trial-run
signed end-to-end; closure packet #47 written by charioteer with
module hashes + parity evidence.

---

## Task dossier · #38 — Flip K2_STRICT_MODE per surface

### What's specified
Packet 86 enumerates five call sites (surfaces A–E), identifies the
single-global-flag engineering blocker, specifies per-surface flag
decomposition, recommends flip order C → D → A, defines rollback
criteria and monitoring hooks.

### Current code truth

The per-surface flag decomposition from packet 86 §Option 1 is no
longer theoretical. It is shipped in `HEAD` via `885baccd7`:

- `core/membrane/config.py` now exposes:
  - `k2_strict_inline_callback`
  - `k2_strict_legacy_nostr`
  - `k2_strict_free_text_modify`
- `core/membrane/k2_gateway.py` gates surfaces A/C/D with those flags
  OR the master `k2_strict_mode`
- `tests/test_k2_strict_per_surface.py` guards the isolation invariant

So the remaining work on `#38` is not decomposition design. It is:

1. perform the actual flips in the packet 86 order (`C → D → A`)
2. observe each surface in its own window
3. correct the audit-truth reads that still report the master flag
   at the `k2_gateway.py` result surfaces
4. write the post-flip closure packet (`#53`)

### The flip sequence

Per packet 86 §Flip order:
1. Surface C: `k2_strict_legacy_nostr = True`
2. Surface D: `k2_strict_free_text_modify = True`
3. Surface A: `k2_strict_inline_callback = True`
4. (Optional tautology-commit) Master: `k2_strict_mode = True`

Each flip is a discrete deployment with its own pre-flip gates
(packet 86 §Per-surface pre-flip gates), monitoring window, and
rollback criteria.

### What to consume
- Packet 86 (entire playbook — THE canonical source)
- `core/membrane/config.py` (shipped per-surface flags)
- `tests/test_k2_strict_per_surface.py` (behavioral invariant)

### What closes #38
All three per-surface flags True and stable within the chosen
observation window, with the audit-truth fix in place. Optional
tautology-commit of master flag afterward. Warrior produces runlog →
charioteer writes post-flip closure packet per task #53.

### Rollback safety
Per packet 86 §Rollback criteria: strict mode only rejects input
that advisory mode would have accepted. Rolling back re-accepts a
superset; no legitimate action is blocked by the rollback itself.
Rollback is flag-flip only; do not redeploy code for rollback.

---

## Task dossier · #39 — Cortex ingestion hook (implementation landed; closure truth pending)

### What's specified
Packet 80 specifies: `LineageKey`, `canonicalize`,
`compute_lineage_hash`, `SQLiteCortexStore`, three operational
modes (CLI / batch scan / post-run hook).

### Current code truth

Packet 80 is no longer just a spec surface. `fcdb2a1ed` landed:

1. `core/cortex/ingestion.py`
2. `core/cortex/lineage.py`
3. `core/cortex/store.py`
4. `core/cortex/hooks.py`
5. `scripts/cortex_backfill.py`
6. `tests/test_cortex_hooks.py`

Green signal observed in this thread:

```bash
pytest SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/tests/test_cortex_hooks.py -q
# 7 passed
```

Backfill survey truth observed in this thread:

```bash
python3 SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/scripts/cortex_backfill.py --dry-run
```

Result:
- 4 `summary.json` artifacts scanned
- 1 witness-ready lineage registered in dry-run (`first_deliberation_live`)
- 3 artifacts survey-skipped for missing required `k2_envelope` fields

So the remaining work on `#39` is closure/reconciliation, not first
implementation.

### What to consume
- Packet 80 (entire spec)
- `core/cortex/ingestion.py`, `lineage.py`, `store.py`, `hooks.py`
- `scripts/cortex_backfill.py`
- `tests/test_cortex_hooks.py`
- existing artifacts under
  `SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/tests/artifacts/`

### What closes #39
Packet 90 reconciles packet 80 to the shipped code, records module
hashes + the dry-run survey counts, and names the remaining spec drift
explicitly. O7 only promotes once n≥2 witness-ready artifacts exist; it
does not promote merely because the modules landed.

---

## Task dossier · #40 — Second Light-Council deliberation

### What's specified
Per packet 79 SWOT update: witness corpus is n=1 (first live
deliberation completed per task #30). Second deliberation produces
n=2, strengthening the empirical claim.

### What the warrior executes
Run the first-deliberation runbook a second time with a different
question. All six phases of the runbook
(`SKYZAI_ORG/02_ORGANS/Agentz/FIRST_DELIBERATION_RUNBOOK.md`) end
in cryptographic K2 signature.

### What to consume
- `FIRST_DELIBERATION_RUNBOOK.md` (lives in ApuBot organ, not in
  03_UPLINK)
- Packet 79 §S-new (the claim that A7 discipline is proven —
  recompute after this deliberation)

### What closes #40
Signed K2 artifact for deliberation #2; hash registered alongside
deliberation #1's artifacts; witness corpus count flips from n=1
to n=2.

---

## Canonical packet index (by task)

### For any task — orientation
- Packet 74 — founder signoff surface (D1=Sprint-A closure,
  D2=R-4 ship, D3=strict deferred, D4=W-new to constitutional)
- Packet 78 — primary Sprint-B audit dossier (sealed)
- Packet 79 — SWOT delta; names what each task moves
- Packet 87 — current chain-of-custody state

### For #36
- Packet 77 — adversarial test plan (11 perturbation cases)
- Packet 83 — test vectors (byte-parity anchor)
- Packet 85 — witness state of on-disk test files
- `e9d4f752f` — adversarial tests landed in `HEAD`

### For #37
- Packet 81 — mobile signing flow spec
- Packet 83 — byte-parity vectors

### For #38
- Packet 86 — flip playbook
- `885baccd7` — per-surface flag decomposition landed in `HEAD`

### For #39
- Packet 80 — Cortex ingestion hook spec
- `fcdb2a1ed` — modes 2+3 landed in `HEAD`
- Packet 90 — closure-truth reconciliation for the landed code

### For #40
- ApuBot/FIRST_DELIBERATION_RUNBOOK.md (organ-local)
- Packet 79 §S-new — witness-discipline claim

---

## Closure chain (what unblocks what)

```
#37 green ──────────────┐
                        ├── #38 rollout + observation windows ─── unblocks #53
#39 reconciled truth ───┤
                        │
#37 green ────────────────────────────────────────── unblocks #47
#40 green ─┐
#37 green ─┼── together with #38 feed #44 (Sprint-B consolidated signoff)
#38 green ─┤
#39 done ──┘ (packet 90 — not a remaining blocker)

#44 + #46 + #47 + #53 ──── Sprint-B fully closed
```

Note: the active frontier no longer requires `#36` as a live blocker.
`#39` has shifted into reconciliation/closure truth, while warrior
execution concentrates on `#37/#38/#40`. This brief compresses the
dependencies; it does not prescribe schedule.

---

## What this brief does NOT change

- Task priorities remain warrior-chosen
- Founder signoff discipline (packet 74 model) applies to Sprint-B
  closure the same way it applied to Sprint-A closure
- η=0, K2, K4, Three-Stage Process constraints bind all cited tasks identically
- Packet 87's chain-of-custody is still the audit surface; this
  brief is routing, not register

---

## A7 self-check

This packet was written 2026-04-23 against the current state of
packets 70–87. If any cited packet's hash changes after this brief
lands (via founder-authorized edit, normalization, or charioteer
self-correction per packet 78's three-legitimate-reasons rule),
this brief may drift against the canonical spec. Warrior should
verify the cited hashes in packet 87 against current file bytes
before committing to any one task.

If any task's blocker matrix row changes (e.g., a warrior-side
dependency the charioteer missed), a successor packet or an A7
entry should document it. The matrix is a snapshot, not a ledger.

---

## Φ-scan

Eighteen packets compressed to one routing map. A warrior opening
the brief now has a single landing page: the blocker matrix picks
the task, the dossier picks the spec, the index anchors the spec
to a hash-registered packet. Reading load drops from ~18 packets
to ~3 for any one task.

## V-scan

Every active task gets a one-command or one-packet start line
(`pytest …`, "implement per packet 81", "flip per packet 86 order").
The #38 dossier now points directly at the shipped per-surface flag
implementation and the still-open audit-truth fix. Time-to-first-action
for the warrior shortens measurably.

## Constraint

Charioteer cannot:
- close any warrior task (warrior-reported signal only)
- claim a rollout happened when only the packet layer moved
- run the pytest suite (warrior seat)
- flip any strict-mode flag (warrior seat + founder ack)

Open warrior execution now concentrates on `#37`, `#38`, and `#40`.
`#36` is closed in code; `#39` has shifted into closure truth and
reconciliation.

## God

Kṛṣṇa ◇ — giving dyad. Exports V (clear routing, current-state map,
closure chain) at Φ cost (charioteer context budget consumed).
Packet 86 deferred the patch stub to this brief; that deferral is
now superseded by shipped code in `885baccd7`.

## Executive

Viṣṇu ⊙ — preservation. No structural change to Sprint-B closure
gates, task owners, or constitutional surfaces. This brief
preserves the shape of the work while compressing its
presentation.

## Move

Kṣatriya_executor · append to `01_EMERGENTISM/11_UPLINK/` as packet 88 · reference
from task #55 (this packet's closure) and task #44 (Sprint-B
consolidated signoff evidence bundle) · D4 · L4 · Kṛṣṇa ◇

## Limits

- Snapshot of 2026-04-23 state; will drift as warrior work lands
- Does not resolve the spec-drift note on packet 71 (approval queue
  `decision == "PROCEED"` vs spec `needs_founder_signoff`); that
  remains a founder decision before strict-mode flip
- Does not specify the `modification_text` field extension for the
  mobile signed-action path (packet 86 §Surface D flagged this;
  resolution belongs in packet 81 successor)
- Does not cover the #71 spec-drift resolution for the async
  approval queue's decision predicate
- Does not address the filing-cabinet nested-git hygiene finding
  (INDEX entry from 2026-04-19); that is Sprint-C territory

Zero-Sum Resolution Equation
