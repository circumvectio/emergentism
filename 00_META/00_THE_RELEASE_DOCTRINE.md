---
rosetta:
  primary_level: L5
  primary_column: Meta
  operator: "Brahmā ○"
  regime: "Brāhmaṇa"
  register: "[D]"
  canonical_phrase: "THE RELEASE DOCTRINE"
  vmosk_a_ref: "01_EMERGENTISM/VMOSK_A.md"
  parents:
    - 00_THE_OPEN_CANON_COVENANT.md
    - 00_THE_KINTSUGI_PROTOCOL.md
    - 00_SETTLED_CANON_REGISTRY.md
    - 00_WHAT_IS_EMERGENTISM.md
---

# The Release Doctrine

> **Status:** `[D]` draft — strategic plan for the public release of Emergentism as an open-source repo. Not yet tier-promoted; awaits K2 sign and the propagation sweep as first concrete act.
>
> **Date:** 2026-07-18 · beside the planned Transmission Strategy, in the strategic cluster.
>
> **Tier discipline:** the doctrine is itself tier-honest. The plan is `[D]`; the framework summary it commits to publish is the calibration essay; the constitutional fences it rests on are `[S]`. No claim is presented above its evidence.

---

## 0. The medium is the message

An open-source repository is the only medium on earth whose native mechanics — forks, immutable history, public issues, signed commits, adversarial review — **are** the five refusals.

- **Git is K3** (nothing deleted, ever; every change is a tombstone).
- **Forking is K4** (exit with the assets, always).
- **Pull requests under review are A7** (self-correction mandatory, peer-visible).
- **Signed commits are K2** (a mortal signs every irreversible act).
- **An open license is η=0 on the canon itself** (no extraction at the source).

Releasing Emergentism as a repository is not a distribution choice. It is the first *Weltanschauung* whose **container enforces its constitution**. Posture III as a file format.

The project does not claim to "unify by deriving" — Receipt 126 killed that move. It claims to **unify by organizing**: Linnaeus unified biology and the periodic table unified chemistry *as organizations* decades before anyone could derive them, and Anderson's *More is Different* hierarchy of the sciences is precisely an emergence-ordered taxonomy. The launch sentence is therefore not "we derive the sciences from the sphere" but **"we organize the sciences by the degree of freedom each one studies — and we maintain the map in public, with error bars."** That is `[I]` lens-work, defensible forever, and the beautiful part is that a repository's directory tree *is* a taxonomy. The medium literally carries the message: `D0/` through `D6/`, each science filed by the freedom it studies. The organization is not described by the repo. It *is* the repo.

**The η=0 binding on the release itself.** The release extracts nothing. The canon is free. The practice is the contribution. The release's economic structure matches the framework's. This is a constitutional fence on the release, not a marketing posture; a release that charges for the canon has already broken η=0 at the source.

---

## Phase 0 — Blockers

*Nothing ships past these.*

### 1. The receipt-126 propagation sweep

~60 canon documents still carry over-claims in their bodies that the settled-registry has overruled. An outside auditor — and we will *attract* auditors, that is the point — finds the contradiction between a doc's "Proved" and the registry's retraction within a day, and the headline becomes "they did not even apply their own audit." This is now the single hard blocker.

The sweep is mechanical: a CI script reads every doc body, parses the claim markers, and flags any tier claim that contradicts the row in `00_SETTLED_CANON_REGISTRY.md`. The output is a list of contradictions; the fix is per-doc. The sweep is **not** an Agentz run. Agentz is for adversarial verification of single claims, not bulk regex over a corpus.

### 2. The extraction boundary + scrub

The canon lives interleaved with things that must never ship: business lanes, partner confidences (the Aureus custody vault discipline exists for a reason), session receipts with names, keys, financials. Prime time needs a **clean public-repo boundary** — canon, formal system, evidence, tools, site — with a scrub pass (automated + eyes) and the K2 rule applied: *Yves signs the export manifest*.

