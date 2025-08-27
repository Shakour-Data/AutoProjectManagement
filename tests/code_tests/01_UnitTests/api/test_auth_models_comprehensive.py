import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import re

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from autoprojectmanagement.api.auth_models import (
    UserRegisterRequest, UserLoginRequest, UserProfileResponse,
    AuthTokenResponse, LoginSuccessResponse, RegisterSuccessResponse,
    LoginErrorResponse, RegisterErrorResponse, PasswordResetRequest,
    PasswordResetConfirmRequest, EmailVerifyRequest, TokenRefreshRequest,
    TokenRefreshResponse, LogoutRequest, LogoutResponse, UserUpdateRequest,
    PasswordChangeRequest, AuthConfigResponse, ErrorResponse, SuccessResponse,
    ValidationErrorDetail, ValidationErrorResponse, ErrorCodes, SuccessMessages
)

class TestUserRegisterRequest:
    """Comprehensive tests for UserRegisterRequest model."""
    
    # Functionality Tests
    def test_valid_registration(self):
        """Test valid registration data."""
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserRegisterRequest(**data)
        assert request.email == "user@example.com"
        assert request.first_name == "John"
        assert request.last_name == "Doe"

    def test_email_normalization(self):
        """Test email case normalization."""
        data = {
            "email": "USER@EXAMPLE.COM",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserRegisterRequest(**data)
        assert request.email == "user@example.com"

    def test_international_names(self):
        """Test international character support."""
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "José",
            "last_name": "Müller-Östlund"
        }
        request = UserRegisterRequest(**data)
        assert request.first_name == "José"
        assert request.last_name == "Müller-Östlund"

    def test_name_length_boundaries(self):
        """Test name field length boundaries."""
        # Minimum length
        data_min = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "J",
            "last_name": "D"
        }
        request_min = UserRegisterRequest(**data_min)
        assert len(request_min.first_name) == 1
        assert len(request_min.last_name) == 1

        # Maximum length
        long_name = "A" * 50
        data_max = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": long_name,
            "last_name": long_name
        }
        request_max = UserRegisterRequest(**data_max)
        assert len(request_max.first_name) == 50
        assert len(request_max.last_name) == 50

    # Edge Case Tests
    def test_email_edge_cases(self):
        """Test various email edge cases."""
        valid_emails = [
            "test.user+tag@example.com",
            "user.name@sub.domain.co.uk",
            "first.last@example.io",
            "email@domain-one.com",
            "123456@example.com"
        ]
        
        for email in valid_emails:
            data = {
                "email": email,
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User"
            }
            request = UserRegisterRequest(**data)
            assert request.email == email.lower()

    def test_password_complexity_edge_cases(self):
        """Test password complexity edge cases."""
        # Just meets requirements
        data = {
            "email": "user@example.com",
            "password": "Pass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserRegisterRequest(**data)
        assert request.password == "Pass123!"

    def test_name_edge_cases(self):
        """Test name field edge cases."""
        edge_cases = [
            ("O'Reilly", "MacDonald"),
            ("Van der Berg", "De Souza"),
            ("Élise", "François"),
            ("Алексей", "Петров"),  # Cyrillic
            ("小明", "王"),         # Chinese
            ("太郎", "山田")        # Japanese
        ]
        
        for first_name, last_name in edge_cases:
            data = {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "first_name": first_name,
                "last_name": last_name
            }
            request = UserRegisterRequest(**data)
            assert request.first_name == first_name
            assert request.last_name == last_name

    # Error Handling Tests
    def test_invalid_email_format(self):
        """Test invalid email formats."""
        invalid_emails = [
            "invalid-email",
            "user@",
            "@example.com",
            "user@.com",
            "user@example..com"
        ]
        
        for email in invalid_emails:
            data = {
                "email": email,
                "password": "SecurePass123!",
                "first_name": "John",
                "last_name": "Doe"
            }
            with pytest.raises(Exception):
                UserRegisterRequest(**data)

    def test_weak_password_validation(self):
        """Test password strength validation."""
        weak_passwords = [
            "short",           # Too short
            "nouppercase123",  # No uppercase
            "NOLOWERCASE123",  # No lowercase  
            "NoNumbers!",      # No numbers
            "onlylowercase"    # Only lowercase
        ]
        
        for password in weak_passwords:
            data = {
                "email": "user@example.com",
                "password": password,
                "first_name": "John",
                "last_name": "Doe"
            }
            with pytest.raises(Exception):
                UserRegisterRequest(**data)

    def test_missing_required_fields(self):
        """Test missing required fields."""
        test_cases = [
            {"password": "SecurePass123!", "first_name": "John", "last_name": "Doe"},
            {"email": "user@example.com", "first_name": "John", "last_name": "Doe"},
            {"email": "user@example.com", "password": "SecurePass123!", "last_name": "Doe"},
            {"email": "user@example.com", "password": "SecurePass123!", "first_name": "John"}
        ]
        
        for data in test_cases:
            with pytest.raises(Exception):
                UserRegisterRequest(**data)

    def test_name_length_validation(self):
        """Test name field length validation."""
        # Too short
        with pytest.raises(Exception):
            UserRegisterRequest(
                email="user@example.com",
                password="SecurePass123!",
                first_name="",
                last_name="Doe"
            )
        
        # Too long
        long_name = "A" * 51
        with pytest.raises(Exception):
            UserRegisterRequest(
                email="user@example.com",
                password="SecurePass123!",
                first_name=long_name,
                last_name="Doe"
            )

    # Integration Tests
    def test_integration_with_error_codes(self):
        """Test integration with error code constants."""
        # This test ensures the model validation aligns with expected error patterns
        try:
            UserRegisterRequest(
                email="invalid",
                password="weak",
                first_name="",
                last_name=""
            )
            assert False, "Should have raised validation error"
        except Exception as e:
            error_str = str(e)
            # Check that error message contains relevant validation info
            assert "email" in error_str.lower() or "password" in error_str.lower()

    def test_serialization_for_api_use(self):
        """Test model serialization for API usage."""
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserRegisterRequest(**data)
        
        # Test dict conversion
        request_dict = request.dict()
        assert request_dict["email"] == "user@example.com"
        assert request_dict["first_name"] == "John"
        assert request_dict["last_name"] == "Doe"
        
        # Test JSON serialization
        request_json = request.json()
        assert "user@example.com" in request_json
        assert "John" in request_json

class TestUserLoginRequest:
    """Comprehensive tests for UserLoginRequest model."""
    
    # Functionality Tests
    def test_valid_login(self):
        """Test valid login data."""
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }
        request = UserLoginRequest(**data)
        assert request.email == "user@example.com"
        assert request.password == "SecurePass123!"

    def test_email_normalization_login(self):
        """Test email case normalization in login."""
        data = {
            "email": "USER@EXAMPLE.COM",
            "password": "SecurePass123!"
        }
        request = UserLoginRequest(**data)
        assert request.email == "user@example.com"

    # Edge Case Tests
    def test_login_email_edge_cases(self):
        """Test various email edge cases for login."""
        valid_emails = [
            "test.user+tag@example.com",
            "user.name@sub.domain.co.uk",
            "first.last@example.io"
        ]
        
        for email in valid_emails:
            data = {
                "email": email,
                "password": "SecurePass123!"
            }
            request = UserLoginRequest(**data)
            assert request.email == email.lower()

    # Error Handling Tests
    def test_invalid_login_email(self):
        """Test invalid email formats for login."""
        invalid_emails = [
            "invalid-email",
            "user@",
            "@example.com"
        ]
        
        for email in invalid_emails:
            data = {
                "email": email,
                "password": "SecurePass123!"
            }
            with pytest.raises(Exception):
                UserLoginRequest(**data)

    def test_missing_login_fields(self):
        """Test missing required fields for login."""
        with pytest.raises(Exception):
            UserLoginRequest(email="user@example.com")
        
        with pytest.raises(Exception):
            UserLoginRequest(password="SecurePass123!")

    # Integration Tests
    def test_login_serialization(self):
        """Test login request serialization."""
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }
        request = UserLoginRequest(**data)
        
        request_dict = request.dict()
        assert request_dict["email"] == "user@example.com"
        assert "password" in request_dict

