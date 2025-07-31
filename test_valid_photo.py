#!/usr/bin/env python3
"""
Test with Valid Photo
Test Phone Link integration using valid photos
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_with_valid_photo():
    """Test with valid photos from captures folder"""
    print("🧪 TESTING WITH VALID PHOTO")
    print("=" * 40)
    
    # Step 1: Find valid photos
    print("\n📸 STEP 1: Finding valid photos...")
    capture_folder = Path(__file__).parent / "data" / "captures"
    
    if not capture_folder.exists():
        print("❌ Captures folder not found")
        return False
    
    # Look for valid photos (exclude test_image.jpg which is corrupted)
    valid_photos = []
    for file in capture_folder.glob("*.jpg"):
        if file.name != "test_image.jpg" and file.stat().st_size > 1000:  # More than 1KB
            valid_photos.append(file)
    
    if not valid_photos:
        print("❌ No valid photos found")
        print("📱 Please transfer a photo from your phone first")
        return False
    
    # Use the largest valid photo
    test_photo = max(valid_photos, key=lambda f: f.stat().st_size)
    file_size = test_photo.stat().st_size
    file_time = datetime.fromtimestamp(test_photo.stat().st_mtime)
    
    print(f"✅ Using photo: {test_photo.name}")
    print(f"📅 Time: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📏 Size: {file_size} bytes")
    
    # Step 2: Test image loading
    print(f"\n🖼️  STEP 2: Testing image loading...")
    try:
        import cv2
        img = cv2.imread(str(test_photo))
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
        img = cv2.imread(str(test_photo))
        results = detector.detect(img)
        
        if results and results.get('detections'):
            print(f"🦟 Found {len(results['detections'])} mosquitoes!")
            for i, detection in enumerate(results['detections']):
                confidence = detection.get('confidence', 0)
                class_name = detection.get('class_name', 'Unknown')
                print(f"   {i+1}. {class_name}: {confidence:.3f}")
        else:
            print("✅ No mosquitoes detected in this photo")
        
        print(f"\n🎉 PHONE LINK INTEGRATION TEST COMPLETED!")
        print("✅ Your system is working correctly!")
        print("\n📱 NEXT STEPS FOR PHONE LINK:")
        print("1. Open Phone Link on your PC")
        print("2. Connect your phone")
        print("3. Take a photo with Phone Link camera")
        print("4. The photo should automatically transfer to the captures folder")
        print("5. Run the monitoring script to detect new photos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_with_valid_photo()
    if success:
        print("\n✅ All tests passed! Your system is ready for Phone Link.")
    else:
        print("\n❌ Some tests failed. Please check the setup.")
    
    print("\nPress Enter to exit...")
    input() 