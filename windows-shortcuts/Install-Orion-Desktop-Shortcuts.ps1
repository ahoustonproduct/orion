param([switch]$NoPause)

$ErrorActionPreference = "Stop"

$OrionRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ShortcutDir = Join-Path $OrionRoot "windows-shortcuts"
$Desktop = [Environment]::GetFolderPath("Desktop")
$PowerShell = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$Shell = New-Object -ComObject WScript.Shell

function New-PowerShellShortcut {
  param(
    [string]$Name,
    [string]$Script,
    [string]$Description,
    [string]$IconLocation
  )

  $ShortcutPath = Join-Path $Desktop "$Name.lnk"
  $ScriptPath = Join-Path $ShortcutDir $Script
  $Shortcut = $Shell.CreateShortcut($ShortcutPath)
  $Shortcut.TargetPath = $PowerShell
  $Shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""
  $Shortcut.WorkingDirectory = $OrionRoot
  $Shortcut.Description = $Description
  $Shortcut.IconLocation = $IconLocation
  $Shortcut.Save()
}

function Remove-DesktopShortcut {
  param([string]$Name)

  $ShortcutPath = Join-Path $Desktop $Name
  if (Test-Path $ShortcutPath) {
    Remove-Item -LiteralPath $ShortcutPath -Force
  }
}

foreach ($OldShortcut in @(
  "Open Orion.url",
  "Orion Rebuild Frontend.lnk",
  "Orion Remove Old Services.lnk",
  "Orion Restart.lnk",
  "Orion Start.lnk",
  "Orion Status.lnk"
)) {
  Remove-DesktopShortcut -Name $OldShortcut
}

New-PowerShellShortcut -Name "Orion" -Script "Start-Orion.ps1" -Description "Start Orion as a local desktop app" -IconLocation "$env:SystemRoot\System32\shell32.dll,167"
New-PowerShellShortcut -Name "Orion Stop" -Script "Stop-Orion.ps1" -Description "Stop Orion frontend and backend processes" -IconLocation "$env:SystemRoot\System32\shell32.dll,109"

Write-Host ("Created Orion desktop shortcuts in {0}" -f $Desktop)
if (-not $NoPause) {
  Read-Host "Press Enter to close" | Out-Null
}
