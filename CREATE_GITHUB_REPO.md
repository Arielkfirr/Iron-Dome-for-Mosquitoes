# Create GitHub Repository - Step by Step

## 1. Create Repository on GitHub

1. Go to https://github.com
2. Click "New repository" (green button)
3. Repository name: `iron-dome-mosquitoes`
4. Description: `Iron Dome for Mosquitoes - Advanced Cat Detection and Mosquito Prevention System`
5. Make it **Public** (so you can access it from work)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## 2. Connect Local Repository to GitHub

After creating the repository, run these commands in the IronDomeMosquitoes directory:

```bash
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/YOUR_USERNAME/iron-dome-mosquitoes.git
"C:\Program Files\Git\cmd\git.exe" push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## 3. Test the Connection

```bash
"C:\Program Files\Git\cmd\git.exe" status
```

## 4. Run the Sync Script

After the repository is connected, you can run the sync script:

```bash
python sync_phone_photos_to_git.py
```

This will automatically sync new phone photos every 10 minutes.

## 5. Clone at Work Computer

At your work computer:

```bash
git clone https://github.com/YOUR_USERNAME/iron-dome-mosquitoes.git
cd iron-dome-mosquitoes
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python test_cat_detection.py
```

## Repository Structure

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
├── sync_phone_photos_to_git.py    # Auto-sync script
├── run_test.bat                   # Windows batch file
├── requirements.txt                # Python dependencies
└── README_QUICK_START.md         # Quick start guide
```

## Next Steps

1. Create the GitHub repository using the steps above
2. Connect the local repository to GitHub
3. Test the sync script with phone photos
4. Clone at your work computer
5. Start testing cat detection!

---

**Note:** The sync script will automatically add and push only images from the last 2 minutes every 10 minutes. 