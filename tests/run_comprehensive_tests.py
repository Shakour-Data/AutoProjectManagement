#!/usr/bin/env python3
"""
Comprehensive test runner for AutoProjectManagement system
This script runs all unit tests and provides detailed reporting
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_unit_tests():
    """Run all unit tests with coverage reporting"""
    print("🧪 Running comprehensive unit tests for AutoProjectManagement...")
    
    # Test configuration
    test_args = [
        "python", "-m", "pytest",
        "tests/code_tests/UnitTests",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",
        "--disable-warnings",
        "--cov=autoprojectmanagement",
        "--cov-report=term-missing",
        "--cov-report=html:coverage_html",
        "--cov-report=xml:coverage.xml",
        "--cov-branch",
        "--cov-fail-under=80",
        "-x",  # Stop on first failure
        "--durations=10",  # Show 10 slowest tests
    ]
    
    try:
        result = subprocess.run(test_args, capture_output=True, text=True)
        
        # Save test results
        test_results = {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timestamp": str(pd.Timestamp.now()) if 'pd' in globals() else str(datetime.now())
        }
        
        with open("test_results.json", "w") as f:
            json.dump(test_results, f, indent=2)
        
        print("\n" + "="*60)
        print("📊 TEST RESULTS SUMMARY")
        print("="*60)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed")
            print("\nSTDOUT:")
            print(result.stdout)
            print("\nSTDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_specific_test_module(module_name):
    """Run tests for a specific module"""
    print(f"🧪 Running tests for module: {module_name}")
    
    test_path = f"tests/code_tests/UnitTests/{module_name}"
    
    test_args = [
        "python", "-m", "pytest",
        test_path,
        "-v",
        "--tb=short",
        "--cov=autoprojectmanagement",
        "--cov-report=term-missing",
        "-s"  # Capture output
    ]
    
    try:
        subprocess.run(test_args, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def generate_test_report():
    """Generate comprehensive test report"""
    print("📋 Generating test report...")
    
    report_data = {
        "project": "AutoProjectManagement",
        "test_type": "Unit Tests",
        "modules_tested": [
            "task_management",
            "resource_management", 
            "progress_calculator",
            "auto_commit",
            "backup_manager",
            "github_integration"
        ],
        "coverage_threshold": 80,
        "test_framework": "pytest"
    }
    
    with open("test_report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    
    print("✅ Test report generated: test_report.json")

def setup_test_environment():
    """Set up test environment"""
    print("🔧 Setting up test environment...")
    
    # Ensure test directories exist
    test_dirs = [
        "tests/code_tests/UnitTests/test_main_modules",
        "tests/code_tests/UnitTests/test_services",
        "coverage_html"
    ]
    
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Install test dependencies
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"], 
                      check=True, capture_output=True)
        print("✅ Test dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not install test dependencies: {e}")

def main():
    """Main test runner function"""
    print("🚀 AutoProjectManagement Unit Test Suite")
    print("=" * 50)
    
    # Setup
    setup_test_environment()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        module_name = sys.argv[1]
        success = run_specific_test_module(module_name)
    else:
        success = run_unit_tests()
        generate_test_report()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
