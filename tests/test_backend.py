#!/usr/bin/env python3
"""
Unit tests for backend Socket.IO functionality
"""
import unittest
import socketio
import time
import threading
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.server import QnABackend

class TestBackendSocketIO(unittest.TestCase):
    """Test backend Socket.IO functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.backend = QnABackend()
        self.client = socketio.Client()
        self.test_results = {}
        
    def tearDown(self):
        """Clean up after tests"""
        if self.client.connected:
            self.client.disconnect()
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        with self.backend.app.test_client() as client:
            response = client.get('/health')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'healthy')
    
    def test_socketio_connection(self):
        """Test Socket.IO connection"""
        connected = threading.Event()
        received_data = {}
        
        @self.client.event
        def connect():
            connected.set()
        
        @self.client.on('connected')
        def on_connected(data):
            received_data['connected'] = data
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(
            target=self.backend.socketio.run,
            args=(self.backend.app,),
            kwargs={'host': 'localhost', 'port': 5002, 'debug': False},
            daemon=True
        )
        backend_thread.start()
        
        # Wait for backend to start
        time.sleep(2)
        
        try:
            # Connect client
            self.client.connect('http://localhost:5002')
            
            # Wait for connection
            self.assertTrue(connected.wait(timeout=5))
            
            # Check received data
            self.assertIn('connected', received_data)
            self.assertIn('message', received_data['connected'])
            
        finally:
            # Cleanup
            if self.client.connected:
                self.client.disconnect()
    
    def test_get_user_profiles_event(self):
        """Test get_user_profiles Socket.IO event"""
        connected = threading.Event()
        profiles_received = threading.Event()
        received_profiles = {}
        
        @self.client.event
        def connect():
            connected.set()
        
        @self.client.on('user_profiles')
        def on_user_profiles(data):
            received_profiles['data'] = data
            profiles_received.set()
        
        @self.client.on('error')
        def on_error(data):
            received_profiles['error'] = data
            profiles_received.set()
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(
            target=self.backend.socketio.run,
            args=(self.backend.app,),
            kwargs={'host': 'localhost', 'port': 5003, 'debug': False},
            daemon=True
        )
        backend_thread.start()
        
        # Wait for backend to start
        time.sleep(2)
        
        try:
            # Connect client
            self.client.connect('http://localhost:5003')
            
            # Wait for connection
            self.assertTrue(connected.wait(timeout=5))
            
            # Send get_user_profiles event
            self.client.emit('get_user_profiles', {'user_id': 'user1'})
            
            # Wait for response
            self.assertTrue(profiles_received.wait(timeout=10))
            
            # Check response
            self.assertIn('data', received_profiles)
            data = received_profiles['data']
            self.assertIn('user_id', data)
            self.assertIn('profiles', data)
            self.assertEqual(data['user_id'], 'user1')
            self.assertIsInstance(data['profiles'], list)
            
        finally:
            # Cleanup
            if self.client.connected:
                self.client.disconnect()
    
    def test_invalid_user_id(self):
        """Test get_user_profiles with invalid user_id"""
        connected = threading.Event()
        error_received = threading.Event()
        received_error = {}
        
        @self.client.event
        def connect():
            connected.set()
        
        @self.client.on('error')
        def on_error(data):
            received_error['data'] = data
            error_received.set()
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(
            target=self.backend.socketio.run,
            args=(self.backend.app,),
            kwargs={'host': 'localhost', 'port': 5004, 'debug': False},
            daemon=True
        )
        backend_thread.start()
        
        # Wait for backend to start
        time.sleep(2)
        
        try:
            # Connect client
            self.client.connect('http://localhost:5004')
            
            # Wait for connection
            self.assertTrue(connected.wait(timeout=5))
            
            # Send get_user_profiles event with invalid user_id
            self.client.emit('get_user_profiles', {'user_id': ''})
            
            # Wait for error response
            self.assertTrue(error_received.wait(timeout=10))
            
            # Check error response
            self.assertIn('data', received_error)
            error_data = received_error['data']
            self.assertIn('message', error_data)
            
        finally:
            # Cleanup
            if self.client.connected:
                self.client.disconnect()

if __name__ == '__main__':
    unittest.main()
