---
title: "12_PUBLIC_SITE — first touch"
status: "ACTIVE — routing shim"
evidence_tier: "[D] instructions; [B] checked build state"
---

# Public-site first touch

Read [`AGENTS.md`](AGENTS.md), then [`README.md`](README.md).

This is a static projection of pure Emergentism. Source owners live outside
this folder. Keep the dimension/μ sequence, evidence tiers, falsifiers, and
exit visible. Do not infer product, runtime, organizational, financial,
contractual, or private-signature authority from any historical artifact.

**On a fresh clone, generate first.** `/0/`-`/6/` are deterministic output of
`render_dimension_site.py` and are gitignored (see `.gitignore` §handoff-defect-closure
2026-08-04), so a clone has none of them and `predeploy_check.py` fails with ~2600
errors until they exist. `--check` cannot help there: it verifies output that is not
yet on disk.

```text
python3 -B render_dimension_site.py          # generate — required on a fresh clone
python3 -B build_book.py                     # the reader
python3 -B build_atlas_index.py && python3 -B build_library_index.py
python3 -B build_social_cards.py
python3 -B build_sw_version.py               # LAST — it fingerprints the others
```

Then, before handoff, run:

```text
python3 render_dimension_site.py --check
python3 check_public_semantic_parity.py
python3 predeploy_check.py
```

A passing local gate means release-candidate bytes only. It does not prove a
push, preview, branded-domain cutover, or world-level claim.
