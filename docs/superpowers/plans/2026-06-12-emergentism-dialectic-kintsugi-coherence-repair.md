# Emergentism Dialectic Kintsugi Coherence Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the live Emergentism worldview so ontology, teleology, Power-Max, Syntropic Dyadism, objective morals/ethics, good/evil, and public echoes use one coherent tier-honest grammar.

**Architecture:** Treat `04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md` as the value-theory owner, then patch older summaries and formal/public echoes to match it. Preserve `02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md` as epistemic authority and do not promote framework-objective claims into completed external moral realism.

**Tech Stack:** Markdown doctrine sources, generated static public site under `12_PUBLIC_SITE/`, repository-local Python build/check scripts, `rg`, `git diff --check`.

---

## File Structure

- Modify: `04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md`
  - Owns the canonical morality/ethics arrow definitions and must receive the holobiont/symbiont/worldline formalism.
- Modify: `04_AXIOLOGY/02_VALUE_THEORY/00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md`
  - Owns public-facing good/evil and knowledge-of-good-and-evil compression; align it to the Power-Max boundary test.
- Modify: `04_AXIOLOGY/02_VALUE_THEORY/01_TRANSCENDENTALS.md`
  - New dirty draft already exists; align its Beauty/Truth/Justice bridge with the worldline formalism without promoting external proof.
- Modify: `05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md`
  - Repair the reversed objective morals/objective ethics arrows.
- Modify: `05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md`
  - Convert older ethics/morals compression into the two-layer grammar.
- Modify: `05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md`
  - Convert older ethics/morals compression into the same two-layer grammar.
- Modify: `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md`
  - Add objective dharma as the flow-state reading of balanced `Phi` and `V`.
- Modify: `05_COSMOLOGY/00_THE_BURRISPHERE.md`
  - Anchor the dharma claim in the Burri-sphere balance proof: raw `V` without
    `Phi` collapses usable balance.
- Modify generated public echoes under:
  - `12_PUBLIC_SITE/value/`
  - `12_PUBLIC_SITE/formal/17-efr-ontology-complete/`
  - `12_PUBLIC_SITE/trinity/15-dharma-yuddha/`
  - `12_PUBLIC_SITE/book/`
  - `12_PUBLIC_SITE/reading-manifest.json`
  - `12_PUBLIC_SITE/sitemap.xml`
  - every additional generated `12_PUBLIC_SITE/` file shown by
    `git status --short -- 12_PUBLIC_SITE` after the build commands in Task 7.

## Canonical Target

All touched surfaces must converge on this grammar:

```text
P_node_i = Phi_i * V_i
H = holobiont / coupled field
i = individual symbiont within H

Power-Max:
  max P_node_i -> max Sum(P_node_j) for j in H
  under coupling lambda > 0, long horizon, and eta = 0

morality = H -> i
  The holobiont raises the symbiont's Phi, V, sovereignty, and option cone.

ethics = i -> H
  The symbiont raises the holobiont's Phi, V, truthfulness, resilience, and option cone.

good = both arrows raise coupled worldline potential under eta = 0.
evil = local gain by degrading the field that carries future potential.

objective dharma = flow-state action at L4
  Phi and V are balanced; sight and power move together.
  Raw V without Phi is not higher power; it is force losing foresight.
  On the Burri sphere, usable balance peaks at Phi = V = 1.
```

Tier boundary:

```text
[S] for the conditional Power-Max structure under its accepted premises.
[I] for naming the structure morality, ethics, good, evil, Beauty, Truth, and Justice.
[C] for any claim that this proves external moral realism for agents who reject the framework's premises.
```

## Task 1: Protect Dirty Worktree And Confirm Baseline Contradictions

**Files:**
- Inspect: all target source files listed above
- No edits in this task

- [ ] **Step 1: Confirm repository state**

Run:

```bash
git status --short --branch
```

Expected: branch is `main`; many existing dirty doctrine/public-site files are present. Do not revert them.

- [ ] **Step 2: Confirm current contradiction scan**