class TestUserProfileResponse:
    """Comprehensive tests for UserProfileResponse model."""
    
    # Functionality Tests
    def test_user_profile_creation(self):
        """Test user profile creation with valid data."""
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
        assert response.email == "user@example.com"
        assert response.is_verified is True
        assert response.is_active is True

    def test_user_profile_optional_fields(self):
        """Test user profile with optional last_login."""
        now = datetime.now()
        data = {
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_verified": False,
            "is_active": True,
            "created_at": now
            # last_login is optional
        }
        response = UserProfileResponse(**data)
        assert response.last_login is None
        assert response.is_verified is False

    # Edge Case Tests
    def test_user_profile_edge_cases(self):
        """Test user profile edge cases."""
        now = datetime.now()
        edge_cases = [
            {
                "user_id": "00000000-0000-0000-0000-000000000000",
                "email": "test@example.com",
                "first_name": "A",  # Minimum length
                "last_name": "B",   # Minimum length
                "is_verified": False,
                "is_active": False,
                "created_at": now
            },
            {
                "user_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
                "email": "long.email.address@very.long.domain.name.com",
                "first_name": "X" * 50,  # Maximum length
                "last_name": "Y" * 50,   # Maximum length
                "is_verified": True,
                "is_active": True,
                "created_at": now,
                "last_login": now
            }
        ]
        
        for data in edge_cases:
            response = UserProfileResponse(**data)
            assert response is not None

    # Error Handling Tests
    def test_user_profile_validation_errors(self):
        """Test user profile validation errors."""
        now = datetime.now()
        
        # Missing required fields
        with pytest.raises(Exception):
            UserProfileResponse(
                email="user@example.com",
                first_name="John",
                last_name="Doe",
                is_verified=True,
                is_active=True,
                created_at=now
            )  # Missing user_id
        
        with pytest.raises(Exception):
            UserProfileResponse(
                user_id="550e8400-e29b-41d4-a716-446655440000",
                first_name="John",
                last_name="Doe",
                is_verified=True,
                is_active=True,
                created_at=now
            )  # Missing email

    # Integration Tests
    def test_user_profile_serialization(self):
        """Test user profile serialization for API responses."""
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
        
        # Test dict conversion
        response_dict = response.dict()
        assert response_dict["user_id"] == "550e8400-e29b-41d4-a716-446655440000"
        assert response_dict["email"] == "user@example.com"
        
        # Test JSON serialization (should handle datetime properly)
        response_json = response.json()
        assert "550e8400-e29b-41d4-a716-446655440000" in response_json
        assert "user@example.com" in response_json

