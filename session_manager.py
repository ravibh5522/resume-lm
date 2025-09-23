import json
import redis
from typing import Optional, Dict, Any, Union
from datetime import datetime, timedelta
import uuid
from models import SessionData, ResumeData, ChatMessage
import os
from dotenv import load_dotenv

load_dotenv()

class SessionManager:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client: Optional[redis.Redis] = None
        self._memory_store: Dict[str, SessionData] = {}
        
        try:
            # Test Redis connection
            test_client = redis.from_url(redis_url, decode_responses=True)
            test_client.ping()  # type: ignore
            self.redis_client = test_client
        except (redis.ConnectionError, redis.TimeoutError, Exception):
            # Fallback to in-memory storage if Redis is not available
            self.redis_client = None
        
        self.session_timeout = timedelta(hours=2)
    
    def create_session(self) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        session_data = SessionData(session_id=session_id)
        
        if self.redis_client:
            self.redis_client.setex(
                f"session:{session_id}",
                int(self.session_timeout.total_seconds()),
                session_data.model_dump_json()
            )
        else:
            self._memory_store[session_id] = session_data
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session data by session ID"""
        if self.redis_client:
            data = self.redis_client.get(f"session:{session_id}")
            if data and isinstance(data, str):
                return SessionData.model_validate_json(data)
        else:
            return self._memory_store.get(session_id)
        
        return None
    
    def update_session(self, session_id: str, session_data: SessionData) -> bool:
        """Update session data"""
        session_data.last_updated = datetime.now()
        
        if self.redis_client:
            result = self.redis_client.setex(
                f"session:{session_id}",
                int(self.session_timeout.total_seconds()),
                session_data.model_dump_json()
            )
            return bool(result)
        else:
            self._memory_store[session_id] = session_data
            return True
    
    def add_chat_message(self, session_id: str, message: ChatMessage) -> bool:
        """Add a chat message to session"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.chat_history.append(message)
        return self.update_session(session_id, session)
    
    def update_resume_data(self, session_id: str, resume_data: ResumeData) -> bool:
        """Update resume data in session"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.user_data = resume_data
        return self.update_session(session_id, session)
    
    def update_resume_markdown(self, session_id: str, markdown: str) -> bool:
        """Update resume markdown in session"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.resume_markdown = markdown
        return self.update_session(session_id, session)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if self.redis_client:
            return bool(self.redis_client.delete(f"session:{session_id}"))
        else:
            return self._memory_store.pop(session_id, None) is not None
    
    def extend_session(self, session_id: str) -> bool:
        """Extend session timeout"""
        if self.redis_client:
            return bool(self.redis_client.expire(f"session:{session_id}", int(self.session_timeout.total_seconds())))
        else:
            # For in-memory storage, sessions don't expire automatically
            return session_id in self._memory_store
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions (for in-memory storage)"""
        if not self.redis_client:
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session_data in self._memory_store.items():
                if current_time - session_data.last_updated > self.session_timeout:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self._memory_store[session_id]