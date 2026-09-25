@echo off
setlocal
cd /d "%~dp0.."
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --windowed --onefile --name SmartDesk --icon desktop/resources/smartdesk_icon.ico --add-data "desktop/resources;desktop/resources" desktop/main.py
if errorlevel 1 (
    echo.
    echo SmartDesk build failed.
    exit /b 1
)
echo.
echo SmartDesk.exe created at dist\SmartDesk.exe
endlocal
