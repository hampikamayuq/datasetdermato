from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path

from dataset_constants import (
    CORE_META,
    DERMNETNZ_MANIFEST,
    IMAGE_TYPES,
    QUALITY_AUDIT,
    RELATIONAL_DIR,
    SOURCE_CATALOG,
)


ALLOWED_BENIGN_MALIGNANT = {
    "",
    "benign",
    "malignant",
    "indeterminate",
    "indeterminate/benign",
    "indeterminate/malignant",
}

ALLOWED_DIAGNOSIS_CONFIRM_TYPES = {
    "",
    "histopathology",
    "serial imaging showing no change",
    "single image expert consensus",
    "confocal microscopy with consensus dermoscopy",
    "single contributor clinical assessment",
}

ALLOWED_LICENSE_STATUSES = {
    "",
    "pending",
    "approved",
    "restricted",
    "rejected",
}

ALLOWED_SPLITS = {"", "train", "validation", "test"}


@dataclass
class ValidationResult:
    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def display_path(path: Path) -> str:
    return path.as_posix()


def read_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_columns(path: Path, required_columns: list[str], result: ValidationResult) -> bool:
    previous_error_count = len(result.errors)
    if not path.exists():
        result.errors.append(f"File not found: {display_path(path)}")
        return False

    header = read_header(path)
    for column in required_columns:
        if column not in header:
            result.errors.append(f"Missing column '{column}' in {display_path(path)}")
    return len(result.errors) == previous_error_count


def validate_metadata(metadata_path: Path = CORE_META) -> ValidationResult:
    result = ValidationResult("metadata")
    if not require_columns(metadata_path, ["filename", "image_type", "diagnosis"], result):
        return result

    for row_number, row in enumerate(read_rows(metadata_path), start=2):
        filename = (row.get("filename") or "").strip()
        image_type = (row.get("image_type") or "").strip()
        diagnosis = (row.get("diagnosis") or "").strip()
        benign_malignant = (row.get("benign_malignant") or "").strip()
        confirm_type = (row.get("diagnosis_confirm_type") or "").strip()
        age = (row.get("age") or "").strip()

        if not filename:
            result.errors.append(f"Row {row_number}: filename is required")
        if not image_type:
            result.errors.append(f"Row {row_number}: image_type is required")
        elif image_type not in IMAGE_TYPES:
            result.errors.append(f"Row {row_number}: image_type '{image_type}' is not allowed")
        if not diagnosis:
            result.errors.append(f"Row {row_number}: diagnosis is required")

        if "benign_malignant" in row and benign_malignant not in ALLOWED_BENIGN_MALIGNANT:
            result.errors.append(
                f"Row {row_number}: benign_malignant '{benign_malignant}' is not allowed"
            )

        if diagnosis == "melanoma" and benign_malignant and benign_malignant != "malignant":
            result.errors.append(f"Row {row_number}: melanoma must have benign_malignant set to malignant")

        if (
            diagnosis == "nevus"
            and benign_malignant
            and benign_malignant not in {"benign", "indeterminate/benign", "indeterminate"}
        ):
            result.errors.append(
                f"Row {row_number}: nevus must be benign, indeterminate/benign, or indeterminate"
            )

        if "diagnosis_confirm_type" in row and confirm_type not in ALLOWED_DIAGNOSIS_CONFIRM_TYPES:
            result.errors.append(
                f"Row {row_number}: diagnosis_confirm_type '{confirm_type}' is not allowed"
            )

        if (
            benign_malignant
            in {"malignant", "indeterminate", "indeterminate/benign", "indeterminate/malignant"}
            and confirm_type
            and confirm_type != "histopathology"
        ):
            result.errors.append(
                f"Row {row_number}: malignant or indeterminate cases should use histopathology confirmation"
            )

        if age and (not age.isdigit() or int(age) > 120):
            result.errors.append(f"Row {row_number}: age must be an integer between 0 and 120")

    return result


