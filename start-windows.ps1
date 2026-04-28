$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $Root "backend"
$FrontendDir = Join-Path $Root "frontend"

$BackendPort = if ($env:BACKEND_PORT) { $env:BACKEND_PORT } else { "8000" }
$FrontendPort = if ($env:FRONTEND_PORT) { $env:FRONTEND_PORT } else { "3000" }

$env:ORION_AI_ENABLED = if ($env:ORION_AI_ENABLED) { $env:ORION_AI_ENABLED } else { "false" }
$env:BACKEND_URL = if ($env:BACKEND_URL) { $env:BACKEND_URL } else { "http://localhost:$BackendPort" }

$LanIp = Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object {
    $_.IPAddress -ne "127.0.0.1" -and
    $_.IPAddress -notlike "169.254*" -and
    $_.PrefixOrigin -ne "WellKnown"
  } |
  Select-Object -First 1 -ExpandProperty IPAddress

$DefaultOrigins = "http://localhost:$FrontendPort,http://127.0.0.1:$FrontendPort"
if ($LanIp) {
  $DefaultOrigins = "$DefaultOrigins,http://${LanIp}:$FrontendPort"
}
$env:ALLOWED_ORIGINS = if ($env:ALLOWED_ORIGINS) { $env:ALLOWED_ORIGINS } else { $DefaultOrigins }
$env:LAN_HOST = if ($env:LAN_HOST) { $env:LAN_HOST } else { $LanIp }

function Stop-ProcessOnPort([string]$Port) {
  $Listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique

  foreach ($Pid in @($Listeners)) {
    if ($Pid) {
      Stop-Process -Id $Pid -Force -ErrorAction SilentlyContinue
    }
  }
}

function Stop-ProcessesMatchingPath([string]$PathFragment) {
  if (-not $PathFragment) {
    return
  }

  $Escaped = [Regex]::Escape($PathFragment)
  $Matches = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -and $_.CommandLine -match $Escaped }

  foreach ($Match in @($Matches)) {
    Stop-Process -Id $Match.ProcessId -Force -ErrorAction SilentlyContinue
  }
}

Write-Host "[1/4] Preparing backend..."
Set-Location $BackendDir
if (-not (Test-Path "venv")) {
  $PyLauncher = Get-Command py -ErrorAction SilentlyContinue
  if ($PyLauncher) {
    & $PyLauncher.Source -3 -m venv venv
  }
  else {
    python -m venv venv
  }
}
$Python = Join-Path $BackendDir "venv\Scripts\python.exe"
& $Python -m pip install -r requirements.txt --quiet

Stop-ProcessesMatchingPath $BackendDir
Stop-ProcessesMatchingPath $FrontendDir
Stop-ProcessOnPort $BackendPort
Stop-ProcessOnPort $FrontendPort

Write-Host "[2/4] Starting backend on http://0.0.0.0:$BackendPort ..."
$Backend = Start-Process -FilePath $Python -ArgumentList @(
  "-m", "uvicorn", "main:app",
  "--host", "0.0.0.0",
  "--port", $BackendPort,
  "--reload"
) -WorkingDirectory $BackendDir -PassThru

Start-Sleep -Seconds 3

Write-Host "[3/4] Building frontend..."
Set-Location $FrontendDir
$NpmCommand = Get-Command npm.cmd -ErrorAction SilentlyContinue
if (-not $NpmCommand) {
  $NpmCommand = Get-Command npm -ErrorAction Stop
}
if (-not (Test-Path "node_modules")) {
  & $NpmCommand.Source install
}
& $NpmCommand.Source run build

Write-Host "[4/4] Starting frontend on http://0.0.0.0:$FrontendPort ..."
$Frontend = Start-Process -FilePath $NpmCommand.Source -ArgumentList @(
  "run", "start", "--",
  "-H", "0.0.0.0",
  "-p", $FrontendPort
) -WorkingDirectory $FrontendDir -PassThru

Write-Host ""
Write-Host "Orion is running on the Windows PC."
Write-Host "Frontend: http://localhost:$FrontendPort"
if ($LanIp) {
  Write-Host "Network:  http://${LanIp}:$FrontendPort"
}
Write-Host "Backend:  http://localhost:$BackendPort"
Write-Host "AI:       optional, ORION_AI_ENABLED=$($env:ORION_AI_ENABLED)"
Write-Host ""
Write-Host "Press Ctrl+C in this window to stop the app processes."

try {
  Wait-Process -Id $Backend.Id, $Frontend.Id
}
finally {
  foreach ($Process in @($Backend, $Frontend)) {
    if ($Process -and -not $Process.HasExited) {
      taskkill /PID $Process.Id /T /F | Out-Null
    }
  }
}
