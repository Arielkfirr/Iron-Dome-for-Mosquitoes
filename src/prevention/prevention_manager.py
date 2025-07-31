"""
Prevention Manager for Iron Dome for Mosquitoes
Handles mosquito prevention actions and alerting
"""

import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from loguru import logger
from utils.logger import LoggerMixin

class PreventionManager(LoggerMixin):
    """Manages mosquito prevention actions and alerting"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.enabled = config.get('enabled', True)
        self.methods = config.get('methods', ['alert', 'log'])
        self.alert_threshold = config.get('alert_threshold', 3)
        self.cooldown_period = config.get('cooldown_period', 300)  # 5 minutes
        
        # Tracking variables
        self.detection_count = 0
        self.last_alert_time = None
        self.alert_history = []
        self.running = False
        
        self.logger.info(f"Prevention manager initialized with methods: {self.methods}")
        self.logger.info(f"Alert threshold: {self.alert_threshold} detections")
    
    def initialize(self):
        """Initialize the prevention system"""
        try:
            self.logger.info("Initializing prevention system...")
            
            # Validate configuration
            self._validate_config()
            
            # Initialize alert history
            self.alert_history = []
            
            self.logger.info("Prevention system initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize prevention system: {e}")
            raise
    
    def _validate_config(self):
        """Validate prevention configuration"""
        if not isinstance(self.methods, list):
            raise ValueError("Methods must be a list")
        
        valid_methods = ['alert', 'log', 'notification', 'email', 'webhook']
        for method in self.methods:
            if method not in valid_methods:
                self.logger.warning(f"Unknown prevention method: {method}")
    
    def process_detection(self, detection_data: Dict[str, Any]) -> bool:
        """
        Process a new detection and trigger prevention actions if needed
        
        Args:
            detection_data: Detection information
            
        Returns:
            True if prevention action was taken, False otherwise
        """
        try:
            if not self.enabled:
                return False
            
            # Increment detection count
            self.detection_count += 1
            
            # Log detection
            self._log_detection(detection_data)
            
            # Check if alert threshold is reached
            if self._should_trigger_alert():
                return self._trigger_prevention_actions(detection_data)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error processing detection: {e}")
            return False
    
    def _should_trigger_alert(self) -> bool:
        """Check if alert should be triggered based on threshold and cooldown"""
        current_time = datetime.now()
        
        # Check cooldown period
        if (self.last_alert_time and 
            current_time - self.last_alert_time < timedelta(seconds=self.cooldown_period)):
            return False
        
        # Check threshold
        if self.detection_count >= self.alert_threshold:
            return True
        
        return False
    
    def _trigger_prevention_actions(self, detection_data: Dict[str, Any]) -> bool:
        """Trigger all configured prevention actions"""
        try:
            self.logger.warning(f"🚨 ALERT: {self.detection_count} detections reached threshold!")
            
            # Update alert tracking
            self.last_alert_time = datetime.now()
            self.detection_count = 0
            
            # Create alert record
            alert_record = {
                'timestamp': datetime.now().isoformat(),
                'detection_count': self.detection_count,
                'detection_data': detection_data,
                'methods_triggered': self.methods
            }
            
            self.alert_history.append(alert_record)
            
            # Execute prevention methods
            for method in self.methods:
                self._execute_prevention_method(method, detection_data)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error triggering prevention actions: {e}")
            return False
    
    def _execute_prevention_method(self, method: str, detection_data: Dict[str, Any]):
        """Execute a specific prevention method"""
        try:
            if method == 'alert':
                self._send_alert(detection_data)
            elif method == 'log':
                self._log_alert(detection_data)
            elif method == 'notification':
                self._send_notification(detection_data)
            elif method == 'email':
                self._send_email_alert(detection_data)
            elif method == 'webhook':
                self._send_webhook_alert(detection_data)
            else:
                self.logger.warning(f"Unknown prevention method: {method}")
                
        except Exception as e:
            self.logger.error(f"Error executing prevention method {method}: {e}")
    
    def _send_alert(self, detection_data: Dict[str, Any]):
        """Send console alert"""
        print("\n" + "="*60)
        print("🚨 MOSQUITO DETECTION ALERT 🚨")
        print("="*60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Detections: {self.detection_count}")
        print(f"Classes detected: {detection_data.get('classes', [])}")
        print(f"Confidence: {detection_data.get('confidence', 0):.2f}")
        print("="*60)
        print("Take immediate action to prevent mosquito activity!")
        print("="*60 + "\n")
    
    def _log_alert(self, detection_data: Dict[str, Any]):
        """Log alert to system logs"""
        self.logger.warning(
            f"ALERT: {self.detection_count} detections - "
            f"Classes: {detection_data.get('classes', [])} - "
            f"Confidence: {detection_data.get('confidence', 0):.2f}"
        )
    
    def _send_notification(self, detection_data: Dict[str, Any]):
        """Send system notification (placeholder)"""
        self.logger.info("System notification sent")
        # TODO: Implement actual notification system
    
    def _send_email_alert(self, detection_data: Dict[str, Any]):
        """Send email alert (placeholder)"""
        self.logger.info("Email alert sent")
        # TODO: Implement email notification system
    
    def _send_webhook_alert(self, detection_data: Dict[str, Any]):
        """Send webhook alert (placeholder)"""
        self.logger.info("Webhook alert sent")
        # TODO: Implement webhook notification system
    
    def _log_detection(self, detection_data: Dict[str, Any]):
        """Log individual detection"""
        self.logger.info(
            f"Detection: {detection_data.get('classes', [])} - "
            f"Confidence: {detection_data.get('confidence', 0):.2f}"
        )
    
    def reset_detection_count(self):
        """Reset detection counter"""
        self.detection_count = 0
        self.logger.info("Detection counter reset")
    
    def get_alert_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent alert history"""
        return self.alert_history[-limit:] if self.alert_history else []
    
    def get_status(self) -> Dict[str, Any]:
        """Get prevention system status"""
        return {
            'enabled': self.enabled,
            'methods': self.methods,
            'alert_threshold': self.alert_threshold,
            'cooldown_period': self.cooldown_period,
            'current_detection_count': self.detection_count,
            'last_alert_time': self.last_alert_time.isoformat() if self.last_alert_time else None,
            'alert_history_count': len(self.alert_history),
            'running': self.running
        }
    
    def check_health(self) -> Dict[str, Any]:
        """Check prevention system health"""
        return {
            'status': 'healthy' if self.enabled else 'disabled',
            'last_alert': self.last_alert_time.isoformat() if self.last_alert_time else None,
            'detection_count': self.detection_count,
            'alert_history_size': len(self.alert_history)
        }
    
    def shutdown(self):
        """Shutdown prevention system"""
        self.logger.info("Shutting down prevention system...")
        self.running = False
        self.logger.info("Prevention system shutdown complete") 