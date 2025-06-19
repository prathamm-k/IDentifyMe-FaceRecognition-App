#!/bin/bash
# Cross-platform (Linux/macOS) setup script for Face Recognition App
set -e

# Print info
echo "[INFO] Setting up Face Recognition App..."

# Create virtual environment if it doesn't exist
if [ ! -d "facerec-venv" ]; then
    echo "[INFO] Creating Python virtual environment..."
    python -m venv facerec-venv
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source facerec-venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "[INFO] Installing Python dependencies..."
pip install -r requirements.txt

echo "[INFO] Setup complete! Activate your venv with: source facerec-venv/bin/activate"
echo "[INFO] To run the app: streamlit run app.py" 