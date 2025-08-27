#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/auth_models.py
File: auth_models.py
Purpose: Pydantic models for authentication API endpoints
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Request and response models for authentication endpoints
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserRegisterRequest(BaseModel):
    """Request model for user registration."""
    email: EmailStr = Field(..., description="User email address", example="user@example.com")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)", example="SecurePass123!")
    first_name: str = Field(..., min_length=1, max_length=50, description="User first name", example="John")
    last_name: str = Field(..., min_length=1, max_length=50, description="User last name", example="Doe")
    
    @validator('email')
    def email_must_be_valid(cls, v):
        """Validate email format."""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v.lower()
    
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

class UserLoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr = Field(..., description="User email address", example="user@example.com")
    password: str = Field(..., description="User password", example="SecurePass123!")

class UserProfileResponse(BaseModel):
    """Response model for user profile."""
    user_id: str = Field(..., description="Unique user identifier", example="550e8400-e29b-41d4-a716-446655440000")
    email: EmailStr = Field(..., description="User email address", example="user@example.com")
    first_name: str = Field(..., description="User first name", example="John")
    last_name: str = Field(..., description="User last name", example="Doe")
    is_verified: bool = Field(..., description="Whether email is verified", example=False)
    is_active: bool = Field(..., description="Whether account is active", example=True)
    created_at: datetime = Field(..., description="Account creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AuthTokenResponse(BaseModel):
    """Response model for authentication tokens."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserProfileResponse = Field(..., description="User profile information")

class LoginSuccessResponse(BaseModel):
    """Response model for successful login."""
    success: bool = Field(True, description="Login success status")
    message: str = Field(..., description="Success message")
    data: AuthTokenResponse = Field(..., description="Authentication data")

class LoginErrorResponse(BaseModel):
    """Response model for login errors."""
    success: bool = Field(False, description="Login success status")
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for client handling")

class RegisterSuccessResponse(BaseModel):
    """Response model for successful registration."""
    success: bool = Field(True, description="Registration success status")
    message: str = Field(..., description="Success message")
    user_id: str = Field(..., description="New user ID")
    email: EmailStr = Field(..., description="User email address")

class RegisterErrorResponse(BaseModel):
    """Response model for registration errors."""
    success: bool = Field(False, description="Registration success status")
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for client handling")
    validation_errors: Optional[Dict[str, Any]] = Field(None, description="Field validation errors")

class PasswordResetRequest(BaseModel):
    """Request model for password reset."""
    email: EmailStr = Field(..., description="User email address", example="user@example.com")

class PasswordResetConfirmRequest(BaseModel):
    """Request model for password reset confirmation."""
    token: str = Field(..., description="Password reset token", example="abc123def456")
    new_password: str = Field(..., min_length=8, description="New password", example="NewSecurePass123!")

class EmailVerifyRequest(BaseModel):
    """Request model for email verification."""
    token: str = Field(..., description="Email verification token", example="verify123456")

class TokenRefreshRequest(BaseModel):
    """Request model for token refresh."""
    refresh_token: str = Field(..., description="Refresh token")

class TokenRefreshResponse(BaseModel):
    """Response model for token refresh."""
    access_token: str = Field(..., description="New access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")

class LogoutRequest(BaseModel):
    """Request model for logout."""
    session_id: Optional[str] = Field(None, description="Session ID to invalidate")

class LogoutResponse(BaseModel):
    """Response model for logout."""
    success: bool = Field(..., description="Logout success status")
    message: str = Field(..., description="Result message")

class UserUpdateRequest(BaseModel):
    """Request model for updating user profile."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User first name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User last name")
    email: Optional[EmailStr] = Field(None, description="User email address")

class PasswordChangeRequest(BaseModel):
    """Request model for changing password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    
    @validator('new_password')
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
    
    @validator('new_password')
    def passwords_must_differ(cls, v, values):
        """Validate that new password is different from current password."""
        if 'current_password' in values and v == values['current_password']:
            raise ValueError('New password must be different from current password')
        return v
    
    def json(self, *args, **kwargs):
        """Override json method to exclude passwords from serialization."""
        # Use exclude parameter to remove password fields from JSON
        kwargs.setdefault('exclude', set()).update({'current_password', 'new_password'})
        return super().json(*args, **kwargs)

class AuthConfigResponse(BaseModel):
    """Response model for authentication configuration."""
    password_min_length: int = Field(..., description="Minimum password length")
    password_requirements: Dict[str, Any] = Field(..., description="Password complexity requirements")
    session_timeout_minutes: int = Field(..., description="Session timeout duration")
    max_login_attempts: int = Field(..., description="Maximum login attempts before lockout")
    lockout_minutes: int = Field(..., description="Lockout duration in minutes")

class ErrorResponse(BaseModel):
    """Generic error response model."""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    error_code: Optional[str] = Field(None, description="Error code")

class SuccessResponse(BaseModel):
    """Generic success response model."""
    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")

class ValidationErrorDetail(BaseModel):
    """Detailed validation error information."""
    field: str = Field(..., description="Field name with error")
    message: str = Field(..., description="Validation error message")
    value: Optional[Any] = Field(None, description="Invalid value")

class ValidationErrorResponse(BaseModel):
    """Response model for validation errors."""
    success: bool = Field(False, description="Operation success status")
    message: str = Field("Validation failed", description="Error message")
    errors: List[ValidationErrorDetail] = Field(..., description="Validation errors")

# Common error codes
class ErrorCodes:
    """Standard error codes for authentication."""
    USER_ALREADY_EXISTS = "auth_user_exists"
    INVALID_CREDENTIALS = "auth_invalid_credentials"
    ACCOUNT_NOT_VERIFIED = "auth_account_not_verified"
    ACCOUNT_LOCKED = "auth_account_locked"
    INVALID_TOKEN = "auth_invalid_token"
    EXPIRED_TOKEN = "auth_expired_token"
    PASSWORD_TOO_WEAK = "auth_password_weak"
    RATE_LIMITED = "auth_rate_limited"
    USER_NOT_FOUND = "auth_user_not_found"
    SESSION_EXPIRED = "auth_session_expired"
    PERMISSION_DENIED = "auth_permission_denied"

# Common success messages
class SuccessMessages:
    """Standard success messages for authentication."""
    REGISTER_SUCCESS = "User registered successfully. Please verify your email."
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logout successful"
    PASSWORD_RESET_REQUESTED = "If the email exists, a reset link has been sent"
    PASSWORD_RESET_SUCCESS = "Password reset successfully"
    EMAIL_VERIFIED = "Email verified successfully"
    TOKEN_REFRESHED = "Token refreshed successfully"
    PROFILE_UPDATED = "Profile updated successfully"
    PASSWORD_CHANGED = "Password changed successfully"

# API documentation examples
class AuthExamples:
    """Example data for API documentation."""
    
    REGISTER_REQUEST = {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    LOGIN_REQUEST = {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    
    PASSWORD_RESET_REQUEST = {
        "email": "user@example.com"
    }
    
    PASSWORD_RESET_CONFIRM = {
        "token": "abc123def456",
        "new_password": "NewSecurePass123!"
    }
    
    EMAIL_VERIFY_REQUEST = {
        "token": "verify123456"
    }
    
    TOKEN_REFRESH_REQUEST = {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    
    USER_UPDATE_REQUEST = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com"
    }
    
    PASSWORD_CHANGE_REQUEST = {
        "current_password": "OldSecurePass123!",
        "new_password": "NewSecurePass123!"
    }
