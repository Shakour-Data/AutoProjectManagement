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
