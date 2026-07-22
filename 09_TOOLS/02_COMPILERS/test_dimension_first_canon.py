"""Corpus-level acceptance tests for the dimension-first Emergentist canon.

These tests protect type and authority boundaries.  They do not treat passing
tests as empirical confirmation of the worldview.
"""

from __future__ import annotations

import json
import importlib.util
import math
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]

PATHS = {
    "completion": ROOT / "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md",
    "settled": ROOT / "00_META/00_SETTLED_CANON_REGISTRY.md",
    "formula": ROOT / "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md",
    "balance": ROOT / "05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md",
    "burri": ROOT / "05_COSMOLOGY/00_THE_BURRI_RULES.md",
    "titans": ROOT / "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md",
    "mu": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md",
    "closure": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md",
    "d1": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md",
    "d2": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/43_D2_FUNCTION_ATLAS_AND_CONFIGURATION.md",
    "d3": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/44_D3_QUANTUM_STATE_REGISTER.md",
    "d45": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
    "soul": ROOT / "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/10_THE_SOUL_LOOP.md",
    "power": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
    "values": ROOT / "04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md",
    "egregore": ROOT / "05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md",
    "g7": ROOT / "05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md",
    "types": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md",
    "topology": ROOT / "05_COSMOLOGY/00_BURRI_RULES_TOPOLOGY.json",
    "formal_index": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/README.md",
    "rosetta_master": ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md",
    "rosetta_table": ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_ROWS/00_GENERATIVE_TABLE.md",
    "suda_crosswalk": ROOT / "03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/SUDA_DIMENSIONAL_CROSS_REFERENCE.md",
    "photon_paper": ROOT / "03_METHODOLOGY/02_THE_PAPERS/PAPER_C_PHOTON_UNIT_OF_ACCOUNT.md",
    "old_d6_owner": ROOT / "06_ONTOLOGY/00_D6_AS_APOPHATIC_CLOSURE.md",
    "old_d56_owner": ROOT / "06_ONTOLOGY/00_D5_D6_CORPUS_STABILIZATION.md",
    "register_axioms": ROOT / "06_ONTOLOGY/07_THE_DIMENSIONAL_REGISTER_AXIOMS.md",
    "door": ROOT / "00_THE_WELTANSCHAUUNG.md",
    "force": ROOT / "01_TELEOLOGY/02_THE_DERIVATION/07_THE_FOUR_FORCES_ARE_THE_FOUR_LINES.md",
    "conjectures": ROOT / "06_ONTOLOGY/04_THE_CONJECTURES.md",
    "steel": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/25_STEEL_THREAD.md",
    "papers_index": ROOT / "03_METHODOLOGY/02_THE_PAPERS/README.md",
    "operational": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/30_OPERATIONAL_DEFINITIONS.md",
    "upgrade": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/32_THEOREM_UPGRADE_PROTOCOL.md",
    "suda_protocol": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/39_SUDA_CROSS_VALIDATION_PROTOCOLS.md",
}


def read(name: str) -> str:
    return PATHS[name].read_text(encoding="utf-8")


def section_without(text: str, heading: str) -> str:
    """Remove one Markdown level-two section, preserving all other content."""

    start = text.index(f"## {heading}")
    match = re.search(r"^## ", text[start + 3 :], flags=re.MULTILINE)
    end = len(text) if match is None else start + 3 + match.start()
    return text[:start] + text[end:]


