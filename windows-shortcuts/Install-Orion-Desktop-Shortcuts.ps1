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

function New-UrlShortcut {
  param(
    [string]$Name,
    [string]$Url
  )

  $ShortcutPath = Join-Path $Desktop "$Name.url"
  @(
    "[InternetShortcut]",
    "URL=$Url",
    "IconFile=$env:SystemRoot\System32\shell32.dll",
    "IconIndex=220"
  ) | Set-Content -Path $ShortcutPath -Encoding ASCII
}

New-UrlShortcut -Name "Open Orion" -Url "http://localhost:3000/"
New-PowerShellShortcut -Name "Orion" -Script "Start-Orion.ps1" -Description "Start Orion as a local desktop app" -IconLocation "$env:SystemRoot\System32\shell32.dll,167"
New-PowerShellShortcut -Name "Orion Start" -Script "Start-Orion.ps1" -Description "Start Orion as a local desktop app" -IconLocation "$env:SystemRoot\System32\shell32.dll,167"
New-PowerShellShortcut -Name "Orion Stop" -Script "Stop-Orion.ps1" -Description "Stop Orion frontend and backend processes" -IconLocation "$env:SystemRoot\System32\shell32.dll,109"
New-PowerShellShortcut -Name "Orion Restart" -Script "Restart-Orion.ps1" -Description "Restart Orion frontend and backend processes" -IconLocation "$env:SystemRoot\System32\shell32.dll,238"
New-PowerShellShortcut -Name "Orion Status" -Script "Orion-Status.ps1" -Description "Show Orion ports, health, and logs" -IconLocation "$env:SystemRoot\System32\shell32.dll,23"
New-PowerShellShortcut -Name "Orion Rebuild Frontend" -Script "Rebuild-Orion-Frontend.ps1" -Description "Rebuild Orion frontend and restart the app" -IconLocation "$env:SystemRoot\System32\shell32.dll,269"
New-PowerShellShortcut -Name "Orion Remove Old Services" -Script "Remove-Old-Orion-Services.ps1" -Description "Remove the old admin-owned Orion Windows services" -IconLocation "$env:SystemRoot\System32\shell32.dll,131"

Write-Host ("Created Orion desktop shortcuts in {0}" -f $Desktop)
Write-Host "Use 'Orion Remove Old Services' once if ports 3000 or 8000 are still owned by old services."
if (-not $NoPause) {
  Read-Host "Press Enter to close" | Out-Null
}
