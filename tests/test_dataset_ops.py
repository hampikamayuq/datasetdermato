"""Tests for dataset_ops: registration logic, duplicate detection, slugify."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
from PIL import Image

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import dataset_constants as _dc
from dataset_ops import append_row, csv_fieldnames, load_diagnoses, load_source_ids, register_image_file, slugify


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolated_repo(tmp_path, monkeypatch):
    """Redirect all dataset paths to a temporary directory."""
    manifest = tmp_path / "metadata" / "dataset_manifest.csv"
    core_meta = tmp_path / "metadata" / "standardized" / "core_metadata_template.csv"
    processed = tmp_path / "data" / "processed" / "images"
    source_catalog = tmp_path / "metadata" / "sources" / "source_catalog.csv"
    taxonomy = tmp_path / "annotations" / "labels" / "taxonomy.csv"

    manifest.parent.mkdir(parents=True)
    core_meta.parent.mkdir(parents=True)
    processed.mkdir(parents=True)
    source_catalog.parent.mkdir(parents=True)
    taxonomy.parent.mkdir(parents=True)

    # Seed source catalog and taxonomy
    with source_catalog.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source_id", "source_name", "homepage_url",
                                           "source_type", "access_type",
                                           "redistribution_status", "license_or_terms_url", "notes"])
        w.writeheader()
        w.writerow({"source_id": "test_source", "source_name": "Test",
                    "homepage_url": "", "source_type": "", "access_type": "",
                    "redistribution_status": "", "license_or_terms_url": "", "notes": ""})

    with taxonomy.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["label_id", "label_name", "parent_label",
                                           "clinical_group", "malignancy", "isic_mapping", "notes"])
        w.writeheader()
        w.writerow({"label_id": "melanoma", "label_name": "Melanoma",
                    "parent_label": "", "clinical_group": "", "malignancy": "malignant",
                    "isic_mapping": "", "notes": ""})

    import dataset_ops
    monkeypatch.setattr(dataset_ops, "MANIFEST", manifest)
    monkeypatch.setattr(dataset_ops, "CORE_META", core_meta)
    monkeypatch.setattr(dataset_ops, "PROCESSED_DIR", processed)
    monkeypatch.setattr(dataset_ops, "SOURCE_CATALOG", source_catalog)
    monkeypatch.setattr(dataset_ops, "TAXONOMY", taxonomy)
    monkeypatch.setattr(dataset_ops, "REPO_ROOT", tmp_path)

    yield {
        "manifest": manifest,
        "core_meta": core_meta,
        "processed": processed,
        "source_catalog": source_catalog,
        "taxonomy": taxonomy,
        "tmp": tmp_path,
    }


def _make_image(path: Path, color=(200, 120, 80)) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (100, 80), color=color).save(path)
    return path


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------

def test_slugify_basic():
    assert slugify("melanoma") == "melanoma"


def test_slugify_spaces():
    assert slugify("basal cell carcinoma") == "basal_cell_carcinoma"


def test_slugify_accents():
    assert slugify("névus") == "nevus"


def test_slugify_uppercase():
    assert slugify("Melanoma") == "melanoma"


def test_slugify_empty():
    assert slugify("") == "unknown"


def test_slugify_special_chars():
    assert slugify("BCC/SCC") == "bcc_scc"


# ---------------------------------------------------------------------------
# load_source_ids / load_diagnoses
# ---------------------------------------------------------------------------

def test_load_source_ids(isolated_repo):
    assert "test_source" in load_source_ids()


def test_load_diagnoses(isolated_repo):
    assert "Melanoma" in load_diagnoses()


# ---------------------------------------------------------------------------
# csv_fieldnames
# ---------------------------------------------------------------------------

def test_csv_fieldnames_reads_header(tmp_path):
    f = tmp_path / "test.csv"
    f.write_text('col_a,col_b,"col c"\n')
    assert csv_fieldnames(f, []) == ["col_a", "col_b", "col c"]


def test_csv_fieldnames_missing_file(tmp_path):
    assert csv_fieldnames(tmp_path / "missing.csv", ["fallback"]) == ["fallback"]


def test_csv_fieldnames_empty_file(tmp_path):
    f = tmp_path / "empty.csv"
    f.write_text("")
    assert csv_fieldnames(f, ["fallback"]) == ["fallback"]


# ---------------------------------------------------------------------------
# append_row
# ---------------------------------------------------------------------------

def test_append_row_creates_header(tmp_path):
    f = tmp_path / "out.csv"
    append_row(f, {"a": "1", "b": "2"})
    rows = list(csv.DictReader(f.open()))
    assert rows[0]["a"] == "1"
    assert rows[0]["b"] == "2"


def test_append_row_multiple(tmp_path):
    f = tmp_path / "out.csv"
    append_row(f, {"x": "1"})
    append_row(f, {"x": "2"})
    rows = list(csv.DictReader(f.open()))
    assert len(rows) == 2


# ---------------------------------------------------------------------------
# register_image_file
# ---------------------------------------------------------------------------

def test_register_returns_expected_keys(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    result = register_image_file(img, "test_source", "dermoscopic", "melanoma")
    assert {"image_id", "filename", "sha256", "width", "height"} <= result.keys()


def test_register_writes_manifest(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    register_image_file(img, "test_source", "dermoscopic", "melanoma")
    rows = list(csv.DictReader(isolated_repo["manifest"].open()))
    assert len(rows) == 1
    assert rows[0]["diagnosis_original"] == "melanoma"


def test_register_writes_core_meta(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    register_image_file(img, "test_source", "dermoscopic", "melanoma")
    rows = list(csv.DictReader(isolated_repo["core_meta"].open()))
    assert len(rows) == 1


def test_register_hashes_patient_id(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    register_image_file(img, "test_source", "dermoscopic", "melanoma", patient_id="PAC001")
    rows = list(csv.DictReader(isolated_repo["manifest"].open()))
    assert rows[0]["patient_id"] != "PAC001"
    assert len(rows[0]["patient_id"]) == 64


def test_register_copies_processed_image(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    result = register_image_file(img, "test_source", "dermoscopic", "melanoma")
    out = isolated_repo["processed"] / Path(result["filename"]).name
    assert out.exists()


def test_register_duplicate_rejected(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    register_image_file(img, "test_source", "dermoscopic", "melanoma")
    with pytest.raises(ValueError, match="Duplicate"):
        register_image_file(img, "test_source", "dermoscopic", "melanoma")


def test_register_duplicate_leaves_no_temp_file(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    register_image_file(img, "test_source", "dermoscopic", "melanoma")
    before = set(isolated_repo["processed"].iterdir())
    with pytest.raises(ValueError):
        register_image_file(img, "test_source", "dermoscopic", "melanoma")
    after = set(isolated_repo["processed"].iterdir())
    assert before == after  # no residual temp file


def test_register_unknown_source_rejected(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    with pytest.raises(ValueError, match="Unknown source_id"):
        register_image_file(img, "nonexistent_source", "dermoscopic", "melanoma")


def test_register_invalid_image_type_rejected(isolated_repo, tmp_path):
    img = _make_image(tmp_path / "img.jpg")
    with pytest.raises(ValueError, match="image_type"):
        register_image_file(img, "test_source", "invalid_type", "melanoma")


def test_register_missing_file_raises(isolated_repo, tmp_path):
    with pytest.raises(FileNotFoundError):
        register_image_file(tmp_path / "missing.jpg", "test_source", "dermoscopic", "melanoma")


def test_register_two_different_images(isolated_repo, tmp_path):
    img1 = _make_image(tmp_path / "img1.jpg", color=(200, 100, 50))
    img2 = _make_image(tmp_path / "img2.jpg", color=(50, 100, 200))
    r1 = register_image_file(img1, "test_source", "dermoscopic", "melanoma")
    r2 = register_image_file(img2, "test_source", "dermoscopic", "nevus")
    assert r1["image_id"] != r2["image_id"]
    assert r1["sha256"] != r2["sha256"]
    rows = list(csv.DictReader(isolated_repo["manifest"].open()))
    assert len(rows) == 2
