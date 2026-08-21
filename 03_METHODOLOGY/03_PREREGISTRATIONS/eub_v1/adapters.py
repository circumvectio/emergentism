#!/usr/bin/env python3
"""Offline-first EUB-1 adapters. Credentials never enter serializable state."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


AUTHORIZED_RUN_CLASSES = {"AUTHORIZED_PILOT", "AUTHORIZED_SCORED"}
CHAT_FRAMING_TOKEN_ALLOWANCE = 1024
MAX_CREDENTIAL_DECODE_DEPTH = 16
MAX_CREDENTIAL_SCAN_CHARS = 1_000_000
MAX_PROVIDER_RESPONSE_BYTES = 16 * 1024 * 1024


def configured_credential_values() -> tuple[str, ...]:
    """Snapshot configured provider credentials without serializing their names."""

    return tuple(
        value
        for name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")
        if (value := os.environ.get(name))
    )


def _credential_variants(value: str) -> set[bytes]:
    variants = {value.encode("utf-8")}
    # Include bounded repeated JSON encodings so malformed outer wrappers
    # cannot hide a credential merely by preventing a top-level JSON parse.
    frontier = {value}
    total = len(value)
    for _depth in range(MAX_CREDENTIAL_DECODE_DEPTH + 1):
        next_frontier: set[str] = set()
        for item in frontier:
            for ensure_ascii in (False, True):
                encoded = json.dumps(item, ensure_ascii=ensure_ascii)
                variants.add(encoded.encode("utf-8"))
                variants.add(encoded.replace("/", r"\/").encode("utf-8"))
                next_frontier.add(encoded)
                total += len(encoded)
                if total >= MAX_CREDENTIAL_SCAN_CHARS:
                    return {variant for variant in variants if variant}
        frontier = next_frontier
    return {variant for variant in variants if variant}


def contains_credential_material(
    raw: bytes | str,
    credential_values: tuple[str, ...] | None = None,
) -> bool:
    """Detect literal, JSON-escaped, and decoded credential occurrences."""

    supplied = credential_values or ()
    credentials = tuple(dict.fromkeys((*supplied, *configured_credential_values())))
    if not credentials:
        return False
    raw_bytes = raw.encode("utf-8") if isinstance(raw, str) else bytes(raw)
    if any(variant in raw_bytes for value in credentials for variant in _credential_variants(value)):
        return True
    try:
        parsed = json.loads(raw_bytes)
    except (UnicodeDecodeError, ValueError, TypeError, json.JSONDecodeError):
        return False

    # Provider wrappers can nest JSON strings repeatedly. Walk every decoded
    # string iteratively and fail closed if either the depth or work ceiling is
    # reached while more JSON remains. This avoids a fixed-depth credential
    # bypass without allowing adversarial output to consume unbounded work.
    stack: list[tuple[Any, int]] = [(parsed, 0)]
    remaining_chars = MAX_CREDENTIAL_SCAN_CHARS
    while stack:
        value, depth = stack.pop()
        if isinstance(value, str):
            remaining_chars -= len(value)
            if remaining_chars < 0:
                return True
            if any(credential in value for credential in credentials):
                return True
            try:
                nested = json.loads(value)
            except (UnicodeDecodeError, ValueError, TypeError, json.JSONDecodeError):
                continue
            if nested == value:
                continue
            if depth >= MAX_CREDENTIAL_DECODE_DEPTH:
                return True
            stack.append((nested, depth + 1))
        elif isinstance(value, dict):
            stack.extend((key, depth) for key in value)
            stack.extend((item, depth) for item in value.values())
        elif isinstance(value, list):
            stack.extend((item, depth) for item in value)
    return False


def _request_contains_credential(
    prompt: str,
    requested_model_id: str,
    policy: "NetworkPolicy",
    endpoint: str,
    credential_values: tuple[str, ...],
) -> bool:
    request_metadata = {
        "prompt": prompt,
        "requested_model_id": requested_model_id,
        "endpoint": endpoint,
        "run_class": policy.run_class,
        "authorization_ref": policy.authorization_ref,
        "cost_basis_ref": policy.cost_basis_ref,
    }
    return contains_credential_material(
        json.dumps(request_metadata, sort_keys=True, ensure_ascii=False),
        credential_values,
    )


def conservative_prompt_token_bound(prompt: str) -> int:
    """Upper-bound content tokens by UTF-8 bytes plus fixed chat framing.

    The bound deliberately assumes no content token can encode less than one
    input byte and reserves a 1,024-token allowance for the single-message chat
    template. Adapters refuse before transport when this bound exceeds the
    declared input-token cap.
    """

    if not isinstance(prompt, str):
        raise BudgetRefused("prompt must be a string")
    return len(prompt.encode("utf-8")) + CHAT_FRAMING_TOKEN_ALLOWANCE


class AdapterError(RuntimeError):
    """Safe adapter error whose message contains no credential material."""

    def __init__(
        self,
        message: str,
        *,
        safe_raw_response: bytes | None = None,
        result_state: str | None = None,
        credential_values: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(message)
        self.safe_raw_output: str | None = None
        self.safe_raw_response_hash: str | None = None
        self.result_state = result_state
        if safe_raw_response is not None:
            if contains_credential_material(safe_raw_response, credential_values):
                raise CredentialMaterialDetected(
                    "provider response contained credential material; bytes and their hash were withheld"
                )
            self.safe_raw_output = safe_raw_response.decode("utf-8", errors="replace")
            self.safe_raw_response_hash = hashlib.sha256(safe_raw_response).hexdigest()


class NetworkRefused(AdapterError):
    pass


class AuthorizationRequired(AdapterError):
    pass


class BudgetRefused(AdapterError):
    pass


class CredentialMaterialDetected(AdapterError):
    """Provider bytes contained a configured credential and must not be hashed."""


def _decimal(value: float | int | None, label: str) -> Decimal:
    if value is None or isinstance(value, bool):
        raise BudgetRefused(f"{label} must be explicitly declared")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise BudgetRefused(f"{label} must be a finite non-negative number") from None
    if not result.is_finite() or result < 0:
        raise BudgetRefused(f"{label} must be a finite non-negative number")
    return result


@dataclass
class NetworkPolicy:
    allow_network: bool = False
    run_class: str = "OFFLINE_DRY_RUN"
    authorization_ref: str = ""
    cost_limit_usd: float = 0.0
    input_cost_per_million_usd: float | None = None
    output_cost_per_million_usd: float | None = None
    cost_basis_ref: str = ""
    _reserved_cost_usd: Decimal = field(default_factory=lambda: Decimal("0"), init=False, repr=False)

    def enforce(self) -> None:
        if not self.allow_network:
            raise NetworkRefused("network access is disabled; use a recorded response or explicit authorized live policy")
        if self.run_class not in AUTHORIZED_RUN_CLASSES or not self.authorization_ref:
            raise AuthorizationRequired("live access requires an authorized run class and external authorization reference")
        if _decimal(self.cost_limit_usd, "cost limit") <= 0:
            raise BudgetRefused("live access requires a positive cost envelope")
        _decimal(self.input_cost_per_million_usd, "input cost rate")
        _decimal(self.output_cost_per_million_usd, "output cost rate")
        if not isinstance(self.cost_basis_ref, str) or not self.cost_basis_ref.strip():
            raise BudgetRefused("live access requires an explicit cost-basis reference")

    @property
    def reserved_cost_usd(self) -> float:
        return float(self._reserved_cost_usd)

    def reserve_call(self, max_input_tokens: int, max_output_tokens: int) -> float:
        """Reserve the worst-case declared token cost before any transport call.

        Reservations are intentionally not released after a cheaper response or a
        transport failure. This makes the five-call rail conservative and keeps a
        later sitting from silently reusing budget already exposed to a provider.
        """

        self.enforce()
        for value, label in ((max_input_tokens, "max_input_tokens"), (max_output_tokens, "max_output_tokens")):
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise BudgetRefused(f"{label} must be a positive integer")
        input_rate = _decimal(self.input_cost_per_million_usd, "input cost rate")
        output_rate = _decimal(self.output_cost_per_million_usd, "output cost rate")
        reservation = (
            Decimal(max_input_tokens) * input_rate
            + Decimal(max_output_tokens) * output_rate
        ) / Decimal("1000000")
        limit = _decimal(self.cost_limit_usd, "cost limit")
        if self._reserved_cost_usd + reservation > limit:
            raise BudgetRefused("the next call would exceed the cumulative declared cost envelope")
        self._reserved_cost_usd += reservation
        return float(reservation)

    def estimate_usage_cost(self, usage: dict[str, int]) -> float:
        input_rate = _decimal(self.input_cost_per_million_usd, "input cost rate")
        output_rate = _decimal(self.output_cost_per_million_usd, "output cost rate")
        estimate = (
            Decimal(usage.get("input_tokens", 0)) * input_rate
            + Decimal(usage.get("output_tokens", 0)) * output_rate
        ) / Decimal("1000000")
        return float(estimate)


@dataclass(frozen=True)
class AdapterResponse:
    content: str
    resolved_model_id: str
    raw_response_hash: str
    usage: dict[str, int]
    estimated_cost_usd: float = 0.0
    reserved_cost_usd: float = 0.0
    raw_response_text: str | None = None


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _strict_json_loads(value: bytes | str) -> Any:
    return json.loads(
        value,
        parse_constant=lambda constant: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant is forbidden: {constant}")
        ),
    )


class _RefuseRedirects(HTTPRedirectHandler):
    """Never forward credential-bearing provider requests to another URL."""

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request | None:
        raise NetworkRefused("provider redirects are refused before credentials can be forwarded")


def _default_transport(request: Request) -> bytes:
    opener = build_opener(_RefuseRedirects())
    with opener.open(request, timeout=120) as response:  # nosec: guarded by NetworkPolicy before construction
        raw = response.read(MAX_PROVIDER_RESPONSE_BYTES + 1)
    if len(raw) > MAX_PROVIDER_RESPONSE_BYTES:
        raise AdapterError("provider response exceeded the bounded response-size limit")
    return raw


class RecordedResponseAdapter:
    name = "recorded"

    def __init__(self, response_path: str | Path):
        self.response_path = Path(response_path)

    def call(self, prompt: str, requested_model_id: str, policy: NetworkPolicy, max_output_tokens: int = 4096, max_input_tokens: int = 16384) -> AdapterResponse:
        credential_values = configured_credential_values()
        if _request_contains_credential(
            prompt, requested_model_id, policy, "recorded-response", credential_values
        ):
            raise CredentialMaterialDetected(
                "request metadata contained credential material; request and its hashes were withheld"
            )
        raw = self.response_path.read_bytes()
        if contains_credential_material(raw, credential_values):
            raise CredentialMaterialDetected("recorded response contained credential material; bytes and their hash were withheld")
        return AdapterResponse(
            content=raw.decode("utf-8", errors="replace"),
            resolved_model_id=requested_model_id,
            raw_response_hash=hashlib.sha256(raw).hexdigest(),
            usage={"input_tokens": 0, "output_tokens": 0},
            raw_response_text=raw.decode("utf-8", errors="replace"),
        )


class AnthropicMessagesAdapter:
    name = "anthropic-messages"

    def __init__(self, transport: Callable[[Request], bytes] | None = None):
        self.transport = transport or _default_transport

    def call(self, prompt: str, requested_model_id: str, policy: NetworkPolicy, max_output_tokens: int = 4096, max_input_tokens: int = 16384) -> AdapterResponse:
        policy.enforce()
        if not isinstance(max_output_tokens, int) or isinstance(max_output_tokens, bool) or max_output_tokens <= 0:
            raise BudgetRefused("max_output_tokens must be a positive integer")
        credential_snapshot = {
            name: value
            for name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")
            if (value := os.environ.get(name))
        }
        credential_values = tuple(credential_snapshot.values())
        api_key = credential_snapshot.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise AuthorizationRequired("ANTHROPIC_API_KEY is absent from the environment")
        if _request_contains_credential(
            prompt,
            requested_model_id,
            policy,
            "https://api.anthropic.com/v1/messages",
            credential_values,
        ):
            raise CredentialMaterialDetected(
                "request metadata contained credential material; request and its hashes were withheld"
            )
        input_bound = conservative_prompt_token_bound(prompt)
        if input_bound > max_input_tokens:
            raise BudgetRefused("prompt exceeds the conservative declared input-token bound")
        reservation = policy.reserve_call(max_input_tokens, max_output_tokens)
        payload = {"model": requested_model_id, "max_tokens": max_output_tokens, "messages": [{"role": "user", "content": prompt}]}
        request = Request(
            "https://api.anthropic.com/v1/messages",
            data=_json_bytes(payload),
            headers={"content-type": "application/json", "anthropic-version": "2023-06-01", "x-api-key": api_key},
            method="POST",
        )
        try:
            raw = self.transport(request)
        except NetworkRefused:
            raise
        except Exception:
            raise AdapterError("Anthropic transport failed without exposing provider details") from None
        if not isinstance(raw, (bytes, bytearray)):
            raise AdapterError(
                "Anthropic transport returned a non-byte response",
                result_state="INVALID_OUTPUT",
            )
        raw = bytes(raw)
        if contains_credential_material(raw, credential_values):
            raise CredentialMaterialDetected("Anthropic response contained credential material; bytes and their hash were withheld")
        try:
            body = _strict_json_loads(raw)
            if not isinstance(body, dict):
                raise TypeError
            resolved = body["model"]
            blocks = body["content"]
            if not isinstance(blocks, list):
                raise TypeError
            parts: list[str] = []
            for item in blocks:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get("text")
                    if not isinstance(text, str):
                        raise TypeError
                    parts.append(text)
            content = "".join(parts)
            usage = body["usage"]
            if not isinstance(usage, dict):
                raise TypeError
            input_tokens = usage["input_tokens"]
            output_tokens = usage["output_tokens"]
            if any(
                not isinstance(amount, int)
                or isinstance(amount, bool)
                or amount < 0
                for amount in (input_tokens, output_tokens)
            ):
                raise TypeError
            normalized_usage = {"input_tokens": input_tokens, "output_tokens": output_tokens}
        except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
            raise AdapterError(
                "Anthropic response omitted required content or exact resolved model ID",
                safe_raw_response=raw,
                result_state="INVALID_OUTPUT",
                credential_values=credential_values,
            ) from None
        if not isinstance(resolved, str) or not resolved:
            raise AdapterError(
                "Anthropic response omitted the exact resolved model ID",
                safe_raw_response=raw,
                result_state="INVALID_OUTPUT",
                credential_values=credential_values,
            )
        if any(amount < 0 for amount in normalized_usage.values()):
            raise AdapterError(
                "Anthropic response reported invalid token usage",
                safe_raw_response=raw,
                result_state="INVALID_OUTPUT",
                credential_values=credential_values,
            )
        if normalized_usage["input_tokens"] > max_input_tokens:
            raise BudgetRefused(
                "provider input usage exceeded the declared input-token limit",
                safe_raw_response=raw,
                result_state="BUDGET_REFUSED",
                credential_values=credential_values,
            )
        if normalized_usage["output_tokens"] > max_output_tokens:
            raise BudgetRefused(
                "provider output usage exceeded the declared output-token limit",
                safe_raw_response=raw,
                result_state="BUDGET_REFUSED",
                credential_values=credential_values,
            )
        return AdapterResponse(
            content,
            resolved,
            hashlib.sha256(raw).hexdigest(),
            normalized_usage,
            policy.estimate_usage_cost(normalized_usage),
            reservation,
            raw.decode("utf-8", errors="replace"),
        )


class OpenAICompatibleAdapter:
    name = "openai-compatible"

    def __init__(self, base_url: str, transport: Callable[[Request], bytes] | None = None, allow_keyless_local: bool = False):
        self.base_url = base_url.rstrip("/")
        self.transport = transport or _default_transport
        self.allow_keyless_local = allow_keyless_local

    def call(self, prompt: str, requested_model_id: str, policy: NetworkPolicy, max_output_tokens: int = 4096, max_input_tokens: int = 16384) -> AdapterResponse:
        policy.enforce()
        if not isinstance(max_output_tokens, int) or isinstance(max_output_tokens, bool) or max_output_tokens <= 0:
            raise BudgetRefused("max_output_tokens must be a positive integer")
        credential_snapshot = {
            name: value
            for name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")
            if (value := os.environ.get(name))
        }
        credential_values = tuple(credential_snapshot.values())
        api_key = credential_snapshot.get("OPENAI_API_KEY")
        parsed = urlparse(self.base_url)
        is_local = parsed.hostname in {"127.0.0.1", "::1", "localhost"}
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise AuthorizationRequired("OpenAI-compatible endpoint must be a plain HTTP(S) origin/path without embedded credentials or query data")
        if not is_local and parsed.scheme != "https":
            raise AuthorizationRequired("remote OpenAI-compatible endpoints require HTTPS")
        if not api_key and not (is_local and self.allow_keyless_local):
            raise AuthorizationRequired("OPENAI_API_KEY is absent from the environment")
        if _request_contains_credential(
            prompt, requested_model_id, policy, self.base_url, credential_values
        ):
            raise CredentialMaterialDetected(
                "request metadata contained credential material; request and its hashes were withheld"
            )
        input_bound = conservative_prompt_token_bound(prompt)
        if input_bound > max_input_tokens:
            raise BudgetRefused("prompt exceeds the conservative declared input-token bound")
        reservation = policy.reserve_call(max_input_tokens, max_output_tokens)
        headers = {"content-type": "application/json"}
        if api_key and not (is_local and self.allow_keyless_local):
            headers["authorization"] = f"Bearer {api_key}"
        payload = {"model": requested_model_id, "messages": [{"role": "user", "content": prompt}], "temperature": 0, "max_tokens": max_output_tokens}
        request = Request(f"{self.base_url}/chat/completions", data=_json_bytes(payload), headers=headers, method="POST")
        try:
            raw = self.transport(request)
        except NetworkRefused:
            raise
        except Exception:
            raise AdapterError("OpenAI-compatible transport failed without exposing provider details") from None
        if not isinstance(raw, (bytes, bytearray)):
            raise AdapterError(
                "OpenAI-compatible transport returned a non-byte response",
                result_state="INVALID_OUTPUT",
            )
        raw = bytes(raw)
        if contains_credential_material(raw, credential_values):
            raise CredentialMaterialDetected("OpenAI-compatible response contained credential material; bytes and their hash were withheld")
        try:
            body = _strict_json_loads(raw)
            if not isinstance(body, dict):
                raise TypeError
            resolved = body["model"]
            choices = body["choices"]
            if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
                raise TypeError
            message = choices[0].get("message")
            if not isinstance(message, dict):
                raise TypeError
            content = message.get("content")
            if not isinstance(content, str):
                raise TypeError
            usage = body["usage"]
            if not isinstance(usage, dict):
                raise TypeError
            input_tokens = usage["prompt_tokens"]
            output_tokens = usage["completion_tokens"]
            if any(
                not isinstance(amount, int)
                or isinstance(amount, bool)
                or amount < 0
                for amount in (input_tokens, output_tokens)
            ):
                raise TypeError
            normalized_usage = {"input_tokens": input_tokens, "output_tokens": output_tokens}
        except (KeyError, IndexError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
            raise AdapterError(
                "OpenAI-compatible response omitted required content or exact resolved model ID",
                safe_raw_response=raw,
                result_state="INVALID_OUTPUT",
                credential_values=credential_values,
            ) from None
        if not isinstance(resolved, str) or not resolved:
            raise AdapterError(
                "OpenAI-compatible response omitted the exact resolved model ID",
                safe_raw_response=raw,
                result_state="INVALID_OUTPUT",
                credential_values=credential_values,
            )
        if any(amount < 0 for amount in normalized_usage.values()):
            raise AdapterError(
                "OpenAI-compatible response reported invalid token usage",
                safe_raw_response=raw,
                result_state="INVALID_OUTPUT",
                credential_values=credential_values,
            )
        if normalized_usage["input_tokens"] > max_input_tokens:
            raise BudgetRefused(
                "provider input usage exceeded the declared input-token limit",
                safe_raw_response=raw,
                result_state="BUDGET_REFUSED",
                credential_values=credential_values,
            )
        if normalized_usage["output_tokens"] > max_output_tokens:
            raise BudgetRefused(
                "provider output usage exceeded the declared output-token limit",
                safe_raw_response=raw,
                result_state="BUDGET_REFUSED",
                credential_values=credential_values,
            )
        return AdapterResponse(
            content,
            resolved,
            hashlib.sha256(raw).hexdigest(),
            normalized_usage,
            policy.estimate_usage_cost(normalized_usage),
            reservation,
            raw.decode("utf-8", errors="replace"),
        )
