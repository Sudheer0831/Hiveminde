# HiveMind - GitHub Push Script
# Run this after Git installation completes

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "HiveMind - GitHub Setup" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "  Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Step 1: Initializing Git repository..." -ForegroundColor Yellow

# Initialize Git repository
git init

Write-Host "✓ Git repository initialized" -ForegroundColor Green
Write-Host ""

# Configure Git (if not already configured)
$userName = git config --global user.name
$userEmail = git config --global user.email

if (-not $userName) {
    Write-Host "Git user name not configured." -ForegroundColor Yellow
    $name = Read-Host "Enter your name"
    git config --global user.name "$name"
}

if (-not $userEmail) {
    Write-Host "Git user email not configured." -ForegroundColor Yellow
    $email = Read-Host "Enter your email"
    git config --global user.email "$email"
}

Write-Host ""
Write-Host "Step 2: Adding files to Git..." -ForegroundColor Yellow

# Add all files
git add .

Write-Host "✓ Files added" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Creating initial commit..." -ForegroundColor Yellow

# Create initial commit
git commit -m "Initial commit: HiveMind distributed audio sync system v1.0

Features:
- Distributed audio synchronization (<50ms accuracy)
- Opus audio compression (10x bandwidth reduction)
- Web dashboard with real-time monitoring
- Per-node volume control and balancing
- Automatic latency calibration
- Quality presets (Low/Medium/High/Ultra)
- TCP/IP transport layer
- NTP-like time synchronization
- Complete documentation and tests"

Write-Host "✓ Initial commit created" -ForegroundColor Green
Write-Host ""

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Repository settings:" -ForegroundColor White
Write-Host "   Name: hivemind" -ForegroundColor Yellow
Write-Host "   Description: Distributed audio synchronization system" -ForegroundColor Yellow
Write-Host "   Public or Private: Your choice" -ForegroundColor Yellow
Write-Host "   Do NOT initialize with README" -ForegroundColor Red
Write-Host ""
Write-Host "3. After creating the repository, run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/hivemind.git" -ForegroundColor Green
Write-Host "   git branch -M main" -ForegroundColor Green
Write-Host "   git push -u origin main" -ForegroundColor Green
Write-Host ""
Write-Host "Replace YOUR_USERNAME with your actual GitHub username" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
