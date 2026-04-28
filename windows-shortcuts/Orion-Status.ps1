$ErrorActionPreference = "Continue"

Write-Host "Orion service status"
Get-Service orion-backend,orion-frontend | Select-Object Name, Status, StartType | Format-Table -AutoSize

Write-Host ""
Write-Host "Backend health"
try {
  Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5 | Format-List
}
catch {
  Write-Host "Backend health check failed: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "Frontend health through proxy"
try {
  Invoke-RestMethod -Uri "http://localhost:3000/api/health" -TimeoutSec 5 | Format-List
}
catch {
  Write-Host "Frontend health check failed: $($_.Exception.Message)"
}

Read-Host "Press Enter to close"
