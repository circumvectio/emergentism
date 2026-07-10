"""Contract tests for the deterministic Burri Rules topology renderer."""

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
EXPECTED_OUTPUTS = [
    REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_PLATE.svg",
    REPO_ROOT / "05_COSMOLOGY" / "00_BURRI_RULES_EMBLEM.svg",
]
RULE_IDS = {f"BR-{number}" for number in range(1, 7)}
ALLOWED_KINDS = {"state", "frame", "crossing", "commitment", "receipt", "trace"}
ALLOWED_REGISTERS = {f"D{number}" for number in range(7)}
ALLOWED_MODALITIES = {"actual", "possible"}
ALLOWED_ROLES = {"forward", "feedback", "coupling"}
ALLOWED_TIERS = {"A", "B", "S", "I", "D", "C"}
FORBIDDEN_SOURCE_PARTS = {"12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"}
TRACE_CRITERIA = {
    "carrier-turnover-persistence",
    "later-selection-reweighting",
    "objective-like-bias",
    "continuing-substrate-input-cost",
}


def load_renderer():
    """Load the wished-for public module without changing sys.path."""
    if not COMPILER.exists():
        raise AssertionError(f"missing renderer implementation: {COMPILER}")
    spec = importlib.util.spec_from_file_location("render_burri_rules", COMPILER)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load renderer implementation: {COMPILER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class BurriRulesRendererTests(unittest.TestCase):
    def api_and_topology(self):
        api = load_renderer()
        self.assertTrue(TOPOLOGY.exists(), f"missing topology input: {TOPOLOGY}")
        return api, api.load_topology(TOPOLOGY)

    def test_public_api_and_schema_contract(self):
        api, topology = self.api_and_topology()
        for name in (
            "load_topology",
            "validate_topology",
            "topology_sha256",
            "render_view",
            "write_outputs",
            "check_outputs",
            "main",
        ):
            self.assertTrue(callable(getattr(api, name, None)), name)
        self.assertTrue(
            {"schemaVersion", "rules", "sources", "nodes", "edges", "views"}
            <= topology.keys()
        )
        self.assertEqual(topology["schemaVersion"], "0.1")
        self.assertEqual({rule["id"] for rule in topology["rules"]}, RULE_IDS)
        self.assertEqual(len(topology["rules"]), 6)

    def test_elements_have_unique_ids_valid_endpoints_and_enums(self):
        api, topology = self.api_and_topology()
        nodes = topology["nodes"]
        edges = topology["edges"]
        element_ids = [element["id"] for element in nodes + edges]
        self.assertEqual(len(element_ids), len(set(element_ids)))
        node_ids = {node["id"] for node in nodes}
        source_ids = {source["id"] for source in topology["sources"]}
        for node in nodes:
            self.assertIn(node["kind"], ALLOWED_KINDS)
            self.assertIn(node["dRegister"], ALLOWED_REGISTERS)
            self.assertIn(node["modality"], ALLOWED_MODALITIES)
            self.assertIn(node["role"], ALLOWED_ROLES)
            self.assertIn(node["tier"], ALLOWED_TIERS)
            self.assertIsInstance(node["label"], str)
            self.assertTrue(node["label"].strip())
            self.assertTrue(set(node["ruleIds"]) <= RULE_IDS)
            self.assertTrue(node["ruleIds"])
            self.assertTrue(set(node["sourceIds"]) <= source_ids)
            self.assertTrue(node["sourceIds"])
            self.assertIsInstance(node["x"], (int, float))
            self.assertIsInstance(node["y"], (int, float))
        for edge in edges:
            self.assertIn(edge["from"], node_ids)
            self.assertIn(edge["to"], node_ids)
            self.assertIn(edge["dRegister"], ALLOWED_REGISTERS)
            self.assertIn(edge["modality"], ALLOWED_MODALITIES)
            self.assertIn(edge["role"], ALLOWED_ROLES)
            self.assertIn(edge["tier"], ALLOWED_TIERS)
            self.assertTrue(set(edge["ruleIds"]) <= RULE_IDS)
            self.assertTrue(edge["ruleIds"])
            self.assertTrue(set(edge["sourceIds"]) <= source_ids)
            self.assertTrue(edge["sourceIds"])
        self.assertEqual(api.validate_topology(topology, REPO_ROOT), [])

        duplicate = copy.deepcopy(topology)
        duplicate["nodes"].append(copy.deepcopy(duplicate["nodes"][0]))
        self.assertTrue(
            any("duplicate element id" in error for error in api.validate_topology(duplicate, REPO_ROOT))
        )

    def test_local_sources_exist_and_stay_in_allowed_live_trees(self):
        api, topology = self.api_and_topology()
        soros = []
        for source in topology["sources"]:
            if "path" in source:
                path = Path(source["path"])
                self.assertFalse(path.is_absolute())
                self.assertFalse(FORBIDDEN_SOURCE_PARTS & set(path.parts))
                self.assertTrue((REPO_ROOT / path).is_file(), source["path"])
            elif "url" in source:
                self.assertTrue(source["url"].startswith("https://"))
                soros.append(source)
        self.assertEqual(len(soros), 1)
        self.assertEqual(soros[0]["tier"], "B")
        self.assertEqual(api.validate_topology(topology, REPO_ROOT), [])

        blocked = copy.deepcopy(topology)
        blocked["sources"][0]["path"] = "90_ARCHIVE/forbidden.md"
        self.assertTrue(
            any("disallowed source path" in error for error in api.validate_topology(blocked, REPO_ROOT))
        )

    def test_dimensional_spine_has_six_crossings_and_one_closure(self):
        _, topology = self.api_and_topology()
        node_ids = {node["id"] for node in topology["nodes"]}
        self.assertTrue({f"d{number}" for number in range(7)} <= node_ids)
        self.assertTrue({f"mu-{number}" for number in range(6)} <= node_ids)
        self.assertNotIn("mu-6", node_ids)
        crossing_ids = {
            node["id"] for node in topology["nodes"] if node["kind"] == "crossing"
        }
        self.assertEqual(crossing_ids, {f"mu-{number}" for number in range(6)})
        closures = [edge for edge in topology["edges"] if edge.get("closure") is True]
        self.assertEqual(len(closures), 1)
        self.assertEqual((closures[0]["from"], closures[0]["to"]), ("d6", "d0"))

    def test_master_topology_semantics_are_explicit(self):
        _, topology = self.api_and_topology()
        frames = [node for node in topology["nodes"] if node["kind"] == "frame"]
        self.assertEqual(len(frames), 1)
        self.assertEqual(set(frames[0]["marks"]), {"bullet", "finity", "horizon"})
        self.assertFalse(frames[0]["acting"])
        self.assertTrue(frames[0]["displayLociOnly"])

        by_id = {node["id"]: node for node in topology["nodes"]}
        self.assertEqual(by_id["chi"]["kind"], "commitment")
        self.assertEqual(by_id["chi"]["dRegister"], "D4")
        self.assertEqual(by_id["d5-model"]["modality"], "possible")
        self.assertEqual(by_id["d5-option-a"]["modality"], "possible")
        self.assertEqual(by_id["d4-action"]["modality"], "actual")
        self.assertEqual(by_id["receipt"]["modality"], "actual")

        self.assertEqual(topology["cones"]["physical"]["id"], "physical-cone")
        self.assertEqual(topology["cones"]["physical"]["label"], "J+")
        self.assertIn("c-bounded", topology["cones"]["physical"]["boundary"])
        self.assertEqual(topology["cones"]["option"]["id"], "option-cone")
        self.assertEqual(topology["cones"]["option"]["label"], "Omega")
        self.assertIn("inside", topology["cones"]["option"]["boundary"])
        self.assertEqual(topology["rosettaProjection"]["label"], "rho_domain")
        self.assertIn("no proof transfer", topology["rosettaProjection"]["boundary"])
        self.assertEqual(
            topology["fullTextEquivalent"],
            "The Titans frame possibility; a finite agent forms a fallible D5 option field, "
            "commits through D4 means and authorization, receives D4 consequences, and "
            "recursively corrects both world-model and selector.",
        )

    def test_collective_boundary_and_trace_contract(self):
        _, topology = self.api_and_topology()
        self.assertEqual(len(topology["boundaries"]), 1)
        boundary = topology["boundaries"][0]
        self.assertTrue(
            {"individual", "whole", "eta", "custody", "consent", "reversibility", "exit"}
            <= boundary["fields"].keys()
        )
        trace = next(node for node in topology["nodes"] if node["kind"] == "trace")
        self.assertEqual(set(trace["criteria"]), TRACE_CRITERIA)
        self.assertIn("no consciousness claim", trace["claimBoundary"].lower())

    def test_reflexive_bridge_names_three_slippages_and_feedback_signs(self):
        _, topology = self.api_and_topology()
        bridge = topology["reflexiveBridge"]
        self.assertEqual(
            {slippage["id"] for slippage in bridge["slippages"]},
            {"cognitive-gap", "execution-gap", "outcome-gap"},
        )
        signs = {item["id"]: item["label"] for item in bridge["feedbackSigns"]}
        self.assertIn("corrective", signs["negative"].lower())
        self.assertIn("amplifying", signs["positive"].lower())
        self.assertIn("not moral", bridge["signBoundary"].lower())
        soros = next(source for source in topology["sources"] if "url" in source)
        self.assertEqual(soros["crosswalkTier"], "I")

    def test_receipt_feedback_requires_update_or_explicit_null_reason(self):
        _, topology = self.api_and_topology()
        receipts = [node for node in topology["nodes"] if node["kind"] == "receipt"]
        self.assertEqual(len(receipts), 1)
        feedback = [
            edge
            for edge in topology["edges"]
            if edge["role"] == "feedback" and edge["from"] == receipts[0]["id"]
        ]
        self.assertEqual(len(feedback), 1)
        self.assertEqual(feedback[0]["updatePolicy"], "changed or explicit null-with-reason")

    def test_quantum_overlay_is_removable_without_breaking_core(self):
        api, topology = self.api_and_topology()
        stripped = copy.deepcopy(topology)
        quantum_nodes = {
            node["id"] for node in stripped["nodes"] if node.get("overlay") == "quantum"
        }
        self.assertTrue(quantum_nodes)
        stripped["nodes"] = [
            node for node in stripped["nodes"] if node.get("overlay") != "quantum"
        ]
        stripped["edges"] = [
            edge
            for edge in stripped["edges"]
            if edge.get("overlay") != "quantum"
            and edge["from"] not in quantum_nodes
            and edge["to"] not in quantum_nodes
        ]
        self.assertEqual(api.validate_topology(stripped, REPO_ROOT), [])
        referenced_rules = {
            rule_id for element in stripped["nodes"] + stripped["edges"] for rule_id in element["ruleIds"]
        }
        self.assertEqual(referenced_rules, RULE_IDS)

        core = set(stripped["operationalCore"])
        adjacency = {node_id: set() for node_id in core}
        for edge in stripped["edges"]:
            if edge["from"] in core and edge["to"] in core:
                adjacency[edge["from"]].add(edge["to"])
                adjacency[edge["to"]].add(edge["from"])
        seen = set()
        frontier = [next(iter(core))]
        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            seen.add(current)
            frontier.extend(adjacency[current] - seen)
        self.assertEqual(seen, core)
        ET.fromstring(api.render_view(stripped, "proof", "0" * 64))

    def test_views_render_safe_valid_xml_with_shared_hash(self):
        api, topology = self.api_and_topology()
        topology_hash = api.topology_sha256(TOPOLOGY)
        self.assertEqual(topology_hash, hashlib.sha256(TOPOLOGY.read_bytes()).hexdigest())
        self.assertEqual(set(topology["views"]), {"proof", "emblem"})
        for view_id in ("proof", "emblem"):
            self.assertEqual(topology["views"][view_id]["width"], 1600)
            self.assertEqual(topology["views"][view_id]["height"], 1000)
            svg = api.render_view(topology, view_id, topology_hash)
            root = ET.fromstring(svg)
            self.assertEqual(local_name(root.tag), "svg")
            self.assertEqual(root.attrib.get("role"), "img")
            self.assertEqual(root.attrib.get("width"), "1600")
            self.assertEqual(root.attrib.get("height"), "1000")
            self.assertEqual(root.attrib.get("viewBox"), "0 0 1600 1000")
            child_names = [local_name(child.tag) for child in root]
            self.assertIn("title", child_names)
            self.assertIn("desc", child_names)
            self.assertIn("metadata", child_names)
            self.assertIn(topology_hash, svg)
            self.assertIn("rendererVersion=", svg)
            rendered_ids = {
                element.attrib["id"] for element in root.iter() if "id" in element.attrib
            }
            self.assertTrue(set(topology["operationalCore"]) <= rendered_ids)
            lowered = svg.lower()
            for forbidden in (
                "<script",
                "<style",
                "<animate",
                "<set",
                "javascript:",
                "data:",
                "@import",
                "<image",
                "<foreignobject",
            ):
                self.assertNotIn(forbidden, lowered)
            self.assertNotIn("http://", lowered)
            self.assertNotIn("https://", lowered)

    def test_repeated_rendering_is_byte_identical(self):
        api, topology = self.api_and_topology()
        topology_hash = api.topology_sha256(TOPOLOGY)
        for view_id in ("proof", "emblem"):
            first = api.render_view(topology, view_id, topology_hash)
            second = api.render_view(copy.deepcopy(topology), view_id, topology_hash)
            self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

    def test_write_paths_and_cli_check_drift_behavior(self):
        api, _ = self.api_and_topology()
        written = api.write_outputs(TOPOLOGY, REPO_ROOT)
        self.assertEqual(written, EXPECTED_OUTPUTS)
        command = [sys.executable, "-B", str(COMPILER)]
        checked = subprocess.run(
            command + ["--check"], cwd=REPO_ROOT, text=True, capture_output=True
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

        original = EXPECTED_OUTPUTS[0].read_bytes()
        try:
            EXPECTED_OUTPUTS[0].write_bytes(original + b"\n<!-- deliberate drift -->\n")
            drifted = subprocess.run(
                command + ["--check"], cwd=REPO_ROOT, text=True, capture_output=True
            )
            self.assertNotEqual(drifted.returncode, 0)
            self.assertIn(
                "05_COSMOLOGY/00_BURRI_RULES_PLATE.svg",
                drifted.stdout + drifted.stderr,
            )
        finally:
            EXPECTED_OUTPUTS[0].write_bytes(original)

    def test_cli_requires_exactly_one_mode(self):
        self.api_and_topology()
        command = [sys.executable, "-B", str(COMPILER)]
        no_mode = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
        both_modes = subprocess.run(
            command + ["--write", "--check"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(no_mode.returncode, 0)
        self.assertNotEqual(both_modes.returncode, 0)
        self.assertIn("exactly one", (no_mode.stdout + no_mode.stderr).lower())
        self.assertIn("exactly one", (both_modes.stdout + both_modes.stderr).lower())


if __name__ == "__main__":
    unittest.main()
