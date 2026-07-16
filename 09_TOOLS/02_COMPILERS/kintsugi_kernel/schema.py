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
    pending = [(left, right)]
    compared_containers: set[tuple[int, int]] = set()
    while pending:
        current_left, current_right = pending.pop()
        if type(current_left) in (int, float) and type(current_right) in (int, float):
            try:
                if not bool(current_left == current_right):
                    return False
            except Exception:
                if current_left is not current_right:
                    return False
            continue
        if type(current_left) is not type(current_right):
            return False
        if isinstance(current_left, dict):
            if set(current_left) != set(current_right):
                return False
            pair = (id(current_left), id(current_right))
            if pair in compared_containers:
                continue
            compared_containers.add(pair)
            pending.extend(
                (current_left[key], current_right[key]) for key in current_left
            )
            continue
        if isinstance(current_left, list):
            if len(current_left) != len(current_right):
                return False
            pair = (id(current_left), id(current_right))
            if pair in compared_containers:
                continue
            compared_containers.add(pair)
            pending.extend(zip(current_left, current_right))
            continue
        try:
            if not bool(current_left == current_right):
                return False
        except Exception:
            if current_left is not current_right:
                return False
    return True


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


def _decode_uri_fragment(fragment: str) -> str | None:
    payload = bytearray()
    index = 0
    while index < len(fragment):
        character = fragment[index]
        if character == "%":
            if index + 2 >= len(fragment):
                return None
            encoded = fragment[index + 1:index + 3]
            if any(digit not in "0123456789abcdefABCDEF" for digit in encoded):
                return None
            payload.append(int(encoded, 16))
            index += 3
            continue
        try:
            payload.extend(character.encode("utf-8"))
        except UnicodeEncodeError:
            return None
        index += 1
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError:
        return None


_NAMED_SUBSCHEMA_KEYWORDS = ("$defs", "properties")
_SINGLE_SUBSCHEMA_KEYWORDS = ("items", "if", "then", "else")
_ARRAY_SUBSCHEMA_KEYWORDS = ("allOf", "anyOf", "oneOf")
_SAME_INSTANCE_SINGLE_KEYWORDS = ("if", "then", "else")
_SAME_INSTANCE_ARRAY_KEYWORDS = ("allOf", "anyOf", "oneOf")
_SchemaLocation = tuple[str, ...]


def _schema_locations(root: dict[str, Any]) -> dict[_SchemaLocation, dict[str, Any]]:
    locations: dict[_SchemaLocation, dict[str, Any]] = {}
    pending: list[tuple[_SchemaLocation, Any, frozenset[int]]] = [
        ((), root, frozenset())
    ]
    while pending:
        location, node, ancestors = pending.pop()
        if not isinstance(node, dict):
            continue
        locations[location] = node
        if id(node) in ancestors:
            continue
        next_ancestors = ancestors | {id(node)}

        for keyword in _NAMED_SUBSCHEMA_KEYWORDS:
            children = node.get(keyword)
            if not isinstance(children, dict):
                continue
            for name, child in reversed(tuple(children.items())):
                if isinstance(name, str) and isinstance(child, dict):
                    pending.append((location + (keyword, name), child, next_ancestors))

        for keyword in _SINGLE_SUBSCHEMA_KEYWORDS:
            child = node.get(keyword)
            if isinstance(child, dict):
                pending.append((location + (keyword,), child, next_ancestors))

        for keyword in _ARRAY_SUBSCHEMA_KEYWORDS:
            children = node.get(keyword)
            if not isinstance(children, list):
                continue
            for index in range(len(children) - 1, -1, -1):
                child = children[index]
                if isinstance(child, dict):
                    pending.append((
                        location + (keyword, str(index)), child, next_ancestors
                    ))
    return locations


def _pointer_tokens(reference: Any) -> _SchemaLocation | None:
    if not isinstance(reference, str) or not reference.startswith("#"):
        return None
    pointer = _decode_uri_fragment(reference[1:])
    if pointer is None or not pointer.startswith("/"):
        return None
    tokens: list[str] = []
    for raw_token in pointer[1:].split("/"):
        token = _decode_pointer_token(raw_token)
        if token is None:
            return None
        tokens.append(token)
    return tuple(tokens)


def _array_index(token: str, length: int) -> int | None:
    if not token or (token != "0" and token[0] == "0"):
        return None
    index = 0
    for character in token:
        if character not in "0123456789":
            return None
        index = index * 10 + ord(character) - ord("0")
        if index >= length:
            return None
    return index


