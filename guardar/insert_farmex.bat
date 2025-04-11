@echo off
echo C:\Program Files\Python310C:\python.exe >farmex_arch.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >farmex_arch.ps1
echo C:\price-scraper\guardar\insert_farmex.py >farmex_arch.ps1
powershell.exe -ExecutionPolicy Bypass -File "farmex_arch.ps1"
del farmex_arch.ps1