"""
Data models and operations for Mock API Server
"""
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from database import get_db

logger = logging.getLogger(__name__)

class UserModel:
    """User model and operations"""
    
    @staticmethod
    def get_user(user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            db = get_db()
            query = "SELECT user_id, username, email, created_at FROM users WHERE user_id = %s"
            result = db.execute_query(query, (user_id,))
            
            if result:
                user = dict(result[0])
                # Convert datetime to string for JSON serialization
                if user.get('created_at'):
                    user['created_at'] = user['created_at'].isoformat()
                return user
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            return None
    
    @staticmethod
    def create_user(user_id: str, username: str, email: str) -> bool:
        """Create a new user"""
        try:
            db = get_db()
            query = """
            INSERT INTO users (user_id, username, email, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
            """
            db.execute_query(query, (user_id, username, email, datetime.now()))
            return True
            
        except Exception as e:
            logger.error(f"Failed to create user {user_id}: {e}")
            return False
    
    @staticmethod
    def update_user(user_id: str, username: str = None, email: str = None) -> bool:
        """Update user information"""
        try:
            db = get_db()
            updates = []
            params = []
            
            if username:
                updates.append("username = %s")
                params.append(username)
            if email:
                updates.append("email = %s")
                params.append(email)
            
            if not updates:
                return False
            
            updates.append("updated_at = %s")
            params.append(datetime.now())
            params.append(user_id)
            
            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
            db.execute_query(query, params)
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user {user_id}: {e}")
            return False
    
    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Delete a user"""
        try:
            db = get_db()
            query = "DELETE FROM users WHERE user_id = %s"
            db.execute_query(query, (user_id,))
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete user {user_id}: {e}")
            return False

class ProfileModel:
    """Profile model and operations"""
    
    @staticmethod
    def get_user_profiles(user_id: str) -> List[Dict]:
        """Get all profiles for a user"""
        try:
            db = get_db()
            query = """
            SELECT profile_id, profile_name, user_id, data_sources, is_active, created_at
            FROM user_profiles 
            WHERE user_id = %s AND is_active = true
            ORDER BY created_at DESC
            """
            result = db.execute_query(query, (user_id,))
            
            profiles = []
            for row in result:
                profile = dict(row)
                # Parse data_sources JSON
                if profile.get('data_sources'):
                    if isinstance(profile['data_sources'], str):
                        try:
                            profile['data_sources'] = json.loads(profile['data_sources'])
                            logger.info(f"Successfully parsed data_sources for profile {profile['profile_id']}: {len(profile['data_sources'])} sources")
                        except Exception as e:
                            logger.error(f"Failed to parse data_sources for profile {profile['profile_id']}: {e}")
                            profile['data_sources'] = []
                    elif isinstance(profile['data_sources'], list):
                        logger.info(f"Data sources already a list for profile {profile['profile_id']}: {len(profile['data_sources'])} sources")
                    else:
                        logger.warning(f"Unexpected data_sources type for profile {profile['profile_id']}: {type(profile['data_sources'])}")
                        profile['data_sources'] = []
                else:
                    profile['data_sources'] = []
                
                # Convert datetime to string
                if profile.get('created_at'):
                    profile['created_at'] = profile['created_at'].isoformat()
                
                profiles.append(profile)
            
            return profiles
            
        except Exception as e:
            logger.error(f"Failed to get profiles for user {user_id}: {e}")
            return []
    
    @staticmethod
    def get_profile(profile_id: str) -> Optional[Dict]:
        """Get profile by ID"""
        try:
            db = get_db()
            query = """
            SELECT profile_id, profile_name, user_id, data_sources, is_active, created_at
            FROM user_profiles 
            WHERE profile_id = %s
            """
            result = db.execute_query(query, (profile_id,))
            
            if result:
                profile = dict(result[0])
                # Parse data_sources JSON
                if profile.get('data_sources'):
                    if isinstance(profile['data_sources'], str):
                        try:
                            profile['data_sources'] = json.loads(profile['data_sources'])
                        except Exception as e:
                            logger.error(f"Failed to parse data_sources for profile {profile['profile_id']}: {e}")
                            profile['data_sources'] = []
                    elif isinstance(profile['data_sources'], list):
                        pass  # Already a list
                    else:
                        profile['data_sources'] = []
                else:
                    profile['data_sources'] = []
                
                # Convert datetime to string
                if profile.get('created_at'):
                    profile['created_at'] = profile['created_at'].isoformat()
                
                return profile
            return None
            
        except Exception as e:
            logger.error(f"Failed to get profile {profile_id}: {e}")
            return None
    
    @staticmethod
    def create_profile(profile_id: str, user_id: str, profile_name: str, 
                      data_sources: List[Dict], is_active: bool = True) -> bool:
        """Create a new profile"""
        try:
            db = get_db()
            query = """
            INSERT INTO user_profiles (profile_id, user_id, profile_name, data_sources, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (profile_id) DO NOTHING
            """
            db.execute_query(query, (
                profile_id, user_id, profile_name, 
                json.dumps(data_sources), is_active, datetime.now()
            ))
            return True
            
        except Exception as e:
            logger.error(f"Failed to create profile {profile_id}: {e}")
            return False
    
    @staticmethod
    def update_profile(profile_id: str, profile_name: str = None, 
                      data_sources: List[Dict] = None, is_active: bool = None) -> bool:
        """Update profile information"""
        try:
            db = get_db()
            updates = []
            params = []
            
            if profile_name:
                updates.append("profile_name = %s")
                params.append(profile_name)
            if data_sources is not None:
                updates.append("data_sources = %s")
                params.append(json.dumps(data_sources))
            if is_active is not None:
                updates.append("is_active = %s")
                params.append(is_active)
            
            if not updates:
                return False
            
            updates.append("updated_at = %s")
            params.append(datetime.now())
            params.append(profile_id)
            
            query = f"UPDATE user_profiles SET {', '.join(updates)} WHERE profile_id = %s"
            db.execute_query(query, params)
            return True
            
        except Exception as e:
            logger.error(f"Failed to update profile {profile_id}: {e}")
            return False
    
    @staticmethod
    def delete_profile(profile_id: str) -> bool:
        """Delete a profile"""
        try:
            db = get_db()
            query = "DELETE FROM user_profiles WHERE profile_id = %s"
            db.execute_query(query, (profile_id,))
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete profile {profile_id}: {e}")
            return False
