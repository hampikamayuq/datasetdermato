from __future__ import annotations

import csv
import re
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any

from ingest_image import file_sha256, hash_identifier, make_uuid, remove_exif


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "metadata" / "dataset_manifest.csv"
CORE_META = REPO_ROOT / "metadata" / "standardized" / "core_metadata_template.csv"
PROCESSED_DIR = REPO_ROOT / "data" / "processed" / "images"
SOURCE_CATALOG = REPO_ROOT / "metadata" / "sources" / "source_catalog.csv"
TAXONOMY = REPO_ROOT / "annotations" / "labels" / "taxonomy.csv"

IMAGE_TYPES = [
    "dermoscopic",
    "clinical: overview",
    "clinical: close-up",
    "surgical",
    "histopathology",
    "TBP tile: close-up",
    "TBP tile: overview",
]

SOURCE_TYPE_OPTIONS = [
    "",
    "faculty_collection",
    "resident_collection",
    "pathology_archive",
    "clinical_archive",
    "conference_archive",
    "research_project",
    "private_practice_archive",
    "institutional_database",
]

SPECIALTY_OPTIONS = [
    "",
    "general_dermatology",
    "pediatric_dermatology",
    "dermatologic_surgery",
    "dermatopathology",
    "oncologic_dermatology",
    "trichology",
    "hanseniasis",
    "autoimmune_skin_disease",
    "contact_dermatitis",
    "pigmented_lesions",
    "inflammatory_skin_disease",
    "infectious_dermatology",
    "tropical_dermatology",
    "cutaneous_tumors",
    "dermoscopy",
]


def load_csv_values(path: Path, column: str) -> list[str]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [row[column] for row in csv.DictReader(handle) if row.get(column)]


def load_source_ids() -> list[str]:
    return load_csv_values(SOURCE_CATALOG, "source_id")


def load_diagnoses() -> list[str]:
    return load_csv_values(TAXONOMY, "label_name")


def known_sha256s() -> set[str]:
    if not MANIFEST.exists() or MANIFEST.stat().st_size == 0:
        return set()
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        return {row["sha256"] for row in csv.DictReader(handle) if row.get("sha256")}


def csv_fieldnames(csv_path: Path, fallback: list[str]) -> list[str]:
    if csv_path.exists() and csv_path.stat().st_size > 0:
        header = csv_path.read_text(encoding="utf-8").splitlines()[0]
        if header.strip():
            return header.split(",")
    return fallback


def append_row(csv_path: Path, row: dict[str, Any]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not csv_path.exists() or csv_path.stat().st_size == 0
    fieldnames = csv_fieldnames(csv_path, list(row.keys()))
    with csv_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "unknown"


def register_image_file(
    input_path: Path,
    source_id: str,
    image_type: str,
    diagnosis: str,
    patient_id: str = "",
    lesion_id: str = "",
    case_id: str = "",
    source_type: str = "",
    specialty_service: str = "",
    source_url: str = "",
    notes: str = "",
    original_name: str | None = None,
) -> dict[str, Any]:
    src = input_path.resolve()
    if not src.exists():
        raise FileNotFoundError(f"File not found: {src}")

    if source_id not in load_source_ids():
        raise ValueError(f"Unknown source_id: {source_id}. Add it to metadata/sources/source_catalog.csv first.")
    if image_type not in IMAGE_TYPES:
        raise ValueError(f"Invalid image_type: {image_type}")
    if source_type not in SOURCE_TYPE_OPTIONS:
        raise ValueError(f"Invalid source_type: {source_type}")
    if specialty_service not in SPECIALTY_OPTIONS:
        raise ValueError(f"Invalid specialty_service: {specialty_service}")

    image_id = make_uuid()
    suffix = Path(original_name or src.name).suffix or ".jpg"
    out_name = f"{source_id}_{slugify(diagnosis)}_{image_id[:8]}{suffix}"
    out_path = PROCESSED_DIR / out_name
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    width, height = remove_exif(src, out_path)
    processed_hash = file_sha256(out_path)

    if processed_hash in known_sha256s():
        out_path.unlink(missing_ok=True)
        raise ValueError(f"Duplicate image: SHA256 {processed_hash[:16]} already exists in manifest.")

    patient_hash = hash_identifier(patient_id, source_id) if patient_id else ""
    filename = str(out_path.relative_to(REPO_ROOT)).replace("\\", "/")

    manifest_row = {
        "image_id": image_id,
        "filename": filename,
        "source_id": source_id,
        "source_type": source_type,
        "specialty_service": specialty_service,
        "source_image_url": source_url,
        "source_page_url": "",
        "source_license_status": "pending",
        "attribution": "",
        "accessed_at": str(date.today()),
        "sha256": processed_hash,
        "width": width,
        "height": height,
        "image_type": image_type,
        "diagnosis_original": diagnosis,
        "diagnosis_normalized": diagnosis,
        "label_id": slugify(diagnosis),
        "patient_id": patient_hash,
        "lesion_id": lesion_id,
        "split": "",
        "quality_status": "pending",
        "review_status": "pending",
        "notes": notes,
    }
    append_row(MANIFEST, manifest_row)

    core_row = {
        "filename": filename,
        "image_type": image_type,
        "dermoscopic_type": "",
        "tbp_tile_type": "",
        "age": "",
        "sex": "",
        "anatom_site_general": "",
        "anatom_site_special": "",
        "fitzpatrick_skin_type": "",
        "acquisition_day": "",
        "personal_hx_mm": "",
        "family_hx_mm": "",
        "lesion_id": lesion_id,
        "patient_id": patient_hash,
        "rcm_case_id": case_id,
        "clin_size_long_diam_mm": "",
        "diagnosis": diagnosis,
        "benign_malignant": "",
        "concomitant_biopsy": "",
        "diagnosis_confirm_type": "",
        "melanocytic": "",
        "nevus_type": "",
        "mel_thick_mm": "",
        "mel_class": "",
        "mel_type": "",
        "mel_mitotic_index": "",
        "mel_ulcer": "",
    }
    append_row(CORE_META, core_row)

    return {
        "image_id": image_id,
        "filename": filename,
        "sha256": processed_hash,
        "width": width,
        "height": height,
    }
