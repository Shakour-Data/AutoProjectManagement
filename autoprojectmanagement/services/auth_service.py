#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/auth_service.py
File: auth_service.py
Purpose: Authentication service for user management
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Core authentication service with user registration, login, and session management
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Tuple, List
from pathlib import Path

from ..models.user import (
    UserCreate, UserLogin, UserUpdate, PasswordResetRequest,
    PasswordResetConfirm, UserProfile, UserSession,
    PasswordResetToken, EmailVerificationToken,
    generate_user_id, generate_session_id, generate_reset_token,
    generate_verification_token, calculate_token_expiry,
    calculate_session_expiry, user_storage
)
from ..utils.security import (
    password_hasher, token_manager, security_utils,
    SecurityConfig
)
from ..storage.user_storage import user_storage_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthService:
    """Authentication service for user management."""
    
    def __init__(self):
        """Initialize authentication service."""
        self.login_attempts: Dict[str, Dict[str, Any]] = {}
    
    def register_user(self, user_data: UserCreate) -> Tuple[bool, str, Optional[UserProfile]]:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            Tuple of (success, message, user_profile)
        """
        try:
            # Check if user already exists
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user:
                return False, "User with this email already exists", None
            
            # Validate password strength
            password_analysis = password_hasher.is_password_strong(user_data.password)
            if password_analysis["strength"] == "weak":
                return False, "Password is too weak", None
            
            # Hash password
            hashed_password = password_hasher.hash_password(user_data.password)
            
            # Create user profile
            user_id = generate_user_id()
            user_profile = UserProfile(
                user_id=user_id,
                email=user_data.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                is_verified=False,
                is_active=True,
                created_at=datetime.now()
            )
            
            # Store user data (password will be stored separately in secure storage)
            user_storage.users[user_id] = user_profile
            
            # Store password hash (in real implementation, this would be in secure storage)
            # For now, we'll store it in the user profile for demonstration
            # In production, this should be stored separately with proper security
            setattr(user_profile, '_password_hash', hashed_password)
            
            # Generate email verification token
            verification_token = self._create_verification_token(user_id, user_data.email)
            
            # Save data to storage
            user_storage_service.save_data()
            
            logger.info(f"User registered successfully: {user_data.email}")
            return True, "User registered successfully. Please verify your email.", user_profile
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return False, f"Registration failed: {str(e)}", None
    
    def login_user(self, login_data: UserLogin, user_agent: Optional[str] = None, 
                  ip_address: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Authenticate user and create session.
        
        Args:
            login_data: User login credentials
            user_agent: User agent string
            ip_address: IP address
            
        Returns:
            Tuple of (success, message, auth_data)
        """
        try:
            # Check rate limiting
            if self._is_rate_limited(login_data.email):
                return False, "Too many login attempts. Please try again later.", None
            
            # Find user by email
            user = self.get_user_by_email(login_data.email)
            if not user or not user.is_active:
                self._record_login_attempt(login_data.email, False)
                return False, "Invalid credentials", None
            
            # Verify password (in real implementation, this would check secure storage)
            # For demonstration, we're storing password hash in the user object
            if not hasattr(user, '_password_hash') or not password_hasher.verify_password(
                login_data.password, getattr(user, '_password_hash')
            ):
                self._record_login_attempt(login_data.email, False)
                return False, "Invalid credentials", None
            
            # Check if email is verified
            if not user.is_verified:
                return False, "Please verify your email before logging in", None
            
            # Create access token
            access_token = self._create_access_token(user.user_id, user.email)
            
            # Create refresh token
            refresh_token = self._create_refresh_token(user.user_id, user.email)
            
            # Create user session
            session = self._create_user_session(
                user.user_id, access_token, user_agent, ip_address
            )
            
            # Update last login
            user.last_login = datetime.now()
            user_storage_service.save_data()
            
            # Clear failed login attempts
            self._clear_login_attempts(login_data.email)
            
            logger.info(f"User logged in successfully: {user.email}")
            
            auth_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": SecurityConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_verified": user.is_verified
                }
            }
            
            return True, "Login successful", auth_data
            
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False, f"Login failed: {str(e)}", None
    
    def logout_user(self, session_id: str) -> Tuple[bool, str]:
        """
        Log out user by invalidating session.
        
        Args:
            session_id: Session ID to invalidate
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if session_id in user_storage.sessions:
                del user_storage.sessions[session_id]
                user_storage_service.save_data()
                logger.info(f"User logged out successfully: {session_id}")
                return True, "Logout successful"
            else:
                return False, "Session not found"
                
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return False, f"Logout failed: {str(e)}"
    
    def verify_email(self, token: str) -> Tuple[bool, str]:
        """
        Verify user email using verification token.
        
        Args:
            token: Verification token
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if token not in user_storage.verification_tokens:
                return False, "Invalid verification token"
            
            verification_data = user_storage.verification_tokens[token]
            
            # Check if token is expired
            if verification_data.expires_at < datetime.now():
                del user_storage.verification_tokens[token]
                user_storage_service.save_data()
                return False, "Verification token has expired"
            
            # Find user and mark as verified
            user_id = verification_data.user_id
            if user_id in user_storage.users:
                user = user_storage.users[user_id]
                user.is_verified = True
                
                # Remove verification token
                del user_storage.verification_tokens[token]
                user_storage_service.save_data()
                
                logger.info(f"Email verified successfully for user: {user.email}")
                return True, "Email verified successfully"
            else:
                return False, "User not found"
                
        except Exception as e:
            logger.error(f"Error verifying email: {e}")
            return False, f"Email verification failed: {str(e)}"
    
    def request_password_reset(self, reset_request: PasswordResetRequest) -> Tuple[bool, str]:
        """
        Request password reset for a user.
        
        Args:
            reset_request: Password reset request data
            
        Returns:
            Tuple of (success, message)
        """
        try:
            user = self.get_user_by_email(reset_request.email)
            if not user:
                # Don't reveal whether user exists for security
                return True, "If the email exists, a reset link has been sent"
            
            # Create reset token
            reset_token = self._create_reset_token(user.user_id, user.email)
            
            # In real implementation, send email with reset link
            logger.info(f"Password reset token created for user: {user.email}")
            
            return True, "If the email exists, a reset link has been sent"
            
        except Exception as e:
            logger.error(f"Error requesting password reset: {e}")
            return False, f"Password reset request failed: {str(e)}"
    
    def reset_password(self, reset_confirm: PasswordResetConfirm) -> Tuple[bool, str]:
        """
        Reset user password using reset token.
        
        Args:
            reset_confirm: Password reset confirmation data
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if reset_confirm.token not in user_storage.reset_tokens:
                return False, "Invalid reset token"
            
            reset_data = user_storage.reset_tokens[reset_confirm.token]
            
            # Check if token is expired or used
            if reset_data.expires_at < datetime.now() or reset_data.used:
                del user_storage.reset_tokens[reset_confirm.token]
                user_storage_service.save_data()
                return False, "Reset token has expired or been used"
            
            # Validate new password strength
            password_analysis = password_hasher.is_password_strong(reset_confirm.new_password)
            if password_analysis["strength"] == "weak":
                return False, "New password is too weak"
            
            # Find user and update password
            user_id = reset_data.user_id
            if user_id in user_storage.users:
                user = user_storage.users[user_id]
                
                # Hash new password
                hashed_password = password_hasher.hash_password(reset_confirm.new_password)
                setattr(user, '_password_hash', hashed_password)
                
                # Mark token as used
                reset_data.used = True
                user_storage_service.save_data()
                
                logger.info(f"Password reset successfully for user: {user.email}")
                return True, "Password reset successfully"
            else:
                return False, "User not found"
                
        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            return False, f"Password reset failed: {str(e)}"
    
    def get_user_by_email(self, email: str) -> Optional[UserProfile]:
        """Find user by email address."""
        email_lower = email.lower()
        for user in user_storage.users.values():
            if user.email.lower() == email_lower:
                return user
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[UserProfile]:
        """Find user by user ID."""
        return user_storage.users.get(user_id)
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token and return payload."""
        return token_manager.verify_token(token)
    
    def refresh_access_token(self, refresh_token: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Refresh access token using refresh token."""
        try:
            payload = self.validate_token(refresh_token)
            if not payload:
                return False, "Invalid refresh token", None
            
            user_id = payload.get("sub")
            email = payload.get("email")
            
            if not user_id or not email:
                return False, "Invalid token payload", None
            
            # Create new access token
            new_access_token = self._create_access_token(user_id, email)
            
            auth_data = {
                "access_token": new_access_token,
                "token_type": "bearer",
                "expires_in": SecurityConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
            
            return True, "Token refreshed successfully", auth_data
            
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return False, f"Token refresh failed: {str(e)}", None
    
    def _create_access_token(self, user_id: str, email: str) -> str:
        """Create JWT access token."""
        return token_manager.create_access_token({
            "sub": user_id,
            "email": email,
            "type": "access"
        })
    
    def _create_refresh_token(self, user_id: str, email: str) -> str:
        """Create JWT refresh token."""
        return token_manager.create_refresh_token({
            "sub": user_id,
            "email": email,
            "type": "refresh"
        })
    
    def _create_user_session(self, user_id: str, token: str, 
                           user_agent: Optional[str], ip_address: Optional[str]) -> UserSession:
        """Create user session."""
        session_id = generate_session_id()
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            token=token,
            created_at=datetime.now(),
            expires_at=calculate_session_expiry(),
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        user_storage.sessions[session_id] = session
        return session
    
    def _create_reset_token(self, user_id: str, email: str) -> str:
        """Create password reset token."""
        token = generate_reset_token()
        reset_token = PasswordResetToken(
            token=token,
            user_id=user_id,
            email=email,
            created_at=datetime.now(),
            expires_at=calculate_token_expiry(SecurityConfig.RESET_TOKEN_EXPIRE_MINUTES),
            used=False
        )
        
        user_storage.reset_tokens[token] = reset_token
        user_storage_service.save_data()
        return token
    
    def _create_verification_token(self, user_id: str, email: str) -> str:
        """Create email verification token."""
        token = generate_verification_token()
        verification_token = EmailVerificationToken(
            token=token,
            user_id=user_id,
            email=email,
            created_at=datetime.now(),
            expires_at=calculate_token_expiry(SecurityConfig.VERIFICATION_TOKEN_EXPIRE_MINUTES)
        )
        
        user_storage.verification_tokens[token] = verification_token
        user_storage_service.save_data()
        return token
    
    def _is_rate_limited(self, email: str) -> bool:
        """Check if login attempts are rate limited."""
        email_key = email.lower()
        
        if email_key not in self.login_attempts:
            return False
        
        attempt_data = self.login_attempts[email_key]
        current_time = datetime.now()
        
        # Check if lockout period has expired
        if (attempt_data.get("lockout_until") and 
            attempt_data["lockout_until"] > current_time):
            return True
        
        # Check if max attempts reached
        if (attempt_data.get("attempt_count", 0) >= SecurityConfig.MAX_LOGIN_ATTEMPTS and
            attempt_data.get("last_attempt") and
            (current_time - attempt_data["last_attempt"]).total_seconds() < 
            SecurityConfig.LOGIN_LOCKOUT_MINUTES * 60):
            
            # Set lockout period
            attempt_data["lockout_until"] = current_time + timedelta(
                minutes=SecurityConfig.LOGIN_LOCKOUT_MINUTES
            )
            return True
        
        return False
    
    def _record_login_attempt(self, email: str, success: bool):
        """Record login attempt for rate limiting."""
        email_key = email.lower()
        
        if email_key not in self.login_attempts:
            self.login_attempts[email_key] = {
                "attempt_count": 0,
                "last_attempt": datetime.now(),
                "lockout_until": None
            }
        
        attempt_data = self.login_attempts[email_key]
        current_time = datetime.now()
        
        if not success:
            attempt_data["attempt_count"] += 1
            attempt_data["last_attempt"] = current_time
            
            # Reset attempt count if enough time has passed
            if (attempt_data["attempt_count"] > 0 and
                (current_time - attempt_data["last_attempt"]).total_seconds() > 3600):  # 1 hour
                attempt_data["attempt_count"] = 1
        else:
            # Reset on successful login
            attempt_data["attempt_count"] = 0
            attempt_data["lockout_until"] = None
    
    def _clear_login_attempts(self, email: str):
        """Clear login attempts for email."""
        email_key = email.lower()
        if email_key in self.login_attempts:
            del self.login_attempts[email_key]

# Global auth service instance
auth_service = AuthService()
