#!/usr/bin/env python3
"""Tests for mver_validator.py."""

from __future__ import annotations
import shutil
import tempfile
from pathlib import Path
import pytest

from mver_validator import parse_index, validate_directory, compute_sha256

# Sample synthetic MVER index text
MVER_INDEX_SAMPLE = """
# MVER Index

### `/01_LEGAL_AND_CORPORATE/`
* `test_doc1.pdf` (Hash: sha256:8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c)
* `test_doc2.pdf` (Hash: sha256:9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d)

### `/02_ASSET_AND_PROPERTY/`
* `test_doc3.pdf` (Hash: sha256:0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e)
"""


@pytest.fixture
def temp_env():
    """Create a temporary directory environment for testing."""
    tmpdir = tempfile.mkdtemp()
    base = Path(tmpdir)
    index_file = base / "MVER_INDEX.md"
    index_file.write_text(MVER_INDEX_SAMPLE, encoding="utf-8")

    data_dir = base / "evidence_room"
    data_dir.mkdir()

    # Create directories
    (data_dir / "01_LEGAL_AND_CORPORATE").mkdir()
    (data_dir / "02_ASSET_AND_PROPERTY").mkdir()

    # Create dummy files with specific contents to match mock hashes
    # To avoid having to compute exact contents to generate dummy hashes, we will
    # compute the actual hashes of dummy files first and rewrite expected index contents.
    f1 = data_dir / "01_LEGAL_AND_CORPORATE" / "test_doc1.pdf"
    f1.write_text("dummy 1 content", encoding="utf-8")
    hash1 = compute_sha256(f1)

    f2 = data_dir / "01_LEGAL_AND_CORPORATE" / "test_doc2.pdf"
    f2.write_text("dummy 2 content", encoding="utf-8")
    hash2 = compute_sha256(f2)

    f3 = data_dir / "02_ASSET_AND_PROPERTY" / "test_doc3.pdf"
    f3.write_text("dummy 3 content", encoding="utf-8")
    hash3 = compute_sha256(f3)

    # Rewrite index to match actual computed hashes
    updated_index_sample = f"""
# MVER Index

### `/01_LEGAL_AND_CORPORATE/`
* `test_doc1.pdf` (Hash: sha256:{hash1})
* `test_doc2.pdf` (Hash: sha256:{hash2})

### `/02_ASSET_AND_PROPERTY/`
* `test_doc3.pdf` (Hash: sha256:{hash3})
"""
    index_file.write_text(updated_index_sample, encoding="utf-8")

    yield index_file, data_dir, hash1, hash2, hash3

    shutil.rmtree(tmpdir)


def test_parse_index(temp_env):
    index_file, _, hash1, hash2, hash3 = temp_env
    data = parse_index(index_file)

    assert "01_LEGAL_AND_CORPORATE" in data
    assert "02_ASSET_AND_PROPERTY" in data

    assert data["01_LEGAL_AND_CORPORATE"]["test_doc1.pdf"] == hash1
    assert data["01_LEGAL_AND_CORPORATE"]["test_doc2.pdf"] == hash2
    assert data["02_ASSET_AND_PROPERTY"]["test_doc3.pdf"] == hash3


def test_validation_passes(temp_env):
    index_file, data_dir, _, _, _ = temp_env
    index_data = parse_index(index_file)
    exit_code, messages = validate_directory(data_dir, index_data)

    assert exit_code == 0
    # Checks that scanned messages list matched files
    assert any("MATCH: 01_LEGAL_AND_CORPORATE/test_doc1.pdf" in msg for msg in messages)
    assert any("MATCH: 01_LEGAL_AND_CORPORATE/test_doc2.pdf" in msg for msg in messages)
    assert any("MATCH: 02_ASSET_AND_PROPERTY/test_doc3.pdf" in msg for msg in messages)


def test_validation_fails_on_missing_file(temp_env):
    index_file, data_dir, _, _, _ = temp_env
    # Delete test_doc2
    (data_dir / "01_LEGAL_AND_CORPORATE" / "test_doc2.pdf").unlink()

    index_data = parse_index(index_file)
    exit_code, messages = validate_directory(data_dir, index_data)

    assert exit_code == 1
    assert any("MISSING: 01_LEGAL_AND_CORPORATE/test_doc2.pdf" in msg for msg in messages)


def test_validation_fails_on_hash_mismatch(temp_env):
    index_file, data_dir, _, _, _ = temp_env
    # Change test_doc1 content
    (data_dir / "01_LEGAL_AND_CORPORATE" / "test_doc1.pdf").write_text("corrupted content", encoding="utf-8")

    index_data = parse_index(index_file)
    exit_code, messages = validate_directory(data_dir, index_data)

    assert exit_code == 1
    assert any("HASH MISMATCH: 01_LEGAL_AND_CORPORATE/test_doc1.pdf" in msg for msg in messages)


def test_validation_flags_unindexed_file(temp_env):
    index_file, data_dir, _, _, _ = temp_env
    # Add unindexed file
    unindexed = data_dir / "01_LEGAL_AND_CORPORATE" / "unindexed.pdf"
    unindexed.write_text("secret payload", encoding="utf-8")

    index_data = parse_index(index_file)
    exit_code, messages = validate_directory(data_dir, index_data)

    # Note: Unindexed files do not cause hard error exit code 1 by default,
    # they just add a warning message. Let's assert exit_code remains 0 and warning is present.
    assert exit_code == 0
    assert any("UNINDEXED: 01_LEGAL_AND_CORPORATE/unindexed.pdf" in msg for msg in messages)
