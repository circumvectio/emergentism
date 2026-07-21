#!/usr/bin/env python3
"""Mutation tests for the deny-by-default public-release gates."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import audit_live_domain_against_manifest as live_audit


ROOT = Path(__file__).resolve().parent


def release_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "RELEASE_SHA256"):
        rel = path.relative_to(root).as_posix()
        digest.update(rel.encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


class ReleaseBuilderCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, "-B", "build_release.py"], cwd=ROOT, check=True, capture_output=True)

    def assert_non_building_invocation(self, *args: str, expected_returncode: int) -> subprocess.CompletedProcess[str]:
        sentinel = ROOT / ".release" / ".cli-sentinel"
        sentinel.write_text("must survive\n", encoding="ascii")
        try:
            result = subprocess.run(
                [sys.executable, "-B", "build_release.py", *args],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, expected_returncode, result.stderr)
            self.assertTrue(sentinel.is_file(), "CLI-only invocation rebuilt .release")
            return result
        finally:
            sentinel.unlink(missing_ok=True)

    def test_help_does_not_build(self) -> None:
        result = self.assert_non_building_invocation("--help", expected_returncode=0)
        self.assertIn("manifest-allowlisted", result.stdout)

    def test_unknown_argument_fails_without_building(self) -> None:
        result = self.assert_non_building_invocation("--not-a-real-option", expected_returncode=2)
        self.assertIn("unrecognized arguments", result.stderr)

    def test_repeated_build_is_byte_deterministic(self) -> None:
        first = (ROOT / ".release" / "RELEASE_SHA256").read_text(encoding="ascii")
        subprocess.run([sys.executable, "-B", "build_release.py"], cwd=ROOT, check=True, capture_output=True)
        second = (ROOT / ".release" / "RELEASE_SHA256").read_text(encoding="ascii")
        self.assertEqual(first, second)


class ReleaseGateMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, "-B", "build_release.py"], cwd=ROOT, check=True, capture_output=True)

    def test_retired_gfs_validation_claims_fail(self) -> None:
        claims = (
            "Global Flourishing Study validates Emergentism.",
            "GFS supports the Emergentist framework.",
            "The Global Flourishing Study provides evidence supporting the Emergentist worldview.",
            "Emergentism is confirmed by GFS.",
        )
        for claim in claims:
            with self.subTest(claim=claim), tempfile.TemporaryDirectory() as tmp:
                release = Path(tmp) / "release"
                shutil.copytree(ROOT / ".release", release)
                index = release / "index.html"
                index.write_text(
                    index.read_text(encoding="utf-8") + f"\n<p>{claim}</p>\n",
                    encoding="utf-8",
                )
                (release / "RELEASE_SHA256").write_text(release_hash(release) + "\n", encoding="ascii")
                result = subprocess.run(
                    [sys.executable, "-B", "predeploy_check.py", "--release", str(release)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                )
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("retired GFS positive validation", result.stdout)

    def test_retired_probes_never_collide_with_promoted_active_roots(self) -> None:
        data = live_audit.json.loads(live_audit.MANIFEST.read_text(encoding="utf-8"))
        for root in ("book", "read", "papers", "canon", "amrita", "book-pwa"):
            with self.subTest(root=root):
                mutated = dict(data)
                mutated["routes"] = list(data["routes"]) + [
                    {"path": f"/{root}/", "file": "index.html"}
                ]
                self.assertNotIn(f"/{root}/", live_audit.retired_paths(mutated))

    def test_trailing_slash_canonical_paths_are_part_of_the_contract(self) -> None:
        data = live_audit.json.loads(live_audit.MANIFEST.read_text(encoding="utf-8"))
        mapping = live_audit.expected_url_map(data)
        self.assertEqual(mapping["/404/"], "404.html")
        self.assertEqual(mapping["/RELEASE_SHA256/"], "RELEASE_SHA256")
        self.assertNotIn("/404.html", mapping)
        self.assertNotIn("/RELEASE_SHA256", mapping)

    def test_one_clean_body_cannot_impersonate_all_routes(self) -> None:
        body = (ROOT / ".release" / "index.html").read_bytes()

        class SameBodyHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Content-Security-Policy", "default-src 'self'")
                self.send_header("X-Frame-Options", "DENY")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, _format: str, *_args: object) -> None:
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), SameBodyHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    "audit_live_domain_against_manifest.py",
                    "--base-url",
                    f"http://127.0.0.1:{server.server_port}/",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("artifact byte mismatch", result.stdout)


if __name__ == "__main__":
    unittest.main()
