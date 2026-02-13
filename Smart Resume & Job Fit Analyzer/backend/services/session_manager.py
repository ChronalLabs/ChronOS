import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

from api.schemas import SessionData

logger = logging.getLogger(__name__)

class FileSessionManager:
    """
    Manages session persistence using file system storage.
    Replaces in-memory session storage to persist data across server restarts.
    """
    
    def __init__(self, storage_dir: str = "sessions"):
        self.storage_dir = Path(os.path.dirname(os.path.dirname(__file__))) / storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Session storage initialized at: {self.storage_dir}")

    def save_session(self, session: SessionData) -> None:
        """Save session to file."""
        try:
            file_path = self.storage_dir / f"{session.session_id}.json"
            
            # Update timestamp
            session.updated_at = datetime.now()
            
            # Serialize using Pydantic V1 json() method
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(session.json(indent=2))
                
            logger.debug(f"Saved session {session.session_id}")
        except Exception as e:
            logger.error(f"Failed to save session {session.session_id}: {str(e)}")
            raise

    def get_session(self, session_id: str) -> Optional[SessionData]:
        """Load session from file."""
        try:
            file_path = self.storage_dir / f"{session_id}.json"
            
            if not file_path.exists():
                logger.warning(f"Session file not found: {file_path}")
                return None
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
                
            # Parse using Pydantic V1
            session = SessionData.parse_raw(data)
            return session
        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {str(e)}")
            return None

    def delete_session(self, session_id: str) -> bool:
        """Delete session file."""
        try:
            file_path = self.storage_dir / f"{session_id}.json"
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {str(e)}")
            return False

    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """Remove sessions older than max_age."""
        count = 0
        now = datetime.now()
        cutoff = now - timedelta(hours=max_age_hours)
        
        try:
            for file_path in self.storage_dir.glob("*.json"):
                try:
                    # Check file modification time
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff:
                        file_path.unlink()
                        count += 1
                except Exception as e:
                    logger.warning(f"Error cleaning up {file_path}: {e}")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            
        if count > 0:
            logger.info(f"Cleaned up {count} expired sessions")
        return count

# Global instance
session_manager = FileSessionManager()
