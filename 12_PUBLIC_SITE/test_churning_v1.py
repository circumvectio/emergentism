#!/usr/bin/env python3
"""Contract, custody, generation, and release-boundary tests for Third Churning v1."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
PACKET = ROOT / "14_THE_DISTILLATION" / "07_THE_THIRD_CHURNING_2026_08_23"
DATA = PACKET / "data"
CONTRACTS = {
    "drop": PACKET / "contracts" / "ChurningDrop.v1.schema.json",
    "problem": PACKET / "contracts" / "ProblemAdjudication.v1.schema.json",
    "corpus": PACKET / "contracts" / "ThirdChurningCorpus.v1.schema.json",
}
DROPS_PATH = DATA / "churning_drops.v1.json"
PROBLEMS_PATH = DATA / "problem_adjudications.v1.json"
INVENTORY_PATH = DATA / "paradox_inventory.v1.json"
CORPUS_PATH = PACKET / "ThirdChurningCorpus.v1.json"
ATLAS_PATH = (
    ROOT
    / "03_METHODOLOGY"
    / "03_PREREGISTRATIONS"
    / "pqa_54"
    / "prompts"
    / "questions.json"
)
BUILDER_PATH = SITE / "build_churning.py"
PREDECESSOR_ARCHIVE = ROOT / "90_ARCHIVE" / "2026_08_23_third_churning_predecessors"
PREDECESSOR_MANIFEST = PREDECESSOR_ARCHIVE / "MANIFEST.sha256"
OWNER_DIRECTION = "00_HANDOFF/EMERGENTISM_ORG_V2_3_THIRD_CHURNING_OWNER_DIRECTION_2026_08_23.md"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def safe_relative_path(base: Path, raw: str, *, must_exist: bool = True) -> Path:
    if not isinstance(raw, str) or not raw:
        raise ValueError("path must be a non-empty string")
    pure = PurePosixPath(raw)
    if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != raw:
        raise ValueError(f"unsafe relative path: {raw!r}")
    candidate = base / Path(*pure.parts)
    resolved_base = base.resolve()
    resolved = candidate.resolve(strict=must_exist)
    try:
        resolved.relative_to(resolved_base)
    except ValueError as exc:
        raise ValueError(f"path escapes its root: {raw!r}") from exc
    return resolved


class VisibleTextParser(HTMLParser):
    """Collect static semantic text while excluding hidden/script-only carriers."""

    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._hidden_stack: list[tuple[str, bool]] = []
        self._hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        hidden = (
            tag in {"script", "style", "template"}
            or "hidden" in values
            or values.get("aria-hidden", "").lower() == "true"
        )
        if tag in self.VOID_TAGS:
            return
        self._hidden_stack.append((tag, hidden))
        if hidden:
            self._hidden_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        while self._hidden_stack:
            open_tag, hidden = self._hidden_stack.pop()
            if hidden:
                self._hidden_depth -= 1
            if open_tag == tag:
                break

    def handle_data(self, data: str) -> None:
        if self._hidden_depth == 0:
            self.parts.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


class ChurningV1Tests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {key: read_json(path) for key, path in CONTRACTS.items()}
        cls.drops = read_json(DROPS_PATH)
        cls.problems = read_json(PROBLEMS_PATH)
        cls.inventory = read_json(INVENTORY_PATH)
        cls.corpus = read_json(CORPUS_PATH)
        cls.atlas = read_json(ATLAS_PATH)

    def assert_contract(self, value: object, schema: dict, where: str) -> None:
        if "const" in schema:
            self.assertEqual(value, schema["const"], where)
        if "enum" in schema:
            self.assertIn(value, schema["enum"], where)

        kind = schema.get("type")
        if kind == "object":
            self.assertIsInstance(value, dict, where)
            assert isinstance(value, dict)
            required = schema.get("required", [])
            self.assertTrue(set(required).issubset(value), f"{where}: missing required fields")
            properties = schema.get("properties", {})
            additional = schema.get("additionalProperties", True)
            if additional is False:
                self.assertFalse(set(value) - set(properties), f"{where}: unknown fields")
            for key, child in properties.items():
                if key in value:
                    self.assert_contract(value[key], child, f"{where}.{key}")
            if isinstance(additional, dict):
                for key in set(value) - set(properties):
                    self.assert_contract(value[key], additional, f"{where}.{key}")
        elif kind == "array":
            self.assertIsInstance(value, list, where)
            assert isinstance(value, list)
            self.assertGreaterEqual(len(value), schema.get("minItems", 0), where)
            if "maxItems" in schema:
                self.assertLessEqual(len(value), schema["maxItems"], where)
            if schema.get("uniqueItems"):
                encoded = [json.dumps(row, sort_keys=True, ensure_ascii=False) for row in value]
                self.assertEqual(len(encoded), len(set(encoded)), where)
            if isinstance(schema.get("items"), dict):
                for index, child in enumerate(value):
                    self.assert_contract(child, schema["items"], f"{where}[{index}]")
        elif kind == "string":
            self.assertIsInstance(value, str, where)
            assert isinstance(value, str)
            self.assertGreaterEqual(len(value), schema.get("minLength", 0), where)
            if "pattern" in schema:
                self.assertRegex(value, schema["pattern"], where)
        elif kind == "boolean":
            self.assertIs(type(value), bool, where)
        elif kind == "integer":
            self.assertIs(type(value), int, where)

    def load_builder(self):
        self.assertTrue(BUILDER_PATH.is_file(), "build_churning.py has not landed")
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("build_churning_v1_under_test", BUILDER_PATH)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SITE))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.remove(str(SITE))
        return module

    def source_payload(self, path: str, frozen_commit: str) -> bytes:
        safe_relative_path(ROOT, path)
        if frozen_commit == "POST_FREEZE_OWNER_DIRECTION":
            self.assertEqual(path, OWNER_DIRECTION)
            return (ROOT / path).read_bytes()
        self.assertEqual(frozen_commit, self.corpus["frozen_source_commit"])
        result = subprocess.run(
            ["git", "show", f"{frozen_commit}:{path}"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        return result.stdout

    def output_paths(self) -> list[Path]:
        paths = [safe_relative_path(ROOT, raw, must_exist=False) for raw in self.corpus["output_map"].values()]
        paths.extend((SITE / "churn" / "schemas" / source.name).resolve() for source in CONTRACTS.values())
        return sorted(set(paths))

    def test_01_contracts_parse_and_instances_obey_required_fields_consts_and_enums(self) -> None:
        expected_titles = {
            "drop": "ChurningDrop.v1",
            "problem": "ProblemAdjudication.v1",
            "corpus": "ThirdChurningCorpus.v1",
        }
        for key, schema in self.schemas.items():
            self.assertEqual(schema.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema.get("title"), expected_titles[key])
            self.assertEqual(schema.get("type"), "object")
            self.assertIs(schema.get("additionalProperties"), False)
            self.assertTrue(set(schema.get("required", [])).issubset(schema.get("properties", {})))
        for index, row in enumerate(self.drops):
            self.assert_contract(row, self.schemas["drop"], f"drops[{index}]")
        for index, row in enumerate(self.problems):
            self.assert_contract(row, self.schemas["problem"], f"problems[{index}]")
        self.assert_contract(self.corpus, self.schemas["corpus"], "corpus")

    def test_02_drop_bound_counts_identity_and_tier_separation(self) -> None:
        self.assertIsInstance(self.drops, list)
        self.assertEqual(len(self.drops), 51)
        self.assertLessEqual(len(self.drops), 64)
        drop_ids = [row["drop_id"] for row in self.drops]
        self.assertEqual(len(drop_ids), len(set(drop_ids)))
        self.assertEqual(drop_ids, self.corpus["drop_order"])
        counts = Counter(row["classification"] for row in self.drops)
        self.assertEqual(counts, {"SURVIVOR_CANDIDATE": 22, "POISON_WARNING": 29})
        classifications = set(counts)
        evidence_tiers = {row["evidence_tier"] for row in self.drops}
        self.assertTrue(classifications.isdisjoint(evidence_tiers))
        for row in self.drops:
            self.assertNotEqual(row["classification"], row["evidence_tier"])
            if row["classification"] == "SURVIVOR_CANDIDATE":
                self.assertEqual(row["mythic_alias"], "AMRITA")
            else:
                self.assertEqual(row["mythic_alias"], "HALAHALA")

    def test_03_source_paths_and_hashes_bind_frozen_commit_or_owner_direction(self) -> None:
        source_rows = self.corpus["source_hashes"]
        self.assertEqual(self.corpus["source_pathset"], [row["path"] for row in source_rows])
        declared = {row["path"]: row["sha256"] for row in source_rows}
        self.assertEqual(len(declared), len(source_rows))
        for row in source_rows:
            self.assertRegex(row["sha256"], SHA256_RE)
            frozen = (
                "POST_FREEZE_OWNER_DIRECTION"
                if row["path"] == OWNER_DIRECTION
                else self.corpus["frozen_source_commit"]
            )
            self.assertEqual(sha256_bytes(self.source_payload(row["path"], frozen)), row["sha256"])

        checked: dict[tuple[str, str], str] = {}
        for drop in self.drops:
            for row in drop["source_refs"]:
                self.assertRegex(row["sha256"], SHA256_RE)
                key = (row["path"], row["frozen_commit"])
                if key not in checked:
                    checked[key] = sha256_bytes(self.source_payload(*key))
                self.assertEqual(checked[key], row["sha256"], drop["drop_id"])
                self.assertEqual(declared[row["path"]], row["sha256"])

    def test_04_pqa_remains_exactly_54_selected_and_zero_earned(self) -> None:
        self.assertEqual(len(self.problems), 54)
        problem_ids = [row["problem_id"] for row in self.problems]
        self.assertEqual(len(problem_ids), len(set(problem_ids)))
        atlas_ids = [
            row["question_id"]
            for domain in self.atlas["domains"]
            for row in domain["questions"]
        ]
        self.assertEqual(problem_ids, atlas_ids)
        self.assertEqual(problem_ids, self.corpus["problem_order"])
        self.assertEqual(
            self.corpus["pqa_launch_counts"],
            {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0},
        )
        self.assertEqual(self.atlas["launch_counts"], self.corpus["pqa_launch_counts"])
        drop_ids = {row["drop_id"] for row in self.drops}
        for row in self.problems:
            self.assertEqual(row["result_state"], "SELECTED")
            self.assertEqual(row["earned_effect"], "NO_INCREMENT")
            self.assertEqual(row["native_reviews"], [])
            self.assertTrue(set(row["linked_drop_ids"]).issubset(drop_ids))

    def test_05_builder_check_is_deterministic_and_read_only(self) -> None:
        self.load_builder()
        paths = [BUILDER_PATH, *self.output_paths()]
        before = {path: sha256_file(path) if path.is_file() else None for path in paths}
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, "-B", str(BUILDER_PATH), "--check"],
            cwd=SITE,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        after = {path: sha256_file(path) if path.is_file() else None for path in paths}
        self.assertEqual(before, after, "build_churning.py --check mutated an owned output")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_06_generated_pages_are_static_and_show_every_drop_id(self) -> None:
        expected = {
            SITE / "churn" / "index.html": [row["drop_id"] for row in self.drops],
            SITE / "amrita" / "index.html": [
                row["drop_id"] for row in self.drops if row["classification"] == "SURVIVOR_CANDIDATE"
            ],
            SITE / "halahala" / "index.html": [
                row["drop_id"] for row in self.drops if row["classification"] == "POISON_WARNING"
            ],
        }
        for path, ids in expected.items():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("fetch(", text, path.name)
            self.assertNotIn("innerHTML", text, path.name)
            parser = VisibleTextParser()
            parser.feed(text)
            visible = parser.text()
            for row_id in ids:
                self.assertIn(row_id, visible, f"{row_id} is not static visible text in {path}")

        problems = read_json(SITE / "churn" / "problems.json")
        self.assertEqual(
            [row["problem_id"] for row in problems],
            [row["problem_id"] for row in self.problems],
        )

    def test_07_legacy_amrita_alias_is_a_22_row_top_level_array(self) -> None:
        alias = read_json(SITE / "amrita" / "amrita.json")
        self.assertIsInstance(alias, list)
        self.assertEqual(len(alias), 22)
        required = {"id", "group", "tier", "title", "body", "source"}
        self.assertEqual(len({row["id"] for row in alias}), 22)
        for row in alias:
            self.assertTrue(required.issubset(row), row)
            self.assertNotEqual(str(row["tier"]).lower(), "halahala")

    def test_08_jsonl_is_exactly_107_typed_records(self) -> None:
        path = SITE / "churn" / "corpus.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(len(rows), 107)
        self.assertEqual(
            Counter(row.get("schema_id") for row in rows),
            {
                "emergentism/ChurningDrop.v1": 51,
                "emergentism/ProblemAdjudication.v1": 54,
                "emergentism/ParadoxInventory.v1": 1,
                "emergentism/ThirdChurningCorpus.v1": 1,
            },
        )

    def test_09_public_schema_copies_are_byte_identical(self) -> None:
        for source in CONTRACTS.values():
            matches = list((SITE / "churn").rglob(source.name))
            self.assertEqual(len(matches), 1, f"expected one public copy of {source.name}: {matches}")
            self.assertEqual(source.read_bytes(), matches[0].read_bytes(), source.name)

    def test_10_predecessor_manifest_verifies_every_archived_byte(self) -> None:
        rows: list[tuple[str, str]] = []
        for number, line in enumerate(PREDECESSOR_MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
            match = re.fullmatch(r"([0-9a-f]{64})  ([^#]+?)(?:\s+#.*)?", line)
            self.assertIsNotNone(match, f"malformed predecessor manifest line {number}")
            assert match is not None
            rows.append((match.group(1), match.group(2).rstrip()))
        self.assertEqual(len(rows), 9)
        self.assertEqual(len({path for _, path in rows}), 9)
        for expected, raw in rows:
            archived = safe_relative_path(PREDECESSOR_ARCHIVE, raw)
            self.assertEqual(sha256_file(archived), expected, raw)

    def test_11_hostile_text_is_escaped_when_builder_exposes_an_escape_helper(self) -> None:
        builder = self.load_builder()
        escape = getattr(builder, "esc", None) or getattr(builder, "escape_html", None)
        if escape is None:
            self.skipTest("build_churning.py exposes no public escaping helper")
        hostile = '<script>alert("x")</script>'
        rendered = escape(hostile)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("&quot;x&quot;", rendered)

    def test_12_builder_path_helper_rejects_absolute_and_parent_paths_if_exposed(self) -> None:
        builder = self.load_builder()
        helper = next(
            (
                getattr(builder, name)
                for name in (
                    "validate_relative_path",
                    "safe_relative_path",
                    "safe_source_path",
                    "_safe_source_path",
                )
                if callable(getattr(builder, name, None))
            ),
            None,
        )
        if helper is None:
            self.skipTest("build_churning.py exposes no path-validation helper")
        for hostile in ("../escape", "/absolute", "safe/../../escape"):
            with self.subTest(hostile=hostile):
                with self.assertRaises((ValueError, OSError)):
                    helper(hostile, "hostile test path")

    def test_13_halahala_is_current_and_absent_from_every_withholding_surface(self) -> None:
        parity = read_json(SITE / "public_semantic_parity.json")
        self.assertIn("halahala/index.html", parity["currentSurfaces"])
        self.assertNotIn("halahala/index.html", parity["declaredProvisional"]["routes"])

        withheld = read_json(SITE / "withheld-routes.json")
        self.assertNotIn("halahala/index.html", {row["artifact"] for row in withheld["artifacts"]})
        for row in withheld["artifacts"]:
            self.assertFalse(any(route.startswith("/halahala") for route in row["publicRoutes"]))

        self.assertNotIn("halahala/index.html", (SITE / ".vercelignore").read_text(encoding="utf-8"))
        vercel = read_json(SITE / "vercel.json")
        for section in ("redirects", "headers", "rewrites"):
            for row in vercel.get(section, []):
                self.assertFalse(row.get("source", "").startswith("/halahala"), (section, row))
        sw = (SITE / "sw.js").read_text(encoding="utf-8")
        spine, withheld_routes = sw.split("const WITHHELD_ROUTES = new Set([", 1)
        withheld_routes = withheld_routes.split("]);", 1)[0]
        self.assertIn('"/halahala/"', spine)
        self.assertNotIn('"/halahala"', withheld_routes)
        self.assertNotIn('"/halahala/"', withheld_routes)
        self.assertNotIn('"/halahala/index.html"', withheld_routes)
        page = (SITE / "halahala" / "index.html").read_text(encoding="utf-8").lower()
        self.assertNotIn("noindex", page)


if __name__ == "__main__":
    unittest.main()
