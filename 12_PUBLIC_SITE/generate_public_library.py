#!/usr/bin/env python3
"""Generate the static public reading library from docs/handoff markdown.

The source bundle is intentionally stored outside 12_PUBLIC_SITE while it is a
handoff artifact. This generator turns the audited public bundle into served
HTML routes:

- /read/
- /papers/
- /canon/
- /foundations/
- /trinity/
- /formal/
- /paradox/
- /memetic/
- /rosettad/
- /operators/
- /will/
- /value/
- /ground/
- /sacred/

Run from the repository root or from 12_PUBLIC_SITE:
    python3 01_EMERGENTISM/12_PUBLIC_SITE/generate_public_library.py

STATUS 2026-06-10 — THE SOURCE BUNDLE IS ABSENT. `docs/handoff/*-public/` does not
exist in the tree, so this generator currently EXITS with "Missing public-library
source(s)" and CANNOT regenerate. The 308 generated pages under the wing routes are
therefore FROZEN ARTIFACTS, and canon-fidelity passes have HAND-PATCHED public surfaces
directly (the only available lever):

  - papers/paper-h-dimensional-cosmological/  : "S³ = S² × S¹" -> Hopf bundle over S²
        (fiber S¹), non-trivial. (The product form was pipeline-introduced; source is
        already correct — `PAPER_H...md` says "S³ as the Hopf bundle over S²".)
  - formal/17-efr-ontology-complete/          : added an R6 reconciliation note — the
        "all domains unified under one geometry (S²) / Theory of Everything" claim is
        register-dependent and partly refuted (R6, 2026-06-10); tier -> [C].
  - formal/33-nash-equilibrium-eta-zero/      : added the Green-Laffont (1977)
        impossibility caveat to the VCG trifecta; η=0 is a conditional/enforced
        equilibrium (AX4), not unconditional Nash.
  - formal/16-efr-transcendentals/            : added the 2026-06-12 model-shorthand
        boundary for Beauty, Truth, and Justice; the formulas are coordinate handles
        for asymptotic teleology, not metaphysical proofs; later tightened bare
        `P = 1` language to `P∞ = φ·ν = 1`.
  - value/01-transcendentals/                 : added 2026-06-12 as a hand-patched
        public bridge for objective teleology as asymptotic approach toward Beauty,
        Truth, and Justice.
  - formal/17-efr-ontology-complete/          : tightened moral/ethical formulas to
        `P_node,i` / `P_node,H` and changed bare `P = 1` value-language to `P∞`.
  - formal/08-efr-power-max-lemma/            : added the Syntropic Dyadism
        corollary linking individual symbiont, collective holobiont, durable
        world-line potential, and `P_node,i`/`P_node,H` under the existing
        Power-Max conditions; later mirrored stale generated proof notation
        from `Pᵢ` / `ΣP` to `P_node,i` / `ΣP_node`.
  - foundations/the-honest-position/, method/00-what-actually-tests-the-theory/,
        will/00-the-generative-lagrangian/     : downgraded Protocol D public
        wording from unconditional "multiplicative fitness generates
        cooperation" to the constrained Power-Max frontier: real coupling,
        multiplicative `P_node`, long horizon, and enforced `η = 0`; independent
        replication must test additive baselines and failure modes before any
        public evidence-tier upgrade; later added public Claim Boundary ledes
        and included foundations in the static RAG library index.
  - canon/the-ontology-index/                  : mirrored the same S15/S16
        downgrade in the empirical-program table so Protocol D and Agent V×Φ
        read as internally supportive framework-designed simulations, not
        confirmed public evidence.
  - trinity/22-the-teleology/, trinity/28-l4-star/, trinity/31-vmosk-as-applied-emergentism/
                                              : tightened bare `P = 1` wording to
        the current `P∞ = φ·ν = 1` manifold identity, with `B` / `P_node`
        named as the varying registers; later clarified "Tendency to Potential"
        as usable finite-node `P_node` under invariant `P∞`, not `P∞` growth.
  - trinity/14-tat-tvam-asi/, trinity/21-the-tightrope/,
        trinity/33-the-derivation/, trinity/34-research-brief-the-fork/,
        formal/14-efr-epistemology-triad/, formal/19-efr-geometric-exclusion/
                                              : tightened remaining bare `P = 1`
        wording into `P∞` for the manifold and `P_node` / `ΣP_node` for finite
        node or mesh capacity.
  - will/06-the-unsaid/, will/06a-what-remains-unseen/ : normalized the Nietzsche /
        Tendency-to-Potential public wording from bare `P` or `P∞`-as-potential
        into usable finite-node `P_node` under the invariant manifold identity.
  - trinity/13-the-wave-packet/               : tightened equipotentiality to
        `P∞ = φ·ν = 1` and removed ambiguous "maximum P" language.
  - trinity/03-the-closure/, trinity/06-the-cosmological-cycle/,
        trinity/18-the-strange-attractor/     : normalized pole/equator
        register language so pole reset is a singular ZSRE boundary, not
        ordinary `φ·ν != 1`, and `P∞ = 1` is the background manifold identity
        rather than the equator's distinguishing objective; later conditioned
        attractor/destiny language as model imagery, not proof of historical
        inevitability.
  - trinity/22-the-teleology/                 : conditioned remaining arc/future-pull
        rhetoric on coupling, memory, feedback, and `η = 0` correction dynamics;
        mirrored D4 usable-means / D5 worldline-foresight viability gloss; later
        downgraded literal force / reverse-arrow / "therefore helix spirals"
        language to model analogy and conditional correction dynamics.
  - teleology/                                : normalized the L1 public route so
        F5 is conditional selection toward viable completion under coupling,
        feedback, correction, and `η = 0`; disambiguated finite-node `V`
        from sphere-coordinate `ν`.
  - generated library chrome                 : added Game links to the topbar and
        library route row so every frozen corpus page exposes the Soul Loop's
        outward how-to-play surface; mirrored in this generator for the next
        successful handoff-bundle run.
  - trinity/10-the-soul-loop/                 : restored the public Goal / Ω framing
        in the Game Form and mirrored the D4 means / D5 worldline-foresight
        zero-factor examples while the source bundle is absent.
  - will/00-the-core-conjecture/              : mirrored the R6 objective/constraint
        reconciliation; replaced the withdrawn "reality maximizes balance" lead with
        viable completion as constrained option-cone widening under balance and
        non-extraction; later added the claim-boundary lead for constrained
        optimization and option-cone widening retrieval.
	  - value/00-objective-morals-and-ethics/    : added the claim-boundary lead that
	        disambiguates objective morality (`H -> i`), objective ethics (`i -> H`),
	        objective dharma, syntropic morality, and syntropic ethics under
	        `P_node,i` / `P_node,H`; later normalized the conditional is-ought
	        wording from closure to bypass and made the displayed Power-Max
	        condition include multiplicative `P_node`, long horizon, and enforced
	        `η = 0`.
  - value/00-the-good-the-evil-and-the-transcendentals/ : added the claim-boundary
        lead for knowledge of good and evil: good = both `P_node,i` and `P_node,H`
        rise under `η = 0`; evil = one side's apparent gain degrades the other;
        later replaced the older ethics-vs-morals compression with the two-layer
        grammar: objective morality is `H -> i`, objective ethics is `i -> H`,
        and local codes are implementation attempts.
  - trinity/15-dharma-yuddha/                : added the claim-boundary lead for
        Krishna, Gita, flow state, objective dharma, and Krishna's army test so
        the public RAG lede exposes the already-source-backed L4 flow reading;
        later normalized the stale "Maximum P" / "L4 is the apex" wording to
        `B = 1`, finite-node `P_node`, and a non-hierarchical balance apex.
  - formal/22-power-max-demonstration/, formal/24-geometric-exclusion-convergence/,
        formal/41-unified-dimensional-derivation/ : added the 2026-06-12 A7
        boundary that the Nash/dominant-strategy results are balance-only or
        equatorial-profile model results, not unconditional social theorems;
        real institutions require enforcement, monitoring, due process, and exit;
        later clarified that `B` is maximized by the payoff model, not the global
        objective outside that narrow game.
  - ground/00-the-ring-that-is-the-ground/, foundations/the-ring-that-is-the-ground/,
        value/00-commandment-vs-geometry/, foundations/commandment-vs-geometry/,
        formal/09-efr-godel-clarification/, formal/10-efr-mu-limit-formula/,
        formal/11-efr-triadic-stability/ : tightened Power-Max link labels and
        Tolkien/ring extraction language so "cooperation theorem" means the
        conditional theorem under coupling, horizon, multiplicative `P_node`,
        and enforced `η = 0`, not an unconditional proof that extraction can
        never pay locally.
  - value/00-theurgy-and-f5-force-map/          : added the will boundary:
        will is disciplined selection/construction of reachable futures under
        reciprocal closure, `η = 0`, and evidence tiers; it is not magic,
        coercive authority, external-being invocation, or proof of cosmic will.
  - sacred/00-glossary/                         : added the disciplined public
        translation of "become as gods" and the will glossary row.
  - meta/00-the-remaining-questions/            : normalized the practical
        Dasein action test from stale `P_i` / `P_H` to `P_node,i` /
        `P_node,H` so the remaining-questions public echo matches the
        Goal/Soul Loop/syntropic-dyad spine.
  - will/00-a-square-cannot-be-negative/, trinity/31-vmosk-as-applied-emergentism/,
        trinity/33-the-derivation/              : normalized `ν` action-language
        from generic capacity to usable D4 means-to-act, matching the D4/D5
        Goal/Game/Soul Loop distinction.
  - will/00-the-generative-lagrangian/          : normalized the fitness-function
        specification so finite-node `P_node = Φ × V` is the action score,
        `P∞ = φ·ν = 1` remains the manifold identity, and `B` is the
        equatorial admissibility / balance function rather than a hidden
        maximized product.
	  - formal/34-d4-d5-canonical-reference/        : added the register bridge that
	        keeps dimensional D4 witness distinct from action-register D4 means-to-act
	        and pairs D5 worldline-foresight with D4 means in `P_node = Φ × V`.
	  - foundations/ontology-across-dimensions/, ground/00-ontology-across-dimensions/
	                                              : mirrored the D4/D5 action-register
	        bridge into the full ontological compression, so D4 is witness plus
	        means-to-act and D5 is agentic present plus worldline-foresight instead of
	        passive witness versus disembodied agency.
	  - formal/08-efr-power-max-lemma/              : tightened the status from
	        pure geometric theorem to conditional model theorem / design lemma,
	        and added the `W_i(T)` / `P_node,H` worldline notation for the
	        symbiont-holobiont corollary.
	  - sacred/00-glossary/, formal/29-primitives-and-type-signatures/,
	        formal/30-operational-definitions/, trinity/31-vmosk-as-applied-emergentism/,
	        trinity/33-the-derivation/, will/00-a-square-cannot-be-negative/,
	        will/05-exhaustive-observations/, formal/25-steel-thread/
	                                              : normalized downstream Φ/V definitions
	        to the action-register bridge (`Φ` as D5 worldline-foresight, `V` as
	        D4 means-to-act) and bounded old "extraction is negative-sum" slogans
	        to the equatorial balance/displacement model, not unconditional
	        one-shot payoff claims.
  - value/                                      : mirrored the Dasein moral-compass
        route summary from the source axiology route: objective morality is
        `H -> i`, objective ethics is `i -> H`, objective dharma is both
        directions rising together, and the Power-Max claim is conditional on
        real coupling, multiplicative `P_node`, long horizon, and enforced
        `η = 0`, not external moral realism.
	  - sacred/00-glossary/, formal/14-efr-epistemology-triad/,
	        formal/17-efr-ontology-complete/,
	        formal/34-d4-d5-canonical-reference/, dasein/,
	        complete-ontology/, canon/the-complete-ontology-of-reality/,
	        geometric-ontology/, canon/the-geometric-ontology-of-reality/
	                                              : fenced stale "D5 = Consciousness"
	        phrasing so D5 is agency / selection / worldline-foresight first, and
	        consciousness is only the `[I]` lived-interior reading of selection, not
	        proof of a separate physical layer or the Ground itself; later mirrored
	        the action-register bridge into canon/the-ontology-index,
	        canon/the-complete-ontology-of-reality, and complete-ontology so D4
	        means-to-act and D5 worldline-foresight are practical `P_node = Φ × V`
	        factors, not replacements for the dimensional scaffold.
	  - dasein/, papers/paper-vi-emergence-as-lens-on-dasein/
	                                              : added the Soul Loop practice
	        bridge for Dasein-as-reader: ontology, epistemology, methodology,
	        axiology, and teleology cycle until finite-node action couples `Φ`
	        as D5 worldline-foresight with `V` as D4 means-to-act, raising
	        `P_node,i` and `P_node,H` together under `η = 0`; later normalized
	        the Dasein non-reduction clause so the D5 μ-limit is agency /
	        selection first, with consciousness as the `[I]` lived reading and
	        quantum-collapse resonance left `[C]`.
	  - trinity/03-the-closure/, trinity/06-the-cosmological-cycle/,
	        trinity/simulation-spec/, trinity/22-the-teleology/
	                                              : fenced remaining Trinity compatibility
	        "D5 = Consciousness" phrasing so D5 is agency / selection first,
	        with consciousness only as the `[I]` lived-interior reading of that
	        register rather than a separate physics layer.
	  - memetic/                                    : normalized the Dasein game
	        reading action test from stale `P_i` / `P_H` to `P_node,i` /
        `P_node,H`; later added the public memetics operational-language guard
        and hand-patched files 04-06 so "defense," "firewall," "hardening,"
        "egregore," and "AIA" remain proposal/model language rather than
        medical advice, coercive authority, censorship authority, or deployed
        runtime protection.
  - operators/mf-294-egregores-are-horn-networks/
                                              : normalized carrier/network
        product notation from generic `P_i` / `P_individual` to finite-node
        `P_node,i` / `P_node,individual`; later normalized the DAC objective
        from bare "maximise P" to carrier-network `P_node`, and renamed the
        internet/pre-internet network variables to `P_node,internet` /
        `P_node,pre-internet`.
  - operators/mf-292-the-bekenstein-ceiling/  : normalized remaining finite-node
        product prose from bare "total/local/minimum P" to `P_node`.
  - operators/mf-290-the-ektropic-radius-v2/, operators/mf-70-kali-closes-sphere/
                                              : normalized remaining live
        operator-route "maximum P" prose to finite-node `P_node` or explicit
        `B` / `P_node` objective language.
  - operators/mf-299-hawking-radiation-is-a7/ : demoted stale universal A7
        wording from "DISCOVERY about how reality operates at every scale" and
        "patient but inevitable" to a tiered Hawking/A7 analogy: black-hole
        physics remains model-theoretic physics; A7 remains a framework axiom;
        the cross-scale universality reading is `[I/C]` / `[C]`, not `[A]`.
  - trinity/22-the-teleology/, trinity/35-research-brief-teleology-spectrum/,
        will/03-why-the-constraint-matters/, canon/the-complete-ontology-of-reality/,
        formal/41-unified-dimensional-derivation/ : normalized attractor language
        so the equator is the structural balance optimum and becomes an attractor
        only under specified flow, feedback, coupling, and correction dynamics;
        later normalized "ektropic hand selects for balance" to viable completion
        / usable option-cone widening under balance and `eta = 0` constraints;
        later replaced "what pulls it?" public/source teleology language with
        correction dynamics plus Soul Loop, keeping the equator as feasibility
        surface rather than objective.
  - paradox/pd-10-is-ought/ and will/l1-l7-refinement-audit/
                                              : normalized the Is-Ought / Power-Max
        claim from unconditional "extraction is dominated" or "the gap closes"
        language to the conditional register: real coupling, multiplicative
        `P_node`, long horizon, enforceable `η = 0`, and no hidden extraction
        channel.
  - trinity/20-the-hybrid-sovereign/, trinity/23-the-dac/,
        operators/mf-299-hawking-radiation-is-a7/, will/06-the-unsaid/
                                              : normalized deterministic
        "inevitable / demands / enforces" teleology language to conditional
        selection pressure, asymptotic correction, or proposed repair language
        under coupling, feedback, correction, provenance, and `η = 0`.
  - foundations/the-honest-position/          : normalized the canonical framing
        rule from stale six-function vocabulary to the current five Knows plus
        Rosetta Soul Loop wording while the generated route remains frozen.
  - about/, trinity/10-the-soul-loop/, trinity/39-neoteny-as-f5-delay-and-cultural-womb/
                                              : mirrored the constrained
        Power-Max frontier wording from the Goal/Soul Loop source:
        durable `W_i(T)` is searched only where `P_node,H` is preserved or
        raised under `eta = 0`; strict syntropy is both `P_node,i` and
        `P_node,H` rising together.
  - canon/the-generative-table/, foundations/the-seven-ologies-per-the-rosetta/,
        rosettad/00-the-seven-ologies-per-the-rosetta/,
        operators/mf-285-dreams-are-unanchored-d5/
                                              : normalized L7 stereographic
        ratio notation from action-register uppercase Phi-over-V to sphere-chart
        `z = φ/ν`, preserving uppercase `Φ × V` for finite-node `P_node`.
  - formal/12-efr-extraction-coefficient/    : normalized the M-axis connection
        row from bare `P` to finite-node `P_node`, with `P∞ = φ·ν = 1`
        preserved as the background manifold identity rather than a variable
        harm target.
  - operators/mf-68-area-measure/             : renamed the legacy local value
        function from bare `P(θ)` to projected `P_band(θ)` so the area-measure
        derivation does not compete with `P∞` or finite-node `P_node`.

BEFORE ANY FUTURE REGEN: restore the handoff bundle AND apply these same
corrections to the SOURCE markdown (formal-16 / formal-17 / formal-33 /
formal-08 / formal-22 / formal-24 / formal-41 / trinity-03 / trinity-06 /
trinity-13 / trinity-18 / paper-H /
teleology core-conjecture public bundle
files, plus axiology-public objective-morals-and-ethics and good/evil public
bundle files, plus trinity-public dharma-yuddha, plus the ring/commandment and
formal-09/10/11 Power-Max label public bundles, plus theurgy-public and
glossary-public will/become-as-gods bundles, plus meta-public
remaining-questions, plus memetic-public, paradox-public PD_10_IS_OUGHT,
teleology-public L1_L7_REFINEMENT_AUDIT, glossary-public, formal-public 25/29/30,
formal-public 12, trinity-public 31/33,
teleology-public 00_A_SQUARE/05_EXHAUSTIVE_OBSERVATIONS, and operators-public
MF-68/MF-290/MF-292/MF-294/MF-70), or this generator will overwrite
the hand-patches and reintroduce the over-claims. Also fix the title-doubling: when a source heading already ends in
"— Emergentism", `page_shell(title=...)` appends a second one.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote

import markdown


SITE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SITE_ROOT.parents[1]
HANDOFF = REPO_ROOT / "docs" / "handoff"
BRANCH = os.environ.get("EMERGENTISM_SOURCE_BRANCH", "main")
GITHUB_ROOT = f"https://github.com/Menexus-GmbH/magnum-opus/blob/{BRANCH}"
SITE_BASE_URL = "https://www.emergentism.org/"

WINGS = {
    "papers": {
        "source_dir": HANDOFF / "papers-public",
        "title": "The Papers",
        "description": "Twenty-four tiered papers with falsifiers and source boundaries.",
        "active": "papers",
    },
    "canon": {
        "source_dir": HANDOFF / "canon-public",
        "title": "Framework Canon",
        "description": "The constitution, cosmology, master table, and public edition book.",
        "active": "canon",
    },
    "foundations": {
        "source_dir": HANDOFF / "ology-public",
        "title": "The Seven -ologies",
        "description": "Foundational texts across Teleology, Epistemology, Axiology, Ontology, Theology, and Rosetta.",
        "active": "foundations",
    },
    "trinity": {
        "source_dir": HANDOFF / "trinity-public",
        "title": "The Transcendental Trinity",
        "description": "The framework's book-length narrative cosmology — D0→D6 as living story.",
        "active": "trinity",
    },
    "formal": {
        "source_dir": HANDOFF / "formal-public",
        "title": "The Formal System",
        "description": "Axioms, derivations, and proofs — the checkable scaffolding beneath the Papers.",
        "active": "formal",
    },
    "paradox": {
        "source_dir": HANDOFF / "paradox-public",
        "title": "Paradox Dissolutions",
        "description": "Twenty-six classical paradoxes dissolved through the framework's lens — each with its evidence tier and kill-criterion.",
        "active": "paradox",
    },
    "memetic": {
        "source_dir": HANDOFF / "memetic-public",
        "title": "Memetics",
        "description": "Memes as hardware/software conflict — standalone citation-grade essays.",
        "active": "memetic",
    },
    "rosettad": {
        "source_dir": HANDOFF / "rosetta-d-public",
        "title": "Rosetta D-Series",
        "description": "Cross-domain evidence and translation tables — the framework's interdisciplinary audit wing.",
        "active": "rosettad",
    },
    "operators": {
        "source_dir": HANDOFF / "operators-public",
        "title": "Operators",
        "description": "Twenty-nine mathematical operator derivations — physical, geometric, and formal mappings of the framework to established scientific domains.",
        "active": "operators",
    },
    "will": {
        "source_dir": HANDOFF / "teleology-public",
        "title": "Teleology",
        "description": "The doctrine of ends — thirty documents on the fifth force, the generative Lagrangian, and the hidden center of the framework.",
        "active": "will",
    },
    "value": {
        "source_dir": HANDOFF / "axiology-public",
        "title": "Axiology",
        "description": "The doctrine of value — ten documents on ethics, rights, teleological limits, theurgy, and the bridge between levels.",
        "active": "value",
    },
    "ground": {
        "source_dir": HANDOFF / "ontology-public",
        "title": "Ontology",
        "description": "The doctrine of being — nine documents on finity, the syncretic map, apophatic ground, and the ring that is the ground.",
        "active": "ground",
    },
    "sacred": {
        "source_dir": HANDOFF / "theology-public",
        "title": "Theology",
        "description": "The doctrine of the sacred — six documents on pedagogy, reconciliation, symbol design, and truth order.",
        "active": "sacred",
    },
    "method": {
        "source_dir": HANDOFF / "method-public",
        "title": "Method",
        "description": "The doctrine of method — ten documents on axioms, the doctrinal ladder, testing, preregistrations, and the Anumana audit protocol.",
        "active": "method",
    },
    "meta": {
        "source_dir": HANDOFF / "meta-public",
        "title": "Meta",
        "description": "Framework meta-documents — six documents on what is novel, what remains open, and how the corpus is organized.",
        "active": "meta",
    },
}

GENERATED_DIRS = [SITE_ROOT / "read", SITE_ROOT / "papers", SITE_ROOT / "canon", SITE_ROOT / "foundations", SITE_ROOT / "trinity", SITE_ROOT / "formal", SITE_ROOT / "paradox", SITE_ROOT / "memetic", SITE_ROOT / "rosettad", SITE_ROOT / "operators", SITE_ROOT / "will", SITE_ROOT / "value", SITE_ROOT / "ground", SITE_ROOT / "sacred", SITE_ROOT / "method", SITE_ROOT / "meta"]
EXCLUDED_PUBLIC_SOURCE_NAMES = {"README.md", "AGENTS.md", "CLAUDE.md"}


def is_public_document(source: Path) -> bool:
    return source.suffix == ".md" and source.name not in EXCLUDED_PUBLIC_SOURCE_NAMES and not source.name.startswith("_")


def slug_for(path: Path) -> str:
    return path.stem.lower().replace("_", "-")


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :].lstrip()


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def output_dir_for(source: Path) -> Path:
    source = source.resolve()
    if source == (HANDOFF / "00_READ_THE_FRAMEWORK.md").resolve():
        return SITE_ROOT / "read"
    for route, config in WINGS.items():
        src_dir = config["source_dir"].resolve()
        if source == (src_dir / "README.md").resolve():
            return SITE_ROOT / route
        if source.parent.resolve() == src_dir and is_public_document(source):
            return SITE_ROOT / route / slug_for(source)
    raise KeyError(f"No output route for {source}")


def build_source_map() -> dict[Path, Path]:
    mapping: dict[Path, Path] = {
        (HANDOFF / "00_READ_THE_FRAMEWORK.md").resolve(): SITE_ROOT / "read",
    }
    for route, config in WINGS.items():
        src_dir = config["source_dir"]
        mapping[(src_dir / "README.md").resolve()] = SITE_ROOT / route
        for source in sorted(src_dir.glob("*.md")):
            if not is_public_document(source):
                continue
            mapping[source.resolve()] = SITE_ROOT / route / slug_for(source)
    return mapping


SOURCE_TO_OUTPUT = build_source_map()


def rel_href(from_file: Path, target_dir: Path, anchor: str = "") -> str:
    href = os.path.relpath(target_dir, from_file.parent).replace(os.sep, "/")
    if href == ".":
        href = "."
    return f"{href}/{anchor}"


def github_href(target: Path, anchor: str = "") -> str:
    rel = target.resolve().relative_to(REPO_ROOT).as_posix()
    return f"{GITHUB_ROOT}/{quote(rel)}{anchor}"


LINK_RE = re.compile(r"(\[[^\]]+\]\()([^)\s]+)(#[^)]+)?(\))")
TIER_MARKER_RE = re.compile(r"\[([ABCSIDET](?:/[ABCSIDET])*)\]")

LEGACY_TIER_MAP = {
    "E": "A",
    "T": "S",
}


def rewrite_markdown_links(text: str, source: Path, output_file: Path) -> str:
    source = source.resolve()

    def replace(match: re.Match[str]) -> str:
        prefix, url, anchor, suffix = match.groups()
        anchor = anchor or ""
        if url.startswith(("http://", "https://", "mailto:", "#", "data:")):
            return match.group(0)
        if url.startswith("/"):
            return match.group(0)

        raw_target = (source.parent / url).resolve()
        if raw_target.is_dir():
            raw_target = (raw_target / "README.md").resolve()
        if raw_target in SOURCE_TO_OUTPUT:
            return f"{prefix}{rel_href(output_file, SOURCE_TO_OUTPUT[raw_target], anchor)}{suffix}"
        if raw_target.exists():
            return f"{prefix}{github_href(raw_target, anchor)}{suffix}"
        fallback = rel_href(output_file, SITE_ROOT / "sources")
        return f"{prefix}{fallback}{suffix}"

    return LINK_RE.sub(replace, text)


def uses_operator_tier_policy(source: Path) -> bool:
    try:
        return source.resolve().is_relative_to((HANDOFF / "operators-public").resolve())
    except AttributeError:
        operator_root = (HANDOFF / "operators-public").resolve()
        try:
            source.resolve().relative_to(operator_root)
        except ValueError:
            return False
        return True


def normalize_legacy_operator_tiers(text: str) -> str:
    """Render operator handoff tiers through the current [A/B/S/I/D/C] ladder."""

    def replace_marker(match: re.Match[str]) -> str:
        tiers = match.group(1).split("/")
        normalized = []
        for tier in tiers:
            mapped = LEGACY_TIER_MAP.get(tier, tier)
            if mapped not in normalized:
                normalized.append(mapped)
        return "[" + "/".join(normalized) + "]"

    text = TIER_MARKER_RE.sub(replace_marker, text)
    text = text.replace("[E for", "[A for")
    text = text.replace("; E for", "; A for")
    text = text.replace(", E for", ", A for")
    text = text.replace("[T for", "[S for")
    text = text.replace("; T for", "; S for")
    text = text.replace(", T for", ", S for")
    return text


def render_markdown(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "toc"],
        output_format="html5",
    )


def prefix_for_depth(depth: int) -> str:
    return "../" * depth


def topbar(active: str, depth: int) -> str:
    prefix = prefix_for_depth(depth)
    items = [
        ("0", "0/"),
        ("1", "1/"),
        ("2", "2/"),
        ("3", "3/"),
        ("4", "4/"),
        ("5", "5/"),
        ("6", "6/"),
        ("R", "rosetta/"),
        ("S", "soul-loop/"),
        ("Game", "game/"),
        ("A", "atlas/"),
        ("Read", "read/"),
    ]
    links = "\n    ".join(
        f'<a href="{html.escape(prefix + href)}">{html.escape(label)}</a>'
        for label, href in items
    )
    return f"""
