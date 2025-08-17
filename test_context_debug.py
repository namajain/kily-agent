#!/usr/bin/env python3
"""
Debug test script to see what's happening in context manager
"""
import sys
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.managers.context_manager import ContextManager

def test_context_manager_debug():
    """Test the context manager with debug logging"""
    print("🧪 Testing Context Manager with Debug Logging...")
    
    # Initialize context manager
    context_manager = ContextManager()
    
    # Test getting context for profile2 (Customer Analytics)
    try:
        print("📊 Loading context for profile2...")
        context_data = context_manager.get_context_for_profile('profile2')
        
        print(f"✅ Context data keys: {list(context_data.keys())}")
        print(f"✅ Context data length: {len(context_data)}")
        
        for filename, df in context_data.items():
            print(f"  - {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading context: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_context_manager_debug()
    sys.exit(0 if success else 1)
