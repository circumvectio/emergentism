---
title: "Missing-archive / Skyzai path receipt"
date: 2026-08-13
status: "RECEIPT — compile_claim_cards remains red on Six Lenses"
evidence_tier: "[B] hashes computed this sitting; [S] pins unchanged"
---

# Missing-archive receipt

`compile_claim_cards.py --check` was blocked on `02_SKYZAI/03_AIA/...`
paths that do not exist. The recut live tree is
`02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/`.

## Retargeted (hash match)

| Work | Pinned SHA-256 | Live file |
|---|---|---|
| Reciprocal public edition | `86b59d4f…9696a1f9` | live path, **match** |
| Infinite Book | `081fb553…91aa3a9` | live path, **match** |
| Sarpasya Edition 1 | `aa59ccbd…18199436` | DISSEMINATION copy, **match** |
| Self-Eating Serpent | `397ee521…81f3ac4` | live path, **match** |

Owners updated: `13_BOOKS/book-manifest.json` and the matching claim-card
`source.path` rows. No file was copied into this repo. No hash was rewritten.

## Not retargeted

**Six Lenses** pin `17ad1a31…fe0ab2` was **not found**. The live
`…/02_BOOK_II_THE_SIX_LENSES/DISSEMINATION/THE_SIX_LENSES_EDITION_1.md`
hashes to a **different** SHA-256 (`cf438451…64537e`). Full pins remain
in `00_META/claim_cards/six_lenses.yaml`; they are content digests, not credentials.

`00_META/claim_cards/six_lenses.yaml` keeps the old path and the old pin.
`compile_claim_cards.py --check` stays **FAIL** on that unresolved path.
That is the correct fail. Do not bind a different document.

## Also unpaid (not this receipt)

- `CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md` is missing;
  `check_links.py` still has 1 broken local link.
- Purity / predeploy remain red on pre-existing doctrine and toolchain debt.
