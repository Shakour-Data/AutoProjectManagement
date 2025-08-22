#!/usr/bin/env python3
"""
Test script for advanced dashboard CLI commands.
This script tests the new advanced dashboard functionality.
"""

import json
import os
import tempfile
from pathlib import Path
from autoprojectmanagement.cli_dashboard import DashboardCLI

def test_create_custom_view():
    """Test creating a custom dashboard view."""
    print("🧪 Testing create_custom_view...")
    cli = DashboardCLI()
    
    # Test with minimal parameters
    success = cli.create_custom_view(
        layout_name="test_view",
        widgets=["health", "progress"],
        refresh_rate=5000,
        theme="light"
    )
    
    print(f"✅ Create custom view test completed: {success}")
    return success

def test_share_dashboard_view():
    """Test sharing dashboard view."""
    print("🧪 Testing share_dashboard_view...")
    cli = DashboardCLI()
    
    # Test JSON export
    success = cli.share_dashboard_view("standard", "json")
    
    # Check if file was created
    json_files = list(Path(".").glob("dashboard_view_standard_*.json"))
    if json_files:
        print(f"✅ JSON export file created: {json_files[0]}")
        success = True
    else:
        print("❌ JSON export file not found")
        success = False
    
    print(f"✅ Share dashboard view test completed: {success}")
    return success

def test_schedule_report():
    """Test scheduling automated reports."""
    print("🧪 Testing schedule_report...")
    cli = DashboardCLI()
    
    # Test valid cron expression
    success = cli.schedule_report("overview", "0 9 * * *", "markdown")
    
    # Check if schedule file was created
    schedule_file = Path("JSonDataBase/OutPuts/dashboard_schedules.json")
    if schedule_file.exists():
        with open(schedule_file, 'r') as f:
            schedules = json.load(f)
            if any(s.get('report_type') == 'overview' for s in schedules):
                print("✅ Schedule configuration saved successfully")
                success = True
            else:
                print("❌ Schedule not found in configuration")
                success = False
    else:
        print("❌ Schedule file not created")
        success = False
    
    print(f"✅ Schedule report test completed: {success}")
    return success

def test_analyze_dashboard_data():
    """Test dashboard data analysis."""
    print("🧪 Testing analyze_dashboard_data...")
    cli = DashboardCLI()
    
    # Test overview analysis
    success = cli.analyze_dashboard_data("overview", "24h")
    
    # Check if analysis file was created
    analysis_files = list(Path(".").glob("dashboard_analysis_overview_*.md"))
    if analysis_files:
        print(f"✅ Analysis file created: {analysis_files[0]}")
        success = True
    else:
        print("❌ Analysis file not found")
        success = False
    
    print(f"✅ Analyze dashboard data test completed: {success}")
    return success

def test_configure_dashboard():
    """Test dashboard configuration."""
    print("🧪 Testing configure_dashboard...")
    cli = DashboardCLI()
    
    # Test specific setting configuration
    success = cli.configure_dashboard("refresh_rate", "5000")
    
    # Check if config file was created/updated
    config_file = Path("JSonDataBase/OutPuts/dashboard_config.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            if config.get("refresh_rate") == 5000:
                print("✅ Configuration updated successfully")
                success = True
            else:
                print("❌ Configuration not updated correctly")
                success = False
    else:
        print("❌ Config file not created")
        success = False
    
    print(f"✅ Configure dashboard test completed: {success}")
    return success

def test_cron_validation():
    """Test cron expression validation."""
    print("🧪 Testing cron validation...")
    cli = DashboardCLI()
    
    # Test valid expressions
    valid_expressions = [
        "0 9 * * *",      # Daily at 9 AM
        "*/5 * * * *",    # Every 5 minutes
        "0 0 * * 0",      # Weekly on Sunday
        "0 12 1 * *",     # Monthly on 1st at noon
    ]
    
    # Test invalid expressions
    invalid_expressions = [
        "invalid",
        "0 9 * *",        # Missing field
        "0 9 * * * *",    # Too many fields
        "60 * * * *",     # Invalid minute
    ]
    
    all_valid = True
    
    for expr in valid_expressions:
        if not cli._validate_cron_expression(expr):
            print(f"❌ Valid expression failed: {expr}")
            all_valid = False
    
    for expr in invalid_expressions:
        if cli._validate_cron_expression(expr):
            print(f"❌ Invalid expression passed: {expr}")
            all_valid = False
    
    print(f"✅ Cron validation test completed: {all_valid}")
    return all_valid

def main():
    """Run all tests."""
    print("🚀 Starting Advanced Dashboard Commands Tests\n")
    
    # Create output directory
    Path("JSonDataBase/OutPuts").mkdir(parents=True, exist_ok=True)
    
    tests = [
        test_cron_validation,
        test_create_custom_view,
        test_share_dashboard_view,
        test_schedule_report,
        test_analyze_dashboard_data,
        test_configure_dashboard,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("📊 Test Results Summary:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
