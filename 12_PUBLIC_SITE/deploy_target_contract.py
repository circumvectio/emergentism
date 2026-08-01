#!/usr/bin/env python3
"""Fail-closed production-target validation for the Vercel deploy wrapper.

The ignored `.vercel/project.json` link is not an independent target pin. A
production invocation therefore also requires two explicitly supplied pins:

    EMERGENTISM_VERCEL_PROJECT_ID_PIN
    EMERGENTISM_VERCEL_ORG_ID_PIN

This checker never prints either value. It performs no network access.
"""

from __future__ import annotations

import argparse
import hmac
import json
import os
import tempfile
from pathlib import Path


PROJECT_PIN_ENV = "EMERGENTISM_VERCEL_PROJECT_ID_PIN"
ORG_PIN_ENV = "EMERGENTISM_VERCEL_ORG_ID_PIN"


def _required_identity(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"invalid Vercel target identity: {label} is missing or malformed")
    return value


def validate_vercel_link(
    link_path: Path,
    project_pin: str | None,
    org_pin: str | None,
) -> None:
    """Require an independently pinned exact match without exposing identities."""
    project_pin = _required_identity(project_pin, PROJECT_PIN_ENV)
    org_pin = _required_identity(org_pin, ORG_PIN_ENV)
    try:
        link = json.loads(link_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid Vercel project linkage: {exc}") from exc
    if not isinstance(link, dict):
        raise ValueError("invalid Vercel project linkage: expected a JSON object")
    project_id = _required_identity(link.get("projectId"), "projectId")
    org_id = _required_identity(link.get("orgId"), "orgId")
    if not (
        hmac.compare_digest(project_id, project_pin)
        and hmac.compare_digest(org_id, org_pin)
    ):
        raise ValueError("Vercel project linkage does not match the explicit production pins")


def self_test() -> None:
    """Exercise pin absence, malformed linkage, mismatch, and exact match."""
    with tempfile.TemporaryDirectory() as tmp:
        link_path = Path(tmp) / "project.json"
        link_path.write_text(
            json.dumps({"projectId": "project-test-pin", "orgId": "org-test-pin"}),
            encoding="utf-8",
        )
        rejected = (
            (None, None),
            ("project-test-pin", None),
            (None, "org-test-pin"),
            ("wrong-project", "org-test-pin"),
            ("project-test-pin", "wrong-org"),
        )
        for project_pin, org_pin in rejected:
            try:
                validate_vercel_link(link_path, project_pin, org_pin)
            except ValueError:
                pass
            else:
                raise AssertionError("Vercel target negative control was accepted")
        validate_vercel_link(link_path, "project-test-pin", "org-test-pin")
        link_path.write_text("{}", encoding="utf-8")
        try:
            validate_vercel_link(link_path, "project-test-pin", "org-test-pin")
        except ValueError:
            pass
        else:
            raise AssertionError("malformed Vercel link negative control was accepted")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vercel-link", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        if args.vercel_link is not None:
            parser.error("--self-test and --vercel-link are mutually exclusive")
        self_test()
        print("DEPLOY TARGET CONTRACT: PASS (Vercel pins fail closed)")
        return 0
    if args.vercel_link is None:
        parser.error("--vercel-link is required")
    try:
        validate_vercel_link(
            args.vercel_link,
            os.environ.get(PROJECT_PIN_ENV),
            os.environ.get(ORG_PIN_ENV),
        )
    except ValueError as exc:
        raise SystemExit(str(exc))
    print("Vercel production target matches both explicit pins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
