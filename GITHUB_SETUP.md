# GitHub Repository Setup Instructions

## 1. Create GitHub Repository

1. Go to https://github.com
2. Click "New repository"
3. Repository name: `iron-dome-mosquitoes`
4. Description: `Iron Dome for Mosquitoes - Advanced Cat Detection and Mosquito Prevention System`
5. Make it **Public** (so you can access it from work)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## 2. Connect Local Repository to GitHub

After creating the repository, run these commands:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/iron-dome-mosquitoes.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 3. Clone at Work

At your work computer:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/iron-dome-mosquitoes.git

# Navigate to project
cd iron-dome-mosquitoes

# Install dependencies
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run test
python test_cat_detection.py
```

## 4. Project Structure Overview

```
iron-dome-mosquitoes/
├── src/
│   ├── core/system_manager.py      # Main system coordinator
│   ├── detection/mosquito_detector.py  # AI detection engine
│   ├── camera/camera_manager.py    # Camera handling (Phone Link, USB, IP)
│   └── utils/
│       ├── logger.py               # Logging system
│       └── config_loader.py       # Configuration management
├── config/config.yaml              # System configuration
├── test_cat_detection.py          # Test script for cat detection
├── run_test.bat                   # Windows batch file
├── requirements.txt                # Python dependencies
└── README_QUICK_START.md         # Quick start guide
```

## 5. Quick Test Instructions

1. **Setup Phone Link:**
   - Open Phone Link on your PC
   - Click on 'Camera' in Phone Link
   - Take photos of your cats

2. **Run Test:**
   ```bash
   python test_cat_detection.py
   ```

3. **Expected Output:**
   - System will detect cats in photos
   - Annotated images saved in `data/detections/`
   - Real-time logging of detections

## 6. Next Steps

1. Test with phone camera for cat detection
2. Switch to computer webcam when ready
3. Implement on Raspberry Pi for final deployment
4. Add mosquito detection capabilities

## 7. Configuration

Edit `config/config.yaml` to customize:
- Camera settings
- Detection sensitivity
- Model paths
- Logging preferences 