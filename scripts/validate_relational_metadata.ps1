param(
    [string]$MetadataDirectory = "metadata/relational"
)

$ErrorActionPreference = "Stop"

$files = @{
    "patients.csv" = @("patient_id", "patient_hash")
    "cases.csv" = @("case_id", "patient_id", "source_type", "specialty_service", "evidence_level")
    "images.csv" = @("image_id", "case_id", "image_type", "file_path")
    "surgical_procedures.csv" = @("procedure_id", "case_id")
    "pathology_reports.csv" = @("report_id", "case_id")
    "expert_reviews.csv" = @("review_id", "case_id")
    "clinical_followups.csv" = @("followup_id", "case_id")
    "annotations.csv" = @("annotation_id", "image_id", "annotation_type")
    "consents_ethics.csv" = @("ethics_id")
    "dataset_splits.csv" = @("split_id", "patient_id", "split")
}

foreach ($entry in $files.GetEnumerator()) {
    $path = Join-Path $MetadataDirectory $entry.Key
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing relational metadata file: $path"
    }

    $header = (Get-Content -LiteralPath $path -TotalCount 1).Split(",")
    foreach ($column in $entry.Value) {
        if ($header -notcontains $column) {
            throw "Missing column '$column' in $path"
        }
    }
}

$splitRows = Import-Csv -LiteralPath (Join-Path $MetadataDirectory "dataset_splits.csv")
$patientSplits = @{}

foreach ($row in $splitRows) {
    if (-not $row.patient_id) {
        continue
    }

    if ($patientSplits.ContainsKey($row.patient_id) -and $patientSplits[$row.patient_id] -ne $row.split) {
        throw "Patient $($row.patient_id) appears in more than one split"
    }

    $patientSplits[$row.patient_id] = $row.split
}

Write-Output "Relational metadata validation passed"
