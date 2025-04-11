@echo off
echo C:\Program Files\Python310C:\python.exe >ahumada_arch.ps1
echo C:\Users\JUAN.RODRIGUEZ\Documents\repos\venv\Scripts\activate.bat >ahumada_arch.ps1
echo C:\Users\JUAN.RODRIGUEZ\Documents\repos\scraper\guardar\insert_ahumada.py >ahumada_arch.ps1
powershell.exe -ExecutionPolicy Bypass -File "ahumada_arch.ps1"
del ahumada_arch.ps1