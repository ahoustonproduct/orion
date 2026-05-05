param([switch]$NoPause)

$ErrorActionPreference = "Continue"

function Test-OrionAdmin {
  $Identity = [Security.Principal.WindowsIdentity]::GetCurrent()
  $Principal = [Security.Principal.WindowsPrincipal]::new($Identity)
  return $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-OrionAdmin)) {
  $Arguments = @(
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    "`"$PSCommandPath`""
  )
  if ($NoPause) {
    $Arguments += "-NoPause"
  }

  Start-Process powershell.exe -Verb RunAs -ArgumentList $Arguments
  exit
}

Write-Host "Removing old Orion Windows services..."

foreach ($ServiceName in @("orion-frontend", "orion-backend")) {
  $Service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
  if (-not $Service) {
    Write-Host ("{0}: not installed" -f $ServiceName)
    continue
  }

  if ($Service.Status -ne "Stopped") {
    Write-Host ("{0}: stopping" -f $ServiceName)
    Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
  }

  Write-Host ("{0}: deleting" -f $ServiceName)
  sc.exe delete $ServiceName | Out-Host
}

Write-Host ""
Write-Host "Old service cleanup is complete."
Write-Host "Next: double-click 'Orion Start'."

if (-not $NoPause) {
  Read-Host "Press Enter to close" | Out-Null
}
