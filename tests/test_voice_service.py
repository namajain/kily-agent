"""
Test cases for Voice Service functionality
"""
import pytest
import os
import base64
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.voice_service import VoiceService


class TestVoiceService:
    """Test cases for VoiceService class"""
    
    @pytest.fixture
    def mock_env(self):
        """Mock environment with ElevenLabs API key"""
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test-api-key'}):
            yield
    
    @pytest.fixture
    def voice_service(self, mock_env):
        """Create VoiceService instance with mocked dependencies"""
        with patch('backend.utils.voice_service.set_api_key'), \
             patch('backend.utils.voice_service.generate'), \
             patch('backend.utils.voice_service.voices'), \
             patch('backend.utils.voice_service.History'):
            return VoiceService()
    
    def test_initialization_success(self, mock_env):
        """Test successful VoiceService initialization"""
        with patch('backend.utils.voice_service.set_api_key'), \
             patch('backend.utils.voice_service.generate'), \
             patch('backend.utils.voice_service.voices'), \
             patch('backend.utils.voice_service.History'):
            
            service = VoiceService()
            assert service.api_key == 'test-api-key'
            assert service.default_voice_id == "21m00Tcm4TlvDq8ikWAM"
    
    def test_initialization_missing_api_key(self):
        """Test VoiceService initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ELEVENLABS_API_KEY environment variable is required"):
                VoiceService()
    
    def test_text_to_speech_base64(self, voice_service):
        """Test text-to-speech with base64 encoding"""
        mock_audio = b"mock_audio_data"
        voice_service.text_to_speech = Mock(return_value=mock_audio)
        
        result = voice_service.text_to_speech_base64("Hello world")
        expected_base64 = base64.b64encode(mock_audio).decode('utf-8')
        assert result == expected_base64
    
    def test_get_available_voices_success(self, voice_service):
        """Test getting available voices"""
        mock_voices = [
            {'voice_id': 'voice1', 'name': 'Voice 1', 'category': 'test', 'description': 'Test voice 1'},
            {'voice_id': 'voice2', 'name': 'Voice 2', 'category': 'test', 'description': 'Test voice 2'}
        ]
        voice_service.get_available_voices = Mock(return_value=mock_voices)
        
        result = voice_service.get_available_voices()
        assert len(result) == 2
        assert result[0]['voice_id'] == 'voice1'
    
    def test_validate_voice_id_true(self, voice_service):
        """Test voice ID validation with valid ID"""
        voice_service.get_available_voices = Mock(return_value=[
            {'voice_id': 'voice1', 'name': 'Voice 1'},
            {'voice_id': 'voice2', 'name': 'Voice 2'}
        ])
        
        result = voice_service.validate_voice_id('voice1')
        assert result is True
    
    def test_validate_voice_id_false(self, voice_service):
        """Test voice ID validation with invalid ID"""
        voice_service.get_available_voices = Mock(return_value=[
            {'voice_id': 'voice1', 'name': 'Voice 1'},
            {'voice_id': 'voice2', 'name': 'Voice 2'}
        ])
        
        result = voice_service.validate_voice_id('invalid_voice')
        assert result is False


class TestVoiceServiceErrorHandling:
    """Test error handling in VoiceService"""
    
    @pytest.fixture
    def voice_service_with_errors(self, mock_env):
        """Create VoiceService with error-prone dependencies"""
        with patch('backend.utils.voice_service.set_api_key'), \
             patch('backend.utils.voice_service.generate', side_effect=Exception("API Error")), \
             patch('backend.utils.voice_service.voices', side_effect=Exception("API Error")), \
             patch('backend.utils.voice_service.History'):
            return VoiceService()
    
    def test_get_available_voices_api_error(self, voice_service_with_errors):
        """Test getting voices when API call fails"""
        result = voice_service_with_errors.get_available_voices()
        assert result == []
    
    def test_get_voice_history_api_error(self, voice_service_with_errors):
        """Test getting history when API call fails"""
        result = voice_service_with_errors.get_voice_history()
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__])
