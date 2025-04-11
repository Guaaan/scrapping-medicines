@echo off
echo C:\Program Files\Python310C:\python.exe >salcobrand_arch.ps1
echo C:\Users\JUAN.RODRIGUEZ\Documents\repos\venv\Scripts\activate.bat >salcobrand_arch.ps1
echo C:\Users\JUAN.RODRIGUEZ\Documents\repos\scraper\guardar\insert_salcobrand.py >salcobrand_arch.ps1
powershell.exe -ExecutionPolicy Bypass -File "salcobrand_arch.ps1"
del salcobrand_arch.ps1