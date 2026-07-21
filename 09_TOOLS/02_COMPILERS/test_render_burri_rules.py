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
RULEBOOK = REPO_ROOT / "05_COSMOLOGY" / "00_THE_BURRI_RULES.md"
MU_OWNER = REPO_ROOT / "05_COSMOLOGY" / "03_FORMAL_SYSTEM" / "10_EFR_MU_LIMIT_FORMULA.md"
TYPE_OWNER = REPO_ROOT / "05_COSMOLOGY" / "03_FORMAL_SYSTEM" / "29_PRIMITIVES_AND_TYPE_SIGNATURES.md"
OUTPUTS = {
    "proof": REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_PLATE.svg",
    "emblem": REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_EMBLEM.svg",
}
RULE_IDS = {f"BR-{number}" for number in range(1, 7)}
REGISTERS = {f"D{number}" for number in range(7)}
KINDS = {"state", "frame", "crossing", "commitment", "receipt", "trace"}
MODALITIES = {"structural", "actual", "possible"}
ROLES = {"forward", "feedback", "coupling"}
TIERS = {"A", "B", "S", "I", "D", "C"}
SHARED_GRAPH_FIELDS = {
    "id",
    "dRegister",
    "modality",
    "role",
    "tier",
    "ruleIds",
    "sourceIds",
}
TOP_LEVEL_KEYS = {"schemaVersion", "rules", "sources", "nodes", "edges", "views"}
FORBIDDEN_TOP_LEVEL_KEYS = {
    "title",
    "authorityBoundary",
    "schemas",
    "formulas",
    "invariants",
    "modelCoupling",
    "receiptBoundary",
    "boundaries",
    "cones",
    "reflexiveBridge",
    "rosettaProjection",
    "quantumOverlay",
    "operationalCore",
}


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

    def test_public_api_and_exact_metadata_sections(self):
        for name in (
            "load_topology",
            "validate_topology",
            "validate_owner_contracts",
            "assess_authorization",
            "assess_outcome_coverage",
            "topology_sha256",
            "render_view",
            "write_outputs",
            "check_outputs",
            "main",
        ):
            self.assertTrue(callable(getattr(self.api, name, None)), name)
        self.assertEqual(set(self.topology), TOP_LEVEL_KEYS)
        self.assertEqual(self.topology["schemaVersion"], "0.4")
        self.assertEqual(self.api.validate_owner_contracts(REPO_ROOT), [])
        self.assertEqual(self.api.validate_topology(self.topology, REPO_ROOT), [])

    def test_forbidden_semantic_sections_fail_closed(self):
        self.assertFalse(FORBIDDEN_TOP_LEVEL_KEYS & set(self.topology))
        for key in sorted(FORBIDDEN_TOP_LEVEL_KEYS):
            with self.subTest(key=key):
                mutant = copy.deepcopy(self.topology)
                mutant[key] = "attempted doctrine"
                self.assertTrue(
                    any(
                        "unexpected top-level keys" in error and key in error
                        for error in self.api.validate_topology(mutant, REPO_ROOT)
                    )
                )

    def test_rules_and_sources_are_references_not_doctrine(self):
        self.assertEqual({rule["id"] for rule in self.topology["rules"]}, RULE_IDS)
        source_ids = {source["id"] for source in self.topology["sources"]}
        for rule in self.topology["rules"]:
            self.assertEqual(set(rule), {"id", "sourceIds"})
            self.assertTrue(rule["sourceIds"])
            self.assertTrue(set(rule["sourceIds"]) <= source_ids)
        for source in self.topology["sources"]:
            self.assertIn(set(source), ({"id", "path"}, {"id", "url"}))
            self.assertNotIn("summary", source)
            self.assertNotIn("authority", source)
            self.assertNotIn("label", source)

        mutant = copy.deepcopy(self.topology)
        mutant["rules"][0]["summary"] = "new doctrine"
        self.assertTrue(
            any(
                "only id and sourceIds" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_graph_elements_contain_only_typed_geometry_and_owner_references(self):
        for node in self.topology["nodes"]:
            self.assertTrue(SHARED_GRAPH_FIELDS <= node.keys())
            self.assertTrue(set(node) <= self.api.NODE_METADATA_FIELDS)
            self.assertIn(node["kind"], KINDS)
            self.assertNotIn("edgeType", node)
            self.assertIn(node["dRegister"], REGISTERS)
            self.assertIn(node["modality"], MODALITIES)
            self.assertIn(node["role"], ROLES)
            self.assertIn(node["tier"], TIERS)
        for edge in self.topology["edges"]:
            self.assertTrue(SHARED_GRAPH_FIELDS <= edge.keys())
            self.assertTrue(set(edge) <= self.api.EDGE_METADATA_FIELDS)
            self.assertIsInstance(edge["edgeType"], str)
            self.assertTrue(edge["edgeType"].strip())
            self.assertNotIn("kind", edge)
            self.assertIn(edge["dRegister"], REGISTERS)
            self.assertIn(edge["modality"], MODALITIES)
            self.assertIn(edge["role"], ROLES)
            self.assertIn(edge["tier"], TIERS)

        mutant = copy.deepcopy(self.topology)
        mutant["nodes"][0]["claimBoundary"] = "smuggled prose"
        self.assertTrue(
            any(
                "carries non-metadata fields: claimBoundary" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )
        mutant = copy.deepcopy(self.topology)
        mutant["edges"][0]["formula"] = "x=y"
        self.assertTrue(
            any(
                "carries non-metadata fields: formula" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_node_kind_and_edge_type_discriminators_fail_closed(self):
        mutations = (
            ("node", "kind", None, "invalid kind"),
            ("node", "edgeType", "feedback", "must use kind, not edgeType"),
            ("edge", "edgeType", None, "needs a non-empty edgeType"),
            ("edge", "kind", "state", "must use edgeType, not kind"),
            ("edge", "tier", None, "missing shared metadata: tier"),
        )
        for element_type, field, value, fragment in mutations:
            with self.subTest(element_type=element_type, field=field):
                mutant = copy.deepcopy(self.topology)
                element = mutant["nodes" if element_type == "node" else "edges"][0]
                if value is None:
                    element.pop(field)
                else:
                    element[field] = value
                self.assertTrue(
                    any(
                        fragment in error
                        for error in self.api.validate_topology(mutant, REPO_ROOT)
                    )
                )

    def test_ids_endpoints_sources_and_frozen_tree_fence(self):
        elements = self.topology["nodes"] + self.topology["edges"]
        ids = [item["id"] for item in elements]
        self.assertEqual(len(ids), len(set(ids)))
        node_ids = {node["id"] for node in self.topology["nodes"]}
        self.assertTrue(
            all(
                edge["from"] in node_ids and edge["to"] in node_ids
                for edge in self.topology["edges"]
            )
        )
        for source in self.topology["sources"]:
            if "path" not in source:
                self.assertTrue(source["url"].startswith("https://"))
                continue
            path = Path(source["path"])
            self.assertFalse(path.is_absolute())
            self.assertFalse(
                {"12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"}
                & set(path.parts)
            )
            self.assertTrue((REPO_ROOT / path).is_file(), source["path"])

        mutant = copy.deepcopy(self.topology)
        mutant["nodes"].append(copy.deepcopy(mutant["nodes"][0]))
        self.assertTrue(
            any(
                "globally unique" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )
        mutant = copy.deepcopy(self.topology)
        mutant["sources"][0]["path"] = "90_ARCHIVE/forbidden.md"
        self.assertTrue(
            any(
                "frozen tree" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_exact_register_spine_crossings_and_non_mu_edges(self):
        nodes = self.topology["nodes"]
        self.assertTrue(
            {f"d{number}" for number in range(7)} <= {node["id"] for node in nodes}
        )
        crossings = {node["id"] for node in nodes if node["kind"] == "crossing"}
        self.assertEqual(crossings, {f"mu-{number}" for number in range(5)})
        serialized = json.dumps(self.topology, ensure_ascii=False).lower()
        self.assertNotIn('"id": "mu-5"', serialized)
        self.assertNotIn('"id": "mu-6"', serialized)
        for number in range(5):
            crossing = next(node for node in nodes if node["id"] == f"mu-{number}")
            self.assertEqual(crossing["dRegister"], f"D{number + 1}")
            for semantic_field in (
                "triggerType",
                "saturatedRegister",
                "saturationEvidence",
                "evidenceStatus",
                "prediction",
                "killCriterion",
            ):
                self.assertNotIn(semantic_field, crossing)
            self.assertTrue(
                any(
                    edge["from"] == f"d{number}"
                    and edge["to"] == f"mu-{number}"
                    and edge["edgeType"] == "crossing-ingress"
                    for edge in self.topology["edges"]
                )
            )
            self.assertTrue(
                any(
                    edge["from"] == f"mu-{number}"
                    and edge["to"] == f"d{number + 1}"
                    and edge["edgeType"] == "crossing-egress"
                    for edge in self.topology["edges"]
                )
            )
        boundary = [
            edge for edge in self.topology["edges"] if edge["edgeType"] == "boundary"
        ]
        closure = [
            edge for edge in self.topology["edges"] if edge["edgeType"] == "closure"
        ]
        self.assertEqual(
            [(edge["id"], edge["from"], edge["to"]) for edge in boundary],
            [("b6", "d5", "d6")],
        )
        self.assertEqual(
            [(edge["id"], edge["from"], edge["to"]) for edge in closure],
            [("r6", "d6", "d0")],
        )
        self.assertNotIn("boundary", boundary[0])
        self.assertNotIn("closure", closure[0])

    def test_mu_and_receipt_semantics_live_in_owner_contracts(self):
        mu_owner = MU_OWNER.read_text(encoding="utf-8")
        type_owner = TYPE_OWNER.read_text(encoding="utf-8")
        self.assertIn("`μ₀` is an origin aperture", mu_owner)
        self.assertIn("`μ₁…μ₄` are saturation", mu_owner)
        self.assertIn("saturationEvidence=[]", mu_owner)
        self.assertIn("currently_unreduced", mu_owner)
        self.assertIn("There are exactly five positive-freedom crossing identifiers", type_owner)
        self.assertIn("AuthorizationValid(e,a,t,B) :=", type_owner)
        self.assertIn("CommitmentReceipt := {", type_owner)
        self.assertIn("OutcomeReceipt := {", type_owner)
        self.assertIn("EgregoreotypeCandidate := {", type_owner)
        self.assertEqual(self.api.validate_owner_contracts(REPO_ROOT), [])

    def test_d4_actual_carriers_represent_d5_possible_content(self):
        by_id = {node["id"]: node for node in self.topology["nodes"]}
        for node_id in ("d4-model-token", "d4-rank-event", "d4-selector-token"):
            self.assertEqual(
                (by_id[node_id]["dRegister"], by_id[node_id]["modality"]),
                ("D4", "actual"),
            )
        for node_id in ("d5-option-a", "d5-option-b"):
            self.assertEqual(
                (by_id[node_id]["dRegister"], by_id[node_id]["modality"]),
                ("D5", "possible"),
            )
        represented = next(
            edge
            for edge in self.topology["edges"]
            if edge["id"] == "e-d5-model-content"
        )
        self.assertEqual(
            (represented["from"], represented["to"], represented["modality"]),
            ("d4-model-token", "d5", "possible"),
        )
        mutant = copy.deepcopy(self.topology)
        edge = next(
            item for item in mutant["edges"] if item["id"] == "e-d5-model-content"
        )
        edge["from"], edge["to"] = "d5", "d4-model-token"
        self.assertTrue(
            any(
                "present D4 model token to D5 possible content" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_structural_spine_and_d4_d5_tokens_obey_distinct_modalities(self):
        structural_nodes = {
            "titan-frame",
            "d0",
            "d1",
            "d2",
            "d3",
            "d6",
            *(f"mu-{number}" for number in range(5)),
        }
        by_id = {node["id"]: node for node in self.topology["nodes"]}
        for node_id in structural_nodes:
            self.assertEqual(by_id[node_id]["modality"], "structural", node_id)
        for element in self.topology["nodes"] + self.topology["edges"]:
            if element["dRegister"] == "D4" and element["id"] not in {
                "mu-3",
                "e-mu3-d4",
                "e-d4-mu4",
            }:
                self.assertEqual(element["modality"], "actual", element["id"])
            if element["dRegister"] == "D5" and element["id"] not in {
                "mu-4",
                "e-mu4-d5",
            }:
                self.assertEqual(element["modality"], "possible", element["id"])
        mutant = copy.deepcopy(self.topology)
        next(
            node for node in mutant["nodes"] if node["id"] == "d4-model-token"
        )["modality"] = "possible"
        self.assertTrue(
            any(
                "every non-crossing D4" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_both_receipts_feed_model_and_selector(self):
        edges = self.topology["edges"]
        for receipt_id in ("commitment-receipt", "outcome-receipt"):
            targets = {
                edge["to"]
                for edge in edges
                if edge["from"] == receipt_id
                and edge["edgeType"] == "feedback"
                and edge["role"] == "feedback"
            }
            self.assertEqual(targets, {"d4-model-token", "d4-selector-token"})

        mutant = copy.deepcopy(self.topology)
        mutant["edges"] = [
            edge
            for edge in mutant["edges"]
            if edge["id"] != "e-commitment-model-feedback"
        ]
        self.assertTrue(
            any(
                "q_t commitment receipt must feed both" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_physical_availability_and_authorization_are_distinct_inputs(self):
        edges = {edge["id"]: edge for edge in self.topology["edges"]}
        self.assertEqual(
            (
                edges["e-availability-chi"]["from"],
                edges["e-availability-chi"]["to"],
                edges["e-availability-chi"]["edgeType"],
            ),
            ("physical-availability", "chi", "physical-availability"),
        )
        self.assertEqual(
            (
                edges["e-authorization-chi"]["from"],
                edges["e-authorization-chi"]["to"],
                edges["e-authorization-chi"]["edgeType"],
            ),
            ("authorization", "chi", "authorization-assessment"),
        )

    def test_authorization_predicates_are_executable_not_json_schemas(self):
        envelope = {
            field: "present" for field in self.api.AUTHORIZATION_ENVELOPE_FIELDS
        }
        predicates = {
            predicate: True for predicate in self.api.AUTHORIZATION_PREDICATES
        }
        self.assertEqual(self.api.assess_authorization(envelope, predicates), "valid")
        self.assertEqual(self.api.assess_authorization(None, {}), "absent")
        self.assertEqual(
            self.api.assess_authorization(None, {}, nonconsequential_scope=True),
            "not_required",
        )
        expired = dict(predicates)
        expired["expiryOrRevocation"] = False
        self.assertEqual(self.api.assess_authorization(envelope, expired), "invalid")
        out_of_scope = dict(predicates)
        out_of_scope["mandateScope"] = False
        self.assertEqual(
            self.api.assess_authorization(envelope, out_of_scope), "invalid"
        )
        missing_predicate = dict(predicates)
        missing_predicate.pop("bearerCoverage")
        self.assertEqual(
            self.api.assess_authorization(envelope, missing_predicate), "invalid"
        )

    def test_commitment_and_outcome_receipts_are_two_typed_nodes(self):
        receipts = [
            node for node in self.topology["nodes"] if node["kind"] == "receipt"
        ]
        self.assertEqual(
            {(node["id"], node["receiptType"]) for node in receipts},
            {
                ("commitment-receipt", "commitment"),
                ("outcome-receipt", "outcome"),
            },
        )
        commitment = next(node for node in receipts if node["receiptType"] == "commitment")
        outcome = next(node for node in receipts if node["receiptType"] == "outcome")
        self.assertNotIn("receiptCause", commitment)
        self.assertNotIn("receiptCause", outcome)
        owner = TYPE_OWNER.read_text(encoding="utf-8")
        self.assertIn("receiptCause: action_attempt | ambient_observation", owner)
        self.assertIn("it is never an action outcome", owner)

    def test_outcome_coverage_executes_unexpected_bearer_and_multi_measure_cases(self):
        drift = self.api.assess_outcome_coverage(
            ["individual", "whole"],
            ["individual", "whole", "unexpected-third"],
            [
                {"observationId": "o1", "bearerId": "individual", "measureId": "m"},
                {"observationId": "o2", "bearerId": "whole", "measureId": "m"},
                {
                    "observationId": "o3",
                    "bearerId": "unexpected-third",
                    "measureId": "harm",
                },
            ],
        )
        self.assertTrue(drift["validEvidence"])
        self.assertEqual(drift["coverageDriftBearerIds"], ["unexpected-third"])
        self.assertFalse(drift["retrospectiveJusticeValid"])
        self.assertFalse(drift["retrospectiveAuthorizationValid"])

        multi = self.api.assess_outcome_coverage(
            ["individual"],
            ["individual"],
            [
                {"observationId": "o1", "bearerId": "individual", "measureId": "health"},
                {"observationId": "o2", "bearerId": "individual", "measureId": "wealth"},
            ],
        )
        self.assertTrue(multi["validEvidence"], multi["errors"])
        self.assertTrue(multi["retrospectiveJusticeValid"])

    def test_collective_fields_are_owner_references_not_embedded_doctrine(self):
        trace = next(node for node in self.topology["nodes"] if node["id"] == "shared-trace")
        self.assertEqual(
            set(trace["collectiveOwnerRefs"]), self.api.COLLECTIVE_OWNER_REFS
        )
        self.assertEqual(
            len(trace["collectiveOwnerRefs"]), len(self.api.COLLECTIVE_OWNER_REFS)
        )
        for ref in trace["collectiveOwnerRefs"]:
            self.assertTrue(ref.startswith("src-types#"), ref)
        for key in (
            "criteria",
            "etaObserved",
            "claimBoundary",
            "consciousnessPresumed",
            "personhoodPresumed",
        ):
            self.assertNotIn(key, trace)

        mutant = copy.deepcopy(self.topology)
        next(node for node in mutant["nodes"] if node["id"] == "shared-trace")[
            "collectiveOwnerRefs"
        ].pop()
        self.assertTrue(
            any(
                "every owner-defined collective and Justice field" in error
                for error in self.api.validate_topology(mutant, REPO_ROOT)
            )
        )

    def test_d3_quantum_state_is_core_while_interpretation_overlay_is_absent(self):
        overlay_ids = {
            element["id"]
            for element in self.topology["nodes"] + self.topology["edges"]
            if element.get("overlay") == "quantum"
        }
        self.assertEqual(overlay_ids, set())
        d3 = next(node for node in self.topology["nodes"] if node["id"] == "d3")
        self.assertEqual((d3["dRegister"], d3["modality"]), ("D3", "structural"))
        self.assertIn("src-d3-state", d3["sourceIds"])
        self.assertIn("src-quantum", d3["sourceIds"])
        self.assertFalse(self.topology["views"]["proof"]["showQuantumInset"])
        self.assertEqual(self.api.validate_topology(self.topology, REPO_ROOT), [])
        svg = self.api.render_view(self.topology, "proof", "0" * 64)
        self.assertNotIn("OPTIONAL QUANTUM", svg)
        self.assertIn("q-state", svg)
        self.assertIn('id="chi"', svg)

    def test_worldview_topology_has_no_private_signature_primitive(self):
        serialized = json.dumps(self.topology, ensure_ascii=False).lower()
        self.assertNotIn("private signer", serialized)
        self.assertNotIn("private signature", serialized)


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
            "FIVE TYPED mu INTERFACES + NON-mu EXIT / RETURN",
            "D4 actual / enacted",
            "D5 merely possible / represented",
            "PHYSICAL",
            "AUTHORIZATION",
            "q_t COMMITMENT",
            "r_t+1 OUTCOME",
            "receipt also revises G",
            "informative q_t can revise M or G while r_t+1 = null",
            "non-informative q_t + null r_t+1 = justified null update",
            "etaObserved = n | ?",
            "affected bearer set",
            "payerIds / beneficiaryIds",
            "ambient OutcomeReceipt (distinct cause)",
        ):
            self.assertIn(fragment, proof)
        self.assertIn("evidence: empty", proof)
        self.assertIn("revises M + G", emblem)
        self.assertIn("informative even when r_t+1 = null", emblem)
        self.assertIn("no new q + null r = justified null update", emblem)
        self.assertIn("etaObserved = n | ?", emblem)
        self.assertNotIn("OPTIONAL QUANTUM", emblem)

        feedback_ids = {
            "e-commitment-model-feedback",
            "e-commitment-selector-feedback",
            "e-outcome-model-feedback",
            "e-outcome-selector-feedback",
        }
        for view_id, rendered in (("proof", proof), ("emblem", emblem)):
            root = ET.fromstring(rendered)
            rendered_ids = {
                item.attrib["id"] for item in root.iter() if "id" in item.attrib
            }
            self.assertTrue(feedback_ids <= rendered_ids, view_id)

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
