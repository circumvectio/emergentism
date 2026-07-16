from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import kintsugi_kernel as kernel
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


class LedgerSynchronizationTests(unittest.TestCase):
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
            (),
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

    def test_one_sided_seam_statuses_do_not_require_after_quote(self):
        for status in ("CONFIRMED", "HELD_OPEN"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, claim, trial, seam, _ = support.build_owner_sync_fixture(root)
                seam["status"] = status
                seam.pop("afterQuote")
                self.assertEqual(
                    kernel.synchronize_owner(root, source, claim, trial, seam),
                    (),
                )


class MalformedPublicBoundaryTests(unittest.TestCase):
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
