"""
Conversation Logger for AI Interactions
Separate logging for user messages, AI responses, STT output, and TTS requests
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class ConversationLogger:
    """
    Dedicated logger for AI conversation interactions
    """
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize conversation logger"""
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Create conversation log file
        self.conversation_log_file = os.path.join(log_dir, "conversations.log")
        
        # Setup logger
        self.logger = logging.getLogger("conversations")
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler for conversations
        file_handler = logging.FileHandler(self.conversation_log_file, mode='a')
        file_handler.setLevel(logging.INFO)
        
        # Formatter for conversation logs
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
    def log_user_message(self, session_id: str, user_id: str, message: str, 
                        input_method: str = "text", stt_output: Optional[str] = None):
        """Log user message"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "user_id": user_id,
            "type": "user_message",
            "input_method": input_method,
            "message": message,
            "stt_output": stt_output
        }
        
        self.logger.info(f"USER MESSAGE - Session: {session_id} - User: {user_id} - Method: {input_method}")
        if stt_output:
            self.logger.info(f"STT OUTPUT: {stt_output}")
        
        # Log message in chunks to avoid line wrapping
        if len(message) > 100:
            self.logger.info(f"MESSAGE (truncated): {message[:100]}...")
            self.logger.info(f"MESSAGE (full): {message}")
        else:
            self.logger.info(f"MESSAGE: {message}")
        
        # Also write to JSON file for structured logging
        self._write_json_log(log_entry)
    
    def log_ai_response(self, session_id: str, user_id: str, response: str, 
                       processing_time: Optional[float] = None):
        """Log AI response"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "user_id": user_id,
            "type": "ai_response",
            "response": response,
            "processing_time": processing_time
        }
        
        self.logger.info(f"AI RESPONSE - Session: {session_id} - User: {user_id}")
        if processing_time:
            self.logger.info(f"Processing time: {processing_time:.2f}s")
        
        # Log response in chunks to avoid line wrapping
        if len(response) > 200:
            self.logger.info(f"RESPONSE (truncated): {response[:200]}...")
            self.logger.info(f"RESPONSE (full): {response}")
        else:
            self.logger.info(f"RESPONSE: {response}")
        
        # Also write to JSON file for structured logging
        self._write_json_log(log_entry)
    
    def log_voice_request(self, session_id: str, user_id: str, text: str, 
                         voice_id: str, audio_length: Optional[int] = None):
        """Log voice generation request (without the actual base64 audio)"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "user_id": user_id,
            "type": "voice_request",
            "text": text,
            "voice_id": voice_id,
            "audio_length_bytes": audio_length
        }
        
        self.logger.info(f"VOICE REQUEST - Session: {session_id} - Voice: {voice_id}")
        
        # Log original text and cleaned text for TTS
        if len(text) > 100:
            self.logger.info(f"ORIGINAL TEXT (truncated): {text[:100]}...")
            self.logger.info(f"ORIGINAL TEXT (full): {text}")
        else:
            self.logger.info(f"ORIGINAL TEXT: {text}")
        
        # Import and clean the text to show what was sent to TTS
        try:
            from backend.utils.voice_service import VoiceService
            voice_service = VoiceService.__new__(VoiceService)
            cleaned_text = voice_service._clean_markdown_for_tts(text)
            
            if len(cleaned_text) > 100:
                self.logger.info(f"CLEANED TEXT (truncated): {cleaned_text[:100]}...")
                self.logger.info(f"CLEANED TEXT (full): {cleaned_text}")
            else:
                self.logger.info(f"CLEANED TEXT: {cleaned_text}")
        except Exception as e:
            self.logger.warning(f"Could not show cleaned text: {e}")
            
        if audio_length:
            self.logger.info(f"Audio generated: {audio_length} bytes")
        
        # Also write to JSON file for structured logging
        self._write_json_log(log_entry)
    
    def log_error(self, session_id: str, user_id: str, error_type: str, 
                  error_message: str, context: Optional[Dict[str, Any]] = None):
        """Log errors in conversations"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "user_id": user_id,
            "type": "error",
            "error_type": error_type,
            "error_message": error_message,
            "context": context
        }
        
        self.logger.error(f"CONVERSATION ERROR - Session: {session_id} - Type: {error_type}")
        self.logger.error(f"Error: {error_message}")
        if context:
            self.logger.error(f"Context: {context}")
        
        # Also write to JSON file for structured logging
        self._write_json_log(log_entry)
    
    def log_session_event(self, session_id: str, user_id: str, event_type: str, 
                         details: Optional[Dict[str, Any]] = None):
        """Log session events (start, end, etc.)"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "user_id": user_id,
            "type": "session_event",
            "event_type": event_type,
            "details": details
        }
        
        self.logger.info(f"SESSION EVENT - Session: {session_id} - Event: {event_type}")
        if details:
            self.logger.info(f"Details: {details}")
        
        # Also write to JSON file for structured logging
        self._write_json_log(log_entry)
    
    def _write_json_log(self, log_entry: Dict[str, Any]):
        """Write structured log entry to JSON file"""
        json_log_file = os.path.join(self.log_dir, "conversations.json")
        try:
            # Read existing logs
            existing_logs = []
            if os.path.exists(json_log_file):
                with open(json_log_file, 'r') as f:
                    try:
                        existing_logs = json.load(f)
                    except json.JSONDecodeError:
                        existing_logs = []
            
            # Add new log entry
            existing_logs.append(log_entry)
            
            # Write back to file
            with open(json_log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
                
        except Exception as e:
            # Fallback to simple logging if JSON writing fails
            self.logger.error(f"Failed to write JSON log: {e}")
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get conversation summary for a session"""
        json_log_file = os.path.join(self.log_dir, "conversations.json")
        if not os.path.exists(json_log_file):
            return {"session_id": session_id, "messages": [], "error": "No conversation log found"}
        
        try:
            with open(json_log_file, 'r') as f:
                logs = json.load(f)
            
            session_logs = [log for log in logs if log.get("session_id") == session_id]
            
            return {
                "session_id": session_id,
                "total_messages": len(session_logs),
                "user_messages": len([log for log in session_logs if log.get("type") == "user_message"]),
                "ai_responses": len([log for log in session_logs if log.get("type") == "ai_response"]),
                "voice_requests": len([log for log in session_logs if log.get("type") == "voice_request"]),
                "errors": len([log for log in session_logs if log.get("type") == "error"]),
                "messages": session_logs
            }
            
        except Exception as e:
            return {"session_id": session_id, "error": f"Failed to read conversation log: {e}"}
