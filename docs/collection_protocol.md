# Collection Protocol

## 1. Source registration

Before collecting images, create or update a row in `metadata/sources/source_catalog.csv` with:

- source identifier
- homepage URL
- terms or license URL
- redistribution status
- notes about attribution and access restrictions

## 2. DermNetNZ page review

For each DermNetNZ condition page:

1. Record the page URL in `metadata/sources/dermnetnz_manifest.csv`.
2. Record each candidate image URL.
3. Record the source condition name exactly as displayed.
4. Map the source condition to `annotations/labels/taxonomy.csv`.
5. Mark `license_status` as `pending`, `approved`, `restricted`, or `rejected`.

## 3. Image ingestion

Copy the source image to `data/raw/<source_id>/images/` and then register it with:

```bash
python scripts/register_image.py data/raw/<source_id>/images/<file> \
    --source-id <source_id> \
    --image-type "dermoscopic" \
    --diagnosis "melanoma" \
    [--patient-id P001] \
    [--lesion-id L001] \
    [--specialty oncologic_dermatology] \
    [--source-url "https://..."] \
    [--notes "..."]
```

The script automatically:
- rejects duplicates (SHA256 check against the manifest)
- strips EXIF and saves to `data/processed/images/`
- appends one row to `metadata/dataset_manifest.csv`
- appends one row to `metadata/standardized/core_metadata_template.csv`
- hashes the patient identifier before writing

Do not register an image until its source row has a known license status in `source_catalog.csv`.

## 4. After registration

Fill in any blank fields left in the manifest and core metadata rows that the script could not infer (e.g. `benign_malignant`, `diagnosis_confirm_type`, `anatom_site_general`).

Run validation to confirm no errors:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate_all.ps1
```

## 5. Quality checks

Minimum recommended checks (most are enforced by the script; these require human review):

- image is dermatology-relevant
- no visible identifying information unless explicitly allowed and ethically reviewed
- diagnosis label is traceable to source page or expert review

## 6. Splits

Create train/validation/test splits in `data/processed/splits/`. If patient or lesion identifiers exist, split by patient or lesion, not by image, to avoid leakage.
