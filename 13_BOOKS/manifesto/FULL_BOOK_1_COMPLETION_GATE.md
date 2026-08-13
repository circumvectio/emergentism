---
title: "Full Book 1 — Completion Gate"
status: "STAGED FIREWALL RECORD — private completion locally passed; not a release approval"
date: 2026-07-31
evidence_tier: "[S] current contract, manuscript, draft, and edition state; [I] completion-test design"
owner: "13_BOOKS projection audit; K-1 through K-7 retain semantic ownership"
source_contract: "FULL_BOOK_1_CONTRACT.json"
boundary_audit: "FULL_BOOK_1_BOUNDARY_AUDIT.md"
scope: "The Emergentist Manifesto: A Worldview for Finite Beings — private Full Book 1"
---

# Full Book 1 — Completion Gate

## Verdict

**PASS for a local private-completion claim; NO-GO for public release.** The
assembled manuscript contains one Preamble, 17 numbered chapters, classified
appendices, 63,681 words, and 638 unique source-mapped units. Its deterministic
build receipt and paragraph ledger are checked by the dedicated Full Book 1
compiler test. The former workbench drafts remain preserved as provenance, but
the reader is assembled from the chapter modules rather than linked to them.
`[S]`

This gate defines when the result may be called a **completed private full
book**. It does not make the book public, prove its claims, validate its
worldview, or authorize any action. `[S/I]`

## Completion predicate

`MANIFESTO-BOOK-1` is complete only when every condition below passes in one
audited revision. A failure in any one condition yields
`staged_full_book_build_not_complete`; it may not be described as merely a
minor editorial remainder. `[I]`

### G1 — One assembled manuscript

1. [`MANIFESTO_BOOK_1.md`](MANIFESTO_BOOK_1.md) is the sole assembled-reader
   manuscript. It contains the Preamble and all numbered chapters inline; it
   may not substitute links to `MANIFESTO_DRAFT_0.md` or `drafts/` for prose.
   `[S/I]`
2. The Preamble is an unnumbered reader door. Exactly 17 numbered chapters
   follow, in this contract order: `[S]`

   | No. | Contract ID | Title |
   |---:|---|---|
   | 1 | `ch01_finite_predicament` | The Finite Predicament |
   | 2 | `ch02_frames_not_furniture` | Frames Are Not Furniture |
   | 3 | `ch03_record_and_possibility` | Probability, Record, and Possibility |
   | 4 | `ch04_soul_loop` | A Loop That Can Learn |
   | 5 | `ch05_finity_card` | The Finity Card |
   | 6 | `ch06_justice_chosen` | Justice Is Chosen |
   | 7 | `ch07_conflict_and_residue` | Conflict, Responsibility, and Residue |
   | 8 | `ch08_social_loop` | The Social Loop and Collective Traces |
   | 9 | `ch09_thin_coordination` | Thin Coordination Across Difference |
   | 10 | `ch10_institutions_can_end` | Institutions That Can End |
   | 11 | `ch11_competition_without_war` | Worldview Competition Without a War Metaphysics |
   | 12 | `ch12_titans_research` | Titans and Finity: A Research Programme |
   | 13 | `ch13_world_contact` | What Translation and World Contact Must Earn |
   | 14 | `ch14_action_and_institution_research` | Accountable Action and Institutional Experiments |
   | 15 | `ch15_lenses_and_immune_protocol` | Six Lenses and the Capture Problem |
   | 16 | `ch16_corrections_kept` | What the Genealogy Keeps and Kills |
   | 17 | `ch17_right_to_leave` | Exit, Record, and the Right to Put It Down |

3. Appendices are present as contractually classified apparatus, not hidden
   additional chapters or a route around lifecycle boundaries. `[S/I]`
4. The assembled reader is within the 60–85k target range, or an explicit
   variance record explains why shorter or longer prose is more honest. Word
   count never licenses padding, a stronger claim, or a release claim. `[S/I]`
5. The contract and manuscript state are changed to an auditable private
   completion state only after G2–G10 pass. `[I]`

### G2 — Paragraph coverage convention

A **substantive unit** is a prose paragraph, block quote, explanatory figure
caption, diagram/table whose cells make propositions, or claim-bearing bullet
list. Headings, a table of contents, navigation, and a purely bibliographic
pointer are non-substantive only if they add no claim. `[I]`

For each substantive unit:

1. Put one unique marker immediately before it:
   `<!-- FULLBOOK-P: <stable_id> -->`. `<stable_id>` uses only lowercase
   letters, digits, `_`, and `-`; no marker may occur twice. `[I]`
