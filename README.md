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
