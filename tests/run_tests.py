#!/usr/bin/env python3
"""
Comprehensive test runner for AutoProjectManagement package.
"""
import os
import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all tests."""
    test_root = Path(__file__).parent
    
    print("🧪 Running AutoProjectManagement Tests...")
    print("=" * 50)
    
    # Run unit tests
    print("\n📊 Unit Tests:")
    result = subprocess.run([
        "pytest", "unit_tests/", "-v", "--tb=short"
    ], cwd=test_root)
    
    if result.returncode != 0:
        print("❌ Unit tests failed")
        return False
    
    # Run integration tests
    print("\n🔗 Integration Tests:")
    result = subprocess.run([
        "pytest", "integration_tests/", "-v", "--tb=short"
    ], cwd=test_root)
    
    if result.returncode != 0:
        print("❌ Integration tests failed")
        return False
    
    # Run system tests
    print("\n🎯 System Tests:")
    result = subprocess.run([
        "pytest", "system_tests/", "-v", "--tb=short"
    ], cwd=test_root)
    
    if result.returncode != 0:
        print("❌ System tests failed")
        return False
    
    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
