#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m pip install -r requirements-build.txt
python3 -m unittest discover
python3 -m PyInstaller --clean calculator.spec

echo "Built app: dist/Calculator"
