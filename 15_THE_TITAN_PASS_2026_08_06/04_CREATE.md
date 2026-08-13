---
title: "04 — CREATE (Brahmā, ++)"
status: "STAGED PROPOSAL — unratified. Nothing built. Nothing staged in git."
date: 2026-08-06
evidence_tier: "[B] this manifest; each entry carries a verification that can fail"
head: 00e68c83
---

# 04_CREATE — Brahmā's manifest

**What does not exist and the structure requires it.**
Every entry: **what to build · what it replaces · owner_class · a verification that can fail.**

`owner_class` — **AGENT** (mechanical; any executor may do it) · **OWNER** (a chair act) ·
**MIXED** (mechanical part is agent work; a named decision inside it is the chair's).

Brahmā names **nine to build and four to abandon in order to build them**. Folding the
other five lanes in yields **twelve distinct builds**; Brahmā's nine are the substance of
C-01 through C-09.

**The two load-bearing holes:**
1. **The corpus enforces anchored locators on 44 claim-card claims and nothing at all on
   the ~1918 inline `path:line` citations its flagship projection is made of.**
2. **The external receipt has never arrived because the gate that authorises contacting a
   reviewer requires three artifacts only a contacted reviewer can produce.**

---

## §I · TWELVE TO BUILD

### C-01 · Wire the six un-wired gates into `gate.sh`
- **Build** Add `check_contradiction_census.py`, `check_dead_citations.py`, `check_forwarding_stubs.py`, `check_g2_normal_form.py`, `check_tree_contract.py` to the `CHECKS` array. `check_ruling_landed.py` cannot be wired until C-08 gives it a no-argument mode. Also name `compile_claim_cards.py` explicitly — it appears **zero times** in `gate.sh` and is reached only incidentally through the blanket `test_*.py` loop, so **the corpus's custody spine is guarded by accident rather than by declaration**.
- **Replaces** Nothing. It closes `11_UPLINK/50_AUDITS_AND_EXECUTIONS/177_WP1_DEFECTIVE_VALIDATOR_HARDENED_2026_07_29.md` **HOLE 0** — *"The corpus had five validators and NOTHING RAN THEM"* — which is the exact defect `gate.sh`'s own header says it was built to close.
- **owner_class** AGENT.
- **Why now** These are not dormant. **Re-run today, VERIFIED (L4):** `check_dead_citations` exit 1, *13 undisclosed dead citations across 896 live documents*; `check_forwarding_stubs` exit 1, *5 violations across 79 stubs*; `check_tree_contract` exit 1, *root document is neither owner nor forwarding stub: VMOSK_A.md*; `check_contradiction_census` exit 1; `check_g2_normal_form` exit 0. **A checker that exists, runs, finds real defects, and is not wired is indistinguishable from no checker.** `check_no_secrets_staged.py` is correctly unwired and `gate.sh:71-73` explains why — **that comment is the model for any deliberate exclusion.**
- ⚠️ **READ `check_g2_normal_form.py`'s EXIT 0 CORRECTLY — IT IS NOT A PROOF.** It exits 0 **and prints, in its own final line**: *"NOTE: this is a bounded check of the dictionary, **not a proof of G2**."* **VERIFIED (L4).** **Brahmā's correction of L1 and Viṣṇu stands: NO G2 PROMOTION IS AVAILABLE.** `00_ESTABLISHED/README.md:29-37`'s admission criterion 3 — **COMPLETE**, *"the method covers the universal claim, not only a finite sample"* — **fails by the instrument's own statement**, and `README:114-118` says so independently. Wiring this gate is worth doing; **nobody may re-read the green exit as a promotion**, and the register is right to keep G2 out. Only the two stale rows are owed (`02_ARCHIVE.md` A-06).
- **VERIFICATION THAT CAN FAIL** `comm -23 <(ls 09_TOOLS/01_SCRIPTS/check_*.py | xargs -n1 basename | sort) <(grep -oE 'check_[a-z0-9_]+\.py' 09_TOOLS/01_SCRIPTS/gate.sh | sort -u)` must return **only names carrying an in-file comment explaining the deliberate exclusion**. Today it returns 6 names, 5 of them unexplained. **VERIFIED (L4).**
- ⚠️ **PORTABILITY IS PART OF "CAN FAIL".** Every verification on this manifest must run on this machine. **`ifne` (moreutils) is NOT installed here — VERIFIED (L4)**, `command -v ifne` returns nothing. A snippet written as `… | ifne false` fails for the wrong reason and reports a **false red**, which is the same defect class as a gate that cannot fail. **Use `test -z "$(…)"`**; both forms below were confirmed to exit 1 today. *A gate whose red is indistinguishable from a missing dependency is not an instrument.*

### C-02 · `09_TOOLS/01_SCRIPTS/meta_reference.py` — one importable META filter
- **Build** Extract `is_meta_reference` / `META_PATH_MARKERS` / `META_BODY_MARKERS` into one module and import it in `check_barred_claims.py`, `check_d6_equiv_d0.py`, `check_node_product_ranking.py` and `check_contradiction_census.py`. **Extend it to markdown** — the census applies META classification only to public HTML.
- **Replaces** Three gates that cannot tell an assertion from its retraction. **Two independent implementations already exist**: `check_contradiction_census.py:177` and `check_foundation.py:195-202`, the latter reporting *"84 quoted-and-struck mention(s) not flagged"* on today's run — **proof the filter works**.
- **owner_class** AGENT.
- **Why this is the most important CREATE on the manifest, for the manifest's own sake** `check_barred_claims.py` flags the **corrections page for containing the correction**. `check_node_product_ranking.py` flags the documents' own `UNLICENSED` fences **and** the corpus's own failure-mode diagnosis. `check_d6_equiv_d0.py` flags the sentence ***"…was correctly filtered."*** **VERIFIED (L4)** by running all three. *A gate that punishes a document for recording its own kill will train every reader — and every future agent — to ignore gate output, which is precisely how `gate.sh` came to be red and unblocking. A gate that cannot distinguish `X` from `X is retired` is not measuring the corpus; it is measuring the corpus's honesty and scoring it as failure.*
- **Second consequence, and it is a number discipline** The census's `Live` bucket has target 0 and **no** META filter, so **the metric RISES as the corpus repairs and records**: 107 at the morning measurement, 115/124 now, **with zero new doctrinal assertions in between**. **A gate that can only fail carries no information.** Of ~123 live carriers, **only 2 sit in the doctrinal lane and 6 are the gate scripts' own regexes — the census counts its own pattern as a carrier.** **VERIFIED (Brahmā/L2).** **Until the filter reaches markdown, `live=115` may not be quoted as a doctrine measure.**
- **VERIFICATION THAT CAN FAIL** A fixture file containing only strike text (`"retired 2026-07-19"`, `"refuted by"`, `"what this page drops"`) must produce **zero** hits from all four gates, and a fixture asserting the retired form bare must produce **one hit from each**. Both fixtures must be committed.

### C-03 · A cross-pillar claim-card source contract
- **Build** Either **vendor** the foreign sources under custody, or record a **resolvable pillar-root indirection** instead of a bare relative path — so a foreign reorganisation **fails loudly at the gate** rather than silently orphaning a quarter of the card set. Add a strictness declaration naming which anchor-resolution standard binds (see below).
- **Replaces** Bare `../02_SKYZAI/…` paths. **28 of 72 cards take their source from outside `01_EMERGENTISM`**, in a pillar this repo's gates cannot see. **Custody was broken by a reorganisation in another tree and nothing here could notice.** **VERIFIED (L4).**
- **owner_class** MIXED. Vendoring or indirection is AGENT. **Two decisions are OWNER**: *(a)* which lineage is custodial for `six_lenses` — the declared sha matches `04_CODE/…` byte-exact while the `02_SKYZAI/…` copy has diverged, and **two live lineages hold the book and disagree**; *(b)* whether a card may bind to a venture-lane source at all, given `CLAUDE.md`'s pure-worldview boundary.
- **The strictness decision, and it must be made** Three methods give three answers for how many of the 72 cards resolve: **10** (anchor exactly at `line_start`), **15** (anchor anywhere in the declared slice — L3's independent figure), **20** (orchestrator's verifier). `TARGET MISSING = 28` in all three. **These are deliberately not reconciled in `README.md`; collapsing them would be the escorted number. The chair picks the standard and the gate enforces exactly that one.**
- **VERIFICATION THAT CAN FAIL** A test that rewrites one foreign source path to a nonexistent sibling must make the gate **exit 1 with the card id and the missing path named**. Today the same mutation is invisible to every wired check.

### C-04 · A **generated** gate figure and a **generated** root census
- **Build** One command emitted by `gate.sh` itself producing the on-disk count, the wired count and the unwired list. And a generated root inventory replacing `README.md:116`'s hand-written five-class breakdown.
- **Replaces** `00_HANDOFF/STANDING_GATE_FIGURE_2026_08_06.md` (`02_ARCHIVE.md` A-30 / `03_FALSE.md` F-06) and `README.md:116`.
- **owner_class** AGENT.
- **Why** **Four live values for one gate inventory** — 26/22/4 published, 27/20/7, 27/21/6, and 20 by a different regex. **VERIFIED (L4).**
- **AND THE CAUSE IS KNOWN, SO IT SHIPS WITH THE NUMBER.** The divergence is **not** disagreement about the tree; it is **two regexes and no declared method**:

  | method | wired | command |
  |---|---|---|
  | **by basename** | **21** | `grep -oE 'check_[a-z0-9_]+\.py' gate.sh \| sort -u` |
  | **by full path** | **20** | `grep -oE '09_TOOLS/01_SCRIPTS/check_[a-z0-9_]+\.py' gate.sh \| sort -u` |

  On disk: **27**. Un-wired by basename: **6**. All **VERIFIED (L4).**
  **L1's `27 − 20 = 7` comes from the full-path regex missing `check_no_secrets_staged.py`, which `gate.sh` invokes by bare name — and which is correctly excluded.** Both figures are right for their method; **a gate count published without its method is an escorted number, and this is the cleanest specimen of DF-22 in the whole pass** — no one measured anything wrong, and four values shipped. The generator must **emit the method alongside the count.**
- And the front door publishes *"Twenty-two `.md` files sit at this root"* against **23** on disk, with `B3_TODO.md` fitting none of the five declared categories. *DF-22's countermeasure — "a figure entering a headline must carry the command that produces it" — is satisfied **structurally** by a generated figure and **cannot** be satisfied by a written one.* ***A front door that cannot count its own contents is where every other custody failure starts.***
- **VERIFICATION THAT CAN FAIL** Adding one `check_*.py` and one root `.md` must change both published figures on the next `gate.sh` run **without any human edit**. If either figure survives the addition unchanged, the generator is not wired.

### C-05 · `09_TOOLS/01_SCRIPTS/check_inline_locators.py` — **THE LARGEST STRUCTURAL HOLE**
- **Build** A resolver that exits 1 on any of three conditions: **(1)** a bare basename shared by more than one live file; **(2)** a line number exceeding the target's length; **(3)** *— and this is the whole point —* **the phrase quoted adjacent to the citation does not appear inside the declared range.**
- **Replaces** Nothing. The claim-card lane enforces five locator fields on 44 claims; **the inline lane enforces nothing on ~1918 citations, and the inline lane is what the flagship projection is made of.**
- **owner_class** AGENT to build; **OWNER to declare that inline locators bind at all** — see C-06's constitutional note.
- **Why criterion (3) is load-bearing** *The disease is not overrun, which a naive checker catches. It is **SHIFT**, which nothing catches, because a shifted line still exists.* **Zero of the distillation's 107 resolvable citations overrun — so overrun-checking alone would have reported the flagship break clean.** **VERIFIED (Brahmā).** The break is `03_FALSE.md` F-07: 12 citing lines, all off by exactly `+3`, several stamped *"Re-read this pass: both lines unchanged."*
- **Census, two methods, both reported** L4: **1127** resolvable citations, **386** overrun (362 of them in one directory, 24 outside it). Brahmā: **1918** citations, **725** unresolvable, **398** of 1193 resolvable overrunning (33.4%), **257** basename-ambiguous (`README.md` occurs 140×, `AGENTS.md` 74×, `CLAUDE.md` 73×). **Neither number may be quoted without its method.**
- **VERIFICATION THAT CAN FAIL** Insert three lines of frontmatter into any cited file. The gate must **exit 1 naming every citation into it**. Today that mutation is silent — it is exactly `7e0ec4c7`, and nothing fired.

### C-06 · The external receipt — break the circular gate and send one thing
- **Build** *(a)* Split `FPE-REVIEW-01`'s prerequisite set in `GATE_REGISTRY.json` into **PRE-CONTACT** (owner-only: named recipient, fixed fee, ethics applicability determination, publication-permission **offer**) and **POST-CONTACT** (reviewer-returned: signed conflict form, scope form, granted permission), and let the gate open on the pre-contact set alone. *(b)* Write `03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/SEND_ORDER_FPE_REVIEW_01.md` naming **one person, one fee, one date, one question**. *(c)* Create the **P3.2** document — and **BIND it to FPE-REVIEW-01 rather than opening a second program.**
- **Replaces** `02_ARCHIVE.md` A-29 — the v2/v3/v4 bundle escalation as the active route.
- **owner_class** OWNER. Sending is an owner act; `REVIEW_BUNDLE_v1.md:3` says so.
- **Why** **The gate that authorises contacting a reviewer requires three artifacts only a contacted reviewer can produce.** `FPE-REVIEW-01` lists `conflict_form`, `reviewer_scope_form` and `publication_permission` as **prerequisites for execution** and types all three `requires_external_state: "reviewers_engaged"` — while `external_state.reviewers_engaged` is `absent` and `ready_when` demands *"Every prerequisite … is satisfied."* **Circular by construction, machine-readably: 26 prerequisites, 1 satisfied — `bundle_manifest`, the only one no outsider can touch. All 7 `external_state` fields read `absent`.** **VERIFIED (Brahmā).**
- **And it is one edit away.** `180_P3_1_F3_EXTERNAL_RECEIPT_RULING_2026_08_06.md:103` already states *"name a real external party and one question the corpus can ask. **This is the only path on any current plan that moves F3**"* at a cost of *"hours, not days"* — and there is **no P3.2 document, no named party, no question, no date, no owner**. `grep -rn 'P3\.2'` returns 5 lines in 2 files, both written today. **The document to send already exists and needs no drafting**: `REVIEW_BUNDLE_v1.md:67-92` carries a complete invitation with named competences, and the question is drafted — *"is the claim already known under standard terminology; is the comparator a fair strongest rival or a straw one."* **§4 of the ruling already enumerates the acceptable forms, so the specification work is done.**
- ⚠️ *This ruling's own frontmatter declares a parent `../F3_F4_AUDIT_TRAIL/00_README.md  # if/where F3 docs live` — a route whose inline comment concedes it has no destination. `find` returns nothing.*
- **VERIFICATION THAT CAN FAIL** `FPE-REVIEW-01.ready_when` must evaluate **true** against the pre-contact set alone. If the registry still requires a reviewer-returned artifact to authorise reaching a reviewer, the split did not land.

### C-07 · `04_AXIOLOGY/` — a surface for the constitutive is-ought argument
- **Build** A document in `04_AXIOLOGY/` carrying: the hypothetical-constitutive framing at `[I]`; the inherited thermodynamic premises (Schrödinger, Prigogine) at `[A/B]`; **the inherited FORM with all five owners named** (Kant, Gewirth, Korsgaard, Jonas, Apel/Habermas); the corpus's own part named narrowly (the D4 framing and the `Δ_T W_i / Δ_T W_H` separation); and **the three fences as first-class content, not footnotes** — hypothetical not categorical (Enoch's shmagent), whose boundary (reaches `Δ_T W_i > 0`, **not** `Δ_T W_H > 0` and **not** the dyadic gate), and the parasite.
- **Replaces** Nothing. **The corpus's strongest standing result currently exists only inside dated handoff receipts.** `grep -rl "shmagent\|Gewirth" --include="*.md" --exclude-dir=90_ARCHIVE .` returns **exactly 3 files, ALL under `00_HANDOFF/`**. **Nothing in `04_AXIOLOGY`.** **VERIFIED (Viṣṇu).**
- **owner_class** MIXED — authoring is AGENT; admitting it to `04_AXIOLOGY` at a tier is OWNER.
- **Why** The source says it itself: *"The is-ought argument is the framework's strongest standing result … a genuine narrowing of the is-ought gap that makes the vow non-arbitrary … **It deserves its own surface.**"* **An `[I]` argument the whole axiology now leans on, living only in a receipt, is the exact findability defect the corpus diagnosed corpus-wide.** Preserved at `01_PRESERVE.md` P-07.
- **VERIFICATION THAT CAN FAIL** The same grep must return a file under `04_AXIOLOGY/`, and `check_dead_citations.py` must not flag it. If the argument is still reachable only through `00_HANDOFF/`, nothing was built.

