#!/usr/bin/env python3
"""
Test if auth_models can be imported
"""

import sys
from pathlib import Path

# Add source to path
current_file = Path(__file__)
project_root = current_file.parent
sys.path.insert(0, str(project_root / "src"))
print(f"Added to path: {project_root / 'src'}")

try:
    from autoprojectmanagement.api.auth_models import UserRegisterRequest
    print("SUCCESS: UserRegisterRequest imported successfully")
except ImportError as e:
    print(f"FAILED: {e}")
    print("Try: pip install email-validator")
except Exception as e:
    print(f"ERROR: {e}")