class TestAuthTokenResponse:
    """Comprehensive tests for AuthTokenResponse model."""
    
    # Functionality Tests
    def test_auth_token_creation(self):
        """Test auth token response creation."""
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
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        
        response = AuthTokenResponse(**data)
        assert response.access_token.startswith("eyJhbGciOiJ")
        assert response.token_type == "bearer"
        assert response.expires_in == 3600
        assert response.user.email == "user@example.com"

    def test_default_token_type(self):
        """Test default token type behavior."""
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
            "access_token": "test_token",
            "refresh_token": "refresh_token",
            "expires_in": 3600,
            "user": user_profile
            # token_type should default to "bearer"
        }
        
        response = AuthTokenResponse(**data)
        assert response.token_type == "bearer"

    # Edge Case Tests
    def test_token_edge_cases(self):
        """Test token response edge cases."""
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
        
        edge_cases = [
            {
                "access_token": "",
                "refresh_token": "",
                "expires_in": 0,
                "user": user_profile
            },
            {
                "access_token": "a" * 1000,  # Very long token
                "refresh_token": "b" * 1000,
                "expires_in": 86400,  # 24 hours
                "user": user_profile
            }
        ]
        
        for data in edge_cases:
            response = AuthTokenResponse(**data)
            assert response is not None

    # Error Handling Tests
    def test_missing_required_fields(self):
        """Test missing required fields in token response."""
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
        
        # Missing access_token
        with pytest.raises(Exception):
            AuthTokenResponse(
                refresh_token="test",
                expires_in=3600,
                user=user_profile
            )
        
        # Missing user
        with pytest.raises(Exception):
            AuthTokenResponse(
                access_token="test",
                refresh_token="test",
                expires_in=3600
            )

    # Integration Tests
    def test_token_response_serialization(self):
        """Test token response serialization."""
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
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        
        response = AuthTokenResponse(**data)
        response_dict = response.dict()
        
        assert response_dict["access_token"] == "test_access_token"
        assert response_dict["refresh_token"] == "test_refresh_token"
        assert response_dict["token_type"] == "bearer"
        assert "user" in response_dict

class TestLoginSuccessResponse:
    """Comprehensive tests for LoginSuccessResponse model."""
    
    # Functionality Tests
    def test_login_success_creation(self):
        """Test login success response creation."""
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
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
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
        assert response.success is True
        assert response.message == "Login successful"
        assert response.data.access_token == "test_access_token"

    def test_default_success_value(self):
        """Test default success value behavior."""
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
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        auth_token = AuthTokenResponse(**auth_token_data)
        
        data = {
            "message": "Login successful",
            "data": auth_token
            # success should default to True
        }
        
        response = LoginSuccessResponse(**data)
        assert response.success is True

    # Edge Case Tests
    def test_message_edge_cases(self):
        """Test various message edge cases."""
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
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        auth_token = AuthTokenResponse(**auth_token_data)
        
        edge_cases = [
            "",  # Empty message
            "A" * 1000,  # Very long message
            "Login successful with special chars !@#$%^&*()"
        ]
        
        for message in edge_cases:
            data = {
                "message": message,
                "data": auth_token
            }
            response = LoginSuccessResponse(**data)
            assert response.message == message

    # Error Handling Tests
    def test_missing_required_fields(self):
        """Test missing required fields."""
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
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        auth_token = AuthTokenResponse(**auth_token_data)
        
        # Missing message
        with pytest.raises(Exception):
            LoginSuccessResponse(
                success=True,
                data=auth_token
            )
        
        # Missing data
        with pytest.raises(Exception):
            LoginSuccessResponse(
                success=True,
                message="Login successful"
            )

    # Integration Tests
    def test_integration_with_success_messages(self):
        """Test integration with success message constants."""
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
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user_profile
        }
        auth_token = AuthTokenResponse(**auth_token_data)
        
        data = {
            "message": SuccessMessages.LOGIN_SUCCESS,
            "data": auth_token
        }
        
        response = LoginSuccessResponse(**data)
        assert response.message == "Login successful"

