"""Tests for ingest_image core utilities."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from PIL import Image

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from ingest_image import file_sha256, hash_identifier, make_uuid, remove_exif


# ---------------------------------------------------------------------------
# make_uuid
# ---------------------------------------------------------------------------

def test_make_uuid_format():
    uid = make_uuid()
    assert len(uid) == 36
    assert uid.count("-") == 4


def test_make_uuid_unique():
    assert make_uuid() != make_uuid()


# ---------------------------------------------------------------------------
# hash_identifier
# ---------------------------------------------------------------------------

def test_hash_identifier_deterministic():
    assert hash_identifier("P001", "dermnet") == hash_identifier("P001", "dermnet")


def test_hash_identifier_different_salt():
    assert hash_identifier("P001", "dermnet") != hash_identifier("P001", "isic")


def test_hash_identifier_different_value():
    assert hash_identifier("P001", "s") != hash_identifier("P002", "s")


def test_hash_identifier_length():
    result = hash_identifier("any", "salt")
    assert len(result) == 64  # SHA256 hex


def test_hash_identifier_hides_original(tmp_path):
    result = hash_identifier("PAC-001", "salt")
    assert "PAC-001" not in result


# ---------------------------------------------------------------------------
# file_sha256
# ---------------------------------------------------------------------------

def test_file_sha256_correct(tmp_path):
    f = tmp_path / "data.bin"
    f.write_bytes(b"hello world")
    expected = hashlib.sha256(b"hello world").hexdigest()
    assert file_sha256(f) == expected


def test_file_sha256_different_files(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"aaa")
    b.write_bytes(b"bbb")
    assert file_sha256(a) != file_sha256(b)


def test_file_sha256_same_content(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"same")
    b.write_bytes(b"same")
    assert file_sha256(a) == file_sha256(b)


# ---------------------------------------------------------------------------
# remove_exif
# ---------------------------------------------------------------------------

def _make_image(path: Path, size=(100, 80), color=(180, 100, 60), mode="RGB") -> Path:
    Image.new(mode, size, color=color).save(path)
    return path


def test_remove_exif_creates_output(tmp_path):
    src = _make_image(tmp_path / "src.jpg")
    out = tmp_path / "out.jpg"
    remove_exif(src, out)
    assert out.exists()


def test_remove_exif_returns_dimensions(tmp_path):
    src = _make_image(tmp_path / "src.jpg", size=(320, 240))
    out = tmp_path / "out.jpg"
    w, h = remove_exif(src, out)
    assert w == 320
    assert h == 240


def test_remove_exif_creates_parent_dirs(tmp_path):
    src = _make_image(tmp_path / "src.jpg")
    out = tmp_path / "deep" / "nested" / "out.jpg"
    remove_exif(src, out)
    assert out.exists()


def test_remove_exif_png(tmp_path):
    src = _make_image(tmp_path / "src.png", mode="RGB")
    out = tmp_path / "out.png"
    w, h = remove_exif(src, out)
    assert out.exists()
    assert (w, h) == (100, 80)


def test_remove_exif_pixel_values_preserved(tmp_path):
    color = (123, 45, 67)
    src = _make_image(tmp_path / "src.png", color=color, mode="RGB")
    out = tmp_path / "out.png"
    remove_exif(src, out)
    with Image.open(out) as img:
        pixel = img.getpixel((0, 0))
    assert pixel == color
