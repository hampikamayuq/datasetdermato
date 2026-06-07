# Quality Audit Protocol

Quality auditing is mandatory before model training, public release, or controlled sharing.

## Audit Targets

Audit at least:

- corrupt images
- duplicate and near-duplicate images
- irrelevant images
- train/validation/test leakage
- inconsistent labels
- low-confidence diagnosis
- identifying information
- missing source provenance
- missing license or ethics status

## Duplicate and Leakage Audit

Minimum checks:

- exact hash duplicate using `sha256`
- perceptual duplicate or near-duplicate review
- same patient across multiple splits
- same lesion across multiple splits
- same pathology report across multiple splits
- same image resized or cropped into different splits

The default rule is patient-level splitting. A patient must never appear in more than one split.

## Label Audit

Track:

- original diagnosis
- normalized diagnosis
- reviewer diagnosis
- consensus diagnosis
- pathology diagnosis
- confirmation method
- evidence level

Flag cases where:

- clinical and pathology diagnoses conflict
- label is too broad for the task
- diagnosis is missing or ambiguous
- source page label is not traceable

## Image Quality Audit

Recommended statuses:

- `accepted`
- `corrupt`
- `duplicate`
- `near_duplicate`
- `low_quality`
- `not_dermatology`
- `contains_identifier`
- `license_restricted`
- `ethics_restricted`
- `label_uncertain`

## Audit Metadata

Use `metadata/audits/quality_audit.csv`.

Each row should identify:

- target entity
- audit type
- status
- severity
- reviewer
- date
- remediation action

## Release Gate

A dataset version can be released only when:

- all images have source provenance
- all images have access status
- train/validation/test leakage has been checked
- known duplicates are marked
- sensitive images are controlled or removed
- datasheet and dataset card are updated
