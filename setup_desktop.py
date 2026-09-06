#!/usr/bin/env python3
"""
Desktop App Setup Helper
Automatic installation and configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🎬 AI Video Generator - Desktop App Setup               ║
    ║     Free • Unlimited • Standalone                        ║
    ║                                                           ║
    ║  This script will:                                       ║
    ║  ✅ Create virtual environment                           ║
    ║  ✅ Install dependencies                                 ║
    ║  ✅ Configure GPU support                                ║
    ║  ✅ Start the desktop app                                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or version.minor < 8:
        print("❌ Python 3.8+ required")
        print(f"   Current: {version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor} OK")

def create_venv():
    """Create virtual environment"""
    venv_path = Path('venv')
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return
    
    print("📦 Creating virtual environment...")
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
    print("✅ Virtual environment created")

def get_pip_path():
    """Get pip executable path"""
    system = platform.system()
    if system == 'Windows':
        return Path('venv/Scripts/pip.exe')
    else:
        return Path('venv/bin/pip')

def install_dependencies():
    """Install required packages"""
    pip_path = get_pip_path()
    
    print("📦 Upgrading pip...")
    subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], check=True)
    
    print("📦 Installing desktop dependencies...")
    subprocess.run([str(pip_path), 'install', '-r', 'requirements-desktop.txt'], check=True)
    print("✅ Dependencies installed")

def install_gpu_support():
    """Install GPU support"""
    pip_path = get_pip_path()
    
    response = input("\n🎮 Install GPU support (NVIDIA CUDA)? (y/n): ").lower()
    if response != 'y':
        print("⏭️  Skipping GPU support")
        return
    
    print("📦 Installing PyTorch with CUDA 12.1...")
    cmd = [
        str(pip_path), 'install',
        'torch', 'torchvision', 'torchaudio',
        '--index-url', 'https://download.pytorch.org/whl/cu121'
    ]
    subprocess.run(cmd, check=True)
    print("✅ GPU support installed")

def verify_setup():
    """Verify installation"""
    print("\n🔍 Verifying setup...")
    
    pip_path = get_pip_path()
    
    # Check PyQt5
    try:
        subprocess.run(
            [str(pip_path), 'show', 'PyQt5'],
            check=True,
            capture_output=True
        )
        print("✅ PyQt5 installed")
    except:
        print("❌ PyQt5 not found")
        return False
    
    # Check OpenCV
    try:
        subprocess.run(
            [str(pip_path), 'show', 'opencv-python'],
            check=True,
            capture_output=True
        )
        print("✅ OpenCV installed")
    except:
        print("❌ OpenCV not found")
        return False
    
    # Check Torch
    try:
        subprocess.run(
            [str(pip_path), 'show', 'torch'],
            check=True,
            capture_output=True
        )
        print("✅ PyTorch installed")
    except:
        print("❌ PyTorch not found")
        return False
    
    return True

def start_app():
    """Start the desktop app"""
    python_path = Path('venv')
    if platform.system() == 'Windows':
        python_path = python_path / 'Scripts' / 'python.exe'
    else:
        python_path = python_path / 'bin' / 'python'
    
    print("\n🚀 Starting Desktop App...")
    print("="*60)
    subprocess.run([str(python_path), 'desktop_app.py'])

def main():
    """Main setup flow"""
    print_banner()
    
    try:
        # Step 1: Check Python
        check_python()
        
        # Step 2: Create venv
        create_venv()
        
        # Step 3: Install dependencies
        install_dependencies()
        
        # Step 4: Install GPU support
        install_gpu_support()
        
        # Step 5: Verify
        if not verify_setup():
            print("\n❌ Setup verification failed")
            sys.exit(1)
        
        print("\n" + "="*60)
        print("✅ Setup Complete!")
        print("="*60)
        
        # Step 6: Start app
        response = input("\n🎬 Start Desktop App now? (y/n): ").lower()
        if response == 'y':
            start_app()
        else:
            print("\n📝 To start the app later, run:")
            if platform.system() == 'Windows':
                print("   venv\\Scripts\\python.exe desktop_app.py")
            else:
                print("   source venv/bin/activate")
                print("   python desktop_app.py")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
