"""
Database Manager for Iron Dome for Mosquitoes
Handles data persistence, storage, and database operations
"""

import sqlite3
import json
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
from utils.logger import LoggerMixin

class DatabaseManager(LoggerMixin):
    """Manages database operations and data persistence"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.db_type = config.get('type', 'sqlite')
        self.db_path = config.get('path', 'data/iron_dome.db')
        self.backup_enabled = config.get('backup_enabled', True)
        self.backup_interval = config.get('backup_interval', 86400)  # 24 hours
        
        # Database connection
        self.connection = None
        self.lock = threading.Lock()
        
        # Backup tracking
        self.last_backup = None
        
        self.logger.info(f"Database manager initialized for {self.db_type}: {self.db_path}")
    
    def initialize(self):
        """Initialize the database system"""
        try:
            self.logger.info("Initializing database system...")
            
            # Create database directory
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Initialize database
            self._create_database()
            
            # Create tables
            self._create_tables()
            
            # Initialize backup system
            if self.backup_enabled:
                self._initialize_backup_system()
            
            self.logger.info("Database system initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database system: {e}")
            raise
    
    def _create_database(self):
        """Create database connection"""
        try:
            if self.db_type == 'sqlite':
                self.connection = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False,
                    timeout=30
                )
                self.connection.row_factory = sqlite3.Row
                self.logger.info(f"SQLite database connected: {self.db_path}")
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to create database connection: {e}")
            raise
    
    def _create_tables(self):
        """Create database tables"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                # Detections table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS detections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        classes TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        image_path TEXT,
                        processing_time REAL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # System events table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        message TEXT,
                        severity TEXT DEFAULT 'info',
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Performance metrics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        cpu_usage REAL,
                        memory_usage REAL,
                        disk_usage REAL,
                        detection_count INTEGER,
                        error_count INTEGER,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Alerts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        alert_type TEXT NOT NULL,
                        message TEXT,
                        detection_count INTEGER,
                        severity TEXT DEFAULT 'warning',
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_detections_timestamp ON detections(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON system_events(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON performance_metrics(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)')
                
                self.connection.commit()
                self.logger.info("Database tables created successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to create database tables: {e}")
            raise
    
    def _initialize_backup_system(self):
        """Initialize database backup system"""
        try:
            # Create backup directory
            backup_dir = Path('data/backups')
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            self.logger.info("Database backup system initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize backup system: {e}")
    
    def log_detection(self, detection_data: Dict[str, Any]) -> bool:
        """Log a detection to the database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cursor.execute('''
                    INSERT INTO detections (timestamp, classes, confidence, image_path, processing_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    detection_data.get('timestamp', datetime.now().isoformat()),
                    json.dumps(detection_data.get('classes', [])),
                    detection_data.get('confidence', 0.0),
                    detection_data.get('image_path', ''),
                    detection_data.get('processing_time', 0.0)
                ))
                
                self.connection.commit()
                self.logger.info("Detection logged to database")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to log detection: {e}")
            return False
    
    def log_event(self, event_type: str, message: str, severity: str = 'info') -> bool:
        """Log a system event to the database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cursor.execute('''
                    INSERT INTO system_events (timestamp, event_type, message, severity)
                    VALUES (?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    event_type,
                    message,
                    severity
                ))
                
                self.connection.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to log event: {e}")
            return False
    
    def log_performance_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Log performance metrics to the database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cursor.execute('''
                    INSERT INTO performance_metrics (timestamp, cpu_usage, memory_usage, disk_usage, detection_count, error_count)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    metrics.get('cpu_usage', 0.0),
                    metrics.get('memory_usage', 0.0),
                    metrics.get('disk_usage', 0.0),
                    metrics.get('detection_count', 0),
                    metrics.get('error_count', 0)
                ))
                
                self.connection.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to log performance metrics: {e}")
            return False
    
    def log_alert(self, alert_type: str, message: str, detection_count: int = 0, severity: str = 'warning') -> bool:
        """Log an alert to the database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cursor.execute('''
                    INSERT INTO alerts (timestamp, alert_type, message, detection_count, severity)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    alert_type,
                    message,
                    detection_count,
                    severity
                ))
                
                self.connection.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to log alert: {e}")
            return False
    
    def get_detections(self, limit: int = 100, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent detections from database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                cursor.execute('''
                    SELECT * FROM detections 
                    WHERE timestamp > ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (cutoff_date.isoformat(), limit))
                
                rows = cursor.fetchall()
                detections = []
                
                for row in rows:
                    detection = dict(row)
                    detection['classes'] = json.loads(detection['classes'])
                    detections.append(detection)
                
                return detections
                
        except Exception as e:
            self.logger.error(f"Failed to get detections: {e}")
            return []
    
    def get_events(self, limit: int = 100, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent system events from database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                cursor.execute('''
                    SELECT * FROM system_events 
                    WHERE timestamp > ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (cutoff_date.isoformat(), limit))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Failed to get events: {e}")
            return []
    
    def get_performance_metrics(self, limit: int = 100, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent performance metrics from database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                cursor.execute('''
                    SELECT * FROM performance_metrics 
                    WHERE timestamp > ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (cutoff_date.isoformat(), limit))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Failed to get performance metrics: {e}")
            return []
    
    def get_alerts(self, limit: int = 100, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent alerts from database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                cursor.execute('''
                    SELECT * FROM alerts 
                    WHERE timestamp > ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (cutoff_date.isoformat(), limit))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Failed to get alerts: {e}")
            return []
    
    def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics summary from database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                # Total detections
                cursor.execute('''
                    SELECT COUNT(*) as count FROM detections WHERE timestamp > ?
                ''', (cutoff_date.isoformat(),))
                total_detections = cursor.fetchone()['count']
                
                # Average confidence
                cursor.execute('''
                    SELECT AVG(confidence) as avg_confidence FROM detections WHERE timestamp > ?
                ''', (cutoff_date.isoformat(),))
                avg_confidence = cursor.fetchone()['avg_confidence'] or 0
                
                # Unique classes
                cursor.execute('''
                    SELECT DISTINCT classes FROM detections WHERE timestamp > ?
                ''', (cutoff_date.isoformat(),))
                classes_rows = cursor.fetchall()
                unique_classes = set()
                for row in classes_rows:
                    classes = json.loads(row['classes'])
                    unique_classes.update(classes)
                
                # Recent detections (last 24 hours)
                recent_cutoff = datetime.now() - timedelta(hours=24)
                cursor.execute('''
                    SELECT COUNT(*) as count FROM detections WHERE timestamp > ?
                ''', (recent_cutoff.isoformat(),))
                recent_detections = cursor.fetchone()['count']
                
                return {
                    'total_detections': total_detections,
                    'recent_detections_24h': recent_detections,
                    'unique_classes_detected': list(unique_classes),
                    'average_confidence': round(avg_confidence, 3),
                    'detection_rate_per_hour': recent_detections / 24 if recent_detections > 0 else 0
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get analytics summary: {e}")
            return {'error': str(e)}
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """Clean up old data from database"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                # Count records to be deleted
                cursor.execute('SELECT COUNT(*) as count FROM detections WHERE timestamp < ?', (cutoff_date.isoformat(),))
                detections_to_delete = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM system_events WHERE timestamp < ?', (cutoff_date.isoformat(),))
                events_to_delete = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM performance_metrics WHERE timestamp < ?', (cutoff_date.isoformat(),))
                metrics_to_delete = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM alerts WHERE timestamp < ?', (cutoff_date.isoformat(),))
                alerts_to_delete = cursor.fetchone()['count']
                
                # Delete old records
                cursor.execute('DELETE FROM detections WHERE timestamp < ?', (cutoff_date.isoformat(),))
                cursor.execute('DELETE FROM system_events WHERE timestamp < ?', (cutoff_date.isoformat(),))
                cursor.execute('DELETE FROM performance_metrics WHERE timestamp < ?', (cutoff_date.isoformat(),))
                cursor.execute('DELETE FROM alerts WHERE timestamp < ?', (cutoff_date.isoformat(),))
                
                self.connection.commit()
                
                total_deleted = detections_to_delete + events_to_delete + metrics_to_delete + alerts_to_delete
                self.logger.info(f"Cleaned up {total_deleted} old records from database")
                
                return total_deleted
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup old data: {e}")
            return 0
    
    def backup_database(self) -> bool:
        """Create a backup of the database"""
        try:
            if not self.backup_enabled:
                return True
            
            backup_path = Path(f"data/backups/iron_dome_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
            
            with self.lock:
                # Create backup
                backup_connection = sqlite3.connect(backup_path)
                self.connection.backup(backup_connection)
                backup_connection.close()
            
            self.last_backup = datetime.now()
            self.logger.info(f"Database backup created: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to backup database: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get database status"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                # Get table sizes
                cursor.execute('SELECT COUNT(*) as count FROM detections')
                detections_count = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM system_events')
                events_count = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM performance_metrics')
                metrics_count = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM alerts')
                alerts_count = cursor.fetchone()['count']
                
                return {
                    'type': self.db_type,
                    'path': self.db_path,
                    'backup_enabled': self.backup_enabled,
                    'last_backup': self.last_backup.isoformat() if self.last_backup else None,
                    'table_sizes': {
                        'detections': detections_count,
                        'events': events_count,
                        'metrics': metrics_count,
                        'alerts': alerts_count
                    }
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get database status: {e}")
            return {'error': str(e)}
    
    def check_health(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute('SELECT 1')
                cursor.fetchone()
                
                return {
                    'status': 'healthy',
                    'connection': 'active',
                    'last_check': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'connection': 'failed',
                'error': str(e),
                'last_check': datetime.now().isoformat()
            }
    
    def shutdown(self):
        """Shutdown database system"""
        self.logger.info("Shutting down database system...")
        
        try:
            if self.connection:
                self.connection.close()
                self.logger.info("Database connection closed")
        except Exception as e:
            self.logger.error(f"Error closing database connection: {e}")
        
        self.logger.info("Database system shutdown complete") 