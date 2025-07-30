"""
Logging utilities for Iron Dome for Mosquitoes
Provides centralized logging configuration and utilities
"""

import sys
import os
from pathlib import Path
from loguru import logger
from typing import Optional

def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: str = "10MB",
    backup_count: int = 5,
    format_string: Optional[str] = None
) -> logger:
    """
    Setup and configure the logger for the Iron Dome for Mosquitoes system
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file (optional)
        max_size: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        format_string: Custom format string for logs
    
    Returns:
        Configured logger instance
    """
    
    # Remove default handler
    logger.remove()
    
    # Default format if not provided
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=format_string,
        level=level,
        colorize=True
    )
    
    # Add file handler if log_file is specified
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_file,
            format=format_string,
            level=level,
            rotation=max_size,
            retention=backup_count,
            compression="zip"
        )
    
    return logger

def get_logger(name: str = None) -> logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (optional)
    
    Returns:
        Logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger

class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = get_logger(self.__class__.__name__)
    
    @property
    def logger(self):
        """Get the logger instance for this class"""
        return self._logger

def log_function_call(func):
    """Decorator to log function calls with parameters and return values"""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Log function call
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {e}")
            raise
    
    return wrapper

def log_execution_time(func):
    """Decorator to log function execution time"""
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    
    return wrapper

class LogContext:
    """Context manager for logging specific operations"""
    
    def __init__(self, operation_name: str, logger_instance: logger = None):
        self.operation_name = operation_name
        self.logger = logger_instance or get_logger()
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        
        if exc_type is None:
            self.logger.info(f"Completed operation: {self.operation_name} in {execution_time:.4f} seconds")
        else:
            self.logger.error(f"Failed operation: {self.operation_name} after {execution_time:.4f} seconds: {exc_val}")
        
        return False  # Don't suppress exceptions

# Import time for LogContext
import time 