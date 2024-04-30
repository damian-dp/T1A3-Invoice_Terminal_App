#!/bin/bash

# Remove existing virtual environment
rm -rf .venv

# Create a new virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install Python dependencies
pip3 install jinja2 xhtml2pdf colored

# Run the Python application
python invoice_app.py