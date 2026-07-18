#!/usr/bin/env python3
"""Fail-closed preflight for a future hosted Managed Agentz run.

Execution is intentionally unavailable in this wave.  Preflight binds a typed
RunRequest to the current local bundle and to a full, remote-verified deployment
receipt.  It does not construct a provider client, auto-confirm a tool, wait on
``requires_action``, emit a commitment receipt, or infer an outcome receipt.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from contract import ContractError, TRUST_POLICY_PATH, preflight, sha256_value


REMOTE_ADAPTER_STATUS = "REMOTE_ADAPTER_UNSUPPORTED"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--request", type=Path, required=True, help="typed RunRequest JSON"
    )
    parser.add_argument(
        "--deployment-receipt",
        type=Path,
        required=True,
        help="remote-verified DeploymentReceipt JSON",
    )
    parser.add_argument(
        "--trust-policy",
        type=Path,
        default=TRUST_POLICY_PATH,
        help="ignored local trust-policy JSON containing approved BIP-340 public keys",
    )
    parser.add_argument(
        "--expect-trust-policy-sha256",
        required=True,
        help="operator-reviewed semantic SHA-256 of the ignored local trust policy",
    )
    parser.add_argument(
        "--execute", action="store_true", help="request execution (currently refused)"
    )
    args = parser.parse_args(argv)

    try:
        lock, request, deployment, trust_policy = preflight(
            args.request,
            args.deployment_receipt,
            args.trust_policy,
            args.expect_trust_policy_sha256,
        )
    except ContractError as exc:
        print(f"RUN-PREFLIGHT-ERROR: {exc}", file=sys.stderr)
        return 1

    summary = {
        "status": "preflight_ok",
        "requestId": request["requestId"],
        "requestSha256": sha256_value(request),
        "budgetSha256": sha256_value(request["budget"]),
        "actionPlanSha256": request["actionPlanSha256"],
        "bundleSha256": lock["bundleSha256"],
        "deploymentSha256": sha256_value(deployment),
        "trustPolicySha256": sha256_value(trust_policy),
        "consequential": request["consequential"],
        "operations": request["operations"],
        "remoteCalls": 0,
        "commitmentReceipt": None,
        "outcomeReceipt": None,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    if args.execute:
        print(
            f"{REMOTE_ADAPTER_STATUS}: preflight passed, but calls/tokens/wall-time/"
            "delegations are not yet provider-observable and enforceable; zero API calls made.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
