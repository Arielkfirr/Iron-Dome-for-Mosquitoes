#!/usr/bin/env python3
"""
Check and process the most recent photo
"""

import os
import sys
import cv2
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def check_latest_photo():
    """Find and process the most recent photo"""
    print("🔍 Checking for latest photo...")
    
    try:
        # Import components
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        # Load configuration
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        # Initialize detector
        detector = MosquitoDetector(config)
        detector.initialize()
        print("✅ Detector ready")
        
        # Check captures folder
        capture_folder = "data/captures"
        if os.path.exists(capture_folder):
            files = os.listdir(capture_folder)
            image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if image_files:
                # Get the most recent file by modification time
                latest_file = max(image_files, key=lambda f: os.path.getmtime(os.path.join(capture_folder, f)))
                latest_path = os.path.join(capture_folder, latest_file)
                file_size = os.path.getsize(latest_path)
                mod_time = os.path.getmtime(latest_path)
                
                print(f"📸 Latest photo: {latest_file}")
                print(f"   Size: {file_size} bytes")
                print(f"   Modified: {mod_time}")
                
                # Load and process the image
                img = cv2.imread(latest_path)
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
            else:
                print("❌ No image files found")
        else:
            print("❌ Captures folder not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_latest_photo() 