2. Place a `Source cards: ` line directly after the unit. The line names every
   card that supports the unit and names no unsupported card. A source marker
   covers content until its own source line or the next marker. An immediately
   following heading is covered only when it labels that same marked unit;
   the generator permits this narrow form only for Claim-Card Atlas and
   Adequacy Docket entries, and rejects it elsewhere. `[I]`
3. Add an entry for every marker to
   `MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json`, whose required path is pinned in
   `FULL_BOOK_1_CONTRACT.json`: `id`, `chapter_id`, `line_range`,
   `claim_card_ids`, derived `source_work_ids`, one inherited source revision
   for each distinct card-set/source tuple, `lifecycle_class`, evidence tiers,
   and `public_disposition`. Research entries additionally record their
   primary card, status, rival, discriminator, narrow-or-kill condition, and
   private disposition. The ledger is the machine authority for coverage; the
   markdown line is the reader-visible receipt. `[S/I]`
4. The ledger must cover 100% of substantive units exactly once. It may not
   use an unlabeled “editorial” exception for substantive theory, advice,
   historical interpretation, or research claim. `[I]`
5. Every card ID resolves uniquely in `00_META/claim_cards/`; source-work IDs
   and SHA-256 revisions must be derived from that registry, not copied as
   independent authority. `[S]`

### G3 — Current-core boundary

The Preamble and Chapters 1–11 and 17 are `current_body`. Each substantive
unit in them uses only `bounded_current` cards and remains no stronger than the
card’s public wording. The book must preserve conditional wording for bounded
conjectural cards, especially the profile, collective-trace, and
causally-plural-conflict claims. `[S/I]`

The current core may not import a candidate, source-only, historical, frozen,
uncarded, or withheld claim simply because a nearby card shares vocabulary.
Finity remains the voluntary `FIN01-01` worksheet; it is not formal Finity,
an authorization, or a demonstrated decision advantage. `[S]`

### G4 — Research-record boundary

Chapters 12–15 are private `research_record` chapters. Every research claim
block must display all five labels adjacent to its reader prose: `[I]`

```text
Research status: [C] candidate / [S] staged protocol / [A] established fragment
Strongest rival:
Discriminator:
Narrow or kill condition:
Public disposition: private_research_record_only
```

The corresponding contract ledger entry must bind the block to its source
cards and must reject a missing rival, discriminator, or narrow/kill field.
Established mathematics may be reported in its declared domain, but it cannot
promote the Titan narrative, a D-system translation, or a Finity protocol to a
new algebra, ontology, or science result. `[S/I]`

### G5 — Historical and custody boundary

Chapter 16 is `historical_provenance`. It may explain the correction record in
the current critical edition and debrief, but it may not copy, modernize, or
make current assertions from the legacy AIA source. Its header identifies the
historical source, revision hash, critical edition, and debrief route. `[S]`

Appendix D is `custody_only` for *The Reciprocal / Infinite Play*. It contains
only work ID, source paths, hashes, frozen lifecycle, preservation reason, and
route. It contains no explanatory paraphrase, quotation, reconstructed
argument, or current claim from `RIP01-*`. `[S/I]`

### G6 — Barred-language firewall

The completed manuscript and its generated material must fail the gate if they
assert any of the following, including through an unqualified chapter title,
table caption, diagram, pull quote, or marketing summary: `[S/I]`

- a complete/total ontology or a universal solution of paradoxes;
- a completed Titan algebra, Titan arithmetic, or a formula that supersedes
  standard mathematics without recovery and independent review;
- science unification, causal power of a symbol, or proof transferred from a
  correspondence;
- objective ethics derived from geometry, a `Φ/V` product, a score, beauty, or
  adherence;
- literal D6/D0 identity, metaphysical rank, caste/hereditary human type, or
  founder/AI authority;
- a collective as a conscious/moral person, a worldview as the universal cause
  of war, an enemy class, existential pressure, or permission for violence;
- a Network State, territorial, sovereign, membership, enforcement, or runtime
  project; or
- health, legal, financial, clinical, or efficacy promises beyond source scope.

The only permitted treatment of barred historical material is a non-substantive
custody entry that names its route and why it is withheld. `[S]`

### G7 — Critical-edition fidelity

Research and historical chapters may draw only from the named carded critical
editions, their associated debriefs, and their source revisions. They must
retain the critical editions’ refusals: no sacred command or physical-force
license (`Dharma`); no enforcement organism (`Evolutionary Network`); no
self-audit safety certificate (`Self-Eating Serpent`); no complete analytic
genome (`Six Lenses`); and no restored rank, recruitment, sovereignty, or
correspondence-as-proof claims (`Sarpasya`). `[S]`

