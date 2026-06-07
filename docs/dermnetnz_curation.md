# DermNetNZ Curation Guide

## Scope

DermNetNZ can be useful for educational dermatology image discovery, disease taxonomy, and source-page traceability. Treat it as a curated source candidate, not as an automatically redistributable image pool.

## Per-page workflow

1. Choose a condition page.
2. Record the page URL in `metadata/sources/dermnetnz_manifest.csv`.
3. Record the source condition name exactly as written on the page.
4. Assign a normalized label from `annotations/labels/taxonomy.csv`.
5. Record each candidate image URL.
6. Mark `license_status` as `pending` until terms are reviewed.
7. Record attribution text if shown near the image or page.
8. Save access date in ISO format, for example `2026-06-07`.

## Recommended identifiers

Use deterministic IDs:

```text
dermnetnz_<condition_slug>_<sequence>
```

Examples:

```text
dermnetnz_psoriasis_0001
dermnetnz_acne_vulgaris_0001
dermnetnz_melanoma_0001
```

## Label normalization

Keep three levels:

- `condition_original`: exact source text
- `condition_normalized`: project-level disease name
- `label_id`: stable machine-friendly label

## Image quality flags

Use these statuses in `dataset_manifest.csv`:

- `pending_review`
- `accepted`
- `duplicate`
- `low_quality`
- `not_dermatology`
- `contains_identifier`
- `license_restricted`

## Review status

Use these statuses:

- `unreviewed`
- `source_reviewed`
- `label_reviewed`
- `clinician_reviewed`
- `excluded`
