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

Use the following naming convention:

```text
data/raw/<source_id>/images/<source_id>_<condition_slug>_<sequence>.<ext>
data/processed/images/<source_id>_<condition_slug>_<sequence>_processed.<ext>
```

Do not process or redistribute an image until its source row has a known license status.

## 4. Metadata

Every accepted image should have:

- one row in `metadata/sources/dermnetnz_manifest.csv`
- one row in `metadata/standardized/core_metadata_template.csv` or a generated export table
- one normalized label from `annotations/labels/taxonomy.csv`

## 5. Quality checks

Minimum recommended checks:

- image opens without corruption
- image is dermatology-relevant
- no visible identifying information unless explicitly allowed and ethically reviewed
- duplicate images are detected and linked
- diagnosis label is traceable to source page or expert review

## 6. Splits

Create train/validation/test splits in `data/processed/splits/`. If patient or lesion identifiers exist, split by patient or lesion, not by image, to avoid leakage.
