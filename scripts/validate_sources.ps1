param(
    [string]$SourceCatalogPath = "metadata/sources/source_catalog.csv",
    [string]$DermnetnzManifestPath = "metadata/sources/dermnetnz_manifest.csv"
)

$ErrorActionPreference = "Stop"

function Assert-Columns {
    param(
        [string]$Path,
        [string[]]$Columns
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "File not found: $Path"
    }

    $header = (Get-Content -LiteralPath $Path -TotalCount 1).Split(",")
    foreach ($column in $Columns) {
        if ($header -notcontains $column) {
            throw "Missing column '$column' in $Path"
        }
    }
}

Assert-Columns -Path $SourceCatalogPath -Columns @(
    "source_id",
    "source_name",
    "homepage_url",
    "redistribution_status",
    "license_or_terms_url"
)

Assert-Columns -Path $DermnetnzManifestPath -Columns @(
    "image_id",
    "source_id",
    "page_url",
    "image_url",
    "condition_original",
    "condition_normalized",
    "license_status",
    "attribution",
    "accessed_at"
)

$allowedLicenseStatuses = @(
    "",
    "pending",
    "approved",
    "restricted",
    "rejected"
)

$errors = New-Object System.Collections.Generic.List[string]
$rowNumber = 1
$manifestRows = Import-Csv -LiteralPath $DermnetnzManifestPath

foreach ($row in $manifestRows) {
    $rowNumber += 1

    if ($row.source_id -and $row.source_id -ne "dermnetnz") {
        $errors.Add("Row ${rowNumber}: source_id should be dermnetnz")
    }

    if ($row.license_status -and ($allowedLicenseStatuses -notcontains $row.license_status)) {
        $errors.Add("Row ${rowNumber}: license_status '$($row.license_status)' is not allowed")
    }

    if ($row.page_url -and ($row.page_url -notmatch "^https://")) {
        $errors.Add("Row ${rowNumber}: page_url should be an https URL")
    }

    if ($row.image_url -and ($row.image_url -notmatch "^https://")) {
        $errors.Add("Row ${rowNumber}: image_url should be an https URL")
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "Source validation passed"
