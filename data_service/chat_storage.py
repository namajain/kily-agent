"""
Chat Storage - Persistent storage for chat sessions and history
"""
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class ChatStorage:
    """File-based storage for chat sessions and history"""
    
    def __init__(self, storage_dir: str = "chat_data"):
        self.storage_dir = Path(storage_dir)
        self.sessions_file = self.storage_dir / "sessions.json"
        self.messages_file = self.storage_dir / "messages.json"
        
        # Create storage directory if it doesn't exist
        self.storage_dir.mkdir(exist_ok=True)
        
        # Initialize storage files
        self._init_storage_files()
    
    def _init_storage_files(self):
        """Initialize storage files if they don't exist"""
        if not self.sessions_file.exists():
            self._save_sessions({})
        
        if not self.messages_file.exists():
            self._save_messages({})
    
    def _load_sessions(self) -> Dict:
        """Load sessions from file"""
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load sessions: {e}")
            return {}
    
    def _save_sessions(self, sessions: Dict):
        """Save sessions to file"""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save sessions: {e}")
    
    def _load_messages(self) -> Dict:
        """Load messages from file"""
        try:
            with open(self.messages_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load messages: {e}")
            return {}
    
    def _save_messages(self, messages: Dict):
        """Save messages to file"""
        try:
            with open(self.messages_file, 'w') as f:
                json.dump(messages, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save messages: {e}")
    
    def create_session(self, session_id: str, user_id: str, profile_id: str, chat_id: str) -> bool:
        """Create a new chat session"""
        try:
            sessions = self._load_sessions()
            
            session_data = {
                'session_id': session_id,
                'user_id': user_id,
                'profile_id': profile_id,
                'chat_id': chat_id,
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'is_active': True
            }
            
            sessions[session_id] = session_data
            self._save_sessions(sessions)
            
            logger.info(f"Created session {session_id} for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create session {session_id}: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        try:
            sessions = self._load_sessions()
            return sessions.get(session_id)
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {e}")
            return None
    
    def update_session_activity(self, session_id: str) -> bool:
        """Update session last activity"""
        try:
            sessions = self._load_sessions()
            
            if session_id in sessions:
                sessions[session_id]['last_activity'] = datetime.now().isoformat()
                self._save_sessions(sessions)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to update session activity {session_id}: {e}")
            return False
    
    def end_session(self, session_id: str) -> bool:
        """End a session"""
        try:
            sessions = self._load_sessions()
            
            if session_id in sessions:
                sessions[session_id]['is_active'] = False
                sessions[session_id]['ended_at'] = datetime.now().isoformat()
                self._save_sessions(sessions)
                logger.info(f"Ended session {session_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to end session {session_id}: {e}")
            return False
    
    def add_message(self, session_id: str, message: Dict) -> bool:
        """Add message to chat history"""
        try:
            messages = self._load_messages()
            
            if session_id not in messages:
                messages[session_id] = []
            
            # Add timestamp if not present
            if 'timestamp' not in message:
                message['timestamp'] = datetime.now().isoformat()
            
            messages[session_id].append(message)
            self._save_messages(messages)
            
            # Update session activity
            self.update_session_activity(session_id)
            
            logger.debug(f"Added message to session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add message to session {session_id}: {e}")
            return False
    
    def get_chat_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a session"""
        try:
            messages = self._load_messages()
            return messages.get(session_id, [])
        except Exception as e:
            logger.error(f"Failed to get chat history for session {session_id}: {e}")
            return []
    
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all sessions for a user"""
        try:
            sessions = self._load_sessions()
            user_sessions = []
            
            for session_id, session_data in sessions.items():
                if session_data.get('user_id') == user_id:
                    user_sessions.append({
                        'session_id': session_id,
                        'profile_id': session_data.get('profile_id'),
                        'created_at': session_data.get('created_at'),
                        'last_activity': session_data.get('last_activity'),
                        'is_active': session_data.get('is_active', False)
                    })
            
            # Sort by last activity (most recent first)
            user_sessions.sort(key=lambda x: x['last_activity'], reverse=True)
            return user_sessions
            
        except Exception as e:
            logger.error(f"Failed to get sessions for user {user_id}: {e}")
            return []
    
    def get_user_chat_history(self, user_id: str) -> List[Dict]:
        """Get all chat history for a user across all sessions"""
        try:
            sessions = self._load_sessions()
            messages = self._load_messages()
            user_history = []
            
            for session_id, session_data in sessions.items():
                if session_data.get('user_id') == user_id:
                    session_messages = messages.get(session_id, [])
                    for message in session_messages:
                        message_with_session = {
                            **message,
                            'session_id': session_id,
                            'profile_id': session_data.get('profile_id'),
                            'session_created_at': session_data.get('created_at')
                        }
                        user_history.append(message_with_session)
            
            # Sort by timestamp (most recent first)
            user_history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return user_history
            
        except Exception as e:
            logger.error(f"Failed to get chat history for user {user_id}: {e}")
            return []
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        """Clean up sessions older than specified days"""
        try:
            sessions = self._load_sessions()
            messages = self._load_messages()
            cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff_date = cutoff_date.replace(day=cutoff_date.day - days_old)
            
            removed_sessions = 0
            
            for session_id, session_data in list(sessions.items()):
                created_at = datetime.fromisoformat(session_data.get('created_at', ''))
                if created_at < cutoff_date:
                    del sessions[session_id]
                    if session_id in messages:
                        del messages[session_id]
                    removed_sessions += 1
            
            self._save_sessions(sessions)
            self._save_messages(messages)
            
            logger.info(f"Cleaned up {removed_sessions} old sessions")
            return removed_sessions
            
        except Exception as e:
            logger.error(f"Failed to cleanup old sessions: {e}")
            return 0
