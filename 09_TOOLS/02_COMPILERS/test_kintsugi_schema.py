from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kintsugi_kernel as kernel
import kintsugi_test_support as support
import validate_kintsugi as facade


ROOT = Path(__file__).resolve().parents[2]
COMPILER = Path(__file__).resolve().parent
TEST_VALIDATE_HASH = "9ca7f87ba8f37f7648bea7ac961e0cea1dcc85441ad4fde16a7ef457c296738a"
BASELINE_CONTRACT_HASH = "74496df660f0ca989f293c30db652b8f9aeb78beb30fa91fe249d87ee29ef69b"
SCHEMA_HASH = "f8c4205af97635f8eea9f83cbf3a1e05ff50a0f64bc6ee8dd54ff61f6df78a3f"
SCHEMA_ID = "https://emergentism.org/schema/kintsugi/1.0.0"
SCHEMA_PATH = ROOT / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
PLAN_PATH = ROOT / "docs/superpowers/plans/2026-07-12-kintsugi-a0b-machine-kernel-implementation.md"
ROOT_ROLES = {"coreData", "publicQueue", "baselineAllowlist"}
REVIEW_HISTORY = {
    "reviewAttempts",
    "reviewAttemptArtifacts",
    "reviewAttestations",
    "reviewFindings",
    "reviewFindingDispositions",
}


def appendix_bytes() -> bytes:
    plan = PLAN_PATH.read_bytes()
    start = plan.rfind(b"\n```json\n") + len(b"\n```json\n")
    end = plan.index(b"```", start)
    return plan[start:end]


def schema_value() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def walk_schemas(node):
    if not isinstance(node, dict):
        return
    yield node
    for key, value in node.items():
        if key in {"$defs", "properties"}:
            for child in value.values():
                yield from walk_schemas(child)
        elif isinstance(value, dict):
            yield from walk_schemas(value)
        elif isinstance(value, list):
            for child in value:
                yield from walk_schemas(child)


def schema_keyword_set(node) -> set[str]:
    result: set[str] = set()

    def visit(value, *, name_map=False):
        if isinstance(value, dict):
            for key, child in value.items():
                if not name_map:
                    result.add(key)
                visit(child, name_map=key in {"$defs", "properties"})
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(node)
    return result


class SchemaAssertions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = schema_value()

    def assertValidRoot(self, role, value):
        self.assertEqual(kernel.validate_schema_instance(self.schema, role, value), ())

    def assertValidDef(self, name, value):
        self.assertEqual(kernel.validate_named_definition(self.schema, name, value), ())

    def assertSchemaFailure(self, issues):
        self.assertTrue(issues)
        self.assertTrue(all(issue.code in {"KIN-E-SCHEMA", "KIN-E-SCHEMA-KEYWORD"} for issue in issues))
        self.assertEqual(tuple(sorted(issues)), issues)


class CompatibilityExtractionTests(unittest.TestCase):
    def test_frozen_a0_inputs_remain_byte_identical(self):
        expected = {
            "test_validate_kintsugi.py": TEST_VALIDATE_HASH,
            "kintsugi_baseline_failures.json": BASELINE_CONTRACT_HASH,
        }
        actual = {
            name: hashlib.sha256((COMPILER / name).read_bytes()).hexdigest()
            for name in expected
        }
        self.assertEqual(actual, expected)

    def test_package_and_facade_share_the_a0_compatibility_surface(self):
        names = (
            "Issue",
            "BaselineResult",
            "KintsugiError",
            "ROOT",
            "DEFAULT_CONTRACT",
            "HASH_RE",
            "FAILED_RE",
            "ERROR_RE",
            "EXCEPTION_RE",
            "BASELINE_COMMAND",
            "COLLECT_COMMAND",
            "EXIT_TWO_CODES",
            "PYTEST_ENV",
            "canonical_json_bytes",
            "raw_hash",
            "normalize_lf",
            "text_hash",
            "safe_repo_path",
            "load_contract",
            "validate_contract",
            "run_process",
            "parse_collected_nodes",
            "parse_failed_nodes",
            "parse_failed_node_lines",
            "parse_pytest_evidence",
            "infer_exception",
            "parse_pytest_failures",
            "parse_pytest_errors",
            "compare_baseline",
            "run_baseline",
        )
        for name in names:
            with self.subTest(name=name):
                self.assertIs(getattr(facade, name), getattr(kernel, name))

    def test_package_and_facade_share_the_schema_surface(self):
        for name in (
            "SCHEMA_ID",
            "ROOT_ROLES",
            "SCHEMA_KEYWORDS",
            "load_schema",
            "validate_schema_document",
            "validate_schema_instance",
            "validate_named_definition",
        ):
            with self.subTest(name=name):
                self.assertIs(getattr(facade, name), getattr(kernel, name))

    def test_facade_parser_retains_a0_flags_and_defaults(self):
        args = facade.build_parser().parse_args(["--check-baseline"])
        self.assertTrue(args.check_baseline)
        self.assertEqual(args.contract, facade.DEFAULT_CONTRACT)
        self.assertEqual(args.canonical_root, facade.ROOT)

    def test_facade_main_retains_a0_success_output_and_exit(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        result = facade.BaselineResult(19, 5, ())
        with mock.patch.object(facade, "run_baseline", return_value=result):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = facade.main([
                    "--check-baseline",
                    "--canonical-root",
                    str(ROOT),
                ])
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), "KIN-OK baseline collected=19 failures=5\n")
        self.assertEqual(stderr.getvalue(), "")


