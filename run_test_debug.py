#!/usr/bin/env python3
"""
Debug script to run tests and capture output
"""

import subprocess
import sys
from pathlib import Path

def run_test():
    """Run the auth_models test and capture output"""
    print("Running auth_models test...")
    
    # Add src to path for imports
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root / "src"))
    
    # Run the test
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/code_tests/01_UnitTests/api/test_auth_models.py", 
        "-v"
    ], capture_output=True, text=True, cwd=project_root)
    
    # Write results to file
    with open("test_debug_output.txt", "w") as f:
        f.write(f"Exit code: {result.returncode}\n")
        f.write(f"STDOUT:\n{result.stdout}\n")
        f.write(f"STDERR:\n{result.stderr}\n")
    
    print(f"Results written to test_debug_output.txt")
    print(f"Exit code: {result.returncode}")
    
    if result.stdout:
        print("STDOUT contains output")
    if result.stderr:
        print("STDERR contains output")

if __name__ == "__main__":
    run_test()
