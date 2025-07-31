# Phone Link Integration Guide

This guide will help you set up Phone Link to work with your Iron Dome Mosquitoes detection system in Cursor.

## 📱 What is Phone Link?

Phone Link (formerly Your Phone) is a Microsoft app that allows you to:
- Connect your Android phone to your Windows PC
- Use your phone's camera from your PC
- Transfer photos automatically
- Control your phone from your PC

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
1. Double-click `setup_phone_link.bat` in the IronDomeMosquitoes folder
2. Follow the on-screen instructions
3. Choose option 1 for complete setup

### Option 2: Manual Setup
1. Run: `python phone_link_cursor_setup.py`
2. Choose option 1 for complete setup
3. Follow the step-by-step instructions

## 📋 Step-by-Step Manual Setup

### Step 1: Install Phone Link
1. Open Microsoft Store on your PC
2. Search for "Phone Link"
3. Click "Install"
4. Wait for installation to complete

### Step 2: Connect Your Phone
1. Open Phone Link on your PC
2. Make sure your phone is on the same WiFi network
3. Follow the pairing instructions
4. Grant necessary permissions on your phone
5. Verify connection status shows "Connected"

### Step 3: Enable Camera Feature
1. In Phone Link, click on "Camera"
2. Grant camera permissions if prompted
3. You should see your phone's camera view
4. Test taking a photo

### Step 4: Configure Photo Transfer
1. Photos taken via Phone Link will automatically save to:
   ```
   C:\Users\Ariel\PycharmProjects\RaspberryPie\IronDomeMosquitoes\data\captures
   ```
2. The system will automatically detect new photos
3. Each photo will be processed for mosquito detection

## 🧪 Testing the Setup

### Quick Test
1. Run: `python phone_link_cursor_setup.py`
2. Choose option 2 for quick test
3. Take a photo with Phone Link camera
4. Check if the photo appears and can be processed

### Continuous Monitoring
1. Run: `python phone_link_monitor.py`
2. Take photos with Phone Link camera
3. Watch for automatic detection results
4. Press Ctrl+C to stop monitoring

## 📁 File Structure

```
IronDomeMosquitoes/
├── phone_link_cursor_setup.py    # Main setup script
├── phone_link_monitor.py         # Continuous monitoring
├── setup_phone_link.bat          # Easy setup batch file
├── data/
│   └── captures/                 # Photos from Phone Link
└── config/
    └── config.yaml               # Configuration file
```

## ⚙️ Configuration

The Phone Link settings are configured in `config/config.yaml`:

```yaml
camera:
  phone_link:
    enabled: true
    capture_folder: "data/captures"
    auto_save: true
```

## 🔧 Troubleshooting

### Phone Link Not Found
- Make sure Phone Link is installed from Microsoft Store
- Check if your Windows version supports Phone Link
- Try restarting your PC

### Connection Issues
- Ensure both devices are on the same WiFi network
- Check firewall settings
- Try disconnecting and reconnecting your phone

### Photo Transfer Not Working
- Check if Phone Link camera permissions are granted
- Verify the capture folder exists: `data/captures`
- Try taking a test photo manually

### Detection Not Working
- Check if the YOLO model file exists: `models/yolov8n.pt`
- Verify Python dependencies are installed
- Check the logs for error messages

## 📱 Using Phone Link

### Taking Photos
1. Open Phone Link on your PC
2. Click on "Camera"
3. Use your phone's camera to take photos
4. Photos will automatically transfer to the captures folder

### Monitoring Results
1. Run the monitoring script: `python phone_link_monitor.py`
2. Take photos with Phone Link
3. Watch for detection results in real-time

### Manual Photo Processing
1. Place photos in the `data/captures` folder
2. Run: `python check_new_photo.py`
3. Check the results

## 🎯 Advanced Features

### Custom Capture Folder
Edit `config/config.yaml` to change the capture folder:
```yaml
camera:
  phone_link:
    capture_folder: "your/custom/path"
```

### Detection Settings
Adjust detection sensitivity in `config/config.yaml`:
```yaml
detection:
  confidence_threshold: 0.3  # Lower = more sensitive
  iou_threshold: 0.5
```

### Logging
Check logs in the `logs/` folder for detailed information about:
- Photo transfers
- Detection results
- Error messages

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs in the `logs/` folder
3. Run the debug script: `python debug_phone_link.py`
4. Check the configuration file: `config/config.yaml`

## 🎉 Success Indicators

You'll know Phone Link is working when:
- ✅ Phone Link shows "Connected" status
- ✅ Camera view appears in Phone Link
- ✅ Photos transfer to the captures folder
- ✅ Detection results appear when processing photos
- ✅ Monitoring script detects new photos automatically

Happy mosquito hunting! 🦟🔍 