class FrozenSchemaArtifactTests(SchemaAssertions):
    def test_appendix_and_artifact_are_exact_canonical_bytes(self):
        payload = SCHEMA_PATH.read_bytes()
        self.assertEqual(payload, appendix_bytes())
        self.assertEqual(hashlib.sha256(payload).hexdigest(), SCHEMA_HASH)
        self.assertEqual(len(payload.splitlines()), 1)
        self.assertTrue(payload.endswith(b"\n"))
        self.assertEqual(payload, kernel.canonical_json_bytes(json.loads(payload)))
        self.assertNotIn(b"PLACEHOLDER", payload)
        self.assertNotIn(b"APPENDIX_MARKER", payload)
        self.assertNotIn(b"TODO", payload)

    def test_schema_identity_roots_and_local_references_are_closed(self):
        self.assertEqual(self.schema["$id"], SCHEMA_ID)
        self.assertEqual(kernel.SCHEMA_ID, SCHEMA_ID)
        self.assertEqual(set(kernel.ROOT_ROLES), ROOT_ROLES)
        self.assertGreater(len(self.schema["$defs"]), 3)
        self.assertTrue(ROOT_ROLES < set(self.schema["$defs"]))
        for node in walk_schemas(self.schema):
            if "$ref" in node:
                self.assertTrue(node["$ref"].startswith("#/$defs/"), node["$ref"])

    def test_declared_keyword_vocabulary_is_exactly_consumed(self):
        self.assertEqual(schema_keyword_set(self.schema), set(kernel.SCHEMA_KEYWORDS))
        self.assertEqual(kernel.validate_schema_document(self.schema), ())

    def test_every_declared_object_is_closed(self):
        objects = [node for node in walk_schemas(self.schema) if node.get("type") == "object"]
        self.assertTrue(objects)
        for node in objects:
            self.assertIs(node.get("additionalProperties"), False)

    def test_unknown_keyword_and_unresolved_or_remote_refs_fail_closed(self):
        unknown = copy.deepcopy(self.schema)
        unknown["$defs"]["text"]["format"] = "invented"
        self.assertSchemaFailure(kernel.validate_schema_document(unknown))

        missing = copy.deepcopy(self.schema)
        missing["$defs"]["text"] = {"$ref": "#/$defs/ABSENT"}
        self.assertSchemaFailure(kernel.validate_schema_document(missing))

        remote = copy.deepcopy(self.schema)
        remote["$defs"]["text"] = {"$ref": "https://example.invalid/schema"}
        self.assertSchemaFailure(kernel.validate_schema_document(remote))

    def test_schema_document_validation_is_total_over_malformed_shapes(self):
        malformed = [None, True, 1, "schema", [], {}, {"$defs": []}, {"$defs": {"x": 1}}]
        for value in malformed:
            with self.subTest(value=repr(value)):
                self.assertSchemaFailure(kernel.validate_schema_document(value))

    def test_overflowing_pattern_quantifier_fails_with_typed_schema_diagnostic(self):
        overflowing = copy.deepcopy(self.schema)
        overflowing["$defs"]["overflowPattern"] = {
            "type": "string",
            "pattern": "a{999999999999999999999999999999}",
        }

        issues = kernel.validate_schema_document(overflowing)
        self.assertSchemaFailure(issues)
        self.assertEqual(issues[0].code, "KIN-E-SCHEMA-KEYWORD")
        self.assertEqual(issues[0].path, "$.$defs.overflowPattern.pattern")

        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "overflow-schema.json"
            schema_path.write_bytes(kernel.canonical_json_bytes(overflowing))
            with self.assertRaises(kernel.KintsugiError) as caught:
                kernel.load_schema(schema_path)
        self.assertEqual(caught.exception.code, "KIN-E-SCHEMA-KEYWORD")
        self.assertEqual(caught.exception.path, "$.$defs.overflowPattern.pattern")

    def test_deeply_nested_pattern_fails_with_typed_schema_diagnostic(self):
        nested = copy.deepcopy(self.schema)
        nested["$defs"]["deepPattern"] = {
            "type": "string",
            "pattern": "(" * 500 + "a" + ")" * 500,
        }

        issues = kernel.validate_schema_document(nested)
        self.assertSchemaFailure(issues)
        self.assertEqual(issues[0].code, "KIN-E-SCHEMA-KEYWORD")
        self.assertEqual(issues[0].path, "$.$defs.deepPattern.pattern")

        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "deep-pattern-schema.json"
            schema_path.write_bytes(kernel.canonical_json_bytes(nested))
            with self.assertRaises(kernel.KintsugiError) as caught:
                kernel.load_schema(schema_path)
        self.assertEqual(caught.exception.code, "KIN-E-SCHEMA-KEYWORD")
        self.assertEqual(caught.exception.path, "$.$defs.deepPattern.pattern")

    def test_const_and_enum_literal_ref_keys_are_not_schema_edges(self):
        literal_refs = copy.deepcopy(self.schema)
        literal_refs["$defs"].update({
            "literalConst": {"const": {"$ref": "#/$defs/literalConst"}},
            "literalEnum": {"enum": [{"$ref": "#/$defs/literalEnum"}]},
        })

        self.assertEqual(kernel.validate_schema_document(literal_refs), ())
        self.assertEqual(
            kernel.validate_named_definition(
                literal_refs, "literalConst", {"$ref": "#/$defs/literalConst"}
            ),
            (),
        )
        self.assertEqual(
            kernel.validate_named_definition(
                literal_refs, "literalEnum", {"$ref": "#/$defs/literalEnum"}
            ),
            (),
        )

    def test_local_refs_resolve_only_to_declared_subschema_locations(self):
        referenced = copy.deepcopy(self.schema)
        referenced["$defs"].update({
            "allContainer": {"allOf": [{"type": "string"}]},
            "allTarget": {"$ref": "#/$defs/allContainer/allOf/0"},
            "anyContainer": {"anyOf": [{"type": "string"}]},
            "anyTarget": {"$ref": "#/$defs/anyContainer/anyOf/0"},
            "oneContainer": {"oneOf": [{"type": "string"}]},
            "oneTarget": {"$ref": "#/$defs/oneContainer/oneOf/0"},
            "itemsContainer": {"items": {"type": "string"}},
            "itemsTarget": {"$ref": "#/$defs/itemsContainer/items"},
            "nestedDefsContainer": {
                "$defs": {"inner": {"type": "string"}},
            },
            "nestedDefsTarget": {
                "$ref": "#/$defs/nestedDefsContainer/$defs/inner",
            },
            "conditionalContainer": {
                "if": {"type": "string"},
                "then": {"type": "string"},
                "else": {"type": "string"},
            },
            "ifTarget": {"$ref": "#/$defs/conditionalContainer/if"},
            "thenTarget": {"$ref": "#/$defs/conditionalContainer/then"},
            "elseTarget": {"$ref": "#/$defs/conditionalContainer/else"},
            "escapedContainer": {
                "properties": {"p/q~r": {"type": "string"}},
            },
            "escapedTarget": {
                "$ref": "#/$defs/escapedContainer/properties/p~1q~0r",
            },
        })

        self.assertEqual(kernel.validate_schema_document(referenced), ())
        for name in (
            "allTarget",
            "anyTarget",
            "oneTarget",
            "itemsTarget",
            "nestedDefsTarget",
            "ifTarget",
            "thenTarget",
            "elseTarget",
            "escapedTarget",
        ):
            with self.subTest(name=name):
                self.assertEqual(
                    kernel.validate_named_definition(referenced, name, "valid"), ()
                )
                self.assertSchemaFailure(
                    kernel.validate_named_definition(referenced, name, 1)
                )

        for token in ("00", "٠"):
            with self.subTest(array_token=token):
                invalid_index = copy.deepcopy(referenced)
                invalid_index["$defs"]["badIndex"] = {
                    "$ref": f"#/$defs/allContainer/allOf/{token}",
                }
                self.assertSchemaFailure(
                    kernel.validate_schema_document(invalid_index)
                )

    def test_refs_cannot_reinterpret_const_or_enum_data_as_subschemas(self):
        for name, literal, reference in (
            (
                "literalConst",
                {"const": {"payload": {"format": "forbidden"}}},
                "#/$defs/literalConst/const/payload",
            ),
            (
                "literalEnum",
                {"enum": [{"payload": {"format": "forbidden"}}]},
                "#/$defs/literalEnum/enum/0/payload",
            ),
        ):
            with self.subTest(name=name):
                opaque = copy.deepcopy(self.schema)
                opaque["$defs"].update({
                    name: literal,
                    "smuggled": {"$ref": reference},
                })
                issues = kernel.validate_schema_document(opaque)
                self.assertSchemaFailure(issues)
                self.assertTrue(any("unresolved $ref" in issue.message for issue in issues))
                self.assertSchemaFailure(
                    kernel.validate_named_definition(opaque, "smuggled", None)
                )

    def test_nested_pointer_self_cycle_is_rejected(self):
        cyclic = copy.deepcopy(self.schema)
        cyclic["$defs"]["nestedCycle"] = {
            "properties": {
                "x": {"$ref": "#/$defs/nestedCycle/properties/x"},
            },
        }

        issues = kernel.validate_schema_document(cyclic)
        self.assertSchemaFailure(issues)
        self.assertTrue(any("cyclic $ref chain" in issue.message for issue in issues))

    def test_thousand_definition_acyclic_ref_chain_is_total(self):
        chain = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": kernel.SCHEMA_ID,
            "$defs": {},
        }
        for index in range(1000):
            chain["$defs"][f"x{index}"] = (
                {"$ref": f"#/$defs/x{index + 1}"}
                if index < 999
                else {"type": "null"}
            )

        self.assertEqual(kernel.validate_schema_document(chain), ())
        self.assertEqual(kernel.validate_named_definition(chain, "x0", None), ())
        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "long-ref-chain.json"
            schema_path.write_bytes(kernel.canonical_json_bytes(chain))
            self.assertEqual(kernel.load_schema(schema_path), chain)

    def test_thousand_definition_ref_chain_with_siblings_is_iterative_and_conjunctive(self):
        chain = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": kernel.SCHEMA_ID,
            "$defs": {},
        }
        for index in range(1000):
            chain["$defs"][f"x{index}"] = (
                {"$ref": f"#/$defs/x{index + 1}", "const": None}
                if index < 999
                else {"type": "null", "const": None}
            )

        self.assertEqual(kernel.validate_schema_document(chain), ())
        self.assertEqual(kernel.validate_named_definition(chain, "x0", None), ())
        issues = kernel.validate_named_definition(chain, "x0", False)
        self.assertSchemaFailure(issues)
        self.assertTrue(any(issue.message == "value does not equal const" for issue in issues))
        self.assertTrue(any("expected null" in issue.message for issue in issues))

    def test_uri_fragment_percent_decoding_is_utf8_strict_and_pointer_aware(self):
        referenced = copy.deepcopy(self.schema)
        referenced["$defs"].update({
            "a b": {"type": "string"},
            "café": {"type": "integer"},
            "a/b": {"type": "boolean"},
            "spaceTarget": {"$ref": "#/$defs/a%20b"},
            "utf8Target": {"$ref": "#/$defs/caf%C3%A9"},
            "pointerTarget": {"$ref": "#/$defs/a%7E1b"},
        })

        self.assertEqual(kernel.validate_schema_document(referenced), ())
        for name, valid, invalid in (
            ("spaceTarget", "ok", 1),
            ("utf8Target", 1, "no"),
            ("pointerTarget", True, 1),
        ):
            with self.subTest(name=name):
                self.assertEqual(
                    kernel.validate_named_definition(referenced, name, valid), ()
                )
                self.assertSchemaFailure(
                    kernel.validate_named_definition(referenced, name, invalid)
                )

        for fragment in ("%", "%2", "%GG", "%FF", "%C3%28"):
            with self.subTest(malformed_fragment=fragment):
                malformed = copy.deepcopy(referenced)
                malformed["$defs"]["badFragment"] = {
                    "$ref": f"#/$defs/{fragment}",
                }
                issues = kernel.validate_schema_document(malformed)
                self.assertSchemaFailure(issues)
                self.assertTrue(any("$ref" in issue.path for issue in issues))

    def test_nested_resource_identifiers_and_dialects_are_rejected(self):
        for keyword, value in (
            ("$id", "nested-resource"),
            ("$schema", self.schema["$schema"]),
        ):
            with self.subTest(keyword=keyword):
                nested = copy.deepcopy(self.schema)
                nested["$defs"]["nestedResource"] = {
                    keyword: value,
                    "type": "string",
                }
                issues = kernel.validate_schema_document(nested)
                self.assertSchemaFailure(issues)
                self.assertIn(
                    kernel.Issue(
                        f"$.$defs.nestedResource.{keyword}",
                        "KIN-E-SCHEMA-KEYWORD",
                        f"nested {keyword} is unsupported in the single-resource evaluator",
                    ),
                    issues,
                )

        root_only = {
            "$schema": self.schema["$schema"],
            "$id": kernel.SCHEMA_ID,
            "$defs": {"x": {"type": "string"}},
        }
        self.assertEqual(kernel.validate_schema_document(root_only), ())

    def test_large_integer_decoder_value_error_is_typed_and_stable(self):
        payload = (
            b'{"$defs":{"x":{"minimum":' + b'1' * 5000
            + b'}},"$id":"https://emergentism.org/schema/kintsugi/1.0.0",'
              b'"$schema":"https://json-schema.org/draft/2020-12/schema"}\n'
        )

        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "large-integer-schema.json"
            schema_path.write_bytes(payload)
            failures = []
            for _ in range(2):
                with self.assertRaises(kernel.KintsugiError) as caught:
                    kernel.load_schema(schema_path)
                failures.append((
                    caught.exception.code,
                    caught.exception.path,
                    caught.exception.message,
                ))
        self.assertEqual(failures[0], failures[1])
        self.assertEqual(
            failures[0],
            (
                "KIN-E-JSON",
                str(schema_path),
                "JSON value exceeds the supported decoder limits",
            ),
        )

    def test_deep_json_load_failure_is_typed_and_stable(self):
        payload = (
            b'{"$defs":{"x":{"const":' + b'[' * 1000 + b'null' + b']' * 1000
            + b'}},"$id":"https://emergentism.org/schema/kintsugi/1.0.0",'
              b'"$schema":"https://json-schema.org/draft/2020-12/schema"}\n'
        )

        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "deep-schema.json"
            schema_path.write_bytes(payload)
            for _ in range(2):
                with self.assertRaises(kernel.KintsugiError) as caught:
                    kernel.load_schema(schema_path)
                self.assertIn(caught.exception.code, {"KIN-E-JSON", "KIN-E-CANONICAL"})
                self.assertEqual(caught.exception.path, str(schema_path))
                self.assertEqual(
                    caught.exception.message,
                    "JSON exceeds the supported nesting depth",
                )

    def test_escaped_lone_surrogate_fails_with_typed_canonical_diagnostic(self):
        payload = (
            b'{"$defs":{"x":{"const":"\\ud800"}},'
            b'"$id":"https://emergentism.org/schema/kintsugi/1.0.0",'
            b'"$schema":"https://json-schema.org/draft/2020-12/schema"}\n'
        )

        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "lone-surrogate-schema.json"
            schema_path.write_bytes(payload)
            with self.assertRaises(kernel.KintsugiError) as caught:
                kernel.load_schema(schema_path)
        self.assertEqual(caught.exception.code, "KIN-E-CANONICAL")
        self.assertEqual(caught.exception.path, str(schema_path))


