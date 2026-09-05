# Complete Setup Guide for All AI Video Generation Tools

## 📡 System Setup

### 1. Install NVIDIA CUDA (for GPU Support)

**Ubuntu/Debian:**
```bash
# Add NVIDIA repository
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-repo-ubuntu2204_12.3.1-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204_12.3.1-1_amd64.deb
sudo apt-get update
sudo apt-get -y install cuda
```

**Windows:**
- Download from: https://developer.nvidia.com/cuda-downloads
- Follow installer instructions

**macOS:**
- CUDA not officially supported on macOS
- Use cloud GPU services instead (Google Colab, Lambda Labs, etc.)

### 2. Install cuDNN (CUDA Deep Neural Network Library)

```bash
# Download from NVIDIA website (requires account)
# https://developer.nvidia.com/cudnn

# For Linux:
tar -xvf cudnn-*.tgz
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo ldconfig
```

### 3. Install Python & Git

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.10 python3-pip git wget curl

# Verify installation
python3 --version
git --version
```

### 4. Install PyTorch with CUDA Support

```bash
# Install latest PyTorch with CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify GPU support
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

---

## 🚀 Quick Start Guides by Tool

### LTX-Video (Fastest - Start Here)

```bash
# 1. Clone repository
git clone https://github.com/Lightricks/LTX-Video
cd LTX-Video

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate your first video
python infer.py --prompt "A beautiful sunset over ocean waves" --output video.mp4
```

### Wan 2.2 (Best Quality)

```bash
# 1. Clone repository
git clone https://github.com/baidu/Wan2.2
cd Wan2.2

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download model weights from Hugging Face
huggingface-cli download model-name --local-dir ./models

# 5. Generate video
python generate.py --prompt "Your creative prompt" --output output.mp4
```

### HunyuanVideo (Cinematic Quality)

```bash
# 1. Clone repository
git clone https://github.com/Tencent/HunyuanVideo
cd HunyuanVideo

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download models
huggingface-cli download Tencent/HunyuanVideo --local-dir ./models

# 5. Generate video
python infer.py --prompt "Cinematic scene description"
```

### Mochi 1 (Easy Fine-tuning)

```bash
# 1. Clone repository
git clone https://github.com/genmo/Mochi-1
cd Mochi-1

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate video
python generate.py --prompt "Your prompt" --output video.mp4
```

### CogVideoX (Image Animation)

```bash
# 1. Clone repository
git clone https://github.com/THUDM/CogVideoX
cd CogVideoX

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate video from image
python infer.py --image_path input.jpg --prompt "Animation description"
```

### AnimateDiff (Low VRAM)

```bash
# 1. Clone repository
git clone https://github.com/guoyww/AnimateDiff
cd AnimateDiff

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Animate an image
python animate.py --image image.jpg --motion "motion description"
```

### Open-Sora (Research & Training)

```bash
# 1. Clone repository
git clone https://github.com/HPC-AI-Open/Open-Sora
cd Open-Sora

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download models and follow repo for training/inference
```

### Stable Video Diffusion (All-purpose)

```bash
# 1. Install via pip
pip install diffusers transformers accelerate torch

# 2. Create inference script (save as generate_svd.py)
python << 'EOF'
from diffusers import StableVideoDiffusionPipeline
from PIL import Image
import torch

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.enable_attention_slicing()

image = Image.open("input.jpg").resize((1024, 576))

frames = pipe(image, num_frames=25, height=576, width=1024, num_inference_steps=25).frames

import imageio
imageio.mimsave("output.mp4", frames, fps=7)
EOF

# 3. Run
python generate_svd.py
```

### VideoCrafter (Artistic Styles)

```bash
# 1. Clone repository
git clone https://github.com/AILab-CVC/VideoCrafter
cd VideoCrafter

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download models
bash scripts/download_models.sh

# 5. Generate video
python scripts/inference.py --prompt "Your prompt"
```

### ModelScope T2V (Balanced)

```bash
# 1. Clone repository
git clone https://github.com/damo-vilab/modelscope
cd modelscope

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate video
python infer.py --prompt "Your prompt" --output video.mp4
```

---

## ☁️ Cloud GPU Setup

### Google Colab (Free with GPU)

Create a new notebook and run:

```python
# 1. Install dependencies
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
!pip install git+https://github.com/Lightricks/LTX-Video

# 2. Clone and setup tool
!git clone https://github.com/Lightricks/LTX-Video
%cd LTX-Video
!pip install -r requirements.txt

# 3. Generate video
!python infer.py --prompt "Your prompt" --output video.mp4

# 4. Download
from google.colab import files
files.download('video.mp4')
```

### Lambda Labs ($0.50/hr)

```bash
# 1. Sign up and launch instance at https://www.lambdalabs.com/
# 2. SSH into instance
ssh ubuntu@<instance-ip>

# 3. Install NVIDIA drivers (usually pre-installed)
nvidia-smi

# 4. Install CUDA (usually pre-installed)
nvcc --version

# 5. Follow tool setup above
git clone https://github.com/Lightricks/LTX-Video
cd LTX-Video
pip install -r requirements.txt
python infer.py --prompt "prompt"
```

