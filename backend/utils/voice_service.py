"""
Voice Service for ElevenLabs Integration
Handles Text-to-Speech (TTS) and Speech-to-Text (STT) capabilities
"""
import os
import base64
import tempfile
import logging
import re
from typing import Optional, Dict, Any
import requests
from elevenlabs import text_to_speech, voices, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from elevenlabs import history

logger = logging.getLogger(__name__)

class VoiceService:
    """
    Voice service for ElevenLabs integration providing TTS and STT capabilities
    """
    
    def __init__(self):
        """Initialize voice service with ElevenLabs API key"""
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable is required")
        
        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=self.api_key)
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
        
        # Default voice settings
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        self.default_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.5,
            style=0.0,
            use_speaker_boost=True
        )
        
        logger.debug("Voice service initialized successfully")
    
    def _clean_markdown_for_tts(self, text: str) -> str:
        """
        Clean markdown formatting from text to make it suitable for TTS
        
        Args:
            text: Text with markdown formatting
            
        Returns:
            Clean text without markdown formatting
        """
        # Remove markdown headers (# ## ### etc.)
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # Remove bold formatting (**text** or __text__)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'__(.*?)__', r'\1', text)
        
        # Remove italic formatting (*text* or _text_)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text)
        
        # Remove code blocks (```code```) first
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        
        # Remove inline code formatting (`code`)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove links [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # Remove horizontal rules (---, ___, ***)
        text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace and newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double newlines
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single space
        text = text.strip()
        
        return text
    
    def text_to_speech(self, text: str, voice_id: Optional[str] = None,
                      settings: Optional[VoiceSettings] = None) -> bytes:
        """
        Convert text to speech using ElevenLabs TTS
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID (optional)
            settings: Voice settings (optional)
            
        Returns:
            Audio data as bytes
        """
        try:
            voice_id = voice_id or self.default_voice_id
            settings = settings or self.default_settings
            
            # Clean markdown formatting before TTS
            cleaned_text = self._clean_markdown_for_tts(text)
            logger.debug(f"Generating speech for text: {cleaned_text[:50]}...")
            
            # Generate audio using ElevenLabs client
            audio = self.client.text_to_speech.convert(
                text=cleaned_text,
                voice_id=voice_id,
                model_id="eleven_monolingual_v1",
                voice_settings=settings
            )
            
            # Convert generator to bytes if needed
            if hasattr(audio, '__iter__') and not isinstance(audio, (bytes, str)):
                audio = b''.join(audio)
            
            logger.debug("Speech generation completed successfully")
            return audio
            
        except Exception as e:
            logger.error(f"Text-to-speech failed: {e}")
            raise
    
    def text_to_speech_base64(self, text: str, voice_id: Optional[str] = None,
                             settings: Optional[VoiceSettings] = None) -> str:
        """
        Convert text to speech and return as base64 encoded string
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID (optional)
            settings: Voice settings (optional)
            
        Returns:
            Base64 encoded audio data
        """
        audio_data = self.text_to_speech(text, voice_id, settings)
        return base64.b64encode(audio_data).decode('utf-8')
    
    def save_audio_file(self, audio_data: bytes, filename: str) -> str:
        """
        Save audio data to a temporary file
        
        Args:
            audio_data: Audio data as bytes
            filename: Name for the file
            
        Returns:
            Path to the saved file
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            logger.info(f"Audio saved to temporary file: {temp_file_path}")
            return temp_file_path
            
        except Exception as e:
            logger.error(f"Failed to save audio file: {e}")
            raise
    
    def get_available_voices(self) -> list:
        """
        Get list of available ElevenLabs voices
        
        Returns:
            List of voice objects
        """
        try:
            available_voices = self.client.voices.get_all()
            return [
                {
                    'voice_id': voice.voice_id,
                    'name': voice.name,
                    'category': voice.category,
                    'description': voice.description
                }
                for voice in available_voices.voices
            ]
        except Exception as e:
            logger.error(f"Failed to get available voices: {e}")
            return []
    
    def get_voice_history(self, limit: int = 10) -> list:
        """
        Get recent voice generation history
        
        Args:
            limit: Number of history items to return
            
        Returns:
            List of history items
        """
        try:
            # Use the new history API
            history_items = history.from_api(self.client)
            return [
                {
                    'history_id': item.history_id,
                    'request_id': item.request_id,
                    'voice_id': item.voice_id,
                    'voice_name': item.voice_name,
                    'text': item.text,
                    'date_unix': item.date_unix,
                    'character_count_change_from': item.character_count_change_from,
                    'character_count_change_to': item.character_count_change_to,
                    'content_type': item.content_type,
                    'state': item.state
                }
                for item in history_items[:limit]
            ]
        except Exception as e:
            logger.error(f"Failed to get voice history: {e}")
            return []
    
    def speech_to_text(self, audio_data: bytes) -> str:
        """
        Convert speech to text using ElevenLabs STT
        
        Args:
            audio_data: Audio data as bytes
            
        Returns:
            Transcribed text
        """
        try:
            logger.debug("Converting speech to text using ElevenLabs STT...")
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # Convert audio to text using ElevenLabs STT
                with open(temp_file_path, 'rb') as audio_file:
                    result = self.client.speech_to_text.convert(
                        file=audio_file,
                        model_id="scribe_v1"
                    )
                
                transcribed_text = result.text.strip()
                logger.debug(f"Speech-to-text successful: '{transcribed_text}'")
                return transcribed_text
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            logger.error(f"Speech-to-text failed: {e}")
            raise
    
    def validate_voice_id(self, voice_id: str) -> bool:
        """
        Validate if a voice ID exists
        
        Args:
            voice_id: Voice ID to validate
            
        Returns:
            True if voice exists, False otherwise
        """
        try:
            available_voices = self.get_available_voices()
            return any(voice['voice_id'] == voice_id for voice in available_voices)
        except Exception as e:
            logger.error(f"Failed to validate voice ID: {e}")
            return False
