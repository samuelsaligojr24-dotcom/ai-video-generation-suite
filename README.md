# AI Video Generation Suite

A complete collection of open-source AI video generation tools for creating professional-quality videos for free.

## 🎬 Tools Included

### 1. **Wan 2.2** (Alibaba)
- **Type:** Text-to-video
- **Best For:** Best quality, 720p videos
- **Features:** Strong prompt understanding, Apache-2.0 license, runs on 12GB+ GPUs
- **Quality:** Professional content, stylized/realistic videos
- **Repository:** https://github.com/baidu/Wan2.2
- **VRAM Required:** 12GB+

### 2. **HunyuanVideo** (Tencent)
- **Type:** Text-to-video
- **Best For:** Realistic motion, cinematic videos
- **Features:** Realistic motion, human subjects, cinematic realism
- **Quality:** Top realism in open source
- **Repository:** https://github.com/Tencent/HunyuanVideo
- **VRAM Required:** 24GB+ for best quality

### 3. **LTX-Video** (Lightricks)
- **Type:** Text-to-video
- **Best For:** Fastest on consumer GPUs
- **Features:** Rapid iterations, lower computational cost
- **Quality:** Good for social content, ad creatives
- **Repository:** https://github.com/Lightricks/LTX-Video
- **VRAM Required:** 8GB+

### 4. **Mochi 1** (Genmo)
- **Type:** Text-to-video & Image-to-video
- **Best For:** Easy to fine-tune
- **Features:** Smooth motion, Apache-2.0 license, ~10B parameters
- **Quality:** Custom pipelines, research-friendly
- **Repository:** https://github.com/genmo/Mochi-1
- **VRAM Required:** Varies

### 5. **CogVideoX**
- **Type:** Image-to-video
- **Best For:** Product demos, animations
- **Features:** Handles text/video input, handles long prompts
- **Quality:** Product showcases, image-based animation
- **Repository:** https://github.com/THUDM/CogVideoX
- **VRAM Required:** Varies

### 6. **AnimateDiff**
- **Type:** Image animation
- **Best For:** Works with low VRAM
- **Features:** Easy integration, lots of community plugins
- **Quality:** Animation loops, creative effects
- **Repository:** https://github.com/guoyww/AnimateDiff
- **VRAM Required:** Lower VRAM friendly

---

## 📋 Quick Comparison

| Tool | Speed | Quality | VRAM | Best For |
|------|-------|---------|------|----------|
| Wan 2.2 | Medium | ⭐⭐⭐⭐⭐ | 12GB+ | Professional content |
| HunyuanVideo | Slow | ⭐⭐⭐⭐⭐ | 24GB+ | Realistic cinematic |
| LTX-Video | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 8GB+ | Quick iterations |
| Mochi 1 | Medium | ⭐⭐⭐⭐ | Varies | Custom pipelines |
| CogVideoX | Medium | ⭐⭐⭐ | Varies | Image animation |
| AnimateDiff | Fast | ⭐⭐⭐ | Low | Budget GPUs |

---

## 🚀 Getting Started

### Prerequisites
- **GPU:** NVIDIA GPU with CUDA support (most tools)
- **Python:** 3.8 or higher
- **Git:** Installed on your system
- **Dependencies:** PyTorch, transformers, and others (tool-specific)

### Installation & Setup

#### Option 1: LTX-Video (Recommended for Beginners - Fastest)
```bash
# Clone the repository
git clone https://github.com/Lightricks/LTX-Video
cd LTX-Video

# Install dependencies
pip install -r requirements.txt

# Run inference
python infer.py --prompt "A beautiful sunset over mountains" --output_path video.mp4
```

#### Option 2: Wan 2.2 (Best Quality)
```bash
# Clone the repository
git clone https://github.com/baidu/Wan2.2
cd Wan2.2

# Install dependencies
pip install -r requirements.txt

# Download model weights from Hugging Face
# See repository for detailed instructions

# Generate video
python generate.py --prompt "Your text prompt here"
```

#### Option 3: HunyuanVideo (Cinematic Quality)
```bash
# Clone the repository
git clone https://github.com/Tencent/HunyuanVideo
cd HunyuanVideo

# Install dependencies
pip install -r requirements.txt

# Generate video with cinematic quality
python infer.py --prompt "Your cinematic prompt"
```

#### Option 4: Mochi 1 (Easy Fine-tuning)
```bash
# Clone the repository
git clone https://github.com/genmo/Mochi-1
cd Mochi-1

# Install dependencies
pip install -r requirements.txt

# Generate video
python generate.py --prompt "Your prompt here"
```