class RestrictedEvaluatorTests(SchemaAssertions):
    def test_all_three_complete_synthetic_roots_validate_and_are_fresh(self):
        builders = {
            "coreData": support.build_core_data,
            "publicQueue": support.build_public_queue,
            "baselineAllowlist": support.build_baseline_allowlist,
        }
        for role, builder in builders.items():
            with self.subTest(role=role):
                first = builder()
                second = builder()
                self.assertIsNot(first, second)
                self.assertEqual(first, second)
                self.assertValidRoot(role, first)
                first.clear()
                self.assertNotEqual(first, second)

    def test_cli_role_selection_rejects_every_nested_definition(self):
        self.assertValidDef("reviewProcessEvidence", support.build_review_process_evidence())
        issues = kernel.validate_schema_instance(
            self.schema, "reviewProcessEvidence", support.build_review_process_evidence()
        )
        self.assertSchemaFailure(issues)

    def test_boolean_is_not_an_integer_and_values_are_never_coerced(self):
        for value in (True, False, "1", 1.0, None):
            with self.subTest(value=value):
                self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "count", value))
        self.assertValidDef("count", 1)
        self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "text", 1))
        self.assertValidDef("text", "1")

    def test_one_of_requires_exactly_one_matching_branch(self):
        ambiguous = copy.deepcopy(self.schema)
        ambiguous["$defs"]["ambiguous"] = {"oneOf": [{}, {}]}
        self.assertEqual(kernel.validate_schema_document(ambiguous), ())
        self.assertSchemaFailure(kernel.validate_named_definition(ambiguous, "ambiguous", {}))
        self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "upgradeCriterion", {}))

    def test_max_length_counts_unicode_code_points(self):
        bounded = copy.deepcopy(self.schema)
        bounded["$defs"]["boundedText"] = {"type": "string", "maxLength": 2}
        self.assertEqual(kernel.validate_schema_document(bounded), ())
        self.assertValidDef("text", "é🙂")
        self.assertEqual(kernel.validate_named_definition(bounded, "boundedText", "é🙂"), ())
        self.assertSchemaFailure(
            kernel.validate_named_definition(bounded, "boundedText", "é🙂x")
        )

    def test_extra_properties_and_duplicate_array_items_fail(self):
        queue = support.build_public_queue()
        queue["smuggled"] = True
        self.assertSchemaFailure(kernel.validate_schema_instance(self.schema, "publicQueue", queue))

        duplicate = support.build_core_data()
        duplicate["manifests"][0]["harvestedClaimIds"].append(support.CLAIM_ID)
        self.assertSchemaFailure(kernel.validate_schema_instance(self.schema, "coreData", duplicate))

    def test_json_numeric_equality_applies_to_const_enum_and_unique_items(self):
        numeric = copy.deepcopy(self.schema)
        numeric["$defs"].update({
            "numericConst": {"const": 1},
            "numericEnum": {"enum": [1]},
            "numericUnique": {"type": "array", "uniqueItems": True},
        })
        self.assertEqual(kernel.validate_schema_document(numeric), ())

        self.assertEqual(kernel.validate_named_definition(numeric, "numericConst", 1.0), ())
        self.assertEqual(kernel.validate_named_definition(numeric, "numericEnum", 1.0), ())
        self.assertSchemaFailure(
            kernel.validate_named_definition(numeric, "numericUnique", [1, 1.0])
        )

        self.assertSchemaFailure(kernel.validate_named_definition(numeric, "numericConst", True))
        self.assertSchemaFailure(kernel.validate_named_definition(numeric, "numericEnum", True))
        self.assertEqual(
            kernel.validate_named_definition(numeric, "numericUnique", [1, True]), ()
        )

        duplicate_enum = copy.deepcopy(numeric)
        duplicate_enum["$defs"]["numericEnum"]["enum"] = [1, 1.0]
        self.assertSchemaFailure(kernel.validate_schema_document(duplicate_enum))

    def test_deep_const_equality_is_iterative(self):
        expected = None
        for _ in range(400):
            expected = [expected]
        deep_const = copy.deepcopy(self.schema)
        deep_const["$defs"]["deepConst"] = {"const": expected}

        self.assertEqual(kernel.validate_schema_document(deep_const), ())
        self.assertEqual(
            kernel.validate_named_definition(
                deep_const, "deepConst", copy.deepcopy(expected)
            ),
            (),
        )
        different = False
        for _ in range(400):
            different = [different]
        self.assertSchemaFailure(
            kernel.validate_named_definition(deep_const, "deepConst", different)
        )

    def test_instance_validation_is_total_and_sorted(self):
        malformed = [None, True, 1, "instance", [], {}, {"schemaVersion": 1}, {"x": object()}]
        for role in sorted(ROOT_ROLES):
            for value in malformed:
                with self.subTest(role=role, value=repr(value)):
                    self.assertSchemaFailure(kernel.validate_schema_instance(self.schema, role, value))