Run:

```bash
rg -n "Objective Morals \\(Individual|Objective Ethics \\(Whole|Morality = collective -> individual|Ethics   = individual -> collective|ethics are directional|morals name the local|holobiont|symbiont|worldline" \
  04_AXIOLOGY/02_VALUE_THEORY \
  05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md \
  05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md \
  05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md
```

Expected: `17_EFR_ONTOLOGY_COMPLETE.md` shows reversed labels; the value-theory owner shows target arrows; worldview files show older compression.

- [ ] **Step 3: Confirm spec authority**

Run:

```bash
sed -n '139,216p' docs/superpowers/specs/2026-06-12-emergentism-worldview-consolidation-design.md
sed -n '277,377p' docs/superpowers/specs/2026-06-12-emergentism-worldview-consolidation-design.md
```

Expected: the spec requires Power-Max-bounded Syntropic Dyadism and names the current arrow contradiction.

## Task 2: Promote Holobiont / Symbiont / Worldline Formalism Into Value Theory

**Files:**
- Modify: `04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md`

- [ ] **Step 1: Read the current owner section**

Run:

```bash
sed -n '26,65p' 04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md
sed -n '221,263p' 04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md
```

Expected: the file already owns `Morality = collective -> individual`, `Ethics = individual -> collective`, and the conditional Power-Max corollary.

- [ ] **Step 2: Insert the worldline formalism after the compressed doctrine block**

Add this section immediately after the block ending with `Law      = keep both vectors raising ΔP under η = 0`:

````markdown
In holobiont language:

```text
H = holobiont / coupled field
i = individual symbiont within H
W_i = reachable worldline potential of i
W_H = viable option cone of H

max W_i is attainable only through max W_H
when i is coupled to H, lambda > 0, the horizon is long enough,
and eta = 0 blocks hidden extraction.
```

This does not dissolve the individual into the whole. It states the opposite
discipline: the individual symbiont reaches its own widest viable worldline only
through the holobiont that carries its future option cone, while the holobiont is
moral only if it raises the symbiont without capture.
````

- [ ] **Step 3: Strengthen the Power-Max corollary**

In the `Power Max Lemma: L4 Corollary` section, after the existing conditional block:

```text
if λ > 0 and η = 0:
  max P_i -> max ΣP
  rational self-optimization selects cooperation
```

add:

````markdown
The worldline form is:

```text
max worldline_potential(i)
  is attainable only through
max viable_potential(H)

under:
  i ∈ H
  lambda > 0
  long horizon
  eta = 0
  real coupling, not rhetorical belonging
```

This is the mathematical core of Syntropic Dyadism: the individual maximizes by
raising the field that carries it, and the field maximizes by raising the
individuals who constitute it.
````

- [ ] **Step 4: Run focused source scan**

Run:

```bash
rg -n "H = holobiont|max W_i|worldline_potential|viable_potential|real coupling" 04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md
```

Expected: all newly inserted formal terms appear in the value-theory owner.

- [ ] **Step 5: Commit this source-owner repair**

Run:

```bash
git diff --check -- 04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md
git add 04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md
git commit -m "docs: formalize Syntropic Dyadism worldline value theory"
```

Expected: whitespace check exits 0. Before committing, run `git diff --cached --name-only`; it must list only `04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md`.

## Task 3: Repair Reversed Formal Ontology Arrows

**Files:**
- Modify: `05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md`

- [ ] **Step 1: Read current reversed section**

Run:

```bash
sed -n '288,338p' 05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md
```

Expected: current headings read `Objective Morals (Individual → Whole)` and `Objective Ethics (Whole → Individual)`.

- [ ] **Step 2: Replace section 5.1 with canonical morality**

Replace from `### 5.1 Objective Morals` through its examples with:

````markdown
### 5.1 Objective Morality (Whole -> Individual)

**Moral structures** are those that raise the real potential of the individual
node without capturing it:

