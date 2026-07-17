from __future__ import annotations

import copy
import hashlib
import html
import json
import math
import unicodedata
from dataclasses import dataclass
from html.entities import html5 as _HTML5_ENTITIES
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from .codec import normalize_lf, raw_hash, safe_repo_path, text_hash
from .diagnostics import Issue, KintsugiError


_NARRATIVE_DOMAIN = b"KINTSUGI-NARRATIVE-V1\x00"
_MAX_UINT64 = (1 << 64) - 1
_MAX_JSON_DEPTH = 512
_MAX_JSON_INTEGER_DIGITS = 4096
_RECEIPT_LEXICAL_GRAMMAR_VERSION = "1"
_MAX_RECEIPT_PROJECTION_CHARS = 8192
_MAX_RECEIPT_BRACKET_DEPTH = 128
_MAX_RECEIPT_CONSTRUCT_CHARS = 8192
_KNOWN_ROLES = frozenset({
    "kintsugi-seam",
    "kintsugi-receipt",
    "kintsugi-review",
    "kintsugi-review-findings",
    "kintsugi-public-queue",
})
_STATIC_RECEIPT_LINES = frozenset({
    "# receipt",
    "# synthetic receipt",
})
_CONTROL_SUBJECT_LEXEMES = frozenset({
    "audit", "audits",
    "attestation", "attestations",
    "btj",
    "check", "checker", "checkers", "checks",
    "digest", "digests",
    "gate", "gates",
    "logic",
    "phase", "phases",
    "receipt", "receipts",
    "review", "reviews",
    "reviewer", "reviewers",
    "status", "statuses",
    "validation", "validations",
    "verdict", "verdicts",
})
_AMBIGUOUS_CONTROL_NOUNS = frozenset({
    "artifact", "artifacts",
    "beauty",
    "bundle", "bundles",
    "justice",
    "outcome", "outcomes",
    "package", "packages",
    "target", "targets",
    "truth",
})
_CLOSURE_PREDICATES = frozenset({
    "abandon", "abandoned",
    "accept", "accepted",
    "approve", "approved", "approves",
    "attested", "audited",
    "checked",
    "close", "closed",
    "complete", "completed",
    "draft",
    "fail", "failed", "fails",
    "final", "finalized",
    "freeze", "frozen",
    "greenlit",
    "pass", "passed", "passes",
    "pending",
    "reject", "rejected", "rejects",
    "reviewed",
    "sign", "signed",
    "succeed", "succeeded", "succeeds",
    "validated",
    "verified",
})
_CLOSURE_LINKERS = frozenset({
    "already", "are", "be", "been", "being", "conclusively",
    "can", "clearly", "considered", "could", "definitively", "formally",
    "fully", "had", "has",
    "have", "indisputably", "is", "not", "now", "officially", "reached",
    "remain", "remains", "may", "might", "must", "plainly", "shall",
    "should", "successfully", "unequivocally", "unquestionably", "was",
    "were", "will", "would",
})
_MAX_CLOSURE_LINKERS = 6
_CONTROL_PHRASES = frozenset({
    ("audit", "artifact"),
    ("audit", "outcome"),
    ("audit", "package"),
    ("beauty", "gate"),
    ("justice", "gate"),
    ("review", "artifact"),
    ("review", "outcome"),
    ("review", "package"),
    ("review", "target"),
    ("truth", "gate"),
    ("validation", "artifact"),
    ("validation", "bundle"),
    ("validation", "outcome"),
    ("validation", "package"),
})
_CONTROL_COMPOUNDS = frozenset(
    {left + right for left, right in _CONTROL_PHRASES}
    | {
        "btjreview", "btjreviewerpath", "btjreviewpath",
        "beautygate", "bundlepath", "gatestatus",
        "justicegate", "logicreview", "logicreviewerpath",
        "logicreviewpath", "receiptstatus", "reviewattempt",
        "reviewattemptid", "reviewerpath", "reviewstatus",
        "reviewtarget", "reviewtargetdigest", "truthgate",
        "validationbundle", "validationbundlepath", "validationdigest",
    }
)
_ONE_SIDED_SEAM_STATUSES = frozenset({"CONFIRMED", "HELD_OPEN"})


@dataclass(frozen=True)
class FenceRecord:
    role: str
    opener_start: int
    json_start: int
    json_end: int
    closer_start: int
    end: int
    value: Any
    parsed_ok: bool


@dataclass(frozen=True)
class LedgerPreamble:
    start: int
    end: int
    raw: bytes
    raw_sha256: str


@dataclass(frozen=True)
class LedgerSection:
    id: str
    start: int
    end: int
    raw: bytes
    raw_sha256: str
    prefix: bytes
    suffix: bytes
    narrative_raw_sha256: str
    seam_record: Any
    seam_projection: Any


@dataclass(frozen=True)
class LedgerSynchronization:
    preamble: LedgerPreamble
    sections: tuple[LedgerSection, ...]
    issues: tuple[Issue, ...]


@dataclass(frozen=True)
class ReceiptSynchronization:
    receipt_id: str | None
    prefix: bytes
    suffix: bytes
    narrative_raw_sha256: str
    receipt_record: Any
    records: tuple[FenceRecord, ...]
    issues: tuple[Issue, ...]


@dataclass(frozen=True)
class MarkdownSynchronization:
    records: tuple[FenceRecord, ...]
    issues: tuple[Issue, ...]


@dataclass(frozen=True)
class _Line:
    start: int
    content_end: int
    end: int
    content: bytes


@dataclass(frozen=True)
class _MarkdownScan:
    records: tuple[FenceRecord, ...]
    headings: tuple[tuple[str, int], ...]
    issues: tuple[Issue, ...]


@dataclass(frozen=True)
class _ContainerState:
    marker: int
    run_length: int
    exact_closer: bool
    json_looking: bool
    valid_role: bool
    role: str
    opener: _Line


@dataclass(frozen=True)
class _OwnerSubstringIndex:
    transitions: tuple[Mapping[str, int], ...]
    occurrences: tuple[int, ...]

    def occurrence_count(self, pattern: str) -> int:
        if not pattern:
            return 2
        state = 0
        for character in pattern:
            target = self.transitions[state].get(character)
            if target is None:
                return 0
            state = target
        return self.occurrences[state]


@dataclass(frozen=True)
class _OwnerView:
    raw_sha256: str
    normalized_text: str | None
    substring_index: _OwnerSubstringIndex | None
    utf8_error_offset: int | None


@dataclass(frozen=True)
class _ReceiptSourceScan:
    unsupported_offset: int | None
    delimiter_offsets: tuple[int, ...]
    literal_entity_offsets: tuple[int, ...]
    code_ranges: tuple[tuple[int, int], ...]
    steps: int


class _DuplicateJsonKey(ValueError):
    pass


def _as_bytes(value: Any, path: str) -> bytes:
    try:
        length = len(value)
    except Exception as exc:
        raise KintsugiError("KIN-E-LEDGER", path, f"narrative is not byte-oriented: {exc}") from None
    if length > _MAX_UINT64:
        raise KintsugiError("KIN-E-LEDGER", path, "narrative byte length exceeds uint64")
    try:
        payload = value if isinstance(value, bytes) else bytes(value)
    except Exception as exc:
        raise KintsugiError("KIN-E-LEDGER", path, f"narrative is not bytes: {exc}") from None
    if len(payload) != length:
        raise KintsugiError("KIN-E-LEDGER", path, "narrative byte length changed during materialization")
    return payload


def framed_narrative_hash(prefix: bytes, suffix: bytes) -> str:
    prefix_bytes = _as_bytes(prefix, "narrative.prefix")
    suffix_bytes = _as_bytes(suffix, "narrative.suffix")
    digest = hashlib.sha256()
    digest.update(_NARRATIVE_DOMAIN)
    digest.update(len(prefix_bytes).to_bytes(8, "big"))
    digest.update(prefix_bytes)
    digest.update(len(suffix_bytes).to_bytes(8, "big"))
    digest.update(suffix_bytes)
    return "sha256:" + digest.hexdigest()


def _issue(path: str, offset: int, code: str, message: str) -> Issue:
    return Issue(f"{path}@{max(0, offset)}", code, message)


def _issue_offset(issue: Issue) -> int:
    try:
        return int(issue.path.rsplit("@", 1)[1])
    except (IndexError, ValueError):
        return 0


def _ordered(issues: Iterable[Issue]) -> tuple[Issue, ...]:
    return tuple(sorted(
        set(issues),
        key=lambda item: (_issue_offset(item), item.code, item.message, item.path),
    ))


def _lines(payload: bytes) -> tuple[_Line, ...]:
    result: list[_Line] = []
    start = 0
    length = len(payload)
    while start < length:
        newline = payload.find(b"\n", start)
        end = length if newline < 0 else newline + 1
        content_end = end if newline < 0 else newline
        if content_end > start and payload[content_end - 1] == 13:
            content_end -= 1
        result.append(_Line(start, content_end, end, payload[start:content_end]))
        start = end
    return tuple(result)


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJsonKey(f"duplicate object key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def _finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError(f"non-finite JSON number: {value}")
    return parsed


def _bounded_json_int(value: str) -> int:
    negative = value.startswith("-")
    digits = value[1:] if negative else value
    if len(digits) > _MAX_JSON_INTEGER_DIGITS:
        raise ValueError(
            "JSON integer exceeds fixed "
            f"{_MAX_JSON_INTEGER_DIGITS}-digit ceiling"
        )
    result = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start:start + 9]
        if not chunk.isascii() or not chunk.isdigit():
            raise ValueError("JSON integer contains a non-decimal digit")
        chunk_value = 0
        for character in chunk:
            chunk_value = chunk_value * 10 + (ord(character) - 48)
        result = result * (10 ** len(chunk)) + chunk_value
    return -result if negative else result


def _json_depth_exceeded(payload: bytes) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for byte in payload:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                in_string = False
            continue
        if byte == 34:
            in_string = True
        elif byte in (91, 123):
            depth += 1
            if depth > _MAX_JSON_DEPTH:
                return True
        elif byte in (93, 125):
            depth -= 1
    return False


def _json_value(raw: bytes, *, path: str, offset: int) -> tuple[Any, list[Issue]]:
    if _json_depth_exceeded(raw):
        return None, [_issue(path, offset, "KIN-E-JSON", "fenced JSON exceeds maximum nesting depth")]
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        return None, [_issue(path, offset + exc.start, "KIN-E-JSON", "fenced JSON is not strict UTF-8")]
    try:
        value = json.loads(
            text,
            object_pairs_hook=_duplicate_safe_object,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
            parse_int=_bounded_json_int,
        )
    except json.JSONDecodeError as exc:
        byte_position = len(text[:exc.pos].encode("utf-8"))
        return None, [_issue(
            path, offset + byte_position, "KIN-E-JSON",
            f"malformed fenced JSON: line {exc.lineno} column {exc.colno}: {exc.msg}",
        )]
    except (_DuplicateJsonKey, ValueError) as exc:
        return None, [_issue(path, offset, "KIN-E-JSON", f"malformed fenced JSON: {exc}")]
    except RecursionError:
        return None, [_issue(path, offset, "KIN-E-JSON", "fenced JSON exceeds parser depth")]
    return value, []