class TestRegisterSuccessResponse:
    """Comprehensive tests for RegisterSuccessResponse model."""
    
    # Functionality Tests
    def test_register_success_creation(self):
        """Test register success response creation."""
        data = {
            "success": True,
            "message": "User registered successfully",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com"
        }
        
        response = RegisterSuccessResponse(**data)
        assert response.success is True
        assert response.message == "User registered successfully"
        assert response.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert response.email == "user@example.com"

    def test_default_success_value_register(self):
        """Test default success value for register response."""
        data = {
            "message": "User registered successfully",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com"
            # success should default to True
        }
        
        response = RegisterSuccessResponse(**data)
        assert response.success is True

    # Edge Case Tests
    def test_uuid_edge_cases(self):
        """Test various UUID format edge cases."""
        uuid_cases = [
            "00000000-0000-0000-0000-000000000000",
            "ffffffff-ffff-ffff-ffff-ffffffffffff",
            "12345678-1234-5678-9abc-def012345678"
        ]
        
        for user_id in uuid_cases:
            data = {
                "message": "User registered successfully",
                "user_id": user_id,
                "email": "user@example.com"
            }
            
            response = RegisterSuccessResponse(**data)
            assert response.user_id == user_id

    # Error Handling Tests
    def test_missing_required_fields_register(self):
        """Test missing required fields for register success."""
        # Missing user_id
        with pytest.raises(Exception):
            RegisterSuccessResponse(
                message="User registered successfully",
                email="user@example.com"
            )
        
        # Missing email
        with pytest.raises(Exception):
            RegisterSuccessResponse(
                message="User registered successfully",
                user_id="550e8400-e29b-41d4-a716-446655440000"
            )
        
        # Missing message
        with pytest.raises(Exception):
            RegisterSuccessResponse(
                user_id="550e8400-e29b-41d4-a716-446655440000",
                email="user@example.com"
            )

    # Integration Tests
    def test_integration_with_register_success_messages(self):
        """Test integration with register success message constants."""
        data = {
            "message": SuccessMessages.REGISTER_SUCCESS,
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com"
        }
        
        response = RegisterSuccessResponse(**data)
        assert response.message == "User registered successfully. Please verify your email."

class TestLoginErrorResponse:
    """Comprehensive tests for LoginErrorResponse model."""
    
    # Functionality Tests
    def test_login_error_creation(self):
        """Test login error response creation."""
        data = {
            "success": False,
            "message": "Invalid credentials",
            "error_code": ErrorCodes.INVALID_CREDENTIALS
        }
        
        response = LoginErrorResponse(**data)
        assert response.success is False
        assert response.message == "Invalid credentials"
        assert response.error_code == "auth_invalid_credentials"

    def test_default_success_value_error(self):
        """Test default success value for error response."""
        data = {
            "message": "Invalid credentials",
            "error_code": ErrorCodes.INVALID_CREDENTIALS
            # success should default to False
        }
        
        response = LoginErrorResponse(**data)
        assert response.success is False

    def test_optional_error_code(self):
        """Test error response without error code."""
        data = {
            "message": "Invalid credentials"
            # error_code is optional
        }
        
        response = LoginErrorResponse(**data)
        assert response.success is False
        assert response.message == "Invalid credentials"
        assert response.error_code is None

    # Edge Case Tests
    def test_error_message_edge_cases(self):
        """Test various error message edge cases."""
        error_cases = [
            ("", ErrorCodes.INVALID_CREDENTIALS),  # Empty message
            ("A" * 1000, ErrorCodes.USER_NOT_FOUND),  # Long message
            ("Error with special chars !@#$%", ErrorCodes.EXPIRED_TOKEN)
        ]
        
        for message, error_code in error_cases:
            data = {
                "message": message,
                "error_code": error_code
            }
            
            response = LoginErrorResponse(**data)
            assert response.message == message
            assert response.error_code == error_code

    # Error Handling Tests
    def test_missing_required_message(self):
        """Test missing required message field."""
        with pytest.raises(Exception):
            LoginErrorResponse(
                success=False,
                error_code=ErrorCodes.INVALID_CREDENTIALS
            )

    # Integration Tests
    def test_integration_with_error_codes(self):
        """Test integration with error code constants."""
        test_cases = [
            (ErrorCodes.INVALID_CREDENTIALS, "Invalid credentials"),
            (ErrorCodes.USER_NOT_FOUND, "User not found"),
            (ErrorCodes.ACCOUNT_LOCKED, "Account locked"),
            (ErrorCodes.EXPIRED_TOKEN, "Token expired")
        ]
        
        for error_code, message in test_cases:
            data = {
                "message": message,
                "error_code": error_code
            }
            
            response = LoginErrorResponse(**data)
            assert response.error_code == error_code
            assert response.message == message

