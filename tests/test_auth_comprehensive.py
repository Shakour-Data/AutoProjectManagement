#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: tests/test_auth_comprehensive.py
File: test_auth_comprehensive.py
Purpose: Comprehensive unit tests for authentication system
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Complete test suite for authentication service, models, and endpoints
"""

import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException, status

from autoprojectmanagement.services.auth_service import AuthService, auth_service
from autoprojectmanagement.api.auth_models import (
    UserRegisterRequest, UserLoginRequest, PasswordResetRequest,
    PasswordResetConfirmRequest, EmailVerifyRequest
)
from autoprojectmanagement.api.main import app
from autoprojectmanagement.storage.user_storage import user_storage_service
from autoprojectmanagement.utils.security import password_hasher, token_manager

# Test client for API testing
client = TestClient(app)

class TestAuthService:
    """Test suite for AuthService class."""
    
    def setup_method(self):
        """Setup before each test method."""
        # Clear any existing test data
        user_storage_service.load_data()
        self.auth_service = AuthService()
        
        # Test user data
        self.test_user_data = UserRegisterRequest(
            email="test@example.com",
            password="SecurePass123!",
            first_name="Test",
            last_name="User"
        )
        
        self.test_login_data = UserLoginRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
    
    def teardown_method(self):
        """Cleanup after each test method."""
        # Clean up test data
        user_storage_service.load_data()
    
    def test_register_user_success(self):
        """Test successful user registration."""
        success, message, user_profile = self.auth_service.register_user(self.test_user_data)
        
        assert success is True
        assert "successfully" in message
        assert user_profile is not None
        assert user_profile.email == self.test_user_data.email
        assert user_profile.first_name == self.test_user_data.first_name
        assert user_profile.last_name == self.test_user_data.last_name
        assert user_profile.is_verified is False
    
    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email."""
        # Register first user
        self.auth_service.register_user(self.test_user_data)
        
        # Try to register again with same email
        success, message, user_profile = self.auth_service.register_user(self.test_user_data)
        
        assert success is False
        assert "already exists" in message
        assert user_profile is None
    
    def test_register_user_weak_password(self):
        """Test registration with weak password."""
        weak_user_data = UserRegisterRequest(
            email="weak@example.com",
            password="weak",
            first_name="Weak",
            last_name="Password"
        )
        
        success, message, user_profile = self.auth_service.register_user(weak_user_data)
        
        assert success is False
        assert "weak" in message.lower()
        assert user_profile is None
    
    def test_login_user_success(self):
        """Test successful user login."""
        # First register user
        self.auth_service.register_user(self.test_user_data)
        
        # Then login
        success, message, auth_data = self.auth_service.login_user(self.test_login_data)
        
        assert success is True
        assert "successful" in message
        assert auth_data is not None
        assert "access_token" in auth_data
        assert "refresh_token" in auth_data
        assert auth_data["user"]["email"] == self.test_user_data.email
    
    def test_login_user_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Register user first
        self.auth_service.register_user(self.test_user_data)
        
        # Try login with wrong password
        wrong_login = UserLoginRequest(
            email="test@example.com",
            password="WrongPassword123!"
        )
        
        success, message, auth_data = self.auth_service.login_user(wrong_login)
        
        assert success is False
        assert "invalid" in message.lower()
        assert auth_data is None
    
    def test_login_user_nonexistent_email(self):
        """Test login with non-existent email."""
        nonexistent_login = UserLoginRequest(
            email="nonexistent@example.com",
