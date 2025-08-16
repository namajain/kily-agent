#!/usr/bin/env python3
"""
Unit tests for database functionality
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import get_db_connection
from backend.managers.context_manager import ContextManager

class TestDatabaseConnection(unittest.TestCase):
    """Test database connection and basic operations"""
    
    def setUp(self):
        """Set up test environment"""
        self.db = get_db_connection()
        
    def test_database_connection(self):
        """Test database connection"""
        self.assertIsNotNone(self.db)
        
        # Test basic query
        try:
            result = self.db.execute_query("SELECT 1 as test")
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
    
    def test_users_table_exists(self):
        """Test that users table exists"""
        try:
            result = self.db.execute_query("SELECT COUNT(*) FROM users")
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Users table query failed: {e}")
    
    def test_user_profiles_table_exists(self):
        """Test that user_profiles table exists"""
        try:
            result = self.db.execute_query("SELECT COUNT(*) FROM user_profiles")
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"User profiles table query failed: {e}")

class TestContextManager(unittest.TestCase):
    """Test context manager functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.context_manager = ContextManager()
        
    def test_context_manager_initialization(self):
        """Test context manager initialization"""
        self.assertIsNotNone(self.context_manager)
    
    def test_list_user_profiles(self):
        """Test listing user profiles"""
        try:
            profiles = self.context_manager.list_user_profiles('user1')
            self.assertIsInstance(profiles, list)
            
            # If profiles exist, check their structure
            if profiles:
                profile = profiles[0]
                self.assertIn('profile_id', profile)
                self.assertIn('profile_name', profile)
                self.assertIn('user_id', profile)
                self.assertIn('is_active', profile)
                
        except Exception as e:
            self.fail(f"list_user_profiles failed: {e}")
    
    def test_get_profile_info(self):
        """Test getting profile info"""
        try:
            # First get a list of profiles
            profiles = self.context_manager.list_user_profiles('user1')
            
            if profiles:
                profile_id = profiles[0]['profile_id']
                profile_info = self.context_manager.get_profile_info(profile_id)
                
                self.assertIsNotNone(profile_info)
                self.assertIn('profile_name', profile_info)
                
        except Exception as e:
            self.fail(f"get_profile_info failed: {e}")
    
    def test_invalid_user_id(self):
        """Test with invalid user_id"""
        try:
            profiles = self.context_manager.list_user_profiles('invalid_user')
            self.assertIsInstance(profiles, list)
            # Should return empty list for invalid user
            self.assertEqual(len(profiles), 0)
            
        except Exception as e:
            self.fail(f"list_user_profiles with invalid user failed: {e}")

class TestDatabaseQueries(unittest.TestCase):
    """Test specific database queries"""
    
    def setUp(self):
        """Set up test environment"""
        self.db = get_db_connection()
        
    def test_get_user_profiles_query(self):
        """Test the specific query used for getting user profiles"""
        try:
            query = """
            SELECT profile_id, profile_name, user_id, is_active, data_sources
            FROM user_profiles 
            WHERE user_id = %s AND is_active = true
            ORDER BY created_at DESC
            """
            
            result = self.db.execute_query(query, ('user1',))
            self.assertIsNotNone(result)
            
            # Check if we have profiles for user1
            if result:
                profile = result[0]
                self.assertIn('profile_id', profile)
                self.assertIn('profile_name', profile)
                self.assertIn('user_id', profile)
                self.assertEqual(profile['user_id'], 'user1')
                
        except Exception as e:
            self.fail(f"User profiles query failed: {e}")
    
    def test_user_exists_query(self):
        """Test query to check if user exists"""
        try:
            query = "SELECT user_id FROM users WHERE user_id = %s"
            
            result = self.db.execute_query(query, ('user1',))
            self.assertIsNotNone(result)
            
            # user1 should exist (we added it in sample data)
            self.assertGreater(len(result), 0)
            
        except Exception as e:
            self.fail(f"User exists query failed: {e}")

if __name__ == '__main__':
    unittest.main()
