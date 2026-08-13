#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
16_THE_EMISSION/emit.py — THE EMITTER.

Reads ONE file — 15_THE_TITAN_PASS_2026_08_06/01_PRESERVE.md — and generates the
two spines of the new tree:

    A_THE_LADDER/  what is       (8 stations, one of them deliberately empty)
    B_THE_METHOD/  how we know   (1 file, 14 entries)
    ANCHORS.jsonl  every citation this tree makes into the frozen tree

THE ONE NON-NEGOTIABLE DESIGN LAW
    NO path:line CITATIONS. EVER. QUOTE-ANCHORED ONLY: path + the exact string.

A quoted anchor survives insertion, reflow, frontmatter and reordering.
A line number survives none of them.

Every anchor this generator writes is verified BEFORE it is written: the exact
string is located in the target file, and the string that gets written is a
byte-exact substring of that file. An anchor that does not resolve is never
written into the markdown; it is written into ANCHORS.jsonl with
`"resolved": false` and reported at the end of the run.

WRITES ONLY under 16_THE_EMISSION/. Reads anything. Moves, deletes and stages
nothing.

Usage
    python3 16_THE_EMISSION/emit.py            # generate the tree
    python3 16_THE_EMISSION/emit.py --verify   # regenerate in memory, diff vs disk
    python3 16_THE_EMISSION/emit.py --counts   # print the escorted counts only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# 0 · Geography.  Nothing outside OUT is ever written.
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent            # …/01_EMERGENTISM/16_THE_EMISSION
ROOT = HERE.parent                                # …/01_EMERGENTISM   (FROZEN)
SOURCE_REL = "15_THE_TITAN_PASS_2026_08_06/01_PRESERVE.md"
SOURCE = ROOT / SOURCE_REL

LADDER_DIR = "A_THE_LADDER"
METHOD_DIR = "B_THE_METHOD"
ANCHORS_REL = "ANCHORS.jsonl"

# Directories excluded from path resolution.  16_THE_EMISSION is excluded so the
# generator can never resolve a citation into its own output — that is what makes
# the second run byte-identical to the first.
INDEX_SKIP_PREFIXES = (".git/", "16_THE_EMISSION/")
# Archive and compatibility mirrors lose to the live lane; 12_PUBLIC_SITE loses too,
# because a publication surface is a mirror of source truth and never the source.
DEPRIORITISED_PREFIXES = ("90_ARCHIVE/", "91_COMPATIBILITY/", "12_PUBLIC_SITE/")
INDEX_SUFFIXES = {".md", ".py", ".html", ".json", ".jsonl", ".yaml", ".yml"}

# ---------------------------------------------------------------------------
# 1 · THE STATION MAP.  Given by the law; not inferred.
#     20 entries sit on the ontological ladder.  14 are METHOD, which has no
#     station on a ladder of what-is.
# ---------------------------------------------------------------------------

