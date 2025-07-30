# Iron Dome for Mosquitoes - Quick Start Guide 🦟🛡️

## Quick Setup

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run Cat Detection Test
```bash
# Run the test script
python test_cat_detection.py

# Or use the batch file (Windows)
run_test.bat
```

### 3. Phone Link Instructions
1. Open Phone Link on your PC
2. Click on 'Camera' in Phone Link
3. Take photos of your cats with your phone camera
4. The system will automatically detect cats in the photos
5. Press Ctrl+C to stop the test

## Project Structure
```
IronDomeMosquitoes/
├── src/                    # Source code
│   ├── core/              # Core system components
│   ├── detection/         # Detection algorithms
│   ├── camera/            # Camera management
│   └── utils/             # Utilities
├── config/                # Configuration files
├── models/                # AI models
├── data/                  # Data storage (auto-created)
├── test_cat_detection.py  # Test script
├── run_test.bat          # Windows batch file
└── requirements.txt       # Dependencies
```

## Configuration
Edit `config/config.yaml` to customize:
- Camera settings
- Detection sensitivity
- Model paths

## Next Steps
1. Test with your phone camera for cat detection
2. Switch to computer webcam when ready
3. Implement on Raspberry Pi for final deployment

## Support
- Check logs in `logs/` directory
- Review configuration in `config/config.yaml`
- Run health checks with the test script 