#!/bin/bash
# Quick start script for Linux/macOS

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  🎬 AI Video Generator - Desktop App Quick Start         ║"
echo "║     Free • Unlimited • Standalone                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "⚙️  Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-desktop.txt > /dev/null 2>&1

# Optional GPU support
read -p "🎮 Install GPU support (NVIDIA CUDA)? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Installing PyTorch with CUDA..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 > /dev/null 2>&1
fi

# Verify
echo ""
echo "🔍 Verifying installation..."
python3 -c "import PyQt5; print('✅ PyQt5 OK')" 2>/dev/null || echo "❌ PyQt5 missing"
python3 -c "import cv2; print('✅ OpenCV OK')" 2>/dev/null || echo "❌ OpenCV missing"
python3 -c "import torch; print('✅ PyTorch OK')" 2>/dev/null || echo "❌ PyTorch missing"

echo ""
echo "✅ Setup Complete!"
echo ""
read -p "🎬 Start Desktop App now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 desktop_app.py
else
    echo "📝 To start the app later, run:"
    echo "   source venv/bin/activate"
    echo "   python desktop_app.py"
fi
