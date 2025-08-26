#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/models/user.py
File: user.py
Purpose: User model and data structures for authentication
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: User model with JSON-based storage for authentication system
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field, validator
import json
from pathlib import Path

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserBase(BaseModel):
    """Base user model with common fields."""
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=50, description="User first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User last name")
    
    @validator('email')
    def email_must_be_lowercase(cls, v):
        """Ensure email is lowercase."""
        return v.lower()

class UserCreate(UserBase):
    """Model for user creation with password."""
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserLogin(BaseModel):
    """Model for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserUpdate(BaseModel):
    """Model for updating user profile."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None)

class PasswordResetRequest(BaseModel):
    """Model for password reset request."""
    email: EmailStr = Field(..., description="User email address")

class PasswordResetConfirm(BaseModel):
    """Model for password reset confirmation."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")

class UserProfile(BaseModel):
    """User profile information."""
    user_id: str = Field(..., description="Unique user identifier")
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    is_verified: bool = Field(False, description="Whether email is verified")
    is_active: bool = Field(True, description="Whether account is active")
    created_at: datetime = Field(default_factory=datetime.now, description="Account creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserSession(BaseModel):
    """User session information."""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    token: str = Field(..., description="JWT token")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation timestamp")
    expires_at: datetime = Field(..., description="Session expiration timestamp")
    user_agent: Optional[str] = Field(None, description="User agent string")
    ip_address: Optional[str] = Field(None, description="IP address")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PasswordResetToken(BaseModel):
    """Password reset token information."""
    token: str = Field(..., description="Reset token")
    user_id: str = Field(..., description="User identifier")
    email: EmailStr = Field(..., description="User email address")
    created_at: datetime = Field(default_factory=datetime.now, description="Token creation timestamp")
    expires_at: datetime = Field(..., description="Token expiration timestamp")
    used: bool = Field(False, description="Whether token has been used")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EmailVerificationToken(BaseModel):
    """Email verification token information."""
    token: str = Field(..., description="Verification token")
    user_id: str = Field(..., description="User identifier")
    email: EmailStr = Field(..., description="User email address")
    created_at: datetime = Field(default_factory=datetime.now, description="Token creation timestamp")
    expires_at: datetime = Field(..., description="Token expiration timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Utility functions for user management
def generate_user_id() -> str:
    """Generate a unique user ID."""
    return str(uuid.uuid4())

def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())

def generate_reset_token() -> str:
    """Generate a password reset token."""
    return str(uuid.uuid4())

def generate_verification_token() -> str:
    """Generate an email verification token."""
    return str(uuid.uuid4())

def calculate_token_expiry(minutes: int = 30) -> datetime:
    """Calculate token expiration time."""
    return datetime.now() + timedelta(minutes=minutes)

def calculate_session_expiry(hours: int = 24) -> datetime:
    """Calculate session expiration time."""
    return datetime.now() + timedelta(hours=hours)

# User storage structure
class UserStorage:
    """In-memory user storage structure."""
    users: Dict[str, UserProfile] = {}
    sessions: Dict[str, UserSession] = {}
    reset_tokens: Dict[str, PasswordResetToken] = {}
    verification_tokens: Dict[str, EmailVerificationToken] = {}
    
    def __init__(self):
        """Initialize user storage."""
        self.users = {}
        self.sessions = {}
        self.reset_tokens = {}
        self.verification_tokens = {}

# Global user storage instance
user_storage = UserStorage()