def _commonmark_fence_parts(
    content: bytes,
) -> tuple[int, int, int, bytes] | None:
    indent = 0
    while indent < len(content) and indent < 4 and content[indent] == 32:
        indent += 1
    if indent > 3 or indent >= len(content) or content[indent] not in (96, 126):
        return None
    marker = content[indent]
    run_length = 1
    while (
        indent + run_length < len(content)
        and content[indent + run_length] == marker
    ):
        run_length += 1
    if run_length < 3:
        return None
    return indent, marker, run_length, content[indent + run_length:]


def _json_looking_info(info: bytes) -> bool:
    classified = info.lstrip(b" \t").lower()
    return (
        classified.startswith(b"json")
        or classified.startswith(b"application/json")
        or classified.startswith(b"{.json}")
    )


def _is_container_closer(
    content: bytes, state: _ContainerState
) -> bool:
    parts = _commonmark_fence_parts(content)
    if parts is None:
        return False
    indent, closer_marker, closer_length, trailing = parts
    if closer_marker != state.marker:
        return False
    if state.exact_closer:
        return (
            indent == 0
            and closer_length == state.run_length
            and trailing == b""
        )
    return (
        closer_length >= state.run_length
        and trailing.strip(b" \t") == b""
    )


def _scan_markdown(payload: bytes, path: str) -> _MarkdownScan:
    lines = _lines(payload)
    records: list[FenceRecord] = []
    headings: list[tuple[str, int]] = []
    issues: list[Issue] = []
    active: _ContainerState | None = None
    for line in lines:
        if active is not None:
            if not _is_container_closer(line.content, active):
                continue
            if active.json_looking and active.valid_role:
                raw_json = payload[active.opener.end:line.start]
                value, json_issues = _json_value(
                    raw_json, path=path, offset=active.opener.end
                )
                issues.extend(json_issues)
                records.append(FenceRecord(
                    active.role,
                    active.opener.start,
                    active.opener.end,
                    line.start,
                    line.start,
                    line.end,
                    value,
                    not json_issues,
                ))
            active = None
            continue

        parts = _commonmark_fence_parts(line.content)
        if parts is None:
            heading_id = _heading_id(line.content)
            if heading_id is not None:
                headings.append((heading_id, line.start))
            continue

        indent, marker, run_length, info = parts
        json_looking = _json_looking_info(info)
        backtick_in_info = marker == 96 and b"`" in info
        if backtick_in_info and not (indent == 0 and json_looking):
            continue
        exact_role = info[len(b"json "):] if info.startswith(b"json ") else b""
        exact_opener = (
            indent == 0
            and marker == 96
            and run_length == 3
            and info.startswith(b"json ")
            and not backtick_in_info
        )
        try:
            role = exact_role.decode("ascii", errors="strict")
        except UnicodeDecodeError:
            role = exact_role.decode("ascii", errors="replace")

        machine_candidate = indent == 0 and json_looking
        valid_role = machine_candidate and exact_opener and role in _KNOWN_ROLES
        if machine_candidate and not valid_role:
            issues.append(_issue(
                path, line.start, "KIN-E-LEDGER", "malformed JSON fence opener"
            ))
        active = _ContainerState(
            marker=marker,
            run_length=run_length,
            exact_closer=machine_candidate,
            json_looking=machine_candidate,
            valid_role=valid_role,
            role=role,
            opener=line,
        )

    if active is not None and active.json_looking:
        detail = (
            f"unterminated {active.role} fence"
            if active.valid_role
            else "unterminated malformed JSON fence"
        )
        issues.append(_issue(path, active.opener.start, "KIN-E-LEDGER", detail))
        if active.valid_role:
            records.append(FenceRecord(
                active.role,
                active.opener.start,
                active.opener.end,
                len(payload),
                len(payload),
                len(payload),
                None,
                False,
            ))
    return _MarkdownScan(tuple(records), tuple(headings), tuple(issues))


def _scan_fences(
    payload: bytes, path: str
) -> tuple[tuple[FenceRecord, ...], list[Issue]]:
    scan = _scan_markdown(payload, path)
    return scan.records, list(scan.issues)


def extract_fenced_json(markdown: bytes, fence_kind: str) -> list[object]:
    if not isinstance(markdown, bytes):
        raise KintsugiError(
            "KIN-E-LEDGER", "markdown@0", "Markdown input must be bytes"
        )
    if type(fence_kind) is not str or fence_kind not in _KNOWN_ROLES:
        raise KintsugiError(
            "KIN-E-LEDGER", "markdown@0", "fence kind must be a known role"
        )
    records, issues = _scan_fences(markdown, "markdown")
    utf8_issue = _outside_utf8_issue(markdown, records, "markdown")
    if utf8_issue is not None:
        issues.append(utf8_issue)
    ordered = _ordered(issues)
    if ordered:
        first = ordered[0]
        raise KintsugiError(first.code, first.path, first.message)
    return [
        record.value for record in records
        if record.role == fence_kind and record.parsed_ok
    ]


def _json_equal(left: Any, right: Any) -> bool:
    pending = [(left, right)]
    seen: set[tuple[int, int]] = set()
    while pending:
        current_left, current_right = pending.pop()
        if type(current_left) is not type(current_right):
            return False
        if isinstance(current_left, dict):
            if set(current_left) != set(current_right):
                return False
            pair = (id(current_left), id(current_right))
            if pair in seen:
                continue
            seen.add(pair)
            pending.extend((current_left[key], current_right[key]) for key in current_left)
        elif isinstance(current_left, list):
            if len(current_left) != len(current_right):
                return False
            pair = (id(current_left), id(current_right))
            if pair in seen:
                continue
            seen.add(pair)
            pending.extend(zip(current_left, current_right))
        else:
            try:
                if not bool(current_left == current_right):
                    return False
            except Exception:
                return False
    return True


def _outside_utf8_issue(
    payload: bytes, records: Sequence[FenceRecord], path: str
) -> Issue | None:
    try:
        payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        if any(record.json_start <= exc.start < record.json_end for record in records):
            return None
        return _issue(path, exc.start, "KIN-E-LEDGER", "Markdown is not strict UTF-8")
    return None


def _coerce_payload(payload: Any, path: str) -> tuple[bytes, list[Issue]]:
    if isinstance(payload, bytes):
        return payload, []
    if not isinstance(payload, (bytearray, memoryview)):
        return b"", [_issue(path, 0, "KIN-E-LEDGER", "Markdown input must be bytes-like")]
    try:
        return bytes(payload), []
    except Exception:
        return b"", [_issue(path, 0, "KIN-E-LEDGER", "Markdown input must be bytes-like")]


def _synchronize_roles(
    payload: bytes,
    expected: Mapping[str, Any],
    *,
    path: str,
) -> MarkdownSynchronization:
    payload, issues = _coerce_payload(payload, path)
    records, fence_issues = _scan_fences(payload, path)
    issues.extend(fence_issues)
    utf8_issue = _outside_utf8_issue(payload, records, path)
    if utf8_issue is not None:
        issues.append(utf8_issue)
    grouped: dict[str, list[FenceRecord]] = {role: [] for role in expected}
    for record in records:
        if record.role not in expected:
            label = "unknown" if record.role not in _KNOWN_ROLES else "misplaced"
            issues.append(_issue(
                path, record.opener_start, "KIN-E-LEDGER",
                f"{label} Markdown role fence: {record.role}",
            ))
            continue
        grouped[record.role].append(record)
    for role, expected_value in expected.items():
        role_records = grouped[role]
        if not role_records:
            issues.append(_issue(path, len(payload), "KIN-E-LEDGER", f"missing {role} fence"))
            continue
        for duplicate in role_records[1:]:
            issues.append(_issue(path, duplicate.opener_start, "KIN-E-LEDGER", f"duplicate {role} fence"))
        first = role_records[0]
        if first.parsed_ok and not _json_equal(first.value, expected_value):
            issues.append(_issue(path, first.json_start, "KIN-E-LEDGER", f"{role} record does not deep-equal core record"))
    return MarkdownSynchronization(records, _ordered(issues))


