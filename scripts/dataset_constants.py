from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "metadata" / "dataset_manifest.csv"
CORE_META = REPO_ROOT / "metadata" / "standardized" / "core_metadata_template.csv"
PROCESSED_DIR = REPO_ROOT / "data" / "processed" / "images"
SOURCE_CATALOG = REPO_ROOT / "metadata" / "sources" / "source_catalog.csv"
DERMNETNZ_MANIFEST = REPO_ROOT / "metadata" / "sources" / "dermnetnz_manifest.csv"
RELATIONAL_DIR = REPO_ROOT / "metadata" / "relational"
QUALITY_AUDIT = REPO_ROOT / "metadata" / "audits" / "quality_audit.csv"
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