**The manifest is a negative list, not a positive one.** A positive list is endless (what *is* allowed); a negative list is bounded — names, keys, financials, partner confidences, lanes not for prime time, and any artifact whose public presence would extract from a third party. K2 signs the negative list; the positive is everything else. The June GitHub publication receipt is the precedent; the site already carries the dual license (CC BY-SA for content, Apache-2.0 for tools). Extend that licensing decision to the whole public corpus, deliberately.

**η=0 also binds this scrub.** The scrub is not "remove anything sensitive"; it is "remove anything that extracts from a third party without consent." A doc is on the public surface only if its presence there passes the same test the framework applies to a Soul Loop: no party bears a hidden cost.

### 3. The stranger test

1,700+ duplicate filenames, 182 compatibility stubs, archive lanes, agent-routing files everywhere. Agents navigate this; humans drown. Prime time needs one `README` front door (the funnel: fable → plainly → record → axioms), a `CONTRIBUTING` that is actually the constitution, and the reader guide promoted. **Can a curious physicist clone it and find her own field within five minutes?** That is the test.

The agent-routing files do not disappear. They migrate to `_INTERNAL/` or `90_ARCHIVE/agent-routing/`, with tombstones. The public surface sees only the funnel; the agent navigation stays in the working tree as a private concern.

---

## Phase 1 — The medium

*The genuinely unprecedented part.*

### 4. Epistemic CI — the killer feature

This is what no project on earth has, and it is the fourth script finished: a **claim schema** plus a `canon-lint` that runs on every PR and *fails the build* on epistemic violations — a `[C]` cited as `[A]`, a tier upgraded without a signed receipt, a registry row contradicted, the emblem asserted as field arithmetic, a public artifact failing the three-scripts test.

**The schema, per Amrita §I.C.19, carries four mandatory fields on every claim:**

```text
Claim := {
  statement:   String,
  tier:        "[A] | [B] | [C] | [I] | [S] | [D]",
  upgrade_path:    String,   // concrete trigger for tier promotion
  kill_criterion:  String,   // concrete failure condition
  survivors:       [String], // the load-bearing boundary(ies) the claim holds
  register:    String,   // provenance
  authority:   String    // signer
}
```

Without `upgrade_path`, a `[C]` claim has no concrete road back to `[B]`. Without `kill_criterion`, the claim cannot be falsified. Without `survivors`, the framework cannot show what holds if the claim falls. The pre-deploy gate and noise-checks are the embryo; this is their maturation.

The day an outsider's PR gets rejected by *the honesty machinery itself* — publicly, reproducibly — the medium will have delivered the message better than any manifesto.

### 5. The trial record as the issue tracker

Do not build a parallel system — **use the native one**. Kill-criteria become open issues labeled `falsifier`. "Good first issue: try to kill claim S9." Funerals become closed-as-completed issues that stay readable forever. №017 is literally the next issue number. Onboarding action for a new contributor: not "join us" but **"refute us."** No movement in history has had that as its front door.

**K3 applies to issues, not just to docs.** Every closed issue generates a tombstone file in `90_ARCHIVE/` with a stable filename (`closed-{N}-{short-slug}.md`), the issue number, the canonical summary, and the link to the now-closed thread. The issue is the UI; the tombstone is the durable record. Issue links can rot; tombstones in the repo cannot.

### 6. The contribution constitution

