#!/usr/bin/env python3
"""
Test cases for frontend integration with REST API
"""
import pytest
import requests
import json
from unittest.mock import patch, MagicMock
import streamlit as st

class TestFrontendIntegration:
    """Test frontend integration with REST API"""
    
    def setup_method(self):
        """Setup test environment"""
        self.backend_url = "http://localhost:5001"
        self.mock_api_url = "http://localhost:5002"
    
    def test_frontend_profile_loading(self):
        """Test that frontend can load profiles via REST API"""
        user_id = "user1"
        
        try:
            # Test backend API directly
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            # Validate that profiles are returned
            assert 'profiles' in data
            assert isinstance(data['profiles'], list)
            assert len(data['profiles']) > 0
            
            # Test that profiles have required fields for frontend display
            for profile in data['profiles']:
                assert 'profile_id' in profile
                assert 'profile_name' in profile
                assert 'data_sources' in profile
                assert 'is_active' in profile
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_profile_data_structure_for_frontend(self):
        """Test that profile data structure is compatible with frontend"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            for profile in data['profiles']:
                # Test data_sources parsing logic
                profile_data = profile.get('data_sources', [])
                
                # Test string parsing (frontend handles both string and list)
                if isinstance(profile_data, str):
                    try:
                        parsed_data = json.loads(profile_data)
                        assert isinstance(parsed_data, list)
                    except json.JSONDecodeError:
                        pytest.fail("Invalid JSON in data_sources")
                
                # Test list format
                elif isinstance(profile_data, list):
                    for source in profile_data:
                        assert isinstance(source, dict)
                        assert 'url' in source
                        assert 'filename' in source
                        assert 'description' in source
                
                # Test data sources count calculation
                if isinstance(profile_data, str):
                    try:
                        parsed_data = json.loads(profile_data)
                        count = len(parsed_data)
                    except:
                        count = 0
                else:
                    count = len(profile_data)
                
                assert count >= 0  # Should be non-negative
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_multiple_users_profiles(self):
        """Test that different users have different profiles"""
        users = ["user1", "user2"]
        user_profiles = {}
        
        try:
            for user_id in users:
                response = requests.get(f"{self.backend_url}/api/users/{user_id}/profiles")
                assert response.status_code == 200
                data = response.json()
                user_profiles[user_id] = data['profiles']
            
            # Test that users have different profiles
            user1_profiles = [p['profile_id'] for p in user_profiles['user1']]
            user2_profiles = [p['profile_id'] for p in user_profiles['user2']]
            
            # Profiles should be different for different users
            assert set(user1_profiles) != set(user2_profiles)
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_data_sources_content(self):
        """Test that data sources contain meaningful content"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            for profile in data['profiles']:
                profile_data = profile.get('data_sources', [])
                
                if isinstance(profile_data, str):
                    try:
                        profile_data = json.loads(profile_data)
                    except:
                        profile_data = []
                
                # Test that data sources have content
                for source in profile_data:
                    assert source.get('url'), "Data source should have URL"
                    assert source.get('filename'), "Data source should have filename"
                    assert source.get('description'), "Data source should have description"
                    
                    # Test URL format
                    url = source.get('url', '')
                    assert url.startswith('http'), "URL should be valid HTTP URL"
                    
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_profile_activation_status(self):
        """Test that profiles have proper activation status"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            for profile in data['profiles']:
                # Test that is_active is boolean
                assert isinstance(profile.get('is_active'), bool)
                
                # Test that active profiles have data sources
                if profile.get('is_active'):
                    profile_data = profile.get('data_sources', [])
                    if isinstance(profile_data, str):
                        try:
                            profile_data = json.loads(profile_data)
                        except:
                            profile_data = []
                    
                    # Active profiles should have at least one data source
                    assert len(profile_data) > 0, "Active profiles should have data sources"
                    
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    @patch('requests.get')
    def test_frontend_error_handling(self, mock_get):
        """Test frontend error handling for API failures"""
        # Mock API failure
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        # This would test the frontend's error handling
        # In a real test, we'd need to mock the frontend's requests calls
        assert True  # Placeholder for actual frontend error handling test
    
    def test_api_response_time(self):
        """Test that API responses are reasonably fast"""
        import time
        user_id = "user1"
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/profiles")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            assert response.status_code == 200
            assert response_time < 5.0, f"API response too slow: {response_time:.2f}s"
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
