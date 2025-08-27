#!/usr/bin/env python3
print("Simple test script running")
print("Testing basic Python functionality")

# Test basic imports
try:
    import sys
    import pytest
    from pathlib import Path
    print("✓ All imports successful")
    
    # Test path setup
    sys.path.insert(0, 'src')
    print("✓ Path setup successful")
    
    # Test model import
    try:
        from autoprojectmanagement.api.auth_models import UserRegisterRequest
        print("✓ Model import successful")
        
        # Test model creation
        req = UserRegisterRequest(
            email='test@example.com',
            password='Test123!',
            first_name='Test',
            last_name='User'
        )
        print(f"✓ Model creation successful: {req.email}")
        
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"✗ Import test failed: {e}")
    import traceback
    traceback.print_exc()

print("Test script completed")
