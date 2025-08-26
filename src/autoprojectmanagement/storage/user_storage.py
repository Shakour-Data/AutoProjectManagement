#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/storage/user_storage.py
File: user_storage.py
Purpose: JSON-based user storage service for authentication
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: JSON file-based storage for user authentication data
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import shutil
from ..models.user import (
    UserProfile, UserSession, PasswordResetToken, 
    EmailVerificationToken, user_storage
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONUserStorage:
    """JSON-based user storage service."""
    
    def __init__(self, storage_dir: str = "user_data"):
        """
        Initialize JSON user storage.
        
        Args:
            storage_dir: Directory path for storing JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.users_file = self.storage_dir / "users.json"
        self.sessions_file = self.storage_dir / "sessions.json"
        self.reset_tokens_file = self.storage_dir / "reset_tokens.json"
        self.verification_tokens_file = self.storage_dir / "verification_tokens.json"
        
        # Initialize empty files if they don't exist
        self._initialize_files()
        
        # Load data from files
        self.load_data()
    
    def _initialize_files(self):
        """Initialize empty JSON files if they don't exist."""
        files = [
            self.users_file,
            self.sessions_file,
            self.reset_tokens_file,
            self.verification_tokens_file
        ]
        
        for file_path in files:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=2)
                logger.info(f"Created empty storage file: {file_path}")
    
    def load_data(self):
        """Load data from JSON files into memory."""
        try:
            # Load users
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
                user_storage.users = {
                    user_id: UserProfile(**user_data) 
                    for user_id, user_data in users_data.items()
                }
            
            # Load sessions
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                sessions_data = json.load(f)
                user_storage.sessions = {
                    session_id: UserSession(**session_data)
                    for session_id, session_data in sessions_data.items()
                }
            
            # Load reset tokens
            with open(self.reset_tokens_file, 'r', encoding='utf-8') as f:
                reset_tokens_data = json.load(f)
                user_storage.reset_tokens = {
                    token: PasswordResetToken(**token_data)
                    for token, token_data in reset_tokens_data.items()
                }
            
            # Load verification tokens
            with open(self.verification_tokens_file, 'r', encoding='utf-8') as f:
                verification_tokens_data = json.load(f)
                user_storage.verification_tokens = {
                    token: EmailVerificationToken(**token_data)
                    for token, token_data in verification_tokens_data.items()
                }
            
            logger.info(f"Loaded {len(user_storage.users)} users from storage")
            logger.info(f"Loaded {len(user_storage.sessions)} sessions from storage")
            logger.info(f"Loaded {len(user_storage.reset_tokens)} reset tokens from storage")
            logger.info(f"Loaded {len(user_storage.verification_tokens)} verification tokens from storage")
            
        except Exception as e:
            logger.error(f"Error loading data from storage: {e}")
            # Initialize empty storage on error
            user_storage.users = {}
            user_storage.sessions = {}
            user_storage.reset_tokens = {}
            user_storage.verification_tokens = {}
    
    def save_data(self):
        """Save data from memory to JSON files."""
        try:
            # Save users
            users_data = {
                user_id: user.dict() 
                for user_id, user in user_storage.users.items()
            }
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, default=str)
            
            # Save sessions
            sessions_data = {
                session_id: session.dict()
                for session_id, session in user_storage.sessions.items()
            }
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(sessions_data, f, indent=2, default=str)
            
            # Save reset tokens
            reset_tokens_data = {
                token: token_data.dict()
                for token, token_data in user_storage.reset_tokens.items()
            }
            with open(self.reset_tokens_file, 'w', encoding='utf-8') as f:
                json.dump(reset_tokens_data, f, indent=2, default=str)
            
            # Save verification tokens
            verification_tokens_data = {
                token: token_data.dict()
                for token, token_data in user_storage.verification_tokens.items()
            }
            with open(self.verification_tokens_file, 'w', encoding='utf-8') as f:
                json.dump(verification_tokens_data, f, indent=2, default=str)
            
            logger.info("Data saved to storage files successfully")
            
        except Exception as e:
            logger.error(f"Error saving data to storage: {e}")
            raise
    
    def backup_data(self, backup_dir: str = "user_data_backups"):
        """Create a backup of all user data."""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"user_data_backup_{timestamp}"
            backup_dir_path = backup_path / backup_name
            
            # Copy all storage files
            shutil.copytree(self.storage_dir, backup_dir_path)
            
            logger.info(f"Backup created successfully: {backup_dir_path}")
            return str(backup_dir_path)
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None
    
    def restore_backup(self, backup_path: str):
        """Restore user data from backup."""
        try:
            backup_dir = Path(backup_path)
            if not backup_dir.exists():
                logger.error(f"Backup directory not found: {backup_path}")
                return False
            
            # Clear current storage
            for file_path in [
                self.users_file, self.sessions_file, 
                self.reset_tokens_file, self.verification_tokens_file
            ]:
                if file_path.exists():
                    file_path.unlink()
            
            # Copy backup files
            for file_name in ["users.json", "sessions.json", "reset_tokens.json", "verification_tokens.json"]:
                backup_file = backup_dir / file_name
                if backup_file.exists():
                    shutil.copy2(backup_file, self.storage_dir / file_name)
            
            # Reload data
            self.load_data()
            
            logger.info(f"Backup restored successfully from: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def cleanup_expired_data(self):
        """Clean up expired sessions and tokens."""
        try:
            current_time = datetime.now()
            cleaned_count = 0
            
            # Clean expired sessions
            expired_sessions = [
                session_id for session_id, session in user_storage.sessions.items()
                if session.expires_at < current_time
            ]
            for session_id in expired_sessions:
                del user_storage.sessions[session_id]
                cleaned_count += 1
            
            # Clean expired reset tokens
            expired_reset_tokens = [
                token for token, token_data in user_storage.reset_tokens.items()
                if token_data.expires_at < current_time or token_data.used
            ]
            for token in expired_reset_tokens:
                del user_storage.reset_tokens[token]
                cleaned_count += 1
            
            # Clean expired verification tokens
            expired_verification_tokens = [
                token for token, token_data in user_storage.verification_tokens.items()
                if token_data.expires_at < current_time
            ]
            for token in expired_verification_tokens:
                del user_storage.verification_tokens[token]
                cleaned_count += 1
            
            if cleaned_count > 0:
                self.save_data()
                logger.info(f"Cleaned up {cleaned_count} expired items")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up expired data: {e}")
            return 0
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        return {
            "total_users": len(user_storage.users),
            "total_sessions": len(user_storage.sessions),
            "total_reset_tokens": len(user_storage.reset_tokens),
            "total_verification_tokens": len(user_storage.verification_tokens),
            "active_sessions": sum(
                1 for session in user_storage.sessions.values()
                if session.expires_at > datetime.now()
            ),
            "storage_directory": str(self.storage_dir),
            "last_cleanup": datetime.now().isoformat()
        }
    
    def export_data(self, export_format: str = "json") -> Optional[str]:
        """Export all user data in specified format."""
        try:
            if export_format == "json":
                export_data = {
                    "users": {uid: user.dict() for uid, user in user_storage.users.items()},
                    "sessions": {sid: session.dict() for sid, session in user_storage.sessions.items()},
                    "reset_tokens": {token: token_data.dict() for token, token_data in user_storage.reset_tokens.items()},
                    "verification_tokens": {token: token_data.dict() for token, token_data in user_storage.verification_tokens.items()},
                    "export_timestamp": datetime.now().isoformat()
                }
                
                export_file = self.storage_dir / f"user_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, default=str)
                
                logger.info(f"Data exported to: {export_file}")
                return str(export_file)
            
            else:
                logger.error(f"Unsupported export format: {export_format}")
                return None
                
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return None

# Global storage instance
user_storage_service = JSONUserStorage()
