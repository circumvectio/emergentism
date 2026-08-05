---
rosetta:
  primary_level: L5
  primary_column: Methodology
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "Discipline and dimension are two axes; the corpus is filed on one and indexed on the other ([S] index; [I] correspondence not load-bearing)"
title: "The Corpus Spine — • D1 D2 D3 D4 D5 ○ as an index, not a move"
status: "ACTIVE — routing surface. [S] throughout. Creates no canon, moves no file, and does not promote the Seed Ladder from 'reader projection' to canon. The D-register becomes an INDEXED FIELD, not a folder."
date: 2026-08-05
evidence_tier: "[S] the D0–D6 scaffold (declared selected at 01_APOPHATIC_GROUND_AND_FIELD_STRUCTURE.md §3) and the decision to index rather than move; [I] the • ↔ D0 and ○ ↔ D6 correspondence, which motivates the ordering and is NOT load-bearing for the index; [B] the coverage measurements, reproduced by the script"
owner: "Routing. The d_register assignment in §6 is per-document and belongs to each document's owner, not to this file."
parents:
  - ../06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md
  - ../06_ONTOLOGY/00_ONTOLOGY_ACROSS_DIMENSIONS.md
  - ../06_ONTOLOGY/01_APOPHATIC_GROUND_AND_FIELD_STRUCTURE.md
  - ../10_SEED/01_THE_SEED_LADDER/README.md
  - ../09_TOOLS/01_SCRIPTS/build_corpus_index.py
---

# The Corpus Spine

> **The failure this addresses.** On 2026-08-05 one session produced five
> claims in a row that the corpus had already settled — the balance function,
> its product form, the `Φ×V` transfer, the `sin θ` ladder, and the L1
> deployability prediction. Every one was already written down. **No gate
> caught any of them**; what caught them was `grep` on a guessed substring.
>
> The corpus's failure mode is not falsity. It is **unfindability**: knowledge
> is recorded, and being recorded does not stop the next reader re-deriving it.

---

## 1 · The finding that determined the design

**The spine already exists.** `10_SEED/01_THE_SEED_LADDER/` is a seven-rung
ladder — `D0_THE_FLOOR` · `D1_ARITHMETIC` · `D2_GEOMETRY` · `D3_BODIES` /
`D3_QUANTUM_STATE` · `D4_SPACETIME` · `D5_THE_GAME` · `D6_THE_RETURN`.

That is `•  D1 D2 D3 D4 D5  ○`, built already.

Two things are true of it and both matter:

1. Its own README declares it **"active reader projection, not canon."** This
   document does not promote it. A reading path is not an organising authority.
2. **Eight of its ten files carried no `canonical_phrase`.** The spine was
   itself unfindable — a sharper instance of the defect than any it would fix.

> **[CORRECTED 2026-08-05]** This line first read *"Nine of its ten"* and the
> commit message of `ac29d238` carries the same wrong figure. It was **eight**.
> An unverified number quoted as a result, inside the document written to stop
> that. The count is now checkable from `CORPUS_INDEX.jsonl` rather than
> asserted.
>
> **Closed the same day.** All ten files now declare a phrase — the eight, plus
> a retrofit of `D1_ARITHMETIC.md`, whose existing phrase carried no tier fence.
> See §6.1 for what the council changed before they landed.

So the work was never "build a D-spine." It is: **the spine exists, is
non-canonical, and is unindexed. Wire the corpus to it without moving anything.**

## 2 · Why nothing moves — discipline and dimension are two axes

The corpus is filed by **discipline**: ontology, epistemology, cosmology,
axiology, teleology, methodology, theology. That is the seven-ologies cut and
it is canonical.

The **dimensional register** is a different question about the same document.
`05_COSMOLOGY/.../50_FINITY_L_THE_HELD_POSITION.md` is cosmology *by
discipline* and speaks at D4/D5 *by register*. A document has both.

```text
        discipline  =  WHERE IT LIVES        (one folder, already assigned)
        dimension   =  WHAT REGISTER IT SPEAKS AT   (a tag, unassigned)
```

