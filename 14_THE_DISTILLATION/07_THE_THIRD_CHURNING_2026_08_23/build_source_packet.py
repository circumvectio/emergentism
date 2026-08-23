#!/usr/bin/env python3
"""Build the canonical Third Churning data from one frozen source state.

This builder owns only files in this source packet's ``data/`` directory and
``ThirdChurningCorpus.v1.json``. It never writes public pages.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = HERE / "data"
FROZEN = "8b07e00c563f338923b1928d3469c862d44c1e07"
OWNER_DIRECTION = "00_HANDOFF/EMERGENTISM_ORG_V2_3_THIRD_CHURNING_OWNER_DIRECTION_2026_08_23.md"
CONTRACTS = {
    "drop": HERE / "contracts" / "ChurningDrop.v1.schema.json",
    "problem": HERE / "contracts" / "ProblemAdjudication.v1.schema.json",
    "corpus": HERE / "contracts" / "ThirdChurningCorpus.v1.schema.json",
}

SOURCES = {
    "one": ("00_THE_WELTANSCHAUUNG_ONE_SITTING.md", "925a71453163d0a23e44c84cf023249014f71dfa99f45969d7a2bdd8d31c9bb0"),  # pragma: allow-secret
    "cards": ("00_META/00_ONE_SITTING_CLAIM_CARD_SET_01.md", "5561c22d78be84040e15e25b420bfe201edf49cb251ba5c2fad9b331a3fca536"),  # pragma: allow-secret
    "second": ("14_THE_DISTILLATION/00_THE_AMRITA.md", "dce26b620dfa9b30eee9880c85c6204f1aa3dc3ce6b281ae50ce55109067e97f"),  # pragma: allow-secret
    "dead": ("14_THE_DISTILLATION/04_WHAT_DIED.md", "2753cfc380135cc842bff68ca865ee70a38cdd772486dc7b1e9484802c458d84"),  # pragma: allow-secret
    "method": ("14_THE_DISTILLATION/05_THE_METHOD.md", "14c3b11399c931226129b4c186beb4c80da4f38e8b5bdddcbdf61cff576d78da"),  # pragma: allow-secret
    "pqa": ("03_METHODOLOGY/03_PREREGISTRATIONS/pqa_54/prompts/questions.json", "1ea31b71c52c274960af9361994d77f0b849eee2579610822c25293a99280250"),  # pragma: allow-secret
    "pqa_projection": ("03_METHODOLOGY/03_PREREGISTRATIONS/pqa_54/public_projection.json", "fad9e470f95bca53c8c77023004020719196271d51ae05a3ff74a8e1e02a10c7"),  # pragma: allow-secret
    "formal": ("05_COSMOLOGY/03_FORMAL_SYSTEM/48_FINITY_PARADOX_LEDGER.yaml", "07c2d9a114624ec4720a66602e8ddf7a47142f1996cec588c025778656d410f6"),  # pragma: allow-secret
    "inventory": ("11_UPLINK/50_AUDITS_AND_EXECUTIONS/188_THE_PARADOX_INVENTORY_2026_07_30.md", "7fd27952d85a39ed46d909f500a96f9f368b98236cb464f6f8970b61f99f9707"),  # pragma: allow-secret
    "f5": ("05_COSMOLOGY/02_EMERGENTISM_CORE/F5Fork.v1.json", "09b2c5700a20fd2d90ad0c2dc11999ad048faea0baf6ce08ac327809a9c1ddb6"),  # pragma: allow-secret
    "owner": (OWNER_DIRECTION, "8fe987447d48a0dd9c559f7769bf05c7f42fd63f9edc0e26440608c744baf107"),  # pragma: allow-secret
}


def frozen_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{FROZEN}:{path}"], cwd=ROOT,
        check=True, capture_output=True,
    )
    return result.stdout


def verify_sources() -> None:
    for key, (path, expected) in SOURCES.items():
        payload = (ROOT / path).read_bytes() if key == "owner" else frozen_bytes(path)
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
            raise ValueError(f"source hash mismatch for {path}: {actual} != {expected}")


def verify_contracts() -> None:
    expected = {
        "drop": "ChurningDrop.v1",
        "problem": "ProblemAdjudication.v1",
        "corpus": "ThirdChurningCorpus.v1",
    }
    for key, path in CONTRACTS.items():
        schema = json.loads(path.read_text(encoding="utf-8"))
        if (
            schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("title") != expected[key]
            or schema.get("type") != "object"
            or schema.get("additionalProperties") is not False
            or not isinstance(schema.get("required"), list)
            or not isinstance(schema.get("properties"), dict)
        ):
            raise ValueError(f"malformed or weakened source contract: {path.name}")
        if not set(schema["required"]).issubset(schema["properties"]):
            raise ValueError(f"required field without property contract: {path.name}")


def validate_top_level(instance: dict, schema_path: Path, *, record_id: str) -> None:
    """Enforce the closed top-level contract without an external dependency."""
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema["required"])
    properties = schema["properties"]
    missing = required - set(instance)
    unknown = set(instance) - set(properties)
    if missing or (schema.get("additionalProperties") is False and unknown):
        raise ValueError(
            f"{record_id}: contract fields fail (missing={sorted(missing)}, "
            f"unknown={sorted(unknown)})"
        )
    for field, contract in properties.items():
        if field not in instance:
            continue
        if "const" in contract and instance[field] != contract["const"]:
            raise ValueError(f"{record_id}: {field} violates const")
        if "enum" in contract and instance[field] not in contract["enum"]:
            raise ValueError(f"{record_id}: {field} violates enum")


def source_ref(key: str, claim_ids: list[str] | None = None) -> dict:
    path, digest = SOURCES[key]
    row = {
        "path": path,
        "sha256": digest,
        "_sha256_scan": "# pragma: allow-secret",
        "frozen_commit": "POST_FREEZE_OWNER_DIRECTION" if key == "owner" else FROZEN,
    }
    if claim_ids:
        row["claim_ids"] = claim_ids
    return row


# id, tier, name, proposition, source, linked problems, rival, kill, residual
AMRITA = [
    ("TC-AMR-001", "[I]", "Dasein and situated dasein stay distinct", "Capitalized Dasein names the selected coherent whole while situated dasein names a finite actual bearer within it; neither is an inventory of the other.", "one", ["PQA54@0.1:MET:ONE_MANY"], "Ordinary whole-part and standpoint language does the same work with fewer commitments.", "Kill the vocabulary if it repeatedly reifies the whole or erases finite bearers.", "Whether Dasein is the best ontology remains open."),
    ("TC-AMR-002", "[I]", "Finity is determinate manifestation", "Finity names determinate manifestation in a declared frame, not finite cardinality and not numeric one.", "second", ["FORMAL:FIELD-01"], "Standard terms such as defined value, limit, event, or instantiation are clearer.", "Retire Finity wherever it adds ambiguity rather than a valid type distinction.", "No new arithmetic follows from the name."),
    ("TC-AMR-003", "[S]", "Value, word, process, operator, and boundary are different types", "A value, its written sign, a generating process, an operator, and a boundary object may be related without being identical.", "second", ["PQA54@0.1:LOG:REFERENCE"], "Native mathematical type systems already prevent these collisions.", "Kill any claimed novelty or extra result not earned beyond the native type discipline.", "The native distinctions survive without Emergentist names."),
    ("TC-AMR-004", "[I/C]", "Higher descriptions may add explanatory value without blocking reduction", "A macro description can remain explanatorily useful when a lower-level reduction exists, provided it earns prediction, intervention, compression, or portability after costs.", "one", ["PQA54@0.1:SCI:EMERGENCE"], "Matched lower-level models may equal or beat every macro benefit.", "Demote to mnemonic wherever matched native models equal or beat it on held-out value and cost.", "Reduction and native domain models remain."),
    ("TC-AMR-005", "[I]", "Quantum state and actual record are different types", "A probability-bearing quantum state and a definite measurement record should not be conflated, even though the distinction alone does not solve measurement.", "one", ["PQA54@0.1:SCI:MEASUREMENT"], "Standard quantum foundations already separates states, channels, apparatus and records.", "Kill distinctiveness if the typing adds no correct prediction or clarification beyond native accounts.", "The measurement problem and Born-rule interpretation remain open."),
    ("TC-AMR-006", "[S]", "Commitment and received consequence need separate receipts", "An actor's stated plan or self-report is not the independently received consequence of the act.", "one", ["PQA54@0.1:SCI:CAUSATION"], "Ordinary audit and causal-inference practice already enforces this separation.", "Kill the framework-specific claim if independent provenance adds no discipline beyond native audit practice.", "Independent outcome evidence remains necessary."),
    ("TC-AMR-007", "[S]", "Possibility acts only through actual carriers", "Represented D5 possibilities influence action only through actual D4 models, bodies, utterances, instruments, memories or institutions.", "one", ["PQA54@0.1:MIN:INTENTIONALITY"], "Standard representational and control theories explain the same causal chain.", "Kill the framework-specific gloss if it adds no discriminator beyond present-carrier models.", "Possible content remains distinct from physical causation."),
    ("TC-AMR-008", "[I]", "The Soul Loop preserves execution and outcome gaps", "A useful reflective loop keeps perception, modelling, commitment, authorization, execution, observation and revision distinguishable.", "one", ["PQA54@0.1:EPI:EXTERNAL_WORLD"], "Decision journals and feedback control provide a simpler equivalent.", "Retire Soul Loop vocabulary if it adds no error detection, correction or transfer benefit.", "The underlying feedback and audit distinctions survive."),
    ("TC-AMR-009", "[C]", "Egregoreotype is an observable coordination hypothesis", "An egregoreotype may be tested as persistent distributed coordination with shared trace, incentive coupling, boundary maintenance and intervention-sensitive added value, without asserting personhood.", "one", ["PQA54@0.1:POL:COLLECTIVE_ACTION"], "Carrier identity, incentives, direct communication and environment may exhaust the effect.", "Kill the construct if those native variables exhaust prediction and intervention response.", "The observable carriers and coordination mechanisms remain."),
    ("TC-AMR-010", "[C]", "Language may deepen coordination", "Shared language may add coordination depth beyond thin exchange signals, but it transfers no truth, consent or common worldview by itself.", "one", ["PQA54@0.1:LOG:RULE_FOLLOWING"], "Repeated interaction, incentives and institutions may explain all coordination gains.", "Kill the incremental claim if language variables add no held-out predictive or intervention value.", "Trade and communication remain bounded coordination channels."),
    ("TC-AMR-011", "[C]", "Worldview competition can be one cause of conflict", "Conflicting coordination patterns may contribute to war alongside security, capacity, geography, finance, trauma and revenge.", "one", ["PQA54@0.1:POL:POWER"], "Material and strategic variables may exhaust the explanatory gain.", "Kill the worldview variable if it adds no held-out value after native conflict controls.", "The multicausal conflict account and nonviolence fence survive."),
    ("TC-AMR-012", "[I]", "Rosetta axes must not collapse", "Trophic role, replicator layer, reasoning function, operator alias and mating or kinship structure are separate axes unless a specific bridge is earned.", "cards", ["PQA54@0.1:EPI:TESTIMONY"], "No crosswalk is needed; native taxonomies should remain separate.", "Kill any crosswalk that predicts nothing and invites hierarchy or identity transfer.", "The native taxonomies remain authoritative."),
    ("TC-AMR-013", "[I]", "Functions are trainable and mobile", "Rosetta work functions are movable practices and never hereditary classes, ranks of human worth or sovereign identities.", "cards", ["PQA54@0.1:POL:LEGITIMACY"], "Plain role descriptions avoid caste and mythic hazards entirely.", "Drop the aliases if they cause persistent rank, essence or authority leakage.", "Equal worth and trainable functional roles remain."),
    ("TC-AMR-014", "[I/C]", "Operational agency is usable under metaphysical nonclosure", "Agents can be assessed by represented options, means, authorization, action and correction while consciousness, ultimate freedom and post-death survival remain open.", "one", ["PQA54@0.1:MIN:FREE_WILL", "PQA54@0.1:MIN:CONSCIOUSNESS"], "Compatibilist and control-based agency already provide the usable account.", "Kill distinctiveness if the decomposition changes no attribution, intervention or correction decision.", "The hard problem and ultimate freedom remain open."),
    ("TC-AMR-015", "[I/C]", "Teleology needs two clocks and all bearers", "A teleological proposal must expose short-horizon enactment and long-horizon option effects for every affected bearer rather than hiding delayed cost in one score.", "one", ["PQA54@0.1:ETH:POPULATION"], "Standard multi-criteria and intergenerational decision theory may dominate the framework.", "Kill the transfer if it hides delayed cost, harmed bearers, uncertainty or decorative Exit.", "Bearer and horizon visibility remain useful."),
    ("TC-AMR-016", "[S/I/C]", "Reciprocal public reason has a conditional bridge", "Inside a voluntarily undertaken reciprocal public-reason practice, arbitrary denial of visibility, contest, correction or feasible Exit defeats the declared reciprocity.", "one", ["PQA54@0.1:ETH:IS_OUGHT"], "Contractualism, discourse ethics or constructivism may explain the same duties more faithfully.", "Kill or narrow the bridge if the conclusion is smuggled into reciprocity or adds no value over serious rivals.", "The practice premise and general is-ought problem remain explicit."),
    ("TC-AMR-017", "[I/C]", "Guardianship is separate from reciprocity", "Care for dependent, absent, nonhuman, ecological and future bearers is a separately chosen, bounded and reviewable extension, not proof borrowed from co-agency.", "one", ["PQA54@0.1:POL:REPRESENTATION"], "Rights, capabilities, fiduciary, precautionary and supported-decision safeguards may perform better.", "Kill or narrow the extension if it self-authorizes, hides conflicts or launders proxy harm.", "Dependent bearers still require visible protection against capture."),
    ("TC-AMR-018", "[S/I/C]", "Moral objectivity must be typed", "Definition stability, procedural reproducibility, empirical adequacy and stance-independent moral realism are different claims and must not inherit one another's warrant.", "one", ["PQA54@0.1:ETH:MORAL_REALISM"], "Established metaethical distinctions already perform the same separation.", "Kill framework distinctiveness if it adds no clarity or hard-case discrimination.", "Moral realism remains open."),
    ("TC-AMR-019", "[D/C]", "Selected is not solved", "A philosophical question earns a result only after native recovery, premise preservation, serious controls, unfired kills and independent native-domain review.", "pqa", ["SYNTH:PQA-EARNED-RESULT"], "Native peer review without a framework benchmark may be more faithful and efficient.", "Kill the construct if it rewards reframing, hides residuals or adds no value over native and generic controls.", "The public denominator and correction ledger survive."),
    ("TC-AMR-020", "[D]", "The means is the message", "How an act is carried already shapes the relation it claims to serve; carriers, costs, consent, authority, reversibility and externalities are part of the claim.", "owner", ["SYNTH:MEANS-MESSAGE"], "Consequentialist cases may permit harmful means when expected outcomes dominate.", "Reject the maxim as universal law if bearer-indexed hard cases show that its constitutive reading obscures justified exceptions.", "Means must still be disclosed and contested."),
    ("TC-AMR-021", "[D]", "The ends are the limits", "Every desired end remains bounded for each affected bearer and responsible horizon; no aggregate end erases a failed row.", "owner", ["SYNTH:ENDS-LIMITS"], "A defended aggregation rule may justify trade-offs across bearers and horizons.", "Reject the non-aggregation reading where a transparent authorized scalar robustly handles hard cases better.", "Hard limits, uncertainty and Exit remain visible."),
    ("TC-AMR-022", "[S]", "G7 closure is vocabulary-scoped", "Four bearer-oriented transfers plus three read-only frames close the selected G7 vocabulary and nothing larger.", "one", ["PQA54@0.1:SCI:EMERGENCE"], "The vocabulary is an arbitrary mnemonic with no explanatory benefit.", "Kill its use if it obscures native game structure or repeatedly collapses necessary distinctions.", "The four typed transfer cells and three separate frame labels remain removable."),
]

HALAHALA = [
    ("TC-HAL-001", "[S]", "Titan glyphs are not arithmetic operands", "Treating •, ⊙ or ○ as ordinary numeric operands or sovereign arithmetic identities is a type error unless a separate numeric model is explicitly declared.", "dead"),
    ("TC-HAL-002", "[I]", "Dasein is not a self-containing set or jointly actual world bundle", "Do not turn the selected Dasein whole into a naive self-membered set, make rival possible worlds jointly actual, or identify one ego with the whole.", "one"),
    ("TC-HAL-003", "[S]", "Convergence is not proof", "Cross-tradition resemblance, model agreement and repeated rendering are robustness clues, never independent truth evidence by themselves.", "second"),
    ("TC-HAL-004", "[S]", "Finity is not finite cardinality or numeric one", "Do not reduce Finity to finite cardinality or identify the centre glyph with ordinary numeric one.", "second"),
    ("TC-HAL-005", "[S]", "Generative arithmetic does not replace field mathematics", "No Titan or projective notation makes field division by zero defined or replaces native mathematics without an explicit structure change.", "formal"),
    ("TC-HAL-006", "[S]", "A process is not its completed denotation", "A non-halting or asymptotic process may denote a completed object in a declared semantics but is not identical to that denoted value.", "formal"),
    ("TC-HAL-007", "[S]", "Missing reduction is not proof of strong emergence", "Failure to provide a reduction is explanatory debt, not evidence that ontological strong emergence has been proved.", "one"),
    ("TC-HAL-008", "[S]", "Macro novelty needs matched controls", "A higher-level description earns no novelty claim without fair lower-level, native and complexity-matched controls.", "one"),
    ("TC-HAL-009", "[S]", "Quantum state, record and time must not collapse", "Do not equate quantum state with event, infer temporal order from unordered snapshots, or claim that D3 typing solves measurement.", "formal"),
    ("TC-HAL-010", "[S]", "Self-issued success is not world-contact evidence", "An actor's own success report can record commitment but cannot alone establish received consequence or independent calibration.", "one"),
    ("TC-HAL-011", "[S]", "Possibility itself does not physically act", "D5 possible content does not push matter, widen a light cone or cause events without an actual D4 carrier or separately evidenced law.", "f5"),
    ("TC-HAL-012", "[S]", "Present future models do not prove retrocausality", "Ordinary model-mediated anticipation is not evidence for a future-boundary interaction or F5-R.", "f5"),
    ("TC-HAL-013", "[S]", "Aliases are not castes, essences or verdicts", "Mythic names and Titan frames must not become hereditary human classes, person-worth ranks or pre-outcome moral judgments.", "cards"),
    ("TC-HAL-014", "[S]", "Four plus three does not prove seven is necessary", "G7 closes only the selected vocabulary and does not prove exactly seven fundamental kinds or exhaust all games.", "one"),
    ("TC-HAL-015", "[S]", "The Burrisphere itinerary is not time or moral ascent", "The selected 360-degree reading path is not recurrence, chronology, physical helix, causal mechanism or moral rank.", "one"),
    ("TC-HAL-016", "[S]", "M4 is not a global or vector-space basis", "M4 may be tested as a lossy code only inside a frozen comparator class; it is not a reconstruction theorem or globally unique basis.", "one"),
    ("TC-HAL-017", "[S]", "The centre is not universally optimal or costless", "The reciprocal centre is analytically balanced but not a universal empirical optimum, trade-off eraser or Dharma theorem.", "one"),
    ("TC-HAL-018", "[S]", "Egregoreotype does not confer personhood", "Persistent coordination does not by itself establish consciousness, legal personhood, autonomous authority or moral patienthood.", "one"),
    ("TC-HAL-019", "[S]", "Synchrony and trade do not establish truth or consent", "Coordination signals can support inference but do not establish truth, fairness, consent or a shared worldview by themselves.", "one"),
    ("TC-HAL-020", "[I]", "War is not reducible to worldview competition", "Worldview conflict is at most one variable among material and strategic causes and never licenses violence.", "one"),
    ("TC-HAL-021", "[S]", "Rosetta axes do not form hereditary hierarchy", "Trophic, replicator, reasoning, operator, Varna and mating axes may not be collapsed into a hereditary rank order.", "cards"),
    ("TC-HAL-022", "[S]", "Aggregates do not hide harmed bearers", "Sacrifice language, product scores and total option gains cannot cancel an undisclosed harmed bearer.", "one"),
    ("TC-HAL-023", "[S]", "Consciousness, free will, death and afterlife remain open", "Operational decompositions do not solve the hard problem, ultimate freedom, death or personal survival.", "inventory"),
    ("TC-HAL-024", "[S]", "Geometry does not prove morality or cosmic purpose", "The reciprocal chart, RCAB and GEX do not prove stance-independent morality, cosmic teleology or coercive guardianship.", "one"),
    ("TC-HAL-025", "[S]", "Force maps and strong emergence remain conjectures", "Correspondence, dimensional order and intuitive fit do not establish a force assignment or strong-emergence crossing.", "one"),
    ("TC-HAL-026", "[S]", "D6 is not D0, afterlife, rank or sixth freedom", "D6 is a nonclosure and Exit marker; boundary-role resemblance neither identifies it with D0 nor makes it an attainment or afterlife.", "one"),
    ("TC-HAL-027", "[S]", "Selection, clarification and reframing are not resolution", "A selected question or elegant reframe cannot be counted as dissolved or resolved, and a bounded majority cannot become most philosophy.", "pqa"),
    ("TC-HAL-028", "[S]", "Process receipts are not external validation", "Offline-ready, ratification, adherents, commits and AI agreement are bounded process facts rather than scientific or philosophical validation.", "method"),
    ("TC-HAL-029", "[D]", "The maxim is not a theorem or permission", "The means-message and ends-limits maxim is a disclosed normative selection, never a theorem and never permission for ends to justify means.", "owner"),
]


def ledger(normative: bool = False) -> tuple[dict, dict]:
    bearers = ["actors", "affected bearers", "future readers"] if normative else ["readers", "researchers"]
    means = {
        "bearers": bearers,
        "short_horizon": "publication and first application",
        "long_horizon": "revision after downstream consequence",
        "carrier": "source-bound text and machine record",
        "cost": "attention, implementation cost and risk of misclassification",
        "consent_or_mandate": "no worldview adoption required; consequence-bearing use needs a declared mandate",
        "authority": "source owners retain semantics; the projection cannot authorize action",
        "reversibility": "classification is revisable and predecessor bytes are preserved",
        "externalities": "overclaim, hidden bearer harm and model-training misquotation remain possible",
    }
    ends = {
        "target": "a clearer, contestable proposition and test",
        "hard_limit": "no tier promotion, false closure, hidden bearer or authority transfer",
        "option_change": "preserve challenge, correction and Exit",
        "residue": "unpaid explanatory and empirical debt stays visible",
        "exit": "drop the claim or framework when it adds no value",
        "uncertainty": "independent review and world contact remain absent",
    }
    return means, ends


def drop_row(row: tuple, classification: str) -> dict:
    if classification == "SURVIVOR_CANDIDATE":
        drop_id, tier, name, proposition, source, problems, rival, kill, residual = row
        alias = "AMRITA"
    else:
        drop_id, tier, name, proposition, source = row
        problems = []
        rival = "The warning may be overbroad; a narrowly typed model could lawfully recover part of the rejected claim."
        kill = "Narrow or retire the warning if an explicit typed model survives native review and its declared discriminator."
        residual = "The narrow lawful use and native domain remain available."
        alias = "HALAHALA"
    normative = drop_id in {"TC-AMR-015", "TC-AMR-016", "TC-AMR-017", "TC-AMR-018", "TC-AMR-020", "TC-AMR-021", "TC-HAL-022", "TC-HAL-024", "TC-HAL-029"}
    means, ends = ledger(normative)
    claim_ids = []
    if source in {"one", "cards"}:
        claim_ids = ["OS01"]
    return {
        "schema_id": "emergentism/ChurningDrop.v1",
        "drop_id": drop_id,
        "plain_name": name,
        "mythic_alias": alias,
        "classification": classification,
        "lifecycle": "SOURCE_BOUND",
        "evidence_tier": tier,
        "proposition": proposition,
        "scope": "Third Churning frozen-source proposition",
        "assumptions": ["source and evidence tier remain attached", "publication does not create earned review"],
        "source_refs": [source_ref(source, claim_ids)],
        "strongest_rival": rival,
        "discriminator": "Compare the exact proposition with its native account and simplest serious rival on clarification, prediction, intervention, compression or harm detection.",
        "kill_criterion": kill,
        "cheapest_next_test": "One blinded native-domain review against a generic decomposition control.",
        "survivor_if_killed": "The native problem, source record and explicit residual remain." if classification == "SURVIVOR_CANDIDATE" else residual,
        "residual_debt": residual,
        "means_message": means,
        "ends_limits": ends,
        "linked_problem_ids": problems,
        "earned_review": {"state": "UNREVIEWED", "independent_review_count": 0, "receipts": []},
        "revision_history": [{"date": "2026-08-23", "event": "source-bound candidate created in the Third Churning rebuild"}],
    }


PROPOSALS = {
    "MET:GROUND": ("REFRAME", "Emergentism places a GROUND_BOUNDARY where object-language explanation no longer has a lawful target; it does not turn Ground into an object or necessary being.", "Why that boundary rather than a brute fact or necessary truth remains open."),
    "MET:ONE_MANY": ("CLARIFICATION", "Typed levels allow one coherent whole and genuine plural situated bearers without identifying either with the other.", "The metaphysical dependence relation is not thereby proved."),
    "MET:UNIVERSALS": ("CLARIFICATION", "Repeatable properties may be tracked as invariants across transformations while their nominalist, realist or trope ontology remains open.", "What makes an invariant ontologically real remains disputed."),
    "MET:IDENTITY": ("CLARIFICATION", "Identity claims must declare which continuity—material, causal, structural, functional, narrative or authorized—carries the same bearer.", "No universal criterion of persistence follows."),
    "MET:MODALITY": ("CLARIFICATION", "Possible content, actual carriers and actual histories are distinct types; this blocks actuality inflation without choosing modal realism.", "Truthmakers for modal claims remain open."),
    "MET:TIME": ("OPEN", "Ordered records and lawful dynamics are required before a sequence can count as time; the dimensional or Burrisphere order alone is not temporal.", "Passage, tense and fundamentality remain open."),
    "EPI:EXTERNAL_WORLD": ("CLARIFICATION", "Resistance, independent consequence and correction provide public warrant beyond present self-report without defeating global skepticism deductively.", "The ultimate skeptical challenge remains."),
    "EPI:INDUCTION": ("CLARIFICATION", "Induction is fallible projectibility whose warrant is comparative calibration, intervention and correction rather than logical entailment.", "The circularity and choice of projectible predicates remain."),
    "EPI:GETTIER": ("CLARIFICATION", "True belief needs a provenance-sensitive warrant that remains connected to the fact through relevant counterfactuals and correction paths.", "Whether this is knowledge or another condition remains contested."),
    "EPI:APRIORI": ("CLARIFICATION", "A priori warrant can be internal necessity inside a declared formal system without becoming a claim about the world's ontology.", "How formal insight is known remains open."),
    "EPI:TESTIMONY": ("CLARIFICATION", "Testimony carries warrant only through declared provenance, competence, calibration, contest and independent contact appropriate to the claim.", "Reductionism versus anti-reductionism remains."),
    "EPI:DISAGREEMENT": ("CLARIFICATION", "Rational disagreement should preserve rivals, discriminators and underdetermination; consensus is never a truth bonus.", "How much peers should conciliate remains case-specific."),
    "LOG:LIAR": ("CONDITIONAL_RESOLUTION", "A liar construction may dissolve within a typed or hierarchical truth language when the offending self-application is excluded explicitly.", "Revenge paradoxes and natural-language truth remain."),
    "LOG:RUSSELL": ("FORMAL_CORRECTION", "The unrestricted formation rule fails; restricted comprehension or a declared type discipline preserves lawful set formation.", "Choice among foundations remains open."),
    "LOG:GODEL": ("CLARIFICATION", "Incompleteness is retained as a nonclosure result for systems meeting its hypotheses; no outside glyph or observer completes the system.", "Philosophical interpretations remain open."),
    "LOG:SORITES": ("CLARIFICATION", "Sorites arguments require an explicit scale, threshold rule and uncertainty region; this diagnoses hidden boundary assumptions without eliminating vagueness.", "A theory of vague truth remains open."),
    "LOG:REFERENCE": ("CLARIFICATION", "Actual signs and uses can carry represented content through causal, inferential and social practices while sign, referent and interpretation stay distinct.", "A complete metasemantics remains open."),
    "LOG:RULE_FOLLOWING": ("CLARIFICATION", "Public correction, shared practice and counterfactual response constrain rule following without converting agreement into truth.", "The normativity of meaning remains."),
    "MIN:MIND_BODY": ("CLARIFICATION", "D5 content is realized through D4 carriers, separating content from carrier without establishing physicalism, dualism or a psychophysical mechanism.", "The realization and consciousness relations remain open."),
    "MIN:CONSCIOUSNESS": ("OPEN", "Emergentism can type reports, carriers, access and behavior but presently supplies no mechanism that explains why processing is accompanied by experience.", "The hard problem remains fully open."),
    "MIN:INTENTIONALITY": ("CLARIFICATION", "Present actual representations can be about absent or possible content; the content itself need not physically act.", "Naturalization of original intentionality remains."),
    "MIN:PERSONAL_IDENTITY": ("CLARIFICATION", "Personal persistence requires a declared bundle of bodily, causal, psychological, narrative and authorized continuities, with fission debt preserved.", "No single necessary and sufficient criterion is established."),
    "MIN:FREE_WILL": ("REFRAME", "Operational agency can be assessed through represented options, available means, authorization, action and correction without settling ultimate sourcehood.", "Ultimate freedom and desert remain open."),
    "MIN:OTHER_MINDS": ("CLARIFICATION", "Other minds and AI mentality require convergent public evidence across behavior, structure, intervention and self-report; private phenomenology remains inaccessible.", "No consciousness attribution is earned here."),
    "SCI:CAUSATION": ("CLARIFICATION", "Causal claims should expose intervention, counterfactual, temporal and receipt structure rather than rest on correlation or narrative fit.", "Competing metaphysics of causation remain."),
    "SCI:LAWS": ("CLARIFICATION", "Law, model, mechanism, constraint and explanation are different types whose adequacy must be tested in their native domain.", "What makes laws necessary remains open."),
    "SCI:EMERGENCE": ("CLARIFICATION", "Emergence claims must distinguish construction, reduction, multiple realization, constraint and explanatory usefulness; missing reduction is not proof of strength.", "Every crossing remains an empirical wager."),
    "SCI:MEASUREMENT": ("CLARIFICATION", "Quantum state, interaction, probability and actual record remain separate; the typing blocks conflation but selects no interpretation.", "Definite outcomes and Born weights remain open."),
    "SCI:BELL": ("CLARIFICATION", "Bell-type conclusions retain their exact assumptions; no Emergentist frame restores a conjunction experimentally ruled out.", "Interpretation and viable assumption packages remain."),
    "SCI:PROBABILITY": ("CLARIFICATION", "Probability calculus, model-relative uncertainty, credence and physical chance are separate claims whose interpretation must be declared.", "The ontology of chance remains open."),
    "ETH:IS_OUGHT": ("CONDITIONAL_RESOLUTION", "RCAB supplies a constitutive ought only inside a disclosed reciprocal public-reason practice; it is not a value-free derivation.", "The general is-ought problem and moral realism remain."),
    "ETH:MORAL_REALISM": ("CLARIFICATION", "Definition stability, reproducibility, world adequacy and stance-independent moral truth are distinct; only the first is presently internal to the model.", "Moral realism remains open."),
    "ETH:EUTHYPHRO": ("REFRAME", "Authority cannot manufacture the Good merely by command; Emergentism separately chooses Justice and exposes its price.", "Why Justice is ultimately binding remains open."),
    "ETH:RIGHTS_OUTCOMES": ("REFRAME", "Justice refusals constrain a bearer-complete Pareto ledger before aggregate outcomes are considered.", "Thresholds, conflicts and tragic cases remain."),
    "ETH:POPULATION": ("CLARIFICATION", "Bearer and horizon indexing prevents automatic laundering across populations but supplies no complete population ordering.", "Nonidentity, aggregation and repugnant-conclusion debt remain."),
    "ETH:RESPONSIBILITY": ("CLARIFICATION", "Responsibility should expose agency, means, authorization, foreseeability, consent, power and correction; sacrifice is never intrinsically good.", "Desert, partiality and demandingness remain."),
    "POL:LEGITIMACY": ("CLARIFICATION", "Legitimacy requires actual authority, bounded mandate, contest, consequence accounting and feasible Exit; coordination alone cannot authorize.", "Political obligation and nonconsensual authority remain contested."),
    "POL:LIBERTY_EQUALITY": ("REFRAME", "Liberty is viable option and non-domination for named bearers, while equality constrains standing; neither collapses into one scalar.", "Institutional trade-offs remain."),
    "POL:DISTRIBUTION": ("CLARIFICATION", "Contribution, support, need, entitlement, capability and burden should remain separate ledger dimensions before any defended aggregation.", "A complete distributive rule remains open."),
    "POL:COLLECTIVE_ACTION": ("CLARIFICATION", "Persistent trace, repeated interaction, bounded sanctions, contest and receipts make cooperation auditable without assuming harmony.", "Institution design remains context-specific."),
    "POL:POWER": ("CLARIFICATION", "Power is capacity to change options; extraction is a bearer-indexed transfer that hides or sustains uncompensated loss, and the two must not be equated.", "Measurement and structural domination remain open."),
    "POL:REPRESENTATION": ("REFRAME", "GEX makes guardianship a chosen, disclosed, conflict-aware, least-restrictive and reviewable mandate rather than inferred consent.", "Who may bind absent bearers remains open."),
    "AXI:PLURALISM": ("CLARIFICATION", "Real value conflicts should remain a vector or Pareto frontier unless an aggregation contract is separately defended.", "Tragic choice and incomparability remain."),
    "AXI:BEAUTY": ("OPEN", "Beauty may be relationally stable across bearer, form, context and response without being reduced to preference or proved stance-independent.", "Aesthetic objectivity remains open."),
    "AXI:ART": ("CLARIFICATION", "Art is an actual carrier that opens represented possibilities; creator, work, interpretation, institution and effect remain different bearers.", "Definition and interpretation limits remain contested."),
    "AXI:MEANING": ("REFRAME", "Meaning can be enacted orientation that survives consequence and correction for a finite bearer without requiring cosmic assignment.", "Whether meaning is objective remains open."),
    "AXI:SUFFERING": ("CLARIFICATION", "Suffering must remain bearer-visible and may never be explained away by a totalizing harmony, score or future end.", "Why suffering exists and how to respond remain open."),
    "AXI:DEATH": ("OPEN", "Death ends an actual carrier and its option cone; traces may persist, but persistence of effects does not prove personal survival.", "The badness of death and afterlife remain open."),
    "ULT:NECESSARY_BEING": ("REFRAME", "A declared Ground boundary stops one explanatory grammar without proving a necessary being or necessary existent.", "Cosmological arguments and ultimate explanation remain open."),
    "ULT:EVIL": ("OPEN", "Emergentism refuses to turn suffering into required harmony and supplies no theodicy.", "The logical and evidential problems of evil remain."),
    "ULT:HIDDENNESS": ("OPEN", "Apophatic limits explain why a map may fail to contain its ground but do not explain nonresistant divine hiddenness.", "Perfect love, revelation and nonbelief remain open."),
    "ULT:PLURALISM": ("CLARIFICATION", "Rosetta can compare structures across traditions while forbidding truth transfer from resemblance or convergence.", "Incompatible truth claims remain unresolved."),
    "ULT:MYSTICAL": ("CLARIFICATION", "Mystical experience is actual evidence about a report and life but receives no automatic public truth bonus beyond its provenance and effects.", "Its metaphysical interpretation remains open."),
    "ULT:NONDUALITY": ("REFRAME", "Dasein and situated dasein permit a nonseparation reading while preserving finite agency, difference and Exit; the reading is not proved by the atlas.", "Nondual ontology and liberation claims remain open."),
}

ALIASES = {
    "LOG:RUSSELL": ["FORMAL:RUSSELL-01", "LEGACY:PD-08"],
    "LOG:LIAR": ["LEGACY:PD-08"],
    "LOG:GODEL": ["FORMAL:GODEL-01"],
    "SCI:MEASUREMENT": ["FORMAL:MEAS-01", "LEGACY:PD-12"],
    "SCI:BELL": ["LEGACY:PD-25"],
    "MIN:FREE_WILL": ["LEGACY:PD-11"],
    "MIN:CONSCIOUSNESS": ["LEGACY:PD-13", "LEGACY:PD-19"],
    "MIN:MIND_BODY": ["LEGACY:PD-14"],
    "ETH:IS_OUGHT": ["LEGACY:PD-10"],
    "AXI:MEANING": ["LEGACY:PD-16"],
    "AXI:DEATH": ["LEGACY:PD-21"],
    "ULT:NECESSARY_BEING": ["LEGACY:PD-09"],
    "ULT:EVIL": ["LEGACY:PD-15"],
    "MET:ONE_MANY": ["LEGACY:PD-05"],
    "MET:IDENTITY": ["LEGACY:PD-06"],
}

DOMAIN_DROPS = {
    "MET": ["TC-AMR-001", "TC-HAL-002"],
    "EPI": ["TC-AMR-006", "TC-HAL-003"],
    "LOG": ["TC-AMR-003", "TC-HAL-006"],
    "MIN": ["TC-AMR-007", "TC-AMR-014", "TC-HAL-023"],
    "SCI": ["TC-AMR-004", "TC-AMR-005", "TC-HAL-007", "TC-HAL-009"],
    "ETH": ["TC-AMR-016", "TC-AMR-018", "TC-HAL-022", "TC-HAL-024"],
    "POL": ["TC-AMR-017", "TC-HAL-021"],
    "AXI": ["TC-AMR-015", "TC-HAL-017", "TC-HAL-023"],
    "ULT": ["TC-HAL-003", "TC-HAL-023", "TC-HAL-024"],
}


def build_problems() -> list[dict]:
    atlas = json.loads(frozen_bytes(SOURCES["pqa"][0]))
    rows = []
    for domain in atlas["domains"]:
        for question in domain["questions"]:
            suffix = ":".join(question["question_id"].split(":")[-2:])
            effect, answer, debt = PROPOSALS[suffix]
            rows.append({
                "schema_id": "emergentism/ProblemAdjudication.v1",
                "problem_id": question["question_id"],
                "canonical_problem_id": question["question_id"],
                "aliases": ALIASES.get(suffix, []),
                "domain": domain["code"],
                "family": question["family"],
                "native_problem": question["native_problem"],
                "native_reference": question["native_reference"],
                "proposed_answer": answer,
                "proposed_effect": effect,
                "earned_effect": "NO_INCREMENT",
                "result_state": "SELECTED",
                "assumptions": ["the native problem and premises are preserved", "the proposal has not been independently reviewed"],
                "strongest_rival": f"The native {question['native_problem'].lower()} literature plus generic decomposition explains the issue more faithfully and with less imposed vocabulary.",
                "native_frame_control": f"Answer only within the native frame anchored by {question['native_reference']}",
                "generic_decomposition_control": "Separate terms, levels, carriers, warrants and residuals without using Emergentist vocabulary.",
                "discriminator": "Two blinded native-domain reviewers must find incremental clarification or resolution beyond both controls while every premise and residual remains visible.",
                "kill_criterion": "No result is earned if the question changes, a premise or residual disappears, the native account is distorted, review quorum is absent or the proposal adds no value over both controls.",
                "remaining_debt": debt,
                "survivor_if_killed": "The native problem, references, public denominator and explicit debt remain.",
                "linked_drop_ids": DOMAIN_DROPS[domain["code"]],
                "native_reviews": [],
            })
    if len(rows) != 54 or len({row["problem_id"] for row in rows}) != 54:
        raise ValueError("problem ledger must contain 54 unique PQA rows")
    return rows


FORMAL_TO_PQA = {
    "ZENO-01": "LEGACY:PD-04", "REAL-01": "FORMAL:REAL-01", "FIELD-01": "FORMAL:FIELD-01",
    "LIMIT-01": "FORMAL:LIMIT-01", "HILBERT-01": "FORMAL:HILBERT-01", "CANTOR-01": "FORMAL:CANTOR-01",
    "RUSSELL-01": "PQA54@0.1:LOG:RUSSELL", "GODEL-01": "PQA54@0.1:LOG:GODEL", "MEAS-01": "PQA54@0.1:SCI:MEASUREMENT",
}


def build_paradox_inventory() -> dict:
    formal = json.loads(frozen_bytes(SOURCES["formal"][0]))
    formal_rows = [{
        "inventory_id": f"FORMAL:{row['id']}",
        "kind": "FORMAL",
        "title": row["question"],
        "canonical_problem_id": FORMAL_TO_PQA[row["id"]],
        "proposed_state": row["classification"].upper(),
        "earned_state": "NOT_INDEPENDENTLY_REVIEWED",
        "residual": row["residual"],
        "source_path": SOURCES["formal"][0],
    } for row in formal["rows"]]
    legacy_names = {
        4: "Zeno", 5: "The One and the Many", 6: "Ship of Theseus", 7: "Fermi paradox", 8: "Liar paradox",
        9: "Leibniz necessary being", 10: "Is-ought", 11: "Free will and determinism", 12: "Measurement problem",
        13: "Hard problem", 14: "Mind-body", 15: "Problem of evil", 16: "Meaning of life", 18: "Extraction paradox",
        19: "Hard problem of consciousness", 20: "Philosophical implications", 21: "Problem of death",
        22: "Scientific implications", 23: "The completion", 24: "The third unveiling", 25: "Bell and local realism",
    }
    meta = {20, 22, 23, 24}
    legacy_rows = [{
        "inventory_id": f"LEGACY:PD-{number:02d}",
        "kind": "META" if number in meta else "LEGACY",
        "title": title,
        "canonical_problem_id": f"LEGACY:PD-{number:02d}",
        "proposed_state": "HISTORICAL_CLAIM",
        "earned_state": "0_OF_21_DISSOLVED",
        "residual": "See Receipt 188; the historical route does not earn a dissolution.",
        "source_path": f"08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/PD_{number:02d}_*.md",
    } for number, title in legacy_names.items()]
    synthesis = [
        {"inventory_id": "SYNTH:INDUCTION", "kind": "SYNTHESIS", "title": "Induction", "canonical_problem_id": "PQA54@0.1:EPI:INDUCTION", "proposed_state": "CLARIFICATION", "earned_state": "SELECTED", "residual": "Projectibility and circularity remain.", "source_path": SOURCES["pqa"][0]},
        {"inventory_id": "SYNTH:EUTHYPHRO", "kind": "SYNTHESIS", "title": "Euthyphro", "canonical_problem_id": "PQA54@0.1:ETH:EUTHYPHRO", "proposed_state": "REFRAME", "earned_state": "SELECTED", "residual": "Ultimate normativity remains.", "source_path": SOURCES["pqa"][0]},
        {"inventory_id": "SYNTH:MEANS-MESSAGE", "kind": "SYNTHESIS", "title": "Means and relation", "canonical_problem_id": "SYNTH:MEANS-MESSAGE", "proposed_state": "SELECTED_MAXIM", "earned_state": "UNREVIEWED", "residual": "Hard cases remain.", "source_path": OWNER_DIRECTION},
        {"inventory_id": "SYNTH:ENDS-LIMITS", "kind": "SYNTHESIS", "title": "Ends and limits", "canonical_problem_id": "SYNTH:ENDS-LIMITS", "proposed_state": "SELECTED_MAXIM", "earned_state": "UNREVIEWED", "residual": "Aggregation hard cases remain.", "source_path": OWNER_DIRECTION},
    ]
    return {
        "schema_id": "emergentism/ParadoxInventory.v1",
        "frozen_source_commit": FROZEN,
        "counts": {"formal": len(formal_rows), "legacy": len(legacy_rows), "synthesis": len(synthesis), "legacy_dissolved": 0},
        "rows": [*formal_rows, *legacy_rows, *synthesis],
        "boundary": "Inventory and proposed effects are not earned resolution; aliases deduplicate problems without erasing their histories.",
    }


def packet_outputs() -> dict[Path, str]:
    drops = [drop_row(row, "SURVIVOR_CANDIDATE") for row in AMRITA] + [drop_row(row, "POISON_WARNING") for row in HALAHALA]
    if len(drops) > 64 or len({row["drop_id"] for row in drops}) != len(drops):
        raise ValueError("drop ceiling or unique-ID contract failed")
    problems = build_problems()
    inventory = build_paradox_inventory()
    source_paths = sorted({ref["path"] for row in drops for ref in row["source_refs"]} | {SOURCES["pqa"][0], SOURCES["pqa_projection"][0], SOURCES["formal"][0], SOURCES["inventory"][0]})
    source_hashes = [{"path": path, "sha256": next(digest for _, (candidate, digest) in SOURCES.items() if candidate == path), "_sha256_scan": "# pragma: allow-secret"} for path in source_paths]
    envelope = {
        "schema_id": "emergentism/ThirdChurningCorpus.v1",
        "release_id": "THIRD-CHURNING-2026-08-23",
        "date": "2026-08-23",
        "frozen_source_commit": FROZEN,
        "drop_ceiling": 64,
        "schema_paths": {
            "drop": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ChurningDrop.v1.schema.json",
            "problem": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ProblemAdjudication.v1.schema.json",
            "corpus": "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/contracts/ThirdChurningCorpus.v1.schema.json"
        },
        "source_pathset": source_paths,
        "source_hashes": source_hashes,
        "predecessor_receipt": "90_ARCHIVE/2026_08_23_third_churning_predecessors/SUPERSESSION_RECEIPT.md",
        "pqa_launch_counts": {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0},
        "drop_order": [row["drop_id"] for row in drops],
        "problem_order": [row["problem_id"] for row in problems],
        "output_map": {
            "churn_page": "12_PUBLIC_SITE/churn/index.html", "amrita_page": "12_PUBLIC_SITE/amrita/index.html",
            "halahala_page": "12_PUBLIC_SITE/halahala/index.html", "corpus_json": "12_PUBLIC_SITE/churn/corpus.json",
            "corpus_jsonl": "12_PUBLIC_SITE/churn/corpus.jsonl", "corpus_markdown": "12_PUBLIC_SITE/churn/corpus.md",
            "problems_json": "12_PUBLIC_SITE/churn/problems.json", "paradoxes_json": "12_PUBLIC_SITE/churn/paradoxes.json",
            "legacy_alias": "12_PUBLIC_SITE/amrita/amrita.json"
        },
        "license": "CC BY-SA 4.0",
        "authorship": "Yves R. Burri",
        "ai_assistance": "AI assistance disclosed for research, adversarial review, formalization, implementation and editing; no AI is an independent reviewer or coauthor.",
        "external_states": {"deployed": False, "doi_archive": False, "github_release": False, "training_inclusion_guaranteed": False},
    }
    for row in drops:
        validate_top_level(row, CONTRACTS["drop"], record_id=row["drop_id"])
    for row in problems:
        validate_top_level(row, CONTRACTS["problem"], record_id=row["problem_id"])
    validate_top_level(envelope, CONTRACTS["corpus"], record_id=envelope["release_id"])
    return {
        DATA / "churning_drops.v1.json": safe_json(drops),
        DATA / "problem_adjudications.v1.json": json.dumps(problems, ensure_ascii=False, indent=2) + "\n",
        DATA / "paradox_inventory.v1.json": json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        HERE / "ThirdChurningCorpus.v1.json": safe_json(envelope),
    }


def safe_json(value: object) -> str:
    """Keep checksum exemptions on the same valid-JSON line as each digest."""
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    text = text.replace(
        '\n        "_sha256_scan": "# pragma: allow-secret",',
        ' "_sha256_scan": "# pragma: allow-secret",',
    )
    text = text.replace(
        '\n      "_sha256_scan": "# pragma: allow-secret"',
        ' "_sha256_scan": "# pragma: allow-secret"',
    )
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        verify_sources()
        verify_contracts()
        outputs = packet_outputs()
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"THIRD CHURNING SOURCE: FAIL\n- {exc}")
        return 1
    drift = []
    for path, content in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                drift.append(path.relative_to(HERE).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        print("THIRD CHURNING SOURCE: FAIL")
        for rel in drift:
            print(f"- deterministic drift: {rel}")
        return 1
    print(f"THIRD CHURNING SOURCE: PASS · {len(AMRITA)} survivor candidates · {len(HALAHALA)} poison warnings · 54/0/0/0 · {'clean' if args.check else 'rendered'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
