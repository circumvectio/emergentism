#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT = "09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json"
HASH_RE = re.compile(r"^[0-9a-f]{40}$")
FAILED_RE = re.compile(r"^FAILED (?P<node>\S+)(?: - (?P<detail>.*))?$")
ERROR_RE = re.compile(r"^ERROR (?P<node>\S+)(?: - .*)?$")
EXCEPTION_RE = re.compile(r"^E\s+(?P<exception>[A-Za-z_][A-Za-z0-9_.]*(?:Error|Exception))(?::|$)")
BASELINE_COMMAND = ["python3", "-m", "pytest", "-q", "--tb=short"]
COLLECT_COMMAND = ["python3", "-m", "pytest", "--collect-only", "-q"]
EXIT_TWO_CODES = {"KIN-E-CLI", "KIN-E-IO"}

@dataclass(frozen=True, order=True)
class Issue:
    path: str
    code: str
    message: str

@dataclass(frozen=True)
class BaselineResult:
    collected: int
    failures: int
    issues: tuple[Issue, ...]

class KintsugiError(Exception):
    def __init__(self, code: str, path: str, message: str):
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message

def canonical_json_bytes(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise KintsugiError("KIN-E-CANONICAL", "json", str(exc)) from None
    return (rendered + "\n").encode("utf-8")

def raw_hash(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()

def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

def text_hash(text: str) -> str:
    return "sha256-text-lf:" + hashlib.sha256(normalize_lf(text).encode("utf-8")).hexdigest()

def safe_repo_path(root: Path, relative: str) -> Path:
    if not relative or relative.startswith("/") or "\\" in relative:
        raise KintsugiError("KIN-E-PATH", relative or "<empty>", "path must be non-empty repository-relative POSIX")
    pure = PurePosixPath(relative)
    if any(part in ("", ".", "..") for part in pure.parts):
        raise KintsugiError("KIN-E-PATH", relative, "path contains a forbidden segment")
    candidate = (root / Path(*pure.parts)).resolve(strict=False)
    try:
        candidate.relative_to(root.resolve(strict=True))
    except ValueError:
        raise KintsugiError("KIN-E-PATH", relative, "path escapes repository root") from None
    return candidate

def load_contract(path: Path) -> dict[str, Any]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise KintsugiError("KIN-E-IO", str(path), str(exc)) from None
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        if isinstance(exc, json.JSONDecodeError):
            detail = f"line {exc.lineno} column {exc.colno}: {exc.msg}"
        else:
            detail = str(exc)
        raise KintsugiError("KIN-E-JSON", str(path), detail) from None
    if payload != canonical_json_bytes(value):
        raise KintsugiError("KIN-E-CANONICAL", str(path), "JSON bytes are not canonical")
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
    return subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)

def parse_collected_nodes(output: str) -> set[str]:
    return {
        line.strip() for line in output.splitlines()
        if "::" in line and not line.startswith(("FAILED ", "ERROR "))
    }

def parse_failed_nodes(output: str) -> list[str]:
    nodes: list[str] = []
    for line in output.splitlines():
        match = FAILED_RE.match(line.strip())
        if match and match.group("node") not in nodes:
            nodes.append(match.group("node"))
    return nodes

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
    for node in sorted(failed_nodes):
        probe = run_process(["python3", "-m", "pytest", "-q", "--tb=short", node], root)
        isolated[node] = probe.stdout + probe.stderr
        failures[node] = infer_exception(isolated[node])
    issues = compare_baseline(contract, collected, failures, isolated)
    return BaselineResult(len(collected), len(failures), tuple(issues))

class KintsugiArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise KintsugiError("KIN-E-CLI", "CLI", message)

def build_parser() -> argparse.ArgumentParser:
    parser = KintsugiArgumentParser(prog="validate_kintsugi.py", add_help=False)
    parser.add_argument("--check-baseline", action="store_true")
    parser.add_argument("--contract", default=DEFAULT_CONTRACT)
    parser.add_argument("--canonical-root", type=Path, default=ROOT)
    return parser

def emit_error(error: KintsugiError) -> None:
    print(f"KIN-ERROR {error.path} {error.code}: {error.message}", file=sys.stderr)

def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        if not args.check_baseline:
            raise KintsugiError("KIN-E-CLI", "arguments", "--check-baseline is required in A0")
        contract_path = safe_repo_path(ROOT, args.contract)
        contract = load_contract(contract_path)
        root = args.canonical_root.resolve(strict=True)
        if not (root / ".git").exists():
            raise KintsugiError("KIN-E-PATH", str(root), "canonical root is not a Git checkout")
        result = run_baseline(root, contract)
        if result.issues:
            for issue in result.issues:
                emit_error(KintsugiError(issue.code, issue.path, issue.message))
            return 1
        print(f"KIN-OK baseline collected={result.collected} failures={result.failures}")
        return 0
    except KintsugiError as exc:
        if exc.code in EXIT_TWO_CODES:
            emit_error(KintsugiError(exc.code, "CLI", f"{exc.path}: {exc.message}"))
            return 2
        emit_error(exc)
        return 1
    except (OSError, subprocess.SubprocessError) as exc:
        emit_error(KintsugiError("KIN-E-IO", "CLI", str(exc)))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
