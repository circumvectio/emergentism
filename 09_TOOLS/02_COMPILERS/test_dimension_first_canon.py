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
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
LINK_CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_links.py"
link_spec = importlib.util.spec_from_file_location("check_links", LINK_CHECKER_PATH)
assert link_spec and link_spec.loader
link_checker = importlib.util.module_from_spec(link_spec)
link_spec.loader.exec_module(link_checker)

PATHS = {
    "completion": ROOT / "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md",
    "settled": ROOT / "00_META/00_SETTLED_CANON_REGISTRY.md",
    "claim_matrix": ROOT / "03_METHODOLOGY/00_CANONICAL_CLAIM_MATRIX.md",
    "ladder": ROOT / "03_METHODOLOGY/00_THE_DOCTRINAL_LADDER.md",
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
    "goal": ROOT / "01_TELEOLOGY/00_THE_GOAL.md",
    "compass": ROOT / "01_TELEOLOGY/04_THE_LIVED_COMPASS.md",
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
    "method_derivation": ROOT / "03_METHODOLOGY/01_THE_DERIVATION/00_THE_DERIVATION.md",
    "macro_paper": ROOT / "03_METHODOLOGY/02_THE_PAPERS/PAPER_X_INFORMATION_TOPOLOGY_AND_MACRO_CONSTRAINTS.md",
    "macro_prereg": ROOT / "03_METHODOLOGY/03_PREREGISTRATIONS/02_MACRO_CONSTRAINT_CAUSAL_EMERGENCE_PREREG.md",
    "actual_tests": ROOT / "03_METHODOLOGY/00_WHAT_ACTUALLY_TESTS_THE_THEORY.md",
    "protocol": ROOT / "08_FRAMEWORK_SUPPORT/00_THE_PROTOCOL.md",
    "remaining": ROOT / "00_META/00_THE_REMAINING_QUESTIONS.md",
    "hidden_center": ROOT / "01_TELEOLOGY/00_THE_HIDDEN_CENTER_OF_THE_FRAMEWORK.md",
    "memetics_index": ROOT / "02_EPISTEMOLOGY/03_MEMETICS/README.md",
    "old_transcendentals": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/16_EFR_TRANSCENDENTALS.md",
}

KSC02_PROJECTION_PATHS = {
    "seed_front": ROOT / "10_SEED/01_THE_SEED_LADDER/00_THE_SEED.md",
    "seed_d5": ROOT / "10_SEED/01_THE_SEED_LADDER/D5_THE_GAME.md",
    "rosetta_master": ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md",
    "d5_register": ROOT / "05_COSMOLOGY/00_D5_REGISTER_GAME_THEORY_AND_BEHAVIORAL_ECONOMICS.md",
    "core_concepts": ROOT / "08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_CORE_CONCEPTS.md",
    "anmut": ROOT / "04_AXIOLOGY/00_ANMUT_AND_DEMUT.md",
    "computational": ROOT / "05_COSMOLOGY/00_THE_COMPUTATIONAL_SPHERE.md",
}

KSC02_LATE_MIGRATION_PATHS = {
    "d32_math": ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_DOMAINS/D32_MATHEMATICS.md",
    "four_forces": ROOT / "01_TELEOLOGY/02_THE_DERIVATION/07_THE_FOUR_FORCES_ARE_THE_FOUR_LINES.md",
    "neoteny": ROOT / "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/39_NEOTENY_AS_F5_DELAY_AND_CULTURAL_WOMB.md",
    "saturation": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/45_SATURATION_CONTRAST_AND_APERTURE_BOUNDARY.md",
    "honest_position": ROOT / "02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md",
    "seed_d1": ROOT / "10_SEED/01_THE_SEED_LADDER/D1_ARITHMETIC.md",
    "seed_d2": ROOT / "10_SEED/01_THE_SEED_LADDER/D2_GEOMETRY.md",
    "seed_d4": ROOT / "10_SEED/01_THE_SEED_LADDER/D4_SPACETIME.md",
    "generative_table": ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_ROWS/00_GENERATIVE_TABLE.md",
    "papers_index": ROOT / "03_METHODOLOGY/02_THE_PAPERS/README.md",
    "knife": ROOT / "08_FRAMEWORK_SUPPORT/00_THE_KNIFE.md",
    "lens_foreword": ROOT / "08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS/FOREWORD.md",
    "amrita": ROOT / "07_THEOLOGY/00_THE_AMRITA.md",
    "old_godel": ROOT / "05_COSMOLOGY/03_FORMAL_SYSTEM/09_EFR_GODEL_CLARIFICATION.md",
    "old_mandelbrot": ROOT / "08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_66_Mandelbrot_Consciousness.md",
    "old_nietzsche": ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_ROWS/D14_ROSETTA_R5_NIETZSCHE.md",
    "old_civilisation": ROOT / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_CIVILISATIONAL.md",
    "old_application": ROOT / "01_TELEOLOGY/02_THE_DERIVATION/08_WHAT_WE_HAVENT_SAID.md",
}

