@echo off
echo ============================================================
echo HiveMind - Git Repository Setup
echo ============================================================
echo.

cd /d "%~dp0"

echo Initializing Git repository...
"C:\Program Files\Git\bin\git.exe" init
if errorlevel 1 goto error

echo Configuring Git...
"C:\Program Files\Git\bin\git.exe" config user.name "HiveMind Developer"
"C:\Program Files\Git\bin\git.exe" config user.email "hivemind@example.com"

echo Adding files...
"C:\Program Files\Git\bin\git.exe" add .
if errorlevel 1 goto error

echo Creating initial commit...
"C:\Program Files\Git\bin\git.exe" commit -m "Initial commit: HiveMind distributed audio sync system v1.0"
if errorlevel 1 goto error

echo.
echo ============================================================
echo SUCCESS! Git repository initialized
echo ============================================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub: https://github.com/new
echo 2. Repository name: hivemind
echo 3. Do NOT initialize with README
echo 4. After creating, run these commands:
echo.
echo    "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/YOUR_USERNAME/hivemind.git
echo    "C:\Program Files\Git\bin\git.exe" branch -M main
echo    "C:\Program Files\Git\bin\git.exe" push -u origin main
echo.
echo Replace YOUR_USERNAME with your GitHub username
echo ============================================================
pause
exit /b 0

:error
echo.
echo ERROR: Git command failed
echo Please check that Git is installed correctly
pause
exit /b 1
