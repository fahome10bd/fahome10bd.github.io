$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path $PSScriptRoot -Parent
Push-Location $siteRoot
try {
    python (Join-Path $PSScriptRoot 'local_editor.py') @args
    if ($LASTEXITCODE -ne 0) { throw 'The local editor stopped with an error.' }
}
finally { Pop-Location }
