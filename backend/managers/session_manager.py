"""
Session Manager for MVP - Handles user sessions with profile-based context
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from ..api_client import api_client

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Manages user sessions with profile-based context.
    Sessions have 15-minute timeout and are tied to specific profiles.
    """
    
    def __init__(self, context_manager, session_timeout: int = 900):  # 15 minutes
        self.context_manager = context_manager
        self.session_timeout = session_timeout
        self.active_sessions = {}  # In-memory session storage
    
    def create_session(self, user_id: str, profile_id: str) -> str:
        """
        Create a new session for a specific profile.
        Called when user starts a chat for a profile.
        """
        try:
            session_id = str(uuid.uuid4())
            chat_id = str(uuid.uuid4())
            
            logger.info(f"Creating session for user {user_id} with profile {profile_id}")
            
            # Load context for the profile (triggers download if needed)
            context_data = self.context_manager.get_context_for_profile(profile_id)
            
            session = {
                'session_id': session_id,
                'user_id': user_id,
                'profile_id': profile_id,
                'chat_id': chat_id,
                'created_at': datetime.now(),
                'last_activity': datetime.now(),
                'chat_history': [],
                'context_data': context_data
            }
            
            # Store in memory
            self.active_sessions[session_id] = session
            
            # Create chat record in database (temporarily disabled for API client migration)
            # self._create_chat_record(chat_id, user_id, profile_id)
            
            logger.info(f"Session {session_id} created successfully")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create session for user {user_id}: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session by ID, extending timeout if found.
        Returns None if session is expired.
        """
        try:
            session = self.active_sessions.get(session_id)
            
            if session:
                # Check if session is expired
                if (datetime.now() - session['last_activity']).seconds > self.session_timeout:
                    logger.info(f"Session {session_id} expired, removing")
                    del self.active_sessions[session_id]
                    return None
                
                # Extend timeout
                session['last_activity'] = datetime.now()
                logger.debug(f"Session {session_id} activity updated")
            
            return session
            
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {e}")
            return None
    
    def add_message(self, session_id: str, message: Dict):
        """
        Add message to session chat history.
        Updates both memory and database.
        """
        try:
            session = self.get_session(session_id)
            if not session:
                logger.warning(f"Cannot add message to expired session {session_id}")
                return
            
            # Add timestamp if not present
            if 'timestamp' not in message:
                message['timestamp'] = datetime.now().isoformat()
            
            # Add to memory
            session['chat_history'].append(message)
            session['last_activity'] = datetime.now()
            
            # Store in database (temporarily disabled for API client migration)
            # self._store_chat_message(session['chat_id'], message)
            
            logger.debug(f"Message added to session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to add message to session {session_id}: {e}")
            raise
    
    def get_chat_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a session"""
        try:
            session = self.get_session(session_id)
            if not session:
                return []
            
            return session.get('chat_history', [])
            
        except Exception as e:
            logger.error(f"Failed to get chat history for session {session_id}: {e}")
            return []
    
    def get_context_data(self, session_id: str) -> Optional[Dict]:
        """Get context data for a session"""
        try:
            session = self.get_session(session_id)
            if not session:
                return None
            
            return session.get('context_data', {})
            
        except Exception as e:
            logger.error(f"Failed to get context data for session {session_id}: {e}")
            return None
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions from memory"""
        try:
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session in self.active_sessions.items():
                if (current_time - session['last_activity']).seconds > self.session_timeout:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self.active_sessions[session_id]
                logger.info(f"Cleaned up expired session {session_id}")
            
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {e}")
    
    def _create_chat_record(self, chat_id: str, user_id: str, profile_id: str):
        """Create chat record in database (temporarily disabled)"""
        # Temporarily disabled for API client migration
        logger.debug(f"Chat record creation disabled: {chat_id}")
        pass
    
    def _store_chat_message(self, chat_id: str, message: Dict):
        """Store chat message in database (temporarily disabled)"""
        # Temporarily disabled for API client migration
        logger.debug(f"Message storage disabled: {message.get('type', 'unknown')}")
        pass
    
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all active sessions for a user"""
        try:
            user_sessions = []
            for session_id, session in self.active_sessions.items():
                if session['user_id'] == user_id:
                    # Check if session is still valid
                    if (datetime.now() - session['last_activity']).seconds <= self.session_timeout:
                        user_sessions.append({
                            'session_id': session_id,
                            'profile_id': session['profile_id'],
                            'created_at': session['created_at'].isoformat(),
                            'last_activity': session['last_activity'].isoformat()
                        })
            
            return user_sessions
            
        except Exception as e:
            logger.error(f"Failed to get sessions for user {user_id}: {e}")
            return []
    
    def end_session(self, session_id: str):
        """End a session and clean up resources"""
        try:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
                logger.info(f"Session {session_id} ended")
            
        except Exception as e:
            logger.error(f"Failed to end session {session_id}: {e}")
    
    def get_session_stats(self) -> Dict:
        """Get session statistics"""
        try:
            current_time = datetime.now()
            active_count = 0
            expired_count = 0
            
            for session in self.active_sessions.values():
                if (current_time - session['last_activity']).seconds <= self.session_timeout:
                    active_count += 1
                else:
                    expired_count += 1
            
            return {
                'total_sessions': len(self.active_sessions),
                'active_sessions': active_count,
                'expired_sessions': expired_count,
                'session_timeout_seconds': self.session_timeout
            }
            
        except Exception as e:
            logger.error(f"Failed to get session stats: {e}")
            return {} 