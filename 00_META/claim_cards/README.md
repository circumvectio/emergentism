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
