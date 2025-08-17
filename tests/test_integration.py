#!/usr/bin/env python3
"""
Integration tests for the complete system
"""
import unittest
import socketio
import time
import threading
import subprocess
import signal
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.server import QnABackend

class TestFullSystemIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up test environment"""
        self.backend = None
        self.backend_thread = None
        self.client = socketio.Client()
        self.test_port = 5007
        
    def tearDown(self):
        """Clean up after tests"""
        if self.client.connected:
            self.client.disconnect()
        
        if self.backend_thread and self.backend_thread.is_alive():
            # Stop the backend
            if self.backend:
                self.backend.socketio.stop()
            self.backend_thread.join(timeout=5)
    
    def start_backend(self):
        """Start the backend server in a separate thread"""
        self.backend = QnABackend()
        
        self.backend_thread = threading.Thread(
            target=self.backend.socketio.run,
            args=(self.backend.app,),
            kwargs={
                'host': 'localhost', 
                'port': self.test_port, 
                'debug': False,
                'allow_unsafe_werkzeug': True
            },
            daemon=True
        )
        self.backend_thread.start()
        
        # Wait for backend to start
        time.sleep(3)
    
    def test_full_profile_loading_flow(self):
        """Test the complete flow from Socket.IO connection to profile loading"""
        # Start backend
        self.start_backend()
        
        # Setup event handlers
        connected_event = threading.Event()
        profiles_received = threading.Event()
        received_data = {}
        
        @self.client.event
        def connect():
            print("✅ Client connected to backend")
            connected_event.set()
        
        @self.client.event
        def disconnect():
            print("❌ Client disconnected from backend")
        
        @self.client.on('connected')
        def on_connected(data):
            print(f"🎉 Backend confirmed connection: {data}")
            received_data['connected'] = data
        
        @self.client.on('user_profiles')
        def on_user_profiles(data):
            print(f"📁 Received user profiles: {data}")
            received_data['profiles'] = data
            profiles_received.set()
        
        @self.client.on('error')
        def on_error(data):
            print(f"❌ Error received: {data}")
            received_data['error'] = data
            profiles_received.set()
        
        try:
            # Connect to backend
            print(f"🔌 Connecting to backend on port {self.test_port}...")
            self.client.connect(f'http://localhost:{self.test_port}')
            
            # Wait for connection
            self.assertTrue(connected_event.wait(timeout=10), "Connection timeout")
            
            # Verify connection data
            self.assertIn('connected', received_data)
            self.assertIn('message', received_data['connected'])
            
            # Send get_user_profiles event
            print("📤 Sending get_user_profiles event...")
            self.client.emit('get_user_profiles', {'user_id': 'user1'})
            
            # Wait for response
            self.assertTrue(profiles_received.wait(timeout=10), "Profile response timeout")
            
            # Verify response
            self.assertIn('profiles', received_data)
            profiles_data = received_data['profiles']
            
            self.assertIn('user_id', profiles_data)
            self.assertIn('profiles', profiles_data)
            self.assertEqual(profiles_data['user_id'], 'user1')
            self.assertIsInstance(profiles_data['profiles'], list)
            
            # Check that we have profiles
            self.assertGreater(len(profiles_data['profiles']), 0, "No profiles returned")
            
            # Verify profile structure
            profile = profiles_data['profiles'][0]
            self.assertIn('profile_id', profile)
            self.assertIn('profile_name', profile)
            self.assertIn('user_id', profile)
            self.assertIn('is_active', profile)
            
            print(f"✅ Successfully loaded {len(profiles_data['profiles'])} profiles")
            
        except Exception as e:
            self.fail(f"Integration test failed: {e}")
    
    def test_multiple_connections(self):
        """Test multiple concurrent connections"""
        # Start backend
        self.start_backend()
        
        # Create multiple clients
        clients = []
        results = []
        
        def client_test(client_id):
            client = socketio.Client()
            connected_event = threading.Event()
            client_result = {'client_id': client_id, 'success': False}
            
            @client.event
            def connect():
                connected_event.set()
            
            @client.on('connected')
            def on_connected(data):
                client_result['connected'] = True
            
            try:
                client.connect(f'http://localhost:{self.test_port}')
                self.assertTrue(connected_event.wait(timeout=5))
                
                # Send get_user_profiles event
                client.emit('get_user_profiles', {'user_id': 'user1'})
                
                # Wait a bit for response
                time.sleep(2)
                
                client_result['success'] = True
                
            except Exception as e:
                client_result['error'] = str(e)
            finally:
                if client.connected:
                    client.disconnect()
            
            results.append(client_result)
        
        # Start multiple client threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=client_test, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10)
        
        # Check results
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result['success'], f"Client {result['client_id']} failed: {result.get('error', 'Unknown error')}")
    
    def test_backend_health_endpoint(self):
        """Test backend health endpoint"""
        # Start backend
        self.start_backend()
        
        # Test health endpoint
        import requests
        try:
            response = requests.get(f'http://localhost:{self.test_port}/health', timeout=5)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'healthy')
            
        except Exception as e:
            self.fail(f"Health endpoint test failed: {e}")

if __name__ == '__main__':
    unittest.main()
