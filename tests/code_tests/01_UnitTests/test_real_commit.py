#!/usr/bin/env python3
"""
Test script to verify real auto-commit functionality
"""

import os
import subprocess
from autoprojectmanagement.services.automation_services.auto_commit import UnifiedAutoCommit

def test_real_commit():
    """Test that real git operations are working"""
    print("Testing real auto-commit functionality...")
    
    # Create a test file
    test_file = "test_commit_file.txt"
    with open(test_file, "w") as f:
        f.write("Test file for auto-commit verification")
    
    # Run auto-commit
    auto_commit = UnifiedAutoCommit()
    success = auto_commit.run_complete_workflow_guaranteed()
    
    if success:
        print("✅ Real auto-commit executed successfully!")
        
        # Check if commit was actually made
        try:
            result = subprocess.run(["git", "log", "--oneline", "-1"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Latest commit: {result.stdout.strip()}")
            else:
                print("❌ No commits found")
        except Exception as e:
            print(f"❌ Error checking git log: {e}")
    else:
        print("❌ Auto-commit failed")
    
    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_real_commit()