LADDER_STATIONS = [
    {
        "key": "ground",
        "file": f"{LADDER_DIR}/00_GROUND.md",
        "mark": "•",
        "title": "GROUND — counting cannot begin",
        "register": "•",
        "entries": ["P-11", "P-12"],
        "is": """The register before the first mark. Nothing here is an operand, because
there is not yet anything of the type that operations take.

Both entries are **fences, and both survive by saying so.** P-11 keeps a mark from
ever being counted; P-12 keeps the Titan frame from ever carrying arithmetic. Neither
is presented as a fact about the world. That is precisely why a hostile reader cannot
take them: there is no concealed factual claim to overturn.

The ground is the one station where the corpus's strongest available result is
deliberately not exported. P-12 concedes that on the compactified positive ray
`{0,1,∞}` is *forced*, and then refuses to carry the forcing anywhere else.""",
        "not": """- **Any operation.** No addition, no multiplication, no ordering over `• ⊙ ○`.
  `ArithmeticSignature(TitanFrame)=∅` is the fence, and it is signed canon.
- **`⊙ = • × ○` in any asserted form.** Retired 2026-08-01. It is not restored, and
  nothing at this station may be read as restoring it. The surviving form names a
  held relation, never a product.
- **Any claim that the ground is zero, a number, or an element.** Zero is a real
  number and belongs at the unit station, under P-15's signed phrasing ban.
- **Any export.** A result forced at this station stays at this station. The document
  that forces `{0,1,∞}` is the same document that forbids exporting it.
- **Any upgrade of a fence to a fact.** "A mark, never an operand" is a stipulation.
  The corpus says so in harsher words than an attacker would use, and it holds only
  as long as it is called a fence.""",
    },
    {
        "key": "unit",
        "file": f"{LADDER_DIR}/01_THE_UNIT.md",
        "mark": "1",
        "title": "THE UNIT",
        "register": "1",
        "entries": ["P-15", "P-20"],
        "is": """The first thing that can be counted, and the seat from which the positive
rationals are generated.

The two entries do opposite work and need each other. P-15 says what the unit's
neighbourhood is **not** — `0` is a real number; what is true is that it is the unique
element of a field with no multiplicative inverse, so the sentence is `0 ∉ ℝˣ` and
never `0 ∉ ℝ`. P-20 says what the unit **does** — the free pair `⟨S,L⟩` generates all
of `ℚ⁺` from `1`, and the inversion `ι` is not recoverable from it.

Both are inherited. Neither is owned. That is the normal condition of this tree.""",
        "not": """- **Ownership.** Elementary field theory is not the corpus's, and the generating
  tree is Calkin–Wilf 2000 — cited by the corpus's own source before anyone attacked it.
- **Bare "X is not a number".** Banned corpus-wide by signed ruling. The ban is the
  entry; the retraction of the corpus's own earlier phrasing is what it survives.
- **Aesthetics as structure.** "The elegant one always moves, one rests exactly once"
  is a property of the chosen pair, not of `ℚ⁺`. The corpus drew that deflation against
  its own taste, and it is correct.
- **The balance warrant.** Any reading in which the unit is *optimal* because a
  balance function peaks there belongs at D2, where it is refuted. See D2, P-03.
- **A signature as a truth-maker.** A signed `[S]` is still an `[S]`. The receipt says
  so in its own header.""",
    },
    {
        "key": "d1",
        "file": f"{LADDER_DIR}/02_D1_ARITHMETIC.md",
        "mark": "D1",
        "title": "D1 — ARITHMETIC · DISTINCTION",
        "register": "D1",
        "entries": ["P-01", "P-16"],
        "is": """The register where a distinction becomes an operation and a word becomes a
normal form.

P-01 is the model for the whole pass: it proved its own open conjecture and destroyed
its own novelty claim **in the same document, before anyone else could**. Reduced words
are unique normal forms — and that is the uniqueness of the finite simple continued
fraction, Hardy & Wright, with Euclid underneath.

P-16 is the same discipline applied to language rather than to a theorem: a two-clause
ruling about `√2`, which publishes the condition under which it would lose and records
that the test has not been run.""",
        "not": """- **Novelty.** Neither entry owns its mathematics. F1 remains **OPEN**, and G2
  must not be cited as passing it — the adjudicating document forfeits that itself.
- **A council vote as authority.** Two agent councils advised on the `√2` ruling;
  neither signed. Only a natural person signed.
- **A theorem number as evidence.** The G2 document records that the cited theorem
  *number* was never checked against a physical copy — and says it first, twice. The
  proof is self-contained and does not depend on the numbering.
- **Reach.** The `√2` ruling concedes its own kill: a fresh reader will still hear
  *they say √2 isn't a number*. It survives by publishing that, not by beating it.""",
    },
    {
        "key": "d2",
        "file": f"{LADDER_DIR}/03_D2_CONFIGURATION.md",
        "mark": "D2",
        "title": "D2 — CONFIGURATION · RELATION",
        "register": "D2",
        "entries": ["P-03", "P-17", "P-18"],
        "is": """The register where two things are held in relation and the relation is given a
form: the harmonic mean and its trigonometric and hyperbolic faces (P-03), the fences
that forbid the retired node-product from being used as a live ordering (P-17), and
the product decomposition `HM = GM × BAL`, narrowed and restored after a fair
re-adjudication (P-18).

This is the most dangerous station in the tree, and it is the one that most clearly
demonstrates the pass's method. Every identity here survives. **Every warrant that was
hung on those identities dies**, and in each case the corpus killed it first.""",
        "not": """- **The ethics warrant.** "B is maximal at the unit, therefore balance is optimal"
  is refuted by the corpus itself: B behaves that way *only* because `ν` is **defined**
  as `1/φ`. Release the constraint and the maximum moves. The identity survives; the
  warrant dies on contact.
- **`P_node = Φ × V` as a current ordering.** The source documents say ***UNLICENSED***
  in their own words. A gate fires on them anyway; the gate is wrong and is scheduled
  for repair. Repair the gate, never the fence.
- **`⊙ = • × ○` in new coordinates.** The *form* is dead. The *reading* stands,
  narrowed and cited — Nash 1950, Sonnevend 1985/86, product t-norm, series reliability.
- **The antipodal reading.** "The two poles are antipodal at chordal distance 2" was
  killed by the corpus — the one genuine kill of the eighteen in the fair re-adjudication.
  The two factors are chart-point-to-pole distances, never mark-to-mark.
- **A change of coordinate published as a result.** `sech(log x)` is `x = cot(θ/2)`.
  Identical typography licenses no substitution.
- **The `What survives` clause of P-18 as written** — the entry carries its own
  falsity flag, and this tree carries it forward rather than quietly repairing it.""",
    },
    {
        "key": "d3",
        "file": f"{LADDER_DIR}/04_D3_STATE.md",
        "mark": "D3",
        "title": "D3 — THE PROBABILITY-BEARING STATE",
        "register": "D3",
        "entries": [],
        "is": "",   # D3 has a bespoke body; see render_d3().
        "not": "",
    },
    {
        "key": "d4",
        "file": f"{LADDER_DIR}/05_D4_ACTUAL.md",
        "mark": "D4",
        "title": "D4 — THE ACTUAL · RECEIPTS",
        "register": "D4",
        "entries": ["P-29", "P-31", "P-32", "P-33", "P-34"],
        "is": """The register of what actually happened: instruments that ran, gates that fired,
stubs that were created for a stated reason, cards that hash byte-exact to the source
they claim to have reviewed.

**The survival test changes shape here, and the change is itself a result.** Every
entry on the ladder above carries an *attack survived* — a named hostile reader, defeated.
Every entry at D4 carries a *finding*, verified. At the actual register the hostile
reader is replaced by a command that either exits 0 or does not, and the entry stands or
falls on the exit code. This is not a weaker standard. It is the only standard the actual
register admits.

Four of these five entries **overturn the pass's own premises in the artifacts' favour.**
They are here so that nothing sweeps them: a link checker that was accused of hiding
148 dead links and is honest (P-29); a census gate that reports its own FAIL rather than
launder it (P-31); a register of dead forms that turned out to be *better* than the
catalogue someone proposed rebuilding (P-32); and 20 claim cards that would have been
killed for unreachability over a directory rename (P-34).""",
        "not": """- **Doctrine.** `live=115` is uninterpretable as a doctrine measure until the census
  gate's META filter reaches markdown, and it may not be quoted as one until then. The
  instrument is preserved *and* fenced in the same breath.
- **A sweep.** Sweeping the 60 archive-terminating stubs would delete the device that
  keeps the archive subordinate. Sweeping the 20 recoverable cards would destroy sound
  reviews over a path prefix.
- **A chair act performed by a generator.** Naming which of two live lineages is
  custodial for a claim-card source is a chair act. Re-stamping `reviewed_source_sha256`
  after a locator repair is a chair act. Both are located and both stop here.
- **An `mv`.** *You do not perform a corpus-wide `mv` while the machinery that detects
  damage is down.* That rule is at METHOD, P-25, and it governs this station absolutely.
- **A repair mistaken for a refutation.** 26 claims are untouched; only their locators
  are stale. Drift is custody failure, not doctrinal failure.""",
    },
    {
        "key": "d5",
        "file": f"{LADDER_DIR}/06_D5_POSSIBLE.md",
        "mark": "D5",
        "title": "D5 — THE POSSIBLE · THE VOW",
        "register": "D5",
        "entries": ["P-05", "P-06", "P-07", "P-09"],
        "is": """The modal register, and the only station in this tree where an *ought* appears.

Everything here is `[I]` at its core, and every entry says so on its own line. The vow
is not a theorem (P-05). The dyadic gate is a posited direction that survived the
instrument which killed its own aggregate paraphrase (P-06). The constitutive argument
makes the vow non-arbitrary and publishes two fences that stop it short of the gate
(P-07). Teleology is a cross-register conjunction, and only one conjunct is at D5 (P-09).

The strongest thing at this station is a **refusal**. The corpus's most wanted result
was a derivation of the ought from the geometry. It published, in five independent
places, that it does not have one.""",
        "not": """- **A theorem.** Not one claim here is `[A]`. The corpus's own word for what it did
  to the is–ought gap is **bypass**, not closure — *"a bypass is honest only while it is
  called one."*
- **`η = 0` as a derivation.** It is a conditional gate. The deleted load-bearing word
  was **CONDITIONAL**, and *"a rule that requires enforcement is a preference with a
  police force, not a derivation."*
- **`ΣΔP` in any aggregate form.** Ruled out 2026-07-13 as a leak that silently
  licenses extraction. Preserve the dyadic gate; never the sum.
- **Evaluation, ranking, selection, or means.** Read the subscripts: only `Φ₅` is at D5.
  The rest is D4. *A future that has not occurred does not push the present.*
- **A settled threshold.** The gate has two inequivalent thresholds and both are called
  "the dyadic gate": one admits non-decrease, one requires strict rise. An act where the
  whole rises and one bearer stays exactly flat passes one and fails the other. **This is
  open and it is a chair act.** This tree does not close it.
- **A quantum reading.** D5 is agent-represented counterfactual content and is not
  quantum branch space. See D3.""",
    },
    {
        "key": "horizon",
        "file": f"{LADDER_DIR}/07_HORIZON.md",
        "mark": "○",
        "title": "HORIZON — ABSORPTION",
        "register": "○",
        "entries": ["P-02", "P-14"],
        "is": """The far pole. Where adjoining a new element changes nothing (P-02), and where
the end of the ladder refuses to be its beginning (P-14).

These two entries are the same discipline read in two directions. Absorption
`V ∪ {x} = V` is the horizon's defining behaviour, and the corpus's source anticipated
the only serious objection to it **before it was made**: this is not Dedekind-infiniteness,
because the equality holds *literally, as classes*, not merely up to bijection.
`ℕ ∪ {x} ≈ ℕ` but `ℕ ∪ {x} ≠ ℕ`. One word — *literally* — is the discriminating step.

P-14 holds the other end shut. D6 and D0 agree in output for **opposite reasons**, and
that agreement-in-output is what keeps being misread as sameness of thing. The licensed
picture is `ι` **exchanging** the poles: one two-element orbit of two distinct points.""",
        "not": """- **Identity.** D6 ≢ D0. **Exchange, not quotient.** The ruling carries a standing
  fence because the error recurs: it is repaired there and not re-litigated.
- **Bijection.** Absorption up to bijection is Dedekind's, is true of `ℕ`, and is not
  what the entry claims. Drop the word *literally* and the entry becomes false.
- **An unfalsifiable horizon.** The kill is decidable — *exhibit a finite set unchanged
  by adjoining a new element* — and it cannot fire. A kill that is decidable and cannot
  fire is a result; a kill that cannot be stated is a decoration.
- **Ratification as a truth-maker.** The host document reads STAGED PROPOSAL. The fact
  is Dedekind's, 1888. Ratification governs the seat assignment, never the theorem.""",
    },
]

METHOD_FILE = f"{METHOD_DIR}/00_THE_METHOD.md"
METHOD_ENTRIES = ["P-04", "P-08", "P-10", "P-13", "P-19", "P-21", "P-22",
                  "P-23", "P-24", "P-25", "P-26", "P-27", "P-28", "P-30"]

# Why each METHOD entry has no station on a ladder of what-is.  Authored here,
# derived from each entry's own text — not transcribed from it.
WHY_METHOD = {
    "P-04": "An ownership ledger over nineteen results. It records who reached them first, "
            "which is a fact about the literature, not about what is. Its conclusion — zero "
            "owned — is uninformative, not bad.",
    "P-08": "It reads like a station and is not one. Its own §5 calls the standalone set "
            "*a METHOD + a POSTURE + a VOW + a geometry*, not a world-picture that accounts "
            "for the contents of the world. Stationing it would promote what it concedes.",
    "P-10": "A typing rule. It says which register a token may be read in; it asserts nothing "
            "about any token. It is the instrument by which the ladder is applied, so it cannot "
            "also be a rung of it.",
    "P-13": "A ruling about how the foundation may be cited. It demotes sphere primacy from "
            "primacy to *selection* and publishes the rival's full bill. Custody, not seat.",
    "P-19": "A kill, done correctly. The `[A]` theorem inside belongs to its owner; what is "
            "preserved here is the shape of a kill that refuses to over-reach.",
    "P-21": "A register of validity. Each row's content sits wherever its own hypotheses put "
            "it. The register is an instrument for reading the ladder, not a place on it.",
    "P-22": "A named defect shape — and the countermeasure this entire tree is written under: "
            "*re-run counts, never re-quote them.*",
    "P-23": "The rules themselves, with the efficacy claim left at `[C]` in the file's own "
            "opening. A method that claims its own success is no longer a method.",
    "P-24": "The rule that did the most damage to its author. Pure procedure — and running it "
            "at corpus scale returned six of seven cluster claims pre-empted.",
    "P-25": "Custody discipline. This pass is its proof: the single largest defect on disk is "
            "custody failure, not doctrinal failure.",
    "P-26": "An admission gate for interpretations. Three entries passed it out of the whole "
            "corpus. A gate is not a claim about the world; it is a claim about admission.",
    "P-27": "`[PROJECTION]` — it has no tier of its own; each entry carries its source's. "
            "A publication form, and the most transferable thing in the corpus.",
    "P-28": "The corpus's diagnosis of itself. *The failure mode is not falsity. It is "
            "unfindability.* Every finding in this pass is an instance of it.",
    "P-30": "An archive protocol. It keeps live citations resolvable without letting the "
            "archive become a competing owner — the cure, not the disease.",
}