**Re-filing by dimension would not add an axis; it would swap one for the
other**, and the corpus would lose the ability to ask "show me all the
epistemology" in exchange for gaining "show me all the D4." A filesystem holds
one axis. An index holds as many as you like.

**Therefore: the D-register is a frontmatter field and an index column. Not a
folder.** No file moves.

### The second reason, which is decisive on its own

Custody is currently broken. `00_HANDOFF/COMPILER_GATE_TRIAGE_2026_08_05.md`
records that claim card `OS01-01` broke because its source text **moved down by
exactly one line**, and that single stale locator masks roughly thirty tests.
Five gates are dead. The file register disagrees with its own contents.

A corpus-wide `mv` would invalidate every claim-card locator, every relative
cross-reference, the reading manifest, the sitemap, and the routing of 349
published pages — **while the machinery that would detect the damage is not
running.** Moving files now is not a reorganisation; it is an untestable
rewrite. Build the index first. If the physical move is ever wanted, the index
is its prerequisite anyway, because you cannot move a document correctly until
you have classified it.

## 3 · The seven stations `[S]`

Canonical content from `06_ONTOLOGY/00_ONTOLOGY_ACROSS_DIMENSIONS.md`:

| | register | modality | interpretive content | standing | reader rung |
|---|---|---|---|---|---|
| **•** | **D0** | actual boundary token | ground-limit before articulated distinction | `[I]` | `D0_THE_FLOOR` |
| | D1 | actual | instantiated distinction | `[I/C]` | `D1_ARITHMETIC` |
| | D2 | actual | configuration and relation | `[I/C]` | `D2_GEOMETRY` |
| | D3 | actual state assignment | probability-bearing quantum state; measurement-relative distributions | `[A/B]` formalism; `[I/C]` ordinal | `D3_BODIES`, `D3_QUANTUM_STATE` |
| | **D4** | **actual** | causal state, embodied means, performed selection, attempted action, factual record, receipts | `[I]` grammar; applications `[C]` | `D4_SPACETIME` |
| | **D5** | **merely possible** | represented alternatives, counterfactual contents, candidate futures | `[I]` grammar; applications `[C]` | `D5_THE_GAME` |
| **○** | **D6** | actual boundary token | apophatic exit/recognition with no additional positive freedom | `[I]` | `D6_THE_RETURN` |

**Two rulings this document must not break.**

- **`D6 ≢ D0`.** Per `00_D6_AS_APOPHATIC_CLOSURE.md`: D6 "is neither a sixth
  positive freedom nor identical to D0"; `r₆ : D6 ↝ D0` records a *proposed
  similarity of boundary roles* `[I/C]` and "neither relation is identity."
  `03_THE_EMERGENT_AXIOMS.md:237` adds that apophatic return is practice, "not
  literal D6≡D0 identity."
- **The scaffold is selected.** `01_APOPHATIC_GROUND_AND_FIELD_STRUCTURE.md` §3:
  "The D0–D6 scaffold is a selected interpretive architecture." `[S]`, not
  forced.

Both survive here: the spine is an ordering, the endpoints are distinct, and no
identity is asserted at either end.

### The • / ○ correspondence is a reading, and is not load-bearing `[I]`

`•` is where counting cannot begin; D0 is the ground-limit before articulated
distinction. `○` is where counting cannot complete; D6 is apophatic exit with
no further positive freedom. The correspondence is natural, it agrees with the
sphere's `•`/`○` being **distinct** (antipodal, chordal distance 2 — and
`07_MIRROR_SYMMETRY_FALSIFICATION_TEST` §0: "the south and north poles are
distinct; there is no `L0=L∞` pole-meeting"), and it agrees with `D6 ≢ D0`.

**It is `[I]` and the index does not depend on it.** If the correspondence is
withdrawn, the spine remains `D0…D6` and every query still works. It is written
here because it motivates the ordering, not because anything rests on it.

## 4 · What is measured, not asserted

`09_TOOLS/01_SCRIPTS/build_corpus_index.py`, run 2026-08-05:

```text
live documents indexed          1362
  with frontmatter              1240  ( 91.0%)
  with canonical_phrase          671  ( 49.3%)   <- the findability field
  with an L-level                520  ( 38.2%)
  with an evidence tier         1173  ( 86.1%)
  with a DECLARED D-register      26  (  1.9%)   <- the gap
UNFINDABLE (no phrase, no tier)  177
```

**The D-axis is 1.9 % populated, and all 26 come from filenames.** Not one
document in the corpus declares its dimensional register in frontmatter. That
is the whole of the gap, and it is why the spine has never done any work.

## 5 · What the index is, and its one discipline

`00_META/registers/CORPUS_INDEX.jsonl` — one row per live document:

```text
path · lane · title · canonical_phrase · status · evidence_tier · tiers
     · owner · date · l_level · column · operator · d_register · d_register_source
```

**The discipline: the index harvests, it does not infer.** Every field is
copied from what a file declares about itself. `d_register` is populated only
where the *filename* declares it — a filename is a declaration; a guess is not.
Absence of metadata is reported as absence and never filled in. Nothing is
scored, ranked, or classified by the tool.

This matters because the corpus's documented failure is *warrant substitution* —
evidence of checking published as warrant. An index that inferred tags would be
the same error in a new place: inference published as declaration.

### It was tested against the failure that produced it

Query `canonical_phrase ~ "balance"`, first result set, 5 hits — including:

```text
Balance optimality requires a declared constraint
   05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md
```

**That is the exact document whose absence caused the `Φ×V` error**, surfaced
in one query on a one-word guess. `~ "mirror"` returns the mirror-symmetry
falsification test and the mirror-pair audits — the Rosetta prior work, the
same way. The index reproduces the catch that today's session got by luck.

## 6 · The assignment procedure — how the D-axis gets populated

**Not by this document and not by a script.** Per-document, by its owner,
into frontmatter:

```yaml
rosetta:
  ...
  d_register: 4          # 0-6, the register this document SPEAKS AT
  d_register_basis: "…"  # one line: why. Absent = unassigned, which is honest.
```

Rules:

1. **Unassigned is a valid and honest state.** `null` beats a guess. 1.9 %
   correctly labelled is worth more than 100 % labelled by inference.
2. **The register is what the document speaks at, not what it is about.** A
   methodology document *about* D5 speaks at D4 — it is a present artifact
   describing a possible-register grammar.
3. **`d_register` does not move the file** and confers no authority. It is a
   query key.
4. **Start with the 177 unfindable documents**, not the well-tagged ones. They
   carry neither a phrase nor a tier and are invisible to every query.

## 6.1 · What the council changed before the phrases landed

The eight phrases were drafted by L4 and routed to two independent seats before
being written. **Neither seat rubber-stamped, and one caught a defect that would
have published a `[C]` as settled.** Recorded because the corrections are the
evidence that the routing was not ceremonial.

