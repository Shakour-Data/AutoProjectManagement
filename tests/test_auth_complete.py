#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: test_auth_complete.py
File: test_auth_complete.py
Purpose: Complete authentication system test
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
"""

import sys
import os
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_authentication_system():
    """Test the complete authentication system."""
    print("🧪 Testing Complete Authentication System")
    print("=" * 60)
    
    try:
        # Import all required modules
        print("1. Importing modules...")
        from autoprojectmanagement.services.auth_service import auth_service
        from autoprojectmanagement.api.auth_models import UserRegisterRequest, UserLoginRequest
        from autoprojectmanagement.storage.user_storage import user_storage_service
        from autoprojectmanagement.utils.security import password_hasher, token_manager
        
        print("✅ Modules imported successfully")
        
        # Initialize storage
        print("2. Initializing storage...")
        user_storage_service.load_data()
        print("✅ Storage initialized")
        
        # Test password hashing
        print("3. Testing password hashing...")
        password = "SecurePass123!"
        hashed_password = password_hasher.hash_password(password)
        is_valid = password_hasher.verify_password(password, hashed_password)
        print(f"✅ Password hashing test: {'PASSED' if is_valid else 'FAILED'}")
        
        # Test user registration
        print("4. Testing user registration...")
        user_data = UserRegisterRequest(
            email="test@example.com",
            password="SecurePass123!",
            first_name="Test",
            last_name="User"
        )
        
        success, message, user_profile = auth_service.register_user(user_data)
        print(f"✅ Registration: {'SUCCESS' if success else 'FAILED'} - {message}")
        
        if success:
            print(f"   User ID: {user_profile.user_id}")
            print(f"   Email: {user_profile.email}")
        
        # Test user login
        print("5. Testing user login...")
        login_data = UserLoginRequest(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        success, message, auth_data = auth_service.login_user(login_data)
        print(f"✅ Login: {'SUCCESS' if success else 'FAILED'} - {message}")
        
        if success:
            print(f"   Access Token: {auth_data['access_token'][:30]}...")
            print(f"   User: {auth_data['user']['first_name']} {auth_data['user']['last_name']}")
        
        # Test token validation
        print("6. Testing token validation...")
        if success:
            token = auth_data['access_token']
            payload = auth_service.validate_token(token)
            print(f"✅ Token validation: {'SUCCESS' if payload else 'FAILED'}")
            
            if payload:
                print(f"   User ID: {payload.get('sub')}")
                print(f"   Email: {payload.get('email')}")
        
        print("\n" + "=" * 60)
        print("🎉 Authentication system test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_authentication_system()
    sys.exit(0 if success else 1)
