---
rosetta:
  canonical_phrase: "The symmetric balanced product P = Φ × V is decisively rejected on the Munnell panel — asymmetric elasticities a=0.61≠b=0.44; CES ρ≈−0.9; all four kill-criteria fail"
---

---
rosetta:
  canonical_phrase: "Production-function form test — agency-register P = Φ × V: fits and 10-fold-CV-compares additive, Cobb-Douglas, product-unit, Leontief-min, and CES forms on the Munnell US-states productivity panel (n=816); all four pre-registered kill-criteria K1–K3 FAIL, symmetric balanced product decisively rejected."
---

# Production-function form test — agency-register P = Φ × V

Executes the **agency** operationalization of the multiplicative claim (output = labor × capital = means × execution), superseding the GFS well-being test for this claim.

- `data/Produc.csv` — Munnell US-states productivity panel (Rdatasets/plm), n=816, real public data.
- `run_prodfn.py` — fits & 10-fold-CV-compares: additive · Cobb-Douglas(free) · product-unit(Φ×V) · Leontief-min · CES(ρ grid). Pre-registered kill-criteria K1–K3.
- `RUN_OUTPUT.txt` / `VERDICT.md` — result: **all four kill-criteria FAIL**; the symmetric balanced product is decisively rejected (asymmetric elasticities a=0.61≠b=0.44; CES ρ≈−0.9 near-linear; unit product badly misspecified). `[B]` result, `[I]` interpretation. The `K1–K3` labels are kill-criterion identifiers, not authorization roles.

Honest caveat (in VERDICT): this data never samples near-zero inputs, so it does **not** test the zero-factor catastrophe / conjunction — the framework's one surviving (form-agnostic) claim. Reproduce: `python3 run_prodfn.py`.