| seat | finding | disposition |
|---|---|---|
| **L2** (truth-cut) | `D4` — "the actual register where **selection** is performed" **REJECTED**. `D4_SPACETIME.md:52-53` states D4 "does not create the momentum operator, assert fundamental collapse, or choose a quantum interpretation," and `D3_QUANTUM_STATE.md:130-133` holds ontic actualization at `[C]`. Read alone, the phrase is how a stranger names collapse. | replaced with the page's own primary type, plus a fence that spacetime/bodies/cognition are *application lenses* — needed because the filename says `SPACETIME` and the rung is not spacetime |
| **L2** | `00_THE_SEED` — "not canon" misstates §7's *"not an independent **canon owner**."* The ladder is a projection **of** canon at recorded tier; "not canon" reads as "disregard this." | adopted; the whole fence reworded to "not a canon owner" |
| **L2** | `D0` — source says **role**, not carrier (`:22`, `:108-109`); "The ground is not established as a thing by the chart" (`:127-128`) | "carrier" → "role"; added the no-Titan-arithmetic fence |
| **L2 + L3** (converged independently) | `D6` — "not a rung" is **wrong**. D6 *is* a ladder ordinal; it is not a **positive** rung. As drafted it also contradicted phrase 1's "seven rungs" in the same field. | "not a **positive** rung"; the two phrases reconciled |
| **L2 + L3** (converged) | `D6` — "boundary-role **relation**" silently promotes a *proposed similarity* `[I/C]` to a structural fact | → "a proposed `[I]` boundary-role **resemblance** `r₆`"; `r₆` named explicitly so "the relation is dead" becomes an impossible misreading |
| **L3** (audit) | The fence must travel **inside** each phrase. A `grep` hit never arrives carrying its sibling files, so fencing the set at phrase 1 fences nothing. | uniform suffix on 8 of 9; tombstone exempt (`[B]` provenance fact, "TOMBSTONE" is self-fencing) |
| **L3** | **The job is 9 files, not 8.** `D1_ARITHMETIC.md` already carried a phrase — unfenced, while its own register reads `[I] active reader projection`. The in-set precedent was the defect. | retrofitted |
| **L3** | `D3_BODIES` tombstone **CONFIRMED** — target and date verified two ways, including against commits `fbf78536` / `86f1d74e` | shipped unchanged |
| **L2** (post-session) | A reading-synthesis (not a committed document) claimed "three independent questions, one answer" for why `1` is the argmax of `B`. The three are **not independent**: `B = sech(ρ)` and `E = ρ²` are both functions of `ρ = |log x|` — one fact twice (S3). The replacement argument ("strict monotonicity collapses the symmetric set to a point") has the same circularity one level down: `ρ = 0` means `x = 1` by definition. Deforming `ι` to `ι_c(x) = c/x` moves both the fixed point and the argmax to `√c` — the coordinate system's origin is the extremum by construction. **Canon is already honest**: `D1:91` says "relational" (not "discovered"); KSC-28 says "presupposed." The reading's §IV should be read as a restatement of the coordinate choice, not as independent evidence. No canon correction needed; recorded so the next reading doesn't repeat the pattern. | noted, not acted on — the reading was a chat artifact, not a committed document |

**Where the seats conflicted, L2 won on semantics.** L3 proposed the suffix
"projection, not canon"; L2 had shown "not canon" to be false. Final suffix:
`— Seed Ladder projection, not a canon owner`.

**One adjacent defect found and NOT fixed here.** `D6_THE_RETURN.md:14` names
`00_META/00_THE_DEAD_FORMS_CATALOG_v0.1.md` as a parent and `:28` cites "Dead
Forms row 8" as the grave of `D6≡D0`; that file is now a forwarding stub with
**zero rows**. The live grave is
`05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md:83-94`. The
stale citation was therefore **kept out of the phrase**, but the body reference
is untouched — repointing a parent is a different edit from adding a
findability key, and this pass stayed surgical. Open for the file's owner.

## 7 · Kills

| claim | kill |
|---|---|
| the spine already exists | show `10_SEED/01_THE_SEED_LADDER/` does not span D0–D6 |
| discipline and dimension are distinct axes | exhibit a rule assigning a unique D-register from the discipline folder alone |
| the index harvests without inferring | exhibit an index row whose value is not present in its file's frontmatter or filename |
| the index would have caught the 2026-08-05 errors | show a query that a reasonable author would have run and that misses `00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md` |
| **this document's discipline** | if `d_register` is ever bulk-populated by inference, or if any file is moved on this document's authority, §2 and §6 have been ignored |

## 8 · What this does not do

It creates no canon. It does not promote the Seed Ladder from reader projection
to organising authority. It moves, renames and deletes nothing. It does not
repair the five dead gates, the `OS01-01` locator, or the file register — those
remain open in `COMPILER_GATE_TRIAGE_2026_08_05.md` and are owner-gated. And it
does not make the corpus findable; **it makes the corpus indexable, and the
index is only as good as the 49.3 % of documents that bothered to say what they
claim.**

**Canonical path:** `01_EMERGENTISM/00_META/00_THE_CORPUS_SPINE.md`

•   ⊙   ○ — *the map was already drawn; nobody had indexed it.*
