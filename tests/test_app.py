#!/usr/bin/env python3
"""
Test script to check the FastAPI app instance.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

try:
    from autoprojectmanagement.api.app import app
    print("App imported successfully")
    print(f"App type: {type(app)}")
    print(f"App is callable: {callable(app)}")
    
    # Test if it's a FastAPI instance
    from fastapi import FastAPI
    print(f"Is FastAPI instance: {isinstance(app, FastAPI)}")
    
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()
