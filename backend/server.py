"""
Socket.IO Backend Server for MVP - Real-time communication layer
"""
import os
import sys
import logging
from datetime import datetime
from flask import Flask, request
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .api_client import api_client
from .managers.context_manager import ContextManager
from .managers.session_manager import SessionManager
from .agents.qna_agent import QnAAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QnABackend:
    """
    Socket.IO backend server for real-time QnA communication.
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        
        # Enable CORS for all routes
        CORS(self.app, origins="*")
        
        # Initialize Socket.IO with CORS support
        self.socketio = SocketIO(
            self.app, 
            cors_allowed_origins="*",
            logger=True,
            engineio_logger=True
        )
        
        # Initialize components
        logger.info("Initializing backend components...")
        self.context_manager = ContextManager()
        self.session_manager = SessionManager(self.context_manager)
        self.qna_agent = QnAAgent(self.context_manager)
        
        # Setup routes
        self.setup_routes()
        
        logger.info("Backend initialization completed")
    
    def setup_routes(self):
        """Setup Socket.IO event handlers and Flask routes"""
        
        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
        
        @self.app.route('/api/users/<user_id>/profiles')
        def get_user_profiles(user_id):
            """REST endpoint to get user profiles"""
            try:
                profiles = api_client.get_user_profiles(user_id)
                return {'profiles': profiles}
            except Exception as e:
                logger.error(f"Error getting user profiles: {e}")
                return {'error': str(e)}, 500
        
        @self.app.route('/api/users/<user_id>/sessions')
        def get_user_sessions(user_id):
            """REST endpoint to get user chat sessions"""
            try:
                sessions = api_client.get_user_sessions(user_id)
                return {'sessions': sessions}
            except Exception as e:
                logger.error(f"Error getting user sessions: {e}")
                return {'error': str(e)}, 500
        
        @self.app.route('/api/users/<user_id>/chat-history')
        def get_user_chat_history(user_id):
            """REST endpoint to get user chat history"""
            try:
                history = api_client.get_user_chat_history(user_id)
                return {'chat_history': history}
            except Exception as e:
                logger.error(f"Error getting user chat history: {e}")
                return {'error': str(e)}, 500
        
        @self.app.route('/api/sessions/<session_id>/messages')
        def get_session_messages(session_id):
            """REST endpoint to get session messages"""
            try:
                messages = api_client.get_session_messages(session_id)
                return {'messages': messages}
            except Exception as e:
                logger.error(f"Error getting session messages: {e}")
                return {'error': str(e)}, 500
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            logger.info(f"Client connected: {request.sid}")
            emit('connected', {'message': 'Connected to QnA Agent Server'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            logger.info(f"Client disconnected: {request.sid}")
        
        @self.socketio.on('authenticate')
        def handle_authentication(data):
            """Handle user authentication"""
            try:
                user_id = data.get('user_id')
                profile_id = data.get('profile_id')
                
                if not user_id or not profile_id:
                    emit('auth_error', {'message': 'User ID and Profile ID are required'})
                    return
                
                # Validate user exists
                if self._validate_user(user_id):
                    emit('authenticated', {
                        'user_id': user_id,
                        'profile_id': profile_id,
                        'message': 'Authentication successful'
                    })
                else:
                    emit('auth_error', {'message': 'User not found'})
                    
            except Exception as e:
                logger.error(f"Authentication error: {e}")
                emit('auth_error', {'message': f'Authentication failed: {str(e)}'})
        
        @self.socketio.on('start_chat')
        def handle_start_chat(data):
            """Handle chat start request with profile_id from frontend"""
            try:
                user_id = data.get('user_id')
                profile_id = data.get('profile_id')
                
                if not user_id or not profile_id:
                    emit('error', {'message': 'User ID and Profile ID are required'})
                    return
                
                logger.info(f"Starting chat for user {user_id} with profile {profile_id}")
                
                # Create session for the specific profile
                session_id = self.session_manager.create_session(user_id, profile_id)
                
                # Get profile info
                profile_info = self.context_manager.get_profile_info(profile_id)
                
                emit('chat_started', {
                    'session_id': session_id,
                    'profile_id': profile_id,
                    'profile_name': profile_info.get('profile_name', 'Unknown Profile'),
                    'message': 'Chat session created successfully'
                })
                
                logger.info(f"Chat session {session_id} created for user {user_id}")
                
            except Exception as e:
                logger.error(f"Failed to start chat: {e}")
                emit('error', {'message': f'Failed to start chat: {str(e)}'})
        
        @self.socketio.on('send_message')
        def handle_message(data):
            """Handle chat message with profile context"""
            try:
                session_id = data.get('session_id')
                message = data.get('message')
                
                if not session_id or not message:
                    emit('error', {'message': 'Session ID and message are required'})
                    return
                
                logger.info(f"Processing message for session {session_id}")
                
                # Get session
                session = self.session_manager.get_session(session_id)
                if not session:
                    emit('error', {'message': 'Session expired or not found'})
                    return
                
                # Validate query
                if not self.qna_agent.validate_query(message):
                    emit('error', {'message': 'Invalid query detected'})
                    return
                
                # Add user message to history
                self.session_manager.add_message(session_id, {
                    'type': 'user',
                    'content': message,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Get context data from session
                context_data = session.get('context_data', {})
                
                # Get chat history and convert to expected format
                chat_history = session.get('chat_history', [])
                formatted_history = []
                for msg in chat_history:
                    if msg.get('type') == 'user':
                        formatted_history.append({'role': 'user', 'content': msg.get('content', '')})
                    elif msg.get('type') == 'assistant':
                        formatted_history.append({'role': 'assistant', 'content': msg.get('content', '')})
                
                # Process with QnA agent using profile context and chat history
                response = self.qna_agent.analyze_with_context(message, context_data, formatted_history)
                
                # Add assistant response to history
                self.session_manager.add_message(session_id, {
                    'type': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Sync session state to ensure all data is persisted
                self.session_manager.sync_session_state(session_id)
                
                emit('message_response', {
                    'response': response,
                    'timestamp': datetime.now().isoformat(),
                    'session_id': session_id
                })
                
                logger.info(f"Message processed successfully for session {session_id}")
                
            except Exception as e:
                logger.error(f"Message processing failed: {e}")
                emit('error', {'message': f'Analysis failed: {str(e)}'})
        
        @self.socketio.on('get_chat_history')
        def handle_get_chat_history(data):
            """Get chat history for a session"""
            try:
                session_id = data.get('session_id')
                
                if not session_id:
                    emit('error', {'message': 'Session ID is required'})
                    return
                
                chat_history = self.session_manager.get_chat_history(session_id)
                
                emit('chat_history', {
                    'session_id': session_id,
                    'history': chat_history
                })
                
            except Exception as e:
                logger.error(f"Failed to get chat history: {e}")
                emit('error', {'message': f'Failed to get chat history: {str(e)}'})
        

        
        @self.socketio.on('get_context_summary')
        def handle_get_context_summary(data):
            """Get summary of context data for a session"""
            try:
                session_id = data.get('session_id')
                
                if not session_id:
                    emit('error', {'message': 'Session ID is required'})
                    return
                
                context_data = self.session_manager.get_context_data(session_id)
                if not context_data:
                    emit('error', {'message': 'No context data available'})
                    return
                
                summary = self.qna_agent.get_basic_summary(context_data)
                datasets = self.qna_agent.get_available_datasets(context_data)
                
                emit('context_summary', {
                    'session_id': session_id,
                    'summary': summary,
                    'datasets': datasets
                })
                
            except Exception as e:
                logger.error(f"Failed to get context summary: {e}")
                emit('error', {'message': f'Failed to get context summary: {str(e)}'})
        
        @self.socketio.on('end_session')
        def handle_end_session(data):
            """End a session"""
            try:
                session_id = data.get('session_id')
                
                if not session_id:
                    emit('error', {'message': 'Session ID is required'})
                    return
                
                self.session_manager.end_session(session_id)
                
                emit('session_ended', {
                    'session_id': session_id,
                    'message': 'Session ended successfully'
                })
                
            except Exception as e:
                logger.error(f"Failed to end session: {e}")
                emit('error', {'message': f'Failed to end session: {str(e)}'})
        
        @self.socketio.on('get_session_stats')
        def handle_get_session_stats(data):
            """Get session statistics"""
            try:
                stats = self.session_manager.get_session_stats()
                
                emit('session_stats', stats)
                
            except Exception as e:
                logger.error(f"Failed to get session stats: {e}")
                emit('error', {'message': f'Failed to get session stats: {str(e)}'})
        
        @self.socketio.on('restore_session')
        def handle_restore_session(data):
            """Restore a session from persistent storage"""
            try:
                session_id = data.get('session_id')
                
                if not session_id:
                    emit('error', {'message': 'Session ID is required'})
                    return
                
                logger.info(f"Restoring session {session_id}")
                
                # Get session from data service
                session_data = api_client.get_session(session_id)
                if not session_data:
                    emit('error', {'message': 'Session not found'})
                    return
                
                # Get chat history from data service
                messages = api_client.get_session_messages(session_id)
                
                # Get profile info
                profile_info = self.context_manager.get_profile_info(session_data.get('profile_id'))
                
                # Restore session in memory (without recreating)
                restored_session = {
                    'session_id': session_id,
                    'user_id': session_data.get('user_id'),
                    'profile_id': session_data.get('profile_id'),
                    'chat_id': session_data.get('chat_id'),
                    'created_at': datetime.fromisoformat(session_data.get('created_at')),
                    'last_activity': datetime.fromisoformat(session_data.get('last_activity')),
                    'chat_history': messages,
                    'context_data': self.context_manager.get_context_for_profile(session_data.get('profile_id'))
                }
                
                # Store in memory
                self.session_manager.active_sessions[session_id] = restored_session
                
                emit('session_restored', {
                    'session_id': session_id,
                    'profile_id': session_data.get('profile_id'),
                    'profile_name': profile_info.get('profile_name', 'Unknown Profile'),
                    'chat_history': messages,
                    'message': 'Session restored successfully'
                })
                
                logger.info(f"Session {session_id} restored successfully")
                
            except Exception as e:
                logger.error(f"Failed to restore session: {e}")
                emit('error', {'message': f'Failed to restore session: {str(e)}'})
    
    def _validate_user(self, user_id: str) -> bool:
        """Validate if user exists via API"""
        try:
            user = api_client.get_user(user_id)
            return user is not None
        except Exception as e:
            logger.error(f"Failed to validate user {user_id}: {e}")
            return False
    
    def run(self, host='0.0.0.0', port=5001, debug=False):
        """Run the Socket.IO server"""
        logger.info(f"Starting QnA Agent Server on {host}:{port}")
        
        # Check API connection
        logger.info("Checking API connection...")
        if not api_client.health_check():
            logger.error("Mock API server is not available")
            raise RuntimeError("Mock API server is not available")
        logger.info("Mock API server is available")
        
        self.socketio.run(
            self.app, 
            host=host, 
            port=port, 
            debug=debug,
            allow_unsafe_werkzeug=True
        )

def main():
    """Main entry point"""
    try:
        # Create and run server
        server = QnABackend()
        server.run(debug=True)
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 