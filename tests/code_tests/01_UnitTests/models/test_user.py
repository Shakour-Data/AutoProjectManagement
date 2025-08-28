import pytest
from datetime import datetime, timedelta
from src.autoprojectmanagement.models.user import (
    UserBase, UserCreate, UserLogin, UserUpdate, PasswordResetRequest, 
    PasswordResetConfirm, UserProfile, UserSession, PasswordResetToken, 
    EmailVerificationToken, generate_user_id, generate_session_id, 
    generate_reset_token, generate_verification_token, calculate_token_expiry,
    calculate_session_expiry, user_storage
)

def test_user_base_creation():
    """Test UserBase model creation with valid data"""
    user = UserBase(
        email="test@example.com",
        first_name="John",
        last_name="Doe"
    )
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"

def test_user_base_email_lowercase():
    """Test UserBase email validation ensures lowercase"""
    user = UserBase(
        email="TEST@EXAMPLE.COM",
        first_name="John",
        last_name="Doe"
    )
    assert user.email == "test@example.com"

def test_user_create_password_strength():
    """Test UserCreate password strength validation"""
    # Valid password
    user = UserCreate(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        password="StrongPass123"
    )
    assert user.password == "StrongPass123"

def test_user_create_invalid_password():
    """Test UserCreate with invalid password raises validation error"""
    with pytest.raises(ValueError):
        UserCreate(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="weak"  # Too short
        )

def test_user_profile_creation():
    """Test UserProfile creation with all required fields"""
    user_id = generate_user_id()
    profile = UserProfile(
        user_id=user_id,
        email="test@example.com",
        first_name="John",
        last_name="Doe"
    )
    assert profile.user_id == user_id
    assert profile.email == "test@example.com"
    assert profile.first_name == "John"
    assert profile.last_name == "Doe"
    assert profile.is_verified is False
    assert profile.is_active is True

def test_user_profile_with_special_characters():
    """Test UserProfile with special characters in names"""
    profile = UserProfile(
        user_id=generate_user_id(),
        email="test@example.com",
        first_name="Jöhn",
        last_name="D'oe-Smith"
    )
    assert profile.first_name == "Jöhn"
    assert profile.last_name == "D'oe-Smith"

def test_user_profile_boundary_values():
    """Test UserProfile with boundary values for names"""
    # Test minimum length names
    profile = UserProfile(
        user_id=generate_user_id(),
        email="test@example.com",
        first_name="J",  # Minimum length
        last_name="D"    # Minimum length
    )
    assert profile.first_name == "J"
    assert profile.last_name == "D"

def test_user_profile_long_names():
    """Test UserProfile with long names (boundary test)"""
    long_name = "A" * 50  # Maximum length
    profile = UserProfile(
        user_id=generate_user_id(),
        email="test@example.com",
        first_name=long_name,
        last_name=long_name
    )
    assert profile.first_name == long_name
    assert profile.last_name == long_name

def test_user_create_missing_uppercase():
    """Test UserCreate with password missing uppercase letter"""
    with pytest.raises(ValueError, match="Password must contain at least one uppercase letter"):
        UserCreate(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="strongpass123"  # No uppercase
        )

def test_user_create_missing_lowercase():
    """Test UserCreate with password missing lowercase letter"""
    with pytest.raises(ValueError, match="Password must contain at least one lowercase letter"):
        UserCreate(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="STRONGPASS123"  # No lowercase
        )

def test_user_create_missing_digit():
    """Test UserCreate with password missing digit"""
    with pytest.raises(ValueError, match="Password must contain at least one digit"):
        UserCreate(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="StrongPassword"  # No digit
        )

def test_user_create_empty_names():
    """Test UserCreate with empty names raises validation error"""
    with pytest.raises(ValueError):
        UserBase(
            email="test@example.com",
            first_name="",  # Empty
            last_name="Doe"
        )

def test_user_update_optional_fields():
    """Test UserUpdate with optional fields"""
    update = UserUpdate(
        first_name="Jane",
        last_name=None,
        email="jane@example.com"
    )
    assert update.first_name == "Jane"
    assert update.last_name is None
    assert update.email == "jane@example.com"

def test_password_reset_request():
    """Test PasswordResetRequest model"""
    reset_request = PasswordResetRequest(email="test@example.com")
    assert reset_request.email == "test@example.com"

def test_password_reset_confirm():
    """Test PasswordResetConfirm model"""
    reset_confirm = PasswordResetConfirm(
        token="abc123",
        new_password="NewStrongPass123"
    )
    assert reset_confirm.token == "abc123"
    assert reset_confirm.new_password == "NewStrongPass123"

def test_user_session_creation():
    """Test UserSession creation"""
    session = UserSession(
        session_id=generate_session_id(),
        user_id=generate_user_id(),
        token="jwt_token",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(hours=1)
    )
    assert session.session_id is not None
    assert session.user_id is not None
    assert session.token == "jwt_token"

def test_password_reset_token_creation():
    """Test PasswordResetToken creation"""
    token = PasswordResetToken(
        token=generate_reset_token(),
        user_id=generate_user_id(),
        email="test@example.com",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(minutes=30)
    )
    assert token.token is not None
    assert token.user_id is not None
    assert token.email == "test@example.com"
    assert token.used is False

def test_email_verification_token_creation():
    """Test EmailVerificationToken creation"""
    token = EmailVerificationToken(
        token=generate_verification_token(),
        user_id=generate_user_id(),
        email="test@example.com",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(minutes=30)
    )
    assert token.token is not None
    assert token.user_id is not None
    assert token.email == "test@example.com"

def test_user_storage_initialization():
    """Test UserStorage initialization"""
    storage = user_storage
    assert storage.users == {}
    assert storage.sessions == {}
    assert storage.reset_tokens == {}
    assert storage.verification_tokens == {}

# Additional integration tests with auth service can be added here