# Candidate anchors for the citation law itself.  First one that resolves is used.
LAW_ANCHOR_CANDIDATES = [
    ("14_THE_DISTILLATION/00_THE_AMRITA.md",
     "cite by unique path **plus a quoted string**, never by a bare line range"),
    ("14_THE_DISTILLATION/README.md",
     "Cite it by path plus quoted string, never by a bare line range"),
    ("14_THE_DISTILLATION/01_WHAT_IS_PROVED.md",
     "cite by unique path **plus a quoted string**, never by a bare line range"),
]

# Candidate anchors for the Provenance block.  Every generated file names its
# source in prose, and the tree's own law binds that mention like any other: a
# path with no quoted string beside it is an unanchored citation.  It was the
# single most repeated failure in this lane — one per generated file.  The fix
# is to ANCHOR the mention, not to exempt it: the source is quoted, verified,
# and the quote is written back byte-exact, exactly as every other anchor here.
SOURCE_ANCHOR_CANDIDATES = [
    (SOURCE_REL, "46 PRESERVE entries across six lanes"),
    (SOURCE_REL, "Each entry: **claim · tier · owner · the attack it"),
    (SOURCE_REL, "the corpus attacked every entry first and published the wound"),
]

# Candidate anchors used by the D3 station to explain its own emptiness.
D3_ANCHOR_CANDIDATES = [
    ("05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
     "A D3 state is one probability-bearing frame."),
    ("06_ONTOLOGY/00_ONTOLOGY_ACROSS_DIMENSIONS.md",
     "its D3 placement is `[I]`"),
    ("06_ONTOLOGY/00_ONTOLOGY_ACROSS_DIMENSIONS.md",
     "Interpretations remain removable."),
    ("05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
     "The Burri film-from-frames conjecture"),
    ("14_THE_DISTILLATION/04_WHAT_DIED.md",
     "two of five candidate emergence crossings, FAILED"),
    ("14_THE_DISTILLATION/06_WHAT_IS_STILL_OPEN.md",
     "both failures survive the change of instrument"),
]

# ---------------------------------------------------------------------------
# 2 · Text normalisation and quote resolution.
#
#     normalise() strips markdown emphasis and collapses whitespace while
#     keeping, for every surviving character, its offset in the ORIGINAL text.
#     That index map is what lets the generator write back a byte-exact
#     substring of the target file rather than the manifest's paraphrase of it.
# ---------------------------------------------------------------------------

MARKUP_CHARS = set("*`_")
CHAR_FOLD = {
    0x201C: '"', 0x201D: '"', 0x201E: '"',
    0x2018: "'", 0x2019: "'", 0x201A: "'",
    0x00A0: " ", 0x2009: " ", 0x202F: " ",
    0x2011: "-",
}
MIN_ANCHOR_LEN = 20
MAX_ANCHORS_PER_TARGET = 2

# ---------------------------------------------------------------------------
# 2a · THE LINE-LOCATOR SCRUBBER.
#
#     THE ONE NON-NEGOTIABLE DESIGN LAW of this generator — stated at the top of
#     this file and printed into the head of every file it writes — is that no
#     line number is ever written into this tree.  Until this scrubber existed
#     the law governed only the anchors the generator MINTED; the prose it
#     COPIED from the manifest carried the manifest's own `path:line` locators
#     straight through, and check_anchors.py failed 18 of them.  The generator
#     was breaking its own stated law in the one place it never looked.
#
#     The three shapes below mirror HARD_BANS in check_anchors.py exactly.  They
#     are duplicated rather than imported on purpose: the generator must not
#     depend on the gate that judges it.  If check_anchors.py changes its bans,
#     these change too — the run report prints every scrub so a divergence shows
#     up as a count, never as a silent pass.
#
#     What is dropped is the LOCATOR ONLY.  The path, the document number and
#     the identifier all survive, because those are the citation; the line
#     number is the part that survives no edit.  A locator with nothing in front
#     of it becomes `…` — an elision the reader can see, not a deletion the
#     reader cannot.  Nothing is inferred and nothing is reworded.
# ---------------------------------------------------------------------------

# B1  path with an extension, then :line        FILE.md:124   FILE.md:15-26
SCRUB_EXT_LINE = re.compile(
    r"([A-Za-z0-9_][A-Za-z0-9_./+\-]*\.(?:md|py|txt|jsonl|json|yaml|yml|csv|html|js|ts|toml|cfg|sh))"
    r":\d+(?:\s*[-–,]\s*\d+)*"
)
# B3  identifier or number, then :line          RUNGS:722   193:15-17   55:156
SCRUB_IDENT_LINE = re.compile(
    r"(?<![\w:])((?:[A-Za-z_][A-Za-z0-9_]*|\d{3,})):\d+(?:\s*[-–,]\s*\d+)*"
    r"|(?<![\w:])(\d{1,2}):\d+\s*[-–,]\s*\d+"
    r"|(?<![\w:])(\d{1,2}):\d{3,}"
)
# B2  bare colon-line, nothing in front of it   at `:246`   , :82-83
SCRUB_BARE_COLON = re.compile(
    r"(?<![\w:])(:\d+(?:\s*[-–,]\s*\d+)*)(?![\d:])"
)
# ordinary URLs are not citations; B3 fires on them and must not.
SCRUB_EXEMPT = re.compile(r"^(?:https?|ftp|file|mailto|git|ssh)$", re.I)

SCRUBBED = []          # every removal, itemised for the run report


def delocate(s, where="—"):
    """Remove line locators from inherited prose.  Records every removal.

    Applied to text COPIED from the manifest, never to an anchor the generator
    minted — a minted anchor has no line number to begin with.
    """
    if not s:
        return s

    def keep_head(m):
        head = m.group(1)
        if SCRUB_EXEMPT.match(head):
            return m.group(0)
        SCRUBBED.append((where, m.group(0), head))
        return head

    def keep_ident(m):
        head = m.group(1) or m.group(2) or m.group(3)
        if SCRUB_EXEMPT.match(head):
            return m.group(0)
        SCRUBBED.append((where, m.group(0), head))
        return head

    def elide(m):
        SCRUBBED.append((where, m.group(1), "…"))
        return "…"

    out = SCRUB_EXT_LINE.sub(keep_head, s)
    out = SCRUB_IDENT_LINE.sub(keep_ident, out)
    out = SCRUB_BARE_COLON.sub(elide, out)
    return out


# ---------------------------------------------------------------------------
# 2b · THE INHERITED-QUOTE REPAIR.
#
#     shrink() already carries the "fix the quote" branch of this tree's law —
#     the manifest quotes with the MANIFEST's punctuation and framing, so the
#     generator recovers the longest run of words that genuinely appears in the
#     target and writes THAT.  Until now that branch governed only the anchors
#     the generator MINTED.  The prose it COPIED carried the manifest's framing
#     straight through, and the gate — which reads a quoted string beside a path
#     token as an anchor, because that is exactly what this tree's law says one
#     is — failed those sites.  `"kill criteria on every axiom."` where the
#     source has a semicolon; `"Keep the dyadic gate."` where the source has a
#     comma; `"actual boundary token."` where the source is a table cell.
#
#     This pass applies the SAME harvester to inherited prose.  It never invents
#     and never widens: a repair is written only when the recovered string is a
#     byte-exact substring of the file the gate will attribute the quotation to.
#     Where nothing can be harvested the quotation is LEFT EXACTLY AS THE
#     MANIFEST WROTE IT and the gate stays red — a red gate is the correct
#     output for a quotation this tree cannot verify.
#
#     Every repair is itemised in the run report, like every scrub.
# ---------------------------------------------------------------------------