class DimensionAndArithmeticTests(unittest.TestCase):
    def test_titan_frames_have_empty_arithmetic_signature(self):
        scoped = "\n".join(read(name) for name in ("titans", "types", "d1", "burri"))
        self.assertIn("ArithmeticSignature(TitanFrame)=∅", scoped)
        self.assertIn("TitanFrame ↛ Number", scoped)
        for operation in ("add_T", "sub_T", "mul_T", "div_T", "pow_T", "log_T"):
            self.assertRegex(
                scoped,
                rf"\b{re.escape(operation)}\b[^\n]*:\s*undefined",
                f"{operation} must remain outside the TitanFrame signature",
            )

        # The render map is permitted; an implicit conversion into an arithmetic
        # carrier is not.  This is a source-type assertion, not a Python model of
        # the Titans.
        self.assertIn("render_T", scoped)
        self.assertRegex(scoped, r"TitanFrame\s*(?:→|->)\s*Glyph")
        self.assertNotRegex(scoped, r"coerce_T\s*:\s*TitanFrame\s*(?:→|->)\s*(?:Number|ℝ|ℂ)")

    def test_numeric_identities_do_not_operate_on_titan_frames(self):
        for x in (-13, -1, 0, 1, 2, 19, 2.5):
            self.assertEqual(x + 0, x)
            self.assertEqual(x * 1, x)
            self.assertEqual(x / 1, x)

        scoped = "\n".join(read(name) for name in ("titans", "types", "d1", "door"))
        self.assertRegex(scoped, r"1_T\s*[≠!=]+\s*1_N")
        self.assertIn("Ordinary numeric `0` and `1` remain", scoped)
        self.assertRegex(scoped, r"(?:x\+0=x|0` is the additive\s+identity)")
        self.assertRegex(scoped, r"(?:x[·*]1=x|1` is the multiplicative\s+identity)")

    def test_positive_first_number_taxonomy_preserves_standard_closures(self):
        unit_seed = {"star"}
        self.assertEqual(len(unit_seed), 1)

        positive_naturals = set(range(1, 32))
        self.assertNotIn(0, positive_naturals)
        self.assertEqual(sum(1 for _ in range(9)), 9)
        self.assertEqual(math.prod([1] * 9), 1)

        punctured_integers = set(range(-16, 0)) | set(range(1, 17))
        self.assertNotIn(0, punctured_integers)
        self.assertIn(1, punctured_integers)
        self.assertIn(-1, punctured_integers)
        self.assertNotIn(1 + (-1), punctured_integers)
        standard_integer_sample = punctured_integers | {0}
        self.assertIn(0, standard_integer_sample)

        text = read("d1")
        self.assertIn("UnitSeed U := {★}", text)
        self.assertRegex(text, r"0_N\s*∉\s*ℕ⁺")
        self.assertIn("SignedMagnitude := {+,-}×ℕ⁺", text)
        self.assertIn("embed(+ ,n)=n; embed(- ,n)=-n", text)
        self.assertIn("ℤ_• := image(embed) = ℕ⁺ ⊎ (-ℕ⁺) = ℤ \\ {0_N}", text)
        self.assertIn("tagged construction that does not presuppose the\ninteger carrier", text)
        self.assertIn("(+1_N)+(-1_N)=0_N ∉ ℤ_•", text)
        self.assertRegex(text, r"ℤ_•` is the \*\*nonzero signed-integer set\*\*, not an additive group or ring")
        self.assertIn("ℤ := ℤ_• ⊔ {0_N}", text)
        self.assertRegex(text, r"every\s+finite product `1_N·…·1_N` still equals `1_N`")
        self.assertRegex(
            text,
            r"This is a\s+categorization choice, not deletion of zero from standard mathematics",
        )

    def test_projective_boundary_remains_one_dimensional(self):
        text = read("d2")
        self.assertIn("ℝP¹ = ℝ ∪ {∞_P}", text)
        self.assertIn("dim_ℝ(ℝP¹)=1", text)
        self.assertIn("Adjoining the boundary point `∞_P` does not create D2", text)
        self.assertIn("preserving its real dimension", text)

    def test_russell_and_power_set_boundary_is_typed(self):
        text = read("d2")
        self.assertIn("R? := {x | x∉x}", text)
        self.assertIn("unrestricted comprehension cannot form `R?` as\na set", text)
        self.assertIn("𝒫(A) := {B | B⊆A}", text)
        self.assertIn("Mem_A := {(a,B)∈A×𝒫(A) | a∈B}", text)
        self.assertIn("treating that relational lift as an instance of `μ₁` is `[I/C]`", text)
        self.assertIn("not a\ntheorem that set formation creates a physical dimension", text)
        self.assertIn("not\nevidence of a μ-crossing", text)
        self.assertIn("D_f := {x∈X | x∉f(x)}", text)
        self.assertRegex(text, r"no `f:X→℘\(X\)` is\s+surjective")

    def test_active_owners_do_not_operationalize_titan_arithmetic(self):
        # This is intentionally bounded to current semantic owners/front doors.
        # Archives, receipts, compatibility records, and explicit tombstones are
        # outside the scan because they must preserve the historical failures.
        owner_names = (
            "titans",
            "types",
            "d1",
            "formula",
            "burri",
            "settled",
            "completion",
            "register_axioms",
            "door",
        )
        allowed_context = (
            "undefined",
            "inadmissible",
            "not arithmetic",
            "not field arithmetic",
            "not an operation",
            "non-operational",
            "no arithmetic",
            "apparent",
            "prohibit",
            "forbid",
            "retired",
            "kill",
        )
        violations: list[str] = []
        suspicious = (
            # Subscripted terms are unambiguously Titan-typed.
            r"(?:0_T|1_T|∞_T)\s*(?:[+\-*/×÷^]|\*\*)\s*(?:0_T|1_T|∞_T)",
            # These are the two familiar visual shorthands that most easily get
            # mistaken for an arithmetic derivation.
            r"⊙\s*=\s*•\s*(?:×|\*)\s*○",
            r"(?:0|0_T)\s*(?:×|\*)\s*(?:∞|∞_T)\s*=\s*(?:1|1_T)",
        )
        for name in owner_names:
            body = read(name)
            for pattern in suspicious:
                for match in re.finditer(pattern, body):
                    context = body[max(0, match.start() - 280) : match.end() + 280].lower()
                    if not any(guard in context for guard in allowed_context):
                        line = body.count("\n", 0, match.start()) + 1
                        violations.append(f"{PATHS[name].relative_to(ROOT)}:{line}: {match.group(0)}")

            # An operation name may only occur as part of the empty-signature
            # declaration or in prose explaining that it is unavailable.
            for match in re.finditer(r"\b(?:add|sub|mul|div|pow|log)_T\b[^\n]*", body):
                line_text = match.group(0).lower()
                context = body[max(0, match.start() - 160) : match.end() + 160].lower()
                if "undefined" not in line_text and not any(
                    guard in context for guard in allowed_context
                ):
                    line = body.count("\n", 0, match.start()) + 1
                    violations.append(f"{PATHS[name].relative_to(ROOT)}:{line}: {match.group(0)}")

        self.assertEqual(
            violations,
            [],
            "Operational Titan arithmetic escaped the empty signature:\n" + "\n".join(violations),
        )

    def test_retired_titan_infix_is_absent_from_live_nonhistorical_surfaces(self):
        roots = [
            ROOT / name
            for name in (
                "00_CONTROL",
                "00_META",
                "01_TELEOLOGY",
                "02_EPISTEMOLOGY",
                "03_METHODOLOGY",
                "04_AXIOLOGY",
                "05_COSMOLOGY",
                "06_ONTOLOGY",
                "07_THEOLOGY",
                "08_FRAMEWORK_SUPPORT",
                "09_TOOLS",
                "10_SEED",
            )
        ]
        historical_markers = (
            'status: "superseded',
            'status: "withdrawn',
            "historical compatibility",
            "historical research",
            "historical filename retained",
            "archive_boundary:",
            "genesis document (pre-hardening",
        )
        violations: list[str] = []
        for root in roots:
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in {
                    ".md",
                    ".py",
                    ".r",
                    ".json",
                    ".yaml",
                    ".yml",
                }:
                    continue
                rel = path.relative_to(ROOT)
                if {"90_ARCHIVE", "91_COMPATIBILITY"}.intersection(rel.parts):
                    continue
                if any(part.startswith(".") for part in rel.parts):
                    continue
                body = path.read_text(encoding="utf-8")
                if any(marker in body[:2000].lower() for marker in historical_markers):
                    continue
                for match in re.finditer(r"⊙\s*=\s*•\s*[×*]\s*○", body):
                    line = body.count("\n", 0, match.start()) + 1
                    violations.append(f"{rel}:{line}: {match.group(0)}")
        self.assertEqual(
            violations,
            [],
            "Retired Titan infix remains live:\n" + "\n".join(violations),
        )

    def test_exact_register_transition_and_boundary_census(self):
        topology = json.loads(read("topology"))
        nodes = {node["id"]: node for node in topology["nodes"]}
        self.assertTrue({f"d{n}" for n in range(7)} <= set(nodes))
        self.assertEqual(nodes["d0"]["kind"], "frame")
        self.assertEqual(nodes["d6"]["kind"], "frame")
        self.assertTrue(all(nodes[f"d{n}"]["kind"] == "state" for n in range(1, 6)))
        self.assertTrue(
            all(nodes[f"d{n}"]["modality"] == "structural" for n in (0, 1, 2, 3, 6))
        )
        self.assertEqual(nodes["d4"]["modality"], "actual")
        self.assertEqual(nodes["d5"]["modality"], "possible")
        self.assertEqual(
            {node["id"] for node in topology["nodes"] if node["kind"] == "crossing"},
            {f"mu-{n}" for n in range(5)},
        )
        self.assertTrue(
            all(
                node["modality"] == "structural"
                for node in topology["nodes"]
                if node["kind"] == "crossing"
            )
        )
        self.assertEqual(
            [(edge["id"], edge["from"], edge["to"]) for edge in topology["edges"] if edge["edgeType"] == "boundary"],
            [("b6", "d5", "d6")],
        )
        self.assertEqual(
            [(edge["id"], edge["from"], edge["to"]) for edge in topology["edges"] if edge["edgeType"] == "closure"],
            [("r6", "d6", "d0")],
        )
        receipts = {
            node["id"]: node["receiptType"]
            for node in topology["nodes"]
            if node["kind"] == "receipt"
        }
        self.assertEqual(
            receipts,
            {"commitment-receipt": "commitment", "outcome-receipt": "outcome"},
        )

    def test_mu_statuses_are_individually_typed(self):
        text = read("mu")
        self.assertIn("`μ₀` is an origin aperture", text)
        self.assertIn("`[] / not_applicable`", text)
        self.assertIn("the constructions are `reduced [A/S]`", text)
        self.assertIn("`reduced [I]` as a formal construction", text)
        self.assertIn("`reduced [A/I]` as an operational reconstruction/interface", text)
        self.assertIn("`[] / not_yet_supplied`", text)
        self.assertNotRegex(text, r"μ[₅₆]\s*:")
        self.assertNotRegex(text, r"μ-[56]")

    def test_field_division_and_directional_limits(self):
        with self.assertRaises(ZeroDivisionError):
            _ = 1.0 / 0.0
        eps = 1e-9
        self.assertGreater(1.0 / eps, 0)
        self.assertLess(1.0 / -eps, 0)
        text = read("d1")
        self.assertIn("div_F : F × (F \\\\ {0}) → F", text)
        self.assertIn("ordinary two-sided real limit", text)
        self.assertIn("diverges", text)

    def test_projective_continuation_changes_structure(self):
        text = read("d1")
        self.assertIn("f_N : ℂP¹ → ℂP¹", text)
        self.assertIn("f_N(0)=∞;  f_N(∞)=0", text)
        self.assertIn("not a repaired field quotient", text)
        self.assertNotIn("division by zero is defined in every field", text.lower())

    def test_chart_identity_and_bound_have_no_world_inference(self):
        for theta in (0.1, 0.7, math.pi / 2, 2.4, 3.0):
            phi = 1 / math.tan(theta / 2)
            nu = math.tan(theta / 2)
            balance = 2 / (phi + nu)
            self.assertAlmostEqual(phi * nu, 1.0, places=14)
            self.assertAlmostEqual(balance, math.sin(theta), places=14)
            self.assertLessEqual(balance, 1.0 + 1e-14)
        text = read("formula")
        self.assertIn("These are **chart facts only**", text)
        self.assertIn("It is not derived from `φ·ν=1`", text)

    def test_conjunctive_aggregators_are_not_interchangeable(self):
        a, b = (0.9, 0.2), (0.4, 0.4)
        product = lambda x: x[0] * x[1]
        minimum = lambda x: min(x)
        harmonic = lambda x: 0 if 0 in x else 2 / (1 / x[0] + 1 / x[1])
        cobb_douglas = lambda x: math.sqrt(x[0] * x[1])
        self.assertGreater(product(a), product(b))
        self.assertLess(minimum(a), minimum(b))
        for aggregator in (product, minimum, harmonic, cobb_douglas):
            self.assertEqual(aggregator((0.0, 0.7)), 0.0)
            self.assertGreaterEqual(aggregator((0.8, 0.9)), aggregator((0.7, 0.9)))
        self.assertIn("do not select\na unique formula", read("formula"))

    def test_perfect_foresight_zero_means_requires_a_budget_premise(self):
        phi_quality = 1.0
        unconstrained_means = 0.6
        self.assertEqual(phi_quality * unconstrained_means, unconstrained_means)

        budget = 1.0
        constrained_means = budget - phi_quality
        self.assertEqual(constrained_means, 0.0)
        self.assertEqual(phi_quality * constrained_means, 0.0)

        text = read("formula")
        self.assertIn("Φ+V≤1", text)
        self.assertIn("Without this budget premise", text)
        self.assertIn("perfect modeled foresight does **not** by itself", text)

        balance = read("balance")
        self.assertIn("Two different mathematical objects", balance)
        self.assertIn("The fixed-sum theorem", balance)
        self.assertIn("Without the budget", balance)

    def test_force_correspondence_is_independent_and_gauge_fenced(self):
        text = read("force")
        wagers = read("conjectures")
        for wager in ("W7a", "W7b", "W7c", "W7d", "W7e"):
            self.assertIn(wager, wagers)
        self.assertIn("roleAffinity", wagers)
        self.assertIn("not a completed unification", text.lower())
        self.assertIn("No evidence transfers", text)
        self.assertIn("A constant shift of gauge potential", text)
        self.assertIn("F_μν = ∂_μA_ν − ∂_νA_μ", text)
        self.assertIn("undifferentiated potential produces no\nlocal field force", text)
        self.assertIn("Aharonov–Bohm caveat", text)
        self.assertIn("An arbitrarily strong electromagnetic field is\nnot no field", text)
        self.assertRegex(text, r"invariant mass.*does not increase")

    def test_measurement_protocol_is_typed_and_noncircular(self):
        operational = read("operational")
        suda = read("suda_protocol")
        upgrade = read("upgrade")

        self.assertIn("| estimates | `Φ̂,V̂`", operational)
        self.assertNotIn("ν̂", operational)
        self.assertIn("`φν=1` is true by definition on the chart", operational)
        self.assertIn("`Φ̂V̂≈1` is not a\nchart identity", operational)
        self.assertIn("Selecting reciprocal pairs and then reporting reciprocal symmetry kills the", operational)
        self.assertIn("Authorization `U` and safety admissibility are independent typed\ngates", operational)
        self.assertIn("never build them into the `V̂` instrument", operational)

        self.assertIn("Do **not** construct or match pairs by setting `V̂=1/Φ̂`", suda)
        self.assertIn("selection step manufactured the advertised result", suda)
        self.assertIn("Even a positive result would support only the stated node-level hypothesis", suda)

        self.assertIn("`[A/B/S/I/D/C]` are evidence types, not rungs", upgrade)
        self.assertIn("L̇(x)=∇L(x)·f(x)≤0", upgrade)
        self.assertIn("is **not** “the Lyapunov function for F5”", upgrade)
        self.assertIn("candidate objective/potential only", upgrade)

    def test_legacy_force_thread_is_a_tombstone(self):
        text = read("steel")
        self.assertIn("HISTORICAL ARGUMENT MAP", text)
        self.assertIn("not current semantic authority", text)
        self.assertIn("original_git_blob: f24f3a31a4b2f0213c3698efcfc96597dab68cf9", text)
        self.assertIn("The GFS lane was retracted and archived", text)

        papers = read("papers_index")
        self.assertNotIn("Why 0 × ∞ = 1", papers)
        self.assertNotIn("Uncertainty as φν=1", papers)


