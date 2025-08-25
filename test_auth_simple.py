#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from autoprojectmanagement.services.auth_service import auth_service
from autoprojectmanagement.api.auth_models import UserRegisterRequest, UserLoginRequest
from autoprojectmanagement.storage.user_storage import user_storage_service

def test_auth_service():
    print("🧪 Testing Authentication Service")
    print("=" * 50)
    
    # Initialize storage
    user_storage_service.load_data()
    
    # Test data
    test_user = UserRegisterRequest(
        email="test@example.com",
        password="SecurePass123!",
        first_name="Test",
        last_name="User"
    )
    
    # Test 1: User Registration
    print("\n1. Testing User Registration...")
    success, message, user_profile = auth_service.register_user(test_user)
    
    if success:
        print(f"✅ Registration successful: {message}")
        print(f"   User ID: {user_profile.user_id}")
        print(f"   Email: {user_profile.email}")
    else:
        print(f"❌ Registration failed: {message}")
        return False
    
    # Test 2: User Login
    print("\n2. Testing User Login...")
    login_data = UserLoginRequest(
        email="test@example.com",
        password="SecurePass123!"
    )
    
