from __future__ import annotations

import copy
import hashlib
import inspect
import itertools
import json
import sys
import tempfile
import typing
import unicodedata
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parent))
import kintsugi_kernel as kernel
import kintsugi_kernel.markdown as markdown_module
import kintsugi_test_support as support


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
NARRATIVE_DOMAIN = b"KINTSUGI-NARRATIVE-V1\x00"


def seam_record(seam_id: str = "KIN-A-001") -> dict:
    core = support.build_semantic_core()
    return copy.deepcopy(support.add_retiered_seam(core, "A", "S", seam_id=seam_id))


def issue_codes(result) -> list[str]:
    return [issue.code for issue in result.issues]


def issue_offsets(result) -> list[int]:
    return [int(issue.path.rsplit("@", 1)[1]) for issue in result.issues]


def replace_fence_json(payload: bytes, role: str, replacement: bytes) -> bytes:
    opener = b"```json " + role.encode("ascii") + b"\n"
    start = payload.index(opener) + len(opener)
    end = payload.index(b"```", start)
    return payload[:start] + replacement + b"\n" + payload[end:]


class HugeBytes:
    def __len__(self):
        return 1 << 64

    def __bytes__(self):
        raise AssertionError("overflow must be refused before materialization")


class LengthBoom:
    def __len__(self):
        raise RuntimeError("length boom")


class BytesBoom:
    def __len__(self):
        return 1

    def __bytes__(self):
        raise RuntimeError("bytes boom")


class LengthControl:
    def __len__(self):
        raise KeyboardInterrupt


class RootPathBoom:
    def __fspath__(self):
        raise RuntimeError("root path boom")


class RootPathControl:
    def __fspath__(self):
        raise KeyboardInterrupt


class TrialSeamIdProbe(dict):
    seam_id_reads = 0

    def get(self, key, default=None):
        if key == "seamId":
            type(self).seam_id_reads += 1
        return super().get(key, default)


class DecodeProbeBytes(bytes):
    decode_calls = 0

    def decode(self, *args, **kwargs):
        type(self).decode_calls += 1
        return super().decode(*args, **kwargs)


def build_shared_owner_core(
    root: Path, count: int, *, tracked_trials: bool = False
) -> tuple[dict[str, object], Path]:
    source, base_claim, base_trial, base_seam, owner = (
        support.build_owner_sync_fixture(root)
    )
    claims = []
    trials = []
    seams = []
    current_quotes = []
    for index in range(1, count + 1):
        suffix = f"{index:03}"
        claim = copy.deepcopy(base_claim)
        claim["id"] = f"CLM-A-{suffix}"
        trial = copy.deepcopy(base_trial)
        trial.update({
            "id": f"TRL-A-{suffix}",
            "claimId": claim["id"],
            "seamId": f"KIN-A-{suffix}",
        })
        if tracked_trials:
            trial = TrialSeamIdProbe(trial)
        seam = copy.deepcopy(base_seam)
        current_quote = f"The repaired owner claim {suffix}."
        seam.update({
            "id": f"KIN-A-{suffix}",
            "claimId": claim["id"],
            "afterQuote": current_quote,
            "priorSeamIds": [],
        })
        claims.append(claim)
        trials.append(trial)
        seams.append(seam)
        current_quotes.append(current_quote)

    raw = (
        "# Owner\n\n## Synthetic owner anchor\n\n"
        + "\n".join(current_quotes)
        + "\n"
    ).encode("utf-8")
    owner.write_bytes(raw)
    source["sha256"] = kernel.raw_hash(raw)
    core: dict[str, object] = {
        "sources": [source],
        "claims": claims,
        "trials": trials,
        "seams": seams,
        "phaseReceipts": [],
        "reviewAttestations": [],
        "reviewFindings": [],
        "reviewAttemptArtifacts": [],
    }
    return core, owner


class NarrativeHashTests(unittest.TestCase):
    def test_framed_hash_uses_exact_domain_lengths_and_raw_bytes(self):
        prefix = b"alpha\r\n"
        suffix = b"\xffomega\n"
        expected = "sha256:" + hashlib.sha256(
            NARRATIVE_DOMAIN
            + len(prefix).to_bytes(8, "big") + prefix
            + len(suffix).to_bytes(8, "big") + suffix
        ).hexdigest()
        self.assertEqual(kernel.framed_narrative_hash(prefix, suffix), expected)

    def test_framing_distinguishes_the_same_concatenation_across_sides(self):
        self.assertNotEqual(
            kernel.framed_narrative_hash(b"ab", b"c"),
            kernel.framed_narrative_hash(b"a", b"bc"),
        )

    def test_framed_hash_refuses_uint64_length_overflow_before_materialization(self):
        with self.assertRaises(kernel.KintsugiError) as caught:
            kernel.framed_narrative_hash(HugeBytes(), b"")
        self.assertEqual(caught.exception.code, "KIN-E-LEDGER")

    def test_framed_hash_controls_ordinary_conversion_errors_only(self):
        for value in (LengthBoom(), BytesBoom()):
            with self.subTest(value=value):
                with self.assertRaises(kernel.KintsugiError) as caught:
                    kernel.framed_narrative_hash(value, b"")
                self.assertEqual(caught.exception.code, "KIN-E-LEDGER")

        with self.assertRaises(KeyboardInterrupt):
            kernel.framed_narrative_hash(LengthControl(), b"")


class StableMarkdownApiTests(unittest.TestCase):
    def test_stable_markdown_apis_have_exact_signatures_and_package_exports(self):
        self.assertIs(kernel.extract_fenced_json, markdown_module.extract_fenced_json)
        self.assertIs(kernel.validate_markdown_sync, markdown_module.validate_markdown_sync)

        extract_signature = inspect.signature(kernel.extract_fenced_json)
        self.assertEqual(tuple(extract_signature.parameters), ("markdown", "fence_kind"))
        self.assertTrue(all(
            parameter.default is inspect.Parameter.empty
            for parameter in extract_signature.parameters.values()
        ))
        self.assertEqual(
            typing.get_type_hints(kernel.extract_fenced_json),
            {"markdown": bytes, "fence_kind": str, "return": list[object]},
        )

        validate_signature = inspect.signature(kernel.validate_markdown_sync)
        self.assertEqual(
            tuple(validate_signature.parameters), ("root", "core", "ledger_path")
        )
        self.assertTrue(all(
            parameter.default is inspect.Parameter.empty
            for parameter in validate_signature.parameters.values()
        ))
        self.assertEqual(
            typing.get_type_hints(kernel.validate_markdown_sync),
            {
                "root": Path,
                "core": dict[str, object],
                "ledger_path": Path | None,
                "return": list[kernel.Issue],
            },
        )

        owner_signature = inspect.signature(kernel.synchronize_owner)
        self.assertEqual(
            tuple(owner_signature.parameters),
            ("root", "source", "claim", "trial", "seam"),
        )
        self.assertTrue(all(
            parameter.default is inspect.Parameter.empty
            for parameter in owner_signature.parameters.values()
        ))

    def test_extract_fenced_json_returns_matching_values_in_source_order_read_only(self):
        first = {"id": "KIN-A-001"}
        second = ["KIN-A-002"]
        payload = (
            support.markdown_fence("kintsugi-seam", first)
            + support.markdown_fence("kintsugi-receipt", {"id": "REC-A-001"})
            + support.markdown_fence("kintsugi-seam", second)
        )
        before = bytes(payload)

        self.assertEqual(
            kernel.extract_fenced_json(payload, "kintsugi-seam"),
            [first, second],
        )
        self.assertEqual(payload, before)

    def test_extract_fenced_json_fails_closed_with_a_typed_deterministic_error(self):
        malformed = b"````json kintsugi-seam\n{}\n````\n"
        for markdown, fence_kind in (
            (malformed, "kintsugi-seam"),
            (b"```json kintsugi-seam\n{broken\n```\n", "kintsugi-seam"),
            (b"", ""),
        ):
            with self.subTest(markdown=markdown, fence_kind=fence_kind):
                with self.assertRaises(kernel.KintsugiError) as caught:
                    kernel.extract_fenced_json(markdown, fence_kind)
                self.assertIn(caught.exception.code, {"KIN-E-JSON", "KIN-E-LEDGER"})


class JsonIntegerBoundaryTests(unittest.TestCase):
    def integer_payload(self, digits: int) -> bytes:
        return (
            b"```json kintsugi-seam\n{\"n\":"
            + b"7" * digits
            + b"}\n```\n"
        )

    def test_large_integer_rejection_is_independent_of_process_global_limit(self):
        has_limit = hasattr(sys, "set_int_max_str_digits")
        original = sys.get_int_max_str_digits() if has_limit else None
        payload = self.integer_payload(5_000)
        try:
            process_limits = (640, 0) if has_limit else (None,)
            for process_limit in process_limits:
                with self.subTest(process_limit=process_limit):
                    if process_limit is not None:
                        sys.set_int_max_str_digits(process_limit)
                    with self.assertRaises(kernel.KintsugiError) as caught:
                        kernel.extract_fenced_json(payload, "kintsugi-seam")
                    self.assertEqual(caught.exception.code, "KIN-E-JSON")
        finally:
            if has_limit:
                sys.set_int_max_str_digits(original)

    def test_json_integer_uses_a_fixed_4096_digit_ceiling(self):
        has_limit = hasattr(sys, "set_int_max_str_digits")
        original = sys.get_int_max_str_digits() if has_limit else None
        try:
            process_limits = (640, 0) if has_limit else (None,)
            for process_limit in process_limits:
                with self.subTest(process_limit=process_limit):
                    if process_limit is not None:
                        sys.set_int_max_str_digits(process_limit)
                    try:
                        accepted = kernel.extract_fenced_json(
                            self.integer_payload(4_096), "kintsugi-seam"
                        )
                    except kernel.KintsugiError as exc:
                        self.fail(
                            "4096 digits must be accepted independently of "
                            f"the process limit; got {exc.code}: {exc.message}"
                        )
                    self.assertEqual(len(accepted), 1)
                    self.assertIsInstance(accepted[0]["n"], int)
                    with self.assertRaises(kernel.KintsugiError) as caught:
                        kernel.extract_fenced_json(
                            self.integer_payload(4_097), "kintsugi-seam"
                        )
                    self.assertEqual(caught.exception.code, "KIN-E-JSON")
                    with self.assertRaises(kernel.KintsugiError) as caught:
                        kernel.extract_fenced_json(
                            self.integer_payload(5_000), "kintsugi-seam"
                        )
                    self.assertEqual(caught.exception.code, "KIN-E-JSON")
        finally:
            if has_limit:
                sys.set_int_max_str_digits(original)

    def test_json_parser_does_not_mask_direct_baseexceptions(self):
        with mock.patch.object(
            markdown_module.json, "loads", side_effect=KeyboardInterrupt
        ):
            with self.assertRaises(KeyboardInterrupt):
                kernel.extract_fenced_json(
                    b"```json kintsugi-seam\n{}\n```\n",
                    "kintsugi-seam",
                )


