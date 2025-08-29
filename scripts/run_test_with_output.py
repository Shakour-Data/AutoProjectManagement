#!/usr/bin/env python3
"""
Run test and capture output to file
"""

import subprocess
import sys
from pathlib import Path

def run_test():
    """Run the test and capture output"""
    # Add src to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root / "src"))
    
    # Run pytest with output capture
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/code_tests/01_UnitTests/api/test_auth_models.py", 
        "-v"
    ], capture_output=True, text=True, cwd=project_root)
    
    # Write results to file
    with open("test_results_final.txt", "w") as f:
        f.write("=" * 50 + "\n")
        f.write("TEST RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Exit Code: {result.returncode}\n\n")
        f.write("STDOUT:\n")
        f.write(result.stdout + "\n")
        f.write("STDERR:\n")
        f.write(result.stderr + "\n")
    
    print(f"Test completed. Results saved to test_results_final.txt")
    print(f"Exit code: {result.returncode}")

if __name__ == "__main__":
    run_test()
