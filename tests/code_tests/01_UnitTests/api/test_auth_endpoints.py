"""
Comprehensive unit tests for autoprojectmanagement/api/auth_endpoints.py
Generated according to AutoProjectManagement testing standards
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from fastapi.security import HTTPAuthorizationCredentials

from autoprojectmanagement.api.auth_endpoints import router, get_current_user
from autoprojectmanagement.api.auth_models import (
    UserRegisterRequest, UserLoginRequest, PasswordResetRequest,
    PasswordResetConfirmRequest, EmailVerifyRequest, TokenRefreshRequest,
    UserUpdateRequest, PasswordChangeRequest, LogoutRequest
)

# Create test client
client = TestClient(router)

# Mock data for testing
TEST_USER_DATA = {
    "email": "test@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

TEST_LOGIN_DATA = {
    "email": "test@example.com",
    "password": "TestPassword123!"
}

class TestAuthEndpoints:
    """Test class for authentication endpoints"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.mock_auth_service = Mock()
        self.mock_user_storage = Mock()
        
        # Patch the dependencies
        self.auth_service_patch = patch('autoprojectmanagement.api.auth_endpoints.auth_service', self.mock_auth_service)
        self.user_storage_patch = patch('autoprojectmanagement.api.auth_endpoints.user_storage_service', self.mock_user_storage)
        
        self.auth_service_patch.start()
        self.user_storage_patch.start()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        self.auth_service_patch.stop()
        self.user_storage_patch.stop()

    # Functionality Tests (5 tests)
    def test_register_user_success(self):
        """Test successful user registration"""
        self.mock_auth_service.register_user.return_value = (True, "Registration successful", Mock(user_id="123", email="test@example.com"))
        
        response = client.post("/register", json=TEST_USER_DATA)
        
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user_id"] == "123"
        self.mock_auth_service.register_user.assert_called_once()

    def test_login_user_success(self):
        """Test successful user login"""
        auth_data = {
            "access_token": "test_token",
            "refresh_token": "refresh_token",
            "token_type": "bearer",
            "expires_in": 3600
        }
        self.mock_auth_service.login_user.return_value = (True, "Login successful", auth_data)
        
        response = client.post("/login", json=TEST_LOGIN_DATA)
        
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["data"]["access_token"] == "test_token"

    def test_get_profile_success(self):
        """Test successful profile retrieval"""
        user_profile = Mock(user_id="123", email="test@example.com", first_name="Test", last_name="User")
        self.mock_auth_service.get_user_by_id.return_value = user_profile
        
        # Mock the get_current_user dependency
        with patch('autoprojectmanagement.api.auth_endpoints.get_current_user') as mock_current_user:
            mock_current_user.return_value = {"sub": "123"}
            
            response = client.get("/profile", headers={"Authorization": "Bearer test_token"})
            
            assert response.status_code == 200
            self.mock_auth_service.get_user_by_id.assert_called_once_with("123")

    def test_refresh_token_success(self):
        """Test successful token refresh"""
        auth_data = {
            "access_token": "new_token",
            "token_type": "bearer",
            "expires_in": 3600
        }
        self.mock_auth_service.refresh_access_token.return_value = (True, "Token refreshed", auth_data)
        
        response = client.post("/refresh-token", json={"refresh_token": "old_refresh_token"})
        
        assert response.status_code == 200
        assert response.json()["access_token"] == "new_token"

    def test_logout_success(self):
        """Test successful user logout"""
        self.mock_auth_service.logout_user.return_value = None
        
        # Mock the get_current_user dependency
        with patch('autoprojectmanagement.api.auth_endpoints.get_current_user') as mock_current_user:
            mock_current_user.return_value = {"sub": "123"}
            
            response = client.post("/logout", json={})
            
            assert response.status_code == 200
            assert response.json()["success"] == True

    # Edge Case Tests (5 tests)
    def test_register_user_email_already_exists(self):
        """Test registration with existing email"""
        self.mock_auth_service.register_user.return_value = (False, "Email already exists", None)
        
        response = client.post("/register", json=TEST_USER_DATA)
        
        assert response.status_code == 400
        assert "Email already exists" in response.json()["detail"]

    def test_login_user_invalid_credentials(self):
        """Test login with invalid credentials"""
        self.mock_auth_service.login_user.return_value = (False, "Invalid credentials", None)
        
        response = client.post("/login", json={"email": "wrong@example.com", "password": "wrong"})
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_user_account_not_verified(self):
        """Test login with unverified account"""
        self.mock_auth_service.login_user.return_value = (False, "Please verify your email", None)
        
        response = client.post("/login", json=TEST_LOGIN_DATA)
        
        assert response.status_code == 403
        assert "verify" in response.json()["detail"].lower()

    def test_refresh_token_invalid(self):
        """Test token refresh with invalid refresh token"""
        self.mock_auth_service.refresh_access_token.return_value = (False, "Invalid refresh token", None)
        
        response = client.post("/refresh-token", json={"refresh_token": "invalid_token"})
        
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]

    def test_get_profile_user_not_found(self):
        """Test profile retrieval for non-existent user"""
        self.mock_auth_service.get_user_by_id.return_value = None
        
        with patch('autoprojectmanagement.api.auth_endpoints.get_current_user') as mock_current_user:
            mock_current_user.return_value = {"sub": "non_existent"}
            
            response = client.get("/profile", headers={"Authorization": "Bearer test_token"})
            
            assert response.status_code == 404
            assert "User profile not found" in response.json()["detail"]

    # Error Handling Tests (5 tests)
    def test_register_user_server_error(self):
        """Test registration with server error"""
        self.mock_auth_service.register_user.side_effect = Exception("Database error")
        
        response = client.post("/register", json=TEST_USER_DATA)
        
        assert response.status_code == 500
        assert "Registration failed" in response.json()["detail"]

    def test_login_user_server_error(self):
        """Test login with server error"""
        self.mock_auth_service.login_user.side_effect = Exception("Authentication service error")
        
        response = client.post("/login", json=TEST_LOGIN_DATA)
        
        assert response.status_code == 500
        assert "Login failed" in response.json()["detail"]

    def test_logout_user_server_error(self):
        """Test logout with server error"""
        self.mock_auth_service.logout_user.side_effect = Exception("Logout service error")
        
        with patch('autoprojectmanagement.api.auth_endpoints.get_current_user') as mock_current_user:
            mock_current_user.return_value = {"sub": "123"}
            
            response = client.post("/logout", json={})
            
            assert response.status_code == 500
            assert "Logout failed" in response.json()["detail"]

    def test_refresh_token_server_error(self):
        """Test token refresh with server error"""
        self.mock_auth_service.refresh_access_token.side_effect = Exception("Token service error")
        
        response = client.post("/refresh-token", json={"refresh_token": "test_token"})
        
        assert response.status_code == 500
        assert "Token refresh failed" in response.json()["detail"]

    def test_get_profile_server_error(self):
        """Test profile retrieval with server error"""
        self.mock_auth_service.get_user_by_id.side_effect = Exception("Profile service error")
        
        with patch('autoprojectmanagement.api.auth_endpoints.get_current_user') as mock_current_user:
            mock_current_user.return_value = {"sub": "123"}
            
            response = client.get("/profile", headers={"Authorization": "Bearer test_token"})
            
            assert response.status_code == 500
            assert "Profile retrieval failed" in response.json()["detail"]

    # Integration Tests (5 tests)
    def test_get_current_user_valid_token(self):
        """Test get_current_user dependency with valid token"""
        self.mock_auth_service.validate_token.return_value = {"sub": "123", "email": "test@example.com"}
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")
        result = get_current_user(credentials)
        
        assert result["sub"] == "123"
        assert result["email"] == "test@example.com"
        self.mock_auth_service.validate_token.assert_called_once_with("valid_token")

    def test_get_current_user_invalid_token(self):
        """Test get_current_user dependency with invalid token"""
        self.mock_auth_service.validate_token.return_value = None
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials)
        
        assert exc_info.value.status_code == 401
        assert "Invalid or expired token" in exc_info.value.detail

    def test_auth_config_endpoint(self):
        """Test authentication configuration endpoint"""
        response = client.get("/config")
        
        assert response.status_code == 200
        assert "password_min_length" in response.json()
        assert "password_requirements" in response.json()

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "authentication"

    def test_password_reset_flow(self):
        """Test password reset request and confirmation flow"""
        # Test password reset request
        self.mock_auth_service.request_password_reset.return_value = (True, "Reset email sent")
        response = client.post("/request-password-reset", json={"email": "test@example.com"})
        assert response.status_code == 200
        assert response.json()["success"] == True
        
        # Test password reset confirmation
        self.mock_auth_service.reset_password.return_value = (True, "Password reset successful")
        response = client.post("/reset-password", json={"token": "reset_token", "new_password": "NewPassword123!"})
        assert response.status_code == 200
        assert response.json()["success"] == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