class QuantumAndCausalityTests(unittest.TestCase):
    def test_valid_d3_states_carry_momentum_distributions(self):
        # A two-level density operator and a declared measurement already yield
        # a nontrivial distribution; no actual D4 click is needed to define it.
        rho = ((0.5, 0.0), (0.0, 0.5))
        projectors = (((1.0, 0.0), (0.0, 0.0)), ((0.0, 0.0), (0.0, 1.0)))
        probabilities = [sum(rho[i][j] * p[j][i] for i in range(2) for j in range(2)) for p in projectors]
        self.assertEqual(probabilities, [0.5, 0.5])
        text = read("d3")
        self.assertRegex(text, r"D3 supplies the\s+state-conditioned position and momentum distributions")
        self.assertRegex(text, r"The momentum operator\s+is therefore not created by D4")

    def test_history_space_lift_types_momentum_paths_and_long_tail(self):
        d3 = read("d3")
        d45 = read("d45")
        mu = read("mu")
        self.assertIn("Γ_T⁺", d3)
        self.assertIn("𝔓_Q(Ĝ_T)≥1−ε", d3)
        self.assertIn("path of\nmomentum distributions", d3)
        self.assertIn("not a unique, context-free classical path", d3)
        self.assertIn("Burri film-from-frames conjecture", d3)
        self.assertIn("unordered** set containing every D3 state", d3)
        self.assertIn("reconstructs motion but does not derive time", d3)
        self.assertRegex(d3, r"not a direct D3-to-D5\s+`μ`-crossing")
        self.assertIn("realized history γ*:", d45)
        self.assertIn("D4 actual", d45)
        self.assertIn("represented alternative history γ:", d45)
        self.assertIn("D5 possible", d45)
        self.assertIn("OptionCone_t(A) ⊆ Γ_T⁺", d45)
        self.assertIn("block-to-ensemble", d45)
        self.assertIn("Ω₅(Q,T)", d45)
        self.assertIn("parallel probable timelines", d45)
        self.assertIn("History-space composition is not another crossing", mu)
        self.assertIn("Saturation is not cardinal infinity", mu)
        self.assertIn("All probable timelines", mu)
        self.assertNotIn("μ₅:", mu)
        settled = read("settled")
        self.assertIn("`KSC-19` | History-space and block-to-ensemble lift", settled)
        self.assertIn("bounded “field of probable timelines.”", settled)
        self.assertIn("`KSC-20` | Light-cone/history-bundle split", settled)

    def test_uncertainty_is_retained_and_quantum_gravity_is_open(self):
        text = read("d3")
        self.assertIn("[X_i,P_j]=iℏδ_ijI", text)
        self.assertIn("uncertainty bound follows from\nnoncommutativity", text)
        self.assertIn("does not “solve” the Heisenberg", text)
        self.assertIn("complete, empirically confirmed high-energy theory of quantum gravity", text)
        self.assertIn("This is a research constraint, not a solution", text)
        self.assertIn("complex amplitudes**, not ordinary\nprobabilities", text)
        self.assertIn("“Everything is a wave” is therefore a heuristic", text)

    def test_d4_actual_tokens_represent_d5_possible_content(self):
        text = read("d45")
        self.assertIn("ModeledFutureToken:D4(actual)", text)
        self.assertIn("AlternativeContent:D5(possible)", text)
        self.assertRegex(text, r"The token, ranking event, and selection event\s+are actual")

    def test_commitment_and_world_outcome_are_separate(self):
        text = read("d45") + read("soul")
        self.assertIn("χ_t:(X_t,Ω_t,M_t,V_t,U_t,G_t) → (a_t,q_t)", text)
        self.assertIn("(X_{t+1},r_{t+1})", text)
        self.assertIn("The selector cannot manufacture its own consequence", text)
        self.assertIn("environment veto", text.lower())
        self.assertIn("null update", text.lower())

    def test_model_mediated_future_influence_is_present_causation(self):
        text = read("d45")
        self.assertIn("Changing the represented future can change the distribution of present\nactions", text)
        self.assertIn("current model state", text)
        self.assertIn("not future content physically propagating backward", text)

    def test_option_cones_do_not_expand_physical_light_cones(self):
        text = read("d45")
        self.assertIn("same physical causal cone and have different option\ncones", text)
        self.assertIn("It remains bounded by spacetime and\n`c`", text)
        self.assertIn("A D5 history bundle over the D4 light cone", text)
        self.assertIn("That geometric widening is D4 physical reachability. It does not count worlds", text)
        self.assertIn("N_eff(t)=exp(H_hist(t))", text)
        self.assertIn("width alone proves neither increasing branch count nor\nphysically parallel universes", text)

    def test_quantum_interpretation_removal_leaves_operational_core(self):
        d3_without_inset = section_without(read("d3"), "8. Interpretation fence")
        mu_without_inset = section_without(read("mu"), "7. Quantum core and removable interpretation inset")
        for fragment in ("ρ_S⪰0", "p(k | ρ,M) = Tr(ρE_k)", "D4MeasurementRecord"):
            self.assertIn(fragment, d3_without_inset)
        for fragment in ("MuCrossing := {", "CommitmentReceipt", "OutcomeReceipt"):
            self.assertIn(fragment, mu_without_inset)


