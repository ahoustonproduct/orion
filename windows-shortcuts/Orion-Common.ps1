$Script:OrionRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Script:BackendDir = Join-Path $Script:OrionRoot "backend"
$Script:FrontendDir = Join-Path $Script:OrionRoot "frontend"
$Script:LogDir = Join-Path $Script:OrionRoot ".codex-run-logs"
$Script:PidDir = Join-Path $Script:LogDir "pids"
$Script:BackendPort = 8000
$Script:FrontendPort = 3000
$Script:BackendUrl = "http://127.0.0.1:$Script:BackendPort"
$Script:FrontendUrl = "http://127.0.0.1:$Script:FrontendPort"

New-Item -ItemType Directory -Force -Path $Script:LogDir, $Script:PidDir | Out-Null

function Get-OrionLanIp {
  $Address = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object {
      $_.IPAddress -ne "127.0.0.1" -and
      $_.IPAddress -notlike "169.254*" -and
      $_.PrefixOrigin -ne "WellKnown"
    } |
    Select-Object -First 1 -ExpandProperty IPAddress

  return $Address
}

function Get-OrionNpm {
  $Command = Get-Command npm.cmd -ErrorAction SilentlyContinue
  if (-not $Command) {
    $Command = Get-Command npm -ErrorAction Stop
  }

  return $Command.Source
}

function Get-OrionSystemPython {
  $Py = Get-Command py -ErrorAction SilentlyContinue
  if ($Py) {
    return @{ FilePath = $Py.Source; Arguments = @("-3") }
  }

  $Python = Get-Command python -ErrorAction Stop
  return @{ FilePath = $Python.Source; Arguments = @() }
}

function Get-OrionPython {
  foreach ($VenvName in @(".venv", "venv")) {
    $Candidate = Join-Path $Script:BackendDir "$VenvName\Scripts\python.exe"
    if (Test-Path $Candidate) {
      return $Candidate
    }
  }

  return $null
}

function Ensure-OrionBackendEnvironment {
  $Python = Get-OrionPython

  if (-not $Python) {
    $SystemPython = Get-OrionSystemPython
    $VenvPath = Join-Path $Script:BackendDir "venv"
    Write-Host "Creating backend virtual environment..."
    & $SystemPython["FilePath"] @($SystemPython["Arguments"] + @("-m", "venv", $VenvPath))
    if ($LASTEXITCODE -ne 0) {
      throw "Python could not create backend\venv."
    }
    $Python = Join-Path $Script:BackendDir "venv\Scripts\python.exe"
  }

  $Requirements = Join-Path $Script:BackendDir "requirements.txt"
  $Stamp = Join-Path $Script:LogDir "backend-requirements.stamp"
  $NeedsInstall = -not (Test-Path $Stamp)

  if (-not $NeedsInstall -and (Test-Path $Requirements)) {
    $NeedsInstall = (Get-Item $Requirements).LastWriteTimeUtc -gt (Get-Item $Stamp).LastWriteTimeUtc
  }

  if ($NeedsInstall) {
    Write-Host "Installing backend dependencies..."
    & $Python -m pip install -r $Requirements --quiet
    if ($LASTEXITCODE -ne 0) {
      throw "Backend dependency install failed in backend\requirements.txt."
    }
    Set-Content -Path $Stamp -Value (Get-Date).ToString("o") -Encoding ASCII
  }

  return $Python
}

