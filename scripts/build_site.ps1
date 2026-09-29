$rubyBin = 'D:\Projects\100_Extras\HS\academicpages_runtime\rubyinstaller-3.2.11-1-x64\bin'
$env:PATH = $rubyBin + ';' + $env:PATH
$env:BUNDLE_PATH = 'D:\Projects\100_Extras\HS\academicpages_runtime\bundle_msys'
$env:JEKYLL_ENV = 'production'
& (Join-Path $rubyBin 'ridk.cmd') exec bundle exec jekyll build --strict_front_matter
