$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $repoRoot

try {
    & (Join-Path $PSScriptRoot "validate_metadata.ps1")
    & (Join-Path $PSScriptRoot "validate_sources.ps1")
    & (Join-Path $PSScriptRoot "validate_relational_metadata.ps1")

    Write-Output "All dataset validations passed."

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        $previousErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        $pythonVersion = & python --version 2>&1
        $pythonExitCode = $LASTEXITCODE
        $ErrorActionPreference = $previousErrorActionPreference

        if ($pythonExitCode -eq 0) {
            Write-Output "Python available: $pythonVersion"
        } else {
            Write-Warning "Python command exists but did not run successfully. CLI/UI image registration requires Python with requirements.txt installed."
        }
    } else {
        Write-Warning "Python was not found. CLI/UI image registration requires Python with requirements.txt installed."
    }
} finally {
    Pop-Location
}
