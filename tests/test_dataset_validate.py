"""Tests for dataset_validate: metadata, sources, relational, split leakage."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from dataset_validate import (
    ValidationResult,
    validate_metadata,
    validate_relational,
    validate_sources,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_csv(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return path
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return path


def _valid_meta_row(**overrides) -> dict:
    base = {
        "filename": "img.jpg",
        "image_type": "dermoscopic",
        "diagnosis": "melanoma",
        "benign_malignant": "malignant",
        "diagnosis_confirm_type": "histopathology",
        "age": "45",
    }
    return {**base, **overrides}


# ---------------------------------------------------------------------------
# validate_metadata
# ---------------------------------------------------------------------------

def test_metadata_valid(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [_valid_meta_row()])
    result = validate_metadata(path)
    assert result.ok


def test_metadata_missing_file(tmp_path):
    result = validate_metadata(tmp_path / "missing.csv")
    assert not result.ok
    assert any("not found" in e for e in result.errors)


def test_metadata_missing_required_column(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [{"filename": "x.jpg", "image_type": "dermoscopic"}])
    result = validate_metadata(path)
    assert not result.ok
    assert any("diagnosis" in e for e in result.errors)


def test_metadata_empty_filename(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [_valid_meta_row(filename="")])
    result = validate_metadata(path)
    assert not result.ok
    assert any("filename" in e for e in result.errors)


def test_metadata_invalid_image_type(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [_valid_meta_row(image_type="selfie")])
    result = validate_metadata(path)
    assert not result.ok
    assert any("image_type" in e for e in result.errors)


def test_metadata_melanoma_must_be_malignant(tmp_path):
    row = _valid_meta_row(diagnosis="melanoma", benign_malignant="benign")
    path = _write_csv(tmp_path / "meta.csv", [row])
    result = validate_metadata(path)
    assert not result.ok
    assert any("malignant" in e for e in result.errors)


def test_metadata_nevus_not_malignant(tmp_path):
    row = _valid_meta_row(diagnosis="nevus", benign_malignant="malignant",
                          diagnosis_confirm_type="histopathology")
    path = _write_csv(tmp_path / "meta.csv", [row])
    result = validate_metadata(path)
    assert not result.ok


def test_metadata_malignant_needs_histopathology(tmp_path):
    row = _valid_meta_row(benign_malignant="malignant",
                          diagnosis_confirm_type="single image expert consensus")
    path = _write_csv(tmp_path / "meta.csv", [row])
    result = validate_metadata(path)
    assert not result.ok
    assert any("histopathology" in e for e in result.errors)


def test_metadata_invalid_age(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [_valid_meta_row(age="150")])
    result = validate_metadata(path)
    assert not result.ok
    assert any("age" in e for e in result.errors)


def test_metadata_age_non_numeric(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [_valid_meta_row(age="forty")])
    result = validate_metadata(path)
    assert not result.ok


def test_metadata_header_only_no_rows(tmp_path):
    path = tmp_path / "meta.csv"
    path.write_text("filename,image_type,diagnosis\n")
    result = validate_metadata(path)
    assert result.ok


def test_metadata_surgical_image_type_valid(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [_valid_meta_row(image_type="surgical")])
    result = validate_metadata(path)
    assert result.ok


def test_metadata_histopathology_image_type_valid(tmp_path):
    path = _write_csv(tmp_path / "meta.csv", [_valid_meta_row(image_type="histopathology")])
    result = validate_metadata(path)
    assert result.ok


# ---------------------------------------------------------------------------
# validate_sources
# ---------------------------------------------------------------------------

def _valid_source_row(**overrides) -> dict:
    base = {
        "source_id": "dermnetnz",
        "source_name": "DermNetNZ",
        "homepage_url": "https://dermnetnz.org/",
        "redistribution_status": "verify before redistribution",
        "license_or_terms_url": "https://dermnetnz.org/terms",
    }
    return {**base, **overrides}


def _valid_manifest_row(**overrides) -> dict:
    base = {
        "image_id": "abc123",
        "source_id": "dermnetnz",
        "page_url": "https://dermnetnz.org/topics/melanoma",
        "image_url": "https://dermnetnz.org/img.jpg",
        "condition_original": "Melanoma",
        "condition_normalized": "melanoma",
        "license_status": "approved",
        "attribution": "DermNetNZ",
        "accessed_at": "2026-01-01",
    }
    return {**base, **overrides}


def test_sources_valid(tmp_path):
    cat = _write_csv(tmp_path / "source_catalog.csv", [_valid_source_row()])
    manifest = _write_csv(tmp_path / "dermnetnz_manifest.csv", [_valid_manifest_row()])
    result = validate_sources(cat, manifest)
    assert result.ok


def test_sources_duplicate_source_id(tmp_path):
    cat = _write_csv(tmp_path / "source_catalog.csv",
                     [_valid_source_row(), _valid_source_row()])
    manifest = _write_csv(tmp_path / "dermnetnz_manifest.csv", [_valid_manifest_row()])
    result = validate_sources(cat, manifest)
    assert not result.ok
    assert any("duplicate" in e.lower() for e in result.errors)


def test_sources_invalid_license_status(tmp_path):
    cat = _write_csv(tmp_path / "source_catalog.csv", [_valid_source_row()])
    manifest = _write_csv(tmp_path / "dermnetnz_manifest.csv",
                          [_valid_manifest_row(license_status="unknown_status")])
    result = validate_sources(cat, manifest)
    assert not result.ok


def test_sources_http_url_rejected(tmp_path):
    cat = _write_csv(tmp_path / "source_catalog.csv", [_valid_source_row()])
    manifest = _write_csv(tmp_path / "dermnetnz_manifest.csv",
                          [_valid_manifest_row(page_url="http://dermnetnz.org/topics/melanoma")])
    result = validate_sources(cat, manifest)
    assert not result.ok
    assert any("https" in e for e in result.errors)


# ---------------------------------------------------------------------------
# validate_relational — split leakage
# ---------------------------------------------------------------------------

def _write_relational(base: Path) -> dict[str, Path]:
    base.mkdir(parents=True, exist_ok=True)
    tables = {
        "patients.csv": [{"patient_id": "p1", "patient_hash": "h1"}],
        "cases.csv": [{"case_id": "c1", "patient_id": "p1", "source_type": "pathology_archive",
                        "specialty_service": "general_dermatology", "evidence_level": "gold"}],
        "images.csv": [{"image_id": "i1", "case_id": "c1", "image_type": "dermoscopic", "file_path": "img.jpg"}],
        "surgical_procedures.csv": [{"procedure_id": "s1", "case_id": "c1"}],
        "pathology_reports.csv": [{"report_id": "r1", "case_id": "c1"}],
        "expert_reviews.csv": [{"review_id": "e1", "case_id": "c1"}],
        "clinical_followups.csv": [{"followup_id": "f1", "case_id": "c1"}],
        "annotations.csv": [{"annotation_id": "a1", "image_id": "i1", "annotation_type": "bbox"}],
        "consents_ethics.csv": [{"ethics_id": "eth1"}],
        "dataset_splits.csv": [{"split_id": "sp1", "patient_id": "p1", "split": "train"}],
    }
    paths = {}
    for name, rows in tables.items():
        p = base / name
        _write_csv(p, rows)
        paths[name] = p

    audit = base.parent / "audits" / "quality_audit.csv"
    _write_csv(audit, [{"audit_id": "au1", "target_type": "image",
                         "target_id": "i1", "audit_type": "duplicate", "audit_status": "ok"}])
    return paths


def test_relational_valid(tmp_path):
    rel = tmp_path / "relational"
    import dataset_constants as dc
    import dataset_validate as dv
    original_quality = dc.QUALITY_AUDIT
    dc.QUALITY_AUDIT = tmp_path / "audits" / "quality_audit.csv"
    try:
        _write_relational(rel)
        result = validate_relational(rel)
        assert result.ok, result.errors
    finally:
        dc.QUALITY_AUDIT = original_quality


def test_relational_patient_in_two_splits(tmp_path):
    rel = tmp_path / "relational"
    import dataset_constants as dc
    import dataset_validate as dv
    original_quality = dc.QUALITY_AUDIT
    dc.QUALITY_AUDIT = tmp_path / "audits" / "quality_audit.csv"
    try:
        _write_relational(rel)
        splits = rel / "dataset_splits.csv"
        _write_csv(splits, [
            {"split_id": "sp1", "patient_id": "p1", "split": "train"},
            {"split_id": "sp2", "patient_id": "p1", "split": "test"},
        ])
        result = validate_relational(rel)
        assert not result.ok
        assert any("p1" in e for e in result.errors)
    finally:
        dc.QUALITY_AUDIT = original_quality


def test_relational_invalid_split_value(tmp_path):
    rel = tmp_path / "relational"
    import dataset_constants as dc
    original_quality = dc.QUALITY_AUDIT
    dc.QUALITY_AUDIT = tmp_path / "audits" / "quality_audit.csv"
    try:
        _write_relational(rel)
        splits = rel / "dataset_splits.csv"
        _write_csv(splits, [
            {"split_id": "sp1", "patient_id": "p1", "split": "hold_out"},
        ])
        result = validate_relational(rel)
        assert not result.ok
        assert any("hold_out" in e for e in result.errors)
    finally:
        dc.QUALITY_AUDIT = original_quality
