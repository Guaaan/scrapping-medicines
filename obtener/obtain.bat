@echo off
echo C:\Program Files\Python310C:\python.exe >archivotemporal.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >archivotemporal.ps1
echo C:\price-scraper\obtener\obtener.py >archivotemporal.ps1
powershell.exe -ExecutionPolicy Bypass -File "archivotemporal.ps1"
del archivotemporal.ps1