Uncarded Titans modules and every public-withheld route remain unavailable as
content sources. `[S]`

### G8 — Reader-quality and non-duplication checks

The manuscript must show a coherent one-book argument, not concatenate the
started editions. Each chapter has a distinct reader job, a transition from the
prior chapter, and a visible boundary where its source class changes. Repeated
Finity/Justice prose is merged rather than retained as parallel arguments.
`[I]`

The reader ladder remains usable: one sentence, one image, short argument,
ninety-minute current core, full private reader, then auditable record. A
reader can locate the tier, source, rival, correction route, and exit without
accepting membership or doctrine. `[S/I]`

### G9 — Mechanical acceptance tests

Before a private completion declaration, add and pass a Full Book 1 compiler
test that verifies at least: `[I]`

1. exactly one Preamble plus 17 numbered contract chapters, in order;
2. the assembled manuscript contains all chapter IDs and has no drafting
   placeholder or link-only chapter;
3. unique `FULLBOOK-P` markers, one ledger record per marker, and exact line
   coverage of every substantive unit;
4. card ID, owner, source-work, source-SHA, tier, lifecycle, and public
   disposition consistency;
5. only `bounded_current` cards in current-body units;
6. all research labels and rivals/discriminators/narrow-or-kill routes;
7. historical/custody restrictions, including zero regenerated `RIP01-*`
   argument; and
8. all barred-language categories above, including generated indexes.

Then run:

```sh
python3 -m unittest discover -s 09_TOOLS/02_COMPILERS -p 'test_*.py'
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check
python3 09_TOOLS/01_SCRIPTS/check_emergentism_purity.py
python3 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope cards
python3 09_TOOLS/01_SCRIPTS/check_links.py
python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --check
python3 09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py
git diff --check
```

Deterministic generation must produce matching hashes across two clean runs.
Green local gates mean only that the private-book contract is internally
checked; they are not evidence, public release, deployment, or independent
review. `[S/I]`

### G10 — Separate public-release gate

Private full-book completion is not public readiness. A public edition can
contain only its separately cleared current body; it excludes research,
historical, custody, barred, and withheld material. Fresh-reader tier
comprehension, hostile review, semantic parity, predeploy, immutable-artifact
audit, and separate host/alias/DNS verification remain unpaid public gates.
`[S]`

## Resolved local blockers and remaining external gates

| ID | Prior blocking observation | Current disposition |
|---|---|---|
| C1 | The assembled reader was a routing stub with no full-book markers or source receipts. | **Resolved:** `MANIFESTO_BOOK_1.md` is one inline 63,681-word reader with 638 unique receipt markers. |
| C2 | The contract had no machine-readable paragraph coverage. | **Resolved:** `MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json` is deterministic and binds marker, card, owner, tier, source revision, lifecycle, and public disposition. |
| C3 | Twelve chapters were planned and five mapped but undrafted. | **Resolved:** all 17 chapters have an assembled source module and current private build state. |
| C4 | The current-core workbench drafts were unintegrated. | **Resolved:** Parts I–III are assembled from their dedicated modules; earlier workbench drafts are preserved but not read by the assembler. |
| C5 | Research, history, and custody lacked reader prose under their lifecycle boundary. | **Resolved:** Parts IV–V, the card atlas, dockets, and custody note are present and mechanically classified. |
| C6 | No completion compiler test existed. | **Resolved:** `test_manifesto_full_book_assembly.py` checks deterministic assembly, order, range, coverage, research/card routes, historical restraint, custody, and refusals. |
| C7 | The first local audit found traceability gaps: wrapped Preamble receipts, collapsed multi-source Titan revisions, missing per-unit research records, and incomplete historical/custody metadata. | **Resolved:** the assembler now rejects receipt drift, records every distinct card-set/source tuple, attaches and ledgers all five research fields for all 77 Chapter 12–15 units, and tests the Sarpasya/Reciprocal provenance records directly. |
| E1 | Fresh-reader comprehension, independent hostile review, and the controlled Finity comparison are not yet performed. | **Open by design:** do not infer them from local tests, AI agreement, or manuscript completion. |
| E2 | A public edition, immutable deployment artifact, host/alias/DNS verification, and public review are not approved. | **NO-GO:** this remains a private staged manuscript; public release has a separate gate. |

## Gate conclusion

The local completion predicate now passes: its single private manuscript,
paragraph-level evidence record, research apparatus, correction genealogy, and
custody boundary pass together in this revision. That result does not establish
the worldview, supply independent review, or permit publication. The remaining
world-contact and public gates are deliberately left visible. `[S/I]`
