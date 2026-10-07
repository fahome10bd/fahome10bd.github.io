$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path $PSScriptRoot -Parent
Push-Location $siteRoot
try {
    python (Join-Path $PSScriptRoot 'import_documents.py') @args
    if ($LASTEXITCODE -ne 0) { throw 'Word import failed. The website content was not updated.' }
    python (Join-Path $PSScriptRoot 'build_cv.py')
    if ($LASTEXITCODE -ne 0) { throw 'CV build failed.' }
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'build_site.ps1')
    if ($LASTEXITCODE -ne 0) { throw 'Website build failed.' }
    python (Join-Path $PSScriptRoot 'verify_site.py')
    if ($LASTEXITCODE -ne 0) { throw 'Website verification failed.' }
    Write-Host 'Ready. Start scripts/start_editor.ps1 and open http://127.0.0.1:8765/preview/ to review.'
}
finally { Pop-Location }
