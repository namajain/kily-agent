"""
Logging configuration for Data Service
"""
import os
import logging
import logging.handlers
from datetime import datetime


def setup_service_logging(service_name: str, log_level: str = 'INFO'):
    """
    Set up logging for a service with file and console handlers
    
    Args:
        service_name: Name of the service (e.g., 'data_service', 'backend')
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)  # Set to lowest level to capture all
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (all logs)
    log_file = f'logs/{service_name}.log'
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console handler (WARNING and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Set console level based on environment
    console_level = getattr(logging, log_level.upper(), logging.INFO)
    console_handler.setLevel(console_level)
    
    logger.info(f"Logging configured for {service_name} - File: {log_file}, Console Level: {log_level}")
    
    return logger


def rotate_logs():
    """
    Rotate log files by renaming current logs to .old
    """
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        return
    
    for filename in os.listdir(logs_dir):
        if filename.endswith('.log') and not filename.endswith('.old'):
            old_path = os.path.join(logs_dir, filename)
            new_path = os.path.join(logs_dir, f"{filename}.old")
            
            if os.path.exists(new_path):
                os.remove(new_path)
            
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(f"Rotated {filename} -> {filename}.old")
