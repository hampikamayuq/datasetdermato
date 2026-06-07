param(
    [string]$MetadataPath = "metadata/standardized/core_metadata_template.csv"
)

$ErrorActionPreference = "Stop"

$requiredColumns = @(
    "filename",
    "image_type",
    "diagnosis"
)

$allowedImageTypes = @(
    "dermoscopic",
    "clinical: overview",
    "clinical: close-up",
    "surgical",
    "histopathology",
    "TBP tile: close-up",
    "TBP tile: overview"
)

$allowedBenignMalignant = @(
    "",
    "benign",
    "malignant",
    "indeterminate",
    "indeterminate/benign",
    "indeterminate/malignant"
)

$allowedDiagnosisConfirmTypes = @(
    "",
    "histopathology",
    "serial imaging showing no change",
    "single image expert consensus",
    "confocal microscopy with consensus dermoscopy",
    "single contributor clinical assessment"
)

if (-not (Test-Path -LiteralPath $MetadataPath)) {
    throw "Metadata file not found: $MetadataPath"
}

$rows = Import-Csv -LiteralPath $MetadataPath
$header = (Get-Content -LiteralPath $MetadataPath -TotalCount 1).Split(",")

foreach ($column in $requiredColumns) {
    if ($header -notcontains $column) {
        throw "Missing required column: $column"
    }
}

$errors = New-Object System.Collections.Generic.List[string]
$rowNumber = 1

foreach ($row in $rows) {
    $rowNumber += 1

    if ([string]::IsNullOrWhiteSpace($row.filename)) {
        $errors.Add("Row ${rowNumber}: filename is required")
    }

    if ([string]::IsNullOrWhiteSpace($row.image_type)) {
        $errors.Add("Row ${rowNumber}: image_type is required")
    } elseif ($allowedImageTypes -notcontains $row.image_type) {
        $errors.Add("Row ${rowNumber}: image_type '$($row.image_type)' is not allowed")
    }

    if ([string]::IsNullOrWhiteSpace($row.diagnosis)) {
        $errors.Add("Row ${rowNumber}: diagnosis is required")
    }

    if ($row.PSObject.Properties.Name -contains "benign_malignant") {
        if ($allowedBenignMalignant -notcontains $row.benign_malignant) {
            $errors.Add("Row ${rowNumber}: benign_malignant '$($row.benign_malignant)' is not allowed")
        }

        if ($row.diagnosis -eq "melanoma" -and $row.benign_malignant -and $row.benign_malignant -ne "malignant") {
            $errors.Add("Row ${rowNumber}: melanoma must have benign_malignant set to malignant")
        }

        if ($row.diagnosis -eq "nevus" -and $row.benign_malignant -and @("benign", "indeterminate/benign", "indeterminate") -notcontains $row.benign_malignant) {
            $errors.Add("Row ${rowNumber}: nevus must be benign, indeterminate/benign, or indeterminate")
        }
    }

    if ($row.PSObject.Properties.Name -contains "diagnosis_confirm_type") {
        if ($allowedDiagnosisConfirmTypes -notcontains $row.diagnosis_confirm_type) {
            $errors.Add("Row ${rowNumber}: diagnosis_confirm_type '$($row.diagnosis_confirm_type)' is not allowed")
        }

        if (($row.PSObject.Properties.Name -contains "benign_malignant") -and @("malignant", "indeterminate", "indeterminate/benign", "indeterminate/malignant") -contains $row.benign_malignant) {
            if ($row.diagnosis_confirm_type -and $row.diagnosis_confirm_type -ne "histopathology") {
                $errors.Add("Row ${rowNumber}: malignant or indeterminate cases should use histopathology confirmation")
            }
        }
    }

    if ($row.age -and ($row.age -notmatch "^\d+$" -or [int]$row.age -gt 120)) {
        $errors.Add("Row ${rowNumber}: age must be an integer between 0 and 120")
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "Metadata validation passed: $MetadataPath"