def project_review_seam(seam: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(seam, Mapping):
        raise KintsugiError("KIN-E-LEDGER", "seam", "seam projection requires an object")
    try:
        projected = copy.deepcopy(dict(seam))
    except RecursionError:
        raise KintsugiError("KIN-E-LEDGER", "seam", "seam projection exceeds supported depth") from None
    if projected.get("status") == "VERIFIED":
        projected["status"] = "REPAIRED"
    for field in ("beautyGate", "truthGate", "justiceGate"):
        gate = projected.get(field)
        if isinstance(gate, dict):
            projected[field] = {"rationale": gate.get("rationale")}
    return projected


def _heading_id(content: bytes) -> str | None:
    if not content.startswith(b"## KIN-"):
        return None
    raw = content[3:]
    end = 0
    while end < len(raw) and (
        48 <= raw[end] <= 57 or 65 <= raw[end] <= 90
        or 97 <= raw[end] <= 122 or raw[end] == 45
    ):
        end += 1
    if end == 0:
        return None
    try:
        return raw[:end].decode("ascii")
    except UnicodeDecodeError:
        return None


def synchronize_ledger_markdown(
    payload: bytes,
    seams: Sequence[Mapping[str, Any]],
    *,
    path: str = "ledger.md",
) -> LedgerSynchronization:
    payload, issues = _coerce_payload(payload, path)
    if not isinstance(seams, Sequence) or isinstance(seams, (str, bytes, bytearray)):
        issues.append(_issue(path, 0, "KIN-E-LEDGER", "expected seams must be a sequence"))
        seams = ()
    scan = _scan_markdown(payload, path)
    headings = list(scan.headings)
    seen_heading_ids: set[str] = set()
    for heading_id, heading_start in headings:
        if heading_id in seen_heading_ids:
            issues.append(_issue(path, heading_start, "KIN-E-LEDGER", f"duplicate seam heading: {heading_id}"))
        seen_heading_ids.add(heading_id)

    records = scan.records
    issues.extend(scan.issues)
    utf8_issue = _outside_utf8_issue(payload, records, path)
    if utf8_issue is not None:
        issues.append(utf8_issue)

    expected_by_id: dict[str, Mapping[str, Any]] = {}
    for seam in seams:
        seam_id = seam.get("id") if isinstance(seam, Mapping) else None
        if not isinstance(seam_id, str):
            issues.append(_issue(path, len(payload), "KIN-E-LEDGER", "expected seam lacks a string id"))
            continue
        if seam_id in expected_by_id:
            issues.append(_issue(path, len(payload), "KIN-E-LEDGER", f"duplicate expected seam id: {seam_id}"))
        else:
            expected_by_id[seam_id] = seam

    first_heading = headings[0][1] if headings else len(payload)
    preamble_raw = payload[:first_heading]
    preamble = LedgerPreamble(0, first_heading, preamble_raw, raw_hash(preamble_raw))
    sections: list[LedgerSection] = []
    heading_ids = {heading_id for heading_id, _ in headings}
    for seam_id in sorted(set(expected_by_id) - heading_ids):
        issues.append(_issue(path, len(payload), "KIN-E-LEDGER", f"missing ledger section: {seam_id}"))

    records_by_section: list[list[FenceRecord]] = [[] for _ in headings]
    section_position = 0
    for record in records:
        while (
            section_position + 1 < len(headings)
            and record.opener_start >= headings[section_position + 1][1]
        ):
            section_position += 1
        if headings and record.opener_start >= headings[section_position][1]:
            records_by_section[section_position].append(record)

    for position, (heading_id, start) in enumerate(headings):
        end = headings[position + 1][1] if position + 1 < len(headings) else len(payload)
        section_records = records_by_section[position]
        seam_records = [record for record in section_records if record.role == "kintsugi-seam"]
        for record in section_records:
            if record.role != "kintsugi-seam":
                label = "unknown" if record.role not in _KNOWN_ROLES else "misplaced"
                issues.append(_issue(
                    path, record.opener_start, "KIN-E-LEDGER",
                    f"{label} role in seam section: {record.role}",
                ))
        if not seam_records:
            issues.append(_issue(path, end, "KIN-E-LEDGER", f"missing kintsugi-seam fence in {heading_id}"))
        for duplicate in seam_records[1:]:
            issues.append(_issue(path, duplicate.opener_start, "KIN-E-LEDGER", f"duplicate kintsugi-seam fence in {heading_id}"))

        expected = expected_by_id.get(heading_id)
        if expected is None:
            issues.append(_issue(path, start, "KIN-E-LEDGER", f"extra ledger section: {heading_id}"))
        selected = seam_records[0] if seam_records else None
        seam_value = selected.value if selected is not None else None
        if selected is not None and selected.parsed_ok:
            if expected is not None and not _json_equal(seam_value, expected):
                issues.append(_issue(path, selected.json_start, "KIN-E-LEDGER", f"{heading_id} fence does not deep-equal core seam"))
            if not isinstance(seam_value, dict) or seam_value.get("id") != heading_id:
                issues.append(_issue(path, selected.json_start, "KIN-E-LEDGER", f"{heading_id} fence id does not match heading"))

        if selected is None:
            prefix = payload[start:end]
            suffix = b""
        else:
            prefix = payload[start:selected.opener_start]
            suffix = payload[selected.end:end]
        projection: Any = None
        if isinstance(seam_value, dict):
            try:
                projection = project_review_seam(seam_value)
            except KintsugiError as exc:
                issues.append(_issue(path, selected.json_start if selected else start, exc.code, exc.message))
        section_raw = payload[start:end]
        sections.append(LedgerSection(
            heading_id,
            start,
            end,
            section_raw,
            raw_hash(section_raw),
            prefix,
            suffix,
            framed_narrative_hash(prefix, suffix),
            seam_value,
            projection,
        ))

    for record in records:
        if record.opener_start < first_heading:
            issues.append(_issue(path, record.opener_start, "KIN-E-LEDGER", f"role fence appears in ledger preamble: {record.role}"))
    return LedgerSynchronization(preamble, tuple(sections), _ordered(issues))


def _ascii_word(character: str) -> bool:
    return character.isascii() and (character.isalnum() or character == "_")


def _source_escape_flags(text: str) -> list[bool]:
    escaped = [False] * len(text)
    slash_run = 0
    for index, character in enumerate(text):
        escaped[index] = bool(slash_run & 1)
        if character == "\\":
            slash_run += 1
        else:
            slash_run = 0
    return escaped


def _valid_email_autolink(value: str) -> bool:
    if value.count("@") != 1:
        return False
    local, domain = value.split("@", 1)
    local_alphabet = frozenset(".!#$%&'*+/=?^_`{|}~-")
    if not local or not all(
        character.isascii()
        and (character.isalnum() or character in local_alphabet)
        for character in local
    ):
        return False
    labels = domain.split(".")
    return bool(labels) and all(
        1 <= len(label) <= 63
        and label[0].isascii()
        and label[0].isalnum()
        and label[-1].isascii()
        and label[-1].isalnum()
        and all(
            character.isascii()
            and (character.isalnum() or character == "-")
            for character in label
        )
        for label in labels
    )


def _receipt_html_end(
    text: str,
    start: int,
    next_positions: Mapping[str, Sequence[int]],
) -> tuple[int | None, int, bool]:
    """Return (end, steps, cap_exhausted) for one source construct."""

    limit = min(len(text), start + _MAX_RECEIPT_CONSTRUCT_CHARS)
    steps = 1

    def skip_tag_whitespace(cursor: int) -> tuple[int, bool]:
        nonlocal steps
        line_endings = 0
        while cursor < limit and text[cursor] in " \t\r\n":
            steps += 1
            if text[cursor] == "\r":
                line_endings += 1
                cursor += 1
                if cursor < limit and text[cursor] == "\n":
                    cursor += 1
            elif text[cursor] == "\n":
                line_endings += 1
                cursor += 1
            else:
                cursor += 1
            if line_endings > 1:
                return cursor, False
        return cursor, True

    if text.startswith("<!-->", start):
        return start + 5, steps, False
    if text.startswith("<!--->", start):
        return start + 6, steps, False

    def terminated(prefix: str, terminator: str) -> tuple[int | None, bool]:
        nonlocal steps
        if not text.startswith(prefix, start):
            return None, False
        steps += 1
        position = next_positions[terminator][start + len(prefix)]
        if position < 0:
            return None, False
        end = position + len(terminator)
        return (end, False) if end <= limit else (None, True)

    for prefix, terminator in (
        ("<!--", "-->"),
        ("<?", "?>"),
        ("<![CDATA[", "]]>")
    ):
        end, exhausted = terminated(prefix, terminator)
        if end is not None or exhausted:
            return end, steps, exhausted

    if text.startswith("<!", start):
        cursor = start + 2
        if cursor < len(text) and text[cursor].isascii() and text[cursor].isalpha():
            position = next_positions[">"][cursor + 1]
            steps += 1
            if position >= 0:
                end = position + 1
                return (end, steps, False) if end <= limit else (None, steps, True)
        return None, steps, False

    # Autolinks are recognized before tag names because URI schemes and email
    # local parts may contain '.', '+', and '-' characters.
    candidate_end = next_positions[">"][start + 1]
    if candidate_end >= 0:
        next_breaks = tuple(
            position for position in (
                next_positions["\n"][start + 1],
                next_positions["\r"][start + 1],
            ) if position >= 0
        )
        next_break = min(next_breaks) if next_breaks else -1
        next_angle = next_positions["<"][start + 1]
        if (
            (next_break < 0 or candidate_end < next_break)
            and (next_angle < 0 or candidate_end < next_angle)
        ):
            if candidate_end + 1 > limit:
                inner_prefix = text[start + 1:limit]
                if ":" in inner_prefix or "@" in inner_prefix:
                    return None, steps, True
            else:
                inner = text[start + 1:candidate_end]
                scheme_end = inner.find(":")
                valid_scheme = (
                    2 <= scheme_end <= 32
                    and inner[0].isascii()
                    and inner[0].isalpha()
                    and all(
                        character.isascii()
                        and (character.isalnum() or character in "+.-")
                        for character in inner[:scheme_end]
                    )
                    and all(
                        not (ord(character) <= 32 or ord(character) == 127)
                        and character not in "<>"
                        for character in inner[scheme_end + 1:]
                    )
                )
                if valid_scheme or _valid_email_autolink(inner):
                    return candidate_end + 1, steps, False

    cursor = start + 1
    closing = False
    if cursor < limit and text[cursor] == "/":
        closing = True
        cursor += 1
    if cursor >= limit:
        return None, steps, limit < len(text)
    if not (text[cursor].isascii() and text[cursor].isalpha()):
        return None, steps, False
    cursor += 1
    while cursor < limit and (
        text[cursor].isascii()
        and (text[cursor].isalnum() or text[cursor] == "-")
    ):
        steps += 1
        cursor += 1

    if closing:
        cursor, valid_whitespace = skip_tag_whitespace(cursor)
        if not valid_whitespace:
            return None, steps, False
        if cursor < limit and text[cursor] == ">":
            return cursor + 1, steps, False
        return None, steps, cursor >= limit and limit < len(text)

    # Open-tag grammar: a tag name followed by zero or more valid attributes.
    while True:
        whitespace_start = cursor
        cursor, valid_whitespace = skip_tag_whitespace(cursor)
        if not valid_whitespace:
            return None, steps, False
        if cursor < limit and text[cursor] == ">":
            return cursor + 1, steps, False
        if (
            cursor + 1 < limit
            and text[cursor] == "/"
            and text[cursor + 1] == ">"
        ):
            return cursor + 2, steps, False
        if cursor >= limit:
            return None, steps, limit < len(text)
        if cursor == whitespace_start:
            return None, steps, False
        if not (
            text[cursor].isascii()
            and (text[cursor].isalpha() or text[cursor] in "_:")
        ):
            return None, steps, False
        cursor += 1
        while cursor < limit and (
            text[cursor].isascii()
            and (text[cursor].isalnum() or text[cursor] in "_.:-")
        ):
            steps += 1
            cursor += 1
        attribute_end = cursor
        value_cursor, valid_whitespace = skip_tag_whitespace(cursor)
        if not valid_whitespace:
            return None, steps, False
        if value_cursor >= limit:
            return None, steps, limit < len(text)
        if text[value_cursor] != "=":
            cursor = attribute_end
            continue
        cursor = value_cursor + 1
        cursor, valid_whitespace = skip_tag_whitespace(cursor)
        if not valid_whitespace:
            return None, steps, False
        if cursor >= limit:
            return None, steps, limit < len(text)
        if text[cursor] in "\"'":
            quote = text[cursor]
            cursor += 1
            while cursor < limit and text[cursor] != quote:
                steps += 1
                cursor += 1
            if cursor >= limit:
                return None, steps, limit < len(text)
            cursor += 1
        else:
            value_start = cursor
            while (
                cursor < limit
                and not text[cursor].isspace()
                and text[cursor] not in "\"'=<>`"
            ):
                steps += 1
                cursor += 1
            if cursor == value_start:
                return None, steps, False


def _valid_link_payload(
    text: str,
    start: int,
    end: int,
    escaped: Sequence[bool],
    *,
    destination_required: bool,
) -> bool:
    def skip_whitespace(cursor: int) -> tuple[int, bool]:
        line_endings = 0
        while cursor < end and text[cursor] in " \t\r\n":
            if text[cursor] == "\r":
                line_endings += 1
                cursor += 1
                if cursor < end and text[cursor] == "\n":
                    cursor += 1
            elif text[cursor] == "\n":
                line_endings += 1
                cursor += 1
            else:
                cursor += 1
            if line_endings > 1:
                return cursor, False
        return cursor, True

    cursor = start
    cursor, valid_whitespace = skip_whitespace(cursor)
    if not valid_whitespace:
        return False
    if cursor == end:
        return not destination_required
    if text[cursor] == "<":
        cursor += 1
        while cursor < end and not (text[cursor] == ">" and not escaped[cursor]):
            if text[cursor] in "\r\n" or (text[cursor] == "<" and not escaped[cursor]):
                return False
            cursor += 1
        if cursor >= end:
            return False
        cursor += 1
    else:
        depth = 0
        destination_start = cursor
        while cursor < end:
            character = text[cursor]
            if character in " \t\r\n" and depth == 0:
                break
            if not escaped[cursor]:
                if ord(character) <= 32 or ord(character) == 127:
                    return False
                if character == "(":
                    depth += 1
                elif character == ")":
                    if depth == 0:
                        return False
                    depth -= 1
            cursor += 1
        if cursor == destination_start or depth:
            return False
    cursor, valid_whitespace = skip_whitespace(cursor)
    if not valid_whitespace:
        return False
    if cursor == end:
        return True
    quote = text[cursor]
    closing_quote = {"\"": "\"", "'": "'", "(": ")"}.get(quote)
    if closing_quote is None:
        return False
    cursor += 1
    title_line_nonblank = True
    while cursor < end:
        if text[cursor] == closing_quote and not escaped[cursor]:
            break
        if text[cursor] in "\r\n":
            if not title_line_nonblank:
                return False
            if text[cursor] == "\r":
                cursor += 1
                if cursor < end and text[cursor] == "\n":
                    cursor += 1
            else:
                cursor += 1
            title_line_nonblank = False
            continue
        if text[cursor] not in " \t":
            title_line_nonblank = True
        cursor += 1
    if cursor >= end:
        return False
    cursor += 1
    cursor, valid_whitespace = skip_whitespace(cursor)
    return valid_whitespace and cursor == end


def _valid_inline_link_payload(
    text: str,
    opener: int,
    closer: int,
    escaped: Sequence[bool],
) -> bool:
    return _valid_link_payload(
        text,
        opener + 1,
        closer,
        escaped,
        destination_required=False,
    )


def _explicit_reference_block_predecessor(line: str) -> bool:
    """Recognize the explicit block endings admitted by the receipt subset."""

    indent = len(line) - len(line.lstrip(" "))
    if indent > 3:
        return False
    content = line[indent:].rstrip(" \t")
    if content.startswith("#"):
        marker_count = len(content) - len(content.lstrip("#"))
        if 1 <= marker_count <= 6 and (
            marker_count == len(content)
            or content[marker_count] in " \t"
        ):
            return True
    compact = content.replace(" ", "").replace("\t", "")
    return (
        len(compact) >= 3
        and compact[0] in "*-_"
        and all(character == compact[0] for character in compact)
    )


def _reference_container_content_start(
    text: str,
    line_start: int,
    opener: int,
) -> tuple[int, bool]:
    """Return the simple block-container content start for a definition."""

    cursor = line_start
    leading_spaces = 0
    while cursor < opener and text[cursor] == " " and leading_spaces < 4:
        cursor += 1
        leading_spaces += 1
    if leading_spaces > 3:
        return line_start, False

    container = False
    while cursor < opener and text[cursor] == ">":
        container = True
        cursor += 1
        if cursor < opener and text[cursor] in " \t":
            cursor += 1
        nested_spaces = 0
        while cursor < opener and text[cursor] == " " and nested_spaces < 4:
            cursor += 1
            nested_spaces += 1
        if nested_spaces > 3:
            return line_start, False

    marker_end = cursor
    if cursor < opener and text[cursor] in "*+-":
        marker_end = cursor + 1
    elif cursor < opener and text[cursor].isascii() and text[cursor].isdigit():
        marker_end = cursor
        while (
            marker_end < opener
            and marker_end - cursor < 9
            and text[marker_end].isascii()
            and text[marker_end].isdigit()
        ):
            marker_end += 1
        if marker_end >= opener or text[marker_end] not in ".)":
            marker_end = cursor
        else:
            marker_end += 1
    if marker_end > cursor and marker_end < opener and text[marker_end] in " \t":
        container = True
        cursor = marker_end + 1
        while cursor < opener and text[cursor] in " \t":
            cursor += 1

    return cursor, container


def _valid_reference_label(
    text: str,
    opener: int,
    closer: int,
    escaped: Sequence[bool],
) -> bool:
    if not 1 <= closer - opener - 1 <= 999:
        return False
    has_non_whitespace = False
    for position in range(opener + 1, closer):
        character = text[position]
        if character in "[]" and not escaped[position]:
            return False
        if character not in " \t\r\n":
            has_non_whitespace = True
    return has_non_whitespace


def _reference_definition_end(
    text: str,
    start: int,
    escaped: Sequence[bool],
) -> tuple[int | None, int, bool]:
    """Parse the bounded CommonMark 0.31.2 section 4.7 payload.

    The returned end is the first byte-position of the following physical line
    (or EOF).  A plausible construct that exceeds the receipt construct bound
    is reported separately so callers can fail closed.
    """

    limit = min(len(text), start + _MAX_RECEIPT_CONSTRUCT_CHARS)
    steps = 0

    def advance_line_ending(cursor: int) -> int | None:
        if cursor >= limit:
            return None
        if text[cursor] == "\n":
            return cursor + 1
        if text[cursor] == "\r":
            cursor += 1
            if cursor < limit and text[cursor] == "\n":
                cursor += 1
            return cursor
        return None

    def skip_spaces_tabs(cursor: int) -> tuple[int, bool]:
        nonlocal steps
        found = False
        while cursor < limit and text[cursor] in " \t":
            cursor += 1
            steps += 1
            found = True
        return cursor, found

    cursor, _ = skip_spaces_tabs(start)
    following_line = advance_line_ending(cursor)
    if following_line is not None:
        steps += following_line - cursor
        cursor, _ = skip_spaces_tabs(following_line)
    if cursor >= limit:
        return None, steps, limit < len(text)
    if text[cursor] in "\r\n":
        return None, steps, False

    # Destination: either an angle-bracket destination (which may be empty)
    # or a nonempty raw destination with balanced parentheses.
    if text[cursor] == "<" and not escaped[cursor]:
        cursor += 1
        steps += 1
        while cursor < limit:
            steps += 1
            character = text[cursor]
            if character in "\r\n":
                return None, steps, False
            if character == "<" and not escaped[cursor]:
                return None, steps, False
            if character == ">" and not escaped[cursor]:
                cursor += 1
                break
            cursor += 1
        else:
            return None, steps, limit < len(text)
    else:
        destination_start = cursor
        depth = 0
        while cursor < limit:
            character = text[cursor]
            if character in " \t\r\n" and depth == 0:
                break
            if not escaped[cursor]:
                if ord(character) <= 32 or ord(character) == 127:
                    return None, steps, False
                if character == "(":
                    depth += 1
                    if depth > _MAX_RECEIPT_BRACKET_DEPTH:
                        return None, steps, True
                elif character == ")":
                    if depth == 0:
                        return None, steps, False
                    depth -= 1
            cursor += 1
            steps += 1
        if cursor == destination_start or depth:
            return None, steps, cursor >= limit and limit < len(text)

    if cursor >= limit:
        return (
            (cursor, steps, False)
            if cursor == len(text)
            else (None, steps, True)
        )

    # Save the no-title boundary before looking one physical line ahead.  If
    # that next line does not begin a properly separated title, it belongs to
    # the following block rather than invalidating the definition.
    cursor, same_line_space = skip_spaces_tabs(cursor)
    if cursor >= limit:
        return (
            (cursor, steps, False)
            if cursor == len(text)
            else (None, steps, True)
        )
    following_title_fallback: int | None = None
    following_line = advance_line_ending(cursor)
    if following_line is not None:
        steps += following_line - cursor
        title_cursor, next_line_space = skip_spaces_tabs(following_line)
        if (
            title_cursor >= limit
            or text[title_cursor] not in "\"'("
            or not (same_line_space or next_line_space)
        ):
            return following_line, steps, False
        following_title_fallback = following_line
        cursor = title_cursor
    elif text[cursor] not in "\"'(" or not same_line_space:
        return None, steps, False

    closing_quote = {"\"": "\"", "'": "'", "(": ")"}[text[cursor]]
    cursor += 1
    steps += 1
    physical_line_nonblank = True
    while cursor < limit:
        character = text[cursor]
        if character == closing_quote and not escaped[cursor]:
            cursor += 1
            steps += 1
            break
        following_line = advance_line_ending(cursor)
        if following_line is not None:
            if not physical_line_nonblank:
                return following_title_fallback, steps, False
            steps += following_line - cursor
            cursor = following_line
            physical_line_nonblank = False
            continue
        if character not in " \t":
            physical_line_nonblank = True
        cursor += 1
        steps += 1
    else:
        if limit < len(text):
            return None, steps, True
        return following_title_fallback, steps, False

    cursor, _ = skip_spaces_tabs(cursor)
    if cursor == len(text):
        return cursor, steps, False
    following_line = advance_line_ending(cursor)
    if following_line is not None:
        steps += following_line - cursor
        return following_line, steps, False
    if cursor >= limit:
        if limit < len(text):
            return None, steps, True
        return following_title_fallback, steps, False
    return following_title_fallback, steps, False


def _scan_receipt_source(text: str) -> _ReceiptSourceScan:
    """Classify source constructs once, before character-reference decoding."""

    length = len(text)
    steps = 0
    escaped = _source_escape_flags(text)
    steps += length
    paragraph_ids = [0] * length
    source_line_starts = [0] * length
    fenced_code_mask = bytearray(length)
    definition_line_starts = bytearray(length + 1)
    paragraph = 0
    cursor = 0
    previous_line_blank = True
    previous_line_content = ""
    active_fence: tuple[str, int] | None = None
    for physical_line in text.splitlines(keepends=True):
        definition_line_starts[cursor] = (
            previous_line_blank
            or _explicit_reference_block_predecessor(previous_line_content)
        )
        end = cursor + len(physical_line)
        content = physical_line.rstrip("\r\n")
        indent = len(content) - len(content.lstrip(" "))
        fence_cursor = indent if indent <= 3 else len(content)
        marker = content[fence_cursor:fence_cursor + 1]
        run_end = fence_cursor
        if marker in {"`", "~"}:
            while run_end < len(content) and content[run_end] == marker:
                run_end += 1
        run_length = run_end - fence_cursor
        line_is_fenced = active_fence is not None
        closes_fence = False
        valid_opener = (
            run_length >= 3
            and (marker != "`" or "`" not in content[run_end:])
        )
        if active_fence is None and valid_opener:
            active_fence = (marker, run_length)
            line_is_fenced = True
        elif (
            active_fence is not None
            and marker == active_fence[0]
            and run_length >= active_fence[1]
            and not content[run_end:].strip(" \t")
        ):
            line_is_fenced = True
            closes_fence = True
        for position in range(cursor, end):
            paragraph_ids[position] = paragraph
            source_line_starts[position] = cursor
            if line_is_fenced:
                fenced_code_mask[position] = 1
            steps += 1
        if closes_fence:
            active_fence = None
        previous_line_blank = not content.strip(" \t")
        previous_line_content = content
        if previous_line_blank:
            paragraph += 1
        cursor = end
    definition_line_starts[cursor] = previous_line_blank
    for position in range(cursor, length):
        paragraph_ids[position] = paragraph
        source_line_starts[position] = cursor
        steps += 1

    def next_table(token: str) -> tuple[int, ...]:
        nonlocal steps
        table = [-1] * (length + 1)
        next_position = -1
        for position in range(length - 1, -1, -1):
            steps += 1
            if text.startswith(token, position):
                next_position = position
            table[position] = next_position
        return tuple(table)

    next_positions: dict[str, Sequence[int]] = {
        token: next_table(token)
        for token in ("-->", "?>", "]]>", ">", "<", "\n", "\r")
    }

    # Pair equal-length backtick runs in source order. Paired intervals are
    # literal code for structural scanning; their delimiters are render syntax.
    runs: list[tuple[int, int, int]] = []
    index = 0
    while index < length:
        steps += 1
        if text[index] != "`" or escaped[index]:
            index += 1
            continue
        end = index + 1
        while end < length and text[end] == "`":
            steps += 1
            end += 1
        runs.append((index, end, end - index))
        index = end
    next_same: list[int | None] = [None] * len(runs)
    last_by_length: dict[int, int] = {}
    for run_index in range(len(runs) - 1, -1, -1):
        run_length = runs[run_index][2]
        next_same[run_index] = last_by_length.get(run_length)
        last_by_length[run_length] = run_index
        steps += 1
    code_mask = bytearray(fenced_code_mask)
    delimiter_mask = bytearray(length)
    code_ranges: list[tuple[int, int]] = []
    run_index = 0
    while run_index < len(runs):
        closing_index = next_same[run_index]
        if closing_index is None:
            run_index += 1
            continue
        opener = runs[run_index]
        closer = runs[closing_index]
        if paragraph_ids[opener[0]] != paragraph_ids[closer[0]]:
            run_index += 1
            continue
        for position in range(opener[0], closer[1]):
            code_mask[position] = 1
            steps += 1
        for position in range(opener[0], opener[1]):
            delimiter_mask[position] = 1
            steps += 1
        for position in range(closer[0], closer[1]):
            delimiter_mask[position] = 1
            steps += 1
        run_index = closing_index + 1

    range_start: int | None = None
    for position in range(length + 1):
        marked = position < length and bool(code_mask[position])
        if marked and range_start is None:
            range_start = position
        elif not marked and range_start is not None:
            code_ranges.append((range_start, position))
            range_start = None

    paren_stack: list[int] = []
    bracket_stack: list[tuple[int, int]] = []
    paren_closers: dict[int, int] = {}
    bracket_pairs: list[tuple[int, int, int]] = []
    for index, character in enumerate(text):
        steps += 1
        if code_mask[index] or escaped[index]:
            continue
        if character == "(":
            if len(paren_stack) >= _MAX_RECEIPT_BRACKET_DEPTH:
                literal_entities = tuple(
                    position for position, character in enumerate(text)
                    if character == "&" and (escaped[position] or code_mask[position])
                )
                return _ReceiptSourceScan(
                    index,
                    tuple(
                        position for position, marked in enumerate(delimiter_mask)
                        if marked
                    ),
                    literal_entities,
                    tuple(code_ranges),
                    steps,
                )
            paren_stack.append(index)
        elif character == ")" and paren_stack:
            paren_closers[paren_stack.pop()] = index
        elif character == "[":
            if len(bracket_stack) >= _MAX_RECEIPT_BRACKET_DEPTH:
                literal_entities = tuple(
                    position for position, character in enumerate(text)
                    if character == "&" and (escaped[position] or code_mask[position])
                )
                return _ReceiptSourceScan(
                    index,
                    tuple(
                        position for position, marked in enumerate(delimiter_mask)
                        if marked
                    ),
                    literal_entities,
                    tuple(code_ranges),
                    steps,
                )
            bracket_stack.append((index, source_line_starts[index]))
        elif character == "]" and bracket_stack:
            opener, opener_line_start = bracket_stack.pop()
            bracket_pairs.append((opener, index, opener_line_start))

    definitions: set[str] = set()
    definition_openers: set[int] = set()
    definition_continuations: set[int] = set()
    definition_span_end = 0
    definition_over_cap: int | None = None
    for opener, closer, opener_line_start in sorted(bracket_pairs):
        if opener < definition_span_end:
            continue
        content_start, in_container = _reference_container_content_start(
            text, opener_line_start, opener
        )
        indent_width = opener - content_start
        eligible = (
            0 <= indent_width <= 3
            and not fenced_code_mask[opener]
            and (
                in_container
                or definition_line_starts[opener_line_start]
                or opener_line_start in definition_continuations
            )
            and all(
                text[position] == " "
                for position in range(content_start, opener)
            )
            and closer + 1 < length
            and text[closer + 1] == ":"
            and _valid_reference_label(text, opener, closer, escaped)
        )
        if not eligible:
            continue
        definition_end, definition_steps, exhausted = _reference_definition_end(
            text, closer + 2, escaped
        )
        steps += definition_steps
        if exhausted:
            definition_over_cap = (
                opener
                if definition_over_cap is None
                else min(definition_over_cap, opener)
            )
            continue
        if definition_end is not None:
            label = " ".join(text[opener + 1:closer].casefold().split())
            steps += closer - opener + 1
            if label:
                definitions.add(label)
                definition_openers.add(opener)
                definition_span_end = max(definition_span_end, definition_end)
                if definition_end < length:
                    definition_continuations.add(definition_end)

    unsupported: int | None = definition_over_cap
    paired_brackets = {opener: closer for opener, closer, _ in bracket_pairs}
    nested_bracket_openers: set[int] = set()
    bracket_interval_stack: list[int] = []
    for opener, closer, _ in sorted(bracket_pairs):
        while bracket_interval_stack and opener > bracket_interval_stack[-1]:
            bracket_interval_stack.pop()
        if bracket_interval_stack:
            nested_bracket_openers.add(opener)
        bracket_interval_stack.append(closer)
    for opener, closer, _ in bracket_pairs:
        steps += 1
        if opener in definition_openers:
            continue
        following_index = closer + 1
        if (
            following_index < length
            and text[following_index] == "("
            and following_index in paren_closers
            and paragraph_ids[opener] == paragraph_ids[closer]
            and paragraph_ids[opener]
            == paragraph_ids[paren_closers[following_index]]
            and _valid_inline_link_payload(
                text,
                following_index,
                paren_closers[following_index],
                escaped,
            )
        ):
            unsupported = opener if unsupported is None else min(unsupported, opener)
        elif (
            following_index < length
            and text[following_index] == "["
            and following_index in paired_brackets
        ):
            reference_closer = paired_brackets[following_index]
            collapsed = reference_closer == following_index + 1
            if (
                paragraph_ids[opener] != paragraph_ids[closer]
                or paragraph_ids[opener] != paragraph_ids[reference_closer]
                or (
                    collapsed
                    and not _valid_reference_label(
                        text, opener, closer, escaped
                    )
                )
                or (
                    not collapsed
                    and not _valid_reference_label(
                        text, following_index, reference_closer, escaped
                    )
                )
            ):
                continue
            reference_label = " ".join(
                text[following_index + 1:reference_closer].casefold().split()
            )
            if not reference_label:
                reference_label = " ".join(
                    text[opener + 1:closer].casefold().split()
                )
            steps += reference_closer - following_index + 1
            if reference_label in definitions:
                unsupported = opener if unsupported is None else min(unsupported, opener)
        elif (
            opener not in nested_bracket_openers
            and opener > 0
            and closer + 1 < length
            and _ascii_word(text[opener - 1])
            and _ascii_word(text[closer + 1])
        ):
            unsupported = opener if unsupported is None else min(unsupported, opener)
        else:
            if definitions:
                label = " ".join(text[opener + 1:closer].casefold().split())
                steps += closer - opener + 1
                if (
                    _valid_reference_label(text, opener, closer, escaped)
                    and label
                    and label in definitions
                ):
                    unsupported = opener if unsupported is None else min(unsupported, opener)

    for index, character in enumerate(text):
        steps += 1
        if character != "<" or code_mask[index] or escaped[index]:
            continue
        end, html_steps, exhausted = _receipt_html_end(
            text, index, next_positions
        )
        steps += html_steps
        block_prefix = text[source_line_starts[index]:index]
        block_capable = (
            len(block_prefix) <= 3
            and not block_prefix.strip(" ")
            and (
                text.startswith("<!--", index)
                or text.startswith("<?", index)
                or text.startswith("<![CDATA[", index)
                or (
                    text.startswith("<!", index)
                    and index + 2 < length
                    and text[index + 2].isascii()
                    and text[index + 2].isalpha()
                )
            )
        )
        crosses_paragraph = (
            end is not None
            and end > index
            and paragraph_ids[index] != paragraph_ids[end - 1]
        )
        if (
            (end is not None and (not crosses_paragraph or block_capable))
            or exhausted
        ):
            unsupported = index if unsupported is None else min(unsupported, index)

    def is_whitespace(character: str) -> bool:
        return not character or character.isspace()

    def is_punctuation(character: str) -> bool:
        return bool(character) and unicodedata.category(character)[0] in "PS"

    delimiter_stacks: dict[str, list[tuple[int, int]]] = {"*": [], "_": []}
    index = 0
    while index < length:
        steps += 1
        marker = text[index]
        if (
            marker not in delimiter_stacks
            or code_mask[index]
            or escaped[index]
        ):
            index += 1
            continue
        end = index + 1
        while end < length and text[end] == marker and not code_mask[end]:
            steps += 1
            end += 1
        run_length = end - index
        previous = text[index - 1] if index else ""
        following = text[end] if end < length else ""
        left_flanking = (
            not is_whitespace(following)
            and (
                not is_punctuation(following)
                or is_whitespace(previous)
                or is_punctuation(previous)
            )
        )
        right_flanking = (
            not is_whitespace(previous)
            and (
                not is_punctuation(previous)
                or is_whitespace(following)
                or is_punctuation(following)
            )
        )
        can_open = left_flanking
        can_close = right_flanking
        if marker == "_":
            can_open = left_flanking and (not right_flanking or is_punctuation(previous))
            can_close = right_flanking and (not left_flanking or is_punctuation(following))
        stack = delimiter_stacks[marker]
        if can_close and stack:
            opener_start, opener_end = stack.pop()
            pair_length = min(opener_end - opener_start, end - index)
            for position in range(opener_end - pair_length, opener_end):
                delimiter_mask[position] = 1
                steps += 1
            for position in range(index, index + pair_length):
                delimiter_mask[position] = 1
                steps += 1
        elif can_open:
            stack.append((index, end))
        index = end

    steps += length
    literal_entities = tuple(
        position for position, character in enumerate(text)
        if character == "&" and (escaped[position] or code_mask[position])
    )
    return _ReceiptSourceScan(
        unsupported,
        tuple(
            position for position, marked in enumerate(delimiter_mask)
            if marked
        ),
        literal_entities,
        tuple(code_ranges),
        steps,
    )


def _decode_commonmark_entities(
    text: str,
    source_offsets: Sequence[int],
    literal_entity_offsets: frozenset[int],
) -> str:
    output: list[str] = []
    index = 0
    while index < len(text):
        if (
            text[index] != "&"
            or source_offsets[index] in literal_entity_offsets
        ):
            output.append(text[index])
            index += 1
            continue
        semicolon = text.find(";", index + 1, min(len(text), index + 36))
        if semicolon < 0:
            output.append("&")
            index += 1
            continue
        candidate = text[index:semicolon + 1]
        body = candidate[1:-1]
        valid = False
        if body.startswith(("#x", "#X")):
            digits = body[2:]
            valid = 1 <= len(digits) <= 6 and all(
                character in "0123456789abcdefABCDEF" for character in digits
            )
        elif body.startswith("#"):
            digits = body[1:]
            valid = 1 <= len(digits) <= 7 and digits.isascii() and digits.isdigit()
        else:
            valid = body + ";" in _HTML5_ENTITIES
        if valid:
            output.append(html.unescape(candidate))
            index = semicolon + 1
        else:
            output.append("&")
            index += 1
    return "".join(output)


def _rendered_receipt_projection(
    text: str,
    *,
    source_start: int = 0,
    delimiter_offsets: frozenset[int] = frozenset(),
    literal_entity_offsets: frozenset[int] = frozenset(),
    code_ranges: tuple[tuple[int, int], ...] = (),
) -> str:
    if len(text) > _MAX_RECEIPT_PROJECTION_CHARS:
        raise ValueError(
            f"receipt lexical grammar v{_RECEIPT_LEXICAL_GRAMMAR_VERSION} "
            "line exceeds projection bound"
        )
    kept_source: list[tuple[str, int]] = []
    range_index = 0
    for index, character in enumerate(text):
        source_offset = source_start + index
        if source_offset in delimiter_offsets:
            continue
        while (
            range_index < len(code_ranges)
            and code_ranges[range_index][1] <= source_offset
        ):
            range_index += 1
        in_code = (
            range_index < len(code_ranges)
            and code_ranges[range_index][0] <= source_offset
            < code_ranges[range_index][1]
        )
        kept_source.append((" " if in_code else character, source_offset))
    source_without_delimiters = "".join(
        character for character, _ in kept_source
    )
    projected = _decode_commonmark_entities(
        source_without_delimiters,
        [offset for _, offset in kept_source],
        literal_entity_offsets,
    )
    if len(projected) > _MAX_RECEIPT_PROJECTION_CHARS:
        raise ValueError(
            f"receipt lexical grammar v{_RECEIPT_LEXICAL_GRAMMAR_VERSION} "
            "entity expansion exceeds projection bound"
        )
    projected = unicodedata.normalize("NFKC", projected)
    if len(projected) > _MAX_RECEIPT_PROJECTION_CHARS:
        raise ValueError(
            f"receipt lexical grammar v{_RECEIPT_LEXICAL_GRAMMAR_VERSION} "
            "NFKC expansion exceeds projection bound"
        )
    projected = "".join(
        character
        for character in projected
        if unicodedata.category(character) != "Cf"
    )
    return projected


def _static_receipt_line(
    projected: str, receipt: Mapping[str, Any]
) -> bool:
    normalized = " ".join(projected.strip().casefold().split())
    if normalized in _STATIC_RECEIPT_LINES:
        return True
    phase = receipt.get("phase")
    if isinstance(phase, str) and normalized == (
        f"# kintsugi phase {phase.casefold()} receipt"
    ):
        return True
    receipt_id = receipt.get("id")
    return (
        isinstance(receipt_id, str)
        and normalized == f"## receipt id: {receipt_id.casefold()}"
    )


def _receipt_subject_tokens(text: str) -> list[str]:
    raw_words = "".join(
        character if character.isalnum() else " " for character in text
    ).split()
    tokens: list[str] = []
    for word in raw_words:
        folded = word.casefold()
        tokens.append(folded)
        parts: list[str] = []
        start = 0
        for index in range(1, len(word)):
            current = word[index]
            previous = word[index - 1]
            following = word[index + 1] if index + 1 < len(word) else ""
            if current.isupper() and (
                previous.islower()
                or previous.isdigit()
                or (previous.isupper() and following.islower())
            ):
                parts.append(word[start:index].casefold())
                start = index
        parts.append(word[start:].casefold())
        if len(parts) > 1:
            tokens.extend(parts)
    return tokens


def _receipt_line_is_dynamic(projected: str, tokens: Sequence[str]) -> bool:
    token_set = set(tokens)
    if token_set & _CONTROL_COMPOUNDS:
        return True
    subjects = _CONTROL_SUBJECT_LEXEMES | _AMBIGUOUS_CONTROL_NOUNS
    if _has_bounded_closure_predicate(tokens, subjects):
        return True
    stripped = projected.strip().casefold()
    if _has_control_field_shape(stripped, tokens, subjects):
        return True
    return False


def _has_control_field_shape(
    stripped: str,
    tokens: Sequence[str],
    subjects: Iterable[str],
) -> bool:
    subject_set = set(subjects)
    token_set = set(tokens)
    has_control_phrase = any(
        (left, right) in _CONTROL_PHRASES
        for left, right in zip(tokens, tokens[1:])
    )
    heading = stripped.startswith("#")
    if heading and (token_set & subject_set or has_control_phrase):
        return True
    separator_positions = [
        position for marker in (":", "=")
        if (position := stripped.find(marker)) >= 0
    ]
    if separator_positions:
        prefix = stripped[:min(separator_positions)]
        prefix_tokens = _receipt_subject_tokens(prefix)
        first = prefix_tokens[0] if prefix_tokens else ""
        field_words = subject_set | _CONTROL_COMPOUNDS | {"id", "path"}
        if (
            1 <= len(prefix_tokens) <= 4
            and (first in subject_set or first in _CONTROL_COMPOUNDS)
            and all(token in field_words for token in prefix_tokens)
        ):
            return True
    if has_control_phrase:
        for index, pair in enumerate(zip(tokens, tokens[1:])):
            if (
                pair in _CONTROL_PHRASES
                and index + 2 < len(tokens)
                and tokens[index + 2] in {"are", "is", "was", "were"}
            ):
                return True
    return False


def _has_bounded_closure_predicate(
    tokens: Sequence[str], subjects: Iterable[str]
) -> bool:
    subject_set = set(subjects)
    for index, token in enumerate(tokens):
        if token not in subject_set:
            continue
        if index > 0 and tokens[index - 1] in _CLOSURE_PREDICATES:
            return True
        predicate_index = index + 1
        linker_count = 0
        while (
            predicate_index < len(tokens)
            and tokens[predicate_index] in _CLOSURE_LINKERS
        ):
            predicate_index += 1
            linker_count += 1
            if linker_count > _MAX_CLOSURE_LINKERS:
                return True
        if (
            predicate_index < len(tokens)
            and tokens[predicate_index] in _CLOSURE_PREDICATES
        ):
            return True
    return False


def _dynamic_receipt_issues(
    raw: bytes,
    receipt: Mapping[str, Any],
    *,
    base: int,
    path: str,
) -> list[Issue]:
    issues: list[Issue] = []
    source_scan: _ReceiptSourceScan | None = None
    delimiter_offsets: frozenset[int] = frozenset()
    literal_entity_offsets: frozenset[int] = frozenset()
    code_ranges: tuple[tuple[int, int], ...] = ()
    try:
        source_text = raw.decode("utf-8", errors="strict")
        source_scan = _scan_receipt_source(source_text)
        delimiter_offsets = frozenset(source_scan.delimiter_offsets)
        literal_entity_offsets = frozenset(
            source_scan.literal_entity_offsets
        )
        code_ranges = source_scan.code_ranges
    except UnicodeDecodeError:
        source_text = ""
    except Exception:
        issues.append(_issue(
            path, base, "KIN-E-LEDGER",
            "receipt prose cannot be represented by the bounded lexical grammar",
        ))
        source_text = ""
    if source_scan is not None and source_scan.unsupported_offset is not None:
        byte_offset = len(
            source_text[:source_scan.unsupported_offset].encode("utf-8")
        )
        issues.append(_issue(
            path, base + byte_offset, "KIN-E-LEDGER",
            "receipt prose cannot be represented by the bounded lexical grammar",
        ))
    source_cursor = 0
    code_range_cursor = 0
    for line in _lines(raw):
        try:
            line_span_length = len(raw[line.start:line.end].decode(
                "utf-8", errors="strict"
            ))
        except UnicodeDecodeError:
            line_span_length = 0
        try:
            text = line.content.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            source_cursor += line_span_length
            continue
        try:
            line_content_end = source_cursor + len(text)
            while (
                code_range_cursor < len(code_ranges)
                and code_ranges[code_range_cursor][1] <= source_cursor
            ):
                code_range_cursor += 1
            range_cursor = code_range_cursor
            line_code_ranges: list[tuple[int, int]] = []
            while (
                range_cursor < len(code_ranges)
                and code_ranges[range_cursor][0] < line_content_end
            ):
                line_code_ranges.append(code_ranges[range_cursor])
                range_cursor += 1
            projected = _rendered_receipt_projection(
                text,
                source_start=source_cursor,
                delimiter_offsets=delimiter_offsets,
                literal_entity_offsets=literal_entity_offsets,
                code_ranges=tuple(line_code_ranges),
            )
        except Exception:
            issues.append(_issue(
                path, base + line.start, "KIN-E-LEDGER",
                "receipt prose cannot be represented by the bounded lexical grammar",
            ))
            source_cursor += line_span_length
            continue
        if not projected.strip() or _static_receipt_line(projected, receipt):
            source_cursor += line_span_length
            continue
        tokens = _receipt_subject_tokens(projected)
        if _receipt_line_is_dynamic(projected, tokens):
            issues.append(_issue(
                path, base + line.start, "KIN-E-LEDGER",
                "dynamic receipt prose is forbidden outside the fence after target freeze",
            ))
        source_cursor += line_span_length
    return issues


def _build_owner_substring_index(text: str) -> _OwnerSubstringIndex:
    """Build a capped-occurrence suffix automaton in linear time and space."""

    transitions: list[dict[str, int]] = [{}]
    links = [-1]
    lengths = [0]
    occurrences = [0]
    last = 0

    for character in text:
        current = len(transitions)
        transitions.append({})
        links.append(0)
        lengths.append(lengths[last] + 1)
        occurrences.append(1)
        predecessor = last
        while (
            predecessor >= 0
            and character not in transitions[predecessor]
        ):
            transitions[predecessor][character] = current
            predecessor = links[predecessor]
        if predecessor < 0:
            links[current] = 0
        else:
            successor = transitions[predecessor][character]
            if lengths[predecessor] + 1 == lengths[successor]:
                links[current] = successor
            else:
                clone = len(transitions)
                transitions.append(transitions[successor].copy())
                links.append(links[successor])
                lengths.append(lengths[predecessor] + 1)
                occurrences.append(0)
                while (
                    predecessor >= 0
                    and transitions[predecessor].get(character) == successor
                ):
                    transitions[predecessor][character] = clone
                    predecessor = links[predecessor]
                links[successor] = clone
                links[current] = clone
        last = current

    length_counts = [0] * (len(text) + 1)
    for length in lengths:
        length_counts[length] += 1
    next_position = [0] * len(length_counts)
    position = 0
    for length, count in enumerate(length_counts):
        next_position[length] = position
        position += count
    length_order = [0] * len(transitions)
    for state, length in enumerate(lengths):
        length_order[next_position[length]] = state
        next_position[length] += 1
    for state in reversed(length_order):
        suffix = links[state]
        if suffix >= 0:
            occurrences[suffix] = min(
                2, occurrences[suffix] + occurrences[state]
            )

    return _OwnerSubstringIndex(
        tuple(MappingProxyType(edges) for edges in transitions),
        tuple(min(2, count) for count in occurrences),
    )


def _build_owner_view(raw: bytes) -> _OwnerView:
    raw_sha256 = raw_hash(raw)
    try:
        owner_text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        return _OwnerView(raw_sha256, None, None, exc.start)
    normalized_owner = normalize_lf(owner_text)
    return _OwnerView(
        raw_sha256,
        normalized_owner,
        _build_owner_substring_index(normalized_owner),
        None,
    )


def _matches_text_hash(value: Any, expected: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return expected == text_hash(value)
    except Exception:
        return False


def synchronize_receipt_markdown(
    payload: bytes,
    receipt: Mapping[str, Any],
    *,
    path: str = "receipt.md",
    target_frozen: bool = False,
) -> ReceiptSynchronization:
    input_issues: list[Issue] = []
    if not isinstance(receipt, Mapping):
        input_issues.append(_issue(path, 0, "KIN-E-LEDGER", "expected receipt must be an object"))
        receipt = {}
    payload, payload_issues = _coerce_payload(payload, path)
    input_issues.extend(payload_issues)
    synchronized = _synchronize_roles(
        payload, {"kintsugi-receipt": receipt}, path=path
    )
    receipt_records = [
        record for record in synchronized.records
        if record.role == "kintsugi-receipt"
    ]
    selected = receipt_records[0] if receipt_records else None
    if selected is None:
        prefix, suffix, value = payload, b"", None
    else:
        prefix, suffix, value = payload[:selected.opener_start], payload[selected.end:], selected.value
    issues = input_issues + list(synchronized.issues)
    if target_frozen:
        issues.extend(_dynamic_receipt_issues(
            prefix, receipt, base=0, path=path
        ))
        suffix_base = selected.end if selected is not None else len(prefix)
        issues.extend(_dynamic_receipt_issues(
            suffix, receipt, base=suffix_base, path=path
        ))
    receipt_id = receipt.get("id") if isinstance(receipt.get("id"), str) else None
    return ReceiptSynchronization(
        receipt_id,
        prefix,
        suffix,
        framed_narrative_hash(prefix, suffix),
        value,
        synchronized.records,
        _ordered(issues),
    )


def synchronize_review_markdown(
    payload: bytes,
    attestation: Mapping[str, Any],
    findings: Sequence[Mapping[str, Any]],
    *,
    path: str = "review.md",
) -> MarkdownSynchronization:
    input_issues: list[Issue] = []
    if not isinstance(attestation, Mapping):
        input_issues.append(_issue(path, 0, "KIN-E-LEDGER", "expected attestation must be an object"))
        attestation = {}
    if not isinstance(findings, Sequence) or isinstance(findings, (str, bytes, bytearray)):
        input_issues.append(_issue(path, 0, "KIN-E-LEDGER", "expected findings must be a sequence"))
        findings = ()
    valid_findings: list[dict[str, Any]] = []
    for finding in findings:
        if isinstance(finding, Mapping):
            valid_findings.append(dict(finding))
        else:
            input_issues.append(_issue(path, 0, "KIN-E-LEDGER", "each expected finding must be an object"))
    seen_finding_ids: set[str] = set()
    for finding in valid_findings:
        finding_id = finding.get("id")
        if not isinstance(finding_id, str):
            input_issues.append(_issue(
                path, 0, "KIN-E-LEDGER",
                "expected review finding id must be a string",
            ))
        elif finding_id in seen_finding_ids:
            input_issues.append(_issue(
                path, 0, "KIN-E-LEDGER",
                f"duplicate expected review finding id: {finding_id}",
            ))
        else:
            seen_finding_ids.add(finding_id)
    attestation_finding_ids = attestation.get("findingIds")
    if isinstance(attestation_finding_ids, Sequence) and not isinstance(
        attestation_finding_ids, (str, bytes, bytearray)
    ):
        seen_attestation_ids: set[str] = set()
        for finding_id in attestation_finding_ids:
            if not isinstance(finding_id, str):
                input_issues.append(_issue(
                    path, 0, "KIN-E-LEDGER",
                    "attestation finding id must be a string",
                ))
            elif finding_id in seen_attestation_ids:
                input_issues.append(_issue(
                    path, 0, "KIN-E-LEDGER",
                    f"duplicate attestation finding id: {finding_id}",
                ))
            else:
                seen_attestation_ids.add(finding_id)
    payload, payload_issues = _coerce_payload(payload, path)
    input_issues.extend(payload_issues)
    sorted_findings = sorted(
        valid_findings,
        key=lambda finding: (
            finding.get("id") if isinstance(finding.get("id"), str) else ""
        ),
    )
    synchronized = _synchronize_roles(payload, {
        "kintsugi-review": attestation,
        "kintsugi-review-findings": sorted_findings,
    }, path=path)
    issues = input_issues + list(synchronized.issues)
    offsets = {
        record.role: record.json_start for record in synchronized.records
        if record.role in {"kintsugi-review", "kintsugi-review-findings"}
    }
    finding_offset = offsets.get("kintsugi-review-findings", len(payload))
    attestation_offset = offsets.get("kintsugi-review", len(payload))
    finding_ids = [finding.get("id") for finding in sorted_findings]
    if attestation.get("findingIds") != finding_ids:
        issues.append(_issue(
            path, attestation_offset, "KIN-E-LEDGER",
            "review finding IDs do not deep-equal the sorted findings fence",
        ))
    for finding in sorted_findings:
        if finding.get("attemptId") != attestation.get("attemptId"):
            issues.append(_issue(
                path, finding_offset, "KIN-E-LEDGER",
                f"review finding attempt does not match attestation: {finding.get('id')}",
            ))
        if finding.get("reviewKind") != attestation.get("kind"):
            issues.append(_issue(
                path, finding_offset, "KIN-E-LEDGER",
                f"review finding kind does not match attestation: {finding.get('id')}",
            ))
    return MarkdownSynchronization(synchronized.records, _ordered(issues))


def synchronize_public_queue_markdown(
    payload: bytes,
    public_queue: Mapping[str, Any],
    *,
    path: str = "public-queue.md",
) -> MarkdownSynchronization:
    issues: list[Issue] = []
    if not isinstance(public_queue, Mapping):
        issues.append(_issue(path, 0, "KIN-E-LEDGER", "expected public queue must be an object"))
        public_queue = {}
    payload, payload_issues = _coerce_payload(payload, path)
    issues.extend(payload_issues)
    synchronized = _synchronize_roles(
        payload, {"kintsugi-public-queue": public_queue}, path=path
    )
    issues.extend(synchronized.issues)
    return MarkdownSynchronization(synchronized.records, _ordered(issues))


def synchronize_owner(
    root: Path,
    source: Mapping[str, Any],
    claim: Mapping[str, Any],
    trial: Mapping[str, Any],
    seam: Mapping[str, Any],
) -> tuple[Issue, ...]:
    if not all(isinstance(record, Mapping) for record in (source, claim, trial, seam)):
        return (_issue("<owner>", 0, "KIN-E-QUOTE", "owner synchronization records must be objects"),)
    try:
        root = Path(root)
    except Exception:
        return (_issue("<owner>", 0, "KIN-E-QUOTE", "owner repository root is invalid"),)
    issues: list[Issue] = []
    relative = source.get("path")
    issue_path = relative if isinstance(relative, str) else "<owner>"
    if not isinstance(relative, str):
        return (_issue(issue_path, 0, "KIN-E-QUOTE", "owner source path is absent"),)
    try:
        owner_path = safe_repo_path(root, relative)
    except KintsugiError as exc:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", f"unsafe owner path: {exc.message}"),)
    except Exception:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", "owner source path cannot be resolved"),)
    try:
        is_file = owner_path.is_file()
    except Exception:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", "owner source kind cannot be resolved"),)
    if not is_file:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", "owner source does not exist as a file"),)
    try:
        raw = owner_path.read_bytes()
    except Exception:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", "owner source is unreadable"),)

    return _synchronize_owner_payload(
        raw, issue_path, source, claim, trial, seam
    )


def _synchronize_owner_payload(
    raw: bytes,
    issue_path: str,
    source: Mapping[str, Any],
    claim: Mapping[str, Any],
    trial: Mapping[str, Any],
    seam: Mapping[str, Any],
) -> tuple[Issue, ...]:
    """Verify owner-bound records against one already-frozen byte snapshot."""

    return _synchronize_owner_view(
        _build_owner_view(raw), issue_path, source, claim, trial, seam
    )


def _synchronize_owner_view(
    owner: _OwnerView,
    issue_path: str,
    source: Mapping[str, Any],
    claim: Mapping[str, Any],
    trial: Mapping[str, Any],
    seam: Mapping[str, Any],
) -> tuple[Issue, ...]:
    """Verify records against one immutable, indexed owner view."""

    issues: list[Issue] = []
    if source.get("kind") != "OWNER" or source.get("authorityRole") != "SEMANTIC_OWNER":
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "declared source is not a semantic owner"))
    if source.get("sha256") != owner.raw_sha256:
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "owner source raw SHA-256 does not match"))
    if claim.get("ownerSourceId") != source.get("id") or seam.get("ownerSource") != source.get("id"):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "owner source identity does not synchronize"))
    if trial.get("claimId") != claim.get("id") or seam.get("claimId") != claim.get("id"):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "owner claim identity does not synchronize"))
    if claim.get("ownerAnchor") != seam.get("ownerAnchor"):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "owner anchor does not synchronize"))

    before_quote = seam.get("beforeQuote")
    tried_quote = trial.get("triedQuote")
    if not _matches_text_hash(before_quote, seam.get("beforeHash")):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "seam beforeHash is not the LF-normalized beforeQuote hash"))
    if not _matches_text_hash(tried_quote, trial.get("triedHash")):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "trial triedHash is not the LF-normalized triedQuote hash"))
    if (
        isinstance(before_quote, str) and isinstance(tried_quote, str)
        and (normalize_lf(before_quote) != normalize_lf(tried_quote)
             or seam.get("beforeHash") != trial.get("triedHash"))
    ):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "seam tried form does not synchronize with its trial"))

    if owner.utf8_error_offset is not None:
        issues.append(_issue(
            issue_path,
            owner.utf8_error_offset,
            "KIN-E-QUOTE",
            "owner source is not strict UTF-8",
        ))
        return _ordered(issues)
    substring_index = owner.substring_index
    if owner.normalized_text is None or substring_index is None:
        issues.append(_issue(
            issue_path, 0, "KIN-E-QUOTE", "owner source index is unavailable"
        ))
        return _ordered(issues)
    anchor = seam.get("ownerAnchor")
    if (
        not isinstance(anchor, str)
        or substring_index.occurrence_count(normalize_lf(anchor)) == 0
    ):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "owner anchor is absent"))
    one_sided = seam.get("status") in _ONE_SIDED_SEAM_STATUSES
    current_field = "beforeQuote" if one_sided else "afterQuote"
    current_quote = seam.get(current_field)
    if one_sided and seam.get("afterQuote") is not None:
        issues.append(_issue(
            issue_path, 0, "KIN-E-QUOTE",
            "afterQuote must be null for a one-sided seam",
        ))
    if (
        not isinstance(current_quote, str)
        or substring_index.occurrence_count(normalize_lf(current_quote)) != 1
    ):
        issues.append(_issue(
            issue_path, 0, "KIN-E-QUOTE",
            f"{current_field} must appear exactly once in the owner source",
        ))
    return _ordered(issues)


