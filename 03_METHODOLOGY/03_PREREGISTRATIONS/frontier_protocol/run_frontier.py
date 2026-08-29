#!/usr/bin/env python3
"""CLI for the offline Emergentism Frontier reference protocol."""

from __future__ import annotations

import argparse
import sys

from frontier_core import ROOT, build_graph, generate, validate_graph


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate_parser = subparsers.add_parser("generate", help="write deterministic public projections")
    generate_parser.add_argument("--check", action="store_true", help="fail on generated-byte drift")
    subparsers.add_parser("validate", help="validate the source-composed launch graph")
    args = parser.parse_args()

    try:
        if args.command == "generate":
            errors = generate(check=args.check)
            if errors:
                print("FRONTIER GENERATION: FAIL", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 2
            mode = "CHECK" if args.check else "WRITE"
            print(
                f"FRONTIER GENERATION: PASS · {mode} · 12 gaps · "
                "0 candidates · 0 tests · 0 receipts · 0 revisions"
            )
            return 0

        graph = build_graph(ROOT)
        errors = validate_graph(graph, root=ROOT)
        if errors:
            print("FRONTIER VALIDATION: FAIL", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 2
        print(
            "FRONTIER VALIDATION: PASS · source-bound · state axes separate · "
            "live service false"
        )
        return 0
    except (OSError, ValueError) as exc:
        print(f"FRONTIER: FAIL\n- {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