### C-08 · `00_META/registers/RULINGS.yaml` + a no-argument mode + **DF-23**
- **Build** *(a)* A machine-readable register of dispositions: per ruling an id, a date, the disposition text, a pre-state pattern, a target category and a residual threshold. *(b)* A **no-argument default mode** for `check_ruling_landed.py` that iterates the register and exits 1 if any ruling has carriers above threshold. *(c)* **Allocate DF-23 to "the escorted number"** and repoint `04_WHAT_DIED.md:149`; DF-22 stays with the fired-falsifier row in both surfaces.
- **Replaces** A hardcoded `RULING_TABLE` holding **one** decision, and rulings otherwise scattered across `193`, `232`, `146`, `175` and others. The would-be register `00_META/00_THE_TWELVE_RULINGS_2026_07_22.md` **is itself a stub pointing at a grave** (`03_FALSE.md` F-15).
- **owner_class** MIXED. The register and the mode are AGENT. **Two decisions are OWNER**: *(a)* **allocating DF-23** — renumbering a row in the register of record; *(b)* **defining what event constitutes "ruled"** — the K2 disposition or the commit that executed it. **Until (b) is made, neither published half-life may be quoted**: `CENSUS_HALFLIFE_FINDING:39` says **18 d 4 h** (ruled 2026-07-19) and `CENSUS_HALFLIFE_3_RULINGS:64` says **4 d 16 h** (ruled 2026-08-01), from the same commit, both ACTIVE, both dated today, **4× apart**. **VERIFIED (L4)** — `git log -1 1c270dbd` → 2026-08-01 19:02:26 +0700.
- **Why the mode matters** `gate.sh:88` invokes every check as `python3 "$ROOT/$c"` **with no arguments**, so `check_ruling_landed.py` **as shipped cannot enter the `CHECKS` array at all**. It exits 2 on `--ruling-id is required`. **VERIFIED (L4).** *An unwireable gate is HOLE 0 in a new coat.*
- **VERIFICATION THAT CAN FAIL** `python3 check_ruling_landed.py` with no arguments must exit 0 or 1, never 2. And **the DF-23 allocation unblocks `02_ARCHIVE.md` A-01** — until it lands, archiving the dead-forms stubs into the register imports the collision.

