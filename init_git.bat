@echo off
cd /d "%~dp0"
"C:\Program Files\Git\bin\git.exe" init
"C:\Program Files\Git\bin\git.exe" config user.name "HiveMind"
"C:\Program Files\Git\bin\git.exe" config user.email "hivemind@example.com"
"C:\Program Files\Git\bin\git.exe" add .
"C:\Program Files\Git\bin\git.exe" commit -m "Initial commit: HiveMind v1.0"
echo.
echo Git repository initialized!
echo Next: Create GitHub repo and push
echo See PUSH_TO_GITHUB.txt for instructions
