# Metadata Fields

## Central manifest

`metadata/dataset_manifest.csv` is the project-level table. It links images, source provenance, labels, review state, and split assignment.

Important fields:

- `image_id`: stable project identifier
- `filename`: local image path
- `source_id`: source catalog identifier
- `source_image_url`: original image URL
- `source_page_url`: source page URL
- `source_license_status`: permission status at image level
- `sha256`: image hash for duplicate detection
- `image_type`: project-standard image type inspired by common dermatology dataset conventions
- `diagnosis_original`: source label as written
- `diagnosis_normalized`: normalized clinical name
- `label_id`: machine-friendly label from taxonomy
- `split`: train, validation, test, or empty
- `quality_status`: image quality/rejection status
- `review_status`: curation/review status

## Core standardized metadata

`metadata/standardized/core_metadata_template.csv` keeps the project field order for image-level metadata:

```text
filename,image_type,dermoscopic_type,tbp_tile_type,age,sex,anatom_site_general,anatom_site_special,fitzpatrick_skin_type,acquisition_day,personal_hx_mm,family_hx_mm,lesion_id,patient_id,rcm_case_id,clin_size_long_diam_mm,diagnosis,benign_malignant,concomitant_biopsy,diagnosis_confirm_type,melanocytic,nevus_type,mel_thick_mm,mel_class,mel_type,mel_mitotic_index,mel_ulcer
```

Use this file for the project's internal standardized image metadata. Separate export files can be generated later if a strict external format is needed.

## ISIC-inspired behavior notes

Based on the ISIC Archive image metadata wiki, these are useful design ideas rather than strict project requirements:

- Unknown or project-specific fields should be preserved, even when they are not part of an external standard.
- `image_type` includes `dermoscopic`, `clinical: close-up`, `clinical: overview`, `TBP tile: close-up`, and `TBP tile: overview`.
- Dermoscopic images may use `dermoscopic_type`.
- TBP tile images may use `tbp_tile_type`.
- Public exports should clip or group age and avoid exposing raw identifiers.
- `patient_id` and `lesion_id` should be mapped or hashed rather than exposing original institutional identifiers.
- `benign_malignant` interacts with `diagnosis`; for example, melanoma must be malignant and nevus should be benign or indeterminate variants.
- Indeterminate or malignant cases should be confirmed by histopathology.
