# Quickstart

This is the shortest safe path to use the repository.

## 1. Validate the repository

From the repository root:

```powershell
python scripts/dataset_validate.py
```

On Windows, this command keeps a PowerShell fallback:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate_all.ps1
```

## 2. Review source and ethics status

Before adding images:

- register the source in `metadata/sources/source_catalog.csv`
- confirm license or access status
- confirm ethics and governance status
- decide whether the image can be public, controlled-access, or internal-only

## 3. Register an image by command line

Python and dependencies are required:

```powershell
python -m pip install -r requirements.txt
python scripts/register_image.py image.jpg --source-id dermnetnz --image-type "clinical: close-up" --diagnosis melanoma
```

Optional context:

```powershell
python scripts/register_image.py image.jpg `
  --source-id institutional_archive `
  --source-type clinical_archive `
  --specialty-service oncologic_dermatology `
  --image-type "clinical: close-up" `
  --diagnosis "basal cell carcinoma" `
  --patient-id P001 `
  --lesion-id L001
```

The script:

- removes EXIF
- writes the processed image to `data/processed/images/`
- checks duplicate SHA256 after preprocessing
- appends rows to `metadata/dataset_manifest.csv`
- appends rows to `metadata/standardized/core_metadata_template.csv`

## 4. Use the visual curation app

```powershell
streamlit run scripts/dataset_app.py
```

## 5. Audit before release

Before any dataset release:

- complete `docs/datasheet_for_dataset.md`
- update `docs/dataset_card.md`
- fill `metadata/audits/quality_audit.csv`
- fill `metadata/audits/fairness_summary_template.csv`
- confirm patient-level train/validation/test splits
