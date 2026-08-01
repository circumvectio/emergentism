#!/usr/bin/env python3
"""Mutation controls for active receipt-citation custody."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py"
SPEC = importlib.util.spec_from_file_location("active_receipt_checker", CHECKER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import {CHECKER_PATH}")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class ActiveReceiptCitationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.audit = self.root / "11_UPLINK/50_AUDITS_AND_EXECUTIONS"
        self.packet = self.root / "11_UPLINK/60_SESSION_PACKETS"
        self.audit.mkdir(parents=True)
        self.packet.mkdir(parents=True)
        self.target = self.audit / "126_AUDITED_TARGET.md"
        self.other = self.packet / "126_UNRELATED_PACKET.md"
        self.target.write_text("# target\n", encoding="utf-8")
        self.other.write_text("# other\n", encoding="utf-8")
        self.index_path = self.audit / "00_RECEIPT_DISAMBIGUATION_INDEX.json"
        self.write_index()
        self.active = self.root / "active.md"
        self.active.write_text(
            "Receipt 126 (`126_AUDITED_TARGET.md`) is the selected audit.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_index(self) -> None:
        data = {
            "schemaVersion": 1,
            "ambiguousNumbers": 1,
            "rows": [
                {
                    "number": "126",
                    "count": 2,
                    "entries": [
                        {
                            "path": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/126_AUDITED_TARGET.md"
                        },
                        {
                            "path": "11_UPLINK/60_SESSION_PACKETS/126_UNRELATED_PACKET.md"
                        },
                    ],
                }
            ],
        }
        self.index_path.write_text(json.dumps(data), encoding="utf-8")

    @contextmanager
    def contract(self, **extra):
        sources = extra.pop("AUDITED_ACTIVE_SOURCES", ("active.md",))
        values = {
            "AUDITED_ACTIVE_SOURCES": sources,
            "EXPECTED_ACTIVE_SOURCE_SET_SHA256": CHECKER.path_set_sha256(sources),
            "EXPECTED_REUSED_PREFIXES": 1,
            "RECEIPT_INDEX": Path(
                "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_RECEIPT_DISAMBIGUATION_INDEX.json"
            ),
            "RECEIPT_REF": Path(
                "11_UPLINK/50_AUDITS_AND_EXECUTIONS/237_TEST_RECEIPT.md"
            ),
            "DIAGNOSTIC_UNITS": (),
            "KNOWN_REPORT_ONLY_RESOLVED": set(),
        }
        values.update(extra)
        with mock.patch.multiple(CHECKER, **values):
            yield

    def test_exact_inline_target_passes(self) -> None:
        with self.contract():
            registry = CHECKER.build_registry(self.root)
            count, _ = CHECKER.validate_registry(
                self.root, registry, require_custody=False
            )
        self.assertEqual(count, 2)
        self.assertEqual(registry["occurrences"]["typed_locator_count"], 1)
        self.assertEqual(registry["occurrences"]["exact_target_token_count"], 1)
        self.assertTrue(
            all(
                row["target"]
                == "11_UPLINK/50_AUDITS_AND_EXECUTIONS/126_AUDITED_TARGET.md"
                for row in registry["occurrences"]["rows"]
            )
        )

    def test_wrong_candidate_substitution_fails(self) -> None:
        with self.contract():
            registry = CHECKER.build_registry(self.root)
        self.active.write_text(
            "Receipt 126 (`126_UNRELATED_PACKET.md`) is wrong.\n", encoding="utf-8"
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "registry differs"
        ):
            CHECKER.validate_registry(self.root, registry, require_custody=False)

    def test_filename_like_substring_cannot_bind_typed_locator(self) -> None:
        self.active.write_text(
            "Receipt 126 (`x126_AUDITED_TARGET.md.bak`) is not the target.\n",
            encoding="utf-8",
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "must bind"
        ):
            CHECKER.build_registry(self.root)

    def test_packet_namespace_cannot_cross_bind_to_receipt_lane(self) -> None:
        self.active.write_text(
            "packet 126 (`126_UNRELATED_PACKET.md`) is lane 60.\n",
            encoding="utf-8",
        )
        with self.contract():
            registry = CHECKER.build_registry(self.root)
        self.active.write_text(
            "packet 126 (`126_AUDITED_TARGET.md`) crosses lanes.\n",
            encoding="utf-8",
        )
        with self.contract(), self.assertRaises(CHECKER.ContractError):
            CHECKER.validate_registry(self.root, registry, require_custody=False)

    def test_arbitrary_same_filename_elsewhere_does_not_shield(self) -> None:
        self.active.write_text(
            "Receipt 126 is bare here.\n"
            "Unrelated appendix: `126_AUDITED_TARGET.md`.\n",
            encoding="utf-8",
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "must bind"
        ):
            CHECKER.build_registry(self.root)

    def test_ledger_table_elsewhere_does_not_shield(self) -> None:
        self.active.write_text(
            "Receipt 126 is bare here.\n"
            "| 126 | `126_AUDITED_TARGET.md` | census row |\n",
            encoding="utf-8",
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "must bind"
        ):
            CHECKER.build_registry(self.root)

    def test_new_active_file_fails_even_with_exact_candidate(self) -> None:
        (self.root / "new.md").write_text(
            "Receipt 126 (`126_AUDITED_TARGET.md`).\n", encoding="utf-8"
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "new unregistered active ambiguity"
        ):
            CHECKER.build_registry(self.root)

    def test_new_active_file_fails_with_exact_target_only(self) -> None:
        (self.root / "new.md").write_text(
            "`126_UNRELATED_PACKET.md`\n", encoding="utf-8"
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "new unregistered active exact target"
        ):
            CHECKER.build_registry(self.root)

    def test_false_negation_cannot_exempt_new_bare_citation(self) -> None:
        (self.root / "new.md").write_text(
            "There is no such receipt 126.\n", encoding="utf-8"
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "new unregistered active ambiguity"
        ):
            CHECKER.build_registry(self.root)

    def test_public_route_dependency_cannot_hide_bare_locator(self) -> None:
        public = self.root / "12_PUBLIC_SITE"
        route = public / "amrita"
        route.mkdir(parents=True)
        (public / "public_semantic_parity.json").write_text(
            json.dumps(
                {
                    "currentSurfaces": [],
                    "declaredProvisional": {"routes": ["amrita/index.html"]},
                }
            ),
            encoding="utf-8",
        )
        (route / "index.html").write_text(
            '<link rel="stylesheet" href="amrita.css">\n'
            '<script>fetch("amrita.json")</script>\n',
            encoding="utf-8",
        )
        (route / "amrita.css").write_text(
            "/* receipt 126 is bare in a delivered dependency */\n",
            encoding="utf-8",
        )
        (route / "amrita.json").write_text("{}\n", encoding="utf-8")
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "new unregistered active ambiguity"
        ):
            CHECKER.build_registry(self.root)

    def test_public_route_cannot_hide_exact_target_only(self) -> None:
        public = self.root / "12_PUBLIC_SITE"
        route = public / "new"
        route.mkdir(parents=True)
        (public / "public_semantic_parity.json").write_text(
            json.dumps(
                {
                    "currentSurfaces": ["new/index.html"],
                    "declaredProvisional": {"routes": []},
                }
            ),
            encoding="utf-8",
        )
        (route / "index.html").write_text(
            "`126_UNRELATED_PACKET.md`\n", encoding="utf-8"
        )
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "new unregistered active exact target"
        ):
            CHECKER.build_registry(self.root)

    def test_public_module_manifest_and_service_worker_closure(self) -> None:
        public = self.root / "12_PUBLIC_SITE"
        route = public / "new"
        assets = public / "assets"
        route.mkdir(parents=True)
        assets.mkdir(parents=True)
        (public / "public_semantic_parity.json").write_text(
            json.dumps(
                {
                    "currentSurfaces": ["new/index.html"],
                    "declaredProvisional": {"routes": []},
                }
            ),
            encoding="utf-8",
        )
        (route / "index.html").write_text(
            '<link rel="manifest" href="../site.webmanifest">\n'
            '<script type="module" src="../assets/entry.mjs"></script>\n'
            '<script src="../assets/pwa.js"></script>\n',
            encoding="utf-8",
        )
        (public / "site.webmanifest").write_text("{}\n", encoding="utf-8")
        (assets / "entry.mjs").write_text(
            'import {\n  nested\n} from "./nested.mjs";\n'
            'new Worker("./dedicated-worker.js");\n'
            'new SharedWorker("./shared-worker.js");\n'
            'CSS.paintWorklet.addModule("./paint-worklet.js");\n',
            encoding="utf-8",
        )
        (assets / "nested.mjs").write_text(
            "export const nested = true;\n", encoding="utf-8"
        )
        for name in (
            "dedicated-worker.js",
            "shared-worker.js",
            "paint-worklet.js",
        ):
            (assets / name).write_text("worker\n", encoding="utf-8")
        (assets / "pwa.js").write_text(
            'navigator.serviceWorker.register("/sw.js");\n', encoding="utf-8"
        )
        (public / "sw.js").write_text(
            'const SPINE = ["/active-data.json", "/offline/"];\n'
            'importScripts("/worker-helper.js", "/worker-extra.js");\n',
            encoding="utf-8",
        )
        (public / "active-data.json").write_text(
            "{}\n", encoding="utf-8"
        )
        (public / "offline").mkdir()
        (public / "offline/index.html").write_text("offline\n", encoding="utf-8")
        (public / "worker-helper.js").write_text(
            "`126_UNRELATED_PACKET.md`\n", encoding="utf-8"
        )
        (public / "worker-extra.js").write_text("extra\n", encoding="utf-8")
        with self.contract():
            dependencies = CHECKER.public_active_artifacts(self.root)
            self.assertTrue(
                {
                    "12_PUBLIC_SITE/site.webmanifest",
                    "12_PUBLIC_SITE/assets/entry.mjs",
                    "12_PUBLIC_SITE/assets/nested.mjs",
                    "12_PUBLIC_SITE/assets/dedicated-worker.js",
                    "12_PUBLIC_SITE/assets/shared-worker.js",
                    "12_PUBLIC_SITE/assets/paint-worklet.js",
                    "12_PUBLIC_SITE/assets/pwa.js",
                    "12_PUBLIC_SITE/sw.js",
                    "12_PUBLIC_SITE/active-data.json",
                    "12_PUBLIC_SITE/offline/index.html",
                    "12_PUBLIC_SITE/worker-helper.js",
                    "12_PUBLIC_SITE/worker-extra.js",
                }.issubset(dependencies)
            )
            with self.assertRaisesRegex(
                CHECKER.ContractError, "new unregistered active exact target"
            ):
                CHECKER.build_registry(self.root)

    def test_count_preserving_registry_row_substitution_fails(self) -> None:
        with self.contract():
            registry = CHECKER.build_registry(self.root)
            mutated = copy.deepcopy(registry)
            mutated["occurrences"]["rows"][0]["target"] = str(
                self.other.relative_to(self.root)
            )
            mutated["occurrences"]["rows_sha256"] = CHECKER.canonical_sha256(
                mutated["occurrences"]["rows"]
            )
            with self.assertRaisesRegex(CHECKER.ContractError, "registry differs"):
                CHECKER.validate_registry(
                    self.root, mutated, require_custody=False
                )

    def test_exact_only_same_prefix_substitution_fails(self) -> None:
        self.active.write_text("`126_AUDITED_TARGET.md`\n", encoding="utf-8")
        with self.contract():
            registry = CHECKER.build_registry(self.root)
        self.assertEqual(registry["occurrences"]["typed_locator_count"], 0)
        self.assertEqual(registry["occurrences"]["exact_target_token_count"], 1)
        self.active.write_text("`126_UNRELATED_PACKET.md`\n", encoding="utf-8")
        with self.contract(), self.assertRaisesRegex(
            CHECKER.ContractError, "registry differs"
        ):
            CHECKER.validate_registry(self.root, registry, require_custody=False)

    def test_count_preserving_source_set_substitution_fails(self) -> None:
        (self.root / "substitute.md").write_text(
            self.active.read_text(encoding="utf-8"), encoding="utf-8"
        )
        with self.contract(
            AUDITED_ACTIVE_SOURCES=("substitute.md",),
            EXPECTED_ACTIVE_SOURCE_SET_SHA256=CHECKER.path_set_sha256(("active.md",)),
        ), self.assertRaisesRegex(CHECKER.ContractError, "source set hash"):
            CHECKER.build_registry(self.root)

    def test_candidate_target_disappearance_fails(self) -> None:
        self.target.unlink()
        with self.contract(), self.assertRaises(CHECKER.ContractError):
            CHECKER.build_registry(self.root)

    def test_index_candidate_substitution_fails(self) -> None:
        data = json.loads(self.index_path.read_text(encoding="utf-8"))
        data["rows"][0]["entries"][0]["path"] = data["rows"][0]["entries"][1]["path"]
        self.index_path.write_text(json.dumps(data), encoding="utf-8")
        with self.contract(), self.assertRaises(CHECKER.ContractError):
            CHECKER.build_registry(self.root)

    def test_duplicate_json_keys_fail_closed(self) -> None:
        path = self.root / "duplicate.json"
        path.write_text('{"schema": 1, "schema": 2}', encoding="utf-8")
        with self.assertRaisesRegex(CHECKER.ContractError, "duplicate JSON"):
            CHECKER.load_json(path)

    def test_malformed_json_fails_closed(self) -> None:
        path = self.root / "malformed.json"
        path.write_text('{"schema":', encoding="utf-8")
        with self.assertRaisesRegex(CHECKER.ContractError, "invalid JSON"):
            CHECKER.load_json(path)

    def test_singular_plural_list_range_colon_and_shorthand_parser(self) -> None:
        text = (
            "Receipt: 126; receipts 126 and 130; receipts 130/131; "
            "receipts 108–110; receipt 114, 2026-07-12; "
            "per C21 / 109; per 110 / 126 §2B.3"
        )
        numbers = [item.number for item in CHECKER.citation_mentions(text)]
        self.assertEqual(
            numbers,
            ["126", "126", "130", "130", "131", "108", "109", "110", "114", "109", "110", "126"],
        )
        self.assertNotIn("202", numbers)

    def test_descending_and_overbroad_ranges_fail_cleanly(self) -> None:
        with self.assertRaises(CHECKER.ContractError):
            CHECKER.citation_mentions("receipts 132–108")
        with self.assertRaises(CHECKER.ContractError):
            CHECKER.citation_mentions("receipts 100–400")

    def test_context_hashed_diagnostic_is_exact(self) -> None:
        unit = "This sentence diagnoses r126 as ambiguous."
        diagnostic = self.root / "diagnostic.md"
        diagnostic.write_text(unit + "\n", encoding="utf-8")
        rule = (
            "diagnostic.md",
            1,
            CHECKER.semantic_unit_sha256(unit),
            frozenset({"126"}),
        )
        with self.contract(DIAGNOSTIC_UNITS=(rule,)):
            CHECKER.build_registry(self.root)
        diagnostic.write_text(unit + " Now it asserts r126.\n", encoding="utf-8")
        with self.contract(DIAGNOSTIC_UNITS=(rule,)), self.assertRaisesRegex(
            CHECKER.ContractError, "new unregistered active ambiguity"
        ):
            CHECKER.build_registry(self.root)

    def test_receipt_digest_marker_binds_registry(self) -> None:
        with self.contract():
            receipt = self.root / CHECKER.RECEIPT_REF
            receipt.write_text("custody pending\n", encoding="utf-8")
            registry = CHECKER.build_registry(self.root)
            receipt.write_text(
                "active_receipt_citation_registry_canonical_sha256: "
                f"{CHECKER.canonical_sha256(registry)}\n",
                encoding="utf-8",
            )
            CHECKER.validate_registry(self.root, registry, require_custody=True)
            receipt.write_text(
                "active_receipt_citation_registry_canonical_sha256: " + "0" * 64 + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(CHECKER.ContractError, "digest marker"):
                CHECKER.validate_registry(self.root, registry, require_custody=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