def _mapping_records(
    core: Mapping[str, object], key: str, issues: list[Issue]
) -> list[Mapping[str, Any]]:
    if key not in core:
        issues.append(_issue(
            f"core.{key}", 0, "KIN-E-LEDGER", f"core is missing {key}"
        ))
        return []
    value = core.get(key)
    if not isinstance(value, Sequence) or isinstance(
        value, (str, bytes, bytearray)
    ):
        issues.append(_issue(
            f"core.{key}", 0, "KIN-E-LEDGER", f"core {key} must be a sequence"
        ))
        return []
    records: list[Mapping[str, Any]] = []
    for index, record in enumerate(value):
        if isinstance(record, Mapping):
            records.append(record)
        else:
            issues.append(_issue(
                f"core.{key}[{index}]", 0, "KIN-E-LEDGER",
                f"core {key} record must be an object",
            ))
    return records


def _record_index(
    records: Sequence[Mapping[str, Any]],
    *,
    label: str,
    code: str,
    issues: list[Issue],
) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for position, record in enumerate(records):
        record_id = record.get("id")
        if not isinstance(record_id, str):
            issues.append(_issue(
                f"core.{label}[{position}]", 0, code,
                f"{label} record lacks a string id",
            ))
        elif record_id in indexed:
            issues.append(_issue(
                f"core.{label}[{position}]", 0, code,
                f"duplicate {label} id: {record_id}",
            ))
        else:
            indexed[record_id] = record
    return indexed


