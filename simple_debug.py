#!/usr/bin/env python3
"""
Simple debug script for phone link
"""

import os
import sys

print("🔍 Simple Phone Link Debug")
print("=" * 30)

# Check current directory
print(f"Current directory: {os.getcwd()}")

# Check if IronDomeMosquitoes directory exists
iron_dome_path = "IronDomeMosquitoes"
if os.path.exists(iron_dome_path):
    print(f"✅ IronDomeMosquitoes directory exists")
    
    # Check data/captures folder
    captures_path = os.path.join(iron_dome_path, "data", "captures")
    if os.path.exists(captures_path):
        print(f"✅ Captures folder exists: {captures_path}")
        files = os.listdir(captures_path)
        print(f"📸 Found {len(files)} files:")
        for file in files:
            file_path = os.path.join(captures_path, file)
            file_size = os.path.getsize(file_path)
            print(f"   - {file} ({file_size} bytes)")
    else:
        print(f"❌ Captures folder not found: {captures_path}")
else:
    print(f"❌ IronDomeMosquitoes directory not found")

# Check Python path
print(f"\nPython executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Try to import basic modules
try:
    import cv2
    print("✅ OpenCV imported successfully")
except ImportError as e:
    print(f"❌ OpenCV import failed: {e}")

try:
    from ultralytics import YOLO
    print("✅ YOLO imported successfully")
except ImportError as e:
    print(f"❌ YOLO import failed: {e}")

print("\n✅ Simple debug completed") 