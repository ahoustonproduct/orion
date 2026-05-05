param([switch]$NoPause)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Orion-Common.ps1")

$Step = "frontend rebuild"

try {
  Write-Host "Rebuilding Orion frontend..."
  $Step = "frontend dependencies"
  Ensure-OrionFrontendDependencies

  $Step = "frontend build"
  Invoke-OrionFrontendBuild -Force

  Write-Host ""
  Write-Host "Frontend rebuild complete. Restarting Orion..."

  $PowerShell = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
  $RestartScript = Join-Path $PSScriptRoot "Restart-Orion.ps1"
  $RestartArgs = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $RestartScript)
  if ($NoPause) {
    $RestartArgs += "-NoPause"
  }

  & $PowerShell @RestartArgs
  exit $LASTEXITCODE
}
catch {
  Write-Host ""
  Write-Host "Frontend rebuild failed."
  Write-Host ("Where: Rebuild-Orion-Frontend.ps1 - {0}" -f $Step)
  Write-Host "Error:"
  Write-Host $_.Exception.Message
  Write-Host ("Logs: {0}" -f $Script:LogDir)

  Wait-OrionClose -NoPause:$NoPause
  exit 1
}