def _validate_markdown_sync(
    root: Path, core: dict[str, object], ledger_path: Path | None
) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(core, dict):
        return [_issue(
            "core", 0, "KIN-E-LEDGER", "Markdown core must be an object"
        )]
    try:
        resolved_root = Path(root).resolve(strict=True)
        root_is_directory = resolved_root.is_dir()
    except Exception:
        return [_issue(
            "<root>", 0, "KIN-E-LEDGER", "Markdown repository root is unavailable"
        )]
    if not root_is_directory:
        return [_issue(
            "<root>", 0, "KIN-E-LEDGER", "Markdown repository root is not a directory"
        )]

    read_cache: dict[Path, bytes] = {}

    def read_path(path: Path, issue_path: str) -> bytes | None:
        try:
            if not path.is_file():
                issues.append(_issue(
                    issue_path, 0, "KIN-E-LEDGER",
                    "declared Markdown path does not exist as a file",
                ))
                return None
            if path not in read_cache:
                read_cache[path] = path.read_bytes()
            return read_cache[path]
        except Exception:
            issues.append(_issue(
                issue_path, 0, "KIN-E-LEDGER", "declared Markdown path is unreadable"
            ))
            return None

    def read_declared(relative: Any, label: str) -> bytes | None:
        if not isinstance(relative, str):
            issues.append(_issue(
                label, 0, "KIN-E-LEDGER", "declared Markdown path must be a string"
            ))
            return None
        try:
            resolved = safe_repo_path(resolved_root, relative)
        except Exception:
            issues.append(_issue(
                relative, 0, "KIN-E-LEDGER", "declared Markdown path is unsafe"
            ))
            return None
        return read_path(resolved, relative)

    seams = _mapping_records(core, "seams", issues)
    receipts = _mapping_records(core, "phaseReceipts", issues)
    attestations = _mapping_records(core, "reviewAttestations", issues)
    findings = _mapping_records(core, "reviewFindings", issues)
    artifacts = _mapping_records(core, "reviewAttemptArtifacts", issues)
    sources = _mapping_records(core, "sources", issues)
    claims = _mapping_records(core, "claims", issues)
    trials = _mapping_records(core, "trials", issues)
    trials_by_seam_id: dict[str, list[Mapping[str, Any]]] = {}
    for position, trial in enumerate(trials):
        seam_id = trial.get("seamId")
        if not isinstance(seam_id, str):
            issues.append(_issue(
                f"core.trials[{position}]", 0, "KIN-E-QUOTE",
                "trial seamId must be a string",
            ))
            continue
        matching_trials = trials_by_seam_id.setdefault(seam_id, [])
        if matching_trials:
            issues.append(_issue(
                f"core.trials[{position}]", 0, "KIN-E-QUOTE",
                f"duplicate trial seamId binding: {seam_id}",
            ))
        matching_trials.append(trial)

    owner_snapshot_cache: dict[
        Path, tuple[_OwnerView | None, str | None]
    ] = {}

    def read_owner_snapshot(
        source: Mapping[str, Any],
    ) -> tuple[str, _OwnerView | None, tuple[Issue, ...]]:
        relative = source.get("path")
        issue_path = relative if isinstance(relative, str) else "<owner>"
        if not isinstance(relative, str):
            return (
                issue_path,
                None,
                (_issue(
                    issue_path, 0, "KIN-E-QUOTE", "owner source path is absent"
                ),),
            )
        try:
            owner_path = safe_repo_path(resolved_root, relative)
        except KintsugiError as exc:
            return (
                issue_path,
                None,
                (_issue(
                    issue_path, 0, "KIN-E-QUOTE",
                    f"unsafe owner path: {exc.message}",
                ),),
            )
        except Exception:
            return (
                issue_path,
                None,
                (_issue(
                    issue_path, 0, "KIN-E-QUOTE",
                    "owner source path cannot be resolved",
                ),),
            )

        if owner_path in owner_snapshot_cache:
            owner_view, error_message = owner_snapshot_cache[owner_path]
            snapshot_issues = (
                ()
                if error_message is None
                else (_issue(
                    issue_path, 0, "KIN-E-QUOTE", error_message
                ),)
            )
            return issue_path, owner_view, snapshot_issues

        if owner_path in read_cache:
            raw = read_cache[owner_path]
        else:
            try:
                is_file = owner_path.is_file()
            except Exception:
                error_message = "owner source kind cannot be resolved"
                owner_snapshot_cache[owner_path] = (None, error_message)
                return (
                    issue_path, None,
                    (_issue(issue_path, 0, "KIN-E-QUOTE", error_message),),
                )
            if not is_file:
                error_message = "owner source does not exist as a file"
                owner_snapshot_cache[owner_path] = (None, error_message)
                return (
                    issue_path, None,
                    (_issue(issue_path, 0, "KIN-E-QUOTE", error_message),),
                )
            try:
                raw = owner_path.read_bytes()
            except Exception:
                error_message = "owner source is unreadable"
                owner_snapshot_cache[owner_path] = (None, error_message)
                return (
                    issue_path, None,
                    (_issue(issue_path, 0, "KIN-E-QUOTE", error_message),),
                )
            read_cache[owner_path] = raw

        try:
            owner_view = _build_owner_view(raw)
        except Exception:
            error_message = "owner source cannot be indexed"
            owner_snapshot_cache[owner_path] = (None, error_message)
            return (
                issue_path, None,
                (_issue(issue_path, 0, "KIN-E-QUOTE", error_message),),
            )
        owner_snapshot_cache[owner_path] = (owner_view, None)
        return issue_path, owner_view, ()

    if ledger_path is not None:
        try:
            candidate = Path(ledger_path)
            if candidate.is_absolute():
                resolved_ledger = candidate.resolve(strict=False)
                resolved_ledger.relative_to(resolved_root)
            else:
                resolved_ledger = safe_repo_path(
                    resolved_root, candidate.as_posix()
                )
        except Exception:
            issues.append(_issue(
                str(ledger_path), 0, "KIN-E-LEDGER", "ledger path is unsafe"
            ))
        else:
            ledger_payload = read_path(resolved_ledger, candidate.as_posix())
            if ledger_payload is not None:
                issues.extend(synchronize_ledger_markdown(
                    ledger_payload, seams, path=candidate.as_posix()
                ).issues)

    target_attempt_ids = {
        artifact.get("attemptId")
        for artifact in artifacts
        if isinstance(artifact.get("attemptId"), str)
        and artifact.get("reviewTargetSha256") is not None
    }
    for receipt in receipts:
        receipt_path = receipt.get("path")
        payload = read_declared(receipt_path, "phaseReceipt.path")
        if payload is None:
            continue
        target_frozen = (
            receipt.get("status") in {"COMPLETE", "VERIFIED"}
            or receipt.get("reviewAttemptId") in target_attempt_ids
        )
        issues.extend(synchronize_receipt_markdown(
            payload,
            receipt,
            path=receipt_path,
            target_frozen=target_frozen,
        ).issues)

    finding_by_id = _record_index(
        findings, label="reviewFindings", code="KIN-E-LEDGER", issues=issues
    )
    for attestation in attestations:
        attestation_path = attestation.get("path")
        payload = read_declared(attestation_path, "reviewAttestation.path")
        if payload is None:
            continue
        requested_ids = attestation.get("findingIds")
        resolved_findings: list[Mapping[str, Any]] = []
        if not isinstance(requested_ids, Sequence) or isinstance(
            requested_ids, (str, bytes, bytearray)
        ):
            issues.append(_issue(
                attestation_path, 0, "KIN-E-LEDGER",
                "review attestation findingIds must be a sequence",
            ))
        else:
            for finding_id in requested_ids:
                if not isinstance(finding_id, str):
                    issues.append(_issue(
                        attestation_path, 0, "KIN-E-LEDGER",
                        "review attestation finding id must be a string",
                    ))
                    continue
                finding = finding_by_id.get(finding_id)
                if finding is None:
                    issues.append(_issue(
                        attestation_path, 0, "KIN-E-LEDGER",
                        f"review finding is not present in core: {finding_id}",
                    ))
                else:
                    resolved_findings.append(finding)
        issues.extend(synchronize_review_markdown(
            payload,
            attestation,
            resolved_findings,
            path=attestation_path,
        ).issues)

    source_by_id = _record_index(
        sources, label="sources", code="KIN-E-QUOTE", issues=issues
    )
    claim_by_id = _record_index(
        claims, label="claims", code="KIN-E-QUOTE", issues=issues
    )
    seams_by_claim: dict[str, list[Mapping[str, Any]]] = {}
    for seam in seams:
        claim_id = seam.get("claimId")
        if not isinstance(claim_id, str):
            issues.append(_issue(
                "core.seams", 0, "KIN-E-QUOTE", "seam claimId must be a string"
            ))
            continue
        seams_by_claim.setdefault(claim_id, []).append(seam)

    for claim_id in sorted(seams_by_claim):
        claim_seams = seams_by_claim[claim_id]
        referenced_prior_ids: set[str] = set()
        for seam in claim_seams:
            prior_ids = seam.get("priorSeamIds", ())
            if not isinstance(prior_ids, Sequence) or isinstance(
                prior_ids, (str, bytes, bytearray)
            ):
                issues.append(_issue(
                    "core.seams", 0, "KIN-E-QUOTE",
                    "seam priorSeamIds must be a sequence",
                ))
                continue
            referenced_prior_ids.update(
                prior_id for prior_id in prior_ids if isinstance(prior_id, str)
            )
        leaves = [
            seam for seam in claim_seams
            if isinstance(seam.get("id"), str)
            and seam.get("id") not in referenced_prior_ids
        ]
        if len(leaves) != 1:
            issues.append(_issue(
                f"claim.{claim_id}", 0, "KIN-E-QUOTE",
                "claim must have exactly one current leaf seam",
            ))
            continue
        leaf = leaves[0]
        leaf_id = leaf.get("id")
        matching_trials = trials_by_seam_id.get(leaf_id, [])
        if len(matching_trials) != 1:
            issues.append(_issue(
                f"seam.{leaf_id}", 0, "KIN-E-QUOTE",
                "current leaf seam must have exactly one trial",
            ))
            continue
        claim = claim_by_id.get(claim_id)
        source_id = leaf.get("ownerSource")
        source = source_by_id.get(source_id) if isinstance(source_id, str) else None
        if claim is None or source is None:
            issues.append(_issue(
                f"seam.{leaf_id}", 0, "KIN-E-QUOTE",
                "current leaf seam owner references are unresolved",
            ))
            continue
        issue_path, owner_view, owner_issues = read_owner_snapshot(source)
        issues.extend(owner_issues)
        if owner_view is None:
            continue
        issues.extend(_synchronize_owner_view(
            owner_view, issue_path, source, claim, matching_trials[0], leaf
        ))

    return sorted(set(issues))


def validate_markdown_sync(
    root: Path, core: dict[str, object], ledger_path: Path | None
) -> list[Issue]:
    try:
        return _validate_markdown_sync(root, core, ledger_path)
    except Exception:
        return [_issue(
            "<markdown-sync>", 0, "KIN-E-LEDGER",
            "Markdown synchronization could not classify malformed input",
        )]


__all__ = [
    "FenceRecord",
    "LedgerPreamble",
    "LedgerSection",
    "LedgerSynchronization",
    "MarkdownSynchronization",
    "ReceiptSynchronization",
    "extract_fenced_json",
    "framed_narrative_hash",
    "project_review_seam",
    "synchronize_ledger_markdown",
    "synchronize_owner",
    "synchronize_public_queue_markdown",
    "synchronize_receipt_markdown",
    "synchronize_review_markdown",
    "validate_markdown_sync",
]
