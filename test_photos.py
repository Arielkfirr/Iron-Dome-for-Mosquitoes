#!/usr/bin/env python3
"""
Quick test to process existing photos
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_existing_photos():
    """Test processing existing photos"""
    print("🦟 Testing existing photos...")
    
    try:
        from detection.mosquito_detector import MosquitoDetector
        from utils.config_loader import ConfigLoader
        
        # Load config
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        # Initialize detector
        detector = MosquitoDetector(config)
        detector.initialize()
        
        # Check captures folder
        capture_folder = "data/captures"
        if os.path.exists(capture_folder):
            files = os.listdir(capture_folder)
            print(f"📸 Found {len(files)} files in captures folder:")
            
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(capture_folder, file)
                    print(f"\n🔍 Processing: {file}")
                    
                    try:
                        results = detector.detect_image(file_path)
                        if results and results.get('detections'):
                            print(f"🦟 Found {len(results['detections'])} mosquitoes!")
                            for detection in results['detections']:
                                print(f"   - Confidence: {detection.get('confidence', 0):.3f}")
                        else:
                            print("✅ No mosquitoes detected in this photo")
                            
                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")
        else:
            print("❌ Captures folder not found")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_existing_photos() 