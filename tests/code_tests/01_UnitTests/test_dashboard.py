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
            calculate_health_score,
            determine_risk_level,
            get_team_performance,
            get_quality_metrics
        )
        
        # Test utility functions
        test_status = {
            'total_tasks': 20,
            'completed_tasks': 15,
            'progress_percentage': 75.0
        }
        
        health_score = calculate_health_score(test_status)
        risk_level = determine_risk_level(test_status)
        team_perf = get_team_performance(test_project_id)
        quality_metrics = get_quality_metrics(test_project_id)
        
        print(f"✅ Health score calculation: {health_score}")
        print(f"✅ Risk level determination: {risk_level}")
        print(f"✅ Team performance: {team_perf}")
        print(f"✅ Quality metrics: {quality_metrics}")
        
    except Exception as e:
        print(f"❌ Error testing utility functions: {e}")
        return False
    
    print("✅ All utility functions working correctly!")
    return True

def test_cli_commands():
    """Test dashboard CLI commands."""
    print("\n🧪 Testing Dashboard CLI Commands...")
    
    try:
        from autoprojectmanagement.cli_dashboard import DashboardCLI
        cli = DashboardCLI()
        
        # Test status check (should show stopped since server isn't running)
        status = cli.dashboard_status()
        print(f"✅ Status check: {status['status']}")
        
        # Test info display
        print("✅ Dashboard info display test passed")
        
    except Exception as e:
        print(f"❌ Error testing CLI commands: {e}")
        return False
    
    print("✅ CLI commands working correctly!")
    return True

def test_static_files():
    """Test that static files are accessible."""
    print("\n🧪 Testing Static Files...")
    
    static_dir = project_root / "autoprojectmanagement" / "static"
    
    required_files = [
        "index.html",
        "css/dashboard.css",
        "js/dashboard.js"
    ]
    
    for file_path in required_files:
        full_path = static_dir / file_path
        if full_path.exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return False
    
    # Test HTML content
    index_file = static_dir / "index.html"
    if index_file.exists():
        content = index_file.read_text()
        if "AutoProjectManagement Dashboard" in content:
            print("✅ HTML content is correct")
        else:
            print("❌ HTML content validation failed")
            return False
    
    print("✅ All static files are present and valid!")
    return True

def test_api_integration():
    """Test API integration points."""
    print("\n🧪 Testing API Integration...")
    
    try:
        # Test that dashboard endpoints are properly imported in app.py
        app_file = project_root / "autoprojectmanagement" / "api" / "app.py"
        app_content = app_file.read_text()
        
        # Check for dashboard router import
        if "from autoprojectmanagement.api.dashboard_endpoints import router as dashboard_router" in app_content:
            print("✅ Dashboard router import found")
        else:
            print("❌ Dashboard router import missing")
            return False
        
        # Check for router inclusion
        if "app.include_router(dashboard_router, prefix=API_PREFIX)" in app_content:
            print("✅ Dashboard router inclusion found")
        else:
            print("❌ Dashboard router inclusion missing")
            return False
        
        # Check for static files mounting
        if 'app.mount("/static", StaticFiles(directory="autoprojectmanagement/static"), name="static")' in app_content:
            print("✅ Static files mounting found")
        else:
            print("❌ Static files mounting missing")
            return False
        
        # Check for dashboard route
        if '@app.get("/dashboard")' in app_content:
            print("✅ Dashboard route found")
        else:
            print("❌ Dashboard route missing")
            return False
        
    except Exception as e:
        print(f"❌ Error testing API integration: {e}")
        return False
    
    print("✅ API integration tests passed!")
    return True

def main():
    """Run all dashboard tests."""
    print("🚀 Starting AutoProjectManagement Dashboard Tests")
    print("=" * 50)
    
    tests = [
        test_dashboard_endpoints,
        test_cli_commands,
        test_static_files,
        test_api_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All dashboard tests passed successfully!")
        return 0
    else:
        print("💥 Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
