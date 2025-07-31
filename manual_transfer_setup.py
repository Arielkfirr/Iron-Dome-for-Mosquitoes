#!/usr/bin/env python3
"""
Manual Transfer Setup
Help manually transfer photos and set up the integration
"""

import os
import sys
import shutil
import cv2
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def setup_manual_transfer():
    """Set up manual photo transfer"""
    print("📱 MANUAL PHOTO TRANSFER SETUP")
    print("=" * 50)
    
    print("🔧 STEP-BY-STEP INSTRUCTIONS:")
    print("=" * 30)
    
    print("\n1. 📱 ON YOUR PHONE:")
    print("   - Open your photo gallery")
    print("   - Find the photo: 20250731_030450.jpg")
    print("   - Share it via one of these methods:")
    print("     • Email it to yourself")
    print("     • Upload to cloud storage (OneDrive, Google Drive)")
    print("     • Use USB cable to transfer")
    print("     • Use AirDrop or similar if available")
    
    print("\n2. 💻 ON YOUR PC:")
    print("   - Download the photo to your PC")
    print("   - Copy it to this folder:")
    print("   - C:\\Users\\Ariel\\PycharmProjects\\RaspberryPie\\IronDomeMosquitoes\\data\\captures")
    
    print("\n3. 🧪 TEST THE TRANSFER:")
    print("   - Run this script again to test")
    print("   - The photo will be processed automatically")
    
    # Check if the photo is already in captures
    capture_folder = "data/captures"
    target_filename = "20250731_030450.jpg"
    target_path = os.path.join(capture_folder, target_filename)
    
    if os.path.exists(target_path):
        print(f"\n✅ FOUND YOUR PHOTO: {target_filename}")
        file_size = os.path.getsize(target_path)
        print(f"📏 Size: {file_size} bytes")
        
        # Test if it can be loaded
        try:
            img = cv2.imread(target_path)
            if img is not None:
                print(f"✅ Image can be loaded ({img.shape[1]}x{img.shape[0]})")
                return True
            else:
                print("❌ Image cannot be loaded")
                return False
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return False
    else:
        print(f"\n❌ Photo not found: {target_filename}")
        print("📱 Please transfer the photo to the captures folder")
        return False

def process_transferred_photo():
    """Process the transferred photo"""
    print("\n🔍 PROCESSING TRANSFERRED PHOTO")
    print("=" * 40)
    
    capture_folder = "data/captures"
    target_filename = "20250731_030450.jpg"
    target_path = os.path.join(capture_folder, target_filename)
    
    if not os.path.exists(target_path):
        print(f"❌ Photo not found: {target_filename}")
        return False
    
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
        
        # Load and process image
        img = cv2.imread(target_path)
        if img is not None:
            print(f"✅ Image loaded ({img.shape[1]}x{img.shape[0]})")
            
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
            
            print(f"\n🎉 SUCCESS! Photo processed successfully!")
            print(f"📱 Now you can take more photos and they will be processed automatically")
            return True
        else:
            print("❌ Failed to load image")
            return False
            
    except Exception as e:
        print(f"❌ Error processing photo: {e}")
        import traceback
        traceback.print_exc()
        return False

def setup_automatic_monitoring():
    """Set up automatic monitoring for future photos"""
    print("\n🔄 SETTING UP AUTOMATIC MONITORING")
    print("=" * 40)
    
    print("📱 Once your photo is working, you can:")
    print("1. Take new photos with your phone")
    print("2. Transfer them to the captures folder")
    print("3. Run the monitoring script to process them automatically")
    
    print("\n📁 The captures folder is:")
    print("C:\\Users\\Ariel\\PycharmProjects\\RaspberryPie\\IronDomeMosquitoes\\data\\captures")
    
    print("\n🧪 To test automatic processing:")
    print("1. Copy a new photo to the captures folder")
    print("2. Run: python process_photos.py")
    print("3. Choose option 1 to process existing photos")

def main():
    """Main function"""
    print("📱 MANUAL PHOTO TRANSFER AND PROCESSING")
    print("=" * 50)
    
    # Check if photo is already transferred
    if setup_manual_transfer():
        print("\n✅ Photo is ready for processing!")
        
        # Process the photo
        if process_transferred_photo():
            print("\n🎉 SUCCESS! Integration is working!")
            
            # Set up automatic monitoring
            setup_automatic_monitoring()
        else:
            print("\n❌ Failed to process photo")
            print("📱 Please check the error messages above")
    else:
        print("\n📱 Please transfer your photo first")
        print("📁 Target location: data/captures/20250731_030450.jpg")

if __name__ == "__main__":
    main() 