# Floor for a REPAIRED quotation.  Lower than MIN_ANCHOR_LEN (which governs the
# anchors this generator mints from scratch) because a repair is not choosing an
# anchor — the manifest already chose it and this pass only trims the manifest's
# punctuation off the ends.  Still above check_anchors.py's MIN_QUOTE_CHARS of 8.
REQUOTE_MIN_LEN = 12
# A repair may not shrink a quotation into a fragment of itself.  Below this
# ratio the difference is not punctuation, it is a different sentence, and the
# honest output is the manifest's words plus a red gate.
REQUOTE_MIN_RATIO = 0.55
# Punctuation this pass is allowed to move OUT of a quotation.  It is moved, not
# deleted: the source's words go inside the quotes and the quoting sentence keeps
# its own terminator outside them.  `"Keep the dyadic gate."` where the source has
# a comma becomes `"Keep the dyadic gate".` — the quotation becomes byte-exact and
# the sentence still ends.  Anything other than these characters means the
# difference is WORDS, not framing, and the repair is refused.
REQUOTE_TAIL_PUNCT = ".,;:!?…"

REQUOTED = []          # every repair, itemised for the run report

_REQ_PATH_RE = re.compile(r"`([^`\n]+)`")
_REQ_PATH_SHAPE = re.compile(
    r"^[A-Za-z0-9_][A-Za-z0-9_./+\-]*\.(?:md|py|txt|jsonl|json|yaml|yml|csv|html|js|ts|toml|cfg|sh)$"
)


def gate_resolve(index: "FileIndex", token: str):
    """Resolve a path token the way check_anchors.py will resolve it.

    Deliberately NOT FileIndex.resolve(): that one ranks candidates and lets the
    quote pick the file, which is right for minting an anchor and wrong here.
    This pass must know which file the GATE will hold the quotation against, and
    the gate takes the corpus-relative path, or a UNIQUE basename, or nothing.
    Anything the gate cannot resolve unambiguously is left untouched.
    """
    token = token.strip().strip("`")
    if token in index.relset:
        return token
    if "/" not in token:
        hits = index.by_base.get(token, [])
        if len(hits) == 1:
            return hits[0]
    return None


def _resolves_in(index: "FileIndex", rel: str, quote: str) -> bool:
    """Whitespace-normalised containment — check_anchors.py's matching contract."""
    nq, _ = normalise(quote)
    if len(nq) < REQUOTE_MIN_LEN:
        return False
    ntext, _ = index.norm(rel)
    return nq in ntext


