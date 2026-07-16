#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from kintsugi_kernel import (  # noqa: F401 - frozen A0 compatibility exports
    BASELINE_COMMAND,
    COLLECT_COMMAND,
    DEFAULT_CONTRACT,
    ERROR_RE,
    EXCEPTION_RE,
    EXIT_TWO_CODES,
    FAILED_RE,
    HASH_RE,
    PYTEST_ENV,
    ROOT,
    ROOT_ROLES,
    SCHEMA_ID,
    SCHEMA_KEYWORDS,
    BaselineResult,
    Issue,
    KintsugiError,
    canonical_json_bytes,
    compare_baseline,
    evaluate_antibody_fixture,
    evaluate_semantic_fixture,
    infer_exception,
    load_contract,
    load_schema,
    normalize_lf,
    parse_collected_nodes,
    parse_failed_node_lines,
    parse_failed_nodes,
    parse_pytest_errors,
    parse_pytest_evidence,
    parse_pytest_failures,
    raw_hash,
    run_baseline,
    run_process,
    safe_regex_search,
    safe_repo_path,
    text_hash,
    validate_contract,
    validate_core_records,
    validate_inputs,
    validate_named_definition,
    validate_schema_document,
    validate_schema_instance,
    validate_public_queue,
    scan_antibodies,
)


DEFAULT_DATA = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
DEFAULT_SCHEMA = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
DEFAULT_LEDGER = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
DEFAULT_PUBLIC_QUEUE = (
    "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_public_propagation_queue.json"
)
DEFAULT_BASELINE_ALLOWLIST = DEFAULT_CONTRACT


class KintsugiArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise KintsugiError("KIN-E-CLI", "CLI", message)


class ExplicitStoreAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: object,
        option_string: str | None = None,
    ) -> None:
        del parser, option_string
        setattr(namespace, self.dest, values)
        setattr(namespace, f"_{self.dest}_explicit", True)

def build_parser() -> argparse.ArgumentParser:
    parser = KintsugiArgumentParser(prog="validate_kintsugi.py", add_help=False)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--check-baseline", action="store_true")
    parser.add_argument(
        "--contract", action=ExplicitStoreAction, default=DEFAULT_CONTRACT
    )
    parser.add_argument(
        "--baseline-allowlist",
        action=ExplicitStoreAction,
        default=DEFAULT_BASELINE_ALLOWLIST,
    )
    parser.add_argument("--phase", choices=("A", "B", "C"))
    parser.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--base-ref", action=ExplicitStoreAction)
    parser.add_argument("--data", action=ExplicitStoreAction, default=DEFAULT_DATA)
    parser.add_argument("--schema", action=ExplicitStoreAction, default=DEFAULT_SCHEMA)
    parser.add_argument("--ledger", action=ExplicitStoreAction, default=DEFAULT_LEDGER)
    parser.add_argument(
        "--public-queue", action=ExplicitStoreAction, default=DEFAULT_PUBLIC_QUEUE
    )
    parser.add_argument(
        "--canonical-root",
        type=Path,
        action=ExplicitStoreAction,
        default=ROOT,
    )
    parser.set_defaults(
        _contract_explicit=False,
        _baseline_allowlist_explicit=False,
        _base_ref_explicit=False,
        _data_explicit=False,
        _schema_explicit=False,
        _ledger_explicit=False,
        _public_queue_explicit=False,
        _canonical_root_explicit=False,
    )
    return parser

def emit_error(error: KintsugiError) -> None:
    print(f"KIN-ERROR {error.path} {error.code}: {error.message}", file=sys.stderr)


def _safe_repo_input(root: Path, relative: str) -> Path:
    try:
        return safe_repo_path(root, relative)
    except RuntimeError:
        raise KintsugiError(
            "KIN-E-PATH",
            relative,
            "repository-relative input cannot be resolved safely",
        ) from None


def _load_baseline_contract(path: Path) -> dict[str, object]:
    try:
        return load_contract(path)
    except RecursionError:
        raise KintsugiError(
            "KIN-E-JSON",
            str(path),
            "JSON exceeds the supported nesting depth",
        ) from None
    except UnicodeError:
        raise KintsugiError(
            "KIN-E-CANONICAL",
            str(path),
            "JSON contains a string that cannot be encoded as canonical UTF-8",
        ) from None
    except ValueError:
        raise KintsugiError(
            "KIN-E-JSON",
            str(path),
            "JSON value exceeds the supported decoder limits",
        ) from None


