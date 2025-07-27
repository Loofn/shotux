#!/bin/bash

# Shotux Launcher Script
# Activates virtual environment and runs the application

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment and run the application
source .venv/bin/activate
python main.py "$@"
