#!/usr/bin/env python3
"""
Frontend startup script with logging to file
"""
import os
import sys
import subprocess
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.utils.logging_config import setup_service_logging, get_log_file_path

def start_frontend():
    """Start the React frontend and redirect output to log file"""
    try:
        # Setup logging
        logger = setup_service_logging('frontend', log_level=os.getenv('LOG_LEVEL', 'INFO'))
        
        # Get paths
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        frontend_dir = os.path.join(project_root, 'frontend-react')
        log_file = get_log_file_path('frontend')
        
        logger.info("Starting React frontend server...")
        logger.info(f"Frontend directory: {frontend_dir}")
        logger.info(f"Log file: {log_file}")
        
        # Check if frontend directory exists
        if not os.path.exists(frontend_dir):
            logger.error(f"Frontend directory not found: {frontend_dir}")
            sys.exit(1)
        
        # Check if node_modules exists
        node_modules = os.path.join(frontend_dir, 'node_modules')
        if not os.path.exists(node_modules):
            logger.error("Node modules not found. Run 'npm install' in frontend-react directory")
            sys.exit(1)
        
        # Start the React development server
        env = os.environ.copy()
        env['BROWSER'] = 'none'  # Don't auto-open browser
        
        process = subprocess.Popen(
            ['npm', 'start'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            env=env
        )
        
        logger.info(f"Frontend process started with PID: {process.pid}")
        
        # Stream output to both console and log file
        with open(log_file, 'a') as log_file_handle:
            for line in iter(process.stdout.readline, ''):
                if line:
                    line_content = line.strip()
                    
                    # Skip verbose deprecation warnings and routine messages
                    skip_patterns = [
                        "DeprecationWarning:",
                        "Use `node --trace-deprecation",
                        "_extend` API is deprecated",
                        "onAfterSetupMiddleware",
                        "onBeforeSetupMiddleware"
                    ]
                    
                    should_skip = any(pattern in line_content for pattern in skip_patterns)
                    
                    # Write to log file with timestamp (keep all logs in file)
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    log_line = f"{timestamp} - FRONTEND - INFO - {line_content}\n"
                    log_file_handle.write(log_line)
                    log_file_handle.flush()
                    
                    # Only print important messages to console
                    if not should_skip and line_content:
                        important_patterns = [
                            "Starting the development server",
                            "Compiled successfully",
                            "You can now view",
                            "Local:",
                            "webpack compiled",
                            "ERROR",
                            "WARN"
                        ]
                        if any(pattern in line_content for pattern in important_patterns):
                            print(f"FRONTEND: {line_content}")
        
        # Wait for process to complete
        process.wait()
        
    except KeyboardInterrupt:
        logger.info("Frontend server stopped by user")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        logger.error(f"Failed to start frontend server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_frontend()
