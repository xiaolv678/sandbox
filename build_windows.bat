@echo off
setlocal

cd /d "%~dp0"

py -m pip install -r requirements-build.txt
if errorlevel 1 exit /b 1

py -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('tkinter OK')"
if errorlevel 1 exit /b 1

py -m unittest discover
if errorlevel 1 exit /b 1

py -m PyInstaller --clean calculator.spec
if errorlevel 1 exit /b 1

echo Built app: dist\Calculator.exe
