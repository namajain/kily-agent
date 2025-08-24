"""
Data Service Server - REST API with hardcoded data (no PostgreSQL dependency)
"""
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import chat storage
from chat_storage import ChatStorage

# Import logging config from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.utils.logging_config import setup_service_logging

# Hardcoded data instead of database
HARDCODED_USERS = {
    "user1": {
        "user_id": "user1",
        "username": "demo_user",
        "email": "demo@example.com",
        "created_at": "2024-01-01T00:00:00"
    }
}

HARDCODED_PROFILES = {
    "profile1": {
        "profile_id": "profile1",
        "user_id": "user1",
        "profile_name": "Sales Analytics",
        "data_sources": [
            {
                "url": "file://downloads/2025-08-16/profile1/sales.csv",
                "filename": "sales.csv",
                "description": "Sales data by region and product"
            },
            {
                "url": "file://downloads/2025-08-16/profile1/products.csv",
                "filename": "products.csv",
                "description": "Product catalog and pricing"
            },
            {
                "url": "file://downloads/2025-08-16/profile1/regions.csv",
                "filename": "regions.csv",
                "description": "Regional sales territories"
            }
        ],
        "is_active": True,
        "created_at": "2024-01-01T00:00:00"
    },
    "profile2": {
        "profile_id": "profile2",
        "user_id": "user1",
        "profile_name": "Customer Analytics",
        "data_sources": [
            {
                "url": "file://downloads/2025-08-17/profile2/this_month_keyword_summary.csv",
                "filename": "this_month_keyword_summary.csv",
                "description": "This month keyword performance summary"
            },
            {
                "url": "file://downloads/2025-08-17/profile2/this_week_keyword_summary.csv",
                "filename": "this_week_keyword_summary.csv",
                "description": "This week keyword performance summary"
            }
        ],
        "is_active": True,
        "created_at": "2024-01-02T00:00:00"
    }
}

# Load environment variables
load_dotenv()

# Configure logging using centralized config
logger = setup_service_logging('data_service', log_level=os.getenv('LOG_LEVEL', 'INFO'))

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize chat storage
chat_storage = ChatStorage()

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'data-service',
        'mode': 'hardcoded'
    })

# User endpoints
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = HARDCODED_USERS.get(user_id)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user (not implemented in hardcoded mode)"""
    return jsonify({'error': 'User creation not supported in hardcoded mode'}), 501

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user (not implemented in hardcoded mode)"""
    return jsonify({'error': 'User updates not supported in hardcoded mode'}), 501

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user (not implemented in hardcoded mode)"""
    return jsonify({'error': 'User deletion not supported in hardcoded mode'}), 501

# Profile endpoints
@app.route('/api/users/<user_id>/profiles', methods=['GET'])
def get_user_profiles(user_id):
    """Get all profiles for a user"""
    try:
        # Filter profiles by user_id
        user_profiles = [
            profile for profile in HARDCODED_PROFILES.values()
            if profile['user_id'] == user_id and profile['is_active']
        ]
        
        return jsonify({
            'user_id': user_id,
            'profiles': user_profiles
        }), 200
    except Exception as e:
        logger.error(f"Error getting profiles for user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles/<profile_id>', methods=['GET'])
def get_profile(profile_id):
    """Get profile by ID"""
    try:
        profile = HARDCODED_PROFILES.get(profile_id)
        if profile:
            return jsonify(profile), 200
        else:
            return jsonify({'error': 'Profile not found'}), 404
    except Exception as e:
        logger.error(f"Error getting profile {profile_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Create a new profile (not implemented in hardcoded mode)"""
    return jsonify({'error': 'Profile creation not supported in hardcoded mode'}), 501

@app.route('/api/profiles/<profile_id>', methods=['PUT'])
def update_profile(profile_id):
    """Update profile (not implemented in hardcoded mode)"""
    return jsonify({'error': 'Profile updates not supported in hardcoded mode'}), 501

@app.route('/api/profiles/<profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Delete profile (not implemented in hardcoded mode)"""
    return jsonify({'error': 'Profile deletion not supported in hardcoded mode'}), 501

# Chat History endpoints
@app.route('/api/users/<user_id>/sessions', methods=['GET'])
def get_user_sessions(user_id):
    """Get all chat sessions for a user"""
    try:
        sessions = chat_storage.get_user_sessions(user_id)
        return jsonify({
            'user_id': user_id,
            'sessions': sessions
        }), 200
    except Exception as e:
        logger.error(f"Error getting sessions for user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session details"""
    try:
        session = chat_storage.get_session(session_id)
        if session:
            return jsonify(session), 200
        else:
            return jsonify({'error': 'Session not found'}), 404
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sessions/<session_id>/messages', methods=['GET'])
def get_session_messages(session_id):
    """Get chat messages for a session"""
    try:
        messages = chat_storage.get_chat_history(session_id)
        return jsonify({
            'session_id': session_id,
            'messages': messages
        }), 200
    except Exception as e:
        logger.error(f"Error getting messages for session {session_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users/<user_id>/chat-history', methods=['GET'])
def get_user_chat_history(user_id):
    """Get all chat history for a user across all sessions"""
    try:
        history = chat_storage.get_user_chat_history(user_id)
        return jsonify({
            'user_id': user_id,
            'chat_history': history
        }), 200
    except Exception as e:
        logger.error(f"Error getting chat history for user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sessions/<session_id>', methods=['POST'])
def create_session(session_id):
    """Create a new chat session"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        profile_id = data.get('profile_id')
        chat_id = data.get('chat_id')
        
        if not all([user_id, profile_id, chat_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = chat_storage.create_session(session_id, user_id, profile_id, chat_id)
        if success:
            return jsonify({'message': 'Session created successfully'}), 201
        else:
            return jsonify({'error': 'Failed to create session'}), 500
    except Exception as e:
        logger.error(f"Error creating session {session_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sessions/<session_id>/messages', methods=['POST'])
def add_message(session_id):
    """Add a message to a session"""
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        success = chat_storage.add_message(session_id, message)
        if success:
            return jsonify({'message': 'Message added successfully'}), 201
        else:
            return jsonify({'error': 'Failed to add message'}), 500
    except Exception as e:
        logger.error(f"Error adding message to session {session_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def end_session(session_id):
    """End a session"""
    try:
        success = chat_storage.end_session(session_id)
        if success:
            return jsonify({'message': 'Session ended successfully'}), 200
        else:
            return jsonify({'error': 'Failed to end session'}), 500
    except Exception as e:
        logger.error(f"Error ending session {session_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sessions/<session_id>/activity', methods=['PUT'])
def update_session_activity(session_id):
    """Update session last activity timestamp"""
    try:
        success = chat_storage.update_session_activity(session_id)
        if success:
            return jsonify({'message': 'Session activity updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update session activity'}), 500
    except Exception as e:
        logger.error(f"Error updating session activity {session_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function to run the server"""
    port = int(os.getenv('DATA_SERVICE_PORT', 5002))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Data Service Server (Hardcoded Mode) on port {port}")
    logger.info(f"Available users: {list(HARDCODED_USERS.keys())}")
    logger.info(f"Available profiles: {list(HARDCODED_PROFILES.keys())}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()
