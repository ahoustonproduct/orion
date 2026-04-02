@echo off
:: Create Desktop Shortcut for Orion Code
set "SCRIPT_DIR=%~dp0"
set "BAT_PATH=%SCRIPT_DIR%start-orion.bat"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\Orion Code.lnk"

:: Create VBScript to make the shortcut
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
echo Set Shortcut = WshShell.CreateShortcut("%SHORTCUT_PATH%") >> "%TEMP%\create_shortcut.vbs"
echo Shortcut.TargetPath = "%BAT_PATH%" >> "%TEMP%\create_shortcut.vbs"
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\create_shortcut.vbs"
echo Shortcut.Description = "Orion Code - AI Learning Platform" >> "%TEMP%\create_shortcut.vbs"
echo Shortcut.IconLocation = "%BAT_PATH%, 0" >> "%TEMP%\create_shortcut.vbs"
echo Shortcut.Save >> "%TEMP%\create_shortcut.vbs"

:: Run the VBScript
cscript //nologo "%TEMP%\create_shortcut.vbs"

:: Clean up
del "%TEMP%\create_shortcut.vbs"

echo.
echo ============================================
echo   Desktop Shortcut Created!
echo ============================================
echo.
echo   A "Orion Code" shortcut has been added to your desktop.
echo   You can also drag this shortcut to your taskbar.
echo.
echo   Double-click to start Orion Code anytime!
echo ============================================
pause