"""
Context Manager for MVP - Handles profile-based file downloads and caching
"""
import os
import json
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import logging
from ..api_client import api_client

logger = logging.getLogger(__name__)

class ContextManager:
    """
    Manages profile-based context file downloads and caching.
    Downloads files on first request for a profile (on-demand).
    """
    
    def __init__(self, base_path: str = "downloads"):
        self.base_path = base_path
        self._ensure_base_directory()
    
    def _ensure_base_directory(self):
        """Ensure base downloads directory exists"""
        os.makedirs(self.base_path, exist_ok=True)
    
    def get_context_for_profile(self, profile_id: str) -> Dict[str, pd.DataFrame]:
        """
        Get context files for a profile. Downloads if not already present.
        Called when first chat message comes for a profile.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        context_path = os.path.join(self.base_path, date_str, profile_id)
        
        # Check if already downloaded today
        if not os.path.exists(context_path):
            logger.info(f"Context not found for profile {profile_id}, downloading...")
            self._download_context_files(profile_id, context_path)
        else:
            logger.info(f"Using existing context for profile {profile_id}")
        
        return self._load_context_files(context_path)
    
    def _fetch_profile_from_db(self, profile_id: str) -> Optional[Dict]:
        """Fetch profile configuration from API"""
        try:
            profile = api_client.get_profile(profile_id)
            
            if profile:
                return profile
            else:
                logger.error(f"Profile {profile_id} not found or inactive")
                return None
                
        except Exception as e:
            logger.error(f"Failed to fetch profile {profile_id}: {e}")
            raise
    
    def _download_context_files(self, profile_id: str, context_path: str):
        """Download context files for a profile"""
        try:
            # Fetch profile configuration
            profile_config = self._fetch_profile_from_db(profile_id)
            if not profile_config:
                raise ValueError(f"Profile {profile_id} not found")
            
            # Create context directory
            os.makedirs(context_path, exist_ok=True)
            
            # Parse data sources
            data_sources = profile_config.get('data_sources', [])
            if isinstance(data_sources, str):
                data_sources = json.loads(data_sources)
            
            if not data_sources:
                logger.warning(f"No data sources configured for profile {profile_id}")
                return
            
            # Download each data source
            for source in data_sources:
                try:
                    url = source.get('url')
                    filename = source.get('filename', 'data.csv')
                    description = source.get('description', 'No description')
                    
                    if not url:
                        logger.warning(f"No URL provided for data source in profile {profile_id}")
                        continue
                    
                    logger.info(f"Downloading {filename} from {url}")
                    
                    # Handle local file URLs
                    if url.startswith('file://'):
                        local_path = url.replace('file://', '')
                        if not os.path.isabs(local_path):
                            # Make relative to project root
                            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                            local_path = os.path.join(project_root, local_path)
                        
                        if os.path.exists(local_path):
                            # Copy local file
                            import shutil
                            file_path = os.path.join(context_path, filename)
                            shutil.copy2(local_path, file_path)
                            logger.info(f"Copied local file {local_path} to {file_path}")
                        else:
                            raise FileNotFoundError(f"Local file not found: {local_path}")
                    else:
                        # Download from HTTP/HTTPS URL
                        response = requests.get(url, timeout=30)
                        response.raise_for_status()
                        
                        # Save file
                        file_path = os.path.join(context_path, filename)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                    
                    # Log successful download
                    self._log_download(profile_id, file_path, 'success', description)
                    
                    logger.info(f"Successfully downloaded {filename}")
                    
                except Exception as e:
                    error_msg = f"Failed to download {source.get('filename', 'unknown')}: {str(e)}"
                    logger.error(error_msg)
                    self._log_download(profile_id, source.get('url', ''), 'failed', error_msg)
                    raise
                    
        except Exception as e:
            logger.error(f"Failed to download context for profile {profile_id}: {e}")
            raise
    
    def _load_context_files(self, context_path: str) -> Dict[str, pd.DataFrame]:
        """Load context files into pandas DataFrames"""
        context_data = {}
        
        try:
            if not os.path.exists(context_path):
                logger.warning(f"Context path {context_path} does not exist")
                return context_data
            
            # Load all CSV files in the context directory
            for filename in os.listdir(context_path):
                if filename.endswith('.csv'):
                    file_path = os.path.join(context_path, filename)
                    try:
                        df = pd.read_csv(file_path)
                        context_data[filename] = df
                        logger.info(f"Loaded {filename} with shape {df.shape}")
                    except Exception as e:
                        logger.error(f"Failed to load {filename}: {e}")
            
            return context_data
            
        except Exception as e:
            logger.error(f"Failed to load context files from {context_path}: {e}")
            raise
    
    def _log_download(self, profile_id: str, file_path: str, status: str, message: str = ""):
        """Log download status (placeholder for future API endpoint)"""
        try:
            # TODO: Add API endpoint for logging download status
            logger.info(f"Download status for profile {profile_id}: {status} - {message}")
            
        except Exception as e:
            logger.error(f"Failed to log download status: {e}")
    
    def cleanup_old_contexts(self, days_to_keep: int = 7):
        """Clean up context files older than specified days"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Find old context directories
            for date_dir in os.listdir(self.base_path):
                try:
                    date_path = os.path.join(self.base_path, date_dir)
                    if os.path.isdir(date_path):
                        dir_date = datetime.strptime(date_dir, "%Y-%m-%d")
                        if dir_date < cutoff_date:
                            import shutil
                            shutil.rmtree(date_path)
                            logger.info(f"Cleaned up old context directory: {date_dir}")
                except ValueError:
                    # Skip non-date directories
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to cleanup old contexts: {e}")
    
    def get_profile_info(self, profile_id: str) -> Optional[Dict]:
        """Get profile information including data sources"""
        return self._fetch_profile_from_db(profile_id)
    
    def list_user_profiles(self, user_id: str) -> List[Dict]:
        """List all profiles for a user"""
        try:
            profiles = api_client.get_user_profiles(user_id)
            return profiles
            
        except Exception as e:
            logger.error(f"Failed to list profiles for user {user_id}: {e}")
            return [] 