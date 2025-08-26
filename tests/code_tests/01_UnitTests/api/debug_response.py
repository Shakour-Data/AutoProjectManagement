#!/usr/bin/env python3
"""
Debug script to check the actual response format from the API
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient
import importlib.util

# Add src directory to path for imports
src_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import the module directly
spec = importlib.util.spec_from_file_location(
    "main", 
    str(src_path / "autoprojectmanagement" / "api" / "main.py")
)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

# Import the app
app = main.app

# Create a test client for the FastAPI app
client = TestClient(app)

# Test invalid format
print("Testing invalid format response:")
response = client.get("/api/v1/projects/123/status?format=invalid")
print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Content: {response.text}")
try:
    print(f"JSON: {response.json()}")
except Exception as e:
    print(f"JSON parsing error: {e}")
print()

# Test not found
print("Testing not found response:")
from fastapi import HTTPException
from unittest.mock import patch

with patch('autoprojectmanagement.api.app.project_service.get_status') as mock_get_status:
    mock_get_status.side_effect = HTTPException(status_code=404, detail="Project '999' not found")
    response = client.get("/api/v1/projects/999/status")
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text}")
    try:
        print(f"JSON: {response.json()}")
    except Exception as e:
        print(f"JSON parsing error: {e}")
