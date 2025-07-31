#!/usr/bin/env python3
"""
Find and Process Phone Images
Search for specific images using Phone Link paths and process them
"""

import os
import sys
import shutil
import cv2
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def find_phone_images():
    """Find images from Phone Link using common paths"""
    print("🔍 SEARCHING FOR PHONE IMAGES")
    print("=" * 50)
    
    # Common Phone Link paths to search
    phone_link_paths = [
        # Windows Phone Link default paths
        os.path.expanduser("~/Pictures/Phone Link"),
        os.path.expanduser("~/Downloads/Phone Link"),
        os.path.expanduser("~/Documents/Phone Link"),
        "C:/Users/Ariel/Pictures/Phone Link",
        "C:/Users/Ariel/Downloads/Phone Link",
        "C:/Users/Ariel/Documents/Phone Link",
        # Alternative paths
        os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Downloads"),
        # Current captures folder
        "data/captures"
    ]
    
    target_filename = "20250731_030450.jpg"
    found_images = []
    
    print(f"🎯 Looking for: {target_filename}")
    print("📁 Searching in Phone Link paths...")
    
    for search_path in phone_link_paths:
        if os.path.exists(search_path):
            print(f"\n📁 Checking: {search_path}")
            try:
                files = os.listdir(search_path)
                image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                # Look for the specific target file
                if target_filename in files:
                    file_path = os.path.join(search_path, target_filename)
                    file_size = os.path.getsize(file_path)
                    print(f"   ✅ FOUND TARGET: {target_filename} ({file_size} bytes)")
                    found_images.append((file_path, target_filename, file_size))
                
                # Also look for any recent images (from today)
                recent_files = [f for f in image_files if '20250731' in f or '2025-07-31' in f]
                for file in recent_files:
                    if file != target_filename:  # Don't duplicate
                        file_path = os.path.join(search_path, file)
                        file_size = os.path.getsize(file_path)
                        print(f"   📸 Recent: {file} ({file_size} bytes)")
                        found_images.append((file_path, file, file_size))
                        
            except Exception as e:
                print(f"   ❌ Error reading {search_path}: {e}")
        else:
            print(f"   ❌ Path not found: {search_path}")
    
    return found_images

def copy_to_captures(image_path, filename):
    """Copy image to captures folder"""
    capture_folder = "data/captures"
    
    if not os.path.exists(capture_folder):
        os.makedirs(capture_folder)
    
    dest_path = os.path.join(capture_folder, filename)
    
    try:
        shutil.copy2(image_path, dest_path)
        print(f"✅ Copied {filename} to captures folder")
        return dest_path
    except Exception as e:
        print(f"❌ Error copying {filename}: {e}")
        return None

def process_image(image_path, filename):
    """Process image with mosquito detection"""
    print(f"\n🔍 PROCESSING: {filename}")
    print("=" * 40)
    
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
        img = cv2.imread(image_path)
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
        else:
            print("❌ Failed to load image")
            
        return True
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to find and process phone images"""
    print("📱 PHONE IMAGE FINDER AND PROCESSOR")
    print("=" * 50)
    
    # Step 1: Find images
    found_images = find_phone_images()
    
    if not found_images:
        print("\n❌ No images found!")
        print("📱 Please make sure:")
        print("   - Phone Link is properly connected")
        print("   - Photos are being saved to a known location")
        print("   - The photo filename is correct")
        return
    
    print(f"\n✅ Found {len(found_images)} image(s)")
    
    # Step 2: Process each image
    successful_processing = []
    
    for image_path, filename, file_size in found_images:
        print(f"\n📸 Processing: {filename}")
        print(f"   📁 Path: {image_path}")
        print(f"   📏 Size: {file_size} bytes")
        
        # Copy to captures folder
        captures_path = copy_to_captures(image_path, filename)
        
        if captures_path:
            # Process the image
            if process_image(captures_path, filename):
                successful_processing.append(filename)
                print(f"✅ Successfully processed: {filename}")
            else:
                print(f"❌ Failed to process: {filename}")
        else:
            print(f"❌ Failed to copy: {filename}")
    
    # Summary
    print(f"\n📊 PROCESSING SUMMARY")
    print("=" * 30)
    print(f"📸 Total images found: {len(found_images)}")
    print(f"✅ Successfully processed: {len(successful_processing)}")
    
    if successful_processing:
        print(f"\n🎉 SUCCESS! Processed images:")
        for filename in successful_processing:
            print(f"   - {filename}")
        
        # Now we can apply to other recent images
        print(f"\n🔄 Ready to process other recent images!")
        print("📱 Take more photos with your phone and they will be processed automatically")
    else:
        print(f"\n❌ No images were successfully processed")
        print("📱 Please check the error messages above")

if __name__ == "__main__":
    main() 