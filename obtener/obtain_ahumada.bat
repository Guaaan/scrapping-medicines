@echo off
echo C:\Program Files\Python310C:\python.exe >archivotemporalahumada.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >archivotemporalahumada.ps1
echo C:\price-scraper\obtener\ahumada.py >archivotemporalahumada.ps1
powershell.exe -ExecutionPolicy Bypass -File "archivotemporalahumada.ps1"
del archivotemporalahumada.ps1