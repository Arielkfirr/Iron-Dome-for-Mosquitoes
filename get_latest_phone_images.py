#!/usr/bin/env python3
"""
Get Latest Phone Images
Captures and processes the most recent images from your phone camera
"""

import os
import sys
import time
import cv2
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def get_latest_phone_images():
    """Get and process the latest images from phone camera"""
    print("📱 Getting Latest Phone Images")
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
            print("📱 Please take a photo with your phone camera first!")
            return
        
        # Get all image files
        image_files = []
        for file in os.listdir(capture_folder):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(capture_folder, file)
                file_time = os.path.getmtime(file_path)
                image_files.append((file, file_path, file_time))
        
        if not image_files:
            print("❌ No images found in captures folder")
            print("📱 Please take a photo with your phone camera first!")
            return
        
        # Sort by modification time (newest first)
        image_files.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\n📸 Found {len(image_files)} images:")
        for i, (file, file_path, file_time) in enumerate(image_files[:5]):  # Show last 5
            file_size = os.path.getsize(file_path)
            file_date = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"   {i+1}. {file} ({file_size} bytes) - {file_date}")
        
        # Process the latest image
        latest_file, latest_path, latest_time = image_files[0]
        print(f"\n🔍 Processing latest image: {latest_file}")
        
        try:
            # Load image with OpenCV
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
                
        except Exception as e:
            print(f"❌ Error processing {latest_file}: {e}")
        
        print(f"\n✅ Latest image processing completed!")
        print(f"📱 Take another photo with your phone to get more images!")
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()

def monitor_for_new_images():
    """Monitor for new images from phone camera"""
    print("🎯 Monitoring for NEW phone images...")
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
        
        print("📱 Ready to capture new photos!")
        print("📱 Instructions:")
        print("   1. Open Phone Link on your PC")
        print("   2. Click on 'Camera' in Phone Link")
        print("   3. Take photos with your phone camera")
        print("   4. Watch for real-time detection results!")
        
        while True:
            try:
                if os.path.exists(capture_folder):
                    current_files = set(os.listdir(capture_folder))
                    new_files = current_files - processed_files
                    
                    for file in new_files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                            file_path = os.path.join(capture_folder, file)
                            file_size = os.path.getsize(file_path)
                            file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%H:%M:%S')
                            
                            print(f"\n📸 NEW PHOTO DETECTED: {file} ({file_size} bytes) at {file_time}")
                            
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
    print("📱 Phone Image Capture Options:")
    print("1. Process latest existing images")
    print("2. Monitor for new phone images")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        get_latest_phone_images()
    elif choice == "2":
        monitor_for_new_images()
    else:
        print("Invalid choice") 