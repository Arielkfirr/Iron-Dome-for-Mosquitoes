#!/usr/bin/env python3
"""
Test Cat Detection with Phone Link
Simple test script to detect cats using your phone camera via Phone Link
"""

import sys
import os
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from utils.logger import setup_logger
from utils.config_loader import ConfigLoader
from detection.mosquito_detector import MosquitoDetector
from camera.camera_manager import CameraManager

def main():
    """Test cat detection with Phone Link"""
    print("🐱 Cat Detection Test with Phone Link")
    print("=" * 50)
    
    try:
        # Setup logging
        logger = setup_logger(level="INFO")
        logger.info("Starting cat detection test")
        
        # Load configuration
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
        
        # Initialize detector
        logger.info("Initializing detector...")
        detector = MosquitoDetector(config['detection'])
        detector.initialize()
        
        # Initialize camera manager
        logger.info("Initializing camera manager...")
        camera_manager = CameraManager(config['camera'])
        camera_manager.initialize()
        
        print("\n📱 Phone Link Cat Detection Test")
        print("=" * 50)
        print("📱 Instructions:")
        print("1. Open Phone Link on your PC")
        print("2. Click on 'Camera' in Phone Link")
        print("3. Take photos of your cats with your phone camera")
        print("4. The system will automatically detect cats in the photos")
        print("5. Press Ctrl+C to stop the test")
        print("=" * 50)
        
        processed_count = 0
        cat_detections = 0
        
        while True:
            try:
                # Get frames from camera
                frames = camera_manager.get_frames()
                
                for frame_data in frames:
                    image = frame_data['image']
                    source = frame_data['source']
                    filename = frame_data.get('metadata', {}).get('filename', 'unknown')
                    
                    logger.info(f"Processing image: {filename} from {source}")
                    
                    # Run cat detection
                    cat_results = detector.detect_cats(image)
                    
                    if cat_results:
                        cat_detections += len(cat_results)
                        logger.info(f"🎉 Found {len(cat_results)} cat(s) in {filename}!")
                        
                        # Print detection details
                        for i, detection in enumerate(cat_results):
                            confidence = detection['confidence']
                            bbox = detection['bbox']
                            logger.info(f"  Cat {i+1}: Confidence {confidence:.3f}, BBox {bbox}")
                        
                        # Save annotated image
                        save_annotated_image(image, cat_results, filename)
                        
                    else:
                        logger.info(f"No cats detected in {filename}")
                    
                    processed_count += 1
                
                # Wait before checking again
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n👋 Stopping cat detection test...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(2)
        
        # Print summary
        print("\n📊 Test Summary")
        print("=" * 50)
        print(f"📸 Images processed: {processed_count}")
        print(f"🐱 Cat detections: {cat_detections}")
        print(f"📁 Images saved in: {config['camera']['phone_link']['capture_folder']}")
        print("=" * 50)
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

def save_annotated_image(image, detections, original_filename):
    """Save image with detection annotations"""
    try:
        import cv2
        
        # Create annotated image
        annotated_image = image.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            
            # Draw bounding box
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.3f}"
            cv2.putText(annotated_image, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save annotated image
        base_name = os.path.splitext(original_filename)[0]
        annotated_filename = f"{base_name}_detected.jpg"
        save_path = os.path.join("data/detections", annotated_filename)
        
        # Ensure directory exists
        os.makedirs("data/detections", exist_ok=True)
        
        cv2.imwrite(save_path, annotated_image)
        print(f"🎨 Saved annotated image: {annotated_filename}")
        
    except Exception as e:
        print(f"Error saving annotated image: {e}")

if __name__ == "__main__":
    main() 