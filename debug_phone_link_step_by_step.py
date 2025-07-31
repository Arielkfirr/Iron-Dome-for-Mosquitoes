#!/usr/bin/env python3
"""
Debug Phone Link Integration Step by Step
Comprehensive debugging for every step of phone camera integration
"""

import os
import sys
import time
import cv2
import shutil
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def debug_step_1_check_environment():
    """Step 1: Check Python environment and dependencies"""
    print("🔍 STEP 1: Checking Python Environment")
    print("=" * 50)
    
    try:
        # Check Python version
        print(f"✅ Python version: {sys.version}")
        
        # Check if we're in the right directory
        current_dir = os.getcwd()
        print(f"✅ Current directory: {current_dir}")
        
        # Check if we're in the IronDomeMosquitoes folder
        if "IronDomeMosquitoes" in current_dir:
            print("✅ We're in the IronDomeMosquitoes directory")
        else:
            print("❌ We're not in the IronDomeMosquitoes directory")
            return False
        
        # Check for required directories
        required_dirs = ["src", "config", "data", "models"]
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                print(f"✅ {dir_name} directory exists")
            else:
                print(f"❌ {dir_name} directory missing")
                return False
        
        print("✅ Step 1 completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Step 1 failed: {e}")
        return False

def debug_step_2_check_dependencies():
    """Step 2: Check if all required packages are installed"""
    print("\n🔍 STEP 2: Checking Dependencies")
    print("=" * 50)
    
    required_packages = [
        "cv2", "numpy", "ultralytics", "loguru", "yaml"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "cv2":
                import cv2
                print(f"✅ {package} imported successfully")
            elif package == "numpy":
                import numpy as np
                print(f"✅ {package} imported successfully")
            elif package == "ultralytics":
                from ultralytics import YOLO
                print(f"✅ {package} imported successfully")
            elif package == "loguru":
                from loguru import logger
                print(f"✅ {package} imported successfully")
            elif package == "yaml":
                import yaml
                print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    print("✅ Step 2 completed successfully!")
    return True

def debug_step_3_check_config():
    """Step 3: Check configuration file"""
    print("\n🔍 STEP 3: Checking Configuration")
    print("=" * 50)
    
    try:
        config_path = "config/config.yaml"
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            return False
        
        print(f"✅ Config file exists: {config_path}")
        
        # Try to load config
        from utils.config_loader import ConfigLoader
        config_loader = ConfigLoader(config_path)
        config = config_loader.load()
        
        if config:
            print("✅ Configuration loaded successfully")
            
            # Check key settings
            detection_config = config.get('detection', {})
            print(f"   - Model path: {detection_config.get('model_path', 'Not found')}")
            print(f"   - Confidence threshold: {detection_config.get('confidence_threshold', 'Not found')}")
            
            camera_config = config.get('camera', {})
            phone_link_config = camera_config.get('phone_link', {})
            print(f"   - Phone Link enabled: {phone_link_config.get('enabled', False)}")
            print(f"   - Capture folder: {phone_link_config.get('capture_folder', 'Not found')}")
            
        else:
            print("❌ Failed to load configuration")
            return False
        
        print("✅ Step 3 completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Step 3 failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_step_4_check_captures_folder():
    """Step 4: Check captures folder and Phone Link setup"""
    print("\n🔍 STEP 4: Checking Captures Folder")
    print("=" * 50)
    
    try:
        capture_folder = "data/captures"
        
        if not os.path.exists(capture_folder):
            print(f"❌ Captures folder not found: {capture_folder}")
            print("📱 Please set up Phone Link first:")
            print("   1. Open Phone Link on your PC")
            print("   2. Click on 'Camera' in Phone Link")
            print("   3. Take a test photo")
            return False
        
        print(f"✅ Captures folder exists: {capture_folder}")
        
        # Check for existing files
        files = os.listdir(capture_folder)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"📸 Found {len(image_files)} image files:")
        for i, file in enumerate(image_files[:5]):  # Show first 5
            file_path = os.path.join(capture_folder, file)
            file_size = os.path.getsize(file_path)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"   {i+1}. {file} ({file_size} bytes) - {file_time}")
        
        if not image_files:
            print("⚠️  No image files found")
            print("📱 Please take a photo with Phone Link camera")
            return False
        
        print("✅ Step 4 completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Step 4 failed: {e}")
        return False

def debug_step_5_test_image_loading():
    """Step 5: Test loading images with OpenCV"""
    print("\n🔍 STEP 5: Testing Image Loading")
    print("=" * 50)
    
    try:
        capture_folder = "data/captures"
        files = os.listdir(capture_folder)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            print("❌ No image files to test")
            return False
        
        # Test loading the first image
        test_file = image_files[0]
        test_path = os.path.join(capture_folder, test_file)
        
        print(f"🔍 Testing image: {test_file}")
        
        # Load with OpenCV
        img = cv2.imread(test_path)
        
        if img is not None:
            print(f"✅ Image loaded successfully")
            print(f"   - Dimensions: {img.shape[1]}x{img.shape[0]}")
            print(f"   - Channels: {img.shape[2]}")
            print(f"   - Data type: {img.dtype}")
            
            # Test if image is not empty
            if img.size > 0:
                print("✅ Image contains data")
            else:
                print("❌ Image is empty")
                return False
                
        else:
            print("❌ Failed to load image with OpenCV")
            return False
        
        print("✅ Step 5 completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Step 5 failed: {e}")
        return False

