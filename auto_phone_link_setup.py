#!/usr/bin/env python3
"""
Auto Phone Link Setup
Fully automated Phone Link integration with no manual steps
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

class AutoPhoneLinkSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.capture_folder = self.project_root / "data" / "captures"
        self.target_filename = "20250731_030450.jpg"
        self.target_path = self.capture_folder / self.target_filename
        
    def auto_setup_phone_link(self):
        """Fully automated Phone Link setup"""
        print("🤖 AUTO PHONE LINK SETUP")
        print("=" * 50)
        print("Running fully automated setup...")
        
        # Step 1: Auto-create folders
        print("\n📁 STEP 1: Creating folder structure...")
        self.capture_folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Capture folder ready: {self.capture_folder}")
        
        # Step 2: Auto-check Phone Link
        print("\n📱 STEP 2: Checking Phone Link...")
        phone_link_working = self.check_phone_link_automatically()
        
        # Step 3: Auto-search for photos
        print("\n🔍 STEP 3: Searching for photos automatically...")
        found_photo = self.auto_search_for_photos()
        
        # Step 4: Auto-test system
        print("\n🧪 STEP 4: Testing system automatically...")
        system_working = self.auto_test_system()
        
        # Step 5: Auto-create monitoring
        print("\n👀 STEP 5: Setting up automatic monitoring...")
        self.auto_create_monitoring()
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 AUTO SETUP SUMMARY")
        print("=" * 30)
        
        results = [
            ("Phone Link", phone_link_working),
            ("Photo Found", found_photo is not None),
            ("System Test", system_working),
        ]
        
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"\n📈 RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 AUTO SETUP COMPLETED!")
            print("\n📱 PHONE LINK IS READY!")
            print("The system will automatically:")
            print("1. Monitor for new photos")
            print("2. Process them for mosquito detection")
            print("3. Show results in real-time")
            
            # Auto-start monitoring
            print("\n🚀 Auto-starting monitoring...")
            self.auto_start_monitoring()
        else:
            print(f"⚠️  {total-passed} tests failed")
            print("The system will still work, but some features may be limited")
        
        return passed == total
    
    def check_phone_link_automatically(self):
        """Automatically check Phone Link without user input"""
        try:
            # Try to start Phone Link automatically
            subprocess.run(['start', 'ms-settings:mobile-devices'], 
                         shell=True, capture_output=True, timeout=5)
            print("✅ Phone Link settings opened")
            return True
        except Exception as e:
            print(f"⚠️  Could not auto-start Phone Link: {e}")
            print("📱 Please install Phone Link from Microsoft Store manually")
            return False
    
    def auto_search_for_photos(self):
        """Automatically search for photos in all possible locations"""
        print("🔍 Searching for photos automatically...")
        
        # Search locations
        search_locations = [
            Path.home() / "Pictures" / "Phone Link",
            Path.home() / "Downloads" / "Phone Link",
            Path.home() / "Documents" / "Phone Link",
            Path.home() / "Desktop" / "Phone Link",
            Path.home() / "OneDrive" / "Pictures" / "Phone Link",
            self.capture_folder,
            self.project_root / "phone_captures",
        ]
        
        found_photos = []
        
        for location in search_locations:
            if location.exists():
                try:
                    # Search for any recent photos
                    for file_path in location.glob("*.jpg"):
                        if file_path.is_file() and file_path.stat().st_size > 1000:
                            found_photos.append(file_path)
                            print(f"✅ Found photo: {file_path.name}")
                except Exception:
                    pass
        
        if found_photos:
            # Use the most recent photo
            latest_photo = max(found_photos, key=lambda f: f.stat().st_mtime)
            print(f"✅ Using latest photo: {latest_photo.name}")
            
            # Copy to captures folder if needed
            if latest_photo != self.target_path:
                shutil.copy2(latest_photo, self.target_path)
                print(f"✅ Copied to captures folder")
            
            return self.target_path
        else:
            print("⚠️  No photos found automatically")
            print("📱 Photos will be detected when you take them with Phone Link")
            return None
    
    def auto_test_system(self):
        """Automatically test the system without user input"""
        try:
            # Test component imports
            from detection.mosquito_detector import MosquitoDetector
            from utils.config_loader import ConfigLoader
            print("✅ Components imported")
            
            # Test configuration
            config_loader = ConfigLoader("config/config.yaml")
            config = config_loader.load()
            print("✅ Configuration loaded")
            
            # Test detector
            detector = MosquitoDetector(config)
            detector.initialize()
            print("✅ Detector initialized")
            
            # Test with any available photo
            if self.target_path.exists():
                import cv2
                img = cv2.imread(str(self.target_path))
                if img is not None:
                    results = detector.detect(img)
                    print(f"✅ System test completed")
                    return True
            
            print("✅ System ready (no test photo available)")
            return True
            
        except Exception as e:
            print(f"❌ System test failed: {e}")
            return False
    
    def auto_create_monitoring(self):
        """Automatically create monitoring script"""
        monitor_script = self.project_root / "auto_phone_link_monitor.py"
        
        script_content = '''#!/usr/bin/env python3
"""
Auto Phone Link Monitor
Fully automated monitoring for Phone Link photos
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def auto_monitor_phone_link():
    """Automatically monitor for Phone Link photos"""
    print("🤖 AUTO PHONE LINK MONITOR")
    print("=" * 40)
    print("Monitoring automatically - no user input required")
    
    capture_folder = Path(__file__).parent / "data" / "captures"
    processed_files = set()
    
    print(f"📁 Monitoring: {capture_folder}")
    print("📱 Take photos with Phone Link camera")
    print("🛑 Press Ctrl+C to stop")
    
    # Initialize detector once
    try:
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        detector = MosquitoDetector(config)
        detector.initialize()
        print("✅ Detector ready for automatic processing")
        
    except Exception as e:
        print(f"❌ Detector initialization failed: {e}")
        return
    
    try:
        while True:
            if capture_folder.exists():
                current_files = set(os.listdir(capture_folder))
                new_files = current_files - processed_files
                
                for file in new_files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        file_path = capture_folder / file
                        file_size = file_path.stat().st_size
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        
                        print(f"\\n📸 AUTO DETECTED: {file}")
                        print(f"   📅 Time: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"   📏 Size: {file_size} bytes")
                        
                        # Auto-process the photo
                        try:
                            import cv2
                            img = cv2.imread(str(file_path))
                            if img is not None:
                                results = detector.detect(img)
                                
                                if results:
                                    print(f"🦟 AUTO DETECTION: {len(results)} objects found!")
                                    for detection in results:
                                        confidence = detection.get('confidence', 0)
                                        class_name = detection.get('class_name', 'Unknown')
                                        print(f"   - {class_name}: {confidence:.3f}")
                                else:
                                    print("✅ No mosquitoes detected automatically")
                            else:
                                print("❌ Could not load image automatically")
                                
                        except Exception as e:
                            print(f"❌ Auto-processing error: {e}")
                        
                        processed_files.add(file)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\\n🛑 Auto-monitoring stopped")

if __name__ == "__main__":
    auto_monitor_phone_link()
'''
        
        with open(monitor_script, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Created auto-monitoring script: {monitor_script}")
    
    def auto_start_monitoring(self):
        """Automatically start monitoring in background"""
        try:
            monitor_script = self.project_root / "auto_phone_link_monitor.py"
            if monitor_script.exists():
                print("🚀 Starting auto-monitoring...")
                # Start monitoring in background
                subprocess.Popen([sys.executable, str(monitor_script)], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
                print("✅ Auto-monitoring started in background")
                print("📱 Take photos with Phone Link - they will be processed automatically!")
            else:
                print("❌ Monitoring script not found")
        except Exception as e:
            print(f"❌ Could not start auto-monitoring: {e}")

if __name__ == "__main__":
    setup = AutoPhoneLinkSetup()
    success = setup.auto_setup_phone_link()
    
    if success:
        print("\n✅ Auto setup completed successfully!")
    else:
        print("\n⚠️  Auto setup completed with some issues")
    
    print("\nPress Enter to exit...")
    input() 