"""
Test cases for Backend Voice Integration
"""
import pytest
import base64
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.server import QnABackend


class TestBackendVoiceIntegration:
    """Test cases for voice integration in backend server"""
    
    @pytest.fixture
    def mock_env(self):
        """Mock environment with required API keys"""
        with patch.dict(os.environ, {
            'ELEVENLABS_API_KEY': 'test-elevenlabs-key',
            'OPENAI_API_KEY': 'test-openai-key'
        }):
            yield
    
    def test_voice_service_initialization_success(self, mock_env):
        """Test successful voice service initialization"""
        with patch('backend.server.ContextManager'), \
             patch('backend.server.SessionManager'), \
             patch('backend.server.QnAAgent'), \
             patch('backend.server.VoiceService') as mock_voice_service:
            
            backend = QnABackend()
            assert backend.voice_service is not None
            mock_voice_service.assert_called_once()
    
    def test_voice_service_initialization_failure(self, mock_env):
        """Test voice service initialization failure"""
        with patch('backend.server.ContextManager'), \
             patch('backend.server.SessionManager'), \
             patch('backend.server.QnAAgent'), \
             patch('backend.server.VoiceService', side_effect=Exception("Voice service failed")):
            
            backend = QnABackend()
            assert backend.voice_service is None


if __name__ == "__main__":
    pytest.main([__file__])
