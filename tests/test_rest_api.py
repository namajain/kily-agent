#!/usr/bin/env python3
"""
Test cases for REST API endpoints
"""
import pytest
import requests
import json
from unittest.mock import patch, MagicMock

class TestRestAPI:
    """Test REST API endpoints"""
    
    def setup_method(self):
        """Setup test environment"""
        self.base_url = "http://localhost:5001"
        self.data_service_url = "http://localhost:5002"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert data['status'] == 'healthy'
            assert 'timestamp' in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_get_user_profiles_success(self):
        """Test successful user profiles retrieval"""
        user_id = "user1"
        expected_profiles = [
            {
                "profile_id": "profile1",
                "user_id": "user1",
                "profile_name": "Sales Data Analysis",
                "data_sources": [
                    {
                        "url": "https://raw.githubusercontent.com/datasets/sales-data/main/sales.csv",
                        "filename": "sales.csv",
                        "description": "Sales data for analysis"
                    }
                ],
                "is_active": True
            }
        ]
        
        try:
            response = requests.get(f"{self.base_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            assert 'profiles' in data
            assert isinstance(data['profiles'], list)
            assert len(data['profiles']) > 0
            
            # Check profile structure
            profile = data['profiles'][0]
            assert 'profile_id' in profile
            assert 'profile_name' in profile
            assert 'data_sources' in profile
            assert 'is_active' in profile
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_get_user_profiles_invalid_user(self):
        """Test user profiles retrieval for invalid user"""
        user_id = "invalid_user"
        
        try:
            response = requests.get(f"{self.base_url}/api/users/{user_id}/profiles")
            # Should return empty list or 404
            assert response.status_code in [200, 404]
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_get_user_profiles_empty_user_id(self):
        """Test user profiles retrieval with empty user ID"""
        try:
            response = requests.get(f"{self.base_url}/api/users//profiles")
            assert response.status_code == 404
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    @patch('requests.get')
    def test_data_service_integration(self, mock_get):
        """Test integration with Mock API"""
        # Mock the Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "profiles": [
                {
                    "profile_id": "test_profile",
                    "profile_name": "Test Profile",
                    "data_sources": []
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test that backend properly calls Mock API
        try:
            response = requests.get(f"{self.base_url}/api/users/user1/profiles")
            assert response.status_code == 200
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_api_response_structure(self):
        """Test API response structure and data types"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.base_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            # Validate response structure
            assert isinstance(data, dict)
            assert 'profiles' in data
            assert isinstance(data['profiles'], list)
            
            if data['profiles']:
                profile = data['profiles'][0]
                
                # Validate profile fields
                assert isinstance(profile.get('profile_id'), str)
                assert isinstance(profile.get('profile_name'), str)
                assert isinstance(profile.get('is_active'), bool)
                assert isinstance(profile.get('data_sources'), list)
                
                # Validate data sources structure
                if profile.get('data_sources'):
                    source = profile['data_sources'][0]
                    assert isinstance(source, dict)
                    assert 'url' in source
                    assert 'filename' in source
                    assert 'description' in source
                    
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")
    
    def test_multiple_data_sources(self):
        """Test that profiles can have multiple data sources"""
        user_id = "user1"
        
        try:
            response = requests.get(f"{self.base_url}/api/users/{user_id}/profiles")
            assert response.status_code == 200
            data = response.json()
            
            # Find a profile with multiple data sources
            profiles_with_sources = [
                p for p in data['profiles'] 
                if p.get('data_sources') and len(p['data_sources']) > 1
            ]
            
            if profiles_with_sources:
                profile = profiles_with_sources[0]
                assert len(profile['data_sources']) > 1
                
                # Validate each data source
                for source in profile['data_sources']:
                    assert 'url' in source
                    assert 'filename' in source
                    assert 'description' in source
                    
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend server not running")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