def validate_sources(
    source_catalog_path: Path = SOURCE_CATALOG,
    dermnetnz_manifest_path: Path = DERMNETNZ_MANIFEST,
) -> ValidationResult:
    result = ValidationResult("sources")
    source_ok = require_columns(
        source_catalog_path,
        ["source_id", "source_name", "homepage_url", "redistribution_status", "license_or_terms_url"],
        result,
    )
    manifest_ok = require_columns(
        dermnetnz_manifest_path,
        [
            "image_id",
            "source_id",
            "page_url",
            "image_url",
            "condition_original",
            "condition_normalized",
            "license_status",
            "attribution",
            "accessed_at",
        ],
        result,
    )

    if source_ok:
        seen_sources: set[str] = set()
        for row_number, row in enumerate(read_rows(source_catalog_path), start=2):
            source_id = (row.get("source_id") or "").strip()
            if not source_id:
                result.errors.append(f"Row {row_number}: source_id is required in source catalog")
            elif source_id in seen_sources:
                result.errors.append(f"Row {row_number}: duplicate source_id '{source_id}'")
            seen_sources.add(source_id)

    if manifest_ok:
        for row_number, row in enumerate(read_rows(dermnetnz_manifest_path), start=2):
            source_id = (row.get("source_id") or "").strip()
            license_status = (row.get("license_status") or "").strip()
            page_url = (row.get("page_url") or "").strip()
            image_url = (row.get("image_url") or "").strip()

            if source_id and source_id != "dermnetnz":
                result.errors.append(f"Row {row_number}: source_id should be dermnetnz")
            if license_status and license_status not in ALLOWED_LICENSE_STATUSES:
                result.errors.append(
                    f"Row {row_number}: license_status '{license_status}' is not allowed"
                )
            if page_url and not page_url.startswith("https://"):
                result.errors.append(f"Row {row_number}: page_url should be an https URL")
            if image_url and not image_url.startswith("https://"):
                result.errors.append(f"Row {row_number}: image_url should be an https URL")

    return result


def validate_relational(metadata_directory: Path = RELATIONAL_DIR) -> ValidationResult:
    result = ValidationResult("relational metadata")
    required_files = {
        metadata_directory / "patients.csv": ["patient_id", "patient_hash"],
        metadata_directory / "cases.csv": [
            "case_id",
            "patient_id",
            "source_type",
            "specialty_service",
            "evidence_level",
        ],
        metadata_directory / "images.csv": ["image_id", "case_id", "image_type", "file_path"],
        metadata_directory / "surgical_procedures.csv": ["procedure_id", "case_id"],
        metadata_directory / "pathology_reports.csv": ["report_id", "case_id"],
        metadata_directory / "expert_reviews.csv": ["review_id", "case_id"],
        metadata_directory / "clinical_followups.csv": ["followup_id", "case_id"],
        metadata_directory / "annotations.csv": ["annotation_id", "image_id", "annotation_type"],
        QUALITY_AUDIT: ["audit_id", "target_type", "target_id", "audit_type", "audit_status"],
        metadata_directory / "consents_ethics.csv": ["ethics_id"],
        metadata_directory / "dataset_splits.csv": ["split_id", "patient_id", "split"],
    }

    for path, columns in required_files.items():
        require_columns(path, columns, result)

    split_path = metadata_directory / "dataset_splits.csv"
    if split_path.exists():
        patient_splits: dict[str, str] = {}
        for row_number, row in enumerate(read_rows(split_path), start=2):
            patient_id = (row.get("patient_id") or "").strip()
            split = (row.get("split") or "").strip()
            if split not in ALLOWED_SPLITS:
                result.errors.append(f"Row {row_number}: split '{split}' is not allowed")
            if not patient_id:
                continue
            if patient_id in patient_splits and patient_splits[patient_id] != split:
                result.errors.append(f"Patient {patient_id} appears in more than one split")
            patient_splits[patient_id] = split

    return result


def validate_all() -> list[ValidationResult]:
    return [
        validate_metadata(),
        validate_sources(),
        validate_relational(),
    ]


def print_report(results: list[ValidationResult]) -> int:
    total_errors = sum(len(result.errors) for result in results)
    total_warnings = sum(len(result.warnings) for result in results)

    for result in results:
        status = "OK" if result.ok else "ERROR"
        print(f"[{status}] {result.name}")
        for warning in result.warnings:
            print(f"  warning: {warning}")
        for error in result.errors:
            print(f"  error: {error}")

    if total_errors:
        print(f"Validation failed: {total_errors} error(s), {total_warnings} warning(s).")
        return 1

    print(f"All dataset validations passed: {total_warnings} warning(s).")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate dermatology dataset metadata.")
    parser.add_argument(
        "--only",
        choices=["all", "metadata", "sources", "relational"],
        default="all",
        help="Validation group to run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.only == "metadata":
        return print_report([validate_metadata()])
    if args.only == "sources":
        return print_report([validate_sources()])
    if args.only == "relational":
        return print_report([validate_relational()])
    return print_report(validate_all())


if __name__ == "__main__":
    raise SystemExit(main())
