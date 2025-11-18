# UPDATERS - Automated Setup Script for Windows
# Run this script in PowerShell to set up the development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  UPDATERS - Development Setup Script  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to main directory
Set-Location -Path "main"

# Step 1: Create virtual environment
Write-Host "[1/8] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists. Skipping..." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Step 2: Activate virtual environment
Write-Host "[2/8] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "   Virtual environment activated" -ForegroundColor Green

# Step 3: Upgrade pip
Write-Host "[3/8] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "   Pip upgraded" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host "[4/8] Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   Dependencies installed" -ForegroundColor Green

# Step 5: Create .env file
Write-Host "[5/8] Setting up environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  .env file already exists. Skipping..." -ForegroundColor Gray
} else {
    Copy-Item ".env.example" ".env"
    
    # Generate SECRET_KEY
    $secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    
    # Update .env file
    (Get-Content ".env") -replace "your-secret-key-here-change-this-in-production", $secretKey | Set-Content ".env"
    
    Write-Host "   .env file created with generated SECRET_KEY" -ForegroundColor Green
}

# Step 6: Run migrations
Write-Host "[6/8] Running database migrations..." -ForegroundColor Yellow
python manage.py migrate --noinput
Write-Host "   Migrations applied" -ForegroundColor Green

# Step 7: Load fixtures
Write-Host "[7/8] Loading initial data (categories)..." -ForegroundColor Yellow
python manage.py loaddata feed/fixtures/categories.json
Write-Host "   Categories loaded" -ForegroundColor Green

# Step 8: Collect static files
Write-Host "[8/8] Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput --clear
Write-Host "   Static files collected" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Create a superuser: python manage.py createsuperuser" -ForegroundColor White
Write-Host "  2. Run the server: python manage.py runserver" -ForegroundColor White
Write-Host "  3. Open browser: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host ""
Write-Host "Admin panel: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host ""