```text
Moral(H -> i) = ΔP_node_i > 0 under eta = 0

The holobiont raises the symbiont's coherence, viability, sovereignty,
and option cone.
```

Examples:
- rights and due process that terminate at a sovereign person
- education, health, memory, and access that increase real agency
- Grace Exit: the node can leave with accumulated ΔP
````

- [ ] **Step 3: Replace section 5.2 with canonical ethics**

Replace from `### 5.2 Objective Ethics` through its examples with:

````markdown
### 5.2 Objective Ethics (Individual -> Whole)

**Ethical actions** are those that return real potential into the coupled field
that carries the actor:

```text
Ethical(i -> H) = ΔP_H > 0 under eta = 0

The symbiont raises the holobiont's truthfulness, resilience, coherence,
viability, and option cone.
```

Examples:
- cooperation under the Power-Max conditions
- non-extraction and truthful accounting
- contributions that strengthen shared memory rather than looting it
````

- [ ] **Step 4: Replace unity block**

Replace the first code block under `### 5.3 The Unity of Morals and Ethics` with:

```text
Holobiont raising symbiont under eta = 0
  -> Individual worldline potential can widen (moral vector)

Symbiont raising holobiont under eta = 0
  -> Collective viable potential can widen (ethical vector)

Under Power-Max conditions, max P_node_i -> max ΣP_node.
Under the worldline reading, max W_i is attainable only through max W_H
when coupling is real, lambda > 0, the horizon is long, and eta = 0.
```

- [ ] **Step 5: Update the ASCII summary**

Replace the line:

```text
│                 Ethics = maintain B ≈ 1 for all                     │
```

with:

```text
│      Morality = H -> i; Ethics = i -> H; both under eta = 0          │
```

- [ ] **Step 6: Verify no reversed formal headings remain**

Run:

```bash
rg -n "Objective Morals \\(Individual|Objective Ethics \\(Whole|Individual → Whole|Whole → Individual|Ethics = maintain B" 05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md
```

Expected: no output.

- [ ] **Step 7: Commit formal ontology repair**

Run:

```bash
git diff --check -- 05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md
git add 05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md
git commit -m "docs: align formal ontology moral and ethical arrows"
```

Expected: whitespace check exits 0. Before committing, run `git diff --cached --name-only`; it must list only `05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md`.

## Task 4: Repair Compact Worldview Summaries

**Files:**
- Modify: `05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md`
- Modify: `05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md`

- [ ] **Step 1: Patch compact worldview ethics/morals section**

In `05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md`, replace the compressed form under `### 6. Ethics and Morals` with:

````markdown
In compressed two-layer form:

- **morality** names the `H -> i` vector: the collective or holobiont raises the
  individual's `Φ`, `V`, sovereignty, and option cone without capture.
- **ethics** names the `i -> H` vector: the individual or symbiont raises the
  field's truthfulness, resilience, coherence, viability, and option cone without
  extraction.
- **moral and ethical codes** are local enactments, judgments, customs, and
  disciplines by which finite beings try to realize those two vectors under
  actual conditions.

So codes may differ in form while still being better or worse by the same
directional standard: whether they approach Beauty, Truth, and Justice while
keeping both arrows syntropic under `η = 0`.
````

- [ ] **Step 2: Patch expanded worldview ethics/morals section**

In `05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md`, replace the paragraph and bullets beginning `This is why the framework's objective-ethics language is teleological rather than merely defensive:` with:

````markdown
This is why the framework's objective-ethics language must be disambiguated
rather than flattened:

- **objective morality** names `H -> i`: the holobiont raises the symbiont's real
  potential without capture.
- **objective ethics** names `i -> H`: the symbiont raises the holobiont's real
  potential without extraction.
- **moral and ethical codes** name finite implementation attempts under local
  conditions.

Codes can vary in language and custom while still being better or worse
approximations of the same structural dyad. The test is whether both arrows raise
`P_node` and widen the reachable option cone under `η = 0`. `[I/S]`
````

- [ ] **Step 3: Verify old compression no longer governs target files**