def debug_step_6_test_detector():
    """Step 6: Test mosquito detector initialization"""
    print("\n🔍 STEP 6: Testing Mosquito Detector")
    print("=" * 50)
    
    try:
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        # Load configuration
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        # Initialize detector
        print("🔍 Initializing mosquito detector...")
        detector = MosquitoDetector(config)
        detector.initialize()
        
        print("✅ Detector initialized successfully")
        
        # Test with a sample image
        capture_folder = "data/captures"
        files = os.listdir(capture_folder)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if image_files:
            test_file = image_files[0]
            test_path = os.path.join(capture_folder, test_file)
            
            print(f"🔍 Testing detection on: {test_file}")
            
            img = cv2.imread(test_path)
            if img is not None:
                detections = detector.detect(img)
                
                if detections:
                    print(f"🦟 Found {len(detections)} detections!")
                    for detection in detections:
                        class_name = detection.get('class_name', 'Unknown')
                        confidence = detection.get('confidence', 0)
                        print(f"   - {class_name}: {confidence:.3f}")
                else:
                    print("✅ No detections found (this is normal for test images)")
            else:
                print("❌ Failed to load test image")
        
        print("✅ Step 6 completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Step 6 failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_step_7_test_phone_link_integration():
    """Step 7: Test Phone Link integration"""
    print("\n🔍 STEP 7: Testing Phone Link Integration")
    print("=" * 50)
    
    try:
        capture_folder = "data/captures"
        
        # Get initial file count
        initial_files = set(os.listdir(capture_folder))
        initial_count = len([f for f in initial_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        print(f"📸 Current image count: {initial_count}")
        print("\n📱 PHONE LINK TEST:")
        print("1. Open Phone Link on your PC")
        print("2. Click on 'Camera' in Phone Link")
        print("3. Take a NEW photo with your phone camera")
        print("4. Wait 10 seconds for the photo to appear...")
        
        # Wait for new files
        start_time = time.time()
        timeout = 30  # 30 seconds timeout
        
        while time.time() - start_time < timeout:
            current_files = set(os.listdir(capture_folder))
            current_count = len([f for f in current_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            
            if current_count > initial_count:
                new_files = current_files - initial_files
                new_image_files = [f for f in new_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                if new_image_files:
                    print(f"\n🎉 NEW PHOTO DETECTED!")
                    for new_file in new_image_files:
                        file_path = os.path.join(capture_folder, new_file)
                        file_size = os.path.getsize(file_path)
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%H:%M:%S')
                        print(f"   📸 {new_file} ({file_size} bytes) at {file_time}")
                    
                    print("✅ Phone Link integration is working!")
                    return True
            
            print(".", end="", flush=True)
            time.sleep(1)
        
        print(f"\n⏰ Timeout reached ({timeout} seconds)")
        print("❌ No new photos detected")
        print("📱 Please check:")
        print("   - Phone Link is open and connected")
        print("   - Camera feature is enabled")
        print("   - You took a photo with your phone")
        return False
        
    except Exception as e:
        print(f"❌ Step 7 failed: {e}")
        return False

def debug_step_8_full_integration_test():
    """Step 8: Full integration test"""
    print("\n🔍 STEP 8: Full Integration Test")
    print("=" * 50)
    
    try:
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        # Load configuration
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        # Initialize detector
        detector = MosquitoDetector(config)
        detector.initialize()
        
        # Monitor for new photos
        capture_folder = "data/captures"
        processed_files = set()
        
        # Get initial files
        if os.path.exists(capture_folder):
            initial_files = set(os.listdir(capture_folder))
            processed_files.update(initial_files)
        
        print("🎯 FULL INTEGRATION TEST:")
        print("The system will now monitor for new phone photos...")
        print("Take a photo with your phone camera to test full integration!")
        print("Press Ctrl+C to stop the test")
        
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
                print("\n🛑 Integration test stopped")
                break
            except Exception as e:
                print(f"❌ Integration test error: {e}")
                break
        
        print("✅ Step 8 completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Step 8 failed: {e}")
        return False

def run_full_debug():
    """Run the complete debugging process"""
    print("🔍 PHONE LINK INTEGRATION DEBUG")
    print("=" * 60)
    print("This will debug every step of the Phone Link integration")
    print("=" * 60)
    
    steps = [
        ("Environment Check", debug_step_1_check_environment),
        ("Dependencies Check", debug_step_2_check_dependencies),
        ("Configuration Check", debug_step_3_check_config),
        ("Captures Folder Check", debug_step_4_check_captures_folder),
        ("Image Loading Test", debug_step_5_test_image_loading),
        ("Detector Test", debug_step_6_test_detector),
        ("Phone Link Test", debug_step_7_test_phone_link_integration),
        ("Full Integration Test", debug_step_8_full_integration_test)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        print(f"\n{'='*60}")
        print(f"🔍 RUNNING: {step_name}")
        print(f"{'='*60}")
        
        try:
            success = step_func()
            results.append((step_name, success))
            
            if success:
                print(f"✅ {step_name} PASSED")
            else:
                print(f"❌ {step_name} FAILED")
                print("🛑 Stopping debug process due to failure")
                break
                
        except Exception as e:
            print(f"❌ {step_name} ERROR: {e}")
            results.append((step_name, False))
            break
    
    # Print summary
    print(f"\n{'='*60}")
    print("🔍 DEBUG SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    for step_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{step_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(results)} steps passed")
    
    if passed == len(results):
        print("🎉 ALL STEPS PASSED! Phone Link integration is working correctly!")
    else:
        print("⚠️  Some steps failed. Please check the errors above.")

if __name__ == "__main__":
    run_full_debug() 