#!/usr/bin/env python3
"""
Check if the Python environment is working correctly
"""

import sys
import os
from pathlib import Path

def check_environment():
    """Check basic environment functionality"""
    print("Checking Python environment...")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check if src directory exists
    src_dir = current_dir / "src"
    print(f"src directory exists: {src_dir.exists()}")
    
    # Check if test file exists
    test_file = current_dir / "tests" / "code_tests" / "01_UnitTests" / "api" / "test_auth_models.py"
    print(f"Test file exists: {test_file.exists()}")
    
    # Try to write to a file
    test_output = current_dir / "environment_check.txt"
    try:
        with open(test_output, "w") as f:
            f.write("Environment check successful\n")
            f.write(f"Python: {sys.version}\n")
            f.write(f"Directory: {current_dir}\n")
        print(f"✅ Successfully wrote to {test_output}")
    except Exception as e:
        print(f"❌ Error writing to file: {e}")

if __name__ == "__main__":
    check_environment()
