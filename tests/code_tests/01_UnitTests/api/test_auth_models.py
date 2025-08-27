import pytest
import sys
import os
from pathlib import Path
from datetime import datetime

# Add source to path - calculate the correct path to src directory
current_file = Path(__file__)
project_root = current_file.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
print(f"Added to path: {project_root / 'src'}")

from autoprojectmanagement.api.auth_models import (
    UserRegisterRequest,
    UserLoginRequest,
    UserProfileResponse,
    AuthTokenResponse,
    LoginSuccessResponse,
    RegisterSuccessResponse,
    RegisterErrorResponse,
    ErrorCodes,
    SuccessMessages
)

class TestUserRegisterRequest:
    def test_valid_registration(self):
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserRegisterRequest(**data)
        assert request.email == "user@example.com"

    def test_invalid_email(self):
        data = {
            "email": "invalid-email",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        with pytest.raises(Exception):
            UserRegisterRequest(**data)

    def test_weak_password(self):
        data = {
            "email": "user@example.com",
            "password": "weak",
            "first_name": "John",
            "last_name": "Doe"
        }
        with pytest.raises(Exception):
            UserRegisterRequest(**data)

    def test_email_case_insensitivity(self):
        data = {
            "email": "USER@EXAMPLE.COM",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserRegisterRequest(**data)
        assert request.email == "user@example.com"

    def test_international_names(self):
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "José",
            "last_name": "Müller"
        }
        request = UserRegisterRequest(**data)
        assert request.first_name == "José"

class TestUserLoginRequest:
    def test_valid_login(self):
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }
        request = UserLoginRequest(**data)
        assert request.email == "user@example.com"

    def test_invalid_login_email(self):
        data = {
            "email": "invalid-email",
            "password": "SecurePass123!"
        }
        with pytest.raises(Exception):
            UserLoginRequest(**data)

class TestUserProfileResponse:
    def test_user_profile_creation(self):
        now = datetime.now()
        data = {
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_verified": True,
            "is_active": True,
            "created_at": now,
            "last_login": now
        }
        response = UserProfileResponse(**data)
        assert response.user_id == "550e8400-e29b-41d4-a716-446655440000"

class TestAuthTokenResponse:
    def test_auth_token_creation(self):
        user_profile_data = {
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_verified": True,
            "is_active": True,
            "created_at": datetime.now(),
            "last_login": datetime.now()
        }
        user_profile = UserProfileResponse(**user_profile_data)
        
        data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        
        response = AuthTokenResponse(**data)
        assert response.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

class TestLoginSuccessResponse:
    def test_login_success_creation(self):
        user_profile_data = {
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_verified": True,
            "is_active": True,
            "created_at": datetime.now(),
            "last_login": datetime.now()
        }
        user_profile = UserProfileResponse(**user_profile_data)
        
        auth_token_data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        auth_token = AuthTokenResponse(**auth_token_data)
        
        data = {
            "success": True,
            "message": "Login successful",
            "data": auth_token
        }
        
        response = LoginSuccessResponse(**data)
        assert response.success == True

# Additional tests for error handling and integration can be added here.

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