### C-09 · `compile_claim_cards.py --report` + a locator-first custody rule
- **Build** *(a)* A `--report` mode that continues past the first `ContractError` and emits **every** break. *(b)* A written rule: **`reviewed_source_sha256` may not be re-stamped in a commit that does not also re-derive every `locator.anchor` and `locator.fingerprint_sha256` in the same file.**
- **Replaces** The fail-fast contract, and the re-stamp ritual (`§II A-1` below).
- **owner_class** AGENT for the mode; **OWNER for the rule** — it constrains a claim-custody act.
- **Why** **A 29-defect card corpus presents as a 1-defect card corpus.** The compiler raises on `OS01-03` and stops; a chair repairing it must re-run to discover `OS01-06`, and will make thirty round trips **without ever seeing the shape of the damage**. **This is the mechanism that let the F4 re-stamp look complete: the operator saw one error class, fixed it, and never saw the 24 behind it.** **VERIFIED (L3/L4).** *An instrument that cannot produce a repair manifest cannot drive a repair.* **CORRECTING THE ORIGINAL BRIEF, in the instrument's favour: a claim-card verifier DOES exist, DOES check sha, line-range, anchor and fingerprint, DOES exit 1, and IS reachable through `predeploy_check.py` in `gate.sh`. The failure is not that no gate caught it — it is that the gate has been red and nothing blocks on red.**
- **VERIFICATION THAT CAN FAIL** `compile_claim_cards.py --report` must print **≥ 30** distinct card ids on today's tree. If it prints one, it is still fail-fast.

