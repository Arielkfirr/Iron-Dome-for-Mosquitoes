"""
Mosquito Detector for Iron Dome for Mosquitoes
Handles object detection including cats, mosquitoes, and other insects
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Optional
from ultralytics import YOLO
from loguru import logger
from utils.logger import LoggerMixin

class MosquitoDetector(LoggerMixin):
    """Advanced object detector for mosquitoes, cats, and other objects"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.model = None
        self.classes_to_detect = config.get('classes_to_detect', ['cat', 'mosquito', 'insect'])
        self.confidence_threshold = config.get('confidence_threshold', 0.3)
        self.iou_threshold = config.get('iou_threshold', 0.5)
        self.max_detections = config.get('max_detections_per_frame', 10)
        
        self.logger.info(f"Initializing detector with classes: {self.classes_to_detect}")
        self.logger.info(f"Confidence threshold: {self.confidence_threshold}")
    
    def initialize(self):
        """Initialize the detection model"""
        try:
            model_path = self.config.get('model_path', 'models/yolov8n.pt')
            self.logger.info(f"Loading YOLO model from: {model_path}")
            
            self.model = YOLO(model_path)
            self.logger.info("YOLO model loaded successfully")
            
            # Test model
            self._test_model()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize detector: {e}")
            raise
    
    def _test_model(self):
        """Test the model with a simple inference"""
        try:
            # Create a test image (black image)
            test_image = np.zeros((640, 640, 3), dtype=np.uint8)
            
            # Run inference
            results = self.model(test_image, conf=self.confidence_threshold, iou=self.iou_threshold)
            
            self.logger.info("Model test successful")
            self.logger.info(f"Available classes: {list(self.model.names.values())}")
            
        except Exception as e:
            self.logger.error(f"Model test failed: {e}")
            raise
    
    def detect(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect objects in the given image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of detection results
        """
        try:
            if self.model is None:
                self.logger.error("Model not initialized")
                return []
            
            # Run detection
            results = self.model(
                image, 
                conf=self.confidence_threshold, 
                iou=self.iou_threshold,
                max_det=self.max_detections
            )
            
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get detection info
                        confidence = float(box.conf[0].item())
                        class_id = int(box.cls[0].item())
                        class_name = self.model.names[class_id]
                        
                        # Get bounding box coordinates
                        bbox = box.xyxy[0].cpu().numpy().tolist()
                        
                        # Create detection result
                        detection = {
                            'class_name': class_name,
                            'class_id': class_id,
                            'confidence': confidence,
                            'bbox': bbox,
                            'timestamp': self._get_timestamp()
                        }
                        
                        detections.append(detection)
                        
                        # Log detection
                        self.logger.info(f"Detected {class_name} with confidence {confidence:.3f}")
            
            return detections
            
        except Exception as e:
            self.logger.error(f"Detection failed: {e}")
            return []
    
    def detect_cats(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Specifically detect cats in the image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of cat detections
        """
        all_detections = self.detect(image)
        cat_detections = [d for d in all_detections if d['class_name'] == 'cat']
        
        if cat_detections:
            self.logger.info(f"Found {len(cat_detections)} cat(s)")
        
        return cat_detections
    
    def detect_mosquitoes(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Specifically detect mosquitoes and insects in the image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of mosquito/insect detections
        """
        all_detections = self.detect(image)
        mosquito_detections = [
            d for d in all_detections 
            if d['class_name'] in ['mosquito', 'insect', 'fly']
        ]
        
        if mosquito_detections:
            self.logger.info(f"Found {len(mosquito_detections)} mosquito(s)/insect(s)")
        
        return mosquito_detections
    
    def get_detection_summary(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get a summary of detections
        
        Args:
            detections: List of detection results
            
        Returns:
            Summary dictionary
        """
        if not detections:
            return {
                'total_detections': 0,
                'classes_found': [],
                'highest_confidence': 0.0
            }
        
        # Count by class
        class_counts = {}
        confidences = []
        
        for detection in detections:
            class_name = detection['class_name']
            confidence = detection['confidence']
            
            if class_name not in class_counts:
                class_counts[class_name] = 0
            class_counts[class_name] += 1
            confidences.append(confidence)
        
        return {
            'total_detections': len(detections),
            'classes_found': list(class_counts.keys()),
            'class_counts': class_counts,
            'highest_confidence': max(confidences) if confidences else 0.0,
            'average_confidence': sum(confidences) / len(confidences) if confidences else 0.0
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def check_health(self) -> Dict[str, Any]:
        """Check the health of the detector"""
        try:
            if self.model is None:
                return {
                    'healthy': False,
                    'message': 'Model not initialized'
                }
            
            # Test with a simple image
            test_image = np.zeros((100, 100, 3), dtype=np.uint8)
            results = self.model(test_image, conf=0.1)
            
            return {
                'healthy': True,
                'message': 'Detector is working properly',
                'model_loaded': True,
                'available_classes': len(self.model.names)
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Health check failed: {e}'
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current detector status"""
        return {
            'model_loaded': self.model is not None,
            'classes_to_detect': self.classes_to_detect,
            'confidence_threshold': self.confidence_threshold,
            'iou_threshold': self.iou_threshold,
            'max_detections': self.max_detections
        }
    
    def shutdown(self):
        """Shutdown the detector"""
        self.logger.info("Shutting down detector")
        self.model = None 