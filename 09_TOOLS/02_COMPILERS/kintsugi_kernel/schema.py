from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

from .codec import load_canonical_value
from .diagnostics import Issue, KintsugiError


SCHEMA_ID = "https://emergentism.org/schema/kintsugi/1.0.0"
SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"
ROOT_ROLES = ("coreData", "publicQueue", "baselineAllowlist")
SCHEMA_KEYWORDS = frozenset({
    "$schema",
    "$id",
    "$defs",
    "$ref",
    "type",
    "required",
    "properties",
    "additionalProperties",
    "enum",
    "pattern",
    "minimum",
    "minLength",
    "maxLength",
    "minItems",
    "maxItems",
    "items",
    "uniqueItems",
    "const",
    "allOf",
    "anyOf",
    "oneOf",
    "if",
    "then",
    "else",
})
JSON_TYPES = frozenset({"object", "array", "string", "integer", "boolean", "null"})
_SCHEMA_CODE = "KIN-E-SCHEMA"
_KEYWORD_CODE = "KIN-E-SCHEMA-KEYWORD"


def _issue(path: str, message: str, *, keyword: bool = False) -> Issue:
    return Issue(path, _KEYWORD_CODE if keyword else _SCHEMA_CODE, message)


def _ordered(issues: Iterable[Issue]) -> tuple[Issue, ...]:
    return tuple(sorted(set(issues), key=lambda item: (item.path, item.code, item.message)))


def _child(path: str, key: str) -> str:
    return f"{path}.{key}"


def _item(path: str, index: int) -> str:
    return f"{path}[{index}]"


def _json_equal(left: Any, right: Any) -> bool:
    if type(left) in (int, float) and type(right) in (int, float):
        try:
            return bool(left == right)
        except Exception:
            return left is right
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(_json_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_json_equal(a, b) for a, b in zip(left, right))
    try:
        return bool(left == right)
    except Exception:
        return left is right


def _is_nonnegative_integer(value: Any) -> bool:
    return type(value) is int and value >= 0


def _decode_pointer_token(token: str) -> str | None:
    result: list[str] = []
    index = 0
    while index < len(token):
        if token[index] != "~":
            result.append(token[index])
            index += 1
            continue
        if index + 1 >= len(token) or token[index + 1] not in "01":
            return None
        result.append("~" if token[index + 1] == "0" else "/")
        index += 2
    return "".join(result)


def _resolve_ref(root: dict[str, Any], reference: Any) -> dict[str, Any] | None:
    if not isinstance(reference, str) or not reference.startswith("#/"):
        return None
    current: Any = root
    for raw_token in reference[2:].split("/"):
        token = _decode_pointer_token(raw_token)
        if token is None or not isinstance(current, dict) or token not in current:
            return None
        current = current[token]
    return current if isinstance(current, dict) else None


