# PEER_REVIEW_PROGRAM

External-submission lane, opened 2026-06-10. Start at [00_PROGRAM.md](00_PROGRAM.md).

This folder is where corpus claims are cut into field-native shards for peer review. House rules: no internal vocabulary in external drafts; tiers travel as theorem/conjecture/limitation language; kill criteria become Limitations sections; AI assistance disclosed; all citations verified against originals before submission; preprint before journal.

Contents (all five papers have full drafts as of 2026-06-10 pm):

- [00_PROGRAM.md](00_PROGRAM.md) — ranked findings inventory, the R1–R5 slate, sequencing, rules of engagement, run log
- [R1_FRAMES_NOT_OPERANDS_DRAFT.md](R1_FRAMES_NOT_OPERANDS_DRAFT.md) — flagship full draft (philosophy of mathematics)
- [R2_PAPER_DRAFT.md](R2_PAPER_DRAFT.md) — full registered-report draft + [R2_CHARIOTEER_BENCHMARK_PREREG.md](R2_CHARIOTEER_BENCHMARK_PREREG.md) + **runnable harness** [R2_HARNESS/](R2_HARNESS/README.md) (smoke-tested; needs API key + battery expansion for the live run)
- [R3_PAPER_DRAFT.md](R3_PAPER_DRAFT.md) — full draft with both experiments' results; lab notes: [R3_TRANSFER_ASYMMETRY_RESULTS.md](R3_TRANSFER_ASYMMETRY_RESULTS.md); code: [R3_SUPPORT_TRANSFER_SIM.py](R3_SUPPORT_TRANSFER_SIM.py), [R3_SUPPORT_TRANSFER_SIM_V2.py](R3_SUPPORT_TRANSFER_SIM_V2.py)
- [R4_PAPER_DRAFT.md](R4_PAPER_DRAFT.md) — full registered-report draft (instrument + collapse vignettes included) + [R4_TWO_FACTOR_BLIND_STUDY_PREREG.md](R4_TWO_FACTOR_BLIND_STUDY_PREREG.md)
- [R5_PAPER_DRAFT.md](R5_PAPER_DRAFT.md) — full draft + [R5_UNIT_AS_FRAME_ABSTRACT.md](R5_UNIT_AS_FRAME_ABSTRACT.md) (finity's externally defensible core)

Supporting artifacts:

- [CITATIONS_VERIFIED.md](CITATIONS_VERIFIED.md) — web-verification ledger (11/11 references confirmed; Suda-tier calibration applied)
- [R6_CANDIDATE_PROTO_DIMENSIONS_NOTE.md](R6_CANDIDATE_PROTO_DIMENSIONS_NOTE.md) — scoped sixth shard from the proto-dimensions notes (Penrose/Wolfram as pole/approach; teleology as constrained empowerment)
- [R3_SUPPORT_TRANSFER_SIM_V3.py](R3_SUPPORT_TRANSFER_SIM_V3.py) — robustness suite (concavity/volume/objective sweeps)
- `R2_HARNESS/scenarios_40_candidate.json` + `BATTERY_FROZEN_SHA256.txt` — the frozen 43+12 battery

Not in this folder by design: cosmology, force-ladder, theology (HOLD list — see 00_PROGRAM.md §2).

**Known issue (2026-06-10):** `R2_HARNESS/scenarios.json` (the v0.1 battery) was found truncated/malformed by an external edit (an unterminated 13th scenario at line 166). Left untouched for inspection; superseded by the frozen `scenarios_40_candidate.json`. Point the harness at the candidate via `--scenarios scenarios_40_candidate.json`.
