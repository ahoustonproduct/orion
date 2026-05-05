param([switch]$NoPause)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Orion-Common.ps1")

$Step = "initializing"
$BackendProcess = $null
$FrontendProcess = $null

try {
  Write-Host "Starting Orion..."

  $LanIp = Get-OrionLanIp
  $Origins = @(
    "http://localhost:$Script:FrontendPort",
    "http://127.0.0.1:$Script:FrontendPort"
  )
  if ($LanIp) {
    $Origins += "http://${LanIp}:$Script:FrontendPort"
  }

  $env:BACKEND_URL = $Script:BackendUrl
  $env:ALLOWED_ORIGINS = ($Origins -join ",")
  if ($LanIp) {
    $env:LAN_HOST = $LanIp
  }

  $Step = "stopping existing Orion processes"
  Stop-OrionAllTrackedProcesses
  Start-Sleep -Milliseconds 500

  $Step = "backend port check"
  Assert-OrionPortAvailable -Port $Script:BackendPort -ServiceName "backend"

  $Step = "frontend port check"
  Assert-OrionPortAvailable -Port $Script:FrontendPort -ServiceName "frontend"

  $Step = "backend environment"
  $Python = Ensure-OrionBackendEnvironment

  $BackendOut = Join-Path $Script:LogDir "backend.out.log"
  $BackendErr = Join-Path $Script:LogDir "backend.err.log"
  Remove-Item -Path $BackendOut, $BackendErr -Force -ErrorAction SilentlyContinue

  $Step = "backend startup"
  Write-Host "Starting backend on $Script:BackendUrl ..."
  $BackendProcess = Start-Process -FilePath $Python -ArgumentList @(
    "-m", "uvicorn", "main:app",
    "--host", "127.0.0.1",
    "--port", "$Script:BackendPort"
  ) -WorkingDirectory $Script:BackendDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput $BackendOut `
    -RedirectStandardError $BackendErr `
    -PassThru

  $Step = "backend health check"
  if (-not (Wait-OrionUrl -Url "$Script:BackendUrl/health" -Seconds 45)) {
    throw "Backend did not answer $Script:BackendUrl/health. Check $BackendErr."
  }

  $BackendPids = @($BackendProcess.Id)
  $BackendPids += @(Get-OrionPortOwners -Port $Script:BackendPort | Select-Object -ExpandProperty ProcessId)
  Write-OrionPids -Name "backend" -ProcessIds $BackendPids

  $Step = "frontend dependencies"
  Ensure-OrionFrontendDependencies

  $Step = "frontend build"
  Invoke-OrionFrontendBuild

  $Npm = Get-OrionNpm
  $FrontendOut = Join-Path $Script:LogDir "frontend.out.log"
  $FrontendErr = Join-Path $Script:LogDir "frontend.err.log"
  Remove-Item -Path $FrontendOut, $FrontendErr -Force -ErrorAction SilentlyContinue

  $Step = "frontend startup"
  Write-Host "Starting frontend on http://0.0.0.0:$Script:FrontendPort ..."
  $FrontendProcess = Start-Process -FilePath $Npm -ArgumentList @(
    "run", "start", "--",
    "-H", "0.0.0.0",
    "-p", "$Script:FrontendPort"
  ) -WorkingDirectory $Script:FrontendDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput $FrontendOut `
    -RedirectStandardError $FrontendErr `
    -PassThru

  $Step = "frontend health check"
  if (-not (Wait-OrionUrl -Url $Script:FrontendUrl -Seconds 45)) {
    throw "Frontend did not answer $Script:FrontendUrl. Check $FrontendErr."
  }

  $Step = "frontend API proxy health check"
  if (-not (Wait-OrionUrl -Url "$Script:FrontendUrl/api/health" -Seconds 45)) {
    throw "Frontend proxy did not answer $Script:FrontendUrl/api/health. Check $FrontendErr."
  }

  $FrontendPids = @($FrontendProcess.Id)
  $FrontendPids += @(Get-OrionPortOwners -Port $Script:FrontendPort | Select-Object -ExpandProperty ProcessId)
  Write-OrionPids -Name "frontend" -ProcessIds $FrontendPids

  Write-Host ""
  Write-Host "Orion is running."
  Write-Host ("Windows URL: http://localhost:{0}" -f $Script:FrontendPort)
  if ($LanIp) {
    Write-Host ("MacBook URL: http://{0}:{1}" -f $LanIp, $Script:FrontendPort)
  }
  else {
    Write-Host "MacBook URL: no private LAN IP was detected."
  }
  Write-Host ("Backend:     http://127.0.0.1:{0}/health" -f $Script:BackendPort)
  Write-Host ("Logs:        {0}" -f $Script:LogDir)
  Write-Host "Stop:        double-click 'Orion Stop'"

  Start-Process ("http://localhost:{0}/" -f $Script:FrontendPort)
  Wait-OrionClose -NoPause:$NoPause
  exit 0
}
catch {
  if ($FrontendProcess) {
    Stop-OrionProcessTree -ProcessId $FrontendProcess.Id
  }
  if ($BackendProcess) {
    Stop-OrionProcessTree -ProcessId $BackendProcess.Id
  }
  Stop-OrionAllTrackedProcesses

  Write-Host ""
  Write-Host "Orion could not start."
  Write-Host ("Where: Start-Orion.ps1 - {0}" -f $Step)
  Write-Host "Error:"
  Write-Host $_.Exception.Message
  Write-Host ""
  Show-OrionPortSummary
  Show-OrionLegacyServiceHint
  Write-Host ("Logs: {0}" -f $Script:LogDir)

  Wait-OrionClose -NoPause:$NoPause
  exit 1
}
