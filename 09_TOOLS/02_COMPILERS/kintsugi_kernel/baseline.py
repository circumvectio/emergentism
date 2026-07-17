from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from types import MappingProxyType
from typing import Any, Sequence

from .codec import load_canonical_value
from .diagnostics import BaselineResult, Issue, KintsugiError


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONTRACT = "09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json"
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
FAILED_RE = re.compile(r"^FAILED (?P<node>\S+)(?: - (?P<detail>.*))?$")
ERROR_RE = re.compile(r"^ERROR (?P<node>\S+)(?: - .*)?$")
EXCEPTION_RE = re.compile(r"^E\s+(?P<exception>[A-Za-z_][A-Za-z0-9_.]*(?:Error|Exception))(?::|$)")
BASELINE_COMMAND = ["python3", "-m", "pytest", "-q", "--tb=short"]
COLLECT_COMMAND = ["python3", "-m", "pytest", "--collect-only", "-q"]
EXIT_TWO_CODES = {"KIN-E-CLI", "KIN-E-IO"}
PYTEST_ENV = MappingProxyType({
    **{
        key: value for key, value in os.environ.items()
        if not key.startswith("PYTEST_")
    },
    "PYTEST_ADDOPTS": "-c /dev/null --rootdir=. -p no:cacheprovider",
    "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
})


def load_contract(path: Path) -> dict[str, Any]:
    value = load_canonical_value(path)
    validate_contract(value)
    return value