function Ensure-OrionFrontendDependencies {
  $Npm = Get-OrionNpm
  $NodeModules = Join-Path $Script:FrontendDir "node_modules"
  $PackageLock = Join-Path $Script:FrontendDir "package-lock.json"
  $PackageJson = Join-Path $Script:FrontendDir "package.json"
  $Stamp = Join-Path $Script:LogDir "frontend-npm-install.stamp"
  $NeedsInstall = -not (Test-Path $NodeModules) -or -not (Test-Path $Stamp)

  if (-not $NeedsInstall) {
    foreach ($Manifest in @($PackageJson, $PackageLock)) {
      if ((Test-Path $Manifest) -and (Get-Item $Manifest).LastWriteTimeUtc -gt (Get-Item $Stamp).LastWriteTimeUtc) {
        $NeedsInstall = $true
      }
    }
  }

  if ($NeedsInstall) {
    Write-Host "Installing frontend dependencies..."
    & $Npm --prefix $Script:FrontendDir install
    if ($LASTEXITCODE -ne 0) {
      throw "Frontend dependency install failed in frontend\package.json."
    }
    Set-Content -Path $Stamp -Value (Get-Date).ToString("o") -Encoding ASCII
  }
}

function Get-OrionNewestFrontendSourceTime {
  $Paths = @(
    "app",
    "components",
    "lib",
    "public",
    "next.config.ts",
    "package.json",
    "package-lock.json",
    "postcss.config.mjs",
    "tailwind.config.ts",
    "tsconfig.json"
  )

  $Newest = [DateTime]::MinValue
  foreach ($Path in $Paths) {
    $FullPath = Join-Path $Script:FrontendDir $Path
    if (-not (Test-Path $FullPath)) {
      continue
    }

    $Item = Get-Item $FullPath
    if ($Item.PSIsContainer) {
      $Files = Get-ChildItem -Path $FullPath -Recurse -File -ErrorAction SilentlyContinue
      foreach ($File in $Files) {
        if ($File.FullName -match "\\node_modules\\" -or $File.FullName -match "\\.next\\") {
          continue
        }
        if ($File.LastWriteTimeUtc -gt $Newest) {
          $Newest = $File.LastWriteTimeUtc
        }
      }
    }
    elseif ($Item.LastWriteTimeUtc -gt $Newest) {
      $Newest = $Item.LastWriteTimeUtc
    }
  }

  return $Newest
}

function Test-OrionFrontendBuildFresh {
  $BuildId = Join-Path $Script:FrontendDir ".next\BUILD_ID"
  if (-not (Test-Path $BuildId)) {
    return $false
  }

  $BuildTime = (Get-Item $BuildId).LastWriteTimeUtc
  $SourceTime = Get-OrionNewestFrontendSourceTime
  return $SourceTime -le $BuildTime
}

function Invoke-OrionFrontendBuild {
  param([switch]$Force)

  if (-not $Force -and (Test-OrionFrontendBuildFresh)) {
    Write-Host "Frontend build is current."
    return
  }

  $Npm = Get-OrionNpm
  Write-Host "Building frontend for production..."
  & $Npm --prefix $Script:FrontendDir run build
  if ($LASTEXITCODE -ne 0) {
    throw "Frontend build failed in frontend."
  }
}

function Wait-OrionUrl {
  param(
    [string]$Url,
    [int]$Seconds = 30
  )

  $Deadline = (Get-Date).AddSeconds($Seconds)
  do {
    try {
      $Response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
      if ($Response.StatusCode -ge 200 -and $Response.StatusCode -lt 500) {
        return $true
      }
    }
    catch {
      Start-Sleep -Milliseconds 750
    }
  } while ((Get-Date) -lt $Deadline)

  return $false
}

function Get-OrionPortOwners {
  param([int]$Port)

  $Connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
  $Owners = @()
  foreach ($Connection in @($Connections)) {
    $ProcessId = [int]$Connection.OwningProcess
    $ProcessInfo = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction SilentlyContinue
    $Name = "unknown"
    $CommandLine = ""

    if ($ProcessInfo) {
      $Name = $ProcessInfo.Name
      $CommandLine = $ProcessInfo.CommandLine
    }
    else {
      $Process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
      if ($Process) {
        $Name = $Process.ProcessName
      }
    }

    $Owners += [PSCustomObject]@{
      Port = $Port
      ProcessId = $ProcessId
      Name = $Name
      CommandLine = $CommandLine
    }
  }

  return $Owners
}

function Get-OrionPidFile {
  param([string]$Name)
  return (Join-Path $Script:PidDir "$Name.pid")
}