class FrozenContractShapeTests(SchemaAssertions):
    def test_claim_and_seam_contracts_have_the_pre_v1_fields(self):
        defs = self.schema["$defs"]
        self.assertEqual(
            set(defs["typedTerm"]["required"]),
            {"symbol", "type", "definition", "semanticRegister"},
        )
        self.assertIn("role", defs["premise"]["required"])
        claim_fields = {
            "supportLinks",
            "upgradeCriterion",
            "killCriterion",
            "survivingIfKilled",
            "authorityScope",
            "authorityEffect",
        }
        self.assertTrue(claim_fields <= set(defs["claim"]["required"]))
        seam_fields = {
            "priorSupportLinks",
            "priorUpgradeCriterion",
            "priorKillCriterion",
            "priorSurvivingIfKilled",
            "supportLinks",
            "upgradeCriterion",
            "killCriterion",
            "survivingIfKilled",
        }
        self.assertTrue(seam_fields <= set(defs["seam"]["required"]))
        self.assertIn("upgradeEvidenceLinkIds", defs["seam"]["properties"])
        self.assertNotIn("upgradeEvidenceLinkIds", defs["seam"]["required"])
        self.assertIn("upgradeEvidenceLinkIds", json.dumps(defs["seam"]["allOf"], sort_keys=True))

    def test_manifest_queue_fixture_and_authority_shapes_are_typed(self):
        defs = self.schema["$defs"]
        self.assertEqual(defs["manifest"]["properties"]["requiredClaimBindings"]["maxItems"], 7)
        self.assertEqual(
            len(defs["requiredClaimBinding"]["properties"]["requirementId"]["enum"]), 7
        )
        self.assertEqual(
            set(defs["ownerSearchEvidence"]["required"]),
            {"manifestIds", "searchedSourceIds", "method", "result"},
        )
        self.assertIn("mutationLevel", defs["fixture"]["required"])
        self.assertEqual(
            set(defs["authority"]["properties"]["mechanism"]["enum"]),
            {
                "NONE",
                "K2_NATURAL_PERSON",
                "PRISM_PUBLIC_GOVERNANCE",
                "CONSTITUTIONAL_AUTO_ENFORCEMENT",
                "OTHER",
            },
        )

    def test_phase_a_requires_seven_bindings_and_b_c_require_empty(self):
        for phase in ("A", "B", "C"):
            manifest = support.build_core_data()["manifests"][0]
            manifest["phase"] = phase
            manifest["requiredClaimBindings"] = (
                copy.deepcopy(support.REQUIRED_PHASE_A_BINDINGS) if phase == "A" else []
            )
            self.assertValidDef("manifest", manifest)
            broken = copy.deepcopy(manifest)
            if phase == "A":
                broken["requiredClaimBindings"].pop()
            else:
                broken["requiredClaimBindings"] = copy.deepcopy(support.REQUIRED_PHASE_A_BINDINGS[:1])
            self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "manifest", broken))

    def test_semantic_payload_registry_is_closed_and_complete(self):
        payloads = support.build_semantic_payloads()
        self.assertEqual(
            set(payloads),
            {
                "verdictMatrixPayload",
                "justiceContextPayload",
                "receiptRolePayload",
                "registerIndexPayload",
                "quantumMeasurePayload",
                "optionConePayload",
                "trophicAggregatorPayload",
                "rosettaTransferPayload",
            },
        )
        for name, payload in payloads.items():
            with self.subTest(name=name):
                self.assertValidDef(name, payload)
                payload["smuggled"] = True
                self.assertSchemaFailure(kernel.validate_named_definition(self.schema, name, payload))

    def test_review_and_bundle_history_fields_are_complete(self):
        defs = self.schema["$defs"]
        core_reviews = {name for name in defs["coreData"]["required"] if name.startswith("review")}
        bundle_reviews = {name for name in defs["validationBundle"]["required"] if name in REVIEW_HISTORY}
        self.assertEqual(core_reviews, REVIEW_HISTORY)
        self.assertEqual(bundle_reviews, REVIEW_HISTORY)
        target_required = set(defs["reviewTarget"]["required"])
        self.assertTrue({
            "currentAttemptId",
            "receiptId",
            "receiptNarrativeRawSha256",
            "reviewSubjectDigest",
            "ledgerPreambleRawSha256",
            "priorReviewAttempts",
            "priorReviewAttemptArtifacts",
            "priorReviewAttestations",
            "priorReviewFindings",
            "priorReviewFindingDispositions",
        } <= target_required)
        self.assertTrue({"receiptNarrativeRawSha256", "ledgerPreambleRawSha256"} <= set(
            defs["validationBundle"]["required"]
        ))
        for name in (
            "reviewAttempt",
            "reviewAttemptArtifact",
            "reviewAttestation",
            "reviewFinding",
            "reviewProcessEvidence",
            "reviewFindingDisposition",
            "reviewFindingDispositionInput",
            "reviewTarget",
            "receiptDescriptor",
            "validationBundle",
        ):
            self.assertIn(name, defs)

    def test_stale_contract_forms_are_absent(self):
        defs = self.schema["$defs"]
        all_property_names = {
            name
            for node in walk_schemas(self.schema)
            for name in node.get("properties", {})
        }
        self.assertNotIn("requiredClaimIds", all_property_names)
        self.assertNotIn("sourceIds", defs["supportLink"]["properties"])
        self.assertNotEqual(defs["killCriterion"].get("type"), "string")
        self.assertGreater(len(defs), 3)


