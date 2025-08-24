#!/usr/bin/env python3
"""
Demo script to test the logging system
"""
import os
import sys
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.utils.logging_config import setup_service_logging

def demo_logging():
    """Demonstrate logging functionality"""
    print("=== Logging System Demo ===")
    
    # Test backend logging
    backend_logger = setup_service_logging('backend', log_level='INFO')
    backend_logger.info("Backend service started")
    backend_logger.warning("This is a warning message")
    backend_logger.error("This is an error message")
    
    # Test data service logging
    data_logger = setup_service_logging('data_service', log_level='INFO')
    data_logger.info("Data service initialized")
    data_logger.debug("Debug message (should not appear in console)")
    
    # Test frontend logging
    frontend_logger = setup_service_logging('frontend', log_level='INFO')
    frontend_logger.info("Frontend service ready")
    
    print("\n=== Demo Complete ===")
    print("Check the logs/ directory for log files:")
    print("  - logs/backend.log")
    print("  - logs/data_service.log") 
    print("  - logs/frontend.log")
    print("\nUse 'make show-logs' to view recent logs")

if __name__ == "__main__":
    demo_logging()
