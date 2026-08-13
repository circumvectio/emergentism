---
title: "00_THE_LAW — the constitution of the emitted tree"
status: "STAGED — unratified. A constitution proposes; it ratifies nothing. Nothing moved, deleted, committed, or staged in git."
date: 2026-08-06
evidence_tier: "[B] every figure below was produced by a command run this pass and the command is printed beside it; [A] the arithmetic of the shear; [I] the framing"
owner: "No owner. Every rule names the document it inherits from. This file may never be cited as authority for a claim."
seat: "Witness."
head: 00e68c83
spine_law: "path + exact quoted string. No line numbers. Anywhere."
frozen_tree: "01_EMERGENTISM is provenance and graveyard. Cited, never touched."
---

# 00_THE_LAW

There is one design law. Everything else in this file is either evidence for it,
inherited from a named document, or a prohibition that follows from it.

---

## I · THE ONE DESIGN LAW

> **NO path-plus-line-number CITATIONS. EVER.**
> **QUOTE-ANCHORED ONLY: a path, plus the exact string.**

A quoted anchor survives insertion, reflow, frontmatter, reordering and reformatting.
A line number survives none of them. This is not a preference. It is the difference
between a citation that keeps pointing at what it cited and a citation that silently
starts pointing at something else while continuing to look correct.

**The corpus wrote this rule for itself, five times, in five files, and did not apply
it to itself.** The rule appears in the distillation in five phrasings — for example
`14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md`:

> "cite it by path plus quoted string, never by a bare line range"

Each of the five was written **in the act of repairing a citation that had already
resolved wrong**. The rule is not theory. It is scar tissue. It was still not enforced
by anything.

---

## II · THE EVIDENCE

### 1 · Three lines of frontmatter

```
$ git show --stat 7e0ec4c7
```

Commit `7e0ec4c7`, 2026-08-05 23:09:16 +0700, "feat(meta): WO-A1 batch 3 — final 11
canonical_phrases; UNFINDABLE COUNT = 0". **66 files changed, 205 insertions, 86
deletions.**

```
$ git show 7e0ec4c7 -- 00_ESTABLISHED/README.md
```

Against the corpus's own truth folder it added **three lines and nothing else** — a
`rosetta:` block carrying a register and a basis. No sentence was changed. No claim was
touched. No fact was altered. **The document is, in content, identical.**

### 2 · What those three lines did

```
$ git show 7e0ec4c7^:00_ESTABLISHED/README.md | awk 'NR==100'
$ awk 'NR==100' 00_ESTABLISHED/README.md
```

Before: the row asserting `G2` as an open general claim.
After: the table header `| id | claim | kill |`.

**A citation aimed at a mathematical claim now returns a table header.** It does not
error. It does not warn. It returns a plausible-looking line, in the right file, in the
right table, and it is the wrong line.

Every locator into that file moved by exactly the same amount. Verified individually,
before and after, by `awk` at each number:

| what was cited | was at line | is now at line | delta |
|---|---|---|---|
| the `G2` open-claim row | 100 | 103 | +3 |
| "remains open until a complete proof or formalization lands" | 114 | 117 | +3 |
| the `Z1` row | 121 | 124 | +3 |
| the μ-contract line | 131 | 134 | +3 |
| "What is NOT here, and this list is the point" (range start) | 126 | 129 | +3 |
| the block quote (range) | 140–142 | 143–145 | +3 |

### 3 · The eleven, and the twelfth

```
$ grep -rn '00_ESTABLISHED/README.md:[0-9]' 14_THE_DISTILLATION/
```

**Eleven citing lines inside the distillation** — the corpus's flagship projection —
across five files: the folder README, the amrita, what-is-proved, what-died, and
what-is-still-open. Corpus-wide the count is **twelve lines in six files**; the twelfth
is in the session audit under `00_HANDOFF/`. Those twelve lines carry **seventeen
locator instances** over **six distinct target lines**. Every one of the seventeen is
off by three.

**The timing is the finding.** The distillation's citations were written at 19:44:57
and refreshed at 21:01:04 on 2026-08-05 (`git log --date=iso -- 14_THE_DISTILLATION/`).
The commit landed at 23:09:16. **They were correct when written and shattered two hours
and eight minutes later, by a commit that changed no claim in either file.** Four
further commits touched the distillation afterwards. None of them noticed.

### 4 · "Re-read this pass"

One of the eleven carries an attestation. `14_THE_DISTILLATION/00_THE_AMRITA.md`:

> "Re-read this pass: both lines unchanged."

