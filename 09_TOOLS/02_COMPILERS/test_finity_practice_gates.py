#!/usr/bin/env python3
"""Contract tests for the typed-draft Finity practice evaluation gates."""

from __future__ import annotations

import hashlib
import copy
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKET_ROOT = (
    ROOT / "03_METHODOLOGY" / "03_PREREGISTRATIONS" / "finity_practice"
)
REGISTRY_PATH = PACKET_ROOT / "GATE_REGISTRY.json"
CARDS_PATH = ROOT / "00_META" / "claim_cards" / "finity_practice.yaml"
DOCKETS_PATH = ROOT / "00_META" / "ADEQUACY_DOCKETS.yaml"
RECEIPT_PATH = ROOT / "00_META" / "00_FINITY_PRACTICE_CLAIM_CARD_SET_01.md"

REGISTRY_KEYS = {
    "schema",
    "program_id",
    "created",
    "authority",
    "definition_source",
    "semantic_owner_ids",
    "claim_card_path",
    "claim_card_ids",
    "docket_ids",
    "packet_status_vocabulary",
    "contact_status_vocabulary",
    "program_boundary",
    "result_custody",
    "external_custody_contract",
    "external_state",
    "gates",
}
GATE_KEYS = {
    "gate_id",
    "title",
    "packet",
    "packet_sha256",
    "packet_status",
    "contact_status",
    "execution",
    "claim_card_ids",
    "docket_ids",
    "depends_on",
    "moves_if_passed",
    "does_not_move",
    "kill_or_revise",
}
EXECUTION_KEYS = {"state", "prerequisites", "ready_when"}
RESULT_CUSTODY_KEYS = {"owner_id", "index", "future_receipt_pattern", "rule"}
EXTERNAL_KEYS = {
    "participants_contacted",
    "reviewers_engaged",
    "ethics_determination_obtained",
    "preregistration_frozen",
    "data_collected",
    "results_exist",
    "independent_replication_exists",
}
PREREQUISITE_RECORD_KEYS = {
    "state",
    "artifact",
    "sha256",
    "receipt",
    "receipt_sha256",
}
EXTERNAL_RECORD_KEYS = {"state", "receipt", "receipt_sha256", "custodian_id"}
EXTERNAL_CUSTODY_KEYS = {
    "project_custodian_ids",
    "receipt_schema",
    "independence_rule",
    "boundary",
}
PACKET_STATUSES = {"typed", "packet-complete"}
CONTACT_STATUSES = {
    "deferred",
    "evidence-open",
    "component-supported",
    "independently-replicated",
    "narrowed",
    "killed",
    "frozen",
}
EXECUTION_STATES = {"blocked", "ready"}
EXPECTED_PREREQUISITES = {
    "FPE-READ-01": {
        "ethics_determination",
        "consent_script",
        "stimulus_manifest",
        "interviewer_script",
        "scoring_rubric",
        "data_management_plan",
        "adverse_event_route",
        "named_custodian",
    },
    "FPE-REVIEW-01": {
        "bundle_manifest",
        "conflict_form",
        "reviewer_scope_form",
        "compensation_terms",
        "publication_permission",
        "applicability_determination_recorded",
    },
    "FPE-COMPARE-01": {
        "same_hash_review_resolved",
        "ethics_determination",
        "consent_script",
        "materials_manifest",
        "component_equivalence_manifest",
        "sample_size_plan",
        "allocation_code",
        "analysis_code",
        "data_management_plan",
        "adverse_event_plan",
        "preregistration_receipt",
    },
}


def _bound_file(root: Path, relative: object, digest: object, label: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"{label}: missing path")
    raw = Path(relative)
    if raw.is_absolute() or ".." in raw.parts:
        raise ValueError(f"{label}: path escapes corpus")
    try:
        resolved = (root / raw).resolve(strict=True)
    except FileNotFoundError as error:
        raise ValueError(f"{label}: missing file") from error
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"{label}: resolved path escapes corpus")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError(f"{label}: invalid digest")
    if hashlib.sha256(resolved.read_bytes()).hexdigest() != digest:
        raise ValueError(f"{label}: stale digest")
    return resolved


