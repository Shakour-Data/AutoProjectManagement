#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/utils/security.py
File: security.py
Purpose: Security utilities for authentication system
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Password hashing, token generation, and security utilities
"""

import bcrypt
import jwt
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security configuration
class SecurityConfig:
    """Security configuration settings."""
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "autoprojectmanagement_secret_key_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password configuration
    PASSWORD_HASH_ROUNDS: int = 12
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 128
    
    # Token configuration
    RESET_TOKEN_EXPIRE_MINUTES: int = 30
    VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Rate limiting
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_MINUTES: int = 15
    
    # Session configuration
    SESSION_EXPIRE_HOURS: int = 24

class PasswordHasher:
    """Password hashing and verification utilities."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
            
        Raises:
            ValueError: If password is empty or too long
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        if len(password) > SecurityConfig.PASSWORD_MAX_LENGTH:
            raise ValueError(f"Password too long (max {SecurityConfig.PASSWORD_MAX_LENGTH} characters)")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=SecurityConfig.PASSWORD_HASH_ROUNDS)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            if plain_password is None or hashed_password is None:
                return False
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Length of the password (default: 16)
            
        Returns:
            Secure random password
        """
        if length < SecurityConfig.PASSWORD_MIN_LENGTH:
            length = SecurityConfig.PASSWORD_MIN_LENGTH
        
        # Character sets
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special = "!@#$%^&*()_-+=[]{}|;:,.<>?"
        
        # Ensure at least one character from each set
        password = [
            secrets.choice(uppercase),
            secrets.choice(lowercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # Fill the rest with random characters from all sets
        all_chars = uppercase + lowercase + digits + special
        password.extend(secrets.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def is_password_strong(password: str) -> Dict[str, Any]:
        """
        Check password strength and return detailed analysis.
        
        Args:
            password: Password to check
            
        Returns:
            Dictionary with strength analysis
        """
        analysis = {
            "length": len(password),
            "has_uppercase": any(c.isupper() for c in password),
            "has_lowercase": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in "!@#$%^&*()_-+=[]{}|;:,.<>?" for c in password),
            "is_common": password.lower() in common_passwords(),
            "score": 0,
            "strength": "weak",
            "suggestions": []
        }
        
        # Calculate score
        if analysis["length"] >= SecurityConfig.PASSWORD_MIN_LENGTH:
            analysis["score"] += 1
        
        if analysis["has_uppercase"]:
            analysis["score"] += 1
        
        if analysis["has_lowercase"]:
            analysis["score"] += 1
        
        if analysis["has_digit"]:
            analysis["score"] += 1
        
        if analysis["has_special"]:
            analysis["score"] += 1
        
        if analysis["length"] >= 12:
            analysis["score"] += 1
        
        if not analysis["is_common"]:
            analysis["score"] += 1
        
        # Determine strength
        if analysis["score"] >= 6:
            analysis["strength"] = "strong"
        elif analysis["score"] >= 4:
            analysis["strength"] = "medium"
        else:
            analysis["strength"] = "weak"
        
        # Generate suggestions
        if analysis["length"] < SecurityConfig.PASSWORD_MIN_LENGTH:
            analysis["suggestions"].append(
                f"Use at least {SecurityConfig.PASSWORD_MIN_LENGTH} characters"
            )
        
        if not analysis["has_uppercase"]:
            analysis["suggestions"].append("Add uppercase letters")
        
        if not analysis["has_lowercase"]:
            analysis["suggestions"].append("Add lowercase letters")
        
        if not analysis["has_digit"]:
            analysis["suggestions"].append("Add numbers")
        
        if not analysis["has_special"]:
            analysis["suggestions"].append("Add special characters")
        
        if analysis["is_common"]:
            analysis["suggestions"].append("Avoid common passwords")
        
        return analysis

class TokenManager:
    """JWT token generation and verification utilities."""
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to include in the token
            expires_delta: Optional expiration time delta
            
        Returns:
            JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=SecurityConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            SecurityConfig.JWT_SECRET_KEY, 
            algorithm=SecurityConfig.JWT_ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            data: Data to include in the token
            expires_delta: Optional expiration time delta
            
        Returns:
            JWT refresh token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=SecurityConfig.JWT_REFRESH_TOKEN_EXPIRE_DAYS
            )
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            SecurityConfig.JWT_SECRET_KEY, 
            algorithm=SecurityConfig.JWT_ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token data if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token, 
                SecurityConfig.JWT_SECRET_KEY, 
                algorithms=[SecurityConfig.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate a secure CSRF token."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key."""
        return f"apk_{secrets.token_urlsafe(32)}"

class SecurityUtils:
    """General security utilities."""
    
    @staticmethod
    def sanitize_input(input_string: str, max_length: int = 255) -> str:
        """
        Sanitize user input to prevent XSS and injection attacks.
        
        Args:
            input_string: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        import re
        if not input_string:
            return ""
        
        # Trim and limit length
        sanitized = input_string.strip()
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Remove script tags and potentially dangerous characters
        sanitized = re.sub(r'<script.*?>.*?</script>', '', sanitized, flags=re.IGNORECASE|re.DOTALL)
        dangerous_chars = ['<', '>', '"', "'", ';', '(', ')', '&', '|', '`', '$']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format and basic security.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email is valid, False otherwise
        """
        import re
        
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False
        
        # Additional security checks
        if len(email) > 254:  # RFC 5321 limit
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'\.\.',  # Double dots
            r'@.*@',  # Multiple @ signs
            r'\.@',   # Dot before @
            r'@\.',   # @ before dot
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, email):
                return False
        
        return True
    
    @staticmethod
    def generate_secure_random_string(length: int = 32) -> str:
        """
        Generate a secure random string.
        
        Args:
            length: Length of the string
            
        Returns:
            Secure random string
        """
        return secrets.token_urlsafe(length)

def common_passwords() -> set:
    """Return a set of common passwords to avoid."""
    return {
        "password", "123456", "12345678", "123456789", "qwerty",
        "abc123", "password1", "12345", "1234567", "1234567890",
        "admin", "welcome", "monkey", "letmein", "login", "passw0rd",
        "master", "hello", "freedom", "whatever", "qazwsx", "trustno1",
        "dragon", "baseball", "superman", "mustang", "shadow", "sunshine",
        "princess", "football", "michael", "ninja", "jennifer", "hunter",
        "charlie", "andrew", "thomas", "computer", "michelle", "jessica",
        "pepper", "daniel", "access", "jordan", "111111", "123123",
        "1234", "123", "qwerty123", "1q2w3e4r", "654321", "555555",
        "lovely", "7777777", "welcome", "888888", "princess", "dragon",
        "password123", "passw0rd", "password1", "123qwe", "aa123456"
    }

# Global instances
password_hasher = PasswordHasher()
token_manager = TokenManager()
security_utils = SecurityUtils()
