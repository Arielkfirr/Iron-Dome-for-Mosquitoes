#!/usr/bin/env python3
"""
Debug Paths and Image Access
Check if we can access the images and debug path issues
"""

import os
import sys
from pathlib import Path

def debug_paths():
    """Debug file paths and image access"""
    print("🔍 DEBUGGING PATHS AND IMAGE ACCESS")
    print("=" * 50)
    
    # Check current working directory
    print(f"📁 Current working directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    if "IronDomeMosquitoes" not in os.getcwd():
        print("❌ Not in IronDomeMosquitoes directory")
        return
    
    print("✅ We're in the IronDomeMosquitoes directory")
    
    # Check if data/captures folder exists
    capture_folder = "data/captures"
    print(f"\n📁 Checking captures folder: {capture_folder}")
    
    if not os.path.exists(capture_folder):
        print(f"❌ Captures folder does not exist: {capture_folder}")
        return
    
    print(f"✅ Captures folder exists: {capture_folder}")
    
    # Get absolute path
    abs_capture_path = os.path.abspath(capture_folder)
    print(f"📁 Absolute path: {abs_capture_path}")
    
    # Check if we can read the directory
    try:
        files = os.listdir(capture_folder)
        print(f"✅ Can read directory, found {len(files)} files")
    except PermissionError:
        print("❌ Permission denied reading directory")
        return
    except Exception as e:
        print(f"❌ Error reading directory: {e}")
        return
    
    # List all files
    print(f"\n📄 Files in captures folder:")
    for i, file in enumerate(files):
        file_path = os.path.join(capture_folder, file)
        try:
            file_size = os.path.getsize(file_path)
            print(f"   {i+1}. {file} ({file_size} bytes)")
        except Exception as e:
            print(f"   {i+1}. {file} (Error getting size: {e})")
    
    # Check image files specifically
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"\n📸 Image files found: {len(image_files)}")
    
    for i, file in enumerate(image_files):
        file_path = os.path.join(capture_folder, file)
        abs_file_path = os.path.abspath(file_path)
        
        print(f"\n🔍 Testing file {i+1}: {file}")
        print(f"   📁 Relative path: {file_path}")
        print(f"   📁 Absolute path: {abs_file_path}")
        
        # Check if file exists
        if os.path.exists(file_path):
            print("   ✅ File exists")
        else:
            print("   ❌ File does not exist")
            continue
        
        # Check if we can read the file
        try:
            with open(file_path, 'rb') as f:
                first_bytes = f.read(10)
                print(f"   ✅ Can read file (first 10 bytes: {first_bytes})")
        except PermissionError:
            print("   ❌ Permission denied reading file")
            continue
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            continue
        
        # Check file size
        try:
            file_size = os.path.getsize(file_path)
            print(f"   📏 File size: {file_size} bytes")
            
            if file_size < 100:
                print("   ⚠️  File is very small, might be corrupted or empty")
            elif file_size > 1000000:
                print("   ✅ File size looks good (over 1MB)")
            else:
                print("   ✅ File size looks reasonable")
                
        except Exception as e:
            print(f"   ❌ Error getting file size: {e}")
        
        # Try to load with OpenCV
        try:
            import cv2
            img = cv2.imread(file_path)
            if img is not None:
                print(f"   ✅ OpenCV can load image ({img.shape[1]}x{img.shape[0]})")
            else:
                print("   ❌ OpenCV cannot load image")
        except ImportError:
            print("   ⚠️  OpenCV not available")
        except Exception as e:
            print(f"   ❌ Error loading with OpenCV: {e}")

def test_image_loading():
    """Test loading images with different methods"""
    print("\n🧪 TESTING IMAGE LOADING")
    print("=" * 50)
    
    capture_folder = "data/captures"
    if not os.path.exists(capture_folder):
        print("❌ Captures folder not found")
        return
    
    files = os.listdir(capture_folder)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("❌ No image files found")
        return
    
    # Test with the first image file
    test_file = image_files[0]
    test_path = os.path.join(capture_folder, test_file)
    
    print(f"🔍 Testing with: {test_file}")
    print(f"📁 Path: {test_path}")
    
    # Method 1: Basic file read
    try:
        with open(test_path, 'rb') as f:
            data = f.read()
            print(f"✅ Basic file read: {len(data)} bytes")
    except Exception as e:
        print(f"❌ Basic file read failed: {e}")
        return
    
    # Method 2: OpenCV
    try:
        import cv2
        img = cv2.imread(test_path)
        if img is not None:
            print(f"✅ OpenCV load: {img.shape[1]}x{img.shape[0]} pixels")
            print(f"   Data type: {img.dtype}")
            print(f"   Memory usage: {img.nbytes} bytes")
        else:
            print("❌ OpenCV load failed")
    except Exception as e:
        print(f"❌ OpenCV load error: {e}")
    
    # Method 3: PIL (if available)
    try:
        from PIL import Image
        pil_img = Image.open(test_path)
        print(f"✅ PIL load: {pil_img.size[0]}x{pil_img.size[1]} pixels")
        print(f"   Mode: {pil_img.mode}")
    except ImportError:
        print("⚠️  PIL not available")
    except Exception as e:
        print(f"❌ PIL load error: {e}")

if __name__ == "__main__":
    debug_paths()
    test_image_loading() 