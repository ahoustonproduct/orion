$ErrorActionPreference = "Stop"

$OrionRoot = "C:\Users\Hack\orion"
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
New-PowerShellShortcut -Name "Orion Start" -Script "Start-Orion.ps1" -Description "Start Orion backend and frontend services" -IconLocation "$env:SystemRoot\System32\shell32.dll,167"
New-PowerShellShortcut -Name "Orion Restart" -Script "Restart-Orion.ps1" -Description "Restart Orion backend and frontend services" -IconLocation "$env:SystemRoot\System32\shell32.dll,238"
New-PowerShellShortcut -Name "Orion Stop" -Script "Stop-Orion.ps1" -Description "Stop Orion backend and frontend services" -IconLocation "$env:SystemRoot\System32\shell32.dll,109"
New-PowerShellShortcut -Name "Orion Rebuild Frontend" -Script "Rebuild-Orion-Frontend.ps1" -Description "Build frontend and restart Orion frontend service" -IconLocation "$env:SystemRoot\System32\shell32.dll,269"
New-PowerShellShortcut -Name "Orion Status" -Script "Orion-Status.ps1" -Description "Show Orion service and health status" -IconLocation "$env:SystemRoot\System32\shell32.dll,23"

Write-Host "Created Orion desktop shortcuts in $Desktop"
