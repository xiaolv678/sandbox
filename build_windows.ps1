$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

py -m pip install -r requirements-build.txt
py -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('tkinter OK')"
py -m unittest discover
py -m PyInstaller --clean calculator.spec

Write-Host "Built app: dist\Calculator.exe"