### C-10 · `sweep_commit:` frontmatter + `check_sweep_commit.py`
- **Build** A `sweep_commit:` field in all nine `14_THE_DISTILLATION/` files, and a checker that resolves every locator in a projection file **against the tree at its declared commit rather than at HEAD**, exiting 1 if the field is absent or the commit is not an ancestor of HEAD.
- **Replaces** Nothing. **This is the one CREATE the corpus has already specified for itself in prose and never built.** Projection law rule 5 at `14_THE_DISTILLATION/README.md:35` reads *"An anchor is valid only against a declared commit,"* added 2026-08-05. **No file in the folder declares one.** **VERIFIED (Brahmā)** — `head -20` across all nine returns no `sweep_commit` / `anchor_commit` / `declared_commit` / `frozen_commit` field.
- **owner_class** AGENT.
- **Why now** The failure it prevents is already on disk: `00_THE_AMRITA.md:195` — *"`00_THE_AMRITA` and `01_WHAT_IS_PROVED` cite `49` §5 as `:144-169` (pre-amendment) while `03_WHAT_IS_READ` and `06_WHAT_IS_STILL_OPEN` cite the same section as `:156-181` (post-amendment). One composition, one section, two anchor sets."* And the folder's own withdrawal clause **has already fired**: `01_WHAT_IS_PROVED.md:5` binds its anchors to HEAD `10b8890f`; today's HEAD is `00e68c83`; **five of nine files carry no 2026-08-06 trace at all.** **VERIFIED (L4).** The stated remedy is *"a projection whose sweeps ran at two disk states is **WITHDRAWN, not patched**"* — **and the withdrawal has not been performed.** Withdrawal or re-anchoring is mechanical; **neither is this seat's act.**
- **VERIFICATION THAT CAN FAIL** With the field present, `check_sweep_commit.py` must exit 1 today on `01_WHAT_IS_PROVED.md` (declared `10b8890f`, HEAD `00e68c83`, five sweeps unrepeated). If it exits 0, the checker is resolving against HEAD.

