#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from kintsugi_kernel.diagnostics import KintsugiError
from kintsugi_kernel.rendering import (
    RenderTransactionRequest,
    write_rendered_value,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORE = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"


class RendererArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise KintsugiError("KIN-E-CLI", "CLI", message)


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--phase", required=True, choices=("A", "B", "C"))
    parser.add_argument("--data", dest="core_path", default=DEFAULT_CORE)
    parser.add_argument("--output", dest="output_path", required=True)
    parser.add_argument("--canonical-root", type=Path)
    parser.add_argument("--base-ref")
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--expected-core-sha256", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = RendererArgumentParser(prog="render_kintsugi.py")
    operations = parser.add_subparsers(
        dest="operation", required=True, parser_class=RendererArgumentParser
    )

    freeze = operations.add_parser("freeze-manifest")
    _common(freeze)
    freeze.add_argument("--final", action="store_true")
    freeze.add_argument("--finding-dispositions-input", type=Path)

    target = operations.add_parser("review-target")
    _common(target)

    bundle = operations.add_parser("bundle")
    _common(bundle)

    transition = operations.add_parser("transition-core")
    _common(transition)
    transition.add_argument(
        "--stage",
        required=True,
        choices=("ATTESTED", "FAILED", "ABANDONED", "COMPLETE", "VERIFIED"),
    )
    transition.add_argument("--logic-review-input", type=Path)
    transition.add_argument("--btj-review-input", type=Path)
    transition.add_argument("--abandon-reason")
    return parser


def _request(args: argparse.Namespace) -> RenderTransactionRequest:
    if args.operation == "freeze-manifest" and not args.final:
        raise KintsugiError(
            "KIN-E-CLI",
            "final",
            "freeze-manifest requires --final",
        )
    return RenderTransactionRequest(
        operation=args.operation,
        phase=args.phase,
        stage=getattr(args, "stage", None),
        core_path=args.core_path,
        output_path=args.output_path,
        canonical_root=args.canonical_root,
        base_ref=args.base_ref,
        expected_head=args.expected_head,
        expected_core_sha256=args.expected_core_sha256,
        logic_review_input=getattr(args, "logic_review_input", None),
        btj_review_input=getattr(args, "btj_review_input", None),
        finding_dispositions_input=getattr(
            args, "finding_dispositions_input", None
        ),
        abandon_reason=getattr(args, "abandon_reason", None),
    )


def _emit(error: KintsugiError) -> None:
    print(
        f"KIN-ERROR {error.path} {error.code}: {error.message}",
        file=sys.stderr,
    )


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        request = _request(args)
    except KintsugiError as error:
        _emit(error)
        return 2
    try:
        write_rendered_value(ROOT, request=request)
    except KintsugiError as error:
        _emit(error)
        return 1
    stage = request.stage or ("FINAL" if request.operation == "freeze-manifest" else "NONE")
    print(
        f"KIN-OK render operation={request.operation} phase={request.phase} stage={stage}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
