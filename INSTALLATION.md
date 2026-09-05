# Installation Instructions for All Tools

## Prerequisites Check

```bash
# Check GPU
nvidia-smi

# Check Python
python3 --version  # Should be 3.8+

# Check pip
pip --version

# Check Git
git --version
```

## Universal Installation Steps

### 1. System Dependencies (Ubuntu/Debian)

```bash
# Update package manager
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    ffmpeg \
    libsm6 \
    libxext6

# Verify installations
python3 --version
pip --version
git --version
```

### 2. NVIDIA CUDA & cuDNN Setup

```bash
# Check NVIDIA driver
nvidia-smi

# If driver not installed:
sudo apt-get install -y nvidia-driver-525  # Or latest version

# Install CUDA (example for Ubuntu 22.04)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-repo-ubuntu2204_12.3.1-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204_12.3.1-1_amd64.deb
sudo apt-get update
sudo apt-get -y install cuda

# Verify CUDA installation
nvcc --version
```

### 3. PyTorch Installation

```bash
# Install PyTorch with CUDA 12.1 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify PyTorch CUDA support
python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA version: {torch.version.cuda}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB')
"
```

---

## Step-by-Step Installation by Tool

### Template Installation Process

```bash
# 1. Clone tool repository
git clone <TOOL_REPOSITORY_URL>
cd <TOOL_NAME>

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 3. Upgrade pip
pip install --upgrade pip setuptools wheel

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download models (if required)
# Check tool-specific instructions

# 6. Test installation
python infer.py --help  # Or appropriate test command
```

### LTX-Video (Recommended First Tool)

```bash
git clone https://github.com/Lightricks/LTX-Video
cd LTX-Video

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Test
python infer.py --prompt "test" --output test.mp4 --resolution 512x384
```

### Wan 2.2

```bash
git clone https://github.com/baidu/Wan2.2
cd Wan2.2

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Download models from Hugging Face
pip install huggingface-hub
huggingface-cli download baidu/Wan2.2 --local-dir ./models

# Test
python generate.py --prompt "test" --output test.mp4
```

### HunyuanVideo

```bash
git clone https://github.com/Tencent/HunyuanVideo
cd HunyuanVideo

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Download models
huggingface-cli download Tencent/HunyuanVideo --local-dir ./models

# Test
python infer.py --prompt "test" --output test.mp4
```

### Mochi 1

```bash
git clone https://github.com/genmo/Mochi-1
cd Mochi-1

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Test
python generate.py --prompt "test" --output test.mp4
```

### CogVideoX

```bash
git clone https://github.com/THUDM/CogVideoX
cd CogVideoX

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Test
python infer.py --image_path test.jpg --prompt "test" --output test.mp4
```

### AnimateDiff

```bash
git clone https://github.com/guoyww/AnimateDiff
cd AnimateDiff

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Test
python animate.py --image test.jpg --output test.mp4
```

### Open-Sora

```bash
git clone https://github.com/HPC-AI-Open/Open-Sora
cd Open-Sora

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Follow repo for specific setup
```

### Stable Video Diffusion

```bash
# No repo clone needed, install via pip
pip install diffusers transformers accelerate safetensors pillow

# Create script file
cat > generate_svd.py << 'EOF'
from diffusers import StableVideoDiffusionPipeline
from PIL import Image
import torch

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")

image = Image.open("input.jpg").resize((1024, 576))
frames = pipe(image, num_frames=25).frames

import imageio
imageio.mimsave("output.mp4", frames, fps=7)
EOF

python generate_svd.py
```

### VideoCrafter

```bash
git clone https://github.com/AILab-CVC/VideoCrafter
cd VideoCrafter

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

bash scripts/download_models.sh

python scripts/inference.py --prompt "test"
```

### ModelScope T2V

```bash
git clone https://github.com/damo-vilab/modelscope
cd modelscope

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python infer.py --prompt "test" --output test.mp4
```

---

## Installation Verification Checklist

```bash
#!/bin/bash
# Save as verify_setup.sh

echo "=== GPU & CUDA Check ==="
nvidia-smi
echo ""

echo "=== Python Version ==="
python3 --version
echo ""

echo "=== PyTorch CUDA Check ==="
python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}')"
echo ""

echo "=== Required Packages ==="
python3 -c "import transformers; print(f'Transformers: OK')"
python3 -c "import diffusers; print(f'Diffusers: OK')"
python3 -c "import accelerate; print(f'Accelerate: OK')"
echo ""

echo "=== Disk Space ==="
df -h | grep -E '^/dev|Avail'
echo ""

echo "=== Setup Complete ==="
```

Run:
```bash
chmod +x verify_setup.sh
./verify_setup.sh
```

---

## Common Installation Issues & Fixes

### Issue: GPU Not Detected

```bash
# Solution 1: Update NVIDIA drivers
sudo apt-get install nvidia-driver-525

# Solution 2: Reinstall PyTorch
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Solution 3: Check CUDA environment
echo $CUDA_HOME
echo $LD_LIBRARY_PATH
```

### Issue: Missing Dependencies

```bash
# Solution 1: Install missing system packages
sudo apt-get install -y libsm6 libxext6 libxrender-dev

# Solution 2: Reinstall Python requirements
pip install --no-cache-dir -r requirements.txt --force-reinstall

# Solution 3: Use Python 3.10 specifically
python3.10 -m venv venv
```

### Issue: Model Download Fails

```bash
# Solution 1: Manual download
huggingface-cli download <model-name> --local-dir ./models

# Solution 2: Check internet
ping huggingface.co

# Solution 3: Use git-lfs
git lfs install
git clone https://huggingface.co/<model-repo>
```

### Issue: "No module named 'xxx'"

```bash
# Solution 1: Check virtual environment is activated
source venv/bin/activate
which python  # Should show venv path

# Solution 2: Install specific package
pip install <module-name>

# Solution 3: Check Python version compatibility
python3 --version  # Should be 3.8+
```

### Issue: Out of Memory During Installation

```bash
# Solution: Install with limited resources
pip install -r requirements.txt --no-cache-dir -q

# Or install one by one
while read requirement; do
    pip install "$requirement"
done < requirements.txt
```

---

## Installation Optimization Tips

```bash
# Faster installation
pip install -r requirements.txt --use-deprecated=legacy-resolver --no-cache-dir

# Parallel installation (if supported)
pip install -r requirements.txt --use-deprecated=legacy-resolver -q

# Use pre-built wheels
pip install --prefer-binary -r requirements.txt

# Check installation
pip check
```

---

## Multiple Tools Installation

```bash
# Create directory structure
mkdir ai-video-tools
cd ai-video-tools

# Install multiple tools with separate environments
for tool in LTX-Video Wan2.2 HunyuanVideo; do
    git clone <tool-url>
    cd $tool
    python3 -m venv venv_$tool
    source venv_$tool/bin/activate
    pip install -r requirements.txt
    cd ..
done
```

---

## After Installation: Next Steps

1. **Generate a test video**
   ```bash
   python infer.py --prompt "test" --output test.mp4
   ```

2. **Check output**
   ```bash
   ls -lh *.mp4
   ffplay test.mp4  # Or use your media player
   ```

3. **Refer to USAGE_EXAMPLES.md** for prompt ideas

4. **Refer to COMPARISON.md** for choosing other tools

5. **Monitor GPU** during generation
   ```bash
   watch -n 1 nvidia-smi
   ```

---

**✅ Installation complete! Ready to generate videos with all tools!**