### Runpod ($0.14-1.22/hr)

```bash
# 1. Visit https://www.runpod.io
# 2. Select GPU template and launch pod
# 3. Use terminal or Jupyter notebook
# 4. Follow tool setup

# Example in terminal:
git clone https://github.com/Lightricks/LTX-Video
cd LTX-Video
pip install -r requirements.txt
python infer.py --prompt "prompt"
```

### Vast.ai ($0.10-0.50/hr)

```bash
# 1. Sign up at https://www.vast.ai/
# 2. Rent GPU instance
# 3. SSH or use Jupyter
# 4. Run setup commands
```

---

## 🐳 Docker Setup (For All Tools)

### Create Universal Dockerfile

```dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /workspace

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install common dependencies
RUN pip install transformers diffusers accelerate safetensors pillow

# Clone example tool (LTX-Video)
RUN git clone https://github.com/Lightricks/LTX-Video /workspace/ltx-video
WORKDIR /workspace/ltx-video
RUN pip install -r requirements.txt

ENTRYPOINT ["bash"]
```

### Build and Run

```bash
# Build image
docker build -t ai-video-gen:latest .

# Run interactive
docker run --gpus all -it -v $(pwd)/outputs:/workspace/outputs ai-video-gen:latest

# Run command directly
docker run --gpus all -v $(pwd)/outputs:/workspace/outputs ai-video-gen:latest \
  -c "cd /workspace/ltx-video && python infer.py --prompt 'Your prompt' --output /workspace/outputs/video.mp4"
```

---

## 🔧 Troubleshooting

### CUDA Not Found

```bash
# Check CUDA installation
nvcc --version

# Check NVIDIA driver
nvidia-smi

# Verify PyTorch CUDA support
python3 -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"

# Reinstall PyTorch if needed
pip install --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Out of Memory (OOM) Error

```bash
# Reduce batch size
python infer.py --prompt "prompt" --batch_size 1

# Use lower resolution
python infer.py --prompt "prompt" --resolution 512x384

# Enable memory optimization
python infer.py --prompt "prompt" --enable_memory_efficient_attention --use_half_precision

# Clear GPU cache
python3 -c "import torch; torch.cuda.empty_cache()"
```

### Slow Inference

```bash
# Check GPU usage
watch -n 1 nvidia-smi

# Reduce resolution for testing
python infer.py --prompt "prompt" --resolution 512x384

# Use faster model (LTX-Video)
git clone https://github.com/Lightricks/LTX-Video

# Enable optimizations
python infer.py --prompt "prompt" --use_half_precision --enable_attention_slicing
```

### Model Download Issues

```bash
# Manual download using Hugging Face CLI
pip install huggingface-hub

# Download specific model
huggingface-cli download model-name --local-dir ./models

# Check internet connection
ping google.com

# Test Hugging Face access
python3 -c "from huggingface_hub import list_repo_files; list_repo_files('repo_id')"
```

### Permission Denied

```bash
# Fix permission issues
chmod +x *.py
sudo chown -R $USER:$USER .
```

---

## 🚀 Performance Optimization

### GPU Memory Management

```python
# In your Python scripts
import torch

# Enable mixed precision (faster, less memory)
with torch.cuda.amp.autocast():
    output = model(input)

# Clear cache periodically
torch.cuda.empty_cache()

# Use gradient checkpointing
model.gradient_checkpointing_enable()
```

### Batch Processing Script

```bash
#!/bin/bash
# save as batch_generate.sh

cat prompts.txt | while read prompt; do
    timestamp=$(date +%s)
    echo "Generating: $prompt"
    python infer.py --prompt "$prompt" --output "video_$timestamp.mp4"
    echo "Done: $timestamp"
    sleep 2
done

# Run
chmod +x batch_generate.sh
./batch_generate.sh
```

---

## 📊 Resource Monitoring

```bash
# Monitor GPU in real-time
watch -n 1 nvidia-smi

# Monitor CPU and Memory
top

# Check disk usage
df -h

# Monitor specific process
pid=$(pgrep -f "python infer.py")
watch -n 1 "ps aux | grep $pid"
```

---

## 📚 Additional Resources

- **PyTorch Installation:** https://pytorch.org/get-started/locally/
- **NVIDIA CUDA Toolkit:** https://developer.nvidia.com/cuda-toolkit
- **NVIDIA cuDNN:** https://developer.nvidia.com/cudnn
- **Hugging Face Hub:** https://huggingface.co
- **Docker Documentation:** https://docs.docker.com
- **Google Colab:** https://colab.research.google.com
- **Lambda Labs:** https://www.lambdalabs.com/
- **Runpod:** https://www.runpod.io/
- **Vast.ai:** https://www.vast.ai/

---

**🎬 You're ready to generate videos with any tool!**
