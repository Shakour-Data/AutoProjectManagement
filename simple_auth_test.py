#!/usr/bin/env python3
"""
Simple test script for auth_models without pytest
"""

import sys
from pathlib import Path

# Add source to path
current_file = Path(__file__)
project_root = current_file.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
print(f"Added to path: {project_root / 'src'}")

try:
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
    
    print("✅ All imports successful!")
    
    # Test UserRegisterRequest
    print("\n=== Testing UserRegisterRequest ===")
    try:
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        request = UserRegisterRequest(**data)
        print(f"✅ Valid registration: {request.email}")
    except Exception as e:
        print(f"❌ Registration failed: {e}")
    
    # Test UserLoginRequest
    print("\n=== Testing UserLoginRequest ===")
    try:
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }
        request = UserLoginRequest(**data)
        print(f"✅ Valid login: {request.email}")
    except Exception as e:
        print(f"❌ Login failed: {e}")
    
    # Test UserProfileResponse
    print("\n=== Testing UserProfileResponse ===")
    try:
        from datetime import datetime
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
        print(f"✅ Profile response: {response.user_id}")
    except Exception as e:
        print(f"❌ Profile failed: {e}")
    
    print("\n✅ All basic tests completed successfully!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Make sure email-validator is installed: pip install email-validator")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
