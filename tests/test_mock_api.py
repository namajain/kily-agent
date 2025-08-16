#!/usr/bin/env python3
"""
Test cases for Mock API server
"""
import pytest
import requests
import json
from unittest.mock import patch, MagicMock

class TestMockAPI:
    """Test Mock API server endpoints"""
    
    def setup_method(self):
        """Setup test environment"""
        self.mock_api_url = "http://localhost:5002"
    
    def test_mock_api_health(self):
        """Test Mock API health endpoint"""
        try:
            response = requests.get(f"{self.mock_api_url}/health")
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert data['status'] == 'healthy'
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_get_user_profiles(self):
        """Test Mock API get user profiles endpoint"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.mock_api_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            # Validate response structure
            assert 'profiles' in data
            assert isinstance(data['profiles'], list)
            
            # Test that profiles exist for user1
            assert len(data['profiles']) > 0
            
            # Validate profile structure
            for profile in data['profiles']:
                assert 'profile_id' in profile
                assert 'user_id' in profile
                assert 'profile_name' in profile
                assert 'data_sources' in profile
                assert 'is_active' in profile
                assert 'created_at' in profile
                
                # Validate data types
                assert isinstance(profile['profile_id'], str)
                assert isinstance(profile['user_id'], str)
                assert isinstance(profile['profile_name'], str)
                assert isinstance(profile['is_active'], bool)
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_get_user_profiles_invalid_user(self):
        """Test Mock API get user profiles for invalid user"""
        user_id = "invalid_user"
        
        try:
            response = requests.get(f"{self.mock_api_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            # Should return empty list for invalid user
            assert 'profiles' in data
            assert isinstance(data['profiles'], list)
            assert len(data['profiles']) == 0
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_get_specific_profile(self):
        """Test Mock API get specific profile endpoint"""
        profile_id = "profile1"
        
        try:
            response = requests.get(f"{self.mock_api_url}/api/profiles/{profile_id}")
            assert response.status_code == 200
            data = response.json()
            
            # Validate profile structure
            assert 'profile_id' in data
            assert 'user_id' in data
            assert 'profile_name' in data
            assert 'data_sources' in data
            assert 'is_active' in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_get_nonexistent_profile(self):
        """Test Mock API get nonexistent profile"""
        profile_id = "nonexistent_profile"
        
        try:
            response = requests.get(f"{self.mock_api_url}/api/profiles/{profile_id}")
            assert response.status_code == 404
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_data_sources_structure(self):
        """Test that data sources have proper structure"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.mock_api_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            for profile in data['profiles']:
                data_sources = profile.get('data_sources', [])
                
                # Test that data_sources is a list
                assert isinstance(data_sources, list)
                
                # Test each data source structure
                for source in data_sources:
                    assert isinstance(source, dict)
                    assert 'url' in source
                    assert 'filename' in source
                    assert 'description' in source
                    
                    # Validate data types
                    assert isinstance(source['url'], str)
                    assert isinstance(source['filename'], str)
                    assert isinstance(source['description'], str)
                    
                    # Validate URL format
                    assert source['url'].startswith('http')
                    
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_multiple_data_sources(self):
        """Test that profiles can have multiple data sources"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.mock_api_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            # Find profiles with multiple data sources
            profiles_with_multiple_sources = [
                p for p in data['profiles']
                if len(p.get('data_sources', [])) > 1
            ]
            
            # Should have at least one profile with multiple data sources
            assert len(profiles_with_multiple_sources) > 0
            
            # Test each profile with multiple sources
            for profile in profiles_with_multiple_sources:
                data_sources = profile['data_sources']
                assert len(data_sources) > 1
                
                # Test that all data sources have unique filenames
                filenames = [source['filename'] for source in data_sources]
                assert len(filenames) == len(set(filenames)), "Data sources should have unique filenames"
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_user_isolation(self):
        """Test that users can only see their own profiles"""
        users = ["user1", "user2"]
        user_profiles = {}
        
        try:
            for user_id in users:
                response = requests.get(f"{self.mock_api_url}/api/users/{user_id}/profiles")
                assert response.status_code == 200
                data = response.json()
                user_profiles[user_id] = data['profiles']
            
            # Test that users have different profiles
            user1_profile_ids = [p['profile_id'] for p in user_profiles['user1']]
            user2_profile_ids = [p['profile_id'] for p in user_profiles['user2']]
            
            # Profiles should be different for different users
            assert set(user1_profile_ids) != set(user2_profile_ids)
            
            # Each profile should belong to the correct user
            for profile in user_profiles['user1']:
                assert profile['user_id'] == 'user1'
            
            for profile in user_profiles['user2']:
                assert profile['user_id'] == 'user2'
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_response_headers(self):
        """Test that Mock API returns proper headers"""
        try:
            response = requests.get(f"{self.mock_api_url}/health")
            assert response.status_code == 200
            
            # Check for CORS headers
            assert 'Access-Control-Allow-Origin' in response.headers
            assert response.headers['Access-Control-Allow-Origin'] == '*'
            
            # Check content type
            assert 'Content-Type' in response.headers
            assert 'application/json' in response.headers['Content-Type']
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")
    
    def test_mock_api_error_handling(self):
        """Test Mock API error handling"""
        try:
            # Test invalid endpoint
            response = requests.get(f"{self.mock_api_url}/invalid/endpoint")
            assert response.status_code == 404
            
            # Test invalid user ID format
            response = requests.get(f"{self.mock_api_url}/api/users//profiles")
            assert response.status_code == 404
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Mock API server not running")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
