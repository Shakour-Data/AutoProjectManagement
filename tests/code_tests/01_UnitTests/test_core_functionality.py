#!/usr/bin/env python3
"""
Core functionality test for advanced dashboard commands.
Tests the core logic without API dependencies.
"""

import json
import tempfile
from pathlib import Path
from autoprojectmanagement.cli_dashboard import DashboardCLI

def test_cron_validation_comprehensive():
    """Test comprehensive cron expression validation."""
    print("🧪 Testing comprehensive cron validation...")
    cli = DashboardCLI()
    
    test_cases = [
        # Valid expressions
        ("0 9 * * *", True, "Daily at 9 AM"),
        ("*/5 * * * *", True, "Every 5 minutes"),
        ("0 0 * * 0", True, "Weekly on Sunday"),
        ("0 12 1 * *", True, "Monthly on 1st at noon"),
        ("30 14 * * 1-5", True, "Weekdays at 2:30 PM"),
        ("0 */2 * * *", True, "Every 2 hours"),
        ("0 0 1,15 * *", True, "1st and 15th of month"),
        
        # Invalid expressions
        ("invalid", False, "Invalid format"),
        ("0 9 * *", False, "Missing field"),
        ("0 9 * * * *", False, "Too many fields"),
        ("60 * * * *", False, "Invalid minute"),
        ("0 24 * * *", False, "Invalid hour"),
        ("0 0 32 * *", False, "Invalid day of month"),
        ("0 0 * 13 *", False, "Invalid month"),
        ("0 0 * * 7", False, "Invalid day of week"),
        ("0 0/0 * * *", False, "Zero step"),
        ("0 -1 * * *", False, "Negative value"),
    ]
    
    results = []
    for expr, expected, description in test_cases:
        result = cli._validate_cron_expression(expr)
        status = "✅" if result == expected else "❌"
        print(f"{status} {expr} - {description} - Expected: {expected}, Got: {result}")
        results.append(result == expected)
    
    passed = sum(results)
    total = len(results)
    print(f"📊 Cron validation: {passed}/{total} passed")
    return passed == total

def test_file_operations():
    """Test file operations for configuration and scheduling."""
    print("🧪 Testing file operations...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test configuration file handling
        config_file = Path(temp_dir) / "test_config.json"
        
        # Test writing config
        config_data = {"refresh_rate": 5000, "theme": "dark"}
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        # Test reading config
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            success = loaded_config == config_data
            print(f"✅ Config file test: {success}")
        else:
            print("❌ Config file not created")
            success = False
        
        # Test schedule file handling
        schedule_file = Path(temp_dir) / "test_schedules.json"
        schedules = [
            {"report_type": "overview", "schedule": "0 9 * * *"},
            {"report_type": "metrics", "schedule": "0 * * * *"}
        ]
        
        with open(schedule_file, 'w', encoding='utf-8') as f:
            json.dump(schedules, f, indent=2)
        
        if schedule_file.exists():
            with open(schedule_file, 'r', encoding='utf-8') as f:
                loaded_schedules = json.load(f)
            success = success and (loaded_schedules == schedules)
            print(f"✅ Schedule file test: {loaded_schedules == schedules}")
        else:
            print("❌ Schedule file not created")
            success = False
    
    print(f"✅ File operations test completed: {success}")
    return success

def test_next_run_calculation():
    """Test next run time calculation."""
    print("🧪 Testing next run calculation...")
    cli = DashboardCLI()
    
    # Test with valid expression
    next_run = cli._calculate_next_run("0 9 * * *")
    print(f"✅ Next run for '0 9 * * *': {next_run}")
    
    # Should return a string (either actual time or fallback message)
    success = isinstance(next_run, str) and len(next_run) > 0
    print(f"✅ Next run calculation test: {success}")
    return success

def test_widget_management():
    """Test widget management functionality."""
    print("🧪 Testing widget management...")
    cli = DashboardCLI()
    
    # Test default widget list
    widgets = cli.get_available_widgets()
    print(f"✅ Default widgets: {widgets}")
    
    # Should return a list (even if empty)
    success = isinstance(widgets, list)
    print(f"✅ Widget management test: {success}")
    return success

def main():
    """Run core functionality tests."""
    print("🚀 Starting Core Functionality Tests\n")
    
    tests = [
        test_cron_validation_comprehensive,
        test_file_operations,
        test_next_run_calculation,
        test_widget_management,
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
    
    print("📊 Core Functionality Test Results:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All core functionality tests passed!")
        return 0
    else:
        print("❌ Some core functionality tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
