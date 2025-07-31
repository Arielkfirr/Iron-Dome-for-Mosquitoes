#!/usr/bin/env python3
"""
Setup Phone Link Transfer
Help set up Phone Link to transfer photos from your phone
"""

import os
import sys
import time
from pathlib import Path

def setup_phone_link():
    """Help set up Phone Link for photo transfer"""
    print("📱 PHONE LINK SETUP GUIDE")
    print("=" * 50)
    
    print("🔧 STEP-BY-STEP SETUP:")
    print("=" * 30)
    
    print("\n1. 📱 OPEN PHONE LINK ON PC:")
    print("   - Press Windows key")
    print("   - Type 'Phone Link'")
    print("   - Click on 'Phone Link' app")
    
    print("\n2. 🔗 CONNECT YOUR PHONE:")
    print("   - Make sure your phone is connected to the same WiFi")
    print("   - In Phone Link, click 'Get started'")
    print("   - Follow the pairing instructions")
    print("   - Make sure your phone shows as 'Connected'")
    
    print("\n3. 📷 ENABLE CAMERA FEATURE:")
    print("   - In Phone Link, click on 'Camera'")
    print("   - Grant camera permissions if prompted")
    print("   - You should see your phone's camera view")
    
    print("\n4. 📸 TAKE A TEST PHOTO:")
    print("   - Click the camera button in Phone Link")
    print("   - Take a photo with your phone")
    print("   - The photo should appear in the Phone Link interface")
    
    print("\n5. 📁 CHECK PHOTO TRANSFER:")
    print("   - Photos should automatically save to:")
    print("   - C:\\Users\\Ariel\\PycharmProjects\\RaspberryPie\\IronDomeMosquitoes\\data\\captures")
    
    print("\n6. 🧪 TEST THE TRANSFER:")
    print("   - Take another photo with your phone")
    print("   - Check if it appears in the captures folder")
    print("   - Run the monitoring script to detect it")

def check_phone_link_status():
    """Check if Phone Link is working"""
    print("\n🔍 CHECKING PHONE LINK STATUS")
    print("=" * 40)
    
    capture_folder = "data/captures"
    
    if not os.path.exists(capture_folder):
        print("❌ Captures folder not found")
        print("📱 Please set up Phone Link first")
        return False
    
    # Get current files
    files = os.listdir(capture_folder)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📸 Current photos in captures folder: {len(image_files)}")
    
    for i, file in enumerate(image_files):
        file_path = os.path.join(capture_folder, file)
        file_size = os.path.getsize(file_path)
        print(f"   {i+1}. {file} ({file_size} bytes)")
    
    # Look for recent photos (from today)
    import datetime
    today = datetime.datetime.now().strftime('%Y%m%d')
    recent_files = [f for f in image_files if today in f or '20250731' in f]
    
    if recent_files:
        print(f"\n✅ Found recent photos: {len(recent_files)}")
        for file in recent_files:
            print(f"   📸 {file}")
    else:
        print(f"\n⚠️  No recent photos found")
        print("📱 Please take a photo with Phone Link camera")
    
    return len(recent_files) > 0

def monitor_for_transfer():
    """Monitor for photo transfer from Phone Link"""
    print("\n🎯 MONITORING FOR PHOTO TRANSFER")
    print("=" * 40)
    print("📱 Instructions:")
    print("1. Make sure Phone Link is open and connected")
    print("2. Click on 'Camera' in Phone Link")
    print("3. Take a photo with your phone camera")
    print("4. Watch for the photo to appear in the captures folder")
    print("5. Press Ctrl+C to stop monitoring")
    
    capture_folder = "data/captures"
    initial_files = set(os.listdir(capture_folder))
    
    print(f"\n📸 Initial files: {len(initial_files)}")
    print("⏳ Waiting for new photos...")
    
    try:
        while True:
            current_files = set(os.listdir(capture_folder))
            new_files = current_files - initial_files
            
            if new_files:
                print(f"\n🎉 NEW FILES DETECTED!")
                for file in new_files:
                    file_path = os.path.join(capture_folder, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   📸 {file} ({file_size} bytes)")
                
                # Check if any are images
                new_images = [f for f in new_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if new_images:
                    print(f"✅ {len(new_images)} new image(s) transferred!")
                    return True
            
            print(".", end="", flush=True)
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
        return False

def manual_transfer_guide():
    """Guide for manual photo transfer"""
    print("\n📋 MANUAL TRANSFER GUIDE")
    print("=" * 30)
    
    print("If Phone Link isn't working, you can manually transfer photos:")
    print("\n1. 📱 On your phone:")
    print("   - Open your photo gallery")
    print("   - Find the photo you just took")
    print("   - Share it via email, cloud storage, or USB")
    
    print("\n2. 💻 On your PC:")
    print("   - Copy the photo to:")
    print("   - C:\\Users\\Ariel\\PycharmProjects\\RaspberryPie\\IronDomeMosquitoes\\data\\captures")
    
    print("\n3. 🧪 Test the photo:")
    print("   - Run the photo processing script")
    print("   - Check if the photo can be loaded and processed")

if __name__ == "__main__":
    print("📱 PHONE LINK TRANSFER SETUP")
    print("=" * 50)
    
    print("Choose an option:")
    print("1. Setup Phone Link guide")
    print("2. Check Phone Link status")
    print("3. Monitor for photo transfer")
    print("4. Manual transfer guide")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        setup_phone_link()
    elif choice == "2":
        check_phone_link_status()
    elif choice == "3":
        monitor_for_transfer()
    elif choice == "4":
        manual_transfer_guide()
    else:
        print("Invalid choice") 