class TestRegisterErrorResponse:
    """Comprehensive tests for RegisterErrorResponse model."""
    
    # Functionality Tests
    def test_register_error_creation(self):
        """Test register error response creation."""
        validation_errors = {
            "email": ["Invalid email format"],
            "password": ["Password too weak"]
        }
        
        data = {
            "success": False,
            "message": "Registration failed",
            "error_code": ErrorCodes.USER_ALREADY_EXISTS,
            "validation_errors": validation_errors
        }
        
        response = RegisterErrorResponse(**data)
        assert response.success is False
        assert response.message == "Registration failed"
        assert response.error_code == "auth_user_exists"
        assert response.validation_errors == validation_errors

    def test_default_success_and_optional_fields(self):
        """Test default values and optional fields."""
        data = {
            "message": "Registration failed"
            # success defaults to False
            # error_code is optional
            # validation_errors is optional
        }
        
        response = RegisterErrorResponse(**data)
        assert response.success is False
        assert response.message == "Registration failed"
        assert response.error_code is None
        assert response.validation_errors is None

    def test_validation_errors_structure(self):
        """Test validation errors structure."""
        validation_errors = {
            "email": ["Invalid format", "Already exists"],
            "password": ["Too short", "Missing uppercase"],
            "first_name": ["Required field"]
        }
        
        data = {
            "message": "Validation failed",
            "validation_errors": validation_errors
        }
        
        response = RegisterErrorResponse(**data)
        assert len(response.validation_errors) == 3
        assert "email" in response.validation_errors
        assert len(response.validation_errors["email"]) == 2

    # Edge Case Tests
    def test_validation_errors_edge_cases(self):
        """Test validation errors edge cases."""
        edge_cases = [
            {},  # Empty validation errors
            {"field": []},  # Empty error list
            {"field": ["Single error"]},  # Single error
            {"field": ["Error 1", "Error 2", "Error 3"]},  # Multiple errors
            {"very_long_field_name_that_exceeds_normal_length": ["Error"]}
        ]
        
        for validation_errors in edge_cases:
            data = {
                "message": "Validation failed",
                "validation_errors": validation_errors
            }
            
            response = RegisterErrorResponse(**data)
            assert response.validation_errors == validation_errors

    # Error Handling Tests
    def test_missing_required_message_register_error(self):
        """Test missing required message field."""
        with pytest.raises(Exception):
            RegisterErrorResponse(
                success=False,
                error_code=ErrorCodes.USER_ALREADY_EXISTS,
                validation_errors={"email": ["Invalid"]}
            )

    # Integration Tests
    def test_integration_with_validation_scenarios(self):
        """Test integration with common validation scenarios."""
        scenarios = [
            {
                "message": "Email validation failed",
                "validation_errors": {"email": ["Invalid format", "Already registered"]},
                "error_code": ErrorCodes.USER_ALREADY_EXISTS
            },
            {
                "message": "Password validation failed", 
                "validation_errors": {"password": ["Too weak", "Missing special character"]},
                "error_code": ErrorCodes.PASSWORD_TOO_WEAK
            }
        ]
        
        for scenario in scenarios:
            response = RegisterErrorResponse(**scenario)
            assert response.message == scenario["message"]
            assert response.validation_errors == scenario["validation_errors"]
            assert response.error_code == scenario["error_code"]

class TestPasswordResetRequest:
    """Comprehensive tests for PasswordResetRequest model."""
    
    # Functionality Tests
    def test_password_reset_request_creation(self):
        """Test password reset request creation."""
        data = {
            "email": "user@example.com"
        }
        
        request = PasswordResetRequest(**data)
        assert request.email == "user@example.com"

    def test_email_normalization_password_reset(self):
        """Test email case normalization in password reset."""
        data = {
            "email": "USER@EXAMPLE.COM"
        }
        
        request = PasswordResetRequest(**data)
        assert request.email == "user@example.com"

    # Edge Case Tests
    def test_password_reset_email_edge_cases(self):
        """Test various email edge cases for password reset."""
        valid_emails = [
            "test.user+tag@example.com",
            "user.name@sub.domain.co.uk",
            "first.last@example.io"
        ]
        
        for email in valid_emails:
            data = {
                "email": email
            }
            request = PasswordResetRequest(**data)
            assert request.email == email.lower()

    # Error Handling Tests
    def test_invalid_email_password_reset(self):
        """Test invalid email formats for password reset."""
        invalid_emails = [
            "invalid-email",
            "user@",
            "@example.com"
        ]
        
        for email in invalid_emails:
            data = {
                "email": email
            }
            with pytest.raises(Exception):
                PasswordResetRequest(**data)

    def test_missing_email_password_reset(self):
        """Test missing required email field."""
        with pytest.raises(Exception):
            PasswordResetRequest()

    # Integration Tests
    def test_password_reset_serialization(self):
        """Test password reset request serialization."""
        data = {
            "email": "user@example.com"
        }
        request = PasswordResetRequest(**data)
        
        request_dict = request.dict()
        assert request_dict["email"] == "user@example.com"
        
        request_json = request.json()
        assert "user@example.com" in request_json

