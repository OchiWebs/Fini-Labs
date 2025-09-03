#!/bin/bash

# Deletes the old database to reset
echo "Deleting old database..."
rm -rf instance db.sqlite3

# Creates a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activates the virtual environment
source venv/Scripts/activate

# Installs requirements
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Runs the application
echo "Starting Flask server at http://0.0.0.0:5000..."
python app.py