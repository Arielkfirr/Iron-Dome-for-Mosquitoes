#!/usr/bin/env python3
"""
Transfer and Test Photo
Help transfer the photo from your phone and test it
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def transfer_and_test_photo():
    """Transfer photo from phone and test it"""
    print("📱 TRANSFER AND TEST PHOTO")
    print("=" * 40)
    
    # Step 1: Check for the specific photo
    print("\n📸 STEP 1: Looking for your photo...")
    target_filename = "20250731_030450.jpg"
    
    # Check common Phone Link locations
    possible_locations = [
        Path.home() / "Pictures" / "Phone Link",
        Path.home() / "Downloads" / "Phone Link",
        Path.home() / "Documents" / "Phone Link",
        Path.home() / "OneDrive" / "Pictures" / "Phone Link",
        Path.home() / "Desktop" / "Phone Link",
    ]
    
    found_photo = None
    for location in possible_locations:
        if location.exists():
            photo_path = location / target_filename
            if photo_path.exists():
                found_photo = photo_path
                print(f"✅ Found photo at: {photo_path}")
                break
    
    if not found_photo:
        print(f"❌ Photo {target_filename} not found in common locations")
        print("\n📱 MANUAL TRANSFER INSTRUCTIONS:")
        print("1. Open Phone Link on your PC")
        print("2. Go to Photos section")
        print("3. Find the photo: 20250731_030450.jpg")
        print("4. Right-click and 'Save as' to:")
        print(f"   {Path(__file__).parent / 'data' / 'captures' / target_filename}")
        print("\n5. Or copy the photo to the captures folder manually")
        
        # Wait for manual transfer
        input("\nPress Enter after you've transferred the photo...")
        
        # Check if photo was transferred
        capture_folder = Path(__file__).parent / "data" / "captures"
        photo_path = capture_folder / target_filename
        if photo_path.exists():
            found_photo = photo_path
            print(f"✅ Photo found at: {photo_path}")
        else:
            print("❌ Photo still not found")
            return False
    
    # Step 2: Copy to captures folder if needed
    capture_folder = Path(__file__).parent / "data" / "captures"
    target_path = capture_folder / target_filename
    
    if found_photo != target_path:
        print(f"\n📁 STEP 2: Copying photo to captures folder...")
        shutil.copy2(found_photo, target_path)
        print(f"✅ Photo copied to: {target_path}")
    
    # Step 3: Test the photo
    print(f"\n🧪 STEP 3: Testing photo...")
    file_size = target_path.stat().st_size
    file_time = datetime.fromtimestamp(target_path.stat().st_mtime)
    
    print(f"📸 Photo: {target_filename}")
    print(f"📅 Time: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📏 Size: {file_size} bytes")
    
    # Step 4: Test image loading
    print(f"\n🖼️  STEP 4: Testing image loading...")
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
    
    # Step 5: Test mosquito detection
    print(f"\n🦟 STEP 5: Testing mosquito detection...")
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
        
        print(f"\n🎉 PHOTO TEST COMPLETED SUCCESSFULLY!")
        print("✅ Your Phone Link photo is working!")
        return True
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = transfer_and_test_photo()
    if success:
        print("\n✅ All tests passed! Your photo is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the setup.")
    
    print("\nPress Enter to exit...")
    input() 