#### Option 5: CogVideoX (Image to Video)
```bash
# Clone the repository
git clone https://github.com/THUDM/CogVideoX
cd CogVideoX

# Install dependencies
pip install -r requirements.txt

# Generate video from image
python infer.py --image_path input.jpg --prompt "Animation prompt"
```

#### Option 6: AnimateDiff (Low VRAM)
```bash
# Clone the repository
git clone https://github.com/guoyww/AnimateDiff
cd AnimateDiff

# Install dependencies
pip install -r requirements.txt

# Animate an image
python animate.py --image input.jpg --motion "smooth camera pan"
```

---

## 💡 Usage Guide

### Basic Workflow
1. **Choose a tool** based on your needs (see comparison table)
2. **Clone the repository**
3. **Install dependencies**
4. **Prepare your input** (text prompt or image)
5. **Run inference**
6. **Export your video**

### Example Prompts
- "A cat walking through a sunny garden, cinematic lighting, 4K quality"
- "A spaceship flying through nebula clouds, sci-fi atmosphere, detailed"
- "Product showcase: Modern smartphone spinning on reflective surface, studio lighting"
- "Animated character running through forest, dynamic camera movement"

### Output Options
- **Resolution:** Usually 720p-1080p (depending on tool)
- **Frame Rate:** 24-30 fps
- **Format:** MP4, WebM, or other video formats

---

## 🔧 Advanced Setup

### Using Google Colab (Free GPU)
```bash
# In Google Colab notebook
!git clone https://github.com/Lightricks/LTX-Video
%cd LTX-Video
!pip install -r requirements.txt
```

### Using Docker
```bash
# Most tools provide Docker support
docker build -t ai-video-gen .
docker run --gpus all -it ai-video-gen
```

### Batch Processing
Each tool supports batch generation. Check individual repositories for batch processing guides.

---

## 📊 Performance Tips

| Scenario | Recommended Tool | Reason |
|----------|-----------------|--------|
| Fast prototyping | LTX-Video | Fastest inference |
| Highest quality | Wan 2.2 or HunyuanVideo | Best visual quality |
| Low VRAM (8GB) | LTX-Video or AnimateDiff | Optimized for limited resources |
| Image animation | CogVideoX or AnimateDiff | Specialized for images |
| Custom training | Mochi 1 | Best fine-tuning support |
| Professional use | Wan 2.2 | Commercial-safe license |

---

## 🔗 Resources

- **Hugging Face Models:** https://huggingface.co
- **Awesome AI Video Generation:** https://github.com/augstai/awesome-ai-video-generation
- **CUDA Setup Guide:** https://pytorch.org/get-started/locally/

---

## ⚙️ System Requirements

### Minimum
- **GPU:** 8GB VRAM (NVIDIA)
- **CPU:** Quad-core processor
- **RAM:** 16GB
- **Storage:** 50GB free space
- **OS:** Ubuntu 20.04+, Windows 10+, macOS

### Recommended
- **GPU:** 24GB+ VRAM (NVIDIA RTX 4090 or A100)
- **CPU:** High-end processor
- **RAM:** 64GB+
- **Storage:** 200GB+ SSD
- **OS:** Ubuntu 22.04+

---

## 🤝 Contributing

Want to add improvements, optimizations, or documentation? Pull requests welcome!

---

## 📝 License

Each tool has its own license. Most are open-source (Apache-2.0, MIT, etc.). Check individual repositories for details.

---

## ⚠️ Important Notes

- These tools require significant computational resources
- First download of models can take 30+ minutes
- VRAM requirements vary based on resolution and model size
- GPU support is primarily NVIDIA (some tools support AMD/CPU)
- Always read individual repository documentation for setup

---

## 🆘 Troubleshooting

### Out of Memory (OOM) Error
- Reduce resolution or video length
- Use a tool with lower VRAM requirements (AnimateDiff, LTX-Video)
- Enable mixed precision training

### Model Download Issues
- Check internet connection
- Use Hugging Face CLI to download models manually
- Check available disk space

### CUDA/GPU Issues
- Install NVIDIA CUDA Toolkit and cuDNN
- Update GPU drivers
- Verify PyTorch installation with CUDA support

---

## 🎯 Next Steps

1. **Pick a tool** from the list above
2. **Clone its repository** (links provided)
3. **Follow the setup** instructions for that tool
4. **Generate your first video!**

For detailed instructions and troubleshooting, visit each tool's GitHub repository.

---

**Happy video generating! 🎬✨**
