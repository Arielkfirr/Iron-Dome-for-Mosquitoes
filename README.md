# Iron Dome for Mosquitoes 🦟🛡️

A sophisticated cat detection and mosquito prevention system using computer vision and AI.

## 🎯 Current Status: Cat Detection Testing Phase

**Ready for testing with your phone camera!**

### What's Working Now:
- ✅ Phone Link integration for photo capture
- ✅ YOLO-based cat detection
- ✅ Automatic image processing
- ✅ Annotated image saving
- ✅ Real-time logging

### Next Phases:
1. **Phase 1:** Cat detection with Phone Link (Current)
2. **Phase 2:** Computer webcam integration
3. **Phase 3:** Raspberry Pi deployment
4. **Phase 4:** Mosquito detection and prevention

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Test Cat Detection
```bash
# Run test script
python test_cat_detection.py

# Or use batch file (Windows)
run_test.bat
```

### 3. Phone Link Instructions
1. Open Phone Link on your PC
2. Click on 'Camera' in Phone Link
3. Take photos of your cats with your phone camera
4. System will automatically detect cats in the photos
5. Press Ctrl+C to stop the test

## 📁 Project Structure

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

## 🔧 Configuration

Edit `config/config.yaml` to customize:
- Camera settings
- Detection sensitivity
- Model paths
- Logging preferences

## 📊 Expected Output

When you run the test:
- System monitors Phone Link folder for new images
- Automatically detects cats in photos
- Saves annotated images in `data/detections/`
- Provides real-time logging of detections
- Shows confidence scores and bounding boxes

## 🎯 Testing Your Cats

1. **Setup:** Run the test script
2. **Capture:** Take photos of your cats using Phone Link
3. **Monitor:** Watch real-time detection results
4. **Review:** Check annotated images in `data/detections/`

## 🔄 Development Roadmap

### Phase 1: Cat Detection (Current)
- ✅ Phone Link integration
- ✅ YOLO model loading
- ✅ Image processing pipeline
- ✅ Detection results logging

### Phase 2: Computer Webcam
- 🔄 USB camera integration
- 🔄 Real-time video processing
- 🔄 Performance optimization

### Phase 3: Raspberry Pi
- 🔄 Pi camera integration
- 🔄 Lightweight model optimization
- 🔄 Remote monitoring

### Phase 4: Mosquito Detection
- 🔄 Mosquito-specific model training
- 🔄 Prevention mechanisms
- 🔄 Alert systems

## 🛠️ Technical Details

### Detection Engine
- **Model:** YOLOv8n (ultralytics)
- **Classes:** cat, mosquito, insect, fly
- **Confidence Threshold:** 0.3 (configurable)
- **Processing:** Real-time image analysis

### Camera Integration
- **Phone Link:** Automatic folder monitoring
- **USB Camera:** Direct capture support
- **IP Camera:** Network camera support

### Logging & Monitoring
- **Real-time logs:** Console and file output
- **Detection tracking:** Timestamp and confidence
- **Image annotation:** Bounding boxes and labels

## 📝 Support

- **Quick Start:** See `README_QUICK_START.md`
- **GitHub Setup:** See `GITHUB_SETUP.md`
- **Configuration:** Edit `config/config.yaml`
- **Logs:** Check `logs/` directory

## 🎉 Ready to Test!

Your Iron Dome for Mosquitoes system is ready for cat detection testing. Start with the test script and take some photos of your cats!

---

**Iron Dome for Mosquitoes** - Protecting your space from unwanted guests! 🦟🛡️ 