def validate_contract(value: Any) -> None:
    required = {
        "schemaVersion", "baseCommit", "command", "collectCommand",
        "collectedAtBaseline", "baselineNodeIds", "allowedFailures",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise KintsugiError("KIN-E-BASELINE", "contract", "contract keys differ from the fixed schema")
    if value["schemaVersion"] != "1.0.0" or not isinstance(value["baseCommit"], str) or not HASH_RE.fullmatch(value["baseCommit"]):
        raise KintsugiError("KIN-E-BASELINE", "contract", "invalid version or base commit")
    if value["command"] != BASELINE_COMMAND or value["collectCommand"] != COLLECT_COMMAND:
        raise KintsugiError("KIN-E-BASELINE", "commands", "baseline commands differ from fixed internal commands")
    nodes = value["baselineNodeIds"]
    if not isinstance(nodes, list) or not nodes or not all(isinstance(item, str) and "::" in item for item in nodes) or len(nodes) != len(set(nodes)):
        raise KintsugiError("KIN-E-BASELINE", "baselineNodeIds", "node IDs must be unique pytest node strings")
    if type(value["collectedAtBaseline"]) is not int or value["collectedAtBaseline"] != len(nodes):
        raise KintsugiError("KIN-E-BASELINE", "collectedAtBaseline", "count must equal baselineNodeIds length")
    failures = value["allowedFailures"]
    if not isinstance(failures, list):
        raise KintsugiError("KIN-E-BASELINE", "allowedFailures", "must be an array")
    failure_keys = {"nodeId", "exceptionType", "requiredSignature"}
    seen: set[str] = set()
    for index, item in enumerate(failures):
        if not isinstance(item, dict) or set(item) != failure_keys:
            raise KintsugiError("KIN-E-BASELINE", f"allowedFailures[{index}]", "invalid failure record")
        if item["nodeId"] not in nodes or item["nodeId"] in seen:
            raise KintsugiError("KIN-E-BASELINE", item["nodeId"], "failure node is absent or duplicated")
        if not all(isinstance(item[field], str) and item[field] for field in failure_keys):
            raise KintsugiError("KIN-E-BASELINE", item["nodeId"], "failure fields must be non-empty strings")
        seen.add(item["nodeId"])


def run_process(command: Sequence[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=root, text=True, capture_output=True, check=False,
        env=PYTEST_ENV,
    )


def parse_collected_nodes(output: str) -> set[str]:
    return {
        line.strip() for line in output.splitlines()
        if "::" in line and not line.startswith(("FAILED ", "ERROR "))
    }


def parse_failed_nodes(output: str) -> list[str]:
    nodes: list[str] = []
    for node in parse_failed_node_lines(output):
        if node not in nodes:
            nodes.append(node)
    return nodes


def parse_failed_node_lines(output: str) -> list[str]:
    return [
        match.group("node")
        for line in output.splitlines()
        if (match := FAILED_RE.match(line.strip()))
    ]


def parse_pytest_evidence(output: str) -> str:
    lines = [line for line in output.splitlines() if re.match(r"^E\s", line)]
    return "\n".join(lines) + ("\n" if lines else "")


def infer_exception(output: str) -> str:
    for line in output.splitlines():
        match = EXCEPTION_RE.match(line)
        if match:
            return match.group("exception").split(".")[-1]
    if any(line.startswith("E   assert") for line in output.splitlines()):
        return "AssertionError"
    return "UNKNOWN"


def parse_pytest_failures(output: str) -> dict[str, str]:
    failures: dict[str, str] = {}
    for line in output.splitlines():
        match = FAILED_RE.match(line.strip())
        if not match:
            continue
        detail = match.group("detail") or ""
        token = detail.split(":", 1)[0].split(" ", 1)[0]
        failures[match.group("node")] = token if token.endswith(("Error", "Exception")) else "UNKNOWN"
    return failures


def parse_pytest_errors(output: str) -> set[str]:
    return {
        match.group("node")
        for line in output.splitlines()
        if (match := ERROR_RE.match(line.strip()))
    }


def compare_baseline(contract: dict[str, Any], collected: set[str],
                     failures: dict[str, str], isolated_outputs: dict[str, str]) -> list[Issue]:
    issues: list[Issue] = []
    baseline = set(contract["baselineNodeIds"])
    allowed = {item["nodeId"]: item for item in contract["allowedFailures"]}
    for node in sorted(baseline - collected):
        issues.append(Issue(node, "KIN-E-BASELINE", "baseline node is missing or renamed"))
    for node, exception in sorted(failures.items()):
        record = allowed.get(node)
        if record is None:
            issues.append(Issue(node, "KIN-E-BASELINE", "new failing node is not allowlisted"))
            continue
        if exception != record["exceptionType"]:
            issues.append(Issue(node, "KIN-E-BASELINE", f"exception drift: {exception} != {record['exceptionType']}"))
        if record["requiredSignature"] not in isolated_outputs.get(node, ""):
            issues.append(Issue(node, "KIN-E-BASELINE", "required failure signature is absent"))
    return sorted(issues)


def run_baseline(root: Path, contract: dict[str, Any]) -> BaselineResult:
    collection = run_process(COLLECT_COMMAND, root)
    if collection.returncode != 0:
        issue = Issue("collectCommand", "KIN-E-BASELINE", "pytest collection command failed")
        return BaselineResult(0, 0, (issue,))
    collected = parse_collected_nodes(collection.stdout + collection.stderr)
    execution = run_process(BASELINE_COMMAND, root)
    combined = execution.stdout + execution.stderr
    failed_nodes = parse_failed_nodes(combined)
    error_nodes = parse_pytest_errors(combined)
    if execution.returncode not in (0, 1):
        issue = Issue("command", "KIN-E-BASELINE", f"pytest returned unexpected exit {execution.returncode}")
        return BaselineResult(len(collected), len(failed_nodes), (issue,))
    if error_nodes:
        issues = tuple(Issue(node, "KIN-E-BASELINE", "pytest runtime/collection error") for node in sorted(error_nodes))
        return BaselineResult(len(collected), len(failed_nodes), issues)
    if (execution.returncode == 0) != (not failed_nodes):
        issue = Issue("command", "KIN-E-BASELINE", "pytest exit code and failure summary disagree")
        return BaselineResult(len(collected), len(failed_nodes), (issue,))
    isolated: dict[str, str] = {}
    failures: dict[str, str] = {}
    issues: list[Issue] = []
    for node in sorted(failed_nodes):
        probe = run_process(["python3", "-m", "pytest", "-q", "--tb=short", node], root)
        probe_output = probe.stdout + probe.stderr
        probe_issues: list[Issue] = []
        if probe.returncode != 1:
            probe_issues.append(Issue(
                node, "KIN-E-BASELINE",
                f"isolated pytest returned unexpected exit {probe.returncode}",
            ))
        if parse_pytest_errors(probe_output):
            probe_issues.append(Issue(
                node, "KIN-E-BASELINE", "isolated pytest runtime/collection error",
            ))
        if parse_failed_node_lines(probe_output) != [node]:
            probe_issues.append(Issue(
                node, "KIN-E-BASELINE",
                "isolated failure summary differs from requested node",
            ))
        if probe_issues:
            issues.extend(probe_issues)
            continue
        evidence = parse_pytest_evidence(probe_output)
        isolated[node] = evidence
        failures[node] = infer_exception(evidence)
    issues.extend(compare_baseline(contract, collected, failures, isolated))
    return BaselineResult(len(collected), len(failures), tuple(sorted(issues)))