class AggregateMarkdownSynchronizationTests(unittest.TestCase):
    def build_repository(self, root: Path):
        source, claim, trial, seam, _ = support.build_owner_sync_fixture(root)
        trial["seamId"] = seam["id"]
        core = support.build_core_data()
        core["sources"] = [source]
        core["claims"] = [claim]
        core["trials"] = [trial]
        core["seams"] = [seam]

        receipt = core["phaseReceipts"][0]
        receipt.update({
            "path": "receipts/phase.md",
            "claimIds": [claim["id"]],
            "trialIds": [trial["id"]],
            "seamIds": [seam["id"]],
        })
        receipt_path = root / receipt["path"]
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_bytes(support.build_receipt_markdown(receipt))

        finding = support.build_review_finding()
        finding.update({
            "claimIds": [claim["id"]],
            "seamIds": [seam["id"]],
            "subjectPaths": [source["path"]],
        })
        attestation = support.build_review_attestation("LOGIC", "FAIL")
        attestation["path"] = "reviews/logic.md"
        core["reviewAttestations"] = [attestation]
        core["reviewFindings"] = [finding]
        review_path = root / attestation["path"]
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_bytes(
            support.build_review_markdown(attestation, [finding])
        )

        ledger_path = Path("ledger.md")
        (root / ledger_path).write_bytes(support.build_ledger_markdown([seam]))
        return core, ledger_path

    @staticmethod
    def tree_snapshot(root: Path):
        return tuple(sorted(
            (path.relative_to(root).as_posix(), path.read_bytes())
            for path in root.rglob("*") if path.is_file()
        ))

    def test_validate_markdown_sync_coordinates_all_task4_layers_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, ledger_path = self.build_repository(root)
            before = self.tree_snapshot(root)

            issues = kernel.validate_markdown_sync(root, core, ledger_path)

            self.assertEqual(issues, [])
            self.assertEqual(self.tree_snapshot(root), before)

    def test_allocated_attempt_does_not_freeze_prose_until_target_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, ledger_path = self.build_repository(root)
            receipt = core["phaseReceipts"][0]
            receipt["reviewAttemptId"] = support.ATTEMPT_ID
            core["reviewAttempts"] = [support.build_review_attempt()]
            core["reviewAttemptArtifacts"] = [{
                **support.build_review_attempt_artifact(),
                "reviewTargetSha256": None,
            }]
            receipt_path = root / receipt["path"]
            receipt_path.write_bytes(support.build_receipt_markdown(
                receipt,
                prefix=b"# Synthetic receipt\n\nLogic approved.\n",
            ))

            allocated_only = kernel.validate_markdown_sync(root, core, ledger_path)
            self.assertEqual(allocated_only, [])

            core["reviewAttemptArtifacts"][0]["reviewTargetSha256"] = support.RAW_HASH
            target_present = kernel.validate_markdown_sync(root, core, ledger_path)
            self.assertTrue(any(
                issue.code == "KIN-E-LEDGER"
                and "dynamic receipt prose" in issue.message
                for issue in target_present
            ))

    def test_only_current_leaf_seam_is_checked_against_current_owner_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, ledger_path = self.build_repository(root)
            current = core["seams"][0]
            historical = copy.deepcopy(current)
            historical.update({
                "id": "KIN-A-000",
                "afterQuote": "A superseded repaired owner claim.",
                "priorSeamIds": [],
            })
            current["priorSeamIds"] = [historical["id"]]
            historical_trial = copy.deepcopy(core["trials"][0])
            historical_trial.update({"id": "TRL-A-000", "seamId": historical["id"]})
            core["trials"].insert(0, historical_trial)
            core["seams"].insert(0, historical)
            core["phaseReceipts"][0]["trialIds"].insert(0, historical_trial["id"])
            core["phaseReceipts"][0]["seamIds"].insert(0, historical["id"])
            receipt = core["phaseReceipts"][0]
            (root / receipt["path"]).write_bytes(support.build_receipt_markdown(receipt))
            (root / ledger_path).write_bytes(
                support.build_ledger_markdown(core["seams"])
            )

            self.assertEqual(
                kernel.validate_markdown_sync(root, core, ledger_path),
                [],
            )

    def test_multiple_current_leaf_seams_are_a_typed_owner_ambiguity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, ledger_path = self.build_repository(root)
            sibling = copy.deepcopy(core["seams"][0])
            sibling.update({"id": "KIN-A-002", "priorSeamIds": []})
            core["seams"][0]["priorSeamIds"] = []
            sibling_trial = copy.deepcopy(core["trials"][0])
            sibling_trial.update({"id": "TRL-A-002", "seamId": sibling["id"]})
            core["seams"].append(sibling)
            core["trials"].append(sibling_trial)
            receipt = core["phaseReceipts"][0]
            receipt["seamIds"].append(sibling["id"])
            receipt["trialIds"].append(sibling_trial["id"])
            (root / receipt["path"]).write_bytes(support.build_receipt_markdown(receipt))
            (root / ledger_path).write_bytes(support.build_ledger_markdown(core["seams"]))

            issues = kernel.validate_markdown_sync(root, core, ledger_path)

            self.assertTrue(any(
                issue.code == "KIN-E-QUOTE" and "current leaf" in issue.message
                for issue in issues
            ))

    def test_validate_markdown_sync_is_exception_total_but_not_baseexception_total(self):
        issues = kernel.validate_markdown_sync(RootPathBoom(), {}, None)
        self.assertTrue(issues)
        self.assertTrue(all(isinstance(issue, kernel.Issue) for issue in issues))
        with self.assertRaises(KeyboardInterrupt):
            kernel.validate_markdown_sync(RootPathControl(), {}, None)

    def test_current_trial_index_reads_seam_ids_only_linearly(self):
        for count in (10, 100):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                core, _ = build_shared_owner_core(
                    root, count, tracked_trials=True
                )
                TrialSeamIdProbe.seam_id_reads = 0

                issues = kernel.validate_markdown_sync(root, core, None)

                self.assertEqual(issues, [])
                self.assertLessEqual(
                    TrialSeamIdProbe.seam_id_reads,
                    2 * count,
                    "trial seamId lookups must remain linear",
                )

    def test_trial_index_reports_malformed_and_duplicate_seam_bindings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            malformed_core, _ = build_shared_owner_core(root, 1)
            malformed_core["trials"].append({
                "id": "TRL-A-BAD",
                "claimId": "CLM-A-001",
            })

            malformed = kernel.validate_markdown_sync(
                root, malformed_core, None
            )

            self.assertTrue(any(
                issue.code == "KIN-E-QUOTE"
                and "trial seamId must be a string" in issue.message
                for issue in malformed
            ))
            self.assertEqual(malformed, sorted(set(malformed)))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            duplicate_core, _ = build_shared_owner_core(root, 1)
            duplicate = copy.deepcopy(duplicate_core["trials"][0])
            duplicate["id"] = "TRL-A-999"
            duplicate_core["trials"].append(duplicate)

            duplicate_issues = kernel.validate_markdown_sync(
                root, duplicate_core, None
            )

            self.assertTrue(any(
                issue.code == "KIN-E-QUOTE"
                and "exactly one trial" in issue.message
                for issue in duplicate_issues
            ))
            self.assertEqual(duplicate_issues, sorted(set(duplicate_issues)))

    def test_trial_index_reports_duplicate_binding_off_the_current_leaf(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, _ = build_shared_owner_core(root, 1)
            current = core["seams"][0]
            historical = copy.deepcopy(current)
            historical.update({
                "id": "KIN-A-000",
                "priorSeamIds": [],
            })
            current["priorSeamIds"] = [historical["id"]]
            core["seams"].append(historical)
            for suffix in ("001", "002"):
                historical_trial = copy.deepcopy(core["trials"][0])
                historical_trial.update({
                    "id": f"TRL-A-HIST-{suffix}",
                    "seamId": historical["id"],
                })
                core["trials"].append(historical_trial)

            issues = kernel.validate_markdown_sync(root, core, None)

            self.assertTrue(any(
                issue.code == "KIN-E-QUOTE"
                and "duplicate trial seamId binding" in issue.message
                and historical["id"] in issue.message
                for issue in issues
            ))
            self.assertEqual(issues, sorted(set(issues)))

    def test_aggregate_reads_each_shared_owner_once_at_all_scales(self):
        real_read_bytes = Path.read_bytes
        for count in (1, 10, 100):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                core, owner = build_shared_owner_core(root, count)
                resolved_owner = owner.resolve()
                owner_reads = 0

                def counting_read(path):
                    nonlocal owner_reads
                    if path.resolve() == resolved_owner:
                        owner_reads += 1
                    return real_read_bytes(path)

                with mock.patch.object(Path, "read_bytes", counting_read):
                    issues = kernel.validate_markdown_sync(root, core, None)

                self.assertEqual(issues, [])
                self.assertEqual(owner_reads, 1)

    def test_aggregate_owner_checks_share_one_frozen_byte_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, owner = build_shared_owner_core(root, 2)
            resolved_owner = owner.resolve()
            original = owner.read_bytes()
            owner_reads = 0
            real_read_bytes = Path.read_bytes

            def changing_read(path):
                nonlocal owner_reads
                if path.resolve() != resolved_owner:
                    return real_read_bytes(path)
                owner_reads += 1
                if owner_reads == 1:
                    return original
                return b"# Owner changed between verification reads.\n"

            with mock.patch.object(Path, "read_bytes", changing_read):
                issues = kernel.validate_markdown_sync(root, core, None)

            self.assertEqual(issues, [])
            self.assertEqual(owner_reads, 1)

    def test_aggregate_derives_shared_owner_bytes_only_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, owner = build_shared_owner_core(root, 100)
            resolved_owner = owner.resolve()
            raw = owner.read_bytes()
            owner_text = raw.decode("utf-8")
            probed_raw = DecodeProbeBytes(raw)
            real_read_bytes = Path.read_bytes
            real_raw_hash = markdown_module.raw_hash
            real_normalize_lf = markdown_module.normalize_lf
            owner_hashes = 0
            owner_normalizations = 0
            DecodeProbeBytes.decode_calls = 0

            def probing_read(path):
                if path.resolve() == resolved_owner:
                    return probed_raw
                return real_read_bytes(path)

            def counting_raw_hash(payload):
                nonlocal owner_hashes
                if payload is probed_raw:
                    owner_hashes += 1
                return real_raw_hash(payload)

            def counting_normalize_lf(text):
                nonlocal owner_normalizations
                if text == owner_text:
                    owner_normalizations += 1
                return real_normalize_lf(text)

            with (
                mock.patch.object(Path, "read_bytes", probing_read),
                mock.patch.object(
                    markdown_module, "raw_hash", counting_raw_hash
                ),
                mock.patch.object(
                    markdown_module, "normalize_lf", counting_normalize_lf
                ),
            ):
                issues = kernel.validate_markdown_sync(root, core, None)

            self.assertEqual(issues, [])
            self.assertEqual(
                (
                    owner_hashes,
                    DecodeProbeBytes.decode_calls,
                    owner_normalizations,
                ),
                (1, 1, 1),
            )

    def test_aggregate_builds_one_owner_view_and_substring_index(self):
        view_builder = getattr(markdown_module, "_build_owner_view", None)
        index_builder = getattr(
            markdown_module, "_build_owner_substring_index", None
        )
        self.assertTrue(callable(view_builder), "owner view builder is absent")
        self.assertTrue(callable(index_builder), "owner index builder is absent")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, _ = build_shared_owner_core(root, 100)
            with (
                mock.patch.object(
                    markdown_module,
                    "_build_owner_view",
                    wraps=view_builder,
                ) as build_view,
                mock.patch.object(
                    markdown_module,
                    "_build_owner_substring_index",
                    wraps=index_builder,
                ) as build_index,
            ):
                issues = kernel.validate_markdown_sync(root, core, None)

            self.assertEqual(issues, [])
            self.assertEqual(build_view.call_count, 1)
            self.assertEqual(build_index.call_count, 1)

    def test_aggregate_owner_view_preserves_overlap_crlf_and_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, owner = build_shared_owner_core(root, 1)
            raw = b"# Owner\n\n## Synthetic owner anchor\n\naaaa\n"
            owner.write_bytes(raw)
            core["sources"][0]["sha256"] = kernel.raw_hash(raw)
            core["seams"][0]["afterQuote"] = "aaa"

            overlap = kernel.validate_markdown_sync(root, core, None)

            self.assertTrue(any(
                issue.code == "KIN-E-QUOTE"
                and "exactly once" in issue.message
                for issue in overlap
            ))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, owner = build_shared_owner_core(root, 2)
            raw = owner.read_bytes().replace(b"\n", b"\r\n")
            owner.write_bytes(raw)
            core["sources"][0]["sha256"] = kernel.raw_hash(raw)

            self.assertEqual(
                kernel.validate_markdown_sync(root, core, None), []
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, owner = build_shared_owner_core(root, 2)
            raw = owner.read_bytes() + b"\xff"
            owner.write_bytes(raw)
            core["sources"][0]["sha256"] = kernel.raw_hash(raw)

            invalid = kernel.validate_markdown_sync(root, core, None)

            self.assertTrue(invalid)
            self.assertEqual({issue.code for issue in invalid}, {"KIN-E-QUOTE"})
            self.assertTrue(any(
                "strict UTF-8" in issue.message for issue in invalid
            ))

    def test_resolved_owner_snapshot_skips_repeated_file_kind_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, owner = build_shared_owner_core(root, 2)
            alias = owner.with_name("owner-alias.md")
            alias.symlink_to(owner)
            alias_source = copy.deepcopy(core["sources"][0])
            alias_source.update({
                "id": "SRC-A-002",
                "path": alias.relative_to(root).as_posix(),
            })
            core["sources"].append(alias_source)
            core["claims"][1]["ownerSourceId"] = alias_source["id"]
            core["seams"][1]["ownerSource"] = alias_source["id"]
            resolved_owner = owner.resolve()
            owner_kind_checks = 0
            real_is_file = Path.is_file

            def counting_is_file(path):
                nonlocal owner_kind_checks
                if path.resolve() == resolved_owner:
                    owner_kind_checks += 1
                return real_is_file(path)

            with mock.patch.object(Path, "is_file", counting_is_file):
                issues = kernel.validate_markdown_sync(root, core, None)

            self.assertEqual(issues, [])
            self.assertEqual(owner_kind_checks, 1)

    def test_resolved_owner_snapshot_caches_failed_read_across_aliases(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core, owner = build_shared_owner_core(root, 2)
            alias = owner.with_name("owner-alias.md")
            alias.symlink_to(owner)
            alias_source = copy.deepcopy(core["sources"][0])
            alias_source.update({
                "id": "SRC-A-002",
                "path": alias.relative_to(root).as_posix(),
            })
            core["sources"].append(alias_source)
            core["claims"][1]["ownerSourceId"] = alias_source["id"]
            core["seams"][1]["ownerSource"] = alias_source["id"]
            resolved_owner = owner.resolve()
            owner_read_attempts = 0
            real_read_bytes = Path.read_bytes

            def failing_read(path):
                nonlocal owner_read_attempts
                if path.resolve() == resolved_owner:
                    owner_read_attempts += 1
                    raise OSError("synthetic owner read failure")
                return real_read_bytes(path)

            with mock.patch.object(Path, "read_bytes", failing_read):
                issues = kernel.validate_markdown_sync(root, core, None)

            self.assertEqual(owner_read_attempts, 1)
            self.assertEqual(
                {issue.path.split("@", 1)[0] for issue in issues},
                {
                    core["sources"][0]["path"],
                    alias_source["path"],
                },
            )
            self.assertTrue(all(
                issue.code == "KIN-E-QUOTE"
                and "unreadable" in issue.message
                for issue in issues
            ))


class LedgerSynchronizationTests(unittest.TestCase):
    def container_variants(self):
        for newline in (b"\n", b"\r\n"):
            for marker in (b"````", b"~~~"):
                for indent in range(4):
                    yield newline, marker, b" " * indent

    def test_literal_heading_cannot_supply_a_live_seam_section(self):
        seam = seam_record()
        for newline, marker, indent in self.container_variants():
            with self.subTest(
                newline=newline, marker=marker, indent=len(indent)
            ):
                payload = (
                    b"# Ledger" + newline + newline
                    + indent + marker + b"text" + newline
                    + b"## KIN-A-001" + newline
                    + indent + marker + newline
                    + b"Narrative only." + newline
                    + support.markdown_fence(
                        "kintsugi-seam", seam, newline=newline
                    )
                )

                result = kernel.synchronize_ledger_markdown(payload, [seam])

                self.assertTrue(result.issues)
                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "missing ledger section" in issue.message
                    for issue in result.issues
                ))

    def test_enclosed_literal_heading_and_role_are_never_machine_records(self):
        seam = seam_record()
        for newline, marker, indent in self.container_variants():
            with self.subTest(
                newline=newline, marker=marker, indent=len(indent)
            ):
                payload = (
                    b"# Ledger" + newline + newline
                    + indent + marker + b"text" + newline
                    + b"## KIN-A-001" + newline
                    + support.markdown_fence(
                        "kintsugi-seam", seam, newline=newline
                    )
                    + indent + marker + newline
                )

                result = kernel.synchronize_ledger_markdown(payload, [seam])

                self.assertTrue(result.issues)
                self.assertEqual(
                    kernel.extract_fenced_json(payload, "kintsugi-seam"), []
                )

    def test_literal_example_headings_do_not_create_extra_sections(self):
        seam = seam_record()
        for newline, marker, indent in self.container_variants():
            with self.subTest(
                newline=newline, marker=marker, indent=len(indent)
            ):
                payload = support.build_ledger_markdown(
                    [seam], newline=newline
                ) + (
                    newline
                    + indent + marker + b"text" + newline
                    + b"## KIN-A-999" + newline
                    + indent + marker + newline
                )

                result = kernel.synchronize_ledger_markdown(payload, [seam])

                self.assertEqual(result.issues, ())

    def test_lf_and_crlf_fence_boundaries_are_excluded_from_narrative_hash(self):
        seam = seam_record()
        for newline in (b"\n", b"\r\n"):
            with self.subTest(newline=newline):
                payload = support.build_ledger_markdown(
                    [seam], newline=newline, preamble=b"",
                    prefixes=[b"Prefix bytes."], suffixes=[b"Suffix bytes."],
                )
                section = kernel.synchronize_ledger_markdown(
                    payload, [seam]
                ).sections[0]
                expected_prefix = (
                    b"## KIN-A-001" + newline + b"Prefix bytes." + newline
                )
                expected_suffix = b"Suffix bytes." + newline
                expected_hash = "sha256:" + hashlib.sha256(
                    NARRATIVE_DOMAIN
                    + len(expected_prefix).to_bytes(8, "big") + expected_prefix
                    + len(expected_suffix).to_bytes(8, "big") + expected_suffix
                ).hexdigest()
                self.assertEqual(section.prefix, expected_prefix)
                self.assertEqual(section.suffix, expected_suffix)
                self.assertEqual(section.narrative_raw_sha256, expected_hash)

    def test_exact_preamble_sections_offsets_and_semantic_projections(self):
        first = seam_record("KIN-A-001")
        second = seam_record("KIN-A-002")
        preamble = b"# Ledger\nPreamble byte.\n"
        payload = support.build_ledger_markdown(
            [first, second], preamble=preamble,
            prefixes=[b"Before one.", b"Before two."],
            suffixes=[b"After one.", b"After two."],
        )
        result = kernel.synchronize_ledger_markdown(
            payload, [first, second], path="ledger.md"
        )

        self.assertEqual(result.issues, ())
        self.assertEqual(result.preamble.raw, preamble)
        self.assertEqual(result.preamble.start, 0)
        self.assertEqual(result.preamble.end, len(preamble))
        self.assertEqual(result.preamble.raw_sha256, kernel.raw_hash(preamble))
        self.assertEqual([section.id for section in result.sections], ["KIN-A-001", "KIN-A-002"])
        self.assertEqual(result.sections[0].start, payload.index(b"## KIN-A-001"))
        self.assertEqual(result.sections[0].end, payload.index(b"## KIN-A-002"))
        self.assertEqual(result.sections[1].end, len(payload))
        for section in result.sections:
            self.assertEqual(section.raw, payload[section.start:section.end])
            self.assertEqual(
                section.narrative_raw_sha256,
                kernel.framed_narrative_hash(section.prefix, section.suffix),
            )
            self.assertEqual(section.seam_record["id"], section.id)
            self.assertEqual(section.seam_projection, kernel.project_review_seam(section.seam_record))

    def test_empty_preamble_hash_and_crlf_bytes_are_preserved(self):
        seam = seam_record()
        payload = support.build_ledger_markdown(
            [seam], newline=b"\r\n", preamble=b"",
            prefixes=[b"Before\r\nraw."], suffixes=[b"After\r\nraw."],
        )
        before = bytes(payload)
        result = kernel.synchronize_ledger_markdown(payload, [seam], path="ledger.md")
        self.assertEqual(result.issues, ())
        self.assertEqual(result.preamble.raw_sha256, kernel.raw_hash(b""))
        self.assertEqual(result.sections[0].raw, payload)
        self.assertIn(b"\r\n", result.sections[0].prefix)
        self.assertEqual(payload, before)

    def test_unrelated_section_change_does_not_change_first_narrative_hash(self):
        seams = [seam_record("KIN-A-001"), seam_record("KIN-A-002")]
        first = support.build_ledger_markdown(
            seams, suffixes=[b"Stable one.", b"Version one."],
        )
        second = support.build_ledger_markdown(
            seams, suffixes=[b"Stable one.", b"Version two."],
        )
        parsed_one = kernel.synchronize_ledger_markdown(first, seams)
        parsed_two = kernel.synchronize_ledger_markdown(second, seams)
        self.assertEqual(parsed_one.sections[0].narrative_raw_sha256, parsed_two.sections[0].narrative_raw_sha256)
        self.assertNotEqual(parsed_one.sections[1].narrative_raw_sha256, parsed_two.sections[1].narrative_raw_sha256)

    def test_relocating_identical_prose_across_fence_changes_section_hash(self):
        seam = seam_record()
        left = support.build_ledger_markdown(
            [seam], prefixes=[b"A\nB"], suffixes=[b"C"], preamble=b"",
        )
        right = support.build_ledger_markdown(
            [seam], prefixes=[b"A"], suffixes=[b"B\nC"], preamble=b"",
        )
        left_section = kernel.synchronize_ledger_markdown(left, [seam]).sections[0]
        right_section = kernel.synchronize_ledger_markdown(right, [seam]).sections[0]
        self.assertEqual(left_section.prefix + left_section.suffix, right_section.prefix + right_section.suffix)
        self.assertNotEqual(left_section.narrative_raw_sha256, right_section.narrative_raw_sha256)

    def test_mechanical_gate_status_and_reviewer_paths_do_not_change_semantic_projection(self):
        candidate = seam_record()
        terminal = copy.deepcopy(candidate)
        terminal["status"] = "VERIFIED"
        for field, reviewer_path in (
            ("truthGate", "reviews/logic.md"),
            ("beautyGate", "reviews/btj.md"),
            ("justiceGate", "reviews/btj.md"),
        ):
            terminal[field]["status"] = "PASS"
            terminal[field]["reviewerPath"] = reviewer_path

        candidate_bytes = support.build_ledger_markdown([candidate])
        terminal_bytes = support.build_ledger_markdown([terminal])
        candidate_result = kernel.synchronize_ledger_markdown(candidate_bytes, [candidate])
        terminal_result = kernel.synchronize_ledger_markdown(terminal_bytes, [terminal])

        self.assertNotEqual(candidate_bytes, terminal_bytes)
        self.assertEqual(candidate_result.issues, ())
        self.assertEqual(terminal_result.issues, ())
        self.assertEqual(candidate_result.sections[0].prefix, terminal_result.sections[0].prefix)
        self.assertEqual(candidate_result.sections[0].suffix, terminal_result.sections[0].suffix)
        self.assertEqual(
            candidate_result.sections[0].narrative_raw_sha256,
            terminal_result.sections[0].narrative_raw_sha256,
        )
        self.assertEqual(
            candidate_result.sections[0].seam_projection,
            terminal_result.sections[0].seam_projection,
        )
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            kernel.validate_named_definition(
                schema, "reviewSeamProjection",
                terminal_result.sections[0].seam_projection,
            ),
            [],
        )

    def test_deep_equality_drift_is_rejected_at_json_offset(self):
        seam = seam_record()
        fenced = copy.deepcopy(seam)
        fenced["conclusion"] = "Drifted fenced conclusion."
        payload = support.build_ledger_markdown([fenced])
        result = kernel.synchronize_ledger_markdown(payload, [seam], path="ledger.md")
        self.assertIn("KIN-E-LEDGER", issue_codes(result))
        self.assertIn(payload.index(b"{") , issue_offsets(result))

    def test_missing_extra_duplicate_wrong_and_misplaced_fences_are_rejected(self):
        seam = seam_record()
        cases = []
        cases.append(b"## KIN-A-001\nNarrative only.\n")
        valid = support.build_ledger_markdown([seam], preamble=b"")
        duplicate = valid.replace(
            b"Human narrative after the fence.",
            support.markdown_fence("kintsugi-seam", seam) + b"Human narrative after the fence.",
        )
        cases.append(duplicate)
        cases.append(valid.replace(b"kintsugi-seam", b"kintsugi-receipt", 1))
        cases.append(valid.replace(b"kintsugi-seam", b"kintsugi-unknown", 1))
        cases.append(valid.replace(b"```json kintsugi-seam", b" ```json kintsugi-seam", 1))
        cases.append(valid.replace(
            b"Human narrative after the fence.",
            support.markdown_fence("unexpected-json-role", {})
            + b"Human narrative after the fence.",
        ))
        for payload in cases:
            with self.subTest(payload=payload[:80]):
                result = kernel.synchronize_ledger_markdown(payload, [seam], path="ledger.md")
                self.assertIn("KIN-E-LEDGER", issue_codes(result))

    def test_every_line_start_json_fence_lexical_variant_is_classified(self):
        seam = seam_record()
        valid = support.build_ledger_markdown([seam], preamble=b"")
        malformed_fences = (
            b"```json\n{}\n```\n",
            b"```json\tkintsugi-seam\n{}\n```\n",
            b"```JSON kintsugi-seam\n{}\n```\n",
            b"```json kintsugi-seam`\n{}\n```\n",
        )
        for malformed in malformed_fences:
            with self.subTest(opener=malformed.splitlines()[0]):
                result = kernel.synchronize_ledger_markdown(
                    valid + malformed, [seam], path="ledger.md"
                )
                self.assertIn("KIN-E-LEDGER", issue_codes(result))
                self.assertTrue(any(
                    "malformed JSON fence opener" in issue.message
                    for issue in result.issues
                ))

    def test_extra_and_missing_sections_and_duplicate_headings_are_rejected(self):
        first = seam_record("KIN-A-001")
        second = seam_record("KIN-A-002")
        missing = kernel.synchronize_ledger_markdown(
            support.build_ledger_markdown([first]), [first, second]
        )
        extra = kernel.synchronize_ledger_markdown(
            support.build_ledger_markdown([first, second]), [first]
        )
        duplicate_payload = support.build_ledger_markdown([first, first])
        duplicate = kernel.synchronize_ledger_markdown(duplicate_payload, [first])
        self.assertIn("KIN-E-LEDGER", issue_codes(missing))
        self.assertIn("KIN-E-LEDGER", issue_codes(extra))
        self.assertTrue(any("duplicate seam heading" in issue.message for issue in duplicate.issues))
        self.assertIn(duplicate_payload.rindex(b"## KIN-A-001"), issue_offsets(duplicate))

    def test_malformed_unterminated_invalid_utf8_and_deep_json_are_controlled(self):
        seam = seam_record()
        opener = b"## KIN-A-001\n```json kintsugi-seam\n"
        cases = (
            opener + b"{broken}\n```\n",
            opener + b"{}\n",
            opener + b"\xff{}\n```\n",
            opener + (b"[" * 1500) + b"0" + (b"]" * 1500) + b"\n```\n",
        )
        for payload in cases:
            with self.subTest(length=len(payload)):
                result = kernel.synchronize_ledger_markdown(payload, [seam], path="ledger.md")
                self.assertTrue(result.issues)
                self.assertTrue(set(issue_codes(result)) <= {"KIN-E-JSON", "KIN-E-LEDGER"})
                self.assertEqual(issue_offsets(result), sorted(issue_offsets(result)))

    def test_issue_order_is_byte_offset_then_code_and_large_narrative_is_bounded(self):
        seam = seam_record()
        payload = (
            b"# " + b"x" * 200_000 + b"\n"
            + b"## KIN-A-001\n"
            + b"```json kintsugi-unknown\n{}\n```\n"
            + b"## KIN-A-001\n"
        )
        result = kernel.synchronize_ledger_markdown(payload, [seam], path="ledger.md")
        self.assertTrue(result.issues)
        self.assertEqual(issue_offsets(result), sorted(issue_offsets(result)))
        self.assertTrue(all(issue.path.startswith("ledger.md@") for issue in result.issues))


