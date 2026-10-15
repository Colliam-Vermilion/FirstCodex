[CmdletBinding()]
param(
  [ValidateSet('Setup','Download','ExtractNew','ExtractExisting','ExportReturn','VerifyPackage','Hydrate','MergeReturn','Search')]
  [string]$Action = 'Setup',
  [string]$LibraryRoot = 'D:\AD-Library',
  [string]$Project = (Split-Path -Parent $PSScriptRoot),
  [string]$Queue = '', [string]$Package = '', [string]$ExpectedSha256 = '',
  [string]$Query = '', [switch]$RetryFailed, [switch]$Ocr
)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:OMP_THREAD_LIMIT = '1'
$Tools = Join-Path $Project 'methods\corpus'
$Python = Join-Path $LibraryRoot '.venv\Scripts\python.exe'
function Run-Python([string[]]$ArgList) {
  & $Python @ArgList
  if ($LASTEXITCODE -ne 0) { throw "Python command failed: exit $LASTEXITCODE" }
}
if ($Action -eq 'Setup') {
  New-Item -ItemType Directory -Force -Path $LibraryRoot | Out-Null
  if (-not (Test-Path $Python)) {
    & py -3 -m venv (Join-Path $LibraryRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.11 or newer and the Windows py launcher.' }
  }
  Run-Python -ArgList @('-m','pip','install','-r',(Join-Path $Tools 'requirements.txt'))
  Run-Python -ArgList @('-m','pip','check')
  Write-Output 'Setup complete. Tesseract OCR is optional and must be installed separately on PATH.'
  exit
}
if (-not (Test-Path $Python)) { throw 'Run -Action Setup first.' }
$Download = Join-Path $Tools 'download_local.py'
$Extract = Join-Path $Tools 'extract_search.py'
$Transfer = Join-Path $Tools 'transfer_library.py'
switch ($Action) {
  'Download' {
    if (-not $Queue) { $Queue = Join-Path $Project 'windows\known_pdf_urls_current_utf8.csv' }
    $A = @($Download,'--project',$Project,'--root',$LibraryRoot,'download','--queue',$Queue,'--delay','6')
    if ($RetryFailed) { $A += '--retry-failed' }
    Run-Python -ArgList $A
  }
  'ExtractNew' {
    $A = @($Extract,'extract','--project',$Project,'--root',$LibraryRoot,'--assets',(Join-Path $LibraryRoot 'intake\assets.json'),'--workers','2')
    if ($Ocr) { $A += '--ocr' }
    Run-Python -ArgList $A
  }
  'ExtractExisting' {
    $A = @($Extract,'extract','--project',$Project,'--root',$LibraryRoot,'--workers','2')
    if ($Ocr) { $A += '--ocr' }
    Run-Python -ArgList $A
  }
  'ExportReturn' {
    if (-not $Package) { $Package = Join-Path $LibraryRoot 'ad-oxygen-return.zip' }
    Run-Python -ArgList @($Transfer,'--project',$Project,'prepare-return','--root',$LibraryRoot,'--out',$Package)
  }
  'VerifyPackage' {
    if (-not $Package) { throw '-Package is required.' }
    $A = @($Transfer,'verify','--package',$Package)
    if ($ExpectedSha256) { $A += @('--expected-sha256',$ExpectedSha256) }
    Run-Python -ArgList $A
  }
  'Hydrate' {
    if (-not $Package) { throw '-Package is required.' }
    $A = @($Transfer,'hydrate','--package',$Package,'--root',$LibraryRoot)
    if ($ExpectedSha256) { $A += @('--expected-sha256',$ExpectedSha256) }
    Run-Python -ArgList $A
  }
  'MergeReturn' { Run-Python -ArgList @($Transfer,'--project',$Project,'merge-return','--root',$LibraryRoot) }
  'Search' {
    if (-not $Query) { throw '-Query is required.' }
    Run-Python -ArgList @($Extract,'search','--root',$LibraryRoot,'--query',$Query,'--limit','20')
  }
}
