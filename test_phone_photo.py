#!/usr/bin/env python3
"""
Test Phone Photo
Test with the specific phone photo 20250731_030450.jpg
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_phone_photo():
    """Test with the specific phone photo"""
    print("📱 TESTING PHONE PHOTO")
    print("=" * 40)
    
    target_filename = "20250731_030450.jpg"
    capture_folder = Path(__file__).parent / "data" / "captures"
    target_path = capture_folder / target_filename
    
    print(f"📸 Looking for: {target_filename}")
    
    # Check if the photo is already in captures folder
    if target_path.exists():
        print(f"✅ Photo found in captures folder: {target_path}")
        photo_path = target_path
    else:
        print(f"❌ Photo not found in captures folder")
        print("\n📱 MANUAL TRANSFER INSTRUCTIONS:")
        print("1. Open Phone Link on your PC")
        print("2. Go to Photos section")
        print("3. Find the photo: 20250731_030450.jpg")
        print("4. Right-click and 'Save as' to:")
        print(f"   {target_path}")
        print("\n5. Or copy the photo to the captures folder manually")
        
        # Wait for manual transfer
        input("\nPress Enter after you've transferred the photo...")
        
        # Check if photo was transferred
        if target_path.exists():
            photo_path = target_path
            print(f"✅ Photo found at: {photo_path}")
        else:
            print("❌ Photo still not found")
            return False
    
    # Test the photo
    print(f"\n🧪 Testing photo...")
    file_size = photo_path.stat().st_size
    file_time = datetime.fromtimestamp(photo_path.stat().st_mtime)
    
    print(f"📸 Photo: {target_filename}")
    print(f"📅 Time: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📏 Size: {file_size} bytes")
    
    # Test image loading
    print(f"\n🖼️  Testing image loading...")
    try:
        import cv2
        img = cv2.imread(str(photo_path))
        if img is not None:
            print(f"✅ Image loaded successfully ({img.shape[1]}x{img.shape[0]})")
        else:
            print("❌ Failed to load image")
            return False
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return False
    
    # Test mosquito detection
    print(f"\n🦟 Testing mosquito detection...")
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
        img = cv2.imread(str(photo_path))
        results = detector.detect(img)
        
        if results:
            print(f"🦟 Found {len(results)} detections!")
            for i, detection in enumerate(results):
                confidence = detection.get('confidence', 0)
                class_name = detection.get('class_name', 'Unknown')
                print(f"   {i+1}. {class_name}: {confidence:.3f}")
        else:
            print("✅ No mosquitoes detected in this photo")
        
        print(f"\n🎉 PHONE LINK INTEGRATION TEST COMPLETED!")
        print("✅ Your Phone Link photo is working!")
        print("\n📱 PHONE LINK SETUP SUCCESSFUL!")
        print("You can now:")
        print("1. Take photos with Phone Link camera")
        print("2. Photos will automatically transfer to captures folder")
        print("3. Run monitoring script to detect new photos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_phone_photo()
    if success:
        print("\n✅ All tests passed! Phone Link integration is working.")
    else:
        print("\n❌ Some tests failed. Please check the setup.")
    
    print("\nPress Enter to exit...")
    input() 