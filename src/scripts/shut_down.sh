#!/bin/bash

clear

rm -rf app/utils/__pycache__

# Delete the virtual environment
rm -rf app/.venv
echo "Virtual environment deleted."

echo "App now closed. Thanks for using my app!"