def _bound_external_receipt(
    root: Path,
    record: dict,
    event: str,
    expected_schema: str,
) -> dict:
    receipt_path = _bound_file(
        root,
        record["receipt"],
        record["receipt_sha256"],
        f"external_state.{event}.receipt",
    )
    try:
        payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"external_state.{event}: receipt is not structured JSON") from error
    required = {
        "schema",
        "event",
        "custodian_id",
        "external_to_project",
        "conflicts_declared",
        "recorded_at",
    }
    if not isinstance(payload, dict) or not required.issubset(payload):
        raise ValueError(f"external_state.{event}: incomplete structured receipt")
    if payload["schema"] != expected_schema or payload["event"] != event:
        raise ValueError(f"external_state.{event}: receipt schema or event mismatch")
    if payload["custodian_id"] != record["custodian_id"]:
        raise ValueError(f"external_state.{event}: custodian is not bound in receipt")
    if not isinstance(payload["external_to_project"], bool):
        raise ValueError(f"external_state.{event}: external declaration must be boolean")
    if not isinstance(payload["conflicts_declared"], bool):
        raise ValueError(f"external_state.{event}: conflict declaration must be boolean")
    if not isinstance(payload["recorded_at"], str) or not payload["recorded_at"].strip():
        raise ValueError(f"external_state.{event}: missing recorded_at")
    return payload


def validate_lifecycle_evidence(registry: dict, root: Path) -> None:
    if set(registry["packet_status_vocabulary"]) != PACKET_STATUSES:
        raise ValueError("invalid packet-status vocabulary")
    if set(registry["contact_status_vocabulary"]) != CONTACT_STATUSES:
        raise ValueError("invalid contact-status vocabulary")
    custody_contract = registry["external_custody_contract"]
    if not isinstance(custody_contract, dict) or set(custody_contract) != EXTERNAL_CUSTODY_KEYS:
        raise ValueError("invalid external-custody contract")
    if not isinstance(custody_contract["project_custodian_ids"], list):
        raise ValueError("invalid project custodian registry")
    project_custodians = set(custody_contract["project_custodian_ids"])
    if len(project_custodians) != len(custody_contract["project_custodian_ids"]):
        raise ValueError("duplicate project custodian ID")
    expected_receipt_schema = custody_contract["receipt_schema"]
    semantic_owners = {
        owner
        for owners in registry["semantic_owner_ids"].values()
        for owner in owners
    }
    for gate in registry["gates"]:
        if gate["packet_status"] not in PACKET_STATUSES:
            raise ValueError(f"{gate['gate_id']}: invalid packet status")
        if gate["contact_status"] not in CONTACT_STATUSES:
            raise ValueError(f"{gate['gate_id']}: invalid contact status")
        if (
            gate["contact_status"] == "component-supported"
            and registry["external_state"]["results_exist"]["state"] != "present"
        ):
            raise ValueError(f"{gate['gate_id']}: component-supported without result receipt")
        if (
            gate["contact_status"] == "independently-replicated"
            and registry["external_state"]["independent_replication_exists"]["state"]
            != "present"
        ):
            raise ValueError(f"{gate['gate_id']}: replication status without independent receipt")
        execution = gate["execution"]
        if execution["state"] not in EXECUTION_STATES:
            raise ValueError(f"{gate['gate_id']}: invalid execution state")
        prerequisites = execution["prerequisites"]
        complete = True
        for name, record in prerequisites.items():
            if not isinstance(record, dict) or set(record) != PREREQUISITE_RECORD_KEYS:
                raise ValueError(f"{gate['gate_id']}.{name}: invalid evidence record")
            state = record["state"]
            if state == "missing":
                complete = False
                if any(record[key] is not None for key in PREREQUISITE_RECORD_KEYS - {"state"}):
                    raise ValueError(f"{gate['gate_id']}.{name}: missing record carries evidence")
            elif state == "satisfied":
                _bound_file(root, record["artifact"], record["sha256"], f"{gate['gate_id']}.{name}.artifact")
                _bound_file(root, record["receipt"], record["receipt_sha256"], f"{gate['gate_id']}.{name}.receipt")
            else:
                raise ValueError(f"{gate['gate_id']}.{name}: invalid prerequisite state")
        if gate["packet_status"] == "packet-complete" and not complete:
            raise ValueError(f"{gate['gate_id']}: packet-complete without evidence")
        if execution["state"] == "ready" and (
            gate["packet_status"] != "packet-complete" or not complete
        ):
            raise ValueError(f"{gate['gate_id']}: ready without complete evidence")
        if not complete and (
            execution["state"] != "blocked" or gate["contact_status"] != "deferred"
        ):
            raise ValueError(f"{gate['gate_id']}: incomplete gate is not fail-closed")

    receipt_payloads: dict[str, dict] = {}
    for name, record in registry["external_state"].items():
        if not isinstance(record, dict) or set(record) != EXTERNAL_RECORD_KEYS:
            raise ValueError(f"external_state.{name}: invalid evidence record")
        if record["state"] == "absent":
            if any(record[key] is not None for key in EXTERNAL_RECORD_KEYS - {"state"}):
                raise ValueError(f"external_state.{name}: absent state carries evidence")
        elif record["state"] == "present":
            if not isinstance(record["custodian_id"], str) or not record["custodian_id"].strip():
                raise ValueError(f"external_state.{name}: missing custodian")
            receipt_payloads[name] = _bound_external_receipt(
                root, record, name, expected_receipt_schema
            )
        else:
            raise ValueError(f"external_state.{name}: invalid state")

    external = registry["external_state"]
    if external["results_exist"]["state"] == "present" and external["data_collected"]["state"] != "present":
        raise ValueError("results exist without a data receipt")
    if external["independent_replication_exists"]["state"] == "present":
        if external["results_exist"]["state"] != "present":
            raise ValueError("replication exists without a result receipt")
        replication_custodian = external["independent_replication_exists"]["custodian_id"]
        original_custodians = {
            external["data_collected"]["custodian_id"],
            external["results_exist"]["custodian_id"],
        }
        if replication_custodian in original_custodians:
            raise ValueError("replication custodian matches original custody")
        if replication_custodian in project_custodians or replication_custodian in semantic_owners:
            raise ValueError("replication custodian uses internal project custody")
        replication_receipt = receipt_payloads["independent_replication_exists"]
        if not replication_receipt["external_to_project"]:
            raise ValueError("replication receipt does not declare external custody")
        if not replication_receipt["conflicts_declared"]:
            raise ValueError("replication receipt lacks conflict disclosure")

    for gate in registry["gates"]:
        if (
            gate["contact_status"] == "component-supported"
            and external["results_exist"]["state"] != "present"
        ):
            raise ValueError(f"{gate['gate_id']}: component-supported without result receipt")
        if (
            gate["contact_status"] == "independently-replicated"
            and external["independent_replication_exists"]["state"] != "present"
        ):
            raise ValueError(f"{gate['gate_id']}: replication status without independent receipt")


class FinityPracticeGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        cls.gate_rows = cls.registry["gates"]
        cls.gates = {gate["gate_id"]: gate for gate in cls.gate_rows}
        cls.cards_doc = json.loads(CARDS_PATH.read_text(encoding="utf-8"))
        cls.card_rows = cls.cards_doc["cards"]
        cls.cards = {card["card_id"]: card for card in cls.card_rows}
        cls.dockets_doc = json.loads(DOCKETS_PATH.read_text(encoding="utf-8"))
        cls.docket_rows = cls.dockets_doc["dockets"]
        cls.dockets = {row["docket_id"]: row for row in cls.docket_rows}

    def corpus_path(
        self,
        relative: str,
        *,
        must_exist: bool = True,
        within: Path = ROOT,
    ) -> Path:
        raw = Path(relative)
        self.assertFalse(raw.is_absolute(), relative)
        self.assertNotIn("..", raw.parts, relative)
        candidate = ROOT / raw
        resolved = candidate.resolve(strict=must_exist)
        self.assertTrue(resolved.is_relative_to(within.resolve()), relative)
        return resolved

    def assert_acyclic(self, graph: dict[str, list[str]]) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> None:
            if node in visiting:
                self.fail(f"dependency cycle at {node}")
            if node in visited:
                return
            visiting.add(node)
            for dependency in graph[node]:
                self.assertIn(dependency, graph, f"{node} -> {dependency}")
                self.assertNotEqual(node, dependency)
                visit(dependency)
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(node)

    def test_registry_schema_is_exact_routing_only_and_externally_empty(self) -> None:
        self.assertEqual(set(self.registry), REGISTRY_KEYS)
        self.assertEqual(
            self.registry["schema"],
            "emergentism/finity-practice-gate-registry/v2",
        )
        self.assertEqual(
            self.registry["authority"], "routing_only_no_semantic_authority"
        )
        self.assertEqual(set(self.registry["result_custody"]), RESULT_CUSTODY_KEYS)
        self.assertEqual(
            set(self.registry["external_custody_contract"]), EXTERNAL_CUSTODY_KEYS
        )
        self.assertEqual(
            self.registry["external_custody_contract"]["project_custodian_ids"],
            [f"K-{index}" for index in range(1, 8)],
        )
        self.assertEqual(
            self.registry["external_custody_contract"]["receipt_schema"],
            "emergentism/finity-practice-external-receipt/v1",
        )
        self.assertEqual(set(self.registry["external_state"]), EXTERNAL_KEYS)
        for record in self.registry["external_state"].values():
            self.assertEqual(set(record), EXTERNAL_RECORD_KEYS)
            self.assertEqual(record["state"], "absent")
            self.assertTrue(
                all(record[key] is None for key in EXTERNAL_RECORD_KEYS - {"state"})
            )
        for gate in self.gate_rows:
            self.assertEqual(set(gate), GATE_KEYS, gate["gate_id"])
            self.assertEqual(set(gate["execution"]), EXECUTION_KEYS, gate["gate_id"])

    def test_ids_are_unique_before_indexing_and_bind_existing_cards_and_dockets(self) -> None:
        gate_ids = [row["gate_id"] for row in self.gate_rows]
        card_ids = [row["card_id"] for row in self.card_rows]
        docket_ids = [row["docket_id"] for row in self.docket_rows]
        self.assertEqual(len(gate_ids), len(set(gate_ids)))
        self.assertEqual(len(card_ids), len(set(card_ids)))
        self.assertEqual(len(docket_ids), len(set(docket_ids)))
        self.assertEqual(
            set(gate_ids), {"FPE-READ-01", "FPE-REVIEW-01", "FPE-COMPARE-01"}
        )
        self.assertEqual(set(docket_ids), {f"A{i}" for i in range(8)})
        self.assertEqual(self.registry["claim_card_ids"], ["FIN01-01", "FIN01-02"])
        self.assertEqual(self.registry["docket_ids"], ["A3", "A5"])
        for gate in self.gate_rows:
            self.assertTrue(set(gate["claim_card_ids"]).issubset(card_ids))
            self.assertTrue(set(gate["docket_ids"]).issubset(docket_ids))

    def test_definition_source_and_semantic_owners_are_bound_not_reassigned(self) -> None:
        definition = self.registry["definition_source"]
        self.assertEqual(set(definition), {"path", "section", "sha256"})
        self.assertEqual(definition["section"], "3B")
        self.assertEqual(
            self.registry["semantic_owner_ids"],
            {"FIN01-01": ["K-5"], "FIN01-02": ["K-4"]},
        )
        self.assertNotIn("source_owner", self.registry)
        source = self.corpus_path(definition["path"])
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), definition["sha256"])
        self.assertEqual(self.cards_doc["source"]["path"], definition["path"])
        self.assertEqual(
            {card_id: self.cards[card_id]["owner_ids"] for card_id in self.registry["claim_card_ids"]},
            self.registry["semantic_owner_ids"],
        )

    def test_all_declared_paths_are_corpus_relative_and_contained(self) -> None:
        self.corpus_path(self.registry["claim_card_path"])
        self.corpus_path(self.registry["definition_source"]["path"])
        self.corpus_path(self.registry["result_custody"]["index"])
        self.corpus_path(
            self.registry["result_custody"]["future_receipt_pattern"],
            must_exist=False,
        )
        for gate in self.gate_rows:
            self.corpus_path(gate["packet"], within=PACKET_ROOT)
        for card in self.card_rows:
            for receipt in card["review"]["receipts"]:
                self.corpus_path(receipt)

    def test_packets_match_current_draft_hashes_and_readiness_is_fail_closed(self) -> None:
        self.assertEqual(self.registry["packet_status_vocabulary"], ["typed", "packet-complete"])
        for gate in self.gate_rows:
            packet = self.corpus_path(gate["packet"], within=PACKET_ROOT)
            self.assertEqual(
                gate["packet_sha256"],
                hashlib.sha256(packet.read_bytes()).hexdigest(),
                gate["gate_id"],
            )
            self.assertEqual(gate["packet_status"], "typed")
            self.assertEqual(gate["contact_status"], "deferred")
            execution = gate["execution"]
            prerequisites = execution["prerequisites"]
            self.assertEqual(set(prerequisites), EXPECTED_PREREQUISITES[gate["gate_id"]])
            for record in prerequisites.values():
                self.assertEqual(set(record), PREREQUISITE_RECORD_KEYS)
                self.assertEqual(record["state"], "missing")
                self.assertTrue(
                    all(
                        record[key] is None
                        for key in PREREQUISITE_RECORD_KEYS - {"state"}
                    )
                )
            self.assertEqual(execution["state"], "blocked")
            self.assertTrue(execution["ready_when"].strip())
        validate_lifecycle_evidence(self.registry, ROOT)

    def test_lifecycle_evidence_mutations_fail_closed(self) -> None:
        def cloned() -> dict:
            return copy.deepcopy(self.registry)

        true_without_evidence = cloned()
        true_without_evidence["gates"][0]["execution"]["prerequisites"]["consent_script"]["state"] = "satisfied"
        with self.assertRaisesRegex(ValueError, "missing path"):
            validate_lifecycle_evidence(true_without_evidence, ROOT)

        missing_file = cloned()
        record = missing_file["gates"][0]["execution"]["prerequisites"]["consent_script"]
        record.update(
            state="satisfied",
            artifact="00_META/does-not-exist.md",
            sha256="0" * 64,
            receipt="00_META/does-not-exist-receipt.md",
            receipt_sha256="0" * 64,
        )
        with self.assertRaisesRegex(ValueError, "missing file"):
            validate_lifecycle_evidence(missing_file, ROOT)

        stale_hash = cloned()
        record = stale_hash["gates"][0]["execution"]["prerequisites"]["consent_script"]
        record.update(
            state="satisfied",
            artifact="00_META/00_FINITY_PRACTICE_CLAIM_CARD_SET_01.md",
            sha256="0" * 64,
            receipt="00_META/00_FINITY_PRACTICE_CLAIM_CARD_SET_01.md",
            receipt_sha256="0" * 64,
        )
        with self.assertRaisesRegex(ValueError, "stale digest"):
            validate_lifecycle_evidence(stale_hash, ROOT)

        promoted_without_evidence = cloned()
        promoted_without_evidence["gates"][0]["packet_status"] = "packet-complete"
        with self.assertRaisesRegex(ValueError, "packet-complete without evidence"):
            validate_lifecycle_evidence(promoted_without_evidence, ROOT)

        result_without_receipt = cloned()
        result_without_receipt["external_state"]["results_exist"].update(
            state="present", custodian_id="CUSTODIAN-UNBOUND"
        )
        with self.assertRaisesRegex(ValueError, "missing path"):
            validate_lifecycle_evidence(result_without_receipt, ROOT)

        invalid_execution = cloned()
        invalid_execution["gates"][0]["execution"]["state"] = "unexpected-state"
        with self.assertRaisesRegex(ValueError, "invalid execution state"):
            validate_lifecycle_evidence(invalid_execution, ROOT)

        invalid_contact = cloned()
        invalid_contact["gates"][0]["contact_status"] = "unsupported-status"
        with self.assertRaisesRegex(ValueError, "invalid contact status"):
            validate_lifecycle_evidence(invalid_contact, ROOT)

        unsupported_replication_status = cloned()
        unsupported_replication_status["gates"][0]["contact_status"] = "independently-replicated"
        with self.assertRaisesRegex(ValueError, "replication status without independent receipt"):
            validate_lifecycle_evidence(unsupported_replication_status, ROOT)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)

            def bind_external(
                registry: dict,
                event: str,
                custodian: str,
                *,
                external: bool,
                conflicts: bool = True,
            ) -> None:
                relative = f"{event}.json"
                payload = {
                    "schema": registry["external_custody_contract"]["receipt_schema"],
                    "event": event,
                    "custodian_id": custodian,
                    "external_to_project": external,
                    "conflicts_declared": conflicts,
                    "recorded_at": "2026-07-28T00:00:00Z",
                }
                target = temp_root / relative
                target.write_text(
                    json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8"
                )
                registry["external_state"][event].update(
                    state="present",
                    receipt=relative,
                    receipt_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                    custodian_id=custodian,
                )

            same_custodian = cloned()
            for event in (
                "data_collected",
                "results_exist",
                "independent_replication_exists",
            ):
                bind_external(
                    same_custodian,
                    event,
                    "CUSTODIAN-SAME",
                    external=event == "independent_replication_exists",
                )
            with self.assertRaisesRegex(ValueError, "matches original custody"):
                validate_lifecycle_evidence(same_custodian, temp_root)

            internal_replication = cloned()
            bind_external(internal_replication, "data_collected", "CUSTODIAN-DATA", external=False)
            bind_external(internal_replication, "results_exist", "CUSTODIAN-RESULT", external=False)
            bind_external(internal_replication, "independent_replication_exists", "K-7", external=True)
            with self.assertRaisesRegex(ValueError, "internal project custody"):
                validate_lifecycle_evidence(internal_replication, temp_root)

            missing_conflict_declaration = cloned()
            bind_external(missing_conflict_declaration, "data_collected", "CUSTODIAN-DATA", external=False)
            bind_external(missing_conflict_declaration, "results_exist", "CUSTODIAN-RESULT", external=False)
            bind_external(
                missing_conflict_declaration,
                "independent_replication_exists",
                "CUSTODIAN-EXTERNAL",
                external=True,
                conflicts=False,
            )
            with self.assertRaisesRegex(ValueError, "lacks conflict disclosure"):
                validate_lifecycle_evidence(missing_conflict_declaration, temp_root)

    def test_gate_and_docket_dependency_graphs_are_valid_and_acyclic(self) -> None:
        gate_graph = {row["gate_id"]: row["depends_on"] for row in self.gate_rows}
        docket_graph = {
            row["docket_id"]: row["depends_on"] for row in self.docket_rows
        }
        self.assertEqual(
            gate_graph,
            {
                "FPE-READ-01": [],
                "FPE-REVIEW-01": [],
                "FPE-COMPARE-01": ["FPE-REVIEW-01"],
            },
        )
        for graph in (gate_graph, docket_graph):
            for node, dependencies in graph.items():
                self.assertEqual(len(dependencies), len(set(dependencies)), node)
            self.assert_acyclic(graph)
        self.assertIn(
            "does not move", self.gates["FPE-READ-01"]["does_not_move"].lower()
        )
        self.assertIn(
            "does not move", self.gates["FPE-REVIEW-01"]["does_not_move"].lower()
        )

    def test_claim_card_locators_dereference_definition_and_retirement(self) -> None:
        source = self.corpus_path(self.cards_doc["source"]["path"])
        lines = source.read_text(encoding="utf-8").splitlines()
        expected = {
            "FIN01-01": {
                "locator": {"section": "3B", "line_start": 129, "line_end": 148},
                "markers": (
                    "## 3B. The Finity Card",
                    "**Finity Card**",
                    "DECISION",
                    "RECEIPT",
                    "theorem, ontology, authorization",
                ),
            },
            "FIN01-02": {
                "locator": {"section": "3B", "line_start": 150, "line_end": 156},
                "markers": (
                    "selected practice `[S]`",
                    "remains `[C]`",
                    "retire the",
                    "branding",
                ),
            },
        }
        for card_id, contract in expected.items():
            locator = self.cards[card_id]["locator"]
            self.assertEqual(locator, contract["locator"])
            start, end = locator["line_start"], locator["line_end"]
            chunk = "\n".join(lines[start - 1 : end])
            for marker in contract["markers"]:
                self.assertIn(marker, chunk, f"{card_id}: {marker}")
            preceding_heading = next(
                line for line in reversed(lines[:start]) if line.startswith("## ")
            )
            self.assertIn(locator["section"], preceding_heading)
        self.assertEqual(self.cards["FIN01-02"]["evidence"][0]["tier"], "C")
        self.assertEqual(self.cards["FIN01-02"]["public"]["state"], "candidate")

    def test_review_receipt_locator_rows_match_cards_and_scope_is_internal(self) -> None:
        receipt = RECEIPT_PATH.read_text(encoding="utf-8")
        pattern = re.compile(
            r"\|\s*`(?P<id>FIN01-\d{2})`\s*\|\s*Lived Compass §(?P<section>[^,]+), "
            r"lines (?P<start>\d+)–(?P<end>\d+)\s*\|"
        )
        rows = {
            match.group("id"): {
                "section": match.group("section"),
                "line_start": int(match.group("start")),
                "line_end": int(match.group("end")),
            }
            for match in pattern.finditer(receipt)
        }
        self.assertEqual(set(rows), {"FIN01-01", "FIN01-02"})
        for card_id, locator in rows.items():
            self.assertEqual(locator, self.cards[card_id]["locator"])
            self.assertEqual(
                self.cards[card_id]["review"]["scope"],
                "source_type_owner_rival_kill_and_public_ceiling_only",
            )
        normalized_receipt = " ".join(receipt.split())
        for marker in (
            "not an independent review",
            "field result",
            "replication",
            "validation of Emergentism",
            "not the external review gate",
        ):
            self.assertIn(marker, normalized_receipt)

    def test_comprehension_packet_tests_transfer_not_parroting(self) -> None:
        text = self.corpus_path(self.gates["FPE-READ-01"]["packet"]).read_text(
            encoding="utf-8"
        )
        for marker in (
            "TYPED DRAFT · CONTACT DEFERRED",
            "Phase A — five-second first contact",
            "Phase C — unbranded transfer",
            "Award no credit merely for repeating corpus vocabulary.",
            "four of five readers",
            "not a population estimate",
            "ETHICS DETERMINATION REQUIRED BEFORE RECRUITMENT",
        ):
            self.assertIn(marker, text)

    def test_review_packet_preserves_independence_and_dissent(self) -> None:
        text = self.corpus_path(self.gates["FPE-REVIEW-01"]["packet"]).read_text(
            encoding="utf-8"
        )
        for marker in (
            "TYPED DRAFT · CONTACT DEFERRED",
            "AI or project-agent review",
            "same frozen bundle",
            "There is no single compensating score.",
            "never edit the reviewer's verdict",
            "NO REVIEWER ENGAGED · NO REVIEW EXISTS",
            "heterogeneous usual practice",
        ):
            self.assertIn(marker, text)

    def test_comparison_has_fair_arms_construct_map_and_separate_outcomes(self) -> None:
        text = self.corpus_path(self.gates["FPE-COMPARE-01"]["packet"]).read_text(
            encoding="utf-8"
        )
        for marker in (
            "TYPED DRAFT · CONTACT DEFERRED",
            "F — branded Finity",
            "U — content-identical, brand-masked",
            "C — Ordinary Decision Record",
            "M — usual method",
            "Draft construct map — not yet a frozen equivalence manifest",
            "normalized F/U equality",
            "a vector, never one compensating score",
            "No defensible participant count exists before these inputs.",
            "Intention-to-treat is primary",
            "primary confirmatory comparator contrast is `U − C`",
            "assignment to the Ordinary Decision Record versus heterogeneous",
            "NOT PREREGISTERED · NOT RUN",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("usual unstructured attention", text)

    def test_public_lab_shows_draft_absence_and_scope_ceiling(self) -> None:
        page = (ROOT / "12_PUBLIC_SITE" / "lab" / "index.html").read_text(
            encoding="utf-8"
        )
        section_match = re.search(
            r'<section[^>]+id="finity-gates".*?</section>', page, re.DOTALL
        )
        self.assertIsNotNone(section_match)
        section = section_match.group(0) if section_match else ""
        for marker in (
            "Three candidate protocols are typed as drafts",
            "FPE-READ-01 · TYPED DRAFT · NOT RUN",
            "FPE-REVIEW-01 · TYPED DRAFT · NO REVIEW EXISTS",
            "FPE-COMPARE-01 · TYPED DRAFT · NOT PREREGISTERED",
            "None of these gates validates an ontology.",
            "The ordinary method is allowed to win.",
        ):
            self.assertIn(marker, section)
        for forbidden in (
            "Practice validation",
            "The protocols are specified",
            "packet-complete",
            "Finity evaluation program is now packet-complete",
            "validated Finity",
            "Finity is validated",
            "Finity is effective",
            "Finity improves decisions.",
            "proven decision improvement",
        ):
            self.assertNotIn(forbidden, section)


if __name__ == "__main__":
    unittest.main()
