# HiveMind - GitHub Setup Guide

## Prerequisites

Git is required to push to GitHub. If you don't have Git installed:

### Install Git on Windows

1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings
4. Restart your terminal after installation

## Quick Setup (After Git is Installed)

```bash
# Navigate to project directory
cd "c:\Users\chava\OneDrive\Desktop\Hive Mind"

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: HiveMind distributed audio sync system"

# Create GitHub repository (on GitHub.com)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/hivemind.git
git branch -M main
git push -u origin main
```

## Step-by-Step Instructions

### 1. Install Git (if not installed)
- Download from: https://git-scm.com/download/win
- Install with default options
- Restart terminal

### 2. Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name: `hivemind`
4. Description: "Distributed audio synchronization system"
5. Public or Private (your choice)
6. **Do NOT** initialize with README (we already have one)
7. Click "Create repository"

### 3. Initialize Local Repository

```bash
cd "c:\Users\chava\OneDrive\Desktop\Hive Mind"
git init
git add .
git commit -m "Initial commit: HiveMind v1.0"
```

### 4. Connect to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/hivemind.git
git branch -M main
git push -u origin main
```

### 5. Verify

Go to your GitHub repository URL and verify all files are there.

## Files Included

The repository includes:
- ✅ Complete HiveMind source code
- ✅ Web dashboard
- ✅ Unit tests
- ✅ Documentation (README.md)
- ✅ Requirements (requirements.txt)
- ✅ .gitignore
- ✅ LICENSE (MIT)

## Future Updates

After initial push, to update:

```bash
git add .
git commit -m "Description of changes"
git push
```

## Troubleshooting

**"git is not recognized"**
- Git is not installed or not in PATH
- Install Git and restart terminal

**Authentication failed**
- Use GitHub Personal Access Token instead of password
- Create token at: https://github.com/settings/tokens

**Permission denied**
- Check repository URL is correct
- Verify you have write access to the repository
