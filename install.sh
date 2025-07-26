#!/bin/usr/env bash
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not installed"
    exit 1
fi

if ! command -v pacman &> /dev/null; then
   if ! command -v pip3 &> /dev/null; then
       echo "ERROR: pip not installed"
       exit 1
   fi

   pip install -r requirements.txt

echo "Installation completed successfully, to run the program run python main.py"

