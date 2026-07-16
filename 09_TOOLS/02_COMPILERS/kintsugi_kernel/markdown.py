from __future__ import annotations

import copy
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .codec import normalize_lf, raw_hash, safe_repo_path, text_hash
from .diagnostics import Issue, KintsugiError


_NARRATIVE_DOMAIN = b"KINTSUGI-NARRATIVE-V1\x00"
_MAX_UINT64 = (1 << 64) - 1
_MAX_JSON_DEPTH = 512
_JSON_FENCE_MARKER = b"```json"
_FENCE_PREFIX = b"```json "
_KNOWN_ROLES = frozenset({
    "kintsugi-seam",
    "kintsugi-receipt",
    "kintsugi-review",
    "kintsugi-review-findings",
    "kintsugi-public-queue",
})
_DYNAMIC_RECEIPT_PREFIXES = (
    "status:",
    "review status:",
    "review target:",
    "review target digest:",
    "review attempt:",
    "logic review:",
    "btj review:",
    "validation bundle:",
    "validation digest:",
    "truth gate:",
    "beauty gate:",
    "justice gate:",
    "digest:",
    "reviewer path:",
    "bundle:",
    "gate:",
    "reviewtargetdigest:",
    "logicreviewpath:",
    "btjreviewpath:",
    "validationbundlepath:",
    "validationdigest:",
    "reviewattemptid:",
    "reviewerpath:",
    "truthgate:",
    "beautygate:",
    "justicegate:",
)
_DYNAMIC_RECEIPT_COMPACT_FIELDS = frozenset({
    "receiptstatus",
    "reviewtargetdigest",
    "logicreviewpath",
    "logicreviewerpath",
    "btjreviewpath",
    "btjreviewerpath",
    "validationbundle",
    "validationbundlepath",
    "validationdigest",
    "reviewattemptid",
    "reviewerpath",
    "truthgate",
    "beautygate",
    "justicegate",
    "gatestatus",
})
_DYNAMIC_REVIEW_OUTCOMES = frozenset({
    "pass", "passed", "fail", "failed", "pending", "abandoned",
    "complete", "verified",
})
_DYNAMIC_RECEIPT_STATES = frozenset({"draft", "complete", "verified"})
_DYNAMIC_REVIEW_SUBJECTS = frozenset({
    "review", "gate", "logic", "btj", "truth", "beauty", "justice",
})
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


def _scan_fences(payload: bytes, path: str) -> tuple[tuple[FenceRecord, ...], list[Issue]]:
    lines = _lines(payload)
    records: list[FenceRecord] = []
    issues: list[Issue] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.content.startswith(_FENCE_PREFIX):
            if line.content.lower().startswith(_JSON_FENCE_MARKER):
                issues.append(_issue(
                    path, line.start, "KIN-E-LEDGER",
                    "malformed JSON fence opener",
                ))
                closer_index = index + 1
                while (
                    closer_index < len(lines)
                    and lines[closer_index].content != b"```"
                ):
                    closer_index += 1
                if closer_index >= len(lines):
                    issues.append(_issue(
                        path, line.start, "KIN-E-LEDGER",
                        "unterminated malformed JSON fence",
                    ))
                    break
                index = closer_index + 1
                continue
            index += 1
            continue
        raw_role = line.content[len(_FENCE_PREFIX):]
        try:
            role = raw_role.decode("ascii", errors="strict")
        except UnicodeDecodeError:
            role = raw_role.decode("ascii", errors="replace")
        closer_index = index + 1
        while closer_index < len(lines) and lines[closer_index].content != b"```":
            closer_index += 1
        if closer_index >= len(lines):
            issues.append(_issue(path, line.start, "KIN-E-LEDGER", f"unterminated {role} fence"))
            records.append(FenceRecord(
                role, line.start, line.end, len(payload), len(payload), len(payload), None, False,
            ))
            break
        closer = lines[closer_index]
        raw_json = payload[line.end:closer.start]
        value, json_issues = _json_value(raw_json, path=path, offset=line.end)
        issues.extend(json_issues)
        records.append(FenceRecord(
            role, line.start, line.end, closer.start, closer.start, closer.end,
            value, not json_issues,
        ))
        index = closer_index + 1
    return tuple(records), issues


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
    lines = _lines(payload)
    headings: list[tuple[str, int]] = []
    seen_heading_ids: set[str] = set()
    for line in lines:
        heading_id = _heading_id(line.content)
        if heading_id is None:
            continue
        headings.append((heading_id, line.start))
        if heading_id in seen_heading_ids:
            issues.append(_issue(path, line.start, "KIN-E-LEDGER", f"duplicate seam heading: {heading_id}"))
        seen_heading_ids.add(heading_id)

    records, fence_issues = _scan_fences(payload, path)
    issues.extend(fence_issues)
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


