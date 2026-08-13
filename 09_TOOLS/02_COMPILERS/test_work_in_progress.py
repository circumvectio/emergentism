#!/usr/bin/env python3
"""Mutation controls for the source-bound WIP manifest rows."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_work_in_progress.py"
SPEC = importlib.util.spec_from_file_location("check_work_in_progress", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
MANIFEST = ROOT / "00_WORK_IN_PROGRESS/README.md"


class WorkInProgressSourceMirrorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest_text = MANIFEST.read_text(encoding="utf-8")

    def write_json(self, root: Path, relative: Path, value: dict) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_live_source_mirror_contract_passes(self) -> None:
        self.assertEqual(CHECKER.source_mirror_errors(ROOT, self.manifest_text), [])
        self.assertEqual(
            CHECKER.OWNER_DOCKET_WIP_PATH,
            "../00_META/00_CONTACT_LIMITED_OWNER_DECISION_DOCKET_2026_08_02.md",
        )

    def mutate_open_row(self, item: str, old: str, new: str) -> str:
        owner_table = CHECKER.owner_rulings_table(self.manifest_text)
        assert owner_table is not None
        source_row = next(line for line in owner_table.splitlines() if f"`{item}`" in line)
        return self.manifest_text.replace(source_row, source_row.replace(old, new, 1), 1)

    def test_each_open_row_must_retain_its_exact_id_docket_and_boundary(self) -> None:
        for item, row in CHECKER.OPEN_SOURCE_MIRROR_ROWS.items():
            with self.subTest(item=item, mutation="id"):
                mutated = self.manifest_text.replace(f"`{item}`", f"`{item}-MOVED`", 1)
                errors = CHECKER.source_mirror_errors(ROOT, mutated)
                self.assertTrue(
                    any(f"source-mirror row for {item}" in error for error in errors),
                    errors,
                )
            with self.subTest(item=item, mutation="docket"):
                mutated = self.mutate_open_row(item, f"`{row['docket_id']}`", "`D-OWNER-RENAMED`")
                errors = CHECKER.source_mirror_errors(ROOT, mutated)
                self.assertTrue(
                    any(f"row {item} no longer matches its exact held" in error for error in errors),
                    errors,
                )
            with self.subTest(item=item, mutation="docket-path"):
                mutated = self.mutate_open_row(
                    item,
                    CHECKER.OWNER_DOCKET_WIP_PATH,
                    "../00_META/not-the-owner-docket.md",
                )
                errors = CHECKER.source_mirror_errors(ROOT, mutated)
                self.assertTrue(
                    any(f"row {item} no longer matches its exact held" in error for error in errors),
                    errors,
                )
            with self.subTest(item=item, mutation="boundary"):
                boundary = "No reviewer or contact is named." if item == CHECKER.REVIEW_CONTACT_SOURCE_ROW else (
                    "No selection is implied"
                    if item == "OWNER_GATE_HELD_PUBLIC_DOCS"
                    else "No move or conformance is implied"
                )
                mutated = self.mutate_open_row(item, boundary, "closed")
                errors = CHECKER.source_mirror_errors(ROOT, mutated)
                self.assertTrue(
                    any(f"row {item} no longer matches its exact held" in error for error in errors),
                    errors,
                )
            with self.subTest(item=item, mutation="closed"):
                mutated = self.mutate_open_row(
                    item,
                    f"{row['question']} |",
                    f"{row['question']} CLOSED |",
                )
                errors = CHECKER.source_mirror_errors(ROOT, mutated)
                self.assertTrue(
                    any(f"row {item} no longer matches its exact held" in error for error in errors),
                    errors,
                )
            with self.subTest(item=item, mutation="semantic-promotion"):
                promotion = (
                    " Reviewer Ada is authorized to contact today. Contact is ready to send."
                    if item == CHECKER.REVIEW_CONTACT_SOURCE_ROW
                    else " The current owner is now selected."
                )
                mutated = self.mutate_open_row(
                    item,
                    f"{row['question']} |",
                    f"{row['question']}{promotion} |",
                )
                errors = CHECKER.source_mirror_errors(ROOT, mutated)
                self.assertTrue(
                    any(f"row {item} no longer matches its exact held" in error for error in errors),
                    errors,
                )

        owner_section = CHECKER.owner_rulings_section(self.manifest_text)
        assert owner_section is not None
        source_row = next(
            line for line in owner_section.splitlines()
            if f"`{CHECKER.REVIEW_CONTACT_SOURCE_ROW}`" in line
        )
        duplicated = self.manifest_text.replace(source_row, source_row + "\n" + source_row, 1)
        errors = CHECKER.source_mirror_errors(ROOT, duplicated)
        self.assertTrue(
            any(
                f"exactly one open source-mirror row for {CHECKER.REVIEW_CONTACT_SOURCE_ROW}"
                in error
                for error in errors
            ),
            errors,
        )
        moved = self.manifest_text.replace(source_row, "", 1) + "\n" + source_row + "\n"
        errors = CHECKER.source_mirror_errors(ROOT, moved)
        self.assertTrue(
            any(
                f"exactly one open source-mirror row for {CHECKER.REVIEW_CONTACT_SOURCE_ROW}"
                in error
                for error in errors
            ),
            errors,
        )
        unknown = self.manifest_text.replace(
            source_row,
            "| `OWNER_GATE_UNDECLARED` | unowned | blocks | `D-OWNER-99` |\n" + source_row,
            1,
        )
        errors = CHECKER.source_mirror_errors(ROOT, unknown)
        self.assertTrue(any("unknown source-mirror rows" in error for error in errors), errors)

        stale_code_example = self.manifest_text.replace(source_row, "", 1).replace(
            "\n---\n\n**Machine-owner mirror.",
            "\n\n```text\n" + source_row + "\n```\n\n---\n\n**Machine-owner mirror.",
            1,
        )
        errors = CHECKER.source_mirror_errors(ROOT, stale_code_example)
        self.assertTrue(
            any(
                f"exactly one open source-mirror row for {CHECKER.REVIEW_CONTACT_SOURCE_ROW}"
                in error
                for error in errors
            ),
            errors,
        )

        malformed_fence = self.manifest_text.replace(
            "| id | question | blocks | source |\n|---|---|---|---|\n",
            "```text\n```not-a-closing-fence-under-CommonMark\n"
            "| id | question | blocks | source |\n|---|---|---|---|\n",
            1,
        )
        errors = CHECKER.source_mirror_errors(ROOT, malformed_fence)
        self.assertTrue(
            any("canonical owner-rulings table" in error for error in errors),
            errors,
        )

        owner_table = CHECKER.owner_rulings_table(self.manifest_text)
        assert owner_table is not None
        canonical_table = "| id | question | blocks | source |\n|---|---|---|---|\n" + owner_table
        commented_table = self.manifest_text.replace(
            canonical_table,
            "<!--\n" + canonical_table + "-->\n",
            1,
        )
        errors = CHECKER.source_mirror_errors(ROOT, commented_table)
        self.assertTrue(
            any("canonical owner-rulings table" in error for error in errors),
            errors,
        )

        hidden_manifest = "<!--\n" + self.manifest_text + "-->\n"
        errors = CHECKER.source_mirror_errors(ROOT, hidden_manifest)
        self.assertTrue(
            any("canonical owner-rulings table" in error for error in errors),
            errors,
        )
        fenced_manifest = "```markdown\n" + self.manifest_text + "```\n"
        errors = CHECKER.source_mirror_errors(ROOT, fenced_manifest)
        self.assertTrue(
            any("canonical owner-rulings table" in error for error in errors),
            errors,
        )
        hidden_frontmatter = (
            "---\n## 1 · Owner rulings — hidden metadata\n\n"
            "| id | question | blocks | source |\n|---|---|---|---|\n"
            + owner_table
            + "---\n"
        )
        errors = CHECKER.source_mirror_errors(ROOT, hidden_frontmatter)
        self.assertTrue(
            any("canonical owner-rulings table" in error for error in errors),
            errors,
        )
        errors = CHECKER.source_mirror_errors(ROOT, "\ufeff" + hidden_frontmatter)
        self.assertTrue(
            any("canonical owner-rulings table" in error for error in errors),
            errors,
        )
        errors = CHECKER.source_mirror_errors(
            ROOT, hidden_frontmatter.replace("---\n", "--- \n")
        )
        self.assertTrue(
            any("canonical owner-rulings table" in error for error in errors),
            errors,
        )

        unrelated = self.manifest_text + "\n## Later table\n\n| `OWNER_GATE_FUTURE` | later | none | — |\n"
        self.assertEqual(CHECKER.source_mirror_errors(ROOT, unrelated), [])

    def test_owner_held_source_must_match_its_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            state = {
                "schema": CHECKER.CONTACT_LIMITED_STATE_SCHEMA,
                "status": "OPEN_INTERNAL",
                "owner_held": {
                    "source_profile": CHECKER.COHERENCE_PROFILE_REL.as_posix(),
                    "debts": [
                        copy.deepcopy(row["state_debt"])
                        for row in CHECKER.OWNER_HELD_SOURCE_ROWS.values()
                    ],
                }
            }
            profile = {
                "schema": CHECKER.COHERENCE_PROFILE_SCHEMA,
                "axes": {
                    "routing": {
                        "state": "PASS_WITH_DEBT",
                        "basis_refs": [CHECKER.ROUTING_BASIS_REF],
                        "debt_ids": [
                            "OWNER_GATE_HELD_PUBLIC_DOCS",
                            "OWNER_GATE_OPEN_TOPOLOGY",
                        ]
                    }
                },
                "overall": {"state": "PASS_WITH_DEBT"},
            }
            receipt = corpus / CHECKER.ROUTING_BASIS_REF
            receipt.parent.mkdir(parents=True, exist_ok=True)
            receipt.write_text("source receipt\n", encoding="utf-8")
            wip_manifest = corpus / CHECKER.WIP_MANIFEST_REL
            wip_manifest.parent.mkdir(parents=True, exist_ok=True)
            wip_manifest.write_text("WIP mirror\n", encoding="utf-8")
            receipt.write_bytes(
                (ROOT / CHECKER.ROUTING_BASIS_REF).read_bytes()
            )
            self.write_json(corpus, CHECKER.CONTACT_LIMITED_STATE_REL, state)
            self.write_json(corpus, CHECKER.COHERENCE_PROFILE_REL, profile)
            ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertEqual(ids, set(CHECKER.OWNER_HELD_SOURCE_ROWS))
            self.assertEqual(errors, [])

            profile["axes"]["routing"]["debt_ids"].pop()
            self.write_json(corpus, CHECKER.COHERENCE_PROFILE_REL, profile)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("drifted from coherence" in error for error in errors), errors)

            profile["axes"]["routing"]["debt_ids"].append("OWNER_GATE_OPEN_TOPOLOGY")
            profile["axes"]["routing"]["state"] = "PASS"
            self.write_json(corpus, CHECKER.COHERENCE_PROFILE_REL, profile)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("must remain PASS_WITH_DEBT" in error for error in errors), errors)

            profile["axes"]["routing"]["state"] = "PASS_WITH_DEBT"
            profile["axes"]["routing"]["basis_refs"] = [CHECKER.WIP_MANIFEST_REL]
            self.write_json(corpus, CHECKER.COHERENCE_PROFILE_REL, profile)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("canonical receipt-only set" in error for error in errors), errors)

            alias = corpus / "wip-alias.md"
            os.link(wip_manifest, alias)
            profile["axes"]["routing"]["basis_refs"] = ["wip-alias.md"]
            self.write_json(corpus, CHECKER.COHERENCE_PROFILE_REL, profile)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("canonical receipt-only set" in error for error in errors), errors)

            copied_basis = corpus / "scratch_basis.md"
            copied_basis.write_bytes(wip_manifest.read_bytes())
            profile["axes"]["routing"]["basis_refs"] = ["scratch_basis.md"]
            self.write_json(corpus, CHECKER.COHERENCE_PROFILE_REL, profile)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("canonical receipt-only set" in error for error in errors), errors)

            profile["axes"]["routing"]["basis_refs"] = [CHECKER.ROUTING_BASIS_REF]
            receipt.write_bytes(wip_manifest.read_bytes())
            self.write_json(corpus, CHECKER.COHERENCE_PROFILE_REL, profile)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("basis receipt digest drifted" in error for error in errors), errors)
            receipt.write_bytes((ROOT / CHECKER.ROUTING_BASIS_REF).read_bytes())

            state["owner_held"]["debts"][0]["owner"] = "Alice Example, selected owner"
            self.write_json(corpus, CHECKER.CONTACT_LIMITED_STATE_REL, state)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("exact held source contract" in error for error in errors), errors)

            state["owner_held"]["debts"][0] = copy.deepcopy(
                CHECKER.OWNER_HELD_SOURCE_ROWS["OWNER_GATE_HELD_PUBLIC_DOCS"]["state_debt"]
            )
            state["owner_held"]["debts"][0]["question"] = (
                "Alice Example is selected; contact is authorized."
            )
            self.write_json(corpus, CHECKER.CONTACT_LIMITED_STATE_REL, state)
            _ids, errors = CHECKER.owner_held_source_ids(corpus)
            self.assertTrue(any("exact held source contract" in error for error in errors), errors)

    def test_review_source_rejects_contact_or_owner_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            registry = CHECKER.load_json_object(
                ROOT, CHECKER.REVIEW_REGISTRY_REL, "live review gate registry"
            )
            self.write_json(corpus, CHECKER.REVIEW_REGISTRY_REL, registry)
            self.assertEqual(CHECKER.review_contact_authority_errors(corpus), [])

            promoted_contact = copy.deepcopy(registry)
            next(
                gate
                for gate in promoted_contact["gates"]
                if gate.get("gate_id") == "FPE-REVIEW-01"
            )["contact_status"] = "ready"
            self.write_json(corpus, CHECKER.REVIEW_REGISTRY_REL, promoted_contact)
            errors = CHECKER.review_contact_authority_errors(corpus)
            self.assertTrue(any("contact deferred" in error for error in errors), errors)

            promoted_owner = copy.deepcopy(registry)
            next(
                gate
                for gate in promoted_owner["gates"]
                if gate.get("gate_id") == "FPE-REVIEW-01"
            )["execution"]["provenance_contract"][
                "owner_authority"
            ]["state_at_freeze"] = "selected"
            self.write_json(corpus, CHECKER.REVIEW_REGISTRY_REL, promoted_owner)
            errors = CHECKER.review_contact_authority_errors(corpus)
            self.assertTrue(any("owner authority" in error for error in errors), errors)

            contacted = copy.deepcopy(registry)
            contacted["external_state"]["reviewers_engaged"]["state"] = "present"
            self.write_json(corpus, CHECKER.REVIEW_REGISTRY_REL, contacted)
            errors = CHECKER.review_contact_authority_errors(corpus)
            self.assertTrue(any("external-state" in error for error in errors), errors)

            malformed = copy.deepcopy(registry)
            malformed["gates"] = None
            self.write_json(corpus, CHECKER.REVIEW_REGISTRY_REL, malformed)
            errors = CHECKER.review_contact_authority_errors(corpus)
            self.assertTrue(any("gates must be a list" in error for error in errors), errors)

    def test_docket_rows_must_remain_exactly_unset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            docket = (ROOT / CHECKER.OWNER_DOCKET_REL).read_text(encoding="utf-8")
            path = corpus / CHECKER.OWNER_DOCKET_REL
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(docket, encoding="utf-8")
            self.assertEqual(CHECKER.owner_docket_unset_errors(corpus), [])
            path.write_text(
                docket.replace(
                    "`D-OWNER-02` | Disposition of the grandfathered framework-support "
                    "`00_META` tombstones under the root-only rule | **UNSET**",
                    "`D-OWNER-02` | Disposition of the grandfathered framework-support "
                    "`00_META` tombstones under the root-only rule | **SELECTED**",
                )
                + "\n\n## Historical Notes\n\n"
                "| `D-OWNER-02` | decoy | **UNSET** | decoy |\n",
                encoding="utf-8",
            )
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("D-OWNER-02" in error for error in errors), errors)

            path.write_text(
                docket.replace(
                    "| `D-OWNER-01` | Canonical owner for the byte-identical public planning duplicate | "
                    "**UNSET** | current/custody routing of two public-site planning copies |",
                    "| `D-OWNER-01` | **UNSET** | **SELECTED** | "
                    "current/custody routing of two public-site planning copies |",
                ),
                encoding="utf-8",
            )
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("D-OWNER-01" in error for error in errors), errors)

            status_rows = CHECKER.owner_docket_status_table(docket)
            assert status_rows is not None

            status_table = (
                "| ID | Decision | Current state | Blocks |\n"
                "|---|---|---|---|\n"
                + status_rows
            )
            path.write_text(
                docket.replace(status_table, "<!--\n" + status_table + "-->\n", 1),
                encoding="utf-8",
            )
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("status-and-boundary" in error for error in errors), errors)

            path.write_text(
                "--- \n## Status and boundary\n\n" + status_table + "--- \n",
                encoding="utf-8",
            )
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("status-and-boundary" in error for error in errors), errors)

            path.write_text(
                "\ufeff---\n## Status and boundary\n\n" + status_table + "---\n",
                encoding="utf-8",
            )
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("status-and-boundary" in error for error in errors), errors)

            path.write_text(
                docket.replace(
                    "| `D-OWNER-01` | Canonical owner for the byte-identical public planning duplicate | "
                    "**UNSET** | current/custody routing of two public-site planning copies |\n",
                    "",
                )
                + "\n```text\n"
                "| `D-OWNER-01` | Canonical owner for the byte-identical public planning duplicate | "
                "**UNSET** | current/custody routing of two public-site planning copies |\n"
                "```\n",
                encoding="utf-8",
            )
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("D-OWNER-01" in error for error in errors), errors)

            selected_decision = docket.replace(
                "| `D-OWNER-01` | Canonical owner for the byte-identical public planning duplicate | "
                "**UNSET** | current/custody routing of two public-site planning copies |",
                "| `D-OWNER-01` | Alice Example selected as canonical owner | **UNSET** | "
                "current/custody routing of two public-site planning copies |",
            )
            path.write_text(selected_decision, encoding="utf-8")
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("D-OWNER-01" in error for error in errors), errors)

            duplicate_selection = docket.replace(
                "- **Selected option:** **UNSET**.",
                "- **Selected option:** **UNSET**.\n- **Selected option:** Alice Example.",
                1,
            )
            path.write_text(duplicate_selection, encoding="utf-8")
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("exact UNSET selection" in error for error in errors), errors)

            duplicate_principal = docket.replace(
                "- **Principal:** **UNSET** (01_EMERGENTISM editorial owner must name one).",
                "- **Principal:** **UNSET** (01_EMERGENTISM editorial owner must name one).\n"
                "- **Principal:** Alice Example.",
                1,
            )
            path.write_text(duplicate_principal, encoding="utf-8")
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("exact UNSET principal" in error for error in errors), errors)

            path.write_text("<!--\n" + docket + "-->\n", encoding="utf-8")
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("status-and-boundary" in error for error in errors), errors)
            path.write_text("```markdown\n" + docket + "```\n", encoding="utf-8")
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("status-and-boundary" in error for error in errors), errors)

            for tag in ("script", "style", "pre", "textarea", "template"):
                with self.subTest(raw_html_block=tag):
                    path.write_text(
                        f"<{tag}>\n" + docket + f"</{tag}>\n",
                        encoding="utf-8",
                    )
                    errors = CHECKER.owner_docket_unset_errors(corpus)
                    self.assertTrue(any("status-and-boundary" in error for error in errors), errors)

            path.write_text(
                "---\n## Status and boundary\n\n"
                + status_table
                + "---\n",
                encoding="utf-8",
            )
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("status-and-boundary" in error for error in errors), errors)

    def test_topology_row_cannot_be_reworded_as_present_conformance(self) -> None:
        row = CHECKER.OWNER_HELD_SOURCE_ROWS["OWNER_GATE_OPEN_TOPOLOGY"]
        self.assertIn("categorical root-only rule", row["question"])
        self.assertIn("No move or conformance is implied", row["question"])
        mutated = self.mutate_open_row(
            "OWNER_GATE_OPEN_TOPOLOGY",
            row["question"],
            "Is the existing non-root path already conforming?",
        )
        errors = CHECKER.source_mirror_errors(ROOT, mutated)
        self.assertTrue(
            any("OWNER_GATE_OPEN_TOPOLOGY" in error for error in errors),
            errors,
        )

    def test_source_readers_reject_symlinks_and_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outer = Path(directory)
            corpus = outer / "corpus"
            corpus.mkdir()
            outside = outer / "outside.json"
            outside.write_text("{}", encoding="utf-8")
            for relative in (
                CHECKER.CONTACT_LIMITED_STATE_REL,
                CHECKER.COHERENCE_PROFILE_REL,
                CHECKER.REVIEW_REGISTRY_REL,
            ):
                path = corpus / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(outside)
                with self.assertRaisesRegex(ValueError, "must not traverse a symlink"):
                    CHECKER.load_json_object(corpus, relative, "test JSON source")
                path.unlink()

            state_path = corpus / CHECKER.CONTACT_LIMITED_STATE_REL
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_bytes(b"\xff")
            with self.assertRaisesRegex(ValueError, "unreadable"):
                CHECKER.load_json_object(corpus, CHECKER.CONTACT_LIMITED_STATE_REL, "state")

            docket_path = corpus / CHECKER.OWNER_DOCKET_REL
            docket_path.parent.mkdir(parents=True, exist_ok=True)
            docket_path.write_bytes(b"\xff")
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(any("owner decision docket is unreadable" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
