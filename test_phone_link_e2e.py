#!/usr/bin/env python3
"""
End-to-End Phone Link Test
Automatically test Phone Link integration without user choices
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_phone_link_e2e():
    """Run end-to-end Phone Link test"""
    print("🧪 PHONE LINK END-TO-END TEST")
    print("=" * 50)
    
    # Step 1: Check capture folder
    print("\n📁 STEP 1: Checking capture folder...")
    capture_folder = Path(__file__).parent / "data" / "captures"
    
    if not capture_folder.exists():
        print("❌ Capture folder not found, creating...")
        capture_folder.mkdir(parents=True, exist_ok=True)
        print("✅ Capture folder created")
    else:
        print("✅ Capture folder exists")
    
    # Step 2: Check for photos
    print("\n📸 STEP 2: Checking for photos...")
    files = os.listdir(capture_folder)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📸 Found {len(image_files)} photos in capture folder")
    
    if not image_files:
        print("⚠️  No photos found")
        print("📱 Please take a photo with Phone Link camera")
        print("⏳ Waiting 10 seconds for photo transfer...")
        
        # Wait for new photos
        initial_files = set(files)
        for i in range(10):
            current_files = set(os.listdir(capture_folder))
            new_files = current_files - initial_files
            new_images = [f for f in new_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if new_images:
                print(f"✅ New photo detected: {new_images[0]}")
                image_files = new_images
                break
            
            print(f"⏳ {10-i} seconds remaining...")
            time.sleep(1)
        else:
            print("❌ No new photos detected")
            return False
    
    # Step 3: Process the latest photo
    print("\n🔍 STEP 3: Processing latest photo...")
    latest_file = max(image_files, key=lambda f: os.path.getmtime(capture_folder / f))
    file_path = capture_folder / latest_file
    file_size = file_path.stat().st_size
    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
    
    print(f"📸 Processing: {latest_file}")
    print(f"📅 Taken: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📏 Size: {file_size} bytes")
    
    # Step 4: Test image loading
    print("\n🖼️  STEP 4: Testing image loading...")
    try:
        import cv2
        img = cv2.imread(str(file_path))
        if img is not None:
            print(f"✅ Image loaded successfully ({img.shape[1]}x{img.shape[0]})")
        else:
            print("❌ Failed to load image")
            return False
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return False
    
    # Step 5: Test mosquito detection
    print("\n🦟 STEP 5: Testing mosquito detection...")
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
        results = detector.detect_image(str(file_path))
        
        if results and results.get('detections'):
            print(f"🦟 Found {len(results['detections'])} mosquitoes!")
            for i, detection in enumerate(results['detections']):
                confidence = detection.get('confidence', 0)
                class_name = detection.get('class_name', 'Unknown')
                print(f"   {i+1}. {class_name}: {confidence:.3f}")
        else:
            print("✅ No mosquitoes detected in this photo")
        
        print("\n🎉 END-TO-END TEST COMPLETED SUCCESSFULLY!")
        print("✅ Phone Link integration is working!")
        return True
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_phone_link_e2e()
    if success:
        print("\n✅ All tests passed! Phone Link is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the setup.")
    
    print("\nPress Enter to exit...")
    input() 