The string resolves exactly once in that file. **Both cited lines had changed.** The
underlying claim it was defending — that the register was stale on `G2` — was and is
**true**.

That is the shape the corpus itself named its worst defect: **evidence-of-checking
published as warrant.** A true claim, escorted by a false attestation, on top of a
broken locator. The attestation did no work a machine could not have done better, and
it did active harm, because a reader who sees "re-read this pass" stops checking.

The prior pass reached the same verdict independently —
`15_THE_TITAN_PASS_2026_08_06/03_FALSE.md`, under "THE FLAGSHIP CUSTODY BREAK":

> "What is FALSE is the locator string, not the claim."

**Retire the formula. Keep the claims.** No document in this tree may carry a
first-person attestation that a check was performed. It carries the command, or it
carries nothing.

### 5 · The census — and why one number would be a lie

The brief that produced this file gave a single figure: 386 of 1127 citations
overrunning. **I ran my own census and got a different number. So did two seats before
me. Here are all three, with methods, because the corpus's own ruling on this exact
question — `15_THE_TITAN_PASS_2026_08_06/04_CREATE.md` — is "Neither number may be
quoted without its method."**

| census | resolvable | overrun | rate | resolution policy |
|---|---|---|---|---|
| L4, prior pass | 1127 | 386 | 34.3% | not stated in full |
| Brahmā, prior pass | 1193 | 398 | 33.4% | 1918 tokens, 725 unresolvable |
| **this pass, strict** | **1323** | **413** | **31.2%** | path must resolve from root or relative to the citing file |
| **this pass, permissive** | **1735** | **416** | **24.0%** | strict, plus a **unique** basename match anywhere in the live tree |

```
# this pass, live tree, 90_ARCHIVE and .git excluded
path:line tokens found        2156
whole tree incl. 90_ARCHIVE   2830 tokens, 2138 resolvable, 532 overrun (24.9%)
```

**Four measurements, four numbers, one conclusion:** between a quarter and a third of
every resolvable line citation in this corpus already points past the end of the file
it names. The disagreement between the four is entirely a disagreement about what
counts as resolvable. That the number moves by 300 depending on a resolution policy is
itself the argument: **a citation form whose failure rate cannot be measured without
first settling four judgement calls is not a citation form.**

### 6 · Overrun is the easy half. SHIFT is the disease.

Here is the fact that makes this a design law rather than a lint rule.

**Not one of the eleven shattered locators overruns.** The file is 155 lines. Every
cited number — 100, 114, 121, 126, 131, 140, 142 — is comfortably inside it. A checker
that flags citations past end-of-file would report the flagship break **completely
clean**.

`15_THE_TITAN_PASS_2026_08_06/04_CREATE.md` states it exactly:

> "The disease is not overrun, which a naive checker catches. It is **SHIFT**"

— and shift is invisible to every check except one: **did the string you claimed to
cite actually appear where you said it was?** Only a quoted anchor can answer that.
This is the entire reason the law is written the way it is.

### 7 · The path half is broken too

The law says path **plus** string. The path half is not free either.

```
# live tree, bare basenames (no directory component) naming 2+ live files
328 of 2156 path:line tokens   (15.2%)
```

| basename | times cited | live files with that name |
|---|---|---|
| `00_THE_AMRITA.md` | 208 | **3** — of 7, 225 and 122 lines |
| `README.md` | 38 | **154** |
| `AGENTS.md` | 25 | **85** |
| `CLAUDE.md` | 24 | **84** |
| *{no-anchor}* | — | *the four basenames in this table are **named as data**, not cited. They are the subject of the census. An anchor would have to pick one of the candidate files and so assert the uniqueness the row exists to deny.* |

A citation reading `00_THE_AMRITA.md` at some line is not merely fragile. It is
**ambiguous across three real files**, one of which is a seven-line forwarding stub. The
same citation string simultaneously overruns one candidate and lands in prose in the
other two. (That basename is {no-anchor} here, for the same reason as the table above:
the sentence is *about* the name, and quoting one of the three files it matches would
decide the very ambiguity the sentence reports.) Which is why the law reads
*unique* path, and why
`15_THE_TITAN_PASS_2026_08_06/04_CREATE.md` names the first condition of any future
gate as "a bare basename shared by more than one live file".

### 8 · The disease reproduces inside the cure

Three independent instances found this pass, each in a document written to prevent the
thing it commits:

1. **The escorted-number rule, violated by the manifest that carries it.**
   `15_THE_TITAN_PASS_2026_08_06/01_PRESERVE.md` opens with "46 PRESERVE entries across
   six lanes". `grep -c '^### P-[0-9]'` returns **34**, under **five** lettered lanes.
