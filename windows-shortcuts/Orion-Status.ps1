param([switch]$NoPause)

$ErrorActionPreference = "Continue"
. (Join-Path $PSScriptRoot "Orion-Common.ps1")

$LanIp = Get-OrionLanIp

Write-Host "Orion status"
Write-Host ("Workspace: {0}" -f $Script:OrionRoot)
Write-Host ("Windows URL: http://localhost:{0}" -f $Script:FrontendPort)
if ($LanIp) {
  Write-Host ("MacBook URL: http://{0}:{1}" -f $LanIp, $Script:FrontendPort)
}
else {
  Write-Host "MacBook URL: no private LAN IP was detected."
}

Write-Host ""
Write-Host "Ports"
Show-OrionPortSummary

Write-Host ""
Write-Host "Tracked PID files"
foreach ($Name in @("backend", "frontend")) {
  $Pids = @(Read-OrionPids -Name $Name)
  if ($Pids.Count -eq 0) {
    Write-Host ("{0}: none" -f $Name)
  }
  else {
    Write-Host ("{0}: {1}" -f $Name, ($Pids -join ", "))
  }
}

Write-Host ""
Write-Host "Backend health"
try {
  Invoke-RestMethod -Uri "$Script:BackendUrl/health" -TimeoutSec 5 | Format-List
}
catch {
  Write-Host ("Backend health failed: {0}" -f $_.Exception.Message)
}

Write-Host ""
Write-Host "Frontend proxy health"
try {
  Invoke-RestMethod -Uri "$Script:FrontendUrl/api/health" -TimeoutSec 5 | Format-List
}
catch {
  Write-Host ("Frontend proxy health failed: {0}" -f $_.Exception.Message)
}

Write-Host ""
Write-Host "Legacy Windows services"
$Services = @(Get-Service -Name orion-backend, orion-frontend -ErrorAction SilentlyContinue)
if ($Services.Count -eq 0) {
  Write-Host "None found."
}
else {
  $Services | Select-Object Name, Status, StartType | Format-Table -AutoSize
}

Write-Host ""
Write-Host ("Logs: {0}" -f $Script:LogDir)
Wait-OrionClose -NoPause:$NoPause
