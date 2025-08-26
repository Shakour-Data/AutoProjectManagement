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
    
    success, message, auth_data = auth_service.login_user(login_data)
    
    if success:
        print(f"✅ Login successful: {message}")
        print(f"   Access Token: {auth_data['access_token'][:30]}...")
        print(f"   User: {auth_data['user']['first_name']} {auth_data['user']['last_name']}")
    else:
        print(f"❌ Login failed: {message}")
        return False
    
    # Test 3: Token Validation
    print("\n3. Testing Token Validation...")
    token = auth_data['access_token']
    payload = auth_service.validate_token(token)
    
    if payload:
        print(f"✅ Token validation successful")
        print(f"   User ID: {payload.get('sub')}")
        print(f"   Email: {payload.get('email')}")
    else:
        print(f"❌ Token validation failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Authentication service tests passed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = test_auth_service()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"💥 Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
