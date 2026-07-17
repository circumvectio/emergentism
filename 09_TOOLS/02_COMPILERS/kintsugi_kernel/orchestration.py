from __future__ import annotations

from pathlib import Path
from typing import cast

from .codec import load_canonical_json
from .diagnostics import Issue, KintsugiError
from .manifest import validate_manifest
from .markdown import validate_markdown_sync
from .schema import load_schema, validate_schema_instance
from .semantics import validate_core_records, validate_public_queue
from .review import validate_review_history


def _ordered(issues: list[Issue]) -> list[Issue]:
    return sorted(issues)


def _validate_arguments(
    *,
    phase: str | None,
    bootstrap: bool,
    base_ref: str | None,
    canonical_root: Path | None,
    public_queue_path: Path | None,
) -> None:
    if phase not in {None, "A", "B", "C"}:
        raise KintsugiError("KIN-E-CLI", "phase", "phase must be A, B, or C")
    if bootstrap and phase != "A":
        raise KintsugiError(
            "KIN-E-CLI", "bootstrap", "bootstrap is permitted only for Phase A"
        )
    if phase is None:
        if base_ref is not None or canonical_root is not None:
            raise KintsugiError(
                "KIN-E-CLI",
                "phase",
                "base ref and canonical root require a selected phase",
            )
        return
    if not isinstance(base_ref, str) or not base_ref:
        raise KintsugiError(
            "KIN-E-CLI", "base-ref", "a non-empty base ref is required for a phase check"
        )
    if canonical_root is None:
        raise KintsugiError(
            "KIN-E-CLI", "canonical-root", "canonical root is required for a phase check"
        )
    if phase == "C" and public_queue_path is None:
        raise KintsugiError(
            "KIN-E-CLI",
            "public-queue",
            "a public queue is required for a Phase C check",
        )


def _load_canonical_input(path: Path) -> object:
    try:
        return load_canonical_json(path)
    except RecursionError:
        raise KintsugiError(
            "KIN-E-JSON",
            str(path),
            "JSON exceeds the supported nesting depth",
        ) from None
    except UnicodeError:
        raise KintsugiError(
            "KIN-E-CANONICAL",
            str(path),
            "JSON contains a string that cannot be encoded as canonical UTF-8",
        ) from None
    except ValueError:
        raise KintsugiError(
            "KIN-E-JSON",
            str(path),
            "JSON value exceeds the supported decoder limits",
        ) from None


def validate_inputs(
    *,
    root: Path,
    data_path: Path,
    schema_path: Path,
    ledger_path: Path | None,
    phase: str | None = None,
    bootstrap: bool = False,
    base_ref: str | None = None,
    canonical_root: Path | None = None,
    public_queue_path: Path | None = None,
) -> list[Issue]:
    """Validate A0B inputs in dependency order without modifying any input."""

    _validate_arguments(
        phase=phase,
        bootstrap=bootstrap,
        base_ref=base_ref,
        canonical_root=canonical_root,
        public_queue_path=public_queue_path,
    )

    schema = load_schema(schema_path)
    core_value = _load_canonical_input(data_path)

    issues = _ordered(validate_schema_instance(schema, "coreData", core_value))
    if issues:
        return issues
    core = cast(dict[str, object], core_value)

    issues = _ordered(validate_core_records(core, phase=phase, bootstrap=bootstrap))
    if issues:
        return issues

    issues = _ordered(validate_review_history(core))
    if issues:
        return issues

    issues = _ordered(validate_markdown_sync(root, core, ledger_path))
    if issues:
        return issues

    if phase is not None:
        # The argument boundary above proves both values are present here.
        checked_root = cast(Path, canonical_root)
        checked_ref = cast(str, base_ref)
        issues = _ordered(
            validate_manifest(root, checked_root, core, phase, checked_ref)
        )
        if issues:
            return issues

    if public_queue_path is not None:
        queue_value = _load_canonical_input(public_queue_path)
        issues = _ordered(
            validate_schema_instance(schema, "publicQueue", queue_value)
        )
        if issues:
            return issues
        queue = cast(dict[str, object], queue_value)
        issues = _ordered(validate_public_queue(queue, core))
        if issues:
            return issues

    return []


__all__ = ["validate_inputs"]
