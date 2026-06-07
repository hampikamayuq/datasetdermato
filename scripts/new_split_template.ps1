param(
    [string]$OutputPath = "data/processed/splits/split_template.csv"
)

$ErrorActionPreference = "Stop"

$directory = Split-Path -Parent $OutputPath
if ($directory -and -not (Test-Path -LiteralPath $directory)) {
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
}

$content = @"
image_id,filename,patient_id,lesion_id,diagnosis,split
example_0001,data/processed/images/example_0001.jpg,patient_0001,lesion_0001,unknown,train
"@

Set-Content -LiteralPath $OutputPath -Value $content -Encoding UTF8 -Force
Write-Output "Created split template: $OutputPath"
