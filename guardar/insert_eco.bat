@echo off
echo C:\Program Files\Python310C:\python.exe >eco_arch.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >eco_arch.ps1
echo C:\price-scraper\guardar\insert_eco.py >eco_arch.ps1
powershell.exe -ExecutionPolicy Bypass -File "eco_arch.ps1"
del eco_arch.ps1