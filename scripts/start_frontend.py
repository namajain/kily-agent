#!/usr/bin/env python3
"""
Frontend startup script for MVP
"""
import os
import sys
import subprocess

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Start the Streamlit frontend"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'app.py')
    
    # Start Streamlit
    subprocess.run([
        'streamlit', 'run', frontend_path,
        '--server.port', '8501',
        '--server.address', 'localhost'
    ])

if __name__ == "__main__":
    main() 