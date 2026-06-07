$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $repoRoot

try {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        throw "Python was not found. Install Python 3.10+ and try again."
    }

    & python --version | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Python command exists but did not run successfully. Install Python 3.10+ and try again."
    }

    & python -m streamlit run scripts/dataset_app.py
} finally {
    Pop-Location
}
