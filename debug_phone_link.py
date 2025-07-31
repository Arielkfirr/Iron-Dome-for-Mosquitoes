#!/usr/bin/env python3
"""
Debug script for Phone Link image processing
"""

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def debug_phone_link():
    """Debug phone link image processing"""
    print("🔍 Debugging Phone Link Image Processing")
    print("=" * 50)
    
    try:
        # Import components
        from utils.config_loader import ConfigLoader
        from camera.camera_manager import CameraManager
        from detection.mosquito_detector import MosquitoDetector
        from utils.logger import get_logger
        
        print("✅ Components imported successfully")
        
        # Load configuration
        print("\n📋 Loading configuration...")
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        if config:
            print("✅ Configuration loaded")
            phone_link_config = config.get('camera', {}).get('phone_link', {})
            print(f"   - Phone Link enabled: {phone_link_config.get('enabled', False)}")
            print(f"   - Capture folder: {phone_link_config.get('capture_folder', 'Not found')}")
        
        # Initialize logger
        print("\n📝 Setting up logger...")
        logger = get_logger("debug_phone_link")
        
        # Initialize camera manager
        print("\n📷 Initializing camera manager...")
        camera_manager = CameraManager(config)
        camera_manager.initialize()
        
        # Initialize detector
        print("\n🔍 Initializing mosquito detector...")
        detector = MosquitoDetector(config)
        detector.initialize()
        
        print("✅ All components initialized")
        
        # Check capture folder
        capture_folder = config.get('camera', {}).get('phone_link', {}).get('capture_folder', 'data/captures')
        print(f"\n📁 Checking capture folder: {capture_folder}")
        
        if os.path.exists(capture_folder):
            print("✅ Capture folder exists")
            files = os.listdir(capture_folder)
            print(f"📸 Found {len(files)} files:")
            
            for file in files:
                file_path = os.path.join(capture_folder, file)
                file_size = os.path.getsize(file_path)
                print(f"   - {file} ({file_size} bytes)")
                
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(f"     🔍 Processing image: {file}")
                    
                    try:
                        # Test if image can be read
                        import cv2
                        img = cv2.imread(file_path)
                        if img is not None:
                            print(f"     ✅ Image loaded successfully ({img.shape[1]}x{img.shape[0]})")
                            
                            # Process with detector
                            results = detector.detect_image(file_path)
                            if results:
                                print(f"     ✅ Detection completed")
                                if results.get('detections'):
                                    print(f"     🦟 Found {len(results['detections'])} detections")
                                    for detection in results['detections']:
                                        print(f"        - Confidence: {detection.get('confidence', 0):.3f}")
                                else:
                                    print(f"     ✅ No mosquitoes detected")
                            else:
                                print(f"     ❌ Detection returned None")
                        else:
                            print(f"     ❌ Failed to load image")
                            
                    except Exception as e:
                        print(f"     ❌ Error processing {file}: {e}")
        else:
            print("❌ Capture folder does not exist")
            print("Creating capture folder...")
            os.makedirs(capture_folder, exist_ok=True)
            print("✅ Capture folder created")
        
        # Monitor for new files
        print(f"\n🎯 Monitoring for new files in {capture_folder}")
        print("Take a photo with your phone camera now...")
        print("Press Ctrl+C to stop monitoring")
        
        processed_files = set()
        last_check = time.time()
        
        while True:
            try:
                current_time = time.time()
                
                # Check for new files every second
                if current_time - last_check >= 1:
                    if os.path.exists(capture_folder):
                        files = os.listdir(capture_folder)
                        for file in files:
                            if file.lower().endswith(('.jpg', '.jpeg', '.png')) and file not in processed_files:
                                file_path = os.path.join(capture_folder, file)
                                file_size = os.path.getsize(file_path)
                                
                                print(f"\n📸 NEW PHOTO DETECTED: {file} ({file_size} bytes)")
                                
                                try:
                                    # Process the image
                                    results = detector.detect_image(file_path)
                                    if results and results.get('detections'):
                                        print(f"🦟 Found {len(results['detections'])} mosquitoes!")
                                        for detection in results['detections']:
                                            print(f"   - Confidence: {detection.get('confidence', 0):.3f}")
                                    else:
                                        print("✅ No mosquitoes detected in this photo")
                                    
                                    processed_files.add(file)
                                    
                                except Exception as e:
                                    print(f"❌ Error processing image: {e}")
                    
                    last_check = current_time
                
                time.sleep(0.1)  # Check every 100ms
                
            except KeyboardInterrupt:
                print("\n\n🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                break
        
        print("\n✅ Debug completed")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_phone_link() 