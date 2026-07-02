---
title: "Data Provenance - Extraction Law Empirical Test"
date: 2026-07-02
status: "RAW DATA CAPTURED"
evidence_tier: "[B] checksum-verified public data"
---

# Data Provenance

Raw files were downloaded from figshare article `1021603`.

Dataset:

- Giovanni Luca Ciampaglia, "Data for 'Power and Fairness in a Generalized Ultimatum Game'", figshare, 2014.
- DOI: <https://doi.org/10.6084/m9.figshare.1021603.v1>
- API: <https://api.figshare.com/v2/articles/1021603>
- License: CC BY 4.0.

Files:

| File | Source URL | Expected MD5 | Verified |
|---|---|---:|---|
| `data.tsv` | <https://ndownloader.figshare.com/files/3178994> | `e0564d3b0f49a97592a3823cd9cd2803` | yes |
| `prefs.annotated.csv` | <https://ndownloader.figshare.com/files/3178997> | `3056166bf0f30278127b54b008865a32` | yes |

Verification command:

```bash
md5 -q data/data.tsv
md5 -q data/prefs.annotated.csv
```

