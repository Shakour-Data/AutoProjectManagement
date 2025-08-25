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
    
