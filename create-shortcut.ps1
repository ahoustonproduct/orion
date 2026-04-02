$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\Hack\Desktop\Orion Code.lnk")
$Shortcut.TargetPath = "C:\Users\Hack\AppData\Local\Programs\Antigravity\orion\start-orion.bat"
$Shortcut.WorkingDirectory = "C:\Users\Hack\AppData\Local\Programs\Antigravity\orion"
$Shortcut.Description = "Orion Code - AI Learning Platform"
$Shortcut.Save()
Write-Host "Shortcut created on desktop!"