#!/usr/bin/env python3
"""
Process phone link photos with correct method
"""

import os
import sys
import time
import cv2
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def process_phone_photos():
    """Process phone link photos with correct method"""
    print("🦟 Processing Phone Link Photos")
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
        
        # Process photos
        capture_folder = "data/captures"
        if os.path.exists(capture_folder):
            files = os.listdir(capture_folder)
            print(f"\n📸 Processing {len(files)} files from phone link:")
            
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(capture_folder, file)
                    file_size = os.path.getsize(file_path)
                    
                    print(f"\n🔍 Processing: {file} ({file_size} bytes)")
                    
                    try:
                        # Load image with OpenCV
                        img = cv2.imread(file_path)
                        if img is not None:
                            print(f"   ✅ Image loaded ({img.shape[1]}x{img.shape[0]})")
                            
                            # Process with detector using correct method
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
            print("❌ Captures folder not found")
            
        print("\n✅ Photo processing completed!")
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()

def monitor_new_photos():
    """Monitor for new photos in real-time"""
    print("🎯 Monitoring for NEW photos...")
    print("Take a photo with your phone camera now!")
    print("Press Ctrl+C to stop")
    
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
        
        # Monitor for new files
        capture_folder = "data/captures"
        processed_files = set()
        
        # Get initial files
        if os.path.exists(capture_folder):
            initial_files = set(os.listdir(capture_folder))
            processed_files.update(initial_files)
        
        while True:
            try:
                if os.path.exists(capture_folder):
                    current_files = set(os.listdir(capture_folder))
                    new_files = current_files - processed_files
                    
                    for file in new_files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                            file_path = os.path.join(capture_folder, file)
                            file_size = os.path.getsize(file_path)
                            
                            print(f"\n📸 NEW PHOTO DETECTED: {file} ({file_size} bytes)")
                            
                            try:
                                # Load and process image
                                img = cv2.imread(file_path)
                                if img is not None:
                                    print(f"   ✅ Processing new photo ({img.shape[1]}x{img.shape[0]})")
                                    
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
                                    print("❌ Failed to load new photo")
                                    
                            except Exception as e:
                                print(f"❌ Error processing new photo: {e}")
                            
                            processed_files.add(file)
                
                time.sleep(1)  # Check every second
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                break
                
    except Exception as e:
        print(f"❌ Monitoring failed: {e}")

if __name__ == "__main__":
    print("Choose option:")
    print("1. Process existing photos")
    print("2. Monitor for new photos")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        process_phone_photos()
    elif choice == "2":
        monitor_new_photos()
    else:
        print("Invalid choice") 