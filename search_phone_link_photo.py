#!/usr/bin/env python3
"""
Search Phone Link Photo
Search for the photo in Phone Link locations and test integration
"""

import os
import sys
import shutil
import glob
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def search_phone_link_photo():
    """Search for the photo in Phone Link locations"""
    print("🔍 SEARCHING PHONE LINK PHOTO")
    print("=" * 50)
    
    target_filename = "20250731_030450.jpg"
    
    # Common Phone Link locations
    search_locations = [
        # User directories
        Path.home() / "Pictures" / "Phone Link",
        Path.home() / "Downloads" / "Phone Link",
        Path.home() / "Documents" / "Phone Link",
        Path.home() / "Desktop" / "Phone Link",
        Path.home() / "OneDrive" / "Pictures" / "Phone Link",
        Path.home() / "OneDrive" / "Downloads" / "Phone Link",
        
        # Phone Link specific folders
        Path.home() / "AppData" / "Local" / "Microsoft" / "Phone Link",
        Path.home() / "AppData" / "Roaming" / "Microsoft" / "Phone Link",
        
        # Windows Phone Link folders
        Path("C:/Users/Public/Pictures/Phone Link"),
        Path("C:/Users/Public/Downloads/Phone Link"),
        
        # Project folders
        Path(__file__).parent / "data" / "captures",
        Path(__file__).parent / "phone_captures",
        
        # Additional search paths
        Path.home() / "Pictures",
        Path.home() / "Downloads",
        Path.home() / "Documents",
        Path.home() / "Desktop",
    ]
    
    print(f"🔍 Searching for: {target_filename}")
    print(f"📁 Searching in {len(search_locations)} locations...")
    
    found_photos = []
    
    for location in search_locations:
        if location.exists():
            print(f"📂 Checking: {location}")
            
            # Search for exact filename
            exact_path = location / target_filename
            if exact_path.exists():
                found_photos.append(exact_path)
                print(f"✅ Found exact match: {exact_path}")
            
            # Search for similar filenames
            try:
                for file_path in location.glob(f"*{target_filename.split('_')[0]}*"):
                    if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        if file_path not in found_photos:
                            found_photos.append(file_path)
                            print(f"✅ Found similar: {file_path}")
            except Exception as e:
                print(f"⚠️  Error searching {location}: {e}")
    
    # Also search for any recent photos
    print(f"\n🔍 Searching for recent photos...")
    for location in search_locations:
        if location.exists():
            try:
                for file_path in location.glob("*.jpg"):
                    if file_path.is_file():
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_time.date() == datetime.now().date():  # Today's photos
                            if file_path not in found_photos:
                                found_photos.append(file_path)
                                print(f"✅ Found recent: {file_path.name} ({file_time.strftime('%H:%M')})")
            except Exception as e:
                pass
    
    if not found_photos:
        print(f"\n❌ No photos found")
        print("\n📱 PHONE LINK INTEGRATION SETUP:")
        print("1. Open Phone Link on your PC")
        print("2. Make sure your phone is connected")
        print("3. Go to Photos section")
        print("4. Find your photo: 20250731_030450.jpg")
        print("5. Right-click and 'Save as' to your project folder")
        return False
    
    print(f"\n✅ Found {len(found_photos)} photos")
    
    # Test the first found photo
    test_photo = found_photos[0]
    print(f"\n🧪 Testing photo: {test_photo.name}")
    
    return test_phone_link_integration(test_photo)

