$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path $PSScriptRoot -Parent
$runtimeRoot = Join-Path (Split-Path $siteRoot -Parent) 'academicpages_runtime'
$rubyBin = Join-Path $runtimeRoot 'rubyinstaller-3.2.11-1-x64/bin'
$env:JEKYLL_ENV = 'production'
Push-Location $siteRoot
try {
    if (Test-Path (Join-Path $rubyBin 'ridk.cmd')) {
        $env:PATH = $rubyBin + ';' + $env:PATH
        $env:BUNDLE_PATH = Join-Path $runtimeRoot 'bundle_msys'
        & (Join-Path $rubyBin 'ridk.cmd') exec bundle exec jekyll build --strict_front_matter
    } else {
        & bundle exec jekyll build --strict_front_matter
    }
    $buildExitCode = $LASTEXITCODE
}
finally { Pop-Location }
exit $buildExitCode
