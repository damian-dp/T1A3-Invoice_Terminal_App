#!/bin/bash

# Remove existing virtual environment
rm -rf ../src/app/.venv

# Create a new virtual environment
python3 -m venv ../src/app/.venv

# Activate the virtual environment
source ../src/app/.venv/bin/activate

# Install Python dependencies
pip3 install jinja2 xhtml2pdf colored pyfiglet

echo "All dependencies installed. Running app..."

# Run the app
python3 ./app/main.py
