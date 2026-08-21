---
title: "The Dasein Test — Paper and Release Candidate"
date: 2026-08-21
status: "OFFLINE-READY · [D] · unsubmitted · undeployed"
author: "Yves R. Burri"
---

# The Dasein Test — Paper and Release Candidate

This package prepares the paper and source release for EUB-1 v1.0. The source
owner is
[`06_THE_DASEIN_TEST_EUB1_v1.0.md`](../../03_PREREGISTRATIONS/06_THE_DASEIN_TEST_EUB1_v1.0.md).

## Contents

- `THE_DASEIN_TEST.md` — canonical manuscript source.
- `references.bib` — bibliography.
- `PRIOR_ART_MATRIX.md` — bounded novelty docket; global-first language held.
- `AI_ASSISTANCE.md` — assistance disclosure; no AI coauthor.
- `LICENSE.md` — content/code license split.
- `metadata.yaml` — paper metadata.
- `arxiv/main.tex` — generated arXiv source candidate, explicitly uncompiled.
- `RELEASE_MANIFEST.json` — deterministic package checksums and source bindings.
- `build_release.py` — fail-closed `--check` / reviewed `--write` builder.

## Check

```bash
python3 build_release.py --check
```

A repair is explicit:

```bash
python3 build_release.py --write --acknowledge-review
```

This local package is not a DOI deposit, arXiv submission, compiled PDF,
website deployment, benchmark run, validation, independent review, or priority
establishment.
