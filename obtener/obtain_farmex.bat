@echo off
echo C:\Program Files\Python310C:\python.exe >farmex.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >farmex.ps1
echo C:\price-scraper\obtener\farmex.py >farmex.ps1
powershell.exe -ExecutionPolicy Bypass -File "farmex.ps1"
del farmex.ps1