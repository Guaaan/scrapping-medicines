@echo off
echo C:\Program Files\Python310C:\python.exe >detailedeco.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >detailedeco.ps1
echo C:\price-scraper\obtener\detailedeco.py >detailedeco.ps1
powershell.exe -ExecutionPolicy Bypass -File "detailedeco.ps1"
del detailedeco.ps1