def _dynamic_receipt_issues(raw: bytes, *, base: int, path: str) -> list[Issue]:
    issues: list[Issue] = []
    for line in _lines(raw):
        try:
            text = line.content.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            continue
        normalized = text.strip().casefold()
        while normalized and normalized[0] in "#-*`> ":
            normalized = normalized[1:].lstrip()
        normalized = normalized.replace("**", "").replace("`", "")
        compact = "".join(character for character in normalized if character.isalnum())
        words = {
            word for word in "".join(
                character if character.isalnum() else " "
                for character in normalized
            ).split()
        }
        first_word = next(iter(
            "".join(
                character if character.isalnum() else " "
                for character in normalized
            ).split()
        ), "")
        is_dynamic = (
            any(normalized.startswith(prefix) for prefix in _DYNAMIC_RECEIPT_PREFIXES)
            or any(field in compact for field in _DYNAMIC_RECEIPT_COMPACT_FIELDS)
            or "status" in words
            or "digest" in words
            or ({"validation", "bundle"} <= words)
            or ({"bundle", "path"} <= words)
            or ({"reviewer", "path"} <= words)
            or ({"review", "path"} <= words)
            or ("review" in words and bool(words & _DYNAMIC_REVIEW_OUTCOMES))
            or ("gate" in words and (
                "status" in words or bool(words & _DYNAMIC_REVIEW_OUTCOMES)
            ))
            or (
                bool(words & _DYNAMIC_REVIEW_SUBJECTS)
                and bool(words & _DYNAMIC_REVIEW_OUTCOMES)
            )
            or (
                bool(words & _DYNAMIC_REVIEW_SUBJECTS)
                and {"signed", "off"} <= words
            )
            or (
                bool(words & _DYNAMIC_RECEIPT_STATES)
                and bool(words & {"receipt", "phase"})
            )
            or first_word in {"bundle", "gate"}
        )
        if is_dynamic:
            issues.append(_issue(
                path, base + line.start, "KIN-E-LEDGER",
                "dynamic receipt prose is forbidden outside the fence after target freeze",
            ))
    return issues


def _occurs_exactly_once(text: str, quote: str) -> bool:
    if not quote:
        return False
    first = text.find(quote)
    return first >= 0 and text.find(quote, first + 1) < 0


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
        issues.extend(_dynamic_receipt_issues(prefix, base=0, path=path))
        suffix_base = selected.end if selected is not None else len(prefix)
        issues.extend(_dynamic_receipt_issues(suffix, base=suffix_base, path=path))
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
    except TypeError:
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
    except OSError as exc:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", f"owner repository root is unavailable: {exc}"),)
    except ValueError as exc:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", f"owner source path is invalid: {exc}"),)
    if not owner_path.is_file():
        return (_issue(issue_path, 0, "KIN-E-QUOTE", "owner source does not exist as a file"),)
    try:
        raw = owner_path.read_bytes()
    except OSError as exc:
        return (_issue(issue_path, 0, "KIN-E-QUOTE", f"owner source is unreadable: {exc}"),)

    if source.get("kind") != "OWNER" or source.get("authorityRole") != "SEMANTIC_OWNER":
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "declared source is not a semantic owner"))
    if source.get("sha256") != raw_hash(raw):
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

    try:
        owner_text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        issues.append(_issue(issue_path, exc.start, "KIN-E-QUOTE", "owner source is not strict UTF-8"))
        return _ordered(issues)
    normalized_owner = normalize_lf(owner_text)
    anchor = seam.get("ownerAnchor")
    if not isinstance(anchor, str) or normalize_lf(anchor) not in normalized_owner:
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "owner anchor is absent"))
    after_quote = seam.get("afterQuote")
    if seam.get("status") not in _ONE_SIDED_SEAM_STATUSES and (
        not isinstance(after_quote, str)
        or not _occurs_exactly_once(normalized_owner, normalize_lf(after_quote))
    ):
        issues.append(_issue(issue_path, 0, "KIN-E-QUOTE", "afterQuote must appear exactly once in the owner source"))
    return _ordered(issues)


__all__ = [
    "FenceRecord",
    "LedgerPreamble",
    "LedgerSection",
    "LedgerSynchronization",
    "MarkdownSynchronization",
    "ReceiptSynchronization",
    "framed_narrative_hash",
    "project_review_seam",
    "synchronize_ledger_markdown",
    "synchronize_owner",
    "synchronize_public_queue_markdown",
    "synchronize_receipt_markdown",
    "synchronize_review_markdown",
]
