#!/usr/bin/env python3
"""
Demo script for IronDome Mosquitoes Phone Camera Integration
Perfect for showing to friends at work!
"""

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def demo_phone_camera_integration():
    """Demo the phone camera integration"""
    print("🦟 IronDome Mosquitoes - Phone Camera Demo")
    print("=" * 50)
    print("📱 This system uses your PHONE camera, not webcam!")
    print("=" * 50)
    
    try:
        # Import components
        from utils.config_loader import ConfigLoader
        from camera.camera_manager import CameraManager
        from detection.mosquito_detector import MosquitoDetector
        from utils.logger import get_logger
        
        print("✅ All components imported successfully!")
        
        # Load configuration
        print("\n📋 Loading configuration...")
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        if config:
            print("✅ Configuration loaded!")
            print(f"   - Phone Link enabled: {config.get('camera', {}).get('phone_link', {}).get('enabled', False)}")
            print(f"   - Detection confidence: {config.get('detection', {}).get('confidence_threshold', 0.3)}")
            print(f"   - Model path: {config.get('detection', {}).get('model_path', 'Not found')}")
        
        # Initialize logger
        print("\n📝 Setting up logging...")
        logger = get_logger("demo")
        logger.info("Demo started - Phone camera integration")
        
        # Initialize camera manager
        print("\n📷 Initializing camera manager...")
        camera_manager = CameraManager(config)
        camera_manager.initialize()
        
        print("✅ Camera manager ready!")
        print("\n📱 PHONE CAMERA SETUP:")
        print("1. Open Phone Link on your PC")
        print("2. Click on 'Camera' in Phone Link")
        print("3. Take photos with your phone camera")
        print("4. Photos will be automatically detected!")
        
        # Initialize detector
        print("\n🔍 Initializing mosquito detector...")
        detector = MosquitoDetector(config)
        detector.initialize()
        
        print("✅ Mosquito detector ready!")
        
        # Demo the system
        print("\n🎯 DEMO MODE:")
        print("The system will now monitor for phone camera captures...")
        print("Take a photo with your phone camera to see it in action!")
        print("Press Ctrl+C to stop the demo")
        
        # Monitor for new captures
        capture_folder = config.get('camera', {}).get('phone_link', {}).get('capture_folder', 'data/captures')
        processed_files = set()
        
        while True:
            try:
                # Check for new files
                if os.path.exists(capture_folder):
                    files = os.listdir(capture_folder)
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png')) and file not in processed_files:
                            file_path = os.path.join(capture_folder, file)
                            print(f"\n📸 New photo detected: {file}")
                            
                            # Process the image
                            try:
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
                
                time.sleep(1)  # Check every second
                
            except KeyboardInterrupt:
                print("\n\n🛑 Demo stopped by user")
                break
            except Exception as e:
                print(f"❌ Demo error: {e}")
                break
        
        print("\n✅ Demo completed successfully!")
        print("🎉 Ready to show to your friends at work!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Please check the system setup")

if __name__ == "__main__":
    demo_phone_camera_integration() 