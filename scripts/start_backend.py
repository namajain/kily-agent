#!/usr/bin/env python3
"""
Backend startup script for MVP
"""
import os
import sys
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.server import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main() 