class TestPasswordResetConfirmRequest:
    """Comprehensive tests for PasswordResetConfirmRequest model."""
    
    # Functionality Tests
    def test_password_reset_confirm_creation(self):
        """Test password reset confirm request creation."""
        data = {
            "token": "reset_token_12345",
            "new_password": "NewSecurePass123!"
        }
        
        request = PasswordResetConfirmRequest(**data)
        assert request.token == "reset_token_12345"
        assert request.new_password == "NewSecurePass123!"

    # Edge Case Tests
    def test_password_reset_confirm_edge_cases(self):
        """Test password reset confirm edge cases."""
        edge_cases = [
            {
                "token": "",
                "new_password": "Short1!"  # Minimum valid password
            },
            {
                "token": "a" * 100,  # Long token
                "new_password": "VeryLongPassword123!" * 5  # Long password
            }
        ]
        
        for data in edge_cases:
            request = PasswordResetConfirmRequest(**data)
            assert request.token == data["token"]
            assert request.new_password == data["new_password"]

    # Error Handling Tests
    def test_weak_password_reset_confirm(self):
        """Test weak password validation in reset confirm."""
        weak_passwords = [
            "short",           # Too short
            "nouppercase123",  # No uppercase
            "NOLOWERCASE123",  # No lowercase
            "NoNumbers!"       # No numbers
        ]
        
        for password in weak_passwords:
            data = {
                "token": "reset_token",
                "new_password": password
            }
            with pytest.raises(Exception):
                PasswordResetConfirmRequest(**data)

    def test_missing_required_fields_reset_confirm(self):
        """Test missing required fields for reset confirm."""
        # Missing token
        with pytest.raises(Exception):
            PasswordResetConfirmRequest(new_password="NewPass123!")
        
        # Missing password
        with pytest.raises(Exception):
            PasswordResetConfirmRequest(token="reset_token")

    # Integration Tests
    def test_password_reset_confirm_serialization(self):
        """Test password reset confirm serialization."""
        data = {
            "token": "reset_token_12345",
            "new_password": "NewSecurePass123!"
        }
        request = PasswordResetConfirmRequest(**data)
        
        request_dict = request.dict()
        assert request_dict["token"] == "reset_token_12345"
        assert "new_password" in request_dict

class TestEmailVerifyRequest:
    """Comprehensive tests for EmailVerifyRequest model."""
    
    # Functionality Tests
    def test_email_verify_request_creation(self):
        """Test email verify request creation."""
        data = {
            "token": "verify_token_12345"
        }
        
        request = EmailVerifyRequest(**data)
        assert request.token == "verify_token_12345"

    # Edge Case Tests
    def test_email_verify_token_edge_cases(self):
        """Test email verify token edge cases."""
        edge_cases = [
            "",  # Empty token
            "a" * 100,  # Long token
            "token_with_special_chars!@#$%^&*()"
        ]
        
        for token in edge_cases:
            data = {
                "token": token
            }
            request = EmailVerifyRequest(**data)
            assert request.token == token

    # Error Handling Tests
    def test_missing_token_email_verify(self):
        """Test missing required token field."""
        with pytest.raises(Exception):
            EmailVerifyRequest()

    # Integration Tests
    def test_email_verify_serialization(self):
        """Test email verify request serialization."""
        data = {
            "token": "verify_token_12345"
        }
        request = EmailVerifyRequest(**data)
        
        request_dict = request.dict()
        assert request_dict["token"] == "verify_token_12345"
        
        request_json = request.json()
        assert "verify_token_12345" in request_json

class TestTokenRefreshRequest:
    """Comprehensive tests for TokenRefreshRequest model."""
    
    # Functionality Tests
    def test_token_refresh_request_creation(self):
        """Test token refresh request creation."""
        data = {
            "refresh_token": "refresh_token_12345"
        }
        
        request = TokenRefreshRequest(**data)
        assert request.refresh_token == "refresh_token_12345"

    # Edge Case Tests
    def test_token_refresh_edge_cases(self):
        """Test token refresh edge cases."""
        edge_cases = [
            "",  # Empty token
            "a" * 1000,  # Very long token
            "token_with_special_chars!@#$%^&*()_+-="
        ]
        
        for token in edge_cases:
            data = {
                "refresh_token": token
            }
            request = TokenRefreshRequest(**data)
            assert request.refresh_token == token

    # Error Handling Tests
    def test_missing_refresh_token(self):
        """Test missing required refresh token field."""
        with pytest.raises(Exception):
            TokenRefreshRequest()

    # Integration Tests
    def test_token_refresh_serialization(self):
        """Test token refresh request serialization."""
        data = {
            "refresh_token": "refresh_token_12345"
        }
        request = TokenRefreshRequest(**data)
        
        request_dict = request.dict()
        assert request_dict["refresh_token"] == "refresh_token_12345"

