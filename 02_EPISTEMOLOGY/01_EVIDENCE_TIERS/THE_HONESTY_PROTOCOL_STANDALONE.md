---
rosetta:
  primary_level: L2
  primary_column: Method
  register: "[S]/[A]"
  canonical_phrase: "The Honesty Protocol — a portable method for claiming under uncertainty"
status: "SUBMISSION FORM v2 — 2026-05-31. Paper IV of the Finity Papers (the exportable honesty machine). Referee pass incorporated: 'six fields' miscount corrected to four; '[A] Asserted' renamed '[A] Attested' (the highest tier no longer named after bare assertion); the governing thesis sentence tiered [S/I]; the file-drawer claim's [A]/[S] compound tier held stable across §5 and §7; Rosenthal paginated; the strip-test domain-term leak ('spec-to-proof transit') removed; a non-empty self-applied negative-results register added to §7."
evidence_tier: "[S] as a method; [A] for the third-party empirical regularities it cites"
depends_on: None for USE (stand-alone; no parent framework required). See Provenance note — derivative in ORIGIN.
exportable: true
strip_test: "Contains zero terms specific to any one theory. If a domain term appears, it is a defect."
---

# The Honesty Protocol
## A domain-agnostic method for anyone making claims under uncertainty

> **What this is.** A small, self-contained discipline for keeping your confidence calibrated to your evidence — across a body of work, over time, in public. It is not tied to any theory, field, or worldview. A biologist, an analyst, an auditor, a forecaster, an engineer, or a journalist can adopt it tomorrow.
>
> **What it costs.** One ladder, four fields per claim, three registers, two gates, and a standing rule that you publish your failures. That is the whole method.
>
> **The one sentence `[S/I]`.** *A body of work that corrects itself approaches truth; a body of work that protects itself approaches ideology.* Everything below is machinery for staying on the first side of that line. This governing sentence is itself a load-bearing claim and carries its tier: the correction-vs-protection split is the protocol's organizing wager (`[S]`); the normative direction it names — that one *approaches truth* and the other *approaches ideology* — is an interpretive reading (`[I]`), not a measured result.

This document **applies the protocol to itself.** Every load-bearing rule is tier-marked. The protocol states its own kill criterion (Section 7). The closing section names what would make the protocol itself fail. If a method of honesty cannot survive being pointed at itself, it is not a method — it is a slogan.

> **Provenance (read once, then ignore).** `[S]` This method is *parent-independent in use*: nothing below requires any particular theory, and the strip-test in the frontmatter is the standing check on that. It is *derivative in origin*: it is a distillation of an internal honesty discipline developed inside a larger body of work, stripped of every domain-specific term. Naming that debt is itself an instance of the protocol — you do not get to claim originality you did not earn. The debt does not travel with the method; the method does.

---

## 0. The failure mode it targets

Most dishonesty in serious work is not lying. It is **tier drift**: a claim is born as a guess, gets repeated, picks up confidence with each repetition, and is eventually cited as a fact — without anyone deciding to upgrade it. The drift is silent because nothing in ordinary prose records *how sure you were allowed to be*.

The protocol is designed to arrest drift by attaching, to every load-bearing claim, an explicit and non-self-upgrading record of its evidential standing — and by making the conditions for changing that standing public in advance. It does not *eliminate* dishonesty and it makes no such promise; it makes one specific failure mode visible and expensive.

`[S]` *This diagnosis (tier drift as the dominant failure mode) is a structural claim about how claims decay; it is the protocol's own organizing wager, not an independently measured fact.*

---

## 1. The Evidence-Tier Ladder `[A / B / S / I / D / C]`

Every load-bearing claim carries exactly one tier. The tier answers a single question: **what kind of thing would I have to be wrong about for this claim to be wrong?**

