#!/usr/bin/env python3
"""Offline-first EUB-1 adapters. Credentials never enter serializable state."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse
from urllib.request import Request, urlopen


AUTHORIZED_RUN_CLASSES = {"AUTHORIZED_PILOT", "AUTHORIZED_SCORED"}


class AdapterError(RuntimeError):
    """Safe adapter error whose message contains no credential material."""


class NetworkRefused(AdapterError):
    pass


class AuthorizationRequired(AdapterError):
    pass


class BudgetRefused(AdapterError):
    pass


@dataclass(frozen=True)
class NetworkPolicy:
    allow_network: bool = False
    run_class: str = "OFFLINE_DRY_RUN"
    authorization_ref: str = ""
    cost_limit_usd: float = 0.0

    def enforce(self) -> None:
        if not self.allow_network:
            raise NetworkRefused("network access is disabled; use a recorded response or explicit authorized live policy")
        if self.run_class not in AUTHORIZED_RUN_CLASSES or not self.authorization_ref:
            raise AuthorizationRequired("live access requires an authorized run class and external authorization reference")
        if self.cost_limit_usd <= 0:
            raise BudgetRefused("live access requires a positive cost envelope")


@dataclass(frozen=True)
class AdapterResponse:
    content: str
    resolved_model_id: str
    raw_response_hash: str
    usage: dict[str, int]


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _default_transport(request: Request) -> bytes:
    with urlopen(request, timeout=120) as response:  # nosec: guarded by NetworkPolicy before construction
        return response.read()


class RecordedResponseAdapter:
    name = "recorded"

    def __init__(self, response_path: str | Path):
        self.response_path = Path(response_path)

    def call(self, prompt: str, requested_model_id: str, policy: NetworkPolicy, max_output_tokens: int = 4096) -> AdapterResponse:
        raw = self.response_path.read_bytes()
        return AdapterResponse(
            content=raw.decode("utf-8", errors="replace"),
            resolved_model_id=requested_model_id,
            raw_response_hash=hashlib.sha256(raw).hexdigest(),
            usage={"input_tokens": 0, "output_tokens": 0},
        )


class AnthropicMessagesAdapter:
    name = "anthropic-messages"

    def __init__(self, transport: Callable[[Request], bytes] | None = None):
        self.transport = transport or _default_transport

    def call(self, prompt: str, requested_model_id: str, policy: NetworkPolicy, max_output_tokens: int = 4096) -> AdapterResponse:
        policy.enforce()
        if not isinstance(max_output_tokens, int) or isinstance(max_output_tokens, bool) or max_output_tokens <= 0:
            raise BudgetRefused("max_output_tokens must be a positive integer")
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise AuthorizationRequired("ANTHROPIC_API_KEY is absent from the environment")
        payload = {"model": requested_model_id, "max_tokens": max_output_tokens, "messages": [{"role": "user", "content": prompt}]}
        request = Request(
            "https://api.anthropic.com/v1/messages",
            data=_json_bytes(payload),
            headers={"content-type": "application/json", "anthropic-version": "2023-06-01", "x-api-key": api_key},
            method="POST",
        )
        try:
            raw = self.transport(request)
        except Exception as exc:
            raise AdapterError("Anthropic transport failed without exposing provider details") from None
        try:
            body = json.loads(raw)
            resolved = body["model"]
            blocks = body["content"]
            content = "".join(item.get("text", "") for item in blocks if isinstance(item, dict) and item.get("type") == "text")
            usage = body.get("usage", {})
            normalized_usage = {"input_tokens": int(usage.get("input_tokens", 0)), "output_tokens": int(usage.get("output_tokens", 0))}
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise AdapterError("Anthropic response omitted required content or exact resolved model ID") from exc
        if not isinstance(resolved, str) or not resolved:
            raise AdapterError("Anthropic response omitted the exact resolved model ID")
        if any(amount < 0 for amount in normalized_usage.values()):
            raise AdapterError("Anthropic response reported invalid token usage")
        if normalized_usage["output_tokens"] > max_output_tokens:
            raise BudgetRefused("provider output usage exceeded the declared output-token limit")
        return AdapterResponse(content, resolved, hashlib.sha256(raw).hexdigest(), normalized_usage)


class OpenAICompatibleAdapter:
    name = "openai-compatible"

    def __init__(self, base_url: str, transport: Callable[[Request], bytes] | None = None, allow_keyless_local: bool = False):
        self.base_url = base_url.rstrip("/")
        self.transport = transport or _default_transport
        self.allow_keyless_local = allow_keyless_local

    def call(self, prompt: str, requested_model_id: str, policy: NetworkPolicy, max_output_tokens: int = 4096) -> AdapterResponse:
        policy.enforce()
        if not isinstance(max_output_tokens, int) or isinstance(max_output_tokens, bool) or max_output_tokens <= 0:
            raise BudgetRefused("max_output_tokens must be a positive integer")
        api_key = os.environ.get("OPENAI_API_KEY")
        parsed = urlparse(self.base_url)
        is_local = parsed.hostname in {"127.0.0.1", "::1", "localhost"}
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise AuthorizationRequired("OpenAI-compatible endpoint must be a plain HTTP(S) origin/path without embedded credentials or query data")
        if not is_local and parsed.scheme != "https":
            raise AuthorizationRequired("remote OpenAI-compatible endpoints require HTTPS")
        if not api_key and not (is_local and self.allow_keyless_local):
            raise AuthorizationRequired("OPENAI_API_KEY is absent from the environment")
        headers = {"content-type": "application/json"}
        if api_key and not (is_local and self.allow_keyless_local):
            headers["authorization"] = f"Bearer {api_key}"
        payload = {"model": requested_model_id, "messages": [{"role": "user", "content": prompt}], "temperature": 0, "max_tokens": max_output_tokens}
        request = Request(f"{self.base_url}/chat/completions", data=_json_bytes(payload), headers=headers, method="POST")
        try:
            raw = self.transport(request)
        except Exception:
            raise AdapterError("OpenAI-compatible transport failed without exposing provider details") from None
        try:
            body = json.loads(raw)
            resolved = body["model"]
            content = body["choices"][0]["message"]["content"]
            usage = body.get("usage", {})
            normalized_usage = {"input_tokens": int(usage.get("prompt_tokens", 0)), "output_tokens": int(usage.get("completion_tokens", 0))}
        except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise AdapterError("OpenAI-compatible response omitted required content or exact resolved model ID") from exc
        if not isinstance(resolved, str) or not resolved:
            raise AdapterError("OpenAI-compatible response omitted the exact resolved model ID")
        if any(amount < 0 for amount in normalized_usage.values()):
            raise AdapterError("OpenAI-compatible response reported invalid token usage")
        if normalized_usage["output_tokens"] > max_output_tokens:
            raise BudgetRefused("provider output usage exceeded the declared output-token limit")
        return AdapterResponse(content, resolved, hashlib.sha256(raw).hexdigest(), normalized_usage)
