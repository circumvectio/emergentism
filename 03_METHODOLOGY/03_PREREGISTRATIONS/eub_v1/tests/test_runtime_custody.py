#!/usr/bin/env python3
"""Offline regression tests for runtime cost and failure-artifact custody."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from adapters import (  # noqa: E402
    AdapterError,
    AdapterResponse,
    AnthropicMessagesAdapter,
    BudgetRefused,
    conservative_prompt_token_bound,
    contains_credential_material,
    CredentialMaterialDetected,
    NetworkPolicy,
    NetworkRefused,
    OpenAICompatibleAdapter,
    _RefuseRedirects,
)
from custodian import prepare_held_out_fixture  # noqa: E402
from eub_core import (  # noqa: E402
    SITTING_ORDER,
    build_recorded_trial,
    generate_fixture,
    load_json,
    sha256_value,
    validate_run_bundle,
    write_json,
)
import run_eub  # noqa: E402


ACCOUNT_PATH = HERE / "recorded_responses" / "dasein_account_dev.json"


def invoke(*arguments: object) -> tuple[int, str, str]:
    """Invoke the CLI in-process so transports can be proven offline."""

    args = run_eub.build_parser().parse_args([str(value) for value in arguments])
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        result = int(args.func(args))
    return result, stdout.getvalue(), stderr.getvalue()


class ExclusiveOutputCustodyTests(unittest.TestCase):
    def test_run_refuses_existing_output_before_reading_or_calling(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "existing-run.json"
            output.write_text("owner evidence\n", encoding="utf-8")
            missing_response = Path(temp) / "must-not-be-read.json"

            result, _stdout, stderr = invoke(
                "run",
                "--dry-run",
                "--recorded-response",
                missing_response,
                "--out",
                output,
            )

            self.assertEqual(result, 2)
            self.assertIn("output path already exists and was preserved", stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "owner evidence\n")

    def test_exclusive_writer_closes_the_preflight_race(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "once.json"
            run_eub._write_json_exclusive(output, {"owner": "first"})
            with self.assertRaises(FileExistsError):
                run_eub._write_json_exclusive(output, {"owner": "second"})
            self.assertEqual(load_json(output), {"owner": "first"})

    def test_failed_publish_never_exposes_a_partial_final_target(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "must-remain-absent.json"
            with patch.object(run_eub.os, "link", side_effect=OSError("simulated interruption")):
                with self.assertRaises(OSError):
                    run_eub._write_json_exclusive(output, {"complete": True})
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(temp).glob(".*.pending-*")), [])


class FailureBundleCustodyTests(unittest.TestCase):
    def test_partial_sittings_and_failed_raw_hash_survive_malformed_second_sitting(self):
        run_id = "runtime-partial-custody"
        staged = build_recorded_trial(load_json(ACCOUNT_PATH), run_id)
        malformed = "{malformed-attack"
        calls: list[str] = []

        class PartialThenMalformedAdapter:
            def __init__(self, *_args: object, **_kwargs: object):
                pass

            def call(
                self,
                prompt: str,
                requested_model_id: str,
                policy: NetworkPolicy,
                max_output_tokens: int,
                max_input_tokens: int,
            ) -> AdapterResponse:
                reservation = policy.reserve_call(max_input_tokens, max_output_tokens)
                content = (
                    json.dumps(staged[0], sort_keys=True, ensure_ascii=False)
                    if not calls
                    else malformed
                )
                calls.append(prompt)
                raw = content.encode("utf-8")
                usage = {"input_tokens": len(calls) + 1, "output_tokens": len(calls) + 2}
                return AdapterResponse(
                    content=content,
                    resolved_model_id=requested_model_id,
                    raw_response_hash=hashlib.sha256(raw).hexdigest(),
                    usage=usage,
                    estimated_cost_usd=policy.estimate_usage_cost(usage),
                    reserved_cost_usd=reservation,
                )

        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "partial-run.json"
            with patch.object(run_eub, "OpenAICompatibleAdapter", PartialThenMalformedAdapter):
                result, _stdout, stderr = invoke(
                    "run",
                    "--adapter",
                    "openai-compatible",
                    "--allow-network",
                    "--run-class",
                    "AUTHORIZED_PILOT",
                    "--authorization-ref",
                    "TEST-ONLY-NO-TRANSPORT",
                    "--cost-limit-usd",
                    "1",
                    "--input-cost-per-million-usd",
                    "1",
                    "--output-cost-per-million-usd",
                    "1",
                    "--cost-basis-ref",
                    "TEST-FIXED-RATES",
                    "--max-input-tokens",
                    "100000",
                    "--max-output-tokens",
                    "10000",
                    "--model",
                    "test-resolved-model",
                    "--run-id",
                    run_id,
                    "--out",
                    output,
                )
            bundle = load_json(output)

        self.assertEqual(result, 2, stderr)
        self.assertEqual(len(calls), 2)
        self.assertEqual(validate_run_bundle(bundle), [])
        self.assertEqual(
            [row["sitting_id"] for row in bundle["trial"]["sittings"]],
            ["UNFOLD"],
        )
        self.assertEqual(
            bundle["trial"]["sittings"][0]["public_account"], staged[0]
        )
        failure = bundle["trial"]["failure"]
        self.assertEqual(failure["sitting_id"], "ATTACK")
        self.assertEqual(failure["result_state"], "INVALID_OUTPUT")
        self.assertEqual(failure["raw_output_disposition"], "PRESERVED")
        self.assertEqual(failure["raw_output"], malformed)
        malformed_hash = hashlib.sha256(malformed.encode("utf-8")).hexdigest()
        self.assertEqual(failure["output_commitment_sha256"], malformed_hash)
        self.assertEqual(
            bundle["receipt"]["sitting_output_hashes"]["ATTACK"], malformed_hash
        )
        self.assertEqual(
            set(bundle["receipt"]["prompt_hashes"]), {"UNFOLD", "ATTACK"}
        )
        self.assertEqual(set(bundle["receipt"]["snapshot_hashes"]), {"UNFOLD"})
        self.assertEqual(bundle["usage"]["input_tokens"], 5)
        self.assertEqual(bundle["usage"]["output_tokens"], 7)
        self.assertGreater(bundle["usage"]["reserved_cost_usd"], 0)

        zeroed_usage = deepcopy(bundle)
        zeroed_usage["usage"] = {
            "calls": [],
            "input_tokens": 0,
            "output_tokens": 0,
            "estimated_cost_usd": 0.0,
            "reserved_cost_usd": 0.0,
        }
        zeroed_usage["receipt"]["usage_hash"] = sha256_value(zeroed_usage["usage"])
        zeroed_usage["receipt"]["trial_transcript_hash"] = sha256_value(
            {
                "snapshot_hashes": zeroed_usage["receipt"]["snapshot_hashes"],
                "raw_output_hashes": zeroed_usage["receipt"]["sitting_output_hashes"],
                "prompt_hashes": zeroed_usage["receipt"]["prompt_hashes"],
                "usage_hash": zeroed_usage["receipt"]["usage_hash"],
                "failure_hash": zeroed_usage["receipt"]["failure_hash"],
            }
        )
        self.assertTrue(
            any("live run usage" in row for row in validate_run_bundle(zeroed_usage))
        )

        forged_cost = deepcopy(bundle)
        forged_cost["usage"]["calls"][0]["reserved_cost_usd"] += 0.01
        forged_cost["usage"]["reserved_cost_usd"] = sum(
            row["reserved_cost_usd"] for row in forged_cost["usage"]["calls"]
        )
        forged_cost["receipt"]["usage_hash"] = sha256_value(forged_cost["usage"])
        forged_cost["receipt"]["trial_transcript_hash"] = sha256_value(
            {
                "snapshot_hashes": forged_cost["receipt"]["snapshot_hashes"],
                "raw_output_hashes": forged_cost["receipt"]["sitting_output_hashes"],
                "prompt_hashes": forged_cost["receipt"]["prompt_hashes"],
                "usage_hash": forged_cost["receipt"]["usage_hash"],
                "failure_hash": forged_cost["receipt"]["failure_hash"],
            }
        )
        self.assertTrue(
            any("reserved_cost_usd" in row for row in validate_run_bundle(forged_cost))
        )

        changed_diagnostics = deepcopy(bundle)
        changed_diagnostics["trial"]["failure"]["structured_errors"] = ["fabricated"]
        self.assertTrue(validate_run_bundle(changed_diagnostics))

        changed_text = deepcopy(bundle)
        changed_text["trial"]["failure"]["raw_output"] = "different malformed text"
        self.assertTrue(
            any("preserved UTF-8 text" in row for row in validate_run_bundle(changed_text))
        )
        changed_completed_prompt = deepcopy(bundle)
        changed_completed_prompt["trial"]["sittings"][0]["prompt_hash"] = "0" * 64
        self.assertTrue(
            any("changed a completed sitting" in row for row in validate_run_bundle(changed_completed_prompt))
        )

    def test_credential_bearing_malformed_output_gets_descriptor_not_raw_hash(self):
        secret = "runtime-custody-secret-73b5"
        credential_bytes = (
            b'{"schema_id":"DaseinAccount.v1","unfinished":"'
            + secret.encode("utf-8")
        )
        raw_secret_hash = hashlib.sha256(credential_bytes).hexdigest()

        with tempfile.TemporaryDirectory() as temp:
            recorded = Path(temp) / "credential-bearing-malformed.json"
            recorded.write_bytes(credential_bytes)
            output = Path(temp) / "redacted-failure.json"
            with patch.dict(os.environ, {"OPENAI_API_KEY": secret}, clear=False):
                result, _stdout, stderr = invoke(
                    "run",
                    "--dry-run",
                    "--recorded-response",
                    recorded,
                    "--run-id",
                    "runtime-redacted-custody",
                    "--out",
                    output,
                )
            bundle = load_json(output)

        self.assertEqual(result, 2, stderr)
        self.assertEqual(validate_run_bundle(bundle), [])
        serialized = json.dumps(bundle, sort_keys=True, ensure_ascii=False)
        self.assertNotIn(secret, serialized)
        self.assertNotIn(raw_secret_hash, serialized)
        failure = bundle["trial"]["failure"]
        self.assertEqual(failure["result_state"], "CONTAMINATED")
        self.assertEqual(
            failure["raw_output_disposition"], "WITHHELD_CREDENTIAL_MATCH"
        )
        self.assertEqual(
            failure["output_commitment_kind"], "REDACTION_DESCRIPTOR_SHA256"
        )
        self.assertIsNone(failure["raw_output"])
        self.assertEqual(
            bundle["receipt"]["sitting_output_hashes"]["UNFOLD"],
            failure["output_commitment_sha256"],
        )
        self.assertNotEqual(failure["output_commitment_sha256"], raw_secret_hash)

        changed_descriptor = deepcopy(bundle)
        changed_descriptor["trial"]["failure"]["output_commitment_sha256"] = "0" * 64
        self.assertTrue(
            any("typed descriptor" in row for row in validate_run_bundle(changed_descriptor))
        )

    def test_common_pre_call_refusals_emit_valid_failure_bundles(self):
        cases = (
            ("default-live-recorded", ()),
            (
                "network-disabled-openai",
                ("--adapter", "openai-compatible"),
            ),
            (
                "missing-live-rates",
                (
                    "--adapter", "openai-compatible",
                    "--allow-network",
                    "--run-class", "AUTHORIZED_PILOT",
                    "--authorization-ref", "TEST-ONLY-NO-TRANSPORT",
                    "--cost-limit-usd", "1",
                ),
            ),
        )
        for label, arguments in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / f"{label}.json"
                result, _stdout, stderr = invoke(
                    "run", *arguments, "--run-id", label, "--out", output
                )
                self.assertEqual(result, 2, stderr)
                bundle = load_json(output)
                self.assertEqual(validate_run_bundle(bundle), [])
                self.assertIn(
                    bundle["trial"]["failure"]["result_state"],
                    {"NETWORK_REFUSED", "BUDGET_REFUSED"},
                )

                no_output = bundle["trial"]["failure"]
                if no_output["raw_output_disposition"] == "NO_PROVIDER_OUTPUT":
                    tampered = deepcopy(bundle)
                    tampered["trial"]["failure"]["output_commitment_sha256"] = "f" * 64
                    self.assertTrue(
                        any("typed descriptor" in row for row in validate_run_bundle(tampered))
                    )

    def test_valid_json_with_invalid_account_shape_is_preserved_and_unscored(self):
        with tempfile.TemporaryDirectory() as temp:
            recorded = Path(temp) / "wrong-shape.json"
            recorded.write_text("{}", encoding="utf-8")
            output = Path(temp) / "wrong-shape-run.json"
            result, _stdout, stderr = invoke(
                "run",
                "--dry-run",
                "--recorded-response",
                recorded,
                "--run-id",
                "runtime-wrong-shape",
                "--out",
                output,
            )
            bundle = load_json(output)

        self.assertEqual(result, 2, stderr)
        self.assertEqual(validate_run_bundle(bundle), [])
        self.assertEqual(bundle["trial"]["failure"]["result_state"], "INVALID_OUTPUT")
        self.assertEqual(bundle["trial"]["failure"]["raw_output"], "{}")

        inflated = deepcopy(bundle)
        inflated["receipt"]["score_vector"]["type_integrity"] = 4.0
        inflated["receipt"]["score_details"]["type_integrity"]["applicability"] = "APPLICABLE"
        errors = validate_run_bundle(inflated)
        self.assertTrue(any("non-scored receipt" in row for row in errors), errors)

        scored_failure = deepcopy(bundle)
        scored_failure["trial"]["failure"]["result_state"] = "SCORED_DEV"
        scored_failure["receipt"]["result_state"] = "SCORED_DEV"
        scored_failure["receipt"]["score_vector"]["type_integrity"] = 4.0
        scored_failure["receipt"]["score_details"]["type_integrity"]["applicability"] = "APPLICABLE"
        errors = validate_run_bundle(scored_failure)
        self.assertTrue(any("cannot carry a scored" in row for row in errors), errors)

    def test_provider_wrapper_shape_failures_write_valid_exact_custody_artifacts(self):
        cases = {
            "content-object": json.dumps(
                {
                    "model": "fixed-model-sha",
                    "choices": [{"message": {"content": {"not": "text"}}}],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1},
                },
                sort_keys=True,
            ).encode("utf-8"),
            "usage-list": json.dumps(
                {
                    "model": "fixed-model-sha",
                    "choices": [{"message": {"content": "{}"}}],
                    "usage": [],
                },
                sort_keys=True,
            ).encode("utf-8"),
            "non-utf8": b"\xffnot-json",
        }
        for label, raw in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / f"{label}.json"

                def factory(*_args: object, payload: bytes = raw, **_kwargs: object) -> OpenAICompatibleAdapter:
                    return OpenAICompatibleAdapter(
                        "https://example.invalid/v1",
                        transport=lambda _request: payload,
                    )

                with (
                    patch.object(run_eub, "OpenAICompatibleAdapter", factory),
                    patch.dict(os.environ, {"OPENAI_API_KEY": "runtime-shape-key"}, clear=False),
                ):
                    result, _stdout, stderr = invoke(
                        "run",
                        "--adapter", "openai-compatible",
                        "--allow-network",
                        "--run-class", "AUTHORIZED_PILOT",
                        "--authorization-ref", "TEST-ONLY-NO-TRANSPORT",
                        "--cost-limit-usd", "1",
                        "--input-cost-per-million-usd", "1",
                        "--output-cost-per-million-usd", "1",
                        "--cost-basis-ref", "TEST-FIXED-RATES",
                        "--max-input-tokens", "100000",
                        "--model", "fixed-model-sha",
                        "--run-id", f"runtime-{label}",
                        "--out", output,
                    )
                bundle = load_json(output)

                self.assertEqual(result, 2, stderr)
                self.assertEqual(validate_run_bundle(bundle), [])
                failure = bundle["trial"]["failure"]
                self.assertEqual(failure["result_state"], "INVALID_OUTPUT")
                self.assertEqual(
                    failure["provider_raw_sha256"], hashlib.sha256(raw).hexdigest()
                )
                self.assertEqual(
                    bundle["receipt"]["sitting_output_hashes"]["UNFOLD"],
                    hashlib.sha256(raw).hexdigest(),
                )
                if label == "non-utf8":
                    self.assertNotEqual(
                        failure["provider_raw_sha256"],
                        failure["output_commitment_sha256"],
                    )

    def test_rotated_and_json_escaped_request_key_is_still_withheld(self):
        secret = 'rotating-key-"\\-\né'

        def transport(_request: object) -> bytes:
            os.environ.pop("OPENAI_API_KEY", None)
            return json.dumps(
                {
                    "model": "fixed-model-sha",
                    "choices": [{"message": {"content": json.dumps({"echo": secret})}}],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1},
                },
                ensure_ascii=True,
            ).encode("utf-8")

        policy = NetworkPolicy(
            allow_network=True,
            run_class="AUTHORIZED_PILOT",
            authorization_ref="TEST-ONLY-NO-TRANSPORT",
            cost_limit_usd=1.0,
            input_cost_per_million_usd=1.0,
            output_cost_per_million_usd=1.0,
            cost_basis_ref="TEST-FIXED-RATES",
        )
        adapter = OpenAICompatibleAdapter(
            "https://example.invalid/v1", transport=transport
        )
        with patch.dict(os.environ, {"OPENAI_API_KEY": secret}, clear=False):
            with self.assertRaises(CredentialMaterialDetected):
                adapter.call("prompt", "fixed-model-sha", policy)


class CredentialAndRedirectMembraneTests(unittest.TestCase):
    @staticmethod
    def policy() -> NetworkPolicy:
        return NetworkPolicy(
            allow_network=True,
            run_class="AUTHORIZED_PILOT",
            authorization_ref="TEST-ONLY-NO-TRANSPORT",
            cost_limit_usd=1.0,
            input_cost_per_million_usd=1.0,
            output_cost_per_million_usd=1.0,
            cost_basis_ref="TEST-FIXED-RATES",
        )

    def test_deep_and_malformed_json_credential_encodings_fail_closed(self):
        secret = "sk-audit-0123456789abcdef"
        nested = '"' + "".join(f"\\u{ord(char):04x}" for char in secret) + '"'
        for _index in range(5):
            nested = json.dumps(nested)
        self.assertTrue(contains_credential_material(nested, (secret,)))

        malformed = secret
        for _index in range(6):
            malformed = json.dumps(malformed)
        malformed += "{"
        self.assertTrue(contains_credential_material(malformed, (secret,)))

    def test_prompt_and_model_credentials_are_refused_before_transport(self):
        secret = "sk-prompt-0123456789abcdef"
        seen: list[object] = []
        adapter = OpenAICompatibleAdapter(
            "https://example.invalid/v1",
            transport=lambda request: seen.append(request) or b"{}",
        )
        with patch.dict(os.environ, {"OPENAI_API_KEY": secret}, clear=False):
            for prompt, model in ((f"fixture {secret}", "fixed"), ("safe", secret)):
                with self.assertRaises(CredentialMaterialDetected):
                    adapter.call(
                        prompt,
                        model,
                        self.policy(),
                        max_input_tokens=100000,
                        max_output_tokens=10,
                    )
        self.assertEqual(seen, [])

    def test_redirect_refusal_is_not_downgraded_to_generic_adapter_error(self):
        def redirecting(_request: object) -> bytes:
            raise NetworkRefused("redirect refused")

        openai = OpenAICompatibleAdapter(
            "https://example.invalid/v1", transport=redirecting
        )
        anthropic = AnthropicMessagesAdapter(transport=redirecting)
        with patch.dict(
            os.environ,
            {"OPENAI_API_KEY": "test-openai-key", "ANTHROPIC_API_KEY": "test-anthropic-key"},
            clear=False,
        ):
            with self.assertRaises(NetworkRefused):
                openai.call(
                    "prompt", "fixed", self.policy(),
                    max_input_tokens=100000, max_output_tokens=10,
                )
            with self.assertRaises(NetworkRefused):
                anthropic.call(
                    "prompt", "fixed", self.policy(),
                    max_input_tokens=100000, max_output_tokens=10,
                )

        handler = _RefuseRedirects()
        for code in (301, 302, 303, 307, 308):
            with self.subTest(code=code), self.assertRaises(NetworkRefused):
                handler.redirect_request(None, None, code, "redirect", {}, "https://other.invalid")

    def test_live_adapters_require_exact_nonnegative_usage_fields(self):
        cases = (
            (
                "openai-missing-usage",
                OpenAICompatibleAdapter,
                "OPENAI_API_KEY",
                {
                    "model": "fixed",
                    "choices": [{"message": {"content": "{}"}}],
                },
            ),
            (
                "anthropic-missing-usage",
                AnthropicMessagesAdapter,
                "ANTHROPIC_API_KEY",
                {
                    "model": "fixed",
                    "content": [{"type": "text", "text": "{}"}],
                },
            ),
            (
                "openai-negative-usage",
                OpenAICompatibleAdapter,
                "OPENAI_API_KEY",
                {
                    "model": "fixed",
                    "choices": [{"message": {"content": "{}"}}],
                    "usage": {"prompt_tokens": -1, "completion_tokens": 1},
                },
            ),
            (
                "anthropic-missing-field",
                AnthropicMessagesAdapter,
                "ANTHROPIC_API_KEY",
                {
                    "model": "fixed",
                    "content": [{"type": "text", "text": "{}"}],
                    "usage": {"input_tokens": 1},
                },
            ),
        )
        for label, adapter_type, key_name, body in cases:
            raw = json.dumps(body, sort_keys=True).encode("utf-8")
            if adapter_type is OpenAICompatibleAdapter:
                adapter = adapter_type(
                    "https://example.invalid/v1",
                    transport=lambda _request, payload=raw: payload,
                )
            else:
                adapter = adapter_type(
                    transport=lambda _request, payload=raw: payload,
                )
            with self.subTest(label=label), patch.dict(
                os.environ, {key_name: "test-provider-key"}, clear=False
            ):
                with self.assertRaises(AdapterError) as caught:
                    adapter.call(
                        "prompt",
                        "fixed",
                        self.policy(),
                        max_input_tokens=100000,
                        max_output_tokens=10,
                    )
                self.assertEqual(caught.exception.result_state, "INVALID_OUTPUT")
                self.assertEqual(
                    caught.exception.safe_raw_response_hash,
                    hashlib.sha256(raw).hexdigest(),
                )

    def test_held_out_run_refuses_before_adapter_construction_or_cost(self):
        public, _payload, _commitment = prepare_held_out_fixture(
            generate_fixture(1701),
            fixture_id="runtime-held-out-preflight",
            custody_nonce="ef" * 32,
        )
        with tempfile.TemporaryDirectory() as temp:
            fixture_path = Path(temp) / "held-out.json"
            output = Path(temp) / "held-out-run.json"
            write_json(fixture_path, public)
            constructed: list[bool] = []

            def forbidden_factory(*_args: object, **_kwargs: object) -> object:
                constructed.append(True)
                raise AssertionError("adapter must not be constructed")

            with patch.object(run_eub, "OpenAICompatibleAdapter", forbidden_factory):
                result, _stdout, stderr = invoke(
                    "run",
                    "--fixture", fixture_path,
                    "--adapter", "openai-compatible",
                    "--allow-network",
                    "--run-class", "AUTHORIZED_PILOT",
                    "--authorization-ref", "TEST-ONLY-NO-TRANSPORT",
                    "--cost-limit-usd", "1",
                    "--input-cost-per-million-usd", "1",
                    "--output-cost-per-million-usd", "1",
                    "--cost-basis-ref", "TEST-FIXED-RATES",
                    "--run-id", "held-out-preflight",
                    "--out", output,
                )
            bundle = load_json(output)
        self.assertEqual(result, 2, stderr)
        self.assertEqual(constructed, [])
        self.assertEqual(bundle["receipt"]["result_state"], "CUSTODY_UNAVAILABLE")
        self.assertEqual(bundle["usage"]["calls"], [])
        self.assertEqual(validate_run_bundle(bundle), [])

    def test_score_reports_custody_unavailable_as_nonzero_not_pass(self):
        public, _payload, _commitment = prepare_held_out_fixture(
            generate_fixture(1701),
            fixture_id="runtime-held-out-score",
            custody_nonce="ab" * 32,
        )
        with tempfile.TemporaryDirectory() as temp:
            fixture_path = Path(temp) / "held-out.json"
            output = Path(temp) / "held-out-score.json"
            write_json(fixture_path, public)
            result, stdout, stderr = invoke(
                "score",
                "--fixture", fixture_path,
                "--account", ACCOUNT_PATH,
                "--out", output,
            )
            receipt = load_json(output)
        self.assertEqual(result, 2, stderr)
        self.assertNotIn("PASS", stdout)
        self.assertEqual(receipt["result_state"], "CUSTODY_UNAVAILABLE")
        self.assertTrue(all(value is None for value in receipt["score_vector"].values()))


class CumulativeCostRailTests(unittest.TestCase):
    def test_fifth_call_is_refused_before_transport_when_reservations_reach_cap(self):
        calls: list[object] = []

        def transport(request: object) -> bytes:
            calls.append(request)
            return json.dumps(
                {
                    "model": "fixed-model-sha",
                    "choices": [{"message": {"content": "{}"}}],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1},
                },
                sort_keys=True,
            ).encode("utf-8")

        prompt = "prompt"
        input_bound = conservative_prompt_token_bound(prompt)
        max_output_tokens = 10
        per_call_reservation = (input_bound + max_output_tokens) / 1_000_000
        policy = NetworkPolicy(
            allow_network=True,
            run_class="AUTHORIZED_PILOT",
            authorization_ref="TEST-ONLY-NO-TRANSPORT",
            cost_limit_usd=4 * per_call_reservation,
            input_cost_per_million_usd=1.0,
            output_cost_per_million_usd=1.0,
            cost_basis_ref="TEST-FIXED-RATES",
        )
        adapter = OpenAICompatibleAdapter(
            "https://example.invalid/v1", transport=transport
        )
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            for _index in range(4):
                adapter.call(
                    prompt,
                    "fixed-model-sha",
                    policy,
                    max_output_tokens=max_output_tokens,
                    max_input_tokens=input_bound,
                )
            with self.assertRaises(BudgetRefused):
                adapter.call(
                    prompt,
                    "fixed-model-sha",
                    policy,
                    max_output_tokens=max_output_tokens,
                    max_input_tokens=input_bound,
                )

        self.assertEqual(len(calls), 4)
        self.assertAlmostEqual(policy.reserved_cost_usd, 4 * per_call_reservation)

    def test_live_cost_rates_and_basis_are_explicit_fail_closed_inputs(self):
        calls: list[object] = []
        policy = NetworkPolicy(
            allow_network=True,
            run_class="AUTHORIZED_PILOT",
            authorization_ref="TEST-ONLY-NO-TRANSPORT",
            cost_limit_usd=1.0,
        )
        adapter = OpenAICompatibleAdapter(
            "https://example.invalid/v1", transport=lambda request: calls.append(request)
        )
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            with self.assertRaises(BudgetRefused):
                adapter.call("prompt", "fixed-model-sha", policy)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
