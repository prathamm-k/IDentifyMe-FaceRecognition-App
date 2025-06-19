# PowerShell setup script for Face Recognition App
Write-Host "[INFO] Setting up Face Recognition App..."

# Create virtual environment if it doesn't exist
if (!(Test-Path -Path "facerec-venv")) {
    Write-Host "[INFO] Creating Python virtual environment..."
    python -m venv facerec-venv
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..."
.\facerec-venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
Write-Host "[INFO] Installing Python dependencies..."
pip install -r requirements.txt

Write-Host "[INFO] Setup complete! Activate your venv with: .\facerec-venv\Scripts\Activate.ps1"
Write-Host "[INFO] To run the app: streamlit run app.py" 