def _schema_shape_issues(
    node: Any,
    root: dict[str, Any],
    path: str,
    *,
    ancestors: frozenset[int],
) -> list[Issue]:
    if not isinstance(node, dict):
        return [_issue(path, "schema node must be an object", keyword=True)]
    if id(node) in ancestors:
        return [_issue(path, "schema object graph is cyclic", keyword=True)]
    next_ancestors = ancestors | {id(node)}
    issues: list[Issue] = []

    for key in node:
        if key not in SCHEMA_KEYWORDS:
            issues.append(_issue(_child(path, key), f"unknown schema keyword: {key}", keyword=True))

    if "$schema" in node and not isinstance(node["$schema"], str):
        issues.append(_issue(_child(path, "$schema"), "$schema must be a string", keyword=True))
    if "$id" in node and not isinstance(node["$id"], str):
        issues.append(_issue(_child(path, "$id"), "$id must be a string", keyword=True))

    definitions = node.get("$defs")
    if "$defs" in node:
        if not isinstance(definitions, dict):
            issues.append(_issue(_child(path, "$defs"), "$defs must be an object", keyword=True))
        else:
            for name, definition in definitions.items():
                definition_path = _child(_child(path, "$defs"), str(name))
                if not isinstance(name, str) or not name:
                    issues.append(_issue(definition_path, "definition name must be a non-empty string", keyword=True))
                issues.extend(_schema_shape_issues(
                    definition, root, definition_path, ancestors=next_ancestors
                ))

    if "$ref" in node:
        reference = node["$ref"]
        if not isinstance(reference, str) or not reference.startswith("#/$defs/"):
            issues.append(_issue(_child(path, "$ref"), "$ref must be a local #/$defs pointer", keyword=True))
        elif _resolve_ref(root, reference) is None:
            issues.append(_issue(_child(path, "$ref"), f"unresolved $ref: {reference}", keyword=True))

    if "type" in node and (not isinstance(node["type"], str) or node["type"] not in JSON_TYPES):
        issues.append(_issue(_child(path, "type"), "type must name one supported JSON type", keyword=True))

    required = node.get("required")
    if "required" in node:
        if (
            not isinstance(required, list)
            or not all(isinstance(item, str) and item for item in required)
            or len(required) != len(set(required))
        ):
            issues.append(_issue(_child(path, "required"), "required must contain unique non-empty strings", keyword=True))

    properties = node.get("properties")
    if "properties" in node:
        if not isinstance(properties, dict):
            issues.append(_issue(_child(path, "properties"), "properties must be an object", keyword=True))
        else:
            for name, definition in properties.items():
                property_path = _child(_child(path, "properties"), str(name))
                if not isinstance(name, str) or not name:
                    issues.append(_issue(property_path, "property name must be a non-empty string", keyword=True))
                issues.extend(_schema_shape_issues(
                    definition, root, property_path, ancestors=next_ancestors
                ))

    if "additionalProperties" in node and type(node["additionalProperties"]) is not bool:
        issues.append(_issue(
            _child(path, "additionalProperties"),
            "additionalProperties must be boolean",
            keyword=True,
        ))

    if "enum" in node:
        enum = node["enum"]
        if not isinstance(enum, list) or not enum:
            issues.append(_issue(_child(path, "enum"), "enum must be a non-empty array", keyword=True))
        elif any(_json_equal(value, prior) for index, value in enumerate(enum) for prior in enum[:index]):
            issues.append(_issue(_child(path, "enum"), "enum values must be unique", keyword=True))

    if "pattern" in node:
        pattern = node["pattern"]
        if not isinstance(pattern, str):
            issues.append(_issue(_child(path, "pattern"), "pattern must be a string", keyword=True))
        else:
            try:
                re.compile(pattern)
            except (re.error, OverflowError) as exc:
                issues.append(_issue(_child(path, "pattern"), f"invalid pattern: {exc}", keyword=True))

    if "minimum" in node and (
        type(node["minimum"]) not in (int, float)
    ):
        issues.append(_issue(_child(path, "minimum"), "minimum must be numeric", keyword=True))

    for keyword in ("minLength", "maxLength", "minItems", "maxItems"):
        if keyword in node and not _is_nonnegative_integer(node[keyword]):
            issues.append(_issue(_child(path, keyword), f"{keyword} must be a non-negative integer", keyword=True))
    for lower, upper in (("minLength", "maxLength"), ("minItems", "maxItems")):
        if (
            _is_nonnegative_integer(node.get(lower))
            and _is_nonnegative_integer(node.get(upper))
            and node[lower] > node[upper]
        ):
            issues.append(_issue(path, f"{lower} cannot exceed {upper}", keyword=True))

    if "items" in node:
        issues.extend(_schema_shape_issues(
            node["items"], root, _child(path, "items"), ancestors=next_ancestors
        ))
    if "uniqueItems" in node and type(node["uniqueItems"]) is not bool:
        issues.append(_issue(_child(path, "uniqueItems"), "uniqueItems must be boolean", keyword=True))

    for keyword in ("allOf", "anyOf", "oneOf"):
        if keyword not in node:
            continue
        branches = node[keyword]
        if not isinstance(branches, list) or not branches:
            issues.append(_issue(_child(path, keyword), f"{keyword} must be a non-empty array", keyword=True))
            continue
        for index, branch in enumerate(branches):
            issues.extend(_schema_shape_issues(
                branch, root, _item(_child(path, keyword), index), ancestors=next_ancestors
            ))

    for keyword in ("if", "then", "else"):
        if keyword in node:
            issues.extend(_schema_shape_issues(
                node[keyword], root, _child(path, keyword), ancestors=next_ancestors
            ))
    if ("then" in node or "else" in node) and "if" not in node:
        issues.append(_issue(path, "then/else requires if", keyword=True))

    return issues


