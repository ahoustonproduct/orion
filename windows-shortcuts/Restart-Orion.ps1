param([switch]$NoPause)

$ErrorActionPreference = "Stop"

$PowerShell = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$StopScript = Join-Path $PSScriptRoot "Stop-Orion.ps1"
$StartScript = Join-Path $PSScriptRoot "Start-Orion.ps1"

Write-Host "Restarting Orion..."
& $PowerShell -NoProfile -ExecutionPolicy Bypass -File $StopScript -NoPause
if ($LASTEXITCODE -ne 0) {
  if (-not $NoPause) {
    Read-Host "Press Enter to close" | Out-Null
  }
  exit $LASTEXITCODE
}

$StartArgs = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $StartScript)
if ($NoPause) {
  $StartArgs += "-NoPause"
}

& $PowerShell @StartArgs
exit $LASTEXITCODE