def _resolve_ref_location(
    root: dict[str, Any],
    reference: Any,
    locations: dict[_SchemaLocation, dict[str, Any]] | None = None,
) -> tuple[_SchemaLocation, dict[str, Any]] | None:
    tokens = _pointer_tokens(reference)
    if tokens is None:
        return None
    current: Any = root
    for token in tokens:
        if isinstance(current, dict):
            if token not in current:
                return None
            current = current[token]
            continue
        if isinstance(current, list):
            index = _array_index(token, len(current))
            if index is None:
                return None
            current = current[index]
            continue
        return None
    schema_locations = locations if locations is not None else _schema_locations(root)
    target = schema_locations.get(tokens)
    if target is None or target is not current:
        return None
    return tokens, target


def _resolve_ref(
    root: dict[str, Any],
    reference: Any,
    locations: dict[_SchemaLocation, dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    resolved = _resolve_ref_location(root, reference, locations)
    return resolved[1] if resolved is not None else None


def _schema_shape_issues(
    node: Any,
    root: dict[str, Any],
    path: str,
    *,
    ancestors: frozenset[int],
    locations: dict[_SchemaLocation, dict[str, Any]],
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

    if path != "$":
        for keyword in ("$id", "$schema"):
            if keyword in node:
                issues.append(_issue(
                    _child(path, keyword),
                    f"nested {keyword} is unsupported in the single-resource evaluator",
                    keyword=True,
                ))

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
                    definition, root, definition_path, ancestors=next_ancestors,
                    locations=locations,
                ))

    if "$ref" in node:
        reference = node["$ref"]
        tokens = _pointer_tokens(reference)
        if tokens is None or len(tokens) < 2 or tokens[0] != "$defs":
            issues.append(_issue(_child(path, "$ref"), "$ref must be a local #/$defs pointer", keyword=True))
        elif _resolve_ref(root, reference, locations) is None:
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
                    definition, root, property_path, ancestors=next_ancestors,
                    locations=locations,
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
            except Exception as exc:
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
            node["items"], root, _child(path, "items"), ancestors=next_ancestors,
            locations=locations,
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
                branch, root, _item(_child(path, keyword), index),
                ancestors=next_ancestors, locations=locations,
            ))

    for keyword in ("if", "then", "else"):
        if keyword in node:
            issues.extend(_schema_shape_issues(
                node[keyword], root, _child(path, keyword),
                ancestors=next_ancestors, locations=locations,
            ))
    if ("then" in node or "else" in node) and "if" not in node:
        issues.append(_issue(path, "then/else requires if", keyword=True))

    return issues


def _location_path(location: _SchemaLocation) -> str:
    result = "$"
    for index, token in enumerate(location):
        if index and location[index - 1] in _ARRAY_SUBSCHEMA_KEYWORDS and token.isdigit():
            result += f"[{token}]"
        else:
            result += f".{token}"
    return result


def _evaluation_cycle_issues(
    schema: dict[str, Any],
    locations: dict[_SchemaLocation, dict[str, Any]],
) -> list[Issue]:
    graph: dict[_SchemaLocation, set[_SchemaLocation]] = {
        location: set() for location in locations
    }
    for location, node in locations.items():
        if "$ref" in node:
            resolved = _resolve_ref_location(schema, node["$ref"], locations)
            if resolved is not None:
                graph[location].add(resolved[0])

        for keyword in _SAME_INSTANCE_SINGLE_KEYWORDS:
            child = location + (keyword,)
            if child in locations:
                graph[location].add(child)

        for keyword in _SAME_INSTANCE_ARRAY_KEYWORDS:
            branches = node.get(keyword)
            if not isinstance(branches, list):
                continue
            for index in range(len(branches)):
                child = location + (keyword, str(index))
                if child in locations:
                    graph[location].add(child)

    state: dict[_SchemaLocation, int] = {}
    issues: list[Issue] = []
    for start in sorted(graph):
        if state.get(start, 0) != 0:
            continue
        state[start] = 1
        active = [start]
        active_indexes = {start: 0}
        stack: list[tuple[_SchemaLocation, Any]] = [
            (start, iter(sorted(graph[start])))
        ]
        while stack:
            current, targets = stack[-1]
            try:
                target = next(targets)
            except StopIteration:
                stack.pop()
                state[current] = 2
                active_indexes.pop(current, None)
                active.pop()
                continue
            target_state = state.get(target, 0)
            if target_state == 0:
                state[target] = 1
                active_indexes[target] = len(active)
                active.append(target)
                stack.append((target, iter(sorted(graph[target]))))
                continue
            if target_state == 1:
                cycle = active[active_indexes[target]:] + [target]
                issues.append(_issue(
                    _location_path(target),
                    "cyclic $ref chain: "
                    + " -> ".join(_location_path(location) for location in cycle),
                    keyword=True,
                ))
    return issues


