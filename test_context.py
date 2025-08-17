#!/usr/bin/env python3
"""
Test script to verify context manager functionality
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import with absolute path
from backend.managers.context_manager import ContextManager

def test_context_manager():
    """Test the context manager with sample data"""
    print("🧪 Testing Context Manager...")
    
    # Initialize context manager
    context_manager = ContextManager()
    
    # Test getting context for profile2 (Customer Analytics)
    try:
        print("📊 Loading context for profile2...")
        context_data = context_manager.get_context_for_profile('profile2')
        
        print(f"✅ Successfully loaded {len(context_data)} data files:")
        for filename, df in context_data.items():
            print(f"  - {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
            print(f"    Columns: {list(df.columns)}")
            print(f"    Sample data:")
            print(df.head(3).to_string())
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading context: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_context_manager()
    sys.exit(0 if success else 1)
