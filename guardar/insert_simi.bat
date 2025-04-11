@echo off
echo C:\Program Files\Python310C:\python.exe >simi_arch.ps1
echo C:\Users\JUAN.RODRIGUEZ\Documents\repos\venv\Scripts\activate.bat >simi_arch.ps1
echo C:\Users\JUAN.RODRIGUEZ\Documents\repos\scraper\guardar\insert_simi.py >simi_arch.ps1
powershell.exe -ExecutionPolicy Bypass -File "simi_arch.ps1"
del simi_arch.ps1