"""
Camera Manager for Iron Dome for Mosquitoes
Handles different camera sources including Phone Link, USB cameras, and IP cameras
"""

import cv2
import os
import glob
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger
from utils.logger import LoggerMixin

class CameraManager(LoggerMixin):
    """Manages different camera sources and image capture"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.cameras = {}
        self.phone_link_folder = config.get('phone_link', {}).get('capture_folder', 'data/captures')
        self.processed_files = set()
        
        self.logger.info("Initializing camera manager")
    
    def initialize(self):
        """Initialize camera systems"""
        try:
            # Create capture folders
            self._create_folders()
            
            # Initialize phone link monitoring
            if self.config.get('phone_link', {}).get('enabled', True):
                self._setup_phone_link()
            
            # Initialize USB camera if enabled
            if self.config.get('usb_camera', {}).get('enabled', False):
                self._setup_usb_camera()
            
            # Initialize IP camera if enabled
            if self.config.get('ip_camera', {}).get('enabled', False):
                self._setup_ip_camera()
            
            self.logger.info("Camera manager initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize camera manager: {e}")
            raise
    
    def _create_folders(self):
        """Create necessary folders for image capture"""
        folders = [
            self.phone_link_folder,
            'data/detections',
            'data/processed'
        ]
        
        for folder in folders:
            Path(folder).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created folder: {folder}")
    
    def _setup_phone_link(self):
        """Setup Phone Link monitoring"""
        self.logger.info("Setting up Phone Link monitoring")
        self.logger.info(f"Phone Link folder: {self.phone_link_folder}")
        
        # Ensure folder exists
        Path(self.phone_link_folder).mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Phone Link setup complete")
        self.logger.info("📱 Instructions for Phone Link:")
        self.logger.info("1. Open Phone Link on your PC")
        self.logger.info("2. Click on 'Camera' in Phone Link")
        self.logger.info("3. Take photos with your phone camera")
        self.logger.info("4. Photos will be automatically detected and processed")
    
    def _setup_usb_camera(self):
        """Setup USB camera"""
        usb_config = self.config.get('usb_camera', {})
        device_id = usb_config.get('device_id', 0)
        
        try:
            cap = cv2.VideoCapture(device_id)
            if cap.isOpened():
                # Set resolution
                resolution = usb_config.get('resolution', [1920, 1080])
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
                
                # Set FPS
                fps = usb_config.get('fps', 30)
                cap.set(cv2.CAP_PROP_FPS, fps)
                
                self.cameras['usb'] = cap
                self.logger.info(f"USB camera initialized (device {device_id})")
            else:
                self.logger.warning(f"Could not open USB camera (device {device_id})")
                
        except Exception as e:
            self.logger.error(f"Failed to setup USB camera: {e}")
    
    def _setup_ip_camera(self):
        """Setup IP camera"""
        ip_config = self.config.get('ip_camera', {})
        url = ip_config.get('url', '')
        
        if not url:
            self.logger.warning("IP camera URL not provided")
            return
        
        try:
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                self.cameras['ip'] = cap
                self.logger.info(f"IP camera initialized: {url}")
            else:
                self.logger.warning(f"Could not open IP camera: {url}")
                
        except Exception as e:
            self.logger.error(f"Failed to setup IP camera: {e}")
    
    def get_frames(self) -> List[Dict[str, Any]]:
        """
        Get frames from all available camera sources
        
        Returns:
            List of frame data with metadata
        """
        frames = []
        
        # Get frames from Phone Link
        phone_frames = self._get_phone_link_frames()
        frames.extend(phone_frames)
        
        # Get frames from USB camera
        if 'usb' in self.cameras:
            usb_frame = self._get_usb_frame()
            if usb_frame:
                frames.append(usb_frame)
        
        # Get frames from IP camera
        if 'ip' in self.cameras:
            ip_frame = self._get_ip_frame()
            if ip_frame:
                frames.append(ip_frame)
        
        return frames
    
    def _get_phone_link_frames(self) -> List[Dict[str, Any]]:
        """Get new images from Phone Link folder"""
        frames = []
        
        try:
            # Look for new image files
            image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
            image_files = []
            
            for ext in image_extensions:
                pattern = os.path.join(self.phone_link_folder, ext)
                image_files.extend(glob.glob(pattern))
            
            for image_file in image_files:
                if image_file not in self.processed_files:
                    try:
                        # Read image
                        image = cv2.imread(image_file)
                        if image is not None:
                            frame_data = {
                                'source': 'phone_link',
                                'file_path': image_file,
                                'image': image,
                                'timestamp': time.time(),
                                'metadata': {
                                    'filename': os.path.basename(image_file),
                                    'size': os.path.getsize(image_file),
                                    'dimensions': image.shape
                                }
                            }
                            frames.append(frame_data)
                            
                            self.logger.info(f"New image from Phone Link: {os.path.basename(image_file)}")
                            
                            # Mark as processed
                            self.processed_files.add(image_file)
                            
                    except Exception as e:
                        self.logger.error(f"Failed to process image {image_file}: {e}")
        
        except Exception as e:
            self.logger.error(f"Error reading Phone Link frames: {e}")
        
        return frames
    
    def _get_usb_frame(self) -> Optional[Dict[str, Any]]:
        """Get frame from USB camera"""
        try:
            cap = self.cameras['usb']
            ret, frame = cap.read()
            
            if ret:
                return {
                    'source': 'usb_camera',
                    'image': frame,
                    'timestamp': time.time(),
                    'metadata': {
                        'dimensions': frame.shape,
                        'device_id': self.config.get('usb_camera', {}).get('device_id', 0)
                    }
                }
        
        except Exception as e:
            self.logger.error(f"Error reading USB camera: {e}")
        
        return None
    
    def _get_ip_frame(self) -> Optional[Dict[str, Any]]:
        """Get frame from IP camera"""
        try:
            cap = self.cameras['ip']
            ret, frame = cap.read()
            
            if ret:
                return {
                    'source': 'ip_camera',
                    'image': frame,
                    'timestamp': time.time(),
                    'metadata': {
                        'dimensions': frame.shape,
                        'url': self.config.get('ip_camera', {}).get('url', '')
                    }
                }
        
        except Exception as e:
            self.logger.error(f"Error reading IP camera: {e}")
        
        return None
    
    def save_frame(self, frame_data: Dict[str, Any], filename: str = None) -> str:
        """
        Save a frame to disk
        
        Args:
            frame_data: Frame data dictionary
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        try:
            if filename is None:
                timestamp = int(time.time())
                filename = f"frame_{timestamp}.jpg"
            
            # Determine save path based on source
            source = frame_data.get('source', 'unknown')
            if source == 'phone_link':
                save_dir = self.phone_link_folder
            else:
                save_dir = 'data/processed'
            
            file_path = os.path.join(save_dir, filename)
            
            # Save image
            cv2.imwrite(file_path, frame_data['image'])
            
            self.logger.info(f"Saved frame: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Failed to save frame: {e}")
            return ""
    
    def get_status(self) -> Dict[str, Any]:
        """Get current camera status"""
        status = {
            'phone_link_enabled': self.config.get('phone_link', {}).get('enabled', True),
            'phone_link_folder': self.phone_link_folder,
            'processed_files_count': len(self.processed_files),
            'active_cameras': list(self.cameras.keys())
        }
        
        # Add camera-specific status
        for camera_name, camera in self.cameras.items():
            if hasattr(camera, 'isOpened'):
                status[f'{camera_name}_connected'] = camera.isOpened()
        
        return status
    
    def check_health(self) -> Dict[str, Any]:
        """Check the health of camera systems"""
        try:
            # Check Phone Link folder
            phone_link_ok = os.path.exists(self.phone_link_folder)
            
            # Check USB camera
            usb_camera_ok = False
            if 'usb' in self.cameras:
                usb_camera_ok = self.cameras['usb'].isOpened()
            
            # Check IP camera
            ip_camera_ok = False
            if 'ip' in self.cameras:
                ip_camera_ok = self.cameras['ip'].isOpened()
            
            overall_health = phone_link_ok or usb_camera_ok or ip_camera_ok
            
            return {
                'healthy': overall_health,
                'message': 'Camera systems operational' if overall_health else 'No camera systems available',
                'phone_link_ok': phone_link_ok,
                'usb_camera_ok': usb_camera_ok,
                'ip_camera_ok': ip_camera_ok
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Camera health check failed: {e}'
            }
    
    def shutdown(self):
        """Shutdown camera systems"""
        self.logger.info("Shutting down camera manager")
        
        # Release camera resources
        for camera_name, camera in self.cameras.items():
            try:
                camera.release()
                self.logger.info(f"Released {camera_name} camera")
            except Exception as e:
                self.logger.error(f"Error releasing {camera_name} camera: {e}")
        
        self.cameras.clear() 