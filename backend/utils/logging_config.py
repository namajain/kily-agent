"""
Centralized logging configuration for all services
"""
import os
import logging
import logging.handlers
from datetime import datetime


def setup_service_logging(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Setup logging for a service with file and console handlers
    
    Args:
        service_name: Name of the service (backend, data_service, frontend)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler - logs to service-specific file
    log_file = os.path.join(logs_dir, f'{service_name}.log')
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler - logs to console (only WARNING and above for less verbosity)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log startup message
    logger.info(f"Logging initialized for {service_name} service")
    logger.info(f"Log file: {log_file}")
    
    return logger


def rotate_logs():
    """
    Rotate log files by moving current logs to .old and creating new ones
    """
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    
    if not os.path.exists(logs_dir):
        return
    
    # Services to rotate logs for
    services = ['backend', 'data_service', 'frontend']
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for service in services:
        current_log = os.path.join(logs_dir, f'{service}.log')
        old_log = os.path.join(logs_dir, f'{service}.log.old')
        timestamped_log = os.path.join(logs_dir, f'{service}_{timestamp}.log.old')
        
        if os.path.exists(current_log):
            # If there's already an .old file, rename it with timestamp
            if os.path.exists(old_log):
                os.rename(old_log, timestamped_log)
            
            # Move current log to .old
            os.rename(current_log, old_log)
            print(f"Rotated {service} log: {current_log} -> {old_log}")


def get_log_file_path(service_name: str) -> str:
    """
    Get the log file path for a service
    
    Args:
        service_name: Name of the service
        
    Returns:
        Full path to the log file
    """
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    return os.path.join(logs_dir, f'{service_name}.log')
