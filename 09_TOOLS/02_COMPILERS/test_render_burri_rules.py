"""Focused contract tests for the typed, deterministic Burri SVG renderer."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET


REPO_ROOT = Path(__file__).resolve().parents[2]
COMPILER = Path(__file__).with_name("render_burri_rules.py")
TOPOLOGY = REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_TOPOLOGY.json"
OUTPUTS = {
    "proof": REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_PLATE.svg",
    "emblem": REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_EMBLEM.svg",
}
RULE_IDS = {f"BR-{number}" for number in range(1, 7)}
REGISTERS = {f"D{number}" for number in range(7)}
KINDS = {"state", "frame", "crossing", "commitment", "receipt", "trace"}
MODALITIES = {"actual", "possible"}
ROLES = {"forward", "feedback", "coupling"}
TIERS = {"A", "B", "S", "I", "D", "C"}


def load_renderer():
    spec = importlib.util.spec_from_file_location("render_burri_rules", COMPILER)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot import {COMPILER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class TopologyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = load_renderer()
        cls.topology = cls.api.load_topology(TOPOLOGY)

    def test_public_api_and_required_sections(self):
        for name in (
            "load_topology",
            "validate_topology",
            "topology_sha256",
            "render_view",
            "write_outputs",
            "check_outputs",
            "main",
        ):
            self.assertTrue(callable(getattr(self.api, name, None)), name)
        self.assertTrue(
            {
                "schemaVersion",
                "rules",
                "sources",
                "schemas",
                "nodes",
                "edges",
                "views",
            }
            <= self.topology.keys()
        )
        self.assertEqual(self.topology["schemaVersion"], "0.2")
        self.assertEqual(self.api.validate_topology(self.topology, REPO_ROOT), [])

    def test_exact_six_rules_and_enum_contract(self):
        self.assertEqual({rule["id"] for rule in self.topology["rules"]}, RULE_IDS)
        source_ids = {source["id"] for source in self.topology["sources"]}
        for node in self.topology["nodes"]:
            self.assertIn(node["kind"], KINDS)
            self.assertIn(node["dRegister"], REGISTERS)
            self.assertIn(node["modality"], MODALITIES)
            self.assertIn(node["role"], ROLES)
            self.assertIn(node["tier"], TIERS)
            self.assertTrue(node["ruleIds"] and set(node["ruleIds"]) <= RULE_IDS)
            self.assertTrue(node["sourceIds"] and set(node["sourceIds"]) <= source_ids)
        for edge in self.topology["edges"]:
            self.assertIn(edge["dRegister"], REGISTERS)
            self.assertIn(edge["modality"], MODALITIES)
            self.assertIn(edge["role"], ROLES)
            self.assertIn(edge["tier"], TIERS)
            self.assertTrue(edge["ruleIds"] and set(edge["ruleIds"]) <= RULE_IDS)
            self.assertTrue(edge["sourceIds"] and set(edge["sourceIds"]) <= source_ids)

    def test_ids_are_unique_and_edges_have_valid_endpoints(self):
        elements = self.topology["nodes"] + self.topology["edges"]
        ids = [item["id"] for item in elements]
        self.assertEqual(len(ids), len(set(ids)))
        node_ids = {node["id"] for node in self.topology["nodes"]}
        self.assertTrue(
            all(edge["from"] in node_ids and edge["to"] in node_ids for edge in self.topology["edges"])
        )
        mutant = copy.deepcopy(self.topology)
        mutant["nodes"].append(copy.deepcopy(mutant["nodes"][0]))
        self.assertTrue(any("globally unique" in error for error in self.api.validate_topology(mutant, REPO_ROOT)))

    def test_sources_exist_and_frozen_trees_are_not_dependencies(self):
        for source in self.topology["sources"]:
            if "path" not in source:
                self.assertTrue(source["url"].startswith("https://"))
                continue
            path = Path(source["path"])
            self.assertFalse(path.is_absolute())
            self.assertFalse({"12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"} & set(path.parts))
            self.assertTrue((REPO_ROOT / path).is_file(), source["path"])
        mutant = copy.deepcopy(self.topology)
        mutant["sources"][0]["path"] = "90_ARCHIVE/forbidden.md"
        errors = self.api.validate_topology(mutant, REPO_ROOT)
        self.assertTrue(any("frozen tree" in error for error in errors))

    def test_exact_register_spine_crossings_and_non_mu_closure(self):
        nodes = self.topology["nodes"]
        self.assertTrue({f"d{number}" for number in range(7)} <= {node["id"] for node in nodes})
        crossings = {node["id"] for node in nodes if node["kind"] == "crossing"}
        self.assertEqual(crossings, {f"mu-{number}" for number in range(6)})
        self.assertNotIn("mu-6", json.dumps(self.topology, ensure_ascii=False).lower())
        closures = [edge for edge in self.topology["edges"] if edge.get("edgeType") == "closure"]
        self.assertEqual(len(closures), 1)
        self.assertEqual(
            (closures[0]["id"], closures[0]["from"], closures[0]["to"]),
            ("r6", "d6", "d0"),
        )
        self.assertTrue(closures[0]["closure"])

    def test_mu_records_expose_empty_evidence_without_pretending_it_is_evidence(self):
        crossings = [node for node in self.topology["nodes"] if node["kind"] == "crossing"]
        self.assertEqual(len(crossings), 6)
        for number, crossing in enumerate(sorted(crossings, key=lambda item: item["id"])):
            self.assertEqual(crossing["source"], f"D{number}")
            self.assertEqual(crossing["target"], f"D{number + 1}")
            self.assertEqual(crossing["saturationEvidence"], [])
            self.assertEqual(crossing["evidenceStatus"], "not_yet_supplied")
            for field in (
                "saturatedRegister",
                "newFreedomOrBoundaryResult",
                "lowerRegisterRecovery",
                "reductionStatus",
                "prediction",
                "killCriterion",
            ):
                self.assertTrue(crossing[field], (crossing["id"], field))

    def test_mu_evidence_status_invariant_is_fail_closed(self):
        for mutation, fragment in (
            (("evidenceStatus", "supplied"), "supplied evidence status requires evidence"),
            (("saturationEvidence", "prose is not a list"), "must be a list"),
        ):
            with self.subTest(mutation=mutation):
                mutant = copy.deepcopy(self.topology)
                crossing = next(node for node in mutant["nodes"] if node["id"] == "mu-0")
                crossing[mutation[0]] = mutation[1]
                self.assertTrue(
                    any(fragment in error for error in self.api.validate_topology(mutant, REPO_ROOT))
                )
        mutant = copy.deepcopy(self.topology)
        next(node for node in mutant["nodes"] if node["id"] == "mu-0")[
            "saturationEvidence"
        ] = [{"sourceId": "x"}]
        self.assertTrue(
            any("not_yet_supplied requires an empty" in error for error in self.api.validate_topology(mutant, REPO_ROOT))
        )

    def test_d4_actual_carriers_represent_d5_possible_content(self):
        by_id = {node["id"]: node for node in self.topology["nodes"]}
        for node_id in ("d4-model-token", "d4-rank-event", "d4-selector-token"):
            self.assertEqual((by_id[node_id]["dRegister"], by_id[node_id]["modality"]), ("D4", "actual"))
        for node_id in ("d5-option-a", "d5-option-b"):
            self.assertEqual((by_id[node_id]["dRegister"], by_id[node_id]["modality"]), ("D5", "possible"))
        representation_edges = {
            edge["id"] for edge in self.topology["edges"] if edge["edgeType"] in {"represents", "represented-ranking"}
        }
        self.assertEqual(
            representation_edges,
            {"e-model-option-a", "e-model-option-b", "e-rank-option-a", "e-rank-option-b"},
        )
        represented_content = next(
            edge for edge in self.topology["edges"] if edge["id"] == "e-d5-model-content"
        )
        self.assertEqual(
            (
                represented_content["from"],
                represented_content["to"],
                represented_content["modality"],
            ),
            ("d4-model-token", "d5", "possible"),
        )
        mutant = copy.deepcopy(self.topology)
        reversed_edge = next(
            edge for edge in mutant["edges"] if edge["id"] == "e-d5-model-content"
        )
        reversed_edge["from"], reversed_edge["to"] = "d5", "d4-model-token"
        self.assertTrue(
            any(
                "present D4 model token to D5 possible content" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_every_d4_and_d5_element_obeys_one_modality(self):
        for element in self.topology["nodes"] + self.topology["edges"]:
            if element["dRegister"] == "D4":
                self.assertEqual(element["modality"], "actual", element["id"])
            if element["dRegister"] == "D5":
                self.assertEqual(element["modality"], "possible", element["id"])
        mutant = copy.deepcopy(self.topology)
        next(node for node in mutant["nodes"] if node["id"] == "d4-model-token")["modality"] = "possible"
        self.assertTrue(any("every D4" in error for error in self.api.validate_topology(mutant, REPO_ROOT)))

    def test_g_is_load_bearing_on_both_sides_of_the_loop(self):
        edges = self.topology["edges"]
        self.assertTrue(
            any(edge["from"] == "d4-selector-token" and edge["to"] == "chi" for edge in edges)
        )
        self.assertTrue(
            any(
                edge["from"] == "outcome-receipt"
                and edge["to"] == "d4-selector-token"
                and edge.get("loadBearing") is True
                for edge in edges
            )
        )
        mutant = copy.deepcopy(self.topology)
        next(edge for edge in mutant["edges"] if edge["id"] == "e-outcome-selector-feedback")["loadBearing"] = False
        self.assertTrue(any("G_t must be load-bearing" in error for error in self.api.validate_topology(mutant, REPO_ROOT)))

    def test_physical_availability_is_not_authorization(self):
        by_id = {node["id"]: node for node in self.topology["nodes"]}
        self.assertEqual(by_id["physical-availability"]["status"], "available | unavailable")
        self.assertEqual(
            by_id["authorization"]["status"], "valid | invalid | absent | not_required"
        )
        self.assertIn("does not make", by_id["authorization"]["claimBoundary"])
        self.assertIn("unauthorized attempt remains an Action", by_id["chi"]["refusalPolicy"])

    def test_authorization_assessment_is_an_inhabited_tagged_union(self):
        schema = next(
            item for item in self.topology["schemas"] if item["id"] == "AuthorizationAssessment"
        )
        self.assertEqual(schema["tag"], "status")
        self.assertEqual(set(schema["variants"]), {"valid", "invalid", "absent", "not_required"})
        self.assertIn("complete non-null", schema["variants"]["valid"]["envelope"])
        self.assertEqual(schema["variants"]["invalid"]["envelope"], "Partial<AuthorizationEnvelope>")
        self.assertIn("NonEmpty", schema["variants"]["invalid"]["reasons"])
        self.assertEqual(schema["variants"]["absent"]["envelope"], "null")
        self.assertEqual(schema["variants"]["not_required"]["reasons"], "[]")
        self.assertEqual(
            schema["variants"]["not_required"]["scope"],
            "NonConsequentialScope",
        )
        receipt = next(item for item in self.topology["schemas"] if item["id"] == "CommitmentReceipt")
        self.assertIn(
            "validated authorization.status",
            receipt["fields"]["authorizationStatusDerivedFrom"],
        )
        self.assertTrue(receipt["statusDerivation"])
        self.assertIn("nonconsequential_attempt", receipt["fields"]["status"])
        self.assertIn("not_required", receipt["statusDerivation"])
        self.assertIn("nonconsequential_attempt", receipt["statusDerivation"])

    def test_authorization_union_mutations_fail_validation(self):
        for status, field, value, fragment in (
            ("valid", "envelope", "nullable", "complete non-null"),
            ("invalid", "reasons", "[]", "partial envelope plus reasons"),
            ("absent", "envelope", "non-null", "null envelope plus reasons"),
            ("not_required", "scope", "consequential", "NonConsequentialScope"),
        ):
            with self.subTest(status=status):
                mutant = copy.deepcopy(self.topology)
                schema = next(item for item in mutant["schemas"] if item["id"] == "AuthorizationAssessment")
                schema["variants"][status][field] = value
                self.assertTrue(
                    any(fragment in error for error in self.api.validate_topology(mutant, REPO_ROOT))
                )

    def test_commitment_action_outcome_and_ambient_receipts_are_typed(self):
        receipt_nodes = [node for node in self.topology["nodes"] if node["kind"] == "receipt"]
        self.assertEqual(
            {(node["id"], node["receiptType"]) for node in receipt_nodes},
            {("commitment-receipt", "commitment"), ("outcome-receipt", "outcome")},
        )
        outcome = next(node for node in receipt_nodes if node["receiptType"] == "outcome")
        self.assertEqual(outcome["receiptCause"], "action_attempt")
        outcome_schema = next(item for item in self.topology["schemas"] if item["id"] == "OutcomeReceipt")
        self.assertEqual(
            outcome_schema["fields"]["receiptCause"],
            "action_attempt | ambient_observation",
        )
        self.assertEqual(outcome_schema["fields"]["attemptedActionId"], "String?")
        self.assertEqual(outcome_schema["fields"]["performedActionId"], "String?")
        self.assertIn("ambient_observation", outcome_schema["invariant"])
        self.assertIn("never an action-attributed outcome", self.topology["receiptBoundary"]["nullActionCase"])

    def test_bearer_coverage_is_explicit_across_authorization_and_both_receipts(self):
        schemas = {item["id"]: item for item in self.topology["schemas"]}
        self.assertIn(
            "NonEmpty Unique[BearerId]",
            schemas["AuthorizationEnvelope"]["invariant"],
        )
        self.assertEqual(
            schemas["EvaluationContract"]["fields"]["bearerIds"],
            "[BearerId]",
        )
        self.assertIn(
            "NonEmpty Unique[BearerId]",
            schemas["EvaluationContract"]["invariant"],
        )

        commitment = schemas["CommitmentReceipt"]
        self.assertEqual(commitment["fields"]["expectedOutcome"], "String?")
        for fragment in (
            "keys(expectedBearerDeltas)=set(evaluation.bearerIds)",
            "authorization.envelope.consequenceBearerIds, payerIds, and beneficiaryIds is a subset of evaluation.bearerIds",
            "status in {refused,unavailable} requires attemptedActionId=null and expectedOutcome=null",
        ):
            self.assertIn(fragment, commitment["invariant"])

        outcome = schemas["OutcomeReceipt"]
        for fragment in (
            "consequenceBearerIds is NonEmpty Unique[BearerId]",
            "set(bearerObservations.bearerId)=set(consequenceBearerIds)",
            "evaluationRef=q.evaluation.id and set(consequenceBearerIds)=set(q.evaluation.bearerIds)",
        ):
            self.assertIn(fragment, outcome["invariant"])

    def test_bearer_contract_mutations_fail_validation(self):
        mutations = (
            (
                "AuthorizationEnvelope",
                "invariant",
                "consequenceBearerIds may be empty",
                "consequence bearers must be nonempty and unique",
            ),
            (
                "EvaluationContract",
                "invariant",
                "bearerIds may repeat",
                "bearerIds must be nonempty and unique",
            ),
            (
                "CommitmentReceipt",
                "invariant",
                "status in {refused,unavailable} requires attemptedActionId=null and expectedOutcome=null",
                "keys(expectedBearerDeltas)=set(evaluation.bearerIds)",
            ),
            (
                "OutcomeReceipt",
                "invariant",
                "consequenceBearerIds is NonEmpty Unique[BearerId]",
                "set(bearerObservations.bearerId)=set(consequenceBearerIds)",
            ),
        )
        for schema_id, field, replacement, expected_error in mutations:
            with self.subTest(schema=schema_id):
                mutant = copy.deepcopy(self.topology)
                schema = next(
                    item for item in mutant["schemas"] if item["id"] == schema_id
                )
                schema[field] = replacement
                self.assertTrue(
                    any(
                        expected_error in error
                        for error in self.api.validate_topology(mutant, REPO_ROOT)
                    )
                )

        mutant = copy.deepcopy(self.topology)
        next(
            item
            for item in mutant["schemas"]
            if item["id"] == "CommitmentReceipt"
        )["fields"]["expectedOutcome"] = "String"
        self.assertTrue(
            any(
                "expectedOutcome must be nullable" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_receipt_cause_mutations_fail_validation(self):
        mutant = copy.deepcopy(self.topology)
        next(item for item in mutant["schemas"] if item["id"] == "OutcomeReceipt")["fields"]["receiptCause"] = "action_attempt"
        self.assertTrue(any("discriminate action_attempt" in error for error in self.api.validate_topology(mutant, REPO_ROOT)))
        mutant = copy.deepcopy(self.topology)
        next(item for item in mutant["schemas"] if item["id"] == "OutcomeReceipt")["fields"]["attemptedActionId"] = "String"
        self.assertTrue(any("identifiers must be nullable" in error for error in self.api.validate_topology(mutant, REPO_ROOT)))

    def test_egregoreotype_is_descriptive_and_justice_is_normative(self):
        candidate = next(
            item for item in self.topology["schemas"] if item["id"] == "EgregoreotypeCandidate"
        )["fields"]
        self.assertIn("etaObserved", candidate)
        self.assertNotIn("eta", candidate)
        self.assertEqual(candidate["consciousnessPresumed"], "false")
        self.assertEqual(candidate["personhoodPresumed"], "false")
        for field in ("affectedBearerIds", "payerIds", "beneficiaryIds"):
            self.assertIn(field, candidate)
        justice = self.topology["boundaries"][0]
        self.assertIn("0", justice["fields"]["eta"])
        self.assertIn("after descriptive candidacy", justice["classificationBoundary"])
        for field in ("affectedBearerIds", "payerIds", "beneficiaryIds"):
            self.assertIn(field, justice["fields"])

    def test_quantum_overlay_is_removable_and_non_load_bearing(self):
        overlay = self.topology["quantumOverlay"]
        self.assertTrue(overlay["removable"])
        overlay_ids = set(overlay["nodeIds"]) | set(overlay["edgeIds"])
        self.assertFalse(overlay_ids & set(self.topology["operationalCore"]))
        reduced = copy.deepcopy(self.topology)
        reduced["nodes"] = [node for node in reduced["nodes"] if node["id"] not in overlay_ids]
        reduced["edges"] = [edge for edge in reduced["edges"] if edge["id"] not in overlay_ids]
        reduced["quantumOverlay"]["nodeIds"] = []
        reduced["quantumOverlay"]["edgeIds"] = []
        reduced["views"]["proof"]["showQuantumInset"] = False
        self.assertEqual(self.api.validate_topology(reduced, REPO_ROOT), [])
        svg = self.api.render_view(reduced, "proof", "0" * 64)
        self.assertNotIn("OPTIONAL QUANTUM", svg)
        self.assertIn("chi commitment selector", json.dumps(reduced))

    def test_worldview_topology_has_no_k2_primitive(self):
        self.assertNotIn("K2", json.dumps(self.topology, ensure_ascii=False))


class RenderingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = load_renderer()
        cls.topology = cls.api.load_topology(TOPOLOGY)
        cls.digest = cls.api.topology_sha256(TOPOLOGY)

    def test_rendering_is_deterministic_and_does_not_mutate_topology(self):
        original = copy.deepcopy(self.topology)
        for view_id in ("proof", "emblem"):
            first = self.api.render_view(self.topology, view_id, self.digest)
            second = self.api.render_view(self.topology, view_id, self.digest)
            self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))
        self.assertEqual(self.topology, original)

    def test_svg_is_well_formed_and_embeds_exact_topology_hash(self):
        for view_id in ("proof", "emblem"):
            rendered = self.api.render_view(self.topology, view_id, self.digest)
            root = ET.fromstring(rendered)
            self.assertEqual(root.attrib["data-topology-sha256"], self.digest)
            metadata = next(item for item in root if local_name(item.tag) == "metadata")
            self.assertIn(self.digest, metadata.text or "")

    def test_proof_and_emblem_preserve_required_boundaries(self):
        proof = self.api.render_view(self.topology, "proof", self.digest)
        emblem = self.api.render_view(self.topology, "emblem", self.digest)
        for fragment in (
            "SIX CANDIDATE CROSSINGS + ONE NON-mu CLOSURE",
            "D4 actual / enacted",
            "D5 merely possible / represented",
            "PHYSICAL",
            "AUTHORIZATION",
            "q_t COMMITMENT",
            "r_t+1 OUTCOME",
            "receipt also revises G",
            "etaObserved = n | ?",
            "affected bearer set",
            "payerIds / beneficiaryIds",
            "ambient OutcomeReceipt (distinct cause)",
        ):
            self.assertIn(fragment, proof)
        self.assertIn("evidence: empty", proof)
        self.assertIn("revises M + G", emblem)
        self.assertIn("etaObserved = n | ?", emblem)
        self.assertNotIn("OPTIONAL QUANTUM", emblem)

    def test_no_scripts_animation_external_assets_or_external_fonts(self):
        forbidden_tags = {"script", "animate", "animateMotion", "animateTransform", "set"}
        for view_id in ("proof", "emblem"):
            rendered = self.api.render_view(self.topology, view_id, self.digest)
            root = ET.fromstring(rendered)
            self.assertFalse({local_name(item.tag) for item in root.iter()} & forbidden_tags)
            self.assertNotIn("@font-face", rendered)
            self.assertNotIn("<image", rendered)
            self.assertNotIn("href=", rendered)
            self.assertNotIn("timestamp", rendered.lower())
            self.assertNotIn("generated-at", rendered.lower())
            self.assertNotIn("font-family=\"http", rendered)

    def test_svg_ids_are_unique_within_each_document(self):
        for view_id in ("proof", "emblem"):
            root = ET.fromstring(self.api.render_view(self.topology, view_id, self.digest))
            ids = [item.attrib["id"] for item in root.iter() if "id" in item.attrib]
            self.assertEqual(len(ids), len(set(ids)), view_id)

    def test_every_rendered_topology_edge_uses_only_its_declared_modality_dash(self):
        topology_edges = {edge["id"]: edge for edge in self.topology["edges"]}
        for view_id in ("proof", "emblem"):
            root = ET.fromstring(
                self.api.render_view(self.topology, view_id, self.digest)
            )
            rendered_by_id = {
                item.attrib["id"]: item
                for item in root.iter()
                if "id" in item.attrib
            }
            rendered_edge_ids = sorted(set(rendered_by_id) & set(topology_edges))
            self.assertTrue(rendered_edge_ids, view_id)
            for edge_id in rendered_edge_ids:
                with self.subTest(view=view_id, edge=edge_id):
                    declared_possible = (
                        topology_edges[edge_id]["modality"] == "possible"
                    )
                    rendered_dashed = bool(
                        rendered_by_id[edge_id].attrib.get("stroke-dasharray")
                    )
                    self.assertEqual(rendered_dashed, declared_possible)

    def test_generated_files_are_current_and_repeat_generation_is_byte_stable(self):
        self.assertEqual(self.api.check_outputs(TOPOLOGY, REPO_ROOT), [])
        before = {name: path.read_bytes() for name, path in OUTPUTS.items()}
        written = self.api.write_outputs(TOPOLOGY, REPO_ROOT)
        self.assertEqual(set(written), set(OUTPUTS.values()))
        after = {name: path.read_bytes() for name, path in OUTPUTS.items()}
        self.assertEqual(before, after)
        for name, data in after.items():
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                hashlib.sha256(OUTPUTS[name].read_bytes()).hexdigest(),
            )

    def test_check_cli_passes_and_is_quietly_bounded(self):
        process = subprocess.run(
            [sys.executable, str(COMPILER), "--check"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(
            process.stdout.strip(),
            "BURRI-OK topology valid; generated SVG bytes are current",
        )


if __name__ == "__main__":
    unittest.main()
