$ErrorActionPreference = "Stop"

function Ensure-Admin {
  $Identity = [Security.Principal.WindowsIdentity]::GetCurrent()
  $Principal = [Security.Principal.WindowsPrincipal]::new($Identity)
  if (-not $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -Verb RunAs -ArgumentList @(
      "-NoProfile",
      "-ExecutionPolicy",
      "Bypass",
      "-File",
      $PSCommandPath
    )
    exit
  }
}

function Wait-ForUrl([string]$Url, [int]$Seconds = 30) {
  $Deadline = (Get-Date).AddSeconds($Seconds)
  do {
    try {
      Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3 | Out-Null
      return $true
    }
    catch {
      Start-Sleep -Seconds 1
    }
  } while ((Get-Date) -lt $Deadline)

  return $false
}

Ensure-Admin

Write-Host "Restarting Orion services..."
Restart-Service orion-backend -Force
Restart-Service orion-frontend -Force

if (Wait-ForUrl "http://localhost:3000/api/health" 30) {
  Write-Host "Orion is running."
  Start-Process "http://localhost:3000/"
}
else {
  Write-Host "Services restarted, but the health check did not respond yet."
}

Read-Host "Press Enter to close"
