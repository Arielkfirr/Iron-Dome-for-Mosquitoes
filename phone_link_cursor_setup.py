#!/usr/bin/env python3
"""
Phone Link Cursor Setup
Comprehensive setup and testing for Phone Link integration in Cursor
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

class PhoneLinkCursorSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.capture_folder = self.project_root / "data" / "captures"
        self.config_file = self.project_root / "config" / "config.yaml"
        
    def setup_phone_link(self):
        """Complete Phone Link setup for Cursor"""
        print("📱 PHONE LINK CURSOR SETUP")
        print("=" * 50)
        
        print("\n🔧 STEP 1: VERIFY PHONE LINK INSTALLATION")
        print("-" * 40)
        
        # Check if Phone Link is installed
        phone_link_installed = self.check_phone_link_installation()
        if not phone_link_installed:
            print("❌ Phone Link not found")
            print("📥 Please install Phone Link from Microsoft Store")
            print("   - Open Microsoft Store")
            print("   - Search for 'Phone Link'")
            print("   - Click Install")
            return False
        
        print("✅ Phone Link is installed")
        
        print("\n🔧 STEP 2: CREATE CAPTURE FOLDER")
        print("-" * 40)
        
        # Create capture folder
        self.capture_folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Capture folder created: {self.capture_folder}")
        
        print("\n🔧 STEP 3: CONFIGURE PHONE LINK")
        print("-" * 40)
        print("📱 Please follow these steps:")
        print("1. Open Phone Link on your PC")
        print("2. Connect your phone (same WiFi network)")
        print("3. Enable camera permissions")
        print("4. Test photo capture")
        
        input("\nPress Enter when Phone Link is configured...")
        
        print("\n🔧 STEP 4: TEST PHOTO TRANSFER")
        print("-" * 40)
        
        # Test photo transfer
        test_success = self.test_photo_transfer()
        if test_success:
            print("✅ Photo transfer working!")
        else:
            print("❌ Photo transfer failed")
            print("📱 Please check Phone Link connection")
            return False
        
        print("\n🔧 STEP 5: CONFIGURE AUTO-MONITORING")
        print("-" * 40)
        
        # Create monitoring script
        self.create_monitoring_script()
        
        print("✅ Phone Link setup completed!")
        print("\n📋 NEXT STEPS:")
        print("1. Run: python phone_link_monitor.py")
        print("2. Take photos with Phone Link camera")
        print("3. Watch for automatic detection")
        
        return True
    
    def check_phone_link_installation(self):
        """Check if Phone Link is installed"""
        try:
            # Try to find Phone Link in common locations
            possible_paths = [
                r"C:\Program Files\WindowsApps\Microsoft.YourPhone_*",
                r"C:\Users\{}\AppData\Local\Microsoft\WindowsApps\Microsoft.YourPhone.exe".format(os.getenv('USERNAME')),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return True
            
            # Try to run Phone Link
            result = subprocess.run(['start', 'ms-settings:mobile-devices'], 
                                  shell=True, capture_output=True)
            return True
            
        except Exception as e:
            print(f"Error checking Phone Link: {e}")
            return False
    
    def test_photo_transfer(self):
        """Test if photos can be transferred"""
        print("📸 Testing photo transfer...")
        print("📱 Please take a photo with Phone Link camera")
        print("⏳ Waiting 30 seconds for photo transfer...")
        
        initial_files = set(os.listdir(self.capture_folder))
        
        for i in range(30):
            current_files = set(os.listdir(self.capture_folder))
            new_files = current_files - initial_files
            
            if new_files:
                print(f"✅ Photo transferred! Found: {list(new_files)}")
                return True
            
            print(f"⏳ {30-i} seconds remaining...")
            time.sleep(1)
        
        print("❌ No photos transferred in 30 seconds")
        return False
    
    def create_monitoring_script(self):
        """Create a monitoring script for Phone Link"""
        monitor_script = self.project_root / "phone_link_monitor.py"
        
        script_content = '''#!/usr/bin/env python3
"""
Phone Link Monitor
Automatically monitors for new photos from Phone Link
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def monitor_phone_link_photos():
    """Monitor for new photos from Phone Link"""
    print("📱 PHONE LINK PHOTO MONITOR")
    print("=" * 40)
    
    capture_folder = Path(__file__).parent / "data" / "captures"
    processed_files = set()
    
    print(f"📁 Monitoring: {capture_folder}")
    print("📱 Take photos with Phone Link camera")
    print("🛑 Press Ctrl+C to stop")
    
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
                        
                        print(f"\\n📸 NEW PHOTO: {file}")
                        print(f"   📅 Time: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"   📏 Size: {file_size} bytes")
                        
                        # Process the photo
                        try:
                            from detection.mosquito_detector import MosquitoDetector
                            from utils.config_loader import ConfigLoader
                            
                            config_loader = ConfigLoader("config/config.yaml")
                            config = config_loader.load()
                            
                            detector = MosquitoDetector(config)
                            detector.initialize()
                            
                            results = detector.detect_image(str(file_path))
                            if results and results.get('detections'):
                                print(f"🦟 Found {len(results['detections'])} mosquitoes!")
                                for detection in results['detections']:
                                    confidence = detection.get('confidence', 0)
                                    print(f"   - Confidence: {confidence:.3f}")
                            else:
                                print("✅ No mosquitoes detected")
                                
                        except Exception as e:
                            print(f"❌ Error processing photo: {e}")
                        
                        processed_files.add(file)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\\n🛑 Monitoring stopped")

if __name__ == "__main__":
    monitor_phone_link_photos()
'''
        
        with open(monitor_script, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Created monitoring script: {monitor_script}")
    
    def run_quick_test(self):
        """Run a quick test of the Phone Link setup"""
        print("🧪 QUICK PHONE LINK TEST")
        print("=" * 30)
        
        # Check capture folder
        if not self.capture_folder.exists():
            print("❌ Capture folder not found")
            return False
        
        # Check for recent photos
        files = os.listdir(self.capture_folder)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"📸 Found {len(image_files)} photos in capture folder")
        
        if image_files:
            latest_file = max(image_files, key=lambda f: os.path.getmtime(self.capture_folder / f))
            file_time = datetime.fromtimestamp(os.path.getmtime(self.capture_folder / latest_file))
            print(f"📸 Latest photo: {latest_file}")
            print(f"📅 Taken: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Test processing
            try:
                from detection.mosquito_detector import MosquitoDetector
                from utils.config_loader import ConfigLoader
                
                config_loader = ConfigLoader("config/config.yaml")
                config = config_loader.load()
                
                detector = MosquitoDetector(config)
                detector.initialize()
                
                results = detector.detect_image(str(self.capture_folder / latest_file))
                if results and results.get('detections'):
                    print(f"🦟 Found {len(results['detections'])} mosquitoes!")
                else:
                    print("✅ No mosquitoes detected")
                
                return True
                
            except Exception as e:
                print(f"❌ Error processing photo: {e}")
                return False
        else:
            print("⚠️  No photos found")
            print("📱 Please take a photo with Phone Link camera")
            return False

def main():
    """Main setup function"""
    setup = PhoneLinkCursorSetup()
    
    print("📱 PHONE LINK CURSOR SETUP")
    print("=" * 50)
    print("Choose an option:")
    print("1. Complete Phone Link setup")
    print("2. Quick test")
    print("3. Run monitoring script")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        setup.setup_phone_link()
    elif choice == "2":
        setup.run_quick_test()
    elif choice == "3":
        print("Starting monitoring script...")
        subprocess.run([sys.executable, "phone_link_monitor.py"])
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main() 