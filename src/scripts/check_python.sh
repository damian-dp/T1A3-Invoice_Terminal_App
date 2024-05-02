#!/bin/bash

clear

echo "Checking Python3 install. Please wait..."

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or newer to run the app."
    exit 1
fi

# Get the installed Python version
python_version=$(python3 --version 2>&1 | cut -d ' ' -f 2)

# Check if the installed Python version is 3.8 or newer
if [ "$(printf '%s\n' "3.8" "$python_version" | sort -V | head -n1)" != "3.8" ]; then
    echo "Error: Python $python_version is installed."
    echo "Please update to Python 3.8 or newer to run the app."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &>/dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 to run the app."
    exit 1
fi

echo "Python 3.8 or newer and pip3 is installed. Installing dependencies..."

# Make the run_invoice_app.sh script executable
chmod +x ./scripts/install_dependencies.sh

# Run the invoice app script
./scripts/install_dependencies.sh