function Read-OrionPids {
  param([string]$Name)

  $Path = Get-OrionPidFile -Name $Name
  if (-not (Test-Path $Path)) {
    return @()
  }

  return @(Get-Content -Path $Path -ErrorAction SilentlyContinue |
    Where-Object { $_ -match "^\d+$" } |
    ForEach-Object { [int]$_ })
}

function Write-OrionPids {
  param(
    [string]$Name,
    [int[]]$ProcessIds
  )

  $Clean = @($ProcessIds | Where-Object { $_ -gt 0 } | Select-Object -Unique)
  Set-Content -Path (Get-OrionPidFile -Name $Name) -Value $Clean -Encoding ASCII
}

function Get-OrionChildProcessIds {
  param([int]$ProcessId)

  $Children = Get-CimInstance Win32_Process -Filter "ParentProcessId = $ProcessId" -ErrorAction SilentlyContinue
  $Ids = @()
  foreach ($Child in @($Children)) {
    $ChildId = [int]$Child.ProcessId
    $Ids += $ChildId
    $Ids += Get-OrionChildProcessIds -ProcessId $ChildId
  }

  return $Ids
}

function Stop-OrionProcessTree {
  param([int]$ProcessId)

  if (-not (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue)) {
    return
  }

  foreach ($ChildId in @(Get-OrionChildProcessIds -ProcessId $ProcessId | Select-Object -Unique)) {
    Stop-OrionProcessTree -ProcessId $ChildId
  }

  Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
}

function Stop-OrionTrackedProcesses {
  param([string]$Name)

  $Pids = @(Read-OrionPids -Name $Name | Select-Object -Unique)
  foreach ($TrackedPid in $Pids) {
    Stop-OrionProcessTree -ProcessId $TrackedPid
  }

  Remove-Item -Path (Get-OrionPidFile -Name $Name) -Force -ErrorAction SilentlyContinue
}

function Stop-OrionAllTrackedProcesses {
  Stop-OrionTrackedProcesses -Name "frontend"
  Stop-OrionTrackedProcesses -Name "backend"
}

function Assert-OrionPortAvailable {
  param(
    [int]$Port,
    [string]$ServiceName
  )

  $Owners = @(Get-OrionPortOwners -Port $Port)
  if ($Owners.Count -eq 0) {
    return
  }

  $Lines = @()
  foreach ($Owner in $Owners) {
    $Command = if ($Owner.CommandLine) { $Owner.CommandLine } else { "command line unavailable" }
    $Lines += "Port $Port is already in use by PID $($Owner.ProcessId) ($($Owner.Name)): $Command"
  }

  $Lines += "Where: Start-Orion.ps1 - $ServiceName port check."
  $Lines += "Fix: double-click 'Orion Remove Old Services' once, then double-click 'Orion Start'."
  throw ($Lines -join [Environment]::NewLine)
}

function Show-OrionLegacyServiceHint {
  $Services = @(Get-Service -Name orion-backend, orion-frontend -ErrorAction SilentlyContinue)
  $Running = @($Services | Where-Object { $_.Status -eq "Running" })
  if ($Running.Count -gt 0) {
    Write-Host ""
    Write-Host "Old Orion Windows services are still running."
    Write-Host "Use the 'Orion Remove Old Services' desktop shortcut once to free fixed ports."
  }
}

function Show-OrionPortSummary {
  foreach ($Port in @($Script:BackendPort, $Script:FrontendPort)) {
    $Owners = @(Get-OrionPortOwners -Port $Port)
    if ($Owners.Count -eq 0) {
      Write-Host ("Port {0}: clear" -f $Port)
    }
    else {
      foreach ($Owner in $Owners) {
        Write-Host ("Port {0}: PID {1} ({2})" -f $Port, $Owner.ProcessId, $Owner.Name)
      }
    }
  }
}

function Wait-OrionClose {
  param([switch]$NoPause)

  if (-not $NoPause) {
    Read-Host "Press Enter to close" | Out-Null
  }
}
