"""Register a single dermatology image into the dataset.

Usage
-----
python scripts/register_image.py <image_path> \\
    --source-id dermnet \\
    --image-type dermoscopic \\
    --diagnosis melanoma \\
    [--patient-id P001] \\
    [--lesion-id L001] \\
    [--case-id <uuid>] \\
    [--specialty oncologic_dermatology] \\
    [--device "Heine Delta 30"] \\
    [--year 2018] \\
    [--notes "..."]

The script:
  1. Checks for SHA256 duplicates against dataset_manifest.csv
  2. Copies and strips EXIF to data/processed/images/
  3. Appends one row to metadata/dataset_manifest.csv
  4. Appends one row to metadata/standardized/core_metadata_template.csv
  5. Prints a summary with the assigned image_id
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "metadata" / "dataset_manifest.csv"
CORE_META = REPO_ROOT / "metadata" / "standardized" / "core_metadata_template.csv"
PROCESSED_DIR = REPO_ROOT / "data" / "processed" / "images"

# Import shared utilities from the same scripts/ directory.
sys.path.insert(0, str(Path(__file__).parent))
from ingest_image import file_sha256, hash_identifier, make_uuid, remove_exif


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_sha256_set(manifest: Path) -> set[str]:
    if not manifest.exists() or manifest.stat().st_size == 0:
        return set()
    with manifest.open(newline="", encoding="utf-8") as fh:
        return {row["sha256"] for row in csv.DictReader(fh) if row.get("sha256")}


def _append_row(csv_path: Path, row: dict[str, object]) -> None:
    write_header = not csv_path.exists() or csv_path.stat().st_size == 0
    with csv_path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()), extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def _output_filename(source_id: str, diagnosis: str, image_id: str, suffix: str) -> str:
    slug = diagnosis.lower().replace(" ", "_")
    return f"{source_id}_{slug}_{image_id[:8]}{suffix}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def register(args: argparse.Namespace) -> None:
    src = Path(args.image).resolve()
    if not src.exists():
        sys.exit(f"Error: file not found: {src}")

    # 1. Duplicate check
    existing_hashes = _read_sha256_set(MANIFEST)
    src_hash = file_sha256(src)
    if src_hash in existing_hashes:
        sys.exit(f"Duplicate: SHA256 {src_hash[:16]}... already exists in manifest.")

    # 2. Build paths
    out_name = _output_filename(args.source_id, args.diagnosis, make_uuid(), src.suffix)
    out_path = PROCESSED_DIR / out_name
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 3. Strip EXIF and copy
    width, height = remove_exif(src, out_path)
    processed_hash = file_sha256(out_path)
    image_id = make_uuid()

    # 4. Patient hash (stable, anonymous)
    patient_id = args.patient_id or ""
    patient_hash = hash_identifier(patient_id, args.source_id) if patient_id else ""

    # 5. Manifest row
    manifest_row = {
        "image_id": image_id,
        "filename": str(out_path.relative_to(REPO_ROOT)),
        "source_id": args.source_id,
        "source_type": "",
        "specialty_service": args.specialty or "",
        "source_image_url": args.source_url or "",
        "source_page_url": "",
        "source_license_status": "pending",
        "attribution": "",
        "accessed_at": str(date.today()),
        "sha256": processed_hash,
        "width": width,
        "height": height,
        "image_type": args.image_type,
        "diagnosis_original": args.diagnosis,
        "diagnosis_normalized": args.diagnosis,
        "label_id": args.diagnosis.lower().replace(" ", "_"),
        "patient_id": patient_hash,
        "lesion_id": args.lesion_id or "",
        "split": "",
        "quality_status": "pending",
        "review_status": "pending",
        "notes": args.notes or "",
    }
    _append_row(MANIFEST, manifest_row)

    # 6. Core metadata row
    core_row = {
        "filename": manifest_row["filename"],
        "image_type": args.image_type,
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
        "lesion_id": args.lesion_id or "",
        "patient_id": patient_hash,
        "rcm_case_id": args.case_id or "",
        "clin_size_long_diam_mm": "",
        "diagnosis": args.diagnosis,
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
    _append_row(CORE_META, core_row)

    print(f"Registered: {image_id}")
    print(f"  output : {out_path.relative_to(REPO_ROOT)}")
    print(f"  sha256 : {processed_hash[:16]}...")
    print(f"  size   : {width}x{height}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Register a dermatology image into the dataset.")
    p.add_argument("image", help="Path to the source image file")
    p.add_argument("--source-id", required=True, help="Source identifier from source_catalog.csv")
    p.add_argument("--image-type", required=True,
                   choices=["dermoscopic", "clinical: overview", "clinical: close-up",
                            "TBP tile: close-up", "TBP tile: overview"],
                   help="Image type")
    p.add_argument("--diagnosis", required=True, help="Original diagnosis label")
    p.add_argument("--patient-id", help="Raw patient identifier (will be hashed)")
    p.add_argument("--lesion-id", help="Lesion identifier")
    p.add_argument("--case-id", help="Existing case UUID to link this image to")
    p.add_argument("--specialty", help="specialty_service value")
    p.add_argument("--device", help="Acquisition device")
    p.add_argument("--year", type=int, help="Acquisition year")
    p.add_argument("--source-url", help="Original image URL (for web sources)")
    p.add_argument("--notes", help="Free-text notes")
    return p.parse_args()


if __name__ == "__main__":
    register(_parse_args())
