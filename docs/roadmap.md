# Roadmap

## Phase 1: Repository skeleton

- Create dataset structure
- Add project-standard metadata template inspired by ISIC conventions
- Add source catalog
- Add DermNetNZ manifest
- Add licensing and ethics notes
- Add validation scripts

## Phase 2: Source review

- Review DermNetNZ terms and attribution requirements
- Review each candidate dataset license
- Decide which sources can be redistributed and which are local-only
- Mark status in `metadata/sources/source_catalog.csv`

## Phase 3: Institutional case model

- Start from anatomic pathology records when available
- Link pathology report, case, patient hash, and image
- Contact professor and assistant archives before broad resident outreach
- Classify cases as bronze, silver, or gold
- Keep train/validation/test splits by patient

## Phase 4: Pilot ingestion

- Curate 3 to 5 DermNetNZ condition pages
- Add image/page rows to `metadata/sources/dermnetnz_manifest.csv`
- Create normalized labels
- Fill `metadata/dataset_manifest.csv`
- Run metadata validation

## Phase 5: Quality and labeling

- Detect duplicates
- Check image dimensions and corrupt files
- Remove images with visible identifiers
- Review label consistency
- Add clinician review status when available

## Phase 6: Dataset release

- Generate train/validation/test splits
- Produce dataset card
- Export metadata CSV
- Package only images with approved redistribution status
- Publish local-only restricted-source instructions separately
