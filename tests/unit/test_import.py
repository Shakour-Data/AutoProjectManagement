import sys
from pathlib import Path

# Add source to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from autoprojectmanagement.api.auth_models import UserRegisterRequest
    print("✅ Import successful!")
    
    # Test creating a user
    data = {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    user = UserRegisterRequest(**data)
    print(f"✅ User created: {user.email}")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
