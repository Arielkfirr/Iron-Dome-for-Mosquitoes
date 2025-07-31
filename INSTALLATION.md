# 📦 Installation Guide

## 🎯 Overview

This guide will help you install and configure Iron Dome for Mosquitoes on your Windows system.

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 or higher
- **RAM**: 4 GB
- **Storage**: 2 GB free space
- **Internet**: Required for model download

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **Python**: 3.9 or higher
- **RAM**: 8 GB or more
- **Storage**: 5 GB free space
- **GPU**: NVIDIA GPU with CUDA support (optional)

## 🚀 Quick Installation

### Step 1: Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Verify installation: `python --version`

### Step 2: Clone Repository
```bash
git clone https://github.com/username/Iron-Dome-for-Mosquitoes.git
cd IronDomeMosquitoes
```

### Step 3: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Download AI Model
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Step 6: Configure Phone Link
```bash
python auto_phone_link_setup.py
```

### Step 7: Run the System
```bash
python src/main.py --dev
```

## ⚙️ Advanced Configuration

### Custom Configuration
Edit `config/config.yaml` to customize settings:

```yaml
detection:
  confidence_threshold: 0.3  # Detection sensitivity
  classes_to_detect: ["mosquito", "insect", "fly"]

camera:
  phone_link:
    enabled: true
    capture_folder: "data/captures"
```

### Environment Variables
Create `.env` file for sensitive settings:

```env
# Optional: Google Drive integration
GOOGLE_DRIVE_CREDENTIALS=path/to/credentials.json
GOOGLE_DRIVE_TOKEN=path/to/token.json

# Optional: Database settings
DATABASE_URL=sqlite:///data/system.db

# Optional: Web interface
WEB_HOST=localhost
WEB_PORT=5000
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Python Not Found
```bash
# Add Python to PATH manually
set PATH=%PATH%;C:\Python39\
```

#### 2. Package Installation Errors
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

#### 3. Model Download Issues
```bash
# Manual model download
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

#### 4. Phone Link Connection Issues
1. Ensure Phone Link app is installed
2. Check Windows version compatibility
3. Restart Phone Link service

### Performance Optimization

#### Enable GPU Acceleration
```bash
# Install CUDA version of PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### Memory Optimization
```yaml
performance:
  max_memory_usage: "1 GB"  # Reduce for low RAM systems
  batch_processing: false    # Disable for single image processing
```

## 📊 Verification

### Test Installation
```bash
# Run system test
python -c "
from src.core.system_manager import SystemManager
from utils.config_loader import ConfigLoader
config = ConfigLoader('config/config.yaml').load()
print('✅ System components loaded successfully')
"
```

### Check Dependencies
```bash
# Verify all packages
pip list | findstr -i "opencv ultralytics numpy pillow"
```

## 🎉 Success!

Your Iron Dome for Mosquitoes system is now ready to use!

### Next Steps
1. **Configure Phone Link**: Follow the setup wizard
2. **Test Detection**: Take a photo and verify detection
3. **Monitor Performance**: Check logs for system status
4. **Customize Settings**: Adjust configuration as needed

### Support
- 📖 [Documentation](README.md)
- 🐛 [Issue Tracker](https://github.com/username/Iron-Dome-for-Mosquitoes/issues)
- 💬 [Discussions](https://github.com/username/Iron-Dome-for-Mosquitoes/discussions)

---

**🦟 Iron Dome for Mosquitoes 🛡️** - Advanced AI-powered pest detection system 