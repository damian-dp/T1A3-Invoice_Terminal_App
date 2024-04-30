#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or newer to run the app."
    exit 1
fi



# Run the invoice app script
./run_invoice_app.sh