def test_phone_link_integration(photo_path):
    """Test Phone Link integration with the found photo"""
    print(f"\n📱 TESTING PHONE LINK INTEGRATION")
    print("=" * 50)
    
    # Step 1: Copy to captures folder
    print(f"\n📁 STEP 1: Copying to captures folder...")
    capture_folder = Path(__file__).parent / "data" / "captures"
    target_path = capture_folder / photo_path.name
    
    if photo_path != target_path:
        shutil.copy2(photo_path, target_path)
        print(f"✅ Copied to: {target_path}")
    
    # Step 2: Test image loading
    print(f"\n🖼️  STEP 2: Testing image loading...")
    try:
        import cv2
        img = cv2.imread(str(target_path))
        if img is not None:
            print(f"✅ Image loaded successfully ({img.shape[1]}x{img.shape[0]})")
        else:
            print("❌ Failed to load image")
            return False
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return False
    
    # Step 3: Test mosquito detection
    print(f"\n🦟 STEP 3: Testing mosquito detection...")
    try:
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        print("✅ Components imported successfully")
        
        # Load configuration
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        print("✅ Configuration loaded")
        
        # Initialize detector
        detector = MosquitoDetector(config)
        detector.initialize()
        print("✅ Mosquito detector initialized")
        
        # Process the image
        results = detector.detect_image(str(target_path))
        
        if results and results.get('detections'):
            print(f"🦟 Found {len(results['detections'])} mosquitoes!")
            for i, detection in enumerate(results['detections']):
                confidence = detection.get('confidence', 0)
                class_name = detection.get('class_name', 'Unknown')
                print(f"   {i+1}. {class_name}: {confidence:.3f}")
        else:
            print("✅ No mosquitoes detected in this photo")
        
        print(f"\n🎉 PHONE LINK INTEGRATION TEST COMPLETED!")
        print("✅ Phone Link integration is working!")
        return True
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        import traceback
        traceback.print_exc()
        return False

def setup_phone_link_monitoring():
    """Set up continuous monitoring for Phone Link photos"""
    print(f"\n📱 SETTING UP PHONE LINK MONITORING")
    print("=" * 50)
    
    # Create monitoring script
    monitor_script = Path(__file__).parent / "phone_link_monitor.py"
    
    script_content = '''#!/usr/bin/env python3
"""
Phone Link Monitor
Automatically monitors for new photos from Phone Link
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def monitor_phone_link_photos():
    """Monitor for new photos from Phone Link"""
    print("📱 PHONE LINK PHOTO MONITOR")
    print("=" * 40)
    
    capture_folder = Path(__file__).parent / "data" / "captures"
    processed_files = set()
    
    print(f"📁 Monitoring: {capture_folder}")
    print("📱 Take photos with Phone Link camera")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        while True:
            if capture_folder.exists():
                current_files = set(os.listdir(capture_folder))
                new_files = current_files - processed_files
                
                for file in new_files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        file_path = capture_folder / file
                        file_size = file_path.stat().st_size
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        
                        print(f"\\n📸 NEW PHOTO: {file}")
                        print(f"   📅 Time: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"   📏 Size: {file_size} bytes")
                        
                        # Process the photo
                        try:
                            from detection.mosquito_detector import MosquitoDetector
                            from utils.config_loader import ConfigLoader
                            
                            config_loader = ConfigLoader("config/config.yaml")
                            config = config_loader.load()
                            
                            detector = MosquitoDetector(config)
                            detector.initialize()
                            
                            results = detector.detect_image(str(file_path))
                            if results and results.get('detections'):
                                print(f"🦟 Found {len(results['detections'])} mosquitoes!")
                                for detection in results['detections']:
                                    confidence = detection.get('confidence', 0)
                                    print(f"   - Confidence: {confidence:.3f}")
                            else:
                                print("✅ No mosquitoes detected")
                                
                        except Exception as e:
                            print(f"❌ Error processing photo: {e}")
                        
                        processed_files.add(file)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\\n🛑 Monitoring stopped")

if __name__ == "__main__":
    monitor_phone_link_photos()
'''
    
    with open(monitor_script, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Created monitoring script: {monitor_script}")
    print("\n📋 TO USE PHONE LINK:")
    print("1. Run: python phone_link_monitor.py")
    print("2. Take photos with Phone Link camera")
    print("3. Watch for automatic detection")

if __name__ == "__main__":
    success = search_phone_link_photo()
    
    if success:
        print("\n✅ Phone Link integration is working!")
        setup_phone_link_monitoring()
    else:
        print("\n❌ Phone Link integration needs setup")
        print("📱 Please follow the Phone Link setup instructions")
    
    print("\nPress Enter to exit...")
    input() 