def _definition_ref_graph(schema: dict[str, Any]) -> dict[str, set[str]]:
    definitions = schema.get("$defs")
    if not isinstance(definitions, dict):
        return {}
    graph = {name: set() for name in definitions}

    def collect(node: Any) -> Iterable[str]:
        if isinstance(node, dict):
            reference = node.get("$ref")
            if isinstance(reference, str) and reference.startswith("#/$defs/"):
                token = reference[len("#/$defs/"):]
                if "/" not in token:
                    decoded = _decode_pointer_token(token)
                    if decoded is not None:
                        yield decoded
            for value in node.values():
                yield from collect(value)
        elif isinstance(node, list):
            for value in node:
                yield from collect(value)

    for name, definition in definitions.items():
        graph[name].update(target for target in collect(definition) if target in graph)
    return graph


def _reference_cycle_issues(schema: dict[str, Any]) -> list[Issue]:
    graph = _definition_ref_graph(schema)
    visited: set[str] = set()
    active: list[str] = []
    active_set: set[str] = set()
    issues: list[Issue] = []

    def visit(name: str) -> None:
        if name in active_set:
            cycle = active[active.index(name):] + [name]
            issues.append(_issue(
                f"$.$defs.{name}",
                "cyclic $ref chain: " + " -> ".join(cycle),
                keyword=True,
            ))
            return
        if name in visited:
            return
        visited.add(name)
        active.append(name)
        active_set.add(name)
        for target in sorted(graph[name]):
            visit(target)
        active.pop()
        active_set.remove(name)

    for name in sorted(graph):
        visit(name)
    return issues


def validate_schema_document(schema: Any) -> tuple[Issue, ...]:
    if not isinstance(schema, dict):
        return (_issue("$", "schema document must be an object", keyword=True),)
    issues: list[Issue] = []
    if schema.get("$schema") != SCHEMA_DIALECT:
        issues.append(_issue("$.$schema", f"$schema must equal {SCHEMA_DIALECT}", keyword=True))
    if schema.get("$id") != SCHEMA_ID:
        issues.append(_issue("$.$id", f"$id must equal {SCHEMA_ID}", keyword=True))
    if not isinstance(schema.get("$defs"), dict) or not schema.get("$defs"):
        issues.append(_issue("$.$defs", "$defs must be a non-empty object", keyword=True))
    issues.extend(_schema_shape_issues(schema, schema, "$", ancestors=frozenset()))
    if not issues:
        issues.extend(_reference_cycle_issues(schema))
    return _ordered(issues)


def load_schema(path: Path) -> dict[str, Any]:
    value = load_canonical_value(path)
    issues = validate_schema_document(value)
    if issues:
        first = issues[0]
        raise KintsugiError(first.code, first.path, first.message)
    return value


def _type_matches(expected: str, value: Any) -> bool:
    return {
        "object": type(value) is dict,
        "array": type(value) is list,
        "string": type(value) is str,
        "integer": type(value) is int,
        "boolean": type(value) is bool,
        "null": value is None,
    }[expected]