class TestTokenRefreshResponse:
    """Comprehensive tests for TokenRefreshResponse model."""
    
    # Functionality Tests
    def test_token_refresh_response_creation(self):
        """Test token refresh response creation."""
        data = {
            "access_token": "new_access_token_12345",
            "refresh_token": "new_refresh_token_12345",
            "token_type": "bearer",
            "expires_in": 3600
        }
        
        response = TokenRefreshResponse(**data)
        assert response.access_token == "new_access_token_12345"
        assert response.refresh_token == "new_refresh_token_12345"
        assert response.token_type == "bearer"
        assert response.expires_in == 3600

    def test_default_token_type_refresh(self):
        """Test default token type for refresh response."""
        data = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600
            # token_type should default to "bearer"
        }
        
        response = TokenRefreshResponse(**data)
        assert response.token_type == "bearer"

    # Edge Case Tests
    def test_token_refresh_response_edge_cases(self):
        """Test token refresh response edge cases."""
        edge_cases = [
            {
                "access_token": "",
                "refresh_token": "",
                "expires_in": 0
            },
            {
                "access_token": "a" * 1000,
                "refresh_token": "b" * 1000,
                "expires_in": 86400
            }
        ]
        
        for data in edge_cases:
            response = TokenRefreshResponse(**data)
            assert response is not None

    # Error Handling Tests
    def test_missing_required_fields_refresh_response(self):
        """Test missing required fields in refresh response."""
        # Missing access_token
        with pytest.raises(Exception):
            TokenRefreshResponse(
                refresh_token="test",
                expires_in=3600
            )
        
        # Missing refresh_token
        with pytest.raises(Exception):
            TokenRefreshResponse(
                access_token="test",
                expires_in=3600
            )
        
        # Missing expires_in
        with pytest.raises(Exception):
            TokenRefreshResponse(
                access_token="test",
                refresh_token="test"
            )

    # Integration Tests
    def test_token_refresh_response_serialization(self):
        """Test token refresh response serialization."""
        data = {
            "access_token": "new_access_token_12345",
            "refresh_token": "new_refresh_token_12345",
            "token_type": "bearer",
            "expires_in": 3600
        }
        
        response = TokenRefreshResponse(**data)
        response_dict = response.dict()
        
        assert response_dict["access_token"] == "new_access_token_12345"
        assert response_dict["refresh_token"] == "new_refresh_token_12345"
        assert response_dict["token_type"] == "bearer"
        assert response_dict["expires_in"] == 3600

class TestLogoutRequest:
    """Comprehensive tests for LogoutRequest model."""
    
    # Functionality Tests
    def test_logout_request_creation(self):
        """Test logout request creation."""
        data = {
            "refresh_token": "refresh_token_12345"
        }
        
        request = LogoutRequest(**data)
        assert request.refresh_token == "refresh_token_12345"

    # Edge Case Tests
    def test_logout_request_edge_cases(self):
        """Test logout request edge cases."""
        edge_cases = [
            "",  # Empty token
            "a" * 1000  # Very long token
        ]
        
        for token in edge_cases:
            data = {
                "refresh_token": token
            }
            request = LogoutRequest(**data)
            assert request.refresh_token == token

    # Error Handling Tests
    def test_missing_refresh_token(self):
        """Test missing required refresh token field."""
        with pytest.raises(Exception):
            LogoutRequest()

    # Integration Tests
    def test_logout_request_serialization(self):
        """Test logout request serialization."""
        data = {
            "refresh_token": "refresh_token_12345"
        }
        request = LogoutRequest(**data)
        
        request_dict = request.dict()
        assert request_dict["refresh_token"] == "refresh_token_12345"

class TestLogoutResponse:
    """Comprehensive tests for LogoutResponse model."""
    
    # Functionality Tests
    def test_logout_response_creation(self):
        """Test logout response creation."""
        data = {
            "success": True,
            "message": "Logout successful"
        }
        
        response = LogoutResponse(**data)
        assert response.success is True
        assert response.message == "Logout successful"

    # Edge Case Tests
    def test_logout_response_edge_cases(self):
        """Test logout response edge cases."""
        edge_cases = [
            {"success": True, "message": ""},
            {"success": False, "message": "Logout failed"}
        ]
        
        for data in edge_cases:
            response = LogoutResponse(**data)
            assert response.success == data["success"]
            assert response.message == data["message"]

    # Error Handling Tests
    def test_missing_required_fields_logout_response(self):
        """Test missing required fields in logout response."""
        with pytest.raises(Exception):
            LogoutResponse(message="Logout successful")  # Missing success field
        
        with pytest.raises(Exception):
            LogoutResponse(success=False)  # Missing message field

    # Integration Tests
    def test_logout_response_serialization(self):
        """Test logout response serialization."""
        data = {
            "success": True,
            "message": "Logout successful"
        }
        response = LogoutResponse(**data)
        
        response_dict = response.dict()
        assert response_dict["success"] is True
        assert response_dict["message"] == "Logout successful"