def requote(s, index: "FileIndex", where="—"):
    """Repair inherited-prose quotations against the file the gate will use.

    Mirrors check_anchors.py's reading of a quotation site: on one line, the
    site runs from the first `"` to the last, the inner pairs are the readings,
    and the path token it belongs to is the NEAREST one that does not sit inside
    the site. Duplicated rather than imported, for the same reason the banned
    forms are: the generator must not depend on the gate that judges it.
    """
    if not s or '"' not in s:
        return s
    out_lines = []
    for line in s.split("\n"):
        qs = [i for i, ch in enumerate(line) if ch == '"']
        if len(qs) < 2:
            out_lines.append(line)
            continue
        lo, hi = qs[0], qs[-1]

        # the nearest path token that is not inside the quotation site
        best_tok, best_d = None, None
        for m in _REQ_PATH_RE.finditer(line):
            cand = m.group(1).strip().split("#")[0].strip()
            if not _REQ_PATH_SHAPE.match(cand):
                continue
            if m.start() < hi and lo < m.end():
                continue                      # inside the site: quoted material
            d = lo - m.end() if m.end() <= lo else m.start() - hi
            if d < 0 or d > 500:              # check_anchors.PAIR_WINDOW
                continue
            if best_d is None or d < best_d:
                best_tok, best_d = cand, d
        if best_tok is None:
            out_lines.append(line)
            continue
        rel = gate_resolve(index, best_tok)
        if rel is None:
            out_lines.append(line)
            continue

        # repair each inner pair in place, right to left so offsets hold
        for i in range(len(qs) // 2 - 1, -1, -1):
            a, b = qs[2 * i], qs[2 * i + 1]
            body = line[a + 1:b]
            if not body.strip() or _resolves_in(index, rel, body):
                continue
            exact, _occ = index.locate(rel, body, min_len=REQUOTE_MIN_LEN)
            if not exact:
                continue
            if '"' in exact or exact.count("`") % 2:
                continue                      # would re-parse the site: refuse
            nb, _ = normalise(body)
            ne, _ = normalise(exact)
            if len(ne) < REQUOTE_MIN_LEN or len(ne) < REQUOTE_MIN_RATIO * len(nb):
                continue                      # a fragment, not a punctuation trim
            # This pass trims the manifest's framing off the END of a quotation
            # and nothing else.  A recovered string that is not a head of what the
            # manifest wrote would be this generator RE-CHOOSING the quotation,
            # which is the author's act, not the projector's.  Refused.
            if not nb.startswith(ne):
                continue
            tail = nb[len(ne):].strip()
            if tail.strip(REQUOTE_TAIL_PUNCT):
                continue                      # the difference is words: refuse
            # move the trimmed punctuation outside the closing quote, never drop it
            line = line[:a + 1] + exact + line[b] + tail + line[b + 1:]
            REQUOTED.append((where, rel, f'"{body}"', f'"{exact}"{tail}'))
        out_lines.append(line)
    return "\n".join(out_lines)


def fold(s: str) -> str:
    """Length-preserving character fold.  Index-safe."""
    s = unicodedata.normalize("NFC", s)
    return s.translate(CHAR_FOLD)


def normalise(s: str):
    """Return (normalised_text, index_map) where index_map[i] is the offset in s."""
    s = fold(s)
    out, idx = [], []
    prev_space = True
    for i, ch in enumerate(s):
        if ch in MARKUP_CHARS:
            continue
        if ch.isspace():
            if prev_space:
                continue
            out.append(" ")
            idx.append(i)
            prev_space = True
        else:
            out.append(ch)
            idx.append(i)
            prev_space = False
    while out and out[-1] == " ":
        out.pop()
        idx.pop()
    return "".join(out), idx


TRIM = " ,;:.!?—–-"


def fragments(needle: str, min_len=MIN_ANCHOR_LEN):
    """Split a needle at elisions; longest fragment first."""
    parts = re.split(r"…|\.\.\.", needle)
    parts = [p.strip(TRIM) for p in parts]
    parts = [p for p in parts if len(p) >= min_len]
    return sorted(set(parts), key=lambda p: (-len(p), p))


MAX_WINDOW_WORDS = 45


def shrink(frag: str, min_len=MIN_ANCHOR_LEN):
    """Yield the fragment, then every contiguous word-window of it, longest first.

    The manifest quotes with the punctuation and framing of the MANIFEST, not of the
    source: a trailing period the source lacks, a comma where the source has an arrow,
    a clause the manifest joined. Windowing recovers the longest run of words that
    genuinely appears. This is the "fix the quote" branch of the law, done
    mechanically — what is finally written is still a byte-exact substring of the
    target, and a window that appears nowhere is never written.
    """
    seen = set()

    def clean(c):
        c = c.strip(TRIM)
        if len(c) >= min_len and c not in seen:
            seen.add(c)
            return c
        return None

    first = clean(frag)
    if first:
        yield first
    words = frag.split(" ")[:MAX_WINDOW_WORDS]
    n = len(words)
    for length in range(n, 1, -1):
        for start in range(0, n - length + 1):
            c = clean(" ".join(words[start:start + length]))
            if c:
                yield c


class FileIndex:
    """The frozen tree, indexed once.  Never includes 16_THE_EMISSION."""

    def __init__(self, root: Path):
        self.root = root
        rels = []
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix not in INDEX_SUFFIXES:
                continue
            rel = p.relative_to(root).as_posix()
            if rel.startswith(INDEX_SKIP_PREFIXES):
                continue
            rels.append(rel)
        self.rels = sorted(rels)
        self.relset = set(self.rels)
        self.by_base = {}
        for rel in self.rels:
            self.by_base.setdefault(rel.rsplit("/", 1)[-1], []).append(rel)
        self._text_cache = {}
        self._norm_cache = {}

    def text(self, rel: str) -> str:
        if rel not in self._text_cache:
            self._text_cache[rel] = (self.root / rel).read_text(
                encoding="utf-8", errors="replace")
        return self._text_cache[rel]

    def norm(self, rel: str):
        if rel not in self._norm_cache:
            self._norm_cache[rel] = normalise(self.text(rel))
        return self._norm_cache[rel]

    def resolve(self, token: str):
        """Map a manifest path token onto real relpaths, best-first.

        Returns a ranked candidate list.  It is deliberately a LIST: when a bare
        basename exists in several lanes, the path preference order is a guess, and
        a guess is not an anchor.  The caller disambiguates by asking which candidate
        the entry's own quoted strings actually appear in.  The quote picks the file.
        """
        token = token.strip().strip("`")
        if "…" in token or "..." in token:          # elided middle segment
            token = token.rsplit("/", 1)[-1]
        base = token.rsplit("/", 1)[-1]
        cands = []
        if token in self.relset:
            cands.append(token)                     # written as-is — a candidate, not a verdict
        cands += [r for r in self.rels if r.endswith("/" + token) and r not in cands]
        if not cands:
            # Basename fallback ONLY when the written path matches nothing. Running it
            # unconditionally turned `00_ESTABLISHED/README.md` into 252 candidates.
            cands = list(self.by_base.get(base, []))
        if not cands:
            return []
        pass_dir = Path(SOURCE_REL).parent.as_posix() + "/"

        def rank(rel):
            # 0 best.  Exactly what the manifest wrote, or a sibling of the manifest
            # for a bare basename.  Archive, compatibility and publication mirrors lose.
            if rel == token:
                return 0
            if "/" not in token and rel == pass_dir + token:
                return 0
            if rel.startswith(DEPRIORITISED_PREFIXES):
                return 3
            if rel.startswith(pass_dir):
                return 2
            return 1

        self._rank_of = getattr(self, "_rank_of", {})
        for r in cands:
            self._rank_of[(token, r)] = rank(r)
        return sorted(cands, key=lambda r: (rank(r), r))

    def rank_of(self, token, rel):
        return getattr(self, "_rank_of", {}).get((token, rel), 9)

    def locate(self, rel: str, quote: str, min_len=MIN_ANCHOR_LEN):
        """Verify a quote inside a file.  Returns (exact_substring|None, occurrences)."""
        text = self.text(rel)
        ntext, imap = self.norm(rel)
        nq, _ = normalise(quote)
        for frag in fragments(nq, min_len) or ([nq] if len(nq) >= min_len else []):
            for cand in shrink(frag, min_len):
                pos = ntext.find(cand)
                if pos < 0:
                    continue
                start, end = imap[pos], imap[pos + len(cand) - 1] + 1
                span = text[start:end]
                # An anchor must be written on one line to stay quotable. When the
                # match crosses a line break in the source, keep the longest piece
                # that is still a real anchor: long enough, or short but unique.
                pieces = [pc.strip() for pc in span.split("\n")]
                pieces = [pc for pc in pieces
                          if len(pc) >= min_len
                          or (len(pc) >= 10 and text.count(pc) == 1)]
                if not pieces:
                    continue
                best = max(pieces, key=len)
                if best in text:
                    return best, text.count(best)
        return None, 0


# ---------------------------------------------------------------------------
# 3 · Parsing 01_PRESERVE.md.  PARSE, DO NOT RETYPE.
# ---------------------------------------------------------------------------

ENTRY_RE = re.compile(r"^### (P-\d\d) · (.+?)[ \t]*$", re.M)
BULLET_RE = re.compile(r"^-\s+(.*)$")
LABEL_RE = re.compile(r"^(?:⚠️\s*)?\*\*(.+?)\*\*(.*)$", re.S)

FIELD_LABELS = [
    ("Owner boundary", "owner_boundary"),
    ("Attacks survived", "attack"),
    ("Attack survived", "attack"),
    ("Locator", "locator"),
    ("Claim", "claim"),
    ("Finding", "finding"),
    ("Owner", "owner"),
    ("Tier", "tier"),
    ("Boundary", "boundary"),
    ("OPEN", "open"),
    ("Separately", "separately"),
    ("The genuine defect", "genuine_defect"),
]

TICK_RE = re.compile(r"`([^`\n]+)`")
PATHTOK_RE = re.compile(r"([A-Za-z0-9_…][A-Za-z0-9_…./\-]*\.(?:md|py|html))")
QUOTE_RE = re.compile(r'"([^"\n]{12,400})"')


class Entry:
    def __init__(self, eid, title, heading, body):
        self.id = eid
        self.title = title
        self.heading = heading          # exact line, used as the anchor into the manifest
        self.body = body
        self.fields = {}
        self.notes = []
        self._parse()

    def _parse(self):
        bullets, cur = [], None
        for line in self.body.split("\n"):
            m = BULLET_RE.match(line)
            if m:
                if cur is not None:
                    bullets.append(cur)
                cur = m.group(1).rstrip()
            elif line.strip():
                if cur is not None:
                    cur += " " + line.strip()
            else:
                if cur is not None:
                    bullets.append(cur)
                    cur = None
        if cur is not None:
            bullets.append(cur)

        for b in bullets:
            m = LABEL_RE.match(b)
            if not m:
                self.notes.append(b.strip())
                continue
            label_raw, rest = m.group(1).strip(), m.group(2).strip()
            hit = None
            for prefix, key in FIELD_LABELS:
                if label_raw == prefix or label_raw.startswith(prefix):
                    hit = (prefix, key)
                    break
            if hit is None:
                self.notes.append(b.strip())
                continue
            prefix, key = hit
            tail = label_raw[len(prefix):].strip()
            value = (f"**{tail}** " if tail else "") + rest
            value = value.strip()
            if key in self.fields:
                self.notes.append(b.strip())
            else:
                self.fields[key] = value

    # -- derived views -----------------------------------------------------
    @property
    def claim(self):
        return self.fields.get("claim") or self.fields.get("finding")

    @property
    def tier(self):
        return self.fields.get("tier")

    @property
    def owner(self):
        return self.fields.get("owner")

    @property
    def attack(self):
        return self.fields.get("attack")

    @property
    def has_named_attack(self):
        return "attack" in self.fields

    def text_all(self):
        return self.body

    def path_tokens(self):
        toks = []
        for span in TICK_RE.findall(self.body):
            for t in PATHTOK_RE.findall(span):
                if t not in toks:
                    toks.append(t)
        return toks

    def quote_candidates(self):
        """Strings the manifest itself quotes, plus its backticked non-path spans.

        Both are candidates only.  Nothing here is written until it has been located
        inside the target file and the byte-exact substring recovered from it.
        """
        out = []
        # Every segment between two `"` characters, not only the ones a pairing
        # regex calls "quoted".  A short pair such as "the base" shifts every later
        # pair by one and silently loses the quotes after it — that bug cost three
        # anchors on the first run.  Over-generate here; the target file is the judge.
        for chunk in fold(self.body).split('"'):
            for seg in chunk.split("\n"):
                seg = seg.strip()
                if len(seg) >= MIN_ANCHOR_LEN and seg not in out:
                    out.append(seg)
        for span in TICK_RE.findall(self.body):
            span = span.strip()
            if PATHTOK_RE.search(span):
                continue
            if len(span) >= MIN_ANCHOR_LEN and span not in out:
                out.append(span)
        return sorted(out, key=lambda q: (-len(q), q))


def parse_entries(text: str):
    heads = list(ENTRY_RE.finditer(text))
    entries = []
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[start:end]
        # stop the last entry before the trailing section of the manifest
        cut = re.search(r"^(?:---\s*$|## )", body, re.M)
        if cut and i == len(heads) - 1:
            body = body[:cut.start()]
        entries.append(Entry(m.group(1), m.group(2).strip(), m.group(0), body))
    return entries


# ---------------------------------------------------------------------------
# 4 · Station tension.  If an entry resists its station, do not force it.
# ---------------------------------------------------------------------------

REG_RE = re.compile(r"\bD([0-6])\b")


def station_flags(entry: Entry, station_register: str, spine: str):
    flags = []
    regs = REG_RE.findall(entry.body)
    if spine == "ladder" and station_register.startswith("D") and regs:
        counts = {}
        for r in regs:
            counts["D" + r] = counts.get("D" + r, 0) + 1
        own = counts.get(station_register, 0)
        louder = sorted([(v, k) for k, v in counts.items() if v > own], reverse=True)
        if louder:
            top = louder[0]
            flags.append(
                f"register mention mismatch — stationed at {station_register}, but the "
                f"entry names {top[1]} {top[0]}× against {station_register} {own}×; the "
                f"station is kept and the mismatch is published rather than resolved")
    if spine == "method" and entry.tier and "[A]" in entry.tier:
        flags.append(
            "carries inherited `[A]` mathematics; the mathematics belongs to its owner "
            "and any ladder seat for it is a separate act this tree does not perform")
    if not entry.has_named_attack:
        flags.append(
            "no named attack — this entry carries a **Finding**, verified, in place of an "
            "*attack survived*; see the station note on how the survival test changes shape")
    return flags


# ---------------------------------------------------------------------------
# 5 · Anchors.
# ---------------------------------------------------------------------------

class AnchorLedger:
    def __init__(self, index: FileIndex):
        self.index = index
        self.rows = []

    def add(self, from_file, to_path, quote, resolved, kind):
        self.rows.append({
            "from_file": from_file,
            "to_path": to_path,
            "quote": quote,
            "resolved": bool(resolved),
            "_kind": kind,
        })

    def cite(self, from_file, token, quotes, want=MAX_ANCHORS_PER_TARGET):
        """Resolve one path token and attach up to `want` verified quotes.

        THE QUOTE PICKS THE FILE.  Every candidate path is tested against every
        candidate quote; the candidate in which the entry's own strings actually
        appear wins.  If no quote resolves in any candidate, the citation is
        DROPPED — never downgraded to a decorative pointer at the file's title —
        and the drop is written to the ledger with "resolved": false.
        """
        cands = self.index.resolve(token)
        if not cands:
            self.add(from_file, token, "", False, "unresolved-path")
            return [], token

        best_rel, best_hits, best_score = None, [], None
        for rel in cands:
            hits, seen = [], set()
            for q in quotes:
                exact, occ = self.index.locate(rel, q)
                if exact and exact not in seen:
                    seen.add(exact)
                    hits.append((occ == 1, len(exact), exact))
            hits.sort(key=lambda t: (not t[0], -t[1], t[2]))
            # more distinct hits wins; then more matched text; then the preferred lane
            score = (len(hits), sum(h[1] for h in hits),
                     -self.index.rank_of(token, rel))
            if best_score is None or score > best_score:
                best_rel, best_hits, best_score = rel, hits, score
            if best_hits and rel == cands[0]:
                break                        # the lane the manifest named carries the quote

        if len(cands) > 1:
            self.ambiguous = getattr(self, "ambiguous", [])
            self.ambiguous.append((from_file, token, best_rel, cands,
                                   bool(best_hits)))

        if not best_hits:
            self.add(from_file, best_rel or cands[0], "", False, "no-resolvable-quote")
            return [], (best_rel or cands[0])

        picked = [(best_rel, exact, "claim-quote") for _u, _l, exact in best_hits[:want]]
        for to_path, quote, kind in picked:
            self.add(from_file, to_path, quote, True, kind)
        return picked, None

    def cite_declared(self, from_file, candidates, want=1):
        """Take the first declared (path, quote) pairs that verify."""
        out = []
        for token, quote in candidates:
            cands = self.index.resolve(token)
            if not cands:
                self.add(from_file, token, quote, False, "unresolved-path")
                continue
            hit = None
            for rel in cands:
                exact, _occ = self.index.locate(rel, quote)
                if exact:
                    hit = (rel, exact)
                    break
            if hit:
                self.add(from_file, hit[0], hit[1], True, "claim-quote")
                out.append((hit[0], hit[1], "claim-quote"))
                if len(out) >= want:
                    break
            else:
                self.add(from_file, cands[0], quote, False, "quote-not-found")
        return out


# ---------------------------------------------------------------------------
# 6 · Rendering.
# ---------------------------------------------------------------------------

LAW_BLOCK = """> **The law of this tree.** Every citation below is `path` **plus an exact quoted
> string**, verified to appear in the target file before it was written. There are no
> line numbers anywhere in this tree, and there never will be. A quoted anchor survives
> insertion, reflow, frontmatter and reordering; a line number survives none of them.
> The corpus wrote this rule for itself and did not apply it to itself. This tree applies
> it from line one."""


def frontmatter(title, station, source_sha, source_date, extra=None):
    lines = [
        "---",
        f'title: "{title}"',
        f'station: "{station}"',
        'spine_law: "path + exact quoted string. No line numbers. Anywhere."',
        'status: "GENERATED — do not hand-edit. Change 01_PRESERVE.md or emit.py and re-run."',
        'generated_by: "16_THE_EMISSION/emit.py"',
        f'source: "{SOURCE_REL}"',
        f'source_sha256: "{source_sha}"',
        f"source_date: {source_date}",
        'frozen_tree: "01_EMERGENTISM is provenance and graveyard. Cited, never touched."',
    ]
    for k, v in (extra or {}):
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def render_provenance(ledger, rel, tail):
    """The Provenance block, with its citation of the source ANCHORED.

    `tail` is the file's own closing sentence and is left exactly as it was.
    """
    a = ledger.cite_declared(rel, SOURCE_ANCHOR_CANDIDATES, want=1)
    if a:
        p, q, _kind = a[0]
        head = (f"Generated from `{p}` — \"{q}\" — "
                f"by `16_THE_EMISSION/emit.py`. ")
    else:
        # No quote in the source verified. Say so; never write a bare pointer.
        head = (f"Generated from `{SOURCE_REL}` by `16_THE_EMISSION/emit.py` "
                f"— {{no-anchor}}: no string quoted from the source could be "
                f"located in it on this run, so no anchor was written. ")
    return ["## Provenance", "", head + tail, ""]


def render_anchor_list(picked, dropped):
    out = []
    if picked:
        out.append("- **Anchors** — `path` + exact quoted string, each verified present "
                   "in the target before it was written")
        for to_path, quote, _kind in picked:
            out.append(f'  - `{to_path}` — "{quote}"')
    else:
        out.append("- **Anchors** — none. Every candidate citation was dropped; see below.")
    if dropped:
        out.append(f"- ⚠️ **Citations dropped as unverifiable — {len(dropped)}** "
                   "(the manifest names these files; no string it quotes could be located "
                   "in them, so no anchor was written rather than an unverified one): "
                   + ", ".join(f"`{d}`" for d in dropped))
    return out


def render_entry(entry: Entry, picked_map, dropped, flags, spine, index, why=None):
    # Everything below that comes from the manifest is inherited prose and goes
    # through delocate() and requote(); the anchor list is MINTED and must not be
    # touched, its quotes being byte-exact substrings of the targets.
    d = lambda s: requote(delocate(s, entry.id), index, entry.id)
    out = [f"### {entry.id} · {d(entry.title)}", ""]
    if why:
        out += [f"*Why METHOD and not a rung.* {why}", ""]
    if entry.claim:
        label = "Claim" if "claim" in entry.fields else "Finding"
        out.append(f"- **{label}** {d(entry.claim)}")
    if entry.tier:
        out.append(f"- **Tier** {d(entry.tier)}")
    if entry.owner:
        out.append(f"- **Owner** {d(entry.owner)}")
    if entry.attack:
        out.append(f"- **The attack it survives** {d(entry.attack)}")
    for key, label in (("boundary", "Boundary"),
                       ("open", "OPEN — chair act"),
                       ("owner_boundary", "Owner boundary"),
                       ("separately", "Separately"),
                       ("genuine_defect", "The genuine defect")):
        if key in entry.fields:
            out.append(f"- **{label}** {d(entry.fields[key])}")
    for n in entry.notes:
        out.append(f"- {d(n)}")
    out += render_anchor_list(picked_map, dropped)
    for f in flags:
        out.append(f"- ⚠️ **Station tension** — {f}")
    out.append("")
    return out


def render_station(st, entries_by_id, ledger, source_sha, source_date, law_anchor):
    rel = st["file"]
    title = f'{st["mark"]}  {st["title"]}'
    out = [frontmatter(title, f'{st["mark"]} — {st["title"]}', source_sha, source_date,
                       extra=[("spine", '"A — THE LADDER (what is)"'),
                              ("entry_count", str(len(st["entries"])))]),
           "",
           f'# {st["mark"]}  —  {st["title"]}',
           "",
           LAW_BLOCK,
           ""]
    if law_anchor:
        p, q, _ = law_anchor[0]
        out += [f'The rule, in the corpus\'s own words — `{p}` — "{q}"', ""]
    out += ["## What this station is", "", st["is"], "",
            "## What does NOT belong here", "", st["not"], "",
            f'## The entries — {len(st["entries"])}', ""]

    all_flags = []
    for eid in st["entries"]:
        e = entries_by_id[eid]
        flags = station_flags(e, st["register"], "ladder")
        all_flags += [(eid, f) for f in flags]
        picked, dropped = [], []
        quotes = e.quote_candidates()
        for tok in e.path_tokens():
            got, drop = ledger.cite(rel, tok, quotes)
            picked += got
            if drop:
                dropped.append(drop)
        picked = [(SOURCE_REL, e.heading, "claim-quote")] + picked
        ledger.add(rel, SOURCE_REL, e.heading, True, "claim-quote")
        out += render_entry(e, picked, dropped, flags, "ladder", ledger.index)

    out += ["---", "",
            "## Escorted counts",
            "",
            "*DF-22 — the escorted number. Every figure here is produced by the command "
            "beside it, on every run.*",
            "",
            f'- entries at this station: **{len(st["entries"])}** — '
            "`python3 16_THE_EMISSION/emit.py --counts`",
            f"- station tensions flagged here: **{len(all_flags)}** — "
            "`python3 16_THE_EMISSION/emit.py --counts`",
            "- anchors written from this file: see `16_THE_EMISSION/ANCHORS.jsonl`, "
            f'`grep -c \'"from_file": "{rel}"\' 16_THE_EMISSION/ANCHORS.jsonl`',
            ""]
    out += render_provenance(
        ledger, rel,
        "The frozen tree was read and not written. Nothing was moved, deleted, "
        "committed or staged.")
    return "\n".join(out)


def render_d3(st, ledger, source_sha, source_date, law_anchor, d3_anchors, total_entries):
    rel = st["file"]
    out = [frontmatter("D3 — THE PROBABILITY-BEARING STATE (empty, and that is a result)",
                       "D3 — the probability-bearing state", source_sha, source_date,
                       extra=[("spine", '"A — THE LADDER (what is)"'),
                              ("entry_count", "0"),
                              ("empty", "true"),
                              ("empty_is", '"a result, not a gap"')]),
           "",
           "# D3  ·  THE PROBABILITY-BEARING STATE",
           "",
           "## This station is empty.",
           "",
           LAW_BLOCK,
           ""]
    if law_anchor:
        p, q, _ = law_anchor[0]
        out += [f'The rule, in the corpus\'s own words — `{p}` — "{q}"', ""]

    out += [
        "## The count, escorted",
        "",
        f"Of the **{total_entries}** entries in the manifest, **0** are stationed here. "
        "That is not an omission in this generator and it is not a queue. It is what the "
        "manifest contains.",
        "",
        "```",
        "python3 16_THE_EMISSION/emit.py --counts        # D3 → 0",
        "```",
        "",
        "## What this station would be",
        "",
        "The register of the probability-bearing state: the density operator and the Born "
        "rule, a state that carries distributions relative to a measurement context, sitting "
        "between configuration (D2) and the actual record (D4).",
        "",
        "## Why nothing survives here",
        "",
        "Three reasons, and they are independent. Any one of them alone would empty the "
        "station; all three hold.",
        "",
        "**1 · The formalism is inherited and its placement is an interpretation.** "
        "The density-operator/Born interface is not the corpus's — it is standard physics, "
        "carried at `[A/B]`. What the corpus contributed is the *decision to seat it at D3*, "
        "and that decision is tiered `[I]` by the corpus itself. An inherited formalism plus "
        "an interpretive placement yields nothing that can survive a hostile reader as a "
        "D3 claim: the attacker simply cites the physics, and the placement concedes.",
        "",
        "**2 · Both crossings that touch D3 are adjudicated FAILED.** `μ₂` is the crossing "
        "*into* D3 and `μ₃` is the crossing *out of* it. Both were ruled failed against the "
        "reducibility criterion by owner ruling, 2026-07-29 — and, decisively, **both failures "
        "survive a change of instrument.** A failure that survives a change of instrument is "
        "a result, not an artifact. D3 is therefore a station the ladder cannot be entered "
        "into or exited from by any crossing the corpus has established.",
        "",
        "**3 · The one candidate that would populate it is a conjecture.** The film-from-frames "
        "conjecture — that a saturated D3 description must additionally expose compatible "
        "transition amplitudes and an internal clock relation — is carried at `[C]`. A `[C]` "
        "is a thing to test, never a thing to publish as a station.",
        "",
        "**And the interpretations are removable by construction.** Everett has no fundamental "
        "collapse; Copenhagen-family actualisation is interpretation-specific; removing those "
        "sentences leaves every contract at D3, D4 and D5 unchanged. A layer whose removal "
        "changes nothing downstream is not load-bearing.",
        "",
        "## What does NOT belong here",
        "",
        "- **A D5 reading of a quantum alternative.** A D3 quantum alternative is not thereby "
        "a D5 modelled future. `μ₃` is an interface label, not a demonstrated collapse "
        "mechanism, and commitment is not quantum measurement.",
        "- **`φν = 1` as a Born normalisation.** The chart identity is never that.",
        "- **A placeholder.** This station is not reserved, not pending, and not a promise. "
        "If nothing comes, nothing comes.",
        "- **Content borrowed upward from D4.** An actual preparation, interaction, outcome "
        "token or record is D4. Moving one down here to fill the station would be exactly the "
        "kind of register-laundering the typing rule at METHOD, P-10, exists to stop.",
        "",
        "## What would have to change",
        "",
        "This station fills when — and only when — one of these lands. Each is a gate, "
        "published before the result exists:",
        "",
        "1. **A crossing is re-established.** `μ₂` or `μ₃` passes the reducibility criterion, "
        "or the criterion itself (HR-1, still open) is replaced by one they pass and that "
        "replacement is defended on its own terms rather than chosen because it lets them pass.",
        "2. **The film-from-frames conjecture is proved or killed.** Proved: D3 gains a claim "
        "with an owner. Killed: the station is empty for a fourth, stronger reason.",
        "3. **A D3 claim is produced that is not the inherited formalism** and that names the "
        "hostile reader it defeats — the same admission standard every other station on this "
        "ladder met.",
        "",
        "Until one of those happens, the honest publication of this register is this page.",
        "",
        "## Anchors",
        "",
    ]
    for p, q, kind in d3_anchors:
        out.append(f'- `{p}` — "{q}"')
    out += ["",
            "---",
            "",
            "## Escorted counts",
            "",
            "*DF-22 — the escorted number.*",
            "",
            f"- entries stationed at D3: **0** of **{total_entries}** — "
            "`python3 16_THE_EMISSION/emit.py --counts`",
            "- anchors written from this file: "
            f'`grep -c \'"from_file": "{rel}"\' 16_THE_EMISSION/ANCHORS.jsonl`',
            ""]
    out += render_provenance(
        ledger, rel, "The frozen tree was read and not written.")
    return "\n".join(out)


def render_method(entries_by_id, ledger, source_sha, source_date, law_anchor, counts):
    rel = METHOD_FILE
    out = [frontmatter("B — THE METHOD (how we know)", "METHOD — no station on the ladder",
                       source_sha, source_date,
                       extra=[("spine", '"B — THE METHOD (how we know)"'),
                              ("entry_count", str(len(METHOD_ENTRIES)))]),
           "",
           "# B  ·  THE METHOD — how we know",
           "",
           LAW_BLOCK,
           ""]
    if law_anchor:
        p, q, _ = law_anchor[0]
        out += [f'The rule, in the corpus\'s own words — `{p}` — "{q}"', ""]

    out += [
        "## What this spine is",
        "",
        f'Of the {counts["total"]} entries in the manifest, {counts["ladder"]} sit on the '
        f'ontological ladder and **{counts["method"]} do not.** These are the '
        f'{counts["method"]}.',
        "",
        "They are not a residue and they are not a lower tier. They are a **different kind "
        "of thing**: rules, gates, typings, registers, named defect shapes and archive "
        "protocols. A ladder is a ladder of *what is*. Method has no station on it, because "
        "method makes no claim about what is — it governs how claims about what is are "
        "admitted, tiered, cited, killed and kept findable.",
        "",
        "Putting them on the ladder would be the corpus's own signature error, performed by a "
        "generator: promoting a procedure to an ontology because it sits in a document that "
        "looks ontological. Two entries here are exactly that temptation. P-08 is called *the "
        "ontology answer* and its own §5 calls the standalone set a method, a posture, a vow "
        "and a geometry — *not yet a world-picture*. P-13 rules on the Foundation and demotes "
        "sphere primacy from primacy to selection. Both read like rungs. Neither is one.",
        "",
        "## What does NOT belong here",
        "",
        "- **Any claim about what exists.** If an entry asserts something about the world "
        "rather than about how the world may be claimed, it belongs on the ladder.",
        "- **A method that certifies its own success.** The efficacy claim for this protocol "
        "is `[C]` and has never been run as a controlled trial. That is stated in the method's "
        "own opening, and this spine does not improve on it.",
        "- **A gate used as a warrant.** Evidence that checking happened is not evidence that "
        "the checked claim is true. Two entries here (P-17, P-28) were flagged by a live gate "
        "and both were overturned in the artifact's favour — the gate was wrong, and the "
        "repair is scheduled against the gate, never against the fence.",
        "- **A silent tier upgrade.** When prose and tier disagree, the tier governs and the "
        "prose is read as invitation.",
        "- **Reflex elaboration.** *Shrink it before you reinvent it* — reflex elaboration "
        "after a failure is how bad ideas grow armour.",
        "",
        f"## The entries — {len(METHOD_ENTRIES)}",
        "",
    ]

    all_flags = []
    for eid in METHOD_ENTRIES:
        e = entries_by_id[eid]
        flags = station_flags(e, "METHOD", "method")
        all_flags += [(eid, f) for f in flags]
        picked, dropped = [], []
        quotes = e.quote_candidates()
        for tok in e.path_tokens():
            got, drop = ledger.cite(rel, tok, quotes)
            picked += got
            if drop:
                dropped.append(drop)
        picked = [(SOURCE_REL, e.heading, "claim-quote")] + picked
        ledger.add(rel, SOURCE_REL, e.heading, True, "claim-quote")
        out += render_entry(e, picked, dropped, flags, "method", ledger.index,
                            why=WHY_METHOD.get(eid))

    out += ["---", "",
            "## Escorted counts",
            "",
            "*DF-22 — the escorted number. This whole tree is written under it: re-run counts, "
            "never re-quote them.*",
            "",
            f'- entries on this spine: **{len(METHOD_ENTRIES)}** — '
            "`python3 16_THE_EMISSION/emit.py --counts`",
            f"- station tensions flagged here: **{len(all_flags)}** — "
            "`python3 16_THE_EMISSION/emit.py --counts`",
            "- anchors written from this file: "
            f'`grep -c \'"from_file": "{rel}"\' 16_THE_EMISSION/ANCHORS.jsonl`',
            ""]
    out += render_provenance(
        ledger, rel,
        "The frozen tree was read and not written. Nothing was moved, deleted, "
        "committed or staged.")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 7 · Build.  Pure: same inputs → byte-identical outputs.
# ---------------------------------------------------------------------------

def build():
    SCRUBBED.clear()          # build() is pure: two calls must report the same
    REQUOTED.clear()
    raw = SOURCE.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")
    m = re.search(r"^date:\s*(\S+)\s*$", text, re.M)
    source_date = m.group(1) if m else "unknown"

    entries = parse_entries(text)
    by_id = {e.id: e for e in entries}

    index = FileIndex(ROOT)
    ledger = AnchorLedger(index)

    stationed = []
    for st in LADDER_STATIONS:
        stationed += st["entries"]
    stationed += METHOD_ENTRIES

    counts = {
        "total": len(entries),
        "ladder": sum(len(s["entries"]) for s in LADDER_STATIONS),
        "method": len(METHOD_ENTRIES),
        "per_station": {s["key"]: len(s["entries"]) for s in LADDER_STATIONS},
        "unstationed": sorted(set(by_id) - set(stationed)),
        "duplicated": sorted({x for x in stationed if stationed.count(x) > 1}),
        "missing": sorted(set(stationed) - set(by_id)),
    }

    files = {}
    law_anchor_cache = {}

    for st in LADDER_STATIONS:
        rel = st["file"]
        law = ledger.cite_declared(rel, LAW_ANCHOR_CANDIDATES, want=1)
        law_anchor_cache[rel] = law
        if st["key"] == "d3":
            d3 = ledger.cite_declared(rel, D3_ANCHOR_CANDIDATES, want=len(D3_ANCHOR_CANDIDATES))
            files[rel] = render_d3(st, ledger, source_sha, source_date, law, d3,
                                   counts["total"])
        else:
            files[rel] = render_station(st, by_id, ledger, source_sha, source_date, law)

    law = ledger.cite_declared(METHOD_FILE, LAW_ANCHOR_CANDIDATES, want=1)
    files[METHOD_FILE] = render_method(by_id, ledger, source_sha, source_date, law, counts)

    anchor_lines = []
    for r in ledger.rows:
        anchor_lines.append(json.dumps(
            {"from_file": r["from_file"], "to_path": r["to_path"],
             "quote": r["quote"], "resolved": r["resolved"]},
            ensure_ascii=False))
    files[ANCHORS_REL] = "\n".join(anchor_lines) + "\n"

    return files, ledger, counts, entries, source_sha


# ---------------------------------------------------------------------------
# 8 · Report / write / verify.
# ---------------------------------------------------------------------------

def report(ledger, counts, entries, source_sha, files, mode):
    md_rows = [r for r in ledger.rows if r["resolved"]]
    bad = [r for r in ledger.rows if not r["resolved"]]
    targets = sorted({r["to_path"] for r in md_rows})

    print("=" * 72)
    print("THE EMISSION — run report")
    print("=" * 72)
    print(f"mode                     : {mode}")
    print(f"source                   : {SOURCE_REL}")
    print(f"source sha256            : {source_sha}")
    print(f"entries parsed           : {counts['total']}")
    print(f"  stationed on the ladder: {counts['ladder']}")
    print(f"  stationed as METHOD    : {counts['method']}")
    print(f"  unstationed            : {len(counts['unstationed'])} {counts['unstationed']}")
    print(f"  duplicated             : {len(counts['duplicated'])} {counts['duplicated']}")
    print(f"  named in map, missing  : {len(counts['missing'])} {counts['missing']}")
    print("per station              :")
    for st in LADDER_STATIONS:
        print(f"    {st['mark']:<3} {st['key']:<8} {counts['per_station'][st['key']]:>2}"
              f"   {', '.join(st['entries']) or '— EMPTY, and it says so —'}")
    print(f"    B   method   {counts['method']:>2}   {', '.join(METHOD_ENTRIES)}")
    print(f"files written            : {len(files)}")
    for k in sorted(files):
        print(f"    {k}")
    print(f"anchors emitted (written): {len(md_rows)}")
    print("  all of them claim-quote anchors: path + exact string, verified in target")
    print(f"  distinct target files  : {len(targets)}")
    print(f"  line numbers used      : 0   "
          "(`grep -cE ':[0-9]+' 16_THE_EMISSION/ANCHORS.jsonl` on the to_path field)")
    print(f"anchors FAILED to resolve: {len(bad)}   "
          "(written to ANCHORS.jsonl as resolved=false; NOT written into the markdown)")
    for r in bad:
        print(f"    [{r['_kind']}] {r['from_file']}")
        print(f"        -> {r['to_path']}  {(r['quote'][:66] + '…') if r['quote'] else ''}")
    amb = getattr(ledger, "ambiguous", [])
    unres = [a for a in amb if not a[4]]
    print(f"ambiguous path tokens    : {len(amb)}  "
          f"(disambiguated by quote: {len(amb) - len(unres)}; unresolved by quote: {len(unres)})")
    for f, tok, rel, cands, ok in amb:
        mark = "quote-picked" if ok else "NO QUOTE — citation dropped"
        others = [c for c in cands if c != rel][:4]
        print(f"    {tok}")
        print(f"        chose {rel}  [{mark}]  from {len(cands)}; "
              f"rejected: {', '.join(others)}{' …' if len(cands) - 1 > 4 else ''}")

    flags = []
    by_id = {e.id: e for e in entries}
    for st in LADDER_STATIONS:
        for eid in st["entries"]:
            for fl in station_flags(by_id[eid], st["register"], "ladder"):
                flags.append((eid, st["key"], fl))
    for eid in METHOD_ENTRIES:
        for fl in station_flags(by_id[eid], "METHOD", "method"):
            flags.append((eid, "method", fl))
    print(f"station tensions flagged : {len(flags)}")
    for eid, key, fl in flags:
        print(f"    {eid} @ {key}: {fl}")

    # The line-locator scrub, itemised.  This tree forbids line numbers; the
    # manifest it projects is full of them.  Every one that was dropped on the
    # way in is printed here, with the entry it came from and what replaced it,
    # so that "no line numbers anywhere in this tree" is a measured statement
    # and never a silent edit.
    print(f"line locators scrubbed   : {len(SCRUBBED)}")
    for where, was, now in SCRUBBED:
        print(f"    {where}: {was}  ->  {now}")

    # The inherited-quote repair, itemised.  Same discipline as the scrub: the
    # generator edited prose it copied, so every edit is printed with the file
    # the repaired string was verified against.  Nothing here is inferred — each
    # `now` is a byte-exact substring of the named target.
    print(f"inherited quotes repaired: {len(REQUOTED)}")
    for where, rel, was, now in REQUOTED:
        print(f"    {where} -> {rel}")
        print(f"        was: {was!r}")
        print(f"        now: {now!r}")
    print("=" * 72)


def write(files):
    for rel, content in sorted(files.items()):
        p = HERE / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")


def verify(files):
    same, diff, missing = [], [], []
    for rel, content in sorted(files.items()):
        p = HERE / rel
        if not p.exists():
            missing.append(rel)
        elif p.read_text(encoding="utf-8") == content:
            same.append(rel)
        else:
            diff.append(rel)
    print("-" * 72)
    print("BYTE-IDENTITY CHECK  (regenerate in memory, compare against disk)")
    for rel in same:
        print(f"  IDENTICAL  {rel}")
    for rel in diff:
        print(f"  DIFFERS    {rel}")
    for rel in missing:
        print(f"  MISSING    {rel}")
    ok = not diff and not missing
    print(f"  => {'byte-identical on re-run: YES' if ok else 'byte-identical on re-run: NO'}")
    print("-" * 72)
    return ok


def main():
    ap = argparse.ArgumentParser(description="Emit the two spines from 01_PRESERVE.md")
    ap.add_argument("--verify", action="store_true",
                    help="regenerate in memory and diff against what is on disk")
    ap.add_argument("--counts", action="store_true",
                    help="print the escorted counts and exit")
    args = ap.parse_args()

    files, ledger, counts, entries, sha = build()

    if args.counts:
        print(f"entries parsed: {counts['total']}")
        for st in LADDER_STATIONS:
            print(f"{st['mark']:<3} {st['key']:<8} {counts['per_station'][st['key']]}")
        print(f"B   method   {counts['method']}")
        return 0

    if args.verify:
        report(ledger, counts, entries, sha, files, "verify (no write)")
        return 0 if verify(files) else 1

    write(files)
    report(ledger, counts, entries, sha, files, "emit (written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
