[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][ValidateSet('Upload','Download')][string]$Direction,
  [Parameter(Mandatory=$true)][string]$Remote,
  [Parameter(Mandatory=$true)][string]$Package,
  [Parameter(Mandatory=$true)][string]$Python,
  [string]$Project = (Split-Path -Parent $PSScriptRoot)
)
$ErrorActionPreference = 'Stop'
if ($Remote -notmatch '^[A-Za-z0-9_-]+:.+') { throw 'Use a configured PRIVATE rclone remote and explicit folder, e.g. adprivate:AD-Oxygen/incoming/run1' }
$Tool = Join-Path $Project 'methods\corpus\transfer_library.py'
function Run-Rclone([string[]]$ArgList) {
  & rclone @ArgList
  if ($LASTEXITCODE -ne 0) { throw "rclone failed: exit $LASTEXITCODE" }
}
if ($Direction -eq 'Upload') {
  & $Python $Tool verify --package $Package
  if ($LASTEXITCODE -ne 0) { throw 'Local package validation failed.' }
  $Receipt = Get-Content -Raw ($Package + '.sha256.json') | ConvertFrom-Json
  $Name = Split-Path -Leaf $Package
  Run-Rclone -ArgList @('copyto',$Package,($Remote.TrimEnd('/') + '/' + $Name),'--immutable','--transfers','1','--checkers','2','--retries','3')
  Run-Rclone -ArgList @('copyto',($Package + '.sha256.json'),($Remote.TrimEnd('/') + '/' + $Name + '.sha256.json'),'--immutable')
  $ReadbackDir = Join-Path ([System.IO.Path]::GetTempPath()) ('ad-oxygen-readback-' + [guid]::NewGuid().ToString())
  New-Item -ItemType Directory $ReadbackDir | Out-Null
  $Readback = Join-Path $ReadbackDir $Name
  Run-Rclone -ArgList @('copyto',($Remote.TrimEnd('/') + '/' + $Name),$Readback,'--transfers','1','--checkers','2')
  & $Python $Tool verify --package $Readback --expected-sha256 $Receipt.package_sha256
  if ($LASTEXITCODE -ne 0) { throw 'Actual remote bytes failed SHA verification.' }
  Write-Output "Remote readback verified in $ReadbackDir. This verifies this machine; configure the Codex runtime remote separately and repeat there."
} else {
  $Name = Split-Path -Leaf $Package
  Run-Rclone -ArgList @('copyto',($Remote.TrimEnd('/') + '/' + $Name),$Package,'--immutable','--transfers','1')
  Run-Rclone -ArgList @('copyto',($Remote.TrimEnd('/') + '/' + $Name + '.sha256.json'),($Package + '.sha256.json'),'--immutable')
  $Receipt = Get-Content -Raw ($Package + '.sha256.json') | ConvertFrom-Json
  & $Python $Tool verify --package $Package --expected-sha256 $Receipt.package_sha256
  if ($LASTEXITCODE -ne 0) { throw 'Downloaded package validation failed.' }
}