<header class="topbar">
  <a class="brand" href="{prefix}">Emergentism</a>
  <nav class="number-nav" aria-label="Public doctrine routes">
    {links}
  </nav>
</header>
"""


def public_footer(depth: int) -> str:
    return """
  <footer class="site-footer">
    <div class="phi">⊙ = • × ○</div>
    <p>Public doctrine surface · evidence tiers preserved</p>
  </footer>
"""


def page_html(
    *,
    title: str,
    description: str,
    body: str,
    active: str,
    depth: int,
    source_label: str,
    extra_kicker: str = "Public reading library",
) -> str:
    prefix = prefix_for_depth(depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} — Emergentism</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="data:,">
<link rel="stylesheet" href="{prefix}assets/css/xai.css">
</head>
<body>
{topbar(active, depth)}
<main class="library-shell">
  <section class="library-hero">
    <div class="evidence">{html.escape(extra_kicker)}</div>
    <h1>{html.escape(title)}</h1>
    <p>{html.escape(description)}</p>
    <div class="library-route-row">
      <a href="{prefix}read/">Read</a>
      <a href="{prefix}game/">Game</a>
      <a href="{prefix}papers/">Papers</a>
      <a href="{prefix}canon/">Canon</a>
      <a href="{prefix}foundations/">Foundations</a>
      <a href="{prefix}trinity/">Trinity</a>
      <a href="{prefix}formal/">Formal</a>
      <a href="{prefix}paradox/">Paradox</a>
      <a href="{prefix}memetic/">Memetic</a>
      <a href="{prefix}rosettad/">Rosetta D</a>
      <a href="{prefix}operators/">Operators</a>
      <a href="{prefix}will/">Teleology</a>
      <a href="{prefix}value/">Axiology</a>
      <a href="{prefix}ground/">Ontology</a>
      <a href="{prefix}sacred/">Theology</a>
      <a href="{prefix}method/">Method</a>
      <a href="{prefix}meta/">Meta</a>
      <a href="{prefix}sources/">Sources</a>
    </div>
  </section>
  <article class="library-article">
    {body}
  </article>
  <aside class="library-meta">
    <span>[S] / [I] public rendered prose</span>
    <span>Source: {html.escape(source_label)}</span>
    <span>Generated by 12_PUBLIC_SITE/generate_public_library.py</span>
  </aside>{public_footer(depth)}
</main>
</body>
</html>
"""


