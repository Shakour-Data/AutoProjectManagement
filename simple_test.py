#!/usr/bin/env python3
"""
Simple test to verify auth_models functionality
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from autoprojectmanagement.api.auth_models import UserRegisterRequest, UserLoginRequest
    
    print("✅ Import successful!")
    
    # Test UserRegisterRequest
    print("\n🧪 Testing UserRegisterRequest...")
    user_data = {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    user = UserRegisterRequest(**user_data)
    print(f"✅ User created: {user.email}")
    
    # Test UserLoginRequest
    print("\n🧪 Testing UserLoginRequest...")
    login_data = {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    login = UserLoginRequest(**login_data)
    print(f"✅ Login created: {login.email}")
    
    print("\n🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
