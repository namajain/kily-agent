"""
Mock API Server - REST API for database operations
"""
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from database import get_db
from models import UserModel, ProfileModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'mock-api'
    })

# User endpoints
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = UserModel.get_user(user_id)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        username = data.get('username')
        email = data.get('email')
        
        if not all([user_id, username, email]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = UserModel.create_user(user_id, username, email)
        if success:
            return jsonify({'message': 'User created successfully'}), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        
        success = UserModel.update_user(user_id, username, email)
        if success:
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 500
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        success = UserModel.delete_user(user_id)
        if success:
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 500
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Profile endpoints
@app.route('/api/users/<user_id>/profiles', methods=['GET'])
def get_user_profiles(user_id):
    """Get all profiles for a user"""
    try:
        profiles = ProfileModel.get_user_profiles(user_id)
        return jsonify({
            'user_id': user_id,
            'profiles': profiles
        }), 200
    except Exception as e:
        logger.error(f"Error getting profiles for user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles/<profile_id>', methods=['GET'])
def get_profile(profile_id):
    """Get profile by ID"""
    try:
        profile = ProfileModel.get_profile(profile_id)
        if profile:
            return jsonify(profile), 200
        else:
            return jsonify({'error': 'Profile not found'}), 404
    except Exception as e:
        logger.error(f"Error getting profile {profile_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Create a new profile"""
    try:
        data = request.get_json()
        profile_id = data.get('profile_id')
        user_id = data.get('user_id')
        profile_name = data.get('profile_name')
        data_sources = data.get('data_sources', [])
        is_active = data.get('is_active', True)
        
        if not all([profile_id, user_id, profile_name]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = ProfileModel.create_profile(profile_id, user_id, profile_name, data_sources, is_active)
        if success:
            return jsonify({'message': 'Profile created successfully'}), 201
        else:
            return jsonify({'error': 'Failed to create profile'}), 500
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles/<profile_id>', methods=['PUT'])
def update_profile(profile_id):
    """Update profile"""
    try:
        data = request.get_json()
        profile_name = data.get('profile_name')
        data_sources = data.get('data_sources')
        is_active = data.get('is_active')
        
        success = ProfileModel.update_profile(profile_id, profile_name, data_sources, is_active)
        if success:
            return jsonify({'message': 'Profile updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update profile'}), 500
    except Exception as e:
        logger.error(f"Error updating profile {profile_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles/<profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Delete profile"""
    try:
        success = ProfileModel.delete_profile(profile_id)
        if success:
            return jsonify({'message': 'Profile deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete profile'}), 500
    except Exception as e:
        logger.error(f"Error deleting profile {profile_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function to run the server"""
    port = int(os.getenv('MOCK_API_PORT', 5002))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Mock API Server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()
