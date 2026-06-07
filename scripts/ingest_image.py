from __future__ import annotations

import hashlib
import uuid
from pathlib import Path

from PIL import Image


DATASET_ROOT = Path(__file__).resolve().parents[1]


def make_uuid() -> str:
    return str(uuid.uuid4())


def hash_identifier(value: str, salt: str) -> str:
    raw = f"{salt}:{value}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def remove_exif(input_path: Path, output_path: Path) -> tuple[int, int]:
    with Image.open(input_path) as image:
        clean = Image.new(image.mode, image.size)
        data = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
        clean.putdata(data)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        clean.save(output_path)
        return clean.size


def create_image_record(
    case_id: str,
    input_path: Path,
    output_path: Path,
    image_type: str,
    acquisition_year: int | None = None,
    device: str | None = None,
) -> dict[str, object]:
    width, height = remove_exif(input_path, output_path)

    return {
        "image_id": make_uuid(),
        "case_id": case_id,
        "image_type": image_type,
        "file_path": str(output_path),
        "original_filename": input_path.name,
        "acquisition_year": acquisition_year,
        "device": device,
        "width": width,
        "height": height,
        "anonymization_status": "exif_removed",
        "has_identifying_risk": None,
        "sha256": file_sha256(output_path),
    }


if __name__ == "__main__":
    raise SystemExit(
        "Import this module from a controlled ingestion script after ethics and storage paths are configured."
    )