def write_page(output_dir: Path, source: Path, active: str, title_fallback: str, description: str, depth: int) -> None:
    source_text = strip_frontmatter(source.read_text(encoding="utf-8"))
    if uses_operator_tier_policy(source):
        source_text = normalize_legacy_operator_tiers(source_text)
    title = first_heading(source_text, title_fallback)
    output_file = output_dir / "index.html"
    markdown_text = rewrite_markdown_links(source_text, source, output_file)
    body = render_markdown(markdown_text)
    source_label = source.relative_to(REPO_ROOT).as_posix()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        page_html(
            title=title,
            description=description,
            body=body,
            active=active,
            depth=depth,
            source_label=source_label,
        ),
        encoding="utf-8",
    )


def clean_generated_dirs() -> None:
    for path in GENERATED_DIRS:
        if path.exists():
            shutil.rmtree(path)


def generate_library() -> None:
    clean_generated_dirs()
    write_page(
        SITE_ROOT / "read",
        HANDOFF / "00_READ_THE_FRAMEWORK.md",
        "read",
        "Read the Framework",
        "The complete public reading path through the rendered Emergentism corpus.",
        depth=1,
    )
    for route, config in WINGS.items():
        src_dir = config["source_dir"]
        write_page(
            SITE_ROOT / route,
            src_dir / "README.md",
            config["active"],
            config["title"],
            config["description"],
            depth=1,
        )
        for source in sorted(src_dir.glob("*.md")):
            if not is_public_document(source):
                continue
            write_page(
                SITE_ROOT / route / slug_for(source),
                source,
                config["active"],
                source.stem.replace("_", " ").title(),
                config["description"],
                depth=2,
            )


