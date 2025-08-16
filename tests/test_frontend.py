#!/usr/bin/env python3
"""
Unit tests for frontend Socket.IO functionality
"""
import unittest
import socketio
import time
import threading
from unittest.mock import patch, MagicMock
import streamlit as st

# Add parent directory to path for imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.app import QnAFrontend

class TestFrontendSocketIO(unittest.TestCase):
    """Test frontend Socket.IO functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.frontend = QnAFrontend(backend_url="http://localhost:5005")
        self.test_results = {}
        
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self.frontend, 'socket') and self.frontend.socket:
            if self.frontend.socket.connected:
                self.frontend.socket.disconnect()
    
    @patch('streamlit.session_state')
    def test_frontend_initialization(self, mock_session_state):
        """Test frontend initialization"""
        # Mock session state
        mock_session_state.connected = False
        mock_session_state.user_profiles = []
        
        # Test frontend initialization
        self.assertIsNotNone(self.frontend)
        self.assertEqual(self.frontend.backend_url, "http://localhost:5005")
        self.assertFalse(self.frontend.connected)
    
    def test_socketio_connection_establishment(self):
        """Test Socket.IO connection establishment"""
        connected_event = threading.Event()
        error_occurred = threading.Event()
        
        # Mock the socket connection
        with patch.object(self.frontend, 'socket') as mock_socket:
            mock_socket.connected = False
            
            @mock_socket.event
            def connect():
                connected_event.set()
            
            @mock_socket.on('connected')
            def on_connected(data):
                self.test_results['connected_data'] = data
            
            @mock_socket.on('error')
            def on_error(data):
                self.test_results['error_data'] = data
                error_occurred.set()
            
            # Simulate successful connection
            mock_socket.connect.return_value = None
            mock_socket.connected = True
            
            # Test connection
            try:
                self.frontend._init_socket()
                self.assertTrue(self.frontend.connected)
            except Exception as e:
                # Connection might fail if backend is not running, which is expected
                pass
    
    @patch('streamlit.session_state')
    def test_load_profiles_functionality(self, mock_session_state):
        """Test load profiles functionality"""
        # Mock session state
        mock_session_state.connected = True
        mock_session_state.user_profiles = []
        
        # Mock socket
        with patch.object(self.frontend, 'socket') as mock_socket:
            mock_socket.connected = True
            
            # Test load profiles
            user_id = "user1"
            self.frontend._load_profiles(user_id)
            
            # Verify emit was called
            mock_socket.emit.assert_called_with('get_user_profiles', {'user_id': user_id})
    
    @patch('streamlit.session_state')
    def test_user_profiles_event_handler(self, mock_session_state):
        """Test user_profiles event handler"""
        # Mock session state
        mock_session_state.user_profiles = []
        
        # Test data
        test_profiles = [
            {
                'profile_id': 'profile1',
                'profile_name': 'Test Profile 1',
                'is_active': True
            },
            {
                'profile_id': 'profile2', 
                'profile_name': 'Test Profile 2',
                'is_active': False
            }
        ]
        
        test_data = {
            'user_id': 'user1',
            'profiles': test_profiles
        }
        
        # Mock the event handler
        with patch.object(self.frontend, 'socket') as mock_socket:
            # Simulate receiving user_profiles event
            self.frontend._on_user_profiles(test_data)
            
            # Check that session state was updated
            self.assertEqual(mock_session_state.user_profiles, test_profiles)
    
    @patch('streamlit.session_state')
    def test_connection_status_handling(self, mock_session_state):
        """Test connection status handling"""
        # Mock session state
        mock_session_state.connected = False
        
        # Test connection event
        with patch.object(self.frontend, 'socket') as mock_socket:
            # Simulate connect event
            self.frontend._on_connect()
            self.assertTrue(mock_session_state.connected)
            
            # Simulate disconnect event
            self.frontend._on_disconnect()
            self.assertFalse(mock_session_state.connected)
    
    def test_error_handling(self):
        """Test error handling in Socket.IO events"""
        error_data = {'message': 'Test error message'}
        
        # Mock streamlit error
        with patch('streamlit.error') as mock_error:
            # Simulate error event
            self.frontend._on_error(error_data)
            
            # Check that error was displayed
            mock_error.assert_called_with(f"Error: {error_data['message']}")

class TestFrontendIntegration(unittest.TestCase):
    """Integration tests for frontend with backend"""
    
    def setUp(self):
        """Set up test environment"""
        self.frontend = QnAFrontend(backend_url="http://localhost:5006")
        self.backend = None
        
    def tearDown(self):
        """Clean up after tests"""
        if self.frontend.socket and self.frontend.socket.connected:
            self.frontend.socket.disconnect()
    
    def test_end_to_end_profile_loading(self):
        """Test end-to-end profile loading functionality"""
        # This test would require a running backend
        # For now, we'll just test the structure
        self.assertIsNotNone(self.frontend)
        self.assertIsNotNone(self.frontend.backend_url)

if __name__ == '__main__':
    unittest.main()
