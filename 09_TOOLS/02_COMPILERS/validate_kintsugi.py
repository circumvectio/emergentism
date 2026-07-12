#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from kintsugi_kernel import (
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
    BaselineResult,
    Issue,
    KintsugiError,
    canonical_json_bytes,
    compare_baseline,
    infer_exception,
    load_contract,
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
    safe_repo_path,
    text_hash,
    validate_contract,
)

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