2. **The findability tool's own preamble is stale.**
   `09_TOOLS/01_SCRIPTS/build_corpus_index.py` says "901 of 1661 live documents"; run
   today it printed **837 of 1369**.
3. **The commit message of `7e0ec4c7` itself** — `UNFINDABLE COUNT = 0 … Verified.`
   That string is a commit message, not a line in any file, so this tree has no path to
   anchor it to and does not pretend otherwise; it is written as literal text and
   escorted by the command that reproduces it, `git log -1 --format=%B 7e0ec4c7`.
   Re-run today, the same script reports **11**. All eleven are documents dated
   2026-08-06, written *after* the commit. **The number was true when written and false
   within twenty-four hours.** Nobody lied. That is the point: a re-quoted count decays
   on its own, without anyone doing anything wrong, which is why it must be re-run at
   the point of use and never carried forward.

---

## III · THE INHERITED RULES

These are not new. Each carries over into this tree with its origin named, because a
rule adopted without its source is a rule nobody can audit.

### 1 · Harvest, never infer
**Origin:** `09_TOOLS/01_SCRIPTS/build_corpus_index.py` — "This index HARVESTS. It does not infer, score, or classify."
**Carries over as:** every field in this tree is copied from something a source
declares. A gap is published as a gap. D3 is the load-bearing instance: the station is
empty because the manifest declares nothing there, and the emptiness is printed rather
than filled.

### 2 · Prior art first
**Origin:** `15_THE_TITAN_PASS_2026_08_06/README.md` — "prior art is a citation duty,
never a defect."
**Carries over as:** an inherited result is named with its owner in the same breath as
the claim. The analytic spine of this tree is inherited essentially in full — Euclid,
Dedekind, Cantor, Hardy & Wright, Cauchy, Möbius, Klein and some thirty others. The
mission is coherence, not priority. **Anyone attacking this tree on the grounds that it
owns nothing is attacking a position the tree publishes above its own entries.**

### 3 · Tiers never promote silently
**Origin:** `01_EMERGENTISM/CLAUDE.md` — "Preserve `[A]/[B]/[S]/[I]/[D]/[C]`; never
promote a claim silently."
**Carries over as:** a tier in this tree is the tier its source declares. Generation is
not promotion. Appearing in this tree confers nothing; ratification is a chair act and
nothing here has been ratified. An entry that reads `[I]` in the manifest reads `[I]`
here even where the surrounding prose would flatter a stronger reading.

### 4 · Kills stated before claims
**Origin:** `01_EMERGENTISM/CLAUDE.md` — "Keep counterexamples, alternatives,
predictions, and kill criteria visible." Formalised as the self-correction fence at
`02_EPISTEMOLOGY/00_HOLOBIONT_MEMBRANE_v0.1.md` — "its self-correction fence and points to evidence tiers and kill criteria"
**Carries over as:** the manifest's admission rule, adopted verbatim —
`15_THE_TITAN_PASS_2026_08_06/01_PRESERVE.md`: "An entry that cannot name a hostile
reader it defeats is not on this list." The attack comes first. A claim that arrives
without one does not arrive.

### 5 · Re-run counts; never re-quote them  *(DF-22, the escorted number)*
**Origin:** `00_META/00_THE_CLAIM_STATUS_REGISTER.md`, where the dead form is typed as
a process defect — "a fired falsifier was logged as a pass". Restated as this pass's
operating law in `15_THE_TITAN_PASS_2026_08_06/README.md` — "Re-run every count".
**Carries over as:** every figure in this tree ships with the command that produced it.
Section II.8 is the proof of necessity: three separate documents, all written to
enforce honesty, all carrying a stale number.
*(Custody note, published against interest: `DF-22` is allocated two ways in the
distillation and a third way in the register of record. The rule is real; the number
naming it is disputed and its renumbering is a chair act. This tree uses the name, not
the number, and does not adjudicate.)*

### 6 · A verifier never wrote what it verifies
**Origin — and this one is stated honestly as weaker than the rest.** I searched the
frozen tree for a canonical statement of this rule and **did not find one**. What exists
is the wound it would have prevented, recorded in
`15_THE_TITAN_PASS_2026_08_06/04_CREATE.md` — "the gate has been red and nothing blocks on red"
— and the standing lesson at `14_THE_DISTILLATION/04_WHAT_DIED.md`:
"A guard that cannot fail is worse than no guard, because it reports success."
**Carries over as:** the author of a document may not be the sole verifier of its
anchors, and a gate must demonstrate that it can go red before its green is worth
anything. This tree's gate ships a `--self-test` that corrupts a quote and injects a
banned citation into a temporary copy; both go red correctly. **That is the minimum,
and it is currently the only part of this rule that is mechanised.** The rest is
convention, and convention is what failed last time.