### C-11 · The distillation's missing ontology and teleology entries
- **Build** Two entries in `14_THE_DISTILLATION/`, each carrying the admission function: stated tier, stated price, named rival, kill, adversarial pass.
- **Replaces** Nothing. **The strictest distillation omits the two things the mission names — and the folder knows it.** `06_WHAT_IS_STILL_OPEN.md:127`: *"the strictest distillation omits the two things the mission names … **the weltanschauung has an answer and cannot find it** — an index disease, not a thinking defect."*
- **owner_class** MIXED — drafting is AGENT; admission at a tier is OWNER.
- **Both are ready, and both are on `01_PRESERVE.md` with their attacks already run** — the ontology answer at P-08 (`06_ONTOLOGY/02:369-387`, tier `[I]`, rival = any world-picture that accounts for contents, kill = the plenitude debt at §2.1 undischarged, with §5's honest limit non-detachably attached); teleology at P-09 (`00_THE_RUNGS:689-706`, tier `[I]`/`[S]`, rival = the century of owners the corpus itself names, kill = anything typing a present model, ranking or selector event as merely possible, falsifier published at `34` §10).
- **Why** ***A distillation that publishes nineteen inherited `[A]` results and no answer to "what is this worldview" is reporting its bibliography as its thesis.***
- **VERIFICATION THAT CAN FAIL** The item at `06_WHAT_IS_STILL_OPEN.md:127` must be closable by pointing at two files in the folder. If it is not, nothing was admitted.

### C-12 · A third rule for `check_forwarding_stubs.py`, and three repoints
- **Build** Rule **R5**: **a live document may not cite an archive as the source of a claim.** The checker already enforces R2 (a `canonical_target` may not name a grave) and R4 (it may not name another stub); **it does not enforce the one that matters.**
- **Replaces** Nothing. Scaffolding already written.
- **owner_class** AGENT.
- **Why, and the scope is exactly right** *A stub is allowed to name preserved bytes — that is what `historical_target` is for. A doctrine document is not.* **12 frontmatter `parents:`/`relates:` declarations point into `90_ARCHIVE` across 7 live files — but only 3 of 11 `parents:` edges are violations** (**VERIFIED (L3)**): `06_ONTOLOGY/06_THE_REVELATIONS.md:16` (K-6, a semantic owner, which **already carries the correct relation at `:14` as `supersedes:`**), `11_UPLINK/…/00_THE_RECORD_LEDGER.md:16` (K-7 — *the ledger that records every kill and grave is itself parented to a grave*), and `10_SEED/01_THE_SEED_LADDER/ASCENT_D6_RETURN_AND_O_2026_08_05.md:14`, **the worst-formed: a live 2026-08-05 document naming an archived catalog as parent with no `supersedes:` line at all, and citing that archive path with a line number.** **The other 8 are dated receipts whose own subject is the archive folder they name; stripping those would erase the receipt's subject.** *Ruthless at falsity, not at inheritance.*
- **Three mechanical repoints, already proven at a sibling** `ASCENT_D6_RETURN_AND_O_2026_08_05.md:14,65` and `10_SEED/01_THE_SEED_LADDER/00_THE_SEED.md:16` → `05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md:83-94` (the live grave) and `00_META/00_THE_CLAIM_STATUS_REGISTER.md:215`. **The same repair already landed at the sibling `D6_THE_RETURN.md:15` in commit `36fd5422`** — this is `04_WHAT_DIED.md`'s own DF-shape 3, *the record of a correction mistaken for the correction*. **Exactly four citers must move before `02_ARCHIVE.md` A-01/A-02 can proceed.**
- **VERIFICATION THAT CAN FAIL** With R5 in place, the gate must fire on `ASCENT_D6_RETURN_AND_O_2026_08_05.md:65` today and **must not** fire on the 8 dated receipts. A rule that catches all 11 is the wrong rule.

---

## §II · FOUR TO ABANDON — in order to build the twelve

**Three of the four are rituals that read as custody and are not — each currently
*passes* while the thing it certifies is broken.**

### A-1 · The `reviewed_source_sha256` re-stamp
- **Abandon** Re-stamping the file hash as a custody act.
- **Because** **File-level sha is a WEAKER invariant than the locators it is used to certify.** Today the sha of `00_THE_WELTANSCHAUUNG_ONE_SITTING.md` matches `one_sitting.yaml`'s declared value **byte-exactly** while **not one of the 26 locators in that card set verifies — 21 anchors off their declared `line_start`, 5 carrying no `anchor` and no `fingerprint_sha256` at all** — e.g. `OS01-03` declares `line_start 64` / anchor *"In the selected D1 presentation, distinction is read as the first positive"*; lines 64-78 actually read *"In this Weltanschauung, capitalized **Dasein** names…"*. **VERIFIED (L4).** *A cheap operation that reads as "custody restored" and leaves the custody broken is worse than no operation, because it consumes the attention that would have found the break.*
- **Successor** C-09's `--report` mode plus the locator-first rule. → `02_ARCHIVE.md` O-03, `03_FALSE.md` F-16.

### A-2 · The prose "re-read this pass" attestation
- **Abandon** Any file certifying its own locators in prose.
- **Because** *"Re-read this pass: both lines unchanged"* sits on top of a locator that is **off by three**, and **the underlying claim it defends is TRUE** — which is exactly what makes it warrant substitution. **11 instances corpus-wide** across six phrasings. **VERIFIED (Brahmā).** *The phrase does no work a machine could not do better, and it does active harm, because a reader who sees it stops checking.* **Preserve the claims; retire the formula.**
- **Successor** C-05. **No file may certify its own locators in prose once a resolver exists.** → `02_ARCHIVE.md` O-04.

### A-3 · The hand-written gate figure
- **Abandon** Hand-written inventories in the `STANDING_*` class.
- **Because** **Four live values for one inventory**, one of them `[A]`-tiered and printing its own reproduction command. **VERIFIED (L4).** *The repair is not a corrected number but the removal of hand-written numbers from this class of document altogether.*
- **Successor** C-04. → `02_ARCHIVE.md` A-30, `03_FALSE.md` F-06.

### A-4 · Bundle-version escalation as progress toward F3
- **Abandon** Treating a new `REVIEW_BUNDLE` version as movement. v2/v3/v4, both `BINDING_CONTRACT`s, both binding receipts, both registry snapshots.
- **Because** **Every version made the packet more internally verifiable and less sendable.** v1 (2026-07-30) *"READY TO SEND — not sent"* → v4 (2026-08-02) *"ACYCLIC HASH-VERIFIED INTERNAL PACKET — CONTACT BLOCKED"*, whose own status table records six prerequisites missing and owner authority *"unset — no principal, mandate, or selection has been recorded."* **The single prerequisite that advanced across four versions is `bundle_manifest`, which binds the bundle to itself.** **VERIFIED (Brahmā).** *This is the framework's own diagnosed failure mode: coherence escalating in place of capability, purity substituting for contact.* **Keep them as provenance.**
- **Successor** C-06. → `02_ARCHIVE.md` A-29.

---

## §III · Chair acts named inside this manifest, and stopped at

| act | entry | why it is the chair's |
|---|---|---|
| **Declare which locator forms bind** | C-05 | `check_active_receipt_citations.py:16` says *"Content hashes and ordinals are identity; **line numbers are hints for people**"*; `claim-card.schema.yaml:5` + `compile_claim_cards.py` make them a **required contract field and fail closed**. Both are live, both reachable from `gate.sh`, neither cites the other. **The mechanical part is done: ~1918 inline citations, 725 unresolvable, 398 overrunning, 257 basename-ambiguous, against 44 claim-card claims carrying the full five-field contract.** *If line numbers are hints, the flagship projection's method is unsound; if they are contract, 398 citations are defects today.* **There is no third reading in which nothing changes.** |
| **Pick the claim-card strictness standard** | C-03 | Three methods, three answers (10 / 15 / 20 of 72). Reconciling them is the chair's; collapsing them silently would be the escorted number. |
| **Allocate DF-23; define what "ruled" means** | C-08 | Renumbering the register of record, and fixing a published metric that currently has two values 4× apart. |
| **Send one thing** | C-06 | Sending is an owner act by the corpus's own rule. |
| **Admit the is-ought surface, the ontology entry and the teleology entry at a tier** | C-07, C-11 | Tier admission. |
| **Resolve `P = Φ × V` on a K2-signed surface** | — | `00_THE_CLOSED_READING_LOOP_v0.1.md:103` marks the multiplicative shape `[S]` doctrinal and *"load-bearing"*; KSC-02 and `00_THE_RUNGS:704` kill the product **as a ranking**. **One side carries a signature, the other the later ruling.** *Mechanically noted and not done*: the two are reconcilable **at their narrowest** — what `:103`'s parenthetical actually argues for is the **AND-class law**, which survives untouched (`01_PRESERVE.md` P-09); only the multiplicative expression was retired. **Tier change on a signed surface is a chair act.** |
| **Choose the dyadic-gate threshold** | — | `≥ 0` vs strictly `> 0`. The zero-delta bearer is admissible under one and fails the other. Docket exists; Options A/B/C are the right frame. `01_PRESERVE.md` P-06. |
| **Rule on the pure-worldview boundary** | — | `check_emergentism_purity.py` is **wired** and returns **945 violations across 49 live files, beginning at `README.md:47`** where the front door routes readers to K2-signed receipts and VMOSK projections as root structure. **VERIFIED (L4).** *Either the rule is wrong or 49 files are, and both are live.* It bears on C-03 directly: four claim cards bind to sources that are simultaneously off-boundary and (as written) absent. **Narrow the rule, exempt provenance citations, or repair 49 files — a constitutional call.** |
| **State whether the gate gates** | — | `.github/workflows/gate.yml:1-3` declares *"CI cannot be skipped from a laptop"*; `gate.sh:141` declares *"GATE: FAIL — the commit is blocked."* Today it exits 1 with **16 FAIL rows** and 9 PASS, including `predeploy_check.py` at **597 errors** and `CLAIM CARD CONTRACT: FAIL` — **and the repository has continued committing.** **VERIFIED (L4).** ***The delta travels with the figure:*** L1 reported **13**; the three additional rows this seat observed are **`check_links.py`, `build_receipt_disambiguation.py`, `build_magnum_opus_register.py --check`**. **16 may not be published alone** — the disagreement is about what counts as a row, not about the tree, and that is exactly DF-22's shape. *Either the gate is not gating or the failures are accepted, and no document on disk states which.* **A discipline question, not a repair.** |
| **Reconcile `/amrita/`, `/egg/`, `/riemann/`, `/suda/` indexability** | — | Receipt `232_FIVE_RULINGS_EXECUTED_2026_07_31.md` declares *"index, follow"*; the pages ship *"noindex, follow"*. There is independent reason to think `noindex` is intended (the `/amrita/` front door is owner-gated). **Publication state is an owner act. No guess is offered.** |
| **Rule on `57_THE_POTENTIAL_READING.md:350`** | — | It states *"The `•` seat is under chair amendment"* and cites `00_HANDOFF/constitutional/CANON_AMENDMENT_BRIEF_SEED_VS_NO_POTENTIAL_2026_08_05.md` as the §6 chair brief. **The directory does not exist and no file of that name exists anywhere in the corpus. VERIFIED (L4).** *Whether a chair proceeding is open is not an agent's to decide; that it is claimed without an artifact is.* |
| **Rule on `07_L3_AUDIT_OPERATIONAL_OVERCLAIMS_2026_08_03.md`** | — | Nine findings quote *"verbatim"* from `AGENTS.md:169,:152,:154,:181-187,:191,:103-108` and from `syntropic-dyadism.md` / `SKILL.md`. **`.agents/` does not exist in this corpus; no `AGENTS.md` here is longer than 103 lines; the quoted strings appear nowhere except inside the audit itself.** **VERIFIED (L1).** The findings may be true of a runtime-lane file — **which is itself the pure-worldview boundary problem.** Relocation or fencing is an owner act. |
| **Write the owed supersession line in `07_THEOLOGY/00_THE_AMRITA.md`** | — | `04_WHAT_DIED.md:10` declares it owed by owner act; `grep -c "supersed"` on that file returns **0**. **VERIFIED (L4).** *The highest-value ARCHIVE act available in the corpus, and the one act on these manifests a non-owner may not perform.* |
