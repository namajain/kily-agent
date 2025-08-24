#!/usr/bin/env python3
"""
Test script for voice service functionality
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.voice_service import VoiceService
from backend.utils.logging_config import setup_service_logging

def test_voice_service():
    """Test voice service functionality"""
    logger = setup_service_logging('test_voice', log_level='INFO')
    
    try:
        # Initialize voice service
        logger.info("Initializing voice service...")
        voice_service = VoiceService()
        logger.info("Voice service initialized successfully")
        
        # Test getting available voices
        logger.info("Testing get_available_voices...")
        voices = voice_service.get_available_voices()
        logger.info(f"Found {len(voices)} available voices")
        
        if voices:
            # Show first few voices
            for i, voice in enumerate(voices[:3]):
                logger.info(f"Voice {i+1}: {voice['name']} (ID: {voice['voice_id']})")
        
        # Test text-to-speech
        logger.info("Testing text-to-speech...")
        test_text = "Hello, this is a test of the voice service."
        audio_data = voice_service.text_to_speech(test_text)
        logger.info(f"Generated audio data: {len(audio_data)} bytes")
        
        # Test base64 encoding
        logger.info("Testing base64 encoding...")
        base64_audio = voice_service.text_to_speech_base64(test_text)
        logger.info(f"Base64 audio length: {len(base64_audio)} characters")
        
        logger.info("All voice service tests passed!")
        
    except Exception as e:
        logger.error(f"Voice service test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voice_service()
