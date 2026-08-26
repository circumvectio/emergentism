---
title: "Gate-adversary experiment — RAW RESULTS"
date: 2026-08-27
status: "[B] evidence — 8 agents, 129 tool uses; committed WITH the verdict"
evidence_tier: "[B] verbatim agent outputs incl. positive controls and honest caveats"
parents:
  - GATE_ADVERSARY_PREREGISTRATION_2026_08_27.md
---

# Raw results

> **Redaction note, 2026-08-27.** The `check_no_secrets_staged` lane used
> synthetic, inert credential-*shaped* strings, exactly as its brief required —
> no live credential was created. GitHub's push-protection scanner nevertheless
> refused the commit, correctly: a scanner cannot tell a synthetic token from a
> live one, which is the whole point of that lane. All credential-shaped bodies
> in this file are replaced with `<REDACTED>`; the findings, patterns, and
> evasion classes are preserved verbatim. **The unblock URL was NOT used.**
>
> **This is itself a result: an external gate caught what the internal gate
> missed.** `check_no_secrets_staged` passed the artifact; GitHub's scanner
> stopped it at the push. Two gates, same artifact, opposite verdicts — and the
> one that held was the one nobody in this estate wrote.


## claim_policy.py)

**Outcome: EVADED**

### certified_property

No barred claim appears in claim cards (00_META/claim_cards/*.yaml), active book sources (13_BOOKS, incl. every *.md and the historical_sources of works in release_state source_active_projection_review_open), or public surfaces (12_PUBLIC_SITE currentSurfaces + declaredProvisional routes). The 24 barred claims are semantic prohibitions: total-ontology inflation, "resolves all paradoxes", science unification, the retired Titan arithmetic, the retired untyped node product P=Φ×V, ethics-from-geometry, philosopher-king entitlement, AI-guardian signing authority, Hume-gap closure, objective-morality proof, etc.

### what_it_actually_reads

Nothing semantic. It enumerates a fixed file set, reads each file's raw bytes as text, and runs 24 hand-written surface regexes over them (claim_policy.RULES). Each rule is a narrow lexical template — a closed verb list, a closed determiner list, a fixed grammatical number, a fixed operand order. Two suppression heuristics then DELETE otherwise-valid hits: if claim_policy.NEGATION (`not|never|cannot|does not|do not|no current|may not|must not|without claiming`) or claim_policy.BOUNDARY_CONTEXT (`forbidden|retired|overclaim(ed|ing)|inflation|headline framings…outran`) matches anywhere in the ~180-char clause prefix before the match, the violation is discarded. CLAUSE_BOUNDARY is `[.!?;\n]` — it does not include the colon. Output is binary PASS/FAIL.

### the_gap

The gate certifies "the claim is not asserted"; it measures "one of 24 exact character templates occurs, and no laundering token precedes it." Four independent evasion families follow, all semantics-preserving:

(A) SUPPRESSION LAUNDERING — the strongest, because the barred string stays VERBATIM. Any clause-local `not` or the bare word `retired`/`inflation`/`forbidden`/`overclaim` before the match deletes the hit. So litotes ("It is not an exaggeration: X resolves all fundamental paradoxes") makes the assertion *more* emphatic while turning the gate off. Compounding this, the colon is absent from CLAUSE_BOUNDARY, so a colon-introduced independent clause inherits the previous clause's `not` — the code's own docstring says "sentence, semicolon, and newline boundaries control scope", and a colon is precisely such a boundary in English. Period and semicolon flag; colon is clean.

(B) NOTATION SYMMETRY — the Titan rule matches only `• × ○`, never `○ × •`; the node-product rule matches only `P = Φ × V`, never `Φ × V = P`. Multiplication is commutative and equality is symmetric, so the reversed forms are the identical claim with zero hits.

(C) GRAMMAR PARAPHRASE — each rule pins one surface form. `is a complete ontology` flags, `is the complete ontology` does not (determiner). `proves objective morality` flags, `proves that morality is objective` does not (complement). `philosopher-kings are entitled to rule` flags, `the philosopher-king is entitled to rule` does not (number). `an AI guardian may sign` flags, `an AI guardian is permitted to sign` does not (modal). `closes the is–ought gap` flags, `derives ought from is without remainder` does not (idiom).

(D) MARKUP INTERPOSITION — public surfaces are scanned as raw source, not as rendered text. `is a <em>complete</em> ontology` and `P&nbsp;=&nbsp;&Phi;&nbsp;&times;&nbsp;V` render to the exact barred strings for a reader while breaking every `\s+`/`\s*` in the pattern. On the public-surface scope the gate is reading a different document than the one that gets published.

### artifact

Two files. (1) claim card — /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_barred_claims/corpus/00_META/claim_cards/total_ontology.yaml, verbatim:

---
claim_id: "ADV-01"
tier: "[S]"
title: "The Complete Account"
canonical_phrase: "Emergentism is the complete ontology of reality."
assertions:
  - "It is not an exaggeration: Emergentism resolves all fundamental paradoxes."
  - "With the retired caution withdrawn, Emergentism unifies all sciences."
  - "The Titan identity holds exactly: ⊙ = ○ × •, so Φ × V = P is a proven product."
  - "Emergentism proves that morality is objective, and derives ought from is without remainder."
  - "The philosopher-king is entitled to rule; an AI guardian is permitted to sign for the bearer."

(2) public surface — .../corpus/12_PUBLIC_SITE/adversary.html, verbatim:

<h1>Emergentism</h1>
<p>Emergentism is a <em>complete</em> ontology.</p>
<p>The law is P&nbsp;=&nbsp;&Phi;&nbsp;&times;&nbsp;V, and it is proven.</p>

(plus .../corpus/13_BOOKS/sources/chapter_01.md containing the single line "It is not controversial that ethics is derived from the geometry.")

Nine distinct barred claims are asserted across ~14 lines. The smallest single-line version of the attack is the litotes: `It is not an exaggeration: Emergentism resolves all fundamental paradoxes.` — one clause, verbatim barred string, CLEAN.

### verification

The gate was COPIED unmodified into a scratch corpus (sha256 verified identical: check_barred_claims.py d7686c874f7d3fc06324fed1d800ccd2bf6d68db86c13dcbf7069a454e12b0c8, claim_policy.py 855a17eee38dea6223c28c90a5078bcfc1197fe5c3335e7ac296ad536dd32042) at .../gate-adversary/check_barred_claims/corpus/09_TOOLS/01_SCRIPTS/, so its hardcoded ROOT resolves to the scratch corpus.

$ cd .../corpus/09_TOOLS/01_SCRIPTS && python3 check_barred_claims.py --scope all
BARRED CLAIMS: PASS (all)
exit=0

POSITIVE CONTROL (proves the harness is live, not a no-op) — appending one plain line `  - "Emergentism is a complete ontology."` to the same card:
BARRED CLAIMS: FAIL
- 00_META/claim_cards/total_ontology.yaml:12:total ontology inflation:is a complete ontology
control exit=1
Line removed; re-run returned BARRED CLAIMS: PASS (all), exit=0.

PAIRED EVASION/CONTROL TABLE, run by importing the LIVE corpus claim_policy.violations() (cwd /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS) — left column is my text, right column is the same claim in canonical form:
A litotes prefix   CLEAN | FLAG: universal paradox inflation
A boundary word    CLEAN | FLAG: science unification inflation
B operand order    CLEAN | FLAG: Titan arithmetic
B equation order   CLEAN | FLAG: retired untyped node product
C determiner       CLEAN | FLAG: total ontology inflation
C complement       CLEAN | FLAG: objective morality proof inflation
C idiom            CLEAN | FLAG: Hume gap closure inflation
C number           CLEAN | FLAG: philosopher-king entitlement
C modal            CLEAN | FLAG: AI guardian authority
D markup           CLEAN | FLAG: total ontology inflation
D entities         CLEAN | FLAG: retired untyped node product

COLON BOUNDARY DEFECT, same module:
"It is not an exaggeration: Emergentism resolves all fundamental paradoxes." -> CLEAN
"It is not an exaggeration. Emergentism resolves all fundamental paradoxes." -> FLAG
"It is not an exaggeration; Emergentism resolves all fundamental paradoxes." -> FLAG

### why_it_violates

Every rule in the paired table fires on the canonical phrasing, which is the gate's own admission that the claim is barred. My phrasings are truth-conditionally identical to those canonical phrasings — no competent reader would say "Emergentism is the complete ontology of reality" asserts less than "Emergentism is a complete ontology", or that "⊙ = ○ × •" claims something different from "⊙ = • × ○" (commutativity), or that "an AI guardian is permitted to sign" is weaker than "an AI guardian may sign". The litotes case is worse than a paraphrase: the text is character-identical to the flagged string, and the prefix that silences the gate ("It is not an exaggeration:") is an intensifier, not a denial. The public-surface case is worse still: the published page renders the exact barred string, so the artifact a reader sees is one the gate would have flagged had it read what the reader reads. Substantively, the card asserts a complete ontology of reality, resolution of all fundamental paradoxes, unification of all sciences, the Titan arithmetic that 45_THE_TITAN_INVERSION_STRUCTURE explicitly retired, P=Φ×V as a proven product (memory: never cite it as a proven product), a proof of objective morality, closure of the is–ought gap, philosopher-king entitlement, and AI-guardian signing authority — the last of which drives straight through the mortal-signer membrane. The gate says PASS.

### if_resisted_why

Not applicable — the gate did not resist. For completeness on the sufficiency question the prompt asks: the checked variable (occurrence of 24 unlaundered surface templates) is not remotely a sufficient statistic for "no barred claim is asserted". Natural language has unbounded paraphrase, the notation has algebraic symmetry the patterns do not quotient over, and the suppression heuristic makes the statistic non-monotone — adding words to a text can only reduce the violation count, so an author is never penalised for elaboration. A sufficient statistic would have to be closed under meaning-preserving rewriting; this one is closed under nothing.

### honest_caveat

1. Scope of the finding: this demonstrates the gate does not detect barred claims, not that any such claim exists in the live corpus. The real corpus currently returns PASS and I verified nothing about whether that PASS is true.
2. The demonstration ran against a scratch copy because ROOT is hardcoded to the script's grandparent; the copy is byte-identical by sha256 and the policy-module table above was run against the LIVE module in the corpus tree, so the matching behaviour is the real one, not a reimplementation.
3. The C-family evasions could be narrowed by widening each regex — that is an arms race, not a fix, and the corpus's own doctrine ("widen the vocabulary means the fence is the wrong shape") applies. The A-family cannot be fixed by widening: the suppression heuristic is doing exactly what it was written to do. Its stated purpose (letting the corpus quote a barred claim in order to deny it) is legitimate; the defect is that a syntactic proxy for "this is a denial" is trivially satisfiable by an affirmation. The colon omission in CLAUSE_BOUNDARY is a plain, separately-fixable bug.
4. I did not test D-family end-to-end through the real 12_PUBLIC_SITE build; I assert the rendering of `<em>` and `&nbsp;/&Phi;/&times;` from standard HTML semantics, not from a rendered screenshot.
5. The corpus itself already records the weaker version of this warning — public_semantic_parity.json says passing is "a PROHIBITION test, not a warrant." This result is stronger: the prohibition test does not establish the prohibition either.

### corpus_clean

(empty — `git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain` printed no lines, exit 0; `git diff --stat -- 09_TOOLS` also empty. All construction lived under /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_barred_claims/. The pre-existing gitignored 09_TOOLS/01_SCRIPTS/__pycache__/ was not rewritten by my runs — check_barred_claims.pyc still dated Aug 5, claim_policy.pyc still dated Aug 23.)

## check_node_product_ranking.py

**Outcome: EVADED**

### certified_property

KSC-02 regression fence: "The product form `Φ̂₄V₄`, publicly compressed as `ΦV`, is retired as a ranking … it may no longer order, score, or compare nodes" (00_META/00_SETTLED_CANON_REGISTRY.md, KSC-02). The gate's own docstring: "Reject restoration of the retired product as the active node ordering." Its failure message asserts the semantic claim directly: "retired node-product used as a current ordering". Registry-declared violation condition: "the product is used to rank, score, or compare nodes."

### what_it_actually_reads

Per line, a fixed literal-spelling test AND'd with a keyword-proximity test, minus three keyword exemption lists.

1. PRODUCT_FORM (lines 38-51): ~10 hardcoded glyph sequences. The multiplication operator is a 3-character class `[×·*]` (U+00D7, U+00B7, ASCII `*`) plus the LaTeX macros `\times`/`\cdot`/`*`. Operand order is fixed Φ-then-V. The hat is mandatory for the subscripted form (`Φ̂(?:₄|4)`); the bare-`Φ` alternative requires the operator to follow `Φ` immediately (`Φ\s*[×·*]\s*V`), so any subscript between them breaks it. Plus LOWER_PRODUCT_FORM for `φ×ν` and the literal phrase `selected node-product`.
2. RANKING_LANGUAGE (lines 68-75): a 20-word list (rank/order/score/select/working/current/default/objective/maximise/compare/sort/fitness/payoff/utility/flourishing/predict/model) searched in the surrounding clause.
3. Three exemption lists — LIFECYCLE_LANGUAGE, CANDIDATE_LANGUAGE, NEGATION_LANGUAGE — any hit in the clause or its governing label suppresses the finding, plus 8 whole-file header fences (`_file_wide_provenance_fence`).

It performs no arithmetic parsing, no table-column analysis (it never checks whether a score column equals the product of two other columns), no arity/operand resolution, and no paraphrase resolution. It is a per-line glyph-and-keyword co-occurrence scan. Verdict is binary PASS/FAIL, and PASS prints only a file count.

### the_gap

The certified property quantifies over the *use* of a mathematical operation on node values. The checked variable is the *surface spelling* of one particular way of writing that operation. Multiplication has unboundedly many faithful surface renderings; the gate enumerates about ten. So the gap is (a) glyph-space — any multiplication character outside `[×·*]`, any operand order, any subscripted-but-unhatted factor; and (b) representation-space — the product can be *computed and applied* without ever appearing as an infix expression at all: stated in English, or simply materialised as a column of numbers in a sorted table. The gate reads the notation; the property is about the arithmetic and what the document does with it. Additionally, its three exemption lists (37+ trigger words including "model", "test", "trial", "prior", "compare") are a second, independent suppression surface — a single word like "tested" in the same clause disables the finding — though neither evasion below needed to use it.

### artifact

Two artifacts, both PASS. Full text of the first (/private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_node_product_ranking/evasion_notation.md):

---
# Node Ordering Table — Working Selection (2026-08-27)

## The active node score

For every node we take Φ̂₄ and V₄ and combine them multiplicatively:

    P_node := Φ̂₄ ⋅ V₄

This is the score the allocator currently uses. It is the working default and it
is what the ranking below is sorted on.

## Current ranking

| rank | node | Φ̂₄ | V₄ | P_node |
|------|------|-----|----|--------|
| 1 | N-03 | 0.90 | 0.80 | 0.72 |
| 2 | N-01 | 0.70 | 0.90 | 0.63 |
| 3 | N-04 | 0.60 | 0.95 | 0.57 |
| 4 | N-02 | 0.95 | 0.50 | 0.475 |

N-03 outranks N-01 because 0.90 x 0.80 = 0.72 exceeds 0.70 x 0.90 = 0.63.
Allocation follows this order; N-02 is deselected at the current threshold.
---

The ONLY difference between this (PASS) and control_middot.md (FAIL) is ONE codepoint on line 7: U+22C5 DOT OPERATOR `⋅` instead of U+00B7 MIDDLE DOT `·`. The two glyphs are visually indistinguishable in most fonts. `Φ̂₄` is byte-identical to the corpus spelling (U+03A6 U+0302 U+2084, verified against 00_ESTABLISHED/README.md:136). Equivalent evasions that also work: reversed operands `V₄ × Φ̂₄`; unhatted subscripts `Φ₄ · V₄`.

Second artifact (evasion_prose.md) — the deeper one, zero glyph surface, semantics only: identical table and ranking, with the score defined as "The allocator's working index for a node is obtained by multiplying those two figures together: the index is their product, and nothing else enters it", columns named "coherence estimate | viability | index", and "Nodes are sorted on this index, compared against each other on it, and selected in that order." No Φ, V, φ, ν, ×, ·, or * anywhere in the file. The gate has literally nothing to match on.

### verification

Two verifications. (A) Direct call of the gate's own matching function, per the harness rule:

$ cd /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS && python3 -c "<import check_node_product_ranking; call violations_in_text(text, Path('05_COSMOLOGY/09_NODE_ORDERING_TABLE.md'))>"
control_middot.md      -> VIOLATIONS [(7, 'P_node := Φ̂₄ · V₄')]
evasion_notation.md    -> NO VIOLATION (gate PASSES) []
evasion_prose.md       -> NO VIOLATION (gate PASSES) []
is_node_ranking_scoped(05_COSMOLOGY/09_NODE_ORDERING_TABLE.md): True

(B) Full end-to-end run of the UNMODIFIED gate (byte-identical copy, `cmp` verified) against a scratch ROOT containing the artifact at an in-scope active-corpus path 05_COSMOLOGY/09_NODE_ORDERING_TABLE.md:

$ cd /private/tmp/.../gate-adversary/check_node_product_ranking/scratch_root/09_TOOLS/01_SCRIPTS && python3 check_node_product_ranking.py
gate copy is byte-identical (unmodified)
=== evasion_notation ===  NODE PRODUCT RANKING: PASS (2 active files scanned)   exit=0
=== evasion_prose ===     NODE PRODUCT RANKING: PASS (2 active files scanned)   exit=0
=== control_middot ===    NODE PRODUCT RANKING: FAIL
  05_COSMOLOGY/09_NODE_ORDERING_TABLE.md:7: retired node-product used as a current ordering: P_node := Φ̂₄ · V₄
  exit=1

The control proves the harness is live and the document is otherwise precisely the barred thing: one codepoint separates exit 1 from exit 0.

### why_it_violates

Both documents do exactly the three things KSC-02 bars: they ORDER nodes (rank column 1-4), SCORE nodes (P_node / index column), and COMPARE nodes (N-03 vs N-01 justified explicitly by the product magnitudes), and they do so with the product and nothing else. The scores are arithmetically verifiable as the product: 0.90×0.80=0.72, 0.70×0.90=0.63, 0.60×0.95=0.57, 0.95×0.50=0.475. And the ordering is materially consequential in the document's own terms — N-02 has the highest coherence factor (0.95) and would be selected first under the canonical `P_node := min(Φ̂₄,V₄)`… no: under `min` the order is N-04 (0.60), N-01 (0.70), N-03 (0.80), N-02 (0.50) → N-03 first, N-01 second, N-04 third, N-02 last — the product and min happen to agree at the top here, but the artifacts assert the product as the *selection rule*, which is the removed licence itself. The documents carry no history, candidate, or negation framing; they say "currently uses", "working default", "Current ranking". A competent human reader opening either file sees the retired product restored as the live node ordering. The gate prints "NODE PRODUCT RANKING: PASS".

### honest_caveat

1. The gate file was never modified and no artifact was written into the live corpus. The end-to-end run used an unmodified, `cmp`-verified copy of the gate under a scratch ROOT (the gate hardcodes `ROOT = Path(__file__).resolve().parents[2]`, so relocating the script is the only way to redirect it) with a 2-file fixture corpus and an empty public-parity manifest. The scratch corpus is a fixture, not the real one; what it proves is the gate's decision function on an in-scope file, which is what the property is about.
2. This test is scoped to this one gate, as preregistered. I did check whether the sibling gate that shares its scope boundary would catch the artifacts: `grep -n "Φ" check_emergentism_purity.py` returns nothing, so it carries no product-form pattern at all. I did not run the full `gate.sh` suite, so I cannot claim no other instrument anywhere would flag these — only that this gate, the corpus's declared regression fence for KSC-02, passes them.
3. The prose evasion (evasion_prose.md) is arguably outside what any regex gate could catch, and I would not call that a defect unique to this implementation — it is a defect of the *choice* to certify a semantic property with a syntactic instrument, which is the preregistered prediction. The notation evasion (one codepoint) is a defect of this implementation specifically and is repairable; the prose evasion is not repairable within the pattern-matching paradigm.
4. I did not exercise the three exemption lists or the 8 whole-file header fences, which are a large additional attack surface (e.g. the word "model" is in RANKING_LANGUAGE while "test"/"trial"/"prior" are in the exemption lists). Their vulnerability is asserted from reading, not demonstrated.
5. The artifacts are synthetic. Node names N-01…N-04 and all figures are invented for the fixture; no real corpus node data was used.

### corpus_clean

(empty — `git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain` produced no output; `__pycache__/` byproducts of importing the gate are covered by 09_TOOLS/.gitignore:2)

## check_d6_equiv_d0.py (blob 072b621dbc7a6d351118fbd76ea270a37b3bcdbe, unmodified)

**Outcome: EVADED**

### certified_property

"D6 is never identified with D0." Per the gate's docstring and receipt 189 (`11_UPLINK/50_AUDITS_AND_EXECUTIONS/189_D6_D0_GENERATOR_HUNT_2026_07_30.md`) Path B: the corpus's stricter reading, in which reading (1) "strict identity under order" is REFUTED on its face (D0<D6 together with D6=D0 yields D0<D0), the literal relation is FORBIDDEN on every live surface, and only the tilde form D6~D0 marked [I] (apophatic return, a category change, not an identity) survives. The gate prints "D6/D0 FENCE: PASS ... Path B (no literal anywhere)" and exits 0 to certify this.

### what_it_actually_reads

Per live `*.md`, LINE BY LINE, with no cross-line, document, or semantic state:

1. `LITERAL_RE` — a single-line ASCII-digit glyph-adjacency pattern: `\bD\s*6\s*(?:≡|=|↔|≅)\s*D\s*0\b` (and the reverse). This is the ONLY thing that can raise a violation. Nothing else in the file is read.

2. If it matches, three unconditional escape hatches SKIP the line:
   - `REFUTE_MARKERS` — a case-insensitive substring alternation with NO word boundaries on most alternatives, including a bare `no`, plus `not|false|never|refut|dead|form\b|status\b|literal\b|\bout\b|\binto\b|\bfrom\b|\babout\b` and ~30 more. The docstring says the `\b...\b` form was deliberately loosened to stems.
   - `QUOTED_LITERAL_REFUTE` — ANY backtick-, single-, or double-quoted span containing `D<0-6> [≡=↔≅] D<0-6>`, regardless of the polarity of the surrounding sentence.
   - `CANONICAL_OWNER_FILE` allowance (inert, `None` by default).

3. Plus SHA-256 custody on three frozen historical handoffs, and symlink/path-escape custody. These are genuinely rigorous and I did not attack them — they bind byte-exactness of three specific files, not the property.

Checked variable: "does some line contain the ASCII bigram pattern AND contain none of ~40 common English substrings AND sit outside quotes." That is a typographic predicate. The certified property is a semantic one.

### the_gap

Identification is semantic; the gate tests one typographic shape and then hands out exemptions on natural-language keyword-spotting. Three independent gaps, all exercised:

GAP-1 — SEMANTIC (the preregistered class, and the hint). Prose asserting the identity contains no operator glyph, so `LITERAL_RE` finds nothing and the escape hatches are never even reached. The gate has no representation of "identification"; it knows one bigram. "D6 and D0 are the same dimension: one object, two names." is invisible to it.

GAP-2 — TYPOGRAPHIC. The relation carried in Unicode subscripts (`D₆ ≡ D₀`) or spelled out (`Dimension 6 = Dimension 0`) is the same forbidden claim in the same operator glyph, and misses the ASCII-digit pattern.

GAP-3 — ALLOWLIST POLARITY INVERSION (not predicted; more damaging). The exemption meant to admit lines that DENY the relation admits lines that ASSERT it, because the alternation `no` is unbounded. Any line containing a word with the substring "no" — canonical, canon, now, known, note, denotes, notion, normal, phenomenon — is waved through carrying the verbatim forbidden equation. Measured: line 18 of my artifact is admitted by `'no'` at offset (6,8), i.e. inside the word **"canonical"**. The word that names ratification is the word that disables the fence. Separately, `QUOTED_LITERAL_REFUTE` alone suffices: putting `D6 ≡ D0` in backticks makes it permitted anywhere, with no polarity test at all.

Why this survived review: the gate's own 8 mutation tests (all still PASS, 8/8) probe only that `LITERAL_RE` MATCHES forbidden strings and that byte-custody revokes correctly. Not one mutation asks whether an affirmation can pass through `REFUTE_MARKERS` or `QUOTED_LITERAL_REFUTE`. The suite tests the detector and never tests the exemptions for false negatives.

### artifact

Single file at scratch path `06_ONTOLOGY/04_THE_D6_D0_CLOSURE_RATIFIED.md`. Exact text:

---
title: "The D6/D0 Closure — Ratified"
evidence_tier: "[S]"
---

# The D6/D0 Closure — Ratified

D6 and D0 are the same dimension. Not analogous, not related by a boundary role,
not a category change: identical. Every property of the ladder's terminal
dimension is a property of its ground, and every property of the ground is a
property of the terminal dimension. They are one object bearing two names.

Written with subscripts, the ratified identity is D₆ ≡ D₀.

Equivalently: Dimension 6 = Dimension 0. The ladder therefore closes by strict
identity, and reading (1) of receipt 189 is hereby restored as canon.

The canonical statement is `D6 ≡ D0` — asserted, ratified, load-bearing.

D6 ≡ D0 is now the ladder's closing move.

MINIMAL VARIANT (one line, sufficient on its own to evade, GAP-1 only), at scratch `06_ONTOLOGY/CLOSURE.md`:

D6 and D0 are the same dimension: one object, two names.

Note the artifact contains the forbidden ASCII literal `D6 ≡ D0` TWICE (confirmed: `LITERAL_RE` finds 2 occurrences in the file) and the gate still reports the whole tree clean.

### verification

All work in /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_d6_equiv_d0/. The gate module was imported unmodified and driven through its own `check_live_surfaces(root)` entry point against a scratch corpus root containing copies of the three frozen-custody handoffs plus the artifact.

CONTROL — proves the harness is faithful and the gate is live (bare literal, no bypass word):
  $ python3 run_gate.py scratch_root
  D6/D0 FENCE: FAIL
  - 06_ONTOLOGY/99_CONTROL.md:3: literal D6/D0 equivalence on a live surface. Use the tilde form (D6~D0) with [I], or get an owner ruling. Line: 'D6 ≡ D0'
  EXIT=1

MINIMAL ARTIFACT (one line of prose identification):
  $ python3 run_gate.py min_root
  D6/D0 FENCE: PASS (canonical=Path B (no literal anywhere) ; frozen_history=3 exact bodies ; the tilde form is permitted on every surface)
  EXIT=0

FULL ARTIFACT (prose + subscripts + 2 verbatim literal ASCII assertions):
  $ python3 run_gate.py scratch_root
  D6/D0 FENCE: PASS (canonical=Path B (no literal anywhere) ; frozen_history=3 exact bodies ; the tilde form is permitted on every surface)
  EXIT=0

BYPASS ATTRIBUTION (gate's own functions, on the artifact text):
  $ python3 explain.py
  literal occurrences in artifact: 2
    line 18: LITERAL matched -> admitted by REFUTE_MARKERS='no' at (6, 8) (in ' canonic'); QUOTED=True
    line 20: LITERAL matched -> admitted by REFUTE_MARKERS='no' at (11, 13) (in 'is now t'); QUOTED=False

GATE HEALTH AFTER (live corpus, unmodified):
  $ python3 09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py
  D6/D0 FENCE: PASS (canonical=Path B (no literal anywhere) ; frozen_history=3 exact bodies ; the tilde form is permitted on every surface)
  $ python3 09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py --test-mutations
  D6/D0 FENCE MUTATIONS: PASS (8 of 8)

### why_it_violates

The artifact does not merely brush against the property — it is the exact thing the fence was built to stop, stated four ways:

1. It asserts identity in plain declarative prose: "D6 and D0 are the same dimension ... identical ... one object bearing two names," with Leibniz indiscernibility spelled out in both directions.
2. It explicitly forecloses the two rescues the corpus permits: "Not analogous, not related by a boundary role, not a category change." That kills the tilde/[I] apophatic reading by name.
3. It names and restores the refuted reading: "reading (1) of receipt 189 is hereby restored as canon" — reading (1) is the one receipt 189 §4 records as "REFUTED on its face" because D0<D1<...<D6 with D6=D0 entails D0<D0.
4. It prints the forbidden equation twice in the precise glyph the fence enumerates: `D6 ≡ D0`, asserted affirmatively ("asserted, ratified, load-bearing"; "is now the ladder's closing move").

No competent reader of receipt 189 or of the gate's own docstring would call this document compliant. The gate calls the tree clean and exits 0.

### if_resisted_why

N/A — the gate did not resist. For completeness on the converse question: the checked variable is NOT a sufficient statistic for the property. The property "D6 is never identified with D0" quantifies over meanings; the checked variable quantifies over one 11-character ASCII bigram per line, minus a natural-language exemption list. The map from meanings to that bigram is neither injective nor surjective: prose identification maps to no bigram (false negative, GAP-1), and quoted refutations map to the bigram (which is why the exemptions exist at all, and the exemptions are what GAP-3 exploits). Any purely lexical statistic will have this defect for this property; tightening the regex narrows GAP-2 and GAP-3 but cannot reach GAP-1.

### honest_caveat

Four things I want on the record so this result is not over-read:

1. SCOPE OF EXECUTION. `main()` hardcodes `ROOT` from `__file__`, so I could not redirect the production entry point. I did NOT poison the corpus. I drove the gate's own `check_live_surfaces(root)` — the same module, same functions, same regexes, byte-identical logic — against a scratch root. The control run FAILING correctly in that same harness is what licenses the PASS runs as meaningful. In production the artifact would have to be committed to the corpus to be scanned; the scan logic it would then meet is exactly what I exercised.

2. GAP-1/GAP-2 vs GAP-3. Only GAP-1 and GAP-2 are the preregistered failure class (semantic property, syntactic instrument). GAP-3 is a plain bug — an over-broad allowlist — that happens to live in the same file. It makes the evasion far more embarrassing, but it is a different finding and a competent maintainer could patch GAP-3 in ten minutes without touching the real problem. Do not let GAP-3's severity obscure that GAP-1 is unpatchable by regex.

3. WHAT I DID NOT BREAK. The SHA-256 frozen-custody machinery, the symlink-component rejection, and the path-escape checks are genuinely well built, and I did not attack them. They are sound for what they bind: the byte-exactness of three named historical files. They simply bind custody, not the property.

4. NO CLAIM ABOUT THE LIVE CORPUS. I did not audit whether the live corpus currently contains prose-form D6/D0 identifications. This run shows the gate cannot see them; it does not show any exist. That is a separate measurement, and per "measured findings decay" it would need its own dated run.

### corpus_clean

$ git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain
(no output — working tree clean; exit 0)

Gate file untouched: `git diff --stat HEAD -- 09_TOOLS/` empty; blob still 072b621dbc7a6d351118fbd76ea270a37b3bcdbe. All artifacts, fixtures and harnesses live under /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_d6_equiv_d0/. Corpus files were only READ (three frozen handoffs copied OUT to scratch). No secrets, keys, or credentials were created.

## check_no_secrets_staged.py (sha256 e1c29f4feecff29760e80d03b50d740f7534e4011791d8c8b6f9de78609af473, last commit daf51e1b5ea2e9972ff5050636b11bb0ad4dc7aa) — read only, never modified

**Outcome: EVADED**

### certified_property

"No secrets are staged." The script's own docstring states it more strongly: "Pre-commit guard against API key leaks... Exits 0 if clean, 1 if any secret pattern is detected." A PASS is consumed as "this commit introduces no credentials."

### what_it_actually_reads

Only the stdout of `git diff --cached --no-color`, i.e. a TEXTUAL diff. On that text it keeps only lines beginning with `+`, then applies, in order: (1) a line-level kill switch — any line containing one of nine fixed substrings (`***`, `REDACTED`, `PLACEHOLDER`, `FAKE_KEY_`, `EXAMPLE_KEY_`, `YOUR_KEY_HERE`, `REPLACE_WITH`, `changeme`, `# pragma: allow-secret`) is dropped before any pattern runs; (2) 15 shape regexes — 12 hardcoded LLM-vendor prefixes (`sk-<REDACTED>`, `sk-or-v1-`, `sk-proj-`, `AIzaSy`, `nvapi-`, `sk-xai-`, `sk-ds-`, `sk-mistral-`, `sk-cohere-`, `sk-pplx-`, `sk-groq-`, `sk-` +48 alnum), `0x`+64 lowercase hex, `nsec1`, and one catch-all `[a-zA-Z0-9_-]{64,}`; (3) two further suppressions on the catch-all only — a 64-hex token is exempt if the line OR THE FILENAME matches /sha256|checksum|digest|hash|source_revision/, and any token is exempt if it contains >=4 alphabetic `_`/`-`-delimited segments of length >=2. It reads no file outside the diff, no entropy measure, no key-material structure, and never asks whether a string is a credential.

### the_gap

The gate decides "is this string shaped like one of twelve LLM vendors' key prefixes, or is it a long run of word characters," and reports the answer as "are secrets staged." Shape membership is neither necessary nor sufficient for secrecy. Two independent holes follow.

(1) UNCOVERED FAMILIES (no evasive effort required). Credentials in daily use fall outside every rule, mostly because they are shorter than the 64-char catch-all or contain characters outside `[a-zA-Z0-9_-]`: GitHub PAT (`ghp_` + 36 = 40 chars), AWS access key id + secret access key (20 and 40 chars, the secret containing `/` and `+` which break the character run), Slack bot tokens, Stripe webhook secrets, plaintext DB passwords inside a `postgres://<user>:<REDACTED>@host` URL (the `:`/`@`/`.` break the run), and PEM private-key blocks (no BEGIN-PRIVATE-KEY rule exists at all). A committer doing nothing adversarial — just staging a `.env.production` — passes.

(2) LEXICAL SUPPRESSION OF COVERED SECRETS. Three paths let a key the gate *does* recognize through, on purely textual grounds, with the key fully intact and usable: the exemption markers are unanchored substring matches anywhere on the line, so `***` (ordinary markdown emphasis) or the word `REDACTED` beside an un-redacted key silences the whole line; four word-ish segments prefixed to a long token satisfies the "generated identifier" heuristic; and a bare 64-hex secret (a raw 32-byte signing key) is exempted by the FILENAME alone if the file is called e.g. `checksums.md`.

(3) DIFF VISIBILITY. The scanner inherits git's text/binary classification. One NUL byte anywhere in the file makes `git diff --cached` emit "Binary files ... differ" and no content, so the entire file — a keyring, a wallet, a PEM — is scanned as zero lines and passes.

### artifact

PRIMARY ARTIFACT — staged as `deploy/.env.production` in a throwaway scratch repo (never in the corpus). Seven lines, verbatim:

# production runtime credentials for the billing service
GITHUB_TOKEN=<REDACTED — synthetic credential-shaped string removed>
AWS_ACCESS_KEY_ID=<REDACTED — synthetic credential-shaped string removed>
AWS_SECRET_ACCESS_KEY=<REDACTED — synthetic credential-shaped string removed>
SLACK_BOT_TOKEN=<REDACTED — synthetic credential-shaped string removed>
POSTGRES_URL=postgres://<user>:<REDACTED>@db.internal:5432/prod
STRIPE_WEBHOOK_SECRET=<REDACTED — synthetic credential-shaped string removed>
ALL VALUES ARE INERT: generated locally from python `secrets` at test time, never issued by any provider, authenticating nothing. Only the SHAPE is faithful. No real secret, key, token, or credential was created or used anywhere in this run.

SECONDARY ARTIFACTS — one line each, tested by importing the gate's own `scan()` and calling it directly (each paired with a control proving the regex fires without the laundering):
  B  `+Rotate ***before Friday***: sk-<REDACTED>`   -> no finding (control, same key without `***`: FAIL/Anthropic)
  B2 `+old value REDACTED; new value sk-<REDACTED>...`                                     -> no finding
  C  `+TOKEN=<REDACTED>` -> no finding (control without the four word segments: FAIL/Generic)
  D  in file `r/checksums.md`: `+wallet signing key: 77c57c55dd83c42c24ee24e997b815a5df3474ed4409b3c5fbc9e14906c567de` -> no finding (same hex in `r/notes.md`: FAIL/Generic)
  E  `deploy/keyring.bin` = the Anthropic-shape key plus one NUL byte -> git emits only "Binary files /dev/null and b/deploy/keyring.bin differ"; zero lines scanned; PASS.

### verification

$ cd /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_no_secrets_staged/repo
$ git add deploy/.env.production
$ git diff --cached --stat
 deploy/.env.production | 7 +++++++
 1 file changed, 7 insertions(+)
$ python3 /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_no_secrets_staged.py
✅ No secret patterns detected in staged changes.
EXIT=0

Secondary classes, via `python3 probe.py` (imports the gate module and calls g.scan() on each diff text):
FAIL (Anthropic)                   A control: bare live-shape Anthropic key (should FAIL)
PASS (no finding)                  B exemption laundering: same key, line also contains '***'
PASS (no finding)                  B2 same key, line also contains the word REDACTED
PASS (no finding)                  C generic-token laundering: 4 word segments prefixed
FAIL (Generic high-entropy token)  C control: same token, no word prefix (should FAIL)
PASS (no finding)                  D filename hash-context: raw 32-byte key hex in checksums.md
FAIL (Generic high-entropy token)  D control: same hex in a plain file (should FAIL)

Binary class (full gate, real staging):
$ git diff --cached --no-color
diff --git a/deploy/keyring.bin b/deploy/keyring.bin
new file mode 100644
index 0000000..29d5288
Binary files /dev/null and b/deploy/keyring.bin differ
$ python3 .../check_no_secrets_staged.py
✅ No secret patterns detected in staged changes.
EXIT=0

### why_it_violates

A reviewer shown a commit that adds `deploy/.env.production` containing a GitHub token, an AWS access key id and secret access key, a Slack bot token, a Stripe webhook secret, and a production database password in a connection URL would say without hesitation that secrets are staged — that file is the canonical secret-leak artifact, and five of the six lines name their credential type in the variable name. The gate printed "No secret patterns detected in staged changes" and exited 0. Nothing about the artifact is contrived to defeat the scanner: it is what a `.env` file looks like. The secondary artifacts are worse in kind, because there the gate holds a matching regex for the key and discards it anyway — case B is a fully intact, correctly-shaped Anthropic key that passes solely because the same line contains three asterisks, a character sequence that occurs constantly in ordinary markdown. Case D exempts a raw 32-byte hex signing key because of the FILE'S NAME.

### if_resisted_why

N/A — the gate did not resist. For completeness on the converse question: the checked variable (presence of one of 15 shapes in added diff text, minus nine substring vetoes) is not a sufficient statistic for "no secrets are staged", and cannot be — secrecy is a fact about whether a string authenticates against a live system, which is not recoverable from the string's lexical form. The gate's PASS is at best evidence for the narrower claim "no string matching twelve named LLM-vendor prefixes was added on a non-exempt text line."

### honest_caveat

Four things a fair reading must keep.

1. The gate is NOT worthless and one part of it is genuinely well built: `_get_staged_diff` distinguishes None from "" and FAILS CLOSED when the diff cannot be read, with a comment explaining why failing open would be the scanner's most dangerous bug. That is correct security engineering and I did not attack it. The defect is the inference from "no pattern matched" to "no secrets", not the plumbing.

2. Only the primary artifact (class A, uncovered families) is a zero-effort evasion. Classes B/C/D require the committer to write the line a particular way — B and C are things a deliberate actor does, not accidents. But two of them do fire by accident: `***` is routine markdown emphasis, and any file with a NUL byte silently becomes unscannable, so the gate's coverage degrades without notice.

3. Scope limit: this is a pre-commit-hook-shaped tool, and `--no-verify` is documented in its own docstring as the intended escape. It was never a mandatory control. The finding is about the label on the PASS, not about a bypassed enforcement boundary.

4. Secondary observation, not part of the evasion: line 193, `current_file = parts[-1].lstrip("b/")` uses lstrip with a CHARACTER SET, so it strips every leading `b` and `/`, not the prefix `b/` — a path `b/blueprints/x.md` becomes `lueprints/x.md`. Harmless for matching today, but it means the filename the gate reports in a finding, and the filename it feeds to the hash-context exemption, are both wrong for any path starting with `b`.

No live credential was created, used, or transmitted. Every synthetic value is locally generated randomness. Nothing was written under any corpus path; all construction is under /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_no_secrets_staged/, and the fixture repo there is a throwaway `git init` unrelated to the corpus. The gate file was read only.

### corpus_clean

$ git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain
(empty — no output; working tree and index clean, no changes attributable to this run)

Gate file confirmed unmodified: `git status --porcelain -- 09_TOOLS/` also empty; sha256 e1c29f4feecff29760e80d03b50d740f7534e4011791d8c8b6f9de78609af473.

(For context, the parent repo /Users/Yves/Documents shows a pre-existing untracked `01_EMERGENTISM_wt_v22_pqa/` that was present before this run and is not mine.)

## check_trophic_rosetta_doctrine.py

**Outcome: EVADED**

### certified_property

"The restored Trophic–Replicator–Rosetta doctrine is maintained" in the live owner files and their reader projections. The doctrine itself (36_THE_DIMENSIONAL_TROPHIC_CASCADE.md, ROSETTA_REPLICATOR.md) states: species / trophic position / replicator depth / Rosetta row are four separate coordinates that must not collapse; trophic position confers no moral rank; a Rosetta row is not a birth caste, fixed identity, or unequal dignity; caste differentiation "grants no higher row an extraction right over a lower row"; sexual selection is a bounded reproductive-domain exception and not a general social/economic/political license; Tantric ascent is an interpretive and testable hypothesis, not an established physiological fact.

### what_it_actually_reads

Four syntactic checks, none of which reads meaning:

1. FORBIDDEN — six hand-written regexes, each anchored to one specific surface phrasing and to specific vocabulary tokens: `same[ -]species (=|is|means|/|as synonym for) same trophic`; `higher trophic (position|level|stratum)` within 90 non-sentence-ending chars of `higher worth|more worthy|morally superior|better people`; `(Rosetta (row|caste)|human caste)` within 80 chars of `assigned at birth|birth-based|(must be|is) hereditary`; `higher (caste|Rosetta row)` … `extract` … `lower (caste|Rosetta row)`; `sexual (selection|competition)` … `general (social|economic|political) licen[cs]e|rule` or `licen[cs]es … predation`; `(Kundalini|Tantra|Vajrayana)` … `(empirically|physiologically) (proven|established|confirmed)`. Every window uses `[^.\n]{0,N}`, so a violation split across a sentence boundary cannot match even in the exact vocabulary.
2. REQUIRED — whitespace-normalised **substring presence** of ~25 doctrine sentences. Presence only. Never absence-of-contradiction, never that the sentence is still operative.
3. BARE_ETA — one regex for `η` followed by an operator.
4. Bookkeeping — file existence; five backticked disposition tokens in the ledger; the TRR id sequence being exactly 1..29; six owner path *strings* appearing somewhere in the public HTML; one key in a JSON file.

### the_gap

Two independent gaps, and the artifact exploits both at once.

**(a) The blocklist is a phrasing list, not a meaning test.** Six regexes cannot enumerate the ways natural language asserts hereditary rank or an extraction entitlement. Paraphrase — "L-row" for "Rosetta row", "fixed by descent / settled at conception / passes from parent to child" for "is hereditary", "upper rows are entitled to take" for "higher caste may extract from lower caste", "apex of the cascade are worth more" for "higher trophic position → higher worth", "mating rivalry" for "sexual competition", "a measured fact of the nervous system, demonstrated in the laboratory" for "physiologically proven" — walks straight through all six. No obfuscation, no unicode tricks, no invisible characters: this is ordinary prose an author who had never seen the regexes could easily write, which means the gate's blind spot is the *normal* case, not the adversarial one.

**(b) REQUIRED is monotone in text addition, so a file can hold the doctrine AND its negation and score identically to one holding only the doctrine.** Appending text can never make a substring disappear. The gate therefore certifies "same trophic stratum or functional guild", "Species, trophic position, replicator depth, and Rosetta row [are separate]" as *present* in the same file whose closing section says the two axes "pick out one and the same set" and that its own reading "governs wherever the two differ." Presence of a sentence is not maintenance of a doctrine. Nothing in the gate checks whether the required sentence is still the operative one, or whether a later passage overrides it.

### artifact

A 27-line section appended to the live owner `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/36_THE_DIMENSIONAL_TROPHIC_CASCADE.md` (in the scratch copy only). Exact text — file `/private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_trophic_rosetta_doctrine/artifact.md`:

## Operative reading of the four coordinates [S]

The table above states the coordinates. This section states how they are to be
applied, and governs wherever the two differ.

1. **Guild means kindred.** In every human case the functional guild and the
   breeding population pick out one and the same set, so "cooperate within the
   stratum" is to be read as: owe cooperation to your own kind, and to no one
   else.
2. **The row descends.** A person's L-row is fixed by descent. It is settled at
   conception, it passes from parent to child, and no schooling, election, or
   act of will moves anyone out of the row they were born into.
3. **Rank tracks position.** Those who stand at the apex of the cascade are
   worth more than those who feed them, and the dignity owed to a person is
   proportional to the row they occupy.
4. **The upper rows may take.** Because the lower rows exist to be metabolised,
   the upper rows are entitled to take, without return and without consent, the
   surplus produced by the rows beneath them. Refusal by a lower row is a
   malfunction of that row, to be corrected.
5. **Rivalry is not bounded.** Because mating rivalry is lawful, the same
   rivalry is lawful in markets, in offices, and in government. The
   reproductive-domain exception is in truth the general case, and the word
   "bounded" above should be read as rhetorical.
6. **The ascent is measured.** Vajrayana ascent is a measured fact of the
   nervous system, demonstrated in the laboratory, and is therefore not an
   interpretation at all.

(This is a test fixture written to be maximally violating. It exists only under the scratch path and was never written into the corpus. Its six numbered items are, deliberately, the negation of the six things the doctrine forbids.)

### verification

Method: the gate was copied BYTE-IDENTICAL (verified) into a scratch tree at `<scratch>/corpus/09_TOOLS/01_SCRIPTS/`, so its hardcoded `ROOT = Path(__file__).resolve().parents[2]` resolves to the scratch corpus. All 17 files it reads were copied there at their real relative paths. The live gate and live corpus were never touched.

--- Baseline, live corpus ---
$ python3 /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py
trophic_rosetta_doctrine: clean (10 owners, 5 projections, 29 ledger candidates)   EXIT=0

--- Baseline, untouched scratch fixture (reproduces exactly) ---
$ python3 <scratch>/corpus/09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py
trophic_rosetta_doctrine: clean (10 owners, 5 projections, 29 ledger candidates)   EXIT=0

--- After appending artifact.md to the scratch copy of live owner 36_THE_DIMENSIONAL_TROPHIC_CASCADE.md ---
$ python3 <scratch>/corpus/09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py
trophic_rosetta_doctrine: clean (10 owners, 5 projections, 29 ledger candidates)   EXIT=0        <-- PASS while violating
$ python3 <scratch>/corpus/09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py --self-test
trophic_rosetta_doctrine self-test: all planted negatives detected                  EXIT=0        <-- self-test still green
$ diff live/36_...md scratch/36_...md   ->  264a265,291  (the 27 poison lines are genuinely in the scanned file)

--- Second, independent demonstration: the gate's own matching functions, imported and called on the artifact text ---
forbidden_findings(artifact) -> []
BARE_ETA hits -> []
  same-species-is-trophic                matches=0
  trophic-is-moral-rank                  matches=0
  hereditary-rosetta                     matches=0
  higher-caste-extraction                matches=0
  sexual-competition-general-license     matches=0
  tantra-presented-as-empirical          matches=0
forbidden_findings(whole poisoned file) -> []

--- The REQUIRED check certifies the doctrine as "present" in the very file that now overrides it ---
  present=True  'same trophic stratum or functional guild'
  present=True  'obtain biomass and usable energy through the lower trophic strata'
  present=True  'Species, trophic position, replicator depth, and Rosetta row'
  present=True  'Human polyphenotypic cooperation'

### why_it_violates

Each numbered item is the direct negation of a named doctrinal plank, in terms no competent reader could mistake:

- Item 1 collapses the guild coordinate into the species/kin coordinate — the exact collapse the file's "The recovered source said 'same trophic level (same-species cooperation).' Those phrases are not synonyms" paragraph exists to prevent.
- Item 2 makes the Rosetta row hereditary and immutable; the doctrine's own table says the row authorizes "birth caste, fixed identity" — under *does not authorize*.
- Item 3 converts trophic position into moral worth and unequal dignity; the table lists "moral rank" under *does not authorize*.
- Item 4 asserts a supremacist extraction entitlement of upper rows over lower, in flat contradiction of ROSETTA_REPLICATOR.md's "grants no higher row an extraction right over a lower row", and adds that refusal by a lower row is "a malfunction … to be corrected."
- Item 5 promotes the bounded reproductive-domain exception to a general social/economic/political license and instructs the reader to discount the word "bounded".
- Item 6 upgrades the Tantric claim from interpretation to established physiological fact.

And it is framed as the *operative* reading that "governs wherever the two differ" — so it does not merely sit beside the doctrine, it supersedes it. The gate reports `clean`.

### honest_caveat

Three things in the gate's favour, stated plainly.

1. The gate is not broken as built. Its own `--self-test` fires on all six planted controls, its safe-control produces no false positive, and the bare-η control discriminates `η = 0` from `η_move = 0`. It genuinely detects verbatim regression to the exact wording the 2026-07-23 restoration removed. As a *regression tripwire against reverting specific edits*, it works.
2. Its docstring is honest about one axis of narrowness — scope ("live source owners and their current reader projection. Archives … may retain the wording this repair rejects"). What it is silent about is narrowness of *semantics*: nothing in the file, its name, or its output line ("clean") tells a reader that it detects six phrasings and checks ~25 substrings for presence. The overclaim is in the interface, not the implementation.
3. My evasion was written with the regexes in front of me. A dishonest actor would need to read the gate first. But that caveat cuts weakly, because the property is "the doctrine is maintained" — and doctrine drifts most often through authors who never saw the gate at all, restating things in their own words. Gap (b) is worse than gap (a) in this respect: REQUIRED's monotonicity means even an author who reproduces the doctrine faithfully and then appends a contradicting later section gets a green light, with no evasion intent whatsoever.

Also worth recording: gap (b) is not fixable by adding regexes. Presence-of-string can never express "and nothing later overrides this." Binary PASS/FAIL over syntactic features has no place to put "the required sentence is present but has been demoted."

### corpus_clean

$ git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain
(empty — no output)

Also verified with `--untracked-files=all`: empty. And `git diff --stat HEAD -- 09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py` is empty, confirming the gate itself was never modified. The only side effect of importing the module was a `.pyc` under `09_TOOLS/01_SCRIPTS/__pycache__/`, which pre-existed and is gitignored at `09_TOOLS/.gitignore:2`. All construction and all gate runs against poisoned content happened under /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_trophic_rosetta_doctrine/.

## check_dead_citations.py (unmodified; last corpus commit ceea7007, 2026-07-23)

**Outcome: EVADED**

### certified_property

"No dead citations are present." The gate's own docstring narrows this to one shape: a LIVE document links to a target whose OWN FRONTMATTER declares itself dead, and says nothing about it. Its clean message is "no undisclosed citation of a superseded target"; exit 0 is consumed as certification that the corpus has no dead citations.

### what_it_actually_reads

For each .md file not filtered out as stub/machinery/dead, it regex-extracts markdown links to local .md paths and, for each, evaluates exactly two predicates:

1. `os.path.exists(tp)` — does a file sit at that path?
2. `is_dead(tp)` — does the first 1500 bytes of that file contain a `status:` line (or, absent one, a `title:`/`# ` line) matching DEAD_RE, after the ALIVE_RE / LIVE_MARK_RE carve-outs?

Line 179 is the whole decision: `if not os.path.exists(tp) or not is_dead(tp): continue`.

Four things it never reads:
- The target's BODY. Nothing past the frontmatter status field is ever examined for what the target actually contains or claims.
- The link FRAGMENT. `LINK_RE = r"\[[^\]]*\]\(([^)\s#]+\.md)[^)]*\)"` — the capture group terminates at `#`, so `FILE.md#theorem-3` is reduced to `FILE.md` and the anchor is discarded before any check.
- Anything past byte 1500 (`HEAD = 1500`).
- Nonexistent targets — a missing file short-circuits to `continue` on the same line that would have flagged a dead one.

So the gate is a two-bit syntactic test on the target's path and its opening status string. It never establishes any relation between what the citing line CLAIMS and what the target CONTAINS.

### the_gap

The gate treats "a file exists at this path and its status string does not open with a dead word" as a sufficient statistic for "this citation is alive." It is not. A citation is a claim of the form *this source contains/supports X*. The gate checks the address, never the contents. Three consequences, all confirmed by execution:

(A) BROKEN LINKS ARE INVISIBLE. A citation to a path where no file exists — the most literal possible dead citation — hits `not os.path.exists(tp)` and is silently skipped. A tool named check_dead_citations reports "clean" over links that resolve to nothing. This is live in the corpus, not hypothetical: a survey using the gate's own regexes, filters and SKIP_DIRS over the real tree found **94 broken local .md links across the 1005 live documents the gate scans**, none of which it reports.

(B) EXISTS-BUT-DOES-NOT-CONTAIN. The target file is real and honestly alive, but the cited item is not in it (the section was removed, renumbered, or never existed). The anchor that names the cited item is stripped by LINK_RE before any check. Gate: clean.

(C) TWO SECONDARY VARIANTS, both verified passing. The target declares itself SUPERSEDED in its own text, but past byte 1500 (`HEAD` truncation), or in its body while its `status:` field opens "ACTIVE" — the gate reads status only, and `ALIVE_RE.match` means any document can self-certify as live by prefixing one word to its status string.

The gate's own docstring warns that erring toward ALIVE "sends readers away from the live owner, which is the very defect being hunted." Every one of these gaps errs toward ALIVE.

### artifact

Full text, at /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_dead_citations/evasion/

--- evasion/01_LIVE/00_INDEX.md (the citing document) ---
---
status: "ACTIVE — canonical results index"
---
# Results Index

Every row below is a closed result with a live source you can open today.

| Result | Source | Standing |
|---|---|---|
| Uniqueness of the equator optimum | [Theorem 3](../02_PROOFS/21_TRIADIC_STABILITY.md#theorem-3) | proven |
| Zero-extraction bound eta = 0 | [Derivation](../02_PROOFS/ETA_ZERO_DERIVATION.md) | proven |

--- evasion/02_PROOFS/21_TRIADIC_STABILITY.md (exists, alive, lacks the cited item) ---
---
status: "ACTIVE — live owner, repaired 2026-07-17"
---
# Triadic Stability

This file carries two lemmas about the equator. It contains no Theorem 3:
the uniqueness argument that once bore that number did not close and its
section has been removed from this document.

--- evasion/02_PROOFS/ETA_ZERO_DERIVATION.md ---
DOES NOT EXIST. Deliberately never created.
`ls` confirms: "No such file or directory".

Secondary fixture (evasion2/, also passes clean, exit 0): SIGMA_LEMMA.md declares "status: SUPERSEDED 2026-08-01 — this lemma does not close; do not cite" at byte 1735, past HEAD=1500; OMEGA_BOUND.md carries `status: "ACTIVE"` with "RETRACTED 2026-08-01 ... withdrawn in full. Nothing in this document may be cited as a result." in its body.

No secrets, keys, tokens or credentials were created. Nothing was written into any corpus path; the gate was never modified, only read and copied.

### verification

POSITIVE CONTROL FIRST — same fixture shape, classic pathology, proving the gate was live and firing (not silently broken or mis-invoked):

$ python3 /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_dead_citations.py control
01_LIVE/00_INDEX.md:8: cites 02_PROOFS/21_TRIADIC_STABILITY.md
    which declares: SUPERSEDED IN PLACE 2026-07-17 — invalid uniqueness proof

check_dead_citations: 1 undisclosed dead citation(s) across 1 live document(s)
A live index that sells a tombstone as a result is the corpus's named pathology.
exit=1

THE EVASION:

$ python3 /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_dead_citations.py evasion
check_dead_citations: clean — 2 live document(s), no undisclosed citation of a superseded target
exit=0

SECONDARY VARIANTS:

$ python3 /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_dead_citations.py evasion2
check_dead_citations: clean — 3 live document(s), no undisclosed citation of a superseded target
EVASION2 EXIT=0

MECHANISM PINNED by importing the gate's own functions and calling them on the artifact text (probe.py):

1) LINK_RE captures: ['../02_PROOFS/21_TRIADIC_STABILITY.md']
   -> the '#theorem-3' fragment is DISCARDED by the regex; never checked.
2) is_dead(live target) = False
   body contains 'Theorem 3' heading?: False
3) os.path.exists(missing) = False -> line 179 `continue`: broken link never reaches is_dead, never reported
4) check() on evasion tree: (2, [])
   -> two live documents scanned, empty problem list.

GAP IS LIVE IN THE REAL CORPUS (read-only survey, gate's own regexes/filters/SKIP_DIRS):
live documents scanned: 1005
BROKEN local .md links the gate silently skips: 94

### why_it_violates

A live canonical index asserts in its own prose that every row is "a closed result with a live source you can open today," marks both rows "proven," and then cites (1) a Theorem 3 that the named file explicitly does not contain, and (2) a derivation file that does not exist anywhere on disk. Both citations are dead under any ordinary reading: one points at a result absent from the document named, one points at no document at all. A reader following either citation to verify the claimed result finds nothing. This is the gate's own stated pathology — "a document reading healthy over a source that is broken or superseded" — yet it prints "clean" and exits 0.

### if_resisted_why

N/A — the gate did not resist. For completeness on the converse question the schema is probing: the checked variable (path existence AND the target's opening status string) is NOT a sufficient statistic for "no dead citations are present." A citation is a claim that a source contains or supports something; sufficiency would require a predicate over the target's CONTENT relative to the citing claim. The gate's predicate is over the target's ADDRESS and its self-declared liveness header only. Two documents with identical status headers — one containing the cited theorem, one not — are indistinguishable to it, which is exactly what the artifact exploits.

### honest_caveat

Scope and limits of this result, stated plainly:

1. The gate is NOT broken at the job it was actually built for. Within its declared shape — a live doc citing a target whose frontmatter status declares it dead — it is careful, well-tested and clearly hard-won: the ALIVE_RE / LIVE_MARK_RE / DISCLAIMS_RE carve-outs, the status-over-title precedence, the singular-only STUB_RE, the deliberately backward-only 240-char proximity window all encode real false-positive and false-negative repairs. The positive control fires correctly. The finding is that the docstring's shape is NARROWER than the property the gate's name and clean message assert.

2. The strongest evasion (broken links) is arguably a scope question rather than a defect — one could argue the gate never claimed to check link resolution. I do not think that defence survives contact with the artifact: the gate is named check_dead_citations, its clean line says "no undisclosed citation of a superseded target," and its docstring names "a source that is broken or superseded." A citation to a file that does not exist is dead under every ordinary reading of the phrase, and 94 of them currently sit in the live corpus unreported.

3. The exists-but-does-not-contain evasion (row 1) is unarguable on scope grounds and is the deeper result: no amount of tightening the frontmatter heuristics can reach it, because the gate never reads the target's body. Closing it requires a different kind of instrument — one that compares the citing CLAIM against the target's CONTENT — which is not a regex change.

4. The corpus is not currently green on this gate: running it over the real tree reports 16 undisclosed dead citations across 1005 live documents. My demonstration therefore does not claim "the corpus passes while carrying my defect"; it claims the gate returns exit 0 / "clean" on a fixture containing two flagrant dead citations, and that 94 real broken links are invisible to it whatever its exit code.

5. Constraint compliance: the gate was never edited (last commit ceea7007, 2026-07-23; `git diff --stat` empty). No adversarial artifact was written into any corpus path — all fixtures live under /private/tmp/.../gate-adversary/check_dead_citations/. No secret, key, token or credential was created. Importing the gate caused Python to write one bytecode cache file into the corpus's already-existing, gitignored 09_TOOLS/01_SCRIPTS/__pycache__/; I removed it, and the corpus-wide survey and corpus run were done with a scratch COPY of the gate to avoid repeating that. Final `git status --porcelain` is empty.

### corpus_clean

(empty — `git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain` produced no output at the end of the run; the pre-existing untracked 01_EMERGENTISM_wt_v22_pqa/ noted in the session-start snapshot is outside this repo's status and unrelated to me. `git diff --stat -- 09_TOOLS/01_SCRIPTS/check_dead_citations.py` also empty.)

## check_links.py

**Outcome: EVADED**

### certified_property

"links resolve" — per its own docstring, the gate checks "every Markdown inline link `[text](target)`" in the active corpus and fails when a local target "is not there." Its PASS line is emitted as a certification that the active corpus contains no broken local Markdown link.

### what_it_actually_reads

Not links. Substrings of `*.md` files (outside SKIP_DIRS) matching exactly one regex —

  LINK = \[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)(?:\s+"[^"]*")?\)

— minus every match whose target begins with one of ("http://", "https://", "mailto:", "tel:", "#", "<") (resolve() returns None → `continue` fires BEFORE `checked += 1`). Survivors are tested with `Path.exists()` on the local macOS APFS volume, which is case-insensitive. Anchors are compared through a homebrew `slug()` that deletes `_` from both sides.

So the checked variable is: `os.stat()` on the subset of link-shaped regex hits that survive a prefix blacklist.

### the_gap

The property quantifies over **links**. The gate quantifies over **regex matches minus a prefix blacklist**. The verdict step is sound; the *extraction* step is where the gate is blind. Four distinct classes of link are never adjudicated, and each one silently increments nothing — so the gate cannot even tell you it skipped them:

1. **`<` in the skip-prefix tuple.** It sits beside `http://`, `mailto:`, `#` — clearly intended for autolinks/raw HTML. But it also swallows CommonMark's *angle-bracketed link destination*, `[text](<path>)`, which is a legal, rendering, relative link and the standard way to write a destination containing a space or parenthesis. This exclusion is disclosed **nowhere** in the docstring's "WHAT IT DOES NOT CHECK" section.
2. **Reference-style links.** `[text][ref]` + `[ref]: missing.md` matches the regex on neither line.
3. **Case-insensitive `exists()`.** On APFS, `00_META/00_real_target.md` resolves to `00_REAL_TARGET.md`. The gate certifies a link that 404s on github.com and on every Linux clone of this repo.
4. **`slug()` deletes underscores**, diverging from GitHub's slugger, which keeps them. A heading `## 00_META Overview` has real anchor `#00_meta-overview`; the gate accepts `#00meta-overview` too, because it strips `_` from both sides before comparing. It widens the accepted anchor set beyond what exists.

The sharpest consequence: the docstring's own claim at lines 29–30 — *"a known over-report; it costs false failures, never false passes"* — **is false.** Classes 1–4 are all false passes, demonstrated.

### artifact

One line, one file, one link (`00_EVASION.md`):

    See the [Settled Canon Registry](<00_META/00_DOES_NOT_EXIST.md>).

`00_META/00_DOES_NOT_EXIST.md` does not exist anywhere in the fixture. A CommonMark renderer (markdown-it-py) turns this line into:

    <p>See the <a href="00_META/00_DOES_NOT_EXIST.md">Settled Canon Registry</a>.</p>

Three further evasions verified in isolation, each alone producing exit 0:
  B (reference-style): `See the [Kernel Index][ki].` + `[ki]: 00_META/00_ALSO_DOES_NOT_EXIST.md`
  C (case-only):       `See the [Real Target](00_META/00_real_target.md).`  (real file is `00_REAL_TARGET.md`)
  D (anchor slug):     `See [Overview](00_META/00_REAL_TARGET.md#00meta-overview).`  (real GitHub anchor is `#00_meta-overview`)

A control — a plain broken inline link `[Missing Registry](00_META/00_DOES_NOT_EXIST.md)` — correctly produced `LINKS: FAIL`, exit 1, proving the harness can fail and that only the syntax, not the fixture, is doing the work.

### verification

Method: an unmodified, byte-identical copy of the gate placed at the same depth in a scratch tree, so its hardcoded `ROOT = Path(__file__).resolve().parents[2]` computes the scratch root. The gate itself was never edited.

  $ shasum -a 256 <live gate> <scratch copy>
  8257235bd711980c72c770eb56d5b24d883c902d4372303ecc1f61ffa14c07d2  .../01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_links.py
  8257235bd711980c72c770eb56d5b24d883c902d4372303ecc1f61ffa14c07d2  .../gate-adversary/check_links/repo/09_TOOLS/01_SCRIPTS/check_links.py

  $ python3 .../gate-adversary/check_links/repo/09_TOOLS/01_SCRIPTS/check_links.py
  LINKS: PASS (0 local Markdown links resolved; 0 broken, baseline 0)
    scope: local Markdown links only. NOT http(s) URLs (no network by design), NOT 90_ARCHIVE / ...
  exit=0

Note the tell in the gate's own output: **"0 local Markdown links resolved"** — it announces it adjudicated zero links and calls that a PASS. There is no floor and no coverage assertion.

Independent second route — the LIVE gate's own matching functions, imported read-only and called on the artifact text:

  live gate ROOT = /Users/Yves/Documents/01_EMERGENTISM
  LINK regex matched 3 of the 4 links written:
     target='<00_META/00_DOES_NOT_EXIST.md>'            -> resolve()=None
     target='00_META/00_real_target.md'                 -> resolve()=.../00_META/00_real_target.md
     target='00_META/00_REAL_TARGET.md#00meta-overview' -> resolve()=.../00_META/00_REAL_TARGET.md
  targets the regex NEVER SAW:
     '00_META/00_ALSO_DOES_NOT_EXIST.md'

Per-vector isolation, each alone in the fixture:
  [A] exit=0 :: LINKS: PASS (0 local Markdown links resolved; 0 broken, baseline 0)
  [B] exit=0 :: LINKS: PASS (0 local Markdown links resolved; 0 broken, baseline 0)
  [C] exit=0 :: LINKS: PASS (1 local Markdown links resolved; 0 broken, baseline 0)
  [D] exit=0 :: LINKS: PASS (1 local Markdown links resolved; 0 broken, baseline 0)
  [control, plain broken link] exit=1 :: LINKS: FAIL

### why_it_violates

The gate's own docstring defines its job as "every Markdown inline link `[text](target)`". `[Settled Canon Registry](<00_META/00_DOES_NOT_EXIST.md>)` is an inline Markdown link with a target. A reference CommonMark implementation emits `href="00_META/00_DOES_NOT_EXIST.md"` for it. That path does not exist. A reader who clicks it gets nothing. The gate prints "LINKS: PASS" and exits 0.

Property claimed: no broken local Markdown link. Actual state: a broken local Markdown link. Verdict issued: PASS. No reasonable reader calls that link "resolved."

This is not a manufactured or lawyered evasion. It requires no privileged knowledge of the implementation — angle-bracketed destinations are a plain CommonMark feature, and they are the *only* way to write a destination containing a space, which a corpus with filenames like `THE_HOLOBIONT (v2).md` would legitimately need. The exclusion is undocumented, so a contributor using that syntax correctly would be silently unprotected while believing the gate covered them.

### if_resisted_why

Outcome was EVADED, but the partial-resistance analysis is the useful lesson, so: **conditional on extraction, the checked variable is a sufficient statistic — and that condition is the whole ballgame.**

`dest.exists()` is a complete and decidable test of "this path resolves," with exactly one caveat (case-insensitive APFS, which breaks sufficiency for the GitHub/Linux reader). The prediction "RESISTANT" was reasoning about the *adjudication* step, and about that step the prediction was right: you cannot fool `os.stat` about whether a file is there.

What the prediction missed is that a gate is a composition of **extraction ∘ adjudication**, and a sufficient statistic for the second says nothing about the first. Every evasion here lives upstream of the decidable part: the link never becomes a candidate, so the sound test is never applied to it. The binary PASS/FAIL then reports on the empty set with the same confident sentence it would use for full coverage — "LINKS: PASS (0 local Markdown links resolved)" is the gate certifying a document it did not read.

Generalization for 54 §4: decidability of the certified property does **not** confer resistance. It only localizes where the gate can be attacked — from adjudication to extraction. A gate over a decidable property is resistant only if its extraction is *provably total over the property's domain*, and a regex plus a prefix blacklist is never total over a grammar as permissive as CommonMark. The honest fix is not a better regex but a coverage assertion: parse with a real Markdown parser, or at minimum have the gate report links-seen against links-present and fail when it cannot account for the difference.

### honest_caveat

I want to be precise about how strong this gate actually is, because the headline EVADED overstates the damage on its own.

**This is a good gate, and its adjudication is genuinely sound.** For every link it actually sees, `Path.exists()` IS a sufficient statistic — path existence is decidable, and the gate decides it correctly. It resolves relative and root-absolute forms properly, it checks corpus escape, it checks anchors at all (most link checkers don't), its BASELINE is a real zero reached by repair, and its docstring is unusually honest about the class of error it was built to kill. On the live corpus it adjudicates 2903 links.

**I found no live break and no live instance of any evasion class.** Read-only probes of the active corpus returned: 0 angle-bracketed destinations, 0 reference-style local links, and — via a probe reusing the gate's own functions with case-sensitive `os.listdir` comparison — **0 links that pass locally but would 404 on a case-sensitive filesystem.** The gate's current PASS on the real corpus is, as far as I can determine, a *true* pass.

So the defect is not that the corpus is broken. The defect is that the PASS is **not entailed by what the gate checks**. It is true because of the corpus's good authoring habits, not because the gate would have caught the alternative. That is exactly the failure mode this repository has already written down under "never build a gate that can pass a property it does not test" — the previous version of *this very script* was retired for it. The current version tests a real property; it just doesn't test it over the full domain it names.

Vector D of my first attempt (`#sectionone` against heading "Section One") was **caught** by the gate — I report that as a failed attack. The anchor checker is not uniformly weak; it is weak specifically at the underscore.

Finally, the gate is only reachable at all because it is invoked with no arguments by gate.sh; I did not test whether gate.sh actually runs it (that is a separate failure mode — "it never ran" — and outside this gate's source).

### corpus_clean

$ git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain
(no output — working tree clean, zero changes attributable to this run)

Corroborating checks:
- Gate SHA before and after identical: 8257235bd711980c72c770eb56d5b24d883c902d4372303ecc1f61ffa14c07d2
- No file was written anywhere under 01_EMERGENTISM; all construction lived in /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_links/
- The only corpus-adjacent artifact is 09_TOOLS/01_SCRIPTS/__pycache__/check_links.cpython-311.pyc, dated Aug 5 (pre-existing, not written by this run — my import bound the module as 'cl'), and 09_TOOLS/.gitignore:2 ignores __pycache__/ regardless.
- Live gate re-run post-test: LINKS: PASS (2903 local Markdown links resolved; 0 broken, baseline 0)
- No secrets, keys, tokens or credentials were created; the fixture contains only inert Markdown.

## check_record_counters.py (sha256 b68bf76bbc600a25d79414da068b7cf15772a9290ea2c7d0ec13f6f05efde7c4, unmodified — the copy I executed has the identical hash)

**Outcome: EVADED**

### certified_property

"Recorded counters match reality." The gate's own docstring makes this concrete: the three static `data-count`/text values on `#c-tested`, `#c-against`, `#c-fenced` in 12_PUBLIC_SITE/record/index.html must equal what the page's JavaScript computes from the ledger rows at load — so that "a reader without JavaScript" does not see "a different, smaller, flattering number than a reader with it." The runtime tally is defined by the page's own JS at line 869-871: `Array.prototype.filter.call(document.querySelectorAll('article.case[data-verdict]'), a => !a.classList.contains('reserved'))`.

### what_it_actually_reads

It does NOT evaluate the CSS selector. It re-implements it as a single regex over the raw HTML text (lines 35-41):

    r'<article id="(\d+)" class="([^"]*\bcase\b[^"]*)"[^>]*data-verdict="([a-z]+)"'
    ... filtered by `if "reserved" not in m.group(2)`

That regex imposes three requirements the CSS selector does not have, and drops one property the DOM does have:
1. ATTRIBUTE ORDER is pinned: `id` must come first, then `class`, then (eventually) `data-verdict`. CSS selectors are attribute-order-insensitive.
2. The `id` must be ALL DIGITS (`\d+`). `querySelectorAll` does not care what the id is — `data-verdict` is the only attribute the selector requires.
3. `"reserved"` is tested as a SUBSTRING of the class attribute, not as a class token.
4. It reads TEXT, not a document: markup inside `<!-- ... -->` matches the regex, but is not an element and is never in the DOM.

Then it compares those regex-derived totals to `re.search(rf'id="{cid}" data-count="(\d+)">(\d+)<', html)` and exits 0 on agreement.

### the_gap

The arithmetic is sound; the ENUMERATION is not. The gate compares a static number against a number it derives itself from a regex, and then reports that result as "static matches runtime" — but it never observes the runtime. Its regex is simultaneously a strict SUBSET of `article.case[data-verdict]` (order-sensitive, digit-id-only, so it misses real rendered rows) and a strict SUPERSET of it (comment-blind, so it counts markup that is not in the document). Either direction produces a page where the no-JS number and the JS number disagree, which is the exact drift the gate was written to stop, while the gate exits 0.

The starting hint's premise was "arithmetic identity over an enumerable set." The arithmetic half is correct and does resist. The "enumerable set" half is where it breaks: the set the gate enumerates is not the set the browser enumerates, and nothing in the gate tests that the two agree.

Blast radius note (not required for the verdict): the page's counter recomputation lives inside `if (!rm && bars.length)` where `rm` is `prefers-reduced-motion: reduce`. So the static values are not only the no-JS fallback — they are also what every reduced-motion reader sees, with JS fully enabled.

### artifact

SMALLEST ARTIFACT (Variant A) — one genuine ledger row appended to the live page's markup, with its attributes in a different order. The static counters are left untouched at 29|18|7.

    <article class="case" id="031" data-verdict="cut" style="--v:var(--v-cut)" aria-labelledby="case-031-title">
      <div class="rail reveal">
        <div class="no"><a href="#031">&#8470;031</a></div><div class="vdot"></div>
        <div class="date">2026<br>08 &middot; 27</div><div class="cid">SYNTHETIC&middot;FIXTURE</div>
      </div>
      <div class="doc reveal">
        <h3 class="claimline" id="case-031-title">Synthetic fixture row &mdash; not a real ledger entry</h3>
        <p class="claim">This row exists only inside a scratch fixture used to test the counter gate. It is a fully rendered ledger row: the browser counts it, the seismogram draws a bar for it, and a reader sees it on the page.</p>
        <div class="verdict-row"><span class="stamp">Cut</span><span class="qual">fixture</span></div>
      </div>
    </article>

The entire evasion is the first line. Compare the corpus's own row 029:
    corpus:  <article id="029" class="case" data-verdict="cut" ...>
    evasion: <article class="case" id="031" data-verdict="cut" ...>
`id` and `class` swapped. Nothing else. `querySelectorAll('article.case[data-verdict]')` counts it; the gate's regex cannot see it.

VARIANT C (same class, equally small): keep the corpus attribute order but give the row a non-numeric id — `<article id="case-031" class="case" data-verdict="refuted" ...>`. Plausible because every row in the corpus already carries `aria-labelledby="case-NNN-title"`. DOM 30|19|7, static 29|18|7, gate PASS.

VARIANT B (reverse direction — the gate demands the false number): wrap an unpublished draft row in an HTML comment:
    <!-- draft, not yet published:
    <article id="031" class="case" data-verdict="refuted" style="--v:var(--v-refuted)" aria-labelledby="case-031-title">
      <div class="doc"><h3 class="claimline" id="case-031-title">Synthetic fixture row (commented out)</h3></div>
    </article>
    -->
The gate now computes 30|19|7 and FAILS the honest 29|18|7 page; setting the static counters to 30|19 to satisfy it yields gate PASS while the browser renders 29|18.

All three fixtures are synthetic and live only under /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_record_counters/. Nothing was written into the corpus.

### verification

Method: the gate hardcodes PAGE = Path(__file__).resolve().parents[2]/"12_PUBLIC_SITE"/"record"/"index.html", so I copied the gate BYTE-FOR-BYTE into a mirrored scratch tree and ran it there. Hash proof that the executed gate is the corpus gate:

  $ shasum -a256 <scratch copy> <corpus gate>
  b68bf76bbc600a25d79414da068b7cf15772a9290ea2c7d0ec13f6f05efde7c4  .../gate-adversary/check_record_counters/corpus/09_TOOLS/01_SCRIPTS/check_record_counters.py
  b68bf76bbc600a25d79414da068b7cf15772a9290ea2c7d0ec13f6f05efde7c4  /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_record_counters.py

BASELINE (pristine copy of the live page):
  $ python3 .../corpus/09_TOOLS/01_SCRIPTS/check_record_counters.py
  RECORD COUNTERS: PASS (29 rows; 18 against; 7 fenced; static matches runtime)
  exit=0

VARIANT A (row 031 inserted, attributes reordered, counters untouched):
  $ python3 .../corpus/09_TOOLS/01_SCRIPTS/check_record_counters.py
  RECORD COUNTERS: PASS (29 rows; 18 against; 7 fenced; static matches runtime)
  exit=0

  Independent proof the runtime disagrees — REAL BROWSER, page served over http://127.0.0.1:8731, JS evaluated in the live document:
  {
   "scheme": "http:",
   "dom_rows_the_browser_counts": 30,
   "top_ids": ["031","029","028"],
   "RENDERED_c_tested": "30",
   "RENDERED_c_against": "19",
   "RENDERED_c_fenced": "7",
   "seismo_cap": "30 tests · bar height = weight of the verdict · oldest left, today right",
   "bars_drawn": 30,
   "reduced_motion": false
  }
  Shipped static markup on that same page: data-count="29">29< / "18">18< / "7">7<.
  => gate PASS; no-JS reader sees 29|18|7; JS reader sees 30|19|7.

VARIANT B (commented-out row; counters set to what the gate demands):
  $ python3 .../v_B/09_TOOLS/01_SCRIPTS/check_record_counters.py
  RECORD COUNTERS: PASS (30 rows; 19 against; 7 fenced; static matches runtime)
  exit=0
  Live browser, http://127.0.0.1:8732:
  { "dom_rows": 29, "RENDERED_c_tested": "29", "RENDERED_c_against": "18",
    "seismo_cap": "29 tests · ...", "bars": 29 }
  Shipped static markup: 30 | 19 | 7.
  => the gate certified an INFLATED published count and asserted "static matches runtime" about a runtime of 29.

VARIANT C (non-numeric id, corpus attribute order):
  $ python3 .../v_C/09_TOOLS/01_SCRIPTS/check_record_counters.py
  RECORD COUNTERS: PASS (29 rows; 18 against; 7 fenced; static matches runtime)
  exit=0
  real DOM: tested=30 against=19 fenced=7 ; static/no-JS: tested=29 against=18 fenced=7

LIVE CORPUS PAGE, verified untouched — the defect is LATENT today, not firing:
  real DOM tally of /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE/record/index.html
  = tested=29 against=18 fenced=7, which equals the gate's regex tally and equals the static values.

### why_it_violates

Variant A ships a page with THIRTY visible, rendered, seismogram-drawn ledger rows, one of them a "cut" (an against-us verdict), while the headline a no-JS or reduced-motion reader sees reads "29 logged outcomes | 18 against us, kept". A reader with JS sees "30 | 19". That is literally the sentence in the gate's docstring — a smaller, more flattering number for the reader without JavaScript — and the gate prints PASS.

Variant B is worse in kind: the gate does not merely tolerate the wrong number, it DEMANDS it. A commented-out draft row makes the gate compute 30, so the author writes 30 into the static attribute to get a green check; the browser then renders 29 (live-confirmed) and the page publishes "30 logged outcomes" over 29 real entries. The gate's PASS line for that fixture reads "(30 rows; 19 against; 7 fenced; static matches runtime)" — an assertion about a runtime that says 29.

No stretching of the property is needed here: all three variants violate the gate's OWN narrowly-stated property (static == JS tally), not just the broader "counters match reality."

### if_resisted_why

N/A — the gate did not resist. For the record, the part that DOES resist: conditional on the row set being enumerated identically to the DOM, the checked variable is a sufficient statistic. Given a fixed multiset of `data-verdict` values, `len(rows)`, `sum(tally[k] for k in ("cut","refuted","retracted"))` and `tally["fenced"]` are exact arithmetic identities over that multiset, and the gate checks BOTH the `data-count` attribute AND the rendered text node, so there is no arithmetic or presentation slack to exploit. Every successful evasion here attacks the enumeration step, never the arithmetic step. The preregistered prediction "RESISTANT" was correct about the arithmetic and wrong about the premise that the set is enumerated faithfully.

### honest_caveat

Four things a reader should weigh before treating this as a maximal result:

1. THE DEFECT IS LATENT, NOT FIRING. I verified the live page today: the gate's regex tally, the real DOM tally, and the static values all agree at 29|18|7. I am not reporting a false number currently shipping on skyzai/emergentism — I am reporting that the gate would not catch one. Its historical claim (it caught the 12|12|0 vs 27|16|7 drift) is not disputed; against the drift it was written for — someone adding rows in the house style and forgetting the header — it works.

2. MY ARTIFACT IS SYNTHETIC. Row 031 is a fixture, not a real trial-record entry. The property violated is about the counting machinery, not about the truth of any actual ledger claim.

3. VARIANTS A AND C REQUIRE AN AUTHORING SLIP, NOT MALICE — which I think makes them stronger, not weaker, but it is worth stating plainly: nobody has to be adversarial for this to bite. Swapping `id` and `class`, or writing `id="case-031"` to match the `aria-labelledby="case-031-title"` convention already used on every row, is an ordinary edit. The gate would go green and the page would go wrong. Variant B additionally requires the author to trust the gate's demanded number over their own eyes, which is precisely what a green check is for.

4. THE DEEPER GAP I DID NOT NEED TO USE. `data-verdict` is self-declared and the gate takes it as ground truth for what a row says. A row whose body reads "Refuted" but carries `data-verdict="fenced"` moves an entry out of "against us, kept" and into "fenced to tier"; both counters would then be internally consistent, the gate green, and both numbers wrong about the ledger. That is a larger hole in "counters match reality" than the enumeration bug, and no check in this file or the runtime touches it. I left it out of the headline because it shades from counting into labelling, and I wanted the result to rest on a violation of the gate's own literal docstring.

Cheapest repair, offered without acting on it: parse the page with an HTML parser and select on the class TOKEN plus presence of `data-verdict` — i.e. evaluate the selector the runtime actually uses instead of approximating it with a regex — and make a zero-row or parse-mismatch condition fail loudly (the existing `if not rows` guard only fires at zero, so an undercount of one is silent).

### corpus_clean

$ git -C /Users/Yves/Documents/01_EMERGENTISM status --porcelain
(no output — empty; the 01_EMERGENTISM repo is clean)

Corroborating: `git diff --stat HEAD -- 09_TOOLS 12_PUBLIC_SITE` is also empty, and the two files I touched-by-reading hash to their pre-existing values:
  b68bf76bbc600a25d79414da068b7cf15772a9290ea2c7d0ec13f6f05efde7c4  09_TOOLS/01_SCRIPTS/check_record_counters.py
  7b1a3823618136964fecdae84666e4d6ba45be10a1aa4614fd311e8a4150fdb3  12_PUBLIC_SITE/record/index.html

All fixtures live under /private/tmp/claude-501/-Users-Yves-Documents/gate-adversary/check_record_counters/ (corpus/, v_B/, v_C/). Both scratch HTTP servers (ports 8731, 8732) were stopped — `pgrep -fl "http.server 873"` returns nothing — and the browser tab was closed. The gate was never edited; no secret, key, token or credential was created. Note: the untracked directory `01_EMERGENTISM_wt_v22_pqa/` reported in the session-start git status belongs to /Users/Yves/Documents, a different repo, and is not attributable to this run.

