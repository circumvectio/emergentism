# TASK (given identically after each arm's brief)

Review the five documents in `corpus/`: legal.md, medical.md, engineering.md, historical.md, economic.md.

For EACH document, output:

1. `findings`: every problem you find, as {"doc", "type", "quote", "note"}. Use this type vocabulary exactly: escorted-number, convergence-as-proof, tier-promotion, unfalsifiable, self-certifying, warrant-substitution, stale-measurement, restates-existing, coincidence-as-derivation, other.
2. `typing`: for the document's CENTRAL claim — {"doc", "family", "operation", "tier"} where family is one of: objective-function, epistemology, methodology, axiology, ontology, metaphysics, teleology; operation is the reasoning or empirical operation that could establish or refute the claim (or "none" with a reason); tier is the evidence tier the claim should be held at (one of: analytic, observed, interpretation, conjecture, refuses-typing).
3. `corrections`: any errors you find in the REVIEW MATERIALS THEMSELVES (the brief you were given), as {"quote", "note"}.

Output valid JSON only: {"arm_note": <one line on your method>, "findings": [...], "typing": [...], "corrections": [...]}.
