#!/usr/bin/env python3
"""Validate or plan the seven Managed Agentz without remote mutation.

The former name-based provisioner could silently reuse stale hosted resources.
That path is retired.  Local checking and a deterministic plan are available;
remote application remains fail-closed until a pinned adapter can retrieve and
hash the complete observed provider payload before issuing a verified receipt.
"""

from __future__ import annotations

import argparse
import json
import sys

from contract import ContractError, validate_lock


REMOTE_ADAPTER_STATUS = "REMOTE_ADAPTER_UNSUPPORTED"


def local_plan(lock: dict) -> dict:
    return {
        "schemaVersion": "1.0",
        "mode": "offline_plan",
        "calibrationStatus": lock["calibrationStatus"],
        "bundleSha256": lock["bundleSha256"],
        "environment": lock["environment"],
        "agents": lock["agents"],
        "topology": lock["topology"],
        "remoteAdapter": {
            "status": "unsupported",
            "reason": (
                "No adapter is approved to retrieve, canonicalize, and compare every "
                "remote environment, agent, version, tool, permission, metadata, and "
                "coordinator-roster field."
            ),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check-local", action="store_true", help="validate the local semantic lock (default)")
    modes.add_argument("--plan", action="store_true", help="print the deterministic zero-mutation plan")
    modes.add_argument("--apply", action="store_true", help="request remote provisioning (currently refused)")
    args = parser.parse_args(argv)

    try:
        if args.apply:
            # Validate the local side before disclosing the external blocker.  No
            # provider SDK is imported and no client is constructed.
            validate_lock()
            print(
                f"{REMOTE_ADAPTER_STATUS}: local bundle is valid, but no "
                "remote-verifying adapter is approved; zero API calls made.",
                file=sys.stderr,
            )
            return 2

        lock = validate_lock()
        if args.plan:
            print(json.dumps(local_plan(lock), indent=2, ensure_ascii=False, sort_keys=True))
        else:
            print(
                "PROVISION-CHECK-OK: "
                f"agents=7 bundle={lock['bundleSha256']} status=unprovisioned_x0 "
                "remote_calls=0"
            )
        return 0
    except ContractError as exc:
        print(f"PROVISION-CHECK-ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