| Tier | Name | What it means | Standard that earns it | Plain-language gloss |
|------|------|---------------|------------------------|----------------------|
| **[A]** | **Attested / measured** | Established fact independent of your work | Third-party measurement, accepted theorem, textbook result, replicated finding you did not produce | "Anyone competent can check this; it does not depend on me." |
| **[B]** | **Built / verified** | Directly verified in *your* system or data | A run you executed, a dataset you receipted, a code path you traced, a document on file | "I checked it myself, and the receipt exists." |
| **[S]** | **Structural** | Follows necessarily *if* you accept stated premises | Valid derivation, logical consequence, model output conditional on assumptions | "Given my assumptions, this must hold — but the assumptions are a choice." |
| **[I]** | **Interpretive** | A bridge from formal result to real-world meaning | Coherence, convergence, analogy; not independently verified | "This is what I think it *means*. It is suggestive, not shown." |
| **[D]** | **Draft / demonstration** | A provisional construction not yet validated | Mock-up, prototype, staged construction, illustrative run | "This shows the shape of the thing; it is not yet load-bearing." |
| **[C]** | **Conjecture** | Speculative, testable, untested | A stated hypothesis with a test you have not yet run | "This might be brilliant or wrong. It earns its place by being testable, not by being true." |

**The cardinal rule: you may never silently upgrade a tier.** A `[C]` may become `[S]` or `[A]` only by meeting its pre-stated upgrade path (Section 3), and the upgrade is *recorded as an event*, with a date and a reason. Downgrades follow the same discipline. Prose may be vivid; it may not move a tier. *When the prose and the tier disagree, the tier governs and the prose is read as invitation.*

**Why six tiers and not two.** "Proven vs. unproven" collapses the three distinctions that actually matter in practice: (1) *yours vs. the world's* evidence (`[B]` vs `[A]`), (2) *conditional vs. unconditional* truth (`[S]` vs `[A]`/`[B]`), and (3) *meaning vs. mechanism* (`[I]` vs `[S]`). `[S]` *Most overclaiming, on this protocol's own wager, lives precisely in those seams — presenting a conditional result as unconditional, or an interpretation as a measurement. That seam-claim is the ladder's organizing bet, not a measured frequency.*

`[S]` *The ladder is a structural device. Its six divisions are defensible and useful, not uniquely necessary; a four-tier or eight-tier variant could serve. Adopt the granularity your domain needs — but never fewer than the three seams above.*

---

## 2. The Three Registers (never blend them in one sentence)

Confidence drifts fastest when modes of speech are mixed. The protocol forces three registers apart:

| Register | Voice | What it does | Standard of evidence |
|----------|-------|-------------|---------------------|
| **The prover** | Quiet confidence | States what follows necessarily from premises | Logical necessity |
| **The interpreter** | Honest speculation | Says what a formal result *means* about the world | Coherence + convergence |
| **The builder** | Conditional commitment | Designs or decides contingent on results not yet in | Empirical validation |

**The transit rule:** a prover-mode claim cannot support a builder-mode decision *without passing through interpreter mode* — and interpreter mode must be labeled as such. "The model proves X, therefore we should do Y" is the single most common laundering of a `[C]`/`[I]` claim into an `[A]` decision. Make the bridge visible or it is doing dishonest work.