KSC02_ONTOLOGY_PATHS = {
    "dof_owner": ROOT / "06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md",
    "axiom_owner": ROOT / "06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md",
    "kernel": ROOT / "06_ONTOLOGY/00_WELTANSCHAUUNG_KERNEL_v0.2_EMERGENTISM_ONLY.md",
    "weltanschauung": ROOT / "00_THE_WELTANSCHAUUNG.md",
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
            "never field arithmetic",
            "fences retained",
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

    def test_retired_titan_infix_is_locally_denied_on_active_surfaces(self):
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
        denial_markers = (
            "forbidden",
            "ill-typed",
            "invalid",
            "inadmissible",
            "retired",
            "superseded",
            "withdrawn",
            "not a titan equation",
            "no titan arithmetic",
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
                # Active history is not exempt. A literal retired infix may remain
                # only when its own local three-line window explicitly denies it.
                # Generic words such as "theorem", "analytic", "posit", or a
                # receipt number cannot turn ill-typed syntax into a lawful claim.
                lines = body.splitlines()
                for match in re.finditer(r"⊙\s*=\s*•\s*[×*]\s*○", body):
                    line = body.count("\n", 0, match.start()) + 1
                    start = max(0, line - 2)
                    stop = min(len(lines), line + 1)
                    window = "\n".join(lines[start:stop]).lower()
                    denied = any(marker in window for marker in denial_markers)
                    if not denied:
                        violations.append(f"{rel}:{line}: {match.group(0)} — NOT LOCALLY DENIED")
        self.assertEqual(
            violations,
            [],
            "Retired Titan infix appears without a local denial:\n" + "\n".join(violations),
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

    def test_ksc02_product_ranking_is_retired_but_selected_min_remains(self):
        a, b = (0.9, 0.2), (0.5, 0.5)
        product = lambda x: x[0] * x[1]
        rescale_phi = lambda x: x**10
        rescale_v = lambda x: x
        transform = lambda x: (rescale_phi(x[0]), rescale_v(x[1]))

        # The raw product ranks a particular cardinal presentation. KSC-02
        # therefore retires it as the ordinal node ranking while retaining min
        # as the framework's selected working model under a common transform.
        self.assertLess(product(a), product(b))
        self.assertGreater(product(transform(a)), product(transform(b)))
        self.assertFalse(a[0] >= b[0] and a[1] >= b[1])
        self.assertFalse(b[0] >= a[0] and b[1] >= a[1])

        owners = "\n".join(
            read(name)
            for name in ("completion", "claim_matrix", "ladder", "types", "goal", "compass")
        )
        self.assertIn("calibration contract", owners.lower())
        self.assertIn("P_node:=min(Φ̂₄,V₄)", owners)
        self.assertNotRegex(owners, r"P_node\s*:?=\s*Φ̂₄\s*[×*·]\s*V₄")

        settled = read("settled")
        formula = read("formula")
        self.assertIn("`P_node:=min(Φ̂₄,V₄)` is the selected working", settled)
        self.assertIn("**retired as a ranking**", settled)
        self.assertIn("P_node := C_min(Φ̂₄,V₄) := min(Φ̂₄,V₄)", formula)
        self.assertIn("It is not derived from `φ·ν=1`", formula)

    def test_ksc02_pareto_profile_does_not_displace_selected_min(self):
        pareto_geq = lambda x, y: x[0] >= y[0] and x[1] >= y[1]
        rescale_phi = lambda x: x**3
        rescale_v = lambda x: math.sqrt(x)
        transform = lambda x: (rescale_phi(x[0]), rescale_v(x[1]))

        profiles = (
            ((0.8, 0.7), (0.6, 0.4)),  # strict dominance
            ((0.9, 0.2), (0.5, 0.5)),  # incomparability
            ((0.3, 0.3), (0.3, 0.3)),  # equality
        )
        for a, b in profiles:
            self.assertEqual(pareto_geq(a, b), pareto_geq(transform(a), transform(b)))
            self.assertEqual(pareto_geq(b, a), pareto_geq(transform(b), transform(a)))

        owners = "\n".join(read(name) for name in ("formula", "types", "goal", "compass"))
        self.assertIn("independent strictly increasing reparameterizations", owners)
        self.assertIn("componentwise Pareto", owners)
        self.assertIn("P_node := C_min(Φ̂₄,V₄) := min(Φ̂₄,V₄)", owners)
        self.assertIn("applied to both factors", owners)

    def test_ksc02_downstream_surfaces_keep_selected_min_and_product_fence(self):
        active_names = (
            "method_derivation",
            "macro_paper",
            "macro_prereg",
            "actual_tests",
            "protocol",
            "remaining",
            "hidden_center",
            "memetics_index",
        )
        active = {name: read(name) for name in active_names}

        joined = "\n".join(active.values())
        self.assertRegex(joined, r"P_node\s*:?=\s*min")
        self.assertIn("N_node", joined)
        self.assertIn("calibration", joined.lower())
        self.assertRegex(joined.lower(), r"product[^\n]{0,120}retired|retired[^\n]{0,120}product")
        for name, body in active.items():
            self.assertNotRegex(body, r"P_node\s*:?=\s*(?:Φ̂₄|Phi_hat_4)\s*[×*·]\s*(?:V₄|V_4)", name)
            self.assertNotIn("ΣP_node", body, name)

        historical = read("old_transcendentals")
        self.assertIn("SUPERSEDED", historical)
        self.assertIn("no current semantic authority", historical.lower())
        self.assertIn("must not be cited", historical)

    def test_ksc02_reader_projections_preserve_selected_min_boundary(self):
        projection_names = (
            "seed_front",
            "seed_d5",
            "rosetta_master",
            "d5_register",
            "core_concepts",
        )
        for name in projection_names:
            body = KSC02_PROJECTION_PATHS[name].read_text(encoding="utf-8")
            self.assertRegex(body, r"P_node\s*:?=\s*min", name)
            self.assertNotRegex(body, r"P_node\s*:?=\s*Φ̂₄\s*[×*·]\s*V₄", name)
            self.assertNotIn("ΣΔP_node", body, name)

        joined = "\n".join(
            KSC02_PROJECTION_PATHS[name].read_text(encoding="utf-8")
            for name in projection_names
        )
        self.assertIn("human worth", joined)
        self.assertIn("N_node", joined)
        self.assertIn("Pareto", joined)
        self.assertIn("calibration contract", joined.lower())
        self.assertIn("P×,κ=Φ_cV_c", joined)

        for name in ("anmut", "computational"):
            body = KSC02_PROJECTION_PATHS[name].read_text(encoding="utf-8")
            self.assertNotIn("P_node = Φ × V", body, name)
            self.assertRegex(body, r"Canonical Formula Block|P_node", name)

    def test_ksc02_late_surfaces_and_legacy_quarantine(self):
        for name in ("d32_math", "four_forces", "neoteny", "saturation"):
            body = KSC02_LATE_MIGRATION_PATHS[name].read_text(encoding="utf-8")
            self.assertRegex(body, r"P_node\s*:?=\s*min", name)
            self.assertNotIn("Default calculation", body, name)
            self.assertNotRegex(body, r"P_node\s*:?=\s*Φ̂₄\s*[×*·]\s*V₄", name)

        d32 = KSC02_LATE_MIGRATION_PATHS["d32_math"].read_text(encoding="utf-8")
        self.assertIn("retired as a ranking", d32)
        self.assertIn("separately cardinal candidate", d32)

        current_projection_names = (
            "honest_position",
            "seed_d1",
            "seed_d2",
            "seed_d4",
            "generative_table",
            "papers_index",
            "knife",
            "lens_foreword",
        )
        for name in current_projection_names:
            body = KSC02_LATE_MIGRATION_PATHS[name].read_text(encoding="utf-8")
            self.assertRegex(body, r"P_node\s*:?=\s*min", name)
            self.assertNotRegex(body, r"P_node\s*:?=\s*Φ̂₄\s*[×*·]\s*V₄", name)

        joined = "\n".join(
            KSC02_LATE_MIGRATION_PATHS[name].read_text(encoding="utf-8")
            for name in ("d32_math", "four_forces", "neoteny", "saturation")
            + current_projection_names
        )
        self.assertIn("calibration contract", joined.lower())
        self.assertRegex(joined.lower(), r"cardinal")

        amrita = KSC02_LATE_MIGRATION_PATHS["amrita"].read_text(encoding="utf-8")
        self.assertIn("does **not** by itself", amrita)
        self.assertIn("uniquely select", amrita)
        self.assertIn("AND-class", amrita)

        for name in (
            "old_godel",
            "old_mandelbrot",
            "old_nietzsche",
            "old_civilisation",
            "old_application",
        ):
            body = KSC02_LATE_MIGRATION_PATHS[name].read_text(encoding="utf-8")
            self.assertIn("SUPERSEDED — no current semantic authority", body, name)
            self.assertIn("no current semantic authority", body.lower(), name)

    def test_ksc02_ontology_owners_distinguish_selected_min_from_forcing(self):
        bodies = {
            name: path.read_text(encoding="utf-8")
            for name, path in KSC02_ONTOLOGY_PATHS.items()
        }
        joined = "\n".join(bodies.values())
        self.assertRegex(joined, r"P_node\s*:?=\s*min")
        self.assertIn("calibration contract", joined.lower())
        self.assertIn("neither aggregator is forced", joined.lower())
        self.assertIn('never "product forced"', joined.lower())
        self.assertIn(
            "force no\nscalar at all",
            bodies["dof_owner"],
        )
        self.assertIn(
            "does not require a\nscalar",
            bodies["kernel"],
        )
        self.assertIn("no recovered default scalar", bodies["axiom_owner"].lower())

    def test_perfect_foresight_zero_means_requires_a_budget_premise(self):
        calibrated_phi = 1.0
        unconstrained_means = 0.6
        self.assertEqual(calibrated_phi * unconstrained_means, unconstrained_means)

        budget = 1.0
        constrained_means = budget - calibrated_phi
        self.assertEqual(constrained_means, 0.0)
        self.assertEqual(calibrated_phi * constrained_means, 0.0)

        text = read("formula")
        self.assertIn("Φ_c+V_c≤1", text)
        self.assertIn("Without this budget premise", text)
        self.assertRegex(text, r"perfect modeled foresight does \*\*not\*\* by\s+itself")

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

        self.assertIn("| finite node | `Φ₅,Φ̂₄,V₄,N_node`", operational)
        self.assertIn("| calibrated application | `Φ_c,V_c,C_κ(Φ_c,V_c)`", operational)
        self.assertNotIn("ν̂", operational)
        self.assertIn("`φν=1` is true by definition on the chart", operational)
        self.assertIn("`C_κ(Φ_c,V_c)≈1` is not a chart identity", operational)
        self.assertIn("Selecting reciprocal pairs and then reporting reciprocal symmetry kills the", operational)
        self.assertIn("Authorization `U` and safety admissibility are independent typed\ngates", operational)
        self.assertIn("never build them into the `V̂₄` instrument", operational)

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

    def test_markdown_link_guard_rejects_existing_target_outside_corpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture_root = Path(tmp)
            corpus = fixture_root / "corpus"
            corpus.mkdir()
            outside = fixture_root / "outside.md"
            outside.write_text("outside", encoding="utf-8")
            (corpus / "entry.md").write_text("[escape](../outside.md)", encoding="utf-8")

            original_root = link_checker.ROOT
            try:
                link_checker.ROOT = corpus
                broken, checked = link_checker.collect()
            finally:
                link_checker.ROOT = original_root

        self.assertEqual(checked, 1)
        self.assertEqual(len(broken), 1)
        self.assertIn("target escapes corpus", broken[0])

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
            "`Φ₅` / public `Φ` | D5 possible power",
            "`Φ̂₄=Eval₄(M,Φ₅)` | present D4 estimate of D5 possible power",
            "`V₄` / public `V` | D4 actual power",
            "`P_node=min(Φ̂₄,V₄)` / retired ranking `ΦV` | selected working AND-class score",
            "`M⋆A` | present model-mediated influence",
        ):
            self.assertIn(fragment, completion)
        scoped = "\n".join(read(name) for name in ("formula", "d1", "d45", "soul", "power", "values"))
        for pattern in (r"P_node\s*[:=]+\s*φ", r"P_node\s*[:=]+\s*Φ\s*ν", r"\bν\s*(?:is|:=|=)\s*(?:usable )?means"):
            self.assertIsNone(re.search(pattern, scoped), pattern)
        d45 = read("d45")
        self.assertIn("Φ₅,t := PossiblePower₅", d45)
        self.assertIn("Φ̂₄,t := Eval₄", d45)
        self.assertIn("not a physical force", d45)

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

    def test_purity_masks_only_complete_physical_receipt_filenames(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location("emergentism_purity_receipts", checker)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                receipt_lane = (
                    module.ROOT / "11_UPLINK/50_AUDITS_AND_EXECUTIONS"
                )
                receipt_lane.mkdir(parents=True)
                (receipt_lane / "123_K2_RECORD.md").write_text(
                    "historical target\n", encoding="utf-8"
                )
                fixture_targets = {
                    "123": [
                        "11_UPLINK/50_AUDITS_AND_EXECUTIONS/123_K2_RECORD.md"
                    ]
                }
                fixture_digest = module.hashlib.sha256(
                    json.dumps(
                        fixture_targets,
                        sort_keys=True,
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest()
                module.EXPECTED_RECEIPT_TARGET_UNIVERSE_SHA256 = fixture_digest
                module.EXPECTED_RECEIPT_TARGET_COUNT = 1
                registry = module.ROOT / module.RECEIPT_TARGET_REGISTRY
                registry.parent.mkdir(parents=True, exist_ok=True)
                registry.write_text(
                    json.dumps(
                        {
                            "receipt_universe": {
                                "all_candidate_paths_sha256": fixture_digest,
                                "citable_targets": 1,
                            }
                        }
                    ),
                    encoding="utf-8",
                )
                source = module.ROOT / "00_META/source.md"
                source.parent.mkdir(parents=True, exist_ok=True)

                source.write_text(
                    "See `123_K2_RECORD.md`.\n", encoding="utf-8"
                )
                self.assertEqual(module.scan_file(source), [])

                source.write_text(
                    "See `11_UPLINK/50_AUDITS_AND_EXECUTIONS/123_K2_RECORD.md#scope`.\n",
                    encoding="utf-8",
                )
                self.assertEqual(module.scan_file(source), [])

                source.write_text(
                    "See `123_K2_RECORD.md.bak`.\n", encoding="utf-8"
                )
                spoof_errors = module.scan_file(source)
                self.assertEqual(len(spoof_errors), 1, spoof_errors)
                self.assertIn("forbidden authority token 'K2'", spoof_errors[0])

                source.write_text(
                    "See `123_K2_RECORD.md/authority`.\n", encoding="utf-8"
                )
                slash_errors = module.scan_file(source)
                self.assertEqual(len(slash_errors), 1, slash_errors)
                self.assertIn("forbidden authority token 'K2'", slash_errors[0])

                source.write_text(
                    "See `999_K2_NONEXISTENT.md`.\n", encoding="utf-8"
                )
                nonexistent_errors = module.scan_file(source)
                self.assertEqual(len(nonexistent_errors), 1, nonexistent_errors)
                self.assertIn(
                    "forbidden authority token 'K2'", nonexistent_errors[0]
                )

                (receipt_lane / "123_K2_RECORD.md").unlink()
                source.write_text(
                    "See `123_K2_RECORD.md`.\n", encoding="utf-8"
                )
                deleted_errors = module.scan_file(source)
                self.assertEqual(len(deleted_errors), 1, deleted_errors)
                self.assertIn("receipt target inventory invalid", deleted_errors[0])

                (receipt_lane / "123_K2_RECORD.md").write_text(
                    "historical target\n", encoding="utf-8"
                )

                source.write_text(
                    "K2 is authority; see `123_K2_RECORD.md`.\n",
                    encoding="utf-8",
                )
                prose_errors = module.scan_file(source)
                self.assertEqual(len(prose_errors), 1, prose_errors)
                self.assertIn("forbidden authority token 'K2'", prose_errors[0])
            finally:
                module.ROOT = original_root

    def test_purity_excludes_exact_dedicated_generated_custody_surfaces(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location("emergentism_purity_registry", checker)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        registry = ROOT / "00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json"
        lookalike = ROOT / "00_META/ACTIVE_RECEIPT_CITATION_REGISTRY_COPY.json"
        contact_snapshot = ROOT / "00_META/CONTACT_LIMITED_STATE.json"
        self.assertFalse(module.is_active_corpus_file(registry))
        self.assertFalse(module.is_active_corpus_file(contact_snapshot))
        self.assertTrue(module.is_active_corpus_file(lookalike))
        self.assertEqual(
            module.DERIVED_CUSTODY_SURFACES,
            {
                Path("00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json"),
                Path("00_META/CONTACT_LIMITED_STATE.json"),
            },
        )

    def test_purity_scans_every_forbidden_token_on_an_allowed_projection_line(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location("emergentism_purity_all_matches", checker)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(
            module.CONTROL_PROJECTION_PATHS,
            (Path("VMOSK_A.md"), Path("VMOSK_A_v2_2026_07_31.md")),
        )

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                projection_reference = module.ROOT / "README.md"
                projection_reference.write_text(
                    "VMOSK_A.md is a non-semantic projection; K2 may not become authority.\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(projection_reference)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("forbidden authority token 'K2'", errors[0])

    def test_purity_exact_navigation_filename_allowance_does_not_spread_to_sibling(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_navigation_locator_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.scan_file(ROOT / "README.md"), [])
        self.assertEqual(
            module.scan_file(ROOT / "01_TELEOLOGY/02_THE_DERIVATION/README.md"),
            [],
        )

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                sibling = (
                    module.ROOT
                    / "01_TELEOLOGY/02_THE_DERIVATION/unlisted_sibling.md"
                )
                sibling.parent.mkdir(parents=True)
                sibling.write_text(
                    "[`07_THE_TYSON_KO_PENDING_K2.md`]"
                    "(07_THE_TYSON_KO_PENDING_K2.md)\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(sibling)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 2, errors)
        self.assertTrue(
            all("forbidden authority token 'K2'" in error for error in errors),
            errors,
        )

    def test_purity_exact_provenance_path_allowances_do_not_spread_to_siblings(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_provenance_path_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ladder = ROOT / (
            "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/"
            "35_THE_LADDER_AND_THE_TWO_PARTITIONS_2026_08_05.md"
        )
        book_control = ROOT / "13_BOOKS/VMOSK_A.md"
        self.assertEqual(module.scan_file(ladder), [])
        self.assertEqual(module.scan_file(book_control), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                audit_sibling = (
                    module.ROOT
                    / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/unlisted.md"
                )
                audit_sibling.parent.mkdir(parents=True)
                audit_sibling.write_text(
                    "[audit](../../../00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/"
                    "L2_CLAIM_VS_EVIDENCE_AUDIT_2026_07_20.md)\n",
                    encoding="utf-8",
                )
                audit_errors = module.scan_file(audit_sibling)

                book_sibling = module.ROOT / "13_BOOKS/unlisted.md"
                book_sibling.parent.mkdir(parents=True)
                book_sibling.write_text(
                    "[boundary](../12_PUBLIC_SITE/VMOSK_A.md#s--strategies-s)\n",
                    encoding="utf-8",
                )
                book_errors = module.scan_file(book_sibling)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(audit_errors), 1, audit_errors)
        self.assertIn("forbidden authority token 'k2'", audit_errors[0])
        self.assertEqual(len(book_errors), 1, book_errors)
        self.assertIn("forbidden authority token 'VMOSK_A'", book_errors[0])

    def test_purity_digest_pinned_executable_rejects_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_tooling_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/semantics.py")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + '\nAUTHORITY_ASSERTION = "K2 is semantic authority"\n',
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("frozen tooling digest drift", errors[0])

    def test_purity_mutable_compiler_rejects_unreviewed_authority_unit(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_compiler_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("09_TOOLS/02_COMPILERS/compile_claim_cards.py")
        source = ROOT / relative

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + '\nEXTERNAL_AUTHORITY = "Skyzai governs Emergentism"\n',
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("forbidden authority token 'Skyzai'", errors[0])

    def test_purity_generated_book_rejects_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_book_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1.md")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + "\nK2 is the generated book's semantic authority.\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("forbidden authority token 'K2'", errors[0])

    def test_purity_external_mapping_audit_rejects_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_mapping_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("02_EPISTEMOLOGY/00_HOLOBIONT_MEMBRANE_v0.1.md")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + "\nSkyzai governs Emergentism.\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("external-mapping audit digest drift", errors[0])

    def test_purity_book_manifest_rejects_non_locator_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_manifest_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("13_BOOKS/book-manifest.json")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                document = json.loads(source.read_text(encoding="utf-8"))
                document["authority"] = "../02_SKYZAI governs Emergentism"
                mutated.write_text(
                    json.dumps(document, indent=2) + "\n", encoding="utf-8"
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("forbidden authority token 'SKYZAI'", errors[0])

    def test_purity_historical_lineage_requires_exact_reviewed_source_path(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_lineage_path_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("00_META/claim_cards/self_eating_serpent.yaml")
        source = ROOT / relative
        expected = module.HISTORICAL_LINEAGE_SOURCE_PATHS[relative]
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                changed = source.read_text(encoding="utf-8").replace(
                    expected,
                    "../02_SKYZAI/K2-governs-Emergentism.md",
                    1,
                )
                self.assertNotEqual(changed, source.read_text(encoding="utf-8"))
                mutated.write_text(changed, encoding="utf-8")
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any("forbidden authority token 'K2'" in error for error in errors),
            errors,
        )

    def test_purity_historical_inline_locator_requires_exact_reviewed_path(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_inline_path_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path(
            "13_BOOKS/manifesto/chapters/PART_IV_V_RESEARCH_GENEALOGY.md"
        )
        source = ROOT / relative
        expected = module.HISTORICAL_INLINE_EXACT_SOURCE_PATHS[relative]
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                changed = source.read_text(encoding="utf-8").replace(
                    expected,
                    "../../02_SKYZAI/K2-governs-Emergentism.md",
                    1,
                )
                self.assertNotEqual(changed, source.read_text(encoding="utf-8"))
                mutated.write_text(changed, encoding="utf-8")
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any("forbidden authority token 'K2'" in error for error in errors),
            errors,
        )

    def test_purity_edition_frontmatter_requires_exact_reviewed_path(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_edition_path_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("13_BOOKS/self_eating_serpent/CRITICAL_EDITION_1.md")
        source = ROOT / relative
        _, expected = module.STRUCTURED_EXTERNAL_SOURCE_MARKDOWN_FIELDS[relative]
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                changed = source.read_text(encoding="utf-8").replace(
                    expected,
                    "../../../02_SKYZAI/K2-governs-Emergentism.md",
                    1,
                )
                self.assertNotEqual(changed, source.read_text(encoding="utf-8"))
                mutated.write_text(changed, encoding="utf-8")
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any("forbidden authority token 'K2'" in error for error in errors),
            errors,
        )

    def test_purity_control_reference_does_not_mask_second_same_line_token(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_control_reference_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                source = module.ROOT / "README.md"
                source.write_text(
                    "VMOSK_A.md is non-semantic; VMOSK governs Emergentism.\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(source)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("forbidden authority token 'VMOSK'", errors[0])

    def test_purity_control_projection_rejects_new_authority_unit(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_control_projection_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("VMOSK_A.md")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + "\nVMOSK governs Emergentism.\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("forbidden authority token 'VMOSK'", errors[0])

    def test_purity_managed_agent_projection_rejects_mutation_and_new_sibling(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_managed_agent_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = (
            module.MANAGED_AGENT_PROJECTION_ROOT
            / "QUALITY_QUANTITY_BALANCE_LAW_2026_07_22.md"
        )
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + "\nSkyzai governs Emergentism.\n",
                    encoding="utf-8",
                )
                mutation_errors = module.scan_file(mutated)

                sibling = (
                    module.ROOT
                    / module.MANAGED_AGENT_PROJECTION_ROOT
                    / "UNLISTED_AUTHORITY.md"
                )
                sibling.write_text(
                    "Skyzai governs Emergentism.\n", encoding="utf-8"
                )
                self.assertTrue(module.is_active_corpus_file(sibling))
                sibling_errors = module.scan_file(sibling)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(mutation_errors), 1, mutation_errors)
        self.assertIn("managed-agent projection digest drift", mutation_errors[0])
        self.assertEqual(len(sibling_errors), 1, sibling_errors)
        self.assertIn("forbidden authority token 'Skyzai'", sibling_errors[0])

    def test_purity_self_checker_rejects_unreviewed_authority_unit(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_self_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        source = ROOT / module.SELF_VALIDATED_TOOLING_PATH
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / module.SELF_VALIDATED_TOOLING_PATH
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + '\nUNREVIEWED_AUTHORITY = "Skyzai governs Emergentism"\n',
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any("self-validated tooling semantic-unit drift" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("forbidden authority token 'Skyzai'" in error for error in errors),
            errors,
        )

    def test_purity_frozen_lint_tooling_rejects_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_lint_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("09_TOOLS/01_SCRIPTS/lint_rule_tokens.py")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + '\nAUTHORITY = "Skyzai governs Emergentism"\n',
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("frozen tooling digest drift", errors[0])

    def test_purity_foundation_tool_rejects_unreviewed_authority_unit(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_foundation_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("09_TOOLS/01_SCRIPTS/check_foundation.py")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + '\nAUTHORITY = "Skyzai governs Emergentism"\n',
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("forbidden authority token 'Skyzai'", errors[0])

    def test_purity_frozen_test_fixture_rejects_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_test_fixture_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("09_TOOLS/02_COMPILERS/test_dimension_first_canon.py")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + '\nAUTHORITY = "Skyzai governs Emergentism"\n',
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("frozen tooling digest drift", errors[0])

    def test_purity_frozen_forwarder_rejects_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_forwarder_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path(
            "08_FRAMEWORK_SUPPORT/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK_MOVED.md"
        )
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + "\nSkyzai governs Emergentism.\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("frozen provenance digest drift", errors[0])

    def test_purity_frozen_filename_receipt_rejects_authority_mutation(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_filename_receipt_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path(
            "08_FRAMEWORK_SUPPORT/03_EVIDENCE/COMPARATIVE/"
            "2026_06_05_FILENAME_REPAIR_RECEIPT.md"
        )
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + "\nSkyzai governs Emergentism.\n",
                    encoding="utf-8",
                )
                errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("frozen provenance digest drift", errors[0])

    def test_purity_dedicated_file_symlink_cannot_satisfy_digest(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_file_symlink_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("09_TOOLS/01_SCRIPTS/lint_rule_tokens.py")
        source = ROOT / relative

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                linked = module.ROOT / relative
                linked.parent.mkdir(parents=True)
                linked.symlink_to(source)
                errors = module.scan_file(linked)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("crosses symlink component", errors[0])

    def test_purity_generic_active_file_symlink_fails_before_read(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_generic_file_symlink_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                target = module.ROOT / "source.data"
                target.write_text("Skyzai governs Emergentism.\n", encoding="utf-8")
                linked = module.ROOT / "00_META/generic.md"
                linked.parent.mkdir(parents=True)
                linked.symlink_to(target)
                errors = module.scan_file(linked)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("scoped path", errors[0])
        self.assertIn("crosses symlink component", errors[0])

    def test_purity_generic_active_parent_symlink_fails_before_read(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_generic_parent_symlink_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_root, tempfile.TemporaryDirectory() as source_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                external = Path(source_root)
                (external / "generic.md").write_text(
                    "Skyzai governs Emergentism.\n", encoding="utf-8"
                )
                parent = module.ROOT / "00_META"
                parent.symlink_to(external, target_is_directory=True)
                errors = module.scan_file(parent / "generic.md")
                tree_errors = module.active_tree_symlink_errors()
            finally:
                module.ROOT = original_root

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("scoped path", errors[0])
        self.assertIn("crosses symlink component", errors[0])
        self.assertEqual(
            tree_errors,
            ["active corpus contains symlink entry: 00_META"],
        )

    def test_purity_required_archive_file_symlink_fails_custody(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_archive_file_symlink_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = module.REQUIRED_ARCHIVE_CUSTODY_PATHS[0]
        source = ROOT / relative

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                linked = module.ROOT / relative
                linked.parent.mkdir(parents=True)
                linked.symlink_to(source)
                errors = module.required_archive_custody_errors()
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any(
                str(relative) in error and "crosses symlink component" in error
                for error in errors
            ),
            errors,
        )

    def test_purity_required_archive_parent_symlink_fails_custody(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_archive_parent_symlink_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = module.REQUIRED_ARCHIVE_CUSTODY_PATHS[0]

        with tempfile.TemporaryDirectory() as temporary_root, tempfile.TemporaryDirectory() as source_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                external = Path(source_root)
                (external / relative.name).write_text("archive\n", encoding="utf-8")
                linked_parent = module.ROOT / relative.parent
                linked_parent.parent.mkdir(parents=True)
                linked_parent.symlink_to(external, target_is_directory=True)
                errors = module.required_archive_custody_errors()
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any(
                str(relative.parent) in error
                and "crosses symlink component" in error
                for error in errors
            ),
            errors,
        )

    def test_purity_reviewed_projection_history_and_archive_links_fail_closed(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_reviewed_history_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for relative in module.REVIEWED_PROJECTION_HISTORY_SHA256:
            self.assertEqual(module.scan_file(ROOT / relative), [])
        for relative in module.EXACT_ARCHIVE_PROVENANCE_LINKS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertEqual(
                module.exact_archive_provenance_link_errors(relative, text), []
            )

        public_relative = Path("12_PUBLIC_SITE/00_THE_RUNGS_2026_08_05.md")
        public_source = ROOT / public_relative
        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / public_relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    public_source.read_text(encoding="utf-8")
                    + "\nSkyzai governs Emergentism.\n",
                    encoding="utf-8",
                )
                mutation_errors = module.scan_file(mutated)
            finally:
                module.ROOT = original_root
        self.assertEqual(len(mutation_errors), 1, mutation_errors)
        self.assertIn("reviewed projection/history digest drift", mutation_errors[0])

        link_relative = Path("00_META/00_THE_CORPUS_SPINE.md")
        locator, _, _ = module.EXACT_ARCHIVE_PROVENANCE_LINKS[link_relative]
        mutated_text = (ROOT / link_relative).read_text(encoding="utf-8").replace(
            locator, locator.replace("57_TITAN", "58_TITAN"), 1
        )
        link_errors = module.exact_archive_provenance_link_errors(
            link_relative, mutated_text
        )
        self.assertEqual(
            link_errors,
            [f"exact archive-provenance link inventory drift: {link_relative}"],
        )

    def test_purity_receipt_filename_allowance_rejects_file_symlink(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_receipt_file_symlink_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                audit_lane = module.ROOT / module.RECEIPT_CITATION_LANES[0]
                packet_lane = module.ROOT / module.RECEIPT_CITATION_LANES[1]
                audit_lane.mkdir(parents=True)
                packet_lane.mkdir(parents=True)
                target = module.ROOT / "target.data"
                target.write_text("historical\n", encoding="utf-8")
                (audit_lane / "126_FAKE_K2.md").symlink_to(target)
                with self.assertRaisesRegex(ValueError, "symlink"):
                    module.physical_receipt_target_names(module.ROOT)
            finally:
                module.ROOT = original_root

    def test_purity_receipt_filename_allowance_rejects_unregistered_regular_target(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_receipt_inventory_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                audit_lane = module.ROOT / module.RECEIPT_CITATION_LANES[0]
                packet_lane = module.ROOT / module.RECEIPT_CITATION_LANES[1]
                audit_lane.mkdir(parents=True)
                packet_lane.mkdir(parents=True)
                (audit_lane / "126_FAKE_K2.md").write_text(
                    "historical\n", encoding="utf-8"
                )
                registry = module.ROOT / module.RECEIPT_TARGET_REGISTRY
                registry.parent.mkdir(parents=True, exist_ok=True)
                registry.write_text(
                    json.dumps(
                        {
                            "receipt_universe": {
                                "all_candidate_paths_sha256": module.EXPECTED_RECEIPT_TARGET_UNIVERSE_SHA256,
                                "citable_targets": module.EXPECTED_RECEIPT_TARGET_COUNT,
                            }
                        }
                    ),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, "exact active-registry binding"):
                    module.physical_receipt_target_names(module.ROOT)
            finally:
                module.ROOT = original_root

    def test_purity_managed_projection_rejects_directory_symlink_and_extra_dir(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_managed_shape_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        source_root = ROOT / module.MANAGED_AGENT_PROJECTION_ROOT

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                linked_root = module.ROOT / module.MANAGED_AGENT_PROJECTION_ROOT
                linked_root.mkdir(parents=True)
                (linked_root / "agents").symlink_to(
                    source_root / "agents", target_is_directory=True
                )
                symlink_errors = module.managed_agent_projection_errors()
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any("symlink component" in error for error in symlink_errors),
            symlink_errors,
        )

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                copied_root = module.ROOT / module.MANAGED_AGENT_PROJECTION_ROOT
                copied_root.parent.mkdir(parents=True)
                shutil.copytree(source_root, copied_root)
                (copied_root / "UNEXPECTED_EMPTY_DIRECTORY").mkdir()
                extra_dir_errors = module.managed_agent_projection_errors()
            finally:
                module.ROOT = original_root

        self.assertTrue(
            any("inventory drift" in error for error in extra_dir_errors),
            extra_dir_errors,
        )
        self.assertTrue(
            any("UNEXPECTED_EMPTY_DIRECTORY" in error for error in extra_dir_errors),
            extra_dir_errors,
        )

    def test_purity_distillation_projection_rejects_mutation_and_new_sibling(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_distillation_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.distillation_projection_errors(), [])
        relative = Path("14_THE_DISTILLATION/00_THE_RUNGS_2026_08_05.md")
        source = ROOT / relative
        self.assertEqual(module.scan_file(source), [])

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                mutated = module.ROOT / relative
                mutated.parent.mkdir(parents=True)
                mutated.write_text(
                    source.read_text(encoding="utf-8")
                    + "\nSkyzai governs Emergentism.\n",
                    encoding="utf-8",
                )
                mutation_errors = module.scan_file(mutated)

                sibling = module.ROOT / "14_THE_DISTILLATION/unlisted.md"
                sibling.write_text(
                    "Skyzai governs Emergentism.\n", encoding="utf-8"
                )
                sibling_errors = module.scan_file(sibling)
            finally:
                module.ROOT = original_root

        self.assertEqual(len(mutation_errors), 1, mutation_errors)
        self.assertIn("distillation projection digest drift", mutation_errors[0])
        self.assertEqual(len(sibling_errors), 1, sibling_errors)
        self.assertIn("forbidden authority token 'Skyzai'", sibling_errors[0])

    def test_purity_distillation_projection_rejects_file_and_directory_symlinks(self):
        checker = ROOT / "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
        spec = importlib.util.spec_from_file_location(
            "emergentism_purity_distillation_symlink_mutation", checker
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = Path("14_THE_DISTILLATION/00_THE_AMRITA.md")
        source = ROOT / relative

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                linked = module.ROOT / relative
                linked.parent.mkdir(parents=True)
                linked.symlink_to(source)
                file_errors = module.distillation_projection_errors()
            finally:
                module.ROOT = original_root
        self.assertTrue(
            any("symlink" in error for error in file_errors), file_errors
        )

        with tempfile.TemporaryDirectory() as temporary_root:
            original_root = module.ROOT
            module.ROOT = Path(temporary_root)
            try:
                linked_root = module.ROOT / module.DISTILLATION_PROJECTION_ROOT
                linked_root.parent.mkdir(parents=True, exist_ok=True)
                linked_root.symlink_to(
                    ROOT / module.DISTILLATION_PROJECTION_ROOT,
                    target_is_directory=True,
                )
                directory_errors = module.distillation_projection_errors()
            finally:
                module.ROOT = original_root
        self.assertTrue(
            any("crosses symlink component" in error for error in directory_errors),
            directory_errors,
        )

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
