"""
Data Service Server - REST API with hardcoded data (no PostgreSQL dependency)
"""
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

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

# Hardcoded data
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