class ReceiptSynchronizationTests(unittest.TestCase):
    def test_lf_and_crlf_receipt_boundaries_are_excluded_from_narrative_hash(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        for newline in (b"\n", b"\r\n"):
            with self.subTest(newline=newline):
                payload = support.build_receipt_markdown(
                    receipt, newline=newline,
                    prefix=b"Prefix.\n", suffix=b"Suffix.\n",
                )
                result = kernel.synchronize_receipt_markdown(payload, receipt)
                expected_prefix = b"Prefix." + newline
                expected_suffix = b"Suffix." + newline
                expected_hash = "sha256:" + hashlib.sha256(
                    NARRATIVE_DOMAIN
                    + len(expected_prefix).to_bytes(8, "big") + expected_prefix
                    + len(expected_suffix).to_bytes(8, "big") + expected_suffix
                ).hexdigest()
                self.assertEqual(result.prefix, expected_prefix)
                self.assertEqual(result.suffix, expected_suffix)
                self.assertEqual(result.narrative_raw_sha256, expected_hash)

    def test_unique_receipt_fence_projects_exact_two_sided_narrative(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        payload = support.build_receipt_markdown(receipt)
        result = kernel.synchronize_receipt_markdown(payload, receipt, path="receipt.md")
        self.assertEqual(result.issues, ())
        self.assertEqual(result.receipt_record, receipt)
        self.assertEqual(result.receipt_id, receipt["id"])
        self.assertEqual(
            result.narrative_raw_sha256,
            kernel.framed_narrative_hash(result.prefix, result.suffix),
        )
        self.assertNotIn(b"kintsugi-receipt", result.prefix + result.suffix)

    def test_receipt_hash_ignores_mechanical_json_but_binds_fence_side(self):
        draft = support.build_core_data()["phaseReceipts"][0]
        complete = copy.deepcopy(draft)
        complete.update({
            "status": "COMPLETE",
            "reviewTargetDigest": support.RAW_HASH,
            "logicReviewPath": "reviews/logic.md",
            "btjReviewPath": "reviews/btj.md",
            "reviewAttemptId": support.ATTEMPT_ID,
        })
        left = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(draft), draft
        )
        mechanical = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(complete), complete
        )
        moved = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                draft, prefix=b"# Synthetic receipt\n", suffix=b"\nFrozen human claim.\nHuman provenance note.\n"
            ),
            draft,
        )
        self.assertEqual(left.narrative_raw_sha256, mechanical.narrative_raw_sha256)
        self.assertNotEqual(left.narrative_raw_sha256, moved.narrative_raw_sha256)

    def test_dynamic_receipt_status_prose_is_rejected_only_after_target_freeze(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        payload = support.build_receipt_markdown(
            receipt, prefix=b"# Receipt\nStatus: VERIFIED\n"
        )
        pre_freeze = kernel.synchronize_receipt_markdown(
            payload, receipt, target_frozen=False
        )
        frozen = kernel.synchronize_receipt_markdown(
            payload, receipt, target_frozen=True
        )
        self.assertEqual(pre_freeze.issues, ())
        self.assertIn("KIN-E-LEDGER", issue_codes(frozen))
        self.assertTrue(any("dynamic receipt prose" in issue.message for issue in frozen.issues))

    def test_frozen_receipt_rejects_machine_field_spellings_outside_fence(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        fields = (
            b"reviewTargetDigest: sha256:abc",
            b"logicReviewPath: reviews/logic.md",
            b"btjReviewPath: reviews/btj.md",
            b"validationBundlePath: bundle.json",
            b"validationDigest: sha256:def",
            b"reviewAttemptId: RVA-B-001",
            b"reviewerPath: reviews/logic.md",
            b"truthGate: PASS",
            b"Digest: sha256:abc",
            b"Reviewer path: reviews/logic.md",
            b"Bundle: bundle.json",
            b"Gate: PASS",
        )
        for field in fields:
            with self.subTest(field=field):
                payload = support.build_receipt_markdown(
                    receipt, prefix=b"# Receipt\n" + field + b"\n"
                )
                result = kernel.synchronize_receipt_markdown(
                    payload, receipt, target_frozen=True
                )
                self.assertIn("KIN-E-LEDGER", issue_codes(result))

    def test_frozen_receipt_rejects_status_review_gate_digest_and_bundle_prose(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        dynamic_lines = (
            b"Receipt status: VERIFIED",
            b"Status is VERIFIED",
            b"| Status | VERIFIED |",
            b"Logic reviewer path: reviews/logic.md",
            b"Gate status: PASS",
            b"The review passed.",
            b"Validation bundle is bundle.json",
            b"Review target digest = sha256:abc",
            b"Truth gate is PASS",
            b"validation_digest = sha256:def",
        )
        for line in dynamic_lines:
            with self.subTest(line=line):
                payload = support.build_receipt_markdown(
                    receipt, prefix=b"# Receipt\n" + line + b"\n"
                )
                result = kernel.synchronize_receipt_markdown(
                    payload, receipt, target_frozen=True
                )
                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "dynamic receipt prose" in issue.message
                    for issue in result.issues
                ))

    def test_frozen_receipt_rejects_explicit_receipt_and_phase_state_prose(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        state_lines = (
            b"This receipt has reached VERIFIED.",
            b"The receipt remains DRAFT.",
            b"The phase is now COMPLETE.",
            b"Logic signed off.",
            b"BTJ review FAILED.",
            b"Truth gate remains PENDING.",
            b"The review was ABANDONED.",
        )
        for line in state_lines:
            with self.subTest(line=line):
                payload = support.build_receipt_markdown(
                    receipt, prefix=b"# Receipt\n" + line + b"\n"
                )
                result = kernel.synchronize_receipt_markdown(
                    payload, receipt, target_frozen=True
                )
                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "dynamic receipt prose" in issue.message
                    for issue in result.issues
                ))

    def test_frozen_receipt_reserves_mechanical_subjects_regardless_of_predicate(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        reserved_lines = (
            b"Logic approved.",
            b"BTJ accepted.",
            b"Justice rejected.",
            b"The receipt is closed.",
            b"The phase was finalized.",
            b"The reviewers approved it.",
            b"The truth gate greenlit everything.",
        )
        for line in reserved_lines:
            with self.subTest(line=line):
                payload = support.build_receipt_markdown(
                    receipt,
                    prefix=b"# Synthetic receipt\n\n" + line + b"\n",
                )
                result = kernel.synchronize_receipt_markdown(
                    payload, receipt, target_frozen=True
                )
                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "dynamic receipt prose" in issue.message
                    for issue in result.issues
                ))

    def test_frozen_receipt_allows_only_closed_structural_heading_templates(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        for heading in (
            b"# Synthetic receipt",
            b"# Kintsugi Phase B receipt",
            b"## Receipt ID: REC-B-109",
        ):
            with self.subTest(heading=heading):
                payload = support.build_receipt_markdown(
                    receipt,
                    prefix=heading + b"\n\nThe bounded claim remains sourced.\n",
                )
                result = kernel.synchronize_receipt_markdown(
                    payload, receipt, target_frozen=True
                )
                self.assertEqual(result.issues, ())

        rejected = support.build_receipt_markdown(
            receipt,
            prefix=b"# The receipt is closed\n\nThe bounded claim remains sourced.\n",
        )
        self.assertTrue(kernel.synchronize_receipt_markdown(
            rejected, receipt, target_frozen=True
        ).issues)

        for mismatched_heading in (
            b"# Kintsugi Phase A receipt",
            b"## Receipt ID: REC-A-108",
        ):
            with self.subTest(mismatched_heading=mismatched_heading):
                mismatched = support.build_receipt_markdown(
                    receipt,
                    prefix=(
                        mismatched_heading
                        + b"\n\nThe bounded claim remains sourced.\n"
                    ),
                )
                self.assertTrue(kernel.synchronize_receipt_markdown(
                    mismatched, receipt, target_frozen=True
                ).issues)

    def test_frozen_receipt_accepts_and_hash_binds_ordinary_narrative(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        first = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                receipt,
                prefix=(
                    b"# Synthetic receipt\n\n"
                    b"The surviving claim remains bounded by sourced evidence.\n"
                ),
            ),
            receipt,
            target_frozen=True,
        )
        second = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                receipt,
                prefix=(
                    b"# Synthetic receipt\n\n"
                    b"The surviving claim remains narrowly bounded by sourced evidence.\n"
                ),
            ),
            receipt,
            target_frozen=True,
        )
        self.assertEqual(first.issues, ())
        self.assertEqual(second.issues, ())
        self.assertNotEqual(first.narrative_raw_sha256, second.narrative_raw_sha256)

    def test_reserved_stems_do_not_match_inside_ordinary_words(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        result = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                receipt,
                prefix=(
                    b"# Synthetic receipt\n\n"
                    b"The aggregate remains bounded by biological evidence.\n"
                ),
            ),
            receipt,
            target_frozen=True,
        )
        self.assertEqual(result.issues, ())

    def test_frozen_receipt_rejects_rendered_equivalent_control_bypasses(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        bypass_lines = (
            "# Kintsugi Ph**ase** A re**ceipt**",
            "## Re**ceipt** ID: REC-A-108",
            "The re**view** passed.",
            "Sta\u200btus: VERIFIED",
            "St&#97;tus: VERIFIED",
            "St&#x61;tus: VERIFIED",
            "Sta&ZeroWidthSpace;tus: VERIFIED",
            "Ｓｔａｔｕｓ: VERIFIED",
            "The audit passed.",
            "The attestation approved it.",
            "The verdict was PASS.",
            "The checker signed off.",
            "The validation succeeded.",
            "The target is frozen.",
            "The artifact is final.",
            "The package passed.",
            "The bundle was finalized.",
            "The outcome was approved.",
            "The target is not approved.",
            "The artifact was formally finalized.",
            "The package has now been fully accepted.",
            "The outcome was definitively rejected.",
            "Bundle=bundle.json",
            "Target=KIN-A-001",
            "Outcome=PASSING-CANDIDATE",
            "Bundle\t=\tbundle.json",
            "Bundle : bundle.json",
            "The target is being reviewed.",
            "The artifact was audited.",
            "The bundle has been validated.",
            "The outcome is being checked.",
        )
        for line in bypass_lines:
            with self.subTest(line=line):
                payload = support.build_receipt_markdown(
                    receipt,
                    prefix=(
                        "# Synthetic receipt\n\n" + line + "\n"
                    ).encode("utf-8"),
                )

                result = kernel.synchronize_receipt_markdown(
                    payload, receipt, target_frozen=True
                )

                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "dynamic receipt prose" in issue.message
                    for issue in result.issues
                ))

    def test_frozen_receipt_rejects_capped_modifier_closure_bypasses(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        for line in (
            "The target is conclusively frozen.",
            "The artifact was unequivocally finalized.",
            "The package has unquestionably passed.",
            "The bundle is indisputably complete.",
            "The outcome was conclusively approved.",
            "The target has already been frozen.",
            "The package should now be considered final.",
            "The target will be frozen.",
            "The target must now be frozen.",
            "The target is plainly frozen.",
            "The package should now officially be formally considered unquestionably final.",
        ):
            with self.subTest(line=line):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + line + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )

                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "dynamic receipt prose" in issue.message
                    for issue in result.issues
                ))

    def test_frozen_receipt_allows_exact_control_nouns_and_math_prose(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        ordinary_lines = (
            "Logic connects premises to conclusions.",
            "A phase transition changes the order parameter.",
            "The literature review surveys prior work.",
            "The status of the theorem remains open.",
            "The digest of a message is a mathematical function.",
            "The gate in a circuit computes conjunction.",
            "The relation x<y remains conjectural.",
            "The interval f[x] remains bounded.",
            "The type List[T] remains abstract.",
            "The notation <A,B> denotes an inner product.",
            "The audit artifact in the museum is historically important.",
            "The status of the theorem is discussed at https://example.test/.",
            "Status reports are documented at https://example.test/.",
            "Audit.",
            "Attestation.",
            "BTJ.",
            "Checker.",
            "Logic.",
            "Phase.",
            "Receipt.",
            "Review.",
            "Reviewer.",
            "Status.",
            "Validation.",
            "Verdict.",
        )
        hashes = []
        for line in ordinary_lines:
            with self.subTest(line=line):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + line + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )

                self.assertEqual(result.issues, ())
                hashes.append(result.narrative_raw_sha256)
        self.assertEqual(len(hashes), len(set(hashes)))

    def test_receipt_projection_preserves_character_reference_punctuation(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        for line in (
            "The spelling re&#42;view remains visibly marked.",
            "The spelling lo&#95;gic remains visibly marked.",
            "The escaped text &lt;span&gt; is literal documentation.",
            "The spelling St&#97tus is not a CommonMark character reference.",
            "The spelling &ltspan is not a CommonMark character reference.",
            "The literal `St&#97;tus: VERIFIED` is code documentation.",
            "The literal `Status: VERIFIED` is code documentation.",
            "The literal `Ｓｔａｔｕｓ: VERIFIED` is code documentation.",
            "The literal `Sta&ZeroWidthSpace;tus: VERIFIED` is code documentation.",
            r"The escaped \&#83;tatus: VERIFIED is literal source.",
            "Lo_gic approved remains literal intraword punctuation.",
            "The spelling re*view remains an unmatched literal delimiter.",
            "The spelling re***view** remains visibly marked.",
            "The spelling re~~view~~ remains visibly marked.",
            "The re***view** passed.",
            "The re***view* passed.",
            "The re~~view~~ passed.",
        ):
            with self.subTest(line=line):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + line + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )

                self.assertEqual(result.issues, ())

        for line in (
            "The re**view** passed.",
            "_Logic_ approved.",
            "St&#97;tus: VERIFIED",
            "Sta&ZeroWidthSpace;tus: VERIFIED",
        ):
            with self.subTest(line=line):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + line + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )

                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "dynamic receipt prose" in issue.message
                    for issue in result.issues
                ))

    def test_frozen_receipt_rejects_proven_links_and_complete_inline_html(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        unsupported_sources = (
            "See [documentation](https://example.test/).",
            "See ![diagram](diagram.svg).",
            "See [documentation][reference].\n\n[reference]: https://example.test/",
            "See [documentation][].\n\n[documentation]: https://example.test/",
            "See [documentation].\n\n[documentation]: https://example.test/",
            "See <https://example.test/>.",
            "See <reader@example.test>.",
            "See <foo@bar>.",
            "See <foo.bar@example.com>.",
            "See <a+b:c>.",
            "The prose contains <span class=\"note\">literal HTML</span>.",
            "The prose contains <span\n class=\"note\">literal HTML</span>.",
            "The prose contains <!-- a bounded\n comment --> here.",
            "The prose contains <?instruction\n value?> here.",
            "The prose contains <!DECLARATION\n value> here.",
            "The prose contains <![CDATA[bounded\n text]]> here.",
            "The prose contains <!doctype html> here.",
            "The prose contains <!--> here.",
            "The prose contains <!---> here.",
            "An unmatched ` opener ends here.\n\n[docs](url)\n\nA later ` is separate.",
        )
        for source in unsupported_sources:
            with self.subTest(source=source):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + source + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )

                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "bounded lexical grammar" in issue.message
                    for issue in result.issues
                ))

        for source in (
            "The relation x<y remains conjectural.",
            "The interval f[x] remains bounded.",
            "The type List[T] remains abstract.",
            "The notation <A,B> denotes an inner product.",
            "The fragment <span is incomplete documentation.",
            "The fragment <!-- remains unfinished documentation.",
            "The fragment <? remains unfinished documentation.",
            "The fragment <!DECLARATION remains unfinished documentation.",
            "The fragment <![CDATA[ remains unfinished documentation.",
            "Literal <span\n\nclass=x> notation remains ordinary source.",
            r"The escaped link \[x](y) remains literal source.",
            r"The escaped tag \<span> remains literal source.",
            "The code span `[x](y)` remains literal source.",
            "The invalid inline form [x](not a link) remains literal source.",
            "The unresolved reference [x][missing] remains literal source.",
        ):
            with self.subTest(source=source):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + source + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )

                self.assertEqual(result.issues, ())

    def test_receipt_source_scanner_has_a_deterministic_linear_step_bound(self):
        scanner = getattr(markdown_module, "_scan_receipt_source", None)
        self.assertTrue(callable(scanner), "receipt source scanner is absent")
        for repeats in (32, 64, 128):
            with self.subTest(repeats=repeats):
                source = (
                    "x<y f[x] List[T] re*view \\[x](y) `z[z]` "
                    * repeats
                )
                first = scanner(source)
                second = scanner(source)
                self.assertEqual(first, second)
                self.assertIsNone(first.unsupported_offset)
                self.assertLessEqual(first.steps, 40 * len(source) + 64)

        for depth in (64, 128):
            with self.subTest(depth=depth):
                source = "[" * depth + "x" + "]" * depth
                result = scanner(source)
                self.assertIsNone(result.unsupported_offset)
                self.assertLessEqual(result.steps, 40 * len(source) + 64)

    def test_receipt_source_scanner_fails_closed_on_complete_over_cap_construct(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        source = "<!--\n" + ("bounded text\n" * 700) + "-->"
        self.assertGreater(
            len(source), markdown_module._MAX_RECEIPT_CONSTRUCT_CHARS
        )
        result = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                receipt,
                prefix=("# Synthetic receipt\n\n" + source + "\n").encode(),
            ),
            receipt,
            target_frozen=True,
        )
        self.assertTrue(any(
            issue.code == "KIN-E-LEDGER"
            and "bounded lexical grammar" in issue.message
            for issue in result.issues
        ))

    def test_frozen_receipt_rejects_unsupported_rendered_split_constructs(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        for line in (
            "The re[vi](x)ew passed.",
            "The re<span>view passed.",
            "The re[vi][x]ew passed.\n\n[x]: https://example.test/",
            "The re[vi]ew passed.\n\n[vi]: https://example.test/",
            "The re<span\nclass=x>view passed.",
            "The re<!--\n-->view passed.",
            "The re<!-- <3 -->view passed.",
            "The re<!-- <3\n-->view passed.",
        ):
            with self.subTest(line=line):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + line + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )

                self.assertTrue(any(
                    issue.code == "KIN-E-LEDGER"
                    and "bounded lexical grammar" in issue.message
                    for issue in result.issues
                ))

        ordinary = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                receipt,
                prefix=(
                    b"# Synthetic receipt\n\n"
                    b"The surviving claim remains bounded by sourced evidence.\n"
                    b"The admissible interval is [0, 1]\n"
                ),
            ),
            receipt,
            target_frozen=True,
        )
        self.assertEqual(ordinary.issues, ())

    def test_receipt_source_grammar_respects_commonmark_block_boundaries(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        cases = (
            ("The re<span disabled required>view passed.", True),
            ("The notation [x](\n\n/url) remains literal source.", False),
            ("The notation [x]\n[x]: /url remains literal source.", False),
            ("[x\n\ny](url)", False),
            ('The notation [x](url "a\n\nb") remains literal source.', False),
            ('The notation <span class="a\n\nb"> remains literal source.', False),
            ("```text\nStatus: VERIFIED\n```", False),
            (
                "The notation [x] remains literal source.\n\n"
                "[x]: not a destination",
                False,
            ),
            (
                "See [second].\n\n[first]: /one\n[second]: /two",
                True,
            ),
        )
        for source, unsupported in cases:
            with self.subTest(source=source):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + source + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )
                if unsupported:
                    self.assertTrue(any(
                        issue.code == "KIN-E-LEDGER"
                        and "bounded lexical grammar" in issue.message
                        for issue in result.issues
                    ))
                else:
                    self.assertEqual(result.issues, ())

    def test_reference_definition_payloads_follow_commonmark_examples(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        cases = (
            (  # CommonMark 0.31.2 example 193.
                "See [foo].\n\n   [foo]:\n      /url\n"
                "           'the title'",
                True,
            ),
            (  # Example 196: a nonblank multiline title is valid.
                "See [foo].\n\n[foo]: /url '\n"
                "title\nline1\nline2\n'",
                True,
            ),
            (  # Example 198: destination on the next line, no title.
                "See [foo].\n\n[foo]:\n/url",
                True,
            ),
            (  # Example 209: trailing characters invalidate the definition.
                "See [foo].\n\n[foo]: /url \"title\" ok",
                False,
            ),
            (  # Example 210: malformed following-line title is separate prose.
                "See [foo].\n\n[foo]: /url\n  \"title\" ok",
                True,
            ),
            (
                "See [foo].\n\n[foo]: /url\n  \"unterminated",
                True,
            ),
            (  # Example 217: definitions continue after a title line.
                "See [baz].\n\n[foo]: /foo-url \"foo\"\n"
                "[bar]: /bar-url\n  \"bar\"\n[baz]: /baz-url",
                True,
            ),
            (
                "# Heading\n[foo]: /url\n\nSee [foo].",
                True,
            ),
            (
                "---\n[foo]: /url\n\nSee [foo].",
                True,
            ),
            (
                "See [foo].\n\n[\nfoo\n]: /url",
                True,
            ),
            (
                "See [foo].\r\r[foo]: /url",
                True,
            ),
            (
                "See [foo].\n\n> [foo]: /url",
                True,
            ),
            (
                "See [foo].\n\n- [foo]: /url",
                True,
            ),
            (
                "See [a[b]c].\n\n[a[b]c]: /url",
                False,
            ),
            (
                "See [foo].\n\n```text\n\n[foo]: /url\n```",
                False,
            ),
        )
        for source, unsupported in cases:
            with self.subTest(source=source):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + source + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )
                if unsupported:
                    self.assertTrue(any(
                        issue.code == "KIN-E-LEDGER"
                        and "bounded lexical grammar" in issue.message
                        for issue in result.issues
                    ))
                else:
                    self.assertEqual(result.issues, ())

    def test_invalid_backtick_fence_info_cannot_hide_dynamic_receipt_prose(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        source = "``` invalid`info\nStatus: VERIFIED"
        result = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                receipt,
                prefix=("# Synthetic receipt\n\n" + source + "\n").encode(),
            ),
            receipt,
            target_frozen=True,
        )
        self.assertTrue(any(
            issue.code == "KIN-E-LEDGER"
            and "dynamic receipt prose" in issue.message
            for issue in result.issues
        ))

    def test_receipt_projection_rechecks_bound_after_nfkc_expansion(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        bound = markdown_module._MAX_RECEIPT_PROJECTION_CHARS
        ligature = "\ufdfa"
        expanded = unicodedata.normalize("NFKC", ligature)
        repeats = bound // len(expanded) + 1
        line = ligature * repeats
        self.assertLessEqual(len(line), bound)
        self.assertGreater(len(unicodedata.normalize("NFKC", line)), bound)

        result = kernel.synchronize_receipt_markdown(
            support.build_receipt_markdown(
                receipt,
                prefix=(
                    "# Synthetic receipt\n\n" + line + "\n"
                ).encode("utf-8"),
            ),
            receipt,
            target_frozen=True,
        )

        self.assertTrue(any(
            issue.code == "KIN-E-LEDGER"
            and "bounded lexical grammar" in issue.message
            for issue in result.issues
        ))

    def test_frozen_receipt_lexical_grammar_preserves_ordinary_narrative(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        ordinary_lines = (
            "The digestive evidence remains narrowly bounded.",
            "The logical relation remains conjectural.",
            "The vector bundle remains topologically nontrivial.",
            "The aggregate remains bounded by biological evidence.",
            "The target is a geometric point in the diagram.",
            "The artifact depicts a historical vessel.",
            "The package contains source material.",
            "The outcome variable remains undefined.",
            "Truth remains a philosophical question.",
            "Beauty remains a contested category.",
            "Justice remains a substantive human concern.",
            "The target is a geometric point in the final diagram.",
            "The artifact depicts the final voyage of a historical vessel.",
            "The package contains an essay whose draft remains in the archive.",
            "Truth remains a philosophical question after the draft essay.",
        )
        hashes = []
        for line in ordinary_lines:
            with self.subTest(line=line):
                result = kernel.synchronize_receipt_markdown(
                    support.build_receipt_markdown(
                        receipt,
                        prefix=(
                            "# Synthetic receipt\n\n" + line + "\n"
                        ).encode("utf-8"),
                    ),
                    receipt,
                    target_frozen=True,
                )
                self.assertEqual(result.issues, ())
                hashes.append(result.narrative_raw_sha256)
        self.assertEqual(len(hashes), len(set(hashes)))

    def test_receipt_missing_duplicate_wrong_malformed_and_drift_are_rejected(self):
        receipt = support.build_core_data()["phaseReceipts"][0]
        valid = support.build_receipt_markdown(receipt)
        drift = copy.deepcopy(receipt)
        drift["manifestId"] = "MAN-B-999"
        cases = (
            b"# No fence\n",
            valid + support.markdown_fence("kintsugi-receipt", receipt),
            valid.replace(b"kintsugi-receipt", b"kintsugi-seam", 1),
            valid.replace(b"{", b"{broken", 1),
            support.build_receipt_markdown(drift),
        )
        for payload in cases:
            with self.subTest(payload=payload[:60]):
                result = kernel.synchronize_receipt_markdown(payload, receipt)
                self.assertTrue(result.issues)
                self.assertTrue(set(issue_codes(result)) <= {"KIN-E-JSON", "KIN-E-LEDGER"})


class ReviewAndQueueSynchronizationTests(unittest.TestCase):
    def review_records(self):
        first = support.build_review_finding()
        second = copy.deepcopy(first)
        second["id"] = "FND-B-002"
        attestation = support.build_review_attestation("LOGIC", "FAIL")
        attestation["findingIds"] = [first["id"], second["id"]]
        attestation["openSevereFindingIds"] = [first["id"], second["id"]]
        return attestation, [first, second]

    def test_review_requires_one_attestation_and_one_sorted_findings_fence(self):
        attestation, findings = self.review_records()
        payload = support.build_review_markdown(attestation, findings)
        result = kernel.synchronize_review_markdown(payload, attestation, findings)
        self.assertEqual(result.issues, ())
        self.assertEqual([record.role for record in result.records], [
            "kintsugi-review", "kintsugi-review-findings",
        ])
        self.assertEqual(result.records[0].value, attestation)
        self.assertEqual(result.records[1].value, findings)

        unsorted_payload = support.build_review_markdown(attestation, list(reversed(findings)))
        unsorted = kernel.synchronize_review_markdown(unsorted_payload, attestation, findings)
        self.assertIn("KIN-E-LEDGER", issue_codes(unsorted))

    def test_review_accepts_an_explicit_empty_findings_array(self):
        attestation = support.build_review_attestation("LOGIC", "PASS")
        payload = support.build_review_markdown(attestation, [])
        result = kernel.synchronize_review_markdown(payload, attestation, [])
        self.assertEqual(result.issues, ())
        self.assertEqual(result.records[1].role, "kintsugi-review-findings")
        self.assertEqual(result.records[1].value, [])

    def test_review_finding_ids_attempt_and_kind_must_match_attestation(self):
        attestation, findings = self.review_records()
        mutations = []
        missing_id = copy.deepcopy(attestation)
        missing_id["findingIds"] = [findings[0]["id"]]
        mutations.append((missing_id, findings))
        wrong_attempt = copy.deepcopy(findings)
        wrong_attempt[1]["attemptId"] = "RVA-B-999"
        mutations.append((attestation, wrong_attempt))
        wrong_kind = copy.deepcopy(findings)
        wrong_kind[1]["reviewKind"] = "BTJ"
        mutations.append((attestation, wrong_kind))
        for candidate_attestation, candidate_findings in mutations:
            payload = support.build_review_markdown(candidate_attestation, candidate_findings)
            result = kernel.synchronize_review_markdown(
                payload, candidate_attestation, candidate_findings
            )
            self.assertIn("KIN-E-LEDGER", issue_codes(result))

    def test_duplicate_expected_findings_and_attestation_ids_are_rejected(self):
        finding = support.build_review_finding()
        findings = [finding, copy.deepcopy(finding)]
        attestation = support.build_review_attestation("LOGIC", "FAIL")
        attestation["findingIds"] = [finding["id"], finding["id"]]
        payload = support.build_review_markdown(attestation, findings)

        result = kernel.synchronize_review_markdown(
            payload, attestation, findings
        )

        self.assertIn("KIN-E-LEDGER", issue_codes(result))
        self.assertTrue(any(
            "duplicate expected review finding id" in issue.message
            for issue in result.issues
        ))
        self.assertTrue(any(
            "duplicate attestation finding id" in issue.message
            for issue in result.issues
        ))

    def test_non_string_expected_finding_and_attestation_ids_are_rejected(self):
        finding = support.build_review_finding()
        finding["id"] = ["not", "an", "id"]
        attestation = support.build_review_attestation("LOGIC", "FAIL")
        attestation["findingIds"] = [["not", "an", "id"]]
        payload = support.build_review_markdown(attestation, [finding])

        result = kernel.synchronize_review_markdown(
            payload, attestation, [finding]
        )

        self.assertIn("KIN-E-LEDGER", issue_codes(result))
        self.assertTrue(any(
            "expected review finding id must be a string" in issue.message
            for issue in result.issues
        ))
        self.assertTrue(any(
            "attestation finding id must be a string" in issue.message
            for issue in result.issues
        ))

    def test_review_rejects_missing_duplicate_malformed_and_misplaced_roles(self):
        attestation, findings = self.review_records()
        valid = support.build_review_markdown(attestation, findings)
        cases = (
            valid.replace(b"```json kintsugi-review-findings", b"```json ignored", 1),
            valid + support.markdown_fence("kintsugi-review", attestation),
            valid.replace(b"kintsugi-review-findings", b"kintsugi-public-queue", 1),
            valid.replace(b"{", b"{broken", 1),
        )
        for payload in cases:
            with self.subTest(payload=payload[-80:]):
                result = kernel.synchronize_review_markdown(payload, attestation, findings)
                self.assertTrue(result.issues)

    def test_public_queue_requires_exactly_one_matching_role_record(self):
        queue = support.build_public_queue()
        valid = support.build_public_queue_markdown(queue, newline=b"\r\n")
        result = kernel.synchronize_public_queue_markdown(valid, queue)
        self.assertEqual(result.issues, ())
        self.assertEqual(result.records[0].value, queue)

        drift = copy.deepcopy(queue)
        drift["manifestId"] = "MAN-C-999"
        cases = (
            b"# no queue\n",
            valid + support.markdown_fence("kintsugi-public-queue", queue),
            valid.replace(b"kintsugi-public-queue", b"kintsugi-receipt", 1),
            support.build_public_queue_markdown(drift),
        )
        for payload in cases:
            with self.subTest(payload=payload[:60]):
                parsed = kernel.synchronize_public_queue_markdown(payload, queue)
                self.assertIn("KIN-E-LEDGER", issue_codes(parsed))


class OwnerSynchronizationTests(unittest.TestCase):
    def test_owner_substring_index_matches_bounded_overlapping_oracle(self):
        def capped_naive_count(text: str, pattern: str) -> int:
            count = 0
            start = 0
            while count < 2:
                position = text.find(pattern, start)
                if position < 0:
                    break
                count += 1
                start = position + 1
            return count

        alphabet = "aβ"
        for text_length in range(7):
            for text_chars in itertools.product(
                alphabet, repeat=text_length
            ):
                text = "".join(text_chars)
                index = markdown_module._build_owner_substring_index(text)
                for pattern_length in range(1, 5):
                    for pattern_chars in itertools.product(
                        alphabet, repeat=pattern_length
                    ):
                        pattern = "".join(pattern_chars)
                        self.assertEqual(
                            index.occurrence_count(pattern),
                            capped_naive_count(text, pattern),
                            (text, pattern),
                        )

    def test_crlf_owner_uses_raw_source_hash_lf_quote_hashes_and_never_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, claim, trial, seam, owner = support.build_owner_sync_fixture(
                root, newline="\r\n"
            )
            before = owner.read_bytes()
            before_tree = sorted(
                (path.relative_to(root).as_posix(), path.read_bytes())
                for path in root.rglob("*") if path.is_file()
            )
            issues = kernel.synchronize_owner(root, source, claim, trial, seam)
            after_tree = sorted(
                (path.relative_to(root).as_posix(), path.read_bytes())
                for path in root.rglob("*") if path.is_file()
            )
            self.assertEqual(issues, ())
            self.assertEqual(owner.read_bytes(), before)
            self.assertEqual(before_tree, after_tree)
            self.assertEqual(source["sha256"], kernel.raw_hash(before))
            self.assertTrue(trial["triedHash"].startswith("sha256-text-lf:"))
            self.assertTrue(seam["beforeHash"].startswith("sha256-text-lf:"))

    def test_owner_rejects_unsafe_missing_hash_anchor_quote_and_identity_drift(self):
        mutators = {
            "unsafe": lambda root, source, claim, trial, seam, owner: source.update(path="../owner.md"),
            "missing": lambda root, source, claim, trial, seam, owner: source.update(path="03_METHODOLOGY/missing.md"),
            "raw hash": lambda root, source, claim, trial, seam, owner: source.update(sha256=support.RAW_HASH),
            "anchor": lambda root, source, claim, trial, seam, owner: (
                claim.update(ownerAnchor="## Missing anchor"), seam.update(ownerAnchor="## Missing anchor")
            ),
            "after quote": lambda root, source, claim, trial, seam, owner: owner.write_bytes(
                owner.read_bytes() + b"\nThe repaired owner claim.\nIts second line.\n"
            ),
            "trial hash": lambda root, source, claim, trial, seam, owner: trial.update(triedHash=support.TEXT_HASH),
            "seam hash": lambda root, source, claim, trial, seam, owner: seam.update(beforeHash=support.TEXT_HASH),
            "owner identity": lambda root, source, claim, trial, seam, owner: seam.update(ownerSource="SRC-A-999"),
        }
        for name, mutate in mutators.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, claim, trial, seam, owner = support.build_owner_sync_fixture(root)
                mutate(root, source, claim, trial, seam, owner)
                issues = kernel.synchronize_owner(root, source, claim, trial, seam)
                self.assertTrue(issues)
                self.assertEqual({issue.code for issue in issues}, {"KIN-E-QUOTE"})
                self.assertEqual(tuple(sorted(issues)), issues)

    def test_owner_invalid_utf8_is_controlled_and_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, claim, trial, seam, owner = support.build_owner_sync_fixture(root)
            raw = owner.read_bytes() + b"\xff"
            owner.write_bytes(raw)
            source["sha256"] = kernel.raw_hash(raw)
            issues = kernel.synchronize_owner(root, source, claim, trial, seam)
            self.assertIn("KIN-E-QUOTE", [issue.code for issue in issues])
            self.assertEqual(owner.read_bytes(), raw)

    def test_owner_quote_uniqueness_counts_overlapping_occurrences(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, claim, trial, seam, owner = support.build_owner_sync_fixture(root)
            raw = ("# Owner\n\n## Synthetic owner anchor\n\naaaa\n").encode("utf-8")
            owner.write_bytes(raw)
            source["sha256"] = kernel.raw_hash(raw)
            seam["afterQuote"] = "aaa"
            issues = kernel.synchronize_owner(root, source, claim, trial, seam)
            self.assertTrue(any("exactly once" in issue.message for issue in issues))

    def test_missing_repository_root_is_a_controlled_owner_issue(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, claim, trial, seam, _ = support.build_owner_sync_fixture(root)
            missing_root = root / "missing-root"
            issues = kernel.synchronize_owner(
                missing_root, source, claim, trial, seam
            )
            self.assertEqual({issue.code for issue in issues}, {"KIN-E-QUOTE"})

    def test_embedded_nul_owner_path_is_a_controlled_sorted_quote_issue(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, claim, trial, seam, _ = support.build_owner_sync_fixture(root)
            source["path"] = "03_METHODOLOGY/owner\x00.md"

            issues = kernel.synchronize_owner(root, source, claim, trial, seam)

            self.assertTrue(issues)
            self.assertEqual({issue.code for issue in issues}, {"KIN-E-QUOTE"})
            self.assertEqual(tuple(sorted(issues)), issues)

    def test_lone_surrogate_owner_quotes_return_controlled_sorted_issues(self):
        mutators = (
            lambda trial, seam: seam.update(beforeQuote="\ud800"),
            lambda trial, seam: trial.update(triedQuote="\ud800"),
            lambda trial, seam: seam.update(afterQuote="\ud800"),
        )
        for mutate in mutators:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, claim, trial, seam, _ = support.build_owner_sync_fixture(root)
                mutate(trial, seam)

                issues = kernel.synchronize_owner(root, source, claim, trial, seam)

                self.assertTrue(issues)
                self.assertEqual({issue.code for issue in issues}, {"KIN-E-QUOTE"})
                self.assertEqual(tuple(sorted(issues)), issues)

    def test_one_sided_seam_statuses_require_before_quote_exactly_once(self):
        for status in ("CONFIRMED", "HELD_OPEN"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, claim, trial, seam, owner = support.build_owner_sync_fixture(root)
                seam["status"] = status
                seam["afterQuote"] = None
                raw = (
                    "# Owner\r\n\r\n## Synthetic owner anchor\r\n\r\n"
                    "The former owner claim.\r\nIts second line.\r\n"
                ).encode("utf-8")
                owner.write_bytes(raw)
                source["sha256"] = kernel.raw_hash(raw)
                self.assertEqual(
                    kernel.synchronize_owner(root, source, claim, trial, seam),
                    (),
                )

    def test_one_sided_seam_rejects_missing_and_duplicate_before_quote(self):
        for status in ("CONFIRMED", "HELD_OPEN"):
            for occurrence_count in (0, 2):
                with (
                    self.subTest(status=status, occurrence_count=occurrence_count),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    root = Path(directory)
                    source, claim, trial, seam, owner = support.build_owner_sync_fixture(root)
                    seam["status"] = status
                    seam["afterQuote"] = None
                    quote = "The former owner claim.\nIts second line.\n"
                    raw = (
                        "# Owner\n\n## Synthetic owner anchor\n\n"
                        + quote * occurrence_count
                    ).encode("utf-8")
                    owner.write_bytes(raw)
                    source["sha256"] = kernel.raw_hash(raw)

                    issues = kernel.synchronize_owner(root, source, claim, trial, seam)

                    self.assertTrue(any(
                        issue.code == "KIN-E-QUOTE"
                        and "beforeQuote" in issue.message
                        and "exactly once" in issue.message
                        for issue in issues
                    ))

    def test_one_sided_seam_rejects_a_non_null_after_quote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, claim, trial, seam, owner = support.build_owner_sync_fixture(root)
            seam["status"] = "CONFIRMED"
            raw = (
                "# Owner\n\n## Synthetic owner anchor\n\n"
                "The former owner claim.\nIts second line.\n"
            ).encode("utf-8")
            owner.write_bytes(raw)
            source["sha256"] = kernel.raw_hash(raw)

            issues = kernel.synchronize_owner(root, source, claim, trial, seam)

            self.assertTrue(any(
                issue.code == "KIN-E-QUOTE"
                and "afterQuote" in issue.message
                and "null" in issue.message
                for issue in issues
            ))

    def test_owner_path_resolution_errors_are_typed_and_baseexceptions_propagate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, claim, trial, seam, _ = support.build_owner_sync_fixture(root)
            loop_a = root / "loop-a"
            loop_b = root / "loop-b"
            loop_a.symlink_to(loop_b)
            loop_b.symlink_to(loop_a)
            source["path"] = "loop-a/owner.md"

            loop_issues = kernel.synchronize_owner(root, source, claim, trial, seam)
            self.assertTrue(loop_issues)
            self.assertEqual({issue.code for issue in loop_issues}, {"KIN-E-QUOTE"})
            self.assertEqual(tuple(sorted(loop_issues)), loop_issues)

            boom_issues = kernel.synchronize_owner(
                RootPathBoom(), source, claim, trial, seam
            )
            self.assertTrue(boom_issues)
            self.assertEqual({issue.code for issue in boom_issues}, {"KIN-E-QUOTE"})
            self.assertEqual(tuple(sorted(boom_issues)), boom_issues)

            with self.assertRaises(KeyboardInterrupt):
                kernel.synchronize_owner(
                    RootPathControl(), source, claim, trial, seam
                )


class MalformedPublicBoundaryTests(unittest.TestCase):
    def test_every_controlled_role_rejects_commonmark_json_fence_variants(self):
        seam = seam_record()
        receipt = support.build_core_data()["phaseReceipts"][0]
        attestation = support.build_review_attestation()
        findings: list[dict] = []
        queue = support.build_public_queue()
        artifacts = (
            (
                "kintsugi-seam",
                support.build_ledger_markdown([seam]),
                lambda payload: kernel.synchronize_ledger_markdown(payload, [seam]),
            ),
            (
                "kintsugi-receipt",
                support.build_receipt_markdown(receipt),
                lambda payload: kernel.synchronize_receipt_markdown(payload, receipt),
            ),
            (
                "kintsugi-review",
                support.build_review_markdown(attestation, findings),
                lambda payload: kernel.synchronize_review_markdown(
                    payload, attestation, findings
                ),
            ),
            (
                "kintsugi-review-findings",
                support.build_review_markdown(attestation, findings),
                lambda payload: kernel.synchronize_review_markdown(
                    payload, attestation, findings
                ),
            ),
            (
                "kintsugi-public-queue",
                support.build_public_queue_markdown(queue),
                lambda payload: kernel.synchronize_public_queue_markdown(payload, queue),
            ),
        )
        variants = (
            lambda role: b"````json " + role + b"\r\n{}\r\n````\r\n",
            lambda role: b"~~~json " + role + b"\n{}\n~~~\n",
            lambda role: b"``` json " + role + b"\n{}\n```\n",
            lambda role: b"```\tjson " + role + b"\n{}\n```\n",
            lambda role: b"```application/json " + role + b"\n{}\n```\n",
            lambda role: b"```{.json} " + role + b"\n{}\n```\n",
            lambda role: b"````json " + role + b"\n{}\n",
        )
        for role, valid, synchronize in artifacts:
            role_bytes = role.encode("ascii")
            for build_variant in variants:
                variant = build_variant(role_bytes)
                with self.subTest(role=role, variant=variant.splitlines()[0]):
                    result = synchronize(valid + variant)
                    self.assertIn("KIN-E-LEDGER", issue_codes(result))

    def test_indented_json_looking_fences_are_outside_column_zero_machine_policy(self):
        seam = seam_record()
        payload = support.build_ledger_markdown([seam]) + (
            b"  ```json kintsugi-seam\n{}\n  ```\n"
        )
        self.assertEqual(
            kernel.synchronize_ledger_markdown(payload, [seam]).issues,
            (),
        )

    def test_markdown_payloads_reject_scalars_and_arbitrary_bytes_hooks(self):
        class Boom:
            def __bytes__(self):
                raise RuntimeError("boom")

        for payload in (0, True, Boom()):
            with self.subTest(payload=payload):
                result = kernel.synchronize_ledger_markdown(payload, [])
                self.assertTrue(result.issues)
                self.assertEqual(
                    {issue.code for issue in result.issues}, {"KIN-E-LEDGER"}
                )

    def test_nonfinite_fenced_number_is_malformed_json_even_when_expected_matches(self):
        finite_queue = support.build_public_queue()
        payload = support.build_public_queue_markdown(finite_queue).replace(
            b'"manifestId":"MAN-C-001"', b'"manifestId":1e999', 1
        )
        expected_queue = copy.deepcopy(finite_queue)
        expected_queue["manifestId"] = float("inf")

        result = kernel.synchronize_public_queue_markdown(
            payload, expected_queue, path="queue.md"
        )

        self.assertIn("KIN-E-JSON", issue_codes(result))

    def test_malformed_public_synchronizer_arguments_return_typed_issues(self):
        with tempfile.TemporaryDirectory() as directory:
            seam = seam_record()
            receipt = support.build_core_data()["phaseReceipts"][0]
            attestation = support.build_review_attestation()
            queue = support.build_public_queue()
            source, claim, trial, owner_seam, _ = support.build_owner_sync_fixture(
                Path(directory)
            )
            calls = (
                lambda: kernel.synchronize_ledger_markdown(b"", None),
                lambda: kernel.synchronize_ledger_markdown(None, [seam]),
                lambda: kernel.synchronize_receipt_markdown(b"", None),
                lambda: kernel.synchronize_receipt_markdown(None, receipt),
                lambda: kernel.synchronize_review_markdown(b"", None, None),
                lambda: kernel.synchronize_review_markdown(
                    None, attestation, []
                ),
                lambda: kernel.synchronize_public_queue_markdown(b"", None),
                lambda: kernel.synchronize_public_queue_markdown(None, queue),
                lambda: kernel.synchronize_owner(
                    Path(directory), None, None, None, None
                ),
                lambda: kernel.synchronize_owner(
                    None, source, claim, trial, owner_seam
                ),
            )
            for call in calls:
                with self.subTest(call=call):
                    result = call()
                    issues = result if isinstance(result, tuple) else result.issues
                    self.assertTrue(issues)
                    self.assertTrue(all(
                        issue.code in {"KIN-E-LEDGER", "KIN-E-QUOTE"}
                        for issue in issues
                    ))

    def test_invalid_utf8_outside_fences_is_a_controlled_ledger_issue(self):
        seam = seam_record()
        receipt = support.build_core_data()["phaseReceipts"][0]
        attestation = support.build_review_attestation()
        queue = support.build_public_queue()
        calls = (
            lambda: kernel.synchronize_ledger_markdown(
                support.build_ledger_markdown(
                    [seam], preamble=b"# Ledger\n\xff\n"
                ),
                [seam], path="ledger.md",
            ),
            lambda: kernel.synchronize_receipt_markdown(
                support.build_receipt_markdown(
                    receipt, prefix=b"# Receipt\n\xff\n"
                ),
                receipt, path="receipt.md",
            ),
            lambda: kernel.synchronize_review_markdown(
                b"\xff\n" + support.build_review_markdown(attestation, []),
                attestation, [], path="review.md",
            ),
            lambda: kernel.synchronize_public_queue_markdown(
                b"\xff\n" + support.build_public_queue_markdown(queue),
                queue, path="queue.md",
            ),
        )
        for call in calls:
            with self.subTest(call=call):
                result = call()
                outside = [
                    issue for issue in result.issues
                    if issue.code == "KIN-E-LEDGER"
                    and "strict UTF-8" in issue.message
                ]
                self.assertEqual(len(outside), 1)

    def test_json_null_never_bypasses_role_or_record_equality(self):
        seam = seam_record()
        receipt = support.build_core_data()["phaseReceipts"][0]
        attestation = support.build_review_attestation()
        findings: list[dict] = []
        queue = support.build_public_queue()
        payloads_and_calls = (
            (
                replace_fence_json(
                    support.build_ledger_markdown([seam]), "kintsugi-seam", b"null"
                ),
                lambda payload: kernel.synchronize_ledger_markdown(payload, [seam]),
            ),
            (
                replace_fence_json(
                    support.build_receipt_markdown(receipt), "kintsugi-receipt", b"null"
                ),
                lambda payload: kernel.synchronize_receipt_markdown(payload, receipt),
            ),
            (
                replace_fence_json(
                    support.build_review_markdown(attestation, findings),
                    "kintsugi-review", b"null",
                ),
                lambda payload: kernel.synchronize_review_markdown(
                    payload, attestation, findings
                ),
            ),
            (
                replace_fence_json(
                    support.build_review_markdown(attestation, findings),
                    "kintsugi-review-findings", b"null",
                ),
                lambda payload: kernel.synchronize_review_markdown(
                    payload, attestation, findings
                ),
            ),
            (
                replace_fence_json(
                    support.build_public_queue_markdown(queue),
                    "kintsugi-public-queue", b"null",
                ),
                lambda payload: kernel.synchronize_public_queue_markdown(payload, queue),
            ),
        )
        for payload, call in payloads_and_calls:
            with self.subTest(payload=payload[:80]):
                result = call(payload)
                self.assertIn("KIN-E-LEDGER", issue_codes(result))


if __name__ == "__main__":
    unittest.main()
