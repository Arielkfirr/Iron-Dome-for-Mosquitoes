#!/usr/bin/env python3
"""
Debug Phone Link image capture
"""

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def debug_image_capture():
    """Debug the image capture process"""
    print("🔍 Debugging Phone Link Image Capture")
    print("=" * 50)
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check IronDomeMosquitoes directory
    iron_dome_path = "IronDomeMosquitoes"
    if os.path.exists(iron_dome_path):
        print(f"✅ IronDomeMosquitoes directory exists")
        
        # Check data/captures folder
        captures_path = os.path.join(iron_dome_path, "data", "captures")
        if os.path.exists(captures_path):
            print(f"✅ Captures folder exists: {captures_path}")
            
            # List all files with details
            files = os.listdir(captures_path)
            print(f"📸 Found {len(files)} files:")
            
            for file in files:
                file_path = os.path.join(captures_path, file)
                file_size = os.path.getsize(file_path)
                mod_time = os.path.getmtime(file_path)
                
                print(f"   - {file}")
                print(f"     Size: {file_size} bytes")
                print(f"     Modified: {time.ctime(mod_time)}")
                
                # Check if it's a valid image
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if file_size > 1000:  # More than 1KB
                        print(f"     ✅ Valid image file")
                    else:
                        print(f"     ❌ Small file - might be corrupted")
                else:
                    print(f"     ⚠️  Not an image file")
        else:
            print(f"❌ Captures folder not found: {captures_path}")
    else:
        print(f"❌ IronDomeMosquitoes directory not found")
    
    # Check Phone Link configuration
    print(f"\n📱 Phone Link Configuration:")
    try:
        from utils.config_loader import ConfigLoader
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        if config:
            phone_link_config = config.get('camera', {}).get('phone_link', {})
            print(f"   - Phone Link enabled: {phone_link_config.get('enabled', False)}")
            print(f"   - Capture folder: {phone_link_config.get('capture_folder', 'Not found')}")
            print(f"   - Auto save: {phone_link_config.get('auto_save', False)}")
        else:
            print("   ❌ Configuration not loaded")
            
    except Exception as e:
        print(f"   ❌ Error loading config: {e}")
    
    # Check if Phone Link is running
    print(f"\n📱 Phone Link Status:")
    print("1. Open Phone Link on your PC")
    print("2. Click on 'Camera' in Phone Link")
    print("3. Take a photo with your phone camera")
    print("4. Check if the photo appears in the captures folder")
    
    # Monitor for new files
    print(f"\n🎯 Monitoring for new files...")
    print("Take a photo now and watch for new files!")
    print("Press Ctrl+C to stop monitoring")
    
    if os.path.exists(captures_path):
        initial_files = set(os.listdir(captures_path))
        print(f"Initial files: {len(initial_files)}")
        
        try:
            while True:
                current_files = set(os.listdir(captures_path))
                new_files = current_files - initial_files
                
                if new_files:
                    print(f"\n📸 NEW FILES DETECTED: {new_files}")
                    for file in new_files:
                        file_path = os.path.join(captures_path, file)
                        file_size = os.path.getsize(file_path)
                        print(f"   - {file} ({file_size} bytes)")
                
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
    else:
        print("❌ Cannot monitor - captures folder not found")

if __name__ == "__main__":
    debug_image_capture() 