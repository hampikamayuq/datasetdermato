$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $repoRoot

try {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        $previousErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        $pythonVersion = & python --version 2>&1
        $pythonExitCode = $LASTEXITCODE
        $ErrorActionPreference = $previousErrorActionPreference

        if ($pythonExitCode -eq 0) {
            Write-Output "Python available: $pythonVersion"
            & python (Join-Path $PSScriptRoot "dataset_validate.py")
            if ($LASTEXITCODE -ne 0) {
                exit $LASTEXITCODE
            }
            exit 0
        } else {
            Write-Warning "Python command exists but did not run successfully. Falling back to PowerShell validators."
        }
    } else {
        Write-Warning "Python was not found. Falling back to PowerShell validators."
    }

    & (Join-Path $PSScriptRoot "validate_metadata.ps1")
    & (Join-Path $PSScriptRoot "validate_sources.ps1")
    & (Join-Path $PSScriptRoot "validate_relational_metadata.ps1")

    Write-Output "All dataset validations passed."
} finally {
    Pop-Location
}
