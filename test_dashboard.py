#!/usr/bin/env python3
"""
Test script for AutoProjectManagement Dashboard functionality.

This script tests the dashboard API endpoints and CLI commands to ensure
they are working correctly.
"""

import sys
import os
import json
import requests
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_dashboard_endpoints():
    """Test dashboard API endpoints."""
    print("🧪 Testing Dashboard API Endpoints...")
    
    # Test data for mock responses
    test_project_id = "test-project-123"
    
    # Import the dashboard endpoints to test the utility functions
    try:
        from autoprojectmanagement.api.dashboard_endpoints import (