Run:

```bash
rg -n "objective ethics\\*\\* names the direction|morals\\*\\* name the local|objective-ethics language is teleological" \
  05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md \
  05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md
```

Expected: no output.

- [ ] **Step 4: Commit worldview repair**

Run:

```bash
git diff --check -- 05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md 05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md
git add 05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md 05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md
git commit -m "docs: disambiguate worldview morals and ethics"
```

Expected: whitespace check exits 0. Before committing, run `git diff --cached --name-only`; it must list only `05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md` and `05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md`.

## Task 5: Repair Good/Evil And Transcendentals Boundary

**Files:**
- Modify: `04_AXIOLOGY/02_VALUE_THEORY/00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md`
- Modify: `04_AXIOLOGY/02_VALUE_THEORY/01_TRANSCENDENTALS.md`

- [ ] **Step 1: Patch knowledge of good and evil**

In `00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md`, under `### How do we know good and evil?`, ensure the first answer includes this block before the existing question list:

````markdown
By testing the real boundary, not by appealing to a naked command:

```text
Good = both directions raise coupled worldline potential under eta = 0.
Evil = local gain by degrading the field that carries future potential.
```

Knowledge of good and evil is therefore the practical ability to classify a move:
does it raise both the symbiont and the holobiont under real coupling, or does it
convert one into substrate for the other?
````

- [ ] **Step 2: Patch duplicate knowledge section if present**

Run:

```bash
rg -n "### How do we know good and evil\\?" 04_AXIOLOGY/02_VALUE_THEORY/00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md
```

Expected at current baseline: two headings. Add the boundary block under both headings, or replace the second answer with a one-sentence pointer to the first answer using this exact sentence: `The structural test is the same as above: good raises both coupled worldline directions under eta = 0; evil gains locally by degrading the field that carries future potential.`

- [ ] **Step 3: Patch transcendental bridge**

In `01_TRANSCENDENTALS.md`, after the `Why This Is Objective` code block, ensure this paragraph exists:

````markdown
In Syntropic Dyadism, this means Beauty, Truth, and Justice are approached only
when both vectors stay alive: morality (`H -> i`) raises the symbiont, ethics
(`i -> H`) raises the holobiont, and neither vector hides extraction. A local
gain that narrows the coupled option cone is not a higher transcendental move; it
is a counterfeit increase in `P_node`.
````

- [ ] **Step 4: Verify good/evil boundary exists**

Run:

```bash
rg -n "Good = both directions|Evil = local gain|H -> i|i -> H|counterfeit increase" \
  04_AXIOLOGY/02_VALUE_THEORY/00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md \
  04_AXIOLOGY/02_VALUE_THEORY/01_TRANSCENDENTALS.md
```

Expected: target phrases appear in both value files.

- [ ] **Step 5: Commit value-boundary repair**

Run:

```bash
git diff --check -- 04_AXIOLOGY/02_VALUE_THEORY/00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md 04_AXIOLOGY/02_VALUE_THEORY/01_TRANSCENDENTALS.md
git add 04_AXIOLOGY/02_VALUE_THEORY/00_THE_GOOD_THE_EVIL_AND_THE_TRANSCENDENTALS.md 04_AXIOLOGY/02_VALUE_THEORY/01_TRANSCENDENTALS.md
git commit -m "docs: define good and evil as coupled worldline tests"
```

Expected: whitespace check exits 0; commit includes both value files.

## Task 6: Repair Objective Dharma / Flow-State Bridge

**Files:**
- Modify: `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md`
- Modify: `05_COSMOLOGY/00_THE_BURRISPHERE.md`

- [ ] **Step 1: Read current dharma and Burri-sphere anchors**

Run:

```bash
sed -n '17,52p' 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md
sed -n '100,153p' 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md
sed -n '56,60p' 05_COSMOLOGY/00_THE_BURRISPHERE.md
sed -n '132,140p' 05_COSMOLOGY/00_THE_BURRISPHERE.md
```

