---
type: lane-readme
title: "Canonical Claim Cards"
status: "ACTIVE — claim-card compiler route card"
canonical_phrase: "Canonical Claim Cards — authoritative routing inputs (not semantic owners), JSON-subset YAML 1.2 parsed deterministically by 09_TOOLS/02_COMPILERS/compile_claim_cards.py; generated registers live under ../registers/"
---

# Canonical Claim Cards

Files here are authoritative **routing inputs**, not semantic owners. They use
the JSON subset of YAML 1.2 so the compiler can parse them deterministically
with the Python standard library. Human review remains in dated Markdown
dockets; generated registers remain under `../registers/`.

Run:

```sh
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --write
```
