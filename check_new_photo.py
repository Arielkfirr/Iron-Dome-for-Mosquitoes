#!/usr/bin/env python3
"""
Check for New Photo
Immediately check for and process the photo that was just taken
"""

import os
import sys
import time
import cv2
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def check_for_new_photo():
    """Check for the new photo that was just taken"""
    print("📸 CHECKING FOR NEW PHOTO")
    print("=" * 40)
    
    try:
        # Import components
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        print("✅ Components imported successfully")
        
        # Load configuration
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        # Initialize detector
        detector = MosquitoDetector(config)
        detector.initialize()
        print("✅ Mosquito detector initialized")
        
        # Check captures folder
        capture_folder = "data/captures"
        if not os.path.exists(capture_folder):
            print(f"❌ Captures folder not found: {capture_folder}")
            return
        
        # Get current files
        current_files = os.listdir(capture_folder)
        image_files = [f for f in current_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"📸 Found {len(image_files)} image files:")
        for i, file in enumerate(image_files):
            file_path = os.path.join(capture_folder, file)
            file_size = os.path.getsize(file_path)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"   {i+1}. {file} ({file_size} bytes) - {file_time}")
        
        # Look for the specific photo you just took
        target_filename = "20250731_030450.jpg"
        target_files = [f for f in image_files if target_filename in f or "20250731" in f]
        
        if target_files:
            print(f"\n🎉 FOUND YOUR NEW PHOTO!")
            for file in target_files:
                file_path = os.path.join(capture_folder, file)
                file_size = os.path.getsize(file_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"\n📸 Processing: {file}")
                print(f"   📅 Taken at: {file_time}")
                print(f"   📏 Size: {file_size} bytes")
                
                # Process the photo
                try:
                    img = cv2.imread(file_path)
                    if img is not None:
                        print(f"   ✅ Image loaded ({img.shape[1]}x{img.shape[0]})")
                        
                        # Process with detector
                        detections = detector.detect(img)
                        
                        if detections:
                            print(f"🦟 Found {len(detections)} detections!")
                            for detection in detections:
                                class_name = detection.get('class_name', 'Unknown')
                                confidence = detection.get('confidence', 0)
                                print(f"   - {class_name}: {confidence:.3f}")
                        else:
                            print("✅ No mosquitoes detected in this photo")
                    else:
                        print("❌ Failed to load image")
                        
                except Exception as e:
                    print(f"❌ Error processing {file}: {e}")
        else:
            print(f"\n⚠️  Your new photo ({target_filename}) not found yet")
            print("📱 The photo might still be transferring from your phone")
            print("📱 Please check if Phone Link is properly connected")
        
        print(f"\n✅ Photo check completed!")
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_for_new_photo() 