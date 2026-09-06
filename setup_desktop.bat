@echo off
REM Quick start script for Windows

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  🎬 AI Video Generator - Desktop App Quick Start         ║
echo ║     Free • Unlimited • Standalone                        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if venv exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate venv
echo ⚙️  Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements-desktop.txt >nul 2>&1

REM Optional GPU support
set /p gpu="🎮 Install GPU support (NVIDIA CUDA)? (y/n): "
if /i "%gpu%"=="y" (
    echo 📦 Installing PyTorch with CUDA...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 >nul 2>&1
)

REM Verify
echo.
echo 🔍 Verifying installation...
python -c "import PyQt5; print('✅ PyQt5 OK')" 2>nul || echo ❌ PyQt5 missing
python -c "import cv2; print('✅ OpenCV OK')" 2>nul || echo ❌ OpenCV missing
python -c "import torch; print('✅ PyTorch OK')" 2>nul || echo ❌ PyTorch missing

echo.
echo ✅ Setup Complete!
echo.
set /p start="🎬 Start Desktop App now? (y/n): "
if /i "%start%"=="y" (
    python desktop_app.py
) else (
    echo 📝 To start the app later, run:
    echo    python desktop_app.py
)
