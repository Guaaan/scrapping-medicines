@echo off
echo C:\Program Files\Python310C:\python.exe >eco.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >eco.ps1
echo C:\price-scraper\obtener\eco.py >eco.ps1
powershell.exe -ExecutionPolicy Bypass -File "eco.ps1"
del eco.ps1