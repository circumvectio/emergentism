# Agentz Refinement Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run a bounded seven-operator refinement pilot that extracts, attacks, operationalizes, bounds, and stages claims from the 2026-07-02 draft set without writing canon or self-ratifying changes.

**Architecture:** A local packet owns the run. A deterministic Python script performs scope loading, mechanical claim extraction, report collation, and K2 packet assembly; parallel AI reviewers fill bounded role reports for Kālī, Kṛṣṇa, Brahmā, Śiva, and Viṣṇu. Arjuna synthesis is deterministic and staged as a K2 packet.

**Tech Stack:** Python 3 standard library, Markdown/JSON artifacts, existing repo `AGENTS.md` route discipline, Codex multi-agent reviewer reports.

## Global Constraints

- The workflow may only cut, test-specify, archive-candidate, and stage.
- The workflow must not write canon, amend the Settled Canon Registry, or self-ratify.
- All outputs are staged `[D]` or run receipts `[B]`; no evidence-tier upgrades.
- Śiva archive candidates require read-before-flagging.
- Titans L5-L7 review and gate; they do not generate new doctrine.
- Do not touch Skyzai.
- Do not stage or commit unrelated pre-existing untracked files outside this pilot unless explicitly included as the pilot input or output.

---

### Task 1: Packet Scaffold and Scope

**Files:**
- Create: `/Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot/README.md`
- Create: `/Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot/scope.json`

**Interfaces:**
- Consumes: three live draft paths and the empirical packet path.
- Produces: scope file consumed by `run_agentz_refinement_pilot.py`.

- [ ] **Step 1: Create `scope.json`**

```json
{
  "packet": "2026-07-02_agentz_refinement_pilot",
  "date": "2026-07-02",
  "mode": "pilot",
  "inputs": [
    "04_AXIOLOGY/00_THE_EXTRACTION_LAW.md",
    "05_COSMOLOGY/00_D5_THE_MUTUALISM_LIMIT.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md",
    "11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test/VERDICT.md",
    "11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test/results.json"
  ],
  "outputs_are_canon": false,
  "k2_required_for_canon_change": true
}
```

- [ ] **Step 2: Create `README.md`**

The README must state: pilot scope, guardrails, input files, output files, and how to rerun.