def _evaluate(
    schema: dict[str, Any],
    instance: Any,
    root: dict[str, Any],
    path: str,
    *,
    stack: frozenset[tuple[int, int]],
) -> list[Issue]:
    pair = (id(schema), id(instance))
    if pair in stack:
        return [_issue(path, "cyclic instance/schema evaluation")]
    next_stack = stack | {pair}
    issues: list[Issue] = []

    if "$ref" in schema:
        target = _resolve_ref(root, schema["$ref"])
        if target is None:
            return [_issue(path, f"unresolved $ref: {schema['$ref']}", keyword=True)]
        issues.extend(_evaluate(target, instance, root, path, stack=next_stack))

    expected_type = schema.get("type")
    type_ok = expected_type is None or _type_matches(expected_type, instance)
    if expected_type is not None and not type_ok:
        issues.append(_issue(path, f"expected {expected_type}; found {type(instance).__name__}"))

    if "const" in schema and not _json_equal(instance, schema["const"]):
        issues.append(_issue(path, "value does not equal const"))
    if "enum" in schema and not any(_json_equal(instance, candidate) for candidate in schema["enum"]):
        issues.append(_issue(path, "value is not in enum"))

    if type(instance) is dict:
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    issues.append(_issue(_child(path, key), "required property is missing"))
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key in sorted(set(instance) & set(properties)):
                issues.extend(_evaluate(
                    properties[key], instance[key], root, _child(path, key), stack=next_stack
                ))
            if schema.get("additionalProperties") is False:
                for key in sorted(set(instance) - set(properties), key=str):
                    issues.append(_issue(_child(path, str(key)), "additional property is forbidden"))

    if type(instance) is list:
        if "minItems" in schema and len(instance) < schema["minItems"]:
            issues.append(_issue(path, f"array has fewer than {schema['minItems']} items"))
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            issues.append(_issue(path, f"array has more than {schema['maxItems']} items"))
        if schema.get("uniqueItems") is True:
            for index, value in enumerate(instance):
                if any(_json_equal(value, prior) for prior in instance[:index]):
                    issues.append(_issue(_item(path, index), "array item is not unique"))
        if "items" in schema:
            for index, value in enumerate(instance):
                issues.extend(_evaluate(
                    schema["items"], value, root, _item(path, index), stack=next_stack
                ))

    if type(instance) is str:
        if "minLength" in schema and len(instance) < schema["minLength"]:
            issues.append(_issue(path, f"string is shorter than {schema['minLength']} code points"))
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            issues.append(_issue(path, f"string is longer than {schema['maxLength']} code points"))
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            issues.append(_issue(path, f"string does not match pattern {schema['pattern']}"))

    if "minimum" in schema and type(instance) in (int, float) and instance < schema["minimum"]:
        issues.append(_issue(path, f"number is less than minimum {schema['minimum']}"))

    for keyword in ("allOf",):
        for branch in schema.get(keyword, []):
            issues.extend(_evaluate(branch, instance, root, path, stack=next_stack))

    if "anyOf" in schema:
        matches = sum(
            not _evaluate(branch, instance, root, path, stack=next_stack)
            for branch in schema["anyOf"]
        )
        if matches == 0:
            issues.append(_issue(path, "value matches no anyOf branch"))

    if "oneOf" in schema:
        matches = sum(
            not _evaluate(branch, instance, root, path, stack=next_stack)
            for branch in schema["oneOf"]
        )
        if matches != 1:
            issues.append(_issue(path, f"value matches {matches} oneOf branches; expected exactly one"))

    if "if" in schema:
        condition_matches = not _evaluate(schema["if"], instance, root, path, stack=next_stack)
        selected = schema.get("then") if condition_matches else schema.get("else")
        if selected is not None:
            issues.extend(_evaluate(selected, instance, root, path, stack=next_stack))

    return issues


def _validate_definition(schema: Any, name: str, instance: Any) -> tuple[Issue, ...]:
    schema_issues = validate_schema_document(schema)
    if schema_issues:
        return schema_issues
    assert isinstance(schema, dict)
    definitions = schema["$defs"]
    if not isinstance(name, str) or name not in definitions:
        return (_issue("definition", f"unknown schema definition: {name}"),)
    return _ordered(_evaluate(definitions[name], instance, schema, "$", stack=frozenset()))


def validate_schema_instance(schema: Any, role: str, instance: Any) -> tuple[Issue, ...]:
    schema_issues = validate_schema_document(schema)
    if schema_issues:
        return schema_issues
    if role not in ROOT_ROLES:
        return (_issue("role", f"unsupported root role: {role}"),)
    return _validate_definition(schema, role, instance)


def validate_named_definition(schema: Any, name: str, instance: Any) -> tuple[Issue, ...]:
    return _validate_definition(schema, name, instance)