`[I]` *The three-register split loosely parallels the ladder — the prover speaks in `[S]` necessity, the interpreter in `[I]` coherence, the builder in `[B]`/`[A]` once its results arrive — but the correspondence is an analogy, not an exact structural mapping (the builder's standard is empirical, so it does not sit at `[C]`/`[D]`). It is a discipline, not a discovery, and the parallel is offered as a memory aid, not a theorem.*

---

## 3. The Mandatory Four Fields (the antifragility rule)

A claim is not load-bearing until a serious reader can answer four questions about it. **If any field is missing, the claim is not forbidden — but it is not yet allowed to carry weight.**

1. **Current tier** — which rung of the ladder is it on, today?
2. **Upgrade path** — what specific, pre-stated evidence would move it *up* a tier?
3. **Kill / downgrade criterion** — what specific, pre-stated observation would move it *down* or retract it?
4. **Survivors** — what remains standing if this claim fails entirely?

The fourth field is the load-bearing one. It severs claims that are wrongly bundled together. **No claim may drag the rest of the body of work down by implication alone**; when something fails, only the claims that *explicitly* depend on it fall with it.

**The subtraction-first rule.** When a claim fails, *shrink it before you reinvent it*. First narrow the claim to what still survives; only then add replacement structure, and only with an explicit downgrade recorded. Reflex elaboration after a failure is how bad ideas grow armor.

`[S]` *The four-field requirement is the operational heart of the method. Its justification is structural: a claim whose failure conditions are unstated cannot be corrected, and a thing that cannot be corrected cannot be honest.*

---

## 4. The Kill-Criterion Mandate (and the active/deferred split)

Every major claim must ship with a **pre-registered kill criterion**: a condition, stated *before* the result is known, whose occurrence retracts or downgrades the claim. Pre-registration is what distinguishes a kill criterion from a post-hoc excuse.

A kill criterion has four parts:

- **The trigger** — the specific observation that fires it (operationalized, not vibes).
- **What dies** — exactly which claim(s) retract or downgrade.
- **What survives** — exactly what is untouched (forces the dependency graph to be honest).
- **Status** — not-yet-tested / testing / **already fired**.

**Active vs. deferred kill criteria.** Separate the criteria you *can* test now from those that require future tools, data, or timescales. Mixing them inflates credibility: an untestable "kill condition" is an aspiration, not a commitment. List both, but never let a deferred criterion pose as a near-term integrity test.

**Honor your own triggers.** The proof that this is a method and not theater is that, when a trigger fires, the claim actually moves. A kill criterion that has fired and been ignored converts the whole protocol into decoration.

`[S]` *Pre-registered, operationalized kill criteria are the published standard for adversarial self-testing. The active/deferred split is the protocol's own structural refinement; its value is that it prevents the file-drawer of untestable commitments from masquerading as rigor.*

---

## 5. The Negative-Results Register (the file-drawer cure)

**The weakest epistemic position any claimant holds is the file-drawer problem:** the world sees the mappings, models, and hypotheses that *worked*, and never sees the ones that were tried and failed. This asymmetry makes any track record look stronger than it is.

The protocol requires a **standing, published register of negative results** — kept with the same status as the positive claims, not in a footnote. For each entry:

- **What was tried** — the candidate claim, mapping, or model.
- **Why it was tried** — the prior reason it seemed promising (this matters; it shows the failure was informative, not careless).
- **Why it failed** — the specific observation or argument that sank it.
- **Verdict** — rejected / downgraded / replaced, with date.

A negative result is **not an embarrassment to bury; it is a load-bearing asset.** It calibrates every surviving claim by showing the denominator. A body of work that publishes only successes is, by construction, miscalibrated — and the reader has no way to know by how much.

**The non-negotiable commitment:** if stronger evidence shows a favored claim is wrong, you publish the failure. This is the line. A claimant who hides negative results is no longer approaching truth.

`[A]/[S]` *The file-drawer / publication-bias problem is an established, third-party, documented bias in the empirical record (Rosenthal, "The file drawer problem and tolerance for null results," Psychological Bulletin 86(3), 1979, pp. 638–641)* `[A]`; *that a standing negative-results register corrects it for an individual body of work is a structural inference, not a measured result* `[S]`. **These two halves keep their separate tiers wherever this claim reappears (cf. §7); the `[A]` half never absorbs the `[S]` half.**

---

## 6. The Irreversibility Gate

Some acts cannot be undone: publishing, shipping, deploying, deleting, committing to an irreversible decision on the strength of a claim. **The protocol requires a gate in front of every irreversible act**, and the gate has one question:

> **Is the tier of the claim I am about to act on irreversibly high enough for the irreversibility of the act?**

Rules of the gate:

- **Reversible acts** (drafts, internal notes, hypotheses) may run on any tier, including `[C]`. Speculate freely where the cost of being wrong is cheap.
- **Irreversible acts** require the supporting claims to be at `[B]` or `[A]` — *verified*, not merely *interpreted* or *conjectured* — unless the irreversibility itself is explicitly consented to as a bet, in writing, by an accountable person.
- **When an irreversible act rests on a lower tier, it must be staged, marked, and signed off by an accountable human** — never auto-approved on the strength of a model output or a conditional result.

The gate is asymmetric on purpose: it is cheap to be wrong in a draft and expensive to be wrong in public, so the burden of evidence rises with the cost of the mistake. The gate does not forbid bold action on thin evidence; it forbids *unmarked* bold action on thin evidence.

`[S]` *The irreversibility gate is a structural device. It does not tell you what to do — it forces the tier of the claim and the cost of the act into the same sentence, where the mismatch (if any) becomes visible before, not after, the act.*

---

## 7. The Protocol Pointed At Itself

A method of honesty must survive its own ladder, or it is a slogan. Here are the protocol's own load-bearing claims, tiered, with the protocol's own kill criterion.

**The protocol's central claims and their tiers**

- `[S]` *The six-tier ladder, three registers, four fields, kill-criterion mandate, negative-results register, and irreversibility gate together constitute a coherent discipline for calibrating confidence to evidence.* — Structural: it follows if you accept that uncorrectable claims cannot be honest. The premise is a choice.
- `[A]/[S]` *The file-drawer / publication-bias problem is real and documented* `[A]` *(Rosenthal 1979, pp. 638–641 — the one genuinely third-party empirical fact the protocol leans on); that a standing negative-results register corrects it for an individual body of work* `[S]` *is the structural inference fenced in §5.* (The compound tier is carried verbatim from §5; the `[A]` half is not allowed to swallow the `[S]` half here.)
- `[C]` *Adopting this protocol measurably reduces overclaiming and improves calibration in a real body of work over time.* — **This is a conjecture, not a demonstrated result.** The protocol has not been run as a controlled trial against a matched body of work that did not use it. It earns its place by being testable, not by being proven.

**The protocol's own kill criterion** (pre-registered, active)

- **Trigger:** A body of work adopts the protocol in full — tiers, four fields, kill criteria, and a published negative-results register — and over a sustained period (say, two years or one major revision cycle) shows *no* improvement in calibration versus a comparable body of work that did not adopt it; OR the protocol is shown to systematically *suppress* true claims (chilling correct boldness) at a rate that outweighs the overclaiming it catches.
- **What dies:** the `[C]` efficacy claim above, and the `[S]` claim that this *particular* arrangement of devices is the right one.
- **What survives:** the `[A]` fact (the file-drawer problem is still real), and the weaker `[S]` claim that *some* explicit tiering discipline is better than none — the kill criterion above tests *this* design, not the existence of any tiering at all.
- **Status:** not-yet-tested. No such controlled comparison has been run. Marking it tested would itself be a tier-drift violation.

**The deferred kill criterion** (honestly labeled as deferred, not a near-term integrity test)

- A long-run study across many independent bodies of work could, in principle, show that disciplines like this one entrench *whatever* tiering a community agrees on — including bad tierings — faster than they correct them. That would downgrade the whole approach. The tools to run it at scale do not currently exist; this is an aspiration, not a commitment, and it is listed here precisely so it cannot masquerade as one.

**This document's own negative-results register** (so §5's rule is not a success-only register that is, by §5's own argument, miscalibrated)

§5 demands a *standing, published* register of what was tried and failed. A protocol document that shipped only its polished claims would be in violation of its own §5. So, kept here with the same status as the positive claims:

- **What was tried:** an earlier draft of this document described the method as one that *"solves"* the file-drawer problem and tier drift. **Why it seemed promising:** the machinery genuinely does target both. **Why it failed:** "solves" is an `[A]`-shaped word for an `[S]`/`[C]` result — the method makes one failure mode visible and expensive, it does not eliminate dishonesty, and §0 now says so explicitly. **Verdict:** downgraded "solves" → "targets / makes visible," 2026-05-31, with the over-claim recorded rather than quietly deleted.
- **What was tried:** naming the top rung *"[A] Asserted / measured."* **Why it seemed promising:** alliteration with the gloss. **Why it failed:** "asserted" is the lowest-warrant speech act and inverts the very ladder it heads — naming the strongest tier after bare assertion licenses exactly the laundering the protocol forbids. **Verdict:** renamed *"[A] Attested / measured,"* 2026-05-31.
- **What was tried:** stating the cost as *"six fields per claim."* **Why it failed:** the protocol mandates **four** fields (§3); the count drifted between the abstract and §3 — precisely the silent-bookkeeping-drift the method exists to catch, caught in the method's own front matter. **Verdict:** corrected to "four fields," 2026-05-31.

The register is not an embarrassment to bury; it is the only thing that lets a reader calibrate the surviving claims above. Its non-emptiness is itself the evidence that §5 was applied to this page and not merely printed on it.

---

## 8. Worked Example (carried at its honest tier)

The example below is deliberately mundane and from no special field, to demonstrate the strip-test: the machinery works without a single domain term. **Every claim in the example carries its own tier, and the example as a whole is offered at `[D]` — it demonstrates the shape of the method; it is not itself evidence that the method works.**

> A forecasting analyst writes: *"Our model shows that customers who open three or more support tickets churn at 4× the base rate; therefore we should auto-escalate any account that hits three tickets."*

Run it through the protocol:

| Step | Finding |
|------|---------|
| **Tier the load-bearing parts** | "Customers with ≥3 tickets churned at 4× base rate, in our data, last quarter" is `[B]` (verified in your own system, receipt = the query). "Three tickets *causes* churn" is `[I]` at best — an interpretation; the tickets may be a *symptom* of an already-leaving customer, not a lever. "Auto-escalation will reduce churn" is `[C]` — a conjecture with a test you have not run. |
| **Apply the transit rule** | The sentence launders a `[B]` correlation and a `[C]` intervention claim into a builder-mode decision ("we should auto-escalate") without passing visibly through the interpreter. The bridge — "we believe the tickets are a lever, not just a flag" — is exactly the `[I]` step that was hidden. Make it visible. |
| **Four fields on the decision** | *Tier:* `[C]`. *Upgrade path:* a controlled A/B test where escalation is randomized. *Kill criterion:* escalated accounts churn at the same rate as matched non-escalated ones. *Survivors:* if the intervention fails, the `[B]` correlation still stands and remains useful as a *flag* for human review. |
| **Irreversibility gate** | Auto-escalation as a *reversible pilot* on a small randomized slice: fine on `[C]`. Auto-escalation hard-wired into the product for all accounts: irreversible-ish, customer-facing — gate says no, not on `[C]`. Stage it, mark it, have an accountable human sign off on the pilot. |
| **Negative-results register** | If the pilot shows no effect, that entry goes in the register, dated, with *why it seemed promising* (the clean 4× correlation) and *why it failed* (correlation was a symptom, not a lever). That entry now calibrates the *next* "X correlates with churn, so intervene on X" proposal. |

**What the example does and does not show.** `[D]` It shows the *shape* of the method on a realistic claim. It does **not** show that the method produces better forecasts — that remains the `[C]` claim of Section 7. The example is an illustration, not evidence; treating it as evidence would be precisely the tier-drift the protocol exists to catch.

---

## The whole method, in one breath

Tier every load-bearing claim on `[A/B/S/I/D/C]` and never upgrade silently. Keep prover, interpreter, and builder apart in any one sentence. Give every load-bearing claim its four fields. Pre-register a kill criterion and honor it when it fires. Keep a published register of what failed. Gate every irreversible act on a tier high enough for its cost. And point all of the above at your own method first — including this document, which carries its efficacy claim at `[C]` and its own kill criterion in Section 7.

*A body of work that corrects itself approaches truth; a body of work that protects itself approaches ideology.* This document tries to stay on the first side of that line by submitting to its own rules. Whether it succeeds is, by its own admission, not yet shown.
