#!/usr/bin/env python3
"""
check_no_secrets_staged.py — Pre-commit guard against API key leaks.

Scans staged git diffs for common API key, token, and secret patterns.
Exits 0 if clean, 1 if any secret pattern is detected in staged changes.

Usage:
    python3 EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/check_no_secrets_staged.py          # manual check
    # Or install as git pre-commit hook:
    # ln -s ../../EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/check_no_secrets_staged.py .git/hooks/pre-commit

Safe patterns (not flagged):
    - Existing committed secrets (only *staged* additions are scanned)
    - Files in .gitignore (they are not staged by definition)
    - Markdown/code docs that mention patterns in comments/strings
      (the regex aims for high-specificity live-key shapes)

If you intentionally need to stage a secret (e.g. encrypted vault,
test fixture with explicit "FAKE_KEY_" prefix), use:
    git commit --no-verify
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


# Patterns: (name, regex, description)
# Each regex is designed to match a LIVE key shape, not a documentation reference.
SECRET_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    (
        "OpenRouter",
        re.compile(r"sk-or-v1-[a-f0-9]{48,}"),
        "OpenRouter API key",
    ),
    (
        "Anthropic",
        re.compile(r"sk-ant-api03-[a-zA-Z0-9_-]{32,}"),
        "Anthropic API key",
    ),
    (
        "OpenAI project",
        re.compile(r"sk-proj-[a-zA-Z0-9_-]{48,}"),
        "OpenAI project key",
    ),
    (
        "OpenAI standard",
        re.compile(r"sk-[a-zA-Z0-9]{48,}"),
        "OpenAI standard key",
    ),
    (
        "Google Gemini",
        re.compile(r"AIzaSy[a-zA-Z0-9_-]{32,}"),
        "Google/Gemini API key",
    ),
    (
        "NVIDIA NIM",
        re.compile(r"nvapi-[a-zA-Z0-9_-]{32,}"),
        "NVIDIA API key",
    ),
    (
        "xAI Grok",
        re.compile(r"sk-xai-[a-zA-Z0-9_-]{32,}"),
        "xAI Grok key",
    ),
    (
        "DeepSeek",
        re.compile(r"sk-ds-[a-zA-Z0-9_-]{32,}|sk-deepseek-[a-zA-Z0-9_-]{32,}"),
        "DeepSeek API key",
    ),
    (
        "Mistral",
        re.compile(r"sk-mistral-[a-zA-Z0-9_-]{32,}"),
        "Mistral API key",
    ),
    (
        "Cohere",
        re.compile(r"sk-cohere-[a-zA-Z0-9_-]{32,}"),
        "Cohere API key",
    ),
    (
        "Perplexity",
        re.compile(r"sk-pplx-[a-zA-Z0-9_-]{32,}"),
        "Perplexity API key",
    ),
    (
        "Groq",
        re.compile(r"sk-groq-[a-zA-Z0-9_-]{32,}"),
        "Groq API key",
    ),
    # Wallet / crypto secrets
    (
        "Ethereum private key",
        re.compile(r"0x[a-f0-9]{64}"),
        "Ethereum private key (hex)",
    ),
    (
        "Nostr nsec",
        re.compile(r"nsec1[ac-hj-np-z02-9]{58,}"),
        "Nostr nsec private key",
    ),
    # Generic high-entropy tokens that look like API keys
    (
        "Generic high-entropy token",
        re.compile(r"[a-zA-Z0-9_-]{64,}"),
        "Generic 64+ char token (possible secret)",
    ),
]

# Exemptions: lines containing these substrings are ignored even if they match a pattern.
# Use for test fixtures, documentation, or encrypted blobs that are intentionally staged.
EXEMPTION_MARKERS = [
    "FAKE_KEY_",
    "EXAMPLE_KEY_",
    "PLACEHOLDER",
    "YOUR_KEY_HERE",
    "REPLACE_WITH",
    "changeme",
    "REDACTED",
    "***",
    "# pragma: allow-secret",
]


def _get_staged_diff() -> str:
    """Return the unified diff of staged changes."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--no-color"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 and "not a git repository" not in result.stderr.lower():
        print(f"⚠️  git diff --cached failed: {result.stderr.strip()}", file=sys.stderr)
        return ""
    return result.stdout


def _line_is_exempt(line: str) -> bool:
    return any(marker in line for marker in EXEMPTION_MARKERS)


def scan(diff_text: str) -> list[dict]:
    """Scan diff text for secret patterns. Return list of findings."""
    findings: list[dict] = []
    current_file = "<unknown>"

    for line in diff_text.splitlines():
        # Track which file we're in
        if line.startswith("diff --git"):
            parts = line.split()
            if len(parts) >= 4:
                current_file = parts[-1].lstrip("b/")
            continue

        # Only look at added lines (staged additions)
        if not line.startswith("+") or line.startswith("+++"):
            continue

        content = line[1:]  # strip leading '+'

        if _line_is_exempt(content):
            continue

        for name, pattern, description in SECRET_PATTERNS:
            if pattern.search(content):
                findings.append({
                    "file": current_file,
                    "line": line,
                    "pattern_name": name,
                    "description": description,
                })
                break  # report first match per line only

    return findings


def main(argv: list[str] | None = None) -> int:
    diff = _get_staged_diff()
    if not diff.strip():
        print("✅ No staged changes to scan.")
        return 0

    findings = scan(diff)

    if not findings:
        print("✅ No secret patterns detected in staged changes.")
        return 0

    print(f"🚨 SECRET LEAK DETECTED: {len(findings)} finding(s) in staged diff\n")
    for f in findings:
        print(f"  File: {f['file']}")
        print(f"  Pattern: {f['pattern_name']} ({f['description']})")
        print(f"  Line: {f['line'][:120]}{'...' if len(f['line']) > 120 else ''}")
        print()

    print("To commit anyway (e.g. for encrypted vaults or test fixtures):")
    print("  git commit --no-verify")
    print()
    print("To exempt a line intentionally, include one of these markers:")
    print(f"  {', '.join(EXEMPTION_MARKERS)}")
    print("Or add '# pragma: allow-secret' to the line.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
