"""
Basic tests for MVP components
"""
import unittest
import os
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import DatabaseConfig, DatabaseConnection
from managers.context_manager import ContextManager
from managers.session_manager import SessionManager
from agents.qna_agent import QnAAgent

class TestDatabaseConfig(unittest.TestCase):
    """Test database configuration"""
    
    def test_config_creation(self):
        """Test database config creation"""
        config = DatabaseConfig()
        self.assertIsNotNone(config.host)
        self.assertIsNotNone(config.port)
        self.assertIsNotNone(config.database)
        self.assertIsNotNone(config.user)
        self.assertIsNotNone(config.password)
    
    def test_connection_string(self):
        """Test connection string generation"""
        config = DatabaseConfig()
        conn_str = config.get_connection_string()
        self.assertIn('postgresql://', conn_str)
        self.assertIn(config.user, conn_str)
        self.assertIn(config.database, conn_str)

class TestContextManager(unittest.TestCase):
    """Test context manager functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.context_manager = ContextManager(base_path=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_directory_creation(self):
        """Test base directory creation"""
        self.assertTrue(os.path.exists(self.temp_dir))
    
    def test_profile_fetch(self):
        """Test profile fetching (mock)"""
        # This would require a mock database connection
        pass

class TestSessionManager(unittest.TestCase):
    """Test session manager functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.context_manager = ContextManager()
        self.session_manager = SessionManager(self.context_manager)
    
    def test_session_creation(self):
        """Test session creation"""
        session_id = self.session_manager.create_session("test_user", "test_profile")
        self.assertIsNotNone(session_id)
        self.assertIsInstance(session_id, str)
    
    def test_session_retrieval(self):
        """Test session retrieval"""
        session_id = self.session_manager.create_session("test_user", "test_profile")
        session = self.session_manager.get_session(session_id)
        self.assertIsNotNone(session)
        self.assertEqual(session['user_id'], "test_user")
        self.assertEqual(session['profile_id'], "test_profile")

class TestQnAAgent(unittest.TestCase):
    """Test QnA agent functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.context_manager = ContextManager()
        self.qna_agent = QnAAgent(self.context_manager)
    
    def test_query_validation(self):
        """Test query validation"""
        # Valid query
        self.assertTrue(self.qna_agent.validate_query("Show me a summary of the data"))
        
        # Invalid query
        self.assertFalse(self.qna_agent.validate_query(""))
        self.assertFalse(self.qna_agent.validate_query("exec('rm -rf /')"))
    
    def test_context_summary(self):
        """Test context summary generation"""
        # Mock context data
        import pandas as pd
        context_data = {
            'test.csv': pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        }
        
        summary = self.qna_agent.get_basic_summary(context_data)
        self.assertIsNotNone(summary)
        self.assertIn('test.csv', summary)

if __name__ == '__main__':
    unittest.main() 