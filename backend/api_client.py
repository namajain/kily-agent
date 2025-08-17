"""
API Client for communicating with Mock API Server
"""
import os
import logging
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class APIClient:
    """Client for communicating with Mock API Server"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv('MOCK_API_URL', 'http://localhost:5002')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Optional[Dict]:
        """Make HTTP request to API"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data if data else {})
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in API request: {e}")
            return None
    
    def health_check(self) -> bool:
        """Check if API server is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self._make_request('GET', f'/api/users/{user_id}')
    
    def create_user(self, user_id: str, username: str, email: str) -> bool:
        """Create a new user"""
        data = {
            'user_id': user_id,
            'username': username,
            'email': email
        }
        result = self._make_request('POST', '/api/users', data)
        return result is not None
    
    def update_user(self, user_id: str, username: str = None, email: str = None) -> bool:
        """Update user"""
        data = {}
        if username:
            data['username'] = username
        if email:
            data['email'] = email
        
        result = self._make_request('PUT', f'/api/users/{user_id}', data)
        return result is not None
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        result = self._make_request('DELETE', f'/api/users/{user_id}')
        return result is not None
    
    def get_user_profiles(self, user_id: str) -> List[Dict]:
        """Get all profiles for a user"""
        result = self._make_request('GET', f'/api/users/{user_id}/profiles')
        if result and 'profiles' in result:
            return result['profiles']
        return []
    
    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Get profile by ID"""
        return self._make_request('GET', f'/api/profiles/{profile_id}')
    
    # Chat Storage methods
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all chat sessions for a user"""
        result = self._make_request('GET', f'/api/users/{user_id}/sessions')
        if result and 'sessions' in result:
            return result['sessions']
        return []
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session details"""
        return self._make_request('GET', f'/api/sessions/{session_id}')
    
    def get_session_messages(self, session_id: str) -> List[Dict]:
        """Get chat messages for a session"""
        result = self._make_request('GET', f'/api/sessions/{session_id}/messages')
        if result and 'messages' in result:
            return result['messages']
        return []
    
    def get_user_chat_history(self, user_id: str) -> List[Dict]:
        """Get all chat history for a user across all sessions"""
        result = self._make_request('GET', f'/api/users/{user_id}/chat-history')
        if result and 'chat_history' in result:
            return result['chat_history']
        return []
    
    def create_session(self, session_id: str, user_id: str, profile_id: str, chat_id: str) -> bool:
        """Create a new chat session"""
        data = {
            'user_id': user_id,
            'profile_id': profile_id,
            'chat_id': chat_id
        }
        result = self._make_request('POST', f'/api/sessions/{session_id}', data)
        return result is not None
    
    def add_message(self, session_id: str, message: Dict) -> bool:
        """Add a message to a session"""
        data = {'message': message}
        result = self._make_request('POST', f'/api/sessions/{session_id}/messages', data)
        return result is not None
    
    def update_session_activity(self, session_id: str) -> bool:
        """Update session last activity timestamp"""
        result = self._make_request('PUT', f'/api/sessions/{session_id}/activity')
        return result is not None
    
    def end_session(self, session_id: str) -> bool:
        """End a session"""
        result = self._make_request('DELETE', f'/api/sessions/{session_id}')
        return result is not None
    
    def create_profile(self, profile_id: str, user_id: str, profile_name: str, 
                      data_sources: List[Dict], is_active: bool = True) -> bool:
        """Create a new profile"""
        data = {
            'profile_id': profile_id,
            'user_id': user_id,
            'profile_name': profile_name,
            'data_sources': data_sources,
            'is_active': is_active
        }
        result = self._make_request('POST', '/api/profiles', data)
        return result is not None
    
    def update_profile(self, profile_id: str, profile_name: str = None, 
                      data_sources: List[Dict] = None, is_active: bool = None) -> bool:
        """Update profile"""
        data = {}
        if profile_name:
            data['profile_name'] = profile_name
        if data_sources is not None:
            data['data_sources'] = data_sources
        if is_active is not None:
            data['is_active'] = is_active
        
        result = self._make_request('PUT', f'/api/profiles/{profile_id}', data)
        return result is not None
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete profile"""
        result = self._make_request('DELETE', f'/api/profiles/{profile_id}')
        return result is not None

# Global API client instance
api_client = APIClient()