class ReviewRecordStructuralTests(SchemaAssertions):
    def test_record_builders_validate_and_one_field_removals_fail(self):
        records = {
            "reviewAttempt": support.build_review_attempt(),
            "reviewAttemptArtifact": support.build_review_attempt_artifact(),
            "reviewAttestation": support.build_review_attestation(),
            "reviewFinding": support.build_review_finding(),
            "reviewProcessEvidence": support.build_review_process_evidence(),
            "reviewFindingDisposition": support.build_review_finding_disposition(),
            "reviewFindingDispositionInput": support.build_review_finding_disposition_input(),
            "reviewTarget": support.build_review_target(),
            "receiptDescriptor": support.build_receipt_descriptor(),
            "validationBundle": support.build_validation_bundle(),
        }
        for name, record in records.items():
            with self.subTest(name=name):
                self.assertValidDef(name, record)
                broken = copy.deepcopy(record)
                del broken[self.schema["$defs"][name]["required"][0]]
                self.assertSchemaFailure(kernel.validate_named_definition(self.schema, name, broken))

    def test_attempt_id_and_status_cardinalities(self):
        valid_ids = ["RVA-A-001", "RVA-B-010", "RVA-C-999", "RVA-A-1000"]
        invalid_ids = ["RVA-A-000", "RVA-A-0001", "RVA-A-01", "RVA-D-001", "RVA-A--001"]
        for attempt_id in valid_ids:
            record = support.build_review_attempt()
            record["id"] = attempt_id
            self.assertValidDef("reviewAttempt", record)
        for attempt_id in invalid_ids:
            record = support.build_review_attempt()
            record["id"] = attempt_id
            self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "reviewAttempt", record))

        variants = [
            ("PENDING", None, None, True),
            ("PENDING", "ATT-L", None, True),
            ("PENDING", None, "ATT-B", True),
            ("PENDING", "ATT-L", "ATT-B", False),
            ("FAILED", "ATT-L", None, True),
            ("FAILED", None, "ATT-B", True),
            ("FAILED", "ATT-L", "ATT-B", True),
            ("FAILED", None, None, False),
            ("PASSED", "ATT-L", "ATT-B", True),
            ("PASSED", "ATT-L", None, False),
            ("ABANDONED", None, None, True),
            ("ABANDONED", "ATT-L", None, True),
            ("ABANDONED", "ATT-L", "ATT-B", True),
        ]
        for status, logic_id, btj_id, valid in variants:
            with self.subTest(status=status, logic=logic_id, btj=btj_id):
                record = support.build_review_attempt(
                    status, logic_attestation_id=logic_id, btj_attestation_id=btj_id
                )
                issues = kernel.validate_named_definition(self.schema, "reviewAttempt", record)
                self.assertEqual(not issues, valid, issues)

        abandoned = support.build_review_attempt("ABANDONED")
        abandoned["abandonReason"] = None
        self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "reviewAttempt", abandoned))

    def test_attestation_pass_and_fail_shapes(self):
        self.assertValidDef("reviewAttestation", support.build_review_attestation("LOGIC", "PASS"))
        self.assertValidDef("reviewAttestation", support.build_review_attestation("LOGIC", "FAIL"))

        bad_pass = support.build_review_attestation("LOGIC", "PASS")
        bad_pass["openSevereFindingIds"] = ["FND-B-001"]
        self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "reviewAttestation", bad_pass))

        for field in ("findingIds", "openSevereFindingIds"):
            bad_fail = support.build_review_attestation("LOGIC", "FAIL")
            bad_fail[field] = []
            self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "reviewAttestation", bad_fail))

    def test_disposition_tagged_unions_and_typed_endpoints(self):
        for disposition in ("ADDRESSED", "DISPUTED", "PROCESS_INVALID"):
            with self.subTest(disposition=disposition):
                record = support.build_review_finding_disposition(disposition)
                self.assertValidDef("reviewFindingDisposition", record)
                self.assertEqual(
                    set(record) & {"claimIds", "seamIds", "ledgerSectionIds", "receiptIds", "subjectPaths"},
                    {"claimIds", "seamIds", "ledgerSectionIds", "receiptIds", "subjectPaths"},
                )
                empty = support.build_review_finding_disposition(disposition, include_ids=False)
                self.assertSchemaFailure(
                    kernel.validate_named_definition(self.schema, "reviewFindingDisposition", empty)
                )

        process = support.build_review_finding_disposition("PROCESS_INVALID")
        del process["evidenceFiles"][0]["sha256"]
        self.assertSchemaFailure(kernel.validate_named_definition(self.schema, "reviewFindingDisposition", process))


class BootstrapCardinalityTests(SchemaAssertions):
    def test_core_schema_permits_honest_empty_trial_arrays(self):
        core = support.build_core_data()
        core["trials"] = []
        core["manifests"][0]["trialedClaimIds"] = []
        core["manifests"][0]["trialedClaimCount"] = 0
        core["phaseReceipts"][0]["trialIds"] = []
        self.assertValidRoot("coreData", core)

    def test_review_target_and_bundle_require_non_empty_trials(self):
        for name, builder in (
            ("reviewTarget", support.build_review_target),
            ("validationBundle", support.build_validation_bundle),
        ):
            record = builder()
            self.assertValidDef(name, record)
            record["trials"] = []
            self.assertSchemaFailure(kernel.validate_named_definition(self.schema, name, record))

    def test_manifest_permits_empty_or_nonempty_final_and_empty_closure(self):
        manifest = support.build_core_data()["manifests"][0]
        self.assertValidDef("manifest", manifest)
        manifest["finalFiles"] = []
        manifest["finalFileCount"] = 0
        manifest["closureOnlyPaths"] = []
        self.assertValidDef("manifest", manifest)


if __name__ == "__main__":
    unittest.main()