def _baseline_path(args: argparse.Namespace) -> Path:
    contract_path = _safe_repo_input(ROOT, args.contract)
    allowlist_path = _safe_repo_input(ROOT, args.baseline_allowlist)
    if (
        args._contract_explicit
        and args._baseline_allowlist_explicit
        and contract_path != allowlist_path
    ):
        raise KintsugiError(
            "KIN-E-CLI",
            "baseline-allowlist",
            "--contract and --baseline-allowlist conflict",
        )
    return allowlist_path if args._baseline_allowlist_explicit else contract_path


def _validate_baseline_arguments(args: argparse.Namespace) -> None:
    check_only_inputs = (
        args.phase is not None
        or args.bootstrap
        or args._base_ref_explicit
        or args._data_explicit
        or args._schema_explicit
        or args._ledger_explicit
        or args._public_queue_explicit
    )
    if check_only_inputs:
        raise KintsugiError(
            "KIN-E-CLI",
            "arguments",
            "baseline mode rejects phase, bootstrap, and full-check inputs",
        )


def _validate_check_arguments(args: argparse.Namespace) -> None:
    if args._contract_explicit or args._baseline_allowlist_explicit:
        raise KintsugiError(
            "KIN-E-CLI",
            "arguments",
            "--contract and --baseline-allowlist are baseline mode inputs",
        )
    if args.bootstrap and args.phase != "A":
        raise KintsugiError(
            "KIN-E-CLI", "arguments", "--bootstrap is permitted only for Phase A"
        )
    if args.phase is None:
        if args._base_ref_explicit or args._canonical_root_explicit:
            raise KintsugiError(
                "KIN-E-CLI",
                "arguments",
                "--base-ref and --canonical-root require --phase",
            )
        return
    if not args._base_ref_explicit or not args.base_ref:
        raise KintsugiError(
            "KIN-E-CLI", "arguments", "--base-ref is required with --phase"
        )
    if not args._canonical_root_explicit:
        raise KintsugiError(
            "KIN-E-CLI",
            "arguments",
            "an explicit --canonical-root is required with --phase",
        )
    if not args.canonical_root.is_absolute():
        raise KintsugiError(
            "KIN-E-CLI", "arguments", "--canonical-root must be absolute"
        )


def _resolve_canonical_root(path: Path) -> Path:
    try:
        return path.resolve(strict=True)
    except RuntimeError:
        raise KintsugiError(
            "KIN-E-PATH",
            str(path),
            "canonical root cannot be resolved safely",
        ) from None

def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        if not args.check and not args.check_baseline:
            raise KintsugiError(
                "KIN-E-CLI", "arguments", "--check or --check-baseline is required"
            )

        if args.check_baseline:
            _validate_baseline_arguments(args)
            contract_path = _baseline_path(args)
            contract = _load_baseline_contract(contract_path)
            root = _resolve_canonical_root(args.canonical_root)
            if not (root / ".git").exists():
                raise KintsugiError("KIN-E-PATH", str(root), "canonical root is not a Git checkout")
            result = run_baseline(root, contract)
            if result.issues:
                for issue in result.issues:
                    emit_error(KintsugiError(issue.code, issue.path, issue.message))
                return 1
            print(f"KIN-OK baseline collected={result.collected} failures={result.failures}")
            return 0

        _validate_check_arguments(args)
        data_path = _safe_repo_input(ROOT, args.data)
        schema_path = _safe_repo_input(ROOT, args.schema)
        ledger_path = _safe_repo_input(ROOT, args.ledger)
        public_queue_path = None
        if args.phase == "C" or args._public_queue_explicit:
            public_queue_path = _safe_repo_input(ROOT, args.public_queue)

        canonical_root = None
        if args.phase is not None:
            canonical_root = _resolve_canonical_root(args.canonical_root)

        issues = validate_inputs(
            root=ROOT,
            data_path=data_path,
            schema_path=schema_path,
            ledger_path=ledger_path,
            phase=args.phase,
            bootstrap=args.bootstrap,
            base_ref=args.base_ref,
            canonical_root=canonical_root,
            public_queue_path=public_queue_path,
        )
        if issues:
            for issue in sorted(issues):
                emit_error(KintsugiError(issue.code, issue.path, issue.message))
            return 1
        print("KIN-OK validation")
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
