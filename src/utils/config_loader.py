"""
Configuration loader for Iron Dome for Mosquitoes
Handles loading and validation of configuration files
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

class ConfigLoader:
    """Configuration loader with validation and defaults"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}
        self._load_defaults()
    
    def _load_defaults(self):
        """Load default configuration values"""
        self.defaults = {
            'system': {
                'name': 'Iron Dome for Mosquitoes',
                'version': '1.0.0',
                'debug': True,
                'log_level': 'INFO'
            },
            'detection': {
                'model_path': 'models/yolov8n.pt',
                'confidence_threshold': 0.3,
                'iou_threshold': 0.5,
                'classes_to_detect': ['mosquito', 'insect', 'fly'],
                'detection_interval': 1.0,
                'max_detections_per_frame': 10
            },
            'camera': {
                'phone_link': {
                    'enabled': True,
                    'capture_folder': 'data/captures',
                    'auto_save': True
                },
                'usb_camera': {
                    'enabled': False,
                    'device_id': 0,
                    'resolution': [1920, 1080],
                    'fps': 30
                },
                'ip_camera': {
                    'enabled': False,
                    'url': '',
                    'username': '',
                    'password': ''
                }
            },
            'prevention': {
                'enabled': True,
                'methods': ['alert', 'log', 'notification'],
                'alert_threshold': 3,
                'cooldown_period': 300
            },
            'monitoring': {
                'enabled': True,
                'log_detections': True,
                'save_images': True,
                'analytics_enabled': True,
                'retention_days': 30
            },
            'database': {
                'type': 'sqlite',
                'path': 'data/iron_dome.db',
                'backup_enabled': True,
                'backup_interval': 86400
            },
            'web_interface': {
                'enabled': True,
                'host': '127.0.0.1',
                'port': 5000,
                'debug': True,
                'auto_reload': True
            },
            'notifications': {
                'email': {
                    'enabled': False,
                    'smtp_server': '',
                    'smtp_port': 587,
                    'username': '',
                    'password': '',
                    'recipients': []
                },
                'push': {
                    'enabled': False,
                    'api_key': ''
                },
                'webhook': {
                    'enabled': False,
                    'url': ''
                }
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/iron_dome.log',
                'max_size': '10MB',
                'backup_count': 5,
                'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}'
            },
            'performance': {
                'max_memory_usage': '2GB',
                'cpu_limit': 80,
                'gpu_enabled': False,
                'batch_size': 1
            },
            'security': {
                'api_key_required': False,
                'api_key': '',
                'rate_limit': 100,
                'cors_enabled': True
            }
        }
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file with validation
        
        Returns:
            Validated configuration dictionary
        """
        try:
            # Check if config file exists
            if not os.path.exists(self.config_path):
                logger.warning(f"Config file not found: {self.config_path}")
                logger.info("Using default configuration")
                return self.defaults.copy()
            
            # Load YAML file
            with open(self.config_path, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
            
            # Merge with defaults
            self.config = self._merge_configs(self.defaults, file_config)
            
            # Validate configuration
            self._validate_config()
            
            logger.info(f"Configuration loaded from: {self.config_path}")
            return self.config
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            logger.info("Using default configuration")
            return self.defaults.copy()
    
    def _merge_configs(self, defaults: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge user configuration with defaults
        
        Args:
            defaults: Default configuration
            user_config: User configuration from file
            
        Returns:
            Merged configuration
        """
        result = defaults.copy()
        
        if user_config is None:
            return result
        
        for key, value in user_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _validate_config(self):
        """Validate the loaded configuration"""
        try:
            # Validate required paths
            self._validate_paths()
            
            # Validate detection settings
            self._validate_detection_settings()
            
            # Validate camera settings
            self._validate_camera_settings()
            
            # Validate performance settings
            self._validate_performance_settings()
            
            logger.info("Configuration validation passed")
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            raise
    
    def _validate_paths(self):
        """Validate that required paths exist or can be created"""
        paths_to_check = [
            self.config['detection']['model_path'],
            self.config['camera']['phone_link']['capture_folder'],
            self.config['database']['path'],
            self.config['logging']['file']
        ]
        
        for path in paths_to_check:
            if path:
                # Create directory if it doesn't exist
                dir_path = Path(path).parent
                if not dir_path.exists():
                    dir_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created directory: {dir_path}")
    
    def _validate_detection_settings(self):
        """Validate detection configuration settings"""
        detection_config = self.config['detection']
        
        # Check confidence threshold
        if not 0.0 <= detection_config['confidence_threshold'] <= 1.0:
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        
        # Check IOU threshold
        if not 0.0 <= detection_config['iou_threshold'] <= 1.0:
            raise ValueError("iou_threshold must be between 0.0 and 1.0")
        
        # Check detection interval
        if detection_config['detection_interval'] <= 0:
            raise ValueError("detection_interval must be positive")
    
    def _validate_camera_settings(self):
        """Validate camera configuration settings"""
        camera_config = self.config['camera']
        
        # Validate USB camera settings
        if camera_config['usb_camera']['enabled']:
            usb_config = camera_config['usb_camera']
            if not isinstance(usb_config['resolution'], list) or len(usb_config['resolution']) != 2:
                raise ValueError("USB camera resolution must be a list of 2 integers")
            if usb_config['fps'] <= 0:
                raise ValueError("USB camera FPS must be positive")
    
    def _validate_performance_settings(self):
        """Validate performance configuration settings"""
        perf_config = self.config['performance']
        
        # Validate CPU limit
        if not 0 <= perf_config['cpu_limit'] <= 100:
            raise ValueError("cpu_limit must be between 0 and 100")
        
        # Validate batch size
        if perf_config['batch_size'] <= 0:
            raise ValueError("batch_size must be positive")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def save(self, file_path: Optional[str] = None):
        """
        Save current configuration to file
        
        Args:
            file_path: Path to save configuration (uses original path if None)
        """
        if file_path is None:
            file_path = self.config_path
        
        try:
            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise
    
    def reload(self) -> Dict[str, Any]:
        """
        Reload configuration from file
        
        Returns:
            Updated configuration
        """
        logger.info("Reloading configuration...")
        return self.load() 