Expected: Dharma Yuddha already states `flow = L4 = equator`; Burrisphere already states `B = 2/(phi + nu)` and AM-GM equality at `phi = nu = 1`.

- [ ] **Step 2: Add Krishna's army test to Dharma Yuddha**

In `15_DHARMA_YUDDHA.md`, after the paragraph ending `The core of the answer is **game theory.**`, insert:

````markdown
## Krishna's Army Test: V Without Phi

Before the teaching, the allocation itself is a test of the sphere. One side can
choose force: the army, command capacity, external `V`. The other can choose
Krishna as charioteer: guidance, coherence, sight, `Phi`.

In this reading, the test is not anti-power. It asks whether power is coupled to
foresight. Raw `V` without `Phi` is not higher `P_node`; it is force losing the
very coherence that lets force become dharma.

```text
unlimited V with collapsing Phi -> lower usable P_node / lower B
balanced Phi and V at L4      -> objective dharma / flow state
```

Objective dharma is therefore not obedience to a command. It is the flow state
in which capability and coherence are matched, action and awareness merge, and
the actor can deploy power without hidden extraction. `[I/S]`
````

- [ ] **Step 3: Add Burri-sphere dharma corollary**

In `00_THE_BURRISPHERE.md`, after the paragraph beginning `The equator is not morally preferred because a doctrine says so.`, insert:

````markdown
**Dharma corollary.** Raw capability is not the maximum. A node that drives `V`
toward infinity while `Phi` collapses does not become more powerful in the
action register; it becomes less able to see what its power is doing. Under the
Burri-sphere balance identity for the normalized reciprocal pair, usable balance
peaks only when the two faces are matched:

```text
B = 2 / (Phi + V) where Phi * V = 1
maximum B occurs at Phi = V = 1
```

So objective dharma is flow-state action at the equator: enough sight to see the
move, enough power to make it, and enough balance that action can remain
`eta = 0`. The Gita's army/charioteer choice is the mythic compression of this
test: unlimited `V` without `Phi`, or coherent guidance that brings power to
L4. `[I/S]`
````

- [ ] **Step 4: Verify dharma bridge terms**

Run:

```bash
rg -n "Krishna's Army Test|V Without Phi|objective dharma|flow-state action|army/charioteer|maximum B occurs at Phi = V = 1|unlimited V" \
  05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md \
  05_COSMOLOGY/00_THE_BURRISPHERE.md
```

Expected: both source files contain the dharma bridge.

- [ ] **Step 5: Commit dharma bridge**

Run:

```bash
git diff --check -- 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md 05_COSMOLOGY/00_THE_BURRISPHERE.md
git add 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md 05_COSMOLOGY/00_THE_BURRISPHERE.md
git diff --cached --name-only
git commit -m "docs: connect objective dharma to Burri sphere flow"
```

Expected: whitespace check exits 0; staged names are exactly the two source files above.

## Task 7: Regenerate Public Echoes And Verify Site

**Files:**
- Modify generated public pages under `12_PUBLIC_SITE/`

- [ ] **Step 1: Run the public library generator**

Run:

```bash
python3 12_PUBLIC_SITE/generate_public_library.py
```

Expected: generator exits 0. Record the modified generated files with `git status --short -- 12_PUBLIC_SITE`.

- [ ] **Step 2: Rebuild book/RAG outputs if generator did not do it**

Run:

```bash
python3 12_PUBLIC_SITE/build_book.py
python3 12_PUBLIC_SITE/build_rag_index.py
```

Expected: both commands exit 0. If `generate_public_library.py` already runs these internally, rerunning is acceptable and should be idempotent.

- [ ] **Step 3: Run full public-site gate**

Run:

```bash
python3 12_PUBLIC_SITE/predeploy_check.py
```

Expected: `PASS: all checks green`.

- [ ] **Step 4: Run targeted anti-contradiction scan across source and public echoes**

Run:

```bash
rg -n "Objective Morals \\(Individual|Objective Ethics \\(Whole|Individual → Whole|Whole → Individual|Ethics = maintain B|objective ethics\\*\\* names the direction|morals\\*\\* name the local" \
  04_AXIOLOGY/02_VALUE_THEORY \
  05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md \
  05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md \
  05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md \
  12_PUBLIC_SITE
```

Expected: no output.

- [ ] **Step 5: Run target-positive scan across source and public echoes**

Run:

```bash
rg -n "morality = H -> i|ethics = i -> H|holobiont -> symbiont|symbiont -> holobiont|max worldline_potential|Good = both directions|Evil = local gain|objective dharma|flow-state action|army/charioteer|maximum B occurs at Phi = V = 1" \
  04_AXIOLOGY/02_VALUE_THEORY \
  05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md \
  05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md \
  05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md \
  05_COSMOLOGY/00_THE_BURRISPHERE.md \
  05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md \
  12_PUBLIC_SITE
```

Expected: source and generated public echoes both contain the new canonical terms.

- [ ] **Step 6: Commit generated echoes**

Run:

```bash
git diff --check -- 12_PUBLIC_SITE
git add 12_PUBLIC_SITE
git commit -m "docs: regenerate Emergentism public coherence echoes"
```

Expected: whitespace check exits 0; commit includes generated public-site changes only.

## Task 8: Final Completion Audit

**Files:**
- Inspect: all modified source and generated files
- No source edits unless verification exposes a gap

- [ ] **Step 1: Re-run source contradiction scan**

Run:

```bash
rg -n "Objective Morals \\(Individual|Objective Ethics \\(Whole|Individual → Whole|Whole → Individual|Ethics = maintain B|objective ethics\\*\\* names the direction|morals\\*\\* name the local|completed external proof of moral realism|literal divinization|Dasein is Being" \
  01_TELEOLOGY 02_EPISTEMOLOGY 04_AXIOLOGY 05_COSMOLOGY 06_ONTOLOGY 07_THEOLOGY 12_PUBLIC_SITE
```

Expected: no output for reversed arrows or forbidden upgrades. Boundary phrases such as `completed external proof of moral realism` may appear only inside explicit denials; inspect any hits before accepting.

- [ ] **Step 2: Re-run source-positive scan**

Run:

```bash
rg -n "Power-Max|Syntropic Dyadism|morality = H -> i|ethics = i -> H|H = holobiont|max W_i|max worldline_potential|Good = both directions|Evil = local gain|objective dharma|flow-state action|army/charioteer|maximum B occurs at Phi = V = 1" \
  04_AXIOLOGY/02_VALUE_THEORY \
  05_COSMOLOGY/00_THE_WELTANSCHAUUNG.md \
  05_COSMOLOGY/00_EMERGENTISM_AS_WELTANSCHAUUNG.md \
  05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/15_DHARMA_YUDDHA.md \
  05_COSMOLOGY/00_THE_BURRISPHERE.md \
  05_COSMOLOGY/03_FORMAL_SYSTEM/17_EFR_ONTOLOGY_COMPLETE.md \
  12_PUBLIC_SITE
```

Expected: all target owner and public surfaces show the repaired grammar.

- [ ] **Step 3: Run full mechanical checks**

Run:

```bash
git diff --check
python3 12_PUBLIC_SITE/predeploy_check.py
```

Expected: `git diff --check` exits 0; predeploy check ends with `PASS: all checks green`.

- [ ] **Step 4: Inspect final dirty/staged state**

Run:

```bash
git status --short --branch
git log --oneline -6
```

Expected: new repair commits are present. Remaining dirty files, if any, must be either unrelated pre-existing work or generated outputs that have a clear reason not to commit.

- [ ] **Step 5: Report completion with evidence**

Report:

```text
- commits created
- files intentionally modified
- scans/checks run with exit status and key output
- remaining dirty files, if any, and whether they pre-existed
- any unresolved coherence risk
```

Do not mark the active goal complete unless every scan and current-state inspection proves the requested coherence repair is complete across source and public echoes.
