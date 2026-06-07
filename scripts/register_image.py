"""Register a single dermatology image into the dataset.

Usage:
    python scripts/register_image.py image.jpg --source-id dermnetnz \
        --image-type "clinical: close-up" --diagnosis melanoma
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dataset_ops import IMAGE_TYPES, SOURCE_TYPE_OPTIONS, SPECIALTY_OPTIONS, register_image_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register a dermatology image into the dataset.")
    parser.add_argument("image", help="Path to the source image file")
    parser.add_argument("--source-id", required=True, help="Source identifier from source_catalog.csv")
    parser.add_argument("--image-type", required=True, choices=IMAGE_TYPES, help="Image type")
    parser.add_argument("--diagnosis", required=True, help="Original diagnosis label")
    parser.add_argument("--patient-id", default="", help="Raw patient identifier; saved only as a hash")
    parser.add_argument("--lesion-id", default="", help="Lesion identifier")
    parser.add_argument("--case-id", default="", help="Existing case UUID to link this image to")
    parser.add_argument("--source-type", default="", choices=SOURCE_TYPE_OPTIONS, help="Case/archive origin")
    parser.add_argument(
        "--specialty",
        "--specialty-service",
        dest="specialty_service",
        default="",
        choices=SPECIALTY_OPTIONS,
        help="Dermatology specialty service",
    )
    parser.add_argument("--source-url", default="", help="Original image URL, when available")
    parser.add_argument("--notes", default="", help="Free-text notes")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = register_image_file(
            input_path=Path(args.image),
            source_id=args.source_id,
            image_type=args.image_type,
            diagnosis=args.diagnosis,
            patient_id=args.patient_id,
            lesion_id=args.lesion_id,
            case_id=args.case_id,
            source_type=args.source_type,
            specialty_service=args.specialty_service,
            source_url=args.source_url,
            notes=args.notes,
        )
    except (FileNotFoundError, ValueError) as exc:
        sys.exit(f"Error: {exc}")

    print(f"Registered: {result['image_id']}")
    print(f"  output : {result['filename']}")
    print(f"  sha256 : {result['sha256'][:16]}...")
    print(f"  size   : {result['width']}x{result['height']}")


if __name__ == "__main__":
    main()
