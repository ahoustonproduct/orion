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

Ensure-Admin

Write-Host "Stopping Orion services..."
Stop-Service orion-frontend -ErrorAction SilentlyContinue
Stop-Service orion-backend -ErrorAction SilentlyContinue
Write-Host "Orion services stopped."

Read-Host "Press Enter to close"
