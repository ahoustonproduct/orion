$ErrorActionPreference = "Stop"

$StartScript = Join-Path $PSScriptRoot "windows-shortcuts\Start-Orion.ps1"
& $StartScript
exit $LASTEXITCODE
