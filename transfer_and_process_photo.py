#!/usr/bin/env python3
"""
Transfer and Process Photo
Transfer the specific photo and process it immediately
"""

import os
import sys
import shutil
import cv2
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def check_photo_status():
    """Check if the photo is already transferred"""
    print("📱 CHECKING PHOTO STATUS")
    print("=" * 40)
    
    target_filename = "20250731_030450.jpg"
    capture_folder = "data/captures"
    target_path = os.path.join(capture_folder, target_filename)
    
    if os.path.exists(target_path):
        file_size = os.path.getsize(target_path)
        print(f"✅ Photo found: {target_filename}")
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
        print(f"❌ Photo not found: {target_filename}")
        print("📱 Please transfer the photo first")
        return False

def process_photo():
    """Process the photo with mosquito detection"""
    print("\n🔍 PROCESSING PHOTO")
    print("=" * 40)
    
    target_filename = "20250731_030450.jpg"
    capture_folder = "data/captures"
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
            return True
        else:
            print("❌ Failed to load image")
            return False
            
    except Exception as e:
        print(f"❌ Error processing photo: {e}")
        import traceback
        traceback.print_exc()
        return False

def provide_transfer_instructions():
    """Provide clear transfer instructions"""
    print("\n📱 TRANSFER INSTRUCTIONS")
    print("=" * 40)
    
    print("🔧 To transfer your photo:")
    print("\n1. 📱 ON YOUR PHONE:")
    print("   - Open your photo gallery")
    print("   - Find the photo: 20250731_030450.jpg")
    print("   - Tap the share button (📤)")
    print("   - Choose one of these methods:")
    print("     • Email to yourself")
    print("     • Upload to OneDrive/Google Drive")
    print("     • Use USB cable")
    print("     • Use Samsung Flow or similar")
    
    print("\n2. 💻 ON YOUR PC:")
    print("   - Download the photo to your PC")
    print("   - Copy it to this exact folder:")
    print("   - C:\\Users\\Ariel\\PycharmProjects\\RaspberryPie\\IronDomeMosquitoes\\data\\captures")
    print("   - Make sure the filename is exactly: 20250731_030450.jpg")
    
    print("\n3. 🧪 TEST:")
    print("   - Run this script again")
    print("   - It will automatically process the photo")

def main():
    """Main function"""
    print("📱 PHOTO TRANSFER AND PROCESSING")
    print("=" * 50)
    
    # Check if photo is already transferred
    if check_photo_status():
        print("\n✅ Photo is ready for processing!")
        
        # Process the photo
        if process_photo():
            print("\n🎉 SUCCESS! Integration is working!")
            print("\n🔄 NEXT STEPS:")
            print("1. Take more photos with your phone")
            print("2. Transfer them to the captures folder")
            print("3. Run: python process_photos.py")
            print("4. Choose option 1 to process existing photos")
        else:
            print("\n❌ Failed to process photo")
            print("📱 Please check the error messages above")
    else:
        print("\n📱 Photo not found in captures folder")
        provide_transfer_instructions()

if __name__ == "__main__":
    main() 