---

## IV · WHAT THIS TREE MAY NEVER DO

Six prohibitions. Each has a mechanical test, because a prohibition that cannot be
tested is a preference.

1. **No path-plus-line-number citations.**
   *Test:* `check_anchors.py` exits non-zero on any `ident:line` or bare `:line` form.
   **Status today: FAILING — 35 instances inside this tree.** Stated first because it
   is the law, and stated as failing because the law does not get a grace period.

2. **No silent tier promotion.**
   *Test:* every entry's tier matches its manifest source. A tier that changes without
   a named chair act is a defect regardless of how well argued the change is.

3. **No claim without its attack.**
   *Test:* an entry with no named hostile reader is not an entry. Deleting the attack
   line deletes the entry.

4. **No number without its command.**
   *Test:* a figure with no adjacent command is unsourced and must be struck rather
   than defended. This applies to numbers inherited from a prior pass with equal force
   — see §II.5, where the figure I was handed was replaced with the one I measured.

5. **Never edit the frozen tree.**
   *Test:* `git status --porcelain` shows no modification originating from this folder.
   *Disclosed breach, this pass:* running the corpus's own indexer to obtain a count
   modified a tracked register file. It was restored with `git checkout --` and the
   figures re-derived by importing the builder's `build()` without its `main()`. **A
   tool documented as a harvester is not thereby read-only, and "read-only" is a
   property to be tested, not read off a docstring.**

6. **No attestation in place of a check.**
   *Test:* the strings "re-read this pass", "re-verified on disk", "anchor
   re-verified", "both lines unchanged" and their family may not appear as warrant.
   The prior pass counted eleven instances of this family corpus-wide. Every one of
   them should have been a command.

---

## V · WHAT THIS LAW DOES NOT DO

Stated plainly, because a constitution that oversells itself is the first thing a
competent attacker takes apart.

- **It does not make anything true.** It makes citations *stay pointed at what they
  cited*. A perfectly anchored tree can be comprehensively wrong. Reading this law as
  an epistemic warrant is warrant substitution — the exact defect §II.4 exists to name.
- **It does not detect a changed source.** If a cited sentence is *edited*, the anchor
  fails loudly, which is correct. If the sentence is edited and the *claim around it*
  quietly reverses, the anchor still resolves and the tree is now wrong with a green
  gate. **Nothing here catches that. It is the largest hole in this design and it is
  named rather than hidden.**
- **It does not survive a non-unique quote.** An anchor appearing twice in a file
  points at neither. Anchors must resolve **exactly once**; this pass pre-checked 37 of
  its own and rejected one.
- **It does not survive hard line wrapping.** An anchor that spans a wrap matches
  nothing. This pass hit that exact failure: the prior-art rule is wrapped across two
  lines in the manifest, so the manifest cannot be quoted for its own rule and the
  pass README is cited instead. **Anchors must be single-line substrings.**
- **It cannot be enforced by anyone who wrote the thing being checked.** See §III.6.
  This is currently the weakest joint in the whole design.

---

## VI · THIS LAW'S OWN KILL

Adopted in the form the frozen tree wrote for its own truth folder —
`00_ESTABLISHED/README.md`:

> "this manifest has become a promotion path."

**Applied here:** if an entry in this tree is ever cited as support for a claim outside
the scope its manifest source states; if an anchor is repaired by weakening the quote
until it matches rather than by fixing the citation; if the gate's failure count is
reduced by narrowing what the gate checks; or if this law is cited as evidence that
anything in this tree is *true* rather than merely *correctly addressed* — **then this
tree has become a promotion path, and the correct response is to withdraw it rather
than defend it.**

The tree is generated. It can be regenerated. Nothing here is worth protecting at the
cost of the thing it was built to protect.

---

## VII · STANDING

This document is **[B] / STAGED and unratified**. It proposes; it decides nothing. It
confers no tier on any entry. It is not a chair act, it does not ratify the manifest it
generates from, and it may never be cited as authority for a claim about the world.

`01_EMERGENTISM` is frozen. It is the provenance record, the graveyard, and the
citation target. **The graves are the immune system.** Nothing in this tree edits them.

•   ⊙   ○