class ValueAuthorityAndRoutingTests(unittest.TestCase):
    def test_power_max_cases_are_not_laundered(self):
        def classify(di: float, dh: float, justice: bool) -> tuple[bool, bool, bool]:
            moral = dh > 0 and di >= 0 and justice
            ethical = di > 0 and dh >= 0 and justice
            return moral, ethical, moral and ethical

        self.assertEqual(classify(0, 0, True), (False, False, False))
        self.assertEqual(classify(1, 1, True), (True, True, True))
        self.assertEqual(classify(2, -1, True), (False, False, False))
        self.assertEqual(classify(-1, 2, True), (False, False, False))
        self.assertEqual(classify(1, 1, False), (False, False, False))
        text = read("power")
        self.assertIn("Extraction can therefore benefit the extractor locally", text)
        self.assertIn("Voluntary sacrifice is a distinct costly class", text)

    def test_egregoreotype_requires_trace_intervention_and_cost(self):
        text = read("egregore")
        for fragment in (
            "persistent shared trace",
            "carrier turnover",
            "Measurable reweighting",
            "Recurrent objective-like bias",
            "Visible substrate costs",
        ):
            self.assertIn(fragment, text)
        self.assertRegex(text, r"not presumed to be a spirit, person, conscious mind")

    def test_one_owner_per_rung_and_kernel_surface(self):
        text = read("completion")
        dimension_rows = re.findall(r"^\| (D[0-6]|μ[₀-₄]|b₆|r₆) \|.*?\| `([^`]+)`|^\| (D[0-6]|μ[₀-₄]|b₆|r₆) \|.*?\| (μ owner above|D4/D5 owner above|closure owner above)", text, re.MULTILINE)
        # The table itself is the authority map; each expected identifier occurs
        # once as a row leader even where it refers back to an already named owner.
        for identifier in [f"D{n}" for n in range(7)] + [f"μ{c}" for c in "₀₁₂₃₄"] + ["b₆", "r₆"]:
            self.assertEqual(len(re.findall(rf"^\| {re.escape(identifier)} \|", text, re.MULTILINE)), 1, identifier)
        for surface in range(1, 8):
            self.assertEqual(len(re.findall(rf"^\| K-{surface} ", text, re.MULTILINE)), 1)
        self.assertNotIn("%", text)

        d1_head = "\n".join(read("d1").splitlines()[:8])
        d2_head = "\n".join(read("d2").splitlines()[:8])
        types_head = "\n".join(read("types").splitlines()[:24])
        self.assertIn("sole semantic owner", d1_head)
        self.assertIn("sole semantic owner", d2_head)
        self.assertIn("subordinate", types_head)
        self.assertNotIn("sole semantic owner", types_head)

    def test_projection_and_translation_never_own_a_rung(self):
        text = read("completion")
        self.assertIn("projection-only", text)
        self.assertIn("Rosetta | audit and translation method | transfers neither proof nor ontology", text)
        self.assertIn("Seed | reader projection", text)
        self.assertIn("website | publication projection", text)

    def test_active_markdown_links_resolve(self):
        active_roots = [ROOT / name for name in (
            "00_CONTROL",
            "00_META",
            "01_TELEOLOGY",
            "02_EPISTEMOLOGY",
            "03_METHODOLOGY",
            "04_AXIOLOGY",
            "05_COSMOLOGY",
            "06_ONTOLOGY",
            "07_THEOLOGY",
            "08_FRAMEWORK_SUPPORT",
            "09_TOOLS",
            "10_SEED",
        )]
        markdown_files: list[Path] = []
        markdown_files.extend(ROOT.glob("*.md"))
        for active_root in active_roots:
            markdown_files.extend(
                path
                for path in active_root.rglob("*.md")
                if not {"90_ARCHIVE", "91_COMPATIBILITY"}.intersection(path.relative_to(ROOT).parts)
                and not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
            )

        broken: list[str] = []
        link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
        fence_pattern = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)
        for path in sorted(set(markdown_files)):
            body = fence_pattern.sub("", path.read_text(encoding="utf-8"))
            for raw_target in link_pattern.findall(body):
                target = raw_target.strip()
                if target.startswith("<") and ">" in target:
                    target = target[1 : target.index(">")]
                else:
                    target = target.split(maxsplit=1)[0]
                if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
                    continue
                target = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not target or "\\" in target:
                    continue
                candidate = Path(target)
                resolved = candidate if candidate.is_absolute() else path.parent / candidate
                if not resolved.exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [], "Broken active Markdown links:\n" + "\n".join(broken))

    def test_legacy_crosswalks_cannot_restore_superseded_types(self):
        formal_index = read("formal_index")
        self.assertNotIn("Proof of D6 ≡ D0", formal_index)

        master = read("rosetta_master")
        self.assertIn("ACTIVE METHOD — never evidence or ontology", master)
        self.assertIn("`L0` and `L∞` are distinct chart-boundary", master)
        self.assertNotIn("**L0 = L∞.**", master)

        table = read("rosetta_table")
        self.assertIn("does not define a D-register", table)
        self.assertIn("not a causal law", master)
        self.assertNotIn("D6=D0", table)
        self.assertNotIn("**L0 = Linf.**", table)

        suda = read("suda_crosswalk")
        self.assertIn("not a D-register owner", suda)
        self.assertIn("two-sided real limit does not exist", suda)
        self.assertNotIn("μ₄→μ₅", suda)
        self.assertNotIn("μ₅→μ₆", suda)

        photon = read("photon_paper")
        self.assertIn("[C — withdrawn.]", photon)
        self.assertIn("do not imply `D6≡D0`", photon)

        for former_owner in (read("old_d6_owner"), read("old_d56_owner")):
            self.assertIn("status: \"SUPERSEDED", former_owner)
            self.assertIn("has no current semantic authority", former_owner)

    def test_notation_contract_and_core_lint(self):
        completion = read("completion")
        for fragment in (
            "`φ,ν` | lowercase reciprocal-chart coordinates",
            "`P∞=φν=1` | analytic chart identity",
            "`Φ` | present D4 measurement of D5 option-field quality or foresight",
            "`V` | D4 usable means",
            "`P_node=ΦV` | selected normalized conjunctive model",
            "`M⋆A` | present model-mediated influence",
        ):
            self.assertIn(fragment, completion)
        scoped = "\n".join(read(name) for name in ("formula", "d1", "d45", "soul", "power", "values"))
        for pattern in (r"P_node\s*[:=]+\s*φ", r"P_node\s*[:=]+\s*Φ\s*ν", r"\bν\s*(?:is|:=|=)\s*(?:usable )?means"):
            self.assertIsNone(re.search(pattern, scoped), pattern)

    def test_purity_gate_executes(self):
        process = subprocess.run(
            [sys.executable, str(ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertIn("EMERGENTISM PURITY: PASS", process.stdout)

    def test_purity_scope_excludes_compatibility_route_cards(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location("emergentism_purity_scope", checker)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        compatibility_card = ROOT / "91_COMPATIBILITY/AGENTS.md"
        self.assertFalse(module.is_active_route(compatibility_card))
        self.assertFalse(module.is_active_corpus_file(compatibility_card))

    def test_purity_tokenizer_catches_underscore_and_plural_forms(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location("emergentism_purity", checker)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for token in ("02_SKYZAI", "PENDING_K2", "DAVs", "DACs"):
            self.assertIsNotNone(module.FORBIDDEN.search(token), token)

    def test_source_negative_mutations_remain_absent(self):
        scoped = "\n".join(read(name) for name in PATHS if name != "topology")
        forbidden = (
            r"Sample\s*\[\s*∫[^\]]*\|ψ\|²",
            r"D6\s*≡\s*D0",
            r"physical (?:light )?cone (?:expands|widens)",
            r"Everett.{0,50}(?:fifth|5th|five-dimensional)",
            r"Copenhagen.{0,50}(?:fourth|4th|four-dimensional)",
            r"(?:solve[sd]?|solution to) quantum gravity",
            r"D3 has no momentum",
        )
        guards = (
            "not ",
            "no ",
            "never",
            "retired",
            "forbid",
            "reject",
            "prohibit",
            "fails if",
            "literal identity",
            "without",
        )
        for pattern in forbidden:
            for match in re.finditer(pattern, scoped, flags=re.IGNORECASE | re.DOTALL):
                context = scoped[max(0, match.start() - 180) : match.end() + 180].lower()
                self.assertTrue(any(guard in context for guard in guards), (pattern, context))

    def test_gfs_lane_is_archived_not_future_tense(self):
        active_roots = [ROOT / name for name in (
            "00_CONTROL", "00_META", "01_TELEOLOGY", "02_EPISTEMOLOGY",
            "03_METHODOLOGY", "04_AXIOLOGY", "05_COSMOLOGY", "06_ONTOLOGY",
            "07_THEOLOGY", "08_FRAMEWORK_SUPPORT", "09_TOOLS", "10_SEED",
        )]
        forbidden = (
            r"Proceed with GFS",
            r"Pending GFS",
            r"until GFS",
            r"GFS (?:test )?remains (?:the )?(?:confirmatory|useful)",
            r"GFS refinement",
            r"GFS.*\|\s*Staged\s*\|",
            r"GFS.*primary empirical tool",
        )
        violations: list[str] = []
        for active_root in active_roots:
            for path in active_root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in {
                    ".md", ".py", ".r", ".json", ".yaml", ".yml",
                }:
                    continue
                if path.resolve() == Path(__file__).resolve():
                    continue
                rel = path.relative_to(ROOT)
                if {"90_ARCHIVE", "91_COMPATIBILITY"}.intersection(rel.parts):
                    continue
                body = path.read_text(encoding="utf-8")
                for pattern in forbidden:
                    for match in re.finditer(pattern, body, flags=re.IGNORECASE):
                        line = body.count("\n", 0, match.start()) + 1
                        violations.append(f"{rel}:{line}: {match.group(0)}")
        self.assertEqual(
            violations,
            [],
            "Retired GFS lane remains live or future-tense:\n" + "\n".join(violations),
        )

    def test_active_nonhistorical_corpus_rejects_superseded_type_phrases(self):
        active_roots = [ROOT / name for name in (
            "00_CONTROL", "00_META", "01_TELEOLOGY", "02_EPISTEMOLOGY",
            "03_METHODOLOGY", "04_AXIOLOGY", "05_COSMOLOGY", "06_ONTOLOGY",
            "07_THEOLOGY", "08_FRAMEWORK_SUPPORT", "09_TOOLS", "10_SEED",
        )]
        patterns = (
            r"Many-Worlds\s*(?:is|=)\s*D5",
            r"Copenhagen\s*(?:is|=)\s*D4",
            r"D4\s+is\s+D5\s+after\s+measurement",
            r"D5\s*(?:is|=)\s*(?:lived\s+)?consciousness",
            r"torus\s+IS\s+the\s+light\s+cone",
            r"choice\s+is\s+modeled\s+as\s+the\s+μ-limit\s+transition",
            r"μ-limit\s+collapses\s+D5",
            r"(?:money|price)\s+(?:is|=)\s+the\s+Born\s+rule",
            r"D3\s*=\s*(?:life|bodies|transformation)",
            r"D4\s*=\s*(?:embodied\s+cognition|spacetime)",
            r"D4:\s*[\"“]?I[\"”]?\s+as\s+Witness",
            r"D5:\s*[\"“]?I[\"”]?\s+as\s+Agent",
            r"D5\s+is\s+strongly\s+emergent",
            r"D3\s+claims\s+translate\s+first\s+through\s+biology",
            r"D4\s+claims\s+translate\s+first\s+through\s+neuroscience",
        )
        historical_markers = (
            "historical compatibility", "historical research boundary",
            "historical peer-review artifact", "historical pressure-test boundary",
            "genesis document (pre-hardening", "status: \"superseded",
            "status: \"withdrawn", "archive_boundary:",
        )
        negative_guards = (
            "not ", "no ", "never", "reject", "forbid", "false", "dead",
            "former", "historical", "superseded", "coincidence", "without",
        )
        violations: list[str] = []
        for active_root in active_roots:
            for path in active_root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".json", ".yaml", ".yml"}:
                    continue
                rel = path.relative_to(ROOT)
                if {"90_ARCHIVE", "91_COMPATIBILITY"}.intersection(rel.parts):
                    continue
                body = path.read_text(encoding="utf-8")
                header = body[:2000].lower()
                if any(marker in header for marker in historical_markers):
                    continue
                for pattern in patterns:
                    for match in re.finditer(pattern, body, flags=re.IGNORECASE):
                        context = body[max(0, match.start() - 180) : match.end() + 180].lower()
                        if not any(guard in context for guard in negative_guards):
                            line = body.count("\n", 0, match.start()) + 1
                            violations.append(f"{rel}:{line}: {match.group(0)}")
        self.assertEqual(violations, [], "Superseded active type claims:\n" + "\n".join(violations))


if __name__ == "__main__":
    unittest.main()
