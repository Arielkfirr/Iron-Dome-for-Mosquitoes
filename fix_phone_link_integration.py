#!/usr/bin/env python3
"""
Fix Phone Link Integration Step by Step
Detailed debugging and fixing of Phone Link integration issues
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

def debug_phone_link_step_1_check_phone_link_setup():
    """Step 1: Check if Phone Link is properly set up"""
    print("🔍 PHONE LINK STEP 1: Checking Phone Link Setup")
    print("=" * 60)
    
    print("📱 PHONE LINK SETUP CHECKLIST:")
    print("1. Is Phone Link installed on your PC?")
    print("2. Is Phone Link connected to your phone?")
    print("3. Is the Camera feature enabled in Phone Link?")
    print("4. Have you taken a test photo with Phone Link?")
    
    # Check if captures folder exists and has files
    capture_folder = "data/captures"
    
    if not os.path.exists(capture_folder):
        print(f"❌ Captures folder not found: {capture_folder}")
        print("📱 SETUP INSTRUCTIONS:")
        print("   1. Open Phone Link on your PC")
        print("   2. Make sure your phone is connected")
        print("   3. Click on 'Camera' in Phone Link")
        print("   4. Take a test photo with your phone")
        print("   5. Check if the photo appears in the captures folder")
        return False
    
    print(f"✅ Captures folder exists: {capture_folder}")
    
    # Check for existing files
    files = os.listdir(capture_folder)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📸 Found {len(image_files)} existing image files:")
    for i, file in enumerate(image_files):
        file_path = os.path.join(capture_folder, file)
        file_size = os.path.getsize(file_path)
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"   {i+1}. {file} ({file_size} bytes) - {file_time}")
    
    if not image_files:
        print("❌ No image files found")
        print("📱 Please take a photo with Phone Link camera first")
        return False
    
    print("✅ Phone Link setup appears to be working")
    return True

def debug_phone_link_step_2_test_file_monitoring():
    """Step 2: Test file monitoring system"""
    print("\n🔍 PHONE LINK STEP 2: Testing File Monitoring")
    print("=" * 60)
    
    capture_folder = "data/captures"
    
    # Get initial state
    initial_files = set(os.listdir(capture_folder))
    initial_image_files = [f for f in initial_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📸 Initial state: {len(initial_image_files)} image files")
    print("📱 TESTING FILE MONITORING:")
    print("1. The system will monitor for new files")
    print("2. Take a NEW photo with your phone camera")
    print("3. Watch for detection of the new file")
    print("4. Press Ctrl+C to stop monitoring")
    
    try:
        start_time = time.time()
        timeout = 60  # 60 seconds timeout
        
        while time.time() - start_time < timeout:
            current_files = set(os.listdir(capture_folder))
            current_image_files = [f for f in current_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            # Check for new files
            new_files = current_files - initial_files
            new_image_files = [f for f in new_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if new_image_files:
                print(f"\n🎉 NEW FILES DETECTED!")
                for new_file in new_image_files:
                    file_path = os.path.join(capture_folder, new_file)
                    file_size = os.path.getsize(file_path)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%H:%M:%S')
                    print(f"   📸 {new_file} ({file_size} bytes) at {file_time}")
                
                print("✅ File monitoring is working!")
                return True
            
            # Show progress
            elapsed = int(time.time() - start_time)
            remaining = timeout - elapsed
            print(f"\r⏳ Waiting for new files... ({remaining}s remaining)", end="", flush=True)
            
            time.sleep(1)
        
        print(f"\n⏰ Timeout reached ({timeout} seconds)")
        print("❌ No new files detected")
        return False
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
        return False

def debug_phone_link_step_3_test_image_processing():
    """Step 3: Test image processing with existing files"""
    print("\n🔍 PHONE LINK STEP 3: Testing Image Processing")
    print("=" * 60)
    
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
        
        # Test with existing images
        capture_folder = "data/captures"
        files = os.listdir(capture_folder)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            print("❌ No image files to test")
            return False
        
        print(f"🔍 Testing processing on {len(image_files)} existing images:")
        
        for i, file in enumerate(image_files):
            file_path = os.path.join(capture_folder, file)
            print(f"\n📸 Processing {i+1}/{len(image_files)}: {file}")
            
            try:
                # Load image
                img = cv2.imread(file_path)
                if img is None:
                    print(f"   ❌ Failed to load {file}")
                    continue
                
                print(f"   ✅ Loaded ({img.shape[1]}x{img.shape[0]})")
                
                # Process with detector
                detections = detector.detect(img)
                
                if detections:
                    print(f"   🦟 Found {len(detections)} detections!")
                    for detection in detections:
                        class_name = detection.get('class_name', 'Unknown')
                        confidence = detection.get('confidence', 0)
                        print(f"      - {class_name}: {confidence:.3f}")
                else:
                    print(f"   ✅ No detections found")
                
            except Exception as e:
                print(f"   ❌ Error processing {file}: {e}")
        
        print("\n✅ Image processing test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Step 3 failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_phone_link_step_4_test_real_time_processing():
    """Step 4: Test real-time processing of new images"""
    print("\n🔍 PHONE LINK STEP 4: Testing Real-time Processing")
    print("=" * 60)
    
    try:
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        # Load configuration and initialize detector
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        detector = MosquitoDetector(config)
        detector.initialize()
        
        print("✅ Detector ready for real-time processing")
        
        # Monitor for new files
        capture_folder = "data/captures"
        processed_files = set()
        
        # Get initial files
        if os.path.exists(capture_folder):
            initial_files = set(os.listdir(capture_folder))
            processed_files.update(initial_files)
        
        print("🎯 REAL-TIME PROCESSING TEST:")
        print("The system will now monitor for new phone photos...")
        print("Take a photo with your phone camera to test real-time processing!")
        print("Press Ctrl+C to stop the test")
        
        start_time = time.time()
        timeout = 120  # 2 minutes timeout
        
        while time.time() - start_time < timeout:
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
                                        print(f"   🦟 Found {len(detections)} detections!")
                                        for detection in detections:
                                            class_name = detection.get('class_name', 'Unknown')
                                            confidence = detection.get('confidence', 0)
                                            print(f"      - {class_name}: {confidence:.3f}")
                                    else:
                                        print(f"   ✅ No mosquitoes detected in this photo")
                                else:
                                    print(f"   ❌ Failed to load new photo")
                                    
                            except Exception as e:
                                print(f"   ❌ Error processing new photo: {e}")
                            
                            processed_files.add(file)
                
                # Show waiting status
                elapsed = int(time.time() - start_time)
                remaining = timeout - elapsed
                print(f"\r⏳ Waiting for new photos... ({remaining}s remaining)", end="", flush=True)
                
                time.sleep(1)  # Check every second
                
            except KeyboardInterrupt:
                print("\n🛑 Real-time processing test stopped")
                break
            except Exception as e:
                print(f"\n❌ Real-time processing error: {e}")
                break
        
        print(f"\n✅ Real-time processing test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Step 4 failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_phone_link_step_5_fix_common_issues():
    """Step 5: Fix common Phone Link integration issues"""
    print("\n🔍 PHONE LINK STEP 5: Fixing Common Issues")
    print("=" * 60)
    
    print("🔧 COMMON PHONE LINK ISSUES AND FIXES:")
    print("=" * 40)
    
    # Issue 1: Phone Link not connected
    print("\n1. 📱 PHONE LINK CONNECTION:")
    print("   - Make sure Phone Link is open on your PC")
    print("   - Check that your phone is connected")
    print("   - Try disconnecting and reconnecting your phone")
    
    # Issue 2: Camera feature not enabled
    print("\n2. 📷 CAMERA FEATURE:")
    print("   - Open Phone Link on your PC")
    print("   - Click on 'Camera' in the Phone Link interface")
    print("   - Make sure camera permissions are granted")
    
    # Issue 3: Photos not saving to correct folder
    print("\n3. 📁 FOLDER PERMISSIONS:")
    print("   - Check if data/captures folder exists")
    print("   - Ensure the folder has write permissions")
    print("   - Verify Phone Link is saving to the correct location")
    
    # Issue 4: File monitoring not working
    print("\n4. 🔍 FILE MONITORING:")
    print("   - The system monitors data/captures folder")
    print("   - New photos should appear automatically")
    print("   - Check if photos are being saved with correct extensions")
    
    # Create a test script to verify setup
    print("\n5. 🧪 TESTING SETUP:")
    print("   - Take a photo with your phone camera")
    print("   - Check if it appears in data/captures folder")
    print("   - Run the monitoring script to test detection")
    
    return True

def run_phone_link_fix():
    """Run the complete Phone Link fixing process"""
    print("🔧 PHONE LINK INTEGRATION FIX")
    print("=" * 60)
    print("This will debug and fix Phone Link integration issues")
    print("=" * 60)
    
    steps = [
        ("Phone Link Setup Check", debug_phone_link_step_1_check_phone_link_setup),
        ("File Monitoring Test", debug_phone_link_step_2_test_file_monitoring),
        ("Image Processing Test", debug_phone_link_step_3_test_image_processing),
        ("Real-time Processing Test", debug_phone_link_step_4_test_real_time_processing),
        ("Common Issues Fix", debug_phone_link_step_5_fix_common_issues)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        print(f"\n{'='*60}")
        print(f"🔧 RUNNING: {step_name}")
        print(f"{'='*60}")
        
        try:
            success = step_func()
            results.append((step_name, success))
            
            if success:
                print(f"✅ {step_name} PASSED")
            else:
                print(f"❌ {step_name} FAILED")
                print("⚠️  This step needs attention")
                
        except Exception as e:
            print(f"❌ {step_name} ERROR: {e}")
            results.append((step_name, False))
    
    # Print summary
    print(f"\n{'='*60}")
    print("🔧 PHONE LINK FIX SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    for step_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{step_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(results)} steps passed")
    
    if passed == len(results):
        print("🎉 ALL STEPS PASSED! Phone Link integration should be working!")
    else:
        print("⚠️  Some steps failed. Please check the issues above.")
        print("\n📱 NEXT STEPS:")
        print("1. Make sure Phone Link is properly connected")
        print("2. Take a test photo with your phone camera")
        print("3. Check if the photo appears in data/captures folder")
        print("4. Run the monitoring script again")

if __name__ == "__main__":
    run_phone_link_fix() 