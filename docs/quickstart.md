# Quickstart

This is the shortest safe path to use the repository.

## 1. Install dependencies

macOS/Linux:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Validate the repository

From the repository root:

```bash
python scripts/dataset_validate.py
```

macOS/Linux can also use:

```bash
sh scripts/validate_all.sh
make validate
```

On Windows, this command keeps a PowerShell fallback:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate_all.ps1
```

## 3. Review source and ethics status

Before adding images:

- register the source in `metadata/sources/source_catalog.csv`
- confirm license or access status
- confirm ethics and governance status
- decide whether the image can be public, controlled-access, or internal-only

## 4. Register an image by command line

Python and dependencies are required:

```bash
python scripts/register_image.py image.jpg --source-id dermnetnz --image-type "clinical: close-up" --diagnosis melanoma
```

Optional context:

```bash
python scripts/register_image.py image.jpg \
  --source-id institutional_archive \
  --source-type clinical_archive \
  --specialty-service oncologic_dermatology \
  --image-type "clinical: close-up" \
  --diagnosis "basal cell carcinoma" \
  --patient-id P001 \
  --lesion-id L001
```

The script:

- removes EXIF
- writes the processed image to `data/processed/images/`
- checks duplicate SHA256 after preprocessing
- appends rows to `metadata/dataset_manifest.csv`
- appends rows to `metadata/standardized/core_metadata_template.csv`

## 5. Use the visual curation app

macOS/Linux:

```bash
sh scripts/run_app.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_app.ps1
```

Any system with Python:

```bash
python -m streamlit run scripts/dataset_app.py
```

Or on macOS/Linux:

```bash
make app
```

## 6. Audit before release

Before any dataset release:

- complete `docs/datasheet_for_dataset.md`
- update `docs/dataset_card.md`
- fill `metadata/audits/quality_audit.csv`
- fill `metadata/audits/fairness_summary_template.csv`
- confirm patient-level train/validation/test splits