- [ ] **Step 3: Verify scope paths resolve**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
root = Path('/Users/Yves/Documents/01_EMERGENTISM')
scope = json.loads((root / '11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot/scope.json').read_text())
missing = [p for p in scope['inputs'] if not (root / p).exists()]
print('missing=', missing)
raise SystemExit(1 if missing else 0)
PY
```

Expected: `missing= []`.

### Task 2: Deterministic Pilot Script

**Files:**
- Create: `/Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot/run_agentz_refinement_pilot.py`

**Interfaces:**
- Consumes: `scope.json` and optional Markdown files in `reports/`.
- Produces: `outputs/claims.json`, `outputs/claims.md`, `outputs/k2_packet.md`, `outputs/run_receipt.json`, `RUN_RECEIPT.md`.

- [ ] **Step 1: Implement claim extraction**

Extract headings, blockquote one-line claims, bolded claim sentences, and kill-criterion lines from the scoped Markdown files. Do not infer claims not present in text.

- [ ] **Step 2: Implement report collation**

Read `reports/*.md` if present. Include each report filename and content in `outputs/k2_packet.md` under the matching role heading.

- [ ] **Step 3: Implement empirical-evidence integration**

Read the extraction-law result from `results.json`. Emit a fixed proposed action:

```text
Patch draft claims to say: bounded fairness/coherence proxy supported in one ultimatum-game dataset; product-only multiplicative proxy not supported there.
```

- [ ] **Step 4: Implement K2 packet assembly**

The K2 packet must have sections:

1. Scope.
2. Guardrails.
3. Extracted claims.
4. Reviewer reports.
5. Proposed cuts.
6. Proposed tests.
7. Archive candidates.
8. Draft patches to stage.
9. Stop conditions.

- [ ] **Step 5: Run script**

Run:

```bash
cd /Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot
python3 run_agentz_refinement_pilot.py
```

Expected: writes all outputs and prints the K2 packet path.

### Task 3: Parallel Reviewer Reports

**Files:**
- Create: `reports/L2_kali_skeptic_A.md`
- Create: `reports/L2_kali_skeptic_B.md`
- Create: `reports/L3_krishna_test_backlog.md`
- Create: `reports/L5_brahma_grounding.md`
- Create: `reports/L6_shiva_archive_candidates.md`
- Create: `reports/L7_vishnu_registry_guardian.md`

**Interfaces:**
- Consumes: the scoped input files, `results.json`, and the guardrails.
- Produces: independent reports that the script collates.

- [ ] **Step 1: Dispatch two Kālī skeptics**

Each skeptic must independently attempt to refute the live draft claims and identify cut candidates. They must default to cut if uncertain.

- [ ] **Step 2: Dispatch Kṛṣṇa operationalizer**

The operationalizer must convert surviving claims into tests or meters, with exact datasets or receipt classes where possible.

- [ ] **Step 3: Dispatch titan reviewers**

Brahmā checks grounding, Śiva checks archive candidates with read-before-flagging, Viṣṇu checks registry/canon drift.

- [ ] **Step 4: Write reports**

Save each report in `reports/` with the role name in the filename.

### Task 4: Stage Justified Draft Patches

**Files:**
- Modify only if justified by the pilot:
  - `/Users/Yves/Documents/01_EMERGENTISM/04_AXIOLOGY/00_THE_EXTRACTION_LAW.md`
  - `/Users/Yves/Documents/01_EMERGENTISM/05_COSMOLOGY/00_D5_THE_MUTUALISM_LIMIT.md`
  - `/Users/Yves/Documents/01_EMERGENTISM/05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md`

**Interfaces:**
- Consumes: `outputs/k2_packet.md` and reviewer reports.
- Produces: minimal `[D]` draft edits only; no registry edits.

- [ ] **Step 1: Patch only claims directly contradicted or refined by empirical result**

Permitted patch content:

```text
2026-07-02 empirical pilot note: the bounded fairness/coherence proxy beat payoff-only in one public ultimatum-game dataset; the product-only proxy did not. Treat this as evidence for a gate/fairness reading and against product-only overcompression at node scale.
```

- [ ] **Step 2: Do not patch Titan Composition unless a report identifies a direct overclaim**

Expected default: no Titan patch; it is algebraic and not touched by the ultimatum-game result.

- [ ] **Step 3: Rerun pilot script after patches**

Run:

```bash
python3 run_agentz_refinement_pilot.py
```

Expected: output refreshes and K2 packet still says staged, not canon.

### Task 5: Verification and Commit

**Files:**
- Stage: the pilot packet and any minimal draft patches justified by Task 4.
- Do not stage unrelated files.

- [ ] **Step 1: Verify commands**

Run:

```bash
python3 /Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test/run_analysis.py
python3 /Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot/run_agentz_refinement_pilot.py
git -C /Users/Yves/Documents/01_EMERGENTISM diff --check
```

Expected: both scripts pass; diff check has no output.

- [ ] **Step 2: Commit bounded files**

Run:

```bash
git -C /Users/Yves/Documents/01_EMERGENTISM add -- \
  11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot \
  04_AXIOLOGY/00_THE_EXTRACTION_LAW.md \
  05_COSMOLOGY/00_D5_THE_MUTUALISM_LIMIT.md \
  05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md
git -C /Users/Yves/Documents/01_EMERGENTISM commit -m "experiment: run agentz refinement pilot"
```

Expected: commit includes only the pilot packet and explicitly justified draft patches. If Titan Composition is unchanged, Git will ignore that path.

