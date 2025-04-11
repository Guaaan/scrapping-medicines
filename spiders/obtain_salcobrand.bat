@echo off
echo C:\Program Files\Python310C:\python.exe >salcotemporal.ps1
echo C:\price-scraper\venv\Scripts\activate.bat >salcotemporal.ps1
echo C:\Users\JUAN.RODRIGUEZ\Documents\repos\scraper\spiders\salcobrand.py >salcotemporal.ps1
powershell.exe -ExecutionPolicy Bypass -File "salcotemporal.ps1"
del salcotemporal.ps1