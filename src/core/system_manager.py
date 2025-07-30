"""
System Manager for Iron Dome for Mosquitoes
Coordinates all system components and manages the overall system state
"""

import threading
import time
from typing import Dict, Any
from loguru import logger

from detection.mosquito_detector import MosquitoDetector
from camera.camera_manager import CameraManager
from prevention.prevention_manager import PreventionManager
from monitoring.monitoring_manager import MonitoringManager
from web.web_interface import WebInterface
from database.database_manager import DatabaseManager

class SystemManager:
    """Main system manager that coordinates all components"""
    
    def __init__(self, config: Dict[str, Any], mode: str = "default"):
        self.config = config
        self.mode = mode
        self.running = False
        self.components = {}
        self.threads = {}
        
        # Initialize component managers
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all system components"""
        logger.info("Initializing system components...")
        
        try:
            # Database manager
            self.components['database'] = DatabaseManager(self.config['database'])
            
            # Camera manager
            self.components['camera'] = CameraManager(self.config['camera'])
            
            # Detection system
            self.components['detector'] = MosquitoDetector(self.config['detection'])
            
            # Prevention system
            self.components['prevention'] = PreventionManager(self.config['prevention'])
            
            # Monitoring system
            self.components['monitoring'] = MonitoringManager(self.config['monitoring'])
            
            # Web interface
            if self.config['web_interface']['enabled']:
                self.components['web'] = WebInterface(self.config['web_interface'])
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def initialize(self):
        """Initialize the system and all components"""
        logger.info("Starting system initialization...")
        
        try:
            # Initialize database
            self.components['database'].initialize()
            logger.info("Database initialized")
            
            # Initialize camera system
            self.components['camera'].initialize()
            logger.info("Camera system initialized")
            
            # Initialize detection system
            self.components['detector'].initialize()
            logger.info("Detection system initialized")
            
            # Initialize prevention system
            self.components['prevention'].initialize()
            logger.info("Prevention system initialized")
            
            # Initialize monitoring system
            self.components['monitoring'].initialize()
            logger.info("Monitoring system initialized")
            
            # Initialize web interface if enabled
            if 'web' in self.components:
                self.components['web'].initialize()
                logger.info("Web interface initialized")
            
            logger.info("System initialization completed successfully")
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            raise
    
    def run(self):
        """Run the main system loop"""
        logger.info("Starting Iron Dome for Mosquitoes system...")
        self.running = True
        
        try:
            # Start camera monitoring thread
            self._start_camera_thread()
            
            # Start detection processing thread
            self._start_detection_thread()
            
            # Start prevention monitoring thread
            self._start_prevention_thread()
            
            # Start web interface if enabled
            if 'web' in self.components:
                self._start_web_thread()
            
            # Main system loop
            self._main_loop()
            
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"System error: {e}")
        finally:
            self.shutdown()
    
    def _start_camera_thread(self):
        """Start camera monitoring thread"""
        def camera_worker():
            while self.running:
                try:
                    frames = self.components['camera'].get_frames()
                    if frames:
                        self.components['monitoring'].process_frames(frames)
                except Exception as e:
                    logger.error(f"Camera thread error: {e}")
                time.sleep(0.1)
        
        self.threads['camera'] = threading.Thread(target=camera_worker, daemon=True)
        self.threads['camera'].start()
        logger.info("Camera monitoring thread started")
    
    def _start_detection_thread(self):
        """Start detection processing thread"""
        def detection_worker():
            while self.running:
                try:
                    # Get frames from monitoring
                    frames = self.components['monitoring'].get_pending_frames()
                    
                    for frame in frames:
                        # Run detection
                        detections = self.components['detector'].detect(frame)
                        
                        if detections:
                            # Process detections
                            self.components['prevention'].process_detections(detections)
                            self.components['monitoring'].log_detections(detections)
                            
                            # Save to database
                            self.components['database'].save_detections(detections)
                            
                except Exception as e:
                    logger.error(f"Detection thread error: {e}")
                time.sleep(0.5)
        
        self.threads['detection'] = threading.Thread(target=detection_worker, daemon=True)
        self.threads['detection'].start()
        logger.info("Detection processing thread started")
    
    def _start_prevention_thread(self):
        """Start prevention monitoring thread"""
        def prevention_worker():
            while self.running:
                try:
                    # Check prevention status
                    self.components['prevention'].check_status()
                    
                    # Update monitoring
                    self.components['monitoring'].update_prevention_status(
                        self.components['prevention'].get_status()
                    )
                    
                except Exception as e:
                    logger.error(f"Prevention thread error: {e}")
                time.sleep(1.0)
        
        self.threads['prevention'] = threading.Thread(target=prevention_worker, daemon=True)
        self.threads['prevention'].start()
        logger.info("Prevention monitoring thread started")
    
    def _start_web_thread(self):
        """Start web interface thread"""
        def web_worker():
            try:
                self.components['web'].run()
            except Exception as e:
                logger.error(f"Web interface error: {e}")
        
        self.threads['web'] = threading.Thread(target=web_worker, daemon=True)
        self.threads['web'].start()
        logger.info("Web interface thread started")
    
    def _main_loop(self):
        """Main system loop"""
        logger.info("System is running. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                # Check system health
                self._check_system_health()
                
                # Update system status
                self._update_system_status()
                
                time.sleep(5.0)
                
        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
    
    def _check_system_health(self):
        """Check the health of all system components"""
        try:
            for name, component in self.components.items():
                if hasattr(component, 'check_health'):
                    health = component.check_health()
                    if not health['healthy']:
                        logger.warning(f"Component {name} health check failed: {health['message']}")
        except Exception as e:
            logger.error(f"Health check error: {e}")
    
    def _update_system_status(self):
        """Update system status and metrics"""
        try:
            # Get system metrics
            metrics = {
                'detections_per_minute': self.components['monitoring'].get_detection_rate(),
                'prevention_active': self.components['prevention'].is_active(),
                'camera_status': self.components['camera'].get_status(),
                'system_uptime': time.time()
            }
            
            # Update database with metrics
            self.components['database'].update_metrics(metrics)
            
        except Exception as e:
            logger.error(f"Status update error: {e}")
    
    def shutdown(self):
        """Shutdown the system gracefully"""
        logger.info("Shutting down Iron Dome for Mosquitoes system...")
        self.running = False
        
        try:
            # Shutdown components
            for name, component in self.components.items():
                if hasattr(component, 'shutdown'):
                    logger.info(f"Shutting down {name}...")
                    component.shutdown()
            
            # Wait for threads to finish
            for name, thread in self.threads.items():
                if thread.is_alive():
                    logger.info(f"Waiting for {name} thread to finish...")
                    thread.join(timeout=5.0)
            
            logger.info("System shutdown completed")
            
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'running': self.running,
            'mode': self.mode,
            'components': {name: component.get_status() for name, component in self.components.items()},
            'threads': {name: thread.is_alive() for name, thread in self.threads.items()}
        } 