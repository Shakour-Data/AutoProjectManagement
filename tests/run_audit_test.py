#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
import subprocess

def run_tests():
    try:
        # Run the specific test file
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'test_github_integration_audit.py', 
            '-v', '--tb=long'
        ], cwd='tests', capture_output=True, text=True, timeout=30)
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("Test execution timed out")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
