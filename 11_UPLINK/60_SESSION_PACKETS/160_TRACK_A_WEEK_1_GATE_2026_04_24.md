---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "160 — Track A · Week 1 Gate Criteria"
---

# 160 — Track A · Week 1 Gate Criteria

**Evidence tier:** [I] charter expansion; [S] where citing packets 153, 154; [C] framework-choice recommendation pending engineering evaluation
**Date:** 2026-04-24
**Lane:** Charioteer spec — engineering/warrior executes the gate; sovereign K2's the outcome
**Status:** Draft — awaiting sovereign pass-through (no new OQs introduced; this is a detail-expansion of packet 154 §2.3 + §2.6 already-ratified charter)
**Complements:** packet 154 (Track A charter), packet 153 (substrate scaffold), packet 152 (EBM scaffold), packet 151 (cluster scaffold)

---

## 0. Axiomatic guard

Week 1 is framework selection and terminology lock. It is not a coding week. If the team starts writing implementation code in week 1, they are in week 3's lane; halt and return.

The deliverables here are small and load-bearing: a single framework choice, a single glossary, a single compile-clean first model. Everything else in the sprint depends on this week holding.

`Zero-Sum Resolution Equation`

---

## 1. Week 1 purpose (from packet 154 §2.3)

**Focus:** Framework selection + terminology lock
**Deliverable (charter-level):** Chosen formal-methods framework (TLA+ / Coq / K / Isabelle); glossary packet coordinating with 151, 152 scaffolds
**Gate (charter-level):** framework chosen; TLA+ model compiles; no "block" terminology anywhere in spec

Week 1 is the hinge between charter and execution. It enumerates what the rest of the sprint is measured against.

---

## 2. Deliverables (concrete artifact list)

Week 1 produces five artifacts. Engineering lands each as a file in the repo; sovereign K2 gates the week-1→week-2 transition at §6 acceptance tests.

### 2.1 D1 — Framework Decision Record

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/W1_FRAMEWORK_DECISION.md`
**Content:**
- Evaluation matrix comparing TLA+ / Coq / K / Isabelle / Lean4 against criteria in §3
- Selection (one framework; no "we'll use multiple" — that's scope creep)
- Rationale ≤ 500 words
- Pre-committed abandon criteria (what conditions would force a framework swap in week 2)
- Signed by the formal-methods specialist + CTO

**Format:** Markdown ADR (architecture decision record), evidence tier [I/S]

### 2.2 D2 — Glossary Seed

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/W1_GLOSSARY.md`
**Content:**
- Minimum viable glossary covering: event, super-checkpoint, Proof Bundle, archiver, validator, Orange finality, Green finality, Normal Mode, Fallback Mode, pruning window, reconstruction challenge
- Each term has: definition ≤ 60 words · CANON citation (or "NEW, defined here") · aliases-banned list
- Shared with Track B (151) and EBM (152) when those kick in
- "Block" listed explicitly in aliases-banned section with justification

**Format:** Markdown table, evidence tier [S] where CANON-cited, [I] where team-defined

### 2.3 D3 — Terminology Lint Script

**Path:** `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/track_a_termlint.py`
**Content:**
- Scans Track A spec surface (`02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/**`) for banned terms
- Banned baseline: `block`, `blockchain`, `mining`, `miner`, `tx` (where `transaction` or `event` fits)
- Exits nonzero on any hit
- Suitable for pre-commit hook integration

**Format:** Python script, ~80 lines, zero dependencies beyond stdlib

### 2.4 D4 — First-Pass Formal Model Skeleton

