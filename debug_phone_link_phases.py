#!/usr/bin/env python3
"""
Debug Phone Link Phases
Test every phase of Phone Link integration step by step
"""

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

class PhoneLinkPhaseDebugger:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.capture_folder = self.project_root / "data" / "captures"
        self.target_filename = "20250731_030450.jpg"
        self.target_path = self.capture_folder / self.target_filename
        
    def debug_phase_1_phone_link_setup(self):
        """Phase 1: Phone Link Setup"""
        print("🔧 PHASE 1: PHONE LINK SETUP")
        print("=" * 40)
        
        print("📱 Checking Phone Link installation...")
        
        # Check if Phone Link is installed
        phone_link_paths = [
            Path.home() / "AppData" / "Local" / "Microsoft" / "WindowsApps" / "Microsoft.YourPhone.exe",
            Path("C:/Program Files/WindowsApps/Microsoft.YourPhone_*"),
        ]
        
        phone_link_found = False
        for path in phone_link_paths:
            if path.exists():
                print(f"✅ Phone Link found at: {path}")
                phone_link_found = True
                break
        
        if not phone_link_found:
            print("❌ Phone Link not found in common locations")
            print("📥 Please install Phone Link from Microsoft Store")
            return False
        
        print("✅ Phone Link installation check passed")
        return True
    
    def debug_phase_2_folder_structure(self):
        """Phase 2: Folder Structure"""
        print("\n📁 PHASE 2: FOLDER STRUCTURE")
        print("=" * 40)
        
        # Check project structure
        required_folders = [
            self.project_root / "data",
            self.project_root / "data" / "captures",
            self.project_root / "config",
            self.project_root / "models",
            self.project_root / "src",
        ]
        
        for folder in required_folders:
            if folder.exists():
                print(f"✅ {folder.name} folder exists")
            else:
                print(f"❌ {folder.name} folder missing")
                folder.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created {folder.name} folder")
        
        # Check required files
        required_files = [
            self.project_root / "config" / "config.yaml",
            self.project_root / "models" / "yolov8n.pt",
        ]
        
        for file in required_files:
            if file.exists():
                print(f"✅ {file.name} exists")
            else:
                print(f"❌ {file.name} missing")
                return False
        
        print("✅ Folder structure check passed")
        return True
    
    def debug_phase_3_photo_transfer(self):
        """Phase 3: Photo Transfer"""
        print("\n📸 PHASE 3: PHOTO TRANSFER")
        print("=" * 40)
        
        print(f"🔍 Looking for photo: {self.target_filename}")
        
        # Check if photo exists in captures folder
        if self.target_path.exists():
            file_size = self.target_path.stat().st_size
            print(f"✅ Photo found in captures folder")
            print(f"📏 Size: {file_size} bytes")
            
            if file_size < 1000:
                print("⚠️  Photo size is very small, may be corrupted")
                return False
            
            return True
        else:
            print(f"❌ Photo not found in captures folder")
            print("\n📱 TRANSFER INSTRUCTIONS:")
            print("1. Open Phone Link on your PC")
            print("2. Go to Photos section")
            print("3. Find the photo: 20250731_030450.jpg")
            print("4. Right-click and 'Save as' to:")
            print(f"   {self.target_path}")
            
            # Wait for transfer
            input("\nPress Enter after transferring the photo...")
            
            if self.target_path.exists():
                file_size = self.target_path.stat().st_size
                print(f"✅ Photo transferred successfully")
                print(f"📏 Size: {file_size} bytes")
                return True
            else:
                print("❌ Photo still not found")
                return False
    
    def debug_phase_4_image_loading(self):
        """Phase 4: Image Loading"""
        print("\n🖼️  PHASE 4: IMAGE LOADING")
        print("=" * 40)
        
        if not self.target_path.exists():
            print("❌ Photo not found, skipping image loading test")
            return False
        
        try:
            import cv2
            print("✅ OpenCV imported successfully")
            
            # Load the image
            img = cv2.imread(str(self.target_path))
            
            if img is not None:
                height, width, channels = img.shape
                print(f"✅ Image loaded successfully")
                print(f"📐 Dimensions: {width}x{height} pixels")
                print(f"🎨 Channels: {channels}")
                
                # Check image quality
                if width < 100 or height < 100:
                    print("⚠️  Image dimensions are very small")
                    return False
                
                return True
            else:
                print("❌ Failed to load image")
                return False
                
        except ImportError as e:
            print(f"❌ OpenCV not installed: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return False
    
    def debug_phase_5_component_imports(self):
        """Phase 5: Component Imports"""
        print("\n📦 PHASE 5: COMPONENT IMPORTS")
        print("=" * 40)
        
        try:
            from detection.mosquito_detector import MosquitoDetector
            print("✅ MosquitoDetector imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import MosquitoDetector: {e}")
            return False
        
        try:
            from utils.config_loader import ConfigLoader
            print("✅ ConfigLoader imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import ConfigLoader: {e}")
            return False
        
        try:
            from utils.logger import get_logger
            print("✅ Logger imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import Logger: {e}")
            return False
        
        print("✅ All component imports successful")
        return True
    
    def debug_phase_6_configuration_loading(self):
        """Phase 6: Configuration Loading"""
        print("\n⚙️  PHASE 6: CONFIGURATION LOADING")
        print("=" * 40)
        
        try:
            from utils.config_loader import ConfigLoader
            
            config_file = self.project_root / "config" / "config.yaml"
            config_loader = ConfigLoader(str(config_file))
            config = config_loader.load()
            
            if config:
                print("✅ Configuration loaded successfully")
                
                # Check key configuration sections
                required_sections = ['detection', 'camera', 'system']
                for section in required_sections:
                    if section in config:
                        print(f"✅ {section} section found")
                    else:
                        print(f"❌ {section} section missing")
                        return False
                
                # Check Phone Link configuration
                phone_link_config = config.get('camera', {}).get('phone_link', {})
                if phone_link_config.get('enabled'):
                    print("✅ Phone Link enabled in configuration")
                else:
                    print("⚠️  Phone Link not enabled in configuration")
                
                return True
            else:
                print("❌ Configuration is empty")
                return False
                
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return False
    
    def debug_phase_7_detector_initialization(self):
        """Phase 7: Detector Initialization"""
        print("\n🔍 PHASE 7: DETECTOR INITIALIZATION")
        print("=" * 40)
        
        try:
            from detection.mosquito_detector import MosquitoDetector
            from utils.config_loader import ConfigLoader
            
            # Load configuration
            config_loader = ConfigLoader("config/config.yaml")
            config = config_loader.load()
            
            # Initialize detector
            detector = MosquitoDetector(config)
            print("✅ Detector object created")
            
            detector.initialize()
            print("✅ Detector initialized successfully")
            
            # Test detector health
            health = detector.check_health()
            if health.get('status') == 'healthy':
                print("✅ Detector health check passed")
            else:
                print(f"⚠️  Detector health issues: {health}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing detector: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def debug_phase_8_detection_test(self):
        """Phase 8: Detection Test"""
        print("\n🦟 PHASE 8: DETECTION TEST")
        print("=" * 40)
        
        if not self.target_path.exists():
            print("❌ Photo not found, skipping detection test")
            return False
        
        try:
            import cv2
            from detection.mosquito_detector import MosquitoDetector
            from utils.config_loader import ConfigLoader
            
            # Load configuration
            config_loader = ConfigLoader("config/config.yaml")
            config = config_loader.load()
            
            # Initialize detector
            detector = MosquitoDetector(config)
            detector.initialize()
            
            # Load and process image
            img = cv2.imread(str(self.target_path))
            if img is None:
                print("❌ Failed to load image for detection")
                return False
            
            print(f"📸 Processing image: {img.shape[1]}x{img.shape[0]}")
            
            # Run detection
            results = detector.detect(img)
            
            if results:
                print(f"🦟 Found {len(results)} detections!")
                for i, detection in enumerate(results):
                    confidence = detection.get('confidence', 0)
                    class_name = detection.get('class_name', 'Unknown')
                    print(f"   {i+1}. {class_name}: {confidence:.3f}")
            else:
                print("✅ No detections found (this is normal for test images)")
            
            print("✅ Detection test completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error during detection test: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def debug_phase_9_monitoring_setup(self):
        """Phase 9: Monitoring Setup"""
        print("\n👀 PHASE 9: MONITORING SETUP")
        print("=" * 40)
        
        # Create monitoring script
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
                            
                            import cv2
                            img = cv2.imread(str(file_path))
                            results = detector.detect(img)
                            
                            if results:
                                print(f"🦟 Found {len(results)} detections!")
                                for detection in results:
                                    confidence = detection.get('confidence', 0)
                                    class_name = detection.get('class_name', 'Unknown')
                                    print(f"   - {class_name}: {confidence:.3f}")
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
        print("✅ Monitoring setup completed")
        return True
    
    def run_all_phases(self):
        """Run all debug phases"""
        print("🔍 PHONE LINK INTEGRATION DEBUG")
        print("=" * 50)
        print("Testing every phase of Phone Link integration...")
        
        phases = [
            ("Phone Link Setup", self.debug_phase_1_phone_link_setup),
            ("Folder Structure", self.debug_phase_2_folder_structure),
            ("Photo Transfer", self.debug_phase_3_photo_transfer),
            ("Image Loading", self.debug_phase_4_image_loading),
            ("Component Imports", self.debug_phase_5_component_imports),
            ("Configuration Loading", self.debug_phase_6_configuration_loading),
            ("Detector Initialization", self.debug_phase_7_detector_initialization),
            ("Detection Test", self.debug_phase_8_detection_test),
            ("Monitoring Setup", self.debug_phase_9_monitoring_setup),
        ]
        
        results = []
        
        for phase_name, phase_func in phases:
            print(f"\n{'='*60}")
            try:
                success = phase_func()
                results.append((phase_name, success))
                if success:
                    print(f"✅ {phase_name}: PASSED")
                else:
                    print(f"❌ {phase_name}: FAILED")
            except Exception as e:
                print(f"❌ {phase_name}: ERROR - {e}")
                results.append((phase_name, False))
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 DEBUG SUMMARY")
        print("=" * 30)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for phase_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{phase_name}: {status}")
        
        print(f"\n📈 RESULTS: {passed}/{total} phases passed")
        
        if passed == total:
            print("🎉 ALL PHASES PASSED! Phone Link integration is ready!")
            print("\n📱 NEXT STEPS:")
            print("1. Run: python phone_link_monitor.py")
            print("2. Take photos with Phone Link camera")
            print("3. Watch for automatic detection")
        else:
            print(f"⚠️  {total-passed} phases failed. Please fix the issues above.")
        
        return passed == total

if __name__ == "__main__":
    debugger = PhoneLinkPhaseDebugger()
    success = debugger.run_all_phases()
    
    if success:
        print("\n✅ Phone Link integration is working correctly!")
    else:
        print("\n❌ Some issues need to be resolved.")
    
    print("\nPress Enter to exit...")
    input() 