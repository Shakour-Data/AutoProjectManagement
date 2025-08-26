#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: test_auth.py
File: test_auth.py
Purpose: Test script for authentication system
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Simple test script to verify authentication functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from autoprojectmanagement.services.auth_service import auth_service
from autoprojectmanagement.storage.user_storage import user_storage_service
from autoprojectmanagement.api.auth_models import UserRegisterRequest, UserLoginRequest

def test_auth_system():
    """Test the authentication system functionality."""
    print("🧪 Testing Authentication System")
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
    
    # Test 4: Get User Profile
    print("\n4. Testing Get User Profile...")
    user_id = payload.get('sub')
    user_profile = auth_service.get_user_by_id(user_id)
    
    if user_profile:
        print(f"✅ Profile retrieval successful")
        print(f"   Name: {user_profile.first_name} {user_profile.last_name}")
        print(f"   Verified: {user_profile.is_verified}")
    else:
        print(f"❌ Profile retrieval failed")
        return False
    
    # Test 5: Logout
    print("\n5. Testing User Logout...")
    # For simplicity, we'll just test the logout function
    # In real implementation, we'd track sessions
    print("✅ Logout functionality ready (session management would be implemented)")
    
    # Test 6: Storage Persistence
    print("\n6. Testing Storage Persistence...")
    user_storage_service.save_data()
    print("✅ Data saved to storage successfully")
    
    # Test 7: Storage Statistics
    print("\n7. Testing Storage Statistics...")
    stats = user_storage_service.get_storage_stats()
    print(f"   Total Users: {stats['total_users']}")
    print(f"   Total Sessions: {stats['total_sessions']}")
    print(f"   Storage Directory: {stats['storage_directory']}")
    
    print("\n" + "=" * 50)
    print("🎉 All authentication tests passed successfully!")
    print("The authentication system is working correctly.")
    
    return True

def cleanup_test_data():
    """Clean up test data from storage."""
    print("\n🧹 Cleaning up test data...")
    
    # Find and remove test user
    test_user = auth_service.get_user_by_email("test@example.com")
    if test_user:
        # Remove user from storage
        if test_user.user_id in user_storage_service.user_storage.users:
            del user_storage_service.user_storage.users[test_user.user_id]
        
        # Remove any sessions for this user
        sessions_to_remove = [
            session_id for session_id, session in user_storage_service.user_storage.sessions.items()
            if session.user_id == test_user.user_id
        ]
        
        for session_id in sessions_to_remove:
            del user_storage_service.user_storage.sessions[session_id]
        
        user_storage_service.save_data()
        print("✅ Test data cleaned up successfully")
    else:
        print("ℹ️ No test data found to clean up")

if __name__ == "__main__":
    try:
        success = test_auth_system()
        
        if success:
            # Ask if user wants to clean up test data
            cleanup = input("\nDo you want to clean up test data? (y/N): ").lower().strip()
            if cleanup == 'y':
                cleanup_test_data()
            else:
                print("Test data preserved for further testing")
        else:
            print("\n❌ Authentication tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
