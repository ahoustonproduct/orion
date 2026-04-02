$shell = New-Object -ComObject Shell.Application
$folder = $shell.NameSpace("C:\Users\Hack\Desktop")
$item = $folder.ParseName("Orion Code.lnk")
if ($item) {
    $verb = $item.Verbs() | Where-Object { $_.Name -eq "Pin to taskbar" }
    if ($verb) {
        $verb.Do()
        Write-Host "Pinned to taskbar!"
    } else {
        Write-Host "Could not find 'Pin to taskbar' verb. Trying alternative method..."
        # Alternative: Create a .url shortcut that can be pinned
        $urlShortcut = @"
[InternetShortcut]
URL=file://C:\Users\Hack\AppData\Local\Programs\Antigravity\orion\start-orion.bat
IconFile=C:\Users\Hack\AppData\Local\Programs\Antigravity\orion\start-orion.bat
IconIndex=0
"@
        $urlShortcut | Out-File -FilePath "C:\Users\Hack\Desktop\Orion Code.url" -Encoding UTF8
        Write-Host "Created .url file on desktop - drag it to taskbar to pin!"
    }
} else {
    Write-Host "Shortcut not found"
}