# GitHub Repository Setup - No Local Git Required

Since Git is not installed on this computer, here's how to set up the repository on GitHub:

## Option 1: Manual Upload to GitHub

### 1. Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Repository name: `iron-dome-mosquitoes`
4. Description: `Iron Dome for Mosquitoes - Advanced Cat Detection and Mosquito Prevention System`
5. Make it **Public**
6. **DO NOT** initialize with README, .gitignore, or license
7. Click "Create repository"

### 2. Upload Files Manually
1. In the new repository, click "uploading an existing file"
2. Drag and drop all files from the `IronDomeMosquitoes` folder
3. Add commit message: "Initial commit: Iron Dome for Mosquitoes - Cat Detection System"
4. Click "Commit changes"

## Option 2: Install Git First

### Install Git on Windows
1. Download Git from: https://git-scm.com/download/win
2. Run the installer with default settings
3. Restart command prompt
4. Then run these commands:

```bash
cd IronDomeMosquitoes
git init
git add .
git commit -m "Initial commit: Iron Dome for Mosquitoes - Cat Detection System"
git remote add origin https://github.com/YOUR_USERNAME/iron-dome-mosquitoes.git
git branch -M main
git push -u origin main
```

## Option 3: Use GitHub Desktop

### Install GitHub Desktop
1. Download from: https://desktop.github.com/
2. Install and sign in to GitHub
3. Click "Clone a repository from the Internet"
4. Create new repository: `iron-dome-mosquitoes`
5. Choose local path: `C:\Users\Ariel\PycharmProjects\RaspberryPie\IronDomeMosquitoes`
6. Click "Create repository"
7. All files will be automatically added and committed

## Files to Include in Repository

### Core Files (Required)
- `src/` - All source code
- `config/config.yaml` - Configuration
- `requirements.txt` - Dependencies
- `test_cat_detection.py` - Test script
- `run_test.bat` - Windows batch file
- `README.md` - Main documentation
- `README_QUICK_START.md` - Quick start guide
- `GITHUB_SETUP.md` - GitHub setup instructions
- `.gitignore` - Git ignore rules

### Optional Files
- `models/yolov8n.pt` - YOLO model (large file, ~6MB)
- `data/` - Generated data (auto-created)

## After Repository is Created

### At Work Computer
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/iron-dome-mosquitoes.git
   cd iron-dome-mosquitoes
   ```

2. Install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run test:
   ```bash
   python test_cat_detection.py
   ```

## Repository Structure

```
iron-dome-mosquitoes/
├── src/
│   ├── core/system_manager.py
│   ├── detection/mosquito_detector.py
│   ├── camera/camera_manager.py
│   └── utils/
│       ├── logger.py
│       └── config_loader.py
├── config/config.yaml
├── test_cat_detection.py
├── run_test.bat
├── requirements.txt
├── README.md
├── README_QUICK_START.md
├── GITHUB_SETUP.md
└── .gitignore
```

## Quick Test Instructions

1. **Setup Phone Link:**
   - Open Phone Link on your PC
   - Click on 'Camera' in Phone Link
   - Take photos of your cats

2. **Run Test:**
   ```bash
   python test_cat_detection.py
   ```

3. **Expected Output:**
   - System detects cats in photos
   - Annotated images saved in `data/detections/`
   - Real-time logging of detections

## Next Steps

1. Create the GitHub repository using one of the options above
2. Clone at your work computer
3. Test cat detection with Phone Link
4. Switch to computer webcam when ready
5. Implement on Raspberry Pi for final deployment 