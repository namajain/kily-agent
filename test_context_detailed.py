#!/usr/bin/env python3
"""
Detailed test script to debug context manager issues
"""
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.api_client import api_client

def test_api_client():
    """Test the API client to see if it can fetch profile data"""
    print("🧪 Testing API Client...")
    
    try:
        # Test getting profile2
        print("📊 Fetching profile2 from API...")
        profile = api_client.get_profile('profile2')
        
        if profile:
            print(f"✅ Profile found: {profile['profile_name']}")
            print(f"   Profile ID: {profile['profile_id']}")
            print(f"   User ID: {profile['user_id']}")
            print(f"   Is Active: {profile['is_active']}")
            
            # Parse data sources
            data_sources = profile.get('data_sources', [])
            if isinstance(data_sources, str):
                data_sources = json.loads(data_sources)
            
            print(f"   Data Sources: {len(data_sources)}")
            for i, source in enumerate(data_sources):
                print(f"     {i+1}. {source['filename']} - {source['description']}")
                print(f"        URL: {source['url']}")
            
            return True
        else:
            print("❌ Profile not found")
            return False
            
    except Exception as e:
        print(f"❌ Error fetching profile: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_paths():
    """Test if the sample data files exist"""
    print("\n🧪 Testing File Paths...")
    
    sample_files = [
        'sample_data/customers.csv',
        'sample_data/purchases.csv', 
        'sample_data/feedback.csv',
        'sample_data/support.csv'
    ]
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} exists ({size} bytes)")
        else:
            print(f"❌ {file_path} does not exist")
    
    return True

if __name__ == "__main__":
    print("🔍 Detailed Context Manager Debug Test")
    print("=" * 50)
    
    success1 = test_api_client()
    success2 = test_file_paths()
    
    if success1 and success2:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    sys.exit(0 if (success1 and success2) else 1)