class TestUserUpdateRequest:
    """Comprehensive tests for UserUpdateRequest model."""
    
    # Functionality Tests
    def test_user_update_request_creation(self):
        """Test user update request creation."""
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        
        request = UserUpdateRequest(**data)
        assert request.first_name == "John"
        assert request.last_name == "Doe"
        assert request.email is None  # Optional field

    def test_user_update_with_email(self):
        """Test user update request with email."""
        data = {
            "email": "new.email@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        request = UserUpdateRequest(**data)
        assert request.email == "new.email@example.com"
        assert request.first_name == "John"
        assert request.last_name == "Doe"

    # Edge Case Tests
    def test_user_update_edge_cases(self):
        """Test user update request edge cases."""
        edge_cases = [
            {
                "first_name": "A",  # Minimum length
                "last_name": "B"    # Minimum length
            },
            {
                "first_name": "X" * 50,  # Maximum length
                "last_name": "Y" * 50,   # Maximum length
                "email": "very.long.email.address@very.long.domain.name.com"
            }
        ]
        
        for data in edge_cases:
            request = UserUpdateRequest(**data)
            assert request is not None

    def test_international_names_update(self):
        """Test international character support in update."""
        data = {
            "first_name": "José",
            "last_name": "Müller-Östlund"
        }
        
        request = UserUpdateRequest(**data)
        assert request.first_name == "José"
        assert request.last_name == "Müller-Östlund"

    # Error Handling Tests
    def test_name_length_validation_update(self):
        """Test name field length validation in update."""
        # Too short
        with pytest.raises(Exception):
            UserUpdateRequest(
                first_name="",
                last_name="Doe"
            )
        
        # Too long
        long_name = "A" * 51
        with pytest.raises(Exception):
            UserUpdateRequest(
                first_name=long_name,
                last_name="Doe"
            )

    def test_invalid_email_update(self):
        """Test invalid email format in update."""
        with pytest.raises(Exception):
            UserUpdateRequest(
                email="invalid-email",
                first_name="John",
                last_name="Doe"
            )

    # Integration Tests
    def test_user_update_serialization(self):
        """Test user update request serialization."""
        data = {
            "email": "new.email@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserUpdateRequest(**data)
        
        request_dict = request.dict()
        assert request_dict["email"] == "new.email@example.com"
        assert request_dict["first_name"] == "John"
        assert request_dict["last_name"] == "Doe"
        
        # Test that None values are excluded
        data_partial = {
            "first_name": "John",
            "last_name": "Doe"
        }
        request_partial = UserUpdateRequest(**data_partial)
        request_dict_partial = request_partial.dict(exclude_none=True)
        assert "email" not in request_dict_partial

class TestPasswordChangeRequest:
    """Comprehensive tests for PasswordChangeRequest model."""
    
    # Functionality Tests
    def test_password_change_request_creation(self):
        """Test password change request creation."""
        data = {
            "current_password": "CurrentPass123!",
            "new_password": "NewSecurePass123!"
        }
        
        request = PasswordChangeRequest(**data)
        assert request.current_password == "CurrentPass123!"
        assert request.new_password == "NewSecurePass123!"

    # Edge Case Tests
    def test_password_change_edge_cases(self):
        """Test password change edge cases."""
        edge_cases = [
            {
                "current_password": "Short1!",  # Minimum valid password
                "new_password": "Short2!"       # Minimum valid password
            },
            {
                "current_password": "VeryLongCurrentPassword123!" * 5,
                "new_password": "VeryLongNewPassword123!" * 5
            }
        ]
        
        for data in edge_cases:
            request = PasswordChangeRequest(**data)
            assert request.current_password == data["current_password"]
            assert request.new_password == data["new_password"]

    # Error Handling Tests
    def test_weak_password_validation_change(self):
        """Test weak password validation in password change."""
        weak_passwords = [
            "short",           # Too short
            "nouppercase123",  # No uppercase
            "NOLOWERCASE123",  # No lowercase
            "NoNumbers!"       # No numbers
        ]
        
        # Test weak current password
        for password in weak_passwords:
            data = {
                "current_password": password,
                "new_password": "ValidPass123!"
            }
            with pytest.raises(Exception):
                PasswordChangeRequest(**data)
        
        # Test weak new password
        for password in weak_passwords:
            data = {
                "current_password": "ValidPass123!",
                "new_password": password
            }
            with pytest.raises(Exception):
                PasswordChangeRequest(**data)

    def test_missing_required_fields_password_change(self):
        """Test missing required fields for password change."""
        # Missing current_password
        with pytest.raises(Exception):
            PasswordChangeRequest(new_password="NewPass123!")
        
        # Missing new_password
        with pytest.raises(Exception):
            PasswordChangeRequest(current_password="CurrentPass123!")

    def test_same_password_validation(self):
        """Test that current and new passwords cannot be the same."""
        data = {
            "current_password": "SamePassword123!",
            "new_password": "SamePassword123!"
        }
        
        with pytest.raises(Exception):
            PasswordChangeRequest(**data)

    # Integration Tests
    def test_password_change_serialization(self):
        """Test password change request serialization."""
        data = {
            "current_password": "CurrentPass123!",
            "new_password": "NewSecurePass123!"
        }
        request = PasswordChangeRequest(**data)
        
        request_dict = request.dict()
        assert "current_password" in request_dict
        assert "new_password" in request_dict
        
        # Test that passwords are not exposed in serialization
        request_json = request.json()
        assert "CurrentPass123!" not in request_json
        assert "NewSecurePass123!" not in request_json

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
