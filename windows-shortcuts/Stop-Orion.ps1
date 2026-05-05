param([switch]$NoPause)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Orion-Common.ps1")

try {
  Write-Host "Stopping Orion..."
  Stop-OrionAllTrackedProcesses
  Start-Sleep -Milliseconds 750

  Write-Host ""
  Write-Host "Tracked Orion processes stopped."
  Show-OrionPortSummary
  Show-OrionLegacyServiceHint

  Wait-OrionClose -NoPause:$NoPause
  exit 0
}
catch {
  Write-Host ""
  Write-Host "Orion could not stop cleanly."
  Write-Host "Where: Stop-Orion.ps1"
  Write-Host "Error:"
  Write-Host $_.Exception.Message
  Write-Host ""
  Show-OrionPortSummary

  Wait-OrionClose -NoPause:$NoPause
  exit 1
}