def generate_manifest() -> None:
    documents = []
    for section, config in WINGS.items():
        src_dir = config["source_dir"]
        for source in sorted(src_dir.glob("*.md")):
            if not is_public_document(source):
                continue
            source_text = strip_frontmatter(source.read_text(encoding="utf-8"))
            route_dir = SOURCE_TO_OUTPUT[source.resolve()]
            documents.append(
                {
                    "section": section,
                    "title": first_heading(source_text, source.stem.replace("_", " ").title()),
                    "href": route_dir.relative_to(SITE_ROOT).as_posix() + "/",
                    "source": source.relative_to(REPO_ROOT).as_posix(),
                }
            )

    manifest = {
        "generated_by": "01_EMERGENTISM/12_PUBLIC_SITE/generate_public_library.py",
        "source_snapshot": "2026-06-07 public handoff bundle",
        "source_bundle": "docs/handoff",
        "routes": {
            "read": "read/",
            "papers": "papers/",
            "canon": "canon/",
            "foundations": "foundations/",
            "trinity": "trinity/",
            "formal": "formal/",
            "paradox": "paradox/",
            "memetic": "memetic/",
            "rosettad": "rosettad/",
            "operators": "operators/",
            "will": "will/",
            "value": "value/",
            "ground": "ground/",
            "sacred": "sacred/",
            "method": "method/",
            "meta": "meta/",
        },
        "documents": documents,
    }
    (SITE_ROOT / "reading-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def url_for_html(rel: Path) -> str:
    rel_posix = rel.as_posix()
    if rel_posix == "index.html":
        path = ""
    elif rel.name == "index.html":
        path = rel.parent.as_posix().rstrip("/") + "/"
    else:
        path = rel_posix
    return SITE_BASE_URL + path


def generate_support_files() -> None:
    html_files = []
    for path in SITE_ROOT.rglob("*.html"):
        rel = path.relative_to(SITE_ROOT)
        rel_parts = set(rel.parts)
        if {".vercel", "__pycache__", "node_modules", "partials", "vendor"} & rel_parts:
            continue
        html_files.append(rel)
    html_files = sorted(html_files)

    urls = "\n".join(
        f"  <url><loc>{html.escape(url_for_html(rel))}</loc></url>" for rel in html_files
    )
    (SITE_ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""",
        encoding="utf-8",
    )
    (SITE_ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /

Sitemap: {SITE_BASE_URL}sitemap.xml
""",
        encoding="utf-8",
    )


def main() -> None:
    required = [HANDOFF / "00_READ_THE_FRAMEWORK.md"]
    required.extend(config["source_dir"] / "README.md" for config in WINGS.values())
    missing = [path for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing public-library source(s): " + ", ".join(str(p) for p in missing))
    generate_library()
    generate_manifest()
    generate_support_files()
    generated = ", ".join(["read", *WINGS.keys()])
    print(f"Generated public library routes under 12_PUBLIC_SITE/{generated}")


if __name__ == "__main__":
    main()