def _validate_schema_document(schema: Any) -> tuple[Issue, ...]:
    if not isinstance(schema, dict):
        return (_issue("$", "schema document must be an object", keyword=True),)
    issues: list[Issue] = []
    if schema.get("$schema") != SCHEMA_DIALECT:
        issues.append(_issue("$.$schema", f"$schema must equal {SCHEMA_DIALECT}", keyword=True))
    if schema.get("$id") != SCHEMA_ID:
        issues.append(_issue("$.$id", f"$id must equal {SCHEMA_ID}", keyword=True))
    if not isinstance(schema.get("$defs"), dict) or not schema.get("$defs"):
        issues.append(_issue("$.$defs", "$defs must be a non-empty object", keyword=True))
    locations = _schema_locations(schema)
    issues.extend(_schema_shape_issues(
        schema, schema, "$", ancestors=frozenset(), locations=locations
    ))
    if not issues:
        issues.extend(_evaluation_cycle_issues(schema, locations))
    return _ordered(issues)


def validate_schema_document(schema: object) -> list[Issue]:
    try:
        return list(_validate_schema_document(schema))
    except RecursionError:
        return [_issue(
            "$",
            "schema exceeds the supported nesting or evaluation depth",
            keyword=True,
        )]


def load_schema(path: Path) -> dict[str, Any]:
    try:
        value = load_canonical_value(path)
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
    locations: dict[_SchemaLocation, dict[str, Any]],
) -> list[Issue]:
    issues: list[Issue] = []
    while "$ref" in schema:
        pair = (id(schema), id(instance))
        if pair in stack:
            return [_issue(path, "cyclic instance/schema evaluation")]
        target = _resolve_ref(root, schema["$ref"], locations)
        if target is None:
            return [_issue(
                path, f"unresolved $ref: {schema['$ref']}", keyword=True
            )]
        stack = stack | {pair}
        sibling_schema = {
            keyword: value
            for keyword, value in schema.items()
            if keyword != "$ref"
        }
        if sibling_schema:
            issues.extend(_evaluate(
                sibling_schema, instance, root, path,
                stack=stack, locations=locations,
            ))
        schema = target

    pair = (id(schema), id(instance))
    if pair in stack:
        return [_issue(path, "cyclic instance/schema evaluation")]
    next_stack = stack | {pair}

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
                    properties[key], instance[key], root, _child(path, key),
                    stack=next_stack, locations=locations,
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
                    schema["items"], value, root, _item(path, index),
                    stack=next_stack, locations=locations,
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
            issues.extend(_evaluate(
                branch, instance, root, path, stack=next_stack,
                locations=locations,
            ))

    if "anyOf" in schema:
        matches = sum(
            not _evaluate(
                branch, instance, root, path, stack=next_stack,
                locations=locations,
            )
            for branch in schema["anyOf"]
        )
        if matches == 0:
            issues.append(_issue(path, "value matches no anyOf branch"))

    if "oneOf" in schema:
        matches = sum(
            not _evaluate(
                branch, instance, root, path, stack=next_stack,
                locations=locations,
            )
            for branch in schema["oneOf"]
        )
        if matches != 1:
            issues.append(_issue(path, f"value matches {matches} oneOf branches; expected exactly one"))

    if "if" in schema:
        condition_matches = not _evaluate(
            schema["if"], instance, root, path, stack=next_stack,
            locations=locations,
        )
        selected = schema.get("then") if condition_matches else schema.get("else")
        if selected is not None:
            issues.extend(_evaluate(
                selected, instance, root, path, stack=next_stack,
                locations=locations,
            ))

    return issues


def _validate_definition(schema: Any, name: str, instance: Any) -> tuple[Issue, ...]:
    schema_issues = tuple(validate_schema_document(schema))
    if schema_issues:
        return schema_issues
    assert isinstance(schema, dict)
    definitions = schema["$defs"]
    if not isinstance(name, str) or name not in definitions:
        return (_issue("definition", f"unknown schema definition: {name}"),)
    try:
        return _ordered(_evaluate(
            definitions[name], instance, schema, "$", stack=frozenset(),
            locations=_schema_locations(schema),
        ))
    except RecursionError:
        return (_issue(
            "$",
            "instance/schema exceeds the supported nesting or evaluation depth",
        ),)


def validate_schema_instance(
    schema: dict[str, object], root_role: str, instance: object
) -> list[Issue]:
    schema_issues = validate_schema_document(schema)
    if schema_issues:
        return schema_issues
    if root_role not in ROOT_ROLES:
        return [_issue("role", f"unsupported root role: {root_role}")]
    return list(_validate_definition(schema, root_role, instance))


def validate_named_definition(
    schema: dict[str, object], def_name: str, instance: object
) -> list[Issue]:
    return list(_validate_definition(schema, def_name, instance))
