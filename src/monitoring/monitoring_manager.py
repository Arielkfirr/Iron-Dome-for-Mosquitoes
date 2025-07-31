"""
Monitoring Manager for Iron Dome for Mosquitoes
Handles system health monitoring, analytics, and performance tracking
"""

import time
import threading
import psutil
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
from utils.logger import LoggerMixin

class MonitoringManager(LoggerMixin):
    """Manages system monitoring, health checks, and analytics"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.enabled = config.get('enabled', True)
        self.log_detections = config.get('log_detections', True)
        self.save_images = config.get('save_images', True)
        self.analytics_enabled = config.get('analytics_enabled', True)
        self.retention_days = config.get('retention_days', 30)
        
        # Monitoring data
        self.system_stats = {}
        self.detection_history = []
        self.performance_metrics = {}
        self.health_status = 'unknown'
        
        # Threading
        self.monitoring_thread = None
        self.running = False
        
        self.logger.info("Monitoring manager initialized")
    
    def initialize(self):
        """Initialize the monitoring system"""
        try:
            self.logger.info("Initializing monitoring system...")
            
            # Create monitoring directories
            self._create_monitoring_dirs()
            
            # Initialize system stats
            self._initialize_system_stats()
            
            # Start monitoring thread
            self._start_monitoring_thread()
            
            self.logger.info("Monitoring system initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize monitoring system: {e}")
            raise
    
    def _create_monitoring_dirs(self):
        """Create necessary monitoring directories"""
        dirs = ['logs', 'data/analytics', 'data/monitoring']
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def _initialize_system_stats(self):
        """Initialize system statistics tracking"""
        self.system_stats = {
            'start_time': datetime.now(),
            'uptime': 0,
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0,
            'detection_count': 0,
            'error_count': 0,
            'last_detection': None,
            'system_health': 'healthy'
        }
    
    def _start_monitoring_thread(self):
        """Start the monitoring thread"""
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.monitoring_thread = threading.Thread(target=self._monitoring_worker, daemon=True)
            self.monitoring_thread.start()
            self.logger.info("Monitoring thread started")
    
    def _monitoring_worker(self):
        """Background monitoring worker"""
        self.running = True
        
        while self.running:
            try:
                # Update system stats
                self._update_system_stats()
                
                # Check system health
                self._check_system_health()
                
                # Clean old data
                self._cleanup_old_data()
                
                # Sleep for monitoring interval
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in monitoring worker: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _update_system_stats(self):
        """Update system statistics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Update stats
            self.system_stats.update({
                'cpu_usage': cpu_percent,
                'memory_usage': memory_percent,
                'disk_usage': disk_percent,
                'uptime': (datetime.now() - self.system_stats['start_time']).total_seconds()
            })
            
        except Exception as e:
            self.logger.error(f"Error updating system stats: {e}")
    
    def _check_system_health(self):
        """Check overall system health"""
        try:
            health_issues = []
            
            # Check CPU usage
            if self.system_stats['cpu_usage'] > 80:
                health_issues.append("High CPU usage")
            
            # Check memory usage
            if self.system_stats['memory_usage'] > 85:
                health_issues.append("High memory usage")
            
            # Check disk usage
            if self.system_stats['disk_usage'] > 90:
                health_issues.append("High disk usage")
            
            # Update health status
            if health_issues:
                self.health_status = 'warning'
                self.logger.warning(f"System health issues: {', '.join(health_issues)}")
            else:
                self.health_status = 'healthy'
            
            self.system_stats['system_health'] = self.health_status
            
        except Exception as e:
            self.logger.error(f"Error checking system health: {e}")
            self.health_status = 'error'
    
    def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            
            # Clean old detection history
            self.detection_history = [
                detection for detection in self.detection_history
                if datetime.fromisoformat(detection['timestamp']) > cutoff_date
            ]
            
            # Clean old performance metrics
            old_keys = []
            for key in self.performance_metrics:
                if datetime.fromisoformat(key) < cutoff_date:
                    old_keys.append(key)
            
            for key in old_keys:
                del self.performance_metrics[key]
            
            if old_keys:
                self.logger.info(f"Cleaned up {len(old_keys)} old performance metrics")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old data: {e}")
    
    def log_detection(self, detection_data: Dict[str, Any]):
        """Log a new detection"""
        try:
            if not self.log_detections:
                return
            
            # Create detection record
            detection_record = {
                'timestamp': datetime.now().isoformat(),
                'classes': detection_data.get('classes', []),
                'confidence': detection_data.get('confidence', 0),
                'image_path': detection_data.get('image_path', ''),
                'processing_time': detection_data.get('processing_time', 0)
            }
            
            # Add to history
            self.detection_history.append(detection_record)
            
            # Update stats
            self.system_stats['detection_count'] += 1
            self.system_stats['last_detection'] = datetime.now()
            
            # Log to file
            self.logger.info(
                f"Detection logged: {detection_record['classes']} "
                f"(confidence: {detection_record['confidence']:.2f})"
            )
            
        except Exception as e:
            self.logger.error(f"Error logging detection: {e}")
    
    def log_error(self, error_data: Dict[str, Any]):
        """Log a system error"""
        try:
            # Update error count
            self.system_stats['error_count'] += 1
            
            # Log error
            self.logger.error(
                f"System error: {error_data.get('message', 'Unknown error')} "
                f"in {error_data.get('component', 'unknown')}"
            )
            
        except Exception as e:
            self.logger.error(f"Error logging error: {e}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system statistics"""
        return self.system_stats.copy()
    
    def get_detection_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent detection history"""
        return self.detection_history[-limit:] if self.detection_history else []
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            'system_stats': self.system_stats,
            'health_status': self.health_status,
            'detection_count': len(self.detection_history),
            'error_count': self.system_stats['error_count'],
            'uptime_hours': self.system_stats['uptime'] / 3600
        }
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary"""
        try:
            if not self.detection_history:
                return {'message': 'No detection data available'}
            
            # Calculate analytics
            total_detections = len(self.detection_history)
            unique_classes = set()
            total_confidence = 0
            
            for detection in self.detection_history:
                unique_classes.update(detection.get('classes', []))
                total_confidence += detection.get('confidence', 0)
            
            avg_confidence = total_confidence / total_detections if total_detections > 0 else 0
            
            # Get time-based stats
            recent_detections = [
                d for d in self.detection_history
                if datetime.fromisoformat(d['timestamp']) > datetime.now() - timedelta(hours=24)
            ]
            
            return {
                'total_detections': total_detections,
                'recent_detections_24h': len(recent_detections),
                'unique_classes_detected': list(unique_classes),
                'average_confidence': round(avg_confidence, 3),
                'detection_rate_per_hour': len(recent_detections) / 24,
                'system_uptime_hours': round(self.system_stats['uptime'] / 3600, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating analytics summary: {e}")
            return {'error': str(e)}
    
    def check_health(self) -> Dict[str, Any]:
        """Check monitoring system health"""
        return {
            'status': self.health_status,
            'monitoring_enabled': self.enabled,
            'thread_running': self.running,
            'last_update': datetime.now().isoformat(),
            'system_stats': self.system_stats
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get monitoring system status"""
        return {
            'enabled': self.enabled,
            'log_detections': self.log_detections,
            'save_images': self.save_images,
            'analytics_enabled': self.analytics_enabled,
            'retention_days': self.retention_days,
            'running': self.running,
            'health_status': self.health_status,
            'detection_count': self.system_stats['detection_count'],
            'error_count': self.system_stats['error_count']
        }
    
    def shutdown(self):
        """Shutdown monitoring system"""
        self.logger.info("Shutting down monitoring system...")
        self.running = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
        
        self.logger.info("Monitoring system shutdown complete") 