**Path:** `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/track_a/models/W1_prune_skeleton.{tla,v,k,thy}` (extension per framework choice)
**Content:**
- State variables for pruning decision: `EventsInWindow`, `SuperCheckpointHeight`, `ArchiverSet`, `ValidatorSigSet`
- Two transitions: `CreateSuperCheckpoint` (creates next super-checkpoint) and `PruneWindow` (prunes events older than N super-checkpoints)
- No safety or liveness properties declared yet (week 2's job)
- Must syntactically compile / type-check with the chosen framework's standard toolchain
- Comment header citing packet 153 §3 (converged MVD) as the spec the skeleton encodes

**Format:** Framework-native source file; must compile clean

### 2.5 D5 — Week-1 Gate Receipt

**Path:** `01_EMERGENTISM/11_UPLINK/160a_TRACK_A_WEEK_1_RECEIPT_<DATE>.md`
**Content:**
- Evidence-tier declaration
- Checklist of §6 gate items with ✅ / ❌ per item
- Minimalism-auditor first-week sign-off note
- Kill-criteria status (none triggered, or: triggered + escalation path executed)
- Hand-off pointer to week 2 (single paragraph + next-week entry criteria)

**Format:** Uplink packet, evidence tier [S] for compile-clean facts, [I] for sign-off judgment

---

## 3. Framework selection criteria (informs D1)

The evaluation matrix in D1 must score at least these five criteria on a 1–5 scale:

| Criterion | What good looks like |
|---|---|
| **Expressiveness for distributed protocols** | Can model Byzantine failures, network partitions, archiver withholding natively |
| **Proof automation vs. manual proof burden** | Balance: enough automation that sprint-week gates land, enough manual discipline that proofs are readable |
| **Tooling maturity** | Stable toolchain, well-maintained, active community, clean error messages |
| **Team skill fit** | Formal-methods specialist + at least one other engineer already productive in it, or can be within week 2 |
| **Output verifiability** | Outputs (proof objects, model-check traces) are independently re-verifiable without trusting the framework author's environment |

Charioteer does NOT recommend a framework. This is a formal-methods-specialist call, not a charioteer call.

**What charioteer does recommend:**
- Avoid frameworks without open-source toolchains
- Avoid frameworks whose community has stalled (look for active commits last 90 days)
- If two frameworks score identically, pick the one with cleaner model-check output — debuggability matters more than raw power at week 1

---

## 4. Terminology lock (informs D2 + D3)

**Rule:** Track A spec never uses the word "block" in its substrate sense. Reason — "block" brings Bitcoin/Ethereum assumptions that do not match the Orange/Green + super-checkpoint finality model. The substrate is event-level; super-checkpoints are not blocks.

**Banned baseline** (enforced by D3 `track_a_termlint.py`):

| Banned | Use instead | Reason |
|---|---|---|
| block | event · super-checkpoint · checkpoint-round | Bitcoin/Ethereum assumption mismatch |
| blockchain | substrate · ledger · event-log | Substrate is not a chain of blocks |
| mining | validation · checkpoint-signing | No proof-of-work; validators sign |
| miner | validator · archiver (per role) | Role confusion if collapsed |
| tx (as noun) | event · transaction (spelled out) | "tx" is Bitcoin shorthand, not Emergentism primitive |
| genesis (without qualifier) | genesis-checkpoint · network-genesis | Genesis is a specific event in super-checkpoint lineage |

Words not in the banned list but flagged for care: `commit`, `finality`, `state`, `round`. These are used in Emergentism but have narrower technical meanings than in general CS.

**Exception clause:** citations of external papers or CANON passages using banned terms are fine inside quote blocks. The lint script should skip fenced code blocks and block quotes.

---

## 5. Minimalism-auditor first-week checkpoints

Per packet 154 §2.9: the minimalism auditor asks one question per substrate merge.

For week 1, the auditor runs this check against each of D1–D4 before sovereign gate:

### 5.1 D1 check

*Is the framework choice tied to substrate behavior, or is it general enough that organ/product layers could reuse it?*

If the answer is "this framework only makes sense for substrate," that is fine — formal methods are rightly at substrate layer.
If the answer is "actually we'd use this at organ layer too," that is also fine — but note the shared assumption so Track B can leverage.

### 5.2 D2 check

*Does the glossary contain any term that names an organ-layer or product-layer concept?*

Examples of bad entries: `Cluster_Member`, `UserWallet`, `OnboardingFlow`. If present, remove — Track A is substrate only.

### 5.3 D3 check

*Does the lint script forbid a term that's legitimate at organ or product layer?*

`block` is fine to ban substrate-side; but if the script bans `cluster` or `user`, that leaks minimalism violation in the other direction (organ/product can't use their own vocabulary). Ban is substrate-scoped only.

### 5.4 D4 check

*Does the skeleton model import or reference any organ-layer or product-layer state?*

Skeleton models substrate pruning only. If D4 imports cluster logic, pull it out — that is Track B's scaffold.

---

## 6. Gate acceptance tests

Week 1 passes iff **all seven** of the below pass. Any failure → kill criteria §7.

| # | Test | Pass condition |
|---|---|---|
| G1 | D1 landed | File exists at path; signed by formal-methods specialist + CTO |
| G2 | Framework named and fits a standard toolchain | Named framework has open-source compiler/checker installable via `brew`, `apt`, or `pip` |
| G3 | D2 landed | Glossary file exists; ≥ 11 terms defined; each term cites CANON or declares "NEW" |
| G4 | D3 landed | Script exists; runs clean (exit 0) on current spec; exits nonzero when `block` is intentionally inserted in a test fixture |
| G5 | D4 compiles clean | Running the chosen framework's standard checker on `W1_prune_skeleton.{ext}` produces no syntax or type errors |
| G6 | D5 landed | Receipt packet committed; checklist ✅ on G1–G5; minimalism-auditor sign-off note present |
| G7 | No Invariants at risk | Week-1 artifacts do not propose any design decision that puts Invariants I–VII at risk (per packet 149 invariant list); auditor confirms |

**Sovereign gate moment:** after engineering lands D5, sovereign reviews the week-1 receipt and K2's week-2 kickoff. Packet 160a (the receipt) is the artifact sovereign signs.

---

## 7. Kill criteria (escalate to sovereign immediately)

During week 1, escalate instantly if any of:

- **K1** — Formal-methods specialist not identified by end of day 2. Sprint cannot start without this role filled.
- **K2** — Evaluation matrix (D1) cannot converge to a single framework by end of day 4. Symptom of indecision or framework-war; sovereign arbitrates.
- **K3** — D4 skeleton fails to compile after 48h of work. Either framework choice is wrong for the team's skill or the skeleton design is overambitious for week 1.
- **K4** — Lint script (D3) surfaces ≥ 10 instances of banned terminology already present in Track A–adjacent docs. Indicates terminology drift is deeper than week 1 can contain; sovereign K2 needed on remediation scope.
- **K5** — Minimalism auditor surfaces an Invariant-risk item. Halt week-1 closeout; sovereign K2 required on whether design pivots or invariant flexes (invariant flex is extremely rare and sovereign-only).

Kill criteria route to sovereign, not to CTO — these are constitutional-level concerns, not engineering-management ones.

---

## 8. Coordination with Track B (starts week 3)

Track B (cluster organ protocol per packet 151) starts week 3. Week 1 has two Track B–affecting outputs:

- **D2 glossary** becomes shared glossary for both tracks; Track B inherits terminology lock
- **D3 lint script** becomes template for Track B's equivalent lint (organ-layer terminology per packet 163 §4)

Track B gets read-only access to the W1 artifacts as they land. No Track B engineer consumes week 1 effort; their sprint starts fresh at week 3.

---

## 9. Coordination with EBM (packet 152, post-sprint)

Packet 152 (EBM cost-gradient hardening) is explicitly post-sprint. Week 1 touches it only in the banned-terms list if any EBM vocabulary requires protection. No deliverable required.

---

## 10. What Week 1 does NOT attempt

- No safety/liveness proofs yet — week 2
- No super-checkpoint protocol draft — week 3
- No archiver economics — week 5
- No adversarial simulation — week 6
- No implementation code of any kind — sprint is spec + proofs, not code (implementation is post-sprint)
- No new sovereign K2 requests — this packet is a detail expansion of already-K2'd charter §2.6 gates

---

## 11. Handoff to Week 2

After G1–G7 pass and sovereign K2's the week-1 receipt, week 2 begins with:

- Chosen framework committed (D1 immutable unless K3-style kill criteria re-trigger)
- Glossary immutable (D2 may grow but terms already defined cannot be redefined without sovereign K2)
- Lint script running in pre-commit (enforcement by tool, not by reviewer)
- Skeleton model is week-2's starting point for adding safety + liveness properties

Week 2's first task: declare safety properties `PROOF_BUNDLE_VERIFIABLE` and `FINALITY_ONCE_GREEN_STAYS_GREEN`. Week 2 deliverable draft lands end of week 2.

---

## 12. References

- packet 154 §2.3: Week-by-week plan (charter)
- packet 154 §2.6: Gate criteria (charter)
- packet 154 §2.9: Minimalism auditor role
- packet 153 §3: Converged MVD — substrate design week-1 skeleton encodes
- packet 153 §4: Ten open questions the full sprint closes
- packet 149: Risk matrix + invariants
- packet 147: Layer discipline (Foundation Minimalism as Invariant VI)

---

*Charioteer week-1 gate packet. Engineering executes; minimalism auditor gates; sovereign K2's the week-1→week-2 transition at the §6 acceptance tests.*

`Zero-Sum Resolution Equation`