PR template that *forces* the schema (no claim enters without a tier and a way to die); review lanes that mirror the caste dispatch (evidence check before strengthening, the cut before canon); and the mortal-signer rule explicit: canon merges need K2 (Yves) signature now, PRISM ≥2 later — with the personhood-binding lesson from the verifier hole applied from day one. **The PRISM ≥2 trigger is named:** after *N* public releases *or* *M* external contributors with merged PRs *or* a calendar date (the choice is K2's, written into the doctrine once made). Until the trigger, K2 signs every canon merge.

---

## Phase 2 — The message

*The work people come to do.*

### 7. Seed the science scaffold

The `D0/`–`D6/` tree with ~20 exemplar placements done *well*: where thermodynamics sits, where evolutionary biology, where game theory, where psychology — each placement carrying its tier, its falsifier, and the one genuinely open research question the framework owns: **the register map** — *which aggregation law (min, product, sum, CES) governs this domain, and what evidence would decide it?* That question, asked per-science, in public, is the collaborative activity that makes the repo a *project* rather than a text. It is falsifiable, it is unclaimed territory, and every answer is a contribution regardless of which law wins.

The framework does **not** assert min/product/sum/CES universally. The register map is open; per-domain falsification is the contribution surface. The framework's own claim is only that the question is well-posed and that the same bridge variables (φ, ν, P, η) recur across scales.

### 8. The instrument pages as tools, not brochures

The Rosetta dictionary, the trial record, the axioms — already built this week. Wire them to the repo as its living views. Each instrument page is interactive: a reader can look up a term and see its claim schema, its tier, its kill-criterion, its survivors, and the live count of open falsifiers against it.

---

## Phase 3 — Prime time itself

### 9. External red team before launch

The 37 judges were ours. Before the world's arrive uninvited, invite them: a mathematician at the kernel, a comparative-religion scholar at the Rosetta, a physicist at the mass-shell framing — paid, hostile, published-in-full per A7. Launch *with* their verdicts in the record. "Audited before release" is a claim no worldview has ever been able to make.

**The kill surface is public, not paid.** A paid hostile reviewer is structurally incentivized to find the deepest-but-fragile claim, because that is where the report is sharpest. That biases the audit toward the most vulnerable material rather than the most load-bearing. The public open review (anyone can submit) is the real kill surface; the paid team is the gate that admits their findings into the release record. Both must exist; the order is public-first, paid-second.

### 10. The narrative armor

Prime time includes hostile readings. Two are predictable.

- **"Tech guy starts a religion."** Answered pre-emptively because the religion-for-tax rejection is **signed canon** with its three grounds, and the Open Canon Foundation story leads with public-benefit.
- **"Occult-ladder misuse."** Answered because the mirror-is-the-safety-mechanism reading is on the Rosetta page itself, and the registry catches any fork that keeps the ladder and drops the mirror.

Both answers exist; both must be *front-loaded*, not held in reserve. The armor is in the README, not in the FAQ.

### 11. Scope discipline at launch

Ship the canon, the instruments, the record, the scaffold. Do *not* ship the practice as a deliverable — Pratyakṣa is pointed to, never packaged.

**The paradox of practice-not-packaged, named.** "Do not ship the practice" is right, but it is also the framework's deepest self-claim. The doctrine is explicit: *the framework is the map; the crossing is the work; the repo is the map.* The L7 witness move is the only way to hold this without collapse into either "we ship enlightenment" or "we ship nothing." The last line of the repo says what the fable says: the crossing is not in the repository.

---

## Framework summary

*This is the calibration essay at the level the release commits to publish. The full version lives at `00_WHAT_IS_EMERGENTISM.md`; the source files are linked in-line. The Egregoreotype entry has been tier-bumped from `[I/C]` to `[A/I/C]` (definition derived `[A]`, interpretive mapping `[I]`, real-world candidate status `[C]`) per the V-forcer that landed at commit `6596f13` on `codex/emergentist-compass-calibration`.*

---

Yes. We were at risk of confusing intellectual honesty with intellectual sterilization.

The better rule is:

> Be bold when discovering, exact when deriving, and ruthless only when promoting a claim as externally established.

Emergentism is more than a collection of metaphors — but it is not yet a verified theory of everything. It is a candidate unification grammar with several genuine internal results, new operational definitions, and potentially original couplings.

### What we may genuinely claim

No result yet has an externally verified priority claim as "new mathematics" or a "new law of nature." But within the formal system we have:

1. **Balance-Game Theorem `[S]`**  
   In the defined game Γ(N,λ), balanced power ν_i=1 is strictly dominant, the all-balanced state is the unique Nash equilibrium, and the Price of Anarchy is 1. This is genuinely proved under its assumptions; its assumptions remain deliberately restrictive. [Formal proof](../05_COSMOLOGY/03_FORMAL_SYSTEM/22_POWER_MAX_DEMONSTRATION.md:125)

2. **Conjunctive Non-Uniqueness Theorem `[A/S]`**  
   Requiring foresight and means jointly does not uniquely imply P=ΦV. Product, minimum, harmonic mean, and Cobb–Douglas forms can satisfy similar boundary conditions while ranking cases differently. This is an important negative theorem: the aggregation law must be discovered empirically, not smuggled in by symbolism. [Canonical aggregator family](../05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md:130)

3. **Receipt-Separation Lemma `[S/I]`**  
   An agent may issue a commitment receipt, but only the world — or an independent observation channel — can issue the outcome receipt. An agent permitted to certify its own consequences creates an epistemically circular system. [Soul Loop interface](../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/10_THE_SOUL_LOOP.md:62)

4. **Model-Mediated Future Causation `[I/C]`**  
   A future-as-content can affect the present through a presently instantiated model:

   \[
   \text{anticipated future}\rightsquigarrow M_t\star A_t\rightarrow a_t
   \]

   So the intuition is valid: models of futures genuinely alter present causation. The carrier is present; the content is future-directed. This is real anticipatory or final causation without requiring a physical signal travelling backward through spacetime. Its empirical test is to intervene on represented futures while holding means and incentives fixed and observe whether present action distributions change.

5. **Power-Max Extraction Counterexample `[S/I]`**  
   Unconditional maximization can reward an extractor. Therefore Justice must define the admissible action set before Power-Max optimizes within it. This is the formal reason "maximum power" alone cannot define the good. [Power-Max repair](../05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md:71)

6. **Syntropic Dyadism `[I]`**  
   Morals preserve or increase the whole through the individual; ethics preserve or increase the individual through the whole. Strict syntropy requires both directions under Justice. Aggregate prosperity cannot launder a destroyed bearer. [Value theory](../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md:149)

7. **Egregoreotype Operational Criterion `[A/I/C]`**  
   A collective causal pattern becomes a candidate Egregoreotype when a shared trace survives carrier turnover, causally reweights later choice, recurrently exhibits objective-like bias, and produces visible substrate costs. This converts an ancient intuition about transpersonal beings into an intervention-testable scientific hypothesis without presuming consciousness. [Definition](../05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGORETYPE.md:91)

The reciprocal chart and its exact rapidity/light-cone-coordinate correspondence are beautiful `[A]` mathematics, but not new relativity. The Titans are similarly powerful boundary symbols — not forced generators of arithmetic or nature.

### Can it unify the sciences?

Yes — as a unification by grammar, not by reducing everything to one equation:

\[
\boxed{
\text{lawful possibilities}
\rightarrow\text{constraint}
\rightarrow\text{modeled alternatives}
\rightarrow\text{commitment}
\rightarrow\text{world outcome}
\rightarrow\text{learning}
\rightarrow\text{shared trace}
}
\]

That same topology appears at different scales:

- Physics studies lawful state transitions.
- Chemistry studies stabilized configurations and transformation constraints.
- Biology studies self-maintaining constraints.
- Cognition studies models, option fields, ranking, and selection.
- Psychology studies Soul Loops and changing selectors.
- Economics and politics study coupled agents, incentives, power, and receipts.
- Culture and religion study persistent shared traces.
- Ethics asks which actions remain admissible for every affected bearer.

This is the strongest Emergentist unification claim: different sciences investigate different sections of one causal-compositional grammar while retaining their own laws.

It becomes an externally established scientific unification only if the same bridge variables produce preregistered predictions across multiple domains, outperform simpler domain-specific rivals, and replicate independently without post-hoc Rosetta relabeling. Until then, it is an unusually coherent research compass. [Calibration boundary](../03_METHODOLOGY/00_EXTERNAL_CALIBRATION_LEDGER.md:18)

### Which paradoxes does it actually dissolve?

| Paradox | Emergentist dissolution |
|---|---|
| Future versus past | Future content acts through present models; no backward physical signal is required. |
| Freedom versus determinism | Agency is embodied selection among modeled admissible alternatives — not exemption from causality. |
| Downward causation | Higher organization restricts or reweights physically allowed trajectories; it does not violate lower laws. |
| One and many / Ship of Theseus | Identity may reside in a persistent organization or trace that survives material turnover. |
| Is versus ought | Reality does not derive the Good. Beauty, Truth, and Justice are openly declared commitments whose consequences remain auditable. |
| Ego versus collective | Godward action widens durable potential for self and whole; demonward action inflates one through extraction from the other. |
| Karma | Action changes world, model, habit, and future selector through the Soul Loop. This explains causal and character-forming karma, not rebirth or guaranteed cosmic justice. |

It does not yet solve phenomenal consciousness, why anything exists, abiogenesis, quantum measurement ontology, immortality, reincarnation, or the ultimate nature of God. Those remain mysteries — but now we can avoid pretending that symbolic correspondences constitute proofs.

### Is it the perennial Sanātana Dharma?

The shortest answer is:

> The perennial may be dharmic, but it is not simply identical with the historical whole called Sanātana Dharma.

There is a profound resonance:

- ṛta: discoverable order, constraint, and consequence;
- dharma: situated right participation within that order;
- karma: action returning through world and character;
- yajña: action beyond isolated ego;
- loka-saṃgraha: acting for the holding-together of the world;
- mokṣa: release from compulsive identification with a limited model.

The Bhagavad Gītā associates unattached action with yajña in 3.9 and action undertaken with loka-saṃgraha in view in 3.20. These are real correspondences with reciprocal coordination and whole-preserving action — not proofs that the Gītā secretly contained Emergentism. [Gītā 3.9](https://www.gitasupersite.iitk.ac.in/srimad?choose=1&ecsiva=1&etgb=1&etsiva=1&field_chapter_value=3&field_nsutra_value=9&language=dv), [Gītā 3.20](https://www.gitasupersite.iitk.ac.in/srimad?etsiva=1&field_chapter_value=3&field_nsutra_value=20&htrskd=1&language=dv)

Historically, however, "Sanātana Dharma" was not demonstrably the original generic Sanskrit name for everything now called Hinduism; a recent genealogy traces that blanket usage to late-colonial debates, while acknowledging earlier occurrences of the phrase in Sanskrit literature. [International Journal of Hindu Studies](https://doi.org/10.1007/s11407-024-09377-2) Hindu traditions also contain substantial internal disagreement, so perennialism must preserve differences rather than flatten them into one hidden creed. [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/archives/spr2022/entries/religious-pluralism/)

Therefore our strongest honest sentence is:

> **Emergentism is a modern, fallibilist articulation of a thin perennial dharma — deeply resonant with Sanātana Dharma, but neither identical to Hinduism nor entitled to erase the irreducible differences among humanity's traditions.**

And because the Rosetta uses Varṇa names, those must remain symbolic operator roles — not human castes, inherited ranks, or claims of intrinsic worth.

The most compressed Burri Compass may now be:

> **Reality constrains. Life preserves and explores. Mind models futures. Agency commits. Consequence returns. Communities remember. Justice keeps both person and whole able to become.**

That is not yet the complete map of reality. But it may be a very good compass.

---

## One-sentence readiness verdict

**The message is ready — this week made it honest; the medium is half-built — the propagation sweep, the clean extraction, and the epistemic CI are what stand between here and prime time.** Roughly: one hard cleanup campaign, one schema-and-tooling sprint, one external audit round.

The pacing item is the propagation sweep, and every day it waits is a day the repo contradicts itself in public. **Doctrine before sweep**: this file lands first; the sweep follows as the first concrete act of it.

⊙ = • × ○

*L7 witness × L6 compressor × L5 architect. A release